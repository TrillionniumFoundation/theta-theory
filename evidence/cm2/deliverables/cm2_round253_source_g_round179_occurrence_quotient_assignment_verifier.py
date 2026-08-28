#!/usr/bin/env python3
"""Independently verify every Round179-to-Round252 quotient assignment."""

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
OUTPUT = HERE / "cm2_round253_source_g_round179_occurrence_quotient_assignment_verification.json"
SCHEMA = "cm2.round253.source-g-round179-occurrence-quotient-assignment.verification.v1"
CANDIDATE = (
    HERE / "cm2_round253_source_g_round179_occurrence_quotient_assignment_certificate.json"
)
CANDIDATE_SHA256 = (
    "1b91b6316e06f74361fc23ce05bc765ca9d8e6b326d481bf67d89f81c351be8a"
)
PINS = {
    "cm2_round244_source_g_cross_parent_same_chart_bulk_quotient_rebuild_certificate.json":
        "5b08d568cccd302ac2dd62e7e9b6573ce83e015181ead168812159c9f882712f",
    "cm2_round251_source_g_wall_p_face_patch_saturation_certificate.json":
        "a1f1d04466585cc8b97fceaa98c1507b293696933af4a58dea3c76d92a0c480f",
    "cm2_round252_source_g_wall_s_t_face_patch_saturation_certificate.json":
        "8ffc927ca3bcefc48581bdb8b66c00f95c302f737692d14ba4cc6dc2e1ad7794",
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


def build() -> dict[str, Any]:
    round244 = load_result(
        "cm2_round244_source_g_cross_parent_same_chart_bulk_quotient_rebuild_certificate.json"
    )
    round251 = load_result(
        "cm2_round251_source_g_wall_p_face_patch_saturation_certificate.json"
    )
    round252 = load_result(
        "cm2_round252_source_g_wall_s_t_face_patch_saturation_certificate.json"
    )

    old_components = {
        row["resolved_bulk_component_row_id"]: row
        for row in round244["formal_resolved_bulk_component_ledger"]["rows"]
    }
    prior_components = {
        row["mixed_sheet_quotient_component_id"]: row
        for row in round251[
            "formal_post_Round251_mixed_sheet_component_ledger"
        ]["rows"]
    }
    quotient_components = {
        row["mixed_sheet_quotient_component_id"]: row
        for row in round252[
            "formal_post_Round252_mixed_sheet_component_ledger"
        ]["rows"]
    }
    source_frontier = round244[
        "formal_post_Round244_occurrence_known_block_frontier_ledger"
    ]["rows"]
    frontier_by_id = {
        row["local_occurrence_row_id"]: row for row in source_frontier
    }
    need(
        len(old_components) == 8_148
        and len(prior_components) == 82_036
        and len(quotient_components) == 65_740
        and len(frontier_by_id) == 53_968,
        "input census",
    )

    old_to_quotient: dict[str, str] = {}
    for quotient_id, component in quotient_components.items():
        for prior_id in component["constituent_Round251_component_ids"]:
            prior = prior_components[prior_id]
            for old_id in prior["constituent_Round250_component_ids"]:
                if old_id not in old_components:
                    continue
                need(old_id not in old_to_quotient, f"old partition:{old_id}")
                old_to_quotient[old_id] = quotient_id
    need(len(old_to_quotient) == 8_148, "all old components mapped")

    assignment_rows: list[dict[str, Any]] = []
    assignment_by_occurrence: dict[str, dict[str, Any]] = {}
    component_occurrence_histogram: Counter[int] = Counter()
    assigned_by_component: dict[str, list[str]] = defaultdict(list)
    for old_id, quotient_id in sorted(old_to_quotient.items()):
        old = old_components[old_id]
        quotient = quotient_components[quotient_id]
        seed_blocks = quotient["seed_known_connectivity_block_ids"]
        need(len(seed_blocks) <= 1, f"unique seed block:{quotient_id}")
        for occurrence_id in old["member_Round179_resolved_child_row_ids"]:
            source = frontier_by_id[occurrence_id]
            attached = source["known_block_incidence_attachment_credit"]
            need(
                source["local_occurrence_gauge"] == "ROUND179_RESOLVED_CHILD"
                and source["official_key_id"] == quotient["official_key_id"]
                and attached == int(bool(seed_blocks))
                and (
                    not attached
                    or source["Round244_known_connectivity_block_id"]
                    == seed_blocks[0]
                ),
                f"assignment consistency:{occurrence_id}",
            )
            row = closed({
                "Round179_occurrence_quotient_assignment_id":
                    "round253-round179-occurrence-quotient-assignment:"
                    + digest(occurrence_id),
                "local_occurrence_row_id": occurrence_id,
                "local_occurrence_gauge": "ROUND179_RESOLVED_CHILD",
                "official_key_ordinal": source["official_key_ordinal"],
                "official_key_id": source["official_key_id"],
                "Round244_resolved_bulk_component_id": old_id,
                "Round252_mixed_sheet_quotient_component_id": quotient_id,
                "Round252_component_seed_known_block_count":
                    len(seed_blocks),
                "Round252_component_seed_known_block_ids": seed_blocks,
                "known_block_incidence_attachment_credit": attached,
                "quotient_component_assignment_credit": 1,
                "quotient_component_maximality_credit": 0,
                "known_block_membership_assignment_credit": 0,
                "maximal_physical_component_credit": 0,
                "global_exact_key_fibre_credit": 0,
            })
            assignment_rows.append(row)
            assignment_by_occurrence[occurrence_id] = row
            assigned_by_component[quotient_id].append(occurrence_id)
    assignment_rows.sort(
        key=lambda row: row["Round179_occurrence_quotient_assignment_id"]
    )
    for occurrence_ids in assigned_by_component.values():
        component_occurrence_histogram[len(occurrence_ids)] += 1
    need(
        len(assignment_rows) == len(assignment_by_occurrence) == 17_192
        and len(assigned_by_component) == 7_932
        and dict(component_occurrence_histogram)
        == {1: 2_916, 2: 2_912, 3: 456, 4: 1_452, 5: 52,
            6: 76, 7: 32, 8: 20, 10: 8, 12: 8},
        "Round179 assignment census",
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
        assignment = assignment_by_occurrence.get(occurrence_id)
        base["Round252_mixed_sheet_quotient_component_id"] = (
            None if assignment is None
            else assignment["Round252_mixed_sheet_quotient_component_id"]
        )
        base["quotient_component_assignment_credit"] = int(
            assignment is not None
        )
        base["quotient_component_maximality_credit"] = 0
        gauge_assignment_histogram[
            f"{source['local_occurrence_gauge']}:"
            f"{int(assignment is not None)}"
        ] += 1
        post_rows.append(closed({
            "post_frontier_row_id":
                "round253-post-occurrence-quotient-frontier:"
                + digest([
                    occurrence_id,
                    base["Round252_mixed_sheet_quotient_component_id"],
                ]),
            **base,
        }))
    post_rows.sort(key=lambda row: row["post_frontier_row_id"])
    need(
        len(post_rows) == 53_968
        and dict(gauge_assignment_histogram) == {
            "ROUND179_RESOLVED_CHILD:1": 17_192,
            "ROUND204_STRICT_OPEN_REGION:0": 736,
            "ROUND208_STRICT_OPEN_REGION:0": 36_040,
        },
        "post frontier census",
    )

    key_source = {
        row["official_key_id"]: row
        for row in round244["formal_post_Round244_key_frontier_ledger"]["rows"]
    }
    post_by_key: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in post_rows:
        post_by_key[row["official_key_id"]].append(row)
    key_rows: list[dict[str, Any]] = []
    for key_id, rows in post_by_key.items():
        source = key_source[key_id]
        assigned = [
            row for row in rows
            if row["quotient_component_assignment_credit"] == 1
        ]
        key_rows.append(closed({
            "key_frontier_row_id":
                "round253-key-occurrence-quotient-frontier:"
                + digest(key_id),
            "official_key_ordinal": source["official_key_ordinal"],
            "official_key_id": key_id,
            "official_key_row": source["official_key_row"],
            "local_occurrence_count": len(rows),
            "occurrences_with_known_block_incidence": sum(
                row["known_block_incidence_attachment_credit"]
                for row in rows
            ),
            "occurrences_without_known_block_incidence": sum(
                1 - row["known_block_incidence_attachment_credit"]
                for row in rows
            ),
            "Round179_occurrence_quotient_assignment_count": len(assigned),
            "Round204_Round208_occurrence_quotient_assignment_count": 0,
            "occurrence_quotient_assignment_count": len(assigned),
            "occurrence_quotient_assignment_complete":
                len(assigned) == len(rows),
            "global_exact_key_fibre_exhausted": False,
            "maximal_physical_component_credit": 0,
            "global_exact_key_fibre_credit": 0,
        }))
    key_rows.sort(key=lambda row: row["key_frontier_row_id"])
    need(
        len(key_rows) == 116
        and sum(
            row["Round179_occurrence_quotient_assignment_count"]
            for row in key_rows
        ) == 17_192,
        "key frontier census",
    )

    attached_assignments = sum(
        row["known_block_incidence_attachment_credit"]
        for row in assignment_rows
    )
    census = {
        "Round179_occurrence_count": 17_192,
        "Round179_occurrence_quotient_assignment_count": 17_192,
        "Round179_occurrence_quotient_assignment_component_count": 7_932,
        "Round179_assignment_component_occurrence_count_histogram": {
            str(key): value
            for key, value in sorted(component_occurrence_histogram.items())
        },
        "Round179_assignments_to_seeded_components": attached_assignments,
        "Round179_assignments_to_unseeded_components":
            17_192 - attached_assignments,
        "post_Round253_occurrences_with_known_block_incidence": 36_200,
        "post_Round253_occurrences_without_known_block_incidence": 17_768,
        "new_occurrence_known_block_incidence_count": 0,
        "Round204_Round208_occurrences_without_quotient_assignment": 36_776,
        "observed_exact_key_count": 116,
        "keys_with_complete_all_gauge_occurrence_quotient_assignment": sum(
            row["occurrence_quotient_assignment_complete"]
            for row in key_rows
        ),
        "maximal_physical_component_assignment_count": 0,
        "globally_exhausted_exact_key_fibre_count": 0,
        "global_exact_key_disposition_count": 0,
    }
    return {
        "status": (
            "CERTIFIED_17192_OF_17192_ROUND179_OCCURRENCE_QUOTIENT_"
            "ASSIGNMENTS__7932_COMPONENTS__ZERO_BLOCK_OR_MAXIMALITY_PROMOTION"
        ),
        "census": census,
        "formal_input_binding": {
            name: PINS[name] for name in sorted(PINS)
        },
        "formal_Round179_occurrence_quotient_assignment_ledger": ledger(
            assignment_rows,
            "Round179_occurrence_quotient_assignment_id",
        ),
        "formal_post_Round253_occurrence_quotient_frontier_ledger": ledger(
            post_rows,
            "post_frontier_row_id",
        ),
        "formal_post_Round253_key_occurrence_quotient_frontier_ledger": ledger(
            key_rows,
            "key_frontier_row_id",
        ),
        "scope_contract": {
            "all_17192_Round179_occurrences_have_unique_Round252_components": True,
            "all_16444_unattached_Round179_occurrences_map_only_to_unseeded_components": True,
            "all_748_attached_Round179_occurrences_map_to_the_same_seed_block": True,
            "quotient_assignment_is_not_known_block_membership": True,
            "quotient_assignment_is_not_component_maximality": True,
            "Round204_and_Round208_assignments_remain_open": True,
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
            "map the 736 Round204 and 36040 Round208 strict-open-region "
            "occurrences into the saturated quotient using explicit sheet/"
            "region physical incidence; do not infer assignments from key "
            "equality"
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
        == "cm2.round253.source-g-round179-occurrence-quotient-assignment.v1"
        and digest(candidate["result"]) == candidate["result_sha256"],
        "candidate envelope",
    )
    reconstructed = build()
    need(
        reconstructed == candidate["result"],
        "independent full-result reconstruction",
    )
    census = reconstructed["census"]
    result = {
        "status": "PASS_INDEPENDENT_ROUND253",
        "producer_imported_or_executed": False,
        "candidate_result_sha256": candidate["result_sha256"],
        "verified_Round179_occurrence_count": 17_192,
        "verified_Round179_quotient_assignment_count":
            census["Round179_occurrence_quotient_assignment_count"],
        "verified_touched_Round252_component_count":
            census["Round179_occurrence_quotient_assignment_component_count"],
        "verified_seeded_assignment_count":
            census["Round179_assignments_to_seeded_components"],
        "verified_unseeded_assignment_count":
            census["Round179_assignments_to_unseeded_components"],
        "verified_complete_key_count":
            census["keys_with_complete_all_gauge_occurrence_quotient_assignment"],
        "verified_new_known_block_incidence_count": 0,
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
