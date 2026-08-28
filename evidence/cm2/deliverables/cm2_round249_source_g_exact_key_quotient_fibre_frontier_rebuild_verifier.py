#!/usr/bin/env python3
"""Independently verify the Round249 quotient-fibre frontier rebuild."""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import gc
import hashlib
import json
import os
from pathlib import Path
import stat
import tempfile
from typing import Any


HERE = Path(__file__).resolve().parent
OUTPUT = (
    HERE
    / "cm2_round249_source_g_exact_key_quotient_fibre_frontier_rebuild_verification.json"
)
SCHEMA = (
    "cm2.round249.source-g-exact-key-quotient-fibre-frontier-rebuild."
    "verification.v1"
)
SOURCE_PINS = {
    "cm2_round179_source_g_residual_tube_arrangement_rows.json":
        "f20b42c1fed781779b537b4d45bf44233eae1ed3ee620b95177a80f0eb2b5e42",
    "cm2_round244_source_g_cross_parent_same_chart_bulk_quotient_rebuild_certificate.json":
        "5b08d568cccd302ac2dd62e7e9b6573ce83e015181ead168812159c9f882712f",
    "cm2_round245_source_g_retained_graph_mixed_sheet_quotient_certificate.json":
        "c76662f7cb068127f3612a3655ae720662eead9b9210b5757d771693149883c1",
    "cm2_round246_source_g_whole_signature_retained_quotient_certificate.json":
        "a448359c0a9b4495e54afe6e2d860c20fb222684bae46ee108574782a5a33bc9",
    "cm2_round247_source_g_crossing_and_source_seam_retained_quotient_certificate.json":
        "72188f5d99a220f44698f3023dd606633b364adbd02d5e20e5d4fa0ff6e1b2c7",
    "cm2_round248_source_g_wall_finite_key_retained_quotient_certificate.json":
        "fa48bdfb0056072f80c5809f57362c225f0beb40e1cc4c145f3f072335cdb311",
}
PINS = {
    **SOURCE_PINS,
    "cm2_round249_source_g_exact_key_quotient_fibre_frontier_rebuild.py":
        "c277610d883df2c1a29a36f6475eb82f2eeaa33caad91cd7c1dc83f11cfe62e0",
    "cm2_round249_source_g_exact_key_quotient_fibre_frontier_rebuild_certificate.json":
        "a4d360f5adab92e70658f5c9d052b079707134f146e8e62a859050d80096a58f",
}


def need(value: bool, label: str) -> None:
    if not value:
        raise RuntimeError(label)


def canonical(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode()


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def read_pinned(name: str) -> bytes:
    path = HERE / name
    info = path.lstat()
    need(
        stat.S_ISREG(info.st_mode)
        and not path.is_symlink()
        and info.st_nlink == 1
        and 0 < info.st_size <= 400_000_000,
        f"regular:{name}",
    )
    raw = path.read_bytes()
    need(hashlib.sha256(raw).hexdigest() == PINS[name], f"pin:{name}")
    return raw


def load_result(name: str) -> dict[str, Any]:
    document = json.loads(read_pinned(name))
    need(
        set(document) == {"schema", "result", "result_sha256"}
        and digest(document["result"]) == document["result_sha256"],
        f"envelope:{name}",
    )
    return document["result"]


def unpack(document: dict[str, Any], table: str) -> list[dict[str, Any]]:
    columns = document["row_column_schemas"][table]
    return [
        dict(zip(columns, packed, strict=True))
        for packed in document[table]
    ]


def validate_ledger(
    value: dict[str, Any],
    id_field: str,
) -> list[dict[str, Any]]:
    rows = value["rows"]
    row_ids = [row[id_field] for row in rows]
    need(
        value["row_count"] == len(rows)
        and len(rows) == len(set(row_ids))
        and row_ids == sorted(row_ids)
        and value["rows_sha256"] == digest(rows)
        and value["row_ids_sha256"] == digest(row_ids)
        and value["row_hashes_sha256"]
        == digest([row["row_sha256"] for row in rows])
        and value["every_row_closed_by_own_SHA256"] is True
        and all(
            row["row_sha256"]
            == digest({
                key: item
                for key, item in row.items()
                if key != "row_sha256"
            })
            for row in rows
        ),
        f"ledger:{id_field}",
    )
    return rows


def exact_row(candidate: dict[str, Any], expected: dict[str, Any], label: str) -> None:
    need(
        {
            key: value
            for key, value in candidate.items()
            if key != "row_sha256"
        } == expected,
        label,
    )


def verify() -> dict[str, Any]:
    for name in PINS:
        read_pinned(name)
    candidate = load_result(
        "cm2_round249_source_g_exact_key_quotient_fibre_frontier_rebuild_certificate.json"
    )
    need(
        candidate["formal_input_binding"]
        == {name: SOURCE_PINS[name] for name in sorted(SOURCE_PINS)},
        "candidate source binding",
    )
    assignment_rows = validate_ledger(
        candidate[
            "formal_mixed_sheet_component_exact_key_assignment_ledger"
        ],
        "component_exact_key_assignment_row_id",
    )
    fibre_rows = validate_ledger(
        candidate["formal_exact_key_quotient_fibre_frontier_ledger"],
        "quotient_fibre_frontier_row_id",
    )
    need(
        len(assignment_rows) == 94_444
        and len(fibre_rows) == 116,
        "candidate ledger census",
    )
    assignment_by_component = {
        row["mixed_sheet_quotient_component_id"]: row
        for row in assignment_rows
    }
    fibre_by_key = {
        row["official_key_id"]: row for row in fibre_rows
    }
    need(
        len(assignment_by_component) == 94_444
        and len(fibre_by_key) == 116,
        "candidate assignment uniqueness",
    )

    round179 = load_result(
        "cm2_round179_source_g_residual_tube_arrangement_rows.json"
    )
    resolved = {
        row["row_id"]: row
        for row in unpack(round179, "resolved_3d_child_rows")
    }
    del round179
    gc.collect()
    need(len(resolved) == 17_192, "Round179 resolved rows")

    round244 = load_result(
        "cm2_round244_source_g_cross_parent_same_chart_bulk_quotient_rebuild_certificate.json"
    )
    old_components = {
        row["resolved_bulk_component_row_id"]: row
        for row in round244["formal_resolved_bulk_component_ledger"]["rows"]
    }
    occurrence_rows = round244[
        "formal_post_Round244_occurrence_known_block_frontier_ledger"
    ]["rows"]
    key_frontier_rows = round244[
        "formal_post_Round244_key_frontier_ledger"
    ]["rows"]
    block_rows = round244[
        "formal_Round244_known_connectivity_block_carry_ledger"
    ]["rows"]
    need(
        len(old_components) == 8_148
        and len(occurrence_rows) == 53_968
        and len(key_frontier_rows) == 116
        and len(block_rows) == 7_388,
        "Round244 inputs",
    )

    round245 = load_result(
        "cm2_round245_source_g_retained_graph_mixed_sheet_quotient_certificate.json"
    )
    round246 = load_result(
        "cm2_round246_source_g_whole_signature_retained_quotient_certificate.json"
    )
    round247 = load_result(
        "cm2_round247_source_g_crossing_and_source_seam_retained_quotient_certificate.json"
    )
    prior_nodes = (
        round245["formal_retained_stratum_node_ledger"]["rows"]
        + round246[
            "formal_new_whole_signature_retained_stratum_node_ledger"
        ]["rows"]
        + round247[
            "formal_new_crossing_and_source_seam_retained_stratum_node_ledger"
        ]["rows"]
    )
    prior_node_key = {
        row["retained_stratum_node_id"]: (
            row["official_key_ordinal"],
            row["official_key_id"],
        )
        for row in prior_nodes
    }
    del round245, round246, round247, prior_nodes
    gc.collect()
    need(len(prior_node_key) == 6_388, "prior node keys")

    round248 = load_result(
        "cm2_round248_source_g_wall_finite_key_retained_quotient_certificate.json"
    )
    wall_bulks = round248[
        "formal_wall_positive_volume_bulk_ledger"
    ]["rows"]
    wall_sheets = round248[
        "formal_wall_half_open_sheet_owner_ledger"
    ]["rows"]
    enrichment_rows = round248[
        "formal_post_Round248_inherited_component_enrichment_ledger"
    ]["rows"]
    need(
        len(wall_bulks) == 88_936
        and len(wall_sheets) == 38_360
        and len(enrichment_rows) == 8_148,
        "Round248 inputs",
    )
    enrichment_by_old = {
        row["inherited_Round244_resolved_bulk_component_id"]: row
        for row in enrichment_rows
    }
    contact_node_key = {
        row["wall_bulk_node_id"]: (
            row["official_key_ordinal"],
            row["official_key_id"],
        )
        for row in wall_bulks
        if row["attached_to_inherited_Round244_component"]
    }
    all_virtual_node_key = {**prior_node_key, **contact_node_key}
    need(
        len(contact_node_key) == 2_640
        and len(all_virtual_node_key) == 9_028
        and set(enrichment_by_old) == set(old_components),
        "enriched component inputs",
    )

    component_ids_by_key: dict[str, list[str]] = defaultdict(list)
    inherited_component_ids_by_key: dict[str, list[str]] = defaultdict(list)
    new_wall_component_ids_by_key: dict[str, list[str]] = defaultdict(list)
    seeded_component_ids_by_key: dict[str, list[str]] = defaultdict(list)
    unseeded_component_ids_by_key: dict[str, list[str]] = defaultdict(list)
    component_member_count_by_key: Counter[str] = Counter()
    component_origin_histogram: Counter[str] = Counter()
    total_member_count = 0
    seeded_component_count = 0
    expected_component_ids: set[str] = set()

    for component_id, component in old_components.items():
        member_ids = component["member_Round179_resolved_child_row_ids"]
        member_keys = {
            (
                resolved[member_id]["official_key_ordinal"],
                resolved[member_id]["official_key_id"],
            )
            for member_id in member_ids
        }
        need(len(member_keys) == 1, f"resolved key purity:{component_id}")
        key_ordinal, key_id = next(iter(member_keys))
        virtual_ids = enrichment_by_old[component_id][
            "cumulative_virtual_stratum_node_ids"
        ]
        need(
            all(
                all_virtual_node_key[node_id] == (key_ordinal, key_id)
                for node_id in virtual_ids
            ),
            f"virtual key purity:{component_id}",
        )
        seed_blocks = component["seed_Round243_known_connectivity_block_ids"]
        member_count = len(member_ids) + len(virtual_ids)
        expected = {
            "component_exact_key_assignment_row_id":
                "round249-component-key-assignment:"
                + digest([component_id, key_id]),
            "mixed_sheet_quotient_component_id": component_id,
            "component_origin":
                "INHERITED_ROUND244_COMPONENT_ENRICHED_THROUGH_ROUND248",
            "official_key_ordinal": key_ordinal,
            "official_key_id": key_id,
            "resolved_occurrence_member_count": len(member_ids),
            "virtual_stratum_member_count": len(virtual_ids),
            "materialized_member_count": member_count,
            "seed_known_connectivity_block_count": len(seed_blocks),
            "seed_known_connectivity_block_ids": seed_blocks,
            "component_key_purity_proof_kind":
                "ALL_RESOLVED_AND_VIRTUAL_MEMBERS_HAVE_IDENTICAL_EXACT_KEY",
            "quotient_component_inventory_credit": 1,
            "maximal_physical_component_claimed": False,
            "global_exact_key_fibre_credit": 0,
        }
        exact_row(
            assignment_by_component[component_id],
            expected,
            f"inherited assignment:{component_id}",
        )
        expected_component_ids.add(component_id)
        component_ids_by_key[key_id].append(component_id)
        inherited_component_ids_by_key[key_id].append(component_id)
        if seed_blocks:
            seeded_component_ids_by_key[key_id].append(component_id)
            seeded_component_count += 1
        else:
            unseeded_component_ids_by_key[key_id].append(component_id)
        component_member_count_by_key[key_id] += member_count
        component_origin_histogram[
            "INHERITED_ROUND244_COMPONENT_ENRICHED_THROUGH_ROUND248"
        ] += 1
        total_member_count += member_count

    sheets_by_owner: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for sheet in wall_sheets:
        sheets_by_owner[sheet["owner_wall_bulk_node_id"]].append(sheet)
    new_component_ids: set[str] = set()
    for bulk in wall_bulks:
        if bulk["attached_to_inherited_Round244_component"]:
            continue
        component_id = bulk["assigned_mixed_sheet_quotient_component_id"]
        need(
            component_id not in new_component_ids,
            f"new component uniqueness:{component_id}",
        )
        new_component_ids.add(component_id)
        sheets = sheets_by_owner.get(bulk["wall_bulk_node_id"], [])
        need(
            all(
                sheet["assigned_mixed_sheet_quotient_component_id"]
                == component_id
                and sheet["owner_official_key_id"] == bulk["official_key_id"]
                for sheet in sheets
            ),
            f"new component purity:{component_id}",
        )
        key_ordinal = bulk["official_key_ordinal"]
        key_id = bulk["official_key_id"]
        member_count = 1 + len(sheets)
        expected = {
            "component_exact_key_assignment_row_id":
                "round249-component-key-assignment:"
                + digest([component_id, key_id]),
            "mixed_sheet_quotient_component_id": component_id,
            "component_origin": "ROUND248_NEW_UNSEEDED_WALL_COMPONENT",
            "official_key_ordinal": key_ordinal,
            "official_key_id": key_id,
            "resolved_occurrence_member_count": 0,
            "virtual_stratum_member_count": member_count,
            "materialized_member_count": member_count,
            "seed_known_connectivity_block_count": 0,
            "seed_known_connectivity_block_ids": [],
            "component_key_purity_proof_kind":
                "ONE_WALL_BULK_PLUS_ONLY_ITS_SAME_KEY_HALF_OPEN_SHEETS",
            "quotient_component_inventory_credit": 1,
            "maximal_physical_component_claimed": False,
            "global_exact_key_fibre_credit": 0,
        }
        exact_row(
            assignment_by_component[component_id],
            expected,
            f"new assignment:{component_id}",
        )
        expected_component_ids.add(component_id)
        component_ids_by_key[key_id].append(component_id)
        new_wall_component_ids_by_key[key_id].append(component_id)
        unseeded_component_ids_by_key[key_id].append(component_id)
        component_member_count_by_key[key_id] += member_count
        component_origin_histogram[
            "ROUND248_NEW_UNSEEDED_WALL_COMPONENT"
        ] += 1
        total_member_count += member_count
    need(
        len(new_component_ids) == 86_296
        and expected_component_ids == set(assignment_by_component)
        and total_member_count == 150_876,
        "component assignment partition",
    )

    occurrence_ids_by_key: dict[str, list[str]] = defaultdict(list)
    unattached_ids_by_key: dict[str, list[str]] = defaultdict(list)
    gauge_deficit_by_key: dict[str, Counter[str]] = defaultdict(Counter)
    block_key: dict[str, str] = {}
    block_ids_by_key: dict[str, list[str]] = defaultdict(list)
    for occurrence in occurrence_rows:
        key_id = occurrence["official_key_id"]
        occurrence_id = occurrence["local_occurrence_row_id"]
        occurrence_ids_by_key[key_id].append(occurrence_id)
        if occurrence["known_block_incidence_attachment_credit"] == 0:
            unattached_ids_by_key[key_id].append(occurrence_id)
            gauge_deficit_by_key[key_id][
                occurrence["local_occurrence_gauge"]
            ] += 1
        block_id = occurrence["Round244_known_connectivity_block_id"]
        if block_id is not None:
            need(
                block_id not in block_key or block_key[block_id] == key_id,
                f"block purity:{block_id}",
            )
            block_key[block_id] = key_id
    carried_blocks = {
        row["Round244_known_connectivity_block_id"] for row in block_rows
    }
    need(
        len(block_key) == 7_388 and set(block_key) == carried_blocks,
        "block partition",
    )
    for block_id, key_id in block_key.items():
        block_ids_by_key[key_id].append(block_id)

    key_frontier_by_id = {
        row["official_key_id"]: row for row in key_frontier_rows
    }
    need(
        len(key_frontier_by_id) == 116
        and set(key_frontier_by_id) == set(component_ids_by_key)
        == set(occurrence_ids_by_key) == set(fibre_by_key),
        "key universe",
    )

    status_histogram: Counter[str] = Counter()
    component_count_histogram: Counter[int] = Counter()
    total_gauge_deficit: Counter[str] = Counter()
    keys_with_gauge_deficit: Counter[str] = Counter()
    keys_with_blocks = 0
    keys_with_new_wall = 0
    all_unattached = True
    all_unseeded_inherited = True

    for key_id, key_frontier in key_frontier_by_id.items():
        component_ids = sorted(component_ids_by_key[key_id])
        inherited_ids = sorted(inherited_component_ids_by_key[key_id])
        new_wall_ids = sorted(new_wall_component_ids_by_key[key_id])
        seeded_ids = sorted(seeded_component_ids_by_key[key_id])
        unseeded_ids = sorted(unseeded_component_ids_by_key[key_id])
        block_ids = sorted(block_ids_by_key[key_id])
        occurrence_ids = sorted(occurrence_ids_by_key[key_id])
        unattached_ids = sorted(unattached_ids_by_key[key_id])
        gauge_deficit = gauge_deficit_by_key[key_id]
        for gauge, count in gauge_deficit.items():
            total_gauge_deficit[gauge] += count
            keys_with_gauge_deficit[gauge] += bool(count)
        gauge_labels = [
            label
            for gauge, label in (
                ("ROUND179_RESOLVED_CHILD", "ROUND179"),
                ("ROUND204_STRICT_OPEN_REGION", "ROUND204"),
                ("ROUND208_STRICT_OPEN_REGION", "ROUND208"),
            )
            if gauge_deficit[gauge] > 0
        ]
        need(
            gauge_labels and gauge_labels[0] == "ROUND179",
            f"key deficit:{key_id}",
        )
        status = "__".join([
            "KNOWN_BLOCKS_PRESENT" if block_ids else "NO_KNOWN_BLOCK",
            (
                "WALL_COMPONENTS_PRESENT"
                if new_wall_ids else "NO_NEW_WALL_COMPONENT"
            ),
            "_".join(gauge_labels) + "_UNATTACHED_OCCURRENCES",
        ])
        unseeded_set = set(unseeded_ids)
        unseeded_inherited_count = sum(
            component_id in unseeded_set for component_id in inherited_ids
        )
        need(
            len(occurrence_ids) == key_frontier["local_occurrence_count"]
            and len(unattached_ids)
            == key_frontier["occurrences_without_known_block_incidence"]
            and unseeded_inherited_count > 0,
            f"key frontier:{key_id}",
        )
        expected_fibre = {
            "quotient_fibre_frontier_row_id":
                "round249-quotient-fibre-frontier:" + digest(key_id),
            "official_key_ordinal": key_frontier["official_key_ordinal"],
            "official_key_id": key_id,
            "official_key_row": key_frontier["official_key_row"],
            "local_occurrence_count": len(occurrence_ids),
            "occurrences_with_known_block_incidence":
                len(occurrence_ids) - len(unattached_ids),
            "occurrences_without_known_block_incidence":
                len(unattached_ids),
            "occurrence_ids_sha256": digest(occurrence_ids),
            "unattached_occurrence_ids_sha256": digest(unattached_ids),
            "unattached_occurrence_gauge_histogram":
                dict(sorted(gauge_deficit.items())),
            "mixed_sheet_quotient_component_count": len(component_ids),
            "mixed_sheet_quotient_component_ids_sha256":
                digest(component_ids),
            "inherited_Round244_component_count": len(inherited_ids),
            "new_Round248_wall_component_count": len(new_wall_ids),
            "seeded_quotient_component_count": len(seeded_ids),
            "unseeded_quotient_component_count": len(unseeded_ids),
            "unseeded_inherited_component_count":
                unseeded_inherited_count,
            "materialized_component_member_count":
                component_member_count_by_key[key_id],
            "known_connectivity_block_count": len(block_ids),
            "known_connectivity_block_ids_sha256": digest(block_ids),
            "frontier_status": status,
            "quotient_fibre_component_inventory_complete": True,
            "all_local_occurrences_have_known_block_incidence": False,
            "all_quotient_components_proved_maximal": False,
            "global_exact_key_fibre_exhausted": False,
            "quotient_fibre_inventory_credit": 1,
            "maximal_physical_component_credit": 0,
            "global_exact_key_fibre_credit": 0,
            "global_exact_key_disposition_credit": 0,
        }
        exact_row(
            fibre_by_key[key_id],
            expected_fibre,
            f"fibre:{key_id}",
        )
        status_histogram[status] += 1
        component_count_histogram[len(component_ids)] += 1
        keys_with_blocks += bool(block_ids)
        keys_with_new_wall += bool(new_wall_ids)
        all_unattached &= bool(unattached_ids)
        all_unseeded_inherited &= unseeded_inherited_count > 0

    block_key_set = {
        key_id for key_id, block_ids in block_ids_by_key.items()
        if block_ids
    }
    new_wall_key_set = {
        key_id for key_id, component_ids
        in new_wall_component_ids_by_key.items()
        if component_ids
    }
    expected_census = {
        "observed_exact_key_count": 116,
        "quotient_fibre_inventory_complete_count": 116,
        "globally_exhausted_exact_key_fibre_count": 0,
        "mixed_sheet_quotient_component_assignment_count":
            len(assignment_rows),
        "component_origin_histogram":
            dict(sorted(component_origin_histogram.items())),
        "mixed_sheet_quotient_component_count_histogram": {
            str(key): value
            for key, value in sorted(component_count_histogram.items())
        },
        "materialized_component_member_count": total_member_count,
        "seeded_quotient_component_count": seeded_component_count,
        "unseeded_quotient_component_count":
            len(assignment_rows) - seeded_component_count,
        "maximality_unproved_quotient_component_count":
            len(assignment_rows),
        "known_connectivity_block_count": len(block_rows),
        "keys_with_known_connectivity_blocks": keys_with_blocks,
        "keys_without_known_connectivity_blocks": 116 - keys_with_blocks,
        "keys_with_new_Round248_wall_components": keys_with_new_wall,
        "keys_without_new_Round248_wall_components": 116 - keys_with_new_wall,
        "known_block_and_new_wall_key_set_relation": {
            "intersection_count": len(block_key_set & new_wall_key_set),
            "union_count": len(block_key_set | new_wall_key_set),
            "neither_count": len(
                set(key_frontier_by_id) - (block_key_set | new_wall_key_set)
            ),
        },
        "fibre_frontier_status_histogram":
            dict(sorted(status_histogram.items())),
        "unattached_occurrence_gauge_histogram":
            dict(sorted(total_gauge_deficit.items())),
        "keys_with_unattached_occurrence_gauge_histogram":
            dict(sorted(keys_with_gauge_deficit.items())),
        "all_116_keys_have_unattached_occurrences": all_unattached,
        "all_116_keys_have_unseeded_inherited_components":
            all_unseeded_inherited,
        "post_Round249_occurrences_with_known_block_incidence": 36_200,
        "post_Round249_occurrences_without_known_block_incidence": 17_768,
        "new_occurrence_known_block_incidence_count": 0,
        "maximal_physical_component_assignment_count": 0,
        "global_exact_key_disposition_count": 0,
    }
    need(
        candidate["census"] == expected_census
        and keys_with_blocks == 24
        and keys_with_new_wall == 92
        and len(block_key_set & new_wall_key_set) == 16
        and len(block_key_set | new_wall_key_set) == 100
        and dict(total_gauge_deficit) == {
            "ROUND179_RESOLVED_CHILD": 16_444,
            "ROUND204_STRICT_OPEN_REGION": 736,
            "ROUND208_STRICT_OPEN_REGION": 588,
        }
        and dict(keys_with_gauge_deficit) == {
            "ROUND179_RESOLVED_CHILD": 116,
            "ROUND204_STRICT_OPEN_REGION": 12,
            "ROUND208_STRICT_OPEN_REGION": 24,
        },
        "census",
    )
    scope = candidate["scope_contract"]
    strict = candidate["strict_nonpromotion"]
    need(
        all(scope.values())
        and strict["new_occurrence_known_block_incidence_credit"] == 0
        and strict["maximal_physical_component_credit"] == 0
        and strict["global_exact_key_fibre_credit"] == 0
        and strict["global_exact_key_disposition_credit"] == 0
        and strict["CM2"] == "NO-GO_FOR_CLAIM",
        "scope and nonpromotion",
    )
    return {
        "status": "PASS_INDEPENDENT_ROUND249",
        "verified_exact_key_quotient_fibre_inventory_count": 116,
        "verified_component_exact_key_assignment_count": 94_444,
        "verified_materialized_component_member_count": 150_876,
        "verified_seeded_quotient_component_count": 440,
        "verified_unseeded_quotient_component_count": 94_004,
        "verified_occurrences_with_known_block_incidence": 36_200,
        "verified_occurrences_without_known_block_incidence": 17_768,
        "verified_globally_exhausted_exact_key_fibre_count": 0,
        "verified_maximal_physical_component_credit": 0,
        "candidate_result_sha256": digest(candidate),
        "producer_imported_or_executed": False,
        "CM2": "NO-GO_FOR_CLAIM",
    }


def safe_write(raw: bytes) -> None:
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{OUTPUT.name}.",
        dir=OUTPUT.parent,
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(raw)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, OUTPUT)
    finally:
        if temporary.exists():
            temporary.unlink()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-write", action="store_true")
    arguments = parser.parse_args()
    result = verify()
    document = {
        "schema": SCHEMA,
        "result": result,
        "result_sha256": digest(result),
    }
    raw = canonical(document) + b"\n"
    if not arguments.no_write:
        safe_write(raw)
    print(result["status"])
    print(json.dumps(result, sort_keys=True))
    print(f"result_sha256={document['result_sha256']}")
    print(f"verification_sha256={hashlib.sha256(raw).hexdigest()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
