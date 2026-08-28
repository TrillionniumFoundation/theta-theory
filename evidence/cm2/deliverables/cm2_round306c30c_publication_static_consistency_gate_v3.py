#!/usr/bin/env python3
"""Static coherence and legacy-assumption inventory for C30c v3 publication."""
from __future__ import annotations

import ast
import hashlib
import json
import os
import stat
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
PREFIX = "cm2_round306c30c_source_w_full_delta_whole_origin_disposition"
NEW_SOURCES = {
    "bundle": ROOT / (PREFIX + "_audit_evidence_bundle_builder_v3.py"),
    "manifests": ROOT / (PREFIX + "_publication_manifest_builder_v3.py"),
    "outer": ROOT / (PREFIX + "_formal_handoff_outer_verifier_v3.py"),
    "terminal": ROOT / (PREFIX + "_terminal_seal_replay_v3.py"),
    "watcher": ROOT / "cm2_round306c30c_postreceipt_v3_publication_chain_watch_v1.py",
}
OLD_SOURCES = {
    "bundle": ROOT / (PREFIX + "_audit_evidence_bundle_builder.py"),
    "manifests": ROOT / (PREFIX + "_publication_manifest_builder.py"),
    "outer": ROOT / (PREFIX + "_formal_handoff_outer_verifier.py"),
    "terminal": ROOT / (PREFIX + "_manifest_first_sealed_verifier.py"),
    "receipt_consistency": ROOT / "cm2_round306c30c_receipt_authority_static_consistency_gate.py",
    "payload_consistency": ROOT / "cm2_round306c30c_payload_replay_static_consistency_gate.py",
}
LEGACY_ASSUMPTIONS = {
    "legacy_run_identity": (
        "c30c-v5-toctou-robustness-rerun-20260807T1012-final",
        "cm2.round306c30c.attack-run-receipt-validation.v1",
    ),
    "legacy_validator_contract": (
        "cm2_round306c30c_62_attack_run_receipt_validator.py",
        "8692c8a8e57d535ba8f8162bd4f7f51e8acb04f28755384158b45b4eb2629b61",
    ),
    "legacy_adapter_contracts": (
        "cm2_round306c30c_attack_receipt_evidence_adapter.py",
        "cm2_round306c30c_attack_receipt_evidence_adapter_independent_verifier.py",
        "f4dac9c42f3de9d02e97060f14bb42ccdfca98015ed4a760bbca044b50c56590",
        "43611f53caa199dce8c529151731db025e197d42232736200fd7b73cd67ba153",
    ),
    "legacy_c30a_precommit_authority": (
        "P0_SUPPLEMENTAL_FINAL_COMMIT_V2_SHA256",
        "P0_POSTCOMMIT_REPLAY_RECEIPT",
        "cm2.round306c30a.supplemental-terminal-replay.v5",
        "cm2.round306c30a.supplemental-pipeline-precommit.v5",
    ),
    "legacy_unversioned_publication_namespace": (
        "PREFIX + \"_audit_evidence.tar.gz\"",
        "PAYLOAD_MANIFEST = PREFIX + \"_payload_manifest.sha256\"",
        "ROOT_MANIFEST = PREFIX + \"_manifest.sha256\"",
        "OUTER_VERIFICATION = PREFIX + \"_verification.json\"",
    ),
    "legacy_sealed_candidate_namespace": (
        "cm2_round306c30c_sealed", "SEALED_DIR",
    ),
    "legacy_static_tool_hash_pins": (
        "OUTER_SHA256", "RECEIPT_SCRIPTS", "SOURCES =",
    ),
}
ACTIVE_TOKENS = (
    "c30c-v5-toctou-robustness-rerun-20260808T0635Z-receipt-v3",
    "c30c-postreceipt-v3-p1-bridge-v1-20260808T0655Z",
    "cm2_round306c30c_62_attack_run_receipt_validator_v3.py",
    "c68633b3cc996c344c737f1e6c71da382a81c8f6bf6c4318b233b6d9db34c97a",
    "6af636a4239f390712d057030f03e09fbbca332c6170f183d3d0095f19f0f248",
    "PASS_ZERO_CREDIT_THROUGH_DUAL_AND_COLD__BLOCKED_BEFORE_PUBLICATION",
)


class Reject(RuntimeError):
    pass


def need(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise Reject(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=True, allow_nan=False, sort_keys=True,
                      separators=(",", ":")).encode("ascii")


def identity(value: os.stat_result) -> tuple[int, ...]:
    return (value.st_dev, value.st_ino, value.st_mode, value.st_nlink,
            value.st_size, value.st_mtime_ns, value.st_ctime_ns)


def capture(path: Path, maximum: int = 8 << 20) -> bytes:
    absolute = Path(os.path.abspath(os.fspath(path)))
    need(absolute.resolve(strict=True) == absolute, "canonical source:" + path.name)
    descriptor = os.open(absolute, os.O_RDONLY | os.O_CLOEXEC |
                         getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(descriptor)
        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1 and
             0 < before.st_size <= maximum, "bounded source:" + path.name)
        chunks: list[bytes] = []
        while block := os.read(descriptor, 1 << 20):
            chunks.append(block)
        after = os.fstat(descriptor)
    finally:
        os.close(descriptor)
    need(identity(before) == identity(after), "stable source:" + path.name)
    return b"".join(chunks)


def literals(raw: bytes, path: Path) -> dict[str, Any]:
    try:
        tree = ast.parse(raw, filename=os.fspath(path))
    except SyntaxError as error:
        raise Reject("source parses:" + path.name) from error
    output: dict[str, Any] = {}
    for node in tree.body:
        name: str | None = None
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            name = node.targets[0].id
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            name = node.target.id
        if name is None:
            continue
        try:
            output[name] = ast.literal_eval(node.value)
        except (ValueError, TypeError):
            pass
    return output


def analyze() -> dict[str, Any]:
    new_raw = {name: capture(path) for name, path in NEW_SOURCES.items()}
    old_raw = {name: capture(path) for name, path in OLD_SOURCES.items()}
    new_text = {name: raw.decode("utf-8") for name, raw in new_raw.items()}
    old_text = {name: raw.decode("utf-8") for name, raw in old_raw.items()}
    inventory: dict[str, list[dict[str, Any]]] = {}
    for category, tokens in LEGACY_ASSUMPTIONS.items():
        rows: list[dict[str, Any]] = []
        for token in tokens:
            hits = sorted(name for name, text in old_text.items() if token in text)
            need(bool(hits), "legacy assumption accounted:" + category + ":" + token)
            rows.append({"token": token, "legacy_source_hits": hits})
            for name, text in new_text.items():
                need(token not in text, "legacy token absent from new " + name + ":" + token)
        inventory[category] = rows
    combined = "\n".join(new_text.values())
    for token in ACTIVE_TOKENS:
        need(token in combined, "active v3 token present:" + token)
    constants = {name: literals(new_raw[name], NEW_SOURCES[name]) for name in NEW_SOURCES}
    for name in ("bundle", "manifests", "outer"):
        need(constants[name].get("RUN_NAME") ==
             "c30c-v5-toctou-robustness-rerun-20260808T0635Z-receipt-v3",
             "coherent RUN_NAME:" + name)
        need(constants[name].get("BRIDGE_NAME") ==
             "c30c-postreceipt-v3-p1-bridge-v1-20260808T0655Z",
             "coherent BRIDGE_NAME:" + name)
    need(constants["watcher"].get("BRIDGE_NAME") ==
         "c30c-postreceipt-v3-p1-bridge-v1-20260808T0655Z",
         "watcher coherent bridge")
    for name in ("manifests", "outer", "terminal", "watcher"):
        need(constants[name].get("C30B_MANIFEST_SHA256") ==
             "6af636a4239f390712d057030f03e09fbbca332c6170f183d3d0095f19f0f248",
             "coherent C30b authority:" + name)
    hashes = {name: hashlib.sha256(raw).hexdigest() for name, raw in new_raw.items()}
    return {
        "schema": "cm2.round306c30c.v3-publication-static-consistency.v1",
        "status": "PASS_V3_PUBLICATION_CONTRACTS_COHERENT__ZERO_FORMAL_CREDIT",
        "new_source_sha256": hashes,
        "legacy_hardcoded_assumption_inventory": inventory,
        "legacy_category_count": len(inventory),
        "active_contract_tokens": list(ACTIVE_TOKENS),
        "publication_order": ["evidence_bundle", "payload_and_root_manifests",
                              "independent_outer_mathematical_checker",
                              "terminal_seal", "terminal_replay"],
        "formal_credit": 0,
        "source_W_formal_remainder": 80,
        "source_W_transition_authorized": False,
        "CM2": "NO-GO_FOR_CLAIM",
    }


def main() -> int:
    try:
        output = analyze()
    except (Reject, OSError, ValueError, TypeError, KeyError) as error:
        print(canonical({"schema": "cm2.round306c30c.v3-publication-static-consistency.v1",
                         "status": "BLOCKED_FAIL_CLOSED", "error": str(error),
                         "formal_credit": 0, "source_W_formal_remainder": 80,
                         "source_W_transition_authorized": False,
                         "CM2": "NO-GO_FOR_CLAIM"}).decode("ascii"))
        return 1
    print(canonical(output).decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
