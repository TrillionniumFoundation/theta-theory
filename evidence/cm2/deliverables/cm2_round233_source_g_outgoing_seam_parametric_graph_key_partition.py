#!/usr/bin/env python3
"""Certify the Round233 outgoing-seam parametric graph key partition."""

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
OUTPUT = HERE / "cm2_round233_source_g_outgoing_seam_parametric_graph_key_partition_certificate.json"
SCHEMA = "cm2.round233.source-g-outgoing-seam-parametric-graph-key-partition.v1"
PINS = {
    "cm2_round179_source_g_residual_tube_arrangement_rows.json": "f20b42c1fed781779b537b4d45bf44233eae1ed3ee620b95177a80f0eb2b5e42",
    "cm2_round220_source_g_round179_resolved_child_boundary_atlas_certificate.json": "569a7849b53805ff4deca0eff9a6938a897942d3d682dfef27c27559135ce974",
    "cm2_round231_source_g_outgoing_seam_depth6_materialization_certificate.json": "7bc861ef4f2c2962dcf7c8e38839af2ec12477f9fc42d808be1b48d858745374",
    "cm2_round232_source_g_depth6_whole_origin_promotion_certificate.json": "a33d14fd7fd0ca0bb8e64efefd97be0839a5a8107b759f2219c14580ef3aa8c0",
    "cm2_round179_source_g_residual_tube_arrangement.py": "8c568c58d82708a7ab549f126c1fcedfccff563d1d00e3c1f7e6545b4b0d29ab",
    "cm2_round174_source_g_unique_first_dynamic_occurrence_materialization_verifier.py": "c7ead7c9cb8b4d7b8680e64bfb7870e5c5f5e39277e7c7d3d08a62b600f5c058",
}


def need(ok: bool, label: str) -> None:
    if not ok:
        raise RuntimeError(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode()


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def read_pinned(name: str, maximum: int = 400_000_000) -> bytes:
    path = HERE / name
    info = path.lstat()
    need(stat.S_ISREG(info.st_mode) and not path.is_symlink() and info.st_nlink == 1, f"regular:{name}")
    need(0 < info.st_size <= maximum, f"size:{name}")
    raw = path.read_bytes()
    need(hashlib.sha256(raw).hexdigest() == PINS[name], f"pin:{name}")
    return raw


def load_result(name: str) -> dict[str, Any]:
    document = json.loads(read_pinned(name))
    need(set(document) == {"schema", "result", "result_sha256"}, f"envelope:{name}")
    need(digest(document["result"]) == document["result_sha256"], f"digest:{name}")
    return document["result"]


def unpack(document: dict[str, Any], table: str) -> list[dict[str, Any]]:
    columns = document["row_column_schemas"][table]
    return [dict(zip(columns, row, strict=True)) for row in document[table]]


def signature(row: dict[str, Any]) -> dict[str, Any]:
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


def side_signature(base: dict[str, Any], cell: str) -> dict[str, Any]:
    result = dict(base)
    result["outgoing_cell"] = cell
    result["target_chart"] = f"{base['target_lift'][0]}:{cell}"
    return result


def cell_from_sign(axis: str, sign_name: str) -> str:
    need(sign_name in {"STRICT_POSITIVE", "STRICT_NEGATIVE"}, f"strict component:{axis}")
    if axis == "x":
        return "E" if sign_name == "STRICT_POSITIVE" else "W"
    return "N" if sign_name == "STRICT_POSITIVE" else "S"


def safe_write(data: bytes) -> None:
    descriptor, name = tempfile.mkstemp(prefix=f".{OUTPUT.name}.", suffix=".tmp", dir=HERE)
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


def build() -> dict[str, Any]:
    for name in PINS:
        read_pinned(name, 5_000_000 if name.endswith(".py") else 400_000_000)
    import cm2_round179_source_g_residual_tube_arrangement as r179

    rows179 = load_result("cm2_round179_source_g_residual_tube_arrangement_rows.json")
    origins = {row["origin_row_id"]: row for row in unpack(rows179, "origin_tube_rows")}
    retained = {row["row_id"]: row for row in unpack(rows179, "retained_3d_child_rows")}
    resolved = {row["row_id"]: row for row in unpack(rows179, "resolved_3d_child_rows")}
    round220 = load_result("cm2_round220_source_g_round179_resolved_child_boundary_atlas_certificate.json")
    table = round220["coordinate_boundary_atlas"]["tables"]["one_step_split_interface_rows"]
    interfaces = {
        row["split_interface_id"]: row
        for row in (dict(zip(table["columns"], packed, strict=True)) for packed in table["rows"])
    }
    round231 = load_result("cm2_round231_source_g_outgoing_seam_depth6_materialization_certificate.json")
    round232 = load_result("cm2_round232_source_g_depth6_whole_origin_promotion_certificate.json")
    prior_promoted = {row["Round220_split_interface_id"] for row in round232["whole_origin_promotion_rows"]}
    unresolved_summaries = [row for row in round231["root_summary_rows"] if row["depth6_retained_frontier_count"] > 0]
    need(len(unresolved_summaries) == 3_148 and len(prior_promoted) == 2_220, "root partition")
    released_by_interface: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in round231["resolved_descendant_rows"]:
        released_by_interface[row["Round220_split_interface_id"]].append(row)
    rows = []
    face_histogram: Counter[str] = Counter()
    derivative_histogram: Counter[str] = Counter()
    side_pair_histogram: Counter[str] = Counter()
    released_count = 0
    for summary in unresolved_summaries:
        interface_id = summary["Round220_split_interface_id"]
        interface = interfaces[interface_id]
        retained_id = summary["Round179_retained_child_row_id"]
        retained_row = retained[retained_id]
        origin = origins[retained_row["origin_row_id"]]
        need(origin["resolved_child_count"] == 1 and origin["retained_child_count"] == 1 and origin["guard_child_count"] == 0, f"partition:{interface_id}")
        need(origin["original_reason_labels"] == ["outgoing_chart_seam"], f"reason:{interface_id}")
        sibling_id = interface["lower_child_row_id"] if interface["lower_child_kind"] == "RESOLVED" else interface["upper_child_row_id"]
        sibling = resolved[sibling_id]
        sibling_signature = signature(sibling)
        need(sibling_signature["target_lift"] == origin["owner_target"], f"owner:{interface_id}")
        box = r179.box_from(retained_row["box"], len(retained_row["refinement_path"]), retained_row["row_id"])
        geometry = r179.interval_geometry(retained_row["chart"], origin["owner_target"], box)
        x_sign = r179.sign(geometry["outgoing_x"][0])
        y_sign = r179.sign(geometry["outgoing_y"][0])
        derivative_sign = r179.sign(geometry["outgoing_equality"][1][0])
        x_cell = cell_from_sign("x", x_sign)
        y_cell = cell_from_sign("y", y_sign)
        x_signature = side_signature(sibling_signature, x_cell)
        y_signature = side_signature(sibling_signature, y_cell)
        need(x_signature["official_key_id"] == y_signature["official_key_id"], f"side key:{interface_id}")
        lower_face = r179.interval_geometry(retained_row["chart"], origin["owner_target"], r179.fixed_axis_face(box, "t", False))["outgoing_equality"][0]
        upper_face = r179.interval_geometry(retained_row["chart"], origin["owner_target"], r179.fixed_axis_face(box, "t", True))["outgoing_equality"][0]
        face_classification = r179.face_classification(lower_face, upper_face)
        lower_cell = y_cell if derivative_sign == "STRICT_POSITIVE" else x_cell
        upper_cell = x_cell if derivative_sign == "STRICT_POSITIVE" else y_cell
        released = released_by_interface[interface_id]
        released_count += len(released)
        allowed = {digest(x_signature), digest(y_signature)}
        need(all(digest(row["local_return_signature"]) in allowed for row in released), f"released side:{interface_id}")
        need(all(row["local_return_signature"]["official_key_id"] == sibling_signature["official_key_id"] for row in released), f"released key:{interface_id}")
        face_histogram[face_classification] += 1
        derivative_histogram[derivative_sign] += 1
        side_pair_histogram[f"{lower_cell}->{upper_cell}"] += 1
        rows.append({
            "parametric_graph_partition_row_id": "round233-graph-key-partition:" + digest(interface_id),
            "Round220_split_interface_id": interface_id,
            "origin_row_id": retained_row["origin_row_id"],
            "Round179_resolved_sibling_row_id": sibling_id,
            "Round179_retained_child_row_id": retained_id,
            "source_chart": retained_row["chart"],
            "target_lift": origin["owner_target"],
            "equation": "target_normal_x^2-target_normal_y^2=0",
            "strict_t_derivative_sign": derivative_sign,
            "strict_outgoing_x_sign": x_sign,
            "strict_outgoing_y_sign": y_sign,
            "lower_t_side_outgoing_cell": lower_cell,
            "upper_t_side_outgoing_cell": upper_cell,
            "x_dominant_signature": x_signature,
            "y_dominant_signature": y_signature,
            "shared_official_key_row": sibling_signature["official_key_row"],
            "shared_official_key_ordinal": sibling_signature["official_key_ordinal"],
            "shared_official_key_id": sibling_signature["official_key_id"],
            "retained_root_t_face_classification": face_classification,
            "seam_dimension": 2,
            "seam_three_dimensional_coordinate_volume": 0,
            "retained_root_exact_key_constant_off_seam": True,
            "whole_origin_local_exact_key_disposition_credit": 1,
            "known_block_incidence_credit": 0,
            "maximal_component_credit": 0,
            "global_exact_key_fibre_credit": 0,
        })
    rows.sort(key=lambda row: row["parametric_graph_partition_row_id"])
    all_interfaces = prior_promoted | {row["Round220_split_interface_id"] for row in rows}
    need(len(rows) == 3_148 and len(all_interfaces) == 5_368, "channel exhaustion")
    census = {
        "previously_whole_signature_promoted_root_count": len(prior_promoted),
        "new_parametric_graph_key_partition_root_count": len(rows),
        "outgoing_seam_channel_whole_origin_local_exact_key_disposed_count": len(all_interfaces),
        "outgoing_seam_channel_root_count": 5_368,
        "released_descendants_cross_checked_count": released_count,
        "strict_component_sign_root_count": len(rows),
        "strict_t_derivative_root_count": len(rows),
        "distinct_shared_official_key_count": len({row["shared_official_key_ordinal"] for row in rows}),
        "retained_root_t_face_classification_histogram": dict(sorted(face_histogram.items())),
        "strict_t_derivative_sign_histogram": dict(sorted(derivative_histogram.items())),
        "lower_to_upper_side_cell_histogram": dict(sorted(side_pair_histogram.items())),
    }
    return {
        "status": "CERTIFIED_3148_PARAMETRIC_GRAPH_KEY_PARTITIONS_AND_5368_OUTGOING_SEAM_LOCAL_KEY_DISPOSITIONS",
        "census": census,
        "scope_contract": {
            "strict_t_derivative_makes_the_zero_set_a_parametric_graph_where_present": True,
            "strict_component_signs_determine_both_open_side_charts": True,
            "both_open_side_signatures_share_one_official_exact_key": True,
            "two_dimensional_seam_has_zero_three_dimensional_coordinate_volume": True,
            "graph_existence_over_every_base_point_not_required_for_exact_key_constancy": True,
        },
        "parametric_graph_key_partition_rows_sha256": digest(rows),
        "parametric_graph_key_partition_rows": rows,
        "strict_nonpromotion": {
            "known_block_incidence_credit": 0,
            "physical_component_credit": 0,
            "maximal_physical_component_credit": 0,
            "global_exact_key_fibre_credit": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "required_next": "attach the 5368 locally exact-key-disposed whole origins to retained event/common-refinement strata and frozen known blocks, then attack 2640 wall endpoint/count-transition roots",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--no-write", action="store_true")
    arguments = parser.parse_args()
    result = build()
    document = {"schema": SCHEMA, "result": result, "result_sha256": digest(result)}
    encoded = canonical(document) + b"\n"
    if not arguments.no_write:
        safe_write(encoded)
    print(result["status"])
    print(json.dumps(result["census"], sort_keys=True))
    print(f"result_sha256={document['result_sha256']}")
    print(f"certificate_sha256={hashlib.sha256(encoded).hexdigest()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
