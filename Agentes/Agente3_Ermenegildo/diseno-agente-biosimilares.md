# Diseño del agente complejo — Biosimilares

Reconstrucción del diseño de arquitectura (nodos) discutido a finales de agosto / principios de septiembre de 2026, dentro del proyecto del agente de ensayos clínicos (clinicaltrials.gov).

## Objetivo

Agente enfocado exclusivamente en **biosimilares**: detectar huecos terapéuticos donde el mercado/prevalencia de una enfermedad no está correspondido por el volumen de ensayos clínicos activos, y evaluar la oportunidad de negocio a la luz de la expiración de patentes y el historial de fracasos.

## Nodos de análisis (exploración de datos)

1. **Panorámico** — evalúa la calidad y unicidad de los datos disponibles antes de avanzar (cobertura, duplicados, campos faltantes).
2. **Distribución temporal** — analiza la tendencia de apertura de ensayos clínicos a lo largo del tiempo.
3. **Distribución bivariante** — cruza el top de enfermedades por mercado/prevalencia contra el top de enfermedades por número de ensayos clínicos, con detección de anomalías en ese cruce.

## Nodos de decisión (cascada)

**Nodo A — Expiración de patente**
¿El biosimilar/medicamento de referencia tiene la patente expirando en los próximos 3 años?
→ Si no, descarta o de-prioriza.

**Nodo B — Descorrespondencia mercado vs. ensayos**
¿Existe un hueco entre el ranking de mercado/prevalencia y el ranking de ensayos clínicos?

- **Umbral definido:** si una enfermedad está en el **top 20 de mercado** pero **no aparece en el top de ensayos clínicos** (o viceversa), se marca como **candidata a hueco terapéutico**.

**Nodo C — Correlación con fracasos históricos**
¿Ese hueco correlaciona con ensayos que históricamente han fracasado en esa enfermedad?

- Si **hay correlación**: el agente identifica qué empresa ha gastado más recursos (mayor número de ensayos intentados) en esa área, y calcula la **tasa de oportunidad de llegar a tiempo**, usando el **promedio histórico de duración de fase 3 hasta finalización** como referencia temporal.

## Lógica de flujo resumida

```
Datos de ensayos clínicos + datos de mercado/prevalencia
        │
        ▼
[Panorámico] → [Distribución temporal] → [Distribución bivariante]
        │
        ▼
   Nodo A: ¿patente expira en <3 años?
        │ sí
        ▼
   Nodo B: ¿hueco top20 mercado vs top ensayos?
        │ sí
        ▼
   Nodo C: ¿correlaciona con fracasos históricos?
        │ sí
        ▼
   → Empresa con más inversión en ensayos fallidos
   → Tasa de oportunidad (basada en duración media fase 3)
```

## Contexto del proyecto

- Este diseño es la evolución "compleja" del agente de ensayos clínicos que forma parte del portfolio de agentes de Miguel (junto a AgenteFarmacia y AgenteFDA).
- Se enmarca en la línea de "próximos agentes" orientados a pricing de medicamentos, variación de precios, uso de medicamentos y lanzamiento de ensayos clínicos.
- Conectado al interés más amplio en huecos de mercado en compra hospitalaria y precios de medicamentos (línea también presente en el proyecto healthtech con Rodri y Rodrigo).
- Estaba planteado incorporar LangGraph a este tipo de agentes para darles más solidez técnica, sin cambiar el diseño de negocio ya definido.

---
*Documento reconstruido a partir de las notas guardadas de la conversación original (finales de agosto / inicio de septiembre 2026), ya que el archivo original vivía en el espacio de trabajo temporal de aquella sesión.*
