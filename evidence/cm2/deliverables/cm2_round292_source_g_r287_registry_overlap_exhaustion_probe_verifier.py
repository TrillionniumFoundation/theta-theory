#!/usr/bin/env python3
"""Standalone cacheless verifier for the Round292 R287 overlap exhaustion.

The Round292 probe producer is pinned and treated only as inert bytes.  It is
never imported or executed.  This verifier independently reconstructs the
421,804-row conditional base/atom registry, the 10,020 Round287 support
unions and their 10,668 source cells, every registry overlap, the exact
(t^2,p,s) refinement, the 9,404 surviving support components, and the
pairwise unresolved-overlap census.  Only after that reconstruction is
complete are the candidate result and ledger opened.

This is a ZERO-CREDIT verifier.  It does not issue occurrence identities,
bind aliases, add component or seam edges, reduce DSU rank, prove
maximality/fibres/global dispositions, or recognize Jx/Jy as same-point glue.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from copy import deepcopy
from fractions import Fraction as Q
import gzip
import hashlib
from itertools import product
import json
import os
from pathlib import Path
import tempfile
from typing import Any, Iterable


HERE = Path(__file__).resolve().parent
PREFIX = "cm2_round292_source_g_r287_registry_overlap_exhaustion_probe"
PRODUCER = HERE / f"{PREFIX}.py"
RESULT = HERE / f"{PREFIX}_result.json"
LEDGER = HERE / f"{PREFIX}_ledger.json.gz"
OUTPUT = HERE / f"{PREFIX}_verification.json"

SCHEMA = "cm2.round292.r287-registry-overlap-exhaustion-probe.v1"
LEDGER_SCHEMA = SCHEMA + ".ledger.v1"
VERIFICATION_SCHEMA = SCHEMA + ".verification.v1"

R174 = "cm2_round174_source_g_unique_first_dynamic_occurrence_materialization_rows.json"
R179 = "cm2_round179_source_g_residual_tube_arrangement_rows.json"
R204 = "cm2_round204_source_g_wall_return_signature_local_replacement_certificate.json"
R208 = "cm2_round208_source_g_outgoing_direct_signature_materialization_certificate.json"
R275 = "cm2_round275_source_g_complete_reverse_rechart_materialization_certificate.json"
R287 = "cm2_round287_source_g_rechart_terminal_occurrence_disposition_probe_ledger.json.gz"
R288 = "cm2_round288_source_g_canonical_atom_occurrence_identity_gate_audit_atom_dispositions.json.gz"

UPSTREAM_PINS = {
    R174: "9edeea2e1033b0dd70dee11a53b0f6aeb21fe74030aeefb60b081a7c420cff54",
    R179: "f20b42c1fed781779b537b4d45bf44233eae1ed3ee620b95177a80f0eb2b5e42",
    R204: "e7e1c49bebcb8c01f0fb4b33af66e4f2a8de560f121cae65f4971b2fec3e1818",
    R208: "4d01fb9cee639ec59786c078f7a20b3bbcd5c18ea674fabbfce64e250e765938",
    R275: "e18935169614fc8b62ead3be7f60b383396ea1d2c52e8151457241f49e770386",
    R287: "29838e3e6b33f03bf623bbce8b87e6ba5c3306e66beb0b6634496503fb9a4f9a",
    R288: "6b0a8aa1cd38019322a61f5aaefc936006d10769cd21a5c8df374576f9ac570a",
}

CANDIDATE_PINS = {
    PRODUCER.name:
        "69078405b39dff3e924630ffbc9fbe35c14e4114e1e33c946b9ab44fe26e8c4c",
    RESULT.name:
        "f3887e75f4ef62459b75d8c77eee4781ec14f57651b4feb09b8d7ca8e372c508",
    LEDGER.name:
        "8863126e88ffd30438938d0a8bdb577f5928ae81f3f17f4b506829d59103a8ab",
}

EXPECTED_NONPROMOTION = {
    "CM2": "NO-GO_FOR_CLAIM",
    "D02": "BLOCKED",
    "DSU_rank_reduction_credit": 0,
    "Gate5": "10/18",
    "Jx_Jy_same_point_glue_credit": 0,
    "component_union_credit": 0,
    "expanded_occurrences": 126_468,
    "formal_new_occurrence_credit": 0,
    "occurrence_identity_collapse_credit": 0,
    "quotient_components": 63_224,
    "representation_alias_binding_credit": 0,
    "seam_edge_credit": 0,
}


class VerificationError(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


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


def read_json_path(path: Path) -> dict[str, Any]:
    with path.open("rb") as handle:
        value = json.load(handle)
    need(isinstance(value, dict), f"JSON object:{path.name}")
    return value


def read_json(name: str) -> dict[str, Any]:
    return read_json_path(HERE / name)


def read_gzip(name: str) -> dict[str, Any]:
    with gzip.open(HERE / name, "rt", encoding="utf-8") as handle:
        value = json.load(handle)
    need(isinstance(value, dict), f"gzip JSON object:{name}")
    return value


def read_gzip_bytes(payload: bytes) -> dict[str, Any]:
    value = json.loads(gzip.decompress(payload))
    need(isinstance(value, dict), "candidate gzip JSON object")
    return value


def deterministic_gzip_bytes(value: Any) -> bytes:
    return gzip.compress(canonical(value) + b"\n", compresslevel=9, mtime=0)


def atomic_write(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(
        prefix="." + path.name + ".", dir=path.parent
    )
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def closed_result(name: str) -> dict[str, Any]:
    wrapper = read_json(name)
    need(
        set(wrapper) >= {"result", "result_sha256"}
        and wrapper["result_sha256"] == digest(wrapper["result"]),
        f"closed upstream result:{name}",
    )
    return wrapper["result"]


def unpack(result: dict[str, Any], table: str) -> list[dict[str, Any]]:
    packed = result[table]
    columns = result["row_column_schemas"][table]
    census = result["table_census_and_sha256"][table]
    need(
        len(packed) == census["row_count"]
        and digest(packed) == census["rows_sha256"],
        f"packed upstream table:{table}",
    )
    return [dict(zip(columns, row, strict=True)) for row in packed]


def verify_closed_row(row: dict[str, Any], label: str) -> None:
    payload = {key: value for key, value in row.items() if key != "row_sha256"}
    need(set(row) == set(payload) | {"row_sha256"}, f"{label}:row fields")
    need(row["row_sha256"] == digest(payload), f"{label}:row digest")


def verify_table(
    document: dict[str, Any], rows_key: str, count_key: str, hash_key: str
) -> list[dict[str, Any]]:
    rows = document[rows_key]
    need(
        isinstance(rows, list)
        and len(rows) == document[count_key]
        and digest(rows) == document[hash_key],
        f"closed upstream table:{rows_key}",
    )
    for row in rows:
        verify_closed_row(row, rows_key)
    return rows


def qbox(values: Iterable[str]) -> tuple[Q, ...]:
    result = tuple(map(Q, values))
    need(
        len(result) == 6
        and all(result[2 * axis] < result[2 * axis + 1] for axis in range(3)),
        "strict rational box",
    )
    return result


def close(payload: dict[str, Any]) -> dict[str, Any]:
    row = dict(payload)
    row["row_sha256"] = digest(payload)
    return row


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


def square_interval(lo: Q, hi: Q) -> tuple[Q, Q]:
    need(lo * hi > 0, "strict signed t interval")
    return (lo * lo, hi * hi) if lo > 0 else (hi * hi, lo * lo)


def signed_t_square(box: tuple[Q, ...], sign: int) -> tuple[Q, Q] | None:
    lo, hi = box[0], box[1]
    if sign > 0:
        lo = max(lo, Q(0))
        return (lo * lo, hi * hi) if lo < hi else None
    hi = min(hi, Q(0))
    return (hi * hi, lo * lo) if lo < hi else None


def interval_overlap(left: tuple[Q, Q], right: tuple[Q, Q]) -> bool:
    return max(left[0], right[0]) < min(left[1], right[1])


def transformed_cell(cell: dict[str, Any]) -> tuple[Q, ...]:
    return (
        *cell["physical_t_square"],
        *cell["p_interval"],
        *cell["s_interval"],
    )


def transformed_registry(
    box: tuple[Q, ...], sign: int
) -> tuple[Q, ...] | None:
    t2 = signed_t_square(box, sign)
    return None if t2 is None else (*t2, box[2], box[3], box[4], box[5])


def intersect(left: tuple[Q, ...], right: tuple[Q, ...]) -> tuple[Q, ...] | None:
    result: list[Q] = []
    for axis in range(3):
        lo = max(left[2 * axis], right[2 * axis])
        hi = min(left[2 * axis + 1], right[2 * axis + 1])
        if not lo < hi:
            return None
        result.extend((lo, hi))
    return tuple(result)


def volume(box: tuple[Q, ...]) -> Q:
    return (
        (box[1] - box[0])
        * (box[3] - box[2])
        * (box[5] - box[4])
    )


def positive_common_face(left: tuple[Q, ...], right: tuple[Q, ...]) -> bool:
    touching = 0
    for axis in range(3):
        l0, l1 = left[2 * axis : 2 * axis + 2]
        r0, r1 = right[2 * axis : 2 * axis + 2]
        if l1 == r0 or r1 == l0:
            touching += 1
        elif not max(l0, r0) < min(l1, r1):
            return False
    return touching == 1


def cell_cell_overlap(left: dict[str, Any], right: dict[str, Any]) -> bool:
    return (
        left["physical_t_sign"] == right["physical_t_sign"]
        and interval_overlap(left["physical_t_square"], right["physical_t_square"])
        and interval_overlap(left["p_interval"], right["p_interval"])
        and interval_overlap(left["s_interval"], right["s_interval"])
    )


def cell_box_relation(
    cell: dict[str, Any], box: tuple[Q, ...]
) -> tuple[str, tuple[Q, ...], tuple[Q, ...]] | None:
    registry = transformed_registry(box, cell["physical_t_sign"])
    if registry is None:
        return None
    source = transformed_cell(cell)
    overlap = intersect(source, registry)
    if overlap is None:
        return None
    existing_contains = all(
        registry[2 * axis] <= source[2 * axis]
        and source[2 * axis + 1] <= registry[2 * axis + 1]
        for axis in range(3)
    )
    source_contains = all(
        source[2 * axis] <= registry[2 * axis]
        and registry[2 * axis + 1] <= source[2 * axis + 1]
        for axis in range(3)
    )
    if existing_contains and source_contains:
        relation = "EXACT_EQUAL_COORDINATE_REPRESENTATION"
    elif existing_contains:
        relation = "R287_CELL_REPRESENTATION_CONTAINED_IN_EXISTING_OCCURRENCE"
    elif source_contains:
        relation = (
            "EXISTING_OCCURRENCE_BOX_CONTAINED_IN_R287_CELL_OUTER_REPRESENTATION"
        )
    else:
        relation = "PARTIAL_POSITIVE_VOLUME_OUTER_REPRESENTATION_OVERLAP"
    return relation, registry, overlap


class IntervalIndex:
    """Exact p-interval index; shortlist counts are part of the frozen audit."""

    __slots__ = ("center", "cross_lo", "cross_hi", "left", "right")

    @staticmethod
    def interval(row: tuple[tuple[Q, ...], dict[str, Any]]) -> tuple[Q, Q]:
        return row[0][2], row[0][3]

    def __init__(self, rows: list[tuple[tuple[Q, ...], dict[str, Any]]]):
        mids = sorted(
            (self.interval(row)[0] + self.interval(row)[1]) / 2 for row in rows
        )
        self.center = mids[len(mids) // 2]
        lower, upper, cross = [], [], []
        for row in rows:
            lo, hi = self.interval(row)
            if hi <= self.center:
                lower.append(row)
            elif lo >= self.center:
                upper.append(row)
            else:
                cross.append(row)
        if not cross:
            ordered = sorted(
                rows, key=lambda row: (self.interval(row), row[1]["occurrence_id"])
            )
            middle = len(ordered) // 2
            cross = [ordered[middle]]
            lower, upper = ordered[:middle], ordered[middle + 1 :]
            lo, hi = self.interval(cross[0])
            self.center = (lo + hi) / 2
        self.cross_lo = sorted(
            cross, key=lambda row: (self.interval(row)[0], row[1]["occurrence_id"])
        )
        self.cross_hi = sorted(
            cross,
            key=lambda row: (self.interval(row)[1], row[1]["occurrence_id"]),
            reverse=True,
        )
        self.left = IntervalIndex(lower) if lower else None
        self.right = IntervalIndex(upper) if upper else None

    def query(
        self,
        lo: Q,
        hi: Q,
        output: list[tuple[tuple[Q, ...], dict[str, Any]]],
    ) -> None:
        if hi <= self.center:
            for row in self.cross_lo:
                if self.interval(row)[0] >= hi:
                    break
                output.append(row)
            if self.left is not None:
                self.left.query(lo, hi, output)
        elif lo >= self.center:
            for row in self.cross_hi:
                if self.interval(row)[1] <= lo:
                    break
                output.append(row)
            if self.right is not None:
                self.right.query(lo, hi, output)
        else:
            output.extend(self.cross_lo)
            if self.left is not None:
                self.left.query(lo, hi, output)
            if self.right is not None:
                self.right.query(lo, hi, output)


def rebuild_round275_regions() -> dict[str, dict[str, Any]]:
    wrapper = read_json(R275)
    need(
        wrapper.get("result_sha256") == digest(wrapper.get("result")),
        "R275 result closure",
    )
    rows: list[dict[str, Any]] = []
    for table_name in ("strict_region_ledger", "arrangement_region_ledger"):
        table = wrapper["result"][table_name]
        need(
            len(table["rows"]) == table["row_count"]
            and digest(table["rows"]) == table["rows_sha256"],
            f"R275 table closure:{table_name}",
        )
        rows.extend(table["rows"])
    need(len(rows) == 13_788, "R275 region census")
    result = {row["reverse_rechart_region_row_id"]: row for row in rows}
    need(len(result) == len(rows), "R275 unique region IDs")
    return result


def rebuild_round287_support_cells(
    regions: dict[str, dict[str, Any]],
) -> tuple[
    list[dict[str, Any]],
    set[tuple[str, str]],
    dict[str, dict[str, Any]],
]:
    document = read_gzip(R287)
    need(
        document.get("schema")
        == "cm2.round287.source-g-rechart-terminal-occurrence-disposition.ledger.v1",
        "R287 schema",
    )
    region_rows = verify_table(
        document, "region_rows", "region_row_count", "region_rows_sha256"
    )
    refinement_rows = verify_table(
        document,
        "refinement_cell_rows",
        "refinement_cell_row_count",
        "refinement_cell_rows_sha256",
    )
    union_rows = verify_table(
        document,
        "potential_new_support_union_rows",
        "potential_new_support_union_row_count",
        "potential_new_support_union_rows_sha256",
    )
    exclusion_rows = verify_table(
        document,
        "mutually_exclusive_outer_overlap_pair_rows",
        "mutually_exclusive_outer_overlap_pair_row_count",
        "mutually_exclusive_outer_overlap_pair_rows_sha256",
    )
    need(
        (len(region_rows), len(refinement_rows), len(union_rows), len(exclusion_rows))
        == (13_788, 7_616, 10_020, 3_488),
        "R287 table censuses",
    )
    dispositions = {row["Round275_region_id"]: row for row in region_rows}
    refinements = {
        row["Round286_refinement_cell_id"]: row for row in refinement_rows
    }
    exclusions = {
        tuple(
            sorted(
                (
                    row["left_Round275_region_id"],
                    row["right_Round275_region_id"],
                )
            )
        )
        for row in exclusion_rows
    }
    need(len(exclusions) == 3_488, "R287 exclusion uniqueness")

    cells: list[dict[str, Any]] = []
    source_histogram: Counter[str] = Counter()
    for union in union_rows:
        union_id = union["Round287_potential_new_support_union_id"]
        region_id = union["Round275_region_id"]
        region = regions[region_id]
        disposition = dispositions[region_id]
        source_kind = union["source_kind"]
        source_histogram[source_kind] += 1
        if source_kind == "WHOLE_R275_DISJOINT_REGION":
            coordinate = qbox(region["adjacent_rational_region_box"])
            cells.append(
                {
                    "support_union_id": union_id,
                    "Round275_region_id": region_id,
                    "cell_id": "WHOLE:" + region_id,
                    "source_chart": region["adjacent_chart"],
                    "signature_sha256":
                        region["complete_10_field_return_signature_sha256"],
                    "physical_t_sign": disposition["physical_t_sign"],
                    "physical_t_square": tuple(
                        map(Q, disposition["physical_t_square_open_interval"])
                    ),
                    "p_interval": (coordinate[2], coordinate[3]),
                    "s_interval": (coordinate[4], coordinate[5]),
                }
            )
            continue
        need(
            source_kind == "R286_NONEMPTY_UNCOVERED_PARENT_UNION",
            "R287 known source kind",
        )
        member_ids = union["nonempty_uncovered_member_cell_ids"]
        need(
            len(member_ids) == union["nonempty_uncovered_member_cell_count"] > 0,
            "R287 mixed union member census",
        )
        for cell_id in member_ids:
            source = refinements[cell_id]
            need(
                source["Round275_region_id"] == region_id
                and source["Round286_coordinate_occupancy_count"] == 0
                and source["signed_region_cell_state"]
                != "EMPTY_OPPOSITE_SIDE_COORDINATE_CELL",
                "R287 physical uncovered refinement member",
            )
            coordinate = qbox(source["coordinate_box"])
            cells.append(
                {
                    "support_union_id": union_id,
                    "Round275_region_id": region_id,
                    "cell_id": cell_id,
                    "source_chart": source["adjacent_chart"],
                    "signature_sha256":
                        source["complete_10_field_return_signature_sha256"],
                    "physical_t_sign": source["physical_t_sign"],
                    "physical_t_square": tuple(
                        map(Q, source["physical_t_square_open_interval"])
                    ),
                    "p_interval": (coordinate[2], coordinate[3]),
                    "s_interval": (coordinate[4], coordinate[5]),
                }
            )
    need(
        source_histogram
        == {
            "WHOLE_R275_DISJOINT_REGION": 9_128,
            "R286_NONEMPTY_UNCOVERED_PARENT_UNION": 892,
        }
        and len(cells) == 10_668,
        "R287 reconstructed support-cell census",
    )
    union_map = {
        row["Round287_potential_new_support_union_id"]: row for row in union_rows
    }
    need(len(union_map) == 10_020, "R287 unique union IDs")
    return cells, exclusions, union_map


def rebuild_preserved_occurrences() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    result174 = closed_result(R174)
    for source in unpack(result174, "resolved_3d_occurrence_rows"):
        rows.append(
            {
                "occurrence_id": source["row_id"],
                "occurrence_source": "ROUND174_RESOLVED",
                "source_chart": source["chart"],
                "signature_sha256": digest(signature_from_geometry(source)),
                "support_boxes": [qbox(source["box"])],
            }
        )
    result179 = closed_result(R179)
    for source in unpack(result179, "resolved_3d_child_rows"):
        rows.append(
            {
                "occurrence_id": source["row_id"],
                "occurrence_source": "ROUND179_RESOLVED",
                "source_chart": source["chart"],
                "signature_sha256": digest(signature_from_geometry(source)),
                "support_boxes": [qbox(source["box"])],
            }
        )
    result204 = closed_result(R204)
    ledger204 = result204["formal_local_open_3D_region_ledger"]
    need(
        len(ledger204["rows"]) == ledger204["row_count"]
        and digest(ledger204["rows"]) == ledger204["rows_sha256"],
        "R204 occurrence ledger closure",
    )
    for source in ledger204["rows"]:
        rows.append(
            {
                "occurrence_id": source["region_row_id"],
                "occurrence_source": "ROUND204_REGION",
                "source_chart": source["chart"],
                "signature_sha256": digest(signature_from_geometry(source)),
                "support_boxes": [qbox(source["leaf_exact_box"])],
            }
        )
    result208 = closed_result(R208)
    ledger208 = result208["formal_local_open_3D_signature_ledger"]
    need(
        len(ledger208["rows"]) == ledger208["row_count"]
        and digest(ledger208["rows"]) == ledger208["rows_sha256"],
        "R208 occurrence ledger closure",
    )
    for source in ledger208["rows"]:
        signature = source["local_return_signature"]
        rows.append(
            {
                "occurrence_id": source["region_row_id"],
                "occurrence_source": "ROUND208_REGION",
                "source_chart": signature["source_chart"],
                "signature_sha256": digest(signature),
                "support_boxes": [qbox(source["Round182_leaf_box"])],
            }
        )
    need(
        Counter(row["occurrence_source"] for row in rows)
        == {
            "ROUND174_RESOLVED": 72_500,
            "ROUND179_RESOLVED": 17_192,
            "ROUND204_REGION": 736,
            "ROUND208_REGION": 36_040,
        }
        and len(rows) == 126_468,
        "preserved occurrence reconstruction",
    )
    return rows


def rebuild_new_atom_candidates() -> list[dict[str, Any]]:
    document = read_gzip(R288)
    need(
        document.get("row_count") == 332_016
        and digest(document.get("rows")) == document.get("rows_sha256"),
        "R288 atom table closure",
    )
    result: list[dict[str, Any]] = []
    histogram: Counter[str] = Counter()
    for source in document["rows"]:
        verify_closed_row(source, "R288 atom")
        histogram[source["occurrence_identity_disposition"]] += 1
        if source["existing_local_occurrence_row_id"] is not None:
            continue
        occurrence_id = source["reserved_candidate_occurrence_id__not_issued"]
        need(occurrence_id is not None, "R288 reserved occurrence candidate ID")
        result.append(
            {
                "occurrence_id": occurrence_id,
                "occurrence_source": "ROUND288_NEW_ATOM_CANDIDATE",
                "source_chart": source["source_chart"],
                "signature_sha256":
                    source["complete_10_field_return_signature_sha256"],
                "support_boxes": [
                    qbox(box)
                    for box in source["frozen_positive_rational_support_envelopes"]
                ],
            }
        )
    need(
        len(result) == 295_336
        and histogram
        == {
            "EXISTING_ROUND208_OCCURRENCE_ID_PRESERVED": 36_040,
            "EXACT_ALIAS_OF_EXISTING_ROUND204_OCCURRENCE": 640,
            "NEW_DISJOINT_PROMOTION_READY_CANDIDATE__ROUND279_STRICT_INWARD_CORRIDOR_INNER_SUPPORT__PENDING_INDEPENDENT_ROUND288_VERIFIER":
                274_176,
            "NEW_DISJOINT_CANDIDATE__POSITIVE_VOLUME_RATIONAL_INNER_SUPPORT_NOT_MATERIALIZED":
                21_160,
        },
        "R288 atom disposition census",
    )
    return result


def independently_rebuild_registry_overlaps(
    support_cells: list[dict[str, Any]],
    registry: list[dict[str, Any]],
) -> tuple[
    list[dict[str, Any]],
    dict[str, Any],
    dict[tuple[str, str], list[dict[str, Any]]],
]:
    cells_by_group: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for cell in support_cells:
        cells_by_group[(cell["source_chart"], cell["signature_sha256"])].append(
            cell
        )
    boxes_by_group: dict[
        tuple[str, str], list[tuple[tuple[Q, ...], dict[str, Any]]]
    ] = defaultdict(list)
    for occurrence in registry:
        key = (occurrence["source_chart"], occurrence["signature_sha256"])
        for box in occurrence["support_boxes"]:
            boxes_by_group[key].append((box, occurrence))
    indexes = {
        key: IntervalIndex(values) for key, values in boxes_by_group.items() if values
    }

    rows: list[dict[str, Any]] = []
    overlaps_by_cell: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    targets_by_cell: dict[tuple[str, str], set[str]] = defaultdict(set)
    containing_by_cell: dict[tuple[str, str], set[str]] = defaultdict(set)
    cells_by_union: dict[str, set[str]] = defaultdict(set)
    comparisons = 0
    positive_count = 0
    incident_unions: set[str] = set()
    by_source: Counter[str] = Counter()
    by_relation: Counter[str] = Counter()
    group_count = 0

    for key in sorted(cells_by_group):
        index = indexes.get(key)
        if index is not None:
            group_count += 1
        for cell in cells_by_group[key]:
            cell_key = (cell["support_union_id"], cell["cell_id"])
            cells_by_union[cell["support_union_id"]].add(cell["cell_id"])
            shortlist: list[tuple[tuple[Q, ...], dict[str, Any]]] = []
            if index is not None:
                index.query(cell["p_interval"][0], cell["p_interval"][1], shortlist)
            for box, occurrence in shortlist:
                comparisons += 1
                relation_data = cell_box_relation(cell, box)
                if relation_data is None:
                    continue
                relation, registry_transformed, overlap = relation_data
                positive_count += 1
                incident_unions.add(cell["support_union_id"])
                by_source[occurrence["occurrence_source"]] += 1
                by_relation[relation] += 1
                targets_by_cell[cell_key].add(occurrence["occurrence_id"])
                if relation in {
                    "EXACT_EQUAL_COORDINATE_REPRESENTATION",
                    "R287_CELL_REPRESENTATION_CONTAINED_IN_EXISTING_OCCURRENCE",
                }:
                    containing_by_cell[cell_key].add(occurrence["occurrence_id"])
                overlap_record = {
                    "registry_occurrence_id": occurrence["occurrence_id"],
                    "registry_occurrence_source": occurrence["occurrence_source"],
                    "registry_rational_support_box": box,
                    "registry_transformed_support_box": registry_transformed,
                    "exact_transformed_intersection_box": overlap,
                }
                overlaps_by_cell[cell_key].append(overlap_record)
                source_transformed = transformed_cell(cell)
                rows.append(
                    close(
                        {
                            "Round292_registry_overlap_row_id":
                                "round292-registry-overlap:"
                                + digest(
                                    [
                                        cell["support_union_id"],
                                        cell["cell_id"],
                                        occurrence["occurrence_id"],
                                        list(map(str, box)),
                                    ]
                                ),
                            "Round287_potential_new_support_union_id":
                                cell["support_union_id"],
                            "Round287_support_cell_id": cell["cell_id"],
                            "registry_occurrence_id": occurrence["occurrence_id"],
                            "registry_occurrence_source":
                                occurrence["occurrence_source"],
                            "relation": relation,
                            "Round287_exact_transformed_support_cell":
                                list(map(str, source_transformed)),
                            "registry_exact_rational_support_box":
                                list(map(str, box)),
                            "registry_exact_transformed_support_box":
                                list(map(str, registry_transformed)),
                            "exact_positive_transformed_intersection_box":
                                list(map(str, overlap)),
                            "formal_occurrence_credit": 0,
                            "formal_component_credit": 0,
                            "formal_DSU_rank_reduction_credit": 0,
                        }
                    )
                )

    rows.sort(key=lambda row: row["Round292_registry_overlap_row_id"])
    unique_target_unions = 0
    multiple_target_unions = 0
    incomplete_unions = 0
    for union_id in incident_unions:
        union_targets: set[str] = set()
        fully_contained = True
        for cell_id in cells_by_union[union_id]:
            targets = containing_by_cell.get((union_id, cell_id), set())
            if not targets:
                fully_contained = False
            union_targets.update(targets)
        if fully_contained and len(union_targets) == 1:
            unique_target_unions += 1
        elif fully_contained:
            multiple_target_unions += 1
        else:
            incomplete_unions += 1
    for relations in overlaps_by_cell.values():
        relations.sort(
            key=lambda row: (
                row["registry_occurrence_id"],
                row["registry_rational_support_box"],
            )
        )
    summary = {
        "same_chart_signature_candidate_group_count": group_count,
        "support_cell_registry_box_comparison_count": comparisons,
        "positive_volume_overlap_count": positive_count,
        "overlap_incident_support_union_count": len(incident_unions),
        "overlap_histogram_by_registry_source": dict(sorted(by_source.items())),
        "overlap_relation_histogram": dict(sorted(by_relation.items())),
        "overlap_incident_support_cell_count": len(targets_by_cell),
        "support_cell_with_containing_existing_occurrence_count":
            len(containing_by_cell),
        "support_cell_with_multiple_containing_targets_count":
            sum(len(values) > 1 for values in containing_by_cell.values()),
        "all_cells_contained_in_one_unique_target_support_union_count":
            unique_target_unions,
        "all_cells_contained_but_multiple_target_support_union_count":
            multiple_target_unions,
        "overlap_but_not_fully_contained_support_union_count": incomplete_unions,
    }
    need(
        len(rows) == positive_count
        and positive_count == 1_564
        and len(incident_unions) == 920,
        "independent registry-overlap census",
    )
    return rows, summary, overlaps_by_cell


def independently_refine_existing_overlaps(
    support_cells: list[dict[str, Any]],
    overlaps_by_cell: dict[tuple[str, str], list[dict[str, Any]]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    records_by_union: dict[str, list[dict[str, Any]]] = defaultdict(list)
    source_volume = Q(0)
    refined_volume = Q(0)
    occupied_volume = Q(0)
    uncovered_volume = Q(0)
    split_source_cells = 0

    for source in support_cells:
        union_id = source["support_union_id"]
        source_box = transformed_cell(source)
        source_volume += volume(source_box)
        relations = overlaps_by_cell.get((union_id, source["cell_id"]), [])
        cut_sets: list[list[Q]] = []
        for axis in range(3):
            values = {source_box[2 * axis], source_box[2 * axis + 1]}
            for relation in relations:
                overlap = relation["exact_transformed_intersection_box"]
                values.update((overlap[2 * axis], overlap[2 * axis + 1]))
            cut_sets.append(sorted(values))
        intervals = [list(zip(values, values[1:])) for values in cut_sets]
        expected_count = len(intervals[0]) * len(intervals[1]) * len(intervals[2])
        split_source_cells += int(expected_count > 1)
        local_volume = Q(0)
        for choice in product(*intervals):
            box = tuple(bound for interval in choice for bound in interval)
            cell_volume = volume(box)
            need(cell_volume > 0, "positive exact refinement volume")
            local_volume += cell_volume
            midpoint = tuple(
                (box[2 * axis] + box[2 * axis + 1]) / 2 for axis in range(3)
            )
            occupancy = sorted(
                {
                    relation["registry_occurrence_id"]
                    for relation in relations
                    if all(
                        relation["registry_transformed_support_box"][2 * axis]
                        < midpoint[axis]
                        < relation["registry_transformed_support_box"][
                            2 * axis + 1
                        ]
                        for axis in range(3)
                    )
                }
            )
            refinement_id = (
                "round292-r287-existing-refinement-cell:"
                + digest([union_id, source["cell_id"], list(map(str, box))])
            )
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
                "exact_transformed_cell_volume": str(cell_volume),
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
            records_by_union[union_id].append(
                {"payload": payload, "box": box, "occupancy": occupancy}
            )
            refined_volume += cell_volume
            if occupancy:
                occupied_volume += cell_volume
            else:
                uncovered_volume += cell_volume
        need(local_volume == volume(source_box), "per-source exact volume conservation")
    need(source_volume == refined_volume, "global exact volume conservation")

    refinement_rows: list[dict[str, Any]] = []
    component_rows: list[dict[str, Any]] = []
    connectivity_rank = 0
    fully_covered = partially_covered = untouched = 0
    occupied_count = uncovered_count = multi_target_count = 0
    size_histogram: Counter[int] = Counter()

    for union_id in sorted(records_by_union):
        records = records_by_union[union_id]
        occupied = [record for record in records if record["occupancy"]]
        uncovered = [record for record in records if not record["occupancy"]]
        occupied_count += len(occupied)
        uncovered_count += len(uncovered)
        multi_target_count += sum(len(record["occupancy"]) > 1 for record in occupied)
        if occupied and uncovered:
            partially_covered += 1
        elif occupied:
            fully_covered += 1
        else:
            untouched += 1

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
                root_left, root_right = find(left_index), find(right_index)
                if root_left != root_right:
                    parent[root_right] = root_left
                    connectivity_rank += 1

        by_root: dict[int, list[dict[str, Any]]] = defaultdict(list)
        for index, record in enumerate(uncovered):
            by_root[find(index)].append(record)
        for members in by_root.values():
            member_ids = sorted(
                record["payload"][
                    "Round292_R287_existing_overlap_refinement_cell_id"
                ]
                for record in members
            )
            component_id = (
                "round292-r287-refined-new-support:"
                + digest(
                    [
                        "ROUND287_EXISTING_OVERLAP_REFINED_NEW_SUPPORT_V1",
                        union_id,
                        member_ids,
                    ]
                )
            )
            for record in members:
                record["payload"]["Round292_refined_new_support_component_id"] = (
                    component_id
                )
                record["payload"]["disposition"] = (
                    "EXACT_UNCOVERED_POSITIVE_OPEN_SLICE__"
                    "MEMBER_OF_REFINED_PARENT_LOCAL_NEW_SUPPORT"
                )
            component_rows.append(
                close(
                    {
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
                    }
                )
            )
            size_histogram[len(member_ids)] += 1

        refinement_rows.extend(close(record["payload"]) for record in records)

    refinement_rows.sort(
        key=lambda row: row["Round292_R287_existing_overlap_refinement_cell_id"]
    )
    component_rows.sort(
        key=lambda row: row["Round292_refined_new_support_component_id"]
    )
    need(
        len(refinement_rows) == 11_852
        and occupied_count == 1_600
        and uncovered_count == 10_252
        and len(component_rows) == 9_404
        and connectivity_rank == 848 == uncovered_count - len(component_rows),
        "independent exact refinement census and rank",
    )
    summary = {
        "source_Round287_support_cell_count": len(support_cells),
        "source_cell_split_by_existing_boundaries_count": split_source_cells,
        "exact_refinement_cell_count": len(refinement_rows),
        "occupied_representation_subcover_cell_count": occupied_count,
        "multi_target_occupied_representation_subcover_cell_count":
            multi_target_count,
        "uncovered_refinement_cell_count": uncovered_count,
        "fully_existing_covered_source_union_count": fully_covered,
        "partially_existing_covered_source_union_count": partially_covered,
        "untouched_source_union_count": untouched,
        "refined_strictly_new_support_component_count": len(component_rows),
        "refined_local_support_connectivity_rank": connectivity_rank,
        "refined_new_support_component_size_histogram": {
            str(key): value for key, value in sorted(size_histogram.items())
        },
        "source_transformed_volume": str(source_volume),
        "occupied_transformed_volume": str(occupied_volume),
        "uncovered_transformed_volume": str(uncovered_volume),
        "refined_transformed_volume": str(refined_volume),
        "exact_transformed_volume_conservation":
            source_volume == occupied_volume + uncovered_volume == refined_volume,
    }
    need(
        (fully_covered, partially_covered, untouched) == (616, 304, 9_100),
        "independent union disposition census",
    )
    return refinement_rows, component_rows, summary


def independently_audit_support_pairs(
    support_cells: list[dict[str, Any]],
    known_exclusions: set[tuple[str, str]],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    groups: dict[tuple[str, str, int], list[dict[str, Any]]] = defaultdict(list)
    for cell in support_cells:
        groups[
            (
                cell["source_chart"],
                cell["signature_sha256"],
                cell["physical_t_sign"],
            )
        ].append(cell)
    rows: list[dict[str, Any]] = []
    comparisons = 0
    same_union = 0
    permitted = 0
    unresolved = 0
    seen_exclusions: set[tuple[str, str]] = set()
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
                    same_union += 1
                    relation = "SAME_UNION_MEMBER_CELL_POSITIVE_OVERLAP__FORBIDDEN"
                else:
                    region_pair = tuple(
                        sorted(
                            (
                                left["Round275_region_id"],
                                right["Round275_region_id"],
                            )
                        )
                    )
                    if region_pair in known_exclusions:
                        permitted += 1
                        seen_exclusions.add(region_pair)
                        relation = (
                            "OUTER_OVERLAP_ONLY__FROZEN_SAME_REGULAR_GRAPH_"
                            "OPPOSITE_OPEN_SIDES__EXACT_PHYSICAL_OVERLAP_EMPTY"
                        )
                    else:
                        unresolved += 1
                        relation = "DISTINCT_SUPPORT_POSITIVE_OVERLAP__UNRESOLVED"
                rows.append(
                    close(
                        {
                            "Round292_support_pair_audit_row_id":
                                "round292-support-pair:"
                                + digest(
                                    [
                                        left["support_union_id"],
                                        left["cell_id"],
                                        right["support_union_id"],
                                        right["cell_id"],
                                    ]
                                ),
                            "left_support_union_id": left["support_union_id"],
                            "left_support_cell_id": left["cell_id"],
                            "right_support_union_id": right["support_union_id"],
                            "right_support_cell_id": right["cell_id"],
                            "relation": relation,
                            "formal_occurrence_identity_collapse_credit": 0,
                            "formal_component_edge_credit": 0,
                        }
                    )
                )
    rows.sort(key=lambda row: row["Round292_support_pair_audit_row_id"])
    summary = {
        "same_chart_signature_sign_shortlist_comparison_count": comparisons,
        "same_union_positive_overlap_count": same_union,
        "permitted_mutually_exclusive_cell_pair_count": permitted,
        "distinct_unresolved_positive_overlap_count": unresolved,
        "seen_frozen_mutually_exclusive_region_pair_count": len(seen_exclusions),
    }
    need(
        comparisons == 231_880
        and same_union == permitted == unresolved == 0
        and not rows,
        "independent pairwise support audit",
    )
    return rows, summary


ROW_ID_FIELDS = (
    "Round292_registry_overlap_row_id",
    "Round292_R287_existing_overlap_refinement_cell_id",
    "Round292_refined_new_support_component_id",
    "Round292_support_pair_audit_row_id",
)


def ledger_row_id(row: dict[str, Any]) -> str:
    # Refinement-member rows also carry their resolved component ID.  Their
    # primary row identity is the first field in this frozen precedence list.
    values = [row[field] for field in ROW_ID_FIELDS if field in row]
    need(values, "at least one Round292 ledger row ID")
    return values[0]


def reconstruct_expected() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    pins = {name: file_sha256(HERE / name) for name in UPSTREAM_PINS}
    need(pins == UPSTREAM_PINS, "upstream byte pins")
    regions = rebuild_round275_regions()
    support_cells, known_exclusions, union_map = (
        rebuild_round287_support_cells(regions)
    )
    preserved = rebuild_preserved_occurrences()
    new_atoms = rebuild_new_atom_candidates()
    registry = preserved + new_atoms
    need(
        len(registry) == 421_804
        and len({row["occurrence_id"] for row in registry}) == 421_804,
        "conditional registry census and ID injectivity",
    )
    overlap_rows, overlap_summary, overlaps_by_cell = (
        independently_rebuild_registry_overlaps(support_cells, registry)
    )
    refinement_rows, component_rows, refinement_summary = (
        independently_refine_existing_overlaps(support_cells, overlaps_by_cell)
    )
    pair_rows, pair_summary = independently_audit_support_pairs(
        support_cells, known_exclusions
    )
    rows = overlap_rows + refinement_rows + component_rows + pair_rows
    rows.sort(key=ledger_row_id)
    need(
        len(rows) == 22_820
        and len({ledger_row_id(row) for row in rows}) == len(rows),
        "expected ledger row census and uniqueness",
    )
    expected_ledger = {
        "schema": LEDGER_SCHEMA,
        "row_count": len(rows),
        "rows_sha256": digest(rows),
        "rows": rows,
    }
    unresolved = (
        pair_summary["same_union_positive_overlap_count"]
        + pair_summary["distinct_unresolved_positive_overlap_count"]
    )
    census = {
        "preserved_occurrence_count": len(preserved),
        "new_atom_candidate_count": len(new_atoms),
        "conditional_base_atom_registry_count": len(registry),
        "Round287_support_union_count": len(union_map),
        "Round287_exact_support_cell_count": len(support_cells),
        "frozen_mutually_exclusive_region_pair_count": len(known_exclusions),
        **overlap_summary,
        **refinement_summary,
        **pair_summary,
        "remaining_unresolved_overlap_count": unresolved,
    }
    expected_result = {
        "schema": SCHEMA,
        "status": (
            "PASS_ZERO_CREDIT__R287_FULL_REGISTRY_OVERLAP_EXHAUSTED"
            if unresolved == 0
            else "FAIL_CLOSED__UNRESOLVED_OVERLAP"
        ),
        "input_file_pins": pins,
        "census": census,
        "strict_nonpromotion": EXPECTED_NONPROMOTION,
        "ledger": {
            "filename": LEDGER.name,
            "row_count": len(rows),
            "rows_sha256": expected_ledger["rows_sha256"],
        },
        "result_sha256": "",
    }
    expected_result["result_sha256"] = digest(
        {
            key: value
            for key, value in expected_result.items()
            if key != "result_sha256"
        }
    )
    expected_gzip = deterministic_gzip_bytes(expected_ledger)
    need(
        expected_ledger["rows_sha256"]
        == "556bd0ed95709fe43ff7837522d8729582ce0e7c9679879a57365f864f6ba055"
        and hashlib.sha256(expected_gzip).hexdigest() == CANDIDATE_PINS[LEDGER.name]
        and expected_result["result_sha256"]
        == "f6bc26c2a7f674901e411342ce388b5c2a9e8facc9a253ce244375bcf7e47372",
        "independent frozen commitments",
    )
    metadata = {
        "registry_occurrence_count": len(registry),
        "support_union_count": len(union_map),
        "source_support_cell_count": len(support_cells),
        "overlap_row_count": len(overlap_rows),
        "refinement_row_count": len(refinement_rows),
        "refined_component_row_count": len(component_rows),
        "pair_audit_row_count": len(pair_rows),
        "census": census,
    }
    return expected_result, expected_ledger, metadata


def audit_candidate_after_expected(
    expected_result: dict[str, Any],
    expected_ledger: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any], bytes]:
    # This is deliberately the first read/hash/parse of either candidate
    # result or candidate ledger in the verification path.
    result_bytes = RESULT.read_bytes()
    ledger_bytes = LEDGER.read_bytes()
    need(
        hashlib.sha256(result_bytes).hexdigest() == CANDIDATE_PINS[RESULT.name],
        "candidate result byte pin",
    )
    need(
        hashlib.sha256(ledger_bytes).hexdigest() == CANDIDATE_PINS[LEDGER.name],
        "candidate ledger byte pin",
    )
    candidate_result = json.loads(result_bytes)
    candidate_ledger = read_gzip_bytes(ledger_bytes)
    need(
        candidate_result == expected_result,
        "candidate result exact independent equality",
    )
    need(
        candidate_ledger == expected_ledger,
        "candidate ledger exact independent equality",
    )
    need(
        ledger_bytes == deterministic_gzip_bytes(expected_ledger),
        "candidate deterministic gzip exact equality",
    )
    for row in candidate_ledger["rows"]:
        verify_closed_row(row, "candidate Round292 overlap ledger")
        need(
            all(
                row.get(field, 0) == 0
                for field in (
                    "formal_occurrence_credit",
                    "formal_new_occurrence_credit",
                    "formal_representation_alias_binding_credit",
                    "formal_component_credit",
                    "formal_DSU_rank_reduction_credit",
                    "formal_occurrence_identity_collapse_credit",
                    "formal_component_edge_credit",
                )
            ),
            "candidate row zero-credit",
        )
    return candidate_result, candidate_ledger, ledger_bytes


def reclose_row(row: dict[str, Any]) -> dict[str, Any]:
    payload = {key: value for key, value in row.items() if key != "row_sha256"}
    payload["row_sha256"] = digest(payload)
    return payload


def reclose_ledger(ledger: dict[str, Any]) -> None:
    ledger["row_count"] = len(ledger["rows"])
    ledger["rows_sha256"] = digest(ledger["rows"])


def reclose_result(result: dict[str, Any]) -> None:
    result.pop("result_sha256", None)
    result["result_sha256"] = digest(result)


def accept_ledger(
    candidate: dict[str, Any], expected: dict[str, Any]
) -> None:
    need(candidate.get("schema") == LEDGER_SCHEMA, "attacked ledger schema")
    need(
        candidate.get("row_count") == len(candidate.get("rows", [])),
        "attacked ledger count closure",
    )
    need(
        candidate.get("rows_sha256") == digest(candidate.get("rows")),
        "attacked ledger rows closure",
    )
    for row in candidate["rows"]:
        verify_closed_row(row, "attacked ledger row")
    need(candidate == expected, "attacked ledger differs from independent expected")


def accept_result(
    candidate: dict[str, Any], expected: dict[str, Any]
) -> None:
    payload = {key: value for key, value in candidate.items() if key != "result_sha256"}
    need(
        candidate.get("result_sha256") == digest(payload),
        "attacked result self closure",
    )
    need(candidate == expected, "attacked result differs from independent expected")


def run_resigned_attacks(
    expected_result: dict[str, Any],
    expected_ledger: dict[str, Any],
) -> dict[str, Any]:
    rejected: list[str] = []
    overlap_index = next(
        index
        for index, row in enumerate(expected_ledger["rows"])
        if "Round292_registry_overlap_row_id" in row
    )
    refinement_index = next(
        index
        for index, row in enumerate(expected_ledger["rows"])
        if "Round292_R287_existing_overlap_refinement_cell_id" in row
    )
    component_index = next(
        index
        for index, row in enumerate(expected_ledger["rows"])
        if "Round292_refined_new_support_component_id" in row
        and "Round292_R287_existing_overlap_refinement_cell_id" not in row
    )

    row_attacks: list[tuple[str, int, Any]] = [
        (
            "OVERLAP_RELATION_RESIGNED",
            overlap_index,
            lambda row: row.__setitem__(
                "relation", "EXACT_EQUAL_COORDINATE_REPRESENTATION"
            ),
        ),
        (
            "OVERLAP_TARGET_ID_RESIGNED",
            overlap_index,
            lambda row: row.__setitem__("registry_occurrence_id", "forged-occurrence"),
        ),
        (
            "OVERLAP_INTERSECTION_BOX_RESIGNED",
            overlap_index,
            lambda row: row["exact_positive_transformed_intersection_box"].__setitem__(
                0, "0"
            ),
        ),
        (
            "OVERLAP_OCCURRENCE_CREDIT_RESIGNED",
            overlap_index,
            lambda row: row.__setitem__("formal_occurrence_credit", 1),
        ),
        (
            "REFINEMENT_OCCUPANCY_RESIGNED",
            refinement_index,
            lambda row: row.__setitem__(
                "existing_occurrence_occupancy_count",
                row["existing_occurrence_occupancy_count"] + 1,
            ),
        ),
        (
            "REFINEMENT_DISPOSITION_RESIGNED",
            refinement_index,
            lambda row: row.__setitem__("disposition", "FORGED_DISPOSITION"),
        ),
        (
            "REFINEMENT_COMPONENT_ID_RESIGNED",
            refinement_index,
            lambda row: row.__setitem__(
                "Round292_refined_new_support_component_id", "forged-component"
            ),
        ),
        (
            "REFINEMENT_VOLUME_RESIGNED",
            refinement_index,
            lambda row: row.__setitem__("exact_transformed_cell_volume", "1"),
        ),
        (
            "REFINEMENT_NEW_OCCURRENCE_CREDIT_RESIGNED",
            refinement_index,
            lambda row: row.__setitem__("formal_new_occurrence_credit", 1),
        ),
        (
            "COMPONENT_MEMBER_COUNT_RESIGNED",
            component_index,
            lambda row: row.__setitem__(
                "member_refinement_cell_count",
                row["member_refinement_cell_count"] + 1,
            ),
        ),
        (
            "COMPONENT_DISJOINTNESS_RESIGNED",
            component_index,
            lambda row: row.__setitem__(
                "strictly_disjoint_from_complete_conditional_base_atom_registry",
                False,
            ),
        ),
        (
            "COMPONENT_DSU_CREDIT_RESIGNED",
            component_index,
            lambda row: row.__setitem__("formal_DSU_rank_reduction_credit", 1),
        ),
    ]
    for attack_id, row_index, mutate in row_attacks:
        attacked = deepcopy(expected_ledger)
        row = deepcopy(attacked["rows"][row_index])
        mutate(row)
        attacked["rows"][row_index] = reclose_row(row)
        reclose_ledger(attacked)
        try:
            accept_ledger(attacked, expected_ledger)
        except VerificationError:
            rejected.append(attack_id)
        else:
            raise VerificationError(f"resigned row attack accepted:{attack_id}")

    ledger_attacks: list[tuple[str, Any]] = [
        (
            "LEDGER_SCHEMA_FORGE_RECOMMITTED",
            lambda ledger: ledger.__setitem__("schema", LEDGER_SCHEMA + ".forged"),
        ),
        (
            "LEDGER_ROW_DELETE_RECOMMITTED",
            lambda ledger: ledger["rows"].pop(),
        ),
        (
            "LEDGER_ROW_DUPLICATE_RECOMMITTED",
            lambda ledger: ledger["rows"].append(deepcopy(ledger["rows"][0])),
        ),
        (
            "LEDGER_ROW_REORDER_RECOMMITTED",
            lambda ledger: ledger["rows"].reverse(),
        ),
        (
            "LEDGER_ROW_ID_SWAP_RECOMMITTED",
            lambda ledger: ledger["rows"].__setitem__(
                0,
                reclose_row(
                    {
                        **ledger["rows"][0],
                        ledger_row_id(ledger["rows"][0]):
                            ledger_row_id(ledger["rows"][1]),
                    }
                ),
            ),
        ),
    ]
    for attack_id, mutate in ledger_attacks:
        attacked = deepcopy(expected_ledger)
        mutate(attacked)
        reclose_ledger(attacked)
        try:
            accept_ledger(attacked, expected_ledger)
        except VerificationError:
            rejected.append(attack_id)
        else:
            raise VerificationError(f"recommitted ledger attack accepted:{attack_id}")

    result_attacks: list[tuple[str, Any]] = [
        (
            "RESULT_STATUS_RECLOSED",
            lambda result: result.__setitem__("status", "PASS_FORGED"),
        ),
        (
            "RESULT_REGISTRY_CENSUS_RECLOSED",
            lambda result: result["census"].__setitem__(
                "conditional_base_atom_registry_count", 421_803
            ),
        ),
        (
            "RESULT_OVERLAP_CENSUS_RECLOSED",
            lambda result: result["census"].__setitem__(
                "positive_volume_overlap_count", 1_563
            ),
        ),
        (
            "RESULT_REFINEMENT_CENSUS_RECLOSED",
            lambda result: result["census"].__setitem__(
                "exact_refinement_cell_count", 11_851
            ),
        ),
        (
            "RESULT_NEW_SUPPORT_CENSUS_RECLOSED",
            lambda result: result["census"].__setitem__(
                "refined_strictly_new_support_component_count", 9_405
            ),
        ),
        (
            "RESULT_UNRESOLVED_OVERLAP_RECLOSED",
            lambda result: result["census"].__setitem__(
                "remaining_unresolved_overlap_count", 1
            ),
        ),
        (
            "RESULT_FORMAL_OCCURRENCE_CREDIT_RECLOSED",
            lambda result: result["strict_nonpromotion"].__setitem__(
                "formal_new_occurrence_credit", 9_404
            ),
        ),
        (
            "RESULT_DSU_RANK_CREDIT_RECLOSED",
            lambda result: result["strict_nonpromotion"].__setitem__(
                "DSU_rank_reduction_credit", 848
            ),
        ),
        (
            "RESULT_QUOTIENT_FORGE_RECLOSED",
            lambda result: result["strict_nonpromotion"].__setitem__(
                "quotient_components", 63_223
            ),
        ),
        (
            "RESULT_JXJY_GLUE_FORGE_RECLOSED",
            lambda result: result["strict_nonpromotion"].__setitem__(
                "Jx_Jy_same_point_glue_credit", 1
            ),
        ),
        (
            "RESULT_LEDGER_DIGEST_RECLOSED",
            lambda result: result["ledger"].__setitem__("rows_sha256", "0" * 64),
        ),
        (
            "RESULT_UPSTREAM_PIN_RECLOSED",
            lambda result: result["input_file_pins"].__setitem__(R287, "0" * 64),
        ),
    ]
    for attack_id, mutate in result_attacks:
        attacked = deepcopy(expected_result)
        mutate(attacked)
        reclose_result(attacked)
        try:
            accept_result(attacked, expected_result)
        except VerificationError:
            rejected.append(attack_id)
        else:
            raise VerificationError(f"reclosed result attack accepted:{attack_id}")

    # Coordinated row -> ledger -> result attack, with every public object
    # commitment recomputed.  Equality to the independently reconstructed
    # inert candidate must still reject it.
    attacked_ledger = deepcopy(expected_ledger)
    row = deepcopy(attacked_ledger["rows"][refinement_index])
    row["formal_representation_alias_binding_credit"] = 1
    attacked_ledger["rows"][refinement_index] = reclose_row(row)
    reclose_ledger(attacked_ledger)
    attacked_result = deepcopy(expected_result)
    attacked_result["ledger"]["rows_sha256"] = attacked_ledger["rows_sha256"]
    attacked_result["strict_nonpromotion"][
        "representation_alias_binding_credit"
    ] = 1
    reclose_result(attacked_result)
    try:
        accept_ledger(attacked_ledger, expected_ledger)
        accept_result(attacked_result, expected_result)
    except VerificationError:
        rejected.append("COORDINATED_ROW_LEDGER_RESULT_RESIGN")
    else:
        raise VerificationError("coordinated full-chain attack accepted")

    # Same decoded object, deliberately noncanonical gzip header.
    import io

    buffer = io.BytesIO()
    with gzip.GzipFile(
        filename="forged-ledger.json",
        mode="wb",
        fileobj=buffer,
        compresslevel=9,
        mtime=1,
    ) as handle:
        handle.write(canonical(expected_ledger) + b"\n")
    forged_gzip = buffer.getvalue()
    need(
        read_gzip_bytes(forged_gzip) == expected_ledger
        and forged_gzip != deterministic_gzip_bytes(expected_ledger),
        "effective alternate gzip header attack",
    )
    try:
        need(
            forged_gzip == deterministic_gzip_bytes(expected_ledger),
            "noncanonical gzip bytes",
        )
    except VerificationError:
        rejected.append("ALTERNATE_GZIP_HEADER_SAME_OBJECT")
    else:
        raise VerificationError("alternate gzip-header attack accepted")

    expected_count = (
        len(row_attacks) + len(ledger_attacks) + len(result_attacks) + 2
    )
    need(
        expected_count >= 20 and len(rejected) == expected_count,
        "all targeted re-sign attacks rejected",
    )
    return {
        "attack_count": expected_count,
        "rejected_attack_count": len(rejected),
        "all_targeted_resigned_attacks_rejected": True,
        "row_attacks_reclosed_by_own_SHA256": True,
        "ledger_attacks_recommitted_at_object_level": True,
        "result_attacks_reclosed_at_result_SHA256_level": True,
        "coordinated_row_ledger_result_attack_reclosed": True,
        "alternate_gzip_header_same_object_rejected": True,
        "rejected_attack_ids": rejected,
    }


def verify() -> dict[str, Any]:
    # Upstream and producer bytes may be pinned before expected
    # reconstruction.  Candidate result/ledger bytes may not.
    for filename, expected_hash in UPSTREAM_PINS.items():
        need(
            file_sha256(HERE / filename) == expected_hash,
            f"upstream artifact pin:{filename}",
        )
    need(
        file_sha256(PRODUCER) == CANDIDATE_PINS[PRODUCER.name],
        "inert producer byte pin",
    )
    expected_result, expected_ledger, metadata = reconstruct_expected()
    expected_gzip = deterministic_gzip_bytes(expected_ledger)

    candidate_result, candidate_ledger, candidate_gzip = (
        audit_candidate_after_expected(expected_result, expected_ledger)
    )
    attacks = run_resigned_attacks(expected_result, expected_ledger)
    need(
        candidate_result == expected_result
        and candidate_ledger == expected_ledger
        and candidate_gzip == expected_gzip,
        "final candidate exact equality",
    )
    verification = {
        "schema": VERIFICATION_SCHEMA,
        "status": (
            "PASS_INDEPENDENT_CACHELESS_ROUND292_R287_REGISTRY_OVERLAP__"
            "421804_REGISTRY_ROWS__10020_SOURCE_UNIONS__10668_SOURCE_CELLS__"
            "1564_EXACT_OVERLAPS__11852_EXACT_REFINEMENT_CELLS__"
            "9404_REFINED_NEW_SUPPORTS__UNRESOLVED_ZERO__ZERO_CREDIT"
        ),
        "artifact_pins": dict(
            sorted({**UPSTREAM_PINS, **CANDIDATE_PINS}.items())
        ),
        "independence_contract": {
            "Round292_probe_producer_imported_or_executed": False,
            "Round292_probe_producer_treated_only_as_pinned_inert_bytes": True,
            "candidate_result_or_ledger_bytes_opened_before_expected_registry_overlap_refinement_pair_audit_complete":
                False,
            "candidate_result_used_as_registry_or_overlap_or_refinement_oracle":
                False,
            "candidate_ledger_used_as_registry_or_overlap_or_refinement_oracle":
                False,
            "cache_or_pickle_input_used": False,
            "exact_arithmetic": "fractions.Fraction",
            "independent_registry_index": "exact deterministic p-interval tree",
            "independent_partition_coordinates": "(t^2,p,s)",
        },
        "independent_reconstruction": {
            **metadata,
            "preserved_occurrence_count": 126_468,
            "new_atom_candidate_count": 295_336,
            "conditional_base_atom_registry_count": 421_804,
            "Round287_support_union_count": 10_020,
            "Round287_source_support_cell_count": 10_668,
            "registry_positive_overlap_row_count": 1_564,
            "overlap_incident_support_union_count": 920,
            "exact_refinement_cell_count": 11_852,
            "occupied_unique_target_refinement_cell_count": 1_600,
            "uncovered_refinement_cell_count": 10_252,
            "refined_local_support_connectivity_rank": 848,
            "refined_new_support_component_count": 9_404,
            "fully_existing_covered_source_union_count": 616,
            "partially_existing_covered_source_union_count": 304,
            "untouched_source_union_count": 9_100,
            "exact_transformed_volume_conservation": True,
            "pairwise_unresolved_positive_overlap_count": 0,
        },
        "ledger_commitment_audit": {
            "row_count": expected_ledger["row_count"],
            "rows_sha256": expected_ledger["rows_sha256"],
            "deterministic_gzip_file_sha256":
                hashlib.sha256(expected_gzip).hexdigest(),
            "candidate_object_exactly_equals_independent_reconstruction": True,
            "candidate_gzip_bytes_exactly_equal_independent_reconstruction": True,
            "every_row_closed_by_own_SHA256": True,
        },
        "candidate_result_audit": {
            "result_sha256": expected_result["result_sha256"],
            "candidate_file_sha256": hashlib.sha256(
                canonical(candidate_result) + b"\n"
            ).hexdigest(),
            "candidate_exactly_equals_independent_reconstruction": True,
            "all_formal_credit_fields_zero": True,
        },
        "targeted_reclosed_attacks": attacks,
        "replay_contract": {
            "seed_argument_affects_output": False,
            "external_PYTHONHASHSEED_replay_expected_byte_identical": True,
        },
        "strict_nonpromotion": EXPECTED_NONPROMOTION,
        "verification_sha256": "",
    }
    verification["verification_sha256"] = digest(
        {
            key: value
            for key, value in verification.items()
            if key != "verification_sha256"
        }
    )
    return verification


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--seed",
        default="292071",
        help="Cold-replay label; deliberately excluded from canonical output.",
    )
    parser.add_argument("--output", type=Path, default=OUTPUT)
    arguments = parser.parse_args()
    del arguments.seed
    verification = verify()
    atomic_write(arguments.output, canonical(verification) + b"\n")
    print(verification["status"])
    print("verification_sha256=" + verification["verification_sha256"])
    print("verification_file_sha256=" + file_sha256(arguments.output))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
