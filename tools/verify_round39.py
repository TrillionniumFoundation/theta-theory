#!/usr/bin/env python3
"""Finite reproducibility checks for the Round 39 manuscript.

This program checks exact source integrity, reviewer-facing theorem labels and,
when requested, the two-pass LaTeX build.  It deliberately does not claim to
formally verify the analytic probability or inverse-spectral arguments.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "round39" / "SOURCE_MANIFEST.json"
PDF = ROOT / "ROUND39_REVISION.pdf"
LOG = ROOT / "ROUND39_REVISION.log"

EXPECTED_LABELS: dict[str, tuple[str, ...]] = {
    "round39/triangular.tex": ("thm:abstract-bvm", "lem:random-laplace"),
    "round39/lattice.tex": ("thm:jet-embedding", "prop:balanced-contrast", "thm:lattice-bvm"),
    "round39/filter_memory.tex": ("thm:filter-jets", "cor:state-image", "cor:memory-posterior"),
    "round39/infinite_jacobi.tex": ("thm:jacobi-reconstruction", "thm:jacobi-consistency"),
    "round39/preparations_verification.tex": ("thm:preparation-mixture",),
}

REQUIRED_INPUTS = (
    "round39/introduction.tex",
    "round39/triangular.tex",
    "round39/lattice.tex",
    "round39/filter_memory.tex",
    "round39/infinite_jacobi.tex",
    "round39/preparations_verification.tex",
    "round39/appendix_uniformity.tex",
    "round39/references.tex",
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def check_structure() -> dict[str, Any]:
    main = ROOT / "ROUND39_REVISION.tex"
    failures: list[str] = []
    if not main.is_file():
        failures.append("missing ROUND39_REVISION.tex")
        main_text = ""
    else:
        main_text = main.read_text(encoding="utf-8")
    for source in REQUIRED_INPUTS:
        if not (ROOT / source).is_file():
            failures.append(f"missing {source}")
        if f"\\input{{{source}}}" not in main_text:
            failures.append(f"main manuscript does not input {source}")
    for source, labels in EXPECTED_LABELS.items():
        path = ROOT / source
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        for label in labels:
            if f"\\label{{{label}}}" not in text:
                failures.append(f"missing label {label} in {source}")
    return {
        "passed": not failures,
        "checked_source_files": 1 + len(REQUIRED_INPUTS),
        "checked_labels": sum(len(labels) for labels in EXPECTED_LABELS.values()),
        "failures": failures,
    }


def check_manifest() -> dict[str, Any]:
    failures: list[str] = []
    if not MANIFEST.is_file():
        return {"passed": False, "path": str(MANIFEST.relative_to(ROOT)), "failures": ["manifest missing"]}
    try:
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return {"passed": False, "path": str(MANIFEST.relative_to(ROOT)), "failures": [str(exc)]}
    entries = manifest.get("files")
    if not isinstance(entries, list) or not entries:
        return {"passed": False, "path": str(MANIFEST.relative_to(ROOT)), "failures": ["files list missing"]}
    for entry in entries:
        relative = entry.get("path")
        if not isinstance(relative, str):
            failures.append("manifest entry without path")
            continue
        path = ROOT / relative
        if not path.is_file():
            failures.append(f"missing {relative}")
            continue
        data_size = path.stat().st_size
        expected_size = entry.get("bytes")
        if data_size != expected_size:
            failures.append(f"size mismatch for {relative}: {data_size} != {expected_size}")
        actual_hash = sha256(path)
        expected_hash = entry.get("sha256")
        if actual_hash != expected_hash:
            failures.append(f"sha256 mismatch for {relative}: {actual_hash} != {expected_hash}")
    return {
        "passed": not failures,
        "path": str(MANIFEST.relative_to(ROOT)),
        "checked_files": len(entries),
        "failures": failures,
    }


def check_build() -> dict[str, Any]:
    failures: list[str] = []
    if not PDF.is_file():
        failures.append("ROUND39_REVISION.pdf missing")
    elif PDF.stat().st_size < 10_000:
        failures.append("ROUND39_REVISION.pdf is unexpectedly small")
    log_text = ""
    if not LOG.is_file():
        failures.append("ROUND39_REVISION.log missing")
    else:
        log_text = LOG.read_text(encoding="utf-8", errors="replace")
        forbidden = (
            "! LaTeX Error:",
            "There were undefined references",
            "Citation `",
            "Reference `",
            "Emergency stop",
            "Fatal error occurred",
        )
        for marker in forbidden:
            if marker in log_text:
                failures.append(f"build log contains: {marker}")
    pages = None
    match = re.search(r"Output written on .*?\((\d+) pages?", log_text)
    if match:
        pages = int(match.group(1))
    elif LOG.is_file():
        failures.append("could not determine PDF page count from LaTeX log")
    return {
        "passed": not failures,
        "pdf": PDF.name,
        "log": LOG.name,
        "pdf_bytes": PDF.stat().st_size if PDF.is_file() else None,
        "pdf_pages": pages,
        "clean_log": LOG.is_file() and not failures,
        "failures": failures,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-manifest", action="store_true")
    parser.add_argument("--check-build", action="store_true")
    parser.add_argument("--json", dest="json_path", type=Path)
    args = parser.parse_args()

    result: dict[str, Any] = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "python": {"implementation": platform.python_implementation(), "version": platform.python_version()},
        "structure": check_structure(),
        "scope": {
            "statement": "Exact finite algebra is exercised by tests/test_round39.py; this script checks source integrity and the document build. Analytic proofs remain mathematical arguments in the manuscript.",
            "formal_proof_assistant": False,
            "not_checked": [
                "martingale empirical-process proofs",
                "relative random-information Laplace theorem",
                "strong Banach-dual differentiability",
                "infinite Jacobi inverse uniqueness",
                "posterior consistency arguments",
                "novelty or journal significance",
            ],
        },
    }
    if args.check_manifest:
        result["manifest"] = check_manifest()
    if args.check_build:
        result["build"] = check_build()

    result["all_passed"] = all(
        section.get("passed", True)
        for key, section in result.items()
        if isinstance(section, dict) and key not in {"python", "scope"}
    )
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.json_path:
        output = args.json_path if args.json_path.is_absolute() else ROOT / args.json_path
        output.write_text(rendered, encoding="utf-8")
    sys.stdout.write(rendered)
    return 0 if result["all_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
