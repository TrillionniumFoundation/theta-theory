#!/usr/bin/env python3
"""Gate-2 local return-strip certificate from the 96-collision shadow loop.

The predecessor certifies an exact fixed point of the 96-collision word and
its same-orbit derivative.  Here that point is thickened.  A correlated
second-order Taylor replay is made in the true Perron coordinates of the
closed derivative.  Exact closure is used to recenter the output; the raw
96-step interval centre is only a diagnostic and is not allowed to create a
fake translation error.

The result is one positive-width vertical return strip which maps across a
local rectangle, plus explicit stable/unstable cone bounds.  It is one
branch, not a full-mass partition.  No affine eigen-fibre is relabelled as an
invariant stable holonomy quotient.

Dependency: python-flint == 0.9.0.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
CLOSED_CERT = HERE / "cm2_gate1_closed_shadow_twisting_cert.py"
FULL_CROSS_CERT = HERE / "cm2_gate1_full_cross_transport_cert.py"
TANGENT_CERT = HERE / "cm2_gate1_tangent_line_matching_cert.py"
TRUE_GRAPH_CERT = HERE / "cm2_gate1_true_graph_krawczyk_cert.py"
QNL_CERT = HERE / "cm2_gate1_qnl_unstable_graph_cert.py"
CONNECTOR_CERT = HERE / "cm2_gate1_connector_stable_graph_cert.py"

PRECISION_BITS = 900
RETURN_RECTANGLE_RADIUS = "1e-43"
SOURCE_UNSTABLE_RADIUS = "1.86e-96"
UNSTABLE_CONE_SLOPE = "1e-40"
STABLE_CONE_SLOPE = "1e-53"


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def certify() -> int:
    closed = load(CLOSED_CERT, "cm2_gate2_local_return_closed")
    full = load(FULL_CROSS_CERT, "cm2_gate2_local_return_full")
    tangent = load(TANGENT_CERT, "cm2_gate2_local_return_tangent")
    parent = load(TRUE_GRAPH_CERT, "cm2_gate2_local_return_parent")
    qnl = load(QNL_CERT, "cm2_gate2_local_return_qnl")
    connector = load(CONNECTOR_CERT, "cm2_gate2_local_return_connector")

    module = tangent.load_frozen_certificate()
    module.ctx.prec = PRECISION_BITS
    closed.refresh_exact_geometry(module)
    root, slope_a, slope_b = tangent.setup_fixed_data(module)
    del root, slope_a, slope_b

    q_word = tangent.QNL_FORWARD_WORD
    b_word = tangent.CONNECTOR_REVERSE_FORWARD_WORD
    half_word = q_word * 2 + b_word * 2
    full_word = q_word * 2 + b_word * 4 + q_word * 2
    if len(half_word) != 48 or len(full_word) != 96:
        raise RuntimeError("closed word lengths changed")

    root_box = module.arb(closed.SHADOW_A_CENTER, closed.SHADOW_A_RADIUS)
    theta_star = module.arb.pi() / 4 + 2 * root_box / module.R_GRAY
    half_matrix, _, _ = closed.symplectic_segment_matrix(
        tangent, module, theta_star, module.arb(0), half_word
    )
    a, b = half_matrix[0, 0], half_matrix[0, 1]
    c, d = half_matrix[1, 0], half_matrix[1, 1]
    loop_a = a * d + b * c
    loop_b = 2 * b * d
    loop_c = 2 * a * c
    if not loop_b > 0 or not loop_c > 0:
        raise RuntimeError("closed derivative lost positive off-diagonal entries")

    # D_loop=[[A,B],[C,A]].  Its Perron coordinates are
    # ds=u+v, dp=k_loop(u-v), with exact expanding eigenvalue A+B*k_loop.
    k_loop = (loop_c / loop_b).sqrt()
    expansion = loop_a + loop_b * k_loop
    if not expansion > module.arb("1e53"):
        raise RuntimeError(f"loop expansion too small: {expansion}")

    rectangle_radius = module.arb(RETURN_RECTANGLE_RADIUS)
    # This is a fixed decimal rational, not an Arb interval selected from an
    # interval-valued eigenvalue.  The nearby quantity 2*R/expansion is only
    # printed as a diagnostic reference width.
    source_unstable_radius = module.arb(SOURCE_UNSTABLE_RADIUS)
    expansion_reference_radius = 2 * rectangle_radius / expansion
    source_stable_radius = rectangle_radius
    if not source_unstable_radius < expansion_reference_radius:
        raise RuntimeError("fixed unstable radius exceeds 2R/lambda reference")

    replay = full.replay_rectangle(
        parent,
        qnl,
        connector,
        tangent,
        module,
        parameter_center=module.arb(0),
        parameter_radius=source_unstable_radius,
        transverse_radius=source_stable_radius,
        base_angle=theta_star,
        slope=k_loop,
        word=full_word,
    )
    output = full.to_connector_eigen(
        module, replay, theta_star, k_loop
    )

    # The predecessor proves that the exact root is fixed.  The raw centre
    # interval loses that correlation over 96 steps but must still contain
    # zero; it is never used in the covering inequalities.
    if not output.center[0].contains(0) or not output.center[1].contains(0):
        raise RuntimeError(f"raw return centre misses exact closure: {output.center}")

    unstable_error = (
        abs(output.linear[0][1]) * source_stable_radius
        + output.remainder[0]
    )
    negative_face = (
        -output.linear[0][0] * source_unstable_radius
        + full.symmetric_ball(parent, module, unstable_error)
    )
    positive_face = (
        output.linear[0][0] * source_unstable_radius
        + full.symmetric_ball(parent, module, unstable_error)
    )
    stable_radius = (
        abs(output.linear[1][0]) * source_unstable_radius
        + abs(output.linear[1][1]) * source_stable_radius
        + output.remainder[1]
    )
    stable_image = full.symmetric_ball(parent, module, stable_radius)

    if not negative_face < -rectangle_radius:
        raise RuntimeError(f"negative unstable face does not exit: {negative_face}")
    if not positive_face > rectangle_radius:
        raise RuntimeError(f"positive unstable face does not exit: {positive_face}")
    if not stable_image > -rectangle_radius or not stable_image < rectangle_radius:
        raise RuntimeError(f"stable image leaves return rectangle: {stable_image}")

    thresholds = {
        "flight": module.arb(18) / 100,
        "discriminant": module.arb(1) / 100,
        "incidence": module.arb(63) / 100,
        "clearance": module.arb(22) / 100,
    }
    for name, threshold in thresholds.items():
        if not replay.minima[name] > threshold:
            raise RuntimeError(f"return-strip word margin {name} fails")

    derivative = output.derivative_box(module)
    aa, bb = derivative[0]
    cc, dd = derivative[1]
    aa_lower = aa.lower()
    bb_abs = abs(bb).upper()
    cc_abs = abs(cc).upper()
    dd_abs = abs(dd).upper()
    if not aa_lower > module.arb("1e53"):
        raise RuntimeError(f"return derivative expansion lost: {aa}")
    if not bb_abs < module.arb(1) / 5:
        raise RuntimeError(f"upper cross derivative too large: {bb}")
    if not cc_abs < module.arb("7e11"):
        raise RuntimeError(f"lower cross derivative too large: {cc}")
    if not dd_abs < module.arb(1) / 5:
        raise RuntimeError(f"stable derivative too large: {dd}")

    unstable_cone = module.arb(UNSTABLE_CONE_SLOPE)
    stable_cone = module.arb(STABLE_CONE_SLOPE)
    unstable_ratio = (
        cc_abs + dd_abs * unstable_cone
    ) / (aa_lower - bb_abs * unstable_cone)
    stable_inverse_ratio = (
        dd_abs * stable_cone + bb_abs
    ) / (aa_lower - cc_abs * stable_cone)
    if not unstable_ratio < unstable_cone:
        raise RuntimeError(f"unstable cone is not invariant: {unstable_ratio}")
    if not stable_inverse_ratio < stable_cone:
        raise RuntimeError(f"stable inverse cone is not invariant: {stable_inverse_ratio}")
    stable_graph_unstable_width = stable_cone * rectangle_radius
    if not stable_graph_unstable_width < source_unstable_radius:
        raise RuntimeError("stable graph cone does not fit in source strip")

    # Normalized collision SRB law is 25/(52*pi) ds dp.  In the Perron
    # chart, (ds,dp)=(du+dv,k_loop(du-dv)), so the absolute Jacobian is
    # 2*k_loop.  The source strip has (u,v)-area 4*r_u*r_v.
    source_srb_mass = (
        module.arb(25) / (52 * module.arb.pi())
        * 8 * k_loop * source_unstable_radius * source_stable_radius
    )
    if not source_srb_mass > module.arb("1e-139"):
        raise RuntimeError(f"source SRB mass positivity bound fails: {source_srb_mass}")

    print("CLOSED_96_WORD_INPUT: VERIFIED")
    print("LOCAL_RETURN_PERRON_CHART: CERTIFIED")
    print(f"  loop_projective_slope={k_loop}")
    print(f"  loop_expansion={expansion}")
    print(f"  rectangle_half_width=(u,v)=({rectangle_radius},{rectangle_radius})")
    print(
        "  source_strip_half_width=(u,v)="
        f"({source_unstable_radius},{source_stable_radius})"
    )
    print(f"  two_R_over_expansion_reference={expansion_reference_radius}")
    print(f"  normalized_collision_SRB_mass={source_srb_mass}")
    print("POSITIVE_WIDTH_96_COLLISION_RETURN_STRIP: CERTIFIED")
    print(f"  negative_unstable_face={negative_face}")
    print(f"  positive_unstable_face={positive_face}")
    print(f"  full_stable_image={stable_image}")
    print(f"  nonlinear_remainder={output.remainder}")
    print(f"  maximum_physical_state_radius={replay.maximum_state_radius}")
    for name, value in replay.minima.items():
        print(f"  minimum_{name}={value}")
    print("LOCAL_HYPERBOLIC_CONES: CERTIFIED")
    print(f"  derivative_box={module.arb_mat(derivative)}")
    print(f"  unstable_cone_slope={unstable_cone}")
    print(f"  unstable_cone_image_slope={unstable_ratio}")
    print(f"  stable_cone_slope={stable_cone}")
    print(f"  stable_inverse_cone_image_slope={stable_inverse_ratio}")
    print(f"  stable_graph_u_width_bound={stable_graph_unstable_width}")
    print("FIXED_POINT_LOCAL_STABLE_UNSTABLE_PLAQUES: CERTIFIED_BY_GRAPH_TRANSFORM")
    print("INTERVAL_INDEXED_LOCAL_STABLE_FOLIATION: NOT_CERTIFIED")
    print("  obstruction=return-word domain is not invariant/stable-saturated")
    print("AFFINE_EIGEN_FIBER_IS_INVARIANT_STABLE_HOLONOMY: NOT_CERTIFIED")
    print("STABLE_HOLONOMY_FAMILY_ACROSS_FULL_MASS_BASE: NOT_CERTIFIED")
    print("FIRST_ONTO_STABLE_QUOTIENT_INVERSE_BRANCH: NOT_CERTIFIED")
    print("FULL_MASS_COUNTABLE_RETURN_PARTITION: NOT_CERTIFIED")
    print("PHYSICAL_GATE2: NOT_CERTIFIED")
    return 0


def main() -> int:
    try:
        return certify()
    except Exception as exc:
        print(f"GATE2_LOCAL_RETURN_STRIP: FAILED: {exc}")
        print("POSITIVE_WIDTH_96_COLLISION_RETURN_STRIP: NOT_CERTIFIED")
        print("FIRST_ONTO_STABLE_QUOTIENT_INVERSE_BRANCH: NOT_CERTIFIED")
        print("PHYSICAL_GATE2: NOT_CERTIFIED")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
