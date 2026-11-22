#!/usr/bin/env python3
"""Figuras y tablas del artículo, generadas desde los datos del experimento.

Entradas: resultados/experimento/episodios.csv, llamadas.jsonl, analisis/resultados_experimento.json,
          analisis/resultados_h3.json
Salidas:  paper/figuras/*.pdf  (tasas, diferencias, categorías, tokens)
          paper/tablas/*.tex   (H1, pass@k, costo, H3)

Las cifras se calculan con las mismas funciones que analisis/analizar_experimento.py.
Uso: .venv/bin/python -m analisis.figuras   (después de analizar_experimento y h3_mutantes)
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

from analisis.analizar_experimento import (  # noqa: E402
    CONDICIONES,
    N_BOOT,
    SALIDA_JSON,
    cargar,
    cargar_llamadas,
    h3_datos,
)

RAIZ = Path(__file__).resolve().parent.parent
FIG = RAIZ / "paper" / "figuras"
TAB = RAIZ / "paper" / "tablas"
SEED_FIG = 20261123
UMBRAL = 0.10

plt.rcParams.update({"font.size": 8, "axes.spines.top": False, "axes.spines.right": False,
                     "pdf.fonttype": 42, "figure.dpi": 150})


def tex(x: float, dec: int = 3, signo: bool = False) -> str:
    """Número para LaTeX: el signo menos en modo matemático."""
    s = f"{x:+.{dec}f}" if signo else f"{x:.{dec}f}"
    s = s.replace(".", "{,}").replace("-", "$-$").replace("+", "+")
    return s


def tasas_por_tarea(filas: list[dict], modelo: str | None, condicion: str) -> np.ndarray:
    tareas = sorted({r["tarea"] for r in filas})
    out = []
    for t in tareas:
        s = [r for r in filas if r["tarea"] == t and r["condicion"] == condicion
             and (modelo is None or r["modelo"] == modelo)]
        out.append(np.mean([int(r["resuelta_heldout"]) for r in s]))
    return np.array(out)


def ic_media(x: np.ndarray, rng: np.random.Generator) -> tuple[float, float, float]:
    idx = rng.integers(0, len(x), size=(N_BOOT, len(x)))
    boot = x[idx].mean(axis=1)
    return float(x.mean()), float(np.quantile(boot, 0.025)), float(np.quantile(boot, 0.975))


def figura_tasas(filas: list[dict], rng: np.random.Generator) -> None:
    modelos = sorted({r["modelo"] for r in filas})
    etiquetas = {m: m.replace("opencode-go/", "") for m in modelos}
    fig, ax = plt.subplots(figsize=(3.5, 2.4))
    ancho = 0.35
    x = np.arange(len(CONDICIONES))
    for i, m in enumerate(modelos):
        medias, errs_lo, errs_hi = [], [], []
        for c in CONDICIONES:
            mu, lo, hi = ic_media(tasas_por_tarea(filas, m, c), rng)
            medias.append(mu)
            errs_lo.append(mu - lo)
            errs_hi.append(hi - mu)
        ax.bar(x + (i - 0.5) * ancho, medias, ancho, yerr=[errs_lo, errs_hi], capsize=2,
               label=etiquetas[m], color=["#4C72B0", "#DD8452"][i], alpha=0.9)
    ax.set_xticks(x, [f"{c}\n" + {"A": "una pasada", "B": "comprobación de ejecución", "C": "verificación"}[c]
                      for c in CONDICIONES], fontsize=7)
    ax.set_ylim(0.85, 1.03)
    ax.set_ylabel("pass@1 (held-out)")
    ax.legend(frameon=False, fontsize=7, loc="upper left", ncol=2)
    ax.set_title("Resolución por condición y modelo (IC95%)", fontsize=8)
    fig.tight_layout()
    fig.savefig(FIG / "tasas.pdf")
    plt.close(fig)


def figura_diferencias(res: dict) -> None:
    filas = []
    p = res["pooled"]
    filas.append(("C − B (primaria)", p["C-B"]))
    filas.append(("C − A", p["C-A"]))
    filas.append(("B − A", p["B-A"]))
    for m, r in res["modelos"].items():
        filas.append((f"C − B, {m.replace('opencode-go/', '')}", r["C-B"]))
    fig, ax = plt.subplots(figsize=(3.5, 2.4))
    y = np.arange(len(filas))[::-1]
    for yi, (nombre, v) in zip(y, filas):
        ax.plot([v["ic_lo"], v["ic_hi"]], [yi, yi], color="black", lw=1)
        ax.plot(v["media"], yi, "o", color="#4C72B0")
    ax.axvline(0, color="grey", lw=0.8)
    ax.axvline(UMBRAL, color="#C44E52", lw=0.8, ls="--")
    ax.text(UMBRAL, -0.9, "umbral 10 pp", color="#C44E52", fontsize=6, ha="right", va="bottom")
    ax.set_ylim(-1.0, len(filas) - 0.5)
    ax.set_yticks(y, [f[0] for f in filas], fontsize=7)
    ax.set_xlabel("Diferencia de pass@1")
    ax.set_title("Diferencias pareadas por tarea (IC95%)", fontsize=8)
    fig.tight_layout()
    fig.savefig(FIG / "diferencias.pdf")
    plt.close(fig)


def figura_categorias(filas: list[dict]) -> None:
    categorias = sorted({r["categoria"] for r in filas})
    M = np.zeros((len(categorias), len(CONDICIONES)))
    for i, cat in enumerate(categorias):
        for j, c in enumerate(CONDICIONES):
            s = [r for r in filas if r["categoria"] == cat and r["condicion"] == c]
            M[i, j] = np.mean([int(r["resuelta_heldout"]) for r in s])
    fig, ax = plt.subplots(figsize=(3.5, 3.0))
    im = ax.imshow(M, cmap="Blues", vmin=0.5, vmax=1.0, aspect="auto")
    for i in range(len(categorias)):
        for j in range(len(CONDICIONES)):
            ax.text(j, i, f"{M[i, j]:.2f}".replace(".", ","), ha="center", va="center", fontsize=6,
                    color="white" if M[i, j] > 0.8 else "black")
    ax.set_xticks(range(len(CONDICIONES)), CONDICIONES)
    ax.set_yticks(range(len(categorias)), [c.replace("_", "-") for c in categorias], fontsize=6)
    ax.set_title("Exploratorio: tasa por categoría (ambos modelos)", fontsize=8)
    fig.colorbar(im, ax=ax, fraction=0.04)
    fig.tight_layout()
    fig.savefig(FIG / "categorias.pdf")
    plt.close(fig)


def figura_tokens(llamadas: dict[tuple, dict]) -> None:
    datos = []
    for c in CONDICIONES:
        tot = [v["entrada"] + v["salida"] + v["razonamiento"] for k, v in llamadas.items() if k[1] == c]
        datos.append(tot)
    fig, ax = plt.subplots(figsize=(3.5, 2.2))
    ax.boxplot(datos, tick_labels=CONDICIONES, showfliers=True, flierprops={"markersize": 2})
    ax.set_ylabel("Tokens por episodio")
    ax.set_title("Tokens por episodio (todas las llamadas, ambos modelos)", fontsize=8)
    fig.tight_layout()
    fig.savefig(FIG / "tokens.pdf")
    plt.close(fig)


def tabla_h1(res: dict) -> None:
    p = res["pooled"]
    L = ["\\begin{tabular}{lccc}", "\\toprule",
         "Comparación & Diferencia & IC95\\% & p (Holm) \\\\", "\\midrule"]
    L.append(f"C $-$ B (primaria) & {tex(p['C-B']['media'], signo=True)} & "
             f"[{tex(p['C-B']['ic_lo'], signo=True)}; {tex(p['C-B']['ic_hi'], signo=True)}] & --- \\\\")
    for k, nombre in (("C-A", "C $-$ A"), ("B-A", "B $-$ A")):
        L.append(f"{nombre} & {tex(p[k]['media'], signo=True)} & "
                 f"[{tex(p[k]['ic_lo'], signo=True)}; {tex(p[k]['ic_hi'], signo=True)}] & "
                 f"{tex(p[k]['p_holm'], 3)} \\\\")
    L += ["\\bottomrule", "\\end{tabular}"]
    (TAB / "h1.tex").write_text("\n".join(L) + "\n", encoding="utf-8")


def tabla_pass(comp: dict) -> None:
    modelos = sorted({k.split("|")[0] for k in comp["pass_k"]})
    L = ["\\begin{tabular}{llccc}", "\\toprule",
         "Modelo & Cond. & pass@1 & pass@2 & pass@4 \\\\", "\\midrule"]
    for m in modelos:
        nombre = m.replace("opencode-go/", "")
        for c in CONDICIONES:
            celdas = [tex(comp["pass_k"][f"{m}|{c}|{k}"]["media"]) for k in (1, 2, 4)]
            L.append(f"{nombre} & {c} & " + " & ".join(celdas) + " \\\\")
        if m != modelos[-1]:
            L.append("\\midrule")
    L += ["\\bottomrule", "\\end{tabular}"]
    (TAB / "pass.tex").write_text("\n".join(L) + "\n", encoding="utf-8")


def tabla_costo(comp: dict) -> None:
    L = ["\\begin{tabular}{lccccc}", "\\toprule",
         "Cond. & Tokens (med.) & Razon. (med.) & Iter. (media) & Coste (USD) & USD/resuelta \\\\", "\\midrule"]
    it = comp["iteraciones"]
    for c in CONDICIONES:
        iters = [v for k, v in it.items() if k.endswith("|" + c)]
        media_it = np.mean([v["media"] for v in iters])
        t = comp["tokens"]
        L.append(f"{c} & {t[c + '|total']['mediana']:.0f} & {t[c + '|razonamiento']['mediana']:.0f} & "
                 f"{tex(media_it, 3)} & {tex(comp['costo'][c]['coste_usd'], 3)} & "
                 f"{tex(comp['costo'][c]['usd_por_resuelta'], 5)} \\\\")
    L += ["\\bottomrule", "\\end{tabular}"]
    (TAB / "costo.tex").write_text("\n".join(L) + "\n", encoding="utf-8")


def tabla_h3(h3: dict) -> None:
    t = h3["totales"]
    L = ["\\begin{tabular}{lc}", "\\toprule", "Medida & Valor \\\\", "\\midrule",
         f"Mutantes generados & {t['mutantes']} \\\\",
         f"Equivalentes excluidos & {t['equivalentes']} \\\\",
         f"No equivalentes evaluados & {t['no_equivalentes']} \\\\",
         f"Puntuación de la suite de C & {tex(h3['puntuacion_C'])} \\\\",
         f"Línea base de B (solo ejecución) & {tex(h3['puntuacion_B'])} \\\\",
         f"Diferencia C $-$ B [IC95\\%] & {tex(h3['diferencia'], signo=True)} "
         f"[{tex(h3['ic_lo'], signo=True)}; {tex(h3['ic_hi'], signo=True)}] \\\\",
         "\\bottomrule", "\\end{tabular}"]
    (TAB / "h3.tex").write_text("\n".join(L) + "\n", encoding="utf-8")


def main() -> int:
    FIG.mkdir(parents=True, exist_ok=True)
    TAB.mkdir(parents=True, exist_ok=True)
    filas = cargar()
    res = json.loads(SALIDA_JSON.read_text(encoding="utf-8"))
    comp = res["complementarias"]
    rng = np.random.default_rng(SEED_FIG)
    figura_tasas(filas, rng)
    figura_diferencias(res)
    figura_categorias(filas)
    figura_tokens(cargar_llamadas())
    tabla_h1(res)
    tabla_pass(comp)
    tabla_costo(comp)
    h3 = h3_datos()
    if h3:
        tabla_h3(h3)
    print("figuras:", sorted(p.name for p in FIG.glob("*.pdf")))
    print("tablas:", sorted(p.name for p in TAB.glob("*.tex")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
