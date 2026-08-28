#!/usr/bin/env python3
"""Coherent attacks for candidate-vs-incidence correction-v2."""

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
VERIFIER = HERE / "cm2_round306c27r2_source_g_fresh_actual_v5_rebuild_interface_correction_v2_verifier.py"


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def reclose(value: dict[str, Any]) -> None:
    value.pop("preflight_sha256", None)
    value["preflight_sha256"] = digest(value)


def write_new(path: Path, value: dict[str, Any]) -> None:
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
    p = argparse.ArgumentParser()
    p.add_argument("--preflight", required=True)
    p.add_argument("--notice", required=True)
    p.add_argument("--output", required=True)
    a = p.parse_args()
    spec = importlib.util.spec_from_file_location("correction_v2_verifier", VERIFIER)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    base = json.loads(Path(a.preflight).read_bytes())
    notice = json.loads(Path(a.notice).read_bytes())
    module.verify_document(base, notice)

    def ci(x: dict[str, Any], name: str) -> dict[str, Any]:
        return x["corrected_interface"][name]

    attacks: list[tuple[str, Callable[[dict[str, Any]], None], bool]] = [
        ("unclosed_promote", lambda x: x.__setitem__("formal_credit", 1), False),
        ("promote_credit", lambda x: x.__setitem__("formal_credit", 1), True),
        ("authorize_manifest", lambda x: x.__setitem__("manifest_authorized", True), True),
        ("authorize_C27", lambda x: x.__setitem__("C27_transition_totality", "AUTHORIZED"), True),
        ("authorize_C28", lambda x: x.__setitem__("C28_pair_routing", "AUTHORIZED"), True),
        ("authorize_C29", lambda x: x.__setitem__("C29_physical_maximality", "AUTHORIZED"), True),
        ("start_producer", lambda x: x.__setitem__("fresh_C27R2_producer_may_start", True), True),
        ("accept_v1", lambda x: x.__setitem__("actual_gate_v1_receipt_accepted", True), True),
        ("promote_old_seal", lambda x: x["append_only_supersession"].__setitem__("v1_receipt_disposition", "AUTHORITATIVE"), True),
        ("claim_old_modified", lambda x: x["append_only_supersession"].__setitem__("v1_files_modified", True), True),
        ("count_incidence_as_candidate", lambda x: x["semantic_judgment"].__setitem__("incidence_may_count_as_candidate", True), True),
        ("replace_pair_count_with_incidences", lambda x: x["semantic_judgment"].__setitem__("T07_T09_candidate_pair_count", 206_632), True),
        ("replace_incidence_count_with_pairs", lambda x: x["semantic_judgment"].__setitem__("T07_T09_atom_pair_incidence_count", 101_080), True),
        ("remove_unique_pair_terminal", lambda x: x["semantic_judgment"].__setitem__("candidate_pair_each_exactly_one_terminal", False), True),
        ("v1_actual_path", lambda x: ci(x, "actual_gate_receipt").__setitem__("path", ".cm2-runtime/audit/c27-primitive-twenty-family-gate-v5-actual-zero-credit-receipt-v1/receipt.json"), True),
        ("atomic_candidate_key", lambda x: ci(x, "candidate_ownership_ledger").__setitem__("unique_key", "atomic_candidate_key"), True),
        ("T00_count_add_C26", lambda x: ci(x, "candidate_ownership_ledger")["T00_rule"].__setitem__("candidate_count", 6_662_264), True),
        ("T00_C26_as_candidates", lambda x: ci(x, "candidate_ownership_ledger")["T00_rule"].__setitem__("C26_691424_is_absence_coverage_theorem_not_candidate_rows", False), True),
        ("T00_use_support_atoms", lambda x: ci(x, "candidate_ownership_ledger")["T00_rule"].__setitem__("uses_T07_T09_483232_atom_incidence_layer", True), True),
        ("T079_candidates_206632", lambda x: ci(x, "candidate_ownership_ledger")["T07_T08_T09_rule"].__setitem__("candidate_count", 206_632), True),
        ("G2A_adds_candidate", lambda x: ci(x, "candidate_ownership_ledger")["T07_T08_T09_rule"].__setitem__("G2A_alias_adds_candidate", True), True),
        ("incidence_key_candidate_only", lambda x: ci(x, "atom_pair_incidence_ledger").__setitem__("unique_key", "candidate_pair_key"), True),
        ("incidence_creates_candidate", lambda x: ci(x, "atom_pair_incidence_ledger").__setitem__("incidence_creates_new_candidate", True), True),
        ("forbid_multi_pair_atom", lambda x: ci(x, "atom_pair_incidence_ledger").__setitem__("atom_may_have_multiple_pairs_and_terminals", False), True),
        ("atom_denominator_62768", lambda x: ci(x, "atom_incidence_disposition_ledger").__setitem__("row_count", 62_768), True),
        ("proof_equals_incidence", lambda x: ci(x, "materialized_physical_proof_join_ledger").__setitem__("incidence_row_is_not_automatically_a_physical_proof", False), True),
        ("drop_member_pair", lambda x: ci(x, "materialized_physical_proof_join_ledger")["required_fields"].remove("ordered_C15_member_pair"), True),
        ("edge_as_candidate_universe", lambda x: ci(x, "full_component_edge_union_ledger").__setitem__("candidate_universe", True), True),
        ("drop_conflation_prohibition", lambda x: ci(x, "prohibited_conflations").remove("206632_INCIDENCES_AS_206632_NORMALIZED_CANDIDATES"), True),
        ("decrement_W", lambda x: x.__setitem__("Source_W_formal_remainder", 79), True),
        ("claim_GO", lambda x: x.__setitem__("CM2", "GO"), True),
    ]
    rejected, accepted = [], []
    for name, mutate, resign in attacks:
        candidate = copy.deepcopy(base)
        mutate(candidate)
        if resign:
            reclose(candidate)
        try:
            module.verify_document(candidate, notice)
        except Exception:
            rejected.append(name)
        else:
            accepted.append(name)
    result = {
        "schema": "cm2.round306c27r2.source-g-fresh-actual-v5-rebuild-interface-correction-v2.attacks.v1",
        "status": "PASS_ALL_CANDIDATE_VS_INCIDENCE_COHERENT_ATTACKS_REJECTED__ZERO_CREDIT" if not accepted else "FAIL_ATTACK_ACCEPTED",
        "attack_count": len(attacks),
        "rejected_count": len(rejected),
        "accepted_count": len(accepted),
        "rejected": rejected,
        "accepted": accepted,
        "attack_names": [name for name, _, _ in attacks],
        "formal_credit": 0,
        "manifest_authorized": False,
    }
    result["attack_result_sha256"] = digest(result)
    write_new(Path(a.output), result)
    print(canonical({"status": result["status"],
                     "attack_result_sha256": result["attack_result_sha256"]}).decode("ascii"))
    return 0 if not accepted and len(rejected) == len(attacks) else 2


if __name__ == "__main__":
    raise SystemExit(main())
