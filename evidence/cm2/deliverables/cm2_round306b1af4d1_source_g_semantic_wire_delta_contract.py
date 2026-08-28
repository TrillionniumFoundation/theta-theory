#!/usr/bin/env python3
"""Round306B1AF4D1 Source-G semantic/wire delta contract.

This is a sealed, versioned, zero-credit overlay on the final AF3D1 authority
delta, the AF4 symbolic kernel, and the final AF4 typed schema.  It freezes the
minimum additional semantics and wire shapes required before a future Source-G
constructor may attempt formal normalized-support output.  In particular it
does not confuse a sealed specification with a discharged theorem: every
currently unavailable mathematical or source-authority premise remains an
explicit hard obligation.

Normal contract printing and self-test are filesystem inert.  The only mode
that reads dependencies is ``--verify-dependencies``; it hashes exactly three
pinned source files twice through held descriptors under a held directory fd.
Candidate and production modes fail before path inspection, input open,
temporary creation, write, or output.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import tempfile
from typing import Any, Callable, Final
from unittest import mock


class ContractBlocked(RuntimeError):
    """Fail-closed AF4D1 contract, dependency, or mode violation."""


def need(condition: bool, label: str) -> None:
    if not condition:
        raise ContractBlocked(label)


SCHEMA: Final = "cm2.round306b1af4d1.source-g-semantic-wire-delta-contract.v1"
STATUS: Final = (
    "PASS_SEALED_ZERO_CREDIT_SEMANTIC_WIRE_DELTA__"
    "FORMAL_CONSTRUCTOR_STILL_BLOCKED_ON_EXPLICIT_THEOREM_OBLIGATIONS"
)
CANDIDATE_BLOCK_REASON: Final = (
    "Round306B1AF4D1 is a sealed non-producing zero-credit semantic/wire "
    "delta; candidate and production modes are blocked before all filesystem "
    "and output boundaries"
)

DEPENDENCY_DIRECTORY: Final = Path(__file__).parent
DEPENDENCY_PINS: Final = (
    {
        "label": "Round306B1AF3D1_FINAL",
        "filename": "cm2_round306b1af3d1_source_g_support_representation_authority_delta_contract.py",
        "exact_size": 57_389,
        "source_sha256": "d61fbdc7e6d917c9c451cf63a7640285e900fd08dff76800119ca60ae5e55138",
    },
    {
        "label": "Round306B1AF4_SYMBOLIC_KERNEL_FINAL",
        "filename": "cm2_round306b1af4_source_g_normalized_support_symbolic_kernel.py",
        "exact_size": 87_237,
        "source_sha256": "c8bb9cf85aace782639859c33625732bf866a7fad34ff31cce58ab84af9f6a6f",
    },
    {
        "label": "Round306B1AF4_TYPED_SCHEMA_FINAL",
        "filename": "cm2_round306b1af4_source_g_normalized_support_representation_typed_schema_contract.py",
        "exact_size": 80_436,
        "source_sha256": "ee095fe5db22c6a4dd0804eca0fb553a132546367dcb37fcd75733050aa52cf9",
    },
)

DELTA_ITEMS: Final = ("B", "C", "D", "E", "F", "G", "H")
DELTA_OPERATOR_IDS: Final = (
    "LE_ZERO",
    "GE_ZERO",
    "RELATIVE_CLOSURE_TRACE",
)
DELTA_WIRE_IDS: Final = (
    "RATIONAL_INTERVAL_BOX_V1",
    "TWO_FACTOR_ARRANGEMENT_V1",
    "SOURCE_G_FORMULA_FRAME_V1",
    "CHART_MAP_AST_V1",
    "PROOF_BUNDLE_DAG_V1",
)
DELTA_KERNEL_IDS: Final = (
    "REGULAR_LEVELSET_ONE_SIDED_TRACE_V1",
    "CODIM2_INTERSECTION_DISPOSITION_V1",
    "VIRTUAL_MEMBER_FULL_SUPPORT_EQUIVALENCE_V1",
    "MIXED_BOUNDARY_FACE_PARTITION_V1",
    "CHART_MAP_BIJECTION_V1",
    "PROOF_BUNDLE_DAG_VALIDATION_V1",
    "PARTIAL_REPRESENTATION_INCLUSION_V1",
    "MEMBER_REPRESENTATION_UNION_COVER_V1",
)

G2_GRAPH_ROOT_COUNT: Final = 38_624
G2A_MEMBER_COUNT: Final = 38_624
G2B_REFERENCE_COUNT: Final = 76_848
G2B_MEMBER_COUNT: Final = 76_832
G2_MEMBER_COUNT: Final = 115_456
R236_PARTITION_COUNT: Final = 16
R245_NODE_COUNT: Final = 3_664
R245_MIXED_EDGE_COUNT: Final = 3_664
R264_CORRECTION_COUNT: Final = 400

HEX64: Final = re.compile(r"^[0-9a-f]{64}$")


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=True,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def _dependency_contract() -> dict[str, Any]:
    return {
        "seal_state": "SEALED_EXACT_THREE_FINAL_SOURCE_BYTES",
        "dependency_sources": [dict(row) for row in DEPENDENCY_PINS],
        "dependency_source_count": 3,
        "dependency_source_set_sha256": digest(DEPENDENCY_PINS),
        "raw_bytes_only": True,
        "dependency_imported": False,
        "dependency_executed": False,
        "dependency_parsed": False,
        "held_directory_fd_required": True,
        "O_NOFOLLOW_required": True,
        "regular_file_and_nlink_one_required": True,
        "two_pass_same_fd_SHA256_required": True,
        "pre_post_fstat_required": True,
        "path_replacement_fail_closed": True,
    }


def _trace_overlay() -> dict[str, Any]:
    return {
        "delta_item": "B",
        "problem": "POINTWISE_RESTRICTION_OF_A_STRICT_SIDE_TO_ITS_ZERO_BOUNDARY_IS_EMPTY",
        "old_AF4_lowering": "RESTRICT(side_support_ast,boundary_support_ast)",
        "old_pointwise_trace_is_forbidden": True,
        "old_lowering_may_mint_physical_incidence": False,
        "canonical_operator": {
            "operator_id": "RELATIVE_CLOSURE_TRACE",
            "wire_type": "TraceExpr<C>",
            "exact_fields": [
                "op",
                "ambient_domain_ast",
                "side_support_ast",
                "boundary_support_ast",
                "defining_factor_ast",
                "side_sign",
                "graph_variable",
            ],
            "side_sign_values": [-1, 1],
            "denotation": "RELATIVE_CLOSURE_IN_AMBIENT(side_support_ast,ambient_domain_ast) INTERSECT boundary_support_ast",
            "not_lowered_to_pointwise_RESTRICT": True,
            "canonicalization": [
                "NORMALIZE_EACH_NESTED_AF4_AST",
                "REJECT_FIELDS_NOT_IN_EXACT_FIELD_SET",
                "PRESERVE_ORIENTATION_SIGN",
                "HASH_CANONICAL_JSON",
            ],
        },
        "canonical_support_forms": {
            "positive_side": "AND(ambient_domain_ast,GT_ZERO(defining_factor_ast))",
            "negative_side": "AND(ambient_domain_ast,LT_ZERO(defining_factor_ast))",
            "boundary": "AND(boundary_domain_ast,EQ_ZERO(defining_factor_ast))",
            "graph": "AND(graph_domain_ast,EQ_ZERO(defining_factor_ast))",
        },
        "kernel": {
            "kernel_id": "REGULAR_LEVELSET_ONE_SIDED_TRACE_V1",
            "premises": {
                "ambient_domain_ast": "PREDICATE_AST",
                "boundary_support_ast": "PREDICATE_AST",
                "defining_factor_ast": "SCALAR_AST",
                "derivative_ast": "SCALAR_AST",
                "graph_support_ast": "PREDICATE_AST",
                "graph_variable": "STR",
                "side_sign": "SIGMA",
                "side_support_ast": "PREDICATE_AST",
                "trace_expr": "RELATIVE_CLOSURE_TRACE_AST",
            },
            "evidence": {
                "base_cell_ids": "NONEMPTY_STR_LIST",
                "continuity_claim_id": "STR",
                "derivative_sign_claim_ids": "NONEMPTY_STR_LIST",
                "monotone_graph_claim_id": "STR",
                "outer_face_assignment_claim_id": "STR",
                "root_face_sign_claim_ids": "NONEMPTY_STR_LIST",
            },
            "conclusion": {
                "closure_trace_ast": "PREDICATE_AST",
                "exact_physical_incidence_claim": "BOOL_TRUE",
                "trace_equals_boundary_claim": "BOOL_TRUE",
            },
        },
        "independent_validation_algorithm": [
            "RECONSTRUCT_SIDE_AS_AMBIENT_AND_REQUESTED_STRICT_SIGN",
            "RECONSTRUCT_BOUNDARY_AS_DOMAIN_AND_FACTOR_EQUAL_ZERO",
            "VERIFY_CONTINUITY_ON_EVERY_CLOSED_PROOF_CELL",
            "VERIFY_ONE_UNIQUE_INTERIOR_ROOT_PER_BASE_POINT",
            "VERIFY_DERIVATIVE_HAS_ONE_STRICT_NONZERO_SIGN_ON_EVERY_CELL",
            "VERIFY_T_FACE_SIGNS_AND_ALL_OUTER_FACE_OWNERS",
            "USE_MEAN_VALUE_THEOREM_TO_FIX_THE_APPROACH_ORIENTATION",
            "PROVE_BOUNDARY_SUBSET_RELATIVE_CLOSURE_BY_ONE_SIDED_APPROACH",
            "PROVE_RELATIVE_CLOSURE_INTERSECT_BOUNDARY_SUBSET_BOUNDARY_BY_CONTINUITY",
            "REQUIRE_BOTH_INCLUSIONS_BEFORE_PHYSICAL_INCIDENCE_TRUE",
        ],
        "mathematical_rule": {
            "hypotheses": "FOR_EACH_BASE_POINT_UNIQUE_ROOT_t0_AND_CONTINUOUS_f_AND_FIXED_NONZERO_dfdT",
            "approach_sign": "sign(f(t0+delta))=sign(dfdT)*sign(delta)_FOR_SUFFICIENTLY_SMALL_NONZERO_delta",
            "forward_inclusion": "EVERY_BOUNDARY_ROOT_IS_A_LIMIT_OF_THE_SELECTED_STRICT_SIDE",
            "reverse_inclusion": "CONTINUITY_FORCES_ANY_BOUNDARY_LIMIT_TO_REMAIN_ON_f_EQUALS_ZERO",
            "result": "RELATIVE_CLOSURE_TRACE_EQUALS_THE_BOUNDARY_GRAPH",
        },
        "current_status": "HARD_THEOREM_OBLIGATION",
        "current_obligation_count": G2B_REFERENCE_COUNT,
        "formal_credit": 0,
    }


def _codim2_overlay() -> dict[str, Any]:
    return {
        "delta_item": "C",
        "family": "R236_DOUBLE_ENDPOINT_GRAPH",
        "partition_count": R236_PARTITION_COUNT,
        "all_partitions_are_hard_obligations": True,
        "canonical_arrangement": {
            "wire_id": "TWO_FACTOR_ARRANGEMENT_V1",
            "exact_fields": [
                "wire_id",
                "domain_ast",
                "source_factor_ast",
                "target_factor_ast",
                "C_MINUS_MINUS",
                "C_MINUS_PLUS",
                "C_PLUS_MINUS",
                "C_PLUS_PLUS",
                "Z_SOURCE",
                "Z_TARGET",
                "Z_SOURCE_TARGET",
                "SAME_SIGN_SUPPORT",
                "NEGATIVE_TO_POSITIVE_SUPPORT",
                "POSITIVE_TO_NEGATIVE_SUPPORT",
            ],
            "lowerings": {
                "C_MINUS_MINUS": "AND(D,LT_ZERO(fs),LT_ZERO(ft))",
                "C_MINUS_PLUS": "AND(D,LT_ZERO(fs),GT_ZERO(ft))",
                "C_PLUS_MINUS": "AND(D,GT_ZERO(fs),LT_ZERO(ft))",
                "C_PLUS_PLUS": "AND(D,GT_ZERO(fs),GT_ZERO(ft))",
                "Z_SOURCE": "AND(D,EQ_ZERO(fs))",
                "Z_TARGET": "AND(D,EQ_ZERO(ft))",
                "Z_SOURCE_TARGET": "AND(D,EQ_ZERO(fs),EQ_ZERO(ft))",
                "SAME_SIGN_SUPPORT": "OR_DISJOINT(C_MINUS_MINUS,C_PLUS_PLUS)",
                "NEGATIVE_TO_POSITIVE_SUPPORT": "C_MINUS_PLUS",
                "POSITIVE_TO_NEGATIVE_SUPPORT": "C_PLUS_MINUS",
            },
            "Z_SOURCE_TARGET_may_not_be_erased": True,
            "four_strict_cells_do_not_cover_Z_SOURCE_TARGET": True,
        },
        "kernel": {
            "kernel_id": "CODIM2_INTERSECTION_DISPOSITION_V1",
            "premises": {
                "domain_ast": "PREDICATE_AST",
                "intersection_ast": "PREDICATE_AST",
                "source_factor_ast": "SCALAR_AST",
                "source_partition_id": "STR",
                "target_factor_ast": "SCALAR_AST",
            },
            "evidence_variants": {
                "EMPTY": {
                    "cover_cell_ids": "NONEMPTY_STR_LIST",
                    "cover_disjoint_exhaustive_claim_id": "STR",
                    "per_cell_zero_exclusion_claim_ids": "NONEMPTY_STR_LIST",
                    "rule": "ON_EVERY_COVER_CELL_AT_LEAST_ONE_FACTOR_INTERVAL_EXCLUDES_ZERO",
                },
                "MATERIALIZED_REGULAR": {
                    "codim2_feature_row_id": "STR",
                    "cover_cell_ids": "NONEMPTY_STR_LIST",
                    "half_open_owner_claim_id": "STR",
                    "jacobian_rank_two_claim_ids": "NONEMPTY_STR_LIST",
                    "nonempty_witness_claim_ids": "NONEMPTY_STR_LIST",
                },
                "BLOCKED_SINGULAR": {
                    "blocking_cell_ids": "NONEMPTY_STR_LIST",
                    "reason": "STR",
                },
            },
            "conclusion_variants": {
                "EMPTY": {"intersection_empty_claim": "BOOL_TRUE"},
                "MATERIALIZED_REGULAR": {
                    "intersection_materialized_claim": "BOOL_TRUE",
                    "materialized_support_ast": "PREDICATE_AST",
                },
                "BLOCKED_SINGULAR": {"formal_credit": "ZERO"},
            },
            "default_disposition_forbidden": True,
        },
        "independent_validation_algorithm": [
            "REBUILD_fs_ft_AND_THE_EXACT_R234_DOMAIN",
            "REBUILD_ALL_FOUR_STRICT_CELLS_AND_BOTH_ZERO_SHEETS",
            "REBUILD_Z_SOURCE_TARGET_WITH_CONJUNCTION_NOT_UNION",
            "FOR_EMPTY_REQUIRE_A_DISJOINT_EXHAUSTIVE_FINITE_DOMAIN_COVER",
            "FOR_EACH_EMPTY_COVER_CELL_RECOMPUTE_AN_OUTWARD_INTERVAL_ZERO_EXCLUSION",
            "FOR_MATERIALIZED_REQUIRE_EXACT_SUPPORT_NONEMPTINESS_RANK_AND_FACE_OWNER",
            "BLOCK_SINGULAR_OR_UNCOVERED_CELLS",
        ],
        "existing_authority_supplies_disposition": False,
        "existing_13_kernel_set_can_discharge_disposition": False,
        "current_status": "16_OF_16_HARD_THEOREM_OBLIGATIONS_UNRESOLVED",
        "formal_credit": 0,
    }


def _representation_semantics_overlay() -> dict[str, Any]:
    """Resolve the AF4 whole-equality/partial-alias wire conflict."""

    return {
        "AF4_conflict": (
            "AF4_REQUIRES_EVERY_REPRESENTATION_ROW_TO_HAVE_FULL_PULLBACK_SET_EQUALITY_"
            "BUT_PINNED_ALIAS_AND_REFINED_ROWS_INCLUDE_STRICT_SUBCOVERS_OR_INCLUSIONS"
        ),
        "per_representation_coverage_semantics_field": {
            "field": "coverage_semantics",
            "exact_values": ["FULL_SET_EQUALITY", "PARTIAL_INCLUSION"],
            "member_cover_group_id_required_for_partial": True,
            "a_partial_row_may_satisfy_full_set_equality": False,
            "a_partial_row_may_mint_member_identity": False,
        },
        "partial_inclusion_kernel": {
            "kernel_id": "PARTIAL_REPRESENTATION_INCLUSION_V1",
            "premises": {
                "chart_map_ast": "CHART_MAP_AST_V1",
                "member_full_support_ast": "PREDICATE_AST",
                "representation_role": "STR",
                "representation_support_ast": "PREDICATE_AST",
                "representation_row_id": "STR",
            },
            "evidence": {
                "forward_inclusion_claim_ids": "NONEMPTY_STR_LIST",
                "nonempty_claim_ids": "NONEMPTY_STR_LIST",
                "owner_member_row_id": "STR",
                "source_binding_row_ids": "NONEMPTY_STR_LIST",
            },
            "conclusion": {
                "mints_member_identity_claim": "BOOL_FALSE",
                "representation_subset_member_claim": "BOOL_TRUE",
                "whole_support_equality_claim": "BOOL_FALSE",
            },
        },
        "member_union_cover_kernel": {
            "kernel_id": "MEMBER_REPRESENTATION_UNION_COVER_V1",
            "premises": {
                "member_full_support_ast": "PREDICATE_AST",
                "member_row_id": "STR",
                "representation_row_ids": "NONEMPTY_STR_LIST",
                "representation_support_asts": "NONEMPTY_PREDICATE_LIST",
            },
            "evidence": {
                "forward_union_inclusion_claim_ids": "NONEMPTY_STR_LIST",
                "owner_anti_join_digest_sha256": "SHA256",
                "reverse_union_inclusion_claim_ids": "NONEMPTY_STR_LIST",
                "source_exhaustion_claim_id": "STR",
            },
            "conclusion": {
                "all_representations_have_one_owner_claim": "BOOL_TRUE",
                "member_equals_representation_union_claim": "BOOL_TRUE",
                "missing_or_orphan_representation_count": "ZERO",
            },
        },
        "known_partial_representation_classes": {
            "PRESERVED_TPS_INCLUSION": 720,
            "PRESERVED_T2PS_SUBCOVER": 1_600,
            "R2_TPS_INCLUSION": 7_288,
            "R295A_ADJACENT_CONTINUATION": 276,
            "R292_REFINED_PRIMARY_EXTRA": 848,
        },
        "known_alias_partial_count": 9_884,
        "known_alias_partial_count_equation": "720+1600+7288+276=9884",
        "known_refined_primary_extra_partial_count": 848,
        "role_specific_semantics": {
            "PRIMARY": {
                "singleton_member": "FULL_SET_EQUALITY",
                "multicell_member": "PARTIAL_INCLUSION_UNLESS_A_SEPARATE_WHOLE_CHART_IS_PROVED",
            },
            "REFINED_PRIMARY_EXTRA": "PARTIAL_INCLUSION_MEMBER_COVER_PART",
            "ALIAS_EXISTING_MEMBER": "SOURCE_CLASS_MUST_DECLARE_FULL_EQUALITY_OR_PARTIAL_INCLUSION",
        },
        "anti_join_rules": [
            "KNOWN_PARTIAL_SOURCE_ID_CLASSES_ARE_PAIRWISE_DISJOINT",
            "EVERY_PARTIAL_REPRESENTATION_HAS_EXACTLY_ONE_EXISTING_MEMBER_OWNER",
            "EVERY_PARTIAL_REPRESENTATION_OCCURS_IN_EXACTLY_ONE_MEMBER_COVER_GROUP",
            "NO_PARTIAL_REPRESENTATION_IS_ACCEPTED_AS_WHOLE_MEMBER_SUPPORT",
            "NO_ALIAS_OR_REFINED_EXTRA_MINTS_MEMBER_IDENTITY",
            "EVERY_MEMBER_COVER_GROUP_HAS_ZERO_MISSING_OR_ORPHAN_REPRESENTATIONS",
        ],
        "TPS_inter_chart_canonical_bijection_available": False,
        "TPS_inter_chart_canonical_bijection_status": "HARD_CHART_MAP_THEOREM_OBLIGATION",
        "R2_four_face_reglue": {
            "source_cell_count": 295_340,
            "member_count": 295_336,
            "two_cell_member_count": 4,
            "artificial_face_reglue_obligation_count": 4,
            "count_equation": "295332_singletons+4_two_cell_members=295336_members_AND_295332+4*2=295340_cells",
            "canonical_reglue_key": [
                "B0_member_id",
                "physical_face_ast_sha256",
                "min_source_cell_id",
                "max_source_cell_id",
            ],
            "all_four_faces_require_bidirectional_trace_and_single_owner": True,
        },
        "R292_canonical_Kruskal": {
            "input_cell_count": 10_252,
            "output_component_count": 9_404,
            "accepted_face_count": 848,
            "count_equation": "10252-848=9404",
            "candidate_face_order": [
                "canonical_physical_face_id_ASCII",
                "min_endpoint_cell_id_ASCII",
                "max_endpoint_cell_id_ASCII",
                "source_face_row_id_ASCII",
            ],
            "only_physically_verified_faces_enter_edge_stream": True,
            "DSU_initial_order": "canonical_cell_id_unsigned_bytewise_ASCII",
            "union_root_rule": "minimum_canonical_cell_id",
            "accept_rule": "ACCEPT_IFF_CURRENT_ROOTS_DIFFER",
            "hash_seed_may_affect_order_or_result": False,
            "all_848_nonprimary_cells_are_REFINED_PRIMARY_EXTRA": True,
        },
        "current_status": "WIRE_RESOLUTION_FROZEN_BUT_INCLUSION_COVER_AND_INTERCHART_THEOREMS_UNDISCHARGED",
        "formal_credit": 0,
    }


def _full_support_overlay() -> dict[str, Any]:
    return {
        "delta_item": "D",
        "kernel": {
            "kernel_id": "VIRTUAL_MEMBER_FULL_SUPPORT_EQUIVALENCE_V1",
            "premises": {
                "B0_member_id": "STR",
                "branch_predicate_ast": "PREDICATE_AST",
                "candidate_full_support_ast": "PREDICATE_AST",
                "construction_domain_ast": "PREDICATE_AST",
                "source_family": "ENUM_R245_R248",
                "source_member_id": "STR",
                "source_semantic_support_ast": "PREDICATE_AST",
            },
            "evidence": {
                "B0_backbinding_row_id": "STR",
                "construction_row_ids": "NONEMPTY_STR_LIST",
                "forward_cell_claim_ids": "NONEMPTY_STR_LIST",
                "nonempty_claim_ids": "NONEMPTY_STR_LIST",
                "R264_disposition_id_or_null": "STR_OR_NULL",
                "reverse_cell_claim_ids": "NONEMPTY_STR_LIST",
            },
            "conclusion": {
                "full_support_claim": "BOOL_TRUE",
                "identity_preserved_claim": "BOOL_TRUE",
                "set_equality_claim": "BOOL_TRUE",
            },
        },
        "canonical_candidate_supports": {
            "R245_SHEET": "R242_DOMAIN_AND_EQ_ZERO(psi)",
            "R245_OWNER_BULK": "R242_DOMAIN_AND_GT_ZERO(psi)",
            "R245_SHADOW_BULK": "R242_DOMAIN_AND_LT_ZERO(psi)",
            "R248_R235_SHEET": "R234_DOMAIN_AND_EQ_ZERO(endpoint_factor)",
            "R248_R235_BULK": "R234_DOMAIN_AND_THE_UNSUPPRESSED_BRANCH_SIGN",
            "R248_R236_SHEET": "R234_DOMAIN_AND_EQ_ZERO(source_or_target_factor)",
            "R248_R236_BULK": "ONE_OF_THE_THREE_EXACT_TWO_FACTOR_BRANCH_SUPPORTS",
        },
        "exact_distinct_member_obligation_count": G2_MEMBER_COUNT,
        "fine_counts": {
            "R245_sheet": 264,
            "R245_side": 528,
            "R248_sheet": 38_360,
            "R248_side_distinct": 76_304,
        },
        "count_equation": "264+528+38360+76304=115456",
        "forbidden_substitutions": [
            "R245_STRICT_INNER_WITNESS_OR_CORRIDOR_AS_FULL_SUPPORT",
            "R245_EDGE_LABEL_OR_IDENTIFIER_ADJACENCY_AS_SET_EQUALITY",
            "R248_NULL_EXACT_POSITIVE_3D_BOX_AS_A_SUPPORT_DEFINITION",
            "R248_SYNTHETIC_OWNER_EDGE_ID_AS_PHYSICAL_INCIDENCE",
            "B1G0_IDENTITY_JOIN_AS_GEOMETRIC_EQUALITY",
            "OFFICIAL_KEY_OR_SIGNATURE_AS_SUPPORT_GEOMETRY",
        ],
        "R264_guardrail": {
            "correction_count": R264_CORRECTION_COUNT,
            "empty_EVENT_ABSENT": 184,
            "empty_EVENT_PRESENT": 216,
            "all_sheets_retained": R264_CORRECTION_COUNT,
            "suppressed_branch_member_or_edge_may_reappear": False,
        },
        "independent_validation_algorithm": [
            "RECONSTRUCT_THE_CANDIDATE_FROM_PINNED_DOMAIN_AND_FORMULA_BYTES",
            "REQUIRE_A_SEPARATE_NORMATIVE_SOURCE_SEMANTIC_SUPPORT_AST",
            "VERIFY_FORWARD_AND_REVERSE_CELL_INCLUSIONS_NOT_ONLY_NONEMPTY_WITNESSES",
            "VERIFY_NONEMPTY_EXACTLY_WHEN_A_B0_MEMBER_IS_RETAINED",
            "APPLY_EVERY_R264_CORRECTION_EXACTLY_ONCE_BEFORE_BACKBINDING",
            "VERIFY_ONE_SUPPORT_EQUALITY_PER_DISTINCT_MEMBER_NOT_PER_REFERENCE",
        ],
        "existing_authority_has_extensional_full_support_semantics": False,
        "representation_semantics_delta": _representation_semantics_overlay(),
        "current_status": "115456_HARD_SET_EQUALITY_OBLIGATIONS_UNRESOLVED",
        "formal_credit": 0,
    }


def _boundary_overlay() -> dict[str, Any]:
    return {
        "delta_item": "E",
        "new_predicate_operators": {
            "LE_ZERO": {
                "exact_fields": ["op", "arg"],
                "argument_type": "SCALAR_AST",
                "result_type": "PREDICATE_AST",
                "interval_truth": "TRUE_IFF_SCALAR_INTERVAL_UPPER_LE_ZERO",
            },
            "GE_ZERO": {
                "exact_fields": ["op", "arg"],
                "argument_type": "SCALAR_AST",
                "result_type": "PREDICATE_AST",
                "interval_truth": "TRUE_IFF_SCALAR_INTERVAL_LOWER_GE_ZERO",
            },
        },
        "interval_box_wire": {
            "wire_id": "RATIONAL_INTERVAL_BOX_V1",
            "exact_fields": ["wire_id", "coordinate_parameter", "axes"],
            "coordinate_parameter": "TPS",
            "axis_order": ["t", "p", "s"],
            "axis_exact_fields": [
                "axis",
                "lower",
                "lower_closed",
                "upper",
                "upper_closed",
            ],
            "lowering": {
                "lower_closed_true": "GE_ZERO(SUB(VAR(axis),CONST_Q(lower)))",
                "lower_closed_false": "GT_ZERO(SUB(VAR(axis),CONST_Q(lower)))",
                "upper_closed_true": "LE_ZERO(SUB(VAR(axis),CONST_Q(upper)))",
                "upper_closed_false": "LT_ZERO(SUB(VAR(axis),CONST_Q(upper)))",
            },
            "alternative_algebraically_equivalent_spellings_forbidden": True,
            "all_rationals_exact_and_reduced": True,
        },
        "kernel": {
            "kernel_id": "MIXED_BOUNDARY_FACE_PARTITION_V1",
            "premises": {
                "child_support_asts": "NONEMPTY_PREDICATE_LIST",
                "owner_member_id": "STR",
                "parent_box_ast": "PREDICATE_AST",
                "physical_face_ast": "PREDICATE_AST",
                "shadow_member_ids": "STR_LIST",
            },
            "evidence": {
                "exhaustive_face_cover_claim_ids": "NONEMPTY_STR_LIST",
                "pairwise_disjoint_claim_ids": "NONEMPTY_STR_LIST",
                "single_owner_claim_id": "STR",
                "source_face_rule_ids": "NONEMPTY_STR_LIST",
            },
            "conclusion": {
                "exhaustive_claim": "BOOL_TRUE",
                "no_duplicate_claim": "BOOL_TRUE",
                "single_owner_claim": "BOOL_TRUE",
            },
        },
        "independent_validation_algorithm": [
            "REJECT_AN_AXIS_NOT_IN_EXACT_TPS_ORDER",
            "LOWER_EACH_ENDPOINT_BIT_WITH_THE_UNIQUE_OPERATOR_RULE",
            "RECOMPUTE_ALL_CHILD_INTERSECTIONS_ON_EACH_PHYSICAL_FACE",
            "VERIFY_PAIRWISE_DISJOINTNESS_AND_EXHAUSTIVENESS",
            "VERIFY_EXACTLY_ONE_OWNER_FOR_EVERY_INCLUDED_FACE_POINT",
            "REJECT_MISSING_OR_DOUBLE_OWNED_OUTER_FACES",
        ],
        "strict_open_TPS_DOMAIN_is_sufficient_for_mixed_topology": False,
        "existing_sources_uniquely_freeze_all_outer_face_bits": False,
        "current_status": "HARD_SOURCE_AUTHORITY_AND_FACE_PARTITION_OBLIGATION",
        "formal_credit": 0,
    }


def _map_overlay() -> dict[str, Any]:
    formula_fields = [
        "center_x",
        "center_y",
        "delta",
        "h_minus",
        "h_plus",
        "hit_x",
        "hit_y",
        "normal_x",
        "normal_y",
        "psi",
        "q_x",
        "q_y",
        "radius",
        "rn",
        "rp",
        "sqrt_delta",
        "tangent_x",
        "tangent_y",
        "transverse_z",
        "v_x",
        "v_y",
    ]
    return {
        "delta_item": "F",
        "physical_target_binding": {
            "G": {
                "center": "(ix,iy)",
                "radius": {"numerator": 9, "denominator": 25},
            },
            "W": {
                "center": "(ix+1/2+s,iy+1/2)",
                "radius": {"numerator": 4, "denominator": 25},
            },
            "radius_is_selected_only_by_target_kind": True,
            "row_supplied_radius_must_equal_this_binding": True,
            "binary_float_or_unreduced_rational_forbidden": True,
        },
        "formula_frame": {
            "wire_id": "SOURCE_G_FORMULA_FRAME_V1",
            "wire_type": "NamedScalarBundle<TPS>",
            "exact_fields": [
                "wire_id",
                "source_coordinate_parameter",
                "chart",
                "target_kind",
                "target_parameters",
                "domain_ast",
                "scalar_fields",
            ],
            "scalar_field_order": formula_fields,
            "scalar_field_count": 21,
            "is_ChartMap": False,
            "is_invertible_representation_by_itself": False,
            "theorem_credit": 0,
        },
        "chart_map": {
            "wire_id": "CHART_MAP_AST_V1",
            "wire_type": "ChartMap<src,dst>",
            "exact_fields": [
                "wire_id",
                "source_coordinate_parameter",
                "target_coordinate_parameter",
                "target_coordinate_system",
                "source_variables",
                "target_variables",
                "domain_ast",
                "codomain_ast",
                "forward_components",
                "inverse_branches",
            ],
            "component_exact_fields": ["target_variable", "expression_ast"],
            "inverse_branch_exact_fields": [
                "branch_id",
                "branch_domain_ast",
                "source_components",
            ],
            "source_component_exact_fields": ["source_variable", "expression_ast"],
            "forward_component_order_equals_target_variable_order": True,
            "inverse_branch_order": "branch_id_ASCII_ASCENDING",
            "inverse_components_order_equals_source_variable_order": True,
            "nonempty_inverse_branch_set_required": True,
        },
        "kernel": {
            "kernel_id": "CHART_MAP_BIJECTION_V1",
            "premises": {
                "chart_map_ast": "CHART_MAP_AST_V1",
                "member_support_ast": "PREDICATE_AST",
                "representation_support_ast": "PREDICATE_AST",
            },
            "evidence": {
                "branch_cover_claim_ids": "NONEMPTY_STR_LIST",
                "branch_disjoint_claim_ids": "NONEMPTY_STR_LIST",
                "forward_after_inverse_claim_ids": "NONEMPTY_STR_LIST",
                "inverse_after_forward_claim_ids": "NONEMPTY_STR_LIST",
                "radical_domain_claim_ids": "STR_LIST",
            },
            "conclusion": {
                "domain_set_equality_claim": "BOOL_TRUE",
                "forward_inverse_identity_claim": "BOOL_TRUE",
                "inverse_forward_identity_claim": "BOOL_TRUE",
            },
        },
        "independent_validation_algorithm": [
            "BIND_G_RADIUS_TO_EXACT_9_OVER_25_AND_W_RADIUS_TO_EXACT_4_OVER_25",
            "REJECT_ANY_TARGET_KIND_CENTER_OR_RADIUS_MISMATCH",
            "TYPECHECK_SOURCE_AND_TARGET_COORDINATE_PARAMETERS_WITHOUT_ERASURE",
            "RECOMPUTE_EVERY_FORWARD_AND_INVERSE_COMPONENT_AST",
            "VERIFY_BRANCH_DOMAINS_PAIRWISE_DISJOINT_AND_EXHAUSTIVE",
            "SYMBOLICALLY_SUBSTITUTE_BOTH_COMPOSITIONS_ON_EVERY_BRANCH",
            "VERIFY_DOMAIN_AND_CODOMAIN_SET_EQUALITY",
            "REJECT_A_NAMED_SCALAR_BUNDLE_IN_FORWARD_CHART_MAP_AST",
        ],
        "current_first_hit_lowering_is_only_SOURCE_G_SCALAR_MAP": True,
        "current_sources_freeze_virtual_target_coordinates_and_inverse_branches": False,
        "G2_representation_obligation_count": G2_MEMBER_COUNT,
        "current_status": "HARD_COORDINATE_AUTHORITY_AND_BIJECTION_OBLIGATION",
        "formal_credit": 0,
    }


def _proof_bundle_overlay() -> dict[str, Any]:
    return {
        "delta_item": "G",
        "singular_proof_kernel_field_can_encode_a_composite_proof": False,
        "proof_bundle_row": {
            "wire_id": "PROOF_BUNDLE_DAG_V1",
            "required_fields": [
                "schema",
                "Round306B1AF4D1_proof_bundle_row_id",
                "subject_row_id",
                "claims",
                "dependency_edges",
                "root_claim_ids",
                "bundle_sha256",
                "formal_credit",
                "row_sha256",
            ],
            "claim_exact_fields": [
                "role",
                "claim_id",
                "kernel_id",
                "payload",
                "payload_sha256",
            ],
            "edge_exact_fields": ["claim_id", "depends_on_claim_id"],
            "claim_order": "role_rank_THEN_kernel_id_THEN_claim_id_ASCII",
            "edge_order": "claim_id_THEN_depends_on_claim_id_ASCII",
            "root_claim_order": "claim_id_ASCII",
            "row_id_rule": "round306b1af4d1-proof-bundle:SHA256(canonical([subject_row_id,ordered_claim_ids,ordered_edges]))",
            "DAG_required": True,
            "duplicate_claim_or_edge_forbidden": True,
            "payload_hash_recomputed": True,
            "all_dependencies_must_name_local_claims": True,
            "family_required_role_set_must_match_exactly": True,
        },
        "kernel": {
            "kernel_id": "PROOF_BUNDLE_DAG_VALIDATION_V1",
            "premises": {
                "bundle": "PROOF_BUNDLE_DAG_V1",
                "family": "STR",
                "subject_row_id": "STR",
            },
            "evidence": {
                "family_required_role_ids": "NONEMPTY_STR_LIST",
                "topological_claim_ids": "NONEMPTY_STR_LIST",
            },
            "conclusion": {
                "acyclic_claim": "BOOL_TRUE",
                "complete_role_set_claim": "BOOL_TRUE",
                "payload_integrity_claim": "BOOL_TRUE",
            },
        },
        "family_required_roles": {
            "G2_GRAPH_ROOT": [
                "AST_NORMALIZATION",
                "RADICAL_POSITIVITY",
                "INTERVAL_SIGNS",
                "MONOTONE_GRAPH_EXISTENCE_UNIQUENESS",
            ],
            "G2A_SHEET_MEMBER": [
                "AST_NORMALIZATION",
                "SHEET_MEMBER_SET_EQUALITY",
                "VIRTUAL_FULL_SUPPORT_SET_EQUALITY",
                "REPRESENTATION_BACKBINDING",
                "CHART_MAP_BIJECTION",
                "SOURCE_LINEAGE_EXHAUSTION",
            ],
            "G2B_SIDE_MEMBER": [
                "AST_NORMALIZATION",
                "PREDICATE_CELL_EQUIVALENCE",
                "FINITE_HALF_OPEN_SUPPORT_UNION_IF_MULTICELL",
                "VIRTUAL_FULL_SUPPORT_SET_EQUALITY",
                "REPRESENTATION_BACKBINDING",
                "CHART_MAP_BIJECTION",
                "SOURCE_LINEAGE_EXHAUSTION",
            ],
            "G2B_PHYSICAL_INCIDENCE": [
                "DEPENDENT_INCIDENCE_RESTRICTION",
                "REGULAR_LEVELSET_ONE_SIDED_TRACE",
                "MIXED_BOUNDARY_FACE_PARTITION",
            ],
        },
        "representation_required_roles": {
            "FULL_SET_EQUALITY": [
                "CHART_MAP_BIJECTION",
                "REPRESENTATION_OWNER_BACKBINDING",
                "WHOLE_SUPPORT_SET_EQUALITY",
            ],
            "PARTIAL_INCLUSION": [
                "CHART_MAP_OR_INCLUSION_MAP",
                "PARTIAL_REPRESENTATION_INCLUSION",
                "REPRESENTATION_OWNER_BACKBINDING",
                "MEMBER_REPRESENTATION_UNION_COVER",
            ],
            "partial_alias_may_omit_union_cover": False,
        },
        "row_id_rules": {
            "incidence": {
                "rule": "round306b1af4d1-incidence:SHA256(canonical([incidence_family,ambient_feature_row_id,dependent_feature_row_id,physical_face_ast_sha256,owner_member_row_id,orientation,source_reference_id]))",
                "natural_key_fields": [
                    "incidence_family",
                    "ambient_feature_row_id",
                    "dependent_feature_row_id",
                    "physical_face_ast_sha256",
                    "owner_member_row_id",
                    "orientation",
                    "source_reference_id",
                ],
            },
            "transition_handle": {
                "rule": "round306b1af4d1-transition-handle:SHA256(canonical([B0_member_id,representation_row_id,local_face_id,chart_side,owner_status]))",
                "natural_key_fields": [
                    "B0_member_id",
                    "representation_row_id",
                    "local_face_id",
                    "chart_side",
                    "owner_status",
                ],
            },
        },
        "transition_handle_exact_count": None,
        "transition_handle_count_may_be_guessed_from_115472": False,
        "independent_validation_algorithm": [
            "RECOMPUTE_EVERY_PAYLOAD_SHA256_AND_BUNDLE_SHA256",
            "VERIFY_CANONICAL_CLAIM_EDGE_AND_ROOT_ORDER",
            "VERIFY_ALL_EDGE_ENDPOINTS_EXIST_AND_THE_GRAPH_IS_ACYCLIC",
            "VERIFY_ROOTS_ARE_EXACTLY_NODES_WITH_NO_OUTGOING_CONSUMER_REQUIREMENT",
            "VERIFY_EXACT_FAMILY_ROLE_SET_WITH_NO_MISSING_OR_EXTRA_ROLE",
            "RECOMPUTE_INCIDENCE_AND_HANDLE_ROW_IDS_FROM_NATURAL_KEYS",
            "BLOCK_TRANSITION_HANDLE_COUNT_UNTIL_A_DIRECT_CENSUS_IS_PINNED",
        ],
        "current_status": "WIRE_RULE_COMPLETE_BUT_PROOF_PAYLOADS_AND_HANDLE_CENSUS_UNAVAILABLE",
        "formal_credit": 0,
    }


def _future_source_pins() -> list[dict[str, Any]]:
    files = [
        ("R220", "cm2_round220_source_g_round179_resolved_child_boundary_atlas_certificate.json", 294_422_681, "569a7849b53805ff4deca0eff9a6938a897942d3d682dfef27c27559135ce974", "ANALYTIC_LINEAGE_ONLY"),
        ("R234", "cm2_round234_source_g_wall_endpoint_order_depth6_materialization_certificate.json", 50_766_450, "6098032cf429855e816190e9345fa531f70e460eca60d75766e7108fc32c6fac", "CONSTRUCTION_DOMAIN_AUTHORITY"),
        ("R235", "cm2_round235_source_g_single_endpoint_graph_word_key_partition_certificate.json", 67_765_471, "e340fa1a071d85a36b54d10a45ae2fdb9d70b8c90f4c21f054c6fc9505e5e787", "CONSTRUCTION_LINEAGE"),
        ("R236", "cm2_round236_source_g_wall_residual_closure_and_root_key_partition_certificate.json", 2_061_199, "b5b9ec358b4837a02218756a034440d8fbc2aa706ca421bedb28aaf785de0217", "CONSTRUCTION_LINEAGE"),
        ("R242", "cm2_round242_source_g_outgoing_graph_existence_stratum_materialization_certificate.json", 13_734_655, "8d32c381e21c03aad6a531b7e5a527d295783b7e3e38baa1e6bcba20c40db22e", "CONSTRUCTION_LINEAGE"),
        ("R245", "cm2_round245_source_g_retained_graph_mixed_sheet_quotient_certificate.json", 20_683_081, "c76662f7cb068127f3612a3655ae720662eead9b9210b5757d771693149883c1", "CONSTRUCTION_LINEAGE"),
        ("R248", "cm2_round248_source_g_wall_finite_key_retained_quotient_certificate.json", 205_148_977, "fa48bdfb0056072f80c5809f57362c225f0beb40e1cc4c145f3f072335cdb311", "CONSTRUCTION_LINEAGE"),
        ("R264", "cm2_round264_source_g_lower_dimensional_endpoint_correction_and_glue_closure_certificate.json", 406_539_851, "ac9e9451e12621fd236fea39bc686e13b41ade62e5255de9c9cd98230763236f", "CORRECTION_AUTHORITY"),
        ("B1G0_GRAPH", "cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_graph_source_inventory.json.gz", 11_720_893, "5ac33be2b7639e1d30ae14abd5a7cf4cc6d1cc65fb0730e98616434f08921cb0", "IDENTITY_JOIN"),
        ("B1G0_SHEET", "cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_graph_sheet_join.json.gz", 13_922_080, "041328aa135a1a67cbbdc8c5d84fe2c1a9bef2231a6cb33668ab05ecd6b227e3", "IDENTITY_JOIN"),
        ("B1G0_SIDE", "cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_graph_side_join.json.gz", 25_932_945, "d79af13182f99cdb2df6d39731e762b0d145baf79772b99be5069669c5b80ee1", "IDENTITY_JOIN"),
        ("B1G0_R264", "cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_r264_correction_disposition.json.gz", 140_958, "834b687845a156328873888e405793f52a12df9d6286ae07d8a572c6163a361a", "CORRECTION_JOIN"),
        ("B1G0_BACKBINDING", "cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_b0_member_backbinding.json.gz", 32_731_854, "79382a6d8c3d086aeb29eff9fcb8653f2a73d85d79aab27e71e72cc8b1165a0b", "IDENTITY_BINDING"),
        ("B1G0_GAP", "cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_gap.json.gz", 23_240_985, "2ba1903e2ce6d44ee623d0ccaacce973f7327e1e36ba8f97d0ab3865f1ec9809", "ZERO_CREDIT_GAP_INVENTORY"),
        ("B0_MEMBER", "cm2_round306b0_source_g_r306a_universe_support_source_freeze_member_support_source_index.json.gz", 162_499_140, "c9a8649c8473bb6a170187e7f803e95748d2ff2198b1b846d97383dd5f0581af", "MEMBER_IDENTITY_BINDING"),
    ]
    return [
        {
            "label": label,
            "filename": filename,
            "exact_size": size,
            "source_sha256": sha,
            "authority_role": role,
        }
        for label, filename, size, sha, role in files
    ]


def _required_tables() -> list[dict[str, Any]]:
    rows = [
        ("R220.one_step_split_interface_rows", ".result.coordinate_boundary_atlas.tables.one_step_split_interface_rows.rows[]", 13_076, "221b5568223c452c9c590157afd592dfdc0f244e1322c275d55263b747d18f57"),
        ("R234.depth6_frontier_rows", ".result.depth6_frontier_rows[]", 38_376, "a1b3bf193ad10045f52244c3e40c52f78e0aeacffa3ba52c262bc8912fc9b5a6"),
        ("R235.single_endpoint_graph_partition_rows", ".result.single_endpoint_graph_partition_rows[]", 38_328, "e9a3794540170bf013160fb713acfbb1a65d42afedfb7b972cbfdad290549731"),
        ("R236.double_endpoint_partition_rows", ".result.double_endpoint_partition_rows[]", 16, "68f41212de0da7f3468a321a682978daa052cb65a611d756a901ca095bcc0bf6"),
        ("R242.formal_positive_2D_transition_sheet_patch_ledger", ".result.formal_positive_2D_transition_sheet_patch_ledger.rows[]", 264, "aaf7a94af40427dd8e1b805f2aa5c8c0532e7dc5b2420c803e165d39ba5c0a0f"),
        ("R245.formal_retained_stratum_node_ledger", ".result.formal_retained_stratum_node_ledger.rows[]", 3_664, "38583b1aa3f37e37dc03c2b59b2a31c18346462d3d918e001040d6651b11401b"),
        ("R245.mixed_sheet_physical_edge_rows", ".result.formal_mixed_sheet_physical_edge_ledger.rows[]", 3_664, "08da8a6331675f0fbb3fe6a01a9310dee8283f7de2673a7b08144bbf9f08e765"),
        ("R248.formal_wall_positive_volume_bulk_ledger", ".result.formal_wall_positive_volume_bulk_ledger.rows[]", 88_936, "aff5ea1401a6919529d1d54fe54bb9b8d378456fa48f88a75043505b5ee7b8b0"),
        ("R248.formal_wall_half_open_sheet_owner_ledger", ".result.formal_wall_half_open_sheet_owner_ledger.rows[]", 38_360, "e61754dc51732c4c82876d1c2e83fa040747d23253addd64350728169f5ae44b"),
        ("R264.formal_endpoint_empty_branch_correction_disposition_ledger", ".result.formal_endpoint_empty_branch_correction_disposition_ledger.rows[]", 400, "fdf499ca22f287866a24685a7671f8cfe950015be72c3da03db2331db7e38285"),
        ("B1G0.graph_source_inventory_rows", ".graph_source_inventory_rows[]", 38_624, "beda6faaf7d3be25075d8f2a7f292cba97f591d6255758b6b16efc141339673f"),
        ("B1G0.graph_sheet_join_rows", ".graph_sheet_join_rows[]", 38_624, "9238a05af9a97002488576d3648ce06ee750858f156638c314ba2e0a24fe3e1f"),
        ("B1G0.graph_side_join_rows", ".graph_side_join_rows[]", 76_848, "43ee8ffd2b77231c43c0af10198bbcc1f1def12f2e6bfd28f82c66ea26a207b2"),
        ("B1G0.r264_correction_disposition_rows", ".r264_correction_disposition_rows[]", 400, "a3df5bc8c8a86ea6958daefa7ec9b99013a04152378e5bcb18991ec4860cac67"),
        ("B1G0.b0_member_backbinding_rows", ".b0_member_backbinding_rows[]", 115_456, "35189ef67c69078e44bbd440be37ef870935a8fd67817501ae995cceae383ea6"),
        ("B1G0.gap_rows", ".gap_rows[]", 154_096, "d47d29e9eccc04374851cf12a3bc08fbe62837673fe8beb5dd1c9382337ad27b"),
        ("B0.member_support_source_rows", ".member_support_source_rows[]", 564_492, "c7dfb5534fddeb22fffb81bf539fe44d837aced46577aa5f490a0ae14aba77f5"),
    ]
    return [
        {"authority": authority, "json_path": path, "row_count": count, "rows_sha256": sha}
        for authority, path, count, sha in rows
    ]


def _source_overlay() -> dict[str, Any]:
    missing = [
        {
            "authority_id": "SOURCE_G_TARGET_GEOMETRY_CONSTANTS_AND_FIRST_HIT_FORMULA_V1",
            "required_content": "EXACT_FORMULA_DOMAIN_AND_TARGET_INDEX_CONVENTION__AF4D1_ALREADY_BINDS_G_RADIUS_9_OVER_25_AND_W_RADIUS_4_OVER_25",
            "current_status": "MISSING_DIRECT_NORMATIVE_AUTHORITY",
        },
        {
            "authority_id": "R236_CODIM2_DISPOSITION_V1",
            "required_content": "16_EXACT_EMPTY_OR_MATERIALIZED_DISPOSITIONS",
            "current_status": "MISSING_THEOREM_AUTHORITY",
        },
        {
            "authority_id": "SOURCE_G_VIRTUAL_MEMBER_EXTENSIONAL_SUPPORT_V1",
            "required_content": "ONE_NORMATIVE_SUPPORT_AST_PER_115456_DISTINCT_G2_MEMBER",
            "current_status": "MISSING_NORMATIVE_SUPPORT_AUTHORITY",
        },
        {
            "authority_id": "SOURCE_G_MIXED_BOUNDARY_TOPOLOGY_V1",
            "required_content": "ALL_TPS_ENDPOINT_INCLUSION_BITS_AND_SINGLE_FACE_OWNERS",
            "current_status": "MISSING_COMPLETE_FACE_AUTHORITY",
        },
        {
            "authority_id": "SOURCE_G_VIRTUAL_COORDINATE_AND_INVERSE_BRANCH_V1",
            "required_content": "VIRTUAL_P3D_AND_VIRTUAL_SHEET_COORDINATES_CODEDOMAINS_AND_INVERSES",
            "current_status": "MISSING_COORDINATE_AUTHORITY",
        },
        {
            "authority_id": "SOURCE_G_TRANSITION_HANDLE_CENSUS_V1",
            "required_content": "EXACT_HANDLE_NATURAL_KEYS_AND_COUNT",
            "current_status": "MISSING_CENSUS_AUTHORITY",
        },
        {
            "authority_id": "TPS_INTER_CHART_CANONICAL_BIJECTION_V1",
            "required_content": "CANONICAL_FORWARD_INVERSE_BRANCHES_AND_DOMAIN_COVER_FOR_TPS_ALIAS_INCLUSIONS",
            "current_status": "MISSING_CHART_MAP_THEOREM_AUTHORITY",
        },
    ]
    return {
        "delta_item": "H",
        "future_constructor_minimum_direct_source_pins": _future_source_pins(),
        "minimum_direct_source_pin_count": 15,
        "required_table_commitments": _required_tables(),
        "required_table_commitment_count": 17,
        "all_existing_pins_are_transitively_committed_by_AF3D1": True,
        "future_constructor_must_rehash_every_direct_file_through_held_fd": True,
        "future_constructor_must_not_rely_only_on_transitive_catalog_membership": True,
        "missing_required_authorities": missing,
        "missing_required_authority_count": 7,
        "R234_is_mandatory_for_R235_and_R236_domains": True,
        "R220_is_lineage_only_not_physical_glue": True,
        "B1G0_is_identity_only_not_geometry": True,
        "current_status": "DIRECT_EXISTING_BYTES_PINNED_BUT_SEVEN_NEW_AUTHORITIES_OR_THEOREMS_MISSING",
        "formal_credit": 0,
    }


def _scope_contract() -> dict[str, Any]:
    return {
        "purpose": "MINIMUM_VERSIONED_B_TO_H_SEMANTIC_AND_WIRE_OVERLAY",
        "delta_items": list(DELTA_ITEMS),
        "base_sources_are_not_modified": True,
        "normal_support_or_representation_credit_minted": False,
        "transition_or_pair_routing_credit_minted": False,
        "CM2_credit_minted": False,
    }


def _count_guardrails() -> dict[str, Any]:
    return {
        "graph_roots": G2_GRAPH_ROOT_COUNT,
        "G2A_members": G2A_MEMBER_COUNT,
        "G2B_references": G2B_REFERENCE_COUNT,
        "G2B_distinct_members": G2B_MEMBER_COUNT,
        "G2_distinct_members": G2_MEMBER_COUNT,
        "R236_reference_multiplicity_histogram": {"1": 76_816, "2": 16},
        "G2B_count_equation": "76256+64+528=76848_refs_AND_76256+48+528=76832_members",
        "G2_member_equation": "38624+76832=115456",
        "B1G0_gap_equation": "38624_graph+38624_sheet+76848_side=154096",
        "feature_ledger_count_may_be_frozen_from_824864": False,
        "known_natural_G2_feature_definition_count": 154_080,
        "known_natural_count_equation": "38624_graph+38624_sheet+76832_side=154080",
        "known_partial_alias_count": 9_884,
        "known_partial_alias_equation": "720_preserved_TPS+1600_preserved_T2PS+7288_R2_TPS+276_R295A=9884",
        "R2_two_cell_member_count": 4,
        "R2_artificial_face_reglue_count": 4,
        "R292_cell_count": 10_252,
        "R292_component_count": 9_404,
        "R292_canonical_Kruskal_accepted_face_count": 848,
    }


def _unresolved_hard_obligations() -> dict[str, Any]:
    return {
        "regular_levelset_one_sided_trace": 76_848,
        "R236_codim2_disposition": 16,
        "virtual_member_full_support_set_equality": 115_456,
        "mixed_boundary_face_partition": "COUNT_UNAVAILABLE_UNTIL_FACE_AUTHORITY",
        "chart_map_bijection_for_G2_representations": 115_456,
        "known_partial_representation_inclusions": 10_732,
        "known_partial_representation_equation": "9884_aliases+848_refined_primary_extras=10732",
        "member_representation_union_cover": "OWNER_GROUP_COUNT_REQUIRES_DIRECT_CENSUS",
        "TPS_inter_chart_canonical_bijection": "UNRESOLVED",
        "R2_artificial_face_reglue": 4,
        "R292_physical_face_and_Kruskal_order": 848,
        "transition_handle_census": "UNKNOWN_NOT_115472_BY_DEFAULT",
        "all_are_formal_blockers": True,
        "none_may_be_closed_by_labels_witnesses_or_identity_joins": True,
    }


def _candidate_modes_contract() -> dict[str, Any]:
    return {
        "enabled": False,
        "block_before_path_lstat": True,
        "block_before_os_stat": True,
        "block_before_input_open": True,
        "block_before_temp_creation": True,
        "block_before_output_write": True,
        "block_before_stdout_or_stderr": True,
        "block_reason": CANDIDATE_BLOCK_REASON,
    }


def _formal_credit_contract() -> dict[str, int]:
    return {
        "normalized_support": 0,
        "representation_cover": 0,
        "physical_incidence": 0,
        "transition": 0,
        "pair_routing": 0,
        "maximality": 0,
        "CM2": 0,
    }


def _downstream_state_contract() -> dict[str, str]:
    return {
        "AF4_CONSTRUCTOR": "BLOCKED_ON_EXPLICIT_B_TO_H_OBLIGATIONS",
        "B1A": "BLOCKED",
        "B2": "NOT_AUTHORIZED",
        "D02": "BLOCKED",
        "CM2": "NO-GO_FOR_CLAIM",
    }


def _contract_document() -> dict[str, Any]:
    return {
        "schema": SCHEMA,
        "status": STATUS,
        "sealed": True,
        "candidate_is_formal": False,
        "scope": _scope_contract(),
        "sealed_base_dependency_pins": _dependency_contract(),
        "delta_operator_ids": list(DELTA_OPERATOR_IDS),
        "delta_wire_ids": list(DELTA_WIRE_IDS),
        "delta_kernel_ids": list(DELTA_KERNEL_IDS),
        "B_one_sided_closure_trace": _trace_overlay(),
        "C_R236_codim2": _codim2_overlay(),
        "D_virtual_full_support": _full_support_overlay(),
        "E_mixed_boundary_topology": _boundary_overlay(),
        "F_formula_frame_and_chart_map": _map_overlay(),
        "G_proof_bundle_and_row_ids": _proof_bundle_overlay(),
        "H_minimum_direct_pins_and_blockers": _source_overlay(),
        "count_guardrails": _count_guardrails(),
        "unresolved_hard_obligations": _unresolved_hard_obligations(),
        "candidate_and_production_modes": _candidate_modes_contract(),
        "formal_credit": _formal_credit_contract(),
        "downstream_state": _downstream_state_contract(),
    }


def _contains_null(value: Any) -> bool:
    if value is None:
        return True
    if isinstance(value, dict):
        return any(_contains_null(item) for item in value.values())
    if isinstance(value, list):
        return any(_contains_null(item) for item in value)
    return False


def validate_contract(document: dict[str, Any]) -> None:
    expected_keys = {
        "schema", "status", "sealed", "candidate_is_formal", "scope",
        "sealed_base_dependency_pins", "delta_operator_ids", "delta_wire_ids",
        "delta_kernel_ids", "B_one_sided_closure_trace", "C_R236_codim2",
        "D_virtual_full_support", "E_mixed_boundary_topology",
        "F_formula_frame_and_chart_map", "G_proof_bundle_and_row_ids",
        "H_minimum_direct_pins_and_blockers", "count_guardrails",
        "unresolved_hard_obligations", "candidate_and_production_modes",
        "formal_credit", "downstream_state",
    }
    need(set(document) == expected_keys, "exact contract top-level keys")
    need(document["schema"] == SCHEMA, "schema")
    need(document["status"] == STATUS, "status")
    need(document["sealed"] is True, "sealed")
    need(document["candidate_is_formal"] is False, "candidate nonformal")
    need(document["scope"] == _scope_contract(), "exact scope contract")
    need(document["scope"]["delta_items"] == list(DELTA_ITEMS), "B-H exact scope")
    need(document["scope"]["base_sources_are_not_modified"] is True, "overlay only")
    need(document["sealed_base_dependency_pins"] == _dependency_contract(), "exact base pins")
    pins = document["sealed_base_dependency_pins"]
    need(pins["dependency_source_count"] == len(pins["dependency_sources"]) == 3, "three pins")
    need(tuple(pins["dependency_sources"]) == DEPENDENCY_PINS, "dependency bytes")
    need(pins["dependency_source_set_sha256"] == digest(DEPENDENCY_PINS), "pin set digest")
    need(not _contains_null(pins), "no null base pins")
    need(tuple(document["delta_operator_ids"]) == DELTA_OPERATOR_IDS, "operators")
    need(tuple(document["delta_wire_ids"]) == DELTA_WIRE_IDS, "wires")
    need(tuple(document["delta_kernel_ids"]) == DELTA_KERNEL_IDS, "kernels")

    trace = document["B_one_sided_closure_trace"]
    need(trace == _trace_overlay(), "exact trace overlay")
    need(trace["old_pointwise_trace_is_forbidden"] is True, "old trace forbidden")
    need(trace["old_lowering_may_mint_physical_incidence"] is False, "old trace no credit")
    need(trace["canonical_operator"]["operator_id"] == "RELATIVE_CLOSURE_TRACE", "closure operator")
    need(trace["canonical_operator"]["not_lowered_to_pointwise_RESTRICT"] is True, "no pointwise lowering")
    need(trace["kernel"]["kernel_id"] == DELTA_KERNEL_IDS[0], "trace kernel")
    need(trace["current_obligation_count"] == G2B_REFERENCE_COUNT, "trace obligations")

    codim2 = document["C_R236_codim2"]
    need(codim2 == _codim2_overlay(), "exact codim2 overlay")
    need(codim2["partition_count"] == R236_PARTITION_COUNT, "R236 count")
    need(codim2["all_partitions_are_hard_obligations"] is True, "R236 hard")
    arrangement = codim2["canonical_arrangement"]
    need(arrangement["Z_SOURCE_TARGET_may_not_be_erased"] is True, "codim2 retained")
    need(arrangement["lowerings"]["Z_SOURCE_TARGET"] == "AND(D,EQ_ZERO(fs),EQ_ZERO(ft))", "codim2 conjunction")
    need(codim2["kernel"]["default_disposition_forbidden"] is True, "no codim default")
    need(set(codim2["kernel"]["evidence_variants"]) == {"EMPTY", "MATERIALIZED_REGULAR", "BLOCKED_SINGULAR"}, "codim variants")
    need(codim2["existing_authority_supplies_disposition"] is False, "codim authority absent")

    support = document["D_virtual_full_support"]
    need(support == _full_support_overlay(), "exact support overlay")
    need(support["exact_distinct_member_obligation_count"] == G2_MEMBER_COUNT, "support obligations")
    need(sum(support["fine_counts"].values()) == G2_MEMBER_COUNT, "support fine count")
    need(len(support["forbidden_substitutions"]) == 6, "support substitutions")
    need(support["R264_guardrail"]["empty_EVENT_ABSENT"] + support["R264_guardrail"]["empty_EVENT_PRESENT"] == R264_CORRECTION_COUNT, "R264 split")
    need(support["R264_guardrail"]["suppressed_branch_member_or_edge_may_reappear"] is False, "R264 suppression")
    need(support["existing_authority_has_extensional_full_support_semantics"] is False, "support authority missing")
    rep_delta = support["representation_semantics_delta"]
    need(rep_delta == _representation_semantics_overlay(), "exact representation semantics overlay")
    need(
        rep_delta["known_partial_representation_classes"]
        == {
            "PRESERVED_TPS_INCLUSION": 720,
            "PRESERVED_T2PS_SUBCOVER": 1_600,
            "R2_TPS_INCLUSION": 7_288,
            "R295A_ADJACENT_CONTINUATION": 276,
            "R292_REFINED_PRIMARY_EXTRA": 848,
        },
        "partial representation classes",
    )
    need(rep_delta["known_alias_partial_count"] == 9_884, "partial alias count")
    need(rep_delta["per_representation_coverage_semantics_field"]["a_partial_row_may_satisfy_full_set_equality"] is False, "partial not whole")
    need(rep_delta["partial_inclusion_kernel"]["kernel_id"] == "PARTIAL_REPRESENTATION_INCLUSION_V1", "partial kernel")
    need(rep_delta["member_union_cover_kernel"]["kernel_id"] == "MEMBER_REPRESENTATION_UNION_COVER_V1", "union cover kernel")
    need(rep_delta["TPS_inter_chart_canonical_bijection_available"] is False, "TPS chart blocker")
    need(rep_delta["R2_four_face_reglue"]["artificial_face_reglue_obligation_count"] == 4, "R2 reglue")
    need(rep_delta["R292_canonical_Kruskal"]["accepted_face_count"] == 848, "R292 Kruskal count")
    need(rep_delta["R292_canonical_Kruskal"]["hash_seed_may_affect_order_or_result"] is False, "R292 seed independence")

    boundary = document["E_mixed_boundary_topology"]
    need(boundary == _boundary_overlay(), "exact boundary overlay")
    need(tuple(boundary["new_predicate_operators"]) == ("LE_ZERO", "GE_ZERO"), "closed operators")
    need(boundary["interval_box_wire"]["axis_order"] == ["t", "p", "s"], "TPS order")
    need(boundary["interval_box_wire"]["lowering"]["lower_closed_true"].startswith("GE_ZERO"), "closed lower")
    need(boundary["interval_box_wire"]["lowering"]["upper_closed_true"].startswith("LE_ZERO"), "closed upper")
    need(boundary["strict_open_TPS_DOMAIN_is_sufficient_for_mixed_topology"] is False, "mixed topology gap")
    need(boundary["existing_sources_uniquely_freeze_all_outer_face_bits"] is False, "face authority gap")

    maps = document["F_formula_frame_and_chart_map"]
    need(maps == _map_overlay(), "exact map overlay")
    need(maps["formula_frame"]["scalar_field_count"] == len(maps["formula_frame"]["scalar_field_order"]) == 21, "formula fields")
    need(
        maps["physical_target_binding"]["G"]["radius"] == {"numerator": 9, "denominator": 25}
        and maps["physical_target_binding"]["W"]["radius"] == {"numerator": 4, "denominator": 25},
        "physical target radii",
    )
    need(maps["physical_target_binding"]["radius_is_selected_only_by_target_kind"] is True, "radius target binding")
    need(maps["formula_frame"]["is_ChartMap"] is False, "frame not map")
    need(maps["chart_map"]["nonempty_inverse_branch_set_required"] is True, "inverse branches")
    need(maps["current_first_hit_lowering_is_only_SOURCE_G_SCALAR_MAP"] is True, "current scalar frame")
    need(maps["current_sources_freeze_virtual_target_coordinates_and_inverse_branches"] is False, "map authority missing")

    bundles = document["G_proof_bundle_and_row_ids"]
    need(bundles == _proof_bundle_overlay(), "exact bundle overlay")
    need(bundles["singular_proof_kernel_field_can_encode_a_composite_proof"] is False, "singular proof forbidden")
    need(bundles["proof_bundle_row"]["DAG_required"] is True, "proof DAG")
    need(bundles["proof_bundle_row"]["payload_hash_recomputed"] is True, "payload hashes")
    need(set(bundles["row_id_rules"]) == {"incidence", "transition_handle"}, "row ID rules")
    need(bundles["transition_handle_exact_count"] is None, "handle count unknown")
    need(bundles["transition_handle_count_may_be_guessed_from_115472"] is False, "no handle guess")

    sources = document["H_minimum_direct_pins_and_blockers"]
    need(sources == _source_overlay(), "exact source overlay")
    need(sources["minimum_direct_source_pin_count"] == len(sources["future_constructor_minimum_direct_source_pins"]) == 15, "source pin count")
    need(sources["required_table_commitment_count"] == len(sources["required_table_commitments"]) == 17, "table commitment count")
    need(sources["missing_required_authority_count"] == len(sources["missing_required_authorities"]) == 7, "missing authority count")
    need(sources["R234_is_mandatory_for_R235_and_R236_domains"] is True, "R234 mandatory")
    need(sources["R220_is_lineage_only_not_physical_glue"] is True, "R220 role")
    need(sources["B1G0_is_identity_only_not_geometry"] is True, "B1G0 role")
    filenames: set[str] = set()
    for row in sources["future_constructor_minimum_direct_source_pins"]:
        need(set(row) == {"label", "filename", "exact_size", "source_sha256", "authority_role"}, "source pin shape")
        need(row["filename"] == os.path.basename(row["filename"]), "source pin basename")
        need(row["filename"] not in filenames, "unique source pin")
        filenames.add(row["filename"])
        need(type(row["exact_size"]) is int and row["exact_size"] > 0, "source pin size")
        need(HEX64.fullmatch(row["source_sha256"]) is not None, "source pin hash")
    authorities: set[str] = set()
    for row in sources["required_table_commitments"]:
        need(set(row) == {"authority", "json_path", "row_count", "rows_sha256"}, "table pin shape")
        need(row["authority"] not in authorities, "unique table authority")
        authorities.add(row["authority"])
        need(row["json_path"].startswith("."), "table path")
        need(type(row["row_count"]) is int and row["row_count"] > 0, "table count")
        need(HEX64.fullmatch(row["rows_sha256"]) is not None, "table hash")

    counts = document["count_guardrails"]
    need(counts == _count_guardrails(), "exact count guardrails")
    need(counts["graph_roots"] == counts["G2A_members"] == G2_GRAPH_ROOT_COUNT, "graph sheet count")
    need(counts["G2B_references"] == G2B_REFERENCE_COUNT, "G2B refs")
    need(counts["G2B_distinct_members"] == G2B_MEMBER_COUNT, "G2B members")
    need(counts["G2_distinct_members"] == G2_MEMBER_COUNT, "G2 members")
    need(counts["R236_reference_multiplicity_histogram"] == {"1": 76_816, "2": 16}, "multiplicity")
    need(counts["feature_ledger_count_may_be_frozen_from_824864"] is False, "824864 nonfinal")
    need(counts["known_natural_G2_feature_definition_count"] == 154_080, "natural G2 features")
    need(counts["known_partial_alias_count"] == 9_884, "known partial aliases")
    need(counts["R2_two_cell_member_count"] == counts["R2_artificial_face_reglue_count"] == 4, "R2 four faces")
    need(counts["R292_cell_count"] - counts["R292_canonical_Kruskal_accepted_face_count"] == counts["R292_component_count"] == 9_404, "R292 Kruskal equation")

    obligations = document["unresolved_hard_obligations"]
    need(obligations == _unresolved_hard_obligations(), "exact unresolved obligations")
    need(obligations["regular_levelset_one_sided_trace"] == 76_848, "trace unresolved")
    need(obligations["R236_codim2_disposition"] == 16, "codim unresolved")
    need(obligations["virtual_member_full_support_set_equality"] == 115_456, "support unresolved")
    need(obligations["chart_map_bijection_for_G2_representations"] == 115_456, "map unresolved")
    need(obligations["known_partial_representation_inclusions"] == 10_732, "partial inclusion unresolved")
    need(obligations["TPS_inter_chart_canonical_bijection"] == "UNRESOLVED", "TPS chart unresolved")
    need(obligations["R2_artificial_face_reglue"] == 4, "R2 reglue unresolved")
    need(obligations["R292_physical_face_and_Kruskal_order"] == 848, "R292 order unresolved")
    need(obligations["all_are_formal_blockers"] is True, "hard blockers")
    need(obligations["none_may_be_closed_by_labels_witnesses_or_identity_joins"] is True, "no substitution")

    modes = document["candidate_and_production_modes"]
    need(modes == _candidate_modes_contract(), "exact candidate mode contract")
    need(modes["enabled"] is False, "modes disabled")
    for key in (
        "block_before_path_lstat", "block_before_os_stat", "block_before_input_open",
        "block_before_temp_creation", "block_before_output_write",
        "block_before_stdout_or_stderr",
    ):
        need(modes[key] is True, "mode boundary:" + key)
    need(modes["block_reason"] == CANDIDATE_BLOCK_REASON, "mode reason")
    need(document["formal_credit"] == _formal_credit_contract(), "exact formal credit map")
    need(all(value == 0 for value in document["formal_credit"].values()), "zero credit")
    state = document["downstream_state"]
    need(state == _downstream_state_contract(), "exact downstream state")
    need(state["AF4_CONSTRUCTOR"].startswith("BLOCKED_"), "constructor blocked")
    need(state["B1A"] == "BLOCKED", "B1A blocked")
    need(state["B2"] == "NOT_AUTHORIZED", "B2 blocked")
    need(state["CM2"] == "NO-GO_FOR_CLAIM", "CM2 blocked")


def contract_envelope() -> dict[str, Any]:
    document = _contract_document()
    validate_contract(document)
    return {"contract": document, "canonical_contract_digest_sha256": digest(document)}


def _stat_fingerprint(info: os.stat_result) -> tuple[int, ...]:
    return (
        info.st_dev,
        info.st_ino,
        info.st_mode,
        info.st_nlink,
        info.st_size,
        info.st_mtime_ns,
        info.st_ctime_ns,
    )


def _directory_identity(info: os.stat_result) -> tuple[int, int, int]:
    return (info.st_dev, info.st_ino, info.st_mode)


def _hash_held_fd(fd: int) -> tuple[int, str]:
    os.lseek(fd, 0, os.SEEK_SET)
    total = 0
    hasher = hashlib.sha256()
    while True:
        block = os.read(fd, 1024 * 1024)
        if not block:
            break
        total += len(block)
        hasher.update(block)
    return total, hasher.hexdigest()


def verify_dependencies() -> dict[str, Any]:
    """Verify exactly the three final base sources through held raw fds."""

    need(len(DEPENDENCY_PINS) == 3, "exact three dependency pins")
    directory_text = os.fspath(DEPENDENCY_DIRECTORY)
    directory_before_path = os.stat(directory_text, follow_symlinks=False)
    need(stat.S_ISDIR(directory_before_path.st_mode), "dependency directory")
    directory_flags = (
        os.O_RDONLY
        | getattr(os, "O_DIRECTORY", 0)
        | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_NOFOLLOW", 0)
    )
    directory_fd = os.open(directory_text, directory_flags)
    result_rows: list[dict[str, Any]] = []
    try:
        directory_held_before = os.fstat(directory_fd)
        need(
            _directory_identity(directory_before_path) == _directory_identity(directory_held_before),
            "directory open race",
        )
        opened: list[tuple[dict[str, Any], int, os.stat_result]] = []
        try:
            for pin in DEPENDENCY_PINS:
                filename = pin["filename"]
                need(filename == os.path.basename(filename) and filename not in ("", ".", ".."), "dependency basename")
                path_before = os.stat(filename, dir_fd=directory_fd, follow_symlinks=False)
                need(stat.S_ISREG(path_before.st_mode), "dependency regular:" + filename)
                need(path_before.st_nlink == 1, "dependency nlink:" + filename)
                need(path_before.st_size == pin["exact_size"], "dependency size:" + filename)
                file_flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
                fd = os.open(filename, file_flags, dir_fd=directory_fd)
                held_before = os.fstat(fd)
                need(_stat_fingerprint(path_before) == _stat_fingerprint(held_before), "dependency open race:" + filename)
                opened.append((pin, fd, held_before))
            for pin, fd, held_before in opened:
                filename = pin["filename"]
                pass1_size, pass1_sha = _hash_held_fd(fd)
                held_between = os.fstat(fd)
                need(_stat_fingerprint(held_before) == _stat_fingerprint(held_between), "dependency pass1 race:" + filename)
                pass2_size, pass2_sha = _hash_held_fd(fd)
                held_after = os.fstat(fd)
                need(_stat_fingerprint(held_before) == _stat_fingerprint(held_after), "dependency pass2 race:" + filename)
                path_after = os.stat(filename, dir_fd=directory_fd, follow_symlinks=False)
                need(_stat_fingerprint(held_before) == _stat_fingerprint(path_after), "dependency path replaced:" + filename)
                need(pass1_size == pass2_size == pin["exact_size"], "dependency two-pass size:" + filename)
                need(pass1_sha == pass2_sha == pin["source_sha256"], "dependency two-pass hash:" + filename)
                result_rows.append({
                    "label": pin["label"],
                    "filename": filename,
                    "exact_size": pin["exact_size"],
                    "expected_source_sha256": pin["source_sha256"],
                    "pass1_size": pass1_size,
                    "pass1_sha256": pass1_sha,
                    "pass2_size": pass2_size,
                    "pass2_sha256": pass2_sha,
                    "regular_file": True,
                    "link_count_one": True,
                    "held_fd_identity_stable": True,
                    "dirfd_path_identity_stable": True,
                })
        finally:
            for _pin, fd, _held_before in reversed(opened):
                os.close(fd)
        directory_held_after = os.fstat(directory_fd)
        directory_after_path = os.stat(directory_text, follow_symlinks=False)
        need(
            _directory_identity(directory_held_before)
            == _directory_identity(directory_held_after)
            == _directory_identity(directory_after_path),
            "dependency directory replaced",
        )
    finally:
        os.close(directory_fd)

    body = {
        "schema": SCHEMA + ".dependency-verification.v1",
        "status": "PASS_EXACT_THREE_FINAL_SOURCES_HELD_DIRFD_TWO_PASS_RAW_BYTES",
        "dependency_source_count": 3,
        "dependency_source_set_sha256": digest(DEPENDENCY_PINS),
        "raw_bytes_only": True,
        "dependency_imported": False,
        "dependency_executed": False,
        "dependency_parsed": False,
        "all_file_fds_open_before_first_hash": True,
        "files": result_rows,
        "formal_credit": 0,
    }
    return {**body, "verification_digest_sha256": digest(body)}


def _set_path(document: dict[str, Any], path: tuple[Any, ...], value: Any) -> None:
    cursor: Any = document
    for key in path[:-1]:
        cursor = cursor[key]
    cursor[path[-1]] = value


def _delete_path(document: dict[str, Any], path: tuple[Any, ...]) -> None:
    cursor: Any = document
    for key in path[:-1]:
        cursor = cursor[key]
    del cursor[path[-1]]


Mutation = tuple[str, Callable[[dict[str, Any]], None]]


def _semantic_mutations() -> list[Mutation]:
    def setter(path: tuple[Any, ...], value: Any) -> Callable[[dict[str, Any]], None]:
        return lambda doc: _set_path(doc, path, value)

    def deleter(path: tuple[Any, ...]) -> Callable[[dict[str, Any]], None]:
        return lambda doc: _delete_path(doc, path)

    return [
        ("schema", setter(("schema",), SCHEMA + ".mutated")),
        ("status", setter(("status",), "PASS_FORMAL")),
        ("sealed", setter(("sealed",), False)),
        ("candidate formal", setter(("candidate_is_formal",), True)),
        ("scope support credit", setter(("scope", "normal_support_or_representation_credit_minted"), True)),
        ("scope CM2 credit", setter(("scope", "CM2_credit_minted"), True)),
        ("AF3D1 pin", setter(("sealed_base_dependency_pins", "dependency_sources", 0, "source_sha256"), "0" * 64)),
        ("kernel pin", setter(("sealed_base_dependency_pins", "dependency_sources", 1, "source_sha256"), "1" * 64)),
        ("schema pin", setter(("sealed_base_dependency_pins", "dependency_sources", 2, "source_sha256"), "2" * 64)),
        ("dependency count", setter(("sealed_base_dependency_pins", "dependency_source_count"), 2)),
        ("operator deletion", lambda doc: doc["delta_operator_ids"].pop()),
        ("kernel invention", lambda doc: doc["delta_kernel_ids"].append("LABEL_PROOF_V1")),
        ("old pointwise trace admitted", setter(("B_one_sided_closure_trace", "old_pointwise_trace_is_forbidden"), False)),
        ("old trace credit", setter(("B_one_sided_closure_trace", "old_lowering_may_mint_physical_incidence"), True)),
        ("drop closure", setter(("B_one_sided_closure_trace", "canonical_operator", "denotation"), "RESTRICT(side,boundary)")),
        ("trace orientation", setter(("B_one_sided_closure_trace", "canonical_operator", "side_sign_values"), [1])),
        ("trace evidence", deleter(("B_one_sided_closure_trace", "kernel", "evidence", "continuity_claim_id"))),
        ("trace obligation", setter(("B_one_sided_closure_trace", "current_obligation_count"), 76_832)),
        ("R236 count", setter(("C_R236_codim2", "partition_count"), 15)),
        ("R236 not hard", setter(("C_R236_codim2", "all_partitions_are_hard_obligations"), False)),
        ("erase codim2", setter(("C_R236_codim2", "canonical_arrangement", "Z_SOURCE_TARGET_may_not_be_erased"), False)),
        ("codim2 OR", setter(("C_R236_codim2", "canonical_arrangement", "lowerings", "Z_SOURCE_TARGET"), "OR(D,EQ_ZERO(fs),EQ_ZERO(ft))")),
        ("codim default", setter(("C_R236_codim2", "kernel", "default_disposition_forbidden"), False)),
        ("codim authority invented", setter(("C_R236_codim2", "existing_authority_supplies_disposition"), True)),
        ("full support count", setter(("D_virtual_full_support", "exact_distinct_member_obligation_count"), 115_455)),
        ("witness as support", lambda doc: doc["D_virtual_full_support"]["forbidden_substitutions"].remove("R245_STRICT_INNER_WITNESS_OR_CORRIDOR_AS_FULL_SUPPORT")),
        ("edge as equality", lambda doc: doc["D_virtual_full_support"]["forbidden_substitutions"].remove("R245_EDGE_LABEL_OR_IDENTIFIER_ADJACENCY_AS_SET_EQUALITY")),
        ("R264 resurrection", setter(("D_virtual_full_support", "R264_guardrail", "suppressed_branch_member_or_edge_may_reappear"), True)),
        ("extensional authority invented", setter(("D_virtual_full_support", "existing_authority_has_extensional_full_support_semantics"), True)),
        ("partial alias as whole", setter(("D_virtual_full_support", "representation_semantics_delta", "per_representation_coverage_semantics_field", "a_partial_row_may_satisfy_full_set_equality"), True)),
        ("partial alias identity", setter(("D_virtual_full_support", "representation_semantics_delta", "per_representation_coverage_semantics_field", "a_partial_row_may_mint_member_identity"), True)),
        ("partial alias count", setter(("D_virtual_full_support", "representation_semantics_delta", "known_partial_representation_classes", "R2_TPS_INCLUSION"), 7_287)),
        ("partial kernel substitution", setter(("D_virtual_full_support", "representation_semantics_delta", "partial_inclusion_kernel", "kernel_id"), "REPRESENTATION_OWNER_BACKBINDING_V1")),
        ("union cover deletion", deleter(("D_virtual_full_support", "representation_semantics_delta", "member_union_cover_kernel", "evidence", "reverse_union_inclusion_claim_ids"))),
        ("TPS chart invented", setter(("D_virtual_full_support", "representation_semantics_delta", "TPS_inter_chart_canonical_bijection_available"), True)),
        ("R2 reglue count", setter(("D_virtual_full_support", "representation_semantics_delta", "R2_four_face_reglue", "artificial_face_reglue_obligation_count"), 3)),
        ("R292 Kruskal order", lambda doc: doc["D_virtual_full_support"]["representation_semantics_delta"]["R292_canonical_Kruskal"]["candidate_face_order"].reverse()),
        ("R292 seed dependence", setter(("D_virtual_full_support", "representation_semantics_delta", "R292_canonical_Kruskal", "hash_seed_may_affect_order_or_result"), True)),
        ("drop LE", deleter(("E_mixed_boundary_topology", "new_predicate_operators", "LE_ZERO"))),
        ("closed lower wrong", setter(("E_mixed_boundary_topology", "interval_box_wire", "lowering", "lower_closed_true"), "GT_ZERO(SUB(VAR(axis),CONST_Q(lower)))")),
        ("axis order", setter(("E_mixed_boundary_topology", "interval_box_wire", "axis_order"), ["p", "s", "t"])),
        ("open box sufficient", setter(("E_mixed_boundary_topology", "strict_open_TPS_DOMAIN_is_sufficient_for_mixed_topology"), True)),
        ("face authority invented", setter(("E_mixed_boundary_topology", "existing_sources_uniquely_freeze_all_outer_face_bits"), True)),
        ("formula frame map", setter(("F_formula_frame_and_chart_map", "formula_frame", "is_ChartMap"), True)),
        ("G radius", setter(("F_formula_frame_and_chart_map", "physical_target_binding", "G", "radius", "numerator"), 4)),
        ("W radius", setter(("F_formula_frame_and_chart_map", "physical_target_binding", "W", "radius", "numerator"), 9)),
        ("radius unbound", setter(("F_formula_frame_and_chart_map", "physical_target_binding", "radius_is_selected_only_by_target_kind"), False)),
        ("formula field deletion", lambda doc: doc["F_formula_frame_and_chart_map"]["formula_frame"]["scalar_field_order"].pop()),
        ("empty inverse allowed", setter(("F_formula_frame_and_chart_map", "chart_map", "nonempty_inverse_branch_set_required"), False)),
        ("virtual inverse invented", setter(("F_formula_frame_and_chart_map", "current_sources_freeze_virtual_target_coordinates_and_inverse_branches"), True)),
        ("singular composite", setter(("G_proof_bundle_and_row_ids", "singular_proof_kernel_field_can_encode_a_composite_proof"), True)),
        ("DAG disabled", setter(("G_proof_bundle_and_row_ids", "proof_bundle_row", "DAG_required"), False)),
        ("payload hash disabled", setter(("G_proof_bundle_and_row_ids", "proof_bundle_row", "payload_hash_recomputed"), False)),
        ("incidence row ID", setter(("G_proof_bundle_and_row_ids", "row_id_rules", "incidence", "rule"), "SOURCE_ID")),
        ("handle guessed", setter(("G_proof_bundle_and_row_ids", "transition_handle_exact_count"), 115_472)),
        ("handle guess allowed", setter(("G_proof_bundle_and_row_ids", "transition_handle_count_may_be_guessed_from_115472"), True)),
        ("source pin size", setter(("H_minimum_direct_pins_and_blockers", "future_constructor_minimum_direct_source_pins", 1, "exact_size"), 50_766_449)),
        ("source pin hash", setter(("H_minimum_direct_pins_and_blockers", "future_constructor_minimum_direct_source_pins", 2, "source_sha256"), "3" * 64)),
        ("table row count", setter(("H_minimum_direct_pins_and_blockers", "required_table_commitments", 3, "row_count"), 15)),
        ("table rows hash", setter(("H_minimum_direct_pins_and_blockers", "required_table_commitments", 4, "rows_sha256"), "4" * 64)),
        ("missing authority erased", lambda doc: doc["H_minimum_direct_pins_and_blockers"]["missing_required_authorities"].pop()),
        ("R234 optional", setter(("H_minimum_direct_pins_and_blockers", "R234_is_mandatory_for_R235_and_R236_domains"), False)),
        ("R220 glue", setter(("H_minimum_direct_pins_and_blockers", "R220_is_lineage_only_not_physical_glue"), False)),
        ("B1G0 geometry", setter(("H_minimum_direct_pins_and_blockers", "B1G0_is_identity_only_not_geometry"), False)),
        ("G2B refs", setter(("count_guardrails", "G2B_references"), 76_832)),
        ("multiplicity", setter(("count_guardrails", "R236_reference_multiplicity_histogram", "2"), 15)),
        ("G2B count equation", setter(("count_guardrails", "G2B_count_equation"), "CORRUPTED")),
        ("partial alias equation", setter(("count_guardrails", "known_partial_alias_equation"), "720+1600+7288+276=9883")),
        ("824864 feature count", setter(("count_guardrails", "feature_ledger_count_may_be_frozen_from_824864"), True)),
        ("mixed boundary resolved", setter(("unresolved_hard_obligations", "mixed_boundary_face_partition"), 0)),
        ("member representation union cover resolved", setter(("unresolved_hard_obligations", "member_representation_union_cover"), "PASS")),
        ("transition handle census guessed", setter(("unresolved_hard_obligations", "transition_handle_census"), 115_472)),
        ("blockers false", setter(("unresolved_hard_obligations", "all_are_formal_blockers"), False)),
        ("label substitution", setter(("unresolved_hard_obligations", "none_may_be_closed_by_labels_witnesses_or_identity_joins"), False)),
        ("candidate enabled", setter(("candidate_and_production_modes", "enabled"), True)),
        ("stat boundary", setter(("candidate_and_production_modes", "block_before_os_stat"), False)),
        ("stdout boundary", setter(("candidate_and_production_modes", "block_before_stdout_or_stderr"), False)),
        ("formal credit", setter(("formal_credit", "physical_incidence"), 1)),
        ("formal credit key deleted", deleter(("formal_credit", "CM2"))),
        ("formal credit map empty", lambda doc: doc["formal_credit"].clear()),
        ("constructor pass", setter(("downstream_state", "AF4_CONSTRUCTOR"), "PASS")),
        ("B1A pass", setter(("downstream_state", "B1A"), "PASS")),
        ("B2 authorized", setter(("downstream_state", "B2"), "AUTHORIZED")),
        ("D02 pass", setter(("downstream_state", "D02"), "PASS")),
        ("D02 deleted", deleter(("downstream_state", "D02"))),
        ("CM2 GO", setter(("downstream_state", "CM2"), "GO")),
    ]


def _blocked_candidate_entry(_output_path: str | None, _produce: bool) -> None:
    raise ContractBlocked(CANDIDATE_BLOCK_REASON)


def _boundary_probe() -> dict[str, int]:
    counters = {
        "builtins_open": 0,
        "os_open": 0,
        "os_stat": 0,
        "os_lstat": 0,
        "path_lstat": 0,
        "path_open": 0,
        "path_write_bytes": 0,
        "path_write_text": 0,
        "mkstemp": 0,
        "named_temp": 0,
    }

    def trip(name: str) -> Callable[..., Any]:
        def inner(*_args: Any, **_kwargs: Any) -> Any:
            counters[name] += 1
            raise AssertionError("filesystem boundary crossed:" + name)
        return inner

    with (
        mock.patch("builtins.open", side_effect=trip("builtins_open")),
        mock.patch("os.open", side_effect=trip("os_open")),
        mock.patch("os.stat", side_effect=trip("os_stat")),
        mock.patch("os.lstat", side_effect=trip("os_lstat")),
        mock.patch.object(Path, "lstat", side_effect=trip("path_lstat")),
        mock.patch.object(Path, "open", side_effect=trip("path_open")),
        mock.patch.object(Path, "write_bytes", side_effect=trip("path_write_bytes")),
        mock.patch.object(Path, "write_text", side_effect=trip("path_write_text")),
        mock.patch("tempfile.mkstemp", side_effect=trip("mkstemp")),
        mock.patch("tempfile.NamedTemporaryFile", side_effect=trip("named_temp")),
    ):
        for produce in (False, True):
            try:
                _blocked_candidate_entry("/must/not/be/inspected", produce)
            except ContractBlocked as exc:
                need(str(exc) == CANDIDATE_BLOCK_REASON, "candidate refusal reason")
            else:
                raise AssertionError("candidate entry accepted")
    need(all(value == 0 for value in counters.values()), "candidate zero filesystem calls")
    return counters


def self_test() -> dict[str, Any]:
    document = _contract_document()
    validate_contract(document)
    raw = canonical_bytes(document)
    need(canonical_bytes(json.loads(raw)) == raw, "canonical round trip")
    need(digest(document) == hashlib.sha256(raw).hexdigest(), "digest stability")

    rejected: list[str] = []
    for label, mutate in _semantic_mutations():
        candidate = copy.deepcopy(document)
        mutate(candidate)
        try:
            validate_contract(candidate)
        except ContractBlocked:
            rejected.append(label)
        else:
            raise AssertionError("semantic mutation accepted:" + label)
    need(len(rejected) == len(_semantic_mutations()), "mutation rejection total")

    boundary = _boundary_probe()
    return {
        "schema": SCHEMA + ".self-test.v1",
        "status": "PASS",
        "canonical_contract_digest_sha256": digest(document),
        "semantic_mutation_count": len(rejected),
        "semantic_mutations_rejected": len(rejected),
        "delta_items_covered": list(DELTA_ITEMS),
        "candidate_and_production_refusals": 2,
        "filesystem_boundary_call_counts": boundary,
        "formal_credit": 0,
    }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--print-contract", action="store_true")
    modes.add_argument("--self-test", action="store_true")
    modes.add_argument("--verify-dependencies", action="store_true")
    modes.add_argument("--candidate-output", metavar="PATH")
    modes.add_argument("--produce", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if args.candidate_output is not None or args.produce:
        try:
            _blocked_candidate_entry(args.candidate_output, args.produce)
        except ContractBlocked:
            return 1
        raise AssertionError("unreachable candidate mode")
    if args.print_contract:
        print(canonical_bytes(contract_envelope()).decode("ascii"))
        return 0
    if args.self_test:
        print(canonical_bytes(self_test()).decode("ascii"))
        return 0
    if args.verify_dependencies:
        print(canonical_bytes(verify_dependencies()).decode("ascii"))
        return 0
    raise AssertionError("unreachable CLI mode")


if __name__ == "__main__":
    raise SystemExit(main())
