#!/usr/bin/env python3
"""Round182: clipped source-G graph collars and pair arrangements.

The input is the independently replayed Round179 attachment.  Round182 keeps
three distinct ledgers:

* the 57,896 still-partial *original tubes* and their exact positive-volume
  Round179 retained children;
* the outgoing/wall *predicate occurrences* carried by those tubes; and
* the global source-G exact-key fibres, to which this bounded local work gives
  no disposition credit.

Every regular graph claim uses a strict interval derivative.  Existence uses
endpoint brackets, never regularity alone.  G-target collars close directly
by parametric face normal forms.  W-target outgoing collars receive at most
six dyadic s-splits.  Pair intersections use an actual nonzero 2x2 Jacobian
minor and interval-Newton inclusion in p; a nonzero minor alone is never
treated as an existence proof.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import stat
import tempfile
from collections import Counter, defaultdict
from fractions import Fraction as Q
from pathlib import Path
from typing import Any, Callable

from flint import arb, ctx, __version__ as FLINT_VERSION

import cm2_round179_source_g_residual_tube_arrangement_verifier as r179


HERE = Path(__file__).resolve().parent
PRODUCER = Path(__file__).resolve()
OUTPUT = HERE / (
    "cm2_round182_source_g_clipped_graph_and_pair_arrangement_certificate.json"
)
ATTACHMENT = HERE / (
    "cm2_round182_source_g_clipped_graph_and_pair_arrangement_rows.json"
)
VERIFIER = HERE / (
    "cm2_round182_source_g_clipped_graph_and_pair_arrangement_verifier.py"
)
VERIFICATION = HERE / (
    "cm2_round182_source_g_clipped_graph_and_pair_arrangement_verification.json"
)
REPORT = HERE / (
    "cm2_round182_source_g_clipped_graph_and_pair_arrangement_report.md"
)
COLD_REPLAY = HERE / (
    "cm2_round182_source_g_clipped_graph_and_pair_arrangement_cold_replay.md"
)
MANIFEST = HERE / (
    "cm2_round182_source_g_clipped_graph_and_pair_arrangement_manifest.sha256"
)
SCHEMA = "cm2.round182.source-g-clipped-graph-and-pair-arrangement.v1"
ATTACHMENT_SCHEMA = (
    "cm2.round182.source-g-clipped-graph-and-pair-arrangement-rows.v1"
)
STATUS = (
    "CERTIFIED_BOUNDED_PARTIAL_SOURCE_G_CLIPPED_GRAPH_AND_PAIR_ARRANGEMENT__"
    "NO_GLOBAL_EXACT_KEY_DISPOSITION_OR_D02_PROMOTION"
)
PRECISION_BITS = 256
W_OUTGOING_MAX_S_SPLITS = 6
G_TARGET_MAX_P_SPLITS = 6
SOURCE_G_KEY_COUNT = 224580

R179P = "cm2_round179_source_g_residual_tube_arrangement.py"
R179C = "cm2_round179_source_g_residual_tube_arrangement_certificate.json"
R179A = "cm2_round179_source_g_residual_tube_arrangement_rows.json"
R179V = "cm2_round179_source_g_residual_tube_arrangement_verifier.py"
R179O = "cm2_round179_source_g_residual_tube_arrangement_verification.json"
R179M = "cm2_round179_source_g_residual_tube_arrangement_manifest.sha256"
R174V = (
    "cm2_round174_source_g_unique_first_dynamic_occurrence_materialization_"
    "verifier.py"
)
G5M = "cm2-gate5-return-word-three-norm-frontier-manifest-2026-07-16.json"

PINS = {
    R179P: "8c568c58d82708a7ab549f126c1fcedfccff563d1d00e3c1f7e6545b4b0d29ab",
    R179C: "edc2c538dc04a93c2b873f53e07b5c97c6b395a1d107e7ed2de4cf2c4bd35111",
    R179A: "f20b42c1fed781779b537b4d45bf44233eae1ed3ee620b95177a80f0eb2b5e42",
    R179V: "292719cedfb4d5b802bf87a48314b5237f7b4438e4615d124d716f497044e679",
    R179O: "37eaa14cd870df64a12c2434deafe5fdead5cec303f5530208f07c11836736bc",
    R179M: "8fd5ae3a0cdd0c3321c0f8ffe6183ab57d31088b96523fa41ce0ebbe10d78b76",
    R174V: "c7ead7c9cb8b4d7b8680e64bfb7870e5c5f5e39277e7c7d3d08a62b600f5c058",
    G5M: "47e84e8b75b289b7a5db4afcbd7dfa8dac909d2f76fa1c95ef290546d031a866",
}
R179_CERT_RESULT = (
    "0f57284c11c617349fe66877552c401f426efafbc75faa08948f099166e9cde3"
)
R179_ATTACHMENT_RESULT = (
    "a5468800c1d89cd307a5a26c608550b04db79c64c562fb12bedb22d6cec308cb"
)
R179_VERIFY_RESULT = (
    "ca2ec32d84edf55919a26f556fd8e9dfc39566ad876b0cb5537168fee2b28229"
)
R179_STATUS = (
    "CERTIFIED_BOUNDED_PARTIAL_SOURCE_G_RESIDUAL_TUBE_ARRANGEMENT__"
    "NO_GLOBAL_DISPOSITION_OR_D02_PROMOTION"
)


def canonical(value: Any) -> str:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"),
        ensure_ascii=False, allow_nan=False,
    )


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def require(condition: bool, label: str) -> None:
    if not condition:
        raise RuntimeError(label)


def qstr(value: Q) -> str:
    return (
        str(value.numerator)
        if value.denominator == 1
        else f"{value.numerator}/{value.denominator}"
    )


def make_id(prefix: str, payload: Any) -> str:
    return f"round182-{prefix}:{digest(payload)}"


def safe_input(path: Path, maximum: int) -> bytes:
    require(path.parent == HERE, f"input parent:{path.name}")
    require(path.exists() and not path.is_symlink(), f"input exists:{path.name}")
    info = path.stat()
    require(stat.S_ISREG(info.st_mode), f"input regular:{path.name}")
    require(info.st_nlink == 1, f"input hardlink:{path.name}")
    require(0 < info.st_size <= maximum, f"input size:{path.name}")
    return path.read_bytes()


def strict_decode(raw: bytes) -> dict[str, Any]:
    require(
        raw and len(raw) <= 180_000_000
        and not raw.startswith(b"\xef\xbb\xbf")
        and b"\x00" not in raw,
        "strict JSON bytes",
    )

    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            require(key not in result, f"duplicate key:{key}")
            result[key] = value
        return result

    def reject(token: str) -> None:
        raise ValueError(token)

    value = json.loads(
        raw.decode(), object_pairs_hook=unique,
        parse_constant=reject, parse_float=reject,
    )

    def walk(item: Any) -> None:
        if type(item) is str:
            require(
                "\x00" not in item
                and not any(0xD800 <= ord(c) <= 0xDFFF for c in item),
                "strict decoded string",
            )
        elif type(item) is list:
            for child in item:
                walk(child)
        elif type(item) is dict:
            for key, child in item.items():
                walk(key)
                walk(child)

    walk(value)
    require(type(value) is dict, "JSON top object")
    return value


def strict_load(path: Path, maximum: int) -> dict[str, Any]:
    return strict_decode(safe_input(path, maximum))


def unpack(table: list[list[Any]], columns: list[str]) -> list[dict[str, Any]]:
    return [dict(zip(columns, row, strict=True)) for row in table]


def pack(columns: list[str], row: dict[str, Any]) -> list[Any]:
    require(set(row) == set(columns), f"packed keys:{columns[0]}")
    return [row[column] for column in columns]


def load_round179() -> dict[str, Any]:
    require(FLINT_VERSION == "0.9.0", "python-flint version")
    for name, expected in PINS.items():
        require(
            hashlib.sha256(safe_input(HERE / name, 180_000_000)).hexdigest()
            == expected,
            f"pin:{name}",
        )
    certificate = strict_load(HERE / R179C, 2_000_000)
    attachment = strict_load(HERE / R179A, 180_000_000)
    verification = strict_load(HERE / R179O, 2_000_000)
    require(
        set(certificate) == {"schema", "result", "result_sha256"}
        and certificate["schema"] == r179.SCHEMA
        and certificate["result_sha256"]
        == R179_CERT_RESULT
        == digest(certificate["result"])
        and certificate["result"]["status"] == R179_STATUS,
        "Round179 certificate wrapper",
    )
    require(
        set(attachment) == {"schema", "result", "result_sha256"}
        and attachment["schema"] == r179.ATTACHMENT_SCHEMA
        and attachment["result_sha256"]
        == R179_ATTACHMENT_RESULT
        == digest(attachment["result"]),
        "Round179 attachment wrapper",
    )
    require(
        set(verification) == {"schema", "result", "result_sha256"}
        and verification["result_sha256"]
        == R179_VERIFY_RESULT
        == digest(verification["result"])
        and verification["result"]["status"] == "PASS"
        and verification["result"]["full_attachment_byte_for_byte_matched"]
        is True
        and verification["result"]["producer_imported_or_executed"] is False,
        "Round179 verification wrapper",
    )
    return attachment["result"]


def qarb(value: Q) -> arb:
    return arb(value.numerator) / value.denominator


def box_from(row: dict[str, Any]) -> Any:
    return r179.box_from(
        row["box"], len(row["refinement_path"]), row["row_id"]
    )


def geometry_value(
    origin: dict[str, Any],
    kind: str,
    meta: dict[str, Any],
    box: Any,
) -> tuple[Any, tuple[Any, ...]]:
    geometry = r179.independent_geometry(
        origin["chart"], origin["owner_target"], box
    )
    if kind == "OUTGOING":
        return geometry["outgoing_equality"]
    target_name = "hit_x" if meta["axis"] == "X" else "hit_y"
    return r179.subtract_wall(geometry[target_name], meta["integer_wall"])


def double_face(box: Any, t_upper: bool, axis: str, upper: bool) -> Any:
    return r179.face_box(r179.face_box(box, "t", t_upper), axis, upper)


def interval_newton_image(
    function: Callable[[Any], tuple[Any, tuple[Any, ...]]],
    box: Any,
    axis: str,
) -> tuple[bool, str]:
    axis_index = "tps".index(axis)
    lower = getattr(box, axis + "0")
    upper = getattr(box, axis + "1")
    midpoint = (lower + upper) / 2
    if axis == "p":
        mid_box = r179.face_box(
            r179.r174.atlas.AtlasBox(
                box.t0, box.t1, midpoint, midpoint,
                box.s0, box.s1, box.depth, box.path,
            ),
            "p", False,
        )
    elif axis == "s":
        mid_box = r179.face_box(
            r179.r174.atlas.AtlasBox(
                box.t0, box.t1, box.p0, box.p1,
                midpoint, midpoint, box.depth, box.path,
            ),
            "s", False,
        )
    else:
        mid_box = r179.r174.atlas.AtlasBox(
            midpoint, midpoint, box.p0, box.p1,
            box.s0, box.s1, box.depth, box.path,
        )
    midpoint_value = function(mid_box)[0]
    derivative = function(box)[1][axis_index]
    require(
        derivative is not None
        and r179.arb_sign(derivative) != "OVERWRAP",
        "interval Newton strict derivative",
    )
    domain = r179.r174.first_hit.arb_interval(lower, upper)
    newton = qarb(midpoint) - midpoint_value / derivative
    return domain.contains_interior(newton), newton.str(40)


def face_status(
    origin: dict[str, Any],
    kind: str,
    meta: dict[str, Any],
    box: Any,
    t_upper: bool,
) -> dict[str, Any]:
    face = r179.face_box(box, "t", t_upper)
    function = lambda child: geometry_value(origin, kind, meta, child)
    value = function(face)
    value_sign = r179.arb_sign(value[0])
    if value_sign != "OVERWRAP":
        return {
            "kind": "STRICT",
            "resolved_sign": value_sign,
            "axis": None,
            "derivative_sign": None,
            "axis_lower_sign": None,
            "axis_upper_sign": None,
            "newton_interior": None,
            "newton_image": None,
        }
    curves = []
    absences = []
    for axis in ("p", "s"):
        axis_index = "tps".index(axis)
        derivative = value[1][axis_index]
        if (
            derivative is None
            or r179.arb_sign(derivative) == "OVERWRAP"
        ):
            continue
        lower = function(double_face(box, t_upper, axis, False))[0]
        upper = function(double_face(box, t_upper, axis, True))[0]
        lower_sign = r179.arb_sign(lower)
        upper_sign = r179.arb_sign(upper)
        classification = r179.face_kind(lower, upper)
        record = {
            "kind": (
                "CURVE"
                if classification == "FULL_BASE_UNIQUE_GRAPH"
                else "ABSENT"
            ),
            "resolved_sign": (
                None
                if classification == "FULL_BASE_UNIQUE_GRAPH"
                else lower_sign
            ),
            "axis": axis,
            "derivative_sign": r179.arb_sign(derivative),
            "axis_lower_sign": lower_sign,
            "axis_upper_sign": upper_sign,
            "newton_interior": None,
            "newton_image": None,
        }
        if classification == "FULL_BASE_UNIQUE_GRAPH":
            inside, image = interval_newton_image(function, face, axis)
            record["newton_interior"] = inside
            record["newton_image"] = image
            curves.append(record)
        elif classification == "STRICT_ZERO_ABSENT":
            absences.append(record)
    require(not (curves and absences), "conflicting face normal forms")
    if curves:
        return curves[0]
    if absences:
        return absences[0]
    return {
        "kind": "UNRESOLVED",
        "resolved_sign": None,
        "axis": None,
        "derivative_sign": None,
        "axis_lower_sign": None,
        "axis_upper_sign": None,
        "newton_interior": None,
        "newton_image": None,
    }


def encode_face(status: dict[str, Any]) -> str:
    signs = {
        "STRICT_POSITIVE": "+",
        "STRICT_NEGATIVE": "-",
        None: "_",
    }
    if status["kind"] == "STRICT":
        return "S" + signs[status["resolved_sign"]]
    if status["kind"] == "UNRESOLVED":
        return "U"
    prefix = "C" if status["kind"] == "CURVE" else "A"
    return "".join([
        prefix,
        status["axis"],
        signs[status["derivative_sign"]],
        signs[status["axis_lower_sign"]],
        signs[status["axis_upper_sign"]],
        signs[status["resolved_sign"]],
        (
            "1" if status["newton_interior"] is True
            else "0" if status["newton_interior"] is False
            else "_"
        ),
    ])


LEAF_COLUMNS = [
    "row_id", "occurrence_row_id", "retained_child_row_id",
    "base_refinement_path", "box", "coordinate_volume",
    "base_coordinate_area", "lower_t_face_status", "upper_t_face_status",
    "graph_classification", "two_dimensional_graph_sheet_count",
    "one_dimensional_clipping_curve_segment_count",
    "zero_dimensional_boundary_endpoint_incidence_count",
    "closed_3d_side_union_volume", "residual_3d_collar_volume",
]
COLLAR_COLUMNS = [
    "row_id", "Round179_occurrence_row_id", "origin_row_id", "parent_id",
    "chart", "owner_target", "kind", "reason_label", "equation",
    "target_obstacle", "strict_t_derivative_sign",
    "Round179_origin_already_fully_replaced",
    "Round179_retained_child_count", "Round179_retained_coordinate_volume",
    "bounded_base_split_axis", "bounded_base_split_depth",
    "closed_leaf_count", "closed_coordinate_volume",
    "residual_leaf_count", "residual_coordinate_volume",
    "full_base_graph_leaf_count", "absent_graph_leaf_count",
    "clipped_graph_leaf_count", "two_dimensional_graph_sheet_count",
    "one_dimensional_clipping_curve_segment_count",
    "zero_dimensional_boundary_endpoint_incidence_count",
    "fully_clipped_over_Round179_retained_children",
    "leaf_rows_sha256", "whole_original_tube_credit",
    "global_exact_key_disposition_credit", "provenance",
]
PAIR_COLUMNS = [
    "row_id", "Round179_pair_row_id", "origin_row_id", "parent_id", "chart",
    "owner_target", "reason_labels", "source_graph_equation",
    "source_graph_exact_factorization",
    "second_graph_equation", "source_graph_t_boundary_face",
    "existence_classification", "p_lower_sign", "p_upper_sign",
    "p_lower_value_interval", "p_upper_value_interval",
    "strict_p_derivative_sign", "strict_p_derivative_interval",
    "strict_source_t_derivative_sign",
    "strict_source_t_derivative_interval",
    "strict_2x2_Jacobian_minor_sign",
    "strict_2x2_Jacobian_minor_interval",
    "first_empty_source_factor_interval",
    "first_empty_target_factor_interval",
    "interval_newton_domain", "interval_newton_interior",
    "interval_newton_image", "actual_intersection_dimension",
    "actual_1D_intersection_component_count",
    "actual_boundary_0D_corner_incidence_count",
    "containing_Round179_retained_child_row_id",
    "integer_wall_endpoint_owner_status", "whole_original_tube_credit",
    "global_exact_key_disposition_credit", "provenance",
]
CORNER_COLUMNS = [
    "row_id", "pair_row_id", "origin_row_id", "boundary_axis",
    "boundary_face", "t_coordinate", "p_interval_newton_image",
    "s_coordinate", "strict_2x2_Jacobian_minor_sign",
    "isolated_zero_dimensional_boundary_corner",
    "corner_count_kind", "global_component_deduplication_credit",
    "global_exact_key_disposition_credit", "provenance",
]
SEAM_COLUMNS = [
    "row_id", "Round179_seam_row_id", "origin_row_id", "parent_id", "chart",
    "equation", "strict_t_derivative_sign", "lower_t_face_sign",
    "upper_t_face_sign", "exact_dimension", "half_open_owner_status",
    "is_half_open_owner", "Round179_retained_child_count",
    "Round179_retained_coordinate_volume", "closed_coordinate_volume",
    "whole_original_tube_credit", "global_exact_key_disposition_credit",
    "provenance",
]
ORIGIN_COLUMNS = [
    "row_id", "Round179_origin_row_id", "parent_id", "chart", "owner_target",
    "original_reason_labels", "original_coordinate_volume",
    "Round179_resolved_coordinate_volume", "Round179_guard_coordinate_volume",
    "Round179_retained_child_count", "Round179_retained_coordinate_volume",
    "collar_occurrence_count", "pair_arrangement_count",
    "source_chart_seam_count", "closed_Round182_retained_coordinate_volume",
    "residual_Round182_retained_coordinate_volume",
    "fully_geometrically_replaced_original_tube",
    "released_local_exact_key_count_carried_from_Round179",
    "Round182_released_global_exact_key_count",
    "global_exact_key_disposition_credit", "provenance",
]
CARRY_COLUMNS = [
    "row_id", "Round179_row_id", "origin_row_id", "predicate_kind",
    "classification", "strict_regularity_or_exact_graph",
    "existence_certification", "half_open_owner_status",
    "global_exact_key_disposition_credit", "provenance",
]


def leaf_record(
    occurrence_id: str,
    origin: dict[str, Any],
    retained: dict[str, Any],
    kind: str,
    path: list[str],
    box: Any,
    t_derivative_sign: str,
    lower: dict[str, Any],
    upper: dict[str, Any],
) -> dict[str, Any]:
    unresolved = (
        lower["kind"] == "UNRESOLVED"
        or upper["kind"] == "UNRESOLVED"
    )
    curve_count = sum(
        status["kind"] == "CURVE" for status in (lower, upper)
    )
    if unresolved:
        graph_class = "RESIDUAL_3D"
        graph_count = 0
    elif curve_count:
        graph_class = "CLIPPED_2D_BOUNDARY_1D"
        graph_count = 1
    else:
        signs = [lower["resolved_sign"], upper["resolved_sign"]]
        require(all(sign is not None for sign in signs), "resolved faces")
        if signs[0] != signs[1]:
            graph_class = "FULL_2D"
            graph_count = 1
        else:
            graph_class = "EMPTY"
            graph_count = 0
    volume = r179.r174.volume(box)
    base_area = (box.p1 - box.p0) * (box.s1 - box.s0)
    payload = [
        occurrence_id, retained["row_id"], path,
        r179.r174.box_values(box), graph_class,
        encode_face(lower), encode_face(upper),
    ]
    return {
        "row_id": make_id("collar-leaf", payload),
        "occurrence_row_id": occurrence_id,
        "retained_child_row_id": retained["row_id"],
        "base_refinement_path": path,
        "box": r179.r174.box_values(box),
        "coordinate_volume": qstr(volume),
        "base_coordinate_area": qstr(base_area),
        "lower_t_face_status": encode_face(lower),
        "upper_t_face_status": encode_face(upper),
        "graph_classification": graph_class,
        "two_dimensional_graph_sheet_count": graph_count,
        "one_dimensional_clipping_curve_segment_count": curve_count,
        "zero_dimensional_boundary_endpoint_incidence_count":
            2 * curve_count,
        "closed_3d_side_union_volume": qstr(Q(0) if unresolved else volume),
        "residual_3d_collar_volume": qstr(volume if unresolved else Q(0)),
    }


def process_retained_cell(
    occurrence_id: str,
    origin: dict[str, Any],
    retained: dict[str, Any],
    kind: str,
    meta: dict[str, Any],
    t_derivative_sign: str,
) -> list[dict[str, Any]]:
    initial = box_from(retained)
    is_w_outgoing = (
        kind == "OUTGOING"
        and origin["owner_target"].startswith("W[")
    )
    queue = [(initial, 0, [])]
    leaves = []
    while queue:
        box, depth, path = queue.pop()
        lower = face_status(origin, kind, meta, box, False)
        upper = face_status(origin, kind, meta, box, True)
        unresolved = (
            lower["kind"] == "UNRESOLVED"
            or upper["kind"] == "UNRESOLVED"
        )
        max_depth = (
            W_OUTGOING_MAX_S_SPLITS
            if is_w_outgoing
            else G_TARGET_MAX_P_SPLITS
        )
        split_axis = 2 if is_w_outgoing else 1
        split_name = "s" if is_w_outgoing else "p"
        if unresolved and depth < max_depth:
            children = r179.r174.bisect(box, split_axis)
            queue.append((
                children[1], depth + 1, [*path, split_name + "1"]
            ))
            queue.append((
                children[0], depth + 1, [*path, split_name + "0"]
            ))
            continue
        leaves.append(leaf_record(
            meta["row_id"], origin, retained, kind, path, box,
            t_derivative_sign, lower, upper,
        ))
    leaves.sort(key=lambda row: row["row_id"])
    require(
        sum((Q(row["coordinate_volume"]) for row in leaves), Q(0))
        == Q(retained["coordinate_volume"]),
        "retained cell exact leaf volume",
    )
    return leaves


def process_collar(
    origin: dict[str, Any],
    retained_rows: list[dict[str, Any]],
    kind: str,
    meta: dict[str, Any],
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    box = r179.box_from(
        origin["original_box"],
        len(origin["original_refinement_path"]),
        origin["origin_row_id"],
    )
    value = geometry_value(origin, kind, meta, box)
    derivative_sign = r179.arb_sign(value[1][0])
    require(derivative_sign != "OVERWRAP", "collar strict t derivative")
    leaves = []
    for retained in retained_rows:
        leaves.extend(process_retained_cell(
            meta["row_id"], origin, retained, kind, meta, derivative_sign
        ))
    leaves.sort(key=lambda row: row["row_id"])
    closed_volume = sum(
        (Q(row["closed_3d_side_union_volume"]) for row in leaves), Q(0)
    )
    residual_volume = sum(
        (Q(row["residual_3d_collar_volume"]) for row in leaves), Q(0)
    )
    input_volume = sum(
        (Q(row["coordinate_volume"]) for row in retained_rows), Q(0)
    )
    require(
        closed_volume + residual_volume == input_volume,
        "collar exact 3D conservation",
    )
    reason = (
        "outgoing_chart_seam"
        if kind == "OUTGOING"
        else meta["reason_label"]
    )
    equation = (
        meta["equation"] if kind == "OUTGOING" else meta["zero_equation"]
    )
    packed_leaves = [pack(LEAF_COLUMNS, row) for row in leaves]
    payload = [meta["row_id"], origin["origin_row_id"], kind]
    summary = {
        "row_id": make_id("collar", payload),
        "Round179_occurrence_row_id": meta["row_id"],
        "origin_row_id": origin["origin_row_id"],
        "parent_id": origin["parent_id"],
        "chart": origin["chart"],
        "owner_target": origin["owner_target"],
        "kind": kind,
        "reason_label": reason,
        "equation": equation,
        "target_obstacle": origin["owner_target"].split("[", 1)[0],
        "strict_t_derivative_sign": derivative_sign,
        "Round179_origin_already_fully_replaced": False,
        "Round179_retained_child_count": len(retained_rows),
        "Round179_retained_coordinate_volume": qstr(input_volume),
        "bounded_base_split_axis":
            "s"
            if origin["owner_target"].startswith("W[")
            else "p",
        "bounded_base_split_depth":
            W_OUTGOING_MAX_S_SPLITS
            if origin["owner_target"].startswith("W[")
            else G_TARGET_MAX_P_SPLITS,
        "closed_leaf_count": sum(
            Q(row["closed_3d_side_union_volume"]) > 0 for row in leaves
        ),
        "closed_coordinate_volume": qstr(closed_volume),
        "residual_leaf_count": sum(
            Q(row["residual_3d_collar_volume"]) > 0 for row in leaves
        ),
        "residual_coordinate_volume": qstr(residual_volume),
        "full_base_graph_leaf_count": sum(
            row["graph_classification"] == "FULL_2D"
            for row in leaves
        ),
        "absent_graph_leaf_count": sum(
            row["graph_classification"] == "EMPTY"
            for row in leaves
        ),
        "clipped_graph_leaf_count": sum(
            row["graph_classification"] == "CLIPPED_2D_BOUNDARY_1D"
            for row in leaves
        ),
        "two_dimensional_graph_sheet_count": sum(
            row["two_dimensional_graph_sheet_count"] for row in leaves
        ),
        "one_dimensional_clipping_curve_segment_count": sum(
            row["one_dimensional_clipping_curve_segment_count"]
            for row in leaves
        ),
        "zero_dimensional_boundary_endpoint_incidence_count": sum(
            row["zero_dimensional_boundary_endpoint_incidence_count"]
            for row in leaves
        ),
        "fully_clipped_over_Round179_retained_children":
            residual_volume == 0,
        "leaf_rows_sha256": digest(packed_leaves),
        "whole_original_tube_credit": 0,
        "global_exact_key_disposition_credit": 0,
        "provenance":
            "ROUND182_RETAINED_CHILD_GRAPH_COLLAR_DIMENSIONAL_LEDGER",
    }
    return summary, leaves


def zero_t_box(box: Any) -> Any:
    return r179.r174.atlas.AtlasBox(
        Q(0), Q(0), box.p0, box.p1, box.s0, box.s1,
        box.depth, box.path,
    )


def pair_and_corners(
    pair: dict[str, Any],
    origin: dict[str, Any],
    retained_rows: list[dict[str, Any]],
    wall_rows: list[dict[str, Any]],
    outgoing: dict[str, Any] | None,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    box = r179.box_from(
        origin["original_box"],
        len(origin["original_refinement_path"]),
        origin["origin_row_id"],
    )
    require(
        (box.t0 == 0) != (box.t1 == 0)
        and origin["owner_target"].startswith("G["),
        "pair source boundary and G target",
    )
    t_face = "LOWER_T_FACE" if box.t0 == 0 else "UPPER_T_FACE"
    containing = [
        row for row in retained_rows
        if (
            Q(row["box"][0]) == 0
            if t_face == "LOWER_T_FACE"
            else Q(row["box"][1]) == 0
        )
    ]
    require(len(containing) == 1, "unique retained child on t=0 boundary")
    empty_wall = next((
        row for row in wall_rows
        if row["source_factor_classification"] == "STRICT_NONZERO"
        and row["target_factor_classification"] == "STRICT_NONZERO"
    ), None)
    source_wall = next((
        row for row in wall_rows
        if row["source_factor_classification"] == "REGULAR_GRAPH"
    ), None)
    require(source_wall is not None, "pair exact source graph")
    cell = origin["chart"].split(":")[1]
    expected_source_axis = "Y" if cell in {"E", "W"} else "X"
    require(
        source_wall["axis"] == expected_source_axis
        and source_wall["integer_wall"] == 0,
        "symbolic source graph axis/wall identity",
    )
    source_name = (
        "source_x" if source_wall["axis"] == "X" else "source_y"
    )
    source_exact_factorization = (
        f"{source_name}=(9/25)*t"
    )
    source_function = lambda child: r179.subtract_wall(
        r179.independent_geometry(
            origin["chart"], origin["owner_target"], child
        )[source_name],
        source_wall["integer_wall"],
    )
    source_dual = source_function(zero_t_box(box))
    exact_source_dt = qarb(Q(9, 25))
    source_dt_sign = r179.arb_sign(exact_source_dt)
    require(
        source_dt_sign == "STRICT_POSITIVE"
        and r179.arb_sign(source_dual[0]) == "OVERWRAP",
        "source wall t=0 normal form",
    )
    require(
        source_dual[1][0].contains(exact_source_dt),
        "source wall t=0 normal form",
    )
    lower_sign = upper_sign = p_sign = jacobian_sign = None
    lower_interval = upper_interval = p_derivative_interval = None
    jacobian_interval = None
    empty_source_interval = empty_target_interval = None
    newton_inside = None
    newton_image = None
    second_equation = "EMPTY_FIRST_PREDICATE"
    corners: list[dict[str, Any]] = []
    if empty_wall is not None:
        geometry = r179.independent_geometry(
            origin["chart"], origin["owner_target"], box
        )
        empty_source_name = (
            "source_x" if empty_wall["axis"] == "X" else "source_y"
        )
        empty_target_name = (
            "hit_x" if empty_wall["axis"] == "X" else "hit_y"
        )
        empty_source = r179.subtract_wall(
            geometry[empty_source_name], empty_wall["integer_wall"]
        )[0]
        empty_target = r179.subtract_wall(
            geometry[empty_target_name], empty_wall["integer_wall"]
        )[0]
        require(
            r179.arb_sign(empty_source) != "OVERWRAP"
            and r179.arb_sign(empty_target) != "OVERWRAP",
            "first empty predicate strict margins",
        )
        empty_source_interval = empty_source.str(40)
        empty_target_interval = empty_target.str(40)
        existence = "EMPTY__ONE_PREDICATE_HAS_EMPTY_ZERO_SET"
        dimension = "EMPTY"
        component_count = 0
    else:
        if outgoing is not None:
            second_equation = outgoing["equation"]
            second_function = lambda child: r179.independent_geometry(
                origin["chart"], origin["owner_target"], child
            )["outgoing_equality"]
        else:
            target_wall = next(
                row for row in wall_rows
                if row["target_factor_classification"] == "REGULAR_GRAPH"
            )
            second_name = (
                "hit_x" if target_wall["axis"] == "X" else "hit_y"
            )
            second_equation = (
                f"target_{target_wall['axis'].lower()}-"
                f"{target_wall['integer_wall']}=0"
            )
            second_function = lambda child: r179.subtract_wall(
                r179.independent_geometry(
                    origin["chart"], origin["owner_target"], child
                )[second_name],
                target_wall["integer_wall"],
            )
        zero_box = zero_t_box(box)
        dual = second_function(zero_box)
        p_sign = r179.arb_sign(dual[1][1])
        require(p_sign != "OVERWRAP", "pair strict p derivative")
        lower = second_function(r179.face_box(zero_box, "p", False))[0]
        upper = second_function(r179.face_box(zero_box, "p", True))[0]
        lower_sign = r179.arb_sign(lower)
        upper_sign = r179.arb_sign(upper)
        lower_interval = lower.str(40)
        upper_interval = upper.str(40)
        p_derivative_interval = dual[1][1].str(40)
        classification = r179.face_kind(lower, upper)
        jacobian = exact_source_dt * dual[1][1]
        jacobian_sign = r179.arb_sign(jacobian)
        jacobian_interval = jacobian.str(40)
        require(
            jacobian_sign != "OVERWRAP",
            "pair strict 2x2 Jacobian minor",
        )
        if classification == "FULL_BASE_UNIQUE_GRAPH":
            newton_inside, newton_image = interval_newton_image(
                second_function, zero_box, "p"
            )
            require(newton_inside, "pair interval Newton inclusion")
            existence = (
                "UNIQUE_TRANSVERSE_1D_INTERSECTION_LINE__"
                "P_BRACKET_AND_INTERVAL_NEWTON"
            )
            dimension = "EXACT_DIMENSION_1"
            component_count = 1
            for face, coordinate in (
                ("LOWER_S_FACE", box.s0),
                ("UPPER_S_FACE", box.s1),
            ):
                payload = [
                    pair["row_id"], face, qstr(coordinate), newton_image
                ]
                corners.append({
                    "row_id": make_id("pair-corner", payload),
                    "pair_row_id": pair["row_id"],
                    "origin_row_id": origin["origin_row_id"],
                    "boundary_axis": "s",
                    "boundary_face": face,
                    "t_coordinate": "0",
                    "p_interval_newton_image": newton_image,
                    "s_coordinate": qstr(coordinate),
                    "strict_2x2_Jacobian_minor_sign": jacobian_sign,
                    "isolated_zero_dimensional_boundary_corner": True,
                    "corner_count_kind":
                        "BOUNDARY_INCIDENCE__NOT_GLOBAL_COMPONENT_COUNT",
                    "global_component_deduplication_credit": 0,
                    "global_exact_key_disposition_credit": 0,
                    "provenance":
                        "ROUND182_PAIR_LINE_INTERSECTED_WITH_EXACT_S_FACE",
                })
        else:
            require(
                classification == "STRICT_ZERO_ABSENT",
                "pair p-face classification",
            )
            existence = "EMPTY__STRICT_SAME_SIGN_P_FACES"
            dimension = "EMPTY"
            component_count = 0
    payload = [pair["row_id"], origin["origin_row_id"], existence]
    row = {
        "row_id": make_id("pair-arrangement", payload),
        "Round179_pair_row_id": pair["row_id"],
        "origin_row_id": origin["origin_row_id"],
        "parent_id": origin["parent_id"],
        "chart": origin["chart"],
        "owner_target": origin["owner_target"],
        "reason_labels": pair["reason_labels"],
        "source_graph_equation": "t=0",
        "source_graph_exact_factorization": source_exact_factorization,
        "second_graph_equation": second_equation,
        "source_graph_t_boundary_face": t_face,
        "existence_classification": existence,
        "p_lower_sign": lower_sign,
        "p_upper_sign": upper_sign,
        "p_lower_value_interval": lower_interval,
        "p_upper_value_interval": upper_interval,
        "strict_p_derivative_sign": p_sign,
        "strict_p_derivative_interval": p_derivative_interval,
        "strict_source_t_derivative_sign": source_dt_sign,
        "strict_source_t_derivative_interval": exact_source_dt.str(40),
        "strict_2x2_Jacobian_minor_sign": jacobian_sign,
        "strict_2x2_Jacobian_minor_interval": jacobian_interval,
        "first_empty_source_factor_interval": empty_source_interval,
        "first_empty_target_factor_interval": empty_target_interval,
        "interval_newton_domain": [qstr(box.p0), qstr(box.p1)],
        "interval_newton_interior": newton_inside,
        "interval_newton_image": newton_image,
        "actual_intersection_dimension": dimension,
        "actual_1D_intersection_component_count": component_count,
        "actual_boundary_0D_corner_incidence_count": len(corners),
        "containing_Round179_retained_child_row_id": containing[0]["row_id"],
        "integer_wall_endpoint_owner_status":
            "ANALYTIC_BOUNDARY_STRATUM__NO_ADJACENT_TUBE_DEDUP_CREDIT",
        "whole_original_tube_credit": 0,
        "global_exact_key_disposition_credit": 0,
        "provenance":
            "ROUND182_ENDPOINT_BRACKET_STRICT_JACOBIAN_AND_INTERVAL_NEWTON",
    }
    return row, corners


def build_rows(source: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    schemas = source["row_column_schemas"]
    origins_all = unpack(source["origin_tube_rows"], schemas["origin_tube_rows"])
    all_origin_by_id = {
        row["origin_row_id"]: row for row in origins_all
    }
    origins = {
        row["origin_row_id"]: row
        for row in origins_all
        if not row["fully_replaced_by_bounded_children"]
    }
    require(len(origins) == 57896, "Round179 partial origin census")
    retained_all = unpack(
        source["retained_3d_child_rows"],
        schemas["retained_3d_child_rows"],
    )
    retained_by_origin: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in retained_all:
        if row["origin_row_id"] in origins:
            retained_by_origin[row["origin_row_id"]].append(row)
    for rows in retained_by_origin.values():
        rows.sort(key=lambda row: row["row_id"])
    require(
        len(retained_by_origin) == 57896
        and sum(map(len, retained_by_origin.values())) == 106680,
        "Round179 retained child census",
    )
    outgoing_all = unpack(
        source["outgoing_normal_form_rows"],
        schemas["outgoing_normal_form_rows"],
    )
    walls_all = unpack(
        source["wall_normal_form_rows"],
        schemas["wall_normal_form_rows"],
    )
    seams_all = unpack(
        source["source_chart_seam_rows"],
        schemas["source_chart_seam_rows"],
    )
    pairs_all = unpack(
        source["pair_arrangement_candidate_rows"],
        schemas["pair_arrangement_candidate_rows"],
    )
    outgoing_by_origin = {
        row["origin_row_id"]: row
        for row in outgoing_all
        if row["origin_row_id"] in origins
    }
    walls_by_origin: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in walls_all:
        if row["origin_row_id"] in origins:
            walls_by_origin[row["origin_row_id"]].append(row)
    seams_by_origin = {
        row["origin_row_id"]: row
        for row in seams_all
        if row["origin_row_id"] in origins
    }
    pairs_by_origin = {
        row["origin_row_id"]: row
        for row in pairs_all
        if row["origin_row_id"] in origins
    }
    collar_tasks: dict[str, tuple[str, dict[str, Any]]] = {}
    require(
        sum(
            row["face_classification"]
            == "FACE_OVERWRAP_REGULAR_ZERO_SET_IF_PRESENT"
            for row in outgoing_all
        ) == 30444,
        "Round179 outgoing collar occurrence census",
    )
    for row in outgoing_all:
        if row["face_classification"] == (
            "FACE_OVERWRAP_REGULAR_ZERO_SET_IF_PRESENT"
        ):
            require(row["origin_row_id"] not in collar_tasks, "one collar/origin")
            collar_tasks[row["origin_row_id"]] = ("OUTGOING", row)
    require(
        sum(
            row["target_face_classification"]
            == "FACE_OVERWRAP_REGULAR_ZERO_SET_IF_PRESENT"
            for row in walls_all
        ) == 23776,
        "Round179 wall collar occurrence census",
    )
    for row in walls_all:
        if row["target_face_classification"] == (
            "FACE_OVERWRAP_REGULAR_ZERO_SET_IF_PRESENT"
        ):
            require(row["origin_row_id"] not in collar_tasks, "one collar/origin")
            collar_tasks[row["origin_row_id"]] = ("WALL", row)
    require(len(collar_tasks) == 54220, "unique collar origin census")

    collars = []
    leaves = []
    collar_by_origin = {}
    for index, origin_id in enumerate(sorted(collar_tasks)):
        origin = all_origin_by_id[origin_id]
        kind, meta = collar_tasks[origin_id]
        if origin_id in origins:
            summary, child_leaves = process_collar(
                origin, retained_by_origin[origin_id], kind, meta
            )
            collar_by_origin[origin_id] = summary
        else:
            require(
                origin["fully_replaced_by_bounded_children"] is True,
                "inactive collar origin replacement",
            )
            box = r179.box_from(
                origin["original_box"],
                len(origin["original_refinement_path"]),
                origin["origin_row_id"],
            )
            derivative_sign = r179.arb_sign(
                geometry_value(origin, kind, meta, box)[1][0]
            )
            require(
                derivative_sign != "OVERWRAP",
                "inactive collar strict t derivative",
            )
            reason = (
                "outgoing_chart_seam"
                if kind == "OUTGOING"
                else meta["reason_label"]
            )
            equation = (
                meta["equation"]
                if kind == "OUTGOING"
                else meta["zero_equation"]
            )
            payload = [meta["row_id"], origin_id, kind, "inactive"]
            summary = {
                "row_id": make_id("collar", payload),
                "Round179_occurrence_row_id": meta["row_id"],
                "origin_row_id": origin_id,
                "parent_id": origin["parent_id"],
                "chart": origin["chart"],
                "owner_target": origin["owner_target"],
                "kind": kind,
                "reason_label": reason,
                "equation": equation,
                "target_obstacle": origin["owner_target"].split("[", 1)[0],
                "strict_t_derivative_sign": derivative_sign,
                "Round179_origin_already_fully_replaced": True,
                "Round179_retained_child_count": 0,
                "Round179_retained_coordinate_volume": "0",
                "bounded_base_split_axis": "NOT_APPLICABLE",
                "bounded_base_split_depth": 0,
                "closed_leaf_count": 0,
                "closed_coordinate_volume": "0",
                "residual_leaf_count": 0,
                "residual_coordinate_volume": "0",
                "full_base_graph_leaf_count": 0,
                "absent_graph_leaf_count": 0,
                "clipped_graph_leaf_count": 0,
                "two_dimensional_graph_sheet_count": 0,
                "one_dimensional_clipping_curve_segment_count": 0,
                "zero_dimensional_boundary_endpoint_incidence_count": 0,
                "fully_clipped_over_Round179_retained_children": True,
                "leaf_rows_sha256": digest([]),
                "whole_original_tube_credit": 0,
                "global_exact_key_disposition_credit": 0,
                "provenance":
                    "ROUND179_ORIGIN_ALREADY_FULLY_REPLACED__"
                    "NO_RETAINED_3D_COLLAR_TO_RECOUNT",
            }
            child_leaves = []
        collars.append(summary)
        leaves.extend(child_leaves)
        if index and index % 4000 == 0:
            print(f"Round182 collars {index}/{len(collar_tasks)}", flush=True)

    pair_rows = []
    corner_rows = []
    for origin_id in sorted(pairs_by_origin):
        row, corners = pair_and_corners(
            pairs_by_origin[origin_id],
            origins[origin_id],
            retained_by_origin[origin_id],
            walls_by_origin[origin_id],
            outgoing_by_origin.get(origin_id),
        )
        pair_rows.append(row)
        corner_rows.extend(corners)

    seam_rows = []
    for origin_id in sorted(seams_by_origin):
        seam = seams_by_origin[origin_id]
        origin = origins[origin_id]
        retained = retained_by_origin[origin_id]
        volume = sum((Q(row["coordinate_volume"]) for row in retained), Q(0))
        owned = seam["half_open_owner_status"] == "E_OR_W_HALF_OPEN_OWNER"
        payload = [seam["row_id"], origin_id, owned]
        seam_rows.append({
            "row_id": make_id("source-seam-owner", payload),
            "Round179_seam_row_id": seam["row_id"],
            "origin_row_id": origin_id,
            "parent_id": origin["parent_id"],
            "chart": origin["chart"],
            "equation": seam["equation"],
            "strict_t_derivative_sign": seam["gradient_sign"],
            "lower_t_face_sign": seam["lower_t_face_sign"],
            "upper_t_face_sign": seam["upper_t_face_sign"],
            "exact_dimension": 2,
            "half_open_owner_status": seam["half_open_owner_status"],
            "is_half_open_owner": owned,
            "Round179_retained_child_count": len(retained),
            "Round179_retained_coordinate_volume": qstr(volume),
            "closed_coordinate_volume": qstr(volume),
            "whole_original_tube_credit": 0,
            "global_exact_key_disposition_credit": 0,
            "provenance":
                "ROUND182_PINNED_E_W_OWNS_N_S_EXCLUDES_SOURCE_DIAGONAL",
        })

    carry_rows = []
    for row in outgoing_all:
        if (
            row["origin_row_id"] in origins
            and row["face_classification"]
            != "FACE_OVERWRAP_REGULAR_ZERO_SET_IF_PRESENT"
        ):
            payload = ["outgoing", row["row_id"]]
            carry_rows.append({
                "row_id": make_id("carried-form", payload),
                "Round179_row_id": row["row_id"],
                "origin_row_id": row["origin_row_id"],
                "predicate_kind": "OUTGOING",
                "classification": row["face_classification"],
                "strict_regularity_or_exact_graph":
                    row["regularity_certification"],
                "existence_certification": row["existence_over_full_base"],
                "half_open_owner_status": "NOT_APPLICABLE",
                "global_exact_key_disposition_credit": 0,
                "provenance": "ROUND182_PINNED_ROUND179_NORMAL_FORM",
            })
    for row in walls_all:
        if (
            row["origin_row_id"] in origins
            and row["target_face_classification"]
            != "FACE_OVERWRAP_REGULAR_ZERO_SET_IF_PRESENT"
        ):
            payload = ["wall", row["row_id"]]
            carry_rows.append({
                "row_id": make_id("carried-form", payload),
                "Round179_row_id": row["row_id"],
                "origin_row_id": row["origin_row_id"],
                "predicate_kind": "WALL",
                "classification": canonical({
                    "source": row["source_factor_classification"],
                    "target": row["target_factor_classification"],
                    "target_face": row["target_face_classification"],
                }),
                "strict_regularity_or_exact_graph":
                    row["zero_set_dimension_account"],
                "existence_certification":
                    "CERTIFIED_FACTOR_NORMAL_FORMS",
                "half_open_owner_status":
                    "ANALYTIC_INTEGER_WALL_BOUNDARY_STRATUM",
                "global_exact_key_disposition_credit": 0,
                "provenance": "ROUND182_PINNED_ROUND179_FACTORIZATION",
            })

    origin_rows = []
    for origin_id in sorted(origins):
        origin = origins[origin_id]
        retained = retained_by_origin[origin_id]
        retained_volume = sum(
            (Q(row["coordinate_volume"]) for row in retained), Q(0)
        )
        collar = collar_by_origin.get(origin_id)
        if collar is None:
            closed_volume = retained_volume
            residual_volume = Q(0)
        else:
            closed_volume = Q(collar["closed_coordinate_volume"])
            residual_volume = Q(collar["residual_coordinate_volume"])
        require(
            Q(origin["resolved_child_coordinate_volume"])
            + Q(origin["guard_child_coordinate_volume"])
            + retained_volume
            == Q(origin["original_coordinate_volume"]),
            "original/Round179 volume conservation",
        )
        require(
            closed_volume + residual_volume == retained_volume,
            "Round182 retained volume conservation",
        )
        payload = [origin_id, qstr(closed_volume), qstr(residual_volume)]
        origin_rows.append({
            "row_id": make_id("origin-replacement", payload),
            "Round179_origin_row_id": origin_id,
            "parent_id": origin["parent_id"],
            "chart": origin["chart"],
            "owner_target": origin["owner_target"],
            "original_reason_labels": origin["original_reason_labels"],
            "original_coordinate_volume": origin["original_coordinate_volume"],
            "Round179_resolved_coordinate_volume":
                origin["resolved_child_coordinate_volume"],
            "Round179_guard_coordinate_volume":
                origin["guard_child_coordinate_volume"],
            "Round179_retained_child_count": len(retained),
            "Round179_retained_coordinate_volume": qstr(retained_volume),
            "collar_occurrence_count": int(collar is not None),
            "pair_arrangement_count": int(origin_id in pairs_by_origin),
            "source_chart_seam_count": int(origin_id in seams_by_origin),
            "closed_Round182_retained_coordinate_volume": qstr(closed_volume),
            "residual_Round182_retained_coordinate_volume":
                qstr(residual_volume),
            "fully_geometrically_replaced_original_tube":
                residual_volume == 0,
            "released_local_exact_key_count_carried_from_Round179":
                origin["released_exact_key_count"],
            "Round182_released_global_exact_key_count": 0,
            "global_exact_key_disposition_credit": 0,
            "provenance":
                "ROUND179_RELEASED_CHILDREN_PLUS_ROUND182_DIMENSIONAL_COMPLEX",
        })

    for table in (
        collars, leaves, pair_rows, corner_rows, seam_rows,
        carry_rows, origin_rows,
    ):
        table.sort(key=lambda row: row["row_id"])
        require(
            len({row["row_id"] for row in table}) == len(table),
            "Round182 row ID uniqueness",
        )
    require(
        len(collars) == 54220
        and len(pair_rows) == 336
        and len(corner_rows) == 224
        and len(seam_rows) == 472
        and len(origin_rows) == 57896,
        "Round182 principal row census",
    )
    return {
        "origin_replacement_rows": origin_rows,
        "collar_occurrence_rows": collars,
        "collar_leaf_rows": leaves,
        "pair_intersection_rows": pair_rows,
        "pair_boundary_corner_rows": corner_rows,
        "source_chart_seam_owner_rows": seam_rows,
        "carried_normal_form_rows": carry_rows,
    }


def statistics(rows: dict[str, list[dict[str, Any]]]) -> dict[str, Any]:
    origins = rows["origin_replacement_rows"]
    collars = rows["collar_occurrence_rows"]
    leaves = rows["collar_leaf_rows"]
    pairs = rows["pair_intersection_rows"]
    corners = rows["pair_boundary_corner_rows"]
    seams = rows["source_chart_seam_owner_rows"]
    retained_volume = sum(
        (Q(row["Round179_retained_coordinate_volume"]) for row in origins),
        Q(0),
    )
    closed_volume = sum(
        (
            Q(row["closed_Round182_retained_coordinate_volume"])
            for row in origins
        ),
        Q(0),
    )
    residual_volume = sum(
        (
            Q(row["residual_Round182_retained_coordinate_volume"])
            for row in origins
        ),
        Q(0),
    )
    require(
        retained_volume == Q("1768407/524288000")
        and closed_volume + residual_volume == retained_volume,
        "global Round182 retained volume conservation",
    )
    kind_target = Counter(
        (row["kind"], row["target_obstacle"]) for row in collars
    )
    graph_classes = Counter(row["graph_classification"] for row in leaves)
    pair_classes = Counter(row["existence_classification"] for row in pairs)
    both_curve_leaves = [
        row for row in leaves
        if row["lower_t_face_status"].startswith("C")
        and row["upper_t_face_status"].startswith("C")
    ]
    result = {
        "Round179_partial_original_tube_count": len(origins),
        "Round179_retained_3d_child_count": sum(
            row["Round179_retained_child_count"] for row in origins
        ),
        "Round179_retained_coordinate_volume": qstr(retained_volume),
        "Round182_fully_geometrically_replaced_original_tube_count": sum(
            row["fully_geometrically_replaced_original_tube"]
            for row in origins
        ),
        "Round182_residual_original_tube_count": sum(
            not row["fully_geometrically_replaced_original_tube"]
            for row in origins
        ),
        "Round182_closed_retained_coordinate_volume": qstr(closed_volume),
        "Round182_residual_retained_coordinate_volume":
            qstr(residual_volume),
        "collar_occurrence_count": len(collars),
        "inactive_collar_occurrence_on_Round179_fully_replaced_origin_count":
            sum(
                row["Round179_origin_already_fully_replaced"]
                for row in collars
            ),
        "active_collar_occurrence_on_partial_origin_count": sum(
            not row["Round179_origin_already_fully_replaced"]
            for row in collars
        ),
        "active_outgoing_collar_occurrence_count": sum(
            row["kind"] == "OUTGOING"
            and not row["Round179_origin_already_fully_replaced"]
            for row in collars
        ),
        "active_wall_collar_occurrence_count": sum(
            row["kind"] == "WALL"
            and not row["Round179_origin_already_fully_replaced"]
            for row in collars
        ),
        "outgoing_G_target_collar_occurrence_count":
            kind_target[("OUTGOING", "G")],
        "outgoing_W_target_collar_occurrence_count":
            kind_target[("OUTGOING", "W")],
        "wall_G_target_collar_occurrence_count":
            kind_target[("WALL", "G")],
        "collar_leaf_count": len(leaves),
        "closed_collar_leaf_count": sum(
            Q(row["closed_3d_side_union_volume"]) > 0 for row in leaves
        ),
        "residual_collar_leaf_count": sum(
            Q(row["residual_3d_collar_volume"]) > 0 for row in leaves
        ),
        "graph_leaf_classification_histogram":
            dict(sorted(graph_classes.items())),
        "two_dimensional_graph_sheet_count": sum(
            row["two_dimensional_graph_sheet_count"] for row in leaves
        ),
        "one_dimensional_clipping_curve_segment_count": sum(
            row["one_dimensional_clipping_curve_segment_count"]
            for row in leaves
        ),
        "zero_dimensional_clipping_endpoint_incidence_count": sum(
            row["zero_dimensional_boundary_endpoint_incidence_count"]
            for row in leaves
        ),
        "both_t_face_curve_leaf_count": len(both_curve_leaves),
        "both_t_face_curve_axis_mismatch_count": sum(
            row["lower_t_face_status"][1]
            != row["upper_t_face_status"][1]
            for row in both_curve_leaves
        ),
        "pair_row_count": len(pairs),
        "pair_existence_classification_histogram":
            dict(sorted(pair_classes.items())),
        "actual_transverse_1D_pair_intersection_count": sum(
            row["actual_1D_intersection_component_count"] for row in pairs
        ),
        "actual_pair_boundary_0D_corner_incidence_count": len(corners),
        "pair_interval_newton_interior_count": sum(
            row["interval_newton_interior"] is True for row in pairs
        ),
        "source_chart_seam_row_count": len(seams),
        "source_chart_seam_half_open_owner_count": sum(
            row["is_half_open_owner"] for row in seams
        ),
        "source_chart_seam_half_open_excluded_shadow_count": sum(
            not row["is_half_open_owner"] for row in seams
        ),
        "global_source_G_exact_key_disposition_count": 0,
    }
    require(
        result["Round179_partial_original_tube_count"] == 57896
        and result["Round179_retained_3d_child_count"] == 106680
        and result["collar_occurrence_count"] == 54220
        and result[
            "inactive_collar_occurrence_on_Round179_fully_replaced_origin_count"
        ] == 396
        and result["active_collar_occurrence_on_partial_origin_count"] == 53824
        and result["active_outgoing_collar_occurrence_count"] == 30160
        and result["active_wall_collar_occurrence_count"] == 23664
        and result["outgoing_G_target_collar_occurrence_count"] == 13008
        and result["outgoing_W_target_collar_occurrence_count"] == 17436
        and result["wall_G_target_collar_occurrence_count"] == 23776
        and result["pair_row_count"] == 336
        and result["actual_transverse_1D_pair_intersection_count"] == 112
        and result["actual_pair_boundary_0D_corner_incidence_count"] == 224
        and result["pair_interval_newton_interior_count"] == 112
        and result["both_t_face_curve_leaf_count"] == 19716
        and result["both_t_face_curve_axis_mismatch_count"] == 0
        and result["source_chart_seam_half_open_owner_count"] == 236
        and result["source_chart_seam_half_open_excluded_shadow_count"] == 236,
        "Round182 expected taxonomy",
    )
    return result


def pack_attachment(
    rows: dict[str, list[dict[str, Any]]],
) -> dict[str, Any]:
    schemas = {
        "origin_replacement_rows": ORIGIN_COLUMNS,
        "collar_occurrence_rows": COLLAR_COLUMNS,
        "collar_leaf_rows": LEAF_COLUMNS,
        "pair_intersection_rows": PAIR_COLUMNS,
        "pair_boundary_corner_rows": CORNER_COLUMNS,
        "source_chart_seam_owner_rows": SEAM_COLUMNS,
        "carried_normal_form_rows": CARRY_COLUMNS,
    }
    tables = {
        name: [pack(schemas[name], row) for row in rows[name]]
        for name in schemas
    }
    result = {
        "row_column_schemas": schemas,
        **tables,
        "table_census_and_sha256": {
            name: {"row_count": len(table), "rows_sha256": digest(table)}
            for name, table in tables.items()
        },
    }
    return {
        "schema": ATTACHMENT_SCHEMA,
        "result": result,
        "result_sha256": digest(result),
    }


def certificate_result(
    stats: dict[str, Any],
    attachment: dict[str, Any],
    attachment_file_sha256: str,
) -> dict[str, Any]:
    return {
        "status": STATUS,
        "producer": {
            "filename": PRODUCER.name,
            "sha256": hashlib.sha256(
                safe_input(PRODUCER, 300_000)
            ).hexdigest(),
            "independent_verifier_must_treat_as_inert_bytes": True,
        },
        "scope": {
            "pinned_Round179_status": R179_STATUS,
            "pinned_Round179_certificate_result_sha256": R179_CERT_RESULT,
            "pinned_Round179_attachment_result_sha256":
                R179_ATTACHMENT_RESULT,
            "pinned_Round179_verification_result_sha256":
                R179_VERIFY_RESULT,
            "parent_third_full_attachment_replay":
                "BYTE_IDENTICAL_PASS_REPORTED_2026_07_26",
            "bounded_W_outgoing_s_split_depth":
                W_OUTGOING_MAX_S_SPLITS,
            "bounded_G_target_p_split_depth":
                G_TARGET_MAX_P_SPLITS,
            "precision_bits": PRECISION_BITS,
            "python_flint_version": FLINT_VERSION,
        },
        "taxonomy": stats,
        "dimension_safe_ledger": {
            "ambient_3D": {
                "input_kind":
                    "Round179 retained positive-volume children only",
                "input_coordinate_volume":
                    stats["Round179_retained_coordinate_volume"],
                "closed_side_union_coordinate_volume":
                    stats["Round182_closed_retained_coordinate_volume"],
                "residual_collar_coordinate_volume":
                    stats["Round182_residual_retained_coordinate_volume"],
                "exact_conservation": True,
            },
            "regular_2D_graphs": {
                "sheet_cell_count": stats[
                    "two_dimensional_graph_sheet_count"
                ],
                "existence_requires_endpoint_bracket": True,
                "regularity_alone_never_promoted_to_existence": True,
                "no_3D_volume_subtraction": True,
            },
            "clipping_1D_curves": {
                "parametric_curve_segment_count": stats[
                    "one_dimensional_clipping_curve_segment_count"
                ],
                "strict_base_derivative_and_face_bracket": True,
                "two_face_curve_leaf_count":
                    stats["both_t_face_curve_leaf_count"],
                "two_face_curve_axis_mismatch_count":
                    stats["both_t_face_curve_axis_mismatch_count"],
                "two_face_curves_strictly_ordered_by_whole_box_t_derivative":
                    True,
                "two_face_curves_bound_one_clipped_2D_sheet_not_two": True,
                "no_2D_or_3D_credit_migration": True,
            },
            "pair_1D_intersections": {
                "actual_component_count": stats[
                    "actual_transverse_1D_pair_intersection_count"
                ],
                "existence_by_p_face_bracket_and_interval_Newton": True,
                "transversality_by_strict_2x2_Jacobian_minor": True,
                "minor_alone_not_used_for_existence": True,
            },
            "boundary_0D": {
                "pair_corner_incidence_count": stats[
                    "actual_pair_boundary_0D_corner_incidence_count"
                ],
                "clipping_endpoint_incidence_count": stats[
                    "zero_dimensional_clipping_endpoint_incidence_count"
                ],
                "incidences_not_global_component_counts": True,
            },
        },
        "ownership": {
            "source_chart_diagonal":
                "E_OR_W_OWNS__N_OR_S_EXCLUDES",
            "owned_source_seam_rows":
                stats["source_chart_seam_half_open_owner_count"],
            "excluded_shadow_source_seam_rows":
                stats[
                    "source_chart_seam_half_open_excluded_shadow_count"
                ],
            "integer_wall_endpoint":
                "ANALYTIC_BOUNDARY_STRATUM__NO_ADJACENT_TUBE_DEDUP_CREDIT",
        },
        "credit_separation": {
            "original_tube_count":
                stats["Round179_partial_original_tube_count"],
            "predicate_occurrence_count": stats["collar_occurrence_count"],
            "global_source_G_exact_key_fibre_count": SOURCE_G_KEY_COUNT,
            "global_source_G_exact_key_disposition_count": 0,
            "tube_occurrence_and_global_key_counts_not_identified": True,
        },
        "global_state": {
            "source_G_global_geometric_dispositions": f"0/{SOURCE_G_KEY_COUNT}",
            "Gate5_closed_fields": "10/18",
            "complete_global_18_field_blocks": 0,
            "open_fields": [
                "F5", "F6", "F10", "F11", "F14", "F15", "F17", "F18",
            ],
            "D02": "BLOCKED",
            "D03_negative_oracle": "UNAUTHORIZED",
            "CM2": "NO-GO",
            "promotions_issued": 0,
        },
        "remaining_core_gate": {
            "residual_original_tube_count":
                stats["Round182_residual_original_tube_count"],
            "residual_retained_coordinate_volume":
                stats["Round182_residual_retained_coordinate_volume"],
            "required_next":
                "resolve the bounded W-target outgoing face collars left "
                "after six s-splits, then materialize side-specific local "
                "return signatures without identifying them with whole "
                "global exact-key fibres",
        },
        "row_attachment": {
            "filename": ATTACHMENT.name,
            "schema": ATTACHMENT_SCHEMA,
            "result_sha256": attachment["result_sha256"],
            "file_sha256": attachment_file_sha256,
            "table_census_and_sha256":
                attachment["result"]["table_census_and_sha256"],
        },
        "pins": dict(sorted(PINS.items())),
    }


def build_all() -> tuple[dict[str, Any], dict[str, Any], bytes]:
    ctx.prec = PRECISION_BITS
    source = load_round179()
    rows = build_rows(source)
    stats = statistics(rows)
    attachment = pack_attachment(rows)
    attachment_bytes = (
        canonical(attachment) + "\n"
    ).encode()
    attachment_file_sha256 = hashlib.sha256(attachment_bytes).hexdigest()
    result = certificate_result(
        stats, attachment, attachment_file_sha256
    )
    certificate = {
        "schema": SCHEMA,
        "result": result,
        "result_sha256": digest(result),
    }
    return certificate, attachment, attachment_bytes


def output_guard(path: Path, protected: set[Path]) -> Path:
    absolute = Path(os.path.abspath(os.fspath(path)))
    require(absolute.parent.resolve() == HERE, "output parent")
    canonical_path = HERE / absolute.name
    protected_names = {item.name for item in protected}
    require(
        canonical_path.name not in protected_names,
        "output aliases protected input",
    )
    if canonical_path.exists() or canonical_path.is_symlink():
        info = canonical_path.lstat()
        require(
            not stat.S_ISLNK(info.st_mode)
            and stat.S_ISREG(info.st_mode)
            and info.st_nlink == 1,
            f"output path:{canonical_path.name}",
        )
    return canonical_path


def atomic_write(path: Path, data: bytes) -> None:
    descriptor, temporary_name = tempfile.mkstemp(
        dir=HERE,
        prefix=f".{path.name}.",
        suffix=".tmp",
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            descriptor = -1
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        info = temporary.lstat()
        require(
            stat.S_ISREG(info.st_mode)
            and not stat.S_ISLNK(info.st_mode)
            and info.st_nlink == 1,
            "exclusive temporary regular file",
        )
        os.replace(temporary, path)
        directory_fd = os.open(HERE, os.O_RDONLY | os.O_DIRECTORY)
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)
    except BaseException:
        if descriptor >= 0:
            os.close(descriptor)
        if temporary.exists() or temporary.is_symlink():
            temporary.unlink()
        raise


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument("--attachment", type=Path, default=ATTACHMENT)
    parser.add_argument("--expect-certificate-result")
    parser.add_argument("--expect-attachment-result")
    parser.add_argument("--print-only", action="store_true")
    args = parser.parse_args()
    readonly = {
        PRODUCER, VERIFIER, VERIFICATION, REPORT, COLD_REPLAY, MANIFEST,
        *(HERE / name for name in PINS),
    }
    output_path = output_guard(args.output, readonly | {ATTACHMENT})
    attachment_path = output_guard(
        args.attachment, readonly | {OUTPUT}
    )
    require(
        output_path != attachment_path,
        "distinct outputs",
    )
    certificate, attachment, attachment_bytes = build_all()
    if args.expect_certificate_result:
        require(
            certificate["result_sha256"]
            == args.expect_certificate_result,
            "expected certificate result",
        )
    if args.expect_attachment_result:
        require(
            attachment["result_sha256"]
            == args.expect_attachment_result,
            "expected attachment result",
        )
    if args.print_only:
        print(canonical(certificate))
        return 0
    atomic_write(attachment_path, attachment_bytes)
    atomic_write(
        output_path, (canonical(certificate) + "\n").encode()
    )
    print(canonical({
        "certificate": output_path.name,
        "certificate_result_sha256": certificate["result_sha256"],
        "attachment": attachment_path.name,
        "attachment_result_sha256": attachment["result_sha256"],
        "attachment_file_sha256":
            hashlib.sha256(attachment_bytes).hexdigest(),
        "status": STATUS,
    }))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
