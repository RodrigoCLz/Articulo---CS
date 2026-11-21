"""Ejecutor del experimento completo (Fase 6, PREREGISTRO §5, §12, D-02, D-36).

50 tareas × 3 condiciones × 2 modelos × 4 repeticiones = 1 200 episodios.

- Muestra progreso por episodio.
- Guarda cada episodio y cada llamada al terminarlos (no al final), así que una interrupción
  no pierde nada.
- Se puede reanudar: los episodios ya presentes en episodios.csv no se repiten.
- Se detiene si el coste acumulado supera el control de 6 USD (D-02).

Uso:  .venv/bin/python -m arnes.experimento
"""

from __future__ import annotations

import csv
import json
import os
import platform
import subprocess
import sys
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path

from arnes.cliente import MODELOS
from arnes.episodio import CONDICIONES, ejecutar_episodio
from arnes.piloto import SEED_BUCLE, TOPE_CONTROL_USD, coste_llamada
from arnes.transporte import VAR_CLAVE, ClaveAusente, TransporteOpenCodeGo
from tareas.catalogo import TAREAS

REPETICIONES = 4
TOPE_TOKENS = 20_000
SALIDA = Path(__file__).resolve().parent.parent / "resultados" / "experimento"
CAMPOS = [
    "tarea", "categoria", "tamano", "criterio", "condicion", "modelo", "repeticion",
    "iteraciones", "resuelta_bucle", "resuelta_heldout", "truncado", "tokens_total",
    "coste_usd", "detalle_heldout",
]


def _commit() -> str:
    try:
        return subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True, check=True).stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "desconocido"


def _metadatos(salida: Path) -> None:
    import qiskit
    import qiskit_aer

    datos = {
        "fecha_inicio_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "commit_arnes": _commit(),
        "python": platform.python_version(),
        "qiskit": qiskit.__version__,
        "qiskit_aer": qiskit_aer.__version__,
        "modelos": list(MODELOS),
        "variante": "medium",
        "repeticiones": REPETICIONES,
        "tope_tokens": TOPE_TOKENS,
        "tope_control_usd": TOPE_CONTROL_USD,
        "seed_bucle_base": SEED_BUCLE,
    }
    (salida / "metadatos.json").write_text(json.dumps(datos, indent=2, ensure_ascii=False), encoding="utf-8")


def _clave_de(fila: dict) -> tuple:
    return (fila["tarea"], fila["condicion"], fila["modelo"], int(fila["repeticion"]))


def correr_experimento(tareas=None, modelos=MODELOS, reps: int = REPETICIONES, salida: Path = SALIDA,
                       transporte_factory=TransporteOpenCodeGo, log=print) -> dict:
    tareas = TAREAS if tareas is None else tareas
    salida.mkdir(parents=True, exist_ok=True)
    ruta_ep = salida / "episodios.csv"
    ruta_ll = salida / "llamadas.jsonl"

    hechos = set()
    if ruta_ep.exists():
        with open(ruta_ep, encoding="utf-8") as f:
            hechos = {_clave_de(r) for r in csv.DictReader(f)}
    else:
        with open(ruta_ep, "w", newline="", encoding="utf-8") as f:
            csv.DictWriter(f, fieldnames=CAMPOS).writeheader()
        _metadatos(salida)

    total = len(tareas) * len(modelos) * len(CONDICIONES) * reps
    coste = 0.0
    hecho_nuevos = 0
    ya = len(hechos)
    log(f"Episodios totales: {total}. Ya guardados: {ya}. Pendientes: {total - ya}.")
    parado = False

    with open(ruta_ep, "a", newline="", encoding="utf-8") as fep, open(ruta_ll, "a", encoding="utf-8") as fll:
        escritor = csv.DictWriter(fep, fieldnames=CAMPOS)
        for tarea in tareas:
            for modelo in modelos:
                for condicion in CONDICIONES:
                    for rep in range(reps):
                        clave = (tarea.id, condicion, modelo, rep)
                        if clave in hechos:
                            continue
                        t = transporte_factory()
                        ep = ejecutar_episodio(
                            tarea, condicion, t, modelo,
                            tope_tokens=TOPE_TOKENS, seed_bucle=SEED_BUCLE + rep,
                        )
                        c_ep = 0.0
                        for reg in ep.registros:
                            c = coste_llamada(reg)
                            c_ep += c
                            fll.write(json.dumps({"tarea": tarea.id, "condicion": condicion, "rep": rep,
                                                  **asdict(reg), "coste_usd": c}, ensure_ascii=False) + "\n")
                        fll.flush()
                        coste += c_ep
                        escritor.writerow({
                            "tarea": tarea.id, "categoria": tarea.categoria, "tamano": tarea.tamano,
                            "criterio": tarea.criterio, "condicion": condicion, "modelo": modelo,
                            "repeticion": rep, "iteraciones": ep.iteraciones,
                            "resuelta_bucle": int(ep.resuelta_bucle), "resuelta_heldout": int(ep.resuelta_heldout),
                            "truncado": int(ep.truncado), "tokens_total": ep.tokens_total,
                            "coste_usd": round(c_ep, 6), "detalle_heldout": ep.detalle_heldout,
                        })
                        fep.flush()
                        hecho_nuevos += 1
                        log(f"[{ya + hecho_nuevos}/{total}] {tarea.id} {condicion} {modelo} rep={rep} "
                            f"it={ep.iteraciones} bucle={int(ep.resuelta_bucle)} "
                            f"heldout={int(ep.resuelta_heldout)} trunc={int(ep.truncado)} "
                            f"coste_acum={coste:.4f}")
                        if coste > TOPE_CONTROL_USD:
                            parado = True
                            log(f"DETENIDO: coste acumulado {coste:.2f} USD supera el control de {TOPE_CONTROL_USD} USD.")
                            break
                    if parado:
                        break
                if parado:
                    break
            if parado:
                break
    return {"nuevos": hecho_nuevos, "previos": ya, "total": total, "coste_usd": round(coste, 4), "detenido": parado}


if __name__ == "__main__":
    if not os.environ.get(VAR_CLAVE):
        raise SystemExit(f"Falta la variable {VAR_CLAVE}. No se ejecuta el experimento.")
    try:
        resumen = correr_experimento(log=lambda m: print(m, flush=True))
    except ClaveAusente as e:
        raise SystemExit(str(e))
    print(resumen, flush=True)
    sys.exit(0)
