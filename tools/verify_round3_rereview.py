#!/usr/bin/env python3
"""Fail-closed verification for the exact-commit rereview replacements."""
from pathlib import Path
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT / "papers"
REPORT = ROOT / "ROUND3_REREVIEW_VERIFICATION.json"

required = {
    "A2-sinai-homological-pressure": [
        "all primitive triangular-lattice direction",
        "Uniform polygon generating functions",
        "bar\\tau=-\\partial_sP_R",
    ],
    "A3-full-empirical-path-ldp": [
        "Defect-completed renewal pressure",
        "Full collision empirical-path LDP",
        "escape-pressure dual",
        "Bounded terminal clock surgery",
    ],
    "A4-history-memory-universal-pressure": [
        "Strict-Ray history theorem",
        "bounded-strict topology",
        "No uniform-norm assertion is made at this level",
    ],
    "B1-microcanonical-preparation": [
        "Span-one particle-number gap",
    ],
    "B2-collision-clusters-dynamic-ldp": [
        "Bounded real-source continuation",
        "Positive collision right inverse",
        "Action-dense regular feasible pairs",
    ],
    "B3-hamilton-boltzmann-cotangents": [
        "Density of local balanced variations",
    ],
    "C1-information-risk-sensitive-saddles": [
        "block-normalized canonical law control",
        "exact conditional block normalizer",
        "No stochastic compensator is postulated",
    ],
    "C2-cotangent-rigidity-tangent-representations": [
        "weighted bounded-strict path-potential topology",
        "Memory is the Laplace transform of the pressure tangent",
        "L_\\Psi^{\\rm D}",
    ],
}

forbidden = {
    "A2-sinai-homological-pressure": [
        "A concrete temporal non-integrability rectangle",
        "((a,b)=\\nabla P_R",
    ],
    "A3-full-empirical-path-ldp": [
        "uniform integrability of both marks on its sublevels",
        "Full collision- and physical-time empirical-path LDP]\\n\\label{thm:r3-a3-two-clock}\\nThe collision empirical path measures satisfy",
    ],
    "A4-history-memory-universal-pressure": [
        "For every stationary prepared path law, the Ray completion just defined is a",
    ],
    "B2-collision-clusters-dynamic-ldp": [
        "Theorem~\\ref{thm:r3-b2-gc-cluster} remains normal on a slightly larger complex ball",
    ],
    "C1-information-risk-sensitive-saddles": [
        "sum_{c}\\log q",
        "int(q^{u,v}-1)dA_{\\pi^\\varepsilon}",
    ],
    "C2-cotangent-rigidity-tangent-representations": [
        "D\\mathcal E_t^\\Psi(0)[A](B)",
        "A strict path-potential topology",
    ],
}

errors = []
result = {"papers": {}}
for name, snippets in required.items():
    path = PAPERS / name / "ROUND3_POSITIVE_CLOSURE.tex"
    if not path.is_file():
        errors.append(f"{name}: module missing")
        continue
    text = path.read_text(encoding="utf-8")
    missing = [snippet for snippet in snippets if snippet not in text]
    bad = [snippet for snippet in forbidden.get(name, []) if snippet in text]
    controls = sorted({ord(ch) for ch in text if ord(ch) < 32 and ch != "\n"})
    if missing:
        errors.append(f"{name}: missing markers {missing}")
    if bad:
        errors.append(f"{name}: superseded text remains {bad}")
    if controls:
        errors.append(f"{name}: ASCII controls {controls}")
    result["papers"][name] = {
        "required": len(snippets),
        "missing": missing,
        "forbidden_present": bad,
        "ascii_controls": controls,
    }

# A3's direct collision rate must be the sole definition of the two-clock
# collision branch, and B2's two LDP labels must remain unique.
for name, labels in {
    "A3-full-empirical-path-ldp": [
        "thm:r3-a3-block",
        "thm:r3-a3-collision-ldp",
        "thm:r3-a3-two-clock",
    ],
    "B2-collision-clusters-dynamic-ldp": [
        "thm:r3-b2-gc-ldp",
        "thm:r3-b2-mc-ldp",
        "thm:r3-b2-source-continuation",
    ],
}.items():
    text = (PAPERS / name / "ROUND3_POSITIVE_CLOSURE.tex").read_text(encoding="utf-8")
    for label in labels:
        count = text.count("\\label{" + label + "}")
        if count != 1:
            errors.append(f"{name}: label {label} count={count}")

result["status"] = "PASS" if not errors else "FAIL"
result["errors"] = errors
REPORT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
if errors:
    for error in errors:
        print("ROUND3_REREVIEW_VERIFY_ERROR " + error, file=sys.stderr)
    raise SystemExit(1)
print("ROUND3_REREVIEW_VERIFICATION_PASS")
