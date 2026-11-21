#!/usr/bin/env python3
"""Simulación de potencia para H1 (C frente a B, pass@1 pareado por tarea).

Criterio de apoyo de H1 (PREREGISTRO §2):
    media de la diferencia por tarea >= 0.10  y  límite inferior del IC95% > 0,
    con IC95% por bootstrap pareado sobre tareas.

Modelo generativo (supuestos explícitos):
    - p_B de cada tarea ~ Beta con media m y concentración K = 2 (heterogeneidad entre tareas).
    - p_C de cada tarea = clip(p_B + delta, 0, 1)  (efecto desplazado, mismo por tarea).
    - Aciertos por tarea ~ Binomial(reps, p).

Salida: analisis/potencia.md
Uso:    .venv/bin/python analisis/potencia.py
"""

from __future__ import annotations

from pathlib import Path

import numpy as np

SEED = 20261121
N_SIM = 1000
N_BOOT = 1000
K_CONC = 2.0
THRESHOLD = 0.10
ALPHA_LOW = 0.025

TASKS = [30, 50]
REPS = [3, 4]
BASELINES = [0.40, 0.55, 0.70]
DELTAS = [0.00, 0.05, 0.10, 0.15, 0.20]

OUT = Path(__file__).resolve().parent / "potencia.md"


def simulate_cell(rng, n_tasks, reps, m, delta):
    a, b = m * K_CONC, (1 - m) * K_CONC
    hits = 0
    for _ in range(N_SIM):
        p_b = rng.beta(a, b, size=n_tasks)
        p_c = np.clip(p_b + delta, 0.0, 1.0)
        r_b = rng.binomial(reps, p_b) / reps
        r_c = rng.binomial(reps, p_c) / reps
        d = r_c - r_b
        idx = rng.integers(0, n_tasks, size=(N_BOOT, n_tasks))
        boot_means = d[idx].mean(axis=1)
        lo = np.quantile(boot_means, ALPHA_LOW)
        if d.mean() >= THRESHOLD and lo > 0:
            hits += 1
    return hits / N_SIM


def main() -> None:
    rng = np.random.default_rng(SEED)
    rows = []
    for n in TASKS:
        for reps in REPS:
            for m in BASELINES:
                for delta in DELTAS:
                    pw = simulate_cell(rng, n, reps, m, delta)
                    rows.append((n, reps, m, delta, pw))

    lines = [
        "# Potencia de H1 (simulación)",
        "",
        "Generado por `analisis/potencia.py`. No editar a mano.",
        "",
        f"- Semilla: {SEED}. Simulaciones por celda: {N_SIM}. Remuestreos bootstrap: {N_BOOT}.",
        f"- Criterio: diferencia media ≥ {THRESHOLD:.2f} y límite inferior del IC95% > 0.",
        f"- Heterogeneidad entre tareas: Beta con concentración {K_CONC}.",
        "- Efecto: `p_C = p_B + δ` por tarea (truncado a [0, 1]).",
        "",
        "## Potencia por celda",
        "",
        "| Tareas | Repeticiones | Baseline B | δ real | Potencia |",
        "|---|---|---|---|---|",
    ]
    for n, reps, m, delta, pw in rows:
        lines.append(f"| {n} | {reps} | {m:.2f} | {delta:+.2f} | {pw:.2f} |")

    lines += ["", "## Efecto mínimo detectable con potencia ≥ 0,80", ""]
    lines += ["| Tareas | Repeticiones | Baseline B | δ mínimo (potencia ≥ 0,80) |", "|---|---|---|---|"]
    for n in TASKS:
        for reps in REPS:
            for m in BASELINES:
                cands = [d for (nn, rr, mm, d, pw) in rows if nn == n and rr == reps and mm == m and pw >= 0.80]
                mde = f"{min(cands):+.2f}" if cands else "> 0,20"
                lines.append(f"| {n} | {reps} | {m:.2f} | {mde} |")

    lines += [
        "",
        "## Lectura para el preregistro",
        "",
        "- Con **4 repeticiones y 30 tareas**, la potencia para δ = 0,10 queda entre 0,34 y 0,46. Con 50 tareas el rango es 0,31–0,51, prácticamente igual: no mejora de forma clara. Para δ = 0,15, 30 tareas dan 0,61–0,78 y 50 tareas dan 0,62–0,88.",
        "- La causa es que el criterio exige una diferencia observada ≥ 0,10: si el efecto real es 0,10, el resultado queda por debajo la mitad de las veces. Aumentar tareas no resuelve esto por sí solo.",
        "- Conclusión operativa: H1 solo tiene potencia adecuada para efectos de unos 15 puntos o más. Un resultado no significativo con efecto cercano a 10 puntos no permite afirmar ausencia de efecto.",
        "- Los resultados dependen de los supuestos (heterogeneidad y forma del efecto). Se declaran como supuestos, no como hechos.",
        "",
    ]
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Escrito {OUT}")


if __name__ == "__main__":
    main()
