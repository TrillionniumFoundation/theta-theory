#!/usr/bin/env python3
"""Fail-closed structural and mathematical-regression gate for round five."""
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
        "Common recut section",
        "Single-valued Hamiltonian first return",
        "Descent and concatenation",
        "Common-fibre response identity",
    ],
    "A2-sinai-homological-pressure": [
        "Moving-cut Lasota--Yorke bundle",
        "Certified joint non-arithmeticity",
        "Three disjoint window regimes",
        "b_n/\\sqrt n\\to\\infty",
    ],
    "A3-full-empirical-path-ldp": [
        "Renewal--survivor pressure identity",
        "Markov recovery with entropy convergence",
        "Full induced path LDP",
        "Bounded terminal clock surgery",
    ],
    "A4-history-memory-universal-pressure": [
        "Space-time harmonic normalization",
        "Doob cocycle and nonlinear tower",
        "Time-domain Volterra memory",
        "area anomaly",
    ],
    "B1-microcanonical-preparation": [
        "Exact finite-volume saddle",
        "Global continuous-frequency decay",
        "Source-uniform finite-saddle coefficient",
        "lambda_{\\varepsilon,H,a}",
    ],
    "B2-collision-clusters-dynamic-ldp": [
        "Regular contact atlas and singular codimension",
        "Pivotal contact-coordinate estimate",
        "Factorial contact recursion",
        "Finite-source block continuation",
    ],
    "B3-hamilton-boltzmann-cotangents": [
        "Typed collision increment",
        "Bounded right inverse of the balance map",
        "Closed weighted gauge complex",
        "(\\Delta_\\omega\\phi)(\\Delta_\\omega\\chi)",
    ],
    "B4-nonlinear-kinetic-semigroups": [
        "Correlation convolution algebra",
        "Convergent connected corrector series",
        "Maxwellian kinetic semigroup",
        "e^{\\theta|v|^2}",
    ],
    "C1-information-risk-sensitive-saddles": [
        "Pathwise-consistent controlled law",
        "Relaxed Elliott--Kalton DPP",
        "Sufficiency and deterministic continuation",
        "Canonical-chart LAN",
    ],
    "C2-cotangent-rigidity-tangent-representations": [
        "Typed direct-sum duality",
        "Finite history likelihood and optional projection",
        "History-pressure/memory identity",
        "complete-history",
    ],
    "D1-deterministic-theta-contractions": [
        "Global rate from compatible finite-source balls",
        "Closed affine interchange",
        "Uniform local likelihood expansion",
        "operatorname{cl}",
    ],
}

FORBIDDEN = {
    "A2-sinai-homological-pressure": [
        "b_n=o(n)",
        "2b_n}{(2\\pi n)^{3/2}",
    ],
    "A3-full-empirical-path-ldp": [
        "periodic orbit measures approximate",
        "periodic orbit approximation with entropy convergence",
    ],
    "A4-history-memory-universal-pressure": [
        "\\log P_t(e^F)-\\log P_t1",
    ],
    "B1-microcanonical-preparation": [
        "condition at the limiting saddle",
    ],
    "B2-collision-clusters-dynamic-ldp": [
        "delete the first cycle",
        "forget all later recollisions",
    ],
    "B3-hamilton-boltzmann-cotangents": [
        "\\Delta p+\\Delta p_*",
        "4(\\Delta_\\omega\\phi)^2",
    ],
    "B4-nonlinear-kinetic-semigroups": [
        "energy alone controls",
    ],
    "C2-cotangent-rigidity-tangent-representations": [
        "P_{t,T}^\\varepsilon F(X_t^\\varepsilon)",
    ],
    "D1-deterministic-theta-contractions": [
        "\\sup_{\\Theta\\in X}",
    ],
}

THEOREM = re.compile(r"\\begin\{(?:theorem|lemma|proposition|corollary)\}")
PROOF = re.compile(r"\\begin\{proof\}")
LABEL = re.compile(r"\\label\{([^}]+)\}")
REF = re.compile(r"\\(?:ref|cref)\{([^}]+)\}")

errors: list[str] = []
report: dict[str, object] = {"schema": "theta-theory-round5-verification-v1", "papers": {}}

actual = {p.name for p in PAPERS.iterdir() if p.is_dir()}
if not EXPECTED.issubset(actual):
    errors.append(f"paper directories missing: {sorted(EXPECTED-actual)}")

total_theorems = 0
total_proofs = 0
for paper in sorted(EXPECTED):
    folder = PAPERS / paper
    main = folder / "main.tex"
    module = folder / "ROUND5_POSITIVE_CLOSURE.tex"
    response = folder / "AUTHOR_RESPONSE_ROUND5.md"
    referee = folder / "REFEREE_REPORT_ROUND4_GPT56_PRO.md"
    for path in (main, module, response, referee):
        if not path.is_file():
            errors.append(f"{paper}: missing {path.name}")
    if not main.is_file() or not module.is_file():
        continue

    main_text = main.read_text(encoding="utf-8")
    text = module.read_text(encoding="utf-8")
    if main_text.count(r"\input{ROUND5_POSITIVE_CLOSURE.tex}") != 1:
        errors.append(f"{paper}: main does not load exactly one round-five module")
    if r"\input{ROUND3_POSITIVE_CLOSURE.tex}" in main_text:
        errors.append(f"{paper}: superseded round-three module remains active")
    if "ROUND5-REFEREE-POSITIVE-CLOSURE" not in main_text:
        errors.append(f"{paper}: controlling revision marker missing")

    controls = sorted({ord(ch) for ch in text if ord(ch) < 32 and ch not in "\n\t"})
    if controls:
        errors.append(f"{paper}: ASCII controls {controls}")

    theorem_count = len(THEOREM.findall(text))
    proof_count = len(PROOF.findall(text))
    total_theorems += theorem_count
    total_proofs += proof_count
    if theorem_count == 0 or theorem_count != proof_count:
        errors.append(f"{paper}: theorem/proof mismatch {theorem_count}/{proof_count}")

    labels = LABEL.findall(text)
    duplicates = sorted({x for x in labels if labels.count(x) > 1})
    if duplicates:
        errors.append(f"{paper}: duplicate labels {duplicates}")
    label_set = set(labels)
    missing_refs: list[str] = []
    for payload in REF.findall(text):
        for ref in (x.strip() for x in payload.split(",")):
            if ref and ref not in label_set:
                missing_refs.append(ref)
    if missing_refs:
        errors.append(f"{paper}: unresolved local refs {sorted(set(missing_refs))}")

    missing = [s for s in REQUIRED[paper] if s not in text]
    forbidden = [s for s in FORBIDDEN.get(paper, []) if s in text]
    if missing:
        errors.append(f"{paper}: required markers missing {missing}")
    if forbidden:
        errors.append(f"{paper}: forbidden regressions present {forbidden}")

    lowered = text.lower()
    for token in ("todo", "fixme", "tbd", "reviewer must verify", "no theorem credit"):
        if token in lowered:
            errors.append(f"{paper}: unfinished/delegated marker {token}")

    report["papers"][paper] = {
        "lines": len(text.splitlines()),
        "bytes": len(text.encode("utf-8")),
        "theorem_like_environments": theorem_count,
        "proofs": proof_count,
        "labels": len(labels),
        "references": sum(len([x for x in p.split(",") if x.strip()]) for p in REF.findall(text)),
        "required_markers": len(REQUIRED[paper]),
        "forbidden_regressions": len(forbidden),
        "ascii_controls": controls,
    }

for root_file in (
    "ROUND5_REFEREE_INVENTORY.json",
    "ROUND5_HISTORICAL_DERIVATION_AUDIT.md",
    "ROUND5_PROOF_DEPENDENCY_LEDGER.md",
    "REFEREE_ROUND5_RESPONSE.md",
):
    if not (ROOT / root_file).is_file():
        errors.append(f"missing root record {root_file}")

report["paper_count"] = len(EXPECTED)
report["total_theorem_like_environments"] = total_theorems
report["total_proofs"] = total_proofs
report["status"] = "PASS" if not errors else "FAIL"
report["errors"] = errors
(ROOT / "ROUND5_STRUCTURAL_VERIFICATION.json").write_text(
    json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
)

if errors:
    for error in errors:
        print("ROUND5_VERIFY_ERROR " + error, file=sys.stderr)
    raise SystemExit(1)
print(f"ROUND5_STRUCTURAL_VERIFICATION_PASS papers=11 theorems={total_theorems} proofs={total_proofs}")
