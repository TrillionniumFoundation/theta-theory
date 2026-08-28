#!/usr/bin/env python3
"""Fail-close strace audit for the additive C30a audit closure.

The default contract is deliberately pinned to the completed independent
verifier replay in ``.cm2-runtime/audit/c30a-p0-closure-verifier-20260807``.
It does not import or execute the C30a producer or verifier and it never writes
the original thirteen-member seal.

A later controlled-producer replay can use the same analyzer with a canonical
JSON contract (``--contract`` plus ``--expected-contract-sha256``).  A custom
contract must retain the exact schema of ``FIXED_CONTRACT`` and must explicitly
name every output path that the traced process may mutate.

The analyzer distinguishes two statements which must not be conflated:

* no forbidden mutation was *observed* in the supplied trace; and
* the trace collection covered every mutation channel in this contract.

The release-grade PASS requires both.  A selectively collected trace that
omits an fd-only mutation syscall therefore fails closed even when its observed
events are clean.
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
import re
import shlex
import stat
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable


SCHEMA = "cm2.c30a.supplemental.strace-audit.v1"
CONTRACT_SCHEMA = "cm2.c30a.supplemental.strace-audit-contract.v1"

WORKSPACE = Path(
    "/home/qian-qi/.openclaw/workspaces/telegram-bot-8449317572"
)
AUDIT_DIR = WORKSPACE / ".cm2-runtime/audit/c30a-p0-closure-verifier-20260807"
MANIFEST = (
    WORKSPACE
    / "deliverables/cm2_round306c30a_source_w_162_reduced_clipped_delta_"
    "whole_origin_promotion_manifest.sha256"
)
CANDIDATE = WORKSPACE / "deliverables/cm2_round306c30a_sealed"

FIXED_MANIFEST_MEMBERS = {
    "cm2_round306c30a_python_flint_requirements.lock":
        "cd171f53dd8a187b2ef4bd7ad0cc2adbe2082395646c0c57407f4e3514c11f5c",
    "cm2_round306c30a_python_flint_runtime_lock.json":
        "ffe714b67a0aa05d8094033a0d9cc8e10ccafa03157951adf3d64055c98cdc79",
    (
        "cm2_round306c30a_runtime/python_flint-0.9.0-cp310-abi3-"
        "manylinux2014_x86_64.manylinux_2_17_x86_64.whl"
    ): "376b88cacd30612479e839ffdba887599d3f9c8c0e214852bf80bb2b194e4d76",
    (
        "cm2_round306c30a_source_w_162_reduced_clipped_delta_whole_origin_"
        "promotion_attack_harness.py"
    ): "debdb1ac9d3b840660600cec66dd2b6b1d45eb5847d366c989a652f893bb3c17",
    (
        "cm2_round306c30a_source_w_162_reduced_clipped_delta_whole_origin_"
        "promotion_cold_replay.md"
    ): "6bac45a8150603370380afca729220fc2c6da9e3d3580ea3b535b9d2b37a94c5",
    (
        "cm2_round306c30a_source_w_162_reduced_clipped_delta_whole_origin_"
        "promotion_independent_verifier.py"
    ): "5af75a97e9c306cc47a514e4c87ae875a8388bb75d9274d106b64e2ceee87c7c",
    (
        "cm2_round306c30a_source_w_162_reduced_clipped_delta_whole_origin_"
        "promotion_producer.py"
    ): "41a3f11c3e44bdbbfcf95edf88902669365186e6fb6394aaee15a6846dc91714",
    (
        "cm2_round306c30a_source_w_162_reduced_clipped_delta_whole_origin_"
        "promotion_report.md"
    ): "e2811b8c9a676e08e1e3014a10ca693ee651f4d143b38540a1ac53195f4b8562",
    (
        "cm2_round306c30a_source_w_162_reduced_clipped_delta_whole_origin_"
        "promotion_verification.json"
    ): "f02f7e3144541284819947c549ce91d8f1d6e9df24c0bdb4b981077f1e358d07",
    (
        "cm2_round306c30a_sealed/cm2_round306c30a_source_w_162_reduced_"
        "clipped_delta_whole_origin_promotion_cell_ledger.jsonl.gz"
    ): "c4c0061a08983471428b2e5113aff60bbeccc67530cac691658a6bbad1ce9904",
    (
        "cm2_round306c30a_sealed/cm2_round306c30a_source_w_162_reduced_"
        "clipped_delta_whole_origin_promotion_inherited_h_obstruction_"
        "ledger.jsonl.gz"
    ): "f86c6c3d90a4a87c7d4366b86a0e8119d019cbf86f5b5ab781140605ddc1e80e",
    (
        "cm2_round306c30a_sealed/cm2_round306c30a_source_w_162_reduced_"
        "clipped_delta_whole_origin_promotion_result.json"
    ): "521be2aefebea96d6a3d2ce1bcf0234753ef69af7182a4e47a0d22d686df6c48",
    (
        "cm2_round306c30a_sealed/cm2_round306c30a_source_w_162_reduced_"
        "clipped_delta_whole_origin_promotion_whole_origin_ledger.jsonl.gz"
    ): "778995522629a362183159420860b65d60c8719bc1453c4fc2657e8e8fba9649",
}

FIXED_CANDIDATE_MEMBERS = {
    Path(name).name: digest
    for name, digest in FIXED_MANIFEST_MEMBERS.items()
    if name.startswith("cm2_round306c30a_sealed/")
}

FIXED_CANDIDATE_MANIFEST_BINDINGS = {
    Path(relative).name: relative
    for relative in FIXED_MANIFEST_MEMBERS
    if relative.startswith("cm2_round306c30a_sealed/")
}

FIXED_STDOUT_OBJECT = {
    "cell_rows": 12888,
    "held_origin_rows": 2,
    "promoted_origin_keys_sha256":
        "df619f757a7176b1cea40af96944387f21e18fa249ca14c07af61c2d8092ab0e",
    "result_sha256":
        "32c449bc9af41a22ab5468d194431d14fadf5bc95b30067d639f9e4443538e09",
    "runtime": {
        "flint": "3.6.0",
        "python": "3.12.3",
        "python_flint": "0.9.0",
    },
    "status": (
        "PASS_INDEPENDENT_C30A_12888_CELL_ROWS__160_WHOLE_ORIGIN_ROWS__"
        "2_INHERITED_H_HOLDS_RECONSTRUCTED__252_TO_92_TRANSITION_VERIFIED__"
        "D02_BOUNDARY_PRESERVED"
    ),
    "total_rows": 13050,
    "whole_origin_rows": 160,
}

# ``%file`` covers pathname-taking variants.  These fd-only or indirect
# channels must be named explicitly when strace is selectively filtered.
# mmap+msync are required because a MAP_SHARED|PROT_WRITE mapping can mutate a
# regular file without a write(2).  io_uring_enter is required and any observed
# invocation is rejected because the SQEs are not represented by ordinary
# strace argument decoding.
REQUIRED_EXPLICIT_CAPTURE_SYSCALLS = sorted({
    "copy_file_range",
    "fallocate",
    "fchmod",
    "fchown",
    "fdatasync",
    "fremovexattr",
    "fsetxattr",
    "fsync",
    "ftruncate",
    "io_uring_enter",
    "mmap",
    "msync",
    "pwrite64",
    "pwritev",
    "pwritev2",
    "sendfile",
    "splice",
    "sync",
    "sync_file_range",
    "syncfs",
    "tee",
    "vmsplice",
    "write",
    "writev",
})

FIXED_CONTRACT: dict[str, Any] = {
    "schema": CONTRACT_SCHEMA,
    "profile": "c30a-independent-verifier-scrubbed-replay-20260807",
    "workspace": str(WORKSPACE),
    "paths": {
        "trace": str(AUDIT_DIR / "trace.log"),
        "stdout": str(AUDIT_DIR / "stdout.json"),
        "stderr": str(AUDIT_DIR / "stderr.log"),
        "time": str(AUDIT_DIR / "time.txt"),
        "manifest": str(MANIFEST),
        "candidate_dir": str(CANDIDATE),
    },
    "pins": {
        "trace_sha256":
            "f607f46c1f646f449476e2e73d9c059f43a55b88aeae8774703ee6eb9c312dfb",
        "stdout_sha256":
            "ffb47cda5d7473b07160ef9824c316523f56b2c069af18c06886e4ef4a7e538f",
        "stderr_sha256":
            "addac86a8584f1a097ddf37a779e30f2c573657e7323c9494dc0429b4504f7bf",
        "time_sha256":
            "763b6a072570eb5f4b153f0bdb2b1e1468ece301536e895c47937c31d0ecf15b",
        "manifest_sha256":
            "0f3e80d54d4307eccf509435470213e19fd4eefffc43b95e01cec0d3b8a094bc",
    },
    "manifest_members": FIXED_MANIFEST_MEMBERS,
    "candidate_members": FIXED_CANDIDATE_MEMBERS,
    "candidate_manifest_bindings": FIXED_CANDIDATE_MANIFEST_BINDINGS,
    "stdout": {
        "policy": "one-canonical-json-write",
        "expected_object": FIXED_STDOUT_OBJECT,
    },
    "stderr": {
        "policy": "c30a-round215-diagnostics",
        "expected_line_count": 50,
    },
    "allowed_write_paths": [],
    "protected_roots": [
        str(WORKSPACE / "deliverables"),
        str(CANDIDATE),
        str(WORKSPACE / ".cm2-runtime/python-flint-0.9.0"),
        str(WORKSPACE / ".cm2-runtime/candidates"),
    ],
    "capture": {
        "require_follow_forks": True,
        "require_fd_path_decoding": True,
        "require_percent_file": True,
        "minimum_string_limit": 4096,
        "required_explicit_syscalls": REQUIRED_EXPLICIT_CAPTURE_SYSCALLS,
    },
}


class AuditFailure(Exception):
    """Fatal malformed-input error."""


@dataclass(frozen=True)
class CapturedFile:
    path: str
    data: bytes
    sha256: str
    size: int
    stat_tuple: tuple[int, ...]


@dataclass(frozen=True)
class TraceCall:
    line_number: int
    pid: int
    name: str
    args_text: str
    args: tuple[str, ...]
    result_text: str
    result_integer: int | None
    raw: str


def canonical_bytes(value: Any) -> bytes:
    return (
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
        + "\n"
    ).encode("utf-8")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def reject_duplicate_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise AuditFailure(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def load_json_strict(data: bytes, label: str) -> Any:
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise AuditFailure(f"{label}: non-UTF-8 JSON") from exc
    try:
        return json.loads(text, object_pairs_hook=reject_duplicate_pairs)
    except (json.JSONDecodeError, AuditFailure) as exc:
        raise AuditFailure(f"{label}: invalid strict JSON: {exc}") from exc


def normalized_absolute(path: str | Path, workspace: Path) -> str:
    raw = os.fspath(path)
    if not os.path.isabs(raw):
        raw = os.path.join(os.fspath(workspace), raw)
    return os.path.normpath(raw)


def stat_identity(st: os.stat_result) -> tuple[int, ...]:
    return (
        st.st_dev,
        st.st_ino,
        st.st_mode,
        st.st_nlink,
        st.st_uid,
        st.st_gid,
        st.st_size,
        st.st_mtime_ns,
        st.st_ctime_ns,
    )


def ensure_no_symlink_chain(path: Path) -> None:
    absolute = Path(os.path.abspath(path))
    parts = absolute.parts
    current = Path(parts[0])
    for part in parts[1:]:
        current /= part
        st = os.lstat(current)
        if stat.S_ISLNK(st.st_mode):
            raise AuditFailure(f"symlink path component rejected: {current}")


def capture_regular(path: Path) -> CapturedFile:
    ensure_no_symlink_chain(path)
    flags = os.O_RDONLY | os.O_CLOEXEC
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    fd = os.open(path, flags)
    try:
        before = os.fstat(fd)
        if not stat.S_ISREG(before.st_mode):
            raise AuditFailure(f"not a regular file: {path}")
        if before.st_nlink != 1:
            raise AuditFailure(f"nlink != 1: {path}")
        chunks: list[bytes] = []
        while True:
            chunk = os.read(fd, 1024 * 1024)
            if not chunk:
                break
            chunks.append(chunk)
        after = os.fstat(fd)
        if stat_identity(before) != stat_identity(after):
            raise AuditFailure(f"metadata race while reading: {path}")
        data = b"".join(chunks)
        if len(data) != before.st_size:
            raise AuditFailure(f"size race while reading: {path}")
        return CapturedFile(
            path=os.path.abspath(path),
            data=data,
            sha256=sha256_bytes(data),
            size=len(data),
            stat_tuple=stat_identity(before),
        )
    finally:
        os.close(fd)


def capture_directory_names(path: Path) -> tuple[list[str], tuple[int, ...]]:
    ensure_no_symlink_chain(path)
    flags = os.O_RDONLY | os.O_CLOEXEC | os.O_DIRECTORY
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    fd = os.open(path, flags)
    try:
        before = os.fstat(fd)
        if not stat.S_ISDIR(before.st_mode):
            raise AuditFailure(f"not a directory: {path}")
        names = sorted(os.listdir(fd))
        after = os.fstat(fd)
        if stat_identity(before) != stat_identity(after):
            raise AuditFailure(f"directory race while listing: {path}")
        return names, stat_identity(before)
    finally:
        os.close(fd)


def validate_contract_shape(contract: dict[str, Any]) -> None:
    expected_top = {
        "schema",
        "profile",
        "workspace",
        "paths",
        "pins",
        "manifest_members",
        "candidate_members",
        "candidate_manifest_bindings",
        "stdout",
        "stderr",
        "allowed_write_paths",
        "protected_roots",
        "capture",
    }
    if set(contract) != expected_top:
        raise AuditFailure(
            "contract top-level keys differ: "
            f"missing={sorted(expected_top - set(contract))}, "
            f"extra={sorted(set(contract) - expected_top)}"
        )
    if contract["schema"] != CONTRACT_SCHEMA:
        raise AuditFailure("contract schema mismatch")
    expected_paths = {"trace", "stdout", "stderr", "time", "manifest", "candidate_dir"}
    if set(contract["paths"]) != expected_paths:
        raise AuditFailure("contract paths keys differ")
    expected_pins = {f"{name}_sha256" for name in ("trace", "stdout", "stderr", "time", "manifest")}
    if set(contract["pins"]) != expected_pins:
        raise AuditFailure("contract pins keys differ")
    for digest in contract["pins"].values():
        if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
            raise AuditFailure("contract contains a malformed SHA-256 pin")
    if contract["stdout"].get("policy") != "one-canonical-json-write":
        raise AuditFailure("unsupported stdout policy")
    if contract["stderr"].get("policy") not in {
        "empty",
        "pinned-bytes",
        "c30a-round215-diagnostics",
    }:
        raise AuditFailure("unsupported stderr policy")
    if contract["capture"].get("stream_transport", "path-redirection") not in {
        "path-redirection",
        "docker-attach-pipe",
    }:
        raise AuditFailure("unsupported traced stream transport")
    candidate_names = set(contract["candidate_members"])
    if set(contract["candidate_manifest_bindings"]) != candidate_names:
        raise AuditFailure("candidate manifest-binding keys differ")
    for candidate_name, manifest_relative in contract["candidate_manifest_bindings"].items():
        if Path(candidate_name).name != candidate_name:
            raise AuditFailure("candidate member is not a basename")
        if manifest_relative not in contract["manifest_members"]:
            raise AuditFailure("candidate binding names an absent manifest member")
        if (
            contract["candidate_members"][candidate_name]
            != contract["manifest_members"][manifest_relative]
        ):
            raise AuditFailure("candidate binding SHA differs from manifest SHA")


def load_contract(args: argparse.Namespace) -> tuple[dict[str, Any], str, str]:
    if args.contract is None:
        contract = json.loads(json.dumps(FIXED_CONTRACT))
        digest = sha256_bytes(canonical_bytes(contract))
        return contract, "embedded-fixed-contract", digest
    if args.expected_contract_sha256 is None:
        raise AuditFailure("custom contract requires --expected-contract-sha256")
    captured = capture_regular(args.contract)
    if captured.sha256 != args.expected_contract_sha256:
        raise AuditFailure("custom contract SHA-256 mismatch")
    contract = load_json_strict(captured.data, "custom contract")
    if not isinstance(contract, dict):
        raise AuditFailure("custom contract must be a JSON object")
    if captured.data != canonical_bytes(contract):
        raise AuditFailure("custom contract is not canonical JSON plus one newline")
    return contract, captured.path, captured.sha256


def parse_manifest(data: bytes) -> dict[str, str]:
    try:
        text = data.decode("ascii")
    except UnicodeDecodeError as exc:
        raise AuditFailure("manifest is not ASCII") from exc
    if not text.endswith("\n"):
        raise AuditFailure("manifest lacks final newline")
    result: dict[str, str] = {}
    for line_number, line in enumerate(text.splitlines(), 1):
        match = re.fullmatch(r"([0-9a-f]{64})  ([^\x00\r\n]+)", line)
        if match is None:
            raise AuditFailure(f"malformed manifest line {line_number}")
        digest, relative = match.groups()
        rel_path = Path(relative)
        if rel_path.is_absolute() or relative in {"", "."} or ".." in rel_path.parts:
            raise AuditFailure(f"unsafe manifest member: {relative}")
        if relative in result:
            raise AuditFailure(f"duplicate manifest member: {relative}")
        result[relative] = digest
    return result


def split_top_level_args(text: str) -> tuple[str, ...]:
    parts: list[str] = []
    start = 0
    quote = False
    escape = False
    depth = 0
    for index, char in enumerate(text):
        if quote:
            if escape:
                escape = False
            elif char == "\\":
                escape = True
            elif char == '"':
                quote = False
            continue
        if char == '"':
            quote = True
        elif char in "([{":
            depth += 1
        elif char in ")]}":
            depth -= 1
            if depth < 0:
                raise AuditFailure("unbalanced strace syscall arguments")
        elif char == "," and depth == 0:
            parts.append(text[start:index].strip())
            start = index + 1
    if quote or depth != 0:
        raise AuditFailure("unterminated strace syscall arguments")
    parts.append(text[start:].strip())
    return tuple(parts)


TRACE_LINE_RE = re.compile(
    r"^(?:\[pid\s+)?(?P<pid>[0-9]+)(?:\]\s+|\s+)"
    r"(?P<name>[A-Za-z0-9_]+)\((?P<args>.*)\)\s+=\s+(?P<result>.+)$"
)


def parse_trace(data: bytes) -> list[TraceCall]:
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise AuditFailure("trace is not UTF-8") from exc
    if not text.endswith("\n"):
        raise AuditFailure("trace lacks final newline")
    calls: list[TraceCall] = []
    for line_number, raw in enumerate(text.splitlines(), 1):
        if "<unfinished ...>" in raw or "resumed>" in raw:
            raise AuditFailure(f"unfinished/resumed syscall at trace line {line_number}")
        match = TRACE_LINE_RE.fullmatch(raw)
        if match is None:
            raise AuditFailure(f"unparsed trace line {line_number}: {raw[:160]}")
        result_text = match.group("result")
        integer_match = re.match(r"(-?[0-9]+)(?:<[^>]*>)?", result_text)
        result_integer = int(integer_match.group(1)) if integer_match else None
        calls.append(
            TraceCall(
                line_number=line_number,
                pid=int(match.group("pid")),
                name=match.group("name"),
                args_text=match.group("args"),
                args=split_top_level_args(match.group("args")),
                result_text=result_text,
                result_integer=result_integer,
                raw=raw,
            )
        )
    if not calls:
        raise AuditFailure("trace is empty")
    return calls


FD_RE = re.compile(r"^(?P<fd>-?[0-9]+)(?:<(?P<target>[^>]*)>)?")


def parse_fd(token: str) -> tuple[int, str | None]:
    match = FD_RE.match(token)
    if match is None:
        raise AuditFailure(f"unparsed fd token: {token}")
    return int(match.group("fd")), match.group("target")


def decode_c_string(token: str) -> bytes:
    if not token.startswith('"') or not token.endswith('"'):
        raise AuditFailure(f"expected complete strace string, got: {token[:120]}")
    try:
        value = ast.literal_eval(token)
    except (SyntaxError, ValueError) as exc:
        raise AuditFailure("cannot decode strace string literal") from exc
    if not isinstance(value, str):
        raise AuditFailure("strace string literal did not decode to text")
    try:
        return value.encode("latin-1")
    except UnicodeEncodeError:
        return value.encode("utf-8")


def normalize_trace_target(target: str | None, workspace: Path) -> str | None:
    if target is None:
        return None
    if target.startswith("/"):
        return normalized_absolute(target, workspace)
    return target


def path_within(path: str, root: str) -> bool:
    if not path.startswith("/") or not root.startswith("/"):
        return False
    try:
        return os.path.commonpath((path, root)) == root
    except ValueError:
        return False


def quoted_strings(token: str) -> list[str]:
    values: list[str] = []
    for match in re.finditer(r'"(?:\\.|[^"\\])*"', token):
        values.append(decode_c_string(match.group(0)).decode("utf-8", "surrogateescape"))
    return values


def dirfd_base(token: str, workspace: Path) -> str | None:
    annotation = re.search(r"<([^>]*)>", token)
    if annotation and annotation.group(1).startswith("/"):
        return normalized_absolute(annotation.group(1), workspace)
    if token.startswith("AT_FDCWD"):
        return str(workspace)
    return None


def resolve_path_arg(
    token: str,
    workspace: Path,
    base_token: str | None = None,
) -> str | None:
    strings = quoted_strings(token)
    if len(strings) != 1:
        return None
    raw = strings[0]
    if os.path.isabs(raw):
        return normalized_absolute(raw, workspace)
    base = str(workspace) if base_token is None else dirfd_base(base_token, workspace)
    if base is None:
        return None
    return normalized_absolute(os.path.join(base, raw), workspace)


PATH_MUTATOR_INDEXES: dict[str, tuple[tuple[int | None, int], ...]] = {
    "creat": ((None, 0),),
    "truncate": ((None, 0),),
    "rename": ((None, 0), (None, 1)),
    "renameat": ((0, 1), (2, 3)),
    "renameat2": ((0, 1), (2, 3)),
    "unlink": ((None, 0),),
    "unlinkat": ((0, 1),),
    "link": ((None, 0), (None, 1)),
    "linkat": ((0, 1), (2, 3)),
    "symlink": ((None, 1),),
    "symlinkat": ((1, 2),),
    "mkdir": ((None, 0),),
    "mkdirat": ((0, 1),),
    "rmdir": ((None, 0),),
    "chmod": ((None, 0),),
    "fchmodat": ((0, 1),),
    "fchmodat2": ((0, 1),),
    "chown": ((None, 0),),
    "lchown": ((None, 0),),
    "fchownat": ((0, 1),),
    "utime": ((None, 0),),
    "utimes": ((None, 0),),
    "lutimes": ((None, 0),),
    "futimesat": ((0, 1),),
    "utimensat": ((0, 1),),
    "setxattr": ((None, 0),),
    "lsetxattr": ((None, 0),),
    "removexattr": ((None, 0),),
    "lremovexattr": ((None, 0),),
    "mknod": ((None, 0),),
    "mknodat": ((0, 1),),
    "mkfifo": ((None, 0),),
    "mkfifoat": ((0, 1),),
}

FD_MUTATOR_INDEXES = {
    "write": 0,
    "writev": 0,
    "pwrite64": 0,
    "pwritev": 0,
    "pwritev2": 0,
    "ftruncate": 0,
    "fallocate": 0,
    "fchmod": 0,
    "fchown": 0,
    "fsetxattr": 0,
    "fremovexattr": 0,
    "fsync": 0,
    "fdatasync": 0,
    "syncfs": 0,
    "sync_file_range": 0,
    "sendfile": 0,
    "sendfile64": 0,
    "copy_file_range": 3,
    "splice": 3,
    "tee": 2,
    "vmsplice": 0,
}

WRITE_OPEN_FLAGS = {
    "O_WRONLY",
    "O_RDWR",
    "O_CREAT",
    "O_TRUNC",
    "O_APPEND",
    "O_TMPFILE",
}


def open_mutation_path(call: TraceCall, workspace: Path) -> tuple[bool, str | None]:
    if call.name == "open" and len(call.args) >= 2:
        path_index, flags_index, base_index = 0, 1, None
    elif call.name in {"openat", "openat2"} and len(call.args) >= 3:
        path_index, flags_index, base_index = 1, 2, 0
    else:
        return False, None
    flags = call.args[flags_index]
    if not any(flag in flags for flag in WRITE_OPEN_FLAGS):
        return False, None
    base_token = call.args[base_index] if base_index is not None else None
    return True, resolve_path_arg(call.args[path_index], workspace, base_token)


def path_mutation_targets(call: TraceCall, workspace: Path) -> list[str | None]:
    spec = PATH_MUTATOR_INDEXES.get(call.name)
    if spec is None:
        return []
    targets: list[str | None] = []
    for base_index, path_index in spec:
        if path_index >= len(call.args):
            targets.append(None)
            continue
        base = call.args[base_index] if base_index is not None and base_index < len(call.args) else None
        targets.append(resolve_path_arg(call.args[path_index], workspace, base))
    return targets


def fd_mutation_target(call: TraceCall, workspace: Path) -> tuple[int, str | None] | None:
    index = FD_MUTATOR_INDEXES.get(call.name)
    if index is None:
        return None
    if index >= len(call.args):
        return -1, None
    fd, target = parse_fd(call.args[index])
    return fd, normalize_trace_target(target, workspace)


def parse_time_command(data: bytes) -> tuple[str, list[str], int]:
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise AuditFailure("time report is not UTF-8") from exc
    if not text.endswith("\n"):
        raise AuditFailure("time report lacks final newline")
    signal_lines = re.findall(
        r"^\s*Command terminated by signal\s+([^\r\n]+)\s*$",
        text,
        re.MULTILINE,
    )
    if signal_lines:
        raise AuditFailure(
            "time report records signal termination: " + repr(signal_lines)
        )
    exit_matches = re.findall(r"^\s*Exit status:\s*([0-9]+)\s*$", text, re.MULTILINE)
    if exit_matches != ["0"]:
        raise AuditFailure(f"time report does not prove exactly one exit status 0: {exit_matches}")
    command_lines = [
        line.strip()
        for line in text.splitlines()
        if line.lstrip().startswith("Command being timed:")
    ]
    if len(command_lines) != 1:
        raise AuditFailure("time report does not contain exactly one command line")
    encoded = command_lines[0].split(":", 1)[1].strip()
    try:
        command = ast.literal_eval(encoded)
    except (SyntaxError, ValueError) as exc:
        raise AuditFailure("cannot decode time command") from exc
    if not isinstance(command, str):
        raise AuditFailure("time command is not a string")
    argv = shlex.split(command)
    if not argv:
        raise AuditFailure("empty time command")
    return command, argv, 0


def parse_trace_filter(argv: list[str]) -> tuple[set[str], int, str | None, dict[str, bool]]:
    tokens: set[str] = set()
    string_limit = -1
    output_path: str | None = None
    flags = {"follow_forks": False, "fd_paths": False}
    # Parse only strace's own option prefix.  The traced command may itself
    # contain flags such as Python's ``-s``; treating those as strace options
    # would either corrupt the capture contract or raise while parsing ``-B``.
    index = 1
    while index < len(argv):
        value = argv[index]
        if value == "--":
            break
        if not value.startswith("-"):
            break
        if value in {"-f", "--follow-forks"}:
            flags["follow_forks"] = True
        elif value in {"-y", "-yy", "--decode-fds", "--decode-fds=all"}:
            # Only -yy (or decode-fds=all) supplies pathname targets reliably.
            flags["fd_paths"] = value in {"-yy", "--decode-fds=all"}
        elif value in {"-s", "--string-limit"} and index + 1 < len(argv):
            index += 1
            string_limit = int(argv[index])
        elif value.startswith("-s") and value[2:].isdigit():
            string_limit = int(value[2:])
        elif value in {"-o", "--output"} and index + 1 < len(argv):
            index += 1
            output_path = argv[index]
        elif value.startswith("--output="):
            output_path = value.split("=", 1)[1]
        elif value == "-e" and index + 1 < len(argv):
            index += 1
            expression = argv[index]
            if expression.startswith("trace="):
                tokens.update(filter(None, expression[6:].split(",")))
        elif value.startswith("--trace="):
            tokens.update(filter(None, value.split("=", 1)[1].split(",")))
        index += 1
    return tokens, string_limit, output_path, flags


def validate_round215_stderr(data: bytes) -> dict[str, Any]:
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise AuditFailure("stderr is not UTF-8") from exc
    if not text.endswith("\n"):
        raise AuditFailure("diagnostic stderr lacks final newline")
    lines = text.splitlines()
    expected_progress = ["Round215 replay frozen source-W frontier"]
    expected_progress += [
        f"Round215 exact-behind origins {number}/596"
        for number in [*range(20, 600, 20), 596]
    ]
    if lines[: len(expected_progress)] != expected_progress:
        raise AuditFailure("Round215 exact-behind diagnostic progression differs")
    cursor = len(expected_progress)
    diagnostic_prefixes = [
        "Round215 reconstruction diagnostic ",
        "Round215 compact outer diagnostic ",
        "Round215 global generalized diagnostic ",
    ]

    def consume_canonical_diagnostic(prefix: str) -> None:
        nonlocal cursor
        if cursor >= len(lines) or not lines[cursor].startswith(prefix):
            raise AuditFailure(f"missing stderr diagnostic: {prefix.rstrip()}")
        payload_text = lines[cursor][len(prefix):]
        payload = load_json_strict(payload_text.encode("utf-8"), prefix.rstrip())
        if payload_text.encode("utf-8") + b"\n" != canonical_bytes(payload):
            raise AuditFailure(f"noncanonical stderr diagnostic: {prefix.rstrip()}")
        cursor += 1

    consume_canonical_diagnostic(diagnostic_prefixes[0])
    compact_progress = [
        f"Round215 compact outer audit {number}/54"
        for number in [10, 20, 30, 40, 50, 54]
    ]
    if lines[cursor: cursor + len(compact_progress)] != compact_progress:
        raise AuditFailure("Round215 compact diagnostic progression differs")
    cursor += len(compact_progress)
    consume_canonical_diagnostic(diagnostic_prefixes[1])
    consume_canonical_diagnostic(diagnostic_prefixes[2])
    algebraic_progress = [
        f"Round215 algebraic cells origins {number}/198"
        for number in [*range(20, 200, 20), 198]
    ]
    if lines[cursor:] != algebraic_progress:
        raise AuditFailure("Round215 algebraic diagnostic progression differs")
    return {
        "diagnostic_line_count": len(lines),
        "embedded_canonical_json_diagnostic_count": 3,
        "policy": "c30a-round215-diagnostics",
    }


def artifact_record(captured: CapturedFile, expected_sha256: str) -> dict[str, Any]:
    return {
        "path": captured.path,
        "sha256": captured.sha256,
        "size": captured.size,
        "matches_pin": captured.sha256 == expected_sha256,
    }


def audit(contract: dict[str, Any], contract_source: str, contract_sha256: str) -> dict[str, Any]:
    validate_contract_shape(contract)
    workspace = Path(contract["workspace"])
    if not workspace.is_absolute():
        raise AuditFailure("workspace must be absolute")
    paths = {name: Path(value) for name, value in contract["paths"].items()}
    for name, path in paths.items():
        if not path.is_absolute():
            raise AuditFailure(f"contract path is not absolute: {name}")
        if normalized_absolute(path, workspace) != str(path):
            raise AuditFailure(f"contract path is not lexically canonical: {name}")

    captured = {
        name: capture_regular(paths[name])
        for name in ("trace", "stdout", "stderr", "time", "manifest")
    }
    errors: list[str] = []
    artifacts: dict[str, Any] = {}
    for name, item in captured.items():
        expected = contract["pins"][f"{name}_sha256"]
        artifacts[name] = artifact_record(item, expected)
        if item.sha256 != expected:
            errors.append(f"{name.upper()}_SHA256_PIN_MISMATCH")

    manifest_map = parse_manifest(captured["manifest"].data)
    if manifest_map != contract["manifest_members"]:
        errors.append("MANIFEST_EXACT_MAP_MISMATCH")
    manifest_member_records: dict[str, dict[str, Any]] = {}
    if manifest_map == contract["manifest_members"]:
        for relative, expected_sha256 in manifest_map.items():
            member = capture_regular(paths["manifest"].parent / relative)
            manifest_member_records[relative] = artifact_record(member, expected_sha256)
            if member.sha256 != expected_sha256:
                errors.append(f"MANIFEST_MEMBER_SHA256_MISMATCH:{relative}")

    candidate_names, candidate_stat = capture_directory_names(paths["candidate_dir"])
    expected_candidate = contract["candidate_members"]
    if candidate_names != sorted(expected_candidate):
        errors.append("CANDIDATE_EXACT_MEMBER_MAP_MISMATCH")
    for name, expected_sha256 in expected_candidate.items():
        relative = contract["candidate_manifest_bindings"][name]
        record = manifest_member_records.get(relative)
        if record is None or record["sha256"] != expected_sha256:
            errors.append(f"CANDIDATE_MEMBER_NOT_BOUND_TO_MANIFEST:{name}")

    stdout_object = load_json_strict(captured["stdout"].data, "stdout")
    stdout_canonical = captured["stdout"].data == canonical_bytes(stdout_object)
    if not stdout_canonical:
        errors.append("STDOUT_NOT_ONE_CANONICAL_JSON_LINE")
    if stdout_object != contract["stdout"]["expected_object"]:
        errors.append("STDOUT_OBJECT_MISMATCH")

    stderr_policy = contract["stderr"]["policy"]
    stderr_semantics: dict[str, Any]
    if stderr_policy == "empty":
        stderr_semantics = {"policy": "empty", "diagnostic_line_count": 0}
        if captured["stderr"].data:
            errors.append("STDERR_EXPECTED_EMPTY")
    elif stderr_policy == "pinned-bytes":
        stderr_semantics = {
            "policy": "pinned-bytes",
            "diagnostic_line_count": len(captured["stderr"].data.splitlines()),
        }
    else:
        stderr_semantics = validate_round215_stderr(captured["stderr"].data)
        if stderr_semantics["diagnostic_line_count"] != contract["stderr"]["expected_line_count"]:
            errors.append("STDERR_DIAGNOSTIC_LINE_COUNT_MISMATCH")

    time_command, time_argv, exit_status = parse_time_command(captured["time"].data)
    if "strace" not in os.path.basename(time_argv[0]):
        errors.append("TIME_COMMAND_NOT_STRACE")
    trace_tokens, string_limit, trace_output, trace_flags = parse_trace_filter(time_argv)
    capture_contract = contract["capture"]
    if capture_contract["require_follow_forks"] and not trace_flags["follow_forks"]:
        errors.append("TRACE_CAPTURE_DID_NOT_FOLLOW_FORKS")
    if capture_contract["require_fd_path_decoding"] and not trace_flags["fd_paths"]:
        errors.append("TRACE_CAPTURE_LACKS_FD_PATH_DECODING")
    if string_limit < capture_contract["minimum_string_limit"]:
        errors.append("TRACE_STRING_LIMIT_TOO_SMALL")
    captures_all_syscalls = "all" in trace_tokens or "%all" in trace_tokens
    if (
        capture_contract["require_percent_file"]
        and "%file" not in trace_tokens
        and not captures_all_syscalls
    ):
        errors.append("TRACE_CAPTURE_LACKS_PERCENT_FILE")
    required_explicit = set(capture_contract["required_explicit_syscalls"])
    missing_explicit = (
        [] if captures_all_syscalls else sorted(required_explicit - trace_tokens)
    )
    if missing_explicit:
        errors.append("TRACE_CAPTURE_MISSING_EXPLICIT_MUTATION_SYSCALLS")
    if trace_output is None:
        errors.append("TRACE_COMMAND_HAS_NO_OUTPUT_PATH")
        normalized_trace_output = None
    else:
        normalized_trace_output = normalized_absolute(trace_output, workspace)
        if normalized_trace_output != str(paths["trace"]):
            errors.append("TRACE_COMMAND_OUTPUT_PATH_MISMATCH")
    if "--candidate-dir" not in time_argv:
        errors.append("TRACE_COMMAND_HAS_NO_CANDIDATE_PATH")
        command_candidate = None
    else:
        candidate_index = time_argv.index("--candidate-dir") + 1
        if candidate_index >= len(time_argv):
            command_candidate = None
            errors.append("TRACE_COMMAND_CANDIDATE_PATH_MISSING")
        else:
            command_candidate = normalized_absolute(time_argv[candidate_index], workspace)
            if command_candidate != str(paths["candidate_dir"]):
                errors.append("TRACE_COMMAND_CANDIDATE_PATH_MISMATCH")

    calls = parse_trace(captured["trace"].data)
    syscall_counts = Counter(call.name for call in calls)
    if any(call.name in {"chdir", "fchdir"} and (call.result_integer or -1) >= 0 for call in calls):
        errors.append("TRACE_CONTAINS_CWD_CHANGE")

    allowed_streams = {
        1: str(paths["stdout"]),
        2: str(paths["stderr"]),
    }
    stream_transport = capture_contract.get(
        "stream_transport", "path-redirection"
    )
    allowed_paths = {
        normalized_absolute(value, workspace)
        for value in contract["allowed_write_paths"]
    }
    protected_roots = [
        normalized_absolute(value, workspace)
        for value in contract["protected_roots"]
    ]
    mutation_events: list[dict[str, Any]] = []
    stdout_payloads: list[bytes] = []
    stderr_payloads: list[bytes] = []

    def record_mutation(
        call: TraceCall,
        kind: str,
        target: str | None,
        fd: int | None = None,
        stream_allowed: bool = False,
    ) -> None:
        protected_hits = sorted(root for root in protected_roots if target and path_within(target, root))
        explicitly_allowed = target in allowed_paths if target is not None else False
        allowed = stream_allowed or explicitly_allowed
        event = {
            "allowed": allowed,
            "fd": fd,
            "kind": kind,
            "line": call.line_number,
            "protected_roots": protected_hits,
            "result": call.result_integer,
            "syscall": call.name,
            "target": target,
        }
        mutation_events.append(event)
        if not allowed:
            errors.append(f"FORBIDDEN_MUTATION_ATTEMPT_AT_TRACE_LINE:{call.line_number}")

    for call in calls:
        write_capable_open, open_target = open_mutation_path(call, workspace)
        if write_capable_open:
            record_mutation(call, "write-capable-open", open_target)

        for target in path_mutation_targets(call, workspace):
            record_mutation(call, "pathname-mutation", target)

        fd_target = fd_mutation_target(call, workspace)
        if fd_target is not None:
            fd, target = fd_target
            stream_allowed = fd in allowed_streams and (
                target == allowed_streams[fd]
                or (
                    stream_transport == "docker-attach-pipe"
                    and type(target) is str
                    and re.fullmatch(r"pipe:\[[0-9]+\]", target) is not None
                )
            )
            record_mutation(call, "fd-mutation", target, fd=fd, stream_allowed=stream_allowed)
            if call.name == "write" and stream_allowed:
                if len(call.args) != 3:
                    errors.append(f"STREAM_WRITE_ARGUMENT_COUNT_AT_TRACE_LINE:{call.line_number}")
                    continue
                payload = decode_c_string(call.args[1])
                try:
                    requested = int(call.args[2], 0)
                except ValueError:
                    errors.append(f"STREAM_WRITE_LENGTH_UNPARSED_AT_TRACE_LINE:{call.line_number}")
                    continue
                if requested != len(payload) or call.result_integer != len(payload):
                    errors.append(f"STREAM_WRITE_LENGTH_MISMATCH_AT_TRACE_LINE:{call.line_number}")
                if fd == 1:
                    stdout_payloads.append(payload)
                else:
                    stderr_payloads.append(payload)

        if call.name == "mmap" and len(call.args) >= 6:
            if "PROT_WRITE" in call.args[2] and "MAP_SHARED" in call.args[3]:
                fd, target = parse_fd(call.args[4])
                target = normalize_trace_target(target, workspace)
                record_mutation(call, "shared-writable-mmap", target, fd=fd)
        elif call.name in {"msync", "io_uring_enter", "sync"}:
            # These calls cannot be bound to a path from their ordinary strace
            # arguments.  Any occurrence fails closed.
            record_mutation(call, "unresolvable-indirect-mutation-channel", None)

    stdout_writes = [event for event in mutation_events if event["fd"] == 1]
    stderr_writes = [event for event in mutation_events if event["fd"] == 2]
    if len(stdout_payloads) != 1 or len(stdout_writes) != 1:
        errors.append("STDOUT_NOT_EXACTLY_ONE_WRITE_SYSCALL")
    if b"".join(stdout_payloads) != captured["stdout"].data:
        errors.append("STDOUT_TRACE_PAYLOAD_MISMATCH")
    if b"".join(stderr_payloads) != captured["stderr"].data:
        errors.append("STDERR_TRACE_PAYLOAD_MISMATCH")
    if len(stderr_payloads) != stderr_semantics["diagnostic_line_count"]:
        errors.append("STDERR_WRITE_COUNT_DOES_NOT_MATCH_DIAGNOSTICS")
    if any(payload.count(b"\n") != 1 or not payload.endswith(b"\n") for payload in stderr_payloads):
        errors.append("STDERR_DIAGNOSTIC_NOT_ONE_LINE_PER_WRITE")

    forbidden_events = [event for event in mutation_events if not event["allowed"]]
    protected_events = [event for event in mutation_events if event["protected_roots"]]
    capture_complete = not missing_explicit and all(
        code not in errors
        for code in (
            "TRACE_CAPTURE_DID_NOT_FOLLOW_FORKS",
            "TRACE_CAPTURE_LACKS_FD_PATH_DECODING",
            "TRACE_STRING_LIMIT_TOO_SMALL",
            "TRACE_CAPTURE_LACKS_PERCENT_FILE",
        )
    )
    observed_protected_zero = not protected_events
    certifiable_protected_zero = capture_complete and observed_protected_zero

    errors = sorted(set(errors))
    status = (
        "PASS_C30A_STRACE_ZERO_MUTATION_CERTIFIED"
        if not errors
        else "FAIL_CLOSED_C30A_STRACE_AUDIT"
    )
    return {
        "artifacts": artifacts,
        "candidate": {
            "directory": str(paths["candidate_dir"]),
            "directory_stat": list(candidate_stat),
            "exact_member_count": len(candidate_names),
            "exact_member_names": candidate_names,
            "manifest_bound": all(
                not error.startswith("CANDIDATE_") for error in errors
            ),
        },
        "conclusion": {
            "certifiable_zero_mutation_to_protected_roots": certifiable_protected_zero,
            "observed_zero_mutation_to_protected_roots": observed_protected_zero,
            "original_c30a_credit_unchanged": {
                "additional_credit": 0,
                "source_w_transition": "252->92",
                "transition_252_to_90": "FORBIDDEN",
            },
        },
        "contract": {
            "profile": contract["profile"],
            "sha256": contract_sha256,
            "source": contract_source,
        },
        "errors": errors,
        "manifest": {
            "exact_map_matches_contract": manifest_map == contract["manifest_members"],
            "member_count": len(manifest_map),
            "members_all_match": all(record["matches_pin"] for record in manifest_member_records.values()),
            "path": str(paths["manifest"]),
            "sha256": captured["manifest"].sha256,
        },
        "schema": SCHEMA,
        "status": status,
        "stderr_contract": {
            **stderr_semantics,
            "sha256": captured["stderr"].sha256,
            "write_syscall_count": len(stderr_payloads),
            "writes_reconstruct_exact_bytes": b"".join(stderr_payloads) == captured["stderr"].data,
        },
        "stdout_contract": {
            "canonical_json": stdout_canonical,
            "object_matches_contract": stdout_object == contract["stdout"]["expected_object"],
            "sha256": captured["stdout"].sha256,
            "write_syscall_count": len(stdout_payloads),
            "writes_reconstruct_exact_bytes": b"".join(stdout_payloads) == captured["stdout"].data,
        },
        "time_contract": {
            "command": time_command,
            "exit_status": exit_status,
            "sha256": captured["time"].sha256,
        },
        "trace_contract": {
            "allowed_exact_nonstream_write_paths": sorted(allowed_paths),
            "capture_complete_for_claimed_scope": capture_complete,
            "captures_all_syscalls": captures_all_syscalls,
            "captured_filter_tokens": sorted(trace_tokens),
            "command_candidate_path": command_candidate,
            "command_trace_output_path": normalized_trace_output,
            "forbidden_mutation_attempt_count": len(forbidden_events),
            "line_count": len(calls),
            "missing_explicit_mutation_syscalls": missing_explicit,
            "mutation_attempt_count": len(mutation_events),
            "protected_mutation_attempt_count": len(protected_events),
            "protected_roots": protected_roots,
            "required_explicit_mutation_syscalls": sorted(required_explicit),
            "sha256": captured["trace"].sha256,
            "string_limit": string_limit,
            "syscall_counts": dict(sorted(syscall_counts.items())),
        },
    }


def failure_result(exc: Exception) -> dict[str, Any]:
    return {
        "errors": [f"FATAL_INPUT_REJECTION:{type(exc).__name__}:{exc}"],
        "schema": SCHEMA,
        "status": "FAIL_CLOSED_C30A_STRACE_AUDIT",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--contract",
        type=Path,
        help="canonical custom contract; omitted means the frozen verifier contract",
    )
    parser.add_argument(
        "--expected-contract-sha256",
        help="mandatory SHA-256 pin for --contract",
    )
    args = parser.parse_args()
    try:
        contract, source, digest = load_contract(args)
        result = audit(contract, source, digest)
    except Exception as exc:  # fail-close boundary; still emit one canonical JSON
        result = failure_result(exc)
    sys.stdout.buffer.write(canonical_bytes(result))
    return 0 if result["status"].startswith("PASS_") else 1


if __name__ == "__main__":
    raise SystemExit(main())
