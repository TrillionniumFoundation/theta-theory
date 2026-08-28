#!/usr/bin/env python3
"""Round306B2C0 feature/transition/pair-routing zero-credit contract.

This is deliberately a small, non-producing contract.  It freezes the typed
dependency DAG and the accounting rules that a future Round306B2 atlas must
satisfy.  It does not reconstruct a feature, route a pair, classify a
candidate, or open any sealed large source.  Candidate mode is blocked at the
function boundary, before path inspection, input open, temporary creation, or
output write.

Round306B1R0 and Round306B1G0 are consumable source-inventory freezes with zero
theorem credit.  Round306B1A remains a draft census: its loader is false and no
formal package exists.  Consequently this contract cannot issue feature,
support, transition, maximality, fibre, or global credit.
"""

from __future__ import annotations

import argparse
import builtins
from contextlib import ExitStack
from copy import deepcopy
import hashlib
import json
import os
from pathlib import Path
import re
import tempfile
from typing import Any, Callable, NoReturn
from unittest import mock


class ContractBlocked(RuntimeError):
    """Fail-closed contract or candidate-mode violation."""


def need(condition: bool, label: str) -> None:
    if not condition:
        raise ContractBlocked(label)


SCHEMA = "cm2.round306b2c0.source-g-feature-transition-pair-routing-contract.v1"
STATUS = (
    "BLOCKED_FAIL_CLOSED_ZERO_CREDIT__B1A_FORMAL_FEATURE_COVER_ABSENT__"
    "NO_PAIR_ROUTING_EMITTED"
)
CANDIDATE_BLOCK_REASON = (
    "Round306B2C0 candidate mode blocked before path lstat/open/temp/write: "
    "the sealed Round306B1A formal feature-cover package is absent"
)
HEX64 = re.compile(r"^[0-9a-f]{64}$")

PAIR_DENOMINATORS = (
    ("O/O", "OCCURRENCE__OCCURRENCE", 92_536_544_199),
    ("O/P3D", "OCCURRENCE__VIRTUAL_POSITIVE_3D", 40_785_517_502),
    ("O/sheet", "OCCURRENCE__VIRTUAL_SHEET", 16_648_669_731),
    ("P3D/P3D", "VIRTUAL_POSITIVE_3D__VIRTUAL_POSITIVE_3D", 4_474_700_754),
    ("P3D/sheet", "VIRTUAL_POSITIVE_3D__VIRTUAL_SHEET", 3_649_299_612),
    ("sheet/sheet", "VIRTUAL_SHEET__VIRTUAL_SHEET", 743_352_556),
)
PAIR_TOTAL = 158_838_084_354

KNOWN_EDGE_SOURCES = (
    ("R297", "ORDINARY_FACE_OCCURRENCE_EDGE", 330_724),
    ("R296", "TRUE_SEAM_OCCURRENCE_EDGE", 48_444),
    ("R303B", "UNIFIED_ATTACHMENT_EDGE", 44_104),
    ("R299C", "R292_SIGNED_SUPPORT_FACE_EDGE", 25_452),
    ("R300E", "R248_HALF_OPEN_OWNER_LOWER_COMPONENT_EDGE", 12_992),
    ("R300B", "REGISTRY_BOUNDARY_AND_COMPLETE_R275_FACE", 10_416),
    ("R300C", "VIRTUAL_STRATUM_POSITIVE_VOLUME_EDGE", 6_314),
    ("R300F", "R245_HALF_OPEN_OWNER_SHEET_ATTACHMENT", 264),
    ("R305B", "TWO_SIDED_PHYSICAL_INCLUSION_EDGE", 8),
)
KNOWN_EDGE_TOTAL = 478_718

TRANSITION_FAMILIES = (
    "SAME_CHART_RELATIVE_CELLS",
    "RETAINED_CONTINUATION",
    "OUTGOING_GRAPHS",
    "SINGLE_GRAPHS",
    "DOUBLE_GRAPHS",
    "SHEET_OWNER",
    "SHEET_SHADOW",
    "REVERSE_RECHART",
    "TRUE_CYCLIC_SEAM_E_TO_N",
    "TRUE_CYCLIC_SEAM_N_TO_W",
    "TRUE_CYCLIC_SEAM_W_TO_S",
    "TRUE_CYCLIC_SEAM_S_TO_E",
    "Jx_NEGATIVE_CONTROL",
    "Jy_NEGATIVE_CONTROL",
    "JxJy_NEGATIVE_CONTROL",
    "SIGNED_BOUNDARY_FACES",
    "COMPLETE_BOUNDARY_FACES",
    "POSITIVE_VOLUME_CARRIERS",
    "REPRESENTATION_ALIASES",
    "INCLUDED_STRATUM_ATTACHMENTS",
)

FUTURE_LEDGERS = (
    "feature_definition",
    "member_cover",
    "transition_witness",
    "unique_candidate_pair",
    "known_edge_recovery",
    "pair_route_shard",
    "candidate_classification",
    "gap",
)

CLASSIFICATIONS = (
    "EXACT_NONEDGE",
    "KNOWN_LEGAL",
    "NEW_LEGAL_CROSS_COMPONENT",
    "UNRESOLVED",
)

ATTACK_SCOPE = (
    "four_split_predicate_cells_mint_member_identities",
    "graph_definition_gap_promoted_to_edge",
    "graph_sheet_identification_promoted_to_adjacency",
    "Round236_side_reference_confused_with_B0_member",
    "R1_R2_dependency_flattened",
    "G1_G2_dependency_flattened",
    "B1A_dependent_incidences_promoted_to_independent_roots",
    "representation_alias_mints_member_identity",
    "outer_box_or_inner_witness_claimed_as_full_support",
    "official_key_used_as_transition_filter",
    "return_signature_used_as_transition_filter",
    "known_row_ID_join_before_geometry_recovery",
    "endpoint_reversal_mints_second_pair",
    "cross_shard_duplicate_pair_accepted",
    "within_component_pair_leaks_into_cross_denominator",
    "wrong_pair_class_accepted",
    "wrong_cross_pair_denominator",
    "transition_family_omitted",
    "Round264_empty_bulk_revived",
    "nonzero_unresolved_gap_forced_to_PASS",
    "new_cross_component_edge_silently_added_to_old_DSU",
    "B1A_draft_treated_as_formal",
    "incomplete_known_edge_recovery_accepted",
    "representation_piece_count_treated_as_member_count",
    "B1G_76848_references_conflated_with_B1A_76304_carriers",
    "duplicate_JSON_key_allowed",
    "noncanonical_gzip_allowed",
    "symlink_or_hardlink_path_allowed",
    "output_clobber_allowed",
    "manifest_admitted_before_verification_last",
    "candidate_marked_formal",
    "nonzero_formal_credit",
)


def canonical(value: Any) -> str:
    return json.dumps(
        value, ensure_ascii=True, allow_nan=False, sort_keys=True, separators=(",", ":")
    )


def _dependency_admission_rows() -> list[dict[str, Any]]:
    return [
        {
            "round": "Round306B0",
            "admission": "SEALED_FORMAL_CONSUMABLE",
            "manifest_filename":
                "cm2_round306b0_source_g_r306a_universe_support_source_freeze_manifest.sha256",
            "manifest_file_sha256":
                "9846b36d28bb1507b273de3e613a5ecd5ac6515258042bf8b91b89e0c156b269",
            "result_filename":
                "cm2_round306b0_source_g_r306a_universe_support_source_freeze_result.json",
            "result_file_sha256":
                "badc000c6fadd8807b26a7c3511edc51796c962f150b438956e4c549fd0d5735",
            "result_sha256":
                "9ffe9144bc67f9bb7bb7e9c071b29a000f7d8e89396a3250b8207bfcc950d3d2",
            "verification_filename":
                "cm2_round306b0_source_g_r306a_universe_support_source_freeze_verification.json",
            "verification_file_sha256":
                "f8acc3150d4663d92976a44ab1c3b35c7264f4c4d14808f9133f1184d3f4b590",
            "verification_sha256":
                "774813f546184aa30c342840ddfa6b0566ebe4d382acd16d74ead8f03dadaddc",
            "consumable_boundary": [
                "564492_member_universe",
                "92688_component_quotient",
                "member_source_binding",
                "six_cross_component_pair_denominators",
            ],
            "theorem_or_maximality_credit": 0,
        },
        {
            "round": "Round306B1R0",
            "admission": "SEALED_FORMAL_CONSUMABLE_ZERO_THEOREM_CREDIT",
            "manifest_filename":
                "cm2_round306b1r0_source_g_r288_predicate_source_inventory_and_union_freeze_manifest.sha256",
            "manifest_file_sha256":
                "f23f4639629e920596e1ecadbb1cd7708f93308dc5780a0f82c196edc0f46aec",
            "result_filename":
                "cm2_round306b1r0_source_g_r288_predicate_source_inventory_and_union_freeze_result.json",
            "result_file_sha256":
                "ca66501d42894dce364ff905045ae69f67cf52c9142ba8f7b45973f857966f04",
            "result_sha256":
                "ad2454ded68ffdcd4b37d39a43b60220ca4fbad780197e0443bcf4ce1904a46c",
            "verification_filename":
                "cm2_round306b1r0_source_g_r288_predicate_source_inventory_and_union_freeze_verification.json",
            "verification_file_sha256":
                "2242732077165e085f6f2e50f2d061a532a3b43d9e9bc0efc17afac3d45df040",
            "verification_sha256":
                "3cb6c976f411a4ad05369434dab8d60ff98fea7204fddd8dd628d6e67c644ea8",
            "consumable_boundary": [
                "predicate_source_cell_inventory",
                "outer_envelope_union_inventory",
                "explicit_gap",
            ],
            "theorem_or_maximality_credit": 0,
        },
        {
            "round": "Round306B1G0",
            "admission": "SEALED_FORMAL_CONSUMABLE_ZERO_THEOREM_CREDIT",
            "manifest_filename":
                "cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_manifest.sha256",
            "manifest_file_sha256":
                "6f79385d0eed9c13bcc1501c8a189e947f1194d28e198290e6a4b2b2a376a9b8",
            "result_filename":
                "cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_result.json",
            "result_file_sha256":
                "3f494ebc9f046bfe9f42aef16edeadaece099d7ba7547b11f07484e3f6d81b9e",
            "result_sha256":
                "7bb3def1952176cbaf98723a6a2c5126e3c9193efac36a0d9a2c07533e0ec9bd",
            "verification_filename":
                "cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_verification.json",
            "verification_file_sha256":
                "65b7a01fd82535f357dbb44b8c68a68c86afcbb75b1c1c9b9159b71f9815139a",
            "verification_sha256":
                "542de6d90a6dcb6cd8775a1caf6fe3c3e62bbae49a10e864a7820ba3d083f700",
            "consumable_boundary": [
                "graph_source_inventory",
                "graph_sheet_identification_inventory",
                "graph_side_incidence_reference_inventory",
                "correction_and_B0_backbinding_inventory",
                "explicit_gap",
            ],
            "theorem_or_maximality_credit": 0,
        },
        {
            "round": "Round306B1A",
            "admission": "CONTRACT_ONLY",
            "formal_package_state": "FORMAL_ABSENT",
            "draft_filename":
                "cm2_round306b1a_source_g_r306b0_carrier_witness_and_support_gap_atlas.py",
            "draft_file_sha256":
                "6e198755d946bc5828a4366dc818469df7af5e44873c470d9d1050003960473a",
            "complete_atlas_loader_installed": False,
            "formal_manifest": None,
            "formal_result": None,
            "formal_verification": None,
            "consumable_boundary": [],
            "theorem_or_maximality_credit": 0,
        },
    ]


def _obligation_rows() -> list[dict[str, Any]]:
    base = [
        ("G1", "Round306B1G0", "INDEPENDENT_DEFINITION_ROOT", 38_624, []),
        ("G2a", "Round306B1G0", "DEPENDENT_GRAPH_TO_SHEET_IDENTIFICATION", 38_624, ["G1"]),
        ("G2b", "Round306B1G0", "DEPENDENT_GRAPH_TO_SIDE_INCIDENCE_REFERENCE", 76_848, ["G1"]),
        ("R1", "Round306B1R0", "INDEPENDENT_PREDICATE_CELL_DEFINITION", 295_340, []),
        ("R2", "Round306B1R0", "DEPENDENT_MEMBER_FULL_SUPPORT_UNION", 295_336, ["R1"]),
        ("A1", "Round306B1A", "INDEPENDENT_ANALYTIC_DEFINITION_ROOT", 17_940, []),
        ("A2", "Round306B1A", "DEPENDENT_ANALYTIC_INCIDENCE", 62_152, ["A1"]),
    ]
    return [
        {
            "node_id": node,
            "source_package": package,
            "obligation_type": kind,
            "row_count": count,
            "depends_on": dependencies,
            "issues_member_identity": False,
            "issues_unordered_member_pair": False,
            "formal_theorem_credit": 0,
        }
        for node, package, kind, count, dependencies in base
    ]


def _transition_rows() -> list[dict[str, Any]]:
    negative = {"Jx_NEGATIVE_CONTROL", "Jy_NEGATIVE_CONTROL", "JxJy_NEGATIVE_CONTROL"}
    return [
        {
            "family_id": family,
            "mandatory_for_future_atlas": True,
            "role": "NEGATIVE_CONTROL_NON_GLUE" if family in negative else "POSITIVE_ROUTING_FAMILY",
            "official_key_is_payload_only": True,
            "return_signature_is_payload_only": True,
            "current_witness_row_count": 0,
            "current_state": "NOT_EMITTED_ZERO_CREDIT_CONTRACT",
        }
        for family in TRANSITION_FAMILIES
    ]


def _contract_document() -> dict[str, Any]:
    return {
        "schema": SCHEMA,
        "status": STATUS,
        "candidate_is_formal": False,
        "candidate_mode": {
            "enabled": False,
            "block_before_path_lstat": True,
            "block_before_input_open": True,
            "block_before_temp_creation": True,
            "block_before_output_write": True,
            "candidate_files": [],
        },
        "dependency_admission_rows": _dependency_admission_rows(),
        "obligation_dependency_rows": _obligation_rows(),
        "obligation_census": {
            "B1G_G1_definition_rows": 38_624,
            "B1G_G2a_identification_rows": 38_624,
            "B1G_G2b_incidence_reference_rows": 76_848,
            "B1G_physical_identification_and_incidence_layer": 115_472,
            "B1G_all_G1_G2_obligation_rows": 154_096,
            "B1R_R1_predicate_cell_rows": 295_340,
            "B1R_R2_member_union_rows": 295_336,
            "B1R_all_dependency_DAG_obligation_rows": 590_676,
            "B1A_independent_root_contract_census": 17_940,
            "B1A_dependent_incidence_contract_census": 62_152,
            "B1A_roots_and_incidences_are_not_flattened": True,
        },
        "semantic_separation": {
            "four_R1_split_cells_are_not_member_identities": True,
            "graph_definition_gap_is_not_edge": True,
            "graph_sheet_identification_is_not_adjacency": True,
            "graph_side_incidence_reference_is_not_member_pair": True,
            "Round236_side_reference_is_not_B0_member": True,
            "dependent_incidence_is_not_independent_root": True,
            "representation_alias_mints_no_member_identity": True,
            "outer_box_is_not_full_normalized_support": True,
            "strict_inner_witness_is_not_full_normalized_support": True,
            "B1G_graph_side_reference_count": 76_848,
            "B1A_graph_side_carrier_contract_count": 76_304,
            "those_two_counts_are_not_interchangeable": True,
        },
        "representation_contract_census": {
            "representation_primitive_count": 611_904,
            "primary_member_representation_count": 564_492,
            "extra_representation_count": 47_412,
            "extra_refined_primary_cell_count": 848,
            "alias_representation_count": 46_564,
            "census_is_not_feature_cover_evidence": True,
            "representation_piece_is_not_member_identity": True,
            "current_feature_cover_rows_emitted": 0,
        },
        "transition_family_contract_rows": _transition_rows(),
        "transition_routing_boundary": {
            "official_key_is_payload_only_never_filter": True,
            "return_signature_is_payload_only_never_filter": True,
            "all_twenty_families_required": True,
            "four_true_cyclic_seams": ["E<->N", "N<->W", "W<->S", "S<->E"],
            "Jx_Jy_JxJy_are_negative_controls_not_true_seams": True,
            "Round264_empty_bulk_revival_allowed": False,
        },
        "pair_denominator_source_pin": {
            "filename":
                "cm2_round306b0_source_g_r306a_universe_support_source_freeze_pair_denominator.json.gz",
            "file_sha256":
                "f8e22c93a0b070ae3ff2da557c1011ba74a214fbf4b841cdfeb219a2556f6261",
            "ledger_sha256":
                "7ca51af3afd4524f62d202649731e461472678e913cc975e0b8127fc4e19e5e3",
            "row_ids_sha256":
                "a1a4405b9f9f8090cbc592553effb169e046adb5ee06b17d93f8c862c53ca85c",
            "row_hashes_sha256":
                "d37b7b2b239f221ce70df0f565483dcb16ba0eaf6e4b45eeefaf5c6f89e49cb1",
            "rows_sha256":
                "63ebcc7713a6fdf5b4d6d96148802e88a2ec39f6a847d5eadfa4f7f906787cde",
        },
        "pair_class_denominator_rows": [
            {
                "pair_class_short": short,
                "B0_pair_class": formal,
                "cross_component_pair_count": count,
                "within_component_pairs_admitted": False,
                "formal_maximality_credit": 0,
            }
            for short, formal, count in PAIR_DENOMINATORS
        ],
        "cross_component_pair_denominator_total": PAIR_TOTAL,
        "shard_contract": {
            "member_home_block": "first_4_hex(SHA256(ASCII canonical_B0_member_id))",
            "home_block_count": 65_536,
            "canonical_unordered_pair": "B0_member_id_lexicographic_min_then_max",
            "pair_home": "(pair_class,home_block(left),home_block(right)) after canonicalization",
            "endpoint_reversal_is_same_canonical_pair": True,
            "one_and_only_one_home_shard_per_pair": True,
            "global_pair_uniqueness_required": True,
            "within_component_pairs_excluded": True,
            "per_class_per_shard_equation": (
                "cross_component_pair_count=exact_block_disjoint_pair_count+"
                "unique_emitted_candidate_pair_count+unresolved_gap_pair_count"
            ),
            "all_future_shard_counts_currently_unmaterialized": True,
            "current_pair_route_shard_rows_emitted": 0,
        },
        "known_edge_recovery_contract": {
            "recovery_rows": [
                {"source_round": round_id, "family": family, "edge_application_row_count": count}
                for round_id, family, count in KNOWN_EDGE_SOURCES
            ],
            "edge_application_row_count": KNOWN_EDGE_TOTAL,
            "geometry_first_before_source_row_id_join": True,
            "edge_rows_are_not_assumed_unique_member_pairs": True,
            "required_missing_row_count": 0,
            "required_orphan_row_count": 0,
            "required_duplicate_recovery_row_count": 0,
            "current_recovery_rows_emitted": 0,
        },
        "future_ledger_names": list(FUTURE_LEDGERS),
        "candidate_classification_contract": {
            "exact_allowed_classifications": list(CLASSIFICATIONS),
            "classification_is_on_unique_canonical_unordered_B0_member_pair": True,
            "unresolved_nonzero_blocks_PASS": True,
            "new_legal_cross_component_status": "RESTART_REQUIRED_ZERO_MAXIMALITY_CREDIT",
            "new_edge_may_be_silently_added_to_existing_DSU": False,
            "restart_requires_new_physical_theorem": True,
            "restart_requires_fresh_DSU": True,
            "restart_requires_B0_refreeze": True,
            "restart_requires_full_B1_B2_replay": True,
            "current_classification_rows_emitted": 0,
        },
        "future_PASS_gates": {
            "B1A_formal_package_sealed": False,
            "source_free_definition_gaps_must_equal": 0,
            "member_support_gaps_must_equal": 0,
            "transition_gaps_must_equal": 0,
            "representation_rows_must_equal": 611_904,
            "representation_missing_or_orphan_or_duplicate_must_equal": 0,
            "B0_members_covered_must_equal": 564_492,
            "all_transition_families_complete": False,
            "known_edge_rows_geometry_first_recovered_must_equal": 478_718,
            "known_edge_missing_or_orphan_or_duplicate_must_equal": 0,
            "all_six_pair_classes_and_every_shard_close_exactly": False,
            "all_pair_classes_total_must_equal": PAIR_TOTAL,
            "unresolved_pair_count_must_equal": 0,
            "new_legal_cross_component_edge_count_must_equal": 0,
            "PASS_currently_permitted": False,
        },
        "future_wire_path_publication_contract": {
            "strict_JSON_duplicate_keys_rejected": True,
            "strict_JSON_nonfinite_numbers_rejected": True,
            "strict_JSON_trailing_bytes_rejected": True,
            "canonical_gzip_exact_bytes_required": True,
            "gzip_multistream_rejected": True,
            "symlink_rejected": True,
            "hardlink_rejected": True,
            "path_replacement_rejected": True,
            "output_no_clobber": True,
            "independent_verification_required": True,
            "formal_manifest_is_verification_last": True,
        },
        "attack_scope": list(ATTACK_SCOPE),
        "formal_credit": {
            "feature_definition": 0,
            "member_support": 0,
            "transition_witness": 0,
            "pair_routing": 0,
            "pair_classification": 0,
            "new_component_edge": 0,
            "component_union": 0,
            "maximality": 0,
            "fibre": 0,
            "global_disposition": 0,
            "D02": "BLOCKED",
            "D03": "NOT_REACHED",
            "D04": "NOT_MINTED",
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "emission_accounting": {
            "large_sources_opened": 0,
            "reconstruction_rows_emitted": 0,
            "pair_routes_emitted": 0,
            "candidate_files_written": 0,
            "formal_files_written": 0,
        },
    }


def validate_contract(document: dict[str, Any]) -> None:
    """Validate the closed, typed B2C0 contract without reading a source."""

    need(document.get("schema") == SCHEMA, "schema")
    need(document.get("status") == STATUS, "blocked status")
    need(document.get("candidate_is_formal") is False, "candidate nonformal")

    admissions = document["dependency_admission_rows"]
    need([row["round"] for row in admissions] == ["Round306B0", "Round306B1R0", "Round306B1G0", "Round306B1A"], "dependency order")
    for row in admissions[:3]:
        for field in (
            "manifest_file_sha256", "result_file_sha256", "result_sha256",
            "verification_file_sha256", "verification_sha256",
        ):
            need(HEX64.fullmatch(row[field]) is not None, "dependency hash:" + row["round"] + ":" + field)
    need(admissions[3]["draft_file_sha256"] == "6e198755d946bc5828a4366dc818469df7af5e44873c470d9d1050003960473a", "B1A draft pin")
    need(admissions[3]["admission"] == "CONTRACT_ONLY" and admissions[3]["formal_package_state"] == "FORMAL_ABSENT", "B1A formal absence")
    need(admissions[3]["complete_atlas_loader_installed"] is False, "B1A loader false")

    dag = {row["node_id"]: row for row in document["obligation_dependency_rows"]}
    need(set(dag) == {"G1", "G2a", "G2b", "R1", "R2", "A1", "A2"}, "typed DAG nodes")
    need(dag["G2a"]["depends_on"] == ["G1"] and dag["G2b"]["depends_on"] == ["G1"], "G dependency edges")
    need(dag["R2"]["depends_on"] == ["R1"], "R dependency edge")
    need(dag["A2"]["depends_on"] == ["A1"], "A dependency edge")
    need(dag["A1"]["row_count"] == 17_940 and dag["A2"]["row_count"] == 62_152, "A root/incidence census")
    need(all(not row["issues_member_identity"] and not row["issues_unordered_member_pair"] for row in dag.values()), "obligations do not mint identities or pairs")

    census = document["obligation_census"]
    need(census["B1G_G2a_identification_rows"] + census["B1G_G2b_incidence_reference_rows"] == 115_472, "B1G physical layer")
    need(census["B1G_G1_definition_rows"] + 115_472 == 154_096, "B1G all obligations")
    need(census["B1R_R1_predicate_cell_rows"] + census["B1R_R2_member_union_rows"] == 590_676, "B1R all obligations")

    reps = document["representation_contract_census"]
    need(reps["primary_member_representation_count"] + reps["extra_representation_count"] == reps["representation_primitive_count"] == 611_904, "representation census")
    need(reps["extra_refined_primary_cell_count"] + reps["alias_representation_count"] == 47_412, "extra representation census")

    transitions = document["transition_family_contract_rows"]
    need(tuple(row["family_id"] for row in transitions) == TRANSITION_FAMILIES, "complete transition family order")
    need(len(transitions) == 20 and all(row["current_witness_row_count"] == 0 for row in transitions), "twenty zero-emission transition families")

    denominator_rows = document["pair_class_denominator_rows"]
    need(tuple((row["pair_class_short"], row["B0_pair_class"], row["cross_component_pair_count"]) for row in denominator_rows) == PAIR_DENOMINATORS, "six exact B0 denominators")
    need(sum(row["cross_component_pair_count"] for row in denominator_rows) == document["cross_component_pair_denominator_total"] == PAIR_TOTAL, "pair denominator total")
    need(all(row["within_component_pairs_admitted"] is False for row in denominator_rows), "within-component exclusion")

    recovery = document["known_edge_recovery_contract"]
    need(tuple((row["source_round"], row["family"], row["edge_application_row_count"]) for row in recovery["recovery_rows"]) == KNOWN_EDGE_SOURCES, "known edge source partition")
    need(sum(row["edge_application_row_count"] for row in recovery["recovery_rows"]) == recovery["edge_application_row_count"] == KNOWN_EDGE_TOTAL, "known edge total")
    need(recovery["geometry_first_before_source_row_id_join"] is True, "geometry-first recovery")

    need(tuple(document["future_ledger_names"]) == FUTURE_LEDGERS, "future ledger names")
    classification = document["candidate_classification_contract"]
    need(tuple(classification["exact_allowed_classifications"]) == CLASSIFICATIONS, "classification partition")
    need(classification["new_legal_cross_component_status"] == "RESTART_REQUIRED_ZERO_MAXIMALITY_CREDIT", "new edge restart status")
    need(classification["new_edge_may_be_silently_added_to_existing_DSU"] is False, "no silent new edge")

    gates = document["future_PASS_gates"]
    need(gates["PASS_currently_permitted"] is False and gates["B1A_formal_package_sealed"] is False, "PASS blocked")
    need(gates["unresolved_pair_count_must_equal"] == 0 and gates["new_legal_cross_component_edge_count_must_equal"] == 0, "zero gap/new-edge gate")
    need(gates["all_pair_classes_total_must_equal"] == PAIR_TOTAL, "PASS denominator")

    credit = document["formal_credit"]
    need(all(value == 0 for key, value in credit.items() if key not in {"D02", "D03", "D04", "CM2"}), "all numeric credit zero")
    need(credit["D02"] == "BLOCKED" and credit["CM2"] == "NO-GO_FOR_CLAIM", "D02 CM2 boundary")
    need(document["emission_accounting"] == {"large_sources_opened": 0, "reconstruction_rows_emitted": 0, "pair_routes_emitted": 0, "candidate_files_written": 0, "formal_files_written": 0}, "zero emission accounting")

    # These anchors intentionally repeat literals rather than consulting the
    # producer globals or factory.  They stop a coherent mutation of a global
    # and _contract_document() from teaching this validator the same lie.
    need(
        document["candidate_mode"] == {
            "enabled": False,
            "block_before_path_lstat": True,
            "block_before_input_open": True,
            "block_before_temp_creation": True,
            "block_before_output_write": True,
            "candidate_files": [],
        },
        "literal anchor:candidate pre-filesystem gate",
    )
    need(
        tuple(
            (
                row["round"], row["admission"], row["manifest_file_sha256"],
                row["result_file_sha256"], row["result_sha256"],
                row["verification_file_sha256"], row["verification_sha256"],
            )
            for row in admissions[:3]
        )
        == (
            (
                "Round306B0", "SEALED_FORMAL_CONSUMABLE",
                "9846b36d28bb1507b273de3e613a5ecd5ac6515258042bf8b91b89e0c156b269",
                "badc000c6fadd8807b26a7c3511edc51796c962f150b438956e4c549fd0d5735",
                "9ffe9144bc67f9bb7bb7e9c071b29a000f7d8e89396a3250b8207bfcc950d3d2",
                "f8acc3150d4663d92976a44ab1c3b35c7264f4c4d14808f9133f1184d3f4b590",
                "774813f546184aa30c342840ddfa6b0566ebe4d382acd16d74ead8f03dadaddc",
            ),
            (
                "Round306B1R0", "SEALED_FORMAL_CONSUMABLE_ZERO_THEOREM_CREDIT",
                "f23f4639629e920596e1ecadbb1cd7708f93308dc5780a0f82c196edc0f46aec",
                "ca66501d42894dce364ff905045ae69f67cf52c9142ba8f7b45973f857966f04",
                "ad2454ded68ffdcd4b37d39a43b60220ca4fbad780197e0443bcf4ce1904a46c",
                "2242732077165e085f6f2e50f2d061a532a3b43d9e9bc0efc17afac3d45df040",
                "3cb6c976f411a4ad05369434dab8d60ff98fea7204fddd8dd628d6e67c644ea8",
            ),
            (
                "Round306B1G0", "SEALED_FORMAL_CONSUMABLE_ZERO_THEOREM_CREDIT",
                "6f79385d0eed9c13bcc1501c8a189e947f1194d28e198290e6a4b2b2a376a9b8",
                "3f494ebc9f046bfe9f42aef16edeadaece099d7ba7547b11f07484e3f6d81b9e",
                "7bb3def1952176cbaf98723a6a2c5126e3c9193efac36a0d9a2c07533e0ec9bd",
                "65b7a01fd82535f357dbb44b8c68a68c86afcbb75b1c1c9b9159b71f9815139a",
                "542de6d90a6dcb6cd8775a1caf6fe3c3e62bbae49a10e864a7820ba3d083f700",
            ),
        ),
        "literal anchor:sealed dependency pins and admissions",
    )
    need(
        (
            admissions[3]["admission"], admissions[3]["formal_package_state"],
            admissions[3]["draft_file_sha256"],
            admissions[3]["complete_atlas_loader_installed"],
            admissions[3]["formal_manifest"], admissions[3]["formal_result"],
            admissions[3]["formal_verification"],
        )
        == (
            "CONTRACT_ONLY", "FORMAL_ABSENT",
            "6e198755d946bc5828a4366dc818469df7af5e44873c470d9d1050003960473a",
            False, None, None, None,
        ),
        "literal anchor:B1A remains an unsealed loader-false draft",
    )
    need(
        tuple(
            (row["node_id"], row["obligation_type"], row["row_count"], tuple(row["depends_on"]))
            for row in document["obligation_dependency_rows"]
        )
        == (
            ("G1", "INDEPENDENT_DEFINITION_ROOT", 38_624, ()),
            ("G2a", "DEPENDENT_GRAPH_TO_SHEET_IDENTIFICATION", 38_624, ("G1",)),
            ("G2b", "DEPENDENT_GRAPH_TO_SIDE_INCIDENCE_REFERENCE", 76_848, ("G1",)),
            ("R1", "INDEPENDENT_PREDICATE_CELL_DEFINITION", 295_340, ()),
            ("R2", "DEPENDENT_MEMBER_FULL_SUPPORT_UNION", 295_336, ("R1",)),
            ("A1", "INDEPENDENT_ANALYTIC_DEFINITION_ROOT", 17_940, ()),
            ("A2", "DEPENDENT_ANALYTIC_INCIDENCE", 62_152, ("A1",)),
        ),
        "literal anchor:typed dependency DAG",
    )
    separation = document["semantic_separation"]
    need(
        all(
            separation[key] is True
            for key in (
                "four_R1_split_cells_are_not_member_identities",
                "graph_definition_gap_is_not_edge",
                "graph_sheet_identification_is_not_adjacency",
                "graph_side_incidence_reference_is_not_member_pair",
                "Round236_side_reference_is_not_B0_member",
                "dependent_incidence_is_not_independent_root",
                "representation_alias_mints_no_member_identity",
                "outer_box_is_not_full_normalized_support",
                "strict_inner_witness_is_not_full_normalized_support",
                "those_two_counts_are_not_interchangeable",
            )
        ),
        "literal anchor:semantic separations",
    )
    need(
        tuple(
            (row["family_id"], row["role"], row["official_key_is_payload_only"], row["return_signature_is_payload_only"])
            for row in transitions
        )
        == (
            ("SAME_CHART_RELATIVE_CELLS", "POSITIVE_ROUTING_FAMILY", True, True),
            ("RETAINED_CONTINUATION", "POSITIVE_ROUTING_FAMILY", True, True),
            ("OUTGOING_GRAPHS", "POSITIVE_ROUTING_FAMILY", True, True),
            ("SINGLE_GRAPHS", "POSITIVE_ROUTING_FAMILY", True, True),
            ("DOUBLE_GRAPHS", "POSITIVE_ROUTING_FAMILY", True, True),
            ("SHEET_OWNER", "POSITIVE_ROUTING_FAMILY", True, True),
            ("SHEET_SHADOW", "POSITIVE_ROUTING_FAMILY", True, True),
            ("REVERSE_RECHART", "POSITIVE_ROUTING_FAMILY", True, True),
            ("TRUE_CYCLIC_SEAM_E_TO_N", "POSITIVE_ROUTING_FAMILY", True, True),
            ("TRUE_CYCLIC_SEAM_N_TO_W", "POSITIVE_ROUTING_FAMILY", True, True),
            ("TRUE_CYCLIC_SEAM_W_TO_S", "POSITIVE_ROUTING_FAMILY", True, True),
            ("TRUE_CYCLIC_SEAM_S_TO_E", "POSITIVE_ROUTING_FAMILY", True, True),
            ("Jx_NEGATIVE_CONTROL", "NEGATIVE_CONTROL_NON_GLUE", True, True),
            ("Jy_NEGATIVE_CONTROL", "NEGATIVE_CONTROL_NON_GLUE", True, True),
            ("JxJy_NEGATIVE_CONTROL", "NEGATIVE_CONTROL_NON_GLUE", True, True),
            ("SIGNED_BOUNDARY_FACES", "POSITIVE_ROUTING_FAMILY", True, True),
            ("COMPLETE_BOUNDARY_FACES", "POSITIVE_ROUTING_FAMILY", True, True),
            ("POSITIVE_VOLUME_CARRIERS", "POSITIVE_ROUTING_FAMILY", True, True),
            ("REPRESENTATION_ALIASES", "POSITIVE_ROUTING_FAMILY", True, True),
            ("INCLUDED_STRATUM_ATTACHMENTS", "POSITIVE_ROUTING_FAMILY", True, True),
        ),
        "literal anchor:transition families, filters, and negative controls",
    )
    need(
        tuple(
            (row["pair_class_short"], row["B0_pair_class"], row["cross_component_pair_count"])
            for row in denominator_rows
        )
        == (
            ("O/O", "OCCURRENCE__OCCURRENCE", 92_536_544_199),
            ("O/P3D", "OCCURRENCE__VIRTUAL_POSITIVE_3D", 40_785_517_502),
            ("O/sheet", "OCCURRENCE__VIRTUAL_SHEET", 16_648_669_731),
            ("P3D/P3D", "VIRTUAL_POSITIVE_3D__VIRTUAL_POSITIVE_3D", 4_474_700_754),
            ("P3D/sheet", "VIRTUAL_POSITIVE_3D__VIRTUAL_SHEET", 3_649_299_612),
            ("sheet/sheet", "VIRTUAL_SHEET__VIRTUAL_SHEET", 743_352_556),
        )
        and document["cross_component_pair_denominator_total"] == 158_838_084_354,
        "literal anchor:pair partition",
    )
    shard = document["shard_contract"]
    need(
        (
            shard["member_home_block"], shard["home_block_count"],
            shard["canonical_unordered_pair"], shard["pair_home"],
            shard["endpoint_reversal_is_same_canonical_pair"],
            shard["one_and_only_one_home_shard_per_pair"],
            shard["global_pair_uniqueness_required"],
            shard["within_component_pairs_excluded"],
            shard["per_class_per_shard_equation"],
        )
        == (
            "first_4_hex(SHA256(ASCII canonical_B0_member_id))", 65_536,
            "B0_member_id_lexicographic_min_then_max",
            "(pair_class,home_block(left),home_block(right)) after canonicalization",
            True, True, True, True,
            "cross_component_pair_count=exact_block_disjoint_pair_count+unique_emitted_candidate_pair_count+unresolved_gap_pair_count",
        ),
        "literal anchor:shard home and closure equation",
    )
    need(
        tuple(
            (row["source_round"], row["family"], row["edge_application_row_count"])
            for row in recovery["recovery_rows"]
        )
        == (
            ("R297", "ORDINARY_FACE_OCCURRENCE_EDGE", 330_724),
            ("R296", "TRUE_SEAM_OCCURRENCE_EDGE", 48_444),
            ("R303B", "UNIFIED_ATTACHMENT_EDGE", 44_104),
            ("R299C", "R292_SIGNED_SUPPORT_FACE_EDGE", 25_452),
            ("R300E", "R248_HALF_OPEN_OWNER_LOWER_COMPONENT_EDGE", 12_992),
            ("R300B", "REGISTRY_BOUNDARY_AND_COMPLETE_R275_FACE", 10_416),
            ("R300C", "VIRTUAL_STRATUM_POSITIVE_VOLUME_EDGE", 6_314),
            ("R300F", "R245_HALF_OPEN_OWNER_SHEET_ATTACHMENT", 264),
            ("R305B", "TWO_SIDED_PHYSICAL_INCLUSION_EDGE", 8),
        )
        and recovery["edge_application_row_count"] == 478_718
        and recovery["required_missing_row_count"] == 0
        and recovery["required_orphan_row_count"] == 0
        and recovery["required_duplicate_recovery_row_count"] == 0,
        "literal anchor:known-edge partition and exact recovery",
    )
    need(
        tuple(document["future_ledger_names"])
        == (
            "feature_definition", "member_cover", "transition_witness",
            "unique_candidate_pair", "known_edge_recovery", "pair_route_shard",
            "candidate_classification", "gap",
        ),
        "literal anchor:future ledgers",
    )
    need(
        tuple(classification["exact_allowed_classifications"])
        == ("EXACT_NONEDGE", "KNOWN_LEGAL", "NEW_LEGAL_CROSS_COMPONENT", "UNRESOLVED")
        and classification["unresolved_nonzero_blocks_PASS"] is True
        and classification["new_legal_cross_component_status"]
        == "RESTART_REQUIRED_ZERO_MAXIMALITY_CREDIT"
        and classification["new_edge_may_be_silently_added_to_existing_DSU"] is False
        and classification["restart_requires_new_physical_theorem"] is True
        and classification["restart_requires_fresh_DSU"] is True
        and classification["restart_requires_B0_refreeze"] is True
        and classification["restart_requires_full_B1_B2_replay"] is True,
        "literal anchor:classification, unresolved gate, and restart",
    )
    wire = document["future_wire_path_publication_contract"]
    need(
        all(wire[key] is True for key in (
            "strict_JSON_duplicate_keys_rejected",
            "strict_JSON_nonfinite_numbers_rejected",
            "strict_JSON_trailing_bytes_rejected",
            "canonical_gzip_exact_bytes_required", "gzip_multistream_rejected",
            "symlink_rejected", "hardlink_rejected", "path_replacement_rejected",
            "output_no_clobber", "independent_verification_required",
            "formal_manifest_is_verification_last",
        )),
        "literal anchor:wire, path, no-clobber, verification-last",
    )
    # A literal digest over the canonical public document is independent of
    # every factory/global above.  It catches same-total repartition attacks
    # and any coherent producer mutation not named by the readable anchors.
    need(
        hashlib.sha256(canonical(document).encode("ascii")).hexdigest()
        == "adbd6a6f45a40fd2a6fb9a330b17c8f8e86a22a02c2058348d6981a913ffe2e8",
        "literal anchor:canonical contract semantic digest",
    )

    # Closed equality still rejects unknown fields, but is only a secondary
    # check after independent literals and the semantic digest above.
    need(document == _contract_document(), "exact closed contract")


def contract() -> dict[str, Any]:
    document = _contract_document()
    validate_contract(document)
    return document


def build_candidate(_candidate_dir: Path) -> NoReturn:
    """Hard gate: deliberately performs no path or filesystem operation."""

    raise ContractBlocked(CANDIDATE_BLOCK_REASON)


def _set_path(document: dict[str, Any], path: tuple[Any, ...], replacement: Any) -> None:
    target: Any = document
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = replacement


def _setter(path: tuple[Any, ...], replacement: Any) -> Callable[[dict[str, Any]], None]:
    return lambda document: _set_path(document, path, replacement)


def _mutation_fixtures() -> list[tuple[str, Callable[[dict[str, Any]], None]]]:
    return [
        (ATTACK_SCOPE[0], _setter(("semantic_separation", "four_R1_split_cells_are_not_member_identities"), False)),
        (ATTACK_SCOPE[1], _setter(("semantic_separation", "graph_definition_gap_is_not_edge"), False)),
        (ATTACK_SCOPE[2], _setter(("semantic_separation", "graph_sheet_identification_is_not_adjacency"), False)),
        (ATTACK_SCOPE[3], _setter(("semantic_separation", "Round236_side_reference_is_not_B0_member"), False)),
        (ATTACK_SCOPE[4], _setter(("obligation_dependency_rows", 4, "depends_on"), [])),
        (ATTACK_SCOPE[5], _setter(("obligation_dependency_rows", 2, "depends_on"), [])),
        (ATTACK_SCOPE[6], _setter(("obligation_dependency_rows", 6, "obligation_type"), "INDEPENDENT_ANALYTIC_DEFINITION_ROOT")),
        (ATTACK_SCOPE[7], _setter(("semantic_separation", "representation_alias_mints_no_member_identity"), False)),
        (ATTACK_SCOPE[8], _setter(("semantic_separation", "strict_inner_witness_is_not_full_normalized_support"), False)),
        (ATTACK_SCOPE[9], _setter(("transition_routing_boundary", "official_key_is_payload_only_never_filter"), False)),
        (ATTACK_SCOPE[10], _setter(("transition_routing_boundary", "return_signature_is_payload_only_never_filter"), False)),
        (ATTACK_SCOPE[11], _setter(("known_edge_recovery_contract", "geometry_first_before_source_row_id_join"), False)),
        (ATTACK_SCOPE[12], _setter(("shard_contract", "endpoint_reversal_is_same_canonical_pair"), False)),
        (ATTACK_SCOPE[13], _setter(("shard_contract", "global_pair_uniqueness_required"), False)),
        (ATTACK_SCOPE[14], _setter(("pair_class_denominator_rows", 0, "within_component_pairs_admitted"), True)),
        (ATTACK_SCOPE[15], _setter(("pair_class_denominator_rows", 1, "B0_pair_class"), "VIRTUAL_SHEET__VIRTUAL_SHEET")),
        (ATTACK_SCOPE[16], _setter(("pair_class_denominator_rows", 0, "cross_component_pair_count"), 92_536_544_200)),
        (ATTACK_SCOPE[17], lambda document: document["transition_family_contract_rows"].pop()),
        (ATTACK_SCOPE[18], _setter(("transition_routing_boundary", "Round264_empty_bulk_revival_allowed"), True)),
        (ATTACK_SCOPE[19], _setter(("candidate_classification_contract", "unresolved_nonzero_blocks_PASS"), False)),
        (ATTACK_SCOPE[20], _setter(("candidate_classification_contract", "new_edge_may_be_silently_added_to_existing_DSU"), True)),
        (ATTACK_SCOPE[21], _setter(("dependency_admission_rows", 3, "admission"), "SEALED_FORMAL_CONSUMABLE")),
        (ATTACK_SCOPE[22], _setter(("known_edge_recovery_contract", "required_missing_row_count"), 1)),
        (ATTACK_SCOPE[23], _setter(("representation_contract_census", "representation_piece_is_not_member_identity"), False)),
        (ATTACK_SCOPE[24], _setter(("semantic_separation", "those_two_counts_are_not_interchangeable"), False)),
        (ATTACK_SCOPE[25], _setter(("future_wire_path_publication_contract", "strict_JSON_duplicate_keys_rejected"), False)),
        (ATTACK_SCOPE[26], _setter(("future_wire_path_publication_contract", "canonical_gzip_exact_bytes_required"), False)),
        (ATTACK_SCOPE[27], _setter(("future_wire_path_publication_contract", "symlink_rejected"), False)),
        (ATTACK_SCOPE[28], _setter(("future_wire_path_publication_contract", "output_no_clobber"), False)),
        (ATTACK_SCOPE[29], _setter(("future_wire_path_publication_contract", "formal_manifest_is_verification_last"), False)),
        (ATTACK_SCOPE[30], _setter(("candidate_is_formal",), True)),
        (ATTACK_SCOPE[31], _setter(("formal_credit", "maximality"), 1)),
    ]


def _replace_source_once(source: str, old: str, new: str, label: str) -> str:
    """Change the first producer occurrence, leaving later validator anchors."""

    offset = source.find(old)
    need(offset >= 0, "coherent source fixture anchor missing:" + label)
    return source[:offset] + new + source[offset + len(old):]


def _coherent_source_mutants(source: str) -> list[tuple[str, str]]:
    """Build same-source producer mutations that must not teach validation."""

    specs: list[tuple[str, tuple[tuple[str, str], ...]]] = [
        (
            "coherent_valid_but_wrong_B0_manifest_pin",
            ((
                "9846b36d28bb1507b273de3e613a5ecd5ac6515258042bf8b91b89e0c156b269",
                "0000000000000000000000000000000000000000000000000000000000000000",
            ),),
        ),
        (
            "coherent_B0_admission_weakening",
            (("\"admission\": \"SEALED_FORMAL_CONSUMABLE\"", "\"admission\": \"CONTRACT_ONLY\""),),
        ),
        (
            "coherent_B1A_fake_formal_manifest",
            (("\"formal_manifest\": None,", "\"formal_manifest\": \"forged.sha256\","),),
        ),
        (
            "coherent_G2a_type_flatten",
            (("\"DEPENDENT_GRAPH_TO_SHEET_IDENTIFICATION\", 38_624", "\"INDEPENDENT_DEFINITION_ROOT\", 38_624"),),
        ),
        (
            "coherent_G1_illicit_dependency",
            (("(\"G1\", \"Round306B1G0\", \"INDEPENDENT_DEFINITION_ROOT\", 38_624, [])", "(\"G1\", \"Round306B1G0\", \"INDEPENDENT_DEFINITION_ROOT\", 38_624, [\"R1\"])"),),
        ),
        (
            "coherent_graph_sheet_adjacency_confusion",
            (("\"graph_sheet_identification_is_not_adjacency\": True", "\"graph_sheet_identification_is_not_adjacency\": False"),),
        ),
        (
            "coherent_official_key_filter",
            (("\"official_key_is_payload_only_never_filter\": True", "\"official_key_is_payload_only_never_filter\": False"),),
        ),
        (
            "coherent_negative_control_role_promotion",
            ((
                "negative = {\"Jx_NEGATIVE_CONTROL\", \"Jy_NEGATIVE_CONTROL\", \"JxJy_NEGATIVE_CONTROL\"}",
                "negative: set[str] = set()",
            ),),
        ),
        (
            "coherent_shard_home_rewrite",
            ((
                "\"member_home_block\": \"first_4_hex(SHA256(ASCII canonical_B0_member_id))\"",
                "\"member_home_block\": \"official_key_prefix\"",
            ),),
        ),
        (
            "coherent_shard_equation_weakening",
            ((
                "cross_component_pair_count=exact_block_disjoint_pair_count+",
                "cross_component_pair_count=exact_block_disjoint_pair_count-",
            ),),
        ),
        (
            "coherent_known_edge_missing_nonzero",
            (("\"required_missing_row_count\": 0", "\"required_missing_row_count\": 1"),),
        ),
        (
            "coherent_unresolved_PASS_weakening",
            (("\"unresolved_nonzero_blocks_PASS\": True", "\"unresolved_nonzero_blocks_PASS\": False"),),
        ),
        (
            "coherent_fresh_DSU_restart_weakening",
            (("\"restart_requires_fresh_DSU\": True", "\"restart_requires_fresh_DSU\": False"),),
        ),
        (
            "coherent_candidate_input_gate_weakening",
            (("\"block_before_input_open\": True", "\"block_before_input_open\": False"),),
        ),
        (
            "coherent_JSON_duplicate_key_weakening",
            (("\"strict_JSON_duplicate_keys_rejected\": True", "\"strict_JSON_duplicate_keys_rejected\": False"),),
        ),
        (
            "coherent_pair_partition_same_total",
            (
                (
                    "(\"O/O\", \"OCCURRENCE__OCCURRENCE\", 92_536_544_199)",
                    "(\"O/O\", \"OCCURRENCE__OCCURRENCE\", 92_536_544_200)",
                ),
                (
                    "(\"O/P3D\", \"OCCURRENCE__VIRTUAL_POSITIVE_3D\", 40_785_517_502)",
                    "(\"O/P3D\", \"OCCURRENCE__VIRTUAL_POSITIVE_3D\", 40_785_517_501)",
                ),
            ),
        ),
        (
            "coherent_known_edge_partition_same_total",
            (
                (
                    "(\"R297\", \"ORDINARY_FACE_OCCURRENCE_EDGE\", 330_724)",
                    "(\"R297\", \"ORDINARY_FACE_OCCURRENCE_EDGE\", 330_725)",
                ),
                (
                    "(\"R296\", \"TRUE_SEAM_OCCURRENCE_EDGE\", 48_444)",
                    "(\"R296\", \"TRUE_SEAM_OCCURRENCE_EDGE\", 48_443)",
                ),
            ),
        ),
        (
            "coherent_transition_family_substitution",
            (("\"SAME_CHART_RELATIVE_CELLS\",", "\"SAME_CHART_RELATIVE_CELLZ\","),),
        ),
        (
            "coherent_classification_substitution",
            (("\"EXACT_NONEDGE\",", "\"APPROXIMATE_NONEDGE\","),),
        ),
        (
            "coherent_no_clobber_weakening",
            (("\"output_no_clobber\": True", "\"output_no_clobber\": False"),),
        ),
    ]
    mutants: list[tuple[str, str]] = []
    for label, replacements in specs:
        mutant = source
        for old, new in replacements:
            mutant = _replace_source_once(mutant, old, new, label)
        need(mutant != source, "coherent source mutation changed bytes:" + label)
        mutants.append((label, mutant))
    return mutants


def _coherent_source_attack_test() -> tuple[list[dict[str, Any]], int]:
    """Compile producer-coherent mutants; independent literals must reject."""

    source_path = Path(__file__)
    source = source_path.read_text(encoding="utf-8")
    source_size = len(source.encode("utf-8"))
    attacks: list[dict[str, Any]] = []
    for index, (label, mutant) in enumerate(_coherent_source_mutants(source)):
        namespace: dict[str, Any] = {
            "__name__": "round306b2c0_coherent_mutant_" + str(index),
            "__file__": str(source_path),
        }
        code = compile(mutant, "<" + label + ">", "exec")
        exec(code, namespace)
        mutant_blocked = namespace["ContractBlocked"]
        try:
            namespace["contract"]()
        except mutant_blocked:
            rejected = True
        else:
            rejected = False
        need(rejected, "coherent source mutation accepted:" + label)
        attacks.append({"attack": label, "category": "COHERENT_SOURCE_MUTATION", "rejected": True})
    return attacks, source_size


def _candidate_hard_gate_probe() -> dict[str, int]:
    calls = {"path_lstat": 0, "open": 0, "temp": 0, "write": 0}

    def forbidden(kind: str) -> Callable[..., NoReturn]:
        def probe(*_args: Any, **_kwargs: Any) -> NoReturn:
            calls[kind] += 1
            raise AssertionError("candidate touched forbidden boundary:" + kind)
        return probe

    patches = (
        (builtins, "open", "open"),
        (os, "open", "open"),
        (os, "lstat", "path_lstat"),
        (os, "stat", "path_lstat"),
        (os, "mkdir", "write"),
        (os, "makedirs", "write"),
        (os, "rename", "write"),
        (os, "replace", "write"),
        (tempfile, "mkdtemp", "temp"),
        (tempfile, "mkstemp", "temp"),
        (tempfile, "NamedTemporaryFile", "temp"),
        (Path, "open", "open"),
        (Path, "lstat", "path_lstat"),
        (Path, "stat", "path_lstat"),
        (Path, "mkdir", "write"),
        (Path, "write_text", "write"),
        (Path, "write_bytes", "write"),
        (Path, "touch", "write"),
        (Path, "rename", "write"),
        (Path, "replace", "write"),
    )
    with ExitStack() as stack:
        for owner, name, kind in patches:
            stack.enter_context(mock.patch.object(owner, name, side_effect=forbidden(kind)))
        try:
            build_candidate(Path("/never-inspected/round306b2c0-candidate-probe"))
        except ContractBlocked as exc:
            need(str(exc) == CANDIDATE_BLOCK_REASON, "candidate block reason")
        else:
            raise ContractBlocked("candidate hard gate did not fire")
    need(calls == {"path_lstat": 0, "open": 0, "temp": 0, "write": 0}, "candidate pre-filesystem hard gate")
    return calls


def self_test() -> dict[str, Any]:
    base = contract()
    attacks: list[dict[str, Any]] = []
    for attack, mutate in _mutation_fixtures():
        mutant = deepcopy(base)
        mutate(mutant)
        need(mutant != base, "mutation changed contract:" + attack)
        try:
            validate_contract(mutant)
        except (ContractBlocked, KeyError, TypeError, ValueError):
            rejected = True
        else:
            rejected = False
        need(rejected, "semantic mutation accepted:" + attack)
        attacks.append({"attack": attack, "category": "UNIT_SEMANTIC_MUTATION", "rejected": True})

    coherent_attacks, contract_source_bytes_read = _coherent_source_attack_test()
    calls = _candidate_hard_gate_probe()
    return {
        "schema": SCHEMA + ".self-test.v1",
        "status": "PASS_LIGHTWEIGHT_ROUND306B2C0_ZERO_CREDIT_CONTRACT_SELF_TEST",
        "unit_attack_count": len(attacks),
        "unit_attacks_rejected": len(attacks),
        "unit_attacks": attacks,
        "coherent_source_attack_count": len(coherent_attacks),
        "coherent_source_attacks_rejected": len(coherent_attacks),
        "coherent_source_attacks": coherent_attacks,
        "contract_source_bytes_read": contract_source_bytes_read,
        "contract_semantic_anchor_sha256":
            hashlib.sha256(canonical(base).encode("ascii")).hexdigest(),
        "reconstruction_attack_count": 0,
        "reconstruction_performed": False,
        "large_sources_opened": 0,
        "candidate_hard_gate_probe_count": 1,
        "candidate_path_lstat_calls": calls["path_lstat"],
        "candidate_open_calls": calls["open"],
        "candidate_temp_calls": calls["temp"],
        "candidate_write_calls": calls["write"],
        "candidate_writes": 0,
        "pair_routes_emitted": 0,
        "formal_credit": 0,
        "D02": "BLOCKED",
        "CM2": "NO-GO_FOR_CLAIM",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--print-contract", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--candidate-dir", type=Path)
    args = parser.parse_args()
    need(
        sum((args.print_contract, args.self_test, args.candidate_dir is not None)) == 1,
        "choose exactly one mode",
    )
    if args.print_contract:
        print(canonical(contract()))
    elif args.self_test:
        print(canonical(self_test()))
    else:
        assert args.candidate_dir is not None
        build_candidate(args.candidate_dir)


if __name__ == "__main__":
    try:
        main()
    except ContractBlocked as exc:
        raise SystemExit(str(exc)) from None
