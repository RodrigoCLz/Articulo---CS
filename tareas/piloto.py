"""Cinco tareas del piloto, fuera del conjunto de 50 (D-26, PREREGISTRO §13).

No entran en el análisis confirmatorio. Sirven para medir coste por llamada, errores del arnés
y el tope de tokens (D-02). Mismo formato que las tareas del catálogo.
"""

from __future__ import annotations

from qiskit import QuantumCircuit

from tareas.catalogo import Tarea


def _mas() -> QuantumCircuit:
    qc = QuantumCircuit(1)
    qc.h(0)
    return qc


def _s_h() -> QuantumCircuit:
    qc = QuantumCircuit(1)
    qc.s(0)
    qc.h(0)
    return qc


def _toffoli() -> QuantumCircuit:
    qc = QuantumCircuit(3)
    qc.x(0)
    qc.x(1)
    qc.ccx(0, 1, 2)
    return qc


def _swap_3cx() -> QuantumCircuit:
    qc = QuantumCircuit(2)
    qc.cx(0, 1)
    qc.cx(1, 0)
    qc.cx(0, 1)
    return qc


def _capa_cz() -> QuantumCircuit:
    qc = QuantumCircuit(5)
    qc.h(range(5))
    for i in range(4):
        qc.cz(i, i + 1)
    return qc


PILOTO: list[Tarea] = [
    Tarea("P1", "piloto_h", "S", "distribucion",
          "Prepare the state |+> = (|0> + |1>)/sqrt(2) on qubit 0.",
          _mas),
    Tarea("P2", "piloto_sh", "S", "unitaria",
          "Apply S and then H to qubit 0, in that order.",
          _s_h),
    Tarea("P3", "piloto_toffoli", "M", "distribucion",
          "Prepare |110> on qubits 0, 1, 2 (X on qubits 0 and 1) and then apply a Toffoli gate with controls 0 and 1 and target 2.",
          _toffoli),
    Tarea("P4", "piloto_swap", "M", "unitaria",
          "Implement the SWAP of qubits 0 and 1 using exactly three CNOT gates.",
          _swap_3cx),
    Tarea("P5", "piloto_cadena_cz", "L", "distribucion",
          "Apply H to each of the 5 qubits, then apply CZ(i, i+1) for i = 0 to 3 in increasing order.",
          _capa_cz),
]
