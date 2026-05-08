#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""
download_raw.py
---------------
A generic source-fetcher for second-brain ingestion.

Reads a list of resources (URLs + filenames) from a TOML catalogue and
downloads them into raw/papers/ and raw/articles/.

Defaults to scripts/resources.toml in the same directory, which ships with a
black-box-optimization & LLM-tuning catalogue. Replace that file (or use
--resources <path>) for any other topic.

USAGE
=====

Use the bundled defaults (BBO + LLM tuning):
    python3 download_raw.py
    python3 download_raw.py --tier 1            # only must-haves
    python3 download_raw.py --skip-html         # PDFs only
    python3 download_raw.py --dry-run           # preview, don't download

Use a custom resource list:
    python3 download_raw.py --resources my-topic.toml
    python3 download_raw.py -r ~/notes/ml-papers.toml --out ~/notes/raw/

Generate a starter template for a new topic:
    python3 download_raw.py --init my-topic.toml

Run with uv (auto-handles Python version per PEP 723):
    uv run download_raw.py [args]

RESOURCE FILE FORMAT
====================

The resource catalogue is a TOML file with a list of [[resource]] entries:

    [[resource]]
    tier     = 1                       # 1=must, 2=nice, 3=ref (any int OK)
    kind     = "pdf"                   # "pdf" or "html"
    filename = "Author-Year-Title.pdf" # local filename
    url      = "https://..."           # download URL
    note     = "Description"           # optional, shown in the manifest

OUTPUT
======

    <out>/
      papers/        all PDFs
      articles/      all HTML pages
      _manifest.csv  index with status, URL, note for each file

Re-runs are idempotent: existing files are skipped unless --force is given.
"""

from __future__ import annotations

import argparse
import csv
import sys
import time
import urllib.request
import urllib.error
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

# tomllib is stdlib in Python 3.11+. For 3.10, fall back to tomli.
try:
    import tomllib  # type: ignore[import]
except ImportError:  # pragma: no cover
    try:
        import tomli as tomllib  # type: ignore[import]
    except ImportError:
        sys.stderr.write(
            "ERROR: Python 3.11+ required (or `pip install tomli` for 3.10).\n"
        )
        sys.exit(2)


# -----------------------------------------------------------------------------
# Resource model
# -----------------------------------------------------------------------------

@dataclass
class Resource:
    tier: int
    kind: str         # "pdf" or "html"
    filename: str
    url: str
    note: str = ""

    @classmethod
    def from_dict(cls, d: dict, source_label: str = "") -> "Resource":
        missing = {"tier", "kind", "filename", "url"} - set(d)
        if missing:
            raise ValueError(
                f"resource missing required field(s) {sorted(missing)} "
                f"in {source_label}: {d}"
            )
        kind = str(d["kind"]).lower()
        if kind not in {"pdf", "html"}:
            raise ValueError(
                f"resource kind must be 'pdf' or 'html', got {kind!r} "
                f"in {source_label}"
            )
        return cls(
            tier=int(d["tier"]),
            kind=kind,
            filename=str(d["filename"]),
            url=str(d["url"]),
            note=str(d.get("note", "")),
        )


def load_resources(toml_path: Path) -> list[Resource]:
    """Parse a resources.toml catalogue."""
    if not toml_path.exists():
        raise FileNotFoundError(f"resource catalogue not found: {toml_path}")
    with toml_path.open("rb") as f:
        data = tomllib.load(f)
    raw = data.get("resource", [])
    if not isinstance(raw, list) or not raw:
        raise ValueError(
            f"{toml_path}: expected at least one [[resource]] entry "
            f"(got {type(raw).__name__})"
        )
    out: list[Resource] = []
    for i, item in enumerate(raw):
        if not isinstance(item, dict):
            raise ValueError(f"{toml_path}: resource #{i} is not a table")
        out.append(Resource.from_dict(item, f"{toml_path}#{i}"))
    return out


def default_catalogue_path() -> Path:
    """resources.toml next to this script."""
    return Path(__file__).resolve().parent / "resources.toml"


STARTER_TEMPLATE = """\
# resources.toml — list of papers and pages to download.
#
# Schema:
#   [[resource]]
#   tier     = 1                # 1=must, 2=nice, 3=ref (any int OK)
#   kind     = "pdf"            # "pdf" or "html"
#   filename = "Author-Year.pdf"
#   url      = "https://..."
#   note     = "One-line description"

[[resource]]
tier     = 1
kind     = "pdf"
filename = "Example-Paper.pdf"
url      = "https://arxiv.org/pdf/0000.00000"
note     = "Replace with your first paper"

[[resource]]
tier     = 2
kind     = "html"
filename = "Example-Blog-Post.html"
url      = "https://example.com/post"
note     = "Replace with your first web article"
"""


# -----------------------------------------------------------------------------
# Downloader
# -----------------------------------------------------------------------------

USER_AGENT = (
    "Mozilla/5.0 (compatible; SecondBrainFetcher/1.0; "
    "+research second-brain builder)"
)
TIMEOUT_S = 60
RETRIES = 3
BACKOFF_S = 3


def download_one(url: str, dest: Path, force: bool = False) -> tuple[str, str]:
    """Download url -> dest. Return (status, message)."""
    if dest.exists() and not force:
        size_kb = dest.stat().st_size / 1024
        return "skipped", f"already exists ({size_kb:.0f} KB)"

    dest.parent.mkdir(parents=True, exist_ok=True)
    last_err = ""
    for attempt in range(1, RETRIES + 1):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=TIMEOUT_S) as resp:
                data = resp.read()
                dest.write_bytes(data)
                size_kb = len(data) / 1024
                return "ok", f"{size_kb:.0f} KB"
        except urllib.error.HTTPError as e:
            last_err = f"HTTP {e.code}"
            if e.code in (403, 404):
                break  # no point retrying
        except (urllib.error.URLError, TimeoutError, OSError) as e:
            last_err = str(e)
        if attempt < RETRIES:
            time.sleep(BACKOFF_S * attempt)
    return "failed", last_err or "unknown error"


def fmt_status(status: str) -> str:
    return {
        "ok":      "  OK ",
        "skipped": "SKIP ",
        "failed":  "FAIL ",
        "dry":     " DRY ",
    }.get(status, status)


# -----------------------------------------------------------------------------
# Filtering
# -----------------------------------------------------------------------------

def filter_resources(
    resources: Iterable[Resource],
    max_tier: int,
    skip_html: bool,
) -> list[Resource]:
    return [
        r for r in resources
        if r.tier <= max_tier and not (skip_html and r.kind == "html")
    ]


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

def cmd_init(path: Path) -> int:
    if path.exists():
        print(f"ERROR: {path} already exists. Refusing to overwrite.",
              file=sys.stderr)
        return 1
    path.write_text(STARTER_TEMPLATE, encoding="utf-8")
    print(f"Wrote starter catalogue to {path}")
    print(f"Edit the [[resource]] entries, then run:")
    print(f"  python3 {Path(__file__).name} --resources {path}")
    return 0


def main() -> int:
    p = argparse.ArgumentParser(
        description="Download papers and pages listed in a TOML catalogue.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("-r", "--resources", type=Path,
                   default=default_catalogue_path(),
                   help=f"Path to resources.toml "
                        f"(default: {default_catalogue_path()})")
    p.add_argument("--tier", type=int, default=99,
                   help="Max tier to download (e.g. 1 = must-haves only). "
                        "Default: 99 (all tiers).")
    p.add_argument("--out", type=Path, default=Path("raw"),
                   help="Output directory (default: ./raw)")
    p.add_argument("--skip-html", action="store_true",
                   help="Skip HTML resources, only fetch PDFs")
    p.add_argument("--force", action="store_true",
                   help="Re-download even if file already exists")
    p.add_argument("--dry-run", action="store_true",
                   help="Print plan without downloading")
    p.add_argument("--init", type=Path, metavar="PATH",
                   help="Create a starter resources.toml at PATH and exit")
    args = p.parse_args()

    if args.init is not None:
        return cmd_init(args.init)

    # Load catalogue
    try:
        resources = load_resources(args.resources)
    except (FileNotFoundError, ValueError) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        if args.resources == default_catalogue_path():
            print(
                "Hint: the default catalogue file is missing. "
                "Either restore it or pass --resources <path>.",
                file=sys.stderr,
            )
        else:
            print(
                "Hint: run `download_raw.py --init my-topic.toml` "
                "to generate a template.",
                file=sys.stderr,
            )
        return 2

    selected = filter_resources(resources, args.tier, args.skip_html)

    print(f"Catalogue        : {args.resources}")
    print(f"Output directory : {args.out.resolve()}")
    print(f"Tier filter      : <= {args.tier}")
    print(f"Skip HTML        : {args.skip_html}")
    print(f"Total in catalog : {len(resources)}")
    print(f"After filtering  : {len(selected)}")
    print("-" * 78)

    if not selected:
        print("Nothing to download with the current filters.")
        return 0

    args.out.mkdir(parents=True, exist_ok=True)
    manifest_rows: list[dict] = []
    counts: dict[str, int] = {"ok": 0, "skipped": 0, "failed": 0, "dry": 0}
    start = time.time()

    for i, r in enumerate(selected, 1):
        sub = "papers" if r.kind == "pdf" else "articles"
        dest = args.out / sub / r.filename
        rel = dest.relative_to(args.out)

        if args.dry_run:
            status, msg = "dry", "would download"
        else:
            status, msg = download_one(r.url, dest, force=args.force)

        counts[status] = counts.get(status, 0) + 1
        print(f"[{i:2d}/{len(selected)}] {fmt_status(status)} "
              f"T{r.tier} {rel}  ({msg})")

        manifest_rows.append({
            "tier":     r.tier,
            "kind":     r.kind,
            "filename": str(rel),
            "url":      r.url,
            "status":   status,
            "message":  msg,
            "note":     r.note,
        })

        # Be polite to upstream: small delay between live downloads
        if status == "ok" and not args.dry_run:
            time.sleep(0.5)

    # Write manifest
    manifest_path = args.out / "_manifest.csv"
    with manifest_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["tier", "kind", "filename", "url",
                        "status", "message", "note"],
        )
        writer.writeheader()
        writer.writerows(manifest_rows)

    elapsed = time.time() - start
    print("-" * 78)
    print(f"Done in {elapsed:.1f}s   "
          f"ok={counts.get('ok', 0)}  "
          f"skipped={counts.get('skipped', 0)}  "
          f"failed={counts.get('failed', 0)}  "
          f"dry={counts.get('dry', 0)}")
    print(f"Manifest: {manifest_path}")

    if counts.get("failed", 0):
        print("\nSome downloads failed. Common causes:")
        print("  - Behind a proxy/firewall (set HTTPS_PROXY)")
        print("  - Publisher blocks direct PDF download (open URL manually)")
        print("  - Network timeout (re-run; existing files are skipped)")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
