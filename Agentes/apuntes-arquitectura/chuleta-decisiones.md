# Chuleta de decisiones

Resumen de una página para repasar. Cada regla enlaza al módulo donde se explica. Crece con
cada módulo.

## Piezas de un agente ([módulo 0](00-mapa-general.md))

- Agente = **modelo + instrucciones + herramientas + bucle + estado**, con control y
  evaluación alrededor.
- El modelo no ejecuta nada: **pide**, y el programa ejecuta. Por eso se puede validar y
  limitar.
- Si algo falla, primero localizar la pieza: herramienta mal descrita, contexto saturado,
  bucle sin límite, demasiada decisión en el modelo, o falta de trazas.

## ¿Workflow, agente o híbrido? ([módulo 1](01-workflow-agente-o-hibrido.md))

La pregunta: **¿quién decide el siguiente paso, el código o el modelo?**

1. ¿Puedo escribir los pasos antes de empezar? → Sí: workflow.
2. ¿Hay solo 2-5 rutas por punto? → Enrutado fijo, no agente.
3. ¿Habrá que explicar o auditar cada decisión? → Workflow.
4. ¿Debe dar lo mismo dos veces? → Código.

- Calcular, filtrar, ordenar, comparar con umbral → **código**.
- Entender texto libre, emparejar nombres parecidos, resumir, redactar → **LLM**.
- Por defecto: **workflow en el núcleo, modelo en los bordes**.
- Empezar por lo más simple y añadir complejidad solo si se demuestra necesaria.
- Verificar que los datos existen antes de elegir arquitectura.
