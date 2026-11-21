"""Cliente de los modelos (PREREGISTRO §5, D-01, D-27, D-28).

Este módulo no llama a ningún modelo. El transporte HTTP no está implementado: el endpoint y
la forma de pasar la variante de razonamiento deben verificarse antes de la Fase 5 [VERIFICAR].
Las claves de API se leerán solo de variables de entorno cuando exista el transporte.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Protocol

MODELOS = ("opencode-go/gpt-6-luna", "opencode-go/claude-haiku-5-5")
VARIANTE = "medium"
LIMITE_CONTEXTO = 100_000


class ContextoExcedido(Exception):
    pass


class ModeloNoPermitido(Exception):
    pass


@dataclass(frozen=True)
class Respuesta:
    texto: str
    tokens_entrada: int
    tokens_salida: int
    tokens_razonamiento: int = 0
    tokens_cache_lectura: int = 0
    tokens_cache_escritura: int = 0
    parametros_ignorados: tuple[str, ...] = ()


class Transporte(Protocol):
    def contar_tokens(self, modelo: str, prompt: str) -> int: ...

    def enviar(self, modelo: str, variante: str, prompt: str) -> Respuesta: ...


class TransporteSinConfigurar:
    def contar_tokens(self, modelo: str, prompt: str) -> int:
        raise NotImplementedError("Transporte HTTP pendiente [VERIFICAR]")

    def enviar(self, modelo: str, variante: str, prompt: str) -> Respuesta:
        raise NotImplementedError("Transporte HTTP pendiente [VERIFICAR]")


@dataclass
class Registro:
    modelo: str
    variante: str
    hora_utc: str
    prompt: str
    respuesta: str
    tokens_entrada: int
    tokens_salida: int
    tokens_razonamiento: int
    tokens_cache_lectura: int
    tokens_cache_escritura: int
    parametros_ignorados: tuple[str, ...] = field(default_factory=tuple)


def llamar(transporte: Transporte, modelo: str, prompt: str, variante: str = VARIANTE) -> Registro:
    """Envía una llamada y devuelve su registro completo.

    Si el prompt supera LIMITE_CONTEXTO tokens, no se envía (D-27).
    """
    if modelo not in MODELOS:
        raise ModeloNoPermitido(modelo)
    contexto = transporte.contar_tokens(modelo, prompt)
    if contexto > LIMITE_CONTEXTO:
        raise ContextoExcedido(f"{contexto} tokens > {LIMITE_CONTEXTO}")
    hora = datetime.now(timezone.utc).isoformat(timespec="seconds")
    r = transporte.enviar(modelo, variante, prompt)
    return Registro(
        modelo=modelo,
        variante=variante,
        hora_utc=hora,
        prompt=prompt,
        respuesta=r.texto,
        tokens_entrada=r.tokens_entrada,
        tokens_salida=r.tokens_salida,
        tokens_razonamiento=r.tokens_razonamiento,
        tokens_cache_lectura=r.tokens_cache_lectura,
        tokens_cache_escritura=r.tokens_cache_escritura,
        parametros_ignorados=r.parametros_ignorados,
    )
