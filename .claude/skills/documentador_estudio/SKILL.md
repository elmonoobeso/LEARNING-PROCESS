---
name: documentador-estudio
description: Documenta y reorganiza ejercicios de estudio de Python/pandas/agentes en un repo de portfolio, clasificando por tema y generando READMEs bilingües (ES/EN).
---

# Documentador de estudio

## Cuándo se activa
Cuando el usuario pide "organiza el repo", "documenta esto" o similar, sin más detalle.

## Alcance por defecto (si el usuario no especifica archivos)
1. TODOS los .py sueltos en la raíz del repo (para clasificarlos).
2. Las carpetas temáticas y `Agentes/`: detecta archivos o agentes nuevos
   sin entrada en su README, y READMEs desfasados respecto al código.
3. El README raíz: tabla resumen, estructura y nota de autoría al día.
Ignora por defecto: datasets, .json, .csv, y cualquier archivo de
configuración — solo tócalos si el usuario lo pide explícitamente.

## Carpetas temáticas (crea las que falten)
/fundamentos-python, /oop, /numpy, /pandas, /Agentes
(si aparece un tema nuevo, p. ej. SQL, propone la carpeta antes de crearla)

## Proceso, paso a paso
1. Identifica tema y concepto concreto de cada archivo.
2. Obtén la fecha real vía `git log` de cada archivo; si no hay 
   historial, pregunta al usuario la fecha aproximada.
3. Renombra y mueve a `/<tema>/AAAA-MM-DD_nombre-descriptivo.py`.
4. Detecta errores de sintaxis/lógicos sin corregirlos — solo 
   márcalos y anota el fallo brevemente.
5. Genera/actualiza README.md de la carpeta con la plantilla ES/EN 
   de más abajo, una entrada por archivo.
6. Actualiza el README.md raíz: nota de autoría, estructura, tabla 
   resumen de ejercicios por tema.
7. Sugiere mensaje de commit: `docs(tema): añade ejercicio de <concepto>`.

## Regla de oro
SIEMPRE muestra el plan completo (archivo → carpeta → nombre nuevo) 
y espera confirmación antes de mover, renombrar o crear nada.
Nunca borra ni "arregla" código salvo instrucción explícita.

## Regla de autoría (importante, no opcional) — por niveles
La autoría se declara por niveles; la fuente de verdad es la tabla
"Nota de autoría" del README.md raíz:
- Ejercicios (fundamentos-python, oop, numpy, pandas): escritos a mano
  por el usuario. La IA solo propone ejercicios, revisa después de
  escritos y genera documentación.
- agente_1.1 y agente_2: escritos por el usuario, con excepciones
  puntuales marcadas línea a línea en su README.
- Agente3_Ermenegildo: código escrito por la IA bajo dirección del
  usuario (diseño y decisiones suyas); reparto exacto en su README.

Nunca atribuyas al usuario código que no escribió, ni a la IA código
que sí escribió él. Si no está claro qué nivel aplica, pregunta.

La declaración debe aparecer siempre, de forma visible, en:
- El README.md raíz del repo (sección destacada al principio, no al final)
- Cada README.md temático y de agente (nota breve al inicio)
- Cada entrada individual de ejercicio (campo "Autoría")

No la omitas nunca, no la suavices, y no la muevas a un lugar poco 
visible del documento — es una declaración de integridad que el 
usuario quiere que se vea primero, no como nota al pie.

## Plantilla de entrada (ES)
**Fecha:** · **Concepto:** · **Dificultad:** Básico/Intermedio/Avanzado
**Estado:** ✅ Funcional / ⚠️ Con errores conocidos / 🔄 En progreso
**Qué practica:** · **Notas/aprendizajes:**
**Autoría:** Escrito a mano sin asistencia de IA. IA usada únicamente 
para corrección/revisión posterior y para generar esta documentación.
**Código:** [enlace]

## Plantilla de entrada (EN)
[misma estructura traducida]

## Tono
Profesional pero honesto. Los fallos se documentan como aprendizaje, 
nunca se ocultan ni se minimizan.