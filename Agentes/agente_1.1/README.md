# agente_1.1 — Analista de ventas de farmacia

> **Modo de autoría: Aprendizaje.** Código escrito a mano por mí; la IA solo revisa y
> documenta. / *Authorship mode: Learning. Hand-written by me; AI only reviews and documents.*

## Qué hace / What it does

**ES** — Mi primer agente. La clase `Agente` carga un CSV de ventas de farmacia con NumPy y
aplica tres reglas de negocio pensadas para el día a día de una farmacia:

| Método | Qué detecta |
|---|---|
| `detectar_stock_negativo` | Productos cuyo último stock registrado es negativo (descuadre de inventario) |
| `abuso_estupes` | Pacientes que superan un límite de unidades de estupefacientes (códigos ATC de opioides y anestésicos) |
| `anomalias_precio` | Productos con precio de compra (PUC) inestable, según su coeficiente de variación. El umbral es más estricto para medicamento (5 %) que para parafarmacia (25 %), distinguidos por el primer dígito del código nacional |

`extraer_listas` guarda los tres resultados como CSV en `listas_agente/`. La clase tiene una
`memoria` con mensajes `role`/`content` y su [mensaje de sistema](instrucciones_sistema.md),
preparada para que un LLM (Gemini) interprete los resultados.

**EN** — My first agent. The `Agente` class loads a pharmacy sales CSV with NumPy and applies
three business rules: negative stock, possible controlled-substance abuse per patient, and
unstable purchase prices (coefficient of variation, stricter for medicines than for
parapharmacy). Results are exported to CSV. A message memory and system prompt are ready
for an LLM, but not wired yet.

## Estado / Status

📚 **Referencia de diseño, no ejecutable** / *Design reference, not runnable*

- Falta el dataset `ventas_mes.csv` (no está en el repo) / *Dataset not included.*
- No tiene punto de entrada (`if __name__ == "__main__":`) / *No entry point.*
- Gemini se configura al importar el archivo (exige `Gemini_API_KEY` en `.env`), pero ningún
  método lo llama / *Gemini is configured at import time but never called.*

Columnas que espera el CSV / *Expected columns*: `codigo_nacional`, `nombre_medicamento`,
`stock_actual`, `cod_estupes` (código ATC), `id_paciente`, `cantidad`, `puc`.

## Lecciones de diseño / Design lessons

- Las reglas de negocio de farmacia se pueden traducir a código auditable: umbrales, listas
  de códigos y agregaciones por producto o paciente.
- Con NumPy cada agregación exige un bucle manual sobre `np.unique`; por eso en `agente_2`
  pasé a pandas (`groupby`).
- Decisión documentada como retrospectiva en
  [decisiones-arquitectura.md](../decisiones-arquitectura.md).

## Tecnologías / Stack

Python · NumPy · csv · python-dotenv · google-generativeai (configurado, sin usar)
