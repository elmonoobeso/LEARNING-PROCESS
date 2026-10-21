# agente_2 — AgenteFDA

> **Modo de autoría: Aprendizaje.** Este script sigue la misma regla del resto del
> repositorio — código escrito a mano por el usuario, con IA solo para proponer, revisar o
> documentar — **con dos excepciones explícitas**, ambas a petición directa del usuario y
> marcadas como tal en vez de presentarse como escritas a mano:
> 1. El método `interpretar_analisis` (la llamada a `google.generativeai`/Gemini con
>    `generate_content`, la construcción del prompt y el manejo de `self.memoria`) fue
>    **generado por IA**.
> 2. En `analisis_estadistico`, el guard `if df1.empty: ... else: ...` alrededor de
>    `analisis_clasificacion`/`analisis_farmaceutica` fue **añadido por IA** para arreglar un
>    `KeyError: 'classification'` que ocurría cuando `no_validos` venía vacío (caso real: la
>    API devolvió datos donde ningún registro fue clasificado como no válido).
>
> El resto del archivo (obtención de datos vía `requests`, validación, el resto de
> `analisis_estadistico`, `exportar_resultados`, el punto de entrada) sí es trabajo propio del
> usuario, revisado por IA de la forma habitual.

## Qué hace
Clase `AgenteFDA` que consulta la API pública de alertas/retiradas de medicamentos de la FDA
(`api.fda.gov/drug/enforcement.json`), valida y separa los registros válidos/no válidos,
calcula un análisis estadístico (por clasificación, por farmacéutica, resumen de tipos/nulos,
descripción de errores) y lo exporta a un Excel con una hoja por resultado. El método
`interpretar_analisis` (la parte marcada arriba) le pasa ese análisis a Gemini para obtener una
interpretación en lenguaje natural, en formato pregunta-respuesta única (no conversación con
varios turnos).

**Dificultad:** Avanzado
**Estado:** ✅ Ejecuta de principio a fin (pipeline completo con punto de entrada). Sensible a
qué registros devuelva la API en cada ejecución (si `no_validos` viene vacío, ese caso ya está
cubierto).
