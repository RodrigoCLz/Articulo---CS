"""Evaluador de circuitos candidatos (PREREGISTRO §8).

El código del modelo se ejecuta en un subproceso con tiempo límite, para que un error o un
bucle infinito no afecte al arnés. La misma función sirve para las pruebas del bucle y para
las reservadas: solo cambia la semilla del simulador (y, en la Fase 6, el conjunto de entradas).
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

from qiskit import QuantumCircuit, qpy, transpile
from qiskit.quantum_info import Operator, Statevector
from qiskit_aer import AerSimulator

from arnes.verificacion import (
    ALPHA_PROGRAMA,
    Resultado,
    chi_cuadrado,
    equivalencia_unitarias,
)
from tareas.catalogo import Tarea

SHOTS = 8192
TIMEOUT_S = 60

_RUNNER = """
import sys
from qiskit import qpy
ns = {}
exec(sys.stdin.read(), ns)
with open(sys.argv[1], "wb") as f:
    qpy.dump(ns["build"](), f)
"""


class ErrorCodigo(Exception):
    pass


def cargar_codigo(codigo: str, timeout: int = TIMEOUT_S) -> QuantumCircuit:
    """Ejecuta `codigo` en un subproceso, llama a build() y devuelve el circuito."""
    with tempfile.TemporaryDirectory() as tmp:
        salida = Path(tmp) / "circuito.qpy"
        try:
            proc = subprocess.run(
                [sys.executable, "-c", _RUNNER, str(salida)],
                input=codigo,
                capture_output=True,
                text=True,
                timeout=timeout,
            )
        except subprocess.TimeoutExpired as e:
            raise ErrorCodigo(f"tiempo límite de {timeout} s") from e
        if proc.returncode != 0:
            raise ErrorCodigo(proc.stderr.strip().splitlines()[-1] if proc.stderr.strip() else "error")
        with open(salida, "rb") as f:
            cargados = qpy.load(f)
    if len(cargados) != 1 or not isinstance(cargados[0], QuantumCircuit):
        raise ErrorCodigo("build() debe devolver un único QuantumCircuit")
    return cargados[0]


def _tiene_medidas(qc: QuantumCircuit) -> bool:
    return any(inst.operation.name == "measure" for inst in qc.data)


def evaluar(tarea: Tarea, circuito: QuantumCircuit, *, seed: int, shots: int = SHOTS) -> Resultado:
    """Compara un circuito con la referencia de la tarea.

    Criterio "unitaria": equivalencia de unitarias módulo fase global (tolerancia 1e-8).
    Criterio "distribucion": chi-cuadrado sobre conteos con AerSimulator y semilla `seed`.
    """
    ref = tarea.construir()
    if circuito.num_qubits != ref.num_qubits:
        return Resultado(
            "evaluacion", False,
            f"el circuito tiene {circuito.num_qubits} qubits; se esperaban {ref.num_qubits}",
        )
    try:
        if tarea.criterio == "unitaria":
            if _tiene_medidas(circuito):
                return Resultado("evaluacion", False, "el circuito contiene medidas")
            return equivalencia_unitarias(Operator(ref).data, Operator(circuito).data)
        probs = Statevector(ref).probabilities_dict()
        medido = circuito.copy()
        medido.measure_all()
        sim = AerSimulator(seed_simulator=seed)
        conteos = sim.run(transpile(medido, sim), shots=shots).result().get_counts()
        return chi_cuadrado(conteos, probs, shots, ALPHA_PROGRAMA)
    except Exception as e:
        return Resultado("evaluacion", False, f"error al evaluar: {e}")


def evaluar_codigo(tarea: Tarea, codigo: str, *, seed: int, shots: int = SHOTS) -> Resultado:
    try:
        circuito = cargar_codigo(codigo)
    except ErrorCodigo as e:
        return Resultado("ejecucion", False, str(e))
    return evaluar(tarea, circuito, seed=seed, shots=shots)


def mata_mutante(tarea: Tarea, mutante: QuantumCircuit, *, seed: int) -> bool:
    """Un mutante cuenta como detectado si la suite lo rechaza."""
    return not evaluar(tarea, mutante, seed=seed).aprobada
