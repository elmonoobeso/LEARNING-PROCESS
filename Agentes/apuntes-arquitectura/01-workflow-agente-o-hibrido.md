# 1 · Workflow, agente o híbrido

**Decisión que se aprende a tomar:** cuánta autonomía darle al modelo. Es la primera decisión
de cualquier diseño y la que más condiciona coste, fiabilidad y facilidad de depuración.

## 1. La idea en claro

La pregunta de fondo es una sola: **¿quién decide el siguiente paso?**

- En un **workflow**, lo decide el programador. Los pasos y su orden están escritos en el
  código. El modelo puede intervenir dentro de un paso (clasificar, resumir, redactar), pero
  no elige el camino.
- En un **agente**, lo decide el modelo. Recibe un objetivo y unas herramientas, y en cada
  vuelta elige qué hacer a continuación y cuándo ha terminado.

Un símil de farmacia: un workflow es un **protocolo normalizado de trabajo**, con los mismos
pasos en el mismo orden y auditable. Un agente es **el farmacéutico ante una consulta
abierta**: va preguntando y decidiendo según lo que le responden. Nadie usa criterio abierto
para algo que tiene protocolo, ni un protocolo rígido para una consulta que no se puede
prever.

## 2. Opciones

| Opción | Qué te da | Qué te quita | Coste y complejidad |
|---|---|---|---|
| **Script sin LLM** | Resultado exacto y repetible, gratis, fácil de probar | No entiende texto libre ni casos imprevistos | Mínimo |
| **Una llamada al LLM** | Entiende y redacta lenguaje natural con muy poco código | No actúa ni consulta datos por sí solo | Muy bajo |
| **Workflow** | Pasos previsibles, coste conocido, se puede auditar paso a paso | No se adapta a situaciones que no previste | Bajo a medio |
| **Agente** | Resuelve tareas cuyo camino no se conoce de antemano | Predecibilidad, coste acotado y facilidad para explicar una decisión | Alto |
| **Híbrido** | Flexibilidad solo donde hace falta, control en el resto | Hay que decidir bien dónde está la frontera | Medio |

El híbrido es el patrón más habitual en sistemas reales: **workflow en el núcleo y modelo en
los bordes**. El núcleo (cálculos, reglas, pasos obligatorios) es código fijo; el modelo
aparece en los puntos de ambigüedad, como interpretar una petición, emparejar textos que no
coinciden exactamente o redactar la conclusión.

## 3. Cuándo usar cada una

Cuatro preguntas, en este orden:

1. **¿Puedo escribir los pasos antes de empezar?**
   Si sí, es un workflow (o un script). Si el camino depende de lo que se vaya encontrando,
   apunta a agente.
2. **¿Cuántos caminos posibles hay en cada punto?**
   Con 2 a 5 rutas, basta un enrutado fijo (un `if`, o un clasificador pequeño). Un agente
   empieza a compensar cuando hay muchas rutas y la correcta depende de contexto desordenado.
3. **¿Qué pasa si se equivoca, y alguien tendrá que explicar por qué?**
   En contextos regulados o con decisiones de dinero o salud, hace falta poder reconstruir
   cada paso. Eso favorece el workflow.
4. **¿Necesito el mismo resultado si lo ejecuto dos veces?**
   Un cálculo o un ranking debe ser reproducible, así que va en código. Una redacción puede
   variar.

Y dentro de cada paso, la misma lógica a pequeña escala:

| El paso consiste en... | Se resuelve con |
|---|---|
| Calcular, filtrar, ordenar, comparar con un umbral | Código |
| Entender texto libre, emparejar nombres parecidos, resumir, redactar | LLM |
| Decidir entre pocas opciones con criterios claros | Código (o LLM como clasificador, con salida restringida) |

**Señales de alarma**

- *Agente de más:* el coste se dispara, dos ejecuciones dan resultados distintos, nadie sabe
  explicar una decisión concreta. Un equipo que reconvirtió sus workflows en agentes reportó
  costes multiplicados por ocho y resultados inconsistentes (dato de un solo caso, citado en
  una guía; orientativo).
- *Workflow de menos:* el código se llena de casos especiales y cada entrada nueva lo rompe.

La recomendación de Anthropic resume todo el módulo: buscar la solución más simple posible y
añadir complejidad solo cuando se demuestre necesaria.

## 4. Ejemplos

**Genérico — dos tareas en una farmacia online**

- *Clasificar los correos entrantes* (pedido, devolución, consulta sanitaria) y enviarlos al
  departamento correcto. Los pasos se conocen y hay tres rutas: **workflow**, con una llamada
  al LLM como clasificador.
- *"Averigua por qué han caído las ventas de dermocosmética este trimestre."* No se sabe qué
  habrá que mirar hasta empezar; cada hallazgo abre la pregunta siguiente: **agente**.

**Agente de biosimilares — cómo se razona un nodo**

Tomemos el nodo *panorámico* (calidad y unicidad de los datos):

- ¿Puedo escribir los pasos antes? Sí: contar filas, contar duplicados, contar nulos por
  columna.
- ¿Debe dar lo mismo cada vez? Sí.
- ¿Hay texto libre que interpretar? No.

Conclusión: es código, sin LLM. El resto de nodos se clasifican con el mismo método en el
apartado *Decide tú*.

## 5. Cómo se ve

Workflow: el orden está en el código. Leyéndolo se sabe exactamente qué va a pasar.

```python
trials = fetch_trials()                 # paso 1, siempre
quality = check_quality(trials)         # paso 2, siempre
if quality.ok:                          # la ruta la decide una regla escrita
    gaps = find_gaps(trials, market)
    report = write_summary(gaps)        # aquí dentro puede haber una llamada al LLM
```

Agente: el orden no está en el código. Solo hay un objetivo, unas herramientas y un bucle.

```python
goal = "Encuentra huecos terapéuticos en biosimilares y justifícalos"
tools = [fetch_trials, fetch_market, fetch_patents, run_analysis]

run_agent(goal, tools, max_steps=20)    # el modelo decide qué llamar y en qué orden
```

En el primero, un error se localiza en una línea. En el segundo hay que leer la traza de lo
que el modelo decidió en cada vuelta.

## 6. Puntos críticos

- **Poner un agente donde hay un protocolo.** Es el error más frecuente: se paga más por un
  resultado menos fiable.
- **Dejar cálculos al modelo.** Sumar, contar u ordenar debe hacerlo código. El modelo puede
  equivocarse en aritmética y, peor, hacerlo con total seguridad en la respuesta.
- **Frontera mal puesta en un híbrido.** Si el paso que hace el LLM alimenta a todos los
  siguientes, su error se propaga sin que nadie lo vea. Ese paso necesita validación
  (módulo 8).
- **Elegir la arquitectura antes de comprobar los datos.** Si una fuente no existe o no es
  fiable, el mejor diseño no sirve. Los datos se verifican antes.

## 7. Qué valora el mercado

Saber justificar por qué **no** se ha usado un agente se valora más que saber montar uno. En
producción, las empresas buscan fiabilidad, coste controlado y decisiones explicables, y eso
suele significar workflow con el modelo en puntos concretos.

Frase útil en entrevista: *"Empecé por un pipeline determinista y solo puse un LLM en los
pasos con ambigüedad real, porque los cálculos tenían que ser reproducibles y auditables."*

## 8. Decide tú

**A. Mini-casos.** Para cada uno, elige una opción de la tabla del apartado 2 y justifícala
con las cuatro preguntas del apartado 3:

1. Cada lunes hay que generar un informe con las ventas de la semana por categoría y enviarlo
   por correo con dos frases de comentario.
2. Un asistente que responde dudas de pacientes sobre posología consultando las fichas
   técnicas oficiales.
3. Un sistema que revisa recetas y avisa si hay una interacción entre dos medicamentos de una
   lista cerrada de interacciones conocidas.

**B. Tu agente de biosimilares.** Clasifica cada nodo como *código* o *LLM* y justifica:

| Nodo | ¿Código o LLM? | Por qué |
|---|---|---|
| Distribución temporal | | |
| Distribución bivariante (cruce mercado vs. ensayos) | | |
| Nodo A — expiración de patente | | |
| Nodo B — hueco top 20 mercado vs. top ensayos | | |
| Nodo C — correlación con fracasos históricos | | |

Y dos preguntas más:

- Para cruzar "mercado" con "ensayos" hace falta que la misma enfermedad se reconozca en dos
  fuentes que la nombran distinto. ¿Dónde lo resolverías y con qué?
- Con todo lo anterior: ¿tu diseño es un workflow, un agente o un híbrido? ¿En qué puntos
  exactos intervendría el modelo?

## 9. Fuentes

Consultadas el 2026-10-09. Salvo la de Anthropic, son guías de empresas del sector, con
interés comercial: útiles como orientación, no como dato contrastado.

- [Building effective agents — Anthropic](https://www.anthropic.com/engineering/building-effective-agents)
- [How to Tell If You Need an AI Agent or a Workflow (7 Smells) — Kunal Ganglani](https://www.kunalganglani.com/blog/ai-agent-workflow-smells)
- [Workflow vs AI agent: when to use — Tensoria](https://tensoria.fr/en/blog/workflow-vs-ai-agent-when-to-use)
- [One agent is all you need (until it isn't) — Agno](https://www.agno.com/blog/one-agent-is-all-you-need-until-it-isnt)
- [The 2026 Guide to Agentic Workflow Architectures — StackAI](https://www.stackai.com/blog/the-2026-guide-to-agentic-workflow-architectures)
