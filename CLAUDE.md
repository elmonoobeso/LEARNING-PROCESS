# LEARNING-PROCESS — instrucciones para Claude

## Qué es este repo

Portfolio de aprendizaje de Miguel Ángel Leo Acedo (data & IA aplicada a farmacia; +5 años
como técnico en farmacia, estudiante del Grado en Farmacia, creador de SmartPharma) hacia un
puesto de **data analyst en el sector salud/farmacia**. Al describirle: primero el rol
profesional, luego la experiencia, y la formación al final; nunca "farmacéutico". Detalle completo en `README.md`. Puntos clave que condicionan
cómo se trabaja aquí:

- Es público y lo pueden revisar reclutadores: el código y el historial de commits también
  son portfolio, no solo funcionalidad.
- Filosofía declarada del propio autor: honestidad sobre errores y trabajo incompleto — no
  se ocultan fallos, se documentan (`errores-recurrentes.md`).

## Regla de autoría (la más importante — leer antes de tocar cualquier ejercicio o agente)

Cada proyecto declara **un modo de autoría**, una sola vez (tabla en la "Nota de autoría"
del `README.md` raíz). No se cuentan ni se listan excepciones:

- **Aprendizaje** — `fundamentos-python/`, `oop/`, `numpy/`, `pandas/`, `agente_1.1`,
  `agente_2`: regla estricta de abajo.
- **Arquitectura** — `Agentes/Agente3_Ermenegildo/` (decidido por el usuario el
  2026-10-09): Claude escribe el código bajo su dirección; el usuario diseña y decide. Ver
  `Agentes/CLAUDE.md`.

**Regla estricta (modo Aprendizaje): Claude nunca escribe el código de los ejercicios.** El código lo escribe
siempre el usuario a mano. El uso permitido de Claude en el código es exclusivamente:

1. Proponer o plantear ejercicios.
2. Corregir o **revisar** código después de que el usuario lo haya escrito (señalar
   problemas, explicar por qué, sugerir — no reescribir por él).
3. Generar documentación (READMEs, clasificación por tema).

Si el usuario pide explícitamente que Claude escriba o complete código en modo Aprendizaje,
se declara en el mensaje del commit o en la descripción del PR, nunca se oculta ni se
presenta como del usuario. No se añade a ninguna lista del README.

Esta regla **no aplica** a tareas de infraestructura del repo: git/GitHub, este archivo,
configuración de Ruff, scripts de `pre-commit`, READMEs — ahí Claude puede actuar con
normalidad.

## Estilo de respuesta de Claude

- **Conciso y directo**: ir al grano, sin rodeos ni resúmenes redundantes al final. Preferir
  frases cortas a párrafos largos.
- **Esquematizado**: usar listas, encabezados y bloques de código en vez de prosa larga,
  salvo que el contenido sea genuinamente narrativo (p. ej. los recaps de fin de sesión).
- **Basado en fuentes fiables**: cuando la respuesta dependa de información externa que
  cambia con el tiempo (APIs, SDKs, frameworks, documentación de terceros), verificar con
  búsqueda web en vez de fiarse solo del conocimiento entrenado, y citar la fuente. Esto ya
  se pedía en `Agentes/CLAUDE.md` para decisiones de arquitectura ("Vigencia") — aquí se
  extiende a todo el repo.

Esto aplica al estilo de las respuestas en la conversación, no a la regla de autoría de
arriba (esa sigue mandando sobre quién escribe el código).

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

**Las decisiones no se quedan en el chat.** Toda decisión de diseño, arquitectura o
autoría tomada en una sesión se escribe en el repo **antes de cerrar la sesión o el PR**
(README del agente/carpeta afectada y, si es de arquitectura,
`Agentes/decisiones-arquitectura.md`). Antes de abrir un PR, comprobar que el README raíz
(tabla resumen, estructura, nota de autoría) sigue reflejando el estado real del repo.

## Workflow de aprendizaje

Objetivo: que cada sesión fije conocimiento, no solo que produzca código.

1. **"Qué aprendí" lo escribe el usuario; Claude lo corrige.** 3 líneas con sus palabras
   por ejercicio, agente o PR. Claude nunca las redacta por él: las corrige (concepto
   erróneo, impreciso o incompleto) explicando el porqué, y los malentendidos se registran
   como huecos.
2. **Comprensión verificada del código de la IA.** Antes de fusionar código escrito por
   Claude (modo Arquitectura), el usuario responde 3 preguntas sobre él o reescribe de
   memoria una función clave. Si falla, no se bloquea el merge: se registra el hueco.
3. **Ejercicios de repaso: solo cuando el usuario los pida** y solo para hacerlos en este
   repo. Claude no los propone por iniciativa propia.
4. **Rutina única de cierre:** skill `cierre-sesion`.

## Seguimiento de errores

Patrones de error recurrentes y huecos de conocimiento se registran en
`errores-recurrentes.md` vía la skill `analizador_errores`. Solo cuenta el código escrito
por el usuario; el de la IA nunca se le atribuye como error.

## Recap de fin de sesión

Forma parte de la skill `cierre-sesion`. Al terminar una sesión de trabajo (cuando el
usuario indica que lo deja por hoy, se despide, o lo pide explícitamente), Claude ejecuta
esa skill, que acaba con un recap breve en dos partes:

1. **Qué se estudió/repasó/aprendió de nuevo** en la sesión (conceptos, herramientas,
   decisiones tomadas).
2. **Gaps o próximos pasos útiles** para las siguientes sesiones, priorizados según lo que
   más acerque al usuario a su objetivo de data analyst en salud/farmacia — no una lista genérica.

## Formato de código: Ruff

**Pendiente de configurar** (a 2026-10-21 no hay `.pre-commit-config.yaml` ni configuración
de Ruff en el repo). Objetivo: que Ruff (format + check) se ejecute automáticamente antes de
cada commit vía `pre-commit`. Cubre estilo (formateo) y también detección de bugs no relacionados con IA (variables no
definidas, imports sin usar, etc. — reglas de Pyflakes incluidas por defecto). No reescribe
lógica, solo aplica estilo y señala problemas — no entra en conflicto con la regla de
autoría.

## Secretos

Claves de API y credenciales van siempre en `.env`, nunca en el código ni en commits.
`.gitignore` ya excluye `__pycache__/`, `*.pyc` y las salidas generadas.
