#!/usr/bin/env python3
"""Coherent re-closed attacks for the post-actual-v5 rebuild preflight."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile
from typing import Any, Callable


WORKSPACE = Path(__file__).resolve().parent.parent


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


def append_new(path: Path, value: dict[str, Any]) -> None:
    path = path.resolve()
    need(path.is_relative_to(WORKSPACE), "output:workspace")
    path.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL
                 | getattr(os, "O_NOFOLLOW", 0), 0o600)
    try:
        os.write(fd, canonical(value) + b"\n")
        os.fsync(fd)
    finally:
        os.close(fd)


def set_path(value: dict[str, Any], path: tuple[Any, ...], replacement: Any) -> None:
    cursor: Any = value
    for key in path[:-1]:
        cursor = cursor[key]
    cursor[path[-1]] = replacement


def reclose(value: dict[str, Any]) -> None:
    value.pop("preflight_sha256", None)
    value["preflight_sha256"] = digest(value)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--receipt", required=True)
    parser.add_argument("--producer", required=True)
    parser.add_argument("--verifier", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    try:
        receipt_path = Path(args.receipt).resolve()
        producer = Path(args.producer).resolve()
        verifier = Path(args.verifier).resolve()
        pristine = json.loads(receipt_path.read_bytes())
        mutations: list[tuple[str, Callable[[dict[str, Any]], None]]] = []

        def add(name: str, path: tuple[Any, ...], replacement: Any) -> None:
            mutations.append((name, lambda value, p=path, r=replacement: set_path(value, p, r)))

        add("status_promoted", ("status",), "PASS")
        add("decision_promoted", ("decision",), "PASS")
        add("intended_exit_zero", ("intended_process_exit_code",), 0)
        add("actual_falsely_present", ("observed_actual_gate_receipt_present",), True)
        add("actual_blocker_removed", ("blocking_authorities",), ["T00_SEALED_SUBAUTHORITY_TRANSITIVELY_REQUIRED_BY_ACTUAL_V5"])
        add("T00_blocker_removed", ("blocking_authorities",), ["ACTUAL_V5_TWENTY_FAMILY_TERMINAL_RECEIPT_V2"])
        add("sealed_candidate_subtotal_forged", ("sealed_subauthority_subtotal", "candidate_count"), 1_515_237)
        add("sealed_proof_subtotal_forged", ("sealed_subauthority_subtotal", "proof_count"), 32_825)
        add("sealed_disposition_forged", ("sealed_subauthority_subtotal", "dispositions", "SAME_FROZEN_C15_COMPONENT__NO_EDGE"), 109_265)
        add("T00_candidate_forged", ("T00_expected_reconciliation_not_yet_consumed", "candidate_count"), 5_970_841)
        add("T00_proof_forged", ("T00_expected_reconciliation_not_yet_consumed", "proof_count"), 32_241)
        add("T00_disposition_forged", ("T00_expected_reconciliation_not_yet_consumed", "dispositions", "NO_COMPONENT_EDGE_BY_TERMINAL_SEMANTICS"), 5_783_707)
        add("T00_path_forged", ("T00_expected_reconciliation_not_yet_consumed", "future_seal_receipt_path"), "old-C27/FAMILIES.json")
        add("global_candidate_count_forged", ("eventual_exact_global_conservation", "candidate_count"), 7_486_075)
        add("global_proof_count_forged", ("eventual_exact_global_conservation", "proof_count"), 65_063)
        add("global_disposition_forged", ("eventual_exact_global_conservation", "dispositions", "CROSS_COMPONENT__MATERIALIZED_PHYSICAL_PROOF_REQUIRED"), 65_063)
        add("global_disposition_sum_forged", ("eventual_exact_global_conservation", "disposition_sum"), 7_486_075)
        add("producer_start_promoted", ("fresh_C27R2_C28_C29_producer_may_start",), True)
        add("formal_credit_promoted", ("formal_credit",), 1)
        add("manifest_authorized", ("manifest_authorized",), True)
        add("C27R2_promoted", ("C27R2",), "AUTHORIZED")
        add("C28_promoted", ("C28",), "AUTHORIZED")
        add("C29_promoted", ("C29",), "AUTHORIZED")
        add("Source_W_promoted", ("Source_W_transition_authorized",), True)
        add("Source_W_remainder_lowered", ("Source_W_formal_remainder",), 78)
        add("CM2_promoted", ("CM2",), "CLAIM_READY")
        add("corrected_interface_pin_forged", ("corrected_interface_object_sha256",), "0" * 64)
        add("producer_source_pin_forged", ("producer_source_sha256",), "0" * 64)
        add("sealed_receipt_pin_forged", ("sealed_subauthorities_consumed", 0, "receipt", "sha256"), "0" * 64)
        add("sealed_replay_pin_forged", ("sealed_subauthorities_consumed", 1, "cold_replay", "sha256"), "0" * 64)
        add("actual_schema_downgraded", ("pipeline_contract", "actual_gate_receipt", "schema"), "cm2.c27-independent.primitive-twenty-family-gate-v5-actual-zero-credit-receipt.v1")
        add("actual_descriptor_removed", ("pipeline_contract", "actual_gate_receipt", "required_top_level_descriptors"), ["terminal_authority_descriptors"])
        add("candidate_total_forged", ("pipeline_contract", "global_candidate_ownership", "exact_rows"), 7_486_075)
        add("candidate_streaming_disabled", ("pipeline_contract", "global_candidate_ownership", "streaming_validation"), False)
        add("proof_total_forged", ("pipeline_contract", "materialized_physical_proof_join", "exact_rows"), 65_063)
        add("proof_order_forged", ("pipeline_contract", "materialized_physical_proof_join", "ordering"), ["proof_row_key"])
        add("noncross_proof_allowed", ("pipeline_contract", "materialized_physical_proof_join", "zero_proofs_for_non_cross_candidates"), False)
        add("historical_edge_authorized", ("pipeline_contract", "full_component_edge_union", "historical_14772_or_14724_accepted_as_authority"), True)
        add("edge_diagnostic_forged", ("pipeline_contract", "full_component_edge_union", "diagnostic_expected_count_not_authority"), 14_724)
        add("C15_hash_forged", ("pipeline_contract", "fresh_C29", "frozen_C15", "sha256"), "0" * 64)
        add("DSU_diagnostic_forged", ("pipeline_contract", "fresh_C29", "diagnostic_expected_final_components_not_authority"), 43_683)
        add("forbidden_old_C27_enabled", ("pipeline_contract", "forbidden_dependencies", "OLD_C27_FAMILIES"), True)

        results = []
        attack_parent = WORKSPACE / ".cm2-runtime/audit"
        attack_parent.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix="cm2-c27r2-attacks-",
                                         dir=attack_parent) as tmp:
            root = Path(tmp)
            for ordinal, (name, mutate) in enumerate(mutations):
                mutant = copy.deepcopy(pristine)
                mutate(mutant)
                reclose(mutant)
                mutant_path = root / f"attack-{ordinal:02d}.json"
                mutant_path.write_bytes(canonical(mutant) + b"\n")
                verify_out = root / f"verify-{ordinal:02d}.json"
                proc = subprocess.run([
                    os.fspath(Path(os.sys.executable)), os.fspath(verifier),
                    "--receipt", os.fspath(mutant_path),
                    "--producer", os.fspath(producer),
                    "--output", os.fspath(verify_out),
                ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
                need(proc.returncode != 0 and not verify_out.exists(), "attack accepted:" + name)
                results.append({
                    "ordinal": ordinal, "attack": name, "object_reclosed": True,
                    "verifier_exit_code": proc.returncode, "rejected": True,
                    "stderr_empty": proc.stderr == b"",
                    "stdout_sha256": hashlib.sha256(proc.stdout).hexdigest(),
                })

        body = {
            "schema": "cm2.round306c27r2-c28-c29.post-actual-v5-rebuild-preflight-coherent-attacks.v2",
            "status": f"PASS_{len(results)}_OF_{len(results)}_COHERENT_RECLOSED_ATTACKS_REJECTED__ZERO_CREDIT",
            "attacks": len(results), "rejected": len(results), "accepted": 0,
            "all_objects_reclosed_before_verification": True,
            "results": results,
            "receipt_file_sha256": hashlib.sha256(receipt_path.read_bytes()).hexdigest(),
            "producer_source_sha256": hashlib.sha256(producer.read_bytes()).hexdigest(),
            "verifier_source_sha256": hashlib.sha256(verifier.read_bytes()).hexdigest(),
            "formal_credit": 0, "manifest_authorized": False,
            "C27R2_C28_C29": "UNAUTHORIZED", "Source_W_formal_remainder": 80,
            "CM2": "NO-GO_FOR_CLAIM",
        }
        body["attacks_sha256"] = digest(body)
        append_new(Path(args.output), body)
        return 0
    except (Failure, KeyError, TypeError, ValueError, OSError,
            json.JSONDecodeError) as exc:
        print("REJECT:" + str(exc))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
