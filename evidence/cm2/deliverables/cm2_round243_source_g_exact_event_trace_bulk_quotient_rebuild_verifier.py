#!/usr/bin/env python3
"""Independently verify the Round243 event-trace quotient rebuild."""

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
    / "cm2_round243_source_g_exact_event_trace_bulk_quotient_rebuild_verification.json"
)
SCHEMA = (
    "cm2.round243.source-g-exact-event-trace-bulk-quotient-rebuild."
    "verification.v1"
)
AXES = ["t", "p", "s"]
SIDES = ["LOWER", "UPPER"]
ROUND220_ROWS_SHA256 = (
    "dca8ddbb66b73ef615f1b1cd2c4b7ee453737ff18ed44e03e2ac222d5005d88f"
)
ROUND220_IDS_SHA256 = (
    "ab8fbea5baaac034b905d4ad2760519f87da25378cd8c2782015e8081ebd68cf"
)
PINS = {
    "cm2_round179_source_g_residual_tube_arrangement_rows.json":
        "f20b42c1fed781779b537b4d45bf44233eae1ed3ee620b95177a80f0eb2b5e42",
    "cm2_round220_source_g_round179_resolved_child_boundary_atlas.py":
        "ae5c4fc259050bafeef335b88a3504ba3de49c64154f128ec26a461ebefdd3f4",
    "cm2_round220_source_g_round179_resolved_child_boundary_atlas_certificate.json":
        "569a7849b53805ff4deca0eff9a6938a897942d3d682dfef27c27559135ce974",
    "cm2_round225_source_g_certified_connectivity_rebuild_certificate.json":
        "0d040af30906f22f600820e14867c45115e679e33b6ee6f052c51a914cf7d841",
    "cm2_round241_source_g_post_round240_global_incidence_overlay_certificate.json":
        "7fd00a654965d223cc9ae88de4f0456f9c743dbfa38b06d22879519a5ad79bcc",
    "cm2_round243_source_g_exact_event_trace_bulk_quotient_rebuild.py":
        "710df010b80ce2a35335d12ac4d7a0707557ee09491e269e19e735472a057e2f",
    "cm2_round243_source_g_exact_event_trace_bulk_quotient_rebuild_certificate.json":
        "8d0ca0f887a0b10f7535cc6d632ddcf4599231c882a87fb5a77875e54380a86d",
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


def qstr(value: Q) -> str:
    return (
        str(value.numerator)
        if value.denominator == 1
        else f"{value.numerator}/{value.denominator}"
    )


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


def box_values(box: list[str]) -> tuple[Q, ...]:
    values = tuple(Q(value) for value in box)
    need(
        len(values) == 6
        and values[0] < values[1]
        and values[2] < values[3]
        and values[4] < values[5],
        "positive box",
    )
    return values


def rect_for(values: tuple[Q, ...], axis: int) -> tuple[Q, ...]:
    tangential = [candidate for candidate in range(3) if candidate != axis]
    return (
        values[2 * tangential[0]],
        values[2 * tangential[0] + 1],
        values[2 * tangential[1]],
        values[2 * tangential[1] + 1],
    )


def rect_strings(rect: tuple[Q, ...]) -> list[str]:
    return [qstr(value) for value in rect]


def make_round220_id(label: str, payload: Any) -> str:
    return f"round220-{label}:{digest(payload)}"


def return_signature(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "source_chart": row["chart"],
        "target_lift": row["owner_target"],
        "ordered_integer_wall_events":
            row["ordered_integer_wall_events"],
        "signed_wall_word": row["signed_wall_word"],
        "roof": row["roof"],
        "outgoing_cell": row["outgoing_cell"],
        "target_chart": row["target_chart"],
        "official_key_row": row["official_key_row"],
        "official_key_ordinal": row["official_key_ordinal"],
        "official_key_id": row["official_key_id"],
    }


class DisjointSet:
    def __init__(self, values: list[str]) -> None:
        self.parent = {value: value for value in values}

    def find(self, value: str) -> str:
        if self.parent[value] != value:
            self.parent[value] = self.find(self.parent[value])
        return self.parent[value]

    def union(self, left: str, right: str) -> None:
        left_root = self.find(left)
        right_root = self.find(right)
        if left_root != right_root:
            low, high = sorted([left_root, right_root])
            self.parent[high] = low


def safe_write(data: bytes) -> None:
    descriptor, name = tempfile.mkstemp(
        prefix=".round243-verifier.",
        suffix=".tmp",
        dir=HERE,
    )
    temporary = Path(name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, OUTPUT)
    finally:
        if temporary.exists():
            temporary.unlink()


def reconstruct_adjacencies(
    resolved: list[dict[str, Any]],
) -> tuple[dict[str, dict[str, Any]], list[list[Any]]]:
    resolved_sorted = sorted(resolved, key=lambda row: row["row_id"])
    faces: dict[
        tuple[str, str, int, Q],
        list[list[tuple[int, tuple[Q, ...], str]]],
    ] = defaultdict(lambda: [[], []])
    for ordinal, child in enumerate(resolved_sorted):
        values = box_values(child["box"])
        for axis in range(3):
            rect = rect_for(values, axis)
            for side in range(2):
                fixed = values[2 * axis + side]
                face_id = make_round220_id(
                    "coordinate-face",
                    [
                        child["row_id"],
                        AXES[axis],
                        SIDES[side],
                        qstr(fixed),
                        rect_strings(rect),
                    ],
                )
                faces[
                    (child["parent_id"], child["chart"], axis, fixed)
                ][side].append((ordinal, rect, face_id))
    columns = [
        "coordinate_adjacency_id",
        "common_refinement_id",
        "parent_id",
        "chart",
        "axis",
        "fixed_coordinate",
        "common_refinement_half_open_box",
        "negative_side_face_id",
        "positive_side_face_id",
        "negative_side_child_ordinal",
        "positive_side_child_ordinal",
        "relation",
        "exact_full_face",
        "positive_area_common_refinement",
        "same_origin",
        "same_official_key",
        "joined_from_box_touch_or_key_equality_alone",
        "formal_coordinate_adjacency_credit",
        "event_trace_glue_credit",
        "physical_component_credit",
        "global_exact_key_disposition_credit",
    ]
    rows: list[dict[str, Any]] = []
    for (parent_id, chart, axis, fixed), sides in sorted(
        faces.items(),
        key=lambda item: (
            item[0][0],
            item[0][1],
            item[0][2],
            item[0][3],
        ),
    ):
        for positive_ordinal, positive_rect, positive_face in sides[0]:
            for negative_ordinal, negative_rect, negative_face in sides[1]:
                intersection = (
                    max(negative_rect[0], positive_rect[0]),
                    min(negative_rect[1], positive_rect[1]),
                    max(negative_rect[2], positive_rect[2]),
                    min(negative_rect[3], positive_rect[3]),
                )
                if (
                    intersection[0] >= intersection[1]
                    or intersection[2] >= intersection[3]
                ):
                    continue
                negative = resolved_sorted[negative_ordinal]
                positive = resolved_sorted[positive_ordinal]
                need(
                    negative["official_key_id"]
                    == positive["official_key_id"],
                    "adjacency key",
                )
                exact = negative_rect == positive_rect
                same_origin = (
                    negative["origin_row_id"]
                    == positive["origin_row_id"]
                )
                relation = (
                    "SAME_ORIGIN_EXACT_ONE_STEP_SPLIT"
                    if same_origin
                    else (
                        "CROSS_ORIGIN_EXACT_SHARED_PARENT_FACE"
                        if exact
                        else
                        "CROSS_ORIGIN_POSITIVE_AREA_PARENT_COMMON_REFINEMENT"
                    )
                )
                common_box = rect_strings(intersection)
                common_id = make_round220_id(
                    "parent-face-common-refinement",
                    [
                        parent_id,
                        chart,
                        AXES[axis],
                        qstr(fixed),
                        common_box,
                    ],
                )
                adjacency_id = make_round220_id(
                    "coordinate-adjacency",
                    [common_id, negative_face, positive_face],
                )
                negative_signature = return_signature(negative)
                positive_signature = return_signature(positive)
                need(
                    negative_signature == positive_signature,
                    f"full signature:{adjacency_id}",
                )
                area = (
                    (intersection[1] - intersection[0])
                    * (intersection[3] - intersection[2])
                )
                rows.append({
                    "coordinate_adjacency_id": adjacency_id,
                    "common_refinement_id": common_id,
                    "parent_id": parent_id,
                    "chart": chart,
                    "axis": AXES[axis],
                    "fixed_coordinate": qstr(fixed),
                    "common_refinement_half_open_box": common_box,
                    "negative_side_face_id": negative_face,
                    "positive_side_face_id": positive_face,
                    "negative_side_child_ordinal": negative_ordinal,
                    "positive_side_child_ordinal": positive_ordinal,
                    "relation": relation,
                    "exact_full_face": exact,
                    "positive_area_common_refinement": True,
                    "same_origin": same_origin,
                    "same_official_key": True,
                    "joined_from_box_touch_or_key_equality_alone": False,
                    "formal_coordinate_adjacency_credit": 1,
                    "event_trace_glue_credit": 0,
                    "physical_component_credit": 0,
                    "global_exact_key_disposition_credit": 0,
                    "negative_child_row_id": negative["row_id"],
                    "positive_child_row_id": positive["row_id"],
                    "signature": negative_signature,
                    "area": qstr(area),
                })
    rows.sort(key=lambda row: row["coordinate_adjacency_id"])
    packed = [
        [row[column] for column in columns]
        for row in rows
    ]
    need(
        len(rows) == 10_384
        and digest(packed) == ROUND220_ROWS_SHA256
        and digest([row[0] for row in packed])
        == ROUND220_IDS_SHA256,
        "Round220 oracle",
    )
    return {
        row["coordinate_adjacency_id"]: row for row in rows
    }, packed


def verify() -> dict[str, Any]:
    for name in PINS:
        read_pinned(
            name,
            5_000_000 if name.endswith(".py") else 400_000_000,
        )
    rows179 = load_result(
        "cm2_round179_source_g_residual_tube_arrangement_rows.json"
    )
    resolved = unpack(rows179, "resolved_3d_child_rows")
    resolved_by_id = {row["row_id"]: row for row in resolved}
    need(len(resolved_by_id) == len(resolved) == 17_192, "resolved")
    adjacency_by_id, _packed = reconstruct_adjacencies(resolved)

    round225 = load_result(
        "cm2_round225_source_g_certified_connectivity_rebuild_certificate.json"
    )
    round241 = load_result(
        "cm2_round241_source_g_post_round240_global_incidence_overlay_certificate.json"
    )
    candidate = load_result(
        "cm2_round243_source_g_exact_event_trace_bulk_quotient_rebuild_certificate.json"
    )

    edge_rows = validate_ledger(
        candidate["formal_exact_event_trace_bulk_edge_ledger"],
        "event_trace_bulk_edge_row_id",
    )
    edge_by_adjacency = {
        row["Round220_coordinate_adjacency_id"]: row
        for row in edge_rows
    }
    need(
        len(edge_rows) == len(edge_by_adjacency) == 10_384
        and set(edge_by_adjacency) == set(adjacency_by_id),
        "edge coverage",
    )
    relation_histogram: Counter[str] = Counter()
    child_dsu = DisjointSet(sorted(resolved_by_id))
    for adjacency_id, source in adjacency_by_id.items():
        edge = edge_by_adjacency[adjacency_id]
        need(
            edge["event_trace_bulk_edge_row_id"]
            == "round243-event-trace-bulk-edge:"
            + digest(adjacency_id)
            and edge["Round220_common_refinement_id"]
            == source["common_refinement_id"]
            and edge["relation"] == source["relation"]
            and edge["parent_id"] == source["parent_id"]
            and edge["chart"] == source["chart"]
            and edge["axis"] == source["axis"]
            and edge["fixed_coordinate"]
            == source["fixed_coordinate"]
            and edge["common_refinement_half_open_box"]
            == source["common_refinement_half_open_box"]
            and edge["exact_positive_area"] == source["area"]
            and edge["negative_side_child_row_id"]
            == source["negative_child_row_id"]
            and edge["positive_side_child_row_id"]
            == source["positive_child_row_id"]
            and edge["negative_side_face_id"]
            == source["negative_side_face_id"]
            and edge["positive_side_face_id"]
            == source["positive_side_face_id"]
            and edge["full_return_signature"]
            == source["signature"]
            and edge["full_return_signature_sha256"]
            == digest(source["signature"])
            and edge["exact_10_field_signature_restriction_equal"]
            is True
            and edge["same_parent_atlas"] is True
            and edge["same_source_chart"] is True
            and edge["explicit_coordinate_transition"]
            == "IDENTITY_ON_SHARED_PARENT_CHART"
            and edge[
                "accepted_from_box_touch_or_key_equality_alone"
            ] is False
            and edge["current_quotient_lower_bound_edge_credit"] == 1
            and edge["known_block_incidence_propagation_credit"] == 1
            and edge["physical_component_credit"] == 0
            and edge["global_exact_key_fibre_credit"] == 0,
            f"edge:{adjacency_id}",
        )
        relation_histogram[source["relation"]] += 1
        child_dsu.union(
            source["negative_child_row_id"],
            source["positive_child_row_id"],
        )

    child_groups: dict[str, list[str]] = defaultdict(list)
    for child_id in sorted(resolved_by_id):
        child_groups[child_dsu.find(child_id)].append(child_id)
    edge_count_by_root: Counter[str] = Counter()
    for source in adjacency_by_id.values():
        edge_count_by_root[
            child_dsu.find(source["negative_child_row_id"])
        ] += 1

    source_frontier = round241[
        "formal_post_Round241_occurrence_known_block_frontier_ledger"
    ]["rows"]
    resolved_frontier = {
        row["local_occurrence_row_id"]: row
        for row in source_frontier
        if row["local_occurrence_gauge"] == "ROUND179_RESOLVED_CHILD"
    }
    need(
        len(source_frontier) == 53_968
        and set(resolved_frontier) == set(resolved_by_id),
        "frontier binding",
    )

    component_rows = validate_ledger(
        candidate["formal_resolved_bulk_component_ledger"],
        "resolved_bulk_component_row_id",
    )
    component_by_members = {
        tuple(row["member_Round179_resolved_child_row_ids"]): row
        for row in component_rows
    }
    need(
        len(component_rows) == len(component_by_members) == 8_440,
        "component rows",
    )
    seed_blocks_by_root: dict[str, set[str]] = {}
    new_ids_by_root: dict[str, list[str]] = {}
    component_id_by_root: dict[str, str] = {}
    component_size_histogram: Counter[int] = Counter()
    seed_count_histogram: Counter[int] = Counter()
    for root, member_ids in sorted(child_groups.items()):
        row = component_by_members[tuple(member_ids)]
        seeds = {
            resolved_frontier[child_id][
                "Round225_known_connectivity_block_id"
            ]
            for child_id in member_ids
            if resolved_frontier[child_id][
                "known_block_incidence_attachment_credit"
            ] == 1
        }
        new_ids = [
            child_id
            for child_id in member_ids
            if resolved_frontier[child_id][
                "known_block_incidence_attachment_credit"
            ] == 0
            and seeds
        ]
        signatures = {
            digest(return_signature(resolved_by_id[child_id]))
            for child_id in member_ids
        }
        expected_id = (
            "round243-resolved-bulk-component:"
            + digest(member_ids)
        )
        need(
            len(signatures) == 1
            and row["resolved_bulk_component_row_id"]
            == expected_id
            and row["member_Round179_resolved_child_count"]
            == len(member_ids)
            and row["member_Round179_resolved_child_row_ids_sha256"]
            == digest(member_ids)
            and row["Round243_event_trace_bulk_edge_count"]
            == edge_count_by_root[root]
            and row["full_return_signature_sha256"]
            == next(iter(signatures))
            and row["seed_Round225_known_connectivity_block_count"]
            == len(seeds)
            and row["seed_Round225_known_connectivity_block_ids"]
            == sorted(seeds)
            and row["new_occurrence_known_block_incidence_count"]
            == len(new_ids)
            and row["new_occurrence_row_ids"] == new_ids
            and row["new_occurrence_row_ids_sha256"]
            == digest(new_ids)
            and row["maximal_physical_component_claimed"] is False,
            f"component:{root}",
        )
        seed_blocks_by_root[root] = set(seeds)
        new_ids_by_root[root] = new_ids
        component_id_by_root[root] = expected_id
        component_size_histogram[len(member_ids)] += 1
        seed_count_histogram[len(seeds)] += 1
    need(
        sum(map(len, new_ids_by_root.values())) == 272
        and sum(bool(value) for value in seed_blocks_by_root.values())
        == 440,
        "component propagation census",
    )

    old_block_rows = round225[
        "formal_certified_known_connectivity_block_ledger"
    ]["rows"]
    old_block_by_id = {
        row["known_connectivity_block_id"]: row
        for row in old_block_rows
    }
    old_block_ids = sorted(old_block_by_id)
    block_dsu = DisjointSet(old_block_ids)
    for seeds in seed_blocks_by_root.values():
        ordered = sorted(seeds)
        for other in ordered[1:]:
            block_dsu.union(ordered[0], other)
    old_groups: dict[str, list[str]] = defaultdict(list)
    for block_id in old_block_ids:
        old_groups[block_dsu.find(block_id)].append(block_id)
    need(
        len(old_groups) == 7_388
        and Counter(map(len, old_groups.values()))
        == {1: 7_372, 2: 16},
        "block union",
    )

    block_rows = validate_ledger(
        candidate["formal_Round243_known_connectivity_block_ledger"],
        "known_connectivity_block_id",
    )
    block_by_old_group = {
        tuple(row["inherited_Round225_known_connectivity_block_ids"]):
            row
        for row in block_rows
    }
    need(
        len(block_rows) == len(block_by_old_group) == 7_388,
        "new blocks",
    )
    component_ids_by_old_block: dict[str, set[str]] = defaultdict(set)
    for root, seeds in seed_blocks_by_root.items():
        for block_id in seeds:
            component_ids_by_old_block[block_id].add(
                component_id_by_root[root]
            )
    new_block_by_old: dict[str, str] = {}
    for old_blocks in old_groups.values():
        row = block_by_old_group[tuple(old_blocks)]
        member_sheets = sorted({
            sheet_id
            for block_id in old_blocks
            for sheet_id in old_block_by_id[block_id][
                "member_Round211_sheet_row_ids"
            ]
        })
        component_ids = sorted({
            component_id
            for block_id in old_blocks
            for component_id in component_ids_by_old_block[block_id]
        })
        expected_id = (
            "round243-known-connectivity-block:"
            + digest(member_sheets)
        )
        need(
            row["known_connectivity_block_id"] == expected_id
            and row["canonical_member_Round211_sheet_row_id"]
            == member_sheets[0]
            and row["member_Round211_sheet_row_count"]
            == len(member_sheets)
            and row["member_Round211_sheet_row_ids"]
            == member_sheets
            and row["member_Round211_sheet_row_ids_sha256"]
            == digest(member_sheets)
            and row[
                "inherited_Round225_known_connectivity_block_count"
            ] == len(old_blocks)
            and row[
                "inherited_Round225_known_connectivity_block_ids_sha256"
            ] == digest(old_blocks)
            and row[
                "incident_Round243_resolved_bulk_component_ids"
            ] == component_ids
            and row["maximal_physical_component_claimed"] is False,
            f"block:{expected_id}",
        )
        for block_id in old_blocks:
            new_block_by_old[block_id] = expected_id

    assignments = validate_ledger(
        candidate["formal_Round211_sheet_assignment_ledger"],
        "sheet_assignment_row_id",
    )
    assignment_by_sheet = {
        row["Round211_sheet_row_id"]: row for row in assignments
    }
    source_assignments = round225[
        "formal_Round211_sheet_assignment_ledger"
    ]["rows"]
    need(
        len(assignments) == len(assignment_by_sheet) == 17_716,
        "assignment count",
    )
    for source in source_assignments:
        sheet_id = source["Round211_sheet_row_id"]
        row = assignment_by_sheet[sheet_id]
        old_block = source["known_connectivity_block_id"]
        new_block = new_block_by_old[old_block]
        need(
            row["sheet_assignment_row_id"]
            == "round243-sheet-assignment:"
            + digest([sheet_id, new_block])
            and row["Round211_sheet_row_sha256"]
            == source["Round211_sheet_row_sha256"]
            and row["Round225_known_connectivity_block_id"]
            == old_block
            and row["Round243_known_connectivity_block_id"]
            == new_block
            and row[
                "Round243_block_changed_by_event_trace_bulk_union"
            ]
            == (len(old_groups[block_dsu.find(old_block)]) > 1)
            and row["known_block_membership_assignment_credit"] == 0,
            f"assignment:{sheet_id}",
        )

    child_root_by_id = {
        child_id: root
        for root, member_ids in child_groups.items()
        for child_id in member_ids
    }
    new_block_for_occurrence: dict[str, str] = {}
    component_for_occurrence: dict[str, str] = {}
    for root, new_ids in new_ids_by_root.items():
        if not new_ids:
            continue
        mapped = {
            new_block_by_old[block_id]
            for block_id in seed_blocks_by_root[root]
        }
        need(len(mapped) == 1, f"mapped component:{root}")
        new_block = next(iter(mapped))
        for occurrence_id in new_ids:
            new_block_for_occurrence[occurrence_id] = new_block
            component_for_occurrence[occurrence_id] = (
                component_id_by_root[root]
            )
    need(len(new_block_for_occurrence) == 272, "new occurrence map")

    delta_rows = validate_ledger(
        candidate["formal_occurrence_known_block_incidence_delta_ledger"],
        "incidence_delta_row_id",
    )
    delta_by_occurrence = {
        row["local_occurrence_row_id"]: row for row in delta_rows
    }
    need(
        len(delta_rows) == len(delta_by_occurrence) == 272
        and set(delta_by_occurrence) == set(new_block_for_occurrence),
        "delta rows",
    )
    for occurrence_id, new_block in new_block_for_occurrence.items():
        row = delta_by_occurrence[occurrence_id]
        source = resolved_frontier[occurrence_id]
        root = child_root_by_id[occurrence_id]
        need(
            row["incidence_delta_row_id"]
            == "round243-known-block-incidence-delta:"
            + digest([occurrence_id, new_block])
            and row["official_key_ordinal"]
            == source["official_key_ordinal"]
            and row["official_key_id"] == source["official_key_id"]
            and row["resolved_bulk_component_row_id"]
            == component_for_occurrence[occurrence_id]
            and row["seed_Round225_known_connectivity_block_ids"]
            == sorted(seed_blocks_by_root[root])
            and row["Round243_known_connectivity_block_id"]
            == new_block
            and row["known_block_incidence_attachment_credit"] == 1
            and row["known_block_membership_assignment_credit"] == 0
            and row["physical_component_credit"] == 0
            and row["global_exact_key_fibre_credit"] == 0,
            f"delta:{occurrence_id}",
        )

    post_rows = validate_ledger(
        candidate[
            "formal_post_Round243_occurrence_known_block_frontier_ledger"
        ],
        "post_frontier_row_id",
    )
    post_by_occurrence = {
        row["local_occurrence_row_id"]: row for row in post_rows
    }
    need(
        len(post_rows) == len(post_by_occurrence) == 53_968,
        "post rows",
    )
    attached_count = 0
    incidence_source_histogram: Counter[str] = Counter()
    grouped: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for source in source_frontier:
        occurrence_id = source["local_occurrence_row_id"]
        row = post_by_occurrence[occurrence_id]
        old_block = source["Round225_known_connectivity_block_id"]
        if source["known_block_incidence_attachment_credit"] == 1:
            expected_block = new_block_by_old[old_block]
            expected_credit = 1
            expected_source = source["incidence_source"]
        elif occurrence_id in new_block_for_occurrence:
            expected_block = new_block_for_occurrence[occurrence_id]
            expected_credit = 1
            expected_source = (
                "ROUND243_EXACT_EVENT_TRACE_BULK_COMPONENT_PROPAGATION"
            )
        else:
            expected_block = None
            expected_credit = 0
            expected_source = source["incidence_source"]
        need(
            row["Round225_known_connectivity_block_id"] == old_block
            and row["Round243_known_connectivity_block_id"]
            == expected_block
            and row["known_block_incidence_attachment_credit"]
            == expected_credit
            and row["incidence_source"] == expected_source
            and row["official_key_id"] == source["official_key_id"]
            and row["official_key_ordinal"]
            == source["official_key_ordinal"]
            and row["known_block_membership_assignment_credit"] == 0
            and row["maximal_physical_component_assignment_credit"]
            == 0
            and row["global_exact_key_fibre_exhausted"] is False,
            f"post occurrence:{occurrence_id}",
        )
        attached_count += expected_credit
        if expected_credit:
            incidence_source_histogram[expected_source] += 1
        grouped[row["official_key_ordinal"]].append(row)

    key_rows = validate_ledger(
        candidate["formal_post_Round243_key_frontier_ledger"],
        "key_frontier_row_id",
    )
    key_by_ordinal = {
        row["official_key_ordinal"]: row for row in key_rows
    }
    source_key_metadata = {
        row["official_key_ordinal"]: row
        for row in round241[
            "formal_post_Round241_key_frontier_ledger"
        ]["rows"]
    }
    delta_by_key = Counter(
        row["official_key_ordinal"] for row in delta_rows
    )
    need(len(key_rows) == len(key_by_ordinal) == 116, "key rows")
    for ordinal, occurrences in grouped.items():
        row = key_by_ordinal[ordinal]
        metadata = source_key_metadata[ordinal]
        attached = sum(
            item["known_block_incidence_attachment_credit"]
            for item in occurrences
        )
        total = len(occurrences)
        need(
            row["key_frontier_row_id"]
            == "round243-key-frontier:"
            + digest([
                ordinal,
                metadata["official_key_id"],
                attached,
                total,
            ])
            and row["official_key_id"] == metadata["official_key_id"]
            and row["official_key_row"] == metadata["official_key_row"]
            and row["local_occurrence_count"] == total
            and row["occurrences_with_known_block_incidence"]
            == attached
            and row["occurrences_without_known_block_incidence"]
            == total - attached
            and row["new_Round243_known_block_incidences"]
            == delta_by_key[ordinal]
            and row["global_exact_key_fibre_exhausted"] is False,
            f"key:{ordinal}",
        )

    expected_census = {
        "Round220_coordinate_adjacency_count": 10_384,
        "Round220_relation_histogram":
            dict(sorted(relation_histogram.items())),
        "exact_10_field_signature_equal_edge_count": 10_384,
        "signature_mismatch_edge_count": 0,
        "Round179_resolved_child_count": 17_192,
        "resolved_bulk_component_count": 8_440,
        "resolved_bulk_component_size_histogram": {
            str(size): count
            for size, count in sorted(component_size_histogram.items())
        },
        "resolved_bulk_component_seed_block_count_histogram": {
            str(count): total
            for count, total in sorted(seed_count_histogram.items())
        },
        "seeded_resolved_bulk_component_count": 440,
        "Round225_known_connectivity_block_count": 7_404,
        "Round243_known_connectivity_block_count": 7_388,
        "Round243_known_connectivity_block_reduction": 16,
        "Round241_occurrences_with_known_block_incidence": 35_908,
        "Round243_new_occurrence_known_block_incidences": 272,
        "post_Round243_occurrences_with_known_block_incidence":
            attached_count,
        "post_Round243_occurrences_without_known_block_incidence":
            53_968 - attached_count,
        "observed_exact_key_count": 116,
        "keys_touched_by_Round243": len(delta_by_key),
        "attached_incidence_source_histogram":
            dict(sorted(incidence_source_histogram.items())),
        "maximal_physical_component_assignment_count": 0,
        "global_exact_key_fibre_exhausted_count": 0,
    }
    need(
        attached_count == 36_180
        and candidate["census"] == expected_census
        and candidate["strict_nonpromotion"]["CM2"]
        == "NO-GO_FOR_CLAIM"
        and candidate["strict_nonpromotion"][
            "physical_component_credit"
        ] == 0
        and candidate["strict_nonpromotion"][
            "global_exact_key_fibre_credit"
        ] == 0,
        "candidate census and nonpromotion",
    )

    return {
        "status": "PASS_INDEPENDENT_ROUND243",
        "verified_Round220_event_trace_bulk_edge_count": 10_384,
        "verified_resolved_bulk_component_count": 8_440,
        "verified_Round243_known_connectivity_block_count": 7_388,
        "verified_Round243_block_reduction": 16,
        "verified_new_occurrence_known_block_incidence_count": 272,
        "verified_post_Round243_incidence_count": 36_180,
        "verified_post_Round243_unattached_count": 17_788,
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
