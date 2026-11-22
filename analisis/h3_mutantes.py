#!/usr/bin/env python3
"""H3 (D-39): puntuación de mutación de la suite del bucle de C sobre mutantes de referencia.

- Mutantes: familias H3 (eliminar_compuerta, intercambiar_qubits, anadir_compuerta), 6 por familia
  y tarea, semilla fija. Las familias del bucle no se usan (son las que C ve).
- Suite de C: evaluar() con la semilla del bucle del experimento (arnes/evaluador.py).
- Línea base de B: comprobación de solo ejecución (mismo número de qubits). Un mutante
  de circuito siempre ejecuta, así que la línea base se calcula explícitamente, no se asume.
- Puntuación: mutantes detectados / mutantes no equivalentes e indeterminados. Los equivalentes
  se excluyen y se reportan.
- Criterio: diferencia C − B ≥ 0,10 con IC95% (bootstrap sobre tareas) > 0. Si la línea base
  supera 0,90, H3 no es evaluable.

Salida: resultados/experimento/h3.md y analisis/resultados_h3.json
Uso:    .venv/bin/python -m analisis.h3_mutantes
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

import numpy as np

from arnes.evaluador import evaluar
from arnes.piloto import SEED_BUCLE
from tareas.catalogo import TAREAS
from tareas.mutantes import FAMILIAS_H3, clasificar, generar_mutantes

RAIZ = Path(__file__).resolve().parent.parent
SALIDA_MD = RAIZ / "resultados" / "experimento" / "h3.md"
SALIDA_JSON = RAIZ / "analisis" / "resultados_h3.json"
SEED_MUTANTES = 20261121
POR_FAMILIA = 6
N_BOOT = 10_000
UMBRAL = 0.10


def main() -> int:
    filas = []
    for tarea in TAREAS:
        ref = tarea.construir()
        mutantes = [m for m in generar_mutantes(ref, seed=SEED_MUTANTES, por_familia=POR_FAMILIA)
                    if m.familia in FAMILIAS_H3]
        n_det = n_base = n_ne = 0
        clases = Counter()
        for m in mutantes:
            clase = clasificar(ref, m.circuito)
            clases[clase] += 1
            if clase == "equivalente":
                continue
            n_ne += 1
            if not evaluar(tarea, m.circuito, seed=SEED_BUCLE).aprobada:
                n_det += 1
            if m.circuito.num_qubits != ref.num_qubits:
                n_base += 1
        filas.append({"tarea": tarea.id, "categoria": tarea.categoria, "no_equivalentes": n_ne,
                      "detectados_C": n_det, "detectados_B": n_base,
                      "equivalentes": clases["equivalente"], "indeterminados": clases["indeterminado"]})

    totales = {
        "mutantes": sum(f["no_equivalentes"] + f["equivalentes"] for f in filas),
        "equivalentes": sum(f["equivalentes"] for f in filas),
        "indeterminados": sum(f["indeterminados"] for f in filas),
        "no_equivalentes": sum(f["no_equivalentes"] for f in filas),
    }
    rng = np.random.default_rng(SEED_MUTANTES)
    puntuacion_C = np.array([f["detectados_C"] / f["no_equivalentes"] for f in filas if f["no_equivalentes"]])
    puntuacion_B = np.array([f["detectados_B"] / f["no_equivalentes"] for f in filas if f["no_equivalentes"]])
    dif = puntuacion_C - puntuacion_B
    idx = rng.integers(0, len(dif), size=(N_BOOT, len(dif)))
    boot = dif[idx].mean(axis=1)
    lo, hi = float(np.quantile(boot, 0.025)), float(np.quantile(boot, 0.975))
    base = float(puntuacion_B.mean())
    evaluable = base <= 0.90
    cumple = evaluable and float(dif.mean()) >= UMBRAL and lo > 0

    res = {
        "puntuacion_C": float(puntuacion_C.mean()),
        "puntuacion_B": base,
        "diferencia": float(dif.mean()),
        "ic_lo": lo,
        "ic_hi": hi,
        "evaluable": evaluable,
        "H3_apoyo": bool(cumple),
        "totales": totales,
        "por_tarea": filas,
    }
    SALIDA_JSON.write_text(json.dumps(res, indent=2, ensure_ascii=False), encoding="utf-8")

    L = ["# H3: puntuación de mutación de la suite del bucle de C", "",
         "Generado por `analisis/h3_mutantes.py`. No editar a mano.", "",
         f"- Mutantes generados: {totales['mutantes']}. Equivalentes excluidos: {totales['equivalentes']}. "
         f"Indeterminados (más de 8 qubits, incluidos en la puntuación): {totales['indeterminados']}. "
         f"No equivalentes evaluados: {totales['no_equivalentes']}.",
         "", "| Medida | Valor |", "|---|---|",
         f"| Puntuación suite de C | {res['puntuacion_C']:.3f} |",
         f"| Línea base B (solo ejecución) | {res['puntuacion_B']:.3f} |",
         f"| Diferencia C − B | {res['diferencia']:+.3f} [IC95% {lo:+.3f}, {hi:+.3f}] |",
         f"| Evaluable (línea base ≤ 0,90) | {'sí' if evaluable else 'no'} |",
         f"| **H3 (≥ 0,10 y IC inferior > 0)** | **{'SE CUMPLE' if cumple else 'NO SE CUMPLE'}** |",
         "", "Los indeterminados se incluyen en el denominador; ver D-39."]
    SALIDA_MD.write_text("\n".join(L) + "\n", encoding="utf-8")
    print("\n".join(L))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
