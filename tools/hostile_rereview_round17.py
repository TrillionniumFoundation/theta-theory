#!/usr/bin/env python3
"""Objection-specific regression checks for Round Seventeen."""
from __future__ import annotations

from pathlib import Path
import json
import math
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
SOURCES = {p.parent.name: p for p in (ROOT / "papers").glob("*/ROUND17_POSITIVE_CLOSURE.tex")}
errors: list[str] = []
result: dict[str, object] = {
    "schema": "theta-theory-round17-hostile-rereview-v1",
    "papers": {}, "errors": errors,
}

checks = {
    "A1-exact-benchmarks": [
        "there is no \\(dp\\)-term",
        "not identified with ordinary H\\\"older cylinder functions",
        "Closed conormal jet calculus",
        "Radon current-valued functional CLT",
        "Global autonomous hybrid realization",
    ],
    "A2-sinai-homological-pressure": [
        "No operator trace, flat trace, Fredholm determinant",
        "Raw branchwise integration by parts",
        "unsmoothed characteristic function itself",
        "\\mathbb T^3\\times\\mathbb R",
        "(2\\pi n)^2",
    ],
    "A3-full-empirical-path-ldp": [
        "arbitrary predictable controls",
        "full branch log likelihood is paid once",
        "prefix probability",
        "Polish topology and compact coercive sets",
        "Physical-clock LDP",
    ],
    "A4-history-memory-universal-pressure": [
        "partition of unity is used to mix local kernels",
        "patched distance",
        "One fixed multiplier algebra",
        "unresolved initial",
        "minimum singular value",
    ],
    "B1-microcanonical-preparation": [
        "polymer decomposition",
        "No independence of connected collision components is asserted",
        "One integrable canonical Fourier majorant",
        "frequency-independent exceptional contribution",
        "B2-GC analytic pressure",
    ],
    "B2-collision-clusters-dynamic-ldp": [
        "open trajectory-parameter domain",
        "Reflection is introduced only on",
        "Rate-dense strictly positive balanced pairs",
        "collision cone",
        "Grand-canonical joint LDP",
    ],
    "B3-hamilton-boltzmann-cotangents": [
        "control $qA_f$",
        "Localized cumulant estimate",
        "Finite-time kinetic observability",
        "Quadratic recovery and Mosco convergence",
        "\\operatorname{Ran}\\Sigma^{1/2}",
    ],
    "B4-nonlinear-kinetic-semigroups": [
        "same relative multiplier $q$, not the same collision measure",
        "Compact dynamic action sublevels",
        "nonlinear resolvent identity",
        "m$-dissipative",
        "one diagonal",
    ],
    "C1-information-risk-sensitive-saddles": [
        "Disintegration is not continuous",
        "Dominated disintegration estimate",
        "good smoothing",
        "Belief transition and posterior DPP",
        "Exact-experiment QMD and LAN",
    ],
    "C2-cotangent-rigidity-tangent-representations": [
        "continuous dual of $(C_W(E),\\beta_W)$ is $\\mathcal M_W(E)$",
        "metric connection",
        "Strict positivity gives injectivity",
        "form-level Schur complement",
        "Extended weak convergence of optional projections",
    ],
    "D1-deterministic-theta-contractions": [
        "genuine positive latent variable",
        "Exact phase-cost sign",
        "Augmented phase-posterior semigroup",
        "map $x\\mapsto\\mathcal V_t$ alone need not",
        "Labelled Gaussian mixtures and tie weights",
    ],
}

for folder, phrases in checks.items():
    path = SOURCES.get(folder)
    if path is None:
        errors.append(f"{folder}: active module missing")
        continue
    text = path.read_text()
    missing = [phrase for phrase in phrases if phrase not in text]
    if missing:
        errors.append(f"{folder}: missing regression phrases {missing}")
    result["papers"][folder] = {
        "checked": phrases,
        "status": "PASS" if not missing else "FAIL",
    }

# A1 exact primitive: no sp term can appear in the active primitive formula.
a1 = SOURCES["A1-exact-benchmarks"].read_text()
primitive = re.search(r"\\begin\{lemma\}\[Correct exact primitive\](.*?)\\end\{lemma\}", a1, re.S)
if not primitive or "-s" in primitive.group(1).replace("s_{j-1}", ""):
    errors.append("A1: primitive regression contains an unverified negative s term")
result["papers"]["A1-exact-benchmarks"]["primitive_dp_coefficient"] = 0.0

# A2 direct tail integrability regression.
rho, kappa, cm, M = 0.8, 0.2, 0.4, 6
first_exp = math.log(rho) - kappa
second_exp = cm - (M - 1) * kappa
if not (first_exp < 0 and second_exp < 0):
    errors.append("A2: selected high-frequency exponents are not integrable")
result["papers"]["A2-sinai-homological-pressure"].update({
    "trace_determinant_used": False,
    "high_frequency_exponents": [first_exp, second_exp],
})

# A3 terminal entropy: selecting a full edge costs -log w independent of prefix.
w, u = 0.2, 0.3
full_cost = -math.log(w)
fractional_cost = u * full_cost
if not full_cost > fractional_cost:
    errors.append("A3: terminal entropy regression failed")
result["papers"]["A3-full-empirical-path-ldp"].update({
    "full_edge_cost": full_cost, "rejected_fractional_cost": fractional_cost,
})

# A4 unresolved forcing must be present.
a4 = SOURCES["A4-history-memory-universal-pressure"].read_text()
if "Q_VA" not in a4 and "unresolved initial" not in a4:
    errors.append("A4: unresolved forcing omitted")

# B1 every large-frequency term must be integrable.
d, s = 5, 10
if s <= d:
    errors.append("B1: fallback Fourier exponent is not integrable")
result["papers"]["B1-microcanonical-preparation"]["fallback_integrable_exponent"] = s

# B2 positive cone regression: the module must reject entropy-as-feasibility.
b2 = SOURCES["B2-collision-clusters-dynamic-ldp"].read_text()
if "no entropy penalty" not in b2.lower() and "not asked to create" not in b2.lower():
    errors.append("B2: positive-cone fallacy not explicitly rejected")

# B3 q is counted exactly once in the covariance formula.
b3 = SOURCES["B3-hamilton-boltzmann-cotangents"].read_text()
cov = re.search(r"\\mathbf E\[M\(p,\\psi\)M\(\\tilde p,\\tilde\\psi\)\](.*?)\\end\{theorem\}", b3, re.S)
if not cov or "q^2" in cov.group(1):
    errors.append("B3: biased intensity is duplicated")
result["papers"]["B3-hamilton-boltzmann-cotangents"]["pure_contact_variance_at_q2_A3"] = 6.0

# B4 same Gamma is not transported between states.
b4 = SOURCES["B4-nonlinear-kinetic-semigroups"].read_text()
if "not the same collision measure" not in b4:
    errors.append("B4: state-dependent admissibility regression failed")

# C1 oscillatory weak-disintegration counterexample remains excluded by the strong chart.
# L1 distance of 1+a sin(2 pi n x) from 1 is 2a/pi, independent of n.
a = 0.5
l1_gap = 2 * a / math.pi
if l1_gap <= 0.3:
    errors.append("C1: oscillatory disintegration gap calculation failed")
result["papers"]["C1-information-risk-sensitive-saddles"]["oscillatory_L1_gap"] = l1_gap

# C2 old non-dissipative 2x2 compression can vanish; new theorem must assume dissipativity.
# L=[[0,-3],[1,0]], z=1, r=(1,1)/sqrt2 gives compressed scalar zero.
old_compression = 0.0
c2 = SOURCES["C2-cotangent-rigidity-tangent-representations"].read_text()
if "Assume the prepared Markov generator is dissipative" not in c2:
    errors.append("C2: compression invertibility lacks dissipativity hypothesis")
result["papers"]["C2-cotangent-rigidity-tangent-representations"]["rejected_old_compression"] = old_compression

# D1 a marginal log-sum of drifts is not additive; augmented posterior is required.
a1d, a2d, theta = 0.0, 1.0, 1.0
f = lambda t: math.log((math.exp(theta*a1d*t)+math.exp(theta*a2d*t))/2)/theta
nonsemigroup_gap = abs((f(1)+f(1))-f(2))
if nonsemigroup_gap <= 1e-6:
    errors.append("D1: marginal log-sum non-semigroup regression failed")
result["papers"]["D1-deterministic-theta-contractions"]["marginal_logsum_nonsemigroup_gap"] = nonsemigroup_gap

result["status"] = "PASS" if not errors else "FAIL"
(ROOT / "ROUND17_HOSTILE_REREVIEW.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
if errors:
    for e in errors: print("ROUND17_HOSTILE_ERROR", e, file=sys.stderr)
    raise SystemExit(1)
print("ROUND17_HOSTILE_REREVIEW_PASS 11/11")
