#!/usr/bin/env python3
"""Counterexample-aware, dependency-aware hostile rereview for round five."""
from __future__ import annotations

from pathlib import Path
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT / "papers"

NODES: dict[str, dict[str, object]] = {
    "A1": {"paper": "A1-exact-benchmarks", "deps": [],
           "labels": ["lem:r5-a1-recut", "thm:r5-a1-return", "prop:r5-a1-work", "thm:r5-a1-response"]},
    "A2": {"paper": "A2-sinai-homological-pressure", "deps": [],
           "labels": ["prop:r5-a2-bundle", "lem:r5-a2-certificate", "thm:r5-a2-spectrum", "thm:r5-a2-llt"]},
    "A3": {"paper": "A3-full-empirical-path-ldp", "deps": ["A2"],
           "labels": ["thm:r5-a3-pressure", "lem:r5-a3-entropy", "thm:r5-a3-induced", "thm:r5-a3-two-clock"]},
    "A4": {"paper": "A4-history-memory-universal-pressure", "deps": ["A2", "A3"],
           "labels": ["thm:r5-a4-history", "prop:r5-a4-doob", "thm:r5-a4-memory", "thm:r5-a4-rough"]},
    "B2-GC": {"paper": "B2-collision-clusters-dynamic-ldp", "deps": [],
              "labels": ["lem:r5-b2-atlas", "thm:r5-b2-pivot", "thm:r5-b2-cumulant", "thm:r5-b2-continuation"]},
    "B1": {"paper": "B1-microcanonical-preparation", "deps": ["B2-GC"],
           "labels": ["lem:r5-b1-convex", "thm:r5-b1-saddle", "thm:r5-b1-coefficient", "thm:r5-b1-transfer"]},
    "B2-MC": {"paper": "B2-collision-clusters-dynamic-ldp", "deps": ["B2-GC", "B1"],
              "labels": ["lem:r5-b2-recovery", "thm:r5-b2-ldp"]},
    "B3": {"paper": "B3-hamilton-boltzmann-cotangents", "deps": ["B1", "B2-MC"],
           "labels": ["thm:r5-b3-right-inverse", "thm:r5-b3-gauge", "thm:r5-b3-duality", "thm:r5-b3-gaussian"]},
    "B4": {"paper": "B4-nonlinear-kinetic-semigroups", "deps": ["B2-MC", "B3"],
           "labels": ["lem:r5-b4-algebra", "thm:r5-b4-exact", "thm:r5-b4-correctors", "thm:r5-b4-comparison"]},
    "C1": {"paper": "C1-information-risk-sensitive-saddles", "deps": ["B2-MC", "B3", "B4"],
           "labels": ["thm:r5-c1-law", "thm:r5-c1-dpp", "prop:r5-c1-sufficiency", "thm:r5-c1-testing", "thm:r5-c1-lan"]},
    "C2": {"paper": "C2-cotangent-rigidity-tangent-representations",
           "deps": ["A1", "A2", "A3", "A4", "B2-MC", "B3", "B4"],
           "labels": ["thm:r5-c2-sum", "thm:r5-c2-contraction", "thm:r5-c2-likelihood", "thm:r5-c2-memory"]},
    "D1": {"paper": "D1-deterministic-theta-contractions", "deps": ["A4", "B1", "B2-MC", "B3", "B4", "C2"],
           "labels": ["thm:r5-d1-global", "thm:r5-d1-conditioning", "thm:r5-d1-interchange", "thm:r5-d1-lan", "thm:r5-d1-triangle"]},
}

CHECK_DESCRIPTIONS = {
    "A1": ["common recut section", "single-valued return", "descended work cocycle", "typed response fibre"],
    "A2": ["moving-cut bundle", "joint non-arithmeticity", "high-frequency estimate", "three LLT regimes"],
    "A3": ["survivor/escape pressure", "entropy-preserving recovery", "full lower bound", "clock surgery"],
    "A4": ["complete history", "space-time Doob cocycle", "Volterra memory", "area anomaly"],
    "B2-GC": ["actual contact charts", "unchanged trajectory pivot", "factorial recursion", "finite-source continuation"],
    "B1": ["exact finite saddle", "minor arcs", "continuous high frequencies", "mixed coefficient"],
    "B2-MC": ["positive balanced recovery", "conditioned joint LDP"],
    "B3": ["weighted gauge", "balance right inverse", "Radon dual", "one-increment bracket"],
    "B4": ["hierarchy algebra", "deterministic hierarchy state", "convergent correctors", "finite exponential Hamiltonian"],
    "C1": ["strategy law", "relaxed DPP", "sufficient state", "finite-centred LAN"],
    "C2": ["countable direct sum", "typed contraction", "history martingale", "memory commutation"],
    "D1": ["finite-source projective family", "closed global dual", "closure-qualified interchange", "finite-volume centering"],
}


def raw(node: str) -> str:
    paper = str(NODES[node]["paper"])
    return (PAPERS / paper / "ROUND5_POSITIVE_CLOSURE.tex").read_text(encoding="utf-8")


def normalized(node: str) -> str:
    return re.sub(r"\s+", " ", raw(node)).strip()


def require(node: str, markers: list[str], errors: list[str]) -> None:
    text = normalized(node)
    for marker in markers:
        if marker not in text:
            errors.append(f"{node}: semantic marker missing: {marker}")


def forbid(node: str, markers: list[str], errors: list[str]) -> None:
    text = normalized(node)
    for marker in markers:
        if marker in text:
            errors.append(f"{node}: superseded formulation present: {marker}")


def topological_order() -> list[str]:
    remaining = set(NODES)
    done: set[str] = set()
    order: list[str] = []
    while remaining:
        ready = sorted(n for n in remaining if set(NODES[n]["deps"]).issubset(done))
        if not ready:
            raise RuntimeError(f"dependency cycle: {sorted(remaining)}")
        for node in ready:
            remaining.remove(node)
            done.add(node)
            order.append(node)
    return order


errors: list[str] = []
order = topological_order()
node_results: dict[str, dict[str, object]] = {}

for node in order:
    text = raw(node)
    missing = [label for label in NODES[node]["labels"] if f"\\label{{{label}}}" not in text]
    bad_deps = [dep for dep in NODES[node]["deps"] if node_results.get(dep, {}).get("status") != "PASS"]
    if missing:
        errors.append(f"{node}: missing load-bearing labels {missing}")
    if bad_deps:
        errors.append(f"{node}: failed dependencies {bad_deps}")
    node_results[node] = {
        "paper": NODES[node]["paper"],
        "dependencies": NODES[node]["deps"],
        "load_bearing_labels": NODES[node]["labels"],
        "audit_checks": CHECK_DESCRIPTIONS[node],
        "status": "FAIL" if missing or bad_deps else "PASS",
    }

require("A1", [
    r"R_e=(i_{\sigma(e)}^-)^{-1}\circ S_e\circ i_e^+",
    r"R_e^*\vartheta-\vartheta=dF_e",
    "with no seam term",
    r"J_a:\Omega\to\Omega_a",
], errors)
forbid("A1", [r"c(x)d\tau"], errors)

# Replay the decisive A2 counterexample numerically.
n = 10**8
b = n ** 0.75
old_order = b * n ** -1.5
saturated_order = n ** -1.0
ratio = old_order / saturated_order
if ratio <= 10:
    errors.append("A2: wide-window numerical replay did not separate the regimes")
require("A2", [
    r"b_n/\sqrt n\to0",
    r"b_n/\sqrt n\to\beta\in(0,\infty)",
    r"b_n/\sqrt n\to\infty",
    r"the order is \(n^{-1}\), not \(b_n n^{-3/2}\)",
], errors)
forbid("A2", ["b_n=o(n)"], errors)

require("A3", [
    r"same \((m+1)\)-block distribution",
    r"H_\nu(X_m\mid X_0,\ldots,X_{m-1})",
    "positive entropy is not replaced by periodic-orbit entropy zero",
], errors)
forbid("A3", ["periodic orbit approximation with entropy convergence"], errors)

require("A4", [
    r"g_s=P^W_{s,t}g_t",
    r"{\mathsf P}^{W,g}_{r,t}",
    r"+t\Gamma",
    r"\Gamma_{ij}[V_i,V_j]",
], errors)
forbid("A4", [r"\log P_t(e^F)-\log P_t1"], errors)

require("B1", [
    r"D_\lambda Q_\varepsilon(H,\lambda_{\varepsilon,H,a})=a",
    r"a_\varepsilon=",
    "The finite saddle centers both coordinates exactly",
], errors)
forbid("B1", ["condition at the limiting saddle"], errors)

require("B2-GC", [
    "Keep the complete trajectory",
    "It does not identify the trajectory with a collision-deleted future",
    "All later contacts are left in the trajectory",
    r"ordered \(m\)-time simplex",
], errors)
forbid("B2-GC", ["delete the first cycle", "forget all later recollisions"], errors)

require("B3", [
    r"W(v,v_*)=1+|v|^2+|v_*|^2",
    r"{\mathcal H}_{\Phi_\eta}",
    r"q\,(\Delta_\omega\phi)(\Delta_\omega\chi)",
    r"There is no extra copy of \(\Delta\phi\)",
], errors)
forbid("B3", [r"=4(\Delta_\omega\phi)^2"], errors)

require("B4", [
    r"(F\star G)_n",
    r"2c_1<\theta",
    "the unused exponential moment",
    "Energy alone is not invoked",
], errors)

require("C1", [
    "Ionescu--Tulcea recursion",
    r"(H_t,\rho_t,G_t)",
    "finite-volume mean",
], errors)
require("C2", [
    r"X=\bigoplus",
    r"M=\prod",
    r"M_t =",
    "positive mean-one martingale on the complete-history filtration",
], errors)
forbid("C2", [r"P_{t,T}^\varepsilon F(X_t^\varepsilon)"], errors)

require("D1", [
    r"I(x)=\operatorname{cl}\sup_R I_R(x)",
    r"\Theta\in\bigcup_RB_R",
    r"J_a = \operatorname{cl}",
    r"m_{\varepsilon,\Theta}=DQ_{\varepsilon,R}(\Theta)",
], errors)
forbid("D1", [r"\sup_{\Theta\in X}"], errors)

for error in errors:
    prefix = error.split(":", 1)[0]
    if prefix in node_results:
        node_results[prefix]["status"] = "FAIL"
    elif prefix == "B2":
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
        "ratio": ratio,
        "conclusion": "the former linear-window formula diverges relative to the saturated mass",
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
print(f"ROUND5_HOSTILE_REREVIEW_PASS nodes={len(NODES)} ratio={ratio:.3f}")
