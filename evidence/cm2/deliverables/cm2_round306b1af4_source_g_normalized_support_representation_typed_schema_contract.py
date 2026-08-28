#!/usr/bin/env python3
"""Zero-credit typed schema contract for Round306B1A normalized support.

This file is deliberately inert.  It freezes the type, row, authority-role,
and census rules needed by a future producer and an independent verifier.  It
does not load construction data, emit a candidate package, or grant theorem
credit.  The final Round306B1AF3D1 and symbolic-kernel source bytes are pinned
exactly and may be verified only through the explicit raw-byte verification
mode; normal contract printing and self-test remain filesystem-inert.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
from pathlib import Path
import stat
import tempfile
from typing import Any, Callable, Final
from unittest import mock


class ContractBlocked(RuntimeError):
    """Fail-closed schema, dependency, or candidate-mode violation."""


def need(condition: bool, label: str) -> None:
    if not condition:
        raise ContractBlocked(label)


SCHEMA: Final = (
    "cm2.round306b1af4.source-g-normalized-support-representation-"
    "typed-schema-contract.v1"
)
STATUS: Final = (
    "PASS_SEALED_ZERO_CREDIT_TYPED_SCHEMA__CONSTRUCTOR_AND_FORMAL_B1A_STILL_BLOCKED"
)
CANDIDATE_BLOCK_REASON: Final = (
    "Round306B1AF4 is a sealed, non-producing zero-credit schema contract; "
    "candidate and producer modes are blocked before path lstat/open/temp/write"
)

DEPENDENCY_DIRECTORY: Final = Path(__file__).parent
DEPENDENCY_PINS: Final = (
    {
        "label": "Round306B1AF3D1",
        "filename": "cm2_round306b1af3d1_source_g_support_representation_authority_delta_contract.py",
        "exact_size": 57_389,
        "source_sha256": "d61fbdc7e6d917c9c451cf63a7640285e900fd08dff76800119ca60ae5e55138",
        "canonical_document_sha256": "a6583a82084b764258c9e8530026b94ec772123e57a62335b1f1b85447be4810",
        "canonical_payload_sha256": "bc8c29784d844294fff77785ebb84bb654eb750bf0f87330f325abfa027e18c1",
        "file_catalog_sha256": "3e5b33d543839b6a0b9352f76e6a14846c80fc547a723c9297deb1ec9952c0ce",
        "table_catalog_sha256": "d91e7e999f7a73e35c6718aa2c36a3af84ea9e018fdf2d305f4fc0dbd9841724",
        "role_catalog_sha256": "ae891a3c915b99eb06335846213ac68980f29342568a2c45fb2d98218e87c336",
        "printed_contract_stdout_size": 20_183,
        "printed_contract_stdout_sha256": "c1cbce1028df9d90e620dba24d4a52292a427622e20b5a1094d6e2f39d2a1c82",
        "verification_digest_sha256": "1dc9f735a460844c6292e45320caf4e2d1f77c8b3e1fb61986a4013003c48dc0",
    },
    {
        "label": "Round306B1AF4_SYMBOLIC_KERNEL",
        "filename": "cm2_round306b1af4_source_g_normalized_support_symbolic_kernel.py",
        "exact_size": 87_237,
        "source_sha256": "c8bb9cf85aace782639859c33625732bf866a7fad34ff31cce58ab84af9f6a6f",
        "kernel_digest_sha256": "1cfe83e756fec2876500e441de2b0ce06962068fa9b3460151463175cc485d51",
        "printed_contract_stdout_size": 8_942,
        "printed_contract_stdout_sha256": "ba08acd1f07ea6941b66b831575c03707ed5d96b1b55792ad177e2642c8e22fb",
        "self_test_stdout_size": 880,
        "self_test_stdout_sha256": "68b21dd59dd03c91e3a3ebe1876698bd9c8da4a9182a0727e72f5f4bb3e21f6e",
        "self_test_digest_sha256": "f8207c2c82033486ea2e507a66713739b8e8052a2991d300280a8e2b59378b7e",
    },
)

MEMBER_COUNT: Final = 564_492
REPRESENTATION_COUNT: Final = 611_904
THEOREM_OBLIGATION_COUNT: Final = 824_864
ROOT_OBLIGATION_COUNT: Final = 351_904
DEPENDENT_OBLIGATION_COUNT: Final = 472_960
A1_COUNT: Final = 17_940
A2_COUNT: Final = 62_152

COORDINATE_PARAMETERS: Final = ("TPS", "T2PS")
REPRESENTATION_COORDINATE_SYSTEMS: Final = (
    "TPS",
    "T2PS",
    "VIRTUAL_P3D",
    "VIRTUAL_SHEET",
)

BASELINE_OPERATORS: Final = (
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

MACRO_LOWERING_ORDER: Final = (
    "OPEN_RATIONAL_BOX",
    "STRICT_SIGN_CELL",
    "FINITE_DISJOINT_UNION",
    "BOUNDARY_RESTRICTION",
    "CHART_PULLBACK",
    "TPS_DOMAIN",
    "SOURCE_G_FIRST_HIT_MAP",
    "WALL_ENDPOINT_FACTOR",
    "OUTGOING_DIAGONAL_FACTOR",
    "IMPLICIT_REGULAR_GRAPH",
    "SHEET_MEMBER_EQUIVALENCE",
    "BOUNDARY_TRACE_INCIDENCE",
    "HALF_OPEN_BOUNDARY_ASSIGNMENT",
)

# This allowlist is byte-for-byte aligned with the separately implemented AF4
# symbolic kernel.  The old AF0 six-ID bundle is not an admissible substitute.
PROOF_KERNEL_IDS: Final = (
    "EXACT_RATIONAL_AST_NORMALIZATION_V2",
    "DIRECTED_RATIONAL_INTERVAL_SIGN_V1",
    "POSITIVE_SQRT_INTERVAL_V1",
    "PREDICATE_CELL_EQUIVALENCE_V1",
    "MONOTONE_GRAPH_EXISTENCE_UNIQUENESS_V1",
    "DEPENDENT_INCIDENCE_RESTRICTION_V1",
    "FINITE_HALF_OPEN_SUPPORT_UNION_V1",
    "ARTIFICIAL_FACE_REGLUE_V1",
    "FIXED_SIGN_T2PS_PULLBACK_V1",
    "REPRESENTATION_OWNER_BACKBINDING_V1",
    "SHEET_MEMBER_EQUIVALENCE_V1",
    "BOUNDARY_TRACE_PHYSICAL_INCIDENCE_V1",
    "SOURCE_LINEAGE_EXHAUSTION_V1",
)

AF0_PROOF_KERNEL_BUNDLE: Final = (
    "EXACT_RATIONAL_AST_NORMALIZATION_V1",
    "DIRECTED_INTERVAL_SIGN_CERTIFICATE_V1",
    "PREDICATE_CELL_EQUIVALENCE_V1",
    "DEPENDENT_INCIDENCE_RESTRICTION_V1",
    "FINITE_DISJOINT_SUPPORT_UNION_V1",
    "GRAPH_SHEET_PHYSICAL_INCIDENCE_V1",
)

# Two stable names are intentionally retained by AF4; the other AF0-only IDs
# are forbidden.  The AF0 bundle as a whole is never accepted as an allowlist.
AF0_RETAINED_KERNEL_IDS: Final = (
    "PREDICATE_CELL_EQUIVALENCE_V1",
    "DEPENDENT_INCIDENCE_RESTRICTION_V1",
)
AF0_LEGACY_ONLY_FORBIDDEN_KERNEL_IDS: Final = (
    "EXACT_RATIONAL_AST_NORMALIZATION_V1",
    "DIRECTED_INTERVAL_SIGN_CERTIFICATE_V1",
    "FINITE_DISJOINT_SUPPORT_UNION_V1",
    "GRAPH_SHEET_PHYSICAL_INCIDENCE_V1",
)

AF2_FAMILY_COUNTS: Final = (
    ("PRESERVED", 126_468),
    ("R2", 295_336),
    ("R292", 9_404),
    ("G2A", 38_624),
    ("G2B", 76_832),
    ("NON_GRAPH_BULK", 17_828),
)

REPRESENTATION_ROLE_COUNTS: Final = (
    ("PRIMARY", 564_492),
    ("REFINED_PRIMARY_EXTRA", 848),
    ("ALIAS_EXISTING_MEMBER", 46_564),
)

REPRESENTATION_COORDINATE_COUNTS: Final = (
    ("TPS", 466_768),
    ("T2PS", 11_852),
    ("VIRTUAL_P3D", 94_660),
    ("VIRTUAL_SHEET", 38_624),
)

REPRESENTATION_CROSS_COUNTS: Final = (
    ("PRIMARY", "TPS", 421_804),
    ("PRIMARY", "T2PS", 9_404),
    ("PRIMARY", "VIRTUAL_P3D", 94_660),
    ("PRIMARY", "VIRTUAL_SHEET", 38_624),
    ("REFINED_PRIMARY_EXTRA", "T2PS", 848),
    ("ALIAS_EXISTING_MEMBER", "T2PS", 1_600),
    ("ALIAS_EXISTING_MEMBER", "TPS", 44_964),
)

ROW_SCHEMA_ORDER: Final = (
    "feature",
    "member",
    "representation",
    "incidence",
    "transition_handle",
    "gap",
)


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


def _contains_null(value: Any) -> bool:
    if value is None:
        return True
    if isinstance(value, dict):
        return any(_contains_null(item) for item in value.values())
    if isinstance(value, (list, tuple)):
        return any(_contains_null(item) for item in value)
    return False


def _sort_contract() -> dict[str, Any]:
    return {
        "coordinate_parameters": list(COORDINATE_PARAMETERS),
        "sorts": {
            "QExpr<TPS|T2PS>": {
                "kind": "EXACT_RATIONAL_SCALAR_EXPRESSION",
                "coordinate_parameter_must_be_one_of": list(COORDINATE_PARAMETERS),
                "nonrational_operations_require_side_conditions": [
                    "DIV_NONZERO",
                    "SQRT_POSITIVE",
                ],
            },
            "BoolPred<C>": {
                "kind": "TYPED_BOOLEAN_PREDICATE",
                "parameter": "C",
                "C_must_be_one_of": list(COORDINATE_PARAMETERS),
                "predicate_result_is_not_a_support_theorem": True,
            },
            "OpenBox<C>": {
                "kind": "STRICT_OPEN_RATIONAL_BOX",
                "parameter": "C",
                "lower_and_upper_bounds_are_CONST_Q": True,
                "all_bounds_strict": True,
            },
            "ChartMap<src,dst>": {
                "kind": "TYPED_PARTIAL_CHART_MAP",
                "parameters": ["src", "dst"],
                "domain_predicate_required": True,
                "component_QExpr_count_matches_dst": True,
            },
            "FeatureDef<C>": {
                "kind": "SOURCE_FREE_EVALUABLE_FEATURE_DEFINITION",
                "parameter": "C",
                "definition_BoolPred_required": True,
                "source_label_alone_is_definition": False,
            },
            "FiniteCellUnion<C>": {
                "kind": "FINITE_PAIRWISE_INTERIOR_DISJOINT_UNION",
                "parameter": "C",
                "cell_ids_nonempty_and_canonically_sorted": True,
                "boundary_assignment_certificate_required": True,
            },
            "PullbackCert<src,dst>": {
                "kind": "EXACT_SUPPORT_PULLBACK_EQUIVALENCE_CERTIFICATE",
                "parameters": ["src", "dst"],
                "forward_map_required": True,
                "inverse_branch_required": True,
                "set_equality_not_subset_required": True,
            },
            "PhysicalFace<C>": {
                "kind": "PHYSICAL_BOUNDARY_FACE_DEFINITION",
                "parameter": "C",
                "ambient_feature_backbinding_required": True,
                "incidence_is_not_identifier_adjacency": True,
            },
        },
        "representation_coordinate_systems": list(REPRESENTATION_COORDINATE_SYSTEMS),
        "representation_AST_coordinate_parameter": {
            "TPS": "TPS",
            "T2PS": "T2PS",
            "VIRTUAL_P3D": "TPS",
            "VIRTUAL_SHEET": "TPS",
        },
        "implicit_coercions_forbidden": True,
        "coordinate_parameter_erasure_forbidden": True,
    }


def _macro_contract() -> dict[str, Any]:
    return {
        "lowering_order": list(MACRO_LOWERING_ORDER),
        "macros_are_not_stored_AST_operators": True,
        "all_macros_must_be_lowered_before_row_hash": True,
        "lowerings": {
            "OPEN_RATIONAL_BOX": {
                "input": "six ordered CONST_Q bounds in TPS or T2PS",
                "output": "AND of strict lower/upper LT_ZERO atoms",
                "requires": ["lower_bound_strictly_less_than_upper_bound"],
            },
            "STRICT_SIGN_CELL": {
                "input": "OpenBox<C> plus finitely many signed QExpr<C>",
                "output": "AND(box predicate, LT_ZERO/GT_ZERO sign atoms)",
                "carrier_box_alone_is_not_the_cell": True,
            },
            "FINITE_DISJOINT_UNION": {
                "input": "canonically ordered nonempty FeatureDef<C> list",
                "output": "OR_DISJOINT",
                "requires": [
                    "pairwise_interior_disjoint_certificate",
                    "exhaustive_union_certificate",
                ],
            },
            "BOUNDARY_RESTRICTION": {
                "input": "FeatureDef<C> and PhysicalFace<C>",
                "output": "RESTRICT",
                "requires": ["dependent_root_backbinding"],
            },
            "CHART_PULLBACK": {
                "input": "ChartMap<src,dst>, BoolPred<dst>, PullbackCert<src,dst>",
                "output": "BoolPred<src>",
                "requires": ["exact_forward_inverse_set_equality"],
            },
            "TPS_DOMAIN": {
                "input": "exact t,p,s bounds and chart identifier",
                "output": "OpenBox<TPS>",
                "chart_identifier_is_metadata_not_a_predicate": True,
            },
            "SOURCE_G_FIRST_HIT_MAP": {
                "input": "TPS source chart, target obstacle constants, strict radical domain",
                "output": "ChartMap<TPS,TPS>",
                "allowed_nonpolynomial_node": "SQRT_POSITIVE",
                "radical_positivity_certificate_required": True,
            },
            "WALL_ENDPOINT_FACTOR": {
                "input": "source wall axis and integer wall",
                "output": "QExpr<TPS>",
                "round204_source_factor_normal_form": "(9/25)*t",
            },
            "OUTGOING_DIAGONAL_FACTOR": {
                "input": "SOURCE_G_FIRST_HIT_MAP normal components",
                "output": "QExpr<TPS>",
                "branches": ["HPLUS=Nx+Ny", "HMINUS=Nx-Ny"],
            },
            "IMPLICIT_REGULAR_GRAPH": {
                "input": "EQ_ZERO(f) plus strict derivative sign certificate",
                "output": "FeatureDef<C>",
                "name_or_method_string_alone_is_forbidden": True,
            },
            "SHEET_MEMBER_EQUIVALENCE": {
                "input": "graph definition, sheet member support, chart map",
                "output": "PullbackCert<src,dst>",
                "identifier_join_alone_is_forbidden": True,
            },
            "BOUNDARY_TRACE_INCIDENCE": {
                "input": "ambient FeatureDef<C> and restricted PhysicalFace<C>",
                "output": "dependent incidence theorem",
                "physical_trace_required": True,
            },
            "HALF_OPEN_BOUNDARY_ASSIGNMENT": {
                "input": "owner/shadow traces on a common boundary",
                "output": "pairwise-disjoint exhaustive assignment certificate",
                "owner_label_alone_is_forbidden": True,
            },
        },
    }


def _proof_kernel_contract() -> dict[str, Any]:
    """Exact AF4 kernel allowlist, wire shapes, and typed field routing."""

    shapes = {
        "EXACT_RATIONAL_AST_NORMALIZATION_V2": {
            "premises": {"input_ast": "ANY_AST"},
            "evidence": {"normalization_rule_ids": "STR_LIST"},
            "conclusion": {
                "normalized_ast": "ANY_AST",
                "normalized_sha256": "SHA256",
            },
        },
        "DIRECTED_RATIONAL_INTERVAL_SIGN_V1": {
            "premises": {
                "scalar_ast": "SCALAR_AST",
                "variable_intervals": "INTERVAL_MAP",
            },
            "evidence": {
                "precision_bits": "SQRT_BITS",
                "rounding_mode": "LITERAL:OUTWARD_EXACT_RATIONAL",
                "subdivision_path": "STR_LIST",
            },
            "conclusion": {"interval": "INTERVAL", "sign": "SIGN"},
        },
        "POSITIVE_SQRT_INTERVAL_V1": {
            "premises": {"radicand_interval": "INTERVAL"},
            "evidence": {
                "method": "LITERAL:INTEGER_SQUARE_BRACKETING",
                "precision_bits": "SQRT_BITS",
            },
            "conclusion": {"sqrt_interval": "INTERVAL"},
        },
        "PREDICATE_CELL_EQUIVALENCE_V1": {
            "premises": {
                "domain": "PREDICATE_AST",
                "left_predicate": "PREDICATE_AST",
                "right_predicate": "PREDICATE_AST",
            },
            "evidence": {
                "cell_ids": "STR_LIST",
                "forward_certificate_ids": "STR_LIST",
                "reverse_certificate_ids": "STR_LIST",
            },
            "conclusion": {"equivalence_claim": "BOOL_TRUE"},
        },
        "MONOTONE_GRAPH_EXISTENCE_UNIQUENESS_V1": {
            "premises": {
                "derivative_ast": "SCALAR_AST",
                "domain": "PREDICATE_AST",
                "equation_ast": "SCALAR_AST",
            },
            "evidence": {
                "base_variables": "STR_LIST",
                "derivative_sign": "STRICT_SIGN",
                "face_signs": "STR_MAP",
                "graph_variable": "STR",
                "interval_cell_ids": "STR_LIST",
            },
            "conclusion": {
                "existence_claim": "BOOL_TRUE",
                "uniqueness_claim": "BOOL_TRUE",
            },
        },
        "DEPENDENT_INCIDENCE_RESTRICTION_V1": {
            "premises": {
                "boundary": "PREDICATE_AST",
                "dependent_support": "PREDICATE_AST",
                "root_support": "PREDICATE_AST",
            },
            "evidence": {
                "orientation": "ORIENTATION",
                "restriction_ast": "PREDICATE_AST",
                "trace_certificate_ids": "STR_LIST",
            },
            "conclusion": {"exact_restriction_claim": "BOOL_TRUE"},
        },
        "FINITE_HALF_OPEN_SUPPORT_UNION_V1": {
            "premises": {"pieces": "PREDICATE_LIST"},
            "evidence": {
                "owner_rule_ids": "STR_LIST",
                "pairwise_disjoint_certificate_ids": "STR_LIST",
                "piece_ids": "STR_LIST",
            },
            "conclusion": {
                "complete_claim": "BOOL_TRUE",
                "support": "PREDICATE_AST",
            },
        },
        "ARTIFICIAL_FACE_REGLUE_V1": {
            "premises": {
                "common_face": "PREDICATE_AST",
                "left_cell": "PREDICATE_AST",
                "right_cell": "PREDICATE_AST",
            },
            "evidence": {
                "left_trace_sha256": "SHA256",
                "owner_rule_id": "STR",
                "right_trace_sha256": "SHA256",
            },
            "conclusion": {
                "no_duplicate_claim": "BOOL_TRUE",
                "reglued_support": "PREDICATE_AST",
            },
        },
        "FIXED_SIGN_T2PS_PULLBACK_V1": {
            "premises": {
                "sigma": "SIGMA",
                "t_ast": "SCALAR_AST",
                "u_ast": "SCALAR_AST",
            },
            "evidence": {
                "substitution_variable": "STR",
                "u_positive_certificate_id": "STR",
            },
            "conclusion": {"pullback_predicate": "PREDICATE_AST"},
        },
        "REPRESENTATION_OWNER_BACKBINDING_V1": {
            "premises": {
                "member_support": "PREDICATE_AST",
                "representation_support": "PREDICATE_AST",
            },
            "evidence": {
                "member_id": "STR",
                "owner_id": "STR",
                "representation_id": "STR",
                "source_join_id": "STR",
            },
            "conclusion": {"supports_equal_claim": "BOOL_TRUE"},
        },
        "SHEET_MEMBER_EQUIVALENCE_V1": {
            "premises": {
                "graph_support": "PREDICATE_AST",
                "sheet_support": "PREDICATE_AST",
            },
            "evidence": {
                "forward_certificate_ids": "STR_LIST",
                "graph_id": "STR",
                "member_id": "STR",
                "reverse_certificate_ids": "STR_LIST",
            },
            "conclusion": {"sets_equal_claim": "BOOL_TRUE"},
        },
        "BOUNDARY_TRACE_PHYSICAL_INCIDENCE_V1": {
            "premises": {
                "boundary": "PREDICATE_AST",
                "graph_support": "PREDICATE_AST",
                "side_support": "PREDICATE_AST",
            },
            "evidence": {
                "incidence_id": "STR",
                "orientation": "ORIENTATION",
                "trace_certificate_ids": "STR_LIST",
            },
            "conclusion": {"exact_physical_incidence_claim": "BOOL_TRUE"},
        },
        "SOURCE_LINEAGE_EXHAUSTION_V1": {
            "premises": {
                "join_ids": "STR_LIST",
                "member_ids": "STR_LIST",
                "source_ids": "STR_LIST",
            },
            "evidence": {
                "exhaustiveness_sha256": "SHA256",
                "join_count": "NONNEG_INT",
                "member_count": "NONNEG_INT",
                "source_count": "NONNEG_INT",
            },
            "conclusion": {
                "duplicate_count": "ZERO",
                "missing_count": "ZERO",
                "orphan_count": "ZERO",
            },
        },
    }
    return {
        "allowlist": list(PROOF_KERNEL_IDS),
        "allowlist_is_exact_and_closed": True,
        "unlisted_kernel_ids_rejected": True,
        "AF0_legacy_bundle": {
            "ids": list(AF0_PROOF_KERNEL_BUNDLE),
            "bundle_accepted_as_AF4_allowlist": False,
            "legacy_only_forbidden_ids": list(AF0_LEGACY_ONLY_FORBIDDEN_KERNEL_IDS),
            "stable_names_retained_in_AF4": list(AF0_RETAINED_KERNEL_IDS),
            "retained_names_do_not_authorize_the_AF0_bundle": True,
        },
        "wire_shapes": shapes,
        "typed_certificate_field_allowlists": {
            "feature.proof_kernel_id": [
                "EXACT_RATIONAL_AST_NORMALIZATION_V2",
                "DIRECTED_RATIONAL_INTERVAL_SIGN_V1",
                "POSITIVE_SQRT_INTERVAL_V1",
                "PREDICATE_CELL_EQUIVALENCE_V1",
                "MONOTONE_GRAPH_EXISTENCE_UNIQUENESS_V1",
                "DEPENDENT_INCIDENCE_RESTRICTION_V1",
                "SHEET_MEMBER_EQUIVALENCE_V1",
            ],
            "member.finite_support_union_certificate.kernel_id": [
                "FINITE_HALF_OPEN_SUPPORT_UNION_V1",
                "ARTIFICIAL_FACE_REGLUE_V1",
                "PREDICATE_CELL_EQUIVALENCE_V1",
            ],
            "member.source_lineage_certificate.kernel_id": [
                "SOURCE_LINEAGE_EXHAUSTION_V1",
            ],
            "representation.pullback_certificate.kernel_ids": [
                "FIXED_SIGN_T2PS_PULLBACK_V1",
                "REPRESENTATION_OWNER_BACKBINDING_V1",
                "PREDICATE_CELL_EQUIVALENCE_V1",
            ],
            "incidence.proof_kernel_id": [
                "DEPENDENT_INCIDENCE_RESTRICTION_V1",
                "SHEET_MEMBER_EQUIVALENCE_V1",
                "BOUNDARY_TRACE_PHYSICAL_INCIDENCE_V1",
            ],
            "gap.blocking_verification_kernel_id": [
                "SOURCE_LINEAGE_EXHAUSTION_V1",
            ],
        },
    }


def _row_schemas() -> dict[str, Any]:
    common_source_binding_fields = [
        "authority",
        "authority_role",
        "filename",
        "file_sha256",
        "json_path",
        "row_id",
        "row_sha256_or_table_position_commitment",
    ]
    return {
        "feature": {
            "row_type": "FeatureDef<C>",
            "required_fields": [
                "schema",
                "Round306B1AF4_feature_row_id",
                "coordinate_parameter",
                "node_id",
                "family",
                "obligation_role",
                "natural_key",
                "definition_ast",
                "coordinate_domain_ast",
                "ast_normal_form_sha256",
                "source_bindings",
                "proof_kernel_id",
                "equivalence_or_dependency_certificate",
                "formal_feature_definition_credit",
                "row_sha256",
            ],
            "source_binding_required_fields": common_source_binding_fields,
            "proof_kernel_id_must_be_one_of": _proof_kernel_contract()[
                "typed_certificate_field_allowlists"
            ]["feature.proof_kernel_id"],
            "root_definition_independently_evaluable": True,
            "dependent_definition_requires_root_row_ids": True,
            "official_key_and_return_signature_are_metadata_only": True,
            "row_id_rule": (
                "round306b1af4-feature:SHA256(canonical([coordinate_parameter,"
                "node_id,family,natural_key]))"
            ),
        },
        "member": {
            "row_type": "FiniteCellUnion<C>",
            "required_fields": [
                "schema",
                "Round306B1AF4_member_row_id",
                "B0_member_id",
                "AF2_family",
                "B0_component_id_metadata_only",
                "primary_representation_row_id",
                "support_feature_row_ids",
                "normalized_full_support_ast",
                "finite_support_union_certificate",
                "source_lineage_certificate",
                "boundary_assignment_certificate",
                "source_bindings",
                "formal_member_support_credit",
                "row_sha256",
            ],
            "one_and_only_one_row_per_B0_member": True,
            "finite_support_union_kernel_ids_must_be_one_of":
                _proof_kernel_contract()["typed_certificate_field_allowlists"][
                    "member.finite_support_union_certificate.kernel_id"
                ],
            "source_lineage_kernel_ids_must_be_one_of":
                _proof_kernel_contract()["typed_certificate_field_allowlists"][
                    "member.source_lineage_certificate.kernel_id"
                ],
            "support_feature_rows_nonempty": True,
            "support_union_equals_member_support": True,
            "carrier_or_witness_subset_is_not_equality": True,
            "row_id_rule": (
                "round306b1af4-member:SHA256(canonical(B0_member_id))"
            ),
        },
        "representation": {
            "row_type": "PullbackCert<src,dst>",
            "required_fields": [
                "schema",
                "Round306B1AF4_representation_row_id",
                "B0_member_id",
                "representation_role",
                "representation_source_round",
                "coordinate_system",
                "coordinate_parameter",
                "representation_source_id",
                "carrier_ast",
                "support_pullback_ast",
                "forward_chart_map_ast",
                "inverse_branch_ast",
                "pullback_certificate",
                "feature_row_ids",
                "transition_handle_row_ids",
                "source_bindings",
                "mints_member_identity",
                "formal_representation_cover_credit",
                "row_sha256",
            ],
            "roles": [name for name, _ in REPRESENTATION_ROLE_COUNTS],
            "coordinate_systems": list(REPRESENTATION_COORDINATE_SYSTEMS),
            "pullback_certificate_kernel_ids_must_be_one_of":
                _proof_kernel_contract()["typed_certificate_field_allowlists"][
                    "representation.pullback_certificate.kernel_ids"
                ],
            "forward_inverse_domain_and_set_equality_required": True,
            "subset_or_outer_envelope_alone_is_forbidden": True,
            "mints_member_identity_must_equal": False,
            "row_id_rule": (
                "round306b1af4-representation:SHA256(canonical([B0_member_id,"
                "representation_role,coordinate_system,representation_source_id]))"
            ),
        },
        "incidence": {
            "row_type": "PhysicalFace<C>",
            "required_fields": [
                "schema",
                "Round306B1AF4_incidence_row_id",
                "incidence_family",
                "ambient_feature_row_id",
                "dependent_feature_row_id",
                "physical_face_ast",
                "restriction_ast",
                "owner_member_row_id",
                "shadow_member_row_ids",
                "physical_trace_certificate",
                "half_open_assignment_certificate",
                "source_bindings",
                "proof_kernel_id",
                "formal_physical_incidence_credit",
                "row_sha256",
            ],
            "proof_kernel_id_must_be_one_of": _proof_kernel_contract()[
                "typed_certificate_field_allowlists"
            ]["incidence.proof_kernel_id"],
            "identifier_adjacency_is_not_physical_incidence": True,
            "owner_shadow_assignment_disjoint_and_exhaustive": True,
            "root_backbinding_required": True,
        },
        "transition_handle": {
            "row_type": "TYPED_TRANSITION_READY_HANDLE",
            "required_fields": [
                "schema",
                "Round306B1AF4_transition_handle_row_id",
                "B0_member_id",
                "representation_row_id",
                "local_face_id",
                "physical_face_ast",
                "chart_side",
                "owner_status",
                "incidence_row_ids",
                "source_bindings",
                "transition_class_metadata_only",
                "formal_transition_credit",
                "row_sha256",
            ],
            "transition_atlas_completeness_claimed": False,
            "pair_routing_claimed": False,
            "handle_is_not_a_transition_theorem": True,
        },
        "gap": {
            "row_type": "FAIL_CLOSED_GAP",
            "required_fields": [
                "schema",
                "Round306B1AF4_gap_row_id",
                "gap_family",
                "blocked_natural_key",
                "source_bindings",
                "reason",
                "blocking_verification_kernel_id",
                "formal_credit",
                "row_sha256",
            ],
            "formal_PASS_gap_count_must_equal": 0,
            "blocking_verification_kernel_id_must_be_one_of":
                _proof_kernel_contract()["typed_certificate_field_allowlists"][
                    "gap.blocking_verification_kernel_id"
                ],
            "missing_AST_equivalence_pullback_incidence_or_binding_is_gap": True,
            "gap_may_not_be_forced_to_PASS": True,
        },
    }


def _family_contracts() -> list[dict[str, Any]]:
    return [
        {
            "family": "PRESERVED",
            "member_count": 126_468,
            "fine_partition": {
                "R174_RESOLVED_OPEN_BOX": 72_500,
                "R179_RESOLVED_OPEN_BOX": 17_192,
                "R204_STRICT_CURVED_SIGN_CELL": 736,
                "R208_FACTORIZED_STRICT_SIGN_CELL": 36_040,
            },
            "count_equation": "72500+17192+736+36040=126468",
            "required_semantics": [
                "B0_TO_R294_TO_R266_TO_SOURCE_GEOMETRY_ID_AND_SHA",
                "R174_R179_OPEN_BOX_EQUALS_PHYSICAL_SUPPORT",
                "R204_LEAF_BOX_INTERSECT_SOURCE_AND_TARGET_STRICT_SIGNS",
                "R208_LEAF_BOX_INTERSECT_F_HPLUS_HMINUS_STRICT_SIGNS",
                "CHART_PULLBACK_AND_BOUNDARY_ASSIGNMENT_COMPLETE",
            ],
            "forbidden_substitutions": [
                "R204_OR_R208_LEAF_CARRIER_BOX_AS_FULL_SUPPORT",
                "OFFICIAL_KEY_OR_RETURN_SIGNATURE_AS_SET_DEFINITION",
            ],
        },
        {
            "family": "R2",
            "member_count": 295_336,
            "source_cell_count": 295_340,
            "member_union_cell_count_histogram": {"1": 295_332, "2": 4},
            "count_equation": "295332*1+4*2=295340_cells_for_295336_members",
            "required_semantics": [
                "SOURCE_FREE_R269_R270_R271_R272_PREDICATE_AST",
                "EXACT_FINITE_DISJOINT_MEMBER_UNION",
            ],
            "forbidden_substitutions": [
                "R290_DIAGNOSTIC_INNER_WITNESS_AS_FULL_SUPPORT",
                "B1R0_INVENTORY_LABEL_AS_DEFINITION",
            ],
        },
        {
            "family": "R292",
            "member_count": 9_404,
            "uncovered_exact_T2PS_cell_count": 10_252,
            "local_connectivity_rank": 848,
            "count_equation": "10252-848=9404",
            "required_semantics": [
                "EXACT_T2PS_CELL_AST",
                "CONNECTED_CELL_UNION_EQUALS_MEMBER_SUPPORT",
                "TPS_T2PS_PULLBACK_WITH_EXPLICIT_INVERSE_BRANCH",
            ],
            "forbidden_substitutions": [
                "R287_OUTER_ENVELOPE_AS_INNER_OR_FULL_SUPPORT",
            ],
        },
        {
            "family": "G2A",
            "member_count": 38_624,
            "fine_partition": {"R245_SHEET": 264, "R248_SHEET": 38_360},
            "count_equation": "264+38360=38624",
            "required_semantics": [
                "ONE_SOURCE_FREE_GRAPH_DEFINITION_PER_SHEET",
                "SHEET_MEMBER_EQUIVALENCE_NOT_IDENTIFIER_JOIN",
                "HALF_OPEN_OWNER_ASSIGNMENT",
            ],
        },
        {
            "family": "G2B",
            "member_count": 76_832,
            "incidence_reference_count": 76_848,
            "fine_partition": {
                "R235_REFERENCE_AND_MEMBER_COUNT": 76_256,
                "R236_REFERENCE_COUNT": 64,
                "R236_DISTINCT_MEMBER_COUNT": 48,
                "R242_REFERENCE_AND_MEMBER_COUNT": 528,
            },
            "count_equations": [
                "76256+64+528=76848_references",
                "76256+48+528=76832_distinct_members",
            ],
            "required_semantics": [
                "GRAPH_SIDE_PHYSICAL_INCIDENCE_CERTIFICATE",
                "REFERENCE_MULTIPLICITY_PRESERVED",
                "REFERENCE_COUNT_NOT_EQUAL_TO_MEMBER_COUNT",
            ],
        },
        {
            "family": "NON_GRAPH_BULK",
            "member_count": 17_828,
            "fine_partition": {
                "R245_WHOLE_ROOT_ZERO_ABSENCE": 2_872,
                "R246_WHOLE_ORIGIN": 2_220,
                "R247_CROSSING_OR_SOURCE_SEAM": 504,
                "R248_R234_RESOLVED_DESCENDANT": 12_200,
                "R248_R236_CROSSING_DISCHARGE": 32,
            },
            "count_equations": [
                "2872+2220+504+12200+32=17828",
                "88936-400_R264_empty-76304_graph_side=12232_R248_non_graph",
            ],
            "required_semantics": [
                "R245_WHOLE_ROOT_REPLAYS_R242_EXHAUSTIVE_ZERO_ABSENCE",
                "R246_REPLAYS_R232_AND_R179_RETAINED_CHILD",
                "R247_CROSSING_USES_WHOLE_RETAINED_BOX",
                "R247_SOURCE_SEAM_USES_RETAINED_BOX_INTERSECT_2T2_MINUS_1_LT_ZERO",
                "R248_REBINDS_COMPLETE_SIGNATURE_FROM_R234_OR_R236",
            ],
            "forbidden_substitutions": [
                "R245_R246_WITNESS_LABEL_AS_EQUALITY_THEOREM",
                "R247_SOURCE_SEAM_DYADIC_CORRIDOR_AS_FULL_SUPPORT",
                "R248_SIGNATURE_SHA_WITHOUT_SIGNATURE_BODY_BACKBINDING",
            ],
        },
    ]


def _authority_roles() -> dict[str, Any]:
    return {
        "precedence_high_to_low": [
            "SUPPORT_ROW_SOURCE",
            "ANALYTIC_LINEAGE",
            "CONSTRUCTION_LINEAGE",
            "IDENTITY_BINDING",
            "PROOF_EVIDENCE",
            "OUTER_ENVELOPE_ONLY",
            "DIAGNOSTIC_ONLY",
        ],
        "policies": {
            "SUPPORT_ROW_SOURCE": {
                "admitted_for_construction": True,
                "forbidden_as": [
                    "NORMALIZED_FULL_SUPPORT_WITHOUT_TYPED_AST_AND_EQUIVALENCE_CERTIFICATE",
                    "FORMAL_B1A_OR_CM2_CREDIT",
                ],
            },
            "ANALYTIC_LINEAGE": {
                "admitted_for_construction": True,
                "forbidden_as": [
                    "PHYSICAL_SUPPORT_OR_GLUE_WITHOUT_EQUIVALENCE_CERTIFICATE",
                    "NORMALIZED_FULL_SUPPORT",
                    "FORMAL_B1A_OR_CM2_CREDIT",
                ],
            },
            "CONSTRUCTION_LINEAGE": {
                "admitted_for_construction": True,
                "forbidden_as": [
                    "NORMALIZED_FULL_SUPPORT_WITHOUT_TYPED_AST_AND_EQUIVALENCE_CERTIFICATE",
                    "PHYSICAL_INCIDENCE_THEOREM",
                    "FORMAL_B1A_OR_CM2_CREDIT",
                ],
            },
            "IDENTITY_BINDING": {
                "admitted_for_construction": True,
                "forbidden_as": [
                    "NORMALIZED_FULL_SUPPORT",
                    "SUPPORT_GEOMETRY",
                    "PHYSICAL_INCIDENCE_OR_EQUIVALENCE_THEOREM",
                    "FORMAL_B1A_OR_CM2_CREDIT",
                ],
            },
            "PROOF_EVIDENCE": {
                "admitted_for_construction": False,
                "forbidden_as": [
                    "CONSTRUCTION_ROW_SOURCE",
                    "NORMALIZED_FULL_SUPPORT",
                    "MAXIMALITY_OR_CM2_CREDIT",
                ],
            },
            "OUTER_ENVELOPE_ONLY": {
                "admitted_for_construction": False,
                "forbidden_as": [
                    "INNER_SUPPORT",
                    "NORMALIZED_FULL_SUPPORT",
                    "EXISTENCE_OR_EQUIVALENCE_THEOREM",
                ],
            },
            "DIAGNOSTIC_ONLY": {
                "admitted_for_construction": False,
                "forbidden_as": [
                    "CONSTRUCTION_ROW_SOURCE",
                    "NORMALIZED_FULL_SUPPORT",
                    "OUTER_SUPPORT_EQUIVALENCE_CERTIFICATE",
                    "FORMAL_B1A_OR_CM2_CREDIT",
                ],
            },
        },
        "named_evidence_rules": {
            "B0_R266_R294_R264_B1R0_B1G0": "IDENTITY_BINDING_ONLY",
            "R174_R179_RESOLVED_R204_R208": "SUPPORT_ROW_SOURCE_ONLY_UNTIL_EQUIVALENCE",
            "R182_R208_R211_R220_R179_RETAINED_R242_ZERO_ABSENCE": "ANALYTIC_LINEAGE",
            "R232_R234_R236_R237_R238_R242_ROOT_R245_R246_R247_R248_R292": "CONSTRUCTION_LINEAGE",
            "R244_R279_EDGES": "PROOF_EVIDENCE_ONLY",
            "R287": "OUTER_ENVELOPE_ONLY",
            "R290": "DIAGNOSTIC_ONLY_INNER_WITNESS",
            "AF2_PARTITION_LABEL": "SOURCE_FAMILY_CLASSIFICATION_ONLY",
        },
        "outer_envelope_or_inner_witness_may_equal_full_support_without_theorem": False,
        "identity_binding_may_supply_geometry": False,
        "official_key_or_signature_may_define_support": False,
    }


def _sealed_dependency_pins() -> dict[str, Any]:
    return {
        "seal_state": "SEALED_EXACT_TWO_SOURCE_DEPENDENCY_SET",
        "dependency_sources": [dict(row) for row in DEPENDENCY_PINS],
        "dependency_source_count": 2,
        "dependency_source_set_sha256": digest(DEPENDENCY_PINS),
        "Round306B1AF3D1_contract_file_sha256":
            "d61fbdc7e6d917c9c451cf63a7640285e900fd08dff76800119ca60ae5e55138",
        "Round306B1AF3D1_contract_digest_sha256":
            "a6583a82084b764258c9e8530026b94ec772123e57a62335b1f1b85447be4810",
        "Round306B1AF3D1_canonical_payload_sha256":
            "bc8c29784d844294fff77785ebb84bb654eb750bf0f87330f325abfa027e18c1",
        "Round306B1AF3D1_file_catalog_sha256":
            "3e5b33d543839b6a0b9352f76e6a14846c80fc547a723c9297deb1ec9952c0ce",
        "Round306B1AF3D1_table_catalog_sha256":
            "d91e7e999f7a73e35c6718aa2c36a3af84ea9e018fdf2d305f4fc0dbd9841724",
        "Round306B1AF3D1_role_catalog_sha256":
            "ae891a3c915b99eb06335846213ac68980f29342568a2c45fb2d98218e87c336",
        "Round306B1AF3D1_printed_contract_stdout_size": 20_183,
        "Round306B1AF3D1_printed_contract_stdout_sha256":
            "c1cbce1028df9d90e620dba24d4a52292a427622e20b5a1094d6e2f39d2a1c82",
        "Round306B1AF3D1_verification_digest_sha256":
            "1dc9f735a460844c6292e45320caf4e2d1f77c8b3e1fb61986a4013003c48dc0",
        "symbolic_kernel_source_file_sha256":
            "c8bb9cf85aace782639859c33625732bf866a7fad34ff31cce58ab84af9f6a6f",
        "symbolic_kernel_semantics_digest_sha256":
            "1cfe83e756fec2876500e441de2b0ce06962068fa9b3460151463175cc485d51",
        "symbolic_kernel_printed_contract_stdout_size": 8_942,
        "symbolic_kernel_printed_contract_stdout_sha256":
            "ba08acd1f07ea6941b66b831575c03707ed5d96b1b55792ad177e2642c8e22fb",
        "symbolic_kernel_self_test_stdout_size": 880,
        "symbolic_kernel_self_test_stdout_sha256":
            "68b21dd59dd03c91e3a3ebe1876698bd9c8da4a9182a0727e72f5f4bb3e21f6e",
        "symbolic_kernel_self_test_digest_sha256":
            "f8207c2c82033486ea2e507a66713739b8e8052a2991d300280a8e2b59378b7e",
        "all_required_hashes_non_null": True,
        "dependency_verifier_reads_raw_bytes_only": True,
        "dependency_verifier_may_import_execute_or_parse_sources": False,
        "known_AF3D1_delta_authorities": [
            {
                "authority": "R242.formal_root_existence_classification_ledger",
                "authority_role": "CONSTRUCTION_LINEAGE",
                "filename": "cm2_round242_source_g_outgoing_graph_existence_stratum_materialization_certificate.json",
                "file_sha256": "8d32c381e21c03aad6a531b7e5a527d295783b7e3e38baa1e6bcba20c40db22e",
                "json_path": ".result.formal_root_existence_classification_ledger.rows[]",
                "row_count": 3_136,
                "row_id_field": "root_existence_row_id",
                "rows_sha256": "39df731f100637b57945faeb907bcb219168f7083b32e876c8e09be5bfb189fa",
            },
            {
                "authority": "R242.formal_zero_absence_base_partition_ledger",
                "authority_role": "ANALYTIC_LINEAGE",
                "filename": "cm2_round242_source_g_outgoing_graph_existence_stratum_materialization_certificate.json",
                "file_sha256": "8d32c381e21c03aad6a531b7e5a527d295783b7e3e38baa1e6bcba20c40db22e",
                "json_path": ".result.formal_zero_absence_base_partition_ledger.rows[]",
                "row_count": 8_400,
                "row_id_field": "zero_absence_leaf_row_id",
                "rows_sha256": "2df003dbc57e1792c1ef09cc388224a6199d5bf8e206c4c8c294a1608cc4980b",
            },
            {
                "authority": "R179.retained_3d_child_rows",
                "authority_role": "ANALYTIC_LINEAGE",
                "filename": "cm2_round179_source_g_residual_tube_arrangement_rows.json",
                "file_sha256": "f20b42c1fed781779b537b4d45bf44233eae1ed3ee620b95177a80f0eb2b5e42",
                "json_path": ".result.retained_3d_child_rows[]",
                "row_count": 106_680,
                "row_id_field": "packed column 0 row_id",
                "rows_sha256": "276483255e2b1dda1c682641f5cdcefd67be9040cadad8f4eb810d0fd5cc0b79",
            },
            {
                "authority": "R236.whole_root_finite_key_partition_rows",
                "authority_role": "CONSTRUCTION_LINEAGE",
                "filename": "cm2_round236_source_g_wall_residual_closure_and_root_key_partition_certificate.json",
                "file_sha256": "b5b9ec358b4837a02218756a034440d8fbc2aa706ca421bedb28aaf785de0217",
                "json_path": ".result.whole_root_finite_key_partition_rows[]",
                "row_count": 2_640,
                "row_id_field": "whole_root_partition_row_id",
                "rows_sha256": "17cee8dcc86d2436b47f1605ca324f2006255ed983b57ac06938743b952dafd9",
            },
            {
                "authority": "R295A.representation_alias_rows",
                "authority_role": "IDENTITY_BINDING",
                "filename": "cm2_round295a_source_g_r291_positive_t_retained_continuation_closure_representation_alias_ledger.json.gz",
                "file_sha256": "5c826ef03dd6f8662528e565c36089422e590d1ebf9fc8bade99f1665c68ad2f",
                "json_path": ".rows[]",
                "row_count": 276,
                "row_id_field": "Round295A_retained_continuation_alias_row_id",
                "rows_sha256": "40047a170d2e89a9e9cf8422ff86e265166e921f86386ecb4df790e8210d09de",
            },
        ],
        "known_delta_authority_count": 5,
        "known_commitments_bound_by_final_AF3D1_hash": True,
    }


def _representation_contract() -> dict[str, Any]:
    return {
        "representation_row_count": REPRESENTATION_COUNT,
        "role_counts": [
            {"role": role, "row_count": count}
            for role, count in REPRESENTATION_ROLE_COUNTS
        ],
        "coordinate_counts": [
            {"coordinate_system": name, "row_count": count}
            for name, count in REPRESENTATION_COORDINATE_COUNTS
        ],
        "role_coordinate_cross_counts": [
            {"role": role, "coordinate_system": coord, "row_count": count}
            for role, coord, count in REPRESENTATION_CROSS_COUNTS
        ],
        "count_equations": [
            "564492+848+46564=611904",
            "46288_R294+276_R295A=46564_aliases",
            "421804+9404+94660+38624=564492_primary",
            "466768+11852+94660+38624=611904_by_coordinate",
            "10252_R292_uncovered_cells-9404_R292_members=848_refined_primary_extras",
            "1600_T2PS_aliases+44964_TPS_aliases=46564_aliases",
        ],
        "R292_primary_selection": {
            "rule": "MIN_CANONICAL_CELL_ID_PER_CONNECTED_COMPONENT",
            "ordering": "unsigned bytewise ASCII order of canonical cell ID",
            "primary_count": 9_404,
            "extra_count": 848,
            "hash_seed_may_affect_selection": False,
            "all_other_component_cell_ids_are_REFINED_PRIMARY_EXTRA": True,
        },
        "R294_alias_count": 46_288,
        "R295A_alias_count": 276,
        "one_primary_representation_per_member": True,
        "every_extra_has_exactly_one_existing_member_owner": True,
        "representation_mints_member_identity": False,
        "missing_orphan_duplicate_must_equal": 0,
        "pullback_set_equality_required": True,
    }


def _obligation_contract() -> dict[str, Any]:
    return {
        "known_theorem_obligation_census": THEOREM_OBLIGATION_COUNT,
        "independent_root_obligation_count": ROOT_OBLIGATION_COUNT,
        "dependent_closure_obligation_count": DEPENDENT_OBLIGATION_COUNT,
        "known_node_counts": {
            "A1": A1_COUNT,
            "A2": A2_COUNT,
            "R1": 295_340,
            "R2": 295_336,
            "G1": 38_624,
            "G2A": 38_624,
            "G2B_REFERENCE_OBLIGATIONS": 76_848,
        },
        "count_equations": [
            "17940_A1+295340_R1+38624_G1=351904_roots",
            "62152_A2+295336_R2+38624_G2A+76848_G2B_refs=472960_dependents",
            "351904+472960=824864_known_obligations",
            "224_R204_sheets+17716_R208_R211_sheets=17940_A1",
            "504_R204_curves+280_R204_points+20456_R211_curves+40912_R211_endpoints=62152_A2",
        ],
        "A1_and_A2_are_known_obligation_counts_only": True,
        "theorem_obligation_census_is_final_feature_ledger_count": False,
        "final_feature_ledger_row_count": None,
        "feature_row_count_may_not_be_frozen_from_824864": True,
    }


def _contract_document() -> dict[str, Any]:
    return {
        "schema": SCHEMA,
        "status": STATUS,
        "sealed": True,
        "candidate_is_formal": False,
        "scope": {
            "purpose": "ZERO_CREDIT_TYPED_SCHEMA_FOR_NORMALIZED_SUPPORT_AND_REPRESENTATION",
            "permitted": [
                "TYPE_AND_MACRO_GRAMMAR",
                "ROW_WIRE_SCHEMA",
                "COUNT_AND_JOIN_EQUATIONS",
                "AUTHORITY_ROLE_SEPARATION",
                "FUTURE_STREAMING_VALIDATION_RULES",
            ],
            "excluded": [
                "NORMALIZED_SUPPORT_CREDIT",
                "REPRESENTATION_COVER_CREDIT",
                "TRANSITION_ATLAS_COMPLETENESS",
                "PAIR_ROUTING",
                "COMPONENT_UNION",
                "MAXIMALITY",
                "FIBRE",
                "GLOBAL_DISPOSITION",
                "CM2_CLAIM",
            ],
        },
        "sealed_dependency_pins": _sealed_dependency_pins(),
        "type_system": _sort_contract(),
        "baseline_AST_operators": list(BASELINE_OPERATORS),
        "macro_lowering": _macro_contract(),
        "proof_kernel_ids": list(PROOF_KERNEL_IDS),
        "proof_kernel_contract": _proof_kernel_contract(),
        "proof_kernel_family_mapping": {
            "EXACT_RATIONAL_AST_NORMALIZATION_V2": [
                "ALL_ROOT_AND_DEPENDENT_AST_ROWS",
                "ALL_CHART_MAP_COMPONENTS",
            ],
            "DIRECTED_RATIONAL_INTERVAL_SIGN_V1": [
                "STRICT_SIGN_CELL",
                "IMPLICIT_REGULAR_GRAPH_DERIVATIVE_SIGN",
            ],
            "POSITIVE_SQRT_INTERVAL_V1": [
                "SOURCE_G_FIRST_HIT_MAP_RADICAND",
                "SQRT_POSITIVE_DOMAIN",
            ],
            "PREDICATE_CELL_EQUIVALENCE_V1": [
                "MEMBER_SUPPORT_EQUALITY",
                "CHART_PULLBACK_SET_EQUALITY",
            ],
            "MONOTONE_GRAPH_EXISTENCE_UNIQUENESS_V1": [
                "R204_TARGET_REGULAR_GRAPH",
                "R208_R211_FACTOR_SHEETS",
                "G1_SOURCE_FREE_GRAPH_DEFINITIONS",
            ],
            "DEPENDENT_INCIDENCE_RESTRICTION_V1": [
                "A2",
                "BOUNDARY_TRACE_INCIDENCE",
            ],
            "FINITE_HALF_OPEN_SUPPORT_UNION_V1": [
                "R2",
                "R292",
                "MULTICELL_MEMBER_SUPPORT",
            ],
            "ARTIFICIAL_FACE_REGLUE_V1": [
                "R292_REFINED_PRIMARY_COMPONENTS",
                "R295A_POSITIVE_T_CONTINUATION_ALIASES",
            ],
            "FIXED_SIGN_T2PS_PULLBACK_V1": [
                "R292_PRIMARY_AND_REFINED_EXTRA_REPRESENTATIONS",
                "R294_T2PS_ALIASES",
            ],
            "REPRESENTATION_OWNER_BACKBINDING_V1": [
                "ALL_611904_REPRESENTATION_ROWS",
            ],
            "SHEET_MEMBER_EQUIVALENCE_V1": [
                "G2A",
                "SHEET_MEMBER_GRAPH_DEFINITION_EQUALITY",
            ],
            "BOUNDARY_TRACE_PHYSICAL_INCIDENCE_V1": [
                "G2B",
                "A2_PHYSICAL_TRACES",
                "HALF_OPEN_BOUNDARY_ASSIGNMENT",
            ],
            "SOURCE_LINEAGE_EXHAUSTION_V1": [
                "ALL_564492_MEMBER_ROWS",
                "ALL_611904_REPRESENTATION_ROWS",
                "MISSING_ORPHAN_DUPLICATE_ZERO_GATES",
            ],
        },
        "row_schema_order": list(ROW_SCHEMA_ORDER),
        "row_schemas": _row_schemas(),
        "AF2_family_variants": _family_contracts(),
        "member_census": {
            "member_count": MEMBER_COUNT,
            "family_counts": [
                {"family": family, "member_count": count}
                for family, count in AF2_FAMILY_COUNTS
            ],
            "count_equation": "126468+295336+9404+38624+76832+17828=564492",
            "one_and_only_one_member_row_per_B0_member": True,
            "missing_orphan_duplicate_must_equal": 0,
        },
        "representation_census": _representation_contract(),
        "theorem_obligation_contract": _obligation_contract(),
        "authority_and_evidence_tiers": _authority_roles(),
        "streaming_implementation_contract": {
            "held_fd_hash_and_parse_required": True,
            "O_NOFOLLOW_and_nlink_one_required": True,
            "fstat_before_and_after_required": True,
            "TOCTOU_path_replacement_fail_closed": True,
            "bounded_streaming_rows_required": True,
            "external_sort_key": [
                "typed_row_kind_order",
                "B0_member_id_or_natural_key",
                "canonical_row_id",
            ],
            "two_hash_seeds_must_emit_byte_identical_candidates": True,
            "independent_verifier_may_import_or_execute_producer": False,
            "independent_verifier_reconstructs_without_writes": True,
            "all_join_missing_orphan_duplicate_gap_counts_must_equal": 0,
        },
        "candidate_and_producer_modes": {
            "enabled": False,
            "block_before_path_lstat": True,
            "block_before_input_open": True,
            "block_before_temp_creation": True,
            "block_before_output_write": True,
            "block_reason": CANDIDATE_BLOCK_REASON,
        },
        "formal_credit": {
            "feature_definition": 0,
            "member_support": 0,
            "representation_cover": 0,
            "physical_incidence": 0,
            "transition": 0,
            "pair_routing": 0,
            "component_union": 0,
            "maximality": 0,
            "fibre": 0,
            "global_disposition": 0,
            "CM2": 0,
        },
        "downstream_state": {
            "B1A": "BLOCKED_AWAITING_CONSTRUCTOR_INDEPENDENT_VERIFIER_AND_FORMAL_PACKAGE",
            "B2": "NOT_AUTHORIZED",
            "D02": "BLOCKED",
            "D03": "NOT_REACHED",
            "D04": "NOT_MINTED",
            "CM2": "NO-GO_FOR_CLAIM",
        },
    }


def _validate_row_schemas(document: dict[str, Any]) -> None:
    need(document["row_schema_order"] == list(ROW_SCHEMA_ORDER), "row schema order")
    rows = document["row_schemas"]
    need(rows == _row_schemas(), "complete typed row schemas")
    need(tuple(rows) == ROW_SCHEMA_ORDER, "row schema keys")
    for name in ROW_SCHEMA_ORDER:
        row = rows[name]
        need(isinstance(row["required_fields"], list), f"{name} required fields")
        need(len(row["required_fields"]) == len(set(row["required_fields"])), f"{name} unique fields")
        need(row["required_fields"][-1] == "row_sha256", f"{name} row hash last")
        need("schema" in row["required_fields"], f"{name} schema field")
    need(rows["feature"]["root_definition_independently_evaluable"] is True, "feature evaluable")
    need(rows["member"]["support_union_equals_member_support"] is True, "member equality")
    need(rows["representation"]["forward_inverse_domain_and_set_equality_required"] is True, "pullback equality")
    need(rows["representation"]["mints_member_identity_must_equal"] is False, "representation identity")
    need(rows["incidence"]["identifier_adjacency_is_not_physical_incidence"] is True, "physical incidence")
    need(rows["transition_handle"]["transition_atlas_completeness_claimed"] is False, "transition nonclaim")
    need(rows["gap"]["formal_PASS_gap_count_must_equal"] == 0, "gap zero")


def validate_contract(document: dict[str, Any]) -> None:
    need(document["schema"] == SCHEMA, "schema")
    need(document["status"] == STATUS, "status")
    need(document["sealed"] is True, "sealed")
    need(document["candidate_is_formal"] is False, "candidate nonformal")

    pins = document["sealed_dependency_pins"]
    need(pins == _sealed_dependency_pins(), "exact sealed dependency pins")
    need(pins["seal_state"] == "SEALED_EXACT_TWO_SOURCE_DEPENDENCY_SET", "dependency seal")
    need(pins["dependency_source_count"] == len(pins["dependency_sources"]) == 2, "dependency source count")
    need(tuple(pins["dependency_sources"]) == DEPENDENCY_PINS, "exact dependency source pins")
    need(pins["dependency_source_set_sha256"] == digest(DEPENDENCY_PINS), "dependency set digest")
    need(not _contains_null(pins), "sealed pins non-null")
    need(pins["all_required_hashes_non_null"] is True, "required hashes non-null")
    need(pins["dependency_verifier_reads_raw_bytes_only"] is True, "raw-byte verifier")
    need(
        pins["dependency_verifier_may_import_execute_or_parse_sources"] is False,
        "dependency no import execute parse",
    )
    need(pins["known_delta_authority_count"] == len(pins["known_AF3D1_delta_authorities"]) == 5, "delta authority count")
    need(
        [row["authority"] for row in pins["known_AF3D1_delta_authorities"]]
        == [
            "R242.formal_root_existence_classification_ledger",
            "R242.formal_zero_absence_base_partition_ledger",
            "R179.retained_3d_child_rows",
            "R236.whole_root_finite_key_partition_rows",
            "R295A.representation_alias_rows",
        ],
        "delta authorities",
    )
    need(
        [row["row_count"] for row in pins["known_AF3D1_delta_authorities"]]
        == [3_136, 8_400, 106_680, 2_640, 276],
        "delta authority row counts",
    )

    need(document["type_system"] == _sort_contract(), "type system")
    need(tuple(document["baseline_AST_operators"]) == BASELINE_OPERATORS, "operators")
    need(document["macro_lowering"] == _macro_contract(), "macro lowering")
    need(tuple(document["proof_kernel_ids"]) == PROOF_KERNEL_IDS, "proof kernels")
    kernel_contract = document["proof_kernel_contract"]
    need(kernel_contract == _proof_kernel_contract(), "exact proof kernel contract")
    need(tuple(kernel_contract["allowlist"]) == PROOF_KERNEL_IDS, "closed kernel allowlist")
    need(tuple(kernel_contract["wire_shapes"]) == PROOF_KERNEL_IDS, "kernel wire shape order")
    legacy = kernel_contract["AF0_legacy_bundle"]
    need(tuple(legacy["ids"]) == AF0_PROOF_KERNEL_BUNDLE, "AF0 legacy bundle")
    need(legacy["bundle_accepted_as_AF4_allowlist"] is False, "AF0 bundle forbidden")
    need(
        tuple(legacy["legacy_only_forbidden_ids"])
        == AF0_LEGACY_ONLY_FORBIDDEN_KERNEL_IDS,
        "legacy-only kernels forbidden",
    )
    need(
        tuple(legacy["stable_names_retained_in_AF4"])
        == AF0_RETAINED_KERNEL_IDS,
        "retained kernel names",
    )
    need(
        set(AF0_LEGACY_ONLY_FORBIDDEN_KERNEL_IDS).isdisjoint(PROOF_KERNEL_IDS),
        "legacy-only IDs absent from allowlist",
    )
    field_kernel_ids = {
        kernel_id
        for allowed in kernel_contract["typed_certificate_field_allowlists"].values()
        for kernel_id in allowed
    }
    need(field_kernel_ids == set(PROOF_KERNEL_IDS), "typed fields cover exact kernels")
    need(set(document["proof_kernel_family_mapping"]) == set(PROOF_KERNEL_IDS), "kernel mapping")
    _validate_row_schemas(document)

    families = document["AF2_family_variants"]
    need(
        tuple((row["family"], row["member_count"]) for row in families)
        == AF2_FAMILY_COUNTS,
        "family variants",
    )
    need(sum(row["member_count"] for row in families) == MEMBER_COUNT, "family total")
    preserved = families[0]
    need(sum(preserved["fine_partition"].values()) == 126_468, "preserved partition")
    r2 = families[1]
    need(
        r2["source_cell_count"] == 295_340
        and r2["member_union_cell_count_histogram"] == {"1": 295_332, "2": 4},
        "R2 cells",
    )
    r292 = families[2]
    need(
        r292["uncovered_exact_T2PS_cell_count"] - r292["local_connectivity_rank"]
        == r292["member_count"]
        == 9_404,
        "R292 equation",
    )
    g2a = families[3]
    need(sum(g2a["fine_partition"].values()) == 38_624, "G2A equation")
    g2b = families[4]
    need(g2b["incidence_reference_count"] == 76_848 and g2b["member_count"] == 76_832, "G2B distinction")
    non_graph = families[5]
    need(sum(non_graph["fine_partition"].values()) == 17_828, "non-graph equation")
    need(
        "R247_SOURCE_SEAM_DYADIC_CORRIDOR_AS_FULL_SUPPORT"
        in non_graph["forbidden_substitutions"],
        "source seam corridor exclusion",
    )

    members = document["member_census"]
    need(members["member_count"] == MEMBER_COUNT, "member count")
    need(
        tuple((row["family"], row["member_count"]) for row in members["family_counts"])
        == AF2_FAMILY_COUNTS,
        "member family counts",
    )
    need(members["one_and_only_one_member_row_per_B0_member"] is True, "one member row")
    need(members["missing_orphan_duplicate_must_equal"] == 0, "member defects")

    reps = document["representation_census"]
    need(reps["representation_row_count"] == REPRESENTATION_COUNT, "representation total")
    need(
        tuple((row["role"], row["row_count"]) for row in reps["role_counts"])
        == REPRESENTATION_ROLE_COUNTS,
        "representation roles",
    )
    need(
        tuple((row["coordinate_system"], row["row_count"]) for row in reps["coordinate_counts"])
        == REPRESENTATION_COORDINATE_COUNTS,
        "representation coordinates",
    )
    need(
        tuple((row["role"], row["coordinate_system"], row["row_count"]) for row in reps["role_coordinate_cross_counts"])
        == REPRESENTATION_CROSS_COUNTS,
        "representation cross counts",
    )
    need(sum(count for _, count in REPRESENTATION_ROLE_COUNTS) == REPRESENTATION_COUNT, "representation role sum")
    need(sum(count for _, count in REPRESENTATION_COORDINATE_COUNTS) == REPRESENTATION_COUNT, "representation coordinate sum")
    need(sum(count for _, _, count in REPRESENTATION_CROSS_COUNTS) == REPRESENTATION_COUNT, "representation cross sum")
    need(reps["R294_alias_count"] + reps["R295A_alias_count"] == 46_564, "alias sum")
    selection = reps["R292_primary_selection"]
    need(selection["rule"] == "MIN_CANONICAL_CELL_ID_PER_CONNECTED_COMPONENT", "R292 primary rule")
    need(selection["primary_count"] == 9_404 and selection["extra_count"] == 848, "R292 representation counts")
    need(selection["hash_seed_may_affect_selection"] is False, "R292 seed independence")
    need(reps["representation_mints_member_identity"] is False, "representation no identity")
    need(reps["pullback_set_equality_required"] is True, "representation equality")

    obligations = document["theorem_obligation_contract"]
    need(obligations["known_theorem_obligation_census"] == THEOREM_OBLIGATION_COUNT, "obligation total")
    need(
        obligations["independent_root_obligation_count"]
        + obligations["dependent_closure_obligation_count"]
        == THEOREM_OBLIGATION_COUNT,
        "obligation partition",
    )
    need(obligations["known_node_counts"]["A1"] == A1_COUNT, "A1")
    need(obligations["known_node_counts"]["A2"] == A2_COUNT, "A2")
    need(obligations["A1_and_A2_are_known_obligation_counts_only"] is True, "A1 A2 scope")
    need(obligations["theorem_obligation_census_is_final_feature_ledger_count"] is False, "824864 nonfinal")
    need(obligations["final_feature_ledger_row_count"] is None, "feature count unknown")

    tiers = document["authority_and_evidence_tiers"]
    need(tiers == _authority_roles(), "authority tiers")
    need(tiers["policies"]["OUTER_ENVELOPE_ONLY"]["admitted_for_construction"] is False, "outer excluded")
    need(tiers["policies"]["DIAGNOSTIC_ONLY"]["admitted_for_construction"] is False, "diagnostic excluded")
    need(tiers["identity_binding_may_supply_geometry"] is False, "identity no geometry")

    modes = document["candidate_and_producer_modes"]
    need(modes["enabled"] is False, "candidate disabled")
    need(
        all(
            modes[key] is True
            for key in (
                "block_before_path_lstat",
                "block_before_input_open",
                "block_before_temp_creation",
                "block_before_output_write",
            )
        ),
        "candidate boundary",
    )
    need(modes["block_reason"] == CANDIDATE_BLOCK_REASON, "candidate reason")

    need(all(value == 0 for value in document["formal_credit"].values()), "all zero credit")
    state = document["downstream_state"]
    need(state["B1A"].startswith("BLOCKED_"), "B1A blocked")
    need(state["B2"] == "NOT_AUTHORIZED", "B2 blocked")
    need(state["D02"] == "BLOCKED", "D02 blocked")
    need(state["CM2"] == "NO-GO_FOR_CLAIM", "CM2 blocked")


def contract_envelope() -> dict[str, Any]:
    document = _contract_document()
    validate_contract(document)
    return {
        "contract": document,
        "canonical_contract_digest_sha256": digest(document),
    }


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
    """Hash exactly two pinned source files twice through held descriptors.

    Dependency bytes are never decoded, imported, executed, or parsed.
    Directory and file identities are checked before and after both passes.
    """

    need(len(DEPENDENCY_PINS) == 2, "exact two dependency pins")
    directory_text = os.fspath(DEPENDENCY_DIRECTORY)
    directory_before_path = os.stat(directory_text, follow_symlinks=False)
    need(stat.S_ISDIR(directory_before_path.st_mode), "dependency directory regular")
    directory_flags = (
        os.O_RDONLY
        | getattr(os, "O_DIRECTORY", 0)
        | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_NOFOLLOW", 0)
    )
    directory_fd = os.open(directory_text, directory_flags)
    rows: list[dict[str, Any]] = []
    try:
        directory_held_before = os.fstat(directory_fd)
        need(
            _directory_identity(directory_before_path)
            == _directory_identity(directory_held_before),
            "dependency directory open race",
        )
        for pin in DEPENDENCY_PINS:
            filename = pin["filename"]
            need(
                filename == os.path.basename(filename)
                and filename not in ("", ".", ".."),
                "dependency basename",
            )
            path_before = os.stat(
                filename,
                dir_fd=directory_fd,
                follow_symlinks=False,
            )
            need(stat.S_ISREG(path_before.st_mode), f"regular dependency:{filename}")
            need(path_before.st_nlink == 1, f"single-link dependency:{filename}")
            need(path_before.st_size == pin["exact_size"], f"dependency size:{filename}")
            file_flags = (
                os.O_RDONLY
                | getattr(os, "O_CLOEXEC", 0)
                | getattr(os, "O_NOFOLLOW", 0)
            )
            fd = os.open(filename, file_flags, dir_fd=directory_fd)
            try:
                held_before = os.fstat(fd)
                need(
                    _stat_fingerprint(path_before) == _stat_fingerprint(held_before),
                    f"dependency path/open race:{filename}",
                )
                pass1_size, pass1_sha = _hash_held_fd(fd)
                held_between = os.fstat(fd)
                need(
                    _stat_fingerprint(held_before) == _stat_fingerprint(held_between),
                    f"dependency changed after pass1:{filename}",
                )
                pass2_size, pass2_sha = _hash_held_fd(fd)
                held_after = os.fstat(fd)
                need(
                    _stat_fingerprint(held_before) == _stat_fingerprint(held_after),
                    f"dependency changed after pass2:{filename}",
                )
                path_after = os.stat(
                    filename,
                    dir_fd=directory_fd,
                    follow_symlinks=False,
                )
                need(
                    _stat_fingerprint(held_before) == _stat_fingerprint(path_after),
                    f"dependency path replaced:{filename}",
                )
                need(
                    pass1_size == pass2_size == pin["exact_size"],
                    f"dependency two-pass size:{filename}",
                )
                need(
                    pass1_sha == pass2_sha == pin["source_sha256"],
                    f"dependency two-pass hash:{filename}",
                )
                rows.append({
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
                os.close(fd)
        directory_held_after = os.fstat(directory_fd)
        directory_after_path = os.stat(directory_text, follow_symlinks=False)
        need(
            _directory_identity(directory_held_before)
            == _directory_identity(directory_held_after)
            == _directory_identity(directory_after_path),
            "dependency directory path replaced",
        )
    finally:
        os.close(directory_fd)

    body = {
        "schema": SCHEMA + ".dependency-verification.v1",
        "status": "PASS_EXACT_TWO_SOURCE_HELD_DIRFD_TWO_PASS_RAW_BYTE_VERIFICATION",
        "dependency_source_count": len(rows),
        "dependency_source_set_sha256": digest(DEPENDENCY_PINS),
        "raw_bytes_only": True,
        "dependency_imported": False,
        "dependency_executed": False,
        "dependency_parsed": False,
        "directory_path_identity_stable": True,
        "files": rows,
        "formal_credit": 0,
    }
    return {
        **body,
        "verification_digest_sha256": digest(body),
    }


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
        ("status downgrade", setter(("status",), "UNSEALED__AWAITING_PINS")),
        ("sealed downgrade", setter(("sealed",), False)),
        ("candidate formal", setter(("candidate_is_formal",), True)),
        ("null AF3D1 pin", setter(("sealed_dependency_pins", "Round306B1AF3D1_contract_file_sha256"), None)),
        ("wrong AF3D1 pin", setter(("sealed_dependency_pins", "Round306B1AF3D1_contract_file_sha256"), "0" * 64)),
        ("null kernel pin", setter(("sealed_dependency_pins", "symbolic_kernel_source_file_sha256"), None)),
        ("wrong kernel pin", setter(("sealed_dependency_pins", "symbolic_kernel_source_file_sha256"), "1" * 64)),
        ("dependency count", setter(("sealed_dependency_pins", "dependency_source_count"), 1)),
        ("dependency source size", setter(("sealed_dependency_pins", "dependency_sources", 0, "exact_size"), 57_388)),
        ("dependency source hash", setter(("sealed_dependency_pins", "dependency_sources", 1, "source_sha256"), "2" * 64)),
        ("delta count", setter(("sealed_dependency_pins", "known_delta_authority_count"), 4)),
        ("delta row count", setter(("sealed_dependency_pins", "known_AF3D1_delta_authorities", 2, "row_count"), 106_679)),
        ("sort erasure", setter(("type_system", "coordinate_parameter_erasure_forbidden"), False)),
        ("sort mutation", setter(("type_system", "sorts", "OpenBox<C>", "all_bounds_strict"), False)),
        ("operator deletion", lambda doc: doc["baseline_AST_operators"].pop()),
        ("operator insertion", lambda doc: doc["baseline_AST_operators"].append("OPAQUE_SOURCE_LABEL")),
        ("macro opaque", setter(("macro_lowering", "macros_are_not_stored_AST_operators"), False)),
        ("macro deletion", lambda doc: doc["macro_lowering"]["lowering_order"].pop()),
        ("kernel deletion", lambda doc: doc["proof_kernel_ids"].pop()),
        ("kernel invention", lambda doc: doc["proof_kernel_ids"].append("UNPINNED_KERNEL_V1")),
        ("legacy kernel substitution", setter(("proof_kernel_contract", "allowlist", 0), "EXACT_RATIONAL_AST_NORMALIZATION_V1")),
        ("AF0 bundle accepted", setter(("proof_kernel_contract", "AF0_legacy_bundle", "bundle_accepted_as_AF4_allowlist"), True)),
        ("legacy forbidden deletion", lambda doc: doc["proof_kernel_contract"]["AF0_legacy_bundle"]["legacy_only_forbidden_ids"].pop()),
        ("kernel wire shape", setter(("proof_kernel_contract", "wire_shapes", "POSITIVE_SQRT_INTERVAL_V1", "evidence", "method"), "STR")),
        ("field accepts legacy kernel", lambda doc: doc["proof_kernel_contract"]["typed_certificate_field_allowlists"]["feature.proof_kernel_id"].append("EXACT_RATIONAL_AST_NORMALIZATION_V1")),
        ("kernel mapping deletion", deleter(("proof_kernel_family_mapping", "BOUNDARY_TRACE_PHYSICAL_INCIDENCE_V1"))),
        ("row schema order", lambda doc: doc["row_schema_order"].reverse()),
        ("feature field", lambda doc: doc["row_schemas"]["feature"]["required_fields"].remove("definition_ast")),
        ("member equality", setter(("row_schemas", "member", "support_union_equals_member_support"), False)),
        ("representation equality", setter(("row_schemas", "representation", "forward_inverse_domain_and_set_equality_required"), False)),
        ("representation identity", setter(("row_schemas", "representation", "mints_member_identity_must_equal"), True)),
        ("incidence adjacency", setter(("row_schemas", "incidence", "identifier_adjacency_is_not_physical_incidence"), False)),
        ("transition claim", setter(("row_schemas", "transition_handle", "transition_atlas_completeness_claimed"), True)),
        ("gap forced", setter(("row_schemas", "gap", "formal_PASS_gap_count_must_equal"), 1)),
        ("family count", setter(("AF2_family_variants", 0, "member_count"), 126_467)),
        ("preserved fine", setter(("AF2_family_variants", 0, "fine_partition", "R204_STRICT_CURVED_SIGN_CELL"), 735)),
        ("R2 cells", setter(("AF2_family_variants", 1, "source_cell_count"), 295_339)),
        ("R292 rank", setter(("AF2_family_variants", 2, "local_connectivity_rank"), 847)),
        ("G2A sheet", setter(("AF2_family_variants", 3, "fine_partition", "R245_SHEET"), 263)),
        ("G2B refs", setter(("AF2_family_variants", 4, "incidence_reference_count"), 76_832)),
        ("source seam witness promoted", lambda doc: doc["AF2_family_variants"][5]["forbidden_substitutions"].remove("R247_SOURCE_SEAM_DYADIC_CORRIDOR_AS_FULL_SUPPORT")),
        ("member census", setter(("member_census", "member_count"), 564_491)),
        ("member defects", setter(("member_census", "missing_orphan_duplicate_must_equal"), 1)),
        ("representation total", setter(("representation_census", "representation_row_count"), 611_903)),
        ("R295A aliases", setter(("representation_census", "R295A_alias_count"), 275)),
        ("R292 selection", setter(("representation_census", "R292_primary_selection", "rule"), "HASH_SEED_MIN")),
        ("R292 seed", setter(("representation_census", "R292_primary_selection", "hash_seed_may_affect_selection"), True)),
        ("representation mint", setter(("representation_census", "representation_mints_member_identity"), True)),
        ("A1", setter(("theorem_obligation_contract", "known_node_counts", "A1"), 17_939)),
        ("A2", setter(("theorem_obligation_contract", "known_node_counts", "A2"), 62_151)),
        ("824864 promoted", setter(("theorem_obligation_contract", "theorem_obligation_census_is_final_feature_ledger_count"), True)),
        ("feature count invented", setter(("theorem_obligation_contract", "final_feature_ledger_row_count"), 824_864)),
        ("outer admitted", setter(("authority_and_evidence_tiers", "policies", "OUTER_ENVELOPE_ONLY", "admitted_for_construction"), True)),
        ("inner admitted", setter(("authority_and_evidence_tiers", "policies", "DIAGNOSTIC_ONLY", "admitted_for_construction"), True)),
        ("identity geometry", setter(("authority_and_evidence_tiers", "identity_binding_may_supply_geometry"), True)),
        ("candidate enabled", setter(("candidate_and_producer_modes", "enabled"), True)),
        ("open boundary", setter(("candidate_and_producer_modes", "block_before_input_open"), False)),
        ("formal credit", setter(("formal_credit", "member_support"), 1)),
        ("B1A promoted", setter(("downstream_state", "B1A"), "PASS")),
        ("B2 promoted", setter(("downstream_state", "B2"), "AUTHORIZED")),
        ("D02 promoted", setter(("downstream_state", "D02"), "PASS")),
        ("CM2 promoted", setter(("downstream_state", "CM2"), "GO")),
    ]


def _blocked_candidate_entry(_output_path: str | None, _producer: bool) -> None:
    # The refusal is intentionally the first and only operation.  The path is
    # never converted to Path, resolved, inspected, opened, or written.
    raise ContractBlocked(CANDIDATE_BLOCK_REASON)


def _boundary_probe() -> dict[str, int]:
    counters = {
        "builtins_open": 0,
        "os_open": 0,
        "path_lstat": 0,
        "path_open": 0,
        "path_write": 0,
        "mkstemp": 0,
        "named_temp": 0,
    }

    def trip(name: str) -> Callable[..., Any]:
        def inner(*_args: Any, **_kwargs: Any) -> Any:
            counters[name] += 1
            raise AssertionError(f"filesystem boundary crossed:{name}")
        return inner

    with (
        mock.patch("builtins.open", side_effect=trip("builtins_open")),
        mock.patch("os.open", side_effect=trip("os_open")),
        mock.patch.object(Path, "lstat", side_effect=trip("path_lstat")),
        mock.patch.object(Path, "open", side_effect=trip("path_open")),
        mock.patch.object(Path, "write_bytes", side_effect=trip("path_write")),
        mock.patch("tempfile.mkstemp", side_effect=trip("mkstemp")),
        mock.patch("tempfile.NamedTemporaryFile", side_effect=trip("named_temp")),
    ):
        for producer in (False, True):
            try:
                _blocked_candidate_entry("/must/not/be/inspected", producer)
            except ContractBlocked as exc:
                need(str(exc) == CANDIDATE_BLOCK_REASON, "candidate refusal reason")
            else:
                raise AssertionError("candidate entry did not refuse")
    need(all(value == 0 for value in counters.values()), "zero filesystem calls")
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
            raise AssertionError(f"semantic mutation accepted:{label}")
    need(len(rejected) == len(_semantic_mutations()), "mutation rejection total")

    boundary = _boundary_probe()
    return {
        "schema": SCHEMA + ".self-test.v1",
        "status": "PASS",
        "canonical_contract_digest_sha256": digest(document),
        "semantic_mutation_count": len(rejected),
        "semantic_mutations_rejected": len(rejected),
        "candidate_and_producer_refusals": 2,
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
        raise AssertionError("unreachable candidate path")
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
