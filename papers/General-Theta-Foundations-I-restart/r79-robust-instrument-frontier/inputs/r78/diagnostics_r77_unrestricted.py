#!/usr/bin/env python3
"""Finite exact-rational diagnostics; not a proof or exhaustive optimization.

The theorem is the written argument in 51-unrestricted-approximation.tex.
These checks target its arithmetic convention, error normalization, extremal
factorizations, and the original algebraic phase that lacked a prior lower
certificate.  No assertion is used, so -O does not disable a check.
"""
from __future__ import annotations

from fractions import Fraction as F
from itertools import combinations
from math import comb
from pathlib import Path
import hashlib
import json
import sys


COUNTS: dict[str, int] = {}


def check(ok: bool, category: str, detail: str = "") -> None:
    if not ok:
        raise RuntimeError(f"{category}: {detail}")
    COUNTS[category] = COUNTS.get(category, 0) + 1


def a_threshold(j: int) -> int:
    m = 1
    while comb(m, m // 2) < j:
        m += 1
    return m


def support_diagnostics() -> None:
    for m in range(2, 9):
        k = m // 2
        sets = tuple(frozenset(s) for s in combinations(range(m), k))
        check(len(sets) == comb(m, k), "maximal_antichain_cardinality")
        b = F(1, 2 * k)
        eps = b * b / (8 * m * m)
        check(eps < b * b / (2 * m * m), "strict_robust_margin")
        for s in sets:
            lam = [F(int(i in s), k) for i in range(m)]
            check(sum(lam) == 1, "probability_rows")
            extracted = {i for i in range(m) if lam[i] >= b / (2 * m)}
            check(extracted == s, "thresholded_support_identity")
            for t in sets:
                d = [eps + (1 - 2 * eps) * int(i not in t)
                     for i in range(m)]
                value = sum(lam[i] * d[i] for i in range(m))
                if s == t:
                    check(value == eps, "perturbed_diagonal")
                else:
                    check(value >= b, "perturbed_off_diagonal")
                    witnesses = [i for i in range(m)
                                 if lam[i] * d[i] >= b / m]
                    check(bool(witnesses), "large_summand_exists")
                    check(all(i in s and i not in t for i in witnesses),
                          "ordered_support_witness")
    for j in range(2, 1025):
        m = a_threshold(j)
        check(comb(m, m // 2) >= j, "antichain_threshold_feasible")
        check(m == 1 or comb(m - 1, (m - 1) // 2) < j,
              "antichain_threshold_minimal")
        check(2 ** m >= j and m <= j, "elementary_threshold_bounds")


def arithmetic_diagnostics() -> None:
    # This is the Bloch rotation z=(3+4i)/5, not its half-angle unitary.
    x, y = F(1), F(0)
    orbit = [(x, y)]
    for q in range(1, 257):
        x, y = (3*x - 4*y)/5, (4*x + 3*y)/5
        orbit.append((x, y))
        check(x*x + y*y == 1, "rational_unit_circle")
        check((x * 5**q).denominator == 1,
              "integer_real_power_numerator")
        reject = (1 - x)/2
        check(reject >= F(1, 2 * 5**q), "original_algebraic_margin")
        check(reject >= F(1, 16 * 25**(2*q)),
              "general_algebraic_norm_margin")
    check(orbit[1] == (F(3, 5), F(4, 5)), "bloch_angle_convention")
    for j in (2, 3, 4, 5, 8, 16, 32, 64):
        s = F(1, 2 * 5**(j - 1))
        actual = min((1 - orbit[q][0])/2 for q in range(1, j))
        check(actual >= s, "finite_orbit_separation")
        for n in range(j):
            for m in range(j):
                dot = sum(orbit[n][i]*orbit[m][i] for i in range(2))
                reject = (1 - dot)/2
                if n == m:
                    check(reject == 0, "projector_diagonal_zero")
                else:
                    check(reject >= s, "projector_off_diagonal_margin")
                    check(reject == (1-orbit[abs(n-m)][0])/2,
                          "rotation_difference_identity")
        for budget in (F(1, 100), F(1, 2), F(1), F(8, 7), F(2), F(100)):
            zeta = min(F(1), 7*budget/8)
            pstar = zeta / 8**j
            delta = F(25)*zeta / (128 * 200**j * j*j)
            check(delta == pstar*s*s/(32*j*j),
                  "explicit_certificate_constant")
            for n in range(j):
                pn = zeta/8**(n+1)
                cost = zeta * sum(F(1, 8**i) for i in range(n+1))
                check(cost <= budget, "target_expected_cost")
                check(pn >= pstar and pn > delta,
                      "positive_herald_normalization")
                diag = delta/(pn-delta)
                off = (pn*s-delta)/(pn+delta)
                check(diag <= 2*delta/pstar <= s*s/(16*j*j),
                      "diagonal_joint_event_margin")
                check(off >= s/2, "off_diagonal_joint_event_margin")
                check(s*s/(16*j*j) < (s/2)**2/(2*j*j),
                      "strict_antichain_margin_from_tv")
    # Algebraic-norm corollary's displayed constant.
    for degree in (2, 3, 5):
        for h in (F(2), F(5), F(25)):
            for j in (2, 3, 7):
                zeta = F(3, 7)
                sj = F(1, 4**degree) / h**(2*(j-1))
                bound = zeta*h**4 / (32*16**degree*(8*h**4)**j*j*j)
                check(bound == zeta/F(8**j) * sj*sj/(32*j*j),
                      "general_algebraic_constant")


def main() -> None:
    support_diagnostics()
    arithmetic_diagnostics()
    source = (Path(__file__).resolve().parent / "sections" / "51-unrestricted-approximation.tex")
    report = {
        "status": "PASS",
        "evidence_kind": "finite_exact_rational_diagnostic",
        "not_evidence_of": ["formal_proof", "unrestricted_optimal_rate",
                            "independent_human_review", "editorial_acceptance"],
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "mathematical_source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "checks": COUNTS,
        "checks_by_group": COUNTS,
        "exact_checks": sum(COUNTS.values()),
        "floating_checks": 0,
        "total_checks": sum(COUNTS.values()),
    }
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else None
    payload = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if target:
        target.write_text(payload)
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
