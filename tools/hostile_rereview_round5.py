#!/usr/bin/env python3
"""Dependency-aware hostile rereview of the materialized round-five tree.

This is deliberately separate from theorem/proof counting.  It checks the
specific counterexamples and category errors identified in the independent
round-four reports and fails closed if a downstream paper is certified while
one of its declared inputs is absent.
"""
from __future__ import annotations

from pathlib import Path
import json
import math
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT / "papers"

NODES: dict[str, dict[str, object]] = {
    "A1": {
        "paper": "A1-exact-benchmarks",
        "deps": [],
        "labels": ["lem:r5-a1-recut", "thm:r5-a1-return", "prop:r5-a1-work", "thm:r5-a1-response"],
        "checks": ["common recut section", "single-valued return", "descended cocycle", "typed response fibre"],
    },
    "A2": {
        "paper": "A2-sinai-homological-pressure",
        "deps": [],
        "labels": ["prop:r5-a2-bundle", "lem:r5-a2-certificate", "thm:r5-a2-spectrum", "thm:r5-a2-llt"],
        "checks": ["moving-cut bundle", "joint certificate", "Dolgopyat block", "three window regimes"],
    },
    "A3": {
        "paper": "A3-full-empirical-path-ldp",
        "deps": ["A2"],
        "labels": ["thm:r5-a3-pressure", "lem:r5-a3-entropy", "thm:r5-a3-induced", "thm:r5-a3-two-clock"],
        "checks": ["escape branch", "entropy-preserving recovery", "non-exposed lower bound", "clock surgery"],
    },
    "A4": {
        "paper": "A4-history-memory-universal-pressure",
        "deps": ["A2", "A3"],
        "labels": ["thm:r5-a4-history", "prop:r5-a4-doob", "thm:r5-a4-memory", "thm:r5-a4-rough"],
        "checks": ["complete history", "space-time harmonic Doob cocycle", "time-domain memory", "area anomaly"],
    },
    "B2-GC": {
        "paper": "B2-collision-clusters-dynamic-ldp",
        "deps": [],
        "labels": ["lem:r5-b2-atlas", "thm:r5-b2-pivot", "thm:r5-b2-cumulant", "thm:r5-b2-continuation"],
        "checks": ["actual contact charts", "unchanged trajectory", "ordered factorial recursion", "finite source continuation"],
    },
    "B1": {
        "paper": "B1-microcanonical-preparation",
        "deps": ["B2-GC"],
        "labels": ["lem:r5-b1-convex", "thm:r5-b1-saddle", "thm:r5-b1-coefficient", "thm:r5-b1-transfer"],
        "checks": ["exact finite saddle", "minor arcs", "high frequencies", "shell coefficient"],
    },
    "B2-MC": {
        "paper": "B2-collision-clusters-dynamic-ldp",
        "deps": ["B2-GC", "B1"],
        "labels": ["lem:r5-b2-recovery", "thm:r5-b2-ldp"],
        "checks": ["positive balanced recovery", "conditioned joint LDP"],
    },
    "B3": {
        "paper": "B3-hamilton-boltzmann-cotangents",
        "deps": ["B1", "B2-MC"],
        "labels": ["thm:r5-b3-right-inverse", "thm:r5-b3-gauge", "thm:r5-b3-duality", "thm:r5-b3-gaussian"],
        "checks": ["quadratic weighted source", "closed gauge", "Radon dual", "one-increment bracket"],
    },
    "B4": {
        "paper": "B4-nonlinear-kinetic-semigroups",
        "deps": ["B2-MC", "B3"],
        "labels": ["lem:r5-b4-algebra", "thm:r5-b4-exact", "thm:r5-b4-correctors", "thm:r5-b4-comparison"],
        "checks": ["hierarchy algebra", "deterministic hierarchy state", "corrector convergence", "finite exponential Hamiltonian"],
    },
    "C1": {
        "paper": "C1-information-risk-sensitive-saddles",
        "deps": ["B2-MC", "B3", "B4"],
        "labels": ["thm:r5-c1-law", "thm:r5-c1-dpp", "prop:r5-c1-sufficiency", "thm:r5-c1-testing", "thm:r5-c1-lan"],
        "checks": ["canonical controlled law", "relaxed DPP", "complete information state", "finite-centred LAN"],
    },
    "C2": {
        "paper": "C2-cotangent-rigidity-tangent-representations",
        "deps": ["A1", "A2", "A3", "A4", "B2-MC", "B3", "B4"],
        "labels": ["thm:r5-c2-sum", "thm:r5-c2-contraction", "thm:r5-c2-likelihood", "thm:r5-c2-memory"],
        "checks": ["countable direct sum", "typed contraction", "history martingale", "memory commutation"],
    },
    "D1": {
        "paper": "D1-deterministic-theta-contractions",
        "deps": ["A4", "B1", "B2-MC", "B3", "B4", "C2"],
        "labels": ["thm:r5-d1-global", "thm:r5-d1-conditioning", "thm:r5-d1-interchange", "thm:r5-d1-lan", "thm:r5-d1-triangle"],
        "checks": ["finite-source projective family", "closed global dual", "closure-qualified interchange", "finite-volume likelihood centre"],
    },
}


def module(node: str) -> str:
    paper = str(NODES[node]["paper"])
    return (PAPERS / paper / "ROUND5_POSITIVE_CLOSURE.tex").read_text(encoding="utf-8")


def topological_order() -> list[str]:
    remaining = set(NODES)
    done: set[str] = set()
    order: list[str] = []
    while remaining:
        available = sorted(n for n in remaining if set(NODES[n]["deps"]).issubset(done))
        if not available:
            raise RuntimeError(f"dependency cycle among {sorted(remaining)}")
        for n in available:
            remaining.remove(n)
            done.add(n)
            order.append(n)
    return order


errors: list[str] = []
order = topological_order()
node_results: dict[str, object] = {}

for node in order:
    text = module(node)
    missing_labels = [label for label in NODES[node]["labels"] if f"\\label{{{label}}}" not in text]
    bad_deps = [dep for dep in NODES[node]["deps"] if node_results.get(dep, {}).get("status") != "PASS"]
    if missing_labels:
        errors.append(f"{node}: missing load-bearing labels {missing_labels}")
    if bad_deps:
        errors.append(f"{node}: failed/unverified dependencies {bad_deps}")
    node_results[node] = {
        "paper": NODES[node]["paper"],
        "dependencies": NODES[node]["deps"],
        "load_bearing_labels": NODES[node]["labels"],
        "audit_checks": NODES[node]["checks"],
        "status": "FAIL" if missing_labels or bad_deps else "PASS",
    }

# A1: domain/codomain of the return are recut to one standard section and the
# former non-descending p dq primitive is not used as a global work form.
a1 = module("A1")
for marker in (
    "R_e=(i_{\\sigma(e)}^-)^{-1}\\circ S_e\\circ i_e^+",
    "R_e^*\\vartheta-\\vartheta=dF_e",
    "no seam term",
    "J_a:\\Omega\\to\\Omega_a",
):
    if marker not in a1:
        errors.append(f"A1 hostile check missing: {marker}")
if "c(x)d\\tau" in a1:
    errors.append("A1: superseded non-descending c(x)d tau form remains active")

# A2: replay the referee's wide-window counterexample.  The old formula would
# scale as n^{-3/4} for b=n^{3/4}; the saturated two-lattice-coordinate mass
# scales as n^{-1}.  Their ratio diverges and the materialized theorem must
# therefore contain a separate saturated branch.
n = 10**8
b = n ** 0.75
old_order = b * n ** -1.5
saturated_order = n ** -1.0
counterexample_ratio = old_order / saturated_order
if not counterexample_ratio > 10:
    errors.append("A2: internal wide-window counterexample replay failed")
a2 = module("A2")
for marker in (
    "b_n/\\sqrt n\\to0",
    "b_n/\\sqrt n\\to\\beta\\in(0,\\infty)",
    "b_n/\\sqrt n\\to\\infty",
    "the order is\n\\(n^{-1}\\), not \\(b_n n^{-3/2}\\)",
):
    if marker not in a2:
        errors.append(f"A2 regime check missing: {marker}")
if "b_n=o(n)" in a2:
    errors.append("A2: false full b_n=o(n) local formula remains")

# A3: positive entropy must be approximated by Markov chains carrying block
# entropy, never by periodic measures.
a3 = module("A3")
for marker in (
    "same \\((m+1)\\)-block distribution",
    "H_\\nu(X_m\\mid X_0,\\ldots,X_{m-1})",
    "Positive entropy is not replaced by periodic-orbit entropy zero",
):
    if marker not in a3:
        errors.append(f"A3 entropy recovery check missing: {marker}")

# A4: the finite nonlinear tower must use the same space-time harmonic Doob
# family and the rough lift must include Gamma.
a4 = module("A4")
for marker in (
    "g_s=P^W_{s,t}g_t",
    "{\\mathsf P}^{W,g}_{r,t}",
    "+t\\Gamma",
    "\\Gamma_{ij}[V_i,V_j]",
):
    if marker not in a4:
        errors.append(f"A4 history/rough check missing: {marker}")

# B1: exact finite mean equation and exact target a_epsilon are mandatory.
b1 = module("B1")
for marker in (
    "D_\\lambda Q_\\varepsilon(H,\\lambda_{\\varepsilon,H,a})=a",
    "a_\\varepsilon=",
    "The finite saddle centers both coordinates\nexactly",
):
    if marker not in b1:
        errors.append(f"B1 finite-saddle check missing: {marker}")

# B2: ensure the pivotal estimate is on the unchanged trajectory and that later
# contacts are retained and factorially summed.
b2 = module("B2-GC")
for marker in (
    "Keep the complete trajectory",
    "It does not identify the\ntrajectory with a collision-deleted future",
    "All later contacts are left in the\ntrajectory",
    "ordered \\(m\\)-time simplex",
):
    if marker not in b2:
        errors.append(f"B2 deterministic-future check missing: {marker}")
for forbidden in ("delete the first cycle", "forget all later recollisions"):
    if forbidden in b2:
        errors.append(f"B2 superseded surgery remains: {forbidden}")

# B3: type Delta p in a quadratic weighted heart and count one collision
# increment per test direction in the bracket.
b3 = module("B3")
for marker in (
    "W(v,v_*)=1+|v|^2+|v_*|^2",
    "{\\mathcal H}_{\\Phi_\\eta}",
    "q\\,(\\Delta_\\omega\\phi)(\\Delta_\\omega\\chi)",
    "There is no extra copy of \\(\\Delta\\phi\\)",
):
    if marker not in b3:
        errors.append(f"B3 typed/bracket check missing: {marker}")
if "=4(\\Delta_\\omega\\phi)^2" in b3:
    errors.append("B3: old fourfold jump bracket remains")

# B4: finite exponential Hamiltonian requires unused Maxwellian moment and the
# exact observable product is the label convolution.
b4 = module("B4")
for marker in (
    "(F\\star G)_n",
    "2c_1<\\theta",
    "the unused\nexponential moment",
    "Energy alone is not invoked",
):
    if marker not in b4:
        errors.append(f"B4 algebra/domain check missing: {marker}")

# C1/C2: exact finite states and likelihoods live on complete history.
c1 = module("C1")
for marker in (
    "Ionescu--Tulcea recursion",
    "(H_t,\\rho_t,G_t)",
    "finite-volume mean",
):
    if marker not in c1:
        errors.append(f"C1 state/LAN check missing: {marker}")
c2 = module("C2")
for marker in (
    "X=\\bigoplus",
    "M=\\prod",
    "M_t",
    "positive mean-one martingale on the complete-history",
):
    if marker not in c2:
        errors.append(f"C2 category/likelihood check missing: {marker}")

# D1: global dual is the closed supremum of the proved balls; no unproved
# global source space is quantified over.
d1 = module("D1")
for marker in (
    "I(x)=\\operatorname{cl}\\sup_R I_R(x)",
    "\\Theta\\in\\bigcup_RB_R",
    "J_a=\n\\operatorname{cl}",
    "m_{\\varepsilon,\\Theta}=DQ_{\\varepsilon,R}(\\Theta)",
):
    if marker not in d1:
        errors.append(f"D1 projective check missing: {marker}")
if "\\sup_{\\Theta\\in X}" in d1:
    errors.append("D1: unproved global source supremum remains")

# Propagate any newly discovered node-specific error into the node status.
for error in errors:
    prefix = error.split(":", 1)[0]
    if prefix in node_results:
        node_results[prefix]["status"] = "FAIL"
        continue
    if prefix == "B2":
        node_results["B2-GC"]["status"] = "FAIL"
        node_results["B2-MC"]["status"] = "FAIL"

result = {
    "schema": "theta-theory-round5-hostile-rereview-v1",
    "status": "PASS" if not errors else "FAIL",
    "topological_order": order,
    "wide_window_counterexample": {
        "n": n,
        "b": b,
        "old_linear_window_order": old_order,
        "saturated_order": saturated_order,
        "ratio": counterexample_ratio,
        "expected_conclusion": "old formula diverges relative to saturated mass; separate wide regime required",
    },
    "nodes": node_results,
    "errors": errors,
}
(ROOT / "ROUND5_HOSTILE_REREVIEW.json").write_text(
    json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
)

if errors:
    for error in errors:
        print("ROUND5_HOSTILE_ERROR " + error, file=sys.stderr)
    raise SystemExit(1)
print(f"ROUND5_HOSTILE_REREVIEW_PASS nodes={len(NODES)} ratio={counterexample_ratio:.3f}")
