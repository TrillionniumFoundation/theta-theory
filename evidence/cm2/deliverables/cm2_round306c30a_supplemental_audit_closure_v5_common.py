#!/usr/bin/env python3
"""Shared fail-closed primitives for the additive C30a P0-B v5 chain.

The v5 chain deliberately does not consume any v4 assembly or derived exit
receipt.  All paths are canonical workspace-relative paths; every evidence
file is captured once through ``O_NOFOLLOW`` after every parent directory has
been checked for symlinks.  Timed-process receipts bind stdout, stderr, GNU
time, Docker pre/post inspection, and the real Docker attach return code from
one invocation.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import re
import shlex
import stat
import sys
import types
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any


sys.dont_write_bytecode = True

WORKSPACE = Path(
    "/home/qian-qi/.openclaw/workspaces/telegram-bot-8449317572"
)
DELIVERABLES = WORKSPACE / "deliverables"
AUDIT = WORKSPACE / ".cm2-runtime/audit"
BASE_PREFIX = (
    "cm2_round306c30a_source_w_162_reduced_clipped_delta_"
    "whole_origin_promotion"
)
BASE_MANIFEST_REL = "deliverables/" + BASE_PREFIX + "_manifest.sha256"
BASE_MANIFEST_SHA256 = (
    "0f3e80d54d4307eccf509435470213e19fd4eefffc43b95e01cec0d3b8a094bc"
)
BASE_SEALED_REL = "deliverables/cm2_round306c30a_sealed"
LOCKED_PYTHON = WORKSPACE / ".cm2-runtime/python-flint-0.9.0/bin/python"
SEEDS = ("30630071", "30630929")
OUTPUT_NAMES = (
    BASE_PREFIX + "_cell_ledger.jsonl.gz",
    BASE_PREFIX + "_inherited_h_obstruction_ledger.jsonl.gz",
    BASE_PREFIX + "_result.json",
    BASE_PREFIX + "_whole_origin_ledger.jsonl.gz",
)
OUTPUT_HASHES = {
    BASE_PREFIX + "_cell_ledger.jsonl.gz":
        "c4c0061a08983471428b2e5113aff60bbeccc67530cac691658a6bbad1ce9904",
    BASE_PREFIX + "_inherited_h_obstruction_ledger.jsonl.gz":
        "f86c6c3d90a4a87c7d4366b86a0e8119d019cbf86f5b5ab781140605ddc1e80e",
    BASE_PREFIX + "_result.json":
        "521be2aefebea96d6a3d2ce1bcf0234753ef69af7182a4e47a0d22d686df6c48",
    BASE_PREFIX + "_whole_origin_ledger.jsonl.gz":
        "778995522629a362183159420860b65d60c8719bc1453c4fc2657e8e8fba9649",
}
ATTACK_NAMES = (
    "promoted_origin_count",
    "remaining_origin_count",
    "D02_illegal_clear",
    "CM2_illegal_go",
    "child_volume_credit",
    "input_pin_retarget",
    "cell_ledger_full_reclosure",
    "origin_ledger_full_reclosure",
    "origin_order_full_reclosure",
    "held_to_promoted_162_overclaim_full_reclosure",
)
NETWORK_SYSCALLS = {
    "accept", "accept4", "bind", "connect", "getpeername", "getsockname",
    "getsockopt", "listen", "recv", "recvfrom", "recvmmsg", "recvmsg",
    "send", "sendmmsg", "sendmsg", "sendto", "setsockopt", "shutdown",
    "socket", "socketcall", "socketpair",
}
RUN_NAME = re.compile(r"c30a-supplemental-p0b-v5-[A-Za-z0-9][A-Za-z0-9._-]{0,63}\Z")
SAFE_COMPONENT = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,95}\Z")
HEX64 = re.compile(r"[0-9a-f]{64}\Z")
TIME_COMMAND = re.compile(r'^\s*Command being timed: "(.*)"\s*$', re.MULTILINE)
TIME_EXIT = re.compile(r"^\s*Exit status:\s*([0-9]+)\s*$", re.MULTILINE)
TIME_SIGNAL = re.compile(
    r"^\s*Command terminated by signal\s+([^\r\n]+)\s*$",
    re.MULTILINE,
)
MAX_FILE = 2 * 1024 * 1024 * 1024
MAX_RETAIN = 256 * 1024 * 1024


class Reject(RuntimeError):
    """A v5 authority precondition failed."""


def require(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise Reject(label)


def canonical(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=True,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("ascii")


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def close_object(body: dict[str, Any]) -> dict[str, Any]:
    require("payload_sha256" not in body, "object already closed")
    return {**body, "payload_sha256": sha256(canonical(body))}


def validate_closed(value: Any, label: str) -> dict[str, Any]:
    require(type(value) is dict, "closed object:" + label)
    body = dict(value)
    digest = body.pop("payload_sha256", None)
    require(digest == sha256(canonical(body)), "object digest closure:" + label)
    return value


def safe_relpath(value: str) -> PurePosixPath:
    require(type(value) is str, "path string")
    pure = PurePosixPath(value)
    require(
        not pure.is_absolute()
        and pure.as_posix() == value
        and all(part not in {"", ".", ".."} for part in pure.parts),
        "safe canonical relative path:" + str(value),
    )
    return pure


def workspace_rel(path: Path) -> str:
    absolute = Path(os.path.abspath(os.fspath(path)))
    require(
        absolute.is_relative_to(WORKSPACE) and absolute != WORKSPACE,
        "workspace containment:" + os.fspath(path),
    )
    return absolute.relative_to(WORKSPACE).as_posix()


def validate_parent_chain(path: Path, *, final_may_be_absent: bool = False) -> None:
    absolute = Path(os.path.abspath(os.fspath(path)))
    require(absolute.is_relative_to(WORKSPACE), "parent-chain workspace containment")
    relative = absolute.relative_to(WORKSPACE)
    cursor = WORKSPACE
    root_status = cursor.lstat()
    require(stat.S_ISDIR(root_status.st_mode) and not cursor.is_symlink(),
            "workspace root directory")
    parts = relative.parts[:-1] if final_may_be_absent else relative.parts
    for part in parts:
        cursor = cursor / part
        status = cursor.lstat()
        require(
            stat.S_ISDIR(status.st_mode) and not cursor.is_symlink(),
            "non-symlink parent:" + workspace_rel(cursor),
        )


@dataclass(frozen=True)
class Capture:
    relpath: str
    sha256: str
    size: int
    dev: int
    ino: int
    mtime_ns: int
    ctime_ns: int
    raw: bytes | None


def capture(path_or_rel: Path | str, *, retain: bool = True) -> Capture:
    path = (
        WORKSPACE / safe_relpath(path_or_rel)
        if isinstance(path_or_rel, str)
        else Path(os.path.abspath(os.fspath(path_or_rel)))
    )
    relpath = workspace_rel(path)
    validate_parent_chain(path, final_may_be_absent=True)
    before = path.lstat()
    require(
        stat.S_ISREG(before.st_mode)
        and not path.is_symlink()
        and before.st_nlink == 1
        and 0 <= before.st_size <= MAX_FILE,
        "regular singleton bounded file:" + relpath,
    )
    descriptor = os.open(
        path,
        os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0),
    )
    chunks: list[bytes] | None = [] if retain else None
    digest = hashlib.sha256()
    try:
        opened = os.fstat(descriptor)
        identity = (
            before.st_dev, before.st_ino, before.st_size,
            before.st_mtime_ns, before.st_ctime_ns,
        )
        require(
            stat.S_ISREG(opened.st_mode)
            and opened.st_nlink == 1
            and (
                opened.st_dev, opened.st_ino, opened.st_size,
                opened.st_mtime_ns, opened.st_ctime_ns,
            ) == identity,
            "pre/open identity:" + relpath,
        )
        remaining = opened.st_size
        while remaining:
            block = os.read(descriptor, min(1 << 20, remaining))
            require(bool(block), "short read:" + relpath)
            digest.update(block)
            if chunks is not None:
                require(opened.st_size <= MAX_RETAIN, "retain bound:" + relpath)
                chunks.append(block)
            remaining -= len(block)
        require(not os.read(descriptor, 1), "growing file:" + relpath)
        final = os.fstat(descriptor)
        require(
            (
                final.st_dev, final.st_ino, final.st_size,
                final.st_mtime_ns, final.st_ctime_ns,
            ) == identity,
            "open/final identity:" + relpath,
        )
    finally:
        os.close(descriptor)
    after = path.lstat()
    require(
        stat.S_ISREG(after.st_mode)
        and not path.is_symlink()
        and after.st_nlink == 1
        and (
            after.st_dev, after.st_ino, after.st_size,
            after.st_mtime_ns, after.st_ctime_ns,
        ) == (
            before.st_dev, before.st_ino, before.st_size,
            before.st_mtime_ns, before.st_ctime_ns,
        ),
        "post-read identity:" + relpath,
    )
    return Capture(
        relpath=relpath,
        sha256=digest.hexdigest(),
        size=before.st_size,
        dev=before.st_dev,
        ino=before.st_ino,
        mtime_ns=before.st_mtime_ns,
        ctime_ns=before.st_ctime_ns,
        raw=None if chunks is None else b"".join(chunks),
    )


def strict_json(raw: bytes, label: str, *, newline: bool = True) -> dict[str, Any]:
    require(raw is not None and b"\x00" not in raw, "JSON bytes:" + label)
    if newline:
        require(raw.endswith(b"\n") and raw.count(b"\n") == 1,
                "one-line JSON:" + label)
        body = raw[:-1]
    else:
        body = raw

    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        output: dict[str, Any] = {}
        for key, value in pairs:
            require(type(key) is str and key not in output,
                    "unique JSON key:" + label)
            output[key] = value
        return output

    try:
        value = json.loads(
            body.decode("utf-8", "strict"),
            object_pairs_hook=unique,
            parse_constant=lambda token: (_ for _ in ()).throw(ValueError(token)),
            parse_float=lambda token: (_ for _ in ()).throw(ValueError(token)),
        )
    except (UnicodeDecodeError, ValueError, json.JSONDecodeError) as error:
        raise Reject("strict JSON:" + label) from error
    require(type(value) is dict and canonical(value) == body,
            "canonical JSON object:" + label)
    return value


def json_capture(path_or_rel: Path | str, label: str) -> tuple[Capture, dict[str, Any]]:
    cap = capture(path_or_rel)
    require(cap.raw is not None, "retained JSON:" + label)
    return cap, strict_json(cap.raw, label)


def parse_manifest(raw: bytes, label: str) -> dict[str, str]:
    try:
        text = raw.decode("ascii", "strict")
    except UnicodeDecodeError as error:
        raise Reject("ASCII manifest:" + label) from error
    require(text.endswith("\n"), "manifest final newline:" + label)
    rows: dict[str, str] = {}
    for line in text.splitlines():
        match = re.fullmatch(r"([0-9a-f]{64})  ([^\x00\r\n]+)", line)
        require(match is not None, "manifest syntax:" + label)
        digest, name = match.groups()
        safe_relpath(name)
        require(name not in rows, "manifest duplicate:" + label)
        rows[name] = digest
    require(bool(rows), "nonempty manifest:" + label)
    return rows


def parse_time(raw: bytes, label: str) -> list[str]:
    try:
        text = raw.decode("utf-8", "strict")
    except UnicodeDecodeError as error:
        raise Reject("GNU time UTF-8:" + label) from error
    require(text.endswith("\n"), "GNU time final newline:" + label)
    commands = TIME_COMMAND.findall(text)
    exits = TIME_EXIT.findall(text)
    signals = TIME_SIGNAL.findall(text)
    require(
        len(commands) == 1 and exits == ["0"] and signals == [],
        "GNU time unique zero nonsignal completion:" + label,
    )
    try:
        argv = shlex.split(commands[0], posix=True)
    except ValueError as error:
        raise Reject("GNU time command parse:" + label) from error
    require(bool(argv), "GNU time nonempty command:" + label)
    return argv


def run_root(value: str) -> Path:
    pure = safe_relpath(value)
    require(
        pure.parent.as_posix() == ".cm2-runtime/audit"
        and RUN_NAME.fullmatch(pure.name) is not None,
        "v5 run root direct-child naming policy",
    )
    path = WORKSPACE / pure
    validate_parent_chain(path, final_may_be_absent=True)
    status = path.lstat()
    require(stat.S_ISDIR(status.st_mode) and not path.is_symlink(),
            "v5 run root directory")
    return path


def artifact(cap: Capture) -> dict[str, Any]:
    return {"path": cap.relpath, "sha256": cap.sha256, "size": cap.size}


def verify_artifact(row: Any, cap: Capture, label: str) -> None:
    require(
        type(row) is dict
        and row == artifact(cap),
        "artifact binding:" + label,
    )


def validate_stage(root: Path, stage_name: str) -> dict[str, Any]:
    require(SAFE_COMPONENT.fullmatch(stage_name) is not None, "safe stage name")
    stage = root / "stages" / stage_name
    start_cap, start = json_capture(stage / "start.json", stage_name + " start")
    exit_cap, receipt = json_capture(stage / "exit.json", stage_name + " exit")
    validate_closed(receipt, stage_name + " exit")
    stdout = capture(stage / "stdout.raw")
    stderr = capture(stage / "stderr.raw")
    timing = capture(stage / "time.txt")
    inspect_pre_cap, inspect_pre = json_capture(
        stage / "docker_inspect_pre.json", stage_name + " docker pre"
    )
    inspect_post_cap, inspect_post = json_capture(
        stage / "docker_inspect_post.json", stage_name + " docker post"
    )
    inspect_pre_raw = capture(stage / "docker_inspect_pre.raw.json")
    inspect_post_raw = capture(stage / "docker_inspect_post.raw.json")
    create_stdout = capture(stage / "docker_create.stdout.raw")
    create_stderr = capture(stage / "docker_create.stderr.raw")
    require(
        inspect_pre_raw.raw is not None and inspect_post_raw.raw is not None,
        "retained raw Docker inspections:" + stage_name,
    )
    try:
        parsed_pre_raw = json.loads(inspect_pre_raw.raw.decode("utf-8", "strict"))
        parsed_post_raw = json.loads(inspect_post_raw.raw.decode("utf-8", "strict"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise Reject("raw Docker inspection JSON:" + stage_name) from error
    require(parsed_pre_raw == inspect_pre and parsed_post_raw == inspect_post,
            "raw/canonical Docker inspection equality:" + stage_name)
    require(timing.raw is not None, "retained timing:" + stage_name)
    inner_argv = parse_time(timing.raw, stage_name)
    require(
        receipt.get("schema")
        == "cm2.round306c30a.supplemental-timed-process-exit.v5"
        and receipt.get("status") == "PASS_SAME_INVOCATION_ZERO_EXIT_NO_SIGNAL"
        and receipt.get("stage") == stage_name
        and receipt.get("attach_returncode") == 0
        and receipt.get("container_exit_code") == 0
        and receipt.get("signal") is None
        and receipt.get("oom_killed") is False
        and receipt.get("docker_error") == ""
        and type(receipt.get("started_wall_time_ns")) is int
        and type(receipt.get("ended_wall_time_ns")) is int
        and receipt.get("started_wall_time_ns") == start.get("wall_time_ns")
        and receipt.get("ended_wall_time_ns") >= receipt.get("started_wall_time_ns")
        and receipt.get("inner_argv") == inner_argv,
        "same invocation exit semantics:" + stage_name,
    )
    for key, cap in (
        ("stdout", stdout), ("stderr", stderr), ("time", timing),
        ("docker_inspect_pre", inspect_pre_cap),
        ("docker_inspect_post", inspect_post_cap),
        ("docker_inspect_pre_raw", inspect_pre_raw),
        ("docker_inspect_post_raw", inspect_post_raw),
        ("docker_create_stdout", create_stdout),
        ("docker_create_stderr", create_stderr),
    ):
        verify_artifact(receipt.get(key), cap, stage_name + ":" + key)
    require(type(inspect_pre) is dict and type(inspect_post) is dict,
            "docker inspect objects:" + stage_name)
    require(
        create_stderr.size == 0
        and create_stdout.raw is not None
        and create_stdout.raw.strip().decode("ascii", "strict")
        == receipt.get("container_id"),
        "Docker create raw streams/container identity:" + stage_name,
    )
    require(
        start.get("schema") == "cm2.round306c30a.supplemental-stage-start.v5"
        and start.get("stage") == stage_name
        and type(start.get("wall_time_ns")) is int
        and start.get("wall_time_ns") > 0,
        "stage start receipt:" + stage_name,
    )
    verify_artifact(receipt.get("start"), start_cap, stage_name + ":start")
    for inspected, phase in ((inspect_pre, "pre"), (inspect_post, "post")):
        host = inspected.get("HostConfig", {})
        config = inspected.get("Config", {})
        binds = host.get("Binds")
        require(
            host.get("NetworkMode") == "none"
            and host.get("ReadonlyRootfs") is True
            and host.get("CapDrop") == ["ALL"]
            and "no-new-privileges" in (host.get("SecurityOpt") or [])
            and host.get("IpcMode") == "none"
            and config.get("User") == receipt.get("docker_user")
            and inspected.get("Image") == receipt.get("image_id"),
            "kernel isolation inspect:" + stage_name + ":" + phase,
        )
        require(type(binds) is list and all(type(item) is str for item in binds),
                "Docker bind list:" + stage_name)
        parsed_binds: list[tuple[str, str, str]] = []
        for item in binds:
            parts = item.rsplit(":", 2)
            require(len(parts) == 3 and parts[2] in {"ro", "rw"},
                    "Docker canonical bind:" + stage_name)
            parsed_binds.append((parts[0], parts[1], parts[2]))
        require(
            (os.fspath(WORKSPACE), os.fspath(WORKSPACE), "ro") in parsed_binds
            and (os.fspath(root), os.fspath(root), "rw") in parsed_binds
            and all(
                mode == "ro"
                or (
                    Path(source).is_relative_to(root)
                    and (
                        Path(destination).is_relative_to(root)
                        or destination.endswith(
                            "/.cm2-runtime/audit/c30a-p0-closure-verifier-20260807"
                        )
                    )
                )
                for source, destination, mode in parsed_binds
            ),
            "only run-root-owned writable bind mounts:" + stage_name,
        )
    state = inspect_post.get("State", {})
    require(
        state.get("Status") == "exited"
        and state.get("ExitCode") == 0
        and state.get("OOMKilled") is False
        and state.get("Error") == "",
        "Docker post state:" + stage_name,
    )
    return {
        "receipt": receipt,
        "receipt_capture": exit_cap,
        "start_capture": start_cap,
        "start": start,
        "stdout": stdout,
        "stderr": stderr,
        "time": timing,
        "inspect_pre": inspect_pre_cap,
        "inspect_post": inspect_post_cap,
        "inspect_pre_raw": inspect_pre_raw,
        "inspect_post_raw": inspect_post_raw,
        "create_stdout": create_stdout,
        "create_stderr": create_stderr,
    }


def load_module(path: Path, name: str) -> types.ModuleType:
    cap = capture(path)
    require(cap.raw is not None, "module retained:" + name)
    module = types.ModuleType(name)
    module.__file__ = os.fspath(path)
    module.__package__ = ""
    sys.modules[name] = module
    try:
        exec(compile(cap.raw, module.__file__, "exec", dont_inherit=True), module.__dict__)
    except Exception:
        sys.modules.pop(name, None)
        raise
    return module


def load_legacy_checker() -> types.ModuleType:
    return load_module(
        DELIVERABLES
        / "cm2_round306c30a_supplemental_audit_closure_release_checker.py",
        "_cm2_c30a_v5_legacy_base_checker",
    )


def load_analyzer() -> types.ModuleType:
    return load_module(
        DELIVERABLES
        / "cm2_round306c30a_supplemental_audit_closure_strace_analyzer.py",
        "_cm2_c30a_v5_strace_analyzer",
    )


def validate_base_manifest() -> dict[str, Capture]:
    checker = load_legacy_checker()
    return checker.validate_base()


def fixed_conclusion() -> dict[str, Any]:
    return {
        "original_c30a_whole_origin_exclusion_credit": 160,
        "supplemental_additional_whole_origin_exclusion_credit": 0,
        "source_W_transition": {"before": 252, "after": 92},
        "source_W_252_to_90": "FORBIDDEN",
        "D02": "BLOCKED_COMPOSITE",
        "CM2": "NO-GO_FOR_CLAIM",
    }


def write_exclusive(path: Path, raw: bytes, mode: int = 0o444) -> None:
    require(path.parent.is_dir() and not path.parent.is_symlink(), "output parent")
    validate_parent_chain(path, final_may_be_absent=True)
    descriptor = os.open(
        path,
        os.O_WRONLY | os.O_CREAT | os.O_EXCL
        | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0),
        mode,
    )
    complete = False
    try:
        offset = 0
        while offset < len(raw):
            count = os.write(descriptor, raw[offset:])
            require(count > 0, "short exclusive write")
            offset += count
        os.fsync(descriptor)
        complete = True
    finally:
        os.close(descriptor)
    require(complete, "exclusive output complete")


def write_json(path: Path, value: dict[str, Any]) -> None:
    write_exclusive(path, canonical(value) + b"\n")
