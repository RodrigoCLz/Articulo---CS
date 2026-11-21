import math
from collections import Counter

import pytest
from qiskit import QuantumCircuit
from qiskit.synthesis.qft import synth_qft_full
from qiskit.quantum_info import Operator, Statevector

from arnes.evaluador import evaluar, evaluar_codigo, mata_mutante
from arnes.verificacion import MAX_QUBITS_EQUIVALENCIA, equivalencia_unitarias
from tareas.catalogo import CATEGORIAS, TAREAS, enunciado_completo, por_id
from tareas.mutantes import FAMILIAS_BUCLE, FAMILIAS_H3, clasificar, generar_mutantes


def probs(qc):
    return Statevector(qc).probabilities_dict()


def marginal(p, qubit, n):
    """Probabilidad de que `qubit` valga 0 (Qiskit: el bit i es la posición n-1-i)."""
    return sum(v for k, v in p.items() if k[n - 1 - qubit] == "0")


def test_catalogo_50_tareas_10_categorias():
    assert len(TAREAS) == 50
    assert len({t.id for t in TAREAS}) == 50
    assert [c for c in CATEGORIAS] == sorted(set(CATEGORIAS), key=CATEGORIAS.index)
    por_cat = Counter(t.categoria for t in TAREAS)
    assert set(por_cat) == set(CATEGORIAS)
    assert all(v == 5 for v in por_cat.values())
    for cat in CATEGORIAS:
        tams = Counter(t.tamano for t in TAREAS if t.categoria == cat)
        assert tams == Counter({"S": 2, "M": 2, "L": 1}), cat


def test_unitarias_dentro_del_limite_de_equivalencia():
    for t in TAREAS:
        if t.criterio == "unitaria":
            assert t.n_qubits <= MAX_QUBITS_EQUIVALENCIA, t.id


def test_referencias_sin_medidas():
    for t in TAREAS:
        qc = t.construir()
        assert not any(i.operation.name == "measure" for i in qc.data), t.id


def test_enunciados_mencionan_el_numero_de_qubits():
    for t in TAREAS:
        assert f"exactly {t.n_qubits} qubits" in enunciado_completo(t), t.id


def test_deutsch_jozsa_distingue_constante_de_balanceada():
    for id_, constante in [("B1", False), ("B2", True), ("B3", False), ("B4", True), ("B5", False)]:
        t = por_id(id_)
        n = t.n_qubits - 1
        p = probs(t.construir())
        cero = sum(v for k, v in p.items() if k[-n:] == "0" * n)
        assert cero == pytest.approx(1.0 if constante else 0.0, abs=1e-9), id_


def test_bernstein_vazirani_recupera_la_cadena_oculta():
    for id_, s in [("C1", "01"), ("C2", "1"), ("C3", "1011"), ("C4", "10101"), ("C5", "1100110")]:
        t = por_id(id_)
        n = len(s)
        p = probs(t.construir())
        marg = Counter()
        for k, v in p.items():
            marg[k[-n:]] += v
        dom = max(marg, key=marg.get)
        assert marg[dom] == pytest.approx(1.0, abs=1e-9), id_
        assert all(dom[n - 1 - i] == s[i] for i in range(n)), id_


def test_grover_encuentra_el_estado_marcado():
    esperados = {"D1": ("11", 1.0), "D2": ("10", 1.0), "D3": ("101", 0.945), "D4": ("1010", None), "D5": ("11001", None)}
    for id_, (marcado, minimo) in esperados.items():
        t = por_id(id_)
        n = len(marcado)
        p = probs(t.construir())
        dom = max(p, key=p.get)
        assert all(dom[n - 1 - i] == marcado[i] for i in range(n)), id_
        if minimo is not None:
            assert p[dom] == pytest.approx(minimo, abs=1e-3), id_
        else:
            assert p[dom] > 0.9, id_


def test_qft_con_y_sin_swaps_son_tareas_distintas():
    e1, e2 = por_id("E1").construir(), por_id("E2").construir()
    assert not equivalencia_unitarias(Operator(e1).data, Operator(e2).data).aprobada
    ref = QuantumCircuit(2)
    ref.compose(synth_qft_full(2, do_swaps=True), inplace=True)
    assert equivalencia_unitarias(Operator(e1).data, Operator(ref).data).aprobada


def test_teleportacion_z_y_x():
    f1 = por_id("F1").construir()
    assert marginal(probs(f1), 2, 3) == pytest.approx(math.cos(math.pi / 6) ** 2, abs=1e-9)
    f3 = por_id("F3").construir()
    assert marginal(probs(f3), 2, 3) == pytest.approx((1 + math.sin(math.pi / 3)) / 2, abs=1e-9)


def test_superdense_decodifica_el_mensaje():
    for id_, msg in [("G1", "00"), ("G2", "10"), ("G3", "1101"), ("G4", "011011"), ("G5", "10110100")]:
        t = por_id(id_)
        p = probs(t.construir())
        dom = max(p, key=p.get)
        assert p[dom] == pytest.approx(1.0, abs=1e-9), id_
        n = t.n_qubits
        for j in range(n // 2):
            b1 = dom[n - 1 - (2 * j + 1)]
            b0 = dom[n - 1 - (2 * j)]
            assert (b1, b0) == (msg[2 * j], msg[2 * j + 1]), id_


def test_qpe_recupera_k():
    for id_, t_, k in [("H1", 2, 1), ("H2", 2, 3), ("H3", 3, 5), ("H4", 4, 3), ("H5", 6, 45)]:
        t = por_id(id_)
        p = probs(t.construir())
        dom = max(p, key=p.get)
        assert p[dom] == pytest.approx(1.0, abs=1e-9), id_
        valor = sum(int(dom[len(dom) - 1 - j]) * 2**j for j in range(t_))
        assert valor == k, id_


def test_mutantes_son_deterministas_y_cubren_las_familias():
    ref = por_id("I3").construir()
    a = generar_mutantes(ref, seed=7, por_familia=3)
    b = generar_mutantes(ref, seed=7, por_familia=3)
    assert [m.descripcion for m in a] == [m.descripcion for m in b]
    familias = {m.familia for m in a}
    assert familias == set(FAMILIAS_BUCLE) | set(FAMILIAS_H3)


def test_clasificacion_detecta_equivalencia_por_fase_global():
    ref = QuantumCircuit(1)
    ref.rz(0.9, 0)
    mut = QuantumCircuit(1)
    mut.p(0.9, 0)
    assert clasificar(ref, mut) == "equivalente"
    mut2 = QuantumCircuit(1)
    mut2.p(0.5, 0)
    assert clasificar(ref, mut2) == "no_equivalente"


def test_evaluador_acepta_solucion_correcta_y_rechaza_incorrecta():
    t = por_id("A1")
    buena = "from qiskit import QuantumCircuit\ndef build():\n    qc = QuantumCircuit(2)\n    qc.h(0)\n    qc.cx(0, 1)\n    return qc\n"
    mala = "from qiskit import QuantumCircuit\ndef build():\n    qc = QuantumCircuit(2)\n    qc.h(0)\n    return qc\n"
    assert evaluar_codigo(t, buena, seed=1).aprobada
    assert not evaluar_codigo(t, mala, seed=1).aprobada


def test_evaluador_reporta_errores_de_ejecucion():
    t = por_id("A1")
    r = evaluar_codigo(t, "def build():\n    raise RuntimeError('boom')\n", seed=1)
    assert not r.aprobada and r.nombre == "ejecucion"
    r = evaluar_codigo(t, "x = 1\n", seed=1)
    assert not r.aprobada


def test_evaluador_unitaria_con_fase_global():
    t = por_id("E1")
    codigo = (
        "from qiskit import QuantumCircuit\nfrom qiskit.circuit.library import QFT\n"
        "def build():\n    qc = QuantumCircuit(2)\n    qc.compose(QFT(2, do_swaps=True), inplace=True)\n    return qc\n"
    )
    assert evaluar_codigo(t, codigo, seed=1).aprobada
    sin_swaps = codigo.replace("do_swaps=True", "do_swaps=False")
    assert not evaluar_codigo(t, sin_swaps, seed=1).aprobada


def test_evaluador_rechaza_medidas_en_unitaria():
    t = por_id("E1")
    qc = t.construir()
    qc.measure_all()
    assert not evaluar(t, qc, seed=1).aprobada


def test_un_mutante_obvio_es_detectado():
    t = por_id("A1")
    sin_cx = QuantumCircuit(2)
    sin_cx.h(0)
    assert mata_mutante(t, sin_cx, seed=1)
    assert not mata_mutante(t, t.construir(), seed=1)
