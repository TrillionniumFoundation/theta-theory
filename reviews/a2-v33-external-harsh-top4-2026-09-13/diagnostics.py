#!/usr/bin/env python3
"""Independent finite diagnostics for the A2 v33 referee report.

Run with ordinary Python and with python -O. Uses explicit checks, not assert.
These calculations are not a native-manuscript build or a proof verifier.
The counterexamples remove stated hypotheses; they do not refute the paper.
"""
from __future__ import annotations

import json
import math
from fractions import Fraction as F


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def finite_couplings() -> list[dict[str, str]]:
    weights = [F(1, 4), F(1, 2), F(1, 4)]
    y = [(F(0), F(2)), (F(1), F(1)), (F(2), F(0))]
    records = []
    for eps in [F(1, 2), F(1, 4), F(1, 16)]:
        x = [(eps, 2-eps), (F(1), F(1)), (2-eps, eps)]
        for i in range(2):
            mx = sum(w*xx[i] for w, xx in zip(weights, x))
            my = sum(w*yy[i] for w, yy in zip(weights, y))
            require(mx == my == 1, "Likelihood normalization failed")
            # The deterministic matching kernel is the same at both alternatives.
            tv = sum(w*abs(xx[i]-yy[i])
                     for w, xx, yy in zip(weights, x, y))/2
            require(tv == eps/4, "Coupling total-variation bound failed")
        cost = sum(w*sum(abs(a-b) for a, b in zip(xx, yy))
                   for w, xx, yy in zip(weights, x, y))
        require(cost == eps, "L1 coupling cost failed")
        records.append({"epsilon": str(eps), "L1_cost": str(cost),
                        "each_alternative_TV": str(eps/4),
                        "reference_TV": "0"})
    return records


def normalization_stress() -> list[dict[str, str | int]]:
    records = []
    for n in [10, 100, 1000]:
        # P0(A)=1/n, L=n 1_A, P1(A)=1. L converges weakly to zero.
        mean = F(1, n)*n
        tv = (abs(F(1)-F(1, n)) + abs(F(0)-F(n-1, n)))/2
        require(mean == 1 and tv == 1-F(1, n), "Lost-mean example failed")
        records.append({"n": n, "prelimit_mean": "1",
                        "limit_mean": "0", "TV": str(tv)})
    return records


def compact_stress() -> dict[str, str]:
    # K={0} union {1/m}. At n only parameter 1/n outputs 1.
    # A reverse kernel from a one-point limit must use one Bernoulli(q).
    risks = [max(F(i, 100), 1-F(i, 100)) for i in range(101)]
    require(min(risks) == F(1, 2), "Compact counterexample minimax failed")
    return {"forward_deficiency": "0", "reverse_deficiency": "1/2",
            "finite_restrictions": "eventually trivial",
            "excluded_by": "uniform continuity modulus hypothesis"}


def waiting_affinity() -> dict[str, object]:
    p, q = F(9, 25), F(16, 25)
    numerator, tail_ratio = F(12, 25), F(12, 25)
    require(numerator**2 == p*q, "Geometric numerator failed")
    require(tail_ratio**2 == (1-p)*(1-q), "Geometric tail failed")
    affinity = numerator/(1-tail_ratio)
    require(affinity == F(12, 13), "Geometric affinity failed")
    # Sum_t binom(t-1,k-1) a^k r^(t-k) = [a/(1-r)]^k.
    records = []
    for k in [1, 2, 5]:
        ak = affinity**k
        records.append({"successes": k, "exact_affinity": str(ak),
                        "exact_H_squared": str(2-2*ak)})
        p_star = 0.8
        bound = k*(math.log(float(p))-math.log(float(q)))**2/(4*(1-p_star))
        require(float(2-2*ak) <= bound, "Waiting Hellinger bound failed")
    return {"p": str(p), "q": str(q), "records": records}


def corner_and_bulk_stress() -> dict[str, object]:
    corner = []
    for k in [20, 100, 1000]:
        radius = F(2)
        # q(x,r)=2 1_{0<r<x<1}; corner x<=R/k.
        mass = (radius/k)**2
        require(k*mass == radius**2/k, "Corner scaling failed")
        corner.append({"k": k, "one_record_corner_mass": str(mass),
                       "scaled_corner_mass": str(k*mass)})
    # Disk ceiling w=1-u^2-v^2, rho=2/pi. Odd-u perturbation is normalized.
    # E u^2 = (2/pi) int_0^{2pi} cos^2(t)dt int_0^1 r^3(1-r^2)dr.
    information = 2*(F(1, 4)-F(1, 6))
    require(information == F(1, 6), "Bulk score information failed")
    return {"corner": corner, "omitted_bulk_hypothesis_information": str(information),
            "bulk_stress_scope": "O(k^-1/2) perturbation violates the paper's O(k^-1) relative bound"}


def matching_stress() -> dict[str, str]:
    eps = F(1, 100)
    # J(x)=(x,0); Jtilde(x)=(x,eps*cos(pi*x/eps)).
    # The squared distance to zero is even; the point 0 is not a minimizer.
    f0, fhalf = eps**2, eps**2/4
    require(fhalf < f0, "C0 matching witness failed")
    return {"epsilon": str(eps), "objective_at_zero": str(f0),
            "objective_at_plus_minus_epsilon_over_two": str(fhalf),
            "conclusion": "at least two minimizers on the symmetric compact interval",
            "scope": "C0-small, not C2-small: does not refute the stated matching lemma"}


def compatible_rates() -> list[dict[str, float | int]]:
    records = []
    for k in [10**3, 10**6, 10**12]:
        delta = math.sqrt(2/(k*math.log(k)))
        j = 2*math.ceil(3*math.log(k))
        records.append({"k": k, "j": j,
                        "critical_scale": k*delta**2*math.log(1/delta),
                        "j_delta": j*delta,
                        "fast_mark_budget": (1+math.log(j*math.sqrt(k)))/j**2,
                        "finite_bridge_budget_tau_exp_minus_one": math.exp(math.log(k)-j)})
        require(j % 2 == 0 and 0 < delta < 1, "Rate construction failed")
    return records


def main() -> None:
    result = {
        "status": "passed",
        "submission_commit": "b577cffcb3ca5597cb4905269bea9de3bd4ead38",
        "scope": "Independent exact identities, hypothesis stress tests and illustrative finite rates; not a full proof or native build.",
        "finite_likelihood_couplings": finite_couplings(),
        "normalization_stress": normalization_stress(),
        "compactness_stress": compact_stress(),
        "waiting_affinity": waiting_affinity(),
        "corner_and_bulk": corner_and_bulk_stress(),
        "signature_matching_stress": matching_stress(),
        "illustrative_rates": compatible_rates(),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
