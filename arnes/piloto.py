"""Ejecutor del piloto (PREREGISTRO §13, D-02, D-26, D-27).

Ejecuta las 5 tareas del piloto en las tres condiciones, con los dos modelos, en `medium`, con
4 repeticiones. No entra en el análisis confirmatorio.

Controles:
- Sin clave en OPENCODE_GO_API_KEY no arranca.
- Si el coste acumulado (precio de lista) supera el tope de control (6 USD, el doble de la
  referencia de 3 USD, D-02), se detiene y se reporta.
- No aplica tope de tokens: el piloto mide el consumo real para fijar el tope (D-02).
"""

from __future__ import annotations

import csv
import json
from dataclasses import asdict
from pathlib import Path

from arnes.cliente import MODELOS, Registro, Transporte
from arnes.episodio import CONDICIONES, Episodio, ejecutar_episodio
from tareas.piloto import PILOTO

REPETICIONES = 4
TOPE_CONTROL_USD = 6.0
SEED_BUCLE = 20261121
SALIDA = Path(__file__).resolve().parent.parent / "resultados" / "piloto"

# Precios de lista por millón de tokens, catálogo de OpenCode Go (2026-11-21):
# (entrada, salida, lectura caché, escritura caché) en tramo base y en tramo alto.
PRECIOS = {
    MODELOS[0]: {"base": (0.10, 0.50, 0.01, 0.125), "alto": (0.20, 0.75, 0.02, 0.25), "umbral": 272_000},
    MODELOS[1]: {"base": (0.10, 0.50, 0.01, 0.125), "alto": (0.50, 2.50, 0.05, 0.625), "umbral": 100_000},
}


def coste_llamada(r: Registro) -> float:
    p = PRECIOS[r.modelo]
    contexto = r.tokens_entrada + r.tokens_cache_lectura + r.tokens_cache_escritura
    ent, sal, lec, esc = p["alto"] if contexto > p["umbral"] else p["base"]
    return (
        r.tokens_entrada * ent
        + (r.tokens_salida + r.tokens_razonamiento) * sal
        + r.tokens_cache_lectura * lec
        + r.tokens_cache_escritura * esc
    ) / 1_000_000


def _fila_episodio(ep: Episodio, coste: float) -> dict:
    return {
        "tarea": ep.tarea_id,
        "condicion": ep.condicion,
        "modelo": ep.modelo,
        "iteraciones": ep.iteraciones,
        "resuelta_bucle": int(ep.resuelta_bucle),
        "resuelta_heldout": int(ep.resuelta_heldout),
        "truncado": int(ep.truncado),
        "tokens_total": ep.tokens_total,
        "coste_usd": round(coste, 6),
        "detalle_heldout": ep.detalle_heldout,
    }


def correr_piloto(transporte: Transporte, salida: Path = SALIDA, reps: int = REPETICIONES) -> dict:
    salida.mkdir(parents=True, exist_ok=True)
    filas, llamadas = [], []
    coste_total = 0.0
    parado = False
    for tarea in PILOTO:
        for modelo in MODELOS:
            for condicion in CONDICIONES:
                for rep in range(reps):
                    ep = ejecutar_episodio(
                        tarea, condicion, transporte, modelo,
                        tope_tokens=10**12, seed_bucle=SEED_BUCLE + rep,
                    )
                    coste_ep = 0.0
                    for reg in ep.registros:
                        c = coste_llamada(reg)
                        coste_ep += c
                        llamadas.append({"tarea": tarea.id, "condicion": condicion, "rep": rep, **asdict(reg), "coste_usd": c})
                    coste_total += coste_ep
                    filas.append(_fila_episodio(ep, coste_ep) | {"repeticion": rep})
                    if coste_total > TOPE_CONTROL_USD:
                        parado = True
                        break
                if parado:
                    break
            if parado:
                break
        if parado:
            break

    with open(salida / "episodios.csv", "w", newline="", encoding="utf-8") as f:
        if filas:
            w = csv.DictWriter(f, fieldnames=list(filas[0].keys()))
            w.writeheader()
            w.writerows(filas)
    with open(salida / "llamadas.jsonl", "w", encoding="utf-8") as f:
        for l in llamadas:
            f.write(json.dumps(l, ensure_ascii=False) + "\n")
    return {"episodios": len(filas), "llamadas": len(llamadas), "coste_usd": round(coste_total, 4), "detenido_por_control": parado}


if __name__ == "__main__":
    from arnes.transporte import ClaveAusente, TransporteOpenCodeGo, VAR_CLAVE

    import os

    if not os.environ.get(VAR_CLAVE):
        raise SystemExit(f"Falta la variable {VAR_CLAVE}. No se ejecuta el piloto.")
    try:
        print(correr_piloto(TransporteOpenCodeGo()))
    except ClaveAusente as e:
        raise SystemExit(str(e))
