#!/usr/bin/env python3
"""Coherent re-signed attacks against the fresh C27R2 actual-v5 preflight."""

from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
from typing import Any, Callable


HERE = Path(__file__).resolve().parent
VERIFIER = HERE / "cm2_round306c27r2_source_g_fresh_actual_v5_rebuild_preflight_independent_verifier.py"


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def reclose(value: dict[str, Any]) -> None:
    value.pop("preflight_sha256", None)
    value["preflight_sha256"] = digest(value)


def write_exclusive(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = canonical(value) + b"\n"
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL
                 | getattr(os, "O_NOFOLLOW", 0), 0o600)
    try:
        os.write(fd, payload)
        os.fsync(fd)
    finally:
        os.close(fd)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--preflight", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    spec = importlib.util.spec_from_file_location("c27r2_actual_preflight_verifier", VERIFIER)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    raw = Path(args.preflight).read_bytes()
    base = json.loads(raw)
    module.verify_document(base, check_current_absence=False)

    def iface(x: dict[str, Any], name: str) -> dict[str, Any]:
        return x["input_interface"][name]

    attacks: list[tuple[str, Callable[[dict[str, Any]], None], bool]] = [
        ("unclosed_byte_tamper", lambda x: x.__setitem__("formal_credit", 1), False),
        ("promote_formal_credit", lambda x: x.__setitem__("formal_credit", 1), True),
        ("authorize_manifest", lambda x: x.__setitem__("manifest_authorized", True), True),
        ("authorize_C27", lambda x: x.__setitem__("C27_transition_totality", "AUTHORIZED"), True),
        ("authorize_C28", lambda x: x.__setitem__("C28_pair_routing", "AUTHORIZED"), True),
        ("authorize_C29", lambda x: x.__setitem__("C29_physical_maximality", "AUTHORIZED"), True),
        ("permit_C29_patch", lambda x: x.__setitem__("C29_patch_or_preservation_permitted", True), True),
        ("authorize_Source_W", lambda x: x.__setitem__("Source_W_transition_authorized", True), True),
        ("decrement_Source_W", lambda x: x.__setitem__("Source_W_formal_remainder", 79), True),
        ("remove_missing_actual", lambda x: x["missing_required_authority"].clear(), True),
        ("force_input_PASS", lambda x: x.__setitem__("decision", "PASS_INPUT_PREFLIGHT_ONLY"), True),
        ("force_exit_zero", lambda x: x.__setitem__("intended_process_exit_code", 0), True),
        ("force_producer_start", lambda x: x.__setitem__("fresh_C27R2_producer_may_start", True), True),
        ("force_PASS_status", lambda x: x.__setitem__("status", "PASS_COMPLETE_ACTUAL_V5_INPUT_FOR_SEPARATE_FRESH_C27R2_PRODUCER__NO_C27_AUTHORIZATION__ZERO_CREDIT"), True),
        ("inject_fake_actual_summary", lambda x: x.__setitem__("derived_actual_gate_summary_if_valid", {"fresh_component_count": 1}), True),
        ("change_actual_receipt_path", lambda x: iface(x, "actual_gate_receipt").__setitem__("path", "deliverables/old_C27.json"), True),
        ("change_actual_receipt_schema", lambda x: iface(x, "actual_gate_receipt").__setitem__("schema", "legacy"), True),
        ("allow_open_terminal", lambda x: iface(x, "actual_gate_receipt")["required_state"].__setitem__("open_terminal_count", 1), True),
        ("swap_terminal_order", lambda x: iface(x, "primitive_authorities")["terminal_order"].__setitem__(0, "SIGNED_BOUNDARY_FACES"), True),
        ("drop_terminal", lambda x: iface(x, "primitive_authorities")["terminal_order"].pop(), True),
        ("change_authority_slot", lambda x: iface(x, "primitive_authorities")["authority_slot_order"].__setitem__(0, "LEGACY_SAME_CHART"), True),
        ("change_normalized_schema", lambda x: iface(x, "primitive_authorities").__setitem__("normalized_candidate_ledger_row_schema", "old.C27.row"), True),
        ("change_normalized_unique_key", lambda x: iface(x, "primitive_authorities").__setitem__("normalized_candidate_unique_key", "component_edge_key"), True),
        ("change_atomic_schema", lambda x: iface(x, "atomic_ownership_ledger").__setitem__("row_schema", "coarse.atom.v0"), True),
        ("change_atomic_unique_key", lambda x: iface(x, "atomic_ownership_ledger").__setitem__("unique_key", "terminal"), True),
        ("drop_proof_member_pair", lambda x: iface(x, "materialized_proof_row_join_ledger")["required_fields"].remove("ordered_C15_member_pair"), True),
        ("drop_physical_witness", lambda x: iface(x, "materialized_proof_row_join_ledger")["required_fields"].remove("physical_witness_key"), True),
        ("change_proof_order", lambda x: iface(x, "materialized_proof_row_join_ledger").__setitem__("ordering", ["proof_row_key"]), True),
        ("change_edge_schema", lambda x: iface(x, "full_component_edge_union_ledger").__setitem__("row_schema", "historical.edge.v1"), True),
        ("promote_edge_ledger_to_universe", lambda x: iface(x, "full_component_edge_union_ledger").__setitem__("authority_rule", "CANDIDATE_UNIVERSE"), True),
        ("change_C15_member_census", lambda x: x["input_interface"]["fixed_census"].__setitem__("frozen_C15_members", 502_203), True),
        ("hardcode_final_components", lambda x: x["input_interface"]["derived_not_hardcoded_census"].remove("fresh_component_count"), True),
        ("promote_scoped_to_global", lambda x: x["input_interface"]["scoped_not_global_census"].__setitem__("may_be_summed_or_used_as_global_universe", True), True),
        ("open_forbidden_dependency", lambda x: x.__setitem__("forbidden_dependency_open_count", 1), True),
        ("delete_forbidden_dependency", lambda x: x["forbidden_dependencies"].pop(), True),
        ("use_strict_as_candidate_source", lambda x: x["edge_universe_governance"].__setitem__("edge_candidate_source", "STRICT_VOLUME_14772"), True),
        ("claim_scoped_universe", lambda x: x["edge_universe_governance"].__setitem__("strict_or_scoped_edge_ledger_used_as_candidate_universe", True), True),
        ("delete_fresh_DSU_step", lambda x: x["fresh_rebuild_algorithm"].pop(6), True),
        ("change_C15_hash", lambda x: x["observed_frozen_C15"]["capture"].__setitem__("sha256", "0" * 64), True),
        ("inject_actual_attestation", lambda x: x["root_input_capture"]["actual_authorities_if_present"].__setitem__("receipt", {}), True),
        ("change_CM2", lambda x: x.__setitem__("CM2", "GO"), True),
    ]

    rejected = []
    accepted = []
    for name, mutate, resign in attacks:
        candidate = copy.deepcopy(base)
        mutate(candidate)
        if resign:
            reclose(candidate)
        try:
            module.verify_document(candidate, check_current_absence=False)
        except Exception:
            rejected.append(name)
        else:
            accepted.append(name)
    result = {
        "schema": "cm2.round306c27r2.source-g-fresh-actual-v5-rebuild-preflight-attacks.v1",
        "status": (
            "PASS_ALL_COHERENT_ACTUAL_INTERFACE_AND_NONPROMOTION_ATTACKS_REJECTED__ZERO_CREDIT"
            if not accepted else "FAIL_ATTACK_ACCEPTED"
        ),
        "attack_count": len(attacks),
        "rejected_count": len(rejected),
        "accepted_count": len(accepted),
        "accepted": accepted,
        "rejected": rejected,
        "attack_names": [name for name, _, _ in attacks],
        "unmutated_control_passed": True,
        "formal_credit": 0,
        "manifest_authorized": False,
    }
    result["attack_result_sha256"] = digest(result)
    write_exclusive(Path(args.output), result)
    print(canonical({"status": result["status"],
                     "attack_result_sha256": result["attack_result_sha256"]}).decode("ascii"))
    return 0 if not accepted and len(rejected) == len(attacks) else 2


if __name__ == "__main__":
    raise SystemExit(main())
