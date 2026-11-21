# Articulo — PDF → Markdown

Convierte artículos PDF a Markdown limpio, con metadatos y figuras extraídas, para
gastar muchos menos tokens al leerlos.

## Uso

```bash
./convertir articulo.pdf            # busca en pdf/ (o pdf's/)
./convertir --all                   # todos los PDFs pendientes
./convertir --force articulo.pdf    # reconvierte
./convertir --reindex               # recalcula métricas e índice sin reconvertir
./convertir --resumen               # regenera resumen.md
./convertir --offline articulo.pdf  # sin consultar Crossref/OpenAlex
./convertir --no-images articulo.pdf
./convertir --verbose articulo.pdf  # muestra la salida interna
```

El nombre puede ser el del archivo (`articulo.pdf`) o una ruta completa.

## Salida

```
resumen.md                     tabla resumen (ID, título, autores, cuartil, citas, aporte)
aportes.json                   aportes principales editables por artículo
md/
├── _indice.md                  tabla resumen de toda la biblioteca
├── .cache/api.json             caché de Crossref/OpenAlex (30 días)
└── <nombre>/
    ├── <nombre>.md             cuerpo del artículo
    ├── <nombre>.meta.md        metadatos, métricas, abstract, keywords
    └── images/                 figuras (p03-01.png = página 3, figura 1)
```

## Metadatos

- Título, autores, año y venue: DOI → Crossref/OpenAlex (con respaldo en el PDF).
- DOI y arXiv: detectados en el texto.
- Abstract y palabras clave: extraídos del PDF; si fallan, de Crossref/OpenAlex.
- Citas recibidas: OpenAlex. Referencias: Crossref.
- Tokens estimados: caracteres / 4.
- Densidad matemática: símbolos matemáticos por 1000 palabras, ignorando código y tablas.
  Si supera 5 (alta), el `.meta.md` avisa de que conviene probar `marker-pdf`.

## Dependencias

El entorno está en `.venv/` (`pymupdf`, `pymupdf4llm`, `pymupdf_layout`).

```bash
python3 -m venv .venv
.venv/bin/pip install -U pip pymupdf pymupdf4llm pymupdf-layout
```
