#!/usr/bin/env python3
"""r54 clean-room successor builder.

r53 is retained as an immutable rejection witness: its launcher has two live
``configure_workspace_paths`` assignments which overwrite the current active
anchor pins with the r50 pair.  This builder uses the reviewed r51 constructor
only in memory, retags the immutable r53 seven-piece bundle, and rewrites all
active-pin assignments (including function-body assignments) before doing one
O_EXCL installation.  It never edits or reuses an r53 output and never grants
runtime credit.
"""
from __future__ import annotations

import ast
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
PREV = "v16r2r53"
TAG = "v16r2r54"
UPSTREAM = "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab"
SUCCESSOR = "dd9d64f3f0bd0dfd00fd399e3154517a34ba19cfb601ec749f44cbc08b03ca1b"

CONSTRUCTOR = ROOT / "scripts/c79g_v16r2r51_candidate_builder.py"
CONSTRUCTOR_SHA = "084de3f79f9f13c9270799a1ba6570bb820447405b3e1300c6d0b2aa18e3d11c"
CONSTRUCTOR_SIZE = 65641

V14 = OUT / f"{BASE}_v14_runtime_registry_shape_drift_rejection_supersession_receipt_v1.json"
V14_SHA = "aa4323027e2313f8a2eda0d6ffc039a537afe342d496d1f75cd73fcd47446c01"
V14_OBJECT = "93689e62ae36f405f045a769f4dc6f6e6fd83a16605d08299d5c3397ad657e2e"

R53_ANCHOR = OUT / f"{BASE}_v16r2r53_active_predecessor_supersession_receipt_v1.json"
R53_ANCHOR_SHA = "0bbc5567be93ea3eb4b107c2e5bc5faf6ff7ad622d1a406fb5faa6f51b0a5b8e"
R53_ANCHOR_OBJECT = "48a3098ce2c4dc59986dbb098bcfd02d52ba666325762b7c3869e37bcc7aa10d"
R53_FILES: dict[str, tuple[Path, str, str | None]] = {
    "schema": (OUT / f"{BASE}_schema_v16r2r53.json",
               "c5bc64c5620fd95ff80cad45a880b98ec0f12c73f6c204e78c6b3b6f684e0aa7", None),
    "contract": (OUT / f"{BASE}_contract_v16r2r53.json",
                 "88721d80ae048ee4c617ef2dea056191027c8bc49551f9c735ce1c348cee753b",
                 "3b9ec48bfbb5d4bd0329d815c3e02bfbdf1f47e341f3f2568310c2c7914e846a"),
    "producer": (OUT / f"{BASE}_v16r2r53_semantic_source.py",
                 "8af23fb4ac54c81f8a2c8699385b469a4436a0de913d735fa5b6ede2bcfcf8d7", None),
    "consumer": (OUT / f"{BASE}_independent_verifier_assembler_authority_consumer_v16r2r53_semantic_source.py",
                 "e5d9b7760b13fffeb3c78984e521182785419dbcaa6235351df7e2de768a29db", None),
    "transition": (OUT / f"{BASE}_v16r2r52_to_v16r2r53_static_launch_transition_receipt_v1.json",
                   "da6f49b2bd9f26003e420a2d2b46eb338aa3007450e94f7934ace471e89aa666",
                   "86a53e96a6b5c6789a1dc9ab32b96a03b7e0e7cd438845c86b47c4848749b0a0"),
    "audit": (OUT / f"{BASE}_static_audit_v16r2r53.json",
              "99e70fd8033ee6e24706c6056093ee33f55b27161d6f6ff0287596fc4fb2fdb8",
              "0cf889ca81a7d770cc57659cbf42e8648081ffa8be0179d0c2a96a878be5c51a"),
    "launcher": (OUT / f"{BASE}_cold_launch_v16r2r53_semantic_source.py",
                 "411285c84fdf655e6561cb0ff5c57ced3d2e0b2ae3620e0eb2b71368f843b9ae", None),
}

REJECTION = OUT / f"{BASE}_{PREV}_static_bundle_rejection_receipt_v1.json"
SUPERSESSION = OUT / f"{BASE}_{PREV}_to_{TAG}_static_bundle_rejection_supersession_receipt_v1.json"
ANCHOR = OUT / f"{BASE}_{TAG}_active_predecessor_supersession_receipt_v1.json"
TARGETS = [
    REJECTION, SUPERSESSION, ANCHOR,
    OUT / f"{BASE}_{TAG}_semantic_source.py",
    OUT / f"{BASE}_independent_verifier_assembler_authority_consumer_{TAG}_semantic_source.py",
    OUT / f"{BASE}_cold_launch_{TAG}_semantic_source.py",
    OUT / f"{BASE}_schema_{TAG}.json", OUT / f"{BASE}_contract_{TAG}.json",
    OUT / f"{BASE}_{PREV}_to_{TAG}_static_launch_transition_receipt_v1.json",
    OUT / f"{BASE}_static_audit_{TAG}.json",
    OUT / f"{BASE}_cold_launch_manifest_{TAG}.sha256",
    OUT / f"{BASE}_cold_launch_outer_receipt_{TAG}.json",
]


def stable(path: Path, expected: str | None = None,
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
            part = os.read(fd, 1 << 20)
            if not part:
                break
            chunks.append(part)
        after = os.fstat(fd)
        raw = b"".join(chunks)
        if ((before.st_dev, before.st_ino, before.st_size) !=
                (after.st_dev, after.st_ino, len(raw))):
            raise RuntimeError(f"witness changed:{path}")
        if size is not None and len(raw) != size:
            raise RuntimeError(f"witness size:{path}")
        if expected is not None and hashlib.sha256(raw).hexdigest() != expected:
            raise RuntimeError(f"witness hash:{path}")
        return raw
    finally:
        os.close(fd)


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canon(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"), allow_nan=False).encode()


def close(value: dict[str, Any]) -> dict[str, Any]:
    body = dict(value)
    body.pop("object_sha256", None)
    body["object_sha256"] = sha(canon(body))
    return body


def pyc_inventory() -> dict[str, str]:
    out: dict[str, str] = {}
    for path in ROOT.rglob("*.pyc"):
        if path.is_file() and not path.is_symlink():
            raw = stable(path)
            out[str(path.relative_to(ROOT))] = sha(raw)
    return out


def load_constructor() -> dict[str, Any]:
    raw = stable(CONSTRUCTOR, CONSTRUCTOR_SHA, CONSTRUCTOR_SIZE)
    tree = ast.parse(raw.decode(), str(CONSTRUCTOR), mode="exec")
    compile(tree, str(CONSTRUCTOR), "exec")
    ns: dict[str, Any] = {"__name__": "_r54_constructor",
                          "__file__": str(CONSTRUCTOR), "__package__": None}
    exec(compile(tree, str(CONSTRUCTOR), "exec"), ns, ns)
    return ns


def replace_hex_top(text: str, name: str, value: str) -> str:
    pattern = rf"(?m)^({re.escape(name)}\s*=\s*)(['\"])[0-9a-f]{{64}}\2\s*$"
    out, count = re.subn(pattern, rf'\1"{value}"', text)
    if count != 1:
        raise RuntimeError(f"r54 top-level pin {name}:{count}")
    return out


def source_patch(raw: bytes, role: str, paths: dict[str, str],
                 anchor_file: str, anchor_object: str, schema_hash: str,
                 contract_hash: str, contract_object: str,
                 producer_hash: str | None = None,
                 base7: dict[str, tuple[str, str | None]] | None = None) -> bytes:
    text = raw.decode("utf-8")
    old_edge = f"{BASE}_v16r2r52_to_v16r2r53_"
    text = text.replace(old_edge, "__R54_EDGE__")
    text = text.replace("v16r2r53", TAG).replace("V16R2R53", "V16R2R54")
    text = text.replace("__R54_EDGE__", f"{BASE}_{PREV}_to_{TAG}_")
    if role != "launcher":
        text = replace_hex_top(text, "ACTIVE_PREDECESSOR_SUPERSESSION_FILE_PIN", anchor_file)
        text = replace_hex_top(text, "ACTIVE_PREDECESSOR_SUPERSESSION_OBJECT_PIN", anchor_object)
        text = replace_hex_top(text, "CONTRACT_FILE_PIN", contract_hash)
        text = replace_hex_top(text, "CONTRACT_OBJECT_PIN", contract_object)
        text = replace_hex_top(text, "CLOSED_SCHEMA_FILE_PIN", schema_hash)
        if role == "consumer" and producer_hash is not None:
            text = replace_hex_top(text, "PRODUCER_SOURCE_PIN", producer_hash)
    else:
        if base7 is None:
            raise RuntimeError("r54 launcher BASE7 missing")
        tree = ast.parse(text, "r54_launcher", mode="exec")
        pin_counts = {"file": 0, "object": 0}
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                targets = node.targets
            elif isinstance(node, ast.AnnAssign):
                targets = [node.target]
            else:
                continue
            for target in targets:
                if not isinstance(target, ast.Name):
                    continue
                if target.id == "ACTIVE_PREDECESSOR_SUPERSESSION_FILE_PIN":
                    node.value = ast.Constant(anchor_file)
                    pin_counts["file"] += 1
                elif target.id == "ACTIVE_PREDECESSOR_SUPERSESSION_OBJECT_PIN":
                    node.value = ast.Constant(anchor_object)
                    pin_counts["object"] += 1
                elif target.id == "FINAL_BASE7_PINS_INSTALLED":
                    node.value = ast.Constant(True)
        if pin_counts != {"file": 2, "object": 2}:
            raise RuntimeError(f"r54 launcher active-pin assignment census:{pin_counts}")
        funcs = [n for n in tree.body if isinstance(n, ast.FunctionDef) and
                 n.name == "configure_workspace_paths"]
        assigns = ([n for n in funcs[0].body if isinstance(n, ast.Assign) and
                    len(n.targets) == 1 and isinstance(n.targets[0], ast.Name) and
                    n.targets[0].id == "BASE7_PINS"]
                   if len(funcs) == 1 else [])
        if len(assigns) != 1:
            raise RuntimeError("r54 launcher BASE7 assignment")
        pins = dict(base7)
        pins.setdefault("v14", (V14_SHA, V14_OBJECT))
        order = [("V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT", "v14"),
                 ("SCHEMA", "schema"), ("CONTRACT", "contract"),
                 ("PRODUCER", "producer"), ("CONSUMER", "consumer"),
                 ("TRANSITION", "transition"), ("AUDIT", "audit")]
        assigns[0].value = ast.Dict(
            keys=[ast.Name(id=name, ctx=ast.Load()) for name, _ in order],
            values=[ast.Tuple([ast.Constant(pins[key][0]),
                               ast.Constant(pins[key][1])], ast.Load())
                    for _, key in order])
        text = ast.unparse(tree) + "\n"
    edge = f"{BASE}_{PREV}_to_{TAG}_static_launch_transition_receipt_v1.json"
    if edge not in text:
        raise RuntimeError(f"{role}: r54 edge absent")
    return text.encode()


def configure(ns: dict[str, Any]) -> Any:
    """Configure the current generic constructor for r53 -> r54."""
    ns.update({
        "ROOT": ROOT, "OUT": OUT, "BASE": BASE, "PREV": PREV, "TAG": TAG,
        "R50_ANCHOR": R53_ANCHOR, "R50_ANCHOR_SHA": R53_ANCHOR_SHA,
        "R50_ANCHOR_OBJECT": R53_ANCHOR_OBJECT, "R50_FILES": R53_FILES,
        "R50_REJECTION": REJECTION, "R51_REJECTION": REJECTION,
        "R51_SUP": SUPERSESSION, "R51_ANCHOR": ANCHOR,
        "R51_TARGETS": TARGETS, "V14": V14, "V14_SHA": V14_SHA,
        "V14_OBJECT": V14_OBJECT, "UPSTREAM_CHECKPOINT": UPSTREAM,
        "SUCCESSOR_CHECKPOINT": SUCCESSOR,
    })
    ns["_direct_source_patch_r50"] = source_patch
    old_canon = ns["_canonicalize_registry_helper"]

    def canonicalize(text: str) -> str:
        try:
            return old_canon(text)
        except RuntimeError as exc:
            if "literal" in str(exc) or "patch incomplete" in str(exc):
                return text
            raise

    ns["_canonicalize_registry_helper"] = canonicalize
    old_cross = ns["_patch_launcher_validator_cross_role"]

    def cross(text: str) -> str:
        if ("consumer_frozen_predecessor_incident_exact5_bytes_read_only_noncredit_allowed"
                not in text and
                "pin_normalization_preserves_v12_rejection_and_all_historical_pins"
                not in text and "actual_runtime_registry_shape_evidence" in text and
                "published_then_officially_rejected_predecessor_v14" in text):
            return text
        return old_cross(text)

    ns["_patch_launcher_validator_cross_role"] = cross
    builder = ns["_load_generic_r51"]()

    def patched(raw: bytes, role: str, paths: dict[str, str], af: str, ao: str,
                sh: str, ch: str, co: str, producer_hash: str | None = None,
                base7: dict[str, tuple[str, str | None]] | None = None) -> bytes:
        out = source_patch(raw, role, paths, af, ao, sh, ch, co,
                           producer_hash, base7)
        text = out.decode("utf-8")
        if role == "launcher":
            text = canonicalize(text)
            text = cross(text)
        tree = ast.parse(text, str(paths.get(role, role)), mode="exec")
        compile(tree, str(paths.get(role, role)), "exec")
        return (text if text.endswith("\n") else text + "\n").encode()

    builder.source_patch = patched
    builder.TAG = TAG
    builder.PREV = PREV
    builder.UPSTREAM = UPSTREAM
    builder.CHECKPOINT = UPSTREAM
    builder.ANCHOR_IN = R53_ANCHOR
    builder.SRC_IN = {key: R53_FILES[key][0] for key in ("producer", "consumer", "launcher")}
    builder.JSON_IN = {key: R53_FILES[key][0] for key in ("schema", "contract", "transition", "audit")}
    return builder


def make_chain(ns: dict[str, Any]) -> dict[str, Any]:
    rejection_value = close({
        "schema": f"cm2.c79g.{PREV}.static-bundle-rejection.v1",
        "status": "PERMANENT_FAIL_CLOSED_R53_CURRENT_PATH_PIN_SPLIT_AND_REVIEWER_INCOMPATIBILITY__ZERO_CREDIT",
        "failed_namespace": PREV, "predecessor_namespace": "v16r2r52",
        "rejection_reason": "LAUNCHER_CONFIGURE_ACTIVE_PREDECESSOR_PINS_RETAINED_R50_AND_GENERIC_REVIEWER_IS_NOT_ROLE_AWARE",
        "failure_vector": {
            "launcher_module_active_predecessor_file_pin": R53_ANCHOR_SHA,
            "launcher_module_active_predecessor_object_pin": R53_ANCHOR_OBJECT,
            "launcher_configure_stale_file_pin": "f7f94d8de8918de7e28d1bf45b890646f5feca8adb36bf0ed2b90c717cab0fc2",
            "launcher_configure_stale_object_pin": "89cd68d3221999496144eb30347e20b3da64f392d7d4a3ce9bc3cfbd1cfe92e8",
            "independent_reviewer_failure_object_sha256": "45fc8ec19f4cc6345b20ea9637819297ea7649ed18cf029875577261ef824a64",
            "candidate_bytes_remain_immutable": True,
        },
        "candidate_install": True, "runtime_protocol_executed": False,
        "manifest_created": False, "outer_created": False,
        "runtime_authorized": False, "formal_global_closure_credit": 0,
        "D02_unlock": False, "append_only": True,
        "overwrite_delete_or_reuse_allowed": False,
        "candidate_schema_file_sha256": R53_FILES["schema"][1],
        "candidate_contract_file_sha256": R53_FILES["contract"][1],
        "candidate_contract_object_sha256": R53_FILES["contract"][2],
        "candidate_audit_file_sha256": R53_FILES["audit"][1],
        "candidate_audit_object_sha256": R53_FILES["audit"][2],
        "candidate_launcher_file_sha256": R53_FILES["launcher"][1],
    })
    rejection_raw = canon(rejection_value) + b"\n"
    rejection = {"path": str(REJECTION.relative_to(ROOT)),
                 "file_sha256": sha(rejection_raw),
                 "object_sha256": rejection_value["object_sha256"],
                 "bytes": rejection_raw}
    sup_value = close({
        "schema": f"cm2.c79g.{PREV}-to-{TAG}.static-bundle-rejection-supersession.v1",
        "status": "FROZEN_APPEND_ONLY_REJECTED_PREDECESSOR_SUPERSEDED__ZERO_CREDIT",
        "predecessor_namespace": PREV, "successor_namespace": TAG,
        "predecessor_active_anchor_path": str(R53_ANCHOR.relative_to(ROOT)),
        "predecessor_active_anchor_file_sha256": R53_ANCHOR_SHA,
        "predecessor_active_anchor_object_sha256": R53_ANCHOR_OBJECT,
        "predecessor_rejection_path": rejection["path"],
        "predecessor_rejection_file_sha256": rejection["file_sha256"],
        "predecessor_rejection_object_sha256": rejection["object_sha256"],
        "upstream_checkpoint_object_sha256": UPSTREAM,
        "successor_checkpoint_object_sha256": SUCCESSOR,
        "append_only": True, "runtime_authorized": False,
        "formal_global_closure_credit": 0, "D02_unlock": False,
    })
    sup_raw = canon(sup_value) + b"\n"
    anchor_value = close({
        "schema": f"cm2.c79g.{TAG}.active-predecessor-supersession.v1",
        "status": "FROZEN_APPEND_ONLY_ACTIVE_PREDECESSOR_ANCHOR__ZERO_CREDIT",
        "predecessor_namespace": PREV,
        "predecessor_supersession_path": str(SUPERSESSION.relative_to(ROOT)),
        "predecessor_supersession_file_sha256": sha(sup_raw),
        "predecessor_supersession_object_sha256": sup_value["object_sha256"],
        "upstream_checkpoint_object_sha256": UPSTREAM,
        "successor_checkpoint_object_sha256": SUCCESSOR,
        "successor_namespace": f"{TAG}_semantic_source",
        "append_only": True, "runtime_authorized": False,
        "formal_global_closure_credit": 0, "D02_unlock": False,
        "manifest_created": False, "outer_created": False,
    })
    anchor_raw = canon(anchor_value) + b"\n"
    return {"rejection": rejection, "sup_value": sup_value,
            "sup_raw": sup_raw, "anchor_value": anchor_value,
            "anchor_raw": anchor_raw, "sup_file_sha256": sha(sup_raw),
            "anchor_file_sha256": sha(anchor_raw),
            "anchor_object_sha256": anchor_value["object_sha256"]}


def validate_generated(generated: dict[str, bytes], meta: dict[str, Any],
                       chain: dict[str, Any]) -> None:
    for role in ("producer", "consumer", "launcher"):
        tree = ast.parse(generated[role].decode(), role, mode="exec")
        compile(tree, role, "exec")
    launcher_tree = ast.parse(generated["launcher"].decode(), "r54_launcher", mode="exec")
    file_values: list[str] = []
    object_values: list[str] = []
    for node in ast.walk(launcher_tree):
        if isinstance(node, ast.Assign):
            targets = node.targets
        elif isinstance(node, ast.AnnAssign):
            targets = [node.target]
        else:
            continue
        for target in targets:
            if not isinstance(target, ast.Name):
                continue
            if target.id == "ACTIVE_PREDECESSOR_SUPERSESSION_FILE_PIN":
                if not isinstance(node.value, ast.Constant):
                    raise RuntimeError("r54 active file pin is not literal")
                file_values.append(node.value.value)
            elif target.id == "ACTIVE_PREDECESSOR_SUPERSESSION_OBJECT_PIN":
                if not isinstance(node.value, ast.Constant):
                    raise RuntimeError("r54 active object pin is not literal")
                object_values.append(node.value.value)
    if len(file_values) != 2 or set(file_values) != {chain["anchor_file_sha256"]}:
        raise RuntimeError(f"r54 launcher file-pin split:{file_values}")
    if len(object_values) != 2 or set(object_values) != {chain["anchor_object_sha256"]}:
        raise RuntimeError(f"r54 launcher object-pin split:{object_values}")
    for role in ("producer", "consumer"):
        raw = generated[role]
        if b"v16r2r52_to_v16r2r53_static_launch_transition_receipt_v1.json" in raw:
            raise RuntimeError(f"{role}: stale active edge")
    schema = json.loads(generated["schema"])
    contract = json.loads(generated["contract"])
    transition = json.loads(generated["transition"])
    audit = json.loads(generated["audit"])
    if sha(canon({k: v for k, v in contract.items() if k != "object_sha256"})) != contract["object_sha256"]:
        raise RuntimeError("r54 contract closure")
    if sha(canon({k: v for k, v in transition.items() if k != "object_sha256"})) != transition["object_sha256"]:
        raise RuntimeError("r54 transition closure")
    if sha(canon({k: v for k, v in audit.items() if k != "object_sha256"})) != audit["object_sha256"]:
        raise RuntimeError("r54 audit closure")
    if len(schema.get("$defs", {})) != 46 or len(contract) != 30 or len(transition) != 31 or len(audit) != 30:
        raise RuntimeError("r54 JSON shape")
    bundle = contract.get("v16r2_bundle", {})
    if bundle.get("bundle_version") != TAG or bundle.get("formal_global_closure_credit") != 0 or bundle.get("D02_unlock") is not False:
        raise RuntimeError("r54 contract state")
    succ = transition.get("successor_v16r2_static_bundle", {})
    if succ.get("transition_receipt_physical_freeze_completed") is not False:
        raise RuntimeError("r54 transition prematurely frozen")
    if meta["hashes"]["audit"] != sha(generated["audit"]):
        raise RuntimeError("r54 audit hash metadata")


def build_in_memory() -> tuple[dict[str, Any], dict[str, bytes], dict[str, Any], dict[str, Any]]:
    before = pyc_inventory()
    if not (sys.flags.isolated and sys.flags.no_site and sys.flags.dont_write_bytecode):
        raise RuntimeError("r54 requires isolated no-bytecode interpreter")
    stable(CONSTRUCTOR, CONSTRUCTOR_SHA, CONSTRUCTOR_SIZE)
    stable(R53_ANCHOR, R53_ANCHOR_SHA)
    for path, file_sha, _ in R53_FILES.values():
        stable(path, file_sha)
    occupied = [str(path.relative_to(ROOT)) for path in TARGETS if path.exists()]
    if occupied:
        raise RuntimeError("r54 target already exists:" + ",".join(occupied))
    ns = load_constructor()
    builder = configure(ns)
    chain = make_chain(ns)
    generated, meta = ns["_build_r51_candidate"](builder, chain)
    validate_generated(generated, meta, chain)
    if pyc_inventory() != before:
        raise RuntimeError("r54 pyc inventory changed during build")
    preflight = {"constructor_sha256": CONSTRUCTOR_SHA,
                 "r53_anchor_file_sha256": R53_ANCHOR_SHA,
                 "r53_anchor_object_sha256": R53_ANCHOR_OBJECT,
                 "target_paths_absent": True, "pyc_inventory_count": len(before),
                 "runtime_authorized": False, "formal_global_closure_credit": 0,
                 "D02_unlock": False}
    return preflight, generated, meta, chain


def install() -> dict[str, Any]:
    preflight, generated, meta, chain = build_in_memory()
    # The constructor's install helper is the reviewed O_EXCL+fsync primitive.
    ns = load_constructor()
    builder = configure(ns)
    actions: dict[str, str] = {}
    actions["rejection"] = builder.install(REJECTION, chain["rejection"]["bytes"], 0o444)
    actions["supersession"] = builder.install(SUPERSESSION, chain["sup_raw"], 0o444)
    actions["anchor"] = builder.install(ANCHOR, chain["anchor_raw"], 0o444)
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
    for key, path in json_targets.items():
        actions[key] = builder.install(path, generated[key], 0o444)
    for key, path in source_targets.items():
        actions[key] = builder.install(path, generated[key], 0o664)
    if pyc_inventory() != pyc_inventory():
        raise RuntimeError("r54 internal pyc inventory read instability")
    return {"schema": f"cm2.c79g.{TAG}.candidate-builder.v1",
            "status": "R54_STATIC_CANDIDATE_INSTALLED__ZERO_CREDIT__RUNTIME_NOT_AUTHORIZED",
            "preflight": preflight, "actions": actions,
            "meta": meta, "chain": {k: v for k, v in chain.items() if k not in ("rejection", "sup_raw", "anchor_raw")},
            "candidate_install": True, "manifest_created": False,
            "outer_created": False, "runtime_authorized": False,
            "formal_global_closure_credit": 0, "D02_unlock": False,
            "pyc_created": False}


def main() -> int:
    try:
        print(json.dumps(install(), ensure_ascii=False, sort_keys=True))
        return 0
    except Exception as exc:
        print(json.dumps({"schema": f"cm2.c79g.{TAG}.candidate-builder.failure.v1",
                          "status": "FAIL_CLOSED_R54_STATIC_INSTALL",
                          "error": {"type": type(exc).__name__, "message": str(exc)},
                          "candidate_install": False, "manifest_created": False,
                          "outer_created": False, "runtime_authorized": False,
                          "formal_global_closure_credit": 0, "D02_unlock": False},
                         ensure_ascii=False, sort_keys=True))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
