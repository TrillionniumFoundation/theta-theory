#!/usr/bin/env python3
"""Mint the final append-only C27R1D provisional zero-credit receipt."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import stat
import sys
from typing import Any


ROOT = Path(__file__).resolve().parent
PREFIX = "cm2_round306c27r1d_source_g_strict_volume_provisional_overlay"
BUNDLE = ROOT / (PREFIX + "_evidence_bundle.json")
OUT = ROOT / (PREFIX + "_final_zero_credit_receipt.json")
SOURCE_PINS = {
    PREFIX + "_producer.py": "ab2c5c335c5888a2734b8a05f1224c190bfea14e70191bb4b9e9102214c12fa5",
    PREFIX + "_independent_verifier.py": "0bce7b7d13997332b6a69e4ffcdaffb1bf969f3db880073bfa89a04646c5a981",
    PREFIX + "_attack_harness.py": "34b9e438a1d77361baed73fe81bba80e58ab3e8e1fbee6236b42706766d001f9",
    PREFIX + "_evidence_bundle_builder.py": "80b83fe1d16cd8d7b98f905599a20972f60a0682e930246f00154d0dcb5886e6",
}
STRICT_RECEIPT_FILE = "22f8f8f6635a6083254311f5ee776e9ebe82b3192b0aadac6dc9585a0b0db3a4"
STRICT_RECEIPT_OBJECT = "34277fdcb593186e9177e60d1c9fcef9969b732200231895d6c0b3a699621002"
EDGE_SHA = "64cb62aa3b5ae298699ef5809e075ce6c2314baad1f589965e675c82deaa4632"
C15_SHA = "e70c667fd8f14cb3c3d6444bb752dfc86244e61be292a9f884889d53951ff25a"
OUTPUT_SHA = {
    PREFIX + "_14772_edge_application_ledger.jsonl.gz": "27c25945cb018ccb4eaba52c7642bba616590523e766f3ddc63a0706ee87ac0b",
    PREFIX + "_305_affected_cluster_ledger.jsonl.gz": "8a7773d334756be5ab187ca40b6e79a180692e675b8de378eaea1f3b15953794",
    PREFIX + "_43772_component_census_ledger.jsonl.gz": "afbba7e14a3203b947c04f5f007386ced94851c961a08c08d0694078ffd13c80",
    PREFIX + "_502204_member_assignment_ledger.jsonl.gz": "94233878c18e938b4df3984f25b4d33b28d078522f4b074549912f104aad0b8d",
    PREFIX + "_result.json": "62a7cd87fa1f1c0e0e145798028fc2860461702dfa2bdd52da9931e65bfc6a52",
}


class Failure(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Failure(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def stable_identity(info: os.stat_result) -> tuple[int, ...]:
    return (info.st_dev, info.st_ino, info.st_mode, info.st_nlink, info.st_size, info.st_mtime_ns, info.st_ctime_ns)


def capture(path: Path) -> tuple[bytes, dict[str, Any]]:
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
    with os.fdopen(fd, "rb") as stream:
        before = os.fstat(stream.fileno())
        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1, "regular single-link capture:" + path.name)
        state = hashlib.sha256()
        pieces = []
        while block := stream.read(4 << 20):
            state.update(block)
            pieces.append(block)
        after = os.fstat(stream.fileno())
        need(stable_identity(before) == stable_identity(after), "capture changed:" + path.name)
    raw = b"".join(pieces)
    need(len(raw) == before.st_size, "capture byte count:" + path.name)
    return raw, {"filename": path.name, "size": before.st_size, "sha256": state.hexdigest()}


def main() -> int:
    raw, bundle_meta = capture(BUNDLE)
    bundle = json.loads(raw)
    need(canonical(bundle) + b"\n" == raw, "canonical evidence bundle")
    body = dict(bundle)
    bundle_object = body.pop("bundle_object_sha256", None)
    need(type(bundle_object) is str and bundle_object == digest(body), "bundle object closure")
    need(bundle.get("status") == "PASS_APPEND_ONLY_STRICT_VOLUME_PROVISIONAL_OVERLAY_EVIDENCE__ZERO_FORMAL_CREDIT" and bundle.get("formal_credit") == 0, "bundle status/credit")
    authority = bundle.get("input_authority", {})
    need(authority.get("strict_volume_subgate_receipt_file_sha256") == STRICT_RECEIPT_FILE and authority.get("strict_volume_subgate_receipt_object_sha256") == STRICT_RECEIPT_OBJECT, "strict-volume receipt inheritance")
    need(authority.get("sealed_component_edge_ledger") == {"row_count": 14772, "size": 2157061, "sha256": EDGE_SHA}, "sealed edge authority")
    need(authority.get("C15_member_assignment_ledger") == {"row_count": 502204, "size": 142025813, "sha256": C15_SHA}, "C15 authority")
    producer = bundle.get("producer_replay", {})
    need(producer.get("real_materializations") == 2 and producer.get("seeds") == [30633101, 30633991] and producer.get("all_five_outputs_byte_identical") is True, "double producer replay")
    independent = bundle.get("independent_verification", {})
    need(independent.get("real_reconstructions") == 2 and independent.get("seeds") == [30633201, 30633891] and independent.get("byte_identical_verification_outputs") is True, "double independent BFS")
    need(independent.get("implementation") == "ADJACENCY_LIST_AND_RANDOMIZED_BFS__NO_DSU_IMPORT_OR_REUSE", "independent algorithm")
    attacks = bundle.get("coherent_attacks", {})
    need(attacks.get("attack_count") == attacks.get("rejected_count") == 26 and attacks.get("attack_result_object_sha256") == "4e543984a0f5392b3b736a63c10cca0076f8ca21fe132a6374843952a438dd1a", "coherent attack gate")
    census = bundle.get("partition_census", {})
    need(census == {
        "members": 502204, "old_C15_components": 57876, "strict_volume_component_edges": 14772,
        "affected_old_component_vertices": 14409, "affected_connected_clusters": 305,
        "forced_rank_reduction": 14104, "provisional_components": 43772,
        "old_within_component_unordered_member_pairs": 487702036,
        "newly_internalized_unordered_member_pairs": 24956788,
        "provisional_cross_component_pair_denominator": 125591518882,
    }, "exact partition census")
    candidate_files = bundle.get("candidate_files", {})
    need({name: meta.get("sha256") for name, meta in candidate_files.items()} == OUTPUT_SHA, "candidate output pins")
    governance = bundle.get("append_only_governance", {})
    need(governance.get("old_overlay_or_formal_files_modified") is False, "append-only governance")
    need(governance.get("old_C27R1BC_overlay_receipt_file_sha256") == "cd05b9c1260bc037f38ff5edde22c635a1dc40fe5dff3d10a632b453361ac6de" and governance.get("old_C27R1BC_overlay_receipt_object_sha256") == "6ea89bb2d752ee0be78d400da8c2602f7efd5c8a9b09de135f68bb0d2e2feaf9", "old overlay preserved")
    need(governance.get("failed_strict_volume_predecessor", {}).get("diagnosis_sha256") == "ab5499a0e93aab58a963638862f06a9df0844050d0188b43f02c4d497744d75b", "strict failed predecessor")
    need(governance.get("failed_local_attack_predecessor", {}).get("numeric_exit") == 2, "local failed predecessor")
    qualification = bundle.get("qualification", {})
    need(qualification == {
        "component_count": "43772_IS_AN_UPPER_BOUND_ONLY", "dim1_dim2_closure_contacts": "OPEN",
        "endpoint_ownership": "OPEN", "C26_transition_handle_routing": "OPEN", "other_support_terminals": "OPEN",
        "twenty_family_physical_totality_and_unique_assignment": "OPEN",
        "C27": "UNAUTHORIZED", "C28": "UNAUTHORIZED", "C29": "UNAUTHORIZED", "CM2": "NO-GO_FOR_CLAIM",
    }, "open obligations/unauthorized chain")
    need({name: bundle.get("source_sha256", {}).get(name) for name in SOURCE_PINS} == SOURCE_PINS, "bundle source pins")
    for name, sha in SOURCE_PINS.items():
        _, meta = capture(ROOT / name)
        need(meta["sha256"] == sha, "live source pin:" + name)

    receipt = {
        "schema": "cm2.round306c27r1d.strict-volume-provisional-overlay-final-zero-credit-receipt.v1",
        "status": "PASS_APPEND_ONLY_STRICT_VOLUME_PROVISIONAL_UPPER_BOUND__ZERO_FORMAL_CREDIT",
        "authority": "PROVISIONAL_WITNESS_PARTITION_ONLY__NOT_A_FORMAL_C27_C28_C29_SEAL",
        "formal_credit": 0,
        "evidence_bundle": {**bundle_meta, "bundle_object_sha256": bundle_object},
        "input_authority": authority,
        "producer_replay": {
            "algorithm": producer["implementation"], "real_materializations": 2,
            "seeds": producer["seeds"], "all_five_outputs_byte_identical": True,
        },
        "independent_verification": {
            "algorithm": independent["implementation"], "real_reconstructions": 2,
            "seeds": independent["seeds"], "byte_identical_outputs": True,
            "verification_object_sha256": independent["runs"][0]["verification_object_sha256"],
        },
        "coherent_attacks": attacks,
        "exact_census": census,
        "candidate_files": candidate_files,
        "append_only_governance": governance,
        "qualification": qualification,
        "source_sha256": {**SOURCE_PINS, Path(__file__).name: hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},
    }
    receipt["receipt_object_sha256"] = digest(receipt)
    payload = canonical(receipt) + b"\n"
    need(not OUT.exists(), "no clobber final receipt")
    fd = os.open(OUT, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
    try:
        os.write(fd, payload)
        os.fsync(fd)
    finally:
        os.close(fd)
    sys.stdout.buffer.write(payload)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (Failure, OSError, KeyError, ValueError, TypeError, json.JSONDecodeError) as error:
        print(json.dumps({"status": "FAIL_CLOSED", "error": str(error)}, sort_keys=True), file=sys.stderr)
        raise SystemExit(2)
