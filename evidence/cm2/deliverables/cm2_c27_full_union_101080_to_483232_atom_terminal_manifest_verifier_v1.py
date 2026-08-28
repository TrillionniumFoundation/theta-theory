#!/usr/bin/env python3
"""Manifest-first verifier for the scoped three-terminal atom seal."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

BASE_MANIFEST_SHA256 = "5ec48d319fd02c6907abf06300d0668604da6ccd10f07f2023c02d099939a648"
BASE_RECEIPT_FILE_SHA256 = "456d462da8f269112908caaed8bb30a9ff042d54760136c675d00abda28f0241"
BASE_RECEIPT_OBJECT_SHA256 = "28124ff2311535d6296251d140567c5dffc9fec0b8a0381362629753afc4ae7e"
SEED_LEDGER_SHA256 = "9b642b40fea1bbae5121ca9fcc43461795190c92f38753d41ff7d0e4e358b114"
SEED1_LEDGER = ".cm2-runtime/audit/c27-full-union-101080-on-483232-atom-join-v2-seed-30640101-attempt2/full_union_101080_on_483232_atom_incidence_or_complement_v2.jsonl.gz"
SEED2_LEDGER = ".cm2-runtime/audit/c27-full-union-101080-on-483232-atom-join-v2-seed-30640991-attempt1/full_union_101080_on_483232_atom_incidence_or_complement_v2.jsonl.gz"
INDEPENDENT = ".cm2-runtime/audit/c27-full-union-101080-on-483232-atom-independent-verification-v2-attempt1/verification.json"
ATTACKS = ".cm2-runtime/audit/c27-full-union-101080-on-483232-atom-attacks-v1-attempt2/attacks.json"


class Reject(RuntimeError):
    pass


def need(value: bool, message: str) -> None:
    if type(value) is not bool or not value:
        raise Reject(message)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def object_sha(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def file_sha(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(4 << 20), b""):
            state.update(block)
    return state.hexdigest()


def closed(path: Path, key: str) -> dict[str, Any]:
    value = json.loads(path.read_bytes())
    body = dict(value)
    claimed = body.pop(key, None)
    need(claimed == object_sha(body), "closure:" + path.name)
    return value


def same_bytes(left: Path, right: Path) -> bool:
    if left.stat().st_size != right.stat().st_size:
        return False
    with left.open("rb") as a, right.open("rb") as b:
        while True:
            x = a.read(4 << 20)
            y = b.read(4 << 20)
            if x != y:
                return False
            if not x:
                return True


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bundle-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--seed", type=int, required=True)
    args = parser.parse_args()
    try:
        need(args.seed > 0 and not args.output.exists(), "fresh positive-seed output")
        root = Path(__file__).resolve().parent.parent
        bundle = args.bundle_dir.resolve()
        need(bundle.parent.parent == root, "bundle root")
        manifest_path = bundle / "manifest.sha256"
        need(file_sha(manifest_path) == BASE_MANIFEST_SHA256, "base manifest pin")
        members: dict[str, str] = {}
        for ordinal, line in enumerate(manifest_path.read_text("ascii").splitlines()):
            pieces = line.split("  ", 1)
            need(len(pieces) == 2, f"manifest syntax:{ordinal}")
            digest, relative = pieces
            need(len(digest) == 64 and all(c in "0123456789abcdef" for c in digest),
                 f"manifest digest:{ordinal}")
            need(relative not in members and not relative.startswith("/") and ".." not in Path(relative).parts,
                 f"manifest path:{ordinal}")
            path = root / relative
            need(path.is_file() and file_sha(path) == digest, "manifest member:" + relative)
            members[relative] = digest
        need(len(members) == 25, "exact manifest member count")
        receipt_relative = "deliverables/cm2_c27_full_union_101080_to_483232_atom_terminal_zero_credit_v3/terminal_zero_credit_receipt.json"
        need(members[receipt_relative] == BASE_RECEIPT_FILE_SHA256
             and members[SEED1_LEDGER] == members[SEED2_LEDGER] == SEED_LEDGER_SHA256,
             "required manifest members")

        receipt = closed(root / receipt_relative, "receipt_sha256")
        need(receipt["receipt_sha256"] == BASE_RECEIPT_OBJECT_SHA256
             and receipt["status"].startswith("PASS_SCOPED_THREE_TERMINAL_FULL_UNION_ATOM_CONTRACT")
             and receipt["pair_union"]["pairs"] == 101080
             and receipt["exact_atom_contract"]["atoms"] == 483232
             and receipt["exact_atom_contract"]["incident_atoms"] == 62768
             and receipt["exact_atom_contract"]["exact_complement_atoms"] == 420464
             and receipt["exact_atom_contract"]["expanded_atom_route_incidences"] == 206632,
             "base receipt exact contract")
        correction = receipt["coarse_to_exact_contract_correction"]
        need(correction["coarse_positive_incidences_removed"] == 184
             and correction["atoms_affected_by_coarse_positive_removal"] == 144
             and correction["new_atoms_added_by_G2B"] == 528
             and correction["coarse_positive_owner_fanout_is_authority"] is False,
             "coarse-to-exact correction")
        need(receipt["formal_credit"] == 0 and receipt["manifest_authorized"] is False
             and receipt["C27_C28_C29"] == "FULL_REBUILD_REQUIRED"
             and receipt["Source_W_formal_remainder"] == 80
             and receipt["CM2"] == "NO-GO_FOR_CLAIM"
             and receipt["source_W_transition_authorized"] is False,
             "base nonpromotion")

        independent = closed(root / INDEPENDENT, "result_sha256")
        attacks = closed(root / ATTACKS, "result_sha256")
        need(independent["dual_seed_join_ledgers_byte_identical"] is True
             and independent["pair_routes"] == 101080
             and independent["primitive_atoms"] == 483232
             and independent["expanded_atom_route_incidences"] == 206632
             and independent["formal_credit"] == 0,
             "independent authority")
        need(attacks["attack_count"] == attacks["rejected_count"] == 54
             and attacks["accepted_count"] == 0
             and attacks["formal_credit"] == 0,
             "attack authority")
        need(same_bytes(root / SEED1_LEDGER, root / SEED2_LEDGER), "dual ledger bytes")

        semantic = {
            "schema": "cm2.c27-independent.full-union-atom-terminal-manifest-verification.v1",
            "status": "PASS_MANIFEST_FIRST_TERMINAL_REPLAY__DUAL_LEDGER_BYTES_AND_SCOPED_ZERO_CREDIT_CONTRACT_VERIFIED",
            "verification_seed": args.seed,
            "base_manifest_sha256": BASE_MANIFEST_SHA256,
            "base_manifest_member_count": len(members),
            "base_receipt_file_sha256": BASE_RECEIPT_FILE_SHA256,
            "base_receipt_sha256": BASE_RECEIPT_OBJECT_SHA256,
            "dual_seed_ledgers_byte_identical": True,
            "seed_ledger_sha256": SEED_LEDGER_SHA256,
            "pair_routes": 101080,
            "primitive_atoms": 483232,
            "incident_atoms": 62768,
            "exact_complement_atoms": 420464,
            "expanded_atom_route_incidences": 206632,
            "coarse_positive_incidences_removed": 184,
            "coarse_positive_atoms_corrected": 144,
            "G2B_new_incident_atoms": 528,
            "coherent_attacks_rejected": 54,
            "formal_credit": 0,
            "manifest_authorized": False,
            "C27_C28_C29": "FULL_REBUILD_REQUIRED",
            "Source_W_formal_remainder": 80,
            "CM2": "NO-GO_FOR_CLAIM",
            "source_W_transition_authorized": False,
        }
        verification = {**semantic, "verification_sha256": object_sha(semantic)}
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_bytes(canonical(verification) + b"\n")
        print(canonical({
            "status": verification["status"],
            "verification_sha256": verification["verification_sha256"],
        }).decode("ascii"))
        return 0
    except (Reject, KeyError, TypeError, ValueError, OSError) as error:
        print("FAIL:" + str(error))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
