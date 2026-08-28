#!/usr/bin/env python3
"""Formal bounded source-G p/s internal-face trace/glue materialization.

The producer reconstructs the pinned Round208 strict 3D leaves, the Round211
local lower-dimensional owner rows, and the Round214 contact taxonomy.  It
materializes only exact p/s common faces on which interval arithmetic proves
an active-factor zero trace over the *entire* common face: opposite strict
endpoint signs in t and a strict t derivative on the full rectangle.

Each accepted trace receives canonical trace, two-sided incidence, and glue
IDs.  Cross-occurrence glue is permitted only when the two upstream leaves
have the same parent atlas, identical restricted evaluator identity, and
exactly equal common-face geometry.  Box touch or a shared signature hash is
never sufficient.

All incomplete endpoint-to-interior, partial-face, physical-component, whole
leaf/origin/tube, global-fibre, and disposition claims remain fail-closed.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import copy
from fractions import Fraction as Q
import hashlib
import json
import os
from pathlib import Path
import stat
import sys
import tempfile
from typing import Any, Iterable

from flint import ctx

import cm2_round186_source_g_factor_face_probe as r186
import cm2_round209_source_g_outgoing_half_open_owner_probe as r209


sys.dont_write_bytecode = True

HERE = Path(__file__).resolve().parent
PREFIX = "cm2_round217_source_g_internal_face_trace_glue_materialization"
OUTPUT = HERE / f"{PREFIX}_certificate.json"
SCHEMA = "cm2.round217.source-g-internal-face-trace-glue-materialization.v1"
STATUS = (
    "CERTIFIED_BOUNDED_EXACT_P_S_INTERNAL_FACE_ZERO_TRACE_AND_GLUE_ROWS__"
    "PHYSICAL_COMPONENT_AND_GLOBAL_FIBRE_INCOMPLETE"
)
MAX_INPUT_BYTES = 300 * 1024 * 1024

R211_SOURCE = "cm2_round211_source_g_outgoing_half_open_owner_materialization.py"
R211_CERTIFICATE = (
    "cm2_round211_source_g_outgoing_half_open_owner_materialization"
    "_certificate.json"
)
R211_SOURCE_SHA256 = (
    "9e8874672150d7585316524a7724070f4543e231de5481d1c1dfbd00ddc65a02"
)
R211_CERTIFICATE_SHA256 = (
    "bb03a39a74a237b9f4449214c698795856fce4d6be2195c4f9d7774cd1d4183f"
)
R211_RESULT_SHA256 = (
    "3b831c67669e52f1247ea30c0a1ed7d5c1002931a1c0f621dd934085e87c2d5b"
)

R204_SOURCE = (
    "cm2_round204_source_g_wall_return_signature_local_replacement.py"
)
R204_CERTIFICATE = (
    "cm2_round204_source_g_wall_return_signature_local_replacement"
    "_certificate.json"
)
R204_SOURCE_SHA256 = (
    "7e4b81846155c1edad0807362c7086a290702da7ce6680d7c449b7193635da77"
)
R204_CERTIFICATE_SHA256 = (
    "e7e1c49bebcb8c01f0fb4b33af66e4f2a8de560f121cae65f4971b2fec3e1818"
)
R204_RESULT_SHA256 = (
    "ef106d06399094a453eb5e66d73a0022a9bb5343f8c4788b3a3fbc9177d45ccd"
)

R214_SOURCE = (
    "cm2_round214_source_g_physical_component_join_dedup_feasibility_probe.py"
)
R214_REPORT = (
    "cm2_round214_source_g_physical_component_join_dedup_spike_report.md"
)
R214_SOURCE_SHA256 = (
    "d074aa045637ce1bb31768fa551bdb73ceda6a58c760cafe3dbf92faa7c922fe"
)
R214_REPORT_SHA256 = (
    "aa48c012fa8c57df89b2bea4123467fc2c74821a03525095976cb61c709fe952"
)
R214_RESULT_SHA256 = (
    "ddc12c8e625a5a65cc8e445d97ee89e64429a6c729efe32778a092f7e6521d09"
)
R214_DOCUMENT_SHA256 = (
    "9a90e2f01cf03b263803298ba1977c9ecfa6e70778698ea13e28a7fdcbc071d7"
)

R209_SOURCE = "cm2_round209_source_g_outgoing_half_open_owner_probe.py"
R209_SOURCE_SHA256 = (
    "dcd8d6d2354151a0aa1c45db8f1ce78f1385b665741ee5a79521bf261cebc13f"
)
R208_SOURCE = (
    "cm2_round208_source_g_outgoing_direct_signature_materialization.py"
)
R208_CERTIFICATE = (
    "cm2_round208_source_g_outgoing_direct_signature_materialization"
    "_certificate.json"
)
R208_SOURCE_SHA256 = (
    "c9fe0cdfb4631c31702473d705b04fa89fb8d51e4c71c9b2b652dc98e4641913"
)
R208_CERTIFICATE_SHA256 = (
    "4d01fb9cee639ec59786c078f7a20b3bbcd5c18ea674fabbfce64e250e765938"
)
R208_RESULT_SHA256 = (
    "d00674fa4061364539ce6f36f6f8de938f50bc54afbf5497266dcfa0e078bca8"
)
R186_SOURCE = "cm2_round186_source_g_factor_face_probe.py"
R186_SOURCE_SHA256 = (
    "5797b8f4c2ba9c8c5b42b32511f3c97a15469b59bdf00cd8430580c3429c7c64"
)

EXPECTED_LEAVES = 18_324
EXPECTED_STRICT_REGIONS = 36_040
EXPECTED_SHEETS = 17_716
EXPECTED_CURVES = 20_456
EXPECTED_ENDPOINTS = 40_912
EXPECTED_POSITIVE_FACE_CONTACTS = 15_540
EXPECTED_EXACT_P_S_CONTACTS = 7_932
EXPECTED_WHOLE_FACE_TRACES = 448
EXPECTED_EXACT_P_S_FRONTIER = 7_484
EXPECTED_PARTIAL_CONTACTS = 644
EXPECTED_PARTIAL_UNRESOLVED = 264
EXPECTED_SOURCE_G_EXACT_KEYS = 224_580
STRICT_SIGNS = {"STRICT_NEGATIVE", "STRICT_POSITIVE"}


class Round217Error(RuntimeError):
    pass


def require(condition: bool, label: str) -> None:
    if not condition:
        raise Round217Error(label)


ENCODER = json.JSONEncoder(
    sort_keys=True,
    separators=(",", ":"),
    ensure_ascii=False,
    allow_nan=False,
)


def encoded_chunks(value: Any) -> Iterable[bytes]:
    for chunk in ENCODER.iterencode(value):
        yield chunk.encode()


def canonical_bytes(value: Any) -> bytes:
    return b"".join(encoded_chunks(value))


def digest(value: Any) -> str:
    state = hashlib.sha256()
    for chunk in encoded_chunks(value):
        state.update(chunk)
    return state.hexdigest()


def closed_row(payload: dict[str, Any]) -> dict[str, Any]:
    row = copy.deepcopy(payload)
    row["row_sha256"] = digest(row)
    return row


def regular_bytes(path: Path, maximum: int = MAX_INPUT_BYTES) -> bytes:
    before = path.lstat()
    require(stat.S_ISREG(before.st_mode), f"regular:{path.name}")
    require(not path.is_symlink(), f"symlink:{path.name}")
    require(before.st_nlink == 1, f"hardlink:{path.name}")
    require(0 < before.st_size <= maximum, f"size:{path.name}")
    descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
    try:
        opened = os.fstat(descriptor)
        require(
            (
                opened.st_dev,
                opened.st_ino,
                opened.st_size,
                opened.st_mtime_ns,
            )
            == (
                before.st_dev,
                before.st_ino,
                before.st_size,
                before.st_mtime_ns,
            ),
            f"stable-open:{path.name}",
        )
        chunks: list[bytes] = []
        total = 0
        while True:
            chunk = os.read(descriptor, 1024 * 1024)
            if not chunk:
                break
            total += len(chunk)
            require(total <= maximum, f"bounded-read:{path.name}")
            chunks.append(chunk)
        after = os.fstat(descriptor)
        require(
            (
                after.st_dev,
                after.st_ino,
                after.st_size,
                after.st_mtime_ns,
            )
            == (
                opened.st_dev,
                opened.st_ino,
                opened.st_size,
                opened.st_mtime_ns,
            ),
            f"stable-read:{path.name}",
        )
        return b"".join(chunks)
    finally:
        os.close(descriptor)


def pinned_bytes(path: Path, expected: str, maximum: int) -> bytes:
    raw = regular_bytes(path, maximum)
    require(
        hashlib.sha256(raw).hexdigest() == expected,
        f"SHA256:{path.name}",
    )
    return raw


def histogram(values: Iterable[Any]) -> dict[str, int]:
    return dict(sorted(Counter(str(value) for value in values).items()))


def row_id(kind: str, identity: dict[str, Any]) -> str:
    return f"round217-{kind}:{digest(identity)}"


def ledger(rows: list[dict[str, Any]], id_key: str) -> dict[str, Any]:
    return {
        "row_count": len(rows),
        "rows_sha256": digest(rows),
        "row_ids_sha256": digest([row[id_key] for row in rows]),
        "row_hashes_sha256": digest([row["row_sha256"] for row in rows]),
        "every_row_closed_by_own_SHA256": True,
        "rows": rows,
    }


def validate_inputs() -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    dict[str, dict[str, Any]],
    dict[str, str],
]:
    require(
        Path(r209.__file__).resolve() == (HERE / R209_SOURCE).resolve(),
        "Round209 module identity",
    )
    require(
        Path(r186.__file__).resolve() == (HERE / R186_SOURCE).resolve(),
        "Round186 module identity",
    )
    pinned_bytes(HERE / R209_SOURCE, R209_SOURCE_SHA256, 5_000_000)
    pinned_bytes(HERE / R208_SOURCE, R208_SOURCE_SHA256, 5_000_000)
    raw208 = pinned_bytes(
        HERE / R208_CERTIFICATE,
        R208_CERTIFICATE_SHA256,
        MAX_INPUT_BYTES,
    )
    pinned_bytes(HERE / R186_SOURCE, R186_SOURCE_SHA256, 5_000_000)
    pinned_bytes(HERE / R214_SOURCE, R214_SOURCE_SHA256, 5_000_000)
    pinned_bytes(HERE / R214_REPORT, R214_REPORT_SHA256, 5_000_000)
    pinned_bytes(HERE / R211_SOURCE, R211_SOURCE_SHA256, 5_000_000)
    pinned_bytes(HERE / R204_SOURCE, R204_SOURCE_SHA256, 5_000_000)
    raw204 = pinned_bytes(
        HERE / R204_CERTIFICATE,
        R204_CERTIFICATE_SHA256,
        20_000_000,
    )
    raw211 = pinned_bytes(
        HERE / R211_CERTIFICATE,
        R211_CERTIFICATE_SHA256,
        MAX_INPUT_BYTES,
    )
    certificate211 = json.loads(raw211)
    certificate204 = json.loads(raw204)
    certificate208 = json.loads(raw208)
    require(
        set(certificate208) == {"schema", "result", "result_sha256"}
        and certificate208["result_sha256"] == R208_RESULT_SHA256
        and digest(certificate208["result"]) == R208_RESULT_SHA256,
        "Round208 direct result closure",
    )
    require(
        set(certificate204) == {"schema", "result", "result_sha256"}
        and certificate204["result_sha256"] == R204_RESULT_SHA256
        and digest(certificate204["result"]) == R204_RESULT_SHA256
        and len(
            certificate204["result"][
                "exact_key_local_join_ledger"
            ]["official_key_ordinals"]
        ) == 12,
        "Round204 result closure and 12-ordinal boundary",
    )
    require(
        set(certificate211) == {"schema", "result", "result_sha256"}
        and certificate211["result_sha256"] == R211_RESULT_SHA256
        and digest(certificate211["result"]) == R211_RESULT_SHA256,
        "Round211 result closure",
    )

    _r173, r208, hashes209 = r209.validate_inputs()
    require(
        hashes209["Round208_producer_source_sha256"] == R208_SOURCE_SHA256
        and hashes209["Round208_certificate_sha256"]
        == R208_CERTIFICATE_SHA256
        and hashes209["Round208_result_sha256"] == R208_RESULT_SHA256,
        "Round208 direct and Round209 boundaries agree",
    )
    leaves, regions, _faces, _u2 = r209.validate_round195_geometry(r208)
    sheets, curves, endpoints, _audit = r209.build_lineages(leaves, regions)
    require(
        len(leaves) == EXPECTED_LEAVES
        and len(regions) == EXPECTED_STRICT_REGIONS
        and len(sheets) == EXPECTED_SHEETS
        and len(curves) == EXPECTED_CURVES
        and len(endpoints) == EXPECTED_ENDPOINTS,
        "reconstructed Round208/Round209 dimensional census",
    )

    formal_sheet_rows = certificate211["result"][
        "formal_2D_sheet_owner_ledger"
    ]["rows"]
    formal_curve_rows = certificate211["result"][
        "formal_1D_curve_incidence_owner_ledger"
    ]["rows"]
    formal_endpoint_rows = certificate211["result"][
        "formal_0D_endpoint_incidence_owner_ledger"
    ]["rows"]
    formal_sheets = {
        row["probe_sheet_row_id"]: row for row in formal_sheet_rows
    }
    require(
        len(formal_sheets) == EXPECTED_SHEETS
        and {
            key: row["probe_sheet_row_sha256"]
            for key, row in formal_sheets.items()
        }
        == {row["sheet_row_id"]: row["row_sha256"] for row in sheets},
        "Round211 exact sheet lineage",
    )
    require(
        {
            row["probe_curve_row_id"]: row["probe_curve_row_sha256"]
            for row in formal_curve_rows
        }
        == {row["curve_row_id"]: row["row_sha256"] for row in curves},
        "Round211 exact curve lineage",
    )
    require(
        {
            row["probe_endpoint_row_id"]: row["probe_endpoint_row_sha256"]
            for row in formal_endpoint_rows
        }
        == {row["endpoint_row_id"]: row["row_sha256"] for row in endpoints},
        "Round211 exact endpoint lineage",
    )
    require(
        all(
            row["component_deduplication_credit"] == 0
            and row["whole_leaf_credit"] == 0
            and row["whole_origin_credit"] == 0
            and row["whole_original_tube_credit"] == 0
            and row["global_exact_key_disposition_credit"] == 0
            for row in formal_sheet_rows + formal_curve_rows
            + formal_endpoint_rows
        ),
        "Round211 zero global promotion",
    )
    hashes = {
        "Round208_certificate_sha256":
            hashes209["Round208_certificate_sha256"],
        "Round208_result_sha256": hashes209["Round208_result_sha256"],
        "Round208_source_sha256": R208_SOURCE_SHA256,
        "Round209_probe_source_sha256": R209_SOURCE_SHA256,
        "Round211_source_sha256": R211_SOURCE_SHA256,
        "Round211_certificate_sha256": R211_CERTIFICATE_SHA256,
        "Round211_result_sha256": R211_RESULT_SHA256,
        "Round204_source_sha256": R204_SOURCE_SHA256,
        "Round204_certificate_sha256": R204_CERTIFICATE_SHA256,
        "Round204_result_sha256": R204_RESULT_SHA256,
        "Round214_probe_source_sha256": R214_SOURCE_SHA256,
        "Round214_probe_report_sha256": R214_REPORT_SHA256,
        "Round214_probe_result_sha256": R214_RESULT_SHA256,
        "Round214_probe_document_sha256": R214_DOCUMENT_SHA256,
        "Round186_factor_evaluator_source_sha256": R186_SOURCE_SHA256,
    }
    return (
        leaves,
        regions,
        sheets,
        curves,
        endpoints,
        formal_sheet_rows,
        formal_sheets,
        hashes,
    )


def build_result(producer_sha256: str) -> dict[str, Any]:
    print("Round217 rebuilding pinned Round208/211 boundary", file=sys.stderr)
    (
        leaves,
        regions,
        sheets,
        curves,
        endpoints,
        _formal_sheet_rows,
        formal_sheets_by_probe,
        input_hashes,
    ) = validate_inputs()

    leaf_by_id = {row["leaf_row_id"]: row for row in leaves}
    region_by_id = {row["region_row_id"]: row for row in regions}
    sheet_by_leaf = {row["leaf_row_id"]: row for row in sheets}
    boxes = {
        leaf_id: tuple(Q(value) for value in leaf_by_id[leaf_id]["box"])
        for leaf_id in sheet_by_leaf
    }
    parent_by_leaf = {
        row["leaf_row_id"]: row["parent_id"]
        for row in regions
        if row["leaf_row_id"] in sheet_by_leaf
    }
    occurrence_by_leaf = {
        leaf_id: row["occurrence_row_id"]
        for leaf_id, row in sheet_by_leaf.items()
    }
    origin_by_leaf = {
        leaf_id: row["origin_row_id"]
        for leaf_id, row in sheet_by_leaf.items()
    }
    retained_by_leaf = {
        leaf_id: row["retained_child_row_id"]
        for leaf_id, row in sheet_by_leaf.items()
    }

    identity_by_leaf: dict[str, tuple[Any, ...]] = {}
    evaluator_by_leaf: dict[str, tuple[str, str, str]] = {}
    ordinal_by_leaf: dict[str, int] = {}
    for leaf_id, sheet in sheet_by_leaf.items():
        owner = region_by_id[sheet["owner_region_row_id"]]
        signature = owner["local_return_signature"]
        identity_by_leaf[leaf_id] = (
            parent_by_leaf[leaf_id],
            signature["source_chart"],
            signature["target_lift"],
            tuple(signature["signed_wall_word"]),
            signature["roof"],
            sheet["active_factor"],
            sheet["owner_outgoing_cell"],
            sheet["owner_signature_core_sha256"],
        )
        evaluator_by_leaf[leaf_id] = (
            signature["source_chart"],
            signature["target_lift"],
            sheet["active_factor"],
        )
        ordinal_by_leaf[leaf_id] = signature["official_key_ordinal"]

    curves_by_leaf: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in curves:
        curves_by_leaf[row["leaf_row_id"]].append(row)

    def curve_carrier(row: dict[str, Any]) -> tuple[Any, ...]:
        leaf_id = row["leaf_row_id"]
        box = boxes[leaf_id]
        t_value = box[0] if row["face_side"] == "LOWER" else box[1]
        return identity_by_leaf[leaf_id] + (
            t_value,
            box[2],
            box[3],
            box[4],
            box[5],
        )

    def endpoint_carrier(row: dict[str, Any]) -> tuple[Any, ...]:
        leaf_id = row["leaf_row_id"]
        box = boxes[leaf_id]
        t_value = box[0] if row["face_side"] == "LOWER" else box[1]
        edge = row["boundary_edge"]
        if edge == "S":
            geometry = ("s", box[4], box[2], box[3])
        elif edge == "N":
            geometry = ("s", box[5], box[2], box[3])
        elif edge == "W":
            geometry = ("p", box[2], box[4], box[5])
        else:
            require(edge == "E", "endpoint edge")
            geometry = ("p", box[3], box[4], box[5])
        return identity_by_leaf[leaf_id] + (t_value,) + geometry

    endpoint_groups: dict[tuple[Any, ...], list[dict[str, Any]]] = (
        defaultdict(list)
    )
    for row in endpoints:
        endpoint_groups[endpoint_carrier(row)].append(row)
    endpoint_leaf_pairs: set[tuple[str, str]] = set()
    for grouped in endpoint_groups.values():
        leaf_ids = sorted({row["leaf_row_id"] for row in grouped})
        for index, left in enumerate(leaf_ids):
            for right in leaf_ids[index + 1:]:
                endpoint_leaf_pairs.add((left, right))

    lower_faces: dict[tuple[str, str, Q], list[str]] = defaultdict(list)
    upper_faces: dict[tuple[str, str, Q], list[str]] = defaultdict(list)
    for leaf_id, box in boxes.items():
        for axis_index, axis in enumerate("tps"):
            lower_faces[
                (parent_by_leaf[leaf_id], axis, box[2 * axis_index])
            ].append(leaf_id)
            upper_faces[
                (parent_by_leaf[leaf_id], axis, box[2 * axis_index + 1])
            ].append(leaf_id)
    for rows in lower_faces.values():
        rows.sort()
    for rows in upper_faces.values():
        rows.sort()

    ctx.prec = 256
    atlas_box = r186.r179.r174.atlas.AtlasBox
    arb_sign = r186.r179.arb_sign

    def interval_box(
        axis: str,
        coordinate: Q,
        overlaps: list[tuple[Q, Q]],
        t_side: str | None,
        path: str,
    ) -> Any:
        if axis == "p":
            (t0, t1), (s0, s1) = overlaps
            if t_side == "LOWER":
                t1 = t0
            elif t_side == "UPPER":
                t0 = t1
            return atlas_box(
                t0, t1, coordinate, coordinate, s0, s1, 0, path
            )
        require(axis == "s", "p/s interval box")
        (t0, t1), (p0, p1) = overlaps
        if t_side == "LOWER":
            t1 = t0
        elif t_side == "UPPER":
            t0 = t1
        return atlas_box(
            t0, t1, p0, p1, coordinate, coordinate, 0, path
        )

    def whole_face_proof(
        leaf_id: str,
        axis: str,
        coordinate: Q,
        overlaps: list[tuple[Q, Q]],
    ) -> dict[str, Any]:
        chart, target, active = evaluator_by_leaf[leaf_id]
        lower_box = interval_box(
            axis, coordinate, overlaps, "LOWER", "r217.lower"
        )
        upper_box = interval_box(
            axis, coordinate, overlaps, "UPPER", "r217.upper"
        )
        face_box = interval_box(
            axis, coordinate, overlaps, None, "r217.face"
        )
        lower_dual = r186.factor_geometry(chart, target, lower_box)[active]
        upper_dual = r186.factor_geometry(chart, target, upper_box)[active]
        face_dual = r186.factor_geometry(chart, target, face_box)[active]
        lower_centered = r186.centered_value(
            chart, target, lower_box, active
        )
        upper_centered = r186.centered_value(
            chart, target, upper_box, active
        )
        direct_signs = (
            arb_sign(lower_dual[0]),
            arb_sign(upper_dual[0]),
            arb_sign(face_dual[1][0]),
        )
        centered_signs = (
            arb_sign(lower_centered),
            arb_sign(upper_centered),
        )
        selected_signs = (
            (
                direct_signs[0]
                if direct_signs[0] in STRICT_SIGNS
                else centered_signs[0]
            ),
            (
                direct_signs[1]
                if direct_signs[1] in STRICT_SIGNS
                else centered_signs[1]
            ),
            direct_signs[2],
        )
        proved = (
            selected_signs[0] in STRICT_SIGNS
            and selected_signs[1] in STRICT_SIGNS
            and selected_signs[0] != selected_signs[1]
            and selected_signs[2] in STRICT_SIGNS
            and (
                (
                    selected_signs[2] == "STRICT_POSITIVE"
                    and selected_signs[:2]
                    == ("STRICT_NEGATIVE", "STRICT_POSITIVE")
                )
                or (
                    selected_signs[2] == "STRICT_NEGATIVE"
                    and selected_signs[:2]
                    == ("STRICT_POSITIVE", "STRICT_NEGATIVE")
                )
            )
        )
        return {
            "proved": proved,
            "direct_endpoint_and_full_face_dt_signs": list(direct_signs),
            "centered_endpoint_signs": list(centered_signs),
            "selected_lower_upper_and_full_face_dt_signs":
                list(selected_signs),
            "direct_lower_t_C0_enclosure": str(lower_dual[0]),
            "centered_lower_t_C0_enclosure": str(lower_centered),
            "direct_upper_t_C0_enclosure": str(upper_dual[0]),
            "centered_upper_t_C0_enclosure": str(upper_centered),
            "full_face_dt_enclosure": str(face_dual[1][0]),
            "proof_rule": (
                "STRICT_OPPOSITE_SELECTED_C0_SIGNS_ON_FULL_TRANSVERSE_"
                "ENDPOINT_EDGES_AND_STRICT_D_T_ON_ENTIRE_COMMON_FACE"
            ),
        }

    def midpoint_proof(
        leaf_id: str,
        axis: str,
        coordinate: Q,
        overlaps: list[tuple[Q, Q]],
    ) -> tuple[bool, tuple[str, str, str]]:
        chart, target, active = evaluator_by_leaf[leaf_id]
        if axis == "p":
            (t0, t1), (s0, s1) = overlaps
            other = (s0 + s1) / 2

            def make(a: Q, b: Q) -> Any:
                return atlas_box(
                    a, b, coordinate, coordinate, other, other, 0, "r217.mid"
                )
            derivative_index = 0
        elif axis == "s":
            (t0, t1), (p0, p1) = overlaps
            other = (p0 + p1) / 2

            def make(a: Q, b: Q) -> Any:
                return atlas_box(
                    a, b, other, other, coordinate, coordinate, 0, "r217.mid"
                )
            derivative_index = 0
        elif axis == "t":
            (p0, p1), (s0, s1) = overlaps
            other = (s0 + s1) / 2

            def make(a: Q, b: Q) -> Any:
                return atlas_box(
                    coordinate, coordinate, a, b, other, other, 0, "r217.mid"
                )
            t0, t1 = p0, p1
            derivative_index = 1
        else:
            raise Round217Error("midpoint axis")
        lower = r186.factor_geometry(chart, target, make(t0, t0))[active]
        upper = r186.factor_geometry(chart, target, make(t1, t1))[active]
        line = r186.factor_geometry(chart, target, make(t0, t1))[active]
        signs = (
            arb_sign(lower[0]),
            arb_sign(upper[0]),
            arb_sign(line[1][derivative_index]),
        )
        return (
            signs[0] in STRICT_SIGNS
            and signs[1] in STRICT_SIGNS
            and signs[0] != signs[1]
            and signs[2] in STRICT_SIGNS,
            signs,
        )

    trace_rows_by_id: dict[str, dict[str, Any]] = {}
    incidence_rows_by_id: dict[str, dict[str, Any]] = {}
    glue_rows: list[dict[str, Any]] = []
    exact_frontier_rows: list[dict[str, Any]] = []
    partial_unresolved_rows: list[dict[str, Any]] = []
    touch_counts: Counter[str] = Counter()
    feasibility_counts: Counter[str] = Counter()
    full_trace_counts: Counter[str] = Counter()
    exact_frontier_counts: Counter[str] = Counter()
    accepted_contacts_per_ordinal: Counter[int] = Counter()
    exact_frontier_per_ordinal: Counter[int] = Counter()
    trace_contact_multiplicity: Counter[str] = Counter()
    positive_contact_count = 0
    exact_p_s_count = 0
    partial_count = 0

    print("Round217 enumerating common-face contacts", file=sys.stderr)
    for key in sorted(lower_faces, key=lambda item: tuple(map(str, item))):
        _parent, axis, coordinate = key
        axis_index = "tps".index(axis)
        other_axes = [index for index in range(3) if index != axis_index]
        for negative_leaf in upper_faces.get(key, []):
            for positive_leaf in lower_faces[key]:
                if (
                    negative_leaf == positive_leaf
                    or identity_by_leaf[negative_leaf]
                    != identity_by_leaf[positive_leaf]
                ):
                    continue
                negative_box = boxes[negative_leaf]
                positive_box = boxes[positive_leaf]
                overlaps = [
                    (
                        max(
                            negative_box[2 * index],
                            positive_box[2 * index],
                        ),
                        min(
                            negative_box[2 * index + 1],
                            positive_box[2 * index + 1],
                        ),
                    )
                    for index in other_axes
                ]
                if any(lower > upper for lower, upper in overlaps):
                    continue
                dimension = sum(lower < upper for lower, upper in overlaps)
                exact = all(
                    negative_box[2 * index:2 * index + 2]
                    == positive_box[2 * index:2 * index + 2]
                    for index in other_axes
                )
                if (
                    occurrence_by_leaf[negative_leaf]
                    == occurrence_by_leaf[positive_leaf]
                ):
                    relation = "SAME_OCCURRENCE"
                elif (
                    origin_by_leaf[negative_leaf]
                    == origin_by_leaf[positive_leaf]
                ):
                    relation = "SAME_ORIGIN_DIFFERENT_OCCURRENCE"
                else:
                    relation = "CROSS_ORIGIN"
                touch_counts[
                    f"{axis}|dimension={dimension}|"
                    f"{'EXACT' if exact else 'PARTIAL'}|{relation}"
                ] += 1
                if dimension != 2:
                    continue
                positive_contact_count += 1
                if not exact:
                    partial_count += 1

                method = "UNRESOLVED"
                midpoint_signs: tuple[str, str, str] | None = None
                pair = tuple(sorted((negative_leaf, positive_leaf)))
                if axis == "t" and exact:
                    shared = (
                        {
                            curve_carrier(row)
                            for row in curves_by_leaf[negative_leaf]
                        }
                        & {
                            curve_carrier(row)
                            for row in curves_by_leaf[positive_leaf]
                        }
                    )
                    require(bool(shared), "exact t face explicit curve carrier")
                    method = (
                        "SAFE_EXPLICIT_T_FACE_CURVE_DUPLICATE"
                        if relation == "SAME_OCCURRENCE"
                        else "CROSS_OCCURRENCE_EXACT_CURVE_CARRIER_CANDIDATE"
                    )
                else:
                    midpoint_axis = axis
                    midpoint_ok, midpoint_signs = midpoint_proof(
                        negative_leaf,
                        midpoint_axis,
                        coordinate,
                        overlaps,
                    )
                    if midpoint_ok:
                        method = "NONPROMOTIONAL_STRICT_ZERO_WITNESS"
                    elif pair in endpoint_leaf_pairs:
                        method = (
                            "NONPROMOTIONAL_EXACT_ENDPOINT_CARRIER_CANDIDATE"
                        )
                feasibility_counts[
                    f"{axis}|{'EXACT' if exact else 'PARTIAL'}|"
                    f"{relation}|{method}"
                ] += 1

                if not exact and method == "UNRESOLVED":
                    identity = {
                        "axis": axis,
                        "negative_leaf_row_id": negative_leaf,
                        "positive_leaf_row_id": positive_leaf,
                        "shared_coordinate": str(coordinate),
                        "overlaps": [
                            [str(lower), str(upper)]
                            for lower, upper in overlaps
                        ],
                    }
                    partial_unresolved_rows.append(closed_row({
                        "frontier_row_id":
                            row_id("partial-face-frontier", identity),
                        **identity,
                        "relation": relation,
                        "exact_full_face": False,
                        "midpoint_signs":
                            list(midpoint_signs) if midpoint_signs else None,
                        "missing_evidence": (
                            "NO_STRICT_MIDLINE_ZERO_WITNESS_AND_NO_EXACT_"
                            "ENDPOINT_CARRIER;PARTIAL_FACE_RESTRICTION_AND_"
                            "ENDPOINT_TO_INTERIOR_GLUE_NOT_MATERIALIZED"
                        ),
                        "formal_trace_credit": 0,
                        "formal_glue_credit": 0,
                        "component_deduplication_credit": 0,
                        "global_exact_key_disposition_credit": 0,
                    }))

                if axis not in {"p", "s"} or not exact:
                    continue
                exact_p_s_count += 1
                proof_negative = whole_face_proof(
                    negative_leaf, axis, coordinate, overlaps
                )
                proof_positive = whole_face_proof(
                    positive_leaf, axis, coordinate, overlaps
                )
                require(
                    proof_negative == proof_positive,
                    "two-sided exact restricted evaluator equality",
                )
                proof = proof_negative
                chart, target, active = evaluator_by_leaf[negative_leaf]
                transverse_axis = "s" if axis == "p" else "p"
                face_identity = {
                    "parent_id": parent_by_leaf[negative_leaf],
                    "fixed_axis": axis,
                    "shared_coordinate": str(coordinate),
                    "t_interval": [str(value) for value in overlaps[0]],
                    "transverse_axis": transverse_axis,
                    "transverse_interval":
                        [str(value) for value in overlaps[1]],
                    "source_chart": chart,
                    "target_lift": target,
                    "active_factor": active,
                    "owner_outgoing_cell":
                        sheet_by_leaf[negative_leaf]["owner_outgoing_cell"],
                    "owner_signature_core_sha256":
                        sheet_by_leaf[negative_leaf][
                            "owner_signature_core_sha256"
                        ],
                    "official_key_ordinal":
                        ordinal_by_leaf[negative_leaf],
                }
                require(
                    ordinal_by_leaf[negative_leaf]
                    == ordinal_by_leaf[positive_leaf],
                    "exact face ordinal equality",
                )
                if not proof["proved"]:
                    selected = proof[
                        "selected_lower_upper_and_full_face_dt_signs"
                    ]
                    if selected[0] == "OVERWRAP" and selected[1] == "OVERWRAP":
                        reason = (
                            "BOTH_T_BOUNDARY_RESTRICTIONS_OVERWRAP;"
                            "TWO_ENDPOINT_TO_INTERIOR_SPLITS_MISSING"
                        )
                    elif selected[0] == "OVERWRAP":
                        reason = (
                            "LOWER_T_BOUNDARY_RESTRICTION_OVERWRAPS;"
                            "ENDPOINT_TO_INTERIOR_SPLIT_MISSING"
                        )
                    elif selected[1] == "OVERWRAP":
                        reason = (
                            "UPPER_T_BOUNDARY_RESTRICTION_OVERWRAPS;"
                            "ENDPOINT_TO_INTERIOR_SPLIT_MISSING"
                        )
                    else:
                        reason = (
                            "FULL_FACE_STRICT_MONOTONE_GRAPH_CONTRACT_FAILED"
                        )
                    frontier_identity = {
                        **face_identity,
                        "negative_leaf_row_id": negative_leaf,
                        "positive_leaf_row_id": positive_leaf,
                    }
                    exact_frontier_rows.append(closed_row({
                        "frontier_row_id":
                            row_id("exact-face-frontier", frontier_identity),
                        **frontier_identity,
                        "relation": relation,
                        "whole_face_proof": proof,
                        "missing_evidence": reason,
                        "Round211_endpoint_rows_carry_exact_root_coordinate":
                            False,
                        "formal_trace_credit": 0,
                        "formal_glue_credit": 0,
                        "component_deduplication_credit": 0,
                        "whole_leaf_credit": 0,
                        "whole_origin_credit": 0,
                        "whole_original_tube_credit": 0,
                        "global_exact_key_disposition_credit": 0,
                    }))
                    exact_frontier_counts[f"{axis}|{relation}|{reason}"] += 1
                    exact_frontier_per_ordinal[
                        ordinal_by_leaf[negative_leaf]
                    ] += 1
                    continue

                trace_identity = {
                    "restricted_evaluator_and_face": face_identity,
                    "proof_rule": proof["proof_rule"],
                }
                trace_id = row_id("zero-trace", trace_identity)
                if trace_id not in trace_rows_by_id:
                    trace_rows_by_id[trace_id] = closed_row({
                        "trace_row_id": trace_id,
                        **face_identity,
                        "whole_face_zero_trace_proof": proof,
                        "restricted_function_identity_sha256":
                            digest(face_identity),
                        "trace_is_unique_graph_over_full_transverse_interval":
                            True,
                        "formal_local_internal_face_trace_credit": 1,
                        "component_deduplication_credit": 0,
                        "whole_leaf_credit": 0,
                        "whole_origin_credit": 0,
                        "whole_original_tube_credit": 0,
                        "global_component_credit": 0,
                        "global_exact_key_disposition_credit": 0,
                    })
                trace = trace_rows_by_id[trace_id]
                trace_contact_multiplicity[trace_id] += 1

                incidence_ids: list[str] = []
                for leaf_id, side, orientation in (
                    (negative_leaf, "UPPER", "POSITIVE_" + axis.upper()),
                    (positive_leaf, "LOWER", "NEGATIVE_" + axis.upper()),
                ):
                    probe_sheet = sheet_by_leaf[leaf_id]
                    formal_sheet = formal_sheets_by_probe[
                        probe_sheet["sheet_row_id"]
                    ]
                    incidence_identity = {
                        "trace_row_id": trace_id,
                        "leaf_row_id": leaf_id,
                        "leaf_face_side": side,
                        "outward_orientation": orientation,
                        "formal_Round211_sheet_row_id":
                            formal_sheet["sheet_row_id"],
                    }
                    incidence_id = row_id(
                        "zero-trace-incidence", incidence_identity
                    )
                    incidence_ids.append(incidence_id)
                    if incidence_id not in incidence_rows_by_id:
                        incidence_rows_by_id[incidence_id] = closed_row({
                            "incidence_row_id": incidence_id,
                            **incidence_identity,
                            "trace_row_sha256": trace["row_sha256"],
                            "formal_Round211_sheet_row_sha256":
                                formal_sheet["row_sha256"],
                            "probe_Round209_sheet_row_id":
                                probe_sheet["sheet_row_id"],
                            "probe_Round209_sheet_row_sha256":
                                probe_sheet["row_sha256"],
                            "origin_row_id": origin_by_leaf[leaf_id],
                            "occurrence_row_id":
                                occurrence_by_leaf[leaf_id],
                            "retained_child_row_id":
                                retained_by_leaf[leaf_id],
                            "exact_coordinate_restriction":
                                copy.deepcopy(face_identity),
                            "formal_local_internal_face_incidence_credit": 1,
                            "component_deduplication_credit": 0,
                            "whole_leaf_credit": 0,
                            "whole_origin_credit": 0,
                            "whole_original_tube_credit": 0,
                            "global_component_credit": 0,
                            "global_exact_key_disposition_credit": 0,
                        })
                negative_incidence, positive_incidence = incidence_ids
                glue_identity = {
                    "trace_row_id": trace_id,
                    "negative_side_incidence_row_id": negative_incidence,
                    "positive_side_incidence_row_id": positive_incidence,
                }
                glue_rows.append(closed_row({
                    "glue_row_id": row_id("exact-face-glue", glue_identity),
                    **glue_identity,
                    "trace_row_sha256": trace["row_sha256"],
                    "negative_side_incidence_row_sha256":
                        incidence_rows_by_id[negative_incidence]["row_sha256"],
                    "positive_side_incidence_row_sha256":
                        incidence_rows_by_id[positive_incidence]["row_sha256"],
                    "negative_side_leaf_row_id": negative_leaf,
                    "positive_side_leaf_row_id": positive_leaf,
                    "relation": relation,
                    "exact_parent_atlas_identity": True,
                    "exact_common_face_geometry": True,
                    "exact_restricted_evaluator_identity": True,
                    "common_refinement_is_the_exact_shared_face": True,
                    "joined_from_box_touch_or_signature_hash_alone": False,
                    "formal_local_common_refinement_glue_credit": 1,
                    "component_deduplication_credit": 0,
                    "whole_leaf_credit": 0,
                    "whole_origin_credit": 0,
                    "whole_original_tube_credit": 0,
                    "global_component_credit": 0,
                    "global_exact_key_disposition_credit": 0,
                }))
                full_trace_counts[f"{axis}|{relation}"] += 1
                accepted_contacts_per_ordinal[
                    ordinal_by_leaf[negative_leaf]
                ] += 1

    trace_rows = sorted(
        trace_rows_by_id.values(), key=lambda row: row["trace_row_id"]
    )
    incidence_rows = sorted(
        incidence_rows_by_id.values(),
        key=lambda row: row["incidence_row_id"],
    )
    glue_rows.sort(key=lambda row: row["glue_row_id"])
    exact_frontier_rows.sort(key=lambda row: row["frontier_row_id"])
    partial_unresolved_rows.sort(key=lambda row: row["frontier_row_id"])

    require(
        positive_contact_count == EXPECTED_POSITIVE_FACE_CONTACTS
        and exact_p_s_count == EXPECTED_EXACT_P_S_CONTACTS
        and len(glue_rows) == EXPECTED_WHOLE_FACE_TRACES
        and len(exact_frontier_rows) == EXPECTED_EXACT_P_S_FRONTIER
        and partial_count == EXPECTED_PARTIAL_CONTACTS
        and len(partial_unresolved_rows) == EXPECTED_PARTIAL_UNRESOLVED,
        "Round214/217 contact and frontier census",
    )
    require(
        len({row["glue_row_id"] for row in glue_rows}) == len(glue_rows)
        and len(trace_rows) <= len(glue_rows)
        and len(incidence_rows) <= 2 * len(glue_rows),
        "canonical trace/incidence/glue identity uniqueness",
    )
    for rows in (
        trace_rows,
        incidence_rows,
        glue_rows,
        exact_frontier_rows,
        partial_unresolved_rows,
    ):
        for row in rows:
            payload = dict(row)
            row_hash = payload.pop("row_sha256")
            require(digest(payload) == row_hash, "closed Round217 row")

    trace_by_id = {row["trace_row_id"]: row for row in trace_rows}
    incidence_by_id = {
        row["incidence_row_id"]: row for row in incidence_rows
    }
    require(
        all(
            row["trace_row_id"] in trace_by_id
            and row["trace_row_sha256"]
            == trace_by_id[row["trace_row_id"]]["row_sha256"]
            for row in incidence_rows
        )
        and all(
            row["trace_row_id"] in trace_by_id
            and row["negative_side_incidence_row_id"] in incidence_by_id
            and row["positive_side_incidence_row_id"] in incidence_by_id
            and row["trace_row_sha256"]
            == trace_by_id[row["trace_row_id"]]["row_sha256"]
            and row["negative_side_incidence_row_sha256"]
            == incidence_by_id[
                row["negative_side_incidence_row_id"]
            ]["row_sha256"]
            and row["positive_side_incidence_row_sha256"]
            == incidence_by_id[
                row["positive_side_incidence_row_id"]
            ]["row_sha256"]
            for row in glue_rows
        ),
        "exact trace-incidence-glue hash joins",
    )

    return {
        "status": STATUS,
        "verdict": (
            "FORMAL_BOUNDED_PREFIX__EXACT_FULL_FACE_P_S_ZERO_TRACES_AND_"
            "COMMON_REFINEMENT_GLUE_MATERIALIZED__PHYSICAL_COMPONENT_"
            "QUOTIENT_STILL_INCOMPLETE"
        ),
        "formal_input_binding": {
            **input_hashes,
            "Round208_strict_leaves_rebuilt": True,
            "Round211_lower_dimensional_rows_joined_to_Round209_lineages":
                True,
            "Round214_contact_taxonomy_independently_rebuilt": True,
            "Round211_or_Round214_producer_imported_or_executed": False,
            "Round186_used_as_pinned_interval_factor_evaluator": True,
        },
        "reconstructed_contact_census": {
            "positive_area_compatible_face_contact_count":
                positive_contact_count,
            "exact_p_or_s_positive_area_contact_count": exact_p_s_count,
            "partial_positive_area_contact_count": partial_count,
            "all_box_touch_count": dict(sorted(touch_counts.items())),
            "Round214_midpoint_feasibility_method_count":
                dict(sorted(feasibility_counts.items())),
            "unresolved_partial_positive_area_contact_count":
                len(partial_unresolved_rows),
            "Round214_expected_unresolved_partial_row_count":
                EXPECTED_PARTIAL_UNRESOLVED,
        },
        "formal_exact_full_face_trace_scope": {
            "accepted_contact_count": len(glue_rows),
            "unique_trace_row_count": len(trace_rows),
            "unique_incidence_row_count": len(incidence_rows),
            "glue_row_count": len(glue_rows),
            "axis_and_relation_count": dict(sorted(full_trace_counts.items())),
            "accepted_official_key_ordinal_count":
                len(accepted_contacts_per_ordinal),
            "accepted_contacts_per_official_key_ordinal": {
                str(key): value
                for key, value in sorted(accepted_contacts_per_ordinal.items())
            },
            "accepted_contacts_per_official_key_ordinal_sha256":
                digest(dict(sorted(accepted_contacts_per_ordinal.items()))),
            "accepted_contacts_per_official_key_ordinal_histogram":
                histogram(accepted_contacts_per_ordinal.values()),
            "unique_face_carrier_contact_multiplicity_histogram":
                histogram(trace_contact_multiplicity.values()),
            "acceptance_rule": (
                "EXACT_COMMON_FACE_GEOMETRY_AND_IDENTICAL_PARENT_ATLAS_"
                "RESTRICTED_EVALUATOR_PLUS_STRICT_OPPOSITE_FULL_TRANSVERSE_"
                "T_ENDPOINT_C0_SIGNS_AND_STRICT_FULL_FACE_D_T"
            ),
            "box_touch_or_signature_core_alone_accepted": False,
            "cross_occurrence_exact_common_refinement_rows_materialized":
                sum(
                    row["relation"] != "SAME_OCCURRENCE"
                    for row in glue_rows
                ),
            "physical_component_edges_promoted": 0,
        },
        "formal_internal_face_zero_trace_ledger":
            ledger(trace_rows, "trace_row_id"),
        "formal_internal_face_incidence_ledger":
            ledger(incidence_rows, "incidence_row_id"),
        "formal_exact_common_refinement_glue_ledger":
            ledger(glue_rows, "glue_row_id"),
        "exact_face_endpoint_to_interior_frontier": {
            "row_count": len(exact_frontier_rows),
            "reason_count": dict(sorted(exact_frontier_counts.items())),
            "first_failed_predicate_count": histogram(
                row["missing_evidence"] for row in exact_frontier_rows
            ),
            "rejected_official_key_ordinal_count":
                len(exact_frontier_per_ordinal),
            "rejected_contacts_per_official_key_ordinal": {
                str(key): value
                for key, value in sorted(exact_frontier_per_ordinal.items())
            },
            "rejected_contacts_per_official_key_ordinal_sha256":
                digest(dict(sorted(exact_frontier_per_ordinal.items()))),
            "rejected_contacts_per_official_key_ordinal_histogram":
                histogram(exact_frontier_per_ordinal.values()),
            "rows_sha256": digest(exact_frontier_rows),
            "row_ids_sha256": digest([
                row["frontier_row_id"] for row in exact_frontier_rows
            ]),
            "rows": exact_frontier_rows,
        },
        "partial_face_frontier": {
            "row_count": len(partial_unresolved_rows),
            "axis_histogram":
                histogram(row["axis"] for row in partial_unresolved_rows),
            "rows_sha256": digest(partial_unresolved_rows),
            "row_ids_sha256": digest([
                row["frontier_row_id"] for row in partial_unresolved_rows
            ]),
            "rows": partial_unresolved_rows,
        },
        "first_missing_frontier": {
            "exact_p_s_contacts_without_whole_face_trace_proof":
                len(exact_frontier_rows),
            "partial_p_t_contacts_without_trace_or_endpoint_carrier":
                len(partial_unresolved_rows),
            "Round211_endpoint_rows_missing_exact_root_coordinate": True,
            "endpoint_to_curve_interior_common_refinement_missing": True,
            "partial_face_curve_restriction_rows_missing": True,
            "cross_occurrence_glue_outside_the_accepted_exact_full_face_"
            "prefix_missing": True,
            "physical_component_transitive_exhaustion_missing": True,
        },
        "formal_credit_contract": {
            "formal_local_internal_face_trace_credits": len(trace_rows),
            "formal_local_internal_face_incidence_credits":
                len(incidence_rows),
            "formal_local_common_refinement_glue_credits": len(glue_rows),
            "formal_component_deduplication_credit": 0,
            "whole_leaf_credit": 0,
            "whole_origin_credit": 0,
            "whole_original_tube_credit": 0,
            "global_component_credit": 0,
            "global_fibre_credit": 0,
            "global_exact_key_disposition_credit": 0,
            "official_source_G_global_disposition_count": 0,
            "official_source_G_global_disposition_denominator":
                EXPECTED_SOURCE_G_EXACT_KEYS,
            "D02": "UNCHANGED_BLOCKED",
            "Gate5": "UNCHANGED_10/18",
            "CM2": "UNCHANGED_NO_GO",
        },
        "required_next": (
            "materialize exact root-coordinate endpoint-to-interior and "
            "partial-face restriction rows, then independently build the "
            "complete physical-component graph; no local glue row here "
            "exhausts an origin, tube, global component, or exact-key fibre"
        ),
        "provenance": {
            "schema": SCHEMA,
            "producer_sha256": producer_sha256,
            "python_version": sys.version.split()[0],
            "python_flint_version":
                getattr(__import__("flint"), "__version__", "unknown"),
            "effective_Arb_precision_bits": ctx.prec,
            "producer_imported_or_executed_by_independent_verifier": False,
            "formal_upstream_files_modified": False,
        },
    }


def validate_output(path: Path) -> Path:
    absolute = path.resolve(strict=False)
    require(absolute.parent == HERE.resolve(), "output parent")
    official = absolute.name == OUTPUT.name
    replay = (
        absolute.name.startswith(f".{PREFIX}_replay_")
        and absolute.name.endswith(".json")
        and "/" not in absolute.name
    )
    require(official or replay, "output filename")
    require(not absolute.is_symlink(), "output symlink")
    if absolute.exists():
        metadata = absolute.lstat()
        require(
            stat.S_ISREG(metadata.st_mode) and metadata.st_nlink == 1,
            "output existing regular unique",
        )
    return absolute


def safe_write(path: Path, data: bytes) -> None:
    destination = validate_output(path)
    descriptor, temporary = tempfile.mkstemp(
        prefix=f".{PREFIX}.tmp.",
        dir=HERE,
    )
    temp_path = Path(temporary)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_path, destination)
        directory = os.open(HERE, os.O_RDONLY)
        try:
            os.fsync(directory)
        finally:
            os.close(directory)
    finally:
        if temp_path.exists():
            temp_path.unlink()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    arguments = parser.parse_args()
    producer_sha256 = hashlib.sha256(
        regular_bytes(Path(__file__), 5_000_000)
    ).hexdigest()
    result = build_result(producer_sha256)
    envelope = {
        "schema": SCHEMA,
        "result": result,
        "result_sha256": digest(result),
    }
    safe_write(arguments.output, canonical_bytes(envelope) + b"\n")
    print(envelope["result_sha256"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
