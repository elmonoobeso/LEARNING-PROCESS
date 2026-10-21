# Data Analyst — Portfolio de aprendizaje

> ## ⚠️ Nota de autoría — modos de trabajo con IA
> Este repositorio es para aprender, y la IA (Claude) forma parte de cómo aprendo. Cada
> proyecto declara **un modo** de trabajo, así queda claro qué es mío:
>
> | Modo | Quién escribe el código | Dónde |
> |---|---|---|
> | **Aprendizaje** | **Yo, a mano.** La IA propone, revisa **después** y documenta | `fundamentos-python/`, `oop/`, `numpy/`, `pandas/`, `agente_1.1`, `agente_2` |
> | **Arquitectura** | **La IA, dirigida por mí.** Yo diseño y decido; aprendo criterio de arquitectura | `Agente3_Ermenegildo` |
>
> La documentación (READMEs, apuntes) la genera la IA a partir de mi trabajo y mis
> decisiones. Lo que no encaja en el modo de un proyecto se declara en su commit o PR, nunca
> se oculta.

## Quién soy

Miguel Ángel Leo Acedo. **Data & IA aplicada a farmacia**: análisis de datos de negocio,
optimización de stock y agentes LLM sobre datos sanitarios. Más de 5 años trabajando en
farmacia como técnico y creador de [SmartPharma](https://github.com/elmonoobeso/SmartPharma),
herramienta de análisis de negocio y predicción de demanda en piloto con una farmacia real.
Formación: Grado en Farmacia (en curso).

Por eso casi todos los ejercicios de este repositorio usan datos de farmacia, medicamentos,
stock, ventas y alertas sanitarias: no es casualidad, es el dominio que mejor conozco y donde
aporto valor con datos.

Mi objetivo es un puesto de **data analyst en el sector salud/farmacia**, y seguir
aprendiendo con la misma lógica con la que está construido este repositorio: sin atajos, sin
ocultar lo que todavía no domino, y siempre preguntándome para qué sirve realmente lo que
estoy construyendo.

## Qué hacemos aquí y por qué

Este repositorio no es una colección de ejercicios sueltos hechos por hacer. Cada carpeta
temática es una fase de aprendizaje deliberada, y `Agentes/` es un paso más allá: proyectos
que ya intentan resolver un problema real (analizar ventas de farmacia, cruzar alertas de la
FDA, interpretar resultados con un LLM), no solo practicar sintaxis.

La idea de fondo es simple: **no construyo herramientas por construirlas — construyo
herramientas que tengan sentido de utilidad**, aunque estén incompletas o tengan errores
todavía. Por eso los fallos y los ejercicios sin terminar se documentan en vez de esconderse
(ver `errores-recurrentes.md`): un portfolio honesto sobre lo que sé y lo que estoy
aprendiendo me parece más útil, tanto para quien lo revise como para mí mismo, que uno que
solo enseña resultados pulidos.

## Cómo pretendo seguir aprendiendo

- **Seguimiento activo de mis propios errores** (`errores-recurrentes.md`): cuando un patrón
  de error se repite, queda registrado y priorizado, no se repite en silencio.
- **De ejercicio suelto a herramienta con propósito**: la progresión de este repo va desde
  fundamentos de Python hasta `Agentes/`, proyectos que ya combinan APIs reales, pandas y un
  LLM para producir algo que un farmacéutico podría usar de verdad.
- **Revisión honesta, no autocomplaciente**: en los ejercicios reviso y corrijo con ayuda de
  IA después de escribir el código, nunca antes — el objetivo es entender el fallo, no que
  desaparezca.
- **Criterio antes que sintaxis en los agentes**: en `Agentes/` lo importante es aprender a
  organizar, decidir y justificar la arquitectura. Cada decisión queda registrada con sus
  alternativas en [`Agentes/decisiones-arquitectura.md`](Agentes/decisiones-arquitectura.md).

## Cómo aprendo (workflow)

Cada sesión de trabajo termina con la misma rutina (skill
[`cierre-sesion`](.claude/skills/cierre_sesion/SKILL.md)):

1. **Explico lo aprendido con mis palabras** en 3 líneas, y la IA las corrige. Lo que
   entiendo mal se convierte en un hueco de conocimiento registrado.
2. **Compruebo que entiendo el código que escribe la IA** antes de fusionarlo: respondo
   preguntas sobre él o reescribo de memoria una función clave.
3. **Registro las decisiones** en el repo, con las alternativas descartadas.
4. **Actualizo mis errores** en [`errores-recurrentes.md`](errores-recurrentes.md): solo
   cuenta mi código, y un error pasa a "superado" cuando dejo de cometerlo.
5. **Cada PR cuenta qué se aprendió** ([plantilla](.github/pull_request_template.md)).

Los ejercicios de repaso sobre mis errores los pido yo, cuando quiero, y se hacen en este
repositorio.

## Estructura

```
.
├── fundamentos-python/   # Listas, tuplas, dicts, sets, strings, bucles (sin librerías)
├── oop/                  # Clases, atributos privados, typing, logging/excepciones
├── numpy/                # Arrays, operaciones matriciales, PCA manual
├── pandas/               # DataFrames, limpieza de datos, groupby, series temporales
├── Agentes/              # Proyectos con APIs reales + pandas + LLM
│   ├── agente_1.1/           # Primer agente, referencia de diseño
│   ├── agente_2/             # AgenteFDA: retiradas de medicamentos (API FDA + Gemini)
│   ├── Agente3_Ermenegildo/  # Huecos terapéuticos en biosimilares (en progreso)
│   ├── apuntes-arquitectura/ # Guía de estudio de diseño de agentes
│   └── decisiones-arquitectura.md  # Registro de decisiones con alternativas
├── dataset/              # Datasets de ejemplo usados por los ejercicios
├── requirements.txt      # Dependencias del repositorio, comentadas en ES/EN
├── errores-recurrentes.md  # Seguimiento de patrones de error y huecos de conocimiento
├── CLAUDE.md             # Reglas de trabajo con IA (autoría, git, estilo)
├── .claude/skills/       # Skills propias: cierre de sesión, documentación, análisis de errores
└── .github/              # Plantilla de Pull Request
```

Cada carpeta temática tiene su propio `README.md` con una entrada detallada por ejercicio
(fecha, concepto, dificultad, estado, qué practica, notas y autoría), en español e inglés.

## Resumen de ejercicios por tema

| Tema | Ejercicios | Rango de fechas | Estado general |
|---|---|---|---|
| [fundamentos-python](fundamentos-python/README.md) | 9 | 2026-07-31 → 2026-08-11 | 6 ✅ funcionales · 3 ⚠️ con errores/incompletos |
| [oop](oop/README.md) | 5 | 2026-08-06 → 2026-08-11 | 4 ⚠️ con errores/incompletos · 1 🔄 en progreso |
| [numpy](numpy/README.md) | 2 | 2026-08-13 → 2026-08-21 | 1 ✅ funcional · 1 ⚠️ con errores |
| [pandas](pandas/README.md) | 4 | 2026-08-25 → 2026-08-29 | 2 ✅ funcionales · 2 ⚠️ con errores |
| Agentes | 3 | 2026-08 → 2026-10 | [`agente_2`](Agentes/agente_2/README.md) ✅ ejecuta de principio a fin (API FDA + pandas + Gemini); [`agente_1.1`](Agentes/agente_1.1/README.md) 📚 primer agente (NumPy, reglas de negocio de farmacia), referencia de diseño no ejecutable; [`Agente3_Ermenegildo`](Agentes/Agente3_Ermenegildo/README.md) 🔄 fetch de ClinicalTrials.gov funcionando, orquestación con LangGraph decidida |

**Total: 23 ejercicios/proyectos.**

## Cómo ejecutar

```
pip install -r requirements.txt
```

Los proyectos de `Agentes/` necesitan además su propio `.env` (no incluido, cada carpeta
tiene su `.gitignore`) con una clave de API de Gemini — ver el README de cada agente.

## Nota sobre las fechas

Las fechas usadas en la reorganización de los ejercicios por tema corresponden a la **fecha
de modificación del archivo** (más granular que el historial de git, que en este repo agrupa
varios archivos en los mismos commits). A partir de esa reorganización, el historial de git es
la fuente de verdad para los ejercicios nuevos.

## Licencia

[MIT](LICENSE) — puedes reutilizar libremente el código de este repositorio.

---

# Data Analyst — Learning Portfolio (EN)

> ## ⚠️ Authorship note — AI work modes
> This is a learning repository and AI (Claude) is part of how I learn. Each project
> declares **one mode**:
>
> | Mode | Who writes the code | Where |
> |---|---|---|
> | **Learning** | **Me, by hand.** AI proposes, reviews **after** writing and documents | `fundamentos-python/`, `oop/`, `numpy/`, `pandas/`, `agente_1.1`, `agente_2` |
> | **Architecture** | **AI, directed by me.** I design and decide; I train architecture judgment | `Agente3_Ermenegildo` |
>
> Documentation is generated by AI from my work and decisions. Anything outside a project's
> mode is declared in its commit or PR, never hidden.
>
> **How I learn:** every session ends with the same routine: I explain what I learned in
> my own words and AI corrects it; I verify I understand any AI-written code before merging;
> decisions are logged with their alternatives; and my error log only counts my own code.

## Who I am

Miguel Ángel Leo Acedo. **Data & AI for pharmacy**: business analytics, inventory
optimization and LLM agents on healthcare data. 5+ years working in pharmacy as a
technician, and creator of [SmartPharma](https://github.com/elmonoobeso/SmartPharma), a
business-analytics and demand-forecasting tool piloted in a real pharmacy. Education:
Pharmacy degree (in progress). That's why most exercises here use pharmacy, drug stock,
sales, and health-alert data: it's the domain I know best and where I bring value with
data. My goal is a **data analyst role in healthcare/pharmacy**, and to keep learning the same way this repository is built:
no shortcuts, nothing hidden, always asking what a tool is actually useful for.

## What we do here and why

This isn't a pile of exercises done for their own sake. Each topic folder is a deliberate
learning phase, and `Agentes/` goes further: projects that already attempt to solve a real
problem (analyzing pharmacy sales, cross-referencing FDA recalls, interpreting results with an
LLM), not just practicing syntax. **I don't build tools just to build them — I build tools
meant to be genuinely useful**, even while incomplete. Failures and unfinished exercises are
documented, not hidden (see `errores-recurrentes.md`) — an honest portfolio about what I know
and what I'm still learning is more useful, to a reviewer and to myself, than one that only
shows polished results.

## How I plan to keep learning

- **Active tracking of my own errors** (`errores-recurrentes.md`): recurring patterns get
  logged and prioritized, not silently repeated.
- **From loose exercise to purposeful tool**: this repo's progression runs from Python
  fundamentals to `Agentes/`, projects that already combine real APIs, pandas, and an LLM to
  produce something a pharmacist could actually use.
- **Honest review, not self-flattering**: in the exercises I review and correct with AI help
  after writing the code, never before — the goal is understanding the failure, not making
  it disappear.
- **Judgment over syntax in agents**: in `Agentes/` the point is learning to organize, decide
  and justify architecture. Every decision is logged with its alternatives in
  [`Agentes/decisiones-arquitectura.md`](Agentes/decisiones-arquitectura.md).

See each topic folder's `README.md` for the full per-exercise breakdown in both Spanish and
English.
