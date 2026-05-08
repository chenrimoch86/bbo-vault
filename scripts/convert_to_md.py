#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "pymupdf4llm>=0.0.17",
#     "trafilatura>=1.12.0",
# ]
# ///
"""
convert_to_md.py
----------------
Converts the PDFs and HTML pages downloaded by download_raw.py into
clean markdown files suitable for a second brain (Obsidian, Logseq, etc).

Usage:
    python3 convert_to_md.py                  # convert raw/ -> raw-md/
    python3 convert_to_md.py --in raw --out raw-md
    python3 convert_to_md.py --force          # re-convert existing files
    python3 convert_to_md.py --dry-run        # show what would happen

Conversion strategy (best tool first, falls back automatically):
    PDF:
        1. pymupdf4llm  (best — preserves structure, headings, tables)
        2. pypdf        (decent — text only, no structure)
        3. pdftotext    (system binary, if installed)
    HTML:
        1. trafilatura  (best — strips boilerplate, gives clean markdown)
        2. markdownify + BeautifulSoup  (good fallback)
        3. html.parser  (stdlib only — crude but works)

Install best-quality dependencies:
    pip install pymupdf4llm trafilatura

The script works without any external packages too, just lower quality.

Output layout:
    raw-md/
      papers/         one .md per PDF, with YAML frontmatter
      articles/       one .md per HTML page
      _conversion_log.csv
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import re
import sys
import time
from pathlib import Path
from typing import Optional

# -----------------------------------------------------------------------------
# Optional dependencies — checked at runtime, never hard-required
# -----------------------------------------------------------------------------

def _try_import(name: str):
    try:
        return __import__(name)
    except ImportError:
        return None

pymupdf4llm   = _try_import("pymupdf4llm")
pypdf         = _try_import("pypdf")
trafilatura   = _try_import("trafilatura")
markdownify_m = _try_import("markdownify")
bs4           = _try_import("bs4")


# -----------------------------------------------------------------------------
# PDF → markdown
# -----------------------------------------------------------------------------

def pdf_to_md(pdf_path: Path) -> tuple[str, str]:
    """Return (markdown_text, method_used). Tries best tool, falls back."""

    # 1) pymupdf4llm — purpose-built for LLM ingestion
    if pymupdf4llm is not None:
        try:
            md = pymupdf4llm.to_markdown(str(pdf_path))
            if md.strip():
                return md, "pymupdf4llm"
        except Exception as e:
            print(f"    pymupdf4llm failed: {e}", file=sys.stderr)

    # 2) pypdf — plain text only, no structure
    if pypdf is not None:
        try:
            reader = pypdf.PdfReader(str(pdf_path))
            text = "\n\n".join(
                page.extract_text() or "" for page in reader.pages
            )
            if text.strip():
                return _light_clean(text), "pypdf"
        except Exception as e:
            print(f"    pypdf failed: {e}", file=sys.stderr)

    # 3) pdftotext system binary
    import shutil, subprocess
    if shutil.which("pdftotext"):
        try:
            out = subprocess.run(
                ["pdftotext", "-layout", str(pdf_path), "-"],
                capture_output=True, text=True, timeout=120,
            )
            if out.returncode == 0 and out.stdout.strip():
                return _light_clean(out.stdout), "pdftotext"
        except Exception as e:
            print(f"    pdftotext failed: {e}", file=sys.stderr)

    return "", "FAILED"


# -----------------------------------------------------------------------------
# HTML → markdown
# -----------------------------------------------------------------------------

def html_to_md(html_path: Path) -> tuple[str, str]:
    """Return (markdown_text, method_used). Tries best tool, falls back."""
    html = html_path.read_text(encoding="utf-8", errors="replace")

    # 1) trafilatura — extracts main content, strips ads/nav
    if trafilatura is not None:
        try:
            md = trafilatura.extract(
                html,
                output_format="markdown",
                include_links=True,
                include_tables=True,
                include_formatting=True,
            )
            if md and md.strip():
                return md, "trafilatura"
        except Exception as e:
            print(f"    trafilatura failed: {e}", file=sys.stderr)

    # 2) markdownify + BeautifulSoup — convert DOM directly
    if markdownify_m is not None and bs4 is not None:
        try:
            soup = bs4.BeautifulSoup(html, "html.parser")
            # Try to grab <article> or <main> if present, else <body>
            root = soup.find("article") or soup.find("main") or soup.body or soup
            for tag in root.find_all(["script", "style", "nav", "footer", "header"]):
                tag.decompose()
            md = markdownify_m.markdownify(str(root), heading_style="ATX")
            if md.strip():
                return _light_clean(md), "markdownify"
        except Exception as e:
            print(f"    markdownify failed: {e}", file=sys.stderr)

    # 3) Stdlib-only fallback — strip tags crudely
    return _stdlib_html_to_text(html), "stdlib"


# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------

def _light_clean(text: str) -> str:
    """Tidy whitespace, drop hyphenated line-breaks, collapse blank runs."""
    # Join hyphenated line breaks: "optimi-\nzation" -> "optimization"
    text = re.sub(r"-\n([a-z])", r"\1", text)
    # Collapse 3+ newlines to 2
    text = re.sub(r"\n{3,}", "\n\n", text)
    # Strip trailing spaces on each line
    text = "\n".join(line.rstrip() for line in text.splitlines())
    return text.strip() + "\n"


def _stdlib_html_to_text(html: str) -> tuple[str, str]:
    """Last-resort HTML stripper using only the stdlib."""
    from html.parser import HTMLParser

    class Stripper(HTMLParser):
        def __init__(self):
            super().__init__()
            self.parts: list[str] = []
            self.skip = 0

        def handle_starttag(self, tag, attrs):
            if tag in {"script", "style", "nav", "footer", "header"}:
                self.skip += 1
            if tag in {"p", "br", "div", "li", "tr"}:
                self.parts.append("\n")
            if re.match(r"h[1-6]", tag):
                level = int(tag[1])
                self.parts.append("\n\n" + "#" * level + " ")

        def handle_endtag(self, tag):
            if tag in {"script", "style", "nav", "footer", "header"}:
                self.skip = max(0, self.skip - 1)
            if re.match(r"h[1-6]", tag):
                self.parts.append("\n\n")

        def handle_data(self, data):
            if self.skip == 0:
                self.parts.append(data)

    s = Stripper()
    s.feed(html)
    return _light_clean("".join(s.parts))


def _read_manifest(raw_root: Path) -> dict[str, dict]:
    """Read _manifest.csv from raw/ to recover URLs for frontmatter."""
    mf = raw_root / "_manifest.csv"
    if not mf.exists():
        return {}
    out: dict[str, dict] = {}
    with mf.open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            # filename in manifest is like "papers/foo.pdf"
            out[row["filename"]] = row
    return out


def _frontmatter(src_file: Path, raw_root: Path,
                 manifest: dict[str, dict], method: str) -> str:
    """Build a YAML frontmatter block for the converted markdown."""
    rel = src_file.relative_to(raw_root).as_posix()
    info = manifest.get(rel, {})
    today = dt.date.today().isoformat()

    lines = ["---"]
    lines.append(f'title: "{src_file.stem}"')
    lines.append(f'source_file: "{rel}"')
    if info.get("url"):
        lines.append(f'source_url: "{info["url"]}"')
    if info.get("note"):
        # escape any double quotes in note
        note = info["note"].replace('"', "'")
        lines.append(f'description: "{note}"')
    lines.append(f"converted: {today}")
    lines.append(f"converter: {method}")
    lines.append("type: source")
    lines.append("tags: [raw, source]")
    lines.append("---")
    lines.append("")
    return "\n".join(lines)


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

def main() -> int:
    p = argparse.ArgumentParser(
        description="Convert raw PDFs/HTML to second-brain-ready markdown.")
    p.add_argument("--in", dest="in_dir", type=Path, default=Path("raw"),
                   help="Input directory (default: ./raw)")
    p.add_argument("--out", dest="out_dir", type=Path, default=Path("raw-md"),
                   help="Output directory (default: ./raw-md)")
    p.add_argument("--force", action="store_true",
                   help="Re-convert even if .md already exists")
    p.add_argument("--dry-run", action="store_true",
                   help="Print plan without writing")
    args = p.parse_args()

    if not args.in_dir.exists():
        print(f"ERROR: input directory not found: {args.in_dir}",
              file=sys.stderr)
        print("  Run download_raw.py first.", file=sys.stderr)
        return 1

    # Diagnostic banner
    print(f"Input            : {args.in_dir.resolve()}")
    print(f"Output           : {args.out_dir.resolve()}")
    print("Available tools:")
    print(f"  PDF : "
          f"pymupdf4llm={'yes' if pymupdf4llm else 'no'}  "
          f"pypdf={'yes' if pypdf else 'no'}")
    print(f"  HTML: "
          f"trafilatura={'yes' if trafilatura else 'no'}  "
          f"markdownify={'yes' if markdownify_m and bs4 else 'no'}")
    print("-" * 78)

    if not (pymupdf4llm or pypdf):
        print("Hint: install one of these for better PDF conversion:")
        print("  pip install pymupdf4llm   (recommended)")
        print("  pip install pypdf         (lighter)")
    if not trafilatura and not (markdownify_m and bs4):
        print("Hint: install for better HTML conversion:")
        print("  pip install trafilatura   (recommended)")
        print("  pip install markdownify beautifulsoup4")
    print()

    manifest = _read_manifest(args.in_dir)
    log_rows: list[dict] = []
    counts = {"ok": 0, "skipped": 0, "failed": 0, "dry": 0}

    pdfs    = sorted((args.in_dir / "papers").glob("*.pdf"))   if (args.in_dir / "papers").exists() else []
    htmls   = sorted((args.in_dir / "articles").glob("*.html")) if (args.in_dir / "articles").exists() else []
    total   = len(pdfs) + len(htmls)

    if total == 0:
        print("No source files found in raw/papers or raw/articles.")
        return 0

    start = time.time()
    i = 0

    for src in pdfs + htmls:
        i += 1
        sub = "papers" if src.suffix == ".pdf" else "articles"
        dest = args.out_dir / sub / (src.stem + ".md")
        rel  = dest.relative_to(args.out_dir).as_posix()

        if dest.exists() and not args.force:
            print(f"[{i:2d}/{total}] SKIP  {rel}  (already converted)")
            counts["skipped"] += 1
            continue

        if args.dry_run:
            print(f"[{i:2d}/{total}]  DRY  {rel}  (would convert)")
            counts["dry"] += 1
            log_rows.append({"src": str(src), "dst": str(dest),
                             "method": "dry", "status": "dry"})
            continue

        if src.suffix == ".pdf":
            md, method = pdf_to_md(src)
        else:
            md, method = html_to_md(src)

        if not md.strip():
            print(f"[{i:2d}/{total}] FAIL  {rel}  (no content extracted)")
            counts["failed"] += 1
            log_rows.append({"src": str(src), "dst": str(dest),
                             "method": method, "status": "failed"})
            continue

        dest.parent.mkdir(parents=True, exist_ok=True)
        front = _frontmatter(src, args.in_dir, manifest, method)
        dest.write_text(front + md, encoding="utf-8")
        size_kb = dest.stat().st_size / 1024
        print(f"[{i:2d}/{total}]  OK   {rel}  ({method}, {size_kb:.0f} KB)")
        counts["ok"] += 1
        log_rows.append({"src": str(src), "dst": str(dest),
                         "method": method, "status": "ok"})

    # Write conversion log
    if not args.dry_run and log_rows:
        args.out_dir.mkdir(parents=True, exist_ok=True)
        log_path = args.out_dir / "_conversion_log.csv"
        with log_path.open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=["src", "dst", "method", "status"])
            w.writeheader()
            w.writerows(log_rows)
        print(f"\nLog: {log_path}")

    elapsed = time.time() - start
    print("-" * 78)
    print(f"Done in {elapsed:.1f}s   "
          f"ok={counts['ok']}  skipped={counts['skipped']}  "
          f"failed={counts['failed']}  dry={counts['dry']}")

    return 0 if counts["failed"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
