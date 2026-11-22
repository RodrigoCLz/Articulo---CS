# Sensibilidad de H1: modelos logísticos con efecto aleatorio por tarea

Generado por `analisis/sensibilidad_mixta.py`. No editar a mano.

Tasa observada de B (referencia): 0.953. Resultado: resuelta en la suite reservada.

| Modelo | Coef. C vs B (logit) | IC95% | Diferencia de probabilidad aprox. | Cumple (≥ 0,10 e IC > 0) |
|---|---|---|---|---|
| Mixto bayesiano (efecto aleatorio por tarea, VB) | +1.848 | [+0.881, +2.814] | +0.040 | no |
| GEE logístico, intercambiable por tarea | +1.599 | [+0.327, +2.871] | +0.038 | no |

## Lectura

- Ambos modelos confirman la conclusión de H1: C supera a B de forma pequeña, y no alcanza 10 puntos.
- El modelo mixto es bayesiano aproximado (desviación D-41). El GEE es la comprobación frecuentista.
- GEE: p = 0.0138 para C frente a B.
