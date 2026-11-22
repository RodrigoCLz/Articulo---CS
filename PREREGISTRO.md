# PREREGISTRO

**Título:** Verification Feedback for LLM Agents Generating Quantum Circuits: A Pre-registered Study with Negative Results on Effect Size (D-42; sustituye al título tentativo anterior).

**Estado:** BORRADOR. No congelado. No ejecutar ningún experimento antes de congelar.

**Fecha del borrador:** 2026-11-21

**Congelación:** se hará con `git tag prereg-v1` sobre el commit que contenga este archivo y DECISIONES.md, una vez resueltos los puntos marcados como PENDIENTE.

Cada cambio posterior se registra en DECISIONES.md con fecha y motivo.

---

## 1. Pregunta de investigación

¿Un agente LLM que verifica su propio código cuántico (aserciones dinámicas, pruebas estadísticas y equivalencia con una referencia) genera programas más correctos que uno que solo recibe retroalimentación de ejecución?

## 2. Hipótesis y criterios de decisión

Los umbrales son fijos y se evalúan con los datos del experimento completo.

**H1 (corrección).** Comparación primaria: **C frente a B**.
- Criterio de apoyo: diferencia de pass@1 ≥ **10 puntos porcentuales** y límite inferior del IC95% > 0.
- IC95% por bootstrap pareado sobre **tareas** (ver §6).
- Comparaciones secundarias: **C frente a A** y **B frente a A**, con corrección de Holm.

**H2 (costo).** Mediana de tokens por tarea de C ≤ **2 veces** la de B, incluyendo tokens de razonamiento.
- Se reporta el desglose por tipo de token y el costo por solución correcta.
- Razón de medianas entre C y B, con IC95% por bootstrap sobre tareas (D-16).

**H3 (detección de mutantes).** Diferencia de mutation score ≥ **10 puntos porcentuales** (solo mutantes no equivalentes), con límite inferior del IC95% > 0.
- Si el baseline de solo ejecución supera el **90%**, H3 se declara **no evaluable** por efecto techo.

**Soporte de H1 por modelo (D-17).** Soporte fuerte: se cumple el criterio en ambos modelos. Soporte parcial: solo en uno, y se declara. El agregado se reporta como descriptivo.

## 3. Condiciones experimentales

| Condición | Descripción |
|---|---|
| **A** | Una sola pasada. |
| **B** | Reintentos con retroalimentación de errores de ejecución. Termina cuando pasa sus propias comprobaciones de ejecución. |
| **C** | Reintentos con verificación en el bucle: comprobaciones estáticas, aserciones dinámicas, prueba estadística de distribución y equivalencia con la referencia (cuando aplique). La retroalimentación indica qué comprobación falló. Termina cuando pasa sus pruebas del bucle. |

Las tres condiciones usan el mismo prompt base, el mismo modelo, la misma variante y el mismo presupuesto máximo de iteraciones.

**Control de presupuesto igualado (B-tok):** no se incluye en este diseño (ver DECISIONES.md, D-06). La conclusión de H1 se limita a "C supera a B", no a "la verificación explica la mejora".

## 4. Tareas y benchmark

- **50 tareas propias**, no publicadas (D-15).
- Organización: **10 categorías × 5 tareas**. Categorías: Bell/GHZ, Deutsch-Jozsa, Bernstein-Vazirani, Grover, QFT, teleportación, superdense coding, estimación de fase (QPE), un algoritmo variacional y QAOA.
- Por categoría: **2 pequeñas, 2 medianas y 1 grande**, dentro del límite de 8 qubits para equivalencia.
- Cada tarea incluye: enunciado en lenguaje natural, solución de referencia, criterio de corrección, conjunto de pruebas del bucle y conjunto de pruebas reservadas.
- **No se usa Qiskit HumanEval como held-out** (D-05). Motivo: posible contaminación de entrenamiento (Chang et al., preprint).

## 5. Modelos y configuración

| Parámetro | Valor |
|---|---|
| Modelos | `opencode-go/gpt-6-luna` y `opencode-go/claude-haiku-5-5` |
| Variante de razonamiento | `medium` en ambos (D-01) |
| Repeticiones por tarea y condición | **4** (D-04) |
| Temperatura | Fija donde el modelo la acepte; los parámetros ignorados se registran (D-07) |
| Iteraciones máximas por episodio | **5** en B y en C (D-14b) |
| Tope de tokens por episodio | **T = 20 000 tokens por episodio** (desviación de la regla original, registrada en D-02 y D-36). Un episodio que supera T se trunca y cuenta como no resuelto; se reporta el número de truncados por condición y modelo. |
| Presupuesto total | **Referencia: ~3 USD a precio de lista** para ~2 800 llamadas (D-02). Si el piloto implica más del doble (~6 USD), la ejecución se detiene y se reporta. El límite de cuota del usuario es desconocido. |
| Tamaño del experimento | 50 tareas × 3 condiciones × 4 repeticiones × 2 modelos = 1200 episodios *(sin contar piloto ni reintentos)* |

## 6. Unidad de análisis y plan estadístico

- **Unidad de análisis: la tarea.** Las repeticiones no se tratan como observaciones independientes.
- Tasas por tarea con comparación pareada sobre las mismas tareas.
- IC95% por **bootstrap sobre tareas** (pareado).
- Análisis de sensibilidad: regresión logística mixta con efecto aleatorio de tarea (D-17).
- **Simulación de potencia** antes de ejecutar, con supuestos explícitos: baseline de B entre 40% y 70%. Generada por `analisis/potencia.py` y guardada en `analisis/potencia.md`. **Resultado con 50 tareas y 4 repeticiones (D-25):** potencia de 0,31–0,51 para δ = 0,10 y de 0,62–0,88 para δ = 0,15. H1 tiene potencia adecuada solo para efectos de unos 15 puntos o más; un resultado no significativo con efecto cercano a 10 puntos no permite afirmar ausencia de efecto.
- Corrección de Holm solo sobre las dos comparaciones secundarias de H1.
- **H3:** igual total de shots por suite de pruebas en ambas condiciones (D-19).
- α = 0,05 para los IC95%.

## 7. Métricas

- **Corrección funcional:** pass@1 por tarea, con el estimador insesgado de Chen et al. (2021), ecuación (1). Pass@2 y pass@4 como secundarias.
- **Iteraciones y tokens:** por episodio, separando tokens de entrada, salida y razonamiento.
- **Costo:** tokens y costo por solución correcta.
- **Mutation score:** solo mutantes no equivalentes. Los mutantes equivalentes se clasifican como equivalentes, no equivalentes o indeterminados, y se reporta cuántos quedan en cada grupo.
- **Tiempos:** por llamada y por episodio.

## 8. Verificación y pruebas

**Pruebas del bucle (usadas por C dentro del bucle):**
- Comprobaciones estáticas (imports, APIs vigentes en la versión fijada).
- Aserciones dinámicas.
- Prueba estadística de distribución de salida con chi-cuadrado.
- Equivalencia con la referencia, cuando aplique (§9).

**Pruebas reservadas (held-out, nunca visibles para ninguna condición):**
- Entradas no vistas, shots distintos y semillas distintas.
- Propiedades metamórficas.
- Referencia independiente cuando exista.

**Separación:** las pruebas del bucle y las reservadas no comparten entradas, shots ni semillas. Ninguna condición recibe la solución de referencia ni los resultados esperados completos. Se documenta qué ve cada condición en cada iteración.

## 9. Equivalencia y mutación

- **Equivalencia de unitarias:** hasta **8 qubits**, con tolerancia numérica **1e-8** en la norma de la diferencia, módulo fase global. Solo en tareas cuya especificación define una unitaria o un estado final.
- **Circuitos con auxiliares:** equivalencia parcial.
- **Resto de tareas:** pruebas estadísticas sobre la distribución de salida.
- **Con ruido:** umbral de fidelidad calibrado como el percentil 1 de referencia frente a referencia, usando semillas distintas de las de la evaluación. Conjunto de calibración separado.
- **Operadores de mutación:**
  - Familias del bucle de C: cambiar compuerta y alterar ángulo.
  - Familias reservadas para H3: eliminar compuerta, intercambiar qubits y añadir compuerta.
- Las dos familias no se mezclan en ninguna prueba.

## 10. Simulador y ruido

- Simulador: Qiskit Aer 0.18.x con Qiskit 2.x, fijados en el lockfile (D-13).
- Dos regímenes: **ideal** y **con ruido despolarizante** de tasas fijas: 0,001 por compuerta de 1 qubit y 0,01 por compuerta de 2 qubits (D-08). Son un escenario de sensibilidad, no una calibración contra hardware.
- Semillas del simulador: lista fija, registrada en el archivo de configuración.
- Shots por prueba estadística: **8192**.
- Nivel α por prueba: **0,01**, con corrección de Bonferroni por programa.

## 11. Parada temprana

- B termina cuando pasa sus propias comprobaciones de ejecución.
- C termina cuando pasa sus pruebas del bucle.
- Ninguna condición termina por las pruebas reservadas.

## 12. Registro y reproducibilidad

Cada ejecución registra:

- Identificador del modelo, variante y fecha de la llamada.
- Prompt completo, respuesta completa y tokens por tipo.
- Shots, α, tolerancia y umbral de cada prueba estadística.
- Semillas del simulador.
- Versiones de Python, Qiskit y Aer.
- Hash del commit del arnés.

Los resultados se guardan en CSV. Todas las cifras del artículo se regeneran con un script desde esos CSV.

## 13. Piloto (Fase 5)

- 5 tareas **adicionales** al conjunto de 50, con `medium` en ambos modelos (D-26). No entran en el análisis confirmatorio.
- Con los datos del piloto se fijan el tope de tokens por episodio (regla de §5) y el coste total estimado de la Fase 6.
- Objetivo: medir costo real por llamada, errores del arnés y problemas de diseño.
- Requiere aprobación del usuario antes de la ejecución completa.
- Tras el piloto se fija el tope de tokens y el presupuesto (D-02) y se confirma el número de repeticiones (D-04, regla: 4 fijas).

---

## Puntos PENDIENTES antes de congelar

1. Tope de tokens fijado en T = 20 000 (D-36, desviación de D-02). Pendiente solo de la aprobación de congelación.
2. Presupuesto para 1200 episodios: el coste sube respecto a 720 episodios (D-02 y D-25).
3. Instalación real de Qiskit 2.x y Aer en el entorno (D-13). Verificada solo en metadatos.

Resueltos en esta ronda por delegación del usuario: iteraciones (D-14b), tasas de ruido (D-08), razón de H2 (D-16), análisis por modelo (D-17), control de shots en H3 (D-19), plantilla IEEE (D-18) y plan de potencia (`analisis/potencia.md`).
