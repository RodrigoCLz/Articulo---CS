import numpy as np
import pytest
from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator

from arnes.verificacion import (
    ALPHA_PROGRAMA,
    alpha_bonferroni,
    chi_cuadrado,
    equivalencia_unitarias,
)


def test_equivalencia_acepta_fase_global():
    u = np.eye(2, dtype=complex)
    v = np.exp(1j * 0.7) * u
    assert equivalencia_unitarias(u, v).aprobada


def test_equivalencia_rz_frente_a_p_con_fase_global():
    qc_rz = QuantumCircuit(1)
    qc_rz.rz(0.9, 0)
    qc_p = QuantumCircuit(1)
    qc_p.p(0.9, 0)
    r = equivalencia_unitarias(Operator(qc_rz).data, Operator(qc_p).data)
    assert r.aprobada, r.detalle


def test_equivalencia_rechaza_compuerta_distinta():
    qc_x = QuantumCircuit(1)
    qc_x.x(0)
    qc_h = QuantumCircuit(1)
    qc_h.h(0)
    r = equivalencia_unitarias(Operator(qc_x).data, Operator(qc_h).data)
    assert not r.aprobada


def test_equivalencia_respeta_la_tolerancia():
    u = np.eye(2, dtype=complex)
    assert equivalencia_unitarias(u, u + 1e-9).aprobada
    assert not equivalencia_unitarias(u, u + 1e-6).aprobada


def test_equivalencia_rechaza_dimensiones_distintas():
    assert not equivalencia_unitarias(np.eye(2), np.eye(4)).aprobada


def test_equivalencia_rechaza_mas_de_8_qubits():
    d = 2**9
    r = equivalencia_unitarias(np.eye(d, dtype=complex), np.eye(d, dtype=complex))
    assert not r.aprobada
    assert "8 qubits" in r.detalle


def test_chi_cuadrado_acepta_distribucion_esperada():
    conteos = {"00": 2050, "01": 2050, "10": 2046, "11": 2046}
    probs = {"00": 0.25, "01": 0.25, "10": 0.25, "11": 0.25}
    assert chi_cuadrado(conteos, probs, 8192, ALPHA_PROGRAMA).aprobada


def test_chi_cuadrado_rechaza_distribucion_sesgada():
    conteos = {"00": 6000, "01": 500, "10": 900, "11": 792}
    probs = {"00": 0.25, "01": 0.25, "10": 0.25, "11": 0.25}
    r = chi_cuadrado(conteos, probs, 8192, ALPHA_PROGRAMA)
    assert not r.aprobada
    assert r.valor is not None and r.valor < ALPHA_PROGRAMA


def test_chi_cuadrado_agrupa_casillas_pequenas():
    probs = {"0": 0.5, "1": 0.5 - 1e-4, "2": 1e-4, "3": 0.0}
    conteos = {"0": 4100, "1": 4088, "2": 4, "3": 0}
    assert chi_cuadrado(conteos, probs, 8192, ALPHA_PROGRAMA).aprobada


def test_chi_cuadrado_exige_shots_consistentes():
    with pytest.raises(ValueError):
        chi_cuadrado({"0": 10}, {"0": 1.0}, 8192, ALPHA_PROGRAMA)


def test_chi_cuadrado_exige_probabilidades_normalizadas():
    with pytest.raises(ValueError):
        chi_cuadrado({"0": 4096, "1": 4096}, {"0": 0.5, "1": 0.4}, 8192, ALPHA_PROGRAMA)


def test_bonferroni_divide_por_numero_de_pruebas():
    assert alpha_bonferroni(4) == pytest.approx(0.0025)
    with pytest.raises(ValueError):
        alpha_bonferroni(0)
