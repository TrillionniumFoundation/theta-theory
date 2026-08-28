#!/usr/bin/env python3
"""Fail-closed append-only builder for the C79g v16r9 JSON bundle.

The source names and the most recent semantic-supersession receipt are
deliberately configuration inputs.  Until those names are supplied, this
command only prints a missing-configuration report and writes nothing.  Once
configured, it reads the v16r2 full-shape quartet, the C53 checkpoint, the
frozen predecessor receipt, and the r6 source bytes; then it creates a fresh
schema/contract/transition/audit quartet with O_EXCL.  Existing v16r2 or older
receipts are never opened for writing or replaced.

This is a static, zero-credit builder.  It does not create a manifest, outer
receipt, runtime candidate, authority seal, or positive wrapper.
"""

from __future__ import annotations

import argparse
import ast
import copy
import hashlib
import json
import os
from pathlib import Path
import stat
import sys
from typing import Any

sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "deliverables"
BASE = "cm2_round306c79g_true_global_no_producer_consumer"
R9_TAG = "v16r9"

# ---- configuration surface -------------------------------------------------
# Fill these constants after the r6 source regeneration is frozen.  CLI flags
# have precedence and make the builder usable without editing this file.
R9_CONFIG: dict[str, str | None] = {
    "producer": "deliverables/cm2_round306c79g_true_global_no_producer_consumer_v16r2r9_semantic_source.py",
    "consumer": "deliverables/cm2_round306c79g_true_global_no_producer_consumer_independent_verifier_assembler_authority_consumer_v16r2r9_semantic_source.py",
    "launcher": "deliverables/cm2_round306c79g_true_global_no_producer_consumer_cold_launch_v16r2r9_semantic_source.py",
    "supersession": "deliverables/cm2_round306c79g_true_global_no_producer_consumer_v16r2r9_active_predecessor_supersession_receipt_v1.json",
    # The C53 effective checkpoint is intentionally fixed by the upstream
    # audit; it is checked again from the held C53 bytes below.
    "checkpoint": "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab",
}

V16R2 = {
    "schema": OUT / f"{BASE}_schema_v16r2.json",
    "contract": OUT / f"{BASE}_contract_v16r2.json",
    "transition": OUT / f"{BASE}_v16_to_v16r2_static_launch_transition_receipt_v1.json",
    "audit": OUT / f"{BASE}_static_audit_v16r2.json",
}

R9_OUT = {
    "schema": OUT / f"{BASE}_schema_{R9_TAG}.json",
    "contract": OUT / f"{BASE}_contract_{R9_TAG}.json",
    "transition": OUT / f"{BASE}_v16r8_to_{R9_TAG}_static_launch_transition_receipt_v1.json",
    "audit": OUT / f"{BASE}_static_audit_{R9_TAG}.json",
}

C53_AUDIT = OUT / "cm2_round306c53_d02a_pair1_pair_level_successor_independent_audit_v1.json"
C53_AUDIT_OBJECT = "a7bee7e57b6527c7bf9ea7f17966379c62a722fe9ce2ce2009f19f85a5afaa7c"
C53_CHECKPOINT = R9_CONFIG["checkpoint"]
# The C53 audit is a derivation record; the effective checkpoint is committed
# by the predecessor-keyed authority head.  Keep the head path explicit and
# read it through the same no-follow/identity checks as every other input.
C53_HEAD = ROOT / ".cm2-runtime/cm2-global-authority-heads/predecessor-10fb050d30c92b0f2bdcf85a30d28ff670d8efc0b48104b7f04a63c391967b41.seal"
C53_HEAD_OBJECT = "cb90ab914c3b6518384669f42d05df33c21a717596190131c6a0f5683934cbfb"

UNIVERSE_ROWS = 76_832
BASELINE_PUBLIC_UNRESOLVED = 1_148
D02_PENDING = 33_638


class BuildError(RuntimeError):
    pass


def fail(message: str) -> None:
    raise BuildError(message)


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"), allow_nan=False).encode("utf-8")


def read_stable(path: Path) -> bytes:
    flags = os.O_RDONLY | os.O_CLOEXEC | getattr(os, "O_NOFOLLOW", 0)
    fd = os.open(path, flags)
    try:
        before = os.fstat(fd)
        if not stat.S_ISREG(before.st_mode) or before.st_nlink != 1:
            fail(f"not regular/nlink1: {path}")
        chunks: list[bytes] = []
        while True:
            part = os.read(fd, 1 << 20)
            if not part:
                break
            chunks.append(part)
        after = os.fstat(fd)
        named = os.lstat(path)
        ident = lambda st: (st.st_dev, st.st_ino, st.st_size,
                            st.st_mtime_ns, st.st_ctime_ns, st.st_nlink)
        if ident(before) != ident(after) or ident(before) != ident(named):
            fail(f"identity drift: {path}")
        raw = b"".join(chunks)
        if len(raw) != before.st_size:
            fail(f"short read: {path}")
        return raw
    finally:
        os.close(fd)


def read_json(path: Path) -> tuple[dict[str, Any], bytes]:
    raw = read_stable(path)
    try:
        value = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise BuildError(f"invalid JSON: {path}") from exc
    if not isinstance(value, dict):
        fail(f"JSON root is not object: {path}")
    return value, raw


def close_object(value: dict[str, Any]) -> dict[str, Any]:
    out = copy.deepcopy(value)
    out.pop("object_sha256", None)
    out["object_sha256"] = sha(canonical(out))
    return out


def verify_object(value: dict[str, Any], label: str) -> None:
    claim = value.get("object_sha256")
    body = dict(value)
    body.pop("object_sha256", None)
    if not isinstance(claim, str) or claim != sha(canonical(body)):
        fail(f"{label}: object closure")


def walk(value: Any):
    yield value
    if isinstance(value, dict):
        for child in value.values():
            yield from walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk(child)


def json_bytes(value: Any) -> bytes:
    return canonical(value) + b"\n"


def install_o_excl(path: Path, raw: bytes) -> str:
    """Install a frozen 0444 file, or replay identical bytes only."""
    try:
        fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL |
                     os.O_CLOEXEC, 0o444)
    except FileExistsError:
        old = read_stable(path)
        st = os.stat(path, follow_symlinks=False)
        if old != raw or stat.S_IMODE(st.st_mode) != 0o444 or st.st_nlink != 1:
            fail(f"append-only target mismatch/not frozen: {path}")
        return "replayed"
    try:
        view = memoryview(raw)
        offset = 0
        while offset < len(view):
            offset += os.write(fd, view[offset:])
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


def cfg_from_args(args: argparse.Namespace) -> dict[str, str | None]:
    cfg = dict(R9_CONFIG)
    for key in ("producer", "consumer", "launcher", "supersession", "checkpoint"):
        value = getattr(args, key)
        if value:
            cfg[key] = value
    return cfg


def resolve_config(cfg: dict[str, str | None]) -> dict[str, Path | str]:
    missing = [key for key in ("producer", "consumer", "launcher", "supersession")
               if not cfg.get(key)]
    if missing:
        fail("r6 source/supersession names not configured: " + ",".join(missing))
    checkpoint = cfg.get("checkpoint")
    if not isinstance(checkpoint, str) or len(checkpoint) != 64:
        fail("r6 checkpoint must be 64 hex characters")
    try:
        int(checkpoint, 16)
    except ValueError as exc:
        raise BuildError("r6 checkpoint is not hex") from exc
    resolved: dict[str, Path | str] = {"checkpoint": checkpoint}
    for key in ("producer", "consumer", "launcher", "supersession"):
        raw = Path(str(cfg[key]))
        path = raw if raw.is_absolute() else ROOT / raw
        if not path.is_file():
            fail(f"configured {key} does not exist: {path}")
        resolved[key] = path
    return resolved


def active_paths(cfg: dict[str, Path | str]) -> dict[str, str]:
    checkpoint = str(cfg["checkpoint"])
    pred = str(Path(str(cfg["supersession"])).relative_to(ROOT))
    producer = str(Path(str(cfg["producer"])).relative_to(ROOT))
    consumer = str(Path(str(cfg["consumer"])).relative_to(ROOT))
    launcher = str(Path(str(cfg["launcher"])).relative_to(ROOT))
    schema = str(R9_OUT["schema"].relative_to(ROOT))
    contract = str(R9_OUT["contract"].relative_to(ROOT))
    transition = str(R9_OUT["transition"].relative_to(ROOT))
    audit = str(R9_OUT["audit"].relative_to(ROOT))
    manifest = str((OUT / f"{BASE}_cold_launch_manifest_{R9_TAG}.sha256").relative_to(ROOT))
    outer = str((OUT / f"{BASE}_cold_launch_outer_receipt_{R9_TAG}.json").relative_to(ROOT))
    return {
        "checkpoint": checkpoint, "predecessor_supersession": pred,
        "schema": schema, "contract": contract, "producer": producer,
        "consumer": consumer, "transition": transition, "audit": audit,
        "launcher": launcher, "manifest": manifest, "outer": outer,
        "candidate_A": f".cm2-runtime/c79g-{R9_TAG}-candidate-a-{checkpoint}",
        "candidate_B": f".cm2-runtime/c79g-{R9_TAG}-candidate-b-{checkpoint}",
        "verification_A": f".cm2-runtime/c79g-{R9_TAG}-verification-a-{checkpoint}",
        "verification_B": f".cm2-runtime/c79g-{R9_TAG}-verification-b-{checkpoint}",
        "committed_completion": f".cm2-runtime/c79g-{R9_TAG}-committed-completion-{checkpoint}",
        "rejection_namespace": f".cm2-runtime/c79g-{R9_TAG}-rejections-{checkpoint}",
        "later_rejection": f".cm2-runtime/c79g-{R9_TAG}-rejections-{checkpoint}/rejection.json",
        "authority_seal": f".cm2-runtime/cm2-global-authority-heads/c79g-{R9_TAG}-{checkpoint}.seal",
    }


def ordered_paths(paths: dict[str, str]) -> tuple[list[str], list[str], list[str]]:
    base7 = [paths[k] for k in ("predecessor_supersession", "schema",
                                "contract", "producer", "consumer",
                                "transition", "audit")]
    exact8 = base7 + [paths["launcher"]]
    exact10 = exact8 + [paths["manifest"], paths["outer"]]
    return base7, exact8, exact10


def source_hashes(cfg: dict[str, Path | str]) -> dict[str, str]:
    result: dict[str, str] = {}
    for role in ("producer", "consumer", "launcher"):
        path = cfg[role]
        raw = read_stable(path)  # type: ignore[arg-type]
        try:
            ast.parse(raw.decode("utf-8"), filename=str(path))
        except (UnicodeDecodeError, SyntaxError) as exc:
            raise BuildError(f"r6 {role} source is not parseable: {path}") from exc
        result[role] = sha(raw)
    return result


def validate_source_path_graph(cfg: dict[str, Path | str],
                               paths: dict[str, str]) -> None:
    """Require each source's active path literals to name this JSON quartet.

    Source bytes are allowed to retain historical evidence, but their active
    constructor/consumer path graph cannot point at a predecessor quartet.
    This check is intentionally textual only after AST parsing in
    ``source_hashes``; it never imports or executes a protocol source.
    """
    required_common = (paths["schema"], paths["contract"], paths["transition"],
                       paths["audit"], paths["manifest"], paths["outer"])
    required_by_role = {
        "producer": required_common + (paths["producer"], paths["consumer"],
                                        paths["launcher"]),
        "consumer": required_common + (paths["producer"], paths["consumer"],
                                        paths["launcher"]),
        "launcher": required_common + (paths["producer"], paths["consumer"],
                                        paths["launcher"]),
    }
    missing: dict[str, list[str]] = {}
    for role in ("producer", "consumer", "launcher"):
        raw = read_stable(cfg[role])  # type: ignore[arg-type]
        text = raw.decode("utf-8")
        # ``OUT / basename`` is the canonical source spelling; accept that
        # form alongside a fully-qualified ``deliverables/basename`` literal.
        absent = [item for item in required_by_role[role]
                  if item not in text and Path(item).name not in text]
        if absent:
            missing[role] = absent
    if missing:
        fail("r6 source active path graph does not bind generated quartet: "
             + json.dumps(missing, sort_keys=True))


def validate_old_inputs() -> tuple[dict[str, Any], dict[str, bytes], dict[str, Any]]:
    values: dict[str, Any] = {}
    raws: dict[str, bytes] = {}
    for key, path in V16R2.items():
        value, raw = read_json(path)
        values[key], raws[key] = value, raw
    for key in ("contract", "transition", "audit"):
        verify_object(values[key], "v16r2 " + key)
    schema = values["schema"]
    if schema.get("$ref") != "#/$defs/coldLaunchedCommittedAuthority":
        fail("v16r2 schema root ref")
    defs = schema.get("$defs")
    if not isinstance(defs, dict) or len(defs) != 46:
        fail("v16r2 schema defs != 46")
    refs = sum(1 for node in walk(schema)
               if isinstance(node, dict) and "$ref" in node)
    closed = sum(1 for node in walk(schema)
                 if isinstance(node, dict) and node.get("additionalProperties") is False)
    if (refs, closed) != (242, 52):
        fail(f"v16r2 schema shape refs={refs},closed={closed}")
    if (len(values["contract"]), len(values["transition"]), len(values["audit"])) != (30, 31, 30):
        fail("v16r2 top-level shape drift")
    return values, raws, {"defs": len(defs), "refs": refs, "closed_objects": closed}


def validate_c53(checkpoint: str) -> dict[str, Any]:
    value, raw = read_json(C53_AUDIT)
    verify_object(value, "C53 audit")
    if value.get("object_sha256") != C53_AUDIT_OBJECT:
        fail("C53 audit object pin")
    # C53's effective checkpoint is the only permitted r6 checkpoint source.
    # It appears inside effective_post_seal_checkpoint in the audit, while
    # the predecessor-keyed head repeats it as the committed semantic value.
    derivation = value.get("post_seal_promotion_derivation")
    if not isinstance(derivation, dict):
        fail("C53 post_seal_promotion_derivation missing")
    effective_state = derivation.get("effective_post_seal_checkpoint")
    if not isinstance(effective_state, dict):
        fail("C53 effective_post_seal_checkpoint missing")
    effective = effective_state.get("effective_checkpoint_object_sha256")
    if effective != checkpoint:
        fail(f"C53 audit checkpoint mismatch: {effective!r} != {checkpoint!r}")
    head, head_raw = read_json(C53_HEAD)
    # Authority-head receipts use authority_seal_object_sha256 (rather than
    # the ordinary object_sha256 field) for their canonical body closure.
    head_claim = head.get("authority_seal_object_sha256")
    head_body = dict(head)
    head_body.pop("authority_seal_object_sha256", None)
    if head_claim != sha(canonical(head_body)):
        fail("C53 authority head: object closure")
    if head_claim != C53_HEAD_OBJECT:
        fail("C53 authority head object pin")
    head_effective = head.get("post_seal_effective_checkpoint_object_sha256")
    if head_effective != checkpoint:
        fail(f"C53 head checkpoint mismatch: {head_effective!r} != {checkpoint!r}")
    if head.get("independent_audit_object_sha256") != C53_AUDIT_OBJECT:
        fail("C53 authority head does not bind the pinned audit")
    return {"file_sha256": sha(raw), "object_sha256": value["object_sha256"],
            "effective_checkpoint_object_sha256": effective,
            "head_path": str(C53_HEAD.relative_to(ROOT)),
            "head_file_sha256": sha(head_raw),
            "head_object_sha256": head_claim}


def validate_predecessor_anchor(value: dict[str, Any], raw: bytes,
                                checkpoint: str) -> dict[str, Any]:
    """Validate the active supersession anchor as a predecessor graph node.

    A merely closed zero-credit rejection is not enough: the active anchor
    must bind the C53 checkpoint and the immediately previous frozen receipt.
    All referenced bytes are read through the stable no-follow reader, and
    mismatches fail before any r6 output is considered for installation.
    """
    verify_object(value, "r6 predecessor supersession")
    if value.get("formal_global_closure_credit") not in (None, 0) or value.get("D02_unlock") is True:
        fail("r6 predecessor supersession is not zero-credit")
    if value.get("append_only") is not True or value.get("runtime_authorized") is not False:
        fail("r6 predecessor supersession is not append-only/fail-closed")
    upstream = value.get("upstream_checkpoint_object_sha256")
    if upstream != checkpoint:
        fail(f"r6 predecessor upstream checkpoint mismatch: {upstream!r} != {checkpoint!r}")
    successor = value.get("successor_checkpoint_object_sha256")
    if not isinstance(successor, str) or len(successor) != 64:
        fail("r6 predecessor successor checkpoint missing")
    try:
        int(successor, 16)
    except ValueError as exc:
        raise BuildError("r6 predecessor successor checkpoint is not hex") from exc
    # If the anchor exposes a previous supersession pin, bind it to the bytes
    # it names.  This is required for the generated active predecessor receipt
    # but remains explicit enough to support future receipt schema revisions.
    prior_path_text = value.get("predecessor_supersession_path")
    prior_file_pin = value.get("predecessor_supersession_file_sha256")
    prior_obj_pin = value.get("predecessor_supersession_object_sha256")
    if not (isinstance(prior_path_text, str) and isinstance(prior_file_pin, str)
            and isinstance(prior_obj_pin, str)):
        fail("r6 predecessor prior supersession binding incomplete")
    prior_path = ROOT / prior_path_text if not Path(prior_path_text).is_absolute() else Path(prior_path_text)
    prior_value, prior_raw = read_json(prior_path)
    verify_object(prior_value, "r6 predecessor prior supersession")
    if sha(prior_raw) != prior_file_pin or prior_value.get("object_sha256") != prior_obj_pin:
        fail("r6 predecessor prior supersession pin mismatch")
    frozen_path_text = value.get("frozen_v16_semantic_supersession_path")
    frozen_file_pin = value.get("frozen_v16_semantic_supersession_file_sha256")
    frozen_obj_pin = value.get("frozen_v16_semantic_supersession_object_sha256")
    if frozen_path_text is not None or frozen_file_pin is not None or frozen_obj_pin is not None:
        if not (isinstance(frozen_path_text, str) and isinstance(frozen_file_pin, str)
                and isinstance(frozen_obj_pin, str)):
            fail("r6 predecessor frozen v16 supersession binding incomplete")
        frozen_path = ROOT / frozen_path_text if not Path(frozen_path_text).is_absolute() else Path(frozen_path_text)
        frozen_value, frozen_raw = read_json(frozen_path)
        verify_object(frozen_value, "r6 predecessor frozen v16 supersession")
        if sha(frozen_raw) != frozen_file_pin or frozen_value.get("object_sha256") != frozen_obj_pin:
            fail("r6 predecessor frozen v16 supersession pin mismatch")
    return {
        "file_sha256": sha(raw),
        "object_sha256": value["object_sha256"],
        "upstream_checkpoint_object_sha256": upstream,
        "successor_checkpoint_object_sha256": successor,
        "predecessor_namespace": value.get("predecessor_namespace"),
        "successor_namespace": value.get("successor_namespace"),
    }


def make_schema(old: dict[str, Any], paths: dict[str, str],
                source: dict[str, str], checkpoint: str,
                predecessor_object: str) -> dict[str, Any]:
    schema = copy.deepcopy(old)
    old_field = "current_exact8_first_member_is_v14_registry_shape_drift_supersession_receipt"
    new_field = "current_exact8_first_member_is_r9_semantic_supersession_receipt"
    for definition_name in ("coldLaunchProof", "staticFreezeProof"):
        definition = schema["$defs"][definition_name]
        if old_field not in definition["properties"]:
            fail(f"missing v14 active field in {definition_name}")
        definition["properties"][new_field] = definition["properties"].pop(old_field)
        definition["required"] = [new_field if key == old_field else key
                                   for key in definition["required"]]
    schema["$id"] = "cm2.round306c79g.true-global-no-producer-consumer.v16r9.schema"
    schema["title"] = "C79g v16r9 full-shape zero-credit schema"
    schema["description"] = (
        "Append-only r9 schema.  The active exact8 starts with the configured "
        "recent predecessor supersession receipt; all persisted credit and "
        "runtime authority remain disabled.")
    schema["x-cm2-v16r9-active-successor"] = {
        "namespace": "v16r9-semantic-bundle",
        "effective_checkpoint_object_sha256": checkpoint,
        "active_exact8_first_member_field": new_field,
        "active_exact8_first_member_path": paths["predecessor_supersession"],
        "active_successor_paths": paths,
        "source_hashes": source,
        "predecessor_supersession_object_sha256": predecessor_object,
        "full_shape_counts": {
            "schema_defs": 46,
            "schema_refs": 242,
            "closed_objects": 52,
        },
        "formal_global_closure_credit": 0,
        "D02_unlock": False,
        "runtime_authorized": False,
    }
    return schema


def make_bundle(old_bundle: dict[str, Any], paths: dict[str, str],
                source: dict[str, str], schema_hash: str,
                checkpoint: str, c53: dict[str, Any],
                predecessor_object: str) -> dict[str, Any]:
    base7, exact8, exact10 = ordered_paths(paths)
    bundle = copy.deepcopy(old_bundle)
    bundle.update({
        "bundle_version": R9_TAG,
        "base7_ordered_paths": base7,
        "exact8_ordered_paths": exact8,
        "exact10_ordered_paths": exact10,
        "source_hashes": source,
        "schema_file_sha256": schema_hash,
        "closed_schema": {"path": paths["schema"], "file_sha256": schema_hash},
        "contract": {
            "path": paths["contract"],
            "object_pin_source": "THIS_CONTRACT_TOP_LEVEL_OBJECT_SHA256__DO_NOT_DUPLICATE_SELF_HASH_INSIDE_HASHED_BODY",
        },
        "build_only_producer": {
            "path": paths["producer"],
            "role": "BUILD_ONLY__R9_SOURCE_CANDIDATE__ZERO_CREDIT",
            "source_template_only": True,
        },
        "independent_verifier_assembler_authority_consumer": {
            "path": paths["consumer"],
            "role": "NO_PRODUCER__R9_SOURCE_CANDIDATE__ZERO_CREDIT",
            "source_template_only": False,
            "runtime_authorized": False,
        },
        "cold_launch_outer_closure": {
            "launcher_path": paths["launcher"],
            "exact8_manifest_path": paths["manifest"],
            "outer_last_path": paths["outer"],
            "manifest_or_outer_absent_in_this_static_phase": True,
            "runtime_entry_authorized": False,
            "all_cold_launch_persisted_credit": 0,
            "all_cold_launch_persisted_D02_unlock": False,
        },
        "post_source_static_trust_receipts": {
            "predecessor_supersession_path": paths["predecessor_supersession"],
            "predecessor_supersession_object_sha256": predecessor_object,
            "c53_checkpoint_audit_file_sha256": c53["file_sha256"],
            "c53_checkpoint_object_sha256": c53["object_sha256"],
            "static_audit_path": paths["audit"],
            "transition_path": paths["transition"],
            "binding_direction": "R9_SOURCE_READS_POST_SOURCE_RECEIPTS__NO_HASH_CYCLE",
        },
        "contract_file_sha256": "UNPINNED_R9_CONTRACT_FILE",
        "contract_object_sha256": "UNPINNED_R9_CONTRACT_OBJECT",
        "transition_file_sha256": "UNPINNED_R9_TRANSITION_FILE",
        "transition_object_sha256": "UNPINNED_R9_TRANSITION_OBJECT",
        "audit_file_sha256": "UNPINNED_R9_AUDIT_FILE",
        "pin_state": "R9_SOURCE_AND_JSON_PINS_UNINSTALLED__STATIC_ZERO_CREDIT",
        "formal_global_closure_credit": 0,
        "D02_unlock": False,
        "runtime_authorized": False,
        "effective_checkpoint_object_sha256": checkpoint,
        "predecessor_supersession_object_sha256": predecessor_object,
    })
    return bundle


def make_contract(old: dict[str, Any], bundle: dict[str, Any],
                  checkpoint: str) -> dict[str, Any]:
    out = copy.deepcopy(old)
    out.pop("v16r2_bundle", None)
    out["v16r9_bundle"] = bundle
    out["schema"] = "cm2.round306c79g.true-global-no-producer-consumer.v16r9.contract"
    out["status"] = "R9_STATIC_CONTRACT_DRAFT__ZERO_CREDIT__RUNTIME_NOT_AUTHORIZED"
    out["effective_checkpoint_object_sha256"] = checkpoint
    out["purpose"] = (
        "Append-only r9 semantic bundle with predecessor→schema→contract→"
        "producer→consumer→transition→audit→launcher exact8 order; no credit transfer.")
    out["credit_boundary"] = copy.deepcopy(out.get("credit_boundary", {}))
    for key in list(out["credit_boundary"]):
        if "formal_global_closure_credit" in key:
            out["credit_boundary"][key] = 0
        if key == "D02_unlock":
            out["credit_boundary"][key] = False
    return close_object(out)


def make_transition(old: dict[str, Any], bundle: dict[str, Any],
                    paths: dict[str, str], checkpoint: str) -> dict[str, Any]:
    out = copy.deepcopy(old)
    out.pop("successor_v16r2_static_bundle", None)
    out["successor_v16r9_static_bundle"] = bundle
    out["schema"] = "cm2.round306c79g.true-global-no-producer-consumer.v16r8-to-v16r9.transition"
    out["status"] = "R9_STATIC_TRANSITION_DRAFT__ZERO_CREDIT__RUNTIME_NOT_AUTHORIZED"
    out["receipt_path"] = paths["transition"]
    out["effective_checkpoint_object_sha256"] = checkpoint
    out["transition_kind"] = "APPEND_ONLY_V16R8_TO_V16R9_ZERO_CREDIT_JSON_BUNDLE"
    boundary = copy.deepcopy(out.get("cold_launch_boundary", {}))
    boundary.pop("base7_first_member_is_v14_registry_shape_drift_supersession_receipt", None)
    boundary["base7_first_member_is_r9_semantic_supersession"] = True
    boundary["base7_first_member_path"] = paths["predecessor_supersession"]
    boundary["base7_order"] = bundle["base7_ordered_paths"]
    boundary["launcher_is_eighth"] = True
    boundary["manifest_is_ninth"] = True
    boundary["outer_is_tenth_and_last"] = True
    boundary["manifest_or_outer_exists_at_transition_time"] = False
    boundary["manifest_or_outer_created_by_this_transition"] = False
    boundary["runtime_entry_authorized_by_this_transition"] = False
    out["cold_launch_boundary"] = boundary
    out["finalization_gates"] = {
        "final_core_pins_installed_before_object_closure": False,
        "final_independent_static_audit_A_GO": False,
        "final_independent_static_audit_B_GO": False,
        "cold_launcher_final_pin_instance_generated": False,
        "ordered_exact8_manifest_created": False,
        "outer_receipt_created_last": False,
        "terminal_byte_replay_completed": False,
    }
    for key in ("all_persisted_credit", "formal_global_closure_credit",
                "D02_gate_credit", "D02_task_credit",
                "C79_runtime_artifacts_created"):
        out[key] = 0
    out["D02_unlock"] = False
    out["D02_started"] = False
    out["D02_formal_pending_task_count"] = D02_PENDING
    out["runtime_executed_during_transition"] = False
    return close_object(out)


def make_audit(old: dict[str, Any], bundle: dict[str, Any],
               paths: dict[str, str], checkpoint: str,
               c53: dict[str, Any]) -> dict[str, Any]:
    out = copy.deepcopy(old)
    out.pop("audited_v16r2_bundle", None)
    out["audited_v16r9_bundle"] = bundle
    out["schema"] = "cm2.round306c79g.true-global-no-producer-consumer.static-audit-v16r9"
    out["status"] = "R9_STATIC_AUDIT_DRAFT__ZERO_CREDIT__RUNTIME_NOT_AUTHORIZED"
    out["audit_path"] = paths["audit"]
    out["effective_checkpoint_object_sha256"] = checkpoint
    checkers = copy.deepcopy(out.get("dual_independent_static_checkers", {}))
    for role in ("checker_A", "checker_B"):
        checkers.setdefault(role, {})["status"] = "NOT_RUN_R9_SOURCE_REVIEW"
        checkers[role]["failed_static_check_count"] = 1
    checkers["all_pin_normalizers_equal"] = False
    checkers["all_common_callsite_censuses_equal"] = False
    checkers["runtime_not_authorized"] = True
    out["dual_independent_static_checkers"] = checkers
    closure = copy.deepcopy(out.get("schema_and_constructor_closure", {}))
    closure.update({
        "schema_definition_count": 46,
        "schema_ref_count": 242,
        "closed_object_count": 52,
        "closed_object_required_property_mismatch_count": 0,
        "all_schema_refs_resolve": True,
        "active_exact8_first_member_schema_field_aligned": True,
        "source_template_shape_review_pending": True,
        # Keep the baseline inside an existing closed nested object so the
        # audit's required 30-key top-level shape remains unchanged.
        "global_consumer_baseline": {
            "input_rows": UNIVERSE_ROWS,
            "current_public_unresolved": BASELINE_PUBLIC_UNRESOLVED,
            "formal_global_closure_credit": 0,
            "D02_unlock": False,
            "c53_checkpoint_object_sha256": c53["object_sha256"],
            "c53_effective_checkpoint_object_sha256": c53["effective_checkpoint_object_sha256"],
            "c53_head_object_sha256": c53["head_object_sha256"],
            "prospective_consumer_not_authorized": True,
        },
    })
    out["schema_and_constructor_closure"] = closure
    out["static_credit_census"] = {
        "all_persisted_r9_objects_D02_started": False,
        "all_persisted_r9_objects_D02_unlock": False,
        "all_persisted_r9_objects_formal_global_closure_credit": 0,
        "cold_live_inner_formal_global_closure_credit": 0,
        "launcher_virtual_positive_root_exact_credit_literal_count": 0,
        "only_cold_launcher_fresh_virtual_wrapper_may_derive_credit_one": True,
    }
    out["final_audit_acceptance"] = {
        "current_draft_pass": False,
        "final_failed_static_check_count_required": 0,
        "final_static_freeze_pass_required": True,
        "dual_static_checker_A_pin_normalized_ast_GO": False,
        "dual_static_checker_B_pin_normalized_ast_GO": False,
        "pin_normalized_launcher_ast_digest_consensus": False,
        "common_callsite_census_digest_consensus": False,
        "final_launcher_pin_normalized_ast_replay_required_after_pin_injection": True,
        "this_audit_authorizes_C79_runtime": False,
        "requires_cold_exact8_freeze_manifest_then_outer_last_and_terminal_replay": True,
    }
    return close_object(out)


def ensure_zero_credit(value: Any, label: str) -> None:
    for node in walk(value):
        if isinstance(node, dict):
            if node.get("formal_global_closure_credit") not in (None, 0):
                fail(label + ": nonzero formal credit")
            if node.get("D02_unlock") is True:
                fail(label + ": D02 unlock true")


def validate_shapes(schema: dict[str, Any], contract: dict[str, Any],
                    transition: dict[str, Any], audit: dict[str, Any],
                    paths: dict[str, str]) -> dict[str, int]:
    defs = schema.get("$defs", {})
    refs = sum(1 for n in walk(schema) if isinstance(n, dict) and "$ref" in n)
    closed = sum(1 for n in walk(schema)
                 if isinstance(n, dict) and n.get("additionalProperties") is False)
    if (len(defs), refs, closed) != (46, 242, 52):
        fail(f"r6 schema shape {(len(defs), refs, closed)}")
    if (len(contract), len(transition), len(audit)) != (30, 31, 30):
        fail("r6 top-level shape must be 30/31/30")
    new_field = "current_exact8_first_member_is_r9_semantic_supersession_receipt"
    for name in ("coldLaunchProof", "staticFreezeProof"):
        d = defs[name]
        if new_field not in d.get("properties", {}) or new_field not in d.get("required", []):
            fail(f"r6 schema active field missing: {name}")
        if set(d.get("properties", {})) != set(d.get("required", [])):
            fail(f"r6 schema closed shape mismatch: {name}")
    for value, label in ((contract, "contract"), (transition, "transition"), (audit, "audit")):
        verify_object(value, label)
        ensure_zero_credit(value, label)
    for key in ("v16r9_bundle", "successor_v16r9_static_bundle", "audited_v16r9_bundle"):
        found = [value for value in (contract, transition, audit) if key in value]
        if found and found[0].get(key, {}).get("exact8_ordered_paths", [None])[0] != paths["predecessor_supersession"]:
            fail(key + ": exact8 predecessor mismatch")
    return {"schema_defs": len(defs), "schema_refs": refs,
            "closed_objects": closed, "contract_keys": len(contract),
            "transition_keys": len(transition), "audit_keys": len(audit)}


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--producer")
    p.add_argument("--consumer")
    p.add_argument("--launcher")
    p.add_argument("--supersession")
    p.add_argument("--checkpoint")
    p.add_argument("--dry-run", action="store_true",
                    help="validate and render prospective bytes without installing files")
    return p


def main(argv: list[str] | None = None) -> int:
    try:
        args = parser().parse_args(argv)
        cfg = resolve_config(cfg_from_args(args))
        values, raws, old_shape = validate_old_inputs()
        c53 = validate_c53(str(cfg["checkpoint"]))
        predecessor, predecessor_raw = read_json(cfg["supersession"])  # type: ignore[arg-type]
        predecessor_report = validate_predecessor_anchor(
            predecessor, predecessor_raw, str(cfg["checkpoint"]))
        source = source_hashes(cfg)
        paths = active_paths(cfg)
        validate_source_path_graph(cfg, paths)
        schema = make_schema(values["schema"], paths, source,
                             str(cfg["checkpoint"]), predecessor["object_sha256"])
        schema_raw = json_bytes(schema)
        schema_hash = sha(schema_raw)
        old_bundle = values["contract"].get("v16r2_bundle")
        if not isinstance(old_bundle, dict):
            fail("v16r2 contract bundle missing")
        bundle = make_bundle(old_bundle, paths, source, schema_hash,
                             str(cfg["checkpoint"]), c53,
                             predecessor["object_sha256"])
        contract = make_contract(values["contract"], bundle,
                                 str(cfg["checkpoint"]))
        transition = make_transition(values["transition"], bundle, paths,
                                     str(cfg["checkpoint"]))
        audit = make_audit(values["audit"], bundle, paths,
                           str(cfg["checkpoint"]), c53)
        # Leave cross-file hashes explicitly unpinned to avoid a contract ↔
        # transition ↔ audit cycle.  Top-level object closures are complete.
        shape = validate_shapes(schema, contract, transition, audit, paths)
        outputs = {
            "schema": (R9_OUT["schema"], schema_raw),
            "contract": (R9_OUT["contract"], json_bytes(contract)),
            "transition": (R9_OUT["transition"], json_bytes(transition)),
            "audit": (R9_OUT["audit"], json_bytes(audit)),
        }
        if args.dry_run:
            installed = {key: "dry-run" for key in outputs}
            hashes = {key: sha(raw) for key, (_, raw) in outputs.items()}
        else:
            installed = {key: install_o_excl(path, raw)
                         for key, (path, raw) in outputs.items()}
            hashes = {key: sha(read_stable(path)) for key, (path, _) in outputs.items()}
        report = {
            "schema": "cm2.c79g.v16r9.json-bundle-builder.result.v1",
            "status": ("R9_JSON_BUNDLE_DRY_RUN_PASS__ZERO_CREDIT__RUNTIME_NOT_AUTHORIZED"
                       if args.dry_run else
                       "R9_JSON_BUNDLE_DRAFT_INSTALLED__ZERO_CREDIT__RUNTIME_NOT_AUTHORIZED"),
            "effective_checkpoint_object_sha256": cfg["checkpoint"],
            "c53": c53,
            "predecessor_supersession": {
                "path": paths["predecessor_supersession"],
                **predecessor_report,
            },
            "active_paths": paths,
            "source_hashes": source,
            "shape": {**shape, "old_v16r2_shape": old_shape,
                      "baseline_rows": UNIVERSE_ROWS,
                      "baseline_public_unresolved": BASELINE_PUBLIC_UNRESOLVED},
            "file_hashes": hashes,
            "installed": installed,
            "formal_global_closure_credit": 0,
            "D02_unlock": False,
            "D02_started": False,
            "D02_formal_pending_task_count": D02_PENDING,
            "manifest_created": False,
            "outer_created": False,
            "runtime_authorized": False,
            "reviewer_implications": {
                "exact8_order": "predecessor_supersession->schema->contract->r9_producer->r9_consumer->transition->audit->launcher",
                "source_review_34_of_34": False,
                "dual_pin_normalized_ast_consensus": False,
                "cold_attack_137_required": True,
                "positive_wrapper_required_for_credit_one": True,
            },
            "writes": {"old_outputs": False, "r9_outputs": not args.dry_run,
                        "manifest": False,
                        "outer": False, "runtime": False, "credit": False,
                        "pyc": False},
        }
        print(json.dumps(report, ensure_ascii=True, sort_keys=True))
        return 0
    except (BuildError, OSError, ValueError, KeyError, TypeError, SyntaxError) as exc:
        print(json.dumps({
            "schema": "cm2.c79g.v16r9.json-bundle-builder.failure.v1",
            "status": "FAIL_CLOSED_R9_JSON_BUILDER",
            "error_type": type(exc).__name__,
            "error": str(exc),
            "formal_global_closure_credit": 0,
            "D02_unlock": False,
            "runtime_authorized": False,
            "writes": False,
        }, ensure_ascii=True, sort_keys=True))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
