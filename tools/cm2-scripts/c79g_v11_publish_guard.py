#!/usr/bin/env python3
from __future__ import annotations

import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import sys
from typing import Any


# This module is a one-shot publisher, not a runtime launcher.  Importing it
# performs no I/O.  The first gate in main deliberately remains false until
# the separately closed v11 audit and final launcher raw bytes are supplied.
FINAL_V11_PUBLISH_PINS_INSTALLED = True
_AUDIT_FILE_SHA256_SENTINEL = "a" * 64
_LAUNCHER_FILE_SHA256_SENTINEL = "b" * 64
AUDIT_FILE_SHA256 = (
    "6c94068e3f60a89fb608585ae5e6c7dbe02af17880195132bf7c9033ab797115")
AUDIT_OBJECT_SHA256 = (
    "007fba200b67c7704360bb85819435ed13cc6459c8dbac381b99c3adaaf884c3")
LAUNCHER_FILE_SHA256 = (
    "9f6971d2ca3e2c8f448a6aeed70bc16f38154c626f7744a4e20ba723e3082cc2")

C = "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab"
B = "cm2_round306c79g_true_global_no_producer_consumer"
ROOT_EXPECTED = Path(
    "/home/qian-qi/.openclaw/workspaces/telegram-bot-8449317572")
CONTRACT_REL = f"deliverables/{B}_contract_v11.json"
V4_RECEIPT_REL = f"deliverables/{B}_v4_rejection_supersession_receipt_v1.json"
AUDIT_REL = f"deliverables/{B}_static_audit_v11.json"
LAUNCHER_REL = f"deliverables/{B}_cold_launch_v11.py"
MANIFEST_REL = f"deliverables/{B}_cold_launch_manifest_v11.sha256"
OUTER_REL = f"deliverables/{B}_cold_launch_outer_receipt_v11.json"
V11_REJECTION_NS = f".cm2-runtime/c79g-v11-rejections-{C}"

V10_REJECTION = (
    f".cm2-runtime/c79g-v10-rejections-{C}/rejection.json",
    "1b5bbd9ec04f07e7d7d433685aa693b73bf2315a91e4813960bd5a81e8112828",
    "efdb614e870e70c20202834d3c6ec1a7513a3e98ba5cb4e1b32f87976a529d76",
)
SCHEMA_V11 = (
    f"deliverables/{B}_schema_v11.json",
    "cf1630e3ab1b590876c663b8752d702eae5fe37b7bdbcc7824efbd03bbdbd8e2",
    None,
)
CONTRACT_V11 = (
    CONTRACT_REL,
    "c8851778bc8df7a9804efb5fc226548424b58119a2dff3f75bdea9fcac0ec5cf",
    "b998162a009927f13eb34a88e37f657515e43ae160b3d550de5edb0040486af9",
)
PRODUCER_V11 = (
    f"deliverables/{B}_v11.py",
    "f3b364afc0f5b2f729a3d7786eb8e9c25a9303959d6d2464a40395968090a30b",
    None,
)
CONSUMER_V11 = (
    f"deliverables/{B}_independent_verifier_assembler_authority_consumer_v11.py",
    "d8ad069e3486b9d657e4840e504885bf13129050f68e6cc04e47b71f149370ec",
    None,
)
TRANSITION_V11 = (
    f"deliverables/{B}_v10_to_v11_static_launch_transition_receipt_v1.json",
    "31b33566b898277fb8b272a6f3cd3b51b0b80eac4f58f43979dddfa647a38f4e",
    "9a253960a378521423751735dd272e06dec5c99cfc016d27bf66cfbe7673caaf",
)


def current_exact8() -> tuple[tuple[str, str, str | None], ...]:
    return (
        V10_REJECTION,
        SCHEMA_V11,
        CONTRACT_V11,
        PRODUCER_V11,
        CONSUMER_V11,
        TRANSITION_V11,
        (AUDIT_REL, AUDIT_FILE_SHA256, AUDIT_OBJECT_SHA256),
        (LAUNCHER_REL, LAUNCHER_FILE_SHA256, None),
    )


V11_RUNTIME_SURFACES = (
    f".cm2-runtime/c79g-v11-candidate-a-{C}",
    f".cm2-runtime/c79g-v11-candidate-b-{C}",
    f".cm2-runtime/c79g-v11-verification-a-{C}",
    f".cm2-runtime/c79g-v11-verification-b-{C}",
    f".cm2-runtime/c79g-v11-committed-completion-{C}",
    f".cm2-runtime/cm2-global-authority-heads/c79g-v11-{C}.seal",
    f".cm2-runtime/.c79g-v11-candidate-stage-a-{C}",
    f".cm2-runtime/.c79g-v11-candidate-stage-b-{C}",
    f".cm2-runtime/.c79g-v11-verification-stage-a-{C}",
    f".cm2-runtime/.c79g-v11-verification-stage-b-{C}",
    f".cm2-runtime/.c79g-v11-completion-stage-{C}",
    f".cm2-runtime/cm2-global-authority-heads/.c79g-v11-authority-stage-{C}.seal",
    V11_REJECTION_NS,
)


def strict_pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in items:
        assert key not in out, f"duplicate JSON key: {key}"
        out[key] = value
    return out


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
    value = dict(body)
    value["object_sha256"] = sha256(canonical(body))
    return value


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
            "cold-launch-outer-receipt.v11"),
        "status": (
            "FROZEN_COLD_LAUNCH_OUTER_LAST__EXACT8_MANIFEST_CLOSED__"
            "RUNTIME_DEFERRED"),
        "effective_checkpoint_object_sha256": C,
        "exact8_ordered_entries": entries,
        "cold_launch_manifest": {
            "path": MANIFEST_REL,
            "file_sha256": manifest_sha,
            "ordered_entry_count": 8,
        },
        "cold_launcher": {
            "path": LAUNCHER_REL,
            "file_sha256": LAUNCHER_FILE_SHA256,
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


def fd_mount_id(fd: int) -> int:
    raw = Path(f"/proc/self/fdinfo/{fd}").read_text(encoding="ascii")
    rows = [line for line in raw.splitlines() if line.startswith("mnt_id:\t")]
    assert len(rows) == 1
    value = int(rows[0].split("\t", 1)[1])
    assert value > 0
    return value


class Held:
    def __init__(self, root: Path, rel: str, file_sha: str,
                 object_sha: str | None, allowed_modes: set[int]):
        self._install_names(root, rel, file_sha, object_sha)
        before = os.lstat(self.path)
        assert stat.S_ISREG(before.st_mode) and not stat.S_ISLNK(before.st_mode)
        assert before.st_nlink == 1
        self.fd = os.open(
            self.path,
            os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC |
            getattr(os, "O_NOATIME", 0))
        try:
            self.before = os.fstat(self.fd)
            assert self.fingerprint(before) == self.fingerprint(self.before)
            assert stat.S_IMODE(self.before.st_mode) in allowed_modes
            self.mount_id = fd_mount_id(self.fd)
            raw = self.read()
            assert sha256(raw) == file_sha, (rel, sha256(raw), file_sha)
            if object_sha is not None:
                verify_object(raw, object_sha)
        except BaseException:
            os.close(self.fd)
            raise

    def _install_names(self, root: Path, rel: str, file_sha: str,
                       object_sha: str | None) -> None:
        assert rel and not rel.startswith("/") and ".." not in Path(rel).parts
        assert re.fullmatch(r"[0-9a-f]{64}", file_sha)
        if object_sha is not None:
            assert re.fullmatch(r"[0-9a-f]{64}", object_sha)
        self.root = root
        self.rel = rel
        self.path = root / rel
        self.file_sha = file_sha
        self.object_sha = object_sha

    @classmethod
    def create_exclusive(cls, root: Path, rel: str, raw: bytes,
                         object_sha: str | None) -> Held:
        self = cls.__new__(cls)
        self._install_names(root, rel, sha256(raw), object_sha)
        relative = Path(rel)
        assert len(relative.parts) == 2 and relative.parts[0] == "deliverables"
        parent = root / relative.parent
        parent_fd = os.open(
            parent, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC)
        try:
            self.fd = os.open(
                relative.name,
                os.O_RDWR | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW |
                os.O_CLOEXEC,
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
            path_st = os.lstat(self.path)
            assert self.fingerprint(path_st) == self.fingerprint(self.before)
            assert stat.S_IMODE(self.before.st_mode) == 0o444
            assert self.before.st_nlink == 1 and self.before.st_size == len(raw)
            assert self.read() == raw and sha256(raw) == self.file_sha
            if object_sha is not None:
                verify_object(raw, object_sha)
            return self
        except BaseException:
            os.close(self.fd)
            raise

    @staticmethod
    def fingerprint(st: os.stat_result) -> tuple[int, int, int, int, int, int]:
        return (st.st_dev, st.st_ino, st.st_size, st.st_nlink,
                st.st_mtime_ns, st.st_ctime_ns)

    def read(self) -> bytes:
        os.lseek(self.fd, 0, os.SEEK_SET)
        chunks: list[bytes] = []
        while True:
            block = os.read(self.fd, 1024 * 1024)
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
        path_st = os.lstat(self.path)
        fd_st = os.fstat(self.fd)
        assert stat.S_ISREG(path_st.st_mode) and not stat.S_ISLNK(path_st.st_mode)
        assert (path_st.st_dev, path_st.st_ino) == (fd_st.st_dev, fd_st.st_ino)
        assert stat.S_IMODE(fd_st.st_mode) == 0o444 and fd_st.st_nlink == 1
        assert fd_st.st_mtime_ns <= fd_st.st_ctime_ns
        assert fd_mount_id(self.fd) == self.mount_id
        raw = self.read()
        assert sha256(raw) == self.file_sha
        if self.object_sha is not None:
            verify_object(raw, self.object_sha)
        return fd_st, raw

    def close(self) -> None:
        try:
            os.close(self.fd)
        except OSError:
            pass


def add_expected(expected: dict[str, tuple[str, str | None]],
                 item: dict[str, Any]) -> None:
    assert set(item) >= {"path", "file_sha256"}
    rel = item["path"]
    file_sha = item["file_sha256"]
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


def fsync_dir(path: Path) -> None:
    fd = os.open(
        path, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def assert_v11_runtime_absent(root: Path) -> None:
    for rel in V11_RUNTIME_SURFACES:
        assert not os.path.lexists(root / rel), rel
    runtime = root / ".cm2-runtime"
    for directory, names, files in os.walk(runtime, followlinks=False):
        for name in [*names, *files]:
            assert "c79g-v11" not in name, str(Path(directory) / name)


def assert_v11_unpublished(root: Path) -> None:
    assert not os.path.lexists(root / MANIFEST_REL)
    assert not os.path.lexists(root / OUTER_REL)
    assert_v11_runtime_absent(root)


def exact_rejection_namespace(root: Path, version: str,
                              held: dict[str, Held]) -> None:
    rel = f".cm2-runtime/c79g-{version}-rejections-{C}"
    path = root / rel
    path_st = os.lstat(path)
    assert stat.S_ISDIR(path_st.st_mode) and not stat.S_ISLNK(path_st.st_mode)
    nsfd = os.open(
        path,
        os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC |
        getattr(os, "O_NOATIME", 0))
    try:
        st = os.fstat(nsfd)
        mount_id = fd_mount_id(nsfd)
        assert (path_st.st_dev, path_st.st_ino) == (st.st_dev, st.st_ino)
        assert stat.S_IMODE(st.st_mode) == 0o555 and st.st_nlink == 2
        assert os.listdir(nsfd) == ["rejection.json"]
    finally:
        os.close(nsfd)
    member = held[f"{rel}/rejection.json"]
    member_path = os.lstat(member.path)
    member_fd = os.fstat(member.fd)
    assert (member_path.st_dev, member_path.st_ino) == (
        member_fd.st_dev, member_fd.st_ino)
    assert member_fd.st_dev == st.st_dev and member.mount_id == mount_id
    assert stat.S_IMODE(member_fd.st_mode) == 0o444 and member_fd.st_nlink == 1


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
    add_expected(
        expected,
        contract["rejected_unpublished_predecessor_v4"]["supersession_receipt"])

    for version in ("v5", "v6", "v7", "v8", "v9", "v10"):
        segment = contract[
            f"published_then_officially_rejected_predecessor_{version}"]
        for item in ordered_exact10(segment, "ordered_published_exact10"):
            add_expected(expected, item)
        add_expected(expected, segment["official_later_rejection"])

    for rel, file_sha, object_sha in exact8:
        item: dict[str, Any] = {"path": rel, "file_sha256": file_sha}
        if object_sha is not None:
            item["object_sha256"] = object_sha
        add_expected(expected, item)
    assert len(expected) == 86, len(expected)
    return expected


def verify_contract_paths(
        contract: dict[str, Any],
        exact8: tuple[tuple[str, str, str | None], ...]) -> None:
    paths = [rel for rel, _, _ in exact8]
    assert contract["effective_checkpoint_object_sha256"] == C
    assert contract["status"] == (
        "STATIC_CONTRACT_BYTES_FINAL__COLD_FREEZE_PENDING__"
        "RUNTIME_NOT_AUTHORIZED")
    bundle = contract["v11_bundle"]
    assert bundle["base7_ordered_paths"] == paths[:7]
    assert bundle["exact8_ordered_paths"] == paths
    assert bundle["exact10_ordered_paths"] == paths + [MANIFEST_REL, OUTER_REL]
    closure = bundle["cold_launch_outer_closure"]
    assert closure[
        "current_v11_exact10_plus_all_append_only_predecessors_"
        "unique_file_identity_count"] == 88
    publication = contract["exact_publication_paths"]
    assert publication["v11_rejection_namespace"] == V11_REJECTION_NS
    assert publication["cold_launch_exact8_manifest"] == MANIFEST_REL
    assert publication["cold_launch_outer_last"] == OUTER_REL
    assert publication["cold_launcher"] == LAUNCHER_REL
    assert paths[0] == V10_REJECTION[0]
    contract_runtime = {
        publication["candidate_A"], publication["candidate_B"],
        publication["verification_A"], publication["verification_B"],
        publication["committed_completion"], publication["authority_seal"],
        publication["completion_staging_path"],
        publication["authority_staging_path"], V11_REJECTION_NS,
        publication["candidate_staging_path_template"].replace("{a|b}", "a"),
        publication["candidate_staging_path_template"].replace("{a|b}", "b"),
        publication["verification_staging_path_template"].replace("{a|b}", "a"),
        publication["verification_staging_path_template"].replace("{a|b}", "b"),
    }
    assert contract_runtime == set(V11_RUNTIME_SURFACES)


def main() -> int:
    if not __debug__:
        raise RuntimeError("python -O is forbidden for the publication guard")
    assert FINAL_V11_PUBLISH_PINS_INSTALLED is True
    assert AUDIT_FILE_SHA256 != _AUDIT_FILE_SHA256_SENTINEL
    assert LAUNCHER_FILE_SHA256 != _LAUNCHER_FILE_SHA256_SENTINEL
    assert re.fullmatch(r"[0-9a-f]{64}", AUDIT_FILE_SHA256)
    assert re.fullmatch(r"[0-9a-f]{64}", AUDIT_OBJECT_SHA256)
    assert re.fullmatch(r"[0-9a-f]{64}", LAUNCHER_FILE_SHA256)
    assert AUDIT_FILE_SHA256 != LAUNCHER_FILE_SHA256
    assert len(sys.argv) in {2, 3}
    preflight = len(sys.argv) == 3
    if preflight:
        assert sys.argv[2] == "PREFLIGHT"
    root = Path(sys.argv[1]).resolve(strict=True)
    assert root == ROOT_EXPECTED
    runtime = root / ".cm2-runtime"
    runtime_st = os.lstat(runtime)
    assert stat.S_ISDIR(runtime_st.st_mode) and not stat.S_ISLNK(runtime_st.st_mode)
    lockfd = os.open(
        runtime,
        os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC |
        getattr(os, "O_NOATIME", 0))
    fcntl.flock(lockfd, fcntl.LOCK_EX)
    held: dict[str, Held] = {}
    opened: list[Held] = []
    try:
        assert_v11_unpublished(root)
        exact8 = current_exact8()
        assert [item[0] for item in exact8] == [
            V10_REJECTION[0], SCHEMA_V11[0], CONTRACT_V11[0], PRODUCER_V11[0],
            CONSUMER_V11[0], TRANSITION_V11[0], AUDIT_REL, LAUNCHER_REL]
        manifest_raw, manifest_sha, outer_raw, outer_sha, outer_object = (
            expected_publication(exact8))

        contract_seed = Held(
            root, CONTRACT_V11[0], CONTRACT_V11[1], CONTRACT_V11[2],
            {0o444, 0o644, 0o664})
        opened.append(contract_seed)
        contract = verify_object(contract_seed.read(), CONTRACT_V11[2])
        verify_contract_paths(contract, exact8)
        v4_ref = contract[
            "rejected_unpublished_predecessor_v4"]["supersession_receipt"]
        assert v4_ref["path"] == V4_RECEIPT_REL
        v4_seed = Held(
            root, V4_RECEIPT_REL, v4_ref["file_sha256"],
            v4_ref["object_sha256"], {0o444})
        opened.append(v4_seed)
        v4_receipt = verify_object(v4_seed.read(), v4_ref["object_sha256"])
        expected = build_expected(contract, v4_receipt, exact8)

        preopened = {CONTRACT_V11[0]: contract_seed, V4_RECEIPT_REL: v4_seed}
        current_paths = {rel for rel, _, _ in exact8}
        historical_paths = set(expected) - (current_paths - {V10_REJECTION[0]})
        for rel, (file_sha, object_sha) in expected.items():
            item = preopened.pop(rel, None)
            if item is None:
                modes = ({0o444, 0o644, 0o664}
                         if rel in current_paths and rel not in historical_paths
                         else {0o444})
                item = Held(root, rel, file_sha, object_sha, modes)
                opened.append(item)
            held[rel] = item
        assert not preopened and len(held) == 86
        identities = {(item.before.st_dev, item.before.st_ino)
                      for item in held.values()}
        assert len(identities) == 86
        assert len({item.before.st_dev for item in held.values()}) == 1
        assert len({item.mount_id for item in held.values()}) == 1
        audit = verify_object(held[AUDIT_REL].read(), AUDIT_OBJECT_SHA256)
        assert audit["object_sha256"] == AUDIT_OBJECT_SHA256
        for version in ("v3", "v5", "v6", "v7", "v8", "v9", "v10"):
            exact_rejection_namespace(root, version, held)
        assert_v11_unpublished(root)

        if preflight:
            print(canonical({
                "status": "PREFLIGHT_86_FILE_READ_ONLY_PASS_UNDER_OFFICIAL_LOCK_V11",
                "held_unique_files": 86,
                "same_st_dev_and_mount_id": True,
                "no_chmod_or_publication_write_performed": True,
                "manifest_absent": True,
                "outer_absent": True,
                "all_v11_runtime_and_rejection_surfaces_absent": True,
                "mechanical_manifest_sha256": manifest_sha,
                "mechanical_outer_file_sha256": outer_sha,
                "mechanical_outer_object_sha256": outer_object,
            }).decode("ascii"), flush=True)
            return 0

        base_stats = [held[rel].freeze() for rel, _, _ in exact8]
        fsync_dir(root / "deliverables")
        fsync_dir(runtime)
        fsync_dir(root)
        assert_v11_unpublished(root)
        base_max = max(max(st.st_mtime_ns, st.st_ctime_ns) for st in base_stats)

        manifest = Held.create_exclusive(
            root, MANIFEST_REL, manifest_raw, None)
        opened.append(manifest)
        held[MANIFEST_REL] = manifest
        fsync_dir(root / "deliverables")
        fsync_dir(root)
        manifest_st = os.fstat(manifest.fd)
        assert base_max < min(manifest_st.st_mtime_ns, manifest_st.st_ctime_ns)
        assert not os.path.lexists(root / OUTER_REL)
        assert_v11_runtime_absent(root)

        outer = Held.create_exclusive(
            root, OUTER_REL, outer_raw, outer_object)
        opened.append(outer)
        held[OUTER_REL] = outer
        fsync_dir(root / "deliverables")
        fsync_dir(runtime)
        fsync_dir(root)
        outer_st = os.fstat(outer.fd)
        assert max(manifest_st.st_mtime_ns, manifest_st.st_ctime_ns) < min(
            outer_st.st_mtime_ns, outer_st.st_ctime_ns)
        assert_v11_runtime_absent(root)

        assert len(held) == 88
        replay = {rel: item.replay() for rel, item in held.items()}
        replay_identities = {(st.st_dev, st.st_ino) for st, _ in replay.values()}
        assert len(replay_identities) == 88
        assert len({st.st_dev for st, _ in replay.values()}) == 1
        assert len({held[rel].mount_id for rel in replay}) == 1
        predecessor_v3 = contract["append_only_predecessor_v3"]
        history = [ordered_exact10(predecessor_v3, "ordered_exact10")]
        for version in ("v5", "v6", "v7", "v8", "v9", "v10"):
            history.append(ordered_exact10(
                contract[f"published_then_officially_rejected_predecessor_{version}"],
                "ordered_published_exact10"))
        for ordered in history:
            expected_manifest = b"".join(
                (entry["file_sha256"] + "  " + entry["path"] + "\n").encode(
                    "ascii")
                for entry in ordered[:8])
            assert replay[ordered[8]["path"]][1] == expected_manifest
        for version in ("v3", "v5", "v6", "v7", "v8", "v9", "v10"):
            exact_rejection_namespace(root, version, held)
        assert replay[MANIFEST_REL][1] == manifest_raw
        assert replay[OUTER_REL][1] == outer_raw
        base_stats = [replay[rel][0] for rel, _, _ in exact8]
        manifest_st = replay[MANIFEST_REL][0]
        outer_st = replay[OUTER_REL][0]
        base_max = max(max(st.st_mtime_ns, st.st_ctime_ns) for st in base_stats)
        assert base_max < min(manifest_st.st_mtime_ns, manifest_st.st_ctime_ns)
        assert max(manifest_st.st_mtime_ns, manifest_st.st_ctime_ns) < min(
            outer_st.st_mtime_ns, outer_st.st_ctime_ns)
        assert_v11_runtime_absent(root)
        fsync_dir(root / "deliverables")
        fsync_dir(runtime)
        fsync_dir(root)
        print(canonical({
            "status": "TERMINAL_88_FILE_REPLAY_PASS_UNDER_SAME_OFFICIAL_LOCK_V11",
            "unique_files": 88,
            "same_st_dev_and_mount_id": True,
            "base_max_ns": base_max,
            "manifest_mtime_ns": manifest_st.st_mtime_ns,
            "manifest_ctime_ns": manifest_st.st_ctime_ns,
            "outer_mtime_ns": outer_st.st_mtime_ns,
            "outer_ctime_ns": outer_st.st_ctime_ns,
            "manifest_sha256": manifest_sha,
            "outer_file_sha256": outer_sha,
            "outer_object_sha256": outer_object,
            "all_v11_runtime_and_rejection_surfaces_absent": True,
        }).decode("ascii"), flush=True)
        return 0
    finally:
        seen: set[int] = set()
        for item in opened:
            identity = id(item)
            if identity not in seen:
                seen.add(identity)
                item.close()
        fcntl.flock(lockfd, fcntl.LOCK_UN)
        os.close(lockfd)


if __name__ == "__main__":
    raise SystemExit(main())
