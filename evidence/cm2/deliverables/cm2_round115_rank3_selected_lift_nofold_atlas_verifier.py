#!/usr/bin/env python3
"""Independent high-precision verifier for the Round115 no-fold atlas.

The verifier does not import the Round115 or Round114 producer.  It rebuilds
the selected two-collision lift, the correlated affine root tubes, and every
implicit q'' leaf at higher precision.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from dataclasses import replace
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from flint import arb, ctx

import cm2_gate25_physical_return_core_registry_cert as core_cert
from cm2_round76_r2_numeric_fields_generator import Jet, aq, center, interval, normal


HERE = Path(__file__).resolve().parent
CERTIFICATE = HERE / "cm2-round115-rank3-selected-lift-nofold-atlas-2026-07-23.json"
PRODUCER = HERE / "cm2_round115_rank3_selected_lift_nofold_atlas.py"
ROUND112 = HERE / "cm2-round112-rank3-double-grazing-two-sided-root-sheet-2026-07-23.json"
ROUND114 = HERE / "cm2-round114-rank3-seam-root-stitch-gap-atlas-2026-07-23.json"
PINS = {
    PRODUCER.name: "2552bcd8ad4cf769b2d65665d43e661331fffd9a0e00330af4bb11283169db7b",
    CERTIFICATE.name: "bcaa3612fe6369b7a6a55e51cd7d345d3a7e4817906dd5998ad544d945035263",
    ROUND112.name: "94a54ddbf31518cfc2a93b105d66337111f2b950be894f126e7b9c042e6b02e5",
    ROUND114.name: "945cbd96032544bdff449398715f173cabb9e034415a0ca5edb594715ce970d4",
    "cm2_gate25_physical_return_core_registry_cert.py": "2da58e5fb5fe030023d6fade7252ec67d0e494708b32d1e32b3ce545e2052fdb",
    "cm2_round76_r2_numeric_fields_generator.py": "96facebedf899d98d274f8a8c036fa8f02d1c34512933a587f7e581df174aadf",
}
CERTIFICATE_SCHEMA = "cm2.round115.rank3-selected-lift-nofold-atlas.v1"
ROUND112_SCHEMA = "cm2.round112.rank3-double-grazing-two-sided-root-sheet.v1"
ROUND114_SCHEMA = "cm2.round114.rank3-seam-root-stitch-gap-atlas.v1"
VERIFICATION_SCHEMA = "cm2.round115.rank3-selected-lift-nofold-atlas-verification.v1"
VERIFIER_PRECISION_BITS = 896
EDGE_WIDTH = Q(1, 16384)
TUBE_RADIUS = Q(3, 100_000_000)
Q_SECOND_MARGIN = Q(1, 1000)
FACE_MARGIN = Q(1, 1_000_000_000)
LEAF_POWERS = (9, 9, 9, 9, 9, 9, 11, 11)
RESULT_KEYS = frozenset({
    "affine_root_tube_radius", "certified_affine_root_tube_count",
    "certified_exact_stationary_corner_count", "certified_q_second_and_q_prime_over_c0_margin",
    "certified_root_edge_q_injective_count", "certified_selected_lift_whole_trace_no_fold_atlas_count",
    "closed_interval_q_prime_nonvanishing_claim", "edge_width",
    "input_round114_selected_lift_trace_coverage_count", "new_gate5_actual_child_field_count",
    "physical_owner_whole_trace_no_fold_atlas_count", "precision_bits", "root_edge_rows",
    "root_edge_rows_sha256", "root_graph_c2_bound_count", "strict_nonclaims", "strict_scope",
    "strict_separator", "upstream_and_helper_pins", "whole_collar_complete_57_candidate_ordering_count",
    "whole_trace_positive_reach_certificate_count", "whole_trace_two_sided_physical_collar_count",
    "whole_trace_uniform_other_singularity_separation_count",
})
ROW_KEYS = frozenset({
    "affine_center_c0", "affine_center_t_root_bracket", "affine_error_radius", "affine_slope",
    "affine_t_reference", "affine_tube_inside_round112_t_box", "branch_key",
    "certified_uniform_q_prime_over_c0_abs_lower_bound", "corner_flow_shift_lambda_sign",
    "corner_flow_shift_lemma", "corner_parameter_enclosure", "corner_stationary_identity",
    "dyadic_leaf_count", "dyadic_leaf_power", "dyadic_leaf_sign_digest", "exterior_port_id",
    "implicit_error_first_formula", "implicit_error_second_formula", "outer_parameter_enclosure",
    "parameterized_root_tube_equation_error_derivative_abs_lower_bound",
    "parameterized_root_tube_equation_error_derivative_sign",
    "parameterized_root_tube_lower_face_abs_margin", "parameterized_root_tube_lower_face_sign",
    "parameterized_root_tube_theorem", "parameterized_root_tube_upper_face_abs_margin",
    "parameterized_root_tube_upper_face_sign", "physical_owner_atlas_installed",
    "positive_reach_installed", "pre_root_tail_parameter_interval", "projective_end",
    "projective_parameter_derivative_sign_for_c0_positive", "projective_parameter_direction",
    "q_prime_closed_interval_avoids_zero", "q_prime_sign_for_c0_positive",
    "q_second_derivative_abs_lower_bound", "q_second_derivative_formula", "q_second_derivative_sign",
    "ray_index", "root_coordinate_interval", "root_edge_overlaps_certified_base_before_tail_margin",
    "root_edge_q_injective", "root_edge_to_base_chain_stitch_parameter",
    "root_edge_to_base_chain_transition", "root_edge_to_base_chain_transition_coordinate",
    "root_graph_abs_d2t_dc0_2_upper_bound", "root_graph_abs_dt_dc0_upper_bound",
    "root_graph_parameter_plane_curvature_upper_bound", "root_q_abs_second_derivative_upper_bound",
    "selected_lift_whole_trace_no_fold_atlas_installed", "source_chart",
    "source_chart_orientation_epsilon", "source_grazing_sign_sigma0",
    "stereographic_q_denominator_lower_bound_inherited_from_round114",
    "two_sided_physical_collar_installed", "uniform_other_singularity_separation_installed",
})
EXPECTED_SCOPE = (
    "eight selected-lift shared grazing edges with parameterized affine root tubes, exact stationary "
    "corner flow-shift identities, strict q_prime/c0 signs, injective q crosswalks, and C2 root-graph bounds"
)
EXPECTED_NONCLAIMS = [
    "q_prime equals zero at c0=0; only q_prime/c0 on c0>0 has a uniform strict sign",
    "selected-lift no-fold does not install first/second/third physical-owner ordering",
    "a C2 graph and injective q coordinate do not by themselves install positive normal reach for the whole physical trace",
    "no uniform distance to every other collision singularity, wall corner, flight cap, or representation seam is installed",
    "HIT and BYPASS remain separate real sheets sharing only c3=b3=0",
    "no two-sided physical collar, complete 57-candidate order, homogeneity child, official word, or Gate5 field is installed",
]
EXPECTED_SEPARATOR = {
    "CM2": "NO-GO_FOR_CLAIM",
    "physical_owner_trace_closure": "0/8",
    "selected_lift_algebraic_trace_coverage": "8/8",
    "selected_lift_whole_trace_no_fold_atlas": "8/8",
    "whole_trace_positive_reach": "0/8",
    "whole_trace_two_sided_physical_collar": "0/8",
}
EXPECTED_UPSTREAM = {
    ROUND114.name: "945cbd96032544bdff449398715f173cabb9e034415a0ca5edb594715ce970d4",
    "cm2_round114_rank3_seam_root_stitch_gap_atlas.py": "47a231e32df2121058185a0fd82cbfb6c6105ace0d268a257103bc005b46ed02",
    "cm2_gate25_physical_return_core_registry_cert.py": "2da58e5fb5fe030023d6fade7252ec67d0e494708b32d1e32b3ce545e2052fdb",
    "cm2_round76_r2_numeric_fields_generator.py": "96facebedf899d98d274f8a8c036fa8f02d1c34512933a587f7e581df174aadf",
    "cm2_round79_tangency_intersection_generator.py": "971f918ca1ed23bd081adf3b233d578e750b61231b20113327f221b40b890ed7",
    "cm2_round112_rank3_double_grazing_two_sided_root_sheet.py": "ccdfeebfa14fdaa466a67b79269145b2a36076b7027f2bac0a9c5daa030b5e3f",
}


def strict_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def reject_nonfinite(token: str) -> Any:
    raise ValueError(f"nonfinite JSON number: {token}")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(), object_pairs_hook=strict_pairs, parse_constant=reject_nonfinite)


def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def strict_sign(value: arb) -> int:
    if bool(value > 0):
        return 1
    if bool(value < 0):
        return -1
    return 0


def radius(target: str) -> Q:
    return Q(9, 25) if target[0] == "G" else Q(4, 25)


def collision(
    point_x: Jet,
    point_y: Jet,
    velocity_x: Jet,
    velocity_y: Jet,
    target_x: Jet,
    target_y: Jet,
    target_radius: Q,
) -> dict[str, Jet]:
    r = aq(target_radius)
    dx, dy = target_x - point_x, target_y - point_y
    longitudinal = velocity_x * dx + velocity_y * dy
    transverse = -velocity_y * dx + velocity_x * dy
    discriminant = r * r - transverse * transverse
    radical = discriminant.sqrt()
    flight = longitudinal - radical
    hit_x = point_x + flight * velocity_x
    hit_y = point_y + flight * velocity_y
    return {
        "hit_x": hit_x,
        "hit_y": hit_y,
        "normal_x": (hit_x - target_x) / r,
        "normal_y": (hit_y - target_y) / r,
        "momentum": transverse / r,
    }


def evaluate_affine(
    source: Any,
    branch: tuple[Any, ...],
    source_sign: int,
    t_reference: Q,
    affine_slope: Q,
    c_center: Q,
    c_lower: Q,
    c_upper: Q,
    e_lower: Q,
    e_upper: Q,
) -> dict[str, Jet]:
    c0 = Jet.variable(interval(c_lower, c_upper), 0)
    error = Jet.variable(interval(e_lower, e_upper), 1)
    t = Jet(aq(t_reference)) + aq(affine_slope) * (c0 - aq(c_center)) + error
    zero = Jet(arb(0))
    nx0, ny0 = normal(source.chart_id.split(":")[1], t)
    p0 = source_sign * (arb(1) - c0 * c0).sqrt()
    ux0, uy0 = c0 * nx0 - p0 * ny0, c0 * ny0 + p0 * nx0
    sx, sy = center(f"{source.source}[0,0]", zero)
    px, py = sx + aq(radius(source.source)) * nx0, sy + aq(radius(source.source)) * ny0

    target1_x, target1_y = center(source.target_id, zero)
    first = collision(px, py, ux0, uy0, target1_x, target1_y, radius(source.target_id))
    p1 = first["momentum"]
    c1 = (arb(1) - p1 * p1).sqrt()
    ux1 = c1 * first["normal_x"] - p1 * first["normal_y"]
    uy1 = c1 * first["normal_y"] + p1 * first["normal_x"]

    target2_x, target2_y = center(branch[1], zero)
    second = collision(
        first["hit_x"], first["hit_y"], ux1, uy1,
        target2_x, target2_y, radius(branch[1]),
    )
    p2 = second["momentum"]
    c2 = (arb(1) - p2 * p2).sqrt()
    ux2 = c2 * second["normal_x"] - p2 * second["normal_y"]
    uy2 = c2 * second["normal_y"] + p2 * second["normal_x"]

    target3_x, target3_y = center(branch[2], zero)
    dx, dy = target3_x - second["hit_x"], target3_y - second["hit_y"]
    transverse = -uy2 * dx + ux2 * dy
    r3 = aq(radius(branch[2]))
    equation = r3 * r3 - transverse * transverse
    denominator = arb(1) + ux2
    return {"equation": equation, "projective_q": uy2 / denominator, "denominator": denominator}


def implicit_derivatives(values: dict[str, Jet]) -> tuple[arb, arb, arb, arb]:
    f, q = values["equation"], values["projective_q"]
    e1 = -f.gradient[0] / f.gradient[1]
    e2 = -(f.hessian[0][0] + 2 * f.hessian[0][1] * e1 + f.hessian[1][1] * e1 * e1) / f.gradient[1]
    q1 = q.gradient[0] + q.gradient[1] * e1
    q2 = q.hessian[0][0] + 2 * q.hessian[0][1] * e1 + q.hessian[1][1] * e1 * e1 + q.gradient[1] * e2
    return e1, e2, q1, q2


def mean_face(
    source: Any,
    branch: tuple[Any, ...],
    source_sign: int,
    t_reference: Q,
    slope: Q,
    center_c: Q,
    face: Q,
) -> arb:
    point = evaluate_affine(source, branch, source_sign, t_reference, slope, center_c, center_c, center_c, face, face)["equation"]
    box = evaluate_affine(source, branch, source_sign, t_reference, slope, center_c, Q(0), EDGE_WIDTH, face, face)["equation"]
    return point.value + box.gradient[0] * interval(-EDGE_WIDTH / 2, EDGE_WIDTH / 2)


def abs_lt(value: arb, bound: Q) -> bool:
    return bool(abs(value) < aq(bound))


def validate_envelope(document: dict[str, Any], schema: str) -> dict[str, Any]:
    if set(document) != {"schema", "result", "result_sha256"}:
        raise RuntimeError("open document envelope")
    if document["schema"] != schema or document["result_sha256"] != digest(document["result"]):
        raise RuntimeError("document digest/schema mismatch")
    return document["result"]


def validate_contract(document: dict[str, Any]) -> dict[str, Any]:
    result = validate_envelope(document, CERTIFICATE_SCHEMA)
    if set(result) != RESULT_KEYS or result["root_edge_rows_sha256"] != digest(result["root_edge_rows"]):
        raise RuntimeError("open result/row digest")
    if (
        result["precision_bits"] != 640
        or result["edge_width"] != "1/16384"
        or result["affine_root_tube_radius"] != "3/100000000"
        or result["certified_q_second_and_q_prime_over_c0_margin"] != "1/1000"
        or result["strict_scope"] != EXPECTED_SCOPE
        or result["strict_nonclaims"] != EXPECTED_NONCLAIMS
        or result["strict_separator"] != EXPECTED_SEPARATOR
        or result["upstream_and_helper_pins"] != EXPECTED_UPSTREAM
    ):
        raise RuntimeError("global literal contract")
    exact_counts = {
        "input_round114_selected_lift_trace_coverage_count": 8,
        "certified_affine_root_tube_count": 8,
        "certified_exact_stationary_corner_count": 8,
        "certified_root_edge_q_injective_count": 8,
        "certified_selected_lift_whole_trace_no_fold_atlas_count": 8,
        "root_graph_c2_bound_count": 8,
        "physical_owner_whole_trace_no_fold_atlas_count": 0,
        "whole_trace_positive_reach_certificate_count": 0,
        "whole_trace_uniform_other_singularity_separation_count": 0,
        "whole_trace_two_sided_physical_collar_count": 0,
        "whole_collar_complete_57_candidate_ordering_count": 0,
        "new_gate5_actual_child_field_count": 0,
    }
    if any(result[key] != value for key, value in exact_counts.items()):
        raise RuntimeError("global count contract")
    if result["closed_interval_q_prime_nonvanishing_claim"] is not False:
        raise RuntimeError("forbidden closed-interval derivative claim")
    if len(result["root_edge_rows"]) != 8:
        raise RuntimeError("root-edge row count")
    for index, row in enumerate(result["root_edge_rows"]):
        if set(row) != ROW_KEYS or row["ray_index"] != index:
            raise RuntimeError("open or misordered root-edge row")
        power = LEAF_POWERS[index]
        expected_direction = 1 if row["projective_end"] == "RIGHT_PROJECTIVE_END" else -1
        expected_epsilon = 1 if row["source_chart"].split(":")[1] in ("E", "S") else -1
        false_fields = (
            "physical_owner_atlas_installed", "positive_reach_installed",
            "uniform_other_singularity_separation_installed", "two_sided_physical_collar_installed",
            "q_prime_closed_interval_avoids_zero",
        )
        if (
            row["root_coordinate_interval"] != ["0", "1/16384"]
            or row["affine_center_c0"] != "1/32768"
            or row["affine_error_radius"] != "3/100000000"
            or row["dyadic_leaf_power"] != power
            or row["dyadic_leaf_count"] != 1 << power
            or row["q_second_derivative_abs_lower_bound"] != "1/1000"
            or row["certified_uniform_q_prime_over_c0_abs_lower_bound"] != "1/1000"
            or row["parameterized_root_tube_equation_error_derivative_abs_lower_bound"] != "7"
            or row["parameterized_root_tube_lower_face_abs_margin"] != "1/1000000000"
            or row["parameterized_root_tube_upper_face_abs_margin"] != "1/1000000000"
            or row["root_graph_abs_dt_dc0_upper_bound"] != "2"
            or row["root_graph_abs_d2t_dc0_2_upper_bound"] != "10"
            or row["root_graph_parameter_plane_curvature_upper_bound"] != "10"
            or row["root_q_abs_second_derivative_upper_bound"] != "10"
            or row["projective_parameter_direction"] != expected_direction
            or row["source_chart_orientation_epsilon"] != expected_epsilon
            or row["corner_flow_shift_lambda_sign"] != expected_epsilon * row["source_grazing_sign_sigma0"]
            or row["q_second_derivative_sign"] not in (-1, 1)
            or row["q_prime_sign_for_c0_positive"] != row["q_second_derivative_sign"]
            or expected_direction * row["q_second_derivative_sign"] != -1
            or row["projective_parameter_derivative_sign_for_c0_positive"] != -1
            or row["root_edge_q_injective"] is not True
            or row["selected_lift_whole_trace_no_fold_atlas_installed"] is not True
            or row["affine_tube_inside_round112_t_box"] is not True
            or any(row[name] is not False for name in false_fields)
        ):
            raise RuntimeError(f"root-edge semantic contract: {index}")
        expected_literals = {
            "parameterized_root_tube_theorem": "UNIFORM_OPPOSITE_FACES_PLUS_FIXED_F_e_SIGN_GIVES_ONE_ROOT_FOR_EVERY_c0",
            "corner_stationary_identity": "q_prime(0)=0_EXACT_BY_SOURCE_GRAZING_FLOW_SHIFT",
            "corner_flow_shift_lemma": "J(x,y)=(-y,x); v=c0*n+p0*J*n; n_t=epsilon*J*n/s; lambda=epsilon*sigma0*s; D(x,v)=(R0*v,0); downstream_Delta3_and_q_are_free-flight-shift-invariant",
            "implicit_error_first_formula": "e_prime=-F_c/F_e",
            "implicit_error_second_formula": "e_second=-(F_cc+2*F_ce*e_prime+F_ee*e_prime^2)/F_e",
            "q_second_derivative_formula": "q_cc+2*q_ce*e_prime+q_ee*e_prime^2+q_e*e_second",
            "root_edge_to_base_chain_transition": "UNIQUE_MONOTONE_q_CROSSWALK_ON_ROUND114_OVERLAP",
            "root_edge_to_base_chain_transition_coordinate": "SAME_STEREOGRAPHIC_PROJECTIVE_q",
        }
        if any(row[key] != value for key, value in expected_literals.items()):
            raise RuntimeError(f"formula/theorem literal contract: {index}")
    return result


def resign(document: dict[str, Any]) -> None:
    result = document["result"]
    if "root_edge_rows" in result:
        result["root_edge_rows_sha256"] = digest(result["root_edge_rows"])
    document["result_sha256"] = digest(result)


def set_nested(document: dict[str, Any], path: tuple[Any, ...], value: Any) -> None:
    target: Any = document
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = value


def hostile_self_test(document: dict[str, Any]) -> list[str]:
    attacks = [
        ("closed_qprime_nonzero", ("result", "closed_interval_q_prime_nonvanishing_claim"), True),
        ("physical_owner_true", ("result", "root_edge_rows", 0, "physical_owner_atlas_installed"), True),
        ("reach_true", ("result", "root_edge_rows", 0, "positive_reach_installed"), True),
        ("collar_true", ("result", "root_edge_rows", 0, "two_sided_physical_collar_installed"), True),
        ("qsecond_sign_zero", ("result", "root_edge_rows", 0, "q_second_derivative_sign"), 0),
        ("qprime_corner_nonzero", ("result", "root_edge_rows", 0, "corner_stationary_identity"), "q_prime(0)>0"),
        ("leaf_power_small", ("result", "root_edge_rows", 6, "dyadic_leaf_power"), 9),
        ("tube_radius_large", ("result", "affine_root_tube_radius"), "1/100"),
        ("q_margin_zero", ("result", "root_edge_rows", 0, "q_second_derivative_abs_lower_bound"), "0"),
        ("orientation_flip", ("result", "root_edge_rows", 0, "projective_parameter_direction"), -1),
        ("formula_forgery", ("result", "root_edge_rows", 0, "implicit_error_second_formula"), "forged"),
        ("scope_promotion", ("result", "strict_scope"), "physical two-sided collar"),
        ("count_promotion", ("result", "whole_trace_positive_reach_certificate_count"), 8),
        ("stored_c2_tight_forgery", ("result", "root_edge_rows", 0, "root_graph_abs_d2t_dc0_2_upper_bound"), "1/1000"),
    ]
    rejected: list[str] = []
    for label, path, value in attacks:
        mutant = copy.deepcopy(document)
        set_nested(mutant, path, value)
        resign(mutant)
        try:
            validate_contract(mutant)
        except (KeyError, TypeError, ValueError, RuntimeError):
            rejected.append(label)
        else:
            raise RuntimeError(f"hostile semantic mutation accepted: {label}")
    for label, location in (
        ("unknown_row_key", ("result", "root_edge_rows", 0)),
        ("unknown_result_key", ("result",)),
        ("unknown_envelope_key", ()),
    ):
        mutant = copy.deepcopy(document)
        target: Any = mutant
        for key in location:
            target = target[key]
        target["hostile_unknown_key"] = True
        resign(mutant)
        try:
            validate_contract(mutant)
        except (KeyError, TypeError, ValueError, RuntimeError):
            rejected.append(label)
        else:
            raise RuntimeError(f"hostile unknown-key mutation accepted: {label}")
    for label, text in {
        "duplicate_json_key": '{"x":1,"x":2}',
        "nan_json_number": '{"x":NaN}',
        "infinity_json_number": '{"x":Infinity}',
    }.items():
        try:
            json.loads(text, object_pairs_hook=strict_pairs, parse_constant=reject_nonfinite)
        except (TypeError, ValueError, RuntimeError):
            rejected.append(label)
        else:
            raise RuntimeError(f"hostile JSON accepted: {label}")
    return rejected


def verify(precision_bits: int = VERIFIER_PRECISION_BITS) -> dict[str, Any]:
    if precision_bits < 768:
        raise RuntimeError("insufficient verifier precision")
    ctx.prec = precision_bits
    for name, expected in PINS.items():
        if sha256(HERE / name) != expected:
            raise RuntimeError(f"byte pin mismatch: {name}")
    document = load_json(CERTIFICATE)
    result = validate_contract(document)
    hostile = hostile_self_test(document)
    round112 = validate_envelope(load_json(ROUND112), ROUND112_SCHEMA)
    round114 = validate_envelope(load_json(ROUND114), ROUND114_SCHEMA)
    r112_hits = {row["exterior_port_id"]: row for row in round112["sheet_rows"] if row["sheet_kind"] == "HIT"}
    r114_rows = {row["exterior_port_id"]: row for row in round114["root_edge_stitch_rows"]}
    cores = core_cert.physical_cores()
    verified_leaves = 0
    verified_stationary_lemmas = 0
    verified_tubes = 0
    verified_crosswalks = 0
    for row in result["root_edge_rows"]:
        port_id = row["exterior_port_id"]
        if port_id not in r112_hits or port_id not in r114_rows:
            raise RuntimeError("upstream row crosswalk")
        hit, stitched = r112_hits[port_id], r114_rows[port_id]
        branch = tuple(row["branch_key"])
        if (
            row["branch_key"] != stitched["branch_key"]
            or row["projective_end"] != stitched["projective_end"]
            or row["source_chart"] != hit["source_chart"]
            or row["source_grazing_sign_sigma0"] != hit["source_grazing_sign_sigma0"]
            or row["outer_parameter_enclosure"] != stitched["outer_parameter_enclosure"]
            or row["corner_parameter_enclosure"] != stitched["corner_parameter_enclosure"]
            or row["pre_root_tail_parameter_interval"] != stitched["pre_root_tail_parameter_interval"]
            or row["stereographic_q_denominator_lower_bound_inherited_from_round114"] != stitched["stereographic_q_denominator_lower_bound"]
        ):
            raise RuntimeError("upstream literal crosswalk")
        source = replace(cores[branch[0]], chart_id=row["source_chart"])
        source_sign = row["source_grazing_sign_sigma0"]
        t_reference = Q(row["affine_t_reference"])
        slope = Q(row["affine_slope"])
        center_c = Q(row["affine_center_c0"])
        t_box = tuple(map(Q, hit["enclosing_parameter_box"]["t"]))
        t_zero, t_outer = t_reference - slope * center_c, t_reference + slope * center_c
        if not (t_box[0] < min(t_zero, t_outer) - TUBE_RADIUS < max(t_zero, t_outer) + TUBE_RADIUS < t_box[1]):
            raise RuntimeError("stored affine tube leaves Round112 t box")

        center_bracket = tuple(map(Q, row["affine_center_t_root_bracket"]))
        if t_reference != sum(center_bracket, Q(0)) / 2:
            raise RuntimeError("center root/reference mismatch")
        center_faces = [
            evaluate_affine(source, branch, source_sign, t, slope, center_c, center_c, center_c, Q(0), Q(0))["equation"].value
            for t in center_bracket
        ]
        if strict_sign(center_faces[0]) * strict_sign(center_faces[1]) != -1:
            raise RuntimeError("center root bracket does not straddle")

        tube = evaluate_affine(
            source, branch, source_sign, t_reference, slope, center_c,
            Q(0), EDGE_WIDTH, -TUBE_RADIUS, TUBE_RADIUS,
        )
        f_e = tube["equation"].gradient[1]
        f_e_sign = strict_sign(f_e)
        lower_face = mean_face(source, branch, source_sign, t_reference, slope, center_c, -TUBE_RADIUS)
        upper_face = mean_face(source, branch, source_sign, t_reference, slope, center_c, TUBE_RADIUS)
        if (
            f_e_sign != row["parameterized_root_tube_equation_error_derivative_sign"]
            or strict_sign(lower_face) != row["parameterized_root_tube_lower_face_sign"]
            or strict_sign(upper_face) != row["parameterized_root_tube_upper_face_sign"]
            or not bool(f_e_sign * f_e > aq(Q(7)))
            or not bool(row["parameterized_root_tube_lower_face_sign"] * lower_face > aq(FACE_MARGIN))
            or not bool(row["parameterized_root_tube_upper_face_sign"] * upper_face > aq(FACE_MARGIN))
            or row["parameterized_root_tube_lower_face_sign"] != -f_e_sign
            or row["parameterized_root_tube_upper_face_sign"] != f_e_sign
        ):
            raise RuntimeError("independent parameterized root-tube replay")
        verified_tubes += 1

        # Exact source-grazing flow-shift algebra for counterclockwise
        # J(x,y)=(-y,x).  Here v=c*n+p*Jn, n_t=eps*Jn/s, and
        # lambda=eps*sigma*s, so delta x=R*sigma*Jn=R*v and
        # delta v=n+lambda*sigma*J*n_t=n-n=0.  A shift x->x+a*v leaves
        # transverse, hit point, and all later collisions unchanged because
        # L->L-a and flight->flight-a.
        epsilon, sigma = row["source_chart_orientation_epsilon"], source_sign
        if epsilon * epsilon != 1 or sigma * sigma != 1 or 1 + (epsilon * sigma) * (-sigma * epsilon) != 0:
            raise RuntimeError("exact source-grazing flow-shift algebra")
        corner_t = tuple(map(Q, stitched["corner_t_root_bracket"]))
        affine_t_zero = t_reference - slope * center_c
        corner_values = evaluate_affine(
            source, branch, source_sign, t_reference, slope, center_c,
            Q(0), Q(0), corner_t[0] - affine_t_zero, corner_t[1] - affine_t_zero,
        )
        corner_e1, _corner_e2, corner_q1, _corner_q2 = implicit_derivatives(corner_values)
        corner_t_prime = aq(slope) + corner_e1
        corner_t_ball = interval(corner_t[0], corner_t[1])
        structural_lambda = epsilon * sigma * (arb(1) - corner_t_ball * corner_t_ball).sqrt()
        if (
            strict_sign(corner_t_prime - structural_lambda) != 0
            or strict_sign(corner_q1) != 0
            or not bool(abs(corner_t_prime - structural_lambda) < arb("1e-40"))
            or not bool(abs(corner_q1) < arb("1e-40"))
        ):
            raise RuntimeError("high-precision corner stationary-derivative replay")
        verified_stationary_lemmas += 1

        leaf_signs: list[tuple[int, int]] = []
        leaf_count = row["dyadic_leaf_count"]
        for leaf_index in range(leaf_count):
            c_lower = EDGE_WIDTH * leaf_index / leaf_count
            c_upper = EDGE_WIDTH * (leaf_index + 1) / leaf_count
            values = evaluate_affine(
                source, branch, source_sign, t_reference, slope, center_c,
                c_lower, c_upper, -TUBE_RADIUS, TUBE_RADIUS,
            )
            e1, e2, _q1, q2 = implicit_derivatives(values)
            sign = strict_sign(q2)
            t1 = aq(slope) + e1
            if (
                sign != row["q_second_derivative_sign"]
                or not bool(sign * q2 > aq(Q_SECOND_MARGIN))
                or not abs_lt(t1, Q(2))
                or not abs_lt(e2, Q(10))
                or not abs_lt(q2, Q(10))
            ):
                raise RuntimeError(f"independent implicit leaf replay: ray {row['ray_index']}, leaf {leaf_index}")
            leaf_signs.append((leaf_index, sign))
        if digest(leaf_signs) != row["dyadic_leaf_sign_digest"]:
            raise RuntimeError("leaf sign digest mismatch")
        verified_leaves += leaf_count

        outer = tuple(map(Q, row["outer_parameter_enclosure"]))
        tail = tuple(map(Q, row["pre_root_tail_parameter_interval"]))
        corner = tuple(map(Q, row["corner_parameter_enclosure"]))
        if (
            not (outer[1] < tail[0] < tail[1] < corner[0])
            or Q(row["root_edge_overlaps_certified_base_before_tail_margin"]) != tail[0] - outer[1]
            or row["root_edge_to_base_chain_stitch_parameter"] != row["pre_root_tail_parameter_interval"][0]
            or Q(row["stereographic_q_denominator_lower_bound_inherited_from_round114"]) <= 0
        ):
            raise RuntimeError("independent no-fold overlap/crosswalk replay")
        verified_crosswalks += 1

    verification = {
        "verifier_precision_bits": precision_bits,
        "producer_imported": False,
        "verified_affine_root_tube_count": verified_tubes,
        "verified_exact_stationary_corner_lemma_count": verified_stationary_lemmas,
        "verified_implicit_q_second_leaf_count": verified_leaves,
        "verified_root_edge_base_chain_crosswalk_count": verified_crosswalks,
        "verified_selected_lift_whole_trace_no_fold_atlas_count": 8,
        "physical_owner_atlas_count": 0,
        "positive_reach_count": 0,
        "two_sided_physical_collar_count": 0,
        "semantic_and_schema_attacks_rejected": len(hostile),
        "rejected_attack_labels": hostile,
        "certificate_sha256": sha256(CERTIFICATE),
        "producer_sha256": sha256(PRODUCER),
        "status": "PASS",
    }
    return {"schema": VERIFICATION_SCHEMA, "result": verification, "result_sha256": digest(verification)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--precision", type=int, default=VERIFIER_PRECISION_BITS)
    args = parser.parse_args()
    print(json.dumps(verify(args.precision), sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
