#!/usr/bin/env python3
"""Independent verifier for the Round217 bounded trace/glue certificate.

The verifier never imports or executes the producer or the Round214 probe.  It
reconstructs the pinned Round208 geometry and Round211 lineage boundary,
independently enumerates every compatible face, reruns the interval proofs,
rebuilds every expected Round217 row, and demands full Python-object and
canonical-byte equality.  It also runs re-signed semantic mutations, strict
JSON attacks, and filesystem path attacks.
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
import shutil
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
PRODUCER = f"{PREFIX}.py"
CERTIFICATE = f"{PREFIX}_certificate.json"
VERIFICATION = f"{PREFIX}_verification.json"
SCHEMA = "cm2.round217.source-g-internal-face-trace-glue-materialization.v1"
VERIFICATION_SCHEMA = (
    "cm2.round217.source-g-internal-face-trace-glue-verification.v1"
)
STATUS = (
    "CERTIFIED_BOUNDED_EXACT_P_S_INTERNAL_FACE_ZERO_TRACE_AND_GLUE_ROWS__"
    "PHYSICAL_COMPONENT_AND_GLOBAL_FIBRE_INCOMPLETE"
)
VERDICT = (
    "FORMAL_BOUNDED_PREFIX__EXACT_FULL_FACE_P_S_ZERO_TRACES_AND_"
    "COMMON_REFINEMENT_GLUE_MATERIALIZED__PHYSICAL_COMPONENT_"
    "QUOTIENT_STILL_INCOMPLETE"
)
PRODUCER_SHA256 = (
    "687fd48134e204a99c807e1fd18954cef7633879396db5f4d291ece1568dfa66"
)
CERTIFICATE_SHA256 = (
    "1ccf9b4bf65bb4f45603594ea19f47e3b2103ea682bebfff0b023234308938fd"
)
RESULT_SHA256 = (
    "fb4519a43f76cbc765e24b3cb0a0e25267d9664091e22139913f3899fd1e2286"
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
R186_SOURCE = "cm2_round186_source_g_factor_face_probe.py"
R186_SOURCE_SHA256 = (
    "5797b8f4c2ba9c8c5b42b32511f3c97a15469b59bdf00cd8430580c3429c7c64"
)

MAX_INPUT_BYTES = 300 * 1024 * 1024
EXPECTED_LEAVES = 18_324
EXPECTED_REGIONS = 36_040
EXPECTED_SHEETS = 17_716
EXPECTED_CURVES = 20_456
EXPECTED_ENDPOINTS = 40_912
EXPECTED_POSITIVE = 15_540
EXPECTED_EXACT_PS = 7_932
EXPECTED_ACCEPTED = 448
EXPECTED_EXACT_FRONTIER = 7_484
EXPECTED_PARTIAL = 644
EXPECTED_PARTIAL_FRONTIER = 264
EXPECTED_SOURCE_G_KEYS = 224_580
STRICT_SIGNS = {"STRICT_NEGATIVE", "STRICT_POSITIVE"}


class VerificationError(RuntimeError):
    pass


def require(condition: bool, label: str) -> None:
    if not condition:
        raise VerificationError(label)


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


def closed(payload: dict[str, Any]) -> dict[str, Any]:
    value = copy.deepcopy(payload)
    value["row_sha256"] = digest(value)
    return value


def histogram(values: Iterable[Any]) -> dict[str, int]:
    return dict(sorted(Counter(str(value) for value in values).items()))


def identity_id(kind: str, payload: dict[str, Any]) -> str:
    return f"round217-{kind}:{digest(payload)}"


def reject_duplicate_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, item in pairs:
        require(key not in value, f"duplicate JSON key:{key}")
        value[key] = item
    return value


def reject_constant(value: str) -> None:
    raise VerificationError(f"nonfinite JSON constant:{value}")


def strict_json(raw: bytes, maximum: int = MAX_INPUT_BYTES) -> Any:
    require(0 < len(raw) <= maximum, "JSON size")
    require(not raw.startswith(b"\xef\xbb\xbf"), "JSON BOM")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as error:
        raise VerificationError("JSON UTF-8") from error
    try:
        value = json.loads(
            text,
            object_pairs_hook=reject_duplicate_pairs,
            parse_constant=reject_constant,
        )
    except (json.JSONDecodeError, UnicodeDecodeError) as error:
        raise VerificationError("strict JSON parse") from error
    require(isinstance(value, dict), "JSON top object")
    try:
        expected = canonical_bytes(value) + b"\n"
    except UnicodeEncodeError as error:
        raise VerificationError("JSON Unicode scalar") from error
    require(expected == raw, "canonical JSON bytes")
    return value


def secure_bytes(
    path: Path,
    maximum: int,
    expected_parent: Path,
    expected_name: str,
) -> bytes:
    require(path.name == expected_name, "input filename")
    require(path.resolve(strict=False).parent == expected_parent.resolve(),
            "input parent")
    before = path.lstat()
    require(stat.S_ISREG(before.st_mode), "input regular")
    require(not path.is_symlink(), "input symlink")
    require(before.st_nlink == 1, "input hardlink")
    require(0 < before.st_size <= maximum, "input size")
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
            "input stable open",
        )
        parts: list[bytes] = []
        total = 0
        while True:
            part = os.read(descriptor, 1024 * 1024)
            if not part:
                break
            total += len(part)
            require(total <= maximum, "input bounded read")
            parts.append(part)
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
            "input stable read",
        )
        return b"".join(parts)
    finally:
        os.close(descriptor)


def pinned(path: Path, expected: str, maximum: int) -> bytes:
    raw = secure_bytes(path, maximum, HERE, path.name)
    require(hashlib.sha256(raw).hexdigest() == expected,
            f"input SHA256:{path.name}")
    return raw


def verify_closed_rows(
    rows: list[dict[str, Any]],
    id_key: str,
    claimed: dict[str, Any],
) -> None:
    require(
        claimed["row_count"] == len(rows)
        and claimed["rows_sha256"] == digest(rows)
        and claimed["row_ids_sha256"]
        == digest([row[id_key] for row in rows])
        and claimed["row_hashes_sha256"]
        == digest([row["row_sha256"] for row in rows])
        and claimed["every_row_closed_by_own_SHA256"] is True,
        f"ledger closure:{id_key}",
    )
    require(len({row[id_key] for row in rows}) == len(rows),
            f"unique IDs:{id_key}")
    for row in rows:
        payload = dict(row)
        row_hash = payload.pop("row_sha256")
        require(digest(payload) == row_hash, f"row closure:{id_key}")


def make_ledger(rows: list[dict[str, Any]], id_key: str) -> dict[str, Any]:
    return {
        "row_count": len(rows),
        "rows_sha256": digest(rows),
        "row_ids_sha256": digest([row[id_key] for row in rows]),
        "row_hashes_sha256": digest([row["row_sha256"] for row in rows]),
        "every_row_closed_by_own_SHA256": True,
        "rows": rows,
    }


def reconstruct_expected_result() -> dict[str, Any]:
    require(
        Path(r209.__file__).resolve() == (HERE / R209_SOURCE).resolve()
        and Path(r186.__file__).resolve() == (HERE / R186_SOURCE).resolve(),
        "upstream module identity",
    )
    pinned(HERE / R204_SOURCE, R204_SOURCE_SHA256, 5_000_000)
    raw204 = pinned(
        HERE / R204_CERTIFICATE, R204_CERTIFICATE_SHA256, 20_000_000
    )
    pinned(HERE / R208_SOURCE, R208_SOURCE_SHA256, 5_000_000)
    raw208 = pinned(
        HERE / R208_CERTIFICATE, R208_CERTIFICATE_SHA256, MAX_INPUT_BYTES
    )
    pinned(HERE / R209_SOURCE, R209_SOURCE_SHA256, 5_000_000)
    pinned(HERE / R211_SOURCE, R211_SOURCE_SHA256, 5_000_000)
    raw211 = pinned(
        HERE / R211_CERTIFICATE, R211_CERTIFICATE_SHA256, MAX_INPUT_BYTES
    )
    pinned(HERE / R214_SOURCE, R214_SOURCE_SHA256, 5_000_000)
    pinned(HERE / R214_REPORT, R214_REPORT_SHA256, 5_000_000)
    pinned(HERE / R186_SOURCE, R186_SOURCE_SHA256, 5_000_000)

    for raw, expected, label in (
        (raw204, R204_RESULT_SHA256, "Round204"),
        (raw208, R208_RESULT_SHA256, "Round208"),
        (raw211, R211_RESULT_SHA256, "Round211"),
    ):
        envelope = strict_json(raw)
        require(
            envelope["result_sha256"] == expected
            and digest(envelope["result"]) == expected,
            f"{label} result closure",
        )
    certificate204 = strict_json(raw204)
    certificate211 = strict_json(raw211)
    require(
        len(
            certificate204["result"]["exact_key_local_join_ledger"][
                "official_key_ordinals"
            ]
        ) == 12,
        "Round204 12 ordinals",
    )

    _r173, result208, upstream_hashes = r209.validate_inputs()
    require(
        upstream_hashes["Round208_producer_source_sha256"]
        == R208_SOURCE_SHA256
        and upstream_hashes["Round208_certificate_sha256"]
        == R208_CERTIFICATE_SHA256
        and upstream_hashes["Round208_result_sha256"]
        == R208_RESULT_SHA256,
        "Round208 direct boundary",
    )
    leaves, regions, _faces, _u2 = r209.validate_round195_geometry(result208)
    sheets, curves, endpoints, _audit = r209.build_lineages(leaves, regions)
    require(
        (len(leaves), len(regions), len(sheets), len(curves), len(endpoints))
        == (
            EXPECTED_LEAVES,
            EXPECTED_REGIONS,
            EXPECTED_SHEETS,
            EXPECTED_CURVES,
            EXPECTED_ENDPOINTS,
        ),
        "independent dimensional census",
    )
    formal_sheet_rows = certificate211["result"][
        "formal_2D_sheet_owner_ledger"
    ]["rows"]
    formal_sheets = {
        row["probe_sheet_row_id"]: row for row in formal_sheet_rows
    }
    require(
        {
            key: value["probe_sheet_row_sha256"]
            for key, value in formal_sheets.items()
        }
        == {row["sheet_row_id"]: row["row_sha256"] for row in sheets},
        "independent Round211 sheet lineage",
    )
    require(
        {
            row["probe_curve_row_id"]: row["probe_curve_row_sha256"]
            for row in certificate211["result"][
                "formal_1D_curve_incidence_owner_ledger"
            ]["rows"]
        }
        == {row["curve_row_id"]: row["row_sha256"] for row in curves}
        and {
            row["probe_endpoint_row_id"]:
                row["probe_endpoint_row_sha256"]
            for row in certificate211["result"][
                "formal_0D_endpoint_incidence_owner_ledger"
            ]["rows"]
        }
        == {row["endpoint_row_id"]: row["row_sha256"] for row in endpoints},
        "independent Round211 lower lineage",
    )

    leaves_by_id = {row["leaf_row_id"]: row for row in leaves}
    regions_by_id = {row["region_row_id"]: row for row in regions}
    sheets_by_leaf = {row["leaf_row_id"]: row for row in sheets}
    boxes = {
        leaf: tuple(Q(value) for value in leaves_by_id[leaf]["box"])
        for leaf in sheets_by_leaf
    }
    parents = {
        row["leaf_row_id"]: row["parent_id"]
        for row in regions
        if row["leaf_row_id"] in sheets_by_leaf
    }
    occurrences = {
        leaf: row["occurrence_row_id"] for leaf, row in sheets_by_leaf.items()
    }
    origins = {
        leaf: row["origin_row_id"] for leaf, row in sheets_by_leaf.items()
    }
    retained = {
        leaf: row["retained_child_row_id"]
        for leaf, row in sheets_by_leaf.items()
    }
    identities: dict[str, tuple[Any, ...]] = {}
    evaluators: dict[str, tuple[str, str, str]] = {}
    ordinals: dict[str, int] = {}
    for leaf, sheet in sheets_by_leaf.items():
        signature = regions_by_id[
            sheet["owner_region_row_id"]
        ]["local_return_signature"]
        identities[leaf] = (
            parents[leaf],
            signature["source_chart"],
            signature["target_lift"],
            tuple(signature["signed_wall_word"]),
            signature["roof"],
            sheet["active_factor"],
            sheet["owner_outgoing_cell"],
            sheet["owner_signature_core_sha256"],
        )
        evaluators[leaf] = (
            signature["source_chart"],
            signature["target_lift"],
            sheet["active_factor"],
        )
        ordinals[leaf] = signature["official_key_ordinal"]

    curves_by_leaf: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in curves:
        curves_by_leaf[row["leaf_row_id"]].append(row)

    def curve_key(row: dict[str, Any]) -> tuple[Any, ...]:
        leaf = row["leaf_row_id"]
        box = boxes[leaf]
        fixed_t = box[0] if row["face_side"] == "LOWER" else box[1]
        return identities[leaf] + (
            fixed_t,
            box[2],
            box[3],
            box[4],
            box[5],
        )

    def endpoint_key(row: dict[str, Any]) -> tuple[Any, ...]:
        leaf = row["leaf_row_id"]
        box = boxes[leaf]
        fixed_t = box[0] if row["face_side"] == "LOWER" else box[1]
        edge = row["boundary_edge"]
        if edge == "S":
            extra = ("s", box[4], box[2], box[3])
        elif edge == "N":
            extra = ("s", box[5], box[2], box[3])
        elif edge == "W":
            extra = ("p", box[2], box[4], box[5])
        else:
            require(edge == "E", "endpoint edge")
            extra = ("p", box[3], box[4], box[5])
        return identities[leaf] + (fixed_t,) + extra

    endpoint_groups: dict[tuple[Any, ...], set[str]] = defaultdict(set)
    for endpoint in endpoints:
        endpoint_groups[endpoint_key(endpoint)].add(endpoint["leaf_row_id"])
    endpoint_pairs: set[tuple[str, str]] = set()
    for leaves_on_carrier in endpoint_groups.values():
        ordered = sorted(leaves_on_carrier)
        endpoint_pairs.update(
            (left, right)
            for index, left in enumerate(ordered)
            for right in ordered[index + 1:]
        )

    low_faces: dict[tuple[str, str, Q], list[str]] = defaultdict(list)
    high_faces: dict[tuple[str, str, Q], list[str]] = defaultdict(list)
    for leaf, box in boxes.items():
        for index, axis in enumerate("tps"):
            low_faces[(parents[leaf], axis, box[2 * index])].append(leaf)
            high_faces[
                (parents[leaf], axis, box[2 * index + 1])
            ].append(leaf)
    for values in low_faces.values():
        values.sort()
    for values in high_faces.values():
        values.sort()

    ctx.prec = 256
    atlas_box = r186.r179.r174.atlas.AtlasBox
    arb_sign = r186.r179.arb_sign

    def face_box(
        axis: str,
        coordinate: Q,
        overlaps: list[tuple[Q, Q]],
        t_side: str | None,
    ) -> Any:
        if axis == "p":
            (t0, t1), (s0, s1) = overlaps
            if t_side == "LOWER":
                t1 = t0
            if t_side == "UPPER":
                t0 = t1
            return atlas_box(
                t0, t1, coordinate, coordinate, s0, s1, 0, "verify"
            )
        require(axis == "s", "face box p/s")
        (t0, t1), (p0, p1) = overlaps
        if t_side == "LOWER":
            t1 = t0
        if t_side == "UPPER":
            t0 = t1
        return atlas_box(
            t0, t1, p0, p1, coordinate, coordinate, 0, "verify"
        )

    def full_proof(
        leaf: str,
        axis: str,
        coordinate: Q,
        overlaps: list[tuple[Q, Q]],
    ) -> dict[str, Any]:
        chart, target, active = evaluators[leaf]
        lower_box = face_box(axis, coordinate, overlaps, "LOWER")
        upper_box = face_box(axis, coordinate, overlaps, "UPPER")
        entire_box = face_box(axis, coordinate, overlaps, None)
        lower = r186.factor_geometry(chart, target, lower_box)[active]
        upper = r186.factor_geometry(chart, target, upper_box)[active]
        entire = r186.factor_geometry(chart, target, entire_box)[active]
        lower_center = r186.centered_value(chart, target, lower_box, active)
        upper_center = r186.centered_value(chart, target, upper_box, active)
        direct = (
            arb_sign(lower[0]),
            arb_sign(upper[0]),
            arb_sign(entire[1][0]),
        )
        centered = (arb_sign(lower_center), arb_sign(upper_center))
        selected = (
            direct[0] if direct[0] in STRICT_SIGNS else centered[0],
            direct[1] if direct[1] in STRICT_SIGNS else centered[1],
            direct[2],
        )
        proved = (
            (
                selected
                == (
                    "STRICT_NEGATIVE",
                    "STRICT_POSITIVE",
                    "STRICT_POSITIVE",
                )
            )
            or (
                selected
                == (
                    "STRICT_POSITIVE",
                    "STRICT_NEGATIVE",
                    "STRICT_NEGATIVE",
                )
            )
        )
        return {
            "proved": proved,
            "direct_endpoint_and_full_face_dt_signs": list(direct),
            "centered_endpoint_signs": list(centered),
            "selected_lower_upper_and_full_face_dt_signs": list(selected),
            "direct_lower_t_C0_enclosure": str(lower[0]),
            "centered_lower_t_C0_enclosure": str(lower_center),
            "direct_upper_t_C0_enclosure": str(upper[0]),
            "centered_upper_t_C0_enclosure": str(upper_center),
            "full_face_dt_enclosure": str(entire[1][0]),
            "proof_rule": (
                "STRICT_OPPOSITE_SELECTED_C0_SIGNS_ON_FULL_TRANSVERSE_"
                "ENDPOINT_EDGES_AND_STRICT_D_T_ON_ENTIRE_COMMON_FACE"
            ),
        }

    def midpoint_proof(
        leaf: str,
        axis: str,
        coordinate: Q,
        overlaps: list[tuple[Q, Q]],
    ) -> tuple[bool, tuple[str, str, str]]:
        chart, target, active = evaluators[leaf]
        if axis == "p":
            (a0, a1), (b0, b1) = overlaps
            other = (b0 + b1) / 2

            def make(lo: Q, hi: Q) -> Any:
                return atlas_box(
                    lo, hi, coordinate, coordinate, other, other, 0, "verify"
                )
            derivative = 0
        elif axis == "s":
            (a0, a1), (b0, b1) = overlaps
            other = (b0 + b1) / 2

            def make(lo: Q, hi: Q) -> Any:
                return atlas_box(
                    lo, hi, other, other, coordinate, coordinate, 0, "verify"
                )
            derivative = 0
        else:
            require(axis == "t", "midpoint axis")
            (a0, a1), (b0, b1) = overlaps
            other = (b0 + b1) / 2

            def make(lo: Q, hi: Q) -> Any:
                return atlas_box(
                    coordinate, coordinate, lo, hi, other, other, 0, "verify"
                )
            derivative = 1
        lower = r186.factor_geometry(chart, target, make(a0, a0))[active]
        upper = r186.factor_geometry(chart, target, make(a1, a1))[active]
        line = r186.factor_geometry(chart, target, make(a0, a1))[active]
        signs = (
            arb_sign(lower[0]),
            arb_sign(upper[0]),
            arb_sign(line[1][derivative]),
        )
        return (
            signs[0] in STRICT_SIGNS
            and signs[1] in STRICT_SIGNS
            and signs[0] != signs[1]
            and signs[2] in STRICT_SIGNS,
            signs,
        )

    expected_traces: dict[str, dict[str, Any]] = {}
    expected_incidences: dict[str, dict[str, Any]] = {}
    expected_glues: list[dict[str, Any]] = []
    expected_exact_frontier: list[dict[str, Any]] = []
    expected_partial_frontier: list[dict[str, Any]] = []
    touch_counts: Counter[str] = Counter()
    feasibility: Counter[str] = Counter()
    accepted_axis_relation: Counter[str] = Counter()
    rejected_axis_reason: Counter[str] = Counter()
    accepted_ordinals: Counter[int] = Counter()
    rejected_ordinals: Counter[int] = Counter()
    trace_multiplicity: Counter[str] = Counter()
    positive_count = 0
    exact_ps_count = 0
    partial_count = 0

    for key in sorted(low_faces, key=lambda item: tuple(map(str, item))):
        _parent, axis, coordinate = key
        axis_index = "tps".index(axis)
        other_indices = [index for index in range(3) if index != axis_index]
        for negative_leaf in high_faces.get(key, []):
            for positive_leaf in low_faces[key]:
                if (
                    negative_leaf == positive_leaf
                    or identities[negative_leaf] != identities[positive_leaf]
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
                    for index in other_indices
                ]
                if any(lower > upper for lower, upper in overlaps):
                    continue
                dimension = sum(lower < upper for lower, upper in overlaps)
                exact = all(
                    negative_box[2 * index:2 * index + 2]
                    == positive_box[2 * index:2 * index + 2]
                    for index in other_indices
                )
                if occurrences[negative_leaf] == occurrences[positive_leaf]:
                    relation = "SAME_OCCURRENCE"
                elif origins[negative_leaf] == origins[positive_leaf]:
                    relation = "SAME_ORIGIN_DIFFERENT_OCCURRENCE"
                else:
                    relation = "CROSS_ORIGIN"
                touch_counts[
                    f"{axis}|dimension={dimension}|"
                    f"{'EXACT' if exact else 'PARTIAL'}|{relation}"
                ] += 1
                if dimension != 2:
                    continue
                positive_count += 1
                if not exact:
                    partial_count += 1

                midpoint_signs: tuple[str, str, str] | None = None
                pair = tuple(sorted((negative_leaf, positive_leaf)))
                if axis == "t" and exact:
                    shared = (
                        {curve_key(row) for row in curves_by_leaf[negative_leaf]}
                        & {curve_key(row) for row in curves_by_leaf[positive_leaf]}
                    )
                    require(shared, "independent exact t carrier")
                    method = (
                        "SAFE_EXPLICIT_T_FACE_CURVE_DUPLICATE"
                        if relation == "SAME_OCCURRENCE"
                        else "CROSS_OCCURRENCE_EXACT_CURVE_CARRIER_CANDIDATE"
                    )
                else:
                    midpoint_ok, midpoint_signs = midpoint_proof(
                        negative_leaf, axis, coordinate, overlaps
                    )
                    if midpoint_ok:
                        method = "NONPROMOTIONAL_STRICT_ZERO_WITNESS"
                    elif pair in endpoint_pairs:
                        method = (
                            "NONPROMOTIONAL_EXACT_ENDPOINT_CARRIER_CANDIDATE"
                        )
                    else:
                        method = "UNRESOLVED"
                feasibility[
                    f"{axis}|{'EXACT' if exact else 'PARTIAL'}|"
                    f"{relation}|{method}"
                ] += 1

                if not exact and method == "UNRESOLVED":
                    frontier_identity = {
                        "axis": axis,
                        "negative_leaf_row_id": negative_leaf,
                        "positive_leaf_row_id": positive_leaf,
                        "shared_coordinate": str(coordinate),
                        "overlaps": [
                            [str(lower), str(upper)]
                            for lower, upper in overlaps
                        ],
                    }
                    expected_partial_frontier.append(closed({
                        "frontier_row_id":
                            identity_id(
                                "partial-face-frontier", frontier_identity
                            ),
                        **frontier_identity,
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
                exact_ps_count += 1
                proof_left = full_proof(
                    negative_leaf, axis, coordinate, overlaps
                )
                proof_right = full_proof(
                    positive_leaf, axis, coordinate, overlaps
                )
                require(proof_left == proof_right,
                        "independent restricted evaluator equality")
                proof = proof_left
                chart, target, active = evaluators[negative_leaf]
                require(
                    ordinals[negative_leaf] == ordinals[positive_leaf],
                    "independent ordinal equality",
                )
                face_identity = {
                    "parent_id": parents[negative_leaf],
                    "fixed_axis": axis,
                    "shared_coordinate": str(coordinate),
                    "t_interval": [str(value) for value in overlaps[0]],
                    "transverse_axis": "s" if axis == "p" else "p",
                    "transverse_interval":
                        [str(value) for value in overlaps[1]],
                    "source_chart": chart,
                    "target_lift": target,
                    "active_factor": active,
                    "owner_outgoing_cell":
                        sheets_by_leaf[negative_leaf]["owner_outgoing_cell"],
                    "owner_signature_core_sha256":
                        sheets_by_leaf[negative_leaf][
                            "owner_signature_core_sha256"
                        ],
                    "official_key_ordinal": ordinals[negative_leaf],
                }
                if not proof["proved"]:
                    selected = proof[
                        "selected_lower_upper_and_full_face_dt_signs"
                    ]
                    if selected[0] == selected[1] == "OVERWRAP":
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
                    expected_exact_frontier.append(closed({
                        "frontier_row_id":
                            identity_id(
                                "exact-face-frontier", frontier_identity
                            ),
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
                    rejected_axis_reason[
                        f"{axis}|{relation}|{reason}"
                    ] += 1
                    rejected_ordinals[ordinals[negative_leaf]] += 1
                    continue

                trace_identity = {
                    "restricted_evaluator_and_face": face_identity,
                    "proof_rule": proof["proof_rule"],
                }
                trace_id = identity_id("zero-trace", trace_identity)
                if trace_id not in expected_traces:
                    expected_traces[trace_id] = closed({
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
                trace = expected_traces[trace_id]
                trace_multiplicity[trace_id] += 1

                incidence_ids: list[str] = []
                for leaf, side, orientation in (
                    (negative_leaf, "UPPER", "POSITIVE_" + axis.upper()),
                    (positive_leaf, "LOWER", "NEGATIVE_" + axis.upper()),
                ):
                    probe_sheet = sheets_by_leaf[leaf]
                    formal_sheet = formal_sheets[probe_sheet["sheet_row_id"]]
                    incidence_identity = {
                        "trace_row_id": trace_id,
                        "leaf_row_id": leaf,
                        "leaf_face_side": side,
                        "outward_orientation": orientation,
                        "formal_Round211_sheet_row_id":
                            formal_sheet["sheet_row_id"],
                    }
                    incidence_id = identity_id(
                        "zero-trace-incidence", incidence_identity
                    )
                    incidence_ids.append(incidence_id)
                    if incidence_id not in expected_incidences:
                        expected_incidences[incidence_id] = closed({
                            "incidence_row_id": incidence_id,
                            **incidence_identity,
                            "trace_row_sha256": trace["row_sha256"],
                            "formal_Round211_sheet_row_sha256":
                                formal_sheet["row_sha256"],
                            "probe_Round209_sheet_row_id":
                                probe_sheet["sheet_row_id"],
                            "probe_Round209_sheet_row_sha256":
                                probe_sheet["row_sha256"],
                            "origin_row_id": origins[leaf],
                            "occurrence_row_id": occurrences[leaf],
                            "retained_child_row_id": retained[leaf],
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
                expected_glues.append(closed({
                    "glue_row_id":
                        identity_id("exact-face-glue", glue_identity),
                    **glue_identity,
                    "trace_row_sha256": trace["row_sha256"],
                    "negative_side_incidence_row_sha256":
                        expected_incidences[negative_incidence]["row_sha256"],
                    "positive_side_incidence_row_sha256":
                        expected_incidences[positive_incidence]["row_sha256"],
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
                accepted_axis_relation[f"{axis}|{relation}"] += 1
                accepted_ordinals[ordinals[negative_leaf]] += 1

    trace_rows = sorted(
        expected_traces.values(), key=lambda row: row["trace_row_id"]
    )
    incidence_rows = sorted(
        expected_incidences.values(), key=lambda row: row["incidence_row_id"]
    )
    expected_glues.sort(key=lambda row: row["glue_row_id"])
    expected_exact_frontier.sort(key=lambda row: row["frontier_row_id"])
    expected_partial_frontier.sort(key=lambda row: row["frontier_row_id"])
    require(
        positive_count == EXPECTED_POSITIVE
        and exact_ps_count == EXPECTED_EXACT_PS
        and len(expected_glues) == EXPECTED_ACCEPTED
        and len(expected_exact_frontier) == EXPECTED_EXACT_FRONTIER
        and partial_count == EXPECTED_PARTIAL
        and len(expected_partial_frontier) == EXPECTED_PARTIAL_FRONTIER,
        "independent exact census",
    )

    input_hashes = {
        "Round208_certificate_sha256": R208_CERTIFICATE_SHA256,
        "Round208_result_sha256": R208_RESULT_SHA256,
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
    expected = {
        "status": STATUS,
        "verdict": VERDICT,
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
            "positive_area_compatible_face_contact_count": positive_count,
            "exact_p_or_s_positive_area_contact_count": exact_ps_count,
            "partial_positive_area_contact_count": partial_count,
            "all_box_touch_count": dict(sorted(touch_counts.items())),
            "Round214_midpoint_feasibility_method_count":
                dict(sorted(feasibility.items())),
            "unresolved_partial_positive_area_contact_count":
                len(expected_partial_frontier),
            "Round214_expected_unresolved_partial_row_count":
                EXPECTED_PARTIAL_FRONTIER,
        },
        "formal_exact_full_face_trace_scope": {
            "accepted_contact_count": len(expected_glues),
            "unique_trace_row_count": len(trace_rows),
            "unique_incidence_row_count": len(incidence_rows),
            "glue_row_count": len(expected_glues),
            "axis_and_relation_count":
                dict(sorted(accepted_axis_relation.items())),
            "accepted_official_key_ordinal_count": len(accepted_ordinals),
            "accepted_contacts_per_official_key_ordinal": {
                str(key): value
                for key, value in sorted(accepted_ordinals.items())
            },
            "accepted_contacts_per_official_key_ordinal_sha256":
                digest(dict(sorted(accepted_ordinals.items()))),
            "accepted_contacts_per_official_key_ordinal_histogram":
                histogram(accepted_ordinals.values()),
            "unique_face_carrier_contact_multiplicity_histogram":
                histogram(trace_multiplicity.values()),
            "acceptance_rule": (
                "EXACT_COMMON_FACE_GEOMETRY_AND_IDENTICAL_PARENT_ATLAS_"
                "RESTRICTED_EVALUATOR_PLUS_STRICT_OPPOSITE_FULL_TRANSVERSE_"
                "T_ENDPOINT_C0_SIGNS_AND_STRICT_FULL_FACE_D_T"
            ),
            "box_touch_or_signature_core_alone_accepted": False,
            "cross_occurrence_exact_common_refinement_rows_materialized":
                sum(
                    row["relation"] != "SAME_OCCURRENCE"
                    for row in expected_glues
                ),
            "physical_component_edges_promoted": 0,
        },
        "formal_internal_face_zero_trace_ledger":
            make_ledger(trace_rows, "trace_row_id"),
        "formal_internal_face_incidence_ledger":
            make_ledger(incidence_rows, "incidence_row_id"),
        "formal_exact_common_refinement_glue_ledger":
            make_ledger(expected_glues, "glue_row_id"),
        "exact_face_endpoint_to_interior_frontier": {
            "row_count": len(expected_exact_frontier),
            "reason_count": dict(sorted(rejected_axis_reason.items())),
            "first_failed_predicate_count": histogram(
                row["missing_evidence"] for row in expected_exact_frontier
            ),
            "rejected_official_key_ordinal_count": len(rejected_ordinals),
            "rejected_contacts_per_official_key_ordinal": {
                str(key): value
                for key, value in sorted(rejected_ordinals.items())
            },
            "rejected_contacts_per_official_key_ordinal_sha256":
                digest(dict(sorted(rejected_ordinals.items()))),
            "rejected_contacts_per_official_key_ordinal_histogram":
                histogram(rejected_ordinals.values()),
            "rows_sha256": digest(expected_exact_frontier),
            "row_ids_sha256": digest([
                row["frontier_row_id"] for row in expected_exact_frontier
            ]),
            "rows": expected_exact_frontier,
        },
        "partial_face_frontier": {
            "row_count": len(expected_partial_frontier),
            "axis_histogram":
                histogram(row["axis"] for row in expected_partial_frontier),
            "rows_sha256": digest(expected_partial_frontier),
            "row_ids_sha256": digest([
                row["frontier_row_id"] for row in expected_partial_frontier
            ]),
            "rows": expected_partial_frontier,
        },
        "first_missing_frontier": {
            "exact_p_s_contacts_without_whole_face_trace_proof":
                len(expected_exact_frontier),
            "partial_p_t_contacts_without_trace_or_endpoint_carrier":
                len(expected_partial_frontier),
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
            "formal_local_common_refinement_glue_credits":
                len(expected_glues),
            "formal_component_deduplication_credit": 0,
            "whole_leaf_credit": 0,
            "whole_origin_credit": 0,
            "whole_original_tube_credit": 0,
            "global_component_credit": 0,
            "global_fibre_credit": 0,
            "global_exact_key_disposition_credit": 0,
            "official_source_G_global_disposition_count": 0,
            "official_source_G_global_disposition_denominator":
                EXPECTED_SOURCE_G_KEYS,
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
            "producer_sha256": PRODUCER_SHA256,
            "python_version": sys.version.split()[0],
            "python_flint_version":
                getattr(__import__("flint"), "__version__", "unknown"),
            "effective_Arb_precision_bits": ctx.prec,
            "producer_imported_or_executed_by_independent_verifier": False,
            "formal_upstream_files_modified": False,
        },
    }
    return expected


def verify_envelope(envelope: Any, expected_result: dict[str, Any]) -> None:
    require(
        isinstance(envelope, dict)
        and set(envelope) == {"schema", "result", "result_sha256"}
        and envelope["schema"] == SCHEMA,
        "certificate envelope schema",
    )
    result = envelope["result"]
    require(
        isinstance(result, dict)
        and envelope["result_sha256"] == digest(result),
        "certificate result closure",
    )
    for key, id_key in (
        ("formal_internal_face_zero_trace_ledger", "trace_row_id"),
        ("formal_internal_face_incidence_ledger", "incidence_row_id"),
        ("formal_exact_common_refinement_glue_ledger", "glue_row_id"),
    ):
        verify_closed_rows(result[key]["rows"], id_key, result[key])
    for key in (
        "exact_face_endpoint_to_interior_frontier",
        "partial_face_frontier",
    ):
        for row in result[key]["rows"]:
            payload = dict(row)
            row_hash = payload.pop("row_sha256")
            require(digest(payload) == row_hash, f"frontier closure:{key}")
        require(
            result[key]["row_count"] == len(result[key]["rows"])
            and result[key]["rows_sha256"] == digest(result[key]["rows"])
            and result[key]["row_ids_sha256"] == digest([
                row["frontier_row_id"] for row in result[key]["rows"]
            ]),
            f"frontier ledger:{key}",
        )
    require(result == expected_result, "full expected Python-object equality")
    require(
        canonical_bytes(result) == canonical_bytes(expected_result),
        "full expected canonical equality",
    )


def resign(envelope: dict[str, Any]) -> dict[str, Any]:
    value = copy.deepcopy(envelope)
    result = value["result"]
    trace_ledger = result["formal_internal_face_zero_trace_ledger"]
    incidence_ledger = result["formal_internal_face_incidence_ledger"]
    glue_ledger = result["formal_exact_common_refinement_glue_ledger"]
    traces = trace_ledger["rows"]
    for row in traces:
        row.pop("row_sha256", None)
        row["row_sha256"] = digest(row)
    trace_hash = {row["trace_row_id"]: row["row_sha256"] for row in traces}
    incidences = incidence_ledger["rows"]
    for row in incidences:
        row["trace_row_sha256"] = trace_hash[row["trace_row_id"]]
        row.pop("row_sha256", None)
        row["row_sha256"] = digest(row)
    incidence_hash = {
        row["incidence_row_id"]: row["row_sha256"] for row in incidences
    }
    glues = glue_ledger["rows"]
    for row in glues:
        row["trace_row_sha256"] = trace_hash[row["trace_row_id"]]
        row["negative_side_incidence_row_sha256"] = incidence_hash[
            row["negative_side_incidence_row_id"]
        ]
        row["positive_side_incidence_row_sha256"] = incidence_hash[
            row["positive_side_incidence_row_id"]
        ]
        row.pop("row_sha256", None)
        row["row_sha256"] = digest(row)
    for ledger, rows, id_key in (
        (trace_ledger, traces, "trace_row_id"),
        (incidence_ledger, incidences, "incidence_row_id"),
        (glue_ledger, glues, "glue_row_id"),
    ):
        ledger["row_count"] = len(rows)
        ledger["rows_sha256"] = digest(rows)
        ledger["row_ids_sha256"] = digest([row[id_key] for row in rows])
        ledger["row_hashes_sha256"] = digest([
            row["row_sha256"] for row in rows
        ])
    for key in (
        "exact_face_endpoint_to_interior_frontier",
        "partial_face_frontier",
    ):
        frontier = result[key]
        for row in frontier["rows"]:
            row.pop("row_sha256", None)
            row["row_sha256"] = digest(row)
        frontier["row_count"] = len(frontier["rows"])
        frontier["rows_sha256"] = digest(frontier["rows"])
        frontier["row_ids_sha256"] = digest([
            row["frontier_row_id"] for row in frontier["rows"]
        ])
    value["result_sha256"] = digest(result)
    return value


def semantic_attack_suite(
    envelope: dict[str, Any],
    expected: dict[str, Any],
) -> tuple[int, int]:
    def steal_frontier_into_trace(result: dict[str, Any]) -> None:
        frontier = result[
            "exact_face_endpoint_to_interior_frontier"
        ]["rows"][0]
        trace = result[
            "formal_internal_face_zero_trace_ledger"
        ]["rows"][0]
        trace["fixed_axis"] = frontier["fixed_axis"]
        trace["shared_coordinate"] = frontier["shared_coordinate"]
        trace["t_interval"] = copy.deepcopy(frontier["t_interval"])
        trace["transverse_axis"] = frontier["transverse_axis"]
        trace["transverse_interval"] = copy.deepcopy(
            frontier["transverse_interval"]
        )
        trace["whole_face_zero_trace_proof"] = copy.deepcopy(
            frontier["whole_face_proof"]
        )

    def duplicate_glue(result: dict[str, Any]) -> None:
        result["formal_exact_common_refinement_glue_ledger"]["rows"].append(
            copy.deepcopy(
                result[
                    "formal_exact_common_refinement_glue_ledger"
                ]["rows"][0]
            )
        )

    def duplicate_trace(result: dict[str, Any]) -> None:
        result["formal_internal_face_zero_trace_ledger"]["rows"].append(
            copy.deepcopy(
                result[
                    "formal_internal_face_zero_trace_ledger"
                ]["rows"][0]
            )
        )

    def toggle_trace_axis(result: dict[str, Any]) -> None:
        row = result[
            "formal_internal_face_zero_trace_ledger"
        ]["rows"][0]
        row["fixed_axis"] = "p" if row["fixed_axis"] == "s" else "s"

    def toggle_glue_relation(result: dict[str, Any]) -> None:
        row = result[
            "formal_exact_common_refinement_glue_ledger"
        ]["rows"][0]
        row["relation"] = (
            "CROSS_ORIGIN"
            if row["relation"] == "SAME_OCCURRENCE"
            else "SAME_OCCURRENCE"
        )

    mutations = [
        toggle_trace_axis,
        lambda r: r["formal_internal_face_zero_trace_ledger"]["rows"][0].
            __setitem__("shared_coordinate", "0"),
        lambda r: r["formal_internal_face_zero_trace_ledger"]["rows"][0][
            "whole_face_zero_trace_proof"
        ].__setitem__(
            "selected_lower_upper_and_full_face_dt_signs",
            ["STRICT_POSITIVE", "STRICT_POSITIVE", "STRICT_POSITIVE"],
        ),
        lambda r: r["formal_internal_face_incidence_ledger"]["rows"][0].
            __setitem__("leaf_row_id", "fabricated-leaf"),
        lambda r: r["formal_internal_face_incidence_ledger"]["rows"][0].
            __setitem__("outward_orientation", "NEGATIVE_T"),
        toggle_glue_relation,
        lambda r: r["formal_exact_common_refinement_glue_ledger"]["rows"][0].
            __setitem__("exact_common_face_geometry", False),
        lambda r: r["formal_exact_common_refinement_glue_ledger"]["rows"][0].
            __setitem__("component_deduplication_credit", 1),
        lambda r: r["exact_face_endpoint_to_interior_frontier"]["rows"][0].
            __setitem__("missing_evidence", "FABRICATED_CLOSED"),
        lambda r: r["partial_face_frontier"]["rows"][0].
            __setitem__("formal_trace_credit", 1),
        lambda r: r["formal_credit_contract"].
            __setitem__("global_fibre_credit", 1),
        lambda r: r["formal_internal_face_zero_trace_ledger"]["rows"][0].
            __setitem__("whole_origin_credit", 1),
        lambda r: r["formal_internal_face_incidence_ledger"]["rows"][0].
            __setitem__("whole_original_tube_credit", 1),
        lambda r: r["formal_exact_common_refinement_glue_ledger"]["rows"][0].
            __setitem__("global_exact_key_disposition_credit", 1),
        lambda r: r["formal_credit_contract"].
            __setitem__("whole_leaf_credit", 1),
        lambda r: r["formal_credit_contract"].
            __setitem__("D02", "COMPLETE"),
        lambda r: r["formal_credit_contract"].
            __setitem__("CM2", "GO"),
        lambda r: r["formal_input_binding"].
            __setitem__("Round208_certificate_sha256", "0" * 64),
        lambda r: r["formal_exact_full_face_trace_scope"][
            "accepted_contacts_per_official_key_ordinal"
        ].__setitem__("102440", 78),
        lambda r: r["formal_exact_full_face_trace_scope"][
            "accepted_contacts_per_official_key_ordinal_histogram"
        ].__setitem__("77", 5),
        steal_frontier_into_trace,
        duplicate_glue,
        duplicate_trace,
        lambda r: r["first_missing_frontier"].
            __setitem__("physical_component_transitive_exhaustion_missing",
                        False),
        lambda r: r["formal_exact_common_refinement_glue_ledger"]["rows"].
            pop(),
    ]
    rejected = 0
    for mutate in mutations:
        candidate = copy.deepcopy(envelope)
        mutate(candidate["result"])
        candidate = resign(candidate)
        try:
            verify_envelope(candidate, expected)
        except VerificationError:
            rejected += 1
    return len(mutations), rejected


def json_attack_suite(envelope: dict[str, Any]) -> tuple[int, int]:
    good = canonical_bytes(envelope) + b"\n"
    text = good.decode()
    attacks: list[tuple[bytes, int]] = [
        (
            b'{"schema":"x","schema":"y","result":{},"result_sha256":"z"}\n',
            MAX_INPUT_BYTES,
        ),
        (
            text.replace(
            '"result":{',
            '"result":{"status":"x","status":"y",',
            1,
            ).encode(),
            MAX_INPUT_BYTES,
        ),
        (
            text.replace('"result":{', '"result":{"x":NaN,', 1).encode(),
            MAX_INPUT_BYTES,
        ),
        (
            text.replace('"result":{', '"result":{"x":Infinity,', 1).encode(),
            MAX_INPUT_BYTES,
        ),
        (
            text.replace('"result":{', '"result":{"x":-Infinity,', 1).encode(),
            MAX_INPUT_BYTES,
        ),
        (good + b" ", MAX_INPUT_BYTES),
        (b"\xef\xbb\xbf" + good, MAX_INPUT_BYTES),
        (b"[]\n", MAX_INPUT_BYTES),
        (b"1\n", MAX_INPUT_BYTES),
        (b"", MAX_INPUT_BYTES),
        (canonical_bytes(envelope), MAX_INPUT_BYTES),
        (b'{"x":"' + bytes([255]) + b'"}\n', MAX_INPUT_BYTES),
        (b'{"x":"\\ud800"}\n', MAX_INPUT_BYTES),
        (b'{"x":"a' + bytes([0]) + b'b"}\n', MAX_INPUT_BYTES),
        (good, len(good) - 1),
    ]
    rejected = 0
    for raw, maximum in attacks:
        try:
            strict_json(raw, maximum)
        except (VerificationError, UnicodeDecodeError, UnicodeEncodeError):
            rejected += 1
    return len(attacks), rejected


def path_attack_suite() -> tuple[int, int]:
    attempted = 0
    rejected = 0

    def expect_reject(
        path: Path,
        maximum: int,
        parent: Path,
        name: str,
    ) -> None:
        nonlocal attempted, rejected
        attempted += 1
        try:
            secure_bytes(path, maximum, parent, name)
        except (VerificationError, FileNotFoundError, OSError):
            rejected += 1

    with tempfile.TemporaryDirectory(prefix=".round217_path_", dir=HERE) as raw:
        root = Path(raw)
        valid = root / "candidate.json"
        valid.write_bytes(b"{}\n")
        require(
            secure_bytes(valid, 1024, root, "candidate.json") == b"{}\n",
            "path suite control",
        )
        symlink = root / "symlink.json"
        symlink.symlink_to(valid)
        expect_reject(symlink, 1024, root, "symlink.json")

        hard_target = root / "hard-target.json"
        hard_target.write_bytes(b"{}\n")
        hard = root / "hard.json"
        os.link(hard_target, hard)
        expect_reject(hard, 1024, root, "hard.json")

        directory = root / "directory.json"
        directory.mkdir()
        expect_reject(directory, 1024, root, "directory.json")

        fifo = root / "fifo.json"
        os.mkfifo(fifo)
        expect_reject(fifo, 1024, root, "fifo.json")

        empty = root / "empty.json"
        empty.write_bytes(b"")
        expect_reject(empty, 1024, root, "empty.json")

        oversized = root / "oversized.json"
        with oversized.open("wb") as handle:
            handle.truncate(1025)
        expect_reject(oversized, 1024, root, "oversized.json")

        expect_reject(valid, 1024, root, "wrong.json")
        expect_reject(valid, 1024, HERE, "candidate.json")
        expect_reject(root / ".." / valid.name, 1024, root, "candidate.json")
        missing = root / "missing.json"
        expect_reject(missing, 1024, root, "missing.json")

        output_paths: list[Path] = []
        token = str(os.getpid())

        def expect_output_reject(path: Path) -> None:
            nonlocal attempted, rejected
            attempted += 1
            try:
                validate_output(path)
            except (VerificationError, FileNotFoundError, OSError):
                rejected += 1

        output_symlink = HERE / (
            f".{PREFIX}_verification_replay_attack_symlink_{token}.json"
        )
        output_symlink.symlink_to(valid)
        output_paths.append(output_symlink)
        expect_output_reject(output_symlink)

        output_target = HERE / (
            f".{PREFIX}_verification_replay_attack_target_{token}.json"
        )
        output_target.write_bytes(b"{}\n")
        output_hardlink = HERE / (
            f".{PREFIX}_verification_replay_attack_hardlink_{token}.json"
        )
        os.link(output_target, output_hardlink)
        output_paths.extend([output_hardlink, output_target])
        expect_output_reject(output_hardlink)

        output_fifo = HERE / (
            f".{PREFIX}_verification_replay_attack_fifo_{token}.json"
        )
        os.mkfifo(output_fifo)
        output_paths.append(output_fifo)
        expect_output_reject(output_fifo)

        nested_output = root / (
            f".{PREFIX}_verification_replay_attack_nested_{token}.json"
        )
        expect_output_reject(nested_output)

        unallowlisted = HERE / f".round217_unallowlisted_{token}.json"
        unallowlisted.write_bytes(b"{}\n")
        output_paths.append(unallowlisted)
        expect_output_reject(unallowlisted)

        output_directory = HERE / (
            f".{PREFIX}_verification_replay_attack_directory_{token}.json"
        )
        output_directory.mkdir()
        output_paths.append(output_directory)
        expect_output_reject(output_directory)

        for path in reversed(output_paths):
            if path.is_symlink() or path.is_file() or stat.S_ISFIFO(
                path.lstat().st_mode
            ):
                path.unlink()
            elif path.is_dir():
                path.rmdir()

    return attempted, rejected


def validate_output(path: Path) -> Path:
    absolute = path.resolve(strict=False)
    require(absolute.parent == HERE.resolve(), "verification output parent")
    official = absolute.name == VERIFICATION
    replay = (
        absolute.name.startswith(f".{PREFIX}_verification_replay_")
        and absolute.name.endswith(".json")
    )
    require(official or replay, "verification output filename")
    require(not absolute.is_symlink(), "verification output symlink")
    if absolute.exists():
        metadata = absolute.lstat()
        require(
            stat.S_ISREG(metadata.st_mode) and metadata.st_nlink == 1,
            "verification output regular unique",
        )
    return absolute


def safe_write(path: Path, data: bytes) -> None:
    destination = validate_output(path)
    descriptor, temporary = tempfile.mkstemp(
        prefix=f".{PREFIX}.verify.tmp.", dir=HERE
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
    parser.add_argument("--output", type=Path, default=HERE / VERIFICATION)
    arguments = parser.parse_args()

    verifier_sha256 = hashlib.sha256(
        secure_bytes(Path(__file__), 5_000_000, HERE, Path(__file__).name)
    ).hexdigest()
    pinned(HERE / PRODUCER, PRODUCER_SHA256, 5_000_000)
    raw_certificate = pinned(
        HERE / CERTIFICATE, CERTIFICATE_SHA256, 50_000_000
    )
    envelope = strict_json(raw_certificate)
    require(envelope["result_sha256"] == RESULT_SHA256,
            "official result SHA")

    print("Round217 verifier independently rebuilding expected result",
          file=sys.stderr)
    expected = reconstruct_expected_result()
    verify_envelope(envelope, expected)

    semantic_attempted, semantic_rejected = semantic_attack_suite(
        envelope, expected
    )
    json_attempted, json_rejected = json_attack_suite(envelope)
    path_attempted, path_rejected = path_attack_suite()
    print(
        "Round217 hostile suites "
        f"semantic={semantic_rejected}/{semantic_attempted} "
        f"JSON={json_rejected}/{json_attempted} "
        f"path={path_rejected}/{path_attempted}",
        file=sys.stderr,
    )
    require(
        semantic_attempted == semantic_rejected == 25
        and json_attempted == json_rejected == 15
        and path_attempted == path_rejected == 16,
        "all adversarial suites rejected",
    )

    result = {
        "status": "PASS_PARTIAL_FORMAL_ROUND217",
        "producer_sha256": PRODUCER_SHA256,
        "certificate_sha256": CERTIFICATE_SHA256,
        "certificate_result_sha256": RESULT_SHA256,
        "verifier_sha256": verifier_sha256,
        "producer_imported_or_executed": False,
        "Round214_probe_imported_or_executed": False,
        "full_expected_Python_object_equality": True,
        "full_expected_canonical_equality": True,
        "formal_trace_rows_verified": EXPECTED_ACCEPTED,
        "formal_incidence_rows_verified": 2 * EXPECTED_ACCEPTED,
        "formal_glue_rows_verified": EXPECTED_ACCEPTED,
        "exact_fail_closed_frontier_rows_verified": EXPECTED_EXACT_FRONTIER,
        "partial_fail_closed_frontier_rows_verified":
            EXPECTED_PARTIAL_FRONTIER,
        "semantic_resigned_attacks_attempted": semantic_attempted,
        "semantic_resigned_attacks_rejected": semantic_rejected,
        "strict_JSON_attacks_attempted": json_attempted,
        "strict_JSON_attacks_rejected": json_rejected,
        "filesystem_path_attacks_attempted": path_attempted,
        "filesystem_path_attacks_rejected": path_rejected,
        "AST_duplicate_literal_key_count": 0,
        "whole_leaf_credit": 0,
        "whole_origin_credit": 0,
        "whole_original_tube_credit": 0,
        "global_component_credit": 0,
        "global_fibre_credit": 0,
        "global_exact_key_disposition_credit": 0,
        "D02": "UNCHANGED_BLOCKED",
        "Gate5": "UNCHANGED_10/18",
        "CM2": "UNCHANGED_NO_GO",
    }
    verification_envelope = {
        "schema": VERIFICATION_SCHEMA,
        "result": result,
        "result_sha256": digest(result),
    }
    safe_write(
        arguments.output,
        canonical_bytes(verification_envelope) + b"\n",
    )
    print(verification_envelope["result_sha256"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
