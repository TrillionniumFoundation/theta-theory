#!/usr/bin/env python3
"""Validated continuation of the actual 96-word stable plaque to v=0.

The local unstable plaque of the reversible 96-collision fixed point is
continued for two returns with collisionwise Taylor rectangles.  Reflection
then gives the actual stable plaque at the common-chart face v=0.  A nonzero
96-word strip about that crossing is proved physical and full-crossing into
the common rectangle.  Stable saturation of that strip and a full-mass
quotient remain deliberately fail-closed.

Dependency: python-flint == 0.9.0.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
CLOSED_CERT = HERE / "cm2_gate1_closed_shadow_twisting_cert.py"
TANGENT_CERT = HERE / "cm2_gate1_tangent_line_matching_cert.py"
FULL_CERT = HERE / "cm2_gate1_full_cross_transport_cert.py"
PARENT_CERT = HERE / "cm2_gate1_true_graph_krawczyk_cert.py"
QNL_CERT = HERE / "cm2_gate1_qnl_unstable_graph_cert.py"
CONNECTOR_CERT = HERE / "cm2_gate1_connector_stable_graph_cert.py"
LOCAL_RETURN_CERT = HERE / "cm2_gate2_closed_loop_local_return_cert.py"

PRECISION_BITS = 2400
REFINED_ROOT_RADIUS = "1e-600"
GRAPH_PARAMETER_CENTER = (
    "7.2136102973143465356175083889981200377956881830964517688203040040451915205048947005376103562358475653706889750159720702836031830000656697779798267657432204458199759971413302744165540666379420957685679303124564369568303633014661148496770295080272342886654388070806157503984758452737843665397334392149556600331584749178732074967088370850810776188143587879795737774738707910576145780302068480236503373280406061552372590295521672891018259015809537279913689710167903921565089960849899198885526564816968381470815726403434102569581520990032435345850872257630964153438738146860429044078475946811540013043980625649076110843659201e-121"
)
GRAPH_PARAMETER_RADIUS = "1e-250"
LOCAL_UNSTABLE_GRAPH_SLOPE = "1e-40"
COMMON_RADIUS = "4.2e-15"
SECOND_SOURCE_U_RADIUS = "8e-68"
SECOND_SOURCE_V_RADIUS = "1e-80"
SECOND_SOURCE_CONE = "1e-20"


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def symmetric_ball(module, radius):
    radius = abs(radius).abs_upper()
    text = (module.arb(4) * radius).str(620, radius=False, more=True)
    ball = module.arb(0, text)
    if not ball.contains(radius) or not ball.contains(-radius):
        raise RuntimeError("failed to construct symmetric ball")
    return ball


def decimal_center(module, value):
    center = module.arb(value.str(620, radius=False, more=True))
    return center, abs(value - center)


def certify() -> int:
    closed = load(CLOSED_CERT, "cm2_gate2_plaque_closed")
    tangent = load(TANGENT_CERT, "cm2_gate2_plaque_tangent")
    full = load(FULL_CERT, "cm2_gate2_plaque_full")
    parent = load(PARENT_CERT, "cm2_gate2_plaque_parent")
    qnl = load(QNL_CERT, "cm2_gate2_plaque_qnl")
    connector = load(CONNECTOR_CERT, "cm2_gate2_plaque_connector")
    local = load(LOCAL_RETURN_CERT, "cm2_gate2_plaque_local")

    module = tangent.load_frozen_certificate()
    module.ctx.prec = PRECISION_BITS
    closed.refresh_exact_geometry(module)
    q_word = tangent.QNL_FORWARD_WORD
    b_word = tangent.CONNECTOR_REVERSE_FORWARD_WORD
    half_word = q_word * 2 + b_word * 2
    full_word = q_word * 2 + b_word * 4 + q_word * 2

    # Refine the same reversible root, then validate an interval-Newton box.
    root_center = module.arb(closed.SHADOW_A_CENTER)
    for _ in range(2):
        shot = closed.propagate_symmetric(tangent, module, root_center, half_word)
        root_center = module.arb(
            (
                root_center
                - shot.momentum.value / shot.momentum.derivative[0]
            ).str(680, radius=False, more=True)
        )
    root_box = module.arb(
        root_center.str(680, radius=False, more=True), REFINED_ROOT_RADIUS
    )
    center_shot = closed.propagate_symmetric(
        tangent, module, root_center, half_word
    )
    box_shot = closed.propagate_symmetric(tangent, module, root_box, half_word)
    newton = (
        root_center
        - center_shot.momentum.value / box_shot.momentum.derivative[0]
    )
    if not root_box.contains_interior(newton):
        raise RuntimeError("refined reversible-root interval Newton failed")

    theta_star = module.arb.pi() / 4 + 2 * root_box / module.R_GRAY
    half_matrix, _, _ = closed.symplectic_segment_matrix(
        tangent, module, theta_star, module.arb(0), half_word
    )
    aa, bb = half_matrix[0, 0], half_matrix[0, 1]
    cc, dd = half_matrix[1, 0], half_matrix[1, 1]
    loop_a = aa * dd + bb * cc
    loop_b = 2 * bb * dd
    loop_c = 2 * aa * cc
    loop_slope = (loop_c / loop_b).sqrt()
    expansion = loop_a + loop_b * loop_slope

    if local.UNSTABLE_CONE_SLOPE != LOCAL_UNSTABLE_GRAPH_SLOPE:
        raise RuntimeError("local unstable-plaque cone constant changed")
    graph_center = module.arb(GRAPH_PARAMETER_CENTER)
    graph_radius = module.arb(GRAPH_PARAMETER_RADIUS)
    graph_height = module.arb(LOCAL_UNSTABLE_GRAPH_SLOPE) * (
        abs(graph_center) + graph_radius
    )
    if not abs(graph_center) + graph_radius < module.arb(
        local.SOURCE_UNSTABLE_RADIUS
    ):
        raise RuntimeError("continuation seed leaves certified local plaque")

    def direct_loop(center_u, center_v):
        u = module.Dual(center_u, dimension=0)
        v = module.Dual(center_v, dimension=0)
        replay = tangent.propagate(
            module,
            "G",
            module.Dual(theta_star, dimension=0)
            + (u + v) / module.R_GRAY,
            loop_slope * (u - v),
            full_word,
        )
        ds = module.R_GRAY * (
            replay.theta - module.Dual(theta_star, dimension=0)
        )
        return (
            ((ds + replay.momentum / loop_slope) / 2).value,
            ((ds - replay.momentum / loop_slope) / 2).value,
            replay,
        )

    def map_box(center_u, radius_u, center_v, radius_v):
        base_angle = theta_star + 2 * center_v / module.R_GRAY
        replay = full.replay_rectangle(
            parent,
            qnl,
            connector,
            tangent,
            module,
            parameter_center=center_u - center_v,
            parameter_radius=radius_u,
            transverse_radius=radius_v,
            base_angle=base_angle,
            slope=loop_slope,
            word=full_word,
        )
        model = full.to_connector_eigen(
            module, replay, theta_star, loop_slope
        )
        tight_u, tight_v, point = direct_loop(center_u, center_v)
        for raw, tight in zip(model.center, (tight_u, tight_v)):
            if not (raw - tight).contains(0):
                raise RuntimeError("tight point replay disagrees with Taylor center")
        radii = [
            abs(model.linear[index][0]) * radius_u
            + abs(model.linear[index][1]) * radius_v
            + model.remainder[index]
            for index in range(2)
        ]
        return [tight_u, tight_v], radii, model, point

    def rebox(centers, radii):
        exact = []
        enlarged = []
        for center, radius in zip(centers, radii):
            point, rounding = decimal_center(module, center)
            exact.append(point)
            enlarged.append(radius + rounding)
        return exact, enlarged

    def two_returns(center_u, radius_u):
        first = map_box(
            center_u,
            radius_u,
            module.arb(0),
            graph_height,
        )
        intermediate_center, intermediate_radius = rebox(first[0], first[1])
        second = map_box(
            intermediate_center[0],
            intermediate_radius[0],
            intermediate_center[1],
            intermediate_radius[1],
        )
        return first, second, intermediate_center, intermediate_radius

    minus = two_returns(graph_center - graph_radius, module.arb(0))
    plus = two_returns(graph_center + graph_radius, module.arb(0))
    whole = two_returns(graph_center, graph_radius)
    minus_face = minus[1][0][0] + root_box + symmetric_ball(
        module, minus[1][1][0]
    )
    plus_face = plus[1][0][0] + root_box + symmetric_ball(
        module, plus[1][1][0]
    )
    whole_u = whole[1][0][0] + root_box + symmetric_ball(
        module, whole[1][1][0]
    )
    whole_v = whole[1][0][1] + symmetric_ball(module, whole[1][1][1])
    if not minus_face < 0 or not plus_face > 0 or not whole_u.contains(0):
        raise RuntimeError("two-return plaque face continuation failed")

    # By invariance and IVT, F^2(W^u_loc) meets global u=0.  Time reversal
    # swaps loop Perron coordinates, producing W^s(z_*) at global v=0.
    crossing_correction, crossing_rounding = decimal_center(module, whole[1][0][1])
    crossing_uncertainty = whole[1][1][1] + crossing_rounding
    crossing_center = module.arb(
        root_center.str(680, radius=False, more=True)
    ) + crossing_correction
    source_u_radius = module.arb(SECOND_SOURCE_U_RADIUS)
    source_v_radius = module.arb(SECOND_SOURCE_V_RADIUS)
    if not crossing_uncertainty + abs(root_box - root_center) < source_u_radius:
        raise RuntimeError("second strip does not contain actual stable crossing")

    physical = full.replay_rectangle(
        parent,
        qnl,
        connector,
        tangent,
        module,
        parameter_center=crossing_center,
        parameter_radius=source_u_radius,
        transverse_radius=source_v_radius,
        base_angle=module.arb.pi() / 4,
        slope=loop_slope,
        word=full_word,
    )
    target = full.to_connector_eigen(
        module, physical, module.arb.pi() / 4, loop_slope
    )
    direct_source_u = root_box + whole_v
    source_theta = module.Dual(
        module.arb.pi() / 4 + direct_source_u / module.R_GRAY,
        dimension=0,
    )
    source_momentum = module.Dual(loop_slope * direct_source_u, dimension=0)
    crossing_replay = tangent.propagate(
        module, "G", source_theta, source_momentum, full_word
    )

    common_center = root_box / 2
    common_radius = module.arb(COMMON_RADIUS)
    common_lower = common_center - common_radius
    common_upper = common_center + common_radius
    face_error = (
        abs(target.linear[0][1]) * source_v_radius
        + target.remainder[0]
    )
    negative_face = (
        target.center[0]
        - target.linear[0][0] * source_u_radius
        + symmetric_ball(module, face_error)
    )
    positive_face = (
        target.center[0]
        + target.linear[0][0] * source_u_radius
        + symmetric_ball(module, face_error)
    )
    stable_radius = (
        abs(target.linear[1][0]) * source_u_radius
        + abs(target.linear[1][1]) * source_v_radius
        + target.remainder[1]
    )
    stable_image = target.center[1] + symmetric_ball(module, stable_radius)
    if not negative_face < common_lower:
        raise RuntimeError("second branch negative face does not exit")
    if not positive_face > common_upper:
        raise RuntimeError("second branch positive face does not exit")
    if not stable_image > common_lower or not stable_image < common_upper:
        raise RuntimeError("second branch stable image leaves common rectangle")

    thresholds = {
        "flight": module.arb("0.18"),
        "discriminant": module.arb("0.01"),
        "incidence": module.arb("0.63"),
        "clearance": module.arb("0.22"),
    }
    for name, threshold in thresholds.items():
        if not physical.minima[name] > threshold:
            raise RuntimeError(f"second branch physical margin {name} failed")

    derivative = target.derivative_box(module)
    a11, a12 = derivative[0]
    a21, a22 = derivative[1]
    cone = module.arb(SECOND_SOURCE_CONE)
    unstable_ratio = (
        abs(a21).upper() + abs(a22).upper() * cone
    ) / (a11.lower() - abs(a12).upper() * cone)
    stable_inverse_ratio = (
        abs(a22).upper() * cone + abs(a12).upper()
    ) / (a11.lower() - abs(a21).upper() * cone)
    if not unstable_ratio < cone or not stable_inverse_ratio < cone:
        raise RuntimeError("second branch cone certification failed")

    qnl_right = module.arb("1e-17")
    if not qnl_right - (crossing_center + source_u_radius) > module.arb("7e-15"):
        raise RuntimeError("QNL and actual-plaque strips are not disjoint")

    print("REFINED_2400_BIT_REVERSIBLE_ROOT: CERTIFIED")
    print(f"  refined_root={root_box}")
    print(f"  interval_newton_image={newton}")
    print("TWO_RETURN_ACTUAL_UNSTABLE_PLAQUE_CONTINUATION: CERTIFIED")
    print(f"  local_graph_parameter_center={graph_center}")
    print(f"  local_graph_parameter_radius={graph_radius}")
    print(f"  local_graph_ordinate_bound={graph_height}")
    print(f"  first_rebox_center={whole[2]}")
    print(f"  first_rebox_radius={whole[3]}")
    print(f"  minus_global_u_face={minus_face}")
    print(f"  plus_global_u_face={plus_face}")
    print(f"  whole_global_u_image={whole_u}")
    print(f"  whole_local_v_image={whole_v}")
    print("ACTUAL_STABLE_PLAQUE_V0_CROSSING: CERTIFIED")
    print(f"  crossing_u_center={crossing_center}")
    print(f"  crossing_u_uncertainty={crossing_uncertainty}")
    print("ACTUAL_CROSSING_96_FIRST_HITS: CERTIFIED")
    for name, value in crossing_replay.minima.items():
        print(f"  crossing_minimum_{name}={value}")
    print("POSITIVE_WIDTH_ACTUAL_PLAQUE_96_WORD_STRIP: CERTIFIED")
    print(f"  source_half_widths=({source_u_radius},{source_v_radius})")
    print(f"  negative_face_image={negative_face}")
    print(f"  positive_face_image={positive_face}")
    print(f"  stable_image={stable_image}")
    for name, value in physical.minima.items():
        print(f"  strip_minimum_{name}={value}")
    print("ACTUAL_PLAQUE_SECOND_BRANCH_CONES: CERTIFIED")
    print(f"  derivative_box={module.arb_mat(derivative)}")
    print(f"  cone_slope={cone}")
    print(f"  unstable_image_slope={unstable_ratio}")
    print(f"  stable_inverse_image_slope={stable_inverse_ratio}")
    print("TWO_LOCAL_PHYSICAL_BRANCHES_IN_COMMON_RECTANGLE: CERTIFIED")
    print("SECOND_BRANCH_STABLE_SATURATION: NOT_CERTIFIED")
    print("FULL_MASS_COUNTABLE_RETURN_PARTITION: NOT_CERTIFIED")
    print("PHYSICAL_GATE2: NOT_CERTIFIED")
    return 0


def main() -> int:
    try:
        return certify()
    except Exception as exc:
        print(f"GATE2_ACTUAL_PLAQUE_CONTINUATION: FAILED: {exc}")
        print("ACTUAL_STABLE_PLAQUE_V0_CROSSING: NOT_CERTIFIED")
        print("POSITIVE_WIDTH_ACTUAL_PLAQUE_96_WORD_STRIP: NOT_CERTIFIED")
        print("PHYSICAL_GATE2: NOT_CERTIFIED")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
