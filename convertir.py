#!/usr/bin/env python3
"""convertir.py — Convierte un PDF a Markdown + metadatos.

Uso:
    ./convertir articulo.pdf
    ./convertir --all
    ./convertir --force articulo.pdf

Genera, por cada PDF:
    md/<stem>/<stem>.md        cuerpo limpio
    md/<stem>/<stem>.meta.md   metadatos, métricas, resumen, palabras clave
    md/<stem>/images/*.png     figuras extraídas
Y actualiza md/_indice.md con la tabla resumen de toda la biblioteca.
"""

from __future__ import annotations

import argparse
import contextlib
import io
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path
from typing import Any

import pymupdf
import pymupdf4llm

ROOT = Path(__file__).resolve().parent
OUT_ROOT = ROOT / "md"
INDEX_JSON = OUT_ROOT / ".indice.json"
INDEX_MD = OUT_ROOT / "_indice.md"
CACHE_DIR = OUT_ROOT / ".cache"
CACHE_PATH = CACHE_DIR / "api.json"
INPUT_CANDIDATES = ("pdf", "pdf's", "pdfs", "PDFs")
RESUMEN_PATH = ROOT / "resumen.md"
APORTES_PATH = ROOT / "aportes.json"

# Cuartil SJR por ISSN (Scimago 2026). Los congresos no tienen cuartil SJR/JCR.
SJR_QUARTILES = {
    "1619-1366": "Q2 (SJR)", "1619-1374": "Q2 (SJR)",
    "1550-4832": "Q2 (SJR)", "1550-4840": "Q2 (SJR)",
}
CACHE_TTL_DAYS = 30
HTTP_TIMEOUT = 10
MAX_ABSTRACT = 2500
MATH_ALTA = 5.0
MATH_MEDIA = 1.5
USER_AGENT = "articulo-md/1.0 (conversion local)"
CROSSREF_URL = "https://api.crossref.org/works/{doi}"
OPENALEX_URL = "https://api.openalex.org/works/doi:{doi}"

MATH_SYMBOLS = re.compile(
    r"[∑∏∫∮√∂∇∞≈≠≤≥⊗⊕†⟨⟩ψφϕαβγδεθλμνρστωΔΩ]"
)
FOOTER_NOISE = (
    re.compile(r"^\s*Authorized licensed use limited to:.*$"),
    re.compile(r"^\s*Downloaded on .*from IEEE Xplore.*$"),
    re.compile(r"^\s*Restrictions apply\.?\s*$"),
    re.compile(r"^\s*Digital Object Identifier.*$"),
)
DOI_RE = re.compile(r"\b10\.\d{4,9}/[^\s,;\]\)}]+")
ARXIV_RE = re.compile(r"arXiv:\s*(\d{4}\.\d{4,5})(?:v\d+)?", re.I)


# --------------------------------------------------------------------------
# utilidades
# --------------------------------------------------------------------------
def log(msg: str) -> None:
    print(msg, flush=True)


@contextlib.contextmanager
def suppress_output(enabled: bool):
    """Silencia stdout/stderr (incluido el de librerías en C) durante la conversión."""
    if not enabled:
        yield
        return
    sys.stdout.flush()
    sys.stderr.flush()
    devnull = os.open(os.devnull, os.O_WRONLY)
    old_out, old_err = os.dup(1), os.dup(2)
    try:
        os.dup2(devnull, 1)
        os.dup2(devnull, 2)
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            yield
    finally:
        os.dup2(old_out, 1)
        os.dup2(old_err, 2)
        os.close(devnull)
        os.close(old_out)
        os.close(old_err)


def natural_key(text: str):
    return [int(p) if p.isdigit() else p.lower() for p in re.split(r"(\d+)", text)]


def safe_stem(path: Path) -> str:
    stem = path.stem.strip()
    stem = re.sub(r'[:*?"<>|\\/]+', "-", stem)
    stem = re.sub(r"\s+", " ", stem)
    return stem or "articulo"


def find_input_dir(explicit: str | None) -> Path | None:
    if explicit:
        p = Path(explicit).expanduser()
        return p if p.is_dir() else None
    for name in INPUT_CANDIDATES:
        p = ROOT / name
        if p.is_dir():
            return p
    return None


def resolve_pdf(arg: str, input_dir: Path | None) -> Path:
    p = Path(arg).expanduser()
    if p.is_file():
        return p.resolve()
    if input_dir:
        candidate = input_dir / arg
        if candidate.is_file():
            return candidate.resolve()
    if not p.suffix:
        for cand in (ROOT / f"{arg}.pdf", Path.cwd() / f"{arg}.pdf"):
            if cand.is_file():
                return cand.resolve()
    raise FileNotFoundError(f"No encuentro el PDF: {arg}")


def normalize_space(text: str) -> str:
    text = text.replace("\u00ad", "")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\s*\n\s*", " ", text)
    return text.strip()

DEHYPH_SUFFIXES = ("ation", "ations", "ically", "ities", "ments", "ness", "ingly", "ability")


def dehyphenate_text(text: str) -> str:
    """Une palabras cortadas por guion al final de línea ("Evalu-ation" -> "Evaluation")."""
    text = re.sub(r"(\w)-[ \t]+(?=\w)", r"\1-", text)
    def repl(m: re.Match) -> str:
        pre, suf = m.group(1), m.group(2)
        if len(pre) >= 3 and any(suf.startswith(x) for x in DEHYPH_SUFFIXES):
            return pre + suf
        if len(pre) == 2 and pre.lower() not in {"ad", "ex", "bi", "co", "de", "in", "re", "un", "pre", "id", "no"}:
            return pre + suf
        return m.group(0)
    return re.sub(r"\b([A-Za-z]{3,})-([a-z]{4,})\b", repl, text)


# --------------------------------------------------------------------------
# caché y APIs
# --------------------------------------------------------------------------
def load_cache() -> dict[str, Any]:
    try:
        return json.loads(CACHE_PATH.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def save_cache(cache: dict[str, Any]) -> None:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    CACHE_PATH.write_text(json.dumps(cache, ensure_ascii=False, indent=1), encoding="utf-8")


def cached_get(cache: dict[str, Any], key: str, url: str) -> dict[str, Any] | None:
    now = time.time()
    entry = cache.get(key)
    if entry and now - entry.get("ts", 0) < CACHE_TTL_DAYS * 86400:
        return entry.get("data")
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT) as resp:
            data = json.load(resp)
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, ValueError, OSError):
        cache[key] = {"ts": now, "data": None}
        return None
    cache[key] = {"ts": now, "data": data}
    return data


def crossref_lookup(doi: str, cache: dict[str, Any], offline: bool) -> dict[str, Any]:
    if offline:
        return {}
    data = cached_get(cache, f"crossref:{doi}", CROSSREF_URL.format(doi=urllib.parse.quote(doi, safe="")))
    return (data or {}).get("message", {}) if isinstance(data, dict) else {}


def openalex_lookup(doi: str, cache: dict[str, Any], offline: bool) -> dict[str, Any]:
    if offline:
        return {}
    data = cached_get(cache, f"openalex:{doi}", OPENALEX_URL.format(doi=urllib.parse.quote(doi, safe="")))
    return data if isinstance(data, dict) else {}


# --------------------------------------------------------------------------
# extracción desde el PDF
# --------------------------------------------------------------------------
def pdf_front_text(doc: "pymupdf.Document", max_pages: int = 2) -> str:
    chunks = [doc[i].get_text() for i in range(min(max_pages, doc.page_count))]
    return "\n".join(chunks)


def detect_doi(text: str) -> str | None:
    for m in DOI_RE.finditer(text):
        doi = m.group(0).rstrip(".,;:")
        if doi.lower().startswith("10."):
            return doi
    return None


def detect_arxiv(text: str) -> str | None:
    m = ARXIV_RE.search(text)
    return m.group(1) if m else None


def extract_pdf_abstract(text: str) -> str | None:
    patterns = (
        r"\bAbstract\b\s*[—–\-:]\s*(.+?)(?=\n\s*(?:Index Terms|Keywords|I\.\s+[A-Z]|1\.?\s+Introduction))",
        r"\bAbstract\b\s*\n\s*(.+?)(?=\n\s*(?:Index Terms|Keywords|I\.\s+[A-Z]|1\.?\s+Introduction))",
        r"\bAbstract\b\s*[—–\-:]\s*(.{200,2000})",
    )
    for pat in patterns:
        m = re.search(pat, text, re.S | re.I)
        if m:
            abstract = normalize_space(m.group(1))
            abstract = dehyphenate_text(abstract)
            if len(abstract) > 80:
                return abstract[:MAX_ABSTRACT]
    return None


def extract_pdf_keywords(text: str) -> list[str]:
    m = re.search(
        r"(?:Index Terms|Keywords?)\s*[—–:\-]?\s*(.{5,400}?)(?=\n\s*\n|\n\s*(?:I\.|1\.|Introduction))",
        text,
        re.S | re.I,
    )
    if not m:
        return []
    raw = normalize_space(m.group(1)).rstrip(" .;")
    raw = dehyphenate_text(raw)
    parts = re.split(r"\s*[;,]\s*", raw)
    out = []
    for p in parts:
        p = p.strip(" .;:-")
        if p and len(p) > 2 and not p.lower().startswith("and "):
            out.append(p)
    return out[:12]


def jats_to_text(html: str) -> str:
    text = re.sub(r"<[^>]+>", " ", html)
    text = text.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&")
    return normalize_space(text)


def openalex_abstract(work: dict[str, Any]) -> str | None:
    inv = work.get("abstract_inverted_index")
    if not isinstance(inv, dict):
        return None
    positions: list[tuple[int, str]] = []
    for word, idxs in inv.items():
        for i in idxs:
            positions.append((i, word))
    if not positions:
        return None
    positions.sort()
    return " ".join(w for _, w in positions)[:MAX_ABSTRACT]


# --------------------------------------------------------------------------
# conversión
# --------------------------------------------------------------------------
LIGATURES = {
    "\ufb00": "ff", "\ufb01": "fi", "\ufb02": "fl", "\ufb03": "ffi",
    "\ufb04": "ffl", "\ufb05": "ft", "\ufb06": "st",
}


def polish_markdown(md: str) -> str:
    for lig, repl in LIGATURES.items():
        md = md.replace(lig, repl)
    md = re.sub(r"<!--.*?-->", "", md, flags=re.S)
    md = re.sub(r"\n{3,}", "\n\n", md)
    def fix_heading(m: re.Match) -> str:
        text = m.group(2).replace("**", "").replace("__", "").strip()
        return f"{m.group(1)}{text}"
    return re.sub(r"^(#{1,6} )(.+)$", fix_heading, md, flags=re.M)


def math_label(density: float) -> str:
    if density > MATH_ALTA:
        return "alta ⚠"
    if density > MATH_MEDIA:
        return "media"
    return "baja"


def math_flags(density: float) -> list[str]:
    if density > MATH_ALTA:
        return ["Matemáticas densas: candidato a reconvertir con marker"]
    if density > MATH_MEDIA:
        return ["Matemáticas moderadas: revisar ecuaciones"]
    return []


def body_metrics(md: str) -> dict[str, Any]:
    body = re.sub(r"```.*?```", " ", md, flags=re.S)
    plain = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", body)
    plain = re.sub(r"^\|.*$", " ", plain, flags=re.M)
    plain = re.sub(r"[|#>*`_]", " ", plain)
    chars = len(md)
    words = len(re.findall(r"\b[\w'-]+\b", plain))
    math_hits = len(MATH_SYMBOLS.findall(plain))
    return {
        "chars": chars,
        "words": words,
        "tokens": round(chars / 4),
        "tables": len(re.findall(r"^\|(?:\s*:?-{3,}:?\s*\|)+", md, re.M)),
        "math_symbols": math_hits,
        "math_density": round(math_hits / max(words, 1) * 1000, 1),
    }


def reindex(index: dict[str, Any]) -> None:
    for stem, rec in index.items():
        article_dir = OUT_ROOT / stem
        body_path = article_dir / f"{stem}.md"
        if not body_path.is_file():
            continue
        md = polish_markdown(body_path.read_text(encoding="utf-8"))
        body_path.write_text(md, encoding="utf-8")
        rec.update(body_metrics(md))
        images_dir = article_dir / "images"
        rec["figures"] = len([p for p in images_dir.iterdir() if p.is_file()]) if images_dir.is_dir() else 0
        flags = [f for f in rec.get("flags", []) if not f.startswith("Matemáticas")]
        flags.extend(math_flags(rec["math_density"]))
        rec["flags"] = flags
        enrich_record(rec, load_cache())
        write_meta(rec, article_dir)
    save_index(index)
    render_index(index)
    render_resumen(index)


def clean_markdown(md: str) -> str:
    lines = md.splitlines()
    kept = []
    for line in lines:
        if any(pat.match(line) for pat in FOOTER_NOISE):
            continue
        kept.append(line.rstrip())
    fixed = []
    in_code = False
    for line in kept:
        if line.startswith("```"):
            in_code = not in_code
            fixed.append(line)
            continue
        if in_code or "](" in line:
            fixed.append(line)
        else:
            fixed.append(dehyphenate_text(line))
    md = "\n".join(fixed)
    md = re.sub(r"\n{3,}", "\n\n", md)
    return md.strip() + "\n"


def rename_images(article_dir: Path, md: str) -> tuple[str, list[str]]:
    images_dir = article_dir / "images"
    if not images_dir.is_dir():
        return md, []
    files = sorted(p for p in images_dir.iterdir() if p.is_file())
    mapping: dict[str, str] = {}
    counters: dict[int, int] = {}
    for f in files:
        m = re.search(r"-(\d{4})-(\d{2})\.png$", f.name)
        page = int(m.group(1)) if m else 0
        counters[page] = counters.get(page, 0) + 1
        new_name = f"p{page:02d}-{counters[page]:02d}{f.suffix.lower()}"
        mapping[f.name] = new_name
    for old, new in mapping.items():
        (images_dir / old).rename(images_dir / new)
    for old, new in mapping.items():
        md = md.replace(old, new)
    kept = sorted(p.name for p in images_dir.iterdir() if p.is_file())
    return md, kept


def convert_pdf(pdf: Path, args: argparse.Namespace) -> dict[str, Any]:
    stem = safe_stem(pdf)
    article_dir = OUT_ROOT / stem
    images_dir = article_dir / "images"
    started = time.time()

    if articles_done(article_dir, stem) and not args.force:
        return {"stem": stem, "skipped": True}

    if args.force and article_dir.exists():
        import shutil

        shutil.rmtree(article_dir)
    article_dir.mkdir(parents=True, exist_ok=True)
    if not args.no_images:
        images_dir.mkdir(parents=True, exist_ok=True)

    doc = pymupdf.open(pdf)
    front = pdf_front_text(doc)
    doc_meta = doc.metadata or {}
    page_count = doc.page_count
    raw_text = "\n".join(page.get_text() for page in doc)
    doc.close()

    doi = load_aportes().get(stem, {}).get("doi") or detect_doi(front) or detect_doi(raw_text[:20000])
    arxiv = detect_arxiv(front)

    pymupdf4llm.use_layout(True)
    cwd = os.getcwd()
    try:
        os.chdir(article_dir)
        with suppress_output(not args.verbose):
            md = pymupdf4llm.to_markdown(
                str(pdf),
                write_images=not args.no_images,
                image_path="images",
                image_format="png",
                dpi=150,
                use_ocr=True,
            )
    finally:
        os.chdir(cwd)

    md = polish_markdown(clean_markdown(md))
    md, image_files = rename_images(article_dir, md)
    body_path = article_dir / f"{stem}.md"
    body_path.write_text(md, encoding="utf-8")

    metrics = body_metrics(md)
    chars, words, tokens = metrics["chars"], metrics["words"], metrics["tokens"]
    tables = metrics["tables"]
    math_hits, math_density = metrics["math_symbols"], metrics["math_density"]

    cache = load_cache()
    cr = crossref_lookup(doi, cache, args.offline) if doi else {}
    oa = openalex_lookup(doi, cache, args.offline) if doi else {}
    save_cache(cache)

    cr_title = (cr.get("title") or [None])[0]
    oa_title = oa.get("title")
    title = cr_title or oa_title or doc_meta.get("title") or first_heading(md) or stem

    authors: list[str] = []
    for a in cr.get("author") or []:
        name = " ".join(x for x in (a.get("given"), a.get("family")) if x).strip()
        if name:
            authors.append(name)
    if not authors:
        for a in (oa.get("authorships") or []):
            name = (a.get("author") or {}).get("display_name")
            if name:
                authors.append(name)
    if not authors and doc_meta.get("author"):
        authors = [x.strip() for x in re.split(r"[;,]", doc_meta["author"]) if x.strip()]

    year = None
    for key in ("published", "published-print", "published-online", "issued", "created"):
        parts = (cr.get(key) or {}).get("date-parts")
        if parts and parts[0] and parts[0][0]:
            year = parts[0][0]
            break
    if not year:
        year = oa.get("publication_year")

    venue = (cr.get("container-title") or [None])[0]
    if not venue:
        venue = ((oa.get("primary_location") or {}).get("source") or {}).get("display_name")
    if not venue and cr.get("event"):
        venue = cr["event"].get("name")

    refs = cr.get("reference-count")
    if refs is None:
        refs = oa.get("referenced_works_count")
    if refs is None:
        refs = count_references(md)

    cited = oa.get("cited_by_count")
    if cited is None:
        cited = cr.get("is-referenced-by-count")

    keywords = extract_pdf_keywords(front)
    if not keywords:
        keywords = [k.get("display_name") for k in (oa.get("keywords") or []) if k.get("display_name")][:12]
    if not keywords:
        keywords = list((cr.get("subject") or [])[:12])

    abstract = extract_pdf_abstract(front)
    if not abstract and cr.get("abstract"):
        abstract = jats_to_text(cr["abstract"])[:MAX_ABSTRACT]
    if not abstract:
        abstract = openalex_abstract(oa)

    chars_per_page = len(raw_text) / max(page_count, 1)
    scanned = chars_per_page < 120

    flags: list[str] = []
    if scanned:
        flags.append("PDF sin capa de texto fiable (revisar OCR)")
    flags.extend(math_flags(math_density))
    if not abstract:
        flags.append("Abstract no detectado")
    if not doi:
        flags.append("DOI no detectado")

    record = {
        "stem": stem,
        "pdf": str(pdf),
        "title": title,
        "authors": authors,
        "year": year,
        "venue": venue,
        "doi": doi,
        "arxiv": arxiv,
        "pages": page_count,
        "chars": chars,
        "words": words,
        "tokens": tokens,
        "figures": len(image_files),
        "tables": tables,
        "math_symbols": math_hits,
        "math_density": math_density,
        "references": refs,
        "cited": cited,
        "abstract": abstract,
        "keywords": keywords,
        "status": "escaneado" if scanned else "ok",
        "flags": flags,
        "converted_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "seconds": round(time.time() - started, 1),
    }

    record["authors_short"] = crossref_authors(cr) or format_authors(authors)
    record["tipo"] = cr.get("type") or (
        "proceedings-article" if re.search(r"conference|congress|symposium|workshop", venue or "", re.I) else "journal-article"
    )
    record["issn"] = cr.get("ISSN") or []
    record["cuartil"] = next((SJR_QUARTILES[i] for i in record["issn"] if i in SJR_QUARTILES), None)
    if not record["cuartil"]:
        record["cuartil"] = "— (congreso)" if record["tipo"] == "proceedings-article" else "—"

    write_meta(record, article_dir)
    return record


def articles_done(article_dir: Path, stem: str) -> bool:
    return (article_dir / f"{stem}.md").is_file()


def first_heading(md: str) -> str | None:
    m = re.search(r"^#\s+(.+)$", md, re.M)
    return m.group(1).strip() if m else None


def count_references(md: str) -> int | None:
    m = re.search(r"^#{0,3}\s*(?:REFERENCES|References|Bibliography)\s*$", md, re.M)
    if not m:
        return None
    tail = md[m.end():]
    numbered = len(re.findall(r"^\s*\[\d+\]", tail, re.M))
    if numbered:
        return numbered
    years = len(re.findall(r"\(\d{4}\)", tail))
    return years or None


# --------------------------------------------------------------------------
# salida
# --------------------------------------------------------------------------
def fmt(value: Any) -> str:
    return "—" if value in (None, "", []) else str(value)


def write_meta(rec: dict[str, Any], article_dir: Path) -> None:
    authors = "; ".join(rec["authors"]) if rec["authors"] else "—"
    label = math_label(rec["math_density"])
    lines = [
        f"# {rec['title']}",
        "",
        "| Campo | Valor |",
        "|---|---|",
        f"| Archivo | `{rec['stem']}.pdf` |",
        f"| Autores | {authors} |",
        f"| Año | {fmt(rec['year'])} |",
        f"| Venue | {fmt(rec['venue'])} |",
        f"| DOI | {fmt(rec['doi'])} |",
        f"| arXiv | {fmt(rec['arxiv'])} |",
        f"| Páginas | {rec['pages']} |",
        f"| Palabras | {rec['words']:,} |",
        f"| Caracteres | {rec['chars']:,} |",
        f"| Tokens estimados | ~{rec['tokens'] / 1000:.1f} k |",
        f"| Figuras | {rec['figures']} |",
        f"| Tablas | {rec['tables']} |",
        f"| Referencias | {fmt(rec['references'])} |",
        f"| Citas recibidas | {fmt(rec['cited'])} |",
        f"| Densidad matemática | {label} ({rec['math_density']} por 1k palabras) |",
        f"| Estado | {rec['status']} |",
        f"| Convertido | {rec['converted_at']} ({rec['seconds']} s) |",
        "",
        "## Abstract",
        "",
        rec["abstract"] or "_No detectado._",
        "",
        "## Palabras clave",
        "",
    ]
    if rec["keywords"]:
        lines += [f"- {k}" for k in rec["keywords"]]
    else:
        lines.append("_No detectadas._")
    lines += ["", "## Avisos", ""]
    if rec["flags"]:
        lines += [f"- {f}" for f in rec["flags"]]
    else:
        lines.append("- Sin avisos.")
    lines.append("")
    (article_dir / f"{rec['stem']}.meta.md").write_text("\n".join(lines), encoding="utf-8")


def load_index() -> dict[str, Any]:
    try:
        return json.loads(INDEX_JSON.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def save_index(index: dict[str, Any]) -> None:
    OUT_ROOT.mkdir(parents=True, exist_ok=True)
    INDEX_JSON.write_text(json.dumps(index, ensure_ascii=False, indent=1), encoding="utf-8")


def load_aportes() -> dict[str, Any]:
    try:
        return json.loads(APORTES_PATH.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def id_from_stem(stem: str) -> int:
    m = re.match(r"^(\d{1,3})(?=-|$)", stem)
    return int(m.group(1)) if m else 10_000


def format_authors(names: list[str]) -> list[str]:
    out = []
    for name in names:
        parts = name.split()
        out.append(f"{parts[-1]}, {parts[0][0]}." if len(parts) >= 2 else name)
    return out


def short_authors(formatted: list[str], limit: int = 3) -> str:
    if not formatted:
        return "—"
    text = "; ".join(formatted[:limit])
    if len(formatted) > limit:
        text += f"; et al. ({len(formatted)})"
    return text


def crossref_authors(cr: dict[str, Any]) -> list[str]:
    out = []
    for a in cr.get("author") or []:
        family = (a.get("family") or "").strip()
        given = (a.get("given") or "").strip()
        if family:
            out.append(f"{family}, {given[0]}." if given else family)
    return out


def enrich_record(rec: dict[str, Any], cache: dict[str, Any]) -> dict[str, Any]:
    cr: dict[str, Any] = {}
    doi = rec.get("doi")
    entry = cache.get(f"crossref:{doi}") if doi else None
    if entry and entry.get("data"):
        cr = (entry["data"].get("message") or {})
    venue = rec.get("venue") or ""
    if not rec.get("tipo"):
        rec["tipo"] = cr.get("type") or (
            "proceedings-article" if re.search(r"conference|congress|symposium|workshop", venue, re.I) else "journal-article"
        )
    if not rec.get("issn"):
        rec["issn"] = cr.get("ISSN") or []
    if not rec.get("authors_short"):
        rec["authors_short"] = crossref_authors(cr) or format_authors(rec.get("authors") or [])
    rec["cuartil"] = next((SJR_QUARTILES[i] for i in rec["issn"] if i in SJR_QUARTILES), None)
    if not rec["cuartil"]:
        rec["cuartil"] = "— (congreso)" if rec["tipo"] == "proceedings-article" else "—"
    return rec


def render_resumen(index: dict[str, Any]) -> None:
    aportes = load_aportes()
    rows: list[str] = []
    conferences: dict[str, str] = {}
    corpus = [s for s in index if id_from_stem(s) != 10_000]
    for stem in sorted(corpus, key=id_from_stem):
        r = index[stem]
        extra = aportes.get(stem, {})
        cuartil = extra.get("cuartil") or r.get("cuartil") or "—"
        aporte = extra.get("aporte") or r.get("aporte") or "—"
        venue = r.get("venue") or "—"
        if r.get("tipo") == "proceedings-article" or "congreso" in str(cuartil):
            shown = short_venue(venue, r.get("year"))
            conferences[shown] = venue
        else:
            shown = venue
        doi = r.get("doi")
        url = f"[{doi}](https://doi.org/{doi})" if doi else "—"
        rows.append(
            "| {id} | {title} | {authors} | {year} | {venue} | {quart} | {cited} | {url} | {aporte} |".format(
                id=id_from_stem(stem),
                title=str(r["title"]).replace("|", "/"),
                authors=short_authors(r.get("authors_short") or format_authors(r.get("authors") or [])).replace("|", "/"),
                year=fmt(r.get("year")),
                venue=str(shown).replace("|", "/"),
                quart=cuartil,
                cited=fmt(r.get("cited")),
                url=url,
                aporte=str(aporte).replace("|", "/"),
            )
        )

    lines = [
        "# Resumen de artículos",
        "",
        f"{len(rows)} artículos convertidos desde `pdf's/`.",
        "",
        "| ID | Título de la investigación | Autores | Año | Revista / Conferencia | Cuartil (SJR / JCR) | Citas | URL / DOI | Aporte Principal |",
        "|---|---|---|---|---|---|---|---|---|",
        *rows,
        "",
        "## Notas",
        "",
        "- **Citas**: contador de OpenAlex (consultado en octubre de 2026).",
        "- **Cuartil**: SJR de Scimago (2026) para las revistas; los congresos no tienen cuartil SJR/JCR.",
        "  Factor de impacto JCR orientativo: *Software and Systems Modeling* 3.0; *ACM JETC* 2.3.",
        "  El cuartil JCR exacto requiere suscripción a Clarivate.",
        "- **Aportes**: resumen propio a partir del abstract; edítalos en `aportes.json`.",
        "- Fichas completas: `md/<id>/<id>.meta.md`.",
        "",
    ]
    if conferences:
        lines += ["### Congresos citados", ""]
        lines += [f"- **{short}**: {full}" for short, full in sorted(conferences.items())]
        lines.append("")
    RESUMEN_PATH.write_text("\n".join(lines), encoding="utf-8")


def short_venue(venue: str | None, year: Any) -> str:
    if not venue:
        return "—"
    venue = venue.replace("|", "/")
    m = re.search(r"\(([A-Z][A-Za-z0-9&./ -]{1,15})\)\s*$", venue)
    if m and len(venue) > 40:
        return f"{m.group(1)} {year}" if year else m.group(1)
    return venue


def render_index(index: dict[str, Any]) -> None:
    rows = []
    total_tokens = 0
    for stem in sorted(index, key=natural_key):
        r = index[stem]
        first_author = ""
        if r.get("authors"):
            first_author = r["authors"][0].split()[-1] + (" et al." if len(r["authors"]) > 1 else "")
        title = r["title"]
        venue = short_venue(r.get("venue"), r.get("year"))
        if len(venue) > 45:
            venue = venue[:42] + "…"
        rows.append(
            "| {n} | [{title}](./{stem}/{stem}.md) · [meta](./{stem}/{stem}.meta.md) | {year} | {venue} | {cited} | {pages} | {tok} | {fig} | {refs} | {math} | {status} |".format(
                n=len(rows) + 1,
                title=title.replace("|", "/"),
                stem=stem,
                year=fmt(r.get("year")),
                venue=venue or "—",
                cited=fmt(r.get("cited")),
                pages=r.get("pages", "—"),
                tok=f"{r.get('tokens', 0) / 1000:.1f}k",
                fig=r.get("figures", 0),
                refs=fmt(r.get("references")),
                math=r.get("math_density", 0),
                status=r.get("status", "—"),
            )
        )
        total_tokens += r.get("tokens", 0)

    lines = [
        "# Índice de artículos",
        "",
        f"{len(rows)} artículo{'' if len(rows) == 1 else 's'} · ~{total_tokens / 1000:.1f} k tokens en total.",
        "",
        "| # | Artículo | Año | Venue | Citas | Pág | Tokens | Fig | Ref | Mat/1k | Estado |",
        "|---|---|---|---|---|---|---|---|---|---|---|",
        *rows,
        "",
    ]
    INDEX_MD.write_text("\n".join(lines), encoding="utf-8")


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------
def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="convertir",
        description="Convierte PDFs a Markdown con metadatos y métricas.",
    )
    p.add_argument("pdfs", nargs="*", help="PDF(s) a convertir (nombre o ruta)")
    p.add_argument("--all", action="store_true", help="convierte todos los PDFs de la carpeta de entrada")
    p.add_argument("--force", action="store_true", help="reconvierte aunque ya exista la salida")
    p.add_argument("--offline", action="store_true", help="no consulta Crossref/OpenAlex")
    p.add_argument("--no-images", action="store_true", help="no extrae figuras")
    p.add_argument("--in", dest="input_dir", help="carpeta de entrada (por defecto pdf/ o pdf's/)")
    p.add_argument("--verbose", action="store_true", help="muestra la salida interna del conversor")
    p.add_argument("--reindex", action="store_true", help="recalcula métricas y el índice sin reconvertir")
    p.add_argument("--resumen", action="store_true", help="regenera resumen.md a partir del índice")
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    input_dir = find_input_dir(args.input_dir)

    if args.reindex:
        index = load_index()
        reindex(index)
        log(f"Reindexados {len(index)} artículos → {INDEX_MD.relative_to(ROOT)}")
        return 0

    if args.resumen:
        index = load_index()
        render_resumen(index)
        log(f"Resumen: {RESUMEN_PATH.relative_to(ROOT)}")
        return 0

    targets: list[Path] = []
    if args.all:
        if not input_dir:
            log("✗ No encuentro la carpeta de entrada (pdf/ o pdf's/)")
            return 2
        targets = sorted(input_dir.glob("*.pdf"), key=lambda p: natural_key(p.stem))
    for arg in args.pdfs:
        try:
            targets.append(resolve_pdf(arg, input_dir))
        except FileNotFoundError as exc:
            log(f"✗ {exc}")
            return 2

    if not targets:
        build_parser().print_help()
        return 2

    OUT_ROOT.mkdir(parents=True, exist_ok=True)
    index = load_index()
    failures = 0
    for pdf in targets:
        label = pdf.name
        log(f"→ {label}")
        try:
            rec = convert_pdf(pdf, args)
        except Exception as exc:  # noqa: BLE001
            failures += 1
            log(f"  ✗ error: {type(exc).__name__}: {exc}")
            partial = OUT_ROOT / safe_stem(pdf)
            if not (partial / f"{safe_stem(pdf)}.meta.md").exists():
                import shutil
                shutil.rmtree(partial, ignore_errors=True)
                log("  · salida parcial eliminada")
            continue
        if rec.get("skipped"):
            log("  ⏭  ya convertido (usa --force para repetir)")
            continue
        index[rec["stem"]] = rec
        save_index(index)
        log(
            "  ✅ {pages} pág · ~{tok:.1f}k tokens · {fig} fig · {tables} tablas · {secs}s".format(
                pages=rec["pages"],
                tok=rec["tokens"] / 1000,
                fig=rec["figures"],
                tables=rec["tables"],
                secs=rec["seconds"],
            )
        )

    render_index(index)
    render_resumen(index)
    log(f"\nÍndice: {INDEX_MD.relative_to(ROOT)}")
    log(f"Resumen: {RESUMEN_PATH.relative_to(ROOT)}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
