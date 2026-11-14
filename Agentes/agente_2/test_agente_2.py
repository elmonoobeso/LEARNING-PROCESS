"""Tests de AgenteFDA sin red: ni API de la FDA ni Gemini.

Uso:  py -3.14 -m pytest Agentes/agente_2 -v
"""
import pandas as pd
import pytest
import requests

import agente_2
from agente_2 import AgenteFDA, obtencion_datos

VALIDO = {
    "classification": "Class II",
    "product_description": "Ibuprofen 600 mg tablets",
    "reason_for_recall": "Failed dissolution specifications",
    "recalling_firm": "Acme Pharma",
}


def agente_con(registros):
    agente = AgenteFDA()
    agente.datos = registros
    return agente


def test_registro_valido_va_a_validos():
    validos, no_validos, errores = agente_con([VALIDO]).validar_clases()
    assert (len(validos), len(no_validos), len(errores)) == (1, 0, 0)


def test_registro_con_dos_problemas_se_cuenta_una_sola_vez():
    malo = {**VALIDO, "classification": "Class X", "recalling_firm": None}
    validos, no_validos, _ = agente_con([malo]).validar_clases()
    assert len(validos) == 0
    assert len(no_validos) == 1
    motivo = no_validos[0]["motivo_no_valido"]
    assert "clasificación no válida" in motivo and "recalling_firm" in motivo


def test_campo_ausente_no_lanza_keyerror():
    sin_empresa = {k: v for k, v in VALIDO.items() if k != "recalling_firm"}
    _, no_validos, errores = agente_con([sin_empresa]).validar_clases()
    assert len(no_validos) == 1 and errores == []


def test_registro_que_no_es_diccionario_va_a_errores():
    _, _, errores = agente_con(["texto suelto"]).validar_clases()
    assert len(errores) == 1


def test_analisis_con_listas_vacias_no_falla(tmp_path):
    agente = AgenteFDA()
    analisis = agente.analisis_estadistico([], [], [])
    assert set(analisis) == {"info_validos", "resumen_validos", "por_clasificacion",
                             "por_empresa", "motivos_no_validos", "errores"}
    ruta = agente.exportar_resultados(analisis, carpeta=tmp_path)
    assert len(pd.ExcelFile(ruta).sheet_names) == 6


def test_analisis_con_columna_anidada_no_falla():
    con_openfda = {**VALIDO, "openfda": {"brand_name": ["ADVIL"]}}
    analisis = AgenteFDA().analisis_estadistico([con_openfda, VALIDO], [], [])
    assert analisis["por_clasificacion"]["Class II"] == 2


def test_fallo_de_conexion_lanza_runtimeerror(monkeypatch):
    def sin_red(*args, **kwargs):
        raise requests.exceptions.ConnectionError("sin red")
    monkeypatch.setattr(agente_2.requests, "get", sin_red)
    with pytest.raises(RuntimeError, match="No se pudo conectar"):
        obtencion_datos("https://ejemplo", {})


def test_respuesta_sin_results_devuelve_lista_vacia(monkeypatch):
    class RespuestaFalsa:
        def raise_for_status(self):
            pass

        def json(self):
            return {"meta": {}}
    monkeypatch.setattr(agente_2.requests, "get", lambda *a, **k: RespuestaFalsa())
    assert obtencion_datos("https://ejemplo", {}) == []


def test_interpretar_sin_clave_lanza_runtimeerror(monkeypatch):
    monkeypatch.delenv("Gemini_API_KEY", raising=False)
    with pytest.raises(RuntimeError, match="Gemini_API_KEY"):
        AgenteFDA().interpretar_analisis({"vacio": pd.DataFrame()})
