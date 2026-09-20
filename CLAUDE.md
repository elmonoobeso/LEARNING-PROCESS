# LEARNING-PROCESS — instrucciones para Claude

## Qué es este repo

Portfolio de aprendizaje de Miguel Ángel Leo Acedo (farmacia → data analyst) hacia un puesto
de **junior data analyst**. Detalle completo en `README.md`. Puntos clave que condicionan
cómo se trabaja aquí:

- Es público y lo pueden revisar reclutadores: el código y el historial de commits también
  son portfolio, no solo funcionalidad.
- Filosofía declarada del propio autor: honestidad sobre errores y trabajo incompleto — no
  se ocultan fallos, se documentan (`errores-recurrentes.md`).

## Regla de autoría (la más importante — leer antes de tocar cualquier ejercicio o agente)

**Claude nunca escribe el código de los ejercicios ni de los agentes en `Agentes/`.** El
código lo escribe siempre el usuario a mano. El uso permitido de Claude en el código es
exclusivamente:

1. Proponer o plantear ejercicios.
2. Corregir o **revisar** código después de que el usuario lo haya escrito (señalar
   problemas, explicar por qué, sugerir — no reescribir por él).
3. Generar documentación (READMEs, clasificación por tema).

Si el usuario pide explícitamente que Claude escriba o complete código de un ejercicio, es
una excepción puntual y debe quedar marcada explícitamente como tal en el README del
proyecto correspondiente (ver `Agentes/agente_2/README.md` para el precedente), nunca oculta
ni presentada como del usuario.

Esta regla **no aplica** a tareas de infraestructura del repo: git/GitHub, este archivo,
configuración de Ruff, scripts de `pre-commit`, READMEs — ahí Claude puede actuar con
normalidad.

## Estructura del repo

- `fundamentos-python/`, `numpy/`, `oop/`, `pandas/` — ejercicios sueltos por tema, cada uno
  con su propio README bilingüe.
- `Agentes/` — miniproyectos que ya resuelven un problema real (no solo practican sintaxis).
  Cada agente vive en su propia carpeta (`Agentes/agente_N/agente_N.py`, + README y `.env`
  si aplica). Tiene su propio `CLAUDE.md` con convenciones específicas.
- `dataset/`, `analisis_es/` — datos y salidas de análisis (no se versionan resultados, solo
  código — ver `.gitignore`).
- `errores-recurrentes.md` — registro de patrones de error, mantenido vía skill
  `analizador_errores`.

## Idioma: código en inglés, documentación bilingüe

Estándar de la industria: identificadores de código (variables, funciones, clases, nombres
de archivo y de proyecto) se escriben **en inglés**, aunque el resto del repo sea en
español. Comentarios y documentación (READMEs) siguen el patrón bilingüe ES/EN que ya usa
el repo.

## Workflow de git y GitHub

- **Una rama por unidad de trabajo** (un agente, una corrección concreta), no una rama para
  todo el repo en general. Nombre: `feature/agente-N-descripcion-corta` o
  `fix/descripcion-corta`.
- **Commits** en formato Conventional Commits: `tipo(alcance): mensaje corto en imperativo`.
  Tipos: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`. Cuerpo opcional explicando el
  porqué, no el qué (el diff ya dice el qué).
- Cuando el trabajo de la rama está terminado: push + Pull Request contra `main` +
  **squash merge** (un PR = un commit final limpio en `main`).
- **El usuario está aprendiendo este proceso activamente.** Claude ejecuta estos pasos de
  git/GitHub directamente (no se los delega al usuario), pero en cada acción (crear rama,
  commit, push, abrir PR, squash, borrar rama) explica en una lista de puntos simple, sin
  dar por sabida la terminología, qué está haciendo y por qué.
- **No se reescribe el historial de commits antiguo** (mensajes previos poco descriptivos
  incluidos) — es prueba de progreso real y coherente con la filosofía de honestidad del
  repo. El estándar de commits limpios aplica hacia adelante, no retroactivamente.

## Pull Requests como caso de estudio

La descripción de cada PR no es un trámite: es contenido de portfolio que un reclutador
puede leer. Estructura breve: qué problema resolvía, qué enfoque se tomó, qué se aprendió o
qué quedó pendiente.

## Documentación

READMEs bilingües ES/EN por carpeta temática, generados/reorganizados con la skill
`documentador_estudio`.

## Seguimiento de errores

Patrones de error recurrentes y huecos de conocimiento se registran en
`errores-recurrentes.md` vía la skill `analizador_errores`.

## Recap de fin de sesión

Al terminar una sesión de trabajo (cuando el usuario indica que lo deja por hoy, se despide,
o lo pide explícitamente), Claude hace un recap breve con dos partes:

1. **Qué se estudió/repasó/aprendió de nuevo** en la sesión (conceptos, herramientas,
   decisiones tomadas).
2. **Gaps o próximos pasos útiles** para las siguientes sesiones, priorizados según lo que
   más acerque al usuario a su objetivo de junior data analyst — no una lista genérica.

## Formato de código: Ruff

Ruff (format + check) se ejecuta automáticamente antes de cada commit vía `pre-commit`.
Cubre estilo (formateo) y también detección de bugs no relacionados con IA (variables no
definidas, imports sin usar, etc. — reglas de Pyflakes incluidas por defecto). No reescribe
lógica, solo aplica estilo y señala problemas — no entra en conflicto con la regla de
autoría.

## Secretos

Claves de API y credenciales van siempre en `.env`, nunca en el código ni en commits.
`.gitignore` ya excluye `__pycache__/`, `*.pyc` y las salidas generadas.
