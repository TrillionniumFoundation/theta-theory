#!/usr/bin/env python3
"""Independent, fail-closed verifier for the candidate-only C30c lane.

The C30c producer is neither imported nor executed.  This verifier loads a
pinned *independent* C30b verifier as its audited interval/half-open geometry
library, consumes only the fixed formally sealed C30b authority, then
reconstructs the two full-Delta origins directly from pinned R184/R215/C30a
inputs.  A successful verification still grants zero C30c formal credit;
the attack, dual-seed, cold-replay, and manifest prerequisites remain.
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import importlib.machinery
import io
import itertools
import json
import os
import stat
import sys
import types
from collections import Counter, defaultdict
from dataclasses import dataclass
from fractions import Fraction as Q
from pathlib import Path
from types import MappingProxyType
from typing import Any

sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parent
PREFIX = "cm2_round306c30c_source_w_full_delta_whole_origin_disposition"
COMBINED_CELL_LEDGER = PREFIX + "_delta_h_cell_ledger.jsonl.gz"
INHERITED_H_LEDGER = PREFIX + "_inherited_h_cell_ledger.jsonl.gz"
ORIGIN_LEDGER = PREFIX + "_whole_origin_ledger.jsonl.gz"
JOIN_LEDGER = PREFIX + "_combined_boundary_atomic_owner_join_ledger.jsonl.gz"
RESULT = PREFIX + "_result.json"
PRODUCER = PREFIX + "_producer.py"

C30B_PREFIX = "cm2_round306c30b_source_w_outgoing_h_whole_origin_disposition"
C30B_VERIFIER = C30B_PREFIX + "_independent_verifier.py"
C30B_VERIFIER_SHA256 = (
    "1776137520b1add49a218e6ccce680aaffdafc195c99ef7992c1a5ee31694b66"
)
C30B_PRODUCER = C30B_PREFIX + "_producer.py"
C30B_PRODUCER_SHA256 = (
    "003191131bff227453d07fa22ecd6e95b4f9d48e9ff74604ea4b7116f5818762"
)
C30B_RUNTIME = "cm2_round306c30b_python_flint_runtime_attestation.json"
C30B_H_LEDGER = C30B_PREFIX + "_h_cell_ledger.jsonl.gz"
C30B_ORIGIN_LEDGER = C30B_PREFIX + "_whole_origin_ledger.jsonl.gz"
C30B_RESULT = C30B_PREFIX + "_result.json"
C30B_MANIFEST = C30B_PREFIX + "_manifest.sha256"
C30B_MANIFEST_SHA256 = (
    "6af636a4239f390712d057030f03e09fbbca332c6170f183d3d0095f19f0f248"
)
C30B_VERIFICATION = C30B_PREFIX + "_verification.json"
C30B_VERIFICATION_SHA256 = (
    "e9e72536be9ba707fe2fdf6034b47978be4d09235e5133414ec7b0a31acf4e71"
)
C30B_SEALED_DIRNAME = "cm2_round306c30b_sealed"
C30B_RESULT_FILE_SHA256 = (
    "b015e5bd6a4ee01d71ac95765d07dcbc63c3888f0c8ff9205e2d8c688958c11b"
)
C30B_SEALED_FILE_PINS = {
    C30B_RUNTIME:
        "6b48cd0ca3fd53f9fdd457cc3c1106055e12db4d4ad999fcfd1fc89ad36b95df",
    C30B_H_LEDGER:
        "4259fdaadfe1b5e1c0b7b315ef71fdae245bb3bbc45c5f814c4d4b7a670e8672",
    C30B_ORIGIN_LEDGER:
        "19edfece87d4f95e3e25a62d508654918c03ec879f574ab01854bde5bee4c6c9",
    C30B_RESULT: C30B_RESULT_FILE_SHA256,
}
C30B_RESULT_OBJECT_SHA256 = (
    "7abf8da628eb35b20ed27b032dc55ea29e9944530d2d5a6a64993a995f1ad85e"
)
C30B_MANIFEST_MEMBER_PINS = {
    "cm2_round306c30a_python_flint_requirements.lock":
        "cd171f53dd8a187b2ef4bd7ad0cc2adbe2082395646c0c57407f4e3514c11f5c",
    "cm2_round306c30a_python_flint_runtime_lock.json":
        "ffe714b67a0aa05d8094033a0d9cc8e10ccafa03157951adf3d64055c98cdc79",
    ("cm2_round306c30a_runtime/python_flint-0.9.0-cp310-abi3-"
     "manylinux2014_x86_64.manylinux_2_17_x86_64.whl"):
        "376b88cacd30612479e839ffdba887599d3f9c8c0e214852bf80bb2b194e4d76",
    "cm2_round306c30b_python_flint_runtime_attestation_auditor.py":
        "0309dc5710421a5e56b0d1b7b04ef2c5ccf971d054943dc6baf7765e512b76f8",
    C30B_PREFIX + "_attack_harness.py":
        "c00d45077511eb87bd650fea090cd5f01b285e6b68d42bab311f2051878eae5d",
    C30B_PREFIX + "_cold_replay.md":
        "98b1a27f2192c90524709457067b777765a5fd6d84002a10f05c9fbdb0a86610",
    C30B_VERIFIER: C30B_VERIFIER_SHA256,
    C30B_PRODUCER: C30B_PRODUCER_SHA256,
    C30B_PREFIX + "_report.md":
        "80ee855b45dec1c21099dfe735ecca4d7be3c222973a17f9cec136efe66426f2",
    C30B_VERIFICATION: C30B_VERIFICATION_SHA256,
    **{
        C30B_SEALED_DIRNAME + "/" + filename: sha256
        for filename, sha256 in C30B_SEALED_FILE_PINS.items()
    },
}

ORIGIN_KEYS = (
    "W:N:04.00.10000010",
    "W:S:H.04.00.10000010",
)
TARGET_BY_ORIGIN = {
    "W:N:04.00.10000010": "G[1,1]",
    "W:S:H.04.00.10000010": "G[1,0]",
}
SEAM_BY_CHART = {"W:N": "NW", "W:S": "SW"}
LIVE_H_SIGN_BY_CHART = {"W:N": "H>0", "W:S": "H<0"}
MISMATCH_H_SIGN_BY_CHART = {"W:N": "H<0", "W:S": "H>0"}
EXPECTED_LINEAGE = {
    "Round176_prior": 0,
    "Round176_preclosed": 3,
    "Round176_roots": 61,
    "Round180_inherited": 160,
    "Round180_final": 378,
    "Round180_inherited_excluded": 105,
    "Round180_inherited_direct_live": 11,
    "Round180_inherited_H": 44,
    "Round201_closed": 328,
    "Round306C30A_closed": 10,
    "combined_Delta_H": 40,
    "top_level_leaf_count": 541,
}
EXPECTED_TOP_LEVEL_DISPOSITION = Counter({
    "EXCLUDED": 446, "LIVE": 31, "MIXED": 64,
})
LOCAL_H_EXCLUSION_CLASSES = {
    "STRICT_OUTGOING_CHART_MISMATCH_RECTANGLE",
    "MONOTONE_H_OUTGOING_CHART_MISMATCH_RECTANGLE",
}
LOCAL_H_LIVE_CLASSES = {
    "STRICT_PREFIX_STAGE_ONE_MATCH_RECTANGLE",
    "MONOTONE_H_PREFIX_STAGE_ONE_MATCH_RECTANGLE",
}
LOCAL_H_TYPED = "TYPED_SEAM_GRAPH_AND_TWO_OPEN_SIDES"


class Reject(RuntimeError):
    pass


def require(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise Reject(label)


def race_checked_single_read(
    path: Path, label: str, containment_root: Path
) -> tuple[bytes, tuple[int, int, int, int, int, int, int]]:
    absolute = Path(os.path.abspath(os.fspath(path)))
    root = containment_root.resolve(strict=True)
    require(
        absolute.resolve(strict=True) == absolute and absolute.is_relative_to(root),
        "race-checked path containment:" + label,
    )
    descriptor = os.open(
        absolute,
        os.O_RDONLY | os.O_CLOEXEC | getattr(os, "O_NOFOLLOW", 0),
    )
    try:
        before = os.fstat(descriptor)
        chunks: list[bytes] = []
        while block := os.read(descriptor, 1 << 20):
            chunks.append(block)
        after = os.fstat(descriptor)
    finally:
        os.close(descriptor)
    path_status = absolute.lstat()
    identity = (
        before.st_dev, before.st_ino, before.st_mode, before.st_nlink,
        before.st_size, before.st_mtime_ns, before.st_ctime_ns,
    )
    require(
        stat.S_ISREG(before.st_mode)
        and before.st_nlink == 1
        and identity == (
            after.st_dev, after.st_ino, after.st_mode, after.st_nlink,
            after.st_size, after.st_mtime_ns, after.st_ctime_ns,
        )
        and identity == (
            path_status.st_dev, path_status.st_ino, path_status.st_mode,
            path_status.st_nlink, path_status.st_size,
            path_status.st_mtime_ns, path_status.st_ctime_ns,
        ),
        "race-checked regular singleton identity:" + label,
    )
    raw = b"".join(chunks)
    require(len(raw) == before.st_size, "race-checked byte count:" + label)
    return raw, identity


def require_capture_still_current(
    path: Path,
    identity: tuple[int, int, int, int, int, int, int],
    label: str,
) -> None:
    status = path.lstat()
    require(
        identity == (
            status.st_dev, status.st_ino, status.st_mode, status.st_nlink,
            status.st_size, status.st_mtime_ns, status.st_ctime_ns,
        ) and stat.S_ISREG(status.st_mode) and not path.is_symlink(),
        "captured path identity changed:" + label,
    )


@dataclass(frozen=True)
class CandidateCapture:
    root: Path
    directory_identity: tuple[int, int, int, int, int, int]
    member_identities: Any
    raw_by_filename: Any


def _directory_identity(status: os.stat_result) -> tuple[int, int, int, int, int, int]:
    return (
        status.st_dev, status.st_ino, status.st_mode, status.st_nlink,
        status.st_mtime_ns, status.st_ctime_ns,
    )


def _member_identity(
    status: os.stat_result,
) -> tuple[int, int, int, int, int, int, int]:
    return (
        status.st_dev, status.st_ino, status.st_mode, status.st_nlink,
        status.st_size, status.st_mtime_ns, status.st_ctime_ns,
    )


def capture_candidate_bytes(
    candidate: Path, expected_files: set[str], maximum: int = 64 * 1024 * 1024,
) -> CandidateCapture:
    """Capture the exact candidate once through one pinned directory fd."""
    absolute = Path(os.path.abspath(os.fspath(candidate)))
    path_before = absolute.lstat()
    require(
        stat.S_ISDIR(path_before.st_mode) and not absolute.is_symlink(),
        "C30c candidate race-checked directory",
    )
    directory_fd = os.open(
        absolute,
        os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC
        | getattr(os, "O_NOFOLLOW", 0),
    )
    try:
        opened_before = os.fstat(directory_fd)
        directory_identity = _directory_identity(opened_before)
        require(
            stat.S_ISDIR(opened_before.st_mode)
            and directory_identity == _directory_identity(path_before)
            and set(os.listdir(directory_fd)) == expected_files,
            "C30c candidate exact race-checked file set",
        )
        raw_by_filename: dict[str, bytes] = {}
        member_identities: dict[
            str, tuple[int, int, int, int, int, int, int]
        ] = {}
        for filename in sorted(expected_files):
            entry_before = os.stat(
                filename, dir_fd=directory_fd, follow_symlinks=False
            )
            require(
                stat.S_ISREG(entry_before.st_mode)
                and entry_before.st_nlink == 1
                and 0 < entry_before.st_size <= maximum,
                "C30c candidate race-checked regular singleton:" + filename,
            )
            try:
                descriptor = os.open(
                    filename,
                    os.O_RDONLY | os.O_CLOEXEC | getattr(os, "O_NOFOLLOW", 0),
                    dir_fd=directory_fd,
                )
            except OSError as error:
                raise Reject(
                    "C30c candidate race-checked regular singleton:" + filename
                ) from error
            try:
                before = os.fstat(descriptor)
                identity = _member_identity(before)
                require(
                    stat.S_ISREG(before.st_mode)
                    and before.st_nlink == 1
                    and 0 < before.st_size <= maximum,
                    "C30c candidate race-checked regular singleton:" + filename,
                )
                chunks: list[bytes] = []
                while block := os.read(descriptor, 1 << 20):
                    chunks.append(block)
                after = os.fstat(descriptor)
            finally:
                os.close(descriptor)
            path_after = os.stat(
                filename, dir_fd=directory_fd, follow_symlinks=False
            )
            raw = b"".join(chunks)
            require(
                identity == _member_identity(entry_before)
                and identity == _member_identity(after)
                and identity == _member_identity(path_after)
                and len(raw) == before.st_size,
                "C30c candidate member changed during capture:" + filename,
            )
            raw_by_filename[filename] = raw
            member_identities[filename] = identity
        opened_after = os.fstat(directory_fd)
        path_after = absolute.lstat()
        require(
            directory_identity == _directory_identity(opened_after)
            and directory_identity == _directory_identity(path_after)
            and set(os.listdir(directory_fd)) == expected_files,
            "C30c candidate directory changed during capture",
        )
    finally:
        os.close(directory_fd)
    return CandidateCapture(
        absolute,
        directory_identity,
        MappingProxyType(dict(member_identities)),
        MappingProxyType(dict(raw_by_filename)),
    )


def require_candidate_capture_still_current(capture: CandidateCapture) -> None:
    status = capture.root.lstat()
    require(
        _directory_identity(status) == capture.directory_identity
        and stat.S_ISDIR(status.st_mode)
        and not capture.root.is_symlink()
        and {path.name for path in capture.root.iterdir()}
        == set(capture.raw_by_filename),
        "C30c candidate directory changed after capture",
    )
    for filename, identity in capture.member_identities.items():
        current = (capture.root / filename).lstat()
        require(
            _member_identity(current) == identity
            and stat.S_ISREG(current.st_mode)
            and not (capture.root / filename).is_symlink(),
            "C30c candidate member changed after capture:" + filename,
        )


def canonical_rows_from_bytes(raw: bytes, label: str) -> list[dict[str, Any]]:
    require(
        len(raw) >= 4 and raw[:2] == b"\x1f\x8b" and raw[3] == 0,
        "canonical gzip header:" + label,
    )
    try:
        clear = gzip.decompress(raw)
    except (OSError, EOFError) as error:
        raise Reject("gzip stream:" + label) from error
    require(clear.endswith(b"\n") and b"\r" not in clear, "JSONL framing:" + label)
    canonical_stream = io.BytesIO()
    with gzip.GzipFile(
        filename="", mode="wb", fileobj=canonical_stream,
        compresslevel=9, mtime=0,
    ) as output:
        output.write(clear)
    require(raw == canonical_stream.getvalue(), "canonical gzip bytes:" + label)
    rows: list[dict[str, Any]] = []
    for ordinal, line in enumerate(clear.splitlines()):
        row = base.strict_object_bytes(line, f"{label}:{ordinal}")
        require(row.get("row_sha256") is not None, "row hash present")
        body = dict(row)
        claimed = body.pop("row_sha256")
        require(claimed == digest(body), "row hash:" + label)
        rows.append(row)
    return rows


C30B_VERIFIER_CAPTURE: tuple[
    bytes, tuple[int, int, int, int, int, int, int]
] | None = None


def import_pinned_c30b_verifier() -> Any:
    global C30B_VERIFIER_CAPTURE
    path = ROOT / C30B_VERIFIER
    raw, identity = race_checked_single_read(path, C30B_VERIFIER, ROOT)
    require(
        hashlib.sha256(raw).hexdigest() == C30B_VERIFIER_SHA256,
        "pinned independent C30b verifier",
    )
    require(
        PRODUCER[:-3] not in sys.modules
        and C30B_PRODUCER[:-3] not in sys.modules,
        "no producer preloaded",
    )
    module_name = C30B_VERIFIER[:-3]
    require(module_name not in sys.modules, "C30b verifier not preloaded")
    module = types.ModuleType(module_name)
    module.__file__ = os.fspath(path)
    module.__package__ = ""
    module.__loader__ = None
    module.__spec__ = importlib.machinery.ModuleSpec(
        module_name, loader=None, origin=os.fspath(path)
    )
    sys.modules[module_name] = module
    try:
        exec(compile(raw, os.fspath(path), "exec", dont_inherit=True), module.__dict__)
    except BaseException:
        sys.modules.pop(module_name, None)
        raise
    C30B_VERIFIER_CAPTURE = (raw, identity)
    require_capture_still_current(path, identity, C30B_VERIFIER)
    require(
        Path(module.__file__).resolve(strict=True) == path.resolve(strict=True)
        and hashlib.sha256(raw).hexdigest() == C30B_VERIFIER_SHA256,
        "imported independent C30b verifier identity",
    )
    return module


base = import_pinned_c30b_verifier()
wire = base.wire
digest = base.digest
file_hash = base.file_hash
regular_bytes = base.regular_bytes
strict_json = base.strict_json
canonical_rows = base.canonical_rows
sealed = base.sealed
r176 = base.r176
r180 = base.r180
r215 = base.r215
ctx = base.flint.ctx


def sign_name(value: Any) -> str:
    value_sign = r176.sign(value)
    return (
        "STRICT_POSITIVE" if value_sign > 0 else
        "STRICT_NEGATIVE" if value_sign < 0 else "OVERWRAP"
    )


def fixed_p_box(box: Any, p0: Q, p1: Q) -> Any:
    return r176.Box(
        box.t0, box.t1, p0, p1, box.s0, box.s1,
        box.depth, box.path,
    )


def local_point_box(
    box: Any, *, t_value: Q | None = None, p_value: Q | None = None
) -> Any:
    return r176.Box(
        box.t0 if t_value is None else t_value,
        box.t1 if t_value is None else t_value,
        box.p0 if p_value is None else p_value,
        box.p1 if p_value is None else p_value,
        box.s0, box.s1, box.depth, box.path,
    )


def local_seam_evidence(
    chart_id: str, box: Any, seam_id: str
) -> dict[str, Any]:
    """Recompute seam evidence only from pinned R176 interval primitives."""
    seam = r176.SEAMS[seam_id]
    _cell, nx, ny = r176.tight_contact(chart_id, box)
    whole = r176.seam_values(chart_id, box, seam_id)
    corner_values = {
        f"t{ti}_p{pi}": r176.seam_values(
            chart_id,
            local_point_box(box, t_value=t_value, p_value=p_value),
            seam_id,
        )["H"]
        for ti, t_value in enumerate((box.t0, box.t1))
        for pi, p_value in enumerate((box.p0, box.p1))
    }
    corners = {
        key: sign_name(value) for key, value in sorted(corner_values.items())
    }
    integer_signs = [r176.sign(value) for value in corner_values.values()]
    lower = r176.seam_values(
        chart_id, local_point_box(box, p_value=box.p0), seam_id
    )["H"]
    upper = r176.seam_values(
        chart_id, local_point_box(box, p_value=box.p1), seam_id
    )["H"]
    dt_sign = r176.sign(whole["dt"])
    typed = (
        r176.sign(seam["normal"](nx, ny)) == 0
        and bool(seam["other"](nx, ny) < 0)
        and bool(whole["forward"] > 0)
        and bool(whole["inward"] > 0)
        and bool(whole["dp"] < 0)
    )
    uniform = 0
    if (
        dt_sign != 0 and integer_signs[0] != 0
        and all(value == integer_signs[0] for value in integer_signs)
    ):
        uniform = integer_signs[0]
    outgoing = None
    if uniform:
        outgoing = (
            ("W" if uniform > 0 else "N") if seam_id == "NW"
            else ("W" if uniform < 0 else "S")
        )
    return {
        "seam_id": seam_id,
        "adjacent_chart": seam["adjacent"],
        "normal_sign": sign_name(seam["normal"](nx, ny)),
        "other_margin_sign": sign_name(seam["other"](nx, ny)),
        "H_whole_box_sign": sign_name(whole["H"]),
        "forward_sign": sign_name(whole["forward"]),
        "inward_sign": sign_name(whole["inward"]),
        "dH_dt_sign": sign_name(whole["dt"]),
        "dH_dp_sign": sign_name(whole["dp"]),
        "p_lower_face_H_sign": sign_name(lower),
        "p_upper_face_H_sign": sign_name(upper),
        "corner_H_signs": corners,
        "typed_preconditions": typed,
        "full_graph": bool(lower > 0) and bool(upper < 0),
        "clipped_graph": (
            dt_sign != 0 and 1 in integer_signs and -1 in integer_signs
        ),
        "uniform_outgoing_chart": outgoing,
    }


def local_complete_typed_strata(
    detail: dict[str, Any], terminal_id: str
) -> dict[str, Any]:
    """Data-driven typed H complex reconstructed inside C30c."""
    seam_id = detail["seam_id"]
    adjacent = detail["adjacent_chart"]
    corners = detail["corner_H_signs"]
    require(
        detail["typed_preconditions"]
        and (detail["full_graph"] or detail["clipped_graph"])
        and all(value != "OVERWRAP" for value in corners.values()),
        "C30c local typed H preconditions:" + terminal_id,
    )
    sign_chart = (
        {"STRICT_POSITIVE": "W", "STRICT_NEGATIVE": "N"}
        if seam_id == "NW" else
        {"STRICT_NEGATIVE": "W", "STRICT_POSITIVE": "S"}
    )
    open_sides = [
        sealed({
            "schema": "cm2.round306c30b.H-open-side.row.v1",
            "terminal_id": terminal_id,
            "predicate": predicate,
            "ambient_dimension": 3,
            "outgoing_chart": sign_chart[sign],
            "disposition": "LIVE" if sign_chart[sign] == "W" else "EXCLUDED",
            "nonempty_positive_measure": True,
            "H_continuity_and_strict_side_sign_proved": True,
            "closed_enclosure_terminal_id": terminal_id,
        })
        for sign, predicate in (
            ("STRICT_NEGATIVE", "H<0"),
            ("STRICT_POSITIVE", "H>0"),
        )
    ]

    def crosses(values: list[str]) -> bool:
        return set(values) == {"STRICT_NEGATIVE", "STRICT_POSITIVE"}

    face_inputs = [
        ("t", "LOWER", [corners["t0_p0"], corners["t0_p1"]],
         "STRICT_dH_dp_UNIQUE_POINT_X_s"),
        ("t", "UPPER", [corners["t1_p0"], corners["t1_p1"]],
         "STRICT_dH_dp_UNIQUE_POINT_X_s"),
        ("p", "LOWER", [corners["t0_p0"], corners["t1_p0"]],
         "STRICT_dH_dt_UNIQUE_POINT_X_s"),
        ("p", "UPPER", [corners["t0_p1"], corners["t1_p1"]],
         "STRICT_dH_dt_UNIQUE_POINT_X_s"),
        ("s", "LOWER", list(corners.values()), "H_GRAPH_CURVE_AT_FIXED_s"),
        ("s", "UPPER", list(corners.values()), "H_GRAPH_CURVE_AT_FIXED_s"),
    ]
    face_rows: list[dict[str, Any]] = []
    face_regions: list[dict[str, Any]] = []
    for axis, side, signs, proof in face_inputs:
        crossing = True if axis == "s" else (
            detail["dH_dt_sign"] != "OVERWRAP" and crosses(signs)
            if axis == "p" else crosses(signs)
        )
        zero = sealed({
            "schema": "cm2.round306c30b.H-sheet-face-incidence.row.v1",
            "terminal_id": terminal_id,
            "fixed_axis": axis,
            "boundary_side": side,
            "predicate": "H=0",
            "nonempty": crossing,
            "dimension_if_nonempty": 1,
            "proof": proof,
            "half_open_outgoing_owner_chart": "W" if crossing else "NONE",
            "chart_level_half_open_owner": "W" if crossing else "NONE",
            "closed_enclosure_terminal_id": terminal_id,
            "shadow_chart": adjacent if crossing else "NONE",
            "disposition": "LIVE" if crossing else "EMPTY",
            "ambient_dyadic_owner_rule": (
                "LOWER_CHILD_OWNS_SPLIT_EQUALITY__LEXICOGRAPHIC_RECURSION"
            ),
        })
        face_rows.append(zero)
        present = (
            {"STRICT_NEGATIVE", "STRICT_POSITIVE"}
            if crossing else set(signs)
        )
        require(bool(present) and "OVERWRAP" not in present,
                "C30c local face sign support")
        for sign in ("STRICT_NEGATIVE", "STRICT_POSITIVE"):
            nonempty = sign in present
            outgoing = sign_chart[sign] if nonempty else "NONE"
            face_regions.append(sealed({
                "schema": "cm2.round306c30b.H-sheet-face-open-region.row.v1",
                "terminal_id": terminal_id,
                "fixed_axis": axis,
                "boundary_side": side,
                "predicate": "H<0" if sign == "STRICT_NEGATIVE" else "H>0",
                "H_sign": sign,
                "nonempty": nonempty,
                "dimension_if_nonempty": 2,
                "proof": (
                    "STRICT_MONOTONE_CROSSING_COMPLEMENT_REGION"
                    if crossing else "UNIFORM_STRICT_FACE_SIGN"
                ),
                "outgoing_chart": outgoing,
                "chart_level_half_open_owner": outgoing if nonempty else "NONE",
                "closed_enclosure_terminal_id": terminal_id,
                "disposition": (
                    "LIVE" if outgoing == "W"
                    else "EXCLUDED" if nonempty else "EMPTY"
                ),
                "H_zero_boundary_row_sha256": zero["row_sha256"],
            }))

    edge_specs: list[tuple[dict[str, str], str, list[str], bool, str]] = []
    for ti, t_side in enumerate(("LOWER", "UPPER")):
        signs = [corners[f"t{ti}_p0"], corners[f"t{ti}_p1"]]
        for s_side in ("LOWER", "UPPER"):
            edge_specs.append((
                {"t": t_side, "s": s_side}, "p", signs,
                crosses(signs), "STRICT_dH_dp_UNIQUE_POINT",
            ))
    for pi, p_side in enumerate(("LOWER", "UPPER")):
        signs = [corners[f"t0_p{pi}"], corners[f"t1_p{pi}"]]
        crossing = detail["dH_dt_sign"] != "OVERWRAP" and crosses(signs)
        for s_side in ("LOWER", "UPPER"):
            edge_specs.append((
                {"p": p_side, "s": s_side}, "t", signs,
                crossing, "STRICT_dH_dt_UNIQUE_POINT",
            ))
    for ti, t_side in enumerate(("LOWER", "UPPER")):
        for pi, p_side in enumerate(("LOWER", "UPPER")):
            edge_specs.append((
                {"t": t_side, "p": p_side}, "s",
                [corners[f"t{ti}_p{pi}"]], False,
                "STRICT_NONZERO_H_AT_t_p_CORNER",
            ))
    edge_rows: list[dict[str, Any]] = []
    edge_regions: list[dict[str, Any]] = []
    for fixed, free_axis, signs, crossing, proof in edge_specs:
        zero = sealed({
            "schema": "cm2.round306c30b.H-sheet-edge-incidence.row.v1",
            "terminal_id": terminal_id,
            "fixed": fixed,
            "free_axis": free_axis,
            "predicate": "H=0",
            "nonempty": crossing,
            "dimension_if_nonempty": 0,
            "proof": proof,
            **({"H_sign": signs[0]} if free_axis == "s" else {}),
            "half_open_outgoing_owner_chart": "W" if crossing else "NONE",
            "chart_level_half_open_owner": "W" if crossing else "NONE",
            "closed_enclosure_terminal_id": terminal_id,
            "disposition": "LIVE" if crossing else "EMPTY",
        })
        edge_rows.append(zero)
        present = (
            {"STRICT_NEGATIVE", "STRICT_POSITIVE"}
            if crossing else set(signs)
        )
        for sign in ("STRICT_NEGATIVE", "STRICT_POSITIVE"):
            nonempty = sign in present
            outgoing = sign_chart[sign] if nonempty else "NONE"
            edge_regions.append(sealed({
                "schema": "cm2.round306c30b.H-sheet-edge-open-interval.row.v1",
                "terminal_id": terminal_id,
                "fixed": fixed,
                "free_axis": free_axis,
                "predicate": "H<0" if sign == "STRICT_NEGATIVE" else "H>0",
                "H_sign": sign,
                "nonempty": nonempty,
                "dimension_if_nonempty": 1,
                "proof": (
                    "STRICT_MONOTONE_CROSSING_COMPLEMENT_INTERVAL"
                    if crossing else "UNIFORM_STRICT_EDGE_SIGN"
                ),
                "outgoing_chart": outgoing,
                "chart_level_half_open_owner": outgoing if nonempty else "NONE",
                "closed_enclosure_terminal_id": terminal_id,
                "disposition": (
                    "LIVE" if outgoing == "W"
                    else "EXCLUDED" if nonempty else "EMPTY"
                ),
                "H_zero_boundary_row_sha256": zero["row_sha256"],
            }))
    corner_rows = [
        sealed({
            "schema": "cm2.round306c30b.H-sheet-corner-incidence.row.v1",
            "terminal_id": terminal_id,
            "corner": {"t": t_side, "p": p_side, "s": s_side},
            "predicate": "H=0",
            "nonempty": False,
            "dimension_if_nonempty": 0,
            "proof": "STRICT_NONZERO_H_AT_t_p_CORNER",
            "H_sign": corners[f"t{ti}_p{pi}"],
            "disposition": "EMPTY",
            "chart_level_half_open_owner": "NONE",
            "closed_enclosure_terminal_id": terminal_id,
            "strict_corner_outgoing_chart": sign_chart[corners[f"t{ti}_p{pi}"]],
            "strict_corner_disposition": (
                "LIVE" if sign_chart[corners[f"t{ti}_p{pi}"]] == "W"
                else "EXCLUDED"
            ),
            "strict_corner_closed_enclosure_terminal_id": terminal_id,
        })
        for ti, t_side in enumerate(("LOWER", "UPPER"))
        for pi, p_side in enumerate(("LOWER", "UPPER"))
        for s_side in ("LOWER", "UPPER")
    ]
    sheet = sealed({
        "schema": "cm2.round306c30b.H-zero-sheet.row.v1",
        "terminal_id": terminal_id,
        "predicate": "H=ux*dy-uy*dx=0",
        "seam_id": seam_id,
        "ambient_dimension": 2,
        "nonempty": True,
        "unique_graph_in_p_by_strict_dH_dp": (
            detail["dH_dp_sign"] == "STRICT_NEGATIVE"
        ),
        "half_open_rule": "E_OR_W_OWNS__N_OR_S_SHADOWS",
        "half_open_owner_chart": "W",
        "chart_level_half_open_owner": "W",
        "relative_interior_dyadic_owner_terminal_id": terminal_id,
        "ownership_scope": (
            "RELATIVE_INTERIOR_OF_CLOSED_TERMINAL__"
            "BOUNDARY_OWNERSHIP_DEFERRED_TO_ATOMIC_OWNER_AUDIT"
        ),
        "shadow_chart": adjacent,
        "disposition": "LIVE",
        "face_incidence_row_count": len(face_rows),
        "face_incidence_rows_sha256": digest(face_rows),
        "edge_incidence_row_count": len(edge_rows),
        "edge_incidence_rows_sha256": digest(edge_rows),
        "corner_incidence_row_count": len(corner_rows),
        "corner_incidence_rows_sha256": digest(corner_rows),
    })
    return {
        "open_3D_sides": open_sides,
        "H_zero_2D_sheet": sheet,
        "terminal_face_2D_H_sign_regions": face_regions,
        "H_zero_1D_face_incidences": face_rows,
        "terminal_edge_1D_H_sign_intervals": edge_regions,
        "H_zero_0D_edge_incidences": edge_rows,
        "H_zero_0D_corner_absence_rows": corner_rows,
    }


def h_at_p(row: Any, seam_id: str, p: Q) -> Any:
    return r176.seam_values(
        row.chart_id, fixed_p_box(row.box, p, p), seam_id
    )["H"]


def independent_h_bracket(row: Any, seam_id: str) -> dict[str, Any]:
    left, right = row.box.p0, row.box.p1
    left_sign = r176.sign(h_at_p(row, seam_id, left))
    right_sign = r176.sign(h_at_p(row, seam_id, right))
    require(left_sign == 1 and right_sign == -1, "full H graph endpoints")
    steps: list[dict[str, Any]] = []
    for ordinal in range(32):
        middle = (left + right) / 2
        middle_sign = r176.sign(h_at_p(row, seam_id, middle))
        if middle_sign == 0:
            steps.append(sealed({
                "schema": "cm2.round306c30c.H-bracket-step.v1",
                "ordinal": ordinal,
                "p_midpoint": str(middle),
                "H_midpoint_face_sign": "OVERWRAP",
                "update": "STOP_INTERVAL_OVERWRAP",
            }))
            break
        if middle_sign == left_sign:
            left = middle
            update = "REPLACE_LEFT_ENDPOINT"
        else:
            require(middle_sign == right_sign, "H bracket sign trichotomy")
            right = middle
            update = "REPLACE_RIGHT_ENDPOINT"
        steps.append(sealed({
            "schema": "cm2.round306c30c.H-bracket-step.v1",
            "ordinal": ordinal,
            "p_midpoint": str(middle),
            "H_midpoint_face_sign": (
                "STRICT_POSITIVE" if middle_sign > 0 else "STRICT_NEGATIVE"
            ),
            "update": update,
        }))
    require(
        sign_name(h_at_p(row, seam_id, left)) == "STRICT_POSITIVE"
        and sign_name(h_at_p(row, seam_id, right)) == "STRICT_NEGATIVE"
        and left < right,
        "closed H bracket",
    )
    return {
        "method": "DETERMINISTIC_RATIONAL_BISECTION_UNTIL_INTERVAL_OVERWRAP",
        "maximum_steps": 32,
        "steps_executed": len(steps),
        "step_rows": steps,
        "step_rows_sha256": digest(steps),
        "p_bracket": [str(left), str(right)],
        "exact_width": str(right - left),
        "p_lower_H_sign": "STRICT_POSITIVE",
        "p_upper_H_sign": "STRICT_NEGATIVE",
        "closed_t_s_base_unchanged": True,
        "unique_H_zero_graph_inside_bracket_by_strict_dH_dp": True,
    }


def independent_delta_collar(
    row: Any, target_id: str, bracket: dict[str, Any]
) -> dict[str, Any]:
    p0, p1 = (Q(value) for value in bracket["p_bracket"])
    collar = fixed_p_box(row.box, p0, p1)
    records = r176.records_for(row.chart_id, collar, (target_id,))
    require(
        len(records) == 1 and bool(records[0].discriminant < 0),
        "Delta negative on entire closed H collar:" + row.key,
    )
    return {
        "target": target_id,
        "closed_box": r176.box_row(collar),
        "Delta_interval_sign": "STRICT_NEGATIVE",
        "strict_on_entire_closed_t_s_p_bracket": True,
        "H_zero_subset_of_bracket": True,
        "conclusion": "H_ZERO_SHEET_SUBSET_OF_STRICT_DELTA_NEGATIVE_REGION",
        "Delta_zero_intersect_H_zero": "EMPTY",
        "restriction_to_every_owned_face_edge_vertex": True,
    }


def independent_boundary_rows(row: Any) -> list[dict[str, Any]]:
    template = [
        {
            "predicate": "Delta>0",
            "disposition": "EXCLUDED_UNIQUE_FIRST_G_OWNER_MISMATCH",
            "equality_owner": "NOT_APPLICABLE_OPEN_STRATUM",
        },
        {
            "predicate": "Delta=0",
            "disposition": "EXCLUDED_UNIQUE_FIRST_G_TANGENCY_OWNER_MISMATCH",
            "equality_owner": "G_TARGET_TANGENCY_STRATUM",
        },
        {
            "predicate": "Delta<0 AND " + LIVE_H_SIGN_BY_CHART[row.chart_id],
            "disposition": "LIVE_W_STAGE_ONE_OWNER_CHART_MATCH",
            "equality_owner": "NOT_APPLICABLE_OPEN_STRATUM",
        },
        {
            "predicate": "Delta<0 AND H=0",
            "disposition": "LIVE_W_HALF_OPEN_SEAM_OWNER",
            "equality_owner": "W",
        },
        {
            "predicate": "Delta<0 AND " + MISMATCH_H_SIGN_BY_CHART[row.chart_id],
            "disposition": "EXCLUDED_OUTGOING_CHART_MISMATCH",
            "equality_owner": "NOT_APPLICABLE_OPEN_STRATUM",
        },
    ]
    rows: list[dict[str, Any]] = []
    axes = ("t", "p", "s")
    for fixed_count in (1, 2, 3):
        for fixed_axes in itertools.combinations(axes, fixed_count):
            for sides in itertools.product(("LOWER", "UPPER"), repeat=fixed_count):
                rows.append(sealed({
                    "schema": "cm2.round306c30c.outer-boundary-restriction.v1",
                    "cell_key": row.key,
                    "fixed_coordinates": dict(zip(
                        fixed_axes, sides, strict=True
                    )),
                    "ambient_dimension": 3 - fixed_count,
                    "restricted_predicate_partition": template,
                    "restricted_predicate_partition_sha256": digest(template),
                    "Delta_zero_AND_H_zero": "EMPTY_BY_CLOSED_H_BRACKET_DELTA_NEGATIVE",
                    "pointwise_disjoint": True,
                    "pointwise_exhaustive": True,
                    "strict_and_equality_predicates_restrict_continuously": True,
                    "dyadic_half_open_owner": "BOUND_BY_WHOLE_ORIGIN_ATOMIC_OWNER_AUDIT",
                    "analytic_equality_owner_applied_after_dyadic_owner": True,
                }))
    require(len(rows) == 26, "outer boundary 6+12+8")
    return rows


def reduction_binding(reduction: dict[str, Any]) -> dict[str, Any]:
    return {
        "category": reduction["category"],
        "residual_reason": reduction["residual_reason"],
        "closed": reduction["closed"],
        "disposition": reduction["disposition"],
        "eligible_targets": reduction["eligible_targets"],
        "candidate_evidence": reduction["candidate_evidence"],
    }


def validate_combined_candidate(
    candidate_row: dict[str, Any],
    ordinal: int,
    row: Any,
    reduction: dict[str, Any],
    evidence: dict[str, Any],
    c30a_row: dict[str, Any] | None,
) -> None:
    """Validate candidate fields stepwise against an independent truth table."""
    def step(condition: bool, layer: str) -> None:
        require(condition, "combined." + layer + ":" + row.key)

    expected_keys = {
        "schema", "cell_ordinal", "cell_key", "origin_key",
        "source_chart_id", "closed_box", "exact_volume", "active_targets",
        "source_kind", "upstream_binding", "centered_root_sign_evidence",
        "candidate_target", "candidate_is_frozen_owner",
        "target_strict_positive_first", "Delta_p_derivative_sign",
        "Delta_p_lower_face_sign", "Delta_p_upper_face_sign",
        "full_p_monotone_Delta_graph", "Delta_negative_leaf",
        "H_seam_evidence", "H_graph_bracket", "Delta_on_H_graph_bracket",
        "strict_graph_order", "Delta_H_intersection", "typed_H_geometry",
        "combined_strata", "combined_strata_sha256",
        "outer_boundary_restriction_rows",
        "outer_boundary_restriction_rows_sha256", "partition_theorem",
        "whole_closed_cell_disposition",
        "positive_measure_LIVE_open_side_proved",
        "positive_measure_EXCLUDED_open_side_proved", "candidate_credit",
        "formal_credit", "strict_nonpromotion", "row_sha256",
    }
    step(set(candidate_row) == expected_keys, "schema.keys")
    step(
        candidate_row["row_sha256"] == digest({
            key: value for key, value in candidate_row.items()
            if key != "row_sha256"
        }),
        "schema.row-closure",
    )
    step(
        (
            candidate_row["schema"],
            candidate_row["cell_ordinal"],
            candidate_row["cell_key"],
            candidate_row["origin_key"],
            candidate_row["source_chart_id"],
            candidate_row["closed_box"],
            candidate_row["exact_volume"],
            candidate_row["active_targets"],
        ) == (
            "cm2.round306c30c.source-w-full-delta-h.cell-row.v1",
            ordinal,
            row.key,
            row.origin_key,
            row.chart_id,
            r176.box_row(row.box),
            str(r215.box_volume(row.box)),
            list(row.active_targets),
        ),
        "identity",
    )

    records, centered = r215.enhance_root_sign_records(
        row, reduction["current_records"]
    )
    unresolved = [
        record for record in records
        if record.classification == "unresolved_discriminant"
    ]
    step(len(unresolved) == 1, "delta.unique-unresolved")
    delta_record = unresolved[0]
    target = TARGET_BY_ORIGIN[row.origin_key]
    derivative, lower, upper, full = r176.graph_faces(row, delta_record)
    step(
        delta_record.target_id == target
        and derivative == (1 if row.chart_id == "W:N" else -1)
        and r176.target_positive_first(delta_record, records)
        and evidence["target_strict_positive_first"] is True,
        "delta.pinned-truth",
    )
    blocker = evidence["blocker"]
    if blocker == "SINGLE_FULL_DELTA_NEGATIVE_SIDE_NOT_EXCLUDED":
        source_kind = "ROUND215_FULL_DELTA_NEGATIVE_SIDE"
        step(full is True and c30a_row is None, "source.full-delta")
    else:
        source_kind = "ROUND306C30A_CLIPPED_DELTA_RESIDUAL"
        step(
            blocker == "SINGLE_CLIPPED_DELTA_ENDPOINT_OVERWRAP"
            and full is False
            and c30a_row is not None
            and c30a_row["disposition"]
            == "RESIDUAL_NEGATIVE_OPEN_SIDE_NOT_EXCLUDED"
            and c30a_row["whole_closed_cell_excluded"] is False,
            "source.clipped-delta",
        )
    expected_upstream = {
        "Round215_evidence": evidence,
        "Round215_evidence_sha256": digest(evidence),
        "Round215_reduction_sha256": digest(reduction_binding(reduction)),
        "C30a_cell_row_sha256": (
            c30a_row["row_sha256"] if c30a_row is not None
            else "NOT_APPLICABLE_FULL_DELTA"
        ),
    }
    step(
        candidate_row["source_kind"] == source_kind
        and candidate_row["upstream_binding"] == expected_upstream,
        "source.binding",
    )
    step(
        candidate_row["centered_root_sign_evidence"] == centered
        and candidate_row["candidate_target"] == target
        and candidate_row["candidate_is_frozen_owner"] is False
        and candidate_row["target_strict_positive_first"] is True
        and candidate_row["Delta_p_derivative_sign"]
        == ("STRICT_POSITIVE" if derivative > 0 else "STRICT_NEGATIVE")
        and candidate_row["Delta_p_lower_face_sign"] == sign_name(lower)
        and candidate_row["Delta_p_upper_face_sign"] == sign_name(upper)
        and candidate_row["full_p_monotone_Delta_graph"] is full,
        "delta.fields",
    )
    negative = r176.classify_records(
        row.chart_id,
        row.box,
        [record for record in records if record.target_id != target],
    )
    expected_negative = {
        "classification": "unique_first",
        "unique_first_owner": r176.FROZEN_OWNER,
        "outgoing_disposition_requires_H_partition": True,
    }
    step(
        negative.classification == "unique_first"
        and negative.owner_target == r176.FROZEN_OWNER
        and candidate_row["Delta_negative_leaf"] == expected_negative,
        "delta.negative-leaf",
    )

    seam_id = SEAM_BY_CHART[row.chart_id]
    seam = local_seam_evidence(row.chart_id, row.box, seam_id)
    step(
        seam["typed_preconditions"] is True
        and seam["full_graph"] is True
        and seam["dH_dp_sign"] == "STRICT_NEGATIVE"
        and candidate_row["H_seam_evidence"] == seam,
        "h.seam",
    )
    bracket = independent_h_bracket(row, seam_id)
    step(candidate_row["H_graph_bracket"] == bracket, "h.bracket")
    collar = independent_delta_collar(row, target, bracket)
    step(
        candidate_row["Delta_on_H_graph_bracket"] == collar
        and collar["strict_on_entire_closed_t_s_p_bracket"] is True
        and "sampled_uniform_upgrade" not in candidate_row,
        "delta-h.uniform-collar",
    )
    expected_order = (
        "H_GRAPH_STRICTLY_BELOW_DELTA_GRAPH_WHERE_DELTA_GRAPH_EXISTS"
        if row.chart_id == "W:N" else
        "DELTA_GRAPH_STRICTLY_BELOW_H_GRAPH_WHERE_DELTA_GRAPH_EXISTS"
    )
    step(candidate_row["strict_graph_order"] == expected_order,
         "delta-h.graph-order")
    expected_intersection = {
        "predicate": "Delta=0 AND H=0",
        "nominal_dimension_if_nonempty": 1,
        "status": "EMPTY_CERTIFIED",
        "certificate": "DELTA_STRICT_NEGATIVE_ON_CLOSED_H_BRACKET",
        "all_outer_face_edge_vertex_restrictions_empty": True,
        "integer_credit": 0,
    }
    step(
        candidate_row["Delta_H_intersection"] == expected_intersection,
        "delta-h.empty-intersection",
    )

    typed = local_complete_typed_strata(
        seam, row.key + "#FULL_DELTA_H"
    )
    expected_typed = {
        "use_scope": (
            "GEOMETRY_AND_INCIDENCE_ONLY_UNTIL_RESTRICTED_BY_DELTA_NEGATIVE"
        ),
        "standalone_H_side_disposition_credit": 0,
        "open_3D_sides": typed["open_3D_sides"],
        "H_zero_2D_sheet": typed["H_zero_2D_sheet"],
        "H_zero_1D_face_incidences": typed[
            "H_zero_1D_face_incidences"
        ],
        "terminal_face_2D_H_sign_regions": typed[
            "terminal_face_2D_H_sign_regions"
        ],
        "H_zero_0D_edge_incidences": typed[
            "H_zero_0D_edge_incidences"
        ],
        "terminal_edge_1D_H_sign_intervals": typed[
            "terminal_edge_1D_H_sign_intervals"
        ],
        "H_zero_0D_corner_absence_rows": typed[
            "H_zero_0D_corner_absence_rows"
        ],
    }
    step(candidate_row["typed_H_geometry"] == expected_typed,
         "h.typed-complex")

    truth_table = (
        (
            "Delta>0", 3,
            "NONEMPTY_ON_EVERY_BASE_FIBRE" if full
            else "NOT_REQUIRED_FOR_COMPLETE_DISPOSITION",
            "EXCLUDED_UNIQUE_FIRST_G_OWNER_MISMATCH", target,
        ),
        (
            "Delta=0", 2,
            "NONEMPTY_FULL_MONOTONE_GRAPH" if full
            else "NOT_REQUIRED_FOR_COMPLETE_DISPOSITION",
            "EXCLUDED_UNIQUE_FIRST_G_TANGENCY_OWNER_MISMATCH", target,
        ),
        (
            "Delta<0 AND " + LIVE_H_SIGN_BY_CHART[row.chart_id], 3,
            "STRICT_POSITIVE_MEASURE_BY_H_BRACKET_FACE_AND_CONTINUITY",
            "LIVE_W_STAGE_ONE_OWNER_CHART_MATCH", r176.FROZEN_OWNER,
        ),
        (
            "Delta<0 AND H=0", 2, "NONEMPTY_UNIQUE_FULL_H_GRAPH",
            "LIVE_W_HALF_OPEN_SEAM_OWNER", "W",
        ),
        (
            "Delta<0 AND " + MISMATCH_H_SIGN_BY_CHART[row.chart_id], 3,
            "STRICT_POSITIVE_MEASURE_BY_H_BRACKET_FACE_AND_CONTINUITY",
            "EXCLUDED_OUTGOING_CHART_MISMATCH",
            "N" if row.chart_id == "W:N" else "S",
        ),
    )
    strata = candidate_row["combined_strata"]
    step(type(strata) is list and len(strata) == 5,
         "truth-table.cardinality")
    for stratum, truth in zip(strata, truth_table, strict=True):
        step(
            set(stratum) == {
                "schema", "cell_key", "predicate", "ambient_dimension",
                "nonemptiness", "disposition", "owner", "row_sha256",
            }
            and stratum["row_sha256"] == digest({
                key: value for key, value in stratum.items()
                if key != "row_sha256"
            })
            and (
                stratum["schema"], stratum["cell_key"],
                stratum["predicate"], stratum["ambient_dimension"],
                stratum["nonemptiness"], stratum["disposition"],
                stratum["owner"],
            ) == (
                "cm2.round306c30c.combined-predicate-stratum.v1",
                row.key, *truth,
            ),
            "truth-table.row",
        )
    step(
        [truth[0] for truth in truth_table]
        == [
            "Delta>0", "Delta=0",
            "Delta<0 AND " + LIVE_H_SIGN_BY_CHART[row.chart_id],
            "Delta<0 AND H=0",
            "Delta<0 AND " + MISMATCH_H_SIGN_BY_CHART[row.chart_id],
        ]
        and candidate_row["combined_strata_sha256"] == digest(strata),
        "truth-table.partition",
    )

    boundary = independent_boundary_rows(row)
    step(
        candidate_row["outer_boundary_restriction_rows"] == boundary
        and candidate_row["outer_boundary_restriction_rows_sha256"]
        == digest(boundary)
        and Counter(item["ambient_dimension"] for item in boundary)
        == Counter({2: 6, 1: 12, 0: 8})
        and all(
            item["Delta_zero_AND_H_zero"]
            == "EMPTY_BY_CLOSED_H_BRACKET_DELTA_NEGATIVE"
            for item in boundary
        ),
        "boundary.26-exact-restrictions",
    )
    step(
        candidate_row["partition_theorem"] == {
            "five_predicate_strata_pointwise_disjoint": True,
            "five_predicate_strata_pointwise_exhaustive": True,
            "Delta_zero_H_zero_intersection_empty": True,
            "all_3D_2D_1D_0D_outer_restrictions_disposed": True,
            "dyadic_half_open_owner_deferred_to_origin_atomic_audit": True,
            "H_zero_half_open_owner": "W",
            "whole_closed_cell_disposition": "MIXED",
        }
        and candidate_row["whole_closed_cell_disposition"] == "MIXED"
        and candidate_row["positive_measure_LIVE_open_side_proved"] is True
        and candidate_row["positive_measure_EXCLUDED_open_side_proved"] is True,
        "theorem",
    )
    step(
        candidate_row["candidate_credit"] == {
            "combined_Delta_H_cell_disposition": 1,
            "resolved_source_W_origin_disposition": 0,
            "whole_source_W_origin_exclusion": 0,
        }
        and candidate_row["formal_credit"] == {
            "combined_Delta_H_cell_disposition": 0,
            "resolved_source_W_origin_disposition": 0,
            "whole_source_W_origin_exclusion": 0,
        }
        and candidate_row["strict_nonpromotion"]
        == "AWAIT_INDEPENDENT_VERIFIER_AND_SEALED_MANIFEST",
        "credit.nonpromotion",
    )

def parse_c30b_manifest_bytes(raw: bytes) -> dict[str, str]:
    require(
        hashlib.sha256(raw).hexdigest() == C30B_MANIFEST_SHA256,
        "C30b sealed manifest hash",
    )
    try:
        lines = raw.decode("ascii").splitlines()
    except UnicodeDecodeError as error:
        raise Reject("C30b sealed manifest ASCII") from error
    rows: dict[str, str] = {}
    for line in lines:
        parts = line.split("  ", 1)
        require(
            len(parts) == 2
            and len(parts[0]) == 64
            and all(character in "0123456789abcdef" for character in parts[0])
            and parts[1]
            and not Path(parts[1]).is_absolute()
            and ".." not in Path(parts[1]).parts
            and parts[1] not in rows,
            "C30b sealed manifest syntax",
        )
        rows[parts[1]] = parts[0]
    require(
        rows == C30B_MANIFEST_MEMBER_PINS and len(rows) == 14,
        "C30b sealed manifest exact member set",
    )
    return rows


def validate_c30b_seal_tree(
    authority_root: Path,
    sealed_dir: Path,
    manifest_path: Path,
    *,
    enforce_fixed_authority: bool,
) -> dict[str, Any]:
    authority_root = Path(os.path.abspath(os.fspath(authority_root)))
    sealed_dir = Path(os.path.abspath(os.fspath(sealed_dir)))
    manifest_path = Path(os.path.abspath(os.fspath(manifest_path)))
    fixed = ROOT / C30B_SEALED_DIRNAME
    fixed_manifest = ROOT / C30B_MANIFEST
    if enforce_fixed_authority:
        require(
            authority_root == ROOT
            and sealed_dir == fixed
            and manifest_path == fixed_manifest,
            "C30b sealed fixed path authority",
        )
    root_status = authority_root.lstat()
    require(
        stat.S_ISDIR(root_status.st_mode)
        and not authority_root.is_symlink()
        and authority_root.resolve(strict=True) == authority_root,
        "C30b seal authority root directory",
    )
    status_before = sealed_dir.lstat()
    directory_identity = (
        status_before.st_dev, status_before.st_ino, status_before.st_mode,
        status_before.st_nlink, status_before.st_mtime_ns,
        status_before.st_ctime_ns,
    )
    require(
        stat.S_ISDIR(status_before.st_mode)
        and not sealed_dir.is_symlink()
        and sealed_dir.parent.resolve(strict=True) == authority_root,
        "C30b sealed fixed directory authority",
    )
    require(
        {member.name for member in sealed_dir.iterdir()}
        == set(C30B_SEALED_FILE_PINS),
        "C30b sealed exact directory member set",
    )
    manifest_raw, _manifest_identity = race_checked_single_read(
        manifest_path, C30B_MANIFEST, authority_root
    )
    manifest_rows = parse_c30b_manifest_bytes(manifest_raw)
    captured: dict[str, bytes] = {}
    for relative, expected in sorted(manifest_rows.items()):
        member = authority_root / relative
        if (
            enforce_fixed_authority
            and relative == C30B_VERIFIER
            and C30B_VERIFIER_CAPTURE is not None
        ):
            raw, identity = C30B_VERIFIER_CAPTURE
            require_capture_still_current(member, identity, relative)
        else:
            raw, _identity = race_checked_single_read(
                member, relative, authority_root
            )
        require(
            hashlib.sha256(raw).hexdigest() == expected,
            "C30b sealed member hash:" + relative,
        )
        captured[relative] = raw
    status_after = sealed_dir.lstat()
    require(
        directory_identity == (
            status_after.st_dev, status_after.st_ino, status_after.st_mode,
            status_after.st_nlink, status_after.st_mtime_ns,
            status_after.st_ctime_ns,
        )
        and {member.name for member in sealed_dir.iterdir()}
        == set(C30B_SEALED_FILE_PINS),
        "C30b sealed directory unchanged during capture",
    )
    verification_raw = captured[C30B_VERIFICATION]
    result_raw = captured[C30B_SEALED_DIRNAME + "/" + C30B_RESULT]
    verification = json.loads(verification_raw)
    require(type(verification) is dict, "C30b sealed verification JSON object")
    result = json.loads(result_raw)
    require(type(result) is dict, "C30b sealed result JSON object")
    result_body = {
        key: value for key, value in result.items() if key != "result_sha256"
    }
    require(
        hashlib.sha256(captured[C30B_PRODUCER]).hexdigest()
        == C30B_PRODUCER_SHA256
        and hashlib.sha256(captured[C30B_VERIFIER]).hexdigest()
        == C30B_VERIFIER_SHA256
        and hashlib.sha256(verification_raw).hexdigest()
        == C30B_VERIFICATION_SHA256
        and hashlib.sha256(result_raw).hexdigest() == C30B_RESULT_FILE_SHA256,
        "C30b sealed authority direct file hashes",
    )
    require(
        verification["status"]
        == ("PASS_FORMAL_C30B__688_H_CELLS__2_WHOLE_ORIGIN_EXCLUSIONS__"
            "10_RESOLVED_MIXED__SOURCE_W_92_TO_80__D02_STILL_BLOCKED")
        and verification["manifest"]["expected_member_count"] == 14
        and verification["published_outputs"]["result_object_sha256"]
        == C30B_RESULT_OBJECT_SHA256
        and verification["source_W_ledger_transition"]["after"]["remaining"] == 80
        and wire(result) == result_raw
        and result["result_sha256"] == C30B_RESULT_OBJECT_SHA256
        and digest(result_body) == C30B_RESULT_OBJECT_SHA256
        and result["status"] == "PASS_BOUNDED_ROUND306C30B_OUTGOING_H_DISPOSITION"
        and result["source_W_ledger_transition"]["after"] == {
            "conservative_live": 2086,
            "excluded": 74746,
            "remaining": 80,
            "remaining_partition": {
                "compact_q": 54, "full_Delta": 2, "multi_Delta": 20,
                "reduced_live": 2, "retained_source_seams": 2,
            },
            "resolved_nonexcluded": 2006,
            "total": 76832,
        }
        and result["strict_nonpromotion"]["D02"]
        == "BLOCKED_BY_80_REMAINING_SOURCE_W_ORIGINS_AND_COMPOSITE_GATE",
        "C30b sealed verification/result 80-baseline handoff",
    )
    return {
        "manifest_sha256": C30B_MANIFEST_SHA256,
        "verification_sha256": C30B_VERIFICATION_SHA256,
        "producer_sha256": C30B_PRODUCER_SHA256,
        "independent_verifier_sha256": C30B_VERIFIER_SHA256,
        "result_file_sha256": C30B_RESULT_FILE_SHA256,
        "result_object_sha256": C30B_RESULT_OBJECT_SHA256,
        "sealed_member_count": len(C30B_SEALED_FILE_PINS),
        "manifest_member_count": len(C30B_MANIFEST_MEMBER_PINS),
        "formal_source_W_remaining": 80,
    }


def validate_c30b_seal_path(path: Path) -> dict[str, Any]:
    absolute = Path(os.path.abspath(os.fspath(path)))
    fixed = ROOT / C30B_SEALED_DIRNAME
    require(absolute == fixed, "C30b sealed fixed path authority")
    return validate_c30b_seal_tree(
        ROOT, fixed, ROOT / C30B_MANIFEST, enforce_fixed_authority=True
    )


def validate_c30b_seal() -> dict[str, Any]:
    return validate_c30b_seal_path(ROOT / C30B_SEALED_DIRNAME)


def independent_prior_partition(
    replay: dict[str, Any], origin: str, frontier_keys: set[str]
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    evidence = sorted(replay["prior"][origin], key=lambda row: row["leaf_key"])
    by_key = {row["leaf_key"]: row for row in evidence}
    boxes: dict[str, Any] = {}
    faces: list[dict[str, Any]] = []
    source = replay["origins"][origin]
    pending = [(source["box"], 0)]
    while pending:
        box, depth = pending.pop()
        key = f"{source['chart_id']}:{box.path}"
        if key in by_key:
            require(by_key[key]["relative_depth"] == depth, "prior depth")
            boxes[key] = box
            continue
        if depth == 6:
            require(key in frontier_keys, "prior/frontier identity")
            continue
        lower, upper = r176.split(box)
        parent = r176.Frontier(
            source["chart_id"], box, (), origin, "ROUND176_PARTITION_SPLIT"
        )
        faces.append(r180.split_face(
            parent, r180.split_axis(box), lower, upper
        ))
        pending.extend(((lower, depth + 1), (upper, depth + 1)))
    faces.sort(key=lambda value: value["parent_cell_key"])
    require(set(boxes) == set(by_key), "independent prior boxes")
    return boxes, faces


@dataclass(frozen=True)
class OriginContext:
    origin: str
    registry: dict[str, Any]
    source_box: Any
    roots: tuple[Any, ...]
    base_rows: tuple[Any, ...]
    refinement: dict[str, Any]
    leaves: dict[str, Any]
    prior_boxes: dict[str, Any]
    prior_faces: tuple[dict[str, Any], ...]
    h_sources: tuple[tuple[str, Any, dict[str, Any]], ...]
    direct_live: tuple[dict[str, Any], ...]
    combined_sources: tuple[tuple[Any, dict[str, Any], dict[str, Any], dict[str, Any] | None], ...]
    final_closed_sources: dict[str, str]


@dataclass(frozen=True)
class Reference:
    input_pins: tuple[tuple[str, str], ...]
    c30b_authority: Any
    replay: Any
    contexts: Any


def reconstruct_reference() -> Reference:
    require(
        PRODUCER[:-3] not in sys.modules
        and C30B_PRODUCER[:-3] not in sys.modules,
        "producer independence before reconstruction",
    )
    base.validate_runtime()
    base.validate_imported_mathematics()
    pins = base.validate_sources()
    c30b_authority = validate_c30b_seal()
    r184 = base.pinned_pretty_json(ROOT / base.R184_CERTIFICATE)
    registry = {
        row["origin_key"]: row
        for row in r184["result"]["priority_registry"]["rows"]
        if row["origin_key"] in set(ORIGIN_KEYS)
    }
    bounded = base.pinned_pretty_json(ROOT / base.R215_CERTIFICATE)["result"][
        "bounded_probe_result"
    ]
    summaries = {
        row["origin_key"]: row
        for row in bounded["whole_origin_outcome"]["per_origin_rows"]
        if row["origin_key"] in set(ORIGIN_KEYS)
    }
    c30a_rows_all = canonical_rows(base.C30A_SEALED / base.C30A_CELL)
    c30a_rows = {
        row["cell_key"]: row
        for row in c30a_rows_all
        if row["origin_key"] in set(ORIGIN_KEYS)
    }
    require(
        set(registry) == set(ORIGIN_KEYS)
        and [registry[key]["priority_ordinal"] for key in ORIGIN_KEYS]
        == [1234, 1235]
        and set(summaries) == set(ORIGIN_KEYS)
        and all(
            row["Round201_residual_cell_count"] == 50
            and row["Round215_analytic_closed_cell_count"] == 0
            and row["Round215_blocker_count"] == {
                "SINGLE_CLIPPED_DELTA_ENDPOINT_OVERWRAP": 20,
                "SINGLE_FULL_DELTA_NEGATIVE_SIDE_NOT_EXCLUDED": 30,
            }
            for row in summaries.values()
        )
        and len(c30a_rows) == 40,
        "pinned full-Delta selection",
    )
    replay = r176.replay_frontier()
    roots_by_origin: dict[str, list[Any]] = defaultdict(list)
    base_by_origin: dict[str, list[Any]] = defaultdict(list)
    for row in replay["frontier"]:
        if row.origin_key not in set(ORIGIN_KEYS):
            continue
        kind, _evidence = r176.closure(row)
        if kind is None:
            roots_by_origin[row.origin_key].append(row)
        else:
            require(kind == "EXCLUDED", "Round176 preclosure")
            base_by_origin[row.origin_key].append(row)
    contexts: dict[str, OriginContext] = {}
    for origin in ORIGIN_KEYS:
        roots = tuple(sorted(roots_by_origin[origin], key=lambda row: row.key))
        base_rows = tuple(sorted(
            base_by_origin[origin], key=lambda row: row.key
        ))
        require(len(roots) == 61 and len(base_rows) == 3, "R176 census")
        refinement = r180.refine_origin(list(roots), 4)
        leaves = r215.reconstruct_refinement_leaf_frontiers(
            list(roots), refinement
        )
        frontier_keys = {row.key for row in roots + base_rows}
        prior_boxes, prior_faces = independent_prior_partition(
            replay, origin, frontier_keys
        )
        h_sources: list[tuple[str, Any, dict[str, Any]]] = []
        direct_live: list[dict[str, Any]] = []
        for evidence in sorted(
            refinement["terminal_rows"], key=lambda row: row["cell_key"]
        ):
            if evidence["coarse_disposition"] == "EXCLUDED":
                continue
            frontier = leaves["terminal"][evidence["cell_key"]]
            if evidence["method"] == "DIRECT_STRICT_CLOSED_BOX":
                require(evidence["coarse_disposition"] == "LIVE", "direct LIVE")
                direct_live.append(evidence)
                continue
            binding = {
                "Round180_terminal_evidence": evidence,
                "Round180_terminal_sha256": evidence["terminal_sha256"],
            }
            if evidence["method"] == "OUTGOING_H_CLOSED_RECTANGLE_TREE":
                source_kind = "ROUND180_INHERITED_OUTGOING_H"
            else:
                require(
                    evidence["method"] == "SAME_SIGN_MONOTONE_DELTA_CLOSED_BOX"
                    and evidence["coarse_disposition"] == "MIXED"
                    and evidence["Delta_zero_graph_inside_closed_box"] is False
                    and evidence["empty_2D_graph_edge_and_corner_ledger"] is True
                    and evidence["witness"] == "FOLLOWUP_H_PARTITION",
                    "same-sign Delta followup H",
                )
                source_kind = "ROUND180_INHERITED_SAME_SIGN_DELTA_FOLLOWUP_H"
                binding["Round180_same_sign_Delta_followup"] = {
                    "method": evidence["method"],
                    "target": evidence["target"],
                    "derivative_sign": evidence["derivative_sign"],
                    "strict_common_face_sign": evidence["strict_common_face_sign"],
                    "Delta_p_lower_face_sign": evidence["strict_common_face_sign"],
                    "Delta_p_upper_face_sign": evidence["strict_common_face_sign"],
                    "Delta_zero_graph_inside_closed_box": False,
                    "empty_2D_graph_edge_and_corner_ledger": True,
                    "witness": evidence["witness"],
                }
            h_sources.append((source_kind, frontier, binding))
        combined: list[tuple[Any, dict[str, Any], dict[str, Any], dict[str, Any] | None]] = []
        final_closed: dict[str, str] = {}
        for row in sorted(
            refinement["final_residual_rows"], key=lambda value: value.key
        ):
            reduction = r215.exact_behind_reduce(
                row, r180.residual_category(row)
            )
            if reduction["closed"]:
                final_closed[row.key] = "ROUND201_EXACT_BEHIND_EXCLUDED"
                continue
            evidence = r215.analyze_residual_cell(row, reduction)
            require(evidence["analytic_closed"] is False, "no R215 closure")
            clipped = c30a_rows.get(row.key)
            if evidence["blocker"] == "SINGLE_CLIPPED_DELTA_ENDPOINT_OVERWRAP":
                require(clipped is not None, "C30a clipped binding")
                if clipped["whole_closed_cell_excluded"]:
                    final_closed[row.key] = "ROUND306C30A_CLIPPED_DELTA_EXCLUDED"
                    continue
            else:
                require(
                    evidence["blocker"]
                    == "SINGLE_FULL_DELTA_NEGATIVE_SIDE_NOT_EXCLUDED"
                    and clipped is None,
                    "full Delta blocker",
                )
            combined.append((row, reduction, evidence, clipped))
        require(
            len(prior_boxes) == 0
            and len(h_sources) == 44
            and len(direct_live) == 11
            and len(combined) == 40
            and Counter(final_closed.values()) == Counter({
                "ROUND201_EXACT_BEHIND_EXCLUDED": 328,
                "ROUND306C30A_CLIPPED_DELTA_EXCLUDED": 10,
            }),
            "independent origin composition census",
        )
        contexts[origin] = OriginContext(
            origin, registry[origin], replay["origins"][origin]["box"],
            roots, base_rows, refinement, leaves,
            prior_boxes, tuple(prior_faces), tuple(h_sources),
            tuple(direct_live), tuple(combined), final_closed,
        )
    expected_pins = sorted(
        pins + [
            {"filename": C30B_PRODUCER, "sha256": C30B_PRODUCER_SHA256},
            {"filename": C30B_VERIFIER, "sha256": C30B_VERIFIER_SHA256},
            {"filename": C30B_MANIFEST, "sha256": C30B_MANIFEST_SHA256},
            {
                "filename": C30B_VERIFICATION,
                "sha256": C30B_VERIFICATION_SHA256,
            },
            {
                "filename": C30B_SEALED_DIRNAME + "/" + C30B_RESULT,
                "sha256": C30B_RESULT_FILE_SHA256,
            },
        ],
        key=lambda row: row["filename"],
    )
    require(
        PRODUCER[:-3] not in sys.modules
        and C30B_PRODUCER[:-3] not in sys.modules,
        "producer independence after reconstruction",
    )
    return Reference(
        tuple((row["filename"], row["sha256"]) for row in expected_pins),
        MappingProxyType(c30b_authority),
        replay,
        MappingProxyType(contexts),
    )


def local_h_terminal(chart_id: str, box: Any) -> tuple[str | None, dict[str, Any]]:
    cell, nx, ny = r176.tight_contact(chart_id, box)
    if cell is not None:
        margins = {
            "E.first": nx - ny, "E.second": nx + ny,
            "W.first": -nx - ny, "W.second": -nx + ny,
            "N.first": ny - nx, "N.second": ny + nx,
            "S.first": -ny - nx, "S.second": -ny + nx,
        }
        classification = (
            "STRICT_PREFIX_STAGE_ONE_MATCH_RECTANGLE" if cell == "W"
            else "STRICT_OUTGOING_CHART_MISMATCH_RECTANGLE"
        )
        return classification, {
            "method": "STRICT_OUTGOING_NORMAL_RECTANGLE",
            "outgoing_chart": cell,
            "outgoing_margin_signs": {
                key: sign_name(value) for key, value in sorted(margins.items())
            },
        }
    candidates = [
        local_seam_evidence(chart_id, box, seam_id)
        for seam_id in sorted(r176.SEAMS)
    ]
    separated = [
        row for row in candidates
        if row["typed_preconditions"]
        and row["uniform_outgoing_chart"] is not None
    ]
    typed = [
        row for row in candidates
        if row["typed_preconditions"]
        and (row["full_graph"] or row["clipped_graph"])
    ]
    if len(separated) == 1 and not typed:
        chosen = separated[0]
        return (
            "MONOTONE_H_PREFIX_STAGE_ONE_MATCH_RECTANGLE"
            if chosen["uniform_outgoing_chart"] == "W" else
            "MONOTONE_H_OUTGOING_CHART_MISMATCH_RECTANGLE"
        ), {
            "method": "MONOTONE_H_STRICT_SIGN_RECTANGLE",
            "seam_evidence": chosen,
            "outgoing_chart": chosen["uniform_outgoing_chart"],
        }
    if len(typed) == 1 and not separated:
        return LOCAL_H_TYPED, {
            "method": "TYPED_H_GRAPH_AND_TWO_OPEN_SIDES",
            "seam_evidence": typed[0],
        }
    return None, {"method": "UNRESOLVED_H_INTERVAL", "candidates": candidates}


def local_internal_split_lower_strata(
    faces: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    axes = ("t", "p", "s")
    line_groups: dict[str, dict[str, Any]] = {}
    point_groups: dict[str, dict[str, Any]] = {}
    for face in faces:
        face_axis = face["axis"]
        span_axes = [axis for axis in axes if axis != face_axis]
        for boundary_axis in span_axes:
            free_axis = next(axis for axis in span_axes if axis != boundary_axis)
            for endpoint, coordinate in zip(
                ("LOWER", "UPPER"), face["spans"][boundary_axis]
            ):
                geometry = {
                    "fixed_coordinates": {
                        face_axis: face["coordinate"],
                        boundary_axis: coordinate,
                    },
                    "free_axis": free_axis,
                    "free_span": face["spans"][free_axis],
                }
                key = wire(geometry).decode("ascii")
                group = line_groups.setdefault(key, {
                    "geometry": geometry, "owners": [], "nonowners": [],
                    "faces": [], "orientations": [],
                })
                group["owners"].append(face["lower_child_owner"])
                group["nonowners"].append(face["upper_child_nonowner"])
                group["faces"].append(face["face_sha256"])
                group["orientations"].append({
                    "incident_split_face_sha256": face["face_sha256"],
                    "split_face_axis": face_axis,
                    "boundary_axis": boundary_axis,
                    "boundary_endpoint": endpoint,
                    "lower_child_owner": face["lower_child_owner"],
                    "upper_child_nonowner": face["upper_child_nonowner"],
                })
        for first_endpoint, first_value in zip(
            ("LOWER", "UPPER"), face["spans"][span_axes[0]]
        ):
            for second_endpoint, second_value in zip(
                ("LOWER", "UPPER"), face["spans"][span_axes[1]]
            ):
                geometry = {"fixed_coordinates": {
                    face_axis: face["coordinate"],
                    span_axes[0]: first_value,
                    span_axes[1]: second_value,
                }}
                key = wire(geometry).decode("ascii")
                group = point_groups.setdefault(key, {
                    "geometry": geometry, "owners": [], "nonowners": [],
                    "faces": [], "orientations": [],
                })
                group["owners"].append(face["lower_child_owner"])
                group["nonowners"].append(face["upper_child_nonowner"])
                group["faces"].append(face["face_sha256"])
                group["orientations"].append({
                    "incident_split_face_sha256": face["face_sha256"],
                    "split_face_axis": face_axis,
                    "boundary_endpoints": {
                        span_axes[0]: first_endpoint,
                        span_axes[1]: second_endpoint,
                    },
                    "lower_child_owner": face["lower_child_owner"],
                    "upper_child_nonowner": face["upper_child_nonowner"],
                })

    def close_group(
        group: dict[str, Any], dimension: int, schema: str
    ) -> dict[str, Any]:
        orientations = sorted(group["orientations"], key=wire)
        return sealed({
            "schema": schema,
            **group["geometry"],
            "ambient_dimension": dimension,
            "half_open_owner_prefix": min(group["owners"]),
            "incident_lower_child_owners": sorted(set(group["owners"])),
            "incident_upper_child_nonowners": sorted(set(group["nonowners"])),
            "incident_split_face_sha256": sorted(set(group["faces"])),
            "incident_split_face_count": len(set(group["faces"])),
            "incident_orientations": orientations,
            "incident_orientations_sha256": digest(orientations),
            "half_open_rule": (
                "LOWER_CHILD_OWNS_SPLIT_EQUALITY__"
                "LEXICOGRAPHIC_LEAST_INCIDENT_LOWER_CHILD"
            ),
        })

    lines = [
        close_group(
            group, 1,
            "cm2.round306c30b.internal-split-face-edge-owner.row.v1",
        )
        for _key, group in sorted(line_groups.items())
    ]
    points = [
        close_group(
            group, 0,
            "cm2.round306c30b.internal-split-face-corner-owner.row.v1",
        )
        for _key, group in sorted(point_groups.items())
    ]
    lines.sort(key=wire)
    points.sort(key=wire)
    return lines, points


def local_h_tree(source: Any) -> dict[str, Any]:
    pending = [(source.box, 0)]
    terminals: list[dict[str, Any]] = []
    terminal_boxes: dict[str, Any] = {}
    split_faces: list[dict[str, Any]] = []
    while pending:
        box, depth = pending.pop()
        classification, evidence = local_h_terminal(source.chart_id, box)
        if classification is not None:
            terminal_id = f"{source.chart_id}:{box.path}"
            coarse = (
                "EXCLUDED" if classification in LOCAL_H_EXCLUSION_CLASSES
                else "LIVE" if classification in LOCAL_H_LIVE_CLASSES
                else "MIXED"
            )
            body = {
                "schema": "cm2.round306c30b.H-terminal-rectangle.row.v1",
                "terminal_id": terminal_id,
                "relative_depth": depth,
                "closed_box": r176.box_row(box),
                "exact_volume": str(r215.box_volume(box)),
                "classification": classification,
                "coarse_disposition": coarse,
                "analytic_evidence": evidence,
            }
            if classification == LOCAL_H_TYPED:
                body["typed_strata"] = local_complete_typed_strata(
                    evidence["seam_evidence"], terminal_id
                )
            terminals.append(sealed(body))
            terminal_boxes[terminal_id] = box
            continue
        require(depth < 4, "C30c local H depth exhaustion:" + source.key)
        t_width = (box.t1 - box.t0) / (r176.T_UPPER - r176.T_LOWER)
        p_width = (box.p1 - box.p0) / (r176.P_UPPER - r176.P_LOWER)
        axis = 0 if t_width >= p_width else 1
        lower, upper = r176.split(box, axis)
        parent = r176.Frontier(
            source.chart_id, box, (r176.FROZEN_OWNER,), source.origin_key,
            "OUTGOING_CHART_SEAM_OVERWRAP",
        )
        split_faces.append(r180.split_face(parent, axis, lower, upper))
        pending.extend(((lower, depth + 1), (upper, depth + 1)))
    terminals.sort(key=lambda row: row["terminal_id"])
    split_faces.sort(key=lambda row: row["parent_cell_key"])
    lines, points = local_internal_split_lower_strata(split_faces)
    census = Counter(row["coarse_disposition"] for row in terminals)
    whole = (
        "EXCLUDED" if set(census) == {"EXCLUDED"}
        else "LIVE" if set(census) == {"LIVE"} else "MIXED"
    )
    coverage = sum(Q(1, 2 ** row["relative_depth"]) for row in terminals)
    volume = sum(Q(row["exact_volume"]) for row in terminals)
    require(
        coverage == 1 and volume == r215.box_volume(source.box),
        "C30c local H volume/coverage:" + source.key,
    )
    return {
        "terminals": terminals,
        "terminal_boxes": terminal_boxes,
        "split_faces": split_faces,
        "split_lines": lines,
        "split_points": points,
        "census": census,
        "whole": whole,
        "volume": volume,
    }


def local_terminal_atomic_owner_reclosure(
    label: str,
    parent: Any,
    leaf_boxes: dict[str, Any],
    proof_source: dict[str, str],
    dispositions: dict[str, str],
    round176_faces: list[dict[str, Any]],
    round180_faces: list[dict[str, Any]],
    *,
    audit_scope: str = "WHOLE_ORIGIN_LINEAGE",
    leaf_key_kind: str = "CELL_KEY",
) -> dict[str, Any]:
    """Locally reclose a terminal tree and every induced lower stratum.

    This does not call or import any C30b owner-audit helper.  The candidate
    audit object is rebuilt from local terminal boxes, split faces,
    dispositions, and terminal-row proof bindings only.
    """
    require(
        bool(leaf_boxes)
        and len(leaf_boxes) == len(set(leaf_boxes))
        and
        set(leaf_boxes) == set(dispositions) == set(proof_source),
        "complete 3D leaf maps:" + label,
    )

    axes = ("t", "p", "s")
    bounds = {
        key: {
            "t": (box.t0, box.t1),
            "p": (box.p0, box.p1),
            "s": (box.s0, box.s1),
        }
        for key, box in leaf_boxes.items()
    }
    parent_bounds = {
        "t": (parent.t0, parent.t1),
        "p": (parent.p0, parent.p1),
        "s": (parent.s0, parent.s1),
    }

    # Closed 3D boxes are an exhaustive partition once containment, positive
    # volume, strict-interior disjointness, and exact total volume all hold.
    leaf_volume_rows: list[dict[str, Any]] = []
    leaf_volume = Q(0)
    for key in sorted(leaf_boxes):
        box = leaf_boxes[key]
        require(
            all(
                parent_bounds[axis][0] <= bounds[key][axis][0]
                < bounds[key][axis][1] <= parent_bounds[axis][1]
                for axis in axes
            ),
            "3D leaf parent containment:" + key,
        )
        volume = r215.box_volume(box)
        require(volume > 0, "positive 3D leaf volume:" + key)
        leaf_volume += volume
        leaf_volume_rows.append({
            "cell_key": key,
            "closed_box": r176.box_row(box),
            "exact_volume": str(volume),
            "disposition": dispositions[key],
            "proof_source": proof_source[key],
        })
    parent_volume = r215.box_volume(parent)
    require(leaf_volume == parent_volume, "exact 3D leaf volume sum:" + label)

    pair_count = 0
    pair_hash = hashlib.sha256()
    pair_hash.update(b"[")
    ordered_keys = sorted(leaf_boxes)
    for first_ordinal, first in enumerate(ordered_keys):
        for second in ordered_keys[first_ordinal + 1:]:
            interior_overlap = all(
                max(bounds[first][axis][0], bounds[second][axis][0])
                < min(bounds[first][axis][1], bounds[second][axis][1])
                for axis in axes
            )
            require(
                not interior_overlap,
                "strict-interior 3D leaf overlap:" + first + ":" + second,
            )
            pair_row = {
                "first": first,
                "second": second,
                "interior_overlap": interior_overlap,
            }
            if pair_count:
                pair_hash.update(b",")
            pair_hash.update(wire(pair_row))
            pair_count += 1
    pair_hash.update(b"]")
    require(
        pair_count == len(leaf_boxes) * (len(leaf_boxes) - 1) // 2,
        "complete 3D pair census:" + label,
    )
    three_dimensional_reclosure = {
        "closed_leaf_count": len(leaf_boxes),
        "closed_leaf_rows_sha256": digest(leaf_volume_rows),
        "closed_leaf_pair_count": pair_count,
        "closed_leaf_pair_rows_sha256": pair_hash.hexdigest(),
        "parent_exact_volume": str(parent_volume),
        "closed_leaf_exact_volume_sum": str(leaf_volume),
        "all_closed_leaves_contained_in_parent": True,
        "all_closed_leaf_strict_interiors_pairwise_disjoint": True,
        "closed_leaf_union_exhausts_parent_by_exact_volume": True,
    }
    three_dimensional_reclosure["reclosure_sha256"] = digest(
        three_dimensional_reclosure
    )

    grid = {
        axis: sorted({value for item in bounds.values() for value in item[axis]})
        for axis in axes
    }
    require(
        all(
            values and values[0] == parent_bounds[axis][0]
            and values[-1] == parent_bounds[axis][1]
            for axis, values in grid.items()
        ),
        "axis grid spans parent:" + label,
    )

    def cuts(axis: str, lower: Q, upper: Q) -> list[Q]:
        values = [lower] + [
            value for value in grid[axis] if lower < value < upper
        ] + [upper]
        require(
            lower < upper and values == sorted(set(values)),
            "strict atomic grid cuts:" + label,
        )
        return values

    def containing_owner(
        fixed: dict[str, Q], open_spans: dict[str, tuple[Q, Q]]
    ) -> str:
        require(
            set(fixed).isdisjoint(open_spans)
            and set(fixed) | set(open_spans) == set(axes),
            "atomic geometry axes:" + label,
        )
        midpoints = {
            axis: (span[0] + span[1]) / 2
            for axis, span in open_spans.items()
        }
        midpoint_candidates = sorted(
            key for key, item in bounds.items()
            if all(item[axis][0] <= value <= item[axis][1]
                   for axis, value in fixed.items())
            and all(item[axis][0] < value < item[axis][1]
                    for axis, value in midpoints.items())
        )
        whole_atom_candidates = sorted(
            key for key, item in bounds.items()
            if all(item[axis][0] <= value <= item[axis][1]
                   for axis, value in fixed.items())
            and all(item[axis][0] <= span[0] < span[1] <= item[axis][1]
                    for axis, span in open_spans.items())
        )
        require(
            midpoint_candidates
            and midpoint_candidates == whole_atom_candidates,
            "constant closed-leaf incidence on whole atom:" + label,
        )
        return midpoint_candidates[0]

    raw_faces: list[dict[str, Any]] = []
    for stage, faces in (
        ("ROUND176_INTERNAL", round176_faces),
        ("ROUND180_INTERNAL", round180_faces),
    ):
        for face in faces:
            raw_faces.append({
                "source": stage + ":" + face["face_sha256"],
                "fixed_axis": face["axis"],
                "coordinate": face["coordinate"],
                "spans": face["spans"],
            })
    for fixed_axis in axes:
        free_axes = [axis for axis in axes if axis != fixed_axis]
        for side, coordinate in zip(
            ("LOWER", "UPPER"), parent_bounds[fixed_axis]
        ):
            raw_faces.append({
                "source": f"OUTER_PARENT:{fixed_axis}:{side}",
                "fixed_axis": fixed_axis,
                "coordinate": str(coordinate),
                "spans": {
                    axis: [str(parent_bounds[axis][0]),
                           str(parent_bounds[axis][1])]
                    for axis in free_axes
                },
            })

    face_atoms: dict[str, dict[str, Any]] = {}
    raw_face_reclosure: list[dict[str, Any]] = []
    raw_edges: dict[str, dict[str, Any]] = {}
    raw_corners: dict[str, dict[str, Any]] = {}
    for raw in raw_faces:
        fixed_axis = raw["fixed_axis"]
        fixed_value = Q(raw["coordinate"])
        free_axes = sorted(raw["spans"])
        spans = {
            axis: (Q(values[0]), Q(values[1]))
            for axis, values in raw["spans"].items()
        }
        axis_cuts = {
            axis: cuts(axis, spans[axis][0], spans[axis][1])
            for axis in free_axes
        }
        source_measure = (
            (spans[free_axes[0]][1] - spans[free_axes[0]][0])
            * (spans[free_axes[1]][1] - spans[free_axes[1]][0])
        )
        atom_measure = Q(0)
        atom_keys: list[str] = []
        for first_lower, first_upper in zip(
            axis_cuts[free_axes[0]], axis_cuts[free_axes[0]][1:]
        ):
            for second_lower, second_upper in zip(
                axis_cuts[free_axes[1]], axis_cuts[free_axes[1]][1:]
            ):
                geometry = {
                    "fixed": {fixed_axis: str(fixed_value)},
                    "open_spans": {
                        free_axes[0]: [str(first_lower), str(first_upper)],
                        free_axes[1]: [str(second_lower), str(second_upper)],
                    },
                }
                encoded = wire(geometry).decode("ascii")
                group = face_atoms.setdefault(encoded, {
                    "geometry": geometry, "incident_sources": [],
                })
                group["incident_sources"].append(raw["source"])
                atom_keys.append(encoded)
                atom_measure += (
                    (first_upper - first_lower)
                    * (second_upper - second_lower)
                )
        require(atom_measure == source_measure,
                "exact atomic face reclosure:" + label)
        raw_face_reclosure.append({
            "source": raw["source"],
            "source_exact_measure": str(source_measure),
            "atomic_exact_measure": str(atom_measure),
            "atomic_geometry_keys_sha256": digest(sorted(atom_keys)),
        })
        for boundary_axis in free_axes:
            other = next(axis for axis in free_axes if axis != boundary_axis)
            for side, endpoint in zip(
                ("LOWER", "UPPER"), spans[boundary_axis]
            ):
                geometry = {
                    "fixed": {
                        fixed_axis: str(fixed_value),
                        boundary_axis: str(endpoint),
                    },
                    "open_span": {
                        other: [str(spans[other][0]), str(spans[other][1])]
                    },
                }
                encoded = wire(geometry).decode("ascii")
                group = raw_edges.setdefault(encoded, {
                    "geometry": geometry, "incident_sources": [],
                })
                group["incident_sources"].append(
                    raw["source"] + ":" + boundary_axis + ":" + side
                )
        for first_side, first in zip(
            ("LOWER", "UPPER"), spans[free_axes[0]]
        ):
            for second_side, second in zip(
                ("LOWER", "UPPER"), spans[free_axes[1]]
            ):
                geometry = {"point": {
                    fixed_axis: str(fixed_value),
                    free_axes[0]: str(first),
                    free_axes[1]: str(second),
                }}
                encoded = wire(geometry).decode("ascii")
                group = raw_corners.setdefault(encoded, {
                    "geometry": geometry, "incident_sources": [],
                })
                group["incident_sources"].append(
                    raw["source"] + ":" + first_side + ":" + second_side
                )

    # Every 2D grid atom contributes its complete cut-line/cut-point boundary.
    # This closes measure-zero strata created by interior leaf-bound cuts, not
    # merely the outer boundaries of the original unsplit face rectangles.
    for _encoded, atom in sorted(face_atoms.items()):
        fixed_axis, fixed_value = next(iter(atom["geometry"]["fixed"].items()))
        span_axes = sorted(atom["geometry"]["open_spans"])
        spans = {
            axis: tuple(values)
            for axis, values in atom["geometry"]["open_spans"].items()
        }
        atom_source = "ATOMIC_2D:" + digest(atom["geometry"])
        for boundary_axis in span_axes:
            other = next(axis for axis in span_axes if axis != boundary_axis)
            for side, endpoint in zip(
                ("LOWER", "UPPER"), spans[boundary_axis]
            ):
                geometry = {
                    "fixed": {
                        fixed_axis: fixed_value,
                        boundary_axis: endpoint,
                    },
                    "open_span": {other: list(spans[other])},
                }
                encoded = wire(geometry).decode("ascii")
                group = raw_edges.setdefault(encoded, {
                    "geometry": geometry, "incident_sources": [],
                })
                group["incident_sources"].append(
                    atom_source + ":" + boundary_axis + ":" + side
                )
        for first_side, first in zip(
            ("LOWER", "UPPER"), spans[span_axes[0]]
        ):
            for second_side, second in zip(
                ("LOWER", "UPPER"), spans[span_axes[1]]
            ):
                geometry = {"point": {
                    fixed_axis: fixed_value,
                    span_axes[0]: first,
                    span_axes[1]: second,
                }}
                encoded = wire(geometry).decode("ascii")
                group = raw_corners.setdefault(encoded, {
                    "geometry": geometry, "incident_sources": [],
                })
                group["incident_sources"].append(
                    atom_source + ":" + first_side + ":" + second_side
                )

    face_rows: list[dict[str, Any]] = []
    for _encoded, group in sorted(face_atoms.items()):
        fixed = {
            axis: Q(value) for axis, value in group["geometry"]["fixed"].items()
        }
        open_spans = {
            axis: (Q(values[0]), Q(values[1]))
            for axis, values in group["geometry"]["open_spans"].items()
        }
        owner = containing_owner(fixed, open_spans)
        span_values = list(open_spans.values())
        face_rows.append(sealed({
            "schema": "cm2.round306c30b.atomic-2D-half-open-owner.row.v1",
            "geometry": group["geometry"],
            "incident_sources": sorted(set(group["incident_sources"])),
            "half_open_owner_leaf_key": owner,
            "owner_selection_rule": (
                "DETERMINISTIC_LEAF_KEY_LEXICOGRAPHIC_MIN_CONTAINING_LEAF"
            ),
            "owner_proof_source": proof_source[owner],
            "owner_disposition": dispositions[owner],
            "exact_measure": str(
                (span_values[0][1] - span_values[0][0])
                * (span_values[1][1] - span_values[1][0])
            ),
        }))

    edge_atoms: dict[str, dict[str, Any]] = {}
    raw_edge_reclosure: list[dict[str, Any]] = []
    for _encoded, raw in sorted(raw_edges.items()):
        free_axis, values = next(iter(raw["geometry"]["open_span"].items()))
        lower, upper = Q(values[0]), Q(values[1])
        source_measure = upper - lower
        atom_measure = Q(0)
        atom_keys: list[str] = []
        axis_cuts = cuts(free_axis, lower, upper)
        for atom_lower, atom_upper in zip(axis_cuts, axis_cuts[1:]):
            geometry = {
                "fixed": raw["geometry"]["fixed"],
                "open_span": {
                    free_axis: [str(atom_lower), str(atom_upper)]
                },
            }
            encoded = wire(geometry).decode("ascii")
            group = edge_atoms.setdefault(encoded, {
                "geometry": geometry, "incident_sources": [],
            })
            group["incident_sources"].extend(raw["incident_sources"])
            atom_keys.append(encoded)
            atom_measure += atom_upper - atom_lower
            atom_source = "ATOMIC_1D:" + digest(geometry)
            for side, endpoint in (
                ("LOWER", atom_lower), ("UPPER", atom_upper)
            ):
                point = dict(raw["geometry"]["fixed"])
                point[free_axis] = str(endpoint)
                point_geometry = {"point": point}
                point_key = wire(point_geometry).decode("ascii")
                point_group = raw_corners.setdefault(point_key, {
                    "geometry": point_geometry, "incident_sources": [],
                })
                point_group["incident_sources"].append(
                    atom_source + ":" + side
                )
        require(atom_measure == source_measure,
                "exact atomic edge reclosure:" + label)
        raw_edge_reclosure.append({
            "source_geometry_sha256": digest(raw["geometry"]),
            "source_exact_measure": str(source_measure),
            "atomic_exact_measure": str(atom_measure),
            "atomic_geometry_keys_sha256": digest(sorted(atom_keys)),
        })

    edge_rows: list[dict[str, Any]] = []
    for _encoded, group in sorted(edge_atoms.items()):
        fixed = {
            axis: Q(value) for axis, value in group["geometry"]["fixed"].items()
        }
        free_axis, values = next(iter(group["geometry"]["open_span"].items()))
        open_spans = {free_axis: (Q(values[0]), Q(values[1]))}
        owner = containing_owner(fixed, open_spans)
        edge_rows.append(sealed({
            "schema": "cm2.round306c30b.atomic-1D-half-open-owner.row.v1",
            "geometry": group["geometry"],
            "incident_sources": sorted(set(group["incident_sources"])),
            "half_open_owner_leaf_key": owner,
            "owner_selection_rule": (
                "DETERMINISTIC_LEAF_KEY_LEXICOGRAPHIC_MIN_CONTAINING_LEAF"
            ),
            "owner_proof_source": proof_source[owner],
            "owner_disposition": dispositions[owner],
            "exact_measure": str(open_spans[free_axis][1]
                                 - open_spans[free_axis][0]),
        }))

    corner_rows: list[dict[str, Any]] = []
    for _encoded, group in sorted(raw_corners.items()):
        fixed = {
            axis: Q(value) for axis, value in group["geometry"]["point"].items()
        }
        owner = containing_owner(fixed, {})
        corner_rows.append(sealed({
            "schema": "cm2.round306c30b.atomic-0D-half-open-owner.row.v1",
            "geometry": group["geometry"],
            "incident_sources": sorted(set(group["incident_sources"])),
            "half_open_owner_leaf_key": owner,
            "owner_selection_rule": (
                "DETERMINISTIC_LEAF_KEY_LEXICOGRAPHIC_MIN_CONTAINING_LEAF"
            ),
            "owner_proof_source": proof_source[owner],
            "owner_disposition": dispositions[owner],
        }))

    all_rows = face_rows + edge_rows + corner_rows
    candidate_audit = {
        "schema": "cm2.round306c30b.exact-atomic-half-open-owner-audit.v2",
        "audit_scope": audit_scope,
        "leaf_key_kind": leaf_key_kind,
        "exact_3D_enclosure": {
            "all_leaf_boxes_contained_in_parent_and_nondegenerate": True,
            "pairwise_leaf_interiors_disjoint": True,
            "tested_unordered_leaf_pair_count": pair_count,
            "tested_leaf_pair_rows_sha256": pair_hash.hexdigest(),
            "leaf_exact_volume_sum": str(leaf_volume),
            "parent_exact_volume": str(parent_volume),
            "leaf_exact_volume_sum_equals_parent": True,
        },
        "axis_grid_coordinate_count": {
            axis: len(values) for axis, values in grid.items()
        },
        "axis_grid_coordinates_sha256": digest({
            axis: [str(value) for value in values]
            for axis, values in grid.items()
        }),
        "atomic_owner_selection_rule": (
            "DETERMINISTIC_LEAF_KEY_LEXICOGRAPHIC_MIN_CONTAINING_LEAF"
        ),
        "closed_3D_leaf_count": len(leaf_boxes),
        "closed_3D_leaf_keys_sha256": digest(sorted(leaf_boxes)),
        "closed_3D_leaf_disposition_census": dict(sorted(Counter(
            dispositions.values()
        ).items())),
        "raw_2D_stratum_reclosure_row_count": len(raw_face_reclosure),
        "raw_2D_stratum_reclosure_rows_sha256": digest(raw_face_reclosure),
        "all_raw_2D_strata_exactly_reclosed": all(
            value["source_exact_measure"] == value["atomic_exact_measure"]
            for value in raw_face_reclosure
        ),
        "raw_1D_stratum_reclosure_row_count": len(raw_edge_reclosure),
        "raw_1D_stratum_reclosure_rows_sha256": digest(raw_edge_reclosure),
        "all_raw_1D_strata_exactly_reclosed": all(
            value["source_exact_measure"] == value["atomic_exact_measure"]
            for value in raw_edge_reclosure
        ),
        "lower_strata_generation_rule": (
            "EACH_2D_ATOM_GENERATES_ALL_FOUR_1D_CUT_BOUNDARIES__"
            "EACH_1D_ATOM_GENERATES_BOTH_0D_CUT_ENDPOINTS__"
            "GLOBAL_PURE_GEOMETRY_DEDUP"
        ),
        "atomic_2D_owner_row_count": len(face_rows),
        "atomic_2D_owner_rows_sha256": digest(face_rows),
        "atomic_1D_owner_row_count": len(edge_rows),
        "atomic_1D_owner_rows_sha256": digest(edge_rows),
        "atomic_0D_owner_row_count": len(corner_rows),
        "atomic_0D_owner_rows_sha256": digest(corner_rows),
        "atomic_owner_disposition_census": dict(sorted(Counter(
            value["owner_disposition"] for value in all_rows
        ).items())),
        "atomic_owner_rows_sha256": digest(all_rows),
    }
    require(
        bool(face_rows) and bool(edge_rows) and bool(corner_rows),
        "nonempty 2D/1D/0D atomic owner ledgers:" + label,
    )
    return {
        "candidate_audit": candidate_audit,
        "independent_3D_reclosure": three_dimensional_reclosure,
    }




def validate_h_row(
    candidate: dict[str, Any],
    source_kind: str,
    source: Any,
    binding: dict[str, Any],
) -> str:
    tree = local_h_tree(source)
    terminals = tree["terminals"]
    partition = candidate["H_partition"]
    typed_terminals = [
        row for row in terminals if row["coarse_disposition"] == "MIXED"
    ]
    sheets = [row["typed_strata"]["H_zero_2D_sheet"] for row in typed_terminals]
    face_regions = [item for row in typed_terminals for item in
                    row["typed_strata"]["terminal_face_2D_H_sign_regions"]]
    faces = [item for row in typed_terminals for item in
             row["typed_strata"]["H_zero_1D_face_incidences"]]
    edge_regions = [item for row in typed_terminals for item in
                    row["typed_strata"]["terminal_edge_1D_H_sign_intervals"]]
    edges = [item for row in typed_terminals for item in
             row["typed_strata"]["H_zero_0D_edge_incidences"]]
    corners = [item for row in typed_terminals for item in
               row["typed_strata"]["H_zero_0D_corner_absence_rows"]]

    def semantic_core(value: Any) -> Any:
        if type(value) is dict:
            return {
                key: semantic_core(item)
                for key, item in sorted(value.items())
                if key not in {"schema", "row_sha256"}
                and not key.endswith("_sha256")
                and not key.endswith("_row_count")
            }
        if type(value) is list:
            return [semantic_core(item) for item in value]
        return value

    projection = {
        "projection_schema": (
            "cm2.round306c30b.H-partition-analytic-semantic-projection.v1"
        ),
        "whole_cell_disposition": tree["whole"],
        "terminal_rectangle_disposition_census": dict(sorted(
            tree["census"].items()
        )),
        "terminal_semantic_rows": [{
            "terminal_id": row["terminal_id"],
            "relative_depth": row["relative_depth"],
            "closed_box": row["closed_box"],
            "exact_volume": row["exact_volume"],
            "classification": row["classification"],
            "coarse_disposition": row["coarse_disposition"],
            "analytic_evidence": semantic_core(row["analytic_evidence"]),
            **({
                "typed_strata_semantic_core": semantic_core(row["typed_strata"]),
            } if "typed_strata" in row else {}),
        } for row in terminals],
        "split_face_geometry_and_child_rows": [{
            key: face[key] for key in (
                "parent_cell_key", "axis", "coordinate", "spans",
                "dimension", "lower_child_owner", "upper_child_nonowner",
                "both_closed_interval_enclosures_include_face",
            )
        } for face in tree["split_faces"]],
        "relative_3D_coverage": "1",
        "exact_volume": str(tree["volume"]),
    }
    audit = partition["terminal_exact_atomic_owner_audit"]
    terminal_by_id = {
        row["terminal_id"]: row for row in terminals
    }
    require(
        set(tree["terminal_boxes"]) == set(terminal_by_id),
        "C30c local H atomic terminal binding:" + source.key,
    )
    terminal_reclosure = local_terminal_atomic_owner_reclosure(
        source.key,
        source.box,
        tree["terminal_boxes"],
        {
            terminal_id: (
                "ROUND306C30B_H_TERMINAL_ROW:"
                + terminal_by_id[terminal_id]["row_sha256"]
            )
            for terminal_id in tree["terminal_boxes"]
        },
        {
            terminal_id: terminal_by_id[terminal_id]["coarse_disposition"]
            for terminal_id in tree["terminal_boxes"]
        },
        [],
        tree["split_faces"],
        audit_scope="PER_H_CELL_TERMINAL_SUBDIVISION",
        leaf_key_kind="H_TERMINAL_ID",
    )
    expected_audit = terminal_reclosure["candidate_audit"]
    require(
        partition["whole_cell_disposition"] == tree["whole"]
        and partition["terminal_rectangle_count"] == len(terminals)
        and partition["terminal_rectangle_disposition_census"]
        == dict(sorted(tree["census"].items()))
        and partition["terminal_rectangles"] == terminals
        and partition["terminal_rectangles_sha256"] == digest(terminals)
        and partition["internal_split_2D_face_rows"] == tree["split_faces"]
        and partition["internal_split_2D_face_row_count"] == len(tree["split_faces"])
        and partition["internal_split_2D_face_rows_sha256"]
        == digest(tree["split_faces"])
        and partition["internal_split_1D_edge_owner_rows"] == tree["split_lines"]
        and partition["internal_split_1D_edge_owner_row_count"]
        == len(tree["split_lines"])
        and partition["internal_split_1D_edge_owner_rows_sha256"]
        == digest(tree["split_lines"])
        and partition["internal_split_0D_corner_owner_rows"] == tree["split_points"]
        and partition["internal_split_0D_corner_owner_row_count"]
        == len(tree["split_points"])
        and partition["internal_split_0D_corner_owner_rows_sha256"]
        == digest(tree["split_points"])
        and partition["typed_H_zero_2D_sheet_count"] == len(typed_terminals)
        and partition["relative_3D_coverage"] == "1"
        and Q(partition["exact_volume"]) == tree["volume"]
        and partition["analytic_semantic_projection"] == projection
        and partition["analytic_semantic_projection_sha256"] == digest(projection)
        and partition["terminal_exact_atomic_owner_audit_sha256"] == digest(audit)
        and partition[
            "exact_exhaustive_disjoint_3D_2D_1D_0D_partition_verified"
        ] is True
        and partition["raw_prefix_lower_strata_formal_owner_credit"] == 0,
        "C30c local H partition:" + source.key,
    )
    require(
        audit == expected_audit
        and terminal_reclosure["independent_3D_reclosure"][
            "all_closed_leaves_contained_in_parent"
        ] is True
        and terminal_reclosure["independent_3D_reclosure"][
            "all_closed_leaf_strict_interiors_pairwise_disjoint"
        ] is True
        and terminal_reclosure["independent_3D_reclosure"][
            "closed_leaf_union_exhausts_parent_by_exact_volume"
        ] is True,
        "C30c local H legacy audit exact reconstruction:" + source.key,
    )
    expected_partition = {
        "whole_cell_disposition": tree["whole"],
        "terminal_rectangle_count": len(terminals),
        "terminal_rectangle_disposition_census": dict(sorted(
            tree["census"].items()
        )),
        "terminal_rectangles": terminals,
        "terminal_rectangles_sha256": digest(terminals),
        "internal_split_2D_face_rows": tree["split_faces"],
        "internal_split_2D_face_row_count": len(tree["split_faces"]),
        "internal_split_2D_face_rows_sha256": digest(tree["split_faces"]),
        "internal_split_1D_edge_owner_rows": tree["split_lines"],
        "internal_split_1D_edge_owner_row_count": len(tree["split_lines"]),
        "internal_split_1D_edge_owner_rows_sha256": digest(
            tree["split_lines"]
        ),
        "internal_split_0D_corner_owner_rows": tree["split_points"],
        "internal_split_0D_corner_owner_row_count": len(tree["split_points"]),
        "internal_split_0D_corner_owner_rows_sha256": digest(
            tree["split_points"]
        ),
        "typed_H_zero_2D_sheet_count": len(typed_terminals),
        "relative_3D_coverage": "1",
        "exact_volume": str(tree["volume"]),
        "analytic_semantic_projection": projection,
        "analytic_semantic_projection_sha256": digest(projection),
        "terminal_exact_atomic_owner_audit": expected_audit,
        "terminal_exact_atomic_owner_audit_sha256": digest(expected_audit),
        "exact_exhaustive_disjoint_3D_2D_1D_0D_partition_verified": True,
        "formal_lower_strata_owner_source": (
            "TERMINAL_EXACT_ATOMIC_OWNER_AUDIT__RAW_PREFIX_INCIDENCE_"
            "DIAGNOSTICS_RECEIVE_ZERO_CREDIT"
        ),
        "raw_prefix_lower_strata_formal_owner_credit": 0,
    }
    require(
        partition == expected_partition,
        "C30c local H exact partition object:" + source.key,
    )
    expected_body = {
        "schema": "cm2.round306c30c.inherited-h-cell.row.v1",
        "source_kind": source_kind,
        "origin_key": source.origin_key,
        "cell_key": source.key,
        "source_chart_id": source.chart_id,
        "closed_box": r176.box_row(source.box),
        "exact_volume": str(r215.box_volume(source.box)),
        "unique_first_owner": r176.FROZEN_OWNER,
        "frozen_outgoing_chart": r176.FROZEN_CHART,
        "source_binding": binding,
        "H_partition": expected_partition,
        "whole_H_cell_disposition": tree["whole"],
        "typed_H_zero_2D_sheet_count": len(typed_terminals),
        "typed_H_zero_2D_sheet_rows_sha256": digest(sheets),
        "terminal_face_2D_H_sign_region_row_count": len(face_regions),
        "terminal_face_2D_H_sign_region_rows_sha256": digest(face_regions),
        "H_zero_1D_face_incidence_row_count": len(faces),
        "H_zero_1D_face_incidence_rows_sha256": digest(faces),
        "terminal_edge_1D_H_sign_interval_row_count": len(edge_regions),
        "terminal_edge_1D_H_sign_interval_rows_sha256": digest(edge_regions),
        "H_zero_0D_edge_incidence_row_count": len(edges),
        "H_zero_0D_edge_incidence_rows_sha256": digest(edges),
        "H_zero_0D_corner_absence_row_count": len(corners),
        "H_zero_0D_corner_absence_rows_sha256": digest(corners),
        "half_open_owner_rule": "E_OR_W_OWNS__N_OR_S_SHADOWS",
        "whole_origin_exclusion_credit": 0,
        "formal_credit": {
            "inherited_H_cell_disposition": 0,
            "whole_source_W_origin_exclusion": 0,
        },
        "candidate_reuse_of_C30b_H_theorem": True,
        "strict_nonpromotion": "C30B_HELPER_REUSE_DOES_NOT_IMPORT_C30B_RESULT_CREDIT",
    }
    require(
        candidate == sealed(expected_body),
        "C30c local inherited H exact row:" + source.key,
    )
    return tree["whole"]


def independent_typed_boundary_support(
    combined: dict[str, Any], signature: dict[str, str]
) -> dict[str, Any]:
    typed = combined["typed_H_geometry"]
    codimension = len(signature)
    if codimension == 0:
        rows = typed["open_3D_sides"] + [typed["H_zero_2D_sheet"]]
        require(len(rows) == 3, "independent interior five-strata support")
        binding_kind = "COMBINED_INTERIOR_FIVE_STRATA"
        analytic_sha256 = combined["combined_strata_sha256"]
    elif codimension == 1:
        axis, side = next(iter(sorted(signature.items())))
        rows = [
            row for row in typed["H_zero_1D_face_incidences"]
            if row["fixed_axis"] == axis and row["boundary_side"] == side
        ] + [
            row for row in typed["terminal_face_2D_H_sign_regions"]
            if row["fixed_axis"] == axis and row["boundary_side"] == side
        ]
        boundary = [
            row for row in combined["outer_boundary_restriction_rows"]
            if row["fixed_coordinates"] == signature
        ]
        require(len(rows) == 3 and len(boundary) == 1,
                "independent face analytic support")
        binding_kind = "COMBINED_OUTER_BOUNDARY_RESTRICTION"
        analytic_sha256 = boundary[0]["row_sha256"]
    elif codimension == 2:
        rows = [
            row for row in typed["H_zero_0D_edge_incidences"]
            if row["fixed"] == signature
        ] + [
            row for row in typed["terminal_edge_1D_H_sign_intervals"]
            if row["fixed"] == signature
        ]
        boundary = [
            row for row in combined["outer_boundary_restriction_rows"]
            if row["fixed_coordinates"] == signature
        ]
        require(len(rows) == 3 and len(boundary) == 1,
                "independent edge analytic support")
        binding_kind = "COMBINED_OUTER_BOUNDARY_RESTRICTION"
        analytic_sha256 = boundary[0]["row_sha256"]
    else:
        require(codimension == 3, "independent relative boundary codimension")
        rows = [
            row for row in typed["H_zero_0D_corner_absence_rows"]
            if row["corner"] == signature
        ]
        boundary = [
            row for row in combined["outer_boundary_restriction_rows"]
            if row["fixed_coordinates"] == signature
        ]
        require(len(rows) == 1 and len(boundary) == 1,
                "independent corner analytic support")
        binding_kind = "COMBINED_OUTER_BOUNDARY_RESTRICTION"
        analytic_sha256 = boundary[0]["row_sha256"]
    return {
        "relative_boundary_codimension": codimension,
        "relative_boundary_signature": signature,
        "binding_kind": binding_kind,
        "analytic_partition_or_boundary_row_sha256": analytic_sha256,
        "typed_H_support_row_count": len(rows),
        "typed_H_support_rows": rows,
        "typed_H_support_rows_sha256": digest(rows),
        "Delta_on_H_graph_bracket_sha256": digest(
            combined["Delta_on_H_graph_bracket"]
        ),
        "Delta_H_intersection_sha256": digest(
            combined["Delta_H_intersection"]
        ),
        "sampled_evidence_used_for_uniform_conclusion": False,
    }


def independent_global_full_atomic_owner_ledger(
    leaf_rows: dict[str, Any],
    proof_source: dict[str, str],
    leaf_disposition: dict[str, str],
) -> dict[str, Any]:
    """Verifier path: sparse global plane sweep and Cartesian membership queries."""
    axes = ("t", "p", "s")
    bounds = {
        key: {
            "t": (row.box.t0, row.box.t1),
            "p": (row.box.p0, row.box.p1),
            "s": (row.box.s0, row.box.s1),
        }
        for key, row in leaf_rows.items()
    }
    origin_key = next(iter(leaf_rows.values())).origin_key
    grid = {
        axis: sorted({value for box in bounds.values() for value in box[axis]})
        for axis in axes
    }

    def parts(
        geometry: dict[str, Any]
    ) -> tuple[dict[str, Q], dict[str, tuple[Q, Q]]]:
        return (
            {axis: Q(value) for axis, value in geometry["fixed"].items()},
            {axis: (Q(span[0]), Q(span[1]))
             for axis, span in geometry["open_spans"].items()},
        )

    def contains(
        box: dict[str, tuple[Q, Q]],
        fixed: dict[str, Q],
        spans: dict[str, tuple[Q, Q]],
    ) -> bool:
        return (
            all(box[axis][0] <= value <= box[axis][1]
                for axis, value in fixed.items())
            and all(box[axis][0] <= lower < upper <= box[axis][1]
                    for axis, (lower, upper) in spans.items())
        )

    def close_owner(
        dimension: int,
        geometry: dict[str, Any],
        sources: list[str],
    ) -> dict[str, Any]:
        fixed, spans = parts(geometry)
        probes = {
            axis: (lower + upper) / 2
            for axis, (lower, upper) in spans.items()
        }
        containing = []
        for leaf_key in sorted(bounds):
            box = bounds[leaf_key]
            if not contains(box, fixed, spans):
                continue
            if any(not box[axis][0] < value < box[axis][1]
                   for axis, value in probes.items()):
                continue
            containing.append(leaf_key)
        require(bool(containing), "global full atomic owner exists")
        owner = containing[0]
        incidence_rows: list[dict[str, Any]] = []
        for leaf_key in containing:
            signature: dict[str, str] = {}
            for axis, value in sorted(fixed.items()):
                lower, upper = bounds[leaf_key][axis]
                if value == lower:
                    signature[axis] = "LOWER"
                elif value == upper:
                    signature[axis] = "UPPER"
            incidence_rows.append(sealed({
                "schema": "cm2.round306c30c.full-atomic-leaf-incidence.row.v1",
                "leaf_key": leaf_key,
                "relative_boundary_signature": signature,
                "relative_boundary_codimension": len(signature),
                "selected_by_half_open_owner": leaf_key == owner,
                "proof_source": proof_source[leaf_key],
                "leaf_disposition": leaf_disposition[leaf_key],
            }))
        measure = Q(1)
        for lower, upper in spans.values():
            measure *= upper - lower
        return sealed({
            "schema": "cm2.round306c30c.full-atomic-owner.row.v1",
            "origin_key": origin_key,
            "ambient_dimension": dimension,
            "geometry": geometry,
            "exact_measure": str(measure),
            "incident_sources": sorted(set(sources)),
            "incident_source_count": len(set(sources)),
            "closed_containing_leaf_keys": containing,
            "closed_incident_leaf_rows": incidence_rows,
            "closed_incident_leaf_rows_sha256": digest(incidence_rows),
            "half_open_owner_leaf_key": owner,
            "owner_selection_rule": (
                "DETERMINISTIC_LEAF_KEY_LEXICOGRAPHIC_MIN_CONTAINING_LEAF"
            ),
            "owner_proof_source": proof_source[owner],
            "owner_disposition": leaf_disposition[owner],
        })

    plane_faces: dict[tuple[str, Q], list[tuple[str, str, dict[str, tuple[Q, Q]]]]] = defaultdict(list)
    for leaf_key, box in sorted(bounds.items()):
        for axis in axes:
            spans = {other: box[other] for other in axes if other != axis}
            plane_faces[(axis, box[axis][0])].append((leaf_key, "LOWER", spans))
            plane_faces[(axis, box[axis][1])].append((leaf_key, "UPPER", spans))
    face_rows: list[dict[str, Any]] = []
    for (fixed_axis, coordinate), sources in sorted(
        plane_faces.items(), key=lambda item: (item[0][0], item[0][1])
    ):
        free_axes = [axis for axis in axes if axis != fixed_axis]
        candidate_rectangles: set[tuple[tuple[Q, Q], tuple[Q, Q]]] = set()
        for _leaf, _side, spans in sources:
            interval_sets = []
            for axis in free_axes:
                values = [value for value in grid[axis]
                          if spans[axis][0] <= value <= spans[axis][1]]
                interval_sets.append(list(zip(values, values[1:])))
            candidate_rectangles.update(itertools.product(*interval_sets))
        for rectangle in sorted(candidate_rectangles):
            incident = [
                "LEAF_FACE:" + leaf_key + ":" + fixed_axis + ":" + side
                for leaf_key, side, spans in sources
                if all(spans[axis][0] <= interval[0] < interval[1]
                       <= spans[axis][1]
                       for axis, interval in zip(
                           free_axes, rectangle, strict=True
                       ))
            ]
            require(bool(incident), "global plane rectangle incidence")
            geometry = {
                "fixed": {fixed_axis: str(coordinate)},
                "open_spans": {
                    axis: [str(interval[0]), str(interval[1])]
                    for axis, interval in zip(
                        free_axes, rectangle, strict=True
                    )
                },
            }
            face_rows.append(close_owner(2, geometry, incident))
    face_rows.sort(key=lambda row: wire(row["geometry"]))

    line_candidates: dict[str, dict[str, Any]] = {}
    for face in face_rows:
        fixed, spans = parts(face["geometry"])
        for boundary_axis in sorted(spans):
            free_axis = next(axis for axis in spans if axis != boundary_axis)
            for endpoint in spans[boundary_axis]:
                geometry = {
                    "fixed": {
                        axis: str(value) for axis, value in sorted({
                            **fixed, boundary_axis: endpoint,
                        }.items())
                    },
                    "open_spans": {
                        free_axis: [
                            str(spans[free_axis][0]), str(spans[free_axis][1])
                        ]
                    },
                }
                line_candidates[wire(geometry).decode("ascii")] = geometry
    line_rows: list[dict[str, Any]] = []
    for _key, geometry in sorted(line_candidates.items()):
        line_fixed, line_spans = parts(geometry)
        sources: list[str] = []
        for face in face_rows:
            face_fixed, face_spans = parts(face["geometry"])
            face_axis, face_value = next(iter(face_fixed.items()))
            if line_fixed.get(face_axis) != face_value:
                continue
            boundary_axes = [axis for axis in face_spans if axis in line_fixed]
            if len(boundary_axes) != 1:
                continue
            boundary_axis = boundary_axes[0]
            side = (
                "LOWER" if line_fixed[boundary_axis]
                == face_spans[boundary_axis][0] else
                "UPPER" if line_fixed[boundary_axis]
                == face_spans[boundary_axis][1] else None
            )
            remaining = next(axis for axis in face_spans if axis != boundary_axis)
            if side is not None and line_spans == {remaining: face_spans[remaining]}:
                sources.append(
                    "ATOMIC_2D:" + face["row_sha256"] + ":"
                    + boundary_axis + ":" + side
                )
        require(bool(sources), "global line parent incidence")
        line_rows.append(close_owner(1, geometry, sources))

    point_candidates: dict[str, dict[str, Any]] = {}
    for line in line_rows:
        fixed, spans = parts(line["geometry"])
        free_axis, interval = next(iter(spans.items()))
        for endpoint in interval:
            geometry = {
                "fixed": {
                    axis: str(value) for axis, value in sorted({
                        **fixed, free_axis: endpoint,
                    }.items())
                },
                "open_spans": {},
            }
            point_candidates[wire(geometry).decode("ascii")] = geometry
    point_rows: list[dict[str, Any]] = []
    for _key, geometry in sorted(point_candidates.items()):
        point_fixed, _spans = parts(geometry)
        sources: list[str] = []
        for line in line_rows:
            line_fixed, line_spans = parts(line["geometry"])
            free_axis, interval = next(iter(line_spans.items()))
            if any(point_fixed.get(axis) != value
                   for axis, value in line_fixed.items()):
                continue
            side = (
                "LOWER" if point_fixed.get(free_axis) == interval[0] else
                "UPPER" if point_fixed.get(free_axis) == interval[1] else None
            )
            if side is not None:
                sources.append("ATOMIC_1D:" + line["row_sha256"] + ":" + side)
        require(bool(sources), "global point parent incidence")
        point_rows.append(close_owner(0, geometry, sources))
    all_rows = face_rows + line_rows + point_rows
    return {
        "schema": "cm2.round306c30c.full-atomic-owner-ledger.v1",
        "origin_key": origin_key,
        "construction_contract": "FULL_AXIS_ALIGNED_CELL_COMPLEX",
        "closed_leaf_count": len(leaf_rows),
        "axis_grid_coordinates_sha256": digest({
            axis: [str(value) for value in values]
            for axis, values in grid.items()
        }),
        "atomic_2D_owner_rows": face_rows,
        "atomic_2D_owner_row_count": len(face_rows),
        "atomic_2D_owner_rows_sha256": digest(face_rows),
        "atomic_1D_owner_rows": line_rows,
        "atomic_1D_owner_row_count": len(line_rows),
        "atomic_1D_owner_rows_sha256": digest(line_rows),
        "atomic_0D_owner_rows": point_rows,
        "atomic_0D_owner_row_count": len(point_rows),
        "atomic_0D_owner_rows_sha256": digest(point_rows),
        "all_atomic_owner_rows_sha256": digest(all_rows),
        "all_rows_have_incident_sources_exact_measure_and_unique_owner": True,
    }


def independent_owner_audit(
    context: OriginContext,
    h_rows: list[dict[str, Any]],
    combined_rows: list[dict[str, Any]],
) -> tuple[
    dict[str, Any], Counter[str], dict[str, Any], dict[str, str], dict[str, str]
]:
    leaf_rows: dict[str, Any] = {
        key: types.SimpleNamespace(box=box, origin_key=context.origin)
        for key, box in context.prior_boxes.items()
    }
    leaf_rows.update({row.key: row for row in context.base_rows})
    leaf_rows.update(context.leaves["terminal"])
    leaf_rows.update(context.leaves["final"])
    h_by_key = {row["cell_key"]: row for row in h_rows}
    combined_by_key = {row["cell_key"]: row for row in combined_rows}
    direct_live = {row["cell_key"] for row in context.direct_live}
    inherited_excluded = {
        row["cell_key"] for row in context.refinement["terminal_rows"]
        if row["coarse_disposition"] == "EXCLUDED"
    }
    proof = {
        key: "PINNED_PRE_DEPTH14_EXCLUDED" for key in context.prior_boxes
    }
    dispositions = {key: "EXCLUDED" for key in context.prior_boxes}
    proof.update({
        row.key: "PINNED_ROUND176_PRECLOSED_EXCLUDED"
        for row in context.base_rows
    })
    dispositions.update({row.key: "EXCLUDED" for row in context.base_rows})
    for evidence in context.refinement["terminal_rows"]:
        key = evidence["cell_key"]
        if key in inherited_excluded:
            proof[key] = "PINNED_ROUND180_INHERITED_EXCLUDED"
            dispositions[key] = "EXCLUDED"
        elif key in direct_live:
            proof[key] = "PINNED_ROUND180_DIRECT_STRICT_LIVE"
            dispositions[key] = "LIVE"
        else:
            require(key in h_by_key, "materialized H owner source")
            proof[key] = "ROUND306C30C_MATERIALIZED_INHERITED_H"
            dispositions[key] = h_by_key[key]["whole_H_cell_disposition"]
    for row in context.refinement["final_residual_rows"]:
        if row.key in combined_by_key:
            proof[row.key] = "ROUND306C30C_COMBINED_DELTA_H_PARTITION"
            dispositions[row.key] = "MIXED"
        else:
            require(row.key in context.final_closed_sources, "final owner source")
            proof[row.key] = context.final_closed_sources[row.key]
            dispositions[row.key] = "EXCLUDED"
    census = Counter(dispositions.values())
    require(
        len(leaf_rows) == 541
        and set(leaf_rows) == set(proof) == set(dispositions)
        and census == EXPECTED_TOP_LEVEL_DISPOSITION,
        "independent 541-leaf census",
    )
    parent = context.source_box
    parent_bounds = {
        "t": (parent.t0, parent.t1),
        "p": (parent.p0, parent.p1),
        "s": (parent.s0, parent.s1),
    }
    axes = ("t", "p", "s")
    leaf_bounds = {
        key: {
            "t": (row.box.t0, row.box.t1),
            "p": (row.box.p0, row.box.p1),
            "s": (row.box.s0, row.box.s1),
        }
        for key, row in leaf_rows.items()
    }
    contained = all(
        all(
            parent_bounds[axis][0] <= box[axis][0] < box[axis][1]
            <= parent_bounds[axis][1]
            for axis in axes
        )
        for box in leaf_bounds.values()
    )
    parent_volume = r215.box_volume(parent)
    leaf_volume = sum(
        (r215.box_volume(row.box) for row in leaf_rows.values()), Q(0)
    )
    ordered = sorted(leaf_rows)
    pair_rows: list[dict[str, Any]] = []
    for first_ordinal, first_key in enumerate(ordered):
        first = leaf_rows[first_key].box
        for second_key in ordered[first_ordinal + 1:]:
            second = leaf_rows[second_key].box
            overlap = (
                max(first.t0, second.t0) < min(first.t1, second.t1)
                and max(first.p0, second.p0) < min(first.p1, second.p1)
                and max(first.s0, second.s0) < min(first.s1, second.s1)
            )
            require(not overlap, "independent strict leaf overlap")
            pair_rows.append({
                "first": first_key,
                "second": second_key,
                "interior_overlap": overlap,
            })
    pair_count = len(pair_rows)
    require(
        contained
        and leaf_volume == parent_volume
        and pair_count == len(leaf_rows) * (len(leaf_rows) - 1) // 2,
        "independent whole-origin 3D reclosure",
    )
    full_ledger = independent_global_full_atomic_owner_ledger(
        leaf_rows, proof, dispositions
    )
    grid = {
        axis: sorted({
            value for box in leaf_bounds.values() for value in box[axis]
        })
        for axis in axes
    }
    owner_audit = {
        "schema": "cm2.round306c30c.exact-full-atomic-owner-audit.v1",
        "audit_scope": "WHOLE_ORIGIN_LINEAGE",
        "leaf_key_kind": "CELL_KEY",
        "exact_3D_enclosure": {
            "all_leaf_boxes_contained_in_parent_and_nondegenerate": True,
            "pairwise_leaf_interiors_disjoint": True,
            "tested_unordered_leaf_pair_count": pair_count,
            "tested_leaf_pair_rows_sha256": digest(pair_rows),
            "leaf_exact_volume_sum": str(leaf_volume),
            "parent_exact_volume": str(parent_volume),
            "leaf_exact_volume_sum_equals_parent": True,
        },
        "axis_grid_coordinate_count": {
            axis: len(values) for axis, values in grid.items()
        },
        "axis_grid_coordinates_sha256": digest({
            axis: [str(value) for value in values]
            for axis, values in grid.items()
        }),
        "atomic_owner_selection_rule": (
            "DETERMINISTIC_LEAF_KEY_LEXICOGRAPHIC_MIN_CONTAINING_LEAF"
        ),
        "closed_3D_leaf_count": len(leaf_rows),
        "closed_3D_leaf_keys_sha256": digest(sorted(leaf_rows)),
        "closed_3D_leaf_disposition_census": dict(sorted(census.items())),
        "C30c_full_atomic_owner_ledger": full_ledger,
        "C30c_full_atomic_owner_ledger_sha256": digest(full_ledger),
        "C30c_full_atomic_owner_rows_are_authoritative_for_join_membership": True,
        "sampled_evidence_used_for_uniform_conclusion": False,
    }
    rebuilt = {
        "owner_audit": owner_audit,
        "full_atomic_owner_ledger": full_ledger,
        "independent_3D_reclosure": {
            "closed_leaf_count": len(leaf_rows),
            "tested_unordered_leaf_pair_count": pair_count,
            "leaf_exact_volume_sum": str(leaf_volume),
            "parent_exact_volume": str(parent_volume),
            "leaf_exact_volume_sum_equals_parent": True,
            "pairwise_leaf_interiors_disjoint": True,
        },
    }
    return rebuilt, census, leaf_rows, proof, dispositions




def independent_inherited_h_relative_binding(
    h_row: dict[str, Any], geometry: dict[str, Any]
) -> dict[str, Any]:
    """Verifier path: global lattice enumeration plus parent membership query."""
    axes = ("t", "p", "s")
    fixed = {axis: Q(value) for axis, value in geometry["fixed"].items()}
    spans = {
        axis: (Q(values[0]), Q(values[1]))
        for axis, values in geometry["open_spans"].items()
    }
    source_dimension = len(spans)
    terminals = h_row["H_partition"]["terminal_rectangles"]
    by_id = {row["terminal_id"]: row for row in terminals}
    boxes = {
        terminal_id: {
            axis: (Q(row["closed_box"][axis][0]),
                   Q(row["closed_box"][axis][1]))
            for axis in axes
        }
        for terminal_id, row in by_id.items()
    }
    applicable = {
        terminal_id for terminal_id, box in boxes.items()
        if all(box[axis][0] <= value <= box[axis][1]
               for axis, value in fixed.items())
        and all(max(lower, box[axis][0]) < min(upper, box[axis][1])
                for axis, (lower, upper) in spans.items())
    }
    require(bool(applicable), "independent inherited H incident terminals")
    span_axes = sorted(spans)
    internal_cuts = {
        axis: sorted({
            endpoint
            for terminal_id in applicable
            for endpoint in boxes[terminal_id][axis]
            if spans[axis][0] < endpoint < spans[axis][1]
        })
        for axis in span_axes
    }
    mesh = {
        axis: [spans[axis][0]] + internal_cuts[axis] + [spans[axis][1]]
        for axis in span_axes
    }
    intervals = {
        axis: list(zip(mesh[axis], mesh[axis][1:])) for axis in span_axes
    }

    def terminal_binding(atomic_geometry: dict[str, Any]) -> dict[str, Any]:
        atomic_fixed = {
            axis: Q(value)
            for axis, value in atomic_geometry["fixed"].items()
        }
        atomic_spans = {
            axis: (Q(values[0]), Q(values[1]))
            for axis, values in atomic_geometry["open_spans"].items()
        }
        probes = {
            axis: (lower + upper) / 2
            for axis, (lower, upper) in atomic_spans.items()
        }
        containing: list[str] = []
        for terminal_id in sorted(boxes):
            if terminal_id not in applicable:
                continue
            box = boxes[terminal_id]
            if any(not box[axis][0] <= value <= box[axis][1]
                   for axis, value in atomic_fixed.items()):
                continue
            if any(
                not (
                    box[axis][0] <= lower < upper <= box[axis][1]
                    and box[axis][0] < probes[axis] < box[axis][1]
                )
                for axis, (lower, upper) in atomic_spans.items()
            ):
                continue
            containing.append(terminal_id)
        require(bool(containing), "independent inherited H terminal owner")
        owner = by_id[containing[0]]
        owner_box = boxes[owner["terminal_id"]]
        relative: dict[str, str] = {}
        for axis, value in sorted(atomic_fixed.items()):
            if value == owner_box[axis][0]:
                relative[axis] = "LOWER"
            elif value == owner_box[axis][1]:
                relative[axis] = "UPPER"
        support: list[dict[str, Any]] = []
        if owner["coarse_disposition"] == "MIXED":
            typed = owner["typed_strata"]
            codimension = len(relative)
            if codimension == 0:
                support = typed["open_3D_sides"] + [
                    typed["H_zero_2D_sheet"]
                ]
            elif codimension == 1:
                axis, side = next(iter(sorted(relative.items())))
                support = [
                    row for row in typed["H_zero_1D_face_incidences"]
                    if row["fixed_axis"] == axis
                    and row["boundary_side"] == side
                ] + [
                    row for row in typed["terminal_face_2D_H_sign_regions"]
                    if row["fixed_axis"] == axis
                    and row["boundary_side"] == side
                ]
            elif codimension == 2:
                support = [
                    row for row in typed["H_zero_0D_edge_incidences"]
                    if row["fixed"] == relative
                ] + [
                    row for row in typed["terminal_edge_1D_H_sign_intervals"]
                    if row["fixed"] == relative
                ]
            else:
                require(codimension == 3,
                        "independent inherited H codimension")
                support = [
                    row for row in typed["H_zero_0D_corner_absence_rows"]
                    if row["corner"] == relative
                ]
            require(bool(support), "independent inherited H typed support")
        pointwise: set[str] = set()
        for support_row in support:
            disposition = support_row.get("disposition")
            if disposition not in {None, "EMPTY"}:
                pointwise.add(disposition)
            corner_disposition = support_row.get("strict_corner_disposition")
            if corner_disposition is not None:
                pointwise.add(corner_disposition)
        if owner["coarse_disposition"] != "MIXED":
            pointwise.add(owner["coarse_disposition"])
        require(bool(pointwise), "independent inherited H disposition set")
        measure = Q(1)
        for lower, upper in atomic_spans.values():
            measure *= upper - lower
        return {
            "exact_measure": str(measure),
            "closed_containing_terminal_ids": containing,
            "half_open_owner_terminal_id": owner["terminal_id"],
            "owner_terminal_row_sha256": owner["row_sha256"],
            "owner_terminal_coarse_disposition": owner[
                "coarse_disposition"
            ],
            "owner_terminal_analytic_evidence": owner["analytic_evidence"],
            "owner_terminal_analytic_evidence_sha256": digest(
                owner["analytic_evidence"]
            ),
            "relative_boundary_signature": relative,
            "relative_boundary_codimension": len(relative),
            "H_sign_sheet_stratum_rows": support,
            "H_sign_sheet_stratum_rows_sha256": digest(support),
            "pointwise_H_predicate_row_count": len(support),
            "pointwise_disposition_set": sorted(pointwise),
            "H_equality_stratum_explicitly_bound": (
                owner["coarse_disposition"] != "MIXED"
                or any(
                    row.get("predicate") in {"H=0", "H=ux*dy-uy*dx=0"}
                    for row in support
                )
            ),
            "H_sign_sheet_pointwise_exhaustive": True,
        }

    geometry_products = (
        itertools.product(*(intervals[axis] for axis in span_axes))
        if span_axes else [()]
    )
    piece_geometries = [{
        "fixed": {
            axis: str(value) for axis, value in sorted(fixed.items())
        },
        "open_spans": {
            axis: [str(interval[0]), str(interval[1])]
            for axis, interval in zip(span_axes, product, strict=True)
        },
    } for product in geometry_products]
    piece_geometries.sort(key=wire)
    piece_rows = [
        sealed({
            "schema": "cm2.round306c30c.inherited-H-relative-atom.row.v2",
            "piece_ordinal": ordinal,
            "piece_geometry": piece_geometry,
            **terminal_binding(piece_geometry),
        })
        for ordinal, piece_geometry in enumerate(piece_geometries)
    ]
    source_measure = Q(1)
    for lower, upper in spans.values():
        source_measure *= upper - lower
    require(
        bool(piece_rows)
        and sum((Q(row["exact_measure"]) for row in piece_rows), Q(0))
        == source_measure,
        "independent inherited H relative exact measure",
    )

    incidence_schema = (
        "cm2.round306c30c.inherited-H-relative-parent-incidence.row.v1"
    )
    line_geometries: list[dict[str, Any]] = []
    if source_dimension == 2:
        for cut_axis in span_axes:
            remaining_axis = next(
                axis for axis in span_axes if axis != cut_axis
            )
            for cut in internal_cuts[cut_axis]:
                for interval in intervals[remaining_axis]:
                    line_geometries.append({
                        "fixed": {
                            axis: str(value)
                            for axis, value in sorted({
                                **fixed, cut_axis: cut,
                            }.items())
                        },
                        "open_spans": {
                            remaining_axis: [
                                str(interval[0]), str(interval[1])
                            ]
                        },
                    })
    unique_lines = {
        wire(item).decode("ascii"): item for item in line_geometries
    }
    line_rows: list[dict[str, Any]] = []
    for ordinal, (_key, line_geometry) in enumerate(sorted(unique_lines.items())):
        line_fixed = {
            axis: Q(value) for axis, value in line_geometry["fixed"].items()
        }
        line_spans = {
            axis: (Q(values[0]), Q(values[1]))
            for axis, values in line_geometry["open_spans"].items()
        }
        parents: list[dict[str, Any]] = []
        for piece in piece_rows:
            piece_spans = {
                axis: (Q(values[0]), Q(values[1]))
                for axis, values in piece["piece_geometry"]["open_spans"].items()
            }
            boundary_axes = [
                axis for axis in piece_spans if axis in line_fixed
                and line_fixed[axis] in piece_spans[axis]
            ]
            if len(boundary_axes) != 1:
                continue
            boundary_axis = boundary_axes[0]
            remaining_axis = next(
                axis for axis in piece_spans if axis != boundary_axis
            )
            if line_spans != {remaining_axis: piece_spans[remaining_axis]}:
                continue
            side = (
                "LOWER"
                if line_fixed[boundary_axis] == piece_spans[boundary_axis][0]
                else "UPPER"
            )
            parents.append(sealed({
                "schema": incidence_schema,
                "parent_kind": "TERMINAL_OPEN_PIECE",
                "parent_row_sha256": piece["row_sha256"],
                "parent_ordinal": piece["piece_ordinal"],
                "boundary_axis": boundary_axis,
                "boundary_side": side,
            }))
        parents.sort(key=wire)
        require(bool(parents), "independent H line parent membership")
        line_rows.append(sealed({
            "schema": (
                "cm2.round306c30c.inherited-H-relative-"
                "internal-cut-equality.row.v1"
            ),
            "cut_ordinal": ordinal,
            "source_atom_dimension": source_dimension,
            "ambient_dimension": 1,
            "geometry": line_geometry,
            "relative_cut_codimension": source_dimension - 1,
            "contains_internal_terminal_cut_equality": True,
            "parent_piece_incidences": parents,
            "parent_piece_incidence_count": len(parents),
            "parent_piece_incidences_sha256": digest(parents),
            **terminal_binding(line_geometry),
        }))

    point_geometries: list[dict[str, Any]] = []
    if source_dimension == 2:
        first_axis, second_axis = span_axes
        point_geometries = [{
            "fixed": {
                axis: str(value)
                for axis, value in sorted({
                    **fixed, first_axis: first, second_axis: second,
                }.items())
            },
            "open_spans": {},
        } for first in internal_cuts[first_axis]
          for second in internal_cuts[second_axis]]
    elif source_dimension == 1:
        free_axis = span_axes[0]
        point_geometries = [{
            "fixed": {
                axis: str(value)
                for axis, value in sorted({**fixed, free_axis: cut}.items())
            },
            "open_spans": {},
        } for cut in internal_cuts[free_axis]]
    unique_points = {
        wire(item).decode("ascii"): item for item in point_geometries
    }
    point_rows: list[dict[str, Any]] = []
    point_parents = line_rows if source_dimension == 2 else piece_rows
    for ordinal, (_key, point_geometry) in enumerate(sorted(unique_points.items())):
        point_fixed = {
            axis: Q(value) for axis, value in point_geometry["fixed"].items()
        }
        parents: list[dict[str, Any]] = []
        for parent in point_parents:
            parent_geometry = (
                parent["geometry"] if source_dimension == 2
                else parent["piece_geometry"]
            )
            parent_fixed = {
                axis: Q(value)
                for axis, value in parent_geometry["fixed"].items()
            }
            parent_spans = {
                axis: (Q(values[0]), Q(values[1]))
                for axis, values in parent_geometry["open_spans"].items()
            }
            if any(point_fixed.get(axis) != value
                   for axis, value in parent_fixed.items()):
                continue
            free_axis, interval = next(iter(parent_spans.items()))
            if point_fixed.get(free_axis) not in interval:
                continue
            side = (
                "LOWER" if point_fixed[free_axis] == interval[0] else "UPPER"
            )
            parents.append(sealed({
                "schema": incidence_schema,
                "parent_kind": (
                    "RECURSIVE_1D_INTERNAL_CUT"
                    if source_dimension == 2 else "TERMINAL_OPEN_PIECE"
                ),
                "parent_row_sha256": parent["row_sha256"],
                "parent_ordinal": parent[
                    "cut_ordinal" if source_dimension == 2
                    else "piece_ordinal"
                ],
                "boundary_axis": free_axis,
                "boundary_side": side,
            }))
        parents.sort(key=wire)
        require(bool(parents), "independent H point parent membership")
        point_rows.append(sealed({
            "schema": (
                "cm2.round306c30c.inherited-H-relative-"
                "internal-cut-equality.row.v1"
            ),
            "cut_ordinal": ordinal,
            "source_atom_dimension": source_dimension,
            "ambient_dimension": 0,
            "geometry": point_geometry,
            "relative_cut_codimension": source_dimension,
            "contains_internal_terminal_cut_equality": True,
            "parent_piece_incidences": parents,
            "parent_piece_incidence_count": len(parents),
            "parent_piece_incidences_sha256": digest(parents),
            **terminal_binding(point_geometry),
        }))
    expected_line_parent_incidences = sum(
        row["parent_piece_incidence_count"] for row in line_rows
    )
    expected_point_parent_incidences = sum(
        row["parent_piece_incidence_count"] for row in point_rows
    )
    recursive = {
        "schema": (
            "cm2.round306c30c.inherited-H-relative-"
            "internal-cut-complex.v1"
        ),
        "source_atom_dimension": source_dimension,
        "internal_terminal_cut_coordinates": {
            axis: [str(value) for value in values]
            for axis, values in sorted(internal_cuts.items())
        },
        "atomic_1D_internal_cut_row_count": len(line_rows),
        "atomic_1D_internal_cut_rows": line_rows,
        "atomic_1D_internal_cut_rows_sha256": digest(line_rows),
        "atomic_0D_internal_cut_row_count": len(point_rows),
        "atomic_0D_internal_cut_rows": point_rows,
        "atomic_0D_internal_cut_rows_sha256": digest(point_rows),
        "expected_1D_parent_piece_incidence_count": (
            expected_line_parent_incidences
        ),
        "expected_0D_parent_piece_incidence_count": (
            expected_point_parent_incidences
        ),
        "pure_geometry_global_deduplication": True,
        "every_internal_terminal_cut_equality_materialized": True,
        "every_recursive_internal_cut_intersection_materialized": True,
        "all_cut_rows_have_exact_terminal_owner_and_H_pointwise_binding": True,
        "point_set_exhaustion_by_dimension": {
            "open_source_atom_dimension": source_dimension,
            "same_dimension_open_piece_count": len(piece_rows),
            "internal_1D_cut_equality_count": len(line_rows),
            "internal_0D_cut_equality_count": len(point_rows),
            "source_endpoints_deferred_to_global_lower_atomic_owner_rows": True,
            "open_pieces_plus_internal_cut_equalities_pointwise_exhaustive": True,
        },
    }
    return {
        "schema": "cm2.round306c30c.inherited-H-relative-binding.v2",
        "H_cell_key": h_row["cell_key"],
        "H_cell_row_sha256": h_row["row_sha256"],
        "source_atomic_geometry": geometry,
        "source_atomic_dimension": source_dimension,
        "terminal_piece_row_count": len(piece_rows),
        "terminal_piece_rows": piece_rows,
        "terminal_piece_rows_sha256": digest(piece_rows),
        "recursive_internal_cut_equality_complex": recursive,
        "recursive_internal_cut_equality_complex_sha256": digest(recursive),
        "all_terminal_pieces_have_explicit_H_sign_sheet_strata": True,
        "all_terminal_pieces_have_explicit_H_pointwise_semantics": True,
        "terminal_cut_partition_exact_measure_reclosed": True,
        "full_relative_point_set_partition_including_cut_equalities": True,
    }


def independently_schedule_and_descend_boundary_joins(
    origin: str,
    leaf_rows: dict[str, Any],
    proof_source: dict[str, str],
    leaf_disposition: dict[str, str],
    combined_rows: list[dict[str, Any]],
    h_rows: list[dict[str, Any]],
    owner_audit: dict[str, Any],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Independent verifier path: schedule geometries, then dimension-descend."""
    axes = ("t", "p", "s")
    boxes = {
        key: tuple((row.box.t0, row.box.t1) if axis == "t" else
                   (row.box.p0, row.box.p1) if axis == "p" else
                   (row.box.s0, row.box.s1) for axis in axes)
        for key, row in leaf_rows.items()
    }
    require(
        len(boxes) == 541
        and set(boxes) == set(proof_source) == set(leaf_disposition),
        "scheduled join 541-leaf universe:" + origin,
    )
    axis_index = {axis: ordinal for ordinal, axis in enumerate(axes)}
    coordinates = {
        axis: sorted({endpoint for box in boxes.values()
                      for endpoint in box[axis_index[axis]]})
        for axis in axes
    }
    combined_by_key = {row["cell_key"]: row for row in combined_rows}
    h_by_key = {row["cell_key"]: row for row in h_rows}
    full_ledger = owner_audit["C30c_full_atomic_owner_ledger"]
    full_rows = sum((
        full_ledger["atomic_" + str(dimension) + "D_owner_rows"]
        for dimension in (2, 1, 0)
    ), [])
    full_owner_index = {
        (row["ambient_dimension"], wire(row["geometry"]).decode("ascii")): row
        for row in full_rows
    }
    require(
        len(full_owner_index) == len(full_rows)
        and owner_audit["C30c_full_atomic_owner_ledger_sha256"]
        == digest(full_ledger),
        "scheduled full atomic owner index",
    )
    identity_registry: dict[str, dict[str, Any]] = {}

    def parts(geometry: dict[str, Any]) -> tuple[dict[str, Q], dict[str, tuple[Q, Q]]]:
        fixed = {axis: Q(value) for axis, value in geometry["fixed"].items()}
        spans = {
            axis: (Q(value[0]), Q(value[1]))
            for axis, value in geometry["open_spans"].items()
        }
        return fixed, spans

    def closure_contains(
        box: tuple[tuple[Q, Q], ...],
        fixed: dict[str, Q],
        spans: dict[str, tuple[Q, Q]],
    ) -> bool:
        for axis, value in fixed.items():
            lower, upper = box[axis_index[axis]]
            if not lower <= value <= upper:
                return False
        for axis, (span_lower, span_upper) in spans.items():
            lower, upper = box[axis_index[axis]]
            if not lower <= span_lower < span_upper <= upper:
                return False
        return True

    def relative_signature(
        box: tuple[tuple[Q, Q], ...],
        fixed: dict[str, Q],
        spans: dict[str, tuple[Q, Q]],
    ) -> dict[str, str] | None:
        if not closure_contains(box, fixed, spans):
            return None
        output: dict[str, str] = {}
        for axis in axes:
            if axis not in fixed:
                continue
            lower, upper = box[axis_index[axis]]
            if fixed[axis] == lower:
                output[axis] = "LOWER"
            elif fixed[axis] == upper:
                output[axis] = "UPPER"
        return output

    def selected_semantics(
        owner: str,
        signature: dict[str, str],
        geometry: dict[str, Any],
    ) -> dict[str, Any]:
        if owner in combined_by_key:
            row = combined_by_key[owner]
            return {
                "kind": "ROUND306C30C_COMBINED_ANALYTIC_PARTITION",
                "owner_cell_row_sha256": row["row_sha256"],
                "relative_atomic_geometry": geometry,
                "analytic_support": independent_typed_boundary_support(
                    row, signature
                ),
            }
        if owner in h_by_key:
            row = h_by_key[owner]
            return {
                "kind": "ROUND306C30C_MATERIALIZED_INHERITED_H",
                "owner_cell_row_sha256": row["row_sha256"],
                "relative_atomic_geometry": geometry,
                "whole_cell_disposition": row["whole_H_cell_disposition"],
                "pointwise_H_partition_sha256": digest(row["H_partition"]),
                "pointwise_semantics_bound_by_complete_H_partition": True,
                "relative_H_sign_sheet_stratum_binding": (
                    independent_inherited_h_relative_binding(row, geometry)
                ),
            }
        return {
            "kind": "PINNED_OR_SEALED_UPSTREAM_LEAF_DISPOSITION",
            "relative_atomic_geometry": geometry,
            "proof_source": proof_source[owner],
            "whole_cell_disposition": leaf_disposition[owner],
        }

    def owner_identity(
        geometry: dict[str, Any]
    ) -> tuple[dict[str, Any], list[dict[str, Any]]]:
        fixed, spans = parts(geometry)
        probe = {
            axis: (span[0] + span[1]) / 2 for axis, span in spans.items()
        }
        candidates: list[str] = []
        for key in sorted(boxes):
            box = boxes[key]
            if not closure_contains(box, fixed, spans):
                continue
            if any(
                not box[axis_index[axis]][0] < value
                < box[axis_index[axis]][1]
                for axis, value in probe.items()
            ):
                continue
            candidates.append(key)
        require(bool(candidates), "scheduled join half-open owner")
        owner = candidates[0]
        full_owner_row = full_owner_index.get((
            len(spans), wire(geometry).decode("ascii")
        ))
        require(
            full_owner_row is not None
            and full_owner_row["closed_containing_leaf_keys"] == candidates
            and full_owner_row["half_open_owner_leaf_key"] == owner
            and full_owner_row["owner_proof_source"] == proof_source[owner]
            and full_owner_row["owner_disposition"] == leaf_disposition[owner],
            "scheduled exact full atomic owner row membership",
        )
        owner_signature: dict[str, str] | None = None
        incidences: list[dict[str, Any]] = []
        for cell_key in sorted(combined_by_key):
            signature = relative_signature(boxes[cell_key], fixed, spans)
            if signature is None:
                continue
            selected = cell_key == owner
            if selected:
                owner_signature = signature
            row = combined_by_key[cell_key]
            incidences.append(sealed({
                "schema": "cm2.round306c30c.atomic-combined-incidence.row.v1",
                "combined_cell_key": cell_key,
                "combined_cell_row_sha256": row["row_sha256"],
                "relative_boundary_codimension": len(signature),
                "relative_boundary_signature": signature,
                "selected_by_half_open_owner": selected,
                "analytic_support": independent_typed_boundary_support(
                    row, signature
                ),
            }))
        require(bool(incidences), "scheduled join combined incidence")
        whole_owner_alignment = sealed({
            "schema": (
                "cm2.round306c30c.whole-origin-atomic-owner-alignment.row.v1"
            ),
            "ambient_dimension": len(spans),
            "geometry": geometry,
            "whole_origin_atomic_owner_audit_sha256": digest(owner_audit),
            "full_atomic_owner_ledger_sha256": owner_audit[
                "C30c_full_atomic_owner_ledger_sha256"
            ],
            "full_atomic_owner_row": full_owner_row,
            "full_atomic_owner_row_sha256": full_owner_row["row_sha256"],
            "unique_geometry_dimension_membership_verified": True,
            "closed_containing_leaf_keys": candidates,
            "half_open_owner_leaf_key": owner,
            "owner_selection_rule": (
                "DETERMINISTIC_LEAF_KEY_LEXICOGRAPHIC_MIN_CONTAINING_LEAF"
            ),
            "owner_proof_source": proof_source[owner],
            "owner_disposition": leaf_disposition[owner],
        })
        identity = {
            "ambient_dimension": len(spans),
            "geometry": geometry,
            "closed_containing_leaf_keys": candidates,
            "half_open_owner_leaf_key": owner,
            "owner_proof_source": proof_source[owner],
            "owner_disposition": leaf_disposition[owner],
            "selected_owner_semantic_binding": selected_semantics(
                owner,
                owner_signature if owner_signature is not None else {},
                geometry,
            ),
            "whole_origin_atomic_owner_alignment": whole_owner_alignment,
        }
        registry_key = str(len(spans)) + ":" + wire(geometry).decode("ascii")
        require(
            identity_registry.setdefault(registry_key, identity) == identity,
            "scheduled cross-incidence atomic identity",
        )
        return identity, incidences

    def split_geometry(absolute: dict[str, Any]) -> list[dict[str, Any]]:
        fixed, spans = parts(absolute)
        interval_lists: list[list[tuple[Q, Q]]] = []
        span_axes = [axis for axis in axes if axis in spans]
        for axis in span_axes:
            lower, upper = spans[axis]
            values = [lower] + [
                value for value in coordinates[axis] if lower < value < upper
            ] + [upper]
            require(values == sorted(set(values)), "scheduled grid cut order")
            interval_lists.append(list(zip(values, values[1:])))
        products = list(itertools.product(*interval_lists)) if span_axes else [()]
        return [{
            "fixed": {axis: str(value) for axis, value in sorted(fixed.items())},
            "open_spans": {
                axis: [str(span[0]), str(span[1])]
                for axis, span in zip(span_axes, product, strict=True)
            },
        } for product in products]

    def codimension_one_children(
        geometry: dict[str, Any]
    ) -> list[tuple[str, str, dict[str, Any]]]:
        fixed, spans = parts(geometry)
        output: list[tuple[str, str, dict[str, Any]]] = []
        for axis in sorted(spans):
            for side, endpoint in (
                ("LOWER", spans[axis][0]), ("UPPER", spans[axis][1])
            ):
                child_fixed = {**fixed, axis: endpoint}
                child_spans = {
                    other: span for other, span in spans.items() if other != axis
                }
                output.append((axis, side, {
                    "fixed": {
                        name: str(value)
                        for name, value in sorted(child_fixed.items())
                    },
                    "open_spans": {
                        name: [str(span[0]), str(span[1])]
                        for name, span in sorted(child_spans.items())
                    },
                }))
        return output

    schedule: list[tuple[dict[str, Any], int, dict[str, Any], dict[str, Any]]] = []
    for cell in sorted(combined_rows, key=lambda row: row["cell_key"]):
        box = boxes[cell["cell_key"]]
        boundaries = cell["outer_boundary_restriction_rows"]
        require(
            len(boundaries) == 26
            and Counter(row["ambient_dimension"] for row in boundaries)
            == Counter({2: 6, 1: 12, 0: 8}),
            "scheduled boundary 6+12+8:" + cell["cell_key"],
        )
        for ordinal, boundary in enumerate(boundaries):
            signature = boundary["fixed_coordinates"]
            fixed = {
                axis: box[axis_index[axis]][0 if side == "LOWER" else 1]
                for axis, side in sorted(signature.items())
            }
            spans = {
                axis: box[axis_index[axis]] for axis in axes if axis not in fixed
            }
            schedule.append((cell, ordinal, boundary, {
                "fixed": {axis: str(value) for axis, value in sorted(fixed.items())},
                "open_spans": {
                    axis: [str(span[0]), str(span[1])]
                    for axis, span in spans.items()
                },
            }))

    output: list[dict[str, Any]] = []
    boundary_census: Counter[str] = Counter()
    primary_census: Counter[str] = Counter()
    lower_census: Counter[str] = Counter()
    for cell, boundary_ordinal, boundary, absolute in schedule:
        primary_geometries = split_geometry(absolute)
        primary_rows: list[dict[str, Any]] = []
        primary_measure = Q(0)
        for atom_ordinal, geometry in enumerate(primary_geometries):
            fixed, spans = parts(geometry)
            measure = Q(1)
            for lower, upper in spans.values():
                measure *= upper - lower
            primary_measure += measure
            identity, incidences = owner_identity(geometry)
            primary_rows.append(sealed({
                "schema": "cm2.round306c30c.boundary-atomic-owner-binding.row.v1",
                "atom_ordinal": atom_ordinal,
                **identity,
                "exact_measure": str(measure),
                "closed_incident_combined_cells": incidences,
                "closed_incident_combined_cells_sha256": digest(incidences),
            }))
            primary_census[str(len(spans)) + "D"] += 1

        dimension = boundary["ambient_dimension"]
        line_groups: dict[str, dict[str, Any]] = {}
        if dimension == 2:
            for parent in primary_rows:
                for axis, side, child in codimension_one_children(
                    parent["geometry"]
                ):
                    key = wire(child).decode("ascii")
                    group = line_groups.setdefault(key, {
                        "geometry": child, "parents": [],
                    })
                    group["parents"].append({
                        "parent_2D_atom_ordinal": parent["atom_ordinal"],
                        "fixed_axis": axis, "side": side,
                    })
        line_rows: list[dict[str, Any]] = []
        for cut_ordinal, key in enumerate(sorted(line_groups)):
            group = line_groups[key]
            identity, incidences = owner_identity(group["geometry"])
            _fixed, span_map = parts(group["geometry"])
            lower, upper = next(iter(span_map.values()))
            parents = sorted(group["parents"], key=wire)
            line_rows.append(sealed({
                "schema": "cm2.round306c30c.recursive-1D-cut-owner.row.v1",
                "cut_ordinal": cut_ordinal,
                **identity,
                "exact_measure": str(upper - lower),
                "incident_parent_2D_atom_ordinals": sorted(set(
                    row["parent_2D_atom_ordinal"] for row in parents
                )),
                "parent_boundary_sides": parents,
                "closed_incident_combined_cells": incidences,
                "closed_incident_combined_cells_sha256": digest(incidences),
            }))

        point_groups: dict[str, dict[str, Any]] = {}
        point_parents = (
            [("RECURSIVE_1D_CUT", row, "cut_ordinal") for row in line_rows]
            if dimension == 2 else
            [("PRIMARY_1D_ATOM", row, "atom_ordinal") for row in primary_rows]
            if dimension == 1 else []
        )
        for kind, parent, ordinal_field in point_parents:
            for _axis, side, child in codimension_one_children(parent["geometry"]):
                key = wire(child).decode("ascii")
                group = point_groups.setdefault(key, {
                    "geometry": child, "parents": [],
                })
                group["parents"].append({
                    "parent_kind": kind,
                    "parent_ordinal": parent[ordinal_field],
                    "side": side,
                })
        point_rows: list[dict[str, Any]] = []
        for point_ordinal, key in enumerate(sorted(point_groups)):
            group = point_groups[key]
            identity, incidences = owner_identity(group["geometry"])
            point_rows.append(sealed({
                "schema": "cm2.round306c30c.recursive-0D-cut-owner.row.v1",
                "point_ordinal": point_ordinal,
                **identity,
                "incident_1D_parents": sorted(group["parents"], key=wire),
                "closed_incident_combined_cells": incidences,
                "closed_incident_combined_cells_sha256": digest(incidences),
            }))
        require(
            (dimension != 2 or sum(len(row["parent_boundary_sides"])
                                   for row in line_rows) == 4 * len(primary_rows))
            and (dimension == 0 or sum(len(row["incident_1D_parents"])
                                       for row in point_rows)
                 == 2 * len(point_parents)),
            "scheduled recursive membership exhaustion:" + cell["cell_key"],
        )
        lower_census["1D"] += len(line_rows)
        lower_census["0D"] += len(point_rows)
        fixed, source_spans = parts(absolute)
        source_measure = Q(1)
        for lower, upper in source_spans.values():
            source_measure *= upper - lower
        require(primary_measure == source_measure, "scheduled source measure")
        output.append(sealed({
            "schema": "cm2.round306c30c.combined-boundary-atomic-owner-join.row.v1",
            "origin_key": origin,
            "combined_cell_key": cell["cell_key"],
            "combined_cell_row_sha256": cell["row_sha256"],
            "boundary_ordinal_within_cell": boundary_ordinal,
            "boundary_restriction_row_sha256": boundary["row_sha256"],
            "fixed_coordinates": boundary["fixed_coordinates"],
            "ambient_dimension": dimension,
            "absolute_boundary_geometry": absolute,
            "source_exact_measure": str(source_measure),
            "atomic_exact_measure": str(primary_measure),
            "atomic_measure_reclosed": True,
            "atomic_binding_count": len(primary_rows),
            "atomic_bindings": primary_rows,
            "atomic_bindings_sha256": digest(primary_rows),
            "recursive_lower_strata": {
                "generation_rule": (
                    "EVERY_2D_ATOM_MATERIALIZES_ALL_FOUR_1D_CUT_EDGES__"
                    "EVERY_1D_CUT_OR_PRIMARY_ATOM_MATERIALIZES_BOTH_0D_ENDPOINTS__"
                    "PURE_GEOMETRY_DEDUP_WITH_INCIDENT_PARENT_MEMBERSHIP"
                ),
                "atomic_1D_cut_row_count": len(line_rows),
                "atomic_1D_cut_rows": line_rows,
                "atomic_1D_cut_rows_sha256": digest(line_rows),
                "atomic_0D_cut_row_count": len(point_rows),
                "atomic_0D_cut_rows": point_rows,
                "atomic_0D_cut_rows_sha256": digest(point_rows),
                "all_2D_atom_cut_lines_materialized": (
                    dimension != 2 or bool(line_rows)
                ),
                "all_1D_cut_endpoints_materialized": (
                    dimension == 0 or bool(point_rows)
                ),
                "lower_strata_owner_identity_bound_to_whole_origin_grid": True,
            },
            "source_boundary_analytic_support": (
                independent_typed_boundary_support(
                    cell, boundary["fixed_coordinates"]
                )
            ),
            "composition_order": [
                "WHOLE_ORIGIN_GRID_ATOM_IS_CLOSED_RECONSTRUCTED",
                "LEXICOGRAPHIC_MIN_CONTAINING_LEAF_SELECTS_HALF_OPEN_OWNER",
                "SELECTED_OWNER_PROOF_BINDS_POINTWISE_DISPOSITION",
                "IF_SELECTED_OWNER_IS_COMBINED_APPLY_EXACT_RELATIVE_ANALYTIC_STRATUM",
            ],
            "child_or_measure_count_used_as_integer_credit": 0,
        }))
        boundary_census[str(dimension) + "D"] += 1

    output.sort(key=lambda row: (
        row["combined_cell_key"], row["boundary_ordinal_within_cell"]
    ))
    require(
        len(output) == 1040
        and boundary_census == Counter({"2D": 240, "1D": 480, "0D": 320}),
        "scheduled 40x26 boundary census:" + origin,
    )
    summary = {
        "schema": "cm2.round306c30c.combined-boundary-atomic-owner-join.summary.v1",
        "row_count": len(output),
        "row_sha256_sequence_sha256": digest([
            row["row_sha256"] for row in output
        ]),
        "boundary_dimension_census": dict(sorted(boundary_census.items())),
        "materialized_atom_incidence_census": dict(sorted(primary_census.items())),
        "recursive_lower_strata_row_census": dict(sorted(lower_census.items())),
        "unique_atomic_geometry_owner_identity_count": len(identity_registry),
        "unique_atomic_geometry_owner_identities_sha256": digest([
            identity_registry[key] for key in sorted(identity_registry)
        ]),
        "whole_origin_atomic_owner_audit_sha256": digest(owner_audit),
        "owner_selection_rule": (
            "DETERMINISTIC_LEAF_KEY_LEXICOGRAPHIC_MIN_CONTAINING_LEAF"
        ),
        "every_boundary_measure_exactly_reclosed": True,
        "every_atom_has_pointwise_semantic_owner_binding": True,
        "every_atom_has_object_level_whole_origin_owner_alignment": True,
        "every_2D_atom_cut_line_and_1D_cut_endpoint_materialized": True,
        "sampled_evidence_used_for_uniform_conclusion": False,
    }
    return output, summary


def descriptor_check(
    filename: str,
    raw: bytes,
    descriptor: dict[str, Any],
    rows: list[dict[str, Any]],
    order: str,
) -> None:
    sequence = hashlib.sha256()
    for row in rows:
        sequence.update(bytes.fromhex(row["row_sha256"]))
    require(
        descriptor == {
            "filename": filename,
            "row_count": len(rows),
            "size": len(raw),
            "sha256": hashlib.sha256(raw).hexdigest(),
            "row_sequence_sha256": sequence.hexdigest(),
            "order": order,
        },
        "ledger descriptor:" + filename,
    )


def validate_origin_row(
    candidate: dict[str, Any],
    ordinal: int,
    context: OriginContext,
    replay: dict[str, Any],
    h_rows: list[dict[str, Any]],
    combined_rows: list[dict[str, Any]],
    join_rows: list[dict[str, Any]],
) -> None:
    rebuilt, census, leaf_rows, proof_source, leaf_disposition = (
        independent_owner_audit(context, h_rows, combined_rows)
    )
    owner_audit = rebuilt["owner_audit"]
    expected_join_rows, join_summary = independently_schedule_and_descend_boundary_joins(
        context.origin,
        leaf_rows,
        proof_source,
        leaf_disposition,
        combined_rows,
        h_rows,
        owner_audit,
    )
    require(
        join_rows == expected_join_rows,
        "object-level analytic/atomic join:" + context.origin,
    )
    parent = replay["origins"][context.origin]["box"]
    prior_volume = sum(
        (r215.box_volume(box) for box in context.prior_boxes.values()), Q(0)
    )
    base_volume = sum(
        (r215.box_volume(row.box) for row in context.base_rows), Q(0)
    )
    root_volume = sum((r215.box_volume(row.box) for row in context.roots), Q(0))
    inherited_volume = sum(
        (
            r215.box_volume(context.leaves["terminal"][row["cell_key"]].box)
            for row in context.refinement["terminal_rows"]
        ), Q(0)
    )
    final_rows = sorted(
        context.refinement["final_residual_rows"], key=lambda row: row.key
    )
    final_volume = sum((r215.box_volume(row.box) for row in final_rows), Q(0))
    combined_volume = sum((Q(row["exact_volume"]) for row in combined_rows), Q(0))
    closed_volume = sum(
        (r215.box_volume(row.box) for row in final_rows
         if row.key in context.final_closed_sources), Q(0)
    )
    parent_volume = r215.box_volume(parent)
    require(
        prior_volume + base_volume + root_volume == parent_volume
        and inherited_volume + final_volume == root_volume
        and closed_volume + combined_volume == final_volume,
        "independent origin volume conservation",
    )
    first_live = min(
        [{
            "kind": "ROUND180_DIRECT_STRICT_LIVE_POSITIVE_VOLUME",
            "cell_key": row["cell_key"],
            "exact_volume": str(r215.box_volume(
                context.leaves["terminal"][row["cell_key"]].box
            )),
        } for row in context.direct_live]
        + [{
            "kind": "COMBINED_DELTA_H_LIVE_OPEN_SIDE",
            "cell_key": row["cell_key"],
            "predicate": LIVE_H_SIGN_BY_CHART[row["source_chart_id"]]
            + " AND Delta<0",
        } for row in combined_rows],
        key=wire,
    )
    lineage = dict(EXPECTED_LINEAGE)
    theorem = {
        "kind": "SOURCE_W_FULL_DELTA_WHOLE_ORIGIN_RESOLVED_MIXED_THEOREM_CANDIDATE",
        "top_level_dyadic_leaf_partition_exact": True,
        "top_level_leaf_disposition_census": dict(sorted(census.items())),
        "every_combined_cell_has_exhaustive_disjoint_five_stratum_partition": True,
        "every_Delta_H_intersection_empty_including_boundary_restrictions": True,
        "all_combined_cells_mixed": True,
        "positive_measure_live_subset_exists": True,
        "positive_measure_excluded_subset_exists": True,
        "whole_original_physical_origin_disposition": "RESOLVED_MIXED",
        "whole_original_physical_origin_excluded": False,
    }
    flattened_boundaries = [
        boundary for row in combined_rows
        for boundary in row["outer_boundary_restriction_rows"]
    ]
    expected = {
        "schema": "cm2.round306c30c.source-w-full-delta.whole-origin-row.v1",
        "origin_ordinal": ordinal,
        "origin_key": context.origin,
        "priority_ordinal": context.registry["priority_ordinal"],
        "source_chart_id": replay["origins"][context.origin]["chart_id"],
        "original_parent_box": r176.box_row(parent),
        "lineage_census": lineage,
        "top_level_leaf_disposition_census": dict(sorted(census.items())),
        "combined_Delta_H_cell_count": 40,
        "combined_Delta_H_cell_keys_sha256": digest([
            row["cell_key"] for row in combined_rows
        ]),
        "combined_Delta_H_cell_rows_sha256": digest(combined_rows),
        "inherited_H_cell_count": 44,
        "inherited_H_cell_keys_sha256": digest([
            row["cell_key"] for row in h_rows
        ]),
        "inherited_H_cell_rows_sha256": digest(h_rows),
        "disposition_aware_half_open_owner_audit": owner_audit,
        "combined_boundary_to_atomic_owner_binding": join_summary,
        "exact_volume_conservation": {
            "original_parent": str(parent_volume),
            "Round176_prior": str(prior_volume),
            "Round176_preclosed": str(base_volume),
            "Round176_roots": str(root_volume),
            "Round180_inherited": str(inherited_volume),
            "Round180_final": str(final_volume),
            "final_closed": str(closed_volume),
            "combined_Delta_H": str(combined_volume),
            "all_equalities_verified": True,
        },
        "lexicographic_first_positive_measure_LIVE_witness": first_live,
        "whole_origin_theorem_candidate": theorem,
        "whole_origin_theorem_candidate_sha256": digest(theorem),
        "whole_origin_disposition": "RESOLVED_MIXED",
        "whole_original_physical_origin_excluded": False,
        "candidate_credit_if_independently_verified": {
            "resolved_source_W_origin_disposition": 1,
            "resolved_nonexcluded": 1,
            "whole_source_W_origin_exclusion": 0,
        },
        "formal_credit": {
            "resolved_source_W_origin_disposition": 0,
            "resolved_nonexcluded": 0,
            "whole_source_W_origin_exclusion": 0,
        },
        "strict_nonpromotion": "PRODUCER_ONLY__NO_INDEPENDENT_VERIFIER_OR_MANIFEST",
    }
    require(
        candidate == sealed(expected)
        and rebuilt["independent_3D_reclosure"][
            "leaf_exact_volume_sum_equals_parent"
        ] is True,
        "exact independent whole-origin row:" + context.origin,
    )


def expected_result_body(
    input_pins: list[dict[str, str]],
    runtime_descriptor: dict[str, Any],
    combined_descriptor: dict[str, Any],
    h_descriptor: dict[str, Any],
    join_descriptor: dict[str, Any],
    origin_descriptor: dict[str, Any],
) -> dict[str, Any]:
    return {
        "schema": "cm2.round306c30c.source-w-full-delta-whole-origin-disposition.candidate.v1",
        "status": "PASS_CANDIDATE_ROUND306C30C_FULL_DELTA_DISPOSITION__AWAITING_INDEPENDENT_VERIFIER_AND_MANIFEST",
        "input_pins": input_pins,
        "runtime_attestation": runtime_descriptor,
        "upstream_C30b_dependency": {
            "pinned_reusable_producer_source": C30B_PRODUCER,
            "pinned_reusable_producer_source_sha256": C30B_PRODUCER_SHA256,
            "controlled_seed_guard_reused": True,
            "canonical_gzip_and_result_contract_reused": True,
            "producer_runtime_contract": (
                "ENV_I_EXACT_4_VARIABLES__PYTHONHASHSEED_IN_{30630071,30630929}"
                "__PYTHON_-P_-s_-B"
            ),
            "cold_verifier_runtime_contract": "PYTHON_-I_-B",
            "sealed_C30b_result_consumed": True,
            "sealed_authority": {
                "manifest_sha256": C30B_MANIFEST_SHA256,
                "verification_sha256": C30B_VERIFICATION_SHA256,
                "producer_sha256": C30B_PRODUCER_SHA256,
                "independent_verifier_sha256": C30B_VERIFIER_SHA256,
                "result_file_sha256": C30B_RESULT_FILE_SHA256,
                "result_object_sha256": C30B_RESULT_OBJECT_SHA256,
                "sealed_member_count": len(C30B_SEALED_FILE_PINS),
                "manifest_member_count": len(C30B_MANIFEST_MEMBER_PINS),
                "formal_source_W_remaining": 80,
            },
            "baseline_80_transition_is_formal_C30b_state": True,
            "official_C30b_credit_consumed": {
                "resolved_origin_disposition": 12,
                "resolved_nonexcluded": 10,
                "whole_origin_exclusion": 2,
            },
            "official_C30c_credit_granted_by_this_candidate": 0,
        },
        "scope": {
            "origin_count": 2,
            "origin_keys": list(ORIGIN_KEYS),
            "origin_keys_sha256": digest(list(ORIGIN_KEYS)),
            "combined_Delta_H_cell_count": 80,
            "combined_source_census": {
                "ROUND215_FULL_DELTA_NEGATIVE_SIDE": 60,
                "ROUND306C30A_CLIPPED_DELTA_RESIDUAL": 20,
            },
            "inherited_H_cell_count": 88,
            "whole_origin_disposition_census": {"RESOLVED_MIXED": 2},
            "whole_origin_exclusion_count": 0,
        },
        "candidate_theorem": {
            "one_sided_H_bracket_used": True,
            "Delta_strictly_negative_on_every_closed_H_bracket": True,
            "Delta_zero_intersect_H_zero_empty_on_all_80_cells": True,
            "every_combined_cell_has_disjoint_exhaustive_3D_2D_1D_0D_partition": True,
            "every_origin_has_exact_541_leaf_half_open_owner_audit": True,
            "all_2080_combined_boundary_rows_have_materialized_atomic_owner_joins": True,
            "both_whole_origins_are_resolved_mixed": True,
            "child_count_or_volume_used_as_whole_origin_credit": False,
        },
        "proposed_source_W_ledger_transition_if_independently_verified": {
            "before": {
                "excluded": 74746, "conservative_live": 2086,
                "remaining": 80, "resolved_nonexcluded": 2006,
                "total": 76832,
                "remaining_partition": {
                    "full_Delta": 2, "multi_Delta": 20,
                    "reduced_live": 2, "retained_source_seams": 2,
                    "compact_q": 54,
                },
            },
            "candidate_credits": {
                "whole_origin_exclusion": 0,
                "resolved_origin_disposition": 2,
                "resolved_nonexcluded": 2,
            },
            "after": {
                "excluded": 74746, "conservative_live": 2086,
                "remaining": 78, "resolved_nonexcluded": 2008,
                "total": 76832,
                "remaining_partition": {
                    "multi_Delta": 20, "reduced_live": 2,
                    "retained_source_seams": 2, "compact_q": 54,
                },
            },
            "conservation_identity": "74746+2086=76832",
            "official_ledger_mutated": False,
        },
        "ledgers": {
            "combined_Delta_H_cell_candidate": combined_descriptor,
            "inherited_H_cell_candidate": h_descriptor,
            "combined_boundary_atomic_owner_join_candidate": join_descriptor,
            "whole_origin_disposition_candidate": origin_descriptor,
        },
        "formal_credit": {
            "combined_Delta_H_cell_dispositions": 0,
            "resolved_source_W_origin_dispositions": 0,
            "resolved_nonexcluded": 0,
            "whole_source_W_origin_exclusions": 0,
        },
        "candidate_credit_if_independently_verified": {
            "combined_Delta_H_cell_dispositions": 80,
            "resolved_source_W_origin_dispositions": 2,
            "resolved_nonexcluded": 2,
            "whole_source_W_origin_exclusions": 0,
        },
        "strict_nonpromotion": {
            "producer_only": True,
            "independent_verifier_present": False,
            "attack_harness_present": False,
            "dual_seed_replay_present": False,
            "cold_replay_present": False,
            "manifest_present": False,
            "official_source_W_transition": "UNCHANGED_FROM_LAST_SEALED_ROUND",
            "D02": "BLOCKED_BY_LAST_SEALED_SOURCE_W_STATE_AND_COMPOSITE_GATE",
            "D03": "UNAUTHORIZED", "D04": "NOT_MINTED",
            "Gate5_filled_field_slots": "10/18",
            "Gate5_complete_global_blocks": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "required_next": "RUN_INDEPENDENT_C30C_VERIFIER_ATTACK_HARNESS_DUAL_CONTROLLED_SEED_REPLAY_SCRUBBED_COLD_REPLAY_AND_MANIFEST_BEFORE_ANY_C30C_LEDGER_CREDIT",
    }


def verify_candidate_dir(candidate: Path, reference: Reference) -> dict[str, Any]:
    expected_files = {
        COMBINED_CELL_LEDGER, INHERITED_H_LEDGER, JOIN_LEDGER, ORIGIN_LEDGER,
        RESULT, C30B_RUNTIME,
    }
    capture = capture_candidate_bytes(candidate, expected_files)
    raw = capture.raw_by_filename
    require(
        raw[C30B_RUNTIME] == base.BOOTSTRAP_RUNTIME_ATTESTATION_RAW,
        "candidate runtime byte identity",
    )
    combined_rows = canonical_rows_from_bytes(
        raw[COMBINED_CELL_LEDGER], COMBINED_CELL_LEDGER
    )
    h_rows = canonical_rows_from_bytes(raw[INHERITED_H_LEDGER], INHERITED_H_LEDGER)
    join_rows = canonical_rows_from_bytes(raw[JOIN_LEDGER], JOIN_LEDGER)
    origin_rows = canonical_rows_from_bytes(raw[ORIGIN_LEDGER], ORIGIN_LEDGER)
    result = base.strict_object_bytes(raw[RESULT], RESULT)
    require(
        wire(result) == raw[RESULT]
        and len(combined_rows) == 80
        and len(h_rows) == 88
        and len(join_rows) == 2080
        and len(origin_rows) == 2
        and [row["cell_key"] for row in combined_rows]
        == sorted(row["cell_key"] for row in combined_rows)
        and [row["cell_key"] for row in h_rows]
        == sorted(row["cell_key"] for row in h_rows)
        and [
            (row["combined_cell_key"], row["boundary_ordinal_within_cell"])
            for row in join_rows
        ] == sorted(
            (row["combined_cell_key"], row["boundary_ordinal_within_cell"])
            for row in join_rows
        )
        and [row["origin_key"] for row in origin_rows] == list(ORIGIN_KEYS),
        "C30c candidate canonical row order/census",
    )
    h_by_origin: dict[str, list[dict[str, Any]]] = defaultdict(list)
    combined_by_origin: dict[str, list[dict[str, Any]]] = defaultdict(list)
    join_by_origin: dict[str, list[dict[str, Any]]] = defaultdict(list)
    global_combined_sources: list[
        tuple[Any, dict[str, Any], dict[str, Any], dict[str, Any] | None]
    ] = []
    global_h_sources: list[tuple[str, Any, dict[str, Any]]] = []
    for origin in ORIGIN_KEYS:
        context = reference.contexts[origin]
        global_h_sources.extend(context.h_sources)
        global_combined_sources.extend(context.combined_sources)
    global_h_sources.sort(key=lambda item: item[1].key)
    global_combined_sources.sort(key=lambda item: item[0].key)
    for candidate_row, (source_kind, source, binding) in zip(
        h_rows, global_h_sources, strict=True
    ):
        require(candidate_row["cell_key"] == source.key, "H source order")
        validate_h_row(candidate_row, source_kind, source, binding)
        h_by_origin[source.origin_key].append(candidate_row)
    for ordinal, (candidate_row, source) in enumerate(zip(
        combined_rows, global_combined_sources, strict=True
    )):
        row, reduction, evidence, c30a_row = source
        require(candidate_row["cell_key"] == row.key, "combined source order")
        validate_combined_candidate(
            candidate_row, ordinal, row, reduction, evidence, c30a_row
        )
        combined_by_origin[row.origin_key].append(candidate_row)
    for row in join_rows:
        require(row["origin_key"] in set(ORIGIN_KEYS), "join origin scope")
        join_by_origin[row["origin_key"]].append(row)
    for ordinal, candidate_row in enumerate(origin_rows):
        origin = ORIGIN_KEYS[ordinal]
        validate_origin_row(
            candidate_row, ordinal, reference.contexts[origin],
            reference.replay, h_by_origin[origin], combined_by_origin[origin],
            join_by_origin[origin],
        )

    combined_descriptor = result["ledgers"]["combined_Delta_H_cell_candidate"]
    h_descriptor = result["ledgers"]["inherited_H_cell_candidate"]
    join_descriptor = result["ledgers"][
        "combined_boundary_atomic_owner_join_candidate"
    ]
    origin_descriptor = result["ledgers"]["whole_origin_disposition_candidate"]
    descriptor_check(
        COMBINED_CELL_LEDGER, raw[COMBINED_CELL_LEDGER],
        combined_descriptor, combined_rows,
        "LEXICOGRAPHIC_ROUND180_FINAL_CELL_KEY",
    )
    descriptor_check(
        INHERITED_H_LEDGER, raw[INHERITED_H_LEDGER], h_descriptor, h_rows,
        "LEXICOGRAPHIC_ROUND180_INHERITED_H_CELL_KEY",
    )
    descriptor_check(
        JOIN_LEDGER, raw[JOIN_LEDGER], join_descriptor, join_rows,
        "LEXICOGRAPHIC_COMBINED_CELL_KEY_THEN_BOUNDARY_ORDINAL",
    )
    descriptor_check(
        ORIGIN_LEDGER, raw[ORIGIN_LEDGER], origin_descriptor, origin_rows,
        "LEXICOGRAPHIC_SOURCE_W_ORIGIN_KEY",
    )
    runtime_descriptor = {
        "filename": C30B_RUNTIME,
        "size": len(base.BOOTSTRAP_RUNTIME_ATTESTATION_RAW),
        "sha256": base.RUNTIME_ATTESTATION_RAW_SHA256,
        "attestation_payload_sha256": base.RUNTIME_ATTESTATION_PAYLOAD_SHA256,
        "auditor_sha256": base.RUNTIME_AUDITOR_SHA256,
        "schema": base.BOOTSTRAP_RUNTIME_ATTESTATION["schema"],
        "verdict": base.BOOTSTRAP_RUNTIME_ATTESTATION["verdict"],
    }
    input_pins = [
        {"filename": filename, "sha256": sha256}
        for filename, sha256 in reference.input_pins
    ]
    expected_body = expected_result_body(
        input_pins, runtime_descriptor, combined_descriptor,
        h_descriptor, join_descriptor, origin_descriptor,
    )
    require(
        result.get("strict_nonpromotion", {}).get("D02")
        == "BLOCKED_BY_LAST_SEALED_SOURCE_W_STATE_AND_COMPOSITE_GATE"
        and result.get("strict_nonpromotion", {}).get("official_source_W_transition")
        == "UNCHANGED_FROM_LAST_SEALED_ROUND",
        "C30c D02 fail-close",
    )
    require(
        result.get("strict_nonpromotion", {}).get("CM2") == "NO-GO_FOR_CLAIM"
        and result.get("strict_nonpromotion", {}).get(
            "Gate5_complete_global_blocks"
        ) == 0,
        "C30c CM2 fail-close",
    )
    require(
        result == {
            **expected_body, "result_sha256": digest(expected_body)
        }
        and result["formal_credit"] == {
            "combined_Delta_H_cell_dispositions": 0,
            "resolved_source_W_origin_dispositions": 0,
            "resolved_nonexcluded": 0,
            "whole_source_W_origin_exclusions": 0,
        }
        and dict(reference.c30b_authority)["result_object_sha256"]
        == C30B_RESULT_OBJECT_SHA256,
        "exact candidate-only C30c result",
    )
    require(
        PRODUCER[:-3] not in sys.modules
        and C30B_PRODUCER[:-3] not in sys.modules,
        "no producer imported or executed",
    )
    require_candidate_capture_still_current(capture)
    return {
        "schema": "cm2.round306c30c.source-w-full-delta.independent-verification.candidate.v1",
        "status": "PASS_INDEPENDENT_CANDIDATE_C30C__80_DELTA_H_CELLS__2_RESOLVED_MIXED__ZERO_FORMAL_CREDIT",
        "candidate_result_sha256": result["result_sha256"],
        "candidate_combined_ledger_sha256": hashlib.sha256(
            raw[COMBINED_CELL_LEDGER]
        ).hexdigest(),
        "candidate_inherited_H_ledger_sha256": hashlib.sha256(
            raw[INHERITED_H_LEDGER]
        ).hexdigest(),
        "candidate_boundary_atomic_join_ledger_sha256": hashlib.sha256(
            raw[JOIN_LEDGER]
        ).hexdigest(),
        "candidate_origin_ledger_sha256": hashlib.sha256(
            raw[ORIGIN_LEDGER]
        ).hexdigest(),
        "C30b_input_kind": "FIXED_FORMALLY_SEALED_MANIFEST_AUTHORITY",
        "C30b_sealed_authority": dict(reference.c30b_authority),
        "combined_Delta_H_cell_census": 80,
        "Delta_H_intersection_census": {"EMPTY_CERTIFIED": 80},
        "whole_origin_disposition_census": {"RESOLVED_MIXED": 2},
        "proposed_source_W_remaining_transition": "80->78",
        "formal_credit": 0,
        "manifest_authorized": False,
        "candidate_producer_imported_or_executed": False,
        "D02": "BLOCKED_BY_LAST_SEALED_SOURCE_W_STATE_AND_COMPOSITE_GATE",
        "required_before_promotion": "C30C_ATTACK_DUAL_CONTROLLED_SEED_COLD_REPLAY_MANIFEST",
    }


def verify(candidate: Path) -> dict[str, Any]:
    return verify_candidate_dir(candidate, reconstruct_reference())


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("candidate", type=Path)
    arguments = parser.parse_args()
    try:
        output = verify(arguments.candidate)
    except (
        Reject, base.Reject, KeyError, OSError, ValueError, TypeError,
        AssertionError,
    ) as error:
        print(wire({
            "schema": "cm2.round306c30c.source-w-full-delta.independent-verification.candidate.v1",
            "status": "FAIL_CLOSED",
            "formal_credit": 0,
            "manifest_authorized": False,
            "error": str(error),
        }).decode("ascii"))
        return 1
    print(wire(output).decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
