#!/usr/bin/env python3
"""FD-bound execution envelope for the append-only C27R2 back-half v5.

The formal caller must already hold every source/input file and every output
parent directory.  This envelope never trusts a pathname after launch: it
revalidates the inherited descriptors, copies source and inputs from those
descriptors into a private same-layout snapshot, executes only that snapshot,
and publishes flat output inventories with mkdirat/openat beneath the held
output-parent descriptors.  The checked-in source is execution-disabled until
the independent boundary-v6 and complete v5 chain audit both authorize it.
"""

from __future__ import annotations

import argparse
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import sys
import tempfile
import time
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
SELF = Path(__file__).resolve()
BASE = "cm2.round306c27r2.source-g-authority-v2.release-repair."
REQUEST_SCHEMA = BASE + "fd-bound-stage-request.v1"
REQUEST_STATUS = "FROZEN_C27R2_BACKHALF_V5_FD_BOUND_STAGE_REQUEST__NO_AUTHORITY"
RESULT_SCHEMA = BASE + "fd-bound-stage-result.v1"
RESULT_STATUS = "PASS_C27R2_BACKHALF_V5_FD_BOUND_PRIVATE_EXEC_AND_DIRFD_PUBLICATION__ZERO_CREDIT"
FORMAL_EXECUTION_AUTHORIZED = False
REQUEST_KEYS = {
    "schema", "status", "stage", "python_path", "python_sha256",
    "stage_source_path", "stage_source_fd", "stage_source_sha256",
    "input_files", "output_roots", "original_argv", "exact_environment",
    "timeout_seconds", "publication_lock_fd", "publication_lock_sha256",
    "publication_lock_stat_fingerprint", "result_fd", "formal_credit",
    "manifest_authorized", "authority_minted", "request_sha256",
}
INPUT_KEYS = {"path", "fd", "sha256", "stat_fingerprint"}
OUTPUT_KEYS = {
    "path", "parent_fd", "parent_stat_fingerprint", "leaf", "exact_files",
}


class Rejected(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Rejected(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
        ensure_ascii=True, allow_nan=False).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def valid_sha(value: Any) -> bool:
    return type(value) is str and re.fullmatch(r"[0-9a-f]{64}", value) is not None


def strict(raw: bytes) -> Any:
    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in items:
            need(type(key) is str and key not in result, "duplicate JSON key")
            result[key] = value
        return result
    return json.loads(raw, object_pairs_hook=pairs,
        parse_constant=lambda value: (_ for _ in ()).throw(Rejected(value)))


def fingerprint(info: os.stat_result) -> list[int]:
    return [info.st_dev, info.st_ino, info.st_mode, info.st_nlink,
            info.st_size, info.st_mtime_ns, info.st_ctime_ns,
            info.st_uid, info.st_gid]


def read_fd(fd: int) -> bytes:
    os.lseek(fd, 0, os.SEEK_SET)
    chunks: list[bytes] = []
    while block := os.read(fd, 1 << 20):
        chunks.append(block)
    os.lseek(fd, 0, os.SEEK_SET)
    return b"".join(chunks)


def fd_record(fd: int, regular: bool) -> dict[str, Any]:
    before = os.fstat(fd)
    if regular:
        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1,
             "inherited regular single-link fd")
        raw = read_fd(fd)
        after = os.fstat(fd)
        need(fingerprint(before) == fingerprint(after), "stable inherited file fd")
        return {"sha256": hashlib.sha256(raw).hexdigest(),
                "size": len(raw), "stat_fingerprint": fingerprint(before)}
    need(stat.S_ISDIR(before.st_mode), "inherited directory fd")
    return {"stat_fingerprint": fingerprint(before)}


def safe_parts(relative: str) -> tuple[str, ...]:
    path = Path(relative)
    need(type(relative) is str and relative and not path.is_absolute()
         and path.parts and all(part not in {"", ".", ".."}
                                for part in path.parts),
         "strict beneath relative path")
    return path.parts


def walk_dirfd(root_fd: int, parts: tuple[str, ...], create: bool) -> int:
    current = os.dup(root_fd)
    try:
        for part in parts:
            if create:
                try:
                    os.mkdir(part, 0o700, dir_fd=current)
                except FileExistsError:
                    pass
            following = os.open(part, os.O_RDONLY
                | getattr(os, "O_DIRECTORY", 0)
                | getattr(os, "O_NOFOLLOW", 0)
                | getattr(os, "O_CLOEXEC", 0), dir_fd=current)
            os.close(current)
            current = following
        return current
    except BaseException:
        os.close(current)
        raise


def open_beneath(root_fd: int, relative: str, flags: int,
                 mode: int = 0o400, create_parents: bool = False) -> int:
    """openat2 RESOLVE_BENEATH|NO_SYMLINKS equivalent for strict components."""
    parts = safe_parts(relative)
    parent = walk_dirfd(root_fd, parts[:-1], create_parents)
    try:
        return os.open(parts[-1], flags | getattr(os, "O_NOFOLLOW", 0)
            | getattr(os, "O_CLOEXEC", 0), mode, dir_fd=parent)
    finally:
        os.close(parent)


def write_all(fd: int, raw: bytes) -> None:
    offset = 0
    while offset < len(raw):
        count = os.write(fd, raw[offset:])
        need(type(count) is int and count > 0, "positive write progress")
        offset += count


def copy_regular_fd(source_fd: int, root_fd: int, relative: str) -> dict[str, Any]:
    source = fd_record(source_fd, True)
    raw = read_fd(source_fd)
    target = open_beneath(root_fd, relative,
        os.O_WRONLY | os.O_CREAT | os.O_EXCL, create_parents=True)
    try:
        write_all(target, raw)
        os.fsync(target)
        target_stat = os.fstat(target)
        need(stat.S_ISREG(target_stat.st_mode) and target_stat.st_nlink == 1,
             "copied regular single-link target")
    finally:
        os.close(target)
    verify = open_beneath(root_fd, relative, os.O_RDONLY)
    try:
        observed = read_fd(verify)
        need(observed == raw and hashlib.sha256(observed).hexdigest()
             == source["sha256"], "copied FD bytes/SHA")
    finally:
        os.close(verify)
    return source


def write_once_at(root_fd: int, relative: str, raw: bytes) -> dict[str, Any]:
    descriptor = open_beneath(root_fd, relative,
        os.O_WRONLY | os.O_CREAT | os.O_EXCL, create_parents=True)
    try:
        write_all(descriptor, raw)
        os.fsync(descriptor)
        before = os.fstat(descriptor)
    finally:
        os.close(descriptor)
    reopened = open_beneath(root_fd, relative, os.O_RDONLY)
    try:
        observed = read_fd(reopened)
        after = os.fstat(reopened)
        need(observed == raw and stat.S_ISREG(after.st_mode)
             and after.st_nlink == 1 and fingerprint(before) == fingerprint(after),
             "published file reopen bytes/full9stat/single-link")
        result = {"sha256": hashlib.sha256(observed).hexdigest(),
                  "stat_fingerprint": fingerprint(after)}
    finally:
        os.close(reopened)
    return result


def dirfd_inventory(root_fd: int, prefix: str = "") -> list[str]:
    answer: list[str] = []
    for name in sorted(os.listdir(root_fd)):
        need(type(name) is str and name not in {"", ".", ".."},
             "strict directory entry")
        info = os.stat(name, dir_fd=root_fd, follow_symlinks=False)
        shown = name if not prefix else prefix + "/" + name
        if stat.S_ISREG(info.st_mode):
            need(info.st_nlink == 1, "inventory regular single-link")
            answer.append(shown)
        elif stat.S_ISDIR(info.st_mode):
            child = os.open(name, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0)
                | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_CLOEXEC", 0),
                dir_fd=root_fd)
            try:
                answer.extend(dirfd_inventory(child, shown))
            finally:
                os.close(child)
        else:
            raise Rejected("inventory rejects link/device/non-regular entry")
    return answer


def mapped_argv(request: dict[str, Any], private_root: Path) -> list[str]:
    inputs = {row["path"]: private_root / row["path"]
              for row in request["input_files"]}
    replacements: dict[str, str] = {}
    for relative, private in inputs.items():
        replacements[relative] = str(private)
        replacements[str((ROOT / relative).absolute())] = str(private)
    output_prefixes: list[tuple[str, str]] = []
    for row in request["output_roots"]:
        relative = row["path"]
        private = str(private_root / relative)
        replacements[relative] = private
        replacements[str((ROOT / relative).absolute())] = private
        output_prefixes.extend(((relative + "/", private + "/"),
            (str((ROOT / relative).absolute()) + "/", private + "/")))
    command: list[str] = []
    for ordinal, token in enumerate(request["original_argv"]):
        need(type(token) is str and token and "\x00" not in token
             and "\n" not in token and "\r" not in token,
             "strict original argv token")
        if ordinal == 0:
            command.append(request["python_path"])
        else:
            replaced = replacements.get(token)
            if replaced is None:
                for old, new in output_prefixes:
                    if token.startswith(old):
                        replaced = new + token[len(old):]
                        break
            command.append(token if replaced is None else replaced)
    source_private = str(private_root / request["stage_source_path"])
    need(len(command) >= 4 and command[1:3] == ["-I", "-B"]
         and command[3] == source_private,
         "private FD-copied stage source is exact executed program")
    for token in command[3:]:
        if (token.startswith(str(ROOT) + "/")
                and not token.startswith(str(private_root) + "/")):
            raise Rejected("original workspace path survived private argv rewrite")
    return command


def execute_request(request: dict[str, Any], self_test_only: bool = False
                    ) -> tuple[dict[str, Any], bytes, bytes]:
    """Execute a validated request entirely from inherited file/dir FDs."""
    need(self_test_only or FORMAL_EXECUTION_AUTHORIZED,
         "fd-bound v5 envelope formal execution independently unauthorized")
    need(set(request) == REQUEST_KEYS, "exact fd-bound request inventory")
    python_path = Path(request["python_path"])
    need(python_path.is_absolute() and python_path.is_file()
         and not python_path.is_symlink() and valid_sha(request["python_sha256"])
         and hashlib.sha256(python_path.read_bytes()).hexdigest()
             == request["python_sha256"], "pinned current Python binary")
    inputs = request["input_files"]
    outputs = request["output_roots"]
    need(type(inputs) is list and len(inputs) > 0
         and [row["path"] for row in inputs]
             == sorted({row["path"] for row in inputs})
         and type(outputs) is list and len(outputs) > 0
         and [row["path"] for row in outputs]
             == sorted({row["path"] for row in outputs}),
         "sorted unique FD input/output inventories")
    observed_inputs: list[dict[str, Any]] = []
    for row in inputs:
        need(type(row) is dict and set(row) == INPUT_KEYS
             and type(row["fd"]) is int and row["fd"] >= 3
             and valid_sha(row["sha256"])
             and type(row["stat_fingerprint"]) is list
             and len(row["stat_fingerprint"]) == 9,
             "strict input FD member")
        safe_parts(row["path"])
        current = fd_record(row["fd"], True)
        need(current["sha256"] == row["sha256"]
             and current["stat_fingerprint"] == row["stat_fingerprint"],
             "inherited input FD SHA/full9 identity")
        observed_inputs.append({"path": row["path"], **current})
    source_rows = [row for row in inputs
                   if row["path"] == request["stage_source_path"]]
    need(len(source_rows) == 1
         and source_rows[0]["fd"] == request["stage_source_fd"]
         and source_rows[0]["sha256"] == request["stage_source_sha256"],
         "stage source is exactly one inherited input FD")
    output_fds: list[int] = []
    for row in outputs:
        need(type(row) is dict and set(row) == OUTPUT_KEYS
             and type(row["parent_fd"]) is int and row["parent_fd"] >= 3
             and type(row["parent_stat_fingerprint"]) is list
             and len(row["parent_stat_fingerprint"]) == 9
             and type(row["leaf"]) is str and len(safe_parts(row["leaf"])) == 1
             and type(row["exact_files"]) is list
             and row["exact_files"] == sorted(set(row["exact_files"]))
             and all(safe_parts(name) for name in row["exact_files"]),
             "strict output parent-dirfd contract")
        current = fd_record(row["parent_fd"], False)
        need(current["stat_fingerprint"] == row["parent_stat_fingerprint"],
             "held output parent-dirfd identity")
        try:
            os.stat(row["leaf"], dir_fd=row["parent_fd"], follow_symlinks=False)
        except FileNotFoundError:
            pass
        else:
            raise Rejected("fresh held-dirfd output leaf already exists")
        output_fds.append(row["parent_fd"])
    need(type(request["timeout_seconds"]) is int
         and 1 <= request["timeout_seconds"] <= 86_400
         and type(request["publication_lock_fd"]) is int
         and request["publication_lock_fd"] >= 3
         and type(request["result_fd"]) is int and request["result_fd"] >= 3,
         "timeout/lock/result FD contract")
    lock_info = os.fstat(request["publication_lock_fd"])
    need(stat.S_ISREG(lock_info.st_mode) and lock_info.st_nlink == 1,
         "inherited publication lock regular single-link")
    lock_record = fd_record(request["publication_lock_fd"], True)
    need(valid_sha(request["publication_lock_sha256"])
         and lock_record["sha256"] == request["publication_lock_sha256"]
         and lock_record["stat_fingerprint"]
             == request["publication_lock_stat_fingerprint"],
         "inherited publication lock SHA/full9 identity")
    fcntl.flock(request["publication_lock_fd"], fcntl.LOCK_EX | fcntl.LOCK_NB)
    environment = request["exact_environment"]
    need(type(environment) is dict and environment == {
        "PATH": "/usr/bin:/bin", "HOME": "/nonexistent", "LANG": "C",
        "LC_ALL": "C", "TZ": "UTC",
        "PYTHONHASHSEED": environment.get("PYTHONHASHSEED")}
        and type(environment["PYTHONHASHSEED"]) is str
        and environment["PYTHONHASHSEED"].isdigit(), "exact child environment")
    private_parent = ROOT / ".cm2-runtime"
    private_parent.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(dir=private_parent,
            prefix="c27r2-fd-bound-private-") as raw:
        private_root = Path(raw) / "workspace"
        private_root.mkdir(mode=0o700)
        private_fd = os.open(private_root, os.O_RDONLY
            | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0))
        try:
            copied = []
            for row in inputs:
                current = copy_regular_fd(row["fd"], private_fd, row["path"])
                copied.append({"path": row["path"], **current})
            command = mapped_argv(request, private_root)
            begun = time.monotonic()
            process = subprocess.Popen(command, cwd=private_root,
                env=environment, stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                start_new_session=True,
                pass_fds=(request["publication_lock_fd"],))
            try:
                stdout, stderr = process.communicate(
                    timeout=request["timeout_seconds"])
                timed_out = False
            except subprocess.TimeoutExpired:
                timed_out = True
                process.kill()
                stdout, stderr = process.communicate()
            elapsed = round(time.monotonic() - begun, 6)
            need(not timed_out and process.returncode == 0 and stderr == b"",
                 "private FD-backed child clean success")
            publication: list[dict[str, Any]] = []
            for row in outputs:
                private_output = private_root / row["path"]
                need(private_output.is_dir() and not private_output.is_symlink(),
                     "private output root exists")
                private_output_fd = os.open(private_output, os.O_RDONLY
                    | getattr(os, "O_DIRECTORY", 0)
                    | getattr(os, "O_NOFOLLOW", 0))
                try:
                    need(dirfd_inventory(private_output_fd) == row["exact_files"],
                         "private output exact regular inventory")
                    os.mkdir(row["leaf"], 0o700, dir_fd=row["parent_fd"])
                    target_fd = os.open(row["leaf"], os.O_RDONLY
                        | getattr(os, "O_DIRECTORY", 0)
                        | getattr(os, "O_NOFOLLOW", 0), dir_fd=row["parent_fd"])
                    try:
                        members: dict[str, Any] = {}
                        for relative in row["exact_files"]:
                            source_fd = open_beneath(
                                private_output_fd, relative, os.O_RDONLY)
                            try:
                                members[relative] = write_once_at(
                                    target_fd, relative, read_fd(source_fd))
                            finally:
                                os.close(source_fd)
                        need(dirfd_inventory(target_fd) == row["exact_files"],
                             "published held-dirfd exact regular inventory")
                        os.fsync(target_fd)
                    finally:
                        os.close(target_fd)
                    os.fsync(row["parent_fd"])
                    publication.append({"path": row["path"],
                        "parent_stat_fingerprint": fd_record(
                            row["parent_fd"], False)["stat_fingerprint"],
                        "exact_files": row["exact_files"],
                        "member_records": members})
                finally:
                    os.close(private_output_fd)
            need(copied == observed_inputs,
                 "private snapshot bytes/SHA/full9 source identity")
            result_body = {"schema": RESULT_SCHEMA, "status": RESULT_STATUS,
                "stage": request["stage"],
                "request_object_sha256": request["request_sha256"],
                "input_fd_map": observed_inputs,
                "private_argv_sha256": digest(command),
                "original_argv_sha256": digest(request["original_argv"]),
                "output_dirfd_publication": publication,
                "numeric_exit_code": 0, "signal": None,
                "stderr_empty": True, "timed_out": False,
                "elapsed_seconds": elapsed,
                "private_root_removed_before_runner_PASS": True,
                "formal_credit": 0, "manifest_authorized": False,
                "authority_minted": False, "CM2": "NO-GO_FOR_CLAIM"}
            result = {**result_body, "result_sha256": digest(result_body)}
            write_all(request["result_fd"], canonical(result) + b"\n")
            if stat.S_ISREG(os.fstat(request["result_fd"]).st_mode):
                os.fsync(request["result_fd"])
            return result, stdout, stderr
        finally:
            os.close(private_fd)


def validate_request(value: Any) -> dict[str, Any]:
    need(type(value) is dict and set(value) == REQUEST_KEYS
         and value.get("schema") == REQUEST_SCHEMA
         and value.get("status") == REQUEST_STATUS
         and value.get("formal_credit") == 0
         and value.get("manifest_authorized") is False
         and value.get("authority_minted") is False,
         "fd-bound request governance")
    body = dict(value)
    claim = body.pop("request_sha256", None)
    need(valid_sha(claim) and claim == digest(body), "request object closure")
    return value


def execute(args: argparse.Namespace) -> dict[str, Any]:
    need(FORMAL_EXECUTION_AUTHORIZED,
         "fd-bound v5 envelope formal execution independently unauthorized")
    need(type(args.request_fd) is str and args.request_fd.isdigit(),
         "numeric inherited request fd")
    request_fd = int(args.request_fd)
    request_record = fd_record(request_fd, True)
    need(valid_sha(args.expect_request_file_sha256)
         and request_record["sha256"] == args.expect_request_file_sha256,
         "request fd file pin")
    raw = read_fd(request_fd)
    need(raw.endswith(b"\n"), "request newline")
    request = validate_request(strict(raw[:-1]))
    need(request["request_sha256"] == args.expect_request_object_sha256,
         "request fd object pin")
    result, stdout, stderr = execute_request(request)
    need(stderr == b"", "wrapper child stderr empty")
    sys.stdout.buffer.write(stdout)
    return result


def self_test() -> dict[str, Any]:
    need(FORMAL_EXECUTION_AUTHORIZED is False, "formal gate false")
    with tempfile.TemporaryDirectory(dir=ROOT / ".cm2-runtime",
            prefix="c27r2-fd-bound-v1-") as raw:
        root = Path(raw)
        original = root / "parent"
        original.mkdir()
        held = os.open(original, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0)
                       | getattr(os, "O_NOFOLLOW", 0))
        probe = root / "probe"
        probe.write_bytes(b"fd-bound\n")
        probe_fd = os.open(probe, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
        source = root / "deliverables/child.py"
        source.parent.mkdir()
        output_relative = ".cm2-runtime/fd-wrapper-selftest-output"
        source.write_text("import pathlib,sys\n"
            f"p=pathlib.Path({output_relative!r});p.mkdir(parents=True)\n"
            "(p/'receipt').write_bytes(b'fd-child\\n')\n"
            "sys.stdout.buffer.write(b'PASS_CHILD\\n')\n", encoding="utf-8")
        source_fd = os.open(source, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
        try:
            renamed = root / "parent-held"
            original.rename(renamed)
            original.mkdir()
            copied = copy_regular_fd(probe_fd, held, "nested/member")
            need((renamed / "nested/member").read_bytes() == b"fd-bound\n"
                 and not (original / "nested/member").exists()
                 and copied["sha256"]
                     == hashlib.sha256(b"fd-bound\n").hexdigest(),
                 "held-dirfd defeats parent-directory swap")
            symlink = renamed / "escape"
            symlink.symlink_to(root)
            try:
                open_beneath(held, "escape/member", os.O_RDONLY)
            except OSError:
                pass
            else:
                raise Rejected("symlink traversal unexpectedly accepted")
            for bad in ("../member", "/absolute", "a/../../member"):
                try:
                    open_beneath(held, bad, os.O_RDONLY)
                except (Rejected, OSError):
                    pass
                else:
                    raise Rejected("non-beneath path unexpectedly accepted")
            output_parent = root / "published"
            output_parent.mkdir()
            output_parent_fd = os.open(output_parent, os.O_RDONLY
                | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0))
            result_path = root / "result.json"
            result_fd = os.open(result_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL,
                                0o400)
            try:
                source_info = fd_record(source_fd, True)
                python_path = Path(sys.executable).resolve()
                request_body = {"schema": REQUEST_SCHEMA,
                    "status": REQUEST_STATUS, "stage": "self_test",
                    "python_path": str(python_path),
                    "python_sha256": hashlib.sha256(
                        python_path.read_bytes()).hexdigest(),
                    "stage_source_path": "deliverables/child.py",
                    "stage_source_fd": source_fd,
                    "stage_source_sha256": source_info["sha256"],
                    "input_files": [{"path": "deliverables/child.py",
                        "fd": source_fd, "sha256": source_info["sha256"],
                        "stat_fingerprint": source_info["stat_fingerprint"]}],
                    "output_roots": [{"path": output_relative,
                        "parent_fd": output_parent_fd,
                        "parent_stat_fingerprint": fd_record(
                            output_parent_fd, False)["stat_fingerprint"],
                        "leaf": "result", "exact_files": ["receipt"]}],
                    "original_argv": [str(python_path), "-I", "-B",
                        str((ROOT / "deliverables/child.py").absolute())],
                    "exact_environment": {"PATH": "/usr/bin:/bin",
                        "HOME": "/nonexistent", "LANG": "C", "LC_ALL": "C",
                        "TZ": "UTC", "PYTHONHASHSEED": "424242"},
                    "timeout_seconds": 30, "publication_lock_fd": source_fd,
                    "publication_lock_sha256": source_info["sha256"],
                    "publication_lock_stat_fingerprint":
                        source_info["stat_fingerprint"],
                    "result_fd": result_fd, "formal_credit": 0,
                    "manifest_authorized": False, "authority_minted": False}
                request = {**request_body, "request_sha256": digest(request_body)}
                result, stdout, stderr = execute_request(request, True)
                need(stdout == b"PASS_CHILD\n" and stderr == b""
                     and (output_parent / "result/receipt").read_bytes()
                         == b"fd-child\n"
                     and result["status"] == RESULT_STATUS,
                     "real private FD-backed child and held-dirfd publication")
            finally:
                os.close(result_fd)
                os.close(output_parent_fd)
        finally:
            os.close(probe_fd)
            os.close(source_fd)
            os.close(held)
    return {"schema": RESULT_SCHEMA, "status": RESULT_STATUS,
        "real_private_fd_child_executed": True,
        "parent_directory_swap_rejected": True,
        "symlink_and_traversal_rejected": True,
        "formal_credit": 0, "manifest_authorized": False,
        "authority_minted": False, "CM2": "NO-GO_FOR_CLAIM"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--request-fd")
    parser.add_argument("--expect-request-file-sha256")
    parser.add_argument("--expect-request-object-sha256")
    args = parser.parse_args()
    try:
        if args.self_test:
            need(args.request_fd is None
                 and args.expect_request_file_sha256 is None
                 and args.expect_request_object_sha256 is None,
                 "self-test no formal args")
            result = self_test()
        else:
            need(all(value is not None for value in (
                args.request_fd, args.expect_request_file_sha256,
                args.expect_request_object_sha256)), "all request fd pins required")
            result = execute(args)
        if args.self_test:
            sys.stdout.buffer.write(canonical({"schema": result["schema"],
                "status": result["status"], "formal_credit": 0,
                "CM2": "NO-GO_FOR_CLAIM"}) + b"\n")
        return 0
    except (Rejected, OSError, ValueError, KeyError, TypeError) as error:
        sys.stderr.write("REJECT:" + str(error) + "\n")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
