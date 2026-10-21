# Decisiones de arquitectura — Agentes

Apuntes acumulativos de criterio sobre organización y orquestación de agentes: qué se probó,
qué ventajas/desventajas se comprobaron en la práctica, qué patrones funcionaron o no. No es
solo un registro de decisiones puntuales — es material de consulta reutilizable entre
agentes. Cada entrada se añade cuando se toma o revisa una decisión de arquitectura en
cualquier agente.

Formato de cada entrada:

```
## [fecha] agente_N — título corto de la decisión

**Contexto**: qué problema había que resolver.
**Opciones consideradas**: lista breve con ventajas/desventajas de cada una.
**Elección**: cuál se eligió y por qué.
**Aprendizaje**: qué se confirmó o descartó al usarlo en la práctica (se rellena después,
cuando ya se ha probado).
```

---

## [2026-09-01, retrospectiva] agente_1.1 — Agente como clase, datos con NumPy, LLM sin conectar

> *Retrospectiva*: decisión tomada de forma implícita al escribir el agente; se documenta
> después para no perder lo aprendido.

**Contexto**: primer agente: analizar un CSV de ventas de farmacia (stock negativo, posible
abuso de estupefacientes, anomalías de precio) y preparar el terreno para que un LLM
interprete los resultados.

**Opciones consideradas** (implícitas):
- **NumPy con arrays estructurados** (`genfromtxt(..., names=True)`) — lo que se dominaba en
  ese momento.
- **pandas** — tabla con `groupby`, pensada justo para este tipo de datos.

**Elección**: una clase `Agente` con el estado dentro (`self.ventas`, `self.memoria` con
mensajes `role`/`content`) y las reglas de negocio como código (umbrales distintos para
medicamento y parafarmacia según el código nacional). El LLM (Gemini) se configura, pero
ningún método lo llama todavía.

**Aprendizaje**: con NumPy, cada agregación por producto o por paciente exige un bucle
manual sobre `np.unique`; en `agente_2` se pasó a pandas. Las reglas de negocio en código son
auditables y deterministas, y ese criterio se mantiene en los agentes siguientes ("workflow
en el núcleo, modelo en los bordes", ver [chuleta](apuntes-arquitectura/chuleta-decisiones.md)).

## [2026-09-03, retrospectiva] agente_2 — Pipeline lineal en clase y LLM en una sola llamada

> *Retrospectiva*: igual que la anterior.

**Contexto**: consultar la API de retiradas de medicamentos de la FDA, validar los
registros, resumirlos y pedir a un LLM una interpretación en lenguaje natural.

**Opciones consideradas** (implícitas):
- **Conversación con memoria** (enviar todo `self.memoria` en cada turno).
- **Una sola llamada** con el mensaje de sistema y el último mensaje concatenados.

**Elección**: pipeline lineal (obtener → validar → analizar → exportar a Excel →
interpretar) dentro de la clase `AgenteFDA`, con pandas para el análisis y **una sola
llamada** a Gemini.

**Aprendizaje**: `self.memoria` acumula mensajes, pero solo se usan el primero y el último,
así que la "memoria" no aporta nada. Además, el estado escondido en `self` hace difícil ver
qué datos pasan de un paso a otro. Esto motivó la decisión del agente 3 de usar **estado
externo explícito** (un diccionario que viaja entre funciones).

## [2026-09-20] agente_3 — Framework de orquestación: LangGraph

**Contexto**: Ermenegildo cruza tres fuentes (ensayos clínicos, mercado, prevalencia) y
decide en cascada: Nodo A (¿la patente expira en <3 años?) → Nodo B (¿hay hueco entre el
top de mercado y el top de ensayos?) → Nodo C (¿correlaciona con fracasos históricos?). Cada
nodo depende del estado que deja el anterior.

**Opciones consideradas**:
- **LangGraph** — grafo con estado explícito que viaja entre nodos y aristas condicionales.
  Encaja con una cascada de reglas A→B→C. Desventaja: librería nueva que aprender.
- **CrewAI** — equipos de agentes con roles que razonan con un LLM. Desventaja: aquí los
  nodos son reglas fijas, no decisiones de un LLM; añadiría coste e imprevisibilidad sin
  aportar nada.
- **Python plano** — funciones encadenadas a mano. Ventaja: cero dependencias. Desventaja:
  la gestión del estado, las ramas y la trazabilidad hay que construirlas a mano.

**Elección**: LangGraph, porque el problema es una cascada de estado con ramas
condicionales, que es justo para lo que está diseñado.

**Aprendizaje**: *(pendiente — se rellena al implementar la orquestación)*

## [2026-09-20] agente_3 — Orden de trabajo: Python plano primero, LangGraph después

**Contexto**: había que decidir si escribir la lógica directamente como nodos de LangGraph o
por separado.

**Opciones consideradas**:
- **Directamente en LangGraph** — menos pasos, pero mezcla dos curvas de aprendizaje (la
  librería y la lógica de negocio real) y un fallo no deja claro de cuál de las dos viene.
- **Python plano disciplinado primero** — funciones de fetch y de nodos con estado externo
  explícito (un diccionario que viaja entre funciones, no `self.algo` como en `agente_2`), y
  después se envuelven con `add_node`/`add_edge`.

**Elección**: Python plano primero. Con el estado ya externo, migrar a LangGraph es solo
"conectar cables", no reescribir.

**Aprendizaje**: *(pendiente — se valida al hacer la migración)*

## [2026-10-14] agente_3 — Consulta precisa para quitar falsos biosimilares

> Implementado en la rama `feature/agente-3-nodo-panoramico` (sin fusionar todavía).

**Contexto**: la consulta `query.intr=biosimilar` de ClinicalTrials.gov devolvía estudios
que solo mencionan "biosimilar" de pasada, no ensayos de biosimilares. Esos falsos positivos
inflan el análisis panorámico.

**Opciones consideradas**:
- **Consulta amplia y filtrar después en pandas** (p. ej. `str.contains` sobre el título) —
  fácil de ajustar, pero se descargan muchos estudios inútiles y el filtro queda lejos del
  origen del problema.
- **Búsqueda por campos con la sintaxis `AREA[...]`** de la API, limitada a nombre de la
  intervención, título oficial y título corto.

**Elección**: `query.term` con `AREA[InterventionName]`, `AREA[OfficialTitle]` y
`AREA[BriefTitle]`: el filtro se aplica en la fuente.

**Aprendizaje**: *(pendiente — medir cuántos estudios se descartan comparando `totalCount`
antes y después, y revisar a mano una muestra de los descartados)*

## [2026-10-20] agente_3 — SQLite para los datos de mercado

> Implementado en la rama `feature/agente-3-datos-mercado` (sin fusionar todavía).

**Contexto**: los datos de mercado (CMS) llegan como CSV y hay que cruzarlos con otras
tablas (ensayos, prevalencia) de forma fiable y repetible.

**Opciones consideradas**:
- **CSV + pandas en memoria** — lo más simple, pero nada impide relaciones rotas entre tablas
  y cada script vuelve a leer y limpiar los CSV.
- **SQLite** — base de datos en un archivo, incluida en Python (`sqlite3`), sin servidor;
  permite claves foráneas y consultas SQL.
- **DuckDB** — muy rápida para análisis, pero es una dependencia más y aporta poco con este
  volumen de datos.

**Elección**: SQLite (`market.db`) con `PRAGMA foreign_keys = ON`. La base se regenera desde
cero en cada ejecución, así siempre refleja el CSV actual. Los CSV y la base no se versionan.

**Aprendizaje**: en SQLite las claves foráneas vienen **desactivadas por defecto** y hay que
activarlas en cada conexión; si no, se aceptan relaciones rotas sin ningún error. Además,
encaja con aprender SQL para análisis de negocio.
