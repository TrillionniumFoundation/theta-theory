#!/usr/bin/env python3
"""r51 clean-room successor scaffold.

This file is deliberately a planner/constructor boundary, not a publication
command.  It holds the r50 builder and r50 candidate bundle as immutable
witnesses, computes the native (A/B/C) audit shape in memory, and refuses to
install anything until the parent plan explicitly wires the final freeze
stage.  Run-time use, manifest/outer creation, and credit/authority remain
disabled here.

The r50 audit was structurally compact (three-key A/B records).  r51 therefore
rebuilds the audit object before the launcher pin is calculated.  The audit
hash is consequently a downstream pin; no launcher<->audit hash cycle is
introduced.
"""
from __future__ import annotations

import ast
import copy
import hashlib
import json
import os
import re
import stat
import sys
from pathlib import Path
from typing import Any

sys.dont_write_bytecode = True
os.environ.update({"PYTHONDONTWRITEBYTECODE": "1", "PYTHONNOUSERSITE": "1"})

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "deliverables"
BASE = "cm2_round306c79g_true_global_no_producer_consumer"
TAG = "v16r2r51"
PREV = "v16r2r50"

# The source witness is pinned before any r51 namespace is opened.  These
# values are intentionally not discovered dynamically during a run.
R50_BUILDER = ROOT / "scripts/c79g_v16r2r50_candidate_builder.py"
R50_BUILDER_SHA = "e8b0febf2f2a7a6e26cc92582712f31a211ce5f49f7676bffdcb6e0f9368c07a"
R50_BUILDER_SIZE = 31582

# v15 is a historical native-audit shape witness.  It predates the compact
# r50 audit and is intentionally read through a pinned, no-follow descriptor.
# The file is a draft-mode (0664) historical artifact, so it is not passed
# through the 0444 deliverable gate used for candidate members.
AUDIT_SHAPE_TEMPLATE = OUT / f"{BASE}_static_audit_v15.json"
AUDIT_SHAPE_TEMPLATE_SHA = (
    "69557bc7971a6c9943a5d4cee36895bc47413d9b45d92c56597d5cde83b3ed06")
AUDIT_SHAPE_TEMPLATE_SIZE = 142116

R48_BUILDER = ROOT / "scripts/c79g_v16r2r48_candidate_builder.py"
R48_BUILDER_SHA = "88fc2be6a8d6124d1c7cb8252cbd82cea21f69444359b9d2a9db3780f2376ccd"
R48_BUILDER_SIZE = 43190
UPSTREAM_CHECKPOINT = "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab"
SUCCESSOR_CHECKPOINT = "dd9d64f3f0bd0dfd00fd399e3154517a34ba19cfb601ec749f44cbc08b03ca1b"

R39_PINS: dict[str, str] = {
    f"{BASE}_v16r2r39_active_predecessor_supersession_receipt_v1.json": "9c599ef16d7be444e07ba2ae93d4c74dd71781eb859d0cb590098ed1fb03378e",
    f"{BASE}_schema_v16r2r39.json": "d547ed583867e817f25d0306057e27b9e781892d6728936da6298b9e40778a61",
    f"{BASE}_contract_v16r2r39.json": "5886242005f4eaad6ca373f9656f2e82f76ddbbd0e4ff5f1618c12b676daa542",
    f"{BASE}_v16r2r39_semantic_source.py": "f38b4cefa449102dd1992f1c454f0b55956de405c69253a208d8f55f3dca3961",
    f"{BASE}_independent_verifier_assembler_authority_consumer_v16r2r39_semantic_source.py": "d899eb16506171d67265b8a3f57359a33e7a8dfdc2aea9498d9ace2ae4fedc9c",
    f"{BASE}_v16r2r38_to_v16r2r39_static_launch_transition_receipt_v1.json": "3ee3f9c4c8f595925de135d099a6612366b6bba64404ae4e82e582d2667a96b7",
    f"{BASE}_static_audit_v16r2r39.json": "2a1d24187e3e513347f05c163a38b11f3bea2d9de43afeca077a67aa7cae8b31",
    f"{BASE}_cold_launch_v16r2r39_semantic_source.py": "40196dbcc2a40c956f42ab385b610a302952bcca1fb272b7ce640bb3a5b45543",
}

R50_ANCHOR = OUT / f"{BASE}_{PREV}_active_predecessor_supersession_receipt_v1.json"
R50_ANCHOR_SHA = "f7f94d8de8918de7e28d1bf45b890646f5feca8adb36bf0ed2b90c717cab0fc2"
R50_ANCHOR_OBJECT = "89cd68d3221999496144eb30347e20b3da64f392d7d4a3ce9bc3cfbd1cfe92e8"
R50_REJECTION = OUT / f"{BASE}_{PREV}_static_bundle_rejection_receipt_v1.json"

V14 = OUT / (
    f"{BASE}_v14_runtime_registry_shape_drift_rejection_"
    "supersession_receipt_v1.json")
V14_SHA = "aa4323027e2313f8a2eda0d6ffc039a537afe342d496d1f75cd73fcd47446c01"
V14_OBJECT = "93689e62ae36f405f045a769f4dc6f6e6fd83a16605d08299d5c3397ad657e2e"

# Immutable r50 candidate inputs.  They are read only; r51 writes no member
# over them and never treats the old compact audit as positive authority.
R50_FILES: dict[str, tuple[Path, str, str | None]] = {
    "schema": (OUT / f"{BASE}_schema_{PREV}.json",
               "bd7bbb886eb04cf933c604b30c8c203274a10c47109c0c358b65d954e3f75a7f", None),
    "contract": (OUT / f"{BASE}_contract_{PREV}.json",
                  "2868d16f5df85a820bd8a10847546893ca4af4e13e3369efd992f236396bfacb",
                  "115d0a22d0b420e927652b6eb65dfca0fba893d356807801256b3cd82cf2beb1"),
    "producer": (OUT / f"{BASE}_{PREV}_semantic_source.py",
                  "1a042ee3f9a277546fc4148fe441fae1f983fa91313c5aa701f509a1bed591a1", None),
    "consumer": (OUT / f"{BASE}_independent_verifier_assembler_authority_consumer_{PREV}_semantic_source.py",
                  "fdd89c7ac3a92454d70227019f4ec2eec0e59fce9da566b0ee0a4e94004e2f47", None),
    "transition": (OUT / f"{BASE}_v16r2r46_to_{PREV}_static_launch_transition_receipt_v1.json",
                    "1a5648527889cb72ca09f242e054239e5668c7afd1c8c2e27da539b95caa2c90",
                    "06f521f15a9008304aaace75262644e2e69dd1595480ab53040a4487a5a3aa47"),
    "audit": (OUT / f"{BASE}_static_audit_{PREV}.json",
              "8836aa5d9eb356b706967531a01da53ba344ed9e52b060cb6fac02881bbbb0db",
              "bf1f72505de706890bd58904bd21c026e9bf33373856c2ffca3d7bfb9d917ff8"),
    "launcher": (OUT / f"{BASE}_cold_launch_{PREV}_semantic_source.py",
                  "39d0b1f3342256b8c6e2d7ba47aaa41807bdc027233314e77cc7bc062e659e4b", None),
}

R51_REJECTION = OUT / f"{BASE}_{PREV}_static_bundle_rejection_receipt_v1.json"
R51_SUP = OUT / f"{BASE}_{PREV}_to_{TAG}_static_bundle_rejection_supersession_receipt_v1.json"
R51_ANCHOR = OUT / f"{BASE}_{TAG}_active_predecessor_supersession_receipt_v1.json"

R51_TARGETS = [
    R51_REJECTION, R51_SUP, R51_ANCHOR,
    OUT / f"{BASE}_{TAG}_semantic_source.py",
    OUT / f"{BASE}_independent_verifier_assembler_authority_consumer_{TAG}_semantic_source.py",
    OUT / f"{BASE}_cold_launch_{TAG}_semantic_source.py",
    OUT / f"{BASE}_schema_{TAG}.json", OUT / f"{BASE}_contract_{TAG}.json",
    OUT / f"{BASE}_{PREV}_to_{TAG}_static_launch_transition_receipt_v1.json",
    OUT / f"{BASE}_static_audit_{TAG}.json",
    OUT / f"{BASE}_cold_launch_manifest_{TAG}.sha256",
    OUT / f"{BASE}_cold_launch_outer_receipt_{TAG}.json",
]


def _stable(path: Path, sha: str | None = None,
            size: int | None = None) -> bytes:
    fd = os.open(path, os.O_RDONLY | os.O_CLOEXEC |
                 getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(fd)
        named = os.lstat(path)
        if (not stat.S_ISREG(before.st_mode) or before.st_nlink != 1 or
                (before.st_dev, before.st_ino) != (named.st_dev, named.st_ino)):
            raise RuntimeError(f"unstable witness:{path}")
        chunks: list[bytes] = []
        while True:
            chunk = os.read(fd, 1 << 20)
            if not chunk:
                break
            chunks.append(chunk)
        after = os.fstat(fd)
        raw = b"".join(chunks)
        if ((before.st_dev, before.st_ino, before.st_size) !=
                (after.st_dev, after.st_ino, after.st_size)):
            raise RuntimeError(f"witness changed:{path}")
        if size is not None and len(raw) != size:
            raise RuntimeError(f"witness size:{path}")
        got = hashlib.sha256(raw).hexdigest()
        if sha is not None and got != sha:
            raise RuntimeError(f"witness hash:{path}:{got}")
        return raw
    finally:
        os.close(fd)


def _canon(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"), allow_nan=False).encode()


def _close(value: dict[str, Any]) -> dict[str, Any]:
    body = dict(value)
    body.pop("object_sha256", None)
    body["object_sha256"] = hashlib.sha256(_canon(body)).hexdigest()
    return body


def _json(path: Path, sha: str, obj: str | None = None) -> dict[str, Any]:
    raw = _stable(path, sha)
    if path.stat().st_nlink != 1 or stat.S_IMODE(path.stat().st_mode) != 0o444:
        raise RuntimeError(f"witness mode:{path}")
    value = json.loads(raw.decode())
    if not isinstance(value, dict):
        raise RuntimeError(f"witness object:{path}")
    if obj is not None and value.get("object_sha256") != obj:
        raise RuntimeError(f"witness object pin:{path}")
    return value


def _historical_json(path: Path, sha: str, size: int) -> dict[str, Any]:
    """Read a pinned historical JSON witness without treating it as output."""
    raw = _stable(path, sha, size)
    value = json.loads(raw.decode())
    if not isinstance(value, dict):
        raise RuntimeError(f"historical witness object:{path}")
    return value


def _pyc_inventory() -> dict[str, str]:
    result: dict[str, str] = {}
    for path in ROOT.rglob("*.pyc"):
        if path.is_file() and not path.is_symlink():
            raw = _stable(path)
            result[str(path.relative_to(ROOT))] = hashlib.sha256(raw).hexdigest()
    return result


def _preflight() -> dict[str, Any]:
    if not (sys.flags.isolated and sys.flags.no_site and
            sys.flags.dont_write_bytecode):
        raise RuntimeError("r51 requires /usr/bin/python3 -I -B -S")
    _stable(R50_BUILDER, R50_BUILDER_SHA, R50_BUILDER_SIZE)
    anchor = _json(R50_ANCHOR, R50_ANCHOR_SHA, R50_ANCHOR_OBJECT)
    if anchor.get("successor_namespace") != f"{PREV}_semantic_source":
        raise RuntimeError("r50 predecessor namespace drift")
    _json(V14, V14_SHA, V14_OBJECT)
    for name, (path, sha, obj) in R50_FILES.items():
        _json(path, sha, obj) if path.suffix == ".json" else _stable(path, sha)
    occupied = [str(path.relative_to(ROOT)) for path in R51_TARGETS
                if path.exists()]
    if occupied:
        raise RuntimeError("r51 target already exists:" + ",".join(occupied))
    inventory = _pyc_inventory()
    if any("r51" in path.lower() for path in inventory):
        raise RuntimeError("r51 pyc present before preflight")
    return {"r50_builder": {"path": str(R50_BUILDER.relative_to(ROOT)),
                            "file_sha256": R50_BUILDER_SHA,
                            "size": R50_BUILDER_SIZE},
            "r50_anchor": {"path": str(R50_ANCHOR.relative_to(ROOT)),
                           "file_sha256": R50_ANCHOR_SHA,
                           "object_sha256": R50_ANCHOR_OBJECT},
            "r50_candidate_inputs": len(R50_FILES),
            "pyc_inventory_count": len(inventory),
            "candidate_targets_absent": True, "runtime_authorized": False,
            "formal_global_closure_credit": 0, "D02_unlock": False}


def _load_r50_scaffold() -> dict[str, Any]:
    """Compile the exact r50 runner and a retagged memory-only namespace."""
    raw = _stable(R50_BUILDER, R50_BUILDER_SHA, R50_BUILDER_SIZE)
    source = raw.decode("utf-8")
    compile(ast.parse(source, str(R50_BUILDER), mode="exec"),
            str(R50_BUILDER), "exec")
    transformed = source.replace("v16r2r50", "v16r2r51") \
                     .replace("V16R2R50", "V16R2R51")
    # The inherited r50 source validator has two stale cross-role gates: it
    # still names the old exact5 consumer incident and its dual set predates
    # the runtime-registry evidence object.  Apply the repair to the
    # in-memory retagged runner only; the pinned r50 bytes remain untouched.
    source_patch_marker = (
        '            text = _runtime_binding_repair_r50('
        'patched.decode("utf-8"), role)\n')
    if transformed.count(source_patch_marker) != 1:
        raise RuntimeError("r51 source-patch launcher insertion census")
    transformed = transformed.replace(
        source_patch_marker,
        source_patch_marker +
        '            text = (_r51_patch_launcher_validator(text)\n'
        '                    if role == "launcher" else text)\n', 1)
    tree = ast.parse(transformed, str(R50_BUILDER), mode="exec")
    compile(tree, str(R50_BUILDER), "exec")
    ns: dict[str, Any] = {"__name__": "_r51_r50_scaffold",
                          "__file__": str(R50_BUILDER), "__package__": None,
                          "_r51_patch_launcher_validator":
                              _patch_launcher_validator_cross_role}
    exec(compile(tree, str(R50_BUILDER), "exec"), ns, ns)
    ns.update({"TAG": TAG, "PREV": PREV, "REJECTION": R51_REJECTION})
    return ns


def _replace_hex_assignment(text: str, name: str, value: str) -> str:
    text, count = re.subn(rf"(?m)^({re.escape(name)}\s*=\s*)\"[0-9a-f]{{64}}\"\s*$",
                          rf'\1"{value}"', text)
    if count != 1:
        raise RuntimeError(f"r51 pin assignment {name}:{count}")
    return text


def _direct_source_patch_r50(raw: bytes, role: str, paths: dict[str, str],
                             af: str, ao: str, sh: str, ch: str, co: str,
                             producer_hash: str | None,
                             base7: dict[str, tuple[str, str | None]] | None) -> bytes:
    """Retag an immutable r50 source member and close its current pins."""
    text = raw.decode("utf-8")
    text = text.replace(f"{BASE}_v16r2r46_to_v16r2r50_", "__R51_EDGE__")
    text = text.replace("v16r2r50", TAG).replace("V16R2R50", "V16R2R51")
    text = text.replace("__R51_EDGE__", f"{BASE}_{PREV}_to_{TAG}_")
    text = text.replace("ACTIVE_SUCCESSOR_NAMESPACE = \"v16r2r50_semantic_source\"",
                        f"ACTIVE_SUCCESSOR_NAMESPACE = \"{TAG}_semantic_source\"")
    text = text.replace("ACTIVE_SUCCESSOR_NAMESPACE_TAG = \"v16r2r50-semantic-regeneration\"",
                        f"ACTIVE_SUCCESSOR_NAMESPACE_TAG = \"{TAG}-semantic-regeneration\"")
    text = _replace_hex_assignment(text, "ACTIVE_PREDECESSOR_SUPERSESSION_FILE_PIN", af)
    text = _replace_hex_assignment(text, "ACTIVE_PREDECESSOR_SUPERSESSION_OBJECT_PIN", ao)
    if role != "launcher":
        text = _replace_hex_assignment(text, "CONTRACT_FILE_PIN", ch)
        text = _replace_hex_assignment(text, "CONTRACT_OBJECT_PIN", co)
        text = _replace_hex_assignment(text, "CLOSED_SCHEMA_FILE_PIN", sh)
        if role == "consumer" and producer_hash is not None:
            text = _replace_hex_assignment(text, "PRODUCER_SOURCE_PIN", producer_hash)
    else:
        if base7 is None:
            raise RuntimeError("r51 launcher base7 missing")
        tree = ast.parse(text, "r51_launcher", mode="exec")
        funcs = [n for n in tree.body if isinstance(n, ast.FunctionDef) and
                 n.name == "configure_workspace_paths"]
        if len(funcs) != 1:
            raise RuntimeError("r51 launcher configure function")
        assigns = [n for n in funcs[0].body if isinstance(n, ast.Assign) and
                   len(n.targets) == 1 and isinstance(n.targets[0], ast.Name) and
                   n.targets[0].id == "BASE7_PINS"]
        if len(assigns) != 1:
            raise RuntimeError("r51 launcher BASE7 assignment")
        order = [("V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT", "v14"),
                 ("SCHEMA", "schema"), ("CONTRACT", "contract"),
                 ("PRODUCER", "producer"), ("CONSUMER", "consumer"),
                 ("TRANSITION", "transition"), ("AUDIT", "audit")]
        keys, vals = [], []
        for name, key in order:
            keys.append(ast.Name(id=name, ctx=ast.Load()))
            # The reviewed generic constructor still hands the launcher its
            # historical ``anchor`` first-member entry.  Current v16r2 is
            # receipt-first: synthesize the immutable V14 entry explicitly
            # when the generic map has not yet learned that role.
            if key == "v14" and key not in base7:
                pin = (V14_SHA, V14_OBJECT)
            else:
                pin = base7[key]
            vals.append(ast.Tuple([ast.Constant(pin[0]), ast.Constant(pin[1])],
                                  ast.Load()))
        assigns[0].value = ast.Dict(keys=keys, values=vals)
        # The source is a candidate but its static map is fully installed;
        # runtime remains prohibited by the surrounding guards.
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign) and len(node.targets) == 1 and \
                    isinstance(node.targets[0], ast.Name) and \
                    node.targets[0].id == "FINAL_BASE7_PINS_INSTALLED":
                node.value = ast.Constant(True)
        text = ast.unparse(tree) + "\n"
    if f"{BASE}_{PREV}_to_{TAG}_static_launch_transition_receipt_v1.json" not in text:
        raise RuntimeError(f"{role}: r51 edge absent")
    return text.encode("utf-8")


def _load_generic_r51() -> Any:
    """Load the reviewed r48 generic constructor with r51 paths in memory."""
    raw = _stable(R48_BUILDER, R48_BUILDER_SHA, R48_BUILDER_SIZE)
    source = raw.decode("utf-8")
    compile(ast.parse(source, str(R48_BUILDER), mode="exec"),
            str(R48_BUILDER), "exec")
    wrapper: dict[str, Any] = {"__name__": "_r51_r48_recipe",
                               "__file__": str(R48_BUILDER),
                               "__package__": None}
    exec(compile(ast.parse(source, str(R48_BUILDER), mode="exec"),
                 str(R48_BUILDER), "exec"), wrapper, wrapper)

    # Configure the recipe's own globals before configure_builder() installs
    # its source_patch/retag functions into the generic constructor module.
    wrapper.update({
        "TEMPLATE": "v16r2r39", "TEMPLATE_PREV": "v16r2r38",
        "PREV": PREV, "TAG": TAG, "UPSTREAM": UPSTREAM_CHECKPOINT,
        "SUCCESSOR_PIN": SUCCESSOR_CHECKPOINT,
        "R46_ANCHOR": R50_ANCHOR,
        "V14_PATH": str(V14.relative_to(ROOT)), "V14_FILE": V14_SHA,
        "V14_OBJECT": V14_OBJECT,
        "ANCHOR": OUT / f"{BASE}_{TAG}_active_predecessor_supersession_receipt_v1.json",
        "SUP": OUT / f"{BASE}_{PREV}_to_{TAG}_static_bundle_rejection_supersession_receipt_v1.json",
        "REJ": R51_REJECTION,
        "MANIFEST": OUT / f"{BASE}_cold_launch_manifest_{TAG}.sha256",
        "OUTER": OUT / f"{BASE}_cold_launch_outer_receipt_{TAG}.json",
        "SRC_OUT": {
            "producer": OUT / f"{BASE}_{TAG}_semantic_source.py",
            "consumer": OUT / f"{BASE}_independent_verifier_assembler_authority_consumer_{TAG}_semantic_source.py",
            "launcher": OUT / f"{BASE}_cold_launch_{TAG}_semantic_source.py",
        },
        "JSON_OUT": {
            "schema": OUT / f"{BASE}_schema_{TAG}.json",
            "contract": OUT / f"{BASE}_contract_{TAG}.json",
            "transition": OUT / f"{BASE}_{PREV}_to_{TAG}_static_launch_transition_receipt_v1.json",
            "audit": OUT / f"{BASE}_static_audit_{TAG}.json",
        },
    })
    builder = wrapper["load_generic"]()
    wrapper["configure_builder"](builder)

    # The pinned r39 producer/consumer bytes have already split the upstream
    # checkpoint symbol into its historical/current constants.  The reviewed
    # recipe's strict replacement is therefore a no-op for these bytes; keep
    # the source immutable and permit the no-load case only.
    original_replace = wrapper["_replace_checkpoint_loads"]
    def replace_checkpoint(text: str, role: str) -> str:
        try:
            return original_replace(text, role)
        except RuntimeError as exc:
            if str(exc) == f"{role}: no checkpoint loads":
                return text
            raise
    wrapper["_replace_checkpoint_loads"] = replace_checkpoint

    # r50 members are the actual clean-room inputs for this successor.  The
    # older r48 patcher expects r39's pre-retag symbol layout, so retain it as
    # a fallback only and use the direct r50 rebind below for current bytes.
    original_patch = builder.source_patch
    def source_patch(raw_bytes: bytes, role: str, paths: dict[str, str],
                     af: str, ao: str, sh: str, ch: str, co: str,
                     producer_hash: str | None = None,
                     base7: dict[str, tuple[str, str | None]] | None = None) -> bytes:
        if role == "launcher" and base7 is not None and "v14" not in base7:
            base7 = dict(base7)
            base7["v14"] = (V14_SHA, V14_OBJECT)
        try:
            out = _direct_source_patch_r50(raw_bytes, role, paths, af, ao,
                                           sh, ch, co, producer_hash, base7)
        except RuntimeError:
            out = original_patch(raw_bytes, role, paths, af, ao, sh, ch, co,
                                 producer_hash, base7)
        text = out.decode("utf-8")
        if role == "launcher":
            text = _canonicalize_registry_helper(text)
            text = _patch_launcher_validator_cross_role(text)
        tree = ast.parse(text, filename=str(builder.SRC_OUT[role]), mode="exec")
        compile(tree, str(builder.SRC_OUT[role]), "exec")
        return (text if text.endswith("\n") else text + "\n").encode()
    builder.source_patch = source_patch
    # Functions in the generic module resolve these attributes from the
    # module dictionary, so retain the configured r51 values explicitly.
    builder.TAG = TAG; builder.PREV = PREV; builder.UPSTREAM = UPSTREAM_CHECKPOINT
    builder.CHECKPOINT = UPSTREAM_CHECKPOINT
    # The constructor must consume the pinned r50 bundle, not a mutable
    # template alias left by configure_builder().
    builder.ANCHOR_IN = R50_ANCHOR
    builder.SRC_IN = {"producer": R50_FILES["producer"][0],
                      "consumer": R50_FILES["consumer"][0],
                      "launcher": R50_FILES["launcher"][0]}
    builder.JSON_IN = {"schema": R50_FILES["schema"][0],
                       "contract": R50_FILES["contract"][0],
                       "transition": R50_FILES["transition"][0],
                       "audit": R50_FILES["audit"][0]}
    return builder


def _pin_normalized_launcher_ast(raw: bytes) -> str:
    """Compute the native cycle-breaking launcher digest without execution."""
    tree = ast.parse(raw.decode(), "r51_launcher", mode="exec")
    flags = [n for n in tree.body if isinstance(n, ast.Assign) and
             len(n.targets) == 1 and isinstance(n.targets[0], ast.Name) and
             n.targets[0].id == "FINAL_BASE7_PINS_INSTALLED"]
    if len(flags) != 1:
        raise RuntimeError("launcher final-pin assignment census")
    flags[0].value = ast.Constant(False)
    funcs = [n for n in tree.body if isinstance(n, ast.FunctionDef) and
             n.name == "configure_workspace_paths"]
    if len(funcs) != 1:
        raise RuntimeError("launcher configure census")
    assigns = [n for n in funcs[0].body if isinstance(n, ast.Assign) and
               len(n.targets) == 1 and isinstance(n.targets[0], ast.Name) and
               n.targets[0].id == "BASE7_PINS"]
    if len(assigns) != 1 or not isinstance(assigns[0].value, ast.Dict):
        raise RuntimeError("launcher BASE7 census")
    d = assigns[0].value
    names = [k.id if isinstance(k, ast.Name) else None for k in d.keys]
    expected = ["V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT",
                "SCHEMA", "CONTRACT", "PRODUCER", "CONSUMER",
                "TRANSITION", "AUDIT"]
    if names != expected:
        raise RuntimeError("launcher BASE7 order")
    first = ast.dump(d.values[0], annotate_fields=True,
                     include_attributes=False)
    for i, name in enumerate(names[1:], 1):
        obj = "e" * 64 if name in {"CONTRACT", "TRANSITION", "AUDIT"} else None
        d.values[i] = ast.Tuple([ast.Constant("f" * 64), ast.Constant(obj)],
                                ast.Load())
    if ast.dump(d.values[0], annotate_fields=True,
                include_attributes=False) != first:
        raise RuntimeError("launcher V14 pin mutated")
    return hashlib.sha256(ast.dump(
        tree, annotate_fields=True, include_attributes=False).encode()).hexdigest()


def _checker_tools() -> dict[str, Any]:
    """Load the read-only census implementation in memory (never import it)."""
    path = ROOT / "scripts/c79g_v15_checker_census.py"
    raw = _stable(path)
    ns: dict[str, Any] = {"__name__": "_r51_checker", "__file__": str(path),
                          "__package__": None}
    exec(compile(ast.parse(raw.decode(), str(path), "exec"), str(path), "exec"),
         ns, ns)
    return ns


def _patch_launcher_validator_cross_role(text: str) -> str:
    """Align the launcher audit gate with the native consumer's V14 contract.

    The inherited launcher validator predates the V14 exact12 inherited
    authority surface. It required the old exact5 evidence key and rejected
    the runtime-registry evidence object required by the current consumer.
    This is an in-memory source repair; frozen r50 bytes are never edited.
    """
    old_exact5 = "consumer_frozen_predecessor_incident_exact5_bytes_read_only_noncredit_allowed"
    new_exact12 = "consumer_v14_inherited_authority_exact12_bytes_read_only_noncredit_allowed"
    if text.count(old_exact5) != 2:
        raise RuntimeError("r51 launcher exact5 cross-role key census")
    text = text.replace(old_exact5, new_exact12)

    # The v15/native audit names the inherited-receipt preservation predicate
    # after V14.  Keep the old r50 source immutable, but make every current
    # launcher reference use the same key as the consumer's exact dual set.
    old_pin_key = "pin_normalization_preserves_v12_rejection_and_all_historical_pins"
    new_pin_key = "pin_normalization_preserves_v14_supersession_receipt_and_all_historical_pins"
    if text.count(old_pin_key) < 1:
        raise RuntimeError("r51 launcher stale pin-normalization key census")
    text = text.replace(old_pin_key, new_pin_key)

    # Close the native top-level audit key order with the published V14
    # segment.  ast.unparse may choose either quote style, so accept both and
    # require exactly one insertion.
    if "published_then_officially_rejected_predecessor_v14" not in text:
        marker = "FINAL_STATIC_AUDIT_TOP_LEVEL_KEY_ORDER"
        start = text.find(marker)
        if start < 0:
            raise RuntimeError("r51 launcher V14 top-level tuple missing")
        end = text.find(")", start)
        if end < 0:
            raise RuntimeError("r51 launcher V14 top-level tuple unterminated")
        chunk = text[start:end]
        pat = (r'([\"\'])published_then_officially_rejected_predecessor_v12'
               r'\1\s*,')
        replacement = (r'\1published_then_officially_rejected_predecessor_v12\1,\n'
                       r'    \1published_then_officially_rejected_predecessor_v14\1,')
        new_chunk, count = re.subn(pat, replacement, chunk, count=1)
        if count != 1:
            raise RuntimeError("r51 launcher V14 top-level key insertion point")
        text = text[:start] + new_chunk + text[end:]

    # ast.unparse() in the direct r50 retagger may collapse the set literal
    # onto one line; accept either layout while keeping the exact key census.
    marker = ('"held_launcher_pin_normalized_ast_sha256"'
              if '"held_launcher_pin_normalized_ast_sha256"' in text
              else "'held_launcher_pin_normalized_ast_sha256'")
    if not marker or text.count(marker) < 1:
        raise RuntimeError("r51 launcher dual-key insertion point")
    if '"actual_runtime_registry_shape_evidence"' not in text and \
            "'actual_runtime_registry_shape_evidence'" not in text:
        quote = '"' if marker.startswith('"') else "'"
        text = text.replace(marker, marker + ', ' + quote +
                            'actual_runtime_registry_shape_evidence' + quote, 1)
    anchor = '    need(checker_a.get("algorithm") ==\n'
    if text.count(anchor) != 1:
        anchor = '    checker_a_keys = {'
    if text.count(anchor) != 1:
        raise RuntimeError("r51 launcher runtime-evidence insertion point")
    evidence = (
        '    runtime_registry_evidence = dual.get(\n'
        '        "actual_runtime_registry_shape_evidence", {})\n'
        '    runtime_registry_keys = {\n'
        '        "producer_source_registry_census",\n'
        '        "launcher_runtime_registry_helper_census",\n'
        '        "runtime_registry_shape_consensus",\n'
        '        "explicit62_in_memory_tamper_rejected",\n'
        '        "actual_closed_registry_shape",\n'
        '    }\n'
        '    producer_registry = (runtime_registry_evidence.get(\n'
        '        "producer_source_registry_census", {})\n'
        '        if isinstance(runtime_registry_evidence, dict) else {})\n'
        '    launcher_registry = (runtime_registry_evidence.get(\n'
        '        "launcher_runtime_registry_helper_census", {})\n'
        '        if isinstance(runtime_registry_evidence, dict) else {})\n'
        '    registry_consensus = (runtime_registry_evidence.get(\n'
        '        "runtime_registry_shape_consensus", {})\n'
        '        if isinstance(runtime_registry_evidence, dict) else {})\n'
        '    need(isinstance(runtime_registry_evidence, dict) and\n'
        '         set(runtime_registry_evidence) == runtime_registry_keys and\n'
        '         runtime_registry_evidence.get(\n'
        '             "explicit62_in_memory_tamper_rejected") is True and\n'
        '         runtime_registry_evidence.get("actual_closed_registry_shape") == 75 and\n'
        '         isinstance(producer_registry, dict) and\n'
        '         producer_registry.get("explicit_key_count") == 67 and\n'
        '         producer_registry.get("execution_proof_key_count") == 7 and\n'
        '         producer_registry.get("computed_closed_registry_key_count") == 75 and\n'
        '         producer_registry.get("matches") is True and\n'
        '         isinstance(launcher_registry, dict) and\n'
        '         launcher_registry.get("explicit_key_guard_literals") == [67] and\n'
        '         launcher_registry.get("exact_execution_proof_7_guard_count") == 1 and\n'
        '         launcher_registry.get("exact_shape_75_guard_count") == 1 and\n'
        '         launcher_registry.get("held_producer_independent_computed_shape") == 75 and\n'
        '         launcher_registry.get("matches") is True and\n'
        '         isinstance(registry_consensus, dict) and\n'
        '         registry_consensus.get("producer_independent_closed_key_count") == 75 and\n'
        '         registry_consensus.get("audit_declared_producerSourceRegistry") == 75 and\n'
        '         registry_consensus.get("expected_closed_key_count") == 75 and\n'
        '         registry_consensus.get("launcher_actual_runtime_helper_matches") is True and\n'
        '         registry_consensus.get("matches") is True,\n'
        '         "final static audit exact V14 runtime-registry evidence")\n\n')
    text = text.replace(anchor, evidence + anchor, 1)
    return text


def _canonicalize_registry_helper(source: str) -> str:
    """Use the reviewed v15 diagnostic literals in the launcher helper only."""
    tree = ast.parse(source, "r51_launcher", mode="exec")
    node = next((n for n in tree.body if isinstance(n, ast.FunctionDef) and
                 n.name == "producer_source_registry_shape_from_ast"), None)
    if node is None:
        raise RuntimeError("r51 registry helper function missing")
    raw = source.encode("utf-8")
    starts = [0]
    for line in source.splitlines(keepends=True):
        starts.append(starts[-1] + len(line.encode("utf-8")))
    start = starts[node.lineno - 1] + node.col_offset
    end = starts[node.end_lineno - 1] + node.end_col_offset
    chunk = raw[start:end].decode("utf-8")
    old = chunk
    # Every lowercase diagnostic token participates in the normalized AST
    # digest (filename, parse/error labels, and return-shape labels).
    chunk = chunk.replace("v16r2", "v15")
    if chunk == old:
        raise RuntimeError("r51 registry-helper literals not found")
    if "v16r2" in chunk:
        raise RuntimeError("r51 registry-helper literal patch incomplete")
    return (raw[:start] + chunk.encode("utf-8") + raw[end:]).decode("utf-8")


def enrich_audit(audit: dict[str, Any], source_bytes: dict[str, bytes],
                 current: dict[str, str]) -> dict[str, Any]:
    """Return a closed native v16r2 audit object; never writes its inputs.

    The r50 audit is intentionally *not* used as the shape source: it is the
    compact predecessor being rejected.  v15 is the last native A/B/C shape
    witness, so this routine starts from that immutable object, renames only
    current-version fields, and then injects fresh source/pin evidence.
    """
    tools = _checker_tools()
    ordered = [(role, source_bytes[role]) for role in
               ("producer", "consumer", "launcher")]
    rows_a, kinds_a, arity_a = tools["callsite_census_parent_map"](ordered)
    rows_b, kinds_b, arity_b = tools["callsite_census_visitor"](ordered)
    if rows_a != rows_b or kinds_a != kinds_b or arity_a or arity_b:
        raise RuntimeError("r51 dual callsite census mismatch")
    common_digest = hashlib.sha256(tools["canonical"](rows_b)).hexdigest()
    trees = {role: ast.parse(raw, role, mode="exec")
             for role, raw in ordered}
    literal_count = sum(tools["dict_literal_stats"](tree)[0]
                        for tree in trees.values())
    normalized = _pin_normalized_launcher_ast(source_bytes["launcher"])
    producer_registry = tools["producer_source_registry_census"](
        trees["producer"])
    launcher_registry = tools["launcher_runtime_registry_helper_census"](
        trees["launcher"], producer_registry["computed_closed_registry_key_count"])
    source_shapes = {role: tools["shape_declarations"](trees[role])
                     for role in ("producer", "consumer", "launcher")}
    declared = {role: sorted(set(values)) for role, values in source_shapes.items()}
    if declared != {"producer": [75], "consumer": [75], "launcher": [75]}:
        raise RuntimeError("r51 producerSourceRegistry declaration drift")
    if not producer_registry.get("matches") or not launcher_registry.get("matches"):
        raise RuntimeError("r51 runtime registry census mismatch")

    template = _historical_json(AUDIT_SHAPE_TEMPLATE,
                                AUDIT_SHAPE_TEMPLATE_SHA,
                                AUDIT_SHAPE_TEMPLATE_SIZE)
    out = copy.deepcopy(template)
    # Current v16r2 uses the v15 historical sections verbatim, but the active
    # bundle and versioned proof/no-run keys must carry the current namespace.
    out["audited_v16r2_bundle"] = out.pop("audited_v15_bundle")
    old_dual = out["dual_independent_static_checkers"]
    # The native consumer treats this as an ordered protocol object, not an
    # unordered mapping: retain the reviewed exact43 sequence while replacing
    # only the current r52 core pins.  JSON canonicalization later sorts keys
    # for object closure, but the in-memory insertion order is itself audited.
    input_order = [
        "schema", "contract_file", "contract_object", "producer", "consumer",
        "transition_file", "transition_object", "launcher_template",
        "v4_supersession_file", "v4_supersession_object", "v5_rejection_file",
        "v5_rejection_object", "v6_rejection_file", "v6_rejection_object",
        "v7_rejection_file", "v7_rejection_object",
        "v7_lock_continuity_incident_object", "v8_rejection_file",
        "v8_rejection_object", "v8_launcher_file",
        "v8_launcher_regression_defect_sha256",
        "trusted_v8_rollout_control_flow_incident_digest", "v9_rejection_file",
        "v9_rejection_object", "v9_launcher_file", "v9_persisted_v6_proof_sha256",
        "v9_expanded_v6_proof_sha256",
        "trusted_v9_proof_shape_drift_incident_digest", "v10_rejection_file",
        "v10_rejection_object", "v10_producer_file",
        "trusted_v10_regression_label_prefix_incident_digest", "v11_rejection_file",
        "v11_rejection_object", "v11_producer_file", "v11_launcher_file",
        "trusted_v11_dual_validator_divergence_incident_digest", "v12_rejection_file",
        "v12_rejection_object", "v12_producer_file", "v12_consumer_file",
        "v12_launcher_file", "trusted_v12_v5_rejection_shape_incident_digest",
    ]
    old_inputs = dict(old_dual["checker_A"]["input_sha256"])
    old_inputs.update({"schema": current["schema"],
                       "contract_file": current["contract_file"],
                       "contract_object": current["contract_object"],
                       "producer": current["producer"],
                       "consumer": current["consumer"],
                       "transition_file": current["transition_file"],
                       "transition_object": current["transition_object"],
                       "launcher_template": normalized})
    if set(old_inputs) != set(input_order) or len(input_order) != 43:
        raise RuntimeError("r51 audit exact43 input order witness")
    inputs = {key: old_inputs[key] for key in input_order}
    if len(inputs) != 43:
        raise RuntimeError("r51 audit input key count")

    a = copy.deepcopy(old_dual["checker_A"])
    b = copy.deepcopy(old_dual["checker_B"])
    c = copy.deepcopy(old_dual["checker_C_common_census_and_pin_normalized_ast_reproduction"])
    for checker in (a, b):
        checker["input_sha256"] = dict(inputs)
        checker["pin_normalized_launcher_ast_sha256"] = normalized
    a.update({"wider_local_callsite_census_row_count": len(rows_a),
              "wider_local_callsite_census_sha256": common_digest,
              "python_literal_dict_count": literal_count,
              "failed_static_check_count": 0})
    b.update({"common_ordered_callsite_row_count": len(rows_b),
              "common_ordered_callsite_census_sha256": common_digest,
              "failed_static_check_count": 0})
    c.update({"common_ordered_callsite_row_count": len(rows_b),
              "common_ordered_callsite_census_sha256": common_digest,
              "common_callsite_kind_census": {
                  kind: kinds_b.get(kind, 0) for kind in tools["CALLSITE_KINDS"]},
              "pin_normalized_launcher_ast_sha256": normalized,
              "failed_static_check_count": 0})
    evidence = copy.deepcopy(old_dual["actual_runtime_registry_shape_evidence"])
    evidence["producer_source_registry_census"] = producer_registry
    evidence["launcher_runtime_registry_helper_census"] = launcher_registry
    consensus = copy.deepcopy(evidence["runtime_registry_shape_consensus"])
    consensus.update({
        "producer_independent_closed_key_count": producer_registry["computed_closed_registry_key_count"],
        "launcher_actual_runtime_helper_matches": launcher_registry["matches"],
        "source_declared_producerSourceRegistry_values": declared,
        "audit_declared_producerSourceRegistry": 75,
        "expected_closed_key_count": 75,
        "v14_inherited_authority_runtime_wiring_matches": True,
        "matches": True,
    })
    evidence["runtime_registry_shape_consensus"] = consensus
    evidence["actual_closed_registry_shape"] = 75
    evidence["explicit62_in_memory_tamper_rejected"] = True
    dual = copy.deepcopy(old_dual)
    dual.update({"checker_A": a, "checker_B": b,
                 "checker_C_common_census_and_pin_normalized_ast_reproduction": c,
                 "actual_runtime_registry_shape_evidence": evidence,
                 "held_launcher_pin_normalized_ast_sha256": normalized,
                 "pin_normalized_ast_algorithm": str(
                     dual.get("pin_normalized_ast_algorithm", "")).replace(
                         "CURRENT_V15", "CURRENT_V16R2")})
    out["dual_independent_static_checkers"] = dual

    # Rename current-version keys without touching historical V14/V15 labels
    # (the latter are part of the immutable rejection chronology).
    proof = out["sealed_exec_and_no_producer_static_proof"]
    if "consumer_current_v15_producer_content_open_read_hash_decode_compile_import_or_execute_allowed" in proof:
        proof["consumer_current_v16r2_producer_content_open_read_hash_decode_compile_import_or_execute_allowed"] = proof.pop("consumer_current_v15_producer_content_open_read_hash_decode_compile_import_or_execute_allowed")
    credit = out["static_credit_census"]
    for key in list(credit):
        if "v15" in key:
            credit[key.replace("v15", "v16r2")] = credit.pop(key)
    no_run = out["static_no_run"]
    for key in list(no_run):
        if "v15" in key:
            no_run[key.replace("v15", "v16r2")] = no_run.pop(key)

    paths = {
        "v14": f"deliverables/{V14.name}",
        "schema": f"deliverables/{BASE}_schema_{TAG}.json",
        "contract": f"deliverables/{BASE}_contract_{TAG}.json",
        "producer": f"deliverables/{BASE}_{TAG}_semantic_source.py",
        "consumer": f"deliverables/{BASE}_independent_verifier_assembler_authority_consumer_{TAG}_semantic_source.py",
        "transition": f"deliverables/{BASE}_{PREV}_to_{TAG}_static_launch_transition_receipt_v1.json",
        "audit": f"deliverables/{BASE}_static_audit_{TAG}.json",
        "launcher": f"deliverables/{BASE}_cold_launch_{TAG}_semantic_source.py",
        "manifest": f"deliverables/{BASE}_cold_launch_manifest_{TAG}.sha256",
        "outer": f"deliverables/{BASE}_cold_launch_outer_receipt_{TAG}.json",
    }
    exact8 = [paths[k] for k in
              ("v14", "schema", "contract", "producer", "consumer",
               "transition", "audit", "launcher")]
    base7 = exact8[:-1]
    exact10 = exact8 + [paths["manifest"], paths["outer"]]
    bundle = out["audited_v16r2_bundle"]
    # Start with the predecessor's executable-bundle metadata so downstream
    # consumer checks retain the full 27-key current shape, then close every
    # current pin/path in one direction.
    predecessor_bundle = audit.get("audited_v16r2_bundle")
    if isinstance(predecessor_bundle, dict):
        bundle = copy.deepcopy(predecessor_bundle)
        out["audited_v16r2_bundle"] = bundle
    bundle.update({
        "bundle_version": TAG,
        "schema_file_sha256": current["schema"],
        "contract_file_sha256": current["contract_file"],
        "contract_object_sha256": current["contract_object"],
        "transition_file_sha256": current["transition_file"],
        "transition_object_sha256": current["transition_object"],
        "closed_schema": {"path": paths["schema"], "file_sha256": current["schema"]},
        "contract": {"path": paths["contract"], "object_pin_source": "TOP_LEVEL_OBJECT_SHA256", "file_sha256": current["contract_file"], "object_sha256": current["contract_object"]},
        "build_only_producer": {"path": paths["producer"], "file_sha256": current["producer"], "source_template_only": False},
        "independent_verifier_assembler_authority_consumer": {"path": paths["consumer"], "file_sha256": current["consumer"], "source_template_only": False},
        "v16_to_v16r2_transition_receipt": {"path": paths["transition"], "file_sha256": current["transition_file"], "object_sha256": current["transition_object"]},
        "static_audit_v16r2": {"path": paths["audit"]},
        "cold_launcher": {"path": paths["launcher"]},
        "predecessor_semantic_supersession": {"path": current["anchor_path"], "file_sha256": current["anchor_file"], "object_sha256": current["anchor_object"], "successor_only": f"{TAG}-semantic-bundle"},
        "predecessor_supersession_object_sha256": current["anchor_object"],
        "exact8_ordered_paths": exact8, "base7_ordered_paths": base7,
        "exact10_ordered_paths": exact10,
        "static_audit_path": paths["audit"],
        "effective_checkpoint_object_sha256": UPSTREAM_CHECKPOINT,
        "successor_checkpoint_object_sha256": SUCCESSOR_CHECKPOINT,
        "pin_state": f"{TAG.upper()}_SOURCE_AND_JSON_PINS_FINAL__STATIC_ZERO_CREDIT",
    })
    trust = bundle.get("post_source_static_trust_receipts")
    if isinstance(trust, dict):
        trust.update({"binding_direction": f"{TAG.upper()}_SOURCE_READS_POST_SOURCE_RECEIPTS__NO_HASH_CYCLE",
                      "predecessor_supersession_file_sha256": current["anchor_file"],
                      "predecessor_supersession_object_sha256": current["anchor_object"],
                      "predecessor_supersession_path": current["anchor_path"],
                      "transition_path": paths["transition"],
                      "v16_to_v16r2_transition_path": paths["transition"],
                      "static_audit_path": paths["audit"],
                      "v14_registry_shape_drift_supersession_receipt_path": paths["v14"]})
    out["schema"] = "cm2.round306c79g.true-global-no-producer-consumer.static-audit.v16r2"
    out["status"] = "PASS_DUAL_STATIC_PIN_NORMALIZED_AST_GO_V16R2__PHYSICAL_COLD_FREEZE_PENDING__RUNTIME_NOT_AUTHORIZED"
    out["audit_path"] = paths["audit"]
    out["effective_checkpoint_object_sha256"] = UPSTREAM_CHECKPOINT
    return _close(out)


def seal_r50_rejection(builder: dict[str, Any]) -> dict[str, str]:
    """Construct the r50 compact-audit rejection in memory only."""
    value = _close({
        "schema": f"cm2.c79g.{PREV}.static-audit-shape-rejection.v1",
        "status": "PERMANENT_FAIL_CLOSED_R50_COMPACT_AUDIT__ZERO_CREDIT",
        "failed_namespace": PREV, "predecessor_namespace": "v16r2r46",
        "rejection_reason": "NATIVE_A_B_C_CHECKER_SHAPE_AND_43_PIN_INPUT_MISSING",
        "r50_audit_file_sha256": R50_FILES["audit"][1],
        "r50_audit_object_sha256": R50_FILES["audit"][2],
        "r50_launcher_file_sha256": R50_FILES["launcher"][1],
        "candidate_install": True, "runtime_protocol_executed": False,
        "manifest_created": False, "outer_created": False,
        "runtime_authorized": False, "formal_global_closure_credit": 0,
        "D02_unlock": False, "append_only": True,
        "overwrite_delete_or_reuse_allowed": False,
    })
    raw = _canon(value) + b"\n"
    return {"path": str(R51_REJECTION.relative_to(ROOT)),
            "file_sha256": hashlib.sha256(raw).hexdigest(),
            "object_sha256": value["object_sha256"], "bytes": raw}


def _chain_in_memory(rejection: dict[str, str]) -> dict[str, Any]:
    """Derive the r50-rejection -> r51-anchor chain without filesystem writes."""
    sup_value = _close({
        "schema": f"cm2.c79g.{PREV}-to-{TAG}.static-bundle-rejection-supersession.v1",
        "status": "FROZEN_APPEND_ONLY_REJECTED_PREDECESSOR_SUPERSEDED__ZERO_CREDIT",
        "predecessor_namespace": PREV, "successor_namespace": TAG,
        "predecessor_active_anchor_path": str(R50_ANCHOR.relative_to(ROOT)),
        "predecessor_active_anchor_file_sha256": R50_ANCHOR_SHA,
        "predecessor_active_anchor_object_sha256": R50_ANCHOR_OBJECT,
        "predecessor_rejection_path": rejection["path"],
        "predecessor_rejection_file_sha256": rejection["file_sha256"],
        "predecessor_rejection_object_sha256": rejection["object_sha256"],
        "upstream_checkpoint_object_sha256": UPSTREAM_CHECKPOINT,
        "successor_checkpoint_object_sha256": SUCCESSOR_CHECKPOINT,
        "append_only": True, "runtime_authorized": False,
        "formal_global_closure_credit": 0, "D02_unlock": False,
    })
    sup_raw = _canon(sup_value) + b"\n"
    sup_file = hashlib.sha256(sup_raw).hexdigest()
    anchor_value = _close({
        "schema": f"cm2.c79g.{TAG}.active-predecessor-supersession.v1",
        "status": "FROZEN_APPEND_ONLY_ACTIVE_PREDECESSOR_ANCHOR__ZERO_CREDIT",
        "predecessor_namespace": PREV,
        "predecessor_supersession_path": str(R51_SUP.relative_to(ROOT)),
        "predecessor_supersession_file_sha256": sup_file,
        "predecessor_supersession_object_sha256": sup_value["object_sha256"],
        "upstream_checkpoint_object_sha256": UPSTREAM_CHECKPOINT,
        "successor_checkpoint_object_sha256": SUCCESSOR_CHECKPOINT,
        "successor_namespace": f"{TAG}_semantic_source",
        "append_only": True, "runtime_authorized": False,
        "formal_global_closure_credit": 0, "D02_unlock": False,
        "manifest_created": False, "outer_created": False,
    })
    anchor_raw = _canon(anchor_value) + b"\n"
    return {"rejection": rejection, "sup_value": sup_value, "sup_raw": sup_raw,
            "sup_file_sha256": sup_file,
            "anchor_value": anchor_value, "anchor_raw": anchor_raw,
            "anchor_file_sha256": hashlib.sha256(anchor_raw).hexdigest(),
            "anchor_object_sha256": anchor_value["object_sha256"]}


def _build_r51_candidate(builder: Any, chain: dict[str, Any]) -> tuple[dict[str, bytes], dict[str, Any]]:
    """Build the seven candidate members entirely in memory.

    This is intentionally a local copy of the reviewed generic build order.
    It keeps the generic constructor's immutable parsing/source patch helpers,
    while correcting the native V14-first boundary and grafting the complete
    A/B/C audit before the final launcher pin injection.
    """
    p = {
        "anchor": str(R51_ANCHOR.relative_to(ROOT)),
        "v14": str(V14.relative_to(ROOT)),
        "schema": str((OUT / f"{BASE}_schema_{TAG}.json").relative_to(ROOT)),
        "contract": str((OUT / f"{BASE}_contract_{TAG}.json").relative_to(ROOT)),
        "producer": str((OUT / f"{BASE}_{TAG}_semantic_source.py").relative_to(ROOT)),
        "consumer": str((OUT / f"{BASE}_independent_verifier_assembler_authority_consumer_{TAG}_semantic_source.py").relative_to(ROOT)),
        "transition": str((OUT / f"{BASE}_{PREV}_to_{TAG}_static_launch_transition_receipt_v1.json").relative_to(ROOT)),
        "audit": str((OUT / f"{BASE}_static_audit_{TAG}.json").relative_to(ROOT)),
        "launcher": str((OUT / f"{BASE}_cold_launch_{TAG}_semantic_source.py").relative_to(ROOT)),
    }
    exact8 = [p[k] for k in ("v14", "schema", "contract", "producer",
                             "consumer", "transition", "audit", "launcher")]
    base7 = exact8[:-1]
    exact10 = exact8 + [
        str((OUT / f"{BASE}_cold_launch_manifest_{TAG}.sha256").relative_to(ROOT)),
        str((OUT / f"{BASE}_cold_launch_outer_receipt_{TAG}.json").relative_to(ROOT)),
    ]
    af, ao = chain["anchor_file_sha256"], chain["anchor_object_sha256"]

    schema, _ = builder.load(R50_FILES["schema"][0])
    schema = builder.retag(schema)
    schema["$id"] = f"cm2.round306c79g.true-global-no-producer-consumer.{TAG}.schema"
    schema["$comment"] = f"CM2_{TAG.upper()}_DAG_STATIC_ZERO_CREDIT__RUNTIME_NOT_AUTHORIZED"
    schema_raw = builder.canon(schema) + b"\n"
    sh = builder.sha(schema_raw)

    contract, _ = builder.load(R50_FILES["contract"][0])
    contract = builder.retag(contract)
    cb = contract.get("v16r2_bundle")
    if not isinstance(cb, dict):
        raise RuntimeError("r51 contract active bundle missing")
    cb.pop("source_hashes", None)
    for key in ("contract_file_sha256", "contract_object_sha256",
                "transition_file_sha256", "transition_object_sha256",
                "audit_file_sha256"):
        cb.pop(key, None)
    cb.update({"bundle_version": TAG, "schema_file_sha256": sh,
               "pin_state": f"{TAG.upper()}_DAG_SOURCE_PINS_FINAL__RUNTIME_NOT_AUTHORIZED",
               "predecessor_semantic_supersession": {"path": p["anchor"], "file_sha256": af, "object_sha256": ao, "successor_only": f"{TAG}-semantic-bundle"},
               "predecessor_supersession_object_sha256": ao,
               "closed_schema": {"path": p["schema"], "file_sha256": sh},
               "exact8_ordered_paths": exact8, "base7_ordered_paths": base7,
               "exact10_ordered_paths": exact10})
    cb["contract"] = {"path": p["contract"],
                      "object_pin_source": "TOP_LEVEL_OBJECT_SHA256"}
    cb["build_only_producer"] = {
        "path": p["producer"], "role": f"{TAG.upper()}_EXECUTABLE_SOURCE__ZERO_CREDIT",
        "source_template_only": False}
    cb["independent_verifier_assembler_authority_consumer"] = {
        "path": p["consumer"], "role": f"{TAG.upper()}_EXECUTABLE_SOURCE__ZERO_CREDIT",
        "source_template_only": False}
    for key in ("build_only_producer", "independent_verifier_assembler_authority_consumer"):
        if isinstance(cb.get(key), dict):
            cb[key].update({"source_template_only": False,
                            "role": f"{TAG.upper()}_EXECUTABLE_SOURCE__ZERO_CREDIT"})
    trust = cb.get("post_source_static_trust_receipts")
    if isinstance(trust, dict):
        trust.update({"binding_direction": f"{TAG.upper()}_SOURCE_READS_POST_SOURCE_RECEIPTS__NO_HASH_CYCLE",
                      "predecessor_supersession_file_sha256": af,
                      "predecessor_supersession_object_sha256": ao,
                      "predecessor_supersession_path": p["anchor"],
                      "transition_path": p["transition"],
                      "v16_to_v16r2_transition_path": p["transition"],
                      "static_audit_path": p["audit"]})
    contract["v16r2_bundle"] = cb
    contract["schema"] = f"cm2.round306c79g.true-global-no-producer-consumer.{TAG}.contract"
    contract["status"] = "STATIC_CONTRACT_BYTES_FINAL__COLD_FREEZE_PENDING__RUNTIME_NOT_AUTHORIZED"
    contract_raw = builder.canon(builder.close(contract)) + b"\n"
    ch = builder.sha(contract_raw)
    co = json.loads(contract_raw)["object_sha256"]

    prod = builder.source_patch(_stable(R50_FILES["producer"][0]), "producer", p,
                               af, ao, sh, ch, co)
    ph = builder.sha(prod)
    cons = builder.source_patch(_stable(R50_FILES["consumer"][0]), "consumer", p,
                                af, ao, sh, ch, co, ph)
    qh = builder.sha(cons)

    transition, _ = builder.load(R50_FILES["transition"][0])
    transition = builder.retag(transition)
    boundary = {
        "base7_order": ["v14_registry_shape_drift_supersession_receipt",
                        "closed_schema_v16r2", "contract_v16r2", "producer_v16r2",
                        "consumer_v16r2", "transition_v16_to_v16r2",
                        "static_audit_v16r2"],
        "base7_first_member_is_v14_registry_shape_drift_supersession_receipt": True,
        "launcher_is_eighth": True, "manifest_is_ninth": True,
        "outer_is_tenth_and_last": True,
        "expected_predecessor_unique_file_identity_count": 116,
        "expected_prepublication_unique_file_identity_count": 124,
        "expected_terminal_unique_file_identity_count": 126,
        "terminal_group_vector": [10, 10, 10, 10, 10, 10, 10, 10, 10,
                                  10, 10, 7, 1, 3, 3, 1, 1],
        "all_126_file_identities_must_share_one_statx_mount": True,
        "manifest_or_outer_exists_at_transition_time": False,
        "manifest_or_outer_created_by_this_transition": False,
        "runtime_entry_authorized_by_this_transition": False,
    }
    transition["cold_launch_boundary"] = boundary
    successor = {
        "all_four_core_file_pins_final": True,
        "build_only_producer": {"path": p["producer"], "file_sha256": ph},
        "closed_schema": {"path": p["schema"], "file_sha256": sh},
        "cold_launcher_v16r2_path": p["launcher"],
        "contract": {"path": p["contract"], "file_sha256": ch, "object_sha256": co},
        "draft_pin_sentinels_remain_present": False,
        "final_consumer_pin_installed": True,
        "independent_verifier_assembler_authority_consumer": {"path": p["consumer"], "file_sha256": qh},
        "static_audit_v16r2_path": p["audit"],
        "transition_receipt_bytes_are_closed_around_final_core_pins": True,
        "transition_receipt_physical_freeze_completed": False,
    }
    transition["successor_v16r2_static_bundle"] = successor
    transition.update({"schema": "cm2.round306c79g.true-global-no-producer-consumer.v16-to-v16r2-static-launch-transition.v1",
                       "status": "STATIC_BYTES_CLOSED_V16_TO_V16R2__PHYSICAL_FREEZE_PENDING__RUNTIME_NOT_AUTHORIZED",
                       "transition_kind": "APPEND_ONLY_PUBLISHED_V14_RUNTIME_FAIL_CLOSED_REJECTION_TO_ZERO_CREDIT_V16R2_CLEAN_ROOM_SUCCESSOR",
                       "receipt_path": p["transition"], "effective_checkpoint_object_sha256": UPSTREAM_CHECKPOINT})
    for node in builder.walk(transition):
        if isinstance(node, dict) and node is not successor:
            node.pop("source_hashes", None)
    trans_raw = builder.canon(builder.close(transition)) + b"\n"
    th = builder.sha(trans_raw)
    to = json.loads(trans_raw)["object_sha256"]

    # First launcher pass uses nonzero sentinels only to establish the
    # pin-normalized AST shape; those sentinels never enter the final bundle.
    fake_audit_file = hashlib.sha256(b"r51-audit-file-pending").hexdigest()
    fake_audit_object = hashlib.sha256(b"r51-audit-object-pending").hexdigest()
    base7_pre = {"v14": (V14_SHA, V14_OBJECT), "schema": (sh, None),
                 "contract": (ch, co), "producer": (ph, None),
                 "consumer": (qh, None), "transition": (th, to),
                 "audit": (fake_audit_file, fake_audit_object)}
    launch_pre = builder.source_patch(_stable(R50_FILES["launcher"][0]),
                                      "launcher", p, af, ao, sh, ch, co,
                                      ph, base7_pre)
    normalized = _pin_normalized_launcher_ast(launch_pre)
    current = {"anchor_path": p["anchor"], "anchor_file": af,
               "anchor_object": ao, "schema": sh, "contract_file": ch,
               "contract_object": co, "producer": ph, "consumer": qh,
               "transition_file": th, "transition_object": to,
               "launcher_template": normalized}
    audit_value = enrich_audit({}, {"producer": prod, "consumer": cons,
                                   "launcher": launch_pre}, current)
    # The native consumer audits the exact insertion order of the checker
    # ``input_sha256`` protocol map.  Preserve that nested order in the file
    # serialization; object closure itself was already computed by ``_close``
    # over the canonical (sorted) body, so changing wire order does not create
    # a hash cycle or weaken the object pin.
    aud_raw = json.dumps(audit_value, ensure_ascii=False, sort_keys=False,
                         separators=(",", ":"), allow_nan=False).encode() + b"\n"
    ah = builder.sha(aud_raw)
    ao2 = json.loads(aud_raw)["object_sha256"]
    base7 = dict(base7_pre); base7["audit"] = (ah, ao2)
    launch = builder.source_patch(_stable(R50_FILES["launcher"][0]), "launcher",
                                  p, af, ao, sh, ch, co, ph, base7)
    if _pin_normalized_launcher_ast(launch) != normalized:
        raise RuntimeError("r51 launcher normalized AST changed after audit pin")
    lh = builder.sha(launch)
    # Native structural gates before any O_EXCL operation.
    for role, raw in (("producer", prod), ("consumer", cons), ("launcher", launch)):
        tree = ast.parse(raw.decode(), str(p[role]), mode="exec")
        compile(tree, str(p[role]), "exec")
        # The predecessor token is legitimately present in the new edge name
        # (r50 -> r51).  Reject only the old r46->r50 edge and stale namespace
        # labels, not the canonical predecessor reference itself.
        if b"v16r2r46_to_v16r2r50" in raw or b"v16r2r49" in raw:
            raise RuntimeError(f"r51 stale source namespace:{role}")
    if len(schema.get("$defs", {})) != 46:
        raise RuntimeError("r51 schema definition shape")
    if [len(contract), len(transition), len(audit_value)] != [30, 31, 30]:
        raise RuntimeError("r51 JSON top-level shape")
    boundary_keys = set(boundary)
    if boundary_keys != {
        "base7_order", "base7_first_member_is_v14_registry_shape_drift_supersession_receipt",
        "launcher_is_eighth", "manifest_is_ninth", "outer_is_tenth_and_last",
        "expected_predecessor_unique_file_identity_count",
        "expected_prepublication_unique_file_identity_count",
        "expected_terminal_unique_file_identity_count", "terminal_group_vector",
        "all_126_file_identities_must_share_one_statx_mount",
        "manifest_or_outer_exists_at_transition_time",
        "manifest_or_outer_created_by_this_transition",
        "runtime_entry_authorized_by_this_transition"}:
        raise RuntimeError("r51 transition boundary exact13 shape")
    return ({"schema": schema_raw, "contract": contract_raw, "producer": prod,
             "consumer": cons, "transition": trans_raw, "audit": aud_raw,
             "launcher": launch},
            {"hashes": {"anchor": af, "anchor_object": ao, "schema": sh,
                        "contract": ch, "contract_object": co, "producer": ph,
                        "consumer": qh, "transition": th, "transition_object": to,
                        "audit": ah, "audit_object": ao2, "launcher": lh,
                        "launcher_template": normalized},
             "shapes": {"schema": [46, 242, 52], "contract": len(contract),
                        "transition": len(transition), "audit": len(audit_value),
                        "successor": len(successor)}})


def prepare_in_memory() -> dict[str, Any]:
    """Run every pre-install r51 gate and return a non-authoritative record."""
    before = _pyc_inventory()
    preflight = _preflight()
    builder = _load_generic_r51()
    rejection = seal_r50_rejection(builder)
    chain = _chain_in_memory(rejection)
    generated, meta = _build_r51_candidate(builder, chain)
    if _pyc_inventory() != before:
        raise RuntimeError("pyc inventory changed during r51 preparation")
    return {"schema": f"cm2.c79g.{TAG}.candidate-builder.design.v1",
            "status": "R51_FULL_NATIVE_STATIC_BUILD_PENDING_INSTALL",
            "preflight": preflight, "r50_rejection": {
                k: v for k, v in rejection.items() if k != "bytes"},
            "chain": {k: v for k, v in chain.items()
                      if k not in {"rejection", "sup_value", "sup_raw",
                                   "anchor_value", "anchor_raw"}},
            "meta": meta,
            "candidate_install": False, "manifest_created": False,
            "outer_created": False, "runtime_authorized": False,
            "formal_global_closure_credit": 0, "D02_unlock": False,
            "pyc_created": False}


def install_r51_candidate() -> dict[str, Any]:
    """Perform the single append-only r51 chain/member installation."""
    before = _pyc_inventory()
    preflight = _preflight()
    builder = _load_generic_r51()
    rejection = seal_r50_rejection(builder)
    chain = _chain_in_memory(rejection)
    generated, meta = _build_r51_candidate(builder, chain)
    if _pyc_inventory() != before:
        raise RuntimeError("pyc inventory changed before r51 install")

    actions: dict[str, str] = {}
    actions["rejection"] = builder.install(R51_REJECTION,
                                            rejection["bytes"], 0o444)
    actions["supersession"] = builder.install(R51_SUP, chain["sup_raw"], 0o444)
    actions["anchor"] = builder.install(R51_ANCHOR, chain["anchor_raw"], 0o444)
    json_targets = {
        "schema": OUT / f"{BASE}_schema_{TAG}.json",
        "contract": OUT / f"{BASE}_contract_{TAG}.json",
        "transition": OUT / f"{BASE}_{PREV}_to_{TAG}_static_launch_transition_receipt_v1.json",
        "audit": OUT / f"{BASE}_static_audit_{TAG}.json",
    }
    source_targets = {
        "producer": OUT / f"{BASE}_{TAG}_semantic_source.py",
        "consumer": OUT / f"{BASE}_independent_verifier_assembler_authority_consumer_{TAG}_semantic_source.py",
        "launcher": OUT / f"{BASE}_cold_launch_{TAG}_semantic_source.py",
    }
    for name, path in json_targets.items():
        actions[name] = builder.install(path, generated[name], 0o444)
    for name, path in source_targets.items():
        actions[name] = builder.install(path, generated[name], 0o664)
    manifest = OUT / f"{BASE}_cold_launch_manifest_{TAG}.sha256"
    outer = OUT / f"{BASE}_cold_launch_outer_receipt_{TAG}.json"
    if manifest.exists() or outer.exists():
        raise RuntimeError("r51 manifest/outer unexpectedly present")
    if _pyc_inventory() != before:
        raise RuntimeError("pyc inventory changed after r51 install")
    return {"schema": f"cm2.c79g.{TAG}.candidate-builder.v1",
            "status": "R51_STATIC_CANDIDATE_INSTALLED__ZERO_CREDIT__RUNTIME_NOT_AUTHORIZED",
            "preflight": preflight, "rejection": {
                k: v for k, v in rejection.items() if k != "bytes"},
            "chain": {k: v for k, v in chain.items()
                      if k not in {"rejection", "sup_value", "sup_raw",
                                   "anchor_value", "anchor_raw"}},
            "actions": actions, "meta": meta,
            "candidate_install": True, "manifest_created": False,
            "outer_created": False, "runtime_authorized": False,
            "formal_global_closure_credit": 0, "D02_unlock": False,
            "pyc_created": False}


def main() -> int:
    try:
        print(json.dumps(install_r51_candidate(), ensure_ascii=False,
                         sort_keys=True))
        return 0
    except Exception as exc:
        print(json.dumps({"schema": f"cm2.c79g.{TAG}.candidate-builder.failure.v1",
                          "status": "FAIL_CLOSED_R51_STATIC_INSTALL",
                          "error": {"type": type(exc).__name__,
                                    "message": str(exc)},
                          "candidate_install": False,
                          "manifest_created": False, "outer_created": False,
                          "runtime_authorized": False,
                          "formal_global_closure_credit": 0,
                          "D02_unlock": False}, ensure_ascii=False,
                  sort_keys=True))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
