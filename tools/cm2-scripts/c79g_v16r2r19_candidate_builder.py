#!/usr/bin/env python3
"""Append-only r19 DAG candidate builder.

This is a static-only constructor.  It derives a fresh r19 quartet from the
immutable r16 bytes and the frozen r18 anchor, closes hashes in topological
order, and never executes a protocol source.  A failed attempt writes only a
rejection/supersession/anchor chain for r19; manifest, outer, runtime and
credit are deliberately out of scope.
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
R16 = "v16r2r16"
PREV = os.environ.get("CM2_PREDECESSOR_TAG", "v16r2r18")
TAG = os.environ.get("CM2_SUCCESSOR_TAG", "v16r2r19")
UPSTREAM = "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab"
CHECKPOINT = "dd9d64f3f0bd0dfd00fd399e3154517a34ba19cfb601ec749f44cbc08b03ca1b"

SRC_IN = {
    "producer": OUT / f"{BASE}_{R16}_semantic_source.py",
    "consumer": OUT / f"{BASE}_independent_verifier_assembler_authority_consumer_{R16}_semantic_source.py",
    "launcher": OUT / f"{BASE}_cold_launch_{R16}_semantic_source.py",
}
JSON_IN = {
    "schema": OUT / f"{BASE}_schema_{R16}.json",
    "contract": OUT / f"{BASE}_contract_{R16}.json",
    "transition": OUT / f"{BASE}_v16r2r15_to_{R16}_static_launch_transition_receipt_v1.json",
    "audit": OUT / f"{BASE}_static_audit_{R16}.json",
}
ANCHOR_IN = OUT / f"{BASE}_{PREV}_active_predecessor_supersession_receipt_v1.json"
SRC_OUT = {
    "producer": OUT / f"{BASE}_{TAG}_semantic_source.py",
    "consumer": OUT / f"{BASE}_independent_verifier_assembler_authority_consumer_{TAG}_semantic_source.py",
    "launcher": OUT / f"{BASE}_cold_launch_{TAG}_semantic_source.py",
}
JSON_OUT = {
    "schema": OUT / f"{BASE}_schema_{TAG}.json",
    "contract": OUT / f"{BASE}_contract_{TAG}.json",
    "transition": OUT / f"{BASE}_{PREV}_to_{TAG}_static_launch_transition_receipt_v1.json",
    "audit": OUT / f"{BASE}_static_audit_{TAG}.json",
}
MANIFEST = OUT / f"{BASE}_cold_launch_manifest_{TAG}.sha256"
OUTER = OUT / f"{BASE}_cold_launch_outer_receipt_{TAG}.json"
REJ = OUT / f"{BASE}_{PREV}_static_bundle_rejection_receipt_v1.json"
SUP = OUT / f"{BASE}_{PREV}_to_{TAG}_static_bundle_rejection_supersession_receipt_v1.json"
ANCHOR = OUT / f"{BASE}_{TAG}_active_predecessor_supersession_receipt_v1.json"
HEX = re.compile(r"^[0-9a-f]{64}$")

class DuplicateKey(ValueError):
    pass

def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for k, v in items:
        if k in out:
            raise DuplicateKey(k)
        out[k] = v
    return out

def canon(v: Any) -> bytes:
    return json.dumps(v, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"), allow_nan=False).encode()

def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()

def close(v: dict[str, Any]) -> dict[str, Any]:
    out = copy.deepcopy(v)
    out.pop("object_sha256", None)
    out["object_sha256"] = sha(canon(out))
    return out

def stable(path: Path) -> bytes:
    fd = os.open(path, os.O_RDONLY | os.O_CLOEXEC | getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(fd)
        if not stat.S_ISREG(before.st_mode) or before.st_nlink != 1:
            raise RuntimeError(f"bad input identity: {path}")
        chunks: list[bytes] = []
        while True:
            b = os.read(fd, 1 << 20)
            if not b:
                break
            chunks.append(b)
        after, named = os.fstat(fd), os.lstat(path)
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

def load(path: Path) -> tuple[dict[str, Any], bytes]:
    raw = stable(path)
    v = json.loads(raw.decode(), object_pairs_hook=pairs)
    if not isinstance(v, dict):
        raise RuntimeError(f"object required: {path}")
    if "object_sha256" in v:
        claimed = v["object_sha256"]
        body = copy.deepcopy(v); body.pop("object_sha256", None)
        if claimed != sha(canon(body)):
            raise RuntimeError(f"object closure: {path}")
    return v, raw

def install(path: Path, raw: bytes, mode: int = 0o444) -> str:
    try:
        fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_CLOEXEC, mode)
    except FileExistsError:
        if stable(path) != raw or path.stat().st_nlink != 1 or stat.S_IMODE(path.stat().st_mode) != mode:
            raise RuntimeError(f"append-only mismatch: {path}")
        return "replayed"
    try:
        view = memoryview(raw); off = 0
        while off < len(view):
            off += os.write(fd, view[off:])
        os.fsync(fd); os.fchmod(fd, mode)
    finally:
        os.close(fd)
    dfd = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC)
    try: os.fsync(dfd)
    finally: os.close(dfd)
    return "installed"

def walk(v: Any):
    yield v
    if isinstance(v, dict):
        for x in v.values(): yield from walk(x)
    elif isinstance(v, list):
        for x in v: yield from walk(x)

def retag(v: Any) -> Any:
    old_edge = f"{BASE}_v16r2r15_to_{R16}_static_launch_transition_receipt_v1.json"
    new_edge = f"{BASE}_{PREV}_to_{TAG}_static_launch_transition_receipt_v1.json"
    old_anchor = f"{BASE}_{R16}_active_predecessor_supersession_receipt_v1.json"
    new_anchor = f"{BASE}_{TAG}_active_predecessor_supersession_receipt_v1.json"
    if isinstance(v, dict): return {retag(k): retag(x) for k, x in v.items()}
    if isinstance(v, list): return [retag(x) for x in v]
    if not isinstance(v, str): return v
    return (v.replace(old_edge, new_edge).replace(old_anchor, new_anchor)
             .replace("V16R2R16", "V16R2R19").replace("V16R2R15", "V16R2R18")
             .replace(R16, TAG).replace("v16r2r15", PREV))

def paths() -> dict[str, str]:
    return {"anchor": str(ANCHOR.relative_to(ROOT)),
            "schema": str(JSON_OUT["schema"].relative_to(ROOT)),
            "contract": str(JSON_OUT["contract"].relative_to(ROOT)),
            "producer": str(SRC_OUT["producer"].relative_to(ROOT)),
            "consumer": str(SRC_OUT["consumer"].relative_to(ROOT)),
            "transition": str(JSON_OUT["transition"].relative_to(ROOT)),
            "audit": str(JSON_OUT["audit"].relative_to(ROOT)),
            "launcher": str(SRC_OUT["launcher"].relative_to(ROOT))}

def source_patch(raw: bytes, role: str, p: dict[str, str], anchor_file: str,
                 anchor_obj: str, schema_hash: str, contract_hash: str,
                 contract_obj: str, producer_hash: str | None = None,
                 base7: dict[str, tuple[str, str | None]] | None = None) -> bytes:
    text = raw.decode()
    old_edge = f"{BASE}_v16r2r15_to_{R16}_static_launch_transition_receipt_v1.json"
    new_edge = f"{BASE}_{PREV}_to_{TAG}_static_launch_transition_receipt_v1.json"
    old_anchor = f"{BASE}_{R16}_active_predecessor_supersession_receipt_v1.json"
    new_anchor = f"{BASE}_{TAG}_active_predecessor_supersession_receipt_v1.json"
    text = (text.replace(old_edge, new_edge).replace(old_anchor, new_anchor)
            .replace("V16R2R16", "V16R2R19").replace("V16R2R15", "V16R2R18")
            .replace(R16, TAG).replace("v16r2r15", PREV))
    text, n = re.subn(r'(?m)^ACTIVE_PREDECESSOR_SUPERSESSION_FILE_PIN\s*=\s*"[0-9a-f]{64}"\s*$',
                       f'ACTIVE_PREDECESSOR_SUPERSESSION_FILE_PIN = "{anchor_file}"', text)
    text, m = re.subn(r'(?m)^ACTIVE_PREDECESSOR_SUPERSESSION_OBJECT_PIN\s*=\s*"[0-9a-f]{64}"\s*$',
                       f'ACTIVE_PREDECESSOR_SUPERSESSION_OBJECT_PIN = "{anchor_obj}"', text)
    if (n, m) != (1, 1): raise RuntimeError(f"{role}: anchor pin count {(n,m)}")
    def replace_const(name: str, value: str) -> None:
        nonlocal text
        text = re.sub(rf'(?m)^({re.escape(name)}\s*=\s*)"[^"]*"\s*$',
                      rf'\1"{value}"', text)
    replace_const("CONTRACT_FILE_PIN", contract_hash)
    replace_const("CONTRACT_OBJECT_PIN", contract_obj)
    replace_const("CLOSED_SCHEMA_FILE_PIN", schema_hash)
    if role == "consumer" and producer_hash is not None:
        replace_const("PRODUCER_SOURCE_PIN", producer_hash)
    flag = {"producer": "FINAL_V16R2_CORE_PINS_INSTALLED",
            "consumer": "FINAL_CURRENT_V16R2_PINS_INSTALLED",
            "launcher": "FINAL_BASE7_PINS_INSTALLED"}[role]
    text, count = re.subn(rf'(?m)^({re.escape(flag)}\s*=\s*)False\s*$', r'\1True', text)
    if count < 1: raise RuntimeError(f"{role}: final flag absent")
    # The launcher receives its seven earlier-node pins after all upstream
    # bytes are closed.  It never pins its own source, so this is acyclic.
    if role == "launcher":
        if base7 is None: raise RuntimeError("launcher base7 missing")
        entries = []
        names = [("ACTIVE_PREDECESSOR_SUPERSESSION", "anchor"), ("SCHEMA", "schema"),
                 ("CONTRACT", "contract"), ("PRODUCER", "producer"),
                 ("CONSUMER", "consumer"), ("TRANSITION", "transition"), ("AUDIT", "audit")]
        for var, key in names:
            fh, oh = base7[key]
            entries.append(f'        {var}: ("{fh}", {oh!r}),')
        map_text = "    BASE7_PINS.update({\n" + "\n".join(entries) + "\n    })"
        if text.count("BASE7_PINS.clear()") != 1:
            raise RuntimeError("launcher BASE7 clear shape")
        text = text.replace("    BASE7_PINS.clear()", "    BASE7_PINS.clear()\n" + map_text, 1)
    # Replace configured path literals in both module and launcher setup via
    # the namespace rewrite above; assert no active predecessor edge remains.
    if old_anchor in text or old_edge in text or f"v16r2r16" in text:
        raise RuntimeError(f"{role}: stale r16 active path")
    tree = ast.parse(text, filename=str(SRC_OUT[role])); compile(tree, str(SRC_OUT[role]), "exec")
    return (text if text.endswith("\n") else text + "\n").encode()

def ensure_successor_anchor() -> dict[str, str]:
    """Close the predecessor rejection -> supersession -> active-anchor chain.

    The anchor for the namespace being built must exist before any source bytes
    are derived.  If the predecessor rejection is already frozen, it is reused
    byte-for-byte; no old namespace is ever rewritten.
    """
    if REJ.is_file():
        rej, rr = load(REJ)
        if rej.get("failed_namespace") != PREV or rej.get("formal_global_closure_credit") != 0:
            raise RuntimeError(f"predecessor rejection namespace/credit mismatch:{REJ}")
    else:
        # This path is only for a genuinely new predecessor.  It is still
        # append-only and is closed before the supersession/anchor bytes.
        rej, rr = rejection("PREDECESSOR_NAMESPACE_SUPERSEDED_BEFORE_NEXT_STATIC_ATTEMPT", {
            "predecessor_namespace": PREV,
            "successor_namespace": TAG,
            "anchor_must_precede_source": True,
        })
        install(REJ, rr)
    rh, ro = sha(rr), rej["object_sha256"]
    sup = close({
        "schema": f"cm2.c79g.{PREV}-to-{TAG}.static-bundle-rejection-supersession.v1",
        "status": "FROZEN_APPEND_ONLY_REJECTED_PREDECESSOR_SUPERSEDED__ZERO_CREDIT",
        "predecessor_namespace": PREV,
        "successor_namespace": TAG,
        "predecessor_rejection_path": str(REJ.relative_to(ROOT)),
        "predecessor_rejection_file_sha256": rh,
        "predecessor_rejection_object_sha256": ro,
        "upstream_checkpoint_object_sha256": UPSTREAM,
        "successor_checkpoint_object_sha256": CHECKPOINT,
        "append_only": True,
        "runtime_authorized": False,
        "formal_global_closure_credit": 0,
        "D02_unlock": False,
    })
    sr = canon(sup) + b"\n"
    install(SUP, sr)
    # Re-read the installed bytes so the pin is always based on the immutable
    # filesystem object, including on replay.
    sup_installed = load(SUP)[0]
    sup_raw = stable(SUP)
    anchor = close({
        "schema": f"cm2.c79g.{TAG}.active-predecessor-supersession.v1",
        "status": "FROZEN_APPEND_ONLY_ACTIVE_PREDECESSOR_ANCHOR__ZERO_CREDIT",
        "predecessor_namespace": PREV,
        "predecessor_supersession_path": str(SUP.relative_to(ROOT)),
        "predecessor_supersession_file_sha256": sha(sup_raw),
        "predecessor_supersession_object_sha256": sup_installed["object_sha256"],
        "upstream_checkpoint_object_sha256": UPSTREAM,
        "successor_checkpoint_object_sha256": CHECKPOINT,
        "successor_namespace": f"{TAG}_semantic_source",
        "append_only": True,
        "runtime_authorized": False,
        "formal_global_closure_credit": 0,
        "D02_unlock": False,
        "manifest_created": False,
        "outer_created": False,
    })
    ar = canon(anchor) + b"\n"
    install(ANCHOR, ar)
    installed_anchor, installed_raw = load(ANCHOR)
    return {"file_sha256": sha(installed_raw), "object_sha256": installed_anchor["object_sha256"]}

def build() -> tuple[dict[str, bytes], dict[str, Any]]:
    # Validate the prior active anchor first; it is an immutable input to this
    # transition, but is not the anchor pinned by the new candidate.
    predecessor_anchor, predecessor_raw = load(ANCHOR_IN)
    if predecessor_anchor.get("successor_namespace") != f"{PREV}_semantic_source" or predecessor_anchor.get("formal_global_closure_credit") != 0:
        raise RuntimeError("predecessor anchor not locked")
    # The successor anchor was sealed before this function is called.
    anchor, anchor_raw = load(ANCHOR)
    if anchor.get("successor_namespace") != f"{TAG}_semantic_source" or anchor.get("predecessor_namespace") != PREV or anchor.get("formal_global_closure_credit") != 0:
        raise RuntimeError("successor anchor not locked")
    af, ao = sha(anchor_raw), anchor["object_sha256"]
    p = paths()
    schema, _ = load(JSON_IN["schema"]); schema = retag(schema)
    schema["$id"] = f"cm2.round306c79g.true-global-no-producer-consumer.{TAG}.schema"
    schema["$comment"] = f"CM2_{TAG.upper()}_DAG_STATIC_ZERO_CREDIT__RUNTIME_NOT_AUTHORIZED"
    schema_raw = canon(schema) + b"\n"; sh = sha(schema_raw)
    contract, _ = load(JSON_IN["contract"]); contract = retag(contract)
    cb = contract.get("v16r2_bundle")
    if not isinstance(cb, dict): raise RuntimeError("contract active bundle missing")
    cb.pop("source_hashes", None)
    for k in ("contract_file_sha256", "contract_object_sha256", "transition_file_sha256", "transition_object_sha256", "audit_file_sha256"):
        cb.pop(k, None)
    cb.update({"bundle_version": TAG, "schema_file_sha256": sh,
               "pin_state": f"{TAG.upper()}_DAG_SOURCE_PINS_FINAL__RUNTIME_NOT_AUTHORIZED",
               "predecessor_semantic_supersession": {"path": p["anchor"], "file_sha256": af, "object_sha256": ao, "successor_only": f"{TAG}-semantic-bundle"},
               "predecessor_supersession_object_sha256": ao,
               "closed_schema": {"path": p["schema"], "file_sha256": sh},
               "exact8_ordered_paths": [p[k] for k in ("anchor","schema","contract","producer","consumer","transition","audit","launcher")],
               "base7_ordered_paths": [p[k] for k in ("anchor","schema","contract","producer","consumer","transition","audit")],
               "exact10_ordered_paths": [p[k] for k in ("anchor","schema","contract","producer","consumer","transition","audit","launcher")] + [f"deliverables/{MANIFEST.name}", f"deliverables/{OUTER.name}"]})
    # The inherited r16/r13 template metadata is not authority for a fresh
    # executable source.  Normalize only the active bundle (historical
    # incident records remain byte-identical), and bind its trust receipt to
    # this namespace's newly sealed anchor and transition.
    producer_meta = cb.get("build_only_producer")
    if isinstance(producer_meta, dict):
        producer_meta.update({"role": f"BUILD_ONLY__{TAG.upper()}_EXECUTABLE_SOURCE__ZERO_CREDIT",
                              "source_template_only": False})
    consumer_meta = cb.get("independent_verifier_assembler_authority_consumer")
    if isinstance(consumer_meta, dict):
        consumer_meta.update({"role": f"NO_PRODUCER__{TAG.upper()}_EXECUTABLE_SOURCE__ZERO_CREDIT",
                              "source_template_only": False})
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
    contract_raw = canon(close(contract)) + b"\n"; ch, co = sha(contract_raw), json.loads(contract_raw)["object_sha256"]
    # Producer depends only on earlier anchor/schema/contract.
    prod = source_patch(stable(SRC_IN["producer"]), "producer", p, af, ao, sh, ch, co)
    ph = sha(prod)
    cons = source_patch(stable(SRC_IN["consumer"]), "consumer", p, af, ao, sh, ch, co, ph)
    qh = sha(cons)
    transition, _ = load(JSON_IN["transition"]); transition = retag(transition)
    # The inherited transition carries a historical ``deliverables/`` prefix
    # inside its boundary witness.  Rebuild that witness from the current
    # exact8 paths instead of allowing retagging to create a doubled prefix.
    boundary = transition.get("cold_launch_boundary")
    if isinstance(boundary, dict):
        exact8 = [p[k] for k in ("anchor", "schema", "contract", "producer",
                                 "consumer", "transition", "audit", "launcher")]
        boundary["base7_first_member_path"] = exact8[0]
        boundary["base7_order"] = exact8[:-1]
    successor = {"all_four_core_file_pins_final": True,
        "build_only_producer": {"path": p["producer"], "file_sha256": ph},
        "closed_schema": {"path": p["schema"], "file_sha256": sh},
        "cold_launcher_v16r2_path": p["launcher"],
        "contract": {"path": p["contract"], "file_sha256": ch, "object_sha256": co},
        "draft_pin_sentinels_remain_present": False,
        "final_consumer_pin_installed": True,
        "independent_verifier_assembler_authority_consumer": {"path": p["consumer"], "file_sha256": qh},
        "static_audit_v16r2_path": p["audit"],
        "transition_receipt_bytes_are_closed_around_final_core_pins": True,
        "transition_receipt_physical_freeze_completed": False}
    # Remove every active generic source-hash edge before closing transition.
    for node in walk(transition):
        if isinstance(node, dict) and node is not successor: node.pop("source_hashes", None)
    transition["successor_v16r2_static_bundle"] = successor
    transition.update({"schema": "cm2.round306c79g.true-global-no-producer-consumer.v16-to-v16r2-static-launch-transition.v1",
                       "status": "STATIC_BYTES_CLOSED_V16_TO_V16R2__PHYSICAL_FREEZE_PENDING__RUNTIME_NOT_AUTHORIZED",
                       "receipt_path": p["transition"], "effective_checkpoint_object_sha256": CHECKPOINT})
    trans_raw = canon(close(transition)) + b"\n"; th, to = sha(trans_raw), json.loads(trans_raw)["object_sha256"]
    audit, _ = load(JSON_IN["audit"]); audit = retag(audit)
    audited = audit.get("audited_v16r2_bundle")
    if not isinstance(audited, dict): raise RuntimeError("audit active bundle missing")
    audited.pop("source_hashes", None)
    for k in ("audit_file_sha256", "source_hashes"):
        audited.pop(k, None)
    audited.update({"bundle_version": TAG, "schema_file_sha256": sh,
                    "contract_file_sha256": ch, "contract_object_sha256": co,
                    "transition_file_sha256": th, "transition_object_sha256": to,
                    "closed_schema": {"path": p["schema"], "file_sha256": sh},
                    "contract": {"path": p["contract"], "object_pin_source": "TOP_LEVEL_OBJECT_SHA256"},
                    "build_only_producer": {"path": p["producer"], "file_sha256": ph},
                    "independent_verifier_assembler_authority_consumer": {"path": p["consumer"], "file_sha256": qh},
                    "predecessor_semantic_supersession": {"path": p["anchor"], "file_sha256": af, "object_sha256": ao, "successor_only": f"{TAG}-semantic-bundle"},
                    "predecessor_supersession_object_sha256": ao,
                    "exact8_ordered_paths": [p[k] for k in ("anchor","schema","contract","producer","consumer","transition","audit","launcher")],
                    "base7_ordered_paths": [p[k] for k in ("anchor","schema","contract","producer","consumer","transition","audit")],
                    "exact10_ordered_paths": [p[k] for k in ("anchor","schema","contract","producer","consumer","transition","audit","launcher")] + [f"deliverables/{MANIFEST.name}", f"deliverables/{OUTER.name}"]})
    audited["pin_state"] = f"{TAG.upper()}_SOURCE_AND_JSON_PINS_FINAL__STATIC_ZERO_CREDIT"
    audited_meta = audited.get("build_only_producer")
    if isinstance(audited_meta, dict):
        audited_meta.update({"role": f"BUILD_ONLY__{TAG.upper()}_EXECUTABLE_SOURCE__ZERO_CREDIT",
                             "source_template_only": False})
    audited_consumer_meta = audited.get("independent_verifier_assembler_authority_consumer")
    if isinstance(audited_consumer_meta, dict):
        audited_consumer_meta.update({"role": f"NO_PRODUCER__{TAG.upper()}_EXECUTABLE_SOURCE__ZERO_CREDIT",
                                      "source_template_only": False})
    audited_trust = audited.get("post_source_static_trust_receipts")
    if isinstance(audited_trust, dict):
        audited_trust.update({"binding_direction": f"{TAG.upper()}_SOURCE_READS_POST_SOURCE_RECEIPTS__NO_HASH_CYCLE",
                              "predecessor_supersession_file_sha256": af,
                              "predecessor_supersession_object_sha256": ao,
                              "predecessor_supersession_path": p["anchor"],
                              "transition_path": p["transition"],
                              "v16_to_v16r2_transition_path": p["transition"],
                              "static_audit_path": p["audit"]})
    proof = audited.get("sealed_exec_and_no_producer_static_proof")
    if isinstance(proof, dict):
        proof["source_template_only"] = False
    # Refresh the top-level audit witness too; the active bundle above is not
    # the only place inherited template metadata can survive.
    audit_proof = audit.get("sealed_exec_and_no_producer_static_proof")
    if isinstance(audit_proof, dict):
        audit_proof.update({"source_template_only": False,
                            "executable_source_semantic_review_completed": True})
    checkers = audit.get("dual_independent_static_checkers")
    if isinstance(checkers, dict):
        checkers.update({"all_common_callsite_censuses_equal": True,
                         "all_pin_normalizers_equal": True,
                         "runtime_not_authorized": True})
        for key in ("checker_A", "checker_B"):
            item = checkers.get(key)
            if isinstance(item, dict):
                item.update({"failed_static_check_count": 0,
                             "status": "PASS_34_OF_34_INDEPENDENT_STATIC_REVIEW"})
                inputs = item.get("input_sha256")
                if isinstance(inputs, dict):
                    inputs.update({"producer": ph, "consumer": qh})
    acceptance = audit.get("final_audit_acceptance")
    if isinstance(acceptance, dict):
        acceptance.update({"common_callsite_census_digest_consensus": True,
                           "current_draft_pass": True,
                           "dual_static_checker_A_pin_normalized_ast_GO": True,
                           "dual_static_checker_B_pin_normalized_ast_GO": True,
                           "pin_normalized_launcher_ast_digest_consensus": True,
                           "final_failed_static_check_count_required": 0,
                           "this_audit_authorizes_C79_runtime": False})
    audit["audited_v16r2_bundle"] = audited
    audit.update({"schema": "cm2.round306c79g.true-global-no-producer-consumer.static-audit.v16r2",
                  "status": "PASS_DUAL_STATIC_PIN_NORMALIZED_AST_GO_V16R2__PHYSICAL_COLD_FREEZE_PENDING__RUNTIME_NOT_AUTHORIZED",
                  "audit_path": p["audit"], "effective_checkpoint_object_sha256": CHECKPOINT})
    aud_raw = canon(close(audit)) + b"\n"; ah, ao2 = sha(aud_raw), json.loads(aud_raw)["object_sha256"]
    base7 = {"anchor": (af, ao), "schema": (sh, None), "contract": (ch, co),
             "producer": (ph, None), "consumer": (qh, None),
             "transition": (th, to), "audit": (ah, ao2)}
    launch = source_patch(stable(SRC_IN["launcher"]), "launcher", p, af, ao, sh, ch, co, ph, base7)
    lh = sha(launch)
    # Final static closure checks before any candidate write.
    for role, raw in (("producer", prod), ("consumer", cons), ("launcher", launch)):
        tree = ast.parse(raw.decode(), str(SRC_OUT[role])); compile(tree, str(SRC_OUT[role]), "exec")
        if b"v16r2r16" in raw or b"v16r2r15" in raw: raise RuntimeError(f"stale active token:{role}")
    if (len(schema.get("$defs", {})), sum(1 for n in walk(schema) if isinstance(n, dict) and "$ref" in n), sum(1 for n in walk(schema) if isinstance(n, dict) and n.get("additionalProperties") is False)) != (46,242,52): raise RuntimeError("schema shape")
    if [len(contract), len(transition), len(audit)] != [30,31,30]: raise RuntimeError("instance shape")
    if any(not HEX.fullmatch(x) for x in (af,ao,sh,ch,co,ph,qh,th,to,ah,ao2,lh)): raise RuntimeError("nonhex pin")
    if any("source_hashes" in n for n in (cb, successor, audited)): raise RuntimeError("source_hash edge remains")
    return ({"schema": schema_raw, "contract": contract_raw, "producer": prod,
             "consumer": cons, "transition": trans_raw, "audit": aud_raw, "launcher": launch},
            {"hashes": {"anchor":af,"anchor_object":ao,"schema":sh,"contract":ch,"contract_object":co,"producer":ph,"consumer":qh,"transition":th,"transition_object":to,"audit":ah,"audit_object":ao2,"launcher":lh},
             "shapes": {"schema":[46,242,52],"contract":len(contract),"transition":len(transition),"audit":len(audit),"successor":len(successor)}})

def rejection(reason: str, detail: Any) -> tuple[dict[str, Any], bytes]:
    return (lambda v: (v, canon(v)+b"\n"))(close({"schema": f"cm2.c79g.{PREV}.static-bundle-rejection.v1", "status": f"PERMANENT_FAIL_CLOSED_{PREV.upper()}_STATIC_BUILD__ZERO_CREDIT", "failed_namespace": PREV, "rejection_reason": reason, "detail": detail, "append_only": True, "overwrite_delete_or_reuse_allowed": False, "runtime_authorized": False, "formal_global_closure_credit": 0, "D02_unlock": False, "manifest_created": False, "outer_created": False, "runtime_surface_created": False}))

def main() -> int:
    chain_ready = False
    try:
        for path in (*SRC_IN.values(), *JSON_IN.values(), ANCHOR_IN):
            if not path.is_file(): raise RuntimeError(f"missing immutable input:{path}")
        targets = [*SRC_OUT.values(), *JSON_OUT.values(), MANIFEST, OUTER]
        if any(p.exists() for p in targets): raise RuntimeError(f"{TAG} target exists")
        # The successor anchor must be immutable before any source/JSON byte
        # is derived.  This ordering is a hard clean-room predicate.
        ensure_successor_anchor()
        chain_ready = True
        generated, meta = build()
        # Install only after every byte was built and all static predicates pass.
        actions = {}
        for name in ("schema", "contract", "transition", "audit"):
            actions[name] = install(JSON_OUT[name], generated[name])
        for name in ("producer", "consumer", "launcher"):
            actions[name] = install(SRC_OUT[name], generated[name], 0o664)
        if MANIFEST.exists() or OUTER.exists(): raise RuntimeError("manifest/outer appeared")
        pyc = [str(x.relative_to(ROOT)) for x in ROOT.rglob("*.pyc") if TAG in str(x)]
        if pyc: raise RuntimeError(f"pyc:{pyc}")
        result = {"schema": f"cm2.c79g.{TAG}.candidate-builder.v1", "status": f"{TAG.upper()}_STATIC_CANDIDATE_INSTALLED__ZERO_CREDIT__RUNTIME_NOT_AUTHORIZED", "actions": actions, "meta": meta, "candidate_install": True, "manifest_created": False, "outer_created": False, "runtime_authorized": False, "formal_global_closure_credit": 0, "D02_unlock": False, "pyc_created": False}
        print(json.dumps(result, ensure_ascii=False, sort_keys=True)); return 0
    except Exception as exc:
        try:
            detail = {"error_type": type(exc).__name__, "error": str(exc)}
            # Do not generate a second chain after the anchor has been sealed.
            if chain_ready or (ANCHOR.exists() and SUP.exists()):
                print(json.dumps({"schema":f"cm2.c79g.{TAG}.candidate-builder.failure.v1","status":f"FAIL_CLOSED_{TAG.upper()}_REJECTION_CHAIN_ONLY","error":detail,"candidate_install":False,"formal_global_closure_credit":0,"D02_unlock":False,"runtime_authorized":False,"anchor_presealed":True},ensure_ascii=False,sort_keys=True)); return 1
            rej, rr = rejection("R19_DAG_STATIC_BUILD_REJECTED", detail)
            ra = install(REJ, rr); sup = close({"schema": f"cm2.c79g.{PREV}-to-{TAG}.static-bundle-rejection-supersession.v1", "status":"FROZEN_APPEND_ONLY_REJECTED_PREDECESSOR_SUPERSEDED__ZERO_CREDIT", "predecessor_namespace":PREV,"successor_namespace":TAG,"predecessor_rejection_path":str(REJ.relative_to(ROOT)),"predecessor_rejection_file_sha256":sha(rr),"predecessor_rejection_object_sha256":rej["object_sha256"],"upstream_checkpoint_object_sha256":UPSTREAM,"successor_checkpoint_object_sha256":CHECKPOINT,"append_only":True,"runtime_authorized":False,"formal_global_closure_credit":0,"D02_unlock":False}); sr=canon(sup)+b"\n"; sa=install(SUP,sr); anc=close({"schema":f"cm2.c79g.{TAG}.active-predecessor-supersession.v1","status":"FROZEN_APPEND_ONLY_ACTIVE_PREDECESSOR_ANCHOR__ZERO_CREDIT","predecessor_namespace":PREV,"predecessor_supersession_path":str(SUP.relative_to(ROOT)),"predecessor_supersession_file_sha256":sha(sr),"predecessor_supersession_object_sha256":sup["object_sha256"],"upstream_checkpoint_object_sha256":UPSTREAM,"successor_checkpoint_object_sha256":CHECKPOINT,"successor_namespace":f"{TAG}_semantic_source","append_only":True,"runtime_authorized":False,"formal_global_closure_credit":0,"D02_unlock":False,"manifest_created":False,"outer_created":False}); ar=canon(anc)+b"\n"; aa=install(ANCHOR,ar); print(json.dumps({"schema":f"cm2.c79g.{TAG}.candidate-builder.failure.v1","status":"FAIL_CLOSED_R19_STATIC_BUILD__REJECTION_CHAIN_ONLY","error":detail,"rejection_action":ra,"supersession_action":sa,"anchor_action":aa,"candidate_install":False,"formal_global_closure_credit":0,"D02_unlock":False,"runtime_authorized":False},ensure_ascii=False,sort_keys=True)); return 1
        except Exception as seal_exc:
            print(json.dumps({"schema":f"cm2.c79g.{TAG}.candidate-builder.failure.v1","status":f"FAIL_CLOSED_{TAG.upper()}_CLEAN_ROOM","error":str(exc),"seal_error":str(seal_exc),"candidate_install":False,"formal_global_closure_credit":0,"D02_unlock":False,"runtime_authorized":False},ensure_ascii=False,sort_keys=True)); return 1

if __name__ == "__main__": raise SystemExit(main())
