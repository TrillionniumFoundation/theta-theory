#!/usr/bin/env python3
"""Independent high-precision verifier for the Round112 two-sided root sheets.

This verifier does not import the producer.  It reconstructs the eight rays,
re-evaluates both sheet equations, and checks all root, chart, and flight
margins at higher precision.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
from collections import defaultdict
from dataclasses import replace
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from flint import arb, ctx

import cm2_gate25_physical_return_core_registry_cert as core_cert
from cm2_round76_r2_numeric_fields_generator import Jet, aq, center, interval, normal


HERE = Path(__file__).resolve().parent
CERTIFICATE = HERE / "cm2-round112-rank3-double-grazing-two-sided-root-sheet-2026-07-23.json"
PRODUCER = HERE / "cm2_round112_rank3_double_grazing_two_sided_root_sheet.py"
ROUND87 = HERE / "cm2-round87-rank3-port-event-continuation-2026-07-22.json"
ROUND94 = HERE / "cm2-round94-rank3-adjacent-chart-transfer-2026-07-22.json"
ROUND99 = HERE / "cm2-round99-rank3-registered-port-candidate-audit-2026-07-22.json"
ROUND100 = HERE / "cm2-round100-rank3-immutable-interior-gap-closure-2026-07-22.json"
PINS = {
    ROUND87.name: "f63f5d627def35f87dd3dfac075f8ecc0e8a5adfa725ddbe0eb692a39b54393b",
    ROUND94.name: "915f7c18d896d92116ab3f4346a5853c09fef2d3226a1f5429a7c19bca948ee3",
    ROUND99.name: "e1f0ea00d48e9eae553d5bb24ce140d27f696fd071cb19270e023263aac32f5e",
    ROUND100.name: "097849bf3da9d34a83ce9693ca68093ed2de7460cc51dcb26ce484c589f278d6",
    "cm2_gate25_physical_return_core_registry_cert.py": "2da58e5fb5fe030023d6fade7252ec67d0e494708b32d1e32b3ce545e2052fdb",
    "cm2_round76_r2_numeric_fields_generator.py": "96facebedf899d98d274f8a8c036fa8f02d1c34512933a587f7e581df174aadf",
    "cm2_round79_tangency_intersection_generator.py": "971f918ca1ed23bd081adf3b233d578e750b61231b20113327f221b40b890ed7",
}
EXPECTED_PRODUCER_SHA256 = "ccdfeebfa14fdaa466a67b79269145b2a36076b7027f2bac0a9c5daa030b5e3f"
EXPECTED_CERTIFICATE_SHA256 = "94a54ddbf31518cfc2a93b105d66337111f2b950be894f126e7b9c042e6b02e5"
CERTIFICATE_SCHEMA = "cm2.round112.rank3-double-grazing-two-sided-root-sheet.v1"
VERIFICATION_SCHEMA = "cm2.round112.rank3-double-grazing-two-sided-root-sheet-verification.v1"
VERIFIER_PRECISION_BITS = 768
WIDTH = Q(1, 16384)
T_RADIUS_MULTIPLIER = 8
NUMBER = re.compile(r"([+-]?[0-9]+(?:\.[0-9]+)?(?:e[+-]?[0-9]+)?)")
RESULT_KEYS = frozenset({
    "admissible_future_homogeneity_start_index",
    "boundary_ownership_schema_sha256",
    "bypass_actual_owner_homogeneity_schema_installed",
    "bypass_normal_coordinate_outer_boundary",
    "bypass_root_equation",
    "certified_bypass_root_sheet_count",
    "certified_hit_root_sheet_count",
    "certified_two_sided_sheet_row_count",
    "classical_squared_coordinate_jacobian_nonclaim",
    "core_transversality_interface",
    "directed_rounded_exact_angle_boundary_enclosure",
    "enclosing_rational_coordinate_width",
    "exact_angle_strip_template",
    "exact_source_and_hit_angle_subbox_contained_in_rational_enclosing_box",
    "exact_source_and_hit_angle_subbox_outer_boundary_expression",
    "first_second_owner_ordering_installed",
    "future_hit_product_child_index_schema",
    "gate5_actual_child_field_count",
    "half_open_boundary_ownership_schema",
    "hit_root_equation",
    "homogeneity_tail_theorem_installed",
    "input_corrected_source_grazing_corner_count",
    "official_word_or_canonical_child_installed",
    "precision_bits",
    "sheet_rows",
    "sheet_rows_sha256",
    "source_root_coordinate",
    "stored_enclosure_outward_padding",
    "stored_angle_boundary_outward_padding",
    "strict_nonclaims",
    "strict_scope",
    "t_radius_multiplier",
    "third_bypass_root_coordinate",
    "third_hit_root_coordinate",
    "upstream_pins",
    "whole_57_candidate_order_installed",
    "whole_trace_collar_installed",
})
ROW_KEYS = frozenset({
    "actual_next_owner_installed",
    "blown_up_jacobian_abs_strict_lower_bound",
    "blown_up_jacobian_coordinate_convention",
    "blown_up_jacobian_determinant_enclosure",
    "blown_up_jacobian_determinant_identity",
    "blown_up_jacobian_determinant_sign",
    "branch_key",
    "corner_index",
    "corner_root_endpoint_signs",
    "corner_root_t_bracket",
    "designated_third_conclusion",
    "designated_third_hit_geometry_installed",
    "designated_third_transverse_enclosure",
    "designated_third_transverse_sign_sigma3",
    "designated_third_whole_line_miss_interior_installed",
    "enclosing_parameter_box",
    "exterior_port_id",
    "first_chart_dominance_margin",
    "first_chart_signed_component_margin",
    "first_outgoing_chart",
    "path_margin_evidence",
    "projective_end",
    "root_bisection_depth",
    "root_equation",
    "second_chart_dominance_margin",
    "second_chart_signed_component_margin",
    "second_outgoing_chart",
    "selected_collision_lift_sequence_and_designated_third",
    "sheet_id",
    "sheet_index",
    "sheet_kind",
    "sheet_status",
    "source_adjacent_chart_squared_dominance_margin",
    "source_chart",
    "source_grazing_sign_sigma0",
    "squared_source_grazing_coordinate_status",
    "t_lower_face_equation_enclosure",
    "t_lower_face_equation_sign",
    "t_upper_face_equation_enclosure",
    "t_upper_face_equation_sign",
    "tight_round94_grazing_parameter_bracket",
    "uniform_abs_dc0_strict_lower_bound",
    "uniform_abs_dt_strict_lower_bound",
    "uniform_dc0_enclosure",
    "uniform_dc0_sign",
    "uniform_dt_enclosure",
    "uniform_dt_sign",
    "uniform_dthird_root_coordinate_enclosure",
})
EXPECTED_SCOPE = (
    "sixteen local root sheets (eight HIT and eight BYPASS) as positive-width manifolds with corners in "
    "(c0,c3) or (c0,b3), with fixed selected-collision lift geometry, source/selected chart and flight "
    "margins, and directed-rounded exact source/HIT angle subboxes"
)
EXPECTED_NONCLAIMS = [
    "the local endpoint root sheets are not whole trace collars",
    "the admissible double-index strip schema is not an installed countable homogeneity-tail theorem",
    "b3 is an analytic miss-side normal coordinate, not a collision-angle homogeneity coordinate",
    "neither HIT nor BYPASS installs an actual next owner; BYPASS proves only a designated-target whole-line miss for b3>0",
    "selected first/second collision lifts are not complete first/second owner-ordering certificates",
    "no whole-box 57-candidate ordering, official word, canonical child, or Gate5 field is installed",
    "this certificate does not repair the Round101 seam-to-grazing one-dimensional chain or the Round102 face quotient",
    "the rational enclosing width is certified but not claimed optimal",
]
EXPECTED_BOUNDARY_SCHEMA = [
    {"condition": "c0>0 and c3>0", "index_domain": "j,k>=128", "stratum": "HIT_INTERIOR_TEMPLATE"},
    {"condition": "c0=0 and c3>0", "index_domain": "k>=128", "stratum": "SOURCE_GRAZING_EDGE_TEMPLATE"},
    {"condition": "c0>0 and c3=0", "index_domain": "j>=128", "stratum": "THIRD_GRAZING_EDGE_TEMPLATE"},
    {"condition": "c0=0 and c3=0", "index_domain": "single corner", "stratum": "DOUBLE_GRAZING_CORNER"},
]


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
    return json.loads(
        path.read_text(),
        object_pairs_hook=strict_pairs,
        parse_constant=reject_nonfinite,
    )


def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def contract_bounds(stored: Any) -> tuple[arb, arb]:
    if not isinstance(stored, list) or len(stored) != 2 or not all(isinstance(item, str) for item in stored):
        raise RuntimeError("malformed stored enclosure")
    try:
        lower, upper = arb(stored[0]), arb(stored[1])
    except (TypeError, ValueError) as exc:
        raise RuntimeError("unparsed stored enclosure") from exc
    if not bool(lower < upper):
        raise RuntimeError("nonpositive stored enclosure width")
    return lower, upper


def enclosure_has_sign(stored: Any, sign: int) -> bool:
    lower, upper = contract_bounds(stored)
    return bool(lower > 0) if sign == 1 else bool(upper < 0) if sign == -1 else False


def validate_closed_contract(document: dict[str, Any]) -> dict[str, Any]:
    if set(document) != {"schema", "result", "result_sha256"}:
        raise RuntimeError("non-closed certificate envelope")
    if document["schema"] != CERTIFICATE_SCHEMA:
        raise RuntimeError("certificate schema mismatch")
    result = document["result"]
    if set(result) != RESULT_KEYS:
        raise RuntimeError("non-closed result schema")
    if document["result_sha256"] != digest(result):
        raise RuntimeError("certificate result digest mismatch")
    if result["sheet_rows_sha256"] != digest(result["sheet_rows"]):
        raise RuntimeError("sheet-row digest mismatch")
    if result["boundary_ownership_schema_sha256"] != digest(result["half_open_boundary_ownership_schema"]):
        raise RuntimeError("boundary-schema digest mismatch")
    if result["precision_bits"] != 512 or result["upstream_pins"] != PINS:
        raise RuntimeError("producer precision or upstream-pin contract")
    if result["strict_scope"] != EXPECTED_SCOPE or result["strict_nonclaims"] != EXPECTED_NONCLAIMS:
        raise RuntimeError("strict scope/nonclaim contract")
    if result["half_open_boundary_ownership_schema"] != EXPECTED_BOUNDARY_SCHEMA:
        raise RuntimeError("boundary template contract")
    if (
        result["core_transversality_interface"]
        != "det D_(c0,t)(c0,F_sheet)=partial_t_F_sheet, absolute value strictly above 3"
        or result["classical_squared_coordinate_jacobian_nonclaim"]
        != "Delta3 is not C1 as a function of g0=c0^2 at g0=0 because partial_c0_Delta3 is strictly nonzero"
    ):
        raise RuntimeError("blown-up/classical Jacobian contract")
    required_false = (
        "homogeneity_tail_theorem_installed",
        "bypass_actual_owner_homogeneity_schema_installed",
        "whole_57_candidate_order_installed",
        "first_second_owner_ordering_installed",
        "whole_trace_collar_installed",
        "official_word_or_canonical_child_installed",
    )
    if any(result[name] is not False for name in required_false):
        raise RuntimeError("forbidden promotion flag")
    if (
        result["input_corrected_source_grazing_corner_count"] != 8
        or result["certified_hit_root_sheet_count"] != 8
        or result["certified_bypass_root_sheet_count"] != 8
        or result["certified_two_sided_sheet_row_count"] != 16
        or result["enclosing_rational_coordinate_width"] != "1/16384"
        or result["stored_enclosure_outward_padding"] != "1/1000000"
        or result["stored_angle_boundary_outward_padding"] != "1/100000000000000000000"
        or result["t_radius_multiplier"] != 8
        or result["admissible_future_homogeneity_start_index"] != 128
        or result["exact_angle_strip_template"] != "sin((n+1)^-2)<c<=sin(n^-2)"
        or result["future_hit_product_child_index_schema"] != "(sigma0,sigma3,j,k), j,k>=128"
        or result["gate5_actual_child_field_count"] != 0
    ):
        raise RuntimeError("global accounting or schema contract")
    angle_lower, angle_upper = contract_bounds(result["directed_rounded_exact_angle_boundary_enclosure"])
    if not (bool(angle_lower > 0) and bool(angle_upper < aq(WIDTH))):
        raise RuntimeError("stored exact-angle enclosure contract")
    rows = result["sheet_rows"]
    if len(rows) != 16:
        raise RuntimeError("sheet-row count")
    cores = core_cert.physical_cores()
    for index, row in enumerate(rows):
        if set(row) != ROW_KEYS:
            raise RuntimeError(f"non-closed sheet-row schema: {index}")
        kind = "HIT" if index % 2 == 0 else "BYPASS"
        coordinate = "c3" if kind == "HIT" else "b3"
        branch = tuple(row["branch_key"])
        expected_sheet_id = "round112-" + kind.lower() + "-sheet:" + digest([
            row["exterior_port_id"], row["branch_key"], row["projective_end"]
        ])
        expected_sequence = [cores[branch[0]].target_id, branch[1], branch[2]]
        expected_equation = (
            "F_hit=Delta3-R3^2*c3^2" if kind == "HIT" else "F_bypass=Delta3+R3^2*b3^2"
        )
        expected_conclusion = (
            "DESIGNATED_THIRD_FORWARD_INTERSECTION_WITH_STRICT_POSITIVE_NEAR_FLIGHT_ON_ROOT_SHEET"
            if kind == "HIT"
            else "DESIGNATED_THIRD_WHOLE_LINE_MISS_FOR_b3_POSITIVE_INTERIOR__b3_ZERO_IS_TANGENCY"
        )
        if (
            row["sheet_index"] != index
            or row["corner_index"] != index // 2
            or row["sheet_kind"] != kind
            or row["actual_next_owner_installed"] is not False
            or row["uniform_abs_dt_strict_lower_bound"] != "3"
            or row["uniform_abs_dc0_strict_lower_bound"] != "3"
            or row["blown_up_jacobian_abs_strict_lower_bound"] != "3"
            or row["blown_up_jacobian_coordinate_convention"] != "rows=(c0,F_sheet), columns=(c0,t)"
            or row["blown_up_jacobian_determinant_identity"] != "det=partial_t_F_sheet"
            or row["sheet_id"] != expected_sheet_id
            or row["selected_collision_lift_sequence_and_designated_third"] != expected_sequence
            or row["root_equation"] != expected_equation
            or row["designated_third_conclusion"] != expected_conclusion
            or row["sheet_status"] != f"UNIQUE_POSITIVE_WIDTH_{kind}_ROOT_SHEET_IN_ENCLOSING_BOX"
            or "NOT_A_C1_REPLACEMENT" not in row["squared_source_grazing_coordinate_status"]
            or set(row["enclosing_parameter_box"]) != {"t", "c0", coordinate}
            or set(row["path_margin_evidence"]) != (
                {
                    "first_discriminant", "first_flight", "first_c_square",
                    "second_discriminant", "second_flight", "second_c_square",
                    "third_longitudinal", "third_hit_near_flight",
                }
                if kind == "HIT"
                else {
                    "first_discriminant", "first_flight", "first_c_square",
                    "second_discriminant", "second_flight", "second_c_square",
                    "third_longitudinal",
                }
            )
            or any(set(evidence) != {"sign", "enclosure"} or evidence["sign"] != 1 for evidence in row["path_margin_evidence"].values())
        ):
            raise RuntimeError(f"sheet-row semantic contract: {index}")
        if row["blown_up_jacobian_determinant_enclosure"] != row["uniform_dt_enclosure"]:
            raise RuntimeError(f"determinant/dt enclosure identity: {index}")
        signed_enclosures = (
            (row["t_lower_face_equation_enclosure"], row["t_lower_face_equation_sign"]),
            (row["t_upper_face_equation_enclosure"], row["t_upper_face_equation_sign"]),
            (row["uniform_dt_enclosure"], row["uniform_dt_sign"]),
            (row["uniform_dc0_enclosure"], row["uniform_dc0_sign"]),
            (row["blown_up_jacobian_determinant_enclosure"], row["blown_up_jacobian_determinant_sign"]),
            (row["designated_third_transverse_enclosure"], row["designated_third_transverse_sign_sigma3"]),
        )
        if any(sign not in (-1, 1) or not enclosure_has_sign(enclosure, sign) for enclosure, sign in signed_enclosures):
            raise RuntimeError(f"stored signed enclosure contract: {index}")
        for field in (
            "source_adjacent_chart_squared_dominance_margin",
            "first_chart_signed_component_margin",
            "first_chart_dominance_margin",
            "second_chart_signed_component_margin",
            "second_chart_dominance_margin",
        ):
            if not enclosure_has_sign(row[field], 1):
                raise RuntimeError(f"stored positive enclosure contract: {field}/{index}")
        contract_bounds(row["uniform_dthird_root_coordinate_enclosure"])
        for name, evidence in row["path_margin_evidence"].items():
            if not enclosure_has_sign(evidence["enclosure"], 1):
                raise RuntimeError(f"stored path enclosure contract: {name}/{index}")
        if kind == "HIT":
            if (
                row["designated_third_hit_geometry_installed"] is not True
                or row["designated_third_whole_line_miss_interior_installed"] is not False
                or "Delta3-R3^2*c3^2" not in row["root_equation"]
            ):
                raise RuntimeError(f"HIT contract: {index}")
        elif (
            row["designated_third_hit_geometry_installed"] is not False
            or row["designated_third_whole_line_miss_interior_installed"] is not True
            or "Delta3+R3^2*b3^2" not in row["root_equation"]
            or "b3_ZERO_IS_TANGENCY" not in row["designated_third_conclusion"]
        ):
            raise RuntimeError(f"BYPASS contract: {index}")
    return result


def resign_mutation(document: dict[str, Any]) -> None:
    result = document["result"]
    if "sheet_rows" in result:
        result["sheet_rows_sha256"] = digest(result["sheet_rows"])
    if "half_open_boundary_ownership_schema" in result:
        result["boundary_ownership_schema_sha256"] = digest(result["half_open_boundary_ownership_schema"])
    document["result_sha256"] = digest(result)


def set_nested(document: dict[str, Any], path: tuple[Any, ...], value: Any) -> None:
    target: Any = document
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = value


def hostile_contract_self_test(document: dict[str, Any]) -> list[str]:
    attacks: list[tuple[str, tuple[Any, ...], Any]] = [
        ("actual_next_owner_true", ("result", "sheet_rows", 0, "actual_next_owner_installed"), True),
        ("whole_57_order_true", ("result", "whole_57_candidate_order_installed"), True),
        ("bypass_miss_false", ("result", "sheet_rows", 1, "designated_third_whole_line_miss_interior_installed"), False),
        ("dt_lower_zero", ("result", "sheet_rows", 0, "uniform_abs_dt_strict_lower_bound"), "0"),
        (
            "classical_c1_claim",
            ("result", "classical_squared_coordinate_jacobian_nonclaim"),
            "Delta3 is C1 in g0 and has a classical nonzero Jacobian",
        ),
        ("certificate_precision_640", ("result", "precision_bits"), 640),
        ("forged_sheet_id", ("result", "sheet_rows", 0, "sheet_id"), "forged-sheet"),
        ("forged_selected_sequence", ("result", "sheet_rows", 0, "selected_collision_lift_sequence_and_designated_third"), ["forged"]),
        ("forged_hit_conclusion", ("result", "sheet_rows", 0, "designated_third_conclusion"), "ACTUAL_NEXT_OWNER_INSTALLED"),
        ("stored_dt_enclosure_false", ("result", "sheet_rows", 0, "uniform_dt_enclosure"), ["999", "1000"]),
        (
            "stored_path_enclosure_negative",
            ("result", "sheet_rows", 0, "path_margin_evidence", "first_flight", "enclosure"),
            ["-2", "-1"],
        ),
        (
            "stored_angle_enclosure_false",
            ("result", "directed_rounded_exact_angle_boundary_enclosure"),
            ["999", "1000"],
        ),
        (
            "forged_boundary_schema",
            ("result", "half_open_boundary_ownership_schema", 0, "stratum"),
            "ACTUAL_CANONICAL_CHILD",
        ),
    ]
    rejected: list[str] = []
    for label, path, value in attacks:
        mutant = copy.deepcopy(document)
        set_nested(mutant, path, value)
        resign_mutation(mutant)
        try:
            validate_closed_contract(mutant)
        except (KeyError, TypeError, ValueError, RuntimeError):
            rejected.append(label)
        else:
            raise RuntimeError(f"hostile semantic mutation accepted: {label}")
    for label, location in (
        ("unknown_row_key", ("result", "sheet_rows", 0)),
        ("unknown_result_key", ("result",)),
        ("unknown_envelope_key", ()),
    ):
        mutant = copy.deepcopy(document)
        target: Any = mutant
        for key in location:
            target = target[key]
        target["hostile_unknown_key"] = True
        resign_mutation(mutant)
        try:
            validate_closed_contract(mutant)
        except (KeyError, TypeError, ValueError, RuntimeError):
            rejected.append(label)
        else:
            raise RuntimeError(f"hostile unknown-key mutation accepted: {label}")
    hostile_json = {
        "duplicate_json_key": '{"x":1,"x":2}',
        "nan_json_number": '{"x":NaN}',
        "infinity_json_number": '{"x":Infinity}',
    }
    for label, text in hostile_json.items():
        try:
            json.loads(text, object_pairs_hook=strict_pairs, parse_constant=reject_nonfinite)
        except (TypeError, ValueError, RuntimeError):
            rejected.append(label)
        else:
            raise RuntimeError(f"hostile JSON accepted: {label}")
    return rejected


def strict_sign(value: arb) -> int:
    if bool(value > 0):
        return 1
    if bool(value < 0):
        return -1
    return 0


def stored_encloses(stored: Any, recomputed: arb) -> bool:
    if not isinstance(stored, list) or len(stored) != 2 or not all(isinstance(item, str) for item in stored):
        return False
    try:
        lower = arb(stored[0])
        upper = arb(stored[1])
    except (TypeError, ValueError):
        return False
    return bool(recomputed > lower) and bool(recomputed < upper)


def radius(target: str) -> Q:
    return Q(9, 25) if target[0] == "G" else Q(4, 25)


def center_number(text: str) -> Q:
    match = NUMBER.search(text)
    if match is None:
        raise RuntimeError(f"unparsed enclosure: {text}")
    return Q(match.group(1))


def branch_key(row: dict[str, Any]) -> tuple[int, str, str, int]:
    return (
        row["source_core_index"],
        row["second_selected_target_id"],
        row["third_candidate_id"],
        row["event_equation_evidence"]["signed_transverse_tangency_factor_sign"],
    )


def reconstruct_rays() -> list[tuple[tuple[int, str, str, int], str, str]]:
    events = load_json(ROUND87)["result"]["port_event_rows"]
    by_id = {row["registered_port_id"]: row for row in events}
    corrected_ids = load_json(ROUND99)["result"]["corrected_locally_physical_registered_port_ids"]
    corrected = {port_id: by_id[port_id] for port_id in corrected_ids}
    caps = {
        (tuple(row["branch_key"]), row["projective_end"])
        for row in load_json(ROUND100)["result"]["source_cap_rows"]
    }
    grouped: defaultdict[tuple[int, str, str, int], list[str]] = defaultdict(list)
    for port_id, event in corrected.items():
        grouped[branch_key(event)].append(port_id)
    rays = []
    for branch, port_ids in sorted(grouped.items()):
        port_ids.sort(key=lambda port_id: center_number(
            corrected[port_id]["event_equation_evidence"]["projective_q_enclosure"]
        ))
        for side, port_id in (
            ("LEFT_PROJECTIVE_END", port_ids[0]),
            ("RIGHT_PROJECTIVE_END", port_ids[-1]),
        ):
            if (branch, side) not in caps:
                rays.append((branch, side, port_id))
    if len(rays) != 8:
        raise RuntimeError("independent corrected-ray accounting")
    return rays


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
        "discriminant": discriminant,
        "flight": flight,
    }


def evaluate_sheet(
    source: Any,
    branch: tuple[int, str, str, int],
    source_sign: int,
    sheet_kind: str,
    t0: Q,
    t1: Q,
    c00: Q,
    c01: Q,
    z0: Q,
    z1: Q,
) -> dict[str, Jet]:
    t = Jet.variable(interval(t0, t1), 0)
    c0 = Jet.variable(interval(c00, c01), 1)
    z3 = Jet.variable(interval(z0, z1), 2)
    zero = Jet(arb(0))
    nx0, ny0 = normal(source.chart_id.split(":")[1], t)
    p0 = source_sign * (arb(1) - c0 * c0).sqrt()
    ux0 = c0 * nx0 - p0 * ny0
    uy0 = c0 * ny0 + p0 * nx0
    source_x, source_y = center(f"{source.source}[0,0]", zero)
    point_x = source_x + aq(radius(source.source)) * nx0
    point_y = source_y + aq(radius(source.source)) * ny0

    target1_x, target1_y = center(source.target_id, zero)
    first = collision(point_x, point_y, ux0, uy0, target1_x, target1_y, radius(source.target_id))
    c1_square = arb(1) - first["momentum"] * first["momentum"]
    c1 = c1_square.sqrt()
    ux1 = c1 * first["normal_x"] - first["momentum"] * first["normal_y"]
    uy1 = c1 * first["normal_y"] + first["momentum"] * first["normal_x"]

    target2_x, target2_y = center(branch[1], zero)
    second = collision(
        first["hit_x"], first["hit_y"], ux1, uy1,
        target2_x, target2_y, radius(branch[1]),
    )
    c2_square = arb(1) - second["momentum"] * second["momentum"]
    c2 = c2_square.sqrt()
    ux2 = c2 * second["normal_x"] - second["momentum"] * second["normal_y"]
    uy2 = c2 * second["normal_y"] + second["momentum"] * second["normal_x"]

    candidate_x, candidate_y = center(branch[2], zero)
    dx, dy = candidate_x - second["hit_x"], candidate_y - second["hit_y"]
    longitudinal3 = ux2 * dx + uy2 * dy
    transverse3 = -uy2 * dx + ux2 * dy
    r3 = aq(radius(branch[2]))
    delta3 = r3 * r3 - transverse3 * transverse3
    square_term = r3 * r3 * z3 * z3
    equation = delta3 - square_term if sheet_kind == "HIT" else delta3 + square_term
    return {
        "equation": equation,
        "third_transverse": transverse3,
        "third_longitudinal": longitudinal3,
        "third_hit_near_flight": longitudinal3 - r3 * z3,
        "first_discriminant": first["discriminant"],
        "first_flight": first["flight"],
        "first_c_square": c1_square,
        "first_normal_x": first["normal_x"],
        "first_normal_y": first["normal_y"],
        "second_discriminant": second["discriminant"],
        "second_flight": second["flight"],
        "second_c_square": c2_square,
        "second_normal_x": second["normal_x"],
        "second_normal_y": second["normal_y"],
    }


def chart_evidence(normal_x: Jet, normal_y: Jet) -> tuple[str, arb, arb] | None:
    nx, ny = normal_x.value, normal_y.value
    ax, ay = abs(nx), abs(ny)
    if bool(ax > ay):
        if bool(nx > 0):
            return "E", nx, ax - ay
        if bool(nx < 0):
            return "W", -nx, ax - ay
    if bool(ay > ax):
        if bool(ny > 0):
            return "N", ny, ay - ax
        if bool(ny < 0):
            return "S", -ny, ay - ax
    return None


def chart(normal_x: Jet, normal_y: Jet) -> str | None:
    evidence = chart_evidence(normal_x, normal_y)
    return None if evidence is None else evidence[0]


def verify(precision_bits: int = VERIFIER_PRECISION_BITS) -> dict[str, Any]:
    ctx.prec = precision_bits
    for name, expected in PINS.items():
        if sha256(HERE / name) != expected:
            raise RuntimeError(f"upstream pin mismatch: {name}")
    if sha256(PRODUCER) != EXPECTED_PRODUCER_SHA256:
        raise RuntimeError("producer source pin mismatch")
    if sha256(CERTIFICATE) != EXPECTED_CERTIFICATE_SHA256:
        raise RuntimeError("certificate byte pin mismatch")
    document = load_json(CERTIFICATE)
    result = validate_closed_contract(document)

    rays = reconstruct_rays()
    transfers = {
        row["exterior_port_id"]: row
        for row in load_json(ROUND94)["result"]["transfer_rows"]
    }
    cores = core_cert.physical_cores()
    rows = result["sheet_rows"]
    if len(rows) != 16:
        raise RuntimeError("sheet-row count")
    for sheet_index, row in enumerate(rows):
        corner_index = sheet_index // 2
        expected_kind = "HIT" if sheet_index % 2 == 0 else "BYPASS"
        branch, side, port_id = rays[corner_index]
        transfer = transfers[port_id]
        base_source = cores[branch[0]]
        source = replace(base_source, chart_id=f"{base_source.source}:{transfer['adjacent_source_chart']}")
        source_sign = 1 if center_number(transfer["transferred_inner_p_enclosure"]) > 0 else -1
        expected_sheet_id = "round112-" + expected_kind.lower() + "-sheet:" + digest([port_id, list(branch), side])
        expected_equation = (
            "F_hit=Delta3-R3^2*c3^2"
            if expected_kind == "HIT"
            else "F_bypass=Delta3+R3^2*b3^2"
        )
        expected_conclusion = (
            "DESIGNATED_THIRD_FORWARD_INTERSECTION_WITH_STRICT_POSITIVE_NEAR_FLIGHT_ON_ROOT_SHEET"
            if expected_kind == "HIT"
            else "DESIGNATED_THIRD_WHOLE_LINE_MISS_FOR_b3_POSITIVE_INTERIOR__b3_ZERO_IS_TANGENCY"
        )
        if (
            row["sheet_index"] != sheet_index
            or row["corner_index"] != corner_index
            or row["sheet_kind"] != expected_kind
            or row["exterior_port_id"] != port_id
            or tuple(row["branch_key"]) != branch
            or row["projective_end"] != side
            or row["source_chart"] != source.chart_id
            or row["source_grazing_sign_sigma0"] != source_sign
            or row["designated_third_transverse_sign_sigma3"] != branch[3]
            or row["tight_round94_grazing_parameter_bracket"] != transfer["transferred_grazing_parameter_bracket"]
            or row["root_bisection_depth"] != 160
            or row["actual_next_owner_installed"] is not False
            or row["sheet_id"] != expected_sheet_id
            or row["root_equation"] != expected_equation
            or row["designated_third_conclusion"] != expected_conclusion
            or row["sheet_status"] != f"UNIQUE_POSITIVE_WIDTH_{expected_kind}_ROOT_SHEET_IN_ENCLOSING_BOX"
            or row["selected_collision_lift_sequence_and_designated_third"] != [source.target_id, branch[1], branch[2]]
        ):
            raise RuntimeError(f"sheet identity mismatch: {sheet_index}")

        root_lower, root_upper = map(Q, row["corner_root_t_bracket"])
        root_left = evaluate_sheet(source, branch, source_sign, "HIT", root_lower, root_lower, Q(0), Q(0), Q(0), Q(0))
        root_right = evaluate_sheet(source, branch, source_sign, "HIT", root_upper, root_upper, Q(0), Q(0), Q(0), Q(0))
        root_signs = [strict_sign(root_left["equation"].value), strict_sign(root_right["equation"].value)]
        if root_signs != row["corner_root_endpoint_signs"] or root_signs[0] * root_signs[1] != -1:
            raise RuntimeError(f"corner root bracket mismatch: {sheet_index}")

        box = row["enclosing_parameter_box"]
        coordinate = "c3" if expected_kind == "HIT" else "b3"
        if set(box) != {"t", "c0", coordinate}:
            raise RuntimeError(f"parameter-box keys: {sheet_index}")
        t_lower, t_upper = map(Q, box["t"])
        c0_lower, c0_upper = map(Q, box["c0"])
        z_lower, z_upper = map(Q, box[coordinate])
        if (
            t_lower != root_lower - T_RADIUS_MULTIPLIER * WIDTH
            or t_upper != root_upper + T_RADIUS_MULTIPLIER * WIDTH
            or (c0_lower, c0_upper) != (Q(0), WIDTH)
            or (z_lower, z_upper) != (Q(0), WIDTH)
        ):
            raise RuntimeError(f"parameter-box geometry: {sheet_index}")
        left = evaluate_sheet(source, branch, source_sign, expected_kind, t_lower, t_lower, c0_lower, c0_upper, z_lower, z_upper)
        right = evaluate_sheet(source, branch, source_sign, expected_kind, t_upper, t_upper, c0_lower, c0_upper, z_lower, z_upper)
        full = evaluate_sheet(source, branch, source_sign, expected_kind, t_lower, t_upper, c0_lower, c0_upper, z_lower, z_upper)
        face_signs = [strict_sign(left["equation"].value), strict_sign(right["equation"].value)]
        dt_sign = strict_sign(full["equation"].gradient[0])
        dc0_sign = strict_sign(full["equation"].gradient[1])
        if (
            face_signs != [row["t_lower_face_equation_sign"], row["t_upper_face_equation_sign"]]
            or face_signs != [-dt_sign, dt_sign]
            or dt_sign != row["uniform_dt_sign"]
            or dc0_sign != row["uniform_dc0_sign"]
            or dc0_sign != -1
            or not bool(abs(full["equation"].gradient[0]) > aq(Q(3)))
            or not bool(-full["equation"].gradient[1] > aq(Q(3)))
            or row["uniform_abs_dt_strict_lower_bound"] != "3"
            or row["uniform_abs_dc0_strict_lower_bound"] != "3"
            or row["blown_up_jacobian_coordinate_convention"] != "rows=(c0,F_sheet), columns=(c0,t)"
            or row["blown_up_jacobian_determinant_identity"] != "det=partial_t_F_sheet"
            or row["blown_up_jacobian_determinant_sign"] != dt_sign
            or row["blown_up_jacobian_abs_strict_lower_bound"] != "3"
            or "NOT_A_C1_REPLACEMENT" not in row["squared_source_grazing_coordinate_status"]
        ):
            raise RuntimeError(f"uniform IFT audit: {sheet_index}")
        source_t = interval(t_lower, t_upper)
        source_chart_margin = arb(1) - 2 * source_t * source_t
        if strict_sign(source_chart_margin) != 1:
            raise RuntimeError(f"source chart dominance: {sheet_index}")
        first_chart_data = chart_evidence(full["first_normal_x"], full["first_normal_y"])
        second_chart_data = chart_evidence(full["second_normal_x"], full["second_normal_y"])
        if first_chart_data is None or second_chart_data is None:
            raise RuntimeError(f"selected chart unresolved: {sheet_index}")
        first_chart, first_signed_margin, first_dominance_margin = first_chart_data
        second_chart, second_signed_margin, second_dominance_margin = second_chart_data
        if first_chart != row["first_outgoing_chart"] or second_chart != row["second_outgoing_chart"]:
            raise RuntimeError(f"selected chart mismatch: {sheet_index}")
        if strict_sign(full["third_transverse"].value) != branch[3]:
            raise RuntimeError(f"third transverse sign: {sheet_index}")
        stored_core_enclosures = {
            "t_lower_face_equation_enclosure": left["equation"].value,
            "t_upper_face_equation_enclosure": right["equation"].value,
            "uniform_dt_enclosure": full["equation"].gradient[0],
            "uniform_dc0_enclosure": full["equation"].gradient[1],
            "uniform_dthird_root_coordinate_enclosure": full["equation"].gradient[2],
            "blown_up_jacobian_determinant_enclosure": full["equation"].gradient[0],
            "source_adjacent_chart_squared_dominance_margin": source_chart_margin,
            "first_chart_signed_component_margin": first_signed_margin,
            "first_chart_dominance_margin": first_dominance_margin,
            "second_chart_signed_component_margin": second_signed_margin,
            "second_chart_dominance_margin": second_dominance_margin,
            "designated_third_transverse_enclosure": full["third_transverse"].value,
        }
        for field, recomputed in stored_core_enclosures.items():
            if not stored_encloses(row[field], recomputed):
                raise RuntimeError(f"stored enclosure does not contain 768-bit replay: {field}/{sheet_index}")
        common_margins = {
            "first_discriminant", "first_flight", "first_c_square",
            "second_discriminant", "second_flight", "second_c_square",
            "third_longitudinal",
        }
        expected_margins = common_margins | ({"third_hit_near_flight"} if expected_kind == "HIT" else set())
        if set(row["path_margin_evidence"]) != expected_margins:
            raise RuntimeError(f"path-margin keys: {sheet_index}")
        for name in expected_margins:
            if (
                row["path_margin_evidence"][name]["sign"] != 1
                or strict_sign(full[name].value) != 1
                or not stored_encloses(row["path_margin_evidence"][name]["enclosure"], full[name].value)
            ):
                raise RuntimeError(f"path margin {name}: {sheet_index}")
        if not bool(full["first_flight"].value < aq(Q(3))) or not bool(full["second_flight"].value < aq(Q(3))):
            raise RuntimeError(f"selected flight upper bound: {sheet_index}")
        if expected_kind == "HIT":
            if (
                row["designated_third_hit_geometry_installed"] is not True
                or row["designated_third_whole_line_miss_interior_installed"] is not False
                or "Delta3-R3^2*c3^2" not in row["root_equation"]
            ):
                raise RuntimeError(f"HIT semantics: {sheet_index}")
        else:
            if (
                row["designated_third_hit_geometry_installed"] is not False
                or row["designated_third_whole_line_miss_interior_installed"] is not True
                or "Delta3+R3^2*b3^2" not in row["root_equation"]
                or "b3_ZERO_IS_TANGENCY" not in row["designated_third_conclusion"]
            ):
                raise RuntimeError(f"BYPASS semantics: {sheet_index}")

    angle_argument = arb(1) / (128 * 128)
    angle_boundary = angle_argument.sin()
    if not (bool(angle_boundary > 0) and bool(angle_boundary < aq(WIDTH))):
        raise RuntimeError("exact angle boundary containment")
    if not stored_encloses(result["directed_rounded_exact_angle_boundary_enclosure"], angle_boundary):
        raise RuntimeError("stored angle-boundary enclosure does not contain 768-bit replay")
    required_false = (
        "homogeneity_tail_theorem_installed",
        "bypass_actual_owner_homogeneity_schema_installed",
        "whole_57_candidate_order_installed",
        "first_second_owner_ordering_installed",
        "whole_trace_collar_installed",
        "official_word_or_canonical_child_installed",
    )
    if any(result[name] is not False for name in required_false):
        raise RuntimeError("forbidden promotion flag")
    if (
        result["input_corrected_source_grazing_corner_count"] != 8
        or result["certified_hit_root_sheet_count"] != 8
        or result["certified_bypass_root_sheet_count"] != 8
        or result["certified_two_sided_sheet_row_count"] != 16
        or result["enclosing_rational_coordinate_width"] != "1/16384"
        or result["admissible_future_homogeneity_start_index"] != 128
        or result["gate5_actual_child_field_count"] != 0
        or "partial_t_F_sheet" not in result["core_transversality_interface"]
        or "not C1" not in result["classical_squared_coordinate_jacobian_nonclaim"]
    ):
        raise RuntimeError("global accounting or scope flag")

    rejected_hostile_mutations = hostile_contract_self_test(document)

    verification = {
        "certificate_byte_sha256": EXPECTED_CERTIFICATE_SHA256,
        "certificate_schema": CERTIFICATE_SCHEMA,
        "certificate_result_sha256": document["result_sha256"],
        "verifier_precision_bits": precision_bits,
        "independently_reconstructed_corner_count": 8,
        "independently_recomputed_hit_sheet_count": 8,
        "independently_recomputed_bypass_sheet_count": 8,
        "independently_recomputed_sheet_row_count": 16,
        "all_root_face_signs_and_uniform_dt_dc0_bounds": "VERIFIED",
        "all_source_selected_chart_and_flight_margins": "VERIFIED",
        "all_stored_core_enclosures_contain_high_precision_replay": "VERIFIED",
        "all_hit_near_flights": "VERIFIED_STRICTLY_POSITIVE",
        "all_bypass_designated_target_interior_misses": "VERIFIED_BY_ROOT_EQUATION_FOR_b3_POSITIVE",
        "actual_next_owner_or_candidate_order": "NOT_INSTALLED",
        "exact_directed_rounded_angle_subbox": "VERIFIED_CONTAINED",
        "producer_imported_by_verifier": False,
        "fail_closed_rejected_hostile_mutation_count": len(rejected_hostile_mutations),
        "fail_closed_rejected_hostile_mutations": rejected_hostile_mutations,
        "upstream_pins": PINS,
        "producer_source_sha256": EXPECTED_PRODUCER_SHA256,
        "verdict": "VERIFIED",
    }
    verification = json.loads(json.dumps(verification, sort_keys=True))
    return {
        "schema": VERIFICATION_SCHEMA,
        "result": verification,
        "result_sha256": digest(verification),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--precision-bits", type=int, default=VERIFIER_PRECISION_BITS)
    args = parser.parse_args()
    print(json.dumps(verify(args.precision_bits), sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
