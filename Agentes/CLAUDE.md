# Agentes/ — instrucciones específicas (hereda el CLAUDE.md raíz)

Todo lo del `CLAUDE.md` de la raíz aplica aquí también (git, commits, ramas, squash merge,
idioma, Ruff, secretos). Este archivo añade lo específico de trabajar en `Agentes/`.

## Qué se practica aquí

Cada `Agentes/agente_N/` es un miniproyecto que resuelve un problema real (no solo
sintaxis). El objetivo declarado del usuario tiene dos partes distintas:

1. Practicar Python de análisis de datos (pandas, numpy, APIs) — igual que en el resto del
   repo.
2. Aprender la "otra mitad": cómo se organiza y orquesta un agente. Esta segunda parte es
   nueva para el usuario y es donde este archivo matiza la regla de autoría del CLAUDE.md
   raíz.

## Regla de autoría aquí — dos capas, no una

- **Lógica de análisis/dominio** (pandas, numpy, llamadas a APIs de datos, reglas de negocio
  de farmacia) → el usuario la escribe a mano. Misma regla que el resto del repo.
- **Arquitectura/orquestación del agente** (framework, nodos, flujo, gobernanza) → aquí
  Claude SÍ puede escribir código y proponer patrones, porque el objetivo explícito es
  aprender por exposición y construir criterio, no memorizar sintaxis nueva desde cero.

## Prioridad de aprendizaje

Lo importante no es dominar la sintaxis de un framework concreto. Es aprender a
**organizar, decidir y justificar**: cuándo usar un framework u otro, ventajas y
desventajas, cómo estructurar el flujo, cómo introducir gobernanza. La sintaxis es el medio,
no el fin — no dar código sin explicar el porqué de las decisiones detrás.

## Workflow para arrancar la parte de orquestación de un agente nuevo

1. El usuario cuenta en una frase qué debe hacer el agente (el problema real).
2. Claude presenta 2-3 enfoques/frameworks razonables **para ese caso concreto**, con
   ventajas y desventajas — nunca uno solo por defecto sin alternativas.
3. El usuario decide cuál probar (puede pedir opinión, pero la elección y el porqué quedan
   suyos).
4. Claude construye el scaffold de orquestación explicando cada pieza mientras la escribe,
   no todo de golpe sin contexto.
5. El usuario escribe la lógica de análisis/negocio dentro de esa estructura (regla de
   autoría normal, sin cambios).
6. Se registra la decisión: en el README del agente y en `decisiones-arquitectura.md`.

## Organización en carpetas y submódulos

Cuando la complejidad de un agente lo justifique (no desde el primer commit de algo simple
como un script único), dividirlo en módulos con responsabilidad clara — por ejemplo:
herramientas/tools, prompts, nodos/flujo, configuración, tests. La estructura de carpetas
debe reflejar un patrón **orquestador-trabajador**: un módulo que coordina y varios módulos
especializados con límites de tarea bien definidos. Ver más abajo por qué.

## Elección de framework

Antes de escribir código de orquestación, presentar opciones razonables para el caso
concreto (ej. LangGraph para flujos con estado tipo grafo, CrewAI para equipos de agentes
con roles, SDK nativo de Anthropic para uso de herramientas simple) con ventajas/desventajas
— nunca elegir en silencio.

## Patrones de orquestación (verificado, no solo teoría)

La evidencia de producción en 2026 favorece los patrones **jerárquicos** (un orquestador
que delega en subagentes/módulos especializados, cada uno con objetivo, formato de salida,
herramientas y límites de tarea claros, con estado aislado y devolviendo resúmenes
condensados) sobre la colaboración libre tipo "enjambre" sin jerarquía clara, que tiende a
desviarse del objetivo. La fiabilidad no viene de "tener carpetas" en sí — viene de la
disciplina de límites de tarea claros y contratos de interfaz entre orquestador y
trabajador; las carpetas son la forma de reflejar esa disciplina en el código, no la causa
de la fiabilidad.

Fuentes (sept. 2026): [Agentic AI Architecture Patterns — Augment Code](https://www.augmentcode.com/guides/agentic-ai-architecture-patterns),
[Orchestrator and subagent multi-agent patterns — Microsoft Learn](https://learn.microsoft.com/en-us/agents/architecture/multi-agent-orchestrator-sub-agent),
[Architectural Design Decisions in AI Agent Harnesses (arXiv)](https://arxiv.org/pdf/2604.18071).

## Gobernanza (introducir progresivamente, explicando qué es y por qué)

- Guardrails: validación de entradas/salidas del agente.
- Puntos de control humano en pasos críticos o irreversibles.
- Control de acceso a herramientas (qué puede y no puede tocar cada módulo/subagente).
- Trazabilidad/logging de las decisiones que toma el agente.

## Vigencia (state of the art)

Este campo cambia rápido. Antes de dar por bueno un framework o patrón como "de última
generación", verificar con búsqueda web en vez de fiarse solo del conocimiento entrenado, y
avisar si algo puede estar desactualizado.

## Estructura de cada agente

`Agentes/agente_N/` con su(s) script(s), README propio (qué problema resuelve + decisiones
de arquitectura tomadas: qué framework, por qué, qué alternativas se consideraron), y `.env`
si usa claves de API.

## `decisiones-arquitectura.md`

No es solo un registro de decisiones puntuales por agente — es una fuente de consulta
acumulativa del criterio que el usuario va adquiriendo entre agentes (qué ventajas/
desventajas se han comprobado en la práctica, qué patrones funcionan o no), a modo de
apuntes reutilizables. Se actualiza cada vez que se toma o revisa una decisión de
arquitectura en cualquier agente.
