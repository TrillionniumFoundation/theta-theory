#!/usr/bin/env python3
"""Independent 768-bit verifier for the Round-87 port-event certificate."""
from __future__ import annotations

import argparse
import copy
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
MANIFEST = HERE / "cm2-round87-rank3-port-event-continuation-2026-07-22.json"
FRONTIER = HERE / "cm2-round85-rank3-outward-port-continuation-frontier-2026-07-22.json"
CERT_SOURCE = HERE / "cm2_round87_rank3_port_event_continuation_cert.py"
CORE_MANIFEST = HERE / "cm2-gate25-physical-return-core-registry-manifest-2026-07-16.json"
SCHEMA = "cm2.round87.rank3-port-event-continuation.v1"
AUDIT_SCHEMA = "cm2.round87.rank3-port-event-continuation-audit.v1"
MANIFEST_SHA256 = "f63f5d627def35f87dd3dfac075f8ecc0e8a5adfa725ddbe0eb692a39b54393b"
MANIFEST_RESULT_SHA256 = "a076c6d5ec7714f8738ba4dd94cd668945c84cf46c01873666e575a7f9ea968e"
CERT_SOURCE_SHA256 = "71f10cde22ea191c7710090e2e7474fdbc2925ded94fe60071159b2c262dc834"
FRONTIER_SHA256 = "b202e432f390266b38d13a4c6c4a8710f9189493897612387bfa632603dd273f"
CORE_MANIFEST_SHA256 = "144f5516ada8b83ca07459582c8cdb07ba09db11ac18a90cff32c6396c6e5a42"
VERIFY_PRECISION_BITS = 768
ROOT_DEPTH = 128
GRID = 64
WORK_CORES: tuple[Any, ...] = ()
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

RESULT_KEYS = {
    "fixed_parameter", "precision_bits", "input_non_source_registered_port_count",
    "certified_local_continuation_port_count", "unresolved_local_continuation_port_count",
    "locally_physical_next_tangency_endpoint_count",
    "locally_physical_next_tangency_port_count",
    "locally_nonphysical_algebraic_tangency_port_count", "root_bisection_depth_per_port",
    "event_classification_histogram", "event_by_round85_outward_classification_histogram",
    "round85_outward_cell_classification_histogram_reproduced",
    "signed_transverse_tangency_factor_sign_histogram",
    "outward_dyadic_normal_depth_histogram", "maximum_outward_dyadic_normal_depth",
    "complete_nontarget_competitor_event_equation_count",
    "competitor_root_classification_histogram",
    "competitor_relation_to_tangent_flight_histogram",
    "minimum_source_core_strict_rational_margin",
    "uniform_source_core_strict_rational_margin_lower_bound",
    "all_3212_algebraic_discriminant_graphs_cross_artificial_union_boundary",
    "all_945_locally_physical_next_tangency_ports_are_nonendpoints",
    "port_event_rows", "port_event_rows_sha256", "strict_scope", "strict_nonclaims",
    "upstream_pins",
}
ROW_KEYS = {
    "port_event_continuation_id", "registered_port_id", "source_core_index",
    "second_selected_target_id", "third_candidate_id", "boundary_axis",
    "fixed_coordinate", "inside_side", "round85_outward_cell_classification",
    "root_equation", "root_bisection_depth", "isolated_root_bracket",
    "isolated_root_endpoint_signs", "continuation_slab", "local_event_classification",
    "event_equation_evidence",
    "algebraic_discriminant_root_graph_crosses_registered_union_boundary",
    "port_is_locally_physical_third_tangency",
    "locally_physical_next_tangency_endpoint_at_this_port",
    "port_pairing_or_global_continuation_asserted",
}
SLAB_KEYS = {
    "normal_axis", "outward_direction_sign", "outward_dyadic_normal_depth",
    "outward_parallel_coordinate", "source_coordinate_box",
    "source_core_strict_rational_margin", "uniform_parameter_boundary_signs",
    "parameter_derivative_sign", "normal_derivative_sign", "implicit_root_slope_sign",
    "two_collision_classification", "two_collision_owner_status",
    "selected_second_target_id", "second_outgoing_chart",
}
EVENT_KEYS = {
    "oriented_line_projective_chart", "projective_chart_denominator_strict_sign",
    "projective_q_enclosure", "signed_transverse_tangency_factor_sign",
    "target_tangent_flight_sign", "target_tangent_flight_tau_relation",
    "complete_translated_candidate_count", "competitor_rows", "competitor_rows_sha256",
    "unique_strict_future_competitor_winner",
}
COMPETITOR_KEYS = {
    "candidate_id", "candidate_root_classification",
    "relation_to_tangent_target_flight",
}


def strict_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        if key in out:
            raise ValueError(f"duplicate JSON key: {key}")
        out[key] = value
    return out


def reject_nonfinite(token: str) -> Any:
    raise ValueError(f"nonfinite JSON number: {token}")


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse_text(text: str) -> dict[str, Any]:
    value = json.loads(text, object_pairs_hook=strict_pairs, parse_constant=reject_nonfinite)
    if not isinstance(value, dict):
        raise RuntimeError("document is not an object")
    return value


def check_closed_schema(document: dict[str, Any]) -> None:
    if set(document) != {"schema", "result", "result_sha256"}:
        raise RuntimeError("non-closed document")
    if document["schema"] != SCHEMA or set(document["result"]) != RESULT_KEYS:
        raise RuntimeError("top-level schema mismatch")
    result = document["result"]
    if not isinstance(result["port_event_rows"], list):
        raise RuntimeError("row ledger type")
    for row in result["port_event_rows"]:
        if set(row) != ROW_KEYS or set(row["continuation_slab"]) != SLAB_KEYS:
            raise RuntimeError("row/slab closed-schema mismatch")
        event = row["event_equation_evidence"]
        if set(event) != EVENT_KEYS:
            raise RuntimeError("event evidence closed-schema mismatch")
        if any(set(candidate) != COMPETITOR_KEYS for candidate in event["competitor_rows"]):
            raise RuntimeError("competitor row closed-schema mismatch")
    if set(result["upstream_pins"]) != {
        "round85_outward_frontier_source_sha256",
        "round85_outward_frontier_manifest_sha256",
        "round85_outward_frontier_audit_sha256",
        "round85_continuation_frontier_rows_sha256",
        "gate25_physical_return_core_registry_manifest_sha256",
        "executable_source_sha256",
    }:
        raise RuntimeError("pin schema mismatch")
    if result["upstream_pins"]["executable_source_sha256"] != dict(sorted(EXECUTABLE_SOURCE_PINS.items())):
        raise RuntimeError("executable source pin ledger mismatch")


def static_validate(document: dict[str, Any]) -> None:
    check_closed_schema(document)
    if document["result_sha256"] != digest(document["result"]):
        raise RuntimeError("result digest mismatch")
    if document["result_sha256"] != MANIFEST_RESULT_SHA256:
        raise RuntimeError("frozen semantic result pin mismatch")


def point_value(source: Any, upstream: dict[str, Any], fixed: Q, parameter: Q) -> Any:
    second, candidate = upstream["second_selected_target_id"], upstream["third_candidate_id"]
    if upstream["boundary_axis"] == "p":
        return third_tangency_jet(source, second, candidate, fixed, fixed, parameter, parameter).value
    return third_tangency_jet(source, second, candidate, parameter, parameter, fixed, fixed).value


def independent_bisection(source: Any, upstream: dict[str, Any]) -> tuple[Q, Q, int, int]:
    fixed = Q(upstream["fixed_coordinate"])
    lower, upper = map(Q, upstream["root_grid_isolation"]["isolated_root_bracket"])
    lower_sign, upper_sign = upstream["root_grid_isolation"]["isolated_endpoint_signs"]
    for _ in range(ROOT_DEPTH):
        middle = (lower + upper) / 2
        sign = strict_sign(point_value(source, upstream, fixed, middle))
        if sign == 0:
            raise RuntimeError("independent bisection indeterminate")
        if sign == lower_sign:
            lower, lower_sign = middle, sign
        else:
            upper, upper_sign = middle, sign
    return lower, upper, lower_sign, upper_sign


def independent_competitors(
    state2: dict[str, Any], second: str, target: str, target_flight: arb,
) -> tuple[list[dict[str, Any]], str | None]:
    ids = time3.time2_cert.translated_candidate_ids(second, state2["chart"])
    if target not in ids:
        raise RuntimeError("target absent from translated candidates")
    rows: list[dict[str, Any]] = []
    future: list[tuple[str, arb]] = []
    for candidate_id in ids:
        if candidate_id == target:
            continue
        candidate = time3.time2_cert.candidate_root(
            state2["contact_x"], state2["contact_y"],
            state2["outgoing_x"], state2["outgoing_y"], state2["s"], candidate_id,
        )
        kind = candidate["classification"]
        if kind == "no_real_intersection":
            relation = "NO_REAL_INTERSECTION"
        elif kind == "intersection_strictly_behind":
            relation = "INTERSECTION_STRICTLY_BEHIND"
        elif kind == "strict_future_near_root":
            near = candidate["near"]
            if bool(near < target_flight):
                relation = "STRICTLY_BEFORE_TANGENT_TARGET"
            elif bool(target_flight < near):
                relation = "STRICTLY_AFTER_TANGENT_TARGET"
            else:
                raise RuntimeError("competitor flight-order equation unresolved")
            future.append((candidate_id, near))
        else:
            raise RuntimeError(f"competitor equation unresolved: {kind}")
        rows.append({
            "candidate_id": candidate_id,
            "candidate_root_classification": kind,
            "relation_to_tangent_target_flight": relation,
        })
    rows.sort(key=lambda item: item["candidate_id"])
    winners = [
        candidate_id for candidate_id, near in future
        if all(candidate_id == other_id or bool(near < other) for other_id, other in future)
    ]
    if len(winners) != (1 if future else 0):
        raise RuntimeError("future competitor winner not unique")
    return rows, winners[0] if winners else None


def init_worker() -> None:
    global WORK_CORES
    ctx.prec = VERIFY_PRECISION_BITS
    WORK_CORES = core_cert.physical_cores()


def verify_row(pair: tuple[dict[str, Any], dict[str, Any]]) -> dict[str, Any]:
    row, upstream = pair
    source = WORK_CORES[upstream["source_core_index"]]
    if row["registered_port_id"] != upstream["registered_port_id"]:
        raise RuntimeError("port id crosswalk")
    for key in (
        "source_core_index", "second_selected_target_id", "third_candidate_id",
        "boundary_axis", "fixed_coordinate", "inside_side",
    ):
        if row[key] != upstream[key]:
            raise RuntimeError(f"upstream crosswalk mismatch: {key}")
    if row["round85_outward_cell_classification"] != upstream["outward_cell_classification"]:
        raise RuntimeError("Round85 outward class mismatch")
    lower, upper, lower_sign, upper_sign = independent_bisection(source, upstream)
    if row["root_bisection_depth"] != ROOT_DEPTH:
        raise RuntimeError("root depth")
    if row["isolated_root_bracket"] != [str(lower), str(upper)]:
        raise RuntimeError("root bracket")
    if row["isolated_root_endpoint_signs"] != [lower_sign, upper_sign]:
        raise RuntimeError("root signs")
    slab = row["continuation_slab"]
    depth = slab["outward_dyadic_normal_depth"]
    axis = upstream["boundary_axis"]
    normal_axis = "t" if axis == "p" else "p"
    fixed = Q(upstream["fixed_coordinate"])
    span = source.t1 - source.t0 if normal_axis == "t" else source.p1 - source.p0
    direction = -int(upstream["inside_side"])
    outer = fixed + direction * span / Q(GRID * (2 ** depth))
    normal_lower, normal_upper = sorted((fixed, outer))
    expected_box = (
        (normal_lower, normal_upper, lower, upper)
        if normal_axis == "t" else (lower, upper, normal_lower, normal_upper)
    )
    margin = min(
        expected_box[0] - source.t0, source.t1 - expected_box[1],
        expected_box[2] - source.p0, source.p1 - expected_box[3],
    )
    if slab["normal_axis"] != normal_axis or slab["outward_direction_sign"] != direction:
        raise RuntimeError("outward slab orientation")
    if slab["outward_parallel_coordinate"] != str(outer):
        raise RuntimeError("outer coordinate")
    if slab["source_coordinate_box"] != list(map(str, expected_box)):
        raise RuntimeError("slab box")
    if slab["source_core_strict_rational_margin"] != str(margin) or margin <= Q(1, 100000):
        raise RuntimeError("source-core margin")
    function = third_tangency_jet(
        source, upstream["second_selected_target_id"], upstream["third_candidate_id"],
        *expected_box,
    )
    parameter_index = 1 if axis == "p" else 0
    pds = strict_sign(function.gradient[parameter_index])
    nds = strict_sign(function.gradient[1 - parameter_index])
    t0, t1, p0, p1 = expected_box
    if axis == "p":
        surfaces = (
            third_tangency_jet(source, upstream["second_selected_target_id"], upstream["third_candidate_id"], t0, t1, lower, lower).value,
            third_tangency_jet(source, upstream["second_selected_target_id"], upstream["third_candidate_id"], t0, t1, upper, upper).value,
        )
    else:
        surfaces = (
            third_tangency_jet(source, upstream["second_selected_target_id"], upstream["third_candidate_id"], lower, lower, p0, p1).value,
            third_tangency_jet(source, upstream["second_selected_target_id"], upstream["third_candidate_id"], upper, upper, p0, p1).value,
        )
    surface_signs = [strict_sign(value) for value in surfaces]
    if not pds or not nds or surface_signs != [lower_sign, upper_sign]:
        raise RuntimeError("implicit root graph test")
    if (
        slab["uniform_parameter_boundary_signs"] != surface_signs
        or slab["parameter_derivative_sign"] != pds
        or slab["normal_derivative_sign"] != nds
        or slab["implicit_root_slope_sign"] != -pds * nds
    ):
        raise RuntimeError("implicit evidence mismatch")
    atom = step1.Atom(
        upstream["source_core_index"], source, *expected_box, Q(0), Q(0), "round87-independent",
    )
    classification, owner_status, destination, state1, owner2 = (
        time3.homogeneity_cert.classify_with_geometry(atom, WORK_CORES)
    )
    if classification != "SURVIVE_THROUGH_2_INNER" or destination is not None or owner2 is None:
        raise RuntimeError("independent two-collision branch")
    state2 = time3.second_outgoing_state(atom, state1, owner2)
    if state2 is None:
        raise RuntimeError("independent second outgoing state")
    if (
        slab["two_collision_classification"] != classification
        or slab["two_collision_owner_status"] != owner_status
        or slab["selected_second_target_id"] != owner2["selected_target_id"]
        or owner2["selected_target_id"] != upstream["second_selected_target_id"]
        or slab["second_outgoing_chart"] != state2["chart"]
        or state2["chart"] != upstream["second_outgoing_chart"]
    ):
        raise RuntimeError("two-collision evidence mismatch")
    target = upstream["third_candidate_id"]
    cx, cy = time3.time2_cert.target_center(target, state2["s"])
    dx, dy = cx - state2["contact_x"], cy - state2["contact_y"]
    ux, uy = state2["outgoing_x"], state2["outgoing_y"]
    flight = ux * dx + uy * dy
    transverse = -uy * dx + ux * dy
    flight_sign, transverse_sign = strict_sign(flight), strict_sign(transverse)
    if not flight_sign or not transverse_sign or strict_sign(arb(1) + ux) != 1:
        raise RuntimeError("target/projective sign")
    competitors, winner = independent_competitors(
        state2, upstream["second_selected_target_id"], target, flight
    )
    tau = aq(time3.time2_cert.step1.first_hit.TAU_MAX)
    if flight_sign < 0:
        event_class = "ALGEBRAIC_TANGENCY_STRICTLY_BEHIND_SECOND__LOCAL_CONTINUATION"
        tau_relation = "STRICTLY_NEGATIVE"
    elif bool(flight > tau):
        event_class = "ALGEBRAIC_TANGENCY_STRICTLY_AFTER_TAU_MAX__LOCAL_CONTINUATION"
        tau_relation = "STRICTLY_ABOVE_TAU_MAX"
    elif bool(flight < tau):
        tau_relation = "STRICTLY_BETWEEN_ZERO_AND_TAU_MAX"
        before = any(
            item["relation_to_tangent_target_flight"] == "STRICTLY_BEFORE_TANGENT_TARGET"
            for item in competitors
        )
        event_class = (
            "ALGEBRAIC_TANGENCY_OCCLUDED_BY_EARLIER_THIRD_OWNER__LOCAL_CONTINUATION"
            if before else "PHYSICAL_NEXT_TANGENCY__LOCAL_CONTINUATION"
        )
    else:
        raise RuntimeError("tau relation unresolved")
    evidence = row["event_equation_evidence"]
    if row["local_event_classification"] != event_class:
        raise RuntimeError("event class")
    expected_discrete = {
        "oriented_line_projective_chart": "Q_TAN_HALF_EQUALS_UY_OVER_ONE_PLUS_UX",
        "projective_chart_denominator_strict_sign": 1,
        "signed_transverse_tangency_factor_sign": transverse_sign,
        "target_tangent_flight_sign": flight_sign,
        "target_tangent_flight_tau_relation": tau_relation,
        "complete_translated_candidate_count": len(competitors) + 1,
        "competitor_rows": competitors,
        "competitor_rows_sha256": digest(competitors),
        "unique_strict_future_competitor_winner": winner,
    }
    for key, value in expected_discrete.items():
        if evidence[key] != value:
            raise RuntimeError(f"event evidence mismatch: {key}")
    q_recomputed = uy / (arb(1) + ux)
    if not arb(evidence["projective_q_enclosure"]).overlaps(q_recomputed):
        raise RuntimeError("projective q enclosure")
    identity_payload = {
        "registered_port_id": upstream["registered_port_id"],
        "source_core_index": upstream["source_core_index"],
        "second_selected_target_id": upstream["second_selected_target_id"],
        "third_candidate_id": upstream["third_candidate_id"],
        "boundary_axis": upstream["boundary_axis"],
        "fixed_coordinate": upstream["fixed_coordinate"],
    }
    if row["port_event_continuation_id"] != "physical-s0-rank3-port-event-continuation:" + digest(identity_payload):
        raise RuntimeError("continuation id")
    locally_physical = event_class == "PHYSICAL_NEXT_TANGENCY__LOCAL_CONTINUATION"
    if not (
        row["algebraic_discriminant_root_graph_crosses_registered_union_boundary"] is True
        and row["port_is_locally_physical_third_tangency"] is locally_physical
        and row["locally_physical_next_tangency_endpoint_at_this_port"] is False
        and row["port_pairing_or_global_continuation_asserted"] is False
    ):
        raise RuntimeError("row verdict flags")
    return {
        "event_class": event_class,
        "outward_class": upstream["outward_cell_classification"],
        "transverse_sign": transverse_sign,
        "normal_depth": depth,
        "margin": str(margin),
        "competitors": competitors,
    }


def independent_verify(document: dict[str, Any], workers: int) -> dict[str, Any]:
    frontier_document = parse_text(FRONTIER.read_text())
    if (
        set(frontier_document) != {"schema", "result", "result_sha256"}
        or frontier_document["result_sha256"] != digest(frontier_document["result"])
    ):
        raise RuntimeError("frontier document validation")
    upstream_rows = frontier_document["result"]["continuation_frontier_rows"]
    certified_rows = document["result"]["port_event_rows"]
    if len(upstream_rows) != 3212 or len(certified_rows) != 3212:
        raise RuntimeError("port count")
    if [row["registered_port_id"] for row in upstream_rows] != [row["registered_port_id"] for row in certified_rows]:
        raise RuntimeError("ordered port crosswalk")
    context = mp.get_context("fork")
    if workers == 1:
        init_worker()
        checks = [verify_row(pair) for pair in zip(certified_rows, upstream_rows)]
    else:
        with context.Pool(workers, initializer=init_worker) as pool:
            checks = pool.map(verify_row, zip(certified_rows, upstream_rows))
    event_hist = Counter(row["event_class"] for row in checks)
    transverse_hist = Counter(row["transverse_sign"] for row in checks)
    competitor_count = sum(len(row["competitors"]) for row in checks)
    competitor_class = Counter(
        item["candidate_root_classification"] for row in checks for item in row["competitors"]
    )
    competitor_relation = Counter(
        item["relation_to_tangent_target_flight"] for row in checks for item in row["competitors"]
    )
    result = document["result"]
    if dict(sorted(event_hist.items())) != result["event_classification_histogram"]:
        raise RuntimeError("aggregate event histogram")
    if {str(k): v for k, v in sorted(transverse_hist.items())} != result["signed_transverse_tangency_factor_sign_histogram"]:
        raise RuntimeError("aggregate transverse histogram")
    if competitor_count != result["complete_nontarget_competitor_event_equation_count"]:
        raise RuntimeError("aggregate competitor count")
    if dict(sorted(competitor_class.items())) != result["competitor_root_classification_histogram"]:
        raise RuntimeError("aggregate competitor class")
    if dict(sorted(competitor_relation.items())) != result["competitor_relation_to_tangent_flight_histogram"]:
        raise RuntimeError("aggregate competitor relation")
    minimum_margin = min(Q(row["margin"]) for row in checks)
    if str(minimum_margin) != result["minimum_source_core_strict_rational_margin"]:
        raise RuntimeError("aggregate minimum margin")
    return {
        "independently_recomputed_port_count": len(checks),
        "independently_recomputed_competitor_equation_count": competitor_count,
        "independent_event_histogram": dict(sorted(event_hist.items())),
        "independent_minimum_source_core_margin": str(minimum_margin),
        "independent_maximum_outward_normal_depth": max(row["normal_depth"] for row in checks),
    }


def mutation_rejected(document: dict[str, Any], mutator: Any) -> bool:
    attack = copy.deepcopy(document)
    mutator(attack)
    attack["result_sha256"] = digest(attack["result"])
    try:
        static_validate(attack)
    except Exception:
        return True
    return False


def strict_json_attacks_rejected(text: str) -> int:
    attacks = [
        text.replace('"schema":', '"schema":"duplicate","schema":', 1),
        text.replace('"precision_bits": 512', '"precision_bits": NaN', 1),
        text.replace('"precision_bits": 512', '"precision_bits": Infinity', 1),
        text.replace('"result": {', '"result": {"unexpected":0,', 1),
    ]
    rejected = 0
    for attack in attacks:
        try:
            static_validate(parse_text(attack))
        except Exception:
            rejected += 1
    return rejected


def build_audit(workers: int) -> dict[str, Any]:
    if file_sha256(MANIFEST) != MANIFEST_SHA256:
        raise RuntimeError("manifest byte pin")
    if file_sha256(CERT_SOURCE) != CERT_SOURCE_SHA256:
        raise RuntimeError("producer source byte pin")
    if file_sha256(FRONTIER) != FRONTIER_SHA256:
        raise RuntimeError("frontier byte pin")
    if file_sha256(CORE_MANIFEST) != CORE_MANIFEST_SHA256:
        raise RuntimeError("physical-core theorem byte pin")
    core_document = parse_text(CORE_MANIFEST.read_text())
    if (
        core_document.get("schema") != "cm2.gate25.physical-return-core-registry.manifest.v1"
        or core_document.get("verdict", {}).get("positive_mass_physical_core_registry") != "CERTIFIED"
        or core_document.get("verdict", {}).get("physical_nonempty_return_key_lower_bound") != "CERTIFIED_AT_LEAST_24"
    ):
        raise RuntimeError("physical-core theorem semantic pin")
    for name, expected in EXECUTABLE_SOURCE_PINS.items():
        if file_sha256(HERE / name) != expected:
            raise RuntimeError(f"executable source byte pin: {name}")
    text = MANIFEST.read_text()
    document = parse_text(text)
    static_validate(document)
    independent = independent_verify(document, workers)
    mutators = [
        lambda value: value["result"].__setitem__("certified_local_continuation_port_count", 3211),
        lambda value: value["result"]["event_classification_histogram"].__setitem__("PHYSICAL_NEXT_TANGENCY__LOCAL_CONTINUATION", 946),
        lambda value: value["result"]["port_event_rows"][0].__setitem__("local_event_classification", "PHYSICAL_NEXT_TANGENCY__LOCAL_CONTINUATION"),
        lambda value: value["result"]["port_event_rows"][0].__setitem__("isolated_root_bracket", ["0", "1"]),
        lambda value: value["result"]["port_event_rows"][0]["event_equation_evidence"]["competitor_rows"][0].__setitem__("relation_to_tangent_target_flight", "STRICTLY_BEFORE_TANGENT_TARGET"),
        lambda value: value["result"].__setitem__("all_945_locally_physical_next_tangency_ports_are_nonendpoints", False),
    ]
    hostile = sum(mutation_rejected(document, mutator) for mutator in mutators)
    scalar_pin_keys = sorted(
        key for key in document["result"]["upstream_pins"]
        if key != "executable_source_sha256"
    )
    pin_mutators = [
        (lambda key: lambda value: value["result"]["upstream_pins"].__setitem__(key, "0" * 64))(key)
        for key in scalar_pin_keys
    ] + [
        (lambda name: lambda value: value["result"]["upstream_pins"]["executable_source_sha256"].__setitem__(name, "0" * 64))(name)
        for name in sorted(EXECUTABLE_SOURCE_PINS)
    ]
    pin_rejected = sum(mutation_rejected(document, mutator) for mutator in pin_mutators)
    strict_json = strict_json_attacks_rejected(text)
    if hostile != len(mutators) or pin_rejected != len(pin_mutators) or strict_json != 4:
        raise RuntimeError("hostile mutation coverage")
    result = {
        "audit_status": "PASS",
        "verifier_precision_bits": VERIFY_PRECISION_BITS,
        **independent,
        "manifest_byte_pin_verified": True,
        "producer_source_byte_pin_verified": True,
        "upstream_frontier_byte_pin_verified": True,
        "physical_core_theorem_byte_pin_verified": True,
        "executable_source_byte_pins_verified": f"{len(EXECUTABLE_SOURCE_PINS)}/{len(EXECUTABLE_SOURCE_PINS)}",
        "closed_schema_verified": True,
        "hostile_semantic_mutations_rejected": f"{hostile}/{len(mutators)}",
        "upstream_pin_mutations_rejected": f"{pin_rejected}/{len(pin_mutators)}",
        "strict_json_attacks_rejected": f"{strict_json}/4",
        "frozen_manifest_sha256": MANIFEST_SHA256,
        "frozen_manifest_result_sha256": MANIFEST_RESULT_SHA256,
    }
    return {"schema": AUDIT_SCHEMA, "result": result, "result_sha256": digest(result)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workers", type=int, default=16)
    args = parser.parse_args()
    json.dump(build_audit(args.workers), sys.stdout, sort_keys=True, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
