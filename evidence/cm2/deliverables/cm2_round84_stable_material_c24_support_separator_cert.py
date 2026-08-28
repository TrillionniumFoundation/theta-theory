#!/usr/bin/env python3
"""Separate the frozen 96-word stable/material anchor from every C24 root core."""
from __future__ import annotations

import hashlib
import json
import sys
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

import cm2_gate2_actual_stable_plaque_continuation_cert as plaque
import cm2_gate25_physical_return_core_registry_cert as core_cert
import cm2_round80_time3_dihedral_quotient_generator as symmetry
from cm2_round79_tangency_intersection_generator import digest


HERE = Path(__file__).resolve().parent
PRECISION_BITS = 2400
TUBE_RADIUS_UPPER = Q(1, 10**13)
CENTER_GAP_LOWER = Q(19, 10000)
TUBE_GAP_LOWER = Q(1, 1000)
PLAQ_MANIFEST = HERE / "cm2-gate2-actual-stable-plaque-continuation-manifest-2026-07-15.json"
ROUND59_MANIFEST = HERE / "cm2-gate123-round59-physical-formula-shadow-dini-frontier-manifest-2026-07-20.json"
MATERIAL_MANIFEST = HERE / "cm2-gate13-round66-same-representative-material-trace-frontier-manifest-2026-07-21.json"
CORE_MANIFEST = HERE / "cm2-gate25-physical-return-core-registry-manifest-2026-07-16.json"
ROOT_MANIFEST = HERE / "cm2-round69-base-s-return-incidence-all-gate-manifest-2026-07-21.json"
EXPECTED_PINS = {
    "stable_plaque_source": "de55156ff2aec7b15ec57d566587c788d75b6f0bd1edc9e28f6700fbea445f82",
    "stable_plaque_manifest": "1bfc3ea9f5eb587b41a94ba4fd808c03c309389269f8d5e903f9bfce09a4f871",
    "round59_binding": "16a2562868df58b2e14bf672d2d0d11735581016ff50e10f5a6d2c1e660d3466",
    "round66_material_binding": "11bb7ba12e3302a547893dae3a897efc5a66223bbc2cf740bb6f7b5e53882224",
    "C24_core_source": "2da58e5fb5fe030023d6fade7252ec67d0e494708b32d1e32b3ce545e2052fdb",
    "C24_core_manifest": "144f5516ada8b83ca07459582c8cdb07ba09db11ac18a90cff32c6396c6e5a42",
    "round69_root": "08d996d52d6aa8ea3b716a46b51d6ae8f0a6b4b9e24c9fab402afe88059bc838",
}


def file_digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def arb_ball(full: Any, parent: Any, module: Any, center: Any, radius: Any) -> Any:
    return center + full.symmetric_ball(parent, module, radius)


def coordinate_separation(
    module: Any,
    t_value: Any,
    p_value: Any,
    core: Any,
) -> tuple[str, Any] | None:
    candidates = (
        ("t_below", module.arb(core.t0.numerator) / core.t0.denominator - t_value),
        ("t_above", t_value - module.arb(core.t1.numerator) / core.t1.denominator),
        ("p_below", module.arb(core.p0.numerator) / core.p0.denominator - p_value),
        ("p_above", p_value - module.arb(core.p1.numerator) / core.p1.denominator),
    )
    strict = [(label, gap) for label, gap in candidates if gap > 0]
    if not strict:
        return None
    return max(strict, key=lambda item: float(item[1].mid()))


def reconstruct_geometry() -> tuple[Any, Any, Any, Any, Any, list[tuple[str, int, int]], Any]:
    closed = plaque.load(plaque.CLOSED_CERT, "cm2_round84_separator_closed")
    tangent = plaque.load(plaque.TANGENT_CERT, "cm2_round84_separator_tangent")
    full = plaque.load(plaque.FULL_CERT, "cm2_round84_separator_full")
    parent = plaque.load(plaque.PARENT_CERT, "cm2_round84_separator_parent")
    qnl = plaque.load(plaque.QNL_CERT, "cm2_round84_separator_qnl")
    connector = plaque.load(plaque.CONNECTOR_CERT, "cm2_round84_separator_connector")
    local = plaque.load(plaque.LOCAL_RETURN_CERT, "cm2_round84_separator_local")
    module = tangent.load_frozen_certificate()
    module.ctx.prec = PRECISION_BITS
    closed.refresh_exact_geometry(module)
    q_word = tangent.QNL_FORWARD_WORD
    b_word = tangent.CONNECTOR_REVERSE_FORWARD_WORD
    half_word = q_word * 2 + b_word * 2
    full_word = q_word * 2 + b_word * 4 + q_word * 2
    if len(full_word) != 96:
        raise RuntimeError("frozen physical word length")

    root_center = module.arb(closed.SHADOW_A_CENTER)
    for _step in range(2):
        shot = closed.propagate_symmetric(tangent, module, root_center, half_word)
        root_center = module.arb(
            (root_center - shot.momentum.value / shot.momentum.derivative[0]).str(
                680, radius=False, more=True
            )
        )
    root_box = module.arb(root_center.str(680, radius=False, more=True), plaque.REFINED_ROOT_RADIUS)
    theta_star = module.arb.pi() / 4 + 2 * root_box / module.R_GRAY
    half_matrix, _, _ = closed.symplectic_segment_matrix(
        tangent, module, theta_star, module.arb(0), half_word
    )
    aa, bb = half_matrix[0, 0], half_matrix[0, 1]
    cc, dd = half_matrix[1, 0], half_matrix[1, 1]
    loop_slope = ((2 * aa * cc) / (2 * bb * dd)).sqrt()
    graph_center = module.arb(plaque.GRAPH_PARAMETER_CENTER)
    graph_radius = module.arb(plaque.GRAPH_PARAMETER_RADIUS)
    graph_height = module.arb(plaque.LOCAL_UNSTABLE_GRAPH_SLOPE) * (
        abs(graph_center) + graph_radius
    )
    if local.UNSTABLE_CONE_SLOPE != plaque.LOCAL_UNSTABLE_GRAPH_SLOPE:
        raise RuntimeError("local unstable cone changed")

    def direct_loop(center_u: Any, center_v: Any) -> tuple[Any, Any]:
        u = module.Dual(center_u, dimension=0)
        v = module.Dual(center_v, dimension=0)
        replay = tangent.propagate(
            module,
            "G",
            module.Dual(theta_star, dimension=0) + (u + v) / module.R_GRAY,
            loop_slope * (u - v),
            full_word,
        )
        ds = module.R_GRAY * (replay.theta - module.Dual(theta_star, dimension=0))
        return (
            ((ds + replay.momentum / loop_slope) / 2).value,
            ((ds - replay.momentum / loop_slope) / 2).value,
        )

    def map_box(
        center_u: Any,
        radius_u: Any,
        center_v: Any,
        radius_v: Any,
    ) -> tuple[list[Any], list[Any]]:
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
        model = full.to_connector_eigen(module, replay, theta_star, loop_slope)
        tight_u, tight_v = direct_loop(center_u, center_v)
        for raw, tight in zip(model.center, (tight_u, tight_v)):
            if not (raw - tight).contains(0):
                raise RuntimeError("Taylor center replay mismatch")
        radii = [
            abs(model.linear[index][0]) * radius_u
            + abs(model.linear[index][1]) * radius_v
            + model.remainder[index]
            for index in range(2)
        ]
        return [tight_u, tight_v], radii

    def rebox(centers: list[Any], radii: list[Any]) -> tuple[list[Any], list[Any]]:
        exact, enlarged = [], []
        for center, radius in zip(centers, radii):
            point, rounding = plaque.decimal_center(module, center)
            exact.append(point)
            enlarged.append(radius + rounding)
        return exact, enlarged

    def two_returns(center_u: Any, radius_u: Any) -> tuple[list[Any], list[Any]]:
        first = map_box(center_u, radius_u, module.arb(0), graph_height)
        intermediate_center, intermediate_radius = rebox(first[0], first[1])
        return map_box(
            intermediate_center[0], intermediate_radius[0],
            intermediate_center[1], intermediate_radius[1],
        )

    whole_center, whole_radius = two_returns(graph_center, graph_radius)
    crossing_correction, crossing_rounding = plaque.decimal_center(module, whole_center[1])
    crossing_uncertainty = whole_radius[1] + crossing_rounding
    crossing_center = module.arb(root_center.str(680, radius=False, more=True)) + crossing_correction
    if not crossing_uncertainty + abs(root_box - root_center) < module.arb(plaque.SECOND_SOURCE_U_RADIUS):
        raise RuntimeError("stable crossing left the frozen source strip")
    return module, full, parent, qnl, connector, full_word, (tangent, loop_slope, crossing_center)


def state_tubes() -> tuple[Any, list[dict[str, Any]], Any]:
    module, full, parent, qnl, connector, word, tail = reconstruct_geometry()
    tangent, loop_slope, crossing_center = tail
    radii = [module.arb(plaque.SECOND_SOURCE_U_RADIUS), module.arb(plaque.SECOND_SOURCE_V_RADIUS)]
    center = [
        module.arb.pi() / 4 + crossing_center / module.R_GRAY,
        loop_slope * crossing_center,
    ]
    linear = [[1 / module.R_GRAY, 1 / module.R_GRAY], [loop_slope, -loop_slope]]
    remainder = [module.arb(0), module.arb(0)]
    current_kind = "G"
    cumulative_i = cumulative_j = 0
    rows = []
    maximum_radius = module.arb(0)

    def append_state(rank: int, next_target: Any | None) -> list[Any]:
        nonlocal maximum_radius
        total_radius = [
            remainder[output]
            + sum(
                (abs(linear[output][parameter]) * radii[parameter] for parameter in range(2)),
                module.arb(0),
            )
            for output in range(2)
        ]
        maximum_radius = maximum_radius.max(total_radius[0]).max(total_radius[1])
        rows.append({
            "state_rank": rank,
            "source_component": current_kind,
            "next_target": None if next_target is None else f"{next_target[0]}[{next_target[1]},{next_target[2]}]",
            "theta_center": str(center[0]),
            "momentum_center": str(center[1]),
            "theta_radius": str(total_radius[0]),
            "momentum_radius": str(total_radius[1]),
            "cumulative_lift": [cumulative_i, cumulative_j],
        })
        return total_radius

    for rank, target_key in enumerate(word):
        total_radius = append_state(rank, target_key)
        state_boxes = [
            arb_ball(full, parent, module, center[output], total_radius[output])
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
            raise RuntimeError("Taylor state tube crossed a transparent wall")
        box_jacobian = [box_step.angle.gradient, box_step.momentum.gradient]
        center_jacobian = [center_step.angle.gradient, center_step.momentum.gradient]
        hessians = [box_step.angle.hessian, box_step.momentum.hessian]
        new_center = [center_step.angle.value, center_step.momentum.value]
        new_linear = full.mat_mul(module, center_jacobian, linear)
        new_remainder = []
        for output in range(2):
            propagated = sum(
                (abs(box_jacobian[output][state]) * remainder[state] for state in range(2)),
                module.arb(0),
            )
            quadratic = sum(
                (
                    abs(hessians[output][left][right])
                    * total_radius[left] * total_radius[right]
                    for left in range(2) for right in range(2)
                ),
                module.arb(0),
            ) / 2
            new_remainder.append(propagated + quadratic)
        center, linear, remainder = new_center, new_linear, new_remainder
        cumulative_i += target_key[1]
        cumulative_j += target_key[2]
        current_kind = target_key[0]
    append_state(len(word), None)
    if len(rows) != 97:
        raise RuntimeError("state tube count")
    return module, rows, maximum_radius


def build() -> dict[str, Any]:
    module, raw_rows, maximum_radius = state_tubes()
    cores = core_cert.physical_cores()
    state_rows = []
    comparison_rows = []
    categorical_component_mismatches = 0
    numeric_comparisons = 0
    separated = 0
    minimum_center: tuple[float, Any, dict[str, Any]] | None = None
    minimum_tube: tuple[float, Any, dict[str, Any]] | None = None
    for raw in raw_rows:
        theta_center = module.arb(raw["theta_center"])
        momentum_center = module.arb(raw["momentum_center"])
        theta_radius = module.arb(raw["theta_radius"])
        momentum_radius = module.arb(raw["momentum_radius"])
        # Build balls through the same outward-rounded helper used in the recurrence.
        radius_text = (4 * theta_radius.abs_upper()).str(130, radius=False, more=True)
        theta_box = theta_center + module.arb(0, radius_text)
        momentum_text = (4 * momentum_radius.abs_upper()).str(130, radius=False, more=True)
        momentum_box = momentum_center + module.arb(0, momentum_text)
        nx_box, ny_box = theta_box.cos(), theta_box.sin()
        nx_center, ny_center = theta_center.cos(), theta_center.sin()
        state_rows.append(raw)
        for action_name, matrix in symmetry.MATRICES.items():
            a, b, c, d = matrix
            determinant = a * d - b * c
            transformed_nx_box = a * nx_box + b * ny_box
            transformed_ny_box = c * nx_box + d * ny_box
            transformed_nx_center = a * nx_center + b * ny_center
            transformed_ny_center = c * nx_center + d * ny_center
            transformed_p_box = determinant * momentum_box
            transformed_p_center = determinant * momentum_center
            for core_index, core in enumerate(cores):
                identity = {
                    "state_rank": raw["state_rank"],
                    "symmetry": action_name,
                    "core_index": core_index,
                }
                if core.source != raw["source_component"]:
                    categorical_component_mismatches += 1
                    separated += 1
                    comparison_rows.append({**identity, "status": "DISJOINT_COMPONENT"})
                    continue
                numeric_comparisons += 1
                side = core.chart_id.split(":")[1]
                t_box = transformed_ny_box if side in ("E", "W") else transformed_nx_box
                t_center = transformed_ny_center if side in ("E", "W") else transformed_nx_center
                tube_separation = coordinate_separation(module, t_box, transformed_p_box, core)
                center_separation = coordinate_separation(module, t_center, transformed_p_center, core)
                if tube_separation is None or center_separation is None:
                    raise RuntimeError(f"unseparated state/core pair {identity}")
                if not tube_separation[1] > module.arb(TUBE_GAP_LOWER.numerator) / TUBE_GAP_LOWER.denominator:
                    raise RuntimeError(f"tube gap below uniform threshold {identity}")
                if not center_separation[1] > module.arb(CENTER_GAP_LOWER.numerator) / CENTER_GAP_LOWER.denominator:
                    raise RuntimeError(f"center gap below uniform threshold {identity}")
                separated += 1
                comparison_rows.append({
                    **identity,
                    "status": "STRICT_COORDINATE_SEPARATION",
                    "separator": tube_separation[0],
                })
                center_key = float(center_separation[1].mid())
                tube_key = float(tube_separation[1].mid())
                witness = {**identity, "separator": tube_separation[0]}
                if minimum_center is None or center_key < minimum_center[0]:
                    minimum_center = center_key, center_separation[1], witness
                if minimum_tube is None or tube_key < minimum_tube[0]:
                    minimum_tube = tube_key, tube_separation[1], witness

    if not maximum_radius < module.arb(TUBE_RADIUS_UPPER.numerator) / TUBE_RADIUS_UPPER.denominator:
        raise RuntimeError("maximum phase-state tube radius")
    expected_total = 8 * 97 * 24
    if len(comparison_rows) != expected_total or separated != expected_total:
        raise RuntimeError("D4 state/core comparison accounting")
    if categorical_component_mismatches != expected_total // 2 or numeric_comparisons != expected_total // 2:
        raise RuntimeError("component/numeric comparison split")
    assert minimum_center is not None and minimum_tube is not None

    plaque_manifest = json.loads(PLAQ_MANIFEST.read_text())
    round59 = json.loads(ROUND59_MANIFEST.read_text())
    material = json.loads(MATERIAL_MANIFEST.read_text())
    core_manifest = json.loads(CORE_MANIFEST.read_text())
    root_manifest = json.loads(ROOT_MANIFEST.read_text())
    if not plaque_manifest["proved_layers"]["positive_width_actual_plaque_96_word_strip"]:
        raise RuntimeError("frozen stable strip binding")
    if round59["result"]["gate2"]["physical_finite_shadow_registry"]["row_count"] != 96:
        raise RuntimeError("Round-59 word binding")
    material_atlas = material["result"]["gate3"]["physical_compact_interior_atlas"]
    if material_atlas["status"] != "CERTIFIED_LOCAL" or "96-collision" not in material_atlas["physical_input"]:
        raise RuntimeError("Round-66 material binding")
    root_audit = root_manifest["result"]["gate24_depth1_graph_audit"]
    if root_audit["actual_invariant_stable_plaques"] != 0 or root_audit["actual_stable_holonomy_rows"] != 0:
        raise RuntimeError("Round-69 root frontier changed")

    result = {
        "precision_bits": PRECISION_BITS,
        "physical_word_length": 96,
        "phase_state_tube_count": len(state_rows),
        "dihedral_action_count": len(symmetry.MATRICES),
        "C24_core_count": len(cores),
        "state_action_core_comparison_count": len(comparison_rows),
        "categorical_component_mismatch_count": categorical_component_mismatches,
        "numeric_phase_core_comparison_count": numeric_comparisons,
        "certified_disjoint_comparison_count": separated,
        "unresolved_comparison_count": 0,
        "maximum_phase_state_radius": str(maximum_radius),
        "maximum_phase_state_radius_strict_upper": str(TUBE_RADIUS_UPPER),
        "minimum_center_coordinate_gap": str(minimum_center[1]),
        "minimum_center_coordinate_gap_strict_lower": str(CENTER_GAP_LOWER),
        "minimum_tube_coordinate_gap": str(minimum_tube[1]),
        "minimum_tube_coordinate_gap_strict_lower": str(TUBE_GAP_LOWER),
        "minimum_gap_witness": minimum_tube[2],
        "state_rows": state_rows,
        "state_rows_sha256": digest(state_rows),
        "comparison_rows": comparison_rows,
        "comparison_rows_sha256": digest(comparison_rows),
        "same_key_conclusion": "EXISTING_96_WORD_STABLE_AND_DEPTH96_MATERIAL_ANCHOR_DISJOINT_FROM_C24_ROOT_SUPPORT_AT_ALL_97_REGISTERED_PHASE_STATES_AND_D4_IMAGES",
        "required_constructive_route": "BUILD_STABLE_MATERIAL_DATA_DIRECTLY_ON_A_SELECTED_C24_ATOM_OR_REPLACE_THE_LANDING_REGISTRY",
        "gate4": "1/7_UNCHANGED",
        "strict_nonclaims": [
            "the separator does not prove absence of stable plaques on C24",
            "the separator does not construct a same-key stable holonomy or all-depth commuting square",
            "the separator does not exclude unrelated time shifts outside the frozen 96-word anchor",
            "the separator does not promote any Gate-4 field",
        ],
    }
    pins = {
        "stable_plaque_source": file_digest(HERE / "cm2_gate2_actual_stable_plaque_continuation_cert.py"),
        "stable_plaque_manifest": file_digest(PLAQ_MANIFEST),
        "round59_binding": file_digest(ROUND59_MANIFEST),
        "round66_material_binding": file_digest(MATERIAL_MANIFEST),
        "C24_core_source": file_digest(HERE / "cm2_gate25_physical_return_core_registry_cert.py"),
        "C24_core_manifest": file_digest(CORE_MANIFEST),
        "round69_root": file_digest(ROOT_MANIFEST),
    }
    if pins != EXPECTED_PINS:
        raise RuntimeError("frozen upstream pin mismatch")
    return {
        "schema": "cm2.round84.stable-material-c24-support-separator.v1",
        "pins": pins,
        "result": result,
        "result_sha256": digest(result),
    }


def main() -> int:
    json.dump(build(), sys.stdout, sort_keys=True, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
