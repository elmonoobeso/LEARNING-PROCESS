# Apuntes de arquitectura de agentes

Guía de estudio y repaso sobre cómo se diseña un agente: qué piezas tiene, qué opciones hay
en cada decisión, qué da y qué quita cada una, y cuándo conviene usar cuál. El objetivo es
**criterio de diseño**, no sintaxis de un framework.

## Cómo se usan

- **Crecen al ritmo del agente 3 (Ermenegildo).** No están escritos de antemano: cada módulo
  se escribe o se amplía cuando el agente llega a esa decisión, o cuando surge una pregunta.
  Por eso hay módulos parciales y módulos sin empezar.
- **El temario es el mapa, no el orden.** Se escribe primero lo que el agente necesita.
- **Primero decides tú.** Cada módulo acaba con una sección *Decide tú*. Se responde antes de
  contrastar; los fallos se añaden después al módulo como errores a vigilar.
- **El código es para leer.** Los fragmentos están para entender la forma de cada pieza, no
  para memorizarlos ni escribirlos a mano.
- **Lo duradero y lo que caduca van separados.** Los principios cambian poco; los nombres de
  frameworks y sus funciones cambian cada pocos meses. Lo segundo lleva siempre fecha y fuente.

Para repasar rápido: [chuleta-decisiones.md](chuleta-decisiones.md).
Decisiones reales tomadas en los agentes del repo: [../decisiones-arquitectura.md](../decisiones-arquitectura.md).

## Temario y progreso

| # | Módulo | Decisión que se aprende a tomar | Estado |
|---|---|---|---|
| 0 | [Mapa general](00-mapa-general.md) | Qué piezas tiene un agente | Primera versión |
| 1 | [Workflow, agente o híbrido](01-workflow-agente-o-hibrido.md) | Cuánta autonomía dar y cuándo no usar un agente | Primera versión |
| 2 | Patrones básicos | Cadena, enrutado, paralelo, orquestador-trabajadores, evaluador-optimizador | Sin empezar |
| 3 | Herramientas | Qué herramientas dar, cómo definirlas, MCP | Sin empezar |
| 4 | Nodos y flujo | Dónde poner un nodo, de qué tamaño, código o LLM, ramas | Sin empezar |
| 5 | Estado, contexto y memoria | Qué ve el modelo en cada paso, memoria corta y larga, RAG | Sin empezar |
| 6 | Multi-agente | Uno o varios agentes, jerarquía, traspasos | Sin empezar |
| 7 | Frameworks | Sin framework, SDK nativo, LangGraph, CrewAI, otros | Sin empezar |
| 8 | Fiabilidad y gobernanza | Guardrails, control humano, errores, coste, seguridad | Sin empezar |
| 9 | Evaluación y observabilidad | Cómo saber que funciona: evals y trazas | Sin empezar |
| 10 | Caso integrador | Diseñar el agente de biosimilares de principio a fin | Sin empezar |

Los módulos 3, 5, 8 y 9 son los que más peso tienen en las ofertas de trabajo actuales y
llevarán más profundidad.

## Plantilla de cada módulo

1. **La idea en claro** — qué es y qué problema resuelve.
2. **Opciones** — qué da, qué quita y cuánto cuesta cada una.
3. **Cuándo usar cada una** — reglas de decisión y señales de alarma.
4. **Ejemplos** — uno genérico y el agente de biosimilares.
5. **Cómo se ve** — diagrama o fragmento mínimo para leer.
6. **Puntos críticos** — fallos típicos y cómo se detectan.
7. **Qué valora el mercado** — qué se pide y cómo explicarlo en una entrevista.
8. **Decide tú** — mini-casos.
9. **Fuentes y fecha.**

Un módulo en "primera versión" puede no tener todavía todas las secciones completas.
