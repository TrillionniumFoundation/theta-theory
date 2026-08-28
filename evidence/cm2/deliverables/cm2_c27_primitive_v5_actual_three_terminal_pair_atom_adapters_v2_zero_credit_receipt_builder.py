#!/usr/bin/env python3
"""Append-only zero-credit seal for corrected T07/T08/T09 v2 adapters."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
PINS = {
    "seed1_receipt": (".cm2-runtime/audit/c27-primitive-v5-actual-three-terminal-pair-atom-adapters-v2-seed30646101/adapter_receipt.json", "19e5a5e564dc3b0586706282d9a5ba370b03a70c312e3c5e58f5e4d0c3722940", "5ebcfeade7c5a4d76d4042cb7d5c310b6c474d272c0caff68e9964939b403385"),
    "seed2_receipt": (".cm2-runtime/audit/c27-primitive-v5-actual-three-terminal-pair-atom-adapters-v2-seed30646991/adapter_receipt.json", "8cc3820bcf7831c957bec5f1995f05c69c032753d890742940127b11717ddf40", "1a1df8dd2b9bcb2adc7eebce32d6100bb23051317568bb717e77d6fe22aab6de"),
    "verification": (".cm2-runtime/audit/c27-primitive-v5-actual-three-terminal-pair-atom-adapters-v2-independent-verifier/verification.json", "16bb863f5b0f0ffeba7e225e579e56ce8b5e22d2aca699a1829282b7bac53533", "b7122891e63c1ee30a0082b8750408516636cc05df1070aaacd6bbb4c862d644"),
    "attacks": (".cm2-runtime/audit/c27-primitive-v5-actual-three-terminal-pair-atom-adapters-v2-coherent-attacks/attack_result.json", "b2550ee7abdc19afa49a926731839555ce2ba6172e884c921fcc000c2d87e26a", "a2e047ee29308baa98777b6faf90c97027e45a034e3e3bdd82c416d5ec796c5b"),
    "interface": (".cm2-runtime/audit/c27r2-fresh-actual-v5-rebuild-interface-correction-v2/preflight.json", "6873b33d7b131a4bde0c4dbcf99873e6826cf2190fde6dfdf6640ee47d53c9d6", "3ece982b83b968e7cc23c4d43f2602fb5f8490484af5ed2f214515be4f0eb37e"),
}
SOURCES = {
    "producer": ("deliverables/cm2_c27_primitive_v5_actual_three_terminal_pair_atom_adapters_v2.py", "8b85ca7e84efde3c55ae54b6bd392de39741f29e29537c01e063cf1e697399e8"),
    "verifier": ("deliverables/cm2_c27_primitive_v5_actual_three_terminal_pair_atom_adapters_v2_independent_verifier.py", "3d3e64d8809bb4c1b9475567028da5774fb0a1683a03992881372d5f884ffb84"),
    "attack_harness": ("deliverables/cm2_c27_primitive_v5_actual_three_terminal_pair_atom_adapters_v2_attack_harness.py", "178c32f8902ec2f8a8bb1c497cf19966b465ab48dccbb118ef5ddc5df398539e"),
}


class Failure(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Failure(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def fsha(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(4 << 20):
            state.update(block)
    return state.hexdigest()


def document(path: Path, closure: str) -> dict[str, Any]:
    value = json.loads(path.read_bytes())
    body = dict(value)
    claim = body.pop(closure, None)
    need(type(claim) is str and claim == digest(body),
         "closure:" + path.name)
    return value


def manifest_entry(path: Path) -> str:
    return f"{fsha(path)}  {path.relative_to(ROOT)}\n"


def write_exclusive(path: Path, payload: bytes) -> None:
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL
                 | getattr(os, "O_NOFOLLOW", 0), 0o600)
    try:
        os.write(fd, payload)
        os.fsync(fd)
    finally:
        os.close(fd)


def build(output: Path) -> dict[str, Any]:
    need(not output.exists(), "fresh output")
    documents = {}
    for label, (relative, file_pin, object_pin) in PINS.items():
        path = ROOT / relative
        need(path.is_file() and fsha(path) == file_pin, "pin:" + label)
        closure = {"seed1_receipt": "receipt_sha256",
                   "seed2_receipt": "receipt_sha256",
                   "verification": "verification_sha256",
                   "attacks": "attack_result_sha256",
                   "interface": "preflight_sha256"}[label]
        row = document(path, closure)
        need(row[closure] == object_pin, "object pin:" + label)
        documents[label] = row
    for label, (relative, pin) in SOURCES.items():
        need(fsha(ROOT / relative) == pin, "source pin:" + label)
    seed1, seed2 = documents["seed1_receipt"], documents["seed2_receipt"]
    verification, attacks = documents["verification"], documents["attacks"]
    need(seed1["formal_credit"] == seed2["formal_credit"] == 0
         and seed1["exact_census"] == seed2["exact_census"],
         "dual seed receipt census")
    need(verification["status"].startswith("PASS_NO_PRODUCER_IMPORT")
         and verification["exact_census"]["byte_identical_ledger_count"] == 8
         and verification["formal_credit"] == 0,
         "independent verification")
    need(attacks["census"] == {"attack_count": 22,
                               "coherently_resigned_attack_count": 22,
                               "row_reclosed_attack_count": 4,
                               "rejected_count": 22}
         and attacks["formal_credit"] == 0,
         "coherent attack closure")
    ledger_pairs = []
    for left, right in zip(seed1["terminal_adapters"],
                           seed2["terminal_adapters"]):
        need(left["terminal"] == right["terminal"], "terminal alignment")
        for key in ("candidate_ownership_ledger",
                    "materialized_physical_proof_fragment_ledger"):
            a, b = left[key], right[key]
            need(a["sha256"] == b["sha256"]
                 and (ROOT / a["path"]).read_bytes()
                    == (ROOT / b["path"]).read_bytes(),
                 "dual ledger:" + key)
            ledger_pairs.append((a, b))
    for key in ("atom_pair_incidence_ledger",
                "atom_incidence_disposition_ledger"):
        a, b = seed1[key], seed2[key]
        need(a["sha256"] == b["sha256"]
             and (ROOT / a["path"]).read_bytes()
                == (ROOT / b["path"]).read_bytes(), "dual ledger:" + key)
        ledger_pairs.append((a, b))
    need(len(ledger_pairs) == 8, "eight ledger pairs")

    output.mkdir(parents=True)
    payload_paths = set()
    for relative, _, _ in PINS.values():
        payload_paths.add(ROOT / relative)
    for relative, _ in SOURCES.values():
        payload_paths.add(ROOT / relative)
    payload_paths.add(Path(__file__).resolve())
    for receipt in (seed1, seed2):
        for entry in receipt["terminal_adapters"]:
            payload_paths.add(ROOT / entry["candidate_ownership_ledger"]["path"])
            payload_paths.add(ROOT / entry["materialized_physical_proof_fragment_ledger"]["path"])
        payload_paths.add(ROOT / receipt["atom_pair_incidence_ledger"]["path"])
        payload_paths.add(ROOT / receipt["atom_incidence_disposition_ledger"]["path"])
        for item in receipt["root_input_capture"]["attestations"].values():
            payload_paths.add(ROOT / item["path"])
    payload_lines = sorted(manifest_entry(path) for path in payload_paths)
    payload_path = output / "payload_manifest.sha256"
    write_exclusive(payload_path, "".join(payload_lines).encode("ascii"))

    body = {
        "schema": "cm2.c27-independent.primitive-v5-actual-three-terminal-pair-atom-adapters-v2-zero-credit-receipt.v1",
        "status": "PASS_CORRECTED_PAIR_CANDIDATE_ATOM_INCIDENCE_SEPARATION__DUAL_SEED_INVERSE_VERIFIED_22_ATTACKS__ZERO_CREDIT",
        "interface_v2_object_sha256": documents["interface"]["preflight_sha256"],
        "terminal_adapters": seed1["terminal_adapters"],
        "atom_pair_incidence_ledger": seed1["atom_pair_incidence_ledger"],
        "atom_incidence_disposition_ledger": seed1["atom_incidence_disposition_ledger"],
        "exact_census": seed1["exact_census"],
        "dual_seed": {
            "seed1_receipt_file_sha256": PINS["seed1_receipt"][1],
            "seed1_receipt_object_sha256": seed1["receipt_sha256"],
            "seed2_receipt_file_sha256": PINS["seed2_receipt"][1],
            "seed2_receipt_object_sha256": seed2["receipt_sha256"],
            "ledger_pair_count": 8, "all_ledgers_byte_identical": True,
        },
        "independent_verifier": {
            "source_sha256": SOURCES["verifier"][1],
            "result_file_sha256": PINS["verification"][1],
            "result_object_sha256": verification["verification_sha256"],
            "producer_imported": False,
        },
        "coherent_attacks": {
            "source_sha256": SOURCES["attack_harness"][1],
            "result_file_sha256": PINS["attacks"][1],
            "result_object_sha256": attacks["attack_result_sha256"],
            "attacks": 22, "rejected": 22, "row_reclosed": 4,
        },
        "separation_theorem": {
            "candidate_pair_ownership_rows": 101_080,
            "atom_pair_incidence_rows": 206_632,
            "atom_disposition_rows": 483_232,
            "incidence_is_candidate": False,
            "each_candidate_pair_exactly_one_terminal": True,
            "atom_may_have_multiple_pairs_and_terminals": True,
        },
        "payload_manifest": {"filename": payload_path.name,
                             "entry_count": len(payload_lines),
                             "file_sha256": fsha(payload_path)},
        "formal_credit": 0, "manifest_authorized": False,
        "Source_W_transition_authorized": False,
        "strict_nonpromotion": {"C27_transition_totality": 0,
                                "C28_pair_routing": 0,
                                "C29_physical_maximality": 0,
                                "CM2": "NO-GO_FOR_CLAIM"},
        "receipt_builder_source_sha256": fsha(Path(__file__).resolve()),
    }
    receipt = dict(body)
    receipt["receipt_sha256"] = digest(receipt)
    receipt_path = output / "receipt.json"
    write_exclusive(receipt_path, canonical(receipt) + b"\n")
    root_lines = sorted((manifest_entry(payload_path), manifest_entry(receipt_path)))
    write_exclusive(output / "root_manifest.sha256",
                    "".join(root_lines).encode("ascii"))
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    try:
        receipt = build(Path(args.output_dir).resolve())
    except (Failure, KeyError, TypeError, ValueError, OSError,
            json.JSONDecodeError) as error:
        print("FAIL:" + str(error))
        return 2
    print(canonical({"status": receipt["status"],
                     "exact_census": receipt["exact_census"],
                     "receipt_sha256": receipt["receipt_sha256"]}).decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
