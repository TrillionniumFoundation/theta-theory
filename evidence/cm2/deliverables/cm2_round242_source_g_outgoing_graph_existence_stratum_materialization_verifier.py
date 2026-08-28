#!/usr/bin/env python3
"""Independently verify the Round242 outgoing-graph strata."""

from __future__ import annotations

import argparse
from collections import Counter, deque
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
    / "cm2_round242_source_g_outgoing_graph_existence_stratum_materialization_verification.json"
)
SCHEMA = (
    "cm2.round242.source-g-outgoing-graph-existence-stratum-materialization."
    "verification.v1"
)
MAX_LOCAL_BASE_SPLIT_DEPTH = 24
PINS = {
    "cm2_round173_source_g_exact_return_signature_transport_certificate.json":
        "5ff82c5822f543109da0d50c0637d0d2f9148a738b1a21b16878c70e5505cf1a",
    "cm2_round174_source_g_unique_first_dynamic_occurrence_materialization_verifier.py":
        "c7ead7c9cb8b4d7b8680e64bfb7870e5c5f5e39277e7c7d3d08a62b600f5c058",
    "cm2_round179_source_g_residual_tube_arrangement.py":
        "8c568c58d82708a7ab549f126c1fcedfccff563d1d00e3c1f7e6545b4b0d29ab",
    "cm2_round179_source_g_residual_tube_arrangement_rows.json":
        "f20b42c1fed781779b537b4d45bf44233eae1ed3ee620b95177a80f0eb2b5e42",
    "cm2_round233_source_g_outgoing_seam_parametric_graph_key_partition_certificate.json":
        "cb2f74daa9836841ce311d8d555c2d94ba897f346a63c1e29551d7f99e8d1a41",
    "cm2_round239_source_g_unaccepted_interface_local_classification_ledger_certificate.json":
        "08d392f43fbc7a8d88c6d70b2c36aed7f8d710aac2f6569cf5910dba240ed9cf",
    "cm2_round240_source_g_remote_sheet_interface_corridor_incidence_certificate.json":
        "65285cd08662006015c388f8dbf1eb077ca2434d80b715dbdc99c332de629359",
    "cm2_round242_source_g_outgoing_graph_existence_stratum_materialization.py":
        "227cb00be470f33f87ee6b69612b319f8fedda51b6aa51a1ebe69ea59042de24",
    "cm2_round242_source_g_outgoing_graph_existence_stratum_materialization_certificate.json":
        "8d32c381e21c03aad6a531b7e5a527d295783b7e3e38baa1e6bcba20c40db22e",
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


def box_values(box: Any) -> list[str]:
    return [
        qstr(box.t0),
        qstr(box.t1),
        qstr(box.p0),
        qstr(box.p1),
        qstr(box.s0),
        qstr(box.s1),
    ]


def base_area(box: Any) -> Q:
    return (box.p1 - box.p0) * (box.s1 - box.s0)


def coordinate_volume(box: Any) -> Q:
    return (box.t1 - box.t0) * base_area(box)


def split_box(box: Any, axis: str, bit: int, atlas_box: Any) -> Any:
    need(axis in {"p", "s"} and bit in {0, 1}, "split request")
    if axis == "p":
        middle = (box.p0 + box.p1) / 2
        values = (
            (box.t0, box.t1, box.p0, middle, box.s0, box.s1)
            if bit == 0
            else (box.t0, box.t1, middle, box.p1, box.s0, box.s1)
        )
    else:
        middle = (box.s0 + box.s1) / 2
        values = (
            (box.t0, box.t1, box.p0, box.p1, box.s0, middle)
            if bit == 0
            else (box.t0, box.t1, box.p0, box.p1, middle, box.s1)
        )
    return atlas_box(
        *values,
        box.depth + 1,
        f"{box.path}:{axis}{bit}",
    )


def split_axis(schedule: str, local_depth: int) -> str:
    if schedule == "P_ONLY":
        return "p"
    need(
        schedule == "P_S_ALTERNATING_FROM_P",
        f"schedule:{schedule}",
    )
    return "p" if local_depth % 2 == 0 else "s"


def evaluate_faces(
    r179: Any,
    source_chart: str,
    target_lift: str,
    box: Any,
) -> tuple[str, str, str]:
    lower = r179.interval_geometry(
        source_chart,
        target_lift,
        r179.fixed_axis_face(box, "t", False),
    )["outgoing_equality"][0]
    upper = r179.interval_geometry(
        source_chart,
        target_lift,
        r179.fixed_axis_face(box, "t", True),
    )["outgoing_equality"][0]
    return (
        r179.face_classification(lower, upper),
        r179.sign(lower),
        r179.sign(upper),
    )


def safe_write(data: bytes) -> None:
    descriptor, name = tempfile.mkstemp(
        prefix=".round242-verifier.",
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
        read_pinned(
            name,
            5_000_000 if name.endswith(".py") else 400_000_000,
        )

    import cm2_round179_source_g_residual_tube_arrangement as r179

    need(
        Path(r179.__file__).resolve()
        == (
            HERE
            / "cm2_round179_source_g_residual_tube_arrangement.py"
        ).resolve(),
        "interval kernel module",
    )
    need(r179.FLINT_VERSION == "0.9.0", "python-flint version")
    r179.ctx.prec = r179.PRECISION_BITS

    round173 = load_result(
        "cm2_round173_source_g_exact_return_signature_transport_certificate.json"
    )
    half_open_rule = round173[
        "outgoing_chart_contract"
    ]["diagonal_seam_rule"]
    need(
        half_open_rule == "E or W owns; N or S excludes",
        "half-open rule",
    )

    rows179 = load_result(
        "cm2_round179_source_g_residual_tube_arrangement_rows.json"
    )
    retained = {
        row["row_id"]: row
        for row in unpack(rows179, "retained_3d_child_rows")
    }
    round233 = load_result(
        "cm2_round233_source_g_outgoing_seam_parametric_graph_key_partition_certificate.json"
    )
    graph_rows = {
        row["Round220_split_interface_id"]: row
        for row in round233["parametric_graph_key_partition_rows"]
    }
    round239 = load_result(
        "cm2_round239_source_g_unaccepted_interface_local_classification_ledger_certificate.json"
    )
    graph_ids239 = {
        row["Round220_split_interface_id"]
        for row in round239["classification_ledger_rows"]
        if row["classification_type"] == "OUTGOING_SEAM_GRAPH_SHARED_KEY"
    }
    round240 = load_result(
        "cm2_round240_source_g_remote_sheet_interface_corridor_incidence_certificate.json"
    )
    attached_ids = {
        row["Round220_split_interface_id"]
        for row in round240[
            "formal_strict_sheet_interface_corridor_ledger"
        ]["rows"]
    }
    target_ids = sorted(graph_ids239 - attached_ids)
    need(
        len(graph_rows) == len(graph_ids239) == 3_148
        and set(graph_rows) == graph_ids239
        and len(attached_ids) == 12
        and len(target_ids) == 3_136,
        "target binding",
    )

    candidate = load_result(
        "cm2_round242_source_g_outgoing_graph_existence_stratum_materialization_certificate.json"
    )
    expected_root_rows: list[dict[str, Any]] = []
    expected_absence_rows: list[dict[str, Any]] = []
    expected_transition_rows: list[dict[str, Any]] = []
    classification_histogram: Counter[str] = Counter()
    schedule_histogram: Counter[str] = Counter()
    graph_depth_histogram: Counter[int] = Counter()
    absence_depth_histogram: Counter[int] = Counter()
    owner_histogram: Counter[str] = Counter()
    transition_keys: set[int] = set()
    absence_keys: set[int] = set()
    total_search_nodes = 0

    for interface_id in target_ids:
        source = graph_rows[interface_id]
        retained_row = retained[source["Round179_retained_child_row_id"]]
        root_box = r179.box_from(
            retained_row["box"],
            len(retained_row["refinement_path"]),
            retained_row["row_id"],
        )
        geometry = r179.interval_geometry(
            source["source_chart"],
            source["target_lift"],
            root_box,
        )
        derivative_axes = r179.strict_derivative_axes(
            geometry["outgoing_equality"]
        )
        need(
            "t" in derivative_axes
            and "p" in derivative_axes
            and r179.sign(geometry["outgoing_equality"][1][0])
            == source["strict_t_derivative_sign"],
            f"derivative:{interface_id}",
        )
        schedule = (
            "P_S_ALTERNATING_FROM_P"
            if "s" in derivative_axes
            else "P_ONLY"
        )
        schedule_histogram[schedule] += 1

        queue = deque([(root_box, 0, "")])
        absent: list[dict[str, Any]] = []
        witness: tuple[Any, int, str, str, str] | None = None
        unresolved = 0
        search_nodes = 0
        max_depth = 0
        while queue:
            box, local_depth, path = queue.popleft()
            search_nodes += 1
            max_depth = max(max_depth, local_depth)
            classification, lower_sign, upper_sign = evaluate_faces(
                r179,
                source["source_chart"],
                source["target_lift"],
                box,
            )
            if classification == "FULL_BASE_UNIQUE_GRAPH":
                witness = (
                    box,
                    local_depth,
                    path,
                    lower_sign,
                    upper_sign,
                )
                break
            if classification == "STRICT_ZERO_ABSENT":
                need(
                    lower_sign == upper_sign
                    and lower_sign
                    in {"STRICT_NEGATIVE", "STRICT_POSITIVE"},
                    f"absence signs:{interface_id}:{path}",
                )
                absent.append({
                    "box": box,
                    "local_depth": local_depth,
                    "split_path": path,
                    "uniform_F_sign": lower_sign,
                })
                continue
            if local_depth == MAX_LOCAL_BASE_SPLIT_DEPTH:
                unresolved += 1
                continue
            axis = split_axis(schedule, local_depth)
            queue.extend([
                (
                    split_box(
                        box,
                        axis,
                        bit,
                        r179.r174.atlas.AtlasBox,
                    ),
                    local_depth + 1,
                    path + str(bit),
                )
                for bit in (0, 1)
            ])
        need(unresolved == 0, f"unresolved:{interface_id}")
        total_search_nodes += search_nodes

        common = {
            "Round220_split_interface_id": interface_id,
            "Round233_graph_partition_row_id":
                source["parametric_graph_partition_row_id"],
            "Round179_retained_child_row_id":
                source["Round179_retained_child_row_id"],
            "Round179_resolved_sibling_row_id":
                source["Round179_resolved_sibling_row_id"],
            "source_chart": source["source_chart"],
            "target_lift": source["target_lift"],
            "official_key_ordinal":
                source["shared_official_key_ordinal"],
            "official_key_id": source["shared_official_key_id"],
            "strict_t_derivative_sign":
                source["strict_t_derivative_sign"],
            "strict_derivative_axes": list(derivative_axes),
            "base_split_schedule": schedule,
            "configured_max_local_base_split_depth":
                MAX_LOCAL_BASE_SPLIT_DEPTH,
            "search_node_count": search_nodes,
            "max_local_base_split_depth_reached": max_depth,
            "known_block_incidence_credit": 0,
            "physical_component_credit": 0,
            "maximal_physical_component_credit": 0,
            "global_exact_key_fibre_credit": 0,
        }

        if witness is None:
            signs = {row["uniform_F_sign"] for row in absent}
            root_area = base_area(root_box)
            partition_area = sum(
                (base_area(row["box"]) for row in absent),
                Q(0),
            )
            need(
                len(signs) == 1
                and partition_area == root_area
                and search_nodes == 2 * len(absent) - 1,
                f"finite partition:{interface_id}",
            )
            uniform_sign = next(iter(signs))
            signature = (
                source["x_dominant_signature"]
                if uniform_sign == "STRICT_POSITIVE"
                else source["y_dominant_signature"]
            )
            local_rows: list[dict[str, Any]] = []
            for item in absent:
                box = item["box"]
                local_rows.append(closed({
                    "zero_absence_leaf_row_id":
                        "round242-zero-absence-leaf:"
                        + digest([
                            interface_id,
                            item["split_path"],
                            box_values(box),
                            item["uniform_F_sign"],
                        ]),
                    "Round220_split_interface_id": interface_id,
                    "split_path": item["split_path"],
                    "local_depth": item["local_depth"],
                    "base_split_schedule": schedule,
                    "closed_box": box_values(box),
                    "exact_base_area": qstr(base_area(box)),
                    "exact_coordinate_volume":
                        qstr(coordinate_volume(box)),
                    "lower_t_face_F_sign":
                        item["uniform_F_sign"],
                    "upper_t_face_F_sign":
                        item["uniform_F_sign"],
                    "strict_zero_absence_on_closed_box": True,
                    "transition_sheet_patch_credit": 0,
                    "known_block_incidence_credit": 0,
                }))
            local_rows.sort(
                key=lambda row: row["zero_absence_leaf_row_id"]
            )
            expected_absence_rows.extend(local_rows)
            classification = (
                "WHOLE_ROOT_STRICT_ZERO_ABSENT_BY_FINITE_BASE_PARTITION"
            )
            classification_histogram[classification] += 1
            absence_depth_histogram[max_depth] += 1
            absence_keys.add(source["shared_official_key_ordinal"])
            expected_root_rows.append(closed({
                "root_existence_row_id":
                    "round242-root-existence:"
                    + digest([interface_id, classification]),
                **common,
                "existence_classification": classification,
                "root_box": box_values(root_box),
                "root_exact_base_area": qstr(root_area),
                "zero_absence_uniform_F_sign": uniform_sign,
                "zero_absence_leaf_count": len(local_rows),
                "zero_absence_leaf_ids_sha256": digest([
                    row["zero_absence_leaf_row_id"]
                    for row in local_rows
                ]),
                "zero_absence_partition_exact_base_area":
                    qstr(partition_area),
                "whole_root_local_return_signature": signature,
                "whole_root_local_return_signature_credit": 1,
                "transition_sheet_patch_row_id": None,
                "local_positive_2D_transition_sheet_patch_credit": 0,
            }))
            continue

        box, local_depth, path, lower_sign, upper_sign = witness
        need(
            {lower_sign, upper_sign}
            == {"STRICT_NEGATIVE", "STRICT_POSITIVE"},
            f"graph signs:{interface_id}",
        )
        if source["strict_t_derivative_sign"] == "STRICT_POSITIVE":
            need(
                (lower_sign, upper_sign)
                == ("STRICT_NEGATIVE", "STRICT_POSITIVE"),
                f"graph orientation:{interface_id}",
            )
        else:
            need(
                (lower_sign, upper_sign)
                == ("STRICT_POSITIVE", "STRICT_NEGATIVE"),
                f"graph orientation:{interface_id}",
            )
        owner_signature = source["x_dominant_signature"]
        shadow_signature = source["y_dominant_signature"]
        owner_cell = owner_signature["outgoing_cell"]
        shadow_cell = shadow_signature["outgoing_cell"]
        need(
            owner_cell in {"E", "W"}
            and shadow_cell in {"N", "S"},
            f"owner pair:{interface_id}",
        )
        owner_side = (
            "LOWER_T_SIDE"
            if source["lower_t_side_outgoing_cell"] == owner_cell
            else "UPPER_T_SIDE"
        )
        need(
            (
                owner_side == "LOWER_T_SIDE"
                and source["upper_t_side_outgoing_cell"]
                == shadow_cell
            )
            or (
                owner_side == "UPPER_T_SIDE"
                and source["lower_t_side_outgoing_cell"]
                == shadow_cell
            ),
            f"owner side:{interface_id}",
        )
        transition_id = (
            "round242-positive-2d-transition-sheet-patch:"
            + digest([
                interface_id,
                path,
                box_values(box),
                owner_cell,
                shadow_cell,
            ])
        )
        expected_transition_rows.append(closed({
            "transition_sheet_patch_row_id": transition_id,
            "Round220_split_interface_id": interface_id,
            "Round233_graph_partition_row_id":
                source["parametric_graph_partition_row_id"],
            "Round179_retained_child_row_id":
                source["Round179_retained_child_row_id"],
            "source_chart": source["source_chart"],
            "target_lift": source["target_lift"],
            "official_key_ordinal":
                source["shared_official_key_ordinal"],
            "official_key_id": source["shared_official_key_id"],
            "equation": "target_normal_x^2-target_normal_y^2=0",
            "parameterization": "t=tau(p,s)",
            "witness_split_path": path,
            "witness_local_depth": local_depth,
            "closed_witness_box": box_values(box),
            "closed_base_rectangle": [
                qstr(box.p0),
                qstr(box.p1),
                qstr(box.s0),
                qstr(box.s1),
            ],
            "exact_positive_base_projection_area":
                qstr(base_area(box)),
            "lower_t_face_F_sign": lower_sign,
            "upper_t_face_F_sign": upper_sign,
            "strict_t_derivative_sign":
                source["strict_t_derivative_sign"],
            "unique_graph_point_for_every_closed_base_point": True,
            "graph_strictly_interior_to_t_interval": True,
            "local_dimension": 2,
            "three_dimensional_coordinate_volume": 0,
            "Round173_half_open_rule": half_open_rule,
            "owner_outgoing_cell": owner_cell,
            "shadow_outgoing_cell": shadow_cell,
            "owner_t_side": owner_side,
            "owner_signature": owner_signature,
            "shadow_signature": shadow_signature,
            "signature_difference_field_allowlist": [
                "outgoing_cell",
                "target_chart",
            ],
            "formal_half_open_owner_credit": 1,
            "local_positive_2D_transition_sheet_patch_credit": 1,
            "known_block_incidence_credit": 0,
            "physical_component_credit": 0,
            "maximal_physical_component_credit": 0,
            "global_exact_key_fibre_credit": 0,
        }))
        classification = (
            "POSITIVE_2D_UNIQUE_GRAPH_PATCH_WITH_HALF_OPEN_OWNER"
        )
        classification_histogram[classification] += 1
        graph_depth_histogram[local_depth] += 1
        owner_histogram[owner_cell] += 1
        transition_keys.add(source["shared_official_key_ordinal"])
        expected_root_rows.append(closed({
            "root_existence_row_id":
                "round242-root-existence:"
                + digest([interface_id, classification]),
            **common,
            "existence_classification": classification,
            "root_box": box_values(root_box),
            "root_exact_base_area": qstr(base_area(root_box)),
            "zero_absence_uniform_F_sign": None,
            "zero_absence_leaf_count": 0,
            "zero_absence_leaf_ids_sha256": digest([]),
            "zero_absence_partition_exact_base_area": "0",
            "whole_root_local_return_signature": None,
            "whole_root_local_return_signature_credit": 0,
            "transition_sheet_patch_row_id": transition_id,
            "local_positive_2D_transition_sheet_patch_credit": 1,
        }))

    expected_root_rows.sort(
        key=lambda row: row["root_existence_row_id"]
    )
    expected_absence_rows.sort(
        key=lambda row: row["zero_absence_leaf_row_id"]
    )
    expected_transition_rows.sort(
        key=lambda row: row["transition_sheet_patch_row_id"]
    )
    expected_census = {
        "Round239_no_block_reference_interface_count": 8_500,
        "Round233_graph_candidate_interface_count": 3_148,
        "Round240_already_attached_graph_interface_count": 12,
        "Round242_audited_graph_interface_count": 3_136,
        "existence_classification_histogram":
            dict(sorted(classification_histogram.items())),
        "base_split_schedule_histogram":
            dict(sorted(schedule_histogram.items())),
        "whole_root_zero_absence_promotion_count": 2_872,
        "positive_2D_transition_sheet_patch_count":
            len(expected_transition_rows),
        "zero_absence_partition_leaf_count":
            len(expected_absence_rows),
        "total_adaptive_search_node_count": total_search_nodes,
        "graph_witness_local_depth_histogram": {
            str(depth): count
            for depth, count in sorted(graph_depth_histogram.items())
        },
        "zero_absence_root_max_local_depth_histogram": {
            str(depth): count
            for depth, count in sorted(absence_depth_histogram.items())
        },
        "maximum_local_base_split_depth_reached": max(
            row["max_local_base_split_depth_reached"]
            for row in expected_root_rows
        ),
        "half_open_owner_cell_histogram":
            dict(sorted(owner_histogram.items())),
        "distinct_transition_patch_exact_key_count":
            len(transition_keys),
        "distinct_zero_absence_exact_key_count": len(absence_keys),
        "unresolved_graph_existence_root_count": 0,
        "new_known_block_incidence_count": 0,
        "post_Round242_occurrences_with_known_block_incidence":
            round240["census"][
                "post_Round240_occurrences_with_known_block_incidence"
            ],
        "post_Round242_occurrences_without_known_block_incidence":
            round240["census"][
                "post_Round240_occurrences_without_known_block_incidence"
            ],
        "maximal_physical_component_assignment_count": 0,
        "global_exact_key_fibre_exhausted_count": 0,
    }
    need(
        len(expected_root_rows) == 3_136
        and len(expected_transition_rows) == 264
        and len(expected_absence_rows) == 8_400
        and candidate["census"] == expected_census
        and candidate[
            "formal_root_existence_classification_ledger"
        ] == ledger(expected_root_rows, "root_existence_row_id")
        and candidate[
            "formal_zero_absence_base_partition_ledger"
        ] == ledger(expected_absence_rows, "zero_absence_leaf_row_id")
        and candidate[
            "formal_positive_2D_transition_sheet_patch_ledger"
        ] == ledger(
            expected_transition_rows,
            "transition_sheet_patch_row_id",
        )
        and candidate["strict_nonpromotion"]["CM2"]
        == "NO-GO_FOR_CLAIM"
        and candidate["strict_nonpromotion"][
            "known_block_incidence_credit"
        ] == 0,
        "candidate exact reconstruction",
    )

    return {
        "status": "PASS_INDEPENDENT_ROUND242",
        "verified_Round242_graph_interface_count": 3_136,
        "verified_whole_root_zero_absence_count": 2_872,
        "verified_zero_absence_partition_leaf_count": 8_400,
        "verified_positive_2D_transition_sheet_patch_count": 264,
        "verified_unresolved_count": 0,
        "verified_half_open_owner_rule": half_open_rule,
        "verified_known_block_incidence_credit": 0,
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
