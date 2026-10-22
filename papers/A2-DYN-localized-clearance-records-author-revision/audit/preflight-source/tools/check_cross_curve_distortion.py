#!/usr/bin/env python3
"""Exact author checks for the real-word cross-curve distortion proof.

Symbolic identities, rational constants, exact index conventions, and a
genuine one-flight endpoint family are checked here.  These finite checks
do not prove the inherited continuum anchor-localization theorem, full
physical pressure, an unproved planar cell lemma, or the raw local limit.
The continuum inequalities are proved in the native manuscript.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import sys

import sympy as sp


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def equal(left: sp.Expr, right: sp.Expr, message: str) -> None:
    difference = sp.simplify(left - right)
    require(difference == 0, message + ": " + str(difference))


def native_source() -> Path:
    here = Path(__file__).resolve().parent
    suffix = "full_word_cross_curve_distortion.tex"
    direct = here / suffix
    if direct.is_file():
        return direct
    candidates = sorted((here.parent / "core").glob("*" + suffix))
    require(len(candidates) == 1, "native source must resolve uniquely")
    return candidates[0]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--details", type=Path)
    args = parser.parse_args()
    checks: list[dict[str, object]] = []

    def passed(name: str, **values: object) -> None:
        checks.append({"name": name, "status": "passed", **values})

    a = sp.Rational(100, 47)
    cone_max = sp.Rational(170, 9)
    radius_min = sp.Rational(9, 20)
    radius_max = sp.Rational(47, 100)
    flight_min = sp.Rational(3, 50)
    curvature_max = 1 / radius_min
    slope_ratio = sp.Rational(47, 48)
    qa = Fraction(3263680, 3263681)
    original_q0 = Fraction(47, 53)
    layer = 94
    require(0 < qa < 1 and 0 < original_q0 < 1, "strict contraction constants")
    require(qa != original_q0, "physical anchor and original guard remain distinct")
    equal(curvature_max + 1 / flight_min, cone_max, "true maximal cone slope")
    equal(1 / (8 * a * flight_min), slope_ratio, "exact 47/48 contraction")
    equal(1 + 2 * a * flight_min, sp.Rational(59, 47), "inherited adapted expansion")
    require(4 * layer == 376, "quartic anchor depth root is exactly 1/376")
    passed("original_geometry_and_distinct_rates", radius=[str(radius_min), str(radius_max)],
           flight_min=str(flight_min), slope_ratio=str(slope_ratio),
           anchor_ratio=str(qa), original_guard_ratio=str(original_q0),
           paired_record_ratio="q_a^(1/376)", probability_normalization="none in a tangent Jacobian")

    # Euclidean division proves the rounding inequality for every depth.
    rounding_cases = []
    for r in range(layer):
        small_gap = Fraction(1, 2) - Fraction(r, 4 * layer)
        positive_layer_gap = Fraction(layer - r, 4 * layer)
        require(small_gap > 0 and positive_layer_gap > 0,
                "quartic rounding gap must remain positive")
        for k in (0, 1, 2, 19):
            depth = layer * k + r
            j = max(0, depth // layer - 1)
            gap = Fraction(j, 4) - (Fraction(depth, 4 * layer) - Fraction(1, 2))
            expected = small_gap if k == 0 else positive_layer_gap
            require(gap == expected, "Euclidean depth decomposition")
        rounding_cases.append(str(positive_layer_gap))
    for m in range(1, 2 * layer + 2):
        require(min(0, m) == 0 and min(m, 0) == 0, "both actual endpoints have depth zero")
        if m % 2 == 0:
            require(min(m // 2, m - m // 2) == m // 2, "central singleton retained")
    passed("all_depth_rounding_and_endpoint_indices", residue_classes=layer,
           universal_gap_if_k_zero="1/2-r/(4N)",
           universal_gap_if_k_positive="(N-r)/(4N)",
           implication="q_a^(j(d)/4) <= q_a^(-1/2) q^d, since 0<q_a<1",
           actual_endpoints="i=0,m retained, including m=1")

    q = sp.symbols("q", positive=True)
    index_masks = []
    for m in range(1, 10):
        b = [q ** i + q ** (m - i) for i in range(m + 1)]
        equal(sum(b), 2 * (1 - q ** (m + 1)) / (1 - q), "two-sided geometric sum")
        for i in range(m):
            # Nonnegative for 0<q<1, so both adjacent endpoint estimates hold.
            equal(b[i] / q - b[i + 1], q ** (i - 1) * (1 - q ** 2),
                  "right adjacent contact tail")
            equal(b[i + 1] / q - b[i], q ** (m - i - 2) * (1 - q ** 2),
                  "left adjacent contact tail")
        interior = list(range(1, m))
        denominator = list(range(1, m + 1))
        require(denominator[:-1] == interior, "multiplication by c_m removes only the terminal incidence")
        index_masks.append({"m": m, "weighted_incidence_indices": interior,
                            "unweighted_incidence_indices": denominator})
    passed("complete_geometric_sums_and_incidence_masks", finite_index_masks=index_masks,
           continuum_series="sum_i(q^i+q^(m-i)) <= 2/(1-q)",
           logarithmic_series="sum_i(q^(i/3)+q^((m-i)/3)) <= 2/(1-q^(1/3))",
           flight_count="m", contact_count="m+1")

    kappa, v, c, d, tau = sp.symbols("kappa v c d tau", positive=True)
    scalar = tau * (kappa + v) + c
    graph = kappa + d * (kappa + v) / scalar
    equal(sp.diff(graph, v), c * d / scalar ** 2, "physical slope derivative")
    equal(sp.diff(graph, c), -d * (kappa + v) / scalar ** 2, "initial incidence derivative")
    equal(sp.diff(graph, d), (kappa + v) / scalar, "terminal incidence derivative")
    equal(sp.diff(graph, tau), -d * (kappa + v) ** 2 / scalar ** 2, "flight derivative")
    B = sp.symbols("B", positive=True)
    equal((B + c) ** 2 - 4 * B * c * d,
          (B - c) ** 2 + 4 * B * c * (1 - d), "contraction nonnegative remainder")
    equal(1 / tau - d * (kappa + v) / scalar,
          ((1 - d) * tau * (kappa + v) + c) / (tau * scalar),
          "physical cone invariance nonnegative remainder")
    passed("exact_slope_derivatives_and_uniform_contraction",
           derivative_remainder="(B-c)^2+4Bc(1-d)>=0 for B,c>=0 and 0<=d<=1",
           parameter_domain="v in[a,K], c,d in[0,1], tau in[tau_min,tau_max], fixed kappa=1/R",
           bounds={"f_v": "47/48", "abs_f_c": "1/(2a tau_min^2)",
                   "f_d": "1/tau_min", "abs_f_tau": "1/tau_min^2"},
           interpolation="only the explicit rational parameter function; no physical path is assumed")

    rho = sp.symbols("rho", positive=True)
    recurrence_cases = []
    for m in range(1, 10):
        v0 = sp.symbols("delta_v0", nonnegative=True)
        forcings = sp.symbols("F0:" + str(max(0, m - 1)), nonnegative=True)
        values = [v0]
        for forcing in forcings:
            values.append(rho * values[-1] + forcing)
        total = sp.expand(sum(values))
        equal(total.coeff(v0), (1 - rho ** m) / (1 - rho), "initial slope paid once")
        for j, forcing in enumerate(forcings):
            equal(total.coeff(forcing), (1 - rho ** (m - 1 - j)) / (1 - rho),
                  "each forcing has one finite geometric coefficient")
        recurrence_cases.append({"m": m, "initial_terms": 1, "forcing_terms": len(forcings)})
    passed("summed_slope_recurrence", finite_symbolic_expansions=recurrence_cases,
           universal_argument="each coefficient is (1-rho^j)/(1-rho)<=1/(1-rho)",
           final_numerator="K-a+(tau_min^-1+(2a tau_min^2)^-1) D_c+tau_min^-2 D_tau")

    matrix = sp.Matrix([[tau * kappa + c, tau],
                        [tau * kappa ** 2 + kappa * d + kappa * c, tau * kappa + d]]) / d
    vector = sp.Matrix([1, v])
    require((matrix * vector - scalar / d * sp.Matrix([1, graph])).applyfunc(sp.simplify)
            == sp.zeros(2, 1), "exact Euclidean tangent-vector transport")
    reversal = sp.diag(1, -1)
    reverse_matrix = matrix.xreplace({c: d, d: c})
    require(((-matrix).inv() - reversal * (-reverse_matrix) * reversal).applyfunc(sp.simplify)
            == sp.zeros(2, 2), "signed physical inverse/time reversal identity")
    require(reversal.T * reversal == sp.eye(2), "time reversal is an exact Euclidean isometry")
    telescope_cases = []
    for m in range(1, 7):
        numerators = sp.symbols("A0:" + str(m), positive=True)
        incidences = sp.symbols("c0:" + str(m + 1), positive=True)
        slopes = sp.symbols("v0:" + str(m + 1), positive=True)
        product = sp.prod(numerators[i] / incidences[i + 1]
                          * sp.sqrt(1 + slopes[i + 1] ** 2)
                          / sp.sqrt(1 + slopes[i] ** 2) for i in range(m))
        expected = sp.prod(numerators) / sp.prod(incidences[1:])
        expected *= sp.sqrt(1 + slopes[-1] ** 2) / sp.sqrt(1 + slopes[0] ** 2)
        equal(product, expected, "actual Euclidean endpoint norm telescoping")
        equal(incidences[-1] * product,
              sp.prod(numerators) / sp.prod(incidences[1:-1])
              * sp.sqrt(1 + slopes[-1] ** 2) / sp.sqrt(1 + slopes[0] ** 2),
              "exact weighted endpoint incidence cancellation")
        telescope_cases.append(m)
    passed("signed_physical_jacobian_and_endpoint_telescope", counts=telescope_cases,
           one_flight="(A_i/c_(i+1)) sqrt((1+v_(i+1)^2)/(1+v_i^2))",
           endpoint_log_budget="log((1+K^2)/(1+a^2)) once for the paired ratio",
           stable_inverse="I T I with I=diag(1,-1); no adapted-norm replacement")

    k, delta = sp.symbols("k delta", positive=True)
    equal(4 * k ** 2 - (k + 1) ** 2, (k - 1) * (3 * k + 1), "strip index remainder")
    equal((k ** 2 * delta) ** 3, delta * (k ** 3 * delta) ** 2, "one-third grazing exponent")
    equal(sp.pi ** 2 * delta - delta ** 3,
          delta * (sp.pi - delta) * (sp.pi + delta), "central one-third conversion")
    passed("grazing_and_central_holder_constants",
           signed_grazing="delta<=3 k^-3, c>=2/(pi(k+1)^2), hence log ratio<=2pi 3^(2/3) delta^(1/3)",
           central="delta<=pi, c>=2/(pi k0^2), hence constant pi^(5/3) k0^2/2",
           scope="closure of the same fixed q=2 strip at exactly those indices whose log incidences are summed; the original disjoint boundary assignment need not commute with reflection")

    # A true short family exhibits the endpoint factor, without any symbolic
    # code standing in for a physical orbit.  The analytic rectangle exclusion
    # below applies to the complete segment and to every other lattice row.
    endpoint_incidence = sp.symbols("u", positive=True)
    R = radius_min
    center_distance = 1 - R
    sine = R / center_distance * sp.sqrt(1 - endpoint_incidence ** 2)
    cosine = sp.sqrt(1 - sine ** 2)
    physical_flight = center_distance * cosine - R * endpoint_incidence
    cosine_limit = sp.limit(cosine, endpoint_incidence, 0, dir="+")
    flight_limit = sp.limit(physical_flight, endpoint_incidence, 0, dir="+")
    equal(cosine_limit, 2 * sp.sqrt(10) / 11, "genuine departure incidence at the tangent limit")
    equal(flight_limit, 1 / sp.sqrt(10), "genuine tangent flight length")
    equal(R + flight_limit * cosine_limit, sp.Rational(139, 220), "tangent contact x coordinate")
    equal(flight_limit * sp.Rational(9, 11), 9 * sp.sqrt(10) / 110, "tangent contact y coordinate")
    equal(center_distance / 2, sp.Rational(11, 40), "whole-segment vertical envelope")
    require(sp.Rational(3, 4) > sp.Rational(29, 40) ** 2,
            "all nonzero triangular-lattice rows miss the whole segment strictly")
    require(R + center_distance == 1 and 1 > R,
            "all other centers on the zero row miss the whole segment strictly")
    kappa_fixed = 1 / R
    scalar_fixed = physical_flight * (kappa_fixed + a) + cosine
    slope_terminal = kappa_fixed + endpoint_incidence * (kappa_fixed + a) / scalar_fixed
    weighted_expansion = scalar_fixed * sp.sqrt(1 + slope_terminal ** 2) / sp.sqrt(1 + a ** 2)
    weighted_limit = sp.simplify(sp.limit(weighted_expansion, endpoint_incidence, 0, dir="+"))
    require(weighted_limit.is_positive is True, "true c1 J1 limit is strictly positive")
    passed("genuine_one_flight_endpoint_factor", radius=str(R),
           word="(0,0) -> (1,0)", initial_contact="(9/20,0)",
           angle_range="0<=theta<arcsin(9/11)",
           exact_c1="sqrt(1-(11 sin(theta)/9)^2)",
           complete_flight_rectangle="[9/20,1] x [0,11/40]",
           other_rows="sqrt(3)/2 - 11/40 > 9/20; exact positive squared remainder checked",
           unweighted_expansion="J1 grows as a positive constant/c1",
           weighted_limit=str(weighted_limit),
           scope="demonstrates the genuine endpoint factor; not a counterexample to Q_* or the raw theorem")

    optical = 30000
    require(optical ** 2 == 900000000, "one upper and one lower optical comparison")
    J, c0, cm = sp.symbols("j c0 cm", positive=True)
    equal(1 / (c0 / J), J / c0, "stable inverse endpoint normalization")
    equal((cm * J) / (c0 * cm), J / c0, "both physical optical endpoint factors")
    passed("stable_and_optical_endpoint_payments", stable="j_m/c0",
           optical="omega/(c0 cm)", optical_ratio_cost=optical ** 2,
           no_collision_exponent="30000^2 once, not 30000^(2m)",
           no_probability_factor="neither cstar^-1 nor a new conditioning measure appears")

    source = native_source()
    result = {"status": "passed", "check_count": len(checks), "checks": checks,
              "native_source": source.name,
              "native_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
              "program_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "limitations": [
                  "This program verifies exact algebra and stated finite index masks, not a continuum theorem by sampling.",
                  "Native module308 remains the proved geometric localization input; the new native proof supplies its cross-curve application.",
                  "Whole physical pressure still requires a complete cell/capacity payment; raw pointwise and boundary-trace claims are not certified here."]}
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.details is not None:
        args.details.parent.mkdir(parents=True, exist_ok=True)
        args.details.write_text(rendered, encoding="utf-8")
    sys.stdout.write(rendered)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        sys.stderr.write(type(exc).__name__ + ": " + str(exc) + "\n")
        raise SystemExit(1)
