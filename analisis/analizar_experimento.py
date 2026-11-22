#!/usr/bin/env python3
"""Análisis confirmatorio del experimento (PREREGISTRO §2, §6, D-16, D-17).

Unidad de análisis: la tarea (D-03). pass@1 por tarea = aciertos / repeticiones (n = 4).
- H1: diferencia media C − B por tarea. Apoyo si ≥ 0,10 y el límite inferior del IC95% > 0.
  IC95% por bootstrap pareado sobre tareas (10 000 remuestreos, semilla fija).
  Secundarias C − A y B − A con corrección de Holm.
- H2: razón de medianas de tokens totales (C / B) por tarea, con IC95% bootstrap sobre tareas.
  Apoyo si ≤ 2,0.
- H3: no se calcula aquí (requiere evaluar mutantes sobre el código final). Ver analisis/PENDIENTE.
- Por modelo (D-17): soporte fuerte si se cumple H1 en ambos modelos; parcial si solo en uno.

Entrada:  resultados/experimento/episodios.csv
Salida:   resultados/experimento/analisis.md  y  analisis/resultados_experimento.json

Uso: .venv/bin/python analisis/analizar_experimento.py
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

import numpy as np

RAIZ = Path(__file__).resolve().parent.parent
ENTRADA = RAIZ / "resultados" / "experimento" / "episodios.csv"
SALIDA_MD = RAIZ / "resultados" / "experimento" / "analisis.md"
SALIDA_JSON = RAIZ / "analisis" / "resultados_experimento.json"
SEED = 20261121
N_BOOT = 10_000
UMBRAL_H1 = 0.10
LIMITE_H2 = 2.0
CONDICIONES = ("A", "B", "C")


def cargar(ruta: Path = ENTRADA) -> list[dict]:
    with open(ruta, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def pass_por_tarea(filas: list[dict], modelo: str) -> dict[str, dict[str, float]]:
    """pass@1[tarea][condición] = aciertos / repeticiones (estimador de Chen et al. con k = 1)."""
    tareas = sorted({r["tarea"] for r in filas})
    out: dict[str, dict[str, float]] = {t: {} for t in tareas}
    for t in tareas:
        for c in CONDICIONES:
            s = [r for r in filas if r["tarea"] == t and r["condicion"] == c and r["modelo"] == modelo]
            out[t][c] = sum(int(r["resuelta_heldout"]) for r in s) / len(s)
    return out


def tokens_por_tarea(filas: list[dict], modelo: str) -> dict[str, dict[str, int]]:
    tareas = sorted({r["tarea"] for r in filas})
    out: dict[str, dict[str, int]] = {t: {} for t in tareas}
    for t in tareas:
        for c in CONDICIONES:
            s = [r for r in filas if r["tarea"] == t and r["condicion"] == c and r["modelo"] == modelo]
            out[t][c] = sum(int(r["tokens_total"]) for r in s)
    return out


def boot_media_diferencia(d: np.ndarray, rng: np.random.Generator) -> tuple[float, float, float]:
    """Media de d y su IC95% por bootstrap pareado sobre tareas. Devuelve (media, lo, hi)."""
    n = len(d)
    idx = rng.integers(0, n, size=(N_BOOT, n))
    medias = d[idx].mean(axis=1)
    return float(d.mean()), float(np.quantile(medias, 0.025)), float(np.quantile(medias, 0.975))


def p_bootstrap(d: np.ndarray, medias: np.ndarray) -> float:
    """p bilateral aproximado: 2 × mín(P(media* ≤ 0), P(media* ≥ 0)), centrado en la media observada."""
    centradas = medias - d.mean()
    p_lo = np.mean(centradas + d.mean() <= 0)
    p_hi = np.mean(centradas + d.mean() >= 0)
    return float(min(1.0, 2 * min(p_lo, p_hi)))


def holm(pvals: dict[str, float]) -> dict[str, float]:
    orden = sorted(pvals.items(), key=lambda kv: kv[1])
    m = len(orden)
    ajustado: dict[str, float] = {}
    previo = 0.0
    for i, (nombre, p) in enumerate(orden):
        aj = min(1.0, max(previo, (m - i) * p))
        ajustado[nombre] = aj
        previo = aj
    return ajustado


def analizar(filas: list[dict]) -> dict:
    rng = np.random.default_rng(SEED)
    modelos = sorted({r["modelo"] for r in filas})
    resultado: dict = {"modelos": {}, "pooled": {}, "n_episodios": len(filas)}

    tablas = {m: pass_por_tarea(filas, m) for m in modelos}
    tareas = sorted(tablas[modelos[0]].keys())

    def vector(modelo_list, a: str, b: str) -> np.ndarray:
        return np.array([np.mean([tablas[m][t][a] - tablas[m][t][b] for m in modelo_list]) for t in tareas])

    for m in modelos:
        res = {}
        for a, b in [("C", "B"), ("C", "A"), ("B", "A")]:
            d = vector([m], a, b)
            mu, lo, hi = boot_media_diferencia(d, rng)
            res[f"{a}-{b}"] = {"media": mu, "ic_lo": lo, "ic_hi": hi}
        res["H1_apoyo"] = bool(res["C-B"]["media"] >= UMBRAL_H1 and res["C-B"]["ic_lo"] > 0)
        res["tasa"] = {c: float(np.mean([tablas[m][t][c] for t in tareas])) for c in CONDICIONES}
        resultado["modelos"][m] = res

    pooled = {}
    for a, b in [("C", "B"), ("C", "A"), ("B", "A")]:
        d = vector(modelos, a, b)
        mu, lo, hi = boot_media_diferencia(d, rng)
        idx = rng.integers(0, len(d), size=(N_BOOT, len(d)))
        boot = d[idx].mean(axis=1)
        pooled[f"{a}-{b}"] = {"media": mu, "ic_lo": lo, "ic_hi": hi, "p": p_bootstrap(d, boot)}
    ajustes = holm({"C-A": pooled["C-A"]["p"], "B-A": pooled["B-A"]["p"]})
    pooled["C-A"]["p_holm"] = ajustes["C-A"]
    pooled["B-A"]["p_holm"] = ajustes["B-A"]
    pooled["H1_apoyo"] = bool(pooled["C-B"]["media"] >= UMBRAL_H1 and pooled["C-B"]["ic_lo"] > 0)
    resultado["pooled"] = pooled

    # H1 por modelo: soporte fuerte o parcial (D-17)
    apoyos = [resultado["modelos"][m]["H1_apoyo"] for m in modelos]
    if all(apoyos):
        resultado["H1_soporte"] = "fuerte"
    elif any(apoyos):
        resultado["H1_soporte"] = "parcial"
    else:
        resultado["H1_soporte"] = "no apoyada"

    # H2: razón de medianas de tokens totales por tarea-condición (D-16), por modelo y agregada
    h2 = {}
    for m in modelos + ["agregado"]:
        mods = modelos if m == "agregado" else [m]
        tok = {}
        for mm in mods:
            t = tokens_por_tarea(filas, mm)
            for tarea in tareas:
                for c in ("B", "C"):
                    tok.setdefault((tarea, c), 0)
                    tok[(tarea, c)] += t[tarea][c]
        tb = np.array([tok[(t, "B")] for t in tareas], dtype=float)
        tc = np.array([tok[(t, "C")] for t in tareas], dtype=float)
        razon = float(np.median(tc) / np.median(tb))
        idx = rng.integers(0, len(tareas), size=(N_BOOT, len(tareas)))
        boot = np.median(tc[idx], axis=1) / np.median(tb[idx], axis=1)
        h2[m] = {"razon": razon, "ic_lo": float(np.quantile(boot, 0.025)),
                 "ic_hi": float(np.quantile(boot, 0.975)), "H2_apoyo": bool(razon <= LIMITE_H2)}
    resultado["H2"] = h2

    trunc = {}
    for m in modelos:
        for c in CONDICIONES:
            s = [r for r in filas if r["modelo"] == m and r["condicion"] == c]
            trunc[f"{m}|{c}"] = sum(int(r["truncado"]) for r in s)
    resultado["truncados"] = trunc
    resultado["coste_usd"] = round(sum(float(r["coste_usd"]) for r in filas), 4)
    return resultado


def redactar(res: dict) -> str:
    L = ["# Análisis confirmatorio (experimento)", "",
         "Generado por `analisis/analizar_experimento.py`. No editar a mano.", "",
         f"- Episodios: {res['n_episodios']}. Coste a precio de lista: {res['coste_usd']} USD.",
         f"- Bootstrap: {N_BOOT} remuestreos sobre tareas, semilla {SEED}.", "",
         "## H1 (corrección): C − B", "",
         "| Comparación | Diferencia media | IC95% | p (Holm) |", "|---|---|---|---|"]
    p = res["pooled"]
    L.append(f"| **C − B** (primaria, agregada) | {p['C-B']['media']:+.3f} | [{p['C-B']['ic_lo']:+.3f}, {p['C-B']['ic_hi']:+.3f}] | — |")
    L.append(f"| C − A (secundaria) | {p['C-A']['media']:+.3f} | [{p['C-A']['ic_lo']:+.3f}, {p['C-A']['ic_hi']:+.3f}] | {p['C-A']['p_holm']:.3f} |")
    L.append(f"| B − A (secundaria) | {p['B-A']['media']:+.3f} | [{p['B-A']['ic_lo']:+.3f}, {p['B-A']['ic_hi']:+.3f}] | {p['B-A']['p_holm']:.3f} |")
    L += ["", f"**Criterio de H1 (≥ {UMBRAL_H1:+.2f} y límite inferior > 0):** {'SE CUMPLE' if p['H1_apoyo'] else 'NO SE CUMPLE'}. "
          f"Soporte por modelo: **{res['H1_soporte']}**.", "",
          "## Tasas pass@1 por modelo y condición", "",
          "| Modelo | A | B | C | C − B | IC95% | Cumple H1 |", "|---|---|---|---|---|---|---|"]
    for m, r in res["modelos"].items():
        cb = r["C-B"]
        L.append(f"| {m} | {r['tasa']['A']:.3f} | {r['tasa']['B']:.3f} | {r['tasa']['C']:.3f} | "
                 f"{cb['media']:+.3f} | [{cb['ic_lo']:+.3f}, {cb['ic_hi']:+.3f}] | {'sí' if r['H1_apoyo'] else 'no'} |")
    L += ["", "## H2 (costo): razón de medianas de tokens C / B", "",
          "| Modelo | Razón | IC95% | Cumple H2 (≤ 2) |", "|---|---|---|---|"]
    for m, r in res["H2"].items():
        L.append(f"| {m} | {r['razon']:.3f} | [{r['ic_lo']:.3f}, {r['ic_hi']:.3f}] | {'sí' if r['H2_apoyo'] else 'no'} |")
    L += ["", "## Truncados (tope de 20 000 tokens, D-36)", "", "| Modelo | Condición | Truncados |", "|---|---|---|"]
    for k, v in res["truncados"].items():
        m, c = k.split("|")
        L.append(f"| {m} | {c} | {v} |")
    L += ["", "## H3 (detección de mutantes)", "",
          "**No calculado en este informe.** Requiere evaluar mutantes sobre el código final de cada episodio. Pendiente."]
    return "\n".join(L) + "\n"


def main() -> int:
    filas = cargar()
    res = analizar(filas)
    SALIDA_MD.parent.mkdir(parents=True, exist_ok=True)
    SALIDA_MD.write_text(redactar(res), encoding="utf-8")
    SALIDA_JSON.write_text(json.dumps(res, indent=2, ensure_ascii=False), encoding="utf-8")
    print(redactar(res))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
