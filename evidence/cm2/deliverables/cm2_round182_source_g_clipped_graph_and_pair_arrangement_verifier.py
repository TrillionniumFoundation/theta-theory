#!/usr/bin/env python3
"""Independent verifier for Round182 clipped source-G arrangements.

The Round182 producer is pinned and read only as inert bytes.  It is never
imported or executed.  Starting from the pinned Round179 attachment, this
verifier independently reconstructs every Round182 table, the complete
attachment bytes, all statistics, and the complete expected certificate.
"""

from __future__ import annotations

import argparse
import copy
import gc
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


BASE = Path(__file__).resolve().parent
PRODUCER = BASE / (
    "cm2_round182_source_g_clipped_graph_and_pair_arrangement.py"
)
CERTIFICATE = BASE / (
    "cm2_round182_source_g_clipped_graph_and_pair_arrangement_certificate.json"
)
ATTACHMENT = BASE / (
    "cm2_round182_source_g_clipped_graph_and_pair_arrangement_rows.json"
)
OUTPUT = BASE / (
    "cm2_round182_source_g_clipped_graph_and_pair_arrangement_verification.json"
)
SCHEMA = "cm2.round182.source-g-clipped-graph-and-pair-arrangement.v1"
ATTACHMENT_SCHEMA = (
    "cm2.round182.source-g-clipped-graph-and-pair-arrangement-rows.v1"
)
VERIFICATION_SCHEMA = (
    "cm2.round182.source-g-clipped-graph-and-pair-arrangement.verification.v1"
)
STATUS = (
    "CERTIFIED_BOUNDED_PARTIAL_SOURCE_G_CLIPPED_GRAPH_AND_PAIR_ARRANGEMENT__"
    "NO_GLOBAL_EXACT_KEY_DISPOSITION_OR_D02_PROMOTION"
)
PRECISION_BITS = 256
W_SPLITS = 6
G_SPLITS = 6
SOURCE_G_KEYS = 224580
EXPECTED_PRODUCER_SHA256 = (
    "8638f2722e68bd5c6e0eb5932dc76780728998f21a47b1d8c02c28449e984d56"
)
EXPECTED_CERTIFICATE_SHA256 = (
    "27491e3943e88772ec15cee110cd983b14ad82a2a56f8a07d605c3cd8fb49f08"
)
EXPECTED_ATTACHMENT_SHA256 = (
    "ae6e0c38df325e98b01a1d75acfbd8a85a71fda6a118db11d7dff6decf3f847c"
)
EXPECTED_CERTIFICATE_RESULT = (
    "e07da794eed6dbb404de8913f5b871621f9f1b59b355172a37192791ae28911d"
)
EXPECTED_ATTACHMENT_RESULT = (
    "9f0f64d93bd0ac2a9dd41965cbfd95531f07582da5eb4c52f14c44da3d0db269"
)

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


def input_bytes(path: Path, maximum: int) -> bytes:
    absolute = Path(os.path.abspath(os.fspath(path)))
    require(absolute.parent.resolve() == BASE, f"path parent:{path.name}")
    canonical_path = BASE / absolute.name
    require(
        canonical_path.exists() or canonical_path.is_symlink(),
        f"path exists:{path.name}",
    )
    info = canonical_path.lstat()
    require(
        not stat.S_ISLNK(info.st_mode)
        and stat.S_ISREG(info.st_mode)
        and info.st_nlink == 1
        and 0 < info.st_size <= maximum,
        f"path type/size:{path.name}",
    )
    return canonical_path.read_bytes()


def strict_decode(raw: bytes, maximum: int = 400_000_000) -> dict[str, Any]:
    require(
        raw and len(raw) <= maximum
        and not raw.startswith(b"\xef\xbb\xbf")
        and b"\x00" not in raw,
        "strict JSON bytes",
    )

    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result = {}
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
                "decoded string",
            )
        elif type(item) is list:
            for child in item:
                walk(child)
        elif type(item) is dict:
            for key, child in item.items():
                walk(key)
                walk(child)

    walk(value)
    require(type(value) is dict, "top object")
    return value


def strict_load(path: Path, maximum: int) -> dict[str, Any]:
    return strict_decode(input_bytes(path, maximum), maximum)


def unpack(table: list[list[Any]], columns: list[str]) -> list[dict[str, Any]]:
    return [dict(zip(columns, row, strict=True)) for row in table]


def pack(columns: list[str], row: dict[str, Any]) -> list[Any]:
    require(set(row) == set(columns), f"packed keys:{columns[0]}")
    return [row[column] for column in columns]


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
    "source_graph_exact_factorization", "second_graph_equation",
    "source_graph_t_boundary_face", "existence_classification",
    "p_lower_sign", "p_upper_sign", "p_lower_value_interval",
    "p_upper_value_interval", "strict_p_derivative_sign",
    "strict_p_derivative_interval", "strict_source_t_derivative_sign",
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
SCHEMAS = {
    "origin_replacement_rows": ORIGIN_COLUMNS,
    "collar_occurrence_rows": COLLAR_COLUMNS,
    "collar_leaf_rows": LEAF_COLUMNS,
    "pair_intersection_rows": PAIR_COLUMNS,
    "pair_boundary_corner_rows": CORNER_COLUMNS,
    "source_chart_seam_owner_rows": SEAM_COLUMNS,
    "carried_normal_form_rows": CARRY_COLUMNS,
}


def load_source_and_documents():
    require(FLINT_VERSION == "0.9.0", "python-flint version")
    producer_raw = input_bytes(PRODUCER, 300_000)
    require(
        hashlib.sha256(producer_raw).hexdigest()
        == EXPECTED_PRODUCER_SHA256,
        "inert producer pin",
    )
    del producer_raw
    for name, expected in PINS.items():
        require(
            hashlib.sha256(input_bytes(BASE / name, 180_000_000)).hexdigest()
            == expected,
            f"pin:{name}",
        )
    source = strict_load(BASE / R179A, 180_000_000)
    r179c = strict_load(BASE / R179C, 2_000_000)
    r179o = strict_load(BASE / R179O, 2_000_000)
    require(
        source["schema"] == r179.ATTACHMENT_SCHEMA
        and source["result_sha256"]
        == R179_ATTACHMENT_RESULT
        == digest(source["result"])
        and r179c["result_sha256"]
        == R179_CERT_RESULT
        == digest(r179c["result"])
        and r179c["result"]["status"] == R179_STATUS
        and r179o["result_sha256"]
        == R179_VERIFY_RESULT
        == digest(r179o["result"])
        and r179o["result"]["status"] == "PASS"
        and r179o["result"]["full_attachment_byte_for_byte_matched"] is True
        and r179o["result"]["producer_imported_or_executed"] is False,
        "Round179 source bindings",
    )
    certificate_raw = input_bytes(CERTIFICATE, 3_000_000)
    attachment_raw = input_bytes(ATTACHMENT, 400_000_000)
    require(
        hashlib.sha256(certificate_raw).hexdigest()
        == EXPECTED_CERTIFICATE_SHA256
        and hashlib.sha256(attachment_raw).hexdigest()
        == EXPECTED_ATTACHMENT_SHA256,
        "Round182 frozen file pins",
    )
    return (
        source["result"],
        strict_decode(certificate_raw, 3_000_000),
        strict_decode(attachment_raw, 400_000_000),
        certificate_raw,
        attachment_raw,
    )


def qarb(value: Q) -> arb:
    return arb(value.numerator) / value.denominator


def v_box(row: dict[str, Any]) -> Any:
    return r179.box_from(
        row["box"], len(row["refinement_path"]), row["row_id"]
    )


def v_value(origin, kind, meta, box):
    geometry = r179.independent_geometry(
        origin["chart"], origin["owner_target"], box
    )
    if kind == "OUTGOING":
        return geometry["outgoing_equality"]
    name = "hit_x" if meta["axis"] == "X" else "hit_y"
    return r179.subtract_wall(geometry[name], meta["integer_wall"])


def v_double_face(box, t_upper, axis, upper):
    return r179.face_box(r179.face_box(box, "t", t_upper), axis, upper)


def v_newton(function, box, axis):
    index = "tps".index(axis)
    lower = getattr(box, axis + "0")
    upper = getattr(box, axis + "1")
    midpoint = (lower + upper) / 2
    if axis == "p":
        middle = r179.r174.atlas.AtlasBox(
            box.t0, box.t1, midpoint, midpoint,
            box.s0, box.s1, box.depth, box.path,
        )
    elif axis == "s":
        middle = r179.r174.atlas.AtlasBox(
            box.t0, box.t1, box.p0, box.p1,
            midpoint, midpoint, box.depth, box.path,
        )
    else:
        middle = r179.r174.atlas.AtlasBox(
            midpoint, midpoint, box.p0, box.p1,
            box.s0, box.s1, box.depth, box.path,
        )
    derivative = function(box)[1][index]
    require(
        derivative is not None
        and r179.arb_sign(derivative) != "OVERWRAP",
        "shadow Newton derivative",
    )
    domain = r179.r174.first_hit.arb_interval(lower, upper)
    image = qarb(midpoint) - function(middle)[0] / derivative
    return domain.contains_interior(image), image.str(40)


def v_face_status(origin, kind, meta, box, t_upper):
    face = r179.face_box(box, "t", t_upper)
    function = lambda child: v_value(origin, kind, meta, child)
    value = function(face)
    value_sign = r179.arb_sign(value[0])
    if value_sign != "OVERWRAP":
        return {
            "kind": "STRICT", "resolved_sign": value_sign,
            "axis": None, "derivative_sign": None,
            "axis_lower_sign": None, "axis_upper_sign": None,
            "newton_interior": None, "newton_image": None,
        }
    curves = []
    absences = []
    for axis in ("p", "s"):
        index = "tps".index(axis)
        derivative = value[1][index]
        if (
            derivative is None
            or r179.arb_sign(derivative) == "OVERWRAP"
        ):
            continue
        lower = function(v_double_face(box, t_upper, axis, False))[0]
        upper = function(v_double_face(box, t_upper, axis, True))[0]
        classification = r179.face_kind(lower, upper)
        if classification not in (
            "FULL_BASE_UNIQUE_GRAPH", "STRICT_ZERO_ABSENT"
        ):
            continue
        record = {
            "kind": (
                "CURVE" if classification == "FULL_BASE_UNIQUE_GRAPH"
                else "ABSENT"
            ),
            "resolved_sign": (
                None if classification == "FULL_BASE_UNIQUE_GRAPH"
                else r179.arb_sign(lower)
            ),
            "axis": axis,
            "derivative_sign": r179.arb_sign(derivative),
            "axis_lower_sign": r179.arb_sign(lower),
            "axis_upper_sign": r179.arb_sign(upper),
            "newton_interior": None,
            "newton_image": None,
        }
        if classification == "FULL_BASE_UNIQUE_GRAPH":
            record["newton_interior"], record["newton_image"] = v_newton(
                function, face, axis
            )
            curves.append(record)
        else:
            absences.append(record)
    require(not (curves and absences), "shadow conflicting normal forms")
    if curves:
        return curves[0]
    if absences:
        return absences[0]
    return {
        "kind": "UNRESOLVED", "resolved_sign": None,
        "axis": None, "derivative_sign": None,
        "axis_lower_sign": None, "axis_upper_sign": None,
        "newton_interior": None, "newton_image": None,
    }


def v_encode(status):
    signs = {
        "STRICT_POSITIVE": "+", "STRICT_NEGATIVE": "-", None: "_",
    }
    if status["kind"] == "STRICT":
        return "S" + signs[status["resolved_sign"]]
    if status["kind"] == "UNRESOLVED":
        return "U"
    return "".join([
        "C" if status["kind"] == "CURVE" else "A",
        status["axis"], signs[status["derivative_sign"]],
        signs[status["axis_lower_sign"]],
        signs[status["axis_upper_sign"]],
        signs[status["resolved_sign"]],
        (
            "1" if status["newton_interior"] is True
            else "0" if status["newton_interior"] is False
            else "_"
        ),
    ])


def v_leaf(occurrence_id, retained, path, box, lower, upper):
    unresolved = (
        lower["kind"] == "UNRESOLVED"
        or upper["kind"] == "UNRESOLVED"
    )
    curves = sum(status["kind"] == "CURVE" for status in (lower, upper))
    if unresolved:
        classification = "RESIDUAL_3D"
        sheets = 0
    elif curves:
        classification = "CLIPPED_2D_BOUNDARY_1D"
        sheets = 1
    else:
        signs = [lower["resolved_sign"], upper["resolved_sign"]]
        require(all(sign is not None for sign in signs), "shadow face signs")
        if signs[0] != signs[1]:
            classification = "FULL_2D"
            sheets = 1
        else:
            classification = "EMPTY"
            sheets = 0
    volume = r179.r174.volume(box)
    area = (box.p1 - box.p0) * (box.s1 - box.s0)
    payload = [
        occurrence_id, retained["row_id"], path,
        r179.r174.box_values(box), classification,
        v_encode(lower), v_encode(upper),
    ]
    return {
        "row_id": make_id("collar-leaf", payload),
        "occurrence_row_id": occurrence_id,
        "retained_child_row_id": retained["row_id"],
        "base_refinement_path": path,
        "box": r179.r174.box_values(box),
        "coordinate_volume": qstr(volume),
        "base_coordinate_area": qstr(area),
        "lower_t_face_status": v_encode(lower),
        "upper_t_face_status": v_encode(upper),
        "graph_classification": classification,
        "two_dimensional_graph_sheet_count": sheets,
        "one_dimensional_clipping_curve_segment_count": curves,
        "zero_dimensional_boundary_endpoint_incidence_count": 2 * curves,
        "closed_3d_side_union_volume":
            qstr(Q(0) if unresolved else volume),
        "residual_3d_collar_volume":
            qstr(volume if unresolved else Q(0)),
    }


def v_retained_leaves(origin, retained, kind, meta):
    initial = v_box(retained)
    w_target = (
        kind == "OUTGOING"
        and origin["owner_target"].startswith("W[")
    )
    maximum = W_SPLITS if w_target else G_SPLITS
    axis = 2 if w_target else 1
    axis_name = "s" if w_target else "p"
    queue = [(initial, 0, [])]
    leaves = []
    while queue:
        box, depth, path = queue.pop()
        lower = v_face_status(origin, kind, meta, box, False)
        upper = v_face_status(origin, kind, meta, box, True)
        unresolved = (
            lower["kind"] == "UNRESOLVED"
            or upper["kind"] == "UNRESOLVED"
        )
        if unresolved and depth < maximum:
            children = r179.r174.bisect(box, axis)
            queue.append((
                children[1], depth + 1, [*path, axis_name + "1"]
            ))
            queue.append((
                children[0], depth + 1, [*path, axis_name + "0"]
            ))
        else:
            leaves.append(v_leaf(
                meta["row_id"], retained, path, box, lower, upper
            ))
    leaves.sort(key=lambda row: row["row_id"])
    require(
        sum((Q(row["coordinate_volume"]) for row in leaves), Q(0))
        == Q(retained["coordinate_volume"]),
        "shadow retained volume",
    )
    return leaves


def v_collar(origin, retained_rows, kind, meta):
    original_box = r179.box_from(
        origin["original_box"],
        len(origin["original_refinement_path"]),
        origin["origin_row_id"],
    )
    derivative_sign = r179.arb_sign(
        v_value(origin, kind, meta, original_box)[1][0]
    )
    require(derivative_sign != "OVERWRAP", "shadow strict t derivative")
    leaves = []
    for retained in retained_rows:
        leaves.extend(v_retained_leaves(origin, retained, kind, meta))
    leaves.sort(key=lambda row: row["row_id"])
    closed = sum(
        (Q(row["closed_3d_side_union_volume"]) for row in leaves), Q(0)
    )
    residual = sum(
        (Q(row["residual_3d_collar_volume"]) for row in leaves), Q(0)
    )
    input_volume = sum(
        (Q(row["coordinate_volume"]) for row in retained_rows), Q(0)
    )
    require(closed + residual == input_volume, "shadow collar volume")
    packed_leaves = [pack(LEAF_COLUMNS, row) for row in leaves]
    reason = (
        "outgoing_chart_seam"
        if kind == "OUTGOING" else meta["reason_label"]
    )
    equation = meta["equation"] if kind == "OUTGOING" else meta["zero_equation"]
    row = {
        "row_id": make_id(
            "collar", [meta["row_id"], origin["origin_row_id"], kind]
        ),
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
        "bounded_base_split_axis": (
            "s" if origin["owner_target"].startswith("W[") else "p"
        ),
        "bounded_base_split_depth": (
            W_SPLITS if origin["owner_target"].startswith("W[") else G_SPLITS
        ),
        "closed_leaf_count": sum(
            Q(leaf["closed_3d_side_union_volume"]) > 0 for leaf in leaves
        ),
        "closed_coordinate_volume": qstr(closed),
        "residual_leaf_count": sum(
            Q(leaf["residual_3d_collar_volume"]) > 0 for leaf in leaves
        ),
        "residual_coordinate_volume": qstr(residual),
        "full_base_graph_leaf_count": sum(
            leaf["graph_classification"] == "FULL_2D" for leaf in leaves
        ),
        "absent_graph_leaf_count": sum(
            leaf["graph_classification"] == "EMPTY" for leaf in leaves
        ),
        "clipped_graph_leaf_count": sum(
            leaf["graph_classification"] == "CLIPPED_2D_BOUNDARY_1D"
            for leaf in leaves
        ),
        "two_dimensional_graph_sheet_count": sum(
            leaf["two_dimensional_graph_sheet_count"] for leaf in leaves
        ),
        "one_dimensional_clipping_curve_segment_count": sum(
            leaf["one_dimensional_clipping_curve_segment_count"]
            for leaf in leaves
        ),
        "zero_dimensional_boundary_endpoint_incidence_count": sum(
            leaf["zero_dimensional_boundary_endpoint_incidence_count"]
            for leaf in leaves
        ),
        "fully_clipped_over_Round179_retained_children": residual == 0,
        "leaf_rows_sha256": digest(packed_leaves),
        "whole_original_tube_credit": 0,
        "global_exact_key_disposition_credit": 0,
        "provenance":
            "ROUND182_RETAINED_CHILD_GRAPH_COLLAR_DIMENSIONAL_LEDGER",
    }
    return row, leaves


def v_inactive_collar(origin, kind, meta):
    box = r179.box_from(
        origin["original_box"],
        len(origin["original_refinement_path"]),
        origin["origin_row_id"],
    )
    derivative_sign = r179.arb_sign(
        v_value(origin, kind, meta, box)[1][0]
    )
    require(derivative_sign != "OVERWRAP", "inactive strict derivative")
    reason = (
        "outgoing_chart_seam"
        if kind == "OUTGOING" else meta["reason_label"]
    )
    equation = meta["equation"] if kind == "OUTGOING" else meta["zero_equation"]
    return {
        "row_id": make_id(
            "collar", [meta["row_id"], origin["origin_row_id"], kind, "inactive"]
        ),
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


def v_zero_t(box):
    return r179.r174.atlas.AtlasBox(
        Q(0), Q(0), box.p0, box.p1, box.s0, box.s1,
        box.depth, box.path,
    )


def v_pair(pair, origin, retained_rows, wall_rows, outgoing):
    box = r179.box_from(
        origin["original_box"],
        len(origin["original_refinement_path"]),
        origin["origin_row_id"],
    )
    require(
        (box.t0 == 0) != (box.t1 == 0)
        and origin["owner_target"].startswith("G["),
        "shadow pair boundary/G target",
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
    require(len(containing) == 1, "shadow unique t-face child")
    empty_wall = next((
        row for row in wall_rows
        if row["source_factor_classification"] == "STRICT_NONZERO"
        and row["target_factor_classification"] == "STRICT_NONZERO"
    ), None)
    source_wall = next(
        row for row in wall_rows
        if row["source_factor_classification"] == "REGULAR_GRAPH"
    )
    cell = origin["chart"].split(":")[1]
    expected_axis = "Y" if cell in {"E", "W"} else "X"
    require(
        source_wall["axis"] == expected_axis
        and source_wall["integer_wall"] == 0,
        "shadow exact source axis",
    )
    source_name = "source_x" if expected_axis == "X" else "source_y"
    source_factorization = f"{source_name}=(9/25)*t"
    source_function = lambda child: r179.subtract_wall(
        r179.independent_geometry(
            origin["chart"], origin["owner_target"], child
        )[source_name],
        0,
    )
    source_dual = source_function(v_zero_t(box))
    source_dt = qarb(Q(9, 25))
    require(
        r179.arb_sign(source_dual[0]) == "OVERWRAP"
        and source_dual[1][0].contains(source_dt),
        "shadow exact source factor",
    )
    lower_sign = upper_sign = p_sign = jacobian_sign = None
    lower_interval = upper_interval = p_interval = jacobian_interval = None
    empty_source_interval = empty_target_interval = None
    newton_inside = newton_image = None
    second_equation = "EMPTY_FIRST_PREDICATE"
    corners = []
    if empty_wall is not None:
        geometry = r179.independent_geometry(
            origin["chart"], origin["owner_target"], box
        )
        source = r179.subtract_wall(
            geometry[
                "source_x" if empty_wall["axis"] == "X" else "source_y"
            ],
            empty_wall["integer_wall"],
        )[0]
        target = r179.subtract_wall(
            geometry["hit_x" if empty_wall["axis"] == "X" else "hit_y"],
            empty_wall["integer_wall"],
        )[0]
        require(
            r179.arb_sign(source) != "OVERWRAP"
            and r179.arb_sign(target) != "OVERWRAP",
            "shadow empty predicate margins",
        )
        empty_source_interval = source.str(40)
        empty_target_interval = target.str(40)
        existence = "EMPTY__ONE_PREDICATE_HAS_EMPTY_ZERO_SET"
        dimension = "EMPTY"
        components = 0
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
            target_name = (
                "hit_x" if target_wall["axis"] == "X" else "hit_y"
            )
            second_equation = (
                f"target_{target_wall['axis'].lower()}-"
                f"{target_wall['integer_wall']}=0"
            )
            second_function = lambda child: r179.subtract_wall(
                r179.independent_geometry(
                    origin["chart"], origin["owner_target"], child
                )[target_name],
                target_wall["integer_wall"],
            )
        zero_box = v_zero_t(box)
        dual = second_function(zero_box)
        p_sign = r179.arb_sign(dual[1][1])
        require(p_sign != "OVERWRAP", "shadow strict p derivative")
        lower = second_function(r179.face_box(zero_box, "p", False))[0]
        upper = second_function(r179.face_box(zero_box, "p", True))[0]
        lower_sign = r179.arb_sign(lower)
        upper_sign = r179.arb_sign(upper)
        lower_interval = lower.str(40)
        upper_interval = upper.str(40)
        p_interval = dual[1][1].str(40)
        jacobian = source_dt * dual[1][1]
        jacobian_sign = r179.arb_sign(jacobian)
        jacobian_interval = jacobian.str(40)
        require(jacobian_sign != "OVERWRAP", "shadow Jacobian")
        classification = r179.face_kind(lower, upper)
        if classification == "FULL_BASE_UNIQUE_GRAPH":
            newton_inside, newton_image = v_newton(
                second_function, zero_box, "p"
            )
            require(newton_inside, "shadow pair Newton")
            existence = (
                "UNIQUE_TRANSVERSE_1D_INTERSECTION_LINE__"
                "P_BRACKET_AND_INTERVAL_NEWTON"
            )
            dimension = "EXACT_DIMENSION_1"
            components = 1
            for face, coordinate in (
                ("LOWER_S_FACE", box.s0),
                ("UPPER_S_FACE", box.s1),
            ):
                payload = [pair["row_id"], face, qstr(coordinate), newton_image]
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
                "shadow pair face classification",
            )
            existence = "EMPTY__STRICT_SAME_SIGN_P_FACES"
            dimension = "EMPTY"
            components = 0
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
        "source_graph_exact_factorization": source_factorization,
        "second_graph_equation": second_equation,
        "source_graph_t_boundary_face": t_face,
        "existence_classification": existence,
        "p_lower_sign": lower_sign,
        "p_upper_sign": upper_sign,
        "p_lower_value_interval": lower_interval,
        "p_upper_value_interval": upper_interval,
        "strict_p_derivative_sign": p_sign,
        "strict_p_derivative_interval": p_interval,
        "strict_source_t_derivative_sign": "STRICT_POSITIVE",
        "strict_source_t_derivative_interval": source_dt.str(40),
        "strict_2x2_Jacobian_minor_sign": jacobian_sign,
        "strict_2x2_Jacobian_minor_interval": jacobian_interval,
        "first_empty_source_factor_interval": empty_source_interval,
        "first_empty_target_factor_interval": empty_target_interval,
        "interval_newton_domain": [qstr(box.p0), qstr(box.p1)],
        "interval_newton_interior": newton_inside,
        "interval_newton_image": newton_image,
        "actual_intersection_dimension": dimension,
        "actual_1D_intersection_component_count": components,
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


def independently_rebuild_attachment(source):
    schemas = source["row_column_schemas"]
    all_origins = unpack(source["origin_tube_rows"], schemas["origin_tube_rows"])
    all_origin_by_id = {row["origin_row_id"]: row for row in all_origins}
    origins = {
        row["origin_row_id"]: row
        for row in all_origins
        if not row["fully_replaced_by_bounded_children"]
    }
    require(len(origins) == 57896, "shadow partial origin census")
    retained_by_origin = defaultdict(list)
    for row in unpack(
        source["retained_3d_child_rows"],
        schemas["retained_3d_child_rows"],
    ):
        if row["origin_row_id"] in origins:
            retained_by_origin[row["origin_row_id"]].append(row)
    for values in retained_by_origin.values():
        values.sort(key=lambda row: row["row_id"])
    require(
        len(retained_by_origin) == 57896
        and sum(map(len, retained_by_origin.values())) == 106680,
        "shadow retained census",
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
        row["origin_row_id"]: row for row in outgoing_all
        if row["origin_row_id"] in origins
    }
    walls_by_origin = defaultdict(list)
    for row in walls_all:
        if row["origin_row_id"] in origins:
            walls_by_origin[row["origin_row_id"]].append(row)
    seams_by_origin = {
        row["origin_row_id"]: row for row in seams_all
        if row["origin_row_id"] in origins
    }
    pairs_by_origin = {
        row["origin_row_id"]: row for row in pairs_all
        if row["origin_row_id"] in origins
    }
    tasks = {}
    for row in outgoing_all:
        if row["face_classification"] == (
            "FACE_OVERWRAP_REGULAR_ZERO_SET_IF_PRESENT"
        ):
            require(row["origin_row_id"] not in tasks, "shadow one collar")
            tasks[row["origin_row_id"]] = ("OUTGOING", row)
    for row in walls_all:
        if row["target_face_classification"] == (
            "FACE_OVERWRAP_REGULAR_ZERO_SET_IF_PRESENT"
        ):
            require(row["origin_row_id"] not in tasks, "shadow one collar")
            tasks[row["origin_row_id"]] = ("WALL", row)
    require(len(tasks) == 54220, "shadow collar occurrence census")
    collars = []
    leaves = []
    collar_by_origin = {}
    for index, origin_id in enumerate(sorted(tasks)):
        origin = all_origin_by_id[origin_id]
        kind, meta = tasks[origin_id]
        if origin_id in origins:
            collar, child_leaves = v_collar(
                origin, retained_by_origin[origin_id], kind, meta
            )
            collar_by_origin[origin_id] = collar
        else:
            require(
                origin["fully_replaced_by_bounded_children"] is True,
                "shadow inactive origin",
            )
            collar = v_inactive_collar(origin, kind, meta)
            child_leaves = []
        collars.append(collar)
        leaves.extend(child_leaves)
        if index and index % 4000 == 0:
            print(
                f"Round182 verifier collars {index}/{len(tasks)}",
                flush=True,
            )
    pair_rows = []
    corner_rows = []
    for origin_id in sorted(pairs_by_origin):
        row, corners = v_pair(
            pairs_by_origin[origin_id], origins[origin_id],
            retained_by_origin[origin_id], walls_by_origin[origin_id],
            outgoing_by_origin.get(origin_id),
        )
        pair_rows.append(row)
        corner_rows.extend(corners)
    seam_rows = []
    for origin_id in sorted(seams_by_origin):
        upstream = seams_by_origin[origin_id]
        origin = origins[origin_id]
        retained = retained_by_origin[origin_id]
        volume = sum(
            (Q(row["coordinate_volume"]) for row in retained), Q(0)
        )
        owned = (
            upstream["half_open_owner_status"]
            == "E_OR_W_HALF_OPEN_OWNER"
        )
        seam_rows.append({
            "row_id": make_id(
                "source-seam-owner", [upstream["row_id"], origin_id, owned]
            ),
            "Round179_seam_row_id": upstream["row_id"],
            "origin_row_id": origin_id,
            "parent_id": origin["parent_id"],
            "chart": origin["chart"],
            "equation": upstream["equation"],
            "strict_t_derivative_sign": upstream["gradient_sign"],
            "lower_t_face_sign": upstream["lower_t_face_sign"],
            "upper_t_face_sign": upstream["upper_t_face_sign"],
            "exact_dimension": 2,
            "half_open_owner_status": upstream["half_open_owner_status"],
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
            carry_rows.append({
                "row_id": make_id(
                    "carried-form", ["outgoing", row["row_id"]]
                ),
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
            carry_rows.append({
                "row_id": make_id("carried-form", ["wall", row["row_id"]]),
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
                "provenance":
                    "ROUND182_PINNED_ROUND179_FACTORIZATION",
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
            closed = retained_volume
            residual = Q(0)
        else:
            closed = Q(collar["closed_coordinate_volume"])
            residual = Q(collar["residual_coordinate_volume"])
        require(
            Q(origin["resolved_child_coordinate_volume"])
            + Q(origin["guard_child_coordinate_volume"])
            + retained_volume
            == Q(origin["original_coordinate_volume"])
            and closed + residual == retained_volume,
            "shadow origin volume",
        )
        origin_rows.append({
            "row_id": make_id(
                "origin-replacement",
                [origin_id, qstr(closed), qstr(residual)],
            ),
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
            "closed_Round182_retained_coordinate_volume": qstr(closed),
            "residual_Round182_retained_coordinate_volume": qstr(residual),
            "fully_geometrically_replaced_original_tube": residual == 0,
            "released_local_exact_key_count_carried_from_Round179":
                origin["released_exact_key_count"],
            "Round182_released_global_exact_key_count": 0,
            "global_exact_key_disposition_credit": 0,
            "provenance":
                "ROUND179_RELEASED_CHILDREN_PLUS_ROUND182_DIMENSIONAL_COMPLEX",
        })
    tables = {
        "origin_replacement_rows": origin_rows,
        "collar_occurrence_rows": collars,
        "collar_leaf_rows": leaves,
        "pair_intersection_rows": pair_rows,
        "pair_boundary_corner_rows": corner_rows,
        "source_chart_seam_owner_rows": seam_rows,
        "carried_normal_form_rows": carry_rows,
    }
    for table in tables.values():
        table.sort(key=lambda row: row["row_id"])
        require(
            len(table) == len({row["row_id"] for row in table}),
            "shadow row IDs",
        )
    require(
        len(origin_rows) == 57896 and len(collars) == 54220
        and len(pair_rows) == 336 and len(corner_rows) == 224
        and len(seam_rows) == 472,
        "shadow principal census",
    )
    packed = {
        name: [pack(SCHEMAS[name], row) for row in tables[name]]
        for name in SCHEMAS
    }
    result = {
        "row_column_schemas": SCHEMAS,
        **packed,
        "table_census_and_sha256": {
            name: {"row_count": len(table), "rows_sha256": digest(table)}
            for name, table in packed.items()
        },
    }
    return {
        "schema": ATTACHMENT_SCHEMA,
        "result": result,
        "result_sha256": digest(result),
    }, tables


def independent_statistics(tables):
    origins = tables["origin_replacement_rows"]
    collars = tables["collar_occurrence_rows"]
    leaves = tables["collar_leaf_rows"]
    pairs = tables["pair_intersection_rows"]
    corners = tables["pair_boundary_corner_rows"]
    seams = tables["source_chart_seam_owner_rows"]
    retained = sum(
        (Q(row["Round179_retained_coordinate_volume"]) for row in origins),
        Q(0),
    )
    closed = sum(
        (
            Q(row["closed_Round182_retained_coordinate_volume"])
            for row in origins
        ),
        Q(0),
    )
    residual = sum(
        (
            Q(row["residual_Round182_retained_coordinate_volume"])
            for row in origins
        ),
        Q(0),
    )
    require(
        retained == Q("1768407/524288000")
        and closed + residual == retained,
        "shadow global volume",
    )
    kind_target = Counter(
        (row["kind"], row["target_obstacle"]) for row in collars
    )
    graph_classes = Counter(row["graph_classification"] for row in leaves)
    pair_classes = Counter(row["existence_classification"] for row in pairs)
    both_curves = [
        row for row in leaves
        if row["lower_t_face_status"].startswith("C")
        and row["upper_t_face_status"].startswith("C")
    ]
    result = {
        "Round179_partial_original_tube_count": len(origins),
        "Round179_retained_3d_child_count": sum(
            row["Round179_retained_child_count"] for row in origins
        ),
        "Round179_retained_coordinate_volume": qstr(retained),
        "Round182_fully_geometrically_replaced_original_tube_count": sum(
            row["fully_geometrically_replaced_original_tube"]
            for row in origins
        ),
        "Round182_residual_original_tube_count": sum(
            not row["fully_geometrically_replaced_original_tube"]
            for row in origins
        ),
        "Round182_closed_retained_coordinate_volume": qstr(closed),
        "Round182_residual_retained_coordinate_volume": qstr(residual),
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
        "both_t_face_curve_leaf_count": len(both_curves),
        "both_t_face_curve_axis_mismatch_count": sum(
            row["lower_t_face_status"][1]
            != row["upper_t_face_status"][1]
            for row in both_curves
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
        and result["actual_transverse_1D_pair_intersection_count"] == 112
        and result["actual_pair_boundary_0D_corner_incidence_count"] == 224
        and result["pair_interval_newton_interior_count"] == 112
        and result["both_t_face_curve_leaf_count"] == 19716
        and result["both_t_face_curve_axis_mismatch_count"] == 0
        and result["source_chart_seam_half_open_owner_count"] == 236
        and result["source_chart_seam_half_open_excluded_shadow_count"] == 236,
        "shadow expected taxonomy",
    )
    return result


def independently_expected_certificate(stats, attachment, attachment_file_hash):
    result = {
        "status": STATUS,
        "producer": {
            "filename": PRODUCER.name,
            "sha256": EXPECTED_PRODUCER_SHA256,
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
            "bounded_W_outgoing_s_split_depth": W_SPLITS,
            "bounded_G_target_p_split_depth": G_SPLITS,
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
                "sheet_cell_count":
                    stats["two_dimensional_graph_sheet_count"],
                "existence_requires_endpoint_bracket": True,
                "regularity_alone_never_promoted_to_existence": True,
                "no_3D_volume_subtraction": True,
            },
            "clipping_1D_curves": {
                "parametric_curve_segment_count":
                    stats["one_dimensional_clipping_curve_segment_count"],
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
                "actual_component_count":
                    stats["actual_transverse_1D_pair_intersection_count"],
                "existence_by_p_face_bracket_and_interval_Newton": True,
                "transversality_by_strict_2x2_Jacobian_minor": True,
                "minor_alone_not_used_for_existence": True,
            },
            "boundary_0D": {
                "pair_corner_incidence_count":
                    stats["actual_pair_boundary_0D_corner_incidence_count"],
                "clipping_endpoint_incidence_count":
                    stats[
                        "zero_dimensional_clipping_endpoint_incidence_count"
                    ],
                "incidences_not_global_component_counts": True,
            },
        },
        "ownership": {
            "source_chart_diagonal": "E_OR_W_OWNS__N_OR_S_EXCLUDES",
            "owned_source_seam_rows":
                stats["source_chart_seam_half_open_owner_count"],
            "excluded_shadow_source_seam_rows":
                stats["source_chart_seam_half_open_excluded_shadow_count"],
            "integer_wall_endpoint":
                "ANALYTIC_BOUNDARY_STRATUM__NO_ADJACENT_TUBE_DEDUP_CREDIT",
        },
        "credit_separation": {
            "original_tube_count":
                stats["Round179_partial_original_tube_count"],
            "predicate_occurrence_count": stats["collar_occurrence_count"],
            "global_source_G_exact_key_fibre_count": SOURCE_G_KEYS,
            "global_source_G_exact_key_disposition_count": 0,
            "tube_occurrence_and_global_key_counts_not_identified": True,
        },
        "global_state": {
            "source_G_global_geometric_dispositions":
                f"0/{SOURCE_G_KEYS}",
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
            "file_sha256": attachment_file_hash,
            "table_census_and_sha256":
                attachment["result"]["table_census_and_sha256"],
        },
        "pins": dict(sorted(PINS.items())),
    }
    return {
        "schema": SCHEMA,
        "result": result,
        "result_sha256": digest(result),
    }


def validate_documents(certificate, attachment, expected_certificate, expected_attachment):
    require(
        set(attachment) == {"schema", "result", "result_sha256"}
        and attachment["schema"] == ATTACHMENT_SCHEMA
        and attachment["result_sha256"] == digest(attachment["result"]),
        "attachment self digest",
    )
    result = attachment["result"]
    require(
        set(result) == {
            "row_column_schemas", "table_census_and_sha256", *SCHEMAS
        }
        and result["row_column_schemas"] == SCHEMAS,
        "attachment exact top/schema",
    )
    for name, columns in SCHEMAS.items():
        table = result[name]
        require(
            all(type(row) is list and len(row) == len(columns) for row in table)
            and result["table_census_and_sha256"][name]
            == {"row_count": len(table), "rows_sha256": digest(table)},
            f"attachment table:{name}",
        )
    require(
        set(certificate) == {"schema", "result", "result_sha256"}
        and certificate["schema"] == SCHEMA
        and certificate["result_sha256"] == digest(certificate["result"]),
        "certificate self digest",
    )
    require(
        canonical(attachment) == canonical(expected_attachment)
        and canonical(certificate) == canonical(expected_certificate),
        "full independently expected documents",
    )


def resign_attachment_and_certificate(attachment, certificate):
    census = {}
    for name in SCHEMAS:
        table = attachment["result"][name]
        census[name] = {
            "row_count": len(table),
            "rows_sha256": digest(table),
        }
    attachment["result"]["table_census_and_sha256"] = census
    attachment["result_sha256"] = digest(attachment["result"])
    attachment_bytes = (canonical(attachment) + "\n").encode()
    binding = certificate["result"]["row_attachment"]
    binding["result_sha256"] = attachment["result_sha256"]
    binding["file_sha256"] = hashlib.sha256(attachment_bytes).hexdigest()
    binding["table_census_and_sha256"] = copy.deepcopy(census)
    certificate["result_sha256"] = digest(certificate["result"])


def resign_certificate(certificate):
    certificate["result_sha256"] = digest(certificate["result"])


def expect_reject(callable_, label):
    try:
        callable_()
    except Exception:
        return label
    raise RuntimeError(f"attack accepted:{label}")


def semantic_attacks(expected_certificate, expected_attachment):
    rejected = []
    mutable_attachment = copy.deepcopy(expected_attachment)
    attachment_specs = [
        ("origin_residual_volume", "origin_replacement_rows", 0,
         "residual_Round182_retained_coordinate_volume", "1"),
        ("origin_full_flag", "origin_replacement_rows", 0,
         "fully_geometrically_replaced_original_tube", "__TOGGLE_BOOL__"),
        ("origin_global_credit", "origin_replacement_rows", 0,
         "global_exact_key_disposition_credit", 1),
        ("collar_residual_count", "collar_occurrence_rows", 0,
         "residual_leaf_count", 999),
        ("collar_derivative", "collar_occurrence_rows", 0,
         "strict_t_derivative_sign", "OVERWRAP"),
        ("collar_leaf_hash", "collar_occurrence_rows", 0,
         "leaf_rows_sha256", "0" * 64),
        ("collar_inactive", "collar_occurrence_rows", 0,
         "Round179_origin_already_fully_replaced", "__TOGGLE_BOOL__"),
        ("leaf_face", "collar_leaf_rows", 0,
         "lower_t_face_status", "ZZ"),
        ("leaf_class", "collar_leaf_rows", 0,
         "graph_classification", "FAKE"),
        ("leaf_volume", "collar_leaf_rows", 0,
         "coordinate_volume", "1"),
        ("leaf_box", "collar_leaf_rows", 0, "box",
         ["0", "1", "0", "1", "0", "1"]),
        ("pair_existence", "pair_intersection_rows", 0,
         "existence_classification", "FAKE"),
        ("pair_newton", "pair_intersection_rows", 0,
         "interval_newton_interior", "__TOGGLE_BOOL__"),
        ("pair_jacobian", "pair_intersection_rows", 0,
         "strict_2x2_Jacobian_minor_sign", "OVERWRAP"),
        ("pair_source_factor", "pair_intersection_rows", 0,
         "source_graph_exact_factorization", "t=0 by coincidence"),
        ("corner_isolation", "pair_boundary_corner_rows", 0,
         "isolated_zero_dimensional_boundary_corner", False),
        ("corner_promoted_to_component", "pair_boundary_corner_rows", 0,
         "corner_count_kind", "GLOBAL_COMPONENT_COUNT"),
        ("seam_owner", "source_chart_seam_owner_rows", 0,
         "is_half_open_owner", not expected_attachment["result"][
             "source_chart_seam_owner_rows"][0][
                 SEAM_COLUMNS.index("is_half_open_owner")]),
        ("carry_global_credit", "carried_normal_form_rows", 0,
         "global_exact_key_disposition_credit", 1),
    ]
    for label, table_name, row_index, column, replacement in attachment_specs:
        table = mutable_attachment["result"][table_name]
        index = SCHEMAS[table_name].index(column)
        original = table[row_index][index]
        table[row_index][index] = (
            not bool(original)
            if replacement == "__TOGGLE_BOOL__"
            else replacement
        )
        certificate = copy.deepcopy(expected_certificate)
        resign_attachment_and_certificate(mutable_attachment, certificate)
        rejected.append(expect_reject(
            lambda c=certificate, a=mutable_attachment: validate_documents(
                c, a, expected_certificate, expected_attachment
            ),
            label,
        ))
        table[row_index][index] = original
        mutable_attachment["result"]["table_census_and_sha256"] = copy.deepcopy(
            expected_attachment["result"]["table_census_and_sha256"]
        )
        mutable_attachment["result_sha256"] = expected_attachment[
            "result_sha256"
        ]
    certificate_specs = [
        ("cert_status", ("status",), "PASS"),
        ("cert_producer_hash", ("producer", "sha256"), "0" * 64),
        ("cert_precision", ("scope", "precision_bits"), 128),
        ("cert_parent_replay",
         ("scope", "parent_third_full_attachment_replay"), "FAIL"),
        ("cert_closed_volume",
         ("taxonomy", "Round182_closed_retained_coordinate_volume"), "1"),
        ("cert_residual_count",
         ("taxonomy", "Round182_residual_original_tube_count"), 0),
        ("cert_both_curve",
         ("taxonomy", "both_t_face_curve_leaf_count"), 0),
        ("cert_axis_mismatch",
         ("taxonomy", "both_t_face_curve_axis_mismatch_count"), 1),
        ("cert_minor_existence",
         ("dimension_safe_ledger", "pair_1D_intersections",
          "minor_alone_not_used_for_existence"), False),
        ("cert_sheet_order",
         ("dimension_safe_ledger", "clipping_1D_curves",
          "two_face_curves_strictly_ordered_by_whole_box_t_derivative"),
         False),
        ("cert_incidence_promoted_to_component",
         ("dimension_safe_ledger", "boundary_0D",
          "incidences_not_global_component_counts"), False),
        ("cert_owner", ("ownership", "source_chart_diagonal"), "ALL_OWN"),
        ("cert_global_disposition",
         ("global_state", "source_G_global_geometric_dispositions"),
         f"{SOURCE_G_KEYS}/{SOURCE_G_KEYS}"),
        ("cert_gate5", ("global_state", "Gate5_closed_fields"), "18/18"),
        ("cert_D02", ("global_state", "D02"), "CLOSED"),
        ("cert_CM2", ("global_state", "CM2"), "GO"),
        ("cert_promotions", ("global_state", "promotions_issued"), 1),
    ]
    for label, path, replacement in certificate_specs:
        certificate = copy.deepcopy(expected_certificate)
        target = certificate["result"]
        for key in path[:-1]:
            target = target[key]
        target[path[-1]] = replacement
        resign_certificate(certificate)
        rejected.append(expect_reject(
            lambda c=certificate: validate_documents(
                c, expected_attachment,
                expected_certificate, expected_attachment,
            ),
            label,
        ))
    require(len(rejected) == 36, "semantic attack census")
    return rejected


def strict_json_attacks():
    cases = {
        "duplicate_key": b'{"a":1,"a":2}',
        "BOM": b'\xef\xbb\xbf{}',
        "NUL": b'{"a":"\\u0000"}\x00',
        "NaN": b'{"a":NaN}',
        "Infinity": b'{"a":Infinity}',
        "float": b'{"a":1.5}',
        "top_array": b'[]',
        "trailing": b'{}x',
        "surrogate": b'{"a":"\\ud800"}',
    }
    rejected = [
        expect_reject(lambda raw=raw: strict_decode(raw, 1024), label)
        for label, raw in cases.items()
    ]
    rejected.append(expect_reject(
        lambda: strict_decode(b'{"a":"' + b"x" * 1024 + b'"}', 64),
        "oversize",
    ))
    require(len(rejected) == 10, "strict JSON attack census")
    return rejected


def guard_output(path: Path, forbidden: set[Path]) -> Path:
    absolute = Path(os.path.abspath(os.fspath(path)))
    require(absolute.parent.resolve() == BASE, "output parent")
    candidate = BASE / absolute.name
    require(candidate.name not in {item.name for item in forbidden},
            "output protected name")
    if candidate.exists() or candidate.is_symlink():
        info = candidate.lstat()
        require(
            not stat.S_ISLNK(info.st_mode)
            and stat.S_ISREG(info.st_mode)
            and info.st_nlink == 1,
            "output type",
        )
    return candidate


def atomic_write(path: Path, data: bytes):
    descriptor, name = tempfile.mkstemp(
        dir=BASE, prefix=f".{path.name}.", suffix=".tmp"
    )
    temporary = Path(name)
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
            "atomic temporary type",
        )
        os.replace(temporary, path)
        directory = os.open(BASE, os.O_RDONLY | os.O_DIRECTORY)
        try:
            os.fsync(directory)
        finally:
            os.close(directory)
    except BaseException:
        if descriptor >= 0:
            os.close(descriptor)
        if temporary.exists() or temporary.is_symlink():
            temporary.unlink()
        raise


def path_attacks():
    rejected = []
    with tempfile.TemporaryDirectory(dir=BASE) as directory:
        root = Path(directory)
        regular = root / "regular"
        regular.write_bytes(b"x")
        symlink = BASE / (root.name + "-symlink")
        hardlink = BASE / (root.name + "-hardlink")
        directory_path = BASE / (root.name + "-directory")
        oversize = BASE / (root.name + "-oversize")
        output_symlink = BASE / (root.name + "-output-symlink")
        output_hardlink = BASE / (root.name + "-output-hardlink")
        victim = root / "victim"
        victim.write_bytes(b"SAFE")
        created = []
        try:
            symlink.symlink_to(regular)
            created.append(symlink)
            os.link(regular, hardlink)
            created.append(hardlink)
            directory_path.mkdir()
            created.append(directory_path)
            oversize.write_bytes(b"x" * 65)
            created.append(oversize)
            output_symlink.symlink_to(victim)
            created.append(output_symlink)
            os.link(regular, output_hardlink)
            created.append(output_hardlink)
            rejected.extend([
                expect_reject(lambda: input_bytes(symlink, 100), "input_symlink"),
                expect_reject(lambda: input_bytes(hardlink, 100), "input_hardlink"),
                expect_reject(lambda: input_bytes(directory_path, 100), "input_directory"),
                expect_reject(lambda: input_bytes(oversize, 64), "input_oversize"),
                expect_reject(
                    lambda: input_bytes(BASE.parent / "outside", 100),
                    "input_outside_parent",
                ),
                expect_reject(
                    lambda: guard_output(PRODUCER, {PRODUCER}),
                    "output_producer_alias",
                ),
                expect_reject(
                    lambda: guard_output(ATTACHMENT, {ATTACHMENT}),
                    "output_attachment_alias",
                ),
                expect_reject(
                    lambda: guard_output(CERTIFICATE, {CERTIFICATE}),
                    "output_certificate_alias",
                ),
                expect_reject(
                    lambda: guard_output(output_symlink, set()),
                    "output_symlink",
                ),
                expect_reject(
                    lambda: guard_output(output_hardlink, set()),
                    "output_hardlink",
                ),
            ])
            predictable = BASE / (root.name + ".tmp.123")
            predictable.symlink_to(victim)
            created.append(predictable)
            safe_target = BASE / (root.name + "-safe-target")
            atomic_write(safe_target, b"NEW")
            require(
                victim.read_bytes() == b"SAFE"
                and safe_target.read_bytes() == b"NEW"
                and predictable.is_symlink(),
                "prepositioned temporary symlink untouched",
            )
            rejected.append("prepositioned_temp_symlink_not_followed")
            safe_target.unlink()
            dangling = BASE / (root.name + "-dangling")
            dangling.symlink_to(root / "missing")
            created.append(dangling)
            rejected.append(expect_reject(
                lambda: input_bytes(dangling, 100), "dangling_symlink"
            ))
        finally:
            for item in reversed(created):
                if item.is_symlink() or item.is_file():
                    item.unlink()
                elif item.exists():
                    item.rmdir()
    require(len(rejected) == 12, "path attack census")
    return rejected


def build_verification():
    ctx.prec = PRECISION_BITS
    (
        source, actual_certificate, actual_attachment,
        certificate_raw, attachment_raw,
    ) = load_source_and_documents()
    expected_attachment, tables = independently_rebuild_attachment(source)
    expected_attachment_bytes = (
        canonical(expected_attachment) + "\n"
    ).encode()
    attachment_byte_count = len(expected_attachment_bytes)
    require(
        expected_attachment["result_sha256"]
        == EXPECTED_ATTACHMENT_RESULT
        and hashlib.sha256(expected_attachment_bytes).hexdigest()
        == EXPECTED_ATTACHMENT_SHA256
        and expected_attachment_bytes == attachment_raw,
        "full expected attachment bytes",
    )
    stats = independent_statistics(tables)
    expected_certificate = independently_expected_certificate(
        stats, expected_attachment,
        hashlib.sha256(expected_attachment_bytes).hexdigest(),
    )
    expected_certificate_bytes = (
        canonical(expected_certificate) + "\n"
    ).encode()
    require(
        expected_certificate["result_sha256"]
        == EXPECTED_CERTIFICATE_RESULT
        and hashlib.sha256(expected_certificate_bytes).hexdigest()
        == EXPECTED_CERTIFICATE_SHA256
        and expected_certificate_bytes == certificate_raw,
        "full expected certificate bytes",
    )
    validate_documents(
        actual_certificate, actual_attachment,
        expected_certificate, expected_attachment,
    )
    del (
        source, tables, actual_certificate, actual_attachment,
        certificate_raw, attachment_raw,
        expected_attachment_bytes, expected_certificate_bytes,
    )
    gc.collect()
    semantic = semantic_attacks(expected_certificate, expected_attachment)
    strict_json = strict_json_attacks()
    paths = path_attacks()
    producer_module = (
        "cm2_round182_source_g_clipped_graph_and_pair_arrangement"
    )
    require(producer_module not in __import__("sys").modules,
            "producer never imported")
    result = {
        "status": "PASS",
        "verifier_filename": Path(__file__).name,
        "verifier_sha256": hashlib.sha256(
            input_bytes(Path(__file__).resolve(), 300_000)
        ).hexdigest(),
        "producer_filename": PRODUCER.name,
        "producer_sha256": EXPECTED_PRODUCER_SHA256,
        "certificate_filename": CERTIFICATE.name,
        "certificate_file_sha256": EXPECTED_CERTIFICATE_SHA256,
        "certificate_result_sha256": EXPECTED_CERTIFICATE_RESULT,
        "attachment_filename": ATTACHMENT.name,
        "attachment_file_sha256": EXPECTED_ATTACHMENT_SHA256,
        "attachment_result_sha256": EXPECTED_ATTACHMENT_RESULT,
        "full_attachment_byte_for_byte_matched": True,
        "full_attachment_rebuilt_byte_count": attachment_byte_count,
        "complete_expected_certificate_rebuilt": True,
        "producer_imported_or_executed": False,
        "upstream_evaluator": (
            "pinned Round179 independent verifier library only"
        ),
        "precision_bits": PRECISION_BITS,
        "python_flint_version": FLINT_VERSION,
        "taxonomy": stats,
        "dimension_checks": {
            "3D_retained_volume_exactly_conserved": True,
            "2D_graphs_not_subtracted_as_3D_volume": True,
            "both_face_curve_leaf_count":
                stats["both_t_face_curve_leaf_count"],
            "both_face_curve_axis_mismatch_count":
                stats["both_t_face_curve_axis_mismatch_count"],
            "both_face_curves_ordered_by_strict_whole_box_t_derivative":
                True,
            "pair_actual_1D_lines":
                stats["actual_transverse_1D_pair_intersection_count"],
            "pair_actual_0D_boundary_incidences":
                stats["actual_pair_boundary_0D_corner_incidence_count"],
        },
        "attack_rejections": {
            "semantic_resigned_count": len(semantic),
            "semantic_resigned_labels": semantic,
            "strict_JSON_count": len(strict_json),
            "strict_JSON_labels": strict_json,
            "path_type_alias_and_temp_count": len(paths),
            "path_type_alias_and_temp_labels": paths,
        },
        "global_state_reconfirmed": {
            "source_G_global_dispositions": f"0/{SOURCE_G_KEYS}",
            "Gate5": "10/18",
            "complete_18_field_blocks": 0,
            "D02": "BLOCKED",
            "D03_negative_oracle": "UNAUTHORIZED",
            "CM2": "NO-GO",
        },
    }
    return {
        "schema": VERIFICATION_SCHEMA,
        "result": result,
        "result_sha256": digest(result),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument("--expect-result")
    parser.add_argument("--print-only", action="store_true")
    args = parser.parse_args()
    readonly = {
        Path(__file__).resolve(), PRODUCER, CERTIFICATE, ATTACHMENT,
        *(BASE / name for name in PINS),
    }
    output = guard_output(args.output, readonly)
    verification = build_verification()
    if args.expect_result:
        require(
            verification["result_sha256"] == args.expect_result,
            "expected verification result",
        )
    if args.print_only:
        print(canonical(verification))
        return 0
    atomic_write(output, (canonical(verification) + "\n").encode())
    print(canonical({
        "output": output.name,
        "result_sha256": verification["result_sha256"],
        "status": "PASS",
    }))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
