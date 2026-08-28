#!/usr/bin/env python3
"""Seal the six legacy-terminal common-v2 adapters with zero formal credit."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
PRODUCER = ROOT / "deliverables/cm2_c27_legacy_terminal_common_v2_adapter_v1.py"
VERIFIER = ROOT / "deliverables/cm2_c27_legacy_terminal_common_v2_adapter_independent_verifier_v1.py"
ATTACKER = ROOT / "deliverables/cm2_c27_legacy_terminal_common_v2_adapter_attack_harness_v1.py"
INTERFACE = ROOT / ".cm2-runtime/audit/c27r2-fresh-actual-v5-rebuild-interface-correction-v2/preflight.json"

EXPECTED = {
    "T01_RETAINED_CONTINUATION": (276, 0),
    "T02_OUTGOING_GRAPHS": (264, 0),
    "T03_SINGLE_GRAPHS": (4_984, 216),
    "T05_SHEET_OWNER": (17_940, 0),
    "T06_SHEET_SHADOW": (17_940, 0),
    "T10_INCLUDED_STRATUM_ATTACHMENTS": (10_660, 0),
}


class Reject(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Reject(label)


def enc(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def dig(value: Any) -> str:
    return hashlib.sha256(enc(value)).hexdigest()


def fsha(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(8 << 20):
            state.update(block)
    return state.hexdigest()


def closed(path: Path, field: str) -> dict[str, Any]:
    value = json.loads(path.read_bytes())
    body = dict(value)
    claim = body.pop(field, None)
    need(type(claim) is str and claim == dig(body), "closure:" + str(path))
    return value


def exclusive(path: Path, payload: bytes) -> None:
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL
                 | getattr(os, "O_NOFOLLOW", 0), 0o600)
    try:
        os.write(fd, payload)
        os.fsync(fd)
    finally:
        os.close(fd)


def manifest_line(path: Path) -> str:
    return f"{fsha(path)}  {path.relative_to(ROOT)}\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed-a", required=True)
    parser.add_argument("--seed-b", required=True)
    parser.add_argument("--verification-a", required=True)
    parser.add_argument("--verification-b", required=True)
    parser.add_argument("--attacks", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    try:
        seed_dirs = [Path(args.seed_a).resolve(), Path(args.seed_b).resolve()]
        result_paths = [directory / "result.json" for directory in seed_dirs]
        results = [closed(path, "result_sha256") for path in result_paths]
        need(result_paths[0].read_bytes() == result_paths[1].read_bytes(),
             "dual seed result byte identity")
        for result in results:
            need(result["status"].startswith("PASS_SIX_LEGACY_AUTHORITIES_ADAPTED")
                 and result["candidate_total"] == 52_064
                 and result["native_semantic_proof_incidence_total"] == 62_160
                 and result["materialized_physical_proof_join_total"] == 216
                 and result["component_relation_disposition_census"] == {
                     "CROSS_COMPONENT__MATERIALIZED_PHYSICAL_PROOF_REQUIRED": 216,
                     "NO_COMPONENT_EDGE_BY_TERMINAL_SEMANTICS": 11_056,
                     "SAME_FROZEN_C15_COMPONENT__NO_EDGE": 40_792,
                 }
                 and result["formal_credit"] == 0
                 and result["manifest_authorized"] is False
                 and result["source_W_transition_authorized"] is False
                 and result["global_atom_and_full_twenty_family_totality_closed"] is False,
                 "result semantics")
        entries_by_seed = []
        payload_paths: set[Path] = set(result_paths)
        for seed_index, (directory, result) in enumerate(zip(seed_dirs, results)):
            entries = {row["authority_slot"]: row for row in result["adapter_entries"]}
            need(set(entries) == set(EXPECTED), f"slot set:{seed_index}")
            for slot, (candidate_count, proof_count) in EXPECTED.items():
                entry = entries[slot]
                need(entry["native_candidate_count"] == candidate_count
                     and entry["semantic_incidences_promoted_to_physical_proof_count"] == proof_count
                     and entry["formal_credit"] == 0,
                     f"slot census:{seed_index}:{slot}")
                for key in ("candidate_ownership_ledger",
                            "materialized_physical_proof_join_ledger"):
                    descriptor = entry[key]
                    path = directory / descriptor["path"]
                    need(path.is_file() and not path.is_symlink()
                         and fsha(path) == descriptor["file_sha256"]
                         and path.stat().st_size == descriptor["file_size"],
                         f"ledger descriptor:{seed_index}:{slot}:{key}")
                    payload_paths.add(path)
            entries_by_seed.append(entries)
        for slot in EXPECTED:
            for key in ("candidate_ownership_ledger",
                        "materialized_physical_proof_join_ledger"):
                left = seed_dirs[0] / entries_by_seed[0][slot][key]["path"]
                right = seed_dirs[1] / entries_by_seed[1][slot][key]["path"]
                need(left.read_bytes() == right.read_bytes(),
                     f"dual seed ledger byte identity:{slot}:{key}")

        verification_paths = [Path(args.verification_a).resolve(),
                              Path(args.verification_b).resolve()]
        verifications = [closed(path, "verification_sha256")
                         for path in verification_paths]
        need(verification_paths[0].read_bytes() == verification_paths[1].read_bytes(),
             "dual verifier byte identity")
        for verification in verifications:
            need(verification["status"].startswith("PASS_NO_ADAPTER_IMPORT")
                 and verification["adapter_imported_or_executed"] is False
                 and verification["candidate_total"] == 52_064
                 and verification["materialized_physical_proof_join_total"] == 216
                 and verification["unique_component_edge_count"] == 88
                 and verification["formal_credit"] == 0
                 and verification["manifest_authorized"] is False
                 and verification["source_W_transition_authorized"] is False,
                 "verification semantics")
        payload_paths.update(verification_paths)

        attacks_path = Path(args.attacks).resolve()
        attacks = closed(attacks_path, "attack_result_sha256")
        need(attacks["status"].startswith("PASS_24_OF_24")
             and attacks["attack_count"] == 24
             and attacks["all_rejected"] is True
             and all(row["rejected"] is True for row in attacks["attacks"])
             and attacks["formal_credit"] == 0
             and attacks["manifest_authorized"] is False
             and attacks["source_W_transition_authorized"] is False,
             "attack semantics")
        payload_paths.add(attacks_path)

        for source in (PRODUCER, VERIFIER, ATTACKER, INTERFACE,
                       Path(__file__).resolve()):
            need(source.is_file() and not source.is_symlink(), "source/interface exists")
            payload_paths.add(source)
        interface = closed(INTERFACE, "preflight_sha256")
        need(interface["schema"].endswith("interface-correction-preflight.v2")
             and interface["decision"] == "REJECT"
             and interface["formal_credit"] == 0
             and interface["Source_W_transition_authorized"] is False
             and interface["corrected_interface"]["candidate_ownership_ledger"]["row_schema"]
                == results[0]["candidate_ownership_row_schema"]
             and interface["corrected_interface"]["materialized_physical_proof_join_ledger"]["row_schema"]
                == results[0]["materialized_physical_proof_join_row_schema"],
             "interface v2")

        output = Path(args.output_dir).resolve()
        need(not output.exists(), "fresh output")
        output.mkdir(parents=True)
        payload_lines = sorted(manifest_line(path) for path in payload_paths)
        payload_manifest = output / "payload_manifest.sha256"
        exclusive(payload_manifest, "".join(payload_lines).encode("ascii"))

        body = {
            "schema": "cm2.c27-independent.legacy-terminal.common-v2-adapter.zero-credit-receipt.v1",
            "status": "PASS_52064_COMMON_V2_CANDIDATES__216_EXACT_T03_PHYSICAL_PROOFS__88_EDGES__DUAL_SEED__DUAL_NO_IMPORT_VERIFIER__24_ATTACKS__ZERO_CREDIT",
            "terminal_slots": list(EXPECTED),
            "candidate_total": 52_064,
            "native_semantic_proof_incidence_total": 62_160,
            "materialized_physical_proof_join_total": 216,
            "physical_component_edge_count": 88,
            "component_relation_disposition_census": results[0]["component_relation_disposition_census"],
            "dual_seed_result_and_twelve_ledgers_byte_identical": True,
            "dual_seed_independent_verification_byte_identical": True,
            "coherent_resigned_attacks_rejected": 24,
            "interface_v2_object_sha256": interface["preflight_sha256"],
            "evidence": {
                "result_file_sha256": fsha(result_paths[0]),
                "result_object_sha256": results[0]["result_sha256"],
                "verification_file_sha256": fsha(verification_paths[0]),
                "verification_object_sha256": verifications[0]["verification_sha256"],
                "attacks_file_sha256": fsha(attacks_path),
                "attacks_object_sha256": attacks["attack_result_sha256"],
            },
            "script_pins": {
                "producer": fsha(PRODUCER),
                "independent_verifier": fsha(VERIFIER),
                "attack_harness": fsha(ATTACKER),
                "receipt_builder": fsha(Path(__file__).resolve()),
            },
            "payload_manifest": {
                "entry_count": len(payload_lines),
                "file_sha256": fsha(payload_manifest),
            },
            "old_C27_FAMILIES_imported_or_read": False,
            "old_transition_or_edge_ledger_used_as_candidate_universe": False,
            "formal_credit": 0,
            "manifest_authorized": False,
            "source_W_transition_authorized": False,
            "global_atom_and_full_twenty_family_totality_closed": False,
            "C27_C28_C29": "REJECT_PENDING_COMPLETE_PRIMITIVE_TWENTY_TERMINAL_GATE",
            "CM2": "NO-GO_FOR_CLAIM",
        }
        receipt = {**body, "receipt_sha256": dig(body)}
        receipt_path = output / "receipt.json"
        exclusive(receipt_path, enc(receipt) + b"\n")
        root_lines = sorted((manifest_line(payload_manifest), manifest_line(receipt_path)))
        exclusive(output / "root_manifest.sha256",
                  "".join(root_lines).encode("ascii"))
    except (Reject, KeyError, TypeError, ValueError, OSError,
            json.JSONDecodeError) as error:
        print("REJECT:" + str(error))
        return 2
    print(enc({"status": receipt["status"],
               "receipt_sha256": receipt["receipt_sha256"]}).decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
