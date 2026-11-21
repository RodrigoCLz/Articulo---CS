import numpy as np
import pytest
from qiskit.quantum_info import Operator

from arnes.cliente import (
    LIMITE_CONTEXTO,
    MODELOS,
    VARIANTE,
    ContextoExcedido,
    ModeloNoPermitido,
    Respuesta,
    TransporteSinConfigurar,
    llamar,
)
from arnes.episodio import ejecutar_episodio, extraer_codigo
from arnes.heldout import evaluar_heldout, referencia_independiente
from tareas.catalogo import TAREAS, por_id

CODIGO_A1_OK = "from qiskit import QuantumCircuit\ndef build():\n    qc = QuantumCircuit(2)\n    qc.h(0)\n    qc.cx(0, 1)\n    return qc\n"
CODIGO_A1_MAL = "from qiskit import QuantumCircuit\ndef build():\n    qc = QuantumCircuit(2)\n    qc.h(0)\n    return qc\n"
CODIGO_A1_ROTO = "def build(:\n"


def bloque(codigo):
    return f"Here is the code:\n```python\n{codigo}```\n"


class FakeTransporte:
    def __init__(self, respuestas, tokens_entrada=3000, tokens_salida=1500, contexto=None):
        self.respuestas = list(respuestas)
        self.tokens_entrada = tokens_entrada
        self.tokens_salida = tokens_salida
        self.contexto = contexto
        self.envios = []

    def contar_tokens(self, modelo, prompt):
        return self.contexto if self.contexto is not None else self.tokens_entrada

    def enviar(self, modelo, variante, prompt):
        self.envios.append((modelo, variante, prompt))
        texto = self.respuestas.pop(0) if len(self.respuestas) > 1 else self.respuestas[0]
        return Respuesta(texto=texto, tokens_entrada=self.tokens_entrada, tokens_salida=self.tokens_salida)


def test_llamada_usa_variante_medium_y_registra():
    t = FakeTransporte([bloque(CODIGO_A1_OK)])
    reg = llamar(t, MODELOS[0], "prompt")
    assert t.envios[0][1] == VARIANTE == "medium"
    assert reg.modelo == MODELOS[0] and reg.variante == "medium"
    assert reg.tokens_entrada == 3000 and reg.tokens_salida == 1500
    assert reg.hora_utc


def test_modelo_fuera_de_la_lista_no_se_envia():
    t = FakeTransporte([bloque(CODIGO_A1_OK)])
    with pytest.raises(ModeloNoPermitido):
        llamar(t, "otro/modelo", "prompt")
    assert t.envios == []


def test_contexto_mayor_de_100000_no_se_envia():
    t = FakeTransporte([bloque(CODIGO_A1_OK)], contexto=LIMITE_CONTEXTO + 1)
    with pytest.raises(ContextoExcedido):
        llamar(t, MODELOS[1], "prompt")
    assert t.envios == []


def test_transporte_sin_configurar_no_llama_a_nada():
    with pytest.raises(NotImplementedError):
        llamar(TransporteSinConfigurar(), MODELOS[0], "prompt")


def test_extraer_codigo_toma_el_ultimo_bloque():
    texto = "```python\nx=1\n```\ntexto\n```python\ny=2\n```"
    assert extraer_codigo(texto) == "y=2\n"


def test_condicion_a_una_sola_llamada():
    t = FakeTransporte([bloque(CODIGO_A1_OK)])
    ep = ejecutar_episodio(por_id("A1"), "A", t, MODELOS[0], tope_tokens=10**9, seed_bucle=1)
    assert ep.iteraciones == 1 and len(t.envios) == 1
    assert ep.resuelta_heldout and not ep.resuelta_bucle


def test_condicion_b_reintenta_tras_error_de_ejecucion():
    t = FakeTransporte([bloque(CODIGO_A1_ROTO), bloque(CODIGO_A1_OK)])
    ep = ejecutar_episodio(por_id("A1"), "B", t, MODELOS[0], tope_tokens=10**9, seed_bucle=1)
    assert ep.iteraciones == 2
    assert "previous attempt failed" in t.envios[1][2]
    assert ep.resuelta_heldout


def test_condicion_c_para_cuando_pasa_el_bucle():
    t = FakeTransporte([bloque(CODIGO_A1_MAL), bloque(CODIGO_A1_OK)])
    ep = ejecutar_episodio(por_id("A1"), "C", t, MODELOS[1], tope_tokens=10**9, seed_bucle=1)
    assert ep.iteraciones == 2 and ep.resuelta_bucle and ep.resuelta_heldout


def test_condicion_c_respeta_el_maximo_de_iteraciones():
    t = FakeTransporte([bloque(CODIGO_A1_MAL)])
    ep = ejecutar_episodio(por_id("A1"), "C", t, MODELOS[0], tope_tokens=10**9, seed_bucle=1, max_iter=3)
    assert ep.iteraciones == 3
    assert not ep.resuelta_bucle and not ep.resuelta_heldout


def test_tope_de_tokens_trunca_y_cuenta_como_no_resuelto():
    t = FakeTransporte([bloque(CODIGO_A1_MAL), bloque(CODIGO_A1_OK)])
    ep = ejecutar_episodio(por_id("A1"), "C", t, MODELOS[0], tope_tokens=4000, seed_bucle=1)
    assert ep.truncado and not ep.resuelta_heldout
    assert ep.iteraciones == 1


def test_contexto_excedido_trunca_el_episodio():
    t = FakeTransporte([bloque(CODIGO_A1_OK)], contexto=LIMITE_CONTEXTO + 5)
    ep = ejecutar_episodio(por_id("A1"), "B", t, MODELOS[0], tope_tokens=10**9, seed_bucle=1)
    assert ep.truncado and ep.iteraciones == 0 and not ep.resuelta_heldout


@pytest.mark.parametrize("id_", ["E1", "E2", "E3", "E4", "E5"])
def test_referencia_independiente_qft_coincide_con_el_circuito(id_):
    ref = por_id(id_).construir()
    U = referencia_independiente(id_)
    assert U is not None
    assert Operator(ref).data.shape == U.shape
    r = np.trace(U.conj().T @ Operator(ref).data)
    fase = r / abs(r)
    assert np.allclose(Operator(ref).data, fase * U, atol=1e-9)


def test_heldout_qft_distingue_con_y_sin_swaps():
    con = "from qiskit import QuantumCircuit\nfrom qiskit.synthesis.qft import synth_qft_full\ndef build():\n    qc = QuantumCircuit(2)\n    qc.compose(synth_qft_full(2, do_swaps=True), inplace=True)\n    return qc\n"
    sin = con.replace("do_swaps=True", "do_swaps=False")
    assert evaluar_heldout(por_id("E1"), con).aprobada
    assert not evaluar_heldout(por_id("E1"), sin).aprobada
    assert evaluar_heldout(por_id("E2"), sin).aprobada


def test_heldout_distribucion_acepta_solucion_correcta():
    assert evaluar_heldout(por_id("A1"), CODIGO_A1_OK).aprobada
    assert not evaluar_heldout(por_id("A1"), CODIGO_A1_MAL).aprobada


def test_catalogo_sin_referencia_independiente_se_declara():
    t = por_id("I1")
    assert referencia_independiente(t.id) is None
    assert len(TAREAS) == 50
