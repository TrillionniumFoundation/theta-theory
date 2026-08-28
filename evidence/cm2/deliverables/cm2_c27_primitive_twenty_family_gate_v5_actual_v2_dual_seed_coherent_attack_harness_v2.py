#!/usr/bin/env python3
"""Coherent resigned attacks v2 on the actual-v2 dual-seed verdict."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
SELF = Path(__file__).resolve()
RUNNER_SHA256 = "c0f2c29d03aad122762ba0b3dad5885418c17872dab3da665eb764dad9cab245"
ASSEMBLER_SHA256 = "038c6a661438f9253fb00a29b9f41941bea33a3a8769a258d8dfa5763880b561"
WATCHER_SHA256 = "3e5f874230c9faf809975808a2bd7284acf32c6e2b771e36a86d532a1a22c386"
EXPECTED_STATUS = "PASS_TWO_REAL_SEEDS_NATIVE_FULL_PASS_INDEPENDENT_GLOBAL_REPLAY_AND_EXACT_SEED_INVARIANCE__ZERO_CREDIT"
EXPECTED_COUNTS = {
    "candidate_total": 7_486_076,
    "materialized_physical_proof_total": 65_064,
    "atom_pair_incidence_total": 206_632,
    "primitive_atom_denominator": 483_232,
    "full_component_edge_union_total": 14_860,
    "frozen_C15_component_total": 57_876,
    "fresh_DSU_successful_merges": 14_192,
    "fresh_DSU_cycle_edges": 668,
    "fresh_DSU_final_component_total": 43_684,
}
LEDGERS = {
    "candidate_ownership", "materialized_physical_proof_join",
    "atom_pair_incidence", "atom_incidence_disposition",
    "full_component_edge_union",
}


class Reject(RuntimeError):
    pass


def require(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Reject(label)


def encode(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(encode(value)).hexdigest()


def fsha(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(4 << 20):
            state.update(block)
    return state.hexdigest()


def load(path: Path) -> dict[str, Any]:
    raw = path.read_bytes()
    value = json.loads(raw)
    require(type(value) is dict and raw == encode(value) + b"\n",
            "canonical verification")
    body = dict(value)
    claim = body.pop("verification_sha256", None)
    require(claim == digest(body), "verification closure")
    return value


def semantic_hash(document: dict[str, Any]) -> str:
    body = dict(document)
    body.pop("verification_sha256", None)
    return digest({key: value for key, value in body.items()
                   if key not in {"verification_seed", "seed_runs",
                                  "semantic_projection_sha256"}})


def accept(document: dict[str, Any], verifier_sha256: str) -> None:
    for label, document in (("verification", document),):
        body = dict(document)
        claim = body.pop("verification_sha256", None)
        require(type(claim) is str and claim == digest(body),
                label + ":closure")
        require(document["schema"]
                == "cm2.c27-independent.primitive-twenty-family-gate-v5-actual-v2-dual-real-seed-verification.v1"
                and document["status"] == EXPECTED_STATUS,
                label + ":schema/status")
        require(document["execution_seeds"] == [30660101, 30660991]
                and type(document["verification_seed"]) is int
                and document["verification_seed"] > 0,
                label + ":real seeds")
        require(set(document["seed_runs"]) == {"30660101", "30660991"},
                label + ":two seed runs")
        seed_runs = document["seed_runs"]
        require(seed_runs["30660101"]["execution_seed"] == 30660101
                and seed_runs["30660991"]["execution_seed"] == 30660991
                and seed_runs["30660101"]["input_snapshot_sha256"]
                    == seed_runs["30660991"]["input_snapshot_sha256"]
                and seed_runs["30660101"]["mathematical_projection_sha256"]
                    == seed_runs["30660991"]["mathematical_projection_sha256"]
                    == document["seed_invariant_mathematical_projection_sha256"],
                label + ":seed-run invariance")
        for item in seed_runs.values():
            require(all(type(item[key]) is str and len(item[key]) == 64
                        for key in (
                            "run_attestation_file_sha256",
                            "run_attestation_object_sha256",
                            "assembler_receipt_file_sha256",
                            "assembler_receipt_object_sha256",
                            "manifest_file_sha256", "input_snapshot_sha256",
                            "mathematical_projection_sha256")),
                    label + ":seed evidence hashes")
        require(all(document["exact_census"].get(key) == value
                    for key, value in EXPECTED_COUNTS.items()),
                label + ":exact census")
        require(set(document["ledger_descriptors"]) == LEDGERS,
                label + ":five ledgers")
        for descriptor in document["ledger_descriptors"].values():
            require(type(descriptor["sha256"]) is str
                    and len(descriptor["sha256"]) == 64
                    and type(descriptor["row_sequence_sha256"]) is str
                    and len(descriptor["row_sequence_sha256"]) == 64
                    and type(descriptor["row_count"]) is int
                    and descriptor["row_count"] > 0,
                    label + ":ledger descriptor")
        pins = document["source_pins"]
        require(pins["runner"] == RUNNER_SHA256
                and pins["assembler"] == ASSEMBLER_SHA256
                and pins["seed2_handoff_watcher"] == WATCHER_SHA256
                and pins["independent_verifier"] == verifier_sha256,
                label + ":source pins")
        require(document["implementation_independence"] == {
            "assembler_runner_watcher_or_C27_C28_C29_module_imported": False,
            "stdlib_only": True,
            "fresh_join_and_DSU_recomputed": True,
        }, label + ":implementation independence")
        require(document["formal_credit"] == 0
                and document["manifest_authorized"] is False
                and document["C27R2_C28_C29"]
                    == "UNAUTHORIZED_PENDING_ACTUAL_V2_TERMINAL_SEAL"
                and document["CM2"] == "NO-GO_FOR_CLAIM",
                label + ":zero-credit governance")
        require(document["semantic_projection_sha256"]
                == semantic_hash(document), label + ":semantic closure")
def resign(document: dict[str, Any]) -> None:
    document.pop("verification_sha256", None)
    document["semantic_projection_sha256"] = semantic_hash(document)
    document["verification_sha256"] = digest(document)


def set_nested(document: dict[str, Any], path: tuple[str, ...], value: Any) -> None:
    target: Any = document
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = value


def run(args: argparse.Namespace) -> dict[str, Any]:
    require(fsha(SELF) == args.expect_attack_harness_sha256,
            "attack harness self pin")
    verifier = (ROOT / args.verifier_source).resolve()
    require(ROOT in verifier.parents
            and fsha(verifier) == args.expect_verifier_sha256,
            "independent verifier pin")
    verification_path = (ROOT / args.verification).resolve()
    baseline = load(verification_path)
    accept(baseline, args.expect_verifier_sha256)

    mutations: list[tuple[str, str, tuple[str, ...], Any]] = [
        ("status_forged", "first", ("status",), "PASS_CREDIT"),
        ("execution_seed_duplicated", "first", ("execution_seeds",), [30660101, 30660101]),
        ("seed2_run_removed", "first", ("seed_runs",), {"30660101": baseline["seed_runs"]["30660101"]}),
        ("input_snapshot_diverged", "first", ("seed_runs", "30660991", "input_snapshot_sha256"), "0" * 64),
        ("mathematical_projection_diverged", "first", ("seed_runs", "30660991", "mathematical_projection_sha256"), "1" * 64),
        ("run_attestation_hash_malformed", "first", ("seed_runs", "30660101", "run_attestation_file_sha256"), "x"),
        ("candidate_total_forged", "first", ("exact_census", "candidate_total"), 7_486_075),
        ("proof_total_forged", "first", ("exact_census", "materialized_physical_proof_total"), 65_063),
        ("atom_denominator_forged", "first", ("exact_census", "primitive_atom_denominator"), 483_231),
        ("edge_total_forged", "first", ("exact_census", "full_component_edge_union_total"), 14_859),
        ("merge_total_forged", "first", ("exact_census", "fresh_DSU_successful_merges"), 14_191),
        ("cycle_total_forged", "first", ("exact_census", "fresh_DSU_cycle_edges"), 669),
        ("component_total_forged", "first", ("exact_census", "fresh_DSU_final_component_total"), 43_685),
        ("ledger_removed", "first", ("ledger_descriptors",), {key: value for key, value in baseline["ledger_descriptors"].items() if key != "full_component_edge_union"}),
        ("ledger_sha_malformed", "first", ("ledger_descriptors", "full_component_edge_union", "sha256"), "2" * 63),
        ("runner_pin_forged", "first", ("source_pins", "runner"), "3" * 64),
        ("assembler_pin_forged", "first", ("source_pins", "assembler"), "4" * 64),
        ("watcher_pin_forged", "first", ("source_pins", "seed2_handoff_watcher"), "5" * 64),
        ("verifier_pin_forged", "first", ("source_pins", "independent_verifier"), "6" * 64),
        ("module_import_claim_forged", "first", ("implementation_independence", "assembler_runner_watcher_or_C27_C28_C29_module_imported"), True),
        ("formal_credit_promoted", "first", ("formal_credit",), 1),
        ("manifest_authorized", "first", ("manifest_authorized",), True),
        ("premature_C27R2_authorization", "first", ("C27R2_C28_C29",), "AUTHORIZED"),
        ("CM2_promoted", "first", ("CM2",), "GO_FOR_CLAIM"),
    ]
    attacks: list[dict[str, Any]] = []
    for ordinal, (name, side, path, value) in enumerate(mutations, 1):
        target = copy.deepcopy(baseline)
        set_nested(target, path, value)
        resign(target)
        accepted = True
        reason = ""
        try:
            accept(target, args.expect_verifier_sha256)
        except (Reject, KeyError, TypeError, ValueError) as error:
            accepted = False
            reason = str(error)
        require(not accepted, "attack accepted:" + name)
        attacks.append({"ordinal": ordinal, "attack": name,
                        "coherently_resigned": True,
                        "verifier_decision": "REJECT", "reason": reason})
    body = {
        "schema": "cm2.c27-independent.primitive-twenty-family-gate-v5-actual-v2-dual-seed-coherent-attacks.v1",
        "status": "PASS_CONTROL_AND_24_OF_24_COHERENT_RESIGNED_ATTACKS_REJECTED__ZERO_CREDIT",
        "control_passed": True,
        "attack_count": len(attacks),
        "rejected_attack_count": len(attacks),
        "accepted_attack_count": 0,
        "attacks": attacks,
        "pins": {
            "verification_file_sha256": fsha(verification_path),
            "verification_object_sha256": baseline["verification_sha256"],
            "independent_verifier_source_sha256": args.expect_verifier_sha256,
            "attack_harness_source_sha256": args.expect_attack_harness_sha256,
        },
        "formal_credit": 0,
        "manifest_authorized": False,
        "C27R2_C28_C29": "UNAUTHORIZED_PENDING_ACTUAL_V2_TERMINAL_SEAL",
        "CM2": "NO-GO_FOR_CLAIM",
    }
    require(len(attacks) == 24, "exact 24 attacks")
    result = dict(body)
    result["attack_result_sha256"] = digest(result)
    output = (ROOT / args.out_file).resolve()
    require(ROOT in output.parents and not output.exists(), "fresh output")
    output.parent.mkdir(parents=True, exist_ok=True)
    descriptor = os.open(output, os.O_WRONLY | os.O_CREAT | os.O_EXCL
                         | getattr(os, "O_NOFOLLOW", 0), 0o600)
    try:
        os.write(descriptor, encode(result) + b"\n")
        os.fsync(descriptor)
    finally:
        os.close(descriptor)
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verification", required=True)
    parser.add_argument("--verifier-source", required=True)
    parser.add_argument("--expect-verifier-sha256", required=True)
    parser.add_argument("--expect-attack-harness-sha256", required=True)
    parser.add_argument("--out-file", required=True)
    args = parser.parse_args()
    try:
        result = run(args)
    except (Reject, KeyError, TypeError, ValueError, OSError,
            json.JSONDecodeError) as error:
        print("REJECT:" + str(error))
        return 2
    print(encode({"status": result["status"],
                  "attack_result_sha256":
                      result["attack_result_sha256"]}).decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
