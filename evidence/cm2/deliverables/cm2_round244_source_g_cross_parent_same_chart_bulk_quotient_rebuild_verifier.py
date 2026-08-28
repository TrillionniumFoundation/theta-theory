#!/usr/bin/env python3
"""Independently verify the Round244 cross-parent quotient rebuild."""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from fractions import Fraction as Q
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
    / "cm2_round244_source_g_cross_parent_same_chart_bulk_quotient_rebuild_verification.json"
)
SCHEMA = (
    "cm2.round244.source-g-cross-parent-same-chart-bulk-quotient-rebuild."
    "verification.v1"
)
PINS = {
    "cm2_round179_source_g_residual_tube_arrangement_rows.json":
        "f20b42c1fed781779b537b4d45bf44233eae1ed3ee620b95177a80f0eb2b5e42",
    "cm2_round220_source_g_round179_resolved_child_boundary_atlas_certificate.json":
        "569a7849b53805ff4deca0eff9a6938a897942d3d682dfef27c27559135ce974",
    "cm2_round243_source_g_exact_event_trace_bulk_quotient_rebuild_certificate.json":
        "8d0ca0f887a0b10f7535cc6d632ddcf4599231c882a87fb5a77875e54380a86d",
    "cm2_round244_source_g_cross_parent_same_chart_bulk_quotient_rebuild.py":
        "9cd649e269e9e734118c4a1241b9ffe9003a1e9e29ebac8e9ab17dedb4601c0e",
    "cm2_round244_source_g_cross_parent_same_chart_bulk_quotient_rebuild_certificate.json":
        "5b08d568cccd302ac2dd62e7e9b6573ce83e015181ead168812159c9f882712f",
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


def reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        need(key not in result, f"duplicate JSON key:{key}")
        result[key] = value
    return result


def reject_token(token: str) -> Any:
    raise RuntimeError(f"forbidden JSON numeric token:{token}")


def read_pinned(name: str, maximum: int = 400_000_000) -> bytes:
    path = HERE / name
    info = path.lstat()
    need(
        stat.S_ISREG(info.st_mode)
        and not path.is_symlink()
        and info.st_nlink == 1
        and 0 < info.st_size <= maximum,
        f"regular:{name}",
    )
    raw = path.read_bytes()
    need(hashlib.sha256(raw).hexdigest() == PINS[name], f"pin:{name}")
    return raw


def load_result(name: str) -> dict[str, Any]:
    document = json.loads(
        read_pinned(name),
        object_pairs_hook=reject_duplicates,
        parse_float=reject_token,
        parse_constant=reject_token,
    )
    need(
        set(document) == {"schema", "result", "result_sha256"}
        and digest(document["result"]) == document["result_sha256"],
        f"envelope:{name}",
    )
    return document["result"]


def unpack(value: dict[str, Any]) -> list[dict[str, Any]]:
    columns = value["columns"]
    return [
        dict(zip(columns, packed, strict=True))
        for packed in value["rows"]
    ]


def unpack_rows(document: dict[str, Any], table: str) -> list[dict[str, Any]]:
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
    need(
        value["row_count"] == len(rows)
        and len(rows) == len({row[id_field] for row in rows})
        and value["rows_sha256"] == digest(rows)
        and value["row_ids_sha256"]
        == digest([row[id_field] for row in rows])
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


def return_signature(row: dict[str, Any]) -> tuple[Any, ...]:
    return (
        row["chart"],
        row["owner_target"],
        tuple(row["ordered_integer_wall_events"]),
        row["signed_wall_word"],
        row["roof"],
        row["outgoing_cell"],
        row["target_chart"],
        tuple(row["official_key_row"]),
        row["official_key_ordinal"],
        row["official_key_id"],
    )


class DisjointSet:
    def __init__(self, values: list[str]) -> None:
        self.parent = {value: value for value in values}

    def find(self, value: str) -> str:
        root = value
        while self.parent[root] != root:
            root = self.parent[root]
        while self.parent[value] != value:
            value, self.parent[value] = self.parent[value], root
        return root

    def union(self, left: str, right: str) -> None:
        left_root = self.find(left)
        right_root = self.find(right)
        if left_root != right_root:
            low, high = sorted([left_root, right_root])
            self.parent[high] = low


def safe_write(raw: bytes) -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
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


def verify() -> dict[str, Any]:
    for name in PINS:
        read_pinned(
            name,
            5_000_000 if name.endswith(".py") else 400_000_000,
        )

    candidate = load_result(
        "cm2_round244_source_g_cross_parent_same_chart_bulk_quotient_rebuild_certificate.json"
    )
    reconciliation = validate_ledger(
        candidate["formal_different_parent_candidate_reconciliation_ledger"],
        "candidate_reconciliation_row_id",
    )
    edge_rows = validate_ledger(
        candidate["formal_cross_parent_same_chart_bulk_edge_ledger"],
        "cross_parent_bulk_edge_row_id",
    )
    validate_ledger(
        candidate["formal_resolved_bulk_component_ledger"],
        "resolved_bulk_component_row_id",
    )
    validate_ledger(
        candidate["formal_Round244_known_connectivity_block_carry_ledger"],
        "block_carry_row_id",
    )
    delta_rows = validate_ledger(
        candidate["formal_occurrence_known_block_incidence_delta_ledger"],
        "incidence_delta_row_id",
    )
    post_rows = validate_ledger(
        candidate["formal_post_Round244_occurrence_known_block_frontier_ledger"],
        "post_frontier_row_id",
    )
    key_rows = validate_ledger(
        candidate["formal_post_Round244_key_frontier_ledger"],
        "key_frontier_row_id",
    )

    round179 = load_result(
        "cm2_round179_source_g_residual_tube_arrangement_rows.json"
    )
    resolved = {
        row["row_id"]: row
        for row in unpack_rows(round179, "resolved_3d_child_rows")
    }
    round220 = load_result(
        "cm2_round220_source_g_round179_resolved_child_boundary_atlas_certificate.json"
    )
    tables = round220["coordinate_boundary_atlas"]["tables"]
    atlas_children = unpack(tables["resolved_child_rows"])
    faces = {
        row["face_id"]: row
        for row in unpack(tables["coordinate_face_rows"])
    }
    raw_candidates = unpack(
        tables["rejected_exact_coordinate_coincidence_rows"]
    )
    need(
        len(resolved) == len(atlas_children) == 17_192
        and len(faces) == 103_152
        and len(raw_candidates) == len(reconciliation) == 9_830,
        "raw census",
    )

    accepted_pairs: list[tuple[str, str]] = []
    accepted_ids: list[str] = []
    axis_histogram: Counter[str] = Counter()
    chart_histogram: Counter[str] = Counter()
    area_histogram: Counter[str] = Counter()
    accepted_key_ordinals: set[int] = set()
    raw_by_id = {row["candidate_id"]: row for row in raw_candidates}
    reconciliation_by_source = {
        row["Round220_candidate_id"]: row for row in reconciliation
    }
    edge_by_source = {row["Round220_candidate_id"]: row for row in edge_rows}

    for source_id, raw in sorted(raw_by_id.items()):
        negative_face = faces[raw["negative_side_face_id"]]
        positive_face = faces[raw["positive_side_face_id"]]
        negative = resolved[
            atlas_children[negative_face["child_ordinal"]]["source_child_row_id"]
        ]
        positive = resolved[
            atlas_children[positive_face["child_ordinal"]]["source_child_row_id"]
        ]
        reconciliation_row = reconciliation_by_source[source_id]
        if not raw["same_chart"]:
            need(
                reconciliation_row["physical_glue_credit"] == 0
                and source_id not in edge_by_source,
                f"cross-chart fail closed:{source_id}",
            )
            continue

        rectangle = tuple(Q(value) for value in raw["coincident_half_open_box"])
        area = (rectangle[1] - rectangle[0]) * (rectangle[3] - rectangle[2])
        need(
            raw["same_official_key"] is True
            and area > 0
            and negative["chart"] == positive["chart"]
            == raw["negative_chart"] == raw["positive_chart"]
            and return_signature(negative) == return_signature(positive)
            and negative_face["side"] == "UPPER"
            and positive_face["side"] == "LOWER"
            and negative_face["fixed_coordinate"]
            == positive_face["fixed_coordinate"]
            == raw["fixed_coordinate"]
            and negative_face["tangential_half_open_box"]
            == positive_face["tangential_half_open_box"]
            == raw["coincident_half_open_box"]
            and negative_face["coordinate_stratum_only"] is True
            and positive_face["coordinate_stratum_only"] is True
            and negative_face["event_sheet_incidence_count"] == 0
            and positive_face["event_sheet_incidence_count"] == 0,
            f"accepted physical face:{source_id}",
        )
        edge = edge_by_source[source_id]
        need(
            reconciliation_row["physical_glue_credit"] == 1
            and edge["current_quotient_lower_bound_edge_credit"] == 1
            and edge["negative_side_child_row_id"] == negative["row_id"]
            and edge["positive_side_child_row_id"] == positive["row_id"]
            and Q(edge["exact_positive_area"]) == area
            and edge["raw_exact_10_field_signature_equal"] is True
            and edge["explicit_coordinate_transition"]
            == "IDENTITY_ON_GLOBAL_SOURCE_CHART"
            and edge["global_chart_embedding_is_parent_independent"] is True
            and edge["maximal_physical_component_credit"] == 0,
            f"accepted certificate edge:{source_id}",
        )
        accepted_ids.append(source_id)
        accepted_pairs.append((negative["row_id"], positive["row_id"]))
        axis_histogram[raw["axis"]] += 1
        chart_histogram[raw["negative_chart"]] += 1
        area_histogram[str(area)] += 1
        accepted_key_ordinals.add(negative["official_key_ordinal"])

    need(
        len(accepted_ids) == len(edge_rows) == 328
        and digest(sorted(accepted_ids))
        == "08bfc67e5519fb4a74bf7effe76b5e87d0c682349f5b01ddf9fdef86b804aaa1"
        and dict(axis_histogram) == {"p": 292, "t": 36}
        and dict(chart_histogram)
        == {"G:E": 86, "G:N": 78, "G:S": 78, "G:W": 86}
        and len(accepted_key_ordinals) == 60,
        "independent accepted edge census",
    )

    round243 = load_result(
        "cm2_round243_source_g_exact_event_trace_bulk_quotient_rebuild_certificate.json"
    )
    prior_edges = round243["formal_exact_event_trace_bulk_edge_ledger"]["rows"]
    prior_frontier = round243[
        "formal_post_Round243_occurrence_known_block_frontier_ledger"
    ]["rows"]
    prior_resolved = {
        row["local_occurrence_row_id"]: row
        for row in prior_frontier
        if row["local_occurrence_gauge"] == "ROUND179_RESOLVED_CHILD"
    }
    need(
        len(prior_edges) == 10_384
        and len(prior_frontier) == 53_968
        and len(prior_resolved) == 17_192,
        "Round243 input census",
    )

    child_ids = sorted(resolved)
    old_dsu = DisjointSet(child_ids)
    for edge in prior_edges:
        old_dsu.union(
            edge["negative_side_child_row_id"],
            edge["positive_side_child_row_id"],
        )
    new_component_pairs = {
        tuple(sorted([old_dsu.find(left), old_dsu.find(right)]))
        for left, right in accepted_pairs
    }
    need(
        len(new_component_pairs) == 292
        and all(left != right for left, right in new_component_pairs),
        "new Round243 component pairs",
    )

    dsu = DisjointSet(child_ids)
    for edge in prior_edges:
        dsu.union(
            edge["negative_side_child_row_id"],
            edge["positive_side_child_row_id"],
        )
    for left, right in accepted_pairs:
        dsu.union(left, right)
    groups: dict[str, list[str]] = defaultdict(list)
    for child_id in child_ids:
        groups[dsu.find(child_id)].append(child_id)
    need(len(groups) == 8_148, "Round244 component count")

    expected_new_blocks: dict[str, str] = {}
    size_histogram: Counter[int] = Counter()
    seed_histogram: Counter[int] = Counter()
    for member_ids in groups.values():
        size_histogram[len(member_ids)] += 1
        seed_blocks = {
            prior_resolved[child_id]["Round243_known_connectivity_block_id"]
            for child_id in member_ids
            if prior_resolved[child_id][
                "known_block_incidence_attachment_credit"
            ] == 1
        }
        need(None not in seed_blocks and len(seed_blocks) <= 1, "no block merge")
        seed_histogram[len(seed_blocks)] += 1
        if seed_blocks:
            block_id = next(iter(seed_blocks))
            for child_id in member_ids:
                if prior_resolved[child_id][
                    "known_block_incidence_attachment_credit"
                ] == 0:
                    expected_new_blocks[child_id] = block_id
    need(
        len(expected_new_blocks) == 20
        and dict(size_histogram)
        == {1: 3116, 2: 2968, 3: 440, 4: 1460, 5: 52, 6: 84, 7: 8, 8: 20}
        and dict(seed_histogram) == {0: 7708, 1: 440},
        "component propagation census",
    )

    delta_by_id = {row["local_occurrence_row_id"]: row for row in delta_rows}
    need(
        set(delta_by_id) == set(expected_new_blocks)
        and all(
            delta_by_id[child_id]["Round244_known_connectivity_block_id"]
            == block_id
            and delta_by_id[child_id][
                "known_block_incidence_attachment_credit"
            ] == 1
            and delta_by_id[child_id]["physical_component_credit"] == 0
            for child_id, block_id in expected_new_blocks.items()
        ),
        "incidence delta",
    )

    prior_by_id = {row["local_occurrence_row_id"]: row for row in prior_frontier}
    post_by_id = {row["local_occurrence_row_id"]: row for row in post_rows}
    need(set(prior_by_id) == set(post_by_id), "global frontier partition")
    attached = 0
    grouped_keys: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for occurrence_id, post in post_by_id.items():
        before = prior_by_id[occurrence_id]
        expected_credit = (
            1 if occurrence_id in expected_new_blocks
            else before["known_block_incidence_attachment_credit"]
        )
        expected_block = (
            expected_new_blocks[occurrence_id]
            if occurrence_id in expected_new_blocks
            else before["Round243_known_connectivity_block_id"]
        )
        need(
            post["known_block_incidence_attachment_credit"] == expected_credit
            and post["Round244_known_connectivity_block_id"] == expected_block
            and post["maximal_physical_component_assignment_credit"] == 0
            and post["global_exact_key_fibre_exhausted"] is False,
            f"post frontier:{occurrence_id}",
        )
        attached += expected_credit
        grouped_keys[post["official_key_ordinal"]].append(post)
    need(attached == 36_200 and len(grouped_keys) == 116, "global frontier census")

    key_by_ordinal = {row["official_key_ordinal"]: row for row in key_rows}
    delta_by_key = Counter(
        row["official_key_ordinal"] for row in delta_rows
    )
    need(len(key_by_ordinal) == 116 and len(delta_by_key) == 12, "key census")
    for ordinal, occurrences in grouped_keys.items():
        row = key_by_ordinal[ordinal]
        attached_for_key = sum(
            item["known_block_incidence_attachment_credit"]
            for item in occurrences
        )
        need(
            row["local_occurrence_count"] == len(occurrences)
            and row["occurrences_with_known_block_incidence"]
            == attached_for_key
            and row["occurrences_without_known_block_incidence"]
            == len(occurrences) - attached_for_key
            and row["new_Round244_known_block_incidences"]
            == delta_by_key[ordinal]
            and row["global_exact_key_fibre_exhausted"] is False,
            f"key frontier:{ordinal}",
        )

    census = candidate["census"]
    need(
        census["accepted_cross_parent_same_chart_bulk_edge_count"] == 328
        and census["rejected_cross_chart_candidate_count"] == 9_502
        and census["Round244_resolved_bulk_component_count"] == 8_148
        and census["Round244_known_connectivity_block_count"] == 7_388
        and census["Round244_new_occurrence_known_block_incidences"] == 20
        and census["post_Round244_occurrences_with_known_block_incidence"]
        == 36_200
        and census["post_Round244_occurrences_without_known_block_incidence"]
        == 17_768
        and census["accepted_exact_area_histogram"]
        == dict(sorted(area_histogram.items()))
        and candidate["strict_nonpromotion"]["CM2"] == "NO-GO_FOR_CLAIM"
        and candidate["strict_nonpromotion"]["physical_component_credit"] == 0
        and candidate["strict_nonpromotion"]["global_exact_key_fibre_credit"] == 0,
        "candidate census and nonpromotion",
    )

    return {
        "status": "PASS_INDEPENDENT_ROUND244",
        "verified_different_parent_candidate_count": 9_830,
        "verified_cross_parent_same_chart_bulk_edge_count": 328,
        "verified_cross_chart_fail_closed_count": 9_502,
        "verified_new_Round243_component_pair_count": 292,
        "verified_resolved_bulk_component_count": 8_148,
        "verified_known_connectivity_block_count": 7_388,
        "verified_new_occurrence_known_block_incidence_count": 20,
        "verified_post_Round244_incidence_count": 36_200,
        "verified_post_Round244_unattached_count": 17_768,
        "verified_maximal_physical_component_credit": 0,
        "verified_global_exact_key_fibre_credit": 0,
        "candidate_result_sha256": digest(candidate),
        "producer_imported_or_executed": False,
        "CM2": "NO-GO_FOR_CLAIM",
    }


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
