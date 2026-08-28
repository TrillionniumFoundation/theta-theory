#!/usr/bin/env python3
"""Freeze the true-seam endpoint pairing contract and its zero-credit census.

This producer deliberately does not emit a DSU edge.  It joins the frozen
Round268 seam patches, Round275 rechart regions, Round279 atom-incidence
semantics, the corrected Round280 occurrence identity contract, Round282
normal corridors, and Round284 overlap dispositions.  The result records
which geometric patches are already fully covered and why none is yet an
occurrence-bound formal component edge.
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


HERE = Path(__file__).resolve().parent
PREFIX = "cm2_round285_source_g_true_seam_safe_pairing_contract_probe"
LEDGER = HERE / f"{PREFIX}_ledger.json.gz"
OUTPUT = HERE / f"{PREFIX}_result.json"
SCHEMA = "cm2.round285.source-g-true-seam-safe-pairing-contract-probe.v1"

PINS = {
    "cm2_round268_source_g_true_seam_candidate_geometry_exhaustion_certificate.json":
        "10d5e42f4353e981e7e8d5aacc002bed119453ee14a13398c524d5cb4ac2f7b9",
    "cm2_round275_source_g_complete_reverse_rechart_materialization_certificate.json":
        "e18935169614fc8b62ead3be7f60b383396ea1d2c52e8151457241f49e770386",
    "cm2_round279_source_g_collar_atom_and_face_edge_freeze_atoms.json.gz":
        "283a10799e0c7d1156695c30cdb2533488602ca646a18804f93211c0a3132dbe",
    "cm2_round280_source_g_expanded_occurrence_identity_contract_audit_result.json":
        "873974c8b343961f9e7c1674a946681749a3c0267bc57a1ccc147ccd21b3bdfc",
    "cm2_round280_source_g_true_seam_and_rechart_region_incidence_probe_region_bindings.json.gz":
        "8354eb042455e6d3ed591ee1620c9fc9def1af916a9bfbc0bf42e473e3e6e58b",
    "cm2_round282_source_g_strict_true_seam_normal_corridor_probe_ledger.json.gz":
        "6d94bce99b3ea57b8a568707705d9f16833cfba28b242a6dabb2de5933f6509e",
    "cm2_round282_source_g_strict_true_seam_normal_corridor_probe_result.json":
        "cd054a7036d9c482357611e9af11d028179e0f34a828dca2fbe91332b178f532",
    "cm2_round284_source_g_rechart_occurrence_overlap_contract_probe_ledger.json.gz":
        "39b69e0c5d249454c7ff13da99b260d3a7fabfa03c8ad6866035cbcaa883eb92",
    "cm2_round284_source_g_rechart_occurrence_overlap_contract_probe_result.json":
        "e25dd7b494ad2c2ccddc17601d28136c1919a3b16e41f008669bd6c14a513692",
}

ENC = json.JSONEncoder(
    sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False
)

FULL = "FULL_BIDIRECTIONAL_STRICT_NORMAL_CORRIDOR_COVER"
TAIL = "SEAM_PATCH_REMAINS_FAIL_CLOSED_FOR_ARRANGEMENT_TAIL"
NEW = "NEW_DISJOINT_CANDIDATE__OCCURRENCE_ID_NOT_YET_ISSUED"
PARTIAL = "PARTIAL_OVERLAP__EXACT_REFINEMENT_REQUIRED"
ALIAS = "CONTAINED_ALIAS_CANDIDATE__OCCURRENCE_ID_NOT_YET_ISSUED"


def canonical(value: Any) -> bytes:
    return ENC.encode(value).encode()


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def fsha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def need(condition: bool, label: str) -> None:
    if not condition:
        raise RuntimeError(label)


def read_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def read_gzip_json(path: Path) -> Any:
    with gzip.open(path, "rt", encoding="utf-8") as handle:
        return json.load(handle)


def gzip_bytes(value: Any) -> bytes:
    buffer = io.BytesIO()
    with gzip.GzipFile(filename="", mode="wb", fileobj=buffer, mtime=0) as handle:
        handle.write(canonical(value))
    return buffer.getvalue()


def atomic_write(path: Path, payload: bytes) -> None:
    fd, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def closed(row: dict[str, Any]) -> dict[str, Any]:
    result = dict(row)
    result["row_sha256"] = digest(result)
    return result


def qtext(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else str(value)


def rectangle(values: list[str] | tuple[str, ...]) -> tuple[Q, Q, Q, Q]:
    result = tuple(Q(value) for value in values)
    need(len(result) == 4, "rectangle arity")
    need(result[0] < result[1] and result[2] < result[3], "positive rectangle")
    return result  # type: ignore[return-value]


def area(box: tuple[Q, Q, Q, Q]) -> Q:
    return (box[1] - box[0]) * (box[3] - box[2])


def positive_overlap(
    left: tuple[Q, Q, Q, Q], right: tuple[Q, Q, Q, Q]
) -> bool:
    return (
        max(left[0], right[0]) < min(left[1], right[1])
        and max(left[2], right[2]) < min(left[3], right[3])
    )


def physical_payload(signature: dict[str, Any]) -> dict[str, Any]:
    """Chart-transported physical return data.

    Raw official key IDs are chart-local and are intentionally not equated
    across a true seam.  The source chart substitution is verified separately.
    """
    return {
        "target_chart": signature["target_chart"],
        "target_lift": signature["target_lift"],
        "outgoing_cell": signature["outgoing_cell"],
        "ordered_integer_wall_events": signature["ordered_integer_wall_events"],
        "roof": signature["roof"],
        "signed_wall_word": signature["signed_wall_word"],
    }


def relation_atom_count(overlap_row: dict[str, Any]) -> int:
    return len(
        {
            relation["canonical_atom_id"]
            for relation in overlap_row["relations"]
        }
    )


def atom_count_bin(value: int) -> str:
    if value == 0:
        return "0"
    if value == 1:
        return "1"
    return "2+"


def exact_cells(
    patch_box: tuple[Q, Q, Q, Q],
    side_rows: list[dict[str, Any]],
) -> list[tuple[tuple[Q, Q, Q, Q], tuple[str, ...], tuple[str, ...]]]:
    footprints: list[tuple[Q, Q, Q, Q]] = []
    by_side: list[list[tuple[str, tuple[Q, Q, Q, Q]]]] = []
    for side in side_rows:
        records = []
        for corridor in side["accepted_strict_corridors"]:
            box = rectangle(corridor["positive_ps_footprint"])
            records.append((corridor["Round275_region_id"], box))
            footprints.append(box)
        by_side.append(records)
    need(len(by_side) == 2, "two seam sides")
    p_values = sorted(
        {patch_box[0], patch_box[1], *(x for box in footprints for x in box[:2])}
    )
    s_values = sorted(
        {patch_box[2], patch_box[3], *(x for box in footprints for x in box[2:])}
    )
    cells = []
    for p0, p1 in zip(p_values, p_values[1:]):
        for s0, s1 in zip(s_values, s_values[1:]):
            cell = (p0, p1, s0, s1)
            if not (
                patch_box[0] <= p0 < p1 <= patch_box[1]
                and patch_box[2] <= s0 < s1 <= patch_box[3]
            ):
                continue
            covers = []
            for records in by_side:
                covers.append(
                    tuple(
                        sorted(
                            {
                                region_id
                                for region_id, box in records
                                if (
                                    box[0] <= p0
                                    and p1 <= box[1]
                                    and box[2] <= s0
                                    and s1 <= box[3]
                                )
                            }
                        )
                    )
                )
            cells.append((cell, covers[0], covers[1]))
    need(sum((area(cell) for cell, _, _ in cells), Q(0)) == area(patch_box), "cell area")
    return cells


def histogram(values: list[Any]) -> dict[str, int]:
    return {
        str(key): value
        for key, value in sorted(Counter(values).items(), key=lambda item: str(item[0]))
    }


def build() -> tuple[dict[str, Any], dict[str, Any]]:
    for name, expected in PINS.items():
        need(fsha(HERE / name) == expected, f"pin:{name}")

    r268_result = read_json(
        HERE / "cm2_round268_source_g_true_seam_candidate_geometry_exhaustion_certificate.json"
    )["result"]
    r268_rows = r268_result["formal_true_source_seam_positive_patch_ledger"]["rows"]
    need(len(r268_rows) == 152, "Round268 patch universe")
    r268 = {row["true_seam_patch_row_id"]: row for row in r268_rows}
    need(len(r268) == 152, "unique Round268 patch ids")

    r275_result = read_json(
        HERE / "cm2_round275_source_g_complete_reverse_rechart_materialization_certificate.json"
    )["result"]
    r275_rows = (
        r275_result["strict_region_ledger"]["rows"]
        + r275_result["arrangement_region_ledger"]["rows"]
    )
    need(len(r275_rows) == 13_788, "Round275 region universe")
    r275 = {row["reverse_rechart_region_row_id"]: row for row in r275_rows}
    need(len(r275) == 13_788, "unique Round275 regions")

    r282_rows = read_gzip_json(
        HERE / "cm2_round282_source_g_strict_true_seam_normal_corridor_probe_ledger.json.gz"
    )["rows"]
    need(len(r282_rows) == 152, "Round282 patch universe")

    r284_rows = read_gzip_json(
        HERE / "cm2_round284_source_g_rechart_occurrence_overlap_contract_probe_ledger.json.gz"
    )["rows"]
    need(len(r284_rows) == 13_788, "Round284 region universe")
    r284 = {row["Round275_region_id"]: row for row in r284_rows}
    need(set(r284) == set(r275), "Round275/Round284 conservation")

    occurrence_audit = read_json(
        HERE / "cm2_round280_source_g_expanded_occurrence_identity_contract_audit_result.json"
    )["result"]
    need(
        occurrence_audit["strict_nonpromotion"]["expanded_occurrences"] == 126_468,
        "corrected occurrence baseline",
    )
    need(
        occurrence_audit["strict_nonpromotion"]["Jx_Jy_same_point_glue_credit"] == 0,
        "Jx/Jy rejected by occurrence contract",
    )

    owner_patches: dict[str, list[tuple[str, tuple[Q, Q, Q, Q]]]] = defaultdict(list)
    owner_pairs = []
    patch_area_hist: Counter[str] = Counter()
    for patch in r268_rows:
        patch_box = rectangle(
            patch["exact_common_p_interval"] + patch["exact_common_s_interval"]
        )
        need(qtext(area(patch_box)) == patch["exact_positive_common_area"], "R268 area")
        patch_area_hist[patch["exact_positive_common_area"]] += 1
        pair = (
            patch["left_Round182_source_seam_row_id"],
            patch["right_Round182_source_seam_row_id"],
        )
        owner_pairs.append(pair)
        for side in ("left", "right"):
            owner_patches[patch[f"{side}_Round182_source_seam_row_id"]].append(
                (patch["true_seam_patch_row_id"], patch_box)
            )
    need(len(set(owner_pairs)) == 152, "unique seam-owner pairs")
    for owner_id, records in owner_patches.items():
        for index, (_, left) in enumerate(records):
            for _, right in records[:index]:
                need(not positive_overlap(left, right), f"owner patch overlap:{owner_id}")
    owner_degree_hist = Counter(len(records) for records in owner_patches.values())
    need(
        owner_degree_hist == Counter({1: 248, 2: 16, 3: 8}),
        "owner degree census",
    )

    patch_rows = []
    geometry_hist: Counter[str] = Counter()
    full_endpoint_region_count_hist: Counter[int] = Counter()
    full_distinct_regions: set[str] = set()
    tail_distinct_regions: set[str] = set()
    all_corridor_region_occurrences: Counter[str] = Counter()
    full_raw_pairs: set[tuple[str, str, str]] = set()
    full_pair_overlap_hist: Counter[str] = Counter()
    full_pair_atom_relation_hist: Counter[str] = Counter()
    full_cell_count = 0
    full_endpoint_count = 0
    full_corridor_record_count = 0
    full_transported_payload_match_count = 0
    full_raw_signature_disjoint_count = 0
    tail_payload_pattern_hist: Counter[str] = Counter()
    tail_partial_endpoint_count = 0
    tail_partial_count_hist: Counter[int] = Counter()
    tail_seam_hist: Counter[str] = Counter()

    for corridor_patch in sorted(
        r282_rows, key=lambda row: row["Round268_true_seam_patch_row_id"]
    ):
        patch_id = corridor_patch["Round268_true_seam_patch_row_id"]
        need(patch_id in r268, "Round282 orphan patch")
        patch = r268[patch_id]
        need(
            corridor_patch["cyclic_transition_identity"]
            == patch["cyclic_transition_identity"],
            "transition identity",
        )
        need(
            corridor_patch["exact_common_p_interval"]
            == patch["exact_common_p_interval"]
            and corridor_patch["exact_common_s_interval"]
            == patch["exact_common_s_interval"],
            "patch bounds",
        )
        patch_box = rectangle(
            patch["exact_common_p_interval"] + patch["exact_common_s_interval"]
        )
        side_summaries = []
        side_payload_sets = []
        side_signature_sets = []
        side_owner_sets = []
        patch_region_ids: set[str] = set()

        for side in corridor_patch["side_corridors"]:
            region_ids = sorted(
                {
                    corridor["Round275_region_id"]
                    for corridor in side["accepted_strict_corridors"]
                }
            )
            need(all(region_id in r275 for region_id in region_ids), "R275 corridor id")
            need(all(region_id in r284 for region_id in region_ids), "R284 corridor id")
            patch_region_ids.update(region_ids)
            all_corridor_region_occurrences.update(region_ids)
            classifications = Counter(r284[region_id]["classification"] for region_id in region_ids)
            parents = {r275[region_id]["parent_id"] for region_id in region_ids}
            signature_hashes = {
                r275[region_id]["complete_10_field_return_signature_sha256"]
                for region_id in region_ids
            }
            payloads = {
                digest(physical_payload(r275[region_id]["local_return_signature"]))
                for region_id in region_ids
            }
            owners = {r275[region_id]["owner_target"] for region_id in region_ids}
            atom_relation_counts = Counter(
                atom_count_bin(relation_atom_count(r284[region_id]))
                for region_id in region_ids
            )
            side_payload_sets.append(payloads)
            side_signature_sets.append(signature_hashes)
            side_owner_sets.append(owners)
            if corridor_patch["classification"] == FULL:
                full_endpoint_count += 1
                full_corridor_record_count += len(side["accepted_strict_corridors"])
                full_endpoint_region_count_hist[len(region_ids)] += 1
            side_summaries.append(
                {
                    "side": side["side"],
                    "source_chart": side["source_chart"],
                    "adjacent_chart": side["adjacent_chart"],
                    "local_t_root": side["local_t_root"],
                    "corridor_classification": side["classification"],
                    "accepted_corridor_record_count": len(
                        side["accepted_strict_corridors"]
                    ),
                    "distinct_Round275_region_count": len(region_ids),
                    "distinct_Round275_region_ids_sha256": digest(region_ids),
                    "Round284_occurrence_overlap_classification_histogram": dict(
                        sorted(classifications.items())
                    ),
                    "Round279_atom_relation_count_histogram": dict(
                        sorted(atom_relation_counts.items())
                    ),
                    "parent_count": len(parents),
                    "chart_local_signature_count": len(signature_hashes),
                    "transported_physical_payload_count": len(payloads),
                    "owner_target_count": len(owners),
                    "strict_corridor_covered_area": side[
                        "strict_corridor_covered_area"
                    ],
                    "unresolved_area": side["unresolved_area"],
                    "formal_occurrence_endpoint_count": 0,
                    "formal_component_endpoint_count": 0,
                    "formal_component_edge_credit": 0,
                }
            )

        need(len(side_summaries) == 2, "two side summaries")
        need(side_owner_sets[0] == side_owner_sets[1], "owner target transport")
        cells = exact_cells(patch_box, corridor_patch["side_corridors"])
        cell_rows = []
        patch_raw_pairs: set[tuple[str, str]] = set()
        patch_pair_overlap_hist: Counter[str] = Counter()
        patch_pair_atom_hist: Counter[str] = Counter()
        for cell_index, (cell, left_ids, right_ids) in enumerate(cells):
            left_payloads = {
                digest(physical_payload(r275[region_id]["local_return_signature"]))
                for region_id in left_ids
            }
            right_payloads = {
                digest(physical_payload(r275[region_id]["local_return_signature"]))
                for region_id in right_ids
            }
            pair_payload_match = bool(left_payloads & right_payloads)
            for left_id in left_ids:
                for right_id in right_ids:
                    pair = (left_id, right_id)
                    if pair in patch_raw_pairs:
                        continue
                    patch_raw_pairs.add(pair)
                    overlap_key = (
                        f"{r284[left_id]['classification']}|"
                        f"{r284[right_id]['classification']}"
                    )
                    atom_key = (
                        f"{atom_count_bin(relation_atom_count(r284[left_id]))}|"
                        f"{atom_count_bin(relation_atom_count(r284[right_id]))}"
                    )
                    patch_pair_overlap_hist[overlap_key] += 1
                    patch_pair_atom_hist[atom_key] += 1
            if not left_ids or not right_ids:
                cell_classification = (
                    "UNCOVERED_SIDE__ARRANGEMENT_REFINEMENT_REQUIRED"
                )
            elif not pair_payload_match:
                cell_classification = (
                    "TRANSPORTED_PAYLOAD_PARTITION_REFINEMENT_REQUIRED"
                )
            else:
                cell_classification = (
                    "GEOMETRIC_PAIR_PRESENT__OCCURRENCE_IDENTITIES_UNISSUED"
                )
            cell_rows.append(
                {
                    "cell_index": cell_index,
                    "exact_p_s_box": [qtext(value) for value in cell],
                    "exact_positive_area": qtext(area(cell)),
                    "left_Round275_region_count": len(left_ids),
                    "right_Round275_region_count": len(right_ids),
                    "left_Round275_region_ids_sha256": digest(list(left_ids)),
                    "right_Round275_region_ids_sha256": digest(list(right_ids)),
                    "transported_physical_payload_intersection_nonempty":
                        pair_payload_match,
                    "classification": cell_classification,
                    "formal_component_edge_credit": 0,
                }
            )

        geometry = corridor_patch["classification"]
        geometry_hist[geometry] += 1
        if geometry == FULL:
            full_distinct_regions.update(patch_region_ids)
            full_cell_count += len(cells)
            full_raw_pairs.update(
                (patch_id, left_id, right_id)
                for left_id, right_id in patch_raw_pairs
            )
            full_pair_overlap_hist.update(patch_pair_overlap_hist)
            full_pair_atom_relation_hist.update(patch_pair_atom_hist)
            need(
                side_payload_sets[0] == side_payload_sets[1],
                "full patch transported payload mismatch",
            )
            full_transported_payload_match_count += 1
            need(
                not (side_signature_sets[0] & side_signature_sets[1]),
                "raw chart-local signatures unexpectedly equal",
            )
            full_raw_signature_disjoint_count += 1
            pairing_classification = (
                "GEOMETRY_FULL__OCCURRENCE_BINDING_UNRESOLVED__ZERO_CREDIT"
            )
        else:
            need(geometry == TAIL, "known Round282 classification")
            tail_distinct_regions.update(patch_region_ids)
            partial_count = sum(
                side["corridor_classification"].startswith("PARTIAL")
                for side in side_summaries
            )
            tail_partial_endpoint_count += partial_count
            tail_partial_count_hist[partial_count] += 1
            tail_seam_hist[patch["cyclic_transition_identity"]] += 1
            if side_payload_sets[0] == side_payload_sets[1]:
                tail_payload_pattern_hist["ONE_TO_ONE_MATCHING_PAYLOAD_SET"] += 1
            else:
                need(
                    bool(side_payload_sets[0] & side_payload_sets[1]),
                    "tail payload sets have no common member",
                )
                tail_payload_pattern_hist["ONE_TO_TWO_PARTITION_REQUIRED"] += 1
            pairing_classification = (
                "ARRANGEMENT_TAIL_AND_OCCURRENCE_BINDING_UNRESOLVED__ZERO_CREDIT"
            )

        patch_rows.append(
            closed(
                {
                    "Round285_safe_pairing_row_id":
                        "round285-safe-seam-pairing:" + digest(patch_id),
                    "Round268_true_seam_patch_row_id": patch_id,
                    "cyclic_transition_identity": patch["cyclic_transition_identity"],
                    "left_Round182_source_seam_row_id": patch[
                        "left_Round182_source_seam_row_id"
                    ],
                    "right_Round182_source_seam_row_id": patch[
                        "right_Round182_source_seam_row_id"
                    ],
                    "left_chart": patch["left_chart"],
                    "right_chart": patch["right_chart"],
                    "left_local_t_root": patch["left_local_t_root"],
                    "right_local_t_root": patch["right_local_t_root"],
                    "same_physical_source_point": patch[
                        "same_physical_source_point"
                    ],
                    "owner_shadow_half_open_pair": patch[
                        "owner_shadow_half_open_pair"
                    ],
                    "Round171_normal_position_velocity_identity": patch[
                        "Round171_normal_position_velocity_identity"
                    ],
                    "exact_common_p_interval": patch["exact_common_p_interval"],
                    "exact_common_s_interval": patch["exact_common_s_interval"],
                    "exact_positive_common_area": patch[
                        "exact_positive_common_area"
                    ],
                    "Round282_geometry_classification": geometry,
                    "side_summaries": side_summaries,
                    "exact_cell_count": len(cells),
                    "exact_cells": cell_rows,
                    "distinct_raw_region_pair_count": len(patch_raw_pairs),
                    "raw_pair_Round284_classification_histogram": dict(
                        sorted(patch_pair_overlap_hist.items())
                    ),
                    "raw_pair_Round279_atom_relation_count_histogram": dict(
                        sorted(patch_pair_atom_hist.items())
                    ),
                    "transported_owner_target_sets_equal": True,
                    "chart_local_signature_ids_are_not_alias_ids": True,
                    "pairing_classification": pairing_classification,
                    "formal_occurrence_identity_credit": 0,
                    "formal_component_edge_credit": 0,
                    "formal_DSU_rank_credit": 0,
                    "formal_maximality_credit": 0,
                    "Jx_Jy_same_point_glue_credit": 0,
                }
            )
        )

    need(len(patch_rows) == 152, "Round285 patch rows")
    need(geometry_hist == Counter({FULL: 128, TAIL: 24}), "geometry census")
    need(full_endpoint_count == 256, "full endpoint count")
    need(full_corridor_record_count == 536, "full corridor record count")
    need(len(full_distinct_regions) == 512, "full distinct region count")
    need(full_cell_count == 148, "full exact cell count")
    need(len(full_raw_pairs) == 496, "full raw pair count")
    need(full_transported_payload_match_count == 128, "full payload match")
    need(full_raw_signature_disjoint_count == 128, "chart-local key census")
    need(tail_partial_endpoint_count == 40, "tail partial endpoints")
    need(tail_partial_count_hist == Counter({2: 16, 1: 8}), "tail sidedness")
    need(
        tail_payload_pattern_hist
        == Counter(
            {
                "ONE_TO_ONE_MATCHING_PAYLOAD_SET": 8,
                "ONE_TO_TWO_PARTITION_REQUIRED": 16,
            }
        ),
        "tail payload census",
    )
    need(
        set(tail_seam_hist.values()) == {6} and len(tail_seam_hist) == 4,
        "four-seam symmetry",
    )

    full_overlap_hist = Counter(r284[region_id]["classification"] for region_id in full_distinct_regions)
    tail_overlap_hist = Counter(r284[region_id]["classification"] for region_id in tail_distinct_regions)
    need(full_overlap_hist == Counter({NEW: 504, PARTIAL: 8}), "full overlap census")
    need(
        full_pair_overlap_hist
        == Counter({f"{NEW}|{NEW}": 488, f"{NEW}|{PARTIAL}": 4, f"{PARTIAL}|{NEW}": 4}),
        "full pair overlap census",
    )
    need(
        full_pair_atom_relation_hist
        == Counter({"0|0": 472, "0|1": 8, "1|0": 8, "0|2+": 4, "2+|0": 4}),
        "full pair atom relation census",
    )
    need(
        not any(
            not key.startswith("0|") and not key.endswith("|0")
            for key in full_pair_atom_relation_hist
        ),
        "no raw pair bound on both sides",
    )

    corridor_reuse_hist = Counter(all_corridor_region_occurrences.values())
    need(corridor_reuse_hist == Counter({1: 2612, 2: 24}), "corridor reuse")

    patch_rows.sort(key=lambda row: row["Round285_safe_pairing_row_id"])
    ledger = {
        "schema": f"{SCHEMA}.ledger",
        "status": "PASS_ROUND285_COMPLETE_TRUE_SEAM_PAIRING_CENSUS__ZERO_CREDIT",
        "rows": patch_rows,
        "row_count": len(patch_rows),
        "rows_sha256": digest(patch_rows),
        "row_ids_sha256": digest(
            [row["Round285_safe_pairing_row_id"] for row in patch_rows]
        ),
        "row_hashes_sha256": digest([row["row_sha256"] for row in patch_rows]),
        "strict_nonpromotion": True,
    }

    safe_contract = {
        "R268_patch_provenance_is_mandatory": True,
        "only_four_true_cyclic_source_seams_are_admissible": True,
        "Jx_Jy_are_never_same_point_seam_edges": True,
        "patch_is_partitioned_into_exact_disjoint_half_open_p_s_cells": True,
        "cell_union_must_equal_patch_with_no_gap_or_positive_area_overlap": True,
        "each_side_requires_a_strict_connected_normal_corridor": True,
        "complete_dynamic_signature_is_constant_on_each_corridor": True,
        "raw_chart_local_key_or_signature_equality_is_not_required_or_sufficient": True,
        "transported_physical_return_payload_and_registry_key_transport_are_required": True,
        "every_incident_R275_region_requires_one_terminal_occurrence_disposition": [
            "EXACT_SAME_POSITIVE_OPEN_REGION_ALIAS",
            "STRICTLY_NEW_DISJOINT_OCCURRENCE",
        ],
        "partial_or_nested_positive_volume_overlap_requires_exact_partition": True,
        "signature_parent_hash_face_or_connectivity_never_implies_occurrence_alias": True,
        "R279_common_face_relations_only_create_component_connectivity": True,
        "only_the_four_frozen_W_tail_aliases_may_precontract_occurrence_identity": True,
        "true_seam_glue_never_collapses_occurrence_identity": True,
        "edge_key": [
            "Round268_true_seam_patch_row_id",
            "exact_half_open_cell_id",
            "left_final_occurrence_id",
            "right_final_occurrence_id",
        ],
        "all_distinct_incident_occurrences_are_retained": True,
        "one_patch_does_not_imply_one_edge_or_one_rank_reduction": True,
        "DSU_rank_credit_is_the_replayed_union_delta_after_edge_deduplication": True,
    }

    result = {
        "schema": SCHEMA,
        "status": (
            "PASS_ROUND285_TRUE_SEAM_SAFE_PAIRING_CONTRACT__"
            "128_GEOMETRY_FULL__24_TAILS__0_OF_152_FORMAL_EDGES__ZERO_CREDIT"
        ),
        "pins": PINS,
        "census": {
            "Round268_true_seam_patch_count": 152,
            "Round268_directed_endpoint_count": 304,
            "Round268_distinct_seam_owner_count": len(owner_patches),
            "Round268_owner_degree_histogram": {
                str(key): value for key, value in sorted(owner_degree_hist.items())
            },
            "Round268_unique_owner_pair_count": len(set(owner_pairs)),
            "Round268_reused_owner_positive_area_overlap_count": 0,
            "Round268_patch_area_histogram": dict(sorted(patch_area_hist.items())),
            "geometry_full_bidirectional_patch_count": geometry_hist[FULL],
            "geometry_arrangement_tail_patch_count": geometry_hist[TAIL],
            "geometry_full_directed_endpoint_count": 264,
            "geometry_partial_directed_endpoint_count": tail_partial_endpoint_count,
            "tail_partial_side_count_per_patch_histogram": {
                str(key): value
                for key, value in sorted(tail_partial_count_hist.items())
            },
            "tail_patch_count_per_true_seam": dict(sorted(tail_seam_hist.items())),
            "tail_transported_payload_pattern_histogram": dict(
                sorted(tail_payload_pattern_hist.items())
            ),
            "full_patch_endpoint_count": full_endpoint_count,
            "full_patch_corridor_record_count": full_corridor_record_count,
            "full_patch_distinct_Round275_region_count": len(full_distinct_regions),
            "full_patch_endpoint_distinct_region_count_histogram": {
                str(key): value
                for key, value in sorted(full_endpoint_region_count_hist.items())
            },
            "full_patch_exact_p_s_cell_count": full_cell_count,
            "full_patch_distinct_raw_region_pair_count": len(full_raw_pairs),
            "full_patch_Round284_region_classification_histogram": dict(
                sorted(full_overlap_hist.items())
            ),
            "full_patch_raw_pair_Round284_classification_histogram": dict(
                sorted(full_pair_overlap_hist.items())
            ),
            "full_patch_raw_pair_Round279_atom_relation_count_histogram": dict(
                sorted(full_pair_atom_relation_hist.items())
            ),
            "full_patch_raw_pairs_with_atom_relation_on_both_sides": 0,
            "full_patch_transported_physical_payload_match_count":
                full_transported_payload_match_count,
            "full_patch_raw_chart_local_signature_disjoint_count":
                full_raw_signature_disjoint_count,
            "tail_current_distinct_Round275_region_count": len(tail_distinct_regions),
            "tail_current_Round284_region_classification_histogram": dict(
                sorted(tail_overlap_hist.items())
            ),
            "all_current_corridor_distinct_Round275_region_count":
                len(all_corridor_region_occurrences),
            "all_current_corridor_region_reuse_histogram": {
                str(key): value for key, value in sorted(corridor_reuse_hist.items())
            },
            "currently_geometry_pairable_patch_count": 128,
            "currently_occurrence_bound_pairable_patch_count": 0,
            "arrangement_refinement_required_patch_count": 24,
            "occurrence_identity_or_overlap_refinement_required_patch_count": 152,
            "formal_true_seam_component_edge_count": 0,
            "formal_true_seam_DSU_rank_credit": 0,
        },
        "decision": {
            "closing_only_the_24_arrangement_tails_would_make_geometry_152_of_152":
                True,
            "closing_only_geometry_does_not_issue_occurrence_identities": True,
            "formal_edges_after_tail_closure_but_before_occurrence_disposition": 0,
            "the_152_patch_count_is_not_a_predicted_edge_or_rank_count": True,
        },
        "safe_pairing_contract": safe_contract,
        "strict_nonpromotion": {
            "expanded_occurrence_credit": 0,
            "component_edge_credit": 0,
            "DSU_rank_credit": 0,
            "maximality_credit": 0,
            "exact_key_fibre_credit": 0,
            "global_disposition_credit": 0,
            "Jx_Jy_same_point_glue_credit": 0,
            "quotient": 63_224,
            "expanded_occurrences": 126_468,
            "Gate5": "10/18",
            "D02": "BLOCKED",
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "ledger": {
            "filename": LEDGER.name,
            "row_count": ledger["row_count"],
            "rows_sha256": ledger["rows_sha256"],
            "row_ids_sha256": ledger["row_ids_sha256"],
            "row_hashes_sha256": ledger["row_hashes_sha256"],
        },
        "next_gate": (
            "Close the 24 outgoing-arrangement tails, terminally disposition every "
            "incident R275 region as exact alias or new-disjoint after exact "
            "partial-overlap refinement, bind every exact seam cell to final "
            "occurrence IDs, then deduplicate and replay the component DSU edges."
        ),
    }
    result["result_sha256"] = digest(result)
    return ledger, result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ledger", type=Path, default=LEDGER)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument("--seed", default="285071")
    args = parser.parse_args()
    ledger, result = build()
    ledger_payload = gzip_bytes(ledger)
    result["ledger"]["file_sha256"] = hashlib.sha256(ledger_payload).hexdigest()
    result["result_sha256"] = digest(
        {key: value for key, value in result.items() if key != "result_sha256"}
    )
    atomic_write(args.ledger, ledger_payload)
    atomic_write(args.output, canonical(result) + b"\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
