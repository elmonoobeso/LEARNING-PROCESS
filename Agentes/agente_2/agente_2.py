import os
from pathlib import Path

import pandas as pd
import requests
from dotenv import load_dotenv
from google import genai
from google.genai import errors, types

URL_FDA = "https://api.fda.gov/drug/enforcement.json"
PARAMS_FDA = {"limit": 100}  # filtro tipo query (no es SQL): se puede filtrar, p. ej., por tipo de medicamento
MODELO_GEMINI = "gemini-3.5-flash"  # versión fija: los alias tipo "-latest" pueden desaparecer
TIMEOUT_GEMINI_MS = 90_000  # sin límite, un modelo saturado puede dejar el agente colgado
CLASES_VALIDAS = ["Class I", "Class II", "Class III"]
CAMPOS_OBLIGATORIOS = ["product_description", "reason_for_recall", "recalling_firm"]


def obtencion_datos(url, params):
    """Descarga los registros de retiradas de la FDA.

    Si la petición falla, lanza RuntimeError con el motivo en vez de devolver None
    en silencio: así el error salta donde ocurre y no más adelante.
    """
    try:
        respuesta = requests.get(url, params=params, timeout=15)
        respuesta.raise_for_status()
        datos = respuesta.json()
    except requests.exceptions.Timeout as error:
        raise RuntimeError("La API de la FDA tardó demasiado en responder") from error
    except requests.exceptions.HTTPError as error:
        raise RuntimeError(f"La API de la FDA devolvió un error HTTP: {error}") from error
    except requests.exceptions.ConnectionError as error:
        raise RuntimeError("No se pudo conectar con la API de la FDA") from error
    except ValueError as error:
        raise RuntimeError("La API de la FDA no devolvió un JSON válido") from error
    return datos.get("results", [])


class AgenteFDA:
    def __init__(self):
        self.datos = []
        self.memoria = [{"role": "system", "content": "Eres un analista regulatorio con formación farmacéutica. Tu objetivo es interpretar los datos de alertas y retiradas de medicamentos de la FDA que te proporciona el script, y explicar en lenguaje claro qué patrones o riesgos son relevantes para un farmacéutico."}]

    def agregar_mensaje_usuario(self, mensaje):
        self.memoria.append({"role": "user", "content": mensaje})

    def respuesta_agente(self, respuesta):
        # "model" es el rol que usa Gemini para sus propias respuestas
        self.memoria.append({"role": "model", "content": respuesta})

    def obtener_memoria_completa(self):
        return self.memoria

    def obtener_datos(self):
        self.datos = obtencion_datos(URL_FDA, PARAMS_FDA)

    def validar_clases(self):
        """Separa los registros en válidos y no válidos.

        Grano: una fila = una retirada. Cada registro va a UNA sola lista; si tiene
        varios problemas, se juntan en "motivo_no_valido" en vez de contarlo dos veces.
        openFDA omite los campos vacíos en vez de enviarlos como None, por eso .get().
        """
        validos, no_validos, errores = [], [], []
        for registro in self.datos:
            if not isinstance(registro, dict):
                errores.append({"registro": str(registro)[:200], "error": "el registro no es un diccionario"})
                continue
            motivos = []
            if registro.get("classification") not in CLASES_VALIDAS:
                motivos.append("clasificación no válida")
            vacios = [campo for campo in CAMPOS_OBLIGATORIOS if not registro.get(campo)]
            if vacios:
                motivos.append("faltan campos: " + ", ".join(vacios))
            if motivos:
                no_validos.append({**registro, "motivo_no_valido": "; ".join(motivos)})
            else:
                validos.append(registro)
        return validos, no_validos, errores

    def analisis_estadistico(self, validos, no_validos, errores):
        """Resume los registros. Cada clave del diccionario es una hoja del Excel."""
        df_validos = pd.DataFrame(validos)
        df_no_validos = pd.DataFrame(no_validos)
        if df_validos.empty:
            info_validos = pd.DataFrame()
            resumen_validos = pd.DataFrame()
            por_clasificacion = pd.Series(dtype="int64")
            por_empresa = pd.Series(dtype="int64")
        else:
            info_validos = pd.DataFrame({"tipo_dato": df_validos.dtypes, "no_nulos": df_validos.count(), "nulos": df_validos.isnull().sum()})
            # describe() no puede contar valores únicos de columnas con dicts o listas (p. ej. "openfda")
            simples = [col for col in df_validos.columns if not df_validos[col].map(lambda v: isinstance(v, (dict, list))).any()]
            resumen_validos = df_validos[simples].describe()
            por_clasificacion = df_validos["classification"].value_counts().sort_index()
            por_empresa = df_validos["recalling_firm"].value_counts()
        if df_no_validos.empty:
            motivos_no_validos = pd.Series(dtype="int64")
        else:
            motivos_no_validos = df_no_validos["motivo_no_valido"].value_counts()

        return {
            "info_validos": info_validos,
            "resumen_validos": resumen_validos,
            "por_clasificacion": por_clasificacion,
            "por_empresa": por_empresa,
            "motivos_no_validos": motivos_no_validos,
            "errores": pd.DataFrame(errores),
        }

    def exportar_resultados(self, analisis, carpeta=Path("analisis_es")):
        carpeta.mkdir(exist_ok=True)
        ruta = carpeta / "analisis.xlsx"
        with pd.ExcelWriter(ruta) as writer:
            for nombre_hoja, tabla in analisis.items():
                tabla.to_excel(writer, sheet_name=nombre_hoja)
        return ruta

    def interpretar_analisis(self, analisis):
        api_key = os.environ.get("Gemini_API_KEY")
        if not api_key:
            raise RuntimeError("Falta Gemini_API_KEY en el archivo .env")
        resumen_texto = ""
        for nombre_hoja, tabla in analisis.items():
            resumen_texto += f"\n\n--- {nombre_hoja} ---\n{tabla.to_string()}"
        self.agregar_mensaje_usuario(
            f"Aquí tienes el análisis de recalls de la FDA. Explícame qué es lo más relevante:{resumen_texto}")
        cliente = genai.Client(api_key=api_key, http_options=types.HttpOptions(timeout=TIMEOUT_GEMINI_MS))
        respuesta = cliente.models.generate_content(
            model=MODELO_GEMINI,
            contents=self.memoria[-1]["content"],
            config=types.GenerateContentConfig(system_instruction=self.memoria[0]["content"]),
        )
        self.respuesta_agente(respuesta.text)
        return respuesta.text


def main():
    load_dotenv()
    agente = AgenteFDA()
    try:
        agente.obtener_datos()
    except RuntimeError as error:
        print(f"No se pudieron obtener los datos: {error}")
        return 1
    validos, no_validos, errores = agente.validar_clases()
    print(f"{len(agente.datos)} registros: {len(validos)} válidos, {len(no_validos)} no válidos, {len(errores)} con error")
    analisis = agente.analisis_estadistico(validos, no_validos, errores)
    ruta = agente.exportar_resultados(analisis)
    print(f"Excel generado en {ruta}")
    try:
        print(agente.interpretar_analisis(analisis))
    except (RuntimeError, errors.APIError) as error:
        print(f"No se pudo generar la interpretación: {error}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
