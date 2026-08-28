#!/usr/bin/env python3
"""Independently verify seed-block quotient closure and Round208 assignments."""

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
OUTPUT = HERE / "cm2_round254_source_g_seed_block_quotient_closure_verification.json"
SCHEMA = "cm2.round254.source-g-seed-block-quotient-closure.verification.v1"
CANDIDATE = HERE / "cm2_round254_source_g_seed_block_quotient_closure_certificate.json"
CANDIDATE_SHA256 = (
    "b3823b57ba6112c37b63fa1eab85507659038170277634853eb0453f418c47cf"
)
PINS = {
    "cm2_round252_source_g_wall_s_t_face_patch_saturation_certificate.json":
        "8ffc927ca3bcefc48581bdb8b66c00f95c302f737692d14ba4cc6dc2e1ad7794",
    "cm2_round253_source_g_round179_occurrence_quotient_assignment_certificate.json":
        "1b91b6316e06f74361fc23ce05bc765ca9d8e6b326d481bf67d89f81c351be8a",
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


class DisjointSet:
    def __init__(self, values: list[str]) -> None:
        self.parent = {value: value for value in values}

    def find(self, value: str) -> str:
        parent = self.parent[value]
        while parent != self.parent[parent]:
            parent = self.parent[parent]
        while value != parent:
            next_value = self.parent[value]
            self.parent[value] = parent
            value = next_value
        return parent

    def union(self, left: str, right: str) -> bool:
        left_root = self.find(left)
        right_root = self.find(right)
        if left_root == right_root:
            return False
        smaller, larger = sorted((left_root, right_root))
        self.parent[larger] = smaller
        return True


def build() -> dict[str, Any]:
    round252 = load_result(
        "cm2_round252_source_g_wall_s_t_face_patch_saturation_certificate.json"
    )
    round253 = load_result(
        "cm2_round253_source_g_round179_occurrence_quotient_assignment_certificate.json"
    )
    components = {
        row["mixed_sheet_quotient_component_id"]: row
        for row in round252[
            "formal_post_Round252_mixed_sheet_component_ledger"
        ]["rows"]
    }
    source_frontier = round253[
        "formal_post_Round253_occurrence_quotient_frontier_ledger"
    ]["rows"]
    source_key_frontier = {
        row["official_key_id"]: row
        for row in round253[
            "formal_post_Round253_key_occurrence_quotient_frontier_ledger"
        ]["rows"]
    }
    need(
        len(components) == 65_740
        and len(source_frontier) == 53_968
        and len(source_key_frontier) == 116,
        "input census",
    )

    components_by_block: dict[str, list[str]] = defaultdict(list)
    for component_id, component in components.items():
        for block_id in component["seed_known_connectivity_block_ids"]:
            components_by_block[block_id].append(component_id)
    repeated_blocks = {
        block_id: sorted(component_ids)
        for block_id, component_ids in components_by_block.items()
        if len(component_ids) > 1
    }
    need(
        len(components_by_block) == 436
        and len(repeated_blocks) == 4
        and all(len(ids) == 2 for ids in repeated_blocks.values()),
        "repeated seed-block census",
    )

    quotient = DisjointSet(list(components))
    merge_rows: list[dict[str, Any]] = []
    for block_id, component_ids in sorted(repeated_blocks.items()):
        left, right = component_ids
        need(
            quotient.union(left, right)
            and components[left]["official_key_id"]
            == components[right]["official_key_id"],
            f"seed-block merge:{block_id}",
        )
        merge_rows.append(closed({
            "seed_block_component_merge_id":
                "round254-seed-block-component-merge:"
                + digest(block_id),
            "known_connectivity_block_id": block_id,
            "official_key_ordinal":
                components[left]["official_key_ordinal"],
            "official_key_id": components[left]["official_key_id"],
            "Round252_component_ids": component_ids,
            "Round252_component_ids_sha256": digest(component_ids),
            "existing_known_block_connectivity_edge_credit": 1,
            "new_physical_patch_credit": 0,
            "maximal_physical_component_credit": 0,
        }))
    merge_rows.sort(key=lambda row: row["seed_block_component_merge_id"])

    groups: dict[str, list[str]] = defaultdict(list)
    for component_id in components:
        groups[quotient.find(component_id)].append(component_id)
    need(
        len(groups) == 65_736
        and Counter(len(ids) for ids in groups.values()) == {1: 65_732, 2: 4},
        "post merge quotient census",
    )

    old_to_new: dict[str, str] = {}
    post_component_rows: list[dict[str, Any]] = []
    post_component_by_id: dict[str, dict[str, Any]] = {}
    block_to_post_component: dict[str, str] = {}
    component_count_by_key: Counter[str] = Counter()
    for old_ids_unsorted in groups.values():
        old_ids = sorted(old_ids_unsorted)
        rows = [components[component_id] for component_id in old_ids]
        keys = {
            (row["official_key_ordinal"], row["official_key_id"])
            for row in rows
        }
        seed_blocks = sorted({
            block_id
            for row in rows
            for block_id in row["seed_known_connectivity_block_ids"]
        })
        need(len(keys) == 1 and len(seed_blocks) <= 1, "component purity")
        key_ordinal, key_id = next(iter(keys))
        post_id = (
            old_ids[0]
            if len(old_ids) == 1
            else "round254-seed-block-saturated-component:"
            + digest([old_ids, seed_blocks])
        )
        for old_id in old_ids:
            old_to_new[old_id] = post_id
        if seed_blocks:
            need(
                seed_blocks[0] not in block_to_post_component,
                f"unique post block:{seed_blocks[0]}",
            )
            block_to_post_component[seed_blocks[0]] = post_id
        row = closed({
            "post_Round254_component_row_id":
                "round254-post-seed-block-component:" + digest(post_id),
            "post_Round254_mixed_sheet_quotient_component_id": post_id,
            "constituent_Round252_component_count": len(old_ids),
            "constituent_Round252_component_ids": old_ids,
            "constituent_Round252_component_ids_sha256": digest(old_ids),
            "official_key_ordinal": key_ordinal,
            "official_key_id": key_id,
            "member_Round179_resolved_child_count": sum(
                item["member_Round179_resolved_child_count"] for item in rows
            ),
            "virtual_stratum_node_count": sum(
                item["virtual_stratum_node_count"] for item in rows
            ),
            "mixed_sheet_edge_count": sum(
                item["mixed_sheet_edge_count"] for item in rows
            ),
            "materialized_member_count": sum(
                item["materialized_member_count"] for item in rows
            ),
            "seed_known_connectivity_block_count": len(seed_blocks),
            "seed_known_connectivity_block_ids": seed_blocks,
            "existing_known_block_connectivity_merge_count": len(old_ids) - 1,
            "certified_known_connectivity_only": True,
            "maximal_physical_component_claimed": False,
            "global_exact_key_fibre_credit": 0,
        })
        post_component_rows.append(row)
        post_component_by_id[post_id] = row
        component_count_by_key[key_id] += 1
    post_component_rows.sort(
        key=lambda row: row["post_Round254_component_row_id"]
    )
    need(
        len(old_to_new) == 65_740
        and len(post_component_rows) == 65_736
        and len(block_to_post_component) == 436,
        "post component partition",
    )

    map_rows = [
        closed({
            "Round252_to_Round254_component_map_id":
                "round254-component-map:" + digest(old_id),
            "Round252_mixed_sheet_quotient_component_id": old_id,
            "post_Round254_mixed_sheet_quotient_component_id": post_id,
            "component_merge_credit": int(old_id != post_id),
        })
        for old_id, post_id in sorted(old_to_new.items())
    ]
    map_rows.sort(
        key=lambda row: row["Round252_to_Round254_component_map_id"]
    )

    round208_assignment_rows: list[dict[str, Any]] = []
    round208_assignment_by_occurrence: dict[str, dict[str, Any]] = {}
    for source in source_frontier:
        if source["local_occurrence_gauge"] != "ROUND208_STRICT_OPEN_REGION":
            continue
        block_id = source["Round244_known_connectivity_block_id"]
        if block_id not in block_to_post_component:
            continue
        post_id = block_to_post_component[block_id]
        component = post_component_by_id[post_id]
        need(
            source["known_block_incidence_attachment_credit"] == 1
            and source["official_key_id"] == component["official_key_id"]
            and component["seed_known_connectivity_block_ids"] == [block_id],
            f"Round208 assignment:{source['local_occurrence_row_id']}",
        )
        row = closed({
            "Round208_occurrence_quotient_assignment_id":
                "round254-round208-occurrence-quotient-assignment:"
                + digest(source["local_occurrence_row_id"]),
            "local_occurrence_row_id": source["local_occurrence_row_id"],
            "local_occurrence_gauge": "ROUND208_STRICT_OPEN_REGION",
            "official_key_ordinal": source["official_key_ordinal"],
            "official_key_id": source["official_key_id"],
            "known_connectivity_block_id": block_id,
            "post_Round254_mixed_sheet_quotient_component_id": post_id,
            "known_block_incidence_attachment_credit": 1,
            "quotient_component_assignment_credit": 1,
            "quotient_component_maximality_credit": 0,
            "known_block_membership_assignment_credit": 0,
            "maximal_physical_component_credit": 0,
            "global_exact_key_fibre_credit": 0,
        })
        round208_assignment_rows.append(row)
        round208_assignment_by_occurrence[source["local_occurrence_row_id"]] = row
    round208_assignment_rows.sort(
        key=lambda row: row["Round208_occurrence_quotient_assignment_id"]
    )
    need(
        len(round208_assignment_rows)
        == len(round208_assignment_by_occurrence)
        == 2_020,
        "Round208 assignment census",
    )

    post_rows: list[dict[str, Any]] = []
    gauge_assignment_histogram: Counter[str] = Counter()
    for source in source_frontier:
        occurrence_id = source["local_occurrence_row_id"]
        base = {
            key: value
            for key, value in source.items()
            if key not in {"post_frontier_row_id", "row_sha256"}
        }
        old_component_id = source["Round252_mixed_sheet_quotient_component_id"]
        assignment = round208_assignment_by_occurrence.get(occurrence_id)
        post_component_id = (
            old_to_new[old_component_id]
            if old_component_id is not None
            else None if assignment is None
            else assignment["post_Round254_mixed_sheet_quotient_component_id"]
        )
        credit = int(post_component_id is not None)
        base["post_Round254_mixed_sheet_quotient_component_id"] = post_component_id
        base["quotient_component_assignment_credit"] = credit
        base["quotient_component_maximality_credit"] = 0
        gauge_assignment_histogram[
            f"{source['local_occurrence_gauge']}:{credit}"
        ] += 1
        post_rows.append(closed({
            "post_frontier_row_id":
                "round254-post-occurrence-quotient-frontier:"
                + digest([occurrence_id, post_component_id]),
            **base,
        }))
    post_rows.sort(key=lambda row: row["post_frontier_row_id"])
    need(
        len(post_rows) == 53_968
        and dict(gauge_assignment_histogram) == {
            "ROUND179_RESOLVED_CHILD:1": 17_192,
            "ROUND204_STRICT_OPEN_REGION:0": 736,
            "ROUND208_STRICT_OPEN_REGION:0": 34_020,
            "ROUND208_STRICT_OPEN_REGION:1": 2_020,
        },
        "post frontier census",
    )

    rows_by_key: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in post_rows:
        rows_by_key[row["official_key_id"]].append(row)
    key_rows: list[dict[str, Any]] = []
    for key_id, rows in rows_by_key.items():
        source = source_key_frontier[key_id]
        assigned = sum(
            row["quotient_component_assignment_credit"] for row in rows
        )
        key_rows.append(closed({
            "key_frontier_row_id":
                "round254-key-occurrence-quotient-frontier:"
                + digest(key_id),
            "official_key_ordinal": source["official_key_ordinal"],
            "official_key_id": key_id,
            "official_key_row": source["official_key_row"],
            "local_occurrence_count": len(rows),
            "occurrences_with_known_block_incidence": sum(
                row["known_block_incidence_attachment_credit"] for row in rows
            ),
            "occurrences_without_known_block_incidence": sum(
                1 - row["known_block_incidence_attachment_credit"] for row in rows
            ),
            "post_Round254_quotient_component_count":
                component_count_by_key[key_id],
            "occurrence_quotient_assignment_count": assigned,
            "occurrences_without_quotient_assignment": len(rows) - assigned,
            "occurrence_quotient_assignment_complete": assigned == len(rows),
            "global_exact_key_fibre_exhausted": False,
            "maximal_physical_component_credit": 0,
            "global_exact_key_fibre_credit": 0,
        }))
    key_rows.sort(key=lambda row: row["key_frontier_row_id"])
    complete_key_count = sum(
        row["occurrence_quotient_assignment_complete"] for row in key_rows
    )
    need(
        len(key_rows) == 116
        and sum(row["occurrence_quotient_assignment_count"] for row in key_rows)
        == 19_212
        and complete_key_count == 80,
        "key frontier census",
    )

    census = {
        "Round252_mixed_sheet_quotient_component_count": 65_740,
        "repeated_seed_known_block_count": 4,
        "seed_block_component_merge_count": 4,
        "post_Round254_mixed_sheet_quotient_component_count": 65_736,
        "distinct_seed_known_block_count": 436,
        "post_Round254_seeded_component_count": 436,
        "post_Round254_unseeded_component_count": 65_300,
        "new_Round208_occurrence_quotient_assignment_count": 2_020,
        "cumulative_occurrence_quotient_assignment_count": 19_212,
        "Round204_occurrences_without_quotient_assignment": 736,
        "Round208_occurrences_without_quotient_assignment": 34_020,
        "keys_with_complete_all_gauge_occurrence_quotient_assignment":
            complete_key_count,
        "post_Round254_occurrences_with_known_block_incidence": 36_200,
        "post_Round254_occurrences_without_known_block_incidence": 17_768,
        "new_occurrence_known_block_incidence_count": 0,
        "maximal_physical_component_assignment_count": 0,
        "globally_exhausted_exact_key_fibre_count": 0,
        "global_exact_key_disposition_count": 0,
    }
    return {
        "status": (
            "CERTIFIED_4_SAME_BLOCK_COMPONENT_MERGES__65736_COMPONENTS__"
            "2020_NEW_ROUND208_QUOTIENT_ASSIGNMENTS__ZERO_MAXIMALITY_PROMOTION"
        ),
        "census": census,
        "formal_input_binding": {
            name: PINS[name] for name in sorted(PINS)
        },
        "formal_seed_block_component_merge_ledger": ledger(
            merge_rows, "seed_block_component_merge_id"
        ),
        "formal_Round252_to_Round254_component_map_ledger": ledger(
            map_rows, "Round252_to_Round254_component_map_id"
        ),
        "formal_post_Round254_component_commitment_ledger": ledger(
            post_component_rows, "post_Round254_component_row_id"
        ),
        "formal_new_Round208_occurrence_quotient_assignment_ledger": ledger(
            round208_assignment_rows,
            "Round208_occurrence_quotient_assignment_id",
        ),
        "formal_post_Round254_occurrence_quotient_frontier_ledger": ledger(
            post_rows, "post_frontier_row_id"
        ),
        "formal_post_Round254_key_occurrence_quotient_frontier_ledger": ledger(
            key_rows, "key_frontier_row_id"
        ),
        "scope_contract": {
            "all_repeated_known_block_seeds_are_merged": True,
            "every_seed_known_block_maps_to_exactly_one_post_component": True,
            "all_2020_Round208_assignments_follow_existing_block_incidence": True,
            "known_block_incidence_is_not_newly_claimed": True,
            "quotient_assignment_is_not_component_maximality": True,
            "remaining_Round204_Round208_assignments_require_new_physical_bridges": True,
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
            "construct new explicit physical bridges for the remaining 34020 "
            "Round208 and 736 Round204 occurrences; existing key or block "
            "labels do not assign them to the saturated quotient"
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
    candidate_raw = CANDIDATE.read_bytes()
    need(
        0 < len(candidate_raw) <= 400_000_000
        and hashlib.sha256(candidate_raw).hexdigest() == CANDIDATE_SHA256,
        "candidate pin",
    )
    candidate = json.loads(candidate_raw)
    need(
        set(candidate) == {"schema", "result", "result_sha256"}
        and candidate["schema"]
        == "cm2.round254.source-g-seed-block-quotient-closure.v1"
        and digest(candidate["result"]) == candidate["result_sha256"],
        "candidate envelope",
    )
    reconstructed = build()
    need(reconstructed == candidate["result"], "independent reconstruction")
    census = reconstructed["census"]
    result = {
        "status": "PASS_INDEPENDENT_ROUND254",
        "producer_imported_or_executed": False,
        "candidate_result_sha256": candidate["result_sha256"],
        "verified_seed_block_component_merge_count":
            census["seed_block_component_merge_count"],
        "verified_post_component_count":
            census["post_Round254_mixed_sheet_quotient_component_count"],
        "verified_new_Round208_assignment_count":
            census["new_Round208_occurrence_quotient_assignment_count"],
        "verified_cumulative_occurrence_assignment_count":
            census["cumulative_occurrence_quotient_assignment_count"],
        "verified_remaining_Round204_count":
            census["Round204_occurrences_without_quotient_assignment"],
        "verified_remaining_Round208_count":
            census["Round208_occurrences_without_quotient_assignment"],
        "verified_maximal_component_assignment_count": 0,
        "CM2": "NO-GO_FOR_CLAIM",
    }
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
