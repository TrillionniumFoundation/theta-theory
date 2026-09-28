#!/usr/bin/env python3
"""Independent finite controls for the A2 v49 referee report.

Requires SymPy. Run with Python and Python -O; no check relies on assert.
These exact algebraic controls do not certify the infinite-flight estimates,
analytic continuation, statistical theorems, or a general reconstruction algorithm.
The geometric clearance and completeness arguments are in REFEREE_REPORT.md.
"""
from __future__ import annotations
import json
import sympy as s


def require(condition: object, message: str) -> None:
    if not bool(condition):
        raise RuntimeError(message)


def zero(value: s.Expr) -> bool:
    return s.simplify(value) == 0


def matrix_zero(value: s.Matrix) -> bool:
    return all(zero(x) for x in value)


def main() -> None:
    out: dict[str, object] = {
        "scope": "Exact finite algebraic controls; not a certification of the manuscript.",
        "sympy_version": s.__version__,
    }
    # A noncircular exact fiber with two distinct positively oriented marked lattices.
    a = s.sqrt(2) / 2
    R, eps = s.Rational(1, 10), s.Rational(1, 1000)
    theta = s.symbols("theta", real=True)
    h = R + eps * s.cos(4 * theta)
    require(zero(h + s.diff(h, theta, 2) - (R - 15 * eps * s.cos(4 * theta))), "curvature")
    require(R - 15 * eps == s.Rational(17, 200), "positive curvature margin")
    require(zero(h.subs(theta, theta + s.pi / 2) - h), "C4 invariance")
    quarter = s.Matrix([[0, -1], [1, 0]])
    first, second = s.Matrix([1, 0]), s.Matrix([a, a])
    candidates = [s.Matrix.hstack(first, quarter ** q * second) for q in range(4)]
    dets = [s.simplify(L.det()) for L in candidates]
    admissible = [q for q, d in enumerate(dets) if d > 0]
    require(admissible == [0, 1], "orientation filter must retain exactly two assignments")
    plus, minus = candidates[0], candidates[1]
    require(matrix_zero(minus[:, 1] - quarter * plus[:, 1]), "proper congruence of second channel")
    gram_difference = s.simplify(plus.T * plus - minus.T * minus)
    require(not matrix_zero(gram_difference), "marked Gram matrices must differ")
    # Sufficient separation and clearance inequalities, not a sampled lattice check.
    require(s.simplify(1 - a - (2 * (R + eps)) ** 2) > 0, "periodic separation margin")
    require(a - R - eps > s.Rational(3, 5), "third-obstacle clearance margin")
    gaps = [1 - 2 * (R + eps), 1 - 2 * (R - eps)]
    require(gaps == [s.Rational(399, 500), s.Rational(401, 500)], "channel gaps")
    out["noncircular_two_branch_fiber"] = {
        "support": "1/10 + cos(4 theta)/1000",
        "curvature_radius_lower_bound": "17/200",
        "rotation_assignment_determinants": [str(x) for x in dets],
        "positive_determinant_assignments": admissible,
        "gaps": [str(x) for x in gaps],
        "gram_difference": [[str(x) for x in row] for row in gram_difference.tolist()],
        "negative_control_omitting_orientation_filter": "four assignments instead of two",
        "status": "pass",
    }

    # Moving-reference determinant derivative: a noncommuting 3-by-3 control.
    H = s.Matrix([[3, -s.Rational(1, 3), 0], [-s.Rational(1, 3), 4, -s.Rational(1, 5)], [0, -s.Rational(1, 5), 5]])
    dH = s.diag(1, 2, -1)
    D = s.Matrix([[2, 1, 0], [1, 3, -1], [0, -1, 2]]) / 100
    dD = s.Matrix([[1, -2, 0], [-2, 1, 1], [0, 1, -1]]) / 200
    for matrix in (H, H + D):
        require(all(matrix[:k, :k].det() > 0 for k in (1, 2, 3)), "positive Hessian")
    G = H.inv()
    T = G * D
    dG = -G * dH * G
    dT = dG * D + G * dD
    Udot = s.Rational(1, 11)
    via_relative = Udot - s.trace((s.eye(3) + T).inv() * dT)
    via_determinants = Udot + s.trace(G * dH) - s.trace((H + D).inv() * (dH + dD))
    frozen_G_wrong = Udot - s.trace((s.eye(3) + T).inv() * G * dD)
    require(zero(via_relative - via_determinants), "moving-reference determinant identity")
    omitted_residual = s.simplify(frozen_G_wrong - via_determinants)
    require(omitted_residual != 0, "negative control must detect missing dG")
    require(not matrix_zero(G * D - D * G), "test must not reduce to commuting matrices")
    out["moving_reference"] = {"status": "pass", "derivative": str(s.simplify(via_relative)), "omitting_dG_residual": str(omitted_residual)}

    # A base symmetry need not survive; the actually followed branch does.
    t, alpha, velocity = s.symbols("t alpha velocity", real=True)
    breaking = R + s.Rational(1, 1000) * s.cos(2 * theta) + t * s.Rational(1, 2000) * s.cos(3 * theta)
    difference = s.expand_trig(breaking.subs(theta, theta + s.pi) - breaking)
    require(zero(difference.subs(t, 0)), "base half-turn symmetry")
    require(not zero(s.diff(difference, t)), "half-turn must break to first order")
    ratio = s.exp(-s.I * 4 * (alpha + velocity * t))
    require(zero(s.I / 4 * s.diff(ratio, t) / ratio - velocity), "local angular velocity sign")
    out["local_branch_and_symmetry_breaking"] = {"status": "pass", "broken_half_turn_derivative": str(s.trigsimp(s.diff(difference, t)))}

    # Four-density cancellation and the positive scalar-anchor derivative term.
    u, v = s.symbols("u v", real=True)
    def action(x: s.Expr) -> s.Expr:
        x = s.sympify(x)
        return x ** 2 / 2 + t * (x ** 2 / 3 + x ** 3 / 5)
    def amplitude(x: s.Expr) -> s.Expr:
        x = s.sympify(x)
        return 1 + x / 10 + t * x / 20
    def density(x: s.Expr, y: s.Expr) -> s.Expr:
        return amplitude(x) * amplitude(y) * (1 - action(x) - action(y)) / (2 + t / 7)
    ratio4 = s.cancel(density(u, v) * density(0, 0) / (density(u, 0) * density(0, v)))
    tau_u = action(u) / (1 - action(u))
    tau_v = action(v) / (1 - action(v))
    require(zero(ratio4 - (1 - tau_u * tau_v)), "four-density cancellation")
    anchor = s.Rational(1, 5)
    q0 = tau_u.subs({u: anchor, t: 0})
    tau0 = tau_u.subs(t, 0)
    dr_ua = s.diff(ratio4.subs(v, anchor), t).subs(t, 0)
    dr_aa = dr_ua.subs(u, anchor)
    predicted = -dr_ua / q0 + tau0 * dr_aa / (2 * q0 ** 2)
    direct = s.diff(tau_u, t).subs(t, 0)
    require(zero(predicted - direct), "anchor derivative")
    wrong = -dr_ua / q0 - tau0 * dr_aa / (2 * q0 ** 2)
    wrong_residual = s.simplify((wrong - direct).subs(u, s.Rational(1, 10)))
    require(wrong_residual != 0, "anchor sign negative control")
    out["four_density_anchor"] = {"status": "pass", "anchor_q": str(q0), "wrong_sign_residual_at_one_tenth": str(wrong_residual)}

    # Two cycle gains generate a nonunimodular matrix; its actual inverse is needed.
    L = s.Matrix([[3, s.Rational(1, 4)], [0, 2]])
    centers = {1: s.zeros(2, 1), 2: s.Matrix([s.Rational(1, 7), s.Rational(2, 9)]), 3: s.Matrix([-s.Rational(1, 8), s.Rational(1, 6)])}
    edges = [(1, 2, s.Matrix([1, 0])), (2, 3, s.Matrix([0, 1])), (3, 1, s.Matrix([1, -1])), (2, 3, s.Matrix([0, 4]))]
    displacements = [centers[b] + L * ell - centers[a_] for a_, b, ell in edges]
    p = {1: s.zeros(2, 1), 2: displacements[0], 3: displacements[0] + displacements[1]}
    marks = {1: s.zeros(2, 1), 2: s.Matrix([1, 0]), 3: s.Matrix([1, 1])}
    vectors, gains = [], []
    for index in (2, 3):
        a_, b, ell = edges[index]
        vectors.append(p[a_] + displacements[index] - p[b])
        gains.append(marks[a_] + ell - marks[b])
    V, M = s.Matrix.hstack(*vectors), s.Matrix.hstack(*gains)
    reconstructed = V * M.inv()
    require(M.det() == 6, "nonunimodular test")
    require(matrix_zero(reconstructed - L), "lattice reconstruction")
    require(all(matrix_zero(p[a_] - reconstructed * marks[a_] - centers[a_]) for a_ in centers), "center reconstruction")
    require(not matrix_zero(V - L), "omitting M inverse must fail")
    out["nonunimodular_cochain"] = {"status": "pass", "gain_matrix": [[str(x) for x in row] for row in M.tolist()], "determinant": "6", "omitting_inverse_detected": True}
    out["all_checks_passed"] = True
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
