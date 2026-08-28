#!/usr/bin/env python3
"""Cacheless independent verifier for the Round289 tail materialization.

The Round289 producer is pinned as inert bytes and is never imported or
executed.  Starting only from frozen Round268, Round275, Round280, Round282,
and Round283 artifacts, this verifier independently reconstructs the exact
half-open children, sign corridors, full ten-field signature bindings, and
all Round275-region/residual-cell dispositions.  The stored Round289 ledger
is inspected only after the expected ledgers have been reconstructed.

The verification is deliberately ZERO-CREDIT.  Analytic tail closure does
not itself identify a physical expanded occurrence and therefore cannot
create a same-point seam edge, component union, or maximality credit.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from copy import deepcopy
from fractions import Fraction as Q
import gzip
import hashlib
import io
import json
import os
from pathlib import Path
import random
import sys
import tempfile
from typing import Any, Callable


HERE = Path(__file__).resolve().parent
PREFIX = "cm2_round289_source_g_outgoing_seam_tail_child_materialization"
PRODUCER = HERE / f"{PREFIX}.py"
LEDGER = HERE / f"{PREFIX}_ledger.json.gz"
RESULT = HERE / f"{PREFIX}_result.json"
OUTPUT = HERE / f"{PREFIX}_verification.json"

R268 = HERE / (
    "cm2_round268_source_g_true_seam_candidate_geometry_exhaustion_"
    "certificate.json"
)
R275 = HERE / (
    "cm2_round275_source_g_complete_reverse_rechart_materialization_"
    "certificate.json"
)
R280 = HERE / (
    "cm2_round280_source_g_true_seam_and_rechart_region_incidence_probe_"
    "patch_channels.json.gz"
)
R282_LEDGER = HERE / (
    "cm2_round282_source_g_strict_true_seam_normal_corridor_probe_ledger.json.gz"
)
R282_RESULT = HERE / (
    "cm2_round282_source_g_strict_true_seam_normal_corridor_probe_result.json"
)
R283_LEDGER = HERE / (
    "cm2_round283_source_g_outgoing_seam_tail_independent_probe_ledger.json.gz"
)
R283_RESULT = HERE / (
    "cm2_round283_source_g_outgoing_seam_tail_independent_probe_result.json"
)

VERIFICATION_SCHEMA = (
    "cm2.round289.source-g-outgoing-seam-tail-child-materialization."
    "verification.v1"
)
CANDIDATE_SCHEMA = (
    "cm2.round289.source-g-outgoing-seam-tail-child-materialization.v1"
)
LEDGER_SCHEMA = CANDIDATE_SCHEMA + ".ledger"

UPSTREAM_PINS = {
    "cm2_round268_source_g_true_seam_candidate_geometry_exhaustion.py":
        "d79f5e8b360fa494dd44968aa84ea1f108ced1645f05f6024a65e862686db71d",
    R268.name:
        "10d5e42f4353e981e7e8d5aacc002bed119453ee14a13398c524d5cb4ac2f7b9",
    "cm2_round268_source_g_true_seam_candidate_geometry_exhaustion_verification.json":
        "a1b43f9f81555a1f48d0593c941c6c5741b99b473649834635ee0ccabc8a53b6",
    "cm2_round268_source_g_true_seam_candidate_geometry_exhaustion_manifest.sha256":
        "d2d4c0c34cc25dd92626a656e3a08abb031190f168f4acfe11cd451d886a538f",
    R275.name:
        "e18935169614fc8b62ead3be7f60b383396ea1d2c52e8151457241f49e770386",
    R280.name:
        "074b27dd062844331d2d43a91283f5d467fe957123294719e32237fece05d814",
    R282_LEDGER.name:
        "6d94bce99b3ea57b8a568707705d9f16833cfba28b242a6dabb2de5933f6509e",
    R282_RESULT.name:
        "cd054a7036d9c482357611e9af11d028179e0f34a828dca2fbe91332b178f532",
    "cm2_round283_source_g_outgoing_seam_tail_independent_probe.py":
        "8e809f1e749408f36aa04edc06490a8b033a0da55a7e0d3454a99cf6d274bb1e",
    R283_RESULT.name:
        "29a1a48140136f105c2454771afa642794de10c61afc18bfbbefe88f0df70eca",
    R283_LEDGER.name:
        "2643a17cd325a16fabe8508a06b8666811641f837e8c2a2ea8a4a71ab982b786",
    "cm2_round283_source_g_outgoing_seam_tail_independent_probe_report.md":
        "697bcd1219790c7312b1331b4a3ec1409ff5e0c6508828da12d8f34e7e32c87a",
    "cm2_round283_source_g_outgoing_seam_tail_independent_probe_manifest.sha256":
        "2b8d58adf6d8857518e30ec5537e16003ac4d3c9900c10b13eaeb6f69bcc0f82",
}

ARTIFACT_PINS = {
    **UPSTREAM_PINS,
    PRODUCER.name:
        "e96cac6b48e333b19a44f50e50536c87b81b744b3b16bb0e28ae209cb965fffc",
    LEDGER.name:
        "6c5680574c17d50749d39fb25970b7fbcbc677f4f73029aca833f549c0ef5001",
    RESULT.name:
        "9091e06b8aca3d5e883621e0e3f701a6b90ce2f02b84f6813cef7727f45c516c",
}

DUAL_REPLAY_SEEDS = (289071, 289929)
GRAPH = "REGULAR_P_GRAPH_HALF_OPEN_OWNER"
ABSENCE = "STRICT_ZERO_ABSENT"
ACTUAL = "ACTUAL_INCIDENT_R275_REGION__SAME_SIGN_CONNECTED_GAP"
SEPARATED = "NOT_SEAM_INCIDENT__SEPARATED_BY_REGULAR_OUTGOING_GRAPH"
POSITIVE = "STRICT_POSITIVE"
NEGATIVE = "STRICT_NEGATIVE"

EXPECTED_CENSUS = {
    "input_true_seam_patch_universe_count": 152,
    "input_tail_patch_count": 24,
    "input_tail_directed_endpoint_count": 40,
    "input_guard_channel_incidence_count": 48,
    "preserved_two_guard_endpoint_count": 8,
    "Round282_residual_rational_cell_count": 540,
    "Round275_region_hit_count": 6596,
    "Round275_region_cell_incidence_count": 9528,
    "materialized_tail_child_count": 64,
    "regular_p_graph_child_count": 40,
    "strict_zero_absence_child_count": 24,
    "logical_s_equals_zero_split_count": 16,
    "exact_half_open_graph_owner_count": 40,
    "complete_sign_corridor_count": 104,
    "complete_signature_binding_count": 104,
    "actual_incident_Round275_region_count": 6500,
    "graph_separated_Round275_region_count": 96,
    "actual_incident_region_cell_relation_count": 9240,
    "graph_separated_region_cell_relation_count": 288,
    "remaining_analytic_tail_endpoint_count": 0,
    "remaining_analytic_tail_patch_count": 0,
}

EXPECTED_NONPROMOTION = {
    "expanded_occurrence_credit": 0,
    "seam_component_edge_credit": 0,
    "component_union_credit": 0,
    "maximality_credit": 0,
    "exact_key_fibre_credit": 0,
    "global_disposition_credit": 0,
    "Jx_Jy_same_point_glue_credit": 0,
    "quotient": 63224,
    "expanded_occurrences": 126468,
    "Gate5": "10/18",
    "D02": "BLOCKED",
    "CM2": "NO-GO_FOR_CLAIM",
}

ENCODER = json.JSONEncoder(
    sort_keys=True,
    separators=(",", ":"),
    ensure_ascii=False,
    allow_nan=False,
)


class VerificationError(RuntimeError):
    """Any failed frozen-input, reconstruction, or candidate invariant."""


def need(condition: bool, label: str) -> None:
    if not condition:
        raise VerificationError(label)


def canonical(value: Any) -> bytes:
    return ENCODER.encode(value).encode()


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def file_sha256(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    with path.open("rb") as handle:
        value = json.load(handle)
    need(isinstance(value, dict), f"{path.name}:top-level object")
    return value


def read_gzip_json(path: Path) -> dict[str, Any]:
    with gzip.open(path, "rb") as handle:
        value = json.load(handle)
    need(isinstance(value, dict), f"{path.name}:top-level object")
    return value


def deterministic_gzip_bytes(value: Any) -> bytes:
    output = io.BytesIO()
    with gzip.GzipFile(
        filename="", mode="wb", fileobj=output, mtime=0
    ) as handle:
        handle.write(canonical(value))
    return output.getvalue()


def qstr(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else str(value)


def close_row(payload: dict[str, Any]) -> dict[str, Any]:
    row = dict(payload)
    row["row_sha256"] = digest(row)
    return row


def positive_intersection(
    left: tuple[Q, Q, Q, Q],
    right: tuple[Q, Q, Q, Q],
) -> tuple[Q, Q, Q, Q] | None:
    p0, p1 = max(left[0], right[0]), min(left[1], right[1])
    s0, s1 = max(left[2], right[2]), min(left[3], right[3])
    return (p0, p1, s0, s1) if p0 < p1 and s0 < s1 else None


def area(rectangle: tuple[Q, Q, Q, Q]) -> Q:
    return (
        (rectangle[1] - rectangle[0])
        * (rectangle[3] - rectangle[2])
    )


def verify_closed_rows(
    label: str,
    ledger: dict[str, Any],
    id_field: str,
    expected_count: int,
) -> list[dict[str, Any]]:
    rows = ledger["rows"]
    need(isinstance(rows, list), f"{label}:rows list")
    need(
        ledger["row_count"] == len(rows) == expected_count,
        f"{label}:row count",
    )
    need(ledger["rows_sha256"] == digest(rows), f"{label}:rows digest")
    ids = [row[id_field] for row in rows]
    need(len(ids) == len(set(ids)), f"{label}:unique ids")
    need(ledger["row_ids_sha256"] == digest(ids), f"{label}:id digest")
    hashes: list[str] = []
    for row in rows:
        payload = dict(row)
        stored = payload.pop("row_sha256")
        need(stored == digest(payload), f"{label}:row closure:{row[id_field]}")
        hashes.append(stored)
    need(
        ledger["row_hashes_sha256"] == digest(hashes),
        f"{label}:row-hash digest",
    )
    return rows


def verify_result_closure(value: dict[str, Any], label: str) -> None:
    stored = value["result_sha256"]
    payload = {key: item for key, item in value.items() if key != "result_sha256"}
    need(stored == digest(payload), f"{label}:result digest")


def load_upstream() -> dict[str, Any]:
    """Load and close every frozen input without importing producer code."""
    r268_wrapper = read_json(R268)
    need(
        set(r268_wrapper) == {"schema", "result", "result_sha256"}
        and r268_wrapper["result_sha256"] == digest(r268_wrapper["result"]),
        "Round268 wrapper",
    )
    r268_result = r268_wrapper["result"]
    r268_rows = verify_closed_rows(
        "Round268 true seam patches",
        r268_result["formal_true_source_seam_positive_patch_ledger"],
        "true_seam_patch_row_id",
        152,
    )
    need(
        r268_result["census"]["strict_positive_area_same_point_patch_count"] == 152,
        "Round268 patch census",
    )
    patch_ids = {row["true_seam_patch_row_id"] for row in r268_rows}

    r275_wrapper = read_json(R275)
    need(
        set(r275_wrapper) == {"result", "result_sha256"}
        and r275_wrapper["result_sha256"] == digest(r275_wrapper["result"]),
        "Round275 wrapper",
    )
    r275_result = r275_wrapper["result"]
    strict_regions = verify_closed_rows(
        "Round275 strict regions",
        r275_result["strict_region_ledger"],
        "reverse_rechart_region_row_id",
        5288,
    )
    arrangement_regions = verify_closed_rows(
        "Round275 arrangement regions",
        r275_result["arrangement_region_ledger"],
        "reverse_rechart_region_row_id",
        8500,
    )
    region_rows: dict[str, dict[str, Any]] = {}
    for region in [*strict_regions, *arrangement_regions]:
        region_id = region["reverse_rechart_region_row_id"]
        need(region_id not in region_rows, f"Round275 duplicate region:{region_id}")
        box = tuple(map(Q, region["adjacent_rational_region_box"]))
        need(
            len(box) == 6
            and box[0] < box[1]
            and box[2] < box[3]
            and box[4] < box[5],
            f"Round275 positive region:{region_id}",
        )
        signature = region["local_return_signature"]
        need(
            len(signature) == 10
            and set(signature) == {
                "official_key_id",
                "official_key_ordinal",
                "official_key_row",
                "ordered_integer_wall_events",
                "outgoing_cell",
                "roof",
                "signed_wall_word",
                "source_chart",
                "target_chart",
                "target_lift",
            }
            and region["complete_10_field_return_signature_sha256"]
            == digest(signature),
            f"Round275 full signature:{region_id}",
        )
        region_rows[region_id] = region
    need(len(region_rows) == 13788, "Round275 region universe")

    r280_doc = read_gzip_json(R280)
    r280_rows = verify_closed_rows(
        "Round280 patch channels",
        r280_doc,
        "Round268_patch_channel_row_id",
        152,
    )
    patch_channels = {
        row["Round268_true_seam_patch_row_id"]: row for row in r280_rows
    }
    need(
        len(patch_channels) == 152 and set(patch_channels) == patch_ids,
        "Round280 patch universe",
    )

    r282_result = read_json(R282_RESULT)
    verify_result_closure(r282_result, "Round282")
    r282_doc = read_gzip_json(R282_LEDGER)
    r282_rows = verify_closed_rows(
        "Round282 seam corridors",
        r282_doc,
        "Round282_seam_corridor_row_id",
        152,
    )
    r282_by_patch = {
        row["Round268_true_seam_patch_row_id"]: row for row in r282_rows
    }
    need(
        len(r282_by_patch) == 152 and set(r282_by_patch) == patch_ids,
        "Round282 patch universe",
    )
    partial_sides = {
        (row["Round268_true_seam_patch_row_id"], side_index)
        for row in r282_rows
        for side_index, side in enumerate(row["side_corridors"])
        if side["classification"]
        == "PARTIAL_STRICT_COVER__ARRANGEMENT_TAIL_FAIL_CLOSED"
    }
    tail_patches = {
        row["Round268_true_seam_patch_row_id"]
        for row in r282_rows
        if row["classification"]
        == "SEAM_PATCH_REMAINS_FAIL_CLOSED_FOR_ARRANGEMENT_TAIL"
    }
    need(
        len(partial_sides) == 40
        and len(tail_patches) == 24
        and r282_result["census"]["remaining_arrangement_tail_patch_count"] == 24,
        "Round282 tail census",
    )

    r283_result = read_json(R283_RESULT)
    verify_result_closure(r283_result, "Round283")
    r283_doc = read_gzip_json(R283_LEDGER)
    endpoints = verify_closed_rows(
        "Round283 analytic endpoints",
        r283_doc,
        "Round283_endpoint_row_id",
        40,
    )
    endpoint_keys = {
        (row["Round268_true_seam_patch_row_id"], row["side_index"])
        for row in endpoints
    }
    need(
        endpoint_keys == partial_sides
        and {
            row["Round268_true_seam_patch_row_id"] for row in endpoints
        } == tail_patches,
        "Round283 endpoint identity with Round282 tails",
    )
    need(
        sum(row["candidate_guard_channel_count"] for row in endpoints) == 48
        and sum(row["candidate_guard_channel_count"] == 2 for row in endpoints)
        == 8
        and sum(
            row["Round282_residual_rational_cell_count"] for row in endpoints
        ) == 540
        and all(
            row["analytic_tail_residual_after_regular_graph_partition"] == "0"
            for row in endpoints
        ),
        "Round283 analytic census",
    )
    need(
        r283_result["census"]["input_failclosed_patch_count"] == 24
        and r283_result["census"]["input_failclosed_directed_endpoint_count"] == 40
        and r283_result["census"]["candidate_guard_channel_incidence_count"] == 48
        and r283_result["census"]["Round282_residual_rational_ps_cell_count"]
        == 540,
        "Round283 result census",
    )

    for endpoint in endpoints:
        patch_id = endpoint["Round268_true_seam_patch_row_id"]
        side_index = endpoint["side_index"]
        patch = r282_by_patch[patch_id]
        channel = patch_channels[patch_id]
        need(
            endpoint["patch_ps_rectangle"]
            == [
                *patch["exact_common_p_interval"],
                *patch["exact_common_s_interval"],
            ]
            and endpoint["patch_ps_rectangle"]
            == [
                *channel["exact_common_p_interval"],
                *channel["exact_common_s_interval"],
            ],
            f"endpoint patch rectangle:{endpoint['Round283_endpoint_row_id']}",
        )
        side282 = patch["side_corridors"][side_index]
        side280 = channel["side_channel_rows"][side_index]
        need(
            endpoint["side"] == side282["side"] == side280["side"]
            and endpoint["source_chart"]
            == side282["source_chart"] == side280["source_chart"]
            and endpoint["adjacent_chart"]
            == side282["adjacent_chart"] == side280["adjacent_chart"],
            f"endpoint side channel:{endpoint['Round283_endpoint_row_id']}",
        )
        cells = [
            tuple(map(Q, cell))
            for cell in endpoint["Round282_residual_rational_cells"]
        ]
        need(
            len(cells) == endpoint["Round282_residual_rational_cell_count"]
            and all(area(cell) > 0 for cell in cells)
            and len(set(cells)) == len(cells),
            f"endpoint residual cells:{endpoint['Round283_endpoint_row_id']}",
        )
        for left_index, left in enumerate(cells):
            for right in cells[left_index + 1:]:
                need(
                    positive_intersection(left, right) is None,
                    f"endpoint disjoint residual cells:{endpoint['Round283_endpoint_row_id']}",
                )

    return {
        "patch_ids": patch_ids,
        "regions": region_rows,
        "patch_channels": patch_channels,
        "r282_by_patch": r282_by_patch,
        "endpoints": endpoints,
    }


def derive_children(
    endpoint: dict[str, Any],
    guard: dict[str, Any],
) -> list[dict[str, Any]]:
    """Independently derive the guard's exact half-open child rectangles."""
    patch_rectangle = tuple(map(Q, endpoint["patch_ps_rectangle"]))
    guard_class = guard["classification"]
    base = {
        "source_guard_row_id": guard["source_guard_row_id"],
        "source_round": guard["source_round"],
        "parent_id": guard["parent_id"],
        "owner_target": guard["owner_target"],
        "source_chart": guard["source_chart"],
        "adjacent_chart": guard["adjacent_chart"],
        "algebraic_root_sign": guard["algebraic_root_sign"],
        "normal_gap_outer_box": guard["normal_gap_outer_box"],
        "whole_gap_derivative_signs_t_p_s":
            guard["whole_gap_derivative_signs_t_p_s"],
        "sole_dynamic_gap_reason": guard["sole_dynamic_gap_reason"],
    }
    if guard_class == "FULL_S_BASE_REGULAR_P_GRAPH":
        need(
            set(guard["seam_p_face_signs"]) == {NEGATIVE, POSITIVE}
            and guard["connected_sign_corridor_count"] == 2,
            "full graph signs",
        )
        return [{
            **base,
            "_rectangle": patch_rectangle,
            "child_classification": GRAPH,
            "seam_signs_present": [NEGATIVE, POSITIVE],
            "strict_absence_sign": None,
            "owns_s_equals_zero_boundary": False,
            "s_half_open_semantics": "UNSPLIT",
            "p_lower_face_sign": guard["seam_p_face_signs"][0],
        }]
    if guard_class == "STRICT_ZERO_ABSENT":
        need(
            len(set(guard["seam_p_face_signs"])) == 1
            and guard["connected_sign_corridor_count"] == 1,
            "full absence sign",
        )
        sign = guard["seam_p_face_signs"][0]
        return [{
            **base,
            "_rectangle": patch_rectangle,
            "child_classification": ABSENCE,
            "seam_signs_present": [sign],
            "strict_absence_sign": sign,
            "owns_s_equals_zero_boundary": False,
            "s_half_open_semantics": "UNSPLIT",
            "p_lower_face_sign": sign,
        }]

    need(
        guard_class == "P_ENDPOINT_REGULAR_GRAPH__EXACT_S0_SPLIT"
        and guard["logical_s_split_count"] == 1
        and len(guard["half_open_split_rows"]) == 2,
        "split guard classification",
    )
    children: list[dict[str, Any]] = []
    for split in guard["half_open_split_rows"]:
        s0, s1 = map(Q, split["half_open_s_interval"])
        is_graph = split["classification"] == GRAPH
        signs = split["p_face_signs_at_witness"]
        need(
            (is_graph and set(signs) == {NEGATIVE, POSITIVE})
            or (not is_graph and split["classification"] == ABSENCE
                and len(set(signs)) == 1),
            "split child signs",
        )
        need(s1 == 0 or s0 == 0, "split boundary at s=0")
        owns_s0 = is_graph
        if s1 == 0:
            semantics = (
                "LOWER_S_CHILD_INCLUDES_S0"
                if owns_s0 else "LOWER_S_CHILD_EXCLUDES_S0"
            )
        else:
            semantics = (
                "UPPER_S_CHILD_INCLUDES_S0"
                if owns_s0 else "UPPER_S_CHILD_EXCLUDES_S0"
            )
        children.append({
            **base,
            "_rectangle": (
                patch_rectangle[0], patch_rectangle[1], s0, s1
            ),
            "child_classification": split["classification"],
            "seam_signs_present":
                [NEGATIVE, POSITIVE] if is_graph else [signs[0]],
            "strict_absence_sign": None if is_graph else signs[0],
            "owns_s_equals_zero_boundary": owns_s0,
            "s_half_open_semantics": semantics,
            "p_lower_face_sign": signs[0],
        })
    need(
        sum(child["owns_s_equals_zero_boundary"] for child in children) == 1,
        "split has unique s=0 owner",
    )
    graph_child = next(child for child in children if child["child_classification"] == GRAPH)
    absence_child = next(
        child for child in children if child["child_classification"] == ABSENCE
    )
    need(
        graph_child["_rectangle"][3] == absence_child["_rectangle"][2]
        or absence_child["_rectangle"][3] == graph_child["_rectangle"][2],
        "split children meet only at s=0",
    )
    return children


def outgoing_sign(region: dict[str, Any]) -> str:
    cell = region["local_return_signature"]["outgoing_cell"]
    sign = POSITIVE if cell in {"E", "W"} else NEGATIVE
    if "active_factor_side_sign" in region:
        need(
            region["active_reason"] == "outgoing_chart_seam"
            and region["active_factor_side_sign"] == sign,
            f"arrangement sign:{region['reverse_rechart_region_row_id']}",
        )
    return sign


def reconstruct(
    upstream: dict[str, Any],
    replay_seed: int,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Rebuild all three Round289 ledgers with exact rational arithmetic."""
    rng = random.Random(replay_seed)
    regions = upstream["regions"]
    patch_channels = upstream["patch_channels"]
    endpoints = list(upstream["endpoints"])
    rng.shuffle(endpoints)

    child_work: dict[str, dict[str, Any]] = {}
    children_by_guard: dict[tuple[str, int, str], list[str]] = defaultdict(list)
    endpoint_work: list[dict[str, Any]] = []
    split_guard_count = 0

    for endpoint in endpoints:
        patch_id = endpoint["Round268_true_seam_patch_row_id"]
        side_index = endpoint["side_index"]
        endpoint_child_ids: list[str] = []
        guards = list(endpoint["guard_channel_rows"])
        rng.shuffle(guards)
        for guard in guards:
            derived = derive_children(endpoint, guard)
            split_guard_count += int(len(derived) == 2)
            # Child index is defined by the frozen split-row order, not replay
            # traversal order.  Re-derive that order directly.
            canonical_children = derive_children(endpoint, guard)
            for template_index, child in enumerate(canonical_children):
                rectangle = child["_rectangle"]
                child_id = "round289-tail-child:" + digest([
                    patch_id,
                    side_index,
                    child["source_guard_row_id"],
                    template_index,
                    [qstr(value) for value in rectangle],
                    child["child_classification"],
                ])
                need(child_id not in child_work, f"unique child:{child_id}")
                child.update({
                    "Round289_tail_child_row_id": child_id,
                    "Round283_endpoint_row_id":
                        endpoint["Round283_endpoint_row_id"],
                    "Round268_true_seam_patch_row_id": patch_id,
                    "side_index": side_index,
                    "side": endpoint["side"],
                    "exact_half_open_ps_rectangle":
                        [qstr(value) for value in rectangle],
                    "_relations": [],
                })
                child_work[child_id] = child
                children_by_guard[
                    (patch_id, side_index, child["source_guard_row_id"])
                ].append(child_id)
                endpoint_child_ids.append(child_id)
        residuals = [
            (index, tuple(map(Q, cell)))
            for index, cell in enumerate(
                endpoint["Round282_residual_rational_cells"]
            )
        ]
        endpoint_work.append({
            "endpoint": endpoint,
            "child_ids": endpoint_child_ids,
            "residuals": residuals,
        })

    need(
        len(child_work) == 64 and split_guard_count == 16,
        "reconstructed child/split census",
    )

    relation_rows: list[dict[str, Any]] = []
    endpoint_rows: list[dict[str, Any]] = []
    unique_hits: set[tuple[str, int, str]] = set()
    unique_actual: set[tuple[str, int, str]] = set()
    unique_separated: set[tuple[str, int, str]] = set()
    disposition_histogram: Counter[str] = Counter()
    signed_disposition_histogram: Counter[tuple[str, str]] = Counter()

    rng.shuffle(endpoint_work)
    for item in endpoint_work:
        endpoint = item["endpoint"]
        patch_id = endpoint["Round268_true_seam_patch_row_id"]
        side_index = endpoint["side_index"]
        channel = patch_channels[patch_id]["side_channel_rows"][side_index]
        candidate_region_ids = list(channel["candidate_Round275_region_ids"])
        rng.shuffle(candidate_region_ids)
        residuals = list(item["residuals"])
        rng.shuffle(residuals)

        endpoint_relation_ids: list[str] = []
        hit_ids: set[str] = set()
        actual_ids: set[str] = set()
        separated_ids: set[str] = set()
        for region_id in candidate_region_ids:
            region = regions[region_id]
            box = tuple(map(Q, region["adjacent_rational_region_box"]))
            footprint = (box[2], box[3], box[4], box[5])
            region_has_hit = False
            for residual_index, residual in residuals:
                overlap = positive_intersection(footprint, residual)
                if overlap is None:
                    continue
                region_has_hit = True
                possible_children = children_by_guard.get(
                    (patch_id, side_index, region["source_guard_row_id"]),
                    [],
                )
                matching_children = [
                    child_id for child_id in possible_children
                    if positive_intersection(
                        child_work[child_id]["_rectangle"], overlap
                    ) is not None
                ]
                need(
                    len(matching_children) == 1,
                    f"unique child for incidence:{endpoint['Round283_endpoint_row_id']}",
                )
                child_id = matching_children[0]
                child = child_work[child_id]
                sign = outgoing_sign(region)
                is_graph = child["child_classification"] == GRAPH
                actual = is_graph or sign == child["strict_absence_sign"]
                disposition = ACTUAL if actual else SEPARATED
                relation_id = "round289-region-cell-incidence:" + digest([
                    endpoint["Round283_endpoint_row_id"],
                    child_id,
                    region_id,
                    residual_index,
                ])
                relation = close_row({
                    "Round289_region_cell_relation_id": relation_id,
                    "Round289_tail_child_row_id": child_id,
                    "Round283_endpoint_row_id":
                        endpoint["Round283_endpoint_row_id"],
                    "Round268_true_seam_patch_row_id": patch_id,
                    "side_index": side_index,
                    "source_guard_row_id": region["source_guard_row_id"],
                    "Round275_region_id": region_id,
                    "Round275_region_classification":
                        region.get("region_classification")
                        or region["arrangement_classification"],
                    "Round282_residual_cell_index": residual_index,
                    "exact_positive_ps_overlap":
                        [qstr(value) for value in overlap],
                    "exact_positive_ps_overlap_area": qstr(area(overlap)),
                    "active_outgoing_equality_sign": sign,
                    "complete_10_field_return_signature_sha256":
                        region["complete_10_field_return_signature_sha256"],
                    "disposition": disposition,
                    "actual_seam_incidence": actual,
                    "occurrence_credit": 0,
                    "component_edge_credit": 0,
                })
                relation_rows.append(relation)
                child["_relations"].append(relation)
                endpoint_relation_ids.append(relation_id)
                disposition_histogram[disposition] += 1
                signed_disposition_histogram[(disposition, sign)] += 1
                if actual:
                    actual_ids.add(region_id)
                    unique_actual.add((patch_id, side_index, region_id))
                else:
                    separated_ids.add(region_id)
                    unique_separated.add((patch_id, side_index, region_id))
            if region_has_hit:
                hit_ids.add(region_id)
                unique_hits.add((patch_id, side_index, region_id))

        need(
            len(hit_ids) == endpoint["candidate_Round275_region_hit_count"]
            and digest(sorted(hit_ids))
            == endpoint["candidate_Round275_region_ids_sha256"],
            f"Round283 hit binding:{endpoint['Round283_endpoint_row_id']}",
        )
        endpoint_rows.append(close_row({
            "Round289_endpoint_conservation_row_id":
                "round289-endpoint-conservation:"
                + digest(endpoint["Round283_endpoint_row_id"]),
            "Round283_endpoint_row_id": endpoint["Round283_endpoint_row_id"],
            "Round268_true_seam_patch_row_id": patch_id,
            "side_index": side_index,
            "tail_child_ids": sorted(item["child_ids"]),
            "tail_child_count": len(item["child_ids"]),
            "Round282_residual_cell_count": len(item["residuals"]),
            "Round275_region_hit_count": len(hit_ids),
            "Round275_region_hit_ids": sorted(hit_ids),
            "actual_incident_Round275_region_count": len(actual_ids),
            "actual_incident_Round275_region_ids": sorted(actual_ids),
            "graph_separated_Round275_region_count": len(separated_ids),
            "graph_separated_Round275_region_ids": sorted(separated_ids),
            "region_cell_relation_count": len(endpoint_relation_ids),
            "region_cell_relation_ids": sorted(endpoint_relation_ids),
            "analytic_tail_residual": 0,
            "component_edge_credit": 0,
        }))

    relation_rows.sort(key=lambda row: row["Round289_region_cell_relation_id"])
    child_rows: list[dict[str, Any]] = []
    sign_corridor_count = 0
    signature_binding_count = 0
    graph_owner_count = 0
    s0_owner_count = 0
    class_histogram: Counter[str] = Counter()
    actual_relation_count = 0
    separated_relation_count = 0

    for child_id in sorted(child_work):
        child = child_work[child_id]
        rectangle = child.pop("_rectangle")
        need(
            child["exact_half_open_ps_rectangle"]
            == [qstr(value) for value in rectangle],
            f"child rectangle:{child_id}",
        )
        relations = child.pop("_relations")
        is_graph = child["child_classification"] == GRAPH
        class_histogram[child["child_classification"]] += 1
        sign_corridors: list[dict[str, Any]] = []
        for sign in child["seam_signs_present"]:
            incident = [
                relation for relation in relations
                if relation["actual_seam_incidence"]
                and relation["active_outgoing_equality_sign"] == sign
            ]
            need(incident, f"nonempty sign corridor:{child_id}:{sign}")
            by_signature: dict[str, list[dict[str, Any]]] = defaultdict(list)
            for relation in incident:
                by_signature[
                    relation["complete_10_field_return_signature_sha256"]
                ].append(relation)
            bindings: list[dict[str, Any]] = []
            for signature_hash in sorted(by_signature):
                bound_relations = by_signature[signature_hash]
                region_ids = sorted({
                    relation["Round275_region_id"]
                    for relation in bound_relations
                })
                objects = {
                    canonical(regions[region_id]["local_return_signature"])
                    for region_id in region_ids
                }
                need(
                    len(objects) == 1,
                    f"signature object unique:{child_id}:{signature_hash}",
                )
                signature = regions[region_ids[0]]["local_return_signature"]
                need(
                    len(signature) == 10 and digest(signature) == signature_hash,
                    f"complete signature binding:{child_id}:{signature_hash}",
                )
                bindings.append({
                    "complete_10_field_return_signature_sha256":
                        signature_hash,
                    "complete_10_field_return_signature": signature,
                    "actual_incident_Round275_region_count": len(region_ids),
                    "actual_incident_Round275_region_ids": region_ids,
                    "actual_incident_region_cell_relation_count":
                        len(bound_relations),
                    "actual_incident_region_cell_relation_ids": sorted(
                        relation["Round289_region_cell_relation_id"]
                        for relation in bound_relations
                    ),
                })
            signature_binding_count += len(bindings)
            incident_region_ids = sorted({
                relation["Round275_region_id"] for relation in incident
            })
            incident_relation_ids = sorted(
                relation["Round289_region_cell_relation_id"]
                for relation in incident
            )
            sign_corridors.append({
                "active_outgoing_equality_sign": sign,
                "half_open_zero_graph_included":
                    is_graph and sign == child["p_lower_face_sign"],
                "zero_graph_owner_rule":
                    "P_LOWER_SIGN_CORRIDOR_OWNS_F_EQUALS_ZERO"
                    if is_graph else "ZERO_SET_ABSENT",
                "connected_on_entire_seam_to_R275_gap": True,
                "actual_incident_Round275_region_count":
                    len(incident_region_ids),
                "actual_incident_Round275_region_ids": incident_region_ids,
                "actual_incident_region_cell_relation_count":
                    len(incident_relation_ids),
                "actual_incident_region_cell_relation_ids":
                    incident_relation_ids,
                "complete_signature_binding_count": len(bindings),
                "complete_signature_bindings": bindings,
                "occurrence_credit": 0,
                "component_edge_credit": 0,
            })
        sign_corridor_count += len(sign_corridors)
        graph_owner_count += int(is_graph)
        s0_owner_count += int(child["owns_s_equals_zero_boundary"])
        actual_relations = [
            relation for relation in relations
            if relation["actual_seam_incidence"]
        ]
        separated_relations = [
            relation for relation in relations
            if not relation["actual_seam_incidence"]
        ]
        actual_relation_count += len(actual_relations)
        separated_relation_count += len(separated_relations)
        child_rows.append(close_row({
            **child,
            "equation": "outgoing_normal_x^2-outgoing_normal_y^2=0",
            "regular_graph_axis": "p" if is_graph else None,
            "half_open_graph_owner_count": int(is_graph),
            "sign_corridor_count": len(sign_corridors),
            "sign_corridors": sign_corridors,
            "actual_incident_Round275_region_count": len({
                relation["Round275_region_id"] for relation in actual_relations
            }),
            "actual_incident_Round275_region_ids": sorted({
                relation["Round275_region_id"] for relation in actual_relations
            }),
            "actual_incident_region_cell_relation_count": len(actual_relations),
            "actual_incident_region_cell_relation_ids": sorted(
                relation["Round289_region_cell_relation_id"]
                for relation in actual_relations
            ),
            "graph_separated_Round275_region_count": len({
                relation["Round275_region_id"] for relation in separated_relations
            }),
            "graph_separated_Round275_region_ids": sorted({
                relation["Round275_region_id"] for relation in separated_relations
            }),
            "graph_separated_region_cell_relation_count":
                len(separated_relations),
            "graph_separated_region_cell_relation_ids": sorted(
                relation["Round289_region_cell_relation_id"]
                for relation in separated_relations
            ),
            "cross_return_branch_overlap_does_not_define_occurrence_identity":
                True,
            "expanded_occurrence_credit": 0,
            "seam_component_edge_credit": 0,
            "component_union_credit": 0,
            "maximality_credit": 0,
        }))

    endpoint_rows.sort(key=lambda row: row["Round289_endpoint_conservation_row_id"])
    need(
        class_histogram == {GRAPH: 40, ABSENCE: 24}
        and len(child_rows) == 64
        and sign_corridor_count == 104
        and signature_binding_count == 104
        and graph_owner_count == 40
        and s0_owner_count == 16,
        "child/corridor/binding census",
    )
    need(
        len(unique_hits) == 6596
        and len(relation_rows) == 9528
        and len(unique_actual) == 6500
        and len(unique_separated) == 96
        and not unique_actual.intersection(unique_separated),
        "region/relation conservation",
    )
    need(
        actual_relation_count == 9240
        and separated_relation_count == 288
        and disposition_histogram == {ACTUAL: 9240, SEPARATED: 288}
        and signed_disposition_histogram == {
            (ACTUAL, NEGATIVE): 4588,
            (ACTUAL, POSITIVE): 4652,
            (SEPARATED, NEGATIVE): 144,
            (SEPARATED, POSITIVE): 144,
        },
        "signed disposition conservation",
    )
    need(
        sum(row["Round282_residual_cell_count"] for row in endpoint_rows) == 540
        and all(row["analytic_tail_residual"] == 0 for row in endpoint_rows),
        "analytic residual zero",
    )

    expected_ledger = {
        "schema": LEDGER_SCHEMA,
        "child_ledger": {
            "row_count": len(child_rows),
            "rows": child_rows,
            "rows_sha256": digest(child_rows),
            "row_ids_sha256": digest([
                row["Round289_tail_child_row_id"] for row in child_rows
            ]),
            "row_hashes_sha256": digest([
                row["row_sha256"] for row in child_rows
            ]),
        },
        "region_cell_relation_ledger": {
            "row_count": len(relation_rows),
            "rows": relation_rows,
            "rows_sha256": digest(relation_rows),
            "row_ids_sha256": digest([
                row["Round289_region_cell_relation_id"] for row in relation_rows
            ]),
            "row_hashes_sha256": digest([
                row["row_sha256"] for row in relation_rows
            ]),
        },
        "endpoint_conservation_ledger": {
            "row_count": len(endpoint_rows),
            "rows": endpoint_rows,
            "rows_sha256": digest(endpoint_rows),
            "row_ids_sha256": digest([
                row["Round289_endpoint_conservation_row_id"]
                for row in endpoint_rows
            ]),
            "row_hashes_sha256": digest([
                row["row_sha256"] for row in endpoint_rows
            ]),
        },
    }
    reconstruction = {
        "census": EXPECTED_CENSUS,
        "relation_disposition_histogram": {
            ACTUAL: 9240,
            SEPARATED: 288,
        },
        "signed_relation_disposition_histogram": {
            "ACTUAL_NEGATIVE": 4588,
            "ACTUAL_POSITIVE": 4652,
            "SEPARATED_NEGATIVE": 144,
            "SEPARATED_POSITIVE": 144,
        },
        "child_rows_sha256":
            expected_ledger["child_ledger"]["rows_sha256"],
        "relation_rows_sha256":
            expected_ledger["region_cell_relation_ledger"]["rows_sha256"],
        "endpoint_rows_sha256":
            expected_ledger["endpoint_conservation_ledger"]["rows_sha256"],
        "ledger_sha256":
            hashlib.sha256(deterministic_gzip_bytes(expected_ledger)).hexdigest(),
    }
    return expected_ledger, reconstruction


def audit_candidate_ledger(
    ledger: dict[str, Any],
    expected: dict[str, Any],
) -> None:
    need(ledger["schema"] == LEDGER_SCHEMA, "candidate ledger schema")
    verify_closed_rows(
        "Round289 child ledger",
        ledger["child_ledger"],
        "Round289_tail_child_row_id",
        64,
    )
    verify_closed_rows(
        "Round289 relation ledger",
        ledger["region_cell_relation_ledger"],
        "Round289_region_cell_relation_id",
        9528,
    )
    verify_closed_rows(
        "Round289 endpoint ledger",
        ledger["endpoint_conservation_ledger"],
        "Round289_endpoint_conservation_row_id",
        40,
    )
    need(
        canonical(ledger) == canonical(expected),
        "candidate ledger differs from independent reconstruction",
    )


def audit_candidate_result(
    result: dict[str, Any],
    ledger: dict[str, Any],
    reconstruction: dict[str, Any],
) -> None:
    verify_result_closure(result, "Round289")
    need(result["schema"] == CANDIDATE_SCHEMA, "Round289 result schema")
    need(
        result["status"]
        == (
            "PASS_PRODUCER_ROUND289_OUTGOING_SEAM_TAIL_CHILD_MATERIALIZATION__"
            "ANALYTIC_RESIDUAL_ZERO__ZERO_CREDIT_PENDING_INDEPENDENT_VERIFIER"
        ),
        "Round289 producer-only status",
    )
    need(result["pins"] == UPSTREAM_PINS, "Round289 input pins")
    need(result["seed_affects_output"] is False, "Round289 seed contract")
    need(result["census"] == reconstruction["census"], "Round289 census")
    need(
        result["relation_disposition_histogram"]
        == reconstruction["relation_disposition_histogram"],
        "Round289 disposition histogram",
    )
    need(
        result["ledger"] == {
            "filename": LEDGER.name,
            "child_rows_sha256":
                ledger["child_ledger"]["rows_sha256"],
            "region_cell_relation_rows_sha256":
                ledger["region_cell_relation_ledger"]["rows_sha256"],
            "endpoint_conservation_rows_sha256":
                ledger["endpoint_conservation_ledger"]["rows_sha256"],
            "file_sha256":
                hashlib.sha256(deterministic_gzip_bytes(ledger)).hexdigest(),
        },
        "Round289 ledger bindings",
    )
    need(
        result["scope_contract"] == {
            "all_64_exact_half_open_children_materialized": True,
            "all_40_regular_graphs_have_one_frozen_owner": True,
            "all_16_s0_splits_own_s0_exactly_once": True,
            "all_104_sign_corridors_have_actual_Round275_region_IDs": True,
            "all_signature_bindings_contain_full_10_field_objects": True,
            "all_6596_region_hits_and_9528_cell_incidences_conserved": True,
            "eight_two_guard_endpoints_preserved_as_distinct_channels": True,
            "overlap_across_return_branches_is_not_occurrence_identity": True,
            "Jx_Jy_same_point_glue_credit": 0,
        },
        "Round289 scope contract",
    )
    need(
        result["strict_nonpromotion"] == EXPECTED_NONPROMOTION,
        "Round289 strict nonpromotion",
    )


def reclose_attacked(
    ledger: dict[str, Any],
    result: dict[str, Any],
) -> None:
    specifications = (
        ("child_ledger", "Round289_tail_child_row_id"),
        ("region_cell_relation_ledger", "Round289_region_cell_relation_id"),
        ("endpoint_conservation_ledger", "Round289_endpoint_conservation_row_id"),
    )
    for ledger_name, id_field in specifications:
        subledger = ledger[ledger_name]
        for row in subledger["rows"]:
            payload = dict(row)
            payload.pop("row_sha256", None)
            row["row_sha256"] = digest(payload)
        subledger["row_count"] = len(subledger["rows"])
        subledger["rows_sha256"] = digest(subledger["rows"])
        subledger["row_ids_sha256"] = digest([
            row[id_field] for row in subledger["rows"]
        ])
        subledger["row_hashes_sha256"] = digest([
            row["row_sha256"] for row in subledger["rows"]
        ])
    result["ledger"]["child_rows_sha256"] = (
        ledger["child_ledger"]["rows_sha256"]
    )
    result["ledger"]["region_cell_relation_rows_sha256"] = (
        ledger["region_cell_relation_ledger"]["rows_sha256"]
    )
    result["ledger"]["endpoint_conservation_rows_sha256"] = (
        ledger["endpoint_conservation_ledger"]["rows_sha256"]
    )
    result["ledger"]["file_sha256"] = hashlib.sha256(
        deterministic_gzip_bytes(ledger)
    ).hexdigest()
    payload = dict(result)
    payload.pop("result_sha256", None)
    result["result_sha256"] = digest(payload)


def run_attacks(
    ledger: dict[str, Any],
    result: dict[str, Any],
    expected: dict[str, Any],
    reconstruction: dict[str, Any],
) -> dict[str, Any]:
    def first_split_owner(l: dict[str, Any]) -> dict[str, Any]:
        return next(
            row for row in l["child_ledger"]["rows"]
            if row["owns_s_equals_zero_boundary"]
        )

    def first_graph(l: dict[str, Any]) -> dict[str, Any]:
        return next(
            row for row in l["child_ledger"]["rows"]
            if row["child_classification"] == GRAPH
        )

    def first_separated(l: dict[str, Any]) -> dict[str, Any]:
        return next(
            row for row in l["region_cell_relation_ledger"]["rows"]
            if not row["actual_seam_incidence"]
        )

    def first_two_guard_endpoint(l: dict[str, Any]) -> dict[str, Any]:
        return next(
            row for row in l["endpoint_conservation_ledger"]["rows"]
            if row["tail_child_count"] >= 2
        )

    attacks: list[
        tuple[str, Callable[[dict[str, Any], dict[str, Any]], None]]
    ] = [
        (
            "REMOVE_UNIQUE_S0_OWNER",
            lambda l, r: first_split_owner(l).__setitem__(
                "owns_s_equals_zero_boundary", False
            ),
        ),
        (
            "FORGE_S0_HALF_OPEN_SEMANTICS",
            lambda l, r: first_split_owner(l).__setitem__(
                "s_half_open_semantics", "BOTH_CHILDREN_INCLUDE_S0"
            ),
        ),
        (
            "COLLAPSE_TWO_GUARD_ENDPOINT",
            lambda l, r: first_two_guard_endpoint(l)["tail_child_ids"].pop(),
        ),
        (
            "FLIP_GRAPH_CHILD_TO_ABSENCE",
            lambda l, r: first_graph(l).__setitem__(
                "child_classification", ABSENCE
            ),
        ),
        (
            "REMOVE_GRAPH_ZERO_OWNER",
            lambda l, r: first_graph(l).__setitem__(
                "half_open_graph_owner_count", 0
            ),
        ),
        (
            "FLIP_RELATION_DISPOSITION",
            lambda l, r: first_separated(l).__setitem__(
                "disposition", ACTUAL
            ),
        ),
        (
            "PROMOTE_SEPARATED_RELATION_TO_INCIDENT",
            lambda l, r: first_separated(l).__setitem__(
                "actual_seam_incidence", True
            ),
        ),
        (
            "FORGE_RELATION_REGION_ID",
            lambda l, r: l["region_cell_relation_ledger"]["rows"][0].__setitem__(
                "Round275_region_id", "round275-strict-region:" + "0" * 64
            ),
        ),
        (
            "FORGE_RESIDUAL_CELL_INDEX",
            lambda l, r: l["region_cell_relation_ledger"]["rows"][0].__setitem__(
                "Round282_residual_cell_index", 999
            ),
        ),
        (
            "FLIP_ACTIVE_SIGN",
            lambda l, r: l["region_cell_relation_ledger"]["rows"][0].__setitem__(
                "active_outgoing_equality_sign", POSITIVE
                if l["region_cell_relation_ledger"]["rows"][0][
                    "active_outgoing_equality_sign"
                ] == NEGATIVE else NEGATIVE
            ),
        ),
        (
            "FORGE_SIGNATURE_DIGEST",
            lambda l, r: first_graph(l)["sign_corridors"][0][
                "complete_signature_bindings"
            ][0].__setitem__(
                "complete_10_field_return_signature_sha256", "0" * 64
            ),
        ),
        (
            "FORGE_TEN_FIELD_SIGNATURE_OBJECT",
            lambda l, r: first_graph(l)["sign_corridors"][0][
                "complete_signature_bindings"
            ][0]["complete_10_field_return_signature"].__setitem__(
                "roof", 999
            ),
        ),
        (
            "DROP_CORRIDOR_REGION_BINDING",
            lambda l, r: first_graph(l)["sign_corridors"][0][
                "actual_incident_Round275_region_ids"
            ].pop(),
        ),
        (
            "PROMOTE_CHILD_OCCURRENCE_CREDIT",
            lambda l, r: l["child_ledger"]["rows"][0].__setitem__(
                "expanded_occurrence_credit", 1
            ),
        ),
        (
            "PROMOTE_CHILD_SEAM_EDGE_CREDIT",
            lambda l, r: l["child_ledger"]["rows"][0].__setitem__(
                "seam_component_edge_credit", 1
            ),
        ),
        (
            "FORGE_ANALYTIC_RESIDUAL",
            lambda l, r: l["endpoint_conservation_ledger"]["rows"][0].__setitem__(
                "analytic_tail_residual", 1
            ),
        ),
        (
            "FORGE_RESULT_RELATION_CENSUS",
            lambda l, r: r["census"].__setitem__(
                "Round275_region_cell_incidence_count", 9527
            ),
        ),
        (
            "PROMOTE_RESULT_JX_JY_GLUE",
            lambda l, r: r["strict_nonpromotion"].__setitem__(
                "Jx_Jy_same_point_glue_credit", 1
            ),
        ),
        (
            "FORGE_RESULT_CM2_GO",
            lambda l, r: r["strict_nonpromotion"].__setitem__(
                "CM2", "UNCONDITIONAL_GO"
            ),
        ),
    ]
    rejected: list[str] = []
    for attack_id, mutate in attacks:
        attacked_ledger = deepcopy(ledger)
        attacked_result = deepcopy(result)
        mutate(attacked_ledger, attacked_result)
        reclose_attacked(attacked_ledger, attacked_result)
        try:
            audit_candidate_ledger(attacked_ledger, expected)
            audit_candidate_result(
                attacked_result, attacked_ledger, reconstruction
            )
        except (
            VerificationError,
            KeyError,
            IndexError,
            StopIteration,
            TypeError,
            ValueError,
        ):
            rejected.append(attack_id)
        else:
            raise VerificationError(f"attack accepted:{attack_id}")
    return {
        "attack_count": len(attacks),
        "rejected_count": len(rejected),
        "all_attacks_rejected": len(rejected) == len(attacks),
        "all_attacks_reclosed_at_row_ledger_and_result_levels": True,
        "rejected_attack_ids": rejected,
    }


def verify() -> dict[str, Any]:
    for filename, expected_hash in ARTIFACT_PINS.items():
        need(
            file_sha256(HERE / filename) == expected_hash,
            f"pin:{filename}",
        )
    need(
        PRODUCER.stem not in sys.modules,
        "Round289 producer imported",
    )

    upstream = load_upstream()
    expected_first, reconstruction_first = reconstruct(
        upstream, DUAL_REPLAY_SEEDS[0]
    )
    expected_second, reconstruction_second = reconstruct(
        upstream, DUAL_REPLAY_SEEDS[1]
    )
    need(
        expected_first == expected_second
        and reconstruction_first == reconstruction_second,
        "dual-seed reconstruction differs",
    )

    stored_ledger = read_gzip_json(LEDGER)
    stored_result = read_json(RESULT)
    need(
        deterministic_gzip_bytes(stored_ledger) == LEDGER.read_bytes(),
        "Round289 deterministic gzip bytes",
    )
    need(
        canonical(stored_result) + b"\n" == RESULT.read_bytes(),
        "Round289 canonical result bytes",
    )
    audit_candidate_ledger(stored_ledger, expected_first)
    audit_candidate_result(
        stored_result, stored_ledger, reconstruction_first
    )
    attacks = run_attacks(
        stored_ledger,
        stored_result,
        expected_first,
        reconstruction_first,
    )

    verification = {
        "schema": VERIFICATION_SCHEMA,
        "status": (
            "PASS_INDEPENDENT_ROUND289_OUTGOING_SEAM_TAIL_CHILD_"
            "MATERIALIZATION__64_CHILDREN__104_CORRIDORS__"
            "9528_RELATIONS__ANALYTIC_RESIDUAL_ZERO__ZERO_CREDIT"
        ),
        "pins": ARTIFACT_PINS,
        "independence_contract": {
            "Round289_producer_imported_or_executed": False,
            "Round289_producer_treated_only_as_pinned_inert_bytes": True,
            "cacheless_upstream_sources":
                ["Round268", "Round275", "Round280", "Round282", "Round283"],
            "exact_arithmetic": "fractions.Fraction",
            "candidate_ledger_read_only_after_expected_ledgers_reconstructed":
                True,
            "signature_hash_never_used_as_occurrence_identity": True,
        },
        "reconstruction": {
            **reconstruction_first,
            "tail_patch_count": 24,
            "tail_directed_endpoint_count": 40,
            "guard_channel_count": 48,
            "preserved_two_guard_endpoint_count": 8,
            "residual_rational_cell_count": 540,
            "materialized_child_count": 64,
            "regular_graph_child_count": 40,
            "strict_absence_child_count": 24,
            "unique_s_equals_zero_owner_count": 16,
            "complete_connected_sign_corridor_count": 104,
            "complete_ten_field_signature_binding_count": 104,
            "unique_Round275_region_hit_count": 6596,
            "actual_incident_unique_region_count": 6500,
            "graph_separated_unique_region_count": 96,
            "region_cell_relation_count": 9528,
            "actual_incident_relation_count": 9240,
            "graph_separated_relation_count": 288,
            "analytic_residual_endpoint_count": 0,
            "analytic_residual_patch_count": 0,
        },
        "dual_seed_replay": {
            "replay_seeds": list(DUAL_REPLAY_SEEDS),
            "input_iteration_order_independently_permuted": True,
            "reconstructed_ledgers_byte_identical": True,
            "reconstructed_ledger_sha256_by_seed": {
                str(seed): reconstruction_first["ledger_sha256"]
                for seed in DUAL_REPLAY_SEEDS
            },
            "external_PYTHONHASHSEED_replay_expected_byte_identical": True,
        },
        "attacks": attacks,
        "zero_credit_contract": {
            "expanded_occurrence_credit": 0,
            "seam_component_edge_credit": 0,
            "component_union_credit": 0,
            "maximality_credit": 0,
            "exact_key_fibre_credit": 0,
            "global_disposition_credit": 0,
            "Jx_Jy_same_point_glue_credit": 0,
            "analytic_tail_closure_is_not_occurrence_identity": True,
            "seam_edges_remain_blocked_until_both_sides_are_occurrence_bound":
                True,
        },
        "strict_nonpromotion": stored_result["strict_nonpromotion"],
    }
    verification["verification_sha256"] = digest(verification)
    return verification


def atomic_write(path: Path, payload: bytes) -> None:
    target = path if path.is_absolute() else Path.cwd() / path
    target.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(
        prefix="." + target.name + ".", dir=target.parent
    )
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, target)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument(
        "--seed",
        default="289071",
        help=(
            "Accepted for external PYTHONHASHSEED cold replay; verification "
            "bytes are deliberately seed-independent."
        ),
    )
    args = parser.parse_args()
    verification = verify()
    atomic_write(args.output, canonical(verification) + b"\n")


if __name__ == "__main__":
    main()
