"""Transporte HTTP hacia OpenCode Go (PREREGISTRO §5, D-32).

Rutas y parámetros según la documentación de OpenCode Go y el catálogo público de modelos
(consultados el 2026-11-21):
- gpt-6-luna: API Responses, POST {BASE}/openai/v1/responses, reasoning.effort = medium.
- claude-haiku-5-5: API Messages, POST {BASE}/anthropic/v1/messages, thinking adaptive +
  output_config.effort = medium. Sin temperature: ninguno de los dos modelos la acepta
  (verificado: GPT-6 Luna devuelve HTTP 400 y Haiku 5.5 no la admite en la documentación).

Lo que NO está verificado con una llamada real queda marcado [VERIFICAR] y se confirma con la
llamada de comprobación (arnes/comprobar.py) antes del piloto.

La clave se lee solo de la variable de entorno OPENCODE_GO_API_KEY. Nunca se escribe en disco.
"""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
import uuid

from arnes.cliente import MODELOS, Respuesta

BASE = "https://opencode.ai/inference/go"
USER_AGENT = "articulo-arnes/0.1"
VAR_CLAVE = "OPENCODE_GO_API_KEY"
TIMEOUT_S = 300
MAX_SALIDA = 8192


class ClaveAusente(RuntimeError):
    pass


class ErrorHTTP(RuntimeError):
    pass


def _clave() -> str:
    clave = os.environ.get(VAR_CLAVE, "")
    if not clave:
        raise ClaveAusente(f"define la variable de entorno {VAR_CLAVE}")
    return clave


class TransporteOpenCodeGo:
    """Una instancia por episodio: comparten la misma cabecera x-opencode-session."""

    def __init__(self, sesion: str | None = None, timeout: int = TIMEOUT_S):
        self.sesion = sesion or f"ses_{uuid.uuid4().hex}"
        self.timeout = timeout

    def contar_tokens(self, modelo: str, prompt: str) -> int:
        # Estimación conservadora (≈3 caracteres por token). El conteo exacto de la API
        # se registra después de cada llamada con usage.
        return -(-len(prompt) // 3)

    def _post(self, url: str, cabeceras: dict, cuerpo: dict) -> dict:
        datos = json.dumps(cuerpo).encode("utf-8")
        cab = {"content-type": "application/json", "user-agent": USER_AGENT, "x-opencode-session": self.sesion}
        cab.update(cabeceras)
        req = urllib.request.Request(url, data=datos, headers=cab, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            raise ErrorHTTP(f"HTTP {e.code}: {e.read().decode('utf-8', 'replace')[:500]}") from e

    def enviar(self, modelo: str, variante: str, prompt: str) -> Respuesta:
        if modelo == MODELOS[0]:
            return self._responses(modelo.split("/", 1)[1], variante, prompt)
        if modelo == MODELOS[1]:
            return self._messages(modelo.split("/", 1)[1], variante, prompt)
        raise ValueError(modelo)

    def _responses(self, nombre: str, variante: str, prompt: str) -> Respuesta:
        clave = _clave()
        cuerpo = {
            "model": nombre,
            "input": prompt,
            "reasoning": {"effort": variante},
            "max_output_tokens": MAX_SALIDA,
        }
        d = self._post(f"{BASE}/openai/v1/responses", {"authorization": f"Bearer {clave}"}, cuerpo)
        texto = d.get("output_text")
        if texto is None:
            partes = []
            for item in d.get("output", []):
                for c in item.get("content", []) or []:
                    if c.get("type") == "output_text":
                        partes.append(c.get("text", ""))
            texto = "".join(partes)
        u = d.get("usage", {})
        det_out = u.get("output_tokens_details", {}) or {}
        det_in = u.get("input_tokens_details", {}) or {}
        return Respuesta(
            texto=texto,
            tokens_entrada=u.get("input_tokens", 0) - det_in.get("cached_tokens", 0),
            tokens_salida=u.get("output_tokens", 0),
            tokens_razonamiento=det_out.get("reasoning_tokens", 0),
            tokens_cache_lectura=det_in.get("cached_tokens", 0),
            tokens_cache_escritura=0,
            parametros_ignorados=("temperature",),
        )

    def _messages(self, nombre: str, variante: str, prompt: str) -> Respuesta:
        clave = _clave()
        cuerpo = {
            "model": nombre,
            "max_tokens": MAX_SALIDA,
            "thinking": {"type": "adaptive"},
            "output_config": {"effort": variante},
            "messages": [{"role": "user", "content": prompt}],
        }
        cab = {"x-api-key": clave, "anthropic-version": "2023-06-01"}
        d = self._post(f"{BASE}/anthropic/v1/messages", cab, cuerpo)
        texto = "".join(b.get("text", "") for b in d.get("content", []) if b.get("type") == "text")
        u = d.get("usage", {})
        det = u.get("output_tokens_details", {}) or {}
        return Respuesta(
            texto=texto,
            tokens_entrada=u.get("input_tokens", 0),
            tokens_salida=u.get("output_tokens", 0),
            tokens_razonamiento=det.get("thinking_tokens", 0),
            tokens_cache_lectura=u.get("cache_read_input_tokens", 0),
            tokens_cache_escritura=u.get("cache_creation_input_tokens", 0),
            parametros_ignorados=("temperature",) if nombre == "claude-haiku-5-5" else (),
        )
