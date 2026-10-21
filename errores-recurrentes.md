# Errores recurrentes y huecos de conocimiento
Último análisis: 2026-10-21 (hasta commit b3640cc)

Cuando pases esta lista para pedir ejercicios de repaso, ya viene
agrupada por prioridad — no hace falta que añadas nada.

**Qué se analiza**: solo código escrito por mí (modo *Aprendizaje*), más las partes de
`Agente3_Ermenegildo` que su README atribuye al usuario. El código escrito por la IA no
cuenta como error mío. También entran los huecos detectados en sesión (apuntes del Agente 3,
correcciones de mis "Qué aprendí" y fallos de la comprensión verificada).

## 🔴 Prioridad alta

- **Función que devuelve `None` sin avisar tras capturar una excepción** — decisión
  subóptima recurrente (nuevo). `obtencion_datos` en `agente_2` y las tres funciones de
  obtención del agente 3 capturan `Timeout`/`HTTPError`/`ConnectionError`, imprimen un
  mensaje y terminan sin `return`: devuelven `None` en silencio. El error aparece después,
  más lejos y más confuso (p. ej. `for registro in self.datos` con `self.datos = None` lanza
  `TypeError`). Hay que decidir una política: relanzar la excepción o devolver algo
  explícito que quien llama compruebe. También señalado en los apuntes del Agente 3 (hueco 8).
  Visto en: Agentes/agente_2/agente_2.py (2026-09-03), Agentes/Agente3_Ermenegildo/agent_3.py
  (2026-10-09).

- **Grano de la tabla: un registro contado dos veces** — decisión subóptima (nuevo). En
  `AgenteFDA.validar_clases`, un mismo registro puede acabar dos veces en `no_validos` (clase
  inválida y campos vacíos) y a la vez en `validos_clase` y en `no_validos`. Los conteos que
  salen de esas listas quedan inflados sin dar error. Es el mismo hueco que los apuntes del
  Agente 3 llaman "grano" (hueco 2): decidir qué es una fila antes de transformar.
  Visto en: Agentes/agente_2/agente_2.py (2026-09-03).

- **Verificar la forma de los datos antes de usarlos** — hueco (nuevo, de sesión).
  `obtencion_datos_prevalencia` devuelve `datos["results"][0]` (solo el primer elemento, y
  la API de Socrata devuelve una lista directa, sin clave `results`), y en sesión costó
  distinguir `["results"]` de `["studies"]`. Antes de indexar, comprobar con `type()`,
  `.keys()` y `len()`. Apuntes del Agente 3, huecos 3 y 4.
  Visto en: Agentes/Agente3_Ermenegildo/agent_3.py (2026-10-09).

- **Pandas — olvidar reasignar operaciones que no mutan in-place** — decisión subóptima
  recurrente en dos archivos distintos: `df.drop_duplicates()` y
  `df["stock"].fillna(df["stock"].median())` se llaman sin reasignar en
  `pandas/2026-08-26_duplicados-nulos-outliers-iqr.py` (el propio autor documenta la confusión
  en el comentario: "porque no sale el valor corregido???"); `df.set_index("fecha")` y
  `df.sort_index()` tienen el mismo problema en `pandas/2026-08-29_series-temporales-rolling-groupby.py`.
  Es el mismo hueco conceptual repitiéndose 3 días después sin haberse consolidado.
  Visto en: pandas/2026-08-26, pandas/2026-08-29.

- **Pandas — groupby mal indexado/alineado** — decisión subóptima: en
  `pandas/2026-08-29_series-temporales-rolling-groupby.py`, la línea
  `df["ingresos_medio_producto"]=df.groupby("producto")["ingresos"].mean()` asigna
  directamente el resultado de un `groupby().mean()` (indexado por `producto`, con menos
  filas que `df`) a una columna del DataFrame original — esto no alinea correctamente y
  genera `NaN`/valores mal emparejados. La línea inmediatamente siguiente usa
  `.transform("mean")`, que sí es la forma correcta, así que el propio archivo contiene el
  contraste entre el patrón malo y el bueno sin que quede señalado como tal.
  Visto en: pandas/2026-08-29.

- **Validación de tipos con `typing`** — errores de sintaxis/ejecución: en
  `oop/2026-08-10_clases-filtrado-truthiness.py`, `ECommerceAnalyzer` usa
  `Dict[str,Dict[str,anyy]]` (typo `anyy` en vez de `Any`) → `NameError` al definir la clase;
  `PharmacyBatchAnalyzer` usa `Tuple(List[dict[str,any]])` con paréntesis en vez de corchetes,
  sintaxis inválida para genéricos de `typing` → error al evaluar la anotación. Dos fallos de
  sintaxis distintos sobre el mismo concepto en el mismo archivo — indica que el hint de tipos
  compuestos (`Dict`/`Tuple` anidados) todavía no está consolidado, más allá del typo puntual.
  Visto en: oop/2026-08-10.

- **`SyntaxError` bloqueante en pandas** — error de sintaxis/ejecución: en
  `pandas/2026-08-29_series-temporales-rolling-groupby.py`, la función `es_ventas_fuerte`
  contiene `int(i)=datos["unidades_vendidas"]`, una asignación a una llamada de función, que
  es un `SyntaxError` de Python — impide que el **archivo completo** se ejecute, no solo esa
  función. Es el error más severo del repo. La función también referencia
  `unidades_vendidas` sin que exista en su ámbito (debería ser `datos["unidades_vendidas"]`
  o el parámetro `i`).
  Visto en: pandas/2026-08-29.

- **Hueco: estructuras de control en flujos de agentes** — sigue abierto, pero ha avanzado.
  `agente_2` ya tiene un pipeline lineal con punto de entrada. Todavía no hay orquestación
  propia (estado explícito entre pasos, ramas condicionales, reintentos). Se cierra al
  implementar los nodos A→B→C del agente 3.
  Visto en: (ausencia — actualizado 2026-10-21).

## 🟡 Prioridad media

- **Claves duplicadas en un diccionario o en una lista de campos** — decisión subóptima
  (nuevo). En `analisis_estadistico` el diccionario `analisis` repite la clave
  `"analisisdf3"`: el segundo valor pisa al primero sin aviso y `analisis_nc` nunca llega al
  Excel. En sesión pasó lo mismo con `fields` (`OverallStatus` repetido, `Phase`/`Phases`).
  Apuntes del Agente 3, hueco 9.
  Visto en: Agentes/agente_2/agente_2.py (2026-09-03).

- **Bloques `try/except` copiados en cada función** — decisión subóptima (nuevo). El mismo
  bloque de tres `except` con el mismo mensaje cortado ("No se pudo conectar con la A")
  aparece en 4 funciones. Una función auxiliar de petición evitaría copiar el error y el
  mensaje.
  Visto en: Agentes/agente_2/agente_2.py, Agentes/Agente3_Ermenegildo/agent_3.py.

- **Código que se ejecuta al importar el archivo** — decisión subóptima (nuevo). `agente_1.1`
  llama a `genai.configure(api_key=os.environ[...])` al importarse: sin `.env` falla con
  `KeyError` antes de hacer nada. `agent_3.py` llama a la API al final del archivo sin
  `if __name__ == "__main__":`. `agente_2` sí lo hace bien: el patrón se conoce pero no se
  aplica siempre.
  Visto en: Agentes/agente_1.1/agente_1.1.py, Agentes/Agente3_Ermenegildo/agent_3.py.

- **Scope y firma de las funciones** — hueco (nuevo, de sesión). Bug de `params` (función
  que usaba la variable global en vez de su parámetro, ya corregido por mí) y dudas entre
  argumentos posicionales y por nombre (`params1=params`, `requests.get(url, params2, ...)`).
  Apuntes del Agente 3, huecos 5 y 6.
  Visto en: sesiones del agente 3 (2026-10).

- **Hueco: estadística descriptiva (coeficiente de variación)** — hueco (nuevo). En
  `anomalias_precio` queda una pregunta sin resolver en un comentario: *"¿cuál es la razón
  por la que se compara con la media?"*. El código calcula bien `std / media`, pero falta el
  porqué: la desviación relativa permite comparar productos de precios muy distintos.
  Visto en: Agentes/agente_1.1/agente_1.1.py (2026-09-02).

- **`None` frente a `NaN`** — hueco (nuevo, de sesión). Aparece al limpiar listas con
  `isinstance`; practicar `pd.isna` y `df.isna().sum()`. Apuntes del Agente 3, hueco 7.
  Visto en: sesiones del agente 3 (2026-10).

- **Estructuras de control — bug de variable en condición** — decisión subóptima: en
  `fundamentos-python/2026-08-04_normalizacion-segmentacion-sets.py`, `pipeline_control`
  compara `id` (la lista completa recibida como parámetro) contra `5`/`15` en vez de `i` (el
  elemento actual del bucle) — el `continue`/`break` nunca se dispara como se pretende.
  Visto en: fundamentos-python/2026-08-04.

- **Ejercicios sin terminar sobre validación por truthiness** — hueco/decisión pendiente:
  `procesar_registro` queda como stub (`pass`) tanto en
  `fundamentos-python/2026-08-05_while-defaults-fromkeys.py` como en
  `oop/2026-08-06_args-logging-clase-inventario.py` — el mismo patrón de ejercicio (filtrar
  con truthiness y acumular en una lista) queda incompleto dos veces en días distintos.
  Visto en: fundamentos-python/2026-08-05, oop/2026-08-06.

- **Type hint inválido como expresión booleana** — decisión subóptima: en
  `fundamentos-python/2026-08-05_while-defaults-fromkeys.py`,
  `def logs(*metricas:dict!=None,idd:list=None):` usa `dict!=None` (una comparación que
  evalúa a `True`) como anotación de tipo, en vez de `Optional[dict]` o similar. No rompe en
  runtime porque Python no valida anotaciones por defecto, pero revela que el propósito de
  los type hints (documentar/validar tipo esperado, no expresar una condición) no está claro
  todavía.
  Visto en: fundamentos-python/2026-08-05.

- **OOP — método privado sin exponer públicamente** — decisión subóptima: en
  `oop/2026-08-07_clase-datapipeline-logging-excepciones.py`, `DataPipeline.__calcular_duracion`
  es un método privado (name-mangled) pero la clase no tiene ningún método público que lo
  invoque — el cálculo de duración nunca se expone ni se ejecuta/testea.
  Visto en: oop/2026-08-07.

- **OOP — método que no retorna resultado útil** — decisión subóptima: en
  `oop/2026-08-11_clase-csvanalyzer-parseo.py`, `get_valid_stocks` filtra líneas válidas en
  `validos` pero termina con `return` vacío — el trabajo del método se pierde, no hay forma
  de usar el resultado desde fuera.
  Visto en: oop/2026-08-11.

- **`NameError` básico + archivo incompleto** — error de sintaxis/ejecución: en
  `oop/2026-08-11_clase-jsonapianalyzer-incompleta.py`, `ruta=dataset/"doc_prueba.json"` usa
  la variable `dataset` sin definir (debía ser `prueba_json`), y hay dos llamadas
  `open(self.__file_path,)` con coma colgante sin argumento — el archivo no llega a
  ejecutarse en ningún punto.
  Visto en: oop/2026-08-11.

## 🟢 Prioridad baja / repaso opcional

- **NumPy — atributos usados como métodos / funciones inexistentes** — errores de
  sintaxis/ejecución: `limpio.range()` no existe en un array de NumPy; `limpio.shape()` se
  llama como método cuando `shape` es un atributo (`limpio.shape`, sin paréntesis);
  `np.itemsize(limpio)` no existe como función standalone (`itemsize` es atributo del array);
  `np.random.randint(0,8,0,8)` repite los límites en la posición de `size`. NumPy no está en
  la lista de alto valor explícita, pero es la base de pandas.
  Visto en: numpy/2026-08-13.

- **Redundancia / código duplicado** — decisión subóptima menor: en
  `fundamentos-python/2026-08-03_eliminar-duplicados-orden.py`, se deduplica primero con un
  bucle manual y después se aplica `dict.fromkeys()` sobre el resultado ya limpio (doble
  trabajo). En `oop/2026-08-06_args-logging-clase-inventario.py`, `Inventario.obtener_resumen`
  y `obtener_resumen2` hacen exactamente lo mismo (comprensión vs. bucle explícito) sin que
  quede claro cuál es la versión "final".
  Visto en: fundamentos-python/2026-08-03, oop/2026-08-06.

- **Ventana deslizante O(n·k)** — decisión subóptima menor: en
  `fundamentos-python/2026-08-03_ventana-deslizante-maximos.py`, el máximo por ventana se
  recalcula con slicing en cada posición; una estructura tipo deque monotónico lo resolvería
  en O(n). No es un error, es una optimización futura.
  Visto en: fundamentos-python/2026-08-03.

- **Ejercicio sin terminar sobre tuplas/listas anidadas** — `congelar_registro` en
  `fundamentos-python/2026-08-03_tuplas-con-listas-mutables.py` no hace nada observable
  (no imprime ni retorna). Bajo impacto porque el concepto (mutabilidad anidada) no está en
  la lista de alto valor.
  Visto en: fundamentos-python/2026-08-03.

- **Roles de mensaje inventados para el LLM** — decisión subóptima menor (nuevo). La memoria
  usa `"role": "analista"`; las APIs de LLM solo aceptan roles fijos (`user`, `assistant` o
  `model`, `system`). Hoy no rompe nada porque esa memoria no se envía como conversación.
  Visto en: Agentes/agente_1.1/agente_1.1.py, Agentes/agente_2/agente_2.py.

- **Imports sin usar** — menor (nuevo). `numpy` y `json` en `agente_2` y `agent_3`. Ruff lo
  detectaría solo, pero el `pre-commit` que menciona `CLAUDE.md` no está configurado en el
  repo.
  Visto en: Agentes/agente_2/agente_2.py, Agentes/Agente3_Ermenegildo/agent_3.py.

- **NumPy para datos tabulares con bucles por grupo** — decisión subóptima menor (nuevo).
  `agente_1.1` agrupa por producto y paciente con bucles sobre `np.unique`, donde
  `groupby` lo resuelve en una línea. Ya corregido en la práctica: `agente_2` usa pandas.
  Visto en: Agentes/agente_1.1/agente_1.1.py (2026-09-02).

## ✅ Superados

- **Manejo de excepciones: `except` demasiado amplio o sin tipar** — ✅ superado el
  2026-09-03. Antes: `except:` desnudo en `fundamentos-python/2026-08-04` y
  `except Exception` genérico en `oop/2026-08-11`. En el código nuevo (`agente_2`,
  `agent_3`) se capturan siempre excepciones específicas de `requests` y el `Exception`
  genérico va al final. *El siguiente paso, qué devolver tras capturar, sigue abierto
  arriba.*

- **Hueco: manejo de APIs/requests** — ✅ superado el 2026-09-03. Antes no había ni una
  llamada HTTP en el repo. Ahora: `requests.get` con `params`, `timeout` y
  `raise_for_status()` en `agente_2` (API de la FDA) y en el agente 3 (ClinicalTrials.gov,
  CDC con App Token en cabecera).
