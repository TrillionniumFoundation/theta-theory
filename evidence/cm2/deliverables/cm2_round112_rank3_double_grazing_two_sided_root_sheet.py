#!/usr/bin/env python3
"""Freeze HIT and BYPASS root sheets at eight source/third double grazings.

The analytic blow-up coordinates are

    p0 = sigma0 * sqrt(1-c0^2),
    F_hit(t,c0,c3)       = Delta3(t,c0) - R3^2*c3^2,
    F_bypass(t,c0,b3)    = Delta3(t,c0) + R3^2*b3^2.

The HIT side includes a positive actual third near-flight margin.  The BYPASS
side proves only that the designated third target is a whole-line miss for
b3>0; finding and ordering the actual next owner is deliberately left open.
"""
from __future__ import annotations

import argparse
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
from cm2_round79_tangency_intersection_generator import digest, strict_sign


HERE = Path(__file__).resolve().parent
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
SCHEMA = "cm2.round112.rank3-double-grazing-two-sided-root-sheet.v1"
PRECISION_BITS = 512
ROOT_BISECTION_DEPTH = 160
ENCLOSING_WIDTH = Q(1, 16384)
T_RADIUS_MULTIPLIER = 8
HOMOGENEITY_START_INDEX = 128
EVIDENCE_PADDING = Q(1, 10**6)
ANGLE_EVIDENCE_PADDING = Q(1, 10**20)
NUMBER = re.compile(r"([+-]?[0-9]+(?:\.[0-9]+)?(?:e[+-]?[0-9]+)?)")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def radius(target: str) -> Q:
    return Q(9, 25) if target[0] == "G" else Q(4, 25)


def arb_bounds(value: arb, rational_padding: Q = EVIDENCE_PADDING) -> list[str]:
    padding = aq(rational_padding)
    return [str(value.lower() - padding), str(value.upper() + padding)]


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


def corrected_rays() -> tuple[list[tuple[tuple[int, str, str, int], str, str]], dict[str, Any]]:
    events = json.loads(ROUND87.read_text())["result"]["port_event_rows"]
    by_id = {row["registered_port_id"]: row for row in events}
    corrected_ids = json.loads(ROUND99.read_text())["result"]["corrected_locally_physical_registered_port_ids"]
    corrected = {port_id: by_id[port_id] for port_id in corrected_ids}
    caps = {
        (tuple(row["branch_key"]), row["projective_end"])
        for row in json.loads(ROUND100.read_text())["result"]["source_cap_rows"]
    }
    grouped: defaultdict[tuple[int, str, str, int], list[str]] = defaultdict(list)
    for port_id, row in corrected.items():
        grouped[branch_key(row)].append(port_id)
    rays: list[tuple[tuple[int, str, str, int], str, str]] = []
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
        raise RuntimeError("corrected source-grazing ray count")
    return rays, corrected


def collision_diagnostic(
    point_x: Jet,
    point_y: Jet,
    velocity_x: Jet,
    velocity_y: Jet,
    target_x: Jet,
    target_y: Jet,
    target_radius: Q,
) -> dict[str, Jet]:
    radius_ball = aq(target_radius)
    dx, dy = target_x - point_x, target_y - point_y
    longitudinal = velocity_x * dx + velocity_y * dy
    transverse = -velocity_y * dx + velocity_x * dy
    discriminant = radius_ball * radius_ball - transverse * transverse
    radical = discriminant.sqrt()
    flight = longitudinal - radical
    hit_x, hit_y = point_x + flight * velocity_x, point_y + flight * velocity_y
    normal_x, normal_y = (hit_x - target_x) / radius_ball, (hit_y - target_y) / radius_ball
    momentum = transverse / radius_ball
    return {
        "hit_x": hit_x,
        "hit_y": hit_y,
        "normal_x": normal_x,
        "normal_y": normal_y,
        "momentum": momentum,
        "discriminant": discriminant,
        "flight": flight,
    }


def root_sheet_jet(
    source: Any,
    second_target: str,
    candidate: str,
    source_grazing_sign: int,
    sheet_kind: str,
    t0: Q,
    t1: Q,
    c00: Q,
    c01: Q,
    c30: Q,
    c31: Q,
) -> dict[str, Jet]:
    t = Jet.variable(interval(t0, t1), 0)
    c0 = Jet.variable(interval(c00, c01), 1)
    third_root_coordinate = Jet.variable(interval(c30, c31), 2)
    zero = Jet(arb(0))
    source_normal_x, source_normal_y = normal(source.chart_id.split(":")[1], t)
    source_p = source_grazing_sign * (arb(1) - c0 * c0).sqrt()
    velocity_x = c0 * source_normal_x - source_p * source_normal_y
    velocity_y = c0 * source_normal_y + source_p * source_normal_x
    source_x, source_y = center(f"{source.source}[0,0]", zero)
    point_x = source_x + aq(radius(source.source)) * source_normal_x
    point_y = source_y + aq(radius(source.source)) * source_normal_y

    first_x, first_y = center(source.target_id, zero)
    first = collision_diagnostic(
        point_x, point_y, velocity_x, velocity_y,
        first_x, first_y, radius(source.target_id),
    )
    first_c_square = arb(1) - first["momentum"] * first["momentum"]
    first_c = first_c_square.sqrt()
    outgoing1_x = first_c * first["normal_x"] - first["momentum"] * first["normal_y"]
    outgoing1_y = first_c * first["normal_y"] + first["momentum"] * first["normal_x"]

    second_x, second_y = center(second_target, zero)
    second = collision_diagnostic(
        first["hit_x"], first["hit_y"], outgoing1_x, outgoing1_y,
        second_x, second_y, radius(second_target),
    )
    second_c_square = arb(1) - second["momentum"] * second["momentum"]
    second_c = second_c_square.sqrt()
    outgoing2_x = second_c * second["normal_x"] - second["momentum"] * second["normal_y"]
    outgoing2_y = second_c * second["normal_y"] + second["momentum"] * second["normal_x"]

    candidate_x, candidate_y = center(candidate, zero)
    dx, dy = candidate_x - second["hit_x"], candidate_y - second["hit_y"]
    third_longitudinal = outgoing2_x * dx + outgoing2_y * dy
    third_transverse = -outgoing2_y * dx + outgoing2_x * dy
    r3 = aq(radius(candidate))
    delta3 = r3 * r3 - third_transverse * third_transverse
    third_square_term = r3 * r3 * third_root_coordinate * third_root_coordinate
    if sheet_kind == "HIT":
        equation = delta3 - third_square_term
    elif sheet_kind == "BYPASS":
        equation = delta3 + third_square_term
    else:
        raise ValueError(f"unknown sheet kind: {sheet_kind}")
    third_hit_near_flight = third_longitudinal - r3 * third_root_coordinate
    return {
        "equation": equation,
        "delta3": delta3,
        "third_longitudinal": third_longitudinal,
        "third_transverse": third_transverse,
        "third_hit_near_flight": third_hit_near_flight,
        "first_discriminant": first["discriminant"],
        "first_flight": first["flight"],
        "first_c_square": first_c_square,
        "first_normal_x": first["normal_x"],
        "first_normal_y": first["normal_y"],
        "second_discriminant": second["discriminant"],
        "second_flight": second["flight"],
        "second_c_square": second_c_square,
        "second_normal_x": second["normal_x"],
        "second_normal_y": second["normal_y"],
    }


def strict_chart(normal_x: Jet, normal_y: Jet) -> tuple[str, arb, arb] | None:
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


def point_value(source: Any, branch: tuple[int, str, str, int], source_sign: int, t: Q) -> arb:
    return root_sheet_jet(
        source, branch[1], branch[2], source_sign,
        "HIT",
        t, t, Q(0), Q(0), Q(0), Q(0),
    )["equation"].value


def isolate_root(source: Any, branch: tuple[int, str, str, int], source_sign: int, seed: Q) -> tuple[Q, Q, int, int]:
    step = Q(1, 10**12)
    for _ in range(30):
        lower, upper = seed - step, seed + step
        lower_sign = strict_sign(point_value(source, branch, source_sign, lower))
        upper_sign = strict_sign(point_value(source, branch, source_sign, upper))
        if lower_sign * upper_sign == -1:
            break
        step *= 2
    else:
        raise RuntimeError("corner root bracket not found")
    for _ in range(ROOT_BISECTION_DEPTH):
        middle = (lower + upper) / 2
        middle_sign = strict_sign(point_value(source, branch, source_sign, middle))
        if middle_sign == lower_sign:
            lower = middle
        elif middle_sign == upper_sign:
            upper = middle
        else:
            raise RuntimeError("corner root bisection indeterminate")
    return lower, upper, lower_sign, upper_sign


def positive_evidence(jet: dict[str, Jet], name: str) -> dict[str, Any]:
    value = jet[name].value
    if strict_sign(value) != 1:
        raise RuntimeError(f"nonpositive path margin: {name}")
    return {"sign": 1, "enclosure": arb_bounds(value)}


def build(precision_bits: int = PRECISION_BITS) -> dict[str, Any]:
    ctx.prec = precision_bits
    for name, expected in PINS.items():
        if sha256(HERE / name) != expected:
            raise RuntimeError(f"pin mismatch: {name}")
    rays, _ = corrected_rays()
    transfers = {
        row["exterior_port_id"]: row
        for row in json.loads(ROUND94.read_text())["result"]["transfer_rows"]
    }
    cores = core_cert.physical_cores()
    rows = []
    for corner_index, (branch, side, port_id) in enumerate(rays):
        transfer = transfers.get(port_id)
        if transfer is None or transfer["algebraic_transferred_terminal_event_type"] != "SOURCE_GRAZING":
            raise RuntimeError("missing tight algebraic source-grazing bracket")
        base_source = cores[branch[0]]
        source = replace(base_source, chart_id=f"{base_source.source}:{transfer['adjacent_source_chart']}")
        source_sign = 1 if center_number(transfer["transferred_inner_p_enclosure"]) > 0 else -1
        seed = center_number(transfer["transferred_inner_t_enclosure"])
        root_lower, root_upper, root_lower_sign, root_upper_sign = isolate_root(
            source, branch, source_sign, seed
        )
        t_lower = root_lower - T_RADIUS_MULTIPLIER * ENCLOSING_WIDTH
        t_upper = root_upper + T_RADIUS_MULTIPLIER * ENCLOSING_WIDTH
        for sheet_kind in ("HIT", "BYPASS"):
            third_coordinate = "c3" if sheet_kind == "HIT" else "b3"
            equation_text = (
                "F_hit=Delta3-R3^2*c3^2"
                if sheet_kind == "HIT"
                else "F_bypass=Delta3+R3^2*b3^2"
            )
            left = root_sheet_jet(
                source, branch[1], branch[2], source_sign, sheet_kind,
                t_lower, t_lower, Q(0), ENCLOSING_WIDTH, Q(0), ENCLOSING_WIDTH,
            )
            right = root_sheet_jet(
                source, branch[1], branch[2], source_sign, sheet_kind,
                t_upper, t_upper, Q(0), ENCLOSING_WIDTH, Q(0), ENCLOSING_WIDTH,
            )
            full = root_sheet_jet(
                source, branch[1], branch[2], source_sign, sheet_kind,
                t_lower, t_upper, Q(0), ENCLOSING_WIDTH, Q(0), ENCLOSING_WIDTH,
            )
            left_sign = strict_sign(left["equation"].value)
            right_sign = strict_sign(right["equation"].value)
            dt_sign = strict_sign(full["equation"].gradient[0])
            dc0_sign = strict_sign(full["equation"].gradient[1])
            transverse_sign = strict_sign(full["third_transverse"].value)
            first_chart = strict_chart(full["first_normal_x"], full["first_normal_y"])
            second_chart = strict_chart(full["second_normal_x"], full["second_normal_y"])
            source_t_ball = interval(t_lower, t_upper)
            source_chart_squared_dominance = arb(1) - 2 * source_t_ball * source_t_ball
            if (
                left_sign * right_sign != -1
                or dt_sign == 0
                or left_sign != -dt_sign
                or right_sign != dt_sign
                or dc0_sign != -1
                or transverse_sign != branch[3]
                or first_chart is None
                or second_chart is None
                or strict_sign(source_chart_squared_dominance) != 1
                or not bool(full["first_flight"].value < aq(Q(3)))
                or not bool(full["second_flight"].value < aq(Q(3)))
                or not bool(abs(full["equation"].gradient[0]) > aq(Q(3)))
                or not bool(-full["equation"].gradient[1] > aq(Q(3)))
            ):
                raise RuntimeError(f"uniform {sheet_kind} root-sheet audit failed")
            margin_names = [
                "first_discriminant", "first_flight", "first_c_square",
                "second_discriminant", "second_flight", "second_c_square",
                "third_longitudinal",
            ]
            if sheet_kind == "HIT":
                margin_names.append("third_hit_near_flight")
            path_margins = {name: positive_evidence(full, name) for name in margin_names}
            rows.append({
                "sheet_index": 2 * corner_index + (0 if sheet_kind == "HIT" else 1),
                "corner_index": corner_index,
                "sheet_kind": sheet_kind,
                "sheet_id": "round112-" + sheet_kind.lower() + "-sheet:" + digest([port_id, list(branch), side]),
                "exterior_port_id": port_id,
                "branch_key": list(branch),
                "projective_end": side,
                "source_chart": source.chart_id,
                "source_grazing_sign_sigma0": source_sign,
                "designated_third_transverse_sign_sigma3": transverse_sign,
                "selected_collision_lift_sequence_and_designated_third": [source.target_id, branch[1], branch[2]],
                "tight_round94_grazing_parameter_bracket": transfer["transferred_grazing_parameter_bracket"],
                "corner_root_t_bracket": [str(root_lower), str(root_upper)],
                "corner_root_endpoint_signs": [root_lower_sign, root_upper_sign],
                "root_bisection_depth": ROOT_BISECTION_DEPTH,
                "enclosing_parameter_box": {
                    "t": [str(t_lower), str(t_upper)],
                    "c0": ["0", str(ENCLOSING_WIDTH)],
                    third_coordinate: ["0", str(ENCLOSING_WIDTH)],
                },
                "root_equation": equation_text,
                "t_lower_face_equation_sign": left_sign,
                "t_lower_face_equation_enclosure": arb_bounds(left["equation"].value),
                "t_upper_face_equation_sign": right_sign,
                "t_upper_face_equation_enclosure": arb_bounds(right["equation"].value),
                "uniform_dt_sign": dt_sign,
                "uniform_dt_enclosure": arb_bounds(full["equation"].gradient[0]),
                "uniform_dc0_sign": dc0_sign,
                "uniform_dc0_enclosure": arb_bounds(full["equation"].gradient[1]),
                "uniform_dthird_root_coordinate_enclosure": arb_bounds(full["equation"].gradient[2]),
                "uniform_abs_dt_strict_lower_bound": "3",
                "uniform_abs_dc0_strict_lower_bound": "3",
                "blown_up_jacobian_coordinate_convention": "rows=(c0,F_sheet), columns=(c0,t)",
                "blown_up_jacobian_determinant_identity": "det=partial_t_F_sheet",
                "blown_up_jacobian_determinant_sign": dt_sign,
                "blown_up_jacobian_determinant_enclosure": arb_bounds(full["equation"].gradient[0]),
                "blown_up_jacobian_abs_strict_lower_bound": "3",
                "squared_source_grazing_coordinate_status": "g0=1-p0^2=c0^2_IS_NOT_A_C1_REPLACEMENT_AT_c0_ZERO_BECAUSE_partial_c0_F_IS_NONZERO",
                "source_adjacent_chart_squared_dominance_margin": arb_bounds(source_chart_squared_dominance),
                "first_outgoing_chart": first_chart[0],
                "first_chart_signed_component_margin": arb_bounds(first_chart[1]),
                "first_chart_dominance_margin": arb_bounds(first_chart[2]),
                "second_outgoing_chart": second_chart[0],
                "second_chart_signed_component_margin": arb_bounds(second_chart[1]),
                "second_chart_dominance_margin": arb_bounds(second_chart[2]),
                "designated_third_transverse_enclosure": arb_bounds(full["third_transverse"].value),
                "path_margin_evidence": path_margins,
                "designated_third_conclusion": (
                    "DESIGNATED_THIRD_FORWARD_INTERSECTION_WITH_STRICT_POSITIVE_NEAR_FLIGHT_ON_ROOT_SHEET"
                    if sheet_kind == "HIT"
                    else "DESIGNATED_THIRD_WHOLE_LINE_MISS_FOR_b3_POSITIVE_INTERIOR__b3_ZERO_IS_TANGENCY"
                ),
                "designated_third_hit_geometry_installed": sheet_kind == "HIT",
                "designated_third_whole_line_miss_interior_installed": sheet_kind == "BYPASS",
                "actual_next_owner_installed": False,
                "sheet_status": f"UNIQUE_POSITIVE_WIDTH_{sheet_kind}_ROOT_SHEET_IN_ENCLOSING_BOX",
            })

    strip_argument = arb(1) / (HOMOGENEITY_START_INDEX * HOMOGENEITY_START_INDEX)
    strip_boundary = strip_argument.sin()
    if not (bool(strip_boundary > 0) and bool(strip_boundary < aq(ENCLOSING_WIDTH))):
        raise RuntimeError("directed-rounded exact strip boundary containment")
    boundary_ownership_schema = [
        {"stratum": "HIT_INTERIOR_TEMPLATE", "condition": "c0>0 and c3>0", "index_domain": "j,k>=128"},
        {"stratum": "SOURCE_GRAZING_EDGE_TEMPLATE", "condition": "c0=0 and c3>0", "index_domain": "k>=128"},
        {"stratum": "THIRD_GRAZING_EDGE_TEMPLATE", "condition": "c0>0 and c3=0", "index_domain": "j>=128"},
        {"stratum": "DOUBLE_GRAZING_CORNER", "condition": "c0=0 and c3=0", "index_domain": "single corner"},
    ]
    result = {
        "precision_bits": precision_bits,
        "input_corrected_source_grazing_corner_count": len(rays),
        "certified_hit_root_sheet_count": sum(row["sheet_kind"] == "HIT" for row in rows),
        "certified_bypass_root_sheet_count": sum(row["sheet_kind"] == "BYPASS" for row in rows),
        "certified_two_sided_sheet_row_count": len(rows),
        "enclosing_rational_coordinate_width": str(ENCLOSING_WIDTH),
        "stored_enclosure_outward_padding": str(EVIDENCE_PADDING),
        "stored_angle_boundary_outward_padding": str(ANGLE_EVIDENCE_PADDING),
        "t_radius_multiplier": T_RADIUS_MULTIPLIER,
        "exact_source_and_hit_angle_subbox_outer_boundary_expression": "sin(128^-2)",
        "directed_rounded_exact_angle_boundary_enclosure": arb_bounds(strip_boundary, ANGLE_EVIDENCE_PADDING),
        "exact_source_and_hit_angle_subbox_contained_in_rational_enclosing_box": True,
        "bypass_normal_coordinate_outer_boundary": str(ENCLOSING_WIDTH),
        "source_root_coordinate": "c0=sqrt(1-p0^2), p0=sigma0*sqrt(1-c0^2)",
        "core_transversality_interface": "det D_(c0,t)(c0,F_sheet)=partial_t_F_sheet, absolute value strictly above 3",
        "classical_squared_coordinate_jacobian_nonclaim": "Delta3 is not C1 as a function of g0=c0^2 at g0=0 because partial_c0_Delta3 is strictly nonzero",
        "third_hit_root_coordinate": "c3=sqrt(Delta3)/R3 on Delta3>=0",
        "third_bypass_root_coordinate": "b3=sqrt(-Delta3)/R3 on Delta3<=0",
        "hit_root_equation": "Delta3-R3^2*c3^2=0",
        "bypass_root_equation": "Delta3+R3^2*b3^2=0",
        "admissible_future_homogeneity_start_index": HOMOGENEITY_START_INDEX,
        "exact_angle_strip_template": "sin((n+1)^-2)<c<=sin(n^-2)",
        "future_hit_product_child_index_schema": "(sigma0,sigma3,j,k), j,k>=128",
        "bypass_actual_owner_homogeneity_schema_installed": False,
        "half_open_boundary_ownership_schema": boundary_ownership_schema,
        "boundary_ownership_schema_sha256": digest(boundary_ownership_schema),
        "homogeneity_tail_theorem_installed": False,
        "whole_57_candidate_order_installed": False,
        "first_second_owner_ordering_installed": False,
        "whole_trace_collar_installed": False,
        "official_word_or_canonical_child_installed": False,
        "gate5_actual_child_field_count": 0,
        "sheet_rows": rows,
        "sheet_rows_sha256": digest(rows),
        "strict_scope": "sixteen local root sheets (eight HIT and eight BYPASS) as positive-width manifolds with corners in (c0,c3) or (c0,b3), with fixed selected-collision lift geometry, source/selected chart and flight margins, and directed-rounded exact source/HIT angle subboxes",
        "strict_nonclaims": [
            "the local endpoint root sheets are not whole trace collars",
            "the admissible double-index strip schema is not an installed countable homogeneity-tail theorem",
            "b3 is an analytic miss-side normal coordinate, not a collision-angle homogeneity coordinate",
            "neither HIT nor BYPASS installs an actual next owner; BYPASS proves only a designated-target whole-line miss for b3>0",
            "selected first/second collision lifts are not complete first/second owner-ordering certificates",
            "no whole-box 57-candidate ordering, official word, canonical child, or Gate5 field is installed",
            "this certificate does not repair the Round101 seam-to-grazing one-dimensional chain or the Round102 face quotient",
            "the rational enclosing width is certified but not claimed optimal",
        ],
        "upstream_pins": PINS,
    }
    if len(rays) != 8 or len(rows) != 16:
        raise RuntimeError("Round112 two-sided sheet accounting")
    result = json.loads(json.dumps(result, sort_keys=True))
    return {"schema": SCHEMA, "result": result, "result_sha256": digest(result)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--precision-bits", type=int, default=PRECISION_BITS)
    args = parser.parse_args()
    print(json.dumps(build(args.precision_bits), sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
