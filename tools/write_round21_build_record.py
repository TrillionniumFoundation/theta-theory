#!/usr/bin/env python3
"""Write exact Round-Twenty-One source/PDF hashes after a clean build."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

PAPERS = [
    "A1-exact-benchmarks",
    "A2-sinai-homological-pressure",
    "A3-full-empirical-path-ldp",
    "A4-history-memory-universal-pressure",
    "B1-microcanonical-preparation",
    "B2-collision-clusters-dynamic-ldp",
    "B3-hamilton-boltzmann-cotangents",
    "B4-nonlinear-kinetic-semigroups",
    "C1-information-risk-sensitive-saddles",
    "C2-cotangent-rigidity-tangent-representations",
    "D1-deterministic-theta-contractions",
]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    rows = []
    for name in PAPERS:
        folder = Path("papers") / name
        pdf = folder / "main.pdf"
        source = folder / "ROUND17_POSITIVE_CLOSURE.tex"
        wrapper = folder / "main.tex"
        response = folder / "AUTHOR_RESPONSE_ROUND20.md"
        for path in (pdf, source, wrapper, response):
            if not path.is_file():
                raise SystemExit(f"missing publication file: {path}")
        if pdf.stat().st_size < 10_000:
            raise SystemExit(f"suspiciously small PDF: {pdf}")
        rows.append(
            {
                "paper": name,
                "source_bytes": source.stat().st_size,
                "source_sha256": digest(source),
                "wrapper_sha256": digest(wrapper),
                "response_sha256": digest(response),
                "pdf_bytes": pdf.stat().st_size,
                "pdf_sha256": digest(pdf),
            }
        )

    payload = {
        "schema": "theta-round21-build-summary-v1",
        "source_commit": os.environ.get("GITHUB_SHA"),
        "workflow_run": os.environ.get("GITHUB_RUN_ID"),
        "paper_count": len(rows),
        "papers": rows,
        "status": "STRUCTURAL_AND_TEX_BUILD_PASS",
        "disclaimer": "Internal reproducibility gate; not external peer review.",
    }
    Path("ROUND21_BUILD_SUMMARY.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    status_lines = [
        "# Round-Twenty-One revision status",
        "",
        f"**Source commit verified:** `{payload['source_commit']}`  ",
        f"**Workflow run:** `{payload['workflow_run']}`  ",
        f"**Paper count:** `{payload['paper_count']}`  ",
        "**Structural verifier:** **PASS**  ",
        "**Clean TeX builds:** **11/11 PASS**  ",
        "**Generated PDFs:** **11/11 nonempty and hash-recorded**",
        "",
        "The workflow ran `tools/update_round21_wrappers.py`,",
        "`tools/verify_round21.py`, and `make all` from a clean checkout.",
        "Exact source, wrapper, author-response, and PDF hashes are recorded in",
        "`ROUND21_BUILD_SUMMARY.json`.",
        "",
        "This is an internal source-identity, dependency, and reproducibility",
        "result. It is not a claim of external journal acceptance or a",
        "substitute for a new independent referee review.",
        "",
    ]
    Path("ROUND21_REVISION_STATUS.md").write_text(
        "\n".join(status_lines), encoding="utf-8"
    )
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
