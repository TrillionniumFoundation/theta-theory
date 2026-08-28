#!/usr/bin/env python3
"""Round299 zero-credit complete common-face frontier for Round292 cells.

Round292 only joined uncovered refinement cells inside one Round287 support
union.  It did not audit common faces between different support unions, nor
did it preserve occupied/uncovered and occupied/occupied face contacts as a
global component frontier.  This diagnostic closes that *coordinate-box*
enumeration gap over all 11,852 exact Round292 cells.

The output is intentionally fail-closed:

* a common coordinate face is not automatically a physical component edge;
* a cell inherited from a REGULAR_GRAPH_CROSSING support remains constrained
  by its signed active factor and requires a face-level signed-support replay;
* even a FULL/FULL face is only a candidate until its physical-face semantics
  (occurrence identity versus component adjacency) are independently frozen;
* all formal credits remain zero.

This file is a diagnostic producer, not a CM2 maximality certificate.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import io
import json
import os
import tempfile
from collections import Counter, defaultdict
from fractions import Fraction as Q
from pathlib import Path
from typing import Any, Iterable


HERE = Path(__file__).resolve().parent
PREFIX = "cm2_round299_source_g_r292_complete_common_face_frontier_diagnostic_probe"
OUTPUT = HERE / f"{PREFIX}_result.json"
LEDGER = HERE / f"{PREFIX}_ledger.json.gz"

R275 = "cm2_round275_source_g_complete_reverse_rechart_materialization_certificate.json"
R287 = "cm2_round287_source_g_rechart_terminal_occurrence_disposition_probe_ledger.json.gz"
R292 = "cm2_round292_source_g_r287_registry_overlap_exhaustion_probe_ledger.json.gz"
R294 = "cm2_round294_source_g_occurrence_registry_atomic_promotion_registry_ledger.json.gz"
R295A = (
    "cm2_round295a_source_g_r291_positive_t_retained_continuation_closure_"
    "physical_witness_incidence_binding_ledger.json.gz"
)
R296 = "cm2_round296_source_g_true_seam_occurrence_edge_ledger_closure_edge_ledger.json.gz"
R297 = "cm2_round297_source_g_ordinary_face_occurrence_edge_promotion_edge_ledger.json.gz"

PINS = {
    R275: "e18935169614fc8b62ead3be7f60b383396ea1d2c52e8151457241f49e770386",
    R287: "29838e3e6b33f03bf623bbce8b87e6ba5c3306e66beb0b6634496503fb9a4f9a",
    R292: "8863126e88ffd30438938d0a8bdb577f5928ae81f3f17f4b506829d59103a8ab",
    R294: "c6b26f13e90072db99fa98f99fc62c77135ff1cbdb23bbbd5bac3e9f64a834bb",
    R295A: "2d9addfc9fca55366a58b29a7084c063674c3f556dd5398b038ae7d51fe97dcf",
    R296: "1b57b10fac9317e1609fb8858972011165bd95e5b1b687604edd6c8ad7139ef7",
    R297: "18a20b4679a8a3e94ccaf1b511694220cad1bc92e1590ded4585ae3735547371",
}

SCHEMA = "cm2.round299.source-g-r292-complete-common-face-frontier-diagnostic.v1"
LEDGER_SCHEMA = SCHEMA + ".ledger.v1"
ENC = json.JSONEncoder(
    sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False
)

U_DISPOSITION = (
    "EXACT_UNCOVERED_POSITIVE_OPEN_SLICE__"
    "MEMBER_OF_REFINED_PARENT_LOCAL_NEW_SUPPORT"
)
O_DISPOSITION = (
    "EXACT_EXISTING_OCCURRENCE_REPRESENTATION_SUBCOVER__NO_NEW_OCCURRENCE_ID"
)


def canonical(value: Any) -> bytes:
    return ENC.encode(value).encode()


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def file_sha256(path: Path) -> str:
    result = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            result.update(chunk)
    return result.hexdigest()


def need(condition: bool, label: str) -> None:
    if not condition:
        raise RuntimeError(label)


def read_json(name: str) -> dict[str, Any]:
    path = HERE / name
    need(file_sha256(path) == PINS[name], f"pin:{name}")
    return json.loads(path.read_bytes())


def read_gzip(name: str) -> dict[str, Any]:
    path = HERE / name
    need(file_sha256(path) == PINS[name], f"pin:{name}")
    with gzip.open(path, "rt", encoding="utf-8") as handle:
        return json.load(handle)


def verify_closed_row(row: dict[str, Any], label: str) -> None:
    payload = {key: value for key, value in row.items() if key != "row_sha256"}
    need(row["row_sha256"] == digest(payload), f"{label}:row_sha256")


def verify_table(
    document: dict[str, Any],
    rows_key: str,
    count_key: str,
    hash_key: str,
) -> list[dict[str, Any]]:
    rows = document[rows_key]
    need(len(rows) == document[count_key], f"{rows_key}:count")
    need(digest(rows) == document[hash_key], f"{rows_key}:rows_sha256")
    return rows


def qbox(values: Iterable[str]) -> tuple[Q, ...]:
    result = tuple(map(Q, values))
    need(
        len(result) == 6
        and all(result[2 * axis] < result[2 * axis + 1] for axis in range(3)),
        "positive exact box",
    )
    return result


def qstr(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else str(value)


def closed(payload: dict[str, Any]) -> dict[str, Any]:
    result = dict(payload)
    need("row_sha256" not in result, "row already closed")
    result["row_sha256"] = digest(result)
    return result


def deterministic_gzip_bytes(value: Any) -> bytes:
    buffer = io.BytesIO()
    with gzip.GzipFile(
        filename="", mode="wb", fileobj=buffer, compresslevel=9, mtime=0
    ) as handle:
        handle.write(canonical(value))
    return buffer.getvalue()


def atomic(path: Path, payload: bytes) -> None:
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


def pair(left: str, right: str) -> tuple[str, str]:
    need(left != right, "nonself pair requested")
    return tuple(sorted((left, right)))


def load_regions() -> dict[str, dict[str, Any]]:
    wrapper = read_json(R275)
    need(wrapper["result_sha256"] == digest(wrapper["result"]), "R275 result digest")
    result = wrapper["result"]
    rows = [
        row
        for table in ("strict_region_ledger", "arrangement_region_ledger")
        for row in verify_table(
            result[table], "rows", "row_count", "rows_sha256"
        )
    ]
    need(len(rows) == 13_788, "R275 region count")
    result_by_id = {
        row["reverse_rechart_region_row_id"]: row for row in rows
    }
    need(len(result_by_id) == len(rows), "R275 region IDs unique")
    return result_by_id


def load_r287() -> tuple[
    dict[str, dict[str, Any]],
    dict[str, dict[str, Any]],
]:
    document = read_gzip(R287)
    region_rows = verify_table(
        document, "region_rows", "region_row_count", "region_rows_sha256"
    )
    cell_rows = verify_table(
        document,
        "refinement_cell_rows",
        "refinement_cell_row_count",
        "refinement_cell_rows_sha256",
    )
    need(len(region_rows) == 13_788 and len(cell_rows) == 7_616, "R287 census")
    return (
        {row["Round275_region_id"]: row for row in region_rows},
        {row["Round286_refinement_cell_id"]: row for row in cell_rows},
    )


def load_r294_refined_occurrence_map() -> dict[str, str]:
    document = read_gzip(R294)
    rows = verify_table(document, "rows", "row_count", "rows_sha256")
    need(len(rows) == 431_208, "R294 registry census")
    result = {
        row["source_row_id"]: row["registry_occurrence_id"]
        for row in rows
        if row["registry_entry_kind"]
        == "CANDIDATE_NEW_ROUND292_REFINED_R287_SUPPORT_COMPONENT"
    }
    need(len(result) == 9_404, "R294 refined occurrence map")
    return result


def inherited_support_state(
    source_cell_id: str,
    region_id: str,
    regions: dict[str, dict[str, Any]],
    r287_regions: dict[str, dict[str, Any]],
    r287_cells: dict[str, dict[str, Any]],
) -> str:
    if source_cell_id.startswith("WHOLE:"):
        need(source_cell_id == "WHOLE:" + region_id, "whole source cell identity")
        kind = r287_regions[region_id]["R275_region_kind"]
        if kind == "REGULAR_GRAPH_CROSSING":
            return "SIGNED_REGULAR_GRAPH_CONSTRAINED_WHOLE_SUPPORT"
        need(
            kind in {"WHOLE_STRICT_SIGNATURE_CELL", "ZERO_SET_ABSENT"},
            "known whole support kind",
        )
        return "FULL_SIGNED_WHOLE_SUPPORT"
    row = r287_cells[source_cell_id]
    need(row["Round275_region_id"] == region_id, "R287 cell parent")
    state = row["signed_region_cell_state"]
    if state == "FULL_DESIRED_SIDE_SUPPORT":
        return "FULL_SIGNED_REFINEMENT_SUPPORT"
    need(state == "CLIPPED_DESIRED_SIDE_SUPPORT", "nonempty R287 cell state")
    need(
        regions[region_id].get("arrangement_classification")
        == "REGULAR_GRAPH_CROSSING",
        "clipped cell has graph parent",
    )
    return "SIGNED_REGULAR_GRAPH_CONSTRAINED_REFINEMENT_SUPPORT"


def load_r292_cells(
    regions: dict[str, dict[str, Any]],
    r287_regions: dict[str, dict[str, Any]],
    r287_cells: dict[str, dict[str, Any]],
    refined_occurrence: dict[str, str],
) -> list[dict[str, Any]]:
    document = read_gzip(R292)
    rows = verify_table(document, "rows", "row_count", "rows_sha256")
    result: list[dict[str, Any]] = []
    for source in rows:
        disposition = source.get("disposition")
        if disposition not in {U_DISPOSITION, O_DISPOSITION}:
            continue
        region_id = source["Round275_region_id"]
        source_cell_id = source["source_Round287_support_cell_id"]
        kind = "UNCOVERED_REFINED_NEW_SUPPORT" if disposition == U_DISPOSITION else (
            "OCCUPIED_EXISTING_OCCURRENCE_REPRESENTATION"
        )
        if disposition == U_DISPOSITION:
            component_id = source["Round292_refined_new_support_component_id"]
            endpoint = refined_occurrence[component_id]
            need(source["existing_occurrence_ids"] == [], "uncovered occupancy")
        else:
            component_id = None
            need(
                source["existing_occurrence_occupancy_count"] == 1
                and len(source["existing_occurrence_ids"]) == 1,
                "occupied unique endpoint",
            )
            endpoint = source["existing_occurrence_ids"][0]
        result.append(
            {
                "cell_id": source[
                    "Round292_R287_existing_overlap_refinement_cell_id"
                ],
                "source_cell_id": source_cell_id,
                "support_union_id": source["Round287_potential_new_support_union_id"],
                "region_id": region_id,
                "source_chart": source["source_chart"],
                "physical_t_sign": r287_regions[region_id]["physical_t_sign"],
                "box": qbox(source["exact_transformed_open_cell"]),
                "signature_sha256": source[
                    "complete_10_field_return_signature_sha256"
                ],
                "endpoint_kind": kind,
                "endpoint_occurrence_id": endpoint,
                "Round292_refined_new_support_component_id": component_id,
                "inherited_signed_support_state": inherited_support_state(
                    source_cell_id,
                    region_id,
                    regions,
                    r287_regions,
                    r287_cells,
                ),
            }
        )
    result.sort(key=lambda row: row["cell_id"])
    need(
        len(result) == 11_852
        and Counter(row["endpoint_kind"] for row in result)
        == {
            "UNCOVERED_REFINED_NEW_SUPPORT": 10_252,
            "OCCUPIED_EXISTING_OCCURRENCE_REPRESENTATION": 1_600,
        },
        "R292 exact cell census",
    )
    need(len({row["cell_id"] for row in result}) == len(result), "R292 cell IDs")
    return result


def common_face(
    left: tuple[Q, ...], right: tuple[Q, ...], axis: int
) -> tuple[Q, ...] | None:
    if left[2 * axis + 1] != right[2 * axis]:
        return None
    result: list[Q] = []
    for current in range(3):
        if current == axis:
            value = left[2 * current + 1]
            result.extend((value, value))
            continue
        lower = max(left[2 * current], right[2 * current])
        upper = min(left[2 * current + 1], right[2 * current + 1])
        if not lower < upper:
            return None
        result.extend((lower, upper))
    return tuple(result)


def pair_kind(left: dict[str, Any], right: dict[str, Any]) -> str:
    return "".join(
        sorted(
            "U" if row["endpoint_kind"].startswith("UNCOVERED") else "O"
            for row in (left, right)
        )
    )


def face_status(left: dict[str, Any], right: dict[str, Any]) -> str:
    states = {
        left["inherited_signed_support_state"],
        right["inherited_signed_support_state"],
    }
    graph = any("REGULAR_GRAPH_CONSTRAINED" in state for state in states)
    if graph:
        return (
            "OUTER_COORDINATE_COMMON_FACE_ONLY__"
            "SIGNED_ACTIVE_FACTOR_FACE_REPLAY_REQUIRED"
        )
    return (
        "BOTH_ENDPOINT_CELLS_FULL_SIGNED_SUPPORT__"
        "EXACT_COORDINATE_COMMON_FACE_CANDIDATE__"
        "PHYSICAL_SEMANTICS_NOT_YET_PROMOTED"
    )


def semantic_frontier(
    left: dict[str, Any], right: dict[str, Any]
) -> str:
    same_endpoint = (
        left["endpoint_occurrence_id"] == right["endpoint_occurrence_id"]
    )
    same_union = left["support_union_id"] == right["support_union_id"]
    kind = pair_kind(left, right)
    if same_endpoint and kind == "UU":
        need(same_union, "R292 refined component cannot span support unions")
        return "ROUND292_INTERNAL_REFINED_OCCURRENCE_IDENTITY__ALREADY_CONSUMED"
    if same_endpoint:
        return "SELF_REPRESENTATION_FACE__NO_NEW_ENDPOINT_PAIR"
    if kind == "UU":
        return (
            "CROSS_UNION_REFINED_SUPPORT_FRONTIER__"
            "IDENTITY_VERSUS_COMPONENT_EDGE_SEMANTICS_PENDING"
        )
    if kind == "OU":
        return "REFINED_TO_EXISTING_OCCURRENCE_COMPONENT_EDGE_CANDIDATE"
    return "EXISTING_TO_EXISTING_OCCURRENCE_COMPONENT_EDGE_CANDIDATE"


def enumerate_faces(cells: list[dict[str, Any]]) -> list[dict[str, Any]]:
    lower_index: dict[tuple[str, int, int, Q], list[int]] = defaultdict(list)
    for index, row in enumerate(cells):
        for axis in range(3):
            lower_index[
                (
                    row["source_chart"],
                    row["physical_t_sign"],
                    axis,
                    row["box"][2 * axis],
                )
            ].append(index)

    rows: list[dict[str, Any]] = []
    for left_index, left in enumerate(cells):
        for axis in range(3):
            key = (
                left["source_chart"],
                left["physical_t_sign"],
                axis,
                left["box"][2 * axis + 1],
            )
            for right_index in lower_index.get(key, []):
                right = cells[right_index]
                face = common_face(left["box"], right["box"], axis)
                if face is None:
                    continue
                same_endpoint = (
                    left["endpoint_occurrence_id"]
                    == right["endpoint_occurrence_id"]
                )
                endpoint_pair = (
                    None
                    if same_endpoint
                    else list(
                        pair(
                            left["endpoint_occurrence_id"],
                            right["endpoint_occurrence_id"],
                        )
                    )
                )
                payload = {
                    "Round299_R292_coordinate_common_face_row_id":
                        "round299-r292-coordinate-common-face:"
                        + digest(
                            [
                                left["cell_id"],
                                right["cell_id"],
                                axis,
                                list(map(qstr, face)),
                            ]
                        ),
                    "left_Round292_refinement_cell_id": left["cell_id"],
                    "right_Round292_refinement_cell_id": right["cell_id"],
                    "left_Round287_support_union_id": left["support_union_id"],
                    "right_Round287_support_union_id": right["support_union_id"],
                    "left_Round275_region_id": left["region_id"],
                    "right_Round275_region_id": right["region_id"],
                    "source_chart": left["source_chart"],
                    "physical_t_sign": left["physical_t_sign"],
                    "common_face_axis": axis,
                    "common_face_coordinate_system": "(t^2,p,s)",
                    "exact_positive_area_coordinate_face": list(map(qstr, face)),
                    "endpoint_pair_kind": pair_kind(left, right),
                    "left_formal_occurrence_id": left["endpoint_occurrence_id"],
                    "right_formal_occurrence_id": right["endpoint_occurrence_id"],
                    "unordered_nonself_formal_occurrence_endpoint_pair":
                        endpoint_pair,
                    "same_formal_occurrence_endpoint": same_endpoint,
                    "same_Round287_support_union":
                        left["support_union_id"] == right["support_union_id"],
                    "same_complete_10_field_return_signature":
                        left["signature_sha256"] == right["signature_sha256"],
                    "left_complete_10_field_return_signature_sha256":
                        left["signature_sha256"],
                    "right_complete_10_field_return_signature_sha256":
                        right["signature_sha256"],
                    "left_inherited_signed_support_state":
                        left["inherited_signed_support_state"],
                    "right_inherited_signed_support_state":
                        right["inherited_signed_support_state"],
                    "coordinate_face_physical_replay_status":
                        face_status(left, right),
                    "semantic_frontier": semantic_frontier(left, right),
                    "formal_occurrence_identity_collapse_credit": 0,
                    "formal_component_edge_credit": 0,
                    "formal_DSU_rank_reduction_credit": 0,
                    "formal_maximality_credit": 0,
                }
                rows.append(closed(payload))
    rows.sort(key=lambda row: row["Round299_R292_coordinate_common_face_row_id"])
    need(len(rows) == 43_092, "complete R292 coordinate common-face census")
    return rows


def channel_pairs() -> dict[str, set[tuple[str, str]]]:
    ordinary_document = read_gzip(R297)
    ordinary_rows = verify_table(
        ordinary_document, "rows", "row_count", "rows_sha256"
    )
    ordinary = {
        tuple(row["exact_occurrence_endpoint_pair"]) for row in ordinary_rows
    }
    need(len(ordinary) == 330_724, "R297 unique ordinary pairs")

    seam_document = read_gzip(R296)
    seam_rows = verify_table(seam_document, "rows", "row_count", "rows_sha256")
    seam = {
        tuple(row["unordered_formal_occurrence_endpoint_pair"])
        for row in seam_rows
    }
    need(len(seam) == 15_316, "R296 unique seam pairs")

    lower_document = read_gzip(R295A)
    lower_rows = verify_table(lower_document, "rows", "row_count", "rows_sha256")
    lower = {
        tuple(row["target_Round294_registry_occurrence_ids"])
        for row in lower_rows
        if row["target_Round294_registry_reference_count"] == 2
    }
    need(len(lower) == 111_524, "R295A distinct lower pairs")
    return {"R297_ORDINARY": ordinary, "R296_TRUE_SEAM": seam, "R295A_LOWER": lower}


def census(
    rows: list[dict[str, Any]],
    channels: dict[str, set[tuple[str, str]]],
) -> dict[str, Any]:
    raw_class = Counter()
    axis = Counter()
    signature = Counter()
    replay = Counter()
    state_pairs = Counter()
    semantic = Counter()
    distinct_by_class: dict[str, set[tuple[str, str]]] = defaultdict(set)
    all_nonself: set[tuple[str, str]] = set()
    self_class = Counter()

    for row in rows:
        scope = "SAME_UNION" if row["same_Round287_support_union"] else "CROSS_UNION"
        classification = scope + "|" + row["endpoint_pair_kind"]
        raw_class[classification] += 1
        axis[str(row["common_face_axis"])] += 1
        signature[
            classification
            + "|"
            + ("SAME_SIGNATURE" if row["same_complete_10_field_return_signature"]
               else "DIFFERENT_SIGNATURE")
        ] += 1
        replay[classification + "|" + row["coordinate_face_physical_replay_status"]] += 1
        state_pairs[
            classification
            + "|"
            + "|".join(
                sorted(
                    (
                        row["left_inherited_signed_support_state"],
                        row["right_inherited_signed_support_state"],
                    )
                )
            )
        ] += 1
        semantic[row["semantic_frontier"]] += 1
        endpoint_pair = row[
            "unordered_nonself_formal_occurrence_endpoint_pair"
        ]
        if endpoint_pair is None:
            self_class[classification] += 1
        else:
            exact_pair = tuple(endpoint_pair)
            distinct_by_class[classification].add(exact_pair)
            all_nonself.add(exact_pair)

    expected_raw = {
        "SAME_UNION|UU": 848,
        "SAME_UNION|OU": 464,
        "SAME_UNION|OO": 740,
        "CROSS_UNION|UU": 38_668,
        "CROSS_UNION|OU": 496,
        "CROSS_UNION|OO": 1_876,
    }
    expected_distinct = {
        "SAME_UNION|OU": 416,
        "SAME_UNION|OO": 464,
        "CROSS_UNION|UU": 36_740,
        "CROSS_UNION|OU": 248,
        "CROSS_UNION|OO": 336,
    }
    expected_self = {
        "SAME_UNION|UU": 848,
        "SAME_UNION|OO": 36,
        "CROSS_UNION|OO": 1_208,
    }
    need(dict(raw_class) == expected_raw, "raw face classification")
    need(
        {key: len(value) for key, value in distinct_by_class.items()}
        == expected_distinct,
        "distinct nonself face classification",
    )
    need(dict(self_class) == expected_self, "self face classification")
    need(axis == {"0": 14_552, "1": 16_244, "2": 12_296}, "axis census")

    full_cross_uu = sum(
        1
        for row in rows
        if not row["same_Round287_support_union"]
        and row["endpoint_pair_kind"] == "UU"
        and row["coordinate_face_physical_replay_status"].startswith(
            "BOTH_ENDPOINT_CELLS_FULL"
        )
    )
    need(full_cross_uu == 12_536, "cross-union FULL/FULL UU census")

    channel_intersections = {
        name: len(all_nonself & pairs) for name, pairs in channels.items()
    }
    return {
        "input_exact_Round292_refinement_cell_count": 11_852,
        "raw_coordinate_common_face_count": len(rows),
        "raw_coordinate_common_face_axis_histogram": dict(sorted(axis.items())),
        "raw_scope_endpoint_kind_histogram": dict(sorted(raw_class.items())),
        "raw_scope_endpoint_signature_histogram": dict(sorted(signature.items())),
        "raw_scope_endpoint_replay_status_histogram": dict(sorted(replay.items())),
        "raw_scope_endpoint_support_state_pair_histogram":
            dict(sorted(state_pairs.items())),
        "raw_semantic_frontier_histogram": dict(sorted(semantic.items())),
        "self_endpoint_face_histogram": dict(sorted(self_class.items())),
        "distinct_nonself_endpoint_pair_histogram": dict(
            sorted(
                (key, len(value)) for key, value in distinct_by_class.items()
            )
        ),
        "distinct_nonself_endpoint_pair_count": len(all_nonself),
        "cross_union_UU_FULL_FULL_raw_candidate_count": full_cross_uu,
        "cross_union_UU_same_signature_raw_count": sum(
            1
            for row in rows
            if not row["same_Round287_support_union"]
            and row["endpoint_pair_kind"] == "UU"
            and row["same_complete_10_field_return_signature"]
        ),
        "cross_union_UU_different_signature_raw_count": sum(
            1
            for row in rows
            if not row["same_Round287_support_union"]
            and row["endpoint_pair_kind"] == "UU"
            and not row["same_complete_10_field_return_signature"]
        ),
        "existing_channel_pair_intersection_count": channel_intersections,
        "coordinate_box_contact_is_not_physical_edge_proof": True,
        "signed_graph_constrained_faces_require_active_factor_replay": True,
        "occurrence_identity_vs_component_edge_semantics_remain_unfrozen": True,
    }


def build() -> tuple[dict[str, Any], dict[str, Any]]:
    regions = load_regions()
    r287_regions, r287_cells = load_r287()
    refined_occurrence = load_r294_refined_occurrence_map()
    cells = load_r292_cells(
        regions, r287_regions, r287_cells, refined_occurrence
    )
    rows = enumerate_faces(cells)
    channels = channel_pairs()
    result_census = census(rows, channels)
    ledger = {
        "schema": LEDGER_SCHEMA,
        "status": "PASS_ZERO_CREDIT__COMPLETE_R292_COORDINATE_COMMON_FACE_FRONTIER",
        "row_count": len(rows),
        "rows": rows,
        "rows_sha256": digest(rows),
        "row_ids_sha256": digest(
            [row["Round299_R292_coordinate_common_face_row_id"] for row in rows]
        ),
        "row_hashes_sha256": digest([row["row_sha256"] for row in rows]),
        "every_row_closed_by_own_SHA256": True,
    }
    result = {
        "schema": SCHEMA,
        "status": "PASS_ZERO_CREDIT__R292_COMMON_FACE_GAP_ENUMERATED_NOT_PROMOTED",
        "input_file_pins": PINS,
        "census": result_census,
        "ledger": {
            "filename": LEDGER.name,
            "row_count": len(rows),
            "rows_sha256": ledger["rows_sha256"],
        },
        "strict_nonpromotion": {
            "formal_occurrence_identity_collapse_credit": 0,
            "formal_component_edge_credit": 0,
            "formal_DSU_rank_reduction_credit": 0,
            "formal_maximality_credit": 0,
            "CM2": "NO_GO_PENDING_SIGNED_FACE_REPLAY_AND_SEMANTIC_PROMOTION",
        },
    }
    result["result_sha256"] = digest(result)
    return ledger, result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ledger", type=Path, default=LEDGER)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    arguments = parser.parse_args()
    ledger, result = build()
    ledger_bytes = deterministic_gzip_bytes(ledger)
    result["ledger"]["file_sha256"] = hashlib.sha256(ledger_bytes).hexdigest()
    result["result_sha256"] = digest(
        {key: value for key, value in result.items() if key != "result_sha256"}
    )
    atomic(arguments.ledger, ledger_bytes)
    atomic(arguments.output, canonical(result) + b"\n")


if __name__ == "__main__":
    main()
