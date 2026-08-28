#!/usr/bin/env python3
"""Coherent mutation attacks for the primitive 20-terminal fail-close gate."""

from __future__ import annotations

import argparse
import copy
import importlib.util
from pathlib import Path
import subprocess
import sys
from typing import Any, Callable


ROOT = Path(__file__).resolve().parent
PRODUCER = ROOT / "cm2_c27_primitive_twenty_family_partition_gate.py"
VERIFIER = ROOT / "cm2_c27_primitive_twenty_family_partition_independent_verifier.py"


def load_verifier():
    spec = importlib.util.spec_from_file_location("primitive_twenty_independent_verifier", VERIFIER)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load independent verifier")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def reclose(value: dict[str, Any], verifier: Any) -> None:
    for row in value.get("grammar", {}).get("terminals", []):
        body = dict(row)
        body.pop("row_sha256", None)
        row["row_sha256"] = verifier.digest(body)
    body = dict(value)
    body.pop("result_sha256", None)
    value["result_sha256"] = verifier.digest(body)


def obtain_baseline(candidate_json: str | None, verifier: Any) -> dict[str, Any]:
    if candidate_json is not None:
        return verifier.parse_candidate_bytes(Path(candidate_json).read_bytes())
    run = subprocess.run(
        [sys.executable, "-I", "-B", str(PRODUCER)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if run.returncode != 2 or run.stderr != b"":
        raise RuntimeError(f"unexpected producer boundary rc={run.returncode} stderr={run.stderr[:200]!r}")
    return verifier.parse_candidate_bytes(run.stdout)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate-json")
    args = parser.parse_args()
    if sys.flags.isolated != 1 or sys.dont_write_bytecode is not True:
        raise RuntimeError("run with python -I -B")
    verifier = load_verifier()
    baseline = obtain_baseline(args.candidate_json, verifier)
    evidence = verifier.collect_source_evidence()
    baseline_receipt = verifier.verify_candidate_dict(baseline, evidence)

    attacks: list[tuple[str, Callable[[dict[str, Any]], None]]] = []

    attacks.append(("promote_reject_status_to_pass", lambda d: d.__setitem__("status", "PASS_PHYSICAL_TOTALITY")))
    attacks.append(("claim_old_family_source_read", lambda d: d.__setitem__("C27_source_or_FAMILIES_imported_or_read", True)))
    attacks.append(("claim_edge_ledger_candidate_universe", lambda d: d.__setitem__("edge_ledger_used_as_candidate_universe", True)))
    attacks.append(("rotate_primitive_chart_cycle", lambda d: d.__setitem__("primitive_chart_cycle", ["N", "W", "S", "E"])))
    attacks.append(("claim_physical_totality_pass", lambda d: d["grammar"].__setitem__("physical_totality", "PASS")))
    attacks.append(("inflate_closed_terminal_count", lambda d: d.__setitem__("closed_zero_credit_terminal_count", 15)))
    attacks.append(("deflate_remaining_terminal_count", lambda d: d.__setitem__("remaining_terminal_totality_proof_count", 5)))
    attacks.append(("mint_formal_credit", lambda d: d.__setitem__("formal_credit", 1)))
    attacks.append(("promote_c27_c28_c29", lambda d: d.__setitem__("C27_C28_C29", "PASS")))
    attacks.append(("promote_cm2", lambda d: d.__setitem__("CM2", "GO_FOR_CLAIM")))
    attacks.append(("spoof_c15_universe", lambda d: d["primitive_universes"].__setitem__("C15_member_count", 502_203)))

    def spoof_semantics(d: dict[str, Any]) -> None:
        census = d["primitive_universes"]["C25_support_semantic_census"]
        census["EXACT_MEMBER_SUPPORT_EQUALITY"] -= 1
        census["FINITE_CELL_UNION_MEMBER_SUPPORT_EQUALITY"] += 1

    attacks.append(("spoof_c25_semantic_partition", spoof_semantics))

    def spoof_nodes(d: dict[str, Any]) -> None:
        census = d["primitive_universes"]["C26_node_census"]
        census["A1"] -= 1
        census["A2"] += 1

    attacks.append(("spoof_c26_node_partition", spoof_nodes))

    def promote_one_open_terminal(d: dict[str, Any]) -> None:
        row = next(x for x in d["terminal_obligations"] if x["terminal"] == "SAME_CHART_RELATIVE_CELLS")
        row["state"] = "LOCAL_SUBGATE_CLOSED_ZERO_CREDIT"
        d["closed_zero_credit_terminal_count"] = 15
        d["remaining_terminal_totality_proof_count"] = 5

    attacks.append(("promote_unproved_support_terminal", promote_one_open_terminal))

    def disable_primitive_generation(d: dict[str, Any]) -> None:
        d["terminal_obligations"][0]["must_prove_candidate_generation_from_primitive_geometry"] = False

    attacks.append(("disable_primitive_candidate_generation", disable_primitive_generation))

    def disable_unique_assignment(d: dict[str, Any]) -> None:
        d["terminal_obligations"][1]["must_prove_unique_terminal_assignment"] = False

    attacks.append(("disable_unique_terminal_assignment", disable_unique_assignment))

    def disable_witness_routing(d: dict[str, Any]) -> None:
        d["terminal_obligations"][2]["must_reject_or_route_every_cross_component_witness"] = False

    attacks.append(("disable_cross_component_witness_routing", disable_witness_routing))

    def drop_support_terminal(d: dict[str, Any]) -> None:
        removed = d["grammar"]["terminals"].pop(0)
        d["terminal_obligations"] = [x for x in d["terminal_obligations"] if x["terminal"] != removed["terminal"]]
        d["grammar"]["terminal_count"] = 19
        d["grammar"]["support_stratum_terminal_count"] = 10
        d["remaining_terminal_totality_proof_count"] = 5
        for ordinal, row in enumerate(d["grammar"]["terminals"]):
            row["ordinal"] = ordinal

    attacks.append(("drop_one_support_terminal_and_recount", drop_support_terminal))

    def duplicate_terminal(d: dict[str, Any]) -> None:
        d["grammar"]["terminals"][1]["terminal"] = d["grammar"]["terminals"][0]["terminal"]
        d["terminal_obligations"][1]["terminal"] = d["terminal_obligations"][0]["terminal"]

    attacks.append(("duplicate_terminal_identity", duplicate_terminal))

    def relabel_branch(d: dict[str, Any]) -> None:
        target = next(x for x in d["grammar"]["terminals"] if x["terminal"] == "SHEET_OWNER")
        target["branch"] = "ATLAS_MAP"

    attacks.append(("relabel_support_as_atlas_branch", relabel_branch))

    def demote_closed_terminal(d: dict[str, Any]) -> None:
        row = next(x for x in d["terminal_obligations"] if x["terminal"] == "DOUBLE_GRAPHS")
        row["state"] = "INDEPENDENT_TOTALITY_PROOF_REQUIRED"
        d["closed_zero_credit_terminal_count"] = 13
        d["remaining_terminal_totality_proof_count"] = 7

    attacks.append(("erase_existing_zero_credit_subgate", demote_closed_terminal))

    def forge_included_stratum_receipt(d: dict[str, Any]) -> None:
        d["closed_subgate_receipts"][3]["candidate_count"] = 10_659

    attacks.append(("forge_included_stratum_receipt_binding", forge_included_stratum_receipt))

    def forge_retained_receipt(d: dict[str, Any]) -> None:
        d["closed_subgate_receipts"][0]["candidate_representation_ids_sha256"] = "0" * 64

    attacks.append(("forge_retained_continuation_receipt_binding", forge_retained_receipt))

    def forge_outgoing_graphs_receipt(d: dict[str, Any]) -> None:
        d["closed_subgate_receipts"][1]["candidate_count"] = 263

    attacks.append(("forge_outgoing_graphs_receipt_binding", forge_outgoing_graphs_receipt))

    def forge_single_graphs_receipt(d: dict[str, Any]) -> None:
        d["closed_subgate_receipts"][2]["materialized_proof_row_count"] = 14_551

    attacks.append(("forge_single_graphs_receipt_binding", forge_single_graphs_receipt))

    def forge_joint_intersection(d: dict[str, Any]) -> None:
        d["joint_boundary_bindings"][0]["intersection_count"] = 1

    attacks.append(("forge_retained_attachment_nonempty_intersection", forge_joint_intersection))

    def forge_joint_union_count(d: dict[str, Any]) -> None:
        d["joint_boundary_bindings"][0]["union_count"] = 10_935

    attacks.append(("forge_retained_attachment_union_count", forge_joint_union_count))

    def forge_joint_digest(d: dict[str, Any]) -> None:
        d["joint_boundary_bindings"][0]["attachment_excluded_adjacent_representation_ids_sha256"] = "f" * 64

    attacks.append(("forge_retained_attachment_identity_digest", forge_joint_digest))

    def erase_joint_binding(d: dict[str, Any]) -> None:
        d["joint_boundary_bindings"] = []

    attacks.append(("erase_retained_attachment_joint_binding", erase_joint_binding))

    def rewithhold_closed_attachment(d: dict[str, Any]) -> None:
        d["withheld_joint_boundary_receipts"] = [d["closed_subgate_receipts"].pop(3)]

    attacks.append(("re_withhold_closed_attachment", rewithhold_closed_attachment))

    def drop_single_receipt(d: dict[str, Any]) -> None:
        d["closed_subgate_receipts"].pop(2)

    attacks.append(("drop_single_graphs_receipt", drop_single_receipt))

    def erase_confirmed_witnesses(d: dict[str, Any]) -> None:
        d["legal_cross_component_witness_found"] = False
        d["legal_same_chart_witness_group_count"] = 0
        d["unique_witness_component_edge_count"] = 0
        d["same_chart_legal_witness_evidence"]["legal_cross_component_witness_found"] = False
        d["same_chart_legal_witness_evidence"]["witness_group_count"] = 0

    attacks.append(("erase_228_confirmed_legal_witness_groups", erase_confirmed_witnesses))

    def falsely_close_same_chart(d: dict[str, Any]) -> None:
        row = next(x for x in d["terminal_obligations"] if x["terminal"] == "SAME_CHART_RELATIVE_CELLS")
        row["state"] = "LOCAL_SUBGATE_CLOSED_ZERO_CREDIT"
        d["closed_zero_credit_terminal_count"] = 17
        d["remaining_terminal_totality_proof_count"] = 3
        d["remaining_terminal_totality_proofs"].remove("SAME_CHART_RELATIVE_CELLS")

    attacks.append(("misclose_same_chart_despite_open_totality", falsely_close_same_chart))

    def inflate_sixteen_to_twenty(d: dict[str, Any]) -> None:
        d["closed_zero_credit_terminal_count"] = 20
        d["remaining_terminal_totality_proof_count"] = 0
        d["remaining_terminal_totality_proofs"] = []
        for row in d["terminal_obligations"]:
            row["state"] = "LOCAL_SUBGATE_CLOSED_ZERO_CREDIT"

    attacks.append(("inflate_evidence_closed_16_to_20", inflate_sixteen_to_twenty))

    def promote_provisional_overlay_to_formal(d: dict[str, Any]) -> None:
        d["C27R1BC_provisional_overlay"]["authority"] = "FORMAL_C27R1_C28R1_C29R1_MAXIMALITY_SEAL"
        d["provisional_overlay_is_maximality_authority"] = True

    attacks.append(("promote_provisional_overlay_to_formal_maximality", promote_provisional_overlay_to_formal))

    def preserve_old_c29(d: dict[str, Any]) -> None:
        d["prior_C27_C28_C29_authority"] = "PRESERVED"
        d["C29_patch_or_preservation_permitted"] = True
        d["rebuild_required"] = False

    attacks.append(("preserve_old_C29_after_legal_witness", preserve_old_c29))

    def forge_owner_shadow_closure(d: dict[str, Any]) -> None:
        d["closed_subgate_receipts"][4]["candidate_count_per_terminal"] = 17_939

    attacks.append(("forge_owner_shadow_closed_subgate_binding", forge_owner_shadow_closure))

    def erase_boundary_blockers(d: dict[str, Any]) -> None:
        d["boundary_volume_unresolved_evidence"]["missing_endpoint_ownership_bit_count"] = 0
        d["boundary_volume_unresolved_evidence"]["three_terminal_unassigned_atom_count"] = 0

    attacks.append(("erase_boundary_volume_materialized_blockers", erase_boundary_blockers))

    def promote_boundary_terminals(d: dict[str, Any]) -> None:
        for row in d["terminal_obligations"]:
            if row["terminal"] in {"SIGNED_BOUNDARY_FACES", "COMPLETE_BOUNDARY_FACES", "POSITIVE_VOLUME_CARRIERS"}:
                row["state"] = "LOCAL_SUBGATE_CLOSED_ZERO_CREDIT"
        d["closed_zero_credit_terminal_count"] = 19
        d["remaining_terminal_totality_proof_count"] = 1
        d["remaining_terminal_totality_proofs"] = ["SAME_CHART_RELATIVE_CELLS"]

    attacks.append(("promote_three_boundary_terminals_without_authority", promote_boundary_terminals))

    def drop_cross_implementation_receipt(d: dict[str, Any]) -> None:
        d["same_chart_legal_witness_evidence"]["cross_implementation_receipt_file_sha256"] = "0" * 64

    attacks.append(("drop_same_chart_cross_implementation_binding", drop_cross_implementation_receipt))

    def mint_formal_credit_from_witnesses(d: dict[str, Any]) -> None:
        d["formal_credit"] = 192
        d["C27_C28_C29"] = "PASS"
        d["CM2"] = "GO_FOR_CLAIM"

    attacks.append(("mint_formal_credit_from_witness_overlay", mint_formal_credit_from_witnesses))

    rejected: list[str] = []
    for name, mutate in attacks:
        forged = copy.deepcopy(baseline)
        mutate(forged)
        reclose(forged, verifier)
        try:
            verifier.verify_candidate_dict(forged, evidence)
        except Exception:
            rejected.append(name)
        else:
            raise RuntimeError("independent verifier accepted coherent attack:" + name)

    receipt = {
        "status": f"PASS_{len(attacks)}_OF_{len(attacks)}_COHERENT_MUTATION_ATTACKS_REJECTED__ZERO_CREDIT_FAIL_CLOSE",
        "baseline_independent_verifier_status": baseline_receipt["status"],
        "candidate_result_sha256": baseline["result_sha256"],
        "rejected_attacks": rejected,
        "closed_zero_credit_terminal_count": 16,
        "remaining_terminal_totality_proof_count": 4,
        "legal_same_chart_witness_group_count": 228,
        "unique_witness_component_edge_count": 192,
        "prior_C27_C28_C29_authority": "INVALIDATED__REBUILD_REQUIRED",
        "provisional_overlay_authority": "PROVISIONAL_UPPER_BOUND_ONLY",
        "formal_credit": 0,
        "C27_C28_C29": "REJECT_AND_REBUILD_REQUIRED",
        "CM2": "NO-GO_FOR_CLAIM",
    }
    print(verifier.canonical(receipt).decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
