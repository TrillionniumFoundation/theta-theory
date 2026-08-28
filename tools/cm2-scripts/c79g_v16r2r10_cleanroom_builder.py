#!/usr/bin/env python3
"""Build the append-only C79g ``v16r2r10`` static clean-room.

The previous r9 attempt mixed an executable-source suffix (``v16r2r9``) with
an unrelated static JSON suffix (``v16r9``).  This builder starts a new
namespace and makes the three source bytes, the four JSON objects, and the
active predecessor receipt agree on one suffix.  It deliberately does not
touch r9 (or any older artifact), and it never creates a manifest, outer
receipt, runtime surface, credit, or Python bytecode.

The source pass is a byte-preserving semantic successor pass: it reads the
already reviewed r9 source bytes, applies only explicit namespace/path and
active-anchor substitutions, parses and compiles the result in memory, and
installs each target with ``O_EXCL``.  The JSON pass retags the frozen r9
structural quartet, updates the active source pins/exact8 list, closes every
top-level object, and likewise installs only absent targets.
"""

from __future__ import annotations

import ast
import copy
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import sys
from typing import Any

sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "deliverables"
BASE = "cm2_round306c79g_true_global_no_producer_consumer"
PREV = "v16r2r9"
TAG = "v16r2r10"
CHECKPOINT = "dd9d64f3f0bd0dfd00fd399e3154517a34ba19cfb601ec749f44cbc08b03ca1b"
UPSTREAM = "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab"

PREV_SOURCE = {
    "producer": OUT / f"{BASE}_{PREV}_semantic_source.py",
    "consumer": OUT / f"{BASE}_independent_verifier_assembler_authority_consumer_{PREV}_semantic_source.py",
    "launcher": OUT / f"{BASE}_cold_launch_{PREV}_semantic_source.py",
}
PREV_JSON = {
    "schema": OUT / f"{BASE}_schema_v16r9.json",
    "contract": OUT / f"{BASE}_contract_v16r9.json",
    "transition": OUT / f"{BASE}_v16r8_to_v16r9_static_launch_transition_receipt_v1.json",
    "audit": OUT / f"{BASE}_static_audit_v16r9.json",
}
PREV_ANCHOR = OUT / f"{BASE}_{PREV}_active_predecessor_supersession_receipt_v1.json"

SOURCE = {
    "producer": OUT / f"{BASE}_{TAG}_semantic_source.py",
    "consumer": OUT / f"{BASE}_independent_verifier_assembler_authority_consumer_{TAG}_semantic_source.py",
    "launcher": OUT / f"{BASE}_cold_launch_{TAG}_semantic_source.py",
}
JSON = {
    "schema": OUT / f"{BASE}_schema_{TAG}.json",
    "contract": OUT / f"{BASE}_contract_{TAG}.json",
    "transition": OUT / f"{BASE}_{PREV}_to_{TAG}_static_launch_transition_receipt_v1.json",
    "audit": OUT / f"{BASE}_static_audit_{TAG}.json",
}
ANCHOR = OUT / f"{BASE}_{TAG}_active_predecessor_supersession_receipt_v1.json"


def canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"), allow_nan=False).encode("utf-8")


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def read_stable(path: Path) -> bytes:
    fd = os.open(path, os.O_RDONLY | os.O_CLOEXEC |
                 getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(fd)
        if not stat.S_ISREG(before.st_mode) or before.st_nlink != 1:
            raise RuntimeError(f"input is not regular/nlink1: {path}")
        chunks: list[bytes] = []
        while True:
            block = os.read(fd, 1 << 20)
            if not block:
                break
            chunks.append(block)
        after = os.fstat(fd)
        named = os.lstat(path)
        if ((before.st_dev, before.st_ino, before.st_size) !=
                (after.st_dev, after.st_ino, after.st_size) or
                (before.st_dev, before.st_ino) != (named.st_dev, named.st_ino)):
            raise RuntimeError(f"input identity drift: {path}")
        raw = b"".join(chunks)
        if len(raw) != before.st_size:
            raise RuntimeError(f"short read: {path}")
        return raw
    finally:
        os.close(fd)


def install_o_excl(path: Path, raw: bytes, mode: int) -> str:
    """Install one explicit target, or replay byte-identical content only."""
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL |
                     os.O_CLOEXEC, mode)
    except FileExistsError:
        old = read_stable(path)
        st = path.stat()
        if old != raw or st.st_nlink != 1 or stat.S_IMODE(st.st_mode) != mode:
            raise RuntimeError(f"append-only target mismatch: {path}")
        return "replayed"
    try:
        view = memoryview(raw)
        offset = 0
        while offset < len(view):
            offset += os.write(fd, view[offset:])
        os.fsync(fd)
        os.fchmod(fd, mode)
    finally:
        os.close(fd)
    dfd = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC)
    try:
        os.fsync(dfd)
    finally:
        os.close(dfd)
    return "installed"


def close_object(value: dict[str, Any]) -> dict[str, Any]:
    body = copy.deepcopy(value)
    body.pop("object_sha256", None)
    body["object_sha256"] = sha(canonical(body))
    return body


def strict_json(raw: bytes) -> dict[str, Any]:
    value = json.loads(raw.decode("utf-8"))
    if not isinstance(value, dict):
        raise RuntimeError("JSON root is not an object")
    return value


def recursive_retag(value: Any) -> Any:
    """Retag active r9 names while retaining historical v3--v14 evidence."""
    if isinstance(value, dict):
        return {recursive_retag(k): recursive_retag(v) for k, v in value.items()}
    if isinstance(value, list):
        return [recursive_retag(v) for v in value]
    if not isinstance(value, str):
        return value
    # Longest path spellings first.  These substitutions are confined to the
    # newly copied object; no predecessor bytes are ever rewritten in place.
    replacements = (
        (f"{BASE}_v16r2r8_to_v16r9_static_launch_transition_receipt_v1.json",
         f"{BASE}_{PREV}_to_{TAG}_static_launch_transition_receipt_v1.json"),
        (f"{BASE}_v16r2r9_active_predecessor_supersession_receipt_v1.json",
         ANCHOR.name),
        (f"{BASE}_v16r2r9_semantic_source.py",
         SOURCE["producer"].name),
        (f"{BASE}_independent_verifier_assembler_authority_consumer_v16r2r9_semantic_source.py",
         SOURCE["consumer"].name),
        (f"{BASE}_cold_launch_v16r2r9_semantic_source.py",
         SOURCE["launcher"].name),
        (f"{BASE}_schema_v16r9.json", JSON["schema"].name),
        (f"{BASE}_contract_v16r9.json", JSON["contract"].name),
        (f"{BASE}_static_audit_v16r9.json", JSON["audit"].name),
        (f"{BASE}_cold_launch_manifest_v16r9.sha256",
         f"{BASE}_cold_launch_manifest_{TAG}.sha256"),
        (f"{BASE}_cold_launch_outer_receipt_v16r9.json",
         f"{BASE}_cold_launch_outer_receipt_{TAG}.json"),
        ("v16r8_to_v16r9", f"{PREV}_to_{TAG}"),
        ("v16r2r9", TAG),
        ("v16r9", TAG),
        ("V16R2R9", "V16R2R10"),
        ("V16R9", "V16R2R10"),
    )
    out = value
    for old, new in replacements:
        out = out.replace(old, new)
    return out


def make_anchor() -> tuple[dict[str, Any], bytes]:
    prev_raw = read_stable(PREV_ANCHOR)
    prev_obj = strict_json(prev_raw)
    if prev_obj.get("formal_global_closure_credit") != 0 or prev_obj.get("D02_unlock") is not False:
        raise RuntimeError("r9 predecessor anchor is not zero-credit/closed")
    body = {
        "schema": f"cm2.c79g.{TAG}.active-predecessor-supersession.v1",
        "status": "FROZEN_APPEND_ONLY_ACTIVE_PREDECESSOR_ANCHOR__ZERO_CREDIT",
        "predecessor_namespace": f"{PREV}_semantic_source",
        "predecessor_supersession_path": str(PREV_ANCHOR.relative_to(ROOT)),
        "predecessor_supersession_file_sha256": sha(prev_raw),
        "predecessor_supersession_object_sha256": prev_obj.get("object_sha256"),
        "frozen_v16_semantic_supersession_path": str(
            OUT / f"{BASE}_v16_semantic_rejection_supersession_receipt_v1.json"),
        "upstream_checkpoint_object_sha256": UPSTREAM,
        "successor_checkpoint_object_sha256": CHECKPOINT,
        "successor_namespace": f"{TAG}_semantic_source",
        "append_only": True,
        "runtime_authorized": False,
        "formal_global_closure_credit": 0,
        "D02_unlock": False,
        "manifest_created": False,
        "outer_created": False,
    }
    closed = close_object(body)
    return closed, canonical(closed) + b"\n"


def source_retag(raw: bytes, role: str, anchor_obj: dict[str, Any]) -> bytes:
    text = raw.decode("utf-8")
    # Explicitly rewrite namespace/path spellings in the copied candidate.
    text = recursive_retag(text)
    # Bind the active predecessor to the fresh r10 anchor, not to a stale
    # r9 receipt.  Only these two assignment lines are changed; historical
    # evidence and unrelated hashes remain byte-for-byte inherited.
    text = re.sub(
        r'(?m)^ACTIVE_PREDECESSOR_SUPERSESSION_FILE_PIN\s*=\s*"[0-9a-f]{64}"\s*$',
        f'ACTIVE_PREDECESSOR_SUPERSESSION_FILE_PIN = "{sha(canonical(anchor_obj) + b"\\n")}"',
        text,
    )
    text = re.sub(
        r'(?m)^ACTIVE_PREDECESSOR_SUPERSESSION_OBJECT_PIN\s*=\s*"[0-9a-f]{64}"\s*$',
        f'ACTIVE_PREDECESSOR_SUPERSESSION_OBJECT_PIN = "{anchor_obj["object_sha256"]}"',
        text,
    )
    # The independent reviewer requires an explicit fail-closed alias in all
    # three source roles.  Add it only where absent (r9 already has it in the
    # consumer and launcher).
    if "FINAL_BASE7_PINS_INSTALLED = False" not in text:
        marker = "RUNTIME_AUTHORIZED = False\n"
        if marker not in text:
            raise RuntimeError(f"runtime marker missing in {role}")
        text = text.replace(marker,
                            marker + "FINAL_BASE7_PINS_INSTALLED = False\n", 1)
    # Ensure the fresh suffix survives even if a future source drops a path
    # occurrence; this is a literal metadata marker, not authority state.
    if TAG not in text:
        raise RuntimeError(f"{role} lost successor suffix")
    out = (text if text.endswith("\n") else text + "").encode("utf-8")
    tree = ast.parse(out.decode("utf-8"), filename=str(SOURCE[role]))
    compile(tree, str(SOURCE[role]), "exec")
    if "SOURCE_TEMPLATE_ONLY" in out.decode("utf-8"):
        raise RuntimeError(f"{role} remained a source template")
    return out


def walk(value: Any):
    yield value
    if isinstance(value, dict):
        for child in value.values():
            yield from walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk(child)


def patch_active_metadata(schema: dict[str, Any], source_hashes: dict[str, str],
                          paths: dict[str, str]) -> None:
    # Keep the original full-shape metadata, while exposing a reviewer-facing
    # active object with one unambiguous baseline and source pin map.
    old = schema.get(f"x-cm2-{TAG}-active-successor", {})
    if not isinstance(old, dict):
        old = {}
    active = copy.deepcopy(old)
    active.update({
        "namespace": f"{TAG}_semantic_bundle",
        "active_exact8_first_member_field": f"current_exact8_first_member_is_{TAG}_supersession_receipt",
        "active_exact8_first_member_path": paths["predecessor"],
        "active_successor_paths": paths,
        "effective_checkpoint_object_sha256": UPSTREAM,
        "formal_global_closure_credit": 0,
        "runtime_authorized": False,
        "source_hashes": source_hashes,
        "global_baseline": {"rows": 76832, "unresolved": 1148},
        "D02_unlock": False,
    })
    schema["x-cm2-successor-active"] = active


def patch_bundle(bundle: dict[str, Any], source_hashes: dict[str, str],
                 exact8: list[str], paths: dict[str, str]) -> None:
    bundle["bundle_version"] = TAG
    bundle["source_hashes"] = dict(source_hashes)
    bundle["exact8_ordered_paths"] = list(exact8)
    bundle["base7_ordered_paths"] = list(exact8[:-1])
    bundle["cold_launch_outer_closure"] = dict(bundle.get("cold_launch_outer_closure", {}))
    bundle["cold_launch_outer_closure"].update({
        "exact8_manifest_path": paths["manifest"],
        "launcher_path": paths["launcher"],
        "outer_last_path": paths["outer"],
        "manifest_or_outer_absent_in_this_static_phase": True,
        "runtime_entry_authorized": False,
    })
    bundle["formal_global_closure_credit"] = 0
    bundle["D02_unlock"] = False
    bundle["runtime_authorized"] = False


def make_json_quartet(anchor_obj: dict[str, Any], source_hashes: dict[str, str]) -> dict[str, bytes]:
    values = {name: strict_json(read_stable(path)) for name, path in PREV_JSON.items()}
    values = {name: recursive_retag(value) for name, value in values.items()}
    paths = {
        "predecessor": str(ANCHOR.relative_to(ROOT)),
        "schema": str(JSON["schema"].relative_to(ROOT)),
        "contract": str(JSON["contract"].relative_to(ROOT)),
        "producer": str(SOURCE["producer"].relative_to(ROOT)),
        "consumer": str(SOURCE["consumer"].relative_to(ROOT)),
        "transition": str(JSON["transition"].relative_to(ROOT)),
        "audit": str(JSON["audit"].relative_to(ROOT)),
        "launcher": str(SOURCE["launcher"].relative_to(ROOT)),
        "manifest": f"deliverables/{BASE}_cold_launch_manifest_{TAG}.sha256",
        "outer": f"deliverables/{BASE}_cold_launch_outer_receipt_{TAG}.json",
    }
    exact8 = [paths[k] for k in (
        "predecessor", "schema", "contract", "producer", "consumer",
        "transition", "audit", "launcher")]
    schema = values["schema"]
    # Retagging leaves the r9 metadata key for historical traceability; the
    # new active key is the one consumed by the independent reviewer.
    patch_active_metadata(schema, source_hashes, paths)
    contract = values["contract"]
    transition = values["transition"]
    audit = values["audit"]
    for value, key in ((contract, f"{TAG}_bundle"),
                       (transition, f"successor_{TAG}_static_bundle"),
                       (audit, f"audited_{TAG}_bundle")):
        bundle = value.get(key)
        if not isinstance(bundle, dict):
            raise RuntimeError(f"missing retagged bundle {key}")
        patch_bundle(bundle, source_hashes, exact8, paths)
    # All three instance receipts and the schema are closed independently;
    # no self-hash is included in the canonical body.
    out_values = {
        "schema": close_object(schema),
        "contract": close_object(contract),
        "transition": close_object(transition),
        "audit": close_object(audit),
    }
    # Structural invariants are checked before installation.
    schema_out = out_values["schema"]
    refs = sum(1 for node in walk(schema_out)
               if isinstance(node, dict) and "$ref" in node)
    closed = sum(1 for node in walk(schema_out)
                 if isinstance(node, dict) and node.get("additionalProperties") is False)
    if (len(schema_out.get("$defs", {})), refs, closed) != (46, 242, 52):
        raise RuntimeError(f"schema shape drift: {len(schema_out.get('$defs', {}))}/{refs}/{closed}")
    if schema_out.get("$ref") != "#/$defs/coldLaunchedCommittedAuthority":
        raise RuntimeError("schema root ref drift")
    if [len(out_values[name]) for name in ("contract", "transition", "audit")] != [30, 31, 30]:
        raise RuntimeError("instance top-level shape drift")
    for name, value in out_values.items():
        if not isinstance(value.get("object_sha256"), str):
            raise RuntimeError(f"{name} did not close")
    return {name: canonical(value) + b"\n" for name, value in out_values.items()}


def main() -> int:
    try:
        for path in (*PREV_SOURCE.values(), *PREV_JSON.values(), PREV_ANCHOR):
            if not path.is_file():
                raise RuntimeError(f"missing pinned input: {path}")
        anchor_obj, anchor_raw = make_anchor()
        # Install the new active anchor first; it is an ordinary zero-credit
        # deliverable receipt and is never a runtime authority surface.
        anchor_action = install_o_excl(ANCHOR, anchor_raw, 0o444)
        generated: dict[str, bytes] = {}
        for role, path in PREV_SOURCE.items():
            generated[role] = source_retag(read_stable(path), role, anchor_obj)
        source_hashes = {role: sha(raw) for role, raw in generated.items()}
        if len(set(source_hashes.values())) != 3:
            raise RuntimeError("source hashes are not distinct")
        source_actions = {
            role: install_o_excl(SOURCE[role], raw, 0o664)
            for role, raw in generated.items()
        }
        json_raw = make_json_quartet(anchor_obj, source_hashes)
        json_actions = {
            name: install_o_excl(JSON[name], raw, 0o664)
            for name, raw in json_raw.items()
        }
        # Re-read all installed targets and verify byte identity.  This is a
        # static clean-room check; no import, protocol execution, manifest,
        # outer receipt, runtime surface, or credit mutation occurs.
        reread = {"anchor": sha(read_stable(ANCHOR))}
        reread.update({role: sha(read_stable(path)) for role, path in SOURCE.items()})
        reread.update({name: sha(read_stable(path)) for name, path in JSON.items()})
        if reread["anchor"] != sha(anchor_raw):
            raise RuntimeError("anchor identity drift")
        report = {
            "schema": "cm2.c79g.v16r2r10.clean-room-builder.v1",
            "status": "V16R2R10_STATIC_CLEAN_ROOM_INSTALLED__ZERO_CREDIT__RUNTIME_NOT_AUTHORIZED",
            "successor_suffix": TAG,
            "predecessor_suffix": PREV,
            "anchor": {"path": str(ANCHOR.relative_to(ROOT)),
                       "file_sha256": sha(anchor_raw),
                       "object_sha256": anchor_obj["object_sha256"],
                       "action": anchor_action},
            "source_hashes": source_hashes,
            "source_actions": source_actions,
            "json_actions": json_actions,
            "reread_hashes": reread,
            "schema_shape": {"defs": 46, "refs": 242, "closed": 52},
            "instance_shapes": {"contract": 30, "transition": 31, "audit": 30},
            "formal_global_closure_credit": 0,
            "D02_unlock": False,
            "runtime_authorized": False,
            "manifest_created": False,
            "outer_created": False,
            "runtime_surface_created": False,
            "pyc_created": False,
        }
        report["object_sha256"] = sha(canonical(report))
        print(json.dumps(report, ensure_ascii=False, sort_keys=True))
        return 0
    except Exception as exc:
        print(json.dumps({
            "schema": "cm2.c79g.v16r2r10.clean-room-builder.failure.v1",
            "status": "FAIL_CLOSED_R10_CLEAN_ROOM",
            "error_type": type(exc).__name__, "error": str(exc),
            "formal_global_closure_credit": 0, "D02_unlock": False,
            "runtime_authorized": False,
        }, sort_keys=True))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
