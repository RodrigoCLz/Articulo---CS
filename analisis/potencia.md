# Potencia de H1 (simulación)

Generado por `analisis/potencia.py`. No editar a mano.

- Semilla: 20261121. Simulaciones por celda: 1000. Remuestreos bootstrap: 1000.
- Criterio: diferencia media ≥ 0.10 y límite inferior del IC95% > 0.
- Heterogeneidad entre tareas: Beta con concentración 2.0.
- Efecto: `p_C = p_B + δ` por tarea (truncado a [0, 1]).

## Potencia por celda

| Tareas | Repeticiones | Baseline B | δ real | Potencia |
|---|---|---|---|---|
| 30 | 3 | 0.40 | +0.00 | 0.03 |
| 30 | 3 | 0.40 | +0.05 | 0.14 |
| 30 | 3 | 0.40 | +0.10 | 0.38 |
| 30 | 3 | 0.40 | +0.15 | 0.68 |
| 30 | 3 | 0.40 | +0.20 | 0.87 |
| 30 | 3 | 0.55 | +0.00 | 0.03 |
| 30 | 3 | 0.55 | +0.05 | 0.12 |
| 30 | 3 | 0.55 | +0.10 | 0.38 |
| 30 | 3 | 0.55 | +0.15 | 0.66 |
| 30 | 3 | 0.55 | +0.20 | 0.85 |
| 30 | 3 | 0.70 | +0.00 | 0.02 |
| 30 | 3 | 0.70 | +0.05 | 0.12 |
| 30 | 3 | 0.70 | +0.10 | 0.34 |
| 30 | 3 | 0.70 | +0.15 | 0.57 |
| 30 | 3 | 0.70 | +0.20 | 0.78 |
| 30 | 4 | 0.40 | +0.00 | 0.02 |
| 30 | 4 | 0.40 | +0.05 | 0.13 |
| 30 | 4 | 0.40 | +0.10 | 0.46 |
| 30 | 4 | 0.40 | +0.15 | 0.78 |
| 30 | 4 | 0.40 | +0.20 | 0.93 |
| 30 | 4 | 0.55 | +0.00 | 0.03 |
| 30 | 4 | 0.55 | +0.05 | 0.13 |
| 30 | 4 | 0.55 | +0.10 | 0.38 |
| 30 | 4 | 0.55 | +0.15 | 0.71 |
| 30 | 4 | 0.55 | +0.20 | 0.92 |
| 30 | 4 | 0.70 | +0.00 | 0.02 |
| 30 | 4 | 0.70 | +0.05 | 0.12 |
| 30 | 4 | 0.70 | +0.10 | 0.34 |
| 30 | 4 | 0.70 | +0.15 | 0.61 |
| 30 | 4 | 0.70 | +0.20 | 0.85 |
| 50 | 3 | 0.40 | +0.00 | 0.01 |
| 50 | 3 | 0.40 | +0.05 | 0.14 |
| 50 | 3 | 0.40 | +0.10 | 0.49 |
| 50 | 3 | 0.40 | +0.15 | 0.81 |
| 50 | 3 | 0.40 | +0.20 | 0.97 |
| 50 | 3 | 0.55 | +0.00 | 0.01 |
| 50 | 3 | 0.55 | +0.05 | 0.14 |
| 50 | 3 | 0.55 | +0.10 | 0.45 |
| 50 | 3 | 0.55 | +0.15 | 0.80 |
| 50 | 3 | 0.55 | +0.20 | 0.95 |
| 50 | 3 | 0.70 | +0.00 | 0.02 |
| 50 | 3 | 0.70 | +0.05 | 0.10 |
| 50 | 3 | 0.70 | +0.10 | 0.36 |
| 50 | 3 | 0.70 | +0.15 | 0.62 |
| 50 | 3 | 0.70 | +0.20 | 0.83 |
| 50 | 4 | 0.40 | +0.00 | 0.00 |
| 50 | 4 | 0.40 | +0.05 | 0.12 |
| 50 | 4 | 0.40 | +0.10 | 0.51 |
| 50 | 4 | 0.40 | +0.15 | 0.88 |
| 50 | 4 | 0.40 | +0.20 | 0.99 |
| 50 | 4 | 0.55 | +0.00 | 0.01 |
| 50 | 4 | 0.55 | +0.05 | 0.09 |
| 50 | 4 | 0.55 | +0.10 | 0.45 |
| 50 | 4 | 0.55 | +0.15 | 0.84 |
| 50 | 4 | 0.55 | +0.20 | 0.97 |
| 50 | 4 | 0.70 | +0.00 | 0.01 |
| 50 | 4 | 0.70 | +0.05 | 0.08 |
| 50 | 4 | 0.70 | +0.10 | 0.31 |
| 50 | 4 | 0.70 | +0.15 | 0.64 |
| 50 | 4 | 0.70 | +0.20 | 0.90 |

## Efecto mínimo detectable con potencia ≥ 0,80

| Tareas | Repeticiones | Baseline B | δ mínimo (potencia ≥ 0,80) |
|---|---|---|---|
| 30 | 3 | 0.40 | +0.20 |
| 30 | 3 | 0.55 | +0.20 |
| 30 | 3 | 0.70 | > 0,20 |
| 30 | 4 | 0.40 | +0.20 |
| 30 | 4 | 0.55 | +0.20 |
| 30 | 4 | 0.70 | +0.20 |
| 50 | 3 | 0.40 | +0.15 |
| 50 | 3 | 0.55 | +0.20 |
| 50 | 3 | 0.70 | +0.20 |
| 50 | 4 | 0.40 | +0.15 |
| 50 | 4 | 0.55 | +0.15 |
| 50 | 4 | 0.70 | +0.20 |

## Lectura para el preregistro

- Con **4 repeticiones y 30 tareas**, la potencia para δ = 0,10 queda entre 0,34 y 0,46. Con 50 tareas el rango es 0,31–0,51, prácticamente igual: no mejora de forma clara. Para δ = 0,15, 30 tareas dan 0,61–0,78 y 50 tareas dan 0,62–0,88.
- La causa es que el criterio exige una diferencia observada ≥ 0,10: si el efecto real es 0,10, el resultado queda por debajo la mitad de las veces. Aumentar tareas no resuelve esto por sí solo.
- Conclusión operativa: H1 solo tiene potencia adecuada para efectos de unos 15 puntos o más. Un resultado no significativo con efecto cercano a 10 puntos no permite afirmar ausencia de efecto.
- Los resultados dependen de los supuestos (heterogeneidad y forma del efecto). Se declaran como supuestos, no como hechos.
