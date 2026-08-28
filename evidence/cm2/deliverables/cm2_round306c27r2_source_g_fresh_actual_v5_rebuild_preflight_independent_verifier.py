#!/usr/bin/env python3
"""No-producer-import verifier for the C27R2 actual-v5 preflight REJECT."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import os
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
WORKSPACE = HERE.parent
C15 = HERE / "cm2_round306c15_source_g_502204_member_fresh_dsu_freeze_member_component_ledger.jsonl.gz"
ACTUAL = (WORKSPACE / ".cm2-runtime/audit/"
          "c27-primitive-twenty-family-gate-v5-actual-zero-credit-receipt-v1/receipt.json")
C15_SHA256 = "e70c667fd8f14cb3c3d6444bb752dfc86244e61be292a9f884889d53951ff25a"
C15_SIZE = 142_025_813

TERMINALS = [
    "SAME_CHART_RELATIVE_CELLS", "RETAINED_CONTINUATION", "OUTGOING_GRAPHS",
    "SINGLE_GRAPHS", "DOUBLE_GRAPHS", "SHEET_OWNER", "SHEET_SHADOW",
    "SIGNED_BOUNDARY_FACES", "COMPLETE_BOUNDARY_FACES",
    "POSITIVE_VOLUME_CARRIERS", "INCLUDED_STRATUM_ATTACHMENTS",
    "REVERSE_RECHART", "TRUE_CYCLIC_SEAM_E_TO_N",
    "TRUE_CYCLIC_SEAM_N_TO_W", "TRUE_CYCLIC_SEAM_W_TO_S",
    "TRUE_CYCLIC_SEAM_S_TO_E", "Jx_NEGATIVE_CONTROL", "Jy_NEGATIVE_CONTROL",
    "JxJy_NEGATIVE_CONTROL", "REPRESENTATION_ALIASES",
]
AUTHORITY_SLOTS = [
    f"T{ordinal:02d}_{terminal}" for ordinal, terminal in enumerate(TERMINALS)
]

FORBIDDEN = [
    "OLD_C27_FAMILIES", "OLD_C27_TRANSITION_CANDIDATE_LEDGER",
    "OLD_C27_TRANSITION_FAMILY_COVERAGE_LEDGER", "OLD_C28_PAIR_ROUTING",
    "OLD_C29_PHYSICAL_MAXIMALITY",
    "HISTORICAL_EDGE_LEDGER_AS_CANDIDATE_UNIVERSE",
    "STRICT_VOLUME_14772_AS_GLOBAL_CANDIDATE_UNIVERSE",
    "SCOPED_THREE_TERMINAL_14724_AS_GLOBAL_CANDIDATE_UNIVERSE",
]

RECEIPT_SCHEMA = (
    "cm2.c27-independent.primitive-twenty-family-gate-v5-actual-zero-credit-receipt.v1"
)
NORMALIZED_SCHEMA = (
    "cm2.c27-independent.primitive-twenty-family-gate-v5-actual."
    "normalized-primitive-authority.row.v1"
)
ATOMIC_SCHEMA = (
    "cm2.c27-independent.primitive-twenty-family-gate-v5-actual.atomic-ownership.row.v1"
)
PROOF_SCHEMA = (
    "cm2.c27-independent.primitive-twenty-family-gate-v5-actual."
    "materialized-proof-row-join.row.v1"
)
EDGE_SCHEMA = (
    "cm2.c27-independent.primitive-twenty-family-gate-v5-actual."
    "full-component-edge-union.row.v1"
)


class Reject(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Reject(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def file_sha(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(4 << 20):
            state.update(block)
    return state.hexdigest()


def verify_document(value: dict[str, Any], check_current_absence: bool = True) -> dict[str, Any]:
    body = dict(value)
    claimed = body.pop("preflight_sha256", None)
    need(type(claimed) is str and claimed == digest(body), "preflight closure")
    need(value.get("schema") ==
         "cm2.round306c27r2.source-g-fresh-actual-v5-rebuild-preflight.v1",
         "schema")
    need(value.get("status") ==
         "REJECT_MISSING_OR_INVALID_ACTUAL_V5_TWENTY_FAMILY_AUTHORITY__"
         "NO_C27_AUTHORIZATION__ZERO_CREDIT", "truthful reject status")
    need(value.get("decision") == "REJECT"
         and value.get("intended_process_exit_code") == 2,
         "reject exit contract")
    need(value.get("missing_required_authority") ==
         ["ACTUAL_V5_TWENTY_FAMILY_TERMINAL_RECEIPT"]
         and value.get("invalid_required_authority") == [],
         "exact missing authority")
    if check_current_absence:
        need(not ACTUAL.exists(), "actual receipt appeared; historical absence no longer current")
    need(value.get("fresh_C27R2_producer_may_start") is False,
         "producer start withheld")
    need(value.get("C27_transition_totality") == "UNAUTHORIZED"
         and value.get("C28_pair_routing") == "UNAUTHORIZED"
         and value.get("C29_physical_maximality") == "UNAUTHORIZED"
         and value.get("C29_patch_or_preservation_permitted") is False,
         "C27-C29 fail closed")
    need(value.get("formal_credit") == 0
         and value.get("manifest_authorized") is False
         and value.get("Source_W_transition_authorized") is False
         and value.get("Source_W_formal_remainder") == 80
         and value.get("CM2") == "NO-GO_FOR_CLAIM",
         "global nonpromotion")
    need(value.get("forbidden_dependencies") == FORBIDDEN
         and value.get("forbidden_dependency_open_count") == 0,
         "forbidden dependencies")

    interface = value.get("input_interface")
    need(type(interface) is dict, "interface object")
    receipt = interface.get("actual_gate_receipt", {})
    need(receipt.get("path") ==
         ".cm2-runtime/audit/c27-primitive-twenty-family-gate-v5-actual-zero-credit-receipt-v1/receipt.json"
         and receipt.get("schema") == RECEIPT_SCHEMA
         and receipt.get("closure_field") == "receipt_sha256",
         "actual receipt interface")
    need(receipt.get("required_state") == {
        "formal_credit": 0, "manifest_authorized": False,
        "primitive_twenty_family_totality_proved": True,
        "terminal_count": 20, "open_terminal_count": 0, "unresolved": 0,
    }, "actual receipt required state")
    primitive = interface.get("primitive_authorities", {})
    need(primitive.get("entry_count") == 20
         and primitive.get("terminal_order") == TERMINALS
         and primitive.get("authority_slot_order") == AUTHORITY_SLOTS
         and primitive.get("normalized_candidate_ledger_row_schema") == NORMALIZED_SCHEMA
         and primitive.get("normalized_candidate_unique_key") == "atomic_candidate_key",
         "primitive authority contract")
    atomic = interface.get("atomic_ownership_ledger", {})
    proof = interface.get("materialized_proof_row_join_ledger", {})
    edge = interface.get("full_component_edge_union_ledger", {})
    need(atomic.get("row_schema") == ATOMIC_SCHEMA
         and atomic.get("unique_key") == "atomic_candidate_key"
         and atomic.get("ordering") == ["atomic_candidate_key"],
         "atomic contract")
    need(proof.get("row_schema") == PROOF_SCHEMA
         and proof.get("unique_key") == "proof_row_key"
         and proof.get("ordering") == ["atomic_candidate_key", "proof_row_key"]
         and "ordered_C15_member_pair" in proof.get("required_fields", [])
         and "physical_witness_key" in proof.get("required_fields", []),
         "proof contract")
    need(edge.get("row_schema") == EDGE_SCHEMA
         and edge.get("unique_key") == "component_edge_key"
         and edge.get("ordering") == ["ordered_C15_component_pair"]
         and edge.get("authority_rule") ==
         "EXACTLY_DERIVED_FROM_MATERIALIZED_PROOF_MEMBER_PAIRS_THROUGH_"
         "FROZEN_C15_MAP__NEVER_A_CANDIDATE_UNIVERSE",
         "edge contract")
    need(interface.get("fixed_census") == {
        "frozen_C15_members": 502_204,
        "initial_frozen_C15_components": 57_876,
        "terminal_count": 20, "open_terminal_count": 0, "unresolved": 0,
    }, "fixed census")
    need(interface.get("derived_not_hardcoded_census") == [
        "global_atomic_candidate_count", "materialized_proof_row_count",
        "full_component_edge_count", "fresh_DSU_rank", "fresh_component_count",
    ], "derived census list")
    need(interface.get("scoped_not_global_census") == {
        "three_terminal_pair_rows": 101_080,
        "three_terminal_atom_denominator": 483_232,
        "same_chart_strict_volume_rows": 187_132,
        "same_chart_lower_exact_contact_rows": 5_783_708,
        "may_be_summed_or_used_as_global_universe": False,
    }, "scoped-not-global census")

    observed = value.get("observed_frozen_C15", {})
    capture = observed.get("capture", {})
    need(observed.get("members") == 502_204
         and observed.get("components") == 57_876
         and capture.get("path") ==
         "deliverables/cm2_round306c15_source_g_502204_member_fresh_dsu_freeze_member_component_ledger.jsonl.gz"
         and capture.get("size") == C15_SIZE
         and capture.get("sha256") == C15_SHA256
         and capture.get("O_NOFOLLOW") is True
         and capture.get("single_open_file_description_hash_parse_fstat") is True,
         "C15 capture")
    need(value.get("derived_actual_gate_summary_if_valid") is None,
         "no derived actual summary while missing")
    edge_governance = value.get("edge_universe_governance", {})
    need(edge_governance.get("edge_candidate_source") ==
         "MATERIALIZED_PRIMITIVE_PROOF_MEMBER_PAIRS_MAPPED_THROUGH_FROZEN_C15"
         and edge_governance.get("actual_gate_edge_ledger_role") ==
         "EXACT_AFTER_THE_FACT_COMPARATOR_ONLY"
         and edge_governance.get("strict_or_scoped_edge_ledger_used_as_candidate_universe") is False,
         "edge universe governance")
    algorithm = value.get("fresh_rebuild_algorithm")
    need(type(algorithm) is list and len(algorithm) == 9
         and algorithm[0].startswith("UNION_TWENTY_NORMALIZED")
         and "REBUILD_NEW_DSU" in algorithm[6]
         and algorithm[-1].startswith("RUN_INDEPENDENT_NO_IMPORT"),
         "fresh rebuild algorithm")
    root = value.get("root_input_capture", {})
    need(root.get("all_opened_inputs_single_stable_O_NOFOLLOW_FD_hash_parse_fstat") is True
         and root.get("actual_authorities_if_present") == {},
         "root capture")
    return {"preflight_sha256": claimed, "truthful_reject": True}


def independent_c15() -> dict[str, Any]:
    need(C15.stat().st_size == C15_SIZE and file_sha(C15) == C15_SHA256,
         "independent C15 file pin")
    members = set()
    components = set()
    with gzip.open(C15, "rb") as stream:
        for ordinal, line in enumerate(stream):
            need(line.endswith(b"\n"), f"C15 newline:{ordinal}")
            payload = line[:-1]
            row = json.loads(payload)
            need(type(row) is dict and canonical(row) == payload,
                 f"C15 canonical:{ordinal}")
            body = dict(row)
            claimed = body.pop("row_sha256", None)
            need(type(claimed) is str and claimed == digest(body),
                 f"C15 closure:{ordinal}")
            need(row.get("member_ordinal") == ordinal, f"C15 ordinal:{ordinal}")
            member = row.get("registry_member_id")
            component = row.get("fresh_component_id")
            need(member not in members, f"C15 duplicate member:{ordinal}")
            members.add(member)
            components.add(component)
    need((len(members), len(components)) == (502_204, 57_876),
         "independent C15 census")
    return {"members": len(members), "components": len(components),
            "file_sha256": C15_SHA256}


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
    try:
        raw = Path(args.preflight).read_bytes()
        need(raw.endswith(b"\n") and b"\n" not in raw[:-1], "single preflight")
        value = json.loads(raw[:-1])
        need(type(value) is dict and canonical(value) == raw[:-1], "canonical preflight")
        verified = verify_document(value)
        c15 = independent_c15()
        result = {
            "schema": "cm2.round306c27r2.source-g-fresh-actual-v5-rebuild-preflight-independent-verification.v1",
            "status": "PASS_INDEPENDENT_NO_IMPORT_TRUTHFUL_REJECT_AND_LOCKED_ACTUAL_INTERFACE__ZERO_CREDIT",
            "verified_preflight": verified,
            "independent_C15": c15,
            "producer_module_imported": False,
            "old_C27_C28_C29_or_historical_edge_ledger_read": False,
            "formal_credit": 0,
            "manifest_authorized": False,
        }
        result["verification_sha256"] = digest(result)
        write_exclusive(Path(args.output), result)
    except (Reject, KeyError, TypeError, ValueError, OSError) as error:
        print("FAIL:" + str(error))
        return 2
    print(canonical({"status": result["status"],
                     "verification_sha256": result["verification_sha256"]}).decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
