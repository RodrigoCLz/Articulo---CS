#!/usr/bin/env python3
"""Análisis EXPLORATORIO por categoría (no confirmatorio, no cambia H1–H3).

Tasa de resolución en la suite reservada, por categoría, condición y modelo. Sirve para
proponer un estudio de seguimiento; no tiene potencia para afirmar diferencias por categoría.

Salida: resultados/experimento/exploratorio_categorias.md
Uso:    .venv/bin/python -m analisis.exploratorio_categorias
"""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path

from analisis.analizar_experimento import CONDICIONES, cargar

RAIZ = Path(__file__).resolve().parent.parent
SALIDA = RAIZ / "resultados" / "experimento" / "exploratorio_categorias.md"


def main() -> int:
    filas = cargar()
    acc = defaultdict(lambda: [0, 0])
    modelos = sorted({r["modelo"] for r in filas})
    categorias = sorted({r["categoria"] for r in filas})
    for r in filas:
        k = (r["categoria"], r["condicion"], r["modelo"])
        acc[k][0] += int(r["resuelta_heldout"])
        acc[k][1] += 1
    L = ["# Análisis exploratorio por categoría", "",
         "**Exploratorio.** No es confirmatorio y no cambia H1–H3. Tasa de resolución en la suite reservada.",
         "Generado por `analisis/exploratorio_categorias.py`.", ""]
    for m in modelos:
        L += [f"## {m}", "", "| Categoría | A | B | C |", "|---|---|---|---|"]
        for cat in categorias:
            celdas = []
            for c in CONDICIONES:
                ok, n = acc[(cat, c, m)]
                celdas.append(f"{ok}/{n}")
            L.append(f"| {cat} | " + " | ".join(celdas) + " |")
        L.append("")
    SALIDA.write_text("\n".join(L), encoding="utf-8")
    print("\n".join(L))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
