"""Llamada de comprobación: una petición mínima por modelo (D-32).

Sirve para confirmar, antes del piloto, que el endpoint, la cabecera de autenticación y el
parámetro de variante son aceptados. No mide nada del experimento.
"""

from __future__ import annotations

import os
import sys

from arnes.cliente import MODELOS, VARIANTE, llamar
from arnes.transporte import VAR_CLAVE, ErrorHTTP, TransporteOpenCodeGo


def main() -> int:
    if not os.environ.get(VAR_CLAVE):
        print(f"Falta la variable {VAR_CLAVE}.", file=sys.stderr)
        return 2
    t = TransporteOpenCodeGo()
    ok = True
    for modelo in MODELOS:
        try:
            r = llamar(t, modelo, "Reply with the single word OK.")
            print(f"{modelo}: OK variante={r.variante} tokens_in={r.tokens_entrada} "
                  f"tokens_out={r.tokens_salida} razonamiento={r.tokens_razonamiento} "
                  f"ignorados={list(r.parametros_ignorados)} respuesta={r.respuesta[:40]!r}")
        except (ErrorHTTP, NotImplementedError) as e:
            ok = False
            print(f"{modelo}: FALLO {e}", file=sys.stderr)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
