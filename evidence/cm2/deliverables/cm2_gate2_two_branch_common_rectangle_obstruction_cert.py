#!/usr/bin/env python3
"""Gate-2 two-branch common-Perron-rectangle obstruction certificate.

The exact QNL period-two point and the exact 96-collision shadow-loop point
are put in the same gray Perron chart.  A concrete common rectangle and a
short-QNL vertical source strip are certified, including physical first
hits, face covering, stable entry, and cones.  A disjoint candidate source
strip is then placed at the 96-loop point.

The latter cannot be a full-height axis-aligned vertical strip in either of
the two natural affine Perron charts audited here (the QNL chart and the
loop chart): every common product rectangle containing both fixed points
contains the mixed-corner point (u,v)=(a_*,0), and every full-height
vertical strip containing the loop point contains that point.  In the QNL
chart its first 69 collisions follow the declared word, but the intended
70th target has strictly negative line-circle discriminant.  In the loop
chart the corresponding mixed corner follows 73 collisions and then misses
the intended 74th target.  Thus the specified 96-word full-height branch is
not physical in either audited affine chart.

This is deliberately narrower than ruling out every possible coordinate
choice or every two-branch horseshoe.  A curvilinear stable-saturated branch
could avoid the mixed corner and remains open.

There is one quantified extension beyond exactly vertical fibres.  A
full-height graph through the loop fixed point with Lipschitz slope
``|du/dv| <= 10^-100`` must cross ``v=0`` inside a tiny interval about the
mixed corner.  Interval replay on that entire crossing interval retains the
same strict misses.  This very narrow conditional cone result is not a
construction of such a plaque and does not cover unrestricted curvilinear
stable leaves.

Dependency: python-flint == 0.9.0.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
CLOSED_CERT = HERE / "cm2_gate1_closed_shadow_twisting_cert.py"
TANGENT_CERT = HERE / "cm2_gate1_tangent_line_matching_cert.py"
QNL_GRAPH_CERT = HERE / "cm2_gate1_qnl_unstable_graph_cert.py"

PRECISION_BITS = 900
COMMON_RADIUS = "4.2e-15"
QNL_SOURCE_LEFT = "-8e-16"
QNL_SOURCE_RIGHT = "1e-17"
LOOP_SOURCE_LEFT_OFFSET = "-1e-69"
LOOP_SOURCE_RIGHT_OFFSET = "8e-68"
UNSTABLE_CONE_SLOPE = "1e-9"
STABLE_CONE_SLOPE = "1e-9"
FULL_HEIGHT_PLAQUE_LIPSCHITZ_BOUND = "1e-100"


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def symmetric_ball(module, radius):
    radius = radius.abs_upper()
    text = (module.arb(101) * radius / 100).str(130, radius=False, more=True)
    ball = module.arb(0, text)
    if not ball.contains(radius) or not ball.contains(-radius):
        raise RuntimeError(f"failed to build symmetric ball for {radius}")
    return ball


def certify() -> int:
    closed = load(CLOSED_CERT, "cm2_gate2_two_branch_closed")
    tangent = load(TANGENT_CERT, "cm2_gate2_two_branch_tangent")
    qnl = load(QNL_GRAPH_CERT, "cm2_gate2_two_branch_qnl")

    module = tangent.load_frozen_certificate()
    module.ctx.prec = PRECISION_BITS
    closed.refresh_exact_geometry(module)
    root, slope_a, _ = tangent.setup_fixed_data(module)
    del root

    a_star = module.arb(closed.SHADOW_A_CENTER, closed.SHADOW_A_RADIUS)
    if not a_star < module.arb("-8.29e-15"):
        raise RuntimeError(f"shadow root lost negative separation: {a_star}")
    if not a_star > module.arb("-8.30e-15"):
        raise RuntimeError(f"shadow root separation too large: {a_star}")

    # Compare the loop Perron slope with the QNL Perron slope in the same
    # canonical gray (s,p) trivialisation.  They are extremely close but not
    # equal; that distinction is retained in the common-chart typing.
    q_word = tangent.QNL_FORWARD_WORD
    b_word = tangent.CONNECTOR_REVERSE_FORWARD_WORD
    half_word = q_word * 2 + b_word * 2
    full_word = q_word * 2 + b_word * 4 + q_word * 2
    theta_star = module.arb.pi() / 4 + 2 * a_star / module.R_GRAY
    half_matrix, _, _ = closed.symplectic_segment_matrix(
        tangent, module, theta_star, module.arb(0), half_word
    )
    aa, bb = half_matrix[0, 0], half_matrix[0, 1]
    cc, dd = half_matrix[1, 0], half_matrix[1, 1]
    loop_a = aa * dd + bb * cc
    loop_b = 2 * bb * dd
    loop_c = 2 * aa * cc
    loop_slope = (loop_c / loop_b).sqrt()
    slope_difference = loop_slope - slope_a
    if not abs(slope_difference) > module.arb("3.74e-25"):
        raise RuntimeError("loop/QNL Perron-slope mismatch lower bound lost")
    if not abs(slope_difference) < module.arb("3.75e-25"):
        raise RuntimeError("loop/QNL Perron-slope mismatch upper bound lost")
    loop_stable_tilt_in_qnl_chart = abs(
        (slope_a - loop_slope) / (slope_a + loop_slope)
    )
    if not loop_stable_tilt_in_qnl_chart > module.arb("2.7e-26"):
        raise RuntimeError("loop stable-axis common-chart tilt lower bound lost")
    qnl_to_physical = module.arb_mat(
        [[1, 1], [slope_a, -slope_a]]
    )
    physical_to_qnl = module.arb_mat(
        [[module.arb(1) / 2, 1 / (2 * slope_a)],
         [module.arb(1) / 2, -1 / (2 * slope_a)]]
    )
    loop_in_qnl_chart = (
        physical_to_qnl
        * module.arb_mat([[loop_a, loop_b], [loop_c, loop_a]])
        * qnl_to_physical
    )
    common_vertical_shear = loop_in_qnl_chart[0, 1]
    if not abs(common_vertical_shear) > module.arb("1e27"):
        raise RuntimeError("common-chart loop vertical shear lower bound lost")

    # In the common QNL Perron chart, p_A=(0,0).  Since the shadow point has
    # delta s=2*a_* and p=0, z_*=(a_*,a_*).
    common_center = a_star / 2
    common_radius = module.arb(COMMON_RADIUS)
    common_lower = common_center - common_radius
    common_upper = common_center + common_radius
    if not common_lower < a_star or not a_star < common_upper:
        raise RuntimeError("common rectangle misses the shadow fixed point")
    if not common_lower < 0 or not module.arb(0) < common_upper:
        raise RuntimeError("common rectangle misses the QNL fixed point")
    minimum_common_half_width = -a_star / 2
    if not minimum_common_half_width > module.arb("4.14e-15"):
        raise RuntimeError("common stable-width lower bound was lost")

    # A concrete asymmetric short-QNL vertical strip.  Asymmetry is needed
    # because p_A lies close to the upper common-rectangle face.
    q_left = module.arb(QNL_SOURCE_LEFT)
    q_right = module.arb(QNL_SOURCE_RIGHT)
    q_center = (q_left + q_right) / 2
    q_radius = (q_right - q_left) / 2
    q_x_box = q_center + module.arb(0, "4.05e-16")
    common_y_box = common_center + module.arb(0, COMMON_RADIUS)
    q_x_deviation = (q_x_box - q_center).abs_upper()
    common_y_deviation = (common_y_box - common_center).abs_upper()
    if not q_x_box.contains(q_left) or not q_x_box.contains(q_right):
        raise RuntimeError("exact QNL source box lost a declared face")
    if not common_lower < q_left or not q_right < common_upper:
        raise RuntimeError("QNL source strip leaves the common rectangle")
    if not q_left < 0 or not module.arb(0) < q_right:
        raise RuntimeError("QNL source strip does not contain p_A")

    q_full_image = qnl.qnl_return(module, q_x_box, common_y_box)
    q_left_center_image = qnl.qnl_return(module, q_left, common_center)
    q_right_center_image = qnl.qnl_return(module, q_right, common_center)
    q_center_image = qnl.qnl_return(module, q_center, common_center)
    # Direct interval values of a two-collision return lose the exact return
    # correlation.  Use the mean-value form with derivatives enclosed on the
    # whole source box.
    q_face_error = abs(q_full_image.unstable.gradient[1]) * common_y_deviation
    q_left_face = q_left_center_image.unstable.value + symmetric_ball(
        module, q_face_error
    )
    q_right_face = q_right_center_image.unstable.value + symmetric_ball(
        module, q_face_error
    )
    q_stable_error = (
        abs(q_full_image.stable.gradient[0]) * q_x_deviation
        + abs(q_full_image.stable.gradient[1]) * common_y_deviation
    )
    q_stable_image = q_center_image.stable.value + symmetric_ball(
        module, q_stable_error
    )
    if not q_left_face < common_lower:
        raise RuntimeError(
            f"QNL left face does not exit: {q_left_face}"
        )
    if not q_right_face > common_upper:
        raise RuntimeError(
            f"QNL right face does not exit: {q_right_face}"
        )
    if not q_stable_image > common_lower:
        raise RuntimeError("QNL stable image crosses the lower common face")
    if not q_stable_image < common_upper:
        raise RuntimeError("QNL stable image crosses the upper common face")

    physical_thresholds = {
        "flight": module.arb("0.18"),
        "discriminant": module.arb("0.025"),
        "incidence": module.arb("0.99"),
        "clearance": module.arb("0.36"),
    }
    q_physical = {
        "flight": q_full_image.minimum_flight,
        "discriminant": q_full_image.minimum_discriminant,
        "incidence": q_full_image.minimum_incidence,
        "clearance": q_full_image.minimum_clearance,
    }
    for name, threshold in physical_thresholds.items():
        if not q_physical[name] > threshold:
            raise RuntimeError(f"QNL common-strip physical margin {name} fails")

    derivative = [q_full_image.unstable.gradient, q_full_image.stable.gradient]
    d_a, d_b = derivative[0]
    d_c, d_d = derivative[1]
    a_lower = d_a.lower()
    b_abs = abs(d_b).upper()
    c_abs = abs(d_c).upper()
    d_abs = abs(d_d).upper()
    unstable_cone = module.arb(UNSTABLE_CONE_SLOPE)
    stable_cone = module.arb(STABLE_CONE_SLOPE)
    unstable_image_slope = (
        c_abs + d_abs * unstable_cone
    ) / (a_lower - b_abs * unstable_cone)
    stable_inverse_image_slope = (
        d_abs * stable_cone + b_abs
    ) / (a_lower - c_abs * stable_cone)
    if not unstable_image_slope < unstable_cone:
        raise RuntimeError(
            "QNL common-strip unstable cone is not invariant: "
            f"{unstable_image_slope} versus {unstable_cone}; "
            f"D={module.arb_mat(derivative)}"
        )
    if not stable_inverse_image_slope < stable_cone:
        raise RuntimeError("QNL common-strip stable inverse cone is not invariant")

    # The candidate loop strip is disjoint in u and is wide enough at the
    # derivative level to be plausible.  Its full stable span is the common
    # y interval, so it necessarily contains P_mix=(a_*,0).
    loop_left = a_star + module.arb(LOOP_SOURCE_LEFT_OFFSET)
    loop_right = a_star + module.arb(LOOP_SOURCE_RIGHT_OFFSET)
    if not common_lower < loop_left or not loop_right < common_upper:
        raise RuntimeError("candidate loop source leaves common rectangle")
    strip_gap = q_left - loop_right
    if not strip_gap > module.arb("7.49e-15"):
        raise RuntimeError(f"candidate source strips are not disjoint: {strip_gap}")
    if not loop_left < a_star or not a_star < loop_right:
        raise RuntimeError("candidate loop source does not contain z_* in u")
    if not common_y_box.contains(0) or not common_y_box.contains(a_star):
        raise RuntimeError("common stable span misses a required mixed corner")

    # P_mix=(u,v)=(a_*,0), hence delta s=a_* and p=k_A*a_*.
    # Certify the first 69 intended collisions, then compute the intended
    # 70th line-circle discriminant without taking a square root.
    probe_theta = module.Dual(
        module.arb.pi() / 4 + a_star / module.R_GRAY, dimension=0
    )
    probe_momentum = module.Dual(slope_a * a_star, dimension=0)
    prefix = tangent.propagate(
        module, "G", probe_theta, probe_momentum, full_word[:69]
    )
    next_key = full_word[69]
    current_kind = full_word[68][0]
    position, velocity, _ = tangent.initial_state(
        module, current_kind, prefix.theta, prefix.momentum
    )
    target = module.obstacle(*next_key)
    displacement = (
        position[0] - target.center[0],
        position[1] - target.center[1],
    )
    linear = module.dual_dot(displacement, velocity)
    offset = (
        module.dual_dot(displacement, displacement)
        - target.radius * target.radius
    )
    bad_discriminant = linear * linear - offset
    if not bad_discriminant.value < module.arb("-0.29"):
        raise RuntimeError(
            f"mixed-corner 70th discriminant is not strictly negative: "
            f"{bad_discriminant.value}"
        )

    # The alternative of taking the loop's own Perron slope as the common
    # slope does not rescue an affine full-height strip.  Its corresponding
    # mixed corner follows three more declared collisions, then misses the
    # intended 74th target with another strict negative discriminant.  This
    # separates genuine nonlinear stable-manifold curvature from the tiny
    # QNL/loop eigenslope mismatch above.
    loop_probe_momentum = module.Dual(loop_slope * a_star, dimension=0)
    loop_prefix = tangent.propagate(
        module, "G", probe_theta, loop_probe_momentum, full_word[:73]
    )
    loop_next_key = full_word[73]
    loop_current_kind = full_word[72][0]
    loop_position, loop_velocity, _ = tangent.initial_state(
        module, loop_current_kind, loop_prefix.theta, loop_prefix.momentum
    )
    loop_target = module.obstacle(*loop_next_key)
    loop_displacement = (
        loop_position[0] - loop_target.center[0],
        loop_position[1] - loop_target.center[1],
    )
    loop_linear = module.dual_dot(loop_displacement, loop_velocity)
    loop_offset = (
        module.dual_dot(loop_displacement, loop_displacement)
        - loop_target.radius * loop_target.radius
    )
    loop_bad_discriminant = loop_linear * loop_linear - loop_offset
    if not loop_bad_discriminant.value < module.arb("-0.21"):
        raise RuntimeError(
            "loop-Perron mixed-corner 74th discriminant is not negative: "
            f"{loop_bad_discriminant.value}"
        )

    # Conditional narrow-cone extension.  Let u=g(v) be a full-height graph
    # through z_*=(a_*,a_*) in either audited Perron product chart.  If
    # Lip(g)<=eta, then |g(0)-a_*|<=eta|a_*|.  Enclose every possible v=0
    # crossing and replay the relevant word prefix on the whole interval.
    # This does not assert existence of the graph; it only rules out the
    # explicitly quantified class as a physical full-height 96-word strip.
    plaque_lipschitz = module.arb(FULL_HEIGHT_PLAQUE_LIPSCHITZ_BOUND)
    plaque_crossing_radius = plaque_lipschitz * abs(a_star)
    plaque_crossing_u = a_star + symmetric_ball(module, plaque_crossing_radius)
    if not plaque_crossing_u.contains(a_star):
        raise RuntimeError("narrow-cone crossing box misses the mixed corner")

    qnl_graph_theta = module.Dual(
        module.arb.pi() / 4 + plaque_crossing_u / module.R_GRAY,
        dimension=0,
    )
    qnl_graph_momentum = module.Dual(
        slope_a * plaque_crossing_u,
        dimension=0,
    )
    qnl_graph_prefix = tangent.propagate(
        module, "G", qnl_graph_theta, qnl_graph_momentum, full_word[:69]
    )
    qnl_graph_position, qnl_graph_velocity, _ = tangent.initial_state(
        module,
        full_word[68][0],
        qnl_graph_prefix.theta,
        qnl_graph_prefix.momentum,
    )
    qnl_graph_target = module.obstacle(*full_word[69])
    qnl_graph_displacement = (
        qnl_graph_position[0] - qnl_graph_target.center[0],
        qnl_graph_position[1] - qnl_graph_target.center[1],
    )
    qnl_graph_linear = module.dual_dot(
        qnl_graph_displacement, qnl_graph_velocity
    )
    qnl_graph_offset = (
        module.dual_dot(qnl_graph_displacement, qnl_graph_displacement)
        - qnl_graph_target.radius * qnl_graph_target.radius
    )
    qnl_graph_bad_discriminant = qnl_graph_linear * qnl_graph_linear - qnl_graph_offset
    if not qnl_graph_bad_discriminant.value < module.arb("-0.29"):
        raise RuntimeError(
            "narrow QNL-Perron graph crossing may hit collision 70: "
            f"{qnl_graph_bad_discriminant.value}"
        )

    loop_graph_theta = module.Dual(
        module.arb.pi() / 4 + plaque_crossing_u / module.R_GRAY,
        dimension=0,
    )
    loop_graph_momentum = module.Dual(
        loop_slope * plaque_crossing_u,
        dimension=0,
    )
    loop_graph_prefix = tangent.propagate(
        module, "G", loop_graph_theta, loop_graph_momentum, full_word[:73]
    )
    loop_graph_position, loop_graph_velocity, _ = tangent.initial_state(
        module,
        full_word[72][0],
        loop_graph_prefix.theta,
        loop_graph_prefix.momentum,
    )
    loop_graph_target = module.obstacle(*full_word[73])
    loop_graph_displacement = (
        loop_graph_position[0] - loop_graph_target.center[0],
        loop_graph_position[1] - loop_graph_target.center[1],
    )
    loop_graph_linear = module.dual_dot(
        loop_graph_displacement, loop_graph_velocity
    )
    loop_graph_offset = (
        module.dual_dot(loop_graph_displacement, loop_graph_displacement)
        - loop_graph_target.radius * loop_graph_target.radius
    )
    loop_graph_bad_discriminant = (
        loop_graph_linear * loop_graph_linear - loop_graph_offset
    )
    if not loop_graph_bad_discriminant.value < module.arb("-0.21"):
        raise RuntimeError(
            "narrow loop-Perron graph crossing may hit collision 74: "
            f"{loop_graph_bad_discriminant.value}"
        )

    print("COMMON_GRAY_PERRON_CHART: CERTIFIED")
    print(f"  qnl_fixed_point=(0,0)")
    print(f"  shadow_fixed_point=({a_star},{a_star})")
    print(f"  common_center=({common_center},{common_center})")
    print(f"  common_half_width=({common_radius},{common_radius})")
    print(f"  common_coordinate_interval=({common_lower},{common_upper})")
    print(f"  minimum_any_common_half_width={minimum_common_half_width}")
    print(f"  loop_minus_qnl_slope={slope_difference}")
    print(
        "  loop_stable_axis_slope_in_qnl_chart="
        f"{loop_stable_tilt_in_qnl_chart}"
    )
    print(f"  D_loop_in_qnl_chart={loop_in_qnl_chart}")
    print(f"  loop_common_vertical_shear={common_vertical_shear}")
    print("SHORT_QNL_COMMON_RECTANGLE_FULL_CROSS: CERTIFIED")
    print(f"  qnl_source_u_interval=({q_left},{q_right})")
    print(f"  qnl_source_v_interval={common_y_box}")
    print(f"  qnl_left_face_image={q_left_face}")
    print(f"  qnl_right_face_image={q_right_face}")
    print(f"  qnl_full_stable_image={q_stable_image}")
    print(
        "  qnl_full_stable_image_bounds="
        f"({q_stable_image.lower()},{q_stable_image.upper()})"
    )
    print(f"  qnl_derivative_box={module.arb_mat(derivative)}")
    print(f"  qnl_unstable_cone_image_slope={unstable_image_slope}")
    print(f"  qnl_stable_inverse_cone_image_slope={stable_inverse_image_slope}")
    for name, value in q_physical.items():
        print(f"  qnl_minimum_{name}={value}")
    print("CANDIDATE_SOURCE_STRIPS_DISJOINT: CERTIFIED")
    print(f"  loop_candidate_u_interval=({loop_left},{loop_right})")
    print(f"  qnl_to_loop_u_gap={strip_gap}")
    print("MIXED_CORNER_IN_EVERY_AXIS_ALIGNED_COMMON_VERTICAL_STRIP: CERTIFIED")
    print(f"  mixed_corner=(u,v)=({a_star},0)")
    print("MIXED_CORNER_FIRST_69_COLLISIONS: CERTIFIED")
    for name, value in prefix.minima.items():
        print(f"  prefix_minimum_{name}={value}")
    print("MIXED_CORNER_INTENDED_COLLISION_70: IMPOSSIBLE")
    print(f"  intended_target={next_key}")
    print(f"  intended_discriminant={bad_discriminant.value}")
    print("COMMON_CHART_LOOP_LINEAR_VERTICAL_SHEAR_OBSTRUCTION: CERTIFIED")
    print("LOOP_PERRON_MIXED_CORNER_FIRST_73_COLLISIONS: CERTIFIED")
    print("LOOP_PERRON_MIXED_CORNER_INTENDED_COLLISION_74: IMPOSSIBLE")
    print(f"  intended_target={loop_next_key}")
    print(f"  intended_discriminant={loop_bad_discriminant.value}")
    print("NARROW_CONE_FULL_HEIGHT_PLAQUE_CLASS: RULED_OUT")
    print(f"  lipschitz_bound={plaque_lipschitz}")
    print(f"  forced_v0_crossing_u={plaque_crossing_u}")
    print(
        "  qnl_perron_crossing_collision_70_discriminant="
        f"{qnl_graph_bad_discriminant.value}"
    )
    print(
        "  loop_perron_crossing_collision_74_discriminant="
        f"{loop_graph_bad_discriminant.value}"
    )
    print("QNL_PERRON_FIXED_96_WORD_FULL_HEIGHT_BRANCH: RULED_OUT")
    print("LOOP_PERRON_FIXED_96_WORD_FULL_HEIGHT_BRANCH: RULED_OUT")
    print("AUDITED_AFFINE_TWO_BRANCH_COMMON_RECTANGLE_ROUTE: RULED_OUT")
    print("ARBITRARY_AFFINE_COORDINATE_TWO_BRANCH_HORSESHOE: NOT_CERTIFIED")
    print("CURVILINEAR_STABLE_SATURATED_TWO_BRANCH_HORSESHOE: NOT_CERTIFIED")
    print("  missing=stable-plaque continuation across |delta v|>=8.29e-15")
    print("FULL_MASS_COUNTABLE_RETURN_PARTITION: NOT_CERTIFIED")
    print("PHYSICAL_GATE2: NOT_CERTIFIED")
    return 0


def main() -> int:
    try:
        return certify()
    except Exception as exc:
        print(f"GATE2_TWO_BRANCH_COMMON_RECTANGLE: FAILED: {exc}")
        print("SHORT_QNL_COMMON_RECTANGLE_FULL_CROSS: NOT_CERTIFIED")
        print("AUDITED_AFFINE_TWO_BRANCH_COMMON_RECTANGLE_ROUTE: NOT_CERTIFIED")
        print("CURVILINEAR_STABLE_SATURATED_TWO_BRANCH_HORSESHOE: NOT_CERTIFIED")
        print("PHYSICAL_GATE2: NOT_CERTIFIED")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
