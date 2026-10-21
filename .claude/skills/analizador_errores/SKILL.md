---
name: analizador-errores
description: Analiza el código del repo para detectar patrones de error recurrentes, huecos de conocimiento (conceptos poco usados o mal usados), prioriza por relevancia para data analytics/agentes, y trackea el progreso a lo largo del tiempo.
---

# Analizador de errores y huecos de conocimiento

## Cuándo se activa
Cuando el usuario pide "analiza mis errores", "actualiza el análisis de 
errores", invoca `/analizador-errores`, o desde la skill `cierre-sesion`.

## Qué código cuenta (importante)
Solo el código escrito por el usuario. Mira el modo de autoría de cada
proyecto en su README (tabla "Nota de autoría" del README raíz):
- Modo **Aprendizaje** → se analiza entero.
- Modo **Arquitectura** (p. ej. `Agente3_Ermenegildo`) → solo las partes
  que su README atribuye al usuario. El código de la IA nunca cuenta como
  error del usuario.
- Fuera de este repo (p. ej. SmartPharma, modo Producto) → no se analiza.

## Fuentes además del código
- Huecos de los apuntes vivos del Agente 3
  (`C:\Users\migue\Documents\LEARNING-PROCESS-recaps\apuntes_agente3_ermenegildo.md`,
  sección "Huecos de conocimiento"): se integran aquí para que haya una
  sola lista.
- Correcciones de los "Qué aprendí" del usuario: un malentendido de
  concepto es un hueco.
- Fallos de la comprensión verificada del código de la IA.
Marca estas entradas como "(de sesión)".

## Ejercicios de repaso
Solo cuando el usuario los pida, y solo para hacerlos en este repo
(LEARNING-PROCESS). Nunca los propongas por iniciativa propia.
- Dirígelos a las entradas de prioridad alta (o a las que pida el usuario).
- Cada ejercicio cita la entrada que trabaja.
- Una entrada pasa a "✅ Superado" cuando el usuario resuelve su ejercicio,
  o escribe código nuevo de ese concepto, sin repetir el error.

## Archivo de estado persistente
Mantiene un único archivo: `errores-recurrentes.md` en la raíz del repo.
Este archivo se actualiza incrementalmente, nunca se regenera desde cero
salvo que el usuario lo pida explícitamente.

## Primera ejecución (repo completo)
1. Analiza TODOS los archivos .py del repo (a través de las carpetas 
   temáticas ya organizadas por documentador-estudio, si existen).
2. Detecta dos categorías de error, siempre separadas:
   - **Errores de sintaxis/ejecución:** código que no corre (ej. 
     asignaciones inválidas, imports rotos, typos en sintaxis).
   - **Decisiones subóptimas:** código que ejecuta pero no es la forma 
     correcta o idiomática (ej. groupby mal indexado, bucles donde cabe 
     comprehension, falta de manejo de excepciones).
3. Detecta huecos de conocimiento: conceptos de la "lista de alto valor" 
   (ver abajo) que no aparecen en el repo desde hace tiempo, o que la 
   última vez que aparecieron fue con error.
4. Genera `errores-recurrentes.md` con la lista agrupada por prioridad.
5. Registra en el archivo qué commit/fecha fue el último analizado.

## Ejecuciones siguientes (incremental)
1. Compara con `git log` qué archivos son nuevos o se modificaron desde 
   la fecha registrada en `errores-recurrentes.md`.
2. Analiza SOLO esos archivos nuevos/modificados — no relee el resto.
3. Para cada patrón de error ya existente en la lista: si NO vuelve a 
   aparecer en el código nuevo, márcalo como "✅ Superado" y bájalo al 
   final del documento (no lo borres, es evidencia de progreso).
4. Si SÍ vuelve a aparecer, mantenlo o súbelo de prioridad, y suma la 
   nueva fecha/archivo como ejemplo adicional.
5. Añade patrones nuevos que no existieran antes.
6. Actualiza la fecha de último análisis.

## Lista de alto valor (para priorizar)
Conceptos que pesan más al detectar error o hueco, por ser centrales 
en data analytics / automatización con agentes:
pandas (groupby, transform, merge, manejo de nulos), manejo de 
excepciones/errores, comprehensions, encapsulamiento OOP, manejo de 
APIs/requests, estructuras de control en flujos de agentes, validación 
de tipos de datos, manejo de fechas.
Un error en uno de estos conceptos sube automáticamente de prioridad 
frente a errores en código irrelevante para ese objetivo.

## Formato de errores-recurrentes.md

# Errores recurrentes y huecos de conocimiento
Último análisis: AAAA-MM-DD (hasta commit <hash>)

Cuando pases esta lista para pedir ejercicios de repaso, ya viene 
agrupada por prioridad — no hace falta que añadas nada.

**Qué se analiza**: [párrafo corto con el alcance según modos de autoría]

## 🔴 Prioridad alta
- **[Concepto]** — [tipo: sintaxis/decisión subóptima/hueco] 
  [Descripción breve del patrón]. Visto en: [archivo(s), fecha(s)].

## 🟡 Prioridad media
[mismo formato]

## 🟢 Prioridad baja / repaso opcional
[mismo formato]

## ✅ Superados
[mismo formato, con fecha en que dejó de aparecer]

## Regla de oro
Nunca corrige el código directamente — solo detecta, documenta y 
prioriza. Nunca borra entradas "Superadas", son evidencia de progreso 
real y portfolio de aprendizaje.

## Tono
Directo y honesto, sin suavizar los patrones de error. El objetivo es 
utilidad para mejorar, no proteger el ego.