#!/usr/bin/env python3
"""Independent receipt verifier for Round306B1AF4K1.

This verifier pins the K1 program and its two direct dependencies, executes
the public CLI in an isolated temporary working tree, and loads the exact
pinned K1 bytes in a separate worker process for black-box function tests.
It is not an independent implementation of the mathematics.  Every emitted
receipt grants exactly zero formal theorem, B1A, B2, D02, or CM2 credit.
"""
from __future__ import annotations

from copy import deepcopy
from fractions import Fraction
import hashlib
import json
import os
from pathlib import Path
import shutil
import stat
import subprocess
import sys
import tempfile
import types
from typing import Any, Callable, Mapping, Sequence


SCHEMA = "cm2.round306b1af4k1.source-g-semantic-theorem-kernel.independent-receipt.v1"
BASE = Path(__file__).absolute().parent
VERIFIER_NAME = Path(__file__).name
RUNTIME_SNAPSHOT_NAME = "runtime_verifier.py"
TARGET_NAME = "cm2_round306b1af4k1_source_g_semantic_theorem_kernel.py"
TARGET_SCHEMA = "cm2.round306b1af4k1.source-g-semantic-theorem-kernel.v1"
TARGET_CONTRACT_SHA256 = "5c2405c96df150079800d2c6fe0a19a737f621ff53bd2785c6a9e39c6c3885f7"
TARGET_DEPENDENCY_VERIFICATION_SHA256 = "bd64019d57d6263bd22119c2e619def721a65d5c58b7f3cbbf0348eb17401700"
TARGET_PIN_SET_SHA256 = "25951efd37e52424897453d62602f6163f3c653558819c4a5c1286575e79875c"
PINS = (
    {
        "role": "K1_TARGET",
        "filename": TARGET_NAME,
        "size": 68346,
        "sha256": "17d9c302984e2e29dcf02832f36ec9437c23c8b65c27289a3469db222ce4edae",
    },
    {
        "role": "DIRECT_DEPENDENCY_SYMBOLIC_KERNEL",
        "filename": "cm2_round306b1af4_source_g_normalized_support_symbolic_kernel.py",
        "size": 87237,
        "sha256": "c8bb9cf85aace782639859c33625732bf866a7fad34ff31cce58ab84af9f6a6f",
    },
    {
        "role": "DIRECT_DEPENDENCY_SEMANTIC_WIRE_DELTA",
        "filename": "cm2_round306b1af4d1_source_g_semantic_wire_delta_contract.py",
        "size": 84392,
        "sha256": "5082df54ea4c514de906f4a923856adb20c6240c9be33401e784b2513a85f09f",
    },
)
CHECKER_KERNEL_IDS = {
    "box": "RATIONAL_BOX_PARTITION_V1",
    "trace": "REGULAR_LEVELSET_ONE_SIDED_TRACE_V1",
    "codim2": "CODIM2_INTERSECTION_DISPOSITION_V1",
    "mixed_face": "MIXED_BOUNDARY_FACE_PARTITION_V1",
    "chart_map": "CHART_MAP_BIJECTION_V1",
    "owner": "MEMBER_REPRESENTATION_UNION_COVER_V1",
    "proof_dag": "PROOF_BUNDLE_DAG_VALIDATION_V1",
}
ZERO_CREDIT = {
    "normalized_support": 0,
    "representation_cover": 0,
    "physical_incidence": 0,
    "transition": 0,
    "pair_routing": 0,
    "maximality": 0,
    "fibre": 0,
    "global_disposition": 0,
    "B1A": 0,
    "B2": 0,
    "D02": 0,
    "CM2": 0,
}


class VerificationBlocked(RuntimeError):
    pass


def need(ok: bool, label: str) -> None:
    if not ok:
        raise VerificationBlocked(label)


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=True,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("ascii")


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def object_sha256(value: Any) -> str:
    return sha256_bytes(canonical_bytes(value))


def file_bytes(value: Any) -> bytes:
    return canonical_bytes(value) + b"\n"


def seal_object(body: Mapping[str, Any]) -> dict[str, Any]:
    need("object_self_sha256" not in body, "self-hash field absent before seal")
    snapshot = json.loads(canonical_bytes(body))
    return {**snapshot, "object_self_sha256": object_sha256(snapshot)}


def strict_json_load(raw: bytes, label: str) -> Any:
    need(raw.endswith(b"\n") and raw.count(b"\n") == 1, label + " exact one-line newline")
    try:
        text = raw[:-1].decode("ascii")
    except UnicodeDecodeError as error:
        raise VerificationBlocked(label + " ASCII") from error

    def pairs(rows: list[tuple[str, Any]]) -> dict[str, Any]:
        out: dict[str, Any] = {}
        for key, value in rows:
            need(type(key) is str and key not in out, label + " unique string keys")
            out[key] = value
        return out

    def reject_float(_token: str) -> Any:
        raise VerificationBlocked(label + " float")

    try:
        value = json.loads(
            text,
            object_pairs_hook=pairs,
            parse_float=reject_float,
            parse_constant=reject_float,
        )
    except VerificationBlocked:
        raise
    except (UnicodeError, ValueError, TypeError, RecursionError) as error:
        raise VerificationBlocked(label + " strict JSON") from error
    need(raw == file_bytes(value), label + " canonical JSON bytes")
    return value


def _fingerprint(row: os.stat_result) -> tuple[int, ...]:
    return (
        row.st_dev,
        row.st_ino,
        row.st_mode,
        row.st_nlink,
        row.st_size,
        row.st_mtime_ns,
        row.st_ctime_ns,
    )


def _hash_fd(fd: int) -> tuple[int, str]:
    os.lseek(fd, 0, os.SEEK_SET)
    total = 0
    digest = hashlib.sha256()
    while True:
        block = os.read(fd, 1 << 20)
        if not block:
            break
        total += len(block)
        digest.update(block)
    return total, digest.hexdigest()


def verify_pins(base: Path = BASE) -> dict[str, Any]:
    """Open all three files before hashing; hold and revalidate every fd/path."""
    directory = os.fspath(base)
    path_dir = os.stat(directory, follow_symlinks=False)
    need(stat.S_ISDIR(path_dir.st_mode), "deliverables directory")
    flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
    dfd = os.open(directory, flags)
    opened: list[tuple[dict[str, Any], int, os.stat_result]] = []
    rows: list[dict[str, Any]] = []
    try:
        held_dir = os.fstat(dfd)
        need(_fingerprint(path_dir) == _fingerprint(held_dir), "directory open race")
        try:
            for pin in PINS:
                name = pin["filename"]
                need(name == os.path.basename(name) and name not in {"", ".", ".."}, "pin basename")
                before = os.stat(name, dir_fd=dfd, follow_symlinks=False)
                need(stat.S_ISREG(before.st_mode), "pin regular")
                need(before.st_nlink == 1, "pin hardlink fail-close")
                need(before.st_size == pin["size"], "pin size")
                fd = os.open(
                    name,
                    os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0),
                    dir_fd=dfd,
                )
                held = os.fstat(fd)
                need(_fingerprint(before) == _fingerprint(held), "pin open race")
                opened.append((pin, fd, held))
            for pin, fd, held in opened:
                size1, hash1 = _hash_fd(fd)
                need(_fingerprint(os.fstat(fd)) == _fingerprint(held), "pin pass1 race")
                size2, hash2 = _hash_fd(fd)
                need(_fingerprint(os.fstat(fd)) == _fingerprint(held), "pin pass2 race")
                need(_fingerprint(os.stat(pin["filename"], dir_fd=dfd, follow_symlinks=False)) == _fingerprint(held), "pin path replacement")
                need(size1 == size2 == pin["size"], "pin two-pass size")
                need(hash1 == hash2 == pin["sha256"], "pin two-pass hash")
                rows.append(
                    {
                        "role": pin["role"],
                        "filename": pin["filename"],
                        "size": size1,
                        "sha256": hash1,
                        "held_fd_stable": True,
                        "two_pass_same_fd": True,
                        "regular_nlink_one": True,
                    }
                )
            for pin, fd, held in opened:
                need(_fingerprint(os.fstat(fd)) == _fingerprint(held), "final held fd")
                need(_fingerprint(os.stat(pin["filename"], dir_fd=dfd, follow_symlinks=False)) == _fingerprint(held), "final all-pin path")
        finally:
            for _pin, fd, _held in reversed(opened):
                os.close(fd)
        need(_fingerprint(os.fstat(dfd)) == _fingerprint(held_dir), "held directory final")
        need(_fingerprint(os.stat(directory, follow_symlinks=False)) == _fingerprint(held_dir), "directory path final")
    finally:
        os.close(dfd)
    return {
        "status": "PASS",
        "pin_count": 3,
        "all_file_fds_open_before_first_hash": True,
        "two_pass_same_fd": True,
        "final_all_pin_path_revalidation_before_any_fd_close": True,
        "symlink_and_hardlink_fail_closed": True,
        "full_directory_fingerprint_stable": True,
        "pins": rows,
        "pin_rows_sha256": object_sha256(rows),
    }


def _write_all(fd: int, raw: bytes) -> None:
    offset = 0
    while offset < len(raw):
        count = os.write(fd, raw[offset:])
        need(count > 0, "snapshot short write")
        offset += count


def _materialize_isolated_snapshot(root: Path, runtime_raw: bytes, runtime_pin: Mapping[str, Any]) -> Path:
    """Copy all exact held-fd pins into one private read-only snapshot."""
    snapshot = root / "snapshot"
    snapshot.mkdir(mode=0o700)
    directory = os.fspath(BASE)
    path_dir = os.stat(directory, follow_symlinks=False)
    dflags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
    dfd = os.open(directory, dflags)
    sfd = os.open(os.fspath(snapshot), dflags)
    opened: list[tuple[dict[str, Any], int, os.stat_result]] = []
    try:
        held_dir = os.fstat(dfd)
        need(_fingerprint(path_dir) == _fingerprint(held_dir), "snapshot source directory race")
        for pin in PINS:
            before = os.stat(pin["filename"], dir_fd=dfd, follow_symlinks=False)
            need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1 and before.st_size == pin["size"], "snapshot source metadata")
            fd = os.open(
                pin["filename"],
                os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0),
                dir_fd=dfd,
            )
            held = os.fstat(fd)
            need(_fingerprint(before) == _fingerprint(held), "snapshot source open race")
            opened.append((pin, fd, held))
        for pin, fd, held in opened:
            size1, hash1 = _hash_fd(fd)
            size2, hash2 = _hash_fd(fd)
            os.lseek(fd, 0, os.SEEK_SET)
            raw = bytearray()
            while True:
                block = os.read(fd, 1 << 20)
                if not block:
                    break
                raw.extend(block)
            need(_fingerprint(os.fstat(fd)) == _fingerprint(held), "snapshot held source")
            need(size1 == size2 == len(raw) == pin["size"] and hash1 == hash2 == sha256_bytes(bytes(raw)) == pin["sha256"], "snapshot exact source")
            out_fd = os.open(
                pin["filename"],
                os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0),
                0o400,
                dir_fd=sfd,
            )
            try:
                _write_all(out_fd, bytes(raw))
                os.fsync(out_fd)
            finally:
                os.close(out_fd)
            copied = os.stat(pin["filename"], dir_fd=sfd, follow_symlinks=False)
            need(stat.S_ISREG(copied.st_mode) and copied.st_nlink == 1 and copied.st_size == pin["size"], "snapshot copy metadata")
        need(len(runtime_raw) == runtime_pin["size"] and sha256_bytes(runtime_raw) == runtime_pin["sha256"], "runtime snapshot source bytes")
        runtime_fd = os.open(
            RUNTIME_SNAPSHOT_NAME,
            os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0),
            0o400,
            dir_fd=sfd,
        )
        try:
            _write_all(runtime_fd, runtime_raw)
            os.fsync(runtime_fd)
        finally:
            os.close(runtime_fd)
        runtime_copy = os.stat(RUNTIME_SNAPSHOT_NAME, dir_fd=sfd, follow_symlinks=False)
        need(stat.S_ISREG(runtime_copy.st_mode) and runtime_copy.st_nlink == 1 and runtime_copy.st_size == runtime_pin["size"], "runtime snapshot copy metadata")
        for pin, fd, held in opened:
            need(_fingerprint(os.fstat(fd)) == _fingerprint(held), "snapshot final held source")
            need(_fingerprint(os.stat(pin["filename"], dir_fd=dfd, follow_symlinks=False)) == _fingerprint(held), "snapshot final source path")
        need(_fingerprint(os.fstat(dfd)) == _fingerprint(held_dir), "snapshot held source directory")
        need(_fingerprint(os.stat(directory, follow_symlinks=False)) == _fingerprint(held_dir), "snapshot source directory final")
        os.fsync(sfd)
    finally:
        for _pin, fd, _held in reversed(opened):
            os.close(fd)
        os.close(sfd)
        os.close(dfd)
    os.chmod(snapshot, 0o500)
    verification = verify_pins(snapshot)
    need(verification["status"] == "PASS" and verification["pin_count"] == 3, "snapshot pin verification")
    _verify_runtime_snapshot_copy(snapshot, runtime_pin)
    return snapshot


def _read_exact_target_bytes(base: Path) -> bytes:
    pin = PINS[0]
    flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
    path = base / pin["filename"]
    before = os.stat(path, follow_symlinks=False)
    need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1 and before.st_size == pin["size"], "worker target path metadata")
    fd = os.open(os.fspath(path), flags)
    try:
        held = os.fstat(fd)
        need(_fingerprint(before) == _fingerprint(held), "worker target open race")
        size1, hash1 = _hash_fd(fd)
        size2, hash2 = _hash_fd(fd)
        os.lseek(fd, 0, os.SEEK_SET)
        raw = bytearray()
        while True:
            block = os.read(fd, 1 << 20)
            if not block:
                break
            raw.extend(block)
        need(_fingerprint(os.fstat(fd)) == _fingerprint(held), "worker held target")
        need(_fingerprint(os.stat(path, follow_symlinks=False)) == _fingerprint(held), "worker target final path identity")
        need(size1 == size2 == len(raw) == pin["size"] and hash1 == hash2 == sha256_bytes(bytes(raw)) == pin["sha256"], "worker target bytes")
        return bytes(raw)
    finally:
        os.close(fd)


def _load_target(base: Path) -> types.ModuleType:
    """Load exact held-fd bytes for black-box calls; do not import dependencies."""
    sys.dont_write_bytecode = True
    source = _read_exact_target_bytes(base)
    name = "_cm2_k1_black_box_target"
    module = types.ModuleType(name)
    module.__file__ = os.fspath(base / TARGET_NAME)
    module.__package__ = ""
    sys.modules[name] = module
    try:
        exec(compile(source, module.__file__, "exec"), module.__dict__)
    except BaseException:
        sys.modules.pop(name, None)
        raise
    return module


def q(value: int | Fraction) -> dict[str, int]:
    value = Fraction(value)
    return {"numerator": value.numerator, "denominator": value.denominator}


def const(value: int | Fraction) -> dict[str, Any]:
    return {"op": "CONST_Q", "value": q(value)}


def var(name: str) -> dict[str, str]:
    return {"op": "VAR", "name": name}


def box(name: str, lower: int | Fraction, upper: int | Fraction) -> dict[str, Any]:
    return {
        "wire_id": "RATIONAL_INTERVAL_BOX_V1",
        "coordinate_parameter": "TEST",
        "axes": [
            {
                "axis": name,
                "lower": q(lower),
                "lower_closed": True,
                "upper": q(upper),
                "upper_closed": True,
            }
        ],
    }


def split_box(name: str, lower: int | Fraction, cut: int | Fraction, upper: int | Fraction) -> list[dict[str, Any]]:
    first = box(name, lower, cut)
    second = box(name, cut, upper)
    first["axes"][0]["upper_closed"] = False
    return [first, second]


def trace_certificate(name: str) -> dict[str, Any]:
    ambient = box(name, 0, 1)
    return {
        "wire_id": "REGULAR_LEVELSET_ONE_SIDED_TRACE_CERT_V1",
        "factor_ast": {"op": "SUB", "left": var(name), "right": const(Fraction(1, 2))},
        "derivative_ast": const(1),
        "graph_variable": name,
        "side_sign": 1,
        "ambient_box": ambient,
        "cells": [deepcopy(ambient)],
        "claimed_approach_face_by_cell": [{"cell_index": 0, "approach_face": "UPPER"}],
    }


def codim_certificate(name: str, upper: int) -> dict[str, Any]:
    domain = box(name, 0, upper)
    return {
        "wire_id": "CODIM2_INTERSECTION_DISPOSITION_CERT_V1",
        "disposition": "EMPTY",
        "domain_box": domain,
        "cover_cells": [deepcopy(domain)],
        "source_factor_ast": {"op": "ADD", "args": [var(name), const(1)]},
        "target_factor_ast": {"op": "SUB", "left": var(name), "right": const(1)},
        "per_cell_excluded_factor": ["SOURCE"],
    }


def mixed_certificate(row_prefix: str, owner_prefix: str) -> dict[str, Any]:
    parent = {
        "wire_id": "RATIONAL_INTERVAL_BOX_V1",
        "coordinate_parameter": "TEST",
        "axes": [box("x", 0, 1)["axes"][0], box("y", 0, 2)["axes"][0]],
    }
    first = deepcopy(parent)
    first["axes"][1]["upper"] = q(1)
    first["axes"][1]["upper_closed"] = False
    second = deepcopy(parent)
    second["axes"][1]["lower"] = q(1)
    return {
        "wire_id": "MIXED_BOUNDARY_FACE_PARTITION_CERT_V1",
        "parent_box": parent,
        "face_axis": "x",
        "face_side": "LOWER",
        "child_rows": [
            {"row_id": row_prefix + "0", "owner_member_id": owner_prefix + "0", "child_box": first},
            {"row_id": row_prefix + "1", "owner_member_id": owner_prefix + "1", "child_box": second},
        ],
    }


def chart_certificate(source: str, target: str) -> dict[str, Any]:
    return {
        "wire_id": "CHART_MAP_AST_V1",
        "source_variables": [source],
        "target_variables": [target],
        "forward_components": [{"target_variable": target, "expression_ast": var(source)}],
        "inverse_branches": [
            {
                "branch_id": "b0",
                "source_components": [{"source_variable": source, "expression_ast": var(target)}],
            }
        ],
    }


def owner_certificate(member: str) -> dict[str, Any]:
    return {
        "wire_id": "REPRESENTATION_OWNER_BOOKKEEPING_V1",
        "member_ids": [member],
        "representation_rows": [
            {
                "representation_row_id": "a",
                "owner_member_id": member,
                "coverage_semantics": "FULL_SET_EQUALITY",
                "cover_group_id": None,
            },
            {
                "representation_row_id": "p",
                "owner_member_id": member,
                "coverage_semantics": "PARTIAL_INCLUSION",
                "cover_group_id": "g",
            },
        ],
        "member_cover_groups": [
            {
                "cover_group_id": "g",
                "owner_member_id": member,
                "representation_row_ids": ["p"],
            }
        ],
    }


def proof_bundle(subject: str, payload_value: str = "strict") -> dict[str, Any]:
    payload0 = {"normalized": True}
    payload1 = {"interval": payload_value}
    claims = [
        {"role": "AST_NORMALIZATION", "claim_id": "c0", "kernel_id": "K0", "payload": payload0, "payload_sha256": object_sha256(payload0)},
        {"role": "INTERVAL_SIGNS", "claim_id": "c1", "kernel_id": "K1", "payload": payload1, "payload_sha256": object_sha256(payload1)},
    ]
    body = {
        "wire_id": "PROOF_BUNDLE_DAG_V1",
        "subject_row_id": subject,
        "claims": claims,
        "dependency_edges": [{"claim_id": "c1", "depends_on_claim_id": "c0"}],
        "root_claim_ids": ["c1"],
        "formal_credit": 0,
    }
    return {**body, "bundle_sha256": object_sha256(body)}


def _summary(result: Mapping[str, Any]) -> dict[str, Any]:
    return {key: deepcopy(value) for key, value in result.items() if key not in {"canonical_input_commitment_sha256", "check_digest_sha256"}}


def _expected_commitment(kernel_id: str, canonical_input: Any) -> str:
    return object_sha256(
        {
            "schema": TARGET_SCHEMA + ".canonical-check-input.v1",
            "kernel_id": kernel_id,
            "input": canonical_input,
        }
    )


def _expect_blocked(call: Callable[[], Any], label: str) -> dict[str, str]:
    try:
        call()
    except Exception as error:
        need(type(error).__name__ == "CheckBlocked", label + " exact fail-closed exception")
        return {"case_id": label, "expected": "REJECTED", "observed": "REJECTED", "category": "STRICT_JSON_TYPE"}
    raise VerificationBlocked(label + " accepted")


def black_box_worker(snapshot: Path) -> dict[str, Any]:
    pin_verification = verify_pins(snapshot)
    module = _load_target(snapshot)

    parent = box("x", 0, 2)
    box_inputs = [
        {"parent_box": parent, "child_boxes": split_box("x", 0, 1, 2), "face": None},
        {"parent_box": parent, "child_boxes": split_box("x", 0, Fraction(1, 2), 2), "face": None},
    ]
    box_results = [module.check_box_partition(row["parent_box"], row["child_boxes"]) for row in box_inputs]

    trace_inputs = [trace_certificate("t"), trace_certificate("z")]
    trace_results = [module.check_regular_trace(row) for row in trace_inputs]

    codim_inputs = [codim_certificate("x", 2), codim_certificate("y", 3)]
    codim_results = [module.check_codim2_empty(row) for row in codim_inputs]

    mixed_inputs = [mixed_certificate("r", "m"), mixed_certificate("s", "n")]
    mixed_results = [module.check_mixed_face_partition(row) for row in mixed_inputs]

    chart_inputs = [chart_certificate("x", "u"), chart_certificate("y", "v")]
    chart_results = [module.check_chart_map(row) for row in chart_inputs]

    owner_inputs = [owner_certificate("m0"), owner_certificate("m1")]
    owner_results = [module.check_representation_owners(row) for row in owner_inputs]

    roles = ["AST_NORMALIZATION", "INTERVAL_SIGNS"]
    dag_bundles = [proof_bundle("subject-a", "strict"), proof_bundle("subject-b", "bounded")]
    dag_inputs = [{"bundle": row, "required_roles": roles} for row in dag_bundles]
    dag_results = [module.check_proof_bundle(row, roles) for row in dag_bundles]

    pairs = {
        "box": (box_inputs, box_results),
        "trace": (trace_inputs, trace_results),
        "codim2": (codim_inputs, codim_results),
        "mixed_face": (mixed_inputs, mixed_results),
        "chart_map": (chart_inputs, chart_results),
        "owner": (owner_inputs, owner_results),
        "proof_dag": (dag_inputs, dag_results),
    }
    pair_rows = []
    for category in CHECKER_KERNEL_IDS:
        inputs, results = pairs[category]
        need(len(inputs) == len(results) == 2, category + " pair arity")
        need(_summary(results[0]) == _summary(results[1]), category + " identical mechanical summary")
        commitments = []
        result_digests = []
        for canonical_input, result in zip(inputs, results):
            need(type(result) is dict, category + " result type")
            expected = _expected_commitment(CHECKER_KERNEL_IDS[category], canonical_input)
            need(result.get("canonical_input_commitment_sha256") == expected, category + " input commitment")
            body = {key: deepcopy(value) for key, value in result.items() if key != "check_digest_sha256"}
            need(result.get("check_digest_sha256") == object_sha256(body), category + " result rehash")
            commitments.append(expected)
            result_digests.append(result["check_digest_sha256"])
        need(len(set(commitments)) == 2 and len(set(result_digests)) == 2, category + " distinct certificate digests")
        pair_rows.append(
            {
                "category": category,
                "kernel_id": CHECKER_KERNEL_IDS[category],
                "valid_certificate_count": 2,
                "identical_result_summary": True,
                "distinct_input_commitments": True,
                "distinct_result_digests": True,
                "independent_commitment_rehash": True,
                "independent_result_rehash": True,
                "input_commitment_sha256s": commitments,
                "check_digest_sha256s": result_digests,
            }
        )

    bool_face = ("x", False)
    int_face = ("x", 0)
    trace_bool_sign = trace_certificate("t")
    trace_bool_sign["side_sign"] = True
    trace_bool_index = trace_certificate("t")
    trace_bool_index["claimed_approach_face_by_cell"][0]["cell_index"] = False
    false_credit = proof_bundle("subject-false")
    false_credit["formal_credit"] = False
    false_body = {key: deepcopy(false_credit[key]) for key in ("wire_id", "subject_row_id", "claims", "dependency_edges", "root_claim_ids", "formal_credit")}
    false_credit["bundle_sha256"] = object_sha256(false_body)
    tuple_payload = proof_bundle("subject-tuple")
    tuple_payload["claims"][0]["payload"] = ("tuple",)
    tuple_payload["claims"][0]["payload_sha256"] = object_sha256(("tuple",))
    non_string_payload = proof_bundle("subject-key")
    non_string_payload["claims"][0]["payload"] = {1: "value"}
    non_string_payload["claims"][0]["payload_sha256"] = object_sha256({1: "value"})
    float_payload = proof_bundle("subject-float")
    float_payload["claims"][0]["payload"] = 1.0
    float_payload["claims"][0]["payload_sha256"] = object_sha256(1.0)
    type_cases = [
        _expect_blocked(lambda: module.check_box_partition(parent, [deepcopy(parent)], bool_face), "face_bool_endpoint_alias"),
        _expect_blocked(lambda: module.check_box_partition(parent, [deepcopy(parent)], int_face), "face_int_endpoint_noncanonical"),
        _expect_blocked(lambda: module.check_regular_trace(trace_bool_sign), "trace_side_sign_bool_alias"),
        _expect_blocked(lambda: module.check_regular_trace(trace_bool_index), "trace_cell_index_bool_alias"),
        _expect_blocked(lambda: module.check_proof_bundle(false_credit, roles), "bundle_formal_credit_bool_alias"),
        _expect_blocked(lambda: module.check_proof_bundle(tuple_payload, roles), "bundle_tuple_payload_non_json"),
        _expect_blocked(lambda: module.check_proof_bundle(non_string_payload, roles), "bundle_non_string_payload_key"),
        _expect_blocked(lambda: module.check_proof_bundle(float_payload, roles), "bundle_float_payload_noncanonical"),
    ]
    return {
        "schema": SCHEMA + ".black-box-worker.v1",
        "status": "PASS",
        "method": {
            "loads_exact_pinned_target_module_bytes": True,
            "calls_target_public_checker_functions_as_black_boxes": True,
            "independent_mathematical_implementation": False,
            "dependencies_imported_or_executed_by_worker": False,
        },
        "worker_pin_verification": pin_verification,
        "input_commitment_categories": pair_rows,
        "input_commitment_category_count": len(pair_rows),
        "valid_certificate_variation_count": 2 * len(pair_rows),
        "strict_json_type_cases": type_cases,
        "strict_json_type_case_count": len(type_cases),
        "strict_json_type_cases_rejected": len(type_cases),
        "formal_credit": 0,
    }


def _run_process(command: Sequence[str], cwd: Path, env: Mapping[str, str]) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(list(command), cwd=os.fspath(cwd), env=dict(env), stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)


def _isolated_environment(root: Path) -> tuple[Path, dict[str, str]]:
    cwd = root / "cwd"
    tmp = root / "tmp"
    pycache = root / "pycache"
    home = root / "home"
    cache = root / "cache"
    for path in (cwd, tmp, pycache, home, cache):
        path.mkdir(mode=0o700)
    env = {
        "PATH": os.environ.get("PATH", "/usr/bin:/bin"),
        "LANG": "C",
        "LC_ALL": "C",
        "TMPDIR": os.fspath(tmp),
        "HOME": os.fspath(home),
        "XDG_CACHE_HOME": os.fspath(cache),
        "PYTHONHASHSEED": "0",
        "PYTHONDONTWRITEBYTECODE": "1",
        "PYTHONPYCACHEPREFIX": os.fspath(pycache),
    }
    return cwd, env


def _regular_files(root: Path) -> list[str]:
    return sorted(
        os.fspath(path.relative_to(root))
        for path in root.rglob("*")
        if path.is_file()
    )


def _run_cli_suite(root: Path, cwd: Path, env: Mapping[str, str], snapshot: Path) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    python = sys.executable
    target = os.fspath(snapshot / TARGET_NAME)

    def passing(mode: str, label: str) -> Any:
        completed = _run_process([python, "-I", "-B", target, mode], cwd, env)
        need(completed.returncode == 0, label + " rc0")
        need(completed.stderr == b"", label + " empty stderr")
        return strict_json_load(completed.stdout, label)

    contract = passing("--print-contract", "print-contract")
    self_test = passing("--self-test", "self-test")
    dependency = passing("--verify-dependencies", "verify-dependencies")
    blocked_modes = [
        [],
        ["--unknown"],
        ["--produce"],
        ["--candidate-output"],
        ["--candidate-output", os.fspath(root / "must-not-exist")],
    ]
    blocked_rows = []
    for args in blocked_modes:
        completed = _run_process([python, "-I", "-B", target, *args], cwd, env)
        need(completed.returncode == 1 and completed.stdout == b"" and completed.stderr == b"", "blocked CLI exact silent rc1")
        blocked_rows.append({"argv_shape": "EMPTY" if not args else args[0], "rc": 1, "stdout_bytes": 0, "stderr_bytes": 0})
    return contract, self_test, dependency, {
        "public_pass_modes": ["--print-contract", "--self-test", "--verify-dependencies"],
        "public_pass_mode_count": 3,
        "blocked_mode_cases": blocked_rows,
        "blocked_mode_case_count": len(blocked_rows),
        "isolated_cwd": True,
        "isolated_tmp": True,
        "isolated_home_and_cache": True,
        "read_only_exact_three_file_snapshot": True,
        "python_isolated_flag": True,
        "python_no_bytecode_flag": True,
    }


def _validate_target_receipts(contract: Any, self_test: Any, dependency: Any) -> None:
    need(type(contract) is dict and set(contract) == {"contract", "canonical_contract_digest_sha256"}, "contract envelope")
    need(contract["canonical_contract_digest_sha256"] == TARGET_CONTRACT_SHA256, "contract digest")
    need(object_sha256(contract["contract"]) == TARGET_CONTRACT_SHA256, "contract independent rehash")
    document = contract["contract"]
    need(document["schema"] == TARGET_SCHEMA and document["sealed_exact"] is True, "contract schema/seal")
    need(document["status"] == "PASS_EXACT_EXECUTABLE_CHECKER_FOUNDATION__ZERO_FORMAL_THEOREM_CREDIT", "contract status")
    need(all(type(value) is int and value == 0 for value in document["formal_credit"].values()), "contract exact zero credits")
    need(document["scope"]["formal_credit_minted"] is False and document["scope"]["CM2_credit_minted"] is False, "contract no credit")
    need(document["downstream_state"] == {"B1A": "BLOCKED", "B2": "NOT_AUTHORIZED", "CM2": "NO-GO_FOR_CLAIM", "D02": "BLOCKED"}, "downstream state")

    need(self_test["status"] == "PASS" and self_test["formal_credit"] == 0 and type(self_test["formal_credit"]) is int, "self-test status")
    need(self_test["adversarial_certificate_count"] == self_test["adversarial_certificates_rejected"] == 25, "25 built-ins")
    need(self_test["contract_mutation_count"] == self_test["contract_mutations_rejected"] == 13, "13 mutations")
    positive = self_test["positive_mechanical_checks"]
    need(positive["entry_snapshot_mutation_regressions"] == 2, "entry snapshot regressions")
    need(positive["canonical_input_bound_results"] == 9, "built-in input-bound results")
    need(positive["distinct_certificate_digest_pairs"] == 2, "built-in distinct digest pairs")
    need(all(value == 0 for value in self_test["filesystem_and_output_boundary_call_counts"].values()), "self-test boundary counts")

    need(dependency["status"] == "PASS" and dependency["formal_credit"] == 0 and type(dependency["formal_credit"]) is int, "dependency receipt")
    need(dependency["pin_count"] == 2 and dependency["pin_set_sha256"] == TARGET_PIN_SET_SHA256, "target direct pins")
    body = {key: deepcopy(value) for key, value in dependency.items() if key != "verification_digest_sha256"}
    need(dependency["verification_digest_sha256"] == object_sha256(body) == TARGET_DEPENDENCY_VERIFICATION_SHA256, "dependency receipt rehash")


def _open_runtime_verifier_source() -> tuple[int, os.stat_result, Path, bytes, dict[str, Any]]:
    path = Path(__file__).absolute()
    before = os.stat(path, follow_symlinks=False)
    need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1, "runtime verifier path metadata")
    fd = os.open(os.fspath(path), os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0))
    try:
        held = os.fstat(fd)
        need(_fingerprint(before) == _fingerprint(held), "runtime verifier open race")
        size1, hash1 = _hash_fd(fd)
        need(_fingerprint(os.fstat(fd)) == _fingerprint(held), "runtime verifier pass1 race")
        size2, hash2 = _hash_fd(fd)
        need(_fingerprint(os.fstat(fd)) == _fingerprint(held), "runtime verifier pass2 race")
        os.lseek(fd, 0, os.SEEK_SET)
        raw = bytearray()
        while True:
            block = os.read(fd, 1 << 20)
            if not block:
                break
            raw.extend(block)
        need(_fingerprint(os.stat(path, follow_symlinks=False)) == _fingerprint(held), "runtime verifier final path identity")
        need(size1 == size2 == len(raw) == held.st_size and hash1 == hash2 == sha256_bytes(bytes(raw)), "runtime verifier two-pass bytes")
    except BaseException:
        os.close(fd)
        raise
    pin = {
        "filename": VERIFIER_NAME,
        "size": size1,
        "sha256": hash1,
        "regular_nlink_one": True,
        "held_fd_two_pass": True,
        "final_path_identity": True,
    }
    return fd, held, path, bytes(raw), pin


def _revalidate_runtime_verifier_source(fd: int, held: os.stat_result, path: Path, pin: Mapping[str, Any]) -> None:
    need(_fingerprint(os.fstat(fd)) == _fingerprint(held), "runtime verifier final held fd")
    size, digest_value = _hash_fd(fd)
    need(_fingerprint(os.fstat(fd)) == _fingerprint(held), "runtime verifier final rehash race")
    need(_fingerprint(os.stat(path, follow_symlinks=False)) == _fingerprint(held), "runtime verifier final source path")
    need(size == pin["size"] and digest_value == pin["sha256"], "runtime verifier final source bytes")


def _verify_runtime_snapshot_copy(snapshot: Path, pin: Mapping[str, Any]) -> None:
    path = snapshot / RUNTIME_SNAPSHOT_NAME
    before = os.stat(path, follow_symlinks=False)
    need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1 and stat.S_IMODE(before.st_mode) == 0o400, "runtime snapshot metadata")
    fd = os.open(os.fspath(path), os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0))
    try:
        held = os.fstat(fd)
        need(_fingerprint(before) == _fingerprint(held), "runtime snapshot open race")
        size1, hash1 = _hash_fd(fd)
        size2, hash2 = _hash_fd(fd)
        need(_fingerprint(os.fstat(fd)) == _fingerprint(held), "runtime snapshot held fd")
        need(_fingerprint(os.stat(path, follow_symlinks=False)) == _fingerprint(held), "runtime snapshot final path")
        need(size1 == size2 == pin["size"] and hash1 == hash2 == pin["sha256"], "runtime snapshot exact bytes")
    finally:
        os.close(fd)


def _build_receipts(
    runtime_fd: int,
    runtime_held: os.stat_result,
    runtime_path: Path,
    runtime_raw: bytes,
    runtime_source_pin: Mapping[str, Any],
) -> dict[str, Any]:
    pre = verify_pins()
    temp_parent = Path("/tmp")
    parent_lstat = os.lstat(temp_parent)
    need(stat.S_ISDIR(parent_lstat.st_mode) and not stat.S_ISLNK(parent_lstat.st_mode), "explicit /tmp directory")
    deliverables_real = BASE.resolve(strict=True)
    root_name = tempfile.mkdtemp(prefix="cm2-k1-independent-", dir=os.fspath(temp_parent))
    root = Path(root_name)
    try:
        root_real = root.resolve(strict=True)
        need(root_real != deliverables_real and deliverables_real not in root_real.parents and root_real not in deliverables_real.parents, "temp outside deliverables")
        cwd, env = _isolated_environment(root)
        snapshot = _materialize_isolated_snapshot(root, runtime_raw, runtime_source_pin)
        contract, self_test, dependency, cli = _run_cli_suite(root, cwd, env, snapshot)
        _validate_target_receipts(contract, self_test, dependency)
        worker_completed = _run_process(
            [sys.executable, "-I", "-B", os.fspath(snapshot / RUNTIME_SNAPSHOT_NAME), "--black-box-worker", os.fspath(snapshot)],
            cwd,
            env,
        )
        need(worker_completed.returncode == 0 and worker_completed.stderr == b"", "black-box worker rc/output")
        worker = strict_json_load(worker_completed.stdout, "black-box worker")
        need(worker["status"] == "PASS" and worker["input_commitment_category_count"] == 7, "seven checker categories")
        need(worker["valid_certificate_variation_count"] == 14, "fourteen valid certificates")
        need(worker["strict_json_type_case_count"] == worker["strict_json_type_cases_rejected"] == 8, "eight external type cases")
        need(worker["formal_credit"] == 0 and type(worker["formal_credit"]) is int, "worker zero credit")
        isolated_files = _regular_files(root)
        expected_snapshot_files = sorted([*("snapshot/" + pin["filename"] for pin in PINS), "snapshot/" + RUNTIME_SNAPSHOT_NAME])
        need(isolated_files == expected_snapshot_files, "isolated execution wrote only exact snapshot files")
        need(all(stat.S_IMODE(os.stat(snapshot / pin["filename"], follow_symlinks=False).st_mode) == 0o400 for pin in PINS), "snapshot files read-only")
        _verify_runtime_snapshot_copy(snapshot, runtime_source_pin)
    finally:
        snapshot_path = root / "snapshot"
        if snapshot_path.exists():
            os.chmod(snapshot_path, 0o700)
        shutil.rmtree(root_name)
    post = verify_pins()
    need(pre == post == worker["worker_pin_verification"], "pre/worker/post pins byte-identical")
    _revalidate_runtime_verifier_source(runtime_fd, runtime_held, runtime_path, runtime_source_pin)
    verifier_pin = {
        **dict(runtime_source_pin),
        "worker_snapshot_filename": RUNTIME_SNAPSHOT_NAME,
        "worker_executed_from_read_only_snapshot": True,
        "worker_snapshot_bytes_equal_source_held_fd": True,
    }

    result = seal_object(
        {
            "schema": SCHEMA + ".result.v1",
            "status": "GO_EXACT_MECHANICAL_CHECKER_FOUNDATION__ZERO_FORMAL_CREDIT",
            "decision": "GO_ONLY_ZERO_CREDIT",
            "target": pre["pins"][0],
            "direct_dependency_count": 2,
            "direct_dependencies": pre["pins"][1:],
            "contract": {
                "canonical_contract_digest_sha256": TARGET_CONTRACT_SHA256,
                "independently_rehashed": True,
                "exact_type_zero_credit": True,
                "downstream_state": {"B1A": "BLOCKED", "B2": "NOT_AUTHORIZED", "D02": "BLOCKED", "CM2": "NO-GO_FOR_CLAIM"},
            },
            "built_in_self_test": {
                "status": "PASS",
                "adversarial_certificates_rejected": 25,
                "adversarial_certificate_count": 25,
                "contract_mutations_rejected": 13,
                "contract_mutation_count": 13,
                "entry_snapshot_mutation_regressions": 2,
                "canonical_input_bound_results": 9,
                "distinct_certificate_digest_pairs": 2,
            },
            "black_box_function_verification": {
                "checker_category_count": 7,
                "valid_certificate_count": 14,
                "every_category_has_distinct_input_commitments": True,
                "every_category_has_distinct_result_digests": True,
                "every_input_commitment_independently_rehashed": True,
                "every_result_digest_independently_rehashed": True,
                "strict_json_type_cases_rejected": 8,
            },
            "method_boundary": {
                "target_module_loaded_for_black_box_function_tests": True,
                "exact_pinned_held_fd_target_bytes_loaded": True,
                "cli_and_worker_run_only_from_read_only_exact_snapshot": True,
                "independent_mathematical_implementation": False,
                "receipt_validation_and_digest_rehash_independent_of_target_helpers": True,
            },
            "resource_boundary": {
                "runtime_or_RSS_upper_bound_for_intermediate_differentiation_substitution_interval_or_atom_work": False,
                "exhaustion_before_checker_return_yields_no_result": True,
                "exhaustion_can_mint_credit": False,
            },
            "formal_credit": deepcopy(ZERO_CREDIT),
        }
    )

    attack_suite = seal_object(
        {
            "schema": SCHEMA + ".attack-suite.v1",
            "status": "PASS_TYPE_AND_VARIATION_CONFORMANCE_ONLY",
            "scope": "TYPE_AND_VARIATION_CONFORMANCE_CASES_ONLY",
            "target_sha256": PINS[0]["sha256"],
            "runtime_verifier": verifier_pin,
            "built_in_conformance": {
                "certificate_cases": 25,
                "certificate_cases_rejected": 25,
                "contract_mutation_cases": 13,
                "contract_mutation_cases_rejected": 13,
                "entry_snapshot_mutation_cases": 2,
                "entry_snapshot_mutation_cases_passed": 2,
            },
            "strict_json_type_cases": worker["strict_json_type_cases"],
            "strict_json_type_case_count": 8,
            "strict_json_type_cases_rejected": 8,
            "valid_input_variation_cases": [
                {
                    "category": row["category"],
                    "valid_certificate_count": row["valid_certificate_count"],
                    "identical_result_summary": row["identical_result_summary"],
                    "distinct_input_commitments": row["distinct_input_commitments"],
                    "distinct_result_digests": row["distinct_result_digests"],
                    "independent_commitment_rehash": row["independent_commitment_rehash"],
                    "independent_result_rehash": row["independent_result_rehash"],
                }
                for row in worker["input_commitment_categories"]
            ],
            "valid_input_variation_category_count": 7,
            "valid_input_variation_certificate_count": 14,
            "raw_case_payloads_recorded": False,
            "formal_credit": 0,
        }
    )

    result_file_sha = sha256_bytes(file_bytes(result))
    attack_file_sha = sha256_bytes(file_bytes(attack_suite))
    verification = seal_object(
        {
            "schema": SCHEMA + ".verification.v1",
            "status": "PASS_INDEPENDENT_RECEIPT__GO_ONLY_ZERO_CREDIT",
            "decision": "GO_ONLY_ZERO_CREDIT",
            "runtime_verifier": verifier_pin,
            "pin_verification": {
                "pre_worker_post_byte_identical": True,
                "pin_count": 3,
                "all_file_fds_open_before_first_hash": True,
                "two_pass_same_fd": True,
                "final_all_pin_path_revalidation_before_any_fd_close": True,
                "symlink_and_hardlink_fail_closed": True,
                "pin_rows_sha256": pre["pin_rows_sha256"],
            },
            "target_cli": {
                **cli,
                "contract_digest_independently_rehashed": True,
                "dependency_verification_digest_independently_rehashed": True,
                "isolated_execution_expected_snapshot_file_count": 4,
                "isolated_execution_unexpected_regular_file_count": 0,
            },
            "black_box_method": worker["method"],
            "black_box_checks": {
                "input_commitment_category_count": 7,
                "valid_certificate_variation_count": 14,
                "strict_json_type_case_count": 8,
                "strict_json_type_cases_rejected": 8,
                "entry_snapshot_regressions_checked_via_pinned_self_test": 2,
                "input_commitment_categories_sha256": object_sha256(worker["input_commitment_categories"]),
            },
            "receipts": {
                "result": {
                    "filename": TARGET_NAME.removesuffix(".py") + "_result.json",
                    "file_sha256": result_file_sha,
                    "object_self_sha256": result["object_self_sha256"],
                },
                "attack_suite": {
                    "filename": TARGET_NAME.removesuffix(".py") + "_attack_suite.json",
                    "file_sha256": attack_file_sha,
                    "object_self_sha256": attack_suite["object_self_sha256"],
                },
            },
            "scope_boundary": {
                "direct_dependency_snapshot_only": True,
                "transitive_dependency_closure_claimed": False,
                "target_loaded_for_black_box_function_tests": True,
                "independent_mathematical_implementation": False,
                "formal_B1A_verified": False,
                "B2_authorized": False,
                "D02_unblocked": False,
                "CM2_claim_authorized": False,
            },
            "resource_boundary": {
                "runtime_or_RSS_upper_bound_for_intermediate_differentiation_substitution_interval_or_atom_work": False,
                "any_exhaustion_before_checker_return_terminates_without_result": True,
                "any_exhaustion_mints_formal_credit": False,
            },
            "formal_credit": deepcopy(ZERO_CREDIT),
        }
    )
    _revalidate_runtime_verifier_source(runtime_fd, runtime_held, runtime_path, runtime_source_pin)
    return {"result": result, "attack_suite": attack_suite, "verification": verification}


def build_receipts() -> dict[str, Any]:
    runtime_fd, runtime_held, runtime_path, runtime_raw, runtime_pin = _open_runtime_verifier_source()
    try:
        return _build_receipts(runtime_fd, runtime_held, runtime_path, runtime_raw, runtime_pin)
    finally:
        os.close(runtime_fd)


def main(argv: Sequence[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if len(args) == 2 and args[0] == "--black-box-worker":
        snapshot = Path(args[1]).absolute()
        print(canonical_bytes(black_box_worker(snapshot)).decode("ascii"))
        return 0
    if args == ["--bundle"]:
        print(canonical_bytes(build_receipts()).decode("ascii"))
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
