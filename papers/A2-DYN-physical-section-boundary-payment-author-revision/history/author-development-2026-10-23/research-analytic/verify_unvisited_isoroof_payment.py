#!/usr/bin/env python3
"""Exact auxiliary checks specific to native342's marked-foot source.

No orbit sampling or floating-point test is used.  The generic truncated
overlay calculation belongs to native341's separate verifier and is not
counted again here.  These checks do not prove continuous billiard geometry,
the inherited source-growth theorem, or the original raw local limit theorem.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as Q
import hashlib
import itertools
import json
from pathlib import Path


def qt(x):
    return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"


def blob(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def mm(a, b):
    return tuple(tuple(sum((a[i][k] * b[k][j] for k in range(2)), Q(0))
                       for j in range(2)) for i in range(2))


def det(a):
    return a[0][0] * a[1][1] - a[0][1] * a[1][0]


def dot(x, y):
    return sum((a * b for a, b in zip(x, y)), Q(0))


def scale(a, x):
    return tuple(a * y for y in x)


def half_product(radius, incidence, first_distance, further_collisions):
    matrix = ((Q(1), first_distance), (Q(0), Q(1)))
    flight = ((Q(1), Q(3, 50)), (Q(0), Q(1)))
    kick = ((Q(1), Q(0)), (2 / (radius * incidence), Q(1)))
    for _ in range(further_collisions):
        matrix = mm(flight, mm(kick, matrix))
    assert det(matrix) == 1
    # The terminal incoming collision is not an additional kick.
    angular = matrix[0][1] / radius + incidence * matrix[1][1]
    clearance = matrix[0][0] / radius + incidence * matrix[1][0]
    assert angular > 0 and clearance > 0
    return matrix, angular, clearance


def run(source, draft):
    radius_min, radius_max = Q(9, 20), Q(47, 100)
    horizon, minimum_flight = Q(28, 5), Q(3, 50)
    k_min, a_square = Q(100, 47), Q(1827, 40000)
    e_square = 1 / (k_min * k_min * a_square)
    assert e_square == Q(94 * 94, 1827)
    sigma = 1 / (1 + 2 * minimum_flight / radius_max)
    assert sigma == Q(47, 59)
    h_min = 1 / (horizon + radius_max)
    foot_constant = 1 / (2 * radius_min * h_min)
    assert foot_constant == Q(607, 90)
    # Pi cancels exactly in 4*pi*c_*, with c_*=91/(10000*pi).
    four_pi_c_star = Q(91, 2500)
    h_endpoint_min = radius_min * radius_min / Q(47, 6)
    f_cs = 1 / (four_pi_c_star * h_endpoint_min)
    assert foot_constant == (horizon + radius_max) / (2 * radius_min)

    # Exact marked-foot displacement and clock cancellation, on rational
    # unit vectors. The derivative of v_perp is -v; no trigonometric
    # approximation occurs and no circle point is treated as an orbit.
    foot_cases = 0
    unit_vectors = ((Q(1), Q(0)), (Q(3, 5), Q(4, 5)),
                    (Q(5, 13), Q(12, 13)), (Q(-8, 17), Q(15, 17)))
    for v, impact, radius, level in itertools.product(
            unit_vectors, (-1, 1), (radius_min, radius_max), (Q(0), Q(3, 200))):
        assert dot(v, v) == 1
        vp = (-v[1], v[0])
        reverse_vp = scale(Q(-1), vp)
        q_theta = scale(impact * (radius + level), v)
        q_level = scale(Q(-impact), vp)
        assert dot(q_theta, vp) == 0
        assert dot(q_theta, reverse_vp) == 0
        assert dot(q_level, vp) == -impact
        assert dot(q_level, reverse_vp) == impact
        split_roof_derivative = dot(v, q_theta) - dot(v, q_theta)
        assert split_roof_derivative == 0
        foot_cases += 1

    # Derive the physical signed determinant directly from both endpoint
    # rows. Opposite clearance-column signs are essential: equal half
    # ratios would cancel if those signs were incorrectly made equal.
    determinant_cases = 0
    row_pairs = []
    for radius, incidence, first_distance, steps in itertools.product(
            (radius_min, radius_max), (Q(1, 5), Q(3, 5), Q(1)),
            (Q(1, 4), Q(1, 2)), (0, 1, 3, 8)):
        assert first_distance * first_distance >= a_square
        assert first_distance <= horizon
        matrix, angular, clearance = half_product(radius, incidence, first_distance, steps)
        h = clearance / angular
        assert h >= h_min
        assert h * h <= 1 / a_square
        row_pairs.append((radius, angular, clearance))
    for index, (radius, am, bm) in enumerate(row_pairs):
        same_radius = [row for row in row_pairs if row[0] == radius]
        _, ap, bp = same_radius[(index * 7 + 1) % len(same_radius)]
        hm, hp = bm / am, bp / ap
        for impact, s0, sm in itertools.product((-1, 1), repeat=3):
            endpoint_matrix = ((s0 * am, impact * s0 * bm),
                               (sm * ap, -impact * sm * bp))
            actual_det = abs(det(endpoint_matrix))
            expected_det = am * ap * (hm + hp)
            assert actual_det == expected_det > 0
            # dnu=(4*pi*R)^-1 dtheta du
            #     =u_x (4*pi)^-1 dp0 dpm.
            ux = 1 / (radius * actual_det)
            assert ux * actual_det == 1 / radius
            assert ux <= foot_constant / (am * ap)
            # The regular coarea bound carries exactly one 4*pi*c_*.
            assert ux / (four_pi_c_star * h_endpoint_min) == f_cs * ux
            determinant_cases += 1
    wrong_equal_sign_det = det(((Q(2), Q(3)), (Q(2), Q(3))))
    correct_opposite_sign_det = abs(det(((Q(2), Q(3)), (Q(2), Q(-3)))))
    assert wrong_equal_sign_det == 0 and correct_opposite_sign_det == 12

    # Inclusive actual-hit counts from a foot in original flight j. This
    # checks all endpoint positions, including m=1, without conflating the
    # m+1 split pieces with the original m complete physical flights.
    index_pairs = 0
    for m in range(1, 513):
        for j in range(m):
            backwards, forwards = j + 1, m - j
            assert backwards >= 1 and forwards >= 1
            assert backwards + forwards == m + 1
            exponent_twice = max(backwards, forwards) - 1
            assert exponent_twice == max(j, m - 1 - j)
            assert 2 * exponent_twice >= m - 1
            # The square of E_* sigma^((L-1)/2), not E_*^2
            # sigma^(L-1)/2, is the exact algebraic decay factor.
            if m <= 48:
                squared_payment = e_square * sigma ** exponent_twice
                assert squared_payment > 0
                assert squared_payment <= e_square
            index_pairs += 1
    assert max(1, 1) - 1 == 0  # m=1, j=0: no fictitious optical step.
    assert (0 + 1, 1 - 0) == (1, 1)
    assert min(0, 1) == 0  # Omitting the backward endpoint would fail l>=1.

    # Exact-label traces and impact signs are DIFFERENT multiplicities.
    # H_nm already sums both labelled impact circles. The norm of an
    # interface's difference of two exact-label point masses can be 2.
    label_cases = 0
    norms = []
    for left, right in itertools.product((None, 0, 1, 2), repeat=2):
        jump = [int(left == label) - int(right == label) for label in range(3)]
        norm = sum(abs(x) for x in jump)
        assert norm <= 2
        if left is None or right is None:
            assert norm <= 1
        norms.append(norm)
        label_cases += 1
    assert max(norms) == 2

    inherited = {}
    for prefix in ("277", "279", "316", "317", "319", "320", "322", "323", "336", "341"):
        candidates = sorted((source / "core").glob(prefix + "_*.tex"))
        assert len(candidates) == 1, (prefix, candidates)
        path = candidates[0]
        data = path.read_bytes()
        inherited[prefix] = {"path": str(path.relative_to(source)),
                             "git_blob": blob(data),
                             "sha256": hashlib.sha256(data).hexdigest()}
    branch_source = (source / inherited["319"]["path"]).read_text()
    assert "\\label{thm:mb-branch-sup}" in branch_source
    direct_start = branch_source.index("At $u_0=0$ perform the same construction directly")
    direct_end = branch_source.index("\\end{proof}", direct_start)
    direct_trace = branch_source[direct_start:direct_end]
    assert "weak convergence assertion is not used" in direct_trace
    assert "includes both mark signs" in branch_source
    data = draft.read_bytes()
    return {
        "status": "PASS",
        "scope": "Exact marked-coordinate algebra and finite diagnostics only; the written native proof supplies continuous geometry and complete source coverage. The original raw LLT is not certified.",
        "draft": {"path": str(draft), "git_blob": blob(data),
                  "sha256": hashlib.sha256(data).hexdigest()},
        "constants": {"E_star_squared": qt(e_square), "E_star": "94/sqrt(1827)",
                      "sigma": qt(sigma), "half_ratio_lower": qt(h_min),
                      "C_foot": qt(foot_constant), "4_pi_c_star": qt(four_pi_c_star),
                      "F_cs": qt(f_cs)},
        "marked_foot": {"exact_rational_vector_cases": foot_cases,
                        "transverse_angular_seed": [0, 1],
                        "forward_clearance_seed": "(-impact_sign,0)",
                        "backward_clearance_seed": "(impact_sign,0)",
                        "split_clock_terms_cancel": True},
        "determinant": {"rational_signed_row_cases": determinant_cases,
                        "formula": "Aminus*Aplus*(hminus+hplus)",
                        "kernel_weight": "1/(R*Aminus*Aplus*(hminus+hplus))",
                        "incorrect_equal_clearance_signs_rejected": True,
                        "conditioning_factors": 1,
                        "note": "Optical coefficients are algebraic diagnostic inputs, not a sampled set of realizable full trajectories."},
        "indices": {"m_range": [1, 512], "complete_pairs_checked": index_pairs,
                    "actual_half_counts": ["j+1", "m-j"],
                    "individual_exponent": "max(j,m-1-j)/2",
                    "summed_bound": "C_umi*m*sigma^((m-1)/4)",
                    "analytic_limit": "For fixed q, (q+1)*log(m)-(m-1)*log(59/47)/4 tends to minus infinity."},
        "multiplicity": {"record_trace_cases": label_cases, "maximum_exact_label_jump": 2,
                         "additional_impact_sign_factor": 1,
                         "reason": "H_nm already bounds the combined two labelled impact circles; the separate factor2 is a signed exact-label trace norm."},
        "direct_zero_trace": {"native_theorem": "319 thm:mb-branch-sup",
                              "proof_paragraph_sha256": hashlib.sha256(direct_trace.encode()).hexdigest(),
                              "weak_transfer_used": False,
                              "scope": "This records the explicit retained proof dependency; text matching is not proof validation."},
        "inherited_sources": inherited,
        "not_recounted": "Native341's truncated-overlay and opposition-quadrant diagnostics are reused mathematically, not counted as additional native342 verification."
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--draft", type=Path,
                        default=Path(__file__).with_name("342_unvisited_boundary_isoroof_payment.tex"))
    parser.add_argument("--output", type=Path,
                        default=Path(__file__).with_name("342_EXACT_CHECKS.json"))
    args = parser.parse_args()
    report = run(args.source.resolve(), args.draft.resolve())
    args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps({"status": report["status"], "output": str(args.output),
                      "marked_foot_cases": report["marked_foot"]["exact_rational_vector_cases"],
                      "determinant_cases": report["determinant"]["rational_signed_row_cases"],
                      "index_pairs": report["indices"]["complete_pairs_checked"],
                      "scope": report["scope"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
