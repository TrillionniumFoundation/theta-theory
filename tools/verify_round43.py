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
MANIFEST = ROOT / "round43/SOURCE_MANIFEST.json"
PDF = ROOT / "ROUND43_REVISION.pdf"
LOG = ROOT / "ROUND43_REVISION.log"

MANIFEST_PATHS = (
    "ROUND43_REVISION.tex",
    "round43/preamble.tex",
    "round43/introduction.tex",
    "round43/triangular.tex",
    "round43/lattice.tex",
    "round43/filter_memory.tex",
    "round43/infinite_jacobi.tex",
    "round43/quantitative_jacobi.tex",
    "round43/effective_inversion_details.tex",
    "round43/linear_time_protocol.tex",
    "round43/preparations.tex",
    "round43/appendix_uniformity.tex",
    "round43/references.tex",
    "AUTHOR_RESPONSE_ROUND42.md",
    "ROUND43_REVIEW_INDEX.md",
    "ROUND43_READY_FOR_REVIEW.md",
    "round43/HISTORICAL_REUSE.md",
    "round43/PROOF_LEDGER.json",
    "tools/materialize_round41.py",
    "tools/harden_round41_ldp.py",
    "tools/materialize_round43.py",
    "tools/verify_round43.py",
    "tests/test_round41.py",
    "tests/test_round43.py",
    ".github/workflows/verify-round43.yml",
)

REQUIRED_LABELS = (
    "thm:abstract-bvm",
    "lem:prefix-window-count",
    "prop:balanced-contrast",
    "lem:strong-pushforward",
    "lem:supnorm-response-slln",
    "thm:jacobi-reconstruction",
    "eq:jacobi-posterior-ldp",
    "thm:effective-jacobi-stability",
    "lem:response-moment-triangularity",
    "prop:effective-gram-reconstruction",
    "thm:effective-response-jet-audit",
    "thm:growing-depth-recovery",
    "thm:explicit-shrinking-block-rate",
    "cor:weighted-operator-recovery",
    "thm:adaptive-exploration-floor",
    "thm:honest-jacobi-cylinders",
    "lem:l1-impulse-geometry",
    "lem:predictable-intercept-information",
    "thm:linear-time-adaptive-jacobi",
    "thm:linear-time-honest-cylinders",
    "eq:linear-physical-time",
    "eq:linear-elapsed-rate",
    "eq:physical-time-complexity",
    "eq:physical-time-speed",
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def refresh_manifest() -> None:
    entries = []
    for relative in MANIFEST_PATHS:
        path = ROOT / relative
        if not path.is_file():
            raise SystemExit(f"manifest source missing: {relative}")
        entries.append({"path": relative, "bytes": path.stat().st_size, "sha256": sha256(path)})
    payload = {
        "source_set": "round43-positive-referee-closure-v2-linear-time-effective-jacobi",
        "controlling_report": "REFEREE_REPORT_ROUND42_GPT56_PRO_HARSH.md",
        "reviewed_report_commit": "f66cb02217574c12b17b3a49ea630086da437e1f",
        "hash": "sha256",
        "publication_unit": "ordinary committed TeX sources; generators are provenance only",
        "files": entries,
    }
    MANIFEST.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def check_structure() -> dict[str, Any]:
    failures: list[str] = []
    for relative in MANIFEST_PATHS:
        if not (ROOT / relative).is_file():
            failures.append(f"missing {relative}")
    article_paths = [ROOT / "ROUND43_REVISION.tex", *sorted((ROOT / "round43").glob("*.tex"))]
    article = "\n".join(p.read_text(encoding="utf-8") for p in article_paths if p.is_file())
    for label in REQUIRED_LABELS:
        if f"\\label{{{label}}}" not in article:
            failures.append(f"missing label {label}")
    for token in (
        chr(12),
        "w_i=w_*i",
        "Doob's inequality",
        "conditional second moment at most",
        r"C_\alpha(i+1)^{-1-\epsilon_w}",
    ):
        if token in article:
            failures.append(f"stale forbidden token: {token}")
    for token in (
        r"(1+\log(i+1))^{|\alpha|}",
        r"\label{eq:explicit-moment-recursion}",
        r"\label{eq:linear-posterior-upper}",
        r"\label{eq:linear-confidence-radius}",
    ):
        if token not in article:
            failures.append(f"required v2 source invariant absent: {token}")

    workflow_dir = ROOT / ".github/workflows"
    retained = sorted(p.name for p in workflow_dir.glob("*.yml"))
    if retained != ["verify-round43.yml"]:
        failures.append(f"unexpected retained workflows: {retained}")
    workflow_path = workflow_dir / "verify-round43.yml"
    workflow = workflow_path.read_text(encoding="utf-8") if workflow_path.is_file() else ""
    if "contents: read" not in workflow or "contents: write" in workflow or "git push" in workflow:
        failures.append("Round 43 verification workflow is not read-only")
    return {"passed": not failures, "failures": failures}


def check_manifest() -> dict[str, Any]:
    failures: list[str] = []
    if not MANIFEST.is_file():
        return {"passed": False, "failures": ["manifest missing"]}
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    entries = data.get("files", [])
    if tuple(e.get("path") for e in entries) != MANIFEST_PATHS:
        failures.append("manifest path list differs from verifier publication unit")
    if data.get("source_set") != "round43-positive-referee-closure-v2-linear-time-effective-jacobi":
        failures.append("manifest source_set is not the v2 publication unit")
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
        failures.append("ROUND43_REVISION.pdf missing or unexpectedly small")
    log = LOG.read_text(encoding="utf-8", errors="replace") if LOG.is_file() else ""
    if not LOG.is_file():
        failures.append("ROUND43_REVISION.log missing")
    for token in (
        "! LaTeX Error:",
        "There were undefined references",
        "Citation `",
        "Reference `",
        "Emergency stop",
        "Fatal error occurred",
    ):
        if token in log:
            failures.append(f"build log contains: {token}")
    match = re.search(r"Output written on .*?\((\d+) pages?", log)
    if LOG.is_file() and not match:
        failures.append("could not determine PDF page count")
    return {
        "passed": not failures,
        "pdf_bytes": PDF.stat().st_size if PDF.is_file() else None,
        "pdf_sha256": sha256(PDF) if PDF.is_file() else None,
        "pdf_pages": int(match.group(1)) if match else None,
        "failures": failures,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--refresh-manifest", action="store_true")
    parser.add_argument("--check-manifest", action="store_true")
    parser.add_argument("--check-build", action="store_true")
    parser.add_argument("--json", dest="json_path", type=Path)
    args = parser.parse_args()
    if args.refresh_manifest:
        refresh_manifest()
    result: dict[str, Any] = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "python": {"implementation": platform.python_implementation(), "version": platform.python_version()},
        "structure": check_structure(),
        "scope": {
            "formal_proof_assistant": False,
            "checked": [
                "source invariants",
                "finite Vandermonde algebra",
                "response-moment recursion",
                "finite Gram reconstruction",
                "predictable-intercept sub-Gaussian inequality",
                "manifest hashes",
                "two-pass LaTeX build",
                "single read-only workflow",
            ],
            "analytic_proofs_for_referee": [
                "adaptive martingale likelihood",
                "strong dual measurability",
                "posterior LDP",
                "effective inverse stability",
                "growing-depth contraction",
                "explicit shrinking radii",
                "no-washout linear-time posterior bound",
                "confidence cylinders",
            ],
        },
    }
    if args.check_manifest:
        result["manifest"] = check_manifest()
    if args.check_build:
        result["build"] = check_build()
    result["all_passed"] = all(
        value.get("passed", True)
        for key, value in result.items()
        if isinstance(value, dict) and key not in {"python", "scope"}
    )
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.json_path:
        path = args.json_path if args.json_path.is_absolute() else ROOT / args.json_path
        path.write_text(rendered, encoding="utf-8")
    sys.stdout.write(rendered)
    return 0 if result["all_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
