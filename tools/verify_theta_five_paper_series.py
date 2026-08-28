#!/usr/bin/env python3
"""Fail-closed structural verifier for the θ-Theory five-paper series.

The verifier checks file presence, named theorem producers/imports, optional
upstream edges, acyclicity, convention anchors, maximal-strengthening scope
anchors, review boundaries, and SHA-256 hashes. It does not certify the truth
of mathematical proofs or grant theorem credit.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "papers" / "theta-program" / "five-paper-series"
MAX = ROOT / "papers" / "theta-program" / "maximal-strengthening"

PAPERS = {
    "paper_I": "paper-I-cm2-u3",
    "paper_II": "paper-II-pressure-diffusion",
    "paper_III": "paper-III-rough-theta",
    "paper_IV": "paper-IV-filter-games",
    "paper_V": "paper-V-representations",
}

EXPORTS = {
    "paper_I": {
        "P1-CM2", "P1-FDQ", "P1-U3", "P1-RWORDS", "P1-ACTUAL-4B",
        "P1-SINAI-RADIAL-U3",
    },
    "paper_II": {
        "P2-COMMON", "P2-PRESSURE3", "P2-SUSP0", "P2-PHYS",
        "P2-COEFF", "P2-ELL", "P2-ACTUAL-4B", "P2-BDL-HF-FAMILY",
    },
    "paper_III": {
        "P3-DOOB", "P3-RWIP", "P3-RWIP-OPTIMAL-WETA-P", "P3-NAHOM",
        "P3-HJB", "P3-THETA", "P3-NONCONVEX", "P3-ACTUAL-4B",
    },
    "paper_IV": {
        "P4-FILTER-B", "P4-FILTER-W", "P4-WEIGHTED-NONCOMPACT-ACTUAL",
        "P4-SEQ", "P4-MIXED", "P4-PURE-GATE",
        "P4-PURE-ISAACS-MAXIMAL", "P4-BELIEF", "P4-PATH", "P4-ACTUAL-4B",
    },
    "paper_V": {
        "P5-SINGLE-LAW-NOGO", "P5-CALIBRATED", "P5-FBSDE",
        "P5-CONTROL-BSDE", "P5-SECOND-ORDER", "P5-PPDE",
        "P5-PATH-ACTUAL", "P5-GIRSANOV",
    },
}

IMPORTS = {
    "paper_I": set(),
    "paper_II": {"P1-CM2", "P1-FDQ", "P1-U3", "P1-RWORDS"},
    "paper_III": {
        "P2-COMMON", "P2-PRESSURE3", "P2-SUSP0", "P2-PHYS",
        "P2-COEFF", "P2-ELL",
    },
    "paper_IV": {"P3-DOOB", "P3-RWIP", "P3-NAHOM"},
    "paper_V": {
        "P3-HJB", "P3-THETA", "P4-SEQ", "P4-MIXED", "P4-PURE-GATE",
        "P4-PURE-ISAACS-MAXIMAL", "P4-BELIEF", "P4-PATH",
        "P4-WEIGHTED-NONCOMPACT-ACTUAL",
    },
}

OPTIONAL_IMPORTS = {
    "paper_I": set(),
    "paper_II": {"P1-SINAI-RADIAL-U3"},
    "paper_III": {"P2-BDL-HF-FAMILY"},
    "paper_IV": {"P3-RWIP-OPTIMAL-WETA-P"},
    "paper_V": set(),
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
    "paper_I": {"TECHNICAL_APPENDIX_SPECULAR_RADIAL_U3.md"},
    "paper_II": {
        "TECHNICAL_NOTE_RENEWAL.md",
        "TECHNICAL_APPENDIX_HIGH_FREQUENCY_FAMILY.md",
    },
    "paper_III": {
        "TECHNICAL_APPENDIX_DPP_COMPARISON.md",
        "TECHNICAL_APPENDIX_OPTIMAL_RATE.md",
    },
    "paper_IV": {
        "TECHNICAL_APPENDIX_GAME_SCHEME.md",
        "TECHNICAL_APPENDIX_PURE_WEIGHTED.md",
    },
    "paper_V": {"TECHNICAL_APPENDIX_PATH_ACTUAL.md"},
}

MAX_REQUIRED = {
    "MAXIMAL_STRENGTHENING_STATUS.md": (
        "former_strengthening_blockers: 5",
        "external_peer_review: NOT_PERFORMED",
    ),
    "SPECULAR_SINAI_RADIAL_U3.md": (
        "SINAI-RADIAL-ASSEMBLED-U-INFINITY-1",
        "P1-SINAI-RADIAL-U3",
        "period-two orbit",
    ),
    "MOVING_FAMILY_HIGH_FREQUENCY_BDL.md": (
        "BDL-FAMILY-WITNESS-v1",
        "BDL-PARAMETER-DOMAIN-v1",
        "P2-BDL-HF-FAMILY",
        "ordered-composition resolvent formula",
        "Gauge conjugacy does not turn item 2 into item 3",
    ),
    "OPTIMAL_ENHANCED_WIP_RATE.md": (
        "P3-RWIP-OPTIMAL-WETA-P",
        "Stein--Dirichlet test class",
        "midpoint bridge defects",
    ),
    "PURE_STRATEGY_ISAACS.md": (
        "P4-PURE-ISAACS-MAXIMAL",
        "matching pennies",
        "pure Isaacs iff pure saddle",
    ),
    "WEIGHTED_NONCOMPACT_PATH_ACTUALIZATION.md": (
        "P4-WEIGHTED-NONCOMPACT-ACTUAL",
        "P5-PATH-ACTUAL",
        "horizontal shift generator",
        "two-sided deterministic Bernoulli shift",
    ),
    "maximal_strengthening_packet_v1.yaml": (
        "THETA_MAXIMAL_STRENGTHENING_PACKET_V2",
        "remaining_internal_mathematical_gaps: 0",
        "q_to_a_parameter_confusions: 0",
    ),
    "HOSTILE_STRENGTHENING_AUDIT.md": (
        "known_internal_strengthening_gaps_after_audit: 0",
        "external_peer_review: NOT_PERFORMED",
        "q_gauge_to_a_table_response_no_go_by_typing",
    ),
}

CONVENTION_ANCHORS = {
    "paper_I": ("X4 --G1--> X3", "finite-DQ"),
    "paper_II": ("quadratic partition", "D^{\\rm phys}(a)=\\frac12\\Sigma(a)"),
    "paper_III": ("direct triangular-characteristics", "4\\delta>0"),
    "paper_IV": ("vanishing slow initial layer", "mixed Isaacs equality"),
    "paper_V": ("generator orientation", "Z_s=\\sigma(s,X_s)^TDu"),
}

TECHNICAL_ANCHORS = {
    ("paper_I", "TECHNICAL_APPENDIX_SPECULAR_RADIAL_U3.md"): (
        "P1-SINAI-RADIAL-U3", "complete physical assembly",
    ),
    ("paper_II", "TECHNICAL_NOTE_RENEWAL.md"): (
        "distinct entry and exit", "\\mathcal O_{a,z}F",
    ),
    ("paper_II", "TECHNICAL_APPENDIX_HIGH_FREQUENCY_FAMILY.md"): (
        "P2-BDL-HF-FAMILY", "compact finite-cover uniformization",
        "BDL-PARAMETER-DOMAIN-v1", "q exact-coboundary derivatives",
    ),
    ("paper_III", "TECHNICAL_APPENDIX_DPP_COMPARISON.md"): (
        "Theorem A.3", "actual theta-expectation",
    ),
    ("paper_III", "TECHNICAL_APPENDIX_OPTIMAL_RATE.md"): (
        "P3-RWIP-OPTIMAL-WETA-P", "Stein--Dirichlet",
        "smooth cylindrical midpoint-defect",
    ),
    ("paper_IV", "TECHNICAL_APPENDIX_GAME_SCHEME.md"): (
        "Theorem B.2", "mixed-Isaacs",
    ),
    ("paper_IV", "TECHNICAL_APPENDIX_PURE_WEIGHTED.md"): (
        "P4-PURE-ISAACS-MAXIMAL", "P4-WEIGHTED-NONCOMPACT-ACTUAL",
    ),
    ("paper_V", "TECHNICAL_APPENDIX_PATH_ACTUAL.md"): (
        "P5-PATH-ACTUAL", "horizontal shift generator",
    ),
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def require(path: Path, anchors: tuple[str, ...], errors: list[str],
            hashes: dict[str, str]) -> str:
    if not path.is_file():
        fail(errors, f"missing file: {path.relative_to(ROOT)}")
        return ""
    text = path.read_text(encoding="utf-8")
    hashes[str(path.relative_to(ROOT))] = sha256(path)
    for anchor in anchors:
        if anchor not in text:
            fail(errors, f"missing anchor {anchor!r} in {path.relative_to(ROOT)}")
    return text


def main() -> int:
    errors: list[str] = []
    hashes: dict[str, str] = {}

    if not BASE.is_dir() or not MAX.is_dir():
        print(json.dumps({
            "status": "FAIL",
            "error": "missing five-paper or maximal-strengthening directory",
        }))
        return 1

    for name in sorted(REQUIRED_TOP):
        require(BASE / name, (), errors, hashes)

    for name, anchors in sorted(MAX_REQUIRED.items()):
        require(MAX / name, anchors, errors, hashes)

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
            "MANUSCRIPT.md", "BLOCKER_CLOSURE.md", "INTERFACE.md",
        } | EXTRA_REQUIRED.get(paper, set())

        texts: dict[str, str] = {}
        for filename in sorted(required):
            anchors = TECHNICAL_ANCHORS.get((paper, filename), ())
            text = require(directory / filename, anchors, errors, hashes)
            texts[filename] = text

            if filename == "MANUSCRIPT.md":
                if "## Abstract" not in text or "## Conclusion" not in text:
                    fail(errors, f"incomplete manuscript skeleton: {dirname}")
                for anchor in CONVENTION_ANCHORS[paper]:
                    if anchor not in text:
                        fail(errors, f"missing convention anchor {anchor!r} in {dirname}")
            elif filename == "BLOCKER_CLOSURE.md" and "CLOSED" not in text:
                fail(errors, f"no closure entries in {dirname}")

            for label in FORBIDDEN_LABELS:
                if label in text:
                    fail(errors, f"forbidden blanket label {label} in {dirname}/{filename}")

        interface = texts.get("INTERFACE.md", "")
        for token in EXPORTS[paper]:
            if f"`{token}`" not in interface:
                fail(errors, f"export {token} missing from {dirname}/INTERFACE.md")
        for token in IMPORTS[paper] | OPTIONAL_IMPORTS[paper]:
            if f"`{token}`" not in interface:
                fail(errors, f"import {token} missing from {dirname}/INTERFACE.md")

        for token in IMPORTS[paper] | OPTIONAL_IMPORTS[paper]:
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

    manifest = require(BASE / "THEOREM_INTERFACE_MANIFEST.yaml", (), errors, hashes)
    for token in producers:
        if token not in manifest:
            fail(errors, f"export {token} missing from theorem manifest")

    status_text = require(BASE / "FIVE_PAPER_CLOSURE_STATUS.md", (), errors, hashes)
    for required_status in (
        "actual_scoped_chain_through_theta: CLOSED",
        "actual_scoped_chain_through_mixed_Isaacs: CLOSED",
        "actual_scoped_chain_through_pure_Isaacs: CLOSED",
        "former_outside_theorem_strengthenings_closed: 5",
        "q_to_a_parameter_confusions: 0",
        "external_peer_review: NOT_PERFORMED",
        "formal_credit: 0",
    ):
        if required_status not in status_text:
            fail(errors, f"status boundary missing: {required_status}")

    result = {
        "schema": "THETA_FIVE_PAPER_VERIFY_V4",
        "status": "PASS" if not errors else "FAIL",
        "paper_count": len(PAPERS),
        "named_export_count": sum(map(len, EXPORTS.values())),
        "required_import_count": sum(map(len, IMPORTS.values())),
        "optional_import_count": sum(map(len, OPTIONAL_IMPORTS.values())),
        "paper_technical_file_count": sum(map(len, EXTRA_REQUIRED.values())),
        "maximal_strengthening_file_count": len(MAX_REQUIRED),
        "former_strengthening_items_closed": 5,
        "errors": errors,
        "sha256": dict(sorted(hashes.items())),
        "mathematical_proof_verified": False,
        "mathematical_proof_certified_externally": False,
        "external_peer_review": "NOT_PERFORMED",
        "formal_credit": 0,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
