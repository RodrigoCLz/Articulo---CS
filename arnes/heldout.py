"""Suite reservada (PREREGISTRO §8, D-11).

Diferencias con las pruebas del bucle:
- semilla y número de shots distintos en las tareas de distribución;
- en las tareas de QFT, una referencia independiente: la DFT (con bit-reversal si no hay swaps),
  calculada a partir de su definición matemática y no del circuito de referencia.
Las tareas variacionales y QAOA no tienen referencia independiente; se evalúan con la referencia
de la tarea, marcadas como "sin referencia independiente" (limitación declarada).
"""

from __future__ import annotations

import numpy as np
from qiskit.quantum_info import Operator

from arnes.evaluador import ErrorCodigo, cargar_codigo, evaluar
from arnes.verificacion import Resultado, equivalencia_unitarias
from tareas.catalogo import Tarea

SEED_RESERVADA = 424242
SHOTS_RESERVADA = 16384

# id -> (qubits, con swaps, inversa)
_QFT = {
    "E1": (2, True, False),
    "E2": (2, False, False),
    "E3": (3, True, False),
    "E4": (4, True, True),
    "E5": (6, True, False),
}


def _dft(n: int, inversa: bool) -> np.ndarray:
    N = 2**n
    signo = -1 if inversa else 1
    j = np.arange(N)
    return np.exp(2j * np.pi * signo * np.outer(j, j) / N) / np.sqrt(N)


def _bit_reversal(n: int) -> np.ndarray:
    N = 2**n
    P = np.zeros((N, N))
    for j in range(N):
        P[int(format(j, f"0{n}b")[::-1], 2), j] = 1
    return P


def referencia_independiente(tarea_id: str) -> np.ndarray | None:
    if tarea_id not in _QFT:
        return None
    n, swaps, inversa = _QFT[tarea_id]
    U = _dft(n, inversa)
    return U if swaps else _bit_reversal(n) @ U


def evaluar_heldout(tarea: Tarea, codigo: str) -> Resultado:
    try:
        circuito = cargar_codigo(codigo)
    except ErrorCodigo as e:
        return Resultado("reservada", False, f"el código falló al ejecutarse: {e}")
    if circuito.num_qubits != tarea.n_qubits:
        return Resultado("reservada", False, f"el circuito tiene {circuito.num_qubits} qubits; se esperaban {tarea.n_qubits}")
    if tarea.criterio == "unitaria":
        if any(i.operation.name == "measure" for i in circuito.data):
            return Resultado("reservada", False, "el circuito contiene medidas")
        ref = referencia_independiente(tarea.id)
        if ref is not None:
            r = equivalencia_unitarias(ref, Operator(circuito).data)
            return Resultado("reservada", r.aprobada, f"referencia independiente: {r.detalle}", r.valor)
        r = evaluar(tarea, circuito, seed=SEED_RESERVADA)
        return Resultado("reservada", r.aprobada, f"sin referencia independiente: {r.detalle}", r.valor)
    r = evaluar(tarea, circuito, seed=SEED_RESERVADA, shots=SHOTS_RESERVADA)
    return Resultado("reservada", r.aprobada, r.detalle, r.valor)
