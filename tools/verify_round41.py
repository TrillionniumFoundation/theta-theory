#!/usr/bin/env python3
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
MANIFEST = ROOT / "round41" / "SOURCE_MANIFEST.json"
PDF = ROOT / "ROUND41_REVISION.pdf"
LOG = ROOT / "ROUND41_REVISION.log"

EXPECTED_LABELS: dict[str, tuple[str, ...]] = {
    "round41/triangular.tex": ("thm:abstract-bvm", "lem:random-laplace"),
    "round41/lattice.tex": ("thm:jet-embedding", "lem:prefix-window-count", "prop:balanced-contrast", "thm:lattice-bvm"),
    "round41/filter_memory.tex": ("lem:strong-pushforward", "thm:filter-jets", "cor:state-image", "cor:memory-posterior"),
    "round41/infinite_jacobi.tex": ("thm:jacobi-reconstruction", "prop:jacobi-response-geometry", "thm:jacobi-rate", "thm:jacobi-consistency"),
    "round41/preparations.tex": ("thm:preparation-mixture",),
    "round41/appendix_uniformity.tex": ("lem:supnorm-response-slln",),
}

REQUIRED_INPUTS = (
    "round41/introduction.tex",
    "round41/triangular.tex",
    "round41/lattice.tex",
    "round41/filter_memory.tex",
    "round41/infinite_jacobi.tex",
    "round41/preparations.tex",
    "round41/appendix_uniformity.tex",
    "round41/references.tex",
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_structure() -> dict[str, Any]:
    failures: list[str] = []
    main = ROOT / "ROUND41_REVISION.tex"
    main_text = main.read_text(encoding="utf-8") if main.is_file() else ""
    if not main.is_file():
        failures.append("missing ROUND41_REVISION.tex")
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
    article = "\n".join((ROOT / p).read_text(encoding="utf-8") for p in ("ROUND41_REVISION.tex", *REQUIRED_INPUTS) if (ROOT / p).is_file())
    for token in ("GitHub Actions", "SHA--256", "Round 40 report", "source manifest"):
        if token in article:
            failures.append(f"article contains governance token: {token}")
    return {"passed": not failures, "failures": failures}


def check_manifest() -> dict[str, Any]:
    failures: list[str] = []
    if not MANIFEST.is_file():
        return {"passed": False, "failures": ["manifest missing"]}
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    entries = manifest.get("files", [])
    for entry in entries:
        path = ROOT / entry["path"]
        if not path.is_file():
            failures.append(f"missing {entry['path']}")
            continue
        if path.stat().st_size != entry["bytes"]:
            failures.append(f"size mismatch for {entry['path']}")
        if sha256(path) != entry["sha256"]:
            failures.append(f"sha256 mismatch for {entry['path']}")
    return {"passed": bool(entries) and not failures, "checked_files": len(entries), "failures": failures}


def check_build() -> dict[str, Any]:
    failures: list[str] = []
    if not PDF.is_file() or PDF.stat().st_size < 10_000:
        failures.append("ROUND41_REVISION.pdf missing or unexpectedly small")
    text = LOG.read_text(encoding="utf-8", errors="replace") if LOG.is_file() else ""
    if not LOG.is_file():
        failures.append("ROUND41_REVISION.log missing")
    for token in ("! LaTeX Error:", "There were undefined references", "Citation `", "Reference `", "Emergency stop", "Fatal error occurred"):
        if token in text:
            failures.append(f"build log contains: {token}")
    match = re.search(r"Output written on .*?\((\d+) pages?", text)
    if not match and LOG.is_file():
        failures.append("could not determine page count")
    return {
        "passed": not failures,
        "pdf_bytes": PDF.stat().st_size if PDF.is_file() else None,
        "pdf_pages": int(match.group(1)) if match else None,
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
            "formal_proof_assistant": False,
            "checked": ["source invariants", "manifest hashes", "two-pass LaTeX build"],
            "analytic_proofs": ["finite-prefix empirical process", "strong dual measurability", "compact-class SLLN", "full Jacobi posterior LDP", "uniform inverse-response moduli"],
        },
    }
    if args.check_manifest:
        result["manifest"] = check_manifest()
    if args.check_build:
        result["build"] = check_build()
    result["all_passed"] = all(v.get("passed", True) for k, v in result.items() if isinstance(v, dict) and k not in {"python", "scope"})
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.json_path:
        out = args.json_path if args.json_path.is_absolute() else ROOT / args.json_path
        out.write_text(rendered, encoding="utf-8")
    sys.stdout.write(rendered)
    return 0 if result["all_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
