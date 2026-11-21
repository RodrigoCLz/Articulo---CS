# DECISIONES

Registro de decisiones de diseño. Cada entrada indica fecha, motivo y estado.

Estados:
- **APROBADA:** decidida por el usuario.
- **PROPUESTA:** recomendada por el asistente; pendiente de aprobación.
- **PENDIENTE:** falta un dato o una decisión para cerrar el punto.
- **REGISTRO DE CAMBIO:** modificación posterior a una decisión ya aprobada.

Regla: ningún cambio a una decisión aprobada se aplica después de congelar el preregistro (`prereg-v1`) sin una entrada nueva aquí.

---

## Modelos y ejecución

### D-01 · Variante de razonamiento `medium` en ambos modelos
- **Fecha:** 2026-11-20
- **Motivo:** coste razonable y mismo nivel para las tres condiciones. Con `high`, el razonamiento multiplicaba los tokens de salida.
- **Estado:** APROBADA.

### D-21 · Modelos: solo API, sin modelos locales
- **Fecha:** 2026-11-20
- **Motivo:** la RTX 3050 de 4 GB solo admite modelos pequeños o cuantizados. El usuario decidió usar modelos de OpenCode Go.
- **Modelos:** `opencode-go/gpt-6-luna` y `opencode-go/claude-haiku-5-5`.
- **Estado:** APROBADA.

### D-07 · Temperatura fija donde el modelo la acepte
- **Fecha:** 2026-11-21
- **Motivo:** permite reducir variación entre repeticiones. Los parámetros que un modelo ignora se registran, porque algunos modelos con razonamiento no aceptan temperatura.
- **Alternativas descartadas:** temperatura por defecto del proveedor (no se controla) y temperatura 0 forzada (puede no ser aceptada).
- **Estado:** APROBADA (opción C).

### D-13 · Versiones fijas: Qiskit 2.x con lockfile
- **Fecha:** 2026-11-21
- **Motivo:** los cambios de API entre versiones (por ejemplo, la eliminación de `execute` en Qiskit 1.x) confundirían corrección con deriva de versión.
- **Verificación (PyPI, 2026-11-21):** Qiskit 2.6.2 publica wheels `cp310-abi3` para Linux x86_64, que sirven para Python 3.14. qiskit-aer 0.18.4 publica wheels `cp314` para Linux. **Falta la instalación real** en el entorno del proyecto; se hace en la Fase 2 y se registra en el lockfile.
- **Si la instalación falla:** Python 3.12 con `uv` dentro del proyecto, registrado como desviación en este archivo.
- **Estado:** APROBADA (opción B). Compatibilidad verificada en metadatos; pendiente de instalación real.

---

## Diseño experimental

### D-04 · 4 repeticiones por tarea y condición
- **Fecha:** 2026-11-20
- **Motivo:** presupuesto disponible. La regla anterior ("5 si el costo ≤ 70%, si no 3") queda sustituida por un valor fijo.
- **Consecuencia:** la simulación de potencia debe hacerse con 4 repeticiones.
- **Estado:** APROBADA.

### D-15 · 50 tareas, 10 categorías × 5
- **Fecha:** 2026-11-21
- **Decisión:** 50 tareas organizadas en 10 categorías de 5 tareas. Categorías: Bell/GHZ, Deutsch-Jozsa, Bernstein-Vazirani, Grover, QFT, teleportación, superdense coding, estimación de fase (QPE), un algoritmo variacional y QAOA. Por categoría: 2 pequeñas, 2 medianas y 1 grande, dentro del límite de 8 qubits.
- **Motivo:** el usuario eligió 50 tareas para mejorar la potencia de H1 (D-25). Se amplió de 6 a 10 categorías para mantener 5 tareas por categoría.
- **Versión anterior:** 30 tareas, 6 categorías × 5 (aprobada el 2026-11-21 y sustituida el mismo día).
- **Consecuencia:** 1200 episodios por modelo y configuración, frente a 720 con 30 tareas. El coste sube en la misma proporción.
- **Estado:** APROBADA (REGISTRO DE CAMBIO sobre la versión de 30 tareas).

### D-05 · Solo tareas propias; sin Qiskit HumanEval como held-out
- **Fecha:** 2026-11-21
- **Motivo:** Qiskit HumanEval es público desde 2024, así que es posible que los modelos lo hayan visto durante el entrenamiento. Chang et al. (preprint) documenta el problema de los benchmarks públicos.
- **Estado:** APROBADA.

### D-06 · Sin control B-tok
- **Fecha:** 2026-11-21
- **Motivo:** el usuario decidió no incluirlo. Consecuencia: la conclusión de H1 se limita a "C supera a B". No podemos atribuir la mejora a la verificación frente a gastar más tokens.
- **Estado:** APROBADA. Registrado como limitación.

### D-14 · Parada temprana
- **Fecha:** 2026-11-21
- **Motivo:** presupuesto. B termina al pasar sus comprobaciones de ejecución, y C al pasar sus pruebas del bucle. Ninguna termina por las pruebas reservadas.
- **Estado:** APROBADA (criterio de parada).

### D-14b · Iteraciones máximas: 5 por episodio
- **Fecha:** 2026-11-21
- **Motivo:** tope que limita el coste sin ser arbitrario para tareas de 1 a 8 qubits. Con `medium`, cinco iteraciones dan un coste acotado y permiten que C corrija errores que un solo reintento no corrige.
- **Decidido por:** asistente, por delegación del usuario.
- **Estado:** APROBADA POR DELEGACIÓN.

### D-02 · Tope de tokens por episodio, fijado tras el piloto
- **Fecha:** 2026-11-21
- **Decisión:** la **regla** se fija ahora y el **valor** se fija después del piloto (Fase 5).
  - Tope por episodio: T = 5 × q95 de tokens por llamada medidos en el piloto, redondeado a miles hacia arriba.
  - Justificación: 5 es el máximo de iteraciones (D-14b). Con T, un episodio cubre el 95% de las llamadas en el peor caso razonable.
  - Un episodio que supera T se trunca y cuenta como **no resuelto**. Se reporta el número de truncados por condición y modelo.
  - Si el coste total estimado de la Fase 6 excede la cuota disponible, la desviación se registra aquí antes de cambiar el número de repeticiones.
- **Motivo:** el coste real por llamada con `medium` no se conoce todavía. Fijar el valor antes de medirlo sería adivinar.
- **Presupuesto de referencia:** unos **3 USD** a precio de lista para las ~2 800 llamadas de los dos modelos (supuestos: 3 000 tokens de entrada y 1 500 de salida por llamada, precio base, sin caché). Lo aprueba el usuario como referencia, sin conocer el límite de su cuota.
- **Control durante el piloto:** si el coste medido por llamada implica un total mayor que **el doble** de la referencia (unos 6 USD), la ejecución se detiene y se reporta antes de la Fase 6.
- **Límite de cuota:** el usuario no puede compartirlo. Se trata como desconocido, y la referencia de 3 USD es el control.
- **Estado:** REGLA APROBADA. Referencia de 3 USD APROBADA por el usuario. Valor del tope por episodio PENDIENTE del piloto.

---

## Análisis estadístico

### D-03 · Unidad de análisis: la tarea
- **Fecha:** 2026-11-21
- **Motivo:** las repeticiones de la misma tarea no son independientes. Bootstrap pareado sobre tareas.
- **Estado:** APROBADA.

### D-09 · Shots 8192, α = 0,01 por prueba con Bonferroni por programa
- **Fecha:** 2026-11-21
- **Motivo:** equilibrio entre potencia y coste de simulación. La corrección por programa evita falsos positivos.
- **Estado:** APROBADA.

### D-17 · Análisis por modelo y regresión mixta de sensibilidad
- **Fecha:** 2026-11-21
- **Decisión:** evaluar H1 por modelo. Soporte fuerte: se cumple en ambos modelos. Soporte parcial: solo en uno, y se declara. El agregado se reporta con el modelo como efecto fijo. Análisis de sensibilidad con regresión logística mixta con efecto aleatorio de tarea.
- **Motivo:** evita que un solo modelo sostenga la conclusión.
- **Decidido por:** asistente, por delegación del usuario.
- **Estado:** APROBADA POR DELEGACIÓN.

### D-16 · Definición de la razón de H2
- **Fecha:** 2026-11-21
- **Decisión:** calcular los tokens totales de cada par tarea-condición (incluyendo razonamiento). Reportar la razón de medianas entre C y B, con IC95% por bootstrap sobre tareas y el IQR. No promediar razones tarea por tarea.
- **Motivo:** la razón de medianas es estable cuando B resuelve pocas tareas.
- **Decidido por:** asistente, por delegación del usuario.
- **Estado:** APROBADA POR DELEGACIÓN.

### D-19 · Control de tamaño en H3
- **Fecha:** 2026-11-21
- **Decisión:** igualar el total de shots por suite de pruebas entre condiciones. Si una suite tiene más pruebas, tiene menos shots por prueba, y viceversa.
- **Motivo:** más pruebas casi siempre detectan más mutantes. Sin este control, H3 mediría cantidad y no calidad de las aserciones.
- **Decidido por:** asistente, por delegación del usuario.
- **Estado:** APROBADA POR DELEGACIÓN.

---

## Pruebas, equivalencia y mutación

### D-11 · Held-out con entradas, shots, semillas, propiedades y referencia independiente
- **Fecha:** 2026-11-21
- **Motivo:** combina varias fuentes de error y evita depender de una sola referencia.
- **Estado:** APROBADA (opción C).

### D-12 · Mutantes separados por familias
- **Fecha:** 2026-11-21
- **Motivo:** el bucle de C y la medición de H3 no pueden usar los mismos mutantes, porque la métrica quedaría sesgada.
- **Familias del bucle:** cambiar compuerta y alterar ángulo.
- **Familias reservadas para H3:** eliminar compuerta, intercambiar qubits y añadir compuerta.
- **Estado:** APROBADA (opción A).

### D-22 · Equivalencia hasta 8 qubits
- **Fecha:** 2026-11-21
- **Motivo:** los métodos exactos escalan hasta cierto número de qubits (Wei et al., DAC 2022). Por encima de ese límite, solo se usan pruebas estadísticas.
- **Estado:** APROBADA (punto 5 del plan revisado).

### D-10 · Tolerancias de equivalencia
- **Fecha:** 2026-11-21
- **Motivo:** en el caso ideal, 1e-8 módulo fase global. Con ruido, umbral de fidelidad calibrado como percentil 1 de referencia contra referencia, con semillas distintas.
- **Estado:** APROBADA (opción A).

### D-08 · Ruido despolarizante con tasas fijas
- **Fecha:** 2026-11-21
- **Motivo:** modelo explícito y reproducible. Cumple el requisito de "con y sin modelo de ruido". Las tasas son de orden de magnitud típico de hardware actual, pero no se calibraron contra ningún dispositivo: el resultado es un escenario de sensibilidad, no una predicción.
- **Valores:** 0,001 por compuerta de 1 qubit y 0,01 por compuerta de 2 qubits.
- **Decidido por:** asistente, por delegación del usuario.
- **Estado:** APROBADA POR DELEGACIÓN.

---

## Idioma, formato y otros

### D-25 · Potencia insuficiente para el umbral de 10 puntos (hallazgo; resuelto con 50 tareas)
- **Fecha:** 2026-11-21
- **Hallazgo:** `analisis/potencia.md` (generado por `analisis/potencia.py`, semilla 20261121). Con 30 tareas y 4 repeticiones, la potencia para δ = 0,10 es de 0,34 a 0,46 según el baseline de B. Con 50 tareas es de 0,31 a 0,51. Para δ = 0,15 sube a 0,61–0,78 con 30 tareas y 0,62–0,88 con 50 tareas.
- **Causa:** el criterio de apoyo exige que la diferencia observada sea ≥ 0,10. Si el efecto real es exactamente 0,10, el resultado observado queda por debajo la mitad de las veces.
- **Decisión tomada:** el usuario eligió **50 tareas** (D-15). El umbral de 10 puntos se mantiene. Con 50 tareas, la potencia sigue siendo baja para efectos cercanos a 10 puntos (0,31–0,51), por lo que el artículo debe declarar que **H1 tiene potencia adecuada solo para efectos de unos 15 puntos o más**.
- **Opciones si se quiere más potencia:** (a) subir a 50 tareas (más coste); (b) mantener 30 tareas y reportar H1 como confirmatoria solo para efectos grandes (≥ 15 puntos); (c) fijar un umbral distinto. Requiere tu decisión.
- **Estado:** RESUELTO por la elección de 50 tareas (D-15). Las limitaciones de potencia se declaran en el artículo.

### D-26 · Piloto con 5 tareas adicionales
- **Fecha:** 2026-11-21
- **Decisión:** el piloto usa 5 tareas **fuera** del conjunto de 50. No entran en el análisis confirmatorio.
- **Motivo:** si el piloto usara tareas del conjunto de 50, las tareas se usarían para ajustar el presupuesto y luego para evaluar H1. Eso introduce un sesgo de selección. El costo es 5 tareas adicionales en el diseño del piloto.
- **Estado:** APROBADA por el usuario (2026-11-21).

### D-27 · Límite de contexto por llamada: menos de 100 000 tokens
- **Fecha:** 2026-11-21
- **Hallazgo:** el catálogo de OpenCode Go tiene dos tramos de precio para Haiku 5.5. Por encima de 100 000 tokens de contexto, el precio es cinco veces mayor (entrada 0,50 $/M, salida 2,50 $/M, lectura de caché 0,05 $/M). El registro de una solicitud de esta conversación (301 059 tokens de caché, 575 de salida) cuesta 0,0167 $ con ese tramo, que es exactamente lo que muestra el panel.
- **Decisión:** el arnés registra el contexto de cada llamada y **no envía llamadas por encima de 100 000 tokens**. Un episodio que lo supera se trunca y cuenta como no resuelto, igual que con el tope de D-02. Los prompts del experimento son del orden de 3 000 tokens, muy por debajo del límite.
- **Motivo:** mantener el precio de lista y que el coste sea predecible.
- **Coste estimado con precio base:** unos 3 $ para los 2800 llamadas de los dos modelos (ver la estimación anterior). Con el tramo alto, el mismo volumen costaría varias veces más.
- **Consecuencia para esta conversación:** cada turno nuevo relee todo el contexto. Por eso el coste sube con la longitud del chat. La Fase 6 debe ejecutarse desde el arnés, no desde esta conversación.
- **Estado:** APROBADA por el usuario (2026-11-21).

### D-28 · Variante `medium` explícita en el arnés
- **Fecha:** 2026-11-21
- **Hallazgo:** el registro de esta sesión indica `Reasoning: adaptive`. La variante `medium` no se aplica por defecto en la sesión interactiva.
- **Decisión:** el arnés envía la variante `medium` en cada llamada y la registra en cada episodio. No depende de la configuración por defecto.
- **Estado:** APROBADA por el usuario (2026-11-21).

### D-20 · Redacción en español
- **Fecha:** 2026-11-20
- **Motivo:** el usuario decidió escribir en español y traducir después.
- **Estado:** APROBADA.

### D-18 · Plantilla IEEE conference en español
- **Fecha:** 2026-11-21
- **Decisión:** `IEEEtran` en modo `conference`, con `\usepackage[spanish]{babel}`. La traducción al inglés, si se necesita para una venue, se hace después.
- **Motivo:** formato IEEE estándar para congresos; el idioma sigue la decisión D-20.
- **Decidido por:** asistente, por delegación del usuario.
- **Estado:** APROBADA POR DELEGACIÓN.

### D-23 · Alcance de fuentes: solo lo que se puede verificar
- **Fecha:** 2026-11-21
- **Motivo:** la Fase 0 solo afirma contenido de fuentes con texto completo. Las demás quedan como `[VERIFICAR]` (ver NOTAS.md).
- **Estado:** REGISTRO DE CAMBIO del plan original (que pedía usar las fuentes en su totalidad).

### D-24 · DOI manual en `aportes.json`
- **Fecha:** 2026-11-21
- **Motivo:** el conversor detectaba DOI de financiadores o artefactos (QuraTest y Quito). Ahora se puede fijar el DOI por archivo.
- **Estado:** REGISTRO DE CAMBIO técnico.

---

### D-29 · Enunciados de las tareas en inglés
- **Fecha:** 2026-11-21
- **Decisión:** los enunciados que se envían a los modelos están en inglés. El código y los identificadores también. El artículo sigue en español.
- **Motivo:** los modelos y las APIs de Qiskit están documentados en inglés; el idioma del prompt es una variable que conviene fijar en el preregistro.
- **Estado:** APROBADA por el usuario (2026-11-21).

### D-30 · Nivel α con una sola prueba por programa
- **Fecha:** 2026-11-21
- **Decisión:** α = 0,01 es el nivel por programa. Si un programa aplica n pruebas, cada una usa 0,01/n (Bonferroni). Las tareas de distribución aplican una sola chi-cuadrado, así que su α es 0,01.
- **Interpretación:** el preregistro dice "α = 0,01 por prueba con Bonferroni por programa". Se implementa como nivel familiar por programa dividido entre pruebas. Si se quiere otra lectura, se cambia aquí antes de congelar.
- **Estado:** APROBADA por el usuario (2026-11-21). Lectura: 0,01 es el nivel por programa; con una prueba por programa el valor efectivo es 0,01.

### D-31 · Limitaciones de las tareas de distribución
- **Fecha:** 2026-11-21
- **Hallazgo:** en las tareas de estado (preparación de Bell, GHZ, teleportación y codificación densa), el criterio de distribución compara solo la base computacional o la base X fijada en la referencia. Un error de fase que no cambie esas distribuciones no se detecta.
- **Consecuencia:** H1 y H3 se miden sobre lo que el criterio ve. Se declara en el artículo.
- **Estado:** REGISTRO DE LIMITACIÓN.

### D-32 · Transporte HTTP
- **Fecha:** 2026-11-21
- **Verificado en la documentación (no en una llamada):** base `https://opencode.ai/inference/go`. Catálogo `https://opencode.ai/inference/go/v1/models` y página de Go. GPT-6 Luna: API Responses en `/openai/v1/responses`, con `reasoning.effort` (valores incluyen `medium`). Claude Haiku 5.5: API Messages en `/anthropic/v1/messages`, con `thinking: {type: adaptive}` y `output_config.effort`. Haiku 5.5 no admite `temperature`. Ver también la guía de Anthropic: los modelos 4.7 o posteriores rechazan `budget_tokens`.
- **Cabeceras requeridas por OpenCode Go:** User-Agent propio (`articulo-arnes/0.1`) y `x-opencode-session` estable por conversación. Implementado en `arnes/transporte.py`.
- **Comprobación real (2026-11-21):** Haiku 5.5 responde OK con `x-api-key`, variante `medium` y sin `temperature`. GPT-6 Luna devolvió HTTP 400 (`temperature` no soportado); se quitó de la petición y se registra como parámetro ignorado. **Pendiente:** repetir `python -m arnes.comprobar` para confirmar GPT-6 Luna sin temperatura.
- **Claves:** solo variable de entorno `OPENCODE_GO_API_KEY`. No está definida en este entorno; la comprobación falla con mensaje claro si falta.
- **Estado:** IMPLEMENTADO Y PROBADO CON TRANSPORTE SIMULADO. Pendiente de comprobación real.

### D-33 · Retención de datos de los proveedores (limitación)
- **Fecha:** 2026-11-21
- **Hallazgo (documentación de OpenCode Go, Privacy):** GPT-6 Luna y Claude Haiku 5.5 retienen las peticiones 30 días para monitoreo de abuso. Las tareas son originales y no contienen datos personales, pero el artículo debe declararlo.
- **Acción del usuario:** comprobar en Settings › Privacy del workspace que el ajuste por defecto (sin endpoints que entrenen con los datos) sigue activo.
- **Estado:** REGISTRO DE LIMITACIÓN.

### D-34 · Piloto: estado
- **Fecha:** 2026-11-21
- **Hecho:** 5 tareas fuera del catálogo (`tareas/piloto.py`, P1 a P5, con pruebas unitarias). Ejecutor (`arnes/piloto.py`) con control de coste de 6 USD (precio de lista, tramos base y alto de cada modelo) y registro por llamada.
- **Bloqueado:** no se ha ejecutado. Falta la clave `OPENCODE_GO_API_KEY` en el entorno.
- **Decisión tomada por delegación del usuario:** el piloto se ejecutará en cuanto la comprobación de D-32 funcione, dentro del control de 6 USD.
- **Estado:** BLOQUEADO por la clave.

### D-35 · Resultado del piloto y tope de tokens
- **Fecha:** 2026-11-21
- **Ejecución:** `arnes/piloto.py` completo: 120 episodios, 120 llamadas, coste 0,0176 USD a precio de lista. No se detuvo por control. Datos en `resultados/piloto/`.
- **Tope de tokens (D-02):** tokens por llamada: mediana 322, q95 702, máximo 911. **T = 5 × q95 → 4 000 tokens por episodio.** Con T = 4 000 no se trunca ningún episodio del piloto (`analisis/fijar_tope.py`, `resultados/piloto/tope.md`).
- **Limitación 1 (grave):** todos los episodios se resolvieron en la primera llamada. El piloto no ejercita reintentos ni el crecimiento del prompt con retroalimentación. El q95 mide solo primeras llamadas. Con prompts que incluyen código previo, las llamadas posteriores serán más largas. **Riesgo:** T puede quedarse corto en tareas difíciles.
- **Limitación 2 (razonamiento):** GPT-6 Luna produce razonamiento en todas las llamadas. Haiku 5.5 lo produce en 5 o 6 de 20 llamadas por condición: `adaptive` decide cuándo pensar. Esto afecta a H2 (tokens incluyendo razonamiento) y debe declararse.
- **Estimación de presupuesto (D-02):** la referencia de 3 USD asumía 3 000 tokens de entrada y 1 500 de salida por llamada. El piloto mide 322 tokens por llamada en tareas fáciles. Es una cota superior, pero las tareas reales tendrán más tokens e iteraciones.
- **Decisión pendiente del usuario:** aceptar T = 4 000 tal como dice la regla, o fijarlo más alto por la limitación 1. Propuesta del asistente: aceptar la regla y registrar el riesgo, porque cambiarla después de ver los datos sería un ajuste a posteriori.
- **Estado:** RESULTADO REGISTRADO. Pendiente de la decisión sobre T.

## Pendientes para congelar `prereg-v1`

| ID | Punto | Quién |
|---|---|---|
| D-02 | Presupuesto y tope de tokens | usuario (cuota) + piloto |
| D-13 | Instalación real de Qiskit 2.x y Aer en el entorno (Fase 2) | asistente |
