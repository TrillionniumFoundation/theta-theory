#!/usr/bin/env python3
"""Round306B1AF0 formal full-feature-cover schema contract.

This is a versioned, non-producing, zero-credit contract.  It does not alter
the frozen Round306B1A diagnostic draft and therefore does not invalidate the
Round306B2C0 pin to that draft.  Its only purpose is to freeze the exact typed
wire interface, accounting equations, proof-kernel boundary, and publication
transaction required for a future formal Round306B1A full feature-cover
package.

The contract resolves a scope cycle in the diagnostic draft.  Round306B1A is
responsible for source-free feature definitions, full member-support cover,
and representation closure.  It must be transition-ready, but it must not
claim a complete transition atlas.  Transition witnesses, pair routing,
known-edge recovery, maximality, fibres, and global dispositions remain the
downstream Round306B2 responsibility.

Candidate mode is deliberately blocked before path inspection, input open,
temporary creation, or output write.  A separate future producer and an
independent verifier must implement this contract before any formal credit is
possible.
"""

from __future__ import annotations

import argparse
import builtins
from copy import deepcopy
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import tempfile
from typing import Any, Callable, NoReturn
from unittest import mock


class ContractBlocked(RuntimeError):
    """Fail-closed schema, dependency, or candidate-mode violation."""


def need(condition: bool, label: str) -> None:
    if not condition:
        raise ContractBlocked(label)


SCHEMA = "cm2.round306b1af0.source-g-formal-full-feature-cover-schema-contract.v1"
STATUS = (
    "BLOCKED_ZERO_CREDIT_SCHEMA_FROZEN__FULL_FEATURE_COVER_LOADER_AND_"
    "INDEPENDENT_VERIFIER_ABSENT"
)
CANDIDATE_BLOCK_REASON = (
    "Round306B1AF0 is a non-producing schema contract; candidate mode is "
    "blocked before path lstat/open/temp/write"
)
HEX64 = re.compile(r"^[0-9a-f]{64}$")

MEMBER_COUNT = 564_492
OCCURRENCE_COUNT = 431_208
VIRTUAL_POSITIVE_3D_COUNT = 94_660
VIRTUAL_SHEET_COUNT = 38_624
COMPONENT_COUNT = 92_688

REPRESENTATION_COUNT = 611_904
PRIMARY_REPRESENTATION_COUNT = 564_492
EXTRA_REPRESENTATION_COUNT = 47_412
REFINED_PRIMARY_EXTRA_COUNT = 848
ALIAS_REPRESENTATION_COUNT = 46_564
R294_ALIAS_COUNT = 46_288
R295A_ALIAS_COUNT = 276

ROOT_COUNT = 351_904
DEPENDENT_COUNT = 472_960
FEATURE_DEFINITION_COUNT = 824_864

NODE_ORDER = ("A1", "A2", "R1", "R2", "G1", "G2a", "G2b")

ROOT_FAMILIES = (
    ("A1", "R204_TARGET_REGULAR_GRAPH_SHEET_DEFINITION", 224),
    ("A1", "R208_FACTOR_SHEET_DEFINITION", 17_716),
    ("R1", "R269_PREDICATE_SOURCE_CELL_DEFINITION", 187_128),
    ("R1", "R270_PREDICATE_SOURCE_CELL_DEFINITION", 37_712),
    ("R1", "R271_PREDICATE_SOURCE_CELL_DEFINITION", 70_356),
    ("R1", "R272_PREDICATE_SOURCE_CELL_DEFINITION", 144),
    ("G1", "R235_SINGLE_ENDPOINT_GRAPH_DEFINITION", 38_328),
    ("G1", "R236_DOUBLE_ENDPOINT_GRAPH_DEFINITION", 32),
    ("G1", "R242_UNIQUE_TRANSITION_GRAPH_DEFINITION", 264),
)

DEPENDENT_FAMILIES = (
    ("A2", "R204_TARGET_GRAPH_CURVE_INCIDENCE", 504, ("A1",)),
    ("A2", "R204_TARGET_GRAPH_POINT_INCIDENCE", 280, ("A1",)),
    ("A2", "R208_CURVE_INCIDENCE", 20_456, ("A1",)),
    ("A2", "R208_ENDPOINT_INCIDENCE", 40_912, ("A1",)),
    ("R2", "R288_MEMBER_FULL_SUPPORT_UNION", 295_336, ("R1",)),
    ("G2a", "GRAPH_TO_SHEET_IDENTIFICATION", 38_624, ("G1",)),
    ("G2b", "R235_GRAPH_SIDE_INCIDENCE", 76_256, ("G1",)),
    ("G2b", "R236_GRAPH_SIDE_INCIDENCE", 64, ("G1",)),
    ("G2b", "R242_GRAPH_SIDE_INCIDENCE", 528, ("G1",)),
)

MEMBER_TRANCHES = (
    ("PRESERVED_ROUND266_EXISTING_LOCAL_OCCURRENCE", 126_468),
    ("NEW_ROUND288_CANONICAL_ATOM_OCCURRENCE", 295_336),
    ("NEW_ROUND292_REFINED_R287_SUPPORT_COMPONENT_OCCURRENCE", 9_404),
    ("VIRTUAL_POSITIVE_3D__INHERITED_R245", 6_124),
    ("VIRTUAL_POSITIVE_3D__ROUND248_WALL", 88_536),
    ("VIRTUAL_SHEET__INHERITED_R245", 264),
    ("VIRTUAL_SHEET__ROUND248_WALL", 38_360),
)

REPRESENTATION_TRANCHES = (
    ("OCCURRENCE_TPS", 466_768),
    ("OCCURRENCE_T2PS", 11_852),
    ("VIRTUAL_POSITIVE_3D", 94_660),
    ("VIRTUAL_SHEET", 38_624),
)

AST_OPERATORS = (
    "CONST_Q",
    "VAR",
    "NEG",
    "ADD",
    "SUB",
    "MUL",
    "DIV_NONZERO",
    "SQUARE",
    "SQRT_POSITIVE",
    "EQ_ZERO",
    "LT_ZERO",
    "GT_ZERO",
    "AND",
    "OR_DISJOINT",
    "RESTRICT",
)

PROOF_KERNELS = (
    "EXACT_RATIONAL_AST_NORMALIZATION_V1",
    "DIRECTED_INTERVAL_SIGN_CERTIFICATE_V1",
    "PREDICATE_CELL_EQUIVALENCE_V1",
    "DEPENDENT_INCIDENCE_RESTRICTION_V1",
    "FINITE_DISJOINT_SUPPORT_UNION_V1",
    "GRAPH_SHEET_PHYSICAL_INCIDENCE_V1",
)

FILES = {
    "feature": "cm2_round306b1a_source_g_r306b0_formal_full_feature_cover_feature_definition.json.gz",
    "member": "cm2_round306b1a_source_g_r306b0_formal_full_feature_cover_member_cover.json.gz",
    "piece": "cm2_round306b1a_source_g_r306b0_formal_full_feature_cover_representation_piece.json.gz",
    "gap": "cm2_round306b1a_source_g_r306b0_formal_full_feature_cover_gap.json.gz",
    "result": "cm2_round306b1a_source_g_r306b0_formal_full_feature_cover_result.json",
}
CANDIDATE_ORDER = tuple(FILES.values())

FORMAL_PACKAGE_MEMBERS = (
    "cm2_round306b1a_source_g_r306b0_formal_full_feature_cover.py",
    FILES["feature"],
    FILES["member"],
    FILES["piece"],
    FILES["gap"],
    FILES["result"],
    "cm2_round306b1a_source_g_r306b0_formal_full_feature_cover_promotion_verifier.py",
    "cm2_round306b1a_source_g_r306b0_formal_full_feature_cover_attack_suite.json",
    "cm2_round306b1a_source_g_r306b0_formal_full_feature_cover_verification.json",
    "cm2_round306b1a_source_g_r306b0_formal_full_feature_cover_report.md",
    "cm2_round306b1a_source_g_r306b0_formal_full_feature_cover_cold_replay.md",
)

DEPENDENCY_PINS = (
    (
        "Round306B0",
        "cm2_round306b0_source_g_r306a_universe_support_source_freeze_manifest.sha256",
        1_760,
        "9846b36d28bb1507b273de3e613a5ecd5ac6515258042bf8b91b89e0c156b269",
        "MANIFEST",
    ),
    (
        "Round306B0",
        "cm2_round306b0_source_g_r306a_universe_support_source_freeze_result.json",
        9_450,
        "badc000c6fadd8807b26a7c3511edc51796c962f150b438956e4c549fd0d5735",
        "RESULT",
    ),
    (
        "Round306B0",
        "cm2_round306b0_source_g_r306a_universe_support_source_freeze_verification.json",
        7_003,
        "f8acc3150d4663d92976a44ab1c3b35c7264f4c4d14808f9133f1184d3f4b590",
        "VERIFICATION",
    ),
    (
        "Round306B0",
        "cm2_round306b0_source_g_r306a_universe_support_source_freeze_member_support_source_index.json.gz",
        162_499_140,
        "c9a8649c8473bb6a170187e7f803e95748d2ff2198b1b846d97383dd5f0581af",
        "CONSUMED_LEDGER",
    ),
    (
        "Round306B1R0",
        "cm2_round306b1r0_source_g_r288_predicate_source_inventory_and_union_freeze_manifest.sha256",
        1_571,
        "f23f4639629e920596e1ecadbb1cd7708f93308dc5780a0f82c196edc0f46aec",
        "MANIFEST",
    ),
    (
        "Round306B1R0",
        "cm2_round306b1r0_source_g_r288_predicate_source_inventory_and_union_freeze_result.json",
        3_019,
        "ca66501d42894dce364ff905045ae69f67cf52c9142ba8f7b45973f857966f04",
        "RESULT",
    ),
    (
        "Round306B1R0",
        "cm2_round306b1r0_source_g_r288_predicate_source_inventory_and_union_freeze_verification.json",
        11_531,
        "2242732077165e085f6f2e50f2d061a532a3b43d9e9bc0efc17afac3d45df040",
        "VERIFICATION",
    ),
    (
        "Round306B1R0",
        "cm2_round306b1r0_source_g_r288_predicate_source_inventory_and_union_freeze_predicate_source_cell.json.gz",
        105_989_322,
        "19d13d93fc02296f673ca18cc2edbd96174985f7be8fb0e03694582b188b0f96",
        "CONSUMED_LEDGER",
    ),
    (
        "Round306B1R0",
        "cm2_round306b1r0_source_g_r288_predicate_source_inventory_and_union_freeze_member_union.json.gz",
        123_019_951,
        "4b3633782e4514f598cb9cce19930ba31616f7d42aab002df4f77f9b4601ddf7",
        "CONSUMED_LEDGER",
    ),
    (
        "Round306B1G0",
        "cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_manifest.sha256",
        1_959,
        "6f79385d0eed9c13bcc1501c8a189e947f1194d28e198290e6a4b2b2a376a9b8",
        "MANIFEST",
    ),
    (
        "Round306B1G0",
        "cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_result.json",
        5_006,
        "3f494ebc9f046bfe9f42aef16edeadaece099d7ba7547b11f07484e3f6d81b9e",
        "RESULT",
    ),
    (
        "Round306B1G0",
        "cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_verification.json",
        11_575,
        "65b7a01fd82535f357dbb44b8c68a68c86afcbb75b1c1c9b9159b71f9815139a",
        "VERIFICATION",
    ),
    (
        "Round306B1G0",
        "cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_graph_source_inventory.json.gz",
        11_720_893,
        "5ac33be2b7639e1d30ae14abd5a7cf4cc6d1cc65fb0730e98616434f08921cb0",
        "CONSUMED_LEDGER",
    ),
    (
        "Round306B1G0",
        "cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_graph_sheet_join.json.gz",
        13_922_080,
        "041328aa135a1a67cbbdc8c5d84fe2c1a9bef2231a6cb33668ab05ecd6b227e3",
        "CONSUMED_LEDGER",
    ),
    (
        "Round306B1G0",
        "cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_graph_side_join.json.gz",
        25_932_945,
        "d79af13182f99cdb2df6d39731e762b0d145baf79772b99be5069669c5b80ee1",
        "CONSUMED_LEDGER",
    ),
    (
        "Round306B1A_DIAGNOSTIC",
        "cm2_round306b1a_source_g_r306b0_carrier_witness_and_support_gap_atlas.py",
        45_144,
        "6e198755d946bc5828a4366dc818469df7af5e44873c470d9d1050003960473a",
        "INERT_SCOPE_PREDECESSOR",
    ),
    (
        "Round306B2C0",
        "cm2_round306b2c0_source_g_feature_transition_pair_routing_contract.py",
        53_212,
        "6a4fbbc3c614b7adaf275d0870a0205360827ed9fe89b8e26748e966a04f4d69",
        "INERT_DOWNSTREAM_CONTRACT",
    ),
)

OBJECT_PINS = {
    "Round306B0_result_sha256":
        "9ffe9144bc67f9bb7bb7e9c071b29a000f7d8e89396a3250b8207bfcc950d3d2",
    "Round306B0_verification_sha256":
        "774813f546184aa30c342840ddfa6b0566ebe4d382acd16d74ead8f03dadaddc",
    "Round306B1R0_result_sha256":
        "ad2454ded68ffdcd4b37d39a43b60220ca4fbad780197e0443bcf4ce1904a46c",
    "Round306B1R0_verification_sha256":
        "3cb6c976f411a4ad05369434dab8d60ff98fea7204fddd8dd628d6e67c644ea8",
    "Round306B1G0_result_sha256":
        "7bb3def1952176cbaf98723a6a2c5126e3c9193efac36a0d9a2c07533e0ec9bd",
    "Round306B1G0_verification_sha256":
        "542de6d90a6dcb6cd8775a1caf6fe3c3e62bbae49a10e864a7820ba3d083f700",
}


def canonical(value: Any) -> str:
    return json.dumps(
        value,
        ensure_ascii=True,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode("ascii")).hexdigest()


def _dependency_rows() -> list[dict[str, Any]]:
    return [
        {
            "round": round_id,
            "filename": filename,
            "exact_size": size,
            "file_sha256": file_sha,
            "role": role,
        }
        for round_id, filename, size, file_sha, role in DEPENDENCY_PINS
    ]


def _root_rows() -> list[dict[str, Any]]:
    return [
        {
            "node_id": node,
            "family": family,
            "obligation_role": "INDEPENDENT_SOURCE_FREE_DEFINITION_ROOT",
            "row_count": count,
            "depends_on_nodes": [],
            "requires_evaluable_ast": True,
            "inventory_label_is_definition": False,
            "issues_member_identity": False,
            "issues_unordered_pair": False,
        }
        for node, family, count in ROOT_FAMILIES
    ]


def _dependent_rows() -> list[dict[str, Any]]:
    return [
        {
            "node_id": node,
            "family": family,
            "obligation_role": "DEPENDENT_DEFINITION_OR_INCIDENCE_CLOSURE",
            "row_count": count,
            "depends_on_nodes": list(dependencies),
            "requires_explicit_root_backbinding": True,
            "flattened_as_independent_root": False,
            "issues_member_identity": False,
            "issues_unordered_pair": False,
        }
        for node, family, count, dependencies in DEPENDENT_FAMILIES
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
        "scope_resolution": {
            "predecessor_diagnostic_file_preserved": True,
            "predecessor_diagnostic_file_sha256":
                "6e198755d946bc5828a4366dc818469df7af5e44873c470d9d1050003960473a",
            "downstream_B2C0_file_preserved": True,
            "downstream_B2C0_file_sha256":
                "6a4fbbc3c614b7adaf275d0870a0205360827ed9fe89b8e26748e966a04f4d69",
            "B1A_responsibility": [
                "source_free_feature_definition",
                "complete_member_support_cover",
                "complete_representation_cover",
                "transition_ready_handles_without_transition_completeness_claim",
            ],
            "B1A_excluded_downstream_responsibility": [
                "transition_atlas_completeness",
                "pair_routing",
                "candidate_pair_classification",
                "known_edge_geometry_first_recovery",
                "component_union",
                "maximality",
                "fibre",
                "global_disposition",
            ],
            "transition_atlas_is_candidate_precondition": False,
            "complete_transition_atlas_claimed_by_B1A": False,
            "B1A_formal_package_must_precede_successor_B2_contract": True,
        },
        "dependency_pins": _dependency_rows(),
        "dependency_object_pins": dict(OBJECT_PINS),
        "typed_feature_DAG": {
            "node_order": list(NODE_ORDER),
            "root_families": _root_rows(),
            "dependent_families": _dependent_rows(),
            "independent_root_count": ROOT_COUNT,
            "dependent_closure_count": DEPENDENT_COUNT,
            "feature_definition_ledger_row_count": FEATURE_DEFINITION_COUNT,
            "source_closure_name_is_not_used_as_ambiguous_alias": True,
            "B2_ledger_name": "feature_definition",
        },
        "member_cover_contract": {
            "member_count": MEMBER_COUNT,
            "occurrence_count": OCCURRENCE_COUNT,
            "virtual_positive_3D_count": VIRTUAL_POSITIVE_3D_COUNT,
            "virtual_sheet_count": VIRTUAL_SHEET_COUNT,
            "component_count_is_metadata_only": COMPONENT_COUNT,
            "tranches": [
                {"tranche": name, "row_count": count}
                for name, count in MEMBER_TRANCHES
            ],
            "one_and_only_one_row_per_B0_member": True,
            "missing_member_count_must_equal": 0,
            "orphan_member_count_must_equal": 0,
            "duplicate_member_count_must_equal": 0,
            "outer_envelope_is_full_support": False,
            "inner_witness_is_full_support": False,
            "carrier_box_is_full_support": False,
            "full_support_requires_predicate_equivalence_and_finite_union_proof": True,
            "four_R271_split_cells_mint_member_identities": False,
        },
        "representation_cover_contract": {
            "representation_row_count": REPRESENTATION_COUNT,
            "primary_representation_count": PRIMARY_REPRESENTATION_COUNT,
            "extra_representation_count": EXTRA_REPRESENTATION_COUNT,
            "refined_primary_extra_count": REFINED_PRIMARY_EXTRA_COUNT,
            "alias_representation_count": ALIAS_REPRESENTATION_COUNT,
            "R294_alias_count": R294_ALIAS_COUNT,
            "R295A_alias_count": R295A_ALIAS_COUNT,
            "coordinate_tranches": [
                {"tranche": name, "row_count": count}
                for name, count in REPRESENTATION_TRANCHES
            ],
            "one_primary_representation_per_member": True,
            "every_extra_has_exactly_one_existing_member_owner": True,
            "representation_mints_member_identity": False,
            "missing_representation_count_must_equal": 0,
            "orphan_representation_count_must_equal": 0,
            "duplicate_representation_count_must_equal": 0,
        },
        "feature_definition_row_schema": {
            "common_required_fields": [
                "schema",
                "Round306B1A_feature_definition_row_id",
                "node_id",
                "family",
                "obligation_role",
                "natural_key",
                "source_bindings",
                "proof_kernel_id",
                "formal_feature_definition_credit",
                "row_sha256",
            ],
            "root_required_fields": [
                "definition_ast",
                "coordinate_domain_ast",
                "ast_normal_form_sha256",
                "equivalence_certificate",
            ],
            "dependent_required_fields": [
                "depends_on_feature_definition_row_ids",
                "restriction_or_union_ast",
                "root_backbinding_complete",
                "dependency_certificate",
            ],
            "row_id_rule": (
                "round306b1a-formal-feature:" 
                "SHA256(canonical([node_id,family,natural_key]))"
            ),
            "sort_rule": (
                "NODE_ORDER then family then canonical natural_key then row_id"
            ),
            "allowed_ast_operators": list(AST_OPERATORS),
            "allowed_proof_kernels": list(PROOF_KERNELS),
            "root_ast_is_independently_evaluable": True,
            "source_filename_or_row_id_alone_is_definition": False,
            "proof_method_label_alone_is_definition": False,
            "official_key_is_metadata_only": True,
            "return_signature_is_metadata_only": True,
        },
        "member_cover_row_schema": {
            "required_fields": [
                "schema",
                "Round306B1A_member_cover_row_id",
                "B0_member_id",
                "B0_member_kind",
                "B0_component_id_metadata_only",
                "primary_representation_row_id",
                "support_feature_definition_row_ids",
                "normalized_full_support_ast",
                "finite_support_union_certificate",
                "source_bindings",
                "formal_member_support_credit",
                "row_sha256",
            ],
            "row_id_rule": (
                "round306b1a-member-cover:SHA256(canonical(B0_member_id))"
            ),
            "sort_rule": "B0_member_id then row_id",
            "support_feature_definition_rows_nonempty": True,
            "support_union_cells_pairwise_interior_disjoint": True,
            "support_union_boundary_assignment_complete": True,
            "support_union_equals_member_support": True,
        },
        "representation_piece_row_schema": {
            "required_fields": [
                "schema",
                "Round306B1A_representation_piece_row_id",
                "B0_member_id",
                "representation_role",
                "representation_source_round",
                "coordinate_system",
                "carrier_ast",
                "support_pullback_ast",
                "feature_definition_row_ids",
                "source_bindings",
                "mints_member_identity",
                "formal_representation_cover_credit",
                "row_sha256",
            ],
            "representation_roles": [
                "PRIMARY",
                "REFINED_PRIMARY_EXTRA",
                "ALIAS_EXISTING_MEMBER",
            ],
            "coordinate_systems": ["TPS", "T2PS", "VIRTUAL_P3D", "VIRTUAL_SHEET"],
            "row_id_rule": (
                "round306b1a-representation-piece:"
                "SHA256(canonical([B0_member_id,representation_role,source_bindings]))"
            ),
            "sort_rule": (
                "B0_member_id then representation role order then row_id"
            ),
            "mints_member_identity_must_equal": False,
        },
        "gap_row_schema": {
            "required_fields_if_any": [
                "schema",
                "Round306B1A_gap_row_id",
                "gap_family",
                "blocked_natural_key",
                "source_bindings",
                "reason",
                "formal_credit",
                "row_sha256",
            ],
            "formal_PASS_gap_row_count_must_equal": 0,
            "missing_evaluable_AST_is_gap": True,
            "missing_equivalence_certificate_is_gap": True,
            "missing_root_backbinding_is_gap": True,
            "missing_member_or_representation_is_gap": True,
            "gap_may_be_forced_to_PASS": False,
        },
        "ledger_wire_contract": {
            "candidate_filenames_in_order": list(CANDIDATE_ORDER),
            "feature_definition_filename": FILES["feature"],
            "source_closure_filename": None,
            "feature_definition_is_explicit_B2_consumable_ledger": True,
            "each_row_has_unique_typed_id": True,
            "each_row_has_self_sha256": True,
            "each_ledger_has_exact_row_count": True,
            "each_ledger_has_ledger_sha256": True,
            "each_ledger_has_row_ids_sha256": True,
            "each_ledger_has_row_hashes_sha256": True,
            "each_ledger_has_rows_sha256": True,
            "strict_JSON_duplicate_keys_rejected": True,
            "strict_JSON_nonfinite_numbers_rejected": True,
            "strict_JSON_trailing_bytes_rejected": True,
            "canonical_single_member_gzip_required": True,
            "gzip_second_member_rejected": True,
            "gzip_trailing_bytes_rejected": True,
            "exact_decompressed_wire_size_required": True,
            "bounded_row_token_required": True,
        },
        "graph_and_incidence_semantics": {
            "source_free_graph_definition_count": 38_624,
            "graph_sheet_identification_count": 38_624,
            "graph_side_incidence_reference_count": 76_848,
            "physical_incidence_count": 115_472,
            "B1A_distinct_graph_side_positive_3D_carrier_count": 76_304,
            "graph_side_reference_count_equals_carrier_count": False,
            "Round264_correction_disposition_count": 400,
            "Round264_empty_bulk_may_be_revived": False,
            "graph_sheet_identification_is_adjacency": False,
            "physical_incidence_requires_independent_certificate": True,
        },
        "publication_contract": {
            "private_candidate_file_count": 5,
            "private_candidate_files": list(CANDIDATE_ORDER),
            "formal_manifest_member_count": 11,
            "formal_manifest_members": list(FORMAL_PACKAGE_MEMBERS),
            "sealed_package_file_count_including_manifest": 12,
            "producer_and_verifier_are_independent": True,
            "verifier_may_import_execute_or_parse_producer": False,
            "producer_is_inert_byte_pin_for_verifier": True,
            "two_hash_seed_candidates_must_be_byte_identical": True,
            "independent_no_write_full_reconstruction_required": True,
            "attack_first": True,
            "verification_last": True,
            "formal_manifest_is_verification_last": True,
            "symlink_rejected": True,
            "hardlink_rejected": True,
            "path_replacement_rejected": True,
            "output_no_clobber": True,
            "mode_0600_and_link_count_one_required": True,
            "orphan_stage_count_must_equal": 0,
        },
        "future_formal_PASS_gates": {
            "feature_definition_rows_must_equal": FEATURE_DEFINITION_COUNT,
            "independent_root_rows_must_equal": ROOT_COUNT,
            "dependent_rows_must_equal": DEPENDENT_COUNT,
            "member_cover_rows_must_equal": MEMBER_COUNT,
            "representation_rows_must_equal": REPRESENTATION_COUNT,
            "gap_rows_must_equal": 0,
            "all_root_ASTs_independently_evaluable": True,
            "all_dependent_rows_backbound_to_roots": True,
            "all_member_support_unions_exact": True,
            "all_graph_physical_incidences_certified": True,
            "missing_or_orphan_or_duplicate_counts_must_equal": 0,
            "transition_atlas_complete": False,
            "pair_routing_complete": False,
            "PASS_currently_permitted": False,
        },
        "formal_credit": {
            "current_feature_definition": 0,
            "current_member_support": 0,
            "current_representation_cover": 0,
            "current_transition": 0,
            "current_pair_routing": 0,
            "current_component_union": 0,
            "current_maximality": 0,
            "current_fibre": 0,
            "current_global_disposition": 0,
            "future_verification_marker_may_grant": [
                "feature_definition_consumability",
                "member_support_cover_consumability",
                "representation_cover_consumability",
            ],
            "future_verification_marker_may_not_grant": [
                "transition_atlas",
                "pair_routing",
                "component_union",
                "maximality",
                "fibre",
                "global_disposition",
                "CM2",
            ],
            "D02": "BLOCKED",
            "D03": "NOT_REACHED",
            "D04": "NOT_MINTED",
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "emission_accounting": {
            "large_sources_opened": 0,
            "feature_rows_emitted": 0,
            "member_rows_emitted": 0,
            "representation_rows_emitted": 0,
            "gap_rows_emitted": 0,
            "candidate_files_written": 0,
            "formal_files_written": 0,
        },
    }


def validate_contract(document: dict[str, Any]) -> None:
    """Validate the frozen schema without consulting a producer."""

    need(document.get("schema") == SCHEMA, "schema")
    need(document.get("status") == STATUS, "status")
    need(document.get("candidate_is_formal") is False, "candidate nonformal")

    mode = document["candidate_mode"]
    need(
        mode == {
            "enabled": False,
            "block_before_path_lstat": True,
            "block_before_input_open": True,
            "block_before_temp_creation": True,
            "block_before_output_write": True,
            "candidate_files": [],
        },
        "candidate pre-filesystem gate",
    )

    scope = document["scope_resolution"]
    need(scope["transition_atlas_is_candidate_precondition"] is False, "no scope cycle")
    need(scope["complete_transition_atlas_claimed_by_B1A"] is False, "no transition claim")
    need(
        scope["predecessor_diagnostic_file_sha256"]
        == "6e198755d946bc5828a4366dc818469df7af5e44873c470d9d1050003960473a",
        "predecessor pin",
    )
    need(
        scope["downstream_B2C0_file_sha256"]
        == "6a4fbbc3c614b7adaf275d0870a0205360827ed9fe89b8e26748e966a04f4d69",
        "B2C0 pin",
    )

    pins = document["dependency_pins"]
    need(len(pins) == 17, "dependency pin count")
    need(
        tuple(
            (row["round"], row["filename"], row["exact_size"], row["file_sha256"], row["role"])
            for row in pins
        ) == DEPENDENCY_PINS,
        "dependency literal pins",
    )
    need(
        all(type(row["exact_size"]) is int and row["exact_size"] > 0 for row in pins),
        "positive exact sizes",
    )
    need(
        all(HEX64.fullmatch(row["file_sha256"]) is not None for row in pins),
        "dependency hash syntax",
    )
    need(document["dependency_object_pins"] == OBJECT_PINS, "object pins")

    dag = document["typed_feature_DAG"]
    need(tuple(dag["node_order"]) == NODE_ORDER, "node order")
    roots = dag["root_families"]
    dependents = dag["dependent_families"]
    need(
        tuple((row["node_id"], row["family"], row["row_count"]) for row in roots)
        == ROOT_FAMILIES,
        "root partition",
    )
    need(
        tuple(
            (
                row["node_id"],
                row["family"],
                row["row_count"],
                tuple(row["depends_on_nodes"]),
            )
            for row in dependents
        ) == DEPENDENT_FAMILIES,
        "dependent partition",
    )
    need(sum(row["row_count"] for row in roots) == ROOT_COUNT == 351_904, "root total")
    need(
        sum(row["row_count"] for row in dependents) == DEPENDENT_COUNT == 472_960,
        "dependent total",
    )
    need(
        dag["feature_definition_ledger_row_count"]
        == ROOT_COUNT + DEPENDENT_COUNT
        == FEATURE_DEFINITION_COUNT
        == 824_864,
        "feature ledger total",
    )
    need(dag["B2_ledger_name"] == "feature_definition", "B2 ledger name")
    need(dag["source_closure_name_is_not_used_as_ambiguous_alias"] is True, "no ambiguous source closure")
    need(all(not row["issues_member_identity"] and not row["issues_unordered_pair"] for row in [*roots, *dependents]), "obligation identities")
    need(all(row.get("flattened_as_independent_root") is False for row in dependents), "no dependent flattening")

    members = document["member_cover_contract"]
    need(
        members["occurrence_count"]
        + members["virtual_positive_3D_count"]
        + members["virtual_sheet_count"]
        == members["member_count"]
        == MEMBER_COUNT
        == 564_492,
        "member census",
    )
    need(
        tuple((row["tranche"], row["row_count"]) for row in members["tranches"])
        == MEMBER_TRANCHES,
        "member tranches",
    )
    need(sum(row["row_count"] for row in members["tranches"]) == MEMBER_COUNT, "member tranche total")
    need(
        members["missing_member_count_must_equal"]
        == members["orphan_member_count_must_equal"]
        == members["duplicate_member_count_must_equal"]
        == 0,
        "member zero defects",
    )
    need(
        members["outer_envelope_is_full_support"] is False
        and members["inner_witness_is_full_support"] is False
        and members["carrier_box_is_full_support"] is False,
        "support semantic separation",
    )
    need(members["four_R271_split_cells_mint_member_identities"] is False, "four split cells")

    reps = document["representation_cover_contract"]
    need(
        reps["primary_representation_count"] + reps["extra_representation_count"]
        == reps["representation_row_count"]
        == REPRESENTATION_COUNT
        == 611_904,
        "representation total",
    )
    need(
        reps["refined_primary_extra_count"] + reps["alias_representation_count"]
        == reps["extra_representation_count"]
        == 47_412,
        "extra representation total",
    )
    need(
        reps["R294_alias_count"] + reps["R295A_alias_count"]
        == reps["alias_representation_count"]
        == 46_564,
        "alias partition",
    )
    need(
        tuple((row["tranche"], row["row_count"]) for row in reps["coordinate_tranches"])
        == REPRESENTATION_TRANCHES,
        "representation tranches",
    )
    need(sum(row["row_count"] for row in reps["coordinate_tranches"]) == REPRESENTATION_COUNT, "coordinate tranche total")
    need(reps["representation_mints_member_identity"] is False, "representation no identity")

    feature_schema = document["feature_definition_row_schema"]
    need(tuple(feature_schema["allowed_ast_operators"]) == AST_OPERATORS, "AST operators")
    need(tuple(feature_schema["allowed_proof_kernels"]) == PROOF_KERNELS, "proof kernels")
    need(feature_schema["root_ast_is_independently_evaluable"] is True, "evaluable roots")
    need(feature_schema["source_filename_or_row_id_alone_is_definition"] is False, "no source label definition")
    need(feature_schema["proof_method_label_alone_is_definition"] is False, "no method label definition")

    graph = document["graph_and_incidence_semantics"]
    need(graph["source_free_graph_definition_count"] == 38_624, "graph definitions")
    need(
        graph["graph_sheet_identification_count"]
        + graph["graph_side_incidence_reference_count"]
        == graph["physical_incidence_count"]
        == 115_472,
        "physical incidence total",
    )
    need(
        graph["graph_side_incidence_reference_count"] == 76_848
        and graph["B1A_distinct_graph_side_positive_3D_carrier_count"] == 76_304
        and graph["graph_side_reference_count_equals_carrier_count"] is False,
        "side reference carrier distinction",
    )
    need(graph["Round264_empty_bulk_may_be_revived"] is False, "Round264 empty bulk")
    need(graph["graph_sheet_identification_is_adjacency"] is False, "sheet identification nonadjacency")

    wire = document["ledger_wire_contract"]
    need(tuple(wire["candidate_filenames_in_order"]) == CANDIDATE_ORDER, "candidate order")
    need(wire["feature_definition_filename"] == FILES["feature"], "feature filename")
    need(wire["source_closure_filename"] is None, "no source closure filename")
    need(wire["feature_definition_is_explicit_B2_consumable_ledger"] is True, "B2 consumable ledger")
    need(all(wire[key] is True for key in (
        "strict_JSON_duplicate_keys_rejected",
        "strict_JSON_nonfinite_numbers_rejected",
        "strict_JSON_trailing_bytes_rejected",
        "canonical_single_member_gzip_required",
        "gzip_second_member_rejected",
        "gzip_trailing_bytes_rejected",
        "exact_decompressed_wire_size_required",
        "bounded_row_token_required",
    )), "wire defenses")

    gaps = document["gap_row_schema"]
    need(gaps["formal_PASS_gap_row_count_must_equal"] == 0, "zero formal gaps")
    need(gaps["gap_may_be_forced_to_PASS"] is False, "no forced gap pass")

    publication = document["publication_contract"]
    need(publication["private_candidate_file_count"] == 5, "candidate file count")
    need(tuple(publication["private_candidate_files"]) == CANDIDATE_ORDER, "candidate files")
    need(publication["formal_manifest_member_count"] == 11, "manifest member count")
    need(tuple(publication["formal_manifest_members"]) == FORMAL_PACKAGE_MEMBERS, "formal members")
    need(publication["sealed_package_file_count_including_manifest"] == 12, "sealed package count")
    need(publication["verifier_may_import_execute_or_parse_producer"] is False, "verifier independence")
    need(publication["attack_first"] is True and publication["verification_last"] is True, "transaction order")
    need(publication["formal_manifest_is_verification_last"] is True, "manifest verification last")

    gates = document["future_formal_PASS_gates"]
    need(gates["feature_definition_rows_must_equal"] == 824_864, "feature gate")
    need(gates["independent_root_rows_must_equal"] == 351_904, "root gate")
    need(gates["dependent_rows_must_equal"] == 472_960, "dependent gate")
    need(gates["member_cover_rows_must_equal"] == 564_492, "member gate")
    need(gates["representation_rows_must_equal"] == 611_904, "representation gate")
    need(gates["gap_rows_must_equal"] == 0, "gap gate")
    need(gates["transition_atlas_complete"] is False, "transition remains downstream")
    need(gates["pair_routing_complete"] is False, "pair routing remains downstream")
    need(gates["PASS_currently_permitted"] is False, "current PASS blocked")

    credit = document["formal_credit"]
    for key, value in credit.items():
        if key.startswith("current_"):
            need(value == 0, "zero current credit:" + key)
    need(credit["D02"] == "BLOCKED", "D02")
    need(credit["CM2"] == "NO-GO_FOR_CLAIM", "CM2")
    need(
        document["emission_accounting"]
        == {
            "large_sources_opened": 0,
            "feature_rows_emitted": 0,
            "member_rows_emitted": 0,
            "representation_rows_emitted": 0,
            "gap_rows_emitted": 0,
            "candidate_files_written": 0,
            "formal_files_written": 0,
        },
        "zero emission accounting",
    )


def contract() -> dict[str, Any]:
    document = _contract_document()
    validate_contract(document)
    return document


def file_sha256(path: Path, expected_size: int) -> str:
    before = os.lstat(path)
    need(stat.S_ISREG(before.st_mode) and not path.is_symlink(), "regular dependency:" + path.name)
    need(before.st_nlink == 1, "dependency link count:" + path.name)
    need(before.st_size == expected_size, "dependency exact size:" + path.name)
    descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
    try:
        opened = os.fstat(descriptor)
        need(
            (opened.st_dev, opened.st_ino, opened.st_size, opened.st_mtime_ns)
            == (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns),
            "dependency stable open:" + path.name,
        )
        state = hashlib.sha256()
        total = 0
        while True:
            block = os.read(descriptor, 1 << 20)
            if not block:
                break
            total += len(block)
            need(total <= expected_size, "dependency bounded read:" + path.name)
            state.update(block)
        after = os.fstat(descriptor)
        need(total == expected_size, "dependency complete read:" + path.name)
        need(
            (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns)
            == (opened.st_dev, opened.st_ino, opened.st_size, opened.st_mtime_ns),
            "dependency stable read:" + path.name,
        )
        return state.hexdigest()
    finally:
        os.close(descriptor)


def discover_data(source: Path) -> Path:
    resolved = source.resolve()
    for ancestor in (resolved.parent, *resolved.parents):
        if ancestor.name == "deliverables" and ancestor.is_dir():
            return ancestor
        candidate = ancestor / "deliverables"
        if candidate.is_dir():
            return candidate
    raise ContractBlocked("deliverables root not found")


def verify_dependencies() -> dict[str, Any]:
    data = discover_data(Path(__file__))
    checked: list[dict[str, Any]] = []
    total_bytes = 0
    for round_id, filename, size, expected_sha, role in DEPENDENCY_PINS:
        actual_sha = file_sha256(data / filename, size)
        need(actual_sha == expected_sha, "dependency byte pin:" + filename)
        checked.append({
            "round": round_id,
            "filename": filename,
            "exact_size": size,
            "file_sha256": actual_sha,
            "role": role,
        })
        total_bytes += size
    result = {
        "schema": SCHEMA + ".dependency-verification.v1",
        "status": "PASS_ROUND306B1AF0_EXACT_DEPENDENCY_BYTE_PINS",
        "checked_file_count": len(checked),
        "checked_byte_count": total_bytes,
        "checked_rows_sha256": digest(checked),
        "candidate_or_formal_files_written": 0,
    }
    return {**result, "verification_sha256": digest(result)}


def build_private_candidate(_candidate: Path) -> NoReturn:
    raise ContractBlocked(CANDIDATE_BLOCK_REASON)


def _mutation_suite() -> tuple[int, int]:
    base = _contract_document()
    attacks: list[Callable[[dict[str, Any]], None]] = [
        lambda d: d.__setitem__("status", "PASS"),
        lambda d: d.__setitem__("candidate_is_formal", True),
        lambda d: d["candidate_mode"].__setitem__("enabled", True),
        lambda d: d["candidate_mode"].__setitem__("block_before_path_lstat", False),
        lambda d: d["scope_resolution"].__setitem__("transition_atlas_is_candidate_precondition", True),
        lambda d: d["scope_resolution"].__setitem__("complete_transition_atlas_claimed_by_B1A", True),
        lambda d: d["dependency_pins"][0].__setitem__("file_sha256", "0" * 64),
        lambda d: d["dependency_pins"][0].__setitem__("exact_size", 1),
        lambda d: d["dependency_object_pins"].__setitem__("Round306B0_result_sha256", "0" * 64),
        lambda d: d["typed_feature_DAG"].__setitem__("node_order", list(reversed(NODE_ORDER))),
        lambda d: d["typed_feature_DAG"]["root_families"][0].__setitem__("row_count", 225),
        lambda d: d["typed_feature_DAG"]["dependent_families"][0].__setitem__("row_count", 505),
        lambda d: d["typed_feature_DAG"]["dependent_families"][0].__setitem__("flattened_as_independent_root", True),
        lambda d: d["typed_feature_DAG"].__setitem__("feature_definition_ledger_row_count", 824_863),
        lambda d: d["typed_feature_DAG"].__setitem__("B2_ledger_name", "source_closure"),
        lambda d: d["member_cover_contract"].__setitem__("member_count", 564_493),
        lambda d: d["member_cover_contract"].__setitem__("outer_envelope_is_full_support", True),
        lambda d: d["member_cover_contract"].__setitem__("inner_witness_is_full_support", True),
        lambda d: d["member_cover_contract"].__setitem__("four_R271_split_cells_mint_member_identities", True),
        lambda d: d["representation_cover_contract"].__setitem__("representation_row_count", 611_903),
        lambda d: d["representation_cover_contract"].__setitem__("representation_mints_member_identity", True),
        lambda d: d["feature_definition_row_schema"].__setitem__("allowed_ast_operators", ["LABEL_ONLY"]),
        lambda d: d["feature_definition_row_schema"].__setitem__("root_ast_is_independently_evaluable", False),
        lambda d: d["feature_definition_row_schema"].__setitem__("source_filename_or_row_id_alone_is_definition", True),
        lambda d: d["graph_and_incidence_semantics"].__setitem__("physical_incidence_count", 115_471),
        lambda d: d["graph_and_incidence_semantics"].__setitem__("graph_side_reference_count_equals_carrier_count", True),
        lambda d: d["graph_and_incidence_semantics"].__setitem__("Round264_empty_bulk_may_be_revived", True),
        lambda d: d["graph_and_incidence_semantics"].__setitem__("graph_sheet_identification_is_adjacency", True),
        lambda d: d["ledger_wire_contract"].__setitem__("source_closure_filename", "legacy.json.gz"),
        lambda d: d["ledger_wire_contract"].__setitem__("gzip_second_member_rejected", False),
        lambda d: d["gap_row_schema"].__setitem__("formal_PASS_gap_row_count_must_equal", 1),
        lambda d: d["gap_row_schema"].__setitem__("gap_may_be_forced_to_PASS", True),
        lambda d: d["publication_contract"].__setitem__("private_candidate_file_count", 4),
        lambda d: d["publication_contract"].__setitem__("verifier_may_import_execute_or_parse_producer", True),
        lambda d: d["publication_contract"].__setitem__("attack_first", False),
        lambda d: d["publication_contract"].__setitem__("formal_manifest_is_verification_last", False),
        lambda d: d["future_formal_PASS_gates"].__setitem__("gap_rows_must_equal", 1),
        lambda d: d["future_formal_PASS_gates"].__setitem__("transition_atlas_complete", True),
        lambda d: d["future_formal_PASS_gates"].__setitem__("PASS_currently_permitted", True),
        lambda d: d["formal_credit"].__setitem__("current_feature_definition", 1),
        lambda d: d["formal_credit"].__setitem__("D02", "PASS"),
        lambda d: d["emission_accounting"].__setitem__("feature_rows_emitted", 1),
    ]
    rejected = 0
    for attack in attacks:
        mutated = deepcopy(base)
        attack(mutated)
        try:
            validate_contract(mutated)
        except ContractBlocked:
            rejected += 1
    return rejected, len(attacks)


def _candidate_boundary_probe() -> dict[str, Any]:
    calls = {"lstat": 0, "open": 0, "temp": 0, "write": 0}

    def touched(name: str) -> Callable[..., Any]:
        def inner(*_args: Any, **_kwargs: Any) -> Any:
            calls[name] += 1
            raise AssertionError("filesystem boundary crossed:" + name)
        return inner

    with (
        mock.patch.object(os, "lstat", side_effect=touched("lstat")),
        mock.patch.object(os, "open", side_effect=touched("open")),
        mock.patch.object(tempfile, "TemporaryFile", side_effect=touched("temp")),
        mock.patch.object(tempfile, "NamedTemporaryFile", side_effect=touched("temp")),
        mock.patch.object(builtins, "open", side_effect=touched("write")),
    ):
        blocked = False
        try:
            build_private_candidate(Path("/forbidden"))
        except ContractBlocked as error:
            blocked = str(error) == CANDIDATE_BLOCK_REASON
    need(blocked, "candidate block reason")
    need(calls == {"lstat": 0, "open": 0, "temp": 0, "write": 0}, "pre-filesystem block")
    return {"blocked": blocked, **calls}


def self_test() -> dict[str, Any]:
    document = contract()
    rejected, total = _mutation_suite()
    need(rejected == total == 42, "all semantic mutations rejected")
    boundary = _candidate_boundary_probe()
    summary = {
        "schema": SCHEMA + ".self-test.v1",
        "status": "PASS_ROUND306B1AF0_LIGHTWEIGHT_SCHEMA_AND_BOUNDARY_SELF_TEST",
        "contract_sha256": digest(document),
        "semantic_mutations_rejected": rejected,
        "semantic_mutation_count": total,
        "candidate_boundary_probe": boundary,
        "dependency_files_opened": 0,
        "candidate_or_formal_files_written": 0,
        "formal_credit": 0,
        "D02": "BLOCKED",
        "CM2": "NO-GO_FOR_CLAIM",
    }
    return {**summary, "self_test_sha256": digest(summary)}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--print-contract", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--verify-dependencies", action="store_true")
    parser.add_argument("--candidate-dir", type=Path)
    args = parser.parse_args()
    need(
        sum((
            args.print_contract,
            args.self_test,
            args.verify_dependencies,
            args.candidate_dir is not None,
        )) == 1,
        "choose exactly one mode",
    )
    if args.print_contract:
        print(canonical(contract()))
    elif args.self_test:
        print(canonical(self_test()))
    elif args.verify_dependencies:
        print(canonical(verify_dependencies()))
    else:
        assert args.candidate_dir is not None
        print(canonical(build_private_candidate(args.candidate_dir)))


if __name__ == "__main__":
    main()
