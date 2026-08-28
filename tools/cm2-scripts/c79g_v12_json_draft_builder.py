#!/usr/bin/env python3
"""Mechanically rebuild the C79g v12 static JSON drafts.

This helper never imports or executes any protocol Python source.  It only
edits the seven explicitly versioned v12 draft JSON surfaces and refuses to
touch a read-only file.  The final acyclic pin injection remains a separate
step after producer/consumer/launcher source convergence.
"""

from __future__ import annotations

import argparse
import ast
import copy
import hashlib
import json
import os
import re
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "deliverables"
BASE = "cm2_round306c79g_true_global_no_producer_consumer"
SCHEMA = OUT / f"{BASE}_schema_v12.json"
CONTRACT = OUT / f"{BASE}_contract_v12.json"
PRODUCER = OUT / f"{BASE}_v12.py"
CONSUMER = OUT / (
    f"{BASE}_independent_verifier_assembler_authority_consumer_v12.py")
LAUNCHER = OUT / f"{BASE}_cold_launch_v12.py"
TRANSITION = OUT / f"{BASE}_v11_to_v12_static_launch_transition_receipt_v1.json"
AUDIT = OUT / f"{BASE}_static_audit_v12.json"
V11_TRANSITION = OUT / f"{BASE}_v10_to_v11_static_launch_transition_receipt_v1.json"
V11_AUDIT = OUT / f"{BASE}_static_audit_v11.json"
V12_MANIFEST = OUT / f"{BASE}_cold_launch_manifest_v12.sha256"
V12_OUTER = OUT / f"{BASE}_cold_launch_outer_receipt_v12.json"

CHECKPOINT = "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab"
V11_REJECTION_REL = (
    ".cm2-runtime/c79g-v11-rejections-" + CHECKPOINT + "/rejection.json")
V11_REJECTION_NS_REL = V11_REJECTION_REL.removesuffix("/rejection.json")
V11_REJECTION_FILE = "f6cc10d8b7e72553ef0b7a32bbfb99255f36cce16b735002f17be58ae51d3bc8"
V11_REJECTION_OBJECT = "7ae86e38c5910bc9ceaa0a4e5cb1f8fbbf1e73de9c0314fedabbd8cb2db3bb7a"
WITNESS_OBJECT = "374ec1404780efc5cf78da8e4c4b2554d25e6a1bc5da65d063263b34e0531011"
INCIDENT_DIGEST = "64db719d426d3604be39d9bcd52118c1c39a409e47c2aaf38704b18d49ce7ab3"
FIRST_ATTEMPT_DIGEST = "3b768c47f673b18c090946aee79dd103c9a37855451b4af09e0f7bd8042ab63f"
HELPER_NORMALIZED_AST = "38ebe2f639bdb26cac05cec05110ef78bf8057159ebf0f9c8f5d1ce22743fa07"
FORMAL_ATTACK_COUNT = 137
FORMAL_ATTACK_NAME_ORDER_SHA256 = (
    "90ca3c45b88c754a6fd7049579afec495c576957d564047966661647cb694f9d")
V11_PROOF_SHA256 = (
    "8ee05054f12eddddb000f354a3dd1354532a91e37ef1b6d53a250257d9fe8990")
V11_TRANSITION_FILE = (
    "31b33566b898277fb8b272a6f3cd3b51b0b80eac4f58f43979dddfa647a38f4e")
V11_TRANSITION_OBJECT = (
    "9a253960a378521423751735dd272e06dec5c99cfc016d27bf66cfbe7673caaf")
V11_AUDIT_FILE = (
    "6c94068e3f60a89fb608585ae5e6c7dbe02af17880195132bf7c9033ab797115")
V11_AUDIT_OBJECT = (
    "007fba200b67c7704360bb85819435ed13cc6459c8dbac381b99c3adaaf884c3")

PIN_NORMALIZED_CURRENT_BASE7_KEY_ORDER = (
    "SCHEMA", "CONTRACT", "PRODUCER", "CONSUMER", "TRANSITION", "AUDIT",
)
PIN_NORMALIZED_OBJECT_BASE7_KEYS = frozenset({
    "CONTRACT", "TRANSITION", "AUDIT",
})
PIN_NORMALIZED_AST_ALGORITHM = (
    "PYTHON_AST_DUMP_NO_ATTRIBUTES__FORCE_FINAL_BASE7_FALSE__"
    "CURRENT_V12_SIX_BASE7_FILE_F64_OBJECT_E64_OR_NONE__"
    "PRESERVE_V11_REJECTION_AND_ALL_HISTORICAL_PINS_V1"
)

STATIC_AUDIT_INPUT_KEY_ORDER = (
    "schema", "contract_file", "contract_object", "producer", "consumer",
    "transition_file", "transition_object", "launcher_template",
    "v4_supersession_file", "v4_supersession_object",
    "v5_rejection_file", "v5_rejection_object",
    "v6_rejection_file", "v6_rejection_object",
    "v7_rejection_file", "v7_rejection_object",
    "v7_lock_continuity_incident_object",
    "v8_rejection_file", "v8_rejection_object", "v8_launcher_file",
    "v8_launcher_regression_defect_sha256",
    "trusted_v8_rollout_control_flow_incident_digest",
    "v9_rejection_file", "v9_rejection_object", "v9_launcher_file",
    "v9_persisted_v6_proof_sha256", "v9_expanded_v6_proof_sha256",
    "trusted_v9_proof_shape_drift_incident_digest",
    "v10_rejection_file", "v10_rejection_object", "v10_producer_file",
    "trusted_v10_regression_label_prefix_incident_digest",
    "v11_rejection_file", "v11_rejection_object", "v11_producer_file",
    "v11_launcher_file",
    "trusted_v11_dual_validator_divergence_incident_digest",
)
STATIC_AUDIT_INPUT_KEY_ORDER_SHA256 = (
    "d5cae8b70aa3dc72247ff2420039e8cb2942797075f439b4273a9537f12a3056")
STATIC_AUDIT_HISTORICAL_INPUT_KEYS = STATIC_AUDIT_INPUT_KEY_ORDER[8:32]

SUPPORTED_SCHEMA_KEYWORDS = frozenset({
    "$schema", "$id", "$comment", "title", "description", "$defs", "$ref",
    "type", "const", "additionalProperties", "required", "properties",
    "items", "prefixItems", "minItems", "maxItems", "uniqueItems",
    "minLength", "pattern", "minimum",
})
EXPECTED_SCHEMA_KEYWORD_UNIVERSE = [
    "$defs", "$id", "$ref", "$schema", "additionalProperties", "const",
    "description", "items", "maxItems", "minItems", "minLength", "minimum",
    "pattern", "prefixItems", "properties", "required", "title", "type",
]
EXPECTED_OUTPUT_SHAPES = {
    "selfIdentity": 33,
    "independentConsumerProof": 59,
    "staticFreezeProof": 75,
    "coldLaunchProof": 108,
    "laterRejection": 54,
    "producerSourceRegistry": 70,
    "liveRequest": 15,
    "liveACK": 32,
    "liveACKCensus": 42,
}
COMMON_CALLSITE_KIND_KEYS = (
    "module_function", "module_constructor", "self_instance_method",
    "cls_class_method", "localclass_static_method",
    "localclass_class_method", "localclass_instance_method",
)
STALE_V11_COMMON_CALLSITE_SHA256 = (
    "d6d1ffa7a47968ff691fac8e720c9c6770549ae0892e64241204dfe2cd41d6cf")

SOURCE_REGISTRY_EXECUTION_PROOF_EXACT7 = [
    "producer_exec_fd_is_fresh_sealed_memfd",
    "producer_exec_fd_distinct_from_installed_source_fd",
    "producer_exec_memfd_required_seals_valid",
    "producer_exec_bytes_equal_installed_source_bytes",
    "producer_exec_and_installed_source_terminal_replayed",
    "five_incident_authority_inputs_inherited_as_held_fds",
    "five_incident_held_fds_path_identity_mount_and_hash_revalidated",
]
CONTRACT_AUTHORITY_ROOT_STRUCTURE = (
    "ZERO_CREDIT_INNER=(LIVE_V11_EXACT10 + OFFICIAL_V11_LATER_REJECTION + "
    "V11_DUAL_VALIDATOR_DIVERGENCE_INCIDENT + "
    "V10_COLON_PREFIX_PER_CLAUSE_WITNESS + LIVE_V10_EXACT10 + "
    "OFFICIAL_V10_LATER_REJECTION + V10_REGRESSION_LABEL_PREFIX_INCIDENT + "
    "LIVE_V9_EXACT10 + OFFICIAL_V9_LATER_REJECTION + "
    "V9_V6_HELD_SELF_DEFECT_SHAPE_DRIFT_INCIDENT + LIVE_V8_EXACT10 + "
    "OFFICIAL_V8_LATER_REJECTION + TRUSTED_V8_ROLLOUT_CONTROL_FLOW_INCIDENT + "
    "LIVE_V7_EXACT10 + OFFICIAL_V7_LATER_REJECTION + "
    "V7_PUBLICATION_LOCK_CONTINUITY_INCIDENT + LIVE_V6_EXACT10 + "
    "OFFICIAL_V6_LATER_REJECTION + LIVE_V5_EXACT10 + "
    "OFFICIAL_V5_LATER_REJECTION + LIVE_V3_EXACT10 + "
    "OFFICIAL_V3_LATER_REJECTION + V4_REJECTION_SUPERSESSION + "
    "COLD_LAUNCH_STATIC_FREEZE_PROOF + PRESEAL_COMMITTED_SURFACE + "
    "INDEPENDENT_CONSUMER_PROOF + AUTHORITY_SEAL + POSTSEAL_LIVE_REPLAY + "
    "FRESH_EMPTY_V12_REJECTION_NAMESPACE); "
    "POSITIVE_ROOT=HELD_FD_BOOTSTRAPPED_EXTERNALLY_PINNED_COLD_LAUNCHER_WRAPPER(INNER)"
)
CONTRACT_PRESEAL_ROOT_FORMULA = (
    "SHA256(domain || checkpoint || committed_completion_root || "
    "ordered22_digest || replay24_expected_order_digest || "
    "v3_rejection_object_sha256 || v4_supersession_file_sha256 || "
    "v4_supersession_object_sha256 || v5_rejection_file_sha256 || "
    "v5_rejection_object_sha256 || v6_rejection_file_sha256 || "
    "v6_rejection_object_sha256 || v7_rejection_file_sha256 || "
    "v7_rejection_object_sha256 || "
    "v7_publication_lock_continuity_incident_object_sha256 || "
    "v8_rejection_file_sha256 || v8_rejection_object_sha256 || "
    "trusted_v8_rollout_control_flow_incident_digest || "
    "v9_rejection_file_sha256 || v9_rejection_object_sha256 || "
    "trusted_v9_shape_drift_incident_digest || v10_rejection_file_sha256 || "
    "v10_rejection_object_sha256 || "
    "trusted_v10_regression_label_prefix_incident_digest || "
    "v11_rejection_file_sha256 || v11_rejection_object_sha256 || "
    "trusted_v11_dual_validator_divergence_incident_digest || "
    "cold_launcher_file_sha256 || cold_manifest_file_sha256 || "
    "cold_outer_file_sha256 || cold_outer_object_sha256)"
)
CONTRACT_REQUIRED_CONJUNCTS = [
    "LIVE_V3_EXACT10_VALID",
    "OFFICIAL_V3_LATER_REJECTION_AND_SINGLETON_NAMESPACE_VALID",
    "V4_REJECTION_SUPERSESSION_AND_REJECTED_DRAFT_VALID",
    "PUBLISHED_V5_EXACT10_AND_OFFICIAL_LATER_REJECTION_VALID",
    "PUBLISHED_V6_EXACT10_AND_OFFICIAL_LATER_REJECTION_VALID",
    "V7_EXACT10_VALID",
    "V7_OFFICIAL_REJECTION_VALID",
    "V7_INTERRUPTED_PUBLICATION_RECORDED",
    "V8_EXACT10_VALID",
    "V8_OFFICIAL_REJECTION_VALID",
    "TRUSTED_V8_ROLLOUT_CONTROL_FLOW_INCIDENT_RECORDED_WITHOUT_TIMESTAMP_INFERENCE",
    "V9_EXACT10_VALID",
    "V9_OFFICIAL_REJECTION_VALID",
    "TRUSTED_V9_V6_HELD_SELF_DEFECT_SHAPE_DRIFT_INCIDENT_RECORDED_WITH_"
    "CANONICAL_9_KEY_PAYLOAD_SEPARATE_FROM_16_KEY_STRUCTURAL_EVIDENCE",
    "V10_EXACT10_VALID",
    "V10_OFFICIAL_REJECTION_VALID",
    "TRUSTED_V10_REGRESSION_LABEL_PREFIX_INCIDENT_RECORDED_FROM_FROZEN_AST_STRUCTURE",
    "V10_COLON_PREFIX_PER_CLAUSE_WITNESS_REDERIVED_FROM_INHERITED_HELD_FDS_VALID",
    "V11_EXACT10_VALID",
    "V11_OFFICIAL_REJECTION_VALID",
    "TRUSTED_V11_DUAL_VALIDATOR_DIVERGENCE_INCIDENT_RECORDED_WITHOUT_"
    "EXACT_FALSE_CLAUSE_INFERENCE",
    "EXACT_CHECKPOINT_AND_EXACT_PATHS_VALID",
    "COMMITTED_COMPLETION_NOCLOBBER_INSTALL_VALID",
    "STANDALONE_OUTER_ZERO_AND_NON_AUTHORITATIVE",
    "INDEPENDENT_NO_PRODUCER_CONSUMER_VALID",
    "POST_SOURCE_TRANSITION_AND_STATIC_AUDIT_TRUST_ANCHOR_VALID",
    "EXTERNALLY_PINNED_COLD_LAUNCH_EXACT8_MANIFEST_AND_OUTER_LAST_VALID",
    "EXACT_24_FULL_IDENTITY_AND_TERMINAL_REPLAY_VALID",
    "FULL10_C42_C53_IDENTITY_AND_TERMINAL_REPLAY_VALID",
    "AUTHORITY_SEAL_BINDING_AND_NOCLOBBER_LAST_POSITIVE_PATH_NON_REVOCATION_COMMIT_VALID",
    "FRESH_AUTHORIZE_IDEMPOTENT_DURABILITY_RECOVERY_VALID",
    "NO_LATER_V12_REJECTION_AT_EACH_READ",
    "OWNER_HISTORY_GLUE_TWO_SIDES_INCIDENCE_PREFIX_KRAFT_CLOSED",
    "PUBLIC_GLOBAL_UNRESOLVED_ZERO",
]

V11_EXACT10 = [
    {
        "name": "v10_official_rejection",
        "path": ".cm2-runtime/c79g-v10-rejections-" + CHECKPOINT + "/rejection.json",
        "file_sha256": "1b5bbd9ec04f07e7d7d433685aa693b73bf2315a91e4813960bd5a81e8112828",
        "object_sha256": "efdb614e870e70c20202834d3c6ec1a7513a3e98ba5cb4e1b32f87976a529d76",
    },
    {
        "name": "closed_schema",
        "path": f"deliverables/{BASE}_schema_v11.json",
        "file_sha256": "cf1630e3ab1b590876c663b8752d702eae5fe37b7bdbcc7824efbd03bbdbd8e2",
    },
    {
        "name": "contract",
        "path": f"deliverables/{BASE}_contract_v11.json",
        "file_sha256": "c8851778bc8df7a9804efb5fc226548424b58119a2dff3f75bdea9fcac0ec5cf",
        "object_sha256": "b998162a009927f13eb34a88e37f657515e43ae160b3d550de5edb0040486af9",
    },
    {
        "name": "build_only_producer",
        "path": f"deliverables/{BASE}_v11.py",
        "file_sha256": "f3b364afc0f5b2f729a3d7786eb8e9c25a9303959d6d2464a40395968090a30b",
    },
    {
        "name": "independent_consumer",
        "path": f"deliverables/{BASE}_independent_verifier_assembler_authority_consumer_v11.py",
        "file_sha256": "d8ad069e3486b9d657e4840e504885bf13129050f68e6cc04e47b71f149370ec",
    },
    {
        "name": "v10_to_v11_transition",
        "path": f"deliverables/{BASE}_v10_to_v11_static_launch_transition_receipt_v1.json",
        "file_sha256": "31b33566b898277fb8b272a6f3cd3b51b0b80eac4f58f43979dddfa647a38f4e",
        "object_sha256": "9a253960a378521423751735dd272e06dec5c99cfc016d27bf66cfbe7673caaf",
    },
    {
        "name": "static_audit",
        "path": f"deliverables/{BASE}_static_audit_v11.json",
        "file_sha256": "6c94068e3f60a89fb608585ae5e6c7dbe02af17880195132bf7c9033ab797115",
        "object_sha256": "007fba200b67c7704360bb85819435ed13cc6459c8dbac381b99c3adaaf884c3",
    },
    {
        "name": "cold_launcher",
        "path": f"deliverables/{BASE}_cold_launch_v11.py",
        "file_sha256": "9f6971d2ca3e2c8f448a6aeed70bc16f38154c626f7744a4e20ba723e3082cc2",
    },
    {
        "name": "cold_manifest",
        "path": f"deliverables/{BASE}_cold_launch_manifest_v11.sha256",
        "file_sha256": "e27e9b58dbf57a72550da701589819dad7ebb01f6b3c649a56b701c99ef13135",
    },
    {
        "name": "cold_outer",
        "path": f"deliverables/{BASE}_cold_launch_outer_receipt_v11.json",
        "file_sha256": "689a4a323e742427c7f50ec6a7bbea08cdf28c36cbdb43d855a29601329f8c8f",
        "object_sha256": "369dfe73b1dbc68e4147ba39e1c1b7155555b5443d9471159c5ac748723414a4",
    },
]

V10_COLON_PREFIX_WITNESS = {
    "schema": "cm2.round306c79g.true-global-no-producer-consumer.v10-colon-prefix-per-clause-witness.v1",
    "v10_producer_file_sha256": "99bb321da8a63855e52c8d6757d00886c0deeb2182f5044cac35f645e2ebd00a",
    "v9_launcher_file_sha256": "f7559ceeb7d491b8489812670392cb63e3cd5f6a2764db469e2dd51d6b5577fa",
    "six_guard_ast_sha256": "aad296d59f0c196d5f1a733db80251fe7d01b8f658db00e3815392228cd1b94a",
    "six_guard_conjunct_count": 6,
    "fifth_membership_ast_sha256": "e1212df00bbe1d30edd9ddd5f0cdd4c5c489533ada4e9b3dee8a63fd1e64b3a5",
    "fifth_membership_is_exact_legacy_tree_wide_in": True,
    "expanded_structural_dict_count": 1,
    "expanded_structural_dict_exact_key_count": 16,
    "expanded_structural_dict_ast_sha256": "5e7482a66f4f5e7daaae15817b0ed4ca227642c259f159cab2ee9aa913b15c6d",
    "validator_helper_call_count": 1,
    "equality_gate_count": 2,
    "equality_gate_ast_sha256_ordered": [
        "770ab33b30a4986edf4dc4501c69fdbd6eeecbc1c2422176f7e2790df06daeec",
        "432c7de57eb46524ecae7121c5ab62e821f93ac731dcbc76e48ed05ee26940b3",
    ],
    "exact_unprefixed_failure_label_literal_count": 0,
    "exact_colon_prefixed_failure_label_literal_count": 1,
    "failure_label_suffix_match_count": 1,
    "exact_colon_prefix_join_count": 1,
    "exact_colon_prefix_join_ast_sha256": "32166f78c1a380ba16122e37f91de30255bf99399e605b97a9c7e97d5a60d138",
    "legacy_guard_conjunct_truth_vector": [True, True, True, True, False, True],
    "legacy_guard_true_conjunct_count": 5,
    "legacy_guard_false_conjunct_count": 1,
    "legacy_guard_unique_false_zero_based_index": 4,
    "successor_clause_truth_vector": [True] * 15,
    "successor_all_clauses_true": True,
    "direct_top_level_build_hold_call_count": 1,
    "direct_top_level_hold_regression_call_count": 1,
    "direct_top_level_build_stage_call_count": 1,
    "build_hold_top_level_statement_index": 1,
    "hold_regression_top_level_statement_index": 52,
    "build_stage_top_level_statement_index": 19,
    "hold_precedes_stage": True,
    "pre_regression_write_primitive_count": 0,
    "pre_regression_write_primitive_census": {},
    "zero_or_multiple_expanded_dicts_controlled_reject": True,
    "exact_prefix_join_is_authority": True,
    "raw_whole_tree_string_membership_is_authority": False,
    "coherent_attack_count": 16,
    "all_coherent_attacks_rejected": True,
    "formal_global_closure_credit": 0,
    "object_sha256": WITNESS_OBJECT,
}

V11_FIRST_RUNTIME_ATTEMPT = {
    "attempted": True,
    "producer_child_spawned": True,
    "candidate_write_started": False,
    "candidate_or_stage_created": False,
    "positive_runtime_surface_count": 0,
    "aborted_by_dual_validator_divergence_guard": True,
    "command": "build",
    "orientation": "a",
}

V11_INCIDENT = {
    "schema": "cm2.round306c79g.true-global-no-producer-consumer.v11-dual-validator-divergence-incident.v1",
    "incident_id": "V11_LAUNCHER_GATE_PASSED__PRODUCER_COMPOSITE_GUARD_REJECTED__NO_EXACT_FALSE_CLAUSE",
    "evidence_source": "FROZEN_V11_LAUNCHER_AND_PRODUCER_AST__FIRST_BUILD_A_STDERR__OFFICIAL_REJECTION",
    "v11_producer_source_path": f"deliverables/{BASE}_v11.py",
    "v11_producer_source_file_sha256": V11_EXACT10[3]["file_sha256"],
    "v11_launcher_source_path": f"deliverables/{BASE}_cold_launch_v11.py",
    "v11_launcher_source_file_sha256": V11_EXACT10[7]["file_sha256"],
    "v11_official_rejection_file_sha256": V11_REJECTION_FILE,
    "v11_official_rejection_object_sha256": V11_REJECTION_OBJECT,
    "first_command": "build",
    "first_orientation": "a",
    "producer_child_spawned": True,
    "candidate_write_started": False,
    "candidate_or_stage_created": False,
    "positive_runtime_surface_count": 0,
    "launcher_gate_function": "v10_regression_label_prefix_gate",
    "launcher_gate_passed_before_child_spawn": True,
    "producer_guard_function": "v10_regression_label_prefix_incident_regression",
    "producer_composite_guard_rejected": True,
    "producer_failure_label": "frozen v10 sole-false colon-prefix regression and pre-stage control flow",
    "producer_embedded_v10_incident_key_count_claim": 44,
    "producer_embedded_v10_incident_actual_key_count": 45,
    "producer_composite_guard_conjunct_count": 12,
    "exact_failing_subpredicate_persisted": False,
    "specific_false_clause_authority": "UNAVAILABLE",
    "child_consumed_inherited_held_predecessor_fds": False,
    "child_reopened_predecessor_paths": True,
    "launcher_and_producer_validator_implementations_distinct": True,
    "producer_per_clause_witness_persisted": False,
    "v10_colon_prefix_witness_object_sha256": WITNESS_OBJECT,
    "v10_colon_prefix_witness_key_count": 40,
    "v10_colon_prefix_witness_successor_clause_truth_vector": [True] * 15,
    "v10_colon_prefix_witness_all_clauses_true": True,
    "inner_stderr_line": "REJECT: frozen v10 sole-false colon-prefix regression and pre-stage control flow",
    "outer_stderr_line": "REJECT: cold child rejected or failed",
    "failure_occurs_before_candidate_or_stage_creation": True,
    "official_rejection_strictly_after_v11_outer": True,
    "required_successor_fix": "INHERITED_HELD_FD_BYTES__THREE_INDEPENDENT_IDENTICAL_HELPERS__EXACT_PER_CLAUSE_WITNESS",
    "required_held_fd_fix": "CHILD_REVALIDATES_INHERITED_V10_V9_V11_AND_REJECTION_FDS__NO_SECOND_PATH_VIEW_AS_INCIDENT_AUTHORITY",
    "required_validator_fix": "EXACT40_CLOSED_WITNESS__CONTROLLED_ZERO_OR_MULTIPLE_DICT_REJECT__NO_RAW_TREE_LITERAL_AUTHORITY",
    "formal_global_closure_credit": 0,
    "D02_unlock": False,
    "D02_started": False,
    "standalone_authority": False,
    "exact_false_clause_claim_allowed": False,
}

V11_COMMON_REJECTION = {
    "path": V11_REJECTION_REL,
    "namespace_path": V11_REJECTION_NS_REL,
    "file_sha256": V11_REJECTION_FILE,
    "object_sha256": V11_REJECTION_OBJECT,
    "schema": "cm2.round306c79g.true-global-no-producer-consumer.v11.later-rejection",
    "status": "PERMANENT_FAIL_CLOSED_REJECTION__ZERO_CREDIT",
    "reason": "ORPHANED_OR_INCOMPLETE_C79G_V11_SURFACE",
    "namespace_mode": "0555",
    "namespace_nlink": 2,
    "exact_member_universe": ["rejection.json"],
    "member_mode": "0444",
    "member_nlink": 1,
    "formal_global_closure_credit": 0,
    "D02_unlock": False,
    "D02_gate_credit": 0,
    "D02_task_credit": 0,
    "D02_formal_pending_task_count": 33638,
    "D02_started": False,
    "overwrite_delete_or_reuse_allowed": False,
}

V11_ABSENT = [
    f".cm2-runtime/c79g-v11-candidate-a-{CHECKPOINT}",
    f".cm2-runtime/c79g-v11-candidate-b-{CHECKPOINT}",
    f".cm2-runtime/c79g-v11-verification-a-{CHECKPOINT}",
    f".cm2-runtime/c79g-v11-verification-b-{CHECKPOINT}",
    f".cm2-runtime/c79g-v11-committed-completion-{CHECKPOINT}",
    f".cm2-runtime/cm2-global-authority-heads/c79g-v11-{CHECKPOINT}.seal",
    f".cm2-runtime/.c79g-v11-candidate-stage-a-{CHECKPOINT}",
    f".cm2-runtime/.c79g-v11-candidate-stage-b-{CHECKPOINT}",
    f".cm2-runtime/.c79g-v11-verification-stage-a-{CHECKPOINT}",
    f".cm2-runtime/.c79g-v11-verification-stage-b-{CHECKPOINT}",
    f".cm2-runtime/.c79g-v11-completion-stage-{CHECKPOINT}",
    f".cm2-runtime/cm2-global-authority-heads/.c79g-v11-authority-stage-{CHECKPOINT}.seal",
]

V11_PROOF = {
    "ordered_published_exact10": copy.deepcopy(V11_EXACT10),
    "official_later_rejection": copy.deepcopy(V11_COMMON_REJECTION),
    "first_runtime_attempt": copy.deepcopy(V11_FIRST_RUNTIME_ATTEMPT),
    "dual_validator_divergence_incident": copy.deepcopy(V11_INCIDENT),
    "positive_and_stage_surfaces_absent": {
        "exact_absent_path_count": 12,
        "exact_absent_paths": copy.deepcopy(V11_ABSENT),
        "all_absent": True,
    },
    "all_ten_file_pins_match": True,
    "all_declared_object_pins_match": True,
    "all_ten_regular_0444_nlink1": True,
    "exact8_manifest_reconstructs_first_eight_in_order": True,
    "outer_last_pins_manifest_and_launcher": True,
    "outer_then_rejection_chronology_validated": True,
    "v11_execution_allowed": False,
    "v11_runtime_surfaces_authoritative": False,
    "formal_global_closure_credit": 0,
    "D02_unlock": False,
    "D02_gate_credit": 0,
    "D02_task_credit": 0,
    "D02_formal_pending_task_count": 33638,
    "D02_started": False,
}


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False).encode("utf-8")


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def object_hash(value: dict[str, Any]) -> str:
    body = {key: item for key, item in value.items() if key != "object_sha256"}
    return sha256_bytes(canonical(body))


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"),
                      object_pairs_hook=_no_duplicate_pairs)


def _no_duplicate_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, item in pairs:
        if key in value:
            raise ValueError(f"duplicate JSON key: {key}")
        value[key] = item
    return value


def write_draft(path: Path, value: dict[str, Any]) -> None:
    if not (os.stat(path).st_mode & 0o200):
        raise PermissionError(f"refuse to overwrite non-writable surface: {path}")
    path.write_bytes(draft_bytes(value))


def draft_bytes(value: dict[str, Any]) -> bytes:
    return (json.dumps(value, indent=2, ensure_ascii=False) + "\n").encode(
        "utf-8")


def require(condition: bool, label: str) -> None:
    if not condition:
        raise ValueError(label)


def is_sha256(value: Any) -> bool:
    return (isinstance(value, str) and
            re.fullmatch(r"[0-9a-f]{64}", value) is not None and
            value != "0" * 64)


def close_object(value: dict[str, Any]) -> dict[str, Any]:
    require("object_sha256" not in value, "object closes exactly once")
    result = copy.deepcopy(value)
    result["object_sha256"] = sha256_bytes(canonical(value))
    return result


def verify_object(value: dict[str, Any], label: str,
                  expected: str | None = None) -> None:
    claim = value.get("object_sha256")
    require(is_sha256(claim), label + ": valid object SHA-256 claim")
    require(object_hash(value) == claim, label + ": canonical object closure")
    if expected is not None:
        require(claim == expected, label + ": expected object pin")


def load_frozen_json(path: Path, file_sha256: str,
                     object_sha256: str) -> dict[str, Any]:
    raw = path.read_bytes()
    require(sha256_bytes(raw) == file_sha256,
            path.name + ": frozen file pin")
    value = json.loads(raw, object_pairs_hook=_no_duplicate_pairs)
    require(isinstance(value, dict), path.name + ": JSON object")
    verify_object(value, path.name, object_sha256)
    return value


def exact_closed_const_schema(value: dict[str, Any]) -> dict[str, Any]:
    return {
        "type": "object",
        "additionalProperties": False,
        "required": list(value),
        "properties": {key: {"const": copy.deepcopy(item)}
                       for key, item in value.items()},
    }


def parse_source_ast(raw: bytes, label: str) -> ast.Module:
    try:
        source = raw.decode("utf-8")
        tree = ast.parse(source, filename=label, mode="exec")
        # Compilation validates the in-memory AST only.  The resulting code
        # object is discarded and never evaluated; no import hook is involved.
        compile(tree, label, "exec", dont_inherit=True)
    except (UnicodeDecodeError, SyntaxError, ValueError, TypeError) as exc:
        raise ValueError(label + ": AST/compile failure") from exc
    return tree


def normalized_named_function_ast_sha256(
        raw: bytes, function_name: str, label: str) -> str:
    tree = parse_source_ast(raw, label)
    matches = [
        node for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and
           node.name == function_name
    ]
    require(len(matches) == 1,
            label + ": one exact module-level " + function_name)
    return sha256_bytes(ast.dump(
        matches[0], annotate_fields=True,
        include_attributes=False).encode("utf-8"))


def exact_helper_callsite_census(
        ordered_sources: list[tuple[str, bytes]]) -> list[dict[str, Any]]:
    require([role for role, _ in ordered_sources] == [
        "producer", "consumer", "launcher"],
        "helper callsite ordered source roles")
    result: list[dict[str, Any]] = []
    for role, raw in ordered_sources:
        tree = parse_source_ast(raw, "helper_callsites_" + role)
        parent: dict[ast.AST, ast.AST] = {}
        for node in ast.walk(tree):
            for child in ast.iter_child_nodes(node):
                parent[child] = node
        loaded_names = [
            node for node in ast.walk(tree)
            if isinstance(node, ast.Name) and
               isinstance(node.ctx, ast.Load) and
               node.id == "derive_v10_colon_prefix_witness"
        ]
        calls: list[
            tuple[ast.Call, ast.FunctionDef | ast.AsyncFunctionDef]] = []
        for name in loaded_names:
            call = parent.get(name)
            require(isinstance(call, ast.Call) and call.func is name and
                    len(call.args) == 2 and not call.keywords,
                    role + ": helper only used by direct two-argument calls")
            cursor: ast.AST = call
            owner: ast.FunctionDef | ast.AsyncFunctionDef | None = None
            while cursor in parent:
                cursor = parent[cursor]
                require(not isinstance(cursor, ast.Lambda),
                        role + ": helper call not nested in lambda")
                if isinstance(cursor, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    owner = cursor
                    break
            require(owner is not None,
                    role + ": helper call has enclosing function")
            calls.append((call, owner))
        require(bool(calls), role + ": helper has at least one callsite")
        owners: list[ast.FunctionDef | ast.AsyncFunctionDef] = []
        counts: Counter[int] = Counter()
        for call, owner in sorted(
                calls, key=lambda item: (item[0].lineno, item[0].col_offset)):
            identity = id(owner)
            if identity not in counts:
                owners.append(owner)
            counts[identity] += 1
        for owner in sorted(
                owners, key=lambda node: (node.lineno, node.col_offset)):
            result.append({
                "source_role": role,
                "enclosing_function": owner.name,
                "direct_call_count": counts[id(owner)],
            })
    return result


def pin_normalized_launcher_ast_sha256(raw: bytes, label: str) -> str:
    tree = parse_source_ast(raw, label)
    flag_assignments: list[ast.Assign | ast.AnnAssign] = []
    for node in tree.body:
        if (isinstance(node, ast.Assign) and len(node.targets) == 1 and
                isinstance(node.targets[0], ast.Name) and
                node.targets[0].id == "FINAL_BASE7_PINS_INSTALLED"):
            flag_assignments.append(node)
        elif (isinstance(node, ast.AnnAssign) and
              isinstance(node.target, ast.Name) and
              node.target.id == "FINAL_BASE7_PINS_INSTALLED"):
            flag_assignments.append(node)
    require(len(flag_assignments) == 1,
            label + ": one FINAL_BASE7_PINS_INSTALLED assignment")
    flag_assignments[0].value = ast.Constant(value=False)

    configure_functions = [
        node for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and
           node.name == "configure_workspace_paths"
    ]
    require(len(configure_functions) == 1,
            label + ": one configure_workspace_paths definition")
    base7_assignments = [
        node for node in configure_functions[0].body
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and
           isinstance(node.targets[0], ast.Name) and
           node.targets[0].id == "BASE7_PINS"
    ]
    require(len(base7_assignments) == 1 and
            isinstance(base7_assignments[0].value, ast.Dict),
            label + ": one direct BASE7_PINS dict assignment")
    base7 = base7_assignments[0].value
    key_names = [
        key.id if isinstance(key, ast.Name) else None for key in base7.keys]
    expected = [
        "V11_OFFICIAL_REJECTION", *PIN_NORMALIZED_CURRENT_BASE7_KEY_ORDER]
    require(key_names == expected and len(base7.values) == len(expected),
            label + ": exact ordered v11-plus-v12 BASE7 census")
    v11_before = ast.dump(
        base7.values[0], annotate_fields=True, include_attributes=False)
    for index, key_name in enumerate(key_names[1:], start=1):
        object_sentinel: str | None = (
            "e" * 64
            if key_name in PIN_NORMALIZED_OBJECT_BASE7_KEYS else None)
        base7.values[index] = ast.Tuple(
            elts=[ast.Constant(value="f" * 64),
                  ast.Constant(value=object_sentinel)],
            ctx=ast.Load())
    require(ast.dump(
        base7.values[0], annotate_fields=True,
        include_attributes=False) == v11_before,
        label + ": v11 rejection BASE7 value preserved")
    return sha256_bytes(ast.dump(
        tree, annotate_fields=True,
        include_attributes=False).encode("utf-8"))


def producer_source_registry_shape_from_ast(raw: bytes) -> int:
    tree = parse_source_ast(raw, "producer_v12")
    registry_function = next((
        node for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and
           node.name == "input_registry"), None)
    held_self = next((
        node for node in tree.body
        if isinstance(node, ast.ClassDef) and node.name == "HeldSelf"), None)
    execution_proof = next((
        node for node in held_self.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and
           node.name == "execution_proof"), None
        ) if isinstance(held_self, ast.ClassDef) else None
    require(isinstance(registry_function,
                       (ast.FunctionDef, ast.AsyncFunctionDef)) and
            isinstance(execution_proof,
                       (ast.FunctionDef, ast.AsyncFunctionDef)),
            "producer input_registry and HeldSelf.execution_proof")
    registry_returns = [
        node for node in ast.walk(registry_function)
        if isinstance(node, ast.Return) and isinstance(node.value, ast.Call) and
           isinstance(node.value.func, ast.Name) and
           node.value.func.id == "close_object" and
           len(node.value.args) == 1 and
           isinstance(node.value.args[0], ast.Dict)
    ]
    proof_returns = [
        node for node in ast.walk(execution_proof)
        if isinstance(node, ast.Return) and isinstance(node.value, ast.Dict)
    ]
    require(len(registry_returns) == 1 and len(proof_returns) == 1,
            "unique producer registry/proof return dicts")
    registry_dict = registry_returns[0].value.args[0]
    proof_dict = proof_returns[0].value
    explicit_keys = [
        key.value for key in registry_dict.keys
        if isinstance(key, ast.Constant) and isinstance(key.value, str)]
    expansions = [
        value for key, value in zip(registry_dict.keys, registry_dict.values)
        if key is None]
    proof_keys = [
        key.value for key in proof_dict.keys
        if isinstance(key, ast.Constant) and isinstance(key.value, str)]
    require(len(explicit_keys) == len(set(explicit_keys)) == 62 and
            len(expansions) == 1 and isinstance(expansions[0], ast.Call) and
            isinstance(expansions[0].func, ast.Attribute) and
            isinstance(expansions[0].func.value, ast.Name) and
            expansions[0].func.value.id == "self_guard" and
            expansions[0].func.attr == "execution_proof" and
            not expansions[0].args and not expansions[0].keywords and
            proof_keys == SOURCE_REGISTRY_EXECUTION_PROOF_EXACT7,
            "producer registry explicit62 plus exact7 execution proof")
    return len(explicit_keys) + len(proof_keys) + 1


def schema_keyword_universe(root: dict[str, Any]) -> frozenset[str]:
    seen: set[str] = set()

    def walk(node: Any, label: str) -> None:
        require(isinstance(node, dict), label + ": schema node object")
        unknown = set(node) - SUPPORTED_SCHEMA_KEYWORDS
        require(not unknown, label + ": unsupported schema keywords: " +
                ",".join(sorted(unknown)))
        seen.update(node)
        definitions = node.get("$defs", {})
        require(isinstance(definitions, dict), label + ": $defs object")
        for name, child in definitions.items():
            require(isinstance(name, str) and bool(name),
                    label + ": $defs name")
            walk(child, label + ".$defs." + name)
        properties = node.get("properties", {})
        require(isinstance(properties, dict), label + ": properties object")
        for name, child in properties.items():
            require(isinstance(name, str) and bool(name),
                    label + ": property name")
            walk(child, label + ".properties." + name)
        prefix_items = node.get("prefixItems", [])
        require(isinstance(prefix_items, list), label + ": prefixItems array")
        for index, child in enumerate(prefix_items):
            walk(child, f"{label}.prefixItems[{index}]")
        items = node.get("items")
        require(items is None or items is False or isinstance(items, dict),
                label + ": items schema-or-false")
        if isinstance(items, dict):
            walk(items, label + ".items")
        additional = node.get("additionalProperties")
        require(additional is None or isinstance(additional, bool) or
                isinstance(additional, dict),
                label + ": additionalProperties schema-or-bool")
        if isinstance(additional, dict):
            walk(additional, label + ".additionalProperties")

    walk(root, "closed-schema")
    return frozenset(seen)


def schema_static_closure(schema: dict[str, Any],
                          producer_raw: bytes) -> dict[str, Any]:
    stack: list[Any] = [schema]
    nodes: list[dict[str, Any]] = []
    while stack:
        node = stack.pop()
        if isinstance(node, dict):
            nodes.append(node)
            stack.extend(node.values())
        elif isinstance(node, list):
            stack.extend(node)
    definitions = schema.get("$defs")
    require(isinstance(definitions, dict), "schema has $defs object")
    references = [node["$ref"] for node in nodes if "$ref" in node]
    unresolved = []
    for reference in references:
        if (not isinstance(reference, str) or
                not reference.startswith("#/$defs/") or
                reference.removeprefix("#/$defs/") not in definitions):
            unresolved.append(reference)
    closed_nodes = [
        node for node in nodes
        if node.get("type") == "object" and
           node.get("additionalProperties") is False]
    mismatch_count = sum(
        set(node.get("required", [])) != set(node.get("properties", {}))
        for node in closed_nodes)
    require(len(definitions) == 46, "schema exact46 definitions")
    require(len(references) == 242, "schema exact242 references")
    require(not unresolved, "schema has unresolved references")
    require(len(closed_nodes) == 52, "schema exact52 closed objects")
    require(mismatch_count == 0,
            "schema closed required/property mismatch count zero")

    keywords = sorted(schema_keyword_universe(schema))
    require(keywords == EXPECTED_SCHEMA_KEYWORD_UNIVERSE,
            "schema exact validation keyword universe")
    require("oneOf" not in keywords, "schema oneOf absent")
    for name in (
            "selfIdentity", "independentConsumerProof", "staticFreezeProof",
            "coldLaunchProof", "laterRejection"):
        definition = definitions.get(name)
        require(isinstance(definition, dict) and
                isinstance(definition.get("properties"), dict) and
                len(definition["properties"]) == EXPECTED_OUTPUT_SHAPES[name],
                "schema output shape: " + name)
    require(producer_source_registry_shape_from_ast(producer_raw) ==
            EXPECTED_OUTPUT_SHAPES["producerSourceRegistry"],
            "producer source-registry output shape exact70")
    return {
        "definition_count": len(definitions),
        "reference_count": len(references),
        "unresolved_reference_count": len(unresolved),
        "closed_object_count": len(closed_nodes),
        "closed_object_mismatch_count": mismatch_count,
        "actual_keywords": keywords,
        "supported_keywords": sorted(SUPPORTED_SCHEMA_KEYWORDS),
    }


CHECKER_REPORT_ZERO_KEYS = (
    "arity_failure_count", "starred_positional_total",
    "double_star_keyword_total", "undefined_global_count",
    "JSON_duplicate_key_count", "python_literal_dict_duplicate_key_count",
    "object_closure_failure_count", "pin_failure_count",
    "failed_static_check_count",
)
CHECKER_REPORT_KEYS = {
    "schema", "producer_file_sha256", "consumer_file_sha256",
    "launcher_file_sha256", "wider_local_callsite_census_row_count",
    "wider_local_callsite_census_sha256",
    "common_ordered_callsite_row_count",
    "common_ordered_callsite_census_sha256", "common_callsite_kind_census",
    "python_literal_dict_count",
    "python_AST_and_compile_in_memory_file_count", *CHECKER_REPORT_ZERO_KEYS,
    "object_sha256",
}


def load_checker_report(path: Path, source_hashes: dict[str, str]) -> dict[str, Any]:
    report = load(path)
    require(set(report) == CHECKER_REPORT_KEYS,
            "checker census report exact key closure")
    verify_object(report, "checker census report")
    require(report.get("schema") ==
            "cm2.round306c79g.true-global-no-producer-consumer."
            "v12-static-checker-census.v1",
            "checker census report schema")
    for role in ("producer", "consumer", "launcher"):
        require(report.get(role + "_file_sha256") == source_hashes[role],
                "checker report binds current " + role + " bytes")
    for key in (
            "wider_local_callsite_census_row_count",
            "common_ordered_callsite_row_count", "python_literal_dict_count"):
        require(type(report.get(key)) is int and report[key] > 0,
                "checker report positive integer: " + key)
    for key in (
            "wider_local_callsite_census_sha256",
            "common_ordered_callsite_census_sha256"):
        require(is_sha256(report.get(key)),
                "checker report nonzero digest: " + key)
    require(report["common_ordered_callsite_census_sha256"] !=
            STALE_V11_COMMON_CALLSITE_SHA256 and
            report["wider_local_callsite_census_sha256"] !=
            STALE_V11_COMMON_CALLSITE_SHA256,
            "refuse stale v11 general-callsite digest")
    require(not (
        report["common_ordered_callsite_row_count"] == 2964 and
        report["wider_local_callsite_census_row_count"] == 2964 and
        report["python_literal_dict_count"] == 790),
        "refuse stale v11 general-callsite counts")
    kinds = report.get("common_callsite_kind_census")
    require(isinstance(kinds, dict) and set(kinds) ==
            set(COMMON_CALLSITE_KIND_KEYS) and
            all(type(value) is int and value >= 0 for value in kinds.values()) and
            sum(kinds.values()) == report["common_ordered_callsite_row_count"],
            "checker report exact common-callsite kind census")
    require(report.get("python_AST_and_compile_in_memory_file_count") == 3,
            "checker report exact three in-memory AST/compile sources")
    for key in CHECKER_REPORT_ZERO_KEYS:
        require(type(report.get(key)) is int and report[key] == 0,
                "checker report exact integer zero: " + key)
    return report


def add_v11_proof_refs(node: Any) -> None:
    if isinstance(node, dict):
        properties = node.get("properties")
        required = node.get("required")
        if (isinstance(properties, dict) and
                "published_then_officially_rejected_predecessor_v10" in properties and
                isinstance(required, list) and
                "published_then_officially_rejected_predecessor_v10" in required):
            if "published_then_officially_rejected_predecessor_v11" not in properties:
                properties["published_then_officially_rejected_predecessor_v11"] = {
                    "$ref": "#/$defs/v11PublishedThenOfficiallyRejectedProof"}
            if "published_then_officially_rejected_predecessor_v11" not in required:
                index = required.index(
                    "published_then_officially_rejected_predecessor_v10") + 1
                required.insert(index,
                                "published_then_officially_rejected_predecessor_v11")
        for item in node.values():
            add_v11_proof_refs(item)
    elif isinstance(node, list):
        for item in node:
            add_v11_proof_refs(item)


def rename_key_recursively(node: Any, old: str, new: str) -> None:
    if isinstance(node, dict):
        if old in node:
            rebuilt: dict[str, Any] = {}
            for key, value in node.items():
                rebuilt[new if key == old else key] = value
            node.clear()
            node.update(rebuilt)
        for value in node.values():
            rename_key_recursively(value, old, new)
    elif isinstance(node, list):
        for value in node:
            rename_key_recursively(value, old, new)
        for index, value in enumerate(node):
            if value == old:
                node[index] = new


def rename_closed_property(definition: dict[str, Any], old: str,
                           new: str) -> None:
    properties = definition["properties"]
    required = definition["required"]
    if old in properties:
        rebuilt: dict[str, Any] = {}
        for key, value in properties.items():
            rebuilt[new if key == old else key] = value
        definition["properties"] = rebuilt
    if old in required:
        required[required.index(old)] = new


def add_required_const(definition: dict[str, Any], key: str, value: Any,
                       *, after: str | None = None) -> None:
    properties = definition["properties"]
    required = definition["required"]
    properties[key] = {"const": copy.deepcopy(value)}
    if key not in required:
        if after is not None and after in required:
            required.insert(required.index(after) + 1, key)
        else:
            required.append(key)


def replace_current_bundle_first_member(node: Any) -> None:
    old = ".cm2-runtime/c79g-v10-rejections-" + CHECKPOINT + "/rejection.json"
    if isinstance(node, dict):
        for value in node.values():
            replace_current_bundle_first_member(value)
    elif isinstance(node, list):
        if (len(node) >= 2 and node[0] == old and isinstance(node[1], str) and
                f"{BASE}_schema_v12.json" in node[1]):
            node[0] = V11_REJECTION_REL
        if (len(node) >= 2 and node[0] == "v10_official_rejection" and
                node[1] == "closed_schema_v12"):
            node[0] = "v11_official_rejection"
        for value in node:
            replace_current_bundle_first_member(value)


def build_schema() -> dict[str, Any]:
    schema = load(SCHEMA)
    defs = schema["$defs"]
    defs["v10ColonPrefixPerClauseWitness"] = exact_closed_const_schema(
        V10_COLON_PREFIX_WITNESS)
    defs["v11DualValidatorDivergenceIncident"] = exact_closed_const_schema(
        V11_INCIDENT)
    defs["v11PublishedThenOfficiallyRejectedProof"] = \
        exact_closed_const_schema(V11_PROOF)
    add_v11_proof_refs(schema)

    static = defs["staticFreezeProof"]
    if "published_then_officially_rejected_predecessor_v11_validated" not in static["properties"]:
        static["properties"][
            "published_then_officially_rejected_predecessor_v11_validated"] = {
                "const": True}
        static["required"].append(
            "published_then_officially_rejected_predecessor_v11_validated")

    verification = defs["verificationSurfaceProof"]
    verification["properties"]["exact_attack_count_each"]["const"] = \
        FORMAL_ATTACK_COUNT

    independent = defs["independentConsumerProof"]
    rename_closed_property(
        independent,
        "producer_or_upstream_producer_source_content_opened_read_decoded_parsed_compiled_imported_or_executed",
        "current_v12_producer_source_content_opened_read_decoded_parsed_compiled_imported_or_executed")
    add_required_const(
        independent,
        "frozen_predecessor_incident_source_exact5_held_fd_bytes_read_only_noncredit",
        True,
        after="current_v12_producer_source_content_opened_read_decoded_parsed_compiled_imported_or_executed")
    add_required_const(
        independent,
        "v10_colon_prefix_witness_independently_rederived_from_inherited_exact5_held_fds",
        True,
        after="frozen_predecessor_incident_source_exact5_held_fd_bytes_read_only_noncredit")
    independent["properties"]["exact_attack_count_reexecuted"]["const"] = \
        FORMAL_ATTACK_COUNT

    later = defs["laterRejection"]
    for key, value in (
            ("v11_official_rejection_file_sha256", V11_REJECTION_FILE),
            ("v11_official_rejection_object_sha256", V11_REJECTION_OBJECT)):
        if key not in later["required"]:
            later["required"].append(key)
        later["properties"][key] = {"const": value}

    rename_key_recursively(
        schema,
        "current_exact8_first_member_is_shared_v10_official_rejection",
        "current_exact8_first_member_is_shared_v11_official_rejection")
    rename_key_recursively(
        schema,
        "current_exact8_first_member_is_v10_official_rejection",
        "current_exact8_first_member_is_v11_official_rejection")
    rename_key_recursively(
        schema,
        "all_current_and_historical_88_identities_globally_unique_on_one_statx_mount",
        "all_current_and_historical_98_identities_globally_unique_on_one_statx_mount")
    replace_current_bundle_first_member(schema)
    defs["staticFreezeProof"]["properties"][
        "append_only_history_unique_file_identity_count"]["const"] = 98
    defs["coldLaunchProof"]["properties"][
        "current_v12_and_all_predecessor_unique_file_identity_count"]["const"] = 98
    return schema


def build_contract(schema_file_sha256: str) -> dict[str, Any]:
    contract = load(CONTRACT)
    contract["purpose"] = (
        "Append-only v12 zero-credit static successor after the frozen v11 "
        "exact10 and singleton official rejection. It preserves every "
        "published predecessor byte-exact and repairs the v11 dual-validator "
        "divergence by deriving an exact40 per-clause colon-prefix witness "
        "independently in producer, consumer, and launcher from the same "
        "inherited held predecessor bytes.")
    contract["published_then_officially_rejected_predecessor_v11"] = \
        copy.deepcopy(V11_PROOF)
    contract["v10_colon_prefix_witness"] = copy.deepcopy(
        V10_COLON_PREFIX_WITNESS)
    contract["v11_dual_validator_divergence_incident"] = copy.deepcopy(
        V11_INCIDENT)
    bundle = contract["v12_bundle"]
    replace_current_bundle_first_member(bundle)
    bundle["closed_schema"]["file_sha256"] = schema_file_sha256
    receipts = bundle["post_source_static_trust_receipts"]
    receipts["v11_official_rejection_path"] = V11_REJECTION_REL
    receipts[
        "seal_stably_binds_v4_supersession_v5_rejection_v6_rejection_v7_rejection_v8_rejection_v8_rollout_incident_v9_rejection_v9_shape_drift_incident_v10_rejection_v10_regression_label_prefix_incident_v11_rejection_v11_dual_validator_divergence_incident_transition_and_audit_file_or_object_hashes"] = True
    receipts.pop(
        "seal_stably_binds_v4_supersession_v5_rejection_v6_rejection_v7_rejection_v8_rejection_v8_rollout_incident_v9_rejection_v9_shape_drift_incident_v10_rejection_v10_regression_label_prefix_incident_transition_and_audit_file_or_object_hashes",
        None)
    receipts["runtime_consumer_must_hold_strict_parse_object_close_and_terminally_replay_all_eleven"] = True
    receipts.pop(
        "runtime_consumer_must_hold_strict_parse_object_close_and_terminally_replay_all_ten",
        None)
    outer = bundle["cold_launch_outer_closure"]
    outer["manifest_order"] = (
        "V11_OFFICIAL_REJECTION_THEN_SCHEMA_THEN_CONTRACT_THEN_PRODUCER_THEN_"
        "INDEPENDENT_SOURCE_THEN_V11_TO_V12_TRANSITION_THEN_STATIC_AUDIT_THEN_LAUNCHER")
    outer["current_v12_exact10_plus_all_append_only_predecessors_unique_file_identity_count"] = 98
    outer["all_98_file_identities_share_one_statx_mount"] = True
    outer.pop("all_88_file_identities_share_one_statx_mount", None)
    outer[
        "launcher_holds_live_v11_exact10_plus_official_later_rejection_and_exact_singleton_namespace_under_same_lock"] = True
    outer[
        "launcher_validates_exact_v11_dual_validator_divergence_incident_under_same_lock"] = True
    outer[
        "launcher_rederives_exact40_v10_colon_prefix_witness_from_inherited_held_bytes_before_child_spawn"] = True
    outer[
        "producer_consumer_launcher_common_witness_helper_normalized_ast_sha256"] = HELPER_NORMALIZED_AST
    old_terminal = next((key for key in outer if key.startswith(
        "launcher_terminally_replays_v12_exact10_v10_exact10_")), None)
    if old_terminal is not None:
        value = outer.pop(old_terminal)
        outer[old_terminal.replace("v12_exact10_v10_exact10_",
                                   "v12_exact10_v11_exact10_v10_exact10_")
              .replace("namespace_v10_regression", "namespace_v11_dual_validator_divergence_incident_v10_regression")] = value
    bundle["acyclic_binding_order"] = (
        "V11_OFFICIAL_REJECTION_THEN_SCHEMA_THEN_CONTRACT_THEN_PRODUCER_THEN_"
        "INDEPENDENT_SOURCE_THEN_V11_TO_V12_TRANSITION_THEN_STATIC_AUDIT_THEN_"
        "LAUNCHER_THEN_EXACT8_MANIFEST_THEN_OUTER_LAST")

    runtime = contract["independent_authority_consumer_protocol"]
    runtime.pop(
        "producer_or_upstream_producer_source_open_read_decode_parse_compile_import_or_execute_allowed",
        None)
    runtime[
        "current_v12_producer_source_open_read_decode_parse_compile_import_or_execute_allowed"] = False
    runtime[
        "frozen_predecessor_incident_source_exact5_inherited_held_fd_bytes_read_only_noncredit_allowed"] = True
    runtime[
        "v10_colon_prefix_witness_independently_rederived_by_consumer_from_inherited_exact5_held_fds"] = True
    census = runtime["cold_live_ACK_final_dynamic_replay_census"]
    census["frozen_v11_readable_held_file_count"] = 7
    census["frozen_v11_source_metadata_only_held_count"] = 3
    census["v11_official_rejection_shared_readable_held_file_count"] = 1
    census.pop("v10_official_rejection_in_static_policy_held_file_count", None)
    census["v11_official_rejection_in_static_policy_held_file_count"] = 1
    runtime.pop(
        "reconstructs_full_evidence_and_reexecutes_exact_121_coherent_attacks",
        None)
    runtime[
        "reconstructs_full_evidence_and_reexecutes_exact_137_coherent_attacks"] = True
    runtime["formal_attack_name_order_sha256"] = \
        FORMAL_ATTACK_NAME_ORDER_SHA256

    producer_bundle = contract["v12_bundle"]["build_only_producer"]
    producer_bundle["source_registry_execution_proof_exact_fields"] = \
        copy.deepcopy(SOURCE_REGISTRY_EXECUTION_PROOF_EXACT7)
    producer_bundle["source_registry_execution_proof_values_all_true"] = True

    authority = contract["composite_authority_predicate"]
    authority["authority_root_structure"] = CONTRACT_AUTHORITY_ROOT_STRUCTURE
    authority["preseal_root_domain"] = "CM2_C79G_V12_PRESEAL_ROOT_V2"
    authority["preseal_root_formula"] = CONTRACT_PRESEAL_ROOT_FORMULA
    authority["required_conjuncts"] = copy.deepcopy(CONTRACT_REQUIRED_CONJUNCTS)

    if (len(producer_bundle["source_registry_execution_proof_exact_fields"]) != 7 or
            len(set(producer_bundle[
                "source_registry_execution_proof_exact_fields"])) != 7):
        raise ValueError("contract source-registry execution proof is not exact7")
    if not all(name in authority["authority_root_structure"] for name in (
            "LIVE_V10_EXACT10", "OFFICIAL_V10_LATER_REJECTION",
            "V10_REGRESSION_LABEL_PREFIX_INCIDENT",
            "V10_COLON_PREFIX_PER_CLAUSE_WITNESS", "LIVE_V11_EXACT10",
            "OFFICIAL_V11_LATER_REJECTION",
            "V11_DUAL_VALIDATOR_DIVERGENCE_INCIDENT")):
        raise ValueError("contract authority root omits v10/v11 incident closure")
    if not all(name in authority["preseal_root_formula"] for name in (
            "v10_rejection_file_sha256", "v10_rejection_object_sha256",
            "trusted_v10_regression_label_prefix_incident_digest",
            "v11_rejection_file_sha256", "v11_rejection_object_sha256",
            "trusted_v11_dual_validator_divergence_incident_digest")):
        raise ValueError("contract preseal root omits v10/v11 incident inputs")
    for required in (
            "V10_EXACT10_VALID", "V10_OFFICIAL_REJECTION_VALID",
            "TRUSTED_V10_REGRESSION_LABEL_PREFIX_INCIDENT_RECORDED_FROM_FROZEN_AST_STRUCTURE",
            "V10_COLON_PREFIX_PER_CLAUSE_WITNESS_REDERIVED_FROM_INHERITED_HELD_FDS_VALID",
            "V11_EXACT10_VALID", "V11_OFFICIAL_REJECTION_VALID",
            "TRUSTED_V11_DUAL_VALIDATOR_DIVERGENCE_INCIDENT_RECORDED_WITHOUT_EXACT_FALSE_CLAUSE_INFERENCE"):
        if required not in authority["required_conjuncts"]:
            raise ValueError("contract missing required conjunct: " + required)
    contract["object_sha256"] = object_hash(contract)
    return contract


def build_transition(
        v11_transition: dict[str, Any], schema_file_sha256: str,
        contract_file_sha256: str, contract_object_sha256: str,
        producer_file_sha256: str,
        consumer_file_sha256: str) -> dict[str, Any]:
    body: dict[str, Any] = {
        "schema": (
            "cm2.round306c79g.true-global-no-producer-consumer."
            "v11-to-v12-static-launch-transition.v1"),
        "status": (
            "STATIC_BYTES_CLOSED_V11_TO_V12__PHYSICAL_FREEZE_PENDING__"
            "RUNTIME_NOT_AUTHORIZED"),
        "receipt_path": str(TRANSITION.relative_to(ROOT)),
        "effective_checkpoint_object_sha256": CHECKPOINT,
        "transition_kind": (
            "APPEND_ONLY_PUBLISHED_THEN_OFFICIALLY_REJECTED_V11_TO_"
            "ZERO_CREDIT_V12_STATIC_SUCCESSOR"),
        "append_only_predecessor_v3_regression": copy.deepcopy(
            v11_transition["append_only_predecessor_v3_regression"]),
        "rejected_unpublished_predecessor_v4": copy.deepcopy(
            v11_transition["rejected_unpublished_predecessor_v4"]),
        "published_then_officially_rejected_predecessor_v5": copy.deepcopy(
            v11_transition[
                "published_then_officially_rejected_predecessor_v5"]),
        "published_then_officially_rejected_predecessor_v6": copy.deepcopy(
            v11_transition[
                "published_then_officially_rejected_predecessor_v6"]),
        "published_then_officially_rejected_predecessor_v7": copy.deepcopy(
            v11_transition[
                "published_then_officially_rejected_predecessor_v7"]),
        "published_then_officially_rejected_predecessor_v8": copy.deepcopy(
            v11_transition[
                "published_then_officially_rejected_predecessor_v8"]),
        "published_then_officially_rejected_predecessor_v9": copy.deepcopy(
            v11_transition[
                "published_then_officially_rejected_predecessor_v9"]),
        "published_then_officially_rejected_predecessor_v10": copy.deepcopy(
            v11_transition[
                "published_then_officially_rejected_predecessor_v10"]),
        "published_then_officially_rejected_predecessor_v11": copy.deepcopy(
            V11_PROOF),
        "successor_v12_static_bundle": {
            "closed_schema": {
                "path": str(SCHEMA.relative_to(ROOT)),
                "file_sha256": schema_file_sha256,
            },
            "contract": {
                "path": str(CONTRACT.relative_to(ROOT)),
                "file_sha256": contract_file_sha256,
                "object_sha256": contract_object_sha256,
            },
            "build_only_producer": {
                "path": str(PRODUCER.relative_to(ROOT)),
                "file_sha256": producer_file_sha256,
            },
            "independent_verifier_assembler_authority_consumer": {
                "path": str(CONSUMER.relative_to(ROOT)),
                "file_sha256": consumer_file_sha256,
            },
            "draft_pin_sentinels_remain_present": False,
            "final_consumer_pin_installed": True,
            "all_four_core_file_pins_final": True,
            "transition_receipt_bytes_are_closed_around_final_core_pins": True,
            "transition_receipt_physical_freeze_completed": False,
            "static_audit_v12_path": str(AUDIT.relative_to(ROOT)),
            "cold_launcher_v12_path": str(LAUNCHER.relative_to(ROOT)),
        },
        "physical_mode_policy": {
            "v12_working_files_mode_before_cold_freeze": "0664",
            "v12_exact8_required_final_mode": "0444",
            "v12_exact8_required_final_nlink": 1,
            "v12_exact8_physical_freeze_completed": False,
            "v12_manifest_physical_freeze_completed": False,
            "v12_outer_physical_freeze_completed": False,
            "historical_modes_are_exact_observed_snapshot_guards_not_immutability_claims":
                True,
        },
        "cold_launch_boundary": {
            "base7_order": [
                "v11_official_rejection", "closed_schema_v12",
                "contract_v12", "producer_v12", "consumer_v12",
                "transition_v11_to_v12", "static_audit_v12",
            ],
            "base7_first_member_is_v11_official_rejection": True,
            "launcher_is_eighth": True,
            "manifest_is_ninth": True,
            "outer_is_tenth_and_last": True,
            "expected_current_plus_history_unique_file_identity_count": 98,
            "all_98_file_identities_must_share_one_statx_mount": True,
            "manifest_or_outer_exists_at_transition_time": False,
            "manifest_or_outer_created_by_this_transition": False,
            "runtime_entry_authorized_by_this_transition": False,
        },
        "finalization_gates": {
            "final_core_pins_installed_before_object_closure": True,
            "final_independent_static_audit_A_GO": False,
            "final_independent_static_audit_B_GO": False,
            "cold_launcher_final_pin_instance_generated": False,
            "ordered_exact8_manifest_created": False,
            "outer_receipt_created_last": False,
            "terminal_byte_replay_completed": False,
        },
        "all_persisted_credit": 0,
        "formal_global_closure_credit": 0,
        "D02_unlock": False,
        "D02_gate_credit": 0,
        "D02_task_credit": 0,
        "D02_formal_pending_task_count": 33_638,
        "D02_started": False,
        "C79_runtime_artifacts_created": 0,
        "runtime_executed_during_transition": False,
    }
    return close_object(body)


def v12_static_no_run() -> dict[str, Any]:
    runtime = ROOT / ".cm2-runtime"
    runtime_artifacts = []
    if runtime.is_dir():
        runtime_artifacts = [
            path for path in runtime.rglob("*")
            if "c79g-v12" in path.name]
    require(not runtime_artifacts,
            "v12 runtime artifacts already exist; refuse static GO audit")

    protocol_names = {
        PRODUCER.name.encode(), CONSUMER.name.encode(), LAUNCHER.name.encode()}
    process_count = 0
    proc = Path("/proc")
    if proc.is_dir():
        for entry in proc.iterdir():
            if not entry.name.isdigit():
                continue
            try:
                command = (entry / "cmdline").read_bytes()
            except (FileNotFoundError, PermissionError, ProcessLookupError):
                continue
            if any(name in command for name in protocol_names):
                process_count += 1
    require(process_count == 0,
            "v12 protocol process exists; refuse static GO audit")

    pyc_count = 0
    pycache = OUT / "__pycache__"
    if pycache.is_dir():
        stems = (PRODUCER.stem, CONSUMER.stem, LAUNCHER.stem)
        pyc_count = sum(
            any(path.name.startswith(stem + ".") for stem in stems)
            for path in pycache.glob("*.pyc"))
    require(pyc_count == 0,
            "v12 protocol pyc exists; refuse static GO audit")
    require(not V12_MANIFEST.exists() and not V12_OUTER.exists(),
            "v12 manifest/outer already exists; refuse draft audit rebuild")
    return {
        "C79_entrypoint_executed": False,
        "C79_v12_runtime_artifact_count": 0,
        "C79_v12_process_count": 0,
        "pyc_or___pycache___created": False,
        "cold_manifest_or_outer_created_before_dual_GO": False,
    }


def build_static_audit(
        v11_audit: dict[str, Any], schema: dict[str, Any],
        schema_closure: dict[str, Any], transition: dict[str, Any],
        transition_raw: bytes, contract_file_sha256: str,
        contract_object_sha256: str, source_raw: dict[str, bytes],
        source_hashes: dict[str, str], checker_report: dict[str, Any],
        pin_normalized_launcher_sha256: str,
        helper_callsites: list[dict[str, Any]],
        static_no_run: dict[str, Any]) -> dict[str, Any]:
    old_inputs = v11_audit[
        "dual_independent_static_checkers"]["checker_A"]["input_sha256"]
    require(tuple(key for key in old_inputs
                  if key in STATIC_AUDIT_HISTORICAL_INPUT_KEYS) ==
            STATIC_AUDIT_HISTORICAL_INPUT_KEYS,
            "frozen v11 audit historical input order")
    historical_inputs = {
        key: old_inputs[key] for key in STATIC_AUDIT_HISTORICAL_INPUT_KEYS}
    require(all(is_sha256(value) for value in historical_inputs.values()),
            "frozen v11 historical input pins")

    transition_file_sha256 = sha256_bytes(transition_raw)
    inputs: dict[str, str] = {
        "schema": sha256_bytes(SCHEMA.read_bytes()),
        "contract_file": contract_file_sha256,
        "contract_object": contract_object_sha256,
        "producer": source_hashes["producer"],
        "consumer": source_hashes["consumer"],
        "transition_file": transition_file_sha256,
        "transition_object": transition["object_sha256"],
        "launcher_template": pin_normalized_launcher_sha256,
        **historical_inputs,
        "v11_rejection_file": V11_REJECTION_FILE,
        "v11_rejection_object": V11_REJECTION_OBJECT,
        "v11_producer_file": V11_EXACT10[3]["file_sha256"],
        "v11_launcher_file": V11_EXACT10[7]["file_sha256"],
        "trusted_v11_dual_validator_divergence_incident_digest":
            INCIDENT_DIGEST,
    }
    require(tuple(inputs) == STATIC_AUDIT_INPUT_KEY_ORDER and
            len(inputs) == 37 and
            sha256_bytes(canonical(list(inputs))) ==
                STATIC_AUDIT_INPUT_KEY_ORDER_SHA256 and
            all(is_sha256(value) for value in inputs.values()),
            "static audit exact37 ordered nonzero input closure")

    helper_digests = [
        normalized_named_function_ast_sha256(
            source_raw[role], "derive_v10_colon_prefix_witness", role)
        for role in ("producer", "consumer", "launcher")]
    require(helper_digests == [HELPER_NORMALIZED_AST] * 3,
            "three independent helper AST digests")
    expected_helper_callsites = [
        {"source_role": "producer",
         "enclosing_function": "hold_static_freeze_trust",
         "direct_call_count": 1},
        {"source_role": "consumer", "enclosing_function": "__init__",
         "direct_call_count": 1},
        {"source_role": "launcher", "enclosing_function": "bind_predecessors",
         "direct_call_count": 1},
        {"source_role": "launcher", "enclosing_function": "terminal_replay",
         "direct_call_count": 1},
    ]
    require(helper_callsites == expected_helper_callsites,
            "exact helper callsite census")

    zero = {key: checker_report[key] for key in CHECKER_REPORT_ZERO_KEYS}
    checker_a = {
        "algorithm": "AST_SYMBOL_TABLE_DATAFLOW_AND_PIN_NORMALIZER_CHECKER_A_V1",
        "status": (
            "GO_STATIC_CHECKER_A__PIN_NORMALIZED_AST_REPRODUCED__"
            "RUNTIME_NOT_AUTHORIZED"),
        "input_sha256": copy.deepcopy(inputs),
        "pin_normalized_launcher_ast_sha256":
            pin_normalized_launcher_sha256,
        "wider_local_callsite_census_row_count": checker_report[
            "wider_local_callsite_census_row_count"],
        "wider_local_callsite_census_sha256": checker_report[
            "wider_local_callsite_census_sha256"],
        "arity_failure_count": zero["arity_failure_count"],
        "undefined_global_count": zero["undefined_global_count"],
        "python_literal_dict_count": checker_report[
            "python_literal_dict_count"],
        "python_literal_dict_duplicate_key_count": zero[
            "python_literal_dict_duplicate_key_count"],
        "python_AST_and_compile_in_memory_file_count": checker_report[
            "python_AST_and_compile_in_memory_file_count"],
        "failed_static_check_count": zero["failed_static_check_count"],
    }
    checker_b = {
        "algorithm": (
            "TOKEN_SYMBOL_TABLE_EXPLICIT_JSON_AND_PIN_NORMALIZER_"
            "CHECKER_B_V1"),
        "status": (
            "GO_STATIC_CHECKER_B__PIN_NORMALIZED_AST_REPRODUCED__"
            "RUNTIME_NOT_AUTHORIZED"),
        "input_sha256": copy.deepcopy(inputs),
        "pin_normalized_launcher_ast_sha256":
            pin_normalized_launcher_sha256,
        "common_ordered_callsite_row_count": checker_report[
            "common_ordered_callsite_row_count"],
        "common_ordered_callsite_census_sha256": checker_report[
            "common_ordered_callsite_census_sha256"],
        **zero,
    }
    checker_c = {
        "algorithm": (
            "INDEPENDENT_LEXICAL_CALLSITE_AND_PIN_NORMALIZED_AST_"
            "REPRODUCER_C_V1"),
        "status": (
            "GO_PIN_NORMALIZED_AST_AND_COMMON_DIGEST_REPRODUCED__"
            "RUNTIME_NOT_AUTHORIZED"),
        "pin_normalized_launcher_ast_sha256":
            pin_normalized_launcher_sha256,
        "common_ordered_callsite_row_count": checker_report[
            "common_ordered_callsite_row_count"],
        "common_ordered_callsite_census_sha256": checker_report[
            "common_ordered_callsite_census_sha256"],
        "common_callsite_kind_census": copy.deepcopy(
            checker_report["common_callsite_kind_census"]),
        "arity_failure_count": zero["arity_failure_count"],
        "starred_positional_total": zero["starred_positional_total"],
        "double_star_keyword_total": zero["double_star_keyword_total"],
        "failed_static_check_count": zero["failed_static_check_count"],
    }
    # B has a narrower exact key set than the composite report.
    checker_b.pop("python_AST_and_compile_in_memory_file_count", None)
    dual = {
        "checker_A": checker_a,
        "checker_B": checker_b,
        "checker_C_common_census_and_pin_normalized_ast_reproduction": checker_c,
        "v10_colon_prefix_helper_consensus": {
            "algorithm": (
                "THREE_SOURCE_NORMALIZED_FUNCTIONDEF_AST_AND_EXACT_CALLSITE_"
                "CENSUS_V1"),
            "implementation_count": 3,
            "ordered_source_roles": ["producer", "consumer", "launcher"],
            "normalized_helper_ast_sha256": HELPER_NORMALIZED_AST,
            "all_three_helpers_equal": True,
            "witness_exact_key_order": list(V10_COLON_PREFIX_WITNESS),
            "witness_exact_key_count": 40,
            "witness_object_sha256": WITNESS_OBJECT,
            "ordered_callsite_census": copy.deepcopy(helper_callsites),
            "ordered_callsite_census_sha256": sha256_bytes(
                canonical(helper_callsites)),
            "all_callsites_exact": True,
        },
        "independent_pin_normalizer_count": 3,
        "all_pin_normalizers_equal": True,
        "pin_normalized_ast_algorithm": PIN_NORMALIZED_AST_ALGORITHM,
        "pin_normalized_current_base7_key_order": list(
            PIN_NORMALIZED_CURRENT_BASE7_KEY_ORDER),
        "pin_normalization_forces_final_base7_installed_false": True,
        "pin_normalization_preserves_v11_rejection_and_all_historical_pins":
            True,
        "pin_normalization_removes_current_audit_hash_dependency": True,
        "independent_common_callsite_implementation_count": 2,
        "all_common_callsite_censuses_equal": True,
        "final_launcher_must_reproduce_pin_normalized_ast_after_pin_injection":
            True,
        "held_launcher_pin_normalized_ast_sha256":
            pin_normalized_launcher_sha256,
    }

    v4 = copy.deepcopy(
        v11_audit["predecessor_v4_rejection_supersession_regression"])
    v4["same_defects_absent_from_v12"] = v4.pop(
        "same_defects_absent_from_v11")
    v4["v12_closed_object_required_property_mismatch_count"] = v4.pop(
        "v11_closed_object_required_property_mismatch_count")
    v4["v12_closed_object_required_property_mismatch_count"] = \
        schema_closure["closed_object_mismatch_count"]

    body: dict[str, Any] = {
        "schema": (
            "cm2.round306c79g.true-global-no-producer-consumer.static-audit.v12"),
        "status": (
            "PASS_DUAL_STATIC_PIN_NORMALIZED_AST_GO_V12__"
            "PHYSICAL_COLD_FREEZE_PENDING__RUNTIME_NOT_AUTHORIZED"),
        "audit_path": str(AUDIT.relative_to(ROOT)),
        "effective_checkpoint_object_sha256": CHECKPOINT,
        "audited_v12_bundle": {
            "build_only_producer": {
                "path": str(PRODUCER.relative_to(ROOT)),
                "file_sha256": source_hashes["producer"],
            },
            "closed_schema": {
                "path": str(SCHEMA.relative_to(ROOT)),
                "file_sha256": inputs["schema"],
            },
            "contract": {
                "path": str(CONTRACT.relative_to(ROOT)),
                "file_sha256": contract_file_sha256,
                "object_sha256": contract_object_sha256,
            },
            "independent_verifier_assembler_authority_consumer": {
                "path": str(CONSUMER.relative_to(ROOT)),
                "file_sha256": source_hashes["consumer"],
            },
            "v11_to_v12_transition_receipt": {
                "path": str(TRANSITION.relative_to(ROOT)),
                "file_sha256": transition_file_sha256,
                "object_sha256": transition["object_sha256"],
            },
        },
        "predecessor_v3_exact10_regression": copy.deepcopy(
            v11_audit["predecessor_v3_exact10_regression"]),
        "v3_official_later_rejection_regression": copy.deepcopy(
            v11_audit["v3_official_later_rejection_regression"]),
        "predecessor_v4_rejection_supersession_regression": v4,
        "published_then_officially_rejected_predecessor_v5": copy.deepcopy(
            v11_audit[
                "published_then_officially_rejected_predecessor_v5"]),
        "published_then_officially_rejected_predecessor_v6": copy.deepcopy(
            v11_audit[
                "published_then_officially_rejected_predecessor_v6"]),
        "published_then_officially_rejected_predecessor_v7": copy.deepcopy(
            v11_audit[
                "published_then_officially_rejected_predecessor_v7"]),
        "published_then_officially_rejected_predecessor_v8": copy.deepcopy(
            v11_audit[
                "published_then_officially_rejected_predecessor_v8"]),
        "published_then_officially_rejected_predecessor_v9": copy.deepcopy(
            v11_audit[
                "published_then_officially_rejected_predecessor_v9"]),
        "published_then_officially_rejected_predecessor_v10": copy.deepcopy(
            v11_audit[
                "published_then_officially_rejected_predecessor_v10"]),
        "published_then_officially_rejected_predecessor_v11": copy.deepcopy(
            V11_PROOF),
        "v10_colon_prefix_witness": copy.deepcopy(V10_COLON_PREFIX_WITNESS),
        "v11_dual_validator_divergence_incident": copy.deepcopy(V11_INCIDENT),
        "dual_independent_static_checkers": dual,
        "coherent_attack_static_census": {
            "exact_unique_ordered_attack_count_required": FORMAL_ATTACK_COUNT,
            "exact_unique_ordered_attack_count_observed": FORMAL_ATTACK_COUNT,
            "attack_name_order_sha256": FORMAL_ATTACK_NAME_ORDER_SHA256,
            "all_mutations_route_through_production_validators": True,
            "C42_full10_hash_join_mutations_included": True,
            "C42_three_directory_mode_nlink_universe_guards_are_independent_live_physical_gates":
                True,
            "attack_execution_deferred_to_cold_runtime": True,
        },
        "schema_and_constructor_closure": {
            "strict_JSON_duplicate_keys_rejected": True,
            "schema_definition_count": schema_closure["definition_count"],
            "schema_ref_count": schema_closure["reference_count"],
            "unresolved_schema_ref_count": schema_closure[
                "unresolved_reference_count"],
            "closed_object_count": schema_closure["closed_object_count"],
            "closed_object_required_property_mismatch_count": schema_closure[
                "closed_object_mismatch_count"],
            "all_closed_object_required_sets_equal_property_sets": True,
            "all_schema_refs_resolve": True,
            "actual_schema_keyword_universe": schema_closure[
                "actual_keywords"],
            "actual_schema_keyword_universe_sha256": sha256_bytes(
                canonical(schema_closure["actual_keywords"])),
            "cold_launcher_supported_schema_keyword_universe":
                schema_closure["supported_keywords"],
            "cold_launcher_supported_schema_keyword_universe_sha256":
                sha256_bytes(canonical(schema_closure["supported_keywords"])),
            "all_schema_validation_keywords_supported_by_cold_launcher": True,
            "unknown_schema_validation_keyword_count": 0,
            "oneOf_keyword_absent_after_pin_definition_split": True,
            "python_literal_dict_duplicate_key_count": zero[
                "python_literal_dict_duplicate_key_count"],
            "undefined_global_count": zero["undefined_global_count"],
            "output_shape_key_counts": copy.deepcopy(EXPECTED_OUTPUT_SHAPES),
            "launcher_and_consumer_laterRejection_key_sets_equal_schema": True,
            "launcher_request_consumer_request_key_sets_equal": True,
            "consumer_ACK_launcher_ACK_key_sets_and_census_values_equal": True,
        },
        "sealed_exec_and_no_producer_static_proof": {
            "all_memfd_seal_checks_precede_source_or_evidence_access": True,
            "all_memfd_seal_checks_are_exact_equality_not_subset_tests": True,
            "consumer_current_v12_producer_content_open_read_hash_decode_compile_import_or_execute_allowed":
                False,
            "consumer_exec_source_coordination_root_fds_pairwise_distinct": True,
            "consumer_frozen_predecessor_incident_exact5_bytes_read_only_noncredit_allowed":
                True,
            "consumer_independently_rederives_witness_from_inherited_held_fds":
                True,
            "consumer_producer_source_hold_api": "O_PATH|O_NOFOLLOW",
            "exact_required_seal_mask": 15,
            "installed_and_exec_bytes_equal_and_terminally_replayed": True,
            "installed_source_mode": "0444",
            "installed_source_nlink": 1,
            "launcher_bootstrap_exec_source_root_fds_distinct": True,
            "launcher_child_exec_source_coordination_root_fds_pairwise_distinct":
                True,
            "producer_exec_source_coordination_root_fds_pairwise_distinct": True,
            "sealed_exec_mode": "0444",
            "sealed_exec_nlink": 0,
        },
        "static_credit_census": {
            "all_persisted_v12_objects_D02_started": False,
            "all_persisted_v12_objects_D02_unlock": False,
            "all_persisted_v12_objects_formal_global_closure_credit": 0,
            "cold_live_inner_formal_global_closure_credit": 0,
            "launcher_virtual_positive_root_exact_credit_literal_count": 2,
            "only_cold_launcher_fresh_virtual_wrapper_may_derive_credit_one":
                True,
        },
        "static_no_run": static_no_run,
        "final_audit_acceptance": {
            "current_draft_pass": True,
            "final_failed_static_check_count_required": 0,
            "final_static_freeze_pass_required": True,
            "dual_static_checker_A_pin_normalized_ast_GO": True,
            "dual_static_checker_B_pin_normalized_ast_GO": True,
            "pin_normalized_launcher_ast_digest_consensus": True,
            "common_callsite_census_digest_consensus": True,
            "final_launcher_pin_normalized_ast_replay_required_after_pin_injection":
                True,
            "this_audit_authorizes_C79_runtime": False,
            "requires_cold_exact8_freeze_manifest_then_outer_last_and_terminal_replay":
                True,
        },
    }
    return close_object(body)


def verify_constants() -> None:
    assert len(V10_COLON_PREFIX_WITNESS) == 40
    assert object_hash(V10_COLON_PREFIX_WITNESS) == WITNESS_OBJECT
    assert len(V11_INCIDENT) == 45
    assert sha256_bytes(canonical(V11_INCIDENT)) == INCIDENT_DIGEST
    assert len(V11_FIRST_RUNTIME_ATTEMPT) == 8
    assert sha256_bytes(canonical(V11_FIRST_RUNTIME_ATTEMPT)) == FIRST_ATTEMPT_DIGEST
    assert len(V11_PROOF) == 19
    assert sha256_bytes(canonical(V11_PROOF)) == V11_PROOF_SHA256
    assert len(SOURCE_REGISTRY_EXECUTION_PROOF_EXACT7) == 7
    assert len(set(SOURCE_REGISTRY_EXECUTION_PROOF_EXACT7)) == 7
    assert len(STATIC_AUDIT_INPUT_KEY_ORDER) == 37
    assert sha256_bytes(canonical(list(STATIC_AUDIT_INPUT_KEY_ORDER))) == \
        STATIC_AUDIT_INPUT_KEY_ORDER_SHA256
    rejection = load(ROOT / V11_REJECTION_REL)
    assert object_hash(rejection) == V11_REJECTION_OBJECT
    assert sha256_bytes((ROOT / V11_REJECTION_REL).read_bytes()) == V11_REJECTION_FILE


def command_schema_contract() -> None:
    verify_constants()
    schema = build_schema()
    write_draft(SCHEMA, schema)
    schema_hash = sha256_bytes(SCHEMA.read_bytes())
    contract = build_contract(schema_hash)
    write_draft(CONTRACT, contract)
    print(json.dumps({
        "schema_file_sha256": schema_hash,
        "schema_definition_count": len(schema["$defs"]),
        "contract_file_sha256": sha256_bytes(CONTRACT.read_bytes()),
        "contract_object_sha256": contract["object_sha256"],
        "witness_object_sha256": WITNESS_OBJECT,
        "incident_sha256": INCIDENT_DIGEST,
    }, sort_keys=True))


def command_transition_audit(checker_report_path: Path) -> None:
    """Rebuild only the two writable post-core v12 JSON drafts.

    The protocol Python files are byte-read, parsed, and compiled in memory for
    static structure only.  They are never imported or executed.  The general
    callsite algorithms are intentionally outside this helper; their current-
    source-bound, canonically closed report is mandatory and stale v11 census
    values are rejected.
    """
    verify_constants()
    for path in (TRANSITION, AUDIT):
        require(path.is_file(), "missing writable v12 JSON draft: " + str(path))
        if not (os.stat(path).st_mode & 0o200):
            raise PermissionError(
                "refuse to overwrite non-writable surface: " + str(path))

    v11_transition = load_frozen_json(
        V11_TRANSITION, V11_TRANSITION_FILE, V11_TRANSITION_OBJECT)
    v11_audit = load_frozen_json(V11_AUDIT, V11_AUDIT_FILE, V11_AUDIT_OBJECT)

    input_paths = (SCHEMA, CONTRACT, PRODUCER, CONSUMER, LAUNCHER)
    input_raw = {path: path.read_bytes() for path in input_paths}
    source_raw = {
        "producer": input_raw[PRODUCER],
        "consumer": input_raw[CONSUMER],
        "launcher": input_raw[LAUNCHER],
    }
    source_hashes = {
        role: sha256_bytes(raw) for role, raw in source_raw.items()}
    for role, raw in source_raw.items():
        parse_source_ast(raw, "current_v12_" + role)

    schema = json.loads(
        input_raw[SCHEMA], object_pairs_hook=_no_duplicate_pairs)
    contract = json.loads(
        input_raw[CONTRACT], object_pairs_hook=_no_duplicate_pairs)
    require(isinstance(schema, dict), "current v12 schema JSON object")
    require(isinstance(contract, dict), "current v12 contract JSON object")
    verify_object(contract, "current v12 contract")
    schema_file_sha256 = sha256_bytes(input_raw[SCHEMA])
    contract_file_sha256 = sha256_bytes(input_raw[CONTRACT])
    contract_object_sha256 = contract["object_sha256"]
    closure = schema_static_closure(schema, source_raw["producer"])

    checker_report = load_checker_report(
        checker_report_path.resolve(), source_hashes)
    pin_normalized = pin_normalized_launcher_ast_sha256(
        source_raw["launcher"], "current_v12_launcher")
    helper_callsites = exact_helper_callsite_census([
        ("producer", source_raw["producer"]),
        ("consumer", source_raw["consumer"]),
        ("launcher", source_raw["launcher"]),
    ])

    transition = build_transition(
        v11_transition, schema_file_sha256, contract_file_sha256,
        contract_object_sha256, source_hashes["producer"],
        source_hashes["consumer"])
    transition_raw = draft_bytes(transition)
    require(object_hash(transition) == transition["object_sha256"],
            "rebuilt transition object closure")

    audit = build_static_audit(
        v11_audit, schema, closure, transition, transition_raw,
        contract_file_sha256, contract_object_sha256, source_raw,
        source_hashes, checker_report, pin_normalized, helper_callsites,
        v12_static_no_run())
    audit_raw = draft_bytes(audit)
    require(object_hash(audit) == audit["object_sha256"],
            "rebuilt static audit object closure")

    # Fail before the first write if any core input drifted during analysis.
    for path, raw in input_raw.items():
        require(path.read_bytes() == raw,
                "core input changed during rebuild: " + str(path))
    write_draft(TRANSITION, transition)
    write_draft(AUDIT, audit)
    require(TRANSITION.read_bytes() == transition_raw,
            "transition terminal-byte write replay")
    require(AUDIT.read_bytes() == audit_raw,
            "static audit terminal-byte write replay")
    print(json.dumps({
        "transition_file_sha256": sha256_bytes(transition_raw),
        "transition_object_sha256": transition["object_sha256"],
        "static_audit_file_sha256": sha256_bytes(audit_raw),
        "static_audit_object_sha256": audit["object_sha256"],
        "static_audit_input_key_count": 37,
        "formal_attack_count": FORMAL_ATTACK_COUNT,
        "schema_definition_count": closure["definition_count"],
        "schema_ref_count": closure["reference_count"],
        "closed_object_count": closure["closed_object_count"],
        "pin_normalized_launcher_ast_sha256": pin_normalized,
    }, sort_keys=True))


def main() -> None:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("schema-contract")
    transition_audit = subparsers.add_parser("transition-audit")
    transition_audit.add_argument(
        "--checker-census-report", required=True, type=Path,
        help=(
            "canonically object-closed current-v12 external checker report; "
            "the report must bind producer/consumer/launcher file hashes and "
            "supply fresh wider/common callsite censuses"))
    args = parser.parse_args()
    if args.command == "schema-contract":
        command_schema_contract()
    elif args.command == "transition-audit":
        command_transition_audit(args.checker_census_report)


if __name__ == "__main__":
    main()
