#!/usr/bin/env python3
"""Mechanically rebuild the C79g v15 static JSON drafts.

This helper never imports or executes any protocol Python source.  It derives
the four explicitly versioned v15 schema/contract/transition/audit drafts from
pinned predecessor bytes and current source ASTs.  A missing draft pair is
installed with no-follow O_EXCL held FDs; an existing pair is replayed exactly
and is never overwritten.  Final acyclic pin injection remains a separate step
after producer/consumer/launcher source convergence.
"""

from __future__ import annotations

import argparse
import ast
import copy
import fcntl
import hashlib
import json
import os
import re
import signal
import stat
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "deliverables"
RUNTIME = ROOT / ".cm2-runtime"
BASE = "cm2_round306c79g_true_global_no_producer_consumer"
V15_DRAFT_BUILDER_ENABLED = True
V15_STAGE2_SCHEMA_CONTRACT_TRANSFORM_COMPLETE = True
SCHEMA = OUT / f"{BASE}_schema_v15.json"
CONTRACT = OUT / f"{BASE}_contract_v15.json"
PRODUCER = OUT / f"{BASE}_v15.py"
CONSUMER = OUT / (
    f"{BASE}_independent_verifier_assembler_authority_consumer_v15.py")
LAUNCHER = OUT / f"{BASE}_cold_launch_v15.py"
TRANSITION = OUT / f"{BASE}_v14_to_v15_static_launch_transition_receipt_v1.json"
AUDIT = OUT / f"{BASE}_static_audit_v15.json"
CORE_PINNED_CHECKER_REPORT = ROOT / "scripts" / (
    "c79g_v15_checker_census_core_pinned_report_v1.json")
CORE_PINNED_CHECKER_REPORT_FILE_SHA256 = (
    "594c3c65c3ab901e4d1aad2a1d6618e494c3b6eb041d261062f143d7a1d44ebf")
CORE_PINNED_CHECKER_REPORT_OBJECT_SHA256 = (
    "ea79fa1627ff1f647f2860ef40434b6a63b9afe4a063933927b4bc2a563b4eb4")
V11_TRANSITION = OUT / f"{BASE}_v10_to_v11_static_launch_transition_receipt_v1.json"
V11_AUDIT = OUT / f"{BASE}_static_audit_v11.json"
V15_MANIFEST = OUT / f"{BASE}_cold_launch_manifest_v15.sha256"
V15_OUTER = OUT / f"{BASE}_cold_launch_outer_receipt_v15.json"
V12_TRANSITION = OUT / f"{BASE}_v11_to_v12_static_launch_transition_receipt_v1.json"
V12_AUDIT = OUT / f"{BASE}_static_audit_v12.json"
V12_SCHEMA = OUT / f"{BASE}_schema_v12.json"
V12_CONTRACT = OUT / f"{BASE}_contract_v12.json"
V12_PRODUCER = OUT / f"{BASE}_v12.py"
V12_CONSUMER = OUT / (
    f"{BASE}_independent_verifier_assembler_authority_consumer_v12.py")
V12_LAUNCHER = OUT / f"{BASE}_cold_launch_v12.py"
V12_MANIFEST = OUT / f"{BASE}_cold_launch_manifest_v12.sha256"
V12_OUTER = OUT / f"{BASE}_cold_launch_outer_receipt_v12.json"
V13_SUPERSESSION_RECEIPT = OUT / (
    f"{BASE}_v13_prepublication_pyc_contamination_rejection_"
    "supersession_receipt_v1.json")
V14_SCHEMA = OUT / f"{BASE}_schema_v14.json"
V14_CONTRACT = OUT / f"{BASE}_contract_v14.json"
V14_PRODUCER = OUT / f"{BASE}_v14.py"
V14_CONSUMER = OUT / (
    f"{BASE}_independent_verifier_assembler_authority_consumer_v14.py")
V14_TRANSITION = OUT / f"{BASE}_v13_to_v14_static_launch_transition_receipt_v1.json"
V14_AUDIT = OUT / f"{BASE}_static_audit_v14.json"
V14_LAUNCHER = OUT / f"{BASE}_cold_launch_v14.py"
V14_MANIFEST = OUT / f"{BASE}_cold_launch_manifest_v14.sha256"
V14_OUTER = OUT / f"{BASE}_cold_launch_outer_receipt_v14.json"
V14_REJECTION_REL = (
    ".cm2-runtime/c79g-v14-rejections-"
    "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab/"
    "rejection.json")
V14_SUPERSESSION_RECEIPT = OUT / (
    f"{BASE}_v14_runtime_registry_shape_drift_rejection_"
    "supersession_receipt_v1.json")

V12_SCHEMA_FILE_SHA256 = (
    "5ed911a55e8f90e750fdcaf6ab4fb6c9683bebaf66a4d6250329dff98acb2e28")
V12_CONTRACT_FILE_SHA256 = (
    "72246725b15891f92cbc6e3fa1c07ab4a76cdaa19f1b366a736f47f51989b343")
V12_CONTRACT_OBJECT_SHA256 = (
    "f5c1710817dc8e3aa7fe2bbf4b88e6e39baaa1b17bbeb0f8bf37c8c4575ae5d7")
V12_TRANSITION_FILE_SHA256 = (
    "45dabc1ef60eb2f8ba34aa7daa69f9d2b3bedccd4168d9c472bd4bbb696b5400")
V12_TRANSITION_OBJECT_SHA256 = (
    "0673ecafaa9991cd78e905e144e7c8c1b91717a3d753befa13e82552d44a4072")
V12_AUDIT_FILE_SHA256 = (
    "ac29b1e31e0d1b51e8610b7699d1aaf55c80fa6f13f00b20b209c2889e121d37")
V12_AUDIT_OBJECT_SHA256 = (
    "c1473ae0f5a08d8772227f61a55bd32c479a7b5c7d40da17b37e796abf4d9783")

CHECKPOINT = "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab"
V12_REJECTION_REL = (
    ".cm2-runtime/c79g-v12-rejections-" + CHECKPOINT + "/rejection.json")
V12_REJECTION_FILE = "b6b087a3e31b25f0bbe0ffe6caa40f3c181b2f77c5c8b6169ce3af27439762b5"
V12_REJECTION_OBJECT = "18951895ea97f455bc3294e8ef9cdaa937f3b16e9831275b047e88142e9b91f6"
V13_SUPERSESSION_RECEIPT_FILE_SHA256 = (
    "098296d9807a89f58250f4fd404bdd45b1cf343e3e2e1c7a51a24d67225d016f")
V13_SUPERSESSION_RECEIPT_OBJECT_SHA256 = (
    "3c9c44500465c6b416cc0ee6689ea82cdd9096a79687b94f94c409ca5a78c677")
V13_INHERITED_EXACT16_CANONICAL_SHA256 = (
    "bf70829a4632cd322ef45e9313d4150138a57f98966fcd93d2c7a718fb44f64e")
V13_NORMALIZED_EXACT10_CANONICAL_SHA256 = (
    "600768327003f17f0f367e64b03d0fd9ada23f2933db64845a37cfee140c61b5")
V13_SUPERSESSION_SCHEMA = (
    "cm2.round306c79g.true-global-no-producer-consumer."
    "v13-prepublication-pyc-contamination-rejection-supersession-receipt.v1")
V13_SUPERSESSION_STATUS = (
    "FROZEN_APPEND_ONLY_V13_PREPUBLICATION_PYC_CONTAMINATION_REJECTION__"
    "V14_SUCCESSOR_ONLY")
V13_TO_V14_TRANSITION_KIND = (
    "APPEND_ONLY_V13_PREPUBLICATION_PYC_CONTAMINATION_REJECTION_TO_"
    "ZERO_CREDIT_V14_STATIC_SUCCESSOR")

V14_SCHEMA_FILE_SHA256 = (
    "3d07ccda67cb71d0e5c64d37c0d8e1fcf425de4fbfefddf03bf43934ffdaaa4d")
V14_CONTRACT_FILE_SHA256 = (
    "479a0b3f6b4f0ad7e25d22c9f32eec046758a9a7d40509a6bda200e8e41e0ece")
V14_CONTRACT_OBJECT_SHA256 = (
    "11fd8966ed631f3bcc0eb6b1881f0536c814b7a7c093eca8289680e38a7d7b8b")
V14_TRANSITION_FILE_SHA256 = (
    "e8c810f85b511cbc3637321f872f96c996a854454ab7ae1fbb3f5bdf19d7fd95")
V14_TRANSITION_OBJECT_SHA256 = (
    "78912a8f23f7a2e229795aae0e609ca58232dbe36c52ad50bddad727f259413f")
V14_AUDIT_FILE_SHA256 = (
    "dbf5e6bf0f13524ee847d01482f9ad34f715368deb2df40207bd2eb436f293e9")
V14_AUDIT_OBJECT_SHA256 = (
    "16a8bc6e274a9e4e5a8fe4b2a39b80136cbbb117bfdf2e0ed89ee90fdc71944a")
V14_REJECTION_FILE_SHA256 = (
    "1cc1b5836457f219ce26aa8e463ebebe8d48a26d2145806d24f7cbfea6c7e567")
V14_REJECTION_OBJECT_SHA256 = (
    "0856353a2390c46b4f4bdefe9f13f6eb6e0e94aa352174cdc8d2f672ace4a41d")
V14_SUPERSESSION_RECEIPT_FILE_SHA256 = (
    "aa4323027e2313f8a2eda0d6ffc039a537afe342d496d1f75cd73fcd47446c01")
V14_SUPERSESSION_RECEIPT_OBJECT_SHA256 = (
    "93689e62ae36f405f045a769f4dc6f6e6fd83a16605d08299d5c3397ad657e2e")
V14_SUPERSESSION_SCHEMA = (
    "cm2.round306c79g.true-global-no-producer-consumer."
    "v14-runtime-registry-shape-drift-rejection-supersession-receipt.v1")
V14_SUPERSESSION_STATUS = (
    "FROZEN_APPEND_ONLY_V14_RUNTIME_REGISTRY_SHAPE_DRIFT_REJECTION__"
    "ZERO_CREDIT__V15_SUCCESSOR_ONLY")
V14_TO_V15_TRANSITION_KIND = (
    "APPEND_ONLY_PUBLISHED_V14_RUNTIME_FAIL_CLOSED_REJECTION_TO_"
    "ZERO_CREDIT_V15_CLEAN_ROOM_SUCCESSOR")
V12_EXACT10_FILE_SHA256_ORDER = (
    "f6cc10d8b7e72553ef0b7a32bbfb99255f36cce16b735002f17be58ae51d3bc8",
    "5ed911a55e8f90e750fdcaf6ab4fb6c9683bebaf66a4d6250329dff98acb2e28",
    "72246725b15891f92cbc6e3fa1c07ab4a76cdaa19f1b366a736f47f51989b343",
    "4cafc594f8a60063b7e7caaa82ddcc2b7983d0fbf0929034cd3cb5f360f3ed1d",
    "b74dee738257d485e9ca3357d7d138b5175b95e58f1c8ea87d1eca7bfc96b2ed",
    "45dabc1ef60eb2f8ba34aa7daa69f9d2b3bedccd4168d9c472bd4bbb696b5400",
    "ac29b1e31e0d1b51e8610b7699d1aaf55c80fa6f13f00b20b209c2889e121d37",
    "b7aaff67be866f8fd7a01f71e97ea1491574f69e62b7760b6ced9183997444ba",
    "297e9f58dc7657c6fa959dd45081efffe4e7e8dadcd16ab89457863e2661ece6",
    "27129990a9d5b6697fd13ee8e2086100cbf158f12e5b767166d771e63088b6d0",
)
V12_EXACT10_OBJECT_SHA256_ORDER = (
    "7ae86e38c5910bc9ceaa0a4e5cb1f8fbbf1e73de9c0314fedabbd8cb2db3bb7a",
    None,
    "f5c1710817dc8e3aa7fe2bbf4b88e6e39baaa1b17bbeb0f8bf37c8c4575ae5d7",
    None, None,
    "0673ecafaa9991cd78e905e144e7c8c1b91717a3d753befa13e82552d44a4072",
    "c1473ae0f5a08d8772227f61a55bd32c479a7b5c7d40da17b37e796abf4d9783",
    None, None,
    "bc6d06141865954590bd11bfc96ad59dbbffa003f568355ecb47155a8a3a809d",
)
V14_EXACT10_PATH_ORDER = (
    V13_SUPERSESSION_RECEIPT,
    V14_SCHEMA,
    V14_CONTRACT,
    V14_PRODUCER,
    V14_CONSUMER,
    V14_TRANSITION,
    V14_AUDIT,
    V14_LAUNCHER,
    V14_MANIFEST,
    V14_OUTER,
)
V14_EXACT10_FILE_SHA256_ORDER = (
    V13_SUPERSESSION_RECEIPT_FILE_SHA256,
    V14_SCHEMA_FILE_SHA256,
    V14_CONTRACT_FILE_SHA256,
    "9fa2f2e20cdf15ed37d7f3ff904197fa7bc46a4eec243cab0ae8fb477e2e1ff0",
    "83c58e792b922ad57a7c031b4aca60fe4d5868679e6f7a70b513e3cc4b7dc24c",
    V14_TRANSITION_FILE_SHA256,
    V14_AUDIT_FILE_SHA256,
    "1236f53865d69d69d27091758a66b21ddc2ea33ed7f422bc8d56adb69a23f5b5",
    "aae2b3735ca9d5469d4228189ff0127e85aca934c6e56dfa3650a4d4d46a5937",
    "fa6d10673d96a36aaf0163c44e014162ffb7811b12b1efa9068d78c8aa5b2040",
)
V14_EXACT10_OBJECT_SHA256_ORDER = (
    V13_SUPERSESSION_RECEIPT_OBJECT_SHA256,
    None,
    V14_CONTRACT_OBJECT_SHA256,
    None,
    None,
    V14_TRANSITION_OBJECT_SHA256,
    V14_AUDIT_OBJECT_SHA256,
    None,
    None,
    "786f9be9142ae0aafd31a6d86b08f815d5d4f7ca09fd67506f499635fdddc256",
)
V14_EXACT12_PATH_ORDER = (
    *V14_EXACT10_PATH_ORDER,
    ROOT / V14_REJECTION_REL,
    V14_SUPERSESSION_RECEIPT,
)
V14_EXACT12_FILE_SHA256_ORDER = (
    *V14_EXACT10_FILE_SHA256_ORDER,
    V14_REJECTION_FILE_SHA256,
    V14_SUPERSESSION_RECEIPT_FILE_SHA256,
)
V14_EXACT12_OBJECT_SHA256_ORDER = (
    *V14_EXACT10_OBJECT_SHA256_ORDER,
    V14_REJECTION_OBJECT_SHA256,
    V14_SUPERSESSION_RECEIPT_OBJECT_SHA256,
)
V14_EXACT12_CANONICAL_SHA256 = (
    "24e5e65f8690ad507f7590fe74b9b29702e978e0a8fb2837977e21e5b48df5cd")
V5_REJECTION_EXACT39_KEYSET_SHA256 = (
    "3b74017677a537d23cacbfbf95f1cc78e3b33fc4839be24e02e848bdd7410460")
V12_REJECTION_EXACT54_KEYSET_SHA256 = (
    "271055dec2aa42fb77c14bbd9b5c19e6bd4281428a71dc5db55c7d0db168b985")
V12_V5_REJECTION_SHAPE_INCIDENT_SHA256 = (
    "79ff0e0aa1df0e455af3abad67348f22e3b6b95512b864edf673422e72e17167")
V12_FIRST_RUNTIME_ATTEMPT_SHA256 = (
    "8ee3eefa4e9f7c1114d5968e5af9b40c8234295ef9ef05f8ef9cf19f1f776ce9")
V12_V5_REJECTION_SHAPE_HELPER_NORMALIZED_AST_SHA256 = (
    "fa4cf4f0bdb9e9f1b2a3bdeed7d7271830833395a2f58d32457f363e596fb5e9")
HISTORICAL_REJECTION_EXACT_KEYSET_WITNESS_SHA256 = (
    "94d860d8e9b4676c622a6eb2d52bce339f874edee7865f7edb275d3d97d15ae7")
V15_LATER_REJECTION_EXACT56_KEYSET_SHA256 = (
    "9c272f16d92497a7c5ced499e9e42c514b81cbfddcdb3f79c4f33837836e057e")
V15_PREDECESSOR_UNIQUE_FILE_IDENTITY_COUNT = 116
V15_PREPUBLICATION_UNIQUE_FILE_IDENTITY_COUNT = 124
V15_TERMINAL_UNIQUE_FILE_IDENTITY_COUNT = 126
V15_TERMINAL_GROUP_VECTOR = [
    10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 7, 1, 3, 3, 1, 1]
V11_REJECTION_REL = (
    ".cm2-runtime/c79g-v11-rejections-" + CHECKPOINT + "/rejection.json")
V11_REJECTION_NS_REL = V11_REJECTION_REL.removesuffix("/rejection.json")
V11_REJECTION_FILE = "f6cc10d8b7e72553ef0b7a32bbfb99255f36cce16b735002f17be58ae51d3bc8"
V11_REJECTION_OBJECT = "7ae86e38c5910bc9ceaa0a4e5cb1f8fbbf1e73de9c0314fedabbd8cb2db3bb7a"
V12_EXACT10_PATH_ORDER = (
    ROOT / V11_REJECTION_REL,
    V12_SCHEMA,
    V12_CONTRACT,
    V12_PRODUCER,
    V12_CONSUMER,
    V12_TRANSITION,
    V12_AUDIT,
    V12_LAUNCHER,
    V12_MANIFEST,
    V12_OUTER,
)
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
    "CURRENT_V15_SIX_BASE7_FILE_F64_OBJECT_E64_OR_NONE__"
    "PRESERVE_V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT_"
    "AND_ALL_HISTORICAL_PINS_V1"
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
    "v12_rejection_file", "v12_rejection_object", "v12_producer_file",
    "v12_consumer_file", "v12_launcher_file",
    "trusted_v12_v5_rejection_shape_incident_digest",
)
STATIC_AUDIT_INPUT_KEY_ORDER_SHA256 = (
    "7e11baf937aa7e9695f30718fcb14793ed2fdacbdf0f33bda659086d399e4574")
STATIC_AUDIT_HISTORICAL_INPUT_KEYS = STATIC_AUDIT_INPUT_KEY_ORDER[8:32]
STATIC_AUDIT_TOP_LEVEL_KEY_ORDER = (
    "schema", "status", "audit_path", "effective_checkpoint_object_sha256",
    "audited_v15_bundle", "predecessor_v3_exact10_regression",
    "v3_official_later_rejection_regression",
    "predecessor_v4_rejection_supersession_regression",
    "published_then_officially_rejected_predecessor_v5",
    "published_then_officially_rejected_predecessor_v6",
    "published_then_officially_rejected_predecessor_v7",
    "published_then_officially_rejected_predecessor_v8",
    "published_then_officially_rejected_predecessor_v9",
    "published_then_officially_rejected_predecessor_v10",
    "published_then_officially_rejected_predecessor_v11",
    "published_then_officially_rejected_predecessor_v12",
    "rejected_prepublication_v13_supersession_receipt",
    "published_then_officially_rejected_predecessor_v14",
    "v10_colon_prefix_witness", "v11_dual_validator_divergence_incident",
    "v12_v5_rejection_shape_incident",
    "historical_rejection_exact_keyset_witness",
    "dual_independent_static_checkers", "coherent_attack_static_census",
    "schema_and_constructor_closure",
    "sealed_exec_and_no_producer_static_proof", "static_credit_census",
    "static_no_run", "final_audit_acceptance",
)

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
    "independentConsumerProof": 60,
    "staticFreezeProof": 84,
    "coldLaunchProof": 112,
    "laterRejection": 56,
    "producerSourceRegistry": 75,
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
    "twelve_v14_inherited_authority_inputs_inherited_as_held_fds",
    "twelve_v14_inherited_authority_held_fds_path_identity_mount_and_hash_revalidated",
]
V15_EXPECTED_LAUNCHER_REGISTRY_HELPER_AST_SHA256 = (
    "f27a5e8df3308e5b022519929e8f0f64257dcbc35b355fa1537b0169d5604a8c")
CONTRACT_AUTHORITY_ROOT_STRUCTURE = (
    "ZERO_CREDIT_INNER=(V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT + "
    "LIVE_V14_EXACT10 + OFFICIAL_V14_LATER_REJECTION + "
    "V14_RUNTIME_REGISTRY_SHAPE_DRIFT_INCIDENT + "
    "V13_PREPUBLICATION_SUPERSESSION_RECEIPT + "
    "V13_INCIDENT_SOURCE_PYC_EXACT6 + LIVE_V12_EXACT10 + "
    "OFFICIAL_V12_LATER_REJECTION + V12_V5_REJECTION_SHAPE_INCIDENT + "
    "LIVE_V11_EXACT10 + OFFICIAL_V11_LATER_REJECTION + "
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
    "FRESH_EMPTY_V15_REJECTION_NAMESPACE); "
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
    "v12_rejection_file_sha256 || v12_rejection_object_sha256 || "
    "trusted_v12_v5_rejection_shape_incident_digest || "
    "v13_supersession_receipt_file_sha256 || "
    "v13_supersession_receipt_object_sha256 || "
    "v13_inherited_exact16_canonical_sha256 || "
    "v14_rejection_file_sha256 || v14_rejection_object_sha256 || "
    "v14_supersession_receipt_file_sha256 || "
    "v14_supersession_receipt_object_sha256 || "
    "v14_inherited_exact12_canonical_sha256 || "
    "actual_launcher_registry_helper_normalized_ast_sha256 || "
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
    "V12_EXACT10_VALID",
    "V12_OFFICIAL_REJECTION_VALID",
    "TRUSTED_V12_V5_REJECTION_SHAPE_INCIDENT_RECORDED_FROM_FROZEN_EXACT16",
    "V13_PREPUBLICATION_SUPERSESSION_RECEIPT_VALID",
    "V13_INCIDENT_SOURCE_PYC_EXACT6_HELD_AND_TERMINALLY_REPLAYED",
    "V14_EXACT10_VALID",
    "V14_OFFICIAL_REJECTION_VALID",
    "V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT_VALID",
    "V14_INHERITED_AUTHORITY_EXACT12_HELD_AND_TERMINALLY_REPLAYED",
    "ACTUAL_LAUNCHER_RUNTIME_REGISTRY_HELPER_EXPLICIT67_PLUS_PROOF7_PLUS_OBJECT1_EQUALS75_VALID",
    "IN_MEMORY_EXPLICIT62_TAMPER_REJECTED",
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
    "NO_LATER_V15_REJECTION_AT_EACH_READ",
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
    raw = read_regular_file_stable(path)
    return json.loads(raw.decode("utf-8"),
                      object_pairs_hook=_no_duplicate_pairs)


def _no_duplicate_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, item in pairs:
        if key in value:
            raise ValueError(f"duplicate JSON key: {key}")
        value[key] = item
    return value


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
    raw = read_regular_file_stable(path)
    require(sha256_bytes(raw) == file_sha256,
            path.name + ": frozen file pin")
    value = json.loads(raw, object_pairs_hook=_no_duplicate_pairs)
    require(isinstance(value, dict), path.name + ": JSON object")
    verify_object(value, path.name, object_sha256)
    return value


def _stat_identity(value: os.stat_result) -> tuple[int, ...]:
    return (
        value.st_dev, value.st_ino, value.st_mode, value.st_nlink,
        value.st_size, value.st_mtime_ns, value.st_ctime_ns,
    )


def _directory_identity(value: os.stat_result) -> tuple[int, ...]:
    """Stable directory authority fields; entry writes may change size/times."""
    return (
        value.st_dev, value.st_ino, value.st_mode, value.st_nlink,
        value.st_uid, value.st_gid,
    )


def fd_mount_id(descriptor: int) -> int:
    """Return the kernel mount identity for one already-held descriptor."""
    try:
        raw = Path(f"/proc/self/fdinfo/{descriptor}").read_text(
            encoding="ascii")
    except OSError as exc:
        raise ValueError("cannot read held-fd mount identity") from exc
    for line in raw.splitlines():
        if line.startswith("mnt_id:"):
            try:
                mount_id = int(line.split(":", 1)[1].strip())
            except ValueError as exc:
                raise ValueError("invalid held-fd mount identity") from exc
            require(mount_id > 0, "positive held-fd mount identity")
            return mount_id
    raise ValueError("held-fd mount identity absent")


def path_lexists(path: Path) -> bool:
    """Existence check that treats every symlink, including broken, as present."""
    try:
        os.lstat(path)
        return True
    except FileNotFoundError:
        return False
    except OSError as exc:
        raise ValueError(str(path) + ": cannot establish path absence") from exc


def open_held_directory(path: Path) -> tuple[int, os.stat_result, int]:
    """Open one pathname as a no-follow directory and bind path/fd/mount."""
    try:
        named = os.lstat(path)
    except OSError as exc:
        raise ValueError(str(path) + ": directory pathname unavailable") from exc
    require(stat.S_ISDIR(named.st_mode) and not stat.S_ISLNK(named.st_mode),
            str(path) + ": no-follow directory pathname")
    descriptor = -1
    try:
        descriptor = os.open(
            path,
            os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC | os.O_NOFOLLOW)
        held = os.fstat(descriptor)
        require(stat.S_ISDIR(held.st_mode) and
                _directory_identity(named) == _directory_identity(held),
                str(path) + ": held/path directory identity")
        return descriptor, held, fd_mount_id(descriptor)
    except BaseException:
        if descriptor >= 0:
            os.close(descriptor)
        raise


def revalidate_held_directory(
        path: Path, descriptor: int, before: os.stat_result,
        mount_id: int) -> None:
    """Reject pathname replacement, mode/owner drift, or mount substitution."""
    try:
        named = os.lstat(path)
        held = os.fstat(descriptor)
    except OSError as exc:
        raise ValueError(str(path) + ": held directory unavailable") from exc
    require(
        stat.S_ISDIR(named.st_mode) and not stat.S_ISLNK(named.st_mode) and
        stat.S_ISDIR(held.st_mode) and
        _directory_identity(named) == _directory_identity(held) ==
            _directory_identity(before) and
        fd_mount_id(descriptor) == mount_id,
        str(path) + ": held/path/mode/owner/mount directory drift")


class OfficialStaticWriterWindow:
    """Whole-command exclusive window on the official runtime directory."""

    def __init__(self) -> None:
        self.root_fd = -1
        self.output_fd = -1
        self.runtime_fd = -1
        self.root_before: os.stat_result | None = None
        self.output_before: os.stat_result | None = None
        self.runtime_before: os.stat_result | None = None
        self.root_mount_id = -1
        self.output_mount_id = -1
        self.runtime_mount_id = -1
        self.lock_owned = False

    @classmethod
    def acquire(cls) -> "OfficialStaticWriterWindow":
        result = cls()
        try:
            (result.root_fd, result.root_before,
             result.root_mount_id) = open_held_directory(ROOT)
            (result.output_fd, result.output_before,
             result.output_mount_id) = open_held_directory(OUT)
            (result.runtime_fd, result.runtime_before,
             result.runtime_mount_id) = open_held_directory(RUNTIME)
            require(result.root_mount_id == result.output_mount_id ==
                    result.runtime_mount_id,
                    "official root/output/runtime share one mount")
            fcntl.flock(result.runtime_fd, fcntl.LOCK_EX)
            result.lock_owned = True
            result.revalidate()
            return result
        except BaseException:
            result.close_without_revalidation()
            raise

    def revalidate(self) -> None:
        require(self.lock_owned and self.runtime_fd >= 0,
                "official static writer LOCK_EX remains owned")
        require(self.root_before is not None and
                self.output_before is not None and
                self.runtime_before is not None,
                "official held directory snapshots exist")
        revalidate_held_directory(
            ROOT, self.root_fd, self.root_before, self.root_mount_id)
        revalidate_held_directory(
            OUT, self.output_fd, self.output_before, self.output_mount_id)
        revalidate_held_directory(
            RUNTIME, self.runtime_fd, self.runtime_before,
            self.runtime_mount_id)
        require(self.root_mount_id == self.output_mount_id ==
                self.runtime_mount_id,
                "official held directories retain one mount")

    def close_without_revalidation(self) -> None:
        if self.runtime_fd >= 0 and self.lock_owned:
            try:
                fcntl.flock(self.runtime_fd, fcntl.LOCK_UN)
            finally:
                self.lock_owned = False
        for attribute in ("runtime_fd", "output_fd", "root_fd"):
            descriptor = getattr(self, attribute)
            if descriptor >= 0:
                os.close(descriptor)
                setattr(self, attribute, -1)

    def release(self) -> None:
        try:
            self.revalidate()
        finally:
            self.close_without_revalidation()


def read_regular_file_stable(
        path: Path, expected_mode: int | None = None) -> bytes:
    """Read a unique regular file by no-follow held file and parent FDs."""
    parent_fd = -1
    descriptor = -1
    try:
        parent_fd, parent_before, parent_mount_id = open_held_directory(
            path.parent)
        descriptor = os.open(
            path.name, os.O_RDONLY | os.O_CLOEXEC | os.O_NOFOLLOW,
            dir_fd=parent_fd)
        before = os.fstat(descriptor)
        require(stat.S_ISREG(before.st_mode) and before.st_nlink == 1 and
                (expected_mode is None or
                 stat.S_IMODE(before.st_mode) == expected_mode),
                str(path) + ": unique regular input")
        require(fd_mount_id(descriptor) == parent_mount_id,
                str(path) + ": input and parent share one mount")
        raw = _read_all_fd(descriptor)
        after = os.fstat(descriptor)
        named = os.stat(
            path.name, dir_fd=parent_fd, follow_symlinks=False)
        require(_stat_identity(before) == _stat_identity(after) ==
                _stat_identity(named) and len(raw) == after.st_size,
                str(path) + ": stable held/path input replay")
        revalidate_held_directory(
            path.parent, parent_fd, parent_before, parent_mount_id)
        return raw
    finally:
        if descriptor >= 0:
            os.close(descriptor)
        if parent_fd >= 0:
            os.close(parent_fd)


def _read_all_fd(descriptor: int) -> bytes:
    os.lseek(descriptor, 0, os.SEEK_SET)
    chunks: list[bytes] = []
    while True:
        chunk = os.read(descriptor, 1024 * 1024)
        if not chunk:
            return b"".join(chunks)
        chunks.append(chunk)


def _write_all_fd(descriptor: int, raw: bytes) -> None:
    view = memoryview(raw)
    while view:
        written = os.write(descriptor, view)
        require(written > 0, "seed draft write made no progress")
        view = view[written:]


def read_frozen_regular_file(path: Path, file_sha256: str) -> bytes:
    """Hold and pin one immutable predecessor file without following links."""
    raw = read_regular_file_stable(path, expected_mode=0o444)
    require(sha256_bytes(raw) == file_sha256,
            path.name + ": frozen file SHA-256 pin")
    return raw


def load_frozen_v13_supersession_receipt() -> dict[str, Any]:
    """Load the historical one-way v13 rejection authority for v14."""
    raw = read_frozen_regular_file(
        V13_SUPERSESSION_RECEIPT,
        V13_SUPERSESSION_RECEIPT_FILE_SHA256)
    value = decode_json_object(raw, "frozen v13 supersession receipt")
    verify_object(
        value, "frozen v13 supersession receipt",
        V13_SUPERSESSION_RECEIPT_OBJECT_SHA256)
    successor = value.get("v14_successor_contract", {})
    inherited = successor.get("inherited_incident_authority_exact16", {})
    normalized = value.get(
        "frozen_v13_inherited_incident_authority_exact10_source_contract", {})
    exact16 = inherited.get("ordered_members")
    require(
        raw == canonical(value) + b"\n" and
        value.get("schema") == V13_SUPERSESSION_SCHEMA and
        value.get("status") == V13_SUPERSESSION_STATUS and
        value.get("receipt_path") ==
            str(V13_SUPERSESSION_RECEIPT.relative_to(ROOT)) and
        value.get("effective_checkpoint_object_sha256") == CHECKPOINT and
        isinstance(exact16, list) and len(exact16) == 16 and
        inherited.get("ordered_member_count") == 16 and
        inherited.get("ordered_member_exact_keys") ==
            ["ordinal", "role", "path", "file_sha256"] and
        len(canonical(exact16)) == 3646 and
        sha256_bytes(canonical(exact16)) ==
            inherited.get("ordered_exact16_canonical_sha256") ==
            V13_INHERITED_EXACT16_CANONICAL_SHA256 and
        normalized.get("normalized_ordered_member_count") == 10 and
        normalized.get("normalized_exact10_canonical_byte_length") == 2657 and
        normalized.get("normalized_exact10_canonical_sha256") ==
            V13_NORMALIZED_EXACT10_CANONICAL_SHA256 and
        successor.get("v14_current_exact8_first_member_must_be_this_receipt")
            is True and
        successor.get("v14_must_preserve_v12_exact10_and_official_rejection")
            is True and
        successor.get("v14_predecessor_unique_live_identity_count") == 105 and
        successor.get("v14_prepublication_unique_live_identity_count") == 113 and
        successor.get("v14_terminal_unique_live_identity_count") == 115 and
        successor.get("v14_terminal_group_vector") ==
            [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 7, 1, 3, 3, 1] and
        inherited.get(
            "v14_must_live_hold_and_terminally_replay_exact16_plus_this_receipt")
            is True,
        "frozen v13 receipt exact16/current-first/census contract")
    return value


def v13_supersession_summary(
        receipt: dict[str, Any]) -> dict[str, Any]:
    """Return the historical seven-key v13-to-v14 summary."""
    summary = {
        "receipt_path": str(V13_SUPERSESSION_RECEIPT.relative_to(ROOT)),
        "receipt_file_sha256": V13_SUPERSESSION_RECEIPT_FILE_SHA256,
        "receipt_object_sha256": V13_SUPERSESSION_RECEIPT_OBJECT_SHA256,
        "receipt_schema": V13_SUPERSESSION_SCHEMA,
        "receipt_status": V13_SUPERSESSION_STATUS,
        "transition_kind": V13_TO_V14_TRANSITION_KIND,
        "v14_successor_contract": copy.deepcopy(
            receipt["v14_successor_contract"]),
    }
    require(list(summary) == [
        "receipt_path", "receipt_file_sha256", "receipt_object_sha256",
        "receipt_schema", "receipt_status", "transition_kind",
        "v14_successor_contract"],
        "v13 supersession exact seven-key summary")
    return summary


def load_frozen_v14_exact12() -> tuple[dict[str, Any], ...]:
    """Hold and close v14 exact10, official rejection, and supersession."""
    require(
        len(V14_EXACT12_PATH_ORDER) ==
        len(V14_EXACT12_FILE_SHA256_ORDER) ==
        len(V14_EXACT12_OBJECT_SHA256_ORDER) == 12,
        "frozen v14 inherited authority exact12 pin-vector lengths")
    rows: list[dict[str, Any]] = []
    for path, file_pin, object_pin in zip(
            V14_EXACT12_PATH_ORDER, V14_EXACT12_FILE_SHA256_ORDER,
            V14_EXACT12_OBJECT_SHA256_ORDER, strict=True):
        raw = read_frozen_regular_file(path, file_pin)
        metadata = path.lstat()
        require(
            stat.S_ISREG(metadata.st_mode) and
            stat.S_IMODE(metadata.st_mode) == 0o444 and
            metadata.st_nlink == 1,
            path.name + ": frozen v14 exact12 regular 0444 nlink1")
        value: dict[str, Any] | None = None
        if object_pin is not None:
            value = decode_json_object(raw, "frozen v14 exact12:" + path.name)
            verify_object(value, "frozen v14 exact12:" + path.name, object_pin)
            require(raw in {canonical(value) + b"\n", draft_bytes(value)},
                    path.name + ": exact canonical-compact-or-draft object bytes")
        rows.append({
            "path": path,
            "raw": raw,
            "file_sha256": file_pin,
            "object_sha256": object_pin,
            "json_object": value,
        })
    records = [{
        "path": str(row["path"].relative_to(ROOT)),
        "file_sha256": row["file_sha256"],
        "object_sha256": row["object_sha256"],
    } for row in rows]
    require(
        sha256_bytes(canonical(records)) == V14_EXACT12_CANONICAL_SHA256,
        "frozen v14 exact12 ordered canonical digest")
    return tuple(rows)


def load_frozen_v14_supersession_receipt(
        rows: tuple[dict[str, Any], ...],
) -> dict[str, Any]:
    """Validate the exact v14 failure authority and its v15 one-way contract."""
    require(len(rows) == 12 and rows[-1]["path"] == V14_SUPERSESSION_RECEIPT,
            "v14 supersession is terminal exact12 member")
    value = rows[-1]["json_object"]
    require(isinstance(value, dict), "frozen v14 supersession JSON object")
    authority = value.get("frozen_v14_publication_authority")
    incident = value.get("runtime_registry_shape_drift_incident")
    credit = value.get("credit")
    successor = value.get("v15_successor_contract")
    require(all(isinstance(item, dict) for item in (
        authority, incident, credit, successor)),
        "v14 supersession authority/incident/credit/successor objects")
    ordered = authority.get("ordered_exact10")
    expected_exact10 = list(zip(
        V14_EXACT10_PATH_ORDER, V14_EXACT10_FILE_SHA256_ORDER,
        V14_EXACT10_OBJECT_SHA256_ORDER, strict=True))
    require(
        value.get("schema") == V14_SUPERSESSION_SCHEMA and
        value.get("status") == V14_SUPERSESSION_STATUS and
        value.get("transition_kind") == V14_TO_V15_TRANSITION_KIND and
        value.get("receipt_path") ==
            str(V14_SUPERSESSION_RECEIPT.relative_to(ROOT)) and
        value.get("effective_checkpoint_object_sha256") == CHECKPOINT and
        isinstance(ordered, list) and len(ordered) == 10 and
        authority.get("ordered_member_count") == 10 and
        all(
            row.get("path") == str(path.relative_to(ROOT)) and
            row.get("file_sha256") == file_pin and
            row.get("object_sha256") == object_pin and
            row.get("mode") == "0444" and row.get("nlink") == 1
            for row, (path, file_pin, object_pin) in
            zip(ordered, expected_exact10, strict=True)) and
        authority.get("official_later_rejection", {}).get("path") ==
            V14_REJECTION_REL and
        authority.get("official_later_rejection", {}).get("file_sha256") ==
            V14_REJECTION_FILE_SHA256 and
        authority.get("official_later_rejection", {}).get("object_sha256") ==
            V14_REJECTION_OBJECT_SHA256 and
        authority.get("outer_strictly_precedes_official_rejection") is True and
        authority.get("all_regular_0444_nlink1_hash_and_object_pins_match")
            is True,
        "frozen v14 supersession published exact10/rejection closure")
    producer_shape = incident.get("producer_registry_shape", {})
    stale = incident.get("cold_launcher_stale_helper_shape", {})
    require(
        producer_shape.get("producer_explicit_registry_key_count") == 67 and
        producer_shape.get("producer_execution_proof_key_count") == 7 and
        producer_shape.get("canonical_object_closure_key_count") == 1 and
        producer_shape.get("actual_total_registry_shape") == 75 and
        stale.get("launcher_stale_expected_explicit_registry_key_count") == 62 and
        stale.get("launcher_stale_total_registry_shape") == 70 and
        incident.get("shape_delta") == 5 and
        incident.get("runtime_effect") ==
            "FAIL_CLOSED_IN_LAUNCHER_SOURCE_REGISTRY_SHAPE_CHECK_BEFORE_"
            "CANDIDATE_OR_STAGE_MATERIALIZATION",
        "frozen v14 supersession registry-shape incident closure")
    require(
        credit == {
            "D02_formal_pending_task_count": 33638,
            "D02_gate_credit": 0,
            "D02_started": False,
            "D02_task_credit": 0,
            "D02_unlock": False,
            "formal_global_closure_credit": 0,
        } and
        successor == {
            "one_way_binding_avoids_hash_cycle": True,
            "this_receipt_does_not_pin_any_v15_successor_byte": True,
            "v15_current_exact8_first_member_must_be_this_receipt": True,
            "v15_independent_reviewer_must_execute_the_actual_launcher_helper_against_actual_producer_bytes": True,
            "v15_independent_reviewer_must_reject_in_memory_explicit62_tamper": True,
            "v15_inherited_published_incident_authority_exact12_count": 12,
            "v15_launcher_registry_helper_must_require_explicit67_plus_execution_proof7_plus_object_closure1_equals75": True,
            "v15_must_directly_hold_and_terminally_replay_v14_exact10_plus_official_rejection_plus_this_receipt": True,
            "v15_must_pin_this_receipt_file_and_object_sha256": True,
        },
        "frozen v14 zero-credit and exact v15 successor contract")
    return value


def v14_supersession_summary(receipt: dict[str, Any]) -> dict[str, Any]:
    summary = {
        "receipt_path": str(V14_SUPERSESSION_RECEIPT.relative_to(ROOT)),
        "receipt_file_sha256": V14_SUPERSESSION_RECEIPT_FILE_SHA256,
        "receipt_object_sha256": V14_SUPERSESSION_RECEIPT_OBJECT_SHA256,
        "receipt_schema": V14_SUPERSESSION_SCHEMA,
        "receipt_status": V14_SUPERSESSION_STATUS,
        "transition_kind": V14_TO_V15_TRANSITION_KIND,
        "inherited_authority_exact12_member_count": 12,
        "inherited_authority_exact12_canonical_sha256":
            V14_EXACT12_CANONICAL_SHA256,
        "v15_successor_contract": copy.deepcopy(
            receipt["v15_successor_contract"]),
    }
    require(list(summary) == [
        "receipt_path", "receipt_file_sha256", "receipt_object_sha256",
        "receipt_schema", "receipt_status", "transition_kind",
        "inherited_authority_exact12_member_count",
        "inherited_authority_exact12_canonical_sha256",
        "v15_successor_contract"],
        "v14 supersession exact nine-key summary")
    return summary


def decode_json_object(raw: bytes, label: str) -> dict[str, Any]:
    value = json.loads(raw, object_pairs_hook=_no_duplicate_pairs)
    require(isinstance(value, dict), label + ": JSON object")
    return value


def load_frozen_v12_exact10() -> tuple[dict[str, Any], ...]:
    """Load the published v12 exact10 once, in its immutable manifest order."""
    require(len(V12_EXACT10_PATH_ORDER) ==
            len(V12_EXACT10_FILE_SHA256_ORDER) ==
            len(V12_EXACT10_OBJECT_SHA256_ORDER) == 10,
            "frozen v12 exact10 pin-vector lengths")
    rows: list[dict[str, Any]] = []
    for path, file_pin, object_pin in zip(
            V12_EXACT10_PATH_ORDER, V12_EXACT10_FILE_SHA256_ORDER,
            V12_EXACT10_OBJECT_SHA256_ORDER, strict=True):
        raw = read_frozen_regular_file(path, file_pin)
        value: dict[str, Any] | None = None
        if object_pin is not None:
            value = decode_json_object(raw, "frozen v12 exact10:" + path.name)
            verify_object(value, "frozen v12 exact10:" + path.name, object_pin)
        rows.append({
            "path": path,
            "raw": raw,
            "file_sha256": file_pin,
            "object_sha256": object_pin,
            "json_object": value,
        })
    require(tuple(row["path"] for row in rows) == V12_EXACT10_PATH_ORDER,
            "frozen v12 exact10 ordered path closure")
    return tuple(rows)


def load_frozen_v12_static_seed_bundle() -> dict[str, Any]:
    """Return pinned S/C/T/A objects backed by the same exact10 byte snapshot."""
    rows = load_frozen_v12_exact10()
    schema = decode_json_object(rows[1]["raw"], "frozen v12 schema")
    contract = rows[2]["json_object"]
    transition = rows[5]["json_object"]
    audit = rows[6]["json_object"]
    require(isinstance(contract, dict) and isinstance(transition, dict) and
            isinstance(audit, dict),
            "frozen v12 object-closed static seeds")
    require(rows[1]["file_sha256"] == V12_SCHEMA_FILE_SHA256 and
            rows[2]["file_sha256"] == V12_CONTRACT_FILE_SHA256 and
            rows[2]["object_sha256"] == V12_CONTRACT_OBJECT_SHA256 and
            rows[5]["file_sha256"] == V12_TRANSITION_FILE_SHA256 and
            rows[5]["object_sha256"] == V12_TRANSITION_OBJECT_SHA256 and
            rows[6]["file_sha256"] == V12_AUDIT_FILE_SHA256 and
            rows[6]["object_sha256"] == V12_AUDIT_OBJECT_SHA256,
            "frozen v12 S/C/T/A explicit pins agree with exact10")
    receipt = load_frozen_v13_supersession_receipt()
    bundle = {
        "schema": schema,
        "contract": copy.deepcopy(contract),
        "transition": copy.deepcopy(transition),
        "audit": copy.deepcopy(audit),
        "exact10": rows,
        "v13_supersession_receipt": receipt,
        "v13_supersession_summary": v13_supersession_summary(receipt),
    }
    bundle["v12_published_rejected_proof"] = \
        reconstruct_v12_published_rejected_proof(bundle)
    return bundle


def load_frozen_v14_static_seed_bundle() -> dict[str, Any]:
    """Return v14 S/C/T/A seeds backed by the frozen inherited exact12."""
    rows = load_frozen_v14_exact12()
    schema = decode_json_object(rows[1]["raw"], "frozen v14 schema")
    contract = rows[2]["json_object"]
    transition = rows[5]["json_object"]
    audit = rows[6]["json_object"]
    require(isinstance(contract, dict) and isinstance(transition, dict) and
            isinstance(audit, dict), "frozen v14 object-closed S/C/T/A seeds")
    require(
        rows[1]["file_sha256"] == V14_SCHEMA_FILE_SHA256 and
        rows[2]["file_sha256"] == V14_CONTRACT_FILE_SHA256 and
        rows[2]["object_sha256"] == V14_CONTRACT_OBJECT_SHA256 and
        rows[5]["file_sha256"] == V14_TRANSITION_FILE_SHA256 and
        rows[5]["object_sha256"] == V14_TRANSITION_OBJECT_SHA256 and
        rows[6]["file_sha256"] == V14_AUDIT_FILE_SHA256 and
        rows[6]["object_sha256"] == V14_AUDIT_OBJECT_SHA256,
        "frozen v14 S/C/T/A explicit pins agree with exact12")
    receipt = load_frozen_v14_supersession_receipt(rows)
    historical = load_frozen_v12_static_seed_bundle()
    require(
        contract.get("published_then_officially_rejected_predecessor_v12") ==
            historical["v12_published_rejected_proof"] and
        contract.get("rejected_prepublication_v13_supersession_receipt") ==
            historical["v13_supersession_summary"],
        "v14 contract preserves v12 and v13 append-only history")
    return {
        "schema": schema,
        "contract": copy.deepcopy(contract),
        "transition": copy.deepcopy(transition),
        "audit": copy.deepcopy(audit),
        "exact12": rows,
        "v12_published_rejected_proof": copy.deepcopy(
            historical["v12_published_rejected_proof"]),
        "v13_supersession_summary": copy.deepcopy(
            historical["v13_supersession_summary"]),
        "v14_supersession_receipt": receipt,
        "v14_supersession_summary": v14_supersession_summary(receipt),
    }


_LITERAL_MISSING = object()


def module_literal_assignments(tree: ast.Module) -> dict[str, list[ast.AST]]:
    """Collect module assignments without evaluating or importing the source."""
    assignments: dict[str, list[ast.AST]] = {}
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    assignments.setdefault(target.id, []).append(node.value)
        elif (isinstance(node, ast.AnnAssign) and
              isinstance(node.target, ast.Name)):
            assignments.setdefault(node.target.id, []).append(node.value)
    return assignments


def restricted_safe_literal(node: ast.AST | None,
                            environment: dict[str, Any]) -> Any:
    """Evaluate the deliberately tiny literal language used by frozen v13.

    Calls, attributes, comprehensions and every other executable expression
    remain rejected.  The only accepted calls are deterministic constructors
    over an already-safe value and ``sorted`` over one already-safe value.
    """
    if node is None:
        return _LITERAL_MISSING
    try:
        return ast.literal_eval(node)
    except (TypeError, ValueError, SyntaxError, MemoryError, RecursionError):
        pass
    if isinstance(node, ast.Name):
        return environment.get(node.id, _LITERAL_MISSING)
    if (isinstance(node, ast.BinOp) and
            isinstance(node.op, (ast.Add, ast.Mult, ast.BitOr, ast.Sub))):
        left = restricted_safe_literal(node.left, environment)
        right = restricted_safe_literal(node.right, environment)
        if left is _LITERAL_MISSING or right is _LITERAL_MISSING:
            return _LITERAL_MISSING
        try:
            if isinstance(node.op, ast.Add):
                return left + right
            if isinstance(node.op, ast.Mult):
                return left * right
            if isinstance(node.op, ast.Sub):
                return left - right
            return left | right
        except (TypeError, ValueError, OverflowError):
            return _LITERAL_MISSING
    if isinstance(node, (ast.Tuple, ast.List, ast.Set)):
        values = [restricted_safe_literal(item, environment)
                  for item in node.elts]
        if any(value is _LITERAL_MISSING for value in values):
            return _LITERAL_MISSING
        if isinstance(node, ast.Tuple):
            return tuple(values)
        if isinstance(node, ast.List):
            return values
        try:
            return set(values)
        except TypeError:
            return _LITERAL_MISSING
    if isinstance(node, ast.Dict):
        result: dict[Any, Any] = {}
        for key_node, value_node in zip(node.keys, node.values, strict=True):
            if key_node is None:
                return _LITERAL_MISSING
            key = restricted_safe_literal(key_node, environment)
            value = restricted_safe_literal(value_node, environment)
            if key is _LITERAL_MISSING or value is _LITERAL_MISSING:
                return _LITERAL_MISSING
            try:
                result[key] = value
            except TypeError:
                return _LITERAL_MISSING
        return result
    if (isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and
            node.func.id in {"tuple", "list", "set", "frozenset"} and
            len(node.args) in {0, 1} and not node.keywords):
        value = (restricted_safe_literal(node.args[0], environment)
                 if node.args else ())
        if value is _LITERAL_MISSING:
            return _LITERAL_MISSING
        try:
            constructor = {
                "tuple": tuple, "list": list, "set": set,
                "frozenset": frozenset,
            }[node.func.id]
            return constructor(value)
        except (TypeError, ValueError):
            return _LITERAL_MISSING
    if (isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and
            node.func.id == "sorted" and len(node.args) == 1 and
            not node.keywords):
        value = restricted_safe_literal(node.args[0], environment)
        if value is _LITERAL_MISSING:
            return _LITERAL_MISSING
        try:
            return sorted(value)
        except (TypeError, ValueError):
            return _LITERAL_MISSING
    return _LITERAL_MISSING


def restricted_literal_environment(tree: ast.Module,
                                   label: str) -> dict[str, Any]:
    assignments = module_literal_assignments(tree)
    duplicates = sorted(
        name for name, nodes in assignments.items() if len(nodes) != 1)
    require(not duplicates,
            label + ": duplicate module assignment(s): " +
            ",".join(duplicates))
    environment: dict[str, Any] = {}
    for _ in range(max(2, len(assignments))):
        changed = False
        for name, nodes in assignments.items():
            if name in environment:
                continue
            value = restricted_safe_literal(nodes[0], environment)
            if value is not _LITERAL_MISSING:
                environment[name] = value
                changed = True
        if not changed:
            break
    return environment


def literal_module_assignment(raw: bytes, name: str, label: str) -> Any:
    """Extract one inert restricted-literal assignment without code execution."""
    tree = parse_source_ast(raw, label)
    assignments = module_literal_assignments(tree)
    require(len(assignments.get(name, [])) == 1,
            label + ": one " + name + " assignment")
    environment = restricted_literal_environment(tree, label)
    value = environment.get(name, _LITERAL_MISSING)
    require(value is not _LITERAL_MISSING,
            label + ": restricted-literal " + name)
    return copy.deepcopy(value)


def restricted_literal_self_test() -> None:
    positive = (
        b'BASE = frozenset({"beta", "alpha"})\n'
        b'ALIAS = BASE\n'
        b'TARGET = {"ordered": sorted(ALIAS), "copy": ALIAS}\n')
    expected = {
        "ordered": ["alpha", "beta"],
        "copy": frozenset({"alpha", "beta"}),
    }
    require(literal_module_assignment(
        positive, "TARGET", "restricted-literal-self-test-positive") ==
        expected, "restricted literal Name/sorted positive self-test")

    negative_sources = {
        "arbitrary-call": b"TARGET = dangerous()\n",
        "attribute": b"TARGET = object.attribute\n",
        "comprehension": b"TARGET = [item for item in (1, 2)]\n",
        "unresolved-name": b"TARGET = UNKNOWN_NAME\n",
        "duplicate-assignment": b"TARGET = 1\nTARGET = 2\n",
    }
    for case, raw in negative_sources.items():
        try:
            literal_module_assignment(
                raw, "TARGET", "restricted-literal-self-test-" + case)
        except ValueError:
            continue
        raise ValueError(
            "restricted literal negative self-test accepted: " + case)


def v12_incident_literals_from_frozen_v13_sources(
        receipt: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    """Independently recover v12 incident literals from all frozen v13 ASTs."""
    rows = receipt["v14_successor_contract"][
        "inherited_incident_authority_exact16"]["ordered_members"][10:13]
    require([row.get("role") for row in rows] == [
        "v13_build_only_producer_source",
        "v13_independent_consumer_source",
        "v13_cold_launcher_source"],
        "frozen v13 source exact3 role order")
    first_attempts: list[dict[str, Any]] = []
    incidents: list[dict[str, Any]] = []
    for row in rows:
        path = ROOT / row["path"]
        raw = read_frozen_regular_file(path, row["file_sha256"])
        first = literal_module_assignment(
            raw, "V12_FIRST_RUNTIME_ATTEMPT", "frozen:" + row["role"])
        incident = literal_module_assignment(
            raw, "V12_V5_REJECTION_SHAPE_INCIDENT",
            "frozen:" + row["role"])
        require(isinstance(first, dict) and isinstance(incident, dict),
                row["role"] + ": v12 incident literal dictionaries")
        first_attempts.append(first)
        incidents.append(incident)
    require(first_attempts[1:] == first_attempts[:-1] and
            incidents[1:] == incidents[:-1] and
            sha256_bytes(canonical(first_attempts[0])) ==
                V12_FIRST_RUNTIME_ATTEMPT_SHA256 and
            sha256_bytes(canonical(incidents[0])) ==
                V12_V5_REJECTION_SHAPE_INCIDENT_SHA256,
            "three frozen v13 sources agree on pinned v12 incident literals")
    return first_attempts[0], incidents[0]


def reconstruct_v12_published_rejected_proof(
        seed_bundle: dict[str, Any]) -> dict[str, Any]:
    """Rebuild the exact v12 exact10/rejection zero-credit history segment."""
    exact10 = seed_bundle["exact10"]
    receipt = seed_bundle["v13_supersession_receipt"]
    first_attempt, incident = \
        v12_incident_literals_from_frozen_v13_sources(receipt)
    names = (
        "v11_official_rejection", "closed_schema", "contract",
        "build_only_producer", "independent_consumer", "v11_to_v12_transition",
        "static_audit", "cold_launcher", "cold_manifest", "cold_outer")
    ordered: list[dict[str, Any]] = []
    for name, row in zip(names, exact10, strict=True):
        member = {
            "name": name,
            "path": str(row["path"].relative_to(ROOT)),
            "file_sha256": row["file_sha256"],
        }
        if row["object_sha256"] is not None:
            member["object_sha256"] = row["object_sha256"]
        ordered.append(member)
    rejection_path = ROOT / V12_REJECTION_REL
    rejection_raw = read_frozen_regular_file(
        rejection_path, V12_REJECTION_FILE)
    rejection = decode_json_object(rejection_raw, "frozen v12 rejection")
    verify_object(rejection, "frozen v12 rejection", V12_REJECTION_OBJECT)
    absent = [
        f".cm2-runtime/c79g-v12-candidate-a-{CHECKPOINT}",
        f".cm2-runtime/c79g-v12-candidate-b-{CHECKPOINT}",
        f".cm2-runtime/c79g-v12-verification-a-{CHECKPOINT}",
        f".cm2-runtime/c79g-v12-verification-b-{CHECKPOINT}",
        f".cm2-runtime/c79g-v12-committed-completion-{CHECKPOINT}",
        f".cm2-runtime/cm2-global-authority-heads/c79g-v12-{CHECKPOINT}.seal",
        f".cm2-runtime/.c79g-v12-candidate-stage-a-{CHECKPOINT}",
        f".cm2-runtime/.c79g-v12-candidate-stage-b-{CHECKPOINT}",
        f".cm2-runtime/.c79g-v12-verification-stage-a-{CHECKPOINT}",
        f".cm2-runtime/.c79g-v12-verification-stage-b-{CHECKPOINT}",
        f".cm2-runtime/.c79g-v12-completion-stage-{CHECKPOINT}",
        f".cm2-runtime/cm2-global-authority-heads/"
        f".c79g-v12-authority-stage-{CHECKPOINT}.seal",
    ]
    require(not any(path_lexists(ROOT / path) for path in absent),
            "v12 positive and stage surfaces remain absent")
    proof = {
        "ordered_published_exact10": ordered,
        "official_later_rejection": {
            "path": V12_REJECTION_REL,
            "namespace_path": V12_REJECTION_REL.removesuffix("/rejection.json"),
            "file_sha256": V12_REJECTION_FILE,
            "object_sha256": V12_REJECTION_OBJECT,
            "schema": rejection["schema"],
            "status": rejection["status"],
            "reason": rejection["rejection_reason"],
            "namespace_mode": "0555",
            "namespace_nlink": 2,
            "exact_member_universe": ["rejection.json"],
            "member_mode": "0444",
            "member_nlink": 1,
            "formal_global_closure_credit": 0,
            "D02_unlock": False,
            "D02_gate_credit": 0,
            "D02_task_credit": 0,
            "D02_formal_pending_task_count": 33_638,
            "D02_started": False,
            "overwrite_delete_or_reuse_allowed": False,
        },
        "first_runtime_attempt": first_attempt,
        "v5_rejection_shape_incident": incident,
        "positive_and_stage_surfaces_absent": {
            "exact_absent_path_count": len(absent),
            "exact_absent_paths": absent,
            "all_absent": True,
        },
        "all_ten_file_pins_match": True,
        "all_declared_object_pins_match": True,
        "all_ten_regular_0444_nlink1": True,
        "exact8_manifest_reconstructs_first_eight_in_order": True,
        "outer_last_pins_manifest_and_launcher": True,
        "outer_then_rejection_chronology_validated": True,
        "v12_execution_allowed": False,
        "v12_runtime_surfaces_authoritative": False,
        "formal_global_closure_credit": 0,
        "D02_unlock": False,
        "D02_gate_credit": 0,
        "D02_task_credit": 0,
        "D02_formal_pending_task_count": 33_638,
        "D02_started": False,
    }
    require(len(proof) == 19, "v12 published/rejected proof exact19")
    return proof


def write_draft_pair_exclusive(
        ordered_drafts: tuple[tuple[Path, dict[str, Any]], ...],
        ) -> list[dict[str, Any]]:
    """Install one complete draft pair with O_EXCL and same-FD replay.

    It can only create a previously absent S/C or T/A pair and can never
    overwrite one or follow a link.
    If either member fails before the parent-directory fsync commit, every
    inode created by this call is removed after an inode-identity check.
    """
    ordered_paths = tuple(path for path, _ in ordered_drafts)
    require(ordered_paths in {
                (SCHEMA, CONTRACT), (TRANSITION, AUDIT)},
            "exclusive pair writer exact S/C or T/A target order")
    raws = [(path, draft_bytes(value)) for path, value in ordered_drafts]
    parent_descriptor, parent_before, parent_mount_id = \
        open_held_directory(OUT)
    created: list[tuple[Path, int, bytes]] = []
    committed = False
    try:
        require(stat.S_ISDIR(parent_before.st_mode),
                "seed writer deliverables parent is directory")
        for path, _ in raws:
            require(path.parent == OUT and path.name not in {"", ".", ".."},
                    "seed writer target remains in deliverables")
            try:
                os.stat(path.name, dir_fd=parent_descriptor,
                        follow_symlinks=False)
            except FileNotFoundError:
                pass
            else:
                raise FileExistsError(
                    "refuse to replace existing v15 seed draft: " + str(path))

        open_flags = (
            os.O_RDWR | os.O_CREAT | os.O_EXCL | os.O_CLOEXEC |
            os.O_NOFOLLOW)
        blocked_signals = {
            item for item in (
                signal.SIGINT, signal.SIGTERM, signal.SIGHUP, signal.SIGQUIT)
            if item in signal.valid_signals()}
        for path, raw in raws:
            descriptor = -1
            recorded = False
            previous_mask = signal.pthread_sigmask(
                signal.SIG_BLOCK, blocked_signals)
            try:
                descriptor = os.open(
                    path.name, open_flags, 0o600,
                    dir_fd=parent_descriptor)
                created.append((path, descriptor, raw))
                recorded = True
            except BaseException:
                # Cover O_EXCL success followed by an interruption before the
                # descriptor is recorded.  Only the still-named held inode may
                # be removed; a foreign replacement is never unlinked.
                if descriptor >= 0:
                    try:
                        held = os.fstat(descriptor)
                        pathname = os.stat(
                            path.name, dir_fd=parent_descriptor,
                            follow_symlinks=False)
                        if ((held.st_dev, held.st_ino) ==
                                (pathname.st_dev, pathname.st_ino)):
                            os.unlink(path.name, dir_fd=parent_descriptor)
                            os.fsync(parent_descriptor)
                    except FileNotFoundError:
                        pass
                    finally:
                        if not any(
                                item[1] == descriptor for item in created):
                            os.close(descriptor)
                            descriptor = -1
                raise
            finally:
                # Any pending catchable signal is delivered only after this
                # inode is recorded or identity-safely removed.
                signal.pthread_sigmask(signal.SIG_SETMASK, previous_mask)
            require(recorded and descriptor >= 0,
                    path.name + ": O_EXCL inode recorded before signal unmask")
            initial = os.fstat(descriptor)
            require(stat.S_ISREG(initial.st_mode) and initial.st_nlink == 1 and
                    initial.st_dev == parent_before.st_dev and
                    fd_mount_id(descriptor) == parent_mount_id,
                    path.name + ": new unique regular draft inode")
            _write_all_fd(descriptor, raw)
            os.fchmod(descriptor, 0o664)
            os.fsync(descriptor)
            frozen_draft = os.fstat(descriptor)
            pathname = os.stat(
                path.name, dir_fd=parent_descriptor, follow_symlinks=False)
            require((frozen_draft.st_dev, frozen_draft.st_ino) ==
                    (pathname.st_dev, pathname.st_ino) and
                    stat.S_IMODE(frozen_draft.st_mode) == 0o664 and
                    frozen_draft.st_nlink == 1 and
                    frozen_draft.st_size == len(raw),
                    path.name + ": exclusive draft inode/mode/size replay")
            require(_read_all_fd(descriptor) == raw,
                    path.name + ": exclusive draft same-FD terminal replay")

        os.fsync(parent_descriptor)
        revalidate_held_directory(
            OUT, parent_descriptor, parent_before, parent_mount_id)
        committed = True
        return [{
            "path": str(path.relative_to(ROOT)),
            "file_sha256": sha256_bytes(raw),
            "byte_count": len(raw),
            "mode": "0664",
            "nlink": os.fstat(descriptor).st_nlink,
        } for path, descriptor, raw in created]
    except BaseException as exc:
        cleanup_errors: list[str] = []
        if not committed:
            for path, descriptor, _ in reversed(created):
                try:
                    held = os.fstat(descriptor)
                    pathname = os.stat(
                        path.name, dir_fd=parent_descriptor,
                        follow_symlinks=False)
                    if ((held.st_dev, held.st_ino) ==
                            (pathname.st_dev, pathname.st_ino)):
                        os.unlink(path.name, dir_fd=parent_descriptor)
                except FileNotFoundError:
                    pass
                except BaseException as cleanup_exc:
                    cleanup_errors.append(
                        type(cleanup_exc).__name__ + ":" + str(cleanup_exc))
            if created:
                try:
                    os.fsync(parent_descriptor)
                except BaseException as cleanup_exc:
                    cleanup_errors.append(
                        type(cleanup_exc).__name__ + ":" + str(cleanup_exc))
            try:
                revalidate_held_directory(
                    OUT, parent_descriptor, parent_before, parent_mount_id)
            except BaseException as cleanup_exc:
                cleanup_errors.append(
                    type(cleanup_exc).__name__ + ":" + str(cleanup_exc))
        if cleanup_errors:
            raise RuntimeError(
                "draft pair rollback cleanup errors: " +
                repr(cleanup_errors)) from exc
        raise
    finally:
        for _, descriptor, _ in created:
            os.close(descriptor)
        os.close(parent_descriptor)


def draft_pair_state(paths: tuple[Path, Path]) -> str:
    require(paths in {(SCHEMA, CONTRACT), (TRANSITION, AUDIT)},
            "draft pair state exact S/C or T/A order")
    parent_descriptor, parent_before, parent_mount_id = \
        open_held_directory(OUT)
    try:
        states: list[bool] = []
        for path in paths:
            require(path.parent == OUT and path.name not in {"", ".", ".."},
                    "draft pair target remains in deliverables")
            try:
                metadata = os.stat(
                    path.name, dir_fd=parent_descriptor,
                    follow_symlinks=False)
            except FileNotFoundError:
                states.append(False)
                continue
            require(stat.S_ISREG(metadata.st_mode) and metadata.st_nlink == 1,
                    path.name + ": existing draft is unique regular file")
            states.append(True)
        require(states in ([False, False], [True, True]),
                "draft pair mixed present/absent state is fail-closed")
        revalidate_held_directory(
            OUT, parent_descriptor, parent_before, parent_mount_id)
        return "absent" if states == [False, False] else "present"
    finally:
        os.close(parent_descriptor)


def replay_draft_pair_exact(
        ordered_drafts: tuple[tuple[Path, dict[str, Any]], ...],
        ) -> list[dict[str, Any]]:
    """Read both existing members through held no-follow FDs; never write."""
    ordered_paths = tuple(path for path, _ in ordered_drafts)
    require(ordered_paths in {
                (SCHEMA, CONTRACT), (TRANSITION, AUDIT)},
            "exact replay pair exact S/C or T/A target order")
    expected = [(path, draft_bytes(value)) for path, value in ordered_drafts]
    parent_descriptor, parent_before, parent_mount_id = \
        open_held_directory(OUT)
    held: list[tuple[Path, int, bytes, os.stat_result]] = []
    try:
        parent = os.fstat(parent_descriptor)
        require(stat.S_ISDIR(parent.st_mode) and
                _directory_identity(parent) ==
                    _directory_identity(parent_before),
                "draft replay deliverables parent is directory")
        flags = os.O_RDONLY | os.O_CLOEXEC | os.O_NOFOLLOW
        for path, raw in expected:
            descriptor = os.open(
                path.name, flags, dir_fd=parent_descriptor)
            before = os.fstat(descriptor)
            require(stat.S_ISREG(before.st_mode) and before.st_nlink == 1 and
                    before.st_dev == parent.st_dev and
                    fd_mount_id(descriptor) == parent_mount_id and
                    stat.S_IMODE(before.st_mode) in {0o664, 0o444},
                    path.name + ": replay unique regular 0664-or-0444 inode")
            pathname = os.stat(
                path.name, dir_fd=parent_descriptor,
                follow_symlinks=False)
            require((before.st_dev, before.st_ino) ==
                    (pathname.st_dev, pathname.st_ino),
                    path.name + ": replay held/path inode identity")
            held.append((path, descriptor, raw, before))

        details: list[dict[str, Any]] = []
        for path, descriptor, raw, before in held:
            observed = _read_all_fd(descriptor)
            after = os.fstat(descriptor)
            pathname = os.stat(
                path.name, dir_fd=parent_descriptor,
                follow_symlinks=False)
            require(_stat_identity(before) == _stat_identity(after) ==
                    _stat_identity(pathname),
                    path.name + ": stable held/path replay identity")
            require(observed == raw and len(observed) == before.st_size,
                    path.name + ": existing bytes exactly reproduce draft")
            details.append({
                "path": str(path.relative_to(ROOT)),
                "file_sha256": sha256_bytes(observed),
                "byte_count": len(observed),
                "mode": f"{stat.S_IMODE(before.st_mode):04o}",
                "nlink": before.st_nlink,
            })
        revalidate_held_directory(
            OUT, parent_descriptor, parent_before, parent_mount_id)
        return details
    finally:
        for _, descriptor, _, _ in held:
            os.close(descriptor)
        os.close(parent_descriptor)


def install_absent_or_replay_exact_pair(
        ordered_drafts: tuple[tuple[Path, dict[str, Any]], ...],
        ) -> tuple[str, list[dict[str, Any]]]:
    paths = tuple(path for path, _ in ordered_drafts)
    require(len(paths) == 2,
            "install/replay receives one exact pair")
    state = draft_pair_state((paths[0], paths[1]))
    if state == "absent":
        write_draft_pair_exclusive(ordered_drafts)
        return "installed_exclusive", replay_draft_pair_exact(
            ordered_drafts)
    return "replayed_existing", replay_draft_pair_exact(ordered_drafts)


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
    module_assignments = module_literal_assignments(tree)
    for name, expected_pin in (
            ("V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT_FILE_PIN",
             V14_SUPERSESSION_RECEIPT_FILE_SHA256),
            ("V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT_OBJECT_PIN",
             V14_SUPERSESSION_RECEIPT_OBJECT_SHA256)):
        nodes = module_assignments.get(name, [])
        require(len(nodes) == 1 and isinstance(nodes[0], ast.Constant) and
                nodes[0].value == expected_pin,
                label + ": fixed v14 supersession receipt literal pin " + name)
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
        "V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT",
        *PIN_NORMALIZED_CURRENT_BASE7_KEY_ORDER]
    require(key_names == expected and len(base7.values) == len(expected),
            label + ": exact ordered receipt-plus-v15 BASE7 census")
    first = base7.values[0]
    require(
        isinstance(first, ast.Tuple) and len(first.elts) == 2 and
        isinstance(first.elts[0], ast.Name) and
        first.elts[0].id ==
            "V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT_FILE_PIN" and
        isinstance(first.elts[1], ast.Name) and
        first.elts[1].id ==
            "V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT_OBJECT_PIN",
        label + ": receipt-first BASE7 tuple uses exact fixed pins")
    exact8_assignments = [
        node for node in configure_functions[0].body
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and
        isinstance(node.targets[0], ast.Name) and
        node.targets[0].id == "EXACT8"]
    require(
        len(exact8_assignments) == 1 and
        isinstance(exact8_assignments[0].value, ast.Tuple) and
        [item.id if isinstance(item, ast.Name) else None
         for item in exact8_assignments[0].value.elts] == [
            "V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT",
            "SCHEMA", "CONTRACT", "PRODUCER", "CONSUMER", "TRANSITION",
            "AUDIT", "SELF"],
        label + ": exact receipt-first current exact8 order")
    receipt_before = ast.dump(
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
        include_attributes=False) == receipt_before,
        label + ": v14 supersession receipt BASE7 value preserved")
    return sha256_bytes(ast.dump(
        tree, annotate_fields=True,
        include_attributes=False).encode("utf-8"))


def producer_source_registry_shape_from_ast(raw: bytes) -> int:
    tree = parse_source_ast(raw, "producer_v15")
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
    require(len(explicit_keys) == len(set(explicit_keys)) == 67 and
            len(expansions) == 1 and isinstance(expansions[0], ast.Call) and
            isinstance(expansions[0].func, ast.Attribute) and
            isinstance(expansions[0].func.value, ast.Name) and
            expansions[0].func.value.id == "self_guard" and
            expansions[0].func.attr == "execution_proof" and
            not expansions[0].args and not expansions[0].keywords and
            proof_keys == SOURCE_REGISTRY_EXECUTION_PROOF_EXACT7,
            "producer registry explicit67 plus exact7 execution proof")
    return len(explicit_keys) + len(proof_keys) + 1


def _function_scope_returns(
        function: ast.FunctionDef | ast.AsyncFunctionDef,
) -> list[ast.Return]:
    rows: list[ast.Return] = []

    class Visitor(ast.NodeVisitor):
        def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
            if node is function:
                self.generic_visit(node)

        def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
            if node is function:
                self.generic_visit(node)

        def visit_Lambda(self, node: ast.Lambda) -> None:
            return

        def visit_Return(self, node: ast.Return) -> None:
            rows.append(node)

    Visitor().visit(function)
    return rows


def _exact_len_name(node: ast.AST, name: str) -> bool:
    return (
        isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and
        node.func.id == "len" and len(node.args) == 1 and not node.keywords and
        isinstance(node.args[0], ast.Name) and node.args[0].id == name)


def _exact_len_set_name(node: ast.AST, name: str) -> bool:
    return (
        isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and
        node.func.id == "len" and len(node.args) == 1 and not node.keywords and
        isinstance(node.args[0], ast.Call) and
        isinstance(node.args[0].func, ast.Name) and
        node.args[0].func.id == "set" and len(node.args[0].args) == 1 and
        not node.args[0].keywords and
        isinstance(node.args[0].args[0], ast.Name) and
        node.args[0].args[0].id == name)


def _exact_len_attribute_name(
        node: ast.AST, name: str, attribute: str,
) -> bool:
    return (
        isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and
        node.func.id == "len" and len(node.args) == 1 and not node.keywords and
        isinstance(node.args[0], ast.Attribute) and
        isinstance(node.args[0].value, ast.Name) and
        node.args[0].value.id == name and node.args[0].attr == attribute)


def _direct_statement(
        function: ast.FunctionDef | ast.AsyncFunctionDef, node: ast.AST,
) -> ast.stmt | None:
    parents = {
        child: item for item in ast.walk(function)
        for child in ast.iter_child_nodes(item)}
    cursor: ast.AST = node
    while cursor in parents:
        owner = parents[cursor]
        if owner is function:
            return cursor if isinstance(cursor, ast.stmt) else None
        cursor = owner
    return None


def _is_direct_need_condition(
        function: ast.FunctionDef | ast.AsyncFunctionDef, node: ast.AST,
) -> bool:
    statement = _direct_statement(function, node)
    if not (
            isinstance(statement, ast.Expr) and
            isinstance(statement.value, ast.Call) and
            isinstance(statement.value.func, ast.Name) and
            statement.value.func.id == "need" and statement.value.args):
        return False
    condition = statement.value.args[0]
    parents = {
        child: item for item in ast.walk(condition)
        for child in ast.iter_child_nodes(item)}
    cursor = node
    while cursor is not condition:
        owner = parents.get(cursor)
        if not isinstance(owner, ast.BoolOp) or not isinstance(
                owner.op, ast.And):
            return False
        cursor = owner
    return True


def _launcher_runtime_registry_helper_core(
        tree: ast.Module, producer_shape: int,
) -> dict[str, Any]:
    helpers = [
        node for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and
        node.name == "producer_source_registry_shape_from_ast"]
    require(len(helpers) == 1, "launcher unique actual registry helper")
    helper = helpers[0]
    nodes = list(ast.walk(helper))
    guards = [
        node for node in nodes
        if isinstance(node, ast.Compare) and len(node.ops) == 2 and
        all(isinstance(operator, ast.Eq) for operator in node.ops) and
        _exact_len_name(node.left, "explicit_keys") and
        _exact_len_set_name(node.comparators[0], "explicit_keys") and
        isinstance(node.comparators[1], ast.Constant) and
        type(node.comparators[1].value) is int and
        _is_direct_need_condition(helper, node)]
    literals = [node.comparators[1].value for node in guards]
    stale_62_count = sum(
        isinstance(node, ast.Constant) and node.value == 62 for node in nodes)
    proof_7_guards = [
        node for node in nodes
        if isinstance(node, ast.Compare) and len(node.ops) == 1 and
        isinstance(node.ops[0], ast.Eq) and
        _exact_len_attribute_name(node.left, "proof_dict", "keys") and
        len(node.comparators) == 1 and
        isinstance(node.comparators[0], ast.Constant) and
        node.comparators[0].value == 7 and
        _is_direct_need_condition(helper, node)]
    expansion_exact_one_guards = [
        node for node in nodes
        if isinstance(node, ast.Compare) and len(node.ops) == 1 and
        isinstance(node.ops[0], ast.Eq) and
        _exact_len_name(node.left, "expansions") and
        len(node.comparators) == 1 and
        isinstance(node.comparators[0], ast.Constant) and
        node.comparators[0].value == 1 and
        _is_direct_need_condition(helper, node)]
    expansion_guard_literals = {
        node.value for node in nodes
        if isinstance(node, ast.Constant) and
        node.value in {"self_guard", "execution_proof"}}
    assignments = [
        node.value for node in helper.body
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and
        isinstance(node.targets[0], ast.Name) and
        node.targets[0].id == "shape"]
    formula = ast.parse(
        "len(explicit_keys) + len(proof_dict.keys) + 1", mode="eval").body
    formula_ok = (
        len(assignments) == 1 and
        ast.dump(assignments[0], include_attributes=False) ==
            ast.dump(formula, include_attributes=False))
    returns = _function_scope_returns(helper)
    return_ok = (
        len(returns) == 1 and isinstance(returns[0].value, ast.Name) and
        returns[0].value.id == "shape" and bool(helper.body) and
        helper.body[-1] is returns[0])
    nested_scope_count = sum(
        isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef,
                          ast.Lambda, ast.ClassDef)) and node is not helper
        for node in nodes)
    shape_75_guards = [
        node for node in nodes
        if isinstance(node, ast.Compare) and len(node.ops) == 1 and
        isinstance(node.ops[0], ast.Eq) and
        isinstance(node.left, ast.Name) and node.left.id == "shape" and
        len(node.comparators) == 1 and
        isinstance(node.comparators[0], ast.Constant) and
        node.comparators[0].value == 75 and
        _is_direct_need_condition(helper, node)]
    parents = {
        child: node for node in ast.walk(tree)
        for child in ast.iter_child_nodes(node)}
    calls = [
        node for node in ast.walk(tree)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and
        node.func.id == "producer_source_registry_shape_from_ast"]
    call_owner: str | None = None
    live_call_ok = False
    live_result_consumed_ok = False
    live_call_direct_assignment_ok = False
    live_consumption_direct_need_ok = False
    if len(calls) == 1:
        call = calls[0]
        expected_argument = ast.parse(
            "held_by_path[PRODUCER].raw", mode="eval").body
        argument_ok = (
            len(call.args) == 1 and not call.keywords and
            ast.dump(call.args[0], include_attributes=False) ==
                ast.dump(expected_argument, include_attributes=False))
        cursor: ast.AST = call
        while cursor in parents:
            owner = parents[cursor]
            if isinstance(owner, (ast.FunctionDef, ast.AsyncFunctionDef)):
                call_owner = owner.name
                direct_statement = cursor if isinstance(cursor, ast.stmt) else None
                live_call_direct_assignment_ok = (
                    isinstance(direct_statement, ast.Assign) and
                    len(direct_statement.targets) == 1 and
                    isinstance(direct_statement.targets[0], ast.Name) and
                    direct_statement.targets[0].id ==
                        "computed_registry_shape" and
                    direct_statement.value is call)
                consumption = [
                    node for node in ast.walk(owner)
                    if isinstance(node, ast.Compare) and len(node.ops) == 2 and
                    all(isinstance(operator, ast.Eq)
                        for operator in node.ops) and
                    isinstance(node.left, ast.Name) and
                    node.left.id == "computed_registry_shape" and
                    isinstance(node.comparators[0], ast.Subscript) and
                    isinstance(node.comparators[0].value, ast.Name) and
                    node.comparators[0].value.id == "expected_shapes" and
                    isinstance(node.comparators[0].slice, ast.Constant) and
                    node.comparators[0].slice.value ==
                        "producerSourceRegistry" and
                    isinstance(node.comparators[1], ast.Constant) and
                    node.comparators[1].value == 75]
                live_consumption_direct_need_ok = (
                    len(consumption) == 1 and
                    _is_direct_need_condition(owner, consumption[0]))
                live_result_consumed_ok = live_consumption_direct_need_ok
                break
            cursor = owner
        live_call_ok = (
            argument_ok and live_call_direct_assignment_ok and
            call_owner == "validate_final_static_audit" and
            live_result_consumed_ok)
    normalized = sha256_bytes(ast.dump(
        helper, annotate_fields=True,
        include_attributes=False).encode("utf-8"))
    parameters = [*helper.args.posonlyargs, *helper.args.args]
    exact_raw_parameter = (
        len(parameters) == 1 and parameters[0].arg == "raw" and
        not helper.args.vararg and not helper.args.kwonlyargs and
        not helper.args.kwarg and not helper.args.defaults)
    matches = (
        literals == [67] and stale_62_count == 0 and
        len(proof_7_guards) == 1 and
        len(expansion_exact_one_guards) == 1 and
        expansion_guard_literals == {"self_guard", "execution_proof"} and
        normalized == V15_EXPECTED_LAUNCHER_REGISTRY_HELPER_AST_SHA256 and
        exact_raw_parameter and nested_scope_count == 0 and formula_ok and
        return_ok and len(shape_75_guards) == 1 and live_call_ok and
        producer_shape == 75)
    return {
        "normalized_helper_ast_sha256": normalized,
        "expected_normalized_helper_ast_sha256":
            V15_EXPECTED_LAUNCHER_REGISTRY_HELPER_AST_SHA256,
        "exact_single_raw_parameter": exact_raw_parameter,
        "normalized_helper_semantics_match_reviewed_template":
            normalized == V15_EXPECTED_LAUNCHER_REGISTRY_HELPER_AST_SHA256,
        "explicit_key_guard_literals": literals,
        "stale_literal_62_count": stale_62_count,
        "exact_execution_proof_7_guard_count": len(proof_7_guards),
        "exact_execution_proof_expansion_guard_count":
            len(expansion_exact_one_guards),
        "nested_helper_scope_count": nested_scope_count,
        "shape_formula_is_len_explicit_plus_len_proof_plus_one": formula_ok,
        "return_is_computed_shape": return_ok,
        "exact_shape_75_guard_count": len(shape_75_guards),
        "live_callsite_count": len(calls),
        "live_callsite_owner": call_owner,
        "live_callsite_is_direct_assignment":
            live_call_direct_assignment_ok,
        "live_callsite_uses_held_producer_raw": live_call_ok,
        "live_computed_shape_consumed_by_expected_shapes_then_75_gate":
            live_result_consumed_ok,
        "live_consumption_is_direct_need_gate":
            live_consumption_direct_need_ok,
        "held_producer_independent_computed_shape": producer_shape,
        "matches": matches,
    }


def launcher_runtime_registry_helper_from_ast(
        raw: bytes, producer_shape: int,
) -> dict[str, Any]:
    tree = parse_source_ast(raw, "launcher_v15_runtime_registry_helper")
    current = _launcher_runtime_registry_helper_core(tree, producer_shape)
    tampered = copy.deepcopy(tree)
    helper = next(
        node for node in tampered.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and
        node.name == "producer_source_registry_shape_from_ast")
    changed = 0
    for node in ast.walk(helper):
        if (isinstance(node, ast.Compare) and len(node.comparators) == 2 and
                isinstance(node.comparators[-1], ast.Constant) and
                node.comparators[-1].value == 67):
            node.comparators[-1].value = 62
            changed += 1
    stale_rejected = (
        changed == 1 and
        _launcher_runtime_registry_helper_core(
            tampered, producer_shape)["matches"] is False)

    dead_callsite_tree = copy.deepcopy(tree)
    audit_functions = [
        node for node in dead_callsite_tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and
        node.name == "validate_final_static_audit"]
    require(len(audit_functions) == 1,
            "launcher unique final static audit owner")
    moved = 0
    for index, statement in enumerate(audit_functions[0].body):
        if (isinstance(statement, ast.Assign) and
                len(statement.targets) == 1 and
                isinstance(statement.targets[0], ast.Name) and
                statement.targets[0].id == "computed_registry_shape"):
            audit_functions[0].body[index] = ast.If(
                test=ast.Constant(value=False), body=[statement], orelse=[])
            moved += 1
    dead_callsite_rejected = (
        moved == 1 and
        _launcher_runtime_registry_helper_core(
            dead_callsite_tree, producer_shape)["matches"] is False)
    current["in_memory_stale_62_mutation_count"] = changed
    current["in_memory_stale_62_rejected"] = stale_rejected
    current["in_memory_dead_callsite_mutation_count"] = moved
    current["in_memory_dead_callsite_rejected"] = dead_callsite_rejected
    current["matches"] = bool(
        current["matches"] and stale_rejected and dead_callsite_rejected)
    require(
        set(current) == LAUNCHER_RUNTIME_HELPER_CENSUS_KEYS and
        current["matches"] is True,
        "actual launcher runtime helper exact67+7+1=75 and explicit62 tamper")
    return current


def historical_rejection_exact_keyset_witness_from_sources(
        source_raw: dict[str, bytes]) -> list[dict[str, Any]]:
    """Safely rederive and cross-check the exact nine-row P/C/L witness."""
    require(tuple(source_raw) == ("producer", "consumer", "launcher"),
            "historical witness exact ordered P/C/L source set")
    row_keys = (
        "version", "path", "file_sha256", "object_sha256", "key_count",
        "sorted_keys", "sorted_key_array_sha256", "canonical_object_closed",
    )
    expected_versions = [
        "v3", "v5", "v6", "v7", "v8", "v9", "v10", "v11", "v12"]
    expected_counts = [37, 39, 41, 43, 46, 48, 50, 52, 54]
    role_rows: list[list[dict[str, Any]]] = []
    for role, raw in source_raw.items():
        literal = literal_module_assignment(
            raw, "HISTORICAL_REJECTION_EXACT_KEYSET_WITNESS", role)
        require(isinstance(literal, tuple) and len(literal) == 9 and
                all(isinstance(row, dict) and tuple(row) == row_keys
                    for row in literal),
                role + ": exact ordered nine-row historical witness")
        rows = copy.deepcopy(list(literal))
        require([row["version"] for row in rows] == expected_versions and
                [row["key_count"] for row in rows] == expected_counts and
                all(isinstance(row["sorted_keys"], list) and
                    len(row["sorted_keys"]) == row["key_count"] and
                    row["sorted_keys"] == sorted(set(row["sorted_keys"])) and
                    is_sha256(row["file_sha256"]) and
                    is_sha256(row["object_sha256"]) and
                    is_sha256(row["sorted_key_array_sha256"]) and
                    sha256_bytes(canonical(row["sorted_keys"])) ==
                        row["sorted_key_array_sha256"] and
                    row["canonical_object_closed"] is True
                    for row in rows) and
                sha256_bytes(canonical(rows)) ==
                    HISTORICAL_REJECTION_EXACT_KEYSET_WITNESS_SHA256,
                role + ": exact historical witness values and digest")
        role_rows.append(rows)
    require(role_rows[0] == role_rows[1] == role_rows[2],
            "P/C/L historical witness exact equality")
    return role_rows[0]


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
            "producer source-registry output shape exact75")
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
    "source_lifecycle_state",
    "v14_inherited_authority_exact12_member_count",
    "v14_inherited_authority_exact12_canonical_sha256",
    "v14_supersession_receipt_file_sha256",
    "v14_supersession_receipt_object_sha256",
    "producer_source_registry_census",
    "launcher_runtime_registry_helper_census",
    "runtime_registry_shape_consensus",
    "object_sha256",
}

PRODUCER_REGISTRY_CENSUS_KEYS = {
    "close_object_semantics",
    "explicit_key_count", "explicit_unique_key_count",
    "explicit_sorted_key_array_sha256", "unsupported_explicit_key_count",
    "explicit_ordered_key_array_sha256",
    "execution_proof_key_count", "execution_proof_keys",
    "execution_proof_return_is_direct_terminal",
    "execution_proof_unique_key_count",
    "execution_proof_unsupported_key_count",
    "execution_proof_values_all_literal_true",
    "execution_proof_expansion_exact_once",
    "explicit_and_execution_proof_keysets_disjoint",
    "in_memory_close_object_field_tamper_rejected",
    "in_memory_explicit_proof_overlap_rejected",
    "in_memory_nonstring_proof_key_rejected",
    "in_memory_preclosure_object_sha256_rejected",
    "object_closure_field_count", "object_sha256_absent_before_closure",
    "registry_return_is_direct_terminal",
    "computed_closed_registry_key_count", "matches",
}
LAUNCHER_RUNTIME_HELPER_CENSUS_KEYS = {
    "normalized_helper_ast_sha256", "explicit_key_guard_literals",
    "expected_normalized_helper_ast_sha256", "exact_single_raw_parameter",
    "stale_literal_62_count",
    "exact_execution_proof_7_guard_count",
    "exact_execution_proof_expansion_guard_count",
    "shape_formula_is_len_explicit_plus_len_proof_plus_one",
    "return_is_computed_shape", "exact_shape_75_guard_count",
    "nested_helper_scope_count",
    "normalized_helper_semantics_match_reviewed_template",
    "live_callsite_count", "live_callsite_owner",
    "live_callsite_is_direct_assignment",
    "live_callsite_uses_held_producer_raw",
    "live_computed_shape_consumed_by_expected_shapes_then_75_gate",
    "live_consumption_is_direct_need_gate",
    "held_producer_independent_computed_shape",
    "in_memory_dead_callsite_mutation_count",
    "in_memory_dead_callsite_rejected",
    "in_memory_stale_62_mutation_count",
    "in_memory_stale_62_rejected", "matches",
}
RUNTIME_REGISTRY_SHAPE_CONSENSUS_KEYS = {
    "producer_independent_closed_key_count",
    "launcher_actual_runtime_helper_matches",
    "source_declared_producerSourceRegistry_values",
    "audit_declared_producerSourceRegistry", "expected_closed_key_count",
    "v14_inherited_authority_runtime_wiring_matches",
    "matches",
}


def load_checker_report(
        path: Path, source_hashes: dict[str, str],
        expected_lifecycle: str,
) -> dict[str, Any]:
    require(expected_lifecycle == "CORE_PINNED",
            "this builder generation accepts only the frozen CORE_PINNED "
            "checker authority")
    require(path == CORE_PINNED_CHECKER_REPORT.resolve(),
            "checker census report exact frozen authority path")
    raw = read_regular_file_stable(path, expected_mode=0o444)
    require(sha256_bytes(raw) == CORE_PINNED_CHECKER_REPORT_FILE_SHA256,
            "checker census report exact frozen file pin")
    report = json.loads(
        raw.decode("utf-8"), object_pairs_hook=_no_duplicate_pairs)
    require(set(report) == CHECKER_REPORT_KEYS,
            "checker census report exact key closure")
    verify_object(report, "checker census report")
    require(report.get("object_sha256") ==
            CORE_PINNED_CHECKER_REPORT_OBJECT_SHA256,
            "checker census report exact frozen object pin")
    require(report.get("schema") ==
            "cm2.round306c79g.true-global-no-producer-consumer."
            "v15-static-checker-census.v1",
            "checker census report schema")
    require(expected_lifecycle in {"CORE_PINNED", "FINAL_STATIC"} and
            report.get("source_lifecycle_state") == expected_lifecycle,
            "checker report exact current JSON/source lifecycle")
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
    require(
        report["common_ordered_callsite_census_sha256"] not in {
            STALE_V11_COMMON_CALLSITE_SHA256,
            "8045428c8276b6a26ab24604a4f888329848a701f4225fe529c74c3b9add3de2",
        } and
        report["wider_local_callsite_census_sha256"] not in {
            STALE_V11_COMMON_CALLSITE_SHA256,
            "8045428c8276b6a26ab24604a4f888329848a701f4225fe529c74c3b9add3de2",
        },
        "refuse stale v11 or v14 general-callsite digest")
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
    require(
        report.get("v14_inherited_authority_exact12_member_count") == 12 and
        report.get("v14_inherited_authority_exact12_canonical_sha256") ==
            V14_EXACT12_CANONICAL_SHA256 and
        report.get("v14_supersession_receipt_file_sha256") ==
            V14_SUPERSESSION_RECEIPT_FILE_SHA256 and
        report.get("v14_supersession_receipt_object_sha256") ==
            V14_SUPERSESSION_RECEIPT_OBJECT_SHA256,
        "checker report exact v14 exact12 and supersession anchors")
    producer = report.get("producer_source_registry_census")
    require(
        isinstance(producer, dict) and
        set(producer) == PRODUCER_REGISTRY_CENSUS_KEYS and
        producer.get("explicit_key_count") == 67 and
        producer.get("explicit_unique_key_count") == 67 and
        is_sha256(producer.get("explicit_sorted_key_array_sha256")) and
        is_sha256(producer.get("explicit_ordered_key_array_sha256")) and
        producer.get("unsupported_explicit_key_count") == 0 and
        producer.get("execution_proof_key_count") == 7 and
        producer.get("execution_proof_unique_key_count") == 7 and
        producer.get("execution_proof_unsupported_key_count") == 0 and
        producer.get("execution_proof_keys") ==
            SOURCE_REGISTRY_EXECUTION_PROOF_EXACT7 and
        producer.get("execution_proof_return_is_direct_terminal") is True and
        producer.get("execution_proof_values_all_literal_true") is True and
        producer.get("execution_proof_expansion_exact_once") is True and
        producer.get("explicit_and_execution_proof_keysets_disjoint") is True and
        producer.get("in_memory_close_object_field_tamper_rejected") is True and
        producer.get("in_memory_explicit_proof_overlap_rejected") is True and
        producer.get("in_memory_nonstring_proof_key_rejected") is True and
        producer.get("in_memory_preclosure_object_sha256_rejected") is True and
        producer.get("object_closure_field_count") == 1 and
        producer.get("object_sha256_absent_before_closure") is True and
        producer.get("registry_return_is_direct_terminal") is True and
        producer.get("computed_closed_registry_key_count") == 75 and
        producer.get("matches") is True,
        "checker report producer actual registry exact67+7+1=75")
    close_semantics = producer.get("close_object_semantics")
    require(
        isinstance(close_semantics, dict) and
        set(close_semantics) == {
            "already_closed_rejection_guard_count",
            "direct_terminal_return_count", "exact_body_statement_count",
            "input_expansion_exact_once", "matches", "nested_scope_count",
            "normalized_close_object_ast_sha256",
            "object_sha256_is_digest_of_unclosed_input",
            "object_sha256_literal_field_exact_once",
            "single_positional_parameter"} and
        close_semantics.get("already_closed_rejection_guard_count") == 1 and
        close_semantics.get("direct_terminal_return_count") == 1 and
        close_semantics.get("exact_body_statement_count") == 2 and
        close_semantics.get("input_expansion_exact_once") is True and
        close_semantics.get("nested_scope_count") == 0 and
        is_sha256(close_semantics.get("normalized_close_object_ast_sha256")) and
        close_semantics.get(
            "object_sha256_is_digest_of_unclosed_input") is True and
        close_semantics.get(
            "object_sha256_literal_field_exact_once") is True and
        close_semantics.get("single_positional_parameter") is True and
        close_semantics.get("matches") is True,
        "checker report producer close_object exact semantics")
    launcher = report.get("launcher_runtime_registry_helper_census")
    require(
        isinstance(launcher, dict) and
        set(launcher) == LAUNCHER_RUNTIME_HELPER_CENSUS_KEYS and
        is_sha256(launcher.get("normalized_helper_ast_sha256")) and
        launcher.get("expected_normalized_helper_ast_sha256") ==
            launcher.get("normalized_helper_ast_sha256") and
        launcher.get("exact_single_raw_parameter") is True and
        launcher.get("explicit_key_guard_literals") == [67] and
        launcher.get("stale_literal_62_count") == 0 and
        launcher.get("exact_execution_proof_7_guard_count") == 1 and
        launcher.get("exact_execution_proof_expansion_guard_count") == 1 and
        launcher.get(
            "shape_formula_is_len_explicit_plus_len_proof_plus_one") is True and
        launcher.get("return_is_computed_shape") is True and
        launcher.get("exact_shape_75_guard_count") == 1 and
        launcher.get("nested_helper_scope_count") == 0 and
        launcher.get(
            "normalized_helper_semantics_match_reviewed_template") is True and
        launcher.get("live_callsite_count") == 1 and
        launcher.get("live_callsite_owner") == "validate_final_static_audit" and
        launcher.get("live_callsite_is_direct_assignment") is True and
        launcher.get("live_callsite_uses_held_producer_raw") is True and
        launcher.get(
            "live_computed_shape_consumed_by_expected_shapes_then_75_gate")
            is True and
        launcher.get("live_consumption_is_direct_need_gate") is True and
        launcher.get("held_producer_independent_computed_shape") == 75 and
        launcher.get("in_memory_dead_callsite_mutation_count") == 1 and
        launcher.get("in_memory_dead_callsite_rejected") is True and
        launcher.get("in_memory_stale_62_mutation_count") == 1 and
        launcher.get("in_memory_stale_62_rejected") is True and
        launcher.get("matches") is True,
        "checker report actual launcher runtime helper and explicit62 tamper gate")
    consensus = report.get("runtime_registry_shape_consensus")
    source_shapes = (
        consensus.get("source_declared_producerSourceRegistry_values")
        if isinstance(consensus, dict) else None)
    require(
        isinstance(consensus, dict) and
        set(consensus) == RUNTIME_REGISTRY_SHAPE_CONSENSUS_KEYS and
        consensus.get("producer_independent_closed_key_count") == 75 and
        consensus.get("launcher_actual_runtime_helper_matches") is True and
        isinstance(source_shapes, dict) and
        set(source_shapes) == {"producer", "consumer", "launcher"} and
        all(isinstance(values, list) and values and set(values) == {75}
            for values in source_shapes.values()) and
        consensus.get("audit_declared_producerSourceRegistry") ==
            (None if expected_lifecycle == "CORE_PINNED" else 75) and
        consensus.get("v14_inherited_authority_runtime_wiring_matches") is True and
        consensus.get("expected_closed_key_count") == 75 and
        consensus.get("matches") is True,
        "checker report producer/launcher/declaration shape consensus")
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


def add_v12_proof_constraints(
        node: Any, v12_proof: dict[str, Any]) -> None:
    """Extend each history object without changing the frozen ref census.

    The runtime contract fixes the inherited schema at exact46 definitions,
    exact242 references and exact52 closed objects.  Exact ``const`` schemas
    add v12 history while preserving all three censuses.  The rejected-v13
    receipt is static policy input, not a field in any of these seven runtime
    proof constructors; only the explicit validation booleans belong there.
    """
    if isinstance(node, dict):
        properties = node.get("properties")
        required = node.get("required")
        if (isinstance(properties, dict) and isinstance(required, list) and
                "published_then_officially_rejected_predecessor_v11" in
                    properties and
                "published_then_officially_rejected_predecessor_v11" in
                    required):
            v11_index = required.index(
                "published_then_officially_rejected_predecessor_v11")
            if "published_then_officially_rejected_predecessor_v12" not in properties:
                properties[
                    "published_then_officially_rejected_predecessor_v12"] = {
                        "const": copy.deepcopy(v12_proof)}
            if "published_then_officially_rejected_predecessor_v12" not in required:
                required.insert(
                    v11_index + 1,
                    "published_then_officially_rejected_predecessor_v12")
        for item in node.values():
            add_v12_proof_constraints(item, v12_proof)
    elif isinstance(node, list):
        for item in node:
            add_v12_proof_constraints(item, v12_proof)


def migrate_current_v14_surface_to_v15(node: Any) -> Any:
    """Rename only v14's current surface while preserving history payloads."""
    def migrate_text(value: str) -> str:
        placeholders = (
            ("v13_to_v14", "__c79g_transition_lower_underscore__",
             "v14_to_v15"),
            ("V13_TO_V14", "__c79g_transition_upper_underscore__",
             "V14_TO_V15"),
            ("v13-to-v14", "__c79g_transition_lower_dash__",
             "v14-to-v15"),
            ("V13-TO-V14", "__c79g_transition_upper_dash__",
             "V14-TO-V15"),
        )
        for old, placeholder, _ in placeholders:
            value = value.replace(old, placeholder)
        value = value.replace("v14", "v15").replace("V14", "V15")
        for _, placeholder, new in placeholders:
            value = value.replace(placeholder, new)
        return value

    if isinstance(node, dict):
        result: dict[Any, Any] = {}
        for key, value in node.items():
            if key == "rejected_prepublication_v13_supersession_receipt":
                result[key] = copy.deepcopy(value)
                continue
            migrated_key = migrate_text(key) if isinstance(key, str) else key
            require(migrated_key not in result,
                    "v14-to-v15 migration key collision: " +
                    repr(migrated_key))
            result[migrated_key] = migrate_current_v14_surface_to_v15(value)
        return result
    if isinstance(node, list):
        return [migrate_current_v14_surface_to_v15(value) for value in node]
    if isinstance(node, str):
        return migrate_text(node)
    return copy.deepcopy(node)


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


def insert_after_key(mapping: dict[str, Any], after: str, key: str,
                     value: Any) -> None:
    """Insert or replace one ordered key immediately after another."""
    require(after in mapping and key != after,
            "ordered insertion anchor exists: " + after)
    rebuilt: dict[str, Any] = {}
    for old_key, old_value in mapping.items():
        if old_key == key:
            continue
        rebuilt[old_key] = old_value
        if old_key == after:
            rebuilt[key] = copy.deepcopy(value)
    mapping.clear()
    mapping.update(rebuilt)


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


def add_required_schema(definition: dict[str, Any], key: str,
                        schema: dict[str, Any],
                        *, after: str | None = None) -> None:
    properties = definition["properties"]
    required = definition["required"]
    properties[key] = copy.deepcopy(schema)
    if key not in required:
        if after is not None and after in required:
            required.insert(required.index(after) + 1, key)
        else:
            required.append(key)


def replace_current_bundle_first_member(node: Any) -> None:
    old = str(V13_SUPERSESSION_RECEIPT.relative_to(ROOT))
    receipt = str(V14_SUPERSESSION_RECEIPT.relative_to(ROOT))
    if isinstance(node, dict):
        for value in node.values():
            replace_current_bundle_first_member(value)
    elif isinstance(node, list):
        if (len(node) >= 2 and node[0] == old and isinstance(node[1], str) and
                f"{BASE}_schema_v15.json" in node[1]):
            node[0] = receipt
        if (len(node) >= 2 and node[0] == "v13_supersession_receipt" and
                node[1] == "closed_schema_v15"):
            node[0] = "v14_registry_shape_drift_supersession_receipt"
        for value in node:
            replace_current_bundle_first_member(value)


def build_schema(
        frozen_v14_schema: dict[str, Any],
        v12_proof: dict[str, Any],
        v13_summary: dict[str, Any],
        v14_summary: dict[str, Any]) -> dict[str, Any]:
    """Pure v14-schema to v15-schema transform; never reads its target."""
    require(isinstance(frozen_v14_schema, dict) and
            frozen_v14_schema.get("$id") ==
                "cm2.round306c79g.true-global-no-producer-consumer."
                "v14.composite-authority-schema",
            "build_schema receives the pinned frozen v14 schema seed")
    require(
        v13_summary.get("receipt_file_sha256") ==
            V13_SUPERSESSION_RECEIPT_FILE_SHA256 and
        v14_summary.get("receipt_file_sha256") ==
            V14_SUPERSESSION_RECEIPT_FILE_SHA256 and
        v14_summary.get("inherited_authority_exact12_member_count") == 12,
        "schema transform binds historical v13 and terminal v14 authority")
    schema = migrate_current_v14_surface_to_v15(frozen_v14_schema)
    require(V15_STAGE2_SCHEMA_CONTRACT_TRANSFORM_COMPLETE is True,
            "FAIL_CLOSED_STAGE2_BLOCKER__V14_EXACT12_AND_RUNTIME_HELPER_"
            "KEYSET_EXACT56_AND_84_112_SCHEMA_TRANSFORM_NOT_COMPLETE")
    require(schema.get("$id") ==
            "cm2.round306c79g.true-global-no-producer-consumer."
            "v15.composite-authority-schema",
            "schema current-version id migrated to v15")
    schema["title"] = (
        "C79g v15 clean-room successor after published/rejected v14")
    schema["description"] = (
        "Closed v15 schema for the append-only zero-credit successor after "
        "the frozen v14 exact10, official rejection, and registry-shape-drift "
        "supersession receipt; all v3-v14 history remains byte-pinned and "
        "the actual launcher helper must close 67+7+1=75; runtime stays "
        "unauthorized until the exact8 cold publication boundary closes.")
    defs = schema["$defs"]
    defs["v10ColonPrefixPerClauseWitness"] = exact_closed_const_schema(
        V10_COLON_PREFIX_WITNESS)
    defs["v11DualValidatorDivergenceIncident"] = exact_closed_const_schema(
        V11_INCIDENT)
    defs["v11PublishedThenOfficiallyRejectedProof"] = \
        exact_closed_const_schema(V11_PROOF)
    add_v11_proof_refs(schema)
    add_v12_proof_constraints(schema, v12_proof)

    static = defs["staticFreezeProof"]
    if "published_then_officially_rejected_predecessor_v11_validated" not in static["properties"]:
        static["properties"][
            "published_then_officially_rejected_predecessor_v11_validated"] = {
                "const": True}
        static["required"].append(
            "published_then_officially_rejected_predecessor_v11_validated")
    for key in (
            "published_then_officially_rejected_predecessor_v12_validated",
            "rejected_prepublication_v13_supersession_receipt_validated"):
        if key not in static["properties"]:
            static["properties"][key] = {"const": True}
            static["required"].append(key)
    add_required_const(
        static, "v12_official_rejection_file_sha256",
        V12_REJECTION_FILE,
        after="published_then_officially_rejected_predecessor_v12_validated")
    add_required_const(
        static, "v12_official_rejection_object_sha256",
        V12_REJECTION_OBJECT,
        after="v12_official_rejection_file_sha256")
    add_required_schema(
        static, "v12_official_rejection_identity", {"type": "object"},
        after="v12_official_rejection_object_sha256")
    add_required_const(
        static, "v12_v5_rejection_shape_incident",
        v12_proof["v5_rejection_shape_incident"],
        after="v12_official_rejection_identity")
    add_required_schema(
        static, "historical_rejection_exact_keyset_witness", {
            "type": "array", "minItems": 9, "maxItems": 9,
        }, after="v12_v5_rejection_shape_incident")
    add_required_const(
        static, "historical_rejection_exact_keyset_witness_validated", True,
        after="historical_rejection_exact_keyset_witness")

    verification = defs["verificationSurfaceProof"]
    verification["properties"]["exact_attack_count_each"]["const"] = \
        FORMAL_ATTACK_COUNT

    independent = defs["independentConsumerProof"]
    rename_closed_property(
        independent,
        "current_v12_producer_source_content_opened_read_decoded_parsed_compiled_imported_or_executed",
        "current_v15_producer_source_content_opened_read_decoded_parsed_compiled_imported_or_executed")
    for obsolete in (
            "frozen_predecessor_incident_source_exact5_held_fd_bytes_read_only_noncredit",
            "v10_colon_prefix_witness_independently_rederived_from_inherited_exact5_held_fds"):
        independent["properties"].pop(obsolete, None)
        if obsolete in independent["required"]:
            independent["required"].remove(obsolete)
    rename_closed_property(
        independent,
        "inherited_incident_authority_exact17_held_and_terminally_replayed",
        "v14_inherited_authority_exact12_held_and_terminally_replayed")
    add_required_const(
        independent,
        "v14_inherited_authority_exact12_held_and_terminally_replayed",
        True,
        after="current_v15_producer_source_content_opened_read_decoded_parsed_compiled_imported_or_executed")
    add_required_const(
        independent,
        "v10_colon_prefix_witness_independently_rederived_from_inherited_exact10_held_fds",
        True,
        after="v14_inherited_authority_exact12_held_and_terminally_replayed")
    independent["properties"]["exact_attack_count_reexecuted"]["const"] = \
        FORMAL_ATTACK_COUNT

    later = defs["laterRejection"]
    for key, value in (
            ("v11_official_rejection_file_sha256", V11_REJECTION_FILE),
            ("v11_official_rejection_object_sha256", V11_REJECTION_OBJECT),
            ("v12_official_rejection_file_sha256", V12_REJECTION_FILE),
            ("v12_official_rejection_object_sha256", V12_REJECTION_OBJECT)):
        if key not in later["required"]:
            later["required"].append(key)
        later["properties"][key] = {"const": value}

    rename_key_recursively(
        schema,
        "current_exact8_first_member_is_shared_v10_official_rejection",
        "current_exact8_first_member_is_v13_supersession_receipt")
    rename_key_recursively(
        schema,
        "current_exact8_first_member_is_v10_official_rejection",
        "current_exact8_first_member_is_v13_supersession_receipt")
    rename_key_recursively(
        schema,
        "current_exact8_first_member_is_shared_v11_official_rejection",
        "current_exact8_first_member_is_v13_supersession_receipt")
    rename_key_recursively(
        schema,
        "current_exact8_first_member_is_v11_official_rejection",
        "current_exact8_first_member_is_v13_supersession_receipt")
    rename_key_recursively(
        schema,
        "current_exact8_first_member_is_v13_supersession_receipt",
        "current_exact8_first_member_is_v14_registry_shape_drift_supersession_receipt")
    rename_key_recursively(
        schema,
        "all_current_and_historical_88_identities_globally_unique_on_one_statx_mount",
        "all_current_and_historical_124_identities_globally_unique_on_one_statx_mount")
    rename_key_recursively(
        schema,
        "all_current_and_historical_98_identities_globally_unique_on_one_statx_mount",
        "all_current_and_historical_124_identities_globally_unique_on_one_statx_mount")
    rename_key_recursively(
        schema,
        "all_current_and_historical_113_identities_globally_unique_on_one_statx_mount",
        "all_current_and_historical_124_identities_globally_unique_on_one_statx_mount")
    for old, new in (
            ("current_v12_and_all_predecessor_unique_file_identity_count",
             "current_v15_and_all_predecessor_unique_file_identity_count"),
            ("current_v12_and_all_predecessor_same_statx_mount",
             "current_v15_and_all_predecessor_same_statx_mount"),
            ("v11_to_v12_transition_identity", "v14_to_v15_transition_identity"),
            ("v11_to_v12_transition_file_sha256",
             "v14_to_v15_transition_file_sha256"),
            ("v11_to_v12_transition_object_sha256",
             "v14_to_v15_transition_object_sha256"),
            ("v12_rejection_namespace", "v15_rejection_namespace"),
            ("v12_later_rejection", "v15_later_rejection"),
            ("reject_command_exempts_only_fresh_empty_v12_rejection_namespace",
             "reject_command_exempts_only_fresh_empty_v15_rejection_namespace")):
        rename_key_recursively(schema, old, new)
    replace_current_bundle_first_member(schema)
    defs["staticFreezeProof"]["properties"][
        "append_only_history_unique_file_identity_count"]["const"] = \
            V15_TERMINAL_UNIQUE_FILE_IDENTITY_COUNT
    defs["coldLaunchProof"]["properties"][
        "current_v15_and_all_predecessor_unique_file_identity_count"]["const"] = \
            V15_PREPUBLICATION_UNIQUE_FILE_IDENTITY_COUNT
    cold = defs["coldLaunchProof"]
    add_required_const(
        cold, "v12_official_rejection_file_sha256", V12_REJECTION_FILE)
    add_required_const(
        cold, "v12_official_rejection_object_sha256", V12_REJECTION_OBJECT,
        after="v12_official_rejection_file_sha256")
    add_required_const(
        cold, "v12_v5_rejection_shape_incident",
        v12_proof["v5_rejection_shape_incident"],
        after="v12_official_rejection_object_sha256")
    return schema


def build_contract(
        frozen_v14_contract: dict[str, Any], schema_file_sha256: str,
        v12_proof: dict[str, Any],
        v13_summary: dict[str, Any],
        v14_summary: dict[str, Any]) -> dict[str, Any]:
    """Pure v14-contract to v15-contract transform; never reads its target."""
    require(isinstance(frozen_v14_contract, dict),
            "build_contract receives a frozen v14 contract object")
    verify_object(
        frozen_v14_contract, "frozen v14 contract seed",
        V14_CONTRACT_OBJECT_SHA256)
    contract = migrate_current_v14_surface_to_v15(frozen_v14_contract)
    require(V15_STAGE2_SCHEMA_CONTRACT_TRANSFORM_COMPLETE is True,
            "FAIL_CLOSED_STAGE2_BLOCKER__V14_EXACT12_AND_RUNTIME_HELPER_"
            "KEYSET_AUTHORITY_ROOT_AND_84_112_CONTRACT_TRANSFORM_NOT_COMPLETE")
    require(contract.get("schema") ==
            "cm2.round306c79g.true-global-no-producer-consumer.v15.contract",
            "contract current-version schema migrated to v15")
    require("v15_bundle" in contract and "v14_bundle" not in contract,
            "contract current bundle key migrated to v15")
    contract["purpose"] = (
        "Append-only v15 zero-credit clean-room successor after the frozen "
        "published-then-officially-rejected v14 exact10, its official "
        "rejection, and the frozen registry-shape-drift supersession receipt. "
        "The inherited exact12 transfers zero credit; the v15 actual launcher "
        "helper must independently close explicit67 + proof7 + object1 = 75.")
    contract["published_then_officially_rejected_predecessor_v11"] = \
        copy.deepcopy(V11_PROOF)
    insert_after_key(
        contract, "published_then_officially_rejected_predecessor_v11",
        "published_then_officially_rejected_predecessor_v12", v12_proof)
    insert_after_key(
        contract, "published_then_officially_rejected_predecessor_v12",
        "rejected_prepublication_v13_supersession_receipt", v13_summary)
    insert_after_key(
        contract, "rejected_prepublication_v13_supersession_receipt",
        "published_then_officially_rejected_predecessor_v14", v14_summary)
    contract["v10_colon_prefix_witness"] = copy.deepcopy(
        V10_COLON_PREFIX_WITNESS)
    contract["v11_dual_validator_divergence_incident"] = copy.deepcopy(
        V11_INCIDENT)
    bundle = contract["v15_bundle"]
    base7_paths = [
        str(V14_SUPERSESSION_RECEIPT.relative_to(ROOT)),
        str(SCHEMA.relative_to(ROOT)),
        str(CONTRACT.relative_to(ROOT)),
        str(PRODUCER.relative_to(ROOT)),
        str(CONSUMER.relative_to(ROOT)),
        str(TRANSITION.relative_to(ROOT)),
        str(AUDIT.relative_to(ROOT)),
    ]
    bundle["base7_ordered_paths"] = copy.deepcopy(base7_paths)
    bundle["exact8_ordered_paths"] = [
        *base7_paths, str(LAUNCHER.relative_to(ROOT))]
    bundle["exact10_ordered_paths"] = [
        *bundle["exact8_ordered_paths"],
        str(V15_MANIFEST.relative_to(ROOT)),
        str(V15_OUTER.relative_to(ROOT)),
    ]
    bundle["contract"]["path"] = str(CONTRACT.relative_to(ROOT))
    bundle["closed_schema"]["path"] = str(SCHEMA.relative_to(ROOT))
    bundle["build_only_producer"]["path"] = str(PRODUCER.relative_to(ROOT))
    bundle["independent_verifier_assembler_authority_consumer"]["path"] = \
        str(CONSUMER.relative_to(ROOT))
    replace_current_bundle_first_member(bundle)
    bundle["closed_schema"]["file_sha256"] = schema_file_sha256
    receipts = bundle["post_source_static_trust_receipts"]
    receipts["static_audit_path"] = str(AUDIT.relative_to(ROOT))
    receipts["v14_to_v15_transition_path"] = str(
        TRANSITION.relative_to(ROOT))
    receipts["v11_official_rejection_path"] = V11_REJECTION_REL
    receipts["v12_official_rejection_path"] = V12_REJECTION_REL
    receipts["v13_supersession_receipt_path"] = str(
        V13_SUPERSESSION_RECEIPT.relative_to(ROOT))
    receipts["v14_official_rejection_path"] = V14_REJECTION_REL
    receipts["v14_registry_shape_drift_supersession_receipt_path"] = str(
        V14_SUPERSESSION_RECEIPT.relative_to(ROOT))
    receipts[
        "seal_stably_binds_v4_supersession_v5_rejection_v6_rejection_v7_rejection_v8_rejection_v8_rollout_incident_v9_rejection_v9_shape_drift_incident_v10_rejection_v10_regression_label_prefix_incident_v11_rejection_v11_dual_validator_divergence_incident_transition_and_audit_file_or_object_hashes"] = True
    receipts.pop(
        "seal_stably_binds_v4_supersession_v5_rejection_v6_rejection_v7_rejection_v8_rejection_v8_rollout_incident_v9_rejection_v9_shape_drift_incident_v10_rejection_v10_regression_label_prefix_incident_transition_and_audit_file_or_object_hashes",
        None)
    receipts.pop(
        "runtime_consumer_must_hold_strict_parse_object_close_and_terminally_replay_inherited_exact17",
        None)
    receipts["runtime_consumer_must_hold_strict_parse_object_close_and_terminally_replay_inherited_v14_exact12"] = True
    receipts.pop(
        "runtime_consumer_must_hold_strict_parse_object_close_and_terminally_replay_all_ten",
        None)
    outer = bundle["cold_launch_outer_closure"]
    outer["launcher_path"] = str(LAUNCHER.relative_to(ROOT))
    outer["exact8_manifest_path"] = str(V15_MANIFEST.relative_to(ROOT))
    outer["outer_last_path"] = str(V15_OUTER.relative_to(ROOT))
    outer["manifest_order"] = (
        "V14_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT_THEN_SCHEMA_THEN_"
        "CONTRACT_THEN_PRODUCER_THEN_INDEPENDENT_SOURCE_THEN_V14_TO_V15_"
        "TRANSITION_THEN_STATIC_AUDIT_THEN_LAUNCHER")
    outer.pop("current_v12_exact10_plus_all_append_only_predecessors_unique_file_identity_count", None)
    outer["current_v15_exact10_plus_all_append_only_predecessors_unique_file_identity_count"] = \
        V15_TERMINAL_UNIQUE_FILE_IDENTITY_COUNT
    outer.pop("all_115_file_identities_share_one_statx_mount", None)
    outer["all_126_file_identities_share_one_statx_mount"] = True
    outer.pop("all_88_file_identities_share_one_statx_mount", None)
    outer.pop("all_98_file_identities_share_one_statx_mount", None)
    outer[
        "launcher_holds_live_v11_exact10_plus_official_later_rejection_and_exact_singleton_namespace_under_same_lock"] = True
    outer[
        "launcher_validates_exact_v11_dual_validator_divergence_incident_under_same_lock"] = True
    outer[
        "launcher_rederives_exact40_v10_colon_prefix_witness_from_inherited_held_bytes_before_child_spawn"] = True
    outer[
        "launcher_holds_live_v12_exact10_plus_official_later_rejection_under_same_lock"] = True
    outer[
        "launcher_holds_and_terminally_replays_v13_incident_source_pyc_exact6_plus_supersession_receipt"] = True
    outer[
        "launcher_holds_and_terminally_replays_v14_exact10_plus_official_rejection_plus_supersession_receipt"] = True
    outer["v15_predecessor_unique_live_identity_count"] = \
        V15_PREDECESSOR_UNIQUE_FILE_IDENTITY_COUNT
    outer["v15_prepublication_unique_live_identity_count"] = \
        V15_PREPUBLICATION_UNIQUE_FILE_IDENTITY_COUNT
    outer["v15_terminal_unique_live_identity_count"] = \
        V15_TERMINAL_UNIQUE_FILE_IDENTITY_COUNT
    outer["v15_terminal_group_vector"] = copy.deepcopy(
        V15_TERMINAL_GROUP_VECTOR)
    outer[
        "producer_consumer_launcher_common_witness_helper_normalized_ast_sha256"] = HELPER_NORMALIZED_AST
    old_terminal = next((key for key in outer if key.startswith(
        "launcher_terminally_replays_v15_exact10_v10_exact10_")), None)
    if old_terminal is not None:
        value = outer.pop(old_terminal)
        outer[old_terminal.replace("v15_exact10_v10_exact10_",
                                   "v15_exact10_v11_exact10_v10_exact10_")
              .replace("namespace_v10_regression", "namespace_v11_dual_validator_divergence_incident_v10_regression")] = value
    bundle["acyclic_binding_order"] = (
        "V14_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT_THEN_SCHEMA_THEN_"
        "CONTRACT_THEN_PRODUCER_THEN_INDEPENDENT_SOURCE_THEN_V14_TO_V15_"
        "TRANSITION_THEN_STATIC_AUDIT_THEN_LAUNCHER_THEN_EXACT8_MANIFEST_"
        "THEN_OUTER_LAST")

    runtime = contract["independent_authority_consumer_protocol"]
    runtime.pop(
        "producer_or_upstream_producer_source_open_read_decode_parse_compile_import_or_execute_allowed",
        None)
    runtime[
        "current_v15_producer_source_open_read_decode_parse_compile_import_or_execute_allowed"] = False
    runtime.pop(
        "frozen_predecessor_incident_source_exact5_inherited_held_fd_bytes_read_only_noncredit_allowed",
        None)
    runtime.pop(
        "v10_colon_prefix_witness_independently_rederived_by_consumer_from_inherited_exact5_held_fds",
        None)
    runtime.pop(
        "inherited_incident_authority_exact17_held_and_terminally_replayed",
        None)
    runtime.pop(
        "v10_colon_prefix_witness_independently_rederived_by_consumer_from_inherited_exact17_held_fds",
        None)
    runtime[
        "v14_inherited_authority_exact12_held_and_terminally_replayed"] = True
    runtime[
        "v10_colon_prefix_witness_independently_rederived_by_consumer_from_v14_inherited_exact12_held_fds"] = True
    census = runtime["cold_live_ACK_final_dynamic_replay_census"]
    census["frozen_v11_readable_held_file_count"] = 7
    census["frozen_v11_source_metadata_only_held_count"] = 3
    census["v11_official_rejection_shared_readable_held_file_count"] = 1
    census.pop("v10_official_rejection_in_static_policy_held_file_count", None)
    census["v11_official_rejection_in_static_policy_held_file_count"] = 1
    census["frozen_v12_readable_held_file_count"] = 7
    census["frozen_v12_source_metadata_only_held_count"] = 3
    census["v12_official_rejection_shared_readable_held_file_count"] = 1
    census["v12_official_rejection_in_static_policy_held_file_count"] = 1
    census["v13_incident_source_readable_held_file_count"] = 3
    census["v13_incident_pyc_readable_held_file_count"] = 3
    census["v13_supersession_receipt_shared_readable_held_file_count"] = 1
    census["frozen_v14_exact10_readable_held_file_count"] = 7
    census["frozen_v14_exact10_source_metadata_only_held_count"] = 3
    census["v14_official_rejection_shared_readable_held_file_count"] = 1
    census["v14_supersession_receipt_shared_readable_held_file_count"] = 1
    census["v15_predecessor_unique_live_identity_count"] = \
        V15_PREDECESSOR_UNIQUE_FILE_IDENTITY_COUNT
    census["v15_prepublication_unique_live_identity_count"] = \
        V15_PREPUBLICATION_UNIQUE_FILE_IDENTITY_COUNT
    census["v15_terminal_unique_live_identity_count"] = \
        V15_TERMINAL_UNIQUE_FILE_IDENTITY_COUNT
    census["v15_terminal_group_vector"] = copy.deepcopy(
        V15_TERMINAL_GROUP_VECTOR)
    runtime.pop(
        "reconstructs_full_evidence_and_reexecutes_exact_121_coherent_attacks",
        None)
    runtime[
        "reconstructs_full_evidence_and_reexecutes_exact_137_coherent_attacks"] = True
    runtime["formal_attack_name_order_sha256"] = \
        FORMAL_ATTACK_NAME_ORDER_SHA256

    producer_bundle = contract["v15_bundle"]["build_only_producer"]
    producer_bundle["source_registry_execution_proof_exact_fields"] = \
        copy.deepcopy(SOURCE_REGISTRY_EXECUTION_PROOF_EXACT7)
    producer_bundle["source_registry_execution_proof_values_all_true"] = True

    authority = contract["composite_authority_predicate"]
    authority["authority_root_structure"] = CONTRACT_AUTHORITY_ROOT_STRUCTURE
    authority["preseal_root_domain"] = "CM2_C79G_V15_PRESEAL_ROOT_V2"
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
            "V11_DUAL_VALIDATOR_DIVERGENCE_INCIDENT", "LIVE_V14_EXACT10",
            "OFFICIAL_V14_LATER_REJECTION",
            "V14_RUNTIME_REGISTRY_SHAPE_DRIFT_INCIDENT")):
        raise ValueError("contract authority root omits v10/v11/v14 incident closure")
    if not all(name in authority["preseal_root_formula"] for name in (
            "v10_rejection_file_sha256", "v10_rejection_object_sha256",
            "trusted_v10_regression_label_prefix_incident_digest",
            "v11_rejection_file_sha256", "v11_rejection_object_sha256",
            "trusted_v11_dual_validator_divergence_incident_digest",
            "v14_rejection_file_sha256", "v14_rejection_object_sha256",
            "v14_supersession_receipt_file_sha256",
            "v14_supersession_receipt_object_sha256",
            "v14_inherited_exact12_canonical_sha256",
            "actual_launcher_registry_helper_normalized_ast_sha256")):
        raise ValueError("contract preseal root omits v10/v11/v14 incident inputs")
    for required in (
            "V10_EXACT10_VALID", "V10_OFFICIAL_REJECTION_VALID",
            "TRUSTED_V10_REGRESSION_LABEL_PREFIX_INCIDENT_RECORDED_FROM_FROZEN_AST_STRUCTURE",
            "V10_COLON_PREFIX_PER_CLAUSE_WITNESS_REDERIVED_FROM_INHERITED_HELD_FDS_VALID",
            "V11_EXACT10_VALID", "V11_OFFICIAL_REJECTION_VALID",
            "TRUSTED_V11_DUAL_VALIDATOR_DIVERGENCE_INCIDENT_RECORDED_WITHOUT_EXACT_FALSE_CLAUSE_INFERENCE",
            "V14_EXACT10_VALID", "V14_OFFICIAL_REJECTION_VALID",
            "V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT_VALID",
            "V14_INHERITED_AUTHORITY_EXACT12_HELD_AND_TERMINALLY_REPLAYED",
            "ACTUAL_LAUNCHER_RUNTIME_REGISTRY_HELPER_EXPLICIT67_PLUS_PROOF7_PLUS_OBJECT1_EQUALS75_VALID",
            "IN_MEMORY_EXPLICIT62_TAMPER_REJECTED"):
        if required not in authority["required_conjuncts"]:
            raise ValueError("contract missing required conjunct: " + required)
    contract["object_sha256"] = object_hash(contract)
    return contract


def build_transition(
        v14_transition: dict[str, Any], schema_file_sha256: str,
        contract_file_sha256: str, contract_object_sha256: str,
        producer_file_sha256: str,
        consumer_file_sha256: str, v12_proof: dict[str, Any],
        v13_summary: dict[str, Any],
        v14_summary: dict[str, Any]) -> dict[str, Any]:
    body: dict[str, Any] = {
        "schema": (
            "cm2.round306c79g.true-global-no-producer-consumer."
            "v14-to-v15-static-launch-transition.v1"),
        "status": (
            "STATIC_BYTES_CLOSED_V14_TO_V15__PHYSICAL_FREEZE_PENDING__"
            "RUNTIME_NOT_AUTHORIZED"),
        "receipt_path": str(TRANSITION.relative_to(ROOT)),
        "effective_checkpoint_object_sha256": CHECKPOINT,
        "transition_kind": V14_TO_V15_TRANSITION_KIND,
        "append_only_predecessor_v3_regression": copy.deepcopy(
            v14_transition["append_only_predecessor_v3_regression"]),
        "rejected_unpublished_predecessor_v4": copy.deepcopy(
            v14_transition["rejected_unpublished_predecessor_v4"]),
        "published_then_officially_rejected_predecessor_v5": copy.deepcopy(
            v14_transition[
                "published_then_officially_rejected_predecessor_v5"]),
        "published_then_officially_rejected_predecessor_v6": copy.deepcopy(
            v14_transition[
                "published_then_officially_rejected_predecessor_v6"]),
        "published_then_officially_rejected_predecessor_v7": copy.deepcopy(
            v14_transition[
                "published_then_officially_rejected_predecessor_v7"]),
        "published_then_officially_rejected_predecessor_v8": copy.deepcopy(
            v14_transition[
                "published_then_officially_rejected_predecessor_v8"]),
        "published_then_officially_rejected_predecessor_v9": copy.deepcopy(
            v14_transition[
                "published_then_officially_rejected_predecessor_v9"]),
        "published_then_officially_rejected_predecessor_v10": copy.deepcopy(
            v14_transition[
                "published_then_officially_rejected_predecessor_v10"]),
        "published_then_officially_rejected_predecessor_v11": copy.deepcopy(
            V11_PROOF),
        "published_then_officially_rejected_predecessor_v12": copy.deepcopy(
            v12_proof),
        "rejected_prepublication_v13_supersession_receipt": copy.deepcopy(
            v13_summary),
        "published_then_officially_rejected_predecessor_v14": copy.deepcopy(
            v14_summary),
        "successor_v15_static_bundle": {
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
            "static_audit_v15_path": str(AUDIT.relative_to(ROOT)),
            "cold_launcher_v15_path": str(LAUNCHER.relative_to(ROOT)),
        },
        "physical_mode_policy": {
            "v15_working_files_mode_before_cold_freeze": "0664",
            "v15_exact8_required_final_mode": "0444",
            "v15_exact8_required_final_nlink": 1,
            "v15_exact8_physical_freeze_completed": False,
            "v15_manifest_physical_freeze_completed": False,
            "v15_outer_physical_freeze_completed": False,
            "historical_modes_are_exact_observed_snapshot_guards_not_immutability_claims":
                True,
        },
        "cold_launch_boundary": {
            "base7_order": [
                "v14_registry_shape_drift_supersession_receipt",
                "closed_schema_v15",
                "contract_v15", "producer_v15", "consumer_v15",
                "transition_v14_to_v15", "static_audit_v15",
            ],
            "base7_first_member_is_v14_registry_shape_drift_supersession_receipt": True,
            "launcher_is_eighth": True,
            "manifest_is_ninth": True,
            "outer_is_tenth_and_last": True,
            "expected_predecessor_unique_file_identity_count":
                V15_PREDECESSOR_UNIQUE_FILE_IDENTITY_COUNT,
            "expected_prepublication_unique_file_identity_count":
                V15_PREPUBLICATION_UNIQUE_FILE_IDENTITY_COUNT,
            "expected_terminal_unique_file_identity_count":
                V15_TERMINAL_UNIQUE_FILE_IDENTITY_COUNT,
            "terminal_group_vector": copy.deepcopy(V15_TERMINAL_GROUP_VECTOR),
            "all_126_file_identities_must_share_one_statx_mount": True,
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


def v15_static_no_run() -> dict[str, Any]:
    runtime_artifacts = []
    runtime_named = os.lstat(RUNTIME)
    require(stat.S_ISDIR(runtime_named.st_mode) and
            not stat.S_ISLNK(runtime_named.st_mode),
            "official runtime remains a no-follow directory")
    if stat.S_ISDIR(runtime_named.st_mode):
        runtime_artifacts = [
            path for path in RUNTIME.rglob("*")
            if "c79g-v15" in path.name]
    require(not runtime_artifacts,
            "v15 runtime artifacts already exist; refuse static GO audit")

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
            "v15 protocol process exists; refuse static GO audit")

    pyc_count = 0
    pycache = OUT / "__pycache__"
    if path_lexists(pycache):
        pycache_named = os.lstat(pycache)
        require(stat.S_ISDIR(pycache_named.st_mode) and
                not stat.S_ISLNK(pycache_named.st_mode),
                "deliverables __pycache__ is a no-follow directory")
        stems = (PRODUCER.stem, CONSUMER.stem, LAUNCHER.stem)
        pyc_count = sum(
            any(path.name.startswith(stem + ".") for stem in stems)
            for path in pycache.glob("*.pyc"))
    require(pyc_count == 0,
            "v15 protocol pyc exists; refuse static GO audit")
    require(not path_lexists(V15_MANIFEST) and not path_lexists(V15_OUTER),
            "v15 manifest/outer already exists; refuse draft audit rebuild")
    return {
        "C79_entrypoint_executed": False,
        "C79_v15_runtime_artifact_count": 0,
        "C79_v15_process_count": 0,
        "pyc_or___pycache___created": False,
        "cold_manifest_or_outer_created_before_dual_GO": False,
    }


def build_static_audit(
        v14_audit: dict[str, Any], schema: dict[str, Any],
        schema_closure: dict[str, Any], transition: dict[str, Any],
        transition_raw: bytes, schema_file_sha256: str,
        contract_file_sha256: str,
        contract_object_sha256: str, source_raw: dict[str, bytes],
        source_hashes: dict[str, str], checker_report: dict[str, Any],
        pin_normalized_launcher_sha256: str,
        helper_callsites: list[dict[str, Any]],
        static_no_run: dict[str, Any], v12_proof: dict[str, Any],
        v13_summary: dict[str, Any],
        v14_summary: dict[str, Any]) -> dict[str, Any]:
    historical_rejection_exact_keyset_witness = \
        historical_rejection_exact_keyset_witness_from_sources(source_raw)
    old_inputs = v14_audit[
        "dual_independent_static_checkers"]["checker_A"]["input_sha256"]
    require(tuple(key for key in old_inputs
                  if key in STATIC_AUDIT_HISTORICAL_INPUT_KEYS) ==
            STATIC_AUDIT_HISTORICAL_INPUT_KEYS,
            "frozen v14 audit inherited historical input order")
    historical_inputs = {
        key: old_inputs[key] for key in STATIC_AUDIT_HISTORICAL_INPUT_KEYS}
    require(all(is_sha256(value) for value in historical_inputs.values()),
            "frozen v14 audit inherited historical input pins")

    transition_file_sha256 = sha256_bytes(transition_raw)
    inputs: dict[str, str] = {
        "schema": schema_file_sha256,
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
        "v12_rejection_file": V12_REJECTION_FILE,
        "v12_rejection_object": V12_REJECTION_OBJECT,
        "v12_producer_file": V12_EXACT10_FILE_SHA256_ORDER[3],
        "v12_consumer_file": V12_EXACT10_FILE_SHA256_ORDER[4],
        "v12_launcher_file": V12_EXACT10_FILE_SHA256_ORDER[7],
        "trusted_v12_v5_rejection_shape_incident_digest":
            V12_V5_REJECTION_SHAPE_INCIDENT_SHA256,
    }
    require(tuple(inputs) == STATIC_AUDIT_INPUT_KEY_ORDER and
            len(inputs) == 43 and
            sha256_bytes(canonical(list(inputs))) ==
                STATIC_AUDIT_INPUT_KEY_ORDER_SHA256 and
            all(is_sha256(value) for value in inputs.values()),
            "static audit exact43 ordered nonzero input closure")

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
        {"source_role": "consumer", "enclosing_function": "terminal_replay",
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
    final_registry_consensus = copy.deepcopy(
        checker_report["runtime_registry_shape_consensus"])
    require(final_registry_consensus.get(
                "audit_declared_producerSourceRegistry") is None and
            final_registry_consensus.get("matches") is True,
            "core-pinned checker consensus precedes static-audit declaration")
    final_registry_consensus[
        "audit_declared_producerSourceRegistry"] = 75
    final_registry_consensus["matches"] = (
        final_registry_consensus.get(
            "producer_independent_closed_key_count") == 75 and
        final_registry_consensus.get(
            "launcher_actual_runtime_helper_matches") is True and
        final_registry_consensus.get("expected_closed_key_count") == 75 and
        final_registry_consensus.get(
            "v14_inherited_authority_runtime_wiring_matches") is True)
    require(final_registry_consensus["matches"] is True,
            "final static-audit registry consensus exact75")
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
        "pin_normalization_preserves_v14_supersession_receipt_and_all_historical_pins":
            True,
        "pin_normalization_removes_current_audit_hash_dependency": True,
        "independent_common_callsite_implementation_count": 2,
        "all_common_callsite_censuses_equal": True,
        "final_launcher_must_reproduce_pin_normalized_ast_after_pin_injection":
            True,
        "held_launcher_pin_normalized_ast_sha256":
            pin_normalized_launcher_sha256,
        "actual_runtime_registry_shape_evidence": {
            "producer_source_registry_census": copy.deepcopy(
                checker_report["producer_source_registry_census"]),
            "launcher_runtime_registry_helper_census": copy.deepcopy(
                checker_report["launcher_runtime_registry_helper_census"]),
            "runtime_registry_shape_consensus": final_registry_consensus,
            "explicit62_in_memory_tamper_rejected": True,
            "actual_closed_registry_shape": 75,
        },
    }

    v4 = copy.deepcopy(
        v14_audit["predecessor_v4_rejection_supersession_regression"])
    v4["same_defects_absent_from_v15"] = v4.pop(
        "same_defects_absent_from_v14")
    v4["v15_closed_object_required_property_mismatch_count"] = v4.pop(
        "v14_closed_object_required_property_mismatch_count")
    v4["v15_closed_object_required_property_mismatch_count"] = \
        schema_closure["closed_object_mismatch_count"]

    body: dict[str, Any] = {
        "schema": (
            "cm2.round306c79g.true-global-no-producer-consumer.static-audit.v15"),
        "status": (
            "PASS_DUAL_STATIC_PIN_NORMALIZED_AST_GO_V15__"
            "PHYSICAL_COLD_FREEZE_PENDING__RUNTIME_NOT_AUTHORIZED"),
        "audit_path": str(AUDIT.relative_to(ROOT)),
        "effective_checkpoint_object_sha256": CHECKPOINT,
        "audited_v15_bundle": {
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
            "v14_to_v15_transition_receipt": {
                "path": str(TRANSITION.relative_to(ROOT)),
                "file_sha256": transition_file_sha256,
                "object_sha256": transition["object_sha256"],
            },
        },
        "predecessor_v3_exact10_regression": copy.deepcopy(
            v14_audit["predecessor_v3_exact10_regression"]),
        "v3_official_later_rejection_regression": copy.deepcopy(
            v14_audit["v3_official_later_rejection_regression"]),
        "predecessor_v4_rejection_supersession_regression": v4,
        "published_then_officially_rejected_predecessor_v5": copy.deepcopy(
            v14_audit[
                "published_then_officially_rejected_predecessor_v5"]),
        "published_then_officially_rejected_predecessor_v6": copy.deepcopy(
            v14_audit[
                "published_then_officially_rejected_predecessor_v6"]),
        "published_then_officially_rejected_predecessor_v7": copy.deepcopy(
            v14_audit[
                "published_then_officially_rejected_predecessor_v7"]),
        "published_then_officially_rejected_predecessor_v8": copy.deepcopy(
            v14_audit[
                "published_then_officially_rejected_predecessor_v8"]),
        "published_then_officially_rejected_predecessor_v9": copy.deepcopy(
            v14_audit[
                "published_then_officially_rejected_predecessor_v9"]),
        "published_then_officially_rejected_predecessor_v10": copy.deepcopy(
            v14_audit[
                "published_then_officially_rejected_predecessor_v10"]),
        "published_then_officially_rejected_predecessor_v11": copy.deepcopy(
            V11_PROOF),
        "published_then_officially_rejected_predecessor_v12": copy.deepcopy(
            v12_proof),
        "rejected_prepublication_v13_supersession_receipt": copy.deepcopy(
            v13_summary),
        "published_then_officially_rejected_predecessor_v14": copy.deepcopy(
            v14_summary),
        "v10_colon_prefix_witness": copy.deepcopy(V10_COLON_PREFIX_WITNESS),
        "v11_dual_validator_divergence_incident": copy.deepcopy(V11_INCIDENT),
        "v12_v5_rejection_shape_incident": copy.deepcopy(
            v12_proof["v5_rejection_shape_incident"]),
        "historical_rejection_exact_keyset_witness": copy.deepcopy(
            historical_rejection_exact_keyset_witness),
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
            "consumer_current_v15_producer_content_open_read_hash_decode_compile_import_or_execute_allowed":
                False,
            "consumer_exec_source_coordination_root_fds_pairwise_distinct": True,
            "consumer_v14_inherited_authority_exact12_bytes_read_only_noncredit_allowed":
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
            "all_persisted_v15_objects_D02_started": False,
            "all_persisted_v15_objects_D02_unlock": False,
            "all_persisted_v15_objects_formal_global_closure_credit": 0,
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
    require(tuple(body) == STATIC_AUDIT_TOP_LEVEL_KEY_ORDER,
            "static audit exact ordered top-level closure before object pin")
    require(sha256_bytes(canonical(
                body["v12_v5_rejection_shape_incident"])) ==
            V12_V5_REJECTION_SHAPE_INCIDENT_SHA256,
            "static audit exact v12 shape incident digest")
    return close_object(body)


def verify_constants() -> None:
    restricted_literal_self_test()
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
    assert len(STATIC_AUDIT_INPUT_KEY_ORDER) == 43
    assert sha256_bytes(canonical(list(STATIC_AUDIT_INPUT_KEY_ORDER))) == \
        STATIC_AUDIT_INPUT_KEY_ORDER_SHA256
    assert len(STATIC_AUDIT_TOP_LEVEL_KEY_ORDER) == 29
    assert len(set(STATIC_AUDIT_TOP_LEVEL_KEY_ORDER)) == 29
    assert len(V12_EXACT10_PATH_ORDER) == 10
    assert V12_EXACT10_FILE_SHA256_ORDER[1] == V12_SCHEMA_FILE_SHA256
    assert V12_EXACT10_FILE_SHA256_ORDER[2] == V12_CONTRACT_FILE_SHA256
    assert V12_EXACT10_OBJECT_SHA256_ORDER[2] == V12_CONTRACT_OBJECT_SHA256
    assert V12_EXACT10_FILE_SHA256_ORDER[5] == V12_TRANSITION_FILE_SHA256
    assert V12_EXACT10_OBJECT_SHA256_ORDER[5] == V12_TRANSITION_OBJECT_SHA256
    assert V12_EXACT10_FILE_SHA256_ORDER[6] == V12_AUDIT_FILE_SHA256
    assert V12_EXACT10_OBJECT_SHA256_ORDER[6] == V12_AUDIT_OBJECT_SHA256
    assert len(V14_EXACT12_PATH_ORDER) == 12
    assert V14_EXACT12_FILE_SHA256_ORDER[-2:] == (
        V14_REJECTION_FILE_SHA256,
        V14_SUPERSESSION_RECEIPT_FILE_SHA256)
    assert V14_EXACT12_OBJECT_SHA256_ORDER[-2:] == (
        V14_REJECTION_OBJECT_SHA256,
        V14_SUPERSESSION_RECEIPT_OBJECT_SHA256)
    rejection = load(ROOT / V11_REJECTION_REL)
    assert object_hash(rejection) == V11_REJECTION_OBJECT
    assert sha256_bytes(read_regular_file_stable(
        ROOT / V11_REJECTION_REL, expected_mode=0o444)) == V11_REJECTION_FILE


def build_schema_contract_from_frozen_v14_seed(
        seed_bundle: dict[str, Any],
        ) -> tuple[dict[str, Any], dict[str, Any], bytes, bytes]:
    schema_seed = seed_bundle.get("schema")
    contract_seed = seed_bundle.get("contract")
    require(isinstance(schema_seed, dict) and isinstance(contract_seed, dict),
            "frozen v14 schema/contract seed bundle")
    v12_proof = seed_bundle.get("v12_published_rejected_proof")
    v13_summary = seed_bundle.get("v13_supersession_summary")
    v14_summary = seed_bundle.get("v14_supersession_summary")
    require(all(isinstance(item, dict) for item in (
        v12_proof, v13_summary, v14_summary)),
        "frozen v12/v13 history and v14 supersession summary seed")
    schema = build_schema(
        schema_seed, v12_proof, v13_summary, v14_summary)
    schema_raw = draft_bytes(schema)
    contract = build_contract(
        contract_seed, sha256_bytes(schema_raw), v12_proof, v13_summary,
        v14_summary)
    contract_raw = draft_bytes(contract)
    verify_object(contract, "rebuilt v15 contract draft")
    return schema, contract, schema_raw, contract_raw


def official_lock_result() -> dict[str, Any]:
    return {
        "api": "fcntl.flock(LOCK_EX)",
        "lock_path": str(RUNTIME.relative_to(ROOT)),
        "root_output_runtime_no_follow_held_fds": True,
        "path_fd_mode_owner_mount_replayed_before_unlock": True,
        "held_before_first_protocol_input_read_through_terminal_replay": True,
        "output_emitted_only_after_successful_unlock": True,
    }


def command_seed_schema_contract(
        writer_window: OfficialStaticWriterWindow) -> dict[str, Any]:
    """O_EXCL-install v15 S/C drafts from the frozen v14 exact12."""
    verify_constants()
    seed_bundle = load_frozen_v14_static_seed_bundle()
    schema, contract, schema_raw, contract_raw = \
        build_schema_contract_from_frozen_v14_seed(seed_bundle)
    writer_window.revalidate()
    require(draft_pair_state((SCHEMA, CONTRACT)) == "absent",
            "seed-schema-contract requires both targets absent")
    write_draft_pair_exclusive((
        (SCHEMA, schema),
        (CONTRACT, contract),
    ))
    writer_window.revalidate()

    # Re-read every frozen seed after commit and require byte-identical output
    # reconstruction before the final same-file-descriptor output replay.
    terminal_seed_bundle = load_frozen_v14_static_seed_bundle()
    terminal_schema, terminal_contract, terminal_schema_raw, \
        terminal_contract_raw = build_schema_contract_from_frozen_v14_seed(
            terminal_seed_bundle)
    require(terminal_schema_raw == schema_raw and
            terminal_contract_raw == contract_raw,
            "terminal S/C rebuild exactly reproduces committed drafts")
    details = replay_draft_pair_exact((
        (SCHEMA, terminal_schema),
        (CONTRACT, terminal_contract),
    ))
    writer_window.revalidate()
    return {
        "status": "SEEDED_V15_SCHEMA_CONTRACT_DRAFTS__RUNTIME_NOT_AUTHORIZED",
        "official_writer_lock": official_lock_result(),
        "seed_schema_file_sha256": V14_SCHEMA_FILE_SHA256,
        "seed_contract_file_sha256": V14_CONTRACT_FILE_SHA256,
        "seed_contract_object_sha256": V14_CONTRACT_OBJECT_SHA256,
        "inherited_v14_exact12_canonical_sha256":
            V14_EXACT12_CANONICAL_SHA256,
        "installed_drafts": details,
        "schema_file_sha256": sha256_bytes(schema_raw),
        "contract_file_sha256": sha256_bytes(contract_raw),
        "contract_object_sha256": contract["object_sha256"],
    }


def command_schema_contract(
        writer_window: OfficialStaticWriterWindow) -> dict[str, Any]:
    """Recompute and held-FD replay an existing S/C pair without writing."""
    verify_constants()
    seed_bundle = load_frozen_v14_static_seed_bundle()
    schema, contract, schema_raw, contract_raw = \
        build_schema_contract_from_frozen_v14_seed(seed_bundle)
    writer_window.revalidate()
    require(draft_pair_state((SCHEMA, CONTRACT)) == "present",
            "schema-contract replay requires both targets present")
    replay_draft_pair_exact((
        (SCHEMA, schema),
        (CONTRACT, contract),
    ))

    terminal_seed_bundle = load_frozen_v14_static_seed_bundle()
    terminal_schema, terminal_contract, terminal_schema_raw, \
        terminal_contract_raw = build_schema_contract_from_frozen_v14_seed(
            terminal_seed_bundle)
    require(terminal_schema_raw == schema_raw and
            terminal_contract_raw == contract_raw,
            "terminal read-only S/C rebuild exactly reproduces inputs")
    details = replay_draft_pair_exact((
        (SCHEMA, terminal_schema),
        (CONTRACT, terminal_contract),
    ))
    writer_window.revalidate()
    schema_hash = sha256_bytes(schema_raw)
    return {
        "status": (
            "REPLAYED_EXISTING_V15_SCHEMA_CONTRACT_EXACT_BYTES__"
            "NO_WRITE__RUNTIME_NOT_AUTHORIZED"),
        "official_writer_lock": official_lock_result(),
        "replayed_drafts": details,
        "schema_file_sha256": schema_hash,
        "schema_definition_count": len(schema["$defs"]),
        "contract_file_sha256": sha256_bytes(contract_raw),
        "contract_object_sha256": contract["object_sha256"],
        "witness_object_sha256": WITNESS_OBJECT,
        "incident_sha256": INCIDENT_DIGEST,
    }


def command_transition_audit(
        checker_report_path: Path,
        writer_window: OfficialStaticWriterWindow) -> dict[str, Any]:
    """Rebuild only the two writable post-core v15 JSON drafts.

    The protocol Python files are byte-read, parsed, and compiled in memory for
    static structure only.  They are never imported or executed.  The general
    callsite algorithms are intentionally outside this helper; their current-
    source-bound, canonically closed report is mandatory and stale v11 census
    values are rejected.
    """
    verify_constants()
    seed_bundle = load_frozen_v14_static_seed_bundle()
    require(V15_STAGE2_SCHEMA_CONTRACT_TRANSFORM_COMPLETE is True,
            "FAIL_CLOSED_STAGE2_BLOCKER__V15_TRANSITION_AUDIT_REBUILD_NOT_READY")

    v14_transition = seed_bundle["transition"]
    v14_audit = seed_bundle["audit"]

    input_paths = (SCHEMA, CONTRACT, PRODUCER, CONSUMER, LAUNCHER)
    input_raw = {path: read_regular_file_stable(path) for path in input_paths}
    source_raw = {
        "producer": input_raw[PRODUCER],
        "consumer": input_raw[CONSUMER],
        "launcher": input_raw[LAUNCHER],
    }
    source_hashes = {
        role: sha256_bytes(raw) for role, raw in source_raw.items()}
    for role, raw in source_raw.items():
        parse_source_ast(raw, "current_v15_" + role)

    schema = json.loads(
        input_raw[SCHEMA], object_pairs_hook=_no_duplicate_pairs)
    contract = json.loads(
        input_raw[CONTRACT], object_pairs_hook=_no_duplicate_pairs)
    require(isinstance(schema, dict), "current v15 schema JSON object")
    require(isinstance(contract, dict), "current v15 contract JSON object")
    verify_object(contract, "current v15 contract")
    schema_file_sha256 = sha256_bytes(input_raw[SCHEMA])
    contract_file_sha256 = sha256_bytes(input_raw[CONTRACT])
    contract_object_sha256 = contract["object_sha256"]
    closure = schema_static_closure(schema, source_raw["producer"])

    pre_pair_state = draft_pair_state((TRANSITION, AUDIT))
    # This builder generation is authorized only by the frozen pre-T/A
    # CORE_PINNED report.  The same exact report also authorizes an idempotent
    # replay of the exact T/A pair while P/C/L bytes remain unchanged; a later
    # launcher-final source hash necessarily fails this generation closed.
    expected_checker_lifecycle = "CORE_PINNED"
    checker_report = load_checker_report(
        checker_report_path.resolve(), source_hashes,
        expected_checker_lifecycle)
    launcher_registry_helper = launcher_runtime_registry_helper_from_ast(
        source_raw["launcher"],
        producer_source_registry_shape_from_ast(source_raw["producer"]))
    require(
        launcher_registry_helper ==
            checker_report["launcher_runtime_registry_helper_census"],
        "builder independently reproduces checker actual launcher helper evidence")
    pin_normalized = pin_normalized_launcher_ast_sha256(
        source_raw["launcher"], "current_v15_launcher")
    helper_callsites = exact_helper_callsite_census([
        ("producer", source_raw["producer"]),
        ("consumer", source_raw["consumer"]),
        ("launcher", source_raw["launcher"]),
    ])

    transition = build_transition(
        v14_transition, schema_file_sha256, contract_file_sha256,
        contract_object_sha256, source_hashes["producer"],
        source_hashes["consumer"],
        seed_bundle["v12_published_rejected_proof"],
        seed_bundle["v13_supersession_summary"],
        seed_bundle["v14_supersession_summary"])
    transition_raw = draft_bytes(transition)
    require(object_hash(transition) == transition["object_sha256"],
            "rebuilt transition object closure")

    audit = build_static_audit(
        v14_audit, schema, closure, transition, transition_raw,
        schema_file_sha256, contract_file_sha256, contract_object_sha256,
        source_raw,
        source_hashes, checker_report, pin_normalized, helper_callsites,
        v15_static_no_run(),
        seed_bundle["v12_published_rejected_proof"],
        seed_bundle["v13_supersession_summary"],
        seed_bundle["v14_supersession_summary"])
    audit_raw = draft_bytes(audit)
    require(object_hash(audit) == audit["object_sha256"],
            "rebuilt static audit object closure")

    # Fail before the first write if any core input drifted during analysis.
    for path, raw in input_raw.items():
        require(read_regular_file_stable(path) == raw,
                "core input changed during rebuild: " + str(path))
    writer_window.revalidate()
    pair_action, pair_details = install_absent_or_replay_exact_pair((
        (TRANSITION, transition),
        (AUDIT, audit),
    ))
    writer_window.revalidate()

    # Terminally re-read and reconstruct the complete input graph after the
    # pair commit.  The official lock excludes the final-pin installer and
    # every other conforming static writer for this entire interval.
    terminal_seed_bundle = load_frozen_v14_static_seed_bundle()
    terminal_input_raw = {
        path: read_regular_file_stable(path) for path in input_paths}
    require(terminal_input_raw == input_raw,
            "terminal core input byte replay exactly equals precommit snapshot")
    terminal_source_raw = {
        "producer": terminal_input_raw[PRODUCER],
        "consumer": terminal_input_raw[CONSUMER],
        "launcher": terminal_input_raw[LAUNCHER],
    }
    terminal_source_hashes = {
        role: sha256_bytes(raw)
        for role, raw in terminal_source_raw.items()}
    terminal_schema = json.loads(
        terminal_input_raw[SCHEMA], object_pairs_hook=_no_duplicate_pairs)
    terminal_contract = json.loads(
        terminal_input_raw[CONTRACT], object_pairs_hook=_no_duplicate_pairs)
    require(isinstance(terminal_schema, dict) and
            isinstance(terminal_contract, dict),
            "terminal v15 schema/contract JSON objects")
    verify_object(terminal_contract, "terminal v15 contract")
    terminal_closure = schema_static_closure(
        terminal_schema, terminal_source_raw["producer"])
    terminal_checker_report = load_checker_report(
        checker_report_path.resolve(), terminal_source_hashes,
        expected_checker_lifecycle)
    require(terminal_checker_report == checker_report,
            "terminal checker census report exact replay")
    terminal_launcher_registry_helper = \
        launcher_runtime_registry_helper_from_ast(
            terminal_source_raw["launcher"],
            producer_source_registry_shape_from_ast(
                terminal_source_raw["producer"]))
    require(
        terminal_launcher_registry_helper == launcher_registry_helper,
        "terminal actual launcher runtime-helper evidence exact replay")
    terminal_pin_normalized = pin_normalized_launcher_ast_sha256(
        terminal_source_raw["launcher"], "terminal_current_v15_launcher")
    terminal_helper_callsites = exact_helper_callsite_census([
        ("producer", terminal_source_raw["producer"]),
        ("consumer", terminal_source_raw["consumer"]),
        ("launcher", terminal_source_raw["launcher"]),
    ])
    terminal_transition = build_transition(
        terminal_seed_bundle["transition"], schema_file_sha256,
        contract_file_sha256, contract_object_sha256,
        terminal_source_hashes["producer"],
        terminal_source_hashes["consumer"],
        terminal_seed_bundle["v12_published_rejected_proof"],
        terminal_seed_bundle["v13_supersession_summary"],
        terminal_seed_bundle["v14_supersession_summary"])
    terminal_transition_raw = draft_bytes(terminal_transition)
    terminal_audit = build_static_audit(
        terminal_seed_bundle["audit"], terminal_schema, terminal_closure,
        terminal_transition, terminal_transition_raw, schema_file_sha256,
        contract_file_sha256, contract_object_sha256, terminal_source_raw,
        terminal_source_hashes, terminal_checker_report,
        terminal_pin_normalized, terminal_helper_callsites,
        v15_static_no_run(),
        terminal_seed_bundle["v12_published_rejected_proof"],
        terminal_seed_bundle["v13_supersession_summary"],
        terminal_seed_bundle["v14_supersession_summary"])
    terminal_audit_raw = draft_bytes(terminal_audit)
    require(terminal_transition_raw == transition_raw and
            terminal_audit_raw == audit_raw and
            terminal_pin_normalized == pin_normalized and
            terminal_helper_callsites == helper_callsites,
            "terminal T/A rebuild exactly reproduces precommit drafts")
    pair_details = replay_draft_pair_exact((
        (TRANSITION, terminal_transition),
        (AUDIT, terminal_audit),
    ))
    writer_window.revalidate()
    return {
        "status": (
            "INSTALLED_EXCLUSIVE_V15_TRANSITION_AUDIT_DRAFT_PAIR__"
            "RUNTIME_NOT_AUTHORIZED"
            if pair_action == "installed_exclusive" else
            "REPLAYED_EXISTING_V15_TRANSITION_AUDIT_EXACT_BYTES__"
            "NO_WRITE__RUNTIME_NOT_AUTHORIZED"),
        "official_writer_lock": official_lock_result(),
        "pair_action": pair_action,
        "pair_details": pair_details,
        "transition_file_sha256": sha256_bytes(transition_raw),
        "transition_object_sha256": transition["object_sha256"],
        "static_audit_file_sha256": sha256_bytes(audit_raw),
        "static_audit_object_sha256": audit["object_sha256"],
        "static_audit_input_key_count": len(STATIC_AUDIT_INPUT_KEY_ORDER),
        "formal_attack_count": FORMAL_ATTACK_COUNT,
        "schema_definition_count": closure["definition_count"],
        "schema_ref_count": closure["reference_count"],
        "closed_object_count": closure["closed_object_count"],
        "pin_normalized_launcher_ast_sha256": pin_normalized,
    }


def main() -> None:
    if not V15_DRAFT_BUILDER_ENABLED:
        raise SystemExit(
            "C79g v15 builder draft is disabled until v14 exact12, actual "
            "runtime registry helper, exact56 rejection schema, and 84/112 census "
            "are independently complete")
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("seed-schema-contract")
    subparsers.add_parser("schema-contract")
    transition_audit = subparsers.add_parser("transition-audit")
    transition_audit.add_argument(
        "--checker-census-report", required=True, type=Path,
        help=(
            "canonically object-closed current-v15 external checker report; "
            "the report must bind producer/consumer/launcher file hashes and "
            "supply fresh wider/common callsite censuses"))
    args = parser.parse_args()
    writer_window = OfficialStaticWriterWindow.acquire()
    result: dict[str, Any] | None = None
    try:
        if args.command == "seed-schema-contract":
            result = command_seed_schema_contract(writer_window)
        elif args.command == "schema-contract":
            result = command_schema_contract(writer_window)
        elif args.command == "transition-audit":
            result = command_transition_audit(
                args.checker_census_report, writer_window)
        require(isinstance(result, dict), "formal builder result object exists")
        writer_window.revalidate()
    finally:
        # No status bytes are emitted while the official lock remains owned.
        writer_window.release()
    require(isinstance(result, dict), "formal builder result survives unlock")
    print(json.dumps(result, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
