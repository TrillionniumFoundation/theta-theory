#!/usr/bin/env python3
"""Fail-closed exact-source verification for the round-five referee revision."""
from __future__ import annotations

from pathlib import Path
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT / "papers"
EXPECTED = {
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
}

REQUIRED = {
    "A1-exact-benchmarks": [
        "Symplectic recutting", "Autonomous recut suspension",
        "Descending work form and section cocycle", "All-order typed response",
        "Mechanical--valuation compatibility",
    ],
    "A2-sinai-homological-pressure": [
        "All-depth moving-cut bundle", "Certified UNI and full lattice span",
        "Uniform high-frequency contraction",
        "Uniform vector--roof local limit in three regimes",
        "if \\(b_n/\\sqrt n\\to\\infty\\)",
    ],
    "A3-full-empirical-path-ldp": [
        "Common operator domains and renewal decomposition",
        "Rate-dense exposed Markov phases",
        "Infinite cost of unresolved singular mass",
        "Full collision empirical-path LDP",
        "Full physical-time empirical-path LDP",
    ],
    "A4-history-memory-universal-pressure": [
        "Measured Ray realization", "History Feller and eigenfunction intertwining",
        "Volterra kernel without formal orthogonal dynamics",
        "Meromorphic continuation and decaying memory",
        "Prepared rough diffusion tangent", "Short-memory and conditional semigroup convergence",
    ],
    "B1-microcanonical-preparation": [
        "Uniform strict constraint convexity", "Uniform mixed Cram",
        "Uniform central characteristic expansion",
        "Source-uniform primitive shell coefficient",
        "Exact source-dependent microcanonical pressure",
    ],
    "B2-collision-clusters-dynamic-ldp": [
        "Quantitative genealogical Gramian", "First-surplus contact tube",
        "Boundary-flux exponential ledger", "Whole cyclic sector estimate",
        "Source-sewing theorem", "Finite-cell conservative repair",
        "Grand-canonical density--actual-contact LDP", "Microcanonical joint LDP",
    ],
    "B3-hamilton-boltzmann-cotangents": [
        "Typing of the collision increment", "Exact weighted gauge complex",
        "No finitely additive collision dual", "Hard-sphere cohomological kernel",
        "Aldous--Mitoma bounds", "Prepared joint fluctuating Boltzmann limit",
    ],
    "B4-nonlinear-kinetic-semigroups": [
        "Exact law-state tower", "Triangular correlation-corrector expansion",
        "The bounded-increment Hamiltonian core", "Hamiltonian finiteness and continuity",
        "Corrected nonlinear-generator convergence", "Comparison and uniqueness",
    ],
    "C1-information-risk-sensitive-saddles": [
        "Measurable posterior hierarchy", "Posterior-normalized likelihood",
        "Strategy-uniform posterior stability", "Adaptive posterior-state game",
        "Uniform posterior phase contraction", "Uniform canonical LAN",
        "Canonical Bernstein--von Mises theorem",
    ],
    "C2-cotangent-rigidity-tangent-representations": [
        "Typed strict dual", "Exact likelihood martingale",
        "Conditional-kernel Markovization", "Pressure tangent equals the Doob semigroup",
        "Compressed resolvent and memory commutation", "Likelihood and BSDE diagram",
    ],
    "D1-deterministic-theta-contractions": [
        "The exhausted source domain", "Exhaustion lemma",
        "Local analytic commutation", "Conditioning--contraction commutation",
        "Finite-dimensional Gaussian likelihood theorem", "Rate--pressure--semigroup triangle",
    ],
}

LOAD_BEARING = {
    "A1-exact-benchmarks": ["thm:r5-a1-suspension", "thm:r5-a1-response"],
    "A2-sinai-homological-pressure": ["thm:r5-a2-bundle", "thm:r5-a2-dolgopyat", "thm:r5-a2-llt"],
    "A3-full-empirical-path-ldp": ["thm:r5-a3-collision-ldp", "thm:r5-a3-physical-ldp"],
    "A4-history-memory-universal-pressure": ["thm:r5-a4-memory-decay", "thm:r5-a4-rough", "thm:r5-a4-short-memory"],
    "B1-microcanonical-preparation": ["thm:r5-b1-coefficient", "thm:r5-b1-transfer"],
    "B2-collision-clusters-dynamic-ldp": ["thm:r5-b2-cyclic", "thm:r5-b2-sewing", "thm:r5-b2-gc-ldp"],
    "B3-hamilton-boltzmann-cotangents": ["thm:r5-b3-duality", "thm:r5-b3-kernel", "thm:r5-b3-gaussian"],
    "B4-nonlinear-kinetic-semigroups": ["thm:r5-b4-generator", "thm:r5-b4-comparison", "thm:r5-b4-limit"],
    "C1-information-risk-sensitive-saddles": ["thm:r5-c1-adaptive", "thm:r5-c1-lan", "thm:r5-c1-bvm"],
    "C2-cotangent-rigidity-tangent-representations": ["thm:r5-c2-markovization", "thm:r5-c2-memory", "thm:r5-c2-girsanov"],
    "D1-deterministic-theta-contractions": ["thm:r5-d1-exhaustion", "thm:r5-d1-contraction", "thm:r5-d1-triangle"],
}

BANNED = [
    "TODO", "FIXME", "TBD", "NO_THEOREM_CREDIT",
    "reviewer must verify", "external reviewers must verify",
    "assume the main gate", "imported analytic packet",
    "proof is omitted", "left to the reader",
]

THEOREM_BEGIN = re.compile(r"\\begin\{(?:theorem|lemma|proposition|corollary)\}")
PROOF_BEGIN = re.compile(r"\\begin\{proof\}")
LABEL = re.compile(r"\\label\{([^}]+)\}")
REF = re.compile(r"\\(?:ref|eqref|cref)\{([^}]+)\}")


def proof_after_label(text: str, label: str) -> str | None:
    pos = text.find("\\label{" + label + "}")
    if pos < 0:
        return None
    begin = text.find("\\begin{proof}", pos)
    if begin < 0:
        return None
    next_statement = re.search(r"\\begin\{(?:theorem|lemma|proposition|corollary)\}", text[pos + 1:])
    if next_statement is not None and pos + 1 + next_statement.start() < begin:
        return None
    end = text.find("\\end{proof}", begin)
    if end < 0:
        return None
    return text[begin:end]


def main() -> None:
    errors: list[str] = []
    report: dict[str, object] = {
        "schema": "theta-theory-round5-referee-verification-v1",
        "status": "PENDING",
        "papers": {},
    }
    actual = {p.name for p in PAPERS.iterdir() if p.is_dir()}
    if actual != EXPECTED:
        errors.append(f"paper directory mismatch expected={sorted(EXPECTED)} actual={sorted(actual)}")

    total_theorems = 0
    total_proofs = 0
    all_labels: dict[str, str] = {}
    for name in sorted(EXPECTED):
        paper = PAPERS / name
        source = paper / "ROUND3_POSITIVE_CLOSURE.tex"
        manuscript = paper / "main.tex"
        response = paper / "AUTHOR_RESPONSE_ROUND5.md"
        if not source.is_file() or not manuscript.is_file() or not response.is_file():
            errors.append(f"{name}: missing controlling source, main, or response")
            continue
        text = source.read_text(encoding="utf-8")
        main_text = manuscript.read_text(encoding="utf-8")
        controls = sorted({ord(ch) for ch in text if ord(ch) < 32 and ch != "\n"})
        if controls:
            errors.append(f"{name}: ASCII controls {controls}")
        if main_text.count(r"\input{ROUND3_POSITIVE_CLOSURE.tex}") != 1:
            errors.append(f"{name}: controlling input count mismatch")
        if "ROUND5-REFEREE-POSITIVE-CLOSURE" not in main_text:
            errors.append(f"{name}: round-five marker missing from main")
        if "August 31, 2026" not in main_text:
            errors.append(f"{name}: date not refreshed")
        for marker in REQUIRED[name]:
            if marker not in text:
                errors.append(f"{name}: required marker missing: {marker}")
        lowered = text.lower()
        for token in BANNED:
            if token.lower() in lowered:
                errors.append(f"{name}: banned unfinished phrase: {token}")

        theorem_count = len(THEOREM_BEGIN.findall(text))
        proof_count = len(PROOF_BEGIN.findall(text))
        total_theorems += theorem_count
        total_proofs += proof_count
        if theorem_count == 0 or theorem_count != proof_count:
            errors.append(f"{name}: theorem/proof mismatch {theorem_count}/{proof_count}")

        labels = LABEL.findall(text)
        dup = sorted({x for x in labels if labels.count(x) > 1})
        if dup:
            errors.append(f"{name}: duplicate labels {dup}")
        for label in labels:
            if label in all_labels:
                errors.append(f"global duplicate label {label}: {all_labels[label]} and {name}")
            all_labels[label] = name
        local = set(labels)
        missing_refs: list[str] = []
        for payload in REF.findall(text):
            for ref in (x.strip() for x in payload.split(",")):
                if ref and ref not in local:
                    missing_refs.append(ref)
        if missing_refs:
            errors.append(f"{name}: unresolved local refs {sorted(set(missing_refs))}")

        proof_lengths: dict[str, int] = {}
        for label in LOAD_BEARING[name]:
            proof = proof_after_label(text, label)
            if proof is None:
                errors.append(f"{name}: load-bearing proof missing for {label}")
                continue
            length = len(re.sub(r"\s+", " ", proof))
            proof_lengths[label] = length
            if length < 500:
                errors.append(f"{name}: load-bearing proof too short {label}: {length}")
            if "\\[" not in proof and "\\(" not in proof:
                errors.append(f"{name}: load-bearing proof has no displayed or inline mathematics: {label}")

        report["papers"][name] = {
            "bytes": len(text.encode("utf-8")),
            "lines": text.count("\n") + 1,
            "theorem_like_environments": theorem_count,
            "proofs": proof_count,
            "labels": len(labels),
            "references": sum(len([x for x in p.split(",") if x.strip()]) for p in REF.findall(text)),
            "required_markers": len(REQUIRED[name]),
            "load_bearing_proof_lengths": proof_lengths,
        }

    # Explicit regression checks for the objections that admitted direct counterexamples.
    a2 = (PAPERS / "A2-sinai-homological-pressure" / "ROUND3_POSITIVE_CLOSURE.tex").read_text(encoding="utf-8")
    for marker in ("b_n=o(\\sqrt n)", "b_n/\\sqrt n\\to\\beta", "b_n/\\sqrt n\\to\\infty"):
        if marker not in a2:
            errors.append(f"A2: missing one of the three window regimes: {marker}")
    if "the joint probability is of order \\(n^{-1}\\), not" not in a2:
        errors.append("A2: wide-window saturation correction absent")

    b1 = (PAPERS / "B1-microcanonical-preparation" / "ROUND3_POSITIVE_CLOSURE.tex").read_text(encoding="utf-8")
    if "lambda_{H,\\varepsilon}" not in b1 or "exact finite-volume saddle" not in b1:
        errors.append("B1: exact finite-volume saddle not controlling the proof")

    b2 = (PAPERS / "B2-collision-clusters-dynamic-ldp" / "ROUND3_POSITIVE_CLOSURE.tex").read_text(encoding="utf-8")
    if "retain the actual reflected state" not in b2 or "No pseudo-trajectory is" not in b2:
        errors.append("B2: future-preserving surplus-contact statement absent")

    b3 = (PAPERS / "B3-hamilton-boltzmann-cotangents" / "ROUND3_POSITIVE_CLOSURE.tex").read_text(encoding="utf-8")
    if "h^2+\\frac h{\\mu_\\varepsilon}" not in b3:
        errors.append("B3: finite-particle fourth-increment term absent")

    c2 = (PAPERS / "C2-cotangent-rigidity-tangent-representations" / "ROUND3_POSITIVE_CLOSURE.tex").read_text(encoding="utf-8")
    if "M_t^\\varepsilon" not in c2 or "positive uniformly integrable martingale" not in c2:
        errors.append("C2: exact finite history likelihood martingale absent")

    for root_file in (
        "ROUND5_REFEREE_INVENTORY.md",
        "ROUND5_HISTORICAL_DERIVATION_AUDIT.md",
        "ROUND5_PROOF_DEPENDENCY_LEDGER.md",
        "ROUND5_MATERIALIZATION.json",
    ):
        if not (ROOT / root_file).is_file():
            errors.append(f"root artifact missing: {root_file}")

    report["paper_count"] = len(EXPECTED)
    report["total_theorem_like_environments"] = total_theorems
    report["total_proofs"] = total_proofs
    report["errors"] = errors
    report["status"] = "PASS" if not errors else "FAIL"
    (ROOT / "ROUND5_STRUCTURAL_VERIFICATION.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    if errors:
        for error in errors:
            print("ROUND5_VERIFY_ERROR " + error, file=sys.stderr)
        raise SystemExit(1)
    print(f"ROUND5_STRUCTURAL_VERIFICATION_PASS papers=11 theorems={total_theorems} proofs={total_proofs}")


if __name__ == "__main__":
    main()
