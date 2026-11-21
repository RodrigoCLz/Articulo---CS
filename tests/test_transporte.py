import io
import json

import pytest

from arnes import transporte as T
from arnes.cliente import MODELOS, Registro
from arnes.piloto import PRECIOS, coste_llamada
from tareas.piloto import PILOTO
from tareas.catalogo import TAREAS


class Respuesta_fake(io.BytesIO):
    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False


def fake_urlopen(capturas, cuerpo):
    def _open(req, timeout=None):
        capturas.append({"url": req.full_url, "headers": {k.lower(): v for k, v in req.header_items()},
                         "body": json.loads(req.data.decode("utf-8"))})
        return Respuesta_fake(json.dumps(cuerpo).encode("utf-8"))
    return _open


def test_sin_clave_no_envia_nada(monkeypatch):
    monkeypatch.delenv(T.VAR_CLAVE, raising=False)
    with pytest.raises(T.ClaveAusente):
        T.TransporteOpenCodeGo().enviar(MODELOS[0], "medium", "hola")


def test_responses_envia_ruta_y_esfuerzo_medium(monkeypatch):
    monkeypatch.setenv(T.VAR_CLAVE, "clave-de-prueba")
    capturas = []
    cuerpo = {"output_text": "OK", "usage": {"input_tokens": 12, "output_tokens": 5,
              "output_tokens_details": {"reasoning_tokens": 3}, "input_tokens_details": {"cached_tokens": 0}}}
    monkeypatch.setattr(T.urllib.request, "urlopen", fake_urlopen(capturas, cuerpo))
    r = T.TransporteOpenCodeGo(sesion="ses_x").enviar(MODELOS[0], "medium", "hola")
    c = capturas[0]
    assert c["url"] == "https://opencode.ai/inference/go/openai/v1/responses"
    assert c["body"]["model"] == "gpt-6-luna"
    assert c["body"]["reasoning"] == {"effort": "medium"}
    assert "temperature" not in c["body"]
    assert c["headers"]["authorization"] == "Bearer clave-de-prueba"
    assert c["headers"]["x-opencode-session"] == "ses_x"
    assert c["headers"]["user-agent"] == T.USER_AGENT
    assert r.texto == "OK" and r.tokens_razonamiento == 3 and r.tokens_salida == 5
    assert r.parametros_ignorados == ("temperature",)


def test_messages_usa_adaptive_y_sin_temperature(monkeypatch):
    monkeypatch.setenv(T.VAR_CLAVE, "clave-de-prueba")
    capturas = []
    cuerpo = {"content": [{"type": "thinking", "thinking": "..."}, {"type": "text", "text": "OK"}],
              "usage": {"input_tokens": 7, "output_tokens": 9, "cache_read_input_tokens": 100,
                        "cache_creation_input_tokens": 4}}
    monkeypatch.setattr(T.urllib.request, "urlopen", fake_urlopen(capturas, cuerpo))
    r = T.TransporteOpenCodeGo().enviar(MODELOS[1], "medium", "hola")
    c = capturas[0]
    assert c["url"] == "https://opencode.ai/inference/go/anthropic/v1/messages"
    assert c["body"]["thinking"] == {"type": "adaptive"}
    assert c["body"]["output_config"] == {"effort": "medium"}
    assert "temperature" not in c["body"]
    assert c["headers"]["x-api-key"] == "clave-de-prueba"
    assert r.texto == "OK"
    assert r.tokens_cache_lectura == 100 and r.tokens_cache_escritura == 4
    assert r.parametros_ignorados == ("temperature",)


def test_error_http_se_reporta(monkeypatch):
    monkeypatch.setenv(T.VAR_CLAVE, "clave-de-prueba")

    def _falla(req, timeout=None):
        import urllib.error
        raise urllib.error.HTTPError(req.full_url, 401, "Unauthorized", {}, io.BytesIO(b'{"error":"no"}'))
    monkeypatch.setattr(T.urllib.request, "urlopen", _falla)
    with pytest.raises(T.ErrorHTTP, match="HTTP 401"):
        T.TransporteOpenCodeGo().enviar(MODELOS[0], "medium", "hola")


def test_contar_tokens_es_conservador():
    t = T.TransporteOpenCodeGo()
    assert t.contar_tokens(MODELOS[0], "a" * 300) == 100


def _reg(modelo, ent, sal, lec=0, esc=0):
    return Registro(modelo, "medium", "t", "p", "r", ent, sal, 0, lec, esc)


def test_coste_tramo_base_y_alto_de_haiku():
    base = coste_llamada(_reg(MODELOS[1], 3000, 1500))
    assert base == pytest.approx((3000 * 0.10 + 1500 * 0.50) / 1e6)
    # Caso del registro de la sesión: 301 059 caché lectura, 334 escritura, 575 salida, 2 entrada.
    alto = coste_llamada(_reg(MODELOS[1], 2, 575, 301059, 334))
    assert alto == pytest.approx(0.0167, abs=0.0001)


def test_piloto_tiene_cinco_tareas_fuera_del_catalogo():
    ids_piloto = {t.id for t in PILOTO}
    ids_catalogo = {t.id for t in TAREAS}
    assert len(PILOTO) == 5
    assert ids_piloto.isdisjoint(ids_catalogo)
