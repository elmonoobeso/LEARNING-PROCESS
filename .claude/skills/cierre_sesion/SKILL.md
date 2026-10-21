---
name: cierre-sesion
description: Rutina única de fin de sesión en LEARNING-PROCESS. Encadena el "qué aprendí" del usuario (corregido por Claude), la comprensión verificada del código escrito por la IA, el registro de decisiones, la actualización de errores y apuntes, la revisión de la documentación y el recap. Úsala cuando el usuario diga que lo deja por hoy, se despida o invoque /cierre-sesion.
---

# Cierre de sesión

## Por qué existe
Antes había cuatro mecanismos manuales (recap, apuntes vivos, documentador y
analizador) que se activaban por separado y por eso se desfasaban. Esta skill
los ejecuta en orden, una sola vez, al terminar.

## Pasos (en este orden; salta los que no apliquen y di cuáles has saltado)

1. **Qué aprendí (lo escribe el usuario).** Pide al usuario 3 líneas, con sus
   palabras, sobre lo trabajado en la sesión. No las redactes tú.
   - Corrígelas: concepto erróneo, impreciso o incompleto. Explica el porqué
     de cada corrección (eje de decisión + analogía, sin tablas exhaustivas).
   - Cuando el usuario dé por buena la versión corregida, va a la entrada del
     README del ejercicio o agente (campo "Qué aprendí") o a la descripción
     del PR.
   - Cada malentendido se apunta como hueco "(de sesión)" en el paso 4.

2. **Comprensión verificada** (solo si en la sesión la IA escribió código que
   se va a fusionar, p. ej. en modo Arquitectura). Antes del merge, el usuario
   hace una de estas dos cosas:
   - responder 3 preguntas concretas sobre ese código (qué hace, por qué así y
     qué pasaría si cambiara X), o
   - reescribir de memoria una función clave y compararla con la original.

   Si falla, no bloquea el merge: se registra como hueco "(de sesión)" en el
   paso 4.

3. **Decisiones.** Toda decisión de diseño, arquitectura o autoría tomada en
   la sesión se escribe en el repo: en el README del agente o carpeta y, si es
   de arquitectura, en `Agentes/decisiones-arquitectura.md` (Contexto /
   Opciones / Elección / Aprendizaje).

4. **Errores y huecos.** Ejecuta la skill `analizador_errores` en modo
   incremental, incluyendo los huecos de los pasos 1 y 2. No propongas
   ejercicios salvo que el usuario los pida.

5. **Apuntes vivos** (solo si la sesión fue del Agente 3). Actualiza
   `C:\Users\migue\Documents\LEARNING-PROCESS-recaps\apuntes_agente3_ermenegildo.md`
   según su procedimiento (marcador de línea del transcript).

6. **Documentación.** Comprueba con la skill `documentador_estudio` que el
   README de cada carpeta tocada y el README raíz (tabla, estructura, modos
   de autoría) reflejan el estado real.

7. **Recap.** Recap breve en dos partes (qué se aprendió y gaps o próximos
   pasos priorizados para el objetivo profesional del usuario). PDF con el
   generador de `C:\Users\migue\Documents\LEARNING-PROCESS-recaps\_tools\`.

8. **Git.** Si hay trabajo sin subir: commit, push y PR con la plantilla del
   repo (problema / enfoque / qué aprendí / pendiente), narrando cada paso.

## Regla de oro
Nada de lo decidido o aprendido en la sesión se queda solo en el chat.
