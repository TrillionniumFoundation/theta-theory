#!/usr/bin/env python3
"""Independently verify the Round240 strict-corridor incidence delta."""

from __future__ import annotations

import argparse
import gc
import hashlib
import json
import os
import stat
import sys
import tempfile
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from flint import ctx


HERE = Path(__file__).resolve().parent
OUTPUT = (
    HERE
    / "cm2_round240_source_g_remote_sheet_interface_corridor_incidence_verification.json"
)
PINS = {
    "cm2_round174_source_g_unique_first_dynamic_occurrence_materialization_verifier.py":
        "c7ead7c9cb8b4d7b8680e64bfb7870e5c5f5e39277e7c7d3d08a62b600f5c058",
    "cm2_round179_source_g_residual_tube_arrangement.py":
        "8c568c58d82708a7ab549f126c1fcedfccff563d1d00e3c1f7e6545b4b0d29ab",
    "cm2_round179_source_g_residual_tube_arrangement_rows.json":
        "f20b42c1fed781779b537b4d45bf44233eae1ed3ee620b95177a80f0eb2b5e42",
    "cm2-gate5-return-word-three-norm-frontier-manifest-2026-07-16.json":
        "47e84e8b75b289b7a5db4afcbd7dfa8dac909d2f76fa1c95ef290546d031a866",
    "cm2_round208_source_g_outgoing_direct_signature_materialization_certificate.json":
        "4d01fb9cee639ec59786c078f7a20b3bbcd5c18ea674fabbfce64e250e765938",
    "cm2_round220_source_g_round179_resolved_child_boundary_atlas_certificate.json":
        "569a7849b53805ff4deca0eff9a6938a897942d3d682dfef27c27559135ce974",
    "cm2_round225_source_g_certified_connectivity_rebuild_certificate.json":
        "0d040af30906f22f600820e14867c45115e679e33b6ee6f052c51a914cf7d841",
    "cm2_round229_source_g_global_occurrence_known_block_frontier_certificate.json":
        "c4152f4764ed7fe977046ef728e8257344803433053e06c0ac11ec68b86ff11a",
    "cm2_round230_source_g_resolved_retained_bulk_continuation_certificate.json":
        "88d9d826bd985635d42820c7b66389603ab56a48717531ace525ee2eaf6d3a73",
    "cm2_round233_source_g_outgoing_seam_parametric_graph_key_partition_certificate.json":
        "cb2f74daa9836841ce311d8d555c2d94ba897f346a63c1e29551d7f99e8d1a41",
    "cm2_round239_source_g_unaccepted_interface_local_classification_ledger_certificate.json":
        "08d392f43fbc7a8d88c6d70b2c36aed7f8d710aac2f6569cf5910dba240ed9cf",
    "cm2_round240_source_g_remote_sheet_interface_corridor_incidence.py":
        "9967d1f5b5684f1d2a95fa174f72deda2d88c3878d73596042d2f49ab25c1987",
    "cm2_round240_source_g_remote_sheet_interface_corridor_incidence_certificate.json":
        "65285cd08662006015c388f8dbf1eb077ca2434d80b715dbdc99c332de629359",
}
MAXIMUM_BYTES = {
    name: (
        5_000_000
        if name.endswith(".py") or "manifest" in name
        else 400_000_000
    )
    for name in PINS
}
STRICT_SIGNS = {"STRICT_NEGATIVE", "STRICT_POSITIVE"}


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


def read_pinned(name: str) -> bytes:
    path = HERE / name
    info = path.lstat()
    need(
        stat.S_ISREG(info.st_mode)
        and not path.is_symlink()
        and info.st_nlink == 1
        and 0 < info.st_size <= MAXIMUM_BYTES[name],
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


def selected_rows(
    document: dict[str, Any],
    table_name: str,
    id_field: str,
    identifiers: set[str],
) -> dict[str, dict[str, Any]]:
    columns = document["row_column_schemas"][table_name]
    index = columns.index(id_field)
    return {
        packed[index]: dict(zip(columns, packed, strict=True))
        for packed in document[table_name]
        if packed[index] in identifiers
    }


def closed(row: dict[str, Any]) -> dict[str, Any]:
    result = dict(row)
    result["row_sha256"] = digest(result)
    return result


def zero_credits() -> dict[str, int]:
    return {
        "known_block_membership_assignment_credit": 0,
        "physical_component_credit": 0,
        "maximal_physical_component_credit": 0,
        "global_exact_key_disposition_credit": 0,
    }


def source_signature(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "source_chart": row["chart"],
        "target_lift": row["owner_target"],
        "ordered_integer_wall_events": row["ordered_integer_wall_events"],
        "signed_wall_word": row["signed_wall_word"],
        "roof": row["roof"],
        "outgoing_cell": row["outgoing_cell"],
        "target_chart": row["target_chart"],
        "official_key_row": row["official_key_row"],
        "official_key_ordinal": row["official_key_ordinal"],
        "official_key_id": row["official_key_id"],
    }


def interval_signature(
    data: dict[str, Any],
    chart: str,
    owner: str,
) -> dict[str, Any]:
    return {
        "source_chart": chart,
        "target_lift": owner,
        "ordered_integer_wall_events": data["events"],
        "signed_wall_word": list(data["pattern"]),
        "roof": data["roof"],
        "outgoing_cell": data["outgoing"],
        "target_chart": data["target_chart"],
        "official_key_row": data["key"]["row"],
        "official_key_ordinal": data["key"]["ordinal"],
        "official_key_id": data["key"]["identifier"],
    }


def box_volume(box: list[Q]) -> Q:
    return (
        (box[1] - box[0])
        * (box[3] - box[2])
        * (box[5] - box[4])
    )


def overlap(left: list[Q], right: list[Q]) -> tuple[list[Q], Q]:
    result: list[Q] = []
    for axis in range(3):
        lower = max(left[2 * axis], right[2 * axis])
        upper = min(left[2 * axis + 1], right[2 * axis + 1])
        need(lower < upper, "positive overlap")
        result.extend((lower, upper))
    return result, box_volume(result)


def face(resolved_values: list[str], corridor: list[Q]) -> dict[str, Any]:
    resolved = [Q(value) for value in resolved_values]
    intersection: list[Q] = []
    touching: list[tuple[int, str, str]] = []
    for axis in range(3):
        left_lower, left_upper = resolved[2 * axis:2 * axis + 2]
        right_lower, right_upper = corridor[2 * axis:2 * axis + 2]
        lower = max(left_lower, right_lower)
        upper = min(left_upper, right_upper)
        need(lower <= upper, "face nonempty")
        if lower == upper:
            if left_upper == right_lower:
                touching.append((axis, "UPPER", "LOWER"))
            elif right_upper == left_lower:
                touching.append((axis, "LOWER", "UPPER"))
            else:
                raise RuntimeError("face boundary")
        intersection.extend((lower, upper))
    need(len(touching) == 1, "single face axis")
    axis, resolved_side, retained_side = touching[0]
    lengths = [
        intersection[2 * index + 1] - intersection[2 * index]
        for index in range(3)
    ]
    positive = [length for length in lengths if length > 0]
    need(len(positive) == 2, "face positive area")
    return {
        "axis": "tps"[axis],
        "resolved_side": resolved_side,
        "retained_side": retained_side,
        "fixed_coordinate": qstr(intersection[2 * axis]),
        "intersection_box": [qstr(value) for value in intersection],
        "exact_positive_area": qstr(positive[0] * positive[1]),
    }


def make_ledger(rows: list[dict[str, Any]], id_field: str) -> dict[str, Any]:
    return {
        "row_count": len(rows),
        "rows_sha256": digest(rows),
        "row_ids_sha256": digest([row[id_field] for row in rows]),
        "row_hashes_sha256": digest([row["row_sha256"] for row in rows]),
        "every_row_closed_by_own_SHA256": True,
        "rows": rows,
    }


def safe_write(data: bytes) -> None:
    descriptor, name = tempfile.mkstemp(
        prefix=".round240-verifier.",
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


def verify() -> dict[str, Any]:
    for name in PINS:
        read_pinned(name)

    candidate = load_result(
        "cm2_round240_source_g_remote_sheet_interface_corridor_incidence_certificate.json"
    )
    round230 = load_result(
        "cm2_round230_source_g_resolved_retained_bulk_continuation_certificate.json"
    )
    remotes = [
        row
        for row in round230[
            "formal_rejected_local_bulk_candidate_ledger"
        ]["rows"]
        if row["reject_classification"]
        == "FULL_SIGNATURE_REMOTE_WITHOUT_EXACT_POSITIVE_AREA_FACE_OVERLAP"
    ]
    need(len(remotes) == 12, "remote count")
    interface_ids = {
        row["Round220_split_interface_id"] for row in remotes
    }
    region_ids = {row["Round208_region_row_id"] for row in remotes}
    retained_ids = {row["retained_child_row_id"] for row in remotes}
    resolved_ids = {row["resolved_child_row_id"] for row in remotes}
    sheet_ids = {row["Round211_sheet_row_id"] for row in remotes}
    block_ids = {row["Round225_known_block_id"] for row in remotes}

    round239 = load_result(
        "cm2_round239_source_g_unaccepted_interface_local_classification_ledger_certificate.json"
    )
    classifications = {
        row["Round220_split_interface_id"]: row
        for row in round239["classification_ledger_rows"]
    }
    round233 = load_result(
        "cm2_round233_source_g_outgoing_seam_parametric_graph_key_partition_certificate.json"
    )
    graphs = {
        row["Round220_split_interface_id"]: row
        for row in round233["parametric_graph_key_partition_rows"]
        if row["Round220_split_interface_id"] in interface_ids
    }
    need(len(graphs) == 12, "graph count")
    del round233
    gc.collect()

    round229 = load_result(
        "cm2_round229_source_g_global_occurrence_known_block_frontier_certificate.json"
    )
    frontiers = {
        row["local_occurrence_row_id"]: row
        for row in round229[
            "formal_occurrence_known_block_attachment_frontier_ledger"
        ]["rows"]
        if row["local_occurrence_row_id"] in resolved_ids
    }
    lineages = {
        row["Round220_split_interface_id"]: row
        for row in round229[
            "formal_Round220_resolved_retained_coordinate_lineage_frontier_ledger"
        ]["rows"]
    }
    missing_ids = sorted(
        identifier
        for identifier in classifications
        if lineages[identifier]["Round225_referenced_known_block_count"] == 0
    )
    direct_ids = {
        identifier
        for identifier in classifications
        if lineages[identifier]["Round225_referenced_known_block_count"] > 0
    }
    need(
        len(frontiers) == 12
        and len(missing_ids) == 8_500
        and direct_ids == interface_ids,
        "frontier partition",
    )
    del round229, lineages
    gc.collect()

    round225 = load_result(
        "cm2_round225_source_g_certified_connectivity_rebuild_certificate.json"
    )
    sheet_blocks = {
        row["Round211_sheet_row_id"]: row["known_connectivity_block_id"]
        for row in round225["formal_Round211_sheet_assignment_ledger"]["rows"]
        if row["Round211_sheet_row_id"] in sheet_ids
    }
    known_blocks = {
        row["known_connectivity_block_id"]: row
        for row in round225[
            "formal_certified_known_connectivity_block_ledger"
        ]["rows"]
        if row["known_connectivity_block_id"] in block_ids
    }
    need(
        len(sheet_blocks) == len(known_blocks) == 12
        and all(
            row["certified_known_connectivity"]
            for row in known_blocks.values()
        ),
        "block seeds",
    )
    del round225
    gc.collect()

    round220 = load_result(
        "cm2_round220_source_g_round179_resolved_child_boundary_atlas_certificate.json"
    )
    table = round220[
        "coordinate_boundary_atlas"
    ]["tables"]["one_step_split_interface_rows"]
    id_index = table["columns"].index("split_interface_id")
    interfaces = {
        packed[id_index]:
            dict(zip(table["columns"], packed, strict=True))
        for packed in table["rows"]
        if packed[id_index] in interface_ids
    }
    need(len(interfaces) == 12, "interface rows")
    del round220
    gc.collect()

    round179 = load_result(
        "cm2_round179_source_g_residual_tube_arrangement_rows.json"
    )
    retained = selected_rows(
        round179,
        "retained_3d_child_rows",
        "row_id",
        retained_ids,
    )
    resolved = selected_rows(
        round179,
        "resolved_3d_child_rows",
        "row_id",
        resolved_ids,
    )
    origins = selected_rows(
        round179,
        "origin_tube_rows",
        "origin_row_id",
        {row["origin_row_id"] for row in retained.values()},
    )
    need(len(retained) == len(resolved) == len(origins) == 12, "Round179")
    del round179
    gc.collect()

    round208 = load_result(
        "cm2_round208_source_g_outgoing_direct_signature_materialization_certificate.json"
    )
    regions = {
        row["region_row_id"]: row
        for row in round208["formal_local_open_3D_signature_ledger"]["rows"]
        if row["region_row_id"] in region_ids
    }
    need(len(regions) == 12, "region rows")
    del round208
    gc.collect()

    sys.path.insert(0, str(HERE))
    import cm2_round179_source_g_residual_tube_arrangement as r179

    need(
        Path(r179.__file__).resolve()
        == (HERE / "cm2_round179_source_g_residual_tube_arrangement.py").resolve(),
        "probe identity",
    )
    registry = r179.r174.rebuild_registry(
        r179.strict_load(
            HERE
            / "cm2-gate5-return-word-three-norm-frontier-manifest-2026-07-16.json",
            5_000_000,
        )
    )
    ctx.prec = 256

    expected_corridors: list[dict[str, Any]] = []
    expected_deltas: list[dict[str, Any]] = []
    profiles: Counter[tuple[str, str, str]] = Counter()
    for remote in sorted(
        remotes,
        key=lambda row: row["Round220_split_interface_id"],
    ):
        interface_id = remote["Round220_split_interface_id"]
        interface = interfaces[interface_id]
        retained_row = retained[remote["retained_child_row_id"]]
        resolved_row = resolved[remote["resolved_child_row_id"]]
        origin = origins[retained_row["origin_row_id"]]
        region = regions[remote["Round208_region_row_id"]]
        graph = graphs[interface_id]
        classification = classifications[interface_id]
        signature = source_signature(resolved_row)
        sheet_id = remote["Round211_sheet_row_id"]
        block_id = remote["Round225_known_block_id"]
        need(
            interface["axis"] == "s"
            and classification["classification_type"]
            == "OUTGOING_SEAM_GRAPH_SHARED_KEY"
            and graph["shared_official_key_id"]
            == signature["official_key_id"]
            and region["local_return_signature"] == signature
            and sheet_blocks[sheet_id] == block_id
            and frontiers[resolved_row["row_id"]][
                "known_block_incidence_attachment_credit"
            ] == 0,
            f"lineage:{interface_id}",
        )

        root_values = [Q(value) for value in retained_row["box"]]
        leaf_values = [Q(value) for value in region["Round182_leaf_box"]]
        fixed = Q(interface["fixed_coordinate"])
        root_box = r179.box_from(
            retained_row["box"],
            len(retained_row["refinement_path"]),
            retained_row["row_id"],
        )
        root_geometry = r179.interval_geometry(
            retained_row["chart"],
            origin["owner_target"],
            root_box,
        )
        derivative = r179.sign(
            root_geometry["outgoing_equality"][1][0]
        )
        use_upper = (
            signature["outgoing_cell"] in {"E", "W"}
        ) == (derivative == "STRICT_POSITIVE")
        width = (root_values[1] - root_values[0]) / 4
        t0 = root_values[1] - width if use_upper else root_values[0]
        t1 = root_values[1] if use_upper else root_values[0] + width
        corridor_values = [
            t0,
            t1,
            leaf_values[2],
            leaf_values[3],
            min(leaf_values[4], fixed),
            max(leaf_values[5], fixed),
        ]
        corridor_box = r179.r174.atlas.AtlasBox(
            *corridor_values,
            len(retained_row["refinement_path"]) + 2,
            f"round240-verifier:{interface_id}",
        )
        data, reasons = r179.r174.certify_signature(
            retained_row["chart"],
            corridor_box,
            origin["owner_target"],
            registry,
        )
        need(
            data is not None
            and reasons == []
            and interval_signature(
                data,
                retained_row["chart"],
                origin["owner_target"],
            ) == signature,
            f"signature:{interface_id}",
        )
        geometry = r179.interval_geometry(
            retained_row["chart"],
            origin["owner_target"],
            corridor_box,
        )
        signs = {
            "F": r179.sign(geometry["outgoing_equality"][0]),
            "HPLUS": r179.sign(
                r179.dual_add(
                    geometry["outgoing_x"],
                    geometry["outgoing_y"],
                )[0]
            ),
            "HMINUS": r179.sign(
                r179.dual_sub(
                    geometry["outgoing_x"],
                    geometry["outgoing_y"],
                )[0]
            ),
        }
        need(
            set(signs.values()) <= STRICT_SIGNS
            and signs["F"] == region["F_sign"]
            and signs["HPLUS"] == region["HPLUS_sign"]
            and signs["HMINUS"] == region["HMINUS_sign"],
            f"factor signs:{interface_id}",
        )
        profiles[(signs["F"], signs["HPLUS"], signs["HMINUS"])] += 1
        overlap_box, overlap_volume = overlap(
            corridor_values,
            leaf_values,
        )
        patch = face(resolved_row["box"], corridor_values)
        need(
            box_volume(corridor_values) > 0
            and overlap_volume > 0
            and Q(patch["exact_positive_area"]) > 0
            and patch["axis"] == "s"
            and patch["fixed_coordinate"] == interface["fixed_coordinate"],
            f"positive contacts:{interface_id}",
        )

        corridor_id = (
            "round240-strict-sheet-interface-corridor:"
            + digest([
                interface_id,
                region["region_row_id"],
                [qstr(value) for value in corridor_values],
            ])
        )
        expected_corridors.append(closed({
            "strict_corridor_row_id": corridor_id,
            "Round220_split_interface_id": interface_id,
            "Round230_remote_reject_row_id": remote["reject_row_id"],
            "Round233_graph_partition_row_id":
                graph["parametric_graph_partition_row_id"],
            "Round239_classification_ledger_row_id":
                classification["classification_ledger_row_id"],
            "resolved_child_row_id": resolved_row["row_id"],
            "retained_child_row_id": retained_row["row_id"],
            "Round208_region_row_id": region["region_row_id"],
            "Round208_leaf_row_id": region["leaf_row_id"],
            "Round211_sheet_row_id": sheet_id,
            "Round225_known_connectivity_block_id": block_id,
            "axis": "s",
            "fixed_coordinate": interface["fixed_coordinate"],
            "t_lane_dyadic_depth": 2,
            "t_lane_uses_upper_quarter": use_upper,
            "strict_t_derivative_sign": derivative,
            "strict_corridor_box":
                [qstr(value) for value in corridor_values],
            "strict_corridor_exact_coordinate_volume":
                qstr(box_volume(corridor_values)),
            "Round208_region_positive_volume_overlap_box":
                [qstr(value) for value in overlap_box],
            "Round208_region_positive_volume_overlap":
                qstr(overlap_volume),
            "resolved_interface_patch": patch["intersection_box"],
            "resolved_interface_patch_exact_positive_area":
                patch["exact_positive_area"],
            "resolved_side": patch["resolved_side"],
            "retained_side": patch["retained_side"],
            "strict_F_sign": signs["F"],
            "strict_HPLUS_sign": signs["HPLUS"],
            "strict_HMINUS_sign": signs["HMINUS"],
            "Round208_factor_signs_exactly_equal_on_corridor": True,
            "all_10_return_signature_fields_exactly_equal": True,
            "return_signature_sha256": digest(signature),
            "direct_Round211_sheet_seeded_known_block": True,
            "known_block_incidence_bridge_credit": 1,
            "whole_interface_certified": False,
            **zero_credits(),
        }))
        expected_deltas.append(closed({
            "incidence_delta_row_id":
                "round240-known-block-incidence-delta:"
                + digest([resolved_row["row_id"], block_id, corridor_id]),
            "local_occurrence_row_id": resolved_row["row_id"],
            "local_occurrence_gauge": "ROUND179_RESOLVED_CHILD",
            "official_key_ordinal": signature["official_key_ordinal"],
            "official_key_id": signature["official_key_id"],
            "Round225_known_connectivity_block_id": block_id,
            "strict_corridor_row_id": corridor_id,
            "derivation": (
                "STRICT_3D_CORRIDOR_FROM_ROUND211_SHEET_SEED_TO_"
                "EXACT_POSITIVE_AREA_RESOLVED_INTERFACE_PATCH"
            ),
            "known_block_incidence_attachment_credit": 1,
            **zero_credits(),
        }))

    expected_corridors.sort(key=lambda row: row["strict_corridor_row_id"])
    expected_deltas.sort(key=lambda row: row["incidence_delta_row_id"])
    need(
        candidate["formal_strict_sheet_interface_corridor_ledger"]
        == make_ledger(expected_corridors, "strict_corridor_row_id")
        and candidate[
            "formal_occurrence_known_block_incidence_delta_ledger"
        ] == make_ledger(expected_deltas, "incidence_delta_row_id"),
        "candidate ledgers",
    )

    remaining_rows = [
        classifications[identifier] for identifier in missing_ids
    ]
    type_histogram = Counter(
        row["classification_type"] for row in remaining_rows
    )
    key_histogram = Counter(
        len(row["candidate_exact_key_ids"]) for row in remaining_rows
    )
    expected_census = {
        "Round230_remote_exact_signature_reference_count": 12,
        "strict_depth2_corridor_count": 12,
        "positive_3D_Round208_region_overlap_count": 12,
        "positive_2D_resolved_interface_patch_count": 12,
        "direct_Round211_sheet_seeded_block_count": 12,
        "distinct_exact_key_count": len({
            row["official_key_ordinal"] for row in expected_deltas
        }),
        "new_occurrence_known_block_incidence_count": 12,
        "pre_Round240_occurrences_with_known_block_incidence": 35_896,
        "post_Round240_occurrences_with_known_block_incidence": 35_908,
        "post_Round240_occurrences_without_known_block_incidence": 18_060,
        "local_occurrence_count": 53_968,
        "remaining_Round239_interface_without_Round225_block_reference_count":
            8_500,
        "remaining_classification_type_histogram":
            dict(sorted(type_histogram.items())),
        "remaining_candidate_key_count_histogram": {
            str(key): value for key, value in sorted(key_histogram.items())
        },
        "strict_factor_profile_histogram": {
            "|".join(profile): count
            for profile, count in sorted(profiles.items())
        },
    }
    need(
        candidate["census"] == expected_census
        and candidate["remaining_no_block_reference_interface_ids_sha256"]
        == digest(missing_ids)
        and candidate["strict_nonpromotion"]["CM2"] == "NO-GO_FOR_CLAIM"
        and candidate["strict_nonpromotion"]["Gate5"] == "10/18",
        "candidate census and no-go",
    )
    return {
        "status": "PASS_INDEPENDENT_ROUND240",
        "candidate_sha256": PINS[
            "cm2_round240_source_g_remote_sheet_interface_corridor_incidence_certificate.json"
        ],
        "candidate_result_sha256": digest(candidate),
        "producer_imported_or_executed": False,
        "independently_recomputed_strict_corridor_count": 12,
        "independently_recomputed_incidence_delta_count": 12,
        "post_Round240_occurrences_with_known_block_incidence": 35_908,
        "post_Round240_occurrences_without_known_block_incidence": 18_060,
        "remaining_no_block_reference_interface_count": 8_500,
        "strict_nonpromotion_reconfirmed": True,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-write", action="store_true")
    arguments = parser.parse_args()
    result = verify()
    document = {
        "schema": (
            "cm2.round240.source-g-remote-sheet-interface-corridor-"
            "incidence.verification.v1"
        ),
        "result": result,
        "result_sha256": digest(result),
    }
    data = canonical(document) + b"\n"
    if not arguments.no_write:
        safe_write(data)
    print(result["status"])
    print(json.dumps(result, sort_keys=True))
    print(f"verification_result_sha256={document['result_sha256']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
