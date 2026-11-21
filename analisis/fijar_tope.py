#!/usr/bin/env python3
"""Análisis del piloto: fija el tope de tokens por episodio (D-02) y resume el coste.

Regla (PREREGISTRO §5, D-02): T = 5 × q95 de tokens por llamada del piloto, redondeado a miles
hacia arriba. Un episodio que supera T se trunca y cuenta como no resuelto.

Entradas: resultados/piloto/llamadas.jsonl y resultados/piloto/episodios.csv
Salida:   resultados/piloto/tope.md

Uso: .venv/bin/python analisis/fijar_tope.py [directorio_piloto]
"""

from __future__ import annotations

import csv
import json
import math
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

MULTIPLO = 5
REDONDEO = 1000


def tokens_llamada(l: dict) -> int:
    return (
        l["tokens_entrada"]
        + l["tokens_cache_lectura"]
        + l["tokens_cache_escritura"]
        + l["tokens_salida"]
        + l["tokens_razonamiento"]
    )


def fijar_tope(llamadas: list[dict]) -> tuple[int, float]:
    valores = np.array([tokens_llamada(l) for l in llamadas], dtype=float)
    q95 = float(np.quantile(valores, 0.95))
    tope = math.ceil(MULTIPLO * q95 / REDONDEO) * REDONDEO
    return tope, q95


def resumir(directorio: Path) -> str:
    llamadas = [json.loads(l) for l in (directorio / "llamadas.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    with open(directorio / "episodios.csv", encoding="utf-8") as f:
        episodios = list(csv.DictReader(f))
    if not llamadas:
        return "# Tope de tokens (piloto)\n\nNo hay llamadas en el piloto.\n"

    tope, q95 = fijar_tope(llamadas)
    valores = np.array([tokens_llamada(l) for l in llamadas], dtype=float)
    coste = sum(float(e["coste_usd"]) for e in episodios)

    razon = defaultdict(lambda: [0, 0])
    for l in llamadas:
        k = (l["modelo"], l["condicion"])
        razon[k][1] += 1
        if l["tokens_razonamiento"] > 0:
            razon[k][0] += 1

    truncados = Counter()
    for e in episodios:
        if int(e["tokens_total"]) > tope:
            truncados[(e["modelo"], e["condicion"])] += 1

    lineas = [
        "# Tope de tokens (piloto)",
        "",
        "Generado por `analisis/fijar_tope.py`. No editar a mano.",
        "",
        f"- Llamadas del piloto: {len(llamadas)}. Episodios: {len(episodios)}.",
        f"- Tokens por llamada: mediana {np.median(valores):.0f}, q95 {q95:.0f}, máximo {valores.max():.0f}.",
        f"- **Tope por episodio T = 5 × q95, redondeado a miles hacia arriba: {tope} tokens.**",
        f"- Coste del piloto a precio de lista: {coste:.4f} USD (control: 6 USD).",
        "",
        "## Razonamiento por modelo y condición (D-28)",
        "",
        "Llamadas con tokens de razonamiento > 0. Si es 0 en todas, `medium` no está actuando.",
        "",
        "| Modelo | Condición | Llamadas con razonamiento | Llamadas |",
        "|---|---|---|---|",
    ]
    for (modelo, cond), (con, tot) in sorted(razon.items()):
        lineas.append(f"| {modelo} | {cond} | {con} | {tot} |")
    lineas += [
        "",
        "## Episodios que superarían T",
        "",
        "| Modelo | Condición | Truncados con T |",
        "|---|---|---|",
    ]
    for (modelo, cond) in sorted(razon):
        lineas.append(f"| {modelo} | {cond} | {truncados.get((modelo, cond), 0)} |")
    lineas.append("")
    return "\n".join(lineas)


def main() -> int:
    directorio = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / "resultados" / "piloto"
    texto = resumir(directorio)
    (directorio / "tope.md").write_text(texto, encoding="utf-8")
    print(texto)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
