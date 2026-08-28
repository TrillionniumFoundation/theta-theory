#!/usr/bin/env python3
"""Normalize the sixteen non-current C27 terminal authorities, fail closed.

This is deliberately not a C27 transition producer.  It reads only fresh
zero-credit subgate evidence plus primitive atlas/representation authorities;
it never reads the old C27 FAMILIES table, an old transition ledger, C28, C29,
or an edge ledger as a candidate universe.

The output distinguishes a real terminal receipt from merely useful evidence.
In particular, the old aggregate's syntactic statement that 16/20 terminals
were "closed" is not accepted as a substitute for terminal-level authority.
"""

from __future__ import annotations

import argparse
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parent.parent

PINS = {
    "retained_receipt": (
        "deliverables/cm2_c27_retained_continuation_subgate_receipt.json",
        "08b760876914406e2fbe4e897609afd6ffc6f3667acaf6a1b4a7a9df58f6e263"),
    "outgoing_receipt": (
        "deliverables/cm2_c27_outgoing_graphs_physical_totality_subgate_receipt.json",
        "39fc442c396038dfcfd9ca01a99c1188c87015b778bc8d15795a0336a8bbd5e9"),
    "single_receipt": (
        "deliverables/cm2_c27_single_graphs_subgate_receipt.json",
        "40435bf43d9bab01b54f9bc0a8c283930228e84a33f95d2af14783a2eb1d6ad5"),
    "owner_shadow_receipt": (
        "deliverables/cm2_c27_sheet_owner_shadow_physical_totality_subgate_receipt.json",
        "2833cc5f1c9d35eeca36722dfb348ad16e9d09e8d44d8983e63b61f390a93d0f"),
    "included_receipt": (
        "deliverables/cm2_c27_included_stratum_attachments_subgate_receipt.json",
        "d66d8aacb517a642684f3ddbe184e270936346726b73fa518c76f29076c184f5"),
    "outgoing_ledger_a": (
        ".cm2-runtime/audit/c27-outgoing-graphs-stream-seed-30627101/ledger.jsonl.gz",
        "3e915eb5f45d2e0cef6911b898d3f9653d13e2035c8d4129613021e82e9f5f4e"),
    "outgoing_ledger_b": (
        ".cm2-runtime/audit/c27-outgoing-graphs-stream-seed-30627901/ledger.jsonl.gz",
        "3e915eb5f45d2e0cef6911b898d3f9653d13e2035c8d4129613021e82e9f5f4e"),
    "single_ledger_a": (
        ".cm2-runtime/audit/c27-single-graphs-stream-seed-30628101/ledger.jsonl.gz",
        "72f34d0246799fa89338849c92c2f1a3e0048ef9d4e75f4da054812822496262"),
    "single_ledger_b": (
        ".cm2-runtime/audit/c27-single-graphs-stream-seed-30628901/ledger.jsonl.gz",
        "72f34d0246799fa89338849c92c2f1a3e0048ef9d4e75f4da054812822496262"),
    "owner_shadow_ledger_a": (
        ".cm2-runtime/audit/c27-sheet-owner-shadow-physical-stream-seed-30627401/sheet_owner_shadow_terminal_ledger.jsonl.gz",
        "3050f59733c5f5e183a3babc3ff1f2e772153b2e655997a3acd0826ad184fac2"),
    "owner_shadow_ledger_b": (
        ".cm2-runtime/audit/c27-sheet-owner-shadow-physical-stream-seed-30627941/sheet_owner_shadow_terminal_ledger.jsonl.gz",
        "3050f59733c5f5e183a3babc3ff1f2e772153b2e655997a3acd0826ad184fac2"),
    "double_reject_result": (
        ".cm2-runtime/audit/c27-semantic-double-graphs-v4-seed-30627931/"
        "cm2_c27_semantic_counterexample_gate_double_graphs_zero_credit_v2_result.json",
        "c96146746a748ec6d54782ceb9997d992f19a983c8bd9b695c071255f3a82d22"),
    "double_diagnostic_ledger": (
        ".cm2-runtime/audit/c27-semantic-double-graphs-v4-seed-30627931/"
        "cm2_c27_semantic_counterexample_gate_double_graphs_zero_credit_v2_candidate_partition_ledger.jsonl.gz",
        "7f3c6254735157d67a47dd89654733fbabe7a9893189e2b14ff9fa90396539f0"),
    "representation_alias_ledger": (
        "deliverables/cm2_round295a_source_g_r291_positive_t_retained_continuation_closure_representation_alias_ledger.json.gz",
        "5c826ef03dd6f8662528e565c36089422e590d1ebf9fc8bade99f1665c68ad2f"),
    "coordinate_bridge": (
        "deliverables/cm2_round171_compact_gate3_source_g_coordinate_bridge_certificate.json",
        "1fb4827b42569d41602765445d0333c76b2ef97615873fc406563ac0e18af7a5"),
    "coordinate_bridge_verification": (
        "deliverables/cm2_round171_compact_gate3_source_g_coordinate_bridge_verification.json",
        "effdfd4306dbf7bd70df1e9b5ed9166a58dc00a5d333b0f2f2a5f0cb930ccce9"),
    "primitive_atlas": (
        "deliverables/cm2_gate3_eight_cell_symmetry_atlas_cert.py",
        "d867f5cb03691289033d1a0d0e277a03e8395d70aae7e0689446d7aa63eac3da"),
    "quotient_result": (
        ".cm2-runtime/audit/c27-explicit-quotient-map-alias-v2-final-seed-30627301/"
        "cm2_c27_explicit_quotient_map_alias_zero_credit_v2_result.json",
        "b6e01dfbae63628931105d9884d9ece46329c2ebb9f629931117e9b2861a2adc"),
    "quotient_cohort_ledger": (
        ".cm2-runtime/audit/c27-explicit-quotient-map-alias-v2-final-seed-30627301/"
        "cm2_c27_explicit_quotient_map_alias_zero_credit_v2_equation_cohort_ledger.jsonl.gz",
        "32a3d1732446481761ccb521660874ab74a48bae39d941cef8cbdf6e22b4cccd"),
}

TERMINALS = (
    "RETAINED_CONTINUATION", "OUTGOING_GRAPHS", "SINGLE_GRAPHS",
    "DOUBLE_GRAPHS", "SHEET_OWNER", "SHEET_SHADOW",
    "INCLUDED_STRATUM_ATTACHMENTS", "REVERSE_RECHART",
    "TRUE_CYCLIC_SEAM_E_TO_N", "TRUE_CYCLIC_SEAM_N_TO_W",
    "TRUE_CYCLIC_SEAM_W_TO_S", "TRUE_CYCLIC_SEAM_S_TO_E",
    "Jx_NEGATIVE_CONTROL", "Jy_NEGATIVE_CONTROL",
    "JxJy_NEGATIVE_CONTROL", "REPRESENTATION_ALIASES",
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


def file_hash(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as handle:
        while block := handle.read(4 << 20):
            state.update(block)
    return state.hexdigest()


def checked_path(label: str) -> Path:
    rel, expected = PINS[label]
    path = ROOT / rel
    need(path.is_file() and not path.is_symlink(), label + ":regular")
    need(file_hash(path) == expected, label + ":sha256")
    return path


def document(label: str) -> dict[str, Any]:
    value = json.loads(checked_path(label).read_bytes())
    need(type(value) is dict, label + ":object")
    return value


def gzip_rows(label: str) -> Iterable[dict[str, Any]]:
    path = checked_path(label)
    with gzip.open(path, "rt", encoding="ascii") as handle:
        for ordinal, line in enumerate(handle):
            value = json.loads(line)
            need(type(value) is dict, f"{label}:{ordinal}:object")
            yield value


def closed_object(value: dict[str, Any], key: str, label: str) -> None:
    claim = value.get(key)
    body = dict(value)
    body.pop(key, None)
    need(type(claim) is str and claim == digest(body), label + ":closure")


def row(body: dict[str, Any]) -> dict[str, Any]:
    need("row_sha256" not in body, "new row closure absent")
    return {**body, "row_sha256": digest(body)}


def audit_receipt_authorities() -> dict[str, Any]:
    retained = document("retained_receipt")
    outgoing = document("outgoing_receipt")
    single = document("single_receipt")
    owner = document("owner_shadow_receipt")
    included = document("included_receipt")
    closed_object(outgoing, "receipt_sha256", "outgoing receipt")
    closed_object(owner, "receipt_sha256", "owner/shadow receipt")

    need(retained["status"] ==
         "PASS_LOCAL_ZERO_CREDIT__RETAINED_CONTINUATION_PHYSICAL_TOTALITY_AND_UNIQUE_ASSIGNMENT"
         and retained["terminal"] == "RETAINED_CONTINUATION"
         and retained["candidate_commitment"]["candidate_count"] == 276
         and retained["formal_credit"] == 0, "retained receipt semantics")
    need(outgoing["status"] ==
         "PASS_OUTGOING_GRAPHS_DUAL_SEMANTICS_DOUBLE_SEED_31_ATTACKS__ZERO_CREDIT"
         and outgoing["outgoing_roots"] == 264
         and outgoing["G2A_sheet_dispositions"] == 264
         and outgoing["G2B_side_dispositions"] == 528
         and outgoing["unresolved"] == 0 and outgoing["formal_credit"] == 0,
         "outgoing receipt semantics")
    need(single["status"] ==
         "PASS_LOCAL_ZERO_CREDIT__SINGLE_GRAPHS_PHYSICAL_TOTALITY_AND_UNIQUE_ASSIGNMENT"
         and single["terminal"] == "SINGLE_GRAPHS"
         and single["single_roots"] == 4_984
         and single["materialized_C15_C24_C25_C26_proof_rows"] == 14_552
         and single["unresolved"] == 0 and single["formal_credit"] == 0,
         "single receipt semantics")
    need(owner["status"] ==
         "PASS_SHEET_OWNER_SHADOW_DUAL_PHYSICAL_SEMANTICS_DOUBLE_SEED_50_ATTACKS__ZERO_CREDIT"
         and owner["terminal_census"] == {"SHEET_OWNER": 17_940,
                                           "SHEET_SHADOW": 17_940}
         and owner["unresolved"] == 0 and owner["formal_credit"] == 0,
         "owner/shadow receipt semantics")
    need(included["status"] ==
         "PASS_LOCAL_ZERO_CREDIT__INCLUDED_STRATUM_ATTACHMENTS_10660__276_EXCLUDED_AND_RESERVED_FOR_OPEN_RETAINED_CONTINUATION"
         and included["candidate_commitment"]["candidate_count"] == 10_660
         and included["terminal_credit_withheld_until_retained_continuation_joint_boundary"] is True
         and included["formal_credit"] == 0, "included receipt semantics")

    # Recompute the retained/attachment joint commitment rather than accepting
    # the old aggregate's claim that it was closed.
    rc = retained["candidate_commitment"]
    ic = included["candidate_commitment"]
    need(ic["excluded_adjacent_representation_ids_sha256"]
         == rc["candidate_representation_ids_sha256"], "joint boundary IDs")
    need(ic["C20D_adjacent_positive_t_excluded_and_reserved_for_open_retained_continuation"]
         == rc["candidate_count"] == 276, "joint boundary count")
    need(ic["candidate_excluded_intersection_count"] == 0
         and ic["candidate_plus_excluded_union_count"] == 10_936,
         "joint boundary disjoint union")

    return {"retained": retained, "outgoing": outgoing, "single": single,
            "owner": owner, "included": included}


def audit_materialized_rows() -> dict[str, Any]:
    outgoing_ids: set[str] = set()
    outgoing_dispositions = 0
    for item in gzip_rows("outgoing_ledger_a"):
        need(item["schema"] ==
             "cm2.c27.outgoing-graphs-physical-totality-zero-credit.v1.candidate-row.v1"
             and item["terminal"] == "OUTGOING_GRAPHS", "outgoing row schema")
        graph_id = item["graph_id"]
        need(graph_id not in outgoing_ids, "outgoing graph unique")
        outgoing_ids.add(graph_id)
        roles = Counter(value["role"] for value in item["dispositions"])
        need(roles == {"G2A_SHEET": 1, "G2B_SIDE": 2}
             and item["physical_totality_certificate"]["unresolved"] == 0,
             "outgoing row physical totality")
        outgoing_dispositions += len(item["dispositions"])
    need(len(outgoing_ids) == 264 and outgoing_dispositions == 792,
         "outgoing ledger census")
    need(checked_path("outgoing_ledger_a").read_bytes()
         == checked_path("outgoing_ledger_b").read_bytes(),
         "outgoing dual seed bytes")

    single_ids: set[str] = set()
    single_dispositions = 0
    single_role_census: Counter[str] = Counter()
    for item in gzip_rows("single_ledger_a"):
        need(item["schema"] ==
             "cm2.c27.single-graphs-physical-totality-zero-credit.v1.candidate-row.v1"
             and item["terminal"] == "SINGLE_GRAPHS", "single row schema")
        graph_id = item["graph_id"]
        need(graph_id not in single_ids, "single graph unique")
        single_ids.add(graph_id)
        need(item["physical_totality_certificate"]["unresolved"] == 0,
             "single row unresolved")
        single_role_census.update(value["role"] for value in item["dispositions"])
        single_dispositions += len(item["dispositions"])
    need(len(single_ids) == 4_984 and single_dispositions == 14_552,
         "single ledger census")
    need(single_role_census == {"G2A_SHEET": 4_984,
                                "G2B_POSITIVE_SIDE": 9_416,
                                "G2B_EXACT_EMPTY_SIDE": 152},
         "single disposition census")
    need(checked_path("single_ledger_a").read_bytes()
         == checked_path("single_ledger_b").read_bytes(),
         "single dual seed bytes")

    sheet_keys: set[tuple[str, str]] = set()
    sheet_roles: Counter[str] = Counter()
    member_pairs: set[tuple[str, str, str]] = set()
    for item in gzip_rows("owner_shadow_ledger_a"):
        need(item["schema"] ==
             "cm2.c27.sheet-owner-shadow-physical-totality.v1.row.v1",
             "sheet row schema")
        key = (item["physical_sheet_id"], item["role"])
        need(key not in sheet_keys, "sheet role unique")
        sheet_keys.add(key)
        sheet_roles[item["terminal"]] += 1
        member_pairs.add((item["physical_sheet_id"], item["owner_member_id"],
                          item["shadow_member_id"]))
        need(item["equality_sheet_included"] is (item["role"] == "OWNER"),
             "sheet half-open ownership")
    need(sheet_roles == {"SHEET_OWNER": 17_940, "SHEET_SHADOW": 17_940}
         and len(member_pairs) == 17_940, "sheet ledger census")
    need(checked_path("owner_shadow_ledger_a").read_bytes()
         == checked_path("owner_shadow_ledger_b").read_bytes(),
         "sheet dual seed bytes")

    alias_doc = json.load(gzip.open(checked_path("representation_alias_ledger"),
                                    "rt", encoding="ascii"))
    need(alias_doc["row_count"] == len(alias_doc["rows"]) == 276,
         "alias row count")
    alias_ids: set[str] = set()
    for item in alias_doc["rows"]:
        alias_id = item["Round295A_retained_continuation_alias_row_id"]
        need(alias_id not in alias_ids, "alias identity unique")
        alias_ids.add(alias_id)
        need(item["exact_full_face_shared"] is True
             and item["same_origin_unique_index1_sibling"] is True
             and item["formal_occurrence_alias_credit"] == 1
             and item["formal_identity_collapse_credit"] == 0
             and item["signature_or_box_equality_used_as_identity_basis"] is False
             and item["symmetry_used_as_identity_basis"] is False,
             "alias physical identity semantics")

    return {
        "outgoing_roots": len(outgoing_ids),
        "outgoing_dispositions": outgoing_dispositions,
        "single_roots": len(single_ids),
        "single_dispositions": single_dispositions,
        "single_role_census": dict(sorted(single_role_census.items())),
        "sheet_role_census": dict(sorted(sheet_roles.items())),
        "sheet_member_pairs": len(member_pairs),
        "representation_alias_rows": len(alias_ids),
    }


def audit_evidence_only() -> dict[str, Any]:
    double = document("double_reject_result")
    need(double["schema"] ==
         "cm2.c27-semantic-counterexample-gate.double-graphs.zero-credit.result.v2"
         and double["status"].startswith("REJECT_ZERO_CREDIT__")
         and double["unresolved_candidate_count"] == 1_361_872
         and double["ledger"]["row_count"] == 696,
         "double result remains reject")
    need(sum(1 for _ in gzip_rows("double_diagnostic_ledger")) == 696,
         "double diagnostic row count")

    bridge = document("coordinate_bridge")
    bridge_verify = document("coordinate_bridge_verification")
    need(bridge_verify["result"]["status"] == "PASS"
         and bridge_verify["result"]["producer_imported_or_executed"] is False
         and bridge_verify["result"]["all_four_source_G_seams_independently_reduced_in_Q_kappa"] is True,
         "coordinate bridge independent verification")
    seams = bridge["result"]["exact_source_G_coordinate_bridge"]["seam_rows"]
    expected = [("E", "N"), ("N", "W"), ("W", "S"), ("S", "E")]
    observed = []
    seam_evidence = {}
    for item in seams:
        pair = (item["left_face"]["chart"], item["right_face"]["chart"])
        observed.append(pair)
        need(item["left_face"]["z"] == "+kappa"
             and item["right_face"]["z"] == "-kappa"
             and item["normal_glues_exactly"] is True
             and item["source_G_position_glues_exactly"] is True
             and item["quarter_turn_and_velocity_glue_for_every_q"] is True,
             "true seam phase glue")
        seam_evidence[f"{pair[0]}_TO_{pair[1]}"] = {
            "left_face": item["left_face"], "right_face": item["right_face"],
            "common_normal_numerator_in_basis_1_kappa":
                item["common_normal_numerator_in_basis_1_kappa"],
            "full_phase_glue": True}
    need(observed == expected, "true seam cyclic order")

    quotient = document("quotient_result")["result"]
    fixed = quotient["nontrivial_physical_action_fixed_set_audit"]
    need(fixed == {
        "JxJy_fixed_sheet_point_family_count": 0,
        "Jx_fixed_sheet_point_family_count": 0,
        "Jy_fixed_sheet_point_family_count": 0,
        "decisive_p_fact": "ALL_16_SOURCE_SHEET_P_INTERVALS_EXCLUDE_ZERO",
        "fixed_set_rows_sha256":
            "018b7f16751a0c2897d79128322659512e6c0d7203a591d4436ed93aa5ff7a49",
        "physical_actions_are_not_quotient_identifications": True,
        "source_sheet_count": 16,
        "unit_normal_fact": "N_X_AND_N_Y_CANNOT_BOTH_BE_ZERO"},
         "physical action fixed sets")
    phase = quotient["primitive_global_phase_map_authority"]
    need(phase["primitive_source_sha256"] == PINS["primitive_atlas"][1]
         and phase["nonidentity_action_orbits_are_quotient_equivalences"] is False,
         "primitive action authority")
    need(quotient["explicit_global_phase_equation_certificate"]["cross_chart_pair_count"]
         == 1_361_424, "quotient exact denominator")
    need(sum(1 for _ in gzip_rows("quotient_cohort_ledger")) == 128,
         "quotient cohort ledger count")
    return {"double": double, "seam_evidence": seam_evidence,
            "physical_actions": phase["physical_actions"],
            "fixed_set_audit": fixed}


def normalized_rows(receipts: dict[str, Any], materialized: dict[str, Any],
                    evidence: dict[str, Any]) -> list[dict[str, Any]]:
    receipt_path = {key: PINS[key + "_receipt"][0] for key in
                    ("retained", "outgoing", "single", "included")}
    receipt_path["owner"] = PINS["owner_shadow_receipt"][0]
    receipt_hash = {key: PINS[key + "_receipt"][1] for key in
                    ("retained", "outgoing", "single", "included")}
    receipt_hash["owner"] = PINS["owner_shadow_receipt"][1]
    common = {
        "schema": "cm2.c27-independent.legacy16-terminal-authority-normalized.row.v1",
        "formal_credit": 0,
        "source_W_transition_authorized": False,
    }
    rows: list[dict[str, Any]] = []

    def add(terminal: str, branch: str, authority_class: str,
            candidate_count: int, terminal_receipt: Any,
            candidate_ledger: Any, key_fields: list[str],
            member_pair: dict[str, Any], witness: dict[str, Any],
            absence: dict[str, Any], blocking: bool) -> None:
        body = {**common, "ordinal": len(rows), "terminal": terminal,
                "branch": branch, "authority_class": authority_class,
                "candidate_count": candidate_count,
                "terminal_receipt": terminal_receipt,
                "candidate_ledger": candidate_ledger,
                "normalized_candidate_key_fields": key_fields,
                "member_pair_contract": member_pair,
                "physical_witness_contract": witness,
                "absence_disposition_contract": absence,
                "terminal_formal_authority_blocking_gap": blocking}
        rows.append(row(body))

    add("RETAINED_CONTINUATION", "SUPPORT_STRATUM", "RECEIPT_AND_ROW_AUTHORITY",
        276, {"path": receipt_path["retained"], "sha256": receipt_hash["retained"],
              "status": receipts["retained"]["status"]},
        {"path": PINS["representation_alias_ledger"][0],
         "sha256": PINS["representation_alias_ledger"][1], "row_count": 276,
         "schema": "cm2.round295a.source-g-retained-continuation-representation-alias-ledger.v1"},
        ["Round295A_retained_continuation_alias_row_id",
         "source_Round179_retained_child_row_id", "resolved_sibling_row_id",
         "artificial_split_face"],
        {"left": "source_Round179_retained_child_row_id",
         "right": "resolved_sibling_row_id", "same_origin": True},
        {"kind": "EXACT_SHARED_FULL_POSITIVE_T_FACE", "positive_volume_overlap": 0},
        {"kind": "NOT_ABSENCE__DISJOINT_INTERIORS_AND_UNIQUE_ADJACENT_SIBLING"}, False)

    add("OUTGOING_GRAPHS", "SUPPORT_STRATUM", "RECEIPT_AND_ROW_AUTHORITY",
        264, {"path": receipt_path["outgoing"], "sha256": receipt_hash["outgoing"],
              "status": receipts["outgoing"]["status"]},
        {"path": PINS["outgoing_ledger_a"][0],
         "sha256": PINS["outgoing_ledger_a"][1], "row_count": 264,
         "schema": "cm2.c27.outgoing-graphs-physical-totality-zero-credit.v1.candidate-row.v1",
         "dual_seed_byte_identical": True},
        ["graph_id", "geometry_root_sha256", "exact_support_ast_sha256",
         "candidate_digest"],
        {"materialized_disposition_members_per_root": 3,
         "roles": {"G2A_SHEET": 1, "G2B_SIDE": 2},
         "C15_component_bound": True},
        {"kind": "C10_GRAPH_AST_PLUS_C24_C25_C26_MATERIALIZED_PROOF_ROWS",
         "disposition_rows": materialized["outgoing_dispositions"]},
        {"kind": "NO_C24B_NEGATIVE_DISPOSITION", "unresolved": 0}, False)

    add("SINGLE_GRAPHS", "SUPPORT_STRATUM", "RECEIPT_AND_ROW_AUTHORITY",
        4_984, {"path": receipt_path["single"], "sha256": receipt_hash["single"],
                "status": receipts["single"]["status"]},
        {"path": PINS["single_ledger_a"][0], "sha256": PINS["single_ledger_a"][1],
         "row_count": 4_984,
         "schema": "cm2.c27.single-graphs-physical-totality-zero-credit.v1.candidate-row.v1",
         "dual_seed_byte_identical": True},
        ["graph_id", "graph_class", "geometry_root_sha256",
         "exact_support_ast_sha256", "candidate_digest"],
        {"materialized_disposition_rows": 14_552,
         "role_census": materialized["single_role_census"],
         "C15_component_bound": True},
        {"kind": "C10_GRAPH_AST_PLUS_C24A_C24B_C25_C26_MATERIALIZED_PROOF_ROWS"},
        {"kind": "G2B_EXACT_EMPTY_SIDE_IS_EXPLICIT_C24B_EMPTY_SUPPORT",
         "count": 152, "unresolved": 0}, False)

    add("DOUBLE_GRAPHS", "SUPPORT_STRATUM", "REJECTED_DIAGNOSTIC_ONLY",
        16, None,
        {"path": PINS["double_diagnostic_ledger"][0],
         "sha256": PINS["double_diagnostic_ledger"][1], "row_count": 696,
         "schema": "MIXED_DIAGNOSTIC_ROWS_NOT_16_ROOT_TERMINAL_LEDGER",
         "not_candidate_authority": True},
        ["MISSING_graph_id", "MISSING_candidate_digest",
         "MISSING_materialized_C15_C24_C25_C26_root_join"],
        {"status": "MISSING_16_ROOT_NORMALIZED_MEMBER_DISPOSITIONS"},
        {"status": "DIAGNOSTIC_ONLY__NOT_TERMINAL_TOTALITY_WITNESS"},
        {"status": evidence["double"]["status"],
         "unresolved_candidate_count": 1_361_872}, True)

    for terminal, role in (("SHEET_OWNER", "OWNER"), ("SHEET_SHADOW", "SHADOW")):
        add(terminal, "SUPPORT_STRATUM", "JOINT_RECEIPT_AND_FILTERED_ROW_AUTHORITY",
            17_940, {"path": receipt_path["owner"], "sha256": receipt_hash["owner"],
                     "status": receipts["owner"]["status"]},
            {"path": PINS["owner_shadow_ledger_a"][0],
             "sha256": PINS["owner_shadow_ledger_a"][1], "row_count": 35_880,
             "filter": {"role": role}, "filtered_row_count": 17_940,
             "schema": "cm2.c27.sheet-owner-shadow-physical-totality.v1.row.v1",
             "dual_seed_byte_identical": True},
            ["physical_sheet_id", "role", "assigned_member_id", "fresh_component_id"],
            {"left": "owner_member_id", "right": "shadow_member_id",
             "physical_sheet_key": "physical_sheet_id"},
            {"kind": "PRIMITIVE_HALF_OPEN_SHEET_INCIDENCE",
             "equality_sheet_included": role == "OWNER"},
            {"kind": "UNIQUE_ADJACENT_SHADOW_EXCLUDES_EQUALITY_SHEET"
                     if role == "SHADOW" else "NOT_ABSENCE__UNIQUE_OWNER_INCLUDES_EQUALITY_SHEET"},
            False)

    add("INCLUDED_STRATUM_ATTACHMENTS", "SUPPORT_STRATUM",
        "RECEIPT_COMMITMENT_ONLY_NO_MATERIALIZED_CANDIDATE_LEDGER", 10_660,
        {"path": receipt_path["included"], "sha256": receipt_hash["included"],
         "status": receipts["included"]["status"],
         "joint_retained_boundary_recomputed": True}, None,
        ["candidate_representation_id_COMMITTED_NOT_MATERIALIZED",
         "support_semantic_kind", "semantic_kernel", "selected_C15_owner"],
        {"status": "C15_OWNER_JOIN_CENSUS_ZERO_GAPS__ROW_LEDGER_NOT_EMITTED"},
        {"kind": "C25_EXACT_SUBCOVER_OR_C20D_STRICT_SUBCOVER",
         "candidate_ids_sha256": receipts["included"]["candidate_commitment"]
                                    ["candidate_representation_ids_sha256"]},
        {"kind": "276_ADJACENT_POSITIVE_T_ROWS_EXCLUDED_TO_RETAINED",
         "intersection_count": 0}, False)

    add("REVERSE_RECHART", "ATLAS_MAP", "PRIMITIVE_EVIDENCE_ONLY_NO_TERMINAL_RECEIPT",
        4, None, None,
        ["forward_chart_pair", "reverse_chart_pair", "forward_faces", "reverse_faces"],
        {"status": "NO_C15_MEMBER_PAIR__ATLAS_BIJECTION_RELATION"},
        {"kind": "INVERSE_OF_FOUR_EXACT_TRUE_PHASE_SEAMS"},
        {"kind": "NO_NEW_PHYSICAL_IDENTIFICATION_OR_COMPONENT_EDGE"}, True)

    for terminal in ("TRUE_CYCLIC_SEAM_E_TO_N", "TRUE_CYCLIC_SEAM_N_TO_W",
                     "TRUE_CYCLIC_SEAM_W_TO_S", "TRUE_CYCLIC_SEAM_S_TO_E"):
        suffix = terminal.removeprefix("TRUE_CYCLIC_SEAM_")
        seam = evidence["seam_evidence"][suffix]
        add(terminal, "ATLAS_MAP", "PRIMITIVE_EVIDENCE_ONLY_NO_TERMINAL_RECEIPT",
            1, None, {"path": PINS["coordinate_bridge"][0],
                      "sha256": PINS["coordinate_bridge"][1],
                      "embedded_seam": seam},
            ["left_face.chart", "left_face.z", "right_face.chart", "right_face.z"],
            {"status": "NO_C15_MEMBER_PAIR__ATLAS_FACE_PAIR"},
            {"kind": "EXACT_NORMAL_POSITION_QUARTER_TURN_VELOCITY_GLUE"},
            {"kind": "NOT_ABSENCE__EXACT_TRUE_SEAM"}, True)

    for terminal, action in (("Jx_NEGATIVE_CONTROL", "Jx"),
                             ("Jy_NEGATIVE_CONTROL", "Jy"),
                             ("JxJy_NEGATIVE_CONTROL", "JxJy")):
        add(terminal, "PHYSICAL_ACTION_NEGATIVE_CONTROL",
            "AGGREGATE_ABSENCE_EVIDENCE_ONLY_NO_PER_ACTION_RECEIPT", 1, None,
            {"path": PINS["quotient_result"][0],
             "sha256": PINS["quotient_result"][1],
             "source_sheet_denominator": 16},
            ["action_word", "physical_action_AST", "source_sheet_id"],
            {"status": "NO_MEMBER_PAIR__NONIDENTITY_ACTION_IS_NOT_QUOTIENT_GLUE"},
            {"kind": "PHYSICAL_ACTION_AST", "action": action,
             "ast": evidence["physical_actions"][action]},
            {"kind": "ZERO_FIXED_SOURCE_SHEET_POINT_FAMILIES",
             "fixed_family_count": 0,
             "decisive_facts": ["ALL_16_SOURCE_SHEET_P_INTERVALS_EXCLUDE_ZERO",
                                 "N_X_AND_N_Y_CANNOT_BOTH_BE_ZERO"]}, True)

    add("REPRESENTATION_ALIASES", "REPRESENTATION_MAP",
        "ROW_EVIDENCE_REUSED_BY_RETAINED__NO_INDEPENDENT_TERMINAL_RECEIPT", 276,
        None, {"path": PINS["representation_alias_ledger"][0],
               "sha256": PINS["representation_alias_ledger"][1],
               "row_count": 276,
               "same_rows_already_bound_to_retained_continuation": True},
        ["Round295A_retained_continuation_alias_row_id",
         "source_Round179_retained_child_row_id", "resolved_sibling_row_id"],
        {"left": "source_Round179_retained_child_row_id",
         "right": "resolved_sibling_row_id", "same_origin": True},
        {"kind": "EXACT_SAME_ORIGIN_ARTIFICIAL_T_SPLIT_CONTINUATION_ALIAS"},
        {"kind": "NO_IDENTITY_COLLAPSE_OR_SYMMETRY_GLUE_CREDIT",
         "missing": "INDEPENDENT_BRANCH_OWNERSHIP_AND_UNIQUE_ASSIGNMENT_RECEIPT"}, True)

    need(tuple(item["terminal"] for item in rows) == TERMINALS,
         "normalized terminal order")
    return rows


def gaps(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    reasons = {
        "DOUBLE_GRAPHS": {
            "missing": ["PASS_TERMINAL_RECEIPT", "16_ROOT_NORMALIZED_LEDGER",
                        "MATERIALIZED_C15_C24_C25_C26_PROOF_ROW_JOIN"],
            "present_but_rejected": "696_ROW_DIAGNOSTIC_LEDGER__1361872_UNRESOLVED"},
        "REVERSE_RECHART": {
            "missing": ["COMPLETED_RUN_RECEIPT", "NORMALIZED_4_ROW_LEDGER",
                        "INDEPENDENT_VERIFIER", "COHERENT_ATTACKS", "TERMINAL_REPLAY"],
            "present_evidence": "SOURCE_PROBE_AND_R171_FOUR_TRUE_SEAMS"},
        "Jx_NEGATIVE_CONTROL": {
            "missing": ["PER_ACTION_16_SOURCE_SHEET_ROW_LEDGER", "TERMINAL_RECEIPT",
                        "INDEPENDENT_ACTION_SPECIFIC_VERIFIER"],
            "present_evidence": "AGGREGATE_FIXED_SET_CENSUS_ZERO"},
        "Jy_NEGATIVE_CONTROL": {
            "missing": ["PER_ACTION_16_SOURCE_SHEET_ROW_LEDGER", "TERMINAL_RECEIPT",
                        "INDEPENDENT_ACTION_SPECIFIC_VERIFIER"],
            "present_evidence": "AGGREGATE_FIXED_SET_CENSUS_ZERO"},
        "JxJy_NEGATIVE_CONTROL": {
            "missing": ["PER_ACTION_16_SOURCE_SHEET_ROW_LEDGER", "TERMINAL_RECEIPT",
                        "INDEPENDENT_ACTION_SPECIFIC_VERIFIER"],
            "present_evidence": "AGGREGATE_FIXED_SET_CENSUS_ZERO"},
        "REPRESENTATION_ALIASES": {
            "missing": ["INDEPENDENT_TERMINAL_RECEIPT",
                        "DISJOINT_BRANCH_OWNERSHIP_FROM_RETAINED_CONTINUATION",
                        "UNIQUE_TERMINAL_ASSIGNMENT_PROOF"],
            "present_evidence": "276_ROWS_REUSED_BY_RETAINED_CONTINUATION"},
    }
    for terminal in ("TRUE_CYCLIC_SEAM_E_TO_N", "TRUE_CYCLIC_SEAM_N_TO_W",
                     "TRUE_CYCLIC_SEAM_W_TO_S", "TRUE_CYCLIC_SEAM_S_TO_E"):
        reasons[terminal] = {
            "missing": ["TERMINAL_SCOPED_RECEIPT", "NORMALIZED_TERMINAL_ROW",
                        "TERMINAL_SPECIFIC_ATTACK_AND_REPLAY"],
            "present_evidence": "R171_EXACT_PHASE_SEAM_AND_INDEPENDENT_VERIFICATION"}
    output = []
    by_name = {item["terminal"]: item for item in rows}
    for ordinal, terminal in enumerate(TERMINALS):
        if terminal not in reasons:
            continue
        body = {
            "schema": "cm2.c27-independent.legacy16-terminal-authority-gap.row.v1",
            "gap_ordinal": len(output), "terminal": terminal,
            "authority_class": by_name[terminal]["authority_class"],
            **reasons[terminal], "gate_blocking": True, "formal_credit": 0,
        }
        output.append(row(body))
    need(len(output) == 10, "ten exact authority gaps")
    return output


def write_jsonl_gz(path: Path, values: list[dict[str, Any]]) -> None:
    with path.open("wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as packed:
            for value in values:
                packed.write(canonical(value) + b"\n")


def run(output: Path) -> dict[str, Any]:
    need(not output.exists(), "fresh output directory")
    receipts = audit_receipt_authorities()
    materialized = audit_materialized_rows()
    evidence = audit_evidence_only()
    rows = normalized_rows(receipts, materialized, evidence)
    gap_rows = gaps(rows)
    output.mkdir(parents=True, exist_ok=False)
    normalized_path = output / "legacy16_terminal_authority_normalized_rows.jsonl.gz"
    gap_path = output / "legacy16_terminal_authority_gap_ledger.jsonl.gz"
    write_jsonl_gz(normalized_path, rows)
    write_jsonl_gz(gap_path, gap_rows)

    body = {
        "schema": "cm2.c27-independent.legacy16-terminal-authority-normalization.result.v1",
        "status": "REJECT_ACTUAL_V5_LEGACY16_AUTHORITY_INCOMPLETE__6_RECEIPT_BACKED__10_HARD_GAPS__ZERO_CREDIT",
        "decision": "FAIL_CLOSED_REJECT",
        "terminal_census": {
            "requested": 16,
            "receipt_backed_terminal_authorities": 6,
            "receipt_and_materialized_row_authorities": 5,
            "receipt_commitment_only_no_candidate_ledger": 1,
            "hard_terminal_authority_gaps": 10,
        },
        "receipt_backed_terminals": [
            "RETAINED_CONTINUATION", "OUTGOING_GRAPHS", "SINGLE_GRAPHS",
            "SHEET_OWNER", "SHEET_SHADOW", "INCLUDED_STRATUM_ATTACHMENTS"],
        "hard_gap_terminals": [value["terminal"] for value in gap_rows],
        "included_retained_joint_boundary": {
            "recomputed": True, "included_candidates": 10_660,
            "retained_candidates": 276, "disjoint_union": 10_936,
            "intersection": 0},
        "normalized_ledger": {
            "filename": normalized_path.name, "row_count": len(rows),
            "file_sha256": file_hash(normalized_path),
            "row_sequence_sha256": digest([value["row_sha256"] for value in rows])},
        "gap_ledger": {
            "filename": gap_path.name, "row_count": len(gap_rows),
            "file_sha256": file_hash(gap_path),
            "row_sequence_sha256": digest([value["row_sha256"] for value in gap_rows])},
        "input_pins": {label: {"path": path, "sha256": sha}
                       for label, (path, sha) in sorted(PINS.items())},
        "materialized_census": materialized,
        "actual_v5_contract": {
            "must_bind_all_six_receipt_backed_authorities": True,
            "must_close_all_ten_hard_gaps_with_terminal_level_authority": True,
            "may_not_treat_old_16_of_20_aggregate_census_as_authority": True,
            "may_not_set_primitive_twenty_family_totality_proved_now": True,
            "strict14772_or_scoped14724_used_as_candidate_universe": False,
        },
        "forbidden_input_governance": {
            "old_C27_FAMILIES_imported_or_read": False,
            "old_transition_ledger_imported_or_read": False,
            "C28_imported_or_read": False,
            "C29_imported_or_read": False,
            "historical_edge_ledger_used_as_candidate_universe": False,
            "strict14772_used_only_as_cross_check": False,
            "scoped14724_used_only_as_cross_check": False,
        },
        "formal_credit": 0,
        "manifest_authorized": False,
        "source_W_transition_authorized": False,
        "strict_nonpromotion": {"C27_transition_totality": 0,
                                "C28_pair_routing": 0,
                                "C29_physical_maximality": 0,
                                "CM2": "NO-GO_FOR_CLAIM"},
    }
    result = {**body, "result_sha256": digest(body)}
    (output / "legacy16_terminal_authority_result.json").write_bytes(
        canonical(result) + b"\n")
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--seed", type=int, required=True)
    args = parser.parse_args()
    del args.seed  # required true runtime seed, intentionally no semantic role
    try:
        result = run(Path(args.output_dir))
    except (Reject, KeyError, TypeError, ValueError, OSError,
            json.JSONDecodeError) as error:
        print("REJECT:" + str(error))
        return 2
    print(canonical({"status": result["status"],
                     "decision": result["decision"],
                     "result_sha256": result["result_sha256"]}).decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
