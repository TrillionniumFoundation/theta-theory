#!/usr/bin/env python3
"""r58 append-only clean-room candidate builder.

The r57 seven-piece bundle is immutable.  This builder loads its reviewed
builder only as an in-memory recipe and fixes the remaining current-path
semantic defects before one O_EXCL installation:

* nine effective-checkpoint leaves were emitted as raw strings instead of
  closed schema nodes;
* the active contract still said that laterRejection had 54 keys although
  the closed schema and both executable constructors have 56;
* the transition and audit current bundles carried stale v15/v14 aliases;
* the launcher registry-shape diagnostics still identified the current
  producer as v15.

No manifest, outer receipt, runtime surface, authority, or credit is created.
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
PREV = "v16r2r57"
TAG = "v16r2r58"
INPUT_PREV = "v16r2r56"
INPUT_TAG = "v16r2r57"
UPSTREAM = "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab"
SUCCESSOR = "dd9d64f3f0bd0dfd00fd399e3154517a34ba19cfb601ec749f44cbc08b03ca1b"
GENERIC_SCHEMA = "cm2.round306c79g.true-global-no-producer-consumer.v16r2"

R57_BUILDER = ROOT / "scripts/c79g_v16r2r57_candidate_builder.py"
R57_ANCHOR = OUT / f"{BASE}_{PREV}_active_predecessor_supersession_receipt_v1.json"
R57_ANCHOR_SHA = "20e35762b74af1a9a52440323d11f51ad88e73dcffa8df558b6966dfe2f8b128"
R57_ANCHOR_OBJECT = "fcee1f563ae439872f6c0db6904e7f6eaac291892af56d4117ec333c0e3ce482"
R57_FILES: dict[str, tuple[Path, str, str | None]] = {
    "schema": (OUT / f"{BASE}_schema_{PREV}.json",
               "d58181505c940388e21b536a4e025de34562143363d27c36068230c225d725e3", None),
    "contract": (OUT / f"{BASE}_contract_{PREV}.json",
                 "d0aae106d0ceb729badf7689702975ca7c4797a318fd80701ef1cfe72df0f6fb",
                 "a257959b5b18cf9810c37b6815318fb6f23f1372ad411d0f6c24f172f8ce0b68"),
    "producer": (OUT / f"{BASE}_{PREV}_semantic_source.py",
                 "dc3cfb7cf3ac9c7db1b5da0cf0cfd920008afbcfea87b53a367d191c0a5b2286", None),
    "consumer": (OUT / f"{BASE}_independent_verifier_assembler_authority_consumer_{PREV}_semantic_source.py",
                 "758ac372464e23df4e1530ff799de07df8119868d0c3bc09babad394d5e646ed", None),
    "transition": (OUT / f"{BASE}_{INPUT_PREV}_to_{PREV}_static_launch_transition_receipt_v1.json",
                   "3f3ccdf7d79624bdf6a9acbf68783e78e4a5fc89ac83e021e7936327a6e94737",
                   "3a73e596af7fb4bd7139b7083e8e5a2542184be5effd9f2595b80d21903cedd2"),
    "audit": (OUT / f"{BASE}_static_audit_{PREV}.json",
              "9bb131ed87feedf1dd4c4bf612cabf56c5a02ee49041cb19384403bdf9674988",
              "ec9ea92338cf0048b642fc9b880e845302d31f6cf6f7e9192aeea737eaf294b7"),
    "launcher": (OUT / f"{BASE}_cold_launch_{PREV}_semantic_source.py",
                 "8aed541d97f8aabb4e9ce7a0fb69a469a302516a93a6399d3af1e96fc6be5785", None),
}

CHECKER_CENSUS = ROOT / "scripts/c79g_v15_checker_census.py"

REJECTION = OUT / f"{BASE}_{PREV}_static_bundle_rejection_receipt_v1.json"
SUPERSESSION = OUT / f"{BASE}_{PREV}_to_{TAG}_static_bundle_rejection_supersession_receipt_v1.json"
ANCHOR = OUT / f"{BASE}_{TAG}_active_predecessor_supersession_receipt_v1.json"
TARGETS = [
    REJECTION, SUPERSESSION, ANCHOR,
    OUT / f"{BASE}_schema_{TAG}.json",
    OUT / f"{BASE}_contract_{TAG}.json",
    OUT / f"{BASE}_{PREV}_to_{TAG}_static_launch_transition_receipt_v1.json",
    OUT / f"{BASE}_static_audit_{TAG}.json",
    OUT / f"{BASE}_{TAG}_semantic_source.py",
    OUT / f"{BASE}_independent_verifier_assembler_authority_consumer_{TAG}_semantic_source.py",
    OUT / f"{BASE}_cold_launch_{TAG}_semantic_source.py",
    OUT / f"{BASE}_cold_launch_manifest_{TAG}.sha256",
    OUT / f"{BASE}_cold_launch_outer_receipt_{TAG}.json",
]


def stable(path: Path, expected: str | None = None) -> bytes:
    fd = os.open(path, os.O_RDONLY | os.O_CLOEXEC | getattr(os, "O_NOFOLLOW", 0))
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
        if (before.st_dev, before.st_ino, before.st_size) != (after.st_dev, after.st_ino, len(raw)):
            raise RuntimeError(f"witness changed:{path}")
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
    result: dict[str, str] = {}
    for path in ROOT.rglob("*.pyc"):
        if path.is_file() and not path.is_symlink():
            result[str(path.relative_to(ROOT))] = sha(stable(path))
    return result


def load_r57_namespace() -> dict[str, Any]:
    raw = stable(R57_BUILDER)
    tree = ast.parse(raw.decode(), str(R57_BUILDER), mode="exec")
    compile(tree, str(R57_BUILDER), "exec")
    ns: dict[str, Any] = {"__name__": "_r58_r57_recipe",
                          "__file__": str(R57_BUILDER), "__package__": None}
    exec(compile(tree, str(R57_BUILDER), "exec"), ns, ns)
    return ns


def rename_key(mapping: dict[str, Any], old: str, new: str) -> None:
    if old in mapping:
        if new not in mapping:
            mapping[new] = mapping.pop(old)
        else:
            mapping.pop(old)


def fix_schema(value: dict[str, Any], old_retag: Any) -> dict[str, Any]:
    out = old_retag(value)
    if not isinstance(out, dict) or "$defs" not in out:
        return out
    found = 0
    raw_nodes = 0
    for name, definition in out["$defs"].items():
        if not isinstance(definition, dict):
            continue
        props = definition.get("properties", {})
        if not isinstance(props, dict) or "effective_checkpoint_object_sha256" not in props:
            continue
        found += 1
        node = props["effective_checkpoint_object_sha256"]
        if isinstance(node, str):
            if node != UPSTREAM:
                raise RuntimeError(f"r58 checkpoint leaf value:{name}")
            props["effective_checkpoint_object_sha256"] = {"const": UPSTREAM}
            raw_nodes += 1
        elif not (isinstance(node, dict) and node.get("const") == UPSTREAM):
            raise RuntimeError(f"r58 checkpoint schema node:{name}")
    if found != 9:
        raise RuntimeError(f"r58 effective checkpoint definition census:{found}")
    if raw_nodes not in (0, 9):
        raise RuntimeError(f"r58 partial checkpoint node repair:{raw_nodes}")
    return out


def fix_json(value: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(value, dict):
        return value
    schema = str(value.get("schema", ""))
    if ".contract" in schema:
        no_later = value.get("no_later_rejection_protocol", {})
        rename_key(no_later,
                   "launcher_native_rejection_matches_closed_schema_laterRejection_exact_54_key_shape",
                   "launcher_native_rejection_matches_closed_schema_laterRejection_exact_56_key_shape")
        no_later["launcher_native_rejection_matches_closed_schema_laterRejection_exact_56_key_shape"] = True
    elif "static-launch-transition" in schema:
        policy = value.get("physical_mode_policy", {})
        for old, new in {
            "v15_exact8_physical_freeze_completed": "v16r2_exact8_physical_freeze_completed",
            "v15_exact8_required_final_mode": "v16r2_exact8_required_final_mode",
            "v15_exact8_required_final_nlink": "v16r2_exact8_required_final_nlink",
            "v15_manifest_physical_freeze_completed": "v16r2_manifest_physical_freeze_completed",
            "v15_outer_physical_freeze_completed": "v16r2_outer_physical_freeze_completed",
            "v15_working_files_mode_before_cold_freeze": "v16r2_working_files_mode_before_cold_freeze",
        }.items():
            rename_key(policy, old, new)
    elif "static-audit" in schema:
        # This is the active current bundle field.  The immutable V14 receipt
        # remains byte-identical; only its current-bundle label is normalized.
        bundle = value.get("audited_v16r2_bundle", {})
        rename_key(bundle, "v14_to_v15_transition_receipt",
                   "v14_registry_shape_drift_supersession_receipt")
    return value


def launcher_registry_canonicalizer(text: str) -> str:
    tree = ast.parse(text, "r58_launcher_registry", mode="exec")
    function = next((node for node in tree.body
                     if isinstance(node, ast.FunctionDef) and
                     node.name == "producer_source_registry_shape_from_ast"), None)
    if function is None:
        raise RuntimeError("r58 launcher registry helper missing")
    lines = text.splitlines(keepends=True)
    chunk = "".join(lines[function.lineno - 1:function.end_lineno])
    old = chunk
    if chunk.count("producer_v15") != 1 or chunk.count("current v15") != 5:
        raise RuntimeError("r58 launcher v15 diagnostic census")
    chunk = chunk.replace("producer_v15", "producer_v16r2")
    chunk = chunk.replace("current v15", "current v16r2")
    if "producer_v15" in chunk or "current v15" in chunk or chunk == old:
        raise RuntimeError("r58 launcher diagnostic patch incomplete")
    lines[function.lineno - 1:function.end_lineno] = [chunk]
    return "".join(lines)


def launcher_registry_helper_ast_sha(text: str) -> str:
    """Return the r58 helper digest after current-path label normalization."""
    tree = ast.parse(text, "r58_launcher_registry_digest", mode="exec")
    function = next((node for node in tree.body
                     if isinstance(node, ast.FunctionDef) and
                     node.name == "producer_source_registry_shape_from_ast"), None)
    if function is None:
        raise RuntimeError("r58 launcher registry helper missing for digest")
    return sha(ast.dump(function, annotate_fields=True,
                        include_attributes=False).encode("utf-8"))


def checker_tools_r58() -> dict[str, Any]:
    """Load the read-only census with the current v16r2 helper digest.

    The inherited census is structurally reusable, but its historical
    constant is named V15_* and pins the old diagnostic spelling.  r58's
    helper is intentionally retagged to v16r2, so the expected digest must be
    rebound in this in-memory checker namespace.  No checker source or frozen
    bytes are modified.
    """
    raw = stable(CHECKER_CENSUS)
    tree = ast.parse(raw.decode("utf-8"), str(CHECKER_CENSUS), mode="exec")
    compile(tree, str(CHECKER_CENSUS), "exec")
    ns: dict[str, Any] = {"__name__": "_r58_checker_census",
                          "__file__": str(CHECKER_CENSUS),
                          "__package__": None}
    exec(compile(tree, str(CHECKER_CENSUS), "exec"), ns, ns)
    # The r57 launcher is immutable and has the same helper structure; use it
    # only to derive the expected r58 digest after the explicit label patch.
    launcher_raw = stable(R57_FILES["launcher"][0], R57_FILES["launcher"][1])
    normalized = launcher_registry_canonicalizer(launcher_raw.decode("utf-8"))
    ns["V15_EXPECTED_LAUNCHER_REGISTRY_HELPER_AST_SHA256"] = \
        launcher_registry_helper_ast_sha(normalized)
    return ns


def source_patch(raw: bytes, role: str, paths: dict[str, str],
                 anchor_file: str, anchor_object: str, schema_hash: str,
                 contract_hash: str, contract_object: str,
                 producer_hash: str | None = None,
                 base7: dict[str, tuple[str, str | None]] | None = None) -> bytes:
    text = raw.decode("utf-8")
    if role == "consumer":
        pattern = (r"\n        \"v12_official_rejection_file_sha256\":\n"
                   r"            V12_OFFICIAL_REJECTION_FILE_PIN,\n"
                   r"        \"v12_official_rejection_object_sha256\":\n"
                   r"            V12_OFFICIAL_REJECTION_OBJECT_PIN,")
        text, count = re.subn(pattern, "", text, count=1)
        if count != 1:
            raise RuntimeError(f"r58 consumer V12 constructor normalization:{count}")
    # The reviewed r57 patcher performs namespace, pin, and BASE7 injection.
    # Its constructor canonicalizer is replaced above, so normalized launcher
    # digests and the final source bytes see the same diagnostic labels.
    return _BASE_SOURCE_PATCH(text.encode(), role, paths, anchor_file,
                              anchor_object, schema_hash, contract_hash,
                              contract_object, producer_hash, base7)


def make_chain() -> dict[str, Any]:
    failure_vector = {
        "contract_exact_54_claim_present": True,
        "active_later_rejection_schema_required_count": 56,
        "active_later_rejection_consumer_constructor_count": 56,
        "active_later_rejection_launcher_constructor_count": 56,
        "schema_raw_effective_checkpoint_property_node_count": 9,
        "transition_active_v15_physical_mode_alias_count": 6,
        "audit_active_v14_to_v15_bundle_alias_count": 1,
        "launcher_active_v15_registry_diagnostic_literal_count": 6,
        "candidate_install": True,
        "manifest_created": False,
        "outer_created": False,
        "runtime_protocol_executed": False,
    }
    for role, (_, file_hash, object_hash) in R57_FILES.items():
        failure_vector[f"r57_{role}_file_sha256"] = file_hash
        if object_hash is not None:
            failure_vector[f"r57_{role}_object_sha256"] = object_hash
    rejection_value = close({
        "schema": f"cm2.c79g.{PREV}.active-boundary-semantic-rejection.v1",
        "status": "PERMANENT_FAIL_CLOSED_R57_ACTIVE_BOUNDARY_SEMANTIC_RESIDUES__ZERO_CREDIT",
        "failed_namespace": PREV,
        "predecessor_namespace": INPUT_PREV,
        "rejection_reason": "ACTIVE_CONTRACT_SCHEMA_NODE_AND_CURRENT_PATH_RESIDUES",
        "failure_vector": failure_vector,
        "candidate_install": True,
        "runtime_protocol_executed": False,
        "manifest_created": False,
        "outer_created": False,
        "runtime_authorized": False,
        "formal_global_closure_credit": 0,
        "D02_unlock": False,
        "append_only": True,
        "overwrite_delete_or_reuse_allowed": False,
        "predecessor_anchor_file_sha256": R57_ANCHOR_SHA,
        "predecessor_anchor_object_sha256": R57_ANCHOR_OBJECT,
    })
    rejection_raw = canon(rejection_value) + b"\n"
    rejection = {"path": str(REJECTION.relative_to(ROOT)),
                 "file_sha256": sha(rejection_raw),
                 "object_sha256": rejection_value["object_sha256"],
                 "bytes": rejection_raw}
    supersession_value = close({
        "schema": f"cm2.c79g.{PREV}-to-{TAG}.static-bundle-rejection-supersession.v1",
        "status": "FROZEN_APPEND_ONLY_REJECTED_PREDECESSOR_SUPERSEDED__ZERO_CREDIT",
        "predecessor_namespace": PREV,
        "successor_namespace": TAG,
        "predecessor_active_anchor_path": str(R57_ANCHOR.relative_to(ROOT)),
        "predecessor_active_anchor_file_sha256": R57_ANCHOR_SHA,
        "predecessor_active_anchor_object_sha256": R57_ANCHOR_OBJECT,
        "predecessor_rejection_path": rejection["path"],
        "predecessor_rejection_file_sha256": rejection["file_sha256"],
        "predecessor_rejection_object_sha256": rejection["object_sha256"],
        "upstream_checkpoint_object_sha256": UPSTREAM,
        "successor_checkpoint_object_sha256": SUCCESSOR,
        "append_only": True,
        "runtime_authorized": False,
        "formal_global_closure_credit": 0,
        "D02_unlock": False,
    })
    supersession_raw = canon(supersession_value) + b"\n"
    anchor_value = close({
        "schema": f"cm2.c79g.{TAG}.active-predecessor-supersession.v1",
        "status": "FROZEN_APPEND_ONLY_ACTIVE_PREDECESSOR_ANCHOR__ZERO_CREDIT",
        "predecessor_namespace": PREV,
        "predecessor_supersession_path": str(SUPERSESSION.relative_to(ROOT)),
        "predecessor_supersession_file_sha256": sha(supersession_raw),
        "predecessor_supersession_object_sha256": supersession_value["object_sha256"],
        "upstream_checkpoint_object_sha256": UPSTREAM,
        "successor_checkpoint_object_sha256": SUCCESSOR,
        "successor_namespace": f"{TAG}_semantic_source",
        "append_only": True,
        "runtime_authorized": False,
        "formal_global_closure_credit": 0,
        "D02_unlock": False,
        "manifest_created": False,
        "outer_created": False,
    })
    anchor_raw = canon(anchor_value) + b"\n"
    return {"rejection": rejection, "sup_value": supersession_value,
            "sup_raw": supersession_raw, "anchor_value": anchor_value,
            "anchor_raw": anchor_raw, "sup_file_sha256": sha(supersession_raw),
            "anchor_file_sha256": sha(anchor_raw),
            "anchor_object_sha256": anchor_value["object_sha256"],
            "anchor_path": str(ANCHOR.relative_to(ROOT))}


def validate_generated(generated: dict[str, bytes], meta: dict[str, Any],
                       chain: dict[str, Any]) -> None:
    _BASE_VALIDATE(generated, meta, chain)
    schema = json.loads(generated["schema"])
    raw_nodes = []
    for name, definition in schema["$defs"].items():
        if not isinstance(definition, dict):
            continue
        node = definition.get("properties", {}).get("effective_checkpoint_object_sha256")
        if node is not None:
            if not isinstance(node, dict) or node.get("const") != UPSTREAM:
                raw_nodes.append(name)
    if raw_nodes:
        raise RuntimeError(f"r58 raw effective checkpoint schema nodes:{raw_nodes}")
    contract = json.loads(generated["contract"])
    no_later = contract.get("no_later_rejection_protocol", {})
    if "launcher_native_rejection_matches_closed_schema_laterRejection_exact_54_key_shape" in no_later or \
            no_later.get("launcher_native_rejection_matches_closed_schema_laterRejection_exact_56_key_shape") is not True:
        raise RuntimeError("r58 active laterRejection contract shape claim")
    transition = json.loads(generated["transition"])
    policy = transition.get("physical_mode_policy", {})
    if any(key.startswith("v15_") for key in policy):
        raise RuntimeError("r58 active transition v15 physical policy residue")
    audit = json.loads(generated["audit"])
    if "v14_to_v15_transition_receipt" in audit.get("audited_v16r2_bundle", {}):
        raise RuntimeError("r58 active audit v14-to-v15 alias")
    launch = generated["launcher"].decode("utf-8")
    tree = ast.parse(launch, "r58_launcher", mode="exec")
    function = next((node for node in tree.body
                     if isinstance(node, ast.FunctionDef) and
                     node.name == "producer_source_registry_shape_from_ast"), None)
    if function is None:
        raise RuntimeError("r58 launcher registry helper absent")
    segment = ast.get_source_segment(launch, function) or ""
    if "producer_v15" in segment or "current v15" in segment:
        raise RuntimeError("r58 launcher active registry diagnostic residue")
    required = schema["$defs"]["laterRejection"].get("required", [])
    props = schema["$defs"]["laterRejection"].get("properties", {})
    if len(required) != 56 or set(required) != set(props):
        raise RuntimeError("r58 laterRejection schema exact56 closure")


def configure() -> tuple[dict[str, Any], Any, Any]:
    recipe, constructor, builder = _BASE_CONFIGURE()
    # The inherited audit constructor resolves _checker_tools from its own
    # namespace.  Rebind that lookup to an isolated r58 copy whose expected
    # helper digest matches the deliberate v16r2 diagnostic retag.
    constructor["_checker_tools"] = checker_tools_r58
    old_retag = builder.retag

    def retag(value: Any) -> Any:
        return fix_json(old_retag(value))

    builder.retag = retag
    old_enrich = constructor["enrich_audit"]

    def enrich(audit: dict[str, Any], source_bytes: dict[str, bytes],
               current: dict[str, str]) -> dict[str, Any]:
        return constructor["_close"](fix_json(old_enrich(audit, source_bytes, current)))

    constructor["enrich_audit"] = enrich
    return recipe, constructor, builder


def install() -> dict[str, Any]:
    result = _BASE_INSTALL()
    result["status"] = "R58_STATIC_CANDIDATE_INSTALLED__ZERO_CREDIT__RUNTIME_NOT_AUTHORIZED"
    return result


def main() -> int:
    try:
        print(json.dumps(install(), ensure_ascii=False, sort_keys=True))
        return 0
    except Exception as exc:
        print(json.dumps({
            "schema": f"cm2.c79g.{TAG}.candidate-builder.failure.v1",
            "status": "FAIL_CLOSED_R58_STATIC_INSTALL",
            "error": {"type": type(exc).__name__, "message": str(exc)},
            "candidate_install": False, "manifest_created": False,
            "outer_created": False, "runtime_authorized": False,
            "formal_global_closure_credit": 0, "D02_unlock": False,
        }, ensure_ascii=False, sort_keys=True))
        return 1


# Load the immutable r57 builder as a recipe, then replace only the hooks above.
_R57 = load_r57_namespace()
_BASE_SOURCE_PATCH = _R57["source_patch"]
_BASE_VALIDATE = _R57["validate_generated"]
_BASE_CONFIGURE = _R57["configure"]
_BASE_INSTALL = _R57["install"]
_BASE_LOAD_RECIPE = _R57["load_r56_recipe"]
_R57.update({
    "PREV": PREV, "TAG": TAG, "INPUT_PREV": INPUT_PREV,
    "INPUT_TAG": INPUT_TAG, "R56_ANCHOR": R57_ANCHOR,
    "R56_ANCHOR_SHA": R57_ANCHOR_SHA,
    "R56_ANCHOR_OBJECT": R57_ANCHOR_OBJECT, "R56_FILES": R57_FILES,
    "REJECTION": REJECTION, "SUPERSESSION": SUPERSESSION,
    "ANCHOR": ANCHOR, "TARGETS": TARGETS,
})


def _load_recipe_with_r58_constructor() -> dict[str, Any]:
    recipe = _BASE_LOAD_RECIPE()
    old_load_constructor = recipe["load_constructor"]

    def load_constructor() -> dict[str, Any]:
        constructor = old_load_constructor()
        constructor["_canonicalize_registry_helper"] = launcher_registry_canonicalizer
        return constructor

    recipe["load_constructor"] = load_constructor
    return recipe


_R57["load_r56_recipe"] = _load_recipe_with_r58_constructor
_R57["schema_fix"] = fix_schema
# Keep the immutable r57 contract transformer as a real captured hook.  Do
# not fetch it back through _R57 after replacing the slot: doing so would
# recurse forever during configure().
_BASE_CONTRACT_FIX = _R57["contract_fix"]
_R57["contract_fix_base"] = _BASE_CONTRACT_FIX
_R57["contract_fix"] = lambda value, old_retag: fix_json(
    _BASE_CONTRACT_FIX(value, old_retag))
_R57["source_patch"] = source_patch
_R57["configure"] = configure
_R57["make_chain"] = make_chain
_R57["validate_generated"] = validate_generated


if __name__ == "__main__":
    # The functions above execute in the r57 namespace when called by the
    # inherited build/install helpers.  Keep the wrapper's own entry point
    # explicit so failures remain nonzero and fail closed.
    raise SystemExit(main())
