# 0 · Mapa general: las piezas de un agente

**Decisión que se aprende a tomar:** reconocer qué piezas tiene cualquier sistema con un LLM,
para saber en cuál hay que pensar cuando algo falla o cuando hay que diseñar algo nuevo.

## 1. La idea en claro

Un modelo de lenguaje (LLM) por sí solo solo hace una cosa: recibe texto y devuelve texto. No
recuerda la conversación anterior, no consulta una API y no ejecuta nada.

Un **agente** es un programa normal que envuelve a ese modelo y le da tres capacidades que no
tiene:

- **actuar**, mediante herramientas;
- **continuar**, mediante un bucle que le devuelve el resultado de cada acción;
- **recordar**, mediante un estado que el programa guarda y le vuelve a enseñar.

Todo lo que rodea al modelo (bucle, herramientas, estado, límites) se suele llamar *harness*
o arnés. La arquitectura de agentes consiste casi por completo en diseñar ese arnés. El modelo
se elige; el arnés se diseña.

## 2. Las piezas

| Pieza | Qué es | Qué se decide al diseñarla | Módulo |
|---|---|---|---|
| **Modelo** | El LLM que razona y redacta | Cuál usar en cada paso: grande y caro, o pequeño y rápido | 7, 8 |
| **Instrucciones** | El texto fijo que define rol, objetivo y límites (*system prompt*) | Qué debe hacer, qué no, y en qué formato responde | 5 |
| **Herramientas** | Funciones que el modelo puede pedir que se ejecuten (consultar una API, leer un archivo) | Cuáles darle, cómo describirlas, qué devuelven | 3 |
| **Bucle** | El código que repite: modelo → herramienta → resultado → modelo | Quién decide el siguiente paso: el código o el modelo | 1, 2, 4 |
| **Estado y contexto** | Lo que el programa guarda y lo que el modelo ve en cada paso | Qué se guarda, qué se le enseña, qué se resume o descarta | 5 |
| **Control** | Validaciones, límites de pasos y coste, aprobación humana | Dónde puede equivocarse sin daño y dónde no | 8 |
| **Evaluación** | Pruebas y trazas para saber si funciona | Qué es "funcionar" y cómo se mide | 9 |

Una idea que conviene fijar desde el principio: el modelo **no ejecuta** las herramientas.
Solo escribe "quiero llamar a esta función con estos datos". Quien la ejecuta es tu programa,
y por eso tu programa puede validar, limitar o rechazar cualquier acción.

## 3. El espectro: de menos a más autonomía

No todo lo que usa un LLM es un agente. De más simple a más complejo:

```
script sin LLM  →  una llamada al LLM  →  workflow  →  agente  →  varios agentes
   (más barato, predecible, fácil de depurar)        (más flexible, caro, impredecible)
```

La regla general es quedarse en el punto más a la izquierda que resuelva el problema. Decidir
en qué punto situarse es la primera decisión de arquitectura y se trata en el
[módulo 1](01-workflow-agente-o-hibrido.md).

## 4. Ejemplos

**Genérico — "¿qué tiempo hará mañana en Sevilla?"**

1. El modelo recibe la pregunta y la lista de herramientas disponibles.
2. No sabe el tiempo, así que responde: "llama a `get_weather` con ciudad = Sevilla".
3. El programa ejecuta esa función y le devuelve el resultado.
4. El modelo redacta la respuesta final con ese dato.

Ahí están todas las piezas: modelo, una herramienta, un bucle de dos vueltas y un estado (la
pregunta y el resultado intermedio).

**Agente de biosimilares**

| Pieza | En este agente |
|---|---|
| Herramientas | Consulta de ensayos clínicos, de mercado/prevalencia y de patentes |
| Bucle | La secuencia de nodos de análisis y la cascada A → B → C |
| Estado | Las tablas descargadas y los resultados de cada nodo |
| Control | Los umbrales (patente a menos de 3 años, top 20) y la comprobación de calidad del nodo panorámico |
| Modelo | Pendiente de decidir en qué pasos interviene (módulo 1) |

## 5. Cómo se ve

El bucle de un agente, reducido a lo esencial. Es para leer la forma, no para memorizarlo:

```python
messages = [{"role": "user", "content": question}]

while True:
    response = call_model(instructions, messages, tools)   # el modelo decide
    messages.append(response)                              # el programa recuerda

    if not response.tool_calls:                            # no pide nada más: ha terminado
        break

    for call in response.tool_calls:
        result = run_tool(call.name, call.arguments)       # el programa ejecuta, no el modelo
        messages.append({"role": "tool", "content": result})
```

Tres detalles que explican muchas decisiones posteriores:

- `messages` crece en cada vuelta. Ese es el contexto, y gestionarlo es el módulo 5.
- `while True` no tiene límite. En un agente real siempre hay un máximo de vueltas (módulo 8).
- El `if` lo resuelve el modelo: él decide cuándo ha terminado. En un workflow, ese `while`
  se sustituye por una secuencia fija que decide el programador.

## 6. Puntos críticos

Cuando un agente falla, casi siempre es una de estas piezas, y rara vez es "el modelo es
tonto":

| Síntoma | Pieza donde mirar |
|---|---|
| Llama a la herramienta equivocada o con datos mal formados | Herramientas: descripción ambigua o demasiadas |
| Se olvida de algo dicho antes, o se contradice | Contexto: se ha llenado, o se resumió mal |
| Da vueltas sin acabar, o gasta mucho | Bucle sin límite, o tarea mal acotada |
| Resultado distinto cada vez | Demasiada decisión en manos del modelo (módulo 1) |
| Nadie sabe por qué hizo lo que hizo | Falta de trazas (módulo 9) |

## 7. Qué valora el mercado

Saber nombrar estas piezas y localizar un fallo en la correcta es lo que distingue a quien
"ha usado un framework" de quien entiende lo que hay debajo. Una oferta real de 2026 lo
resume pidiendo responsabilizarse de "gestión de contexto, diseño de herramientas,
evaluación, trazas y coste": son, una por una, las filas de la tabla del apartado 2.

Frase útil en entrevista: *"Un agente es un modelo dentro de un bucle con herramientas y
estado. Casi todo el trabajo de diseño está en lo que rodea al modelo, no en el modelo."*

## 8. Decide tú

1. Un asistente recomienda un medicamento que el paciente había dicho, diez mensajes antes,
   que le daba alergia. ¿En qué pieza está el problema y por qué?
2. Un agente consulta la misma API quince veces seguidas con la misma petición. Nombra dos
   piezas que podrían estar mal diseñadas.
3. Explica con tus palabras por qué es importante que sea el programa, y no el modelo, quien
   ejecuta las herramientas. Pon un ejemplo de farmacia.

## 9. Fuentes

Consultadas el 2026-10-09.

- [Building effective agents — Anthropic](https://www.anthropic.com/engineering/building-effective-agents)
- [Context engineering for AI agents: a practical guide — Mastra](https://mastra.ai/articles/context-engineering)
- [AI Product Engineer at ClickHouse (oferta) — hotfix.jobs](https://hotfix.jobs/jobs/ai-product-engineer-at-clickhouse-d71af7e2-0dad-46b5-840a-387ddd0ba9aa)
