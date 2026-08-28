#!/usr/bin/env python3
"""Produce the *candidate-only* C30c full-Delta source-W certificate.

This producer handles exactly the two frozen full-Delta origins

    W:N:04.00.10000010
    W:S:H.04.00.10000010

and deliberately grants no formal ledger credit.  It reconstructs the
R176/R180/R201/R215/C30a lineage, materializes every inherited outgoing-H
cell, and resolves the forty remaining Delta/H cells in each origin by a
one-sided H-graph bracket.  The decisive certificate is that Delta for the
mismatch G target is strictly negative on the entire closed H bracket.
Consequently Delta=0 and H=0 are disjoint, including every owned outer
face, edge, and vertex.

The output consumes the fixed, formally sealed C30b 80-origin baseline and
is a deterministic C30c candidate for an independent verifier.  It must not
be promoted, sealed, or used to mutate the official source-W ledger merely
because this producer completes successfully.
"""
from __future__ import annotations

import argparse
import ctypes
import errno
import gzip
import hashlib
import importlib.machinery
import itertools
import json
import os
import shutil
import stat
import sys
import tempfile
import types
from collections import Counter, defaultdict
from fractions import Fraction as Q
from pathlib import Path
from typing import Any, Iterable

sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parent
PREFIX = "cm2_round306c30c_source_w_full_delta_whole_origin_disposition"
COMBINED_CELL_LEDGER = PREFIX + "_delta_h_cell_ledger.jsonl.gz"
INHERITED_H_LEDGER = PREFIX + "_inherited_h_cell_ledger.jsonl.gz"
ORIGIN_LEDGER = PREFIX + "_whole_origin_ledger.jsonl.gz"
JOIN_LEDGER = PREFIX + "_combined_boundary_atomic_owner_join_ledger.jsonl.gz"
RESULT = PREFIX + "_result.json"

C30B_SOURCE = (
    "cm2_round306c30b_source_w_outgoing_h_"
    "whole_origin_disposition_producer.py"
)
C30B_SOURCE_SHA256 = (
    "003191131bff227453d07fa22ecd6e95b4f9d48e9ff74604ea4b7116f5818762"
)
C30B_PREFIX = "cm2_round306c30b_source_w_outgoing_h_whole_origin_disposition"
C30B_VERIFIER = C30B_PREFIX + "_independent_verifier.py"
C30B_VERIFIER_SHA256 = (
    "1776137520b1add49a218e6ccce680aaffdafc195c99ef7992c1a5ee31694b66"
)
C30B_MANIFEST = C30B_PREFIX + "_manifest.sha256"
C30B_MANIFEST_SHA256 = (
    "6af636a4239f390712d057030f03e09fbbca332c6170f183d3d0095f19f0f248"
)
C30B_VERIFICATION = C30B_PREFIX + "_verification.json"
C30B_VERIFICATION_SHA256 = (
    "e9e72536be9ba707fe2fdf6034b47978be4d09235e5133414ec7b0a31acf4e71"
)
C30B_SEALED_DIRNAME = "cm2_round306c30b_sealed"
C30B_RESULT = C30B_PREFIX + "_result.json"
C30B_RESULT_FILE_SHA256 = (
    "b015e5bd6a4ee01d71ac95765d07dcbc63c3888f0c8ff9205e2d8c688958c11b"
)
C30B_RESULT_OBJECT_SHA256 = (
    "7abf8da628eb35b20ed27b032dc55ea29e9944530d2d5a6a64993a995f1ad85e"
)
C30B_SEALED_FILE_PINS = {
    "cm2_round306c30b_python_flint_runtime_attestation.json":
        "6b48cd0ca3fd53f9fdd457cc3c1106055e12db4d4ad999fcfd1fc89ad36b95df",
    C30B_PREFIX + "_h_cell_ledger.jsonl.gz":
        "4259fdaadfe1b5e1c0b7b315ef71fdae245bb3bbc45c5f814c4d4b7a670e8672",
    C30B_RESULT: C30B_RESULT_FILE_SHA256,
    C30B_PREFIX + "_whole_origin_ledger.jsonl.gz":
        "19edfece87d4f95e3e25a62d508654918c03ec879f574ab01854bde5bee4c6c9",
}
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
    C30B_SOURCE: C30B_SOURCE_SHA256,
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

BEFORE_EXCLUDED = 74_746
BEFORE_LIVE = 2_086
BEFORE_REMAINING = 80
BEFORE_RESOLVED_NONEXCLUDED = 2_006
AFTER_EXCLUDED = 74_746
AFTER_LIVE = 2_086
AFTER_REMAINING = 78
AFTER_RESOLVED_NONEXCLUDED = 2_008

EXPECTED_PER_ORIGIN = {
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
    "EXCLUDED": 446,
    "LIVE": 31,
    "MIXED": 64,
})
EXPECTED_COMBINED_SOURCE = Counter({
    "ROUND215_FULL_DELTA_NEGATIVE_SIDE": 60,
    "ROUND306C30A_CLIPPED_DELTA_RESIDUAL": 20,
})


class BootstrapFailure(RuntimeError):
    pass


def bootstrap_need(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise BootstrapFailure(label)


def bootstrap_file_hash(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(1 << 20):
            state.update(block)
    return state.hexdigest()


def race_checked_single_read(
    path: Path, label: str
) -> tuple[bytes, tuple[int, int, int, int, int, int, int]]:
    """Read one regular singleton once, detecting replacement during read."""
    absolute = Path(os.path.abspath(os.fspath(path)))
    bootstrap_need(
        absolute.resolve(strict=True) == absolute
        and absolute.is_relative_to(ROOT.resolve(strict=True)),
        "race-checked path containment:" + label,
    )
    flags = os.O_RDONLY | os.O_CLOEXEC | getattr(os, "O_NOFOLLOW", 0)
    descriptor = os.open(absolute, flags)
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
    bootstrap_need(
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
    bootstrap_need(len(raw) == before.st_size, "race-checked byte count:" + label)
    return raw, identity


def require_capture_still_current(
    path: Path,
    identity: tuple[int, int, int, int, int, int, int],
    label: str,
) -> None:
    status = path.lstat()
    bootstrap_need(
        identity == (
            status.st_dev, status.st_ino, status.st_mode, status.st_nlink,
            status.st_size, status.st_mtime_ns, status.st_ctime_ns,
        ) and stat.S_ISREG(status.st_mode) and not path.is_symlink(),
        "captured path identity changed:" + label,
    )


C30B_SOURCE_CAPTURE: tuple[
    bytes, tuple[int, int, int, int, int, int, int]
] | None = None


def import_pinned_c30b() -> Any:
    """Execute exactly the once-read C30b bytes; never reopen for import."""
    global C30B_SOURCE_CAPTURE
    path = ROOT / C30B_SOURCE
    raw, identity = race_checked_single_read(path, C30B_SOURCE)
    bootstrap_need(
        hashlib.sha256(raw).hexdigest() == C30B_SOURCE_SHA256,
        "pinned C30b producer source",
    )
    module_name = C30B_SOURCE[:-3]
    bootstrap_need(module_name not in sys.modules, "C30b not preloaded")
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
    C30B_SOURCE_CAPTURE = (raw, identity)
    require_capture_still_current(path, identity, C30B_SOURCE)
    bootstrap_need(
        Path(module.__file__).resolve(strict=True) == path.resolve(strict=True)
        and hashlib.sha256(raw).hexdigest() == C30B_SOURCE_SHA256,
        "imported C30b module identity",
    )
    return module


c30b = import_pinned_c30b()
need = c30b.need
canonical = c30b.canonical
digest = c30b.digest
file_hash = c30b.file_hash
strict_json = c30b.strict_json
gzip_rows = c30b.gzip_rows
sealed_row = c30b.sealed_row
fraction = c30b.fraction
r176 = c30b.r176
r180 = c30b.r180
r215 = c30b.r215
c30a = c30b.c30a
ctx = c30b.ctx


def validate_runtime_and_imports() -> None:
    c30b.validate_runtime()
    c30b.validate_imported_mathematics()
    bootstrap_need(C30B_SOURCE_CAPTURE is not None, "C30b source capture exists")
    assert C30B_SOURCE_CAPTURE is not None
    source_raw, source_identity = C30B_SOURCE_CAPTURE
    require_capture_still_current(ROOT / C30B_SOURCE, source_identity, C30B_SOURCE)
    need(
        sys.modules.get(C30B_SOURCE[:-3]) is c30b
        and Path(c30b.__file__).resolve(strict=True)
        == (ROOT / C30B_SOURCE).resolve(strict=True)
        and hashlib.sha256(source_raw).hexdigest() == C30B_SOURCE_SHA256,
        "C30b reuse identity/hash",
    )


def parse_c30b_manifest_bytes(raw: bytes) -> dict[str, str]:
    need(
        hashlib.sha256(raw).hexdigest() == C30B_MANIFEST_SHA256,
        "C30b sealed manifest hash",
    )
    rows: dict[str, str] = {}
    try:
        lines = raw.decode("ascii").splitlines()
    except UnicodeDecodeError as error:
        raise BootstrapFailure("C30b sealed manifest ASCII") from error
    for line in lines:
        parts = line.split("  ", 1)
        need(
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
    need(
        rows == C30B_MANIFEST_MEMBER_PINS and len(rows) == 14,
        "C30b sealed manifest exact member set",
    )
    return rows


def validate_c30b_seal() -> dict[str, Any]:
    """Consume a single immutable byte capture of the fixed C30b seal."""
    sealed_dir = ROOT / C30B_SEALED_DIRNAME
    status_before = sealed_dir.lstat()
    directory_identity = (
        status_before.st_dev, status_before.st_ino, status_before.st_mode,
        status_before.st_nlink, status_before.st_mtime_ns,
        status_before.st_ctime_ns,
    )
    need(
        stat.S_ISDIR(status_before.st_mode)
        and not sealed_dir.is_symlink()
        and sealed_dir.resolve(strict=True)
        == Path(os.path.abspath(os.fspath(sealed_dir)))
        and sealed_dir.parent.resolve(strict=True) == ROOT.resolve(strict=True),
        "C30b sealed fixed directory authority",
    )
    need(
        {path.name for path in sealed_dir.iterdir()}
        == set(C30B_SEALED_FILE_PINS),
        "C30b sealed exact directory member set",
    )
    manifest_raw, _manifest_identity = race_checked_single_read(
        ROOT / C30B_MANIFEST, C30B_MANIFEST
    )
    manifest_rows = parse_c30b_manifest_bytes(manifest_raw)
    captured: dict[str, bytes] = {}
    for relative, expected in sorted(manifest_rows.items()):
        member = ROOT / relative
        if relative == C30B_SOURCE:
            bootstrap_need(C30B_SOURCE_CAPTURE is not None, "C30b import capture")
            assert C30B_SOURCE_CAPTURE is not None
            raw, identity = C30B_SOURCE_CAPTURE
            require_capture_still_current(member, identity, relative)
        else:
            raw, _identity = race_checked_single_read(member, relative)
        need(
            hashlib.sha256(raw).hexdigest() == expected,
            "C30b sealed member hash:" + relative,
        )
        captured[relative] = raw
    status_after = sealed_dir.lstat()
    need(
        directory_identity == (
            status_after.st_dev, status_after.st_ino, status_after.st_mode,
            status_after.st_nlink, status_after.st_mtime_ns,
            status_after.st_ctime_ns,
        )
        and {path.name for path in sealed_dir.iterdir()}
        == set(C30B_SEALED_FILE_PINS),
        "C30b sealed directory unchanged during capture",
    )
    verification_raw = captured[C30B_VERIFICATION]
    result_raw = captured[C30B_SEALED_DIRNAME + "/" + C30B_RESULT]
    verification = json.loads(verification_raw)
    need(type(verification) is dict, "C30b sealed verification JSON object")
    result = json.loads(result_raw)
    need(type(result) is dict, "C30b sealed result JSON object")
    result_body = {
        key: value for key, value in result.items() if key != "result_sha256"
    }
    need(
        hashlib.sha256(captured[C30B_SOURCE]).hexdigest() == C30B_SOURCE_SHA256
        and hashlib.sha256(captured[C30B_VERIFIER]).hexdigest()
        == C30B_VERIFIER_SHA256
        and hashlib.sha256(verification_raw).hexdigest()
        == C30B_VERIFICATION_SHA256
        and hashlib.sha256(result_raw).hexdigest() == C30B_RESULT_FILE_SHA256,
        "C30b sealed authority direct file hashes",
    )
    need(
        verification["status"]
        == ("PASS_FORMAL_C30B__688_H_CELLS__2_WHOLE_ORIGIN_EXCLUSIONS__"
            "10_RESOLVED_MIXED__SOURCE_W_92_TO_80__D02_STILL_BLOCKED")
        and verification["manifest"]["expected_member_count"] == 14
        and verification["published_outputs"]["result_object_sha256"]
        == C30B_RESULT_OBJECT_SHA256
        and verification["source_W_ledger_transition"]["after"]["remaining"] == 80
        and canonical(result) == result_raw
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
        },
        "C30b sealed verification/result 80-baseline handoff",
    )
    return {
        "manifest_sha256": C30B_MANIFEST_SHA256,
        "verification_sha256": C30B_VERIFICATION_SHA256,
        "producer_sha256": C30B_SOURCE_SHA256,
        "independent_verifier_sha256": C30B_VERIFIER_SHA256,
        "result_file_sha256": C30B_RESULT_FILE_SHA256,
        "result_object_sha256": C30B_RESULT_OBJECT_SHA256,
        "sealed_member_count": len(C30B_SEALED_FILE_PINS),
        "manifest_member_count": len(C30B_MANIFEST_MEMBER_PINS),
        "formal_source_W_remaining": 80,
    }


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


def h_at_p(row: Any, seam_id: str, p: Q) -> Any:
    return r176.seam_values(
        row.chart_id, fixed_p_box(row.box, p, p), seam_id
    )["H"]


def bracket_h_graph(row: Any, seam_id: str) -> dict[str, Any]:
    """Return a deterministic closed rational collar containing H=0."""
    left, right = row.box.p0, row.box.p1
    left_sign = r176.sign(h_at_p(row, seam_id, left))
    right_sign = r176.sign(h_at_p(row, seam_id, right))
    need(
        left_sign == 1 and right_sign == -1,
        "strict full H graph endpoint signs:" + row.key,
    )
    steps: list[dict[str, Any]] = []
    for ordinal in range(32):
        middle = (left + right) / 2
        middle_sign = r176.sign(h_at_p(row, seam_id, middle))
        if middle_sign == 0:
            steps.append(sealed_row({
                "schema": "cm2.round306c30c.H-bracket-step.v1",
                "ordinal": ordinal,
                "p_midpoint": fraction(middle),
                "H_midpoint_face_sign": "OVERWRAP",
                "update": "STOP_INTERVAL_OVERWRAP",
            }))
            break
        if middle_sign == left_sign:
            left = middle
            update = "REPLACE_LEFT_ENDPOINT"
        else:
            need(middle_sign == right_sign, "H bracket sign trichotomy")
            right = middle
            update = "REPLACE_RIGHT_ENDPOINT"
        steps.append(sealed_row({
            "schema": "cm2.round306c30c.H-bracket-step.v1",
            "ordinal": ordinal,
            "p_midpoint": fraction(middle),
            "H_midpoint_face_sign": (
                "STRICT_POSITIVE" if middle_sign > 0
                else "STRICT_NEGATIVE"
            ),
            "update": update,
        }))
    final_left = sign_name(h_at_p(row, seam_id, left))
    final_right = sign_name(h_at_p(row, seam_id, right))
    need(
        final_left == "STRICT_POSITIVE"
        and final_right == "STRICT_NEGATIVE"
        and left < right,
        "closed one-sided H bracket:" + row.key,
    )
    return {
        "method": "DETERMINISTIC_RATIONAL_BISECTION_UNTIL_INTERVAL_OVERWRAP",
        "maximum_steps": 32,
        "steps_executed": len(steps),
        "step_rows": steps,
        "step_rows_sha256": digest(steps),
        "p_bracket": [fraction(left), fraction(right)],
        "exact_width": fraction(right - left),
        "p_lower_H_sign": final_left,
        "p_upper_H_sign": final_right,
        "closed_t_s_base_unchanged": True,
        "unique_H_zero_graph_inside_bracket_by_strict_dH_dp": True,
    }


def delta_on_h_bracket(
    row: Any,
    target_id: str,
    bracket: dict[str, Any],
) -> dict[str, Any]:
    p0, p1 = (Q(value) for value in bracket["p_bracket"])
    collar = fixed_p_box(row.box, p0, p1)
    records = r176.records_for(row.chart_id, collar, (target_id,))
    need(len(records) == 1, "single target on H bracket")
    delta = records[0].discriminant
    need(bool(delta < 0), "Delta strictly negative on H bracket:" + row.key)
    return {
        "target": target_id,
        "closed_box": r176.box_row(collar),
        "Delta_interval_sign": sign_name(delta),
        "strict_on_entire_closed_t_s_p_bracket": True,
        "H_zero_subset_of_bracket": True,
        "conclusion": "H_ZERO_SHEET_SUBSET_OF_STRICT_DELTA_NEGATIVE_REGION",
        "Delta_zero_intersect_H_zero": "EMPTY",
        "restriction_to_every_owned_face_edge_vertex": True,
    }


def boundary_partition_rows(row: Any) -> list[dict[str, Any]]:
    """Enumerate the 6+12+8 outer strata and restrict the five predicates."""
    rows: list[dict[str, Any]] = []
    axes = ("t", "p", "s")
    predicate_template = [
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
            "predicate": (
                "Delta<0 AND " + MISMATCH_H_SIGN_BY_CHART[row.chart_id]
            ),
            "disposition": "EXCLUDED_OUTGOING_CHART_MISMATCH",
            "equality_owner": "NOT_APPLICABLE_OPEN_STRATUM",
        },
    ]
    for fixed_count in (1, 2, 3):
        for fixed_axes in itertools.combinations(axes, fixed_count):
            for sides in itertools.product(("LOWER", "UPPER"), repeat=fixed_count):
                fixed = dict(zip(fixed_axes, sides, strict=True))
                ambient_dimension = 3 - fixed_count
                rows.append(sealed_row({
                    "schema": "cm2.round306c30c.outer-boundary-restriction.v1",
                    "cell_key": row.key,
                    "fixed_coordinates": fixed,
                    "ambient_dimension": ambient_dimension,
                    "restricted_predicate_partition": predicate_template,
                    "restricted_predicate_partition_sha256": digest(
                        predicate_template
                    ),
                    "Delta_zero_AND_H_zero": "EMPTY_BY_CLOSED_H_BRACKET_DELTA_NEGATIVE",
                    "pointwise_disjoint": True,
                    "pointwise_exhaustive": True,
                    "strict_and_equality_predicates_restrict_continuously": True,
                    "dyadic_half_open_owner": (
                        "BOUND_BY_WHOLE_ORIGIN_ATOMIC_OWNER_AUDIT"
                    ),
                    "analytic_equality_owner_applied_after_dyadic_owner": True,
                }))
    need(len(rows) == 26, "six faces twelve edges eight vertices")
    return rows


def combined_delta_h_body(
    ordinal: int,
    row: Any,
    reduction: dict[str, Any],
    evidence: dict[str, Any],
    c30a_row: dict[str, Any] | None,
) -> dict[str, Any]:
    records, centered_rows = r215.enhance_root_sign_records(
        row, reduction["current_records"]
    )
    unresolved = [
        record for record in records
        if record.classification == "unresolved_discriminant"
    ]
    need(len(unresolved) == 1, "one full/clipped Delta:" + row.key)
    candidate = unresolved[0]
    target_id = TARGET_BY_ORIGIN[row.origin_key]
    derivative, lower, upper, full = r176.graph_faces(row, candidate)
    expected_derivative = 1 if row.chart_id == "W:N" else -1
    need(
        candidate.target_id == target_id
        and derivative == expected_derivative
        and r176.target_positive_first(candidate, records)
        and evidence["target_strict_positive_first"] is True,
        "full-Delta frozen target/monotonicity:" + row.key,
    )
    blocker = evidence["blocker"]
    if blocker == "SINGLE_FULL_DELTA_NEGATIVE_SIDE_NOT_EXCLUDED":
        source_kind = "ROUND215_FULL_DELTA_NEGATIVE_SIDE"
        need(full is True and c30a_row is None, "full Delta source binding")
    else:
        source_kind = "ROUND306C30A_CLIPPED_DELTA_RESIDUAL"
        need(
            blocker == "SINGLE_CLIPPED_DELTA_ENDPOINT_OVERWRAP"
            and full is False
            and c30a_row is not None
            and c30a_row["disposition"]
            == "RESIDUAL_NEGATIVE_OPEN_SIDE_NOT_EXCLUDED"
            and c30a_row["whole_closed_cell_excluded"] is False,
            "C30a clipped residual binding:" + row.key,
        )

    without_candidate = [
        record for record in records if record.target_id != target_id
    ]
    negative_leaf = r176.classify_records(
        row.chart_id, row.box, without_candidate
    )
    need(
        negative_leaf.classification == "unique_first"
        and negative_leaf.owner_target == r176.FROZEN_OWNER,
        "Delta-negative W unique first:" + row.key,
    )
    seam_id = SEAM_BY_CHART[row.chart_id]
    seam = c30b.seam_candidate(row.chart_id, row.box, seam_id)
    need(
        seam["typed_preconditions"] is True
        and seam["full_graph"] is True
        and seam["dH_dp_sign"] == "STRICT_NEGATIVE",
        "full typed H graph:" + row.key,
    )
    bracket = bracket_h_graph(row, seam_id)
    delta_collar = delta_on_h_bracket(row, target_id, bracket)
    typed_h = c30b.typed_sheet_materialization(
        row.chart_id, row.box, seam, row.key + "#FULL_DELTA_H"
    )
    boundary_rows = boundary_partition_rows(row)
    strata = [
        sealed_row({
            "schema": "cm2.round306c30c.combined-predicate-stratum.v1",
            "cell_key": row.key,
            "predicate": "Delta>0",
            "ambient_dimension": 3,
            "nonemptiness": (
                "NONEMPTY_ON_EVERY_BASE_FIBRE" if full
                else "NOT_REQUIRED_FOR_COMPLETE_DISPOSITION"
            ),
            "disposition": "EXCLUDED_UNIQUE_FIRST_G_OWNER_MISMATCH",
            "owner": target_id,
        }),
        sealed_row({
            "schema": "cm2.round306c30c.combined-predicate-stratum.v1",
            "cell_key": row.key,
            "predicate": "Delta=0",
            "ambient_dimension": 2,
            "nonemptiness": (
                "NONEMPTY_FULL_MONOTONE_GRAPH" if full
                else "NOT_REQUIRED_FOR_COMPLETE_DISPOSITION"
            ),
            "disposition": "EXCLUDED_UNIQUE_FIRST_G_TANGENCY_OWNER_MISMATCH",
            "owner": target_id,
        }),
        sealed_row({
            "schema": "cm2.round306c30c.combined-predicate-stratum.v1",
            "cell_key": row.key,
            "predicate": "Delta<0 AND " + LIVE_H_SIGN_BY_CHART[row.chart_id],
            "ambient_dimension": 3,
            "nonemptiness": "STRICT_POSITIVE_MEASURE_BY_H_BRACKET_FACE_AND_CONTINUITY",
            "disposition": "LIVE_W_STAGE_ONE_OWNER_CHART_MATCH",
            "owner": r176.FROZEN_OWNER,
        }),
        sealed_row({
            "schema": "cm2.round306c30c.combined-predicate-stratum.v1",
            "cell_key": row.key,
            "predicate": "Delta<0 AND H=0",
            "ambient_dimension": 2,
            "nonemptiness": "NONEMPTY_UNIQUE_FULL_H_GRAPH",
            "disposition": "LIVE_W_HALF_OPEN_SEAM_OWNER",
            "owner": "W",
        }),
        sealed_row({
            "schema": "cm2.round306c30c.combined-predicate-stratum.v1",
            "cell_key": row.key,
            "predicate": (
                "Delta<0 AND " + MISMATCH_H_SIGN_BY_CHART[row.chart_id]
            ),
            "ambient_dimension": 3,
            "nonemptiness": "STRICT_POSITIVE_MEASURE_BY_H_BRACKET_FACE_AND_CONTINUITY",
            "disposition": "EXCLUDED_OUTGOING_CHART_MISMATCH",
            "owner": "N" if row.chart_id == "W:N" else "S",
        }),
    ]
    delta_h_intersection = {
        "predicate": "Delta=0 AND H=0",
        "nominal_dimension_if_nonempty": 1,
        "status": "EMPTY_CERTIFIED",
        "certificate": "DELTA_STRICT_NEGATIVE_ON_CLOSED_H_BRACKET",
        "all_outer_face_edge_vertex_restrictions_empty": True,
        "integer_credit": 0,
    }
    graph_order = (
        "H_GRAPH_STRICTLY_BELOW_DELTA_GRAPH_WHERE_DELTA_GRAPH_EXISTS"
        if row.chart_id == "W:N" else
        "DELTA_GRAPH_STRICTLY_BELOW_H_GRAPH_WHERE_DELTA_GRAPH_EXISTS"
    )
    body = {
        "schema": "cm2.round306c30c.source-w-full-delta-h.cell-row.v1",
        "cell_ordinal": ordinal,
        "cell_key": row.key,
        "origin_key": row.origin_key,
        "source_chart_id": row.chart_id,
        "closed_box": r176.box_row(row.box),
        "exact_volume": fraction(r215.box_volume(row.box)),
        "active_targets": list(row.active_targets),
        "source_kind": source_kind,
        "upstream_binding": {
            "Round215_evidence": evidence,
            "Round215_evidence_sha256": digest(evidence),
            "Round215_reduction_sha256": digest(
                c30b.reduction_binding(reduction)
            ),
            "C30a_cell_row_sha256": (
                c30a_row["row_sha256"] if c30a_row is not None
                else "NOT_APPLICABLE_FULL_DELTA"
            ),
        },
        "centered_root_sign_evidence": centered_rows,
        "candidate_target": target_id,
        "candidate_is_frozen_owner": False,
        "target_strict_positive_first": True,
        "Delta_p_derivative_sign": (
            "STRICT_POSITIVE" if derivative > 0 else "STRICT_NEGATIVE"
        ),
        "Delta_p_lower_face_sign": sign_name(lower),
        "Delta_p_upper_face_sign": sign_name(upper),
        "full_p_monotone_Delta_graph": full,
        "Delta_negative_leaf": {
            "classification": negative_leaf.classification,
            "unique_first_owner": negative_leaf.owner_target,
            "outgoing_disposition_requires_H_partition": True,
        },
        "H_seam_evidence": seam,
        "H_graph_bracket": bracket,
        "Delta_on_H_graph_bracket": delta_collar,
        "strict_graph_order": graph_order,
        "Delta_H_intersection": delta_h_intersection,
        "typed_H_geometry": {
            "use_scope": "GEOMETRY_AND_INCIDENCE_ONLY_UNTIL_RESTRICTED_BY_DELTA_NEGATIVE",
            "standalone_H_side_disposition_credit": 0,
            "open_3D_sides": typed_h["open_3D_sides"],
            "H_zero_2D_sheet": typed_h["H_zero_2D_sheet"],
            "H_zero_1D_face_incidences": typed_h[
                "H_zero_1D_face_incidences"
            ],
            "terminal_face_2D_H_sign_regions": typed_h[
                "terminal_face_2D_H_sign_regions"
            ],
            "H_zero_0D_edge_incidences": typed_h[
                "H_zero_0D_edge_incidences"
            ],
            "terminal_edge_1D_H_sign_intervals": typed_h[
                "terminal_edge_1D_H_sign_intervals"
            ],
            "H_zero_0D_corner_absence_rows": typed_h[
                "H_zero_0D_corner_absence_rows"
            ],
        },
        "combined_strata": strata,
        "combined_strata_sha256": digest(strata),
        "outer_boundary_restriction_rows": boundary_rows,
        "outer_boundary_restriction_rows_sha256": digest(boundary_rows),
        "partition_theorem": {
            "five_predicate_strata_pointwise_disjoint": True,
            "five_predicate_strata_pointwise_exhaustive": True,
            "Delta_zero_H_zero_intersection_empty": True,
            "all_3D_2D_1D_0D_outer_restrictions_disposed": True,
            "dyadic_half_open_owner_deferred_to_origin_atomic_audit": True,
            "H_zero_half_open_owner": "W",
            "whole_closed_cell_disposition": "MIXED",
        },
        "whole_closed_cell_disposition": "MIXED",
        "positive_measure_LIVE_open_side_proved": True,
        "positive_measure_EXCLUDED_open_side_proved": True,
        "candidate_credit": {
            "combined_Delta_H_cell_disposition": 1,
            "resolved_source_W_origin_disposition": 0,
            "whole_source_W_origin_exclusion": 0,
        },
        "formal_credit": {
            "combined_Delta_H_cell_disposition": 0,
            "resolved_source_W_origin_disposition": 0,
            "whole_source_W_origin_exclusion": 0,
        },
        "strict_nonpromotion": "AWAIT_INDEPENDENT_VERIFIER_AND_SEALED_MANIFEST",
    }
    return body


def collect_frozen_inputs() -> tuple[
    dict[str, dict[str, Any]],
    dict[str, dict[str, Any]],
    dict[str, dict[str, Any]],
]:
    r184 = strict_json(ROOT / c30b.R184_CERTIFICATE)
    registry = {
        row["origin_key"]: row
        for row in r184["result"]["priority_registry"]["rows"]
        if row["origin_key"] in set(ORIGIN_KEYS)
    }
    bounded = strict_json(ROOT / c30b.R215_CERTIFICATE)["result"][
        "bounded_probe_result"
    ]
    summaries = {
        row["origin_key"]: row
        for row in bounded["whole_origin_outcome"]["per_origin_rows"]
        if row["origin_key"] in set(ORIGIN_KEYS)
    }
    c30a_result = strict_json(ROOT / c30b.C30A_RESULT)
    all_c30a_rows = gzip_rows(
        ROOT / c30b.C30A_CELL_LEDGER,
        c30a_result["ledgers"]["reduced_clipped_cell"],
    )
    c30a_rows = {
        row["cell_key"]: row
        for row in all_c30a_rows
        if row["origin_key"] in set(ORIGIN_KEYS)
    }
    need(
        set(registry) == set(ORIGIN_KEYS)
        and set(summaries) == set(ORIGIN_KEYS)
        and [registry[key]["priority_ordinal"] for key in ORIGIN_KEYS]
        == [1234, 1235]
        and all(
            summary["Round201_residual_cell_count"] == 50
            and summary["Round215_analytic_closed_cell_count"] == 0
            and summary["Round215_blocker_count"] == {
                "SINGLE_CLIPPED_DELTA_ENDPOINT_OVERWRAP": 20,
                "SINGLE_FULL_DELTA_NEGATIVE_SIDE_NOT_EXCLUDED": 30,
            }
            for summary in summaries.values()
        )
        and len(c30a_rows) == 40
        and Counter(row["origin_key"] for row in c30a_rows.values())
        == Counter({key: 20 for key in ORIGIN_KEYS})
        and all(
            Counter(
                row["disposition"]
                for row in c30a_rows.values()
                if row["origin_key"] == origin
            ) == Counter({
                "CLOSED_REDUCED_CANDIDATE_OWNER_MISMATCH": 10,
                "RESIDUAL_NEGATIVE_OPEN_SIDE_NOT_EXCLUDED": 10,
            })
            for origin in ORIGIN_KEYS
        ),
        "frozen two-origin C30c selection/input census",
    )
    return registry, summaries, c30a_rows


def inherited_h_rows(
    origin: str,
    refinement: dict[str, Any],
    leaves: dict[str, Any],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    output: list[dict[str, Any]] = []
    direct_live: list[dict[str, Any]] = []
    for evidence in sorted(
        refinement["terminal_rows"], key=lambda value: value["cell_key"]
    ):
        if evidence["coarse_disposition"] == "EXCLUDED":
            continue
        frontier = leaves["terminal"][evidence["cell_key"]]
        if evidence["method"] == "DIRECT_STRICT_CLOSED_BOX":
            need(
                evidence["coarse_disposition"] == "LIVE",
                "direct inherited nonexcluded must be LIVE",
            )
            direct_live.append(evidence)
            continue
        if evidence["method"] == "OUTGOING_H_CLOSED_RECTANGLE_TREE":
            source_kind, binding = c30b.inherited_source_binding(
                evidence, None
            )
        else:
            need(
                evidence["method"] == "SAME_SIGN_MONOTONE_DELTA_CLOSED_BOX"
                and evidence["coarse_disposition"] == "MIXED",
                "inherited same-sign Delta/H followup",
            )
            source_kind = "ROUND180_INHERITED_SAME_SIGN_DELTA_FOLLOWUP_H"
            binding = c30b.inherited_same_sign_delta_followup_h_binding(
                evidence
            )
        body = c30b.h_cell_body(source_kind, frontier, binding)
        body["schema"] = "cm2.round306c30c.inherited-h-cell.row.v1"
        body["formal_credit"] = {
            "inherited_H_cell_disposition": 0,
            "whole_source_W_origin_exclusion": 0,
        }
        body["candidate_reuse_of_C30b_H_theorem"] = True
        body["strict_nonpromotion"] = (
            "C30B_HELPER_REUSE_DOES_NOT_IMPORT_C30B_RESULT_CREDIT"
        )
        output.append(sealed_row(body))
    output.sort(key=lambda value: value["cell_key"])
    need(
        len(output) == EXPECTED_PER_ORIGIN["Round180_inherited_H"]
        and len(direct_live)
        == EXPECTED_PER_ORIGIN["Round180_inherited_direct_live"],
        "inherited H/direct LIVE census:" + origin,
    )
    return output, direct_live


def typed_boundary_support(
    combined: dict[str, Any], signature: dict[str, str]
) -> dict[str, Any]:
    """Bind one relative cell stratum to its complete analytic H support."""
    typed = combined["typed_H_geometry"]
    codimension = len(signature)
    if codimension == 0:
        rows = typed["open_3D_sides"] + [typed["H_zero_2D_sheet"]]
        need(len(rows) == 3, "interior five-strata analytic support")
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
        need(len(rows) == 3 and len(boundary) == 1, "face analytic support")
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
        need(len(rows) == 3 and len(boundary) == 1, "edge analytic support")
        binding_kind = "COMBINED_OUTER_BOUNDARY_RESTRICTION"
        analytic_sha256 = boundary[0]["row_sha256"]
    else:
        need(codimension == 3, "relative boundary codimension")
        rows = [
            row for row in typed["H_zero_0D_corner_absence_rows"]
            if row["corner"] == signature
        ]
        boundary = [
            row for row in combined["outer_boundary_restriction_rows"]
            if row["fixed_coordinates"] == signature
        ]
        need(len(rows) == 1 and len(boundary) == 1, "corner analytic support")
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


def materialize_full_atomic_owner_ledger(
    leaf_rows: dict[str, Any],
    proof_source: dict[str, str],
    leaf_disposition: dict[str, str],
) -> dict[str, Any]:
    """Materialize the complete 2D/1D/0D owner complex from leaf faces."""
    axes = ("t", "p", "s")
    bounds = {
        key: {
            "t": (row.box.t0, row.box.t1),
            "p": (row.box.p0, row.box.p1),
            "s": (row.box.s0, row.box.s1),
        }
        for key, row in leaf_rows.items()
    }
    grid = {
        axis: sorted({value for box in bounds.values() for value in box[axis]})
        for axis in axes
    }
    origin_key = next(iter(leaf_rows.values())).origin_key

    def geometry_parts(
        geometry: dict[str, Any]
    ) -> tuple[dict[str, Q], dict[str, tuple[Q, Q]]]:
        return (
            {axis: Q(value) for axis, value in geometry["fixed"].items()},
            {
                axis: (Q(values[0]), Q(values[1]))
                for axis, values in geometry["open_spans"].items()
            },
        )

    def closure_contains(
        box: dict[str, tuple[Q, Q]],
        fixed: dict[str, Q],
        spans: dict[str, tuple[Q, Q]],
    ) -> bool:
        return all(
            box[axis][0] <= value <= box[axis][1]
            for axis, value in fixed.items()
        ) and all(
            box[axis][0] <= lower < upper <= box[axis][1]
            for axis, (lower, upper) in spans.items()
        )

    def owner_row(
        dimension: int,
        geometry: dict[str, Any],
        incident_sources: list[str],
    ) -> dict[str, Any]:
        fixed, spans = geometry_parts(geometry)
        midpoints = {
            axis: (lower + upper) / 2
            for axis, (lower, upper) in spans.items()
        }
        containing = sorted(
            key for key, box in bounds.items()
            if closure_contains(box, fixed, spans)
            and all(
                box[axis][0] < value < box[axis][1]
                for axis, value in midpoints.items()
            )
        )
        need(bool(containing), "full atomic owner exists")
        owner = containing[0]
        incidences: list[dict[str, Any]] = []
        for key in containing:
            signature: dict[str, str] = {}
            for axis, value in sorted(fixed.items()):
                if value == bounds[key][axis][0]:
                    signature[axis] = "LOWER"
                elif value == bounds[key][axis][1]:
                    signature[axis] = "UPPER"
            incidences.append(sealed_row({
                "schema": (
                    "cm2.round306c30c.full-atomic-leaf-incidence.row.v1"
                ),
                "leaf_key": key,
                "relative_boundary_signature": signature,
                "relative_boundary_codimension": len(signature),
                "selected_by_half_open_owner": key == owner,
                "proof_source": proof_source[key],
                "leaf_disposition": leaf_disposition[key],
            }))
        measure = Q(1)
        for lower, upper in spans.values():
            measure *= upper - lower
        return sealed_row({
            "schema": "cm2.round306c30c.full-atomic-owner.row.v1",
            "origin_key": origin_key,
            "ambient_dimension": dimension,
            "geometry": geometry,
            "exact_measure": fraction(measure),
            "incident_sources": sorted(set(incident_sources)),
            "incident_source_count": len(set(incident_sources)),
            "closed_containing_leaf_keys": containing,
            "closed_incident_leaf_rows": incidences,
            "closed_incident_leaf_rows_sha256": digest(incidences),
            "half_open_owner_leaf_key": owner,
            "owner_selection_rule": (
                "DETERMINISTIC_LEAF_KEY_LEXICOGRAPHIC_MIN_CONTAINING_LEAF"
            ),
            "owner_proof_source": proof_source[owner],
            "owner_disposition": leaf_disposition[owner],
        })

    face_groups: dict[str, dict[str, Any]] = {}
    for leaf_key, box in sorted(bounds.items()):
        for fixed_axis in axes:
            free_axes = [axis for axis in axes if axis != fixed_axis]
            for side, coordinate in (
                ("LOWER", box[fixed_axis][0]),
                ("UPPER", box[fixed_axis][1]),
            ):
                interval_lists: list[list[tuple[Q, Q]]] = []
                for axis in free_axes:
                    values = [value for value in grid[axis]
                              if box[axis][0] <= value <= box[axis][1]]
                    interval_lists.append(list(zip(values, values[1:])))
                for product in itertools.product(*interval_lists):
                    geometry = {
                        "fixed": {fixed_axis: fraction(coordinate)},
                        "open_spans": {
                            axis: [fraction(span[0]), fraction(span[1])]
                            for axis, span in zip(
                                free_axes, product, strict=True
                            )
                        },
                    }
                    key = canonical(geometry).decode("ascii")
                    group = face_groups.setdefault(key, {
                        "geometry": geometry, "sources": [],
                    })
                    group["sources"].append(
                        "LEAF_FACE:" + leaf_key + ":" + fixed_axis + ":" + side
                    )
    face_rows = [
        owner_row(2, group["geometry"], group["sources"])
        for _key, group in sorted(face_groups.items())
    ]

    line_groups: dict[str, dict[str, Any]] = {}
    for face in face_rows:
        fixed, spans = geometry_parts(face["geometry"])
        for boundary_axis in sorted(spans):
            remaining_axis = next(
                axis for axis in spans if axis != boundary_axis
            )
            for side, endpoint in (
                ("LOWER", spans[boundary_axis][0]),
                ("UPPER", spans[boundary_axis][1]),
            ):
                geometry = {
                    "fixed": {
                        axis: fraction(value)
                        for axis, value in sorted({
                            **fixed, boundary_axis: endpoint,
                        }.items())
                    },
                    "open_spans": {
                        remaining_axis: [
                            fraction(spans[remaining_axis][0]),
                            fraction(spans[remaining_axis][1]),
                        ]
                    },
                }
                key = canonical(geometry).decode("ascii")
                group = line_groups.setdefault(key, {
                    "geometry": geometry, "sources": [],
                })
                group["sources"].append(
                    "ATOMIC_2D:" + face["row_sha256"] + ":"
                    + boundary_axis + ":" + side
                )
    line_rows = [
        owner_row(1, group["geometry"], group["sources"])
        for _key, group in sorted(line_groups.items())
    ]

    point_groups: dict[str, dict[str, Any]] = {}
    for line in line_rows:
        fixed, spans = geometry_parts(line["geometry"])
        free_axis, span = next(iter(spans.items()))
        for side, endpoint in (("LOWER", span[0]), ("UPPER", span[1])):
            geometry = {
                "fixed": {
                    axis: fraction(value)
                    for axis, value in sorted({**fixed, free_axis: endpoint}.items())
                },
                "open_spans": {},
            }
            key = canonical(geometry).decode("ascii")
            group = point_groups.setdefault(key, {
                "geometry": geometry, "sources": [],
            })
            group["sources"].append(
                "ATOMIC_1D:" + line["row_sha256"] + ":" + side
            )
    point_rows = [
        owner_row(0, group["geometry"], group["sources"])
        for _key, group in sorted(point_groups.items())
    ]
    all_rows = face_rows + line_rows + point_rows
    need(bool(face_rows) and bool(line_rows) and bool(point_rows),
         "nonempty full atomic owner ledger")
    return {
        "schema": "cm2.round306c30c.full-atomic-owner-ledger.v1",
        "origin_key": origin_key,
        "construction_contract": "FULL_AXIS_ALIGNED_CELL_COMPLEX",
        "closed_leaf_count": len(leaf_rows),
        "axis_grid_coordinates_sha256": digest({
            axis: [fraction(value) for value in values]
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


def materialize_full_atomic_owner_audit(
    original_parent: Any,
    leaf_rows: dict[str, Any],
    proof_source: dict[str, str],
    leaf_disposition: dict[str, str],
    *,
    audit_scope: str = "WHOLE_ORIGIN_LINEAGE",
    leaf_key_kind: str = "CELL_KEY",
) -> dict[str, Any]:
    """Emit only independently reconstructible owner authority for C30c."""
    axes = ("t", "p", "s")
    bounds = {
        key: {
            "t": (row.box.t0, row.box.t1),
            "p": (row.box.p0, row.box.p1),
            "s": (row.box.s0, row.box.s1),
        }
        for key, row in leaf_rows.items()
    }
    parent = {
        "t": (original_parent.t0, original_parent.t1),
        "p": (original_parent.p0, original_parent.p1),
        "s": (original_parent.s0, original_parent.s1),
    }
    contained = all(
        all(
            parent[axis][0] <= box[axis][0] < box[axis][1]
            <= parent[axis][1]
            for axis in axes
        )
        for box in bounds.values()
    )
    leaf_volume = sum((
        (box["t"][1] - box["t"][0])
        * (box["p"][1] - box["p"][0])
        * (box["s"][1] - box["s"][0])
        for box in bounds.values()
    ), Q(0))
    parent_volume = (
        (original_parent.t1 - original_parent.t0)
        * (original_parent.p1 - original_parent.p0)
        * (original_parent.s1 - original_parent.s0)
    )
    ordered = sorted(bounds)
    pair_rows: list[dict[str, Any]] = []
    for first_ordinal, first_key in enumerate(ordered):
        for second_key in ordered[first_ordinal + 1:]:
            overlap = all(
                max(bounds[first_key][axis][0], bounds[second_key][axis][0])
                < min(bounds[first_key][axis][1], bounds[second_key][axis][1])
                for axis in axes
            )
            pair_rows.append({
                "first": first_key,
                "second": second_key,
                "interior_overlap": overlap,
            })
    need(
        contained
        and not any(row["interior_overlap"] for row in pair_rows)
        and leaf_volume == parent_volume
        and len(pair_rows) == len(leaf_rows) * (len(leaf_rows) - 1) // 2,
        "C30c exact full atomic owner 3D enclosure",
    )
    ledger = materialize_full_atomic_owner_ledger(
        leaf_rows, proof_source, leaf_disposition
    )
    grid = {
        axis: sorted({value for box in bounds.values() for value in box[axis]})
        for axis in axes
    }
    return {
        "schema": "cm2.round306c30c.exact-full-atomic-owner-audit.v1",
        "audit_scope": audit_scope,
        "leaf_key_kind": leaf_key_kind,
        "exact_3D_enclosure": {
            "all_leaf_boxes_contained_in_parent_and_nondegenerate": contained,
            "pairwise_leaf_interiors_disjoint": True,
            "tested_unordered_leaf_pair_count": len(pair_rows),
            "tested_leaf_pair_rows_sha256": digest(pair_rows),
            "leaf_exact_volume_sum": fraction(leaf_volume),
            "parent_exact_volume": fraction(parent_volume),
            "leaf_exact_volume_sum_equals_parent": True,
        },
        "axis_grid_coordinate_count": {
            axis: len(values) for axis, values in grid.items()
        },
        "axis_grid_coordinates_sha256": digest({
            axis: [fraction(value) for value in values]
            for axis, values in grid.items()
        }),
        "atomic_owner_selection_rule": (
            "DETERMINISTIC_LEAF_KEY_LEXICOGRAPHIC_MIN_CONTAINING_LEAF"
        ),
        "closed_3D_leaf_count": len(leaf_rows),
        "closed_3D_leaf_keys_sha256": digest(sorted(leaf_rows)),
        "closed_3D_leaf_disposition_census": dict(sorted(Counter(
            leaf_disposition.values()
        ).items())),
        "C30c_full_atomic_owner_ledger": ledger,
        "C30c_full_atomic_owner_ledger_sha256": digest(ledger),
        "C30c_full_atomic_owner_rows_are_authoritative_for_join_membership": True,
        "sampled_evidence_used_for_uniform_conclusion": False,
    }


def inherited_h_relative_stratum_binding(
    h_row: dict[str, Any], geometry: dict[str, Any]
) -> dict[str, Any]:
    """Materialize open pieces and every internal terminal-cut equality."""
    axes = ("t", "p", "s")
    atom_fixed = {axis: Q(value) for axis, value in geometry["fixed"].items()}
    atom_spans = {
        axis: (Q(values[0]), Q(values[1]))
        for axis, values in geometry["open_spans"].items()
    }
    source_dimension = len(atom_spans)
    terminals = h_row["H_partition"]["terminal_rectangles"]
    terminal_by_id = {row["terminal_id"]: row for row in terminals}
    terminal_boxes = {
        terminal_id: {
            axis: (Q(row["closed_box"][axis][0]),
                   Q(row["closed_box"][axis][1]))
            for axis in axes
        }
        for terminal_id, row in terminal_by_id.items()
    }
    eligible_ids = sorted(
        terminal_id for terminal_id, box in terminal_boxes.items()
        if all(box[axis][0] <= value <= box[axis][1]
               for axis, value in atom_fixed.items())
        and all(max(lower, box[axis][0]) < min(upper, box[axis][1])
                for axis, (lower, upper) in atom_spans.items())
    )
    need(bool(eligible_ids), "relative inherited H incident terminals")
    span_axes = sorted(atom_spans)
    internal_cuts: dict[str, list[Q]] = {}
    mesh: dict[str, list[Q]] = {}
    for axis in span_axes:
        lower, upper = atom_spans[axis]
        internal_cuts[axis] = sorted({
            endpoint
            for terminal_id in eligible_ids
            for endpoint in terminal_boxes[terminal_id][axis]
            if lower < endpoint < upper
        })
        mesh[axis] = [lower] + internal_cuts[axis] + [upper]

    def terminal_binding(atomic_geometry: dict[str, Any]) -> dict[str, Any]:
        fixed = {
            axis: Q(value)
            for axis, value in atomic_geometry["fixed"].items()
        }
        spans = {
            axis: (Q(values[0]), Q(values[1]))
            for axis, values in atomic_geometry["open_spans"].items()
        }
        probes = {
            axis: (lower + upper) / 2
            for axis, (lower, upper) in spans.items()
        }
        containing = sorted(
            terminal_id for terminal_id in eligible_ids
            if all(
                terminal_boxes[terminal_id][axis][0] <= value
                <= terminal_boxes[terminal_id][axis][1]
                for axis, value in fixed.items()
            )
            and all(
                terminal_boxes[terminal_id][axis][0] <= lower < upper
                <= terminal_boxes[terminal_id][axis][1]
                and terminal_boxes[terminal_id][axis][0] < probes[axis]
                < terminal_boxes[terminal_id][axis][1]
                for axis, (lower, upper) in spans.items()
            )
        )
        need(bool(containing), "relative inherited H terminal owner")
        selected = terminal_by_id[containing[0]]
        selected_box = terminal_boxes[selected["terminal_id"]]
        relative: dict[str, str] = {}
        for axis, value in sorted(fixed.items()):
            if value == selected_box[axis][0]:
                relative[axis] = "LOWER"
            elif value == selected_box[axis][1]:
                relative[axis] = "UPPER"
        support_rows: list[dict[str, Any]] = []
        if selected["coarse_disposition"] == "MIXED":
            typed = selected["typed_strata"]
            codimension = len(relative)
            if codimension == 0:
                support_rows = typed["open_3D_sides"] + [
                    typed["H_zero_2D_sheet"]
                ]
            elif codimension == 1:
                axis, side = next(iter(sorted(relative.items())))
                support_rows = [
                    row for row in typed["H_zero_1D_face_incidences"]
                    if row["fixed_axis"] == axis
                    and row["boundary_side"] == side
                ] + [
                    row for row in typed["terminal_face_2D_H_sign_regions"]
                    if row["fixed_axis"] == axis
                    and row["boundary_side"] == side
                ]
            elif codimension == 2:
                support_rows = [
                    row for row in typed["H_zero_0D_edge_incidences"]
                    if row["fixed"] == relative
                ] + [
                    row for row in typed["terminal_edge_1D_H_sign_intervals"]
                    if row["fixed"] == relative
                ]
            else:
                need(codimension == 3, "relative inherited H codimension")
                support_rows = [
                    row for row in typed["H_zero_0D_corner_absence_rows"]
                    if row["corner"] == relative
                ]
            need(bool(support_rows), "relative inherited H stratum rows")
        dispositions: set[str] = set()
        for support in support_rows:
            if support.get("disposition") not in {None, "EMPTY"}:
                dispositions.add(support["disposition"])
            if support.get("strict_corner_disposition") is not None:
                dispositions.add(support["strict_corner_disposition"])
        if selected["coarse_disposition"] != "MIXED":
            dispositions.add(selected["coarse_disposition"])
        need(bool(dispositions), "relative inherited H pointwise disposition")
        measure = Q(1)
        for lower, upper in spans.values():
            measure *= upper - lower
        return {
            "exact_measure": fraction(measure),
            "closed_containing_terminal_ids": containing,
            "half_open_owner_terminal_id": selected["terminal_id"],
            "owner_terminal_row_sha256": selected["row_sha256"],
            "owner_terminal_coarse_disposition": selected[
                "coarse_disposition"
            ],
            "owner_terminal_analytic_evidence": selected["analytic_evidence"],
            "owner_terminal_analytic_evidence_sha256": digest(
                selected["analytic_evidence"]
            ),
            "relative_boundary_signature": relative,
            "relative_boundary_codimension": len(relative),
            "H_sign_sheet_stratum_rows": support_rows,
            "H_sign_sheet_stratum_rows_sha256": digest(support_rows),
            "pointwise_H_predicate_row_count": len(support_rows),
            "pointwise_disposition_set": sorted(dispositions),
            "H_equality_stratum_explicitly_bound": (
                selected["coarse_disposition"] != "MIXED"
                or any(
                    row.get("predicate") in {"H=0", "H=ux*dy-uy*dx=0"}
                    for row in support_rows
                )
            ),
            "H_sign_sheet_pointwise_exhaustive": True,
        }

    interval_lists = [
        list(zip(mesh[axis], mesh[axis][1:])) for axis in span_axes
    ]
    products = list(itertools.product(*interval_lists)) if span_axes else [()]
    piece_rows: list[dict[str, Any]] = []
    for piece_ordinal, product in enumerate(products):
        piece_geometry = {
            "fixed": {
                axis: fraction(value)
                for axis, value in sorted(atom_fixed.items())
            },
            "open_spans": {
                axis: [fraction(span[0]), fraction(span[1])]
                for axis, span in zip(span_axes, product, strict=True)
            },
        }
        piece_rows.append(sealed_row({
            "schema": "cm2.round306c30c.inherited-H-relative-atom.row.v2",
            "piece_ordinal": piece_ordinal,
            "piece_geometry": piece_geometry,
            **terminal_binding(piece_geometry),
        }))
    piece_rows.sort(key=lambda row: canonical(row["piece_geometry"]))
    for ordinal, row in enumerate(piece_rows):
        row["piece_ordinal"] = ordinal
        row.update(sealed_row({
            key: value for key, value in row.items() if key != "row_sha256"
        }))
    source_measure = Q(1)
    for lower, upper in atom_spans.values():
        source_measure *= upper - lower
    need(
        bool(piece_rows)
        and sum((Q(row["exact_measure"]) for row in piece_rows), Q(0))
        == source_measure,
        "relative inherited H terminal-piece exact reclosure",
    )

    line_groups: dict[str, dict[str, Any]] = {}
    point_groups: dict[str, dict[str, Any]] = {}
    expected_line_parent_incidences = 0
    if source_dimension == 2:
        for piece in piece_rows:
            fixed = {
                axis: Q(value)
                for axis, value in piece["piece_geometry"]["fixed"].items()
            }
            spans = {
                axis: (Q(values[0]), Q(values[1]))
                for axis, values in piece["piece_geometry"]["open_spans"].items()
            }
            for cut_axis in sorted(spans):
                remaining_axis = next(
                    axis for axis in spans if axis != cut_axis
                )
                for side, endpoint in (
                    ("LOWER", spans[cut_axis][0]),
                    ("UPPER", spans[cut_axis][1]),
                ):
                    if endpoint not in set(internal_cuts[cut_axis]):
                        continue
                    child = {
                        "fixed": {
                            axis: fraction(value)
                            for axis, value in sorted({
                                **fixed, cut_axis: endpoint,
                            }.items())
                        },
                        "open_spans": {
                            remaining_axis: [
                                fraction(spans[remaining_axis][0]),
                                fraction(spans[remaining_axis][1]),
                            ]
                        },
                    }
                    key = canonical(child).decode("ascii")
                    group = line_groups.setdefault(key, {
                        "geometry": child, "parents": [],
                    })
                    group["parents"].append(sealed_row({
                        "schema": (
                            "cm2.round306c30c.inherited-H-relative-"
                            "parent-incidence.row.v1"
                        ),
                        "parent_kind": "TERMINAL_OPEN_PIECE",
                        "parent_row_sha256": piece["row_sha256"],
                        "parent_ordinal": piece["piece_ordinal"],
                        "boundary_axis": cut_axis,
                        "boundary_side": side,
                    }))
                    expected_line_parent_incidences += 1
    line_rows: list[dict[str, Any]] = []
    for ordinal, (_key, group) in enumerate(sorted(line_groups.items())):
        parents = sorted(group["parents"], key=canonical)
        line_rows.append(sealed_row({
            "schema": (
                "cm2.round306c30c.inherited-H-relative-"
                "internal-cut-equality.row.v1"
            ),
            "cut_ordinal": ordinal,
            "source_atom_dimension": source_dimension,
            "ambient_dimension": 1,
            "geometry": group["geometry"],
            "relative_cut_codimension": source_dimension - 1,
            "contains_internal_terminal_cut_equality": True,
            "parent_piece_incidences": parents,
            "parent_piece_incidence_count": len(parents),
            "parent_piece_incidences_sha256": digest(parents),
            **terminal_binding(group["geometry"]),
        }))

    expected_point_parent_incidences = 0
    if source_dimension == 2:
        for line in line_rows:
            fixed = {
                axis: Q(value)
                for axis, value in line["geometry"]["fixed"].items()
            }
            free_axis, values = next(iter(line["geometry"]["open_spans"].items()))
            span = (Q(values[0]), Q(values[1]))
            for side, endpoint in (("LOWER", span[0]), ("UPPER", span[1])):
                if endpoint not in set(internal_cuts[free_axis]):
                    continue
                child = {
                    "fixed": {
                        axis: fraction(value)
                        for axis, value in sorted({
                            **fixed, free_axis: endpoint,
                        }.items())
                    },
                    "open_spans": {},
                }
                key = canonical(child).decode("ascii")
                group = point_groups.setdefault(key, {
                    "geometry": child, "parents": [],
                })
                group["parents"].append(sealed_row({
                    "schema": (
                        "cm2.round306c30c.inherited-H-relative-"
                        "parent-incidence.row.v1"
                    ),
                    "parent_kind": "RECURSIVE_1D_INTERNAL_CUT",
                    "parent_row_sha256": line["row_sha256"],
                    "parent_ordinal": line["cut_ordinal"],
                    "boundary_axis": free_axis,
                    "boundary_side": side,
                }))
                expected_point_parent_incidences += 1
    elif source_dimension == 1:
        for piece in piece_rows:
            fixed = {
                axis: Q(value)
                for axis, value in piece["piece_geometry"]["fixed"].items()
            }
            free_axis, values = next(iter(
                piece["piece_geometry"]["open_spans"].items()
            ))
            span = (Q(values[0]), Q(values[1]))
            for side, endpoint in (("LOWER", span[0]), ("UPPER", span[1])):
                if endpoint not in set(internal_cuts[free_axis]):
                    continue
                child = {
                    "fixed": {
                        axis: fraction(value)
                        for axis, value in sorted({
                            **fixed, free_axis: endpoint,
                        }.items())
                    },
                    "open_spans": {},
                }
                key = canonical(child).decode("ascii")
                group = point_groups.setdefault(key, {
                    "geometry": child, "parents": [],
                })
                group["parents"].append(sealed_row({
                    "schema": (
                        "cm2.round306c30c.inherited-H-relative-"
                        "parent-incidence.row.v1"
                    ),
                    "parent_kind": "TERMINAL_OPEN_PIECE",
                    "parent_row_sha256": piece["row_sha256"],
                    "parent_ordinal": piece["piece_ordinal"],
                    "boundary_axis": free_axis,
                    "boundary_side": side,
                }))
                expected_point_parent_incidences += 1
    point_rows: list[dict[str, Any]] = []
    for ordinal, (_key, group) in enumerate(sorted(point_groups.items())):
        parents = sorted(group["parents"], key=canonical)
        point_rows.append(sealed_row({
            "schema": (
                "cm2.round306c30c.inherited-H-relative-"
                "internal-cut-equality.row.v1"
            ),
            "cut_ordinal": ordinal,
            "source_atom_dimension": source_dimension,
            "ambient_dimension": 0,
            "geometry": group["geometry"],
            "relative_cut_codimension": source_dimension,
            "contains_internal_terminal_cut_equality": True,
            "parent_piece_incidences": parents,
            "parent_piece_incidence_count": len(parents),
            "parent_piece_incidences_sha256": digest(parents),
            **terminal_binding(group["geometry"]),
        }))
    need(
        sum(row["parent_piece_incidence_count"] for row in line_rows)
        == expected_line_parent_incidences
        and sum(row["parent_piece_incidence_count"] for row in point_rows)
        == expected_point_parent_incidences,
        "relative inherited H recursive cut parent incidence exhaustion",
    )
    recursive = {
        "schema": (
            "cm2.round306c30c.inherited-H-relative-"
            "internal-cut-complex.v1"
        ),
        "source_atom_dimension": source_dimension,
        "internal_terminal_cut_coordinates": {
            axis: [fraction(value) for value in values]
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


def build_boundary_atomic_join_rows(
    origin: str,
    leaf_rows: dict[str, Any],
    proof_source: dict[str, str],
    leaf_disposition: dict[str, str],
    combined_rows: list[dict[str, Any]],
    h_rows: list[dict[str, Any]],
    owner_audit: dict[str, Any],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Materialize every combined boundary -> whole-origin atomic-owner join."""
    axes = ("t", "p", "s")
    bounds = {
        key: {
            "t": (row.box.t0, row.box.t1),
            "p": (row.box.p0, row.box.p1),
            "s": (row.box.s0, row.box.s1),
        }
        for key, row in leaf_rows.items()
    }
    need(
        len(bounds) == 541
        and set(bounds) == set(proof_source) == set(leaf_disposition),
        "join exact 541-leaf maps:" + origin,
    )
    grid = {
        axis: sorted({value for item in bounds.values() for value in item[axis]})
        for axis in axes
    }
    combined_by_key = {row["cell_key"]: row for row in combined_rows}
    h_by_key = {row["cell_key"]: row for row in h_rows}
    full_owner_rows = sum((
        owner_audit["C30c_full_atomic_owner_ledger"][
            "atomic_" + str(dimension) + "D_owner_rows"
        ]
        for dimension in (2, 1, 0)
    ), [])
    full_owner_index = {
        (row["ambient_dimension"], canonical(row["geometry"]).decode("ascii")): row
        for row in full_owner_rows
    }
    need(
        len(full_owner_index) == len(full_owner_rows),
        "unique full atomic owner geometry/dimension membership",
    )

    def cuts(axis: str, lower: Q, upper: Q) -> list[Q]:
        values = [lower] + [
            value for value in grid[axis] if lower < value < upper
        ] + [upper]
        need(values == sorted(set(values)), "join atomic grid cuts")
        return values

    def atom_parts(
        geometry: dict[str, Any]
    ) -> tuple[dict[str, Q], dict[str, tuple[Q, Q]]]:
        return (
            {axis: Q(value) for axis, value in geometry["fixed"].items()},
            {
                axis: (Q(values[0]), Q(values[1]))
                for axis, values in geometry["open_spans"].items()
            },
        )

    def closure_contains(
        item: dict[str, tuple[Q, Q]],
        fixed: dict[str, Q],
        spans: dict[str, tuple[Q, Q]],
    ) -> bool:
        return all(
            item[axis][0] <= value <= item[axis][1]
            for axis, value in fixed.items()
        ) and all(
            item[axis][0] <= span[0] < span[1] <= item[axis][1]
            for axis, span in spans.items()
        )

    def containing_owner(
        fixed: dict[str, Q], spans: dict[str, tuple[Q, Q]]
    ) -> tuple[str, list[str]]:
        midpoints = {
            axis: (span[0] + span[1]) / 2 for axis, span in spans.items()
        }
        candidates = sorted(
            key for key, item in bounds.items()
            if all(
                item[axis][0] <= value <= item[axis][1]
                for axis, value in fixed.items()
            ) and all(
                item[axis][0] < value < item[axis][1]
                for axis, value in midpoints.items()
            ) and closure_contains(item, fixed, spans)
        )
        need(bool(candidates), "join atomic half-open owner exists")
        owner = candidates[0]
        need(
            closure_contains(bounds[owner], fixed, spans),
            "join owner covers complete atom",
        )
        return owner, candidates

    def relative_signature(
        item: dict[str, tuple[Q, Q]],
        fixed: dict[str, Q],
        spans: dict[str, tuple[Q, Q]],
    ) -> dict[str, str] | None:
        if not closure_contains(item, fixed, spans):
            return None
        signature: dict[str, str] = {}
        for axis, value in sorted(fixed.items()):
            if value == item[axis][0]:
                signature[axis] = "LOWER"
            elif value == item[axis][1]:
                signature[axis] = "UPPER"
        return signature

    def semantic_binding(
        owner: str,
        signature: dict[str, str],
        geometry: dict[str, Any],
    ) -> dict[str, Any]:
        if owner in combined_by_key:
            combined = combined_by_key[owner]
            return {
                "kind": "ROUND306C30C_COMBINED_ANALYTIC_PARTITION",
                "owner_cell_row_sha256": combined["row_sha256"],
                "relative_atomic_geometry": geometry,
                "analytic_support": typed_boundary_support(combined, signature),
            }
        if owner in h_by_key:
            h_row = h_by_key[owner]
            return {
                "kind": "ROUND306C30C_MATERIALIZED_INHERITED_H",
                "owner_cell_row_sha256": h_row["row_sha256"],
                "relative_atomic_geometry": geometry,
                "whole_cell_disposition": h_row["whole_H_cell_disposition"],
                "pointwise_H_partition_sha256": digest(h_row["H_partition"]),
                "pointwise_semantics_bound_by_complete_H_partition": True,
                "relative_H_sign_sheet_stratum_binding": (
                    inherited_h_relative_stratum_binding(h_row, geometry)
                ),
            }
        return {
            "kind": "PINNED_OR_SEALED_UPSTREAM_LEAF_DISPOSITION",
            "relative_atomic_geometry": geometry,
            "proof_source": proof_source[owner],
            "whole_cell_disposition": leaf_disposition[owner],
        }

    identity_by_geometry: dict[str, dict[str, Any]] = {}

    def materialized_identity(
        fixed: dict[str, Q], spans: dict[str, tuple[Q, Q]]
    ) -> tuple[dict[str, Any], dict[str, Any], list[dict[str, Any]]]:
        geometry = {
            "fixed": {
                axis: fraction(value) for axis, value in sorted(fixed.items())
            },
            "open_spans": {
                axis: [fraction(span[0]), fraction(span[1])]
                for axis, span in sorted(spans.items())
            },
        }
        owner, containing = containing_owner(fixed, spans)
        owner_member = full_owner_index.get((
            len(spans), canonical(geometry).decode("ascii")
        ))
        need(
            owner_member is not None
            and owner_member["closed_containing_leaf_keys"] == containing
            and owner_member["half_open_owner_leaf_key"] == owner
            and owner_member["owner_proof_source"] == proof_source[owner]
            and owner_member["owner_disposition"] == leaf_disposition[owner],
            "unique full atomic owner object membership",
        )
        incidences: list[dict[str, Any]] = []
        owner_signature: dict[str, str] | None = None
        for incident_key, incident in sorted(combined_by_key.items()):
            relative = relative_signature(bounds[incident_key], fixed, spans)
            if relative is None:
                continue
            selected = incident_key == owner
            if selected:
                owner_signature = relative
            incidences.append(sealed_row({
                "schema": "cm2.round306c30c.atomic-combined-incidence.row.v1",
                "combined_cell_key": incident_key,
                "combined_cell_row_sha256": incident["row_sha256"],
                "relative_boundary_codimension": len(relative),
                "relative_boundary_signature": relative,
                "selected_by_half_open_owner": selected,
                "analytic_support": typed_boundary_support(incident, relative),
            }))
        need(bool(incidences), "source combined incidence exists")
        whole_owner_alignment = sealed_row({
            "schema": (
                "cm2.round306c30c.whole-origin-atomic-owner-alignment.row.v1"
            ),
            "ambient_dimension": len(spans),
            "geometry": geometry,
            "whole_origin_atomic_owner_audit_sha256": digest(owner_audit),
            "full_atomic_owner_ledger_sha256": owner_audit[
                "C30c_full_atomic_owner_ledger_sha256"
            ],
            "full_atomic_owner_row": owner_member,
            "full_atomic_owner_row_sha256": owner_member["row_sha256"],
            "unique_geometry_dimension_membership_verified": True,
            "closed_containing_leaf_keys": containing,
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
            "closed_containing_leaf_keys": containing,
            "half_open_owner_leaf_key": owner,
            "owner_proof_source": proof_source[owner],
            "owner_disposition": leaf_disposition[owner],
            "selected_owner_semantic_binding": semantic_binding(
                owner,
                owner_signature if owner_signature is not None else {},
                geometry,
            ),
            "whole_origin_atomic_owner_alignment": whole_owner_alignment,
        }
        identity_key = str(len(spans)) + ":" + canonical(geometry).decode("ascii")
        previous = identity_by_geometry.setdefault(identity_key, identity)
        need(previous == identity, "cross-dimensional atomic owner consistency")
        return geometry, identity, incidences

    output: list[dict[str, Any]] = []
    dimension_census: Counter[str] = Counter()
    atom_dimension_census: Counter[str] = Counter()
    recursive_lower_census: Counter[str] = Counter()
    for combined in sorted(combined_rows, key=lambda row: row["cell_key"]):
        cell_key = combined["cell_key"]
        item = bounds[cell_key]
        boundaries = combined["outer_boundary_restriction_rows"]
        need(
            len(boundaries) == 26
            and Counter(row["ambient_dimension"] for row in boundaries)
            == Counter({2: 6, 1: 12, 0: 8}),
            "join source boundary 6+12+8:" + cell_key,
        )
        for boundary_ordinal, boundary in enumerate(boundaries):
            signature = boundary["fixed_coordinates"]
            fixed = {
                axis: item[axis][0 if side == "LOWER" else 1]
                for axis, side in sorted(signature.items())
            }
            free_axes = [axis for axis in axes if axis not in fixed]
            source_measure = Q(1)
            interval_choices: list[list[tuple[Q, Q]]] = []
            for axis in free_axes:
                source_measure *= item[axis][1] - item[axis][0]
                values = cuts(axis, item[axis][0], item[axis][1])
                interval_choices.append(list(zip(values, values[1:])))
            products = list(itertools.product(*interval_choices)) if free_axes else [()]
            atomic_bindings: list[dict[str, Any]] = []
            atomic_measure = Q(0)
            for atom_ordinal, product in enumerate(products):
                spans = dict(zip(free_axes, product, strict=True))
                measure = Q(1)
                for span in spans.values():
                    measure *= span[1] - span[0]
                atomic_measure += measure
                _geometry, identity, incidences = materialized_identity(fixed, spans)
                atomic_bindings.append(sealed_row({
                    "schema": "cm2.round306c30c.boundary-atomic-owner-binding.row.v1",
                    "atom_ordinal": atom_ordinal,
                    **identity,
                    "exact_measure": fraction(measure),
                    "closed_incident_combined_cells": incidences,
                    "closed_incident_combined_cells_sha256": digest(incidences),
                }))
                atom_dimension_census[str(len(free_axes)) + "D"] += 1
            cut_1d_groups: dict[str, dict[str, Any]] = {}
            if len(free_axes) == 2:
                for parent_atom in atomic_bindings:
                    atom_fixed, atom_spans = atom_parts(parent_atom["geometry"])
                    span_axes = sorted(atom_spans)
                    for boundary_axis in span_axes:
                        other_axis = next(
                            axis for axis in span_axes if axis != boundary_axis
                        )
                        for side, endpoint in (
                            ("LOWER", atom_spans[boundary_axis][0]),
                            ("UPPER", atom_spans[boundary_axis][1]),
                        ):
                            child_fixed = {
                                **atom_fixed, boundary_axis: endpoint,
                            }
                            child_spans = {other_axis: atom_spans[other_axis]}
                            child_geometry = {
                                "fixed": {
                                    axis: fraction(value)
                                    for axis, value in sorted(child_fixed.items())
                                },
                                "open_spans": {
                                    other_axis: [
                                        fraction(child_spans[other_axis][0]),
                                        fraction(child_spans[other_axis][1]),
                                    ]
                                },
                            }
                            key = canonical(child_geometry).decode("ascii")
                            group = cut_1d_groups.setdefault(key, {
                                "fixed": child_fixed,
                                "spans": child_spans,
                                "incident_parent_2D_atom_ordinals": [],
                                "parent_boundary_sides": [],
                            })
                            group["incident_parent_2D_atom_ordinals"].append(
                                parent_atom["atom_ordinal"]
                            )
                            group["parent_boundary_sides"].append({
                                "parent_2D_atom_ordinal": parent_atom["atom_ordinal"],
                                "fixed_axis": boundary_axis,
                                "side": side,
                            })
            cut_1d_rows: list[dict[str, Any]] = []
            for cut_ordinal, key in enumerate(sorted(cut_1d_groups)):
                group = cut_1d_groups[key]
                _geometry, identity, incidences = materialized_identity(
                    group["fixed"], group["spans"]
                )
                span = next(iter(group["spans"].values()))
                cut_1d_rows.append(sealed_row({
                    "schema": "cm2.round306c30c.recursive-1D-cut-owner.row.v1",
                    "cut_ordinal": cut_ordinal,
                    **identity,
                    "exact_measure": fraction(span[1] - span[0]),
                    "incident_parent_2D_atom_ordinals": sorted(set(
                        group["incident_parent_2D_atom_ordinals"]
                    )),
                    "parent_boundary_sides": sorted(
                        group["parent_boundary_sides"], key=canonical
                    ),
                    "closed_incident_combined_cells": incidences,
                    "closed_incident_combined_cells_sha256": digest(incidences),
                }))

            point_groups: dict[str, dict[str, Any]] = {}
            one_dimensional_parents: list[tuple[str, dict[str, Any]]] = []
            if len(free_axes) == 2:
                one_dimensional_parents = [
                    ("RECURSIVE_1D_CUT", row) for row in cut_1d_rows
                ]
            elif len(free_axes) == 1:
                one_dimensional_parents = [
                    ("PRIMARY_1D_ATOM", row) for row in atomic_bindings
                ]
            for parent_kind, parent_row in one_dimensional_parents:
                parent_fixed, parent_spans = atom_parts(parent_row["geometry"])
                free_axis, span = next(iter(parent_spans.items()))
                parent_ordinal = (
                    parent_row["cut_ordinal"]
                    if parent_kind == "RECURSIVE_1D_CUT"
                    else parent_row["atom_ordinal"]
                )
                for side, endpoint in (("LOWER", span[0]), ("UPPER", span[1])):
                    point_fixed = {**parent_fixed, free_axis: endpoint}
                    point_geometry = {
                        "fixed": {
                            axis: fraction(value)
                            for axis, value in sorted(point_fixed.items())
                        },
                        "open_spans": {},
                    }
                    key = canonical(point_geometry).decode("ascii")
                    group = point_groups.setdefault(key, {
                        "fixed": point_fixed,
                        "incident_1D_parents": [],
                    })
                    group["incident_1D_parents"].append({
                        "parent_kind": parent_kind,
                        "parent_ordinal": parent_ordinal,
                        "side": side,
                    })
            point_rows: list[dict[str, Any]] = []
            for point_ordinal, key in enumerate(sorted(point_groups)):
                group = point_groups[key]
                _geometry, identity, incidences = materialized_identity(
                    group["fixed"], {}
                )
                point_rows.append(sealed_row({
                    "schema": "cm2.round306c30c.recursive-0D-cut-owner.row.v1",
                    "point_ordinal": point_ordinal,
                    **identity,
                    "incident_1D_parents": sorted(
                        group["incident_1D_parents"], key=canonical
                    ),
                    "closed_incident_combined_cells": incidences,
                    "closed_incident_combined_cells_sha256": digest(incidences),
                }))
            need(
                (
                    len(free_axes) != 2
                    or sum(
                        len(row["parent_boundary_sides"])
                        for row in cut_1d_rows
                    ) == 4 * len(atomic_bindings)
                )
                and (
                    len(free_axes) == 0
                    or sum(
                        len(row["incident_1D_parents"])
                        for row in point_rows
                    ) == 2 * len(one_dimensional_parents)
                ),
                "recursive lower-strata membership exhaustion:" + cell_key,
            )
            recursive_lower_census["1D"] += len(cut_1d_rows)
            recursive_lower_census["0D"] += len(point_rows)
            need(
                atomic_measure == source_measure and bool(atomic_bindings),
                "boundary atom exact measure reclosure:" + cell_key,
            )
            absolute_geometry = {
                "fixed": {
                    axis: fraction(value) for axis, value in sorted(fixed.items())
                },
                "open_spans": {
                    axis: [fraction(item[axis][0]), fraction(item[axis][1])]
                    for axis in free_axes
                },
            }
            output.append(sealed_row({
                "schema": "cm2.round306c30c.combined-boundary-atomic-owner-join.row.v1",
                "origin_key": origin,
                "combined_cell_key": cell_key,
                "combined_cell_row_sha256": combined["row_sha256"],
                "boundary_ordinal_within_cell": boundary_ordinal,
                "boundary_restriction_row_sha256": boundary["row_sha256"],
                "fixed_coordinates": signature,
                "ambient_dimension": boundary["ambient_dimension"],
                "absolute_boundary_geometry": absolute_geometry,
                "source_exact_measure": fraction(source_measure),
                "atomic_exact_measure": fraction(atomic_measure),
                "atomic_measure_reclosed": True,
                "atomic_binding_count": len(atomic_bindings),
                "atomic_bindings": atomic_bindings,
                "atomic_bindings_sha256": digest(atomic_bindings),
                "recursive_lower_strata": {
                    "generation_rule": (
                        "EVERY_2D_ATOM_MATERIALIZES_ALL_FOUR_1D_CUT_EDGES__"
                        "EVERY_1D_CUT_OR_PRIMARY_ATOM_MATERIALIZES_BOTH_0D_ENDPOINTS__"
                        "PURE_GEOMETRY_DEDUP_WITH_INCIDENT_PARENT_MEMBERSHIP"
                    ),
                    "atomic_1D_cut_row_count": len(cut_1d_rows),
                    "atomic_1D_cut_rows": cut_1d_rows,
                    "atomic_1D_cut_rows_sha256": digest(cut_1d_rows),
                    "atomic_0D_cut_row_count": len(point_rows),
                    "atomic_0D_cut_rows": point_rows,
                    "atomic_0D_cut_rows_sha256": digest(point_rows),
                    "all_2D_atom_cut_lines_materialized": (
                        len(free_axes) != 2 or bool(cut_1d_rows)
                    ),
                    "all_1D_cut_endpoints_materialized": (
                        len(free_axes) == 0 or bool(point_rows)
                    ),
                    "lower_strata_owner_identity_bound_to_whole_origin_grid": True,
                },
                "source_boundary_analytic_support": typed_boundary_support(
                    combined, signature
                ),
                "composition_order": [
                    "WHOLE_ORIGIN_GRID_ATOM_IS_CLOSED_RECONSTRUCTED",
                    "LEXICOGRAPHIC_MIN_CONTAINING_LEAF_SELECTS_HALF_OPEN_OWNER",
                    "SELECTED_OWNER_PROOF_BINDS_POINTWISE_DISPOSITION",
                    "IF_SELECTED_OWNER_IS_COMBINED_APPLY_EXACT_RELATIVE_ANALYTIC_STRATUM",
                ],
                "child_or_measure_count_used_as_integer_credit": 0,
            }))
            dimension_census[str(boundary["ambient_dimension"]) + "D"] += 1
    output.sort(key=lambda row: (
        row["combined_cell_key"], row["boundary_ordinal_within_cell"]
    ))
    need(
        len(output) == 1040
        and dimension_census == Counter({"2D": 240, "1D": 480, "0D": 320}),
        "per-origin join 40x26 exact census:" + origin,
    )
    summary = {
        "schema": "cm2.round306c30c.combined-boundary-atomic-owner-join.summary.v1",
        "row_count": len(output),
        "row_sha256_sequence_sha256": digest([
            row["row_sha256"] for row in output
        ]),
        "boundary_dimension_census": dict(sorted(dimension_census.items())),
        "materialized_atom_incidence_census": dict(sorted(
            atom_dimension_census.items()
        )),
        "recursive_lower_strata_row_census": dict(sorted(
            recursive_lower_census.items()
        )),
        "unique_atomic_geometry_owner_identity_count": len(identity_by_geometry),
        "unique_atomic_geometry_owner_identities_sha256": digest([
            identity_by_geometry[key] for key in sorted(identity_by_geometry)
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


def build_origin_row(
    ordinal: int,
    origin: str,
    replay: dict[str, Any],
    roots: list[Any],
    base_rows: list[Any],
    refinement: dict[str, Any],
    leaves: dict[str, Any],
    h_rows: list[dict[str, Any]],
    direct_live: list[dict[str, Any]],
    combined_rows: list[dict[str, Any]],
    final_closed_sources: dict[str, str],
    registry: dict[str, Any],
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    prior = c30a.generalized_prior_partition(replay, origin)
    inherited = sorted(
        refinement["terminal_rows"], key=lambda value: value["cell_key"]
    )
    final_rows = sorted(
        refinement["final_residual_rows"], key=lambda value: value.key
    )
    h_by_key = {row["cell_key"]: row for row in h_rows}
    combined_by_key = {row["cell_key"]: row for row in combined_rows}
    direct_live_keys = {row["cell_key"] for row in direct_live}
    inherited_excluded_keys = {
        row["cell_key"] for row in inherited
        if row["coarse_disposition"] == "EXCLUDED"
    }

    audit_leaf_rows: dict[str, Any] = dict(prior["prior_closed_rows"])
    audit_leaf_rows.update({row.key: row for row in base_rows})
    audit_leaf_rows.update(leaves["terminal"])
    audit_leaf_rows.update(leaves["final"])
    proof_source = {
        key: "PINNED_PRE_DEPTH14_EXCLUDED"
        for key in prior["prior_closed_rows"]
    }
    proof_source.update({
        row.key: "PINNED_ROUND176_PRECLOSED_EXCLUDED" for row in base_rows
    })
    leaf_disposition = {
        key: "EXCLUDED" for key in prior["prior_closed_rows"]
    }
    leaf_disposition.update({row.key: "EXCLUDED" for row in base_rows})
    for evidence in inherited:
        key = evidence["cell_key"]
        if key in inherited_excluded_keys:
            proof_source[key] = "PINNED_ROUND180_INHERITED_EXCLUDED"
            leaf_disposition[key] = "EXCLUDED"
        elif key in direct_live_keys:
            proof_source[key] = "PINNED_ROUND180_DIRECT_STRICT_LIVE"
            leaf_disposition[key] = "LIVE"
        else:
            need(key in h_by_key, "missing inherited H materialization")
            proof_source[key] = "ROUND306C30C_MATERIALIZED_INHERITED_H"
            leaf_disposition[key] = h_by_key[key]["whole_H_cell_disposition"]
    for row in final_rows:
        if row.key in combined_by_key:
            proof_source[row.key] = "ROUND306C30C_COMBINED_DELTA_H_PARTITION"
            leaf_disposition[row.key] = "MIXED"
        else:
            need(row.key in final_closed_sources, "unbound final closure")
            proof_source[row.key] = final_closed_sources[row.key]
            leaf_disposition[row.key] = "EXCLUDED"

    disposition_census = Counter(leaf_disposition.values())
    need(
        len(audit_leaf_rows) == EXPECTED_PER_ORIGIN["top_level_leaf_count"]
        and len(leaf_disposition) == len(audit_leaf_rows)
        and disposition_census == EXPECTED_TOP_LEVEL_DISPOSITION,
        "complete 541-leaf disposition census:" + origin,
    )
    owner_audit = materialize_full_atomic_owner_audit(
        replay["origins"][origin]["box"],
        audit_leaf_rows,
        proof_source,
        leaf_disposition,
    )
    exact_owner_closure = (
        owner_audit["exact_3D_enclosure"]
        ["all_leaf_boxes_contained_in_parent_and_nondegenerate"]
        and owner_audit["exact_3D_enclosure"]
        ["pairwise_leaf_interiors_disjoint"]
        and owner_audit["exact_3D_enclosure"]
        ["leaf_exact_volume_sum_equals_parent"]
        and owner_audit["C30c_full_atomic_owner_ledger"]
        ["atomic_2D_owner_row_count"] > 0
        and owner_audit["C30c_full_atomic_owner_ledger"]
        ["atomic_1D_owner_row_count"] > 0
        and owner_audit["C30c_full_atomic_owner_ledger"]
        ["atomic_0D_owner_row_count"] > 0
    )
    need(exact_owner_closure, "whole-origin atomic owner closure:" + origin)
    join_rows, join_summary = build_boundary_atomic_join_rows(
        origin,
        audit_leaf_rows,
        proof_source,
        leaf_disposition,
        combined_rows,
        h_rows,
        owner_audit,
    )

    parent_volume = r215.box_volume(replay["origins"][origin]["box"])
    prior_volume = prior["prior_closed_exact_volume"]
    base_volume = sum((r215.box_volume(row.box) for row in base_rows), Q(0))
    root_volume = sum((r215.box_volume(row.box) for row in roots), Q(0))
    inherited_volume = sum(
        (
            r215.box_volume(leaves["terminal"][row["cell_key"]].box)
            for row in inherited
        ),
        Q(0),
    )
    final_volume = sum((r215.box_volume(row.box) for row in final_rows), Q(0))
    combined_volume = sum((Q(row["exact_volume"]) for row in combined_rows), Q(0))
    final_closed_volume = sum(
        (
            r215.box_volume(row.box) for row in final_rows
            if row.key in final_closed_sources
        ),
        Q(0),
    )
    need(
        prior_volume + base_volume + root_volume == parent_volume
        and inherited_volume + final_volume == root_volume
        and final_closed_volume + combined_volume == final_volume,
        "whole-origin exact volume conservation:" + origin,
    )

    first_live = min(
        [
            {
                "kind": "ROUND180_DIRECT_STRICT_LIVE_POSITIVE_VOLUME",
                "cell_key": row["cell_key"],
                "exact_volume": fraction(r215.box_volume(
                    leaves["terminal"][row["cell_key"]].box
                )),
            }
            for row in direct_live
        ]
        + [
            {
                "kind": "COMBINED_DELTA_H_LIVE_OPEN_SIDE",
                "cell_key": row["cell_key"],
                "predicate": LIVE_H_SIGN_BY_CHART[row["source_chart_id"]]
                + " AND Delta<0",
            }
            for row in combined_rows
        ],
        key=canonical,
    )
    theorem = {
        "kind": "SOURCE_W_FULL_DELTA_WHOLE_ORIGIN_RESOLVED_MIXED_THEOREM_CANDIDATE",
        "top_level_dyadic_leaf_partition_exact": exact_owner_closure,
        "top_level_leaf_disposition_census": dict(
            sorted(disposition_census.items())
        ),
        "every_combined_cell_has_exhaustive_disjoint_five_stratum_partition": all(
            row["partition_theorem"]
            ["five_predicate_strata_pointwise_disjoint"]
            and row["partition_theorem"]
            ["five_predicate_strata_pointwise_exhaustive"]
            for row in combined_rows
        ),
        "every_Delta_H_intersection_empty_including_boundary_restrictions": all(
            row["Delta_H_intersection"]["status"] == "EMPTY_CERTIFIED"
            and row["Delta_H_intersection"]
            ["all_outer_face_edge_vertex_restrictions_empty"]
            for row in combined_rows
        ),
        "all_combined_cells_mixed": True,
        "positive_measure_live_subset_exists": True,
        "positive_measure_excluded_subset_exists": True,
        "whole_original_physical_origin_disposition": "RESOLVED_MIXED",
        "whole_original_physical_origin_excluded": False,
    }
    body = {
        "schema": "cm2.round306c30c.source-w-full-delta.whole-origin-row.v1",
        "origin_ordinal": ordinal,
        "origin_key": origin,
        "priority_ordinal": registry["priority_ordinal"],
        "source_chart_id": replay["origins"][origin]["chart_id"],
        "original_parent_box": r176.box_row(replay["origins"][origin]["box"]),
        "lineage_census": {
            "Round176_prior": prior["prior_closed_count"],
            "Round176_preclosed": len(base_rows),
            "Round176_roots": len(roots),
            "Round180_inherited": len(inherited),
            "Round180_final": len(final_rows),
            "Round180_inherited_excluded": len(inherited_excluded_keys),
            "Round180_inherited_direct_live": len(direct_live_keys),
            "Round180_inherited_H": len(h_rows),
            "Round201_closed": sum(
                source == "ROUND201_EXACT_BEHIND_EXCLUDED"
                for source in final_closed_sources.values()
            ),
            "Round306C30A_closed": sum(
                source == "ROUND306C30A_CLIPPED_DELTA_EXCLUDED"
                for source in final_closed_sources.values()
            ),
            "combined_Delta_H": len(combined_rows),
            "top_level_leaf_count": len(audit_leaf_rows),
        },
        "top_level_leaf_disposition_census": dict(
            sorted(disposition_census.items())
        ),
        "combined_Delta_H_cell_count": len(combined_rows),
        "combined_Delta_H_cell_keys_sha256": digest([
            row["cell_key"] for row in combined_rows
        ]),
        "combined_Delta_H_cell_rows_sha256": digest(combined_rows),
        "inherited_H_cell_count": len(h_rows),
        "inherited_H_cell_keys_sha256": digest([
            row["cell_key"] for row in h_rows
        ]),
        "inherited_H_cell_rows_sha256": digest(h_rows),
        "disposition_aware_half_open_owner_audit": owner_audit,
        "combined_boundary_to_atomic_owner_binding": join_summary,
        "exact_volume_conservation": {
            "original_parent": fraction(parent_volume),
            "Round176_prior": fraction(prior_volume),
            "Round176_preclosed": fraction(base_volume),
            "Round176_roots": fraction(root_volume),
            "Round180_inherited": fraction(inherited_volume),
            "Round180_final": fraction(final_volume),
            "final_closed": fraction(final_closed_volume),
            "combined_Delta_H": fraction(combined_volume),
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
    need(
        body["lineage_census"] == EXPECTED_PER_ORIGIN,
        "exact expected lineage census:" + origin,
    )
    return sealed_row(body), join_rows


def write_rows(
    path: Path,
    rows: Iterable[dict[str, Any]],
) -> tuple[int, str]:
    sequence = hashlib.sha256()
    count = 0
    descriptor_fd = os.open(
        path,
        os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_CLOEXEC
        | getattr(os, "O_NOFOLLOW", 0),
        0o600,
    )
    with os.fdopen(descriptor_fd, "wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as output:
            for row in rows:
                output.write(canonical(row) + b"\n")
                sequence.update(bytes.fromhex(row["row_sha256"]))
                count += 1
        raw.flush()
        os.fsync(raw.fileno())
    return count, sequence.hexdigest()


def descriptor(path: Path, count: int, sequence: str, order: str) -> dict[str, Any]:
    return {
        "filename": path.name,
        "row_count": count,
        "size": path.stat().st_size,
        "sha256": file_hash(path),
        "row_sequence_sha256": sequence,
        "order": order,
    }


EXPECTED_CANDIDATE_FILES = {
    COMBINED_CELL_LEDGER, INHERITED_H_LEDGER, JOIN_LEDGER, ORIGIN_LEDGER,
    RESULT, "cm2_round306c30b_python_flint_runtime_attestation.json",
}


def durable_exclusive_write(path: Path, payload: bytes) -> None:
    flags = (
        os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_CLOEXEC
        | getattr(os, "O_NOFOLLOW", 0)
    )
    descriptor = os.open(path, flags, 0o600)
    try:
        view = memoryview(payload)
        while view:
            written = os.write(descriptor, view)
            need(written > 0, "durable output write:" + path.name)
            view = view[written:]
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def fsync_directory(path: Path) -> None:
    descriptor = os.open(
        path, os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC
        | getattr(os, "O_NOFOLLOW", 0)
    )
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def prepare_staging(path: Path) -> tuple[Path, Path]:
    target = Path(os.path.abspath(os.fspath(path)))
    need(target != ROOT and target.parent != target, "candidate target")
    parent_status = target.parent.lstat()
    need(
        stat.S_ISDIR(parent_status.st_mode)
        and not target.parent.is_symlink()
        and target.parent.resolve(strict=True)
        == Path(os.path.abspath(os.fspath(target.parent))),
        "candidate parent fixed regular directory",
    )
    try:
        target.lstat()
    except FileNotFoundError:
        pass
    else:
        raise BootstrapFailure("candidate target already exists")
    staging = Path(tempfile.mkdtemp(
        prefix="." + target.name + ".c30c-staging-",
        dir=target.parent,
    ))
    need(
        staging.parent == target.parent and not staging.is_symlink(),
        "same-parent staging directory",
    )
    return target, staging


def atomic_rename_noreplace(staging: Path, target: Path) -> None:
    libc = ctypes.CDLL(None, use_errno=True)
    renameat2 = getattr(libc, "renameat2", None)
    need(renameat2 is not None, "renameat2 RENAME_NOREPLACE available")
    renameat2.argtypes = [
        ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p,
        ctypes.c_uint,
    ]
    renameat2.restype = ctypes.c_int
    result = renameat2(
        -100, os.fsencode(staging), -100, os.fsencode(target), 1
    )
    if result != 0:
        error = ctypes.get_errno()
        if error == errno.EEXIST:
            raise BootstrapFailure("candidate target appeared before publication")
        raise OSError(error, os.strerror(error), os.fspath(target))


def validate_staging_bytes(staging: Path) -> dict[str, str]:
    directory_before = staging.lstat()
    directory_identity = (
        directory_before.st_dev, directory_before.st_ino,
        directory_before.st_mode, directory_before.st_nlink,
        directory_before.st_mtime_ns, directory_before.st_ctime_ns,
    )
    need(
        stat.S_ISDIR(directory_before.st_mode)
        and not staging.is_symlink()
        and {path.name for path in staging.iterdir()}
        == EXPECTED_CANDIDATE_FILES,
        "staging exact six-file set",
    )
    hashes: dict[str, str] = {}
    for filename in sorted(EXPECTED_CANDIDATE_FILES):
        path = staging / filename
        status = path.lstat()
        need(
            stat.S_ISREG(status.st_mode)
            and not path.is_symlink()
            and status.st_nlink == 1
            and path.resolve(strict=True).parent == staging.resolve(strict=True),
            "staging regular singleton:" + filename,
        )
        descriptor_fd = os.open(
            path, os.O_RDONLY | os.O_CLOEXEC | getattr(os, "O_NOFOLLOW", 0)
        )
        try:
            before = os.fstat(descriptor_fd)
            state = hashlib.sha256()
            size = 0
            while block := os.read(descriptor_fd, 1 << 20):
                state.update(block)
                size += len(block)
            after = os.fstat(descriptor_fd)
        finally:
            os.close(descriptor_fd)
        current = path.lstat()
        identity = (
            before.st_dev, before.st_ino, before.st_mode, before.st_nlink,
            before.st_size, before.st_mtime_ns, before.st_ctime_ns,
        )
        need(
            identity == (
                after.st_dev, after.st_ino, after.st_mode, after.st_nlink,
                after.st_size, after.st_mtime_ns, after.st_ctime_ns,
            )
            and identity == (
                current.st_dev, current.st_ino, current.st_mode,
                current.st_nlink, current.st_size, current.st_mtime_ns,
                current.st_ctime_ns,
            )
            and size == before.st_size,
            "staging stable byte capture:" + filename,
        )
        hashes[filename] = state.hexdigest()
    fsync_directory(staging)
    directory_after = staging.lstat()
    need(
        directory_identity == (
            directory_after.st_dev, directory_after.st_ino,
            directory_after.st_mode, directory_after.st_nlink,
            directory_after.st_mtime_ns, directory_after.st_ctime_ns,
        )
        and {path.name for path in staging.iterdir()}
        == EXPECTED_CANDIDATE_FILES,
        "staging directory/exact file set unchanged during validation",
    )
    return hashes


def _build_staging(candidate: Path) -> dict[str, Any]:
    validate_runtime_and_imports()
    c30b_authority = validate_c30b_seal()
    ctx.prec = 192
    runtime_path = candidate / c30b.RUNTIME_ATTESTATION
    durable_exclusive_write(runtime_path, c30b.BOOTSTRAP_RUNTIME_ATTESTATION_RAW)
    need(
        file_hash(runtime_path) == c30b.RUNTIME_ATTESTATION_RAW_SHA256,
        "published runtime attestation bytes",
    )
    registry, _summaries, c30a_rows = collect_frozen_inputs()
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
            need(kind == "EXCLUDED", "Round176 base closure disposition")
            base_by_origin[row.origin_key].append(row)
    need(
        set(roots_by_origin) == set(ORIGIN_KEYS)
        and all(
            len(roots_by_origin[key]) == EXPECTED_PER_ORIGIN["Round176_roots"]
            and len(base_by_origin[key])
            == EXPECTED_PER_ORIGIN["Round176_preclosed"]
            for key in ORIGIN_KEYS
        ),
        "two-origin Round176 reconstruction",
    )

    all_combined: list[dict[str, Any]] = []
    all_h: list[dict[str, Any]] = []
    all_origins: list[dict[str, Any]] = []
    all_join: list[dict[str, Any]] = []
    combined_ordinal = 0
    for origin_ordinal, origin in enumerate(ORIGIN_KEYS):
        roots = sorted(roots_by_origin[origin], key=lambda value: value.key)
        base_rows = sorted(base_by_origin[origin], key=lambda value: value.key)
        refinement = r180.refine_origin(roots, 4)
        leaves = r215.reconstruct_refinement_leaf_frontiers(roots, refinement)
        h_rows, direct_live = inherited_h_rows(origin, refinement, leaves)
        combined_rows: list[dict[str, Any]] = []
        final_closed_sources: dict[str, str] = {}
        for row in sorted(
            refinement["final_residual_rows"], key=lambda value: value.key
        ):
            reduction = r215.exact_behind_reduce(
                row, r180.residual_category(row)
            )
            if reduction["closed"]:
                final_closed_sources[row.key] = "ROUND201_EXACT_BEHIND_EXCLUDED"
                continue
            evidence = r215.analyze_residual_cell(row, reduction)
            need(
                evidence["analytic_closed"] is False,
                "unexpected Round215 analytic closure in full-Delta origin",
            )
            clipped = c30a_rows.get(row.key)
            if evidence["blocker"] == "SINGLE_CLIPPED_DELTA_ENDPOINT_OVERWRAP":
                need(clipped is not None, "missing C30a clipped row")
                if clipped["whole_closed_cell_excluded"]:
                    final_closed_sources[row.key] = (
                        "ROUND306C30A_CLIPPED_DELTA_EXCLUDED"
                    )
                    continue
                need(
                    clipped["disposition"]
                    == "RESIDUAL_NEGATIVE_OPEN_SIDE_NOT_EXCLUDED",
                    "unexpected C30a clipped disposition",
                )
            else:
                need(
                    evidence["blocker"]
                    == "SINGLE_FULL_DELTA_NEGATIVE_SIDE_NOT_EXCLUDED"
                    and clipped is None,
                    "unexpected final full-Delta blocker",
                )
            body = combined_delta_h_body(
                combined_ordinal, row, reduction, evidence, clipped
            )
            combined_rows.append(sealed_row(body))
            combined_ordinal += 1
        combined_rows.sort(key=lambda value: value["cell_key"])
        need(
            len(combined_rows) == EXPECTED_PER_ORIGIN["combined_Delta_H"]
            and Counter(row["source_kind"] for row in combined_rows)
            == Counter({
                "ROUND215_FULL_DELTA_NEGATIVE_SIDE": 30,
                "ROUND306C30A_CLIPPED_DELTA_RESIDUAL": 10,
            })
            and Counter(final_closed_sources.values()) == Counter({
                "ROUND201_EXACT_BEHIND_EXCLUDED": 328,
                "ROUND306C30A_CLIPPED_DELTA_EXCLUDED": 10,
            }),
            "per-origin final full-Delta composition:" + origin,
        )
        origin_row, join_rows = build_origin_row(
            origin_ordinal,
            origin,
            replay,
            roots,
            base_rows,
            refinement,
            leaves,
            h_rows,
            direct_live,
            combined_rows,
            final_closed_sources,
            registry[origin],
        )
        all_combined.extend(combined_rows)
        all_h.extend(h_rows)
        all_origins.append(origin_row)
        all_join.extend(join_rows)

    all_combined.sort(key=lambda value: value["cell_key"])
    all_h.sort(key=lambda value: value["cell_key"])
    all_origins.sort(key=lambda value: value["origin_key"])
    all_join.sort(key=lambda value: (
        value["combined_cell_key"], value["boundary_ordinal_within_cell"]
    ))
    need(
        len(all_combined) == 80
        and Counter(row["source_kind"] for row in all_combined)
        == EXPECTED_COMBINED_SOURCE
        and all(
            row["whole_closed_cell_disposition"] == "MIXED"
            and row["Delta_H_intersection"]["status"] == "EMPTY_CERTIFIED"
            for row in all_combined
        )
        and len(all_h) == 88
        and len(all_origins) == 2
        and len(all_join) == 2080
        and all(
            row["whole_origin_disposition"] == "RESOLVED_MIXED"
            and row["whole_original_physical_origin_excluded"] is False
            for row in all_origins
        ),
        "global C30c candidate census",
    )

    combined_count, combined_sequence = write_rows(
        candidate / COMBINED_CELL_LEDGER, all_combined
    )
    h_count, h_sequence = write_rows(candidate / INHERITED_H_LEDGER, all_h)
    origin_count, origin_sequence = write_rows(
        candidate / ORIGIN_LEDGER, all_origins
    )
    join_count, join_sequence = write_rows(candidate / JOIN_LEDGER, all_join)
    combined_descriptor = descriptor(
        candidate / COMBINED_CELL_LEDGER,
        combined_count,
        combined_sequence,
        "LEXICOGRAPHIC_ROUND180_FINAL_CELL_KEY",
    )
    h_descriptor = descriptor(
        candidate / INHERITED_H_LEDGER,
        h_count,
        h_sequence,
        "LEXICOGRAPHIC_ROUND180_INHERITED_H_CELL_KEY",
    )
    origin_descriptor = descriptor(
        candidate / ORIGIN_LEDGER,
        origin_count,
        origin_sequence,
        "LEXICOGRAPHIC_SOURCE_W_ORIGIN_KEY",
    )
    join_descriptor = descriptor(
        candidate / JOIN_LEDGER,
        join_count,
        join_sequence,
        "LEXICOGRAPHIC_COMBINED_CELL_KEY_THEN_BOUNDARY_ORDINAL",
    )
    runtime_descriptor = {
        "filename": c30b.RUNTIME_ATTESTATION,
        "size": len(c30b.BOOTSTRAP_RUNTIME_ATTESTATION_RAW),
        "sha256": c30b.RUNTIME_ATTESTATION_RAW_SHA256,
        "attestation_payload_sha256": c30b.RUNTIME_ATTESTATION_PAYLOAD_SHA256,
        "auditor_sha256": c30b.RUNTIME_AUDITOR_SHA256,
        "schema": c30b.BOOTSTRAP_RUNTIME_ATTESTATION["schema"],
        "verdict": c30b.BOOTSTRAP_RUNTIME_ATTESTATION["verdict"],
    }
    input_pins = sorted(
        c30b.INPUT_PINS + [
            {"filename": C30B_SOURCE, "sha256": C30B_SOURCE_SHA256},
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
        key=lambda value: value["filename"],
    )
    body = {
        "schema": "cm2.round306c30c.source-w-full-delta-whole-origin-disposition.candidate.v1",
        "status": (
            "PASS_CANDIDATE_ROUND306C30C_FULL_DELTA_DISPOSITION__"
            "AWAITING_INDEPENDENT_VERIFIER_AND_MANIFEST"
        ),
        "input_pins": input_pins,
        "runtime_attestation": runtime_descriptor,
        "upstream_C30b_dependency": {
            "pinned_reusable_producer_source": C30B_SOURCE,
            "pinned_reusable_producer_source_sha256": C30B_SOURCE_SHA256,
            "controlled_seed_guard_reused": True,
            "canonical_gzip_and_result_contract_reused": True,
            "producer_runtime_contract": (
                "ENV_I_EXACT_4_VARIABLES__PYTHONHASHSEED_IN_{30630071,30630929}"
                "__PYTHON_-P_-s_-B"
            ),
            "cold_verifier_runtime_contract": "PYTHON_-I_-B",
            "sealed_C30b_result_consumed": True,
            "sealed_authority": c30b_authority,
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
            "combined_source_census": dict(sorted(
                EXPECTED_COMBINED_SOURCE.items()
            )),
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
                "excluded": BEFORE_EXCLUDED,
                "conservative_live": BEFORE_LIVE,
                "remaining": BEFORE_REMAINING,
                "resolved_nonexcluded": BEFORE_RESOLVED_NONEXCLUDED,
                "total": 76_832,
                "remaining_partition": {
                    "full_Delta": 2,
                    "multi_Delta": 20,
                    "reduced_live": 2,
                    "retained_source_seams": 2,
                    "compact_q": 54,
                },
            },
            "candidate_credits": {
                "whole_origin_exclusion": 0,
                "resolved_origin_disposition": 2,
                "resolved_nonexcluded": 2,
            },
            "after": {
                "excluded": AFTER_EXCLUDED,
                "conservative_live": AFTER_LIVE,
                "remaining": AFTER_REMAINING,
                "resolved_nonexcluded": AFTER_RESOLVED_NONEXCLUDED,
                "total": 76_832,
                "remaining_partition": {
                    "multi_Delta": 20,
                    "reduced_live": 2,
                    "retained_source_seams": 2,
                    "compact_q": 54,
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
            "D03": "UNAUTHORIZED",
            "D04": "NOT_MINTED",
            "Gate5_filled_field_slots": "10/18",
            "Gate5_complete_global_blocks": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "required_next": (
            "RUN_INDEPENDENT_C30C_VERIFIER_ATTACK_HARNESS_DUAL_CONTROLLED_"
            "SEED_REPLAY_SCRUBBED_COLD_REPLAY_AND_MANIFEST_BEFORE_ANY_"
            "C30C_LEDGER_CREDIT"
        ),
    }
    result = {**body, "result_sha256": digest(body)}
    durable_exclusive_write(candidate / RESULT, canonical(result))
    need(
        {path.name for path in candidate.iterdir()} == EXPECTED_CANDIDATE_FILES,
        "candidate final exact file set",
    )
    return result


def build(candidate_path: Path) -> dict[str, Any]:
    target, staging = prepare_staging(candidate_path)
    committed = False
    try:
        result = _build_staging(staging)
        hashes = validate_staging_bytes(staging)
        need(
            hashes[RESULT] == hashlib.sha256(canonical(result)).hexdigest(),
            "staging result hash after durable close",
        )
        atomic_rename_noreplace(staging, target)
        committed = True
        fsync_directory(target.parent)
        return result
    except BaseException:
        # A successful no-replace rename is an irreversible publication
        # commit: the six-file directory is complete, and deleting members at
        # the final path would itself expose a partial final directory.  Only
        # never-published staging is eligible for cleanup.
        if not committed and staging.exists() and not staging.is_symlink():
            shutil.rmtree(staging)
            try:
                fsync_directory(target.parent)
            except OSError:
                pass
        raise


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate-dir", required=True)
    arguments = parser.parse_args()
    result = build(Path(arguments.candidate_dir))
    print(canonical({
        "status": result["status"],
        "result_sha256": result["result_sha256"],
    }).decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
