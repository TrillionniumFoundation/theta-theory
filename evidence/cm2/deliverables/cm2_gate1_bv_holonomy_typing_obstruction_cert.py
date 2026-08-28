#!/usr/bin/env python3
"""Gate 1 theorem-typing obstruction for the certified closed shadow loop.

This certificate does not try to turn a finite same-orbit derivative product
into a stable/unstable holonomy by changing notation.  It checks the exact
periodic obstruction to Park--Piraino fiber bunching on the natural QNL
codings, proves that the certified shadow basepoint is a distinct periodic
point, and exhibits an explicit positive fiber gauge under which the raw
cross-fiber identity comparison loses one of its advertised twisting
wedges.

The conclusion is deliberately fail-closed: the finite shadow loop remains
certified, but it has not been identified with

    H^s_{z,p_A} o H^u_{p_A,z}

on the exact QNL periodic fiber.  In particular, a global gray (s,p) chart
is a trivialization, not a canonical holonomy.

Dependency: python-flint == 0.9.0.
"""

from __future__ import annotations

import hashlib
import importlib.util
import sys
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
QNL_EXACT_CERT = HERE / "cm2_fixed_section_qnl_cert.py"
SHADOW_CERT = HERE / "cm2_gate1_closed_shadow_twisting_cert.py"
TANGENT_CERT = HERE / "cm2_gate1_tangent_line_matching_cert.py"

PRECISION_BITS = 900

# These are frozen predecessor hashes, not discovery values.
EXPECTED_SHA256 = {
    QNL_EXACT_CERT: "31410fcf87e3b1aca862e0ee561582dbc48478fb5ad803eeff6827bafc66c0c6",
    SHADOW_CERT: "5ce6e38558bd1de56e17c8ef620fc27b6e73f7b04764d272823964c3b9334abc",
    TANGENT_CERT: "d58a196da59b1f31191ad67239b079e669a5629aec1deaee925fa76d9c489ed1",
}


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def verify_frozen_dependencies() -> None:
    for path, expected in EXPECTED_SHA256.items():
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != expected:
            raise RuntimeError(
                f"frozen dependency hash changed for {path.name}: "
                f"{actual} != {expected}"
            )
    print("FROZEN_THEOREM_TYPING_DEPENDENCIES: VERIFIED")


def exact_qnl_matrix_identity() -> None:
    """Check det(P_A)=1 in Q(sqrt(2)), before any interval numerics."""

    exact = load(QNL_EXACT_CERT, "cm2_gate1_bv_qnl_exact")
    q = exact.Qsqrt2
    alpha = q(Fraction(661, 36), Fraction(-325, 36))
    beta = q(Fraction(859, 100), Fraction(-11, 2))
    gamma = q(Fraction(15625, 324), Fraction(-625, 81))
    if alpha**2 - beta * gamma != q(1):
        raise RuntimeError("exact QNL determinant identity failed")
    print("QNL_EXACT_RETURN_DETERMINANT_ONE: CERTIFIED")


def qnl_periodic_fiber_bunching_obstruction(module):
    """Certify the periodic obstruction to the PP pointwise inequality.

    Park--Piraino use ||A(x)|| ||A(x)^-1|| < 2^theta with
    0 < theta <= 1.  On the natural full-boundary coding p_A has period two,
    so submultiplicativity would force kappa(P_A)<4.  On the induced gray
    return coding it is a fixed point and would force kappa(P_A)<2.
    The spectral condition number lower bound below is greater than 123.
    """

    sqrt_two = module.arb(2).sqrt()
    alpha = (module.arb(661) - 325 * sqrt_two) / 36
    beta = (module.arb(859) - 550 * sqrt_two) / 100
    gamma = module.arb(625) * (25 - 4 * sqrt_two) / 324
    eigen_root = (beta * gamma).sqrt()
    unstable = alpha + eigen_root
    stable = alpha - eigen_root
    spectral_condition_lower = unstable / stable
    determinant = alpha * alpha - beta * gamma

    if not (determinant - 1).contains(0):
        raise RuntimeError(f"Arb QNL determinant misses one: {determinant}")
    if not unstable > 11:
        raise RuntimeError(f"QNL unstable multiplier is not >11: {unstable}")
    if not (stable > module.arb(9) / 100 and stable < module.arb(91) / 1000):
        raise RuntimeError(f"QNL stable multiplier leaves (0.09,0.091): {stable}")
    if not spectral_condition_lower > 123:
        raise RuntimeError(
            "QNL spectral condition-number lower bound is not >123: "
            f"{spectral_condition_lower}"
        )

    # The strict contradictions are written as interval inequalities too.
    if not spectral_condition_lower > 4:
        raise RuntimeError("period-two fiber-bunching contradiction failed")
    if not spectral_condition_lower > 2:
        raise RuntimeError("induced-return fiber-bunching contradiction failed")

    print("QNL_PERIODIC_SPECTRAL_CONDITION_OBSTRUCTION: CERTIFIED")
    print(f"  arb_precision_bits={module.ctx.prec}")
    print(f"  unstable_multiplier={unstable}")
    print(f"  stable_multiplier={stable}")
    print(f"  spectral_condition_lower={spectral_condition_lower}")
    print("  Park_Piraino_period_two_upper=4")
    print("  Park_Piraino_induced_return_upper=2")
    print("NATURAL_SOLID_COLLISION_CODING_FIBER_BUNCHING: REFUTED")
    print("NATURAL_QNL_RETURN_CODING_FIBER_BUNCHING: REFUTED")
    return beta, gamma


def reconstruct_shadow_loop_and_gauge(shadow, tangent, beta, gamma):
    """Reconstruct the predecessor loop and an explicit gauge obstruction."""

    module = tangent.load_frozen_certificate()
    module.ctx.prec = PRECISION_BITS
    shadow.refresh_exact_geometry(module)

    if shadow.SHADOW_A_CENTER == "0":
        raise RuntimeError("shadow root center was replaced by the QNL point")
    root_box = module.arb(shadow.SHADOW_A_CENTER, shadow.SHADOW_A_RADIUS)
    if root_box.contains(0):
        raise RuntimeError(f"shadow root box meets the QNL coordinate: {root_box}")

    q_word = tangent.QNL_FORWARD_WORD
    b_word = tangent.CONNECTOR_REVERSE_FORWARD_WORD
    half_word = q_word * 2 + b_word * 2
    if len(q_word) != 10 or len(b_word) != 14 or len(half_word) != 48:
        raise RuntimeError("frozen shadow word accounting changed")

    theta_start = module.arb.pi() / 4 + 2 * root_box / module.R_GRAY
    half_matrix, _, _ = shadow.symplectic_segment_matrix(
        tangent,
        module,
        theta_start,
        module.arb(0),
        half_word,
    )
    a = half_matrix[0, 0]
    b = half_matrix[0, 1]
    c = half_matrix[1, 0]
    d = half_matrix[1, 1]
    loop_a = a * d + b * c
    loop_b = 2 * b * d
    loop_c = 2 * a * c
    loop = module.arb_mat([[loop_a, loop_b], [loop_c, loop_a]])

    if not loop_a > 0 or not loop_b > 0 or not loop_c > 0:
        raise RuntimeError(f"shadow loop lost its positive hyperbolic form: {loop}")

    # QNL and shadow-loop Perron slopes in the common gray chart.
    qnl_slope = (gamma / beta).sqrt()
    shadow_slope = (loop_c / loop_b).sqrt()
    raw_same_line_wedge = loop_c - loop_b * qnl_slope * qnl_slope
    if not raw_same_line_wedge < -module.arb("1e28"):
        raise RuntimeError(
            f"predecessor raw same-line wedge lost its margin: {raw_same_line_wedge}"
        )

    # C=diag(1,r) maps the two L eigenlines (1,+/-k_L) to the two QNL
    # lines (1,+/-k_A).  It is positive, nontrivial, and arbitrarily close
    # to the identity here.  Under the coordinate change v'=Cv the return
    # matrix is C L C^-1.
    gauge_ratio = qnl_slope / shadow_slope
    if not gauge_ratio > 1 + module.arb("1e-27"):
        raise RuntimeError(f"aligning gauge was not proved nontrivial: {gauge_ratio}")
    if not gauge_ratio < 1 + module.arb("1e-24"):
        raise RuntimeError(f"aligning gauge left its expected small range: {gauge_ratio}")
    aligned = module.arb_mat(
        [
            [loop_a, loop_b / gauge_ratio],
            [gauge_ratio * loop_c, loop_a],
        ]
    )

    # These are zero exactly from r=k_A/k_L and k_L^2=c_L/b_L.
    # Arb containment independently audits the identity without accepting a
    # rounded zero as a strict numerical test.
    aligned_plus_wedge = (
        aligned[1, 0]
        + aligned[1, 1] * qnl_slope
        - qnl_slope * (aligned[0, 0] + aligned[0, 1] * qnl_slope)
    )
    aligned_minus_wedge = (
        aligned[1, 0]
        - aligned[1, 1] * qnl_slope
        + qnl_slope * (aligned[0, 0] - aligned[0, 1] * qnl_slope)
    )
    if not aligned_plus_wedge.contains(0):
        raise RuntimeError(
            f"gauge-aligned plus wedge misses exact zero: {aligned_plus_wedge}"
        )
    if not aligned_minus_wedge.contains(0):
        raise RuntimeError(
            f"gauge-aligned minus wedge misses exact zero: {aligned_minus_wedge}"
        )

    print("ZSTAR_DISTINCT_FROM_PA: CERTIFIED")
    print(f"  zstar_a_root_box={root_box}")
    print("  pa_a_coordinate=0")
    print("ZSTAR_IS_PA_HOMOCLINIC: REFUTED")
    print("  reason=distinct periodic orbits cannot be stable/unstable asymptotic")
    print("RAW_IDENTITY_TRIVIALIZATION_WEDGE: REPLAYED")
    print(f"  qnl_slope={qnl_slope}")
    print(f"  shadow_loop_slope={shadow_slope}")
    print(f"  raw_same_line_wedge={raw_same_line_wedge}")
    print("POSITIVE_LOCALLY_CONSTANT_ALIGNING_GAUGE: CERTIFIED")
    print(f"  C=diag(1,{gauge_ratio})")
    print(f"  aligned_plus_same_line_wedge={aligned_plus_wedge}")
    print(f"  aligned_minus_same_line_wedge={aligned_minus_wedge}")
    print("  exact_identity=r=k_A/k_L and k_L^2=c_L/b_L")
    print("GLOBAL_GRAY_TRIVIALIZATION_AS_CANONICAL_HOLONOMY: REFUTED")


def certify() -> int:
    verify_frozen_dependencies()
    exact_qnl_matrix_identity()

    shadow = load(SHADOW_CERT, "cm2_gate1_bv_shadow")
    tangent = load(TANGENT_CERT, "cm2_gate1_bv_tangent")
    module = tangent.load_frozen_certificate()
    module.ctx.prec = PRECISION_BITS
    shadow.refresh_exact_geometry(module)

    beta, gamma = qnl_periodic_fiber_bunching_obstruction(module)
    reconstruct_shadow_loop_and_gauge(shadow, tangent, beta, gamma)

    print("PARK_PIRAINO_CANONICAL_HOLONOMY_FROM_FIBER_BUNCHING: UNAVAILABLE")
    print("  scope=the two natural certified QNL codings")
    print("  note=nonexistence of every possible holonomy limit is not claimed")
    print("FINITE_ONE_VERTEX_ACTUAL_DERIVATIVE_COCYCLE: NOT CERTIFIED")
    print("BONATTI_VIANA_QNL_FIBER_HOLONOMY_IDENTIFICATION: OPEN / FAIL-CLOSED")
    print("GATE1_UNCONDITIONAL_TYPICALITY_INPUT: OPEN / NO-GO")
    return 0


def main() -> int:
    try:
        return certify()
    except Exception as exc:
        print(f"GATE1_BV_HOLONOMY_TYPING_AUDIT: FAILED: {exc}")
        print("BONATTI_VIANA_QNL_FIBER_HOLONOMY_IDENTIFICATION: NOT CERTIFIED")
        print("GATE1_UNCONDITIONAL_TYPICALITY_INPUT: OPEN / FAIL-CLOSED")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
