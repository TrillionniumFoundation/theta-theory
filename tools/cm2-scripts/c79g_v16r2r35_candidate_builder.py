#!/usr/bin/env python3
"""Append-only r35 clean-room successor builder.

r34 reached exact10 but its frozen schema contains nine raw checkpoint strings
where schema-node objects are required.  This builder reads the immutable r34
exact10 bytes, creates only the r34 rejection -> r35 supersession/anchor chain,
repairs those nine schema nodes in a fresh r35 JSON object, and derives fresh
r35 source/contract/transition/audit bytes.  It never edits or reuses an r34
namespace, never creates manifest/outer/runtime/credit surfaces, and disables
bytecode before loading the generic in-memory DAG constructor.
"""
from __future__ import annotations

import ast
import contextlib
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import sys
from typing import Any

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
os.environ["CM2_TEMPLATE_SUFFIX"] = "v16r2r34"
os.environ["CM2_TEMPLATE_PREV_SUFFIX"] = "v16r2r33"
os.environ["CM2_PREDECESSOR_SUFFIX"] = "v16r2r34"
os.environ["CM2_SUCCESSOR_SUFFIX"] = "v16r2r35"

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "deliverables"
BASE = "cm2_round306c79g_true_global_no_producer_consumer"
TAG = "v16r2r35"
PREV = "v16r2r34"
UPSTREAM = "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab"
SUCCESSOR_PIN = "dd9d64f3f0bd0dfd00fd399e3154517a34ba19cfb601ec749f44cbc08b03ca1b"

R34_EXACT10 = {
    f"deliverables/{BASE}_v16r2r34_active_predecessor_supersession_receipt_v1.json":
        "b0a47e3ea586aa9bca2fb647ace2086651c318b0676369e09b59d8b705ef7a89",
    f"deliverables/{BASE}_schema_v16r2r34.json":
        "faa68634c03eda0818f970c1963436bcc446a83695c5f20da36f6c632de9192d",
    f"deliverables/{BASE}_contract_v16r2r34.json":
        "3c1e109fbb6a80b83e623131b549bf5007d8c9e3f3676087133714aa5f554b71",
    f"deliverables/{BASE}_v16r2r34_semantic_source.py":
        "e83a718c0a480e4deaa44fc091b18d3438f87519efe7db27f4204cf99a3596ed",
    f"deliverables/{BASE}_independent_verifier_assembler_authority_consumer_v16r2r34_semantic_source.py":
        "877f4a6ba6475ee27ffca8e030302d9af7c5309fcefb689b37be4049682a1e9b",
    f"deliverables/{BASE}_v16r2r33_to_v16r2r34_static_launch_transition_receipt_v1.json":
        "86ccf4e8543a095105958981804b1531a48b4da89f0dc9f1f363bf0c396c7933",
    f"deliverables/{BASE}_static_audit_v16r2r34.json":
        "b924ecbc71ef8e280d1fa15bba22ba0af682711217713b2c7217b475c629e187",
    f"deliverables/{BASE}_cold_launch_v16r2r34_semantic_source.py":
        "24f9686462f47c009118887d1cdfd0f1b22791eeef335bcb64252d3ade931c0a",
    f"deliverables/{BASE}_cold_launch_manifest_v16r2r34.sha256":
        "10dc65def99655225de2483dcda227cc68a510dc1f2a11e1ac504641c52950cc",
    f"deliverables/{BASE}_cold_launch_outer_receipt_v16r2r34.json":
        "9e1b41dd1083f11edcdfd6e26771eff707a14b09dd3dd3c9ba311adcd0c48d07",
}

SCHEMA_NODE_DEFS = (
    "authoritySeal", "coldLaunchedCommittedAuthority", "innerComposite",
    "laterRejection", "presealCommittedSurface", "standaloneOuter",
    "v3OfficialLaterRejectionProof", "v4RejectionSupersessionProof",
    "v7_publication_lock_continuity_incident",
)


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def stable(path: Path) -> bytes:
    fd = os.open(path, os.O_RDONLY | os.O_CLOEXEC |
                 getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(fd)
        if not (os.path.isfile(path) and before.st_nlink == 1):
            raise RuntimeError(f"bad immutable input:{path}")
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
            raise RuntimeError(f"immutable input drift:{path}")
        raw = b"".join(chunks)
        if len(raw) != before.st_size:
            raise RuntimeError(f"immutable input short read:{path}")
        return raw
    finally:
        os.close(fd)


def pyc_inventory() -> dict[str, str]:
    out: dict[str, str] = {}
    for path in ROOT.rglob("*.pyc"):
        if path.is_symlink() or not path.is_file():
            continue
        out[str(path.relative_to(ROOT))] = sha(path.read_bytes())
    return out


def assert_r34_exact10() -> dict[str, str]:
    observed: dict[str, str] = {}
    for relative, expected in R34_EXACT10.items():
        path = ROOT / relative
        raw = stable(path)
        actual = sha(raw)
        if actual != expected:
            raise RuntimeError(f"r34 immutable pin mismatch:{relative}")
        if path.stat().st_nlink != 1 or (path.stat().st_mode & 0o777) != 0o444:
            raise RuntimeError(f"r34 exact10 mode/nlink:{relative}")
        observed[relative] = actual
    return observed


def load_r34_module():
    path = ROOT / "scripts/c79g_v16r2r34_candidate_builder.py"
    raw = stable(path)
    spec = importlib.util.spec_from_file_location("_r34_builder_template_for_r35", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("r34 builder loader")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    exec(compile(raw.decode("utf-8"), str(path), "exec"), module.__dict__, module.__dict__)
    if (module.TAG, module.PREV, module.TEMPLATE, module.TEMPLATE_PREV) != (
            TAG, PREV, "v16r2r34", "v16r2r33"):
        raise RuntimeError("r35 template namespace configuration")
    return module


def repair_schema_nodes(value: Any) -> Any:
    """Retag r34 JSON then restore schema-node object shape at nine paths."""
    if not isinstance(value, dict):
        return value
    defs = value.get("$defs")
    if not isinstance(defs, dict):
        return value
    for name in SCHEMA_NODE_DEFS:
        node = defs.get(name)
        if not isinstance(node, dict):
            raise RuntimeError(f"schema definition missing:{name}")
        props = node.get("properties")
        if not isinstance(props, dict):
            raise RuntimeError(f"schema properties missing:{name}")
        current = props.get("effective_checkpoint_object_sha256")
        if current == UPSTREAM:
            props["effective_checkpoint_object_sha256"] = {"const": UPSTREAM}
        elif current != {"const": UPSTREAM}:
            raise RuntimeError(f"unexpected schema checkpoint node:{name}:{current!r}")
    return value


def install_retag(module):
    inherited = module.retag

    def retag(value: Any) -> Any:
        out = inherited(value)
        return repair_schema_nodes(out)

    module.retag = retag


def schema_node_walk(root: Any) -> list[str]:
    bad: list[str] = []
    supported = {
        "$schema", "$id", "$comment", "title", "description", "$defs", "$ref",
        "type", "const", "additionalProperties", "required", "properties",
        "items", "prefixItems", "minItems", "maxItems", "uniqueItems",
        "minLength", "pattern", "minimum",
    }

    def walk(node: Any, label: str) -> None:
        if not isinstance(node, dict):
            bad.append(label)
            return
        unknown = set(node) - supported
        if unknown:
            bad.append(label + ":unknown=" + ",".join(sorted(unknown)))
        defs = node.get("$defs", {})
        if not isinstance(defs, dict):
            bad.append(label + ".$defs")
            return
        for name, child in defs.items():
            walk(child, label + ".$defs." + str(name))
        props = node.get("properties", {})
        if not isinstance(props, dict):
            bad.append(label + ".properties")
            return
        for name, child in props.items():
            walk(child, label + ".properties." + str(name))
        prefix = node.get("prefixItems", [])
        if not isinstance(prefix, list):
            bad.append(label + ".prefixItems")
        else:
            for i, child in enumerate(prefix):
                walk(child, f"{label}.prefixItems[{i}]")
        items = node.get("items")
        if items is not None and items is not False:
            walk(items, label + ".items")
        additional = node.get("additionalProperties")
        if isinstance(additional, dict):
            walk(additional, label + ".additionalProperties")
        elif additional is not None and not isinstance(additional, bool):
            bad.append(label + ".additionalProperties")

    walk(root, "closed-schema")
    return bad


def run_builder(module) -> tuple[int, str]:
    # The r34 main is used only as an in-memory DAG constructor with all
    # namespace globals parameterized to r35.  It writes only new deliverable
    # rejection/anchor/candidate members through its O_EXCL installer.
    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        rc = module.main()
    return rc, output.getvalue()


def main() -> int:
    before_pyc = pyc_inventory()
    try:
        previous = assert_r34_exact10()
        if any(TAG in path for path in before_pyc):
            raise RuntimeError("r35 pyc preexists")
        if pyc_inventory() != before_pyc:
            raise RuntimeError("initial pyc inventory drift")
        module = load_r34_module()
        install_retag(module)
        rc, raw_output = run_builder(module)
        if not raw_output.strip():
            raise RuntimeError("builder emitted no JSON")
        try:
            result = json.loads(raw_output)
        except json.JSONDecodeError as exc:
            raise RuntimeError("builder output is not one JSON object") from exc
        if not isinstance(result, dict):
            raise RuntimeError("builder output object required")
        # Verify the newly written schema before presenting a success.  A
        # malformed schema is a static rejection even if source files exist.
        schema_path = OUT / f"{BASE}_schema_{TAG}.json"
        repaired = 0
        if schema_path.is_file():
            schema = json.loads(stable(schema_path).decode("utf-8"))
            bad = schema_node_walk(schema)
            if bad:
                raise RuntimeError("r35 schema node walk:" + ",".join(bad[:12]))
            repaired = len(SCHEMA_NODE_DEFS)
        if pyc_inventory() != before_pyc:
            raise RuntimeError("pyc inventory changed")
        if any(path.exists() for path in (
                OUT / f"{BASE}_cold_launch_manifest_{TAG}.sha256",
                OUT / f"{BASE}_cold_launch_outer_receipt_{TAG}.json")):
            raise RuntimeError("r35 manifest/outer unexpectedly created")
        # r34 exact10 is checked again after the constructor to prove the
        # append-only boundary was respected.
        assert_r34_exact10()
        result.update({
            "schema": f"cm2.c79g.{TAG}.candidate-builder.v1",
            "r34_exact10_unchanged": previous == assert_r34_exact10(),
            "schema_node_repairs": repaired,
            "schema_node_repair_names": list(SCHEMA_NODE_DEFS),
            "manifest_created": False,
            "outer_created": False,
            "runtime_authorized": False,
            "formal_global_closure_credit": 0,
            "D02_unlock": False,
            "pyc_created": False,
        })
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
        return int(rc)
    except Exception as exc:
        print(json.dumps({
            "schema": f"cm2.c79g.{TAG}.candidate-builder.failure.v1",
            "status": f"FAIL_CLOSED_{TAG.upper()}_STATIC_BUILD",
            "error": {"type": type(exc).__name__, "message": str(exc)},
            "candidate_install": False,
            "manifest_created": False,
            "outer_created": False,
            "runtime_authorized": False,
            "formal_global_closure_credit": 0,
            "D02_unlock": False,
            "pyc_created": False,
        }, ensure_ascii=False, sort_keys=True))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
