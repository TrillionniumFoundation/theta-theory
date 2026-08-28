#!/usr/bin/env python3
"""CM2 Gate 1: correlated full-cross and transition-transport certificate.

This file upgrades the certified true-graph heteroclinic root in two ways.

First, the unknown invariant-graph ordinate is retained as a second Taylor
variable.  This preserves the cancellation between ``theta`` and ``p`` that
was lost when the ordinate was put into two unrelated scalar remainders.  A
new Krawczyk audit therefore localises the same actual graph intersection much
more sharply.

Second, a genuine two-dimensional QNL eigen-rectangle is propagated through
the complete 24-collision transition word.  Two parameter faces exit opposite
connector unstable faces and the entire transverse graph tube lies strictly
between the two connector stable faces.  All comparisons use Arb balls and
the same Taylor tubes are subjected to a complete first-hit audit.

The derivative of the actual transition is also enclosed at the graph root.
Exact preservation of ``ds wedge dp`` supplies the fourth matrix entry without
destroying its correlation.  This is *not* silently promoted to transported
twisting: a finite closed dwell/shadowing loop based at the common vertex has
not been certified, so the final twisting label remains fail-closed.

Dependency: python-flint == 0.9.0.
"""

from __future__ import annotations

import importlib.util
import sys
from dataclasses import dataclass
from pathlib import Path


HERE = Path(__file__).resolve().parent
TRUE_GRAPH_CERT = HERE / "cm2_gate1_true_graph_krawczyk_cert.py"
QNL_CERT = HERE / "cm2_gate1_qnl_unstable_graph_cert.py"
CONNECTOR_CERT = HERE / "cm2_gate1_connector_stable_graph_cert.py"
TANGENT_CERT = HERE / "cm2_gate1_tangent_line_matching_cert.py"

PRECISION_BITS = 500

# Correlated true-root box.  The outward Arb boxes constructed below are
# wider; the derivative model is deliberately evaluated on twice that width.
ROOT_T_RADIUS = "1e-27"
ROOT_U_RADIUS = "1e-30"
ROOT_T_MODEL_RADIUS = "8e-27"
ROOT_U_MODEL_RADIUS = "8e-30"

# Independent Poincare--Miranda face box for C F(t,u).
FACE_T_RADIUS = "1e-20"
FACE_U_RADIUS = "1e-23"

# Explicit QNL source and connector target rectangles in eigen-coordinates.
SOURCE_T_RADIUS = "1e-20"
SOURCE_TRANSVERSE_RADIUS = "2.1e-18"
TARGET_UNSTABLE_RADIUS = "1e-8"
TARGET_STABLE_RADIUS = "1e-14"


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def mat_mul(module, left, right):
    return [
        [
            sum(
                (left[i][k] * right[k][j] for k in range(2)),
                module.arb(0),
            )
            for j in range(2)
        ]
        for i in range(2)
    ]


def mat_vec(module, matrix, vector):
    return [
        sum((matrix[i][j] * vector[j] for j in range(2)), module.arb(0))
        for i in range(2)
    ]


def abs_matrix(matrix):
    return [[abs(entry) for entry in row] for row in matrix]


def update_minimum(current, value):
    return value if current is None else current.min(value)


@dataclass
class TaylorRectangle:
    """Affine two-parameter Taylor model plus a rigorous scalar remainder."""

    center: list[object]
    linear: list[list[object]]
    remainder: list[object]
    derivative_center: list[list[object]]
    derivative_remainder: list[list[object]]
    radii: list[object]
    minima: dict[str, object]
    maximum_state_radius: object
    cumulative_lifts: tuple[tuple[int, int], ...]

    def value_box(self, module):
        values = []
        for output in range(2):
            radius = self.remainder[output] + sum(
                (
                    abs(self.linear[output][parameter]) * self.radii[parameter]
                    for parameter in range(2)
                ),
                module.arb(0),
            )
            values.append(
                self.center[output]
                + self._symmetric_ball(module, radius)
            )
        return values

    def derivative_box(self, module):
        return [
            [
                self.derivative_center[output][parameter]
                + self._symmetric_ball(
                    module, self.derivative_remainder[output][parameter]
                )
                for parameter in range(2)
            ]
            for output in range(2)
        ]

    def face_box(self, module, output: int, parameter: int, sign: int):
        if sign not in (-1, 1):
            raise ValueError("face sign must be +/-1")
        other = 1 - parameter
        radius = (
            abs(self.linear[output][other]) * self.radii[other]
            + self.remainder[output]
        )
        return (
            self.center[output]
            + sign * self.linear[output][parameter] * self.radii[parameter]
            + self._symmetric_ball(module, radius)
        )

    @staticmethod
    def _symmetric_ball(module, radius):
        radius = radius.abs_upper()
        text = (4 * radius).str(130, radius=False, more=True)
        ball = module.arb(0, text)
        if not ball.contains(radius) or not ball.contains(-radius):
            raise RuntimeError(f"failed to build symmetric ball for {radius}")
        return ball


def symmetric_ball(parent, module, radius):
    del parent
    radius = radius.abs_upper()
    text = (4 * radius).str(130, radius=False, more=True)
    ball = module.arb(0, text)
    if not ball.contains(radius) or not ball.contains(-radius):
        raise RuntimeError(f"failed to build symmetric ball for {radius}")
    return ball


def replay_rectangle(
    parent,
    qnl,
    connector,
    tangent,
    module,
    *,
    parameter_center,
    parameter_radius,
    transverse_radius,
    base_angle,
    slope,
    word,
    terminal_momentum_sign=1,
):
    """Propagate a correlated eigen-coordinate rectangle collision by collision."""

    radii = [abs(parameter_radius), abs(transverse_radius)]
    center = [
        base_angle + parameter_center / module.R_GRAY,
        slope * parameter_center,
    ]
    # Eigen coordinates (a,b) satisfy s=a+b, p=k(a-b).
    linear = [[1 / module.R_GRAY, 1 / module.R_GRAY], [slope, -slope]]
    remainder = [module.arb(0), module.arb(0)]
    derivative_center = [row[:] for row in linear]
    derivative_remainder = [
        [module.arb(0), module.arb(0)],
        [module.arb(0), module.arb(0)],
    ]
    minima = {
        "flight": None,
        "discriminant": None,
        "incidence": None,
        "clearance": None,
    }
    maximum_state_radius = module.arb(0)
    current_kind = "G"
    cumulative_i = 0
    cumulative_j = 0
    cumulative_lifts = [(0, 0)]

    for target_key in word:
        total_radius = [
            remainder[output]
            + sum(
                (
                    abs(linear[output][parameter]) * radii[parameter]
                    for parameter in range(2)
                ),
                module.arb(0),
            )
            for output in range(2)
        ]
        maximum_state_radius = (
            maximum_state_radius.max(total_radius[0]).max(total_radius[1])
        )
        state_boxes = [
            center[output] + symmetric_ball(parent, module, total_radius[output])
            for output in range(2)
        ]
        source = module.obstacle(current_kind, 0, 0)
        target = module.obstacle(*target_key)
        box_step = parent.tm_collision_step(
            qnl, connector, module, source, target, state_boxes[0], state_boxes[1]
        )
        center_step = parent.tm_collision_step(
            qnl, connector, module, source, target, center[0], center[1]
        )

        global_x = box_step.impact[0] + cumulative_i
        global_y = box_step.impact[1] + cumulative_j
        if not (global_x > 0 and global_x < 1 and global_y > 0 and global_y < 1):
            raise RuntimeError(
                "Taylor rectangle may cross a transparent wall: "
                f"({global_x},{global_y})"
            )

        box_jacobian = [box_step.angle.gradient, box_step.momentum.gradient]
        center_jacobian = [
            center_step.angle.gradient,
            center_step.momentum.gradient,
        ]
        hessians = [box_step.angle.hessian, box_step.momentum.hessian]

        new_center = [center_step.angle.value, center_step.momentum.value]
        new_linear = mat_mul(module, center_jacobian, linear)
        new_remainder = []
        derivative_variation = [
            [module.arb(0), module.arb(0)],
            [module.arb(0), module.arb(0)],
        ]
        for output in range(2):
            propagated = sum(
                (
                    abs(box_jacobian[output][state]) * remainder[state]
                    for state in range(2)
                ),
                module.arb(0),
            )
            quadratic = sum(
                (
                    abs(hessians[output][left][right])
                    * total_radius[left]
                    * total_radius[right]
                    for left in range(2)
                    for right in range(2)
                ),
                module.arb(0),
            ) / 2
            new_remainder.append(propagated + quadratic)
            for state in range(2):
                derivative_variation[output][state] = sum(
                    (
                        abs(hessians[output][state][other]) * total_radius[other]
                        for other in range(2)
                    ),
                    module.arb(0),
                )

        new_derivative_center = mat_mul(
            module, center_jacobian, derivative_center
        )
        new_derivative_remainder = [
            [module.arb(0), module.arb(0)],
            [module.arb(0), module.arb(0)],
        ]
        for output in range(2):
            for parameter in range(2):
                inherited = sum(
                    (
                        abs(box_jacobian[output][state])
                        * derivative_remainder[state][parameter]
                        for state in range(2)
                    ),
                    module.arb(0),
                )
                varying = sum(
                    (
                        derivative_variation[output][state]
                        * abs(derivative_center[state][parameter])
                        for state in range(2)
                    ),
                    module.arb(0),
                )
                new_derivative_remainder[output][parameter] = inherited + varying

        for name, value in (
            ("flight", box_step.flight),
            ("discriminant", box_step.discriminant),
            ("incidence", box_step.incidence),
            ("clearance", box_step.clearance),
        ):
            minima[name] = update_minimum(minima[name], value)

        center = new_center
        linear = new_linear
        remainder = new_remainder
        derivative_center = new_derivative_center
        derivative_remainder = new_derivative_remainder
        cumulative_i += target_key[1]
        cumulative_j += target_key[2]
        cumulative_lifts.append((cumulative_i, cumulative_j))
        current_kind = target_key[0]

    if terminal_momentum_sign == -1:
        center[1] = -center[1]
        linear[1] = [-entry for entry in linear[1]]
        derivative_center[1] = [-entry for entry in derivative_center[1]]
    elif terminal_momentum_sign != 1:
        raise ValueError("terminal_momentum_sign must be +/-1")

    return TaylorRectangle(
        center,
        linear,
        remainder,
        derivative_center,
        derivative_remainder,
        radii,
        minima,
        maximum_state_radius,
        tuple(cumulative_lifts),
    )


def to_connector_eigen(module, replay, base_angle, slope):
    transform = [
        [module.R_GRAY / 2, 1 / (2 * slope)],
        [module.R_GRAY / 2, -1 / (2 * slope)],
    ]
    center = mat_vec(
        module, transform, [replay.center[0] - base_angle, replay.center[1]]
    )
    linear = mat_mul(module, transform, replay.linear)
    remainder = mat_vec(module, abs_matrix(transform), replay.remainder)
    derivative_center = mat_mul(module, transform, replay.derivative_center)
    derivative_remainder = mat_mul(
        module, abs_matrix(transform), replay.derivative_remainder
    )
    return TaylorRectangle(
        center,
        linear,
        remainder,
        derivative_center,
        derivative_remainder,
        replay.radii,
        replay.minima,
        replay.maximum_state_radius,
        replay.cumulative_lifts,
    )


def graph_matching_data(
    parent,
    qnl,
    connector,
    tangent,
    module,
    root,
    slope_a,
    slope_b,
    t_center,
    u_center,
    t_radius,
    u_radius,
):
    qnl_ordinate = module.arb(parent.QNL_GRAPH_QUADRATIC) * (
        abs(t_center) + abs(t_radius)
    ) ** 2
    connector_ordinate = module.arb(parent.CONNECTOR_GRAPH_QUADRATIC) * (
        abs(u_center) + abs(u_radius)
    ) ** 2
    left = replay_rectangle(
        parent,
        qnl,
        connector,
        tangent,
        module,
        parameter_center=t_center,
        parameter_radius=t_radius,
        transverse_radius=qnl_ordinate,
        base_angle=module.arb.pi() / 4,
        slope=slope_a,
        word=tangent.QNL_FORWARD_WORD,
    )
    right = replay_rectangle(
        parent,
        qnl,
        connector,
        tangent,
        module,
        parameter_center=u_center,
        parameter_radius=u_radius,
        transverse_radius=connector_ordinate,
        base_angle=root.boxes[0],
        slope=slope_b,
        word=tangent.CONNECTOR_REVERSE_FORWARD_WORD,
        terminal_momentum_sign=-1,
    )
    left_value = left.value_box(module)
    right_value = right.value_box(module)
    values = [left_value[index] - right_value[index] for index in range(2)]
    left_derivative = left.derivative_box(module)
    right_derivative = right.derivative_box(module)
    h_a_prime = symmetric_ball(
        parent, module, module.arb(parent.QNL_GRAPH_LIPSCHITZ)
    )
    h_b_prime = symmetric_ball(
        parent, module, module.arb(parent.CONNECTOR_GRAPH_LIPSCHITZ)
    )
    derivative_t = [
        left_derivative[output][0]
        + left_derivative[output][1] * h_a_prime
        for output in range(2)
    ]
    derivative_u = [
        right_derivative[output][0]
        + right_derivative[output][1] * h_b_prime
        for output in range(2)
    ]
    jacobian = [
        [derivative_t[0], -derivative_u[0]],
        [derivative_t[1], -derivative_u[1]],
    ]
    return values, jacobian, left, right, qnl_ordinate, connector_ordinate


def certify_correlated_root_and_faces(
    parent, qnl, connector, tangent, module, root, slope_a, slope_b, t_center, u_center
):
    center_values, center_jacobian, _, _, qnl_ord, connector_ord = (
        graph_matching_data(
            parent,
            qnl,
            connector,
            tangent,
            module,
            root,
            slope_a,
            slope_b,
            t_center,
            u_center,
            module.arb(0),
            module.arb(0),
        )
    )
    preconditioner = parent.rational_preconditioner(module, center_jacobian)
    identity = module.arb_mat([[1, 0], [0, 1]])

    t_delta = symmetric_ball(parent, module, module.arb(ROOT_T_RADIUS))
    u_delta = symmetric_ball(parent, module, module.arb(ROOT_U_RADIUS))
    model_t = module.arb(ROOT_T_MODEL_RADIUS)
    model_u = module.arb(ROOT_U_MODEL_RADIUS)
    if not abs(t_delta) < model_t or not abs(u_delta) < model_u:
        raise RuntimeError("root derivative models do not cover outward Arb boxes")
    _, box_jacobian, left, right, _, _ = graph_matching_data(
        parent,
        qnl,
        connector,
        tangent,
        module,
        root,
        slope_a,
        slope_b,
        t_center,
        u_center,
        model_t,
        model_u,
    )
    center_vector = module.arb_mat([[t_center], [u_center]])
    residual_vector = module.arb_mat([[center_values[0]], [center_values[1]]])
    centered_box = module.arb_mat([[t_delta], [u_delta]])
    krawczyk = (
        center_vector
        - preconditioner * residual_vector
        + (identity - preconditioner * module.arb_mat(box_jacobian))
        * centered_box
    )
    t_box = t_center + t_delta
    u_box = u_center + u_delta
    determinant = module.arb_mat(box_jacobian).det()
    if determinant.contains(0):
        raise RuntimeError(f"correlated matching determinant may vanish: {determinant}")
    if not t_box.contains_interior(krawczyk[0, 0]):
        raise RuntimeError(f"correlated t Krawczyk inclusion fails: {krawczyk[0,0]}")
    if not u_box.contains_interior(krawczyk[1, 0]):
        raise RuntimeError(f"correlated u Krawczyk inclusion fails: {krawczyk[1,0]}")

    face_t = module.arb(FACE_T_RADIUS)
    face_u = module.arb(FACE_U_RADIUS)
    _, face_jacobian, _, _, _, _ = graph_matching_data(
        parent,
        qnl,
        connector,
        tangent,
        module,
        root,
        slope_a,
        slope_b,
        t_center,
        u_center,
        face_t,
        face_u,
    )
    transformed_center = preconditioner * residual_vector
    transformed_jacobian = preconditioner * module.arb_mat(face_jacobian)
    t_minus = (
        transformed_center[0, 0]
        - transformed_jacobian[0, 0] * face_t
        + symmetric_ball(
            parent, module, abs(transformed_jacobian[0, 1]) * face_u
        )
    )
    t_plus = (
        transformed_center[0, 0]
        + transformed_jacobian[0, 0] * face_t
        + symmetric_ball(
            parent, module, abs(transformed_jacobian[0, 1]) * face_u
        )
    )
    u_minus = (
        transformed_center[1, 0]
        - transformed_jacobian[1, 1] * face_u
        + symmetric_ball(
            parent, module, abs(transformed_jacobian[1, 0]) * face_t
        )
    )
    u_plus = (
        transformed_center[1, 0]
        + transformed_jacobian[1, 1] * face_u
        + symmetric_ball(
            parent, module, abs(transformed_jacobian[1, 0]) * face_t
        )
    )
    if not t_minus < 0 or not t_plus > 0:
        raise RuntimeError(f"t face signs fail: minus={t_minus}, plus={t_plus}")
    if not u_minus < 0 or not u_plus > 0:
        raise RuntimeError(f"u face signs fail: minus={u_minus}, plus={u_plus}")

    print("CORRELATED_TRUE_GRAPH_KRAWCZYK: CERTIFIED")
    print(f"  t_box={t_box}")
    print(f"  u_box={u_box}")
    print(f"  center_graph_ordinate_radius_qnl={qnl_ord}")
    print(f"  center_graph_ordinate_radius_connector={connector_ord}")
    print(f"  center_residual={center_values}")
    print(f"  box_jacobian={module.arb_mat(box_jacobian)}")
    print(f"  determinant={determinant}")
    print(f"  krawczyk_image={krawczyk}")
    print("PRECONDITIONED_GRAPH_FACE_CROSSING: CERTIFIED")
    print(f"  transformed_jacobian={transformed_jacobian}")
    print(f"  t_minus_face={t_minus}")
    print(f"  t_plus_face={t_plus}")
    print(f"  u_minus_face={u_minus}")
    print(f"  u_plus_face={u_plus}")
    print(f"  qnl_maximum_state_radius={left.maximum_state_radius}")
    print(f"  connector_maximum_state_radius={right.maximum_state_radius}")
    return t_box, u_box, preconditioner


def certify_physical_full_cross(
    parent, qnl, connector, tangent, module, root, slope_a, slope_b, t_center, u_center
):
    source_t = module.arb(SOURCE_T_RADIUS)
    source_b = module.arb(SOURCE_TRANSVERSE_RADIUS)
    target_x = module.arb(TARGET_UNSTABLE_RADIUS)
    target_u = module.arb(TARGET_STABLE_RADIUS)

    graph_bound = module.arb(parent.QNL_GRAPH_QUADRATIC) * (
        abs(t_center) + source_t
    ) ** 2
    if not graph_bound < source_b:
        raise RuntimeError(
            f"source transverse tube misses QNL graph: {graph_bound} versus {source_b}"
        )
    target_graph_bound = module.arb(parent.CONNECTOR_GRAPH_QUADRATIC) * (
        abs(u_center) + target_u
    ) ** 2
    if not target_graph_bound < target_x:
        raise RuntimeError("target rectangle does not contain connector stable graph")
    if not abs(u_center) + target_u < module.arb(parent.CONNECTOR_GRAPH_RADIUS):
        raise RuntimeError("target stable faces leave connector graph domain")

    physical = replay_rectangle(
        parent,
        qnl,
        connector,
        tangent,
        module,
        parameter_center=t_center,
        parameter_radius=source_t,
        transverse_radius=source_b,
        base_angle=module.arb.pi() / 4,
        slope=slope_a,
        word=tangent.FULL_FORWARD_TRANSITION_WORD,
    )
    target = to_connector_eigen(module, physical, root.boxes[0], slope_b)

    exit_minus = target.face_box(module, 0, 0, -1)
    exit_plus = target.face_box(module, 0, 0, 1)
    stable_all = target.value_box(module)[1]
    transverse_minus = target.face_box(module, 1, 1, -1)
    transverse_plus = target.face_box(module, 1, 1, 1)
    lower_stable = u_center - target_u
    upper_stable = u_center + target_u

    if not exit_minus < -target_x:
        raise RuntimeError(f"negative parameter face does not exit: {exit_minus}")
    if not exit_plus > target_x:
        raise RuntimeError(f"positive parameter face does not exit: {exit_plus}")
    if not stable_all > lower_stable:
        raise RuntimeError(f"image may cross lower stable face: {stable_all}")
    if not stable_all < upper_stable:
        raise RuntimeError(f"image may cross upper stable face: {stable_all}")
    for label, face in (
        ("negative transverse", transverse_minus),
        ("positive transverse", transverse_plus),
    ):
        if not face > lower_stable or not face < upper_stable:
            raise RuntimeError(f"{label} graph-tube face loses entry: {face}")

    thresholds = {
        "flight": module.arb(1) / 10,
        "discriminant": module.arb(1) / 1000,
        "incidence": module.arb(1) / 2,
        "clearance": module.arb(1) / 10,
    }
    for name, threshold in thresholds.items():
        if not physical.minima[name] > threshold:
            raise RuntimeError(
                f"full-cross first-hit margin {name} fails: {physical.minima[name]}"
            )

    print("TRUE_GRAPH_TRANSITION_FULL_CROSS: CERTIFIED")
    print("FULL_CROSS_COMMON_VERTEX: CERTIFIED")
    print("  scope=actual directed 24-collision QNL-to-connector transition rectangle")
    print(f"  source_center=(t0,0)=({t_center},0)")
    print(f"  source_half_widths=(t,b)=({source_t},{source_b})")
    print(f"  target_center=(0,u0)=(0,{u_center})")
    print(f"  target_half_widths=(x,u)=({target_x},{target_u})")
    print(f"  qnl_graph_bound_on_source={graph_bound}")
    print(f"  connector_graph_bound_on_target={target_graph_bound}")
    print(f"  negative_parameter_exit={exit_minus}")
    print(f"  positive_parameter_exit={exit_plus}")
    print(f"  full_image_stable_coordinate={stable_all}")
    print(f"  negative_transverse_face_stable_coordinate={transverse_minus}")
    print(f"  positive_transverse_face_stable_coordinate={transverse_plus}")
    print(f"  stable_entry_interval=({lower_stable},{upper_stable})")
    print(f"  maximum_state_radius={physical.maximum_state_radius}")
    for name, value in physical.minima.items():
        print(f"  minimum_{name}={value}")
    print(f"  collision_count={len(tangent.FULL_FORWARD_TRANSITION_WORD)}")
    print(f"  word={tangent.FULL_FORWARD_TRANSITION_WORD}")
    print(f"  cumulative_lifts={physical.cumulative_lifts}")
    print("  finite_lattice_first_hit_exhaustion=[-3,3]^2")
    print("REVERSIBLE_OPPOSITE_TRANSITION_FULL_CROSS: CERTIFIED")
    print("  mechanism=I*T^24*I=T^-24; stable/unstable faces exchanged")
    return target


def certify_transition_transport(
    parent, qnl, connector, tangent, module, root, slope_a, slope_b, t_center
):
    # This box contains the sharper Krawczyk t-box and every admissible graph
    # ordinate at the actual source point.
    vertex_t_radius = module.arb(ROOT_T_MODEL_RADIUS)
    vertex_b_radius = module.arb(SOURCE_TRANSVERSE_RADIUS)
    physical = replay_rectangle(
        parent,
        qnl,
        connector,
        tangent,
        module,
        parameter_center=t_center,
        parameter_radius=vertex_t_radius,
        transverse_radius=vertex_b_radius,
        base_angle=module.arb.pi() / 4,
        slope=slope_a,
        word=tangent.FULL_FORWARD_TRANSITION_WORD,
    )
    target = to_connector_eigen(module, physical, root.boxes[0], slope_b)
    raw = target.derivative_box(module)
    a, b = raw[0]
    c = raw[1][0]
    exact_determinant = slope_a / slope_b
    if a.contains(0):
        raise RuntimeError(f"transport a-entry may vanish: {a}")
    # In (s,p), every regular billiard collision preserves ds wedge dp.
    # The eigen-coordinate changes have determinants -2*k_A and -2*k_B,
    # hence det D H_AB = k_A/k_B exactly.
    d = (exact_determinant + b * c) / a
    transport = module.arb_mat([[a, b], [c, d]])
    if not a > 0 or not b < 0 or not c < 0 or not d > 0:
        raise RuntimeError(f"transition derivative sign pattern fails: {transport}")

    inverse = module.arb_mat(
        [[d / exact_determinant, -b / exact_determinant],
         [-c / exact_determinant, a / exact_determinant]]
    )
    swap = module.arb_mat([[0, 1], [1, 0]])
    reversed_transport = swap * inverse * swap

    print("ACTUAL_VERTEX_TRANSITION_DERIVATIVE: CERTIFIED")
    print(f"  D_H_AB={transport}")
    print(f"  det_D_H_AB={exact_determinant} (exact symplectic coordinate ratio)")
    print(f"  raw_fourth_entry_diagnostic={raw[1][1]}")
    print(f"  symplectic_reconstructed_fourth_entry={d}")
    print("REVERSED_VERTEX_TRANSITION_DERIVATIVE: CERTIFIED")
    print(f"  D_H_BA_at_involuted_endpoints={reversed_transport}")
    print("  identity=D(I)_A * D(H_AB)^(-1) * D(I)_B")
    print("CLOSED_COMMON_VERTEX_LOOP_DERIVATIVE: NOT CERTIFIED")
    print("  missing=finite dwell/shadowing return joining the inbound stable endpoint")
    print("          to the outbound involuted endpoint on one closed symbolic orbit")
    print("TRANSPORTED_TWISTING: NOT CERTIFIED")
    print("  reason=J_B^n is based at the connector periodic point and cannot be")
    print("         multiplied into endpoint transports before that closed dwell is certified")


def certify():
    parent = load(TRUE_GRAPH_CERT, "cm2_gate1_full_cross_parent")
    qnl = load(QNL_CERT, "cm2_gate1_full_cross_qnl")
    connector = load(CONNECTOR_CERT, "cm2_gate1_full_cross_connector")
    tangent = load(TANGENT_CERT, "cm2_gate1_full_cross_tangent")
    module = tangent.load_frozen_certificate()
    module.ctx.prec = PRECISION_BITS
    root, slope_a, slope_b = tangent.setup_fixed_data(module)
    t_decimal, u_decimal = tangent.refine_center(module, root, slope_a, slope_b)
    t_center = module.arb(t_decimal)
    u_center = module.arb(u_decimal)

    expected = (
        (qnl.RADIUS, parent.QNL_GRAPH_RADIUS, "QNL graph radius"),
        (qnl.QUADRATIC_CONSTANT, parent.QNL_GRAPH_QUADRATIC, "QNL graph bound"),
        (qnl.LIPSCHITZ_CONSTANT, parent.QNL_GRAPH_LIPSCHITZ, "QNL derivative bound"),
        (connector.TARGET_RADIUS, parent.CONNECTOR_GRAPH_RADIUS, "connector radius"),
        (
            connector.QUADRATIC_CONSTANT,
            parent.CONNECTOR_GRAPH_QUADRATIC,
            "connector graph bound",
        ),
        (
            connector.LIPSCHITZ_CONSTANT,
            parent.CONNECTOR_GRAPH_LIPSCHITZ,
            "connector derivative bound",
        ),
    )
    for actual, frozen, label in expected:
        if actual != frozen:
            raise RuntimeError(f"{label} changed: {actual} != {frozen}")

    certify_correlated_root_and_faces(
        parent,
        qnl,
        connector,
        tangent,
        module,
        root,
        slope_a,
        slope_b,
        t_center,
        u_center,
    )
    certify_physical_full_cross(
        parent,
        qnl,
        connector,
        tangent,
        module,
        root,
        slope_a,
        slope_b,
        t_center,
        u_center,
    )
    certify_transition_transport(
        parent,
        qnl,
        connector,
        tangent,
        module,
        root,
        slope_a,
        slope_b,
        t_center,
    )
    print("GATE1_FULL_CROSS_LAYER: CERTIFIED")
    print("GATE1_TRANSPORTED_TWISTING_LAYER: OPEN / FAIL-CLOSED")
    return 0


def main():
    try:
        return certify()
    except Exception as exc:
        print(f"GATE1_FULL_CROSS_TRANSPORT: FAILED: {exc}")
        print("FULL_CROSS_COMMON_VERTEX: NOT CERTIFIED")
        print("ACTUAL_VERTEX_TRANSITION_DERIVATIVE: NOT CERTIFIED")
        print("CLOSED_COMMON_VERTEX_LOOP_DERIVATIVE: NOT CERTIFIED")
        print("TRANSPORTED_TWISTING: NOT CERTIFIED")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
