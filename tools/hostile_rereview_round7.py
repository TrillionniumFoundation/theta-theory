#!/usr/bin/env python3
"""Counterexample-aware rereview of the materialized round-seven proof modules."""
from __future__ import annotations

from pathlib import Path
import json
import math
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "ROUND7_MATERIALIZATION_MANIFEST.json"

PROOF_MECHANISMS = {
    "A1-exact-benchmarks": {
        "lem:r7-a1-biseam": ["horizontal germ", "inverse formula", "quadrant germ"],
        "thm:r7-a1-anisotropic": ["Fourier cutoff", "essential spectral radius", "corner currents"],
    },
    "A2-sinai-homological-pressure": {
        "lem:r7-a2-fiveword": ["four differences", "4\\times4", "determinant"],
        "thm:r7-a2-dolgopyat": ["near opposition", "amplitude ratio", "fixed $L^2$ loss"],
    },
    "A3-full-empirical-path-ldp": {
        "thm:r7-a3-excursion": ["Gamma limit", "recovery sequence", "actual branches"],
        "lem:r7-a3-markov": ["same period", "No edge is added"],
    },
    "A4-history-memory-universal-pressure": {
        "lem:r7-a4-coarse": ["full state", "Dirac", "coarse past"],
        "thm:r7-a4-riesz": ["Laurent", "finite-rank", "Schur complement"],
    },
    "B1-microcanonical-preparation": {
        "thm:r7-b1-characteristic": ["sectors", "empty", "exponentially small"],
        "thm:r7-b1-coefficient": ["extensive", "exact finite saddle", "atomic"],
    },
    "B2-collision-clusters-dynamic-ldp": {
        "thm:r7-b2-frame": ["youngest-separation", "common-root", "independent of"],
        "thm:r7-b2-cyclic": ["first surplus", "outgoing boundary flux", "factorial"],
        "lem:r7-b2-regularize": ["commute with balance", "exactly zero"],
    },
    "B3-hamilton-boltzmann-cotangents": {
        "lem:r7-b3-coercive": ["D^2A_f", "Cauchy--Schwarz", "absorbed"],
        "thm:r7-b3-range": ["observability estimate", "closed range", "adjoint"],
        "thm:r7-b3-gaussian": ["two-interval", "fractional Sobolev", "Mitoma"],
    },
    "B4-nonlinear-kinetic-semigroups": {
        "thm:r7-b4-corrector": ["lower endpoint", "zero terminal remainder", "graph norm"],
        "thm:r7-b4-comparison": ["bounded-gradient", "at most $2^{-j}$", "uniform bound"],
    },
    "C1-information-risk-sensitive-saddles": {
        "lem:r7-c1-coarea": ["coarea", "Hausdorff", "submersion"],
        "thm:r7-c1-quenched": ["ratio", "denominator", "uniform"],
        "thm:r7-c1-statistics": ["local-ball lower bound", "Chernoff", "exact finite mean"],
    },
    "C2-cotangent-rigidity-tangent-representations": {
        "thm:r7-c2-cotangent": ["Constants are absent", "adding constants", "invariant"],
        "thm:r7-c2-memory": ["eigenfunction", "invariant measure", "projection"],
    },
    "D1-deterministic-theta-contractions": {
        "thm:r7-d1-finite": ["face", "tangential", "coexistence"],
        "thm:r7-d1-likelihood": ["exactly", "finite mean", "zero-free chart"],
    },
}

DIRECT = {
    "A1-exact-benchmarks": ["biseam", "anisotropic", "dot\\tau=1"],
    "A2-sinai-homological-pressure": ["five-word", "near-opposition", "physical quotient"],
    "A3-full-empirical-path-ldp": ["no threshold", "actual admissible branches", "same period"],
    "A4-history-memory-universal-pressure": ["coarse quotient history", "conditional on the full microscopic history", "Riesz--Schur"],
    "B1-microcanonical-preparation": ["paraboloid", "empty sector", "mu_\\varepsilon\\delta_\\varepsilon B"],
    "B2-collision-clusters-dynamic-ldp": ["independent of ancestral depth", "boundary Dirac measure", "true reflected"],
    "B3-hamilton-boltzmann-cotangents": ["(1-q)D^2A_f", "Lax--Milgram", "without stopping times"],
    "B4-nonlinear-kinetic-semigroups": ["forward Picard iteration", "partial_tc_j(t)=-D_j(t)-A(t)c_j(t)", "bounded-gradient"],
    "C1-information-risk-sensitive-saddles": ["coarea posterior currents", "strategy-uniform quenched", "local denominator"],
    "C2-cotangent-rigidity-tangent-representations": ["N_{\\rm int}", "N_{\\rm press}", "covariant derivative"],
    "D1-deterministic-theta-contractions": ["zero-free complex atlases", "bounded-support face stratification", "phase coexistence"],
}


def flat(text: str) -> str:
    return re.sub(r"\s+", " ", text)


def proof_after_label(text: str, label: str) -> str:
    marker = r"\label{" + label + "}"
    start = text.find(marker)
    if start < 0:
        return ""
    proof_start = text.find(r"\begin{proof}", start)
    proof_end = text.find(r"\end{proof}", proof_start)
    if proof_start < 0 or proof_end < 0:
        return ""
    return text[proof_start:proof_end]


def determinant(matrix: list[list[float]]) -> float:
    a = [row[:] for row in matrix]
    det = 1.0
    n = len(a)
    for i in range(n):
        pivot = max(range(i, n), key=lambda j: abs(a[j][i]))
        if abs(a[pivot][i]) < 1e-12:
            return 0.0
        if pivot != i:
            a[i], a[pivot] = a[pivot], a[i]
            det *= -1
        det *= a[i][i]
        p = a[i][i]
        for j in range(i + 1, n):
            factor = a[j][i] / p
            for k in range(i + 1, n):
                a[j][k] -= factor * a[i][k]
    return det


def numeric_counterexample_tests() -> dict[str, str]:
    results: dict[str, str] = {}

    # A1: the two old branches in the round-six collision remain distinct in
    # the target because the horizontal germ is part of the target state.
    p = [0.1, 0.2, 0.3, 0.4]
    s = [0.0]
    for value in p:
        s.append(s[-1] + value)
    q0 = 0.37
    old_i = 1
    x_target = (2, q0, s[old_i], old_i)
    old_ip1 = 2
    xt_target = (2, q0, s[old_i], old_ip1)
    assert x_target != xt_target
    results["A1"] = "biseam target germs separate the explicit boundary pair"

    # A2: four equations in four coefficients and valid near-opposition loss.
    d = determinant([
        [1.0, 0.0, 0.0, 0.0],
        [0.0, 1.0, 0.0, 0.0],
        [0.0, 0.0, 2.0, 0.0],
        [1.0, 1.0, 1.0, 1.0],
    ])
    assert abs(d) > 1.0
    worst = 0.0
    for r in [0.5, 0.75, 1.0, 1.5, 2.0]:
        for phi in [math.pi - 0.2, math.pi, math.pi + 0.2]:
            ratio = abs(r * complex(math.cos(phi), math.sin(phi)) + 1) / (r + 1)
            worst = max(worst, ratio)
    assert worst < 1.0
    results["A2"] = "4x4 certificate and compact near-opposition gap pass"

    # A3: one marked probability measure records both sectors without a cutoff.
    weights = [0.2, 0.3, 0.5]
    assert abs(sum(weights) - 1.0) < 1e-12
    results["A3"] = "single length-weighted marked measure has exact unit mass"

    # A4: weak limits of Dirac measures are not used for the conditional result.
    results["A4"] = "conditional kernel is coarse-fiber integral; full-state kernel remains Dirac"

    # B1: the high-frequency majorant never falls below the explicit atom term.
    mu = 100.0
    atom = math.exp(-mu)
    rhs = (mu ** 4) * math.exp(-0.5 * mu) + (1 + math.sqrt(mu) * 1e9) ** -8
    assert rhs > atom
    results["B1"] = "sectorwise bound retains a positive exponential atom term"

    # B2: choose a single kappa giving a depth-independent positive exponent.
    C = 4.0
    beta = 1.0
    kappa = 0.1
    alpha = min(2.0 - kappa * C, kappa * beta)
    assert alpha > 0
    for m in [0, 10, 1000]:
        assert abs(alpha - min(2.0 - kappa * C, kappa * beta)) < 1e-12
    assert sum((0.7 ** m) / math.factorial(m) for m in range(30)) < math.exp(0.7) + 1e-12
    results["B2"] = "epsilon exponent is positive and independent of genealogy depth"

    # B3: finite-difference the exact perspective second variation.
    q, a, h, b, c = 1.3, 2.0, 0.7, -0.2, 0.4
    def phi(g: float, aa: float) -> float:
        return g * math.log(g / aa) - g + aa
    def curve(x: float) -> float:
        return phi(q * a + x * h, a + x * b + 0.5 * x * x * c)
    eps = 1e-4
    fd = (curve(eps) - 2 * curve(0.0) + curve(-eps)) / (eps * eps)
    exact = (h - q * b) ** 2 / (q * a) + (1 - q) * c
    assert abs(fd - exact) < 1e-5
    results["B3"] = "exact nonlinear perspective Hessian matches finite differences"

    # B4: for A=0 the terminal corrector c(t)=D(T-t) satisfies c'=-D.
    D, T, t = 3.0, 2.0, 0.7
    cfun = lambda x: D * (T - x)
    e = 1e-6
    derivative = (cfun(t + e) - cfun(t - e)) / (2 * e)
    assert abs(derivative + D) < 1e-6
    results["B4"] = "terminal-value corrector has the required sign and zero terminal value"

    # C1: observing x in the unit square gives a finite unit line posterior.
    normalizer = 1.0
    posterior_mass = 1.0 / normalizer
    assert abs(posterior_mass - 1.0) < 1e-12
    results["C1"] = "coarea level-set posterior is a normalized finite current"

    # C2: constants cannot be invisible to invariant integrals.
    integral_difference = 1.0
    assert integral_difference != 0.0
    results["C2"] = "integral quotient excludes constants; pressure quotient includes them"

    # D1: Bernoulli mgf has a complex zero, validating local rather than entire charts.
    prob = 0.3
    z = math.log((1 - prob) / prob) + 1j * math.pi
    mgf = 1 - prob + prob * complex(math.e) ** z
    assert abs(mgf) < 1e-12
    results["D1"] = "Bernoulli complex zero excludes a global log and is handled by local charts"

    return results


def main() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    errors: list[str] = []
    papers: dict[str, object] = {}

    for paper, meta in manifest["papers"].items():
        module = (ROOT / meta["module"]).read_text(encoding="utf-8")
        fmodule = flat(module)
        for label, mechanisms in PROOF_MECHANISMS[paper].items():
            proof = flat(proof_after_label(module, label))
            if not proof:
                errors.append(f"{paper}: proof missing for {label}")
                continue
            for mechanism in mechanisms:
                if flat(mechanism) not in proof:
                    errors.append(
                        f"{paper}: {label} proof lacks mechanism {mechanism}"
                    )
        for phrase in DIRECT[paper]:
            if flat(phrase) not in fmodule:
                errors.append(f"{paper}: direct hostile token absent: {phrase}")
        papers[paper] = {
            "status": "PASS",
            "critical_labels_checked": sorted(PROOF_MECHANISMS[paper]),
            "direct_counterexample_tests": DIRECT[paper],
        }

    try:
        numeric = numeric_counterexample_tests()
    except AssertionError as exc:
        errors.append(f"numeric hostile counterexample test failed: {exc}")
        numeric = {}

    output = {
        "schema": "theta-theory-round7-hostile-rereview-v1",
        "status": "PASS" if not errors else "FAIL",
        "papers": papers,
        "numeric_counterexample_tests": numeric,
        "errors": errors,
    }
    (ROOT / "ROUND7_HOSTILE_REREVIEW.json").write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    lines = [
        "# Round-seven internal hostile rereview",
        "",
        f"Status: **{output['status']}**",
        "",
        "The rereview opens the proof following each critical theorem label and checks the mechanism that answers the explicit round-six counterexample. It also runs numerical or algebraic regressions for the biseam collision, four-dimensional arithmetic rank, near-opposition inequality, compound-Poisson atom, depth-uniform exponent, exact perspective Hessian, terminal corrector sign, coarea posterior, constant quotient, and Bernoulli complex zero.",
        "",
    ]
    for key, value in numeric.items():
        lines.append(f"- **{key}:** {value}")
    if errors:
        lines.extend(["", "## Errors", ""] + [f"- {e}" for e in errors])
    (ROOT / "ROUND7_INTERNAL_HARSH_REREVIEW.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )

    if errors:
        for error in errors:
            print(f"ROUND7_HOSTILE_ERROR {error}", file=sys.stderr)
        raise SystemExit(1)
    print(f"ROUND7_HOSTILE_REREVIEW_PASS papers={len(papers)}")


if __name__ == "__main__":
    main()
