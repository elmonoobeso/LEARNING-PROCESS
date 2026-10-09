# Agente 3 — Ermenegildo (biosimilares)

> **Nota de autoría (excepción documentada):** a diferencia del resto del repositorio, donde
> el código lo escribe el usuario a mano, **en este agente el código lo escribe la IA
> (Claude)**, por decisión explícita del usuario el 2026-10-09. El objetivo aquí no es
> practicar sintaxis sino aprender **criterio de arquitectura de agentes**: el usuario decide
> y justifica cada decisión de diseño, y la IA la construye. El repaso de Python se hace
> aparte, en ejercicios propios donde la regla de autoría normal sigue vigente.
>
> Reparto concreto en `agent_3.py`:
> - **Escrito por el usuario:** la primera versión del archivo (petición a la API, manejo de
>   errores de `requests`, esqueleto de las tres funciones de obtención de datos).
> - **Escrito por la IA:** dentro de `obtencion_datos_ensayos`, la paginación, el renombrado
>   de columnas (`columnas_ensayos`) y la limpieza de `collaborators`, `conditions`, `phase`
>   (`orden_fases`) y `start_date`.
>
> El diseño de negocio (nodos y umbrales en
> [diseno-agente-biosimilares.md](diseno-agente-biosimilares.md)) es del usuario.

## Qué hace / What it does

**ES** — Agente centrado en biosimilares: busca huecos terapéuticos donde el mercado o la
prevalencia de una enfermedad no se corresponde con el volumen de ensayos clínicos activos, y
valora la oportunidad según la expiración de patentes y el historial de fracasos. Diseño
completo en [diseno-agente-biosimilares.md](diseno-agente-biosimilares.md).

**EN** — Biosimilar-focused agent: looks for therapeutic gaps where a disease's market size
or prevalence is not matched by the volume of active clinical trials, and weighs the
opportunity against patent expiry and the history of failed trials. Full design in
[diseno-agente-biosimilares.md](diseno-agente-biosimilares.md).

## Estado / Status

🚧 **En progreso / In progress**

| Parte / Part | Estado / Status |
|---|---|
| Ensayos clínicos — `obtencion_datos_ensayos` (ClinicalTrials.gov API v2) | ✅ Funciona: descarga todas las páginas y devuelve una tabla limpia de 9 columnas / Works: fetches every page and returns a clean 9-column table |
| Mercado — `obtencion_datos_mercado` | ❌ Sin fuente definida, no ejecutable / No data source yet, not runnable |
| Prevalencia — `obtencion_datos_prevalencia` | ❌ Sin fuente definida, no ejecutable / No data source yet, not runnable |
| Nodos de análisis y de decisión / Analysis and decision nodes | ❌ Sin empezar / Not started |
| Orquestación (framework) / Orchestration (framework) | ❌ Sin decidir / Not decided |

## Decisiones de arquitectura / Architecture decisions

Todavía ninguna tomada. Se registrarán aquí y en
[../decisiones-arquitectura.md](../decisiones-arquitectura.md) cuando el agente llegue a cada
una.

None taken yet. They will be recorded here and in
[../decisiones-arquitectura.md](../decisiones-arquitectura.md) as the agent reaches each one.

## Cómo ejecutarlo / How to run

```
python Agentes/Agente3_Ermenegildo/agent_3.py
```

Requiere / Requires: `pandas`, `requests`, `python-dotenv`. Las claves de API van en `.env`
(no versionado) / API keys go in `.env` (not versioned).
