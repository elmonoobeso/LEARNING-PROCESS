# agente_2 — AgenteFDA

> **Autoría.** La versión 1 (septiembre de 2026) la escribí yo en modo Aprendizaje, salvo la
> llamada a Gemini. Las **correcciones de robustez de la versión 2** (noviembre de 2026) y los
> tests **los escribió la IA a petición mía**, a partir de una revisión del código; el detalle
> está en el PR que las introdujo. El historial de git conserva la versión 1 completa.
>
> *Authorship. Version 1 was hand-written by me (except the Gemini call). Version 2's
> robustness fixes and tests were written by AI at my request, after a code review.*

## Qué hace / What it does

**ES** — Agente que consulta la API pública de retiradas de medicamentos de la FDA
(`api.fda.gov/drug/enforcement.json`), valida los registros, los resume con pandas, exporta
el análisis a Excel y pide a Gemini una interpretación en lenguaje claro para un
profesional de farmacia.

**EN** — Agent that queries the FDA public drug recall API, validates the records,
summarizes them with pandas, exports the analysis to Excel and asks Gemini for a
plain-language interpretation for pharmacy professionals.

```
API FDA ──► validar_clases ──► analisis_estadistico ──► Excel (analisis_es/analisis.xlsx)
                 │                                             │
          válidos / no válidos                          interpretar_analisis ──► Gemini
          (cada registro en una sola lista)
```

Hojas del Excel / *Excel sheets*: `info_validos`, `resumen_validos`, `por_clasificacion`,
`por_empresa`, `motivos_no_validos`, `errores`.

## Cómo ejecutarlo / How to run

```
pip install pandas requests openpyxl python-dotenv google-genai
python Agentes/agente_2/agente_2.py
```

Necesita un `.env` junto al script (`Agentes/agente_2/.env`) con `Gemini_API_KEY=...`. Sin la clave,
el agente genera igualmente el Excel y avisa de que no puede interpretar.
*Needs a `.env` with `Gemini_API_KEY`; without it, the Excel is still generated.*

## Tests

```
pip install pytest
python -m pytest Agentes/agente_2 -v
```

9 tests sin red (ni FDA ni Gemini): registros válidos e inválidos, campos ausentes o vacíos,
listas vacías, columnas anidadas, fallo de conexión, respuesta sin resultados y falta de
clave.

## Qué se corrigió en la versión 2 / What changed in v2

| Fallo de la v1 | Corrección |
|---|---|
| Clave `"analisisdf3"` repetida: una tabla se perdía sin aviso | Claves únicas y descriptivas (son los nombres de las hojas) |
| Un registro podía contarse dos veces como no válido, o como válido y no válido a la vez | Cada registro va a una sola lista, con el motivo en `motivo_no_valido` |
| `KeyError` si openFDA omitía un campo | `registro.get(...)`: openFDA omite los campos vacíos en vez de enviar `None` |
| `describe()`/`groupby` fallaban con tablas vacías o columnas anidadas | Comprobación de tabla vacía y `describe()` solo sobre columnas simples |
| Si fallaba la petición, devolvía `None` en silencio y el error saltaba después | Lanza `RuntimeError` con el motivo; `main()` lo captura y sale con código 1 |
| Importar el archivo exigía la clave de Gemini | La clave se lee solo al interpretar |
| Librería `google.generativeai`, sin soporte de Google | Migrado a `google-genai`, con el mensaje de sistema como `system_instruction` |
| El alias `gemini-flash-latest` ya no existe (error 404) | Versión de modelo fijada en una constante |
| Un fallo de Gemini (clave, cuota, modelo) acababa en traceback | Se captura y se informa; el Excel ya está generado |
| Sin tiempo límite: un modelo saturado dejaba el agente colgado | Límite de 90 s en la llamada (`TIMEOUT_GEMINI_MS`) |

## Limitaciones / Limitations

- Descarga solo 100 registros (`limit`), sin paginación.
- El modelo está fijado (`gemini-3.5-flash`, en `MODELO_GEMINI`). La v1 usaba el alias
  `gemini-flash-latest`, que Google retiró y rompía el agente; cuando se retire esta versión,
  basta con cambiar esa constante. Se eligió tras probar los modelos disponibles: los más
  nuevos (3.7 y 3.8) no respondían en noviembre de 2026.
- La interpretación de Gemini es un apoyo, no un análisis regulatorio.

**Dificultad / Difficulty:** Avanzado · **Estado / Status:** ✅ Funcional, con tests
