#!/usr/bin/env python3
"""Fail-closed structural verification for the eleven round-three papers."""
from __future__ import annotations

from pathlib import Path
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
PAPERS = sorted(p for p in (ROOT / "papers").iterdir() if p.is_dir())
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

errors: list[str] = []
report: dict[str, object] = {"papers": {}, "checks": {}}
actual = {p.name for p in PAPERS}
if actual != EXPECTED:
    errors.append(f"paper directory mismatch: expected={sorted(EXPECTED)} actual={sorted(actual)}")

THEOREM_BEGIN = re.compile(
    r"\\begin\{(?:theorem|lemma|proposition|corollary)\}"
)
PROOF_BEGIN = re.compile(r"\\begin\{proof\}")
LABEL = re.compile(r"\\label\{([^}]+)\}")
REF = re.compile(r"\\(?:ref|cref)\{([^}]+)\}")
BANNED = {
    "TODO": "unfinished TODO",
    "FIXME": "unfinished FIXME",
    "TBD": "unfinished TBD",
    "NO_THEOREM_CREDIT": "non-theorem placeholder",
    "reviewer must verify": "reviewer-delegated proof",
    "external reviewers must verify": "reviewer-delegated proof",
    "assume the main gate": "assumed principal gate",
    "imported analytic packet": "unmaterialized analytic packet",
    "conditional only on": "conditional principal theorem",
}

for name in sorted(EXPECTED):
    paper = ROOT / "papers" / name
    main = paper / "main.tex"
    module = paper / "ROUND3_POSITIVE_CLOSURE.tex"
    if not main.is_file() or not module.is_file():
        errors.append(f"{name}: missing main or round3 module")
        continue
    main_text = main.read_text(encoding="utf-8")
    text = module.read_text(encoding="utf-8")

    if main_text.count(r"\input{ROUND3_POSITIVE_CLOSURE.tex}") != 1:
        errors.append(f"{name}: main does not contain exactly one controlling input")
    if "ROUND3-POSITIVE-CLOSURE" not in main_text:
        errors.append(f"{name}: controlling revision marker absent")
    if r"\begin{abstract}" not in main_text or r"\printbibliography" not in main_text:
        errors.append(f"{name}: regenerated document shell incomplete")

    theorem_count = len(THEOREM_BEGIN.findall(text))
    proof_count = len(PROOF_BEGIN.findall(text))
    if theorem_count == 0 or theorem_count != proof_count:
        errors.append(
            f"{name}: theorem/proof count mismatch {theorem_count}/{proof_count}"
        )

    labels = set(LABEL.findall(text))
    duplicate_labels = sorted(
        label for label in labels if text.count(r"\label{" + label + "}") > 1
    )
    if duplicate_labels:
        errors.append(f"{name}: duplicate labels {duplicate_labels}")

    missing_refs: list[str] = []
    for payload in REF.findall(text):
        for label in (x.strip() for x in payload.split(",")):
            if label and label not in labels:
                missing_refs.append(label)
    if missing_refs:
        errors.append(f"{name}: unresolved local refs {sorted(set(missing_refs))}")

    lowered = text.lower()
    for token, reason in BANNED.items():
        if token.lower() in lowered:
            errors.append(f"{name}: {reason}: {token}")

    report["papers"][name] = {
        "theorem_like_environments": theorem_count,
        "proof_environments": proof_count,
        "labels": len(labels),
        "local_references": sum(
            len([x for x in payload.split(",") if x.strip()])
            for payload in REF.findall(text)
        ),
        "bytes": len(text.encode("utf-8")),
    }

# Model-specific positive gates.
active = {
    name: (ROOT / "papers" / name / "ROUND3_POSITIVE_CLOSURE.tex").read_text(
        encoding="utf-8"
    )
    for name in EXPECTED
}
required_snippets = {
    "A1-exact-benchmarks": [
        "Autonomous Hamiltonian impact network",
        "Process-level Gibbs conditioning",
        "canonical mechanical cocycle",
    ],
    "A2-sinai-homological-pressure": [
        "Uniform temporal UNI",
        "Uniform vector--clock local limit",
        "moving-cut atlas",
    ],
    "A3-full-empirical-path-ldp": [
        "Terminal clock surgery",
        "Full collision- and physical-time empirical-path LDP",
        "Hausdorff cotangents",
    ],
    "A4-history-memory-universal-pressure": [
        "Compressed-resolvent generalized Langevin identity",
        "Weighted history Feller theorem",
        "Prepared rough diffusion tangent",
    ],
    "B1-microcanonical-preparation": [
        r"\lambda_H",
        "Source-dependent microcanonical transfer",
        "time-zero source test",
    ],
    "B2-collision-clusters-dynamic-ldp": [
        "First-cycle geometric gain",
        "All-contact exponential generating bound",
        "Microcanonical joint LDP",
    ],
    "B3-hamilton-boltzmann-cotangents": [
        "Exact gauge complex",
        r"\mathfrak G r=(r,-\Delta r)",
        "Prepared joint fluctuating Boltzmann limit",
    ],
    "B4-nonlinear-kinetic-semigroups": [
        "Recursive correlation correctors",
        "Comparison and uniqueness",
        "lifted static saddle",
    ],
    "C1-information-risk-sensitive-saddles": [
        "Game I: one-time preparation",
        "Game II: reward-only feedback",
        "Game III: canonical adaptive law control",
    ],
    "C2-cotangent-rigidity-tangent-representations": [
        "The platform coproduct",
        "Strict dual and compact phase sets",
        "Memory is the Laplace tangent of history pressure",
    ],
    "D1-deterministic-theta-contractions": [
        "Exact speed normalization",
        "Analytic--convex commutation theorem",
        "Gaussian tangent and likelihood-ratio convergence",
    ],
}
for name, snippets in required_snippets.items():
    for snippet in snippets:
        if snippet not in active[name]:
            errors.append(f"{name}: positive gate missing: {snippet}")

# Superseded formulations must not remain in the materialized main bodies.
for name in EXPECTED:
    main_text = (ROOT / "papers" / name / "main.tex").read_text(encoding="utf-8")
    for obsolete in (
        "Complete-observation no-go",
        "The same rate functional produces by contraction",
        "Paper I gives $o(\\mu_\\varepsilon)$ equivalence",
        r"D^2Q_T(\Theta)[F,G]=\Cov",
    ):
        if obsolete in main_text:
            errors.append(f"{name}: obsolete active formulation remains: {obsolete}")

manifest = ROOT / "ROUND3_REVISION_MANIFEST.yaml"
ledger = ROOT / "ROUND3_PROOF_DEPENDENCY_LEDGER.md"
if not manifest.is_file() or not ledger.is_file():
    errors.append("root manifest or dependency ledger missing")

report["checks"] = {
    "paper_count": len(EXPECTED),
    "errors": len(errors),
    "status": "PASS" if not errors else "FAIL",
}
(ROOT / "ROUND3_STRUCTURAL_VERIFICATION.json").write_text(
    json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
)

if errors:
    for error in errors:
        print(f"ROUND3_VERIFY_ERROR {error}", file=sys.stderr)
    raise SystemExit(1)

print("ROUND3_STRUCTURAL_VERIFICATION_PASS 11/11")
