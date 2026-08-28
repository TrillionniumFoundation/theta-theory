#!/usr/bin/env python3
"""Seal the immutable r39 manifest-before-outer failure as a rejection.

The r39 manifest is intentionally retained as historical evidence.  This
small append-only sealer creates only the missing r39 rejection receipt; it
does not touch r39 bytes, add an outer receipt, or enter runtime/authority.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import stat
import sys

os.environ.update({"PYTHONDONTWRITEBYTECODE": "1", "PYTHONNOUSERSITE": "1"})
sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "deliverables"
BASE = "cm2_round306c79g_true_global_no_producer_consumer"
TAG = "v16r2r39"
UPSTREAM = "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab"
SUCCESSOR = "dd9d64f3f0bd0dfd00fd399e3154517a34ba19cfb601ec749f44cbc08b03ca1b"
MANIFEST = OUT / f"{BASE}_cold_launch_manifest_{TAG}.sha256"
OUTER = OUT / f"{BASE}_cold_launch_outer_receipt_{TAG}.json"
REJECTION = OUT / f"{BASE}_{TAG}_static_bundle_rejection_receipt_v1.json"

PINS = {
    "anchor": ("9c599ef16d7be444e07ba2ae93d4c74dd71781eb859d0cb590098ed1fb03378e", "2a61766cf941e1798c106a150e335f224fa3d351aff3ee5eda31185b991308bd"),
    "schema": ("d547ed583867e817f25d0306057e27b9e781892d6728936da6298b9e40778a61", None),
    "contract": ("5886242005f4eaad6ca373f9656f2e82f76ddbbd0e4ff5f1618c12b676daa542", "5fd9b909a7df5e77f33f9c202d211e9fd83f38792738c0711c06976249098b93"),
    "producer": ("f38b4cefa449102dd1992f1c454f0b55956de405c69253a208d8f55f3dca3961", None),
    "consumer": ("d899eb16506171d67265b8a3f57359a33e7a8dfdc2aea9498d9ace2ae4fedc9c", None),
    "transition": ("3ee3f9c4c8f595925de135d099a6612366b6bba64404ae4e82e582d2667a96b7", "b17553849c4d001457922f50f44af02006ccfab758ffcd1160f97ed735f5df9e"),
    "audit": ("2a1d24187e3e513347f05c163a38b11f3bea2d9de43afeca077a67aa7cae8b31", "8833b9ef25215a1b4b6c9813506fdb7a90ad498a6132a78e1ef186a287a7ed51"),
    "launcher": ("40196dbcc2a40c956f42ab385b610a302952bcca1fb272b7ce640bb3a5b45543", None),
}


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"), allow_nan=False).encode("utf-8")


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def stable(path: Path) -> bytes:
    fd = os.open(path, os.O_RDONLY | os.O_CLOEXEC |
                 getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(fd)
        named = os.lstat(path)
        if not stat.S_ISREG(before.st_mode) or before.st_nlink != 1 or \
           (before.st_dev, before.st_ino, before.st_size) != \
           (named.st_dev, named.st_ino, named.st_size):
            raise RuntimeError(f"unstable:{path}")
        raw = bytearray()
        while True:
            block = os.read(fd, 1 << 20)
            if not block:
                break
            raw.extend(block)
        after = os.fstat(fd)
        if (before.st_dev, before.st_ino, before.st_size) != \
           (after.st_dev, after.st_ino, after.st_size):
            raise RuntimeError(f"drift:{path}")
        return bytes(raw)
    finally:
        os.close(fd)


def close(value: dict) -> dict:
    body = dict(value)
    body.pop("object_sha256", None)
    body["object_sha256"] = digest(canonical(body))
    return body


def install(path: Path, raw: bytes) -> str:
    try:
        fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL |
                     os.O_CLOEXEC, 0o444)
    except FileExistsError:
        if stable(path) != raw or path.stat().st_nlink != 1 or \
           stat.S_IMODE(path.stat().st_mode) != 0o444:
            raise RuntimeError(f"append-only mismatch:{path}")
        return "replayed"
    try:
        view = memoryview(raw)
        pos = 0
        while pos < len(view):
            n = os.write(fd, view[pos:])
            if n <= 0:
                raise RuntimeError("short write")
            pos += n
        os.fsync(fd)
        os.fchmod(fd, 0o444)
    finally:
        os.close(fd)
    dfd = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC)
    try:
        os.fsync(dfd)
    finally:
        os.close(dfd)
    return "installed"


def main() -> int:
    try:
        if not MANIFEST.is_file() or OUTER.exists():
            raise RuntimeError("r39 publication shape is not manifest-only")
        manifest_raw = stable(MANIFEST)
        manifest_sha = digest(manifest_raw)
        if manifest_sha != "f4be58e68811566a554f7505d142646a1dc2be029913833fb42b9bd4589b96eb":
            raise RuntimeError("r39 manifest pin")
        rows = manifest_raw.decode("ascii").splitlines()
        if len(rows) != 8:
            raise RuntimeError("r39 manifest exact8 count")
        for role, (file_pin, object_pin) in PINS.items():
            suffix = {
                "anchor": f"{BASE}_{TAG}_active_predecessor_supersession_receipt_v1.json",
                "schema": f"{BASE}_schema_{TAG}.json",
                "contract": f"{BASE}_contract_{TAG}.json",
                "producer": f"{BASE}_{TAG}_semantic_source.py",
                "consumer": f"{BASE}_independent_verifier_assembler_authority_consumer_{TAG}_semantic_source.py",
                "transition": f"{BASE}_v16r2r38_to_{TAG}_static_launch_transition_receipt_v1.json",
                "audit": f"{BASE}_static_audit_{TAG}.json",
                "launcher": f"{BASE}_cold_launch_{TAG}_semantic_source.py",
            }[role]
            path = OUT / suffix
            raw = stable(path)
            if digest(raw) != file_pin or stat.S_IMODE(path.stat().st_mode) != 0o444 or path.stat().st_nlink != 1:
                raise RuntimeError(f"r39 member pin:{role}")
            if object_pin is not None:
                value = json.loads(raw.decode("utf-8"))
                body = dict(value); claim = body.pop("object_sha256", None)
                if claim != object_pin or digest(canonical(body)) != object_pin:
                    raise RuntimeError(f"r39 object pin:{role}")
        value = close({
            "schema": f"cm2.c79g.{TAG}.static-bundle-rejection.v1",
            "status": "PERMANENT_FAIL_CLOSED_V16R2R39_PUBLICATION_INCOMPLETE__ZERO_CREDIT",
            "failed_namespace": TAG,
            "rejection_reason": "MANIFEST_CREATED_BUT_OUTER_LAST_NOT_CREATED__O_WRONLY_TERMINAL_REPLAY_EBADF",
            "detail": {
                "manifest_path": str(MANIFEST.relative_to(ROOT)),
                "manifest_file_sha256": manifest_sha,
                "outer_path": str(OUTER.relative_to(ROOT)),
                "outer_created": False,
                "exact8_sources_frozen": True,
                "runtime_protocol_executed": False,
                "authority_written": False,
                "error_errno": 9,
                "error": "publisher attempted os.read on O_WRONLY publication fd",
                "required_successor_fix": "fresh publisher opens O_RDWR for same-fd terminal replay",
            },
            "append_only": True,
            "overwrite_delete_or_reuse_allowed": False,
            "runtime_authorized": False,
            "formal_global_closure_credit": 0,
            "D02_unlock": False,
            "manifest_created": True,
            "outer_created": False,
            "runtime_surface_created": False,
            "upstream_checkpoint_object_sha256": UPSTREAM,
            "successor_checkpoint_object_sha256": SUCCESSOR,
        })
        raw = canonical(value) + b"\n"
        action = install(REJECTION, raw)
        print(json.dumps({"schema": f"cm2.c79g.{TAG}.publication-rejection-sealer.v1",
                          "status": "PASS_R39_PUBLICATION_INCOMPLETE_SEALED__ZERO_CREDIT",
                          "action": action, "file_sha256": digest(raw),
                          "object_sha256": value["object_sha256"],
                          "formal_global_closure_credit": 0, "D02_unlock": False,
                          "runtime_authorized": False}, sort_keys=True))
        return 0
    except Exception as exc:
        print(json.dumps({"schema": f"cm2.c79g.{TAG}.publication-rejection-sealer.v1",
                          "status": "FAIL_CLOSED_R39_PUBLICATION_REJECTION_SEAL",
                          "error": f"{type(exc).__name__}: {exc}",
                          "formal_global_closure_credit": 0, "D02_unlock": False}, sort_keys=True))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
