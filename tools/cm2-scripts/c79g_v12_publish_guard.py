#!/usr/bin/env python3
"""One-shot, fail-closed publisher for the final C79g v12 cold bundle.

Importing this module performs no I/O.  The read-only ``PREFLIGHT`` mode holds
the 96 identities that exist before publication.  The publishing mode keeps
the same official writer lock and held descriptors while it freezes exact8,
creates the manifest with O_EXCL, creates the outer receipt last with O_EXCL,
fsyncs every boundary, and terminally replays all 98 identities.

This program never imports or executes any C79g protocol source.
"""

from __future__ import annotations

import ast
import ctypes
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import sys
from typing import Any


FINAL_V12_PUBLISH_PINS_INSTALLED = True
CHECKPOINT = "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab"
BASENAME = "cm2_round306c79g_true_global_no_producer_consumer"
ROOT_EXPECTED = Path(
    "/home/qian-qi/.openclaw/workspaces/telegram-bot-8449317572")

V11_REJECTION = (
    f".cm2-runtime/c79g-v11-rejections-{CHECKPOINT}/rejection.json",
    "f6cc10d8b7e72553ef0b7a32bbfb99255f36cce16b735002f17be58ae51d3bc8",
    "7ae86e38c5910bc9ceaa0a4e5cb1f8fbbf1e73de9c0314fedabbd8cb2db3bb7a",
)
SCHEMA_V12 = (
    f"deliverables/{BASENAME}_schema_v12.json",
    "5ed911a55e8f90e750fdcaf6ab4fb6c9683bebaf66a4d6250329dff98acb2e28",
    None,
)
CONTRACT_V12 = (
    f"deliverables/{BASENAME}_contract_v12.json",
    "72246725b15891f92cbc6e3fa1c07ab4a76cdaa19f1b366a736f47f51989b343",
    "f5c1710817dc8e3aa7fe2bbf4b88e6e39baaa1b17bbeb0f8bf37c8c4575ae5d7",
)
PRODUCER_V12 = (
    f"deliverables/{BASENAME}_v12.py",
    "4cafc594f8a60063b7e7caaa82ddcc2b7983d0fbf0929034cd3cb5f360f3ed1d",
    None,
)
CONSUMER_V12 = (
    f"deliverables/{BASENAME}_independent_verifier_assembler_authority_consumer_v12.py",
    "b74dee738257d485e9ca3357d7d138b5175b95e58f1c8ea87d1eca7bfc96b2ed",
    None,
)
TRANSITION_V12 = (
    f"deliverables/{BASENAME}_v11_to_v12_static_launch_transition_receipt_v1.json",
    "45dabc1ef60eb2f8ba34aa7daa69f9d2b3bedccd4168d9c472bd4bbb696b5400",
    "0673ecafaa9991cd78e905e144e7c8c1b91717a3d753befa13e82552d44a4072",
)
AUDIT_V12 = (
    f"deliverables/{BASENAME}_static_audit_v12.json",
    "ac29b1e31e0d1b51e8610b7699d1aaf55c80fa6f13f00b20b209c2889e121d37",
    "c1473ae0f5a08d8772227f61a55bd32c479a7b5c7d40da17b37e796abf4d9783",
)
LAUNCHER_V12 = (
    f"deliverables/{BASENAME}_cold_launch_v12.py",
    "b7aaff67be866f8fd7a01f71e97ea1491574f69e62b7760b6ced9183997444ba",
    None,
)
MANIFEST_REL = f"deliverables/{BASENAME}_cold_launch_manifest_v12.sha256"
OUTER_REL = f"deliverables/{BASENAME}_cold_launch_outer_receipt_v12.json"
V4_RECEIPT_REL = f"deliverables/{BASENAME}_v4_rejection_supersession_receipt_v1.json"
V12_REJECTION_NS = f".cm2-runtime/c79g-v12-rejections-{CHECKPOINT}"
PIN_NORMALIZED_LAUNCHER_AST_SHA256 = (
    "ef9c204d3e0a97e4cca113da3aab99979efacb24085b96ffc51f3428d473087d")

V12_RUNTIME_SURFACES = (
    f".cm2-runtime/c79g-v12-candidate-a-{CHECKPOINT}",
    f".cm2-runtime/c79g-v12-candidate-b-{CHECKPOINT}",
    f".cm2-runtime/c79g-v12-verification-a-{CHECKPOINT}",
    f".cm2-runtime/c79g-v12-verification-b-{CHECKPOINT}",
    f".cm2-runtime/c79g-v12-committed-completion-{CHECKPOINT}",
    f".cm2-runtime/cm2-global-authority-heads/c79g-v12-{CHECKPOINT}.seal",
    f".cm2-runtime/.c79g-v12-candidate-stage-a-{CHECKPOINT}",
    f".cm2-runtime/.c79g-v12-candidate-stage-b-{CHECKPOINT}",
    f".cm2-runtime/.c79g-v12-verification-stage-a-{CHECKPOINT}",
    f".cm2-runtime/.c79g-v12-verification-stage-b-{CHECKPOINT}",
    f".cm2-runtime/.c79g-v12-completion-stage-{CHECKPOINT}",
    f".cm2-runtime/cm2-global-authority-heads/.c79g-v12-authority-stage-{CHECKPOINT}.seal",
    V12_REJECTION_NS,
)


def current_exact8() -> tuple[tuple[str, str, str | None], ...]:
    return (
        V11_REJECTION, SCHEMA_V12, CONTRACT_V12, PRODUCER_V12,
        CONSUMER_V12, TRANSITION_V12, AUDIT_V12, LAUNCHER_V12,
    )


def strict_pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in items:
        assert key not in result, f"duplicate JSON key: {key}"
        result[key] = value
    return result


def canonical(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=True,
        allow_nan=False).encode("ascii")


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def verify_object(raw: bytes, expected: str | None) -> dict[str, Any]:
    value = json.loads(raw, object_pairs_hook=strict_pairs)
    assert isinstance(value, dict)
    claim = value.get("object_sha256")
    if expected is not None:
        assert claim == expected, (claim, expected)
    if claim is not None:
        assert isinstance(claim, str) and re.fullmatch(r"[0-9a-f]{64}", claim)
        body = dict(value)
        del body["object_sha256"]
        assert sha256(canonical(body)) == claim
    return value


def close_object(body: dict[str, Any]) -> dict[str, Any]:
    assert "object_sha256" not in body
    result = dict(body)
    result["object_sha256"] = sha256(canonical(body))
    return result


def expected_publication(
        exact8: tuple[tuple[str, str, str | None], ...],
        ) -> tuple[bytes, str, bytes, str, str]:
    assert len(exact8) == 8
    entries = [{"path": rel, "file_sha256": file_sha}
               for rel, file_sha, _ in exact8]
    manifest_raw = b"".join(
        f"{item['file_sha256']}  {item['path']}\n".encode("ascii")
        for item in entries)
    manifest_sha = sha256(manifest_raw)
    outer = close_object({
        "schema": (
            "cm2.round306c79g.true-global-no-producer-consumer."
            "cold-launch-outer-receipt.v12"),
        "status": (
            "FROZEN_COLD_LAUNCH_OUTER_LAST__EXACT8_MANIFEST_CLOSED__"
            "RUNTIME_DEFERRED"),
        "effective_checkpoint_object_sha256": CHECKPOINT,
        "exact8_ordered_entries": entries,
        "cold_launch_manifest": {
            "path": MANIFEST_REL,
            "file_sha256": manifest_sha,
            "ordered_entry_count": 8,
        },
        "cold_launcher": {
            "path": LAUNCHER_V12[0],
            "file_sha256": LAUNCHER_V12[1],
        },
        "all_exact8_regular_0444_nlink1_and_held_for_runtime": True,
        "outer_published_after_exact8_manifest": True,
        "runtime_entry_must_be_cold_launcher": True,
        "sole_external_static_file_anchor_is_launcher_sha256": True,
        "declared_external_tcb": [
            "EXTERNAL_HELD_FD_SEALED_MEMFD_BOOTSTRAP",
            "PYTHON3_ISOLATED_INTERPRETER",
            "LINUX_KERNEL_OPENAT2_STATX_MEMFD_PROCFS",
        ],
        "formal_global_closure_credit": 0,
        "D02_unlock": False,
        "runtime_executed_during_static_freeze": False,
    })
    outer_raw = canonical(outer) + b"\n"
    return (manifest_raw, manifest_sha, outer_raw, sha256(outer_raw),
            outer["object_sha256"])


AT_EMPTY_PATH = 0x1000
AT_SYMLINK_NOFOLLOW = 0x100
STATX_BASIC_STATS = 0x000007ff
STATX_MNT_ID = 0x00001000


class StatxTimestamp(ctypes.Structure):
    _fields_ = [
        ("tv_sec", ctypes.c_int64), ("tv_nsec", ctypes.c_uint32),
        ("reserved", ctypes.c_int32),
    ]


class Statx(ctypes.Structure):
    _fields_ = [
        ("stx_mask", ctypes.c_uint32), ("stx_blksize", ctypes.c_uint32),
        ("stx_attributes", ctypes.c_uint64), ("stx_nlink", ctypes.c_uint32),
        ("stx_uid", ctypes.c_uint32), ("stx_gid", ctypes.c_uint32),
        ("stx_mode", ctypes.c_uint16), ("spare0", ctypes.c_uint16),
        ("stx_ino", ctypes.c_uint64), ("stx_size", ctypes.c_uint64),
        ("stx_blocks", ctypes.c_uint64),
        ("stx_attributes_mask", ctypes.c_uint64),
        ("stx_atime", StatxTimestamp), ("stx_btime", StatxTimestamp),
        ("stx_ctime", StatxTimestamp), ("stx_mtime", StatxTimestamp),
        ("stx_rdev_major", ctypes.c_uint32),
        ("stx_rdev_minor", ctypes.c_uint32),
        ("stx_dev_major", ctypes.c_uint32),
        ("stx_dev_minor", ctypes.c_uint32),
        ("stx_mnt_id", ctypes.c_uint64),
        ("stx_dio_mem_align", ctypes.c_uint32),
        ("stx_dio_offset_align", ctypes.c_uint32),
        ("spare3", ctypes.c_uint64 * 12),
    ]


def fd_mount_id(fd: int) -> int:
    """Require both statx(AT_EMPTY_PATH) and proc fdinfo to name one mount."""
    library = ctypes.CDLL(None, use_errno=True)
    assert hasattr(library, "statx")
    info = Statx()
    ctypes.set_errno(0)
    outcome = library.statx(
        ctypes.c_int(fd), ctypes.c_char_p(b""),
        ctypes.c_int(AT_EMPTY_PATH | AT_SYMLINK_NOFOLLOW),
        ctypes.c_uint(STATX_BASIC_STATS | STATX_MNT_ID), ctypes.byref(info))
    assert outcome == 0 and bool(info.stx_mask & STATX_MNT_ID)
    statx_id = int(info.stx_mnt_id)
    assert statx_id > 0
    raw = Path(f"/proc/self/fdinfo/{fd}").read_text(encoding="ascii")
    rows = [line for line in raw.splitlines() if line.startswith("mnt_id:\t")]
    assert len(rows) == 1
    proc_id = int(rows[0].split("\t", 1)[1])
    assert proc_id == statx_id
    return statx_id


class Held:
    def __init__(self, root: Path, rel: str, file_sha: str,
                 object_sha: str | None, allowed_modes: set[int]):
        self._set_names(root, rel, file_sha, object_sha)
        path_state = os.lstat(self.path)
        assert stat.S_ISREG(path_state.st_mode) and not stat.S_ISLNK(path_state.st_mode)
        assert path_state.st_nlink == 1
        self.fd = os.open(
            self.path, os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC |
            getattr(os, "O_NOATIME", 0))
        try:
            self.before = os.fstat(self.fd)
            assert self.fingerprint(path_state) == self.fingerprint(self.before)
            assert stat.S_IMODE(self.before.st_mode) in allowed_modes
            self.mount_id = fd_mount_id(self.fd)
            raw = self.read()
            assert sha256(raw) == file_sha, (rel, sha256(raw), file_sha)
            if object_sha is not None:
                verify_object(raw, object_sha)
        except BaseException:
            os.close(self.fd)
            raise

    def _set_names(self, root: Path, rel: str, file_sha: str,
                   object_sha: str | None) -> None:
        assert rel and not rel.startswith("/") and ".." not in Path(rel).parts
        assert re.fullmatch(r"[0-9a-f]{64}", file_sha)
        assert object_sha is None or re.fullmatch(r"[0-9a-f]{64}", object_sha)
        self.root = root
        self.rel = rel
        self.path = root / rel
        self.file_sha = file_sha
        self.object_sha = object_sha

    @classmethod
    def create_exclusive(cls, root: Path, rel: str, raw: bytes,
                         object_sha: str | None) -> "Held":
        self = cls.__new__(cls)
        self._set_names(root, rel, sha256(raw), object_sha)
        relative = Path(rel)
        assert len(relative.parts) == 2 and relative.parts[0] == "deliverables"
        parent = root / relative.parent
        parent_fd = os.open(
            parent, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC)
        try:
            self.fd = os.open(
                relative.name,
                os.O_RDWR | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW | os.O_CLOEXEC,
                0o444, dir_fd=parent_fd)
        finally:
            os.close(parent_fd)
        try:
            offset = 0
            while offset < len(raw):
                count = os.write(self.fd, raw[offset:])
                assert count > 0
                offset += count
            os.fsync(self.fd)
            os.fchmod(self.fd, 0o444)
            os.fsync(self.fd)
            self.before = os.fstat(self.fd)
            self.mount_id = fd_mount_id(self.fd)
            path_state = os.lstat(self.path)
            assert self.fingerprint(path_state) == self.fingerprint(self.before)
            assert stat.S_IMODE(self.before.st_mode) == 0o444
            assert self.before.st_nlink == 1 and self.before.st_size == len(raw)
            assert self.read() == raw
            if object_sha is not None:
                verify_object(raw, object_sha)
            return self
        except BaseException:
            os.close(self.fd)
            raise

    @staticmethod
    def fingerprint(value: os.stat_result) -> tuple[int, int, int, int, int, int]:
        return (value.st_dev, value.st_ino, value.st_size, value.st_nlink,
                value.st_mtime_ns, value.st_ctime_ns)

    def read(self) -> bytes:
        os.lseek(self.fd, 0, os.SEEK_SET)
        chunks: list[bytes] = []
        while True:
            block = os.read(self.fd, 1 << 20)
            if not block:
                return b"".join(chunks)
            chunks.append(block)

    def freeze(self) -> os.stat_result:
        os.fsync(self.fd)
        if stat.S_IMODE(os.fstat(self.fd).st_mode) != 0o444:
            os.fchmod(self.fd, 0o444)
        os.fsync(self.fd)
        return self.replay()[0]

    def replay(self) -> tuple[os.stat_result, bytes]:
        path_state = os.lstat(self.path)
        fd_state = os.fstat(self.fd)
        assert stat.S_ISREG(path_state.st_mode) and not stat.S_ISLNK(path_state.st_mode)
        assert (path_state.st_dev, path_state.st_ino) == (fd_state.st_dev, fd_state.st_ino)
        assert stat.S_IMODE(fd_state.st_mode) == 0o444 and fd_state.st_nlink == 1
        assert fd_state.st_mtime_ns <= fd_state.st_ctime_ns
        assert fd_mount_id(self.fd) == self.mount_id
        raw = self.read()
        assert sha256(raw) == self.file_sha
        if self.object_sha is not None:
            verify_object(raw, self.object_sha)
        return fd_state, raw

    def close(self) -> None:
        try:
            os.close(self.fd)
        except OSError:
            pass


def add_expected(expected: dict[str, tuple[str, str | None]],
                 item: dict[str, Any]) -> None:
    assert set(item) >= {"path", "file_sha256"}
    rel, file_sha = item["path"], item["file_sha256"]
    object_sha = item.get("object_sha256")
    assert isinstance(rel, str) and isinstance(file_sha, str)
    assert re.fullmatch(r"[0-9a-f]{64}", file_sha)
    assert object_sha is None or (
        isinstance(object_sha, str) and re.fullmatch(r"[0-9a-f]{64}", object_sha))
    if rel in expected:
        old_file, old_object = expected[rel]
        assert old_file == file_sha
        if old_object is not None and object_sha is not None:
            assert old_object == object_sha
        expected[rel] = (old_file, old_object or object_sha)
    else:
        expected[rel] = (file_sha, object_sha)


def ordered_exact10(segment: dict[str, Any], key: str) -> list[dict[str, Any]]:
    ordered = segment[key]
    assert isinstance(ordered, list) and len(ordered) == 10
    assert len({item["path"] for item in ordered}) == 10
    return ordered


def build_expected(contract: dict[str, Any], v4_receipt: dict[str, Any],
                   exact8: tuple[tuple[str, str, str | None], ...],
                   ) -> dict[str, tuple[str, str | None]]:
    expected: dict[str, tuple[str, str | None]] = {}
    predecessor_v3 = contract["append_only_predecessor_v3"]
    for item in ordered_exact10(predecessor_v3, "ordered_exact10"):
        add_expected(expected, item)
    add_expected(expected, predecessor_v3["official_later_rejection"])

    v4_members = v4_receipt["frozen_v4_provisional_exact8"]["ordered_members"]
    assert isinstance(v4_members, list) and len(v4_members) == 8
    for item in v4_members:
        add_expected(expected, item)
    add_expected(expected, contract["rejected_unpublished_predecessor_v4"]["supersession_receipt"])

    for version in ("v5", "v6", "v7", "v8", "v9", "v10", "v11"):
        segment = contract[f"published_then_officially_rejected_predecessor_{version}"]
        for item in ordered_exact10(segment, "ordered_published_exact10"):
            add_expected(expected, item)
        add_expected(expected, segment["official_later_rejection"])

    for rel, file_sha, object_sha in exact8:
        item: dict[str, Any] = {"path": rel, "file_sha256": file_sha}
        if object_sha is not None:
            item["object_sha256"] = object_sha
        add_expected(expected, item)
    assert len(expected) == 96, len(expected)
    return expected


def pin_normalized_launcher_ast_sha256(raw: bytes) -> str:
    tree = ast.parse(raw.decode("utf-8"), filename=LAUNCHER_V12[0], mode="exec")
    flags = [
        node for node in tree.body
        if ((isinstance(node, ast.Assign) and len(node.targets) == 1 and
             isinstance(node.targets[0], ast.Name) and
             node.targets[0].id == "FINAL_BASE7_PINS_INSTALLED") or
            (isinstance(node, ast.AnnAssign) and
             isinstance(node.target, ast.Name) and
             node.target.id == "FINAL_BASE7_PINS_INSTALLED"))]
    assert len(flags) == 1
    flags[0].value = ast.Constant(False)
    configurators = [
        node for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and
        node.name == "configure_workspace_paths"]
    assert len(configurators) == 1
    tables = [
        node for node in configurators[0].body
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and
        isinstance(node.targets[0], ast.Name) and
        node.targets[0].id == "BASE7_PINS"]
    assert len(tables) == 1 and isinstance(tables[0].value, ast.Dict)
    table = tables[0].value
    names = [key.id if isinstance(key, ast.Name) else None for key in table.keys]
    assert names == [
        "V11_OFFICIAL_REJECTION", "SCHEMA", "CONTRACT", "PRODUCER",
        "CONSUMER", "TRANSITION", "AUDIT"]
    predecessor = ast.dump(table.values[0], annotate_fields=True, include_attributes=False)
    for index, name in enumerate(names[1:], start=1):
        object_sentinel = "e" * 64 if name in {"CONTRACT", "TRANSITION", "AUDIT"} else None
        table.values[index] = ast.Tuple(
            elts=[ast.Constant("f" * 64), ast.Constant(object_sentinel)],
            ctx=ast.Load())
    assert ast.dump(table.values[0], annotate_fields=True,
                    include_attributes=False) == predecessor
    normalized = ast.dump(
        tree, annotate_fields=True, include_attributes=False).encode("utf-8")
    return sha256(normalized)


def verify_static_audit(audit: dict[str, Any], launcher_raw: bytes) -> None:
    assert audit["status"] == (
        "PASS_DUAL_STATIC_PIN_NORMALIZED_AST_GO_V12__"
        "PHYSICAL_COLD_FREEZE_PENDING__RUNTIME_NOT_AUTHORIZED")
    bundle = audit["audited_v12_bundle"]
    expected = {
        "closed_schema": SCHEMA_V12,
        "contract": CONTRACT_V12,
        "build_only_producer": PRODUCER_V12,
        "independent_verifier_assembler_authority_consumer": CONSUMER_V12,
        "v11_to_v12_transition_receipt": TRANSITION_V12,
    }
    for name, (rel, file_sha, object_sha) in expected.items():
        assert bundle[name]["path"] == rel
        assert bundle[name]["file_sha256"] == file_sha
        if object_sha is not None:
            assert bundle[name]["object_sha256"] == object_sha
    actual_normalized = pin_normalized_launcher_ast_sha256(launcher_raw)
    assert actual_normalized == PIN_NORMALIZED_LAUNCHER_AST_SHA256
    dual = audit["dual_independent_static_checkers"]
    checker_c = dual["checker_C_common_census_and_pin_normalized_ast_reproduction"]
    assert dual["checker_A"]["pin_normalized_launcher_ast_sha256"] == actual_normalized
    assert dual["checker_B"]["pin_normalized_launcher_ast_sha256"] == actual_normalized
    assert checker_c["pin_normalized_launcher_ast_sha256"] == actual_normalized
    assert dual["held_launcher_pin_normalized_ast_sha256"] == actual_normalized
    assert audit["static_credit_census"]["all_persisted_v12_objects_D02_unlock"] is False
    assert audit["static_credit_census"]["all_persisted_v12_objects_formal_global_closure_credit"] == 0
    assert audit["static_no_run"]["C79_v12_runtime_artifact_count"] == 0
    assert audit["final_audit_acceptance"]["this_audit_authorizes_C79_runtime"] is False
    assert audit["final_audit_acceptance"][
        "requires_cold_exact8_freeze_manifest_then_outer_last_and_terminal_replay"] is True


def fsync_dir(path: Path) -> None:
    descriptor = os.open(
        path, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def assert_v12_runtime_absent(root: Path) -> None:
    for rel in V12_RUNTIME_SURFACES:
        assert not os.path.lexists(root / rel), rel
    runtime = root / ".cm2-runtime"
    for directory, names, files in os.walk(runtime, followlinks=False):
        for name in [*names, *files]:
            assert "c79g-v12" not in name.lower(), str(Path(directory) / name)


def assert_v12_unpublished(root: Path) -> None:
    assert not os.path.lexists(root / MANIFEST_REL)
    assert not os.path.lexists(root / OUTER_REL)
    assert_v12_runtime_absent(root)


def exact_rejection_namespace(root: Path, version: str,
                              held: dict[str, Held]) -> None:
    rel = f".cm2-runtime/c79g-{version}-rejections-{CHECKPOINT}"
    path_state = os.lstat(root / rel)
    assert stat.S_ISDIR(path_state.st_mode) and not stat.S_ISLNK(path_state.st_mode)
    descriptor = os.open(
        root / rel, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW |
        os.O_CLOEXEC | getattr(os, "O_NOATIME", 0))
    try:
        fd_state = os.fstat(descriptor)
        mount_id = fd_mount_id(descriptor)
        assert (path_state.st_dev, path_state.st_ino) == (fd_state.st_dev, fd_state.st_ino)
        assert stat.S_IMODE(fd_state.st_mode) == 0o555 and fd_state.st_nlink == 2
        assert os.listdir(descriptor) == ["rejection.json"]
    finally:
        os.close(descriptor)
    member = held[f"{rel}/rejection.json"]
    member_state = os.fstat(member.fd)
    assert member_state.st_dev == fd_state.st_dev and member.mount_id == mount_id
    assert stat.S_IMODE(member_state.st_mode) == 0o444 and member_state.st_nlink == 1


def verify_contract_paths(
        contract: dict[str, Any],
        exact8: tuple[tuple[str, str, str | None], ...]) -> None:
    paths = [rel for rel, _, _ in exact8]
    assert contract["effective_checkpoint_object_sha256"] == CHECKPOINT
    assert contract["status"] == (
        "STATIC_CONTRACT_BYTES_FINAL__COLD_FREEZE_PENDING__"
        "RUNTIME_NOT_AUTHORIZED")
    bundle = contract["v12_bundle"]
    assert bundle["base7_ordered_paths"] == paths[:7]
    assert bundle["exact8_ordered_paths"] == paths
    assert bundle["exact10_ordered_paths"] == paths + [MANIFEST_REL, OUTER_REL]
    assert bundle["cold_launch_outer_closure"][
        "current_v12_exact10_plus_all_append_only_predecessors_unique_file_identity_count"] == 98
    publication = contract["exact_publication_paths"]
    assert publication["v12_rejection_namespace"] == V12_REJECTION_NS
    assert publication["cold_launch_exact8_manifest"] == MANIFEST_REL
    assert publication["cold_launch_outer_last"] == OUTER_REL
    assert publication["cold_launcher"] == LAUNCHER_V12[0]
    assert paths[0] == V11_REJECTION[0]
    contract_runtime = {
        publication["candidate_A"], publication["candidate_B"],
        publication["verification_A"], publication["verification_B"],
        publication["committed_completion"], publication["authority_seal"],
        publication["completion_staging_path"], publication["authority_staging_path"],
        V12_REJECTION_NS,
        publication["candidate_staging_path_template"].replace("{a|b}", "a"),
        publication["candidate_staging_path_template"].replace("{a|b}", "b"),
        publication["verification_staging_path_template"].replace("{a|b}", "a"),
        publication["verification_staging_path_template"].replace("{a|b}", "b"),
    }
    assert contract_runtime == set(V12_RUNTIME_SURFACES)


def main() -> int:
    if not __debug__:
        raise RuntimeError("python -O is forbidden for the publication guard")
    assert FINAL_V12_PUBLISH_PINS_INSTALLED is True
    assert len(sys.argv) in {2, 3}
    preflight = len(sys.argv) == 3
    if preflight:
        assert sys.argv[2] == "PREFLIGHT"
    root = Path(sys.argv[1]).resolve(strict=True)
    assert root == ROOT_EXPECTED
    runtime = root / ".cm2-runtime"
    runtime_state = os.lstat(runtime)
    assert stat.S_ISDIR(runtime_state.st_mode) and not stat.S_ISLNK(runtime_state.st_mode)
    lock_fd = os.open(
        runtime, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC |
        getattr(os, "O_NOATIME", 0))
    fcntl.flock(lock_fd, fcntl.LOCK_EX)
    held: dict[str, Held] = {}
    opened: list[Held] = []
    try:
        assert_v12_unpublished(root)
        exact8 = current_exact8()
        manifest_raw, manifest_sha, outer_raw, outer_sha, outer_object = (
            expected_publication(exact8))
        assert manifest_sha == "297e9f58dc7657c6fa959dd45081efffe4e7e8dadcd16ab89457863e2661ece6"
        assert outer_sha == "27129990a9d5b6697fd13ee8e2086100cbf158f12e5b767166d771e63088b6d0"
        assert outer_object == "bc6d06141865954590bd11bfc96ad59dbbffa003f568355ecb47155a8a3a809d"

        contract_seed = Held(root, *CONTRACT_V12, {0o444, 0o644, 0o664})
        opened.append(contract_seed)
        contract = verify_object(contract_seed.read(), CONTRACT_V12[2])
        verify_contract_paths(contract, exact8)
        v4_ref = contract["rejected_unpublished_predecessor_v4"]["supersession_receipt"]
        assert v4_ref["path"] == V4_RECEIPT_REL
        v4_seed = Held(root, V4_RECEIPT_REL, v4_ref["file_sha256"],
                       v4_ref["object_sha256"], {0o444})
        opened.append(v4_seed)
        v4_receipt = verify_object(v4_seed.read(), v4_ref["object_sha256"])
        expected = build_expected(contract, v4_receipt, exact8)

        preopened = {CONTRACT_V12[0]: contract_seed, V4_RECEIPT_REL: v4_seed}
        current_paths = {rel for rel, _, _ in exact8}
        historical_paths = set(expected) - (current_paths - {V11_REJECTION[0]})
        for rel, (file_sha, object_sha) in expected.items():
            item = preopened.pop(rel, None)
            if item is None:
                modes = ({0o444, 0o644, 0o664}
                         if rel in current_paths and rel not in historical_paths
                         else {0o444})
                item = Held(root, rel, file_sha, object_sha, modes)
                opened.append(item)
            held[rel] = item
        assert not preopened and len(held) == 96
        identities = {(item.before.st_dev, item.before.st_ino) for item in held.values()}
        assert len(identities) == 96
        assert len({item.before.st_dev for item in held.values()}) == 1
        assert len({item.mount_id for item in held.values()}) == 1

        audit = verify_object(held[AUDIT_V12[0]].read(), AUDIT_V12[2])
        verify_static_audit(audit, held[LAUNCHER_V12[0]].read())
        v11 = verify_object(held[V11_REJECTION[0]].read(), V11_REJECTION[2])
        assert v11["status"] == "PERMANENT_FAIL_CLOSED_REJECTION__ZERO_CREDIT"
        assert v11["D02_unlock"] is False and v11["D02_started"] is False
        for version in ("v3", "v5", "v6", "v7", "v8", "v9", "v10", "v11"):
            exact_rejection_namespace(root, version, held)
        assert_v12_unpublished(root)

        if preflight:
            print(canonical({
                "status": "PREFLIGHT_96_EXISTING_FILE_READ_ONLY_PASS_UNDER_OFFICIAL_LOCK_V12",
                "held_unique_files": 96,
                "same_st_dev_and_statx_mount_id": True,
                "v11_permanent_rejection_held_and_replayed": True,
                "pin_normalized_launcher_ast_sha256": PIN_NORMALIZED_LAUNCHER_AST_SHA256,
                "no_chmod_or_publication_write_performed": True,
                "manifest_absent": True,
                "outer_absent": True,
                "all_v12_runtime_and_rejection_surfaces_absent": True,
                "mechanical_manifest_sha256": manifest_sha,
                "mechanical_outer_file_sha256": outer_sha,
                "mechanical_outer_object_sha256": outer_object,
            }).decode("ascii"), flush=True)
            return 0

        base_stats = [held[rel].freeze() for rel, _, _ in exact8]
        fsync_dir(root / "deliverables")
        fsync_dir(root / V11_REJECTION[0].rsplit("/", 1)[0])
        fsync_dir(runtime)
        fsync_dir(root)
        assert_v12_unpublished(root)
        base_max = max(max(item.st_mtime_ns, item.st_ctime_ns) for item in base_stats)

        manifest = Held.create_exclusive(root, MANIFEST_REL, manifest_raw, None)
        opened.append(manifest)
        held[MANIFEST_REL] = manifest
        fsync_dir(root / "deliverables")
        fsync_dir(root)
        manifest_state = os.fstat(manifest.fd)
        assert base_max < min(manifest_state.st_mtime_ns, manifest_state.st_ctime_ns)
        assert not os.path.lexists(root / OUTER_REL)
        assert_v12_runtime_absent(root)

        outer = Held.create_exclusive(root, OUTER_REL, outer_raw, outer_object)
        opened.append(outer)
        held[OUTER_REL] = outer
        fsync_dir(root / "deliverables")
        fsync_dir(runtime)
        fsync_dir(root)
        outer_state = os.fstat(outer.fd)
        assert max(manifest_state.st_mtime_ns, manifest_state.st_ctime_ns) < min(
            outer_state.st_mtime_ns, outer_state.st_ctime_ns)
        assert_v12_runtime_absent(root)

        assert len(held) == 98
        replay = {rel: item.replay() for rel, item in held.items()}
        assert len({(state.st_dev, state.st_ino) for state, _ in replay.values()}) == 98
        assert len({state.st_dev for state, _ in replay.values()}) == 1
        assert len({held[rel].mount_id for rel in replay}) == 1
        history = [ordered_exact10(contract["append_only_predecessor_v3"], "ordered_exact10")]
        for version in ("v5", "v6", "v7", "v8", "v9", "v10", "v11"):
            history.append(ordered_exact10(
                contract[f"published_then_officially_rejected_predecessor_{version}"],
                "ordered_published_exact10"))
        for ordered in history:
            historical_manifest = b"".join(
                (entry["file_sha256"] + "  " + entry["path"] + "\n").encode("ascii")
                for entry in ordered[:8])
            assert replay[ordered[8]["path"]][1] == historical_manifest
        for version in ("v3", "v5", "v6", "v7", "v8", "v9", "v10", "v11"):
            exact_rejection_namespace(root, version, held)
        assert replay[MANIFEST_REL][1] == manifest_raw
        assert replay[OUTER_REL][1] == outer_raw
        base_stats = [replay[rel][0] for rel, _, _ in exact8]
        manifest_state = replay[MANIFEST_REL][0]
        outer_state = replay[OUTER_REL][0]
        base_max = max(max(item.st_mtime_ns, item.st_ctime_ns) for item in base_stats)
        assert base_max < min(manifest_state.st_mtime_ns, manifest_state.st_ctime_ns)
        assert max(manifest_state.st_mtime_ns, manifest_state.st_ctime_ns) < min(
            outer_state.st_mtime_ns, outer_state.st_ctime_ns)
        verify_static_audit(audit, replay[LAUNCHER_V12[0]][1])
        assert_v12_runtime_absent(root)
        fsync_dir(root / "deliverables")
        fsync_dir(runtime)
        fsync_dir(root)
        print(canonical({
            "status": "TERMINAL_98_FILE_REPLAY_PASS_UNDER_SAME_OFFICIAL_LOCK_V12",
            "unique_files": 98,
            "same_st_dev_and_statx_mount_id": True,
            "v11_permanent_rejection_preserved_no_rerun": True,
            "pin_normalized_launcher_ast_sha256": PIN_NORMALIZED_LAUNCHER_AST_SHA256,
            "base_max_ns": base_max,
            "manifest_mtime_ns": manifest_state.st_mtime_ns,
            "manifest_ctime_ns": manifest_state.st_ctime_ns,
            "outer_mtime_ns": outer_state.st_mtime_ns,
            "outer_ctime_ns": outer_state.st_ctime_ns,
            "manifest_sha256": manifest_sha,
            "outer_file_sha256": outer_sha,
            "outer_object_sha256": outer_object,
            "all_v12_runtime_and_rejection_surfaces_absent": True,
        }).decode("ascii"), flush=True)
        return 0
    finally:
        seen: set[int] = set()
        for item in opened:
            if id(item) not in seen:
                seen.add(id(item))
                item.close()
        fcntl.flock(lock_fd, fcntl.LOCK_UN)
        os.close(lock_fd)


if __name__ == "__main__":
    raise SystemExit(main())
