#!/usr/bin/env python3
"""Análisis confirmatorio del experimento (PREREGISTRO §2, §6, D-16, D-17).

Unidad de análisis: la tarea (D-03). pass@1 por tarea = aciertos / repeticiones (n = 4).
- H1: diferencia media C − B por tarea. Apoyo si ≥ 0,10 y el límite inferior del IC95% > 0.
  IC95% por bootstrap pareado sobre tareas (10 000 remuestreos, semilla fija).
  Secundarias C − A y B − A con corrección de Holm.
- H2: razón de medianas de tokens totales (C / B) por tarea, con IC95% bootstrap sobre tareas.
  Apoyo si ≤ 2,0.
- H3: se calcula en analisis/h3_mutantes.py (D-39) y aquí se incorpora desde analisis/resultados_h3.json.
- Por modelo (D-17): soporte fuerte si se cumple H1 en ambos modelos; parcial si solo en uno.
- Métricas complementarias (PREREGISTRO §7): pass@2 y pass@4 (estimador de Chen et al., n = 4),
  iteraciones, tokens por tipo, costo por solución correcta y cumplimiento del preregistro.
  Usan otra semilla de bootstrap para no alterar las cifras confirmatorias.

Entrada:  resultados/experimento/episodios.csv y llamadas.jsonl
Salida:   resultados/experimento/analisis.md  y  analisis/resultados_experimento.json

Uso: .venv/bin/python analisis/analizar_experimento.py
"""

from __future__ import annotations

import csv
import json
from collections import defaultdict
from math import comb
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


LLAMADAS = RAIZ / "resultados" / "experimento" / "llamadas.jsonl"
SALIDA_H3 = RAIZ / "analisis" / "resultados_h3.json"
SEED_COMPLEMENTARIAS = SEED + 1


def pass_at_k(n: int, c: int, k: int) -> float:
    """Estimador insesgado de pass@k (Chen et al., 2021) con n muestras y c aciertos."""
    if n - c < k:
        return 1.0
    return 1.0 - comb(n - c, k) / comb(n, k)


def cargar_llamadas(ruta: Path = LLAMADAS) -> dict[tuple, dict]:
    """Suma tokens por tipo y número de llamadas por episodio (tarea, condición, repetición, modelo)."""
    acc: dict[tuple, dict] = defaultdict(lambda: {"entrada": 0, "salida": 0, "razonamiento": 0, "llamadas": 0})
    with open(ruta, encoding="utf-8") as f:
        for linea in f:
            d = json.loads(linea)
            a = acc[(d["tarea"], d["condicion"], str(d["rep"]), d["modelo"])]
            a["entrada"] += int(d["tokens_entrada"])
            a["salida"] += int(d["tokens_salida"])
            a["razonamiento"] += int(d["tokens_razonamiento"])
            a["llamadas"] += 1
    return acc


def complementarias(filas: list[dict], llamadas: dict[tuple, dict]) -> dict:
    rng = np.random.default_rng(SEED_COMPLEMENTARIAS)
    modelos = sorted({r["modelo"] for r in filas})
    tareas = sorted({r["tarea"] for r in filas})
    out: dict = {"pass_k": {}, "iteraciones": {}, "tokens": {}, "costo": {}, "llamadas_consistentes": None}

    for m in modelos + ["agregado"]:
        mods = modelos if m == "agregado" else [m]
        for c in CONDICIONES:
            for k in (1, 2, 4):
                por_tarea = []
                for t in tareas:
                    s = [r for r in filas if r["tarea"] == t and r["condicion"] == c and r["modelo"] in mods]
                    cc = sum(int(r["resuelta_heldout"]) for r in s)
                    por_tarea.append(pass_at_k(len(s), cc, k))
                arr = np.array(por_tarea)
                idx = rng.integers(0, len(arr), size=(N_BOOT, len(arr)))
                boot = arr[idx].mean(axis=1)
                out["pass_k"][f"{m}|{c}|{k}"] = {"media": float(arr.mean()),
                                                 "ic_lo": float(np.quantile(boot, 0.025)),
                                                 "ic_hi": float(np.quantile(boot, 0.975))}

    for m in modelos:
        for c in CONDICIONES:
            s = [r for r in filas if r["modelo"] == m and r["condicion"] == c]
            it = np.array([int(r["iteraciones"]) for r in s])
            out["iteraciones"][f"{m}|{c}"] = {"media": float(it.mean()), "maximo": int(it.max()),
                                              "episodios_con_reintento": int((it > 1).sum()),
                                              "n": len(s), "llamadas": int(it.sum())}

    total_llamadas = sum(v["llamadas"] for v in llamadas.values())
    total_iter = sum(int(r["iteraciones"]) for r in filas)
    out["llamadas_consistentes"] = total_llamadas == total_iter
    out["llamadas_total"] = total_llamadas

    for c in CONDICIONES:
        ep = [(k, v) for k, v in llamadas.items() if k[1] == c]
        for tipo in ("entrada", "salida", "razonamiento"):
            vals = np.array([v[tipo] for _, v in ep], dtype=float)
            out["tokens"][f"{c}|{tipo}"] = {"mediana": float(np.median(vals)), "media": float(vals.mean())}
        tot = np.array([v["entrada"] + v["salida"] + v["razonamiento"] for _, v in ep], dtype=float)
        out["tokens"][f"{c}|total"] = {"mediana": float(np.median(tot)), "media": float(tot.mean())}

    for c in CONDICIONES:
        s = [r for r in filas if r["condicion"] == c]
        coste = sum(float(r["coste_usd"]) for r in s)
        ok = sum(int(r["resuelta_heldout"]) for r in s)
        out["costo"][c] = {"coste_usd": coste, "resueltas": ok,
                           "usd_por_resuelta": coste / ok if ok else float("nan")}
    return out


def h3_datos() -> dict | None:
    if not SALIDA_H3.exists():
        return None
    return json.loads(SALIDA_H3.read_text(encoding="utf-8"))


def redactar(res: dict, comp: dict | None = None) -> str:
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
    h3 = h3_datos()
    L += ["", "## H3 (detección de mutantes, D-39)", ""]
    if h3:
        L += [f"- Puntuación de la suite de C: {h3['puntuacion_C']:.3f}. Línea base de B: {h3['puntuacion_B']:.3f}.",
              f"- Diferencia C − B: {h3['diferencia']:+.3f} [IC95% {h3['ic_lo']:+.3f}, {h3['ic_hi']:+.3f}].",
              f"- Mutantes: {h3['totales']['mutantes']} generados; {h3['totales']['equivalentes']} equivalentes excluidos; "
              f"{h3['totales']['indeterminados']} indeterminados incluidos; {h3['totales']['no_equivalentes']} evaluados.",
              f"- **H3: {'SE CUMPLE' if h3['H3_apoyo'] else 'NO SE CUMPLE'}** (lectura: fuerza de la suite, no efecto sobre los modelos; ver D-40)."]
    else:
        L.append("**No disponible.** Ejecutar `analisis/h3_mutantes.py`.")

    if comp:
        L += ["", "## Métricas complementarias (PREREGISTRO §7)", "",
              "### pass@1, pass@2 y pass@4 (n = 4 repeticiones por tarea)", "",
              "| Modelo | Condición | pass@1 | pass@2 | pass@4 |", "|---|---|---|---|---|"]
        for m in sorted({k.split("|")[0] for k in comp["pass_k"]}):
            for c in CONDICIONES:
                celdas = []
                for k in (1, 2, 4):
                    v = comp["pass_k"][f"{m}|{c}|{k}"]
                    celdas.append(f"{v['media']:.3f} [{v['ic_lo']:.3f}, {v['ic_hi']:.3f}]")
                L.append(f"| {m} | {c} | " + " | ".join(celdas) + " |")
        L += ["", "Por modelo, n = 4 por tarea. La fila *agregado* usa n = 8 por tarea (ambos modelos).", "",
              "### Iteraciones por episodio", "",
              "| Modelo | Condición | Media | Máximo | Episodios con reintento | Llamadas |", "|---|---|---|---|---|---|"]
        for k, v in comp["iteraciones"].items():
            m, c = k.split("|")
            L.append(f"| {m} | {c} | {v['media']:.3f} | {v['maximo']} | {v['episodios_con_reintento']} de {v['n']} | {v['llamadas']} |")
        L += ["", f"Llamadas en `llamadas.jsonl`: {comp['llamadas_total']}. "
              f"Coinciden con la suma de iteraciones: {'sí' if comp['llamadas_consistentes'] else 'NO'}.",
              "", "### Tokens por episodio (suma de todas las llamadas del episodio, ambos modelos)", "",
              "| Condición | Entrada (mediana) | Salida (mediana) | Razonamiento (mediana) | Total (mediana) | Total (media) |",
              "|---|---|---|---|---|---|"]
        for c in CONDICIONES:
            t = comp["tokens"]
            L.append(f"| {c} | {t[c + '|entrada']['mediana']:.0f} | {t[c + '|salida']['mediana']:.0f} | "
                     f"{t[c + '|razonamiento']['mediana']:.0f} | {t[c + '|total']['mediana']:.0f} | {t[c + '|total']['media']:.0f} |")
        L += ["", "### Costo por solución correcta", "",
              "| Condición | Coste total (USD) | Resueltas | USD por resuelta |", "|---|---|---|---|"]
        for c in CONDICIONES:
            v = comp["costo"][c]
            L.append(f"| {c} | {v['coste_usd']:.4f} | {v['resueltas']} | {v['usd_por_resuelta']:.5f} |")

    L += ["", "## Cumplimiento del preregistro", "",
          "| Elemento (PREREGISTRO) | Estado | Nota |", "|---|---|---|",
          "| H1 primaria y secundarias con Holm (§2, §6) | Ejecutado | Ver arriba. |",
          "| Sensibilidad con regresión mixta y GEE (D-17) | Ejecutado | Ver `sensibilidad.md`; el mixto es bayesiano aproximado (D-41). |",
          "| H2 con desglose de tokens y costo por resuelta (§7) | Ejecutado | Ver arriba. |",
          "| H3 con equivalentes reportados (§7, §9) | Ejecutado | Ver `h3.md` (D-39). |",
          "| pass@2 y pass@4 (§7) | Ejecutado | Ver arriba. |",
          "| Iteraciones y tokens por episodio (§7) | Ejecutado | Ver arriba. |",
          "| Potencia de H1 (§6) | Ejecutado | `analisis/potencia.md`. |",
          "| Truncados por condición y modelo (§5, D-36) | Ejecutado | Ver tabla de truncados. |",
          "| Tiempos por llamada y episodio (§7) | **No ejecutado** | `llamadas.jsonl` solo guarda la hora de inicio; no hay latencia. |",
          "| Comprobaciones estáticas y aserciones dinámicas en el bucle de C (§3, §8) | **No implementado** | El bucle de C usa solo equivalencia de unitarias y chi-cuadrado. |",
          "| Propiedades metamórficas en la suite reservada (§8) | **No implementado** | `arnes/heldout.py` solo usa referencia independiente. |",
          "| Equivalencia parcial con auxiliares (§9) | **No encontrado** | Sin implementación en `arnes/verificacion.py`. Revisar antes de citarla. |",
          "| Régimen con ruido despolarizante (§10) | **No ejecutado** | No hay código de ruido ni calibración del umbral (§9). |",
          "| Reintentos de B (§3, §11) | **Hallazgo** | B nunca reintentó: 0 de 400 episodios con más de 1 iteración. |",
          "| Presupuesto igualado B-tok (§3) | Excluido | D-06: la conclusión se limita a 'C supera a B'. |"]
    return "\n".join(L) + "\n"


def main() -> int:
    filas = cargar()
    res = analizar(filas)
    comp = complementarias(filas, cargar_llamadas())
    res["complementarias"] = comp
    texto = redactar(res, comp)
    SALIDA_MD.parent.mkdir(parents=True, exist_ok=True)
    SALIDA_MD.write_text(texto, encoding="utf-8")
    SALIDA_JSON.write_text(json.dumps(res, indent=2, ensure_ascii=False), encoding="utf-8")
    print(texto)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
