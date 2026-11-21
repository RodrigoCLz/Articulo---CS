"""Pruebas del bucle de C: equivalencia de unitarias y chi-cuadrado de distribuciones.

Sin llamadas a modelos. Parámetros según PREREGISTRO §9 y §10:
- equivalencia de unitarias hasta 8 qubits, tolerancia 1e-8 módulo fase global;
- chi-cuadrado sobre distribuciones de salida con 8192 shots;
- α = 0,01 por programa, con corrección de Bonferroni por número de pruebas.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.stats import chisquare

TOL_IDEAL = 1e-8
ALPHA_PROGRAMA = 0.01
MIN_ESPERADO = 5.0
MAX_QUBITS_EQUIVALENCIA = 8


@dataclass(frozen=True)
class Resultado:
    nombre: str
    aprobada: bool
    detalle: str
    valor: float | None = None


def alpha_bonferroni(n_pruebas: int, alpha: float = ALPHA_PROGRAMA) -> float:
    if n_pruebas < 1:
        raise ValueError("n_pruebas debe ser al menos 1")
    return alpha / n_pruebas


def equivalencia_unitarias(
    u: np.ndarray, v: np.ndarray, tol: float = TOL_IDEAL
) -> Resultado:
    """Compara dos unitarias módulo fase global.

    La fase óptima es la que minimiza ||u - e^{iφ} v||_F; su valor cerrado es
    tr(v†u)/|tr(v†u)|. La distancia resultante se compara con `tol`.
    """
    if u.shape != v.shape or u.ndim != 2 or u.shape[0] != u.shape[1]:
        return Resultado("equivalencia", False, f"dimensiones distintas: {u.shape} y {v.shape}")
    dim = u.shape[0]
    n_qubits = int(round(np.log2(dim)))
    if 2**n_qubits != dim or n_qubits > MAX_QUBITS_EQUIVALENCIA:
        return Resultado(
            "equivalencia",
            False,
            f"dimensión {dim} fuera del límite de {MAX_QUBITS_EQUIVALENCIA} qubits",
        )
    traza = np.trace(v.conj().T @ u)
    fase = traza / abs(traza) if abs(traza) > 0 else 1.0
    distancia = float(np.linalg.norm(u - fase * v))
    aprobada = distancia <= tol
    return Resultado(
        "equivalencia",
        aprobada,
        f"distancia módulo fase global = {distancia:.3e} (tolerancia {tol:.0e})",
        valor=distancia,
    )


def chi_cuadrado(
    conteos: dict[str, int],
    probs_esperadas: dict[str, float],
    shots: int,
    alpha: float,
) -> Resultado:
    """Prueba de bondad de ajuste de conteos frente a una distribución esperada.

    Los casillas con frecuencia esperada menor que 5 se agrupan en una sola
    casilla "otros" para que la aproximación chi-cuadrado sea válida.
    """
    total = sum(conteos.values())
    if total != shots:
        raise ValueError(f"los conteos suman {total}, pero shots = {shots}")
    suma_p = sum(probs_esperadas.values())
    if abs(suma_p - 1.0) > 1e-9:
        raise ValueError(f"las probabilidades esperadas suman {suma_p}, no 1")

    claves = sorted(set(conteos) | set(probs_esperadas))
    obs, esp = [], []
    otros_obs, otros_esp = 0, 0.0
    for k in claves:
        e = probs_esperadas.get(k, 0.0) * shots
        o = conteos.get(k, 0)
        if e < MIN_ESPERADO:
            otros_obs += o
            otros_esp += e
        else:
            obs.append(o)
            esp.append(e)
    if otros_esp >= MIN_ESPERADO or (otros_esp > 0 and not obs):
        obs.append(otros_obs)
        esp.append(otros_esp)
    elif obs:
        i = int(np.argmin(esp))
        obs[i] += otros_obs
        esp[i] += otros_esp

    if len(obs) < 2:
        return Resultado(
            "distribucion",
            obs[0] == shots if obs else False,
            "una sola casilla con masa esperada",
        )

    esp_arr = np.asarray(esp, dtype=float)
    esp_arr = esp_arr * (shots / esp_arr.sum())
    if np.any(esp_arr < MIN_ESPERADO):
        return Resultado(
            "distribucion",
            False,
            "frecuencias esperadas insuficientes tras agrupar; no se puede aplicar chi-cuadrado",
        )
    estadistico, p = chisquare(np.asarray(obs, dtype=float), f_exp=esp_arr)
    aprobada = p >= alpha
    return Resultado(
        "distribucion",
        aprobada,
        f"chi2 = {estadistico:.3f}, p = {p:.3g}, alpha = {alpha:.3g}",
        valor=float(p),
    )
