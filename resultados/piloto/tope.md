# Tope de tokens (piloto)

Generado por `analisis/fijar_tope.py`. No editar a mano.

- Llamadas del piloto: 120. Episodios: 120.
- Tokens por llamada: mediana 322, q95 702, máximo 911.
- **Tope por episodio T = 5 × q95, redondeado a miles hacia arriba: 4000 tokens.**
- Coste del piloto a precio de lista: 0.0176 USD (control: 6 USD).

## Razonamiento por modelo y condición (D-28)

Llamadas con tokens de razonamiento > 0. Si es 0 en todas, `medium` no está actuando.

| Modelo | Condición | Llamadas con razonamiento | Llamadas |
|---|---|---|---|
| opencode-go/claude-haiku-5-5 | A | 6 | 20 |
| opencode-go/claude-haiku-5-5 | B | 5 | 20 |
| opencode-go/claude-haiku-5-5 | C | 5 | 20 |
| opencode-go/gpt-6-luna | A | 20 | 20 |
| opencode-go/gpt-6-luna | B | 20 | 20 |
| opencode-go/gpt-6-luna | C | 20 | 20 |

## Episodios que superarían T

| Modelo | Condición | Truncados con T |
|---|---|---|
| opencode-go/claude-haiku-5-5 | A | 0 |
| opencode-go/claude-haiku-5-5 | B | 0 |
| opencode-go/claude-haiku-5-5 | C | 0 |
| opencode-go/gpt-6-luna | A | 0 |
| opencode-go/gpt-6-luna | B | 0 |
| opencode-go/gpt-6-luna | C | 0 |
