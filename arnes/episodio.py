"""Episodio de una tarea en una condición (PREREGISTRO §3, §11, D-02, D-14, D-14b).

A: una pasada, sin retroalimentación.
B: reintentos con el error de ejecución; para cuando el código ejecuta y tiene el número de qubits correcto.
C: reintentos con las pruebas del bucle (evaluador con semilla del bucle); para cuando las pasa.

Al terminar, todas las condiciones se evalúan con la suite reservada (arnes/heldout.py).
Un episodio truncado (tope de tokens o contexto excedido) cuenta como no resuelto.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from arnes.cliente import ContextoExcedido, Registro, Transporte, llamar
from arnes.evaluador import ErrorCodigo, cargar_codigo, evaluar_codigo
from arnes.heldout import evaluar_heldout
from arnes.verificacion import Resultado
from tareas.catalogo import Tarea, enunciado_completo

CONDICIONES = ("A", "B", "C")
MAX_ITER = 5
_BLOQUE = re.compile(r"```(?:python)?\s*\n(.*?)```", re.S)


def extraer_codigo(texto: str) -> str:
    bloques = _BLOQUE.findall(texto)
    return bloques[-1] if bloques else texto


@dataclass
class Episodio:
    tarea_id: str
    condicion: str
    modelo: str
    iteraciones: int = 0
    resuelta_bucle: bool = False
    truncado: bool = False
    resuelta_heldout: bool = False
    tokens_total: int = 0
    codigo_final: str = ""
    detalle_heldout: str = ""
    registros: list[Registro] = field(default_factory=list)


def _retroalimentacion_b(tarea: Tarea, codigo: str) -> Resultado:
    try:
        qc = cargar_codigo(codigo)
    except ErrorCodigo as e:
        return Resultado("ejecucion", False, f"el código falló al ejecutarse: {e}")
    if qc.num_qubits != tarea.n_qubits:
        return Resultado("ejecucion", False, f"el circuito tiene {qc.num_qubits} qubits; se esperaban {tarea.n_qubits}")
    return Resultado("ejecucion", True, "ejecución correcta")


def ejecutar_episodio(
    tarea: Tarea,
    condicion: str,
    transporte: Transporte,
    modelo: str,
    *,
    tope_tokens: int,
    seed_bucle: int,
    max_iter: int = MAX_ITER,
) -> Episodio:
    if condicion not in CONDICIONES:
        raise ValueError(condicion)
    ep = Episodio(tarea_id=tarea.id, condicion=condicion, modelo=modelo)
    base = enunciado_completo(tarea)
    prompt = base
    limite = 1 if condicion == "A" else max_iter

    for _ in range(limite):
        try:
            reg = llamar(transporte, modelo, prompt)
        except ContextoExcedido:
            ep.truncado = True
            break
        ep.registros.append(reg)
        ep.iteraciones += 1
        ep.tokens_total += reg.tokens_entrada + reg.tokens_salida + reg.tokens_razonamiento
        codigo = extraer_codigo(reg.respuesta)
        ep.codigo_final = codigo
        if ep.tokens_total > tope_tokens:
            ep.truncado = True
            break
        if condicion == "A":
            break
        if condicion == "B":
            r = _retroalimentacion_b(tarea, codigo)
        else:
            r = evaluar_codigo(tarea, codigo, seed=seed_bucle)
        if r.aprobada:
            ep.resuelta_bucle = True
            break
        prompt = (
            f"{base}\n\nYour previous attempt failed this check: {r.detalle}\n"
            f"Previous code:\n```python\n{codigo}\n```\n"
            "Return the full corrected build() in a single ```python block."
        )

    if ep.truncado:
        ep.detalle_heldout = "episodio truncado; no resuelto"
        return ep
    if not ep.codigo_final:
        ep.detalle_heldout = "sin código"
        return ep
    final = evaluar_heldout(tarea, ep.codigo_final)
    ep.resuelta_heldout = final.aprobada
    ep.detalle_heldout = final.detalle
    return ep
