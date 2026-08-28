#!/usr/bin/env python3
"""Fail-closed structural verifier for the θ-Theory five-paper series.

This script verifies repository structure, named imports/exports, acyclicity,
forbidden blanket labels, convention anchors, actual scoped technical
appendices, review boundaries, and file hashes.  It does not verify the truth of
mathematical proofs or grant theorem credit.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "papers" / "theta-program" / "five-paper-series"

PAPERS = {
    "paper_I": "paper-I-cm2-u3",
    "paper_II": "paper-II-pressure-diffusion",
    "paper_III": "paper-III-rough-theta",
    "paper_IV": "paper-IV-filter-games",
    "paper_V": "paper-V-representations",
}

EXPORTS = {
    "paper_I": {
        "P1-CM2", "P1-FDQ", "P1-U3", "P1-RWORDS", "P1-ACTUAL-4B"
    },
    "paper_II": {
        "P2-COMMON", "P2-PRESSURE3", "P2-SUSP0", "P2-PHYS",
        "P2-COEFF", "P2-ELL", "P2-ACTUAL-4B"
    },
    "paper_III": {
        "P3-DOOB", "P3-RWIP", "P3-NAHOM", "P3-HJB", "P3-THETA",
        "P3-NONCONVEX", "P3-ACTUAL-4B"
    },
    "paper_IV": {
        "P4-FILTER-B", "P4-FILTER-W", "P4-SEQ", "P4-MIXED",
        "P4-PURE-GATE", "P4-BELIEF", "P4-PATH", "P4-ACTUAL-4B"
    },
    "paper_V": {
        "P5-SINGLE-LAW-NOGO", "P5-CALIBRATED", "P5-FBSDE",
        "P5-CONTROL-BSDE", "P5-SECOND-ORDER", "P5-PPDE", "P5-GIRSANOV"
    },
}

IMPORTS = {
    "paper_I": set(),
    "paper_II": {"P1-CM2", "P1-FDQ", "P1-U3", "P1-RWORDS"},
    "paper_III": {
        "P2-COMMON", "P2-PRESSURE3", "P2-SUSP0", "P2-PHYS",
        "P2-COEFF", "P2-ELL"
    },
    "paper_IV": {"P3-DOOB", "P3-RWIP", "P3-NAHOM"},
    "paper_V": {
        "P3-HJB", "P3-THETA", "P4-SEQ", "P4-MIXED",
        "P4-PURE-GATE", "P4-BELIEF", "P4-PATH"
    },
}

FORBIDDEN_LABELS = {
    "thm:main_response_package",
    "thm:moving_singularity_response",
    "thm:regularity_loss_budget",
    "lem:suspension_laplace_contour",
}

REQUIRED_TOP = {
    "README.md",
    "FIVE_PAPER_CLOSURE_STATUS.md",
    "THEOREM_INTERFACE_MANIFEST.yaml",
    "HOSTILE_PROOF_AUDIT.md",
    "FIVE_PAPER_VERIFICATION_RECEIPT.json",
}

EXTRA_REQUIRED = {
    "paper_II": {"TECHNICAL_NOTE_RENEWAL.md"},
    "paper_III": {"TECHNICAL_APPENDIX_DPP_COMPARISON.md"},
    "paper_IV": {"TECHNICAL_APPENDIX_GAME_SCHEME.md"},
}

CONVENTION_ANCHORS = {
    "paper_I": ("X4 --G1--> X3", "finite-DQ"),
    "paper_II": ("quadratic partition", "D^{\\rm phys}(a)=\\frac12\\Sigma(a)"),
    "paper_III": ("direct triangular-characteristics", "4\\delta>0"),
    "paper_IV": ("vanishing slow initial layer", "mixed Isaacs equality"),
    "paper_V": ("generator orientation", "Z_s=\\sigma(s,X_s)^TDu"),
}

TECHNICAL_ANCHORS = {
    ("paper_II", "TECHNICAL_NOTE_RENEWAL.md"): (
        "distinct entry and exit", "\\mathcal O_{a,z}F"
    ),
    ("paper_III", "TECHNICAL_APPENDIX_DPP_COMPARISON.md"): (
        "Theorem A.3", "actual theta-expectation"
    ),
    ("paper_IV", "TECHNICAL_APPENDIX_GAME_SCHEME.md"): (
        "Theorem B.2", "mixed-Isaacs"
    ),
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def main() -> int:
    errors: list[str] = []
    hashes: dict[str, str] = {}

    if not BASE.is_dir():
        print(json.dumps({"status": "FAIL", "error": f"missing {BASE}"}))
        return 1

    for name in sorted(REQUIRED_TOP):
        path = BASE / name
        if not path.is_file():
            fail(errors, f"missing top-level file: {name}")
        else:
            hashes[str(path.relative_to(ROOT))] = sha256(path)

    producers: dict[str, str] = {}
    for paper, tokens in EXPORTS.items():
        for token in tokens:
            if token in producers:
                fail(errors, f"duplicate export producer for {token}")
            producers[token] = paper

    order = {paper: i for i, paper in enumerate(PAPERS)}
    graph: dict[str, set[str]] = {paper: set() for paper in PAPERS}

    for paper, dirname in PAPERS.items():
        directory = BASE / dirname
        required = {
            "MANUSCRIPT.md", "BLOCKER_CLOSURE.md", "INTERFACE.md"
        } | EXTRA_REQUIRED.get(paper, set())

        for filename in sorted(required):
            path = directory / filename
            if not path.is_file():
                fail(errors, f"missing {dirname}/{filename}")
                continue

            text = path.read_text(encoding="utf-8")
            hashes[str(path.relative_to(ROOT))] = sha256(path)

            if filename == "MANUSCRIPT.md":
                if "## Abstract" not in text or "## Conclusion" not in text:
                    fail(errors, f"incomplete manuscript skeleton: {dirname}")
                for anchor in CONVENTION_ANCHORS[paper]:
                    if anchor not in text:
                        fail(errors, f"missing convention anchor {anchor!r} in {dirname}")
            elif filename == "BLOCKER_CLOSURE.md":
                if "CLOSED" not in text:
                    fail(errors, f"no closure entries in {dirname}")
            elif filename == "INTERFACE.md":
                for token in EXPORTS[paper]:
                    if text.count(f"`{token}`") != 1:
                        fail(errors, f"export {token} missing or duplicated in {dirname}")
                for token in IMPORTS[paper]:
                    if text.count(f"`{token}`") != 1:
                        fail(errors, f"import {token} missing or duplicated in {dirname}")
            else:
                for anchor in TECHNICAL_ANCHORS.get((paper, filename), ()):
                    if anchor not in text:
                        fail(errors, f"missing technical anchor {anchor!r} in {dirname}/{filename}")

            for label in FORBIDDEN_LABELS:
                if label in text:
                    fail(errors, f"forbidden blanket label {label} in {dirname}/{filename}")

        for token in IMPORTS[paper]:
            producer = producers.get(token)
            if producer is None:
                fail(errors, f"unresolved import {token} in {paper}")
                continue
            if order[producer] >= order[paper]:
                fail(errors, f"reverse/non-upstream import {token}: {producer}->{paper}")
            graph[producer].add(paper)

    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node: str) -> None:
        if node in visited:
            return
        if node in visiting:
            fail(errors, f"cycle detected at {node}")
            return
        visiting.add(node)
        for nxt in graph[node]:
            visit(nxt)
        visiting.remove(node)
        visited.add(node)

    for paper in PAPERS:
        visit(paper)

    status_path = BASE / "FIVE_PAPER_CLOSURE_STATUS.md"
    if status_path.is_file():
        status_text = status_path.read_text(encoding="utf-8")
        for required_status in (
            "actual_scoped_chain_through_theta: CLOSED",
            "actual_scoped_chain_through_mixed_Isaacs: CLOSED",
            "external_peer_review: NOT_PERFORMED",
            "formal_credit: 0",
        ):
            if required_status not in status_text:
                fail(errors, f"status boundary missing: {required_status}")

    result = {
        "schema": "THETA_FIVE_PAPER_VERIFY_V2",
        "status": "PASS" if not errors else "FAIL",
        "paper_count": len(PAPERS),
        "named_export_count": sum(map(len, EXPORTS.values())),
        "named_import_count": sum(map(len, IMPORTS.values())),
        "actual_technical_file_count": sum(map(len, EXTRA_REQUIRED.values())),
        "errors": errors,
        "sha256": dict(sorted(hashes.items())),
        "mathematical_proof_verified": False,
        "external_peer_review": "NOT_PERFORMED",
        "formal_credit": 0,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
