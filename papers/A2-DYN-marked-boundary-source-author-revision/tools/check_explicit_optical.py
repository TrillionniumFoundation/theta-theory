#!/usr/bin/env python3
"""Exact algebra supporting module 313; not a continuum-proof certificate."""
from __future__ import annotations

import argparse
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import sympy as sp


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def matmul(A, B):
    return tuple(tuple(sum(A[i][k] * B[k][j] for k in range(2))
                       for j in range(2)) for i in range(2))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", type=Path)
    ap.add_argument("--details", type=Path)
    args = ap.parse_args()
    a, K, H = F(100, 47), F(170, 9), F(19)
    rminus, rplus, tminus = F(9, 20), F(47, 100), F(3, 50)
    e = 2 * a / H**2
    lower_inverse = H**3 / (4 * rminus * a**2)
    upper_ratio = rplus * K * H**3 / a
    one_step = H**3 / (4 * tminus * a**2)
    q = 1 / (8 * tminus * a)
    require(a > 0 and K > a, "nonempty positive cone")
    require(K == 1 / rminus + 1 / tminus, "maximum physical cone slope")
    require(1 + K**2 < H**2, "Euclidean norm enclosure")
    require(q == F(47, 48) and 0 < q < 1, "uniform slope contraction")
    require(1 + 2 * tminus * a == F(59, 47), "true stable rate")
    require(lower_inverse < 30000, "lower optical comparison")
    require(upper_ratio < 30000, "upper optical comparison")
    require(one_step < 6400, "one-step inverse-incidence payment")

    tau, kap, kapp, c, cp, v = sp.symbols(
        "tau kap kapp c cp v", positive=True)
    N = sp.Matrix([[tau * kap + c, tau],
                   [tau * kap * kapp + kap * cp + kapp * c,
                    tau * kapp + cp]])
    M = N / cp
    B = sp.Matrix([[c, 0], [kap, 1]])
    Bp = sp.Matrix([[cp, 0], [kapp, 1]])
    Cp = sp.Matrix([[1, 0], [2 * kapp / cp, 1]])
    S = sp.Matrix([[1, tau], [0, 1]])
    f = (N[1, 0] + N[1, 1] * v) / (N[0, 0] + N[0, 1] * v)
    tests = {
        "determinant_before_incidence_division": N.det() - c * cp,
        "determinant_after_incidence_division": M.det() - c / cp,
        "slope_identity":
            f - (kapp + cp * (kap + v) / (tau * (kap + v) + c)),
        "slope_derivative":
            sp.diff(f, v) - c * cp / (tau * (kap + v) + c)**2,
        "first_column_ratio":
            N[0, 0] / N[0, 1] - (kap + c / tau),
        "second_column_ratio":
            N[1, 0] / N[1, 1] - (kap + kapp * c / (tau * kapp + cp)),
        "positive_slope_upper_gap":
            kapp + 1 / tau - f
            - (tau * (kap + v) * (1-cp) + c)
            / (tau * (tau * (kap + v) + c)),
    }
    b = sp.symbols("b", positive=True)
    tests["contraction_square_identity"] = (b + c)**2 - 4*b*c - (b-c)**2
    for name, expression in tests.items():
        require(sp.simplify(expression) == 0, name)
    conjugacy = Bp * M * B.inv() - Cp * S
    require(all(sp.simplify(x) == 0 for x in conjugacy), "optical conjugacy")
    tests["optical_conjugacy"] = sp.Integer(0)

    eye = ((F(1), F(0)), (F(0), F(1)))
    cases = []
    for R in (rminus, F(23, 50), rplus):
        curvature = 1 / R
        for count in (1, 2, 3, 7):
            incidences = [F(1), F(1, 10**20), F(7, 9), F(1, 10**6),
                          F(2, 3), F(9, 10), F(1, 71), F(1)]
            incidences = incidences[:count+1]
            lengths = [tminus, F(1), F(28, 5), F(3, 7),
                       F(11, 13), F(5, 2), F(6, 5)][:count]
            product = eye
            optical = eye
            for i, length in enumerate(lengths):
                ci, cj = incidences[i], incidences[i+1]
                matrix = (
                    ((length*curvature+ci)/cj, length/cj),
                    ((length*curvature**2+curvature*cj+curvature*ci)/cj,
                     (length*curvature+cj)/cj))
                product = matmul(matrix, product)
                shear = ((F(1), length), (F(0), F(1)))
                if i:
                    collision = ((F(1), F(0)), (2*curvature/ci, F(1)))
                    optical = matmul(collision, optical)
                optical = matmul(shear, optical)
            determinant = product[0][0]*product[1][1] - product[0][1]*product[1][0]
            require(determinant == incidences[0] / incidences[-1],
                    "all-step determinant telescope")
            bm = product[0][1]
            require(bm > 0, "nonzero physical endpoint derivative")
            require(bm * incidences[-1] == optical[0][1],
                    "all-step original optical denominator")
            for row in range(2):
                require(a * product[row][1] <= product[row][0]
                        <= K * product[row][1], "nonaccumulating column bounds")
            require(a <= product[1][1]/bm <= K, "terminal vertical-column cone")
            cases.append({"radius": str(R), "flights": count,
                          "determinant_telescopes": True,
                          "original_optical_denominator_matches": True,
                          "nonaccumulating_column_bounds": True})

    source = Path(__file__).with_name("313_explicit_physical_optical_comparison.tex")
    # In the packaged article this script may be in tools/ and the source in core/.
    if not source.exists():
        source = Path(__file__).resolve().parent.parent / "core" / source.name
    require(source.is_file(), "native module 313 is present")
    result = {
        "status": "passed",
        "scope": "Exact identities and conservative rational enclosures supporting the native proof",
        "continuum_proof_certificate": False,
        "physical_orbit_sampling_claimed": False,
        "native_source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "constants": {
            "a": str(a), "K": str(K), "H": str(H), "angle_lower": str(e),
            "slope_contraction": str(q), "stable_rate": "59/47",
            "C0": 30000, "C1": 6400,
            "lower_optical_inverse_upper_bound": str(lower_inverse),
            "upper_optical_ratio_bound": str(upper_ratio),
            "one_step_ratio_bound": str(one_step),
        },
        "symbolic_identities_verified": sorted(tests),
        "rational_matrix_stress_cases": cases,
        "case_scope": "Admissible coefficient algebra, including extreme incidences; these are not claimed to be realized physical records",
        "empty_block": {"stable_cocycle": 1, "optical_inverse_derivative_defined": False},
        "remaining_whole_cylinder_pressure_premise": True,
    }
    data = json.dumps(result, indent=2, sort_keys=True) + "\n"
    for destination in (args.output, args.details):
        if destination:
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text(data)
    print(data, end="")


if __name__ == "__main__":
    main()
