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

## H3 (detección de mutantes)

**No calculado en este informe.** Requiere evaluar mutantes sobre el código final de cada episodio. Pendiente.
