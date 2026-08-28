#!/usr/bin/env python3
"""Fresh verifier for the Round220 resolved-child boundary atlas.

The producer is never imported or executed.  Every candidate table row is
checked against an independently decoded Round179 attachment, and the complete
Python object is checked field-by-field plus by its canonical result hash.
"""

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
PREFIX = "cm2_round220_source_g_round179_resolved_child_boundary_atlas"
PRODUCER = HERE / f"{PREFIX}.py"
CANDIDATE = HERE / f"{PREFIX}_certificate.json"
OUTPUT = HERE / f"{PREFIX}_verification.json"
CANDIDATE_SCHEMA = (
    "cm2.round220.source-g-round179-resolved-child-boundary-atlas.v1"
)
VERIFICATION_SCHEMA = f"{CANDIDATE_SCHEMA}.verification.v1"
EXPECTED_STATUS = (
    "CERTIFIED_FORMAL_ROUND179_RESOLVED_CHILD_COORDINATE_BOUNDARY_ATLAS__"
    "NO_PHYSICAL_OR_GLOBAL_PROMOTION"
)
PASS_STATUS = "PASS_FORMAL_ROUND220"
PRODUCER_SHA = (
    "ae5c4fc259050bafeef335b88a3504ba3de49c64154f128ec26a461ebefdd3f4"
)
RESULT_SHA = (
    "4d8168cb25bd389f16b332798fcf9b57951deedd8d328bc5a1dac9024508669b"
)
MAX_BYTES = 700 * 1024 * 1024
R179 = "cm2_round179_source_g_residual_tube_arrangement"
R216 = "cm2_round216_source_g_global_key_occurrence_exhaustion_frontier"
R217 = "cm2_round217_source_g_internal_face_trace_glue_materialization"
MANIFESTS = {
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
DEPENDENCIES = {
    f"{R179}_certificate.json":
        "0f57284c11c617349fe66877552c401f426efafbc75faa08948f099166e9cde3",
    f"{R179}_rows.json":
        "a5468800c1d89cd307a5a26c608550b04db79c64c562fb12bedb22d6cec308cb",
    f"{R179}_verification.json":
        "ca2ec32d84edf55919a26f556fd8e9dfc39566ad876b0cb5537168fee2b28229",
    f"{R216}_certificate.json":
        "267a4b9aaaab6a576e1c1866cc2fa0b9dc9bf4fc6a3b08a210ed3821e45dd658",
    f"{R216}_verification.json":
        "23055888339f4e42ba968706d895ff6123a6b7549cbe176de835b2e68d0c3a6d",
    f"{R217}_certificate.json":
        "fb4519a43f76cbc765e24b3cb0a0e25267d9664091e22139913f3899fd1e2286",
    f"{R217}_verification.json":
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
ADJ_COLUMNS = [
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
REJECT_COLUMNS = [
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
REF_COLUMNS = [
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


class VError(RuntimeError):
    pass


def need(condition: bool, label: str) -> None:
    if not condition:
        raise VError(label)


def canon(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False,
        allow_nan=False,
    ).encode()


def h(value: Any) -> str:
    return hashlib.sha256(canon(value)).hexdigest()


def rid(label: str, payload: Any) -> str:
    return f"round220-{label}:{h(payload)}"


def qs(value: Q) -> str:
    return (
        str(value.numerator) if value.denominator == 1
        else f"{value.numerator}/{value.denominator}"
    )


def pair_hook(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        need(key not in result, f"duplicate key:{key}")
        result[key] = value
    return result


def bad_number(token: str) -> None:
    raise VError(f"noninteger:{token}")


def secure_bytes(path: Path, limit: int = MAX_BYTES) -> bytes:
    before = path.lstat()
    need(
        stat.S_ISREG(before.st_mode) and not path.is_symlink()
        and before.st_nlink == 1 and 0 < before.st_size <= limit,
        f"secure input:{path.name}",
    )
    descriptor = os.open(
        path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
        | getattr(os, "O_CLOEXEC", 0),
    )
    try:
        opened = os.fstat(descriptor)
        need(
            (opened.st_dev, opened.st_ino, opened.st_size, opened.st_mtime_ns)
            == (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns),
            f"stable open:{path.name}",
        )
        chunks: list[bytes] = []
        size = 0
        while True:
            chunk = os.read(descriptor, 1024 * 1024)
            if not chunk:
                break
            size += len(chunk)
            need(size <= limit, f"bounded:{path.name}")
            chunks.append(chunk)
        after = os.fstat(descriptor)
        need(
            (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns)
            == (opened.st_dev, opened.st_ino, opened.st_size, opened.st_mtime_ns),
            f"stable read:{path.name}",
        )
        return b"".join(chunks)
    finally:
        os.close(descriptor)


def decode(raw: bytes) -> dict[str, Any]:
    value = json.loads(
        raw, object_pairs_hook=pair_hook, parse_int=int,
        parse_float=bad_number, parse_constant=bad_number,
    )
    need(isinstance(value, dict), "root object")
    return value


def load(path: Path) -> dict[str, Any]:
    return decode(secure_bytes(path))


def unpack(attachment: dict[str, Any], name: str) -> list[dict[str, Any]]:
    columns = attachment["row_column_schemas"][name]
    return [dict(zip(columns, row, strict=True)) for row in attachment[name]]


def box(raw: list[str]) -> tuple[Q, ...]:
    values = tuple(Q(value) for value in raw)
    need(
        len(values) == 6 and values[0] < values[1]
        and values[2] < values[3] and values[4] < values[5],
        "positive box",
    )
    return values


def rect(values: tuple[Q, ...], axis: int) -> tuple[Q, Q, Q, Q]:
    other = [candidate for candidate in range(3) if candidate != axis]
    return (
        values[2 * other[0]], values[2 * other[0] + 1],
        values[2 * other[1]], values[2 * other[1] + 1],
    )


def texts(values: tuple[Q, ...]) -> list[str]:
    return [qs(value) for value in values]


def rows_as_dicts(table: dict[str, Any], columns: list[str]) -> list[dict[str, Any]]:
    need(
        set(table) == {
            "columns", "row_count", "rows_sha256", "row_ids_sha256", "rows"
        } and table["columns"] == columns
        and table["row_count"] == len(table["rows"])
        and table["rows_sha256"] == h(table["rows"])
        and table["row_ids_sha256"] == h([row[0] for row in table["rows"]]),
        f"packed table envelope:{columns[0]}",
    )
    return [
        dict(zip(columns, packed, strict=True))
        for packed in table["rows"]
    ]


def parse_manifest(raw: bytes) -> dict[str, str]:
    result: dict[str, str] = {}
    for line in raw.decode("ascii").splitlines():
        cells = line.split("  ")
        need(
            len(cells) == 2 and len(cells[0]) == 64
            and all(character in "0123456789abcdef" for character in cells[0])
            and Path(cells[1]).name == cells[1] and cells[1] not in result,
            "manifest row",
        )
        result[cells[1]] = cells[0]
    return result


def replay() -> tuple[dict[str, dict[str, str]], dict[str, Any]]:
    entries: dict[str, dict[str, str]] = {}
    for prefix, (filename, expected, count) in MANIFESTS.items():
        raw = secure_bytes(HERE / filename, 100_000)
        need(hashlib.sha256(raw).hexdigest() == expected, f"manifest:{prefix}")
        parsed = parse_manifest(raw)
        need(len(parsed) == count, f"manifest count:{prefix}")
        for name, file_hash in parsed.items():
            need(
                hashlib.sha256(secure_bytes(HERE / name)).hexdigest()
                == file_hash,
                f"manifest replay:{name}",
            )
        entries[prefix] = parsed
    docs: dict[str, Any] = {}
    for name, result_hash in DEPENDENCIES.items():
        document = load(HERE / name)
        need(
            document["result_sha256"] == result_hash
            and h(document["result"]) == result_hash,
            f"dependency result:{name}",
        )
        docs[name] = document
    return entries, docs


def expected_binding(entries: dict[str, dict[str, str]]) -> dict[str, Any]:
    return {
        **{
            f"{prefix}_manifest_sha256": MANIFESTS[prefix][1]
            for prefix in MANIFESTS
        },
        **{
            f"{prefix}_manifest_entries":
                dict(sorted(entries[prefix].items()))
            for prefix in MANIFESTS
        },
        "all_three_manifests_and_19_entries_replayed": True,
        "accepted_result_sha256": {
            "Round179_attachment": DEPENDENCIES[f"{R179}_rows.json"],
            "Round179_certificate":
                DEPENDENCIES[f"{R179}_certificate.json"],
            "Round179_verification":
                DEPENDENCIES[f"{R179}_verification.json"],
            "Round216_certificate":
                DEPENDENCIES[f"{R216}_certificate.json"],
            "Round216_verification":
                DEPENDENCIES[f"{R216}_verification.json"],
            "Round217_certificate":
                DEPENDENCIES[f"{R217}_certificate.json"],
            "Round217_verification":
                DEPENDENCIES[f"{R217}_verification.json"],
        },
        "Round217_is_read_only_separate_Round208_trace_evidence": True,
        "Round217_rows_not_substituted_for_Round179_child_atlas": True,
    }


def expected_normals(
    attachment: dict[str, Any], origins: set[str],
) -> tuple[dict[str, dict[str, Any]], dict[str, list[tuple[str, str, str]]]]:
    specifications = (
        ("outgoing_normal_form_rows", "OUTGOING", 7_924),
        ("wall_normal_form_rows", "INTEGER_WALL", 4_896),
        ("source_chart_seam_rows", "SOURCE_CHART_SEAM", 264),
        ("pair_arrangement_candidate_rows", "PAIR_ARRANGEMENT_FRONTIER", 8),
    )
    expected: dict[str, dict[str, Any]] = {}
    by_origin: dict[str, list[tuple[str, str, str]]] = defaultdict(list)
    for table_name, kind, expected_count in specifications:
        columns = attachment["row_column_schemas"][table_name]
        selected = [
            packed for packed in attachment[table_name]
            if packed[columns.index("origin_row_id")] in origins
        ]
        need(len(selected) == expected_count, f"normal count:{table_name}")
        for packed in selected:
            source = dict(zip(columns, packed, strict=True))
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
                existence = classification == "FULL_BASE_UNIQUE_GRAPH"
            elif kind == "SOURCE_CHART_SEAM":
                equation = source["equation"]
                gradient_axis = source["gradient_axis"]
                gradient_sign = source["gradient_sign"]
                classification = source["face_classification"]
                dimension = source["exact_dimension"]
                existence = True
            else:
                equation = gradient_axis = gradient_sign = None
                classification = source["existence_certification"]
                dimension = source["candidate_pair_intersection_dimension"]
                existence = False
            normal_id = rid(
                "origin-normal-form", [table_name, source["row_id"], packed]
            )
            row = {
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
                "source_packed_row_sha256": h(packed),
                "source_packed_row": packed,
            }
            need(normal_id not in expected, "unique normal id")
            expected[normal_id] = row
            by_origin[source["origin_row_id"]].append(
                (normal_id, table_name, source["row_id"])
            )
    return expected, by_origin


def verify_full(
    certificate: dict[str, Any],
    entries: dict[str, dict[str, str]],
    docs: dict[str, Any],
) -> dict[str, Any]:
    need(
        set(certificate) == {"schema", "result", "result_sha256"}
        and certificate["schema"] == CANDIDATE_SCHEMA
        and certificate["result_sha256"] == RESULT_SHA
        and h(certificate["result"]) == RESULT_SHA,
        "candidate complete canonical envelope",
    )
    result = certificate["result"]
    need(
        set(result) == {
            "status", "formal_input_binding", "coordinate_boundary_atlas",
            "outgoing_wall_and_seam_normal_form_boundary_account",
            "per_key_coordinate_coverage_ledger",
            "Round216_boundary_blocker_delta", "strict_nonpromotion",
            "next_core_gate", "provenance",
        }
        and result["status"] == EXPECTED_STATUS
        and result["formal_input_binding"] == expected_binding(entries)
        and result["provenance"] == {
            "schema": CANDIDATE_SCHEMA,
            "producer_sha256": PRODUCER_SHA,
            "formal_input_files_modified": False,
        },
        "top-level complete Python-object fields",
    )
    attachment = docs[f"{R179}_rows.json"]["result"]
    origins = unpack(attachment, "origin_tube_rows")
    resolved = unpack(attachment, "resolved_3d_child_rows")
    retained = unpack(attachment, "retained_3d_child_rows")
    guards = unpack(attachment, "chart_guard_child_rows")
    need(
        (len(origins), len(resolved), len(retained), len(guards))
        == (62_012, 17_192, 106_680, 152),
        "Round179 table census",
    )
    origin_map = {row["origin_row_id"]: row for row in origins}
    all_children: dict[str, list[tuple[str, dict[str, Any]]]] = defaultdict(list)
    for kind, rows in (
        ("RESOLVED", resolved), ("RETAINED", retained), ("GUARD", guards)
    ):
        for row in rows:
            all_children[row["origin_row_id"]].append((kind, row))
    need(
        len(all_children) == 62_012
        and all(
            sorted(row["child_index"] for _kind, row in rows) == [0, 1]
            for rows in all_children.values()
        ),
        "one-step child partition",
    )
    resolved_origins = {row["origin_row_id"] for row in resolved}
    need(len(resolved_origins) == 13_076, "resolved origin count")
    normal_expected, normal_by_origin = expected_normals(
        attachment, resolved_origins
    )

    atlas = result["coordinate_boundary_atlas"]
    need(
        set(atlas) == {
            "scope", "canonical_half_open_convention", "tables",
            "headline_census", "parent_atlas_carrier_census",
        }
        and atlas["scope"]
        == "ALL_17192_PINNED_ROUND179_RESOLVED_CHILD_CLOSED_BOX_STRATA"
        and atlas["canonical_half_open_convention"] == {
            "box": "[t0,t1) x [p0,p1) x [s0,s1)",
            "face_incidence_included_iff_fixed_side": "LOWER",
            "edge_incidence_included_iff_both_fixed_sides": "LOWER",
            "corner_incidence_included_iff_all_fixed_sides": "LOWER",
            "closure_strata_recorded_even_when_half_open_excluded": True,
            "half_open_label_is_coordinate_ownership_not_physical_boundary":
                True,
        },
        "atlas header and half-open contract",
    )
    tables = atlas["tables"]
    need(
        set(tables) == {
            "resolved_child_rows", "coordinate_face_rows",
            "coordinate_edge_rows", "coordinate_corner_rows",
            "one_step_split_interface_rows",
            "formal_coordinate_adjacency_rows",
            "rejected_exact_coordinate_coincidence_rows",
        },
        "atlas exact table names",
    )
    child_rows = rows_as_dicts(tables["resolved_child_rows"], CHILD_COLUMNS)
    face_rows = rows_as_dicts(tables["coordinate_face_rows"], FACE_COLUMNS)
    edge_rows = rows_as_dicts(tables["coordinate_edge_rows"], EDGE_COLUMNS)
    corner_rows = rows_as_dicts(
        tables["coordinate_corner_rows"], CORNER_COLUMNS
    )
    split_rows = rows_as_dicts(
        tables["one_step_split_interface_rows"], SPLIT_COLUMNS
    )
    adjacency_rows = rows_as_dicts(
        tables["formal_coordinate_adjacency_rows"], ADJ_COLUMNS
    )
    rejected_rows = rows_as_dicts(
        tables["rejected_exact_coordinate_coincidence_rows"], REJECT_COLUMNS
    )
    need(
        (
            len(child_rows), len(face_rows), len(edge_rows), len(corner_rows),
            len(split_rows), len(adjacency_rows), len(rejected_rows),
        ) == (
            17_192, 103_152, 206_304, 137_536,
            13_076, 10_384, 9_830,
        ),
        "atlas row census",
    )

    children = sorted(resolved, key=lambda row: row["row_id"])
    child_by_ordinal = dict(enumerate(children))
    child_candidate = {
        row["source_child_row_id"]: row for row in child_rows
    }
    need(len(child_candidate) == 17_192, "unique candidate children")
    split_candidate = {row["origin_row_id"]: row for row in split_rows}
    need(len(split_candidate) == 13_076, "unique split origins")
    split_ids: dict[str, str] = {}
    key_counts: dict[int, Counter[str]] = defaultdict(Counter)
    key_ids: dict[int, set[str]] = defaultdict(set)

    for origin_id in sorted(resolved_origins):
        origin = origin_map[origin_id]
        siblings = sorted(
            all_children[origin_id], key=lambda item: item[1]["child_index"]
        )
        lower_kind, lower = siblings[0]
        upper_kind, upper = siblings[1]
        axis = AXES.index(origin["chosen_split_axis"])
        parent_box = box(origin["original_box"])
        midpoint = (
            parent_box[2 * axis] + parent_box[2 * axis + 1]
        ) / 2
        rectangle = rect(parent_box, axis)
        split_id = rid(
            "one-step-split-interface",
            [
                origin_id, origin["parent_id"], origin["chart"],
                AXES[axis], qs(midpoint), texts(rectangle),
            ],
        )
        split_ids[origin_id] = split_id
        resolved_count = int(lower_kind == "RESOLVED") + int(
            upper_kind == "RESOLVED"
        )
        retained_count = int(lower_kind == "RETAINED") + int(
            upper_kind == "RETAINED"
        )
        expected_split = {
            "split_interface_id": split_id,
            "origin_row_id": origin_id,
            "parent_id": origin["parent_id"],
            "chart": origin["chart"],
            "axis": AXES[axis],
            "fixed_coordinate": qs(midpoint),
            "tangential_half_open_box": texts(rectangle),
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
        }
        need(
            split_candidate.get(origin_id) == expected_split,
            "full split Python-object equality",
        )

    face_candidate = {row["face_id"]: row for row in face_rows}
    edge_candidate = {row["edge_id"]: row for row in edge_rows}
    corner_candidate = {row["corner_id"]: row for row in corner_rows}
    need(
        len(face_candidate) == 103_152
        and len(edge_candidate) == 206_304
        and len(corner_candidate) == 137_536,
        "unique coordinate stratum ids",
    )
    expected_face_ids: set[str] = set()
    expected_edge_ids: set[str] = set()
    expected_corner_ids: set[str] = set()
    face_local: dict[tuple[int, int, int], tuple[str, Q, tuple[Q, ...]]] = {}
    expected_reference_keys: set[tuple[int, str]] = set()

    for ordinal, child in enumerate(children):
        origin = origin_map[child["origin_row_id"]]
        axis = AXES.index(origin["chosen_split_axis"])
        parent_box = box(origin["original_box"])
        values = box(child["box"])
        midpoint = (
            parent_box[2 * axis] + parent_box[2 * axis + 1]
        ) / 2
        siblings = sorted(
            all_children[child["origin_row_id"]],
            key=lambda item: item[1]["child_index"],
        )
        sibling_kind, sibling = siblings[1 - child["child_index"]]
        split_side = "UPPER" if child["child_index"] == 0 else "LOWER"
        refs = normal_by_origin[child["origin_row_id"]]
        expected_child = {
            "atlas_child_id": rid(
                "resolved-child-atlas",
                [child["row_id"], child["box"], child["refinement_path"]],
            ),
            "source_child_row_id": child["row_id"],
            "origin_row_id": child["origin_row_id"],
            "parent_id": child["parent_id"],
            "chart": child["chart"],
            "child_index": child["child_index"],
            "refinement_path": child["refinement_path"],
            "box": texts(values),
            "coordinate_volume": child["coordinate_volume"],
            "chosen_split_axis": origin["chosen_split_axis"],
            "split_coordinate": qs(midpoint),
            "split_face_side": split_side,
            "split_sibling_kind": sibling_kind,
            "split_sibling_row_id": sibling["row_id"],
            "owner_target": child["owner_target"],
            "official_key_ordinal": child["official_key_ordinal"],
            "official_key_id": child["official_key_id"],
            "face_count": 6,
            "edge_count": 12,
            "corner_count": 8,
            "origin_normal_form_reference_count": len(refs),
            "event_sheet_incidence_count": 0,
            "cross_chart_glue_count": 0,
            "coordinate_boundary_atlas_complete": True,
            "whole_origin_credit": 0,
            "physical_component_credit": 0,
            "global_exact_key_disposition_credit": 0,
        }
        need(
            child_candidate.get(child["row_id"]) == expected_child,
            "full child Python-object equality",
        )
        key = child["official_key_ordinal"]
        counts = key_counts[key]
        key_ids[key].add(child["official_key_id"])
        counts["children"] += 1
        counts["normal_refs"] += len(refs)
        if sibling_kind == "RETAINED":
            counts["resolved_retained"] += 1
        for normal_id, _table_name, _source_id in refs:
            expected_reference_keys.add((ordinal, normal_id))

        for face_axis in range(3):
            tangent = [candidate for candidate in range(3)
                       if candidate != face_axis]
            rectangle = rect(values, face_axis)
            for side in range(2):
                fixed = values[2 * face_axis + side]
                face_id = rid(
                    "coordinate-face",
                    [
                        child["row_id"], AXES[face_axis], SIDES[side],
                        qs(fixed), texts(rectangle),
                    ],
                )
                is_split = (
                    face_axis == axis and SIDES[side] == split_side
                    and fixed == midpoint
                )
                expected_face = {
                    "face_id": face_id,
                    "child_ordinal": ordinal,
                    "source_child_row_id": child["row_id"],
                    "parent_id": child["parent_id"],
                    "chart": child["chart"],
                    "axis": AXES[face_axis],
                    "side": SIDES[side],
                    "fixed_coordinate": qs(fixed),
                    "tangential_axes": [AXES[value] for value in tangent],
                    "tangential_half_open_box": texts(rectangle),
                    "carrier_id": rid(
                        "parent-face-carrier",
                        [
                            child["parent_id"], child["chart"],
                            AXES[face_axis], qs(fixed), texts(rectangle),
                        ],
                    ),
                    "closure_dimension": 2,
                    "half_open_incidence_status": (
                        "INCLUDED_LOWER_FIXED_COORDINATE"
                        if side == 0
                        else "EXCLUDED_UPPER_FIXED_COORDINATE"
                    ),
                    "origin_boundary_role": (
                        "ONE_STEP_INTERNAL_SPLIT_FACE" if is_split
                        else "INHERITED_ORIGIN_BOX_BOUNDARY_FACE"
                    ),
                    "one_step_split_interface_id": (
                        split_ids[child["origin_row_id"]] if is_split else None
                    ),
                    "event_sheet_incidence_count": 0,
                    "coordinate_stratum_only": True,
                    "physical_glue_credit": 0,
                    "global_exact_key_disposition_credit": 0,
                }
                need(
                    face_candidate.get(face_id) == expected_face,
                    "full face Python-object equality",
                )
                expected_face_ids.add(face_id)
                face_local[(ordinal, face_axis, side)] = (
                    face_id, fixed, rectangle
                )
                counts["faces"] += 1

        for first_axis in range(3):
            for second_axis in range(first_axis + 1, 3):
                free_axis = 3 - first_axis - second_axis
                for first_side in range(2):
                    for second_side in range(2):
                        fixed = [
                            qs(values[2 * first_axis + first_side]),
                            qs(values[2 * second_axis + second_side]),
                        ]
                        interval = [
                            qs(values[2 * free_axis]),
                            qs(values[2 * free_axis + 1]),
                        ]
                        edge_id = rid(
                            "coordinate-edge",
                            [
                                child["row_id"],
                                [AXES[first_axis], AXES[second_axis]],
                                [SIDES[first_side], SIDES[second_side]],
                                fixed, AXES[free_axis], interval,
                            ],
                        )
                        meets_split = (
                            first_axis == axis
                            and SIDES[first_side] == split_side
                            and values[2 * first_axis + first_side] == midpoint
                        ) or (
                            second_axis == axis
                            and SIDES[second_side] == split_side
                            and values[2 * second_axis + second_side] == midpoint
                        )
                        expected_edge = {
                            "edge_id": edge_id,
                            "child_ordinal": ordinal,
                            "source_child_row_id": child["row_id"],
                            "parent_id": child["parent_id"],
                            "chart": child["chart"],
                            "fixed_axes":
                                [AXES[first_axis], AXES[second_axis]],
                            "fixed_sides":
                                [SIDES[first_side], SIDES[second_side]],
                            "fixed_coordinates": fixed,
                            "free_axis": AXES[free_axis],
                            "free_half_open_interval": interval,
                            "carrier_id": rid(
                                "parent-edge-carrier",
                                [
                                    child["parent_id"], child["chart"],
                                    [AXES[first_axis], AXES[second_axis]],
                                    fixed, AXES[free_axis], interval,
                                ],
                            ),
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
                        }
                        need(
                            edge_candidate.get(edge_id) == expected_edge,
                            "full edge Python-object equality",
                        )
                        expected_edge_ids.add(edge_id)
                        counts["edges"] += 1

        for t_side in range(2):
            for p_side in range(2):
                for s_side in range(2):
                    side_values = [t_side, p_side, s_side]
                    coordinate = [
                        qs(values[2 * coordinate_axis
                                  + side_values[coordinate_axis]])
                        for coordinate_axis in range(3)
                    ]
                    corner_id = rid(
                        "coordinate-corner",
                        [
                            child["row_id"],
                            [SIDES[value] for value in side_values],
                            coordinate,
                        ],
                    )
                    expected_corner = {
                        "corner_id": corner_id,
                        "child_ordinal": ordinal,
                        "source_child_row_id": child["row_id"],
                        "parent_id": child["parent_id"],
                        "chart": child["chart"],
                        "sides": [SIDES[value] for value in side_values],
                        "coordinate": coordinate,
                        "carrier_id": rid(
                            "parent-corner-carrier",
                            [child["parent_id"], child["chart"], coordinate],
                        ),
                        "closure_dimension": 0,
                        "half_open_incidence_status": (
                            "INCLUDED_ALL_FIXED_COORDINATES_LOWER"
                            if side_values == [0, 0, 0]
                            else "EXCLUDED_AT_LEAST_ONE_FIXED_COORDINATE_UPPER"
                        ),
                        "meets_one_step_split_interface": (
                            SIDES[side_values[axis]] == split_side
                            and values[2 * axis + side_values[axis]] == midpoint
                        ),
                        "event_sheet_incidence_count": 0,
                        "coordinate_stratum_only": True,
                        "physical_glue_credit": 0,
                        "global_exact_key_disposition_credit": 0,
                    }
                    need(
                        corner_candidate.get(corner_id) == expected_corner,
                        "full corner Python-object equality",
                    )
                    expected_corner_ids.add(corner_id)
                    counts["corners"] += 1
    need(
        expected_face_ids == set(face_candidate)
        and expected_edge_ids == set(edge_candidate)
        and expected_corner_ids == set(corner_candidate),
        "no deleted or inserted atlas stratum row",
    )

    normal_account = result[
        "outgoing_wall_and_seam_normal_form_boundary_account"
    ]
    need(
        set(normal_account) == {
            "tables", "relevant_origin_normal_form_count",
            "resolved_child_normal_form_reference_count",
            "normal_form_kind_count",
            "materialized_event_sheet_row_count_on_resolved_children",
            "materialized_event_sheet_incidence_count_on_resolved_children",
            "formal_reason",
            "origin_normal_forms_are_not_claimed_to_be_clipped_sheets_on_the_retained_sibling",
            "pair_arrangement_equations_or_isolation_not_invented",
        },
        "normal account keys",
    )
    normal_tables = normal_account["tables"]
    need(
        set(normal_tables) == {
            "relevant_origin_normal_form_rows",
            "resolved_child_normal_form_reference_rows",
        },
        "normal table names",
    )
    normal_rows = rows_as_dicts(
        normal_tables["relevant_origin_normal_form_rows"], NORMAL_COLUMNS
    )
    reference_rows = rows_as_dicts(
        normal_tables["resolved_child_normal_form_reference_rows"], REF_COLUMNS
    )
    normal_candidate = {row["normal_form_id"]: row for row in normal_rows}
    need(
        len(normal_candidate) == 13_092
        and normal_candidate == normal_expected,
        "full normal-form Python-object equality",
    )
    reference_candidate = {
        (row["child_ordinal"], row["normal_form_id"]): row
        for row in reference_rows
    }
    need(
        len(reference_candidate) == len(reference_rows) == 17_208
        and set(reference_candidate) == expected_reference_keys,
        "complete normal-reference key set",
    )
    for key, row in reference_candidate.items():
        child_ordinal, normal_id = key
        normal = normal_expected[normal_id]
        child = children[child_ordinal]
        expected_reference = {
            "reference_id": rid(
                "resolved-child-normal-form-reference",
                [child["row_id"], normal_id],
            ),
            "child_ordinal": child_ordinal,
            "source_child_row_id": child["row_id"],
            "normal_form_id": normal_id,
            "source_table": normal["source_table"],
            "source_row_id": normal["source_row_id"],
            "resolved_child_closed_enclosure_status":
                "STRICT_DYNAMIC_SIGNATURE__EVENT_ZERO_SET_ABSENT",
            "event_sheet_incidence_count": 0,
            "event_trace_glue_count": 0,
            "proof_basis":
                "PINNED_ROUND179_RESOLVED_BUILD_REQUIRES_DYNAMIC_SIGNATURE_STRICT_ON_CLOSED_INTERVAL_ENCLOSURE",
            "physical_component_credit": 0,
            "global_exact_key_disposition_credit": 0,
        }
        need(row == expected_reference, "full normal-reference equality")

    planes: dict[
        tuple[str, str, int, Q],
        list[list[tuple[int, tuple[Q, ...]]]],
    ] = defaultdict(lambda: [[], []])
    raw_carriers: dict[
        tuple[int, Q, tuple[Q, ...]], list[list[int]],
    ] = defaultdict(lambda: [[], []])
    for (ordinal, axis, side), (_face_id, fixed, rectangle) in (
        face_local.items()
    ):
        child = children[ordinal]
        planes[(child["parent_id"], child["chart"], axis, fixed)][side].append(
            (ordinal, rectangle)
        )
        raw_carriers[(axis, fixed, rectangle)][side].append(ordinal)

    adjacency_candidate = {
        row["coordinate_adjacency_id"]: row for row in adjacency_rows
    }
    expected_adjacency_ids: set[str] = set()
    adjacency_class: Counter[str] = Counter()
    for (parent_id, chart, axis, fixed), sides in planes.items():
        for positive_ordinal, positive_rect in sides[0]:
            for negative_ordinal, negative_rect in sides[1]:
                common = (
                    max(positive_rect[0], negative_rect[0]),
                    min(positive_rect[1], negative_rect[1]),
                    max(positive_rect[2], negative_rect[2]),
                    min(positive_rect[3], negative_rect[3]),
                )
                if common[0] >= common[1] or common[2] >= common[3]:
                    continue
                positive = children[positive_ordinal]
                negative = children[negative_ordinal]
                need(
                    positive["official_key_id"] == negative["official_key_id"],
                    "same-parent coordinate adjacency key equality",
                )
                exact = positive_rect == negative_rect
                same_origin = (
                    positive["origin_row_id"] == negative["origin_row_id"]
                )
                relation = (
                    "SAME_ORIGIN_EXACT_ONE_STEP_SPLIT"
                    if same_origin else (
                        "CROSS_ORIGIN_EXACT_SHARED_PARENT_FACE"
                        if exact else
                        "CROSS_ORIGIN_POSITIVE_AREA_PARENT_COMMON_REFINEMENT"
                    )
                )
                common_id = rid(
                    "parent-face-common-refinement",
                    [
                        parent_id, chart, AXES[axis], qs(fixed),
                        texts(common),
                    ],
                )
                negative_face = face_local[(negative_ordinal, axis, 1)][0]
                positive_face = face_local[(positive_ordinal, axis, 0)][0]
                adjacency_id = rid(
                    "coordinate-adjacency",
                    [common_id, negative_face, positive_face],
                )
                expected_adjacency = {
                    "coordinate_adjacency_id": adjacency_id,
                    "common_refinement_id": common_id,
                    "parent_id": parent_id,
                    "chart": chart,
                    "axis": AXES[axis],
                    "fixed_coordinate": qs(fixed),
                    "common_refinement_half_open_box": texts(common),
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
                need(
                    adjacency_candidate.get(adjacency_id)
                    == expected_adjacency,
                    "full parent/chart/key/common-refinement adjacency equality",
                )
                expected_adjacency_ids.add(adjacency_id)
                adjacency_class[relation] += 1
                counts = key_counts[negative["official_key_ordinal"]]
                counts["adjacencies"] += 1
                counts[
                    "exact_adjacencies" if exact else "partial_adjacencies"
                ] += 1
    need(
        expected_adjacency_ids == set(adjacency_candidate)
        and adjacency_class == {
            "SAME_ORIGIN_EXACT_ONE_STEP_SPLIT": 4_116,
            "CROSS_ORIGIN_EXACT_SHARED_PARENT_FACE": 5_900,
            "CROSS_ORIGIN_POSITIVE_AREA_PARENT_COMMON_REFINEMENT": 368,
        },
        "no cross-parent fake or deleted adjacency",
    )

    rejected_candidate = {row["candidate_id"]: row for row in rejected_rows}
    expected_rejected_ids: set[str] = set()
    rejected_class: Counter[tuple[bool, bool]] = Counter()
    for (axis, fixed, rectangle), sides in raw_carriers.items():
        for positive_ordinal in sides[0]:
            for negative_ordinal in sides[1]:
                positive = children[positive_ordinal]
                negative = children[negative_ordinal]
                if positive["parent_id"] == negative["parent_id"]:
                    continue
                negative_face = face_local[(negative_ordinal, axis, 1)][0]
                positive_face = face_local[(positive_ordinal, axis, 0)][0]
                candidate_id = rid(
                    "rejected-coordinate-coincidence",
                    [negative_face, positive_face],
                )
                same_chart = negative["chart"] == positive["chart"]
                same_key = (
                    negative["official_key_id"] == positive["official_key_id"]
                )
                expected_rejected = {
                    "candidate_id": candidate_id,
                    "axis": AXES[axis],
                    "fixed_coordinate": qs(fixed),
                    "coincident_half_open_box": texts(rectangle),
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
                }
                need(
                    rejected_candidate.get(candidate_id) == expected_rejected,
                    "full rejected cross-parent coincidence equality",
                )
                expected_rejected_ids.add(candidate_id)
                rejected_class[(same_chart, same_key)] += 1
    need(
        expected_rejected_ids == set(rejected_candidate)
        and rejected_class == {(True, True): 328, (False, False): 9_502},
        "complete rejected cross-parent frontier",
    )

    key_rows = rows_as_dicts(
        result["per_key_coordinate_coverage_ledger"], KEY_COLUMNS
    )
    key_candidate = {row["official_key_ordinal"]: row for row in key_rows}
    need(len(key_candidate) == len(key_rows) == 116, "116 unique key rows")
    for key in sorted(key_counts):
        need(len(key_ids[key]) == 1, "one id per ordinal")
        counts = key_counts[key]
        expected_key = {
            "official_key_ordinal": key,
            "official_key_id": next(iter(key_ids[key])),
            "resolved_child_count": counts["children"],
            "face_count": counts["faces"],
            "edge_count": counts["edges"],
            "corner_count": counts["corners"],
            "formal_coordinate_adjacency_count": counts["adjacencies"],
            "exact_full_face_adjacency_count": counts["exact_adjacencies"],
            "partial_common_refinement_adjacency_count":
                counts["partial_adjacencies"],
            "one_step_resolved_retained_frontier_count":
                counts["resolved_retained"],
            "origin_normal_form_reference_count": counts["normal_refs"],
            "event_sheet_incidence_count": 0,
            "cross_chart_glue_count": 0,
            "coordinate_boundary_atlas_complete": True,
            "global_exact_key_fibre_exhausted": False,
            "whole_origin_credit": 0,
            "physical_component_credit": 0,
            "global_exact_key_disposition_credit": 0,
        }
        need(
            key_candidate.get(key) == expected_key,
            "full per-key Python-object equality",
        )
    need(set(key_candidate) == set(key_counts), "complete key set")

    face_carriers = Counter(row["carrier_id"] for row in face_rows)
    edge_carriers = Counter(row["carrier_id"] for row in edge_rows)
    corner_carriers = Counter(row["carrier_id"] for row in corner_rows)
    need(
        atlas["headline_census"] == {
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
        }
        and atlas["parent_atlas_carrier_census"] == {
            "face_carrier_count": 93_136,
            "face_incidence_multiplicity_histogram":
                {"1": 83_120, "2": 10_016},
            "edge_carrier_count": 166_528,
            "edge_incidence_multiplicity_histogram":
                {"1": 130_388, "2": 33_976, "3": 692, "4": 1_472},
            "corner_carrier_count": 96_612,
            "corner_incidence_multiplicity_histogram": {
                "1": 63_560, "2": 28_364, "3": 1_564,
                "4": 3_092, "5": 4, "6": 28,
            },
        }
        and Counter(face_carriers.values()) == {1: 83_120, 2: 10_016}
        and Counter(edge_carriers.values())
        == {1: 130_388, 2: 33_976, 3: 692, 4: 1_472}
        and Counter(corner_carriers.values())
        == {1: 63_560, 2: 28_364, 3: 1_564, 4: 3_092, 5: 4, 6: 28},
        "headline and carrier object equality",
    )
    need(
        normal_account["relevant_origin_normal_form_count"] == 13_092
        and normal_account[
            "resolved_child_normal_form_reference_count"
        ] == 17_208
        and normal_account["normal_form_kind_count"] == {
            "INTEGER_WALL": 4_896, "OUTGOING": 7_924,
            "PAIR_ARRANGEMENT_FRONTIER": 8, "SOURCE_CHART_SEAM": 264,
        }
        and normal_account[
            "materialized_event_sheet_row_count_on_resolved_children"
        ] == 0
        and normal_account[
            "materialized_event_sheet_incidence_count_on_resolved_children"
        ] == 0
        and normal_account["formal_reason"]
        == (
            "PINNED_ROUND179_RESOLVED_CHILDREN_REQUIRE_A_STRICT_DYNAMIC_"
            "SIGNATURE_ON_THE_CLOSED_INTERVAL_ENCLOSURE; THE_ORIGIN_EVENT_"
            "ZERO_SETS_THEREFORE_HAVE_ZERO_CHILD_INCIDENCE"
        )
        and normal_account[
            "origin_normal_forms_are_not_claimed_to_be_clipped_sheets_on_the_retained_sibling"
        ] is True
        and normal_account[
            "pair_arrangement_equations_or_isolation_not_invented"
        ] is True,
        "complete normal account object equality",
    )
    need(
        result["Round216_boundary_blocker_delta"] == {
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
        }
        and result["strict_nonpromotion"] == {
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
        }
        and result["next_core_gate"]
        == (
            "derive explicit cross-parent/cross-chart transition identities "
            "and exact event-trace restrictions before any physical-component "
            "quotient; then combine with the still-open Round217 endpoint-to-"
            "interior and partial-face frontiers"
        ),
        "blocker, nonpromotion, next gate object equality",
    )
    return {
        "full_candidate_Python_object_field_equality": True,
        "full_canonical_result_equality": True,
        "resolved_children": 17_192,
        "faces": 103_152,
        "edges": 206_304,
        "corners": 137_536,
        "split_interfaces": 13_076,
        "coordinate_adjacencies": 10_384,
        "rejected_coordinate_coincidences": 9_830,
        "normal_forms": 13_092,
        "normal_references": 17_208,
        "keys": 116,
    }


def signed_snapshot(values: dict[str, Any]) -> dict[str, Any]:
    body = {key: value for key, value in values.items() if key != "sha256"}
    return {**body, "sha256": h(body)}


def verify_snapshot(row: dict[str, Any]) -> None:
    expected_keys = {
        "parent_id_equal", "chart_equal", "key_equal",
        "face_lower_owner", "face_upper_excluded",
        "edge_both_lower_owner", "corner_all_lower_owner",
        "cross_parent_adjacency_credit", "box_touch_only_credit",
        "face_rows", "edge_rows", "corner_rows", "exact_adjacencies",
        "partial_adjacencies", "rejected_cross_parent",
        "event_sheet_incidences", "physical_credit", "global_credit",
        "dispositions", "D02", "Gate5", "CM2", "sha256",
    }
    need(set(row) == expected_keys, "snapshot keys")
    body = {key: value for key, value in row.items() if key != "sha256"}
    need(row["sha256"] == h(body), "snapshot signature")
    need(
        row["parent_id_equal"] and row["chart_equal"] and row["key_equal"]
        and row["face_lower_owner"] and row["face_upper_excluded"]
        and row["edge_both_lower_owner"] and row["corner_all_lower_owner"]
        and row["cross_parent_adjacency_credit"] == 0
        and row["box_touch_only_credit"] == 0
        and row["face_rows"] == 103_152
        and row["edge_rows"] == 206_304
        and row["corner_rows"] == 137_536
        and row["exact_adjacencies"] == 10_016
        and row["partial_adjacencies"] == 368
        and row["rejected_cross_parent"] == 9_830
        and row["event_sheet_incidences"] == 0
        and row["physical_credit"] == 0 and row["global_credit"] == 0
        and row["dispositions"] == "0/224580"
        and row["D02"] == "BLOCKED" and row["Gate5"] == "10/18"
        and row["CM2"] == "NO-GO_FOR_CLAIM",
        "snapshot semantics",
    )


def snapshot_attacks() -> dict[str, int]:
    base = signed_snapshot({
        "parent_id_equal": True,
        "chart_equal": True,
        "key_equal": True,
        "face_lower_owner": True,
        "face_upper_excluded": True,
        "edge_both_lower_owner": True,
        "corner_all_lower_owner": True,
        "cross_parent_adjacency_credit": 0,
        "box_touch_only_credit": 0,
        "face_rows": 103_152,
        "edge_rows": 206_304,
        "corner_rows": 137_536,
        "exact_adjacencies": 10_016,
        "partial_adjacencies": 368,
        "rejected_cross_parent": 9_830,
        "event_sheet_incidences": 0,
        "physical_credit": 0,
        "global_credit": 0,
        "dispositions": "0/224580",
        "D02": "BLOCKED",
        "Gate5": "10/18",
        "CM2": "NO-GO_FOR_CLAIM",
    })
    mutations = [
        ("parent_id_equal", False), ("chart_equal", False),
        ("key_equal", False), ("face_lower_owner", False),
        ("face_upper_excluded", False), ("edge_both_lower_owner", False),
        ("corner_all_lower_owner", False),
        ("cross_parent_adjacency_credit", 1), ("box_touch_only_credit", 1),
        ("face_rows", 103_151), ("face_rows", 103_153),
        ("edge_rows", 206_303), ("corner_rows", 137_535),
        ("exact_adjacencies", 10_015), ("partial_adjacencies", 367),
        ("rejected_cross_parent", 9_829), ("event_sheet_incidences", 1),
        ("physical_credit", 1), ("global_credit", 1),
        ("dispositions", "1/224580"), ("D02", "CLEARED"),
        ("Gate5", "11/18"), ("CM2", "GO"),
    ]
    rejected = 0
    for key, value in mutations:
        attacked = dict(base)
        attacked[key] = value
        attacked = signed_snapshot(attacked)
        try:
            verify_snapshot(attacked)
        except VError:
            rejected += 1
    need(rejected == len(mutations), "resigned semantic attacks")
    unsigned = dict(base)
    unsigned["face_rows"] -= 1
    try:
        verify_snapshot(unsigned)
    except VError:
        rejected += 1
    need(rejected == len(mutations) + 1, "unsigned attack")
    return {
        "truly_resigned_semantic_attacks_rejected": len(mutations),
        "unsigned_attacks_rejected": 1,
        "total_rejected": rejected,
    }


def resign_table(table: dict[str, Any]) -> None:
    table["row_count"] = len(table["rows"])
    table["rows_sha256"] = h(table["rows"])
    table["row_ids_sha256"] = h([row[0] for row in table["rows"]])


def actual_candidate_attacks(
    certificate: dict[str, Any], attachment: dict[str, Any],
) -> dict[str, Any]:
    """Mutate, fully re-sign, and semantically reject the real candidate."""
    result = certificate["result"]
    atlas_tables = result["coordinate_boundary_atlas"]["tables"]
    child_table = atlas_tables["resolved_child_rows"]
    face_table = atlas_tables["coordinate_face_rows"]
    adjacency_table = atlas_tables["formal_coordinate_adjacency_rows"]
    rejected_table = atlas_tables[
        "rejected_exact_coordinate_coincidence_rows"
    ]
    source_children = {
        row["row_id"]: row
        for row in unpack(attachment, "resolved_3d_child_rows")
    }
    ordered_children = sorted(
        source_children.values(), key=lambda row: row["row_id"]
    )
    rejected = 0
    labels: list[str] = []

    def signed_rejection(
        label: str,
        table: dict[str, Any] | None,
        mutate: Any,
        restore: Any,
        guard: Any,
    ) -> None:
        nonlocal rejected
        old_metadata = None
        if table is not None:
            old_metadata = (
                table["row_count"], table["rows_sha256"],
                table["row_ids_sha256"],
            )
        mutate()
        if table is not None:
            resign_table(table)
            need(
                table["row_count"] == len(table["rows"])
                and table["rows_sha256"] == h(table["rows"])
                and table["row_ids_sha256"]
                == h([row[0] for row in table["rows"]]),
                f"actual attack table fully resigned:{label}",
            )
        certificate["result_sha256"] = h(result)
        need(
            certificate["result_sha256"] == h(result),
            f"actual attack envelope fully resigned:{label}",
        )
        try:
            guard()
        except VError:
            rejected += 1
            labels.append(label)
        else:
            raise VError(f"actual resigned attack accepted:{label}")
        restore()
        if table is not None:
            assert old_metadata is not None
            (
                table["row_count"], table["rows_sha256"],
                table["row_ids_sha256"],
            ) = old_metadata
        certificate["result_sha256"] = RESULT_SHA

    child_row = child_table["rows"][0]
    child_source = source_children[child_row[1]]
    old_child_key = child_row[16]
    signed_rejection(
        "REAL_CHILD_OFFICIAL_KEY_ID",
        child_table,
        lambda: child_row.__setitem__(16, "gate5-word:fake"),
        lambda: child_row.__setitem__(16, old_child_key),
        lambda: need(
            child_row[16] == child_source["official_key_id"],
            "child source key equality",
        ),
    )

    face_row = face_table["rows"][0]
    face_source = source_children[face_row[2]]
    old_face_parent = face_row[3]
    signed_rejection(
        "REAL_FACE_PARENT_ID",
        face_table,
        lambda: face_row.__setitem__(3, "round174-gate3-parent:fake"),
        lambda: face_row.__setitem__(3, old_face_parent),
        lambda: need(
            face_row[3] == face_source["parent_id"],
            "face source parent equality",
        ),
    )
    old_face_chart = face_row[4]
    signed_rejection(
        "REAL_FACE_CHART",
        face_table,
        lambda: face_row.__setitem__(4, "G:FAKE"),
        lambda: face_row.__setitem__(4, old_face_chart),
        lambda: need(
            face_row[4] == face_source["chart"],
            "face source chart equality",
        ),
    )
    old_owner = face_row[12]
    wrong_owner = (
        "EXCLUDED_UPPER_FIXED_COORDINATE"
        if face_row[6] == "LOWER"
        else "INCLUDED_LOWER_FIXED_COORDINATE"
    )
    signed_rejection(
        "REAL_FACE_HALF_OPEN_OWNER",
        face_table,
        lambda: face_row.__setitem__(12, wrong_owner),
        lambda: face_row.__setitem__(12, old_owner),
        lambda: need(
            face_row[12] == (
                "INCLUDED_LOWER_FIXED_COORDINATE"
                if face_row[6] == "LOWER"
                else "EXCLUDED_UPPER_FIXED_COORDINATE"
            ),
            "face half-open owner",
        ),
    )

    adjacency_row = adjacency_table["rows"][0]
    old_adjacency_parent = adjacency_row[2]
    negative_parent = ordered_children[adjacency_row[9]]["parent_id"]
    positive_parent = ordered_children[adjacency_row[10]]["parent_id"]
    need(
        negative_parent == positive_parent == old_adjacency_parent,
        "baseline adjacency parent",
    )
    signed_rejection(
        "REAL_ACCEPTED_ADJACENCY_CROSS_PARENT_FORGERY",
        adjacency_table,
        lambda: adjacency_row.__setitem__(
            2, "round174-gate3-parent:cross-parent-fake"
        ),
        lambda: adjacency_row.__setitem__(2, old_adjacency_parent),
        lambda: need(
            adjacency_row[2] == negative_parent == positive_parent,
            "accepted adjacency identical parent",
        ),
    )

    rejected_row = rejected_table["rows"][0]
    old_cross_parent_credit = rejected_row[13]
    signed_rejection(
        "REAL_REJECTED_CROSS_PARENT_ADJACENCY_CREDIT",
        rejected_table,
        lambda: rejected_row.__setitem__(13, 1),
        lambda: rejected_row.__setitem__(13, old_cross_parent_credit),
        lambda: need(
            rejected_row[6] != rejected_row[7]
            and rejected_row[13] == 0,
            "cross-parent coincidence remains rejected",
        ),
    )

    removed_face: list[Any] = []
    signed_rejection(
        "REAL_DELETE_ATLAS_FACE_ROW",
        face_table,
        lambda: removed_face.append(face_table["rows"].pop()),
        lambda: face_table["rows"].append(removed_face.pop()),
        lambda: need(
            len(face_table["rows"]) == 103_152
            and len({row[0] for row in face_table["rows"]}) == 103_152,
            "complete face atlas",
        ),
    )
    signed_rejection(
        "REAL_DUPLICATE_ATLAS_FACE_ROW",
        face_table,
        lambda: face_table["rows"].append(face_table["rows"][0]),
        lambda: face_table["rows"].pop(),
        lambda: need(
            len(face_table["rows"]) == 103_152
            and len({row[0] for row in face_table["rows"]}) == 103_152,
            "unique face atlas",
        ),
    )

    nonpromotion = result["strict_nonpromotion"]
    old_global_credit = nonpromotion["global_exact_key_disposition_credit"]
    signed_rejection(
        "REAL_GLOBAL_DISPOSITION_CREDIT",
        None,
        lambda: nonpromotion.__setitem__(
            "global_exact_key_disposition_credit", 1
        ),
        lambda: nonpromotion.__setitem__(
            "global_exact_key_disposition_credit", old_global_credit
        ),
        lambda: need(
            nonpromotion["global_exact_key_disposition_credit"] == 0,
            "zero global disposition credit",
        ),
    )
    old_dispositions = nonpromotion["source_G_global_exact_key_dispositions"]
    signed_rejection(
        "REAL_GLOBAL_DISPOSITION_COUNT",
        None,
        lambda: nonpromotion.__setitem__(
            "source_G_global_exact_key_dispositions", "1/224580"
        ),
        lambda: nonpromotion.__setitem__(
            "source_G_global_exact_key_dispositions", old_dispositions
        ),
        lambda: need(
            nonpromotion["source_G_global_exact_key_dispositions"]
            == "0/224580",
            "zero global dispositions",
        ),
    )
    need(
        rejected == 10 and h(result) == RESULT_SHA
        and certificate["result_sha256"] == RESULT_SHA,
        "actual candidate restored after attacks",
    )
    return {
        "actual_candidate_envelope_truly_resigned_attacks_attempted": 10,
        "actual_candidate_envelope_truly_resigned_attacks_rejected": rejected,
        "representative_classes": labels,
        "old_signature_was_not_the_rejection_reason": True,
        "affected_table_summaries_and_complete_result_SHA_recomputed": True,
    }


def json_attacks() -> dict[str, int]:
    attacks = [
        b'{"a":1,"a":2}', b'{"a":1.0}', b'{"a":NaN}',
        b'{"a":Infinity}', b'{"a":-Infinity}', b'[]', b'null',
        b'true', b'1', b'{"a":1} tail', b'{', b'', b'{"a":01}',
        b'{"a":+1}', b'\xff',
    ]
    rejected = 0
    for raw in attacks:
        try:
            decode(raw)
        except (VError, UnicodeDecodeError, json.JSONDecodeError):
            rejected += 1
    need(rejected == len(attacks), "JSON attacks")
    return {"attempted": len(attacks), "rejected": rejected}


def validate_candidate(path: Path) -> Path:
    need(not any(part == ".." for part in path.parts), "candidate alias")
    absolute = Path(os.path.abspath(os.fspath(path)))
    need(
        absolute.parent == HERE and absolute.parent.resolve() == HERE,
        "candidate exact parent",
    )
    need(
        absolute.name == CANDIDATE.name
        or (
            absolute.name.startswith(".cm2_round220_")
            and absolute.name.endswith("_certificate.json")
        ),
        "candidate allowlist",
    )
    need(
        absolute.resolve(strict=False) not in {
            PRODUCER.resolve(), Path(__file__).resolve()
        },
        "candidate protected",
    )
    return absolute


def validate_output(path: Path) -> Path:
    need(not any(part == ".." for part in path.parts), "output alias")
    absolute = Path(os.path.abspath(os.fspath(path)))
    need(
        absolute.parent == HERE and absolute.parent.resolve() == HERE,
        "output exact parent",
    )
    need(
        absolute.name == OUTPUT.name
        or (
            absolute.name.startswith(".cm2_round220_")
            and absolute.name.endswith("_verification.json")
        ),
        "output allowlist",
    )
    protected = {
        PRODUCER.resolve(), CANDIDATE.resolve(), Path(__file__).resolve(),
        *((HERE / values[0]).resolve() for values in MANIFESTS.values()),
    }
    need(absolute.resolve(strict=False) not in protected, "output protected")
    if absolute.exists() or absolute.is_symlink():
        metadata = absolute.lstat()
        need(
            stat.S_ISREG(metadata.st_mode) and not absolute.is_symlink()
            and metadata.st_nlink == 1,
            "existing output secure",
        )
    return absolute


def path_attacks() -> dict[str, int]:
    candidate_paths = [
        HERE / ".." / CANDIDATE.name, HERE.parent / CANDIDATE.name,
        HERE / "wrong_certificate.json",
        HERE / ".cm2_round219_x_certificate.json",
        HERE / ".cm2_round220_x_verification.json",
        Path("/tmp") / CANDIDATE.name,
        Path(".") / ".." / CANDIDATE.name, PRODUCER,
    ]
    output_paths = [
        HERE / ".." / OUTPUT.name, HERE.parent / OUTPUT.name,
        HERE / "wrong_verification.json",
        HERE / ".cm2_round219_x_verification.json",
        HERE / ".cm2_round220_x_certificate.json",
        Path("/tmp") / OUTPUT.name, Path(".") / ".." / OUTPUT.name,
        PRODUCER, CANDIDATE, Path(__file__).resolve(),
        HERE / MANIFESTS[R179][0], HERE / MANIFESTS[R216][0],
        HERE / MANIFESTS[R217][0],
    ]
    rejected = 0
    for candidate_path in candidate_paths:
        try:
            validate_candidate(candidate_path)
        except VError:
            rejected += 1
    for output_path in output_paths:
        try:
            validate_output(output_path)
        except VError:
            rejected += 1
    attempted = len(candidate_paths) + len(output_paths)
    need(rejected == attempted, "static path attacks")

    attack_dir = Path(tempfile.mkdtemp(prefix=".round220-parent-link-", dir=HERE))
    parent_link = attack_dir / "linked-parent"
    try:
        parent_link.symlink_to(HERE, target_is_directory=True)
        try:
            validate_candidate(parent_link / CANDIDATE.name)
        except VError:
            rejected += 1
        try:
            validate_output(parent_link / OUTPUT.name)
        except VError:
            rejected += 1
    finally:
        if parent_link.is_symlink():
            parent_link.unlink()
        attack_dir.rmdir()
    attempted += 2
    need(rejected == attempted, "parent symlink path attacks")

    token = f"{os.getpid()}-{next(tempfile._get_candidate_names())}"
    hostile_dir = Path(tempfile.mkdtemp(prefix=".round220-file-objects-", dir=HERE))

    def candidate_object_rejected(path: Path) -> None:
        nonlocal rejected
        try:
            secure_bytes(validate_candidate(path))
        except (VError, OSError):
            rejected += 1

    def output_object_rejected(path: Path) -> None:
        nonlocal rejected
        try:
            validate_output(path)
        except (VError, OSError):
            rejected += 1

    def remove_object(path: Path) -> None:
        if not path.exists() and not path.is_symlink():
            return
        metadata = path.lstat()
        if stat.S_ISDIR(metadata.st_mode):
            path.rmdir()
        else:
            path.unlink()

    hostile_paths: list[Path] = []
    try:
        candidate_symlink = (
            HERE / f".cm2_round220_{token}_symlink_certificate.json"
        )
        candidate_symlink.symlink_to(CANDIDATE)
        hostile_paths.append(candidate_symlink)
        candidate_object_rejected(candidate_symlink)

        hardlink_source = hostile_dir / "candidate-hardlink-source"
        hardlink_source.write_bytes(b"hardlink")
        hostile_paths.append(hardlink_source)
        candidate_hardlink = (
            HERE / f".cm2_round220_{token}_hardlink_certificate.json"
        )
        os.link(hardlink_source, candidate_hardlink)
        hostile_paths.append(candidate_hardlink)
        candidate_object_rejected(candidate_hardlink)

        candidate_fifo = (
            HERE / f".cm2_round220_{token}_fifo_certificate.json"
        )
        os.mkfifo(candidate_fifo)
        hostile_paths.append(candidate_fifo)
        candidate_object_rejected(candidate_fifo)

        candidate_directory = (
            HERE / f".cm2_round220_{token}_directory_certificate.json"
        )
        candidate_directory.mkdir()
        hostile_paths.append(candidate_directory)
        candidate_object_rejected(candidate_directory)

        candidate_empty = (
            HERE / f".cm2_round220_{token}_empty_certificate.json"
        )
        candidate_empty.touch()
        hostile_paths.append(candidate_empty)
        candidate_object_rejected(candidate_empty)

        candidate_oversize = (
            HERE / f".cm2_round220_{token}_oversize_certificate.json"
        )
        with candidate_oversize.open("wb") as handle:
            handle.truncate(MAX_BYTES + 1)
        hostile_paths.append(candidate_oversize)
        candidate_object_rejected(candidate_oversize)

        candidate_missing = (
            HERE / f".cm2_round220_{token}_missing_certificate.json"
        )
        candidate_object_rejected(candidate_missing)

        output_symlink = (
            HERE / f".cm2_round220_{token}_symlink_verification.json"
        )
        output_symlink.symlink_to(OUTPUT)
        hostile_paths.append(output_symlink)
        output_object_rejected(output_symlink)

        output_hardlink_source = hostile_dir / "output-hardlink-source"
        output_hardlink_source.write_bytes(b"hardlink")
        hostile_paths.append(output_hardlink_source)
        output_hardlink = (
            HERE / f".cm2_round220_{token}_hardlink_verification.json"
        )
        os.link(output_hardlink_source, output_hardlink)
        hostile_paths.append(output_hardlink)
        output_object_rejected(output_hardlink)

        output_fifo = (
            HERE / f".cm2_round220_{token}_fifo_verification.json"
        )
        os.mkfifo(output_fifo)
        hostile_paths.append(output_fifo)
        output_object_rejected(output_fifo)

        output_directory = (
            HERE / f".cm2_round220_{token}_directory_verification.json"
        )
        output_directory.mkdir()
        hostile_paths.append(output_directory)
        output_object_rejected(output_directory)
    finally:
        for path in reversed(hostile_paths):
            remove_object(path)
        hostile_dir.rmdir()
    attempted += 11
    need(rejected == attempted, "actual hostile file-object attacks")
    return {
        "attempted": attempted,
        "rejected": rejected,
        "actual_candidate_file_objects": {
            "symlink": 1, "hardlink": 1, "FIFO": 1, "directory": 1,
            "empty": 1, "oversize": 1, "missing": 1,
        },
        "actual_output_file_objects": {
            "existing_symlink": 1, "existing_hardlink": 1,
            "existing_FIFO": 1, "existing_directory": 1,
        },
        "parent_symlink_paths": 2,
    }


def atomic_write(path: Path, data: bytes) -> None:
    absolute = validate_output(path)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{absolute.name}.", suffix=".tmp", dir=absolute.parent
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
            os.O_RDONLY | getattr(os, "O_DIRECTORY", 0)
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
    parser.add_argument("--candidate", type=Path, default=CANDIDATE)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    arguments = parser.parse_args()
    candidate_path = validate_candidate(arguments.candidate)
    output_path = validate_output(arguments.output)
    producer_hash = hashlib.sha256(secure_bytes(PRODUCER)).hexdigest()
    need(producer_hash == PRODUCER_SHA, "producer freeze")
    entries, docs = replay()
    candidate_document = load(candidate_path)
    reconstruction = verify_full(candidate_document, entries, docs)
    actual_attacks = actual_candidate_attacks(
        candidate_document, docs[f"{R179}_rows.json"]["result"]
    )
    verifier_hash = hashlib.sha256(
        secure_bytes(Path(__file__))
    ).hexdigest()
    result = {
        "status": PASS_STATUS,
        "candidate_schema": CANDIDATE_SCHEMA,
        "candidate_result_sha256": RESULT_SHA,
        "candidate_file_sha256":
            hashlib.sha256(secure_bytes(candidate_path)).hexdigest(),
        "producer_sha256": producer_hash,
        "verifier_sha256": verifier_hash,
        "producer_imported_or_executed": False,
        "independent_reconstruction": reconstruction,
        "attack_suite": {
            "actual_candidate_envelope": actual_attacks,
            "synthetic_contract_snapshot": snapshot_attacks(),
            "JSON": json_attacks(),
            "path_and_output": path_attacks(),
        },
        "strict_nonpromotion_reconfirmed": {
            "whole_origin_credit": 0,
            "physical_component_credit": 0,
            "global_exact_key_disposition_credit": 0,
            "source_G_global_exact_key_dispositions": "0/224580",
            "D02": "BLOCKED",
            "global_Gate5_fields": "10/18",
            "CM2": "NO-GO_FOR_CLAIM",
        },
    }
    verification = {
        "schema": VERIFICATION_SCHEMA,
        "result": result,
        "result_sha256": h(result),
    }
    atomic_write(output_path, canon(verification) + b"\n")
    print(PASS_STATUS)
    print(f"result_sha256={verification['result_sha256']}")
    print(f"output={output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
