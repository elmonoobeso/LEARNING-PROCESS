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
