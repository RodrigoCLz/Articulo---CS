"""Generador determinista de mutantes (PREREGISTRO §9, D-12).

Familias del bucle de C: cambiar_compuerta, alterar_angulo.
Familias reservadas para H3: eliminar_compuerta, intercambiar_qubits, anadir_compuerta.
Las dos familias no se mezclan en ninguna prueba.
"""

from __future__ import annotations

import random
from dataclasses import dataclass

from qiskit import QuantumCircuit
from qiskit.circuit.library import get_standard_gate_name_mapping
from qiskit.quantum_info import Operator

from arnes.verificacion import MAX_QUBITS_EQUIVALENCIA, equivalencia_unitarias

FAMILIAS_BUCLE = ("cambiar_compuerta", "alterar_angulo")
FAMILIAS_H3 = ("eliminar_compuerta", "intercambiar_qubits", "anadir_compuerta")
CAMBIOS = {"h": "x", "x": "h", "z": "x", "s": "sdg", "sdg": "s", "t": "tdg", "tdg": "t", "cx": "cz", "cz": "cx"}
PARAMETRICAS = {"rx", "ry", "rz", "rzz", "cp"}
DOS_QUBITS = {"cx", "cz", "rzz", "cp"}
FACTORES = (0.5, 1.5, -1.0)
_GATES = get_standard_gate_name_mapping()


@dataclass(frozen=True)
class Mutante:
    id: str
    familia: str
    descripcion: str
    circuito: QuantumCircuit


def _ops(qc: QuantumCircuit) -> list[tuple]:
    return [
        (inst.operation, [qc.find_bit(q).index for q in inst.qubits])
        for inst in qc.data
    ]


def _construir(n: int, ops: list[tuple]) -> QuantumCircuit:
    out = QuantumCircuit(n)
    for op, idx in ops:
        out.append(op.copy(), [out.qubits[i] for i in idx])
    return out


def _candidatos(qc: QuantumCircuit) -> dict[str, list[tuple[str, list[tuple]]]]:
    base = _ops(qc)
    n = qc.num_qubits
    cand: dict[str, list[tuple[str, list[tuple]]]] = {f: [] for f in FAMILIAS_BUCLE + FAMILIAS_H3}

    for i, (op, idx) in enumerate(base):
        nombre = op.name
        if nombre in CAMBIOS:
            nuevo = base.copy()
            nuevo[i] = (_GATES[CAMBIOS[nombre]].copy(), idx)
            cand["cambiar_compuerta"].append(
                (f"compuerta {i}: {nombre} -> {CAMBIOS[nombre]} en {idx}", nuevo)
            )
        if nombre in PARAMETRICAS:
            for f in FACTORES:
                op2 = op.copy()
                op2.params = [op.params[0] * f] + list(op.params[1:])
                nuevo = base.copy()
                nuevo[i] = (op2, idx)
                cand["alterar_angulo"].append(
                    (f"compuerta {i}: {nombre} ángulo x {f} en {idx}", nuevo)
                )
        if nombre in DOS_QUBITS:
            nuevo = base.copy()
            nuevo[i] = (op, list(reversed(idx)))
            cand["intercambiar_qubits"].append(
                (f"compuerta {i}: {nombre} con qubits {idx} -> {list(reversed(idx))}", nuevo)
            )
        nuevo = base[:i] + base[i + 1:]
        cand["eliminar_compuerta"].append((f"elimina compuerta {i}: {nombre} en {idx}", nuevo))

    for i in range(len(base) + 1):
        for q in range(n):
            for g in ("x", "h"):
                nuevo = base[:i] + [(_GATES[g].copy(), [q])] + base[i:]
                cand["anadir_compuerta"].append((f"inserta {g} en qubit {q} en posición {i}", nuevo))
    return cand


def generar_mutantes(qc: QuantumCircuit, seed: int, por_familia: int) -> list[Mutante]:
    """Muestrea hasta `por_familia` mutantes por familia, con semilla fija.

    qc debe ser la referencia sin medidas. El orden y los ids son deterministas.
    """
    rng = random.Random(seed)
    cand = _candidatos(qc)
    salida: list[Mutante] = []
    for familia in FAMILIAS_BUCLE + FAMILIAS_H3:
        lista = cand[familia]
        k = min(por_familia, len(lista))
        elegidos = sorted(rng.sample(range(len(lista)), k))
        for j, pos in enumerate(elegidos):
            desc, ops = lista[pos]
            salida.append(
                Mutante(
                    id=f"{familia}-{j:02d}",
                    familia=familia,
                    descripcion=desc,
                    circuito=_construir(qc.num_qubits, ops),
                )
            )
    return salida


def clasificar(ref: QuantumCircuit, mut: QuantumCircuit) -> str:
    """'equivalente' si la unitaria coincide módulo fase global; 'no_equivalente' si no;
    'indeterminado' si hay más qubits que el límite de equivalencia."""
    if ref.num_qubits > MAX_QUBITS_EQUIVALENCIA:
        return "indeterminado"
    r = equivalencia_unitarias(Operator(ref).data, Operator(mut).data)
    return "equivalente" if r.aprobada else "no_equivalente"
