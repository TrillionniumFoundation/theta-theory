#!/usr/bin/env python3
"""External held-FD bootstrap for the frozen C79g v12 cold launcher.

The wrapper never retries and never imports the launcher.  It pins the complete
published exact10, proves the publication and phase surface, copies the held
launcher bytes into a fresh sealed memfd, and execs that same memfd with a
minimal environment.  Before manifest/outer publication, exact10 cannot be
held and this wrapper therefore fails closed.
"""

from __future__ import annotations

import ast
import ctypes
import fcntl
import hashlib
import json
import os
import stat
import sys
from typing import Any


ROOT_LABEL = "/home/qian-qi/.openclaw/workspaces/telegram-bot-8449317572"
ROOT_REL = b"home/qian-qi/.openclaw/workspaces/telegram-bot-8449317572"
CHECKPOINT = "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab"
PYTHON = "/usr/bin/python3.12"
BASENAME = "cm2_round306c79g_true_global_no_producer_consumer"

V11_REJECTION_REL = (
    ".cm2-runtime/c79g-v11-rejections-" + CHECKPOINT + "/rejection.json")
SCHEMA_REL = f"deliverables/{BASENAME}_schema_v12.json"
CONTRACT_REL = f"deliverables/{BASENAME}_contract_v12.json"
PRODUCER_REL = f"deliverables/{BASENAME}_v12.py"
CONSUMER_REL = (
    f"deliverables/{BASENAME}_independent_verifier_assembler_authority_consumer_v12.py")
TRANSITION_REL = (
    f"deliverables/{BASENAME}_v11_to_v12_static_launch_transition_receipt_v1.json")
AUDIT_REL = f"deliverables/{BASENAME}_static_audit_v12.json"
LAUNCHER_REL = f"deliverables/{BASENAME}_cold_launch_v12.py"
MANIFEST_REL = f"deliverables/{BASENAME}_cold_launch_manifest_v12.sha256"
OUTER_REL = f"deliverables/{BASENAME}_cold_launch_outer_receipt_v12.json"

EXACT10: tuple[tuple[str, str, str | None], ...] = (
    (V11_REJECTION_REL,
     "f6cc10d8b7e72553ef0b7a32bbfb99255f36cce16b735002f17be58ae51d3bc8",
     "7ae86e38c5910bc9ceaa0a4e5cb1f8fbbf1e73de9c0314fedabbd8cb2db3bb7a"),
    (SCHEMA_REL,
     "5ed911a55e8f90e750fdcaf6ab4fb6c9683bebaf66a4d6250329dff98acb2e28", None),
    (CONTRACT_REL,
     "72246725b15891f92cbc6e3fa1c07ab4a76cdaa19f1b366a736f47f51989b343",
     "f5c1710817dc8e3aa7fe2bbf4b88e6e39baaa1b17bbeb0f8bf37c8c4575ae5d7"),
    (PRODUCER_REL,
     "4cafc594f8a60063b7e7caaa82ddcc2b7983d0fbf0929034cd3cb5f360f3ed1d", None),
    (CONSUMER_REL,
     "b74dee738257d485e9ca3357d7d138b5175b95e58f1c8ea87d1eca7bfc96b2ed", None),
    (TRANSITION_REL,
     "45dabc1ef60eb2f8ba34aa7daa69f9d2b3bedccd4168d9c472bd4bbb696b5400",
     "0673ecafaa9991cd78e905e144e7c8c1b91717a3d753befa13e82552d44a4072"),
    (AUDIT_REL,
     "ac29b1e31e0d1b51e8610b7699d1aaf55c80fa6f13f00b20b209c2889e121d37",
     "c1473ae0f5a08d8772227f61a55bd32c479a7b5c7d40da17b37e796abf4d9783"),
    (LAUNCHER_REL,
     "b7aaff67be866f8fd7a01f71e97ea1491574f69e62b7760b6ced9183997444ba", None),
    (MANIFEST_REL,
     "297e9f58dc7657c6fa959dd45081efffe4e7e8dadcd16ab89457863e2661ece6", None),
    (OUTER_REL,
     "27129990a9d5b6697fd13ee8e2086100cbf158f12e5b767166d771e63088b6d0",
     "bc6d06141865954590bd11bfc96ad59dbbffa003f568355ecb47155a8a3a809d"),
)
EXPECTED_LAUNCHER_SHA256 = EXACT10[7][1]
EXPECTED_MANIFEST_SHA256 = EXACT10[8][1]
EXPECTED_PIN_NORMALIZED_AST_SHA256 = (
    "ef9c204d3e0a97e4cca113da3aab99979efacb24085b96ffc51f3428d473087d")

RUNTIME_REL = ".cm2-runtime"
REJECTION_NAME = "c79g-v12-rejections-" + CHECKPOINT
CANDIDATE_A_NAME = "c79g-v12-candidate-a-" + CHECKPOINT
CANDIDATE_B_NAME = "c79g-v12-candidate-b-" + CHECKPOINT
VERIFICATION_A_NAME = "c79g-v12-verification-a-" + CHECKPOINT
VERIFICATION_B_NAME = "c79g-v12-verification-b-" + CHECKPOINT
COMPLETION_NAME = "c79g-v12-committed-completion-" + CHECKPOINT
AUTHORITY_NAME = "c79g-v12-" + CHECKPOINT + ".seal"

REQUIRED_EXEC_SEALS = (
    getattr(fcntl, "F_SEAL_WRITE", 0x0008)
    | getattr(fcntl, "F_SEAL_GROW", 0x0004)
    | getattr(fcntl, "F_SEAL_SHRINK", 0x0002)
    | getattr(fcntl, "F_SEAL_SEAL", 0x0001))
F_ADD_SEALS = getattr(fcntl, "F_ADD_SEALS", 1033)
F_GET_SEALS = getattr(fcntl, "F_GET_SEALS", 1034)
MFD_CLOEXEC = getattr(os, "MFD_CLOEXEC", 0x0001)
MFD_ALLOW_SEALING = getattr(os, "MFD_ALLOW_SEALING", 0x0002)


class BootstrapFailure(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if not condition:
        raise BootstrapFailure(message)


class OpenHow(ctypes.Structure):
    _fields_ = [
        ("flags", ctypes.c_uint64),
        ("mode", ctypes.c_uint64),
        ("resolve", ctypes.c_uint64),
    ]


LIBC = ctypes.CDLL(None, use_errno=True)
LIBC.syscall.restype = ctypes.c_long


def openat2(dir_fd: int, path: str | bytes, flags: int) -> int:
    raw = path if isinstance(path, bytes) else os.fsencode(path)
    need(raw not in (b"", b".") and not raw.startswith(b"/"),
         "openat2 path must be a nonempty root-relative label")
    need(b".." not in raw.split(b"/"), "openat2 path traversal forbidden")
    how = OpenHow(
        flags | os.O_CLOEXEC, 0,
        0x01 | 0x02 | 0x04 | 0x08)  # NO_XDEV|NO_MAGICLINKS|NO_SYMLINKS|BENEATH
    ctypes.set_errno(0)
    descriptor = LIBC.syscall(
        437, dir_fd, ctypes.c_char_p(raw), ctypes.byref(how), ctypes.sizeof(how))
    if descriptor < 0:
        code = ctypes.get_errno()
        raise OSError(code, os.strerror(code), os.fsdecode(raw))
    return int(descriptor)


def read_all(fd: int) -> bytes:
    os.lseek(fd, 0, os.SEEK_SET)
    chunks: list[bytes] = []
    while True:
        block = os.read(fd, 1 << 20)
        if not block:
            return b"".join(chunks)
        chunks.append(block)


def fingerprint(value: os.stat_result) -> tuple[int, ...]:
    return (
        value.st_dev, value.st_ino, value.st_mode, value.st_nlink,
        value.st_uid, value.st_gid, value.st_size,
        value.st_mtime_ns, value.st_ctime_ns)


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def strict_pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in items:
        need(key not in result, "duplicate JSON key: " + key)
        result[key] = value
    return result


def parse_object(raw: bytes) -> dict[str, Any]:
    value = json.loads(raw, object_pairs_hook=strict_pairs)
    need(isinstance(value, dict), "canonical object must be a JSON object")
    return value


def canonical_object_sha256(raw: bytes) -> str:
    value = parse_object(raw)
    declared = value.get("object_sha256")
    need(isinstance(declared, str), "canonical object declares object_sha256")
    material = dict(value)
    del material["object_sha256"]
    canonical = json.dumps(
        material, sort_keys=True, separators=(",", ":"),
        ensure_ascii=True, allow_nan=False).encode("ascii")
    digest = sha256(canonical)
    need(declared == digest, "declared canonical object SHA-256")
    return digest


def pin_normalized_launcher_ast_sha256(raw: bytes) -> str:
    try:
        tree = ast.parse(raw.decode("utf-8"), filename=LAUNCHER_REL, mode="exec")
    except (UnicodeDecodeError, SyntaxError) as exc:
        raise BootstrapFailure("launcher PIN_NORMALIZED AST parse") from exc
    flags = [
        node for node in tree.body
        if ((isinstance(node, ast.Assign) and len(node.targets) == 1 and
             isinstance(node.targets[0], ast.Name) and
             node.targets[0].id == "FINAL_BASE7_PINS_INSTALLED") or
            (isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name) and
             node.target.id == "FINAL_BASE7_PINS_INSTALLED"))]
    need(len(flags) == 1, "one final BASE7 flag")
    flags[0].value = ast.Constant(False)
    functions = [
        node for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and
        node.name == "configure_workspace_paths"]
    need(len(functions) == 1, "one workspace configurator")
    assignments = [
        node for node in functions[0].body
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and
        isinstance(node.targets[0], ast.Name) and node.targets[0].id == "BASE7_PINS"]
    need(len(assignments) == 1 and isinstance(assignments[0].value, ast.Dict),
         "one direct BASE7 map")
    table = assignments[0].value
    names = [key.id if isinstance(key, ast.Name) else None for key in table.keys]
    need(names == [
        "V11_OFFICIAL_REJECTION", "SCHEMA", "CONTRACT", "PRODUCER",
        "CONSUMER", "TRANSITION", "AUDIT"], "exact BASE7 order")
    predecessor = ast.dump(table.values[0], annotate_fields=True, include_attributes=False)
    for index, name in enumerate(names[1:], start=1):
        object_sentinel = "e" * 64 if name in {"CONTRACT", "TRANSITION", "AUDIT"} else None
        table.values[index] = ast.Tuple(
            elts=[ast.Constant("f" * 64), ast.Constant(object_sentinel)],
            ctx=ast.Load())
    need(ast.dump(table.values[0], annotate_fields=True,
                  include_attributes=False) == predecessor,
         "v11 rejection BASE7 pin preserved")
    return sha256(ast.dump(
        tree, annotate_fields=True, include_attributes=False).encode("utf-8"))


class HeldExact:
    def __init__(self, root_fd: int, relative: str, expected_file: str,
                 expected_object: str | None) -> None:
        self.relative = relative
        self.expected_file = expected_file
        self.expected_object = expected_object
        self.fd = openat2(root_fd, relative, os.O_RDONLY)
        try:
            self.before = os.fstat(self.fd)
            self.raw = read_all(self.fd)
            after = os.fstat(self.fd)
            need(stat.S_ISREG(self.before.st_mode) and
                 stat.S_IMODE(self.before.st_mode) == 0o444 and
                 self.before.st_nlink == 1,
                 relative + ": regular 0444 nlink1")
            need(fingerprint(self.before) == fingerprint(after),
                 relative + ": identity-bracketed read")
            need(sha256(self.raw) == expected_file, relative + ": file pin")
            if expected_object is not None:
                need(canonical_object_sha256(self.raw) == expected_object,
                     relative + ": object pin")
        except BaseException:
            os.close(self.fd)
            self.fd = -1
            raise

    def replay(self, root_fd: int) -> None:
        before = os.fstat(self.fd)
        raw = read_all(self.fd)
        after = os.fstat(self.fd)
        path_fd = openat2(root_fd, self.relative, os.O_RDONLY)
        try:
            path_state = os.fstat(path_fd)
            need(fingerprint(before) == fingerprint(self.before) ==
                 fingerprint(after) == fingerprint(path_state),
                 self.relative + ": terminal fd/path identity replay")
            need(raw == self.raw and sha256(raw) == self.expected_file,
                 self.relative + ": terminal byte replay")
        finally:
            os.close(path_fd)

    def close(self) -> None:
        if self.fd >= 0:
            os.close(self.fd)
            self.fd = -1


def verify_publication(held: tuple[HeldExact, ...]) -> None:
    need(len(held) == 10, "published exact10 count")
    need(len({(item.before.st_dev, item.before.st_ino) for item in held}) == 10,
         "published exact10 unique identities")
    need(len({item.before.st_dev for item in held}) == 1,
         "published exact10 single device")
    manifest = b"".join(
        (item.expected_file + "  " + item.relative + "\n").encode("ascii")
        for item in held[:8])
    need(held[8].raw == manifest, "ordered exact8 manifest bytes")
    outer = parse_object(held[9].raw)
    need(set(outer) == {
        "schema", "status", "effective_checkpoint_object_sha256",
        "exact8_ordered_entries", "cold_launch_manifest", "cold_launcher",
        "all_exact8_regular_0444_nlink1_and_held_for_runtime",
        "outer_published_after_exact8_manifest",
        "runtime_entry_must_be_cold_launcher",
        "sole_external_static_file_anchor_is_launcher_sha256",
        "declared_external_tcb", "formal_global_closure_credit", "D02_unlock",
        "runtime_executed_during_static_freeze", "object_sha256"},
         "v12 outer exact keyset")
    canonical_outer = json.dumps(
        outer, sort_keys=True, separators=(",", ":"), ensure_ascii=True,
        allow_nan=False).encode("ascii") + b"\n"
    need(held[9].raw == canonical_outer, "v12 outer canonical bytes")
    expected_entries = [
        {"file_sha256": item.expected_file, "path": item.relative}
        for item in held[:8]]
    need(
        outer.get("schema") ==
        "cm2.round306c79g.true-global-no-producer-consumer.cold-launch-outer-receipt.v12"
        and outer.get("status") ==
        "FROZEN_COLD_LAUNCH_OUTER_LAST__EXACT8_MANIFEST_CLOSED__RUNTIME_DEFERRED"
        and outer.get("effective_checkpoint_object_sha256") == CHECKPOINT
        and outer.get("exact8_ordered_entries") == expected_entries
        and outer.get("cold_launch_manifest") == {
            "file_sha256": EXPECTED_MANIFEST_SHA256,
            "ordered_entry_count": 8, "path": MANIFEST_REL}
        and outer.get("cold_launcher") == {
            "file_sha256": EXPECTED_LAUNCHER_SHA256, "path": LAUNCHER_REL}
        and outer.get("all_exact8_regular_0444_nlink1_and_held_for_runtime") is True
        and outer.get("outer_published_after_exact8_manifest") is True
        and outer.get("runtime_entry_must_be_cold_launcher") is True
        and outer.get("sole_external_static_file_anchor_is_launcher_sha256") is True
        and outer.get("declared_external_tcb") == [
            "EXTERNAL_HELD_FD_SEALED_MEMFD_BOOTSTRAP",
            "PYTHON3_ISOLATED_INTERPRETER",
            "LINUX_KERNEL_OPENAT2_STATX_MEMFD_PROCFS"]
        and outer.get("formal_global_closure_credit") == 0
        and outer.get("D02_unlock") is False
        and outer.get("runtime_executed_during_static_freeze") is False,
        "v12 outer-last publication closure")
    v11 = parse_object(held[0].raw)
    need(v11.get("schema") ==
         "cm2.round306c79g.true-global-no-producer-consumer.v11.later-rejection"
         and v11.get("status") == "PERMANENT_FAIL_CLOSED_REJECTION__ZERO_CREDIT"
         and v11.get("D02_unlock") is False and v11.get("D02_started") is False,
         "v11 is permanently rejected and cannot be rerun")
    need(pin_normalized_launcher_ast_sha256(held[7].raw) ==
         EXPECTED_PIN_NORMALIZED_AST_SHA256,
         "v12 launcher PIN_NORMALIZED AST")
    audit = parse_object(held[6].raw)
    dual = audit.get("dual_independent_static_checkers", {})
    checker_c = dual.get(
        "checker_C_common_census_and_pin_normalized_ast_reproduction", {})
    need(
        audit.get("status") ==
        "PASS_DUAL_STATIC_PIN_NORMALIZED_AST_GO_V12__"
        "PHYSICAL_COLD_FREEZE_PENDING__RUNTIME_NOT_AUTHORIZED"
        and dual.get("checker_A", {}).get(
            "pin_normalized_launcher_ast_sha256") ==
            EXPECTED_PIN_NORMALIZED_AST_SHA256
        and dual.get("checker_B", {}).get(
            "pin_normalized_launcher_ast_sha256") ==
            EXPECTED_PIN_NORMALIZED_AST_SHA256
        and checker_c.get("pin_normalized_launcher_ast_sha256") ==
            EXPECTED_PIN_NORMALIZED_AST_SHA256
        and dual.get("held_launcher_pin_normalized_ast_sha256") ==
            EXPECTED_PIN_NORMALIZED_AST_SHA256,
        "v12 audit PIN_NORMALIZED consensus")
    base_max = max(max(item.before.st_mtime_ns, item.before.st_ctime_ns)
                   for item in held[:8])
    manifest_min = min(held[8].before.st_mtime_ns, held[8].before.st_ctime_ns)
    manifest_max = max(held[8].before.st_mtime_ns, held[8].before.st_ctime_ns)
    outer_min = min(held[9].before.st_mtime_ns, held[9].before.st_ctime_ns)
    need(base_max < manifest_min and manifest_max < outer_min,
         "exact8 then manifest then outer-last chronology")


def parse_command(argv: list[str]) -> tuple[list[str], str, set[str]]:
    candidate_a_rel = RUNTIME_REL + "/" + CANDIDATE_A_NAME
    candidate_b_rel = RUNTIME_REL + "/" + CANDIDATE_B_NAME
    candidate_a_abs = ROOT_LABEL + "/" + candidate_a_rel
    candidate_b_abs = ROOT_LABEL + "/" + candidate_b_rel
    if len(argv) == 3 and argv[0] == "build" and argv[1] == "--outdir":
        if argv[2] in (candidate_a_rel, candidate_a_abs):
            return ["build", "--outdir", candidate_a_abs], "build-a", set()
        if argv[2] in (candidate_b_rel, candidate_b_abs):
            return ["build", "--outdir", candidate_b_abs], "build-b", {CANDIDATE_A_NAME}
    if argv == ["verify", "--orientation", "a"]:
        return list(argv), "verify-a", {CANDIDATE_A_NAME, CANDIDATE_B_NAME}
    if argv == ["verify", "--orientation", "b"]:
        return list(argv), "verify-b", {
            CANDIDATE_A_NAME, CANDIDATE_B_NAME, VERIFICATION_A_NAME}
    if argv == ["assemble"]:
        return list(argv), "assemble", {
            CANDIDATE_A_NAME, CANDIDATE_B_NAME,
            VERIFICATION_A_NAME, VERIFICATION_B_NAME}
    if argv == ["authorize"]:
        return list(argv), "authorize", {
            CANDIDATE_A_NAME, CANDIDATE_B_NAME, VERIFICATION_A_NAME,
            VERIFICATION_B_NAME, COMPLETION_NAME}
    if argv == ["reject"]:
        return list(argv), "reject", set()
    raise BootstrapFailure(
        "exactly one command required: build --outdir <exact A/B>, "
        "verify --orientation a/b, assemble, authorize, or reject")


def verify_directory_member(parent_fd: int, name: str, label: str) -> None:
    state = os.stat(name, dir_fd=parent_fd, follow_symlinks=False)
    need(stat.S_ISDIR(state.st_mode) and stat.S_IMODE(state.st_mode) == 0o555
         and state.st_nlink == 2, label + ": exact sealed directory")


def verify_runtime_phase(root_fd: int, phase: str, expected: set[str]) -> None:
    runtime_fd = openat2(root_fd, RUNTIME_REL, os.O_RDONLY | os.O_DIRECTORY)
    authority_fd = -1
    try:
        runtime_names = set(os.listdir(runtime_fd))
        if phase == "reject":
            return
        current_names = {name for name in runtime_names if "c79g-v12" in name}
        if phase == "build-a":
            need(current_names == set(),
                 "build-a requires wholly absent v12 runtime namespace")
        else:
            need(current_names == expected | {REJECTION_NAME},
                 phase + ": exact prior surfaces plus empty rejection namespace")
            verify_directory_member(runtime_fd, REJECTION_NAME,
                                    phase + " rejection namespace")
            rejection_fd = openat2(
                runtime_fd, REJECTION_NAME, os.O_RDONLY | os.O_DIRECTORY)
            try:
                need(os.listdir(rejection_fd) == [],
                     phase + ": rejection namespace exactly empty")
            finally:
                os.close(rejection_fd)
        for name in expected:
            verify_directory_member(runtime_fd, name, phase + " " + name)
        authority_fd = openat2(
            runtime_fd, "cm2-global-authority-heads",
            os.O_RDONLY | os.O_DIRECTORY)
        authority_names = {
            name for name in os.listdir(authority_fd) if "c79g-v12" in name}
        if phase == "authorize":
            need(authority_names in (set(), {AUTHORITY_NAME}),
                 "authorize permits absent or exact v12 authority")
            if authority_names:
                state = os.stat(AUTHORITY_NAME, dir_fd=authority_fd,
                                follow_symlinks=False)
                need(stat.S_ISREG(state.st_mode) and
                     stat.S_IMODE(state.st_mode) == 0o444 and state.st_nlink == 1,
                     "existing v12 authority exact frozen seal")
        else:
            need(authority_names == set(), phase + ": no v12 authority/stage")
    finally:
        if authority_fd >= 0:
            os.close(authority_fd)
        os.close(runtime_fd)


def make_sealed_exec(raw: bytes) -> int:
    need(hasattr(os, "memfd_create"), "Linux memfd_create required")
    descriptor = os.memfd_create(
        "c79g-v12-external-bootstrap", MFD_CLOEXEC | MFD_ALLOW_SEALING)
    try:
        offset = 0
        while offset < len(raw):
            written = os.write(descriptor, raw[offset:])
            need(written > 0, "complete sealed memfd write")
            offset += written
        os.fsync(descriptor)
        os.fchmod(descriptor, 0o444)
        fcntl.fcntl(descriptor, F_ADD_SEALS, REQUIRED_EXEC_SEALS)
        before = os.fstat(descriptor)
        replay = read_all(descriptor)
        after = os.fstat(descriptor)
        need(stat.S_ISREG(before.st_mode) and stat.S_IMODE(before.st_mode) == 0o444
             and before.st_nlink == 0 and fingerprint(before) == fingerprint(after)
             and fcntl.fcntl(descriptor, F_GET_SEALS) == REQUIRED_EXEC_SEALS
             and replay == raw and sha256(replay) == EXPECTED_LAUNCHER_SHA256,
             "fresh launcher memfd exact bytes/mode/nlink/seals")
        return descriptor
    except BaseException:
        os.close(descriptor)
        raise


def close_unlisted_fds(keep: set[int]) -> None:
    for name in os.listdir("/proc/self/fd"):
        try:
            descriptor = int(name)
        except ValueError:
            continue
        if descriptor > 2 and descriptor not in keep:
            try:
                os.close(descriptor)
            except OSError:
                pass


def main(argv: list[str] | None = None) -> int:
    forwarded, phase, expected = parse_command(
        list(sys.argv[1:] if argv is None else argv))
    slash_fd = os.open(
        "/", os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC | os.O_NOFOLLOW)
    root_fd = -1
    exec_fd = -1
    held: tuple[HeldExact, ...] = ()
    try:
        root_fd = openat2(slash_fd, ROOT_REL, os.O_RDONLY | os.O_DIRECTORY)
        root_before = os.fstat(root_fd)
        root_path = os.lstat(ROOT_LABEL)
        need(stat.S_ISDIR(root_before.st_mode) and
             fingerprint(root_before) == fingerprint(root_path),
             "workspace label equals held root identity")
        held = tuple(HeldExact(root_fd, *entry) for entry in EXACT10)
        try:
            verify_publication(held)
            verify_runtime_phase(root_fd, phase, expected)
            for item in held:
                item.replay(root_fd)
            launcher = held[7]
            need(launcher.relative == LAUNCHER_REL, "exact10 launcher position")
            exec_fd = make_sealed_exec(launcher.raw)
            need(len({exec_fd, launcher.fd, root_fd}) == 3 and
                 all(fd >= 3 for fd in (exec_fd, launcher.fd, root_fd)),
                 "three distinct inherited bootstrap descriptors")
            os.close(slash_fd)
            slash_fd = -1
            keep = {exec_fd, launcher.fd, root_fd}
            for item in held:
                if item is not launcher:
                    item.close()
            close_unlisted_fds(keep)
            for descriptor in keep:
                os.set_inheritable(descriptor, True)
            exec_argv = [
                PYTHON, "-I", "-B", "-S", "/proc/self/fd/" + str(exec_fd),
                "--bootstrap-exec-fd", str(exec_fd),
                "--bootstrap-source-fd", str(launcher.fd),
                "--bootstrap-root-fd", str(root_fd),
                "--cold-workspace-root", ROOT_LABEL,
                "--expected-launcher-sha256", EXPECTED_LAUNCHER_SHA256,
                *forwarded,
            ]
            clean_env = {
                "PATH": "/usr/bin:/bin", "LANG": "C.UTF-8",
                "LC_ALL": "C.UTF-8", "TZ": "UTC"}
            os.execve(PYTHON, exec_argv, clean_env)
        finally:
            for item in held:
                item.close()
    except (BootstrapFailure, AssertionError, OSError, ValueError,
            json.JSONDecodeError) as exc:
        os.write(2, ("C79G_V12_BOOTSTRAP_REJECT: " + str(exc) + "\n").encode())
        return 2
    finally:
        for descriptor in (exec_fd, root_fd, slash_fd):
            if descriptor >= 0:
                try:
                    os.close(descriptor)
                except OSError:
                    pass
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
