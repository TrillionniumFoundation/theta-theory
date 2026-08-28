#!/usr/bin/env python3
"""Add block-only known-connectivity carriers to the unified quotient."""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import hashlib
import json
import os
from pathlib import Path
import stat
import tempfile
from typing import Any


HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "cm2_round255_source_g_block_carrier_quotient_augmentation_certificate.json"
SCHEMA = "cm2.round255.source-g-block-carrier-quotient-augmentation.v1"
PINS = {
    "cm2_round244_source_g_cross_parent_same_chart_bulk_quotient_rebuild_certificate.json":
        "5b08d568cccd302ac2dd62e7e9b6573ce83e015181ead168812159c9f882712f",
    "cm2_round254_source_g_seed_block_quotient_closure_certificate.json":
        "b3823b57ba6112c37b63fa1eab85507659038170277634853eb0453f418c47cf",
}


def need(value: bool, label: str) -> None:
    if not value:
        raise RuntimeError(label)


def canonical(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"),
        ensure_ascii=False, allow_nan=False,
    ).encode()


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def read_pinned(name: str) -> bytes:
    path = HERE / name
    info = path.lstat()
    need(
        stat.S_ISREG(info.st_mode) and not path.is_symlink()
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


def closed(row: dict[str, Any]) -> dict[str, Any]:
    result = dict(row)
    result["row_sha256"] = digest(result)
    return result


def ledger(rows: list[dict[str, Any]], id_field: str) -> dict[str, Any]:
    need(len(rows) == len({row[id_field] for row in rows}), f"unique:{id_field}")
    return {
        "row_count": len(rows),
        "rows_sha256": digest(rows),
        "row_ids_sha256": digest([row[id_field] for row in rows]),
        "row_hashes_sha256": digest([row["row_sha256"] for row in rows]),
        "every_row_closed_by_own_SHA256": True,
        "rows": rows,
    }


def build() -> dict[str, Any]:
    round244 = load_result(
        "cm2_round244_source_g_cross_parent_same_chart_bulk_quotient_rebuild_certificate.json"
    )
    round254 = load_result(
        "cm2_round254_source_g_seed_block_quotient_closure_certificate.json"
    )
    source_components = round254[
        "formal_post_Round254_component_commitment_ledger"
    ]["rows"]
    source_frontier = round254[
        "formal_post_Round254_occurrence_quotient_frontier_ledger"
    ]["rows"]
    source_keys = {
        row["official_key_id"]: row
        for row in round254[
            "formal_post_Round254_key_occurrence_quotient_frontier_ledger"
        ]["rows"]
    }
    all_blocks = {
        row["Round243_known_connectivity_block_id"]
        for row in round244[
            "formal_Round244_known_connectivity_block_carry_ledger"
        ]["rows"]
    }
    represented_blocks = {
        block_id
        for row in source_components
        for block_id in row["seed_known_connectivity_block_ids"]
    }
    block_only_ids = sorted(all_blocks - represented_blocks)
    need(
        len(source_components) == 65_736
        and len(source_frontier) == 53_968
        and len(source_keys) == 116
        and len(all_blocks) == 7_388
        and len(represented_blocks) == 436
        and len(block_only_ids) == 6_952,
        "input partition",
    )

    occurrences_by_block: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in source_frontier:
        block_id = row["Round244_known_connectivity_block_id"]
        if block_id is not None:
            occurrences_by_block[block_id].append(row)
    need(set(occurrences_by_block) == all_blocks, "all blocks have occurrences")

    carrier_rows: list[dict[str, Any]] = []
    block_to_component: dict[str, str] = {}
    carrier_count_by_key: Counter[str] = Counter()
    carrier_size_histogram: Counter[int] = Counter()
    for block_id in block_only_ids:
        occurrences = occurrences_by_block[block_id]
        keys = {
            (row["official_key_ordinal"], row["official_key_id"])
            for row in occurrences
        }
        need(len(keys) == 1, f"block key purity:{block_id}")
        key_ordinal, key_id = next(iter(keys))
        occurrence_ids = sorted(
            row["local_occurrence_row_id"] for row in occurrences
        )
        component_id = "round255-known-block-carrier-component:" + digest(block_id)
        block_to_component[block_id] = component_id
        carrier_count_by_key[key_id] += 1
        carrier_size_histogram[len(occurrence_ids)] += 1
        carrier_rows.append(closed({
            "block_carrier_component_row_id":
                "round255-block-carrier-component:" + digest(component_id),
            "post_Round255_quotient_component_id": component_id,
            "component_origin": "ROUND244_KNOWN_BLOCK_ONLY_CARRIER",
            "known_connectivity_block_id": block_id,
            "official_key_ordinal": key_ordinal,
            "official_key_id": key_id,
            "member_occurrence_count": len(occurrence_ids),
            "member_occurrence_ids": occurrence_ids,
            "member_occurrence_ids_sha256": digest(occurrence_ids),
            "certified_known_connectivity_only": True,
            "new_physical_patch_credit": 0,
            "maximal_physical_component_claimed": False,
            "global_exact_key_fibre_credit": 0,
        }))
    carrier_rows.sort(key=lambda row: row["block_carrier_component_row_id"])
    need(
        len(carrier_rows) == len(block_to_component) == 6_952
        and sum(
            row["member_occurrence_count"] for row in carrier_rows
        ) == 33_432,
        "carrier census",
    )

    assignment_rows: list[dict[str, Any]] = []
    assignment_by_occurrence: dict[str, dict[str, Any]] = {}
    for source in source_frontier:
        if (
            source["local_occurrence_gauge"] != "ROUND208_STRICT_OPEN_REGION"
            or source["quotient_component_assignment_credit"] == 1
        ):
            continue
        block_id = source["Round244_known_connectivity_block_id"]
        if block_id not in block_to_component:
            continue
        need(
            source["known_block_incidence_attachment_credit"] == 1,
            f"block-only assignment:{source['local_occurrence_row_id']}",
        )
        row = closed({
            "Round208_block_carrier_assignment_id":
                "round255-round208-block-carrier-assignment:"
                + digest(source["local_occurrence_row_id"]),
            "local_occurrence_row_id": source["local_occurrence_row_id"],
            "official_key_ordinal": source["official_key_ordinal"],
            "official_key_id": source["official_key_id"],
            "known_connectivity_block_id": block_id,
            "post_Round255_quotient_component_id":
                block_to_component[block_id],
            "known_block_incidence_attachment_credit": 1,
            "quotient_component_assignment_credit": 1,
            "quotient_component_maximality_credit": 0,
            "new_known_block_incidence_credit": 0,
            "maximal_physical_component_credit": 0,
        })
        assignment_rows.append(row)
        assignment_by_occurrence[source["local_occurrence_row_id"]] = row
    assignment_rows.sort(
        key=lambda row: row["Round208_block_carrier_assignment_id"]
    )
    need(
        len(assignment_rows) == len(assignment_by_occurrence) == 33_432,
        "block-only Round208 assignment census",
    )

    post_rows: list[dict[str, Any]] = []
    gauge_histogram: Counter[str] = Counter()
    for source in source_frontier:
        occurrence_id = source["local_occurrence_row_id"]
        base = {
            key: value
            for key, value in source.items()
            if key not in {"post_frontier_row_id", "row_sha256"}
        }
        assignment = assignment_by_occurrence.get(occurrence_id)
        component_id = source["post_Round254_mixed_sheet_quotient_component_id"]
        if assignment is not None:
            component_id = assignment["post_Round255_quotient_component_id"]
        credit = int(component_id is not None)
        base["post_Round255_quotient_component_id"] = component_id
        base["quotient_component_assignment_credit"] = credit
        base["quotient_component_maximality_credit"] = 0
        gauge_histogram[f"{source['local_occurrence_gauge']}:{credit}"] += 1
        post_rows.append(closed({
            "post_frontier_row_id":
                "round255-post-unified-quotient-frontier:"
                + digest([occurrence_id, component_id]),
            **base,
        }))
    post_rows.sort(key=lambda row: row["post_frontier_row_id"])
    need(
        len(post_rows) == 53_968
        and dict(gauge_histogram) == {
            "ROUND179_RESOLVED_CHILD:1": 17_192,
            "ROUND204_STRICT_OPEN_REGION:0": 736,
            "ROUND208_STRICT_OPEN_REGION:0": 588,
            "ROUND208_STRICT_OPEN_REGION:1": 35_452,
        },
        "post frontier census",
    )

    rows_by_key: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in post_rows:
        rows_by_key[row["official_key_id"]].append(row)
    key_rows: list[dict[str, Any]] = []
    for key_id, rows in rows_by_key.items():
        source = source_keys[key_id]
        assigned = sum(
            row["quotient_component_assignment_credit"] for row in rows
        )
        post_component_count = (
            source["post_Round254_quotient_component_count"]
            + carrier_count_by_key[key_id]
        )
        key_rows.append(closed({
            "key_frontier_row_id":
                "round255-key-unified-quotient-frontier:" + digest(key_id),
            "official_key_ordinal": source["official_key_ordinal"],
            "official_key_id": key_id,
            "official_key_row": source["official_key_row"],
            "local_occurrence_count": len(rows),
            "post_Round255_quotient_component_count": post_component_count,
            "new_block_carrier_component_count": carrier_count_by_key[key_id],
            "occurrence_quotient_assignment_count": assigned,
            "occurrences_without_quotient_assignment": len(rows) - assigned,
            "occurrence_quotient_assignment_complete": assigned == len(rows),
            "occurrences_with_known_block_incidence": sum(
                row["known_block_incidence_attachment_credit"] for row in rows
            ),
            "occurrences_without_known_block_incidence": sum(
                1 - row["known_block_incidence_attachment_credit"] for row in rows
            ),
            "global_exact_key_fibre_exhausted": False,
            "maximal_physical_component_credit": 0,
            "global_exact_key_fibre_credit": 0,
        }))
    key_rows.sort(key=lambda row: row["key_frontier_row_id"])
    complete_keys = sum(
        row["occurrence_quotient_assignment_complete"] for row in key_rows
    )
    need(
        len(key_rows) == 116
        and sum(row["occurrence_quotient_assignment_count"] for row in key_rows)
        == 52_644
        and complete_keys == 80,
        "key frontier census",
    )

    census = {
        "Round254_mixed_sheet_quotient_component_count": 65_736,
        "new_known_block_only_carrier_component_count": 6_952,
        "post_Round255_unified_quotient_component_count": 72_688,
        "new_Round208_block_carrier_assignment_count": 33_432,
        "cumulative_occurrence_quotient_assignment_count": 52_644,
        "Round208_occurrences_without_quotient_assignment": 588,
        "Round204_occurrences_without_quotient_assignment": 736,
        "total_occurrences_without_quotient_assignment": 1_324,
        "known_connectivity_block_count": 7_388,
        "known_blocks_represented_in_unified_quotient": 7_388,
        "keys_with_complete_all_gauge_occurrence_quotient_assignment":
            complete_keys,
        "post_Round255_occurrences_with_known_block_incidence": 36_200,
        "post_Round255_occurrences_without_known_block_incidence": 17_768,
        "new_occurrence_known_block_incidence_count": 0,
        "maximal_physical_component_assignment_count": 0,
        "globally_exhausted_exact_key_fibre_count": 0,
        "global_exact_key_disposition_count": 0,
        "block_carrier_occurrence_count_histogram": {
            str(key): value
            for key, value in sorted(carrier_size_histogram.items())
        },
    }
    return {
        "status": (
            "CERTIFIED_6952_BLOCK_CARRIER_COMPONENTS__33432_NEW_ROUND208_"
            "ASSIGNMENTS__52644_OF_53968_UNIFIED_QUOTIENT_ASSIGNMENTS"
        ),
        "census": census,
        "formal_input_binding": {
            name: PINS[name] for name in sorted(PINS)
        },
        "formal_new_known_block_carrier_component_ledger": ledger(
            carrier_rows, "block_carrier_component_row_id"
        ),
        "formal_new_Round208_block_carrier_assignment_ledger": ledger(
            assignment_rows, "Round208_block_carrier_assignment_id"
        ),
        "formal_post_Round255_unified_occurrence_quotient_frontier_ledger": ledger(
            post_rows, "post_frontier_row_id"
        ),
        "formal_post_Round255_key_unified_quotient_frontier_ledger": ledger(
            key_rows, "key_frontier_row_id"
        ),
        "scope_contract": {
            "all_7388_known_blocks_are_represented_in_the_unified_quotient": True,
            "all_35452_block_attached_Round208_occurrences_have_quotient_assignments": True,
            "all_588_unattached_Round208_occurrences_remain_fail_closed": True,
            "all_736_Round204_occurrences_remain_fail_closed": True,
            "block_carrier_assignment_is_not_component_maximality": True,
            "no_new_known_block_incidence_is_claimed": True,
        },
        "strict_nonpromotion": {
            "new_occurrence_known_block_incidence_credit": 0,
            "known_block_membership_assignment_credit": 0,
            "physical_component_credit": 0,
            "maximal_physical_component_credit": 0,
            "global_exact_key_fibre_credit": 0,
            "global_exact_key_disposition_credit": 0,
            "Gate5_filled_field_slot_count": 10,
            "Gate5_total_field_slot_count": 18,
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "required_next": (
            "construct explicit physical incidence for the final 588 "
            "sheetless Round208 and 736 Round204 occurrences, then audit "
            "component maximality"
        ),
    }


def safe_write(raw: bytes) -> None:
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{OUTPUT.name}.", dir=OUTPUT.parent
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
    result = build()
    document = {"schema": SCHEMA, "result": result, "result_sha256": digest(result)}
    raw = canonical(document) + b"\n"
    if not arguments.no_write:
        safe_write(raw)
    print(result["status"])
    print(json.dumps(result["census"], sort_keys=True))
    print(f"result_sha256={document['result_sha256']}")
    print(f"certificate_sha256={hashlib.sha256(raw).hexdigest()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
