#!/usr/bin/env python3
"""Independent verifier for Round179 source-G residual arrangements.

The Round179 producer is pinned as inert bytes and is never imported or
executed.  The verifier starts from the independently verified Round174 row
attachment, redoes every one-step split, reconstructs every child and normal
form, checks all nine Round179 tables row for row, and re-audits the complete
certificate and no-promotion state.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import stat
import tempfile
from collections import Counter, defaultdict
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from flint import arb, ctx, __version__ as FLINT_VERSION

import cm2_round174_source_g_unique_first_dynamic_occurrence_materialization_verifier as r174


BASE = Path(__file__).resolve().parent
PRODUCER = BASE / "cm2_round179_source_g_residual_tube_arrangement.py"
CERTIFICATE = BASE / (
    "cm2_round179_source_g_residual_tube_arrangement_certificate.json"
)
ATTACHMENT = BASE / "cm2_round179_source_g_residual_tube_arrangement_rows.json"
OUTPUT = BASE / "cm2_round179_source_g_residual_tube_arrangement_verification.json"
SCHEMA = "cm2.round179.source-g-residual-tube-arrangement.v1"
ATTACHMENT_SCHEMA = "cm2.round179.source-g-residual-tube-arrangement-rows.v1"
VERIFICATION_SCHEMA = (
    "cm2.round179.source-g-residual-tube-arrangement.verification.v1"
)
CERTIFIED_STATUS = (
    "CERTIFIED_BOUNDED_PARTIAL_SOURCE_G_RESIDUAL_TUBE_ARRANGEMENT__"
    "NO_GLOBAL_DISPOSITION_OR_D02_PROMOTION"
)
EXPECTED_PRODUCER_SHA256 = (
    "8c568c58d82708a7ab549f126c1fcedfccff563d1d00e3c1f7e6545b4b0d29ab"
)
EXPECTED_CERTIFICATE_SHA256 = (
    "edc2c538dc04a93c2b873f53e07b5c97c6b395a1d107e7ed2de4cf2c4bd35111"
)
EXPECTED_ATTACHMENT_SHA256 = (
    "f20b42c1fed781779b537b4d45bf44233eae1ed3ee620b95177a80f0eb2b5e42"
)
EXPECTED_CERTIFICATE_RESULT = (
    "0f57284c11c617349fe66877552c401f426efafbc75faa08948f099166e9cde3"
)
EXPECTED_ATTACHMENT_RESULT = (
    "a5468800c1d89cd307a5a26c608550b04db79c64c562fb12bedb22d6cec308cb"
)
PRECISION_BITS = 256

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


def input_bytes(path: Path, maximum: int) -> bytes:
    require(path.parent == BASE, f"path parent:{path.name}")
    require(path.exists() and not path.is_symlink(), f"path exists:{path.name}")
    info = path.stat()
    require(stat.S_ISREG(info.st_mode), f"path regular:{path.name}")
    require(info.st_nlink == 1, f"path hardlink:{path.name}")
    require(0 < info.st_size <= maximum, f"path size:{path.name}")
    return path.read_bytes()


def strict_decode(raw: bytes) -> dict[str, Any]:
    require(
        raw and len(raw) <= 180_000_000
        and not raw.startswith(b"\xef\xbb\xbf")
        and b"\x00" not in raw,
        "strict JSON bytes",
    )

    def unique(pairs):
        result = {}
        for key, value in pairs:
            require(key not in result, f"duplicate key:{key}")
            result[key] = value
        return result

    def reject(token):
        raise ValueError(token)

    result = json.loads(
        raw.decode(),
        object_pairs_hook=unique,
        parse_constant=reject,
        parse_float=reject,
    )
    def walk(value):
        if type(value) is str:
            require(
                "\x00" not in value
                and not any(
                    0xD800 <= ord(character) <= 0xDFFF
                    for character in value
                ),
                "decoded string",
            )
        elif type(value) is list:
            for item in value:
                walk(item)
        elif type(value) is dict:
            for key, item in value.items():
                walk(key)
                walk(item)
    walk(result)
    require(type(result) is dict, "top object")
    return result


def strict_load(path: Path, maximum: int) -> dict[str, Any]:
    return strict_decode(input_bytes(path, maximum))


def make_id(prefix: str, payload: Any) -> str:
    return f"round179-{prefix}:{digest(payload)}"


def unpack(table: list[list[Any]], columns: list[str]) -> list[dict[str, Any]]:
    return [dict(zip(columns, row, strict=True)) for row in table]


def load_sources() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    require(FLINT_VERSION == "0.9.0", "python-flint version")
    producer_raw = input_bytes(PRODUCER, 200_000)
    require(
        hashlib.sha256(producer_raw).hexdigest() == EXPECTED_PRODUCER_SHA256,
        "inert producer pin",
    )
    del producer_raw
    for name, expected in PINS.items():
        require(
            hashlib.sha256(input_bytes(BASE / name, 180_000_000)).hexdigest()
            == expected,
            f"pin:{name}",
        )
    r174c = strict_load(BASE / R174C, 2_000_000)
    r174v = strict_load(BASE / R174O, 2_000_000)
    r174a = strict_load(BASE / R174A, 180_000_000)
    require(
        r174c["result_sha256"]
        == "d45f05458c42189cf0ebc51e258356d13278ba40845cce80b6a072ffbc8cf09b"
        == digest(r174c["result"])
        and r174v["result_sha256"]
        == "6c82800d41e456aeed7000bccb13bfe0e5e6d5f1637ac52a4d5c45b24ed9a23b"
        == digest(r174v["result"])
        and r174v["result"]["status"] == "PASS"
        and r174v["result"]["full_attachment_byte_for_byte_matched"] is True
        and r174v["result"]["producer_imported_or_executed"] is False
        and r174a["result_sha256"]
        == "002ca6631edd39c2325c63a1e8f9717d111f4d10c6d2585077d665a0ff128d18"
        == digest(r174a["result"]),
        "Round174 bindings",
    )
    gate5 = strict_load(BASE / G5M, 5_000_000)
    registry = r174.rebuild_registry(gate5)
    return r174c["result"], r174a["result"], registry


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


def box_from(values: list[str], depth: int, path: str):
    return r174.atlas.AtlasBox(*map(Q, values), depth, path)


def arb_sign(value: arb) -> str:
    if bool(value > 0):
        return "STRICT_POSITIVE"
    if bool(value < 0):
        return "STRICT_NEGATIVE"
    return "OVERWRAP"


def expected_resolved(
    origin, owner, child_index, axis_name, child, signature
):
    path = [*origin["refinement_path"], f"{axis_name}{child_index}"]
    payload = [
        origin["row_id"], child_index, path, r174.box_values(child),
        signature["key"]["identifier"], signature["outgoing"],
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


def expected_guard(origin, child_index, axis_name, child):
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


def expected_retained(origin, child_index, axis_name, child, reasons):
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


def independently_split_origin(origin, owner, registry):
    box = box_from(
        origin["box"], len(origin["refinement_path"]), origin["row_id"]
    )
    axes = (0,) if "source_chart_seam" in origin["reason_labels"] else (0, 1, 2)
    widths = (
        box.t1 - box.t0, box.p1 - box.p0, box.s1 - box.s0
    )
    choices = []
    for axis in axes:
        children = r174.bisect(box, axis)
        evaluations = [
            r174.classify_child(origin["chart"], child, owner, registry)
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
        choices.append((
            released, widths[axis] / widths[axis], -axis,
            axis, children, evaluations,
        ))
    _released, _width, _tie, axis, children, evaluations = max(
        choices, key=lambda choice: choice[:3]
    )
    axis_name = "tps"[axis]
    resolved = []
    retained = []
    guards = []
    for index, (child, evaluation) in enumerate(
        zip(children, evaluations, strict=True)
    ):
        kind, data = evaluation
        if kind == "resolved":
            resolved.append(expected_resolved(
                origin, owner, index, axis_name, child, data
            ))
        elif kind == "guard":
            guards.append(expected_guard(
                origin, index, axis_name, child
            ))
        else:
            retained.append(expected_retained(
                origin, index, axis_name, child, data
            ))
    rv = sum((Q(row["coordinate_volume"]) for row in resolved), Q(0))
    gv = sum((Q(row["coordinate_volume"]) for row in guards), Q(0))
    tv = sum((Q(row["coordinate_volume"]) for row in retained), Q(0))
    require(rv + gv + tv == Q(origin["coordinate_volume"]), "origin volume")
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
        "original_reason_labels": origin["reason_labels"],
        "reason_count": len(origin["reason_labels"]),
        "chosen_split_axis": axis_name,
        "resolved_child_count": len(resolved),
        "resolved_child_coordinate_volume": qstr(rv),
        "guard_child_count": len(guards),
        "guard_child_coordinate_volume": qstr(gv),
        "retained_child_count": len(retained),
        "retained_child_coordinate_volume": qstr(tv),
        "fully_replaced_by_bounded_children": not retained,
        "released_exact_key_count": len(ordinals),
        "released_exact_key_ordinals_sha256": digest(ordinals),
        "provenance": "ROUND174_RESIDUAL_PLUS_ONE_ADAPTIVE_DYADIC_SPLIT",
    }
    return summary, resolved, retained, guards, ordinals


def dadd(a, b):
    return (
        a[0] + b[0],
        tuple(
            None if x is None or y is None else x + y
            for x, y in zip(a[1], b[1], strict=True)
        ),
    )


def dneg(a):
    return -a[0], tuple(None if x is None else -x for x in a[1])


def dsub(a, b):
    return dadd(a, dneg(b))


def dmul(a, b):
    return (
        a[0] * b[0],
        tuple(
            None if x is None or y is None else x * b[0] + a[0] * y
            for x, y in zip(a[1], b[1], strict=True)
        ),
    )


def dscale(a, factor):
    return (
        a[0] * factor,
        tuple(None if x is None else x * factor for x in a[1]),
    )


def dconstant(value):
    return value, (arb(0), arb(0), arb(0))


def independent_geometry(chart, target_id, box):
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
    rt_value = r174.atlas.ge.sqrt_one_minus_square(box.t0, box.t1)
    rp_value = r174.atlas.ge.sqrt_one_minus_square(box.p0, box.p1)
    rt = (rt_value, (-t[0] / rt_value, arb(0), arb(0)))
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
        nx, ny = rt, t
    elif cell == "W":
        nx, ny = dneg(rt), t
    elif cell == "N":
        nx, ny = t, rt
    else:
        nx, ny = t, dneg(rt)
    ux = dsub(dmul(rp, nx), dmul(p, ny))
    uy = dadd(dmul(rp, ny), dmul(p, nx))
    source_x = dscale(nx, arb(9) / 25)
    source_y = dscale(ny, arb(9) / 25)
    target = r174.first_hit.target_by_id(target_id)
    if target.obstacle == "G":
        cx = dconstant(arb(target.ix))
        cy = dconstant(arb(target.iy))
    else:
        cx = dadd(dconstant(arb(target.ix) + arb(1) / 2), s)
        cy = dconstant(arb(target.iy) + arb(1) / 2)
    dx = dsub(cx, source_x)
    dy = dsub(cy, source_y)
    transverse = dadd(dneg(dmul(uy, dx)), dmul(ux, dy))
    radius_q = r174.first_hit.RADIUS[target.obstacle]
    radius = arb(radius_q.numerator) / radius_q.denominator
    discriminant = dsub(
        dconstant(radius * radius), dmul(transverse, transverse)
    )
    require(bool(discriminant[0] > 0), "strict discriminant")
    radical_value = discriminant[0].sqrt()
    radical = (
        radical_value,
        tuple(
            None if derivative is None
            else derivative / (2 * radical_value)
            for derivative in discriminant[1]
        ),
    )
    out_x = dscale(
        dadd(dneg(dmul(radical, ux)), dmul(transverse, uy)),
        1 / radius,
    )
    out_y = dscale(
        dsub(dneg(dmul(radical, uy)), dmul(transverse, ux)),
        1 / radius,
    )
    return {
        "source_x": source_x,
        "source_y": source_y,
        "hit_x": dadd(cx, dscale(out_x, radius)),
        "hit_y": dadd(cy, dscale(out_y, radius)),
        "outgoing_equality": dsub(dmul(out_x, out_x), dmul(out_y, out_y)),
    }


def strict_axes(dual):
    return tuple(
        axis
        for axis, derivative in zip("tps", dual[1], strict=True)
        if derivative is not None and arb_sign(derivative) != "OVERWRAP"
    )


def face_box(box, axis, upper):
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


def face_kind(lower, upper):
    signs = {arb_sign(lower), arb_sign(upper)}
    if signs == {"STRICT_NEGATIVE", "STRICT_POSITIVE"}:
        return "FULL_BASE_UNIQUE_GRAPH"
    if len(signs) == 1 and "OVERWRAP" not in signs:
        return "STRICT_ZERO_ABSENT"
    return "FACE_OVERWRAP_REGULAR_ZERO_SET_IF_PRESENT"


def expected_outgoing(origin, owner, geometry):
    equality = geometry["outgoing_equality"]
    axes = strict_axes(equality)
    require(
        arb_sign(equality[0]) == "OVERWRAP"
        and axes and axes[0] == "t",
        "outgoing regular t graph",
    )
    box = box_from(
        origin["box"], len(origin["refinement_path"]), origin["row_id"]
    )
    low = independent_geometry(
        origin["chart"], owner, face_box(box, "t", False)
    )["outgoing_equality"][0]
    high = independent_geometry(
        origin["chart"], owner, face_box(box, "t", True)
    )["outgoing_equality"][0]
    classification = face_kind(low, high)
    if classification == "FULL_BASE_UNIQUE_GRAPH":
        dimension = "EXACT_REGULAR_DIMENSION_2_GRAPH"
        existence = "CERTIFIED_UNIQUE_OVER_FULL_P_S_BASE"
    elif classification == "STRICT_ZERO_ABSENT":
        dimension = "EMPTY_ZERO_SET"
        existence = "CERTIFIED_ABSENT"
    else:
        dimension = "REGULAR_DIMENSION_2_ZERO_SET_IF_PRESENT"
        existence = "BASE_PROJECTION_AND_CLIPPING_DEFERRED"
    return {
        "row_id": make_id(
            "outgoing-normal-form",
            [origin["row_id"], "outgoing_chart_seam"],
        ),
        "origin_row_id": origin["row_id"],
        "parent_id": origin["parent_id"],
        "chart": origin["chart"],
        "equation": "target_normal_x^2-target_normal_y^2=0",
        "gradient_axis": "t",
        "gradient_sign": arb_sign(equality[1][0]),
        "regularity_certification": "CERTIFIED_STRICT_INTERVAL_DERIVATIVE",
        "lower_t_face_sign": arb_sign(low),
        "upper_t_face_sign": arb_sign(high),
        "face_classification": classification,
        "zero_set_dimension_account": dimension,
        "existence_over_full_base": existence,
        "two_open_3d_sides_retained": True,
        "whole_origin_credit": 0,
        "global_geometric_disposition_credit": 0,
        "provenance": "ROUND179_256_BIT_INTERVAL_GRADIENT_AND_T_FACE_SIGNS",
    }


def subtract_wall(dual, wall):
    return dual[0] - arb(wall), dual[1]


def expected_wall(origin, owner, geometry, reason):
    kind, axis, wall_text = reason.split(":")
    wall = int(wall_text)
    source_name = "source_x" if axis == "X" else "source_y"
    target_name = "hit_x" if axis == "X" else "hit_y"
    source = subtract_wall(geometry[source_name], wall)
    target = subtract_wall(geometry[target_name], wall)
    source_sign = arb_sign(source[0])
    source_axes = strict_axes(source)
    if source_sign != "OVERWRAP":
        source_class, source_axis, source_gradient = (
            "STRICT_NONZERO", None, None
        )
    else:
        require(source_axes, "source factor gradient")
        source_axis = source_axes[0]
        source_class = "REGULAR_GRAPH"
        source_gradient = arb_sign(
            source[1]["tps".index(source_axis)]
        )
    target_sign = arb_sign(target[0])
    target_axes = strict_axes(target)
    if target_sign != "OVERWRAP":
        target_class, target_axis, target_gradient = (
            "STRICT_NONZERO", None, None
        )
        lower_sign = upper_sign = None
        target_face = "STRICT_ZERO_ABSENT"
    else:
        require(target_axes, "target factor gradient")
        target_axis = target_axes[0]
        target_class = "REGULAR_GRAPH"
        target_gradient = arb_sign(
            target[1]["tps".index(target_axis)]
        )
        box = box_from(
            origin["box"], len(origin["refinement_path"]), origin["row_id"]
        )
        low = subtract_wall(
            independent_geometry(
                origin["chart"], owner,
                face_box(box, target_axis, False),
            )[target_name],
            wall,
        )[0]
        high = subtract_wall(
            independent_geometry(
                origin["chart"], owner,
                face_box(box, target_axis, True),
            )[target_name],
            wall,
        )[0]
        lower_sign = arb_sign(low)
        upper_sign = arb_sign(high)
        target_face = face_kind(low, high)
    graph_count = sum(
        item == "REGULAR_GRAPH" for item in (source_class, target_class)
    )
    crossing_discharged = (
        kind == "wall_crossing_time_not_strict"
        and source_class == target_class == "STRICT_NONZERO"
    )
    return {
        "row_id": make_id("wall-normal-form", [origin["row_id"], reason]),
        "origin_row_id": origin["row_id"],
        "parent_id": origin["parent_id"],
        "chart": origin["chart"],
        "reason_label": reason,
        "axis": axis,
        "integer_wall": wall,
        "zero_equation":
            f"(source_{axis.lower()}-{wall})*"
            f"(target_{axis.lower()}-{wall})=0",
        "source_factor_classification": source_class,
        "source_gradient_axis": source_axis,
        "source_gradient_sign": source_gradient,
        "target_factor_classification": target_class,
        "target_gradient_axis": target_axis,
        "target_gradient_sign": target_gradient,
        "target_lower_face_sign": lower_sign,
        "target_upper_face_sign": upper_sign,
        "target_face_classification": target_face,
        "zero_set_dimension_account": (
            "EMPTY_ZERO_SET"
            if graph_count == 0
            else "UNION_OF_CERTIFIED_REGULAR_DIMENSION_2_FACTORS"
        ),
        "crossing_time_dependency_overwrap_discharged":
            crossing_discharged,
        "whole_origin_credit": 0,
        "global_geometric_disposition_credit": 0,
        "provenance":
            "ROUND179_EXACT_ENDPOINT_FACTORIZATION_AND_256_BIT_GRADIENT",
    }


def expected_source_seam(origin):
    box = box_from(
        origin["box"], len(origin["refinement_path"]), origin["row_id"]
    )
    low = 2 * box.t0 * box.t0 - 1
    high = 2 * box.t1 * box.t1 - 1
    low_sign = (
        "STRICT_POSITIVE" if low > 0 else "STRICT_NEGATIVE"
        if low < 0 else "ZERO"
    )
    high_sign = (
        "STRICT_POSITIVE" if high > 0 else "STRICT_NEGATIVE"
        if high < 0 else "ZERO"
    )
    require(
        {low_sign, high_sign}
        == {"STRICT_NEGATIVE", "STRICT_POSITIVE"},
        "source seam face signs",
    )
    return {
        "row_id": make_id(
            "source-seam-normal-form",
            [origin["row_id"], "source_chart_seam"],
        ),
        "origin_row_id": origin["row_id"],
        "parent_id": origin["parent_id"],
        "chart": origin["chart"],
        "equation": "2*t^2-1=0",
        "gradient_axis": "t",
        "gradient_sign":
            "STRICT_POSITIVE" if box.t0 > 0 else "STRICT_NEGATIVE",
        "lower_t_face_sign": low_sign,
        "upper_t_face_sign": high_sign,
        "face_classification": "FULL_BASE_UNIQUE_GRAPH",
        "exact_dimension": 2,
        "half_open_owner_status": r174.seam_owner(origin["chart"]),
        "whole_origin_credit": 0,
        "global_geometric_disposition_credit": 0,
        "provenance": "ROUND179_EXACT_RATIONAL_FACE_SIGNS_AND_4T_DERIVATIVE",
    }


def expected_arrangement(origin):
    reasons = sorted(origin["reason_labels"])
    require(len(reasons) == 2, "pair arrangement")
    return {
        "row_id": make_id(
            "pair-arrangement",
            [origin["row_id"], "pair-arrangement", reasons],
        ),
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


def packed(columns, row):
    require(set(columns) == set(row), "expected packed keys")
    return [row[column] for column in columns]


def independently_rebuild_attachment(source_attachment, registry):
    schemas = source_attachment["row_column_schemas"]
    parents = unpack(source_attachment["parent_rows"], schemas["parent_rows"])
    origins = unpack(
        source_attachment["residual_3d_tube_rows"],
        schemas["residual_3d_tube_rows"],
    )
    owner = {row["parent_id"]: row["owner_target"] for row in parents}
    summaries = []
    resolved = []
    retained = []
    guards = []
    outgoing = []
    walls = []
    seams = []
    arrangements = []
    clusters = Counter()
    for origin in origins:
        target = owner[origin["parent_id"]]
        summary, rrows, trows, grows, ordinals = independently_split_origin(
            origin, target, registry
        )
        summaries.append(summary)
        resolved.extend(rrows)
        retained.extend(trows)
        guards.extend(grows)
        if summary["fully_replaced_by_bounded_children"]:
            clusters[tuple(ordinals)] += 1
        reasons = origin["reason_labels"]
        if any(
            reason == "outgoing_chart_seam" or reason.startswith("wall_")
            for reason in reasons
        ):
            geometry = independent_geometry(
                origin["chart"], target,
                box_from(
                    origin["box"], len(origin["refinement_path"]),
                    origin["row_id"],
                ),
            )
        else:
            geometry = None
        if "outgoing_chart_seam" in reasons:
            outgoing.append(expected_outgoing(origin, target, geometry))
        for reason in reasons:
            if reason.startswith("wall_"):
                walls.append(expected_wall(
                    origin, target, geometry, reason
                ))
        if "source_chart_seam" in reasons:
            seams.append(expected_source_seam(origin))
        if len(reasons) == 2:
            arrangements.append(expected_arrangement(origin))
    cluster_rows = [
        {
            "cluster_id": make_id(
                "closed-key-cluster", [list(ordinals), count]
            ),
            "released_exact_key_ordinals": list(ordinals),
            "released_exact_key_ordinals_sha256": digest(list(ordinals)),
            "fully_replaced_origin_count": count,
            "global_geometric_disposition_credit": 0,
        }
        for ordinals, count in sorted(clusters.items())
    ]
    summaries.sort(key=lambda row: row["origin_row_id"])
    for table in (
        resolved, retained, guards, outgoing, walls, seams, arrangements
    ):
        table.sort(key=lambda row: row["row_id"])
    cluster_rows.sort(key=lambda row: row["cluster_id"])
    packed_tables = {
        "origin_tube_rows": [
            packed(ORIGIN_COLUMNS, row) for row in summaries
        ],
        "resolved_3d_child_rows": [
            packed(RESOLVED_COLUMNS, row) for row in resolved
        ],
        "retained_3d_child_rows": [
            packed(RETAINED_COLUMNS, row) for row in retained
        ],
        "chart_guard_child_rows": [
            packed(GUARD_COLUMNS, row) for row in guards
        ],
        "outgoing_normal_form_rows": [
            packed(OUTGOING_COLUMNS, row) for row in outgoing
        ],
        "wall_normal_form_rows": [
            packed(WALL_COLUMNS, row) for row in walls
        ],
        "source_chart_seam_rows": [
            packed(SOURCE_SEAM_COLUMNS, row) for row in seams
        ],
        "pair_arrangement_candidate_rows": [
            packed(ARRANGEMENT_COLUMNS, row) for row in arrangements
        ],
        "fully_replaced_key_cluster_rows": [
            packed(KEY_CLUSTER_COLUMNS, row) for row in cluster_rows
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
        **packed_tables,
        "table_census_and_sha256": {
            name: {"row_count": len(table), "rows_sha256": digest(table)}
            for name, table in packed_tables.items()
        },
    }
    return {
        "schema": ATTACHMENT_SCHEMA,
        "result": result,
        "result_sha256": digest(result),
    }


def independent_statistics(attachment):
    result = attachment["result"]
    schemas = result["row_column_schemas"]
    origins = unpack(result["origin_tube_rows"], schemas["origin_tube_rows"])
    resolved = unpack(
        result["resolved_3d_child_rows"], schemas["resolved_3d_child_rows"]
    )
    retained = unpack(
        result["retained_3d_child_rows"], schemas["retained_3d_child_rows"]
    )
    guards = unpack(
        result["chart_guard_child_rows"], schemas["chart_guard_child_rows"]
    )
    outgoing = unpack(
        result["outgoing_normal_form_rows"],
        schemas["outgoing_normal_form_rows"],
    )
    walls = unpack(
        result["wall_normal_form_rows"], schemas["wall_normal_form_rows"]
    )
    seams = unpack(
        result["source_chart_seam_rows"], schemas["source_chart_seam_rows"]
    )
    arrangements = unpack(
        result["pair_arrangement_candidate_rows"],
        schemas["pair_arrangement_candidate_rows"],
    )
    clusters = unpack(
        result["fully_replaced_key_cluster_rows"],
        schemas["fully_replaced_key_cluster_rows"],
    )
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
        "statistics volume",
    )
    closed = [
        row for row in origins
        if row["fully_replaced_by_bounded_children"]
    ]
    partial = [
        row for row in origins
        if not row["fully_replaced_by_bounded_children"]
    ]
    reason_hist = Counter(
        reason for row in origins for reason in row["original_reason_labels"]
    )
    retained_hist = Counter(
        reason for row in retained for reason in row["reason_labels"]
    )
    closed_reasons = Counter(
        tuple(row["original_reason_labels"]) for row in closed
    )
    partial_reasons = Counter(
        tuple(row["original_reason_labels"]) for row in partial
    )
    zero_reasons = {
        reason: reason_hist.get(reason, 0)
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
    return {
        "Round174_origin_residual_tube_count": len(origins),
        "Round174_origin_partial_parent_count":
            len({row["parent_id"] for row in origins}),
        "Round174_origin_coordinate_volume": qstr(original_volume),
        "original_reason_occurrence_histogram": dict(sorted(reason_hist.items())),
        "original_reason_combo_count":
            len({tuple(row["original_reason_labels"]) for row in origins}),
        "original_single_reason_tube_count":
            sum(row["reason_count"] == 1 for row in origins),
        "original_two_reason_tube_count":
            sum(row["reason_count"] == 2 for row in origins),
        "one_step_fully_replaced_origin_tube_count": len(closed),
        "one_step_still_partial_origin_tube_count": len(partial),
        "one_step_closed_parent_union_count":
            len({row["parent_id"] for row in closed}),
        "one_step_partial_parent_union_count":
            len({row["parent_id"] for row in partial}),
        "one_step_resolved_child_count": len(resolved),
        "one_step_guard_child_count": len(guards),
        "one_step_retained_positive_3d_child_count": len(retained),
        "one_step_resolved_coordinate_volume": qstr(resolved_volume),
        "one_step_guard_coordinate_volume": qstr(guard_volume),
        "one_step_retained_coordinate_volume": qstr(retained_volume),
        "one_step_volume_conservation_exact": True,
        "released_local_exact_key_count":
            len({row["official_key_ordinal"] for row in resolved}),
        "released_local_exact_key_ordinals_sha256": digest(sorted({
            row["official_key_ordinal"] for row in resolved
        })),
        "fully_replaced_origin_key_cluster_count": len(clusters),
        "fully_replaced_by_reason": [
            {"reason_labels": list(reasons), "origin_count": count}
            for reasons, count in sorted(closed_reasons.items())
        ],
        "still_partial_by_reason": [
            {"reason_labels": list(reasons), "origin_count": count}
            for reasons, count in sorted(partial_reasons.items())
        ],
        "retained_reason_occurrence_histogram":
            dict(sorted(retained_hist.items())),
        "outgoing_predicate_row_count": len(outgoing),
        "outgoing_strict_t_derivative_count": sum(
            row["gradient_axis"] == "t"
            and row["gradient_sign"]
            in {"STRICT_NEGATIVE", "STRICT_POSITIVE"}
            for row in outgoing
        ),
        "outgoing_face_classification_histogram": dict(sorted(
            Counter(row["face_classification"] for row in outgoing).items()
        )),
        "wall_predicate_row_count": len(walls),
        "wall_source_factor_classification_histogram": dict(sorted(
            Counter(
                row["source_factor_classification"] for row in walls
            ).items()
        )),
        "wall_target_factor_classification_histogram": dict(sorted(
            Counter(
                row["target_factor_classification"] for row in walls
            ).items()
        )),
        "wall_target_face_classification_histogram": dict(sorted(
            Counter(
                row["target_face_classification"] for row in walls
            ).items()
        )),
        "wall_crossing_time_dependency_overwrap_discharged_count": sum(
            row["crossing_time_dependency_overwrap_discharged"]
            for row in walls
        ),
        "source_chart_seam_full_base_graph_count": len(seams),
        "two_predicate_arrangement_candidate_count": len(arrangements),
        "candidate_nominal_1D_intersection_row_count": len(arrangements),
        "candidate_boundary_0D_corner_row_count": len(arrangements),
        "certified_actual_pair_intersection_count": 0,
        "certified_actual_boundary_corner_count": 0,
        "zero_failure_reason_census": zero_reasons,
        "global_geometric_exact_key_disposition_count_before_Round179": 0,
        "global_geometric_exact_key_disposition_count_after_Round179": 0,
        "keys_without_global_geometric_disposition_after_Round179": 224580,
    }


def independently_expected_certificate(statistics, attachment):
    result = {
        "status": CERTIFIED_STATUS,
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
            "interval_precision_bits": 256,
            "Round171_result_sha256":
                "ffac0e2e16829c1a3ffc4783af2c224288265d02cf53c1d041aaf02013b52957",
            "Round171_verification_result_sha256":
                "60e9d4038c63bba14c0bd95478f63840735d8283f9cdfdefb1405ee2ed7defe3",
            "Round173_result_sha256":
                "948ab0a8539b08adc96c9493de415b44a5ffb75a1ee3ef47a4742902c211c11f",
            "Round173_verification_result_sha256":
                "047a580eb546cdb3880b93a9d0358e390d7ce418b371612f8e9fc4b0528f4644",
            "Round174_result_sha256":
                "d45f05458c42189cf0ebc51e258356d13278ba40845cce80b6a072ffbc8cf09b",
            "Round174_attachment_result_sha256":
                "002ca6631edd39c2325c63a1e8f9717d111f4d10c6d2585077d665a0ff128d18",
            "Round174_verification_result_sha256":
                "6c82800d41e456aeed7000bccb13bfe0e5e6d5f1637ac52a4d5c45b24ed9a23b",
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
            "full_base_unique_graph_requires_opposite_strict_face_signs": True,
            "strict_zero_absence_requires_same_strict_face_sign": True,
            "derivative_sign_alone_never_promoted_to_full_base_existence":
                True,
            "face_overwrap_rows_remain_partial": True,
        },
        "integer_wall_normal_forms": {
            "predicate_row_count": statistics["wall_predicate_row_count"],
            "exact_factorization":
                "(source_axis-wall)*(target_axis-wall)=0",
            "source_factor_classification_histogram":
                statistics["wall_source_factor_classification_histogram"],
            "target_factor_classification_histogram":
                statistics["wall_target_factor_classification_histogram"],
            "target_face_classification_histogram":
                statistics["wall_target_face_classification_histogram"],
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
                statistics["two_predicate_arrangement_candidate_count"],
            "nominal_1D_candidate_intersection_row_count":
                statistics["candidate_nominal_1D_intersection_row_count"],
            "boundary_0D_candidate_corner_row_count":
                statistics["candidate_boundary_0D_corner_row_count"],
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
            "keys_without_global_geometric_disposition_after_Round179": 224580,
            "reason":
                "child occurrences and bounded tube replacements do not "
                "connect or exclude every fibre of any global exact key",
        },
        "row_attachment": {
            "path": ATTACHMENT.name,
            "schema": ATTACHMENT_SCHEMA,
            "file_sha256": EXPECTED_ATTACHMENT_SHA256,
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
    return {
        "schema": SCHEMA,
        "result": result,
        "result_sha256": digest(result),
    }


def audit_certificate(certificate, expected_attachment):
    require(
        set(certificate) == {"schema", "result", "result_sha256"}
        and certificate["schema"] == SCHEMA
        and certificate["result_sha256"]
        == EXPECTED_CERTIFICATE_RESULT
        == digest(certificate["result"]),
        "certificate wrapper",
    )
    result = certificate["result"]
    require(
        set(result) == {
            "status", "scope", "provenance", "failure_taxonomy",
            "bounded_one_step_census", "outgoing_chart_normal_forms",
            "integer_wall_normal_forms",
            "source_chart_and_pair_arrangement", "dimension_safe_ledger",
            "observed_occurrence_vs_global_disposition", "row_attachment",
            "strict_nonpromotion", "next_core_gate",
        }
        and result["status"] == CERTIFIED_STATUS,
        "certificate top sections",
    )
    scope = result["scope"]
    require(
        scope["input_residual_tube_count"] == 62012
        and scope["input_partial_parent_count"] == 3840
        and scope["all_input_tubes_processed"] is True
        and scope["formal_verdict"] == "PARTIAL"
        and scope["global_geometric_exact_key_dispositions_added"] == 0
        and scope["CM2_exterior_sheet_exclusions_added"] == 0,
        "scope no promotion",
    )
    provenance = result["provenance"]
    require(
        provenance["dependency_sha256"] == PINS
        and provenance["python_flint_version"] == FLINT_VERSION
        and provenance["interval_precision_bits"] == 256
        and provenance["Round174_result_sha256"]
        == "d45f05458c42189cf0ebc51e258356d13278ba40845cce80b6a072ffbc8cf09b"
        and provenance["Round174_attachment_result_sha256"]
        == "002ca6631edd39c2325c63a1e8f9717d111f4d10c6d2585077d665a0ff128d18"
        and provenance["Round174_verification_result_sha256"]
        == "6c82800d41e456aeed7000bccb13bfe0e5e6d5f1637ac52a4d5c45b24ed9a23b"
        and provenance["Round174_verified_evaluator_reused_by_producer"] is True
        and provenance["throwaway_spike_imported"] is False
        and provenance["old_artifacts_modified"] is False,
        "provenance exact",
    )
    failure = result["failure_taxonomy"]
    require(
        failure["original_reason_combo_count"] == 28
        and failure["original_single_reason_tube_count"] == 61676
        and failure["original_two_reason_tube_count"] == 336
        and sum(failure["original_reason_occurrence_histogram"].values())
        == 62348
        and all(
            value == 0
            for value in failure["zero_failure_reason_census"].values()
        )
        and failure[
            "selected_root_grazing_equality_order_failures_present"
        ] is False
        and failure["simultaneous_corner_order_failure_present"] is False,
        "failure taxonomy",
    )
    bounded = result["bounded_one_step_census"]
    require(
        bounded["Round174_origin_residual_tube_count"] == 62012
        and bounded["Round174_origin_partial_parent_count"] == 3840
        and bounded["Round174_origin_coordinate_volume"]
        == "6337131/1638400000"
        and bounded["one_step_fully_replaced_origin_tube_count"] == 4116
        and bounded["one_step_still_partial_origin_tube_count"] == 57896
        and bounded["one_step_closed_parent_union_count"] == 1768
        and bounded["one_step_partial_parent_union_count"] == 3744
        and bounded["one_step_resolved_child_count"] == 17192
        and bounded["one_step_guard_child_count"] == 152
        and bounded["one_step_retained_positive_3d_child_count"] == 106680
        and bounded["one_step_resolved_coordinate_volume"]
        == "257889/524288000"
        and bounded["one_step_guard_coordinate_volume"]
        == "1239/409600000"
        and bounded["one_step_retained_coordinate_volume"]
        == "1768407/524288000"
        and bounded["one_step_volume_conservation_exact"] is True
        and bounded["released_local_exact_key_count"] == 116
        and bounded["fully_replaced_origin_key_cluster_count"] == 96,
        "bounded census",
    )
    outgoing = result["outgoing_chart_normal_forms"]
    require(
        outgoing["predicate_row_count"] == 34188
        and outgoing["strict_t_derivative_count"] == 34188
        and outgoing["face_classification_histogram"]
        == {
            "FACE_OVERWRAP_REGULAR_ZERO_SET_IF_PRESENT": 30444,
            "FULL_BASE_UNIQUE_GRAPH": 344,
            "STRICT_ZERO_ABSENT": 3400,
        }
        and outgoing[
            "derivative_sign_alone_never_promoted_to_full_base_existence"
        ] is True
        and outgoing["face_overwrap_rows_remain_partial"] is True,
        "outgoing normal forms",
    )
    wall = result["integer_wall_normal_forms"]
    require(
        wall["predicate_row_count"] == 27688
        and wall["source_factor_classification_histogram"]
        == {"REGULAR_GRAPH": 1056, "STRICT_NONZERO": 26632}
        and wall["target_factor_classification_histogram"]
        == {"REGULAR_GRAPH": 26344, "STRICT_NONZERO": 1344}
        and wall["target_face_classification_histogram"]
        == {
            "FACE_OVERWRAP_REGULAR_ZERO_SET_IF_PRESENT": 23776,
            "FULL_BASE_UNIQUE_GRAPH": 320,
            "STRICT_ZERO_ABSENT": 3592,
        }
        and wall[
            "crossing_time_dependency_overwrap_discharged_count"
        ] == 480
        and wall[
            "all_overwrapped_source_or_target_factors_have_a_strict_gradient"
        ] is True,
        "wall normal forms",
    )
    arrangement = result["source_chart_and_pair_arrangement"]
    require(
        arrangement["source_chart_full_base_unique_graph_count"] == 472
        and arrangement["source_chart_graph_exact_dimension"] == 2
        and arrangement["two_predicate_arrangement_candidate_count"] == 336
        and arrangement[
            "nominal_1D_candidate_intersection_row_count"
        ] == 336
        and arrangement["boundary_0D_candidate_corner_row_count"] == 336
        and arrangement["certified_actual_pair_intersection_count"] == 0
        and arrangement["certified_actual_boundary_corner_count"] == 0
        and arrangement[
            "candidate_existence_transversality_and_isolation_deferred"
        ] is True,
        "pair arrangement no false existence",
    )
    dimension = result["dimension_safe_ledger"]
    require(
        dimension["lower_dimensional_three_dimensional_volume_credit"] == 0
        and dimension["lower_dimensional_whole_origin_credit"] == 0
        and dimension[
            "retained_positive_volume_child_whole_origin_credit"
        ] == 0
        and dimension["chart_guard_is_not_CM2_exterior_sheet_exclusion"] is True
        and dimension["chart_guard_is_not_Gate5_geometric_disposition"] is True
        and dimension["local_occurrence_is_not_global_geometric_disposition"]
        is True,
        "dimension-safe credits",
    )
    observed = result["observed_occurrence_vs_global_disposition"]
    require(
        observed["released_local_exact_key_count"] == 116
        and observed[
            "global_geometric_exact_key_disposition_count_before_Round179"
        ] == 0
        and observed[
            "global_geometric_exact_key_disposition_count_after_Round179"
        ] == 0
        and observed[
            "keys_without_global_geometric_disposition_after_Round179"
        ] == 224580,
        "local versus global",
    )
    attachment = result["row_attachment"]
    require(
        attachment["path"] == ATTACHMENT.name
        and attachment["schema"] == ATTACHMENT_SCHEMA
        and attachment["file_sha256"] == EXPECTED_ATTACHMENT_SHA256
        and attachment["result_sha256"] == EXPECTED_ATTACHMENT_RESULT
        and attachment["table_census_and_sha256"]
        == expected_attachment["result"]["table_census_and_sha256"]
        and attachment["full_rows_materialized"] is True,
        "attachment binding",
    )
    strict = result["strict_nonpromotion"]
    require(
        strict["all_62012_Round174_residual_tubes_closed"] is False
        and strict["remaining_original_tube_count"] == 57896
        and strict["remaining_positive_volume_child_count"] == 106680
        and strict["all_pair_intersections_isolated"] is False
        and strict["source_G_global_exact_key_dispositions_complete"] is False
        and strict["D02"] == "BLOCKED"
        and strict["D03_negative_oracle"] == "UNAUTHORIZED"
        and strict["global_Gate5_fields"] == "10/18"
        and strict["global_complete_18_field_blocks"] == 0
        and strict["CM2"] == "NO-GO_FOR_CLAIM",
        "strict nonpromotion",
    )


def resign(document):
    document["result_sha256"] = digest(document["result"])


def validate_documents(
    candidate_certificate,
    candidate_attachment,
    expected_certificate,
    expected_attachment,
):
    require(
        candidate_certificate["result_sha256"]
        == digest(candidate_certificate["result"]),
        "candidate certificate self digest",
    )
    require(
        candidate_attachment["result_sha256"]
        == digest(candidate_attachment["result"]),
        "candidate attachment self digest",
    )
    for table_name, census in candidate_attachment["result"][
        "table_census_and_sha256"
    ].items():
        table = candidate_attachment["result"][table_name]
        require(
            census["row_count"] == len(table)
            and census["rows_sha256"] == digest(table),
            "candidate table self digest:" + table_name,
        )
    require(
        candidate_certificate == expected_certificate,
        "full canonical certificate equality",
    )
    require(
        candidate_attachment == expected_attachment,
        "full canonical attachment equality",
    )


def semantic_attacks(certificate, attachment, expected_attachment):
    expected_certificate = copy.deepcopy(certificate)
    certificate_attacks = [
        ("closed", ("strict_nonpromotion", "all_62012_Round174_residual_tubes_closed"), True),
        ("full_origins", ("bounded_one_step_census", "one_step_fully_replaced_origin_tube_count"), 4117),
        ("partial_origins", ("bounded_one_step_census", "one_step_still_partial_origin_tube_count"), 57895),
        ("resolved", ("bounded_one_step_census", "one_step_resolved_child_count"), 17193),
        ("guards", ("bounded_one_step_census", "one_step_guard_child_count"), 151),
        ("retained", ("bounded_one_step_census", "one_step_retained_positive_3d_child_count"), 106679),
        ("local_keys", ("bounded_one_step_census", "released_local_exact_key_count"), 117),
        ("local_to_global", ("observed_occurrence_vs_global_disposition", "global_geometric_exact_key_disposition_count_after_Round179"), 116),
        ("out_full", ("outgoing_chart_normal_forms", "face_classification_histogram", "FULL_BASE_UNIQUE_GRAPH"), 345),
        ("out_absent", ("outgoing_chart_normal_forms", "face_classification_histogram", "STRICT_ZERO_ABSENT"), 3399),
        ("out_overwrap", ("outgoing_chart_normal_forms", "face_classification_histogram", "FACE_OVERWRAP_REGULAR_ZERO_SET_IF_PRESENT"), 30443),
        ("wall_source_graph", ("integer_wall_normal_forms", "source_factor_classification_histogram", "REGULAR_GRAPH"), 1055),
        ("wall_target_strict", ("integer_wall_normal_forms", "target_factor_classification_histogram", "STRICT_NONZERO"), 1343),
        ("wall_target_graph", ("integer_wall_normal_forms", "target_factor_classification_histogram", "REGULAR_GRAPH"), 26343),
        ("wall_full", ("integer_wall_normal_forms", "target_face_classification_histogram", "FULL_BASE_UNIQUE_GRAPH"), 321),
        ("wall_absent", ("integer_wall_normal_forms", "target_face_classification_histogram", "STRICT_ZERO_ABSENT"), 3591),
        ("wall_overwrap", ("integer_wall_normal_forms", "target_face_classification_histogram", "FACE_OVERWRAP_REGULAR_ZERO_SET_IF_PRESENT"), 23775),
        ("nominal_actual", ("source_chart_and_pair_arrangement", "certified_actual_pair_intersection_count"), 336),
        ("corner_actual", ("source_chart_and_pair_arrangement", "certified_actual_boundary_corner_count"), 336),
        ("root_zero", ("failure_taxonomy", "zero_failure_reason_census", "selected_root_sign_or_owner"), 1),
        ("grazing_zero", ("failure_taxonomy", "zero_failure_reason_census", "target_grazing_or_discriminant"), 1),
        ("corner_zero", ("failure_taxonomy", "zero_failure_reason_census", "simultaneous_corner_order"), 1),
        ("D02", ("strict_nonpromotion", "D02"), "READY"),
        ("Gate5", ("strict_nonpromotion", "global_Gate5_fields"), "18/18"),
        ("CM2", ("strict_nonpromotion", "CM2"), "GO"),
    ]
    rejected = []
    for name, path, replacement in certificate_attacks:
        candidate = copy.deepcopy(certificate)
        node = candidate["result"]
        for part in path[:-1]:
            node = node[part]
        node[path[-1]] = replacement
        resign(candidate)
        try:
            validate_documents(
                candidate, attachment,
                expected_certificate, expected_attachment,
            )
        except Exception:
            rejected.append("certificate:" + name)
        else:
            raise RuntimeError("accepted certificate attack:" + name)
    attachment_attacks = [
        ("origin_closed", ("result", "origin_tube_rows", 0, 16), True),
        ("resolved_global", ("result", "resolved_3d_child_rows", 0, 19), 1),
        ("retained_whole", ("result", "retained_3d_child_rows", 0, 10), 1),
        ("guard_global", ("result", "chart_guard_child_rows", 0, 10), True),
        ("out_whole", ("result", "outgoing_normal_form_rows", 0, 14), 1),
        ("wall_global", ("result", "wall_normal_form_rows", 0, 20), 1),
        ("pair_actual", ("result", "pair_arrangement_candidate_rows", 0, 8), "CERTIFIED_PRESENT"),
        ("cluster_global", ("result", "fully_replaced_key_cluster_rows", 0, 4), 1),
    ]
    for name, path, replacement in attachment_attacks:
        table_name = path[1]
        node = attachment
        for part in path[:-1]:
            node = node[part]
        key = path[-1]
        original = node[key]
        original_table_digest = attachment["result"][
            "table_census_and_sha256"
        ][table_name]["rows_sha256"]
        original_attachment_hash = attachment["result_sha256"]
        original_certificate_attachment = copy.deepcopy(
            certificate["result"]["row_attachment"]
        )
        original_certificate_hash = certificate["result_sha256"]
        node[key] = replacement
        table = attachment["result"][table_name]
        attachment["result"]["table_census_and_sha256"][table_name][
            "rows_sha256"
        ] = digest(table)
        resign(attachment)
        certificate["result"]["row_attachment"][
            "table_census_and_sha256"
        ] = copy.deepcopy(
            attachment["result"]["table_census_and_sha256"]
        )
        certificate["result"]["row_attachment"]["result_sha256"] = (
            attachment["result_sha256"]
        )
        certificate["result"]["row_attachment"]["file_sha256"] = (
            hashlib.sha256(
                (canonical(attachment) + "\n").encode()
            ).hexdigest()
        )
        resign(certificate)
        try:
            validate_documents(
                certificate, attachment,
                expected_certificate, expected_attachment,
            )
        except Exception:
            rejected.append("attachment:" + name)
        else:
            raise RuntimeError("accepted attachment attack:" + name)
        finally:
            node[key] = original
            attachment["result"]["table_census_and_sha256"][table_name][
                "rows_sha256"
            ] = original_table_digest
            attachment["result_sha256"] = original_attachment_hash
            certificate["result"]["row_attachment"] = (
                original_certificate_attachment
            )
            certificate["result_sha256"] = original_certificate_hash
    require(
        len(rejected) == len(certificate_attacks) + len(attachment_attacks),
        "semantic attack census",
    )
    return {
        "attempted": len(rejected), "rejected": len(rejected),
        "labels": rejected, "all_rejected": True,
    }


def strict_json_attacks():
    cases = {
        "duplicate": b'{"x":1,"x":2}',
        "bom": b'\xef\xbb\xbf{"x":1}',
        "nul": b'{"x":"\\u0000"}',
        "nan": b'{"x":NaN}',
        "infinity": b'{"x":Infinity}',
        "float": b'{"x":1.5}',
        "top_array": b'[]',
        "trailing": b'{"x":1}x',
        "invalid_utf8": b'{"x":"\xff"}',
    }
    rejected = []
    for name, raw in cases.items():
        try:
            strict_decode(raw)
        except Exception:
            rejected.append(name)
        else:
            raise RuntimeError("accepted JSON attack:" + name)
    try:
        strict_decode(b"x" * 180_000_001)
    except Exception:
        rejected.append("oversize")
    else:
        raise RuntimeError("accepted oversize")
    return {
        "attempted": 10, "rejected": len(rejected),
        "labels": rejected, "all_rejected": len(rejected) == 10,
    }


def output_guard(path: Path):
    protected = {
        PRODUCER.resolve(), CERTIFICATE.resolve(), ATTACHMENT.resolve(),
        Path(__file__).resolve(),
        *[(BASE / name).resolve() for name in PINS],
    }
    require(path.parent.exists() and path.parent.is_dir(), "output parent")
    require(not path.parent.is_symlink(), "output parent symlink")
    require(path.resolve(strict=False) not in protected, "output alias")
    if path.exists() or path.is_symlink():
        require(not path.is_symlink(), "output symlink")
        info = path.stat()
        require(stat.S_ISREG(info.st_mode), "output regular")
        require(info.st_nlink == 1, "output hardlink")


def path_attacks():
    rejected = []
    with tempfile.TemporaryDirectory(dir=BASE) as directory_name:
        temporary = Path(directory_name)
        stem = temporary.name
        ordinary = BASE / f"{stem}-ordinary"
        symlink = BASE / f"{stem}-symlink"
        hardlink = BASE / f"{stem}-hardlink"
        directory = BASE / f"{stem}-directory"
        fifo = BASE / f"{stem}-fifo"
        ordinary.write_text("{}", encoding="utf-8")
        symlink.symlink_to(ordinary)
        os.link(ordinary, hardlink)
        directory.mkdir()
        os.mkfifo(fifo)
        input_cases = [
            ("parent", temporary / "escape"),
            ("symlink", symlink),
            ("hardlink", hardlink),
            ("directory", directory),
            ("fifo", fifo),
            ("missing", BASE / f"{stem}-missing"),
        ]
        try:
            for name, path in input_cases:
                try:
                    input_bytes(path, 1000)
                except Exception:
                    rejected.append("input:" + name)
                else:
                    raise RuntimeError("accepted path:" + name)
            output_cases = [
                ("producer", PRODUCER),
                ("certificate", CERTIFICATE),
                ("attachment", ATTACHMENT),
                ("symlink", symlink),
                ("hardlink", hardlink),
            ]
            for name, path in output_cases:
                try:
                    output_guard(path)
                except Exception:
                    rejected.append("output:" + name)
                else:
                    raise RuntimeError("accepted output alias:" + name)
        finally:
            for path in (symlink, hardlink, ordinary, fifo):
                if path.exists() or path.is_symlink():
                    path.unlink()
            if directory.exists():
                directory.rmdir()
    return {
        "attempted": 11, "rejected": len(rejected),
        "labels": rejected, "all_rejected": len(rejected) == 11,
    }


def build_verification():
    certificate_raw = input_bytes(CERTIFICATE, 2_000_000)
    attachment_raw = input_bytes(ATTACHMENT, 180_000_000)
    require(
        hashlib.sha256(certificate_raw).hexdigest()
        == EXPECTED_CERTIFICATE_SHA256,
        "certificate file pin",
    )
    require(
        hashlib.sha256(attachment_raw).hexdigest()
        == EXPECTED_ATTACHMENT_SHA256,
        "attachment file pin",
    )
    certificate = strict_decode(certificate_raw)
    attachment = strict_decode(attachment_raw)
    require(
        attachment["schema"] == ATTACHMENT_SCHEMA
        and attachment["result_sha256"]
        == EXPECTED_ATTACHMENT_RESULT
        == digest(attachment["result"]),
        "actual attachment wrapper",
    )
    _source_certificate, source_attachment, registry = load_sources()
    ctx.prec = PRECISION_BITS
    expected_attachment = independently_rebuild_attachment(
        source_attachment, registry
    )
    expected_raw = (canonical(expected_attachment) + "\n").encode()
    require(
        len(expected_raw) == len(attachment_raw) == 131273924,
        "full attachment byte count",
    )
    require(
        hashlib.sha256(expected_raw).hexdigest()
        == EXPECTED_ATTACHMENT_SHA256
        and expected_raw == attachment_raw
        and expected_attachment == attachment,
        "full attachment exact reconstruction",
    )
    statistics = independent_statistics(expected_attachment)
    expected_certificate = independently_expected_certificate(
        statistics, expected_attachment
    )
    require(
        expected_certificate["result_sha256"]
        == EXPECTED_CERTIFICATE_RESULT
        and expected_certificate == certificate,
        "full independently expected certificate canonical equality",
    )
    audit_certificate(certificate, expected_attachment)
    semantic = semantic_attacks(
        certificate, attachment, expected_attachment
    )
    strict_json = strict_json_attacks()
    paths = path_attacks()
    tables = expected_attachment["result"]
    schemas = tables["row_column_schemas"]
    origins = unpack(tables["origin_tube_rows"], schemas["origin_tube_rows"])
    outgoing = unpack(
        tables["outgoing_normal_form_rows"],
        schemas["outgoing_normal_form_rows"],
    )
    walls = unpack(
        tables["wall_normal_form_rows"],
        schemas["wall_normal_form_rows"],
    )
    arrangements = unpack(
        tables["pair_arrangement_candidate_rows"],
        schemas["pair_arrangement_candidate_rows"],
    )
    result = {
        "status": "PASS",
        "certificate_schema": SCHEMA,
        "certificate_file_sha256": EXPECTED_CERTIFICATE_SHA256,
        "certificate_result_sha256": EXPECTED_CERTIFICATE_RESULT,
        "attachment_schema": ATTACHMENT_SCHEMA,
        "attachment_file_sha256": EXPECTED_ATTACHMENT_SHA256,
        "attachment_result_sha256": EXPECTED_ATTACHMENT_RESULT,
        "producer_file_sha256": EXPECTED_PRODUCER_SHA256,
        "verifier_file_sha256": hashlib.sha256(
            Path(__file__).read_bytes()
        ).hexdigest(),
        "producer_imported_or_executed": False,
        "producer_treated_as_inert_pinned_bytes": True,
        "full_attachment_exactly_reconstructed": True,
        "full_attachment_byte_for_byte_matched": True,
        "full_attachment_bytes_compared": len(attachment_raw),
        "full_certificate_exactly_reconstructed": True,
        "full_certificate_canonical_equality_matched": True,
        "full_certificate_file_pinned_and_all_sections_audited": True,
        "independent_reconstruction": {
            "origin_tube_count": len(origins),
            "fully_replaced_origin_tube_count": sum(
                row["fully_replaced_by_bounded_children"]
                for row in origins
            ),
            "still_partial_origin_tube_count": sum(
                not row["fully_replaced_by_bounded_children"]
                for row in origins
            ),
            "resolved_child_count":
                len(tables["resolved_3d_child_rows"]),
            "guard_child_count": len(tables["chart_guard_child_rows"]),
            "retained_positive_3d_child_count":
                len(tables["retained_3d_child_rows"]),
            "released_local_exact_key_count": 116,
            "outgoing_predicate_count": len(outgoing),
            "outgoing_face_classification_histogram": dict(sorted(
                Counter(row["face_classification"] for row in outgoing).items()
            )),
            "wall_predicate_count": len(walls),
            "wall_source_factor_histogram": dict(sorted(
                Counter(
                    row["source_factor_classification"] for row in walls
                ).items()
            )),
            "wall_target_factor_histogram": dict(sorted(
                Counter(
                    row["target_factor_classification"] for row in walls
                ).items()
            )),
            "pair_arrangement_candidate_count": len(arrangements),
            "certified_actual_pair_intersection_count": 0,
            "certified_actual_boundary_corner_count": 0,
            "zero_failure_reasons_reconfirmed": True,
            "global_geometric_exact_key_disposition_count": 0,
        },
        "resigned_semantic_attacks": semantic,
        "strict_json_and_oversize_attacks": strict_json,
        "path_type_and_output_alias_attacks": paths,
        "strict_nonpromotion_reconfirmed": {
            "D02": "BLOCKED",
            "D03_negative_oracle": "UNAUTHORIZED",
            "global_Gate5_fields": "10/18",
            "global_complete_18_field_blocks": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "hash_seed_sensitive_output_fields": [],
    }
    return {
        "schema": VERIFICATION_SCHEMA,
        "result": result,
        "result_sha256": digest(result),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    arguments = parser.parse_args()
    output_guard(arguments.output)
    verification = build_verification()
    arguments.output.write_text(
        json.dumps(
            verification, sort_keys=True, indent=2,
            ensure_ascii=False, allow_nan=False,
        ) + "\n",
        encoding="utf-8",
    )
    result = verification["result"]
    print(result["status"])
    print(
        "origins/children",
        result["independent_reconstruction"]["origin_tube_count"],
        result["independent_reconstruction"]["resolved_child_count"],
        result["independent_reconstruction"]["retained_positive_3d_child_count"],
    )
    print(
        "attacks",
        result["resigned_semantic_attacks"]["rejected"],
        result["strict_json_and_oversize_attacks"]["rejected"],
        result["path_type_and_output_alias_attacks"]["rejected"],
    )
    print(verification["result_sha256"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
