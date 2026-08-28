#!/usr/bin/env python3
"""Rebuild the source-G quotient with exact Round220 event-trace edges."""

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
    / "cm2_round243_source_g_exact_event_trace_bulk_quotient_rebuild_certificate.json"
)
SCHEMA = (
    "cm2.round243.source-g-exact-event-trace-bulk-quotient-rebuild.v1"
)
AXES = ["t", "p", "s"]
SIDES = ["LOWER", "UPPER"]
ROUND220_ADJACENCY_ROWS_SHA256 = (
    "dca8ddbb66b73ef615f1b1cd2c4b7ee453737ff18ed44e03e2ac222d5005d88f"
)
ROUND220_ADJACENCY_IDS_SHA256 = (
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


def closed(row: dict[str, Any]) -> dict[str, Any]:
    result = dict(row)
    result["row_sha256"] = digest(result)
    return result


def ledger(rows: list[dict[str, Any]], id_field: str) -> dict[str, Any]:
    need(
        len(rows) == len({row[id_field] for row in rows}),
        f"unique:{id_field}",
    )
    return {
        "row_count": len(rows),
        "rows_sha256": digest(rows),
        "row_ids_sha256": digest([row[id_field] for row in rows]),
        "row_hashes_sha256": digest([row["row_sha256"] for row in rows]),
        "every_row_closed_by_own_SHA256": True,
        "rows": rows,
    }


def make_round220_id(label: str, payload: Any) -> str:
    return f"round220-{label}:{digest(payload)}"


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
        parent = self.parent[value]
        while parent != self.parent[parent]:
            self.parent[parent] = self.parent[self.parent[parent]]
            parent = self.parent[parent]
        while value != parent:
            following = self.parent[value]
            self.parent[value] = parent
            value = following
        return parent

    def union(self, left: str, right: str) -> None:
        left_root = self.find(left)
        right_root = self.find(right)
        if left_root == right_root:
            return
        low, high = sorted([left_root, right_root])
        self.parent[high] = low


def safe_write(data: bytes) -> None:
    descriptor, name = tempfile.mkstemp(
        prefix=".round243.",
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


def rebuild_round220_adjacencies(
    resolved: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    resolved_sorted = sorted(resolved, key=lambda row: row["row_id"])
    face_groups: dict[
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
                face_groups[
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
    source_rows: list[dict[str, Any]] = []
    edge_rows: list[dict[str, Any]] = []
    for (parent_id, chart, axis, fixed), sides in sorted(
        face_groups.items(),
        key=lambda item: (
            item[0][0],
            item[0][1],
            item[0][2],
            item[0][3],
        ),
    ):
        for (
            positive_ordinal,
            positive_rect,
            positive_face,
        ) in sides[0]:
            for (
                negative_ordinal,
                negative_rect,
                negative_face,
            ) in sides[1]:
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
                    "Round220 exact key agreement",
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
                source_row = {
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
                }
                source_rows.append(source_row)
                negative_signature = return_signature(negative)
                positive_signature = return_signature(positive)
                need(
                    negative_signature == positive_signature,
                    f"exact full signature restriction:{adjacency_id}",
                )
                area = (
                    (intersection[1] - intersection[0])
                    * (intersection[3] - intersection[2])
                )
                need(area > 0, f"positive area:{adjacency_id}")
                edge_rows.append(closed({
                    "event_trace_bulk_edge_row_id":
                        "round243-event-trace-bulk-edge:"
                        + digest(adjacency_id),
                    "Round220_coordinate_adjacency_id": adjacency_id,
                    "Round220_common_refinement_id": common_id,
                    "relation": relation,
                    "parent_id": parent_id,
                    "chart": chart,
                    "axis": AXES[axis],
                    "fixed_coordinate": qstr(fixed),
                    "common_refinement_half_open_box": common_box,
                    "exact_positive_area": qstr(area),
                    "negative_side_child_row_id": negative["row_id"],
                    "positive_side_child_row_id": positive["row_id"],
                    "negative_side_face_id": negative_face,
                    "positive_side_face_id": positive_face,
                    "full_return_signature":
                        negative_signature,
                    "full_return_signature_sha256":
                        digest(negative_signature),
                    "exact_10_field_signature_restriction_equal": True,
                    "same_parent_atlas": True,
                    "same_source_chart": True,
                    "explicit_coordinate_transition":
                        "IDENTITY_ON_SHARED_PARENT_CHART",
                    "both_closed_children_have_strict_dynamic_signature":
                        True,
                    "event_zero_set_absent_on_both_closed_children":
                        True,
                    "accepted_from_box_touch_or_key_equality_alone":
                        False,
                    "current_quotient_lower_bound_edge_credit": 1,
                    "known_block_incidence_propagation_credit": 1,
                    "known_block_membership_assignment_credit": 0,
                    "physical_component_credit": 0,
                    "maximal_physical_component_credit": 0,
                    "global_exact_key_fibre_credit": 0,
                }))
    source_rows.sort(
        key=lambda row: row["coordinate_adjacency_id"]
    )
    edge_rows.sort(
        key=lambda row: row["event_trace_bulk_edge_row_id"]
    )
    packed = [
        [row[column] for column in columns]
        for row in source_rows
    ]
    need(
        len(source_rows) == len(edge_rows) == 10_384
        and digest(packed) == ROUND220_ADJACENCY_ROWS_SHA256
        and digest([row[0] for row in packed])
        == ROUND220_ADJACENCY_IDS_SHA256,
        "exact Round220 adjacency reconstruction",
    )
    return source_rows, edge_rows


def build() -> dict[str, Any]:
    for name in PINS:
        read_pinned(
            name,
            5_000_000 if name.endswith(".py") else 400_000_000,
        )

    rows179 = load_result(
        "cm2_round179_source_g_residual_tube_arrangement_rows.json"
    )
    resolved = unpack(rows179, "resolved_3d_child_rows")
    need(len(resolved) == 17_192, "Round179 resolved child count")
    resolved_by_id = {row["row_id"]: row for row in resolved}
    need(len(resolved_by_id) == len(resolved), "unique resolved children")
    source_adjacencies, edge_rows = rebuild_round220_adjacencies(
        resolved
    )

    child_dsu = DisjointSet(sorted(resolved_by_id))
    edge_count_by_child_root: Counter[str] = Counter()
    for edge in edge_rows:
        child_dsu.union(
            edge["negative_side_child_row_id"],
            edge["positive_side_child_row_id"],
        )
    child_groups: dict[str, list[str]] = defaultdict(list)
    for child_id in sorted(resolved_by_id):
        child_groups[child_dsu.find(child_id)].append(child_id)
    for edge in edge_rows:
        root = child_dsu.find(edge["negative_side_child_row_id"])
        need(
            root == child_dsu.find(edge["positive_side_child_row_id"]),
            "edge component",
        )
        edge_count_by_child_root[root] += 1

    round241 = load_result(
        "cm2_round241_source_g_post_round240_global_incidence_overlay_certificate.json"
    )
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
        and len(resolved_frontier) == 17_192
        and set(resolved_frontier) == set(resolved_by_id),
        "Round241 resolved frontier binding",
    )

    seed_blocks_by_child_root: dict[str, set[str]] = {}
    newly_attached_ids_by_child_root: dict[str, list[str]] = {}
    component_rows: list[dict[str, Any]] = []
    component_id_by_child_root: dict[str, str] = {}
    child_root_by_id: dict[str, str] = {}
    seeded_component_count = 0
    for root, member_ids in sorted(child_groups.items()):
        for child_id in member_ids:
            child_root_by_id[child_id] = root
        seed_blocks = {
            resolved_frontier[child_id][
                "Round225_known_connectivity_block_id"
            ]
            for child_id in member_ids
            if resolved_frontier[child_id][
                "known_block_incidence_attachment_credit"
            ] == 1
        }
        need(None not in seed_blocks, f"non-null seeds:{root}")
        new_ids = [
            child_id
            for child_id in member_ids
            if resolved_frontier[child_id][
                "known_block_incidence_attachment_credit"
            ] == 0
            and seed_blocks
        ]
        if seed_blocks:
            seeded_component_count += 1
        seed_blocks_by_child_root[root] = set(seed_blocks)
        newly_attached_ids_by_child_root[root] = new_ids
        component_id = (
            "round243-resolved-bulk-component:"
            + digest(member_ids)
        )
        component_id_by_child_root[root] = component_id
        signatures = {
            digest(return_signature(resolved_by_id[child_id]))
            for child_id in member_ids
        }
        need(len(signatures) == 1, f"component signature:{root}")
        component_rows.append(closed({
            "resolved_bulk_component_row_id": component_id,
            "member_Round179_resolved_child_count": len(member_ids),
            "member_Round179_resolved_child_row_ids": member_ids,
            "member_Round179_resolved_child_row_ids_sha256":
                digest(member_ids),
            "Round243_event_trace_bulk_edge_count":
                edge_count_by_child_root[root],
            "full_return_signature_sha256": next(iter(signatures)),
            "seed_Round225_known_connectivity_block_count":
                len(seed_blocks),
            "seed_Round225_known_connectivity_block_ids":
                sorted(seed_blocks),
            "new_occurrence_known_block_incidence_count": len(new_ids),
            "new_occurrence_row_ids": new_ids,
            "new_occurrence_row_ids_sha256": digest(new_ids),
            "certified_known_connectivity_only": True,
            "maximal_physical_component_claimed": False,
            "global_exact_key_fibre_credit": 0,
        }))
    component_rows.sort(
        key=lambda row: row["resolved_bulk_component_row_id"]
    )

    need(
        len(component_rows) == 8_440
        and seeded_component_count == 440
        and sum(
            len(values)
            for values in newly_attached_ids_by_child_root.values()
        ) == 272,
        "resolved bulk component census",
    )

    round225 = load_result(
        "cm2_round225_source_g_certified_connectivity_rebuild_certificate.json"
    )
    old_block_rows = round225[
        "formal_certified_known_connectivity_block_ledger"
    ]["rows"]
    old_block_ids = sorted(
        row["known_connectivity_block_id"] for row in old_block_rows
    )
    need(len(old_block_ids) == 7_404, "Round225 block count")
    block_dsu = DisjointSet(old_block_ids)
    for seed_blocks in seed_blocks_by_child_root.values():
        ordered = sorted(seed_blocks)
        for other in ordered[1:]:
            block_dsu.union(ordered[0], other)

    old_blocks_by_root: dict[str, list[str]] = defaultdict(list)
    for block_id in old_block_ids:
        old_blocks_by_root[block_dsu.find(block_id)].append(block_id)
    need(
        len(old_blocks_by_root) == 7_388
        and Counter(
            len(blocks) for blocks in old_blocks_by_root.values()
        ) == {1: 7_372, 2: 16},
        "Round243 block reduction",
    )

    old_block_by_id = {
        row["known_connectivity_block_id"]: row
        for row in old_block_rows
    }
    component_ids_by_old_block: dict[str, set[str]] = defaultdict(set)
    for root, seed_blocks in seed_blocks_by_child_root.items():
        component_id = component_id_by_child_root[root]
        for block_id in seed_blocks:
            component_ids_by_old_block[block_id].add(component_id)

    new_block_rows: list[dict[str, Any]] = []
    new_block_by_old_block: dict[str, str] = {}
    for root, old_blocks in sorted(old_blocks_by_root.items()):
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
        new_block_id = (
            "round243-known-connectivity-block:"
            + digest(member_sheets)
        )
        for block_id in old_blocks:
            new_block_by_old_block[block_id] = new_block_id
        new_block_rows.append(closed({
            "known_connectivity_block_id": new_block_id,
            "canonical_member_Round211_sheet_row_id":
                member_sheets[0],
            "member_Round211_sheet_row_count": len(member_sheets),
            "member_Round211_sheet_row_ids": member_sheets,
            "member_Round211_sheet_row_ids_sha256":
                digest(member_sheets),
            "inherited_Round225_known_connectivity_block_count":
                len(old_blocks),
            "inherited_Round225_known_connectivity_block_ids":
                old_blocks,
            "inherited_Round225_known_connectivity_block_ids_sha256":
                digest(old_blocks),
            "incident_Round243_resolved_bulk_component_count":
                len(component_ids),
            "incident_Round243_resolved_bulk_component_ids":
                component_ids,
            "certified_known_connectivity": True,
            "maximal_physical_component_claimed": False,
            "component_exhaustion_credit": 0,
            "global_exact_key_fibre_credit": 0,
        }))
    new_block_rows.sort(
        key=lambda row: row["known_connectivity_block_id"]
    )
    need(
        len(new_block_rows) == len({
            row["known_connectivity_block_id"]
            for row in new_block_rows
        }) == 7_388
        and len(new_block_by_old_block) == 7_404,
        "new block ledger",
    )

    sheet_assignment_rows: list[dict[str, Any]] = []
    for source in round225[
        "formal_Round211_sheet_assignment_ledger"
    ]["rows"]:
        old_block = source["known_connectivity_block_id"]
        new_block = new_block_by_old_block[old_block]
        sheet_assignment_rows.append(closed({
            "sheet_assignment_row_id":
                "round243-sheet-assignment:"
                + digest([
                    source["Round211_sheet_row_id"],
                    new_block,
                ]),
            "Round211_sheet_row_id": source["Round211_sheet_row_id"],
            "Round211_sheet_row_sha256":
                source["Round211_sheet_row_sha256"],
            "Round225_known_connectivity_block_id": old_block,
            "Round243_known_connectivity_block_id": new_block,
            "Round243_block_changed_by_event_trace_bulk_union":
                len(
                    old_blocks_by_root[
                        block_dsu.find(old_block)
                    ]
                ) > 1,
            "known_block_membership_assignment_credit": 0,
            "maximal_physical_component_assignment_credit": 0,
            "global_exact_key_fibre_credit": 0,
        }))
    sheet_assignment_rows.sort(
        key=lambda row: row["sheet_assignment_row_id"]
    )
    need(
        len(sheet_assignment_rows) == 17_716
        and len({
            row["Round211_sheet_row_id"]
            for row in sheet_assignment_rows
        }) == 17_716,
        "sheet assignment partition",
    )

    new_block_for_new_occurrence: dict[str, str] = {}
    component_for_new_occurrence: dict[str, str] = {}
    for root, child_ids in newly_attached_ids_by_child_root.items():
        if not child_ids:
            continue
        seed_blocks = seed_blocks_by_child_root[root]
        mapped = {
            new_block_by_old_block[block_id]
            for block_id in seed_blocks
        }
        need(
            len(mapped) == 1,
            f"one rebuilt block:{root}:{sorted(seed_blocks)}:{sorted(mapped)}",
        )
        new_block = next(iter(mapped))
        for child_id in child_ids:
            new_block_for_new_occurrence[child_id] = new_block
            component_for_new_occurrence[child_id] = (
                component_id_by_child_root[root]
            )
    need(
        len(new_block_for_new_occurrence) == 272,
        "new occurrence mapping",
    )

    delta_rows: list[dict[str, Any]] = []
    for occurrence_id in sorted(new_block_for_new_occurrence):
        child_root = child_root_by_id[occurrence_id]
        source = resolved_frontier[occurrence_id]
        need(
            source["known_block_incidence_attachment_credit"] == 0
            and source["Round225_known_connectivity_block_id"] is None,
            f"new incidence precondition:{occurrence_id}",
        )
        delta_rows.append(closed({
            "incidence_delta_row_id":
                "round243-known-block-incidence-delta:"
                + digest([
                    occurrence_id,
                    new_block_for_new_occurrence[occurrence_id],
                ]),
            "local_occurrence_row_id": occurrence_id,
            "local_occurrence_gauge": "ROUND179_RESOLVED_CHILD",
            "official_key_ordinal": source["official_key_ordinal"],
            "official_key_id": source["official_key_id"],
            "resolved_bulk_component_row_id":
                component_for_new_occurrence[occurrence_id],
            "seed_Round225_known_connectivity_block_ids":
                sorted(seed_blocks_by_child_root[child_root]),
            "Round243_known_connectivity_block_id":
                new_block_for_new_occurrence[occurrence_id],
            "derivation": (
                "ROUND220_SHARED_PARENT_CHART_IDENTITY_PLUS_EXACT_"
                "10_FIELD_EVENT_TRACE_RESTRICTION"
            ),
            "known_block_incidence_attachment_credit": 1,
            "known_block_membership_assignment_credit": 0,
            "physical_component_credit": 0,
            "maximal_physical_component_credit": 0,
            "global_exact_key_fibre_credit": 0,
        }))
    delta_rows.sort(key=lambda row: row["incidence_delta_row_id"])

    post_rows: list[dict[str, Any]] = []
    for source in source_frontier:
        occurrence_id = source["local_occurrence_row_id"]
        base = {
            key: value
            for key, value in source.items()
            if key not in {"post_frontier_row_id", "row_sha256"}
        }
        old_block = source["Round225_known_connectivity_block_id"]
        if source["known_block_incidence_attachment_credit"] == 1:
            need(old_block is not None, f"old attached block:{occurrence_id}")
            current_block = new_block_by_old_block[old_block]
        elif occurrence_id in new_block_for_new_occurrence:
            need(old_block is None, f"new old block null:{occurrence_id}")
            current_block = new_block_for_new_occurrence[occurrence_id]
            base["known_block_incidence_attachment_credit"] = 1
            base["incidence_source"] = (
                "ROUND243_EXACT_EVENT_TRACE_BULK_COMPONENT_PROPAGATION"
            )
        else:
            current_block = None
        base["Round243_known_connectivity_block_id"] = current_block
        post_rows.append(closed({
            "post_frontier_row_id":
                "round243-post-known-block-frontier:"
                + digest([
                    occurrence_id,
                    old_block,
                    current_block,
                    base["incidence_source"],
                    base["known_block_incidence_attachment_credit"],
                ]),
            **base,
        }))
    post_rows.sort(key=lambda row: row["post_frontier_row_id"])
    need(
        len(post_rows) == len({
            row["local_occurrence_row_id"] for row in post_rows
        }) == 53_968,
        "post frontier partition",
    )

    key_metadata = {
        row["official_key_ordinal"]: {
            "official_key_id": row["official_key_id"],
            "official_key_row": row["official_key_row"],
        }
        for row in round241[
            "formal_post_Round241_key_frontier_ledger"
        ]["rows"]
    }
    grouped: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for row in post_rows:
        grouped[row["official_key_ordinal"]].append(row)
    delta_by_key = Counter(
        row["official_key_ordinal"] for row in delta_rows
    )
    key_rows: list[dict[str, Any]] = []
    for ordinal, occurrences in sorted(grouped.items()):
        metadata = key_metadata[ordinal]
        attached = sum(
            row["known_block_incidence_attachment_credit"]
            for row in occurrences
        )
        total = len(occurrences)
        need(
            all(
                row["official_key_id"]
                == metadata["official_key_id"]
                for row in occurrences
            ),
            f"key identity:{ordinal}",
        )
        key_rows.append(closed({
            "key_frontier_row_id":
                "round243-key-frontier:"
                + digest([
                    ordinal,
                    metadata["official_key_id"],
                    attached,
                    total,
                ]),
            "official_key_ordinal": ordinal,
            "official_key_id": metadata["official_key_id"],
            "official_key_row": metadata["official_key_row"],
            "local_occurrence_count": total,
            "occurrences_with_known_block_incidence": attached,
            "occurrences_without_known_block_incidence":
                total - attached,
            "new_Round243_known_block_incidences":
                delta_by_key[ordinal],
            "cumulative_known_block_incidences": attached,
            "maximal_physical_component_assignment_count": 0,
            "global_exact_key_fibre_exhausted": False,
            "global_exact_key_disposition_credit": 0,
        }))
    key_rows.sort(key=lambda row: row["key_frontier_row_id"])

    attached_count = sum(
        row["known_block_incidence_attachment_credit"]
        for row in post_rows
    )
    relation_histogram = Counter(
        row["relation"] for row in source_adjacencies
    )
    component_size_histogram = Counter(
        row["member_Round179_resolved_child_count"]
        for row in component_rows
    )
    seed_block_histogram = Counter(
        row["seed_Round225_known_connectivity_block_count"]
        for row in component_rows
    )
    attached_source_histogram = Counter(
        row["incidence_source"] for row in post_rows
        if row["known_block_incidence_attachment_credit"] == 1
    )
    need(
        len(key_rows) == 116
        and attached_count == 36_180
        and sum(
            row["occurrences_without_known_block_incidence"]
            for row in key_rows
        ) == 17_788,
        "post Round243 incidence census",
    )

    census = {
        "Round220_coordinate_adjacency_count": len(source_adjacencies),
        "Round220_relation_histogram":
            dict(sorted(relation_histogram.items())),
        "exact_10_field_signature_equal_edge_count": len(edge_rows),
        "signature_mismatch_edge_count": 0,
        "Round179_resolved_child_count": len(resolved),
        "resolved_bulk_component_count": len(component_rows),
        "resolved_bulk_component_size_histogram": {
            str(size): count
            for size, count in sorted(component_size_histogram.items())
        },
        "resolved_bulk_component_seed_block_count_histogram": {
            str(count): total
            for count, total in sorted(seed_block_histogram.items())
        },
        "seeded_resolved_bulk_component_count":
            seeded_component_count,
        "Round225_known_connectivity_block_count": 7_404,
        "Round243_known_connectivity_block_count":
            len(new_block_rows),
        "Round243_known_connectivity_block_reduction": 16,
        "Round241_occurrences_with_known_block_incidence": 35_908,
        "Round243_new_occurrence_known_block_incidences":
            len(delta_rows),
        "post_Round243_occurrences_with_known_block_incidence":
            attached_count,
        "post_Round243_occurrences_without_known_block_incidence":
            53_968 - attached_count,
        "observed_exact_key_count": len(key_rows),
        "keys_touched_by_Round243": len(delta_by_key),
        "attached_incidence_source_histogram":
            dict(sorted(attached_source_histogram.items())),
        "maximal_physical_component_assignment_count": 0,
        "global_exact_key_fibre_exhausted_count": 0,
    }

    return {
        "status": (
            "CERTIFIED_10384_EXACT_EVENT_TRACE_BULK_EDGES__"
            "7388_KNOWN_CONNECTIVITY_BLOCKS__"
            "36180_OF_53968_OCCURRENCE_INCIDENCES__"
            "ZERO_COMPONENT_OR_GLOBAL_FIBRE_PROMOTION"
        ),
        "census": census,
        "Round220_adjacency_oracle_binding": {
            "pinned_Round220_certificate_sha256":
                PINS[
                    "cm2_round220_source_g_round179_resolved_child_boundary_atlas_certificate.json"
                ],
            "reconstructed_Round220_adjacency_rows_sha256":
                ROUND220_ADJACENCY_ROWS_SHA256,
            "reconstructed_Round220_adjacency_ids_sha256":
                ROUND220_ADJACENCY_IDS_SHA256,
            "all_10384_rows_reconstructed_from_Round179": True,
        },
        "formal_exact_event_trace_bulk_edge_ledger":
            ledger(edge_rows, "event_trace_bulk_edge_row_id"),
        "formal_resolved_bulk_component_ledger":
            ledger(component_rows, "resolved_bulk_component_row_id"),
        "formal_Round243_known_connectivity_block_ledger":
            ledger(new_block_rows, "known_connectivity_block_id"),
        "formal_Round211_sheet_assignment_ledger":
            ledger(sheet_assignment_rows, "sheet_assignment_row_id"),
        "formal_occurrence_known_block_incidence_delta_ledger":
            ledger(delta_rows, "incidence_delta_row_id"),
        "formal_post_Round243_occurrence_known_block_frontier_ledger":
            ledger(post_rows, "post_frontier_row_id"),
        "formal_post_Round243_key_frontier_ledger":
            ledger(key_rows, "key_frontier_row_id"),
        "scope_contract": {
            "same_parent_and_same_chart_give_explicit_identity_transition": True,
            "both_closed_children_carry_strict_dynamic_signatures": True,
            "all_10_return_signature_fields_equal_on_every_edge": True,
            "positive_area_common_refinement_is_physical_bulk_continuation": True,
            "no_edge_accepted_from_box_touch_or_exact_key_equality_alone": True,
            "known_block_incidence_is_not_component_membership": True,
            "known_connectivity_blocks_are_not_claimed_maximal": True,
        },
        "strict_nonpromotion": {
            "known_block_membership_assignment_credit": 0,
            "physical_component_credit": 0,
            "maximal_physical_component_credit": 0,
            "global_exact_key_fibre_credit": 0,
            "global_exact_key_disposition_credit": 0,
            "Gate5_complete_field_block_count": 0,
            "Gate5_filled_field_slot_count": 10,
            "Gate5_total_field_slot_count": 18,
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "required_next": (
            "extend the exact event-trace identity audit to the 9830 "
            "different-parent coordinate coincidences and to the remaining "
            "Round239 retained wall, crossing-time, source-seam, and "
            "whole-signature strata; then rebuild the quotient again"
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-write", action="store_true")
    arguments = parser.parse_args()
    result = build()
    document = {
        "schema": SCHEMA,
        "result": result,
        "result_sha256": digest(result),
    }
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
