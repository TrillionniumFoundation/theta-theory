#!/usr/bin/env python3
"""Gate-2 audit after certification of the directed physical full-cross.

The certified source rectangle is a genuine positive-collision-SRB set.  This
script computes its physical mass in canonical collision coordinates and
checks that the certified 24-collision transition ends in a disjoint target
rectangle, so it is a transition branch rather than a return branch.

The accompanying report then applies Poincare recurrence and Kac's lemma to
the exact two-dimensional first return.  Because the billiard map is
invertible, that full-mass two-dimensional return is invertible as well: its
reverse kernel is a Dirac kernel.  A non-invertible countable full-branch
kernel appears only after a stable quotient, which has not been constructed
on this source rectangle.

Dependency: python-flint == 0.9.0.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
FULL_CROSS_CERT = HERE / "cm2_gate1_full_cross_transport_cert.py"
TANGENT_CERT = HERE / "cm2_gate1_tangent_line_matching_cert.py"
PRECISION_BITS = 500


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def certify() -> int:
    full_cross = load(FULL_CROSS_CERT, "cm2_gate2_post_full_cross_constants")
    tangent = load(TANGENT_CERT, "cm2_gate2_post_full_cross_tangent")
    billiard = tangent.load_frozen_certificate()
    billiard.ctx.prec = PRECISION_BITS

    # Fail if the certified rectangle is silently changed.
    expected = {
        "SOURCE_T_RADIUS": "1e-20",
        "SOURCE_TRANSVERSE_RADIUS": "2.1e-18",
        "TARGET_UNSTABLE_RADIUS": "1e-8",
        "TARGET_STABLE_RADIUS": "1e-14",
    }
    for field, value in expected.items():
        if getattr(full_cross, field) != value:
            raise RuntimeError(
                f"full-cross rectangle changed: {field}={getattr(full_cross, field)}"
            )

    root, slope_a, _ = tangent.setup_fixed_data(billiard)
    t_decimal, u_decimal = tangent.refine_center(billiard, root, slope_a, _)
    t_center = billiard.arb(t_decimal)
    u_center = billiard.arb(u_decimal)

    r_t = billiard.arb(full_cross.SOURCE_T_RADIUS)
    r_b = billiard.arb(full_cross.SOURCE_TRANSVERSE_RADIUS)
    r_x = billiard.arb(full_cross.TARGET_UNSTABLE_RADIUS)
    r_u = billiard.arb(full_cross.TARGET_STABLE_RADIUS)

    # In the QNL eigenchart, s=a+b and p=k_A(a-b).  Hence
    # |d(s,p)/d(a,b)|=2 k_A.  The normalized collision law on the two solid
    # obstacles is (2*total_boundary)^-1 ds dp, with
    # total_boundary=2*pi*(9/25+4/25)=26*pi/25.
    if billiard.R_GRAY != billiard.arb(9) / 25:
        raise RuntimeError("gray radius changed")
    if billiard.R_WHITE != billiard.arb(4) / 25:
        raise RuntimeError("white radius changed")
    total_boundary = 2 * billiard.arb.pi() * (
        billiard.R_GRAY + billiard.R_WHITE
    )
    collision_density = 1 / (2 * total_boundary)
    eigen_jacobian = 2 * slope_a
    rectangle_area = (2 * r_t) * (2 * r_b)
    base_mass = collision_density * eigen_jacobian * rectangle_area
    kac_mean = 1 / base_mass

    if not base_mass > billiard.arb("1.7e-37"):
        raise RuntimeError(f"source SRB mass lower bound failed: {base_mass}")
    if not base_mass < billiard.arb("1.8e-37"):
        raise RuntimeError(f"source SRB mass upper bound failed: {base_mass}")
    if not kac_mean > billiard.arb("5e36"):
        raise RuntimeError(f"Kac mean lower bound failed: {kac_mean}")

    # The entire source rectangle is far from grazing.
    momentum_radius = slope_a * (abs(t_center) + r_t + r_b)
    if not momentum_radius < billiard.arb(1) / 2:
        raise RuntimeError(f"source rectangle may approach grazing: {momentum_radius}")

    # Compare the source and final target using only their gray collision
    # angles.  Source: theta=pi/4+(a+b)/R_G.  Target connector eigenchart:
    # s=x+u, centered at (0,u0), theta=theta_B+s/R_G.
    source_angle_center = billiard.arb.pi() / 4 + t_center / billiard.R_GRAY
    source_angle_radius = (r_t + r_b) / billiard.R_GRAY
    target_angle_center = root.boxes[0] + u_center / billiard.R_GRAY
    target_angle_radius = (r_x + r_u) / billiard.R_GRAY
    angular_gap = (
        abs(source_angle_center - target_angle_center)
        - source_angle_radius
        - target_angle_radius
    )
    if not angular_gap > billiard.arb("0.001"):
        raise RuntimeError(f"source/target disjointness failed: {angular_gap}")

    print("DIRECTED_FULL_CROSS_INPUT: CERTIFIED")
    print("Q_ANCHORED_2D_SOURCE_RECTANGLE: CERTIFIED")
    print(f"  source_half_widths=(a,b)=({r_t},{r_b})")
    print(f"  qnl_eigen_slope_k_A={slope_a}")
    print(f"  canonical_eigen_jacobian=2*k_A={eigen_jacobian}")
    print(f"  total_solid_boundary=26*pi/25={total_boundary}")
    print("  exact_mass_formula=(105*k_A/(13*pi))*10^-38")
    print(f"  collision_SRB_mass={base_mass}")
    print(f"  Kac_mean_first_return=1/mass={kac_mean}")
    print(f"  maximum_abs_momentum={momentum_radius}")
    print("TRANSITION_24_IS_NOT_A_RETURN_TO_SOURCE: CERTIFIED")
    print(f"  source_target_angular_gap={angular_gap}")
    print("TWO_DIMENSIONAL_FIRST_RETURN_FULL_MASS: PROVED_BY_POINCARE")
    print("TWO_DIMENSIONAL_REVERSE_KERNEL: DETERMINISTIC_DIRAC")
    print("  reason=invertible billiard first return has one a.e. predecessor")
    print("KAC_ONLY_TAIL_BOUND=min(1,1/(mass*L))")
    print("STABLE_SATURATED_YOUNG_RECTANGLE: NOT_CERTIFIED")
    print("NONINVERTIBLE_FULL_BRANCH_STABLE_QUOTIENT: NOT_CERTIFIED")
    print("EXECUTABLE_FIRST_RETURN_BRANCH_WORD: NOT_CERTIFIED")
    print("PHYSICAL_GATE2: NOT_CERTIFIED")
    return 0


def main() -> int:
    try:
        return certify()
    except Exception as exc:
        print(f"POST_FULL_CROSS_RETURN_BASE: FAILED: {exc}")
        print("Q_ANCHORED_2D_SOURCE_RECTANGLE: NOT_CERTIFIED")
        print("STABLE_SATURATED_YOUNG_RECTANGLE: NOT_CERTIFIED")
        print("PHYSICAL_GATE2: NOT_CERTIFIED")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
