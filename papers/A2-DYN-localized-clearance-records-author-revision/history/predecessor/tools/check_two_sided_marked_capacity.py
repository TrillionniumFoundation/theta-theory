#!/usr/bin/env python3
"""Exact auxiliary checks for native module 319.

The interval families and positive matrices below test the displayed algebra.
They are not substituted for physical trajectories.  The native proofs supply
the actual first-hit geometry, source partitions and continuous suprema.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as F
from functools import lru_cache
import itertools
import json
from pathlib import Path
import sympy as sp


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def matrix_mul(a, b):
    return ((a[0][0]*b[0][0]+a[0][1]*b[1][0],
             a[0][0]*b[0][1]+a[0][1]*b[1][1]),
            (a[1][0]*b[0][0]+a[1][1]*b[1][0],
             a[1][0]*b[0][1]+a[1][1]*b[1][1]))


@lru_cache(None)
def interval_families(n, start=0):
    """Every family of disjoint open integer-endpoint intervals in (0,n).

    Gaps, adjacent intervals, and the empty family are included.
    """
    if start >= n:
        return ((),)
    result = list(interval_families(n, start+1))
    for end in range(start+1, n+1):
        for tail in interval_families(n, end):
            result.append(((start, end),)+tail)
    return tuple(result)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--details", type=Path)
    args = parser.parse_args()
    groups = []
    sigma = F(47, 59)
    require(1+2*F(3, 50)/F(47, 100) == 1/sigma,
            "Optical expansion factor or physical radius conversion changed")
    require((F(28, 5)+F(47, 100))/(2*F(9, 20)) == F(607, 90),
            "Foot factor must be exactly 607/90")
    require(sp.simplify(1/(sp.Rational(100, 47)*sp.sqrt(1827)/200)
                        - 94/sp.sqrt(1827)) == 0, "Initial inverse factor")
    require((4*F(1, 100)**2+(2*F(3, 50))*(2*F(3, 20)))/4
            == F(91, 10000), "Original section area divided by 4")
    groups.append({"group": "exact_original_constants_and_section_factor",
                   "status": "passed"})

    am, ap, hm, hp = sp.symbols("am ap hm hp", positive=True)
    signs_checked = 0
    for s0, sm, side in itertools.product([-1, 1], repeat=3):
        jac = sp.Matrix([[s0*am, side*s0*am*hm],
                         [sm*ap, -side*sm*ap*hp]])
        require(sp.expand(jac.det()**2-am**2*ap**2*(hm+hp)**2) == 0,
                "Half-ray determinant sign or positive sum")
        signs_checked += 1
    groups.append({"group": "all_half_ray_orientation_signs",
                   "cases": signs_checked, "status": "passed"})

    optical_cases = 0
    # These are exact tests of a proved positive-product inequality.  The
    # parameters range over its bounds; no claim of physical realization is made.
    for radius in [F(9, 20), F(23, 50), F(47, 100)]:
        for foot in [F(21, 100), F(1, 2), F(28, 5)]:
            prod = ((F(1), foot), (F(0), F(1)))
            for ell_index in range(8):
                for terminal_c in [F(1), F(1, 2), F(1, 10000)]:
                    aa = prod[0][1]/radius + terminal_c*prod[1][1]
                    bb = prod[0][0]/radius + terminal_c*prod[1][0]
                    require(aa >= foot/F(47, 100)*sigma**(-ell_index),
                            "Positive optical expansion lower bound")
                    h = bb/aa
                    require(F(1)/(F(28, 5)+F(47, 100)) <= h <= 1/foot,
                            "Incoming endpoint ratio bounds")
                    require(prod[0][0]*prod[1][1]-prod[0][1]*prod[1][0] == 1,
                            "Unfolded physical matrix determinant")
                    optical_cases += 1
                ell = [F(3, 50), F(1, 3), F(28, 5)][ell_index % 3]
                interior_c = [F(1), F(1, 7), F(1, 10000)][ell_index % 3]
                kick = 2/(radius*interior_c)
                prod = matrix_mul(((1+ell*kick, ell), (kick, F(1))), prod)
    groups.append({"group": "positive_optical_products",
                   "cases": optical_cases, "status": "passed",
                   "scope": "rational algebra, not sampled billiard existence"})

    families = interval_families(5)
    pair_cases = overlap_cases = 0
    for fam_i in families:
        for fam_j in families:
            wa = [F(1+i[0]+2*i[1], 3+i[1]-i[0]) for i in fam_i]
            wb = [F(2+2*j[0]+j[1], 5+j[1]-j[0]) for j in fam_j]
            seen_i, seen_j = set(), set()
            lhs = F(0)
            for ni, i in enumerate(fam_i):
                for nj, j in enumerate(fam_j):
                    if max(i[0], j[0]) >= min(i[1], j[1]):
                        continue
                    lhs += wa[ni]*wb[nj]
                    overlap_cases += 1
                    if i[0] >= j[0]:
                        require(ni not in seen_i, "A left endpoint charged twice")
                        seen_i.add(ni)
                    else:
                        require(nj not in seen_j, "B left endpoint charged twice")
                        seen_j.add(nj)
            rhs = max(wb, default=F(0))*sum(wa, F(0))
            rhs += max(wa, default=F(0))*sum(wb, F(0))
            require(lhs <= rhs, "Weighted overlay inequality")
            pair_cases += 1
    groups.append({"group": "exhaustive_interval_overlay_with_gaps_and_seams",
                   "families": len(families), "family_pairs": pair_cases,
                   "nonempty_intersections": overlap_cases, "status": "passed"})

    # Row/column set partitions have nine intersections, so the interval
    # hypothesis is mathematically indispensable.
    n = 3
    row_column_lhs = n*n*F(1, n)**2
    interval_rhs = 2*F(1, n)
    require(row_column_lhs > interval_rhs, "Noninterval counterexample missing")
    groups.append({"group": "noninterval_partition_counterexample",
                   "lhs": str(row_column_lhs), "purported_rhs": str(interval_rhs),
                   "status": "passed"})

    depth_cases = 0
    for m in range(1, 101):
        for d in range((m+1)//2+2):
            indices = [j for j in range(m) if min(j, m-1-j) >= d]
            value = sum((sigma**j+sigma**(m-j-1) for j in indices), F(0))
            require(value <= 2*sigma**d/(1-sigma), "Complete depth sum")
            for j in indices:
                require((j+1)+(m-j) == m+1, "Foot half-counts")
                require((j+1)-1 == j and (m-j)-1 == m-j-1,
                        "Optical kick-count indexing")
            depth_cases += 1
    groups.append({"group": "all_finite_depth_and_half_count_edge_cases",
                   "cases": depth_cases, "status": "passed"})
    result = {"status": "passed", "native_module": 319,
              "continuum_proof_certificate": False,
              "groups": groups}
    payload = json.dumps(result, indent=2, sort_keys=True)+"\n"
    if args.details:
        args.details.parent.mkdir(parents=True, exist_ok=True)
        args.details.write_text(payload)
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
