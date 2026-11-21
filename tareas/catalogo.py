"""Catálogo de 50 tareas propias (PREREGISTRO §4, D-15).

10 categorías × 5 tareas: 2 pequeñas (S), 2 medianas (M) y 1 grande (L).
Criterio "unitaria": el evaluador compara la unitaria completa, módulo fase global.
Criterio "distribucion": el evaluador mide todos los qubits y compara la distribución.
Sin llamadas a modelos. Los enunciados están en inglés (D-29).
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Callable

from qiskit import QuantumCircuit
from qiskit.synthesis.qft import synth_qft_full

CATEGORIAS = [
    "bell_ghz",
    "deutsch_jozsa",
    "bernstein_vazirani",
    "grover",
    "qft",
    "teleportacion",
    "superdense",
    "qpe",
    "variacional",
    "qaoa",
]
CRITERIOS = ("unitaria", "distribucion")


@dataclass(frozen=True)
class Tarea:
    id: str
    categoria: str
    tamano: str
    criterio: str
    enunciado: str
    construir: Callable[[], QuantumCircuit]

    @property
    def n_qubits(self) -> int:
        return self.construir().num_qubits


def _bell(psi_plus: bool = False) -> QuantumCircuit:
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    if psi_plus:
        qc.x(1)
    return qc


def _ghz(n: int) -> QuantumCircuit:
    qc = QuantumCircuit(n)
    qc.h(0)
    for i in range(n - 1):
        qc.cx(i, i + 1)
    return qc


def _dj(a: str, constante_uno: bool = False) -> QuantumCircuit:
    """Deutsch-Jozsa con f(x) = a·x mod 2. Con a = '0…0' la función es constante."""
    n = len(a)
    qc = QuantumCircuit(n + 1)
    qc.x(n)
    qc.h(list(range(n + 1)))
    for i, b in enumerate(a):
        if b == "1":
            qc.cx(i, n)
    if constante_uno:
        qc.x(n)
    qc.h(list(range(n)))
    return qc


def _bv(s: str) -> QuantumCircuit:
    n = len(s)
    qc = QuantumCircuit(n + 1)
    qc.x(n)
    qc.h(list(range(n + 1)))
    for i, b in enumerate(s):
        if b == "1":
            qc.cx(i, n)
    qc.h(list(range(n)))
    return qc


def _mcz(qc: QuantumCircuit, n: int) -> None:
    """Fase -1 sobre |1…1> de n qubits."""
    if n == 1:
        qc.z(0)
        return
    t = n - 1
    qc.h(t)
    qc.mcx(list(range(t)), t)
    qc.h(t)


def _grover(marcada: str, iteraciones: int) -> QuantumCircuit:
    n = len(marcada)
    qc = QuantumCircuit(n)
    qc.h(list(range(n)))
    for _ in range(iteraciones):
        ceros = [i for i, b in enumerate(marcada) if b == "0"]
        if ceros:
            qc.x(ceros)
        _mcz(qc, n)
        if ceros:
            qc.x(ceros)
        qc.h(list(range(n)))
        qc.x(list(range(n)))
        _mcz(qc, n)
        qc.x(list(range(n)))
        qc.h(list(range(n)))
    return qc


def _qft(n: int, swaps: bool = True, inversa: bool = False) -> QuantumCircuit:
    qc = QuantumCircuit(n)
    qc.compose(synth_qft_full(n, do_swaps=swaps, inverse=inversa), inplace=True)
    return qc


def _teleport(thetas: list[float], base_x: bool) -> QuantumCircuit:
    """Teleportación con correcciones diferidas (sin medidas intermedias).

    Cada copia usa 3 qubits: fuente (s), Alice (a) y Bob (b). Bob queda con ry(θ)|0>.
    Si base_x, Bob se mide en la base X (h antes de medir).
    """
    k = len(thetas)
    qc = QuantumCircuit(3 * k)
    for j, th in enumerate(thetas):
        s, a, b = 3 * j, 3 * j + 1, 3 * j + 2
        qc.ry(th, s)
        qc.h(a)
        qc.cx(a, b)
        qc.cx(s, a)
        qc.h(s)
        qc.cx(a, b)
        qc.cz(s, b)
        if base_x:
            qc.h(b)
    return qc


def _superdense(mensaje: str) -> QuantumCircuit:
    """Codificación densa. Cada pareja del mensaje es (b1, b0): b1 → X, b0 → Z.

    Tras la decodificación, el qubit a = b0 y el qubit b = b1.
    """
    k = len(mensaje) // 2
    qc = QuantumCircuit(2 * k)
    for j in range(k):
        a, b = 2 * j, 2 * j + 1
        qc.h(a)
        qc.cx(a, b)
        if mensaje[2 * j + 1] == "1":
            qc.z(a)
        if mensaje[2 * j] == "1":
            qc.x(a)
        qc.cx(a, b)
        qc.h(a)
    return qc


def _qpe(t: int, k: int) -> QuantumCircuit:
    """Estimación de fase de P(2πk/2^t) sobre |1>, con t qubits de contador."""
    qc = QuantumCircuit(t + 1)
    qc.x(t)
    qc.h(list(range(t)))
    for j in range(t):
        qc.cp(2 * math.pi * k * 2**j / 2**t, j, t)
    qc.compose(synth_qft_full(t, do_swaps=True, inverse=True), qubits=list(range(t)), inplace=True)
    return qc


def _variacional(n: int, capas: int) -> QuantumCircuit:
    qc = QuantumCircuit(n)
    for capa in range(capas):
        for q in range(n):
            idx = capa * n + q + 1
            qc.ry(0.1 * idx, q)
            qc.rz(0.2 * idx, q)
        if n > 1:
            for q in range(n - 1):
                qc.cx(q, q + 1)
    return qc


def _qaoa(n: int, aristas: list[tuple[int, int]], gamma: float = 0.4, beta: float = 0.3) -> QuantumCircuit:
    qc = QuantumCircuit(n)
    qc.h(list(range(n)))
    for i, j in aristas:
        qc.rzz(2 * gamma, i, j)
    for q in range(n):
        qc.rx(2 * beta, q)
    return qc


def _t(id_, cat, tam, crit, enun, fn) -> Tarea:
    return Tarea(id_, cat, tam, crit, enun, fn)


TAREAS: list[Tarea] = [
    # 1. Bell/GHZ
    _t("A1", "bell_ghz", "S", "distribucion",
       "Prepare the Bell state (|00> + |11>)/sqrt(2) on qubits 0 and 1.",
       lambda: _bell()),
    _t("A2", "bell_ghz", "S", "distribucion",
       "Prepare the state (|01> + |10>)/sqrt(2) on qubits 0 and 1.",
       lambda: _bell(True)),
    _t("A3", "bell_ghz", "M", "distribucion",
       "Prepare the 3-qubit GHZ state (|000> + |111>)/sqrt(2).",
       lambda: _ghz(3)),
    _t("A4", "bell_ghz", "M", "distribucion",
       "Prepare the 4-qubit GHZ state (|0000> + |1111>)/sqrt(2).",
       lambda: _ghz(4)),
    _t("A5", "bell_ghz", "L", "distribucion",
       "Prepare the 7-qubit GHZ state (|0000000> + |1111111>)/sqrt(2).",
       lambda: _ghz(7)),
    # 2. Deutsch-Jozsa
    _t("B1", "deutsch_jozsa", "S", "distribucion",
       "Deutsch-Jozsa with 1 input qubit and the balanced oracle f(x) = x. "
       "Use qubit 1 as the ancilla. The input register must end in |0> only if f is constant.",
       lambda: _dj("1")),
    _t("B2", "deutsch_jozsa", "S", "distribucion",
       "Deutsch-Jozsa with 1 input qubit and the constant oracle f(x) = 1. "
       "Use qubit 1 as the ancilla.",
       lambda: _dj("0", True)),
    _t("B3", "deutsch_jozsa", "M", "distribucion",
       "Deutsch-Jozsa with 3 input qubits (0, 1, 2) and ancilla qubit 3. "
       "The oracle is balanced: f(x) = x0 XOR x2.",
       lambda: _dj("101")),
    _t("B4", "deutsch_jozsa", "M", "distribucion",
       "Deutsch-Jozsa with 4 input qubits (0 to 3) and ancilla qubit 4. "
       "The oracle is constant f(x) = 0.",
       lambda: _dj("0000")),
    _t("B5", "deutsch_jozsa", "L", "distribucion",
       "Deutsch-Jozsa with 6 input qubits (0 to 5) and ancilla qubit 6. "
       "The oracle is balanced: f(x) = parity of all input bits.",
       lambda: _dj("111111")),
    # 3. Bernstein-Vazirani
    _t("C1", "bernstein_vazirani", "S", "distribucion",
       "Bernstein-Vazirani with 2 input qubits (0, 1) and ancilla qubit 2. "
       "The hidden string s is '01', meaning s_i multiplies input bit i. Recover s.",
       lambda: _bv("01")),
    _t("C2", "bernstein_vazirani", "S", "distribucion",
       "Bernstein-Vazirani with 1 input qubit (0) and ancilla qubit 1. "
       "The hidden string is s = '1'. Recover s.",
       lambda: _bv("1")),
    _t("C3", "bernstein_vazirani", "M", "distribucion",
       "Bernstein-Vazirani with 4 input qubits (0 to 3) and ancilla qubit 4. "
       "The hidden string is s = '1011' (s_i multiplies input bit i). Recover s.",
       lambda: _bv("1011")),
    _t("C4", "bernstein_vazirani", "M", "distribucion",
       "Bernstein-Vazirani with 5 input qubits (0 to 4) and ancilla qubit 5. "
       "The hidden string is s = '10101' (s_i multiplies input bit i). Recover s.",
       lambda: _bv("10101")),
    _t("C5", "bernstein_vazirani", "L", "distribucion",
       "Bernstein-Vazirani with 7 input qubits (0 to 6) and ancilla qubit 7. "
       "The hidden string is s = '1100110' (s_i multiplies input bit i). Recover s.",
       lambda: _bv("1100110")),
    # 4. Grover
    _t("D1", "grover", "S", "distribucion",
       "Grover search over 2 qubits with marked state |11>, using 1 iteration.",
       lambda: _grover("11", 1)),
    _t("D2", "grover", "S", "distribucion",
       "Grover search over 2 qubits with marked state qubit 0 = 1, qubit 1 = 0, using 1 iteration.",
       lambda: _grover("10", 1)),
    _t("D3", "grover", "M", "distribucion",
       "Grover search over 3 qubits with marked state |101> (qubit 0 = 1, qubit 1 = 0, qubit 2 = 1), using 2 iterations.",
       lambda: _grover("101", 2)),
    _t("D4", "grover", "M", "distribucion",
       "Grover search over 4 qubits with marked state qubit 0 = 1, qubit 1 = 0, qubit 2 = 1, qubit 3 = 0, using 3 iterations.",
       lambda: _grover("1010", 3)),
    _t("D5", "grover", "L", "distribucion",
       "Grover search over 5 qubits with marked state qubit 0 = 1, qubit 1 = 1, qubit 2 = 0, qubit 3 = 0, qubit 4 = 1, using 4 iterations.",
       lambda: _grover("11001", 4)),
    # 5. QFT
    _t("E1", "qft", "S", "unitaria",
       "Implement the 2-qubit Quantum Fourier Transform with the final bit-reversal swaps.",
       lambda: _qft(2, True)),
    _t("E2", "qft", "S", "unitaria",
       "Implement the 2-qubit Quantum Fourier Transform WITHOUT the final bit-reversal swaps.",
       lambda: _qft(2, False)),
    _t("E3", "qft", "M", "unitaria",
       "Implement the 3-qubit Quantum Fourier Transform with the final bit-reversal swaps.",
       lambda: _qft(3, True)),
    _t("E4", "qft", "M", "unitaria",
       "Implement the inverse 4-qubit Quantum Fourier Transform with the final bit-reversal swaps.",
       lambda: _qft(4, True, True)),
    _t("E5", "qft", "L", "unitaria",
       "Implement the 6-qubit Quantum Fourier Transform with the final bit-reversal swaps.",
       lambda: _qft(6, True)),
    # 6. Teleportación (correcciones diferidas)
    _t("F1", "teleportacion", "S", "distribucion",
       "Teleport the state ry(pi/3)|0> from qubit 0 to qubit 2, using qubit 1 as Alice's half of the Bell pair "
       "and deferred-measurement corrections (no mid-circuit measurements). Qubit 2 is the receiver. Measure in the Z basis.",
       lambda: _teleport([math.pi / 3], False)),
    _t("F2", "teleportacion", "S", "distribucion",
       "Teleport the state ry(2*pi/5)|0> from qubit 0 to qubit 2, using qubit 1 as Alice's half of the Bell pair "
       "and deferred-measurement corrections (no mid-circuit measurements). Qubit 2 is the receiver. Measure in the Z basis.",
       lambda: _teleport([2 * math.pi / 5], False)),
    _t("F3", "teleportacion", "M", "distribucion",
       "Teleport the state ry(pi/3)|0> from qubit 0 to qubit 2, using qubit 1 as Alice's half of the Bell pair "
       "and deferred-measurement corrections. Before measurement, apply a Hadamard to qubit 2 (X-basis measurement).",
       lambda: _teleport([math.pi / 3], True)),
    _t("F4", "teleportacion", "M", "distribucion",
       "Teleport the state ry(2*pi/5)|0> from qubit 0 to qubit 2, using qubit 1 as Alice's half of the Bell pair "
       "and deferred-measurement corrections. Before measurement, apply a Hadamard to qubit 2 (X-basis measurement).",
       lambda: _teleport([2 * math.pi / 5], True)),
    _t("F5", "teleportacion", "L", "distribucion",
       "Teleport three independent states ry(0.4)|0>, ry(0.9)|0>, ry(1.3)|0>, each from qubit 3j to qubit 3j+2 "
       "(j = 0, 1, 2), using qubit 3j+1 as Alice's half of each Bell pair. Use deferred-measurement corrections and "
       "measure every receiver in the X basis.",
       lambda: _teleport([0.4, 0.9, 1.3], True)),
    # 7. Superdense coding
    _t("G1", "superdense", "S", "distribucion",
       "Superdense coding of the 2-bit message 00 over one Bell pair (qubits 0 and 1). "
       "Qubit 0 is Alice's and is encoded locally; qubit 1 is Bob's and is decoded.",
       lambda: _superdense("00")),
    _t("G2", "superdense", "S", "distribucion",
       "Superdense coding of the 2-bit message 10 (first bit b1 = 1, second bit b0 = 0) over one Bell pair (qubits 0 and 1). "
       "Use b1 -> X and b0 -> Z on Alice's qubit 0, then decode on Bob's qubit 1.",
       lambda: _superdense("10")),
    _t("G3", "superdense", "M", "distribucion",
       "Superdense coding of the 4-bit message 1101 over two Bell pairs (qubits 0-1 and 2-3), "
       "two bits per pair in the order (b1, b0): pair 0 = 11, pair 1 = 01.",
       lambda: _superdense("1101")),
    _t("G4", "superdense", "M", "distribucion",
       "Superdense coding of the 6-bit message 011011 over three Bell pairs (qubits 0-1, 2-3, 4-5), "
       "two bits per pair in the order (b1, b0).",
       lambda: _superdense("011011")),
    _t("G5", "superdense", "L", "distribucion",
       "Superdense coding of the 8-bit message 10110100 over four Bell pairs (qubits 0-1, 2-3, 4-5, 6-7), "
       "two bits per pair in the order (b1, b0).",
       lambda: _superdense("10110100")),
    # 8. QPE
    _t("H1", "qpe", "S", "distribucion",
       "Quantum phase estimation of the phase unitary P(2*pi*k/2^t) with t = 2 counting qubits (0, 1), "
       "target qubit 2 prepared in |1>, and k = 1. Use the inverse QFT with final swaps.",
       lambda: _qpe(2, 1)),
    _t("H2", "qpe", "S", "distribucion",
       "Quantum phase estimation of P(2*pi*k/2^t) with t = 2 counting qubits (0, 1), "
       "target qubit 2 prepared in |1>, and k = 3. Use the inverse QFT with final swaps.",
       lambda: _qpe(2, 3)),
    _t("H3", "qpe", "M", "distribucion",
       "Quantum phase estimation of P(2*pi*k/2^t) with t = 3 counting qubits (0 to 2), "
       "target qubit 3 prepared in |1>, and k = 5. Use the inverse QFT with final swaps.",
       lambda: _qpe(3, 5)),
    _t("H4", "qpe", "M", "distribucion",
       "Quantum phase estimation of P(2*pi*k/2^t) with t = 4 counting qubits (0 to 3), "
       "target qubit 4 prepared in |1>, and k = 3. Use the inverse QFT with final swaps.",
       lambda: _qpe(4, 3)),
    _t("H5", "qpe", "L", "distribucion",
       "Quantum phase estimation of P(2*pi*k/2^t) with t = 6 counting qubits (0 to 5), "
       "target qubit 6 prepared in |1>, and k = 45. Use the inverse QFT with final swaps.",
       lambda: _qpe(6, 45)),
    # 9. Variacional
    _t("I1", "variacional", "S", "unitaria",
       "Implement the 1-qubit ansatz with 2 layers. In layer l (l = 0, 1), with idx = l + 1: apply ry(0.1*idx) "
       "then rz(0.2*idx) on qubit 0. There are no entangling gates.",
       lambda: _variacional(1, 2)),
    _t("I2", "variacional", "S", "unitaria",
       "Implement the 2-qubit ansatz with 1 layer. For each qubit q (q = 0, 1), with idx = q + 1: "
       "apply ry(0.1*idx) then rz(0.2*idx). Then apply cx(0, 1).",
       lambda: _variacional(2, 1)),
    _t("I3", "variacional", "M", "unitaria",
       "Implement the 3-qubit ansatz with 2 layers. In layer l (l = 0, 1), for each qubit q (0 to 2), with idx = 3*l + q + 1: "
       "apply ry(0.1*idx) then rz(0.2*idx). After each layer apply cx(0,1) and cx(1,2).",
       lambda: _variacional(3, 2)),
    _t("I4", "variacional", "M", "unitaria",
       "Implement the 4-qubit ansatz with 2 layers. In layer l (l = 0, 1), for each qubit q (0 to 3), with idx = 4*l + q + 1: "
       "apply ry(0.1*idx) then rz(0.2*idx). After each layer apply cx(0,1), cx(1,2) and cx(2,3).",
       lambda: _variacional(4, 2)),
    _t("I5", "variacional", "L", "unitaria",
       "Implement the 6-qubit ansatz with 3 layers. In layer l (l = 0, 1, 2), for each qubit q (0 to 5), with idx = 6*l + q + 1: "
       "apply ry(0.1*idx) then rz(0.2*idx). After each layer apply cx(q, q+1) for q = 0 to 4 in increasing order.",
       lambda: _variacional(6, 3)),
    # 10. QAOA (p = 1, gamma = 0.4, beta = 0.3)
    _t("J1", "qaoa", "S", "unitaria",
       "QAOA with p = 1 for MaxCut on the graph with 2 nodes and edge (0, 1). Use gamma = 0.4 and beta = 0.3. "
       "Apply H to all qubits, then rzz(2*gamma) on each edge, then rx(2*beta) on each qubit.",
       lambda: _qaoa(2, [(0, 1)])),
    _t("J2", "qaoa", "S", "unitaria",
       "QAOA with p = 1 for MaxCut on the path graph with 3 nodes and edges (0, 1) and (1, 2). Use gamma = 0.4 and beta = 0.3. "
       "Apply H to all qubits, then rzz(2*gamma) on each edge in the given order, then rx(2*beta) on each qubit.",
       lambda: _qaoa(3, [(0, 1), (1, 2)])),
    _t("J3", "qaoa", "M", "unitaria",
       "QAOA with p = 1 for MaxCut on the ring with 4 nodes and edges (0,1), (1,2), (2,3), (3,0). Use gamma = 0.4 and beta = 0.3. "
       "Apply H to all qubits, then rzz(2*gamma) on each edge in the given order, then rx(2*beta) on each qubit.",
       lambda: _qaoa(4, [(0, 1), (1, 2), (2, 3), (3, 0)])),
    _t("J4", "qaoa", "M", "unitaria",
       "QAOA with p = 1 for MaxCut on the complete graph K4 with edges (0,1), (0,2), (0,3), (1,2), (1,3), (2,3) in that order. "
       "Use gamma = 0.4 and beta = 0.3. Apply H to all qubits, then rzz(2*gamma) on each edge, then rx(2*beta) on each qubit.",
       lambda: _qaoa(4, [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)])),
    _t("J5", "qaoa", "L", "unitaria",
       "QAOA with p = 1 for MaxCut on the ring with 6 nodes and edges (0,1), (1,2), (2,3), (3,4), (4,5), (5,0) in that order. "
       "Use gamma = 0.4 and beta = 0.3. Apply H to all qubits, then rzz(2*gamma) on each edge, then rx(2*beta) on each qubit.",
       lambda: _qaoa(6, [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 0)])),
]


def por_id(id_: str) -> Tarea:
    for t in TAREAS:
        if t.id == id_:
            return t
    raise KeyError(id_)


def enunciado_completo(t: Tarea) -> str:
    if t.criterio == "unitaria":
        cierre = (
            "The evaluator compares the full unitary of your circuit with the reference, up to a global phase. "
            "Do not add measurements."
        )
    else:
        cierre = (
            "The evaluator appends a measurement of every qubit in the computational basis and compares the "
            "output distribution with the reference. Do not add measurements."
        )
    return (
        f"{t.enunciado}\n\n"
        f"Define `build()` that returns a qiskit.QuantumCircuit with exactly {t.n_qubits} qubits. "
        f"Use the Qiskit 2.x API. {cierre}"
    )
