#!/usr/bin/env python3
"""Independent read-only audit of the already-frozen C79g v14 surface.

The original v14 static reviewer intentionally rejects a *published* bundle:
its last three gates assert that the manifest, outer receipt, and runtime
namespace are absent before publication.  This companion is for the next
state only.  It reads the frozen exact10 plus the official v14 later-rejection
and supersession receipt, checks byte/object pins, chronology and namespace
absence, and emits a closed report on stdout.  No protocol source is imported
or executed, and this file never writes a workspace file (``-B`` is still
recommended at invocation).
"""

from __future__ import annotations

import ast
import hashlib
import json
import os
from pathlib import Path
import stat
import sys
from typing import Any


sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[1]
CHECKPOINT = "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab"
BASE = "cm2_round306c79g_true_global_no_producer_consumer"

EXACT10: tuple[dict[str, Any], ...] = (
    {
        "name": "v13_prepublication_supersession_receipt",
        "path": f"deliverables/{BASE}_v13_prepublication_pyc_contamination_rejection_supersession_receipt_v1.json",
        "file_sha256": "098296d9807a89f58250f4fd404bdd45b1cf343e3e2e1c7a51a24d67225d016f",
        "object_sha256": "3c9c44500465c6b416cc0ee6689ea82cdd9096a79687b94f94c409ca5a78c677",
    },
    {
        "name": "closed_schema_v14",
        "path": f"deliverables/{BASE}_schema_v14.json",
        "file_sha256": "3d07ccda67cb71d0e5c64d37c0d8e1fcf425de4fbfefddf03bf43934ffdaaa4d",
    },
    {
        "name": "contract_v14",
        "path": f"deliverables/{BASE}_contract_v14.json",
        "file_sha256": "479a0b3f6b4f0ad7e25d22c9f32eec046758a9a7d40509a6bda200e8e41e0ece",
        "object_sha256": "11fd8966ed631f3bcc0eb6b1881f0536c814b7a7c093eca8289680e38a7d7b8b",
    },
    {
        "name": "build_only_producer_v14",
        "path": f"deliverables/{BASE}_v14.py",
        "file_sha256": "9fa2f2e20cdf15ed37d7f3ff904197fa7bc46a4eec243cab0ae8fb477e2e1ff0",
    },
    {
        "name": "independent_consumer_v14",
        "path": f"deliverables/{BASE}_independent_verifier_assembler_authority_consumer_v14.py",
        "file_sha256": "83c58e792b922ad57a7c031b4aca60fe4d5868679e6f7a70b513e3cc4b7dc24c",
    },
    {
        "name": "transition_v13_to_v14",
        "path": f"deliverables/{BASE}_v13_to_v14_static_launch_transition_receipt_v1.json",
        "file_sha256": "e8c810f85b511cbc3637321f872f96c996a854454ab7ae1fbb3f5bdf19d7fd95",
        "object_sha256": "78912a8f23f7a2e229795aae0e609ca58232dbe36c52ad50bddad727f259413f",
    },
    {
        "name": "static_audit_v14",
        "path": f"deliverables/{BASE}_static_audit_v14.json",
        "file_sha256": "dbf5e6bf0f13524ee847d01482f9ad34f715368deb2df40207bd2eb436f293e9",
        "object_sha256": "16a8bc6e274a9e4e5a8fe4b2a39b80136cbbb117bfdf2e0ed89ee90fdc71944a",
    },
    {
        "name": "cold_launcher_v14",
        "path": f"deliverables/{BASE}_cold_launch_v14.py",
        "file_sha256": "1236f53865d69d69d27091758a66b21ddc2ea33ed7f422bc8d56adb69a23f5b5",
    },
    {
        "name": "cold_manifest_v14",
        "path": f"deliverables/{BASE}_cold_launch_manifest_v14.sha256",
        "file_sha256": "aae2b3735ca9d5469d4228189ff0127e85aca934c6e56dfa3650a4d4d46a5937",
    },
    {
        "name": "cold_outer_v14",
        "path": f"deliverables/{BASE}_cold_launch_outer_receipt_v14.json",
        "file_sha256": "fa6d10673d96a36aaf0163c44e014162ffb7811b12b1efa9068d78c8aa5b2040",
        "object_sha256": "786f9be9142ae0aafd31a6d86b08f815d5d4f7ca09fd67506f499635fdddc256",
    },
)

REJECTION = {
    "name": "official_v14_later_rejection",
    "path": f".cm2-runtime/c79g-v14-rejections-{CHECKPOINT}/rejection.json",
    "file_sha256": "1cc1b5836457f219ce26aa8e463ebebe8d48a26d2145806d24f7cbfea6c7e567",
    "object_sha256": "0856353a2390c46b4f4bdefe9f13f6eb6e0e94aa352174cdc8d2f672ace4a41d",
}
SUPERSESSION = {
    "name": "v14_runtime_registry_shape_drift_supersession_receipt",
    "path": f"deliverables/{BASE}_v14_runtime_registry_shape_drift_rejection_supersession_receipt_v1.json",
    "file_sha256": "aa4323027e2313f8a2eda0d6ffc039a537afe342d496d1f75cd73fcd47446c01",
    "object_sha256": "93689e62ae36f405f045a769f4dc6f6e6fd83a16605d08299d5c3397ad657e2e",
}

EXACT56_KEYSET_SHA256 = (
    "9c272f16d92497a7c5ced499e9e42c514b81cbfddcdb3f79c4f33837836e057e")
FORBIDDEN_RUNTIME = tuple(
    f".cm2-runtime/c79g-v14-{suffix}-{CHECKPOINT}"
    for suffix in (
        "candidate-a", "candidate-b", "verification-a", "verification-b",
        "committed-completion")) + (
    f".cm2-runtime/cm2-global-authority-heads/c79g-v14-{CHECKPOINT}.seal",
    f".cm2-runtime/.c79g-v14-candidate-stage-a-{CHECKPOINT}",
    f".cm2-runtime/.c79g-v14-candidate-stage-b-{CHECKPOINT}",
    f".cm2-runtime/.c79g-v14-verification-stage-a-{CHECKPOINT}",
    f".cm2-runtime/.c79g-v14-verification-stage-b-{CHECKPOINT}",
    f".cm2-runtime/.c79g-v14-completion-stage-{CHECKPOINT}",
    f".cm2-runtime/cm2-global-authority-heads/.c79g-v14-authority-stage-{CHECKPOINT}.seal",
)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def strict_json(raw: bytes, label: str) -> dict[str, Any]:
    if not raw.endswith(b"\n") or raw.endswith(b"\n\n"):
        raise ValueError(label + ": terminal newline")

    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in items:
            if key in result:
                raise ValueError(label + ": duplicate JSON key " + key)
            result[key] = value
        return result

    value = json.loads(raw, object_pairs_hook=pairs)
    if not isinstance(value, dict):
        raise ValueError(label + ": top-level object required")
    return value


def verify_object(raw: bytes, label: str, expected: str | None = None,
                  *, require_canonical_file: bool = False) -> dict[str, Any]:
    value = strict_json(raw, label)
    claim = value.get("object_sha256")
    body = dict(value)
    body.pop("object_sha256", None)
    if not isinstance(claim, str) or sha256(canonical(body)) != claim:
        raise ValueError(label + ": object closure")
    if expected is not None and claim != expected:
        raise ValueError(label + ": object pin")
    if require_canonical_file and raw != canonical(value) + b"\n":
        raise ValueError(label + ": canonical bytes")
    return value


def stable(path: Path) -> tuple[bytes, os.stat_result]:
    flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    fd = os.open(path, flags)
    try:
        before = os.fstat(fd)
        named_before = os.stat(path, follow_symlinks=False)
        if (not stat.S_ISREG(before.st_mode) or
                (before.st_dev, before.st_ino, before.st_size) !=
                (named_before.st_dev, named_before.st_ino, named_before.st_size)):
            raise ValueError(str(path) + ": unstable/non-regular")
        chunks: list[bytes] = []
        while True:
            chunk = os.read(fd, 1 << 20)
            if not chunk:
                break
            chunks.append(chunk)
        raw = b"".join(chunks)
        after = os.fstat(fd)
        named_after = os.stat(path, follow_symlinks=False)
        if ((before.st_dev, before.st_ino, before.st_size) !=
                (after.st_dev, after.st_ino, after.st_size) or
                (after.st_dev, after.st_ino, after.st_size) !=
                (named_after.st_dev, named_after.st_ino, named_after.st_size) or
                len(raw) != after.st_size):
            raise ValueError(str(path) + ": changed during held read")
        return raw, before
    finally:
        os.close(fd)


def mode_is_frozen(state: os.stat_result) -> bool:
    return (stat.S_ISREG(state.st_mode) and stat.S_IMODE(state.st_mode) == 0o444
            and state.st_nlink == 1)


def chronology(states: list[os.stat_result]) -> bool:
    # The eight exact members are one frozen group and are not required to be
    # internally ordered.  Publication requires the *whole* group before the
    # manifest, then manifest before outer, outer before the later rejection,
    # and rejection before its supersession receipt.
    if len(states) != 12:
        return False
    exact8, manifest, outer, rejection, receipt = (
        states[:8], states[8], states[9], states[10], states[11])
    exact8_max = max(max(item.st_mtime_ns, item.st_ctime_ns)
                     for item in exact8)
    manifest_min = min(manifest.st_mtime_ns, manifest.st_ctime_ns)
    manifest_max = max(manifest.st_mtime_ns, manifest.st_ctime_ns)
    outer_min = min(outer.st_mtime_ns, outer.st_ctime_ns)
    outer_max = max(outer.st_mtime_ns, outer.st_ctime_ns)
    rejection_min = min(rejection.st_mtime_ns, rejection.st_ctime_ns)
    rejection_max = max(rejection.st_mtime_ns, rejection.st_ctime_ns)
    receipt_min = min(receipt.st_mtime_ns, receipt.st_ctime_ns)
    return (exact8_max < manifest_min and manifest_max < outer_min and
            outer_max < rejection_min and rejection_max < receipt_min)


def check(name: str, passed: bool, details: Any = None) -> dict[str, Any]:
    row: dict[str, Any] = {"name": name, "passed": bool(passed)}
    if details is not None:
        row["details"] = details
    return row


def audit() -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    held: dict[str, tuple[bytes, os.stat_result]] = {}
    errors: list[str] = []

    def hold(pin: dict[str, Any]) -> tuple[bytes, os.stat_result] | None:
        try:
            item = stable(ROOT / pin["path"])
            held[pin["name"]] = item
            return item
        except Exception as exc:
            errors.append(f"{pin['name']}: {type(exc).__name__}: {exc}")
            return None

    # exact10: all bytes and inode properties are checked while descriptors
    # are held, but no descriptor is ever handed to a protocol process.
    exact_rows: list[dict[str, Any]] = []
    for pin in EXACT10:
        item = hold(pin)
        raw, state = item if item is not None else (b"", None)
        object_ok = True
        if item is not None and pin.get("object_sha256") is not None:
            try:
                verify_object(raw, pin["name"], pin["object_sha256"])
            except Exception as exc:
                object_ok = False
                errors.append(f"{pin['name']}: {exc}")
        row = {
            "name": pin["name"], "path": pin["path"],
            "file_sha256": sha256(raw) if item is not None else None,
            "expected_file_sha256": pin["file_sha256"],
            "mode": oct(stat.S_IMODE(state.st_mode)) if state else None,
            "nlink": state.st_nlink if state else None,
            "object_ok": object_ok,
            "matches": item is not None and
            sha256(raw) == pin["file_sha256"] and mode_is_frozen(state) and
            object_ok,
        }
        exact_rows.append(row)
    rows.append(check("v14_exact10_bytes_objects_0444_nlink1", all(
        row["matches"] for row in exact_rows), exact_rows))

    # Manifest and outer are the two post-publication members of exact10.
    manifest_raw = held.get("cold_manifest_v14", (b"", None))[0]
    expected_manifest = b"".join(
        f"{pin['file_sha256']}  {pin['path']}\n".encode("ascii")
        for pin in EXACT10[:8])
    rows.append(check("v14_manifest_exact8_bytes", manifest_raw == expected_manifest,
                      {"expected_sha256": sha256(expected_manifest),
                       "observed_sha256": sha256(manifest_raw)}))
    outer_value: dict[str, Any] = {}
    try:
        outer_raw = held["cold_outer_v14"][0]
        outer_value = verify_object(outer_raw, "cold_outer_v14",
                                    EXACT10[9]["object_sha256"])
    except Exception as exc:
        errors.append(str(exc))
    rows.append(check("v14_outer_object_and_d02_zero_credit", bool(outer_value) and
                      outer_value.get("status") ==
                      "FROZEN_COLD_LAUNCH_OUTER_LAST__EXACT8_MANIFEST_CLOSED__RUNTIME_DEFERRED" and
                      outer_value.get("formal_global_closure_credit") == 0 and
                      outer_value.get("D02_unlock") is False,
                      {"status": outer_value.get("status"),
                       "formal_global_closure_credit": outer_value.get(
                           "formal_global_closure_credit"),
                       "D02_unlock": outer_value.get("D02_unlock")}))

    # The official later rejection is a separate append-only namespace member.
    rejection_item = hold(REJECTION)
    rejection_value: dict[str, Any] = {}
    try:
        if rejection_item is None:
            raise ValueError("missing rejection")
        rejection_value = verify_object(rejection_item[0], REJECTION["name"],
                                        REJECTION["object_sha256"])
    except Exception as exc:
        errors.append(str(exc))
    rejection_keys = set(rejection_value)
    rows.append(check("v14_later_rejection_exact56_zero_credit", bool(rejection_value) and
                      sha256(rejection_item[0]) == REJECTION["file_sha256"] and
                      len(rejection_keys) == 56 and
                      sha256(canonical(sorted(rejection_keys))) ==
                      EXACT56_KEYSET_SHA256 and
                      rejection_value.get("status") ==
                      "PERMANENT_FAIL_CLOSED_REJECTION__ZERO_CREDIT" and
                      rejection_value.get("formal_global_closure_credit") == 0 and
                      rejection_value.get("D02_unlock") is False and
                      rejection_value.get("D02_started") is False,
                      {"key_count": len(rejection_keys),
                       "keyset_sha256": sha256(canonical(sorted(rejection_keys))),
                       "status": rejection_value.get("status")}))

    # The v14->v15 supersession receipt is not part of v14 exact10; it must be
    # append-only, canonical and later than the official v14 rejection.
    receipt_item = hold(SUPERSESSION)
    receipt_value: dict[str, Any] = {}
    try:
        if receipt_item is None:
            raise ValueError("missing v14 supersession receipt")
        receipt_value = verify_object(receipt_item[0], SUPERSESSION["name"],
                                      SUPERSESSION["object_sha256"])
    except Exception as exc:
        errors.append(str(exc))
    receipt_credit = receipt_value.get("credit", {})
    receipt_credit = receipt_credit if isinstance(receipt_credit, dict) else {}
    rows.append(check("v14_supersession_receipt_closed_0444", bool(receipt_value) and
                      sha256(receipt_item[0]) == SUPERSESSION["file_sha256"] and
                      mode_is_frozen(receipt_item[1]) and
                      receipt_value.get("status") ==
                      "FROZEN_APPEND_ONLY_V14_RUNTIME_REGISTRY_SHAPE_DRIFT_REJECTION__ZERO_CREDIT__V15_SUCCESSOR_ONLY" and
                      receipt_credit.get("formal_global_closure_credit") == 0 and
                      receipt_credit.get("D02_unlock") is False and
                      receipt_credit.get("D02_started") is False,
                      {"object_sha256": receipt_value.get("object_sha256"),
                       "status": receipt_value.get("status"),
                       "credit": receipt_credit}))

    # exact8 -> manifest -> outer -> rejection -> supersession chronology.
    chronology_states: list[os.stat_result] = []
    for name in [pin["name"] for pin in EXACT10[:8]] + [
            "cold_manifest_v14", "cold_outer_v14", REJECTION["name"],
            SUPERSESSION["name"]]:
        item = held.get(name)
        if item is None:
            chronology_states = []
            break
        chronology_states.append(item[1])
    rows.append(check("v14_exact8_manifest_outer_rejection_receipt_chronology",
                      len(chronology_states) == 12 and chronology(chronology_states),
                      {"member_count": len(chronology_states)}))

    forbidden_present = [rel for rel in FORBIDDEN_RUNTIME
                         if os.path.lexists(ROOT / rel)]
    rows.append(check("v14_positive_and_stage_namespaces_absent",
                      not forbidden_present, {"present": forbidden_present}))

    pyc = sorted(str(path.relative_to(ROOT)) for path in
                 (ROOT / "deliverables").glob("__pycache__/*v14*.pyc"))
    rows.append(check("v14_target_pyc_absent", not pyc, {"paths": pyc}))

    # In-memory AST parse/compile of the three pinned v14 sources is allowed;
    # no code object is evaluated and no import machinery is used.
    source_rows: list[dict[str, Any]] = []
    for pin in EXACT10[3:5] + (EXACT10[7],):
        item = held.get(pin["name"])
        ok = False
        error = None
        if item is not None:
            try:
                tree = ast.parse(item[0].decode("utf-8"), filename=pin["path"],
                                 mode="exec")
                compile(tree, pin["path"], "exec", dont_inherit=True)
                ok = True
            except Exception as exc:
                error = f"{type(exc).__name__}: {exc}"
                errors.append(f"{pin['name']}: {error}")
        source_rows.append({"name": pin["name"], "matches": ok,
                            "error": error})
    rows.append(check("v14_sources_ast_parse_compile_in_memory", all(
        row["matches"] for row in source_rows), source_rows))

    # Re-read all held paths and reject byte/inode drift during this audit.
    drift: list[str] = []
    for pin in (*EXACT10, REJECTION, SUPERSESSION):
        before = held.get(pin["name"])
        if before is None:
            continue
        try:
            after = stable(ROOT / pin["path"])
            if before[0] != after[0] or (before[1].st_dev, before[1].st_ino,
                                         before[1].st_size, before[1].st_mtime_ns,
                                         before[1].st_ctime_ns) != (
                                             after[1].st_dev, after[1].st_ino,
                                             after[1].st_size, after[1].st_mtime_ns,
                                             after[1].st_ctime_ns):
                drift.append(pin["path"])
        except Exception as exc:
            drift.append(f"{pin['path']}: {exc}")
    rows.append(check("v14_terminal_replay_no_byte_or_inode_drift", not drift,
                      {"drift": drift}))

    passed = all(row["passed"] for row in rows) and not errors
    return {
        "schema": "cm2.c79g.v14.independent-read-only-postfreeze-audit.v1",
        "status": "PASS_POSTFREEZE_READ_ONLY__RUNTIME_NOT_AUTHORIZED" if passed
        else "FAIL_CLOSED_POSTFREEZE_READ_ONLY__RUNTIME_NOT_AUTHORIZED",
        "read_only": True,
        "protocol_python_imported_or_executed": False,
        "protocol_or_runtime_files_written": False,
        "root": str(ROOT),
        "check_count": len(rows),
        "failed_check_count": sum(not row["passed"] for row in rows),
        "failed_checks": [row["name"] for row in rows if not row["passed"]],
        "errors": errors,
        "checks": rows,
    }


def main() -> int:
    try:
        result = audit()
    except Exception as exc:
        result = {
            "schema": "cm2.c79g.v14.independent-read-only-postfreeze-audit.v1",
            "status": "FAIL_CLOSED_POSTFREEZE_READ_ONLY__RUNTIME_NOT_AUTHORIZED",
            "read_only": True,
            "protocol_python_imported_or_executed": False,
            "protocol_or_runtime_files_written": False,
            "fatal_error": f"{type(exc).__name__}: {exc}",
            "failed_check_count": 1,
            "failed_checks": ["audit_completed_without_fatal_error"],
        }
    print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2))
    return 0 if result.get("status", "").startswith("PASS_") else 1


if __name__ == "__main__":
    raise SystemExit(main())
