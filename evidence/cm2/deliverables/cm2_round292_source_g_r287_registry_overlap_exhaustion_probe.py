#!/usr/bin/env python3
"""ZERO-CREDIT overlap exhaustion for the conditional Round292 registry.

This probe does not issue occurrence IDs.  It checks the only overlap audit
that was not already frozen by Round288: every one of the 10,020 conditional
Round287 supports against the complete conditional 421,804-row base/atom
registry, and against every other Round287 support.

Round287 supports are represented by exact open coordinate cells:

* a whole Round275 region contributes its exact rechart t-square interval and
  rational p/s intervals;
* a mixed Round286 parent contributes each of its nonempty uncovered rational
  cells with its exact rechart t-square interval.

The representation is an outer description in the active-factor direction.
Therefore absence of a positive overlap is conclusive.  The only permitted
outer overlaps between distinct Round287 supports are the 3,488 frozen
same-regular-graph/opposite-open-side pairs, whose exact physical overlap was
independently proved empty in Round287.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction as Q
import gzip
import hashlib
from itertools import product
import json
from pathlib import Path
from typing import Any, Iterable


HERE = Path(__file__).resolve().parent
PREFIX = "cm2_round292_source_g_r287_registry_overlap_exhaustion_probe"
RESULT = HERE / f"{PREFIX}_result.json"
LEDGER = HERE / f"{PREFIX}_ledger.json.gz"

R174 = "cm2_round174_source_g_unique_first_dynamic_occurrence_materialization_rows.json"
R179 = "cm2_round179_source_g_residual_tube_arrangement_rows.json"
R204 = "cm2_round204_source_g_wall_return_signature_local_replacement_certificate.json"
R208 = "cm2_round208_source_g_outgoing_direct_signature_materialization_certificate.json"
R275 = "cm2_round275_source_g_complete_reverse_rechart_materialization_certificate.json"
R287 = "cm2_round287_source_g_rechart_terminal_occurrence_disposition_probe_ledger.json.gz"
R288 = "cm2_round288_source_g_canonical_atom_occurrence_identity_gate_audit_atom_dispositions.json.gz"

SCHEMA = "cm2.round292.r287-registry-overlap-exhaustion-probe.v1"
LEDGER_SCHEMA = SCHEMA + ".ledger.v1"


def canonical(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    ).encode()


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def need(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def read_json(name: str) -> dict[str, Any]:
    with (HERE / name).open("rb") as handle:
        return json.load(handle)


def read_gzip(name: str) -> dict[str, Any]:
    with gzip.open(HERE / name, "rt", encoding="utf-8") as handle:
        return json.load(handle)


def closed_result(name: str) -> dict[str, Any]:
    document = read_json(name)
    need(
        "result" in document
        and document.get("result_sha256") == digest(document["result"]),
        f"closed result:{name}",
    )
    return document["result"]


def unpack(result: dict[str, Any], table: str) -> list[dict[str, Any]]:
    rows = result[table]
    columns = result["row_column_schemas"][table]
    census = result["table_census_and_sha256"][table]
    need(
        len(rows) == census["row_count"]
        and digest(rows) == census["rows_sha256"],
        f"packed table:{table}",
    )
    return [dict(zip(columns, row, strict=True)) for row in rows]


def signature_from_geometry(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "official_key_id": row["official_key_id"],
        "official_key_ordinal": row["official_key_ordinal"],
        "official_key_row": row["official_key_row"],
        "ordered_integer_wall_events": row["ordered_integer_wall_events"],
        "outgoing_cell": row["outgoing_cell"],
        "roof": row["roof"],
        "signed_wall_word": row["signed_wall_word"],
        "source_chart": row["chart"],
        "target_chart": row["target_chart"],
        "target_lift": row["owner_target"],
    }


def qbox(values: Iterable[str]) -> tuple[Q, ...]:
    result = tuple(map(Q, values))
    need(
        len(result) == 6
        and all(result[2 * axis] < result[2 * axis + 1] for axis in range(3)),
        "positive rational box",
    )
    return result


def verify_closed_row(row: dict[str, Any], label: str) -> None:
    payload = {key: value for key, value in row.items() if key != "row_sha256"}
    need(row["row_sha256"] == digest(payload), f"{label}:row digest")


def verify_ledger(
    document: dict[str, Any], rows_key: str, count_key: str, hash_key: str
) -> list[dict[str, Any]]:
    rows = document[rows_key]
    need(len(rows) == document[count_key], f"{rows_key}:count")
    need(digest(rows) == document[hash_key], f"{rows_key}:digest")
    for row in rows:
        verify_closed_row(row, rows_key)
    return rows


def square_interval(lo: Q, hi: Q) -> tuple[Q, Q]:
    need(lo * hi > 0, "strict signed t interval")
    return (lo * lo, hi * hi) if lo > 0 else (hi * hi, lo * lo)


def rational_box_t_square_for_sign(
    box: tuple[Q, ...], sign: int
) -> tuple[Q, Q] | None:
    lo, hi = box[0], box[1]
    if sign > 0:
        lo = max(lo, Q(0))
        if not lo < hi:
            return None
        return (lo * lo, hi * hi)
    hi = min(hi, Q(0))
    if not lo < hi:
        return None
    return (hi * hi, lo * lo)


def positive_interval_overlap(left: tuple[Q, Q], right: tuple[Q, Q]) -> bool:
    return max(left[0], right[0]) < min(left[1], right[1])


def cell_box_overlap(
    cell: dict[str, Any], rational_box: tuple[Q, ...]
) -> bool:
    other_t2 = rational_box_t_square_for_sign(
        rational_box, cell["physical_t_sign"]
    )
    return (
        other_t2 is not None
        and positive_interval_overlap(cell["physical_t_square"], other_t2)
        and max(cell["p_interval"][0], rational_box[2])
        < min(cell["p_interval"][1], rational_box[3])
        and max(cell["s_interval"][0], rational_box[4])
        < min(cell["s_interval"][1], rational_box[5])
    )


def cell_box_relation(
    cell: dict[str, Any], rational_box: tuple[Q, ...]
) -> str | None:
    other_t2 = rational_box_t_square_for_sign(
        rational_box, cell["physical_t_sign"]
    )
    if (
        other_t2 is None
        or not positive_interval_overlap(cell["physical_t_square"], other_t2)
        or not positive_interval_overlap(
            cell["p_interval"], (rational_box[2], rational_box[3])
        )
        or not positive_interval_overlap(
            cell["s_interval"], (rational_box[4], rational_box[5])
        )
    ):
        return None
    existing_contains_cell = (
        other_t2[0] <= cell["physical_t_square"][0]
        and cell["physical_t_square"][1] <= other_t2[1]
        and rational_box[2] <= cell["p_interval"][0]
        and cell["p_interval"][1] <= rational_box[3]
        and rational_box[4] <= cell["s_interval"][0]
        and cell["s_interval"][1] <= rational_box[5]
    )
    cell_contains_existing = (
        cell["physical_t_square"][0] <= other_t2[0]
        and other_t2[1] <= cell["physical_t_square"][1]
        and cell["p_interval"][0] <= rational_box[2]
        and rational_box[3] <= cell["p_interval"][1]
        and cell["s_interval"][0] <= rational_box[4]
        and rational_box[5] <= cell["s_interval"][1]
    )
    if existing_contains_cell and cell_contains_existing:
        return "EXACT_EQUAL_COORDINATE_REPRESENTATION"
    if existing_contains_cell:
        return "R287_CELL_REPRESENTATION_CONTAINED_IN_EXISTING_OCCURRENCE"
    if cell_contains_existing:
        return "EXISTING_OCCURRENCE_BOX_CONTAINED_IN_R287_CELL_OUTER_REPRESENTATION"
    return "PARTIAL_POSITIVE_VOLUME_OUTER_REPRESENTATION_OVERLAP"


def transformed_cell_box(cell: dict[str, Any]) -> tuple[Q, ...]:
    return (
        cell["physical_t_square"][0],
        cell["physical_t_square"][1],
        cell["p_interval"][0],
        cell["p_interval"][1],
        cell["s_interval"][0],
        cell["s_interval"][1],
    )


def transformed_registry_box(
    rational_box: tuple[Q, ...], sign: int
) -> tuple[Q, ...] | None:
    t_square = rational_box_t_square_for_sign(rational_box, sign)
    if t_square is None:
        return None
    return (
        t_square[0],
        t_square[1],
        rational_box[2],
        rational_box[3],
        rational_box[4],
        rational_box[5],
    )


def intersection_box(
    left: tuple[Q, ...], right: tuple[Q, ...]
) -> tuple[Q, ...] | None:
    result: list[Q] = []
    for axis in range(3):
        lower = max(left[2 * axis], right[2 * axis])
        upper = min(left[2 * axis + 1], right[2 * axis + 1])
        if not lower < upper:
            return None
        result.extend((lower, upper))
    return tuple(result)


def transformed_volume(box: tuple[Q, ...]) -> Q:
    return (
        (box[1] - box[0])
        * (box[3] - box[2])
        * (box[5] - box[4])
    )


def positive_common_face(left: tuple[Q, ...], right: tuple[Q, ...]) -> bool:
    touching_axis_count = 0
    for axis in range(3):
        left_lo, left_hi = left[2 * axis : 2 * axis + 2]
        right_lo, right_hi = right[2 * axis : 2 * axis + 2]
        if left_hi == right_lo or right_hi == left_lo:
            touching_axis_count += 1
            continue
        if not max(left_lo, right_lo) < min(left_hi, right_hi):
            return False
    return touching_axis_count == 1


def cell_cell_overlap(left: dict[str, Any], right: dict[str, Any]) -> bool:
    return (
        left["physical_t_sign"] == right["physical_t_sign"]
        and positive_interval_overlap(
            left["physical_t_square"], right["physical_t_square"]
        )
        and positive_interval_overlap(left["p_interval"], right["p_interval"])
        and positive_interval_overlap(left["s_interval"], right["s_interval"])
    )


class PIntervalNode:
    """Exact p-interval tree used only to form a conservative shortlist."""

    __slots__ = ("center", "cross_lower", "cross_upper", "left", "right")

    @staticmethod
    def interval(row: tuple[tuple[Q, ...], dict[str, Any]]) -> tuple[Q, Q]:
        return row[0][2], row[0][3]

    def __init__(self, rows: list[tuple[tuple[Q, ...], dict[str, Any]]]):
        midpoints = sorted(
            (self.interval(row)[0] + self.interval(row)[1]) / 2
            for row in rows
        )
        self.center = midpoints[len(midpoints) // 2]
        lower_rows = []
        upper_rows = []
        cross = []
        for row in rows:
            lower, upper = self.interval(row)
            if upper <= self.center:
                lower_rows.append(row)
            elif lower >= self.center:
                upper_rows.append(row)
            else:
                cross.append(row)
        if not cross:
            ordered = sorted(
                rows,
                key=lambda row: (
                    self.interval(row),
                    row[1]["occurrence_id"],
                ),
            )
            middle = len(ordered) // 2
            cross = [ordered[middle]]
            lower_rows = ordered[:middle]
            upper_rows = ordered[middle + 1 :]
            lo, hi = self.interval(cross[0])
            self.center = (lo + hi) / 2
        self.cross_lower = sorted(
            cross,
            key=lambda row: (
                self.interval(row)[0],
                row[1]["occurrence_id"],
            ),
        )
        self.cross_upper = sorted(
            cross,
            key=lambda row: (
                self.interval(row)[1],
                row[1]["occurrence_id"],
            ),
            reverse=True,
        )
        self.left = PIntervalNode(lower_rows) if lower_rows else None
        self.right = PIntervalNode(upper_rows) if upper_rows else None

    def query(
        self,
        lower: Q,
        upper: Q,
        output: list[tuple[tuple[Q, ...], dict[str, Any]]],
    ) -> None:
        if upper <= self.center:
            for row in self.cross_lower:
                if self.interval(row)[0] >= upper:
                    break
                output.append(row)
            if self.left is not None:
                self.left.query(lower, upper, output)
        elif lower >= self.center:
            for row in self.cross_upper:
                if self.interval(row)[1] <= lower:
                    break
                output.append(row)
            if self.right is not None:
                self.right.query(lower, upper, output)
        else:
            output.extend(self.cross_lower)
            if self.left is not None:
                self.left.query(lower, upper, output)
            if self.right is not None:
                self.right.query(lower, upper, output)


def closed(payload: dict[str, Any]) -> dict[str, Any]:
    row = dict(payload)
    row["row_sha256"] = digest(payload)
    return row


def load_round275_regions() -> dict[str, dict[str, Any]]:
    wrapper = read_json(R275)
    need(wrapper["result_sha256"] == digest(wrapper["result"]), "R275 result digest")
    result = wrapper["result"]
    rows: list[dict[str, Any]] = []
    for table in ("strict_region_ledger", "arrangement_region_ledger"):
        ledger = result[table]
        need(
            len(ledger["rows"]) == ledger["row_count"]
            and digest(ledger["rows"]) == ledger["rows_sha256"],
            f"R275 {table}",
        )
        rows.extend(ledger["rows"])
    need(len(rows) == 13_788, "R275 region census")
    regions = {row["reverse_rechart_region_row_id"]: row for row in rows}
    need(len(regions) == len(rows), "R275 unique regions")
    return regions


def load_r287_support_cells(
    regions: dict[str, dict[str, Any]],
) -> tuple[
    list[dict[str, Any]],
    set[tuple[str, str]],
    dict[str, dict[str, Any]],
]:
    document = read_gzip(R287)
    need(
        document["schema"]
        == "cm2.round287.source-g-rechart-terminal-occurrence-disposition.ledger.v1",
        "R287 schema",
    )
    region_rows = verify_ledger(
        document, "region_rows", "region_row_count", "region_rows_sha256"
    )
    cell_rows = verify_ledger(
        document,
        "refinement_cell_rows",
        "refinement_cell_row_count",
        "refinement_cell_rows_sha256",
    )
    union_rows = verify_ledger(
        document,
        "potential_new_support_union_rows",
        "potential_new_support_union_row_count",
        "potential_new_support_union_rows_sha256",
    )
    mutually_exclusive = verify_ledger(
        document,
        "mutually_exclusive_outer_overlap_pair_rows",
        "mutually_exclusive_outer_overlap_pair_row_count",
        "mutually_exclusive_outer_overlap_pair_rows_sha256",
    )
    need(
        len(region_rows) == 13_788
        and len(cell_rows) == 7_616
        and len(union_rows) == 10_020
        and len(mutually_exclusive) == 3_488,
        "R287 census",
    )
    region_disposition = {
        row["Round275_region_id"]: row for row in region_rows
    }
    cells = {
        row["Round286_refinement_cell_id"]: row for row in cell_rows
    }
    known_pairs = {
        tuple(sorted((
            row["left_Round275_region_id"],
            row["right_Round275_region_id"],
        )))
        for row in mutually_exclusive
    }
    need(len(known_pairs) == 3_488, "R287 unique mutually-exclusive pairs")

    support_cells: list[dict[str, Any]] = []
    source_kind_histogram: Counter[str] = Counter()
    for union in union_rows:
        verify_closed_row(union, "R287 union")
        union_id = union["Round287_potential_new_support_union_id"]
        region_id = union["Round275_region_id"]
        region = regions[region_id]
        disposition = region_disposition[region_id]
        source_kind = union["source_kind"]
        source_kind_histogram[source_kind] += 1
        if source_kind == "WHOLE_R275_DISJOINT_REGION":
            coordinate = qbox(region["adjacent_rational_region_box"])
            support_cells.append({
                "support_union_id": union_id,
                "Round275_region_id": region_id,
                "cell_id": "WHOLE:" + region_id,
                "source_chart": region["adjacent_chart"],
                "signature_sha256":
                    region["complete_10_field_return_signature_sha256"],
                "physical_t_sign": disposition["physical_t_sign"],
                "physical_t_square":
                    tuple(map(Q, disposition["physical_t_square_open_interval"])),
                "p_interval": (coordinate[2], coordinate[3]),
                "s_interval": (coordinate[4], coordinate[5]),
            })
            continue
        need(
            source_kind == "R286_NONEMPTY_UNCOVERED_PARENT_UNION",
            "known R287 source kind",
        )
        member_ids = union["nonempty_uncovered_member_cell_ids"]
        need(
            len(member_ids) == union["nonempty_uncovered_member_cell_count"] > 0,
            "R287 union members",
        )
        for cell_id in member_ids:
            row = cells[cell_id]
            need(
                row["Round275_region_id"] == region_id
                and row["Round286_coordinate_occupancy_count"] == 0
                and row["signed_region_cell_state"]
                != "EMPTY_OPPOSITE_SIDE_COORDINATE_CELL",
                "R287 physical uncovered member",
            )
            coordinate = qbox(row["coordinate_box"])
            support_cells.append({
                "support_union_id": union_id,
                "Round275_region_id": region_id,
                "cell_id": cell_id,
                "source_chart": row["adjacent_chart"],
                "signature_sha256":
                    row["complete_10_field_return_signature_sha256"],
                "physical_t_sign": row["physical_t_sign"],
                "physical_t_square":
                    tuple(map(Q, row["physical_t_square_open_interval"])),
                "p_interval": (coordinate[2], coordinate[3]),
                "s_interval": (coordinate[4], coordinate[5]),
            })
    need(
        source_kind_histogram
        == {
            "WHOLE_R275_DISJOINT_REGION": 9_128,
            "R286_NONEMPTY_UNCOVERED_PARENT_UNION": 892,
        }
        and len(support_cells) == 10_668,
        "R287 support cell census",
    )
    return support_cells, known_pairs, {
        row["Round287_potential_new_support_union_id"]: row for row in union_rows
    }


def load_preserved_occurrences() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    round174 = closed_result(R174)
    for source in unpack(round174, "resolved_3d_occurrence_rows"):
        signature = signature_from_geometry(source)
        rows.append({
            "occurrence_id": source["row_id"],
            "occurrence_source": "ROUND174_RESOLVED",
            "source_chart": source["chart"],
            "signature_sha256": digest(signature),
            "support_boxes": [qbox(source["box"])],
        })
    round179 = closed_result(R179)
    for source in unpack(round179, "resolved_3d_child_rows"):
        signature = signature_from_geometry(source)
        rows.append({
            "occurrence_id": source["row_id"],
            "occurrence_source": "ROUND179_RESOLVED",
            "source_chart": source["chart"],
            "signature_sha256": digest(signature),
            "support_boxes": [qbox(source["box"])],
        })
    round204 = closed_result(R204)
    ledger204 = round204["formal_local_open_3D_region_ledger"]
    need(
        len(ledger204["rows"]) == ledger204["row_count"]
        and digest(ledger204["rows"]) == ledger204["rows_sha256"],
        "R204 ledger",
    )
    for source in ledger204["rows"]:
        signature = signature_from_geometry(source)
        rows.append({
            "occurrence_id": source["region_row_id"],
            "occurrence_source": "ROUND204_REGION",
            "source_chart": source["chart"],
            "signature_sha256": digest(signature),
            "support_boxes": [qbox(source["leaf_exact_box"])],
        })
    round208 = closed_result(R208)
    ledger208 = round208["formal_local_open_3D_signature_ledger"]
    need(
        len(ledger208["rows"]) == ledger208["row_count"]
        and digest(ledger208["rows"]) == ledger208["rows_sha256"],
        "R208 ledger",
    )
    for source in ledger208["rows"]:
        signature = source["local_return_signature"]
        rows.append({
            "occurrence_id": source["region_row_id"],
            "occurrence_source": "ROUND208_REGION",
            "source_chart": signature["source_chart"],
            "signature_sha256": digest(signature),
            "support_boxes": [qbox(source["Round182_leaf_box"])],
        })
    need(
        Counter(row["occurrence_source"] for row in rows)
        == {
            "ROUND174_RESOLVED": 72_500,
            "ROUND179_RESOLVED": 17_192,
            "ROUND204_REGION": 736,
            "ROUND208_REGION": 36_040,
        }
        and len(rows) == 126_468,
        "preserved occurrence census",
    )
    return rows


def load_new_atoms() -> list[dict[str, Any]]:
    document = read_gzip(R288)
    need(document["row_count"] == 332_016, "R288 atom census")
    need(digest(document["rows"]) == document["rows_sha256"], "R288 rows digest")
    rows: list[dict[str, Any]] = []
    disposition_histogram: Counter[str] = Counter()
    for source in document["rows"]:
        verify_closed_row(source, "R288 atom")
        disposition_histogram[source["occurrence_identity_disposition"]] += 1
        if source["existing_local_occurrence_row_id"] is not None:
            continue
        need(
            source["reserved_candidate_occurrence_id__not_issued"] is not None,
            "R288 reserved new occurrence ID",
        )
        rows.append({
            "occurrence_id":
                source["reserved_candidate_occurrence_id__not_issued"],
            "occurrence_source": "ROUND288_NEW_ATOM_CANDIDATE",
            "source_chart": source["source_chart"],
            "signature_sha256":
                source["complete_10_field_return_signature_sha256"],
            "support_boxes": [
                qbox(box)
                for box in source["frozen_positive_rational_support_envelopes"]
            ],
        })
    need(len(rows) == 295_336, "R288 new atom census")
    return rows


def registry_overlap_audit(
    support_cells: list[dict[str, Any]],
    registry: list[dict[str, Any]],
) -> tuple[
    list[dict[str, Any]],
    dict[str, Any],
    dict[tuple[str, str], list[dict[str, Any]]],
]:
    cells_by_group: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for cell in support_cells:
        cells_by_group[
            (cell["source_chart"], cell["signature_sha256"])
        ].append(cell)

    registry_by_group: dict[
        tuple[str, str], list[tuple[tuple[Q, ...], dict[str, Any]]]
    ] = defaultdict(list)
    for occurrence in registry:
        key = (occurrence["source_chart"], occurrence["signature_sha256"])
        for box in occurrence["support_boxes"]:
            registry_by_group[key].append((box, occurrence))

    registry_trees = {
        key: PIntervalNode(values)
        for key, values in registry_by_group.items()
        if values
    }
    rows: list[dict[str, Any]] = []
    comparisons = 0
    positive_overlap_count = 0
    incident_supports: set[str] = set()
    by_source: Counter[str] = Counter()
    relation_histogram: Counter[str] = Counter()
    targets_by_cell: dict[tuple[str, str], set[str]] = defaultdict(set)
    containing_targets_by_cell: dict[tuple[str, str], set[str]] = defaultdict(set)
    all_cell_keys = {
        (cell["support_union_id"], cell["cell_id"]) for cell in support_cells
    }
    overlaps_by_cell: dict[
        tuple[str, str], list[dict[str, Any]]
    ] = defaultdict(list)
    candidate_group_count = 0
    for key in sorted(cells_by_group):
        cells = cells_by_group[key]
        tree = registry_trees.get(key)
        if tree is not None:
            candidate_group_count += 1
        for cell in cells:
            candidates: list[tuple[tuple[Q, ...], dict[str, Any]]] = []
            if tree is not None:
                tree.query(
                    cell["p_interval"][0],
                    cell["p_interval"][1],
                    candidates,
                )
            for box, occurrence in candidates:
                comparisons += 1
                relation = cell_box_relation(cell, box)
                if relation is None:
                    continue
                positive_overlap_count += 1
                incident_supports.add(cell["support_union_id"])
                by_source[occurrence["occurrence_source"]] += 1
                relation_histogram[relation] += 1
                cell_key = (cell["support_union_id"], cell["cell_id"])
                targets_by_cell[cell_key].add(occurrence["occurrence_id"])
                if relation in {
                    "EXACT_EQUAL_COORDINATE_REPRESENTATION",
                    "R287_CELL_REPRESENTATION_CONTAINED_IN_EXISTING_OCCURRENCE",
                }:
                    containing_targets_by_cell[cell_key].add(
                        occurrence["occurrence_id"]
                    )
                cell_transformed = transformed_cell_box(cell)
                registry_transformed = transformed_registry_box(
                    box, cell["physical_t_sign"]
                )
                need(registry_transformed is not None, "positive signed registry box")
                overlap_box = intersection_box(
                    cell_transformed, registry_transformed
                )
                need(overlap_box is not None, "exact transformed overlap box")
                overlaps_by_cell[cell_key].append({
                    "registry_occurrence_id": occurrence["occurrence_id"],
                    "registry_occurrence_source":
                        occurrence["occurrence_source"],
                    "registry_rational_support_box": box,
                    "registry_transformed_support_box": registry_transformed,
                    "exact_transformed_intersection_box": overlap_box,
                })
                rows.append(closed({
                    "Round292_registry_overlap_row_id":
                        "round292-registry-overlap:" + digest([
                            cell["support_union_id"],
                            cell["cell_id"],
                            occurrence["occurrence_id"],
                            list(map(str, box)),
                        ]),
                    "Round287_potential_new_support_union_id":
                        cell["support_union_id"],
                    "Round287_support_cell_id": cell["cell_id"],
                    "registry_occurrence_id": occurrence["occurrence_id"],
                    "registry_occurrence_source":
                        occurrence["occurrence_source"],
                    "relation": relation,
                    "Round287_exact_transformed_support_cell":
                        list(map(str, cell_transformed)),
                    "registry_exact_rational_support_box":
                        list(map(str, box)),
                    "registry_exact_transformed_support_box":
                        list(map(str, registry_transformed)),
                    "exact_positive_transformed_intersection_box":
                        list(map(str, overlap_box)),
                    "formal_occurrence_credit": 0,
                    "formal_component_credit": 0,
                    "formal_DSU_rank_reduction_credit": 0,
                }))
    rows.sort(key=lambda row: row["Round292_registry_overlap_row_id"])
    cells_by_union: dict[str, set[str]] = defaultdict(set)
    for union_id, cell_id in all_cell_keys:
        cells_by_union[union_id].add(cell_id)
    all_cells_contained_unique_target_union_count = 0
    all_cells_contained_multiple_target_union_count = 0
    overlap_but_not_fully_contained_union_count = 0
    for union_id in incident_supports:
        cell_ids = cells_by_union[union_id]
        containing_union_targets: set[str] = set()
        fully_contained = True
        for cell_id in cell_ids:
            targets = containing_targets_by_cell.get((union_id, cell_id), set())
            if not targets:
                fully_contained = False
            containing_union_targets.update(targets)
        if fully_contained and len(containing_union_targets) == 1:
            all_cells_contained_unique_target_union_count += 1
        elif fully_contained:
            all_cells_contained_multiple_target_union_count += 1
        else:
            overlap_but_not_fully_contained_union_count += 1
    summary = {
        "same_chart_signature_candidate_group_count": candidate_group_count,
        "support_cell_registry_box_comparison_count": comparisons,
        "positive_volume_overlap_count": positive_overlap_count,
        "overlap_incident_support_union_count": len(incident_supports),
        "overlap_histogram_by_registry_source": dict(sorted(by_source.items())),
        "overlap_relation_histogram": dict(sorted(relation_histogram.items())),
        "overlap_incident_support_cell_count": len(targets_by_cell),
        "support_cell_with_containing_existing_occurrence_count":
            len(containing_targets_by_cell),
        "support_cell_with_multiple_containing_targets_count":
            sum(len(targets) > 1 for targets in containing_targets_by_cell.values()),
        "all_cells_contained_in_one_unique_target_support_union_count":
            all_cells_contained_unique_target_union_count,
        "all_cells_contained_but_multiple_target_support_union_count":
            all_cells_contained_multiple_target_union_count,
        "overlap_but_not_fully_contained_support_union_count":
            overlap_but_not_fully_contained_union_count,
    }
    for relations in overlaps_by_cell.values():
        relations.sort(
            key=lambda row: (
                row["registry_occurrence_id"],
                row["registry_rational_support_box"],
            )
        )
    return rows, summary, overlaps_by_cell


def exact_existing_overlap_refinement(
    support_cells: list[dict[str, Any]],
    overlaps_by_cell: dict[tuple[str, str], list[dict[str, Any]]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    """Partition every support in exact (t^2,p,s) coordinates."""

    raw_cells_by_union: dict[str, list[dict[str, Any]]] = defaultdict(list)
    refined_payloads_by_union: dict[str, list[dict[str, Any]]] = defaultdict(list)
    source_volume = Q(0)
    refined_volume = Q(0)
    occupied_volume = Q(0)
    uncovered_volume = Q(0)
    split_source_cell_count = 0

    for source in support_cells:
        union_id = source["support_union_id"]
        raw_cells_by_union[union_id].append(source)
        source_box = transformed_cell_box(source)
        source_volume += transformed_volume(source_box)
        relations = overlaps_by_cell.get((union_id, source["cell_id"]), [])
        cuts: list[list[Q]] = []
        for axis in range(3):
            values = {source_box[2 * axis], source_box[2 * axis + 1]}
            for relation in relations:
                overlap = relation["exact_transformed_intersection_box"]
                values.add(overlap[2 * axis])
                values.add(overlap[2 * axis + 1])
            cuts.append(sorted(values))
        intervals = [list(zip(values, values[1:])) for values in cuts]
        expected_cell_count = (
            len(intervals[0]) * len(intervals[1]) * len(intervals[2])
        )
        split_source_cell_count += int(expected_cell_count > 1)
        local_volume = Q(0)
        for axis_intervals in product(*intervals):
            box = tuple(
                value
                for lower_upper in axis_intervals
                for value in lower_upper
            )
            volume = transformed_volume(box)
            need(volume > 0, "positive exact refinement cell")
            local_volume += volume
            midpoint = tuple(
                (box[2 * axis] + box[2 * axis + 1]) / 2
                for axis in range(3)
            )
            occupancy = sorted({
                relation["registry_occurrence_id"]
                for relation in relations
                if all(
                    relation["registry_transformed_support_box"][2 * axis]
                    < midpoint[axis]
                    < relation["registry_transformed_support_box"][2 * axis + 1]
                    for axis in range(3)
                )
            })
            refinement_id = "round292-r287-existing-refinement-cell:" + digest([
                union_id,
                source["cell_id"],
                list(map(str, box)),
            ])
            payload = {
                "Round292_R287_existing_overlap_refinement_cell_id":
                    refinement_id,
                "Round287_potential_new_support_union_id": union_id,
                "source_Round287_support_cell_id": source["cell_id"],
                "Round275_region_id": source["Round275_region_id"],
                "source_chart": source["source_chart"],
                "complete_10_field_return_signature_sha256":
                    source["signature_sha256"],
                "exact_transformed_coordinate_system": "(t^2,p,s)",
                "exact_transformed_open_cell": list(map(str, box)),
                "exact_transformed_cell_volume": str(volume),
                "existing_occurrence_occupancy_count": len(occupancy),
                "existing_occurrence_ids": occupancy,
                "disposition": (
                    "EXACT_EXISTING_OCCURRENCE_REPRESENTATION_SUBCOVER__"
                    "NO_NEW_OCCURRENCE_ID"
                    if occupancy
                    else
                    "EXACT_UNCOVERED_POSITIVE_OPEN_SLICE__"
                    "PENDING_PARENT_LOCAL_CONNECTIVITY"
                ),
                "Round292_refined_new_support_component_id": None,
                "formal_new_occurrence_credit": 0,
                "formal_representation_alias_binding_credit": 0,
                "formal_component_credit": 0,
                "formal_DSU_rank_reduction_credit": 0,
            }
            refined_payloads_by_union[union_id].append({
                "payload": payload,
                "box": box,
                "occupancy": occupancy,
            })
            refined_volume += volume
            if occupancy:
                occupied_volume += volume
            else:
                uncovered_volume += volume
        need(local_volume == transformed_volume(source_box), "cell volume conservation")

    need(source_volume == refined_volume, "global transformed volume conservation")
    refinement_rows: list[dict[str, Any]] = []
    component_rows: list[dict[str, Any]] = []
    local_connectivity_rank = 0
    uncovered_component_count = 0
    fully_covered_union_count = 0
    partially_covered_union_count = 0
    untouched_union_count = 0
    multi_target_occupied_cell_count = 0
    occupied_cell_count = 0
    uncovered_cell_count = 0
    component_size_histogram: Counter[int] = Counter()

    for union_id in sorted(refined_payloads_by_union):
        records = refined_payloads_by_union[union_id]
        occupied = [record for record in records if record["occupancy"]]
        uncovered = [record for record in records if not record["occupancy"]]
        occupied_cell_count += len(occupied)
        uncovered_cell_count += len(uncovered)
        multi_target_occupied_cell_count += sum(
            len(record["occupancy"]) > 1 for record in occupied
        )
        if occupied and uncovered:
            partially_covered_union_count += 1
        elif occupied:
            fully_covered_union_count += 1
        else:
            untouched_union_count += 1

        parent = list(range(len(uncovered)))

        def find(index: int) -> int:
            while parent[index] != index:
                parent[index] = parent[parent[index]]
                index = parent[index]
            return index

        for left_index, left in enumerate(uncovered):
            for right_index in range(left_index):
                right = uncovered[right_index]
                if not positive_common_face(left["box"], right["box"]):
                    continue
                left_root, right_root = find(left_index), find(right_index)
                if left_root != right_root:
                    parent[right_root] = left_root
                    local_connectivity_rank += 1

        members_by_root: dict[int, list[dict[str, Any]]] = defaultdict(list)
        for index, record in enumerate(uncovered):
            members_by_root[find(index)].append(record)
        for members in members_by_root.values():
            member_ids = sorted(
                record["payload"][
                    "Round292_R287_existing_overlap_refinement_cell_id"
                ]
                for record in members
            )
            component_id = "round292-r287-refined-new-support:" + digest([
                "ROUND287_EXISTING_OVERLAP_REFINED_NEW_SUPPORT_V1",
                union_id,
                member_ids,
            ])
            for record in members:
                record["payload"][
                    "Round292_refined_new_support_component_id"
                ] = component_id
                record["payload"]["disposition"] = (
                    "EXACT_UNCOVERED_POSITIVE_OPEN_SLICE__"
                    "MEMBER_OF_REFINED_PARENT_LOCAL_NEW_SUPPORT"
                )
            component_rows.append(closed({
                "Round292_refined_new_support_component_id": component_id,
                "source_Round287_potential_new_support_union_id": union_id,
                "member_refinement_cell_count": len(member_ids),
                "member_refinement_cell_ids": member_ids,
                "one_connected_positive_open_support": True,
                "strictly_disjoint_from_complete_conditional_base_atom_registry":
                    True,
                "formal_new_occurrence_credit": 0,
                "formal_component_credit": 0,
                "formal_DSU_rank_reduction_credit": 0,
            }))
            uncovered_component_count += 1
            component_size_histogram[len(member_ids)] += 1

        for record in records:
            refinement_rows.append(closed(record["payload"]))

    refinement_rows.sort(
        key=lambda row: row[
            "Round292_R287_existing_overlap_refinement_cell_id"
        ]
    )
    component_rows.sort(
        key=lambda row: row["Round292_refined_new_support_component_id"]
    )
    need(
        uncovered_component_count
        == len(component_rows)
        and local_connectivity_rank
        == uncovered_cell_count - uncovered_component_count,
        "refined local connectivity rank conservation",
    )
    summary = {
        "source_Round287_support_cell_count": len(support_cells),
        "source_cell_split_by_existing_boundaries_count": split_source_cell_count,
        "exact_refinement_cell_count": len(refinement_rows),
        "occupied_representation_subcover_cell_count": occupied_cell_count,
        "multi_target_occupied_representation_subcover_cell_count":
            multi_target_occupied_cell_count,
        "uncovered_refinement_cell_count": uncovered_cell_count,
        "fully_existing_covered_source_union_count": fully_covered_union_count,
        "partially_existing_covered_source_union_count":
            partially_covered_union_count,
        "untouched_source_union_count": untouched_union_count,
        "refined_strictly_new_support_component_count":
            uncovered_component_count,
        "refined_local_support_connectivity_rank": local_connectivity_rank,
        "refined_new_support_component_size_histogram":
            {str(key): value for key, value in sorted(component_size_histogram.items())},
        "source_transformed_volume": str(source_volume),
        "occupied_transformed_volume": str(occupied_volume),
        "uncovered_transformed_volume": str(uncovered_volume),
        "refined_transformed_volume": str(refined_volume),
        "exact_transformed_volume_conservation": (
            source_volume == occupied_volume + uncovered_volume == refined_volume
        ),
    }
    return refinement_rows, component_rows, summary


def pairwise_support_audit(
    support_cells: list[dict[str, Any]],
    known_pairs: set[tuple[str, str]],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    groups: dict[tuple[str, str, int], list[dict[str, Any]]] = defaultdict(list)
    for cell in support_cells:
        groups[(
            cell["source_chart"],
            cell["signature_sha256"],
            cell["physical_t_sign"],
        )].append(cell)

    rows: list[dict[str, Any]] = []
    comparisons = 0
    same_union_overlap = 0
    permitted_mutually_exclusive = 0
    unresolved = 0
    seen_pairs: set[tuple[str, str]] = set()
    for key in sorted(groups):
        cells = sorted(
            groups[key],
            key=lambda cell: (
                cell["physical_t_square"][0],
                cell["p_interval"][0],
                cell["s_interval"][0],
                cell["cell_id"],
            ),
        )
        for left_index, left in enumerate(cells):
            for right in cells[left_index + 1 :]:
                if right["physical_t_square"][0] >= left["physical_t_square"][1]:
                    break
                comparisons += 1
                if not cell_cell_overlap(left, right):
                    continue
                if left["support_union_id"] == right["support_union_id"]:
                    same_union_overlap += 1
                    relation = "SAME_UNION_MEMBER_CELL_POSITIVE_OVERLAP__FORBIDDEN"
                else:
                    region_pair = tuple(sorted((
                        left["Round275_region_id"],
                        right["Round275_region_id"],
                    )))
                    support_pair = tuple(sorted((
                        left["support_union_id"],
                        right["support_union_id"],
                    )))
                    if region_pair in known_pairs:
                        permitted_mutually_exclusive += 1
                        seen_pairs.add(region_pair)
                        relation = (
                            "OUTER_OVERLAP_ONLY__FROZEN_SAME_REGULAR_GRAPH_"
                            "OPPOSITE_OPEN_SIDES__EXACT_PHYSICAL_OVERLAP_EMPTY"
                        )
                    else:
                        unresolved += 1
                        relation = "DISTINCT_SUPPORT_POSITIVE_OVERLAP__UNRESOLVED"
                rows.append(closed({
                    "Round292_support_pair_audit_row_id":
                        "round292-support-pair:" + digest([
                            left["support_union_id"],
                            left["cell_id"],
                            right["support_union_id"],
                            right["cell_id"],
                        ]),
                    "left_support_union_id": left["support_union_id"],
                    "left_support_cell_id": left["cell_id"],
                    "right_support_union_id": right["support_union_id"],
                    "right_support_cell_id": right["cell_id"],
                    "relation": relation,
                    "formal_occurrence_identity_collapse_credit": 0,
                    "formal_component_edge_credit": 0,
                }))
    rows.sort(key=lambda row: row["Round292_support_pair_audit_row_id"])
    summary = {
        "same_chart_signature_sign_shortlist_comparison_count": comparisons,
        "same_union_positive_overlap_count": same_union_overlap,
        "permitted_mutually_exclusive_cell_pair_count":
            permitted_mutually_exclusive,
        "distinct_unresolved_positive_overlap_count": unresolved,
        "seen_frozen_mutually_exclusive_region_pair_count": len(seen_pairs),
    }
    return rows, summary


def deterministic_gzip_bytes(value: Any) -> bytes:
    buffer = gzip.compress(canonical(value) + b"\n", compresslevel=9, mtime=0)
    return buffer


def build() -> tuple[dict[str, Any], dict[str, Any]]:
    input_files = [
        R174, R179, R204, R208, R275, R287, R288
    ]
    pins = {name: file_sha256(HERE / name) for name in input_files}
    regions = load_round275_regions()
    support_cells, known_pairs, unions = load_r287_support_cells(regions)
    preserved = load_preserved_occurrences()
    new_atoms = load_new_atoms()
    registry = preserved + new_atoms
    need(len(registry) == 421_804, "conditional base/atom registry census")
    need(
        len({row["occurrence_id"] for row in registry}) == len(registry),
        "conditional registry occurrence IDs injective",
    )

    overlap_rows, overlap_summary, overlaps_by_cell = registry_overlap_audit(
        support_cells, registry
    )
    refinement_rows, component_rows, refinement_summary = (
        exact_existing_overlap_refinement(
            support_cells, overlaps_by_cell
        )
    )
    pair_rows, pair_summary = pairwise_support_audit(
        support_cells, known_pairs
    )
    all_rows = overlap_rows + refinement_rows + component_rows + pair_rows
    row_id_fields = (
        "Round292_registry_overlap_row_id",
        "Round292_R287_existing_overlap_refinement_cell_id",
        "Round292_refined_new_support_component_id",
        "Round292_support_pair_audit_row_id",
    )
    all_rows.sort(
        key=lambda row: next(
            (row[field] for field in row_id_fields if field in row),
            "",
        )
    )
    ledger = {
        "schema": LEDGER_SCHEMA,
        "row_count": len(all_rows),
        "rows_sha256": digest(all_rows),
        "rows": all_rows,
    }
    unresolved = (
        pair_summary["same_union_positive_overlap_count"]
        + pair_summary["distinct_unresolved_positive_overlap_count"]
    )
    result = {
        "schema": SCHEMA,
        "status":
            "PASS_ZERO_CREDIT__R287_FULL_REGISTRY_OVERLAP_EXHAUSTED"
            if unresolved == 0
            else "FAIL_CLOSED__UNRESOLVED_OVERLAP",
        "input_file_pins": pins,
        "census": {
            "preserved_occurrence_count": len(preserved),
            "new_atom_candidate_count": len(new_atoms),
            "conditional_base_atom_registry_count": len(registry),
            "Round287_support_union_count": len(unions),
            "Round287_exact_support_cell_count": len(support_cells),
            "frozen_mutually_exclusive_region_pair_count": len(known_pairs),
            **overlap_summary,
            **refinement_summary,
            **pair_summary,
            "remaining_unresolved_overlap_count": unresolved,
        },
        "strict_nonpromotion": {
            "formal_new_occurrence_credit": 0,
            "representation_alias_binding_credit": 0,
            "occurrence_identity_collapse_credit": 0,
            "component_union_credit": 0,
            "seam_edge_credit": 0,
            "DSU_rank_reduction_credit": 0,
            "Jx_Jy_same_point_glue_credit": 0,
            "expanded_occurrences": 126_468,
            "quotient_components": 63_224,
            "Gate5": "10/18",
            "D02": "BLOCKED",
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "ledger": {
            "filename": LEDGER.name,
            "row_count": len(all_rows),
            "rows_sha256": ledger["rows_sha256"],
        },
        "result_sha256": "",
    }
    payload = {key: value for key, value in result.items() if key != "result_sha256"}
    result["result_sha256"] = digest(payload)
    return result, ledger


def main() -> None:
    result, ledger = build()
    LEDGER.write_bytes(deterministic_gzip_bytes(ledger))
    RESULT.write_bytes(canonical(result) + b"\n")
    print(result["status"])
    print(json.dumps(result["census"], sort_keys=True))
    print(f"result_sha256={result['result_sha256']}")
    print(f"ledger_file_sha256={file_sha256(LEDGER)}")


if __name__ == "__main__":
    main()
