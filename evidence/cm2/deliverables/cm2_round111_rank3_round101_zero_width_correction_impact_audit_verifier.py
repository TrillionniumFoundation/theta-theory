#!/usr/bin/env python3
"""Independent 640-bit verifier for the Round111 Round101 correction.

This module deliberately does not import the Round111 producer or Round96's
``certify``/``state`` routines.  It reconstructs the centered reverse path,
all competitor-clearance rows, the frozen zero-width digest, the corrected
positive-width cells, and the endpoint-ring prefix directly from older
immutable geometry helpers.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from collections import Counter
from dataclasses import replace
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from flint import arb, ctx

import cm2_gate25_physical_return_core_registry_cert as core_cert
import cm2_gate3_candidate_first_hit_cert as first_hit
import cm2_gate34_round26_q1_time2_frontier_cert as time2
import cm2_round91_rank3_exterior_source_exit_cert as round91
import cm2_round93_rank3_full_source_chart_exit_cert as round93
import cm2_round94_rank3_adjacent_chart_transfer_cert as round94
import cm2_round95_rank3_centered_reverse_interval_cert as round95
from cm2_round79_tangency_intersection_generator import aq, strict_sign


HERE = Path(__file__).resolve().parent
CERT = HERE / "cm2-round111-rank3-round101-zero-width-correction-impact-audit-2026-07-23.json"
CERT_SHA256 = "e343a15d5ad4838c2b9a808d64f9724e564e850cbdb13168c5e31e8f059794f1"
SCHEMA = "cm2.round111.rank3-round101-zero-width-correction-impact-audit.v1"
VERIFY_SCHEMA = "cm2.round111.rank3-round101-zero-width-correction-impact-audit-verification.v1"
PRECISION_BITS = 640
ENDPOINT_RING_PREFIX = 32

FILES = {
    "r87": "cm2-round87-rank3-port-event-continuation-2026-07-22.json",
    "r94": "cm2-round94-rank3-adjacent-chart-transfer-2026-07-22.json",
    "r99": "cm2-round99-rank3-registered-port-candidate-audit-2026-07-22.json",
    "r100": "cm2-round100-rank3-immutable-interior-gap-closure-2026-07-22.json",
    "r101": "cm2-round101-rank3-eight-ray-source-grazing-closure-2026-07-22.json",
    "r102": "cm2-round102-rank3-corrected-face-quotient-2026-07-22.json",
    "r103": "cm2-round103-rank3-rn-f1-f2-binding-2026-07-22.json",
    "r104": "cm2-round104-rank3-rn-f3-prefix-chart-2026-07-22.json",
    "r105": "cm2-round105-rank3-rn-f4-suffix-chart-2026-07-22.json",
    "r106": "cm2-round106-rank3-f5-adjacent-cell-scope-audit-2026-07-22.json",
    "r107": "cm2-round107-rank3-adjacent-smooth-cell-atlas-2026-07-22.json",
    "r108": "cm2-round108-rank3-official-word-crosswalk-2026-07-22.json",
    "r109": "cm2-round109-rank3-registered-arc-immutable-whole-tube-reaudit-2026-07-22.json",
    "r110": "cm2-round110-rank3-gap-tube-side-decomposition-2026-07-22.json",
}
PINS = {
    "cm2_gate25_physical_return_core_registry_cert.py": "2da58e5fb5fe030023d6fade7252ec67d0e494708b32d1e32b3ce545e2052fdb",
    "cm2_gate3_candidate_first_hit_cert.py": "6d224d74cda186a40ef9956d1dd6556d5a7b9f506d47c942427ceb66fd705bd2",
    "cm2_gate34_round26_q1_time2_frontier_cert.py": "18385fe423aeb38c4ea988f11b76293e573becf82c50e663030f17ae70430fc9",
    "cm2_round79_tangency_intersection_generator.py": "971f918ca1ed23bd081adf3b233d578e750b61231b20113327f221b40b890ed7",
    FILES["r87"]: "f63f5d627def35f87dd3dfac075f8ecc0e8a5adfa725ddbe0eb692a39b54393b",
    FILES["r94"]: "915f7c18d896d92116ab3f4346a5853c09fef2d3226a1f5429a7c19bca948ee3",
    FILES["r99"]: "e1f0ea00d48e9eae553d5bb24ce140d27f696fd071cb19270e023263aac32f5e",
    FILES["r100"]: "097849bf3da9d34a83ce9693ca68093ed2de7460cc51dcb26ce484c589f278d6",
    FILES["r101"]: "df29ea8467c09351276a40b38424d6c9effc763f287815e7bac67829bca58172",
    FILES["r102"]: "85069546fbc29f45af93eb65e2c2979bc83bfb5d744199771e234c2f7a1f0edb",
    FILES["r103"]: "76ac1099805e5fb3d9eac9984a078ed52f1f6ec706a5a12ec880de28a262c8e8",
    FILES["r104"]: "d6d47ac6b7cb03f70d483536a31ca031718f9aa96bd8adfce072866870bb9c5d",
    FILES["r105"]: "ef747bcd760bf8fe0a8bd8ac3bc65f9df4cf381898ffe98afcdb823f19c44b28",
    FILES["r106"]: "d3fbf85017f173e609a34b8b202d09d1fb0e5a664b922951c1c0730836d8f57e",
    FILES["r107"]: "bb6aeaa821174a1e1994eff2eb10046811b66dd7cf41c4e2d1c898b74d9dea74",
    FILES["r108"]: "96bf22d97f517d53cb360c4aae64a2d5a5a0bbfb7125610dc69b519629bd78ea",
    FILES["r109"]: "fa5231f91f71da8014f9ca606702e3a59499adf78ce86ce09954bb424dae540e",
    FILES["r110"]: "2b49f900e05a29fc65897b8ebf350882a310fa95ebcd0031f94214f87ded38a2",
    "cm2_round91_rank3_exterior_source_exit_cert.py": "d75eb3a9a6aeca2c45b5b9eaa487c32481d4a9cf7e3da04c5d45d6f9a79414da",
    "cm2_round93_rank3_full_source_chart_exit_cert.py": "cec3bc83ae2a9df015441ce72397c2d553a74baf2cab89946a220ee4debb1023",
    "cm2_round94_rank3_adjacent_chart_transfer_cert.py": "ecc5fae4bf35bb33408f10b8357b546d487be57329e2a798fc1ace95a3c0a24b",
    "cm2_round95_rank3_centered_reverse_interval_cert.py": "c7921f2e999df9f1fb9ac935f28093e830d036116dafaf18dc2b2090c5e7702b",
    "cm2_round96_rank3_correlated_owner_interval_cert.py": "5c0205e4756270d8f94ede4947c2b80f82ad655b37d81a6bc02aa8bade54c702",
    "cm2_round101_rank3_eight_ray_source_grazing_closure.py": "2e42513fdc6674200a3a6b29f7fa4182c938bf9b8e30facf43085a790f1b8a1f",
}
SCHEMAS = {
    "r87": "cm2.round87.rank3-port-event-continuation.v1",
    "r94": "cm2.round94.rank3-adjacent-chart-transfer.v1",
    "r99": "cm2.round99.rank3-registered-port-candidate-audit.v1",
    "r100": "cm2.round100.rank3-immutable-interior-gap-closure.v1",
    "r101": "cm2.round101.rank3-eight-ray-source-grazing-closure.v1",
    "r102": "cm2.round102.rank3-corrected-face-quotient.v1",
    "r103": "cm2.round103.rank3-rn-f1-f2-binding.v1",
    "r104": "cm2.round104.rank3-rn-f3-prefix-chart.v1",
    "r105": "cm2.round105.rank3-rn-f4-suffix-chart.v1",
    "r106": "cm2.round106.rank3-f5-adjacent-cell-scope-audit.v1",
    "r107": "cm2.round107.rank3-adjacent-smooth-cell-atlas.v1",
    "r108": "cm2.round108.rank3-official-word-crosswalk.v1",
    "r109": "cm2.round109.rank3-registered-arc-immutable-whole-tube-reaudit.v1",
    "r110": "cm2.round110.rank3-gap-tube-side-decomposition.v1",
}
RESULT_KEYS = {
    "CM2", "audited_round101_ray_count", "certified_endpoint_dyadic_ring_count",
    "certified_endpoint_dyadic_ring_prefix_per_ray", "complete_18_field_operator_block_count",
    "corrected_actual_positive_width_adjacent_base_segment_count",
    "corrected_nonterminal_replay_mode_histogram", "corrected_nonterminal_segment_rows_sha256",
    "corrected_positive_width_nonterminal_base_segment_count_certified",
    "corrected_source_chart_replay_mode_histogram",
    "corrected_source_chart_same_table_segment_count_certified",
    "corrected_source_chart_segment_count_certified", "corrected_source_chart_segment_rows_sha256",
    "corrected_source_chart_source_normal_union_segment_count_certified",
    "downstream_impact_rows", "downstream_impact_rows_sha256", "end_to_end_source_grazing_ray_closure_count",
    "endpoint_dyadic_ring_rows_sha256", "endpoint_dyadic_ring_strict_adjacent_source_normal_count",
    "global_Gate5", "new_immutable_F5_slot_count",
    "new_immutable_F6_slot_count", "positive_width_eta_c3_collar_count",
    "preserved_round109_registered_arc_whole_tube_count", "preserved_round110_two_sided_gap_pair_count",
    "producer_precision_bits", "rank3_face_local_maturity_after_correction", "ray_correction_rows",
    "ray_correction_rows_sha256", "remaining_pre_root_bracket_interval_tail_count",
    "remaining_pre_root_bracket_interval_tail_relative_width_per_ray",
    "round101_frozen_adjacent_segment_row_count_rebuilt",
    "round101_frozen_positive_width_adjacent_segment_row_count",
    "round101_frozen_source_chart_old_table_completeness_revalidated",
    "round101_frozen_source_chart_segment_row_count_rebuilt",
    "round101_remaining_open_exterior_ray_count_claim_revalidated",
    "round101_reported_adjacent_chart_segment_count", "round101_reported_source_chart_segment_count",
    "strict_nonclaims", "strict_separator",
    "terminal_base_segment_whole_closed_count", "unbridged_source_chart_transfer_seam_bracket_count",
    "unresolved_tight_algebraic_source_grazing_root_bracket_count", "upstream_and_executable_pins",
    "whole_collar_complete_57_candidate_ordering_count",
}
RAY_KEYS = {
    "actual_adjacent_parameter_interval", "actual_adjacent_parameter_width", "adjacent_source_chart",
    "branch_key", "certified_endpoint_dyadic_ring_prefix_count",
    "certified_positive_width_nonterminal_base_segment_count", "corrected_base_partition_count",
    "corrected_source_chart_replay_mode_histogram", "corrected_source_chart_segment_count_certified",
    "corrected_source_chart_segment_rows_sha256", "endpoint_dyadic_ring_rows_sha256",
    "endpoint_dyadic_ring_strict_adjacent_source_normal_count", "exterior_port_id",
    "first_physical_bracket_right_equals_tight_grazing_lower",
    "frozen_adjacent_segment_row_count", "frozen_full_segment_digest_independently_rebuilt",
    "frozen_source_chart_old_table_completeness_revalidated",
    "frozen_source_chart_same_table_complete_segment_count_revalidated",
    "frozen_source_chart_segment_row_count",
    "frozen_positive_width_adjacent_segment_row_count", "nonterminal_replay_mode_histogram",
    "nonterminal_segment_rows_sha256", "old_source_chart", "projective_end", "ray_index",
    "remaining_pre_root_bracket_interval_tail_parameter_interval",
    "remaining_pre_root_bracket_interval_tail_relative_width", "round101_stored_terminal_parameter_bracket",
    "round94_first_physical_terminal_parameter_bracket", "round94_tight_grazing_parameter_bracket",
    "source_chart_transfer_seam_whole_interval_bridged", "source_grazing_corner_status",
    "terminal_base_segment_whole_closed", "unbridged_source_chart_transfer_seam_bracket",
    "unbridged_source_chart_transfer_seam_bracket_width",
    "unresolved_tight_algebraic_source_grazing_root_bracket", "wrong_terminal_equals_seam_outer",
}
SAME_MODE = "SAME_CHART_CORRELATED_REPLAY"
SOURCE_UNION_MODE = "SOURCE_NORMAL_FOUR_CHART_UNION_CORRELATED_REPLAY"
OUTGOING_UNION_MODE = "OUTGOING_NORMAL_FOUR_CHART_UNION_CORRELATED_REPLAY"
EXPECTED_SOURCE_MODE_HISTOGRAM = {
    SAME_MODE: 1024,
    SOURCE_UNION_MODE: 8,
}
EXPECTED_ADJACENT_MODE_HISTOGRAM = {
    OUTGOING_UNION_MODE: 8,
    SAME_MODE: 496,
    SOURCE_UNION_MODE: 8,
}
EXPECTED_PER_RAY_ADJACENT_MODE_HISTOGRAM = {
    OUTGOING_UNION_MODE: 1,
    SAME_MODE: 62,
    SOURCE_UNION_MODE: 1,
}
EXPECTED_SOURCE_GRAZING_STATUS = (
    "PRE_ROOT_LOWER_END_TAIL_PLUS_SEPARATE_TIGHT_ALGEBRAIC_ROOT_BRACKET_OPEN__"
    "ROOT_CENTERED_ETA_C3_COLLAR_NOT_YET_CERTIFIED"
)
EXPECTED_SEPARATOR = (
    "Round101's frozen old-chart same-table claim fails on 8 terminal segments and its "
    "adjacent terminal was the transfer seam, producing 520 zero-width rows; corrected "
    "source rows have 1,024 same-table plus 8 four-chart-union replays, and the corrected "
    "open adjacent intervals have 512/520 positive-width base cells certified plus "
    "32 dyadic endpoint rings per ray, while 8 source-chart transfer seam brackets, 8 "
    "pre-root-bracket lower-end tails, 8 separate tight algebraic grazing-root brackets, and all "
    "positive-width (eta,c3) collars remain open"
)
EXPECTED_NONCLAIMS = [
    "rebuilding all 1,032 frozen source rows does not preserve the old same-table completeness claim on its 8 source-normal-seam terminal enclosures",
    "the fixed dyadic ring prefix is not an infinite exhaustion proof",
    "the pre-root-bracket interval tail stops at grazing_inner and is not a root-centred exhaustion or evidence that source cosine tends to zero",
    "the Round93 old-chart inner to adjacent-chart seam-outer bracket is not whole-interval bridged",
    "end-to-end closure is therefore 0/8 even though 512 corrected nonterminal adjacent base cells replay",
    "no positive-width root-centred (eta,c3) collar is constructed",
    "no countable H_{sigma,k} ownership theorem, canonical recut, F5, or F6 slot is installed",
    "the preserved Round109/110 internal computations do not restore endpoint-complete faces",
]
EXPECTED_IMPACT_ROWS_SHA256 = "e0eb1bf4323f3d0d4c90ec9a751a0213f807af8f2a0e992a6fe24d50d07593bf"


def digest(value: Any) -> str:
    text = json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)
    return hashlib.sha256(text.encode()).hexdigest()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rational(value: Any, label: str) -> Q:
    try:
        return Q(value)
    except (TypeError, ValueError, ZeroDivisionError) as exc:
        raise RuntimeError(f"invalid rational field: {label}") from exc


def strict_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def reject_nonfinite(token: str) -> Any:
    raise ValueError(f"nonfinite JSON number: {token}")


def load_strict(text: str) -> dict[str, Any]:
    value = json.loads(text, object_pairs_hook=strict_pairs, parse_constant=reject_nonfinite)
    if not isinstance(value, dict):
        raise RuntimeError("JSON document is not an object")
    return value


def load_inputs() -> dict[str, dict[str, Any]]:
    for name, expected in PINS.items():
        if sha256(HERE / name) != expected:
            raise RuntimeError(f"pin mismatch: {name}")
    documents = {}
    for alias, name in FILES.items():
        value = load_strict((HERE / name).read_text(encoding="utf-8"))
        if set(value) != {"schema", "result", "result_sha256"}:
            raise RuntimeError(f"open upstream document: {name}")
        if value["schema"] != SCHEMAS[alias] or value["result_sha256"] != digest(value["result"]):
            raise RuntimeError(f"upstream closure mismatch: {name}")
        documents[alias] = value["result"]
    return documents


def independent_chart(normal: Any) -> str:
    x_value, y_value = normal
    abs_x, abs_y = abs(x_value.value), abs(y_value.value)
    if bool(abs_x > abs_y):
        if bool(x_value.value > 0):
            return "E"
        if bool(x_value.value < 0):
            return "W"
    if bool(abs_y > abs_x):
        if bool(y_value.value > 0):
            return "N"
        if bool(y_value.value < 0):
            return "S"
    raise RuntimeError("correlated chart seam")


def independent_state(source: Any, branch: tuple[Any, ...], q_value: Any, path: tuple[int, int, int]) -> dict[str, Any]:
    normal, direction, offset = round95.tangent(branch, q_value)
    hit2, normal2 = round95.line_hit(normal, direction, offset, branch[1], path[0])
    incoming2 = round95.reflect(direction, normal2)
    hit1, normal1, flight1 = round95.ray_hit(
        hit2, round95.scale(-1, incoming2), source.target_id, path[1]
    )
    initial = round95.reflect(incoming2, normal1)
    hit0, normal0, flight0 = round95.ray_hit(
        hit1, round95.scale(-1, initial), f"{source.source}[0,0]", path[2]
    )
    contact = round95.sub(
        round95.center(branch[2]),
        round95.scale(branch[3] * round95.radius(branch[2]), normal),
    )
    tangent_flight = round95.dot(direction, round95.sub(contact, hit2))
    return {
        "hit0": hit0, "normal0": normal0, "initial": initial, "flight0": flight0,
        "hit1": hit1, "outgoing1": incoming2, "normal1": normal1, "flight1": flight1,
        "hit2": hit2, "outgoing2": direction, "normal2": normal2,
        "tangent_flight": tangent_flight,
    }


def independent_clear(point: Any, velocity: Any, target: str, terminal: Any, stage: str) -> str:
    delta = round95.sub(round95.center(target), point)
    ell = round95.dot(velocity, delta)
    transverse = round95.cross(velocity, delta)
    radius = round95.radius(target)
    line_clear = transverse * transverse - radius * radius
    end_clear = (ell - terminal) * (ell - terminal) + transverse * transverse - radius * radius
    if strict_sign(line_clear.value) == 1:
        return "WHOLE_LINE_MISS"
    if bool(ell.value < 0):
        return "CLOSEST_BEHIND_START"
    if bool(ell.value > terminal.value) and strict_sign(end_clear.value) == 1:
        return "CLOSEST_AFTER_TERMINAL__END_CLEAR"
    raise RuntimeError(f"{stage} competitor unresolved: {target}")


def centered_state(source: Any, branch: tuple[Any, ...], qa: Q, qb: Q) -> tuple[tuple[int, int, int], dict[str, Any]]:
    lo, hi = min(qa, qb), max(qa, qb)
    middle, radius = (lo + hi) / 2, (hi - lo) / 2
    path = round95.discover_path(source, branch, middle)
    q_value = round95.Centered.variable(
        aq(middle), round91.qball(lo, hi), arb(0, aq(radius).upper())
    )
    state = independent_state(source, branch, q_value, path)
    for terminal in (state["flight0"], state["flight1"], state["tangent_flight"]):
        if not bool(terminal.value > 0) or not bool(terminal.value < aq(Q(3))):
            raise RuntimeError("selected flight is not strict")
    return path, state


def independent_same_chart(source: Any, branch: tuple[Any, ...], qa: Q, qb: Q) -> dict[str, Any]:
    path, state = centered_state(source, branch, qa, qb)
    first_rows = []
    for target in first_hit.candidate_ids(source.chart_id):
        if target not in {source.target_id, f"{source.source}[0,0]"}:
            first_rows.append((target, independent_clear(state["hit0"], state["initial"], target, state["flight0"], "first")))
    chart1 = independent_chart(state["normal1"])
    second_rows = []
    for target in time2.translated_candidate_ids(source.target_id, chart1):
        if target not in {branch[1], source.target_id}:
            second_rows.append((target, independent_clear(state["hit1"], state["outgoing1"], target, state["flight1"], "second")))
    chart2 = independent_chart(state["normal2"])
    third_rows = []
    for target in time2.translated_candidate_ids(branch[1], chart2):
        if target not in {branch[2], branch[1]}:
            third_rows.append((target, independent_clear(state["hit2"], state["outgoing2"], target, state["tangent_flight"], "third")))
    return {
        "reverse_path": list(path),
        "first_outgoing_chart": chart1,
        "second_outgoing_chart": chart2,
        "complete_first_competitor_rows_sha256": digest(first_rows),
        "complete_second_competitor_rows_sha256": digest(second_rows),
        "complete_third_competitor_rows_sha256": digest(third_rows),
    }


def independent_union_chart(source: Any, branch: tuple[Any, ...], qa: Q, qb: Q) -> dict[str, Any]:
    path, state = centered_state(source, branch, qa, qb)
    first_rows = []
    for target in first_hit.candidate_ids(source.chart_id):
        if target not in {source.target_id, f"{source.source}[0,0]"}:
            first_rows.append((target, independent_clear(state["hit0"], state["initial"], target, state["flight0"], "first-union")))
    second_ids: set[str] = set()
    third_ids: set[str] = set()
    for chart in ("E", "W", "N", "S"):
        second_ids.update(time2.translated_candidate_ids(source.target_id, chart))
        third_ids.update(time2.translated_candidate_ids(branch[1], chart))
    second_rows = [
        (target, independent_clear(state["hit1"], state["outgoing1"], target, state["flight1"], "second-union"))
        for target in sorted(second_ids - {branch[1], source.target_id})
    ]
    third_rows = [
        (target, independent_clear(state["hit2"], state["outgoing2"], target, state["tangent_flight"], "third-union"))
        for target in sorted(third_ids - {branch[2], branch[1]})
    ]
    first_rows.sort()
    return {
        "reverse_path": list(path),
        "representation_seam_policy": "UNION_OF_E_W_N_S_IMMUTABLE_CANDIDATE_TABLES",
        "first_candidate_row_count": len(first_rows),
        "second_candidate_union_size": len(second_ids),
        "third_candidate_union_size": len(third_ids),
        "complete_first_competitor_rows_sha256": digest(first_rows),
        "complete_second_union_competitor_rows_sha256": digest(second_rows),
        "complete_third_union_competitor_rows_sha256": digest(third_rows),
    }


def independent_source_normal_union_chart(
    source: Any, branch: tuple[Any, ...], qa: Q, qb: Q,
) -> dict[str, Any]:
    path, state = centered_state(source, branch, qa, qb)
    first_ids: set[str] = set()
    for chart in ("E", "W", "N", "S"):
        first_ids.update(first_hit.candidate_ids(f"{source.source}:{chart}"))
    first_rows = [
        (target, independent_clear(state["hit0"], state["initial"], target, state["flight0"], "first-source-union"))
        for target in sorted(first_ids - {source.target_id, f"{source.source}[0,0]"})
    ]
    chart1 = independent_chart(state["normal1"])
    second_rows = []
    for target in time2.translated_candidate_ids(source.target_id, chart1):
        if target not in {branch[1], source.target_id}:
            second_rows.append((target, independent_clear(state["hit1"], state["outgoing1"], target, state["flight1"], "second-source-union")))
    chart2 = independent_chart(state["normal2"])
    third_rows = []
    for target in time2.translated_candidate_ids(branch[1], chart2):
        if target not in {branch[2], branch[1]}:
            third_rows.append((target, independent_clear(state["hit2"], state["outgoing2"], target, state["tangent_flight"], "third-source-union")))
    if len(first_rows) != 75:
        raise RuntimeError("independent source-normal union census mismatch")
    return {
        "reverse_path": list(path),
        "source_representation_seam_policy": "UNION_OF_E_W_N_S_FIRST_HIT_CANDIDATE_TABLES",
        "first_candidate_union_size": len(first_ids),
        "first_candidate_row_count": len(first_rows),
        "first_outgoing_chart": chart1,
        "second_outgoing_chart": chart2,
        "complete_first_union_competitor_rows_sha256": digest(first_rows),
        "complete_second_competitor_rows_sha256": digest(second_rows),
        "complete_third_competitor_rows_sha256": digest(third_rows),
    }


def frozen_row(source: Any, branch: tuple[Any, ...], qa: Q, qb: Q, layer: str) -> dict[str, Any]:
    return {
        "q_interval": [str(qa), str(qb)],
        "source_chart": source.chart_id,
        **independent_same_chart(source, branch, qa, qb),
        "layer": layer,
    }


def validate_static(result: dict[str, Any]) -> None:
    if set(result) != RESULT_KEYS:
        raise RuntimeError("Round111 result key mismatch")
    if result["upstream_and_executable_pins"] != PINS:
        raise RuntimeError("Round111 pin ledger mismatch")
    required = {
        "producer_precision_bits": 512,
        "audited_round101_ray_count": 8,
        "round101_reported_source_chart_segment_count": 1032,
        "round101_frozen_source_chart_segment_row_count_rebuilt": 1032,
        "round101_frozen_source_chart_old_table_completeness_revalidated": False,
        "corrected_source_chart_segment_count_certified": 1032,
        "corrected_source_chart_same_table_segment_count_certified": 1024,
        "corrected_source_chart_source_normal_union_segment_count_certified": 8,
        "corrected_source_chart_replay_mode_histogram": EXPECTED_SOURCE_MODE_HISTOGRAM,
        "round101_reported_adjacent_chart_segment_count": 520,
        "round101_frozen_adjacent_segment_row_count_rebuilt": 520,
        "round101_frozen_positive_width_adjacent_segment_row_count": 0,
        "round101_remaining_open_exterior_ray_count_claim_revalidated": False,
        "corrected_actual_positive_width_adjacent_base_segment_count": 520,
        "corrected_positive_width_nonterminal_base_segment_count_certified": 512,
        "corrected_nonterminal_replay_mode_histogram": EXPECTED_ADJACENT_MODE_HISTOGRAM,
        "terminal_base_segment_whole_closed_count": 0,
        "certified_endpoint_dyadic_ring_prefix_per_ray": 32,
        "certified_endpoint_dyadic_ring_count": 256,
        "endpoint_dyadic_ring_strict_adjacent_source_normal_count": 256,
        "remaining_pre_root_bracket_interval_tail_count": 8,
        "remaining_pre_root_bracket_interval_tail_relative_width_per_ray": "1/4294967296",
        "unresolved_tight_algebraic_source_grazing_root_bracket_count": 8,
        "unbridged_source_chart_transfer_seam_bracket_count": 8,
        "end_to_end_source_grazing_ray_closure_count": 0,
        "positive_width_eta_c3_collar_count": 0,
        "whole_collar_complete_57_candidate_ordering_count": 0,
        "preserved_round109_registered_arc_whole_tube_count": 52,
        "preserved_round110_two_sided_gap_pair_count": 56,
        "rank3_face_local_maturity_after_correction": "FACE_METADATA_ONLY__ACTUAL_HOMOGENEOUS_CHILD_MATURITY_0/18",
        "new_immutable_F5_slot_count": 0,
        "new_immutable_F6_slot_count": 0,
        "complete_18_field_operator_block_count": 0,
        "global_Gate5": "10/18__BLOCKS_0__NO_PROMOTION",
        "CM2": "NO-GO_FOR_CLAIM",
    }
    for key, expected in required.items():
        if result[key] != expected:
            raise RuntimeError(f"Round111 static semantic mismatch: {key}")
    if result["strict_separator"] != EXPECTED_SEPARATOR:
        raise RuntimeError("strict separator mismatch")
    if result["strict_nonclaims"] != EXPECTED_NONCLAIMS:
        raise RuntimeError("strict nonclaim ledger mismatch")
    rows = result["ray_correction_rows"]
    if len(rows) != 8 or result["ray_correction_rows_sha256"] != digest(rows):
        raise RuntimeError("Round111 ray-row closure mismatch")
    for index, row in enumerate(rows):
        if set(row) != RAY_KEYS or row["ray_index"] != index:
            raise RuntimeError("Round111 ray-row schema/order mismatch")
        first = row["round94_first_physical_terminal_parameter_bracket"]
        tight = row["round94_tight_grazing_parameter_bracket"]
        actual = row["actual_adjacent_parameter_interval"]
        bridge = row["unbridged_source_chart_transfer_seam_bracket"]
        residual = row["remaining_pre_root_bracket_interval_tail_parameter_interval"]
        if any(not isinstance(pair, list) or len(pair) != 2 for pair in (first, tight, actual, bridge, residual)):
            raise RuntimeError("ray interval schema mismatch")
        first_q = [rational(value, "first bracket") for value in first]
        tight_q = [rational(value, "tight bracket") for value in tight]
        actual_q = [rational(value, "actual interval") for value in actual]
        bridge_q = [rational(value, "bridge bracket") for value in bridge]
        residual_q = [rational(value, "residual interval") for value in residual]
        if not (
            first_q == actual_q
            and first_q[1] == tight_q[0]
            and tight_q[0] < tight_q[1]
            and row["round101_stored_terminal_parameter_bracket"] == first
            and row["unresolved_tight_algebraic_source_grazing_root_bracket"] == tight
        ):
            raise RuntimeError("nested bracket relationship mismatch")
        if row["actual_adjacent_parameter_width"] != str(actual_q[1] - actual_q[0]):
            raise RuntimeError("actual adjacent width mismatch")
        if bridge_q[1] != actual_q[0] or row["unbridged_source_chart_transfer_seam_bracket_width"] != str(bridge_q[1] - bridge_q[0]):
            raise RuntimeError("source-chart bridge width mismatch")
        terminal_cell_width = (actual_q[1] - actual_q[0]) / Q(65)
        expected_residual = actual_q[1] - terminal_cell_width / Q(2 ** ENDPOINT_RING_PREFIX)
        if residual_q != [expected_residual, actual_q[1]]:
            raise RuntimeError("pre-root residual arithmetic mismatch")
        fixed = {
            "wrong_terminal_equals_seam_outer": True,
            "first_physical_bracket_right_equals_tight_grazing_lower": True,
            "frozen_source_chart_segment_row_count": 129,
            "frozen_source_chart_same_table_complete_segment_count_revalidated": 128,
            "frozen_source_chart_old_table_completeness_revalidated": False,
            "corrected_source_chart_segment_count_certified": 129,
            "corrected_source_chart_replay_mode_histogram": {SAME_MODE: 128, SOURCE_UNION_MODE: 1},
            "frozen_adjacent_segment_row_count": 65,
            "frozen_positive_width_adjacent_segment_row_count": 0,
            "frozen_full_segment_digest_independently_rebuilt": True,
            "corrected_base_partition_count": 65,
            "certified_positive_width_nonterminal_base_segment_count": 64,
            "nonterminal_replay_mode_histogram": EXPECTED_PER_RAY_ADJACENT_MODE_HISTOGRAM,
            "terminal_base_segment_whole_closed": False,
            "certified_endpoint_dyadic_ring_prefix_count": 32,
            "endpoint_dyadic_ring_strict_adjacent_source_normal_count": 32,
            "remaining_pre_root_bracket_interval_tail_relative_width": "1/4294967296",
            "source_chart_transfer_seam_whole_interval_bridged": False,
            "source_grazing_corner_status": EXPECTED_SOURCE_GRAZING_STATUS,
        }
        for key, expected in fixed.items():
            if row[key] != expected:
                raise RuntimeError(f"ray static semantic mismatch: {key}")
        if row["old_source_chart"] == row["adjacent_source_chart"]:
            raise RuntimeError("old/adjacent source chart distinction lost")
    impacts = result["downstream_impact_rows"]
    if (
        len(impacts) != 10
        or [row.get("round") for row in impacts] != list(range(101, 111))
        or any(set(row) != {"round", "status", "preserved", "affected"} for row in impacts)
    ):
        raise RuntimeError("impact census mismatch")
    if (
        result["downstream_impact_rows_sha256"] != digest(impacts)
        or digest(impacts) != EXPECTED_IMPACT_ROWS_SHA256
    ):
        raise RuntimeError("impact digest mismatch")


def replay_all(result: dict[str, Any]) -> dict[str, Any]:
    ctx.prec = PRECISION_BITS
    docs = load_inputs()
    by_port = {row["registered_port_id"]: row for row in docs["r87"]["port_event_rows"]}
    physical = {
        port_id: by_port[port_id]
        for port_id in docs["r99"]["corrected_locally_physical_registered_port_ids"]
    }
    transfers = {row["exterior_port_id"]: row for row in docs["r94"]["transfer_rows"]}
    frozen_by_index = {row["ray_index"]: row for row in docs["r101"]["ray_rows"]}
    cores = core_cert.physical_cores()
    round91.round87.WORK_CORES = cores
    all_source_corrections = []
    all_nonterminal = []
    all_rings = []
    source_mode_histogram: Counter[str] = Counter()
    mode_histogram: Counter[str] = Counter()
    frozen_digest_rebuilds = zero_rows = ring_strict_adjacent_normals = 0

    for stored in result["ray_correction_rows"]:
        index = stored["ray_index"]
        frozen = frozen_by_index[index]
        branch = tuple(frozen["branch_key"])
        port_id = frozen["exterior_port_id"]
        transfer = transfers[port_id]
        q0, direction, cell_edge, inner, seam_outer, event, _, _ = round93.isolate_event(
            branch, frozen["projective_end"], port_id, physical, cores
        )
        if event != "SOURCE_CHART_SEAM":
            raise RuntimeError("independent source seam mismatch")
        source = cores[branch[0]]
        source_bounds = [
            cell_edge + (inner - cell_edge) * Q(i, round93.PROBE_COUNT + 1)
            for i in range(round93.PROBE_COUNT + 2)
        ]
        frozen_source_rows = [
            frozen_row(source, branch, q0 + direction * a, q0 + direction * b, "SOURCE_CHART")
            for a, b in zip(source_bounds, source_bounds[1:])
        ]
        source_correction_rows = []
        for segment_index, (lower, upper) in enumerate(zip(source_bounds, source_bounds[1:])):
            qa, qb = q0 + direction * lower, q0 + direction * upper
            _path0, source_state = centered_state(source, branch, qa, qb)
            try:
                chart0 = independent_chart(source_state["normal0"])
            except RuntimeError as exc:
                if str(exc) != "correlated chart seam":
                    raise
                evidence = independent_source_normal_union_chart(source, branch, qa, qb)
                mode = SOURCE_UNION_MODE
            else:
                if chart0 != source.chart_id.split(":")[1]:
                    raise RuntimeError("independent old-chart source normal mismatch")
                evidence = independent_same_chart(source, branch, qa, qb)
                mode = SAME_MODE
            correction = {
                "segment_index": segment_index,
                "parameter_interval": [str(lower), str(upper)],
                "q_interval": [str(qa), str(qb)],
                "source_chart": source.chart_id,
                "strictly_positive_parameter_width": lower < upper,
                "replay_mode": mode,
                "evidence": evidence,
            }
            source_correction_rows.append(correction)
            all_source_corrections.append({"ray_index": index, **correction})
            source_mode_histogram[mode] += 1
        adjacent = replace(source, chart_id=f"{source.source}:{transfer['adjacent_source_chart']}")
        wrong = Q(transfer["first_physical_terminal_event_parameter_bracket"][0])
        if wrong != seam_outer:
            raise RuntimeError("independent Round101 collapse mismatch")
        wrong_evidence = frozen_row(
            adjacent, branch, q0 + direction * seam_outer, q0 + direction * seam_outer,
            "ADJACENT_CHART",
        )
        frozen_rows = [*frozen_source_rows, *([wrong_evidence] * 65)]
        if digest(frozen_rows) != frozen["certified_segment_rows_sha256"]:
            raise RuntimeError("independent Round101 full segment digest mismatch")
        frozen_digest_rebuilds += 1
        zero_rows += 65

        first_bracket = list(map(Q, transfer["first_physical_terminal_event_parameter_bracket"]))
        grazing = list(map(Q, transfer["transferred_grazing_parameter_bracket"]))
        if first_bracket != [seam_outer, grazing[0]] or not grazing[0] < grazing[1]:
            raise RuntimeError("independent bracket relationship mismatch")
        bounds = [
            seam_outer + (grazing[0] - seam_outer) * Q(i, round94.PROBE_COUNT + 1)
            for i in range(round94.PROBE_COUNT + 2)
        ]
        nonterminal_rows = []
        for segment_index, (lower, upper) in enumerate(zip(bounds[:-2], bounds[1:-1])):
            qa, qb = q0 + direction * lower, q0 + direction * upper
            _path0, source_state = centered_state(adjacent, branch, qa, qb)
            try:
                chart0 = independent_chart(source_state["normal0"])
            except RuntimeError as exc:
                if str(exc) != "correlated chart seam":
                    raise
                evidence = independent_source_normal_union_chart(adjacent, branch, qa, qb)
                mode = SOURCE_UNION_MODE
            else:
                if chart0 != adjacent.chart_id.split(":")[1]:
                    raise RuntimeError("independent source normal chart mismatch")
                try:
                    evidence = independent_same_chart(adjacent, branch, qa, qb)
                    mode = SAME_MODE
                except RuntimeError as exc:
                    if str(exc) != "correlated chart seam":
                        raise
                    evidence = independent_union_chart(adjacent, branch, qa, qb)
                    mode = OUTGOING_UNION_MODE
            row = {
                "segment_index": segment_index,
                "parameter_interval": [str(lower), str(upper)],
                "q_interval": [str(qa), str(qb)],
                "strictly_positive_parameter_width": lower < upper,
                "replay_mode": mode,
                "evidence": evidence,
            }
            nonterminal_rows.append(row)
            all_nonterminal.append({"ray_index": index, **row})
            mode_histogram[mode] += 1
        if digest(nonterminal_rows) != stored["nonterminal_segment_rows_sha256"]:
            raise RuntimeError("independent nonterminal row digest mismatch")

        terminal_start, terminal = bounds[-2], grazing[0]
        terminal_width = terminal - terminal_start
        ring_rows = []
        for ring_index in range(ENDPOINT_RING_PREFIX):
            lower = terminal - terminal_width / Q(2 ** ring_index)
            upper = terminal - terminal_width / Q(2 ** (ring_index + 1))
            qa, qb = q0 + direction * lower, q0 + direction * upper
            _ring_path, ring_state = centered_state(adjacent, branch, qa, qb)
            try:
                ring_chart = independent_chart(ring_state["normal0"])
            except RuntimeError as exc:
                raise RuntimeError("endpoint-ring source normal is not strict adjacent") from exc
            if ring_chart != transfer["adjacent_source_chart"]:
                raise RuntimeError("endpoint-ring source normal left the adjacent chart")
            ring_strict_adjacent_normals += 1
            ring = {
                "ring_index": ring_index,
                "parameter_interval": [str(lower), str(upper)],
                "q_interval": [str(qa), str(qb)],
                "strictly_positive_parameter_width": lower < upper,
                "replay_mode": SAME_MODE,
                "evidence": independent_same_chart(adjacent, branch, qa, qb),
            }
            ring_rows.append(ring)
            all_rings.append({"ray_index": index, **ring})
        residual = terminal - terminal_width / Q(2 ** ENDPOINT_RING_PREFIX)
        expected = {
            "ray_index": index,
            "exterior_port_id": port_id,
            "branch_key": list(branch),
            "projective_end": frozen["projective_end"],
            "old_source_chart": transfer["old_source_chart"],
            "adjacent_source_chart": transfer["adjacent_source_chart"],
            "round101_stored_terminal_parameter_bracket": frozen["terminal_event_parameter_bracket"],
            "round94_first_physical_terminal_parameter_bracket": transfer["first_physical_terminal_event_parameter_bracket"],
            "round94_tight_grazing_parameter_bracket": transfer["transferred_grazing_parameter_bracket"],
            "wrong_terminal_equals_seam_outer": True,
            "first_physical_bracket_right_equals_tight_grazing_lower": True,
            "frozen_source_chart_segment_row_count": len(frozen_source_rows),
            "frozen_source_chart_same_table_complete_segment_count_revalidated": sum(
                row["replay_mode"] == SAME_MODE for row in source_correction_rows
            ),
            "frozen_source_chart_old_table_completeness_revalidated": False,
            "corrected_source_chart_segment_count_certified": len(source_correction_rows),
            "corrected_source_chart_replay_mode_histogram": dict(sorted(Counter(
                row["replay_mode"] for row in source_correction_rows
            ).items())),
            "corrected_source_chart_segment_rows_sha256": digest(source_correction_rows),
            "frozen_adjacent_segment_row_count": 65,
            "frozen_positive_width_adjacent_segment_row_count": 0,
            "frozen_full_segment_digest_independently_rebuilt": True,
            "actual_adjacent_parameter_interval": [str(seam_outer), str(terminal)],
            "actual_adjacent_parameter_width": str(terminal - seam_outer),
            "unbridged_source_chart_transfer_seam_bracket": [str(inner), str(seam_outer)],
            "unbridged_source_chart_transfer_seam_bracket_width": str(seam_outer - inner),
            "source_chart_transfer_seam_whole_interval_bridged": False,
            "corrected_base_partition_count": 65,
            "certified_positive_width_nonterminal_base_segment_count": len(nonterminal_rows),
            "nonterminal_replay_mode_histogram": dict(sorted(Counter(
                row["replay_mode"] for row in nonterminal_rows
            ).items())),
            "nonterminal_segment_rows_sha256": digest(nonterminal_rows),
            "terminal_base_segment_whole_closed": False,
            "certified_endpoint_dyadic_ring_prefix_count": len(ring_rows),
            "endpoint_dyadic_ring_strict_adjacent_source_normal_count": len(ring_rows),
            "endpoint_dyadic_ring_rows_sha256": digest(ring_rows),
            "remaining_pre_root_bracket_interval_tail_parameter_interval": [str(residual), str(terminal)],
            "remaining_pre_root_bracket_interval_tail_relative_width": str(Q(1, 2 ** ENDPOINT_RING_PREFIX)),
            "unresolved_tight_algebraic_source_grazing_root_bracket": list(map(str, grazing)),
            "source_grazing_corner_status": EXPECTED_SOURCE_GRAZING_STATUS,
        }
        if stored != expected:
            differing = sorted(key for key in RAY_KEYS if stored.get(key) != expected.get(key))
            raise RuntimeError(f"independent complete ray metadata mismatch: {differing}")

    if digest(all_source_corrections) != result["corrected_source_chart_segment_rows_sha256"]:
        raise RuntimeError("aggregate source-correction digest mismatch")
    if digest(all_nonterminal) != result["corrected_nonterminal_segment_rows_sha256"]:
        raise RuntimeError("aggregate nonterminal digest mismatch")
    if digest(all_rings) != result["endpoint_dyadic_ring_rows_sha256"]:
        raise RuntimeError("aggregate endpoint-ring digest mismatch")
    if source_mode_histogram != Counter(EXPECTED_SOURCE_MODE_HISTOGRAM):
        raise RuntimeError("independent source-correction mode histogram mismatch")
    if mode_histogram != Counter(EXPECTED_ADJACENT_MODE_HISTOGRAM):
        raise RuntimeError("independent mode histogram mismatch")
    if ring_strict_adjacent_normals != 256:
        raise RuntimeError("endpoint-ring strict adjacent source-normal census mismatch")
    return {
        "frozen_round101_full_segment_digest_rebuild_count": frozen_digest_rebuilds,
        "frozen_round101_source_segment_row_rebuild_count": len(all_source_corrections),
        "corrected_source_segment_replay_count": len(all_source_corrections),
        "corrected_source_same_chart_replay_count": source_mode_histogram[SAME_MODE],
        "corrected_source_normal_four_chart_union_replay_count": source_mode_histogram[SOURCE_UNION_MODE],
        "confirmed_zero_width_adjacent_row_count": zero_rows,
        "corrected_positive_width_nonterminal_base_segment_replay_count": len(all_nonterminal),
        "adjacent_source_normal_four_chart_union_replay_count": mode_histogram[SOURCE_UNION_MODE],
        "adjacent_outgoing_normal_four_chart_union_replay_count": mode_histogram[OUTGOING_UNION_MODE],
        "endpoint_dyadic_ring_replay_count": len(all_rings),
        "endpoint_dyadic_ring_strict_adjacent_source_normal_count": ring_strict_adjacent_normals,
        "unbridged_source_chart_transfer_seam_bracket_count": 8,
        "unresolved_tight_algebraic_grazing_root_bracket_count": 8,
    }


def verify(document: dict[str, Any], run_replay: bool = True, run_attacks: bool = True) -> dict[str, Any]:
    if set(document) != {"schema", "result", "result_sha256"}:
        raise RuntimeError("unknown or missing top-level key")
    if document["schema"] != SCHEMA or document["result_sha256"] != digest(document["result"]):
        raise RuntimeError("Round111 producer closure mismatch")
    result = document["result"]
    validate_static(result)
    replay = replay_all(result) if run_replay else {}
    verification = {
        "verifier_precision_bits": PRECISION_BITS,
        "producer_module_imported": False,
        **replay,
        "downstream_impact_row_count": len(result["downstream_impact_rows"]),
        "end_to_end_source_grazing_ray_closure_count": 0,
        "positive_width_eta_c3_collar_count": 0,
        "global_Gate5": "10/18__BLOCKS_0__NO_PROMOTION",
        "CM2": "NO-GO_FOR_CLAIM",
        "verdict": "ROUND101_ZERO_WIDTH_DEFECT_CONFIRMED__PARTIAL_CORRECTION_REPLAYED__8_ENDPOINT_CHAINS_STILL_OPEN",
    }
    if run_attacks:
        attacks = []
        mutations = (
            ("round101_frozen_positive_width_adjacent_segment_row_count", 1),
            ("corrected_positive_width_nonterminal_base_segment_count_certified", 520),
            ("end_to_end_source_grazing_ray_closure_count", 8),
            ("remaining_pre_root_bracket_interval_tail_count", 0),
            ("unresolved_tight_algebraic_source_grazing_root_bracket_count", 0),
            ("positive_width_eta_c3_collar_count", 8),
            ("preserved_round109_registered_arc_whole_tube_count", 51),
            ("global_Gate5", "CERTIFIED"),
        )
        for key, value in mutations:
            mutation = copy.deepcopy(document)
            mutation["result"][key] = value
            mutation["result_sha256"] = digest(mutation["result"])
            attacks.append(mutation)
        nested_width = copy.deepcopy(document)
        nested_width["result"]["ray_correction_rows"][0]["actual_adjacent_parameter_width"] = "999"
        nested_width["result"]["ray_correction_rows_sha256"] = digest(
            nested_width["result"]["ray_correction_rows"]
        )
        nested_width["result_sha256"] = digest(nested_width["result"])
        attacks.append(nested_width)
        nested_count = copy.deepcopy(document)
        nested_count["result"]["ray_correction_rows"][0]["corrected_base_partition_count"] = 64
        nested_count["result"]["ray_correction_rows_sha256"] = digest(
            nested_count["result"]["ray_correction_rows"]
        )
        nested_count["result_sha256"] = digest(nested_count["result"])
        attacks.append(nested_count)
        impact_status = copy.deepcopy(document)
        impact_status["result"]["downstream_impact_rows"][-1]["status"] = "PROMOTED"
        impact_status["result"]["downstream_impact_rows_sha256"] = digest(
            impact_status["result"]["downstream_impact_rows"]
        )
        impact_status["result_sha256"] = digest(impact_status["result"])
        attacks.append(impact_status)
        nonclaim_deletion = copy.deepcopy(document)
        nonclaim_deletion["result"]["strict_nonclaims"] = nonclaim_deletion["result"]["strict_nonclaims"][1:]
        nonclaim_deletion["result_sha256"] = digest(nonclaim_deletion["result"])
        attacks.append(nonclaim_deletion)
        rejected = 0
        for attack in attacks:
            try:
                verify(attack, run_replay=False, run_attacks=False)
            except RuntimeError:
                rejected += 1
        if rejected != len(attacks):
            raise RuntimeError("hostile semantic mutation escaped")
        strict_attacks = [
            '{"schema":"x","schema":"y","result":{},"result_sha256":"z"}',
            '{"schema":"x","result":{"bad":NaN},"result_sha256":"z"}',
            json.dumps({**document, "unknown": True}),
        ]
        strict_rejected = 0
        for raw in strict_attacks:
            try:
                verify(load_strict(raw), run_replay=False, run_attacks=False)
            except (RuntimeError, ValueError):
                strict_rejected += 1
        if strict_rejected != len(strict_attacks):
            raise RuntimeError("strict JSON attack escaped")
        verification["hostile_semantic_mutations_rejected"] = rejected
        verification["strict_json_attacks_rejected"] = strict_rejected
    return verification


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=CERT)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.input == CERT and sha256(CERT) != CERT_SHA256:
        raise RuntimeError("Round111 certificate byte pin mismatch")
    document = load_strict(args.input.read_text(encoding="utf-8"))
    result = verify(document)
    wrapped = {"schema": VERIFY_SCHEMA, "result": result, "result_sha256": digest(result)}
    rendered = json.dumps(wrapped, sort_keys=True, indent=2, allow_nan=False) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
