# Análisis confirmatorio (experimento)

Generado por `analisis/analizar_experimento.py`. No editar a mano.

- Episodios: 1200. Coste a precio de lista: 1.1766 USD.
- Bootstrap: 10000 remuestreos sobre tareas, semilla 20261121.

## H1 (corrección): C − B

| Comparación | Diferencia media | IC95% | p (Holm) |
|---|---|---|---|
| **C − B** (primaria, agregada) | +0.037 | [+0.013, +0.068] | — |
| C − A (secundaria) | +0.048 | [+0.018, +0.080] | 0.002 |
| B − A (secundaria) | +0.010 | [-0.018, +0.037] | 0.544 |

**Criterio de H1 (≥ +0.10 y límite inferior > 0):** NO SE CUMPLE. Soporte por modelo: **no apoyada**.

## Tasas pass@1 por modelo y condición

| Modelo | A | B | C | C − B | IC95% | Cumple H1 |
|---|---|---|---|---|---|---|
| opencode-go/claude-haiku-5-5 | 0.945 | 0.965 | 0.990 | +0.025 | [+0.000, +0.055] | no |
| opencode-go/gpt-6-luna | 0.940 | 0.940 | 0.990 | +0.050 | [+0.005, +0.105] | no |

## H2 (costo): razón de medianas de tokens C / B

| Modelo | Razón | IC95% | Cumple H2 (≤ 2) |
|---|---|---|---|
| opencode-go/claude-haiku-5-5 | 1.017 | [0.888, 1.206] | sí |
| opencode-go/gpt-6-luna | 1.088 | [0.766, 1.373] | sí |
| agregado | 1.040 | [0.911, 1.369] | sí |

## Truncados (tope de 20 000 tokens, D-36)

| Modelo | Condición | Truncados |
|---|---|---|
| opencode-go/claude-haiku-5-5 | A | 0 |
| opencode-go/claude-haiku-5-5 | B | 0 |
| opencode-go/claude-haiku-5-5 | C | 2 |
| opencode-go/gpt-6-luna | A | 0 |
| opencode-go/gpt-6-luna | B | 0 |
| opencode-go/gpt-6-luna | C | 2 |

## H3 (detección de mutantes, D-39)

- Puntuación de la suite de C: 0.696. Línea base de B: 0.000.
- Diferencia C − B: +0.696 [IC95% +0.583, +0.802].
- Mutantes: 730 generados; 64 equivalentes excluidos; 18 indeterminados incluidos; 666 evaluados.
- **H3: SE CUMPLE** (lectura: fuerza de la suite, no efecto sobre los modelos; ver D-40).

## Métricas complementarias (PREREGISTRO §7)

### pass@1, pass@2 y pass@4 (n = 4 repeticiones por tarea)

| Modelo | Condición | pass@1 | pass@2 | pass@4 |
|---|---|---|---|---|
| agregado | A | 0.943 [0.907, 0.973] | 0.989 [0.978, 0.996] | 1.000 [0.999, 1.000] |
| agregado | B | 0.953 [0.922, 0.978] | 0.993 [0.983, 0.999] | 1.000 [0.999, 1.000] |
| agregado | C | 0.990 [0.978, 1.000] | 0.999 [0.998, 1.000] | 1.000 [1.000, 1.000] |
| opencode-go/claude-haiku-5-5 | A | 0.945 [0.900, 0.980] | 0.987 [0.973, 0.997] | 1.000 [1.000, 1.000] |
| opencode-go/claude-haiku-5-5 | B | 0.965 [0.935, 0.990] | 0.997 [0.990, 1.000] | 1.000 [1.000, 1.000] |
| opencode-go/claude-haiku-5-5 | C | 0.990 [0.975, 1.000] | 1.000 [1.000, 1.000] | 1.000 [1.000, 1.000] |
| opencode-go/gpt-6-luna | A | 0.940 [0.890, 0.980] | 0.980 [0.953, 0.997] | 1.000 [1.000, 1.000] |
| opencode-go/gpt-6-luna | B | 0.940 [0.885, 0.980] | 0.973 [0.930, 1.000] | 0.980 [0.940, 1.000] |
| opencode-go/gpt-6-luna | C | 0.990 [0.975, 1.000] | 1.000 [1.000, 1.000] | 1.000 [1.000, 1.000] |

Por modelo, n = 4 por tarea. La fila *agregado* usa n = 8 por tarea (ambos modelos).

### Iteraciones por episodio

| Modelo | Condición | Media | Máximo | Episodios con reintento | Llamadas |
|---|---|---|---|---|---|
| opencode-go/claude-haiku-5-5 | A | 1.000 | 1 | 0 de 200 | 200 |
| opencode-go/claude-haiku-5-5 | B | 1.000 | 1 | 0 de 200 | 200 |
| opencode-go/claude-haiku-5-5 | C | 1.080 | 5 | 10 de 200 | 216 |
| opencode-go/gpt-6-luna | A | 1.000 | 1 | 0 de 200 | 200 |
| opencode-go/gpt-6-luna | B | 1.000 | 1 | 0 de 200 | 200 |
| opencode-go/gpt-6-luna | C | 1.070 | 5 | 8 de 200 | 214 |

Llamadas en `llamadas.jsonl`: 1230. Coinciden con la suma de iteraciones: sí.

### Tokens por episodio (suma de todas las llamadas del episodio, ambos modelos)

| Condición | Entrada (mediana) | Salida (mediana) | Razonamiento (mediana) | Total (mediana) | Total (media) |
|---|---|---|---|---|---|
| A | 134 | 808 | 516 | 1496 | 1992 |
| B | 134 | 864 | 516 | 1545 | 1917 |
| C | 137 | 897 | 543 | 1622 | 2338 |

### Costo por solución correcta

| Condición | Coste total (USD) | Resueltas | USD por resuelta |
|---|---|---|---|
| A | 0.3757 | 377 | 0.00100 |
| B | 0.3609 | 381 | 0.00095 |
| C | 0.4401 | 396 | 0.00111 |

## Cumplimiento del preregistro

| Elemento (PREREGISTRO) | Estado | Nota |
|---|---|---|
| H1 primaria y secundarias con Holm (§2, §6) | Ejecutado | Ver arriba. |
| Sensibilidad con regresión mixta y GEE (D-17) | Ejecutado | Ver `sensibilidad.md`; el mixto es bayesiano aproximado (D-41). |
| H2 con desglose de tokens y costo por resuelta (§7) | Ejecutado | Ver arriba. |
| H3 con equivalentes reportados (§7, §9) | Ejecutado | Ver `h3.md` (D-39). |
| pass@2 y pass@4 (§7) | Ejecutado | Ver arriba. |
| Iteraciones y tokens por episodio (§7) | Ejecutado | Ver arriba. |
| Potencia de H1 (§6) | Ejecutado | `analisis/potencia.md`. |
| Truncados por condición y modelo (§5, D-36) | Ejecutado | Ver tabla de truncados. |
| Tiempos por llamada y episodio (§7) | **No ejecutado** | `llamadas.jsonl` solo guarda la hora de inicio; no hay latencia. |
| Comprobaciones estáticas y aserciones dinámicas en el bucle de C (§3, §8) | **No implementado** | El bucle de C usa solo equivalencia de unitarias y chi-cuadrado. |
| Propiedades metamórficas en la suite reservada (§8) | **No implementado** | `arnes/heldout.py` solo usa referencia independiente. |
| Equivalencia parcial con auxiliares (§9) | **No encontrado** | Sin implementación en `arnes/verificacion.py`. Revisar antes de citarla. |
| Régimen con ruido despolarizante (§10) | **No ejecutado** | No hay código de ruido ni calibración del umbral (§9). |
| Reintentos de B (§3, §11) | **Hallazgo** | B nunca reintentó: 0 de 400 episodios con más de 1 iteración. |
| Presupuesto igualado B-tok (§3) | Excluido | D-06: la conclusión se limita a 'C supera a B'. |
