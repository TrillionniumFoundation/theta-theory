#!/usr/bin/env python3
"""Append-only repair publication for the inconsistent r62 freeze.

The r62 publisher sealed a manifest whose first line named the r62 active
predecessor receipt, while the three immutable r62 sources bind the v14
registry-shape-drift supersession receipt as exact8 member one.  This script
does not alter that failed publication.  It creates a separately named,
zero-credit repair manifest/outer pair with the exact8 bytes required by the
immutable r62 sources, plus a receipt recording the mismatch and both pins.
Runtime remains unauthorized; the repair bootstrap is the only consumer of
the new manifest/outer names.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "deliverables"
BASE = "cm2_round306c79g_true_global_no_producer_consumer"
CHECKPOINT = "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab"
LAUNCHER_SHA = "d82461275e83ce720b1c18751b54de5611781db9992eae63e57091a4bf9230f0"

REPAIR_MANIFEST = OUT / (BASE + "_cold_launch_manifest_v16r2r63_repair.sha256")
REPAIR_OUTER = OUT / (BASE + "_cold_launch_outer_receipt_v16r2r63_repair.json")
REPAIR_RECEIPT = OUT / (BASE + "_v16r2r62_to_v16r2r63_publication_repair_receipt_v1.json")

IMMUTABLE_R62_MANIFEST = OUT / (BASE + "_cold_launch_manifest_v16r2r62.sha256")
IMMUTABLE_R62_OUTER = OUT / (BASE + "_cold_launch_outer_receipt_v16r2r62.json")

EXACT8 = (
    (OUT / (BASE + "_v14_runtime_registry_shape_drift_rejection_supersession_receipt_v1.json"),
     "aa4323027e2313f8a2eda0d6ffc039a537afe342d496d1f75cd73fcd47446c01"),
    (OUT / (BASE + "_schema_v16r2r62.json"),
     "1a9c03d332a1c12a34f330b30acb77b13a8f315732fc0bc75be29d3b8c3e1577"),
    (OUT / (BASE + "_contract_v16r2r62.json"),
     "e5093fc90f063542f23c69dde6e0a674b885a5115893b668d755da81156fd4b7"),
    (OUT / (BASE + "_v16r2r62_semantic_source.py"),
     "1c494a66668b7ee7f12a1d5eac25225a68f72d256303aa7114b939e57772659a"),
    (OUT / (BASE + "_independent_verifier_assembler_authority_consumer_v16r2r62_semantic_source.py"),
     "0e68a498f60d659f72247fc6a2a45ee7ee2503765c6b645d1e6ab46d6abc8f20"),
    (OUT / (BASE + "_v16r2r61_to_v16r2r62_static_launch_transition_receipt_v1.json"),
     "23d328057145051a0e42d5b6c4d06350a5e2aab38c06a6a02049225b520b7357"),
    (OUT / (BASE + "_static_audit_v16r2r62.json"),
     "e1cf25ad75c9f7b99e375e03eee92581ac5108b35e51cabe993a77040dbe9601"),
    (OUT / (BASE + "_cold_launch_v16r2r62_semantic_source.py"), LAUNCHER_SHA),
)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False).encode("utf-8")


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def stable_file(path: Path, expected: str) -> bytes:
    fd = os.open(path, os.O_RDONLY | os.O_CLOEXEC |
                 getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(fd)
        named = os.lstat(path)
        if (not os.path.isfile(path) or before.st_nlink != 1 or
                (before.st_dev, before.st_ino, before.st_size) !=
                (named.st_dev, named.st_ino, named.st_size)):
            raise RuntimeError("unstable immutable input:" + str(path))
        raw = bytearray()
        while True:
            block = os.read(fd, 1 << 20)
            if not block:
                break
            raw.extend(block)
        after = os.fstat(fd)
        data = bytes(raw)
        if ((before.st_dev, before.st_ino, before.st_size) !=
                (after.st_dev, after.st_ino, len(data)) or sha(data) != expected):
            raise RuntimeError("immutable input hash/identity drift:" + str(path))
        if os.stat(path).st_mode & 0o777 != 0o444:
            raise RuntimeError("immutable input mode drift:" + str(path))
        return data
    finally:
        os.close(fd)


def exclusive(path: Path, raw: bytes, mode: int = 0o444) -> None:
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL |
                 os.O_CLOEXEC | getattr(os, "O_NOFOLLOW", 0), 0o600)
    try:
        offset = 0
        while offset < len(raw):
            n = os.write(fd, raw[offset:])
            if n <= 0:
                raise RuntimeError("short exclusive write:" + str(path))
            offset += n
        os.fsync(fd)
        os.fchmod(fd, mode)
        os.fsync(fd)
    finally:
        os.close(fd)
    dir_fd = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC)
    try:
        os.fsync(dir_fd)
    finally:
        os.close(dir_fd)
    st = os.stat(path, follow_symlinks=False)
    if st.st_nlink != 1 or (st.st_mode & 0o777) != mode:
        raise RuntimeError("exclusive output identity/mode drift:" + str(path))


def main() -> int:
    for path in (REPAIR_MANIFEST, REPAIR_OUTER, REPAIR_RECEIPT):
        if path.exists() or path.is_symlink():
            raise RuntimeError("repair target already exists; never overwrite:" + str(path))
    entries: list[dict[str, str]] = []
    for path, expected in EXACT8:
        stable_file(path, expected)
        entries.append({"path": str(path.relative_to(ROOT)), "file_sha256": expected})
    manifest_raw = b"".join((entry["file_sha256"] + "  " + entry["path"] + "\n").encode("ascii")
                            for entry in entries)
    manifest_sha = sha(manifest_raw)
    outer_body: dict[str, Any] = {
        "schema": "cm2.round306c79g.true-global-no-producer-consumer.cold-launch-outer-receipt.v16r2",
        "status": "FROZEN_COLD_LAUNCH_OUTER_LAST__EXACT8_MANIFEST_CLOSED__RUNTIME_DEFERRED",
        "effective_checkpoint_object_sha256": CHECKPOINT,
        "exact8_ordered_entries": entries,
        "cold_launch_manifest": {"path": str(REPAIR_MANIFEST.relative_to(ROOT)),
                                 "file_sha256": manifest_sha,
                                 "ordered_entry_count": 8},
        "cold_launcher": {"path": str(EXACT8[-1][0].relative_to(ROOT)),
                          "file_sha256": LAUNCHER_SHA},
        "all_exact8_regular_0444_nlink1_and_held_for_runtime": True,
        "outer_published_after_exact8_manifest": True,
        "runtime_entry_must_be_cold_launcher": True,
        "sole_external_static_file_anchor_is_launcher_sha256": True,
        "declared_external_tcb": ["EXTERNAL_HELD_FD_SEALED_MEMFD_BOOTSTRAP",
                                   "PYTHON3_ISOLATED_INTERPRETER",
                                   "LINUX_KERNEL_OPENAT2_STATX_MEMFD"],
        "formal_global_closure_credit": 0,
        "D02_unlock": False,
        "runtime_executed_during_static_freeze": False,
    }
    outer_object = dict(outer_body)
    outer_object["object_sha256"] = sha(canonical(outer_body))
    outer_raw = canonical(outer_object) + b"\n"
    immutable_manifest_raw = IMMUTABLE_R62_MANIFEST.read_bytes()
    immutable_outer_raw = IMMUTABLE_R62_OUTER.read_bytes()
    repair_body: dict[str, Any] = {
        "schema": "cm2.c79g.v16r2r63.publication-repair.v1",
        "status": "FROZEN_APPEND_ONLY_PUBLICATION_REPAIR__ZERO_CREDIT__R62_RUNTIME_NOT_AUTHORIZED",
        "predecessor_namespace": "v16r2r62",
        "predecessor_manifest_path": str(IMMUTABLE_R62_MANIFEST.relative_to(ROOT)),
        "predecessor_manifest_file_sha256": sha(immutable_manifest_raw),
        "predecessor_outer_path": str(IMMUTABLE_R62_OUTER.relative_to(ROOT)),
        "predecessor_outer_file_sha256": sha(immutable_outer_raw),
        "failure_phase": "PRE_CHILD_HELD_BUNDLE_MANIFEST_RECONSTRUCTION",
        "failure_label": "R62_PUBLISHER_BOUND_ACTIVE_PREDECESSOR_RECEIPT_WHILE_FROZEN_SOURCES_BIND_V14_REGISTRY_RECEIPT",
        "immutable_r62_preserved": True,
        "corrected_exact8_first_member_path": str(EXACT8[0][0].relative_to(ROOT)),
        "corrected_exact8_first_member_file_sha256": EXACT8[0][1],
        "corrected_manifest_path": str(REPAIR_MANIFEST.relative_to(ROOT)),
        "corrected_manifest_file_sha256": manifest_sha,
        "corrected_outer_path": str(REPAIR_OUTER.relative_to(ROOT)),
        "corrected_outer_file_sha256": sha(outer_raw),
        "corrected_outer_object_sha256": outer_object["object_sha256"],
        "formal_global_closure_credit": 0,
        "D02_unlock": False,
        "runtime_authorized": False,
        "overwrite_delete_or_reuse_allowed": False,
    }
    repair = dict(repair_body)
    repair["object_sha256"] = sha(canonical(repair_body))
    # Receipt first records the reason and intended immutable outputs; all
    # three writes are O_EXCL and therefore a partial run can never overwrite.
    exclusive(REPAIR_RECEIPT, canonical(repair) + b"\n")
    exclusive(REPAIR_MANIFEST, manifest_raw)
    exclusive(REPAIR_OUTER, outer_raw)
    print(json.dumps({"status": "PASS_APPEND_ONLY_R63_PUBLICATION_REPAIR",
                      "manifest": str(REPAIR_MANIFEST.relative_to(ROOT)),
                      "manifest_sha256": manifest_sha,
                      "outer": str(REPAIR_OUTER.relative_to(ROOT)),
                      "outer_file_sha256": sha(outer_raw),
                      "outer_object_sha256": outer_object["object_sha256"],
                      "receipt": str(REPAIR_RECEIPT.relative_to(ROOT)),
                      "formal_global_closure_credit": 0, "D02_unlock": False},
                     sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
