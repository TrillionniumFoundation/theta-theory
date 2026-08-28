#!/usr/bin/env python3
"""Seal native and common-v2 T11--T19 authorities with zero formal credit."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
SOURCES = [
    ROOT / "deliverables/cm2_c27_t11_t19_atlas_control_alias_authority_materializer_v1.py",
    ROOT / "deliverables/cm2_c27_t11_t19_atlas_control_alias_authority_independent_verifier_v1.py",
    ROOT / "deliverables/cm2_c27_t11_t19_atlas_control_alias_authority_attack_harness_v1.py",
    ROOT / "deliverables/cm2_c27_t11_t19_common_v2_adapter_v1.py",
    ROOT / "deliverables/cm2_c27_t11_t19_common_v2_adapter_independent_verifier_v1.py",
    ROOT / "deliverables/cm2_c27_t11_t19_common_v2_adapter_attack_harness_v1.py",
]
INTERFACE = ROOT / ".cm2-runtime/audit/c27r2-fresh-actual-v5-rebuild-interface-correction-v2/preflight.json"


class Reject(RuntimeError): pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value: raise Reject(label)


def enc(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def dig(value: Any) -> str: return hashlib.sha256(enc(value)).hexdigest()


def fsha(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(8 << 20): state.update(block)
    return state.hexdigest()


def closed(path: Path, field: str) -> dict[str, Any]:
    value = json.loads(path.read_bytes())
    body = dict(value); claim = body.pop(field, None)
    need(type(claim) is str and claim == dig(body), "closure:" + str(path))
    return value


def exclusive(path: Path, payload: bytes) -> None:
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL
                 | getattr(os, "O_NOFOLLOW", 0), 0o600)
    try:
        os.write(fd, payload); os.fsync(fd)
    finally:
        os.close(fd)


def line(path: Path) -> str:
    return f"{fsha(path)}  {path.relative_to(ROOT)}\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    for name in ("common-seed-a", "common-seed-b", "common-verification-a",
                 "common-verification-b", "common-attacks", "authority-seed-a",
                 "authority-seed-b", "authority-verification-a",
                 "authority-verification-b", "authority-attacks", "output-dir"):
        parser.add_argument("--" + name, required=True)
    args = parser.parse_args()
    try:
        payload: set[Path] = set(SOURCES + [INTERFACE, Path(__file__).resolve()])
        common_dirs = [Path(args.common_seed_a).resolve(),
                       Path(args.common_seed_b).resolve()]
        common_results_paths = [directory / "result.json" for directory in common_dirs]
        common_results = [closed(path, "result_sha256") for path in common_results_paths]
        need(common_results_paths[0].read_bytes() == common_results_paths[1].read_bytes(),
             "common dual result identity")
        payload.update(common_results_paths)
        for result in common_results:
            need(result["candidate_total"] == 4
                 and result["materialized_physical_proof_join_total"] == 0
                 and result["auxiliary_authority_row_total"] == 328
                 and result["component_relation_disposition_census"]
                    == {"NO_COMPONENT_EDGE_BY_TERMINAL_SEMANTICS": 4}
                 and result["reverse_control_alias_independent_candidate_count"] == 0
                 and result["formal_credit"] == 0
                 and result["manifest_authorized"] is False
                 and result["source_W_transition_authorized"] is False
                 and result["global_atom_and_full_twenty_family_totality_closed"] is False,
                 "common result semantics")
        entries = []
        for seed_index, (directory, result) in enumerate(zip(common_dirs, common_results)):
            seed_entries = {entry["authority_slot"]: entry
                            for entry in result["adapter_entries"]}
            need(len(seed_entries) == 9, "nine common slots")
            for slot, entry in seed_entries.items():
                for key in ("candidate_ownership_ledger",
                            "materialized_physical_proof_join_ledger"):
                    descriptor = entry[key]; path = directory / descriptor["path"]
                    need(fsha(path) == descriptor["file_sha256"]
                         and path.stat().st_size == descriptor["file_size"],
                         "common descriptor:" + slot + ":" + key)
                    payload.add(path)
            entries.append(seed_entries)
        for slot in entries[0]:
            for key in ("candidate_ownership_ledger",
                        "materialized_physical_proof_join_ledger"):
                left = common_dirs[0] / entries[0][slot][key]["path"]
                right = common_dirs[1] / entries[1][slot][key]["path"]
                need(left.read_bytes() == right.read_bytes(),
                     "common dual ledger:" + slot + ":" + key)

        common_verification_paths = [Path(args.common_verification_a).resolve(),
                                     Path(args.common_verification_b).resolve()]
        common_verifications = [closed(path, "verification_sha256")
                                for path in common_verification_paths]
        need(common_verification_paths[0].read_bytes()
             == common_verification_paths[1].read_bytes(),
             "common dual verification identity")
        need(all(value["status"].startswith("PASS_NO_ADAPTER_IMPORT")
                 and value["candidate_total"] == 4
                 and value["materialized_physical_proof_join_total"] == 0
                 and value["auxiliary_authority_row_total"] == 328
                 and value["formal_credit"] == 0
                 for value in common_verifications), "common verification semantics")
        payload.update(common_verification_paths)
        common_attacks_path = Path(args.common_attacks).resolve()
        common_attacks = closed(common_attacks_path, "attack_result_sha256")
        need(common_attacks["attack_count"] == 24
             and common_attacks["all_rejected"] is True
             and all(row["rejected"] is True for row in common_attacks["attacks"]),
             "common attacks")
        payload.add(common_attacks_path)

        authority_dirs = [Path(args.authority_seed_a).resolve(),
                          Path(args.authority_seed_b).resolve()]
        authority_result_paths = [directory / "result.json" for directory in authority_dirs]
        authority_results = [closed(path, "result_sha256") for path in authority_result_paths]
        need(authority_result_paths[0].read_bytes() == authority_result_paths[1].read_bytes(),
             "authority dual result identity")
        payload.update(authority_result_paths)
        authority_names = ("t11_t19_atlas_seam_candidate_ownership.jsonl.gz",
                           "t11_t18_auxiliary_proof_rows.jsonl.gz",
                           "t11_t19_slot_authority.jsonl.gz")
        for seed_index, (directory, result) in enumerate(zip(authority_dirs, authority_results)):
            need(result["candidate_ownership_total"] == 4
                 and result["total_proof_only_authority_rows"] == 328
                 and result["formal_credit"] == 0
                 and result["manifest_authorized"] is False
                 and result["source_W_transition_authorized"] is False,
                 "authority result semantics")
            for name in authority_names:
                path = directory / name; descriptor = result["ledgers"][name]
                need(fsha(path) == descriptor["file_sha256"],
                     "authority descriptor:" + name)
                payload.add(path)
        for name in authority_names:
            need((authority_dirs[0] / name).read_bytes()
                 == (authority_dirs[1] / name).read_bytes(),
                 "authority dual ledger:" + name)

        authority_verification_paths = [Path(args.authority_verification_a).resolve(),
                                        Path(args.authority_verification_b).resolve()]
        authority_verifications = [closed(path, "verification_sha256")
                                   for path in authority_verification_paths]
        need(authority_verification_paths[0].read_bytes()
             == authority_verification_paths[1].read_bytes(),
             "authority dual verification identity")
        need(all(value["status"].startswith("PASS_NO_MATERIALIZER_IMPORT")
                 and value["candidate_ownership_total"] == 4
                 and value["total_proof_only_authority_rows"] == 328
                 and value["formal_credit"] == 0
                 for value in authority_verifications),
             "authority verification semantics")
        payload.update(authority_verification_paths)
        authority_attacks_path = Path(args.authority_attacks).resolve()
        authority_attacks = closed(authority_attacks_path, "attack_result_sha256")
        need(authority_attacks["attack_count"] == 24
             and authority_attacks["all_rejected"] is True
             and all(row["rejected"] is True for row in authority_attacks["attacks"]),
             "authority attacks")
        payload.add(authority_attacks_path)

        interface = closed(INTERFACE, "preflight_sha256")
        need(interface["decision"] == "REJECT" and interface["formal_credit"] == 0,
             "corrected interface fail-closed")
        output = Path(args.output_dir).resolve()
        need(not output.exists(), "fresh output")
        output.mkdir(parents=True)
        payload_lines = sorted(line(path) for path in payload)
        payload_manifest = output / "payload_manifest.sha256"
        exclusive(payload_manifest, "".join(payload_lines).encode("ascii"))
        body = {
            "schema": "cm2.c27-independent.t11-t19.common-v2.zero-credit-receipt.v1",
            "status": "PASS_NATIVE_AND_COMMON_V2_T11_T19__4_FORWARD_SEAM_CANDIDATES__0_PHYSICAL_PROOFS__328_AUXILIARY_ROWS__DUAL_SEED_DUAL_INDEPENDENT_VERIFICATION__48_ATTACKS__ZERO_CREDIT",
            "candidate_total": 4,
            "materialized_physical_proof_join_total": 0,
            "auxiliary_authority_row_total": 328,
            "slot_census": common_results[0]["adapter_entries"],
            "dual_seed_common_result_and_eighteen_ledgers_byte_identical": True,
            "dual_seed_native_result_and_three_ledgers_byte_identical": True,
            "dual_seed_common_verification_byte_identical": True,
            "dual_seed_native_verification_byte_identical": True,
            "coherent_resigned_attacks": {"native": 24, "common_v2": 24,
                                            "total": 48, "all_rejected": True},
            "evidence": {
                "common_result_file_sha256": fsha(common_results_paths[0]),
                "common_result_object_sha256": common_results[0]["result_sha256"],
                "common_verification_file_sha256": fsha(common_verification_paths[0]),
                "common_verification_object_sha256": common_verifications[0]["verification_sha256"],
                "common_attacks_file_sha256": fsha(common_attacks_path),
                "common_attacks_object_sha256": common_attacks["attack_result_sha256"],
                "native_result_file_sha256": fsha(authority_result_paths[0]),
                "native_result_object_sha256": authority_results[0]["result_sha256"],
                "native_verification_file_sha256": fsha(authority_verification_paths[0]),
                "native_verification_object_sha256": authority_verifications[0]["verification_sha256"],
                "native_attacks_file_sha256": fsha(authority_attacks_path),
                "native_attacks_object_sha256": authority_attacks["attack_result_sha256"],
            },
            "script_pins": {path.name: fsha(path) for path in SOURCES + [Path(__file__).resolve()]},
            "payload_manifest": {"entry_count": len(payload_lines),
                                 "file_sha256": fsha(payload_manifest)},
            "auxiliary_authority_is_not_candidate_or_materialized_physical_proof": True,
            "old_C27_FAMILIES_imported_or_read": False,
            "old_transition_or_edge_ledger_used_as_candidate_universe": False,
            "formal_credit": 0, "manifest_authorized": False,
            "source_W_transition_authorized": False,
            "global_atom_and_full_twenty_family_totality_closed": False,
            "C27_C28_C29": "REJECT_PENDING_COMPLETE_PRIMITIVE_TWENTY_TERMINAL_GATE",
            "CM2": "NO-GO_FOR_CLAIM",
        }
        receipt = {**body, "receipt_sha256": dig(body)}
        receipt_path = output / "receipt.json"
        exclusive(receipt_path, enc(receipt) + b"\n")
        root_manifest = output / "root_manifest.sha256"
        exclusive(root_manifest, "".join(sorted((line(payload_manifest),
                                                  line(receipt_path)))).encode("ascii"))
    except (Reject, KeyError, TypeError, ValueError, OSError,
            json.JSONDecodeError) as error:
        print("REJECT:" + str(error)); return 2
    print(enc({"status": receipt["status"],
               "receipt_sha256": receipt["receipt_sha256"]}).decode("ascii"))
    return 0


if __name__ == "__main__": raise SystemExit(main())
