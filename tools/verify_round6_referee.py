#!/usr/bin/env python3
"""Fail-closed verification of the materialized round-six manuscripts."""
from __future__ import annotations

from pathlib import Path
import hashlib
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT / "papers"
INVENTORY = json.loads((ROOT / "ROUND6_REFEREE_INVENTORY.json").read_text(encoding="utf-8"))
EXPECTED = set(INVENTORY["papers"])
CONTROL_RE = re.compile(rb"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")
THEOREM_RE = re.compile(r"\\begin\{(?:theorem|lemma|proposition|corollary)\}")
PROOF_RE = re.compile(r"\\begin\{proof\}")
LABEL_RE = re.compile(r"\\label\{([^}]+)\}")
REF_RE = re.compile(r"\\(?:ref|cref|Cref)\{([^}]+)\}")

REQUIRED = {
    "A1-exact-benchmarks": [
        "full regular Liouville path law",
        r"\alpha_a|_{\{i\}",
        "not restricted to a port core",
        "trace-jet Banach scale",
    ],
    "A2-sinai-homological-pressure": [
        "one fixed ambient distribution space",
        r"\mathbb B^{(2)}",
        "Paired cancellation operator",
        "Uniform master local-limit estimate",
        "relative asymptotic whenever",
    ],
    "A3-full-empirical-path-ldp": [
        r"\zeta_N",
        r"\int r\,dm+\zeta(1)=1",
        "admissible connector path",
        "Collision-time empirical-path LDP",
    ],
    "A4-history-memory-universal-pressure": [
        r"\eta_B(0)=PLQB",
        "Smith--McMillan",
        "transmission-zero modes",
        "Uniform conditional-kernel homogenization",
        "area drift",
    ],
    "B1-microcanonical-preparation": [
        r"\mathfrak p_{1,\varepsilon}",
        r"\lambda_{H,\varepsilon}",
        "exact Poisson series",
        "Exact-number shrinking-shell coefficient",
    ],
    "B2-collision-clusters-dynamic-ldp": [
        r"\|G\|_{\alpha,\beta}^{\rm tr}",
        "No corresponding estimate is claimed for arbitrary interior",
        "root-position translations",
        "Future-preserving cyclic-sector estimate",
        "Grand-canonical joint actual-contact LDP",
    ],
    "B3-hamilton-boltzmann-cotangents": [
        r"\mathcal U_\eta",
        r"\mathcal D_{\rm glob}",
        r"\bar\pi_\varepsilon",
        "No predictable Poisson compensator",
        "Time-localized cumulant bounds",
    ],
    "B4-nonlinear-kinetic-semigroups": [
        "genuine commutative algebra",
        "No finite hierarchy truncation is claimed",
        "ordinary weighted weak topology",
        "bounded collision increment",
        "Comparison on the bounded-increment core",
    ],
    "C1-information-risk-sensitive-saddles": [
        r"\mathcal B_{k,\varepsilon}^{u,v}",
        "conditioning on the new observation",
        "Chernoff information",
        r"DQ_\varepsilon(\theta_0)",
        "Finite-volume-centred canonical LAN",
    ],
    "C2-cotangent-rigidity-tangent-representations": [
        r"I_\alpha(\nu)\ge a_\alpha\nu(W_\alpha)-b_\alpha",
        "complete-history kernel",
        r"\mathcal H_D=L^2(\nu_\Psi^D)",
        "Typed pressure-tangent/memory commutation",
    ],
    "D1-deterministic-theta-contractions": [
        "Projective steep-pressure LDP",
        "Dawson--G",
        r"m_{\varepsilon,\theta}=DQ_{\varepsilon,m}(\theta)",
        "exactly the Radon--Nikodym density",
        "does not use a pressure outside",
    ],
}

FORBIDDEN = {
    "A1-exact-benchmarks": [r"\epsilon_i\chi_i(x)\rho(\tau)d\tau"],
    "A2-sinai-homological-pressure": [
        "assigned the zero trace space",
        r"\frac{2b_n}{(2\pi n)^{3/2}",
    ],
    "A3-full-empirical-path-ldp": [r"\delta_m e^{-W(B')}", "periodic orbit measures in the finite-depth survivor"],
    "A4-history-memory-universal-pressure": [
        "forcing is orthogonal to V at time zero",
        "covariance positivity excludes complex zeros",
    ],
    "B1-microcanonical-preparation": ["m0-particle singleton block is a connected cluster"],
    "B2-collision-clusters-dynamic-ldp": [
        "for every nonnegative L1 Liouville density",
        "forget a later contact",
    ],
    "B3-hamilton-boltzmann-cotangents": [
        "compensated actual-contact ledger",
        r"\zeta^\varepsilon=\sqrt{\mu_\varepsilon}(\pi^\varepsilon-f)",
    ],
    "B4-nonlinear-kinetic-semigroups": [
        "weak convergence augmented by convergence of the second moment",
        "finite hierarchy truncations are order-preserving",
    ],
    "C1-information-risk-sensitive-saddles": [
        "expected posterior error has the KL rate",
        r"X_\varepsilon-DQ(\theta_0)",
    ],
    "C2-cotangent-rigidity-tangent-representations": [
        r"P_{t,T}^\varepsilon F(X_t^\varepsilon)",
        r"\frac{P_t^\Psi A}{P_t^\Psi\mathbf1}\text{ is the Doob",
    ],
    "D1-deterministic-theta-contractions": [
        r"Z_\varepsilon=\sqrt{\mu_\varepsilon}(\mathcal X_\varepsilon-DQ(\Theta))",
        "assume rate-dense exposed points",
    ],
}

GENERIC_FORBIDDEN = [
    "TODO",
    "FIXME",
    "TBD",
    "NO_THEOREM_CREDIT",
    "reviewer must verify",
    "external reviewers must verify",
    "assume the principal theorem",
]

errors: list[str] = []
report: dict[str, object] = {"status": "FAIL", "papers": {}, "errors": errors}
actual_dirs = {p.name for p in PAPERS.iterdir() if p.is_dir()}
if actual_dirs != EXPECTED:
    errors.append(f"paper directories differ: expected={sorted(EXPECTED)} actual={sorted(actual_dirs)}")

all_labels: dict[str, str] = {}
total_theorems = 0
total_proofs = 0

for paper, item in INVENTORY["papers"].items():
    folder = PAPERS / paper
    source = ROOT / item["source"]
    module = folder / "ROUND6_POSITIVE_CLOSURE.tex"
    main = folder / "main.tex"
    latest_report = ROOT / item["report"]
    author_response = folder / "AUTHOR_RESPONSE_ROUND6.md"

    for required_file in (source, module, main, latest_report, author_response):
        if not required_file.is_file():
            errors.append(f"{paper}: missing {required_file.relative_to(ROOT)}")
    if not source.is_file() or not module.is_file() or not main.is_file():
        continue

    raw_source = source.read_bytes()
    raw_module = module.read_bytes()
    for path, raw in ((source, raw_source), (module, raw_module)):
        match = CONTROL_RE.search(raw)
        if match:
            errors.append(f"{paper}: ASCII control byte {match.group()[0]} in {path.relative_to(ROOT)}")

    source_text = raw_source.decode("utf-8")
    module_text = raw_module.decode("utf-8")
    expected_module = "% ROUND6-REFEREE-POSITIVE-CLOSURE\n" + source_text
    if module_text != expected_module:
        errors.append(f"{paper}: controlling module is not byte-identical to registered source")

    main_text = main.read_text(encoding="utf-8")
    if main_text.count(r"\input{ROUND6_POSITIVE_CLOSURE.tex}") != 1:
        errors.append(f"{paper}: main.tex does not load exactly one round-six module")
    if "ROUND6-REFEREE-POSITIVE-CLOSURE" not in main_text:
        errors.append(f"{paper}: controlling revision marker absent")
    if re.search(r"\\input\{ROUND[0-5]_POSITIVE_CLOSURE\.tex\}", main_text):
        errors.append(f"{paper}: superseded controlling input remains active")

    theorem_count = len(THEOREM_RE.findall(source_text))
    proof_count = len(PROOF_RE.findall(source_text))
    total_theorems += theorem_count
    total_proofs += proof_count
    if theorem_count == 0 or theorem_count != proof_count:
        errors.append(f"{paper}: theorem/proof mismatch {theorem_count}/{proof_count}")

    labels = LABEL_RE.findall(source_text)
    if len(labels) != len(set(labels)):
        errors.append(f"{paper}: duplicate local labels")
    for label in labels:
        if label in all_labels:
            errors.append(f"global duplicate label {label}: {all_labels[label]} and {paper}")
        all_labels[label] = paper

    missing_refs: set[str] = set()
    for payload in REF_RE.findall(source_text):
        for label in (part.strip() for part in payload.split(",")):
            if label and label not in set(labels):
                missing_refs.add(label)
    if missing_refs:
        errors.append(f"{paper}: unresolved local refs {sorted(missing_refs)}")

    for label in item["labels"]:
        if label not in labels:
            errors.append(f"{paper}: inventory label absent: {label}")
    for phrase in REQUIRED[paper]:
        if phrase not in source_text:
            errors.append(f"{paper}: required counterexample repair absent: {phrase}")
    for phrase in FORBIDDEN[paper]:
        if phrase in source_text:
            errors.append(f"{paper}: superseded formulation present: {phrase}")
    lowered = source_text.lower()
    for phrase in GENERIC_FORBIDDEN:
        if phrase.lower() in lowered:
            errors.append(f"{paper}: forbidden placeholder: {phrase}")

    report["papers"][paper] = {
        "source_sha256": hashlib.sha256(raw_source).hexdigest(),
        "module_sha256": hashlib.sha256(raw_module).hexdigest(),
        "source_bytes": len(raw_source),
        "theorem_like_environments": theorem_count,
        "proofs": proof_count,
        "labels": len(labels),
        "references": sum(len(x.split(",")) for x in REF_RE.findall(source_text)),
    }

# Explicit acyclic dependency check.
graph = {
    "A1": [],
    "A2": [],
    "A3": ["A2"],
    "A4": ["A2", "A3"],
    "B2-GC": [],
    "B1": ["B2-GC"],
    "B2-MC": ["B2-GC", "B1"],
    "B3": ["B1", "B2-MC"],
    "B4": ["B2-MC", "B3"],
    "C1": ["B2-MC", "B3", "B4"],
    "C2": ["A4", "B3", "B4"],
    "D1": ["A2", "A3", "A4", "B1", "B2-MC", "B3", "B4", "C2"],
}
visiting: set[str] = set()
visited: set[str] = set()

def visit(node: str) -> None:
    if node in visiting:
        errors.append(f"dependency cycle at {node}")
        return
    if node in visited:
        return
    visiting.add(node)
    for dep in graph[node]:
        visit(dep)
    visiting.remove(node)
    visited.add(node)

for node in graph:
    visit(node)

report.update({
    "status": "PASS" if not errors else "FAIL",
    "paper_count": len(EXPECTED),
    "total_theorem_like_environments": total_theorems,
    "total_proofs": total_proofs,
    "dependency_dag": "PASS" if not any("dependency cycle" in e for e in errors) else "FAIL",
})
(ROOT / "ROUND6_STRUCTURAL_VERIFICATION.json").write_text(
    json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
)

if errors:
    for error in errors:
        print(f"ROUND6_VERIFY_ERROR {error}", file=sys.stderr)
    raise SystemExit(1)

print(
    "ROUND6_STRUCTURAL_VERIFICATION_PASS "
    f"papers=11 theorem_proof={total_theorems}/{total_proofs}"
)
