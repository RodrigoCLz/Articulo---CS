import pytest
import csv
import json

from analisis.fijar_tope import fijar_tope, resumir


def _llamada(ent, sal, raz=0, lec=0, esc=0):
    return {"modelo": "m", "condicion": "C", "tokens_entrada": ent, "tokens_salida": sal,
            "tokens_razonamiento": raz, "tokens_cache_lectura": lec, "tokens_cache_escritura": esc}


def test_tope_es_5_veces_q95_redondeado_a_miles():
    llamadas = [_llamada(1000, 0)] * 19 + [_llamada(2000, 0)]
    tope, q95 = fijar_tope(llamadas)
    assert q95 == pytest.approx(1050.0)
    assert tope == 6000


def test_resumen_detecta_razonamiento_nulo_y_truncados(tmp_path):
    llamadas = [_llamada(3000, 1500, raz=0), _llamada(3000, 1500, raz=200)]
    with open(tmp_path / "llamadas.jsonl", "w", encoding="utf-8") as f:
        for l in llamadas:
            f.write(json.dumps(l) + "\n")
    with open(tmp_path / "episodios.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["modelo", "condicion", "tokens_total", "coste_usd"])
        w.writeheader()
        w.writerow({"modelo": "m", "condicion": "C", "tokens_total": 9000, "coste_usd": 0.01})
    texto = resumir(tmp_path)
    assert "Tope por episodio T = 5 × q95" in texto
    assert "| m | C | 1 | 2 |" in texto
