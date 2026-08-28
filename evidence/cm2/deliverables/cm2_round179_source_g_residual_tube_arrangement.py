#!/usr/bin/env python3
"""Round179: dimension-safe source-G residual-tube arrangement.

Round174 left 62,012 positive-volume residual tubes.  This bounded
continuation processes every one of them in two independent ways:

* one additional adaptive dyadic split releases strict regular occurrence
  cells and exact rational source-chart guards while retaining every
  unresolved positive-volume child; and
* interval-gradient normal forms classify every outgoing-chart and
  integer-wall predicate, without promoting a derivative sign to graph
  existence unless the corresponding endpoint signs prove it.

Two-predicate rows are retained as nominal intersection/corner candidates.
No local occurrence, chart guard, child cell, analytic graph, or candidate
intersection is a global exact-key disposition.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import os
import stat
from collections import Counter, defaultdict
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from flint import arb, ctx, __version__ as FLINT_VERSION

import cm2_round174_source_g_unique_first_dynamic_occurrence_materialization_verifier as r174


HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "cm2_round179_source_g_residual_tube_arrangement_certificate.json"
ATTACHMENT = HERE / "cm2_round179_source_g_residual_tube_arrangement_rows.json"
SCHEMA = "cm2.round179.source-g-residual-tube-arrangement.v1"
ATTACHMENT_SCHEMA = "cm2.round179.source-g-residual-tube-arrangement-rows.v1"
STATUS = (
    "CERTIFIED_BOUNDED_PARTIAL_SOURCE_G_RESIDUAL_TUBE_ARRANGEMENT__"
    "NO_GLOBAL_DISPOSITION_OR_D02_PROMOTION"
)
PRECISION_BITS = 256
SOURCE_G_KEY_COUNT = 224580

R171P = "cm2_round171_compact_gate3_source_g_coordinate_bridge.py"
R171C = "cm2_round171_compact_gate3_source_g_coordinate_bridge_certificate.json"
R171V = "cm2_round171_compact_gate3_source_g_coordinate_bridge_verifier.py"
R171O = "cm2_round171_compact_gate3_source_g_coordinate_bridge_verification.json"
R171M = (
    "cm2-round171-compact-gate3-source-g-coordinate-bridge-manifest-"
    "2026-07-26.sha256"
)
R173P = "cm2_round173_source_g_exact_return_signature_transport.py"
R173C = "cm2_round173_source_g_exact_return_signature_transport_certificate.json"
R173V = "cm2_round173_source_g_exact_return_signature_transport_verifier.py"
R173O = "cm2_round173_source_g_exact_return_signature_transport_verification.json"
R173M = (
    "cm2-round173-source-g-exact-return-signature-transport-manifest-"
    "2026-07-26.sha256"
)
R174P = (
    "cm2_round174_source_g_unique_first_dynamic_occurrence_materialization.py"
)
R174C = (
    "cm2_round174_source_g_unique_first_dynamic_occurrence_materialization_"
    "certificate.json"
)
R174A = (
    "cm2_round174_source_g_unique_first_dynamic_occurrence_materialization_"
    "rows.json"
)
R174V = (
    "cm2_round174_source_g_unique_first_dynamic_occurrence_materialization_"
    "verifier.py"
)
R174O = (
    "cm2_round174_source_g_unique_first_dynamic_occurrence_materialization_"
    "verification.json"
)
R174M = (
    "cm2_round174_source_g_unique_first_dynamic_occurrence_materialization_"
    "manifest.sha256"
)
G5M = "cm2-gate5-return-word-three-norm-frontier-manifest-2026-07-16.json"
FHP = "cm2_gate3_candidate_first_hit_cert.py"
G3P = "cm2_gate3_eight_cell_symmetry_atlas_cert.py"

PINS = {
    R171P: "bcaba20978ebb5386d64bcf248d254c54c8ac79d9c9c7eb023be278ab7e05c75",
    R171C: "1fb4827b42569d41602765445d0333c76b2ef97615873fc406563ac0e18af7a5",
    R171V: "aee7b3cc3f1468b6a46e7a90e1bb219bd609bddfe54075c6c73e124d98eda7e0",
    R171O: "effdfd4306dbf7bd70df1e9b5ed9166a58dc00a5d333b0f2f2a5f0cb930ccce9",
    R171M: "b86a5faa33f503a2de6139f7765fda4e54e027954373ecdf8b8d587ba179417c",
    R173P: "bdbf794a99dc9276b11b7680818994d63f52fe0e5a857948701f64e8d5d16a0f",
    R173C: "5ff82c5822f543109da0d50c0637d0d2f9148a738b1a21b16878c70e5505cf1a",
    R173V: "eb2b51929719563cd9fe72d180f3f1932a049e983ad1e7a8ec9ac89526bc30f1",
    R173O: "e205367506bc02aa982de074253e5806f07b4358dd3738fb4a0e14476e44ce99",
    R173M: "ba2a1b6eea612e538e3ca70e2916e07469fda38eaef24a751ff862262336f275",
    R174P: "3d329525dda6697a3a5d2a8227c94bd9c309ea7ebcc4cdd0c7fbe573c267a218",
    R174C: "10221141c58c044b42e43009beb34ae4705995925a88deaa70ff2eba2ea852c7",
    R174A: "9edeea2e1033b0dd70dee11a53b0f6aeb21fe74030aeefb60b081a7c420cff54",
    R174V: "c7ead7c9cb8b4d7b8680e64bfb7870e5c5f5e39277e7c7d3d08a62b600f5c058",
    R174O: "1f65b5e02b1d1e63bd7e41d6a88d5eb180e2be92620af4b8afa2141c9f6e344c",
    R174M: "9e92db7748a2c0acdce532c830f899ce153765de64a59e9f372df3099ac91b76",
    G5M: "47e84e8b75b289b7a5db4afcbd7dfa8dac909d2f76fa1c95ef290546d031a866",
    FHP: "6d224d74cda186a40ef9956d1dd6556d5a7b9f506d47c942427ceb66fd705bd2",
    G3P: "d867f5cb03691289033d1a0d0e277a03e8395d70aae7e0689446d7aa63eac3da",
}
R171_RESULT = "ffac0e2e16829c1a3ffc4783af2c224288265d02cf53c1d041aaf02013b52957"
R171_VERIFY_RESULT = (
    "60e9d4038c63bba14c0bd95478f63840735d8283f9cdfdefb1405ee2ed7defe3"
)
R173_RESULT = "948ab0a8539b08adc96c9493de415b44a5ffb75a1ee3ef47a4742902c211c11f"
R173_VERIFY_RESULT = (
    "047a580eb546cdb3880b93a9d0358e390d7ce418b371612f8e9fc4b0528f4644"
)
R174_RESULT = "d45f05458c42189cf0ebc51e258356d13278ba40845cce80b6a072ffbc8cf09b"
R174_ATTACHMENT_RESULT = (
    "002ca6631edd39c2325c63a1e8f9717d111f4d10c6d2585077d665a0ff128d18"
)
R174_VERIFY_RESULT = (
    "6c82800d41e456aeed7000bccb13bfe0e5e6d5f1637ac52a4d5c45b24ed9a23b"
)


def canonical(value: Any) -> str:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    )


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def require(condition: bool, label: str) -> None:
    if not condition:
        raise RuntimeError(label)


def qstr(value: Q) -> str:
    return (
        str(value.numerator)
        if value.denominator == 1
        else f"{value.numerator}/{value.denominator}"
    )


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
        "strict JSON raw",
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
        raw.decode("utf-8"),
        object_pairs_hook=unique,
        parse_constant=reject,
        parse_float=reject,
    )
    require(type(value) is dict, "JSON top object")
    return value


def strict_load(path: Path, maximum: int) -> dict[str, Any]:
    return strict_decode(safe_input(path, maximum))


def unwrap(
    document: dict[str, Any],
    schema: str,
    result_sha256: str,
    status: str,
) -> dict[str, Any]:
    require(
        set(document) == {"schema", "result", "result_sha256"}
        and document["schema"] == schema
        and document["result_sha256"]
        == result_sha256
        == digest(document["result"])
        and document["result"]["status"] == status,
        f"wrapper:{schema}",
    )
    return document["result"]


def load_inputs() -> dict[str, Any]:
    require(FLINT_VERSION == "0.9.0", "python-flint version")
    for name, expected in PINS.items():
        require(
            hashlib.sha256(safe_input(HERE / name, 180_000_000)).hexdigest()
            == expected,
            f"pin:{name}",
        )
    r171 = unwrap(
        strict_load(HERE / R171C, 2_000_000),
        "cm2.round171.compact-gate3-source-g-coordinate-bridge.v1",
        R171_RESULT,
        "CERTIFIED_COMPACT_TO_GATE3_SOURCE_G_COORDINATE_COVER__"
        "NO_RETURN_KEY_OR_D02_PROMOTION",
    )
    r171v = unwrap(
        strict_load(HERE / R171O, 2_000_000),
        "cm2.round171.compact-gate3-source-g-coordinate-bridge.verification.v1",
        R171_VERIFY_RESULT,
        "PASS",
    )
    r173 = unwrap(
        strict_load(HERE / R173C, 2_000_000),
        "cm2.round173.source-g-exact-return-signature-transport.v1",
        R173_RESULT,
        "CERTIFIED_SOURCE_G_JX_JY_EXACT_RETURN_SIGNATURE_TRANSPORT_DICTIONARY__"
        "NO_DYNAMIC_ROW_OR_D02_PROMOTION",
    )
    r173v = unwrap(
        strict_load(HERE / R173O, 2_000_000),
        "cm2.round173.source-g-exact-return-signature-transport.verification.v1",
        R173_VERIFY_RESULT,
        "PASS",
    )
    r174c = unwrap(
        strict_load(HERE / R174C, 2_000_000),
        "cm2.round174.source-g-unique-first-dynamic-occurrence-materialization.v1",
        R174_RESULT,
        "CERTIFIED_BOUNDED_PARTIAL_SOURCE_G_UNIQUE_FIRST_DYNAMIC_OCCURRENCE_ROWS__"
        "NO_GLOBAL_DISPOSITION_OR_D02_PROMOTION",
    )
    r174v = unwrap(
        strict_load(HERE / R174O, 2_000_000),
        "cm2.round174.source-g-unique-first-dynamic-occurrence-materialization."
        "verification.v1",
        R174_VERIFY_RESULT,
        "PASS",
    )
    r174a_document = strict_load(HERE / R174A, 180_000_000)
    require(
        r174a_document["schema"]
        == "cm2.round174.source-g-unique-first-dynamic-occurrence-rows.v1"
        and r174a_document["result_sha256"]
        == R174_ATTACHMENT_RESULT
        == digest(r174a_document["result"]),
        "Round174 attachment wrapper",
    )
    require(
        r171v["certificate_result_sha256"] == R171_RESULT
        and r173v["certificate_result_sha256"] == R173_RESULT
        and r174v["certificate_result_sha256"] == R174_RESULT
        and r174v["attachment_result_sha256"] == R174_ATTACHMENT_RESULT
        and r174v["full_attachment_byte_for_byte_matched"] is True
        and r174v["producer_imported_or_executed"] is False
        and r174c["materialization_census"][
            "residual_3d_tube_row_count"
        ] == 62012
        and r174c["materialization_census"][
            "bounded_partial_nonempty_parent_count"
        ] == 3840
        and r174c["observed_occurrence_vs_global_disposition"][
            "global_geometric_exact_key_disposition_count_after_Round174"
        ] == 0
        and r174c["strict_nonpromotion"]["D02"] == "BLOCKED",
        "prior verification and no-credit binding",
    )
    gate5 = strict_load(HERE / G5M, 5_000_000)
    registry = r174.rebuild_registry(gate5)
    return {
        "r171": r171,
        "r173": r173,
        "r174c": r174c,
        "r174v": r174v,
        "r174a": r174a_document["result"],
        "registry": registry,
    }


def make_id(prefix: str, payload: Any) -> str:
    return f"round179-{prefix}:{digest(payload)}"


def box_from(values: list[str], depth: int, path: str) -> Any:
    return r174.atlas.AtlasBox(
        *map(Q, values), depth, path
    )


def sign(value: arb) -> str:
    if bool(value > 0):
        return "STRICT_POSITIVE"
    if bool(value < 0):
        return "STRICT_NEGATIVE"
    return "OVERWRAP"


def dual_add(a: tuple[Any, tuple[Any, ...]], b: tuple[Any, tuple[Any, ...]]):
    return (
        a[0] + b[0],
        tuple(
            None if x is None or y is None else x + y
            for x, y in zip(a[1], b[1], strict=True)
        ),
    )


def dual_neg(a: tuple[Any, tuple[Any, ...]]):
    return (
        -a[0],
        tuple(None if x is None else -x for x in a[1]),
    )


def dual_sub(a: tuple[Any, tuple[Any, ...]], b: tuple[Any, tuple[Any, ...]]):
    return dual_add(a, dual_neg(b))


def dual_mul(a: tuple[Any, tuple[Any, ...]], b: tuple[Any, tuple[Any, ...]]):
    return (
        a[0] * b[0],
        tuple(
            None if x is None or y is None else x * b[0] + a[0] * y
            for x, y in zip(a[1], b[1], strict=True)
        ),
    )


def dual_scale(a: tuple[Any, tuple[Any, ...]], factor: Any):
    return (
        a[0] * factor,
        tuple(None if x is None else x * factor for x in a[1]),
    )


def dual_constant(value: arb):
    return value, (arb(0), arb(0), arb(0))


def interval_geometry(chart: str, target_id: str, box: Any) -> dict[str, Any]:
    t = (
        r174.first_hit.arb_interval(box.t0, box.t1),
        (arb(1), arb(0), arb(0)),
    )
    p = (
        r174.first_hit.arb_interval(box.p0, box.p1),
        (arb(0), arb(1), arb(0)),
    )
    s = (
        r174.first_hit.arb_interval(box.s0, box.s1),
        (arb(0), arb(0), arb(1)),
    )
    rn_value = r174.atlas.ge.sqrt_one_minus_square(box.t0, box.t1)
    rp_value = r174.atlas.ge.sqrt_one_minus_square(box.p0, box.p1)
    rn = (
        rn_value,
        (-t[0] / rn_value, arb(0), arb(0)),
    )
    rp = (
        rp_value,
        (
            arb(0),
            None if not bool(rp_value > 0) else -p[0] / rp_value,
            arb(0),
        ),
    )
    cell = chart.split(":")[1]
    if cell == "E":
        nx, ny = rn, t
    elif cell == "W":
        nx, ny = dual_neg(rn), t
    elif cell == "N":
        nx, ny = t, rn
    else:
        nx, ny = t, dual_neg(rn)
    ux = dual_sub(dual_mul(rp, nx), dual_mul(p, ny))
    uy = dual_add(dual_mul(rp, ny), dual_mul(p, nx))
    source_radius = arb(9) / 25
    source_x = dual_scale(nx, source_radius)
    source_y = dual_scale(ny, source_radius)
    target = r174.first_hit.target_by_id(target_id)
    if target.obstacle == "G":
        center_x = dual_constant(arb(target.ix))
        center_y = dual_constant(arb(target.iy))
    else:
        center_x = dual_add(
            dual_constant(arb(target.ix) + arb(1) / 2),
            s,
        )
        center_y = dual_constant(arb(target.iy) + arb(1) / 2)
    dx = dual_sub(center_x, source_x)
    dy = dual_sub(center_y, source_y)
    transverse = dual_add(
        dual_neg(dual_mul(uy, dx)),
        dual_mul(ux, dy),
    )
    target_radius_q = r174.first_hit.RADIUS[target.obstacle]
    target_radius = (
        arb(target_radius_q.numerator) / target_radius_q.denominator
    )
    discriminant = dual_sub(
        dual_constant(target_radius * target_radius),
        dual_mul(transverse, transverse),
    )
    require(bool(discriminant[0] > 0), "selected root discriminant strict")
    radical_value = discriminant[0].sqrt()
    radical = (
        radical_value,
        tuple(
            None if derivative is None
            else derivative / (2 * radical_value)
            for derivative in discriminant[1]
        ),
    )
    outgoing_x = dual_scale(
        dual_add(
            dual_neg(dual_mul(radical, ux)),
            dual_mul(transverse, uy),
        ),
        1 / target_radius,
    )
    outgoing_y = dual_scale(
        dual_sub(
            dual_neg(dual_mul(radical, uy)),
            dual_mul(transverse, ux),
        ),
        1 / target_radius,
    )
    hit_x = dual_add(center_x, dual_scale(outgoing_x, target_radius))
    hit_y = dual_add(center_y, dual_scale(outgoing_y, target_radius))
    outgoing_equality = dual_sub(
        dual_mul(outgoing_x, outgoing_x),
        dual_mul(outgoing_y, outgoing_y),
    )
    return {
        "source_x": source_x,
        "source_y": source_y,
        "hit_x": hit_x,
        "hit_y": hit_y,
        "outgoing_x": outgoing_x,
        "outgoing_y": outgoing_y,
        "outgoing_equality": outgoing_equality,
    }


def strict_derivative_axes(dual: tuple[Any, tuple[Any, ...]]) -> tuple[str, ...]:
    return tuple(
        axis
        for axis, derivative in zip("tps", dual[1], strict=True)
        if derivative is not None and sign(derivative) != "OVERWRAP"
    )


def fixed_axis_face(box: Any, axis: str, upper: bool) -> Any:
    if axis == "t":
        value = box.t1 if upper else box.t0
        values = (value, value, box.p0, box.p1, box.s0, box.s1)
    elif axis == "p":
        value = box.p1 if upper else box.p0
        values = (box.t0, box.t1, value, value, box.s0, box.s1)
    else:
        value = box.s1 if upper else box.s0
        values = (box.t0, box.t1, box.p0, box.p1, value, value)
    return r174.atlas.AtlasBox(*values, box.depth, box.path)


def face_classification(lower: arb, upper: arb) -> str:
    lower_sign = sign(lower)
    upper_sign = sign(upper)
    if (
        {lower_sign, upper_sign}
        == {"STRICT_NEGATIVE", "STRICT_POSITIVE"}
    ):
        return "FULL_BASE_UNIQUE_GRAPH"
    if (
        lower_sign == upper_sign
        and lower_sign in {"STRICT_NEGATIVE", "STRICT_POSITIVE"}
    ):
        return "STRICT_ZERO_ABSENT"
    return "FACE_OVERWRAP_REGULAR_ZERO_SET_IF_PRESENT"


ORIGIN_COLUMNS = [
    "origin_row_id", "parent_id", "chart", "owner_target",
    "original_refinement_path", "original_box", "original_coordinate_volume",
    "original_reason_labels", "reason_count", "chosen_split_axis",
    "resolved_child_count", "resolved_child_coordinate_volume",
    "guard_child_count", "guard_child_coordinate_volume",
    "retained_child_count", "retained_child_coordinate_volume",
    "fully_replaced_by_bounded_children", "released_exact_key_count",
    "released_exact_key_ordinals_sha256", "provenance",
]
RESOLVED_COLUMNS = [
    "row_id", "origin_row_id", "parent_id", "chart", "child_index",
    "refinement_path", "box", "coordinate_volume", "owner_target",
    "ordered_integer_wall_events", "signed_wall_word", "roof",
    "outgoing_cell", "target_chart", "official_key_row",
    "official_key_ordinal", "official_key_id", "ambient_dimension",
    "credit_kind", "global_geometric_disposition_credit",
]
RETAINED_COLUMNS = [
    "row_id", "origin_row_id", "parent_id", "chart", "child_index",
    "refinement_path", "box", "coordinate_volume", "reason_labels",
    "ambient_dimension", "whole_origin_credit",
    "global_geometric_disposition_credit", "provenance",
]
GUARD_COLUMNS = [
    "row_id", "origin_row_id", "parent_id", "chart", "child_index",
    "refinement_path", "box", "coordinate_volume",
    "exact_rejection_predicate", "is_CM2_exterior_sheet_exclusion",
    "is_Gate5_geometric_disposition", "provenance",
]
OUTGOING_COLUMNS = [
    "row_id", "origin_row_id", "parent_id", "chart", "equation",
    "gradient_axis", "gradient_sign", "regularity_certification",
    "lower_t_face_sign", "upper_t_face_sign", "face_classification",
    "zero_set_dimension_account", "existence_over_full_base",
    "two_open_3d_sides_retained", "whole_origin_credit",
    "global_geometric_disposition_credit", "provenance",
]
WALL_COLUMNS = [
    "row_id", "origin_row_id", "parent_id", "chart", "reason_label",
    "axis", "integer_wall", "zero_equation",
    "source_factor_classification", "source_gradient_axis",
    "source_gradient_sign", "target_factor_classification",
    "target_gradient_axis", "target_gradient_sign",
    "target_lower_face_sign", "target_upper_face_sign",
    "target_face_classification", "zero_set_dimension_account",
    "crossing_time_dependency_overwrap_discharged",
    "whole_origin_credit", "global_geometric_disposition_credit",
    "provenance",
]
SOURCE_SEAM_COLUMNS = [
    "row_id", "origin_row_id", "parent_id", "chart", "equation",
    "gradient_axis", "gradient_sign", "lower_t_face_sign",
    "upper_t_face_sign", "face_classification", "exact_dimension",
    "half_open_owner_status", "whole_origin_credit",
    "global_geometric_disposition_credit", "provenance",
]
ARRANGEMENT_COLUMNS = [
    "row_id", "origin_row_id", "parent_id", "chart", "reason_labels",
    "predicate_count", "candidate_pair_intersection_dimension",
    "candidate_boundary_corner_dimension", "existence_certification",
    "transversality_certification", "isolation_certification",
    "whole_origin_credit", "global_geometric_disposition_credit",
    "provenance",
]
KEY_CLUSTER_COLUMNS = [
    "cluster_id", "released_exact_key_ordinals",
    "released_exact_key_ordinals_sha256", "fully_replaced_origin_count",
    "global_geometric_disposition_credit",
]


def pack_row(columns: list[str], row: dict[str, Any]) -> list[Any]:
    require(set(columns) == set(row), "row exact keys")
    return [row[column] for column in columns]


def unpack_round174_rows(
    attachment: dict[str, Any],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    schemas = attachment["row_column_schemas"]
    parent_columns = schemas["parent_rows"]
    residual_columns = schemas["residual_3d_tube_rows"]
    parents = [
        dict(zip(parent_columns, row, strict=True))
        for row in attachment["parent_rows"]
    ]
    residual = [
        dict(zip(residual_columns, row, strict=True))
        for row in attachment["residual_3d_tube_rows"]
    ]
    require(
        len(parents) == 21232
        and len(residual) == 62012
        and all(len(row["refinement_path"]) == 6 for row in residual),
        "Round174 unpacked census",
    )
    return parents, residual


def build_resolved_child(
    origin: dict[str, Any],
    owner: str,
    child_index: int,
    axis_name: str,
    child: Any,
    signature: dict[str, Any],
) -> dict[str, Any]:
    path = [*origin["refinement_path"], f"{axis_name}{child_index}"]
    payload = [
        origin["row_id"], child_index, path,
        r174.box_values(child), signature["key"]["identifier"],
        signature["outgoing"],
    ]
    return {
        "row_id": make_id("resolved-child", payload),
        "origin_row_id": origin["row_id"],
        "parent_id": origin["parent_id"],
        "chart": origin["chart"],
        "child_index": child_index,
        "refinement_path": path,
        "box": r174.box_values(child),
        "coordinate_volume": qstr(r174.volume(child)),
        "owner_target": owner,
        "ordered_integer_wall_events": signature["events"],
        "signed_wall_word": list(signature["pattern"]),
        "roof": signature["roof"],
        "outgoing_cell": signature["outgoing"],
        "target_chart": signature["target_chart"],
        "official_key_row": signature["key"]["row"],
        "official_key_ordinal": signature["key"]["ordinal"],
        "official_key_id": signature["key"]["identifier"],
        "ambient_dimension": 3,
        "credit_kind": "LOCAL_POSITIVE_3D_OCCURRENCE_ONLY",
        "global_geometric_disposition_credit": 0,
    }


def build_guard_child(
    origin: dict[str, Any],
    child_index: int,
    axis_name: str,
    child: Any,
) -> dict[str, Any]:
    path = [*origin["refinement_path"], f"{axis_name}{child_index}"]
    payload = [origin["row_id"], child_index, path, r174.box_values(child)]
    return {
        "row_id": make_id("chart-guard-child", payload),
        "origin_row_id": origin["row_id"],
        "parent_id": origin["parent_id"],
        "chart": origin["chart"],
        "child_index": child_index,
        "refinement_path": path,
        "box": r174.box_values(child),
        "coordinate_volume": qstr(r174.volume(child)),
        "exact_rejection_predicate": "min|t| gives 2*t^2-1>0",
        "is_CM2_exterior_sheet_exclusion": False,
        "is_Gate5_geometric_disposition": False,
        "provenance": "ROUND179_EXACT_RATIONAL_SOURCE_CHART_GUARD",
    }


def build_retained_child(
    origin: dict[str, Any],
    child_index: int,
    axis_name: str,
    child: Any,
    reasons: list[str],
) -> dict[str, Any]:
    reasons = sorted(set(reasons))
    path = [*origin["refinement_path"], f"{axis_name}{child_index}"]
    payload = [
        origin["row_id"], child_index, path, r174.box_values(child), reasons
    ]
    return {
        "row_id": make_id("retained-child", payload),
        "origin_row_id": origin["row_id"],
        "parent_id": origin["parent_id"],
        "chart": origin["chart"],
        "child_index": child_index,
        "refinement_path": path,
        "box": r174.box_values(child),
        "coordinate_volume": qstr(r174.volume(child)),
        "reason_labels": reasons,
        "ambient_dimension": 3,
        "whole_origin_credit": 0,
        "global_geometric_disposition_credit": 0,
        "provenance": "ROUND179_ONE_STEP_POSITIVE_VOLUME_REMAINDER",
    }


def one_step_origin(
    origin: dict[str, Any],
    owner: str,
    registry: dict[str, Any],
) -> dict[str, Any]:
    box = box_from(
        origin["box"],
        len(origin["refinement_path"]),
        origin["row_id"],
    )
    reasons = origin["reason_labels"]
    eligible_axes = (
        (0,) if "source_chart_seam" in reasons else (0, 1, 2)
    )
    widths = (
        box.t1 - box.t0,
        box.p1 - box.p0,
        box.s1 - box.s0,
    )
    options = []
    for axis_index in eligible_axes:
        children = r174.bisect(box, axis_index)
        evaluations = [
            r174.classify_child(
                origin["chart"], child, owner, registry
            )
            for child in children
        ]
        released = sum(
            (
                r174.volume(child)
                for child, evaluation
                in zip(children, evaluations, strict=True)
                if evaluation[0] in {"resolved", "guard"}
            ),
            Q(0),
        )
        options.append((
            released, widths[axis_index] / widths[axis_index],
            -axis_index, axis_index, children, evaluations,
        ))
    (
        _released, _relative, _tie, chosen_axis,
        children, evaluations,
    ) = max(options, key=lambda option: option[:3])
    axis_name = ("t", "p", "s")[chosen_axis]
    resolved: list[dict[str, Any]] = []
    guards: list[dict[str, Any]] = []
    retained: list[dict[str, Any]] = []
    for child_index, (child, evaluation) in enumerate(
        zip(children, evaluations, strict=True)
    ):
        kind, data = evaluation
        if kind == "resolved":
            resolved.append(build_resolved_child(
                origin, owner, child_index, axis_name, child, data
            ))
        elif kind == "guard":
            guards.append(build_guard_child(
                origin, child_index, axis_name, child
            ))
        else:
            retained.append(build_retained_child(
                origin, child_index, axis_name, child, data
            ))
    resolved_volume = sum(
        (Q(row["coordinate_volume"]) for row in resolved), Q(0)
    )
    guard_volume = sum(
        (Q(row["coordinate_volume"]) for row in guards), Q(0)
    )
    retained_volume = sum(
        (Q(row["coordinate_volume"]) for row in retained), Q(0)
    )
    original_volume = Q(origin["coordinate_volume"])
    require(
        resolved_volume + guard_volume + retained_volume == original_volume,
        "one-step origin exact volume conservation",
    )
    ordinals = sorted({
        row["official_key_ordinal"] for row in resolved
    })
    summary = {
        "origin_row_id": origin["row_id"],
        "parent_id": origin["parent_id"],
        "chart": origin["chart"],
        "owner_target": owner,
        "original_refinement_path": origin["refinement_path"],
        "original_box": origin["box"],
        "original_coordinate_volume": origin["coordinate_volume"],
        "original_reason_labels": reasons,
        "reason_count": len(reasons),
        "chosen_split_axis": axis_name,
        "resolved_child_count": len(resolved),
        "resolved_child_coordinate_volume": qstr(resolved_volume),
        "guard_child_count": len(guards),
        "guard_child_coordinate_volume": qstr(guard_volume),
        "retained_child_count": len(retained),
        "retained_child_coordinate_volume": qstr(retained_volume),
        "fully_replaced_by_bounded_children": len(retained) == 0,
        "released_exact_key_count": len(ordinals),
        "released_exact_key_ordinals_sha256": digest(ordinals),
        "provenance": "ROUND174_RESIDUAL_PLUS_ONE_ADAPTIVE_DYADIC_SPLIT",
    }
    return {
        "summary": summary,
        "resolved": resolved,
        "guards": guards,
        "retained": retained,
        "ordinals": ordinals,
    }


def outgoing_row(
    origin: dict[str, Any],
    owner: str,
    geometry: dict[str, Any],
) -> dict[str, Any]:
    equality = geometry["outgoing_equality"]
    require(sign(equality[0]) == "OVERWRAP", "outgoing residual overwrap")
    axes = strict_derivative_axes(equality)
    require(axes and axes[0] == "t", "outgoing strict t derivative")
    derivative_sign = sign(equality[1][0])
    box = box_from(
        origin["box"], len(origin["refinement_path"]), origin["row_id"]
    )
    lower = interval_geometry(
        origin["chart"], owner, fixed_axis_face(box, "t", False)
    )["outgoing_equality"][0]
    upper = interval_geometry(
        origin["chart"], owner, fixed_axis_face(box, "t", True)
    )["outgoing_equality"][0]
    face = face_classification(lower, upper)
    if face == "FULL_BASE_UNIQUE_GRAPH":
        dimension = "EXACT_REGULAR_DIMENSION_2_GRAPH"
        existence = "CERTIFIED_UNIQUE_OVER_FULL_P_S_BASE"
    elif face == "STRICT_ZERO_ABSENT":
        dimension = "EMPTY_ZERO_SET"
        existence = "CERTIFIED_ABSENT"
    else:
        dimension = "REGULAR_DIMENSION_2_ZERO_SET_IF_PRESENT"
        existence = "BASE_PROJECTION_AND_CLIPPING_DEFERRED"
    payload = [origin["row_id"], "outgoing_chart_seam"]
    return {
        "row_id": make_id("outgoing-normal-form", payload),
        "origin_row_id": origin["row_id"],
        "parent_id": origin["parent_id"],
        "chart": origin["chart"],
        "equation": "target_normal_x^2-target_normal_y^2=0",
        "gradient_axis": "t",
        "gradient_sign": derivative_sign,
        "regularity_certification": "CERTIFIED_STRICT_INTERVAL_DERIVATIVE",
        "lower_t_face_sign": sign(lower),
        "upper_t_face_sign": sign(upper),
        "face_classification": face,
        "zero_set_dimension_account": dimension,
        "existence_over_full_base": existence,
        "two_open_3d_sides_retained": True,
        "whole_origin_credit": 0,
        "global_geometric_disposition_credit": 0,
        "provenance": "ROUND179_256_BIT_INTERVAL_GRADIENT_AND_T_FACE_SIGNS",
    }


def subtract_wall(
    dual: tuple[Any, tuple[Any, ...]],
    wall: int,
) -> tuple[Any, tuple[Any, ...]]:
    return dual[0] - arb(wall), dual[1]


def wall_row(
    origin: dict[str, Any],
    owner: str,
    geometry: dict[str, Any],
    reason: str,
) -> dict[str, Any]:
    kind, axis, wall_text = reason.split(":")
    wall = int(wall_text)
    source_name = "source_x" if axis == "X" else "source_y"
    target_name = "hit_x" if axis == "X" else "hit_y"
    source = subtract_wall(geometry[source_name], wall)
    target = subtract_wall(geometry[target_name], wall)
    source_value_sign = sign(source[0])
    source_axes = strict_derivative_axes(source)
    if source_value_sign != "OVERWRAP":
        source_classification = "STRICT_NONZERO"
        source_axis = None
        source_gradient_sign = None
    else:
        require(source_axes, "source wall factor regular")
        source_classification = "REGULAR_GRAPH"
        source_axis = source_axes[0]
        source_gradient_sign = sign(
            source[1][("t", "p", "s").index(source_axis)]
        )
    target_value_sign = sign(target[0])
    target_axes = strict_derivative_axes(target)
    if target_value_sign != "OVERWRAP":
        target_classification = "STRICT_NONZERO"
        target_axis = None
        target_gradient_sign = None
        lower_sign = None
        upper_sign = None
        target_face = "STRICT_ZERO_ABSENT"
    else:
        require(target_axes, "target wall factor regular")
        target_classification = "REGULAR_GRAPH"
        target_axis = target_axes[0]
        target_gradient_sign = sign(
            target[1][("t", "p", "s").index(target_axis)]
        )
        box = box_from(
            origin["box"],
            len(origin["refinement_path"]),
            origin["row_id"],
        )
        lower_geometry = interval_geometry(
            origin["chart"],
            owner,
            fixed_axis_face(box, target_axis, False),
        )
        upper_geometry = interval_geometry(
            origin["chart"],
            owner,
            fixed_axis_face(box, target_axis, True),
        )
        lower = subtract_wall(lower_geometry[target_name], wall)[0]
        upper = subtract_wall(upper_geometry[target_name], wall)[0]
        lower_sign = sign(lower)
        upper_sign = sign(upper)
        target_face = face_classification(lower, upper)
    active_graph_factors = sum(
        classification == "REGULAR_GRAPH"
        for classification in (
            source_classification, target_classification
        )
    )
    dimension = (
        "EMPTY_ZERO_SET"
        if active_graph_factors == 0
        else "UNION_OF_CERTIFIED_REGULAR_DIMENSION_2_FACTORS"
    )
    crossing_discharged = (
        kind == "wall_crossing_time_not_strict"
        and source_classification == "STRICT_NONZERO"
        and target_classification == "STRICT_NONZERO"
    )
    payload = [origin["row_id"], reason]
    return {
        "row_id": make_id("wall-normal-form", payload),
        "origin_row_id": origin["row_id"],
        "parent_id": origin["parent_id"],
        "chart": origin["chart"],
        "reason_label": reason,
        "axis": axis,
        "integer_wall": wall,
        "zero_equation":
            f"(source_{axis.lower()}-{wall})*"
            f"(target_{axis.lower()}-{wall})=0",
        "source_factor_classification": source_classification,
        "source_gradient_axis": source_axis,
        "source_gradient_sign": source_gradient_sign,
        "target_factor_classification": target_classification,
        "target_gradient_axis": target_axis,
        "target_gradient_sign": target_gradient_sign,
        "target_lower_face_sign": lower_sign,
        "target_upper_face_sign": upper_sign,
        "target_face_classification": target_face,
        "zero_set_dimension_account": dimension,
        "crossing_time_dependency_overwrap_discharged":
            crossing_discharged,
        "whole_origin_credit": 0,
        "global_geometric_disposition_credit": 0,
        "provenance":
            "ROUND179_EXACT_ENDPOINT_FACTORIZATION_AND_256_BIT_GRADIENT",
    }


def source_seam_row(origin: dict[str, Any]) -> dict[str, Any]:
    box = box_from(
        origin["box"], len(origin["refinement_path"]), origin["row_id"]
    )
    lower = 2 * box.t0 * box.t0 - 1
    upper = 2 * box.t1 * box.t1 - 1
    lower_sign = (
        "STRICT_POSITIVE" if lower > 0 else "STRICT_NEGATIVE"
        if lower < 0 else "ZERO"
    )
    upper_sign = (
        "STRICT_POSITIVE" if upper > 0 else "STRICT_NEGATIVE"
        if upper < 0 else "ZERO"
    )
    require(
        {lower_sign, upper_sign}
        == {"STRICT_NEGATIVE", "STRICT_POSITIVE"}
        and (box.t0 > 0 or box.t1 < 0),
        "source seam unique graph",
    )
    gradient_sign = "STRICT_POSITIVE" if box.t0 > 0 else "STRICT_NEGATIVE"
    payload = [origin["row_id"], "source_chart_seam"]
    return {
        "row_id": make_id("source-seam-normal-form", payload),
        "origin_row_id": origin["row_id"],
        "parent_id": origin["parent_id"],
        "chart": origin["chart"],
        "equation": "2*t^2-1=0",
        "gradient_axis": "t",
        "gradient_sign": gradient_sign,
        "lower_t_face_sign": lower_sign,
        "upper_t_face_sign": upper_sign,
        "face_classification": "FULL_BASE_UNIQUE_GRAPH",
        "exact_dimension": 2,
        "half_open_owner_status": r174.seam_owner(origin["chart"]),
        "whole_origin_credit": 0,
        "global_geometric_disposition_credit": 0,
        "provenance": "ROUND179_EXACT_RATIONAL_FACE_SIGNS_AND_4T_DERIVATIVE",
    }


def arrangement_row(origin: dict[str, Any]) -> dict[str, Any]:
    require(len(origin["reason_labels"]) == 2, "pair arrangement input")
    reasons = sorted(origin["reason_labels"])
    payload = [origin["row_id"], "pair-arrangement", reasons]
    return {
        "row_id": make_id("pair-arrangement", payload),
        "origin_row_id": origin["row_id"],
        "parent_id": origin["parent_id"],
        "chart": origin["chart"],
        "reason_labels": reasons,
        "predicate_count": 2,
        "candidate_pair_intersection_dimension": 1,
        "candidate_boundary_corner_dimension": 0,
        "existence_certification": "NOT_CERTIFIED",
        "transversality_certification": "NOT_CERTIFIED",
        "isolation_certification": "NOT_CERTIFIED",
        "whole_origin_credit": 0,
        "global_geometric_disposition_credit": 0,
        "provenance":
            "ROUND179_NOMINAL_1D_INTERSECTION_AND_BOUNDARY_0D_CANDIDATE",
    }


def build_rows(inputs: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    parents, origins = unpack_round174_rows(inputs["r174a"])
    owner_by_parent = {
        row["parent_id"]: row["owner_target"] for row in parents
    }
    origin_summaries: list[dict[str, Any]] = []
    resolved: list[dict[str, Any]] = []
    retained: list[dict[str, Any]] = []
    guards: list[dict[str, Any]] = []
    outgoing: list[dict[str, Any]] = []
    walls: list[dict[str, Any]] = []
    source_seams: list[dict[str, Any]] = []
    arrangements: list[dict[str, Any]] = []
    cluster_counts: Counter[tuple[int, ...]] = Counter()
    for origin in origins:
        owner = owner_by_parent[origin["parent_id"]]
        step = one_step_origin(origin, owner, inputs["registry"])
        origin_summaries.append(step["summary"])
        resolved.extend(step["resolved"])
        retained.extend(step["retained"])
        guards.extend(step["guards"])
        if step["summary"]["fully_replaced_by_bounded_children"]:
            cluster_counts[tuple(step["ordinals"])] += 1
        reasons = origin["reason_labels"]
        need_geometry = any(
            reason == "outgoing_chart_seam"
            or reason.startswith("wall_")
            for reason in reasons
        )
        geometry = None
        if need_geometry:
            box = box_from(
                origin["box"],
                len(origin["refinement_path"]),
                origin["row_id"],
            )
            geometry = interval_geometry(
                origin["chart"], owner, box
            )
        if "outgoing_chart_seam" in reasons:
            assert geometry is not None
            outgoing.append(outgoing_row(
                origin, owner, geometry
            ))
        for reason in reasons:
            if reason.startswith("wall_"):
                assert geometry is not None
                walls.append(wall_row(
                    origin, owner, geometry, reason
                ))
        if "source_chart_seam" in reasons:
            source_seams.append(source_seam_row(origin))
        if len(reasons) == 2:
            arrangements.append(arrangement_row(origin))
        require(len(reasons) in {1, 2}, "origin reason arity")
    key_clusters = []
    for ordinals, count in sorted(cluster_counts.items()):
        payload = [list(ordinals), count]
        key_clusters.append({
            "cluster_id": make_id("closed-key-cluster", payload),
            "released_exact_key_ordinals": list(ordinals),
            "released_exact_key_ordinals_sha256": digest(list(ordinals)),
            "fully_replaced_origin_count": count,
            "global_geometric_disposition_credit": 0,
        })
    origin_summaries.sort(key=lambda row: row["origin_row_id"])
    resolved.sort(key=lambda row: row["row_id"])
    retained.sort(key=lambda row: row["row_id"])
    guards.sort(key=lambda row: row["row_id"])
    outgoing.sort(key=lambda row: row["row_id"])
    walls.sort(key=lambda row: row["row_id"])
    source_seams.sort(key=lambda row: row["row_id"])
    arrangements.sort(key=lambda row: row["row_id"])
    key_clusters.sort(key=lambda row: row["cluster_id"])
    require(
        len(origin_summaries) == 62012
        and len({row["origin_row_id"] for row in origin_summaries}) == 62012
        and len({row["row_id"] for row in resolved}) == len(resolved)
        and len({row["row_id"] for row in retained}) == len(retained)
        and len({row["row_id"] for row in guards}) == len(guards)
        and len({row["row_id"] for row in outgoing}) == len(outgoing)
        and len({row["row_id"] for row in walls}) == len(walls)
        and len({row["row_id"] for row in source_seams})
        == len(source_seams)
        and len({row["row_id"] for row in arrangements})
        == len(arrangements),
        "Round179 row ID census",
    )
    return {
        "origins": origin_summaries,
        "resolved": resolved,
        "retained": retained,
        "guards": guards,
        "outgoing": outgoing,
        "walls": walls,
        "source_seams": source_seams,
        "arrangements": arrangements,
        "key_clusters": key_clusters,
    }


def table_statistics(
    rows: dict[str, list[dict[str, Any]]],
) -> dict[str, Any]:
    origins = rows["origins"]
    resolved = rows["resolved"]
    retained = rows["retained"]
    guards = rows["guards"]
    outgoing = rows["outgoing"]
    walls = rows["walls"]
    source_seams = rows["source_seams"]
    arrangements = rows["arrangements"]
    original_volume = sum(
        (Q(row["original_coordinate_volume"]) for row in origins), Q(0)
    )
    resolved_volume = sum(
        (Q(row["coordinate_volume"]) for row in resolved), Q(0)
    )
    retained_volume = sum(
        (Q(row["coordinate_volume"]) for row in retained), Q(0)
    )
    guard_volume = sum(
        (Q(row["coordinate_volume"]) for row in guards), Q(0)
    )
    require(
        resolved_volume + retained_volume + guard_volume == original_volume,
        "global one-step volume conservation",
    )
    fully_replaced = [
        row for row in origins
        if row["fully_replaced_by_bounded_children"]
    ]
    partial = [
        row for row in origins
        if not row["fully_replaced_by_bounded_children"]
    ]
    observed_ordinals = sorted({
        row["official_key_ordinal"] for row in resolved
    })
    closed_parent_union = {
        row["parent_id"] for row in fully_replaced
    }
    partial_parent_union = {
        row["parent_id"] for row in partial
    }
    closure_by_reason = Counter(
        tuple(row["original_reason_labels"]) for row in fully_replaced
    )
    partial_by_reason = Counter(
        tuple(row["original_reason_labels"]) for row in partial
    )
    reason_histogram = Counter(
        reason
        for row in origins
        for reason in row["original_reason_labels"]
    )
    outgoing_faces = Counter(
        row["face_classification"] for row in outgoing
    )
    wall_source = Counter(
        row["source_factor_classification"] for row in walls
    )
    wall_target = Counter(
        row["target_factor_classification"] for row in walls
    )
    wall_target_faces = Counter(
        row["target_face_classification"] for row in walls
    )
    retained_reason_histogram = Counter(
        reason
        for row in retained
        for reason in row["reason_labels"]
    )
    zero_reasons = {
        reason: reason_histogram.get(reason, 0)
        for reason in (
            "target_grazing_or_discriminant",
            "selected_root_sign_or_owner",
            "return_time_not_below_three",
            "simultaneous_corner_order",
            "outgoing_chart_component_sign",
            "wall_endpoint_audit_range:X",
            "wall_endpoint_audit_range:Y",
            "more_than_four_crossings:X",
            "more_than_four_crossings:Y",
        )
    }
    require(all(value == 0 for value in zero_reasons.values()), "zero reasons")
    statistics = {
        "Round174_origin_residual_tube_count": len(origins),
        "Round174_origin_partial_parent_count": len({
            row["parent_id"] for row in origins
        }),
        "Round174_origin_coordinate_volume": qstr(original_volume),
        "original_reason_occurrence_histogram": dict(sorted(
            reason_histogram.items()
        )),
        "original_reason_combo_count": len({
            tuple(row["original_reason_labels"]) for row in origins
        }),
        "original_single_reason_tube_count": sum(
            row["reason_count"] == 1 for row in origins
        ),
        "original_two_reason_tube_count": sum(
            row["reason_count"] == 2 for row in origins
        ),
        "one_step_fully_replaced_origin_tube_count": len(fully_replaced),
        "one_step_still_partial_origin_tube_count": len(partial),
        "one_step_closed_parent_union_count": len(closed_parent_union),
        "one_step_partial_parent_union_count": len(partial_parent_union),
        "one_step_resolved_child_count": len(resolved),
        "one_step_guard_child_count": len(guards),
        "one_step_retained_positive_3d_child_count": len(retained),
        "one_step_resolved_coordinate_volume": qstr(resolved_volume),
        "one_step_guard_coordinate_volume": qstr(guard_volume),
        "one_step_retained_coordinate_volume": qstr(retained_volume),
        "one_step_volume_conservation_exact": True,
        "released_local_exact_key_count": len(observed_ordinals),
        "released_local_exact_key_ordinals_sha256": digest(observed_ordinals),
        "fully_replaced_origin_key_cluster_count":
            len(rows["key_clusters"]),
        "fully_replaced_by_reason": [
            {"reason_labels": list(reason), "origin_count": count}
            for reason, count in sorted(closure_by_reason.items())
        ],
        "still_partial_by_reason": [
            {"reason_labels": list(reason), "origin_count": count}
            for reason, count in sorted(partial_by_reason.items())
        ],
        "retained_reason_occurrence_histogram": dict(sorted(
            retained_reason_histogram.items()
        )),
        "outgoing_predicate_row_count": len(outgoing),
        "outgoing_strict_t_derivative_count": sum(
            row["gradient_axis"] == "t"
            and row["gradient_sign"]
            in {"STRICT_NEGATIVE", "STRICT_POSITIVE"}
            for row in outgoing
        ),
        "outgoing_face_classification_histogram": dict(sorted(
            outgoing_faces.items()
        )),
        "wall_predicate_row_count": len(walls),
        "wall_source_factor_classification_histogram": dict(sorted(
            wall_source.items()
        )),
        "wall_target_factor_classification_histogram": dict(sorted(
            wall_target.items()
        )),
        "wall_target_face_classification_histogram": dict(sorted(
            wall_target_faces.items()
        )),
        "wall_crossing_time_dependency_overwrap_discharged_count": sum(
            row["crossing_time_dependency_overwrap_discharged"]
            for row in walls
        ),
        "source_chart_seam_full_base_graph_count": len(source_seams),
        "two_predicate_arrangement_candidate_count": len(arrangements),
        "candidate_nominal_1D_intersection_row_count": len(arrangements),
        "candidate_boundary_0D_corner_row_count": len(arrangements),
        "certified_actual_pair_intersection_count": 0,
        "certified_actual_boundary_corner_count": 0,
        "zero_failure_reason_census": zero_reasons,
        "global_geometric_exact_key_disposition_count_before_Round179": 0,
        "global_geometric_exact_key_disposition_count_after_Round179": 0,
        "keys_without_global_geometric_disposition_after_Round179":
            SOURCE_G_KEY_COUNT,
    }
    require(
        statistics["Round174_origin_partial_parent_count"] == 3840
        and statistics["original_reason_combo_count"] == 28
        and statistics["original_single_reason_tube_count"] == 61676
        and statistics["original_two_reason_tube_count"] == 336
        and len(fully_replaced) == 4116
        and len(partial) == 57896
        and len(resolved) == 17192
        and len(guards) == 152
        and len(retained) == 106680
        and qstr(resolved_volume) == "257889/524288000"
        and qstr(guard_volume) == "1239/409600000"
        and qstr(retained_volume) == "1768407/524288000"
        and len(observed_ordinals) == 116
        and len(rows["key_clusters"]) == 96
        and len(closed_parent_union) == 1768
        and len(partial_parent_union) == 3744
        and len(outgoing) == 34188
        and outgoing_faces
        == {
            "FACE_OVERWRAP_REGULAR_ZERO_SET_IF_PRESENT": 30444,
            "FULL_BASE_UNIQUE_GRAPH": 344,
            "STRICT_ZERO_ABSENT": 3400,
        }
        and len(walls) == 27688
        and wall_source == {"REGULAR_GRAPH": 1056, "STRICT_NONZERO": 26632}
        and wall_target == {"REGULAR_GRAPH": 26344, "STRICT_NONZERO": 1344}
        and wall_target_faces
        == {
            "FACE_OVERWRAP_REGULAR_ZERO_SET_IF_PRESENT": 23776,
            "FULL_BASE_UNIQUE_GRAPH": 320,
            "STRICT_ZERO_ABSENT": 3592,
        }
        and statistics[
            "wall_crossing_time_dependency_overwrap_discharged_count"
        ] == 480
        and len(source_seams) == 472
        and len(arrangements) == 336,
        "Round179 headline census",
    )
    return statistics


def pack_attachment(
    rows: dict[str, list[dict[str, Any]]],
) -> dict[str, Any]:
    packed = {
        "origin_tube_rows": [
            pack_row(ORIGIN_COLUMNS, row) for row in rows["origins"]
        ],
        "resolved_3d_child_rows": [
            pack_row(RESOLVED_COLUMNS, row) for row in rows["resolved"]
        ],
        "retained_3d_child_rows": [
            pack_row(RETAINED_COLUMNS, row) for row in rows["retained"]
        ],
        "chart_guard_child_rows": [
            pack_row(GUARD_COLUMNS, row) for row in rows["guards"]
        ],
        "outgoing_normal_form_rows": [
            pack_row(OUTGOING_COLUMNS, row) for row in rows["outgoing"]
        ],
        "wall_normal_form_rows": [
            pack_row(WALL_COLUMNS, row) for row in rows["walls"]
        ],
        "source_chart_seam_rows": [
            pack_row(SOURCE_SEAM_COLUMNS, row)
            for row in rows["source_seams"]
        ],
        "pair_arrangement_candidate_rows": [
            pack_row(ARRANGEMENT_COLUMNS, row)
            for row in rows["arrangements"]
        ],
        "fully_replaced_key_cluster_rows": [
            pack_row(KEY_CLUSTER_COLUMNS, row)
            for row in rows["key_clusters"]
        ],
    }
    result = {
        "row_column_schemas": {
            "origin_tube_rows": ORIGIN_COLUMNS,
            "resolved_3d_child_rows": RESOLVED_COLUMNS,
            "retained_3d_child_rows": RETAINED_COLUMNS,
            "chart_guard_child_rows": GUARD_COLUMNS,
            "outgoing_normal_form_rows": OUTGOING_COLUMNS,
            "wall_normal_form_rows": WALL_COLUMNS,
            "source_chart_seam_rows": SOURCE_SEAM_COLUMNS,
            "pair_arrangement_candidate_rows": ARRANGEMENT_COLUMNS,
            "fully_replaced_key_cluster_rows": KEY_CLUSTER_COLUMNS,
        },
        **packed,
        "table_census_and_sha256": {
            name: {
                "row_count": len(table),
                "rows_sha256": digest(table),
            }
            for name, table in packed.items()
        },
    }
    return {
        "schema": ATTACHMENT_SCHEMA,
        "result": result,
        "result_sha256": digest(result),
    }


def build_certificate_result(
    inputs: dict[str, Any],
    statistics: dict[str, Any],
    attachment: dict[str, Any],
    attachment_sha256: str,
) -> dict[str, Any]:
    return {
        "status": STATUS,
        "scope": {
            "source_obstacle": "G",
            "input_kind": "all Round174 retained positive-volume 3D tubes",
            "input_residual_tube_count": 62012,
            "input_partial_parent_count": 3840,
            "bounded_operation":
                "one adaptive dyadic split plus interval-gradient normal forms",
            "all_input_tubes_processed": True,
            "formal_verdict": "PARTIAL",
            "global_geometric_exact_key_dispositions_added": 0,
            "CM2_exterior_sheet_exclusions_added": 0,
        },
        "provenance": {
            "dependency_sha256": PINS,
            "python_flint_version": FLINT_VERSION,
            "interval_precision_bits": PRECISION_BITS,
            "Round171_result_sha256": R171_RESULT,
            "Round171_verification_result_sha256": R171_VERIFY_RESULT,
            "Round173_result_sha256": R173_RESULT,
            "Round173_verification_result_sha256": R173_VERIFY_RESULT,
            "Round174_result_sha256": R174_RESULT,
            "Round174_attachment_result_sha256": R174_ATTACHMENT_RESULT,
            "Round174_verification_result_sha256": R174_VERIFY_RESULT,
            "Round174_verified_evaluator_reused_by_producer": True,
            "throwaway_spike_imported": False,
            "old_artifacts_modified": False,
        },
        "failure_taxonomy": {
            "original_reason_combo_count":
                statistics["original_reason_combo_count"],
            "original_single_reason_tube_count":
                statistics["original_single_reason_tube_count"],
            "original_two_reason_tube_count":
                statistics["original_two_reason_tube_count"],
            "original_reason_occurrence_histogram":
                statistics["original_reason_occurrence_histogram"],
            "zero_failure_reason_census":
                statistics["zero_failure_reason_census"],
            "selected_root_grazing_equality_order_failures_present": False,
            "simultaneous_corner_order_failure_present": False,
        },
        "bounded_one_step_census": {
            key: statistics[key]
            for key in (
                "Round174_origin_residual_tube_count",
                "Round174_origin_partial_parent_count",
                "Round174_origin_coordinate_volume",
                "one_step_fully_replaced_origin_tube_count",
                "one_step_still_partial_origin_tube_count",
                "one_step_closed_parent_union_count",
                "one_step_partial_parent_union_count",
                "one_step_resolved_child_count",
                "one_step_guard_child_count",
                "one_step_retained_positive_3d_child_count",
                "one_step_resolved_coordinate_volume",
                "one_step_guard_coordinate_volume",
                "one_step_retained_coordinate_volume",
                "one_step_volume_conservation_exact",
                "released_local_exact_key_count",
                "released_local_exact_key_ordinals_sha256",
                "fully_replaced_origin_key_cluster_count",
                "fully_replaced_by_reason",
                "still_partial_by_reason",
                "retained_reason_occurrence_histogram",
            )
        },
        "outgoing_chart_normal_forms": {
            "predicate_row_count":
                statistics["outgoing_predicate_row_count"],
            "strict_t_derivative_count":
                statistics["outgoing_strict_t_derivative_count"],
            "equation": "target_normal_x^2-target_normal_y^2=0",
            "face_classification_histogram":
                statistics["outgoing_face_classification_histogram"],
            "full_base_unique_graph_requires_opposite_strict_face_signs":
                True,
            "strict_zero_absence_requires_same_strict_face_sign": True,
            "derivative_sign_alone_never_promoted_to_full_base_existence":
                True,
            "face_overwrap_rows_remain_partial": True,
        },
        "integer_wall_normal_forms": {
            "predicate_row_count":
                statistics["wall_predicate_row_count"],
            "exact_factorization":
                "(source_axis-wall)*(target_axis-wall)=0",
            "source_factor_classification_histogram":
                statistics[
                    "wall_source_factor_classification_histogram"
                ],
            "target_factor_classification_histogram":
                statistics[
                    "wall_target_factor_classification_histogram"
                ],
            "target_face_classification_histogram":
                statistics[
                    "wall_target_face_classification_histogram"
                ],
            "crossing_time_dependency_overwrap_discharged_count":
                statistics[
                    "wall_crossing_time_dependency_overwrap_discharged_count"
                ],
            "all_overwrapped_source_or_target_factors_have_a_strict_gradient":
                True,
            "face_overwrap_factor_rows_remain_partial": True,
        },
        "source_chart_and_pair_arrangement": {
            "source_chart_equation": "2*t^2-1=0",
            "source_chart_full_base_unique_graph_count":
                statistics["source_chart_seam_full_base_graph_count"],
            "source_chart_graph_exact_dimension": 2,
            "two_predicate_arrangement_candidate_count":
                statistics[
                    "two_predicate_arrangement_candidate_count"
                ],
            "nominal_1D_candidate_intersection_row_count":
                statistics[
                    "candidate_nominal_1D_intersection_row_count"
                ],
            "boundary_0D_candidate_corner_row_count":
                statistics[
                    "candidate_boundary_0D_corner_row_count"
                ],
            "certified_actual_pair_intersection_count":
                statistics["certified_actual_pair_intersection_count"],
            "certified_actual_boundary_corner_count":
                statistics["certified_actual_boundary_corner_count"],
            "candidate_existence_transversality_and_isolation_deferred": True,
        },
        "dimension_safe_ledger": {
            "resolved_and_retained_child_ambient_dimension": 3,
            "outgoing_and_wall_regular_zero_set_dimension_if_present": 2,
            "pair_intersection_nominal_dimension_if_transverse": 1,
            "boundary_corner_candidate_dimension": 0,
            "lower_dimensional_three_dimensional_volume_credit": 0,
            "lower_dimensional_whole_origin_credit": 0,
            "retained_positive_volume_child_whole_origin_credit": 0,
            "chart_guard_is_not_CM2_exterior_sheet_exclusion": True,
            "chart_guard_is_not_Gate5_geometric_disposition": True,
            "local_occurrence_is_not_global_geometric_disposition": True,
            "fully_replaced_original_tube_count_is_not_a_global_key_credit":
                True,
        },
        "observed_occurrence_vs_global_disposition": {
            "released_local_exact_key_count":
                statistics["released_local_exact_key_count"],
            "global_geometric_exact_key_disposition_count_before_Round179": 0,
            "global_geometric_exact_key_disposition_count_after_Round179": 0,
            "keys_without_global_geometric_disposition_after_Round179":
                SOURCE_G_KEY_COUNT,
            "reason":
                "child occurrences and bounded tube replacements do not "
                "connect or exclude every fibre of any global exact key",
        },
        "row_attachment": {
            "path": ATTACHMENT.name,
            "schema": ATTACHMENT_SCHEMA,
            "file_sha256": attachment_sha256,
            "result_sha256": attachment["result_sha256"],
            "table_census_and_sha256":
                attachment["result"]["table_census_and_sha256"],
            "full_rows_materialized": True,
        },
        "strict_nonpromotion": {
            "all_62012_Round174_residual_tubes_closed": False,
            "remaining_original_tube_count": 57896,
            "remaining_positive_volume_child_count": 106680,
            "all_pair_intersections_isolated": False,
            "source_G_global_exact_key_dispositions_complete": False,
            "D02": "BLOCKED",
            "D03_negative_oracle": "UNAUTHORIZED",
            "global_Gate5_fields": "10/18",
            "global_complete_18_field_blocks": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "next_core_gate":
            "adaptively clip the 30444 outgoing and 23776 wall "
            "face-overwrap regular graph collars, isolate the 336 pair "
            "arrangements with interval Newton and boundary charts, and "
            "retain every unisolated positive-volume or lower-dimensional "
            "piece with zero global exact-key disposition credit",
    }


def safe_output(path: Path, protected: set[Path]) -> None:
    require(path.parent.exists() and path.parent.is_dir(), "output parent")
    require(not path.parent.is_symlink(), "output parent symlink")
    candidate = path.resolve(strict=False)
    require(candidate not in protected, "output aliases protected")
    if path.exists() or path.is_symlink():
        require(not path.is_symlink(), "output symlink")
        info = path.stat()
        require(stat.S_ISREG(info.st_mode), "output regular")
        require(info.st_nlink == 1, "output hardlink")
        require(
            all(not os.path.samefile(path, protected_path)
                for protected_path in protected),
            "output samefile protected",
        )


def build_all() -> tuple[dict[str, Any], dict[str, Any], bytes]:
    inputs = load_inputs()
    ctx.prec = PRECISION_BITS
    rows = build_rows(inputs)
    statistics = table_statistics(rows)
    attachment = pack_attachment(rows)
    attachment_bytes = (
        canonical(attachment) + "\n"
    ).encode("utf-8")
    attachment_sha256 = hashlib.sha256(attachment_bytes).hexdigest()
    result = build_certificate_result(
        inputs, statistics, attachment, attachment_sha256
    )
    certificate = {
        "schema": SCHEMA,
        "result": result,
        "result_sha256": digest(result),
    }
    return certificate, attachment, attachment_bytes


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument("--attachment-output", type=Path, default=ATTACHMENT)
    arguments = parser.parse_args()
    protected = {
        Path(__file__).resolve(),
        *[(HERE / name).resolve() for name in PINS],
    }
    safe_output(arguments.output, {
        *protected, arguments.attachment_output.resolve(strict=False)
    })
    safe_output(arguments.attachment_output, {
        *protected, arguments.output.resolve(strict=False)
    })
    require(
        arguments.output.resolve(strict=False)
        != arguments.attachment_output.resolve(strict=False),
        "certificate/attachment distinct",
    )
    certificate, _attachment, attachment_bytes = build_all()
    arguments.attachment_output.write_bytes(attachment_bytes)
    arguments.output.write_text(
        json.dumps(
            certificate,
            sort_keys=True,
            indent=2,
            ensure_ascii=False,
            allow_nan=False,
        ) + "\n",
        encoding="utf-8",
    )
    census = certificate["result"]["bounded_one_step_census"]
    print(
        "origins",
        census["one_step_fully_replaced_origin_tube_count"],
        "fully replaced +",
        census["one_step_still_partial_origin_tube_count"],
        "partial",
    )
    print(
        "children",
        census["one_step_resolved_child_count"],
        census["one_step_guard_child_count"],
        census["one_step_retained_positive_3d_child_count"],
    )
    print(certificate["result_sha256"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
