#!/usr/bin/env python3
"""Freeze the accepted C76l A9/A11 evidence behind one append-only receipt.

This publisher does not create new mathematical evidence.  It verifies the
accepted dual build, the A11 independent verifier v2 pair, the earlier
completion receipt, and the three retained rejection/supersession records.
It then publishes a manifest and an outer receipt last, followed by a
terminal-byte replay.  The frozen bundle remains zero-credit.
"""

from __future__ import annotations

import hashlib
import json
import os
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BUILD_A = ROOT / ".cm2-runtime/c76l-build-a9.v2-baf36f71"
BUILD_B = ROOT / ".cm2-runtime/c76l-build-b9.v2-baf36f71"
VERIFY_A = ROOT / ".cm2-runtime/c76l-independent-v2-a11.ba8a77c2.json"
VERIFY_B = ROOT / ".cm2-runtime/c76l-independent-v2-b11.ba8a77c2.json"
COMPLETION = ROOT / ".cm2-runtime/c76l-completion-a11.ba8a77c2.json"
PRODUCER = ROOT / "deliverables/cm2_round306c76l_large_component_collision1_graph_exact_oracle_v1.py"
VERIFIER = ROOT / "deliverables/cm2_round306c76l_large_component_collision1_graph_exact_oracle_independent_verifier_v2.py"

EXPECTED = {
    "producer": "baf36f7188dbb343271170ec3a88ce5e390bc43f5cbb3e1a28a4546e95a59fed",
    "verifier": "ba8a77c2f8c0907e9236877c0f1147a6688e79e2ba89e33bce0bc9fbda0f4bf2",
    "verification_file": "29aa766d9249ea49f9fc2d923e57e6e424bf799aa3bb8dee3988085674a967d9",
    "verification_object": "d6bbb72bb1226dd73225f225b0934d7767d0f8f2cfa23f0a84a49848d9d5cebf",
    "completion_file": "222b5e75b35ebaca6a48cc0065ba7348a827dc3a334c3242e33a81581faae247",
    "completion_object": "6657bcb9bfd34703d03073276e57a21fabbcfe5cf6c9b22ee56f050d541a0cc2",
    "candidate_object": "7c33ed192ce7814168cee8bc23c92ba23a367dc588abdde5dae6da7a179425b8",
}

REJECTIONS = [
    ("independent-verifier-v1-insufficient-upstream-provenance",
     ROOT / ".cm2-runtime/c76l-independent-v1-a9-rejected-superseded.txt"),
    ("independent-verifier-v2-a9-wrong-intermediate-public-cell-assertion",
     ROOT / ".cm2-runtime/c76l-independent-v2-first-attempt-rejected.txt"),
    ("independent-verifier-v2-a10-interrupted-wrong-per-side-count",
     ROOT / ".cm2-runtime/c76l-independent-v2-a10-b10-rejected-interrupted.txt"),
]

MEMBERS = [
    "ZERO_CREDIT_STAGED_C76L_COLLISION1_GRAPH_ONLY.lock",
    "cm2_round306c76l_large_component_collision1_graph_exact_oracle_v1_collision3_handoffs.jsonl.gz",
    "cm2_round306c76l_large_component_collision1_graph_exact_oracle_v1_decisions.jsonl.gz",
    "cm2_round306c76l_large_component_collision1_graph_exact_oracle_v1_degree1_scope_source_boundary_registry.jsonl.gz",
    "cm2_round306c76l_large_component_collision1_graph_exact_oracle_v1_exact_branch_partitions.jsonl.gz",
    "cm2_round306c76l_large_component_collision1_graph_exact_oracle_v1_manifest.sha256",
    "cm2_round306c76l_large_component_collision1_graph_exact_oracle_v1_outer_receipt.json",
    "cm2_round306c76l_large_component_collision1_graph_exact_oracle_v1_physical_graph_incidence.jsonl.gz",
    "cm2_round306c76l_large_component_collision1_graph_exact_oracle_v1_report.md",
    "cm2_round306c76l_large_component_collision1_graph_exact_oracle_v1_result.json",
    "cm2_round306c76l_large_component_collision1_graph_exact_oracle_v1_semialgebraic_branch_registry.json",
]

INNER = "cm2_round306c76l_large_component_collision1_graph_exact_oracle_v2_frozen_dual_completion_receipt.json"
MANIFEST = "cm2_round306c76l_large_component_collision1_graph_exact_oracle_v2_frozen_manifest.sha256"
OUTER = "cm2_round306c76l_large_component_collision1_graph_exact_oracle_v2_frozen_outer_receipt.json"


def need(value: bool, label: str) -> None:
    if not value:
        raise RuntimeError(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("ascii")


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read(path: Path) -> bytes:
    need(path.is_file() and not path.is_symlink(), f"secure file: {path}")
    return path.read_bytes()


def sha_file(path: Path) -> str:
    return sha_bytes(read(path))


def strict_json(path: Path) -> dict[str, Any]:
    value = json.loads(read(path))
    need(isinstance(value, dict), f"object JSON: {path}")
    return value


def close_object(value: dict[str, Any]) -> dict[str, Any]:
    out = dict(value)
    out["object_sha256"] = sha_bytes(canonical(out))
    return out


def exclusive(path: Path, data: bytes) -> None:
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o444)
    with os.fdopen(fd, "wb") as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())


def main() -> int:
    need(len(sys.argv) == 2, "usage: freeze.py FRESH_STAGE")
    stage = Path(sys.argv[1])
    need(not stage.exists(), "fresh append-only stage")
    stage.mkdir(parents=True, mode=0o755)

    need(sha_file(PRODUCER) == EXPECTED["producer"], "producer pin")
    need(sha_file(VERIFIER) == EXPECTED["verifier"], "verifier v2 pin")
    va_raw, vb_raw = read(VERIFY_A), read(VERIFY_B)
    need(va_raw == vb_raw, "A/B v2 verification byte identity")
    need(sha_bytes(va_raw) == EXPECTED["verification_file"], "verification file pin")
    va = json.loads(va_raw)
    need(va["object_sha256"] == EXPECTED["verification_object"], "verification object pin")
    need(va["verifier_v2_file_sha256"] == EXPECTED["verifier"], "verification verifier pin")
    need(va["status"] == "PASS_INDEPENDENT_C76L_V2__DUAL_BYTES__UPSTREAM_PROVENANCE__EXACT_INCIDENCE_BOUNDARY__ZERO_CREDIT", "verification PASS")
    attacks = va["upstream_provenance_reconstruction"]["coherent_provenance_attacks"]
    need(attacks["attack_count"] == 29 and len(attacks["attacks"]) == 29, "29 provenance attacks")

    completion = strict_json(COMPLETION)
    need(sha_file(COMPLETION) == EXPECTED["completion_file"], "completion file pin")
    need(completion["object_sha256"] == EXPECTED["completion_object"], "completion object pin")
    need(completion["independent_verification_file_sha256"] == EXPECTED["verification_file"], "completion verification file pin")
    need(completion["independent_verification_object_sha256"] == EXPECTED["verification_object"], "completion verification object pin")
    need(completion["dual_build_byte_identical"] is True, "completion dual identity")
    need(completion["terminal_byte_replay_completed_after_outer_receipts"] is True, "prior terminal replay")

    member_sha: dict[str, str] = {}
    for name in MEMBERS:
        a, b = read(BUILD_A / name), read(BUILD_B / name)
        need(a == b, f"dual member byte identity: {name}")
        digest = sha_bytes(a)
        need(completion["member_sha256"][name] == digest, f"completion member pin: {name}")
        member_sha[name] = digest
    result = strict_json(BUILD_A / "cm2_round306c76l_large_component_collision1_graph_exact_oracle_v1_result.json")
    need(result["object_sha256"] == EXPECTED["candidate_object"], "candidate object pin")

    rejected = []
    for reason, path in REJECTIONS:
        data = read(path)
        rejected.append({"reason": reason, "path": str(path.relative_to(ROOT)),
                         "sha256": sha_bytes(data), "status": "REJECTED_SUPERSEDED_ZERO_CREDIT"})

    receipt = close_object({
        "schema": "cm2.round306c76l.large-component-collision1-graph-exact-oracle.v2.frozen-dual-completion-receipt",
        "status": "PASS_FROZEN_C76L_V2_A9_DUAL_BUILD__A11_DUAL_INDEPENDENT_VERIFICATION__APPEND_ONLY_SUPERSESSION_CLOSED",
        "producer_file_sha256": EXPECTED["producer"],
        "independent_verifier_v2_file_sha256": EXPECTED["verifier"],
        "candidate_result_object_sha256": EXPECTED["candidate_object"],
        "dual_build_member_file_sha256": member_sha,
        "dual_build_byte_identical": True,
        "verification_A_path": str(VERIFY_A.relative_to(ROOT)),
        "verification_B_path": str(VERIFY_B.relative_to(ROOT)),
        "verification_A_B_byte_identical": True,
        "independent_verification_file_sha256": EXPECTED["verification_file"],
        "independent_verification_object_sha256": EXPECTED["verification_object"],
        "upstream_provenance_attacks": "PASS_29_OF_29",
        "prior_completion_path": str(COMPLETION.relative_to(ROOT)),
        "prior_completion_file_sha256": EXPECTED["completion_file"],
        "prior_completion_object_sha256": EXPECTED["completion_object"],
        "superseded_evidence": rejected,
        "only_A9_build_and_A11_v2_verification_are_consumable": True,
        "terminal_byte_replay_after_A9_outer_receipts": True,
        "formal_credit": 0, "global_credit": 0, "D02_gate_credit": 0,
        "whole_component_credit": 0, "canonical_pointer_or_seal_written": False,
    })
    exclusive(stage / INNER, canonical(receipt) + b"\n")
    manifest_raw = f"{sha_file(stage / INNER)}  {INNER}\n".encode("ascii")
    exclusive(stage / MANIFEST, manifest_raw)
    outer = close_object({
        "schema": "cm2.round306c76l.large-component-collision1-graph-exact-oracle.v2.frozen-outer-receipt",
        "frozen_completion_object_sha256": receipt["object_sha256"],
        "manifest_sha256": sha_bytes(manifest_raw),
        "ordered_member_file_sha256": [{"filename": INNER, "sha256": sha_file(stage / INNER)}],
        "outer_receipt_published_last": True,
        "terminal_byte_replay_required_after_outer_receipt": True,
        "formal_credit": 0, "global_credit": 0, "D02_gate_credit": 0,
        "whole_component_credit": 0,
    })
    exclusive(stage / OUTER, canonical(outer) + b"\n")

    # Terminal replay occurs only after the outer receipt has been published.
    for path in (stage / INNER, stage / MANIFEST, stage / OUTER):
        sha_file(path)
    print(json.dumps({"stage": str(stage), "receipt_object_sha256": receipt["object_sha256"],
                      "outer_object_sha256": outer["object_sha256"],
                      "terminal_byte_replay": True}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
