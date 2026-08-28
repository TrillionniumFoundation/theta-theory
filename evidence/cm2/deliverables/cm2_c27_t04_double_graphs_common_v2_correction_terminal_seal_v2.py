#!/usr/bin/env python3
"""Manifest-first zero-credit seal for the corrected T04 common-v2 adapter."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
CORE = [
    "T04_DOUBLE_GRAPHS_candidate_ownership.jsonl.gz",
    "T04_DOUBLE_GRAPHS_terminal_absence_authority.jsonl.gz",
    "T04_DOUBLE_GRAPHS_materialized_physical_proof_join.jsonl.gz",
    "adapter_receipt.json",
    "manifest.sha256",
]


class Reject(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Reject(label)


def enc(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(enc(value)).hexdigest()


def file_sha(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(8 << 20), b""):
            state.update(block)
    return state.hexdigest()


def document(path: Path, closure: str) -> dict[str, Any]:
    value = json.loads(path.read_bytes())
    body = dict(value)
    claim = body.pop(closure, None)
    need(claim == digest(body), "document closure:" + path.name)
    return value


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT))


def write_new(path: Path, payload: bytes) -> None:
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL
                 | getattr(os, "O_NOFOLLOW", 0), 0o600)
    try:
        os.write(fd, payload)
        os.fsync(fd)
    finally:
        os.close(fd)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--adapter-a", required=True)
    parser.add_argument("--adapter-b", required=True)
    parser.add_argument("--verification", required=True)
    parser.add_argument("--attacks", required=True)
    parser.add_argument("--native-receipt", required=True)
    parser.add_argument("--native-cold-replay", required=True)
    parser.add_argument("--interface-v2", required=True)
    parser.add_argument("--out-dir", required=True)
    args = parser.parse_args()
    adapter_a = Path(args.adapter_a).resolve()
    adapter_b = Path(args.adapter_b).resolve()
    verification_path = Path(args.verification).resolve()
    attacks_path = Path(args.attacks).resolve()
    native_receipt_path = Path(args.native_receipt).resolve()
    native_cold_path = Path(args.native_cold_replay).resolve()
    interface_path = Path(args.interface_v2).resolve()
    output = Path(args.out_dir).resolve()
    need(not output.exists(), "fresh seal output")

    adapter_receipt_a = document(adapter_a / "adapter_receipt.json", "receipt_sha256")
    adapter_receipt_b = document(adapter_b / "adapter_receipt.json", "receipt_sha256")
    verification = document(verification_path, "verification_sha256")
    attacks = document(attacks_path, "attack_receipt_sha256")
    native_receipt = document(native_receipt_path, "receipt_sha256")
    native_cold = document(native_cold_path, "receipt_sha256")
    interface = document(interface_path, "preflight_sha256")
    need(adapter_receipt_a == adapter_receipt_b, "dual adapter receipt identity")
    for name in CORE:
        need(file_sha(adapter_a / name) == file_sha(adapter_b / name),
             "dual adapter byte identity:" + name)
    exact = adapter_receipt_a["exact_census"]
    need(exact["candidate_pairs"] == 1_362_088
         and exact["terminal_absence_authority_rows"] == 1_362_088
         and exact["physical_proof_rows"] == 0
         and exact["unresolved"] == 0
         and exact["legal_cross_component_witnesses"] == 0
         and exact["component_edges"] == 0
         and adapter_receipt_a["common_v2_contract"]
             ["component_relation_disposition"]
             == "NO_COMPONENT_EDGE_BY_TERMINAL_SEMANTICS"
         and adapter_receipt_a["formal_credit"] == 0,
         "adapter corrected semantics")
    need(verification["physical_proof_rows"] == 0
         and verification["candidate_pairs"] == 1_362_088
         and verification["terminal_absence_authority_rows"] == 1_362_088
         and verification["dual_seed_all_files_byte_identical"] is True
         and verification["adapter_source_imported"] is False
         and verification["formal_credit"] == 0, "independent verification")
    need(attacks["attack_count"] == 34 and attacks["rejected"] == 34
         and attacks["accepted"] == 0
         and attacks["explicitly_rejects_quarantined_one_pseudo_proof_mode"] is True
         and attacks["formal_credit"] == 0, "coherent attacks")
    need(native_receipt["pair_contract"]["candidate_pairs"] == 1_362_088
         and native_receipt["pair_contract"]["physical_witness_ledger_rows"] == 0
         and native_receipt["formal_credit"] == 0, "native receipt")
    need(native_cold["candidate_pairs"] == 1_362_088
         and native_cold["legal_cross_component_witnesses"] == 0
         and native_cold["pre_post_sha256_identical"] is True
         and native_cold["pre_post_stat_identical"] is True,
         "native cold replay")
    allowed = (interface["corrected_interface"]["candidate_ownership_ledger"]
               ["allowed_component_relation_dispositions"])
    need("NO_COMPONENT_EDGE_BY_TERMINAL_SEMANTICS" in allowed
         and interface["decision"] == "REJECT" and interface["formal_credit"] == 0,
         "correction-v2 interface")

    source_paths = [
        ROOT / "deliverables/cm2_c27_t04_double_graphs_common_v2_typed_adapter_correction_v2.py",
        ROOT / "deliverables/cm2_c27_t04_double_graphs_common_v2_typed_adapter_correction_v2_independent_verifier.py",
        ROOT / "deliverables/cm2_c27_t04_double_graphs_common_v2_typed_adapter_correction_v2_attack_harness.py",
        Path(__file__).resolve(),
    ]
    members = ([adapter_a / name for name in CORE]
               + [adapter_b / name for name in CORE]
               + [verification_path, attacks_path, native_receipt_path,
                  native_cold_path, interface_path]
               + source_paths)
    need(all(path.is_file() for path in members), "all payload members exist")
    output.mkdir(parents=True)
    payload_manifest = output / "payload_manifest.sha256"
    payload_lines = [file_sha(path) + "  " + rel(path)
                     for path in sorted(members, key=rel)]
    write_new(payload_manifest,
              ("\n".join(payload_lines) + "\n").encode("ascii"))
    body = {
        "schema": (
            "cm2.c27-independent.t04-double-graphs.common-v2-correction-"
            "terminal-zero-credit-seal-receipt.v2"),
        "status": (
            "PASS_T04_COMMON_V2_1362088_CANDIDATES_1362088_ABSENCE_AUTHORITIES_"
            "ZERO_PHYSICAL_PROOFS_DUAL_SEED_34_ATTACKS__ZERO_CREDIT"),
        "terminal": "DOUBLE_GRAPHS",
        "terminal_ordinal": 4,
        "authority_slot": "T04_DOUBLE_GRAPHS",
        "candidate_pairs": 1_362_088,
        "terminal_absence_authority_rows": 1_362_088,
        "materialized_physical_proof_rows": 0,
        "component_relation_disposition": "NO_COMPONENT_EDGE_BY_TERMINAL_SEMANTICS",
        "legal_cross_component_witnesses": 0,
        "component_edges": 0,
        "unresolved": 0,
        "dual_seed_all_files_byte_identical": True,
        "independent_no_import_verifier": True,
        "coherent_attacks": {"rejected": 34, "accepted": 0},
        "quarantined_one_pseudo_proof_mode_rejected": True,
        "adapter_receipt_file_sha256": file_sha(adapter_a / "adapter_receipt.json"),
        "independent_verification_file_sha256": file_sha(verification_path),
        "attack_receipt_file_sha256": file_sha(attacks_path),
        "payload_manifest": {
            "path": rel(payload_manifest),
            "sha256": file_sha(payload_manifest),
            "entry_count": len(payload_lines),
        },
        "strict_nonpromotion": {
            "C27": "UNAUTHORIZED", "C28": "UNAUTHORIZED",
            "C29": "UNAUTHORIZED", "Source_W": 80,
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "formal_credit": 0,
        "manifest_authorized": False,
        "source_W_transition_authorized": False,
    }
    receipt = {**body, "receipt_sha256": digest(body)}
    receipt_path = output / "receipt.json"
    write_new(receipt_path, enc(receipt) + b"\n")
    root_manifest = output / "root_manifest.sha256"
    root_lines = [file_sha(path) + "  " + rel(path)
                  for path in (payload_manifest, receipt_path)]
    write_new(root_manifest, ("\n".join(root_lines) + "\n").encode("ascii"))
    print(enc({
        "status": receipt["status"],
        "receipt_file_sha256": file_sha(receipt_path),
        "receipt_sha256": receipt["receipt_sha256"],
        "payload_manifest_sha256": file_sha(payload_manifest),
        "root_manifest_sha256": file_sha(root_manifest),
    }).decode("ascii"))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Reject as exc:
        print("T04_COMMON_V2_CORRECTION_SEAL_REJECT:" + str(exc))
        raise SystemExit(2)
