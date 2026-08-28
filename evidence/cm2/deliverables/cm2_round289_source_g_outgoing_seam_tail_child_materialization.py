#!/usr/bin/env python3
"""Formal ZERO-CREDIT materialization of the Round282 outgoing-seam children.

This producer converts the frozen Round283 analytic census into 64 explicit
half-open children and binds every child sign corridor to actual frozen
Round275 region IDs and complete ten-field signatures.  It conserves all
Round282/Round283 overlap relations, but intentionally emits no occurrence or
component credit.  An independent verifier is still required.
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import io
import json
import os
import tempfile
from collections import Counter, defaultdict
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

import cm2_round283_source_g_outgoing_seam_tail_independent_probe as r283


HERE = Path(__file__).resolve().parent
PREFIX = "cm2_round289_source_g_outgoing_seam_tail_child_materialization"
OUTPUT = HERE / f"{PREFIX}_result.json"
LEDGER = HERE / f"{PREFIX}_ledger.json.gz"
SCHEMA = "cm2.round289.source-g-outgoing-seam-tail-child-materialization.v1"
PINS = {
    "cm2_round268_source_g_true_seam_candidate_geometry_exhaustion.py":
        "d79f5e8b360fa494dd44968aa84ea1f108ced1645f05f6024a65e862686db71d",
    "cm2_round268_source_g_true_seam_candidate_geometry_exhaustion_certificate.json":
        "10d5e42f4353e981e7e8d5aacc002bed119453ee14a13398c524d5cb4ac2f7b9",
    "cm2_round268_source_g_true_seam_candidate_geometry_exhaustion_verification.json":
        "a1b43f9f81555a1f48d0593c941c6c5741b99b473649834635ee0ccabc8a53b6",
    "cm2_round268_source_g_true_seam_candidate_geometry_exhaustion_manifest.sha256":
        "d2d4c0c34cc25dd92626a656e3a08abb031190f168f4acfe11cd451d886a538f",
    "cm2_round275_source_g_complete_reverse_rechart_materialization_certificate.json":
        "e18935169614fc8b62ead3be7f60b383396ea1d2c52e8151457241f49e770386",
    "cm2_round280_source_g_true_seam_and_rechart_region_incidence_probe_patch_channels.json.gz":
        "074b27dd062844331d2d43a91283f5d467fe957123294719e32237fece05d814",
    "cm2_round282_source_g_strict_true_seam_normal_corridor_probe_ledger.json.gz":
        "6d94bce99b3ea57b8a568707705d9f16833cfba28b242a6dabb2de5933f6509e",
    "cm2_round282_source_g_strict_true_seam_normal_corridor_probe_result.json":
        "cd054a7036d9c482357611e9af11d028179e0f34a828dca2fbe91332b178f532",
    "cm2_round283_source_g_outgoing_seam_tail_independent_probe.py":
        "8e809f1e749408f36aa04edc06490a8b033a0da55a7e0d3454a99cf6d274bb1e",
    "cm2_round283_source_g_outgoing_seam_tail_independent_probe_result.json":
        "29a1a48140136f105c2454771afa642794de10c61afc18bfbbefe88f0df70eca",
    "cm2_round283_source_g_outgoing_seam_tail_independent_probe_ledger.json.gz":
        "2643a17cd325a16fabe8508a06b8666811641f837e8c2a2ea8a4a71ab982b786",
    "cm2_round283_source_g_outgoing_seam_tail_independent_probe_report.md":
        "697bcd1219790c7312b1331b4a3ec1409ff5e0c6508828da12d8f34e7e32c87a",
    "cm2_round283_source_g_outgoing_seam_tail_independent_probe_manifest.sha256":
        "2b8d58adf6d8857518e30ec5537e16003ac4d3c9900c10b13eaeb6f69bcc0f82",
}


def canonical(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False,
        allow_nan=False,
    ).encode()


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def fsha(path: Path) -> str:
    result = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            result.update(block)
    return result.hexdigest()


def need(condition: bool, label: str) -> None:
    if not condition:
        raise RuntimeError(label)


def qstr(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else str(value)


def close(row: dict[str, Any]) -> dict[str, Any]:
    result = dict(row)
    result["row_sha256"] = digest(result)
    return result


def gzip_bytes(value: Any) -> bytes:
    output = io.BytesIO()
    with gzip.GzipFile(filename="", mode="wb", fileobj=output, mtime=0) as handle:
        handle.write(canonical(value))
    return output.getvalue()


def atomic(path: Path, payload: bytes) -> None:
    descriptor, temporary = tempfile.mkstemp(prefix="." + path.name + ".", dir=path.parent)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def load_gzip(path: Path) -> dict[str, Any]:
    with gzip.open(path, "rt") as handle:
        return json.load(handle)


def active_sign(region: dict[str, Any]) -> str:
    outgoing = region["local_return_signature"]["outgoing_cell"]
    result = (
        "STRICT_POSITIVE" if outgoing in {"E", "W"} else "STRICT_NEGATIVE"
    )
    if "active_factor_side_sign" in region:
        need(
            region["active_reason"] == "outgoing_chart_seam"
            and region["active_factor_side_sign"] == result,
            "arrangement sign agrees with full outgoing signature",
        )
    return result


def child_templates(
    endpoint: dict[str, Any], guard: dict[str, Any]
) -> list[dict[str, Any]]:
    patch_rectangle = tuple(map(Q, endpoint["patch_ps_rectangle"]))
    guard_id = guard["source_guard_row_id"]
    common = {
        "source_guard_row_id": guard_id,
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
    if guard["classification"] == "FULL_S_BASE_REGULAR_P_GRAPH":
        return [{
            **common,
            "ps_rectangle": patch_rectangle,
            "child_classification": "REGULAR_P_GRAPH_HALF_OPEN_OWNER",
            "seam_signs_present": ["STRICT_NEGATIVE", "STRICT_POSITIVE"],
            "strict_absence_sign": None,
            "owns_s_equals_zero_boundary": False,
            "s_half_open_semantics": "UNSPLIT",
            "p_lower_face_sign": guard["seam_p_face_signs"][0],
        }]
    if guard["classification"] == "STRICT_ZERO_ABSENT":
        need(
            len(set(guard["seam_p_face_signs"])) == 1,
            "whole absence sign",
        )
        return [{
            **common,
            "ps_rectangle": patch_rectangle,
            "child_classification": "STRICT_ZERO_ABSENT",
            "seam_signs_present": [guard["seam_p_face_signs"][0]],
            "strict_absence_sign": guard["seam_p_face_signs"][0],
            "owns_s_equals_zero_boundary": False,
            "s_half_open_semantics": "UNSPLIT",
            "p_lower_face_sign": guard["seam_p_face_signs"][0],
        }]

    need(
        guard["classification"]
        == "P_ENDPOINT_REGULAR_GRAPH__EXACT_S0_SPLIT"
        and len(guard["half_open_split_rows"]) == 2,
        "s0 split guard",
    )
    result = []
    for split in guard["half_open_split_rows"]:
        s0, s1 = map(Q, split["half_open_s_interval"])
        classification = split["classification"]
        is_graph = classification == "REGULAR_P_GRAPH_HALF_OPEN_OWNER"
        signs = split["p_face_signs_at_witness"]
        need(
            is_graph and set(signs) == {"STRICT_NEGATIVE", "STRICT_POSITIVE"}
            or not is_graph and len(set(signs)) == 1,
            "split child signs",
        )
        owns_s0 = is_graph
        if s1 == 0:
            semantics = (
                "LOWER_S_CHILD_INCLUDES_S0" if owns_s0
                else "LOWER_S_CHILD_EXCLUDES_S0"
            )
        else:
            need(s0 == 0, "split at s0")
            semantics = (
                "UPPER_S_CHILD_INCLUDES_S0" if owns_s0
                else "UPPER_S_CHILD_EXCLUDES_S0"
            )
        result.append({
            **common,
            "ps_rectangle": (
                patch_rectangle[0], patch_rectangle[1], s0, s1
            ),
            "child_classification": classification,
            "seam_signs_present": (
                ["STRICT_NEGATIVE", "STRICT_POSITIVE"]
                if is_graph else [signs[0]]
            ),
            "strict_absence_sign": None if is_graph else signs[0],
            "owns_s_equals_zero_boundary": owns_s0,
            "s_half_open_semantics": semantics,
            "p_lower_face_sign": signs[0],
        })
    need(
        sum(child["owns_s_equals_zero_boundary"] for child in result) == 1,
        "s0 owned once",
    )
    return result


def build(seed: int) -> tuple[dict[str, Any], dict[str, Any]]:
    need(seed >= 0, "seed")
    for filename, expected in PINS.items():
        need(fsha(HERE / filename) == expected, "pin:" + filename)

    round268_document = json.load(open(
        HERE / "cm2_round268_source_g_true_seam_candidate_geometry_exhaustion_certificate.json"
    ))
    round268 = round268_document["result"]
    need(
        round268_document["result_sha256"] == digest(round268)
        and round268["census"]["strict_positive_area_same_point_patch_count"] == 152,
        "Round268 wrapper",
    )
    round268_ids = {
        row["true_seam_patch_row_id"]
        for row in round268["formal_true_source_seam_positive_patch_ledger"]["rows"]
    }

    round275 = json.load(open(
        HERE / "cm2_round275_source_g_complete_reverse_rechart_materialization_certificate.json"
    ))["result"]
    region_rows = {
        row["reverse_rechart_region_row_id"]: row
        for ledger_name in ("strict_region_ledger", "arrangement_region_ledger")
        for row in round275[ledger_name]["rows"]
    }
    round280_document = load_gzip(
        HERE / "cm2_round280_source_g_true_seam_and_rechart_region_incidence_probe_patch_channels.json.gz"
    )
    round280_rows = {
        row["Round268_true_seam_patch_row_id"]: row
        for row in round280_document["rows"]
    }
    round282_document = load_gzip(
        HERE / "cm2_round282_source_g_strict_true_seam_normal_corridor_probe_ledger.json.gz"
    )
    round282_rows = {
        row["Round268_true_seam_patch_row_id"]: row
        for row in round282_document["rows"]
    }
    round283_result = json.load(open(
        HERE / "cm2_round283_source_g_outgoing_seam_tail_independent_probe_result.json"
    ))
    round283_document = load_gzip(
        HERE / "cm2_round283_source_g_outgoing_seam_tail_independent_probe_ledger.json.gz"
    )
    need(
        round283_result["result_sha256"] == digest({
            key: value for key, value in round283_result.items()
            if key != "result_sha256"
        })
        and round283_document["rows_sha256"]
        == round283_result["ledger"]["rows_sha256"]
        and round283_document["row_count"] == 40,
        "Round283 result and ledger",
    )
    endpoint_rows = round283_document["rows"]
    tail_patch_ids = {
        row["Round268_true_seam_patch_row_id"] for row in endpoint_rows
    }
    need(
        len(round268_ids) == len(round280_rows) == len(round282_rows) == 152
        and set(round280_rows) == set(round282_rows) == round268_ids
        and tail_patch_ids <= round268_ids
        and len(tail_patch_ids) == 24,
        "patch universe conservation",
    )

    child_builders: dict[str, dict[str, Any]] = {}
    endpoint_builders = []
    child_key_by_guard: dict[tuple[str, int, str], list[str]] = defaultdict(list)
    logical_s_split_count = 0
    for endpoint in endpoint_rows:
        patch_id = endpoint["Round268_true_seam_patch_row_id"]
        side_index = endpoint["side_index"]
        child_ids = []
        for guard in endpoint["guard_channel_rows"]:
            templates = child_templates(endpoint, guard)
            logical_s_split_count += int(len(templates) == 2)
            for template_index, template in enumerate(templates):
                rectangle = template.pop("ps_rectangle")
                child_id = "round289-tail-child:" + digest([
                    patch_id, side_index, template["source_guard_row_id"],
                    template_index, [qstr(value) for value in rectangle],
                    template["child_classification"],
                ])
                need(child_id not in child_builders, "unique child")
                template.update({
                    "Round289_tail_child_row_id": child_id,
                    "Round283_endpoint_row_id": endpoint["Round283_endpoint_row_id"],
                    "Round268_true_seam_patch_row_id": patch_id,
                    "side_index": side_index,
                    "side": endpoint["side"],
                    "exact_half_open_ps_rectangle": [
                        qstr(value) for value in rectangle
                    ],
                    "_rectangle": rectangle,
                    "_relations": [],
                })
                child_builders[child_id] = template
                child_key_by_guard[(
                    patch_id, side_index, template["source_guard_row_id"]
                )].append(child_id)
                child_ids.append(child_id)
        endpoint_builders.append({
            "Round283_endpoint_row_id": endpoint["Round283_endpoint_row_id"],
            "Round268_true_seam_patch_row_id": patch_id,
            "side_index": side_index,
            "Round282_residual_cells": [
                tuple(map(Q, cell))
                for cell in endpoint["Round282_residual_rational_cells"]
            ],
            "child_ids": child_ids,
        })

    need(
        len(child_builders) == 64
        and logical_s_split_count == 16,
        "64 children and 16 splits",
    )

    relation_rows = []
    endpoint_conservation_rows = []
    endpoint_region_hits: set[tuple[str, int, str]] = set()
    endpoint_incident_regions: set[tuple[str, int, str]] = set()
    endpoint_separated_regions: set[tuple[str, int, str]] = set()
    relation_status_histogram = Counter()
    relation_sign_histogram = Counter()

    for endpoint in endpoint_builders:
        patch_id = endpoint["Round268_true_seam_patch_row_id"]
        side_index = endpoint["side_index"]
        side_channel = round280_rows[patch_id]["side_channel_rows"][side_index]
        endpoint_relation_ids = []
        endpoint_hit_ids = set()
        endpoint_incident_ids = set()
        endpoint_separated_ids = set()
        for region_id in side_channel["candidate_Round275_region_ids"]:
            region = region_rows[region_id]
            box = list(map(Q, region["adjacent_rational_region_box"]))
            footprint = (box[2], box[3], box[4], box[5])
            region_hit = False
            for residual_index, residual in enumerate(
                endpoint["Round282_residual_cells"]
            ):
                overlap = r283.intersection(footprint, residual)
                if overlap is None:
                    continue
                region_hit = True
                candidate_child_ids = child_key_by_guard.get((
                    patch_id, side_index, region["source_guard_row_id"]
                ), [])
                matches = [
                    child_id for child_id in candidate_child_ids
                    if r283.intersection(
                        child_builders[child_id]["_rectangle"], overlap
                    ) is not None
                ]
                need(len(matches) == 1, "one analytic child per incidence")
                child_id = matches[0]
                child = child_builders[child_id]
                sign = active_sign(region)
                is_graph = (
                    child["child_classification"]
                    == "REGULAR_P_GRAPH_HALF_OPEN_OWNER"
                )
                actual_incident = (
                    is_graph or sign == child["strict_absence_sign"]
                )
                disposition = (
                    "ACTUAL_INCIDENT_R275_REGION__SAME_SIGN_CONNECTED_GAP"
                    if actual_incident else
                    "NOT_SEAM_INCIDENT__SEPARATED_BY_REGULAR_OUTGOING_GRAPH"
                )
                relation_id = "round289-region-cell-incidence:" + digest([
                    endpoint["Round283_endpoint_row_id"], child_id,
                    region_id, residual_index,
                ])
                relation = close({
                    "Round289_region_cell_relation_id": relation_id,
                    "Round289_tail_child_row_id": child_id,
                    "Round283_endpoint_row_id": endpoint["Round283_endpoint_row_id"],
                    "Round268_true_seam_patch_row_id": patch_id,
                    "side_index": side_index,
                    "source_guard_row_id": region["source_guard_row_id"],
                    "Round275_region_id": region_id,
                    "Round275_region_classification": (
                        region.get("region_classification")
                        or region["arrangement_classification"]
                    ),
                    "Round282_residual_cell_index": residual_index,
                    "exact_positive_ps_overlap": [
                        qstr(value) for value in overlap
                    ],
                    "exact_positive_ps_overlap_area": qstr(r283.area(overlap)),
                    "active_outgoing_equality_sign": sign,
                    "complete_10_field_return_signature_sha256":
                        region["complete_10_field_return_signature_sha256"],
                    "disposition": disposition,
                    "actual_seam_incidence": actual_incident,
                    "occurrence_credit": 0,
                    "component_edge_credit": 0,
                })
                relation_rows.append(relation)
                child["_relations"].append(relation)
                endpoint_relation_ids.append(relation_id)
                relation_status_histogram[disposition] += 1
                relation_sign_histogram[(disposition, sign)] += 1
                if actual_incident:
                    endpoint_incident_ids.add(region_id)
                    endpoint_incident_regions.add(
                        (patch_id, side_index, region_id)
                    )
                else:
                    endpoint_separated_ids.add(region_id)
                    endpoint_separated_regions.add(
                        (patch_id, side_index, region_id)
                    )
            if region_hit:
                endpoint_hit_ids.add(region_id)
                endpoint_region_hits.add((patch_id, side_index, region_id))
        need(
            len(endpoint_hit_ids)
            == next(
                row["candidate_Round275_region_hit_count"]
                for row in endpoint_rows
                if row["Round283_endpoint_row_id"]
                == endpoint["Round283_endpoint_row_id"]
            ),
            "endpoint region hits",
        )
        endpoint_conservation_rows.append(close({
            "Round289_endpoint_conservation_row_id":
                "round289-endpoint-conservation:" + digest(
                    endpoint["Round283_endpoint_row_id"]
                ),
            "Round283_endpoint_row_id": endpoint["Round283_endpoint_row_id"],
            "Round268_true_seam_patch_row_id": patch_id,
            "side_index": side_index,
            "tail_child_ids": sorted(endpoint["child_ids"]),
            "tail_child_count": len(endpoint["child_ids"]),
            "Round282_residual_cell_count":
                len(endpoint["Round282_residual_cells"]),
            "Round275_region_hit_count": len(endpoint_hit_ids),
            "Round275_region_hit_ids": sorted(endpoint_hit_ids),
            "actual_incident_Round275_region_count":
                len(endpoint_incident_ids),
            "actual_incident_Round275_region_ids":
                sorted(endpoint_incident_ids),
            "graph_separated_Round275_region_count":
                len(endpoint_separated_ids),
            "graph_separated_Round275_region_ids":
                sorted(endpoint_separated_ids),
            "region_cell_relation_count": len(endpoint_relation_ids),
            "region_cell_relation_ids": sorted(endpoint_relation_ids),
            "analytic_tail_residual": 0,
            "component_edge_credit": 0,
        }))

    relation_rows.sort(key=lambda row: row["Round289_region_cell_relation_id"])
    child_rows = []
    sign_corridor_count = 0
    signature_binding_count = 0
    child_classification_histogram = Counter()
    actual_incident_relation_count = 0
    separated_relation_count = 0
    graph_owner_count = 0
    s0_owner_count = 0

    for child_id in sorted(child_builders):
        child = child_builders[child_id]
        relations = child.pop("_relations")
        child.pop("_rectangle")
        child_classification_histogram[child["child_classification"]] += 1
        is_graph = (
            child["child_classification"]
            == "REGULAR_P_GRAPH_HALF_OPEN_OWNER"
        )
        signs = child["seam_signs_present"]
        sign_corridors = []
        for sign in signs:
            incident = [
                relation for relation in relations
                if relation["actual_seam_incidence"]
                and relation["active_outgoing_equality_sign"] == sign
            ]
            need(incident, "every materialized sign corridor is incident")
            by_signature: dict[str, list[dict[str, Any]]] = defaultdict(list)
            for relation in incident:
                by_signature[
                    relation["complete_10_field_return_signature_sha256"]
                ].append(relation)
            bindings = []
            for signature_hash in sorted(by_signature):
                bound_relations = by_signature[signature_hash]
                region_ids = sorted({
                    relation["Round275_region_id"]
                    for relation in bound_relations
                })
                local_signatures = {
                    canonical(region_rows[region_id]["local_return_signature"])
                    for region_id in region_ids
                }
                need(len(local_signatures) == 1, "signature hash object unique")
                local_signature = region_rows[region_ids[0]][
                    "local_return_signature"
                ]
                need(
                    digest(local_signature) == signature_hash,
                    "full signature digest",
                )
                bindings.append({
                    "complete_10_field_return_signature_sha256":
                        signature_hash,
                    "complete_10_field_return_signature": local_signature,
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
                "half_open_zero_graph_included": (
                    is_graph and sign == child["p_lower_face_sign"]
                ),
                "zero_graph_owner_rule": (
                    "P_LOWER_SIGN_CORRIDOR_OWNS_F_EQUALS_ZERO"
                    if is_graph else "ZERO_SET_ABSENT"
                ),
                "connected_on_entire_seam_to_R275_gap": True,
                "actual_incident_Round275_region_count":
                    len(incident_region_ids),
                "actual_incident_Round275_region_ids":
                    incident_region_ids,
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
        actual_incident_relation_count += len(actual_relations)
        separated_relation_count += len(separated_relations)
        child_rows.append(close({
            **child,
            "equation": "outgoing_normal_x^2-outgoing_normal_y^2=0",
            "regular_graph_axis": "p" if is_graph else None,
            "half_open_graph_owner_count": int(is_graph),
            "sign_corridor_count": len(sign_corridors),
            "sign_corridors": sign_corridors,
            "actual_incident_Round275_region_count": len({
                relation["Round275_region_id"]
                for relation in actual_relations
            }),
            "actual_incident_Round275_region_ids": sorted({
                relation["Round275_region_id"]
                for relation in actual_relations
            }),
            "actual_incident_region_cell_relation_count":
                len(actual_relations),
            "actual_incident_region_cell_relation_ids": sorted(
                relation["Round289_region_cell_relation_id"]
                for relation in actual_relations
            ),
            "graph_separated_Round275_region_count": len({
                relation["Round275_region_id"]
                for relation in separated_relations
            }),
            "graph_separated_Round275_region_ids": sorted({
                relation["Round275_region_id"]
                for relation in separated_relations
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

    endpoint_conservation_rows.sort(
        key=lambda row: row["Round289_endpoint_conservation_row_id"]
    )
    need(child_classification_histogram == {
        "REGULAR_P_GRAPH_HALF_OPEN_OWNER": 40,
        "STRICT_ZERO_ABSENT": 24,
    }, "child classification")
    need(
        len(child_rows) == 64
        and sign_corridor_count == 104
        and graph_owner_count == 40
        and s0_owner_count == 16,
        "child/sign/owner census",
    )
    need(
        len(endpoint_region_hits) == 6596
        and len(relation_rows) == 9528
        and len(endpoint_incident_regions) == 6500
        and len(endpoint_separated_regions) == 96
        and not (
            endpoint_incident_regions & endpoint_separated_regions
        ),
        "region conservation",
    )
    need(
        actual_incident_relation_count == 9240
        and separated_relation_count == 288
        and relation_status_histogram == {
            "ACTUAL_INCIDENT_R275_REGION__SAME_SIGN_CONNECTED_GAP": 9240,
            "NOT_SEAM_INCIDENT__SEPARATED_BY_REGULAR_OUTGOING_GRAPH": 288,
        },
        "relation disposition conservation",
    )
    need(
        relation_sign_histogram == {
            (
                "ACTUAL_INCIDENT_R275_REGION__SAME_SIGN_CONNECTED_GAP",
                "STRICT_NEGATIVE",
            ): 4588,
            (
                "ACTUAL_INCIDENT_R275_REGION__SAME_SIGN_CONNECTED_GAP",
                "STRICT_POSITIVE",
            ): 4652,
            (
                "NOT_SEAM_INCIDENT__SEPARATED_BY_REGULAR_OUTGOING_GRAPH",
                "STRICT_NEGATIVE",
            ): 144,
            (
                "NOT_SEAM_INCIDENT__SEPARATED_BY_REGULAR_OUTGOING_GRAPH",
                "STRICT_POSITIVE",
            ): 144,
        },
        "relation sign conservation",
    )
    need(
        sum(
            row["Round282_residual_cell_count"]
            for row in endpoint_conservation_rows
        ) == 540
        and sum(
            row["analytic_tail_residual"]
            for row in endpoint_conservation_rows
        ) == 0,
        "residual conservation",
    )

    ledger = {
        "schema": SCHEMA + ".ledger",
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
                row["Round289_region_cell_relation_id"]
                for row in relation_rows
            ]),
            "row_hashes_sha256": digest([
                row["row_sha256"] for row in relation_rows
            ]),
        },
        "endpoint_conservation_ledger": {
            "row_count": len(endpoint_conservation_rows),
            "rows": endpoint_conservation_rows,
            "rows_sha256": digest(endpoint_conservation_rows),
            "row_ids_sha256": digest([
                row["Round289_endpoint_conservation_row_id"]
                for row in endpoint_conservation_rows
            ]),
            "row_hashes_sha256": digest([
                row["row_sha256"] for row in endpoint_conservation_rows
            ]),
        },
    }
    result = {
        "schema": SCHEMA,
        "status": (
            "PASS_PRODUCER_ROUND289_OUTGOING_SEAM_TAIL_CHILD_MATERIALIZATION__"
            "ANALYTIC_RESIDUAL_ZERO__ZERO_CREDIT_PENDING_INDEPENDENT_VERIFIER"
        ),
        "pins": PINS,
        "seed_affects_output": False,
        "census": {
            "input_true_seam_patch_universe_count": 152,
            "input_tail_patch_count": 24,
            "input_tail_directed_endpoint_count": 40,
            "input_guard_channel_incidence_count": 48,
            "preserved_two_guard_endpoint_count": 8,
            "Round282_residual_rational_cell_count": 540,
            "Round275_region_hit_count": len(endpoint_region_hits),
            "Round275_region_cell_incidence_count": len(relation_rows),
            "materialized_tail_child_count": len(child_rows),
            "regular_p_graph_child_count":
                child_classification_histogram[
                    "REGULAR_P_GRAPH_HALF_OPEN_OWNER"
                ],
            "strict_zero_absence_child_count":
                child_classification_histogram["STRICT_ZERO_ABSENT"],
            "logical_s_equals_zero_split_count": logical_s_split_count,
            "exact_half_open_graph_owner_count": graph_owner_count,
            "complete_sign_corridor_count": sign_corridor_count,
            "complete_signature_binding_count": signature_binding_count,
            "actual_incident_Round275_region_count":
                len(endpoint_incident_regions),
            "graph_separated_Round275_region_count":
                len(endpoint_separated_regions),
            "actual_incident_region_cell_relation_count":
                actual_incident_relation_count,
            "graph_separated_region_cell_relation_count":
                separated_relation_count,
            "remaining_analytic_tail_endpoint_count": 0,
            "remaining_analytic_tail_patch_count": 0,
        },
        "relation_disposition_histogram":
            dict(sorted(relation_status_histogram.items())),
        "ledger": {
            "filename": LEDGER.name,
            "child_rows_sha256":
                ledger["child_ledger"]["rows_sha256"],
            "region_cell_relation_rows_sha256":
                ledger["region_cell_relation_ledger"]["rows_sha256"],
            "endpoint_conservation_rows_sha256":
                ledger["endpoint_conservation_ledger"]["rows_sha256"],
        },
        "scope_contract": {
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
        "strict_nonpromotion": {
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
        },
        "required_next": (
            "Independently reconstruct all 64 children, 104 sign corridors, "
            "full signature bindings, and 9528 relation dispositions.  Only "
            "after verifier PASS may these tail rows join the already strict "
            "Round282 corridors; seam DSU edges remain forbidden until the "
            "two directed sides of every patch are occurrence-bound."
        ),
    }
    result["result_sha256"] = digest(result)
    return ledger, result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=289071)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument("--ledger", type=Path, default=LEDGER)
    args = parser.parse_args()
    ledger, result = build(args.seed)
    ledger_payload = gzip_bytes(ledger)
    result["ledger"]["file_sha256"] = hashlib.sha256(ledger_payload).hexdigest()
    result["result_sha256"] = digest({
        key: value for key, value in result.items()
        if key != "result_sha256"
    })
    atomic(args.ledger, ledger_payload)
    atomic(args.output, canonical(result) + b"\n")
    print(json.dumps({
        "status": result["status"],
        "result_sha256": result["result_sha256"],
        **result["census"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
