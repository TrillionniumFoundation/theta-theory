#!/usr/bin/env python3
"""Exact Gate-1 obstruction to the canonical QNL stable holonomy.

The frozen exact QNL certificate gives the cubic Taylor jet of the physical
gray--white--gray return.  This script reconstructs that jet in its exact
eigen-coordinates and checks the resonant coefficient which prevents

    H_n^s(p,z) = D F^n(z)^(-1) D F^n(p)

from converging for any nontrivial sufficiently local z in W^s(p).

The mathematical implication from the checked jet to nonconvergence is the
``resonant increment lemma`` recorded in the companion report.  Briefly, if
lambda*mu=1 and z_n=(h(y_n),y_n) is on the stable graph, then

    y_n / mu^n -> c != 0,
    d_y := partial_x F_2(z_n)
         = (F_{2,xyy}(0)/2) y_n^2 + o(y_n^2).

For K_n=H_n^(-1)H_{n+1}, exact 2x2 symplectic algebra gives

    (K_n)_{21} = -lambda*(lambda/mu)^n*d_y
                -> -lambda*F_{2,xyy}(0)c^2/2 = 325*c^2/144 != 0.

Thus K_n cannot tend to the identity, which is necessary if H_n converges.
The conclusion is fail-closed: the predecessor's finite 96-collision shadow
and its four wedges remain certified, but they are not a canonical holonomy
loop on the QNL periodic fiber.
"""

from __future__ import annotations

import hashlib
import importlib.util
import sys
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
QNL_CERT = HERE / "cm2_fixed_section_qnl_cert.py"
QNL_GRAPH_CERT = HERE / "cm2_gate1_qnl_unstable_graph_cert.py"
SHADOW_CERT = HERE / "cm2_gate1_closed_shadow_twisting_cert.py"
PREVIOUS_AUDIT = HERE / "cm2_gate1_bv_holonomy_typing_obstruction_cert.py"

EXPECTED_SHA256 = {
    QNL_CERT: "31410fcf87e3b1aca862e0ee561582dbc48478fb5ad803eeff6827bafc66c0c6",
    QNL_GRAPH_CERT: "0945b084263e2f48d4cc8521e3e1f24986d28d057ec62de829a18471b8e46fa9",
    SHADOW_CERT: "5ce6e38558bd1de56e17c8ef620fc27b6e73f7b04764d272823964c3b9334abc",
    PREVIOUS_AUDIT: "d0ffea4694401d6b9bc08638cf83c21aa123ad21b0294ef7ccb3458bda55d524",
}


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def verify_dependencies() -> None:
    for path, expected in EXPECTED_SHA256.items():
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != expected:
            raise RuntimeError(
                f"frozen dependency hash changed for {path.name}: "
                f"{actual} != {expected}"
            )
    print("FROZEN_GATE1_RESONANCE_DEPENDENCIES: VERIFIED")


def exact_qnl_eigenjet(module):
    """Rebuild the order-three physical QNL return exactly."""

    zero = module.Qsqrt2(0)
    one = module.Qsqrt2(1)
    gray_radius = module.Qsqrt2(Fraction(9, 25))
    white_radius = module.Qsqrt2(Fraction(4, 25))
    center_distance = module.Qsqrt2(0, Fraction(1, 2))

    arclength = module.Polynomial.variable(0, one)
    momentum = module.Polynomial.variable(1, one)
    angle = arclength.scale(1 / gray_radius)
    cosine = module.Polynomial.constant(one) - (angle * angle).scale(Fraction(1, 2))
    sine = angle - (angle * angle * angle).scale(Fraction(1, 6))
    normal = (cosine, sine)
    tangent = (-sine, cosine)
    cosine_phi = module.Polynomial.constant(one) - (momentum * momentum).scale(
        Fraction(1, 2)
    )
    velocity = (
        cosine_phi * normal[0] + momentum * tangent[0],
        cosine_phi * normal[1] + momentum * tangent[1],
    )
    position = (
        normal[0].scale(gray_radius),
        normal[1].scale(gray_radius),
    )

    white_position, white_velocity = module.collide(
        position,
        velocity,
        (center_distance, zero),
        white_radius,
    )
    gray_position, gray_velocity = module.collide(
        white_position,
        white_velocity,
        (zero, zero),
        gray_radius,
    )
    gray_normal = (
        gray_position[0].scale(1 / gray_radius),
        gray_position[1].scale(1 / gray_radius),
    )
    slope = module.quotient(gray_normal[1], gray_normal[0], zero)
    output_angle = slope - (slope * slope * slope).scale(Fraction(1, 3))
    output_arclength = output_angle.scale(gray_radius)
    gray_tangent = (-gray_normal[1], gray_normal[0])
    output_momentum = module.dot(gray_velocity, gray_tangent)

    matrix_a = module.derivative(output_arclength, 1, 0, zero)
    matrix_b = module.derivative(output_arclength, 0, 1, zero)
    matrix_c = module.derivative(output_momentum, 1, 0, zero)
    matrix_d = module.derivative(output_momentum, 0, 1, zero)
    if matrix_a != matrix_d or matrix_a**2 - matrix_b * matrix_c != one:
        raise RuntimeError("exact QNL linear return lost determinant one")

    module.EXTENSION_SQUARE = matrix_b * matrix_c
    eigen_root = module.EigenExtension(module.Qsqrt2(0), module.Qsqrt2(1))
    adapted_ratio = eigen_root / matrix_c
    unstable = module.EigenExtension.coerce(matrix_a) + eigen_root
    stable = module.EigenExtension.coerce(matrix_a) - eigen_root
    if unstable * stable != module.EigenExtension.coerce(1):
        raise RuntimeError("QNL eigenvalues lost reciprocal identity")

    first = module.Polynomial.variable(0, module.EigenExtension.coerce(1))
    second = module.Polynomial.variable(1, module.EigenExtension.coerce(1))
    original_arclength = first - second.scale(adapted_ratio / 2)
    original_momentum = first.scale(1 / adapted_ratio) + second.scale(Fraction(1, 2))
    transformed_arclength = module.substitute(
        module.convert(output_arclength),
        original_arclength,
        original_momentum,
    )
    transformed_momentum = module.substitute(
        module.convert(output_momentum),
        original_arclength,
        original_momentum,
    )
    output_unstable = transformed_arclength.scale(Fraction(1, 2)) + (
        transformed_momentum.scale(adapted_ratio / 2)
    )
    output_stable = transformed_momentum - transformed_arclength.scale(
        1 / adapted_ratio
    )
    return output_unstable, output_stable, unstable, stable


def certify_resonance(module) -> None:
    output_unstable, output_stable, unstable, stable = exact_qnl_eigenjet(module)
    zero = module.EigenExtension.coerce(0)
    one = module.EigenExtension.coerce(1)

    # The eigencoordinate derivative is exactly diagonal.
    if module.derivative(output_unstable, 1, 0, zero) != unstable:
        raise RuntimeError("unstable diagonal derivative mismatch")
    if module.derivative(output_stable, 0, 1, zero) != stable:
        raise RuntimeError("stable diagonal derivative mismatch")
    if module.derivative(output_unstable, 0, 1, zero) != zero:
        raise RuntimeError("D_y F_1(0) is not zero")
    if module.derivative(output_stable, 1, 0, zero) != zero:
        raise RuntimeError("D_x F_2(0) is not zero")
    if unstable * stable != one:
        raise RuntimeError("lambda*mu is not one")

    # All quadratic terms vanish.  In particular the local stable graph has
    # h''(0)=0 and hence x=h(y)=O(y^3).
    quadratic = ((2, 0), (1, 1), (0, 2))
    for component_name, component in (
        ("F_1", output_unstable),
        ("F_2", output_stable),
    ):
        for degree in quadratic:
            value = module.derivative(component, degree[0], degree[1], zero)
            if value != zero:
                raise RuntimeError(
                    f"{component_name} quadratic derivative {degree} is nonzero: {value}"
                )

    stable_xyy = module.derivative(output_stable, 1, 2, zero)
    expected_normalized = module.EigenExtension.coerce(Fraction(-325, 72))
    if stable_xyy / stable != expected_normalized:
        raise RuntimeError(
            "QNL resonant derivative changed: "
            f"F_2_xyy/mu={stable_xyy / stable}"
        )

    # Exact limiting coefficient in (H_n^{-1}H_{n+1})_{21}, divided by c^2.
    resonant_increment = -unstable * stable_xyy / 2
    expected_increment = module.EigenExtension.coerce(Fraction(325, 144))
    if resonant_increment != expected_increment:
        raise RuntimeError(
            f"resonant increment is not 325/144: {resonant_increment}"
        )
    if resonant_increment == zero:
        raise RuntimeError("resonant increment vanished")

    print("QNL_EIGENJET_LINEAR_DIAGONAL: EXACT")
    print("QNL_EIGENJET_ALL_QUADRATIC_DERIVATIVES_ZERO: EXACT")
    print(f"  unstable_multiplier={unstable}")
    print(f"  stable_multiplier={stable}")
    print("  unstable_times_stable=1")
    print(f"  F2_xyy={stable_xyy}")
    print(f"  F2_xyy_over_stable={stable_xyy / stable}")
    print("QNL_CANONICAL_STABLE_HOLONOMY_RESONANCE: EXACT")
    print(f"  limiting_increment_coefficient={resonant_increment}")
    print("  formula=lim (H_n^-1 H_{n+1})_21=(325/144)*c(z)^2")
    print("  scope=every sufficiently local nontrivial z in W^s(QNL)")
    print("CANONICAL_STABLE_HOLONOMY_AT_QNL: DOES_NOT_CONVERGE")
    print("BUTLER_PARK_CLASS_H_CANONICAL_LIMIT_CONDITION_ON_FAITHFUL_FROZEN_REPRESENTATIVE: FAILS")
    print("HOLDER_COHOMOLOGY_TO_LOCALLY_CONSTANT_QNL_COCYCLE: NOT CERTIFIED")
    print("  note=natural-gauge nonconvergence alone is not a cohomology obstruction")


def certify() -> int:
    verify_dependencies()
    module = load(QNL_CERT, "cm2_gate1_resonance_qnl")
    certify_resonance(module)
    print("NONUNIFORM_HOLONOMY_BLOCK_ROUTE_AT_QNL_PERIODIC_FIBER: UNAVAILABLE")
    print("  reason=the required canonical stable limit fails at the chosen pinching fiber")
    print("FINITE_SHADOW_TRANSPORTED_TWISTING: CERTIFIED_BY_FROZEN_PREDECESSOR")
    print("FINITE_SHADOW_AS_QNL_CANONICAL_HOLONOMY: REFUTED")
    print("PARK_PIRAINO_ON_TWO_FROZEN_NATURAL_CODINGS: NO_GO")
    print("  reason=periodic fiber-bunching obstruction is invariant under same-coding cohomology")
    print("BUTLER_PARK_H_VIA_NEW_COHOMOLOGY_OR_OTHER_NON_FB_THEOREM: OPEN")
    print("GENUINELY_ALTERNATIVE_CODING_OR_TRANSPORT: OPEN")
    print("GATE1_UNCONDITIONAL_TYPICALITY_INPUT: OPEN / FAIL-CLOSED")
    return 0


def main() -> int:
    try:
        return certify()
    except Exception as exc:
        print(f"GATE1_CANONICAL_HOLONOMY_RESONANCE_AUDIT: FAILED: {exc}")
        print("GATE1_UNCONDITIONAL_TYPICALITY_INPUT: OPEN / FAIL-CLOSED")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
