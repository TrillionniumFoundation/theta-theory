#!/usr/bin/env python3
"""Formal boundary atlas for every Round179 resolved source-G child.

This producer is deliberately coordinate-local.  It materializes the closed
2D faces, 1D edges, and 0D corners of all 17,192 Round179 resolved children,
then gives those strata canonical half-open incidence labels.  Coordinate
adjacency is accepted only inside an identical pinned Round174 parent atlas
and only on an exact shared face or an explicitly constructed positive-area
common refinement.  A coordinate adjacency is not a physical glue.

Round179 event normal forms are carried forward for every relevant origin.
Because a Round179 ``resolved`` child is produced only after the dynamic
signature is strict on its closed interval enclosure, the origin-level event
zero sets have zero incidence with those resolved children.  No event sheet,
cross-chart glue, physical component, whole tube, or global exact-key fibre is
invented here.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from fractions import Fraction
import hashlib
import json
import os
from pathlib import Path
import stat
import tempfile
from typing import Any


HERE = Path(__file__).resolve().parent
PREFIX = "cm2_round220_source_g_round179_resolved_child_boundary_atlas"
OUTPUT = HERE / f"{PREFIX}_certificate.json"
SCHEMA = "cm2.round220.source-g-round179-resolved-child-boundary-atlas.v1"
STATUS = (
    "CERTIFIED_FORMAL_ROUND179_RESOLVED_CHILD_COORDINATE_BOUNDARY_ATLAS__"
    "NO_PHYSICAL_OR_GLOBAL_PROMOTION"
)
MAX_INPUT_BYTES = 700 * 1024 * 1024

R179 = "cm2_round179_source_g_residual_tube_arrangement"
R216 = "cm2_round216_source_g_global_key_occurrence_exhaustion_frontier"
R217 = "cm2_round217_source_g_internal_face_trace_glue_materialization"

PACKAGE_MANIFESTS = {
    R179: (
        f"{R179}_manifest.sha256",
        "8fd5ae3a0cdd0c3321c0f8ffe6183ab57d31088b96523fa41ce0ebbe10d78b76",
        7,
    ),
    R216: (
        f"{R216}_manifest.sha256",
        "54f9f270a6bad485691fa1db12a46052fcd91615b01461ce40ad55b66475b58b",
        6,
    ),
    R217: (
        f"{R217}_manifest.sha256",
        "2b6df0e791e62743ee7a27e8556292166f07d8873a41e8de854b27787981b8c5",
        6,
    ),
}

EXPECTED_RESULTS = {
    "Round179_certificate":
        "0f57284c11c617349fe66877552c401f426efafbc75faa08948f099166e9cde3",
    "Round179_attachment":
        "a5468800c1d89cd307a5a26c608550b04db79c64c562fb12bedb22d6cec308cb",
    "Round179_verification":
        "ca2ec32d84edf55919a26f556fd8e9dfc39566ad876b0cb5537168fee2b28229",
    "Round216_certificate":
        "267a4b9aaaab6a576e1c1866cc2fa0b9dc9bf4fc6a3b08a210ed3821e45dd658",
    "Round216_verification":
        "23055888339f4e42ba968706d895ff6123a6b7549cbe176de835b2e68d0c3a6d",
    "Round217_certificate":
        "fb4519a43f76cbc765e24b3cb0a0e25267d9664091e22139913f3899fd1e2286",
    "Round217_verification":
        "48dd5123517f07bda9aa84ce76edd8e10e3baf1cc3924ad9e1398c1f3f28fb75",
}

AXES = ("t", "p", "s")
SIDES = ("LOWER", "UPPER")

CHILD_COLUMNS = [
    "atlas_child_id", "source_child_row_id", "origin_row_id", "parent_id",
    "chart", "child_index", "refinement_path", "box",
    "coordinate_volume", "chosen_split_axis", "split_coordinate",
    "split_face_side", "split_sibling_kind", "split_sibling_row_id",
    "owner_target", "official_key_ordinal", "official_key_id",
    "face_count", "edge_count", "corner_count",
    "origin_normal_form_reference_count",
    "event_sheet_incidence_count", "cross_chart_glue_count",
    "coordinate_boundary_atlas_complete", "whole_origin_credit",
    "physical_component_credit", "global_exact_key_disposition_credit",
]
FACE_COLUMNS = [
    "face_id", "child_ordinal", "source_child_row_id", "parent_id", "chart",
    "axis", "side", "fixed_coordinate", "tangential_axes",
    "tangential_half_open_box", "carrier_id", "closure_dimension",
    "half_open_incidence_status", "origin_boundary_role",
    "one_step_split_interface_id", "event_sheet_incidence_count",
    "coordinate_stratum_only", "physical_glue_credit",
    "global_exact_key_disposition_credit",
]
EDGE_COLUMNS = [
    "edge_id", "child_ordinal", "source_child_row_id", "parent_id", "chart",
    "fixed_axes", "fixed_sides", "fixed_coordinates", "free_axis",
    "free_half_open_interval", "carrier_id", "closure_dimension",
    "half_open_incidence_status", "meets_one_step_split_interface",
    "event_sheet_incidence_count", "coordinate_stratum_only",
    "physical_glue_credit", "global_exact_key_disposition_credit",
]
CORNER_COLUMNS = [
    "corner_id", "child_ordinal", "source_child_row_id", "parent_id",
    "chart", "sides", "coordinate", "carrier_id", "closure_dimension",
    "half_open_incidence_status", "meets_one_step_split_interface",
    "event_sheet_incidence_count", "coordinate_stratum_only",
    "physical_glue_credit", "global_exact_key_disposition_credit",
]
SPLIT_COLUMNS = [
    "split_interface_id", "origin_row_id", "parent_id", "chart", "axis",
    "fixed_coordinate", "tangential_half_open_box",
    "lower_child_kind", "lower_child_row_id",
    "upper_child_kind", "upper_child_row_id",
    "resolved_incidence_count", "retained_incidence_count",
    "resolved_to_resolved_coordinate_adjacency",
    "half_open_owner_child_kind", "half_open_owner_child_row_id",
    "event_trace_materialized_on_interface",
    "physical_glue_credit", "whole_origin_credit",
    "global_exact_key_disposition_credit",
]
ADJACENCY_COLUMNS = [
    "coordinate_adjacency_id", "common_refinement_id", "parent_id", "chart",
    "axis", "fixed_coordinate", "common_refinement_half_open_box",
    "negative_side_face_id", "positive_side_face_id",
    "negative_side_child_ordinal", "positive_side_child_ordinal",
    "relation", "exact_full_face", "positive_area_common_refinement",
    "same_origin", "same_official_key",
    "joined_from_box_touch_or_key_equality_alone",
    "formal_coordinate_adjacency_credit", "event_trace_glue_credit",
    "physical_component_credit", "global_exact_key_disposition_credit",
]
REJECTED_COLUMNS = [
    "candidate_id", "axis", "fixed_coordinate",
    "coincident_half_open_box", "negative_side_face_id",
    "positive_side_face_id", "negative_parent_id", "positive_parent_id",
    "negative_chart", "positive_chart", "same_chart", "same_official_key",
    "first_missing_proof", "coordinate_adjacency_credit",
    "physical_component_credit", "global_exact_key_disposition_credit",
]
NORMAL_COLUMNS = [
    "normal_form_id", "source_table", "source_row_id", "origin_row_id",
    "normal_form_kind", "equation", "gradient_axis", "gradient_sign",
    "face_classification", "dimension_account", "existence_over_origin",
    "source_packed_row_sha256", "source_packed_row",
]
REFERENCE_COLUMNS = [
    "reference_id", "child_ordinal", "source_child_row_id",
    "normal_form_id", "source_table", "source_row_id",
    "resolved_child_closed_enclosure_status",
    "event_sheet_incidence_count", "event_trace_glue_count",
    "proof_basis", "physical_component_credit",
    "global_exact_key_disposition_credit",
]
KEY_COLUMNS = [
    "official_key_ordinal", "official_key_id", "resolved_child_count",
    "face_count", "edge_count", "corner_count",
    "formal_coordinate_adjacency_count",
    "exact_full_face_adjacency_count",
    "partial_common_refinement_adjacency_count",
    "one_step_resolved_retained_frontier_count",
    "origin_normal_form_reference_count", "event_sheet_incidence_count",
    "cross_chart_glue_count", "coordinate_boundary_atlas_complete",
    "global_exact_key_fibre_exhausted", "whole_origin_credit",
    "physical_component_credit", "global_exact_key_disposition_credit",
]


class Round220Error(RuntimeError):
    pass


def require(condition: bool, label: str) -> None:
    if not condition:
        raise Round220Error(label)


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode()


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def make_id(label: str, payload: Any) -> str:
    return f"round220-{label}:{digest(payload)}"


def qstr(value: Fraction) -> str:
    return (
        str(value.numerator)
        if value.denominator == 1
        else f"{value.numerator}/{value.denominator}"
    )


def reject_noninteger(token: str) -> None:
    raise Round220Error(f"noninteger JSON number:{token}")


def unique_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    output: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in output, f"duplicate JSON key:{key}")
        output[key] = value
    return output


def regular_bytes(path: Path, maximum: int = MAX_INPUT_BYTES) -> bytes:
    before = path.lstat()
    require(
        stat.S_ISREG(before.st_mode)
        and not path.is_symlink()
        and before.st_nlink == 1,
        f"single-link regular input:{path.name}",
    )
    require(0 < before.st_size <= maximum, f"bounded input:{path.name}")
    descriptor = os.open(
        path,
        os.O_RDONLY
        | getattr(os, "O_NOFOLLOW", 0)
        | getattr(os, "O_CLOEXEC", 0),
    )
    try:
        opened = os.fstat(descriptor)
        require(
            (
                opened.st_dev, opened.st_ino, opened.st_size,
                opened.st_mtime_ns,
            ) == (
                before.st_dev, before.st_ino, before.st_size,
                before.st_mtime_ns,
            ),
            f"stable open:{path.name}",
        )
        chunks: list[bytes] = []
        size = 0
        while True:
            chunk = os.read(descriptor, 1024 * 1024)
            if not chunk:
                break
            size += len(chunk)
            require(size <= maximum, f"bounded read:{path.name}")
            chunks.append(chunk)
        after = os.fstat(descriptor)
        require(
            (
                after.st_dev, after.st_ino, after.st_size,
                after.st_mtime_ns,
            ) == (
                opened.st_dev, opened.st_ino, opened.st_size,
                opened.st_mtime_ns,
            ),
            f"stable read:{path.name}",
        )
        return b"".join(chunks)
    finally:
        os.close(descriptor)


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(
        regular_bytes(path),
        object_pairs_hook=unique_pairs,
        parse_int=int,
        parse_float=reject_noninteger,
        parse_constant=reject_noninteger,
    )
    require(isinstance(value, dict), f"JSON object:{path.name}")
    return value


def parse_manifest(raw: bytes) -> dict[str, str]:
    rows: dict[str, str] = {}
    for line in raw.decode("ascii").splitlines():
        parts = line.split("  ")
        require(
            len(parts) == 2
            and len(parts[0]) == 64
            and all(character in "0123456789abcdef" for character in parts[0])
            and parts[1]
            and Path(parts[1]).name == parts[1]
            and parts[1] not in rows,
            "strict manifest row",
        )
        rows[parts[1]] = parts[0]
    return rows


def replay_inputs() -> tuple[dict[str, dict[str, str]], dict[str, Any]]:
    entries: dict[str, dict[str, str]] = {}
    for prefix, (filename, expected_sha, expected_count) in (
        PACKAGE_MANIFESTS.items()
    ):
        raw = regular_bytes(HERE / filename, 100_000)
        require(
            hashlib.sha256(raw).hexdigest() == expected_sha,
            f"manifest SHA:{prefix}",
        )
        parsed = parse_manifest(raw)
        require(len(parsed) == expected_count, f"manifest count:{prefix}")
        for entry, expected in parsed.items():
            require(
                hashlib.sha256(regular_bytes(HERE / entry)).hexdigest()
                == expected,
                f"manifest replay:{entry}",
            )
        entries[prefix] = parsed

    documents = {
        "r179_certificate": read_json(HERE / f"{R179}_certificate.json"),
        "r179_rows": read_json(HERE / f"{R179}_rows.json"),
        "r179_verification": read_json(HERE / f"{R179}_verification.json"),
        "r216_certificate": read_json(HERE / f"{R216}_certificate.json"),
        "r216_verification": read_json(HERE / f"{R216}_verification.json"),
        "r217_certificate": read_json(HERE / f"{R217}_certificate.json"),
        "r217_verification": read_json(HERE / f"{R217}_verification.json"),
    }
    observed = {
        "Round179_certificate":
            documents["r179_certificate"]["result_sha256"],
        "Round179_attachment": documents["r179_rows"]["result_sha256"],
        "Round179_verification":
            documents["r179_verification"]["result_sha256"],
        "Round216_certificate":
            documents["r216_certificate"]["result_sha256"],
        "Round216_verification":
            documents["r216_verification"]["result_sha256"],
        "Round217_certificate":
            documents["r217_certificate"]["result_sha256"],
        "Round217_verification":
            documents["r217_verification"]["result_sha256"],
    }
    require(observed == EXPECTED_RESULTS, "accepted dependency result hashes")
    blocker = documents["r216_certificate"]["result"][
        "formal_missing_exhaustion_frontier"
    ]["Round179_resolved_child_lower_dimensional_boundary_blocker"]
    require(
        blocker[
            "Round179_resolved_child_occurrence_count_missing_explicit_lower_dimensional_boundary_atlas"
        ] == 17_192
        and blocker["explicit_Round179_resolved_child_boundary_atlas_row_count"]
        == 0,
        "Round216 boundary blocker",
    )
    require(
        documents["r217_certificate"]["result"]["formal_credit_contract"][
            "formal_local_common_refinement_glue_credits"
        ] == 448
        and documents["r217_certificate"]["result"][
            "formal_credit_contract"
        ]["global_exact_key_disposition_credit"] == 0,
        "Round217 bounded evidence",
    )
    return entries, documents


def unpack(
    attachment: dict[str, Any], table_name: str,
) -> list[dict[str, Any]]:
    columns = attachment["row_column_schemas"][table_name]
    return [
        dict(zip(columns, packed, strict=True))
        for packed in attachment[table_name]
    ]


def pack(columns: list[str], row: dict[str, Any]) -> list[Any]:
    require(set(columns) == set(row), f"exact row keys:{columns[0]}")
    return [row[column] for column in columns]


def table(
    columns: list[str], rows: list[dict[str, Any]],
) -> dict[str, Any]:
    packed = [pack(columns, row) for row in rows]
    return {
        "columns": columns,
        "row_count": len(packed),
        "rows_sha256": digest(packed),
        "row_ids_sha256": digest([row[0] for row in packed]),
        "rows": packed,
    }


def box_values(box: list[str]) -> tuple[Fraction, ...]:
    require(len(box) == 6, "six box endpoints")
    values = tuple(Fraction(value) for value in box)
    require(
        values[0] < values[1]
        and values[2] < values[3]
        and values[4] < values[5],
        "positive box",
    )
    return values


def rect_for(
    values: tuple[Fraction, ...], axis: int,
) -> tuple[Fraction, Fraction, Fraction, Fraction]:
    tangential = [candidate for candidate in range(3) if candidate != axis]
    return (
        values[2 * tangential[0]],
        values[2 * tangential[0] + 1],
        values[2 * tangential[1]],
        values[2 * tangential[1] + 1],
    )


def rect_strings(
    rect: tuple[Fraction, Fraction, Fraction, Fraction],
) -> list[str]:
    return [qstr(value) for value in rect]


def build_result(producer_sha256: str) -> dict[str, Any]:
    manifests, documents = replay_inputs()
    attachment = documents["r179_rows"]["result"]
    origins = unpack(attachment, "origin_tube_rows")
    resolved = unpack(attachment, "resolved_3d_child_rows")
    retained = unpack(attachment, "retained_3d_child_rows")
    guards = unpack(attachment, "chart_guard_child_rows")
    require(
        len(origins) == 62_012
        and len(resolved) == 17_192
        and len(retained) == 106_680
        and len(guards) == 152,
        "Round179 source row census",
    )

    origin_by_id = {row["origin_row_id"]: row for row in origins}
    require(len(origin_by_id) == len(origins), "unique origins")
    children_by_origin: dict[str, list[tuple[str, dict[str, Any]]]] = (
        defaultdict(list)
    )
    for kind, rows in (
        ("RESOLVED", resolved),
        ("RETAINED", retained),
        ("GUARD", guards),
    ):
        for row in rows:
            children_by_origin[row["origin_row_id"]].append((kind, row))
    require(
        len(children_by_origin) == 62_012
        and all(
            sorted(row["child_index"] for _kind, row in rows) == [0, 1]
            for rows in children_by_origin.values()
        ),
        "exact one-step child partition",
    )
    relevant_origin_ids = {
        row["origin_row_id"] for row in resolved
    }
    require(len(relevant_origin_ids) == 13_076, "resolved origin census")

    normal_source_tables = (
        ("outgoing_normal_form_rows", "OUTGOING"),
        ("wall_normal_form_rows", "INTEGER_WALL"),
        ("source_chart_seam_rows", "SOURCE_CHART_SEAM"),
        ("pair_arrangement_candidate_rows", "PAIR_ARRANGEMENT_FRONTIER"),
    )
    relevant_normal_rows: list[dict[str, Any]] = []
    normal_ids_by_origin: dict[str, list[tuple[str, str, str]]] = (
        defaultdict(list)
    )
    expected_normal_counts = {
        "outgoing_normal_form_rows": 7_924,
        "wall_normal_form_rows": 4_896,
        "source_chart_seam_rows": 264,
        "pair_arrangement_candidate_rows": 8,
    }
    for table_name, kind in normal_source_tables:
        columns = attachment["row_column_schemas"][table_name]
        source_rows = [
            packed for packed in attachment[table_name]
            if packed[columns.index("origin_row_id")] in relevant_origin_ids
        ]
        require(
            len(source_rows) == expected_normal_counts[table_name],
            f"relevant normal form count:{table_name}",
        )
        for packed_row in source_rows:
            source = dict(zip(columns, packed_row, strict=True))
            if kind == "OUTGOING":
                equation = source["equation"]
                gradient_axis = source["gradient_axis"]
                gradient_sign = source["gradient_sign"]
                classification = source["face_classification"]
                dimension = source["zero_set_dimension_account"]
                existence = source["existence_over_full_base"]
            elif kind == "INTEGER_WALL":
                equation = source["zero_equation"]
                gradient_axis = source["target_gradient_axis"]
                gradient_sign = source["target_gradient_sign"]
                classification = source["target_face_classification"]
                dimension = source["zero_set_dimension_account"]
                existence = (
                    classification == "FULL_BASE_UNIQUE_GRAPH"
                )
            elif kind == "SOURCE_CHART_SEAM":
                equation = source["equation"]
                gradient_axis = source["gradient_axis"]
                gradient_sign = source["gradient_sign"]
                classification = source["face_classification"]
                dimension = source["exact_dimension"]
                existence = True
            else:
                equation = None
                gradient_axis = None
                gradient_sign = None
                classification = source["existence_certification"]
                dimension = source[
                    "candidate_pair_intersection_dimension"
                ]
                existence = False
            normal_id = make_id(
                "origin-normal-form",
                [table_name, source["row_id"], packed_row],
            )
            relevant_normal_rows.append({
                "normal_form_id": normal_id,
                "source_table": table_name,
                "source_row_id": source["row_id"],
                "origin_row_id": source["origin_row_id"],
                "normal_form_kind": kind,
                "equation": equation,
                "gradient_axis": gradient_axis,
                "gradient_sign": gradient_sign,
                "face_classification": classification,
                "dimension_account": dimension,
                "existence_over_origin": existence,
                "source_packed_row_sha256": digest(packed_row),
                "source_packed_row": packed_row,
            })
            normal_ids_by_origin[source["origin_row_id"]].append(
                (normal_id, table_name, source["row_id"])
            )
    relevant_normal_rows.sort(key=lambda row: row["normal_form_id"])

    child_rows: list[dict[str, Any]] = []
    face_rows: list[dict[str, Any]] = []
    edge_rows: list[dict[str, Any]] = []
    corner_rows: list[dict[str, Any]] = []
    split_rows: list[dict[str, Any]] = []
    reference_rows: list[dict[str, Any]] = []
    face_geometry: dict[
        tuple[int, int, int],
        tuple[Fraction, tuple[Fraction, Fraction, Fraction, Fraction]],
    ] = {}
    face_id_by_local: dict[tuple[int, int, int], str] = {}
    child_key: dict[int, tuple[int, str]] = {}
    key_counts: dict[int, Counter[str]] = defaultdict(Counter)
    key_ids: dict[int, set[str]] = defaultdict(set)
    split_id_by_origin: dict[str, str] = {}

    resolved_sorted = sorted(resolved, key=lambda row: row["row_id"])
    ordinal_by_id = {
        row["row_id"]: ordinal
        for ordinal, row in enumerate(resolved_sorted)
    }
    for origin_id in sorted(relevant_origin_ids):
        origin = origin_by_id[origin_id]
        source_children = sorted(
            children_by_origin[origin_id],
            key=lambda item: item[1]["child_index"],
        )
        lower_kind, lower = source_children[0]
        upper_kind, upper = source_children[1]
        axis = AXES.index(origin["chosen_split_axis"])
        original = box_values(origin["original_box"])
        midpoint = (original[2 * axis] + original[2 * axis + 1]) / 2
        lower_box = box_values(lower["box"])
        upper_box = box_values(upper["box"])
        require(
            lower_box[2 * axis] == original[2 * axis]
            and lower_box[2 * axis + 1] == midpoint
            and upper_box[2 * axis] == midpoint
            and upper_box[2 * axis + 1] == original[2 * axis + 1]
            and all(
                lower_box[index] == upper_box[index] == original[index]
                for candidate_axis in range(3)
                if candidate_axis != axis
                for index in (2 * candidate_axis, 2 * candidate_axis + 1)
            ),
            "exact dyadic child boxes",
        )
        rect = rect_for(original, axis)
        split_id = make_id(
            "one-step-split-interface",
            [
                origin_id, origin["parent_id"], origin["chart"],
                AXES[axis], qstr(midpoint), rect_strings(rect),
            ],
        )
        split_id_by_origin[origin_id] = split_id
        resolved_count = int(lower_kind == "RESOLVED") + int(
            upper_kind == "RESOLVED"
        )
        retained_count = int(lower_kind == "RETAINED") + int(
            upper_kind == "RETAINED"
        )
        require(
            (resolved_count, retained_count)
            in {(2, 0), (1, 1)},
            "relevant split taxonomy",
        )
        if resolved_count == 2:
            require(
                lower["official_key_id"] == upper["official_key_id"],
                "resolved siblings exact key",
            )
        split_rows.append({
            "split_interface_id": split_id,
            "origin_row_id": origin_id,
            "parent_id": origin["parent_id"],
            "chart": origin["chart"],
            "axis": AXES[axis],
            "fixed_coordinate": qstr(midpoint),
            "tangential_half_open_box": rect_strings(rect),
            "lower_child_kind": lower_kind,
            "lower_child_row_id": lower["row_id"],
            "upper_child_kind": upper_kind,
            "upper_child_row_id": upper["row_id"],
            "resolved_incidence_count": resolved_count,
            "retained_incidence_count": retained_count,
            "resolved_to_resolved_coordinate_adjacency":
                resolved_count == 2,
            "half_open_owner_child_kind": upper_kind,
            "half_open_owner_child_row_id": upper["row_id"],
            "event_trace_materialized_on_interface": False,
            "physical_glue_credit": 0,
            "whole_origin_credit": 0,
            "global_exact_key_disposition_credit": 0,
        })

    for ordinal, child in enumerate(resolved_sorted):
        origin = origin_by_id[child["origin_row_id"]]
        axis = AXES.index(origin["chosen_split_axis"])
        original = box_values(origin["original_box"])
        values = box_values(child["box"])
        midpoint = (original[2 * axis] + original[2 * axis + 1]) / 2
        siblings = sorted(
            children_by_origin[child["origin_row_id"]],
            key=lambda item: item[1]["child_index"],
        )
        sibling_kind, sibling = siblings[1 - child["child_index"]]
        require(
            child["child_index"] in {0, 1}
            and child["refinement_path"][-1]
            == f"{origin['chosen_split_axis']}{child['child_index']}"
            and Fraction(child["coordinate_volume"])
            * 2 == Fraction(origin["original_coordinate_volume"]),
            "resolved child exact split lineage",
        )
        split_side = "UPPER" if child["child_index"] == 0 else "LOWER"
        normal_refs = normal_ids_by_origin[child["origin_row_id"]]
        atlas_child_id = make_id(
            "resolved-child-atlas",
            [child["row_id"], child["box"], child["refinement_path"]],
        )
        key_ordinal = child["official_key_ordinal"]
        key_id = child["official_key_id"]
        child_key[ordinal] = (key_ordinal, key_id)
        key_ids[key_ordinal].add(key_id)
        key_counts[key_ordinal]["children"] += 1
        key_counts[key_ordinal]["normal_refs"] += len(normal_refs)
        if sibling_kind == "RETAINED":
            key_counts[key_ordinal]["resolved_retained_frontiers"] += 1
        child_rows.append({
            "atlas_child_id": atlas_child_id,
            "source_child_row_id": child["row_id"],
            "origin_row_id": child["origin_row_id"],
            "parent_id": child["parent_id"],
            "chart": child["chart"],
            "child_index": child["child_index"],
            "refinement_path": child["refinement_path"],
            "box": [qstr(value) for value in values],
            "coordinate_volume": child["coordinate_volume"],
            "chosen_split_axis": origin["chosen_split_axis"],
            "split_coordinate": qstr(midpoint),
            "split_face_side": split_side,
            "split_sibling_kind": sibling_kind,
            "split_sibling_row_id": sibling["row_id"],
            "owner_target": child["owner_target"],
            "official_key_ordinal": key_ordinal,
            "official_key_id": key_id,
            "face_count": 6,
            "edge_count": 12,
            "corner_count": 8,
            "origin_normal_form_reference_count": len(normal_refs),
            "event_sheet_incidence_count": 0,
            "cross_chart_glue_count": 0,
            "coordinate_boundary_atlas_complete": True,
            "whole_origin_credit": 0,
            "physical_component_credit": 0,
            "global_exact_key_disposition_credit": 0,
        })
        for normal_id, source_table, source_row_id in normal_refs:
            reference_rows.append({
                "reference_id": make_id(
                    "resolved-child-normal-form-reference",
                    [child["row_id"], normal_id],
                ),
                "child_ordinal": ordinal,
                "source_child_row_id": child["row_id"],
                "normal_form_id": normal_id,
                "source_table": source_table,
                "source_row_id": source_row_id,
                "resolved_child_closed_enclosure_status":
                    "STRICT_DYNAMIC_SIGNATURE__EVENT_ZERO_SET_ABSENT",
                "event_sheet_incidence_count": 0,
                "event_trace_glue_count": 0,
                "proof_basis":
                    "PINNED_ROUND179_RESOLVED_BUILD_REQUIRES_DYNAMIC_SIGNATURE_STRICT_ON_CLOSED_INTERVAL_ENCLOSURE",
                "physical_component_credit": 0,
                "global_exact_key_disposition_credit": 0,
            })

        for face_axis in range(3):
            tangential = [
                candidate for candidate in range(3)
                if candidate != face_axis
            ]
            rect = rect_for(values, face_axis)
            for side in range(2):
                fixed = values[2 * face_axis + side]
                face_id = make_id(
                    "coordinate-face",
                    [
                        child["row_id"], AXES[face_axis], SIDES[side],
                        qstr(fixed), rect_strings(rect),
                    ],
                )
                carrier_id = make_id(
                    "parent-face-carrier",
                    [
                        child["parent_id"], child["chart"],
                        AXES[face_axis], qstr(fixed), rect_strings(rect),
                    ],
                )
                is_split = (
                    face_axis == axis
                    and SIDES[side] == split_side
                    and fixed == midpoint
                )
                face_rows.append({
                    "face_id": face_id,
                    "child_ordinal": ordinal,
                    "source_child_row_id": child["row_id"],
                    "parent_id": child["parent_id"],
                    "chart": child["chart"],
                    "axis": AXES[face_axis],
                    "side": SIDES[side],
                    "fixed_coordinate": qstr(fixed),
                    "tangential_axes": [AXES[value] for value in tangential],
                    "tangential_half_open_box": rect_strings(rect),
                    "carrier_id": carrier_id,
                    "closure_dimension": 2,
                    "half_open_incidence_status": (
                        "INCLUDED_LOWER_FIXED_COORDINATE"
                        if side == 0
                        else "EXCLUDED_UPPER_FIXED_COORDINATE"
                    ),
                    "origin_boundary_role": (
                        "ONE_STEP_INTERNAL_SPLIT_FACE"
                        if is_split
                        else "INHERITED_ORIGIN_BOX_BOUNDARY_FACE"
                    ),
                    "one_step_split_interface_id": (
                        split_id_by_origin[child["origin_row_id"]]
                        if is_split else None
                    ),
                    "event_sheet_incidence_count": 0,
                    "coordinate_stratum_only": True,
                    "physical_glue_credit": 0,
                    "global_exact_key_disposition_credit": 0,
                })
                face_geometry[(ordinal, face_axis, side)] = (fixed, rect)
                face_id_by_local[(ordinal, face_axis, side)] = face_id
                key_counts[key_ordinal]["faces"] += 1

        for first_axis in range(3):
            for second_axis in range(first_axis + 1, 3):
                free_axis = 3 - first_axis - second_axis
                for first_side in range(2):
                    for second_side in range(2):
                        fixed_coordinates = [
                            qstr(values[2 * first_axis + first_side]),
                            qstr(values[2 * second_axis + second_side]),
                        ]
                        interval = [
                            qstr(values[2 * free_axis]),
                            qstr(values[2 * free_axis + 1]),
                        ]
                        edge_id = make_id(
                            "coordinate-edge",
                            [
                                child["row_id"],
                                [AXES[first_axis], AXES[second_axis]],
                                [SIDES[first_side], SIDES[second_side]],
                                fixed_coordinates, AXES[free_axis], interval,
                            ],
                        )
                        carrier_id = make_id(
                            "parent-edge-carrier",
                            [
                                child["parent_id"], child["chart"],
                                [AXES[first_axis], AXES[second_axis]],
                                fixed_coordinates, AXES[free_axis], interval,
                            ],
                        )
                        meets_split = (
                            (
                                first_axis == axis
                                and SIDES[first_side] == split_side
                                and values[2 * first_axis + first_side]
                                == midpoint
                            )
                            or (
                                second_axis == axis
                                and SIDES[second_side] == split_side
                                and values[2 * second_axis + second_side]
                                == midpoint
                            )
                        )
                        edge_rows.append({
                            "edge_id": edge_id,
                            "child_ordinal": ordinal,
                            "source_child_row_id": child["row_id"],
                            "parent_id": child["parent_id"],
                            "chart": child["chart"],
                            "fixed_axes": [
                                AXES[first_axis], AXES[second_axis]
                            ],
                            "fixed_sides": [
                                SIDES[first_side], SIDES[second_side]
                            ],
                            "fixed_coordinates": fixed_coordinates,
                            "free_axis": AXES[free_axis],
                            "free_half_open_interval": interval,
                            "carrier_id": carrier_id,
                            "closure_dimension": 1,
                            "half_open_incidence_status": (
                                "INCLUDED_BOTH_FIXED_COORDINATES_LOWER"
                                if first_side == second_side == 0
                                else "EXCLUDED_AT_LEAST_ONE_FIXED_COORDINATE_UPPER"
                            ),
                            "meets_one_step_split_interface": meets_split,
                            "event_sheet_incidence_count": 0,
                            "coordinate_stratum_only": True,
                            "physical_glue_credit": 0,
                            "global_exact_key_disposition_credit": 0,
                        })
                        key_counts[key_ordinal]["edges"] += 1

        for t_side in range(2):
            for p_side in range(2):
                for s_side in range(2):
                    sides = [t_side, p_side, s_side]
                    coordinate = [
                        qstr(values[2 * candidate + sides[candidate]])
                        for candidate in range(3)
                    ]
                    corner_id = make_id(
                        "coordinate-corner",
                        [child["row_id"], [SIDES[value] for value in sides],
                         coordinate],
                    )
                    carrier_id = make_id(
                        "parent-corner-carrier",
                        [child["parent_id"], child["chart"], coordinate],
                    )
                    meets_split = (
                        SIDES[sides[axis]] == split_side
                        and values[2 * axis + sides[axis]] == midpoint
                    )
                    corner_rows.append({
                        "corner_id": corner_id,
                        "child_ordinal": ordinal,
                        "source_child_row_id": child["row_id"],
                        "parent_id": child["parent_id"],
                        "chart": child["chart"],
                        "sides": [SIDES[value] for value in sides],
                        "coordinate": coordinate,
                        "carrier_id": carrier_id,
                        "closure_dimension": 0,
                        "half_open_incidence_status": (
                            "INCLUDED_ALL_FIXED_COORDINATES_LOWER"
                            if sides == [0, 0, 0]
                            else "EXCLUDED_AT_LEAST_ONE_FIXED_COORDINATE_UPPER"
                        ),
                        "meets_one_step_split_interface": meets_split,
                        "event_sheet_incidence_count": 0,
                        "coordinate_stratum_only": True,
                        "physical_glue_credit": 0,
                        "global_exact_key_disposition_credit": 0,
                    })
                    key_counts[key_ordinal]["corners"] += 1

    require(
        len(child_rows) == 17_192
        and len(face_rows) == 103_152
        and len(edge_rows) == 206_304
        and len(corner_rows) == 137_536
        and len(split_rows) == 13_076
        and len(reference_rows) == 17_208,
        "complete atlas and normal-reference census",
    )

    face_by_parent_plane: dict[
        tuple[str, str, int, Fraction],
        list[list[tuple[int, int, tuple[Fraction, ...]]]],
    ] = defaultdict(lambda: [[], []])
    face_by_raw_carrier: dict[
        tuple[int, Fraction, tuple[Fraction, ...]],
        list[list[tuple[int, int]]],
    ] = defaultdict(lambda: [[], []])
    for local, geometry in face_geometry.items():
        ordinal, axis, side = local
        fixed, rect = geometry
        child = resolved_sorted[ordinal]
        face_by_parent_plane[
            (child["parent_id"], child["chart"], axis, fixed)
        ][side].append((ordinal, side, rect))
        face_by_raw_carrier[(axis, fixed, rect)][side].append(
            (ordinal, side)
        )

    adjacency_rows: list[dict[str, Any]] = []
    adjacency_pair_keys: set[tuple[int, int, int]] = set()
    for (parent_id, chart, axis, fixed), sides in sorted(
        face_by_parent_plane.items(),
        key=lambda item: (
            item[0][0], item[0][1], item[0][2], item[0][3]
        ),
    ):
        # A LOWER face bounds a child on the positive coordinate side; an
        # UPPER face bounds a child on the negative coordinate side.
        for positive_ordinal, _positive_side, positive_rect in sides[0]:
            for negative_ordinal, _negative_side, negative_rect in sides[1]:
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
                require(
                    negative["official_key_id"]
                    == positive["official_key_id"],
                    "common-parent adjacency exact key agreement",
                )
                exact = negative_rect == positive_rect
                same_origin = (
                    negative["origin_row_id"] == positive["origin_row_id"]
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
                common_id = make_id(
                    "parent-face-common-refinement",
                    [
                        parent_id, chart, AXES[axis], qstr(fixed),
                        common_box,
                    ],
                )
                negative_face = face_id_by_local[
                    (negative_ordinal, axis, 1)
                ]
                positive_face = face_id_by_local[
                    (positive_ordinal, axis, 0)
                ]
                adjacency_id = make_id(
                    "coordinate-adjacency",
                    [common_id, negative_face, positive_face],
                )
                adjacency_rows.append({
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
                })
                pair_key = (
                    min(negative_ordinal, positive_ordinal),
                    max(negative_ordinal, positive_ordinal),
                    axis,
                )
                require(
                    pair_key not in adjacency_pair_keys,
                    "unique child-axis adjacency",
                )
                adjacency_pair_keys.add(pair_key)
                key_ordinal = negative["official_key_ordinal"]
                key_counts[key_ordinal]["adjacencies"] += 1
                key_counts[key_ordinal][
                    "exact_adjacencies" if exact else "partial_adjacencies"
                ] += 1
    adjacency_rows.sort(key=lambda row: row["coordinate_adjacency_id"])
    adjacency_class = Counter(row["relation"] for row in adjacency_rows)
    adjacency_axis = Counter(row["axis"] for row in adjacency_rows)
    require(
        len(adjacency_rows) == 10_384
        and adjacency_class == {
            "SAME_ORIGIN_EXACT_ONE_STEP_SPLIT": 4_116,
            "CROSS_ORIGIN_EXACT_SHARED_PARENT_FACE": 5_900,
            "CROSS_ORIGIN_POSITIVE_AREA_PARENT_COMMON_REFINEMENT": 368,
        }
        and adjacency_axis == {"t": 2_572, "p": 2_452, "s": 5_360},
        "formal coordinate adjacency census",
    )

    rejected_rows: list[dict[str, Any]] = []
    for (axis, fixed, rect), sides in sorted(
        face_by_raw_carrier.items(),
        key=lambda item: (item[0][0], item[0][1], item[0][2]),
    ):
        for positive_ordinal, _positive_side in sides[0]:
            for negative_ordinal, _negative_side in sides[1]:
                negative = resolved_sorted[negative_ordinal]
                positive = resolved_sorted[positive_ordinal]
                if negative["parent_id"] == positive["parent_id"]:
                    continue
                negative_face = face_id_by_local[
                    (negative_ordinal, axis, 1)
                ]
                positive_face = face_id_by_local[
                    (positive_ordinal, axis, 0)
                ]
                same_chart = negative["chart"] == positive["chart"]
                same_key = (
                    negative["official_key_id"] == positive["official_key_id"]
                )
                rejected_rows.append({
                    "candidate_id": make_id(
                        "rejected-coordinate-coincidence",
                        [negative_face, positive_face],
                    ),
                    "axis": AXES[axis],
                    "fixed_coordinate": qstr(fixed),
                    "coincident_half_open_box": rect_strings(rect),
                    "negative_side_face_id": negative_face,
                    "positive_side_face_id": positive_face,
                    "negative_parent_id": negative["parent_id"],
                    "positive_parent_id": positive["parent_id"],
                    "negative_chart": negative["chart"],
                    "positive_chart": positive["chart"],
                    "same_chart": same_chart,
                    "same_official_key": same_key,
                    "first_missing_proof":
                        "NO_IDENTICAL_PARENT_ATLAS_OR_EXPLICIT_CROSS_CHART_TRANSITION_ID",
                    "coordinate_adjacency_credit": 0,
                    "physical_component_credit": 0,
                    "global_exact_key_disposition_credit": 0,
                })
    rejected_rows.sort(key=lambda row: row["candidate_id"])
    rejected_class = Counter(
        (row["same_chart"], row["same_official_key"])
        for row in rejected_rows
    )
    require(
        len(rejected_rows) == 9_830
        and rejected_class == {
            (True, True): 328,
            (False, False): 9_502,
        },
        "rejected raw-coordinate coincidence census",
    )

    face_carriers = Counter(row["carrier_id"] for row in face_rows)
    edge_carriers = Counter(row["carrier_id"] for row in edge_rows)
    corner_carriers = Counter(row["carrier_id"] for row in corner_rows)
    require(
        len(face_carriers) == 93_136
        and Counter(face_carriers.values()) == {1: 83_120, 2: 10_016}
        and len(edge_carriers) == 166_528
        and Counter(edge_carriers.values())
        == {1: 130_388, 2: 33_976, 3: 692, 4: 1_472}
        and len(corner_carriers) == 96_612
        and Counter(corner_carriers.values())
        == {1: 63_560, 2: 28_364, 3: 1_564, 4: 3_092, 5: 4, 6: 28},
        "parent-atlas carrier multiplicities",
    )

    key_rows: list[dict[str, Any]] = []
    for key_ordinal in sorted(key_counts):
        require(
            len(key_ids[key_ordinal]) == 1,
            "one official key id per ordinal",
        )
        counts = key_counts[key_ordinal]
        key_rows.append({
            "official_key_ordinal": key_ordinal,
            "official_key_id": next(iter(key_ids[key_ordinal])),
            "resolved_child_count": counts["children"],
            "face_count": counts["faces"],
            "edge_count": counts["edges"],
            "corner_count": counts["corners"],
            "formal_coordinate_adjacency_count": counts["adjacencies"],
            "exact_full_face_adjacency_count": counts["exact_adjacencies"],
            "partial_common_refinement_adjacency_count":
                counts["partial_adjacencies"],
            "one_step_resolved_retained_frontier_count":
                counts["resolved_retained_frontiers"],
            "origin_normal_form_reference_count": counts["normal_refs"],
            "event_sheet_incidence_count": 0,
            "cross_chart_glue_count": 0,
            "coordinate_boundary_atlas_complete": True,
            "global_exact_key_fibre_exhausted": False,
            "whole_origin_credit": 0,
            "physical_component_credit": 0,
            "global_exact_key_disposition_credit": 0,
        })
    require(
        len(key_rows) == 116
        and sum(row["resolved_child_count"] for row in key_rows) == 17_192
        and sum(row["face_count"] for row in key_rows) == 103_152
        and sum(row["edge_count"] for row in key_rows) == 206_304
        and sum(row["corner_count"] for row in key_rows) == 137_536
        and sum(
            row["formal_coordinate_adjacency_count"] for row in key_rows
        ) == 10_384
        and sum(
            row["one_step_resolved_retained_frontier_count"]
            for row in key_rows
        ) == 8_960
        and sum(
            row["origin_normal_form_reference_count"] for row in key_rows
        ) == 17_208
        and all(
            row["coordinate_boundary_atlas_complete"]
            and not row["global_exact_key_fibre_exhausted"]
            and row["event_sheet_incidence_count"] == 0
            and row["cross_chart_glue_count"] == 0
            and row["whole_origin_credit"] == 0
            and row["physical_component_credit"] == 0
            and row["global_exact_key_disposition_credit"] == 0
            for row in key_rows
        ),
        "per-key complete coordinate coverage and nonpromotion",
    )

    child_rows.sort(key=lambda row: row["source_child_row_id"])
    face_rows.sort(key=lambda row: row["face_id"])
    edge_rows.sort(key=lambda row: row["edge_id"])
    corner_rows.sort(key=lambda row: row["corner_id"])
    split_rows.sort(key=lambda row: row["split_interface_id"])
    reference_rows.sort(key=lambda row: row["reference_id"])
    key_rows.sort(key=lambda row: row["official_key_ordinal"])

    atlas_tables = {
        "resolved_child_rows": table(CHILD_COLUMNS, child_rows),
        "coordinate_face_rows": table(FACE_COLUMNS, face_rows),
        "coordinate_edge_rows": table(EDGE_COLUMNS, edge_rows),
        "coordinate_corner_rows": table(CORNER_COLUMNS, corner_rows),
        "one_step_split_interface_rows": table(SPLIT_COLUMNS, split_rows),
        "formal_coordinate_adjacency_rows":
            table(ADJACENCY_COLUMNS, adjacency_rows),
        "rejected_exact_coordinate_coincidence_rows":
            table(REJECTED_COLUMNS, rejected_rows),
    }
    normal_tables = {
        "relevant_origin_normal_form_rows":
            table(NORMAL_COLUMNS, relevant_normal_rows),
        "resolved_child_normal_form_reference_rows":
            table(REFERENCE_COLUMNS, reference_rows),
    }
    key_table = table(KEY_COLUMNS, key_rows)

    result = {
        "status": STATUS,
        "formal_input_binding": {
            **{
                f"{prefix}_manifest_sha256":
                    PACKAGE_MANIFESTS[prefix][1]
                for prefix in PACKAGE_MANIFESTS
            },
            **{
                f"{prefix}_manifest_entries":
                    dict(sorted(manifests[prefix].items()))
                for prefix in PACKAGE_MANIFESTS
            },
            "all_three_manifests_and_19_entries_replayed": (
                sum(len(rows) for rows in manifests.values()) == 19
            ),
            "accepted_result_sha256": dict(sorted(EXPECTED_RESULTS.items())),
            "Round217_is_read_only_separate_Round208_trace_evidence": True,
            "Round217_rows_not_substituted_for_Round179_child_atlas": True,
        },
        "coordinate_boundary_atlas": {
            "scope": (
                "ALL_17192_PINNED_ROUND179_RESOLVED_CHILD_CLOSED_BOX_STRATA"
            ),
            "canonical_half_open_convention": {
                "box": "[t0,t1) x [p0,p1) x [s0,s1)",
                "face_incidence_included_iff_fixed_side": "LOWER",
                "edge_incidence_included_iff_both_fixed_sides": "LOWER",
                "corner_incidence_included_iff_all_fixed_sides": "LOWER",
                "closure_strata_recorded_even_when_half_open_excluded": True,
                "half_open_label_is_coordinate_ownership_not_physical_boundary":
                    True,
            },
            "tables": atlas_tables,
            "headline_census": {
                "resolved_child_count": 17_192,
                "two_D_face_incidence_count": 103_152,
                "one_D_edge_incidence_count": 206_304,
                "zero_D_corner_incidence_count": 137_536,
                "one_step_split_interface_count": 13_076,
                "resolved_resolved_one_step_split_count": 4_116,
                "resolved_retained_one_step_frontier_count": 8_960,
                "formal_same_parent_coordinate_adjacency_count": 10_384,
                "exact_full_face_adjacency_count": 10_016,
                "positive_area_common_refinement_adjacency_count": 368,
                "same_origin_exact_adjacency_count": 4_116,
                "cross_origin_same_parent_exact_adjacency_count": 5_900,
                "cross_origin_same_parent_partial_adjacency_count": 368,
                "rejected_different_parent_exact_coordinate_coincidence_count":
                    9_830,
            },
            "parent_atlas_carrier_census": {
                "face_carrier_count": len(face_carriers),
                "face_incidence_multiplicity_histogram":
                    dict(sorted(Counter(face_carriers.values()).items())),
                "edge_carrier_count": len(edge_carriers),
                "edge_incidence_multiplicity_histogram":
                    dict(sorted(Counter(edge_carriers.values()).items())),
                "corner_carrier_count": len(corner_carriers),
                "corner_incidence_multiplicity_histogram":
                    dict(sorted(Counter(corner_carriers.values()).items())),
            },
        },
        "outgoing_wall_and_seam_normal_form_boundary_account": {
            "tables": normal_tables,
            "relevant_origin_normal_form_count":
                len(relevant_normal_rows),
            "resolved_child_normal_form_reference_count":
                len(reference_rows),
            "normal_form_kind_count": dict(sorted(
                Counter(
                    row["normal_form_kind"]
                    for row in relevant_normal_rows
                ).items()
            )),
            "materialized_event_sheet_row_count_on_resolved_children": 0,
            "materialized_event_sheet_incidence_count_on_resolved_children": 0,
            "formal_reason": (
                "PINNED_ROUND179_RESOLVED_CHILDREN_REQUIRE_A_STRICT_DYNAMIC_"
                "SIGNATURE_ON_THE_CLOSED_INTERVAL_ENCLOSURE; THE_ORIGIN_EVENT_"
                "ZERO_SETS_THEREFORE_HAVE_ZERO_CHILD_INCIDENCE"
            ),
            "origin_normal_forms_are_not_claimed_to_be_clipped_sheets_on_the_retained_sibling":
                True,
            "pair_arrangement_equations_or_isolation_not_invented": True,
        },
        "per_key_coordinate_coverage_ledger": key_table,
        "Round216_boundary_blocker_delta": {
            "Round216_missing_resolved_child_count": 17_192,
            "Round220_atlased_resolved_child_count": 17_192,
            "remaining_unatlased_Round179_resolved_child_count": 0,
            "coordinate_face_rows_added": 103_152,
            "coordinate_edge_rows_added": 206_304,
            "coordinate_corner_rows_added": 137_536,
            "coordinate_atlas_blocker_closed": True,
            "physical_glue_blocker_closed": False,
            "cross_chart_transition_blocker_closed": False,
            "global_exact_key_exhaustion_blocker_closed": False,
        },
        "strict_nonpromotion": {
            "formal_coordinate_adjacency_is_physical_glue": False,
            "formal_coordinate_adjacency_credit": 10_384,
            "formal_event_trace_glue_credit": 0,
            "cross_chart_glue_count": 0,
            "whole_origin_credit": 0,
            "whole_original_tube_credit": 0,
            "physical_component_credit": 0,
            "global_exact_key_fibre_exhausted_count": 0,
            "global_exact_key_disposition_credit": 0,
            "source_G_global_exact_key_dispositions": "0/224580",
            "D02": "BLOCKED",
            "D03_negative_oracle": "UNAUTHORIZED",
            "global_Gate5_fields": "10/18",
            "global_complete_18_field_blocks": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "next_core_gate": (
            "derive explicit cross-parent/cross-chart transition identities "
            "and exact event-trace restrictions before any physical-component "
            "quotient; then combine with the still-open Round217 endpoint-to-"
            "interior and partial-face frontiers"
        ),
        "provenance": {
            "schema": SCHEMA,
            "producer_sha256": producer_sha256,
            "formal_input_files_modified": False,
        },
    }
    return result


def validate_output(path: Path) -> Path:
    require(not any(part == ".." for part in path.parts), "output parent alias")
    absolute = Path(os.path.abspath(os.fspath(path)))
    require(
        absolute.parent == HERE
        and absolute.parent.resolve() == HERE
        and (
            absolute.name == OUTPUT.name
            or (
                absolute.name.startswith(".cm2_round220_")
                and absolute.name.endswith("_certificate.json")
            )
        ),
        "output exact directory and allowlist",
    )
    protected = {
        Path(__file__).resolve(),
        *((HERE / values[0]).resolve()
          for values in PACKAGE_MANIFESTS.values()),
    }
    require(
        absolute.resolve(strict=False) not in protected,
        "protected output",
    )
    if absolute.exists() or absolute.is_symlink():
        metadata = absolute.lstat()
        require(
            stat.S_ISREG(metadata.st_mode)
            and not absolute.is_symlink()
            and metadata.st_nlink == 1,
            "existing output type",
        )
    return absolute


def safe_write(path: Path, data: bytes) -> None:
    absolute = validate_output(path)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{absolute.name}.",
        suffix=".tmp",
        dir=absolute.parent,
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            descriptor = -1
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, absolute)
        directory_descriptor = os.open(
            os.fspath(absolute.parent),
            os.O_RDONLY
            | getattr(os, "O_DIRECTORY", 0)
            | getattr(os, "O_CLOEXEC", 0),
        )
        try:
            os.fsync(directory_descriptor)
        finally:
            os.close(directory_descriptor)
    except BaseException:
        if descriptor >= 0:
            os.close(descriptor)
        raise
    finally:
        if temporary.exists() or temporary.is_symlink():
            temporary.unlink()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    arguments = parser.parse_args()
    producer_sha256 = hashlib.sha256(regular_bytes(Path(__file__))).hexdigest()
    result = build_result(producer_sha256)
    certificate = {
        "schema": SCHEMA,
        "result": result,
        "result_sha256": digest(result),
    }
    safe_write(arguments.output, canonical_bytes(certificate) + b"\n")
    print(STATUS)
    print(f"result_sha256={certificate['result_sha256']}")
    print(f"output={validate_output(arguments.output)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
