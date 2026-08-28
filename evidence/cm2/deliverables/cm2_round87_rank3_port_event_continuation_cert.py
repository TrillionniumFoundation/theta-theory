#!/usr/bin/env python3
"""Typed local continuation of every frozen non-source rank-three port.

The Round-85 port census exposed 3,212 roots on boundaries of registered box
unions.  A box-union boundary is not a physical endpoint.  This producer
isolates the unique discriminant root on every exposed segment, constructs a
strict positive-width implicit-function slab on the outward side, replays the
first two physical collisions, and types visibility of the nominated third
tangency against the complete translated candidate table.

The certificate is deliberately local.  It proves that every registered port
continues across its artificial union boundary, but it neither pairs ports nor
claims that the resulting registered arcs are complete physical faces.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import multiprocessing as mp
import sys
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from flint import arb, ctx

import cm2_gate25_physical_return_core_registry_cert as core_cert
import cm2_gate34_full_core_return_adaptive_frontier_cert as step1
import cm2_gate34_round29_q2_time3_anchor_registry_cert as time3
from cm2_round79_tangency_intersection_generator import aq, digest, strict_sign
from cm2_round80_time3_tangency_curve_generator import third_tangency_jet


HERE = Path(__file__).resolve().parent
FRONTIER = HERE / "cm2-round85-rank3-outward-port-continuation-frontier-2026-07-22.json"
FRONTIER_SOURCE = HERE / "cm2_round85_rank3_outward_port_continuation_frontier_cert.py"
FRONTIER_AUDIT = HERE / "cm2-round85-rank3-outward-port-continuation-frontier-audit-2026-07-22.json"
CORE_MANIFEST = HERE / "cm2-gate25-physical-return-core-registry-manifest-2026-07-16.json"
FRONTIER_SHA256 = "b202e432f390266b38d13a4c6c4a8710f9189493897612387bfa632603dd273f"
FRONTIER_SOURCE_SHA256 = "b68d13dc6ddec382858138928e46cfb2d7d856acc9180822ceab6b9f6ca06ebc"
FRONTIER_AUDIT_SHA256 = "7f6ef59e84d1ae4d7760517cfab1926d2d475438a9123c5f6ccba3e73be86698"
CORE_MANIFEST_SHA256 = "144f5516ada8b83ca07459582c8cdb07ba09db11ac18a90cff32c6396c6e5a42"
SCHEMA = "cm2.round87.rank3-port-event-continuation.v1"
PRECISION_BITS = 512
ROOT_BISECTION_DEPTH = 128
MINIMUM_NORMAL_DEPTH = 112
MAXIMUM_NORMAL_DEPTH = 192
GRID = 64
UNIFORM_SOURCE_CORE_MARGIN = Q(1, 100000)
EXPECTED_EVENT_HISTOGRAM = {
    "ALGEBRAIC_TANGENCY_OCCLUDED_BY_EARLIER_THIRD_OWNER__LOCAL_CONTINUATION": 855,
    "ALGEBRAIC_TANGENCY_STRICTLY_AFTER_TAU_MAX__LOCAL_CONTINUATION": 432,
    "ALGEBRAIC_TANGENCY_STRICTLY_BEHIND_SECOND__LOCAL_CONTINUATION": 980,
    "PHYSICAL_NEXT_TANGENCY__LOCAL_CONTINUATION": 945,
}
EXPECTED_COMPETITOR_CLASSIFICATION_HISTOGRAM = {
    "intersection_strictly_behind": 1481,
    "no_real_intersection": 81417,
    "strict_future_near_root": 3417,
}
EXPECTED_COMPETITOR_RELATION_HISTOGRAM = {
    "INTERSECTION_STRICTLY_BEHIND": 1481,
    "NO_REAL_INTERSECTION": 81417,
    "STRICTLY_AFTER_TANGENT_TARGET": 1509,
    "STRICTLY_BEFORE_TANGENT_TARGET": 1908,
}
EXECUTABLE_SOURCE_PINS = {
    "cm2_gate25_physical_return_core_registry_cert.py": "2da58e5fb5fe030023d6fade7252ec67d0e494708b32d1e32b3ce545e2052fdb",
    "cm2_gate34_full_core_return_adaptive_frontier_cert.py": "d18b234471b192282abf064684fa535cc99c205797399b268f052c0884063a24",
    "cm2_gate34_round26_q1_time2_frontier_cert.py": "18385fe423aeb38c4ea988f11b76293e573becf82c50e663030f17ae70430fc9",
    "cm2_gate34_round28_nonempty_adaptive_component_registry_cert.py": "b489f498cac2650a6456da0540d035b2cc9654a69f5dc0110db85933eecd12f6",
    "cm2_gate34_round29_q2_time3_anchor_registry_cert.py": "399ea86401e97d2679fb3f3f7a0a9328266d8d583e73fd5c5ed2bc811c14475b",
    "cm2_gate3_candidate_first_hit_cert.py": "6d224d74cda186a40ef9956d1dd6556d5a7b9f506d47c942427ceb66fd705bd2",
    "cm2_gate45_round27_q2_branch_payload_frontier_cert.py": "be96ada6c90e792b7abe556982c65b78dae051498b680ebad3267117f44078c9",
    "cm2_gate45_round28_q2_homogeneity_recut_cert.py": "1acf1072caa22b676ed7f579cd2a909f06c6b8249396a7be4cdaa9c37997cf64",
    "cm2_gate4_componentwise_global_growth_recovery_frontier_cert.py": "90b7f7a9c0f02c19a80a9679ff393818318675c378ff4c1f139985ae23f069e1",
    "cm2_gate5_return_word_three_norm_frontier_cert.py": "ddcc250f8700c6a695f96019d9f7824fe98636e20a67685fdc6a3cce77f6d695",
    "cm2_round76_r2_numeric_fields_generator.py": "96facebedf899d98d274f8a8c036fa8f02d1c34512933a587f7e581df174aadf",
    "cm2_round78_tangency_curve_generator.py": "cc9da9d607bbe19c54ffccfd4974b37eb96459f0c4ed9e70d7a68e732f625d85",
    "cm2_round79_tangency_intersection_generator.py": "971f918ca1ed23bd081adf3b233d578e750b61231b20113327f221b40b890ed7",
    "cm2_round80_time3_carrier_component_generator.py": "c978c10f0585e8001d02ca4a79c45d99e2fdc43a24b9b42142b4fba93bbfef6e",
    "cm2_round80_time3_tangency_curve_generator.py": "68d17d088e94a8d5b0b97a6518691e19da2560be7df7fcff32eacdfd367aa659",
}
WORK_CORES: tuple[Any, ...] = ()


def strict_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def reject_nonfinite(token: str) -> Any:
    raise ValueError(f"nonfinite JSON number: {token}")


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_frontier() -> dict[str, Any]:
    if file_sha256(FRONTIER) != FRONTIER_SHA256:
        raise RuntimeError("Round85 frontier byte pin mismatch")
    if file_sha256(FRONTIER_SOURCE) != FRONTIER_SOURCE_SHA256:
        raise RuntimeError("Round85 frontier source byte pin mismatch")
    if file_sha256(FRONTIER_AUDIT) != FRONTIER_AUDIT_SHA256:
        raise RuntimeError("Round85 frontier audit byte pin mismatch")
    if file_sha256(CORE_MANIFEST) != CORE_MANIFEST_SHA256:
        raise RuntimeError("Gate25 physical-core theorem byte pin mismatch")
    core_document = json.loads(
        CORE_MANIFEST.read_text(),
        object_pairs_hook=strict_pairs,
        parse_constant=reject_nonfinite,
    )
    if (
        core_document.get("schema") != "cm2.gate25.physical-return-core-registry.manifest.v1"
        or core_document.get("verdict", {}).get("positive_mass_physical_core_registry") != "CERTIFIED"
        or core_document.get("verdict", {}).get("physical_nonempty_return_key_lower_bound") != "CERTIFIED_AT_LEAST_24"
    ):
        raise RuntimeError("Gate25 physical-core theorem semantic mismatch")
    for name, expected in EXECUTABLE_SOURCE_PINS.items():
        if file_sha256(HERE / name) != expected:
            raise RuntimeError(f"executable source pin mismatch: {name}")
    document = json.loads(
        FRONTIER.read_text(),
        object_pairs_hook=strict_pairs,
        parse_constant=reject_nonfinite,
    )
    if set(document) != {"schema", "result", "result_sha256"}:
        raise RuntimeError("non-closed Round85 frontier document")
    if document["schema"] != "cm2.round85.rank3-outward-port-continuation-frontier.v1":
        raise RuntimeError("Round85 frontier schema mismatch")
    if document["result_sha256"] != digest(document["result"]):
        raise RuntimeError("Round85 frontier result digest mismatch")
    return document["result"]


def evaluate_point(
    source: Any, second: str, candidate: str,
    boundary_axis: str, fixed: Q, parameter: Q,
) -> Any:
    if boundary_axis == "p":
        return third_tangency_jet(
            source, second, candidate, fixed, fixed, parameter, parameter
        ).value
    return third_tangency_jet(
        source, second, candidate, parameter, parameter, fixed, fixed
    ).value


def isolate_root(source: Any, row: dict[str, Any]) -> tuple[Q, Q, int, int]:
    axis = row["boundary_axis"]
    fixed = Q(row["fixed_coordinate"])
    second = row["second_selected_target_id"]
    candidate = row["third_candidate_id"]
    lower, upper = map(Q, row["root_grid_isolation"]["isolated_root_bracket"])
    lower_sign, upper_sign = row["root_grid_isolation"]["isolated_endpoint_signs"]
    if lower_sign * upper_sign != -1:
        raise RuntimeError("input port lacks an opposite-sign root bracket")
    for _depth in range(ROOT_BISECTION_DEPTH):
        middle = (lower + upper) / 2
        middle_sign = strict_sign(evaluate_point(source, second, candidate, axis, fixed, middle))
        if middle_sign == 0:
            raise RuntimeError("indeterminate dyadic root bisection sign")
        if middle_sign == lower_sign:
            lower, lower_sign = middle, middle_sign
        else:
            upper, upper_sign = middle, middle_sign
    return lower, upper, lower_sign, upper_sign


def slab_box(
    source: Any, row: dict[str, Any],
    lower: Q, upper: Q, normal_depth: int,
) -> tuple[tuple[Q, Q, Q, Q], str, Q, int]:
    boundary_axis = row["boundary_axis"]
    normal_axis = "t" if boundary_axis == "p" else "p"
    fixed = Q(row["fixed_coordinate"])
    span = source.t1 - source.t0 if normal_axis == "t" else source.p1 - source.p0
    direction = -int(row["inside_side"])
    outer = fixed + direction * span / Q(GRID * (2 ** normal_depth))
    normal_lower, normal_upper = sorted((fixed, outer))
    if normal_axis == "t":
        box = normal_lower, normal_upper, lower, upper
    else:
        box = lower, upper, normal_lower, normal_upper
    return box, normal_axis, outer, direction


def surface_signs(
    source: Any, second: str, candidate: str,
    boundary_axis: str, box: tuple[Q, Q, Q, Q], lower: Q, upper: Q,
) -> tuple[int, int]:
    t0, t1, p0, p1 = box
    if boundary_axis == "p":
        first = third_tangency_jet(source, second, candidate, t0, t1, lower, lower).value
        second_value = third_tangency_jet(source, second, candidate, t0, t1, upper, upper).value
    else:
        first = third_tangency_jet(source, second, candidate, lower, lower, p0, p1).value
        second_value = third_tangency_jet(source, second, candidate, upper, upper, p0, p1).value
    return strict_sign(first), strict_sign(second_value)


def source_margin(source: Any, box: tuple[Q, Q, Q, Q]) -> Q:
    t0, t1, p0, p1 = box
    return min(t0 - source.t0, source.t1 - t1, p0 - source.p0, source.p1 - p1)


def competitor_rows(
    state2: dict[str, Any], current_target: str, tangent_target: str, tangent_flight: arb,
) -> tuple[list[dict[str, Any]], str | None]:
    candidate_ids = time3.time2_cert.translated_candidate_ids(current_target, state2["chart"])
    if tangent_target not in candidate_ids:
        raise RuntimeError("tangent candidate absent from complete translated table")
    rows: list[dict[str, Any]] = []
    future: list[tuple[str, arb]] = []
    for candidate_id in candidate_ids:
        if candidate_id == tangent_target:
            continue
        candidate = time3.time2_cert.candidate_root(
            state2["contact_x"], state2["contact_y"],
            state2["outgoing_x"], state2["outgoing_y"],
            state2["s"], candidate_id,
        )
        classification = candidate["classification"]
        if classification == "no_real_intersection":
            relation = "NO_REAL_INTERSECTION"
        elif classification == "intersection_strictly_behind":
            relation = "INTERSECTION_STRICTLY_BEHIND"
        elif classification == "strict_future_near_root":
            near = candidate["near"]
            if bool(near < tangent_flight):
                relation = "STRICTLY_BEFORE_TANGENT_TARGET"
            elif bool(tangent_flight < near):
                relation = "STRICTLY_AFTER_TANGENT_TARGET"
            else:
                raise RuntimeError("unresolved competitor/tangent flight order")
            future.append((candidate_id, near))
        else:
            raise RuntimeError(f"unresolved competitor event equation: {classification}")
        rows.append({
            "candidate_id": candidate_id,
            "candidate_root_classification": classification,
            "relation_to_tangent_target_flight": relation,
        })
    rows.sort(key=lambda item: item["candidate_id"])
    winner = None
    for candidate_id, near in future:
        if all(candidate_id == other_id or bool(near < other_near) for other_id, other_near in future):
            if winner is not None:
                raise RuntimeError("nonunique strict future competitor winner")
            winner = candidate_id
    if future and winner is None:
        raise RuntimeError("unresolved strict future competitor winner")
    return rows, winner


def physical_type(
    state2: dict[str, Any], current_target: str, tangent_target: str,
) -> tuple[str, dict[str, Any]]:
    candidate_x, candidate_y = time3.time2_cert.target_center(tangent_target, state2["s"])
    dx = candidate_x - state2["contact_x"]
    dy = candidate_y - state2["contact_y"]
    ux, uy = state2["outgoing_x"], state2["outgoing_y"]
    tangent_flight = ux * dx + uy * dy
    transverse = -uy * dx + ux * dy
    tangent_flight_sign = strict_sign(tangent_flight)
    transverse_sign = strict_sign(transverse)
    if tangent_flight_sign == 0 or transverse_sign == 0:
        raise RuntimeError("unresolved target tangent flight/transverse sign")
    denominator = arb(1) + ux
    if strict_sign(denominator) != 1:
        raise RuntimeError("projective q chart denominator not strictly positive")
    q_value = uy / denominator
    competitors, competitor_winner = competitor_rows(
        state2, current_target, tangent_target, tangent_flight
    )
    tau_max = aq(time3.time2_cert.step1.first_hit.TAU_MAX)
    if tangent_flight_sign < 0:
        status = "ALGEBRAIC_TANGENCY_STRICTLY_BEHIND_SECOND__LOCAL_CONTINUATION"
        tau_relation = "STRICTLY_NEGATIVE"
    elif bool(tangent_flight > tau_max):
        status = "ALGEBRAIC_TANGENCY_STRICTLY_AFTER_TAU_MAX__LOCAL_CONTINUATION"
        tau_relation = "STRICTLY_ABOVE_TAU_MAX"
    elif bool(tangent_flight < tau_max):
        tau_relation = "STRICTLY_BETWEEN_ZERO_AND_TAU_MAX"
        before = [
            item["candidate_id"] for item in competitors
            if item["relation_to_tangent_target_flight"] == "STRICTLY_BEFORE_TANGENT_TARGET"
        ]
        if before:
            if competitor_winner not in before:
                raise RuntimeError("occluding winner does not precede tangent target")
            status = "ALGEBRAIC_TANGENCY_OCCLUDED_BY_EARLIER_THIRD_OWNER__LOCAL_CONTINUATION"
        else:
            status = "PHYSICAL_NEXT_TANGENCY__LOCAL_CONTINUATION"
    else:
        raise RuntimeError("unresolved tangent flight / tau-max event equation")
    return status, {
        "oriented_line_projective_chart": "Q_TAN_HALF_EQUALS_UY_OVER_ONE_PLUS_UX",
        "projective_chart_denominator_strict_sign": 1,
        "projective_q_enclosure": str(q_value),
        "signed_transverse_tangency_factor_sign": transverse_sign,
        "target_tangent_flight_sign": tangent_flight_sign,
        "target_tangent_flight_tau_relation": tau_relation,
        "complete_translated_candidate_count": len(competitors) + 1,
        "competitor_rows": competitors,
        "competitor_rows_sha256": digest(competitors),
        "unique_strict_future_competitor_winner": competitor_winner,
    }


def certify_slab(
    source: Any, row: dict[str, Any],
    lower: Q, upper: Q, lower_sign: int, upper_sign: int,
) -> dict[str, Any]:
    second = row["second_selected_target_id"]
    candidate = row["third_candidate_id"]
    boundary_axis = row["boundary_axis"]
    for normal_depth in range(MINIMUM_NORMAL_DEPTH, MAXIMUM_NORMAL_DEPTH + 1):
        try:
            box, normal_axis, outer, direction = slab_box(
                source, row, lower, upper, normal_depth
            )
            margin = source_margin(source, box)
            if margin <= 0:
                continue
            function = third_tangency_jet(source, second, candidate, *box)
            parameter_index = 1 if boundary_axis == "p" else 0
            normal_index = 1 - parameter_index
            parameter_derivative_sign = strict_sign(function.gradient[parameter_index])
            normal_derivative_sign = strict_sign(function.gradient[normal_index])
            if parameter_derivative_sign == 0 or normal_derivative_sign == 0:
                continue
            uniform_signs = surface_signs(
                source, second, candidate, boundary_axis, box, lower, upper
            )
            if uniform_signs != (lower_sign, upper_sign):
                continue
            atom = step1.Atom(
                row["source_core_index"], source,
                box[0], box[1], box[2], box[3], Q(0), Q(0),
                f"round87-port-slab:{normal_depth}",
            )
            classification, owner_status, destination, state1, owner2 = (
                time3.homogeneity_cert.classify_with_geometry(atom, WORK_CORES)
            )
            if classification != "SURVIVE_THROUGH_2_INNER" or destination is not None:
                continue
            if owner2 is None or owner2["selected_target_id"] != second:
                continue
            state2 = time3.second_outgoing_state(atom, state1, owner2)
            if state2 is None or state2["chart"] != row["second_outgoing_chart"]:
                continue
            status, event = physical_type(state2, second, candidate)
            expected_transverse = row["reverse_tangent_continuation_input"]["signed_transverse_sign"]
            if event["signed_transverse_tangency_factor_sign"] != expected_transverse:
                raise RuntimeError("Round85 transverse sign mismatch")
            return {
                "normal_axis": normal_axis,
                "outward_direction_sign": direction,
                "outward_dyadic_normal_depth": normal_depth,
                "outward_parallel_coordinate": str(outer),
                "source_coordinate_box": list(map(str, box)),
                "source_core_strict_rational_margin": str(margin),
                "uniform_parameter_boundary_signs": list(uniform_signs),
                "parameter_derivative_sign": parameter_derivative_sign,
                "normal_derivative_sign": normal_derivative_sign,
                "implicit_root_slope_sign": -parameter_derivative_sign * normal_derivative_sign,
                "two_collision_classification": classification,
                "two_collision_owner_status": owner_status,
                "selected_second_target_id": owner2["selected_target_id"],
                "second_outgoing_chart": state2["chart"],
                "local_event_classification": status,
                "event_equation_evidence": event,
            }
        except (ValueError, ZeroDivisionError):
            continue
    raise RuntimeError(f"failed outward continuation slab: {row['registered_port_id']}")


def init_worker(precision_bits: int) -> None:
    global WORK_CORES
    ctx.prec = precision_bits
    WORK_CORES = core_cert.physical_cores()


def process_row(row: dict[str, Any]) -> dict[str, Any]:
    source = WORK_CORES[row["source_core_index"]]
    lower, upper, lower_sign, upper_sign = isolate_root(source, row)
    slab = certify_slab(source, row, lower, upper, lower_sign, upper_sign)
    payload = {
        "registered_port_id": row["registered_port_id"],
        "source_core_index": row["source_core_index"],
        "second_selected_target_id": row["second_selected_target_id"],
        "third_candidate_id": row["third_candidate_id"],
        "boundary_axis": row["boundary_axis"],
        "fixed_coordinate": row["fixed_coordinate"],
    }
    return {
        "port_event_continuation_id": "physical-s0-rank3-port-event-continuation:" + digest(payload),
        **payload,
        "inside_side": row["inside_side"],
        "round85_outward_cell_classification": row["outward_cell_classification"],
        "root_equation": "third_candidate_radius_squared_minus_signed_transverse_squared_equals_zero",
        "root_bisection_depth": ROOT_BISECTION_DEPTH,
        "isolated_root_bracket": [str(lower), str(upper)],
        "isolated_root_endpoint_signs": [lower_sign, upper_sign],
        "continuation_slab": {key: value for key, value in slab.items() if key not in {
            "local_event_classification", "event_equation_evidence",
        }},
        "local_event_classification": slab["local_event_classification"],
        "event_equation_evidence": slab["event_equation_evidence"],
        "algebraic_discriminant_root_graph_crosses_registered_union_boundary": True,
        "port_is_locally_physical_third_tangency": (
            slab["local_event_classification"] == "PHYSICAL_NEXT_TANGENCY__LOCAL_CONTINUATION"
        ),
        "locally_physical_next_tangency_endpoint_at_this_port": False,
        "port_pairing_or_global_continuation_asserted": False,
    }


def build(workers: int = 16, precision_bits: int = PRECISION_BITS) -> dict[str, Any]:
    global WORK_CORES
    ctx.prec = precision_bits
    frontier = load_frontier()
    rows = frontier["continuation_frontier_rows"]
    if len(rows) != 3212:
        raise RuntimeError("Round85 non-source port count mismatch")
    if workers == 1:
        init_worker(precision_bits)
        certified = [process_row(row) for row in rows]
    else:
        context = mp.get_context("fork")
        with context.Pool(workers, initializer=init_worker, initargs=(precision_bits,)) as pool:
            certified = pool.map(process_row, rows)
    certified.sort(key=lambda row: row["registered_port_id"])
    event_histogram = Counter(row["local_event_classification"] for row in certified)
    round85_histogram = Counter(row["round85_outward_cell_classification"] for row in certified)
    transverse_histogram = Counter(
        row["event_equation_evidence"]["signed_transverse_tangency_factor_sign"]
        for row in certified
    )
    normal_depth_histogram = Counter(
        row["continuation_slab"]["outward_dyadic_normal_depth"] for row in certified
    )
    competitor_classifications: Counter[str] = Counter()
    competitor_relations: Counter[str] = Counter()
    cross_histogram: Counter[str] = Counter()
    competitor_count = 0
    for row in certified:
        cross_histogram[
            row["local_event_classification"] + " | "
            + row["round85_outward_cell_classification"]
        ] += 1
        for competitor in row["event_equation_evidence"]["competitor_rows"]:
            competitor_count += 1
            competitor_classifications[competitor["candidate_root_classification"]] += 1
            competitor_relations[competitor["relation_to_tangent_target_flight"]] += 1
    minimum_source_margin = min(
        Q(row["continuation_slab"]["source_core_strict_rational_margin"])
        for row in certified
    )
    if dict(event_histogram) != EXPECTED_EVENT_HISTOGRAM:
        raise RuntimeError(f"unexpected local event partition: {dict(event_histogram)}")
    if dict(competitor_classifications) != EXPECTED_COMPETITOR_CLASSIFICATION_HISTOGRAM:
        raise RuntimeError("unexpected complete competitor equation partition")
    if dict(competitor_relations) != EXPECTED_COMPETITOR_RELATION_HISTOGRAM:
        raise RuntimeError("unexpected competitor/tangent flight-order partition")
    if competitor_count != 86315 or not minimum_source_margin > UNIFORM_SOURCE_CORE_MARGIN:
        raise RuntimeError("competitor count or uniform source-core margin mismatch")
    result = {
        "fixed_parameter": "s=0",
        "precision_bits": precision_bits,
        "input_non_source_registered_port_count": frontier["input_non_source_registered_port_count"],
        "certified_local_continuation_port_count": len(certified),
        "unresolved_local_continuation_port_count": 0,
        "locally_physical_next_tangency_endpoint_count": 0,
        "locally_physical_next_tangency_port_count": event_histogram[
            "PHYSICAL_NEXT_TANGENCY__LOCAL_CONTINUATION"
        ],
        "locally_nonphysical_algebraic_tangency_port_count": len(certified) - event_histogram[
            "PHYSICAL_NEXT_TANGENCY__LOCAL_CONTINUATION"
        ],
        "root_bisection_depth_per_port": ROOT_BISECTION_DEPTH,
        "event_classification_histogram": dict(sorted(event_histogram.items())),
        "event_by_round85_outward_classification_histogram": dict(sorted(cross_histogram.items())),
        "round85_outward_cell_classification_histogram_reproduced": dict(sorted(round85_histogram.items())),
        "signed_transverse_tangency_factor_sign_histogram": {
            str(key): value for key, value in sorted(transverse_histogram.items())
        },
        "outward_dyadic_normal_depth_histogram": {
            str(key): value for key, value in sorted(normal_depth_histogram.items())
        },
        "maximum_outward_dyadic_normal_depth": max(normal_depth_histogram),
        "complete_nontarget_competitor_event_equation_count": competitor_count,
        "competitor_root_classification_histogram": dict(sorted(competitor_classifications.items())),
        "competitor_relation_to_tangent_flight_histogram": dict(sorted(competitor_relations.items())),
        "minimum_source_core_strict_rational_margin": str(minimum_source_margin),
        "uniform_source_core_strict_rational_margin_lower_bound": str(UNIFORM_SOURCE_CORE_MARGIN),
        "all_3212_algebraic_discriminant_graphs_cross_artificial_union_boundary": True,
        "all_945_locally_physical_next_tangency_ports_are_nonendpoints": True,
        "port_event_rows": certified,
        "port_event_rows_sha256": digest(certified),
        "strict_scope": "local implicit-function continuation and physical visibility typing at all 3212 frozen non-source registered union-boundary ports",
        "strict_nonclaims": [
            "no two ports are paired by this local certificate",
            "3212/2=1606 is not a gap count",
            "local continuation is not a complete global reverse-tangent interval quotient",
            "registered elementary arcs are not promoted to complete physical faces",
            "the 2267 locally nonphysical algebraic roots are not physical third-tangency points",
            "Gate 5 and RN return-face rows are not promoted",
        ],
        "upstream_pins": {
            "round85_outward_frontier_source_sha256": FRONTIER_SOURCE_SHA256,
            "round85_outward_frontier_manifest_sha256": FRONTIER_SHA256,
            "round85_outward_frontier_audit_sha256": FRONTIER_AUDIT_SHA256,
            "round85_continuation_frontier_rows_sha256": frontier["continuation_frontier_rows_sha256"],
            "gate25_physical_return_core_registry_manifest_sha256": CORE_MANIFEST_SHA256,
            "executable_source_sha256": dict(sorted(EXECUTABLE_SOURCE_PINS.items())),
        },
    }
    return {"schema": SCHEMA, "result": result, "result_sha256": digest(result)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workers", type=int, default=16)
    args = parser.parse_args()
    json.dump(build(args.workers), sys.stdout, sort_keys=True, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
