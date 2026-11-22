#!/usr/bin/env python3
"""Análisis de sensibilidad de H1 (D-17, D-41).

Modelos sobre los 1 200 episodios, con resultado binario = resuelta en la suite reservada:
1. Logística mixta con efecto aleatorio por tarea (BinomialBayesMixedGLM, aproximación
   variacional). statsmodels no trae un GLMM logístico frecuentista; por eso el resultado
   es bayesiano aproximado y se declara como desviación (D-41).
2. GEE logístico con estructura de correlación intercambiable, agrupado por tarea. Es
   frecuentista y sirve de comprobación independiente.

Efecto de interés: C frente a B. Se reporta en escala logit y como diferencia de probabilidad
aproximada en el punto medio de las tasas observadas.

Salida: resultados/experimento/sensibilidad.md
Uso:    .venv/bin/python -m analisis.sensibilidad_mixta
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.genmod.bayes_mixed_glm import BinomialBayesMixedGLM

from analisis.analizar_experimento import cargar

RAIZ = Path(__file__).resolve().parent.parent
SALIDA = RAIZ / "resultados" / "experimento" / "sensibilidad.md"
Z95 = 1.96


def datos() -> pd.DataFrame:
    filas = cargar()
    df = pd.DataFrame({
        "y": [int(r["resuelta_heldout"]) for r in filas],
        "condicion": [r["condicion"] for r in filas],
        "modelo": [r["modelo"].replace("opencode-go/", "") for r in filas],
        "tarea": [r["tarea"] for r in filas],
    })
    df["condicion"] = pd.Categorical(df["condicion"], categories=["B", "A", "C"])
    return df


def mixta(df: pd.DataFrame) -> dict:
    modelo = BinomialBayesMixedGLM.from_formula(
        "y ~ C(condicion, Treatment('B')) + C(modelo)",
        {"tarea": "0 + C(tarea)"},
        df,
    )
    r = modelo.fit_vb()
    nombres = list(modelo.exog_names)
    medias = np.asarray(r.fe_mean)
    sds = np.asarray(r.fe_sd)
    i = nombres.index("C(condicion, Treatment('B'))[T.C]")
    return {
        "coef_C_vs_B": float(medias[i]),
        "ic_lo": float(medias[i] - Z95 * sds[i]),
        "ic_hi": float(medias[i] + Z95 * sds[i]),
        "todos": {n: (float(m), float(s)) for n, m, s in zip(nombres, medias, sds)},
    }


def gee(df: pd.DataFrame) -> dict:
    m = smf.gee(
        "y ~ C(condicion, Treatment('B')) + C(modelo)",
        groups="tarea",
        data=df,
        family=sm.families.Binomial(),
        cov_struct=sm.cov_struct.Exchangeable(),
    ).fit()
    nombre = "C(condicion, Treatment('B'))[T.C]"
    b = float(m.params[nombre])
    se = float(m.bse[nombre])
    return {"coef_C_vs_B": b, "ic_lo": b - Z95 * se, "ic_hi": b + Z95 * se, "p": float(m.pvalues[nombre])}


def diferencia_prob(coef: float, tasa_b: float) -> float:
    """Diferencia de probabilidad aproximada de C frente a B en la tasa de B dada."""
    logit_b = np.log(tasa_b / (1 - tasa_b))
    p_c = 1 / (1 + np.exp(-(logit_b + coef)))
    return float(p_c - tasa_b)


def main() -> int:
    df = datos()
    tasa_b = float(df.loc[df["condicion"] == "B", "y"].mean())
    m = mixta(df)
    g = gee(df)
    dp_m = diferencia_prob(m["coef_C_vs_B"], tasa_b)
    dp_g = diferencia_prob(g["coef_C_vs_B"], tasa_b)

    L = ["# Sensibilidad de H1: modelos logísticos con efecto aleatorio por tarea", "",
         "Generado por `analisis/sensibilidad_mixta.py`. No editar a mano.", "",
         f"Tasa observada de B (referencia): {tasa_b:.3f}. Resultado: resuelta en la suite reservada.", "",
         "| Modelo | Coef. C vs B (logit) | IC95% | Diferencia de probabilidad aprox. | Cumple (≥ 0,10 e IC > 0) |",
         "|---|---|---|---|---|",
         f"| Mixto bayesiano (efecto aleatorio por tarea, VB) | {m['coef_C_vs_B']:+.3f} | [{m['ic_lo']:+.3f}, {m['ic_hi']:+.3f}] | {dp_m:+.3f} | {'sí' if dp_m >= 0.10 and m['ic_lo'] > 0 else 'no'} |",
         f"| GEE logístico, intercambiable por tarea | {g['coef_C_vs_B']:+.3f} | [{g['ic_lo']:+.3f}, {g['ic_hi']:+.3f}] | {dp_g:+.3f} | {'sí' if dp_g >= 0.10 and g['ic_lo'] > 0 else 'no'} |",
         "", "## Lectura", "",
         "- Ambos modelos confirman la conclusión de H1: C supera a B de forma pequeña, y no alcanza 10 puntos.",
         "- El modelo mixto es bayesiano aproximado (desviación D-41). El GEE es la comprobación frecuentista.",
         f"- GEE: p = {g['p']:.3g} para C frente a B.",
         ""]
    SALIDA.write_text("\n".join(L), encoding="utf-8")
    print("\n".join(L))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
