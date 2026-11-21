import csv

from arnes.cliente import Respuesta
from arnes.experimento import correr_experimento
from tareas.catalogo import por_id

CODIGO_OK = "```python\nfrom qiskit import QuantumCircuit\ndef build():\n    qc = QuantumCircuit(2)\n    qc.h(0)\n    qc.cx(0, 1)\n    return qc\n```"


class FakeTransporte:
    def contar_tokens(self, modelo, prompt):
        return 100

    def enviar(self, modelo, variante, prompt):
        return Respuesta(texto=CODIGO_OK, tokens_entrada=100, tokens_salida=50)


def test_corre_y_reanuda_sin_repetir(tmp_path):
    tareas = [por_id("A1")]
    mensajes = []
    r1 = correr_experimento(tareas=tareas, reps=1, salida=tmp_path, transporte_factory=FakeTransporte, log=mensajes.append)
    assert r1["nuevos"] == 6 and r1["previos"] == 0 and not r1["detenido"]
    with open(tmp_path / "episodios.csv", encoding="utf-8") as f:
        filas = list(csv.DictReader(f))
    assert len(filas) == 6
    assert all(f["resuelta_heldout"] == "1" for f in filas)
    assert (tmp_path / "metadatos.json").exists()

    r2 = correr_experimento(tareas=tareas, reps=1, salida=tmp_path, transporte_factory=FakeTransporte, log=mensajes.append)
    assert r2["nuevos"] == 0 and r2["previos"] == 6
    with open(tmp_path / "episodios.csv", encoding="utf-8") as f:
        assert len(list(csv.DictReader(f))) == 6


def test_progreso_se_muestra(tmp_path):
    mensajes = []
    correr_experimento(tareas=[por_id("A1")], reps=1, salida=tmp_path, transporte_factory=FakeTransporte, log=mensajes.append)
    assert mensajes[0].startswith("Episodios totales: 6")
    assert any(m.startswith("[6/6]") for m in mensajes)
