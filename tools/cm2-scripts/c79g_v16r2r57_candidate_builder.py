#!/usr/bin/env python3
"""r57 clean-room successor builder.

This builder consumes the immutable r56 bytes and fixes the semantic, rather
than merely lexical, boundary that the r56 review exposed: the active schema
definitions still described the v15 runtime, and the consumer's live schema
ids diverged from the cold launcher's stable v16r2 protocol ids.  All work is
performed in memory until one O_EXCL installation.  No manifest, outer receipt,
runtime surface, authority, or credit is created here.
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
PREV = "v16r2r56"
TAG = "v16r2r57"
INPUT_PREV = "v16r2r54"
INPUT_TAG = "v16r2r56"
UPSTREAM = "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab"
SUCCESSOR = "dd9d64f3f0bd0dfd00fd399e3154517a34ba19cfb601ec749f44cbc08b03ca1b"
GENERIC_SCHEMA = "cm2.round306c79g.true-global-no-producer-consumer.v16r2"

R56_ANCHOR = OUT / f"{BASE}_{INPUT_TAG}_active_predecessor_supersession_receipt_v1.json"
R56_ANCHOR_SHA = "915a73ed6c83375fa1aeaaf0045e1f5f96e9fa6a415d2ff79c7d3c764a87ffa6"
R56_ANCHOR_OBJECT = "c191c6082e512e89e39de12fb2253a0dc3ea3ea7f36f9d803217fb67d5a6bb8a"
R56_FILES: dict[str, tuple[Path, str, str | None]] = {
    "schema": (OUT / f"{BASE}_schema_{INPUT_TAG}.json",
               "aa3418a8b4776b6cc3792d6a60781ca9e6c1ad156894328780557fd502cfebce", None),
    "contract": (OUT / f"{BASE}_contract_{INPUT_TAG}.json",
                 "3b7344fce00345b1ccbd51ad6efb6d93ba3e8e56567670b3c6c46251284eb183",
                 "c545078a021e5b407df2279c4d410c46c80539ad40eef2310d7824e64bdcafef"),
    "producer": (OUT / f"{BASE}_{INPUT_TAG}_semantic_source.py",
                 "de8640059d8e71f4babc125823120942c9b319914091d7ea5a3c36a3d727db2a", None),
    "consumer": (OUT / f"{BASE}_independent_verifier_assembler_authority_consumer_{INPUT_TAG}_semantic_source.py",
                 "8db1061b52404eb86640e31c6e23f89229020d559d2c2cff9d2ff77cc1edc728", None),
    "transition": (OUT / f"{BASE}_{INPUT_PREV}_to_{INPUT_TAG}_static_launch_transition_receipt_v1.json",
                   "5201d0af89da926bcea1663a1e321edd7bd847e7519d94e063a4ab682f518ac5",
                   "19c203e9de57cc3c75abc38570f35f4b3e4336594f181f5806ddc50e84e84667"),
    "audit": (OUT / f"{BASE}_static_audit_{INPUT_TAG}.json",
              "4970bc341dbc8d0130a531eea981ac706cffacc3d376a00f764a7e9d7dd69542",
              "58aa8f68fc63672f93a64efb942c91e4c01c9beb5557a45b2cd9fd12844cdd8f"),
    "launcher": (OUT / f"{BASE}_cold_launch_{INPUT_TAG}_semantic_source.py",
                 "e045fb0f1b83d10b0a48f0cd89fc20c03a799bdeafbb72addb3cbc871b747718", None),
}

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
    result: dict[str, str] = {}
    for path in ROOT.rglob("*.pyc"):
        if path.is_file() and not path.is_symlink():
            result[str(path.relative_to(ROOT))] = sha(stable(path))
    return result


def load_r56_recipe() -> dict[str, Any]:
    """Load the reviewed r56 recipe without importing it or writing pyc."""
    recipe = ROOT / "scripts/c79g_v16r2r56_candidate_builder.py"
    raw = stable(recipe)
    tree = ast.parse(raw.decode(), str(recipe), mode="exec")
    compile(tree, str(recipe), "exec")
    ns: dict[str, Any] = {"__name__": "_r56_recipe_in_memory",
                          "__file__": str(recipe), "__package__": None}
    exec(compile(tree, str(recipe), "exec"), ns, ns)
    return ns


def replace_hex(text: str, name: str, value: str) -> str:
    pattern = rf"(?m)^({re.escape(name)}\s*=\s*)(['\"])[0-9a-f]{{64}}\2\s*$"
    result, count = re.subn(pattern, rf'\1"{value}"', text)
    if count != 1:
        raise RuntimeError(f"r57 source pin census {name}:{count}")
    return result


def source_patch(raw: bytes, role: str, paths: dict[str, str],
                 anchor_file: str, anchor_object: str, schema_hash: str,
                 contract_hash: str, contract_object: str,
                 producer_hash: str | None = None,
                 base7: dict[str, tuple[str, str | None]] | None = None) -> bytes:
    text = raw.decode("utf-8")
    old_edge = f"{BASE}_{INPUT_PREV}_to_{INPUT_TAG}_"
    text = text.replace(old_edge, "__R57_EDGE__")
    text = text.replace(INPUT_TAG, TAG).replace(INPUT_TAG.upper(), TAG.upper())
    text = text.replace("__R57_EDGE__", f"{BASE}_{PREV}_to_{TAG}_")
    if role != "launcher":
        for name, value in (
            ("ACTIVE_PREDECESSOR_SUPERSESSION_FILE_PIN", anchor_file),
            ("ACTIVE_PREDECESSOR_SUPERSESSION_OBJECT_PIN", anchor_object),
            ("CONTRACT_FILE_PIN", contract_hash),
            ("CONTRACT_OBJECT_PIN", contract_object),
            ("CLOSED_SCHEMA_FILE_PIN", schema_hash),
        ):
            text = replace_hex(text, name, value)
        if role == "consumer" and producer_hash is not None:
            text = replace_hex(text, "PRODUCER_SOURCE_PIN", producer_hash)
        # The launcher and consumer must validate the same stable v16r2
        # protocol objects.  The round namespace remains the contract/source
        # namespace, not the live schema-id namespace.
        if role == "consumer":
            for name, suffix in (
                ("AUTHORITY_SEAL_SCHEMA", "authority-seal"),
                ("PRESEAL_SCHEMA", "preseal-committed-surface"),
                ("INNER_ROOT_SCHEMA", "inner-composite"),
                ("LATER_REJECTION_SCHEMA", "later-rejection"),
                ("COLD_ROOT_SCHEMA", "cold-launched-committed-authority"),
                ("LIVE_REQUEST_SCHEMA", "cold-live-commit-request"),
                ("LIVE_ACK_SCHEMA", "cold-live-ack"),
                ("LIVE_RELEASE_SCHEMA", "cold-live-release"),
            ):
                text, count = re.subn(
                    rf"(?m)^{name}\s*=.*$",
                    f'{name} = "{GENERIC_SCHEMA}.{suffix}"', text, count=1)
                if count != 1:
                    raise RuntimeError(f"r57 protocol id census {name}:{count}")
            # The consumer's live rejection constructor is executable code,
            # not merely an audit hint.  r56 omitted the two inherited V12
            # pins from that constructor even though laterRejection requires
            # them (and the launcher already emitted them).  Insert the
            # fields before the first AST/shape gate so the source hash and
            # all downstream receipts are computed over the corrected bytes.
            needle = (
                '        "v11_official_rejection_object_sha256":\n'
                '            V11_OFFICIAL_REJECTION_OBJECT_PIN,\n'
                '        "v7_publication_lock_continuity_incident_object_sha256":')
            addition = (
                '        "v11_official_rejection_object_sha256":\n'
                '            V11_OFFICIAL_REJECTION_OBJECT_PIN,\n'
                '        "v12_official_rejection_file_sha256":\n'
                '            V12_OFFICIAL_REJECTION_FILE_PIN,\n'
                '        "v12_official_rejection_object_sha256":\n'
                '            V12_OFFICIAL_REJECTION_OBJECT_PIN,\n'
                '        "v7_publication_lock_continuity_incident_object_sha256":')
            if text.count(needle) != 1:
                raise RuntimeError("r57 consumer laterRejection constructor insertion census")
            text = text.replace(needle, addition, 1)
    else:
        tree = ast.parse(text, "r57_launcher", mode="exec")
        counts = {"file": 0, "object": 0}
        for node in ast.walk(tree):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target] if isinstance(node, ast.AnnAssign) else []
            for target in targets:
                if not isinstance(target, ast.Name):
                    continue
                if target.id == "ACTIVE_PREDECESSOR_SUPERSESSION_FILE_PIN":
                    node.value = ast.Constant(anchor_file); counts["file"] += 1
                elif target.id == "ACTIVE_PREDECESSOR_SUPERSESSION_OBJECT_PIN":
                    node.value = ast.Constant(anchor_object); counts["object"] += 1
                elif target.id == "FINAL_BASE7_PINS_INSTALLED":
                    node.value = ast.Constant(True)
        if counts != {"file": 2, "object": 2}:
            raise RuntimeError(f"r57 launcher active pin assignment census:{counts}")
        funcs = [node for node in tree.body if isinstance(node, ast.FunctionDef)
                 and node.name == "configure_workspace_paths"]
        if len(funcs) != 1:
            raise RuntimeError("r57 launcher configure function census")
        assignments = [node for node in funcs[0].body
                       if isinstance(node, ast.Assign) and len(node.targets) == 1
                       and isinstance(node.targets[0], ast.Name)
                       and node.targets[0].id == "BASE7_PINS"]
        if len(assignments) != 1 or base7 is None:
            raise RuntimeError("r57 launcher BASE7 census")
        pins = dict(base7)
        pins.setdefault("v14", ("aa4323027e2313f8a2eda0d6ffc039a537afe342d496d1f75cd73fcd47446c01",
                                 "93689e62ae36f405f045a769f4dc6f6e6fd83a16605d08299d5c3397ad657e2e"))
        order = [("V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT", "v14"),
                 ("SCHEMA", "schema"), ("CONTRACT", "contract"),
                 ("PRODUCER", "producer"), ("CONSUMER", "consumer"),
                 ("TRANSITION", "transition"), ("AUDIT", "audit")]
        assignments[0].value = ast.Dict(
            keys=[ast.Name(id=name, ctx=ast.Load()) for name, _ in order],
            values=[ast.Tuple([ast.Constant(pins[key][0]),
                               ast.Constant(pins[key][1])], ast.Load())
                    for _, key in order])
        text = ast.unparse(tree) + "\n"
    edge_name = f"{BASE}_{PREV}_to_{TAG}_static_launch_transition_receipt_v1.json"
    if edge_name not in text:
        raise RuntimeError(f"{role}: r57 active edge absent")
    return text.encode()


def rename_key(mapping: dict[str, Any], old: str, new: str) -> None:
    if old in mapping:
        if new not in mapping:
            mapping[new] = mapping.pop(old)
        else:
            mapping.pop(old)


def schema_fix(value: dict[str, Any], old_retag: Any) -> dict[str, Any]:
    out = old_retag(value)
    if not isinstance(out, dict) or "$defs" not in out:
        return out
    defs = out["$defs"]
    def put(def_name: str, path: tuple[Any, ...], new_value: Any) -> None:
        node: Any = defs[def_name]
        for part in path[:-1]:
            node = node[part]
        node[path[-1]] = new_value

    checkpoint = UPSTREAM
    producer = f"deliverables/{BASE}_{TAG}_semantic_source.py"
    consumer = f"deliverables/{BASE}_independent_verifier_assembler_authority_consumer_{TAG}_semantic_source.py"
    # Rename the active v15 property names before assigning their new const
    # values below.  `current` intentionally addresses the post-rename
    # names, so doing this after the put() loop would be a KeyError and would
    # leave a partially transformed in-memory schema.
    renames = {
        "v14_to_v15_transition_file_sha256": "v16_to_v16r2_transition_file_sha256",
        "v14_to_v15_transition_object_sha256": "v16_to_v16r2_transition_object_sha256",
        "v14_to_v15_transition_identity": "v16_to_v16r2_transition_identity",
        "current_v15_and_all_predecessor_same_statx_mount": "current_v16r2_and_all_predecessor_same_statx_mount",
        "current_v15_and_all_predecessor_unique_file_identity_count": "current_v16r2_and_all_predecessor_unique_file_identity_count",
        "reject_command_exempts_only_fresh_empty_v15_rejection_namespace": "reject_command_exempts_only_fresh_empty_v16r2_rejection_namespace",
        "current_v15_producer_source_content_opened_read_decoded_parsed_compiled_imported_or_executed": "current_v16r2_producer_source_content_opened_read_decoded_parsed_compiled_imported_or_executed",
        "v15_later_rejection": "v16r2_later_rejection",
        "v15_rejection_namespace": "v16r2_rejection_namespace",
    }
    for name in ("authoritySeal", "coldLaunchProof", "exactPaths",
                 "independentConsumerProof", "staticFreezeProof"):
        props = defs[name].get("properties", {})
        for old, new in renames.items():
            rename_key(props, old, new)
        if isinstance(defs[name].get("required"), list):
            defs[name]["required"] = [renames.get(item, item)
                                        for item in defs[name]["required"]]
    current = {
        ("authoritySeal", ("properties", "schema", "const")): GENERIC_SCHEMA + ".authority-seal",
        ("authoritySeal", ("properties", "staging_path", "const")): f".cm2-runtime/cm2-global-authority-heads/.c79g-v16r2-authority-stage-{checkpoint}.seal",
        ("authoritySeal", ("properties", "target_path", "const")): f".cm2-runtime/cm2-global-authority-heads/c79g-v16r2-{checkpoint}.seal",
        ("candidateSurfaceProof", ("properties", "candidate_A_path", "const")): f".cm2-runtime/c79g-v16r2-candidate-a-{checkpoint}",
        ("candidateSurfaceProof", ("properties", "candidate_B_path", "const")): f".cm2-runtime/c79g-v16r2-candidate-b-{checkpoint}",
        ("candidateSurfaceProof", ("properties", "staging_path_template", "const")): f".cm2-runtime/.c79g-v16r2-candidate-stage-{{a|b}}-{checkpoint}",
        ("coldLaunchProof", ("properties", "child_source_path", "const")): consumer,
        ("coldLaunchProof", ("properties", "cold_two_phase_live_protocol", "const")): "CM2_C79G_V16R2_COLD_TWO_PHASE_LIVE_ACK_V1",
        ("coldLaunchedCommittedAuthority", ("properties", "authority_root_domain", "const")): "CM2_C79G_V16R2_COLD_LAUNCHED_AUTHORITY_ROOT_V1",
        ("coldLaunchedCommittedAuthority", ("properties", "schema", "const")): GENERIC_SCHEMA + ".cold-launched-committed-authority",
        ("coldLiveProtocol", ("properties", "ack_binding_domain", "const")): "CM2_C79G_V16R2_COLD_LIVE_ACK_BINDING_V1",
        ("coldLiveProtocol", ("properties", "deterministic_transaction_binding_domain", "const")): "CM2_C79G_V16R2_COLD_TRANSACTION_BINDING_V1",
        ("coldLiveProtocol", ("properties", "prewrapper_body_domain", "const")): "CM2_C79G_V16R2_COLD_PREWRAPPER_BODY_V1",
        ("coldLiveProtocol", ("properties", "protocol", "const")): "CM2_C79G_V16R2_COLD_TWO_PHASE_LIVE_ACK_V1",
        ("coldLiveProtocol", ("properties", "ack_schema", "const")): GENERIC_SCHEMA + ".cold-live-ack",
        ("coldLiveProtocol", ("properties", "request_schema", "const")): GENERIC_SCHEMA + ".cold-live-commit-request",
        ("coldLiveProtocol", ("properties", "release_schema", "const")): GENERIC_SCHEMA + ".cold-live-release",
        ("completionInstallProof", ("properties", "committed_path", "const")): f".cm2-runtime/c79g-v16r2-committed-completion-{checkpoint}",
        ("completionInstallProof", ("properties", "staging_path", "const")): f".cm2-runtime/.c79g-v16r2-completion-stage-{checkpoint}",
        ("completionInstallProof", ("properties", "exact_member_order", "prefixItems", 0, "const")): "cm2_round306c79g_true_global_no_producer_consumer_completion_verification_copy_v16r2.json",
        ("completionInstallProof", ("properties", "exact_member_order", "prefixItems", 1, "const")): "cm2_round306c79g_true_global_no_producer_consumer_pre_outer_completion_receipt_v16r2.json",
        ("completionInstallProof", ("properties", "exact_member_order", "prefixItems", 2, "const")): "cm2_round306c79g_true_global_no_producer_consumer_one_global_manifest_v16r2.sha256",
        ("completionInstallProof", ("properties", "exact_member_order", "prefixItems", 3, "const")): f"cm2_round306c79g_true_global_no_producer_consumer_cold_launch_outer_receipt_{TAG}.json",
        ("exactPaths", ("properties", "authority_seal", "const")): f".cm2-runtime/cm2-global-authority-heads/c79g-v16r2-{checkpoint}.seal",
        ("exactPaths", ("properties", "candidate_A", "const")): f".cm2-runtime/c79g-v16r2-candidate-a-{checkpoint}",
        ("exactPaths", ("properties", "candidate_B", "const")): f".cm2-runtime/c79g-v16r2-candidate-b-{checkpoint}",
        ("exactPaths", ("properties", "committed_completion", "const")): f".cm2-runtime/c79g-v16r2-committed-completion-{checkpoint}",
        ("exactPaths", ("properties", "v16r2_later_rejection", "const")): f".cm2-runtime/c79g-v16r2-rejections-{checkpoint}/rejection.json",
        ("exactPaths", ("properties", "v16r2_rejection_namespace", "const")): f".cm2-runtime/c79g-v16r2-rejections-{checkpoint}",
        ("exactPaths", ("properties", "verification_A", "const")): f".cm2-runtime/c79g-v16r2-verification-a-{checkpoint}",
        ("exactPaths", ("properties", "verification_B", "const")): f".cm2-runtime/c79g-v16r2-verification-b-{checkpoint}",
        ("independentConsumerProof", ("properties", "authority_seal_target_path", "const")): f".cm2-runtime/cm2-global-authority-heads/c79g-v16r2-{checkpoint}.seal",
        # These two objects are constructed as SCHEMA + suffix by the
        # round-scoped consumer, while the cold launcher uses explicit stable
        # generic IDs for its live protocol roots.  Keep the constructor's
        # round-scoped values exact and reserve GENERIC_SCHEMA for the shared
        # live protocol constants.
        ("independentConsumerProof", ("properties", "schema", "const")): f"cm2.round306c79g.true-global-no-producer-consumer.{TAG}.independent-consumer-proof",
        ("innerComposite", ("properties", "authority_root_domain", "const")): "CM2_C79G_V16R2_AUTHORITY_ROOT_V1",
        ("innerComposite", ("properties", "schema", "const")): GENERIC_SCHEMA + ".inner-composite",
        ("laterRejection", ("properties", "namespace_exact_path", "const")): f".cm2-runtime/c79g-v16r2-rejections-{checkpoint}",
        ("laterRejection", ("properties", "rejection_reason", "const")): "ORPHANED_OR_INCOMPLETE_C79G_V16R2_SURFACE",
        ("laterRejection", ("properties", "schema", "const")): GENERIC_SCHEMA + ".later-rejection",
        ("laterRejection", ("properties", "target_exact_path", "const")): f".cm2-runtime/c79g-v16r2-rejections-{checkpoint}/rejection.json",
        ("noLaterRejection", ("properties", "deterministic_target_exact_path", "const")): f".cm2-runtime/c79g-v16r2-rejections-{checkpoint}/rejection.json",
        ("noLaterRejection", ("properties", "namespace_exact_path", "const")): f".cm2-runtime/c79g-v16r2-rejections-{checkpoint}",
        ("postsealLiveReplay", ("properties", "authority_seal_exact_path", "const")): f".cm2-runtime/cm2-global-authority-heads/c79g-v16r2-{checkpoint}.seal",
        ("presealCommittedSurface", ("properties", "preseal_root_domain", "const")): "CM2_C79G_V16R2_PRESEAL_ROOT_V2",
        ("presealCommittedSurface", ("properties", "schema", "const")): GENERIC_SCHEMA + ".preseal-committed-surface",
        ("producerIdentityMetadata", ("properties", "path", "const")): producer,
        ("selfIdentity", ("properties", "path", "const")): consumer,
        ("standaloneOuter", ("properties", "schema", "const")): f"cm2.round306c79g.true-global-no-producer-consumer.{TAG}.standalone-final-outer",
        ("v3OfficialLaterRejectionProof", ("properties", "successor_root_schema", "const")): GENERIC_SCHEMA + ".cold-launched-committed-authority",
        ("verificationSurfaceProof", ("properties", "verification_A_path", "const")): f".cm2-runtime/c79g-v16r2-verification-a-{checkpoint}",
        ("verificationSurfaceProof", ("properties", "verification_B_path", "const")): f".cm2-runtime/c79g-v16r2-verification-b-{checkpoint}",
    }
    for (name, path), new_value in current.items():
        put(name, path, new_value)
    # The active property/required renames were applied before `current`
    # above; repeat is intentionally omitted here to keep the transformation
    # order explicit and avoid silently masking a missing active definition.
    for name in ("authoritySeal", "coldLaunchProof", "exactPaths",
                 "independentConsumerProof", "staticFreezeProof"):
        props = defs[name].get("properties", {})
        for old, new in renames.items():
            rename_key(props, old, new)
        if isinstance(defs[name].get("required"), list):
            defs[name]["required"] = [renames.get(item, item)
                                        for item in defs[name]["required"]]
    out["title"] = f"C79g {TAG} full-shape zero-credit schema"
    out["description"] = (f"Append-only {TAG} schema with a unified v16r2 live protocol; "
                           "all persisted credit and runtime authority remain disabled.")
    return out


def contract_fix(value: dict[str, Any], old_retag: Any) -> dict[str, Any]:
    out = old_retag(value)
    if not isinstance(out, dict) or ".contract" not in str(out.get("schema", "")):
        return out
    paths = out.get("exact_publication_paths", {})
    rename_key(paths, "v15_later_rejection", "v16r2_later_rejection")
    rename_key(paths, "v15_rejection_namespace", "v16r2_rejection_namespace")
    checkpoint = UPSTREAM
    paths["v16r2_later_rejection"] = f".cm2-runtime/c79g-v16r2-rejections-{checkpoint}/rejection.json"
    paths["v16r2_rejection_namespace"] = f".cm2-runtime/c79g-v16r2-rejections-{checkpoint}"
    completion = out.get("completion_protocol", {})
    completion["completion_member_order"] = [
        "cm2_round306c79g_true_global_no_producer_consumer_completion_verification_copy_v16r2.json",
        "cm2_round306c79g_true_global_no_producer_consumer_pre_outer_completion_receipt_v16r2.json",
        "cm2_round306c79g_true_global_no_producer_consumer_one_global_manifest_v16r2.sha256",
        f"cm2_round306c79g_true_global_no_producer_consumer_cold_launch_outer_receipt_{TAG}.json",
    ]
    composite = out.get("composite_authority_predicate", {})
    composite.update({
        "authority_root_domain": "CM2_C79G_V16R2_AUTHORITY_ROOT_V1",
        "inner_schema": GENERIC_SCHEMA + ".inner-composite",
        "preseal_root_domain": "CM2_C79G_V16R2_PRESEAL_ROOT_V2",
        "preseal_schema": GENERIC_SCHEMA + ".preseal-committed-surface",
        "schema_root": GENERIC_SCHEMA + ".cold-launched-committed-authority",
    })
    if "later_v15_rejection_revokes_authority_immediately" in composite:
        composite["later_v16r2_rejection_revokes_authority_immediately"] = composite.pop("later_v15_rejection_revokes_authority_immediately")
    composite["authority_root_structure"] = str(composite.get("authority_root_structure", "")).replace("V15_", "V16R2_")
    composite["required_conjuncts"] = [str(x).replace("V15_", "V16R2_") for x in composite.get("required_conjuncts", [])]
    no_later = out.get("no_later_rejection_protocol", {})
    no_later.update({
        "deterministic_target_exact_path": f".cm2-runtime/c79g-v16r2-rejections-{checkpoint}/rejection.json",
        "namespace_exact_path": f".cm2-runtime/c79g-v16r2-rejections-{checkpoint}",
        "fixed_rejection_reason": "ORPHANED_OR_INCOMPLETE_C79G_V16R2_SURFACE",
    })
    if "reject_entrypoint_exemption_is_only_fresh_empty_v15_rejection_namespace_guard" in no_later:
        no_later["reject_entrypoint_exemption_is_only_fresh_empty_v16r2_rejection_namespace_guard"] = no_later.pop("reject_entrypoint_exemption_is_only_fresh_empty_v15_rejection_namespace_guard")
    protocol = out.get("independent_authority_consumer_protocol", {})
    rename_key(protocol, "current_v15_producer_source_open_read_decode_parse_compile_import_or_execute_allowed",
               "current_v16r2_producer_source_open_read_decode_parse_compile_import_or_execute_allowed")
    census = protocol.get("cold_live_ACK_final_dynamic_replay_census", {})
    for key in list(census):
        if key.startswith("v15_"):
            rename_key(census, key, "v16r2_" + key[4:])
    boundary = out.get("credit_boundary", {})
    for key in list(boundary):
        if key.startswith("v15_"):
            rename_key(boundary, key, "v16r2_" + key[4:])
    return out


def configure() -> tuple[dict[str, Any], Any, Any]:
    recipe = load_r56_recipe()
    recipe.update({"PREV": PREV, "TAG": TAG,
                   "R54_ANCHOR": R56_ANCHOR, "R54_ANCHOR_SHA": R56_ANCHOR_SHA,
                   "R54_ANCHOR_OBJECT": R56_ANCHOR_OBJECT, "R54_FILES": R56_FILES,
                   "REJECTION": REJECTION, "SUPERSESSION": SUPERSESSION,
                   "ANCHOR": ANCHOR, "TARGETS": TARGETS, "SUCCESSOR": SUCCESSOR})
    recipe["source_patch"] = source_patch
    constructor = recipe["load_constructor"]()
    builder = recipe["configure"](constructor)
    old_retag = builder.retag
    def retag(value: Any) -> Any:
        if isinstance(value, dict) and "$defs" in value:
            return schema_fix(value, old_retag)
        return contract_fix(value, old_retag)
    builder.retag = retag
    builder.TAG = TAG; builder.PREV = PREV; builder.UPSTREAM = UPSTREAM
    builder.CHECKPOINT = UPSTREAM
    builder.ANCHOR_IN = R56_ANCHOR
    builder.SRC_IN = {k: R56_FILES[k][0] for k in ("producer", "consumer", "launcher")}
    builder.JSON_IN = {k: R56_FILES[k][0] for k in ("schema", "contract", "transition", "audit")}
    return recipe, constructor, builder


def make_chain() -> dict[str, Any]:
    rejection = close({
        "schema": f"cm2.c79g.{PREV}.schema-runtime-path-split-rejection.v1",
        "status": "PERMANENT_FAIL_CLOSED_R56_SCHEMA_RUNTIME_PATH_AND_PROTOCOL_ID_SPLIT__ZERO_CREDIT",
        "failed_namespace": PREV, "predecessor_namespace": INPUT_PREV,
        "rejection_reason": "ACTIVE_SCHEMA_DEFS_REMAINED_V15_AND_CONSUMER_LIVE_SCHEMA_IDS_DIVERGED_FROM_LAUNCHER_V16R2",
        "failure_vector": {
            "stale_schema_const_leaf_count": 50,
            "stale_active_key_or_required_ref_count": 9,
            "consumer_launcher_live_schema_id_split": True,
            "consumer_runtime_schema_namespace": "v16r2r56",
            "launcher_runtime_schema_namespace": "v16r2",
            "r56_candidate_schema_file_sha256": R56_FILES["schema"][1],
            "r56_candidate_contract_file_sha256": R56_FILES["contract"][1],
            "r56_candidate_contract_object_sha256": R56_FILES["contract"][2],
            "r56_candidate_producer_file_sha256": R56_FILES["producer"][1],
            "r56_candidate_consumer_file_sha256": R56_FILES["consumer"][1],
            "r56_candidate_transition_file_sha256": R56_FILES["transition"][1],
            "r56_candidate_transition_object_sha256": R56_FILES["transition"][2],
            "r56_candidate_audit_file_sha256": R56_FILES["audit"][1],
            "r56_candidate_audit_object_sha256": R56_FILES["audit"][2],
            "r56_candidate_launcher_file_sha256": R56_FILES["launcher"][1],
            "candidate_install": True,
            "manifest_created": False, "outer_created": False,
            "runtime_protocol_executed": False,
        },
        "candidate_install": True, "runtime_protocol_executed": False,
        "manifest_created": False, "outer_created": False,
        "runtime_authorized": False, "formal_global_closure_credit": 0,
        "D02_unlock": False, "append_only": True,
        "overwrite_delete_or_reuse_allowed": False,
        "predecessor_anchor_file_sha256": R56_ANCHOR_SHA,
        "predecessor_anchor_object_sha256": R56_ANCHOR_OBJECT,
    })
    rejection_raw = canon(rejection) + b"\n"
    rejection_entry = {"path": str(REJECTION.relative_to(ROOT)),
                       "file_sha256": sha(rejection_raw),
                       "object_sha256": rejection["object_sha256"],
                       "bytes": rejection_raw}
    supersession = close({
        "schema": f"cm2.c79g.{PREV}-to-{TAG}.static-bundle-rejection-supersession.v1",
        "status": "FROZEN_APPEND_ONLY_REJECTED_PREDECESSOR_SUPERSEDED__ZERO_CREDIT",
        "predecessor_namespace": PREV, "successor_namespace": TAG,
        "predecessor_active_anchor_path": str(R56_ANCHOR.relative_to(ROOT)),
        "predecessor_active_anchor_file_sha256": R56_ANCHOR_SHA,
        "predecessor_active_anchor_object_sha256": R56_ANCHOR_OBJECT,
        "predecessor_rejection_path": rejection_entry["path"],
        "predecessor_rejection_file_sha256": rejection_entry["file_sha256"],
        "predecessor_rejection_object_sha256": rejection_entry["object_sha256"],
        "upstream_checkpoint_object_sha256": UPSTREAM,
        "successor_checkpoint_object_sha256": SUCCESSOR,
        "append_only": True, "runtime_authorized": False,
        "formal_global_closure_credit": 0, "D02_unlock": False,
    })
    supersession_raw = canon(supersession) + b"\n"
    anchor = close({
        "schema": f"cm2.c79g.{TAG}.active-predecessor-supersession.v1",
        "status": "FROZEN_APPEND_ONLY_ACTIVE_PREDECESSOR_ANCHOR__ZERO_CREDIT",
        "predecessor_namespace": PREV,
        "predecessor_supersession_path": str(SUPERSESSION.relative_to(ROOT)),
        "predecessor_supersession_file_sha256": sha(supersession_raw),
        "predecessor_supersession_object_sha256": supersession["object_sha256"],
        "upstream_checkpoint_object_sha256": UPSTREAM,
        "successor_checkpoint_object_sha256": SUCCESSOR,
        "successor_namespace": f"{TAG}_semantic_source",
        "append_only": True, "runtime_authorized": False,
        "formal_global_closure_credit": 0, "D02_unlock": False,
        "manifest_created": False, "outer_created": False,
    })
    anchor_raw = canon(anchor) + b"\n"
    return {"rejection": rejection_entry, "sup_value": supersession,
            "sup_raw": supersession_raw, "anchor_value": anchor,
            "anchor_raw": anchor_raw, "sup_file_sha256": sha(supersession_raw),
            "anchor_file_sha256": sha(anchor_raw),
            "anchor_object_sha256": anchor["object_sha256"],
            "anchor_path": str(ANCHOR.relative_to(ROOT))}


def validate_generated(generated: dict[str, bytes], meta: dict[str, Any],
                       chain: dict[str, Any]) -> None:
    def constructor_keys(raw: bytes, function_name: str) -> set[str]:
        """Return the literal keys passed to close_object in a constructor.

        This is deliberately an AST-only check: importing either executable
        source could touch runtime state.  The object_sha256 member is added
        by close_object, so the source literal is compared with the schema's
        required set minus that derived member.
        """
        tree = ast.parse(raw.decode(), function_name, mode="exec")
        funcs = [node for node in ast.walk(tree)
                 if isinstance(node, ast.FunctionDef) and node.name == function_name]
        if len(funcs) != 1:
            raise RuntimeError(f"r57 constructor function census:{function_name}")
        found: list[set[str]] = []
        for node in ast.walk(funcs[0]):
            if not isinstance(node, ast.Return) or not isinstance(node.value, ast.Call):
                continue
            call = node.value
            if not isinstance(call.func, ast.Name) or call.func.id != "close_object" or len(call.args) != 1:
                continue
            arg = call.args[0]
            if not isinstance(arg, ast.Dict):
                continue
            keys: set[str] = set()
            for key in arg.keys:
                if not isinstance(key, ast.Constant) or not isinstance(key.value, str):
                    raise RuntimeError(f"r57 nonliteral constructor key:{function_name}")
                if key.value in keys:
                    raise RuntimeError(f"r57 duplicate constructor key:{function_name}:{key.value}")
                keys.add(key.value)
            found.append(keys)
        if len(found) != 1:
            raise RuntimeError(f"r57 constructor return census:{function_name}:{len(found)}")
        return found[0]

    for role in ("producer", "consumer", "launcher"):
        tree = ast.parse(generated[role].decode(), role, mode="exec")
        compile(tree, role, "exec")
    schema = json.loads(generated["schema"])
    if len(schema.get("$defs", {})) != 46 or schema.get("$ref") != "#/$defs/coldLaunchedCommittedAuthority":
        raise RuntimeError("r57 schema shape/root")
    if "v15" in json.dumps(schema["$defs"], sort_keys=True):
        # Historical incident prose is not in active $defs; any remaining v15
        # token there is therefore an executable current-path residue.
        raise RuntimeError("r57 active schema v15 residue")
    for role in ("contract", "transition", "audit"):
        obj = json.loads(generated[role])
        body = dict(obj); claim = body.pop("object_sha256", None)
        if claim != sha(canon(body)):
            raise RuntimeError(f"r57 {role} object closure")
    contract = json.loads(generated["contract"])
    if len(contract) != 30 or len(json.loads(generated["transition"])) != 31 or len(json.loads(generated["audit"])) != 30:
        raise RuntimeError("r57 top-level shape")
    bundle = contract.get("v16r2_bundle", {})
    if bundle.get("bundle_version") != TAG or bundle.get("formal_global_closure_credit") != 0 or bundle.get("D02_unlock") is not False:
        raise RuntimeError("r57 zero-credit bundle state")
    if contract.get("composite_authority_predicate", {}).get("schema_root") != GENERIC_SCHEMA + ".cold-launched-committed-authority":
        raise RuntimeError("r57 contract/schema protocol root split")
    if contract.get("completion_protocol", {}).get("completion_member_order", [""])[-1] != f"cm2_round306c79g_true_global_no_producer_consumer_cold_launch_outer_receipt_{TAG}.json":
        raise RuntimeError("r57 completion member order")
    launch = ast.parse(generated["launcher"].decode(), "r57_launcher", mode="exec")
    required_later = set(schema["$defs"]["laterRejection"]["required"])
    expected_constructor = required_later - {"object_sha256"}
    consumer_keys = constructor_keys(generated["consumer"], "construct_later_rejection")
    launcher_keys = constructor_keys(generated["launcher"], "construct_launcher_native_rejection")
    if consumer_keys != expected_constructor or launcher_keys != expected_constructor:
        raise RuntimeError(
            "r57 laterRejection constructor/schema key-set split:"
            f" consumer_missing={sorted(expected_constructor - consumer_keys)}"
            f" consumer_extra={sorted(consumer_keys - expected_constructor)}"
            f" launcher_missing={sorted(expected_constructor - launcher_keys)}"
            f" launcher_extra={sorted(launcher_keys - expected_constructor)}")
    if consumer_keys != launcher_keys:
        raise RuntimeError("r57 consumer/launcher laterRejection key-set split")
    files = []; objects = []
    for node in ast.walk(launch):
        targets = node.targets if isinstance(node, ast.Assign) else [node.target] if isinstance(node, ast.AnnAssign) else []
        for target in targets:
            if isinstance(target, ast.Name) and target.id == "ACTIVE_PREDECESSOR_SUPERSESSION_FILE_PIN":
                files.append(ast.literal_eval(node.value))
            elif isinstance(target, ast.Name) and target.id == "ACTIVE_PREDECESSOR_SUPERSESSION_OBJECT_PIN":
                objects.append(ast.literal_eval(node.value))
    if len(files) != 2 or set(files) != {chain["anchor_file_sha256"]} or len(objects) != 2 or set(objects) != {chain["anchor_object_sha256"]}:
        raise RuntimeError("r57 launcher active pin split")
    # The caller snapshots the inventory around the entire in-memory build;
    # there is no meaningful same-expression comparison here.


def build_in_memory() -> tuple[dict[str, Any], dict[str, bytes], dict[str, Any], dict[str, Any]]:
    if not (sys.flags.isolated and sys.flags.no_site and sys.flags.dont_write_bytecode):
        raise RuntimeError("r57 requires isolated no-bytecode interpreter")
    before = pyc_inventory()
    for path, expected, _ in R56_FILES.values():
        stable(path, expected)
    stable(R56_ANCHOR, R56_ANCHOR_SHA)
    occupied = [str(path.relative_to(ROOT)) for path in TARGETS if path.exists()]
    if occupied:
        raise RuntimeError("r57 target already exists:" + ",".join(occupied))
    recipe, constructor, builder = configure()
    chain = make_chain()
    generated, meta = constructor["_build_r51_candidate"](builder, chain)
    validate_generated(generated, meta, chain)
    if pyc_inventory() != before:
        raise RuntimeError("r57 pyc inventory changed during build")
    preflight = {"r56_anchor_file_sha256": R56_ANCHOR_SHA,
                 "r56_anchor_object_sha256": R56_ANCHOR_OBJECT,
                 "target_paths_absent": True, "pyc_inventory_count": len(before),
                 "runtime_authorized": False, "formal_global_closure_credit": 0,
                 "D02_unlock": False}
    return preflight, generated, meta, chain


def install() -> dict[str, Any]:
    preflight, generated, meta, chain = build_in_memory()
    before = pyc_inventory()
    recipe, constructor, builder = configure()
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
    if pyc_inventory() != before:
        raise RuntimeError("r57 pyc inventory changed during installation")
    return {"schema": f"cm2.c79g.{TAG}.candidate-builder.v1",
            "status": "R57_STATIC_CANDIDATE_INSTALLED__ZERO_CREDIT__RUNTIME_NOT_AUTHORIZED",
            "preflight": preflight, "actions": actions, "meta": meta,
            "chain": {k: v for k, v in chain.items() if k not in {"rejection", "sup_raw", "anchor_raw"}},
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
                          "status": "FAIL_CLOSED_R57_STATIC_INSTALL",
                          "error": {"type": type(exc).__name__, "message": str(exc)},
                          "candidate_install": False, "manifest_created": False,
                          "outer_created": False, "runtime_authorized": False,
                          "formal_global_closure_credit": 0, "D02_unlock": False},
                         ensure_ascii=False, sort_keys=True))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
