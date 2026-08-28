#!/usr/bin/env python3
"""C79g v16r2 append-only zero-credit candidate builder.

This append-only v16r2 binds the independently verified C78s 13-member final
surface.  It independently replays C55A/C55B/C72g, both
byte-identical C78l builds and their verification/completion surface, and the
corresponding C78s surface.  It derives (never guesses) an exact
1,148-row overlay, a compact 76,832-row successor ledger, and all 862
reflection-parent closure rows.  This producer exposes only ``build`` and can
never verifies, assembles, authorizes, or awards credit.  Its candidate outer
is permanently non-authoritative.  The separately committed v16r2 seal plus the
downstream consumer's secure replay may derive only a zero-credit inner
composite; only the held-fd-bootstrapped, externally SHA-256-pinned cold
launcher may wrap that inner value into the one virtual positive-credit root.
The inline bootstrap, declared Python interpreter, Linux kernel, openat2,
statx, procfs, and sealed memfd are an explicit cold-start TCB.
"""

from __future__ import annotations
def r63ah_normalize_kraft_registry(value: dict[str, Any]) -> dict[str, Any]:
    dropped = {
        "C42_candidate_observed_physical_policy",
        "C42_independent_audit_observed_physical_policy",
        "C42_installation_receipt_observed_physical_policy",
        "held_direct_input_identity_count",
        "C42_rows_by_pair",
        "C53_projections_by_pair",
    }
    normalized = {
        key: copy.deepcopy(item)
        for key, item in value.items()
        if key not in dropped
    }
    normalized.update({
        "C42_held_directory_count": 3,
        "C42_candidate_directory_expected_mode": "0755",
        "C42_candidate_directory_expected_nlink": 2,
        "C42_independent_audit_directory_expected_mode": "0700",
        "C42_independent_audit_directory_expected_nlink": 2,
        "C42_installation_receipt_directory_expected_mode": "0500",
        "C42_installation_receipt_directory_expected_nlink": 2,
        "C42_auxiliary_directory_exact_member_count_each": 1,
        "historical_directory_modes_are_exact_observed_snapshot_guards_not_immutability_claims": True,
    })
    return normalized

import argparse
import ast
from collections import Counter, defaultdict
import copy
import ctypes
import errno
import fcntl
import gzip
import hashlib
import io
import json
import os
from pathlib import Path
import stat
import sys
from typing import Any, Iterable, Iterator, Mapping
import zlib


EXECUTED_SOURCE = Path(os.path.abspath(__file__))
COLD_EXEC_FD_ENV = "CM2_C79G_V16R2_COLD_EXEC_FD"
COLD_SOURCE_FD_ENV = "CM2_C79G_V16R2_COLD_SOURCE_FD"
COLD_COORDINATION_PARENT_FD_ENV = "CM2_C79G_V16R2_COORDINATION_PARENT_FD"
COLD_WORKSPACE_ROOT_ENV = "CM2_C79G_V16R2_COLD_WORKSPACE_ROOT"
COLD_WORKSPACE_ROOT_FD_ENV = "CM2_C79G_V16R2_COLD_WORKSPACE_ROOT_FD"
COLD_LAUNCHER_SHA_ENV = "CM2_C79G_V16R2_COLD_LAUNCHER_FILE_SHA256"
_cold_root_text = os.environ.get(COLD_WORKSPACE_ROOT_ENV)
ROOT = (Path(_cold_root_text) if _cold_root_text is not None
        else EXECUTED_SOURCE.parents[1])
OUT = ROOT / "deliverables"
V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT = OUT / "cm2_round306c79g_true_global_no_producer_consumer_v14_runtime_registry_shape_drift_rejection_supersession_receipt_v1.json"

ACTIVE_PREDECESSOR_SUPERSESSION = OUT / "cm2_round306c79g_true_global_no_producer_consumer_v16r2r62_active_predecessor_supersession_receipt_v1.json"
ACTIVE_SUCCESSOR_NAMESPACE = "v16r2r62_semantic_source"
ACTIVE_SUCCESSOR_NAMESPACE_TAG = "v16r2r62-semantic-regeneration"
ACTIVE_PREDECESSOR_SUPERSESSION_FILE_PIN = "bf90b37c218c18d974793498816f6165807685e3f8e806bbf034468a7af66194"
ACTIVE_PREDECESSOR_SUPERSESSION_OBJECT_PIN = "0262a45dfb6812eaae673955934f6eb0ca5d6ace92f75b428f1cde33e777c9c6"
HISTORICAL_V16_SEMANTIC_SUPERSESSION = OUT / "cm2_round306c79g_true_global_no_producer_consumer_v16_semantic_rejection_supersession_receipt_v1.json"
HISTORICAL_V16_SEMANTIC_SUPERSESSION_FILE_PIN = "4b05c7dcd7303311fed7b51ea878641e006e707b5fe413f2aefbc3146afddb3c"
HISTORICAL_V16_SEMANTIC_SUPERSESSION_OBJECT_PIN = "430c663c5ccababd932246d9bc87ecc08fa9957113792aa2bd1e10e205a2ff7c"
UPSTREAM_CHECKPOINT_OBJECT_PIN = "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab"
SUCCESSOR_CHECKPOINT_OBJECT_PIN = "dd9d64f3f0bd0dfd00fd399e3154517a34ba19cfb601ec749f44cbc08b03ca1b"
UPSTREAM_C53_CHECKPOINT_OBJECT_PIN = UPSTREAM_CHECKPOINT_OBJECT_PIN
SUCCESSOR_REJECTION_CHECKPOINT_OBJECT_PIN = SUCCESSOR_CHECKPOINT_OBJECT_PIN
CHECKPOINT_CHAIN_OBJECT_PINS = (UPSTREAM_C53_CHECKPOINT_OBJECT_PIN, SUCCESSOR_REJECTION_CHECKPOINT_OBJECT_PIN)
RUNTIME_AUTHORIZED = False
FINAL_BASE7_PINS_INSTALLED = False
FORMAL_GLOBAL_CLOSURE_CREDIT = 0
D02_UNLOCK = False
ACTIVE_EXACT8_FIRST_MEMBER = V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT
V16R2_DRAFT_RUNTIME_DISABLED = True
V16_DRAFT_RUNTIME_DISABLED = True
FINAL_V16R2_CORE_PINS_INSTALLED = True
FINAL_V16_CORE_PINS_INSTALLED = False
ACTIVE_REJECTED_RETRY_SUPERSESSION = OUT / "cm2_round306c79g_true_global_no_producer_consumer_v16r2r62_active_predecessor_supersession_receipt_v1.json"
SELF = OUT / "cm2_round306c79g_true_global_no_producer_consumer_v16r2r63ah_repair_semantic_source.py"
V12_FROZEN_PRODUCER = OUT / "cm2_round306c79g_true_global_no_producer_consumer_v12.py"
V12_FROZEN_CONSUMER = OUT / (
    "cm2_round306c79g_true_global_no_producer_consumer_"
    "independent_verifier_assembler_authority_consumer_v12.py")
V12_FROZEN_LAUNCHER = OUT / (
    "cm2_round306c79g_true_global_no_producer_consumer_cold_launch_v12.py")
SCHEMA = "cm2.round306c79g.true-global-no-producer-consumer.v16r2r62"
BASE = "cm2_round306c79g_true_global_no_producer_consumer_v16r2r62_semantic_source"

CONTRACT = OUT / "cm2_round306c79g_true_global_no_producer_consumer_contract_v16r2r63ah_repair.json"
CLOSED_SCHEMA = OUT / "cm2_round306c79g_true_global_no_producer_consumer_schema_v16r2r62.json"
V3_OFFICIAL_REJECTION = ROOT / (
    ".cm2-runtime/c79g-v3-rejections-"
    "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab/"
    "rejection.json")
V4_REJECTION_SUPERSESSION = OUT / (
    "cm2_round306c79g_true_global_no_producer_consumer_"
    "v4_rejection_supersession_receipt_v1.json")
V5_OFFICIAL_REJECTION_NAMESPACE = ROOT / (
    ".cm2-runtime/c79g-v5-rejections-"
    "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab")
V5_OFFICIAL_REJECTION = V5_OFFICIAL_REJECTION_NAMESPACE / "rejection.json"
V6_OFFICIAL_REJECTION_NAMESPACE = ROOT / (
    ".cm2-runtime/c79g-v6-rejections-"
    "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab")
V6_OFFICIAL_REJECTION = V6_OFFICIAL_REJECTION_NAMESPACE / "rejection.json"
V7_OFFICIAL_REJECTION_NAMESPACE = ROOT / (
    ".cm2-runtime/c79g-v7-rejections-"
    "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab")
V7_OFFICIAL_REJECTION = V7_OFFICIAL_REJECTION_NAMESPACE / "rejection.json"
V8_OFFICIAL_REJECTION_NAMESPACE = ROOT / (
    ".cm2-runtime/c79g-v8-rejections-"
    "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab")
V8_OFFICIAL_REJECTION = V8_OFFICIAL_REJECTION_NAMESPACE / "rejection.json"
V9_OFFICIAL_REJECTION_NAMESPACE = ROOT / (
    ".cm2-runtime/c79g-v9-rejections-"
    "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab")
V9_OFFICIAL_REJECTION = V9_OFFICIAL_REJECTION_NAMESPACE / "rejection.json"
V10_OFFICIAL_REJECTION_NAMESPACE = ROOT / (
    ".cm2-runtime/c79g-v10-rejections-"
    "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab")
V10_OFFICIAL_REJECTION = V10_OFFICIAL_REJECTION_NAMESPACE / "rejection.json"
V11_OFFICIAL_REJECTION_NAMESPACE = ROOT / (
    ".cm2-runtime/c79g-v11-rejections-"
    "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab")
V11_OFFICIAL_REJECTION = V11_OFFICIAL_REJECTION_NAMESPACE / "rejection.json"
V12_OFFICIAL_REJECTION_NAMESPACE = ROOT / (
    ".cm2-runtime/c79g-v12-rejections-"
    "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab")
V12_OFFICIAL_REJECTION = V12_OFFICIAL_REJECTION_NAMESPACE / "rejection.json"
V13_SUPERSESSION_RECEIPT = OUT / (
    "cm2_round306c79g_true_global_no_producer_consumer_"
    "v13_prepublication_pyc_contamination_rejection_supersession_receipt_v1.json")
V13_FROZEN_PRODUCER = OUT / (
    "cm2_round306c79g_true_global_no_producer_consumer_v13.py")
V13_FROZEN_CONSUMER = OUT / (
    "cm2_round306c79g_true_global_no_producer_consumer_"
    "independent_verifier_assembler_authority_consumer_v13.py")
V13_FROZEN_LAUNCHER = OUT / (
    "cm2_round306c79g_true_global_no_producer_consumer_cold_launch_v13.py")
V13_FROZEN_PRODUCER_PYC = OUT / "__pycache__" / (
    "cm2_round306c79g_true_global_no_producer_consumer_v13.cpython-312.pyc")
V13_FROZEN_CONSUMER_PYC = OUT / "__pycache__" / (
    "cm2_round306c79g_true_global_no_producer_consumer_"
    "independent_verifier_assembler_authority_consumer_v13.cpython-312.pyc")
V13_FROZEN_LAUNCHER_PYC = OUT / "__pycache__" / (
    "cm2_round306c79g_true_global_no_producer_consumer_"
    "cold_launch_v13.cpython-312.pyc")
V16_TO_V16R2_TRANSITION = OUT / "cm2_round306c79g_true_global_no_producer_consumer_v16r2r62_to_v16r2r63ah_repair_static_launch_transition_receipt_v1.json"
STATIC_AUDIT_V16R2 = OUT / "cm2_round306c79g_true_global_no_producer_consumer_static_audit_v16r2r63ah_repair.json"
COLD_LAUNCHER = OUT / "cm2_round306c79g_true_global_no_producer_consumer_cold_launch_v16r2r63ah_repair_semantic_source.py"
COLD_MANIFEST = OUT / "cm2_round306c79g_true_global_no_producer_consumer_cold_launch_manifest_v16r2r63ah_runtime_repair.sha256"
COLD_OUTER = OUT / "cm2_round306c79g_true_global_no_producer_consumer_cold_launch_outer_receipt_v16r2r63ah_runtime_repair.json"
# Draft current-core pins.  The final no-cycle injection is deliberately
# deferred until schema, contract, consumer, transition, audit and launcher
# bytes have independently converged.
V16R2_DRAFT_RUNTIME_DISABLED = True
FINAL_V16R2_CORE_PINS_INSTALLED = True
CONTRACT_FILE_PIN = "a05d09aed417c4ef5df5a32e85af02e49e46f4a086ccdd7f6fa49b2060ef5a39"
CONTRACT_OBJECT_PIN = "949f6e490ef54be69563c3647931d4257a086696dfbef6dee8049a75ec966137"
CLOSED_SCHEMA_FILE_PIN = "1a9c03d332a1c12a34f330b30acb77b13a8f315732fc0bc75be29d3b8c3e1577"
V16R2_DRAFT_CORE_PIN_SENTINELS = ("dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd", "eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee", "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff")
V3_REJECTION_FILE_PIN = "57ce7a4361555c4ff403f725f17ef9cef50446a2e76d7086635c30a0f17bc62f"
V3_REJECTION_OBJECT_PIN = "c946e0d8170a75e32aa7031b42cf0dd5b7b585ba463b7b1ce0010cb65bb3b421"
V4_REJECTION_SUPERSESSION_FILE_PIN = (
    "e3dff621fec2fa5bac14f73685c8f44ce89bc68d80b6478e0688ce926f57c183")
V4_REJECTION_SUPERSESSION_OBJECT_PIN = (
    "1c8fc9d91be75502b0741b096a1ca6d9d59b877b1e69daada15096669215d19f")
V5_OFFICIAL_REJECTION_FILE_PIN = (
    "c49218967b2d5023d07e5c65fa53df12f0383d6644bf4bd7d35a8e50abeb85b5")
V5_OFFICIAL_REJECTION_OBJECT_PIN = (
    "9a94bf8b580f6145c4977dd335d9a63c69057d18d62678ab47c7916c764f8e4c")
V6_OFFICIAL_REJECTION_FILE_PIN = (
    "3559dcfd9e6d0ebb0e093226d6d3ae8d09d67eaeb186d4ec956241af87fcbd06")
V6_OFFICIAL_REJECTION_OBJECT_PIN = (
    "87c0cd17ae6ca3885a01da82b47b66e96419eb778594b51423eb04cf3c68f48c")
V7_OFFICIAL_REJECTION_FILE_PIN = (
    "63d4bbc4f50ef674b6b90f6fde625ac4705d5272f500fd495111d445274ebf6b")
V7_OFFICIAL_REJECTION_OBJECT_PIN = (
    "29c43ad51082bd56c2291dea88b619731c2853969b79ea008abea1cca3c83ecd")
V8_OFFICIAL_REJECTION_FILE_PIN = (
    "3b00a60c6c30cc10171d82e8262f880d67aa975e9f040888a29d7bdb4014ef95")
V8_OFFICIAL_REJECTION_OBJECT_PIN = (
    "9fbc65609f33a62751b9fc60aa4def316a499dae9e3f64e1d4ae8a3be58894d5")
V9_OFFICIAL_REJECTION_FILE_PIN = (
    "bca8f1042a1f3ee5b82d85a2e10c6ed2bf35d486116870bf50387f9ee9dcd302")
V9_OFFICIAL_REJECTION_OBJECT_PIN = (
    "682ead5d02c386b992c15e1e845e5e35a3147e0c1387d440c604f431c7a8b1b4")
V10_OFFICIAL_REJECTION_FILE_PIN = (
    "1b5bbd9ec04f07e7d7d433685aa693b73bf2315a91e4813960bd5a81e8112828")
V10_OFFICIAL_REJECTION_OBJECT_PIN = (
    "efdb614e870e70c20202834d3c6ec1a7513a3e98ba5cb4e1b32f87976a529d76")
V11_OFFICIAL_REJECTION_FILE_PIN = (
    "f6cc10d8b7e72553ef0b7a32bbfb99255f36cce16b735002f17be58ae51d3bc8")
V11_OFFICIAL_REJECTION_OBJECT_PIN = (
    "7ae86e38c5910bc9ceaa0a4e5cb1f8fbbf1e73de9c0314fedabbd8cb2db3bb7a")
V12_OFFICIAL_REJECTION_FILE_PIN = (
    "b6b087a3e31b25f0bbe0ffe6caa40f3c181b2f77c5c8b6169ce3af27439762b5")
V12_OFFICIAL_REJECTION_OBJECT_PIN = (
    "18951895ea97f455bc3294e8ef9cdaa937f3b16e9831275b047e88142e9b91f6")
V13_SUPERSESSION_RECEIPT_FILE_PIN = (
    "098296d9807a89f58250f4fd404bdd45b1cf343e3e2e1c7a51a24d67225d016f")
V13_SUPERSESSION_RECEIPT_OBJECT_PIN = (
    "3c9c44500465c6b416cc0ee6689ea82cdd9096a79687b94f94c409ca5a78c677")
V13_INCIDENT_EXACT6_PINS = {
    V13_FROZEN_PRODUCER:
        "ec4982babaec3bfb6693e29a220ca827087fb591c77f6c715889e934f124310e",
    V13_FROZEN_CONSUMER:
        "a8b32b7e0073e70a95e6f5f17ad08b63b701ca64a1299f0f614215c5aa9f970a",
    V13_FROZEN_LAUNCHER:
        "aa1306ed3e764c69679db531c3dcd30d609ed1cbd699feda5ed17cc1e24da88b",
    V13_FROZEN_PRODUCER_PYC:
        "0383cab58260ff076b18482f2077ed100456b21bcc2587afd5e457c8a19d7d36",
    V13_FROZEN_CONSUMER_PYC:
        "f13c8f7f40139bcbe6d5f20014fb14d8659539814baf985f73f99fbb13ffccaa",
    V13_FROZEN_LAUNCHER_PYC:
        "50a210fe6c414d140f7e0ac9a969500192f68fafae2de9d104526d73479365e0",
}
V13_SUPERSESSION_NORMALIZED_EXACT10_CANONICAL_BYTE_LENGTH = 2657
V13_SUPERSESSION_NORMALIZED_EXACT10_CANONICAL_SHA256 = (
    "600768327003f17f0f367e64b03d0fd9ada23f2933db64845a37cfee140c61b5")
V13_SUPERSESSION_EXACT16_CANONICAL_BYTE_LENGTH = 3646
V13_SUPERSESSION_EXACT16_CANONICAL_SHA256 = (
    "bf70829a4632cd322ef45e9313d4150138a57f98966fcd93d2c7a718fb44f64e")
V16R2_PREDECESSOR_UNIQUE_LIVE_IDENTITY_COUNT = 116
V16R2_PREPUBLICATION_UNIQUE_LIVE_IDENTITY_COUNT = 124
V16R2_TERMINAL_UNIQUE_LIVE_IDENTITY_COUNT = 126
V16R2_TERMINAL_GROUP_VECTOR = (
    10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10,
    7, 1, 3, 3, 1, 1)
CHECKPOINT_OBJECT_PIN = "dd9d64f3f0bd0dfd00fd399e3154517a34ba19cfb601ec749f44cbc08b03ca1b"

# Direct immutable predecessor authority.  v14's exact10 was published and
# subsequently rejected; neither those bytes nor this witness transfer any
# credit into v16r2.  Runtime consumers must supply these bytes from distinct
# held descriptors and replay them in the exact order below.
V14_PUBLISHED_EXACT10_WITNESS = (
    ("v13_supersession_receipt", "deliverables/cm2_round306c79g_true_global_no_producer_consumer_v13_prepublication_pyc_contamination_rejection_supersession_receipt_v1.json", "098296d9807a89f58250f4fd404bdd45b1cf343e3e2e1c7a51a24d67225d016f", "3c9c44500465c6b416cc0ee6689ea82cdd9096a79687b94f94c409ca5a78c677"),
    ("closed_schema", "deliverables/cm2_round306c79g_true_global_no_producer_consumer_schema_v14.json", "3d07ccda67cb71d0e5c64d37c0d8e1fcf425de4fbfefddf03bf43934ffdaaa4d", None),
    ("contract", "deliverables/cm2_round306c79g_true_global_no_producer_consumer_contract_v14.json", "479a0b3f6b4f0ad7e25d22c9f32eec046758a9a7d40509a6bda200e8e41e0ece", "11fd8966ed631f3bcc0eb6b1881f0536c814b7a7c093eca8289680e38a7d7b8b"),
    ("build_only_producer", "deliverables/cm2_round306c79g_true_global_no_producer_consumer_v14.py", "9fa2f2e20cdf15ed37d7f3ff904197fa7bc46a4eec243cab0ae8fb477e2e1ff0", None),
    ("independent_consumer", "deliverables/cm2_round306c79g_true_global_no_producer_consumer_independent_verifier_assembler_authority_consumer_v14.py", "83c58e792b922ad57a7c031b4aca60fe4d5868679e6f7a70b513e3cc4b7dc24c", None),
    ("v13_to_v14_transition", "deliverables/cm2_round306c79g_true_global_no_producer_consumer_v13_to_v14_static_launch_transition_receipt_v1.json", "e8c810f85b511cbc3637321f872f96c996a854454ab7ae1fbb3f5bdf19d7fd95", "78912a8f23f7a2e229795aae0e609ca58232dbe36c52ad50bddad727f259413f"),
    ("static_audit", "deliverables/cm2_round306c79g_true_global_no_producer_consumer_static_audit_v14.json", "dbf5e6bf0f13524ee847d01482f9ad34f715368deb2df40207bd2eb436f293e9", "16a8bc6e274a9e4e5a8fe4b2a39b80136cbbb117bfdf2e0ed89ee90fdc71944a"),
    ("cold_launcher", "deliverables/cm2_round306c79g_true_global_no_producer_consumer_cold_launch_v14.py", "1236f53865d69d69d27091758a66b21ddc2ea33ed7f422bc8d56adb69a23f5b5", None),
    ("cold_manifest", "deliverables/cm2_round306c79g_true_global_no_producer_consumer_cold_launch_manifest_v14.sha256", "aae2b3735ca9d5469d4228189ff0127e85aca934c6e56dfa3650a4d4d46a5937", None),
    ("cold_outer", "deliverables/cm2_round306c79g_true_global_no_producer_consumer_cold_launch_outer_receipt_v14.json", "fa6d10673d96a36aaf0163c44e014162ffb7811b12b1efa9068d78c8aa5b2040", "786f9be9142ae0aafd31a6d86b08f815d5d4f7ca09fd67506f499635fdddc256"),
)
V14_PREDECESSOR_TERMINAL_REPLAY_ORDER = tuple(
    row[0] for row in V14_PUBLISHED_EXACT10_WITNESS
) + ("v14_official_rejection",)
V14_OFFICIAL_REJECTION_RELATIVE_PATH = (
    ".cm2-runtime/c79g-v14-rejections-" + UPSTREAM_CHECKPOINT_OBJECT_PIN +
    "/rejection.json")
V14_OFFICIAL_REJECTION_FILE_PIN = (
    "1cc1b5836457f219ce26aa8e463ebebe8d48a26d2145806d24f7cbfea6c7e567")
V14_OFFICIAL_REJECTION_OBJECT_PIN = (
    "0856353a2390c46b4f4bdefe9f13f6eb6e0e94aa352174cdc8d2f672ace4a41d")
V14_OFFICIAL_REJECTION_EXACT56_KEYSET_SHA256 = (
    "9c272f16d92497a7c5ced499e9e42c514b81cbfddcdb3f79c4f33837836e057e")
V14_PUBLISHED_EXACT10_PINS = V14_PUBLISHED_EXACT10_WITNESS
V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT_RELATIVE_PATH = (
    "deliverables/cm2_round306c79g_true_global_no_producer_consumer_"
    "v14_runtime_registry_shape_drift_rejection_supersession_receipt_v1.json")
V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT_FILE_PIN = (
    "aa4323027e2313f8a2eda0d6ffc039a537afe342d496d1f75cd73fcd47446c01")
V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT_OBJECT_PIN = (
    "93689e62ae36f405f045a769f4dc6f6e6fd83a16605d08299d5c3397ad657e2e")
V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT_DRAFT_SENTINELS = (
    "b4" * 32, "c4" * 32)
V14_EXACT10_FD_ENV_ORDER = tuple(
    (role, "CM2_C79G_V16R2_V14_" + role.upper() + "_FD")
    for role, _, _, _ in V14_PUBLISHED_EXACT10_WITNESS)
V14_OFFICIAL_REJECTION_FD_ENV = "CM2_C79G_V16R2_V14_OFFICIAL_REJECTION_FD"
V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT_FD_ENV = (
    "CM2_C79G_V16R2_V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT_FD")
V14_INHERITED_AUTHORITY_EXACT12_FD_ENV_ORDER = (
    V14_EXACT10_FD_ENV_ORDER + (
        ("v14_official_rejection", V14_OFFICIAL_REJECTION_FD_ENV),
        ("v14_registry_shape_drift_supersession_receipt",
         V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT_FD_ENV),
    ))
V14_INHERITED_AUTHORITY_EXACT12 = V14_PUBLISHED_EXACT10_WITNESS + (
    ("v14_official_rejection", V14_OFFICIAL_REJECTION_RELATIVE_PATH,
     V14_OFFICIAL_REJECTION_FILE_PIN, V14_OFFICIAL_REJECTION_OBJECT_PIN),
    ("v14_registry_shape_drift_supersession_receipt",
     V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT_RELATIVE_PATH,
     V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT_FILE_PIN,
     V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT_OBJECT_PIN),
)
V14_INHERITED_AUTHORITY_EXACT12_ROLE_ORDER = tuple(
    row[0] for row in V14_INHERITED_AUTHORITY_EXACT12)
V16R2_BOOTSTRAP_DESCRIPTOR_COUNT = 4
V16R2_CHILD_AUTHORITY_DESCRIPTOR_COUNT = 12
V16R2_CHILD_PASS_FD_COUNT = 16
V14_RUNTIME_REGISTRY_SHAPE_DRIFT_INCIDENT = {
    "schema": "cm2.round306c79g.true-global-no-producer-consumer.v14-runtime-registry-shape-drift-incident.v1",
    "failed_phase": "LAUNCHER_PRECHILD_PRODUCER_SOURCE_REGISTRY_SHAPE_CENSUS",
    "stale_launcher_explicit_key_expectation": 62,
    "actual_producer_explicit_key_count": 67,
    "execution_proof_key_count": 7,
    "enclosing_object_closure_count": 1,
    "stale_computed_shape": 70,
    "actual_registry_shape": 75,
    "producer_child_spawned": False,
    "consumer_child_spawned": False,
    "candidate_surface_count": 0,
    "stage_surface_count": 0,
    "positive_runtime_surface_count": 0,
    "formal_global_closure_credit": 0,
    "D02_unlock": False,
    "D02_gate_credit": 0,
    "D02_task_credit": 0,
    "D02_formal_pending_task_count": 33_638,
    "D02_started": False,
    "timestamps_are_not_chronology_authority": True,
    "chronology": [
        "V14_EXACT10_OUTER_PUBLISHED_RUNTIME_DEFERRED",
        "FIRST_RUNTIME_ATTEMPT_FAILED_BEFORE_CHILD_OR_SURFACE",
        "OFFICIAL_V14_REJECTION_INSTALLED",
        "TERMINAL_REPLAY_EXACT10_THEN_REJECTION_REQUIRED",
    ],
    "v14_credit_may_transfer_to_v16r2": False,
}
RUNTIME = ROOT / ".cm2-runtime"
CANDIDATE_A = RUNTIME / ("c79g-v16r2r63ah-candidate-a-" + UPSTREAM_CHECKPOINT_OBJECT_PIN)
CANDIDATE_B = RUNTIME / ("c79g-v16r2r63ah-candidate-b-" + UPSTREAM_CHECKPOINT_OBJECT_PIN)
COLD_EXACT8 = (    V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT,
    OUT / "cm2_round306c79g_true_global_no_producer_consumer_schema_v16r2r62.json",
    OUT / "cm2_round306c79g_true_global_no_producer_consumer_contract_v16r2r63ah_repair.json",
    SELF,
    OUT / "cm2_round306c79g_true_global_no_producer_consumer_independent_verifier_assembler_authority_consumer_v16r2r63ah_repair_semantic_source.py",
    OUT / "cm2_round306c79g_true_global_no_producer_consumer_v16r2r62_to_v16r2r63ah_repair_static_launch_transition_receipt_v1.json",
    OUT / "cm2_round306c79g_true_global_no_producer_consumer_static_audit_v16r2r63ah_repair.json",
    OUT / "cm2_round306c79g_true_global_no_producer_consumer_cold_launch_v16r2r63ah_repair_semantic_source.py",
)

# Frozen predecessor authority for the v16r2 successor draft.  This is a
# byte-level witness only; runtime remains disabled until the held-FD validator
# and the full v12 published-then-rejected proof are wired into all three
# sources and independently audited.
V12_PUBLISHED_EXACT10_WITNESS = (
    ("v11_official_rejection", ".cm2-runtime/c79g-v11-rejections-" +
     UPSTREAM_CHECKPOINT_OBJECT_PIN + "/rejection.json",
     "f6cc10d8b7e72553ef0b7a32bbfb99255f36cce16b735002f17be58ae51d3bc8",
     "7ae86e38c5910bc9ceaa0a4e5cb1f8fbbf1e73de9c0314fedabbd8cb2db3bb7a"),
    ("closed_schema", "deliverables/cm2_round306c79g_true_global_no_producer_consumer_schema_v12.json",
     "5ed911a55e8f90e750fdcaf6ab4fb6c9683bebaf66a4d6250329dff98acb2e28", None),
    ("contract", "deliverables/cm2_round306c79g_true_global_no_producer_consumer_contract_v12.json",
     "72246725b15891f92cbc6e3fa1c07ab4a76cdaa19f1b366a736f47f51989b343",
     "f5c1710817dc8e3aa7fe2bbf4b88e6e39baaa1b17bbeb0f8bf37c8c4575ae5d7"),
    ("build_only_producer", "deliverables/cm2_round306c79g_true_global_no_producer_consumer_v12.py",
     "4cafc594f8a60063b7e7caaa82ddcc2b7983d0fbf0929034cd3cb5f360f3ed1d", None),
    ("independent_consumer", "deliverables/cm2_round306c79g_true_global_no_producer_consumer_independent_verifier_assembler_authority_consumer_v12.py",
     "b74dee738257d485e9ca3357d7d138b5175b95e58f1c8ea87d1eca7bfc96b2ed", None),
    ("v11_to_v12_transition", "deliverables/cm2_round306c79g_true_global_no_producer_consumer_v11_to_v12_static_launch_transition_receipt_v1.json",
     "45dabc1ef60eb2f8ba34aa7daa69f9d2b3bedccd4168d9c472bd4bbb696b5400",
     "0673ecafaa9991cd78e905e144e7c8c1b91717a3d753befa13e82552d44a4072"),
    ("static_audit", "deliverables/cm2_round306c79g_true_global_no_producer_consumer_static_audit_v12.json",
     "ac29b1e31e0d1b51e8610b7699d1aaf55c80fa6f13f00b20b209c2889e121d37",
     "c1473ae0f5a08d8772227f61a55bd32c479a7b5c7d40da17b37e796abf4d9783"),
    ("cold_launcher", "deliverables/cm2_round306c79g_true_global_no_producer_consumer_cold_launch_v12.py",
     "b7aaff67be866f8fd7a01f71e97ea1491574f69e62b7760b6ced9183997444ba", None),
    ("cold_manifest", "deliverables/cm2_round306c79g_true_global_no_producer_consumer_cold_launch_manifest_v12.sha256",
     "297e9f58dc7657c6fa959dd45081efffe4e7e8dadcd16ab89457863e2661ece6", None),
    ("cold_outer", "deliverables/cm2_round306c79g_true_global_no_producer_consumer_cold_launch_outer_receipt_v12.json",
     "27129990a9d5b6697fd13ee8e2086100cbf158f12e5b767166d771e63088b6d0",
    "bc6d06141865954590bd11bfc96ad59dbbffa003f568355ecb47155a8a3a809d"),
)
V12_PUBLISHED_EXACT10_PINS = tuple(
    (ROOT / relative_path, file_sha256, object_sha256)
    for _, relative_path, file_sha256, object_sha256 in
        V12_PUBLISHED_EXACT10_WITNESS)
V12_PUBLISHED_EXACT10_NAMES = tuple(
    name for name, _, _, _ in V12_PUBLISHED_EXACT10_WITNESS)

V5_OFFICIAL_REJECTION_EXACT39_KEYS = frozenset({
    "D02_formal_pending_task_count", "D02_gate_credit", "D02_started",
    "D02_task_credit", "D02_unlock", "closed_schema_file_sha256",
    "cold_launcher_file_sha256", "cold_manifest_file_sha256",
    "cold_outer_file_sha256", "cold_outer_object_sha256",
    "commit_operation", "consumer_file_sha256", "contract_file_sha256",
    "contract_object_sha256", "effective_checkpoint_object_sha256",
    "file_fsync_required", "formal_global_closure_credit",
    "idempotent_existing_recovery_re_fsyncs_rejection_file_namespace_and_runtime_parent",
    "namespace_at_rest_mode", "namespace_exact_path",
    "namespace_fsync_required_after_file_and_after_reseal",
    "namespace_lock_held_write_window_mode", "object_sha256",
    "official_writer_coordination_lock_held_for_entire_reject_command",
    "official_writer_coordination_lock_policy",
    "overwrite_delete_or_reuse_allowed",
    "partial_malformed_or_extra_namespace_entry_revokes_authority",
    "producer_file_sha256", "rejection_file_mode", "rejection_file_nlink",
    "rejection_reason", "runtime_parent_fsync_required_after_namespace_creation",
    "schema", "standalone_authority", "status", "target_exact_path",
    "target_is_protocol_and_checkpoint_deterministic",
    "v4_rejection_supersession_file_sha256",
    "v4_rejection_supersession_object_sha256",
})
V5_OFFICIAL_REJECTION_EXACT39_KEYSET_SHA256 = (
    "3b74017677a537d23cacbfbf95f1cc78e3b33fc4839be24e02e848bdd7410460")
V12_OFFICIAL_REJECTION_EXACT54_KEYS = (
    V5_OFFICIAL_REJECTION_EXACT39_KEYS | frozenset({
        "v5_official_rejection_file_sha256", "v5_official_rejection_object_sha256",
        "v6_official_rejection_file_sha256", "v6_official_rejection_object_sha256",
        "v7_official_rejection_file_sha256", "v7_official_rejection_object_sha256",
        "v7_publication_lock_continuity_incident_object_sha256",
        "v8_official_rejection_file_sha256", "v8_official_rejection_object_sha256",
        "v9_official_rejection_file_sha256", "v9_official_rejection_object_sha256",
        "v10_official_rejection_file_sha256", "v10_official_rejection_object_sha256",
        "v11_official_rejection_file_sha256", "v11_official_rejection_object_sha256",
    }))
V12_OFFICIAL_REJECTION_EXACT54_KEYSET_SHA256 = (
    "271055dec2aa42fb77c14bbd9b5c19e6bd4281428a71dc5db55c7d0db168b985")
V12_V5_REJECTION_SHAPE_INCIDENT_SHA256 = (
    "79ff0e0aa1df0e455af3abad67348f22e3b6b95512b864edf673422e72e17167")
V12_FIRST_RUNTIME_ATTEMPT = {
    "attempted": True,
    "failed_phase": "LAUNCHER_PRECHILD_HELD_HISTORY_CONSTRUCTOR",
    "producer_child_spawned": False,
    "consumer_child_spawned": False,
    "candidate_write_started": False,
    "stage_write_started": False,
    "positive_runtime_surface_count": 0,
    "official_v12_rejection_installed": True,
}
V12_FIRST_RUNTIME_ATTEMPT_SHA256 = (
    "8ee3eefa4e9f7c1114d5968e5af9b40c8234295ef9ef05f8ef9cf19f1f776ce9")
V12_V5_REJECTION_SHAPE_INCIDENT = {
    "schema": "cm2.round306c79g.true-global-no-producer-consumer.v12-v5-rejection-shape-incident.v1",
    "incident_id": "V12_LAUNCHER_V5_REJECTION_WRONG_EXPECTED_KEY_COUNT_52_FOR_CANONICAL_EXACT39",
    "evidence_source": "FROZEN_V12_LAUNCHER_AST__FROZEN_V12_PRODUCER_AND_CONSUMER_AST__FROZEN_V5_REJECTION_BYTES__FIRST_BUILD_A_CONTROL_FLOW__OFFICIAL_V12_REJECTION",
    "failure_class": "FAIL_CLOSED_HISTORICAL_REJECTION_SHAPE_FALSE_NEGATIVE",
    "failure_label": "official v5 rejection binds published v5 exact10",
    "failed_phase": "LAUNCHER_PRECHILD_HELD_HISTORY_CONSTRUCTOR",
    "v12_launcher_source_path": "deliverables/cm2_round306c79g_true_global_no_producer_consumer_cold_launch_v12.py",
    "v12_launcher_source_file_sha256": "b7aaff67be866f8fd7a01f71e97ea1491574f69e62b7760b6ced9183997444ba",
    "v12_producer_source_file_sha256": "4cafc594f8a60063b7e7caaa82ddcc2b7983d0fbf0929034cd3cb5f360f3ed1d",
    "v12_consumer_source_file_sha256": "b74dee738257d485e9ca3357d7d138b5175b95e58f1c8ea87d1eca7bfc96b2ed",
    "v12_manifest_file_sha256": "297e9f58dc7657c6fa959dd45081efffe4e7e8dadcd16ab89457863e2661ece6",
    "v12_outer_file_sha256": "27129990a9d5b6697fd13ee8e2086100cbf158f12e5b767166d771e63088b6d0",
    "v12_outer_object_sha256": "bc6d06141865954590bd11bfc96ad59dbbffa003f568355ecb47155a8a3a809d",
    "v12_official_rejection_file_sha256": V12_OFFICIAL_REJECTION_FILE_PIN,
    "v12_official_rejection_object_sha256": V12_OFFICIAL_REJECTION_OBJECT_PIN,
    "diagnostic_class_name": "HeldV5PredecessorExact10",
    "diagnostic_function_name": "__init__",
    "diagnostic_frozen_source_line": 4750,
    "source_locations_are_diagnostic_not_authority": True,
    "actual_v5_rejection_key_count": 39,
    "wrong_v12_launcher_expected_key_count": 52,
    "v5_rejection_exact39_sorted_keys": sorted(V5_OFFICIAL_REJECTION_EXACT39_KEYS),
    "v5_rejection_exact39_keyset_sha256": V5_OFFICIAL_REJECTION_EXACT39_KEYSET_SHA256,
    "producer_v12_validator_uses_exact39_keyset": True,
    "consumer_v12_validator_uses_exact39_keyset": True,
    "launcher_v12_validator_used_bare_wrong_length_52": True,
    "bare_length_only_is_authority": False,
    "required_successor_fix": "THREE_WAY_EXACT39_SORTED_KEYSET_AND_KEYSET_SHA256_WITNESS__NO_BARE_LENGTH_AUTHORITY",
    "producer_child_spawned": False,
    "consumer_child_spawned": False,
    "candidate_write_started": False,
    "stage_write_started": False,
    "positive_runtime_surface_count": 0,
    "formal_global_closure_credit": 0,
    "D02_unlock": False,
    "D02_gate_credit": 0,
    "D02_task_credit": 0,
    "D02_formal_pending_task_count": 33_638,
    "D02_started": False,
}

# Cross-component machine contract.  Consumer, launcher, and static audit must
# use this exact order; sets alone are insufficient authority.
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
STATIC_AUDIT_INPUT_KEY_COUNT = 43
STATIC_AUDIT_INPUT_KEY_ORDER_SHA256 = (
    "7e11baf937aa7e9695f30718fcb14793ed2fdacbdf0f33bda659086d399e4574")

V11_PUBLISHED_EXACT10_PINS: tuple[tuple[Path, str, str | None], ...] = (
    (V10_OFFICIAL_REJECTION,
     "1b5bbd9ec04f07e7d7d433685aa693b73bf2315a91e4813960bd5a81e8112828",
     "efdb614e870e70c20202834d3c6ec1a7513a3e98ba5cb4e1b32f87976a529d76"),
    (OUT / "cm2_round306c79g_true_global_no_producer_consumer_schema_v11.json",
     "cf1630e3ab1b590876c663b8752d702eae5fe37b7bdbcc7824efbd03bbdbd8e2", None),
    (OUT / "cm2_round306c79g_true_global_no_producer_consumer_contract_v11.json",
     "c8851778bc8df7a9804efb5fc226548424b58119a2dff3f75bdea9fcac0ec5cf",
     "b998162a009927f13eb34a88e37f657515e43ae160b3d550de5edb0040486af9"),
    (OUT / "cm2_round306c79g_true_global_no_producer_consumer_v11.py",
     "f3b364afc0f5b2f729a3d7786eb8e9c25a9303959d6d2464a40395968090a30b", None),
    (OUT / ("cm2_round306c79g_true_global_no_producer_consumer_"
            "independent_verifier_assembler_authority_consumer_v11.py"),
     "d8ad069e3486b9d657e4840e504885bf13129050f68e6cc04e47b71f149370ec", None),
    (OUT / ("cm2_round306c79g_true_global_no_producer_consumer_"
            "v10_to_v11_static_launch_transition_receipt_v1.json"),
     "31b33566b898277fb8b272a6f3cd3b51b0b80eac4f58f43979dddfa647a38f4e",
     "9a253960a378521423751735dd272e06dec5c99cfc016d27bf66cfbe7673caaf"),
    (OUT / "cm2_round306c79g_true_global_no_producer_consumer_static_audit_v11.json",
     "6c94068e3f60a89fb608585ae5e6c7dbe02af17880195132bf7c9033ab797115",
     "007fba200b67c7704360bb85819435ed13cc6459c8dbac381b99c3adaaf884c3"),
    (OUT / "cm2_round306c79g_true_global_no_producer_consumer_cold_launch_v11.py",
     "9f6971d2ca3e2c8f448a6aeed70bc16f38154c626f7744a4e20ba723e3082cc2", None),
    (OUT / ("cm2_round306c79g_true_global_no_producer_consumer_"
            "cold_launch_manifest_v11.sha256"),
     "e27e9b58dbf57a72550da701589819dad7ebb01f6b3c649a56b701c99ef13135", None),
    (OUT / ("cm2_round306c79g_true_global_no_producer_consumer_"
            "cold_launch_outer_receipt_v11.json"),
     "689a4a323e742427c7f50ec6a7bbea08cdf28c36cbdb43d855a29601329f8c8f",
     "369dfe73b1dbc68e4147ba39e1c1b7155555b5443d9471159c5ac748723414a4"),
)
V11_PUBLISHED_EXACT10_NAMES = (
    "v10_official_rejection", "closed_schema", "contract",
    "build_only_producer", "independent_consumer", "v10_to_v11_transition",
    "static_audit", "cold_launcher", "cold_manifest", "cold_outer",
)

V10_PUBLISHED_EXACT10_PINS: tuple[tuple[Path, str, str | None], ...] = (
    (V9_OFFICIAL_REJECTION,
     "bca8f1042a1f3ee5b82d85a2e10c6ed2bf35d486116870bf50387f9ee9dcd302",
     "682ead5d02c386b992c15e1e845e5e35a3147e0c1387d440c604f431c7a8b1b4"),
    (OUT / "cm2_round306c79g_true_global_no_producer_consumer_schema_v10.json",
     "a42dc06e276cc9206b29ec22df74ac7f8d76a4afb1de30115d048e1f7ce52801", None),
    (OUT / "cm2_round306c79g_true_global_no_producer_consumer_contract_v10.json",
     "e9f9387c191ff7d34a75f73331d4926c989e0bcc641e21c6a3ace58fc5a7d479",
     "c99acd60e953a939e3e9fd95e7559ce4249dc6efda0c3653e8ac1ae42b771bf4"),
    (OUT / "cm2_round306c79g_true_global_no_producer_consumer_v10.py",
     "99bb321da8a63855e52c8d6757d00886c0deeb2182f5044cac35f645e2ebd00a", None),
    (OUT / ("cm2_round306c79g_true_global_no_producer_consumer_"
            "independent_verifier_assembler_authority_consumer_v10.py"),
     "3a72bba8930f15a66fa1111c76b9c3b6b2b9a2d21db32093d64d0c68a9f6d708", None),
    (OUT / ("cm2_round306c79g_true_global_no_producer_consumer_"
            "v9_to_v10_static_launch_transition_receipt_v1.json"),
     "6fe81931ee2051148e8ce0b7e67fcc45e56b992db7c74307f95aa9cc9dac6643",
     "249fd39eb7da989cbce59656f567028a38bb9900e4b577ae6d2f2ab4983ca6ac"),
    (OUT / "cm2_round306c79g_true_global_no_producer_consumer_static_audit_v10.json",
     "e8a3f0497451689ec0835bb4048fe7be69fee4926e40620cdd128cc7b55ffb71",
     "bb2cf294babf04fdbbbd35c88c1d6bce8c58426765ae69925c659b396feabcb8"),
    (OUT / "cm2_round306c79g_true_global_no_producer_consumer_cold_launch_v10.py",
     "629347f42bcfd2eca3d9e38d29eb3bea66ff9abd48ec16867040c74e81e9134c", None),
    (OUT / ("cm2_round306c79g_true_global_no_producer_consumer_"
            "cold_launch_manifest_v10.sha256"),
     "bead6e9e1c53478c874612f00cae6cab1add14069d41b71b4310eb9b46b958db", None),
    (OUT / ("cm2_round306c79g_true_global_no_producer_consumer_"
            "cold_launch_outer_receipt_v10.json"),
     "2d95b83a2658d10a70d7c1e87b195920fc8207fc639fa407ff23252e5bc5edc4",
     "fc2f595fb47795aff01396b9593630ef15f65237dcc0ffab2e5628e92722a6a4"),
)
V10_PUBLISHED_EXACT10_NAMES = (
    "v9_official_rejection", "closed_schema", "contract",
    "build_only_producer", "independent_consumer", "v9_to_v10_transition",
    "static_audit", "cold_launcher", "cold_manifest", "cold_outer",
)
V10_FIRST_RUNTIME_ATTEMPT = {
    "attempted": True,
    "producer_child_spawned": True,
    "candidate_write_started": False,
    "candidate_or_stage_created": False,
    "positive_runtime_surface_count": 0,
    "aborted_by_regression_label_prefix_guard": True,
    "command": "build",
    "orientation": "a",
}
V10_REGRESSION_LABEL_PREFIX_INCIDENT = {
    "schema": "cm2.round306c79g.true-global-no-producer-consumer."
              "v10-regression-label-prefix-incident.v1",
    "incident_id": "V10_PRODUCER_V9_REGRESSION_LABEL_PREFIX_COLON_MISMATCH",
    "evidence_source": "FROZEN_V10_PRODUCER_AST_CONTROL_FLOW_AND_FIRST_BUILD_A_STDERR",
    "producer_source_path":
        "deliverables/cm2_round306c79g_true_global_no_producer_consumer_v10.py",
    "producer_source_file_sha256": V10_PUBLISHED_EXACT10_PINS[3][1],
    "frozen_v9_launcher_path":
        "deliverables/cm2_round306c79g_true_global_no_producer_consumer_cold_launch_v9.py",
    "frozen_v9_launcher_file_sha256":
        "f7559ceeb7d491b8489812670392cb63e3cd5f6a2764db469e2dd51d6b5577fa",
    "regression_function": "v9_prechild_shape_drift_regression",
    "failure_label_without_colon_prefix":
        "exact v6 exact10, rejection, spawned-before-write and "
        "HeldSelf.identity defect regression",
    "colon_prefixed_failure_label_literal":
        ":exact v6 exact10, rejection, spawned-before-write and "
        "HeldSelf.identity defect regression",
    "exact_unprefixed_failure_label_literal_count": 0,
    "exact_colon_prefixed_failure_label_literal_count": 1,
    "failure_label_suffix_match_count": 1,
    "expanded_structural_dict_count": 1,
    "expanded_structural_dict_exact_key_count": 16,
    "validator_call_count": 1,
    "equality_gate_count": 2,
    "v9_launcher_hash_gate": True,
    "regression_guard_conjunct_count": 6,
    "regression_guard_true_conjunct_count": 5,
    "regression_guard_false_conjunct_count": 1,
    "regression_guard_conjunct_truth_vector": [True, True, True, True, False, True],
    "unique_false_conjunct_zero_based_index": 4,
    "unique_false_conjunct_source_line": 2315,
    "authority_source":
        "AST_STRUCTURE_AND_EXACT_PREFIX_JOIN__NOT_RAW_WHOLE_TREE_STRING_EQUALITY",
    "raw_whole_tree_string_equality_is_authority": False,
    "authority_derived_from_AST_structure_and_exact_prefix_join": True,
    "hold_static_freeze_trust_call_source_line": 6310,
    "regression_call_inside_hold_source_line": 3811,
    "candidate_stage_creation_source_line": 6415,
    "hold_function_contains_mkdir_call": False,
    "failure_occurs_before_candidate_or_stage_creation": True,
    "first_command": "build",
    "first_orientation": "a",
    "producer_child_spawned": True,
    "candidate_write_started": False,
    "candidate_or_stage_created": False,
    "positive_runtime_surface_count": 0,
    "inner_stderr_line":
        "REJECT: frozen v9 launcher statically embeds structural16 in exact equality gate",
    "outer_stderr_line": "REJECT: cold child rejected or failed",
    "required_successor_fix":
        "MATCH_COLON_PREFIX_BY_AST_STRUCTURE_AND_EXACT_PREFIX_JOIN__"
        "NEVER_RAW_WHOLE_TREE_LITERAL_MEMBERSHIP",
    "formal_global_closure_credit": 0,
    "D02_unlock": False,
    "D02_started": False,
}
V10_PUBLISHED_REJECTED_PROOF_KEY_ORDER = (
    "ordered_published_exact10", "official_later_rejection",
    "first_runtime_attempt", "regression_label_prefix_incident",
    "positive_and_stage_surfaces_absent", "all_ten_file_pins_match",
    "all_declared_object_pins_match", "all_ten_regular_0444_nlink1",
    "exact8_manifest_reconstructs_first_eight_in_order",
    "outer_last_pins_manifest_and_launcher",
    "outer_then_rejection_chronology_validated", "v10_execution_allowed",
    "v10_runtime_surfaces_authoritative", "formal_global_closure_credit",
    "D02_unlock", "D02_gate_credit", "D02_task_credit",
    "D02_formal_pending_task_count", "D02_started",
)
V10_PUBLISHED_REJECTED_PROOF_KEY_COUNT = 19
V10_REGRESSION_LABEL_PREFIX_INCIDENT_KEY_COUNT = 44
V10_FIRST_RUNTIME_ATTEMPT_KEY_COUNT = 8
V10_PUBLISHED_REJECTED_PROOF_CANONICAL_SHA256 = (
    "4577141f51b627048f674bf36f91e19a95d21f19fd0f496dd05c3c962ba89643")
V10_REGRESSION_LABEL_PREFIX_INCIDENT_CANONICAL_SHA256 = (
    "882d5646ea49b31ccdb9db4f5b8f5d6dd860d2ed8eb9b44c9d10f9c5eacfa33b")
V10_FIRST_RUNTIME_ATTEMPT_CANONICAL_SHA256 = (
    "08f9f80d5d5442ab60ed96fa71e97cc92695d3298cd3fa240ac51661a652114f")
V10_PROOF_KEY_ORDER = V10_PUBLISHED_REJECTED_PROOF_KEY_ORDER
V10_PROOF_CANONICAL_SHA256 = V10_PUBLISHED_REJECTED_PROOF_CANONICAL_SHA256
V10_FIRST_RUNTIME_ATTEMPT_KEY_ORDER = tuple(V10_FIRST_RUNTIME_ATTEMPT)
V10_REGRESSION_LABEL_PREFIX_INCIDENT_KEY_ORDER = tuple(
    V10_REGRESSION_LABEL_PREFIX_INCIDENT)

V10_COLON_PREFIX_WITNESS_OBJECT_PIN = (
    "374ec1404780efc5cf78da8e4c4b2554d25e6a1bc5da65d063263b34e0531011")
V10_COLON_PREFIX_HELPER_NORMALIZED_AST_SHA256 = (
    "38ebe2f639bdb26cac05cec05110ef78bf8057159ebf0f9c8f5d1ce22743fa07")
V10_COLON_PREFIX_WITNESS_KEY_ORDER = (
    "schema", "v10_producer_file_sha256", "v9_launcher_file_sha256",
    "six_guard_ast_sha256", "six_guard_conjunct_count",
    "fifth_membership_ast_sha256",
    "fifth_membership_is_exact_legacy_tree_wide_in",
    "expanded_structural_dict_count",
    "expanded_structural_dict_exact_key_count",
    "expanded_structural_dict_ast_sha256", "validator_helper_call_count",
    "equality_gate_count", "equality_gate_ast_sha256_ordered",
    "exact_unprefixed_failure_label_literal_count",
    "exact_colon_prefixed_failure_label_literal_count",
    "failure_label_suffix_match_count", "exact_colon_prefix_join_count",
    "exact_colon_prefix_join_ast_sha256",
    "legacy_guard_conjunct_truth_vector",
    "legacy_guard_true_conjunct_count", "legacy_guard_false_conjunct_count",
    "legacy_guard_unique_false_zero_based_index",
    "successor_clause_truth_vector", "successor_all_clauses_true",
    "direct_top_level_build_hold_call_count",
    "direct_top_level_hold_regression_call_count",
    "direct_top_level_build_stage_call_count",
    "build_hold_top_level_statement_index",
    "hold_regression_top_level_statement_index",
    "build_stage_top_level_statement_index", "hold_precedes_stage",
    "pre_regression_write_primitive_count",
    "pre_regression_write_primitive_census",
    "zero_or_multiple_expanded_dicts_controlled_reject",
    "exact_prefix_join_is_authority",
    "raw_whole_tree_string_membership_is_authority",
    "coherent_attack_count", "all_coherent_attacks_rejected",
    "formal_global_closure_credit", "object_sha256",
)
V10_COLON_PREFIX_WITNESS_KEY_COUNT = 40
V11_INCIDENT_FORMAL_ATTACK_NAMES = (
    "v11incident:exact_prefix_join_colon_removed",
    "v11incident:exact_prefix_join_double_colon",
    "v11incident:unrelated_bare_suffix_literal_injection",
    "v11incident:unrelated_colon_prefixed_literal_without_exact_join",
    "v11incident:duplicate_exact_prefix_join",
    "v11incident:join_rewritten_fstring_format_or_other_variable",
    "v11incident:equality_gate_delete_or_unrelated_eq_injection",
    "v11incident:structural16_15_17_or_multiple_candidate_dicts",
    "v11incident:regression_dead_nested_loop_or_exception_control_flow",
    "v11incident:hold_after_stage_or_pre_regression_write_primitive",
    "v11incident:duplicate_hold_regression_or_stage_call",
    "v11incident:inherited_fd_path_inode_mount_or_hash_mismatch",
    "v11incident:producer_consumer_launcher_helper_ast_drift",
    "v11incident:witness_truth_vector_key_order_or_digest_tamper",
    "v11incident:v11_rejection_or_positive_surface_closure_violation",
    "v11incident:zero_structural16_match_must_controlled_reject_not_indexerror",
)

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
V11_DUAL_VALIDATOR_DIVERGENCE_INCIDENT = {
    "schema": "cm2.round306c79g.true-global-no-producer-consumer."
              "v11-dual-validator-divergence-incident.v1",
    "incident_id":
        "V11_LAUNCHER_GATE_PASSED__PRODUCER_COMPOSITE_GUARD_REJECTED__"
        "NO_EXACT_FALSE_CLAUSE",
    "evidence_source":
        "FROZEN_V11_LAUNCHER_AND_PRODUCER_AST__FIRST_BUILD_A_STDERR__"
        "OFFICIAL_REJECTION",
    "v11_producer_source_path":
        "deliverables/cm2_round306c79g_true_global_no_producer_consumer_v11.py",
    "v11_producer_source_file_sha256": V11_PUBLISHED_EXACT10_PINS[3][1],
    "v11_launcher_source_path":
        "deliverables/cm2_round306c79g_true_global_no_producer_consumer_"
        "cold_launch_v11.py",
    "v11_launcher_source_file_sha256": V11_PUBLISHED_EXACT10_PINS[7][1],
    "v11_official_rejection_file_sha256": V11_OFFICIAL_REJECTION_FILE_PIN,
    "v11_official_rejection_object_sha256": V11_OFFICIAL_REJECTION_OBJECT_PIN,
    "first_command": "build",
    "first_orientation": "a",
    "producer_child_spawned": True,
    "candidate_write_started": False,
    "candidate_or_stage_created": False,
    "positive_runtime_surface_count": 0,
    "launcher_gate_function": "v10_regression_label_prefix_gate",
    "launcher_gate_passed_before_child_spawn": True,
    "producer_guard_function":
        "v10_regression_label_prefix_incident_regression",
    "producer_composite_guard_rejected": True,
    "producer_failure_label":
        "frozen v10 sole-false colon-prefix regression and pre-stage control flow",
    "producer_embedded_v10_incident_key_count_claim": 44,
    "producer_embedded_v10_incident_actual_key_count": 45,
    "producer_composite_guard_conjunct_count": 12,
    "exact_failing_subpredicate_persisted": False,
    "specific_false_clause_authority": "UNAVAILABLE",
    "child_consumed_inherited_held_predecessor_fds": False,
    "child_reopened_predecessor_paths": True,
    "launcher_and_producer_validator_implementations_distinct": True,
    "producer_per_clause_witness_persisted": False,
    "v10_colon_prefix_witness_object_sha256":
        V10_COLON_PREFIX_WITNESS_OBJECT_PIN,
    "v10_colon_prefix_witness_key_count": V10_COLON_PREFIX_WITNESS_KEY_COUNT,
    "v10_colon_prefix_witness_successor_clause_truth_vector": [True] * 15,
    "v10_colon_prefix_witness_all_clauses_true": True,
    "inner_stderr_line":
        "REJECT: frozen v10 sole-false colon-prefix regression and pre-stage "
        "control flow",
    "outer_stderr_line": "REJECT: cold child rejected or failed",
    "failure_occurs_before_candidate_or_stage_creation": True,
    "official_rejection_strictly_after_v11_outer": True,
    "required_successor_fix":
        "INHERITED_HELD_FD_BYTES__THREE_INDEPENDENT_IDENTICAL_HELPERS__"
        "EXACT_PER_CLAUSE_WITNESS",
    "required_held_fd_fix":
        "CHILD_REVALIDATES_INHERITED_V10_V9_V11_AND_REJECTION_FDS__"
        "NO_SECOND_PATH_VIEW_AS_INCIDENT_AUTHORITY",
    "required_validator_fix":
        "EXACT40_CLOSED_WITNESS__CONTROLLED_ZERO_OR_MULTIPLE_DICT_REJECT__"
        "NO_RAW_TREE_LITERAL_AUTHORITY",
    "formal_global_closure_credit": 0,
    "D02_unlock": False,
    "D02_started": False,
    "standalone_authority": False,
    "exact_false_clause_claim_allowed": False,
}
V11_DUAL_VALIDATOR_DIVERGENCE_INCIDENT_KEY_ORDER = tuple(
    V11_DUAL_VALIDATOR_DIVERGENCE_INCIDENT)
V11_DUAL_VALIDATOR_DIVERGENCE_INCIDENT_KEY_COUNT = 45
V11_DUAL_VALIDATOR_DIVERGENCE_INCIDENT_CANONICAL_SHA256 = (
    "64db719d426d3604be39d9bcd52118c1c39a409e47c2aaf38704b18d49ce7ab3")
V11_FIRST_RUNTIME_ATTEMPT_KEY_ORDER = tuple(V11_FIRST_RUNTIME_ATTEMPT)
V11_FIRST_RUNTIME_ATTEMPT_KEY_COUNT = 8
V11_FIRST_RUNTIME_ATTEMPT_CANONICAL_SHA256 = (
    "3b768c47f673b18c090946aee79dd103c9a37855451b4af09e0f7bd8042ab63f")
V11_PUBLISHED_REJECTED_PROOF_KEY_ORDER = (
    "ordered_published_exact10", "official_later_rejection",
    "first_runtime_attempt", "dual_validator_divergence_incident",
    "positive_and_stage_surfaces_absent", "all_ten_file_pins_match",
    "all_declared_object_pins_match", "all_ten_regular_0444_nlink1",
    "exact8_manifest_reconstructs_first_eight_in_order",
    "outer_last_pins_manifest_and_launcher",
    "outer_then_rejection_chronology_validated", "v11_execution_allowed",
    "v11_runtime_surfaces_authoritative", "formal_global_closure_credit",
    "D02_unlock", "D02_gate_credit", "D02_task_credit",
    "D02_formal_pending_task_count", "D02_started",
)
V11_PUBLISHED_REJECTED_PROOF_KEY_COUNT = 19
V11_PUBLISHED_REJECTED_PROOF_CANONICAL_SHA256 = (
    "8ee05054f12eddddb000f354a3dd1354532a91e37ef1b6d53a250257d9fe8990")

V9_PUBLISHED_EXACT10_PINS: tuple[tuple[Path, str, str | None], ...] = (
    (V8_OFFICIAL_REJECTION,
     "3b00a60c6c30cc10171d82e8262f880d67aa975e9f040888a29d7bdb4014ef95",
     "9fbc65609f33a62751b9fc60aa4def316a499dae9e3f64e1d4ae8a3be58894d5"),
    (OUT / "cm2_round306c79g_true_global_no_producer_consumer_schema_v9.json",
     "2ddd254e43a196bb550fce69552c7f51eae063f4a9b75bc5818099c93335080b", None),
    (OUT / "cm2_round306c79g_true_global_no_producer_consumer_contract_v9.json",
     "c37676119597f235f94104a55095c07e292fdd5c373c1811eeeed10c1b3d333f",
     "9a5fc94e11a30099ea0e23a574394399842efb8b350c98e9c16c5e8a8ce3963a"),
    (OUT / "cm2_round306c79g_true_global_no_producer_consumer_v9.py",
     "e3dfcf7d2bda8daaeaf1412685909a1a96e1ff88f8d3c6ab1645288ee97c5a70", None),
    (OUT / ("cm2_round306c79g_true_global_no_producer_consumer_"
            "independent_verifier_assembler_authority_consumer_v9.py"),
     "0b38317123f88dc5f065603e51f63171ac0fcd3760de758cd1aa50544f8d3c97", None),
    (OUT / ("cm2_round306c79g_true_global_no_producer_consumer_"
            "v8_to_v9_static_launch_transition_receipt_v1.json"),
     "ff4b42e258fec6cdd68d3c24f4903c9f3c2cec1ed2dc8f19dca703bddb45c522",
     "618f560f9ebbaaa5442af66af11f2efa7e4fe110a4f9cb586e3ab4424a1f95dc"),
    (OUT / "cm2_round306c79g_true_global_no_producer_consumer_static_audit_v9.json",
     "1c272852c18bff065a6b641d9c1f2a1c5a0da6db2a6e86a20588acb2be843571",
     "39463fbf2fb1c12ec68e4802b3ecd7dc48a95a2af6fcfe3430a27a0cb6ef9f4e"),
    (OUT / "cm2_round306c79g_true_global_no_producer_consumer_cold_launch_v9.py",
     "f7559ceeb7d491b8489812670392cb63e3cd5f6a2764db469e2dd51d6b5577fa", None),
    (OUT / ("cm2_round306c79g_true_global_no_producer_consumer_"
            "cold_launch_manifest_v9.sha256"),
     "648f3dce04ca5fdfed8635e0f8c0d21c09404b3799dbfd108e92013fab5392a4", None),
    (OUT / ("cm2_round306c79g_true_global_no_producer_consumer_"
            "cold_launch_outer_receipt_v9.json"),
     "498a2d3c46c091f3a218c835bef0557b783401e81bb30dfb131562c23027b28b",
     "7df5cfed652b2696fa63387b9d471cd1947f90dd269c4e7846ffa0f6641ad6be"),
)
V9_PUBLISHED_EXACT10_NAMES = (
    "v8_official_rejection", "closed_schema", "contract",
    "build_only_producer", "independent_consumer", "v8_to_v9_transition",
    "static_audit", "cold_launcher", "cold_manifest", "cold_outer",
)
V13_SUPERSESSION_EXACT16 = (
    ("v10_producer", V10_PUBLISHED_EXACT10_PINS[3][0],
     V10_PUBLISHED_EXACT10_PINS[3][1]),
    ("v9_launcher", V9_PUBLISHED_EXACT10_PINS[7][0],
     V9_PUBLISHED_EXACT10_PINS[7][1]),
    ("v11_producer", V11_PUBLISHED_EXACT10_PINS[3][0],
     V11_PUBLISHED_EXACT10_PINS[3][1]),
    ("v11_launcher", V11_PUBLISHED_EXACT10_PINS[7][0],
     V11_PUBLISHED_EXACT10_PINS[7][1]),
    ("v11_rejection", V11_OFFICIAL_REJECTION,
     V11_OFFICIAL_REJECTION_FILE_PIN),
    ("v12_producer", V12_FROZEN_PRODUCER,
     V12_V5_REJECTION_SHAPE_INCIDENT["v12_producer_source_file_sha256"]),
    ("v12_consumer", V12_FROZEN_CONSUMER,
     V12_V5_REJECTION_SHAPE_INCIDENT["v12_consumer_source_file_sha256"]),
    ("v12_launcher", V12_FROZEN_LAUNCHER,
     V12_V5_REJECTION_SHAPE_INCIDENT["v12_launcher_source_file_sha256"]),
    ("v5_rejection", V5_OFFICIAL_REJECTION, V5_OFFICIAL_REJECTION_FILE_PIN),
    ("v12_rejection", V12_OFFICIAL_REJECTION,
     V12_OFFICIAL_REJECTION_FILE_PIN),
    ("v13_build_only_producer_source", V13_FROZEN_PRODUCER,
     V13_INCIDENT_EXACT6_PINS[V13_FROZEN_PRODUCER]),
    ("v13_independent_consumer_source", V13_FROZEN_CONSUMER,
     V13_INCIDENT_EXACT6_PINS[V13_FROZEN_CONSUMER]),
    ("v13_cold_launcher_source", V13_FROZEN_LAUNCHER,
     V13_INCIDENT_EXACT6_PINS[V13_FROZEN_LAUNCHER]),
    ("v13_build_only_producer_pyc", V13_FROZEN_PRODUCER_PYC,
     V13_INCIDENT_EXACT6_PINS[V13_FROZEN_PRODUCER_PYC]),
    ("v13_independent_consumer_pyc", V13_FROZEN_CONSUMER_PYC,
     V13_INCIDENT_EXACT6_PINS[V13_FROZEN_CONSUMER_PYC]),
    ("v13_cold_launcher_pyc", V13_FROZEN_LAUNCHER_PYC,
     V13_INCIDENT_EXACT6_PINS[V13_FROZEN_LAUNCHER_PYC]),
)
V9_FIRST_RUNTIME_ATTEMPT = {
    "attempted": True,
    "producer_child_spawned": False,
    "candidate_write_started": False,
    "positive_runtime_surface_count": 0,
    "aborted_by_v6_defect_shape_drift_guard": True,
}
V6_PERSISTED_HELD_SELF_IDENTITY_DEFECT = {
    "source_path":
        "deliverables/cm2_round306c79g_true_global_no_producer_consumer_v6.py",
    "class_name": "HeldSelf",
    "missing_attribute": "identity",
    "failing_function": "hold_static_freeze_trust",
    "failing_expression":
        "len({guard.identity for guard in current_cold_ten_guards})",
    "frozen_source_line": 2041,
    "deterministic_failure_kind": "AttributeError",
    "failure_occurs_before_candidate_or_stage_creation": True,
    "same_defect_must_be_absent_from_v7": True,
}
V6_LAUNCHER_EXPANDED_STRUCTURAL_EVIDENCE = {
    "source_path":
        "deliverables/cm2_round306c79g_true_global_no_producer_consumer_v6.py",
    "class_name": "HeldSelf",
    "missing_attribute": "identity",
    "failing_function": "hold_static_freeze_trust",
    "failing_expression":
        "len({guard.identity for guard in current_cold_ten_guards})",
    "diagnostic_source_lines": [2041, 2062, 2235],
    "source_locations_are_diagnostic_not_authority": True,
    "guard_identity_structural_census": 3,
    "target_structural_comprehension_count": 1,
    "target_structural_comprehension_ast_sha256":
        "a7fb9f5f32fd3fbf06a7fafce3643c003e2f90a2b5be42872838e11da4f20b6c",
    "normalized_frozen_source_ast_sha256":
        "1b4ddb88cb5ac48548ac2bcad3e4d13f93bf41e40d9905c3647e4c56ce09fe48",
    "independent_semantic_checker_count": 2,
    "independent_semantic_checkers_agree": True,
    "deterministic_failure_kind": "AttributeError",
    "failure_occurs_before_candidate_or_stage_creation": True,
    "same_defect_must_be_absent_from_v7": True,
}
V9_V6_DEFECT_SHAPE_DRIFT_INCIDENT = {
    "schema":
        "cm2.round306c79g.true-global-no-producer-consumer."
        "v9-v6-held-self-defect-shape-drift-incident.v1",
    "incident_id":
        "V9_LAUNCHER_EXPANDED_V6_PERSISTED_DEFECT_PAYLOAD_16_KEYS_"
        "VERSUS_CONTRACT_CANONICAL_9_KEYS",
    "evidence_source":
        "FROZEN_V9_LAUNCHER_CONTROL_FLOW_AND_FIRST_RUNTIME_STDERR",
    "failure_label":
        "exact v6 exact10, rejection, spawned-before-write and "
        "HeldSelf.identity defect regression",
    "persisted_held_self_identity_defect_exact_key_count": 9,
    "persisted_held_self_identity_defect":
        copy.deepcopy(V6_PERSISTED_HELD_SELF_IDENTITY_DEFECT),
    "launcher_expanded_structural_evidence_exact_key_count": 16,
    "launcher_expanded_structural_evidence":
        copy.deepcopy(V6_LAUNCHER_EXPANDED_STRUCTURAL_EVIDENCE),
    "contract_v9_predecessor_v6_full_canonical_sha256":
        "827bff2782109ae7aa905b4a8f5d25ac37cd814cef34cbee531a25fad4b1abc0",
    "contract_v9_persisted_defect_nested_canonical_sha256":
        "8dce2a1ea02dc47b3158540547b97810ee3e0ad5adfc5b4849f275fc4ac0407f",
    "launcher_v9_predecessor_v6_full_canonical_sha256":
        "7f3cc1b44f157b8a7ab981d0918e0cf83cb93c49661173a104489deecd38371a",
    "launcher_v9_expanded_defect_nested_canonical_sha256":
        "d6ac736b4a8e72deef40cf5573545285440b2102e48f9bf6ea2cbcb6fe46a068",
    "whole_predecessor_v6_equality_failed_before_child_spawn": True,
    "structural_evidence_must_not_be_inserted_into_persisted_payload": True,
    "required_successor_fix":
        "PRESERVE_CANONICAL_9_KEY_PERSISTED_PAYLOAD_AND_VALIDATE_16_KEY_"
        "STRUCTURAL_EVIDENCE_SEPARATELY",
    "producer_child_spawned": False,
    "candidate_or_stage_created": False,
    "positive_runtime_surface_count": 0,
    "formal_global_closure_credit": 0,
    "D02_unlock": False,
    "D02_started": False,
}

V8_PUBLISHED_EXACT10_PINS: tuple[tuple[Path, str, str | None], ...] = (
    (V7_OFFICIAL_REJECTION,
     "63d4bbc4f50ef674b6b90f6fde625ac4705d5272f500fd495111d445274ebf6b",
     "29c43ad51082bd56c2291dea88b619731c2853969b79ea008abea1cca3c83ecd"),
    (OUT / "cm2_round306c79g_true_global_no_producer_consumer_schema_v8.json",
     "65904d48296a568d2cd4ec2fc49abe1a7651ca77d4a119a780fc91fb6ddaaeeb", None),
    (OUT / "cm2_round306c79g_true_global_no_producer_consumer_contract_v8.json",
     "6ddb6dd015ee9bb88c716cfb939bf2b954789effffa17b141833091a72187ca4",
     "0bb6634778bf50a9f090d5df7b23358cae30769ce9b2fb87119800f38a1b75c0"),
    (OUT / "cm2_round306c79g_true_global_no_producer_consumer_v8.py",
     "93a591fc870c0fa35ed37e6e2d0f9066161988d3d340031b7ffdb7239eb2c512", None),
    (OUT / ("cm2_round306c79g_true_global_no_producer_consumer_"
            "independent_verifier_assembler_authority_consumer_v8.py"),
     "d9c5c56f0ae88b573812c660a64eb94dd345d7efd0257cce975752945e1240f3", None),
    (OUT / ("cm2_round306c79g_true_global_no_producer_consumer_"
            "v7_to_v8_static_launch_transition_receipt_v1.json"),
     "92c7b1473bdced6426b0e52a4b29d181d4153fc1174ae7709469a7552bfd3524",
     "679920565b320b2bfb94f431902cac93a2af1ce506b725f0e3ea88ec1a59ae96"),
    (OUT / "cm2_round306c79g_true_global_no_producer_consumer_static_audit_v8.json",
     "b467b7eea54a0d208ff560677929e15d14304f044016e858b9a267f6c5dab8dd",
     "8138cb5c1c99cb737ae50ff61c1a56efad6ac202889719d22d12997d1e0b6bb0"),
    (OUT / "cm2_round306c79g_true_global_no_producer_consumer_cold_launch_v8.py",
     "169866df2d418c3ccb467ef2b678d322584910500cdeee9dd2b40d8564de3d1e", None),
    (OUT / ("cm2_round306c79g_true_global_no_producer_consumer_"
            "cold_launch_manifest_v8.sha256"),
     "ae6e4998d6b347902b3e1ab5256abb6f9ab62d5feabf63a597a28e881068365f", None),
    (OUT / ("cm2_round306c79g_true_global_no_producer_consumer_"
            "cold_launch_outer_receipt_v8.json"),
     "bc1f7d4c4c8cd2d5ade666ba71e920532651266a9e733b361dfa979b7a0e446f",
     "35c63aebeb08cf93339f01d3cc05c9552cbf0bffa50010ce60d4350990f3181d"),
)
V8_PUBLISHED_EXACT10_NAMES = (
    "v7_official_rejection", "closed_schema", "contract",
    "build_only_producer", "independent_consumer", "v7_to_v8_transition",
    "static_audit", "cold_launcher", "cold_manifest", "cold_outer",
)
V8_FIRST_ROLLOUT_ATTEMPT = {
    "attempted": True,
    "producer_child_spawned": False,
    "candidate_write_started": False,
    "positive_runtime_surface_count": 0,
    "aborted_by_regression_guard": True,
}
V8_ROLLOUT_CONTROL_FLOW_INCIDENT = {
    "schema":
        "cm2.round306c79g.true-global-no-producer-consumer."
        "v8-rollout-control-flow-incident.v1",
    "incident_id":
        "V8_LAUNCHER_REGRESSOR_WHOLE_FUNCTION_OCCURRENCE_COUNT_FALSE_POSITIVE",
    "evidence_source": "TRUSTED_ROLLOUT_CONTROL_FLOW_RECORD",
    "incident_fact_comes_from_rollout_control_flow_record_not_from_timestamps":
        True,
    "timestamps_are_not_used_to_infer_control_flow": True,
    "timestamp_chronology_is_corrobative_only": True,
    "regressor_scope": "WHOLE_FUNCTION_SOURCE_OCCURRENCE_CENSUS",
    "regressor_expected_occurrence_count": 1,
    "regressor_observed_occurrence_count": 3,
    "observed_source_lines": [2041, 2062, 2235],
    "actual_semantic_trigger_line": 2041,
    "nontrigger_occurrence_lines": [2062, 2235],
    "actual_semantic_trigger_count": 1,
    "failure_kind": "FALSE_POSITIVE_REGRESSION_GUARD_ABORT",
    "required_successor_fix":
        "AST_SEMANTIC_TRIGGER_CHECK_MUST_SELECT_LINE_2041_AND_MUST_NOT_REQUIRE_"
        "WHOLE_FUNCTION_TEXT_OCCURRENCE_COUNT_ONE",
    "v8_execution_allowed": False,
    "v8_runtime_surfaces_authoritative": False,
    "positive_runtime_surface_count": 0,
    "formal_global_closure_credit": 0,
    "D02_unlock": False,
    "D02_started": False,
}
V8_LAUNCHER_REGRESSION_DEFECT_SHA256 = (
    "e7fc06d045990de049be7f973ab1eec99c1f1c0af0b694d9f349b4e633525b95")

V7_PUBLISHED_EXACT10_PINS: tuple[tuple[Path, str, str | None], ...] = (
    (V6_OFFICIAL_REJECTION,
     "3559dcfd9e6d0ebb0e093226d6d3ae8d09d67eaeb186d4ec956241af87fcbd06",
     "87c0cd17ae6ca3885a01da82b47b66e96419eb778594b51423eb04cf3c68f48c"),
    (OUT / "cm2_round306c79g_true_global_no_producer_consumer_schema_v7.json",
     "edcdbb568044d04fc7c86b4c4e64fdb7b12b3841f1e93092694ebc3177b6fe18", None),
    (OUT / "cm2_round306c79g_true_global_no_producer_consumer_contract_v7.json",
     "041ca2567f81c148f765dd85e3515a6ac01295bca06c3032b027459eceb2c014",
     "a87f7434b32a96923ee81f7761efab9b0937f15103c2fa9b47e8402104b612a5"),
    (OUT / "cm2_round306c79g_true_global_no_producer_consumer_v7.py",
     "67670681481cf372f775ad39a9f8d8b2459a77ef708e2f4da14ca114ac0f0d95", None),
    (OUT / ("cm2_round306c79g_true_global_no_producer_consumer_"
            "independent_verifier_assembler_authority_consumer_v7.py"),
     "3ee9f2c666b7297a23faa31d39d5ea66b708d545120b1aeb93f77ac9ef704f8a", None),
    (OUT / ("cm2_round306c79g_true_global_no_producer_consumer_"
            "v6_to_v7_static_launch_transition_receipt_v1.json"),
     "e732442e16a3a1f66629562af4cae72d9ae3e78b511f67ee22aa84869b90bec8",
     "0f1f240b6a61a6774991b8355c6132c1a9ae30b15690e8c058f88206db69453e"),
    (OUT / "cm2_round306c79g_true_global_no_producer_consumer_static_audit_v7.json",
     "74c72540bd66b5929fa30ec554207db21f40999484752340f0294590d407a667",
     "efd83fae1a716c864e8bb61238370e10b9ebf54444f023b902c7cef2a41a6766"),
    (OUT / "cm2_round306c79g_true_global_no_producer_consumer_cold_launch_v7.py",
     "93404ad229728b682018ad236075b6c789e12ee4bf043426049e2aa501b2b9e0", None),
    (OUT / ("cm2_round306c79g_true_global_no_producer_consumer_"
            "cold_launch_manifest_v7.sha256"),
     "eeabe5d52504231a6163b0e057e9129b632b8a4c33a18fc3a3ac4576612de80c", None),
    (OUT / ("cm2_round306c79g_true_global_no_producer_consumer_"
            "cold_launch_outer_receipt_v7.json"),
     "0a1fc6afe12db5c630b0c73e1fb8280140adb1590c93f176c564e4e24637584e",
     "8214fa50020fed7ea4046d607b1631723f660d18b3f8a2f8653f7444b02a1795"),
)
V7_PUBLISHED_EXACT10_NAMES = (
    "v6_official_rejection", "closed_schema", "contract",
    "build_only_producer", "independent_consumer", "v6_to_v7_transition",
    "static_audit", "cold_launcher", "cold_manifest", "cold_outer",
)
V7_LOCK_CONTINUITY_INCIDENT_OBJECT_PIN = (
    "15f92090e77eda4c6acac0af759541fe47dc4f8358e15659077d6dea8071e764")
V7_LOCK_CONTINUITY_INCIDENT: dict[str, Any] = {
    "D02_started": False,
    "D02_unlock": False,
    "effective_checkpoint_object_sha256": UPSTREAM_CHECKPOINT_OBJECT_PIN,
    "exact10_bytes_alone_do_not_prove_publication_acceptance": True,
    "failure_trigger":
        "LOCAL_READ_ONLY_HISTORY_REPLAY_RETURNED_NONZERO_UNDER_SET_E_LOCK_HOLDER",
    "false_extra_assumption":
        "HISTORICAL_V4_PRETTY_JSON_REQUIRED_CANONICAL_SINGLE_LINE",
    "in_lock_terminal_replay_attempt_started": True,
    "incident_fact_comes_from_publisher_control_flow_record_not_from_timestamps_alone":
        True,
    "incident_id":
        "V7_OFFICIAL_LOCK_RELEASED_AFTER_OUTER_BEFORE_REQUIRED_IN_LOCK_TERMINAL_REPLAY_COMPLETION",
    "later_read_only_replay_cannot_rehabilitate_v7": True,
    "object_sha256": V7_LOCK_CONTINUITY_INCIDENT_OBJECT_PIN,
    "official_rejection_file_sha256": V7_OFFICIAL_REJECTION_FILE_PIN,
    "official_rejection_object_sha256": V7_OFFICIAL_REJECTION_OBJECT_PIN,
    "outer_frozen_and_fsynced": True,
    "outer_then_rejection_chronology_validated": True,
    "positive_runtime_surface_count": 0,
    "postincident_byte_replay_passed_but_did_not_restore_lock_continuity": True,
    "publication_lock_continuity_interrupted_after_outer_before_required_replay_completion":
        True,
    "publication_lock_released_on_replay_attempt_failure": True,
    "published_exact10_count": 10,
    "published_outer_file_sha256": V7_PUBLISHED_EXACT10_PINS[9][1],
    "published_outer_object_sha256": V7_PUBLISHED_EXACT10_PINS[9][2],
    "required_in_lock_terminal_replay_completed": False,
    "schema":
        "cm2.round306c79g.true-global-no-producer-consumer."
        "v7-publication-lock-continuity-incident.v1",
    "v7_formal_credit_transferred": False,
    "v7_runtime_command_count": 0,
}

V6_PUBLISHED_EXACT10_PINS: tuple[tuple[Path, str, str | None], ...] = (
    (V5_OFFICIAL_REJECTION,
     "c49218967b2d5023d07e5c65fa53df12f0383d6644bf4bd7d35a8e50abeb85b5",
     "9a94bf8b580f6145c4977dd335d9a63c69057d18d62678ab47c7916c764f8e4c"),
    (OUT / "cm2_round306c79g_true_global_no_producer_consumer_schema_v6.json",
     "250e27777e3ffdaf159a19c00ae683a4ef079f6e785f0b37d003a724099419bc", None),
    (OUT / "cm2_round306c79g_true_global_no_producer_consumer_contract_v6.json",
     "6e4f7f4693b759397c8775f8d943048c867b3c460c27f5cb3d9681a0fefee30c",
     "58ae6e3c9912294cc89b6804741e56b373a143d16a5fa2547325989fa1af2546"),
    (OUT / "cm2_round306c79g_true_global_no_producer_consumer_v6.py",
     "f48982effd6a1068c50260d0d419b281a3fa8c614e4ca76c3b8ee2a48e8afb56", None),
    (OUT / ("cm2_round306c79g_true_global_no_producer_consumer_"
            "independent_verifier_assembler_authority_consumer_v6.py"),
     "af4875d2ab84101b05eff9811f33d8bf7b1a060720a956ae3fb42d8d466f4775", None),
    (OUT / ("cm2_round306c79g_true_global_no_producer_consumer_"
            "v5_to_v6_static_launch_transition_receipt_v1.json"),
     "a6ac971e7efd9a6a80c7055449fb6c4ef02b77d3e8303324104a060618d45569",
     "edb97beae5ca5cfeff9e549c017892d6381d3b5a01be16b12e7e52e06d09c5e1"),
    (OUT / "cm2_round306c79g_true_global_no_producer_consumer_static_audit_v6.json",
     "f4f5b3ea2c289f388da9cc7d4181c0f1d6cf692aae0b85cbb17533ca4131f474",
     "2478b44d085336b87d13e309dc4416e58a85ef6ae28eb89cd787ea95b07c0449"),
    (OUT / "cm2_round306c79g_true_global_no_producer_consumer_cold_launch_v6.py",
     "796cbb3c0a4a2a5f3801f9a9132421112fc19e81272938092edd3014ef031fcb", None),
    (OUT / ("cm2_round306c79g_true_global_no_producer_consumer_"
            "cold_launch_manifest_v6.sha256"),
     "281232171e4c2713f81122e731bd4d50e95afef6bdbd2a5040f5e93c3b7171ea", None),
    (OUT / ("cm2_round306c79g_true_global_no_producer_consumer_"
            "cold_launch_outer_receipt_v6.json"),
     "e37cce305826fb2149798a125a12b3880070fca5f338b6508beeea947c2854bd",
     "423621bbe2115183a54dc0161abdbdc964f09af31efb39eee40f46bc81bbe251"),
)
V6_PUBLISHED_EXACT10_NAMES = (
    "v5_official_rejection", "closed_schema", "contract",
    "build_only_producer", "independent_consumer", "v5_to_v6_transition",
    "static_audit", "cold_launcher", "cold_manifest", "cold_outer",
)

V3_PUBLISHED_EXACT10_PINS: tuple[tuple[Path, str, str | None], ...] = (
    (OUT / ("cm2_round306c79g_true_global_no_producer_consumer_"
            "v2_rejection_supersession_receipt_v1.json"),
     "fdd1921afda98a34c87ae20094e60fca1b75c8f233cf37890e7817fe35d82408",
     "518cbc5b30fc62d55291feef407c5677b880a05cb9a5b9f51404c79381c648fa"),
    (OUT / "cm2_round306c79g_true_global_no_producer_consumer_schema_v3.json",
     "275a86286480f915af69e18d81d7032140e3db6982d32679206a6a5b88fee036", None),
    (OUT / "cm2_round306c79g_true_global_no_producer_consumer_contract_v3.json",
     "ee2a969b5d3ae28dfc116fc24ab6bee6c3983d64db183641981108481c05ae7d",
     "fe82dcf80e8dd856390b694e8a286abc3087f33d0a2b4bebda1a01836b796a6b"),
    (OUT / "cm2_round306c79g_true_global_no_producer_consumer_v3.py",
     "587933a52505488fd87b1c4f99d5659df6f3c3e9557c0a77edd642e6e4dde0ab", None),
    (OUT / ("cm2_round306c79g_true_global_no_producer_consumer_"
            "independent_verifier_assembler_authority_consumer_v3.py"),
     "d66143d32f4c4257041f03e24e4a4da8f15542853b2a8f47fa39f5b72871bfdd", None),
    (OUT / ("cm2_round306c79g_true_global_no_producer_consumer_"
            "v2_to_v3_static_launch_transition_receipt_v1.json"),
     "d2c0a78db1ae19ccb21f068c4c4f9337220cabbf16721fdc15ed41825a6f3374",
     "fabe51379dc16bd4177d2116a43f2d1d5c103cc5a53f845fd5397eae0ea1c25b"),
    (OUT / "cm2_round306c79g_true_global_no_producer_consumer_static_audit_v3.json",
     "b7c3732296df713b6588527284983fab758e225c17c51fbc4a38b1f43da8aece",
     "2ef7588e66a83944fee0e2044177445f15b71fe030871ca96f354ce65dc8499a"),
    (OUT / "cm2_round306c79g_true_global_no_producer_consumer_cold_launch_v3.py",
     "63e1b04ce152770ce4bcfda826d418414fd3196ba540752d0bd61a97eec0075b", None),
    (OUT / ("cm2_round306c79g_true_global_no_producer_consumer_"
            "cold_launch_manifest_v3.sha256"),
     "53c97fc8f01f0dc0de3f7c5729d5940587467a1877ef9a7c96e9ea2403c0b028", None),
    (OUT / ("cm2_round306c79g_true_global_no_producer_consumer_"
            "cold_launch_outer_receipt_v3.json"),
     "692608ca777ca9ee625e2044bc71f694edf893f51953d7ff5662f29264d245ea",
     "450e1551a9f3cac2529bd202aa63ad28e4fd7e2ec4c7d7fb415883840ca0143d"),
)
V3_PUBLISHED_EXACT10_NAMES = (
    "v2_rejection_supersession", "closed_schema", "contract", "producer",
    "consumer", "transition", "static_audit", "cold_launcher",
    "cold_manifest", "cold_outer",
)

# The v4 provisional exact8 begins with V3_OFFICIAL_REJECTION.  That linked
# file is held exactly once below; these seven pins are the remaining distinct
# v4 draft files, so the historical identity census cannot double-count it.
V4_DRAFT7_PINS: tuple[tuple[Path, str, str | None], ...] = (
    (OUT / "cm2_round306c79g_true_global_no_producer_consumer_schema_v4.json",
     "b2cb58e88b66daed7d0449d11a4441095179b7e537a48a35ee9c630f76beca6a", None),
    (OUT / "cm2_round306c79g_true_global_no_producer_consumer_contract_v4.json",
     "84608ada466fb9aa3d99adfd34662e9af02dfd009d8eb185374c065a6da0c23c",
     "62609ff0809ba9439be07a215ece772262f30ead7d87fda92a6e4e23bb5895b7"),
    (OUT / "cm2_round306c79g_true_global_no_producer_consumer_v4.py",
     "968e401852f45d5104f48526b50d4f59a86bb1fed8e7af23782c5f6d447d1cf1", None),
    (OUT / ("cm2_round306c79g_true_global_no_producer_consumer_"
            "independent_verifier_assembler_authority_consumer_v4.py"),
     "23753584725365cdc0174d518c26b7d8dbdeb12eea2345a5e3b281274548420c", None),
    (OUT / ("cm2_round306c79g_true_global_no_producer_consumer_"
            "v3_to_v4_static_launch_transition_receipt_v1.json"),
     "4c46f7cf8eaba93fd1b9562c288c2117b49d7c8cdeb62482b93c5e247d412256",
     "d2d0797a6edb8463f9af7007e28356932472f2e0478fb73b35869d3f51184129"),
    (OUT / "cm2_round306c79g_true_global_no_producer_consumer_static_audit_v4.json",
     "5efa44ae5cf78000940a4640a98ac0fe486e1946aecc9d20e7023e27ed13049c",
     "489a0aad575872e79dc264d5fc45cf2f12903c4c990f25d15a9cdd1448e980f4"),
    (OUT / "cm2_round306c79g_true_global_no_producer_consumer_cold_launch_v4.py",
     "04617c7ac60ad4cee278ac1b4c7d154fd130a3e2225a691ef9a75ad644a062a3", None),
)

V5_PUBLISHED_EXACT10_PINS: tuple[tuple[Path, str, str | None], ...] = (
    (V4_REJECTION_SUPERSESSION,
     "e3dff621fec2fa5bac14f73685c8f44ce89bc68d80b6478e0688ce926f57c183",
     "1c8fc9d91be75502b0741b096a1ca6d9d59b877b1e69daada15096669215d19f"),
    (OUT / "cm2_round306c79g_true_global_no_producer_consumer_schema_v5.json",
     "1048740103257351abb1266ed91bb80028436cb1497918a0f0f177ec3268ff4f", None),
    (OUT / "cm2_round306c79g_true_global_no_producer_consumer_contract_v5.json",
     "162cd554ea972b434c019924a9ab8b87621ab65aae7d4896b6dac72d6288b997",
     "27d457a583f4d9892e0a866917ea4add25ff677669ee814861e0608036189377"),
    (OUT / "cm2_round306c79g_true_global_no_producer_consumer_v5.py",
     "bc6d48903f61257cd75b20b83c6cd369ca3748d19427cf18129c0fb9bb59e76e", None),
    (OUT / ("cm2_round306c79g_true_global_no_producer_consumer_"
            "independent_verifier_assembler_authority_consumer_v5.py"),
     "03aed000a94fc7b7d7e68d3c55611bcc55e7ce293f65ddfb3be7709e44fc854d", None),
    (OUT / ("cm2_round306c79g_true_global_no_producer_consumer_"
            "v4_to_v5_static_launch_transition_receipt_v1.json"),
     "6784668e91a4a4cc0812c6405cb1df8c10ad90e40daf321ac75c16cadd5cd715",
     "0678e3b81d5a4f6088967613df0cd585910b9b26800dfbf1724b637fc7c43526"),
    (OUT / "cm2_round306c79g_true_global_no_producer_consumer_static_audit_v5.json",
     "b852a41aaa992b85abec5f7139dc4669d2f1fe38bd79ab8ab812453c5cfca4f0",
     "ba9bf728ce08b795b5dd92191f2ccac3b2cfbc6ef7f7b919379feb6b9557e546"),
    (OUT / "cm2_round306c79g_true_global_no_producer_consumer_cold_launch_v5.py",
     "889775cfbe1d3cba597c85c28765545805710c99f06ad05673e57b7b7627bc54", None),
    (OUT / ("cm2_round306c79g_true_global_no_producer_consumer_"
            "cold_launch_manifest_v5.sha256"),
     "55336d5a95e1765cc0f229bbc98ddfb1f6c14218f5b5e619f84d19da39961474", None),
    (OUT / ("cm2_round306c79g_true_global_no_producer_consumer_"
            "cold_launch_outer_receipt_v5.json"),
     "71b7eaca4af58a34b70bb751044bd09d0e40352a1dc6f016a0c7618b6d4b4ab8",
     "57d5c31bf232d725e661932d2d210b31d1125cd0877a74a8167451bbbdaf0e1c"),
)
V5_PUBLISHED_EXACT10_NAMES = (
    "v4_rejection_supersession", "closed_schema", "contract",
    "build_only_producer", "independent_consumer", "v4_to_v5_transition",
    "static_audit", "cold_launcher", "cold_manifest", "cold_outer",
)

V5_POSITIVE_RUNTIME_SURFACES = tuple(ROOT / value for value in (
    ".cm2-runtime/c79g-v5-candidate-a-" + UPSTREAM_CHECKPOINT_OBJECT_PIN,
    ".cm2-runtime/c79g-v5-candidate-b-" + UPSTREAM_CHECKPOINT_OBJECT_PIN,
    ".cm2-runtime/c79g-v5-verification-a-" + UPSTREAM_CHECKPOINT_OBJECT_PIN,
    ".cm2-runtime/c79g-v5-verification-b-" + UPSTREAM_CHECKPOINT_OBJECT_PIN,
    ".cm2-runtime/c79g-v5-committed-completion-" + UPSTREAM_CHECKPOINT_OBJECT_PIN,
    ".cm2-runtime/cm2-global-authority-heads/c79g-v5-" +
        UPSTREAM_CHECKPOINT_OBJECT_PIN + ".seal",
))
V5_DETERMINISTIC_STAGE_SURFACES = tuple(ROOT / value for value in (
    ".cm2-runtime/.c79g-v5-candidate-stage-a-" + UPSTREAM_CHECKPOINT_OBJECT_PIN,
    ".cm2-runtime/.c79g-v5-candidate-stage-b-" + UPSTREAM_CHECKPOINT_OBJECT_PIN,
    ".cm2-runtime/.c79g-v5-verification-stage-a-" + UPSTREAM_CHECKPOINT_OBJECT_PIN,
    ".cm2-runtime/.c79g-v5-verification-stage-b-" + UPSTREAM_CHECKPOINT_OBJECT_PIN,
    ".cm2-runtime/.c79g-v5-completion-stage-" + UPSTREAM_CHECKPOINT_OBJECT_PIN,
    ".cm2-runtime/cm2-global-authority-heads/.c79g-v5-authority-stage-" +
        UPSTREAM_CHECKPOINT_OBJECT_PIN + ".seal",
))
V5_ALL_POSITIVE_AND_STAGE_SURFACES = (
    V5_POSITIVE_RUNTIME_SURFACES + V5_DETERMINISTIC_STAGE_SURFACES)

V6_POSITIVE_RUNTIME_SURFACES = tuple(ROOT / value for value in (
    ".cm2-runtime/c79g-v6-candidate-a-" + UPSTREAM_CHECKPOINT_OBJECT_PIN,
    ".cm2-runtime/c79g-v6-candidate-b-" + UPSTREAM_CHECKPOINT_OBJECT_PIN,
    ".cm2-runtime/c79g-v6-verification-a-" + UPSTREAM_CHECKPOINT_OBJECT_PIN,
    ".cm2-runtime/c79g-v6-verification-b-" + UPSTREAM_CHECKPOINT_OBJECT_PIN,
    ".cm2-runtime/c79g-v6-committed-completion-" + UPSTREAM_CHECKPOINT_OBJECT_PIN,
    ".cm2-runtime/cm2-global-authority-heads/c79g-v6-" +
        UPSTREAM_CHECKPOINT_OBJECT_PIN + ".seal",
))
V6_DETERMINISTIC_STAGE_SURFACES = tuple(ROOT / value for value in (
    ".cm2-runtime/.c79g-v6-candidate-stage-a-" + UPSTREAM_CHECKPOINT_OBJECT_PIN,
    ".cm2-runtime/.c79g-v6-candidate-stage-b-" + UPSTREAM_CHECKPOINT_OBJECT_PIN,
    ".cm2-runtime/.c79g-v6-verification-stage-a-" + UPSTREAM_CHECKPOINT_OBJECT_PIN,
    ".cm2-runtime/.c79g-v6-verification-stage-b-" + UPSTREAM_CHECKPOINT_OBJECT_PIN,
    ".cm2-runtime/.c79g-v6-completion-stage-" + UPSTREAM_CHECKPOINT_OBJECT_PIN,
    ".cm2-runtime/cm2-global-authority-heads/.c79g-v6-authority-stage-" +
        UPSTREAM_CHECKPOINT_OBJECT_PIN + ".seal",
))
V6_ALL_POSITIVE_AND_STAGE_SURFACES = (
    V6_POSITIVE_RUNTIME_SURFACES + V6_DETERMINISTIC_STAGE_SURFACES)

V7_POSITIVE_RUNTIME_SURFACES = tuple(ROOT / value for value in (
    ".cm2-runtime/c79g-v7-candidate-a-" + UPSTREAM_CHECKPOINT_OBJECT_PIN,
    ".cm2-runtime/c79g-v7-candidate-b-" + UPSTREAM_CHECKPOINT_OBJECT_PIN,
    ".cm2-runtime/c79g-v7-verification-a-" + UPSTREAM_CHECKPOINT_OBJECT_PIN,
    ".cm2-runtime/c79g-v7-verification-b-" + UPSTREAM_CHECKPOINT_OBJECT_PIN,
    ".cm2-runtime/c79g-v7-committed-completion-" + UPSTREAM_CHECKPOINT_OBJECT_PIN,
    ".cm2-runtime/cm2-global-authority-heads/c79g-v7-" +
        UPSTREAM_CHECKPOINT_OBJECT_PIN + ".seal",
))
V7_DETERMINISTIC_STAGE_SURFACES = tuple(ROOT / value for value in (
    ".cm2-runtime/.c79g-v7-candidate-stage-a-" + UPSTREAM_CHECKPOINT_OBJECT_PIN,
    ".cm2-runtime/.c79g-v7-candidate-stage-b-" + UPSTREAM_CHECKPOINT_OBJECT_PIN,
    ".cm2-runtime/.c79g-v7-verification-stage-a-" + UPSTREAM_CHECKPOINT_OBJECT_PIN,
    ".cm2-runtime/.c79g-v7-verification-stage-b-" + UPSTREAM_CHECKPOINT_OBJECT_PIN,
    ".cm2-runtime/.c79g-v7-completion-stage-" + UPSTREAM_CHECKPOINT_OBJECT_PIN,
    ".cm2-runtime/cm2-global-authority-heads/.c79g-v7-authority-stage-" +
        UPSTREAM_CHECKPOINT_OBJECT_PIN + ".seal",
))
V7_ALL_POSITIVE_AND_STAGE_SURFACES = (
    V7_POSITIVE_RUNTIME_SURFACES + V7_DETERMINISTIC_STAGE_SURFACES)

V8_POSITIVE_RUNTIME_SURFACES = tuple(ROOT / value for value in (
    ".cm2-runtime/c79g-v8-candidate-a-" + UPSTREAM_CHECKPOINT_OBJECT_PIN,
    ".cm2-runtime/c79g-v8-candidate-b-" + UPSTREAM_CHECKPOINT_OBJECT_PIN,
    ".cm2-runtime/c79g-v8-verification-a-" + UPSTREAM_CHECKPOINT_OBJECT_PIN,
    ".cm2-runtime/c79g-v8-verification-b-" + UPSTREAM_CHECKPOINT_OBJECT_PIN,
    ".cm2-runtime/c79g-v8-committed-completion-" + UPSTREAM_CHECKPOINT_OBJECT_PIN,
    ".cm2-runtime/cm2-global-authority-heads/c79g-v8-" +
        UPSTREAM_CHECKPOINT_OBJECT_PIN + ".seal",
))
V8_DETERMINISTIC_STAGE_SURFACES = tuple(ROOT / value for value in (
    ".cm2-runtime/.c79g-v8-candidate-stage-a-" + UPSTREAM_CHECKPOINT_OBJECT_PIN,
    ".cm2-runtime/.c79g-v8-candidate-stage-b-" + UPSTREAM_CHECKPOINT_OBJECT_PIN,
    ".cm2-runtime/.c79g-v8-verification-stage-a-" + UPSTREAM_CHECKPOINT_OBJECT_PIN,
    ".cm2-runtime/.c79g-v8-verification-stage-b-" + UPSTREAM_CHECKPOINT_OBJECT_PIN,
    ".cm2-runtime/.c79g-v8-completion-stage-" + UPSTREAM_CHECKPOINT_OBJECT_PIN,
    ".cm2-runtime/cm2-global-authority-heads/.c79g-v8-authority-stage-" +
        UPSTREAM_CHECKPOINT_OBJECT_PIN + ".seal",
))
V8_ALL_POSITIVE_AND_STAGE_SURFACES = (
    V8_POSITIVE_RUNTIME_SURFACES + V8_DETERMINISTIC_STAGE_SURFACES)

V9_POSITIVE_RUNTIME_SURFACES = tuple(ROOT / value for value in (
    ".cm2-runtime/c79g-v9-candidate-a-" + UPSTREAM_CHECKPOINT_OBJECT_PIN,
    ".cm2-runtime/c79g-v9-candidate-b-" + UPSTREAM_CHECKPOINT_OBJECT_PIN,
    ".cm2-runtime/c79g-v9-verification-a-" + UPSTREAM_CHECKPOINT_OBJECT_PIN,
    ".cm2-runtime/c79g-v9-verification-b-" + UPSTREAM_CHECKPOINT_OBJECT_PIN,
    ".cm2-runtime/c79g-v9-committed-completion-" + UPSTREAM_CHECKPOINT_OBJECT_PIN,
    ".cm2-runtime/cm2-global-authority-heads/c79g-v9-" +
        UPSTREAM_CHECKPOINT_OBJECT_PIN + ".seal",
))
V9_DETERMINISTIC_STAGE_SURFACES = tuple(ROOT / value for value in (
    ".cm2-runtime/.c79g-v9-candidate-stage-a-" + UPSTREAM_CHECKPOINT_OBJECT_PIN,
    ".cm2-runtime/.c79g-v9-candidate-stage-b-" + UPSTREAM_CHECKPOINT_OBJECT_PIN,
    ".cm2-runtime/.c79g-v9-verification-stage-a-" + UPSTREAM_CHECKPOINT_OBJECT_PIN,
    ".cm2-runtime/.c79g-v9-verification-stage-b-" + UPSTREAM_CHECKPOINT_OBJECT_PIN,
    ".cm2-runtime/.c79g-v9-completion-stage-" + UPSTREAM_CHECKPOINT_OBJECT_PIN,
    ".cm2-runtime/cm2-global-authority-heads/.c79g-v9-authority-stage-" +
        UPSTREAM_CHECKPOINT_OBJECT_PIN + ".seal",
))
V9_ALL_POSITIVE_AND_STAGE_SURFACES = (
    V9_POSITIVE_RUNTIME_SURFACES + V9_DETERMINISTIC_STAGE_SURFACES)

V10_POSITIVE_RUNTIME_SURFACES = tuple(ROOT / value for value in (
    ".cm2-runtime/c79g-v10-candidate-a-" + UPSTREAM_CHECKPOINT_OBJECT_PIN,
    ".cm2-runtime/c79g-v10-candidate-b-" + UPSTREAM_CHECKPOINT_OBJECT_PIN,
    ".cm2-runtime/c79g-v10-verification-a-" + UPSTREAM_CHECKPOINT_OBJECT_PIN,
    ".cm2-runtime/c79g-v10-verification-b-" + UPSTREAM_CHECKPOINT_OBJECT_PIN,
    ".cm2-runtime/c79g-v10-committed-completion-" + UPSTREAM_CHECKPOINT_OBJECT_PIN,
    ".cm2-runtime/cm2-global-authority-heads/c79g-v10-" +
        UPSTREAM_CHECKPOINT_OBJECT_PIN + ".seal",
))
V10_DETERMINISTIC_STAGE_SURFACES = tuple(ROOT / value for value in (
    ".cm2-runtime/.c79g-v10-candidate-stage-a-" + UPSTREAM_CHECKPOINT_OBJECT_PIN,
    ".cm2-runtime/.c79g-v10-candidate-stage-b-" + UPSTREAM_CHECKPOINT_OBJECT_PIN,
    ".cm2-runtime/.c79g-v10-verification-stage-a-" + UPSTREAM_CHECKPOINT_OBJECT_PIN,
    ".cm2-runtime/.c79g-v10-verification-stage-b-" + UPSTREAM_CHECKPOINT_OBJECT_PIN,
    ".cm2-runtime/.c79g-v10-completion-stage-" + UPSTREAM_CHECKPOINT_OBJECT_PIN,
    ".cm2-runtime/cm2-global-authority-heads/.c79g-v10-authority-stage-" +
        UPSTREAM_CHECKPOINT_OBJECT_PIN + ".seal",
))
V10_ALL_POSITIVE_AND_STAGE_SURFACES = (
    V10_POSITIVE_RUNTIME_SURFACES + V10_DETERMINISTIC_STAGE_SURFACES)

V11_POSITIVE_RUNTIME_SURFACES = tuple(ROOT / value for value in (
    ".cm2-runtime/c79g-v11-candidate-a-" + UPSTREAM_CHECKPOINT_OBJECT_PIN,
    ".cm2-runtime/c79g-v11-candidate-b-" + UPSTREAM_CHECKPOINT_OBJECT_PIN,
    ".cm2-runtime/c79g-v11-verification-a-" + UPSTREAM_CHECKPOINT_OBJECT_PIN,
    ".cm2-runtime/c79g-v11-verification-b-" + UPSTREAM_CHECKPOINT_OBJECT_PIN,
    ".cm2-runtime/c79g-v11-committed-completion-" + UPSTREAM_CHECKPOINT_OBJECT_PIN,
    ".cm2-runtime/cm2-global-authority-heads/c79g-v11-" +
        UPSTREAM_CHECKPOINT_OBJECT_PIN + ".seal",
))
V11_DETERMINISTIC_STAGE_SURFACES = tuple(ROOT / value for value in (
    ".cm2-runtime/.c79g-v11-candidate-stage-a-" + UPSTREAM_CHECKPOINT_OBJECT_PIN,
    ".cm2-runtime/.c79g-v11-candidate-stage-b-" + UPSTREAM_CHECKPOINT_OBJECT_PIN,
    ".cm2-runtime/.c79g-v11-verification-stage-a-" + UPSTREAM_CHECKPOINT_OBJECT_PIN,
    ".cm2-runtime/.c79g-v11-verification-stage-b-" + UPSTREAM_CHECKPOINT_OBJECT_PIN,
    ".cm2-runtime/.c79g-v11-completion-stage-" + UPSTREAM_CHECKPOINT_OBJECT_PIN,
    ".cm2-runtime/cm2-global-authority-heads/.c79g-v11-authority-stage-" +
        UPSTREAM_CHECKPOINT_OBJECT_PIN + ".seal",
))
V11_ALL_POSITIVE_AND_STAGE_SURFACES = (
    V11_POSITIVE_RUNTIME_SURFACES + V11_DETERMINISTIC_STAGE_SURFACES)
V12_POSITIVE_RUNTIME_SURFACES = tuple(ROOT / value for value in (
    ".cm2-runtime/c79g-v12-candidate-a-" + UPSTREAM_CHECKPOINT_OBJECT_PIN,
    ".cm2-runtime/c79g-v12-candidate-b-" + UPSTREAM_CHECKPOINT_OBJECT_PIN,
    ".cm2-runtime/c79g-v12-verification-a-" + UPSTREAM_CHECKPOINT_OBJECT_PIN,
    ".cm2-runtime/c79g-v12-verification-b-" + UPSTREAM_CHECKPOINT_OBJECT_PIN,
    ".cm2-runtime/c79g-v12-committed-completion-" + UPSTREAM_CHECKPOINT_OBJECT_PIN,
    ".cm2-runtime/cm2-global-authority-heads/c79g-v12-" +
        UPSTREAM_CHECKPOINT_OBJECT_PIN + ".seal",
))
V12_DETERMINISTIC_STAGE_SURFACES = tuple(ROOT / value for value in (
    ".cm2-runtime/.c79g-v12-candidate-stage-a-" + UPSTREAM_CHECKPOINT_OBJECT_PIN,
    ".cm2-runtime/.c79g-v12-candidate-stage-b-" + UPSTREAM_CHECKPOINT_OBJECT_PIN,
    ".cm2-runtime/.c79g-v12-verification-stage-a-" + UPSTREAM_CHECKPOINT_OBJECT_PIN,
    ".cm2-runtime/.c79g-v12-verification-stage-b-" + UPSTREAM_CHECKPOINT_OBJECT_PIN,
    ".cm2-runtime/.c79g-v12-completion-stage-" + UPSTREAM_CHECKPOINT_OBJECT_PIN,
    ".cm2-runtime/cm2-global-authority-heads/.c79g-v12-authority-stage-" +
        UPSTREAM_CHECKPOINT_OBJECT_PIN + ".seal",
))
V12_ALL_POSITIVE_AND_STAGE_SURFACES = (
    V12_POSITIVE_RUNTIME_SURFACES + V12_DETERMINISTIC_STAGE_SURFACES)

V5_STRICT_BOOL_RISK_IDS = (
    "V5_LAUNCHER_SCHEMA_DEFS_NAME_NON_BOOL",
    "V5_LAUNCHER_SCHEMA_PROPERTY_NAME_NON_BOOL",
    "V5_CONSUMER_ATTACK_PATCH_NON_BOOL",
    "V5_PRODUCER_RELATIVE_PARTS_NON_BOOL_SHORT_CIRCUIT",
    "V5_CONSUMER_RELATIVE_PARTS_NON_BOOL_SHORT_CIRCUIT",
    "V5_LAUNCHER_RELATIVE_PARTS_NON_BOOL_SHORT_CIRCUIT",
    "V5_LAUNCHER_RELATIVE_BYTES_NON_BOOL_SHORT_CIRCUIT",
)
V5_HARD_STRICT_BOOL_DEFECT_IDS = V5_STRICT_BOOL_RISK_IDS[:3]
V5_DIRECT_NEED_CALL_COUNT = 700
V5_COMMON_PREDECESSOR_CANONICAL_SHA256 = (
    "58d14f03c5021803533d316f4aa405482314a0f809951d9e71068fdeab1aa295")
V5_STRICT_BOOL_RISK_SPECS = (
    (V5_STRICT_BOOL_RISK_IDS[0], "launcher_v5", 1677,
     "isinstance(name, str) and name"),
    (V5_STRICT_BOOL_RISK_IDS[1], "launcher_v5", 1682,
     "isinstance(name, str) and name"),
    (V5_STRICT_BOOL_RISK_IDS[2], "consumer_v5", 3740,
     "isinstance(patch, dict) and patch"),
    (V5_STRICT_BOOL_RISK_IDS[3], "producer_v5", 510,
     "relative.parts and all((part not in {'', '.', '..'} for part in relative.parts))"),
    (V5_STRICT_BOOL_RISK_IDS[4], "consumer_v5", 894,
     "relative.parts and all((part not in {'', '.', '..'} for part in relative.parts))"),
    (V5_STRICT_BOOL_RISK_IDS[5], "launcher_v5", 317,
     "relative.parts and all((part not in {'', '.', '..'} for part in relative.parts))"),
    (V5_STRICT_BOOL_RISK_IDS[6], "launcher_v5", 324,
     "relative and (not relative.startswith(b'/')) and "
     "(b'\\x00' not in relative) and (b'..' not in relative.split(b'/'))"),
)

_STRICT_BOOL_CALL_NAMES = frozenset({
    "isinstance", "issubclass", "hasattr", "callable", "bool", "all", "any",
})
_STRICT_BOOL_METHOD_NAMES = frozenset({
    "startswith", "endswith", "isalnum", "isalpha", "isascii", "isdecimal",
    "isdigit", "isidentifier", "islower", "isnumeric", "isprintable",
    "isspace", "istitle", "isupper", "is_absolute", "is_symlink", "is_file",
    "is_dir", "exists", "samefile", "isdisjoint", "issubset", "issuperset",
    "is_integer", "get_blocking",
})

# Bound exactly once from the launcher-inherited, already-proved workspace
# root descriptor.  Every later openat2 is anchored to this long-held dirfd;
# the producer never reopens ROOT by pathname.
_COLD_WORKSPACE_ROOT_FD = -1
_COLD_WORKSPACE_ROOT_BEFORE: os.stat_result | None = None
_COLD_WORKSPACE_ROOT_MOUNT_ID = -1

# Linux memfd seal ABI.  The cold launcher supplies an already sealed,
# unlinked executable copy; the installed producer is a distinct held source
# fd used for pathname identity and byte equality, never as the exec entry.
F_GET_SEALS = getattr(fcntl, "F_GET_SEALS", 1034)
F_SEAL_SEAL = getattr(fcntl, "F_SEAL_SEAL", 0x0001)
F_SEAL_SHRINK = getattr(fcntl, "F_SEAL_SHRINK", 0x0002)
F_SEAL_GROW = getattr(fcntl, "F_SEAL_GROW", 0x0004)
F_SEAL_WRITE = getattr(fcntl, "F_SEAL_WRITE", 0x0008)
REQUIRED_EXEC_SEALS = F_SEAL_SEAL | F_SEAL_SHRINK | F_SEAL_GROW | F_SEAL_WRITE

EXPECTED_UNIVERSE = 76_832
EXPECTED_BASELINE = 75_684
EXPECTED_OVERLAY = 1_148
EXPECTED_LARGE = 1_124
EXPECTED_SINGLETON = 24
EXPECTED_C55B_CELLS = 1_724
EXPECTED_PAIRS = 862
EXPECTED_BASELINE_PAIRS = 288
EXPECTED_OVERLAY_PAIRS = 574
EXPECTED_LARGE_PAIRS = 562
EXPECTED_SINGLETON_PAIRS = 12
EXPECTED_PENDING_D02 = 33_638
EXPECTED_C55B_EDGES = 5_358
EXPECTED_COMPONENT_PAIR_COUNTS = {
    (0, 1): 850, (2, 13): 1, (3, 21): 1, (4, 15): 1,
    (5, 20): 1, (6, 7): 1, (8, 9): 1, (10, 19): 1,
    (11, 24): 1, (12, 18): 1, (14, 16): 1, (17, 25): 1,
    (22, 23): 1,
}
EXPECTED_GLUE_KIND_CENSUS = {
    "INHERITED_FIRST_EVENT_FACE": 336, "INTRA_CHART_FACE": 3_952,
    "SOURCE_CHART_TRANSITION": 38, "SOURCE_GRAZING_FACE": 1_024,
    "SOURCE_GRAZING_SEAM_CORNER": 8,
}
EXPECTED_EDGE_SCOPE_CENSUS = {
    "EXCLUDED_EVENT_CANDIDATE": 40, "GLOBAL_CORNER_INVENTORY": 8,
    "GLOBAL_GRAZING_INVENTORY": 1_024, "LIVE_TYPED_EVENT": 296,
    "ORDINARY_INTERNAL": 3_276,
    "ORDINARY_TO_FORMAL_EXCLUSION_BOUNDARY": 310,
    "ORDINARY_TO_TYPED_EVENT_BOUNDARY": 404,
}
C55B_C37_PAIR_INDEX_SEQUENCE_PIN = "b2b1c903abd44a5bd6aa6d85535a52f6d17ee91e6de8ee68c25ec354432fecda"
C55B_C42_PAIR_INDEX_SEQUENCE_PIN = "00d8e4a88766a2bba46f9a06f528795773c0606d66cd71e87fa26700e2fa4807"
C55B_C53_PAIR_INDEX_SEQUENCE_PIN = "eb1f66adc4f6a54819555a36bbeb108091614135761743cd4ec9fea0b51cba0e"
C55B_COMPONENT_INVOLUTION_SUMMARY_PIN = "0cdbdafd1edf87aee1e96b521867d69ddaa431a474e679cb9d6a4799e644612c"
C55B_FULL_PAIR_SUMMARY_PIN = "40d7b43d7e6b3852644bf6d3d6a3470df5203e3a8cf1a81aaa62cace77a239e1"

# Prefix/Kraft is reconstructed from the installed C42 parent-conservation
# authority and the independently audited C53 projection.  C72g's aggregate
# boolean is deliberately only redundant corroboration.
C42_CANDIDATE_DIR = ROOT / ".cm2-runtime/candidates/c42-p391-formal-producer-20260811T044500Z-f1"
C42_PARENT_PATH = C42_CANDIDATE_DIR / "parent_conservation.jsonl.gz"
C42_RESULT_PATH = C42_CANDIDATE_DIR / "result.json"
C42_MANIFEST_PATH = C42_CANDIDATE_DIR / "root_manifest.sha256"
C42_INDEPENDENT_AUDIT_PATH = ROOT / ".cm2-runtime/audit/c42-independent-audit-20260811T052900Z-p391-f1/independent_audit.json"
C42_INSTALLATION_RECEIPT_PATH = ROOT / ".cm2-runtime/audit/c42-f1-authority-install-a50914a266af-85a7cd719cee-v1/installation_receipt.json"
C42_INDEPENDENT_AUDIT_DIR = C42_INDEPENDENT_AUDIT_PATH.parent
C42_INSTALLATION_RECEIPT_DIR = C42_INSTALLATION_RECEIPT_PATH.parent
C42_CANDIDATE_TOKEN_PATH = ROOT / ".cm2-runtime/c42-current-token"
C42_AUDIT_TOKEN_PATH = ROOT / ".cm2-runtime/c42-current-audit-token"
C42_SEAL_PATH = ROOT / ".cm2-runtime/c42-current-authority-seal"
C53_AUDIT_PATH = OUT / "cm2_round306c53_d02a_pair1_pair_level_successor_independent_audit_v1.json"
C53_HEAD_PATH = ROOT / ".cm2-runtime/cm2-global-authority-heads/predecessor-10fb050d30c92b0f2bdcf85a30d28ff670d8efc0b48104b7f04a63c391967b41.seal"
C42_CANDIDATE_TOKEN = "c42-p391-formal-producer-20260811T044500Z-f1"
C42_AUDIT_TOKEN = "c42-independent-audit-20260811T052900Z-p391-f1"
C42_INSTALLATION_RELEASE = "c42-f1-authority-install-a50914a266af-85a7cd719cee-v1"
C42_INSTALLATION_RECEIPT_REL = ".cm2-runtime/audit/" + C42_INSTALLATION_RELEASE + "/installation_receipt.json"
C42_CANDIDATE_MANIFEST_MEMBERS = {
    "C42_SINGLETON_CLOSURE.lock", "corner_owner_incidence.jsonl.gz",
    "exact_source.jsonl.gz", "face_owner_incidence.jsonl.gz",
    "interior_certificates.jsonl.gz", "parent_conservation.jsonl.gz",
    "reflection_transport.jsonl.gz", "result.json",
}
C42_C53_PINS = {
    "C42_parent": "9e414b2fea9de614e73fd72f604fb857fb332dbfef49f11c33ae3929f68c8323",
    "C42_result": "f029c3ce6af33e2f93c33b4155286f60bfafecd724720a598b103ca3c263ccb0",
    "C42_manifest": "ce1b6260b26a901a9dda3cfbd94eba5a752b5188d6bdbe7c7d3cd7a4d3f7d058",
    "C42_independent_audit": "d60bb3c8f79f989df776effa4616ec170097a018547b1f4c929ad068c11138d3",
    "C42_installation_receipt": "3599494ff330a367a6c27ee57c19c01e86626428871d014c9153f290fdfc407f",
    "C42_candidate_token": "fbc5dd3c55bfdd3098ed34ae09ae633a9526a9c9cc6f40b3d87b5669b2ea7f07",
    "C42_audit_token": "59aca53c4c35260801b3c559648c88ee974db01ae950f045a5e5aecd64aa36e5",
    "C42_seal": "0e5a76059b2c9407340d88e07f4fcc356d376f5c24b7173e6b95fd5e06bc312d",
    "C53_audit": "b58a6ba170e43be02ca414208e7197e746183dd335a49982b9ae28dab919497b",
    "C53_head": "f62483c87df4b6f4a8a2ad8dcf56febbfce9977200ce94a0ad6ce38e736aeeb3",
}
C42_C53_PATHS = {
    "C42_parent": C42_PARENT_PATH,
    "C42_result": C42_RESULT_PATH,
    "C42_manifest": C42_MANIFEST_PATH,
    "C42_independent_audit": C42_INDEPENDENT_AUDIT_PATH,
    "C42_installation_receipt": C42_INSTALLATION_RECEIPT_PATH,
    "C42_candidate_token": C42_CANDIDATE_TOKEN_PATH,
    "C42_audit_token": C42_AUDIT_TOKEN_PATH,
    "C42_seal": C42_SEAL_PATH,
    "C53_audit": C53_AUDIT_PATH,
    "C53_head": C53_HEAD_PATH,
}
C42_C53_EXPECTED_MODES = {
    "C42_parent": 0o664,
    "C42_result": 0o664,
    "C42_manifest": 0o664,
    "C42_independent_audit": 0o600,
    "C42_installation_receipt": 0o444,
    "C42_candidate_token": 0o444,
    "C42_audit_token": 0o444,
    "C42_seal": 0o444,
    "C53_audit": 0o664,
    "C53_head": 0o444,
}
C42_CANDIDATE_DIRECTORY_EXPECTED_MODE = 0o755
C42_CANDIDATE_MEMBER_EXPECTED_MODE = 0o664
C42_INDEPENDENT_AUDIT_DIRECTORY_EXPECTED_MODE = 0o700
C42_INSTALLATION_RECEIPT_DIRECTORY_EXPECTED_MODE = 0o500
C42_RESULT_OBJECT_PIN = "a50914a266aff3396054d7f16e91d69db7fa735ad15f01cbf07eee8e708d99d2"
C42_EXECUTION_RECEIPT_OBJECT_PIN = "e89f66d0e7636bfa781a6ef7e0309fc1ad00c3215ea699c08b231003e1c39f08"
C42_INDEPENDENT_AUDIT_OBJECT_PIN = "85a7cd719cee9dceb1763135f74d50bcf28f78ff2426e65996b975b1def7790c"
C42_INSTALLATION_RECEIPT_OBJECT_PIN = "c5f2eb78a0d9d717326bc57fb14df823ab3c5181e3e613a0327425c5e33e784e"
C42_SEAL_OBJECT_PIN = "b321552768a6aeae6c1d229e52b61ca0b4420314234e02e98366153d4156d460"
C53_AUDIT_OBJECT_PIN = "a7bee7e57b6527c7bf9ea7f17966379c62a722fe9ce2ce2009f19f85a5afaa7c"
C53_HEAD_OBJECT_PIN = "cb90ab914c3b6518384669f42d05df33c21a717596190131c6a0f5683934cbfb"

TERMINALS = {
    "CONNECTED_TO_KNOWN",
    "EARLIEST_PREFIX_EXCLUDED",
    "SOURCE_GRAZING_OR_CEMETERY",
    "TYPED_EVENT_GRAPH",
}
LARGE_MAP = {
    "WHOLE_PUBLIC_CELL_STRICT_EXCLUSION": (
        "EARLIEST_PREFIX_EXCLUDED",
        "C78L_WHOLE_STRICT_TO_EARLIEST_PREFIX_EXCLUDED",
    ),
    "EXHAUSTIVE_PUBLIC_CELL_TYPED_EVENT_C3_PARTITION": (
        "TYPED_EVENT_GRAPH",
        "C78L_TYPED_PARTITION_TO_TYPED_EVENT_GRAPH",
    ),
}
SINGLETON_MAP = {
    "STRICT_EXCLUSION_ONLY": (
        "EARLIEST_PREFIX_EXCLUDED",
        "C78S_STRICT_ONLY_TO_EARLIEST_PREFIX_EXCLUDED",
    ),
    "STRICT_EXCLUSION_PLUS_CEMETERY_TANGENCY": (
        "SOURCE_GRAZING_OR_CEMETERY",
        "C78S_STRICT_PLUS_CEMETERY_TO_SOURCE_GRAZING_OR_CEMETERY",
    ),
}
CLOSURE = {
    "owner": True,
    "history": True,
    "glue": True,
    "two_sides": True,
    "incidence": True,
    "prefix_Kraft": True,
}
ZERO_CANDIDATE_CREDIT = {
    "formal_global_closure_credit": 0,
    "D02_unlock": False,
    "D02_gate_credit": 0,
    "D02_task_credit": 0,
    "D02_formal_pending_task_count": EXPECTED_PENDING_D02,
    "D02_started": False,
}

C55A_PATHS = {
    "leaf_ledger": OUT / "cm2_round306c55a_four_chart_fundamental_domain_bnb_leaf_ledger_v1.json",
    "result": OUT / "cm2_round306c55a_four_chart_fundamental_domain_bnb_result_v1.json",
    "verification": OUT / "cm2_round306c55a_four_chart_fundamental_domain_bnb_independent_verification_v1.json",
    "manifest": OUT / "cm2_round306c55a_four_chart_fundamental_domain_bnb_manifest_v1.sha256",
}
C55A_PINS = {
    "leaf_ledger": "e80c012e3260e8f9e68d5858ba5d9dafd94611e2a1c1200d787a20e3842d8db6",
    "result": "d38f39792fc944b72e70100f9f96f312b5e30e034d5104ce5f848d24378ae5af",
    "verification": "6e9dfe5c50cfb104cbb8014873f69f79761b22848f50a51033fced651a121772",
    "manifest": "848c56c5d328cbdf291715d1eaab2611d3af95fb8bf2875beaadcbb9ffca6e0d",
}
C55A_OBJECTS = {
    "leaf_ledger": "7dd4c19cfb2b9f8cd30a4a9a23e30f11734e856cc6cc5a04e9a169c051059d90",
    "result": "93b732cd65be4453e7b29379d7f70d8c849057d5bcba5489e1f6c4dd705972e3",
    "verification": "cd6e3915f1dd89d8eef0766b4a806bc8a22244f348162af72fd009b98368d623",
}

C55B_PATHS = {
    "cells": OUT / "cm2_round306c55b_global_component_adjacency_known_sheet_cell_component_crosswalk_v1.jsonl.gz",
    "edges": OUT / "cm2_round306c55b_global_component_adjacency_known_sheet_component_edges_and_glue_v1.jsonl.gz",
    "components": OUT / "cm2_round306c55b_global_component_adjacency_known_sheet_ordinary_components_v1.jsonl.gz",
    "result": OUT / "cm2_round306c55b_global_component_adjacency_known_sheet_result_v1.json",
    "verification": OUT / "cm2_round306c55b_global_component_adjacency_known_sheet_independent_verification_v1.json",
    "self_test": OUT / "cm2_round306c55b_global_component_adjacency_known_sheet_independent_self_test_v1.json",
    "manifest": OUT / "cm2_round306c55b_global_component_adjacency_known_sheet_manifest_v1.sha256",
}
C55B_PINS = {
    "cells": "123a742ed553d89fd1026cf65c64879d9a92916492b5b583888c3312551ca2ce",
    "edges": "23ea0b4419f155f62d32b6b73c5a16c6f402884d333c222ff803899a58da29a0",
    "components": "bebc49f66efb01c0b980ec10258a60d7aead9d4d2006d28bdd169c9a9ae38a04",
    "result": "6bf9cae7b4b422c5c2121f95828e1508700fe1a5d1b1128598c8617f65032a93",
    "verification": "42f31f0c158b08651bec97d83d6980f0372353e71cb4f59959f186a329601bae",
    "self_test": "e2e45f1a26ae73dd5e0aca08d8fa05b5b3f87fc985cf0a55b977c136948c7a15",
    "manifest": "c5bd6973bd4836c3d72ae6c32961266ea12a281e4821306fbcc69be86acc45be",
}
C55B_OBJECTS = {
    "result": "1ce396e9746d3c0364325e8308e94c9dcd4a3bfbba8c17a9c9961915e807cc56",
    "verification": "350f076a3dcfaa4424bfb27f2730e876d0f6159baa033c7aafbfaded8c870a68",
    "self_test": "665cb4eea435b367e8c261788c0c6fe30620b2f0f66f6cd618976500ada1ef01",
}

C72G_PATHS = {
    "contract": OUT / "cm2_round306c72g_no_producer_global_consumer_successor_contract_v1.json",
    "verification": OUT / "cm2_round306c72g_no_producer_global_consumer_successor_verification_v1.json",
    "self_test": OUT / "cm2_round306c72g_no_producer_global_consumer_successor_self_test_v1.json",
    "manifest": OUT / "cm2_round306c72g_no_producer_global_consumer_successor_manifest_v1.sha256",
    "outer": OUT / "cm2_round306c72g_no_producer_global_consumer_successor_outer_receipt_v1.json",
    "head": ROOT / ".cm2-runtime/cm2-global-authority-heads/predecessor-10fb050d30c92b0f2bdcf85a30d28ff670d8efc0b48104b7f04a63c391967b41.seal",
}
C72G_PINS = {
    "contract": "6de59a039600f75d0b0d5722f9735fb2456f3b25b8a777df3fffef1f27e1749a",
    "verification": "7e21fcca280d1f860559d9a1a4afdd2f592b717c5844fc4178fabb2e1d8b684f",
    "self_test": "79935bb45848ff83db595a4b173bd2df12925be09fa4c3be66dabcdd5453b058",
    "manifest": "fa77aff4fee070710fb9daf3d229182fb9f14f6b3e7a2534bb728ea91f5a51a7",
    "outer": "de70ab6c7c621e768662055f96a552d5cb4aaae123d4dd82b56ceed926fa68ee",
    "head": "f62483c87df4b6f4a8a2ad8dcf56febbfce9977200ce94a0ad6ce38e736aeeb3",
}
C72G_OBJECTS = {
    "contract": "5b2784b7f033ba4dde0a3d7f30af05ba4a71fb64bd6bf9fe34b64c48cc976b51",
    "verification": "cd259985de0d2c43d5ad030843fc8116204c6f1cbcce1e18eea44137fe62c62d",
    "self_test": "0ac9d83cc5e08dae3d0aabeddc2bf0fa665af0bc31c382ff20543c31ec64e0c1",
    "outer": "6380e5bf80dc2063bce5632fa73389dd07f4fe175c6c4b54a2661516d712fa92",
    "head": "cb90ab914c3b6518384669f42d05df33c21a717596190131c6a0f5683934cbfb",
}

HISTORICAL_FIXED_EXPECTED_MODES = {
    **{C55A_PATHS[key]: mode for key, mode in {
        "leaf_ledger": 0o444, "result": 0o444,
        "verification": 0o444, "manifest": 0o664,
    }.items()},
    **{C55B_PATHS[key]: 0o664 for key in C55B_PATHS},
    **{C72G_PATHS[key]: mode for key, mode in {
        "contract": 0o664, "verification": 0o644, "self_test": 0o644,
        "manifest": 0o644, "outer": 0o644, "head": 0o444,
    }.items()},
}
C78L_HISTORICAL_DIRECTORY_EXPECTED_MODE = 0o755
C78S_HISTORICAL_DIRECTORY_EXPECTED_MODE = 0o555
C78_HISTORICAL_MEMBER_EXPECTED_MODE = 0o444

C78L_A = ROOT / ".cm2-runtime/c78l-build-a3.9cdedea3"
C78L_B = ROOT / ".cm2-runtime/c78l-build-b3.9cdedea3"
C78L_VERIFY_A = ROOT / ".cm2-runtime/c78l-independent-v1-a3.a384bba4.json"
C78L_VERIFY_B = ROOT / ".cm2-runtime/c78l-independent-v1-b3.a384bba4.json"
C78L_COMPLETION = ROOT / ".cm2-runtime/c78l-completion-a3.a384bba4"
C78L_PREFIX = "cm2_round306c78l_large_component_final_no_producer_consumer_v1"
C78L_NAMES = {
    "lock": "ZERO_CREDIT_STAGED_C78L_FINAL_CONSUMER_ONLY.lock",
    "tasks": C78L_PREFIX + "_task_consumption.jsonl.gz",
    "sides": C78L_PREFIX + "_task_side_occurrences.jsonl.gz",
    "cells": C78L_PREFIX + "_public_cell_rollup.jsonl.gz",
    "pairs": C78L_PREFIX + "_reflection_pair_rollup.jsonl.gz",
    "registry": C78L_PREFIX + "_source_registry.json",
    "result": C78L_PREFIX + "_result.json",
    "report": C78L_PREFIX + "_report.md",
    "manifest": C78L_PREFIX + "_manifest.sha256",
    "outer": C78L_PREFIX + "_outer_receipt.json",
}
C78L_PINS = {
    "lock": "3eaaa094987dce2545148d6e66c7fb241f2e7429b2988547eff064d05b0f8b19",
    "tasks": "e439be9ae8bc56ab00479baab6d23c029bc6274e7fda72d986153e97fed8c6c9",
    "sides": "7b2f7b57e1d7eeab6fbd1075f23e4d837e9521cb3c17a9d5ab6ef82de4dbea52",
    "cells": "a602f62b5c1c54253256887feac37359cdbb408ce2cad6678c853551e4a1c115",
    "pairs": "47b0c22dc66139964b1a93060ecae30b3fe4786ade5d842ca3e193c63becbbfa",
    "registry": "bf7aa990854950430effb0bc8a05c8e77051f25e3eca8b043cef9a91a237a893",
    "result": "0ab8e3dc9c379dbc14a276b05a394ef96e1cbe93392c940edb0cfe4f246cbb1d",
    "report": "42b6041bf25e94faec45dadf5c013d0d83f995a4e1f9c9e39d81e7c74a294be8",
    "manifest": "09c8a466d3906e01ea38d504f4dcb81b812e591ae7d515551674f7232982bd19",
    "outer": "e343c21c4c5ba1273d370e10eca5aba82e34c6b7f05609b7cb3c25878af0d044",
}
C78L_VERIFY_FILE_PIN = "22223e2aca6eaa069cfda7ab95da5f31b6adb36773544f9f2034bd01c6d1f0c1"
C78L_VERIFY_OBJECT_PIN = "850eba67fb2d343e8b607394469c8d2febf47229b26d86c6894249fd060c1419"
C78L_COMPLETION_NAMES = {
    "receipt": C78L_PREFIX + "_dual_completion_receipt.json",
    "manifest": C78L_PREFIX + "_dual_completion_manifest.sha256",
    "outer": C78L_PREFIX + "_dual_completion_outer_receipt.json",
}
C78L_COMPLETION_PINS = {
    "receipt": "235e876e53f1ee390ce0f89715fe465376de6b82e07ef6258068e26f35b8a3fd",
    "manifest": "c2ff451ad50cbe5f9b226569351e255b441f7ae500b81867c539b12a8656b1ff",
    "outer": "aa6da7b659af57e7eb5f45ea6e88fc67acdb2e6cbc51953e18e01f265a4e70e4",
}
C78L_RESULT_OBJECT_PIN = "bfee46ce15d46718326881fce97cbca7ff10df459732a789b314928ca7c62204"
C78L_COMPLETION_OBJECT_PIN = "4b627b9e05d4552ce1a5c55c31a2e9dc11e3e5067657691e0b3fdfdf53562cfe"
C78L_COMPLETION_OUTER_OBJECT_PIN = "d67abd63ffabefddcb7829cb781dc038a00498686726e54d806db10f3c2fc4a9"

C78S_PREFIX = "cm2_round306c78s_singleton_final_no_producer_consumer_v1"
C78S_NAMES = {
    "lock": "ZERO_CREDIT_CANDIDATE_SINGLETON_FINAL_NO_PRODUCER_CONSUMER_ONLY.lock",
    "children": C78S_PREFIX + "_child_dispositions.jsonl.gz",
    "sources": C78S_PREFIX + "_source_rollups.jsonl.gz",
    "pairs": C78S_PREFIX + "_reflection_pair_rollups.jsonl.gz",
    "cells": C78S_PREFIX + "_singleton_cell_rollups.jsonl.gz",
    "projection": C78S_PREFIX + "_global_enum_projection.jsonl.gz",
    "result": C78S_PREFIX + "_result.json",
    "report": C78S_PREFIX + "_report.md",
    "manifest": C78S_PREFIX + "_manifest.sha256",
    "outer": C78S_PREFIX + "_outer_receipt.json",
}
# Frozen, independently verified C78s 13-member final surface.
C78S_FINAL = {
    "build_A_directory": ".cm2-runtime/c78s-build-a.v1",
    "build_B_directory": ".cm2-runtime/c78s-build-b.v1",
    "pins": {
        "lock": "29e545e9b6fe75f95215a80bbbefee2a56668153f29a5afd42ea2afeddeb523e",
        "children": "cdb5606dd4561846e46bb484a3e4b34f11b6e89c8867c25acf4c43982dfc4783",
        "sources": "efad60b5cff0193033c92577d7c3b2e6c8788b47c8d7e45e0c474f59a491cc25",
        "pairs": "68493c4c1ef530c14b74cdac03a6e7cc632a0f788db05c15b69a58625b9bc614",
        "cells": "89d04fdb79cf5b6af95e6abc85978e684c6fcce86e221b28cf756b5e6afaaa7a",
        "projection": "2bb4e3c2885ed2d87b34ea7a79f2f850452eb402673d5cdfae8fdfdada0f27da",
        "result": "8256d10eb8f81db49ec33782f510e18ed61f3b8bfe8f9406adc457c152083ac4",
        "report": "c9ae55aff5ff8897023f0d8d9500cac2a7fedc1f14798d4e0db195d1597c839d",
        "manifest": "73aa1f256fcdc585b5c824ba5d0c48fd9d37de80054f2d4411df413880b982f4",
        "outer": "dd2ec68ec46fb8e6cf50032e575fe0429344c83d8e8979ca9a2f414f7522cabd",
    },
    "result_object_sha256": "7e79d23a1dc1d2cf6c9f59ddb41571649a0a8d7f4a8451f9565ef89730552edd",
    "verification_A_path": ".cm2-runtime/c78s-build-a.v1/cm2_round306c78s_singleton_final_no_producer_consumer_independent_verification_v1.json",
    "verification_A_file_sha256": "b9fe78455672fa873a23d6bd2d8c803dfa26ab38986275cd35aefc5cd51690c6",
    "verification_A_object_sha256": "dff4cc4af2f1348a110c0010c58444607eb49707a63fb30380d405911f319d82",
    "verification_B_path": ".cm2-runtime/c78s-build-b.v1/cm2_round306c78s_singleton_final_no_producer_consumer_independent_verification_v1.json",
    "verification_B_file_sha256": "b9fe78455672fa873a23d6bd2d8c803dfa26ab38986275cd35aefc5cd51690c6",
    "verification_B_object_sha256": "dff4cc4af2f1348a110c0010c58444607eb49707a63fb30380d405911f319d82",
    "verifier_source_file_sha256": "7884f606a45e35b15425c1f20864376ea78c8615ec74e467227d76c8081c2b27",
    "final_manifest_A_path": ".cm2-runtime/c78s-build-a.v1/cm2_round306c78s_singleton_final_no_producer_consumer_final_manifest_v1.sha256",
    "final_manifest_B_path": ".cm2-runtime/c78s-build-b.v1/cm2_round306c78s_singleton_final_no_producer_consumer_final_manifest_v1.sha256",
    "final_manifest_file_sha256": "568e60d5d67703a9fc9cf8fa4082865c3cd78474ba5bfac6f6fc435e38290642",
    "final_outer_A_path": ".cm2-runtime/c78s-build-a.v1/cm2_round306c78s_singleton_final_no_producer_consumer_final_outer_receipt_v1.json",
    "final_outer_B_path": ".cm2-runtime/c78s-build-b.v1/cm2_round306c78s_singleton_final_no_producer_consumer_final_outer_receipt_v1.json",
    "final_outer_file_sha256": "6c682ee6e22340fe0a329f834e675198a541244a79b1577189e940bd488a9145",
    "final_outer_object_sha256": "500efc48360a239817cce40106850d96dce257f15d57e7711ca3c8bb7bf57242",
    "closure_receipt_is_final_outer": True,
    "final_stage_member_count_per_build": 13,
    "extra_completion_receipt_exists": False,
}

LOCK = "ZERO_CREDIT_CANDIDATE_C79G_TRUE_GLOBAL_CONSUMER_ONLY.lock"
OVERLAY = BASE + "_overlay_1148.jsonl.gz"
SUCCESSOR = BASE + "_full_successor_76832.jsonl.gz"
PARENTS = BASE + "_reflection_parent_closure_862.jsonl.gz"
REGISTRY = BASE + "_source_registry.json"
RESULT = BASE + "_result.json"
REPORT = BASE + "_report.md"
CANDIDATE_MANIFEST = BASE + "_candidate_manifest.sha256"
CANDIDATE_OUTER = BASE + "_candidate_outer_receipt.json"
CANDIDATE_MEMBERS = (
    LOCK, OVERLAY, SUCCESSOR, PARENTS, REGISTRY, RESULT, REPORT,
    CANDIDATE_MANIFEST, CANDIDATE_OUTER,
)


class Reject(RuntimeError):
    pass


AT_EMPTY_PATH = 0x1000
AT_SYMLINK_NOFOLLOW = 0x100
STATX_BASIC_STATS = 0x000007ff
STATX_MNT_ID = 0x00001000
RENAME_NOREPLACE = 1
RESOLVE_NO_XDEV = 0x01
RESOLVE_NO_MAGICLINKS = 0x02
RESOLVE_NO_SYMLINKS = 0x04
RESOLVE_BENEATH = 0x08


class OpenHow(ctypes.Structure):
    _fields_ = [("flags", ctypes.c_uint64), ("mode", ctypes.c_uint64),
                ("resolve", ctypes.c_uint64)]


class StatxTimestamp(ctypes.Structure):
    _fields_ = [("tv_sec", ctypes.c_int64), ("tv_nsec", ctypes.c_uint32),
                ("reserved", ctypes.c_int32)]


class Statx(ctypes.Structure):
    _fields_ = [
        ("stx_mask", ctypes.c_uint32), ("stx_blksize", ctypes.c_uint32),
        ("stx_attributes", ctypes.c_uint64), ("stx_nlink", ctypes.c_uint32),
        ("stx_uid", ctypes.c_uint32), ("stx_gid", ctypes.c_uint32),
        ("stx_mode", ctypes.c_uint16), ("spare0", ctypes.c_uint16),
        ("stx_ino", ctypes.c_uint64), ("stx_size", ctypes.c_uint64),
        ("stx_blocks", ctypes.c_uint64), ("stx_attributes_mask", ctypes.c_uint64),
        ("stx_atime", StatxTimestamp), ("stx_btime", StatxTimestamp),
        ("stx_ctime", StatxTimestamp), ("stx_mtime", StatxTimestamp),
        ("stx_rdev_major", ctypes.c_uint32), ("stx_rdev_minor", ctypes.c_uint32),
        ("stx_dev_major", ctypes.c_uint32), ("stx_dev_minor", ctypes.c_uint32),
        ("stx_mnt_id", ctypes.c_uint64), ("stx_dio_mem_align", ctypes.c_uint32),
        ("stx_dio_offset_align", ctypes.c_uint32),
        ("spare3", ctypes.c_uint64 * 12),
    ]


def _linux_libc() -> ctypes.CDLL:
    need(sys.platform.startswith("linux"), "Linux-only v16r2 publication protocol")
    library = ctypes.CDLL(None, use_errno=True)
    need(hasattr(library, "syscall") and hasattr(library, "statx") and
         hasattr(library, "renameat2"),
         "openat2+statx+renameat2 required; fail closed without fallback")
    return library


def _root_relative(path: Path) -> bytes:
    absolute = Path(os.path.abspath(path))
    need(absolute != ROOT and ROOT in absolute.parents,
         "exact lexical workspace-root-contained path:" + str(path))
    relative = absolute.relative_to(ROOT)
    need(len(relative.parts) > 0 and
         all(part not in {"", ".", ".."} for part in relative.parts),
         "clean lexical workspace-relative path:" + str(path))
    return os.fsencode(str(relative))


def openat2_beneath(path: Path, flags: int) -> int:
    library = _linux_libc()
    need(_COLD_WORKSPACE_ROOT_FD >= 3 and
         _COLD_WORKSPACE_ROOT_BEFORE is not None and
         _COLD_WORKSPACE_ROOT_MOUNT_ID >= 0,
         "inherited cold workspace root fd configured before any openat2")
    how = OpenHow(flags | os.O_CLOEXEC, 0,
                  RESOLVE_NO_XDEV | RESOLVE_NO_MAGICLINKS |
                  RESOLVE_NO_SYMLINKS | RESOLVE_BENEATH)
    ctypes.set_errno(0)
    descriptor = library.syscall(
        ctypes.c_long(437), ctypes.c_int(_COLD_WORKSPACE_ROOT_FD),
        ctypes.c_char_p(_root_relative(path)), ctypes.byref(how),
        ctypes.c_size_t(ctypes.sizeof(how)))
    if descriptor < 0:
        code = ctypes.get_errno()
        raise Reject("openat2 fail closed:" + str(path) + ":" + os.strerror(code))
    return int(descriptor)


def statx_mount_id(descriptor: int) -> int:
    library = _linux_libc()
    info = Statx()
    ctypes.set_errno(0)
    outcome = library.statx(ctypes.c_int(descriptor), ctypes.c_char_p(b""),
                            ctypes.c_int(AT_EMPTY_PATH | AT_SYMLINK_NOFOLLOW),
                            ctypes.c_uint(STATX_BASIC_STATS | STATX_MNT_ID),
                            ctypes.byref(info))
    if outcome != 0:
        code = ctypes.get_errno()
        raise Reject("statx mount identity fail closed:" + os.strerror(code))
    need(bool(info.stx_mask & STATX_MNT_ID), "statx mount id unavailable")
    return int(info.stx_mnt_id)


def workspace_root_terminal_replay() -> None:
    """Reprove the inherited root fd and its label without reopening ROOT."""
    need(_COLD_WORKSPACE_ROOT_FD >= 3 and
         _COLD_WORKSPACE_ROOT_BEFORE is not None and
         _COLD_WORKSPACE_ROOT_MOUNT_ID >= 0,
         "cold workspace root guard configured")
    before = _COLD_WORKSPACE_ROOT_BEFORE
    current = os.fstat(_COLD_WORKSPACE_ROOT_FD)
    path_current = ROOT.lstat()
    need(stat.S_ISDIR(current.st_mode) and stat.S_ISDIR(path_current.st_mode) and
         (current.st_dev, current.st_ino, current.st_mode, current.st_nlink) ==
             (before.st_dev, before.st_ino, before.st_mode, before.st_nlink) ==
             (path_current.st_dev, path_current.st_ino,
              path_current.st_mode, path_current.st_nlink) and
         statx_mount_id(_COLD_WORKSPACE_ROOT_FD) ==
             _COLD_WORKSPACE_ROOT_MOUNT_ID,
         "inherited workspace root fd/path identity and mount terminal replay")


def file_fingerprint(value: os.stat_result) -> tuple[int, ...]:
    return (value.st_dev, value.st_ino, value.st_mode, value.st_nlink,
            value.st_size, value.st_mtime_ns, value.st_ctime_ns)


def cold_publication_chronology(
        exact8: list[os.stat_result], manifest: os.stat_result,
        outer: os.stat_result) -> dict[str, bool]:
    exact8_mtime_not_after_ctime = all(
        item.st_mtime_ns <= item.st_ctime_ns for item in exact8)
    max_exact8_before_manifest = (
        max(max(item.st_mtime_ns, item.st_ctime_ns) for item in exact8) <
        manifest.st_mtime_ns)
    manifest_mtime_not_after_ctime = manifest.st_mtime_ns <= manifest.st_ctime_ns
    manifest_ctime_before_outer = manifest.st_ctime_ns < outer.st_mtime_ns
    outer_mtime_not_after_ctime = outer.st_mtime_ns <= outer.st_ctime_ns
    return {
        "all_exact8_mtime_not_after_final_ctime": exact8_mtime_not_after_ctime,
        "max_exact8_final_mtime_ctime_before_manifest_mtime":
            max_exact8_before_manifest,
        "manifest_mtime_not_after_final_ctime": manifest_mtime_not_after_ctime,
        "manifest_final_ctime_before_outer_mtime": manifest_ctime_before_outer,
        "outer_mtime_not_after_final_ctime": outer_mtime_not_after_ctime,
        "physical_exact8_freeze_then_manifest_freeze_then_outer_freeze_chronology":
            exact8_mtime_not_after_ctime and max_exact8_before_manifest and
            manifest_mtime_not_after_ctime and manifest_ctime_before_outer and
            outer_mtime_not_after_ctime,
    }


def directory_fingerprint(value: os.stat_result) -> tuple[int, ...]:
    return (value.st_dev, value.st_ino, value.st_mode, value.st_nlink,
            value.st_mtime_ns, value.st_ctime_ns)


_ACTIVE_HELD_RESOURCES: list[Any] = []


def register_held_resource(value: Any) -> None:
    """Register every opened fd immediately for exception-safe reverse close."""
    _ACTIVE_HELD_RESOURCES.append(value)


def close_all_held_resources() -> None:
    """Best-effort idempotent cleanup after success or any fail-closed path."""
    while _ACTIVE_HELD_RESOURCES:
        value = _ACTIVE_HELD_RESOURCES.pop()
        try:
            value.close()
        except OSError:
            pass


class HeldWorkspaceRoot:
    """Own the launcher-inherited workspace root for the whole invocation."""

    def __init__(self, inherited_fd: int, source_fd: int,
                 coordination_fd: int) -> None:
        try:
            self.fd = os.dup(inherited_fd)
        except OSError as exc:
            raise Reject("cold-launch inherited workspace root fd unavailable") from exc
        register_held_resource(self)
        self.before = os.fstat(self.fd)
        self.mount_id = statx_mount_id(self.fd)
        source_before = os.fstat(source_fd)
        coordination_before = os.fstat(coordination_fd)
        path_before = ROOT.lstat()
        need(stat.S_ISDIR(self.before.st_mode) and
             stat.S_ISREG(source_before.st_mode) and
             stat.S_ISDIR(coordination_before.st_mode) and
             stat.S_ISDIR(path_before.st_mode) and
             directory_fingerprint(path_before) ==
                 directory_fingerprint(self.before) and
             statx_mount_id(source_fd) == self.mount_id and
             statx_mount_id(coordination_fd) == self.mount_id,
             "inherited root/source/coordination fd types, path identity, and mount")

    def terminal_replay(self) -> None:
        workspace_root_terminal_replay()

    def close(self) -> None:
        if self.fd >= 0:
            os.close(self.fd)
            self.fd = -1


class HeldSelf:
    """Hold the v16r2 exec/source pair plus exact12 frozen v14 authority.

    Historical v3-v13 bytes are no longer inherited as live descriptors.
    Their append-only chain is transitively bound by the frozen v14 exact10,
    official rejection, and shape-drift supersession receipt held here.
    """

    def __init__(self, exec_inherited: int, source_inherited: int,
                 coordination_inherited: int, root_inherited: int,
                 authority_inherited: Mapping[Path, int]) -> None:
        self.exec_fd = -1
        self.source_fd = -1
        self.incident_fds: dict[Path, int] = {}
        self.incident_before: dict[Path, os.stat_result] = {}
        self.incident_mount_ids: dict[Path, int] = {}
        self.incident_raw: dict[Path, bytes] = {}
        self.incident_path_before: dict[Path, os.stat_result] = {}
        self.v12_shape_incident = copy.deepcopy(V12_V5_REJECTION_SHAPE_INCIDENT)
        self.v13_supersession_receipt: dict[str, Any] | None = None
        self.v14_supersession_receipt: dict[str, Any] | None = None
        self.v14_authority_replay: dict[str, Any] | None = None
        expected_rows = V14_INHERITED_AUTHORITY_EXACT12
        expected_paths = tuple(ROOT / row[1] for row in expected_rows)
        expected_pins = {ROOT / row[1]: row[2] for row in expected_rows}
        need(len(expected_rows) == V16R2_CHILD_AUTHORITY_DESCRIPTOR_COUNT == 12 and
             tuple(authority_inherited) == expected_paths and
             len(set(authority_inherited.values())) == 12,
             "producer exact ordered v14 authority exact12 inherited fds")
        try:
            self.exec_fd = os.dup(exec_inherited)
            self.source_fd = os.dup(source_inherited)
            for path, inherited_fd in authority_inherited.items():
                self.incident_fds[path] = os.dup(inherited_fd)
            register_held_resource(self)

            self.exec_before = os.fstat(self.exec_fd)
            self.source_before = os.fstat(self.source_fd)
            coordination_before = os.fstat(coordination_inherited)
            root_before = os.fstat(root_inherited)
            self.exec_mount_id = statx_mount_id(self.exec_fd)
            self.source_mount_id = statx_mount_id(self.source_fd)
            coordination_mount_id = statx_mount_id(coordination_inherited)
            root_mount_id = statx_mount_id(root_inherited)
            for path, descriptor in self.incident_fds.items():
                self.incident_before[path] = os.fstat(descriptor)
                self.incident_mount_ids[path] = statx_mount_id(descriptor)
            try:
                self.exec_seals = int(fcntl.fcntl(self.exec_fd, F_GET_SEALS))
            except OSError as exc:
                raise Reject("cold-launch exec fd is not a sealed memfd") from exc
            need(stat.S_ISREG(self.exec_before.st_mode) and
                 stat.S_IMODE(self.exec_before.st_mode) == 0o444 and
                 self.exec_before.st_nlink == 0 and
                 self.exec_seals == REQUIRED_EXEC_SEALS and
                 stat.S_ISREG(self.source_before.st_mode) and
                 stat.S_IMODE(self.source_before.st_mode) == 0o444 and
                 self.source_before.st_nlink == 1 and
                 stat.S_ISDIR(coordination_before.st_mode) and
                 stat.S_ISDIR(root_before.st_mode) and
                 self.source_mount_id == coordination_mount_id == root_mount_id and
                 all(stat.S_ISREG(value.st_mode) and
                     stat.S_IMODE(value.st_mode) == 0o444 and
                     value.st_nlink == 1
                     for value in self.incident_before.values()) and
                 all(value == root_mount_id
                     for value in self.incident_mount_ids.values()) and
                 len({(value.st_dev, value.st_ino)
                      for value in self.incident_before.values()}) == 12 and
                 (self.source_before.st_dev, self.source_before.st_ino) not in
                     {(value.st_dev, value.st_ino)
                      for value in self.incident_before.values()},
                 "sealed exec/source/root plus exact12 frozen v14 authority first gate")

            self.exec_raw = self._read_fd(self.exec_fd)
            self.source_raw = self._read_fd(self.source_fd)
            self.incident_raw = {
                path: self._read_fd(descriptor)
                for path, descriptor in self.incident_fds.items()}
            need(self.exec_raw == self.source_raw and
                 file_fingerprint(os.fstat(self.exec_fd)) ==
                     file_fingerprint(self.exec_before) and
                 file_fingerprint(os.fstat(self.source_fd)) ==
                     file_fingerprint(self.source_before) and
                 int(fcntl.fcntl(self.exec_fd, F_GET_SEALS)) == self.exec_seals and
                 all(file_fingerprint(os.fstat(self.incident_fds[path])) ==
                         file_fingerprint(self.incident_before[path]) and
                     statx_mount_id(self.incident_fds[path]) ==
                         self.incident_mount_ids[path] and
                     sha_bytes(self.incident_raw[path]) == expected_pins[path]
                     for path in expected_paths),
                 "producer sealed bytes and v14 exact12 fd hashes stable")

            held_by_role = {
                role: self.incident_raw[ROOT / relative]
                for role, relative, _file_pin, _object_pin in expected_rows}
            self.v14_authority_replay = \
                terminal_replay_v14_inherited_authority_exact12(held_by_role)
            need(self.v14_authority_replay.get("child_pass_fd_count") == 16 and
                 self.v14_authority_replay.get("formal_global_closure_credit") == 0 and
                 self.v14_authority_replay.get("D02_unlock") is False,
                 "producer v14 exact12 transitive zero-credit replay")

            v13_path = ROOT / V14_PUBLISHED_EXACT10_WITNESS[0][1]
            v13_value = strict_json(
                self.incident_raw[v13_path], "held v13 supersession receipt")
            need(isinstance(v13_value, dict), "held v13 receipt object")
            verify_object(v13_value, "held v13 supersession receipt",
                          V13_SUPERSESSION_RECEIPT_OBJECT_PIN)
            self.v13_supersession_receipt = v13_value
            v14_receipt_path = ROOT / \
                V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT_RELATIVE_PATH
            v14_value = strict_json(
                self.incident_raw[v14_receipt_path],
                "held v14 shape-drift supersession receipt")
            need(isinstance(v14_value, dict), "held v14 supersession object")
            verify_object(
                v14_value, "held v14 shape-drift supersession receipt",
                V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT_OBJECT_PIN)
            self.v14_supersession_receipt = v14_value

            # Pathnames are observed only after the descriptor-only first gate.
            need(SELF == OUT /
                 "cm2_round306c79g_true_global_no_producer_consumer_v16r2r63ah_repair_semantic_source.py",
                 "SELF exact frozen producer path")
            self.source_path_before = SELF.lstat()
            need(stat.S_ISREG(self.source_path_before.st_mode) and
                 stat.S_IMODE(self.source_path_before.st_mode) == 0o444 and
                 self.source_path_before.st_nlink == 1 and
                 file_fingerprint(self.source_path_before) ==
                     file_fingerprint(self.source_before),
                 "installed producer path equals held source fd")
            for path in expected_paths:
                path_before = path.lstat()
                need(stat.S_ISREG(path_before.st_mode) and
                     stat.S_IMODE(path_before.st_mode) == 0o444 and
                     path_before.st_nlink == 1 and
                     file_fingerprint(path_before) ==
                         file_fingerprint(self.incident_before[path]),
                     "v14 exact12 fd equals frozen path:" + str(path))
                self.incident_path_before[path] = path_before

            self.fd = self.source_fd
            self.before = self.source_before
            self.mount_id = self.source_mount_id
            self.raw = self.source_raw
            self.file_sha256 = sha_bytes(self.source_raw)
        except BaseException:
            self.close()
            raise

    @property
    def identity(self) -> tuple[int, int]:
        return (self.before.st_dev, self.before.st_ino)

    @staticmethod
    def _read_fd(descriptor: int) -> bytes:
        blocks: list[bytes] = []
        offset = 0
        while True:
            block = os.pread(descriptor, 1 << 20, offset)
            if not block:
                return b"".join(blocks)
            blocks.append(block)
            offset += len(block)

    def execution_proof(self) -> dict[str, Any]:
        return {
            "producer_exec_fd_is_fresh_sealed_memfd": True,
            "producer_exec_fd_distinct_from_installed_source_fd": True,
            "producer_exec_memfd_required_seals_valid": True,
            "producer_exec_bytes_equal_installed_source_bytes": True,
            "producer_exec_and_installed_source_terminal_replayed": True,
            "ten_incident_authority_inputs_inherited_as_held_fds": True,
            "ten_incident_held_fds_path_identity_mount_and_hash_revalidated": True,
        }

    def terminal_replay(self) -> None:
        need(self._read_fd(self.exec_fd) == self.exec_raw ==
                 self._read_fd(self.source_fd) == self.source_raw and
             file_fingerprint(os.fstat(self.exec_fd)) ==
                 file_fingerprint(self.exec_before) and
             file_fingerprint(os.fstat(self.source_fd)) ==
                 file_fingerprint(self.source_before) ==
                 file_fingerprint(SELF.lstat()) and
             int(fcntl.fcntl(self.exec_fd, F_GET_SEALS)) == self.exec_seals and
             all(self._read_fd(self.incident_fds[path]) ==
                     self.incident_raw[path] and
                 file_fingerprint(os.fstat(self.incident_fds[path])) ==
                     file_fingerprint(self.incident_before[path]) ==
                     file_fingerprint(path.lstat()) and
                 statx_mount_id(self.incident_fds[path]) ==
                     self.incident_mount_ids[path]
                 for path in self.incident_fds),
             "producer exec/source plus v14 exact12 terminal fd/path replay")
        held_by_role = {
            role: self.incident_raw[ROOT / relative]
            for role, relative, _file_pin, _object_pin in
                V14_INHERITED_AUTHORITY_EXACT12}
        need(terminal_replay_v14_inherited_authority_exact12(held_by_role) ==
                 self.v14_authority_replay,
             "producer terminal v14 exact12 semantic replay")

    def close(self) -> None:
        first_error: OSError | None = None
        for path in reversed(list(self.incident_fds)):
            descriptor = self.incident_fds.pop(path)
            try:
                os.close(descriptor)
            except OSError as exc:
                if first_error is None:
                    first_error = exc
        for name in ("source_fd", "exec_fd"):
            descriptor = getattr(self, name, -1)
            if descriptor >= 0:
                setattr(self, name, -1)
                try:
                    os.close(descriptor)
                except OSError as exc:
                    if first_error is None:
                        first_error = exc
        self.fd = -1
        if first_error is not None:
            raise first_error


class HeldPinnedInput:
    """Hold one exact observed input snapshot until terminal replay.

    ``expected_mode`` is a per-path historical fact, not an immutability or
    read-only claim.  The held fd and lexical path must retain the same bytes,
    identity, mode, link count, size, timestamps, and mount for this run.
    """

    def __init__(self, path: Path, label: str, expected_mode: int,
                 expected_sha256: str | None = None,
                 inherited_fd: int | None = None) -> None:
        self.path = path
        self.label = label
        self.expected_mode = expected_mode
        before_path = path.lstat()
        need(stat.S_ISREG(before_path.st_mode) and not path.is_symlink() and
             stat.S_IMODE(before_path.st_mode) == expected_mode and
             before_path.st_nlink == 1,
             label + ":initial exact observed regular single-link path mode")
        if inherited_fd is None:
            self.fd = openat2_beneath(path, os.O_RDONLY)
        else:
            try:
                self.fd = os.dup(inherited_fd)
            except OSError as exc:
                raise Reject(label + ":inherited held fd unavailable") from exc
        register_held_resource(self)
        self.before = os.fstat(self.fd)
        self.mount_id = statx_mount_id(self.fd)
        need(stat.S_ISREG(self.before.st_mode) and
             stat.S_IMODE(self.before.st_mode) == expected_mode and
             self.before.st_nlink == 1 and
             (self.before.st_dev, self.before.st_ino) ==
             (before_path.st_dev, before_path.st_ino),
             label + ":initial held-fd identity")
        self.raw = self._read_same_fd()
        after_fd = os.fstat(self.fd)
        after_path = path.lstat()
        need(file_fingerprint(after_fd) == file_fingerprint(self.before) ==
             file_fingerprint(before_path) and
             file_fingerprint(after_path) == file_fingerprint(self.before) and
             statx_mount_id(self.fd) == self.mount_id,
             label + ":initial same-fd read stable before/after")
        self.file_sha256 = sha_bytes(self.raw)
        if expected_sha256 is not None:
            need(self.file_sha256 == expected_sha256, label + ":file pin")

    @property
    def identity(self) -> tuple[int, int]:
        return (self.before.st_dev, self.before.st_ino)

    def _read_same_fd(self) -> bytes:
        os.lseek(self.fd, 0, os.SEEK_SET)
        blocks: list[bytes] = []
        while True:
            block = os.read(self.fd, 1 << 20)
            if not block:
                return b"".join(blocks)
            blocks.append(block)

    def terminal_replay(self) -> None:
        before_fd = os.fstat(self.fd)
        before_path = self.path.lstat()
        replay = self._read_same_fd()
        after_fd = os.fstat(self.fd)
        after_path = self.path.lstat()
        need(replay == self.raw and
             file_fingerprint(before_fd) == file_fingerprint(before_path) ==
             file_fingerprint(self.before) == file_fingerprint(after_fd) ==
             file_fingerprint(after_path) and
             stat.S_IMODE(after_fd.st_mode) == self.expected_mode and
             statx_mount_id(self.fd) == self.mount_id,
             self.label + ":same-fd terminal replay and path identity")

    def close(self) -> None:
        if self.fd >= 0:
            os.close(self.fd)
            self.fd = -1


class HeldDirectory:
    """Hold one exact observed directory snapshot for the full invocation."""

    def __init__(self, path: Path, names: set[str], required_mode: int,
                 required_nlink: int, label: str) -> None:
        self.path = path
        self.names = set(names)
        self.label = label
        self.required_mode = required_mode
        self.required_nlink = required_nlink
        self.fd = openat2_beneath(path, os.O_RDONLY | os.O_DIRECTORY)
        register_held_resource(self)
        before_path = path.lstat()
        self.before = os.fstat(self.fd)
        self.mount_id = statx_mount_id(self.fd)
        first_names = set(os.listdir(self.fd))
        after_fd = os.fstat(self.fd)
        after_path = path.lstat()
        second_names = set(os.listdir(self.fd))
        need(stat.S_ISDIR(self.before.st_mode) and
             stat.S_IMODE(self.before.st_mode) == required_mode and
             self.before.st_nlink == required_nlink and
             not path.is_symlink() and
             directory_fingerprint(before_path) == directory_fingerprint(self.before) ==
             directory_fingerprint(after_fd) == directory_fingerprint(after_path) and
             first_names == second_names == self.names and
             statx_mount_id(self.fd) == self.mount_id,
             label + ":initial held exact directory")

    @property
    def identity(self) -> tuple[int, int]:
        return (self.before.st_dev, self.before.st_ino)

    def terminal_replay(self) -> None:
        before_fd = os.fstat(self.fd)
        before_path = self.path.lstat()
        first_names = set(os.listdir(self.fd))
        after_fd = os.fstat(self.fd)
        after_path = self.path.lstat()
        second_names = set(os.listdir(self.fd))
        need(directory_fingerprint(before_fd) == directory_fingerprint(before_path) ==
             directory_fingerprint(self.before) == directory_fingerprint(after_fd) ==
             directory_fingerprint(after_path) and
             stat.S_IMODE(after_fd.st_mode) == self.required_mode and
             after_fd.st_nlink == self.required_nlink and
             statx_mount_id(self.fd) == self.mount_id and
             first_names == second_names == self.names,
             self.label + ":terminal directory identity/mount/universe")

    def close(self) -> None:
        if self.fd >= 0:
            os.close(self.fd)
            self.fd = -1


class HeldParent:
    """Hold the publication parent dirfd used for create, rename, and fsync."""

    def __init__(self, path: Path, inherited_fd: int | None = None) -> None:
        self.path = path
        self.fd = (openat2_beneath(path, os.O_RDONLY | os.O_DIRECTORY)
                   if inherited_fd is None else os.dup(inherited_fd))
        register_held_resource(self)
        before_path = path.lstat()
        self.before = os.fstat(self.fd)
        self.mount_id = statx_mount_id(self.fd)
        need(stat.S_ISDIR(self.before.st_mode) and not path.is_symlink() and
             (before_path.st_dev, before_path.st_ino) ==
                 (self.before.st_dev, self.before.st_ino),
             "held RUNTIME publication parent identity")

    def verify(self) -> None:
        after = os.fstat(self.fd)
        path_after = self.path.lstat()
        need((after.st_dev, after.st_ino) == (self.before.st_dev, self.before.st_ino) and
             (path_after.st_dev, path_after.st_ino) ==
                 (self.before.st_dev, self.before.st_ino) and
             statx_mount_id(self.fd) == self.mount_id,
             "held RUNTIME parent identity/mount stable")

    def close(self) -> None:
        if self.fd >= 0:
            os.close(self.fd)
            self.fd = -1


class HeldMutableStage:
    """Hold the hidden stage from immediately after mkdirat through commit."""

    def __init__(self, path: Path, fd: int, parent: HeldParent) -> None:
        self.path = path
        self.fd = fd
        register_held_resource(self)
        self.initial = os.fstat(fd)
        self.mount_id = statx_mount_id(fd)
        path_initial = os.stat(path.name, dir_fd=parent.fd, follow_symlinks=False)
        need(stat.S_ISDIR(self.initial.st_mode) and
             (path_initial.st_dev, path_initial.st_ino) ==
                 (self.initial.st_dev, self.initial.st_ino) and
             self.mount_id == parent.mount_id,
             "new hidden stage immediately held by exact dirfd identity/mount")
        self.final: os.stat_result | None = None
        self.names: set[str] | None = None

    @property
    def identity(self) -> tuple[int, int]:
        return (self.initial.st_dev, self.initial.st_ino)

    def seal(self, names: set[str]) -> None:
        os.fsync(self.fd)
        os.fchmod(self.fd, 0o555)
        os.fsync(self.fd)
        self.final = os.fstat(self.fd)
        self.names = set(names)
        first_names = set(os.listdir(self.fd))
        after = os.fstat(self.fd)
        second_names = set(os.listdir(self.fd))
        need(stat.S_IMODE(self.final.st_mode) == 0o555 and
             directory_fingerprint(after) == directory_fingerprint(self.final) and
             first_names == second_names == self.names,
             "hidden stage exact9 sealed 0555 on held dirfd")

    def terminal_replay(self, parent: HeldParent) -> None:
        need(self.final is not None and self.names is not None,
             "hidden stage final snapshot exists")
        before_fd = os.fstat(self.fd)
        before_path = os.stat(self.path.name, dir_fd=parent.fd, follow_symlinks=False)
        first_names = set(os.listdir(self.fd))
        after_fd = os.fstat(self.fd)
        after_path = os.stat(self.path.name, dir_fd=parent.fd, follow_symlinks=False)
        second_names = set(os.listdir(self.fd))
        need(directory_fingerprint(before_fd) == directory_fingerprint(before_path) ==
             directory_fingerprint(self.final) == directory_fingerprint(after_fd) ==
             directory_fingerprint(after_path) and
             statx_mount_id(self.fd) == self.mount_id == parent.mount_id and
             first_names == second_names == self.names,
             "hidden stage held-dirfd terminal identity/mount/universe")

    def close(self) -> None:
        if self.fd >= 0:
            os.close(self.fd)
            self.fd = -1


class HeldCreatedFile:
    """A stage member held from its O_EXCL creation until directory commit."""

    def __init__(self, path: Path, fd: int, raw: bytes) -> None:
        self.path = path
        self.fd = fd
        register_held_resource(self)
        self.raw = raw
        self.before = os.fstat(fd)
        self.mount_id = statx_mount_id(fd)
        before_path = path.lstat()
        initial_raw = self._read()
        after_fd = os.fstat(fd)
        after_path = path.lstat()
        need(stat.S_ISREG(self.before.st_mode) and
             stat.S_IMODE(self.before.st_mode) == 0o444 and self.before.st_nlink == 1,
             "created member exact 0444/nlink1")
        need(initial_raw == raw and
             file_fingerprint(before_path) == file_fingerprint(self.before) ==
             file_fingerprint(after_fd) == file_fingerprint(after_path) and
             statx_mount_id(fd) == self.mount_id,
             "created member initial same-fd byte/path/identity replay")

    @property
    def identity(self) -> tuple[int, int]:
        return (self.before.st_dev, self.before.st_ino)

    def _read(self) -> bytes:
        os.lseek(self.fd, 0, os.SEEK_SET)
        chunks: list[bytes] = []
        while True:
            block = os.read(self.fd, 1 << 20)
            if not block:
                return b"".join(chunks)
            chunks.append(block)

    def terminal_replay(self) -> None:
        before_fd = os.fstat(self.fd)
        before_path = self.path.lstat()
        replay = self._read()
        after_fd = os.fstat(self.fd)
        after_path = self.path.lstat()
        need(replay == self.raw and
             file_fingerprint(before_fd) == file_fingerprint(before_path) ==
             file_fingerprint(self.before) == file_fingerprint(after_fd) ==
             file_fingerprint(after_path) and
             statx_mount_id(self.fd) == self.mount_id,
             "created member held-fd terminal byte/path/identity/mount replay")

    def close(self) -> None:
        if self.fd >= 0:
            os.close(self.fd)
            self.fd = -1


def new_candidate_stage(outdir: Path, parent: HeldParent) -> tuple[Path, HeldMutableStage]:
    orientation = "a" if outdir == CANDIDATE_A else "b"
    name = ".c79g-v16r2r63ah-candidate-stage-" + orientation + "-" + UPSTREAM_CHECKPOINT_OBJECT_PIN
    os.mkdir(name, 0o700, dir_fd=parent.fd)
    fd = os.open(name, os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC |
                 getattr(os, "O_NOFOLLOW", 0), dir_fd=parent.fd)
    stage = RUNTIME / name
    return stage, HeldMutableStage(stage, fd, parent)


def require_candidate_target_absent(outdir: Path, parent: HeldParent) -> None:
    """Avoid a deterministic orphan when the fixed target is already installed.

    This is only an early fail-closed check.  The later renameat2
    RENAME_NOREPLACE remains the race-safe, no-clobber commit gate.
    """
    need(outdir.parent == parent.path and outdir.name not in {"", ".", ".."} and
         "/" not in outdir.name,
         "candidate target is one fixed basename under held RUNTIME parent")
    parent.verify()
    try:
        os.stat(outdir.name, dir_fd=parent.fd, follow_symlinks=False)
    except FileNotFoundError:
        return
    raise Reject(
        "candidate fixed target already exists; reject or supersede without creating stage")


def rename_candidate_noreplace(source: Path, destination: Path,
                               stage_guard: HeldMutableStage,
                               member_guards: list[HeldCreatedFile],
                               parent: HeldParent) -> None:
    """Last semantic action: bind held stage inode/mount to fixed target."""
    need(source.parent == destination.parent == parent.path and
         source.name not in {"", ".", ".."} and destination.name not in {"", ".", ".."} and
         "/" not in source.name and "/" not in destination.name,
         "candidate commit same held parent and single basenames")
    parent.verify()
    try:
        for guard in member_guards:
            guard.terminal_replay()
        stage_guard.terminal_replay(parent)
        source_before = os.stat(source.name, dir_fd=parent.fd, follow_symlinks=False)
        need((source_before.st_dev, source_before.st_ino) == stage_guard.identity and
             statx_mount_id(stage_guard.fd) == stage_guard.mount_id == parent.mount_id,
             "candidate precommit entry equals creation-held stage identity/mount")
        library = _linux_libc()
        ctypes.set_errno(0)
        outcome = library.renameat2(
            ctypes.c_int(parent.fd), ctypes.c_char_p(os.fsencode(source.name)),
            ctypes.c_int(parent.fd), ctypes.c_char_p(os.fsencode(destination.name)),
            ctypes.c_uint(RENAME_NOREPLACE))
        if outcome != 0:
            code = ctypes.get_errno()
            raise Reject("candidate renameat2 RENAME_NOREPLACE fail closed:" +
                         os.strerror(code))
        destination_after = os.stat(
            destination.name, dir_fd=parent.fd, follow_symlinks=False)
        need(stat.S_ISDIR(destination_after.st_mode) and
             (destination_after.st_dev, destination_after.st_ino) == stage_guard.identity,
             "candidate postcommit destination equals held stage identity")
        try:
            os.stat(source.name, dir_fd=parent.fd, follow_symlinks=False)
        except FileNotFoundError:
            pass
        else:
            raise Reject("candidate postcommit source did not disappear")
        os.fsync(parent.fd)
        return
    finally:
        pass


def need(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise Reject(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def sha_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def derive_v12_v5_rejection_shape_incident(
        producer_raw: bytes, consumer_raw: bytes, launcher_raw: bytes,
        v5_rejection_raw: bytes, v12_rejection_raw: bytes) -> dict[str, Any]:
    """Reproduce the frozen v12 pre-child exact39-vs-52 incident."""
    source_rows = (
        ("producer", producer_raw,
         "official v5 rejection exact canonical 39-key zero-credit closure"),
        ("consumer", consumer_raw,
         "v5 official rejection canonical singleton zero-credit envelope"),
        ("launcher", launcher_raw,
         "official v5 rejection binds published v5 exact10"),
    )
    expected_hashes = {
        "producer": V12_V5_REJECTION_SHAPE_INCIDENT["v12_producer_source_file_sha256"],
        "consumer": V12_V5_REJECTION_SHAPE_INCIDENT["v12_consumer_source_file_sha256"],
        "launcher": V12_V5_REJECTION_SHAPE_INCIDENT["v12_launcher_source_file_sha256"],
    }
    exact39_counts: dict[str, int] = {}
    wrong52_counts: dict[str, int] = {}
    for role, raw, label in source_rows:
        need(sha_bytes(raw) == expected_hashes[role],
             "frozen v12 incident source hash:" + role)
        try:
            tree = ast.parse(raw.decode("utf-8"), filename="v12_" + role)
        except (UnicodeDecodeError, SyntaxError) as exc:
            raise Reject("frozen v12 incident source AST:" + role) from exc
        owners = [
            node for node in ast.walk(tree)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and
               any(isinstance(call, ast.Call) and
                   isinstance(call.func, ast.Name) and call.func.id == "need" and
                   len(call.args) == 2 and
                   isinstance(call.args[1], ast.Constant) and
                   call.args[1].value == label for call in ast.walk(node))
        ]
        need(len(owners) == 1,
             "frozen v12 unique labelled v5 rejection gate:" + role)
        owner = owners[0]
        exact39_counts[role] = sum(
            1 for node in ast.walk(owner)
            if isinstance(node, ast.Set) and len(node.elts) == 39 and
               all(isinstance(item, ast.Constant) and isinstance(item.value, str)
                   for item in node.elts) and
               {item.value for item in node.elts} ==
                   V5_OFFICIAL_REJECTION_EXACT39_KEYS)
        wrong52_counts[role] = sum(
            1 for node in ast.walk(owner)
            if isinstance(node, ast.Compare) and
               isinstance(node.left, ast.Call) and
               isinstance(node.left.func, ast.Name) and node.left.func.id == "len" and
               len(node.left.args) == 1 and len(node.ops) ==
                   len(node.comparators) == 1 and
               isinstance(node.ops[0], ast.Eq) and
               isinstance(node.comparators[0], ast.Constant) and
               node.comparators[0].value == 52)
    need(exact39_counts == {"producer": 1, "consumer": 1, "launcher": 0} and
         wrong52_counts == {"producer": 0, "consumer": 0, "launcher": 1},
         "frozen v12 P/C exact39 versus launcher wrong52 structural witness")
    v5_rejection = strict_json(v5_rejection_raw, "frozen v5 rejection incident")
    need(isinstance(v5_rejection, dict) and
         set(v5_rejection) == V5_OFFICIAL_REJECTION_EXACT39_KEYS and
         len(v5_rejection) == 39 and
         sha_bytes(canonical(sorted(v5_rejection))) ==
             V5_OFFICIAL_REJECTION_EXACT39_KEYSET_SHA256 and
         sha_bytes(v5_rejection_raw) == V5_OFFICIAL_REJECTION_FILE_PIN and
         v5_rejection_raw == canonical(v5_rejection) + b"\n",
         "frozen v5 rejection exact39 incident bytes")
    verify_object(v5_rejection, "frozen v5 rejection incident",
                  V5_OFFICIAL_REJECTION_OBJECT_PIN)
    v12_rejection = strict_json(v12_rejection_raw, "frozen v12 rejection incident")
    need(isinstance(v12_rejection, dict) and
         set(v12_rejection) == V12_OFFICIAL_REJECTION_EXACT54_KEYS and
         len(v12_rejection) == 54 and
         sha_bytes(canonical(sorted(v12_rejection))) ==
             V12_OFFICIAL_REJECTION_EXACT54_KEYSET_SHA256 and
         sha_bytes(v12_rejection_raw) == V12_OFFICIAL_REJECTION_FILE_PIN and
         v12_rejection_raw == canonical(v12_rejection) + b"\n" and
         v12_rejection.get("formal_global_closure_credit") == 0 and
         v12_rejection.get("D02_unlock") is False and
         v12_rejection.get("D02_started") is False,
         "frozen v12 rejection exact54 zero-credit incident bytes")
    verify_object(v12_rejection, "frozen v12 rejection incident",
                  V12_OFFICIAL_REJECTION_OBJECT_PIN)
    need(sha_bytes(canonical(V12_FIRST_RUNTIME_ATTEMPT)) ==
             V12_FIRST_RUNTIME_ATTEMPT_SHA256 and
         sha_bytes(canonical(V12_V5_REJECTION_SHAPE_INCIDENT)) ==
             V12_V5_REJECTION_SHAPE_INCIDENT_SHA256,
         "v12 first-attempt and shape-incident canonical witnesses")
    return copy.deepcopy(V12_V5_REJECTION_SHAPE_INCIDENT)


HISTORICAL_REJECTION_BASE_EXACT37_KEYS = frozenset({
    "D02_formal_pending_task_count",
    "D02_gate_credit",
    "D02_started",
    "D02_task_credit",
    "D02_unlock",
    "closed_schema_file_sha256",
    "cold_launcher_file_sha256",
    "cold_manifest_file_sha256",
    "cold_outer_file_sha256",
    "cold_outer_object_sha256",
    "commit_operation",
    "consumer_file_sha256",
    "contract_file_sha256",
    "contract_object_sha256",
    "effective_checkpoint_object_sha256",
    "file_fsync_required",
    "formal_global_closure_credit",
    "idempotent_existing_recovery_re_fsyncs_rejection_file_namespace_and_runtime_parent",
    "namespace_at_rest_mode",
    "namespace_exact_path",
    "namespace_fsync_required_after_file_and_after_reseal",
    "namespace_lock_held_write_window_mode",
    "object_sha256",
    "official_writer_coordination_lock_held_for_entire_reject_command",
    "official_writer_coordination_lock_policy",
    "overwrite_delete_or_reuse_allowed",
    "partial_malformed_or_extra_namespace_entry_revokes_authority",
    "producer_file_sha256",
    "rejection_file_mode",
    "rejection_file_nlink",
    "rejection_reason",
    "runtime_parent_fsync_required_after_namespace_creation",
    "schema",
    "standalone_authority",
    "status",
    "target_exact_path",
    "target_is_protocol_and_checkpoint_deterministic",
})
HISTORICAL_REJECTION_KEYSET_STEPS = (
    (3, frozenset(), V3_REJECTION_FILE_PIN, V3_REJECTION_OBJECT_PIN,
     "21ba021c649349266d95670e63136fef1772b5d8dbb79334907c9df400620a18"),
    (5, frozenset({"v4_rejection_supersession_file_sha256",
                   "v4_rejection_supersession_object_sha256"}),
     V5_OFFICIAL_REJECTION_FILE_PIN, V5_OFFICIAL_REJECTION_OBJECT_PIN,
     V5_OFFICIAL_REJECTION_EXACT39_KEYSET_SHA256),
    (6, frozenset({"v5_official_rejection_file_sha256",
                   "v5_official_rejection_object_sha256"}),
     V6_OFFICIAL_REJECTION_FILE_PIN, V6_OFFICIAL_REJECTION_OBJECT_PIN,
     "5881a652aabef3e7e65917689487f13b99bfa60fff0ebb7c144bc02b26897638"),
    (7, frozenset({"v6_official_rejection_file_sha256",
                   "v6_official_rejection_object_sha256"}),
     V7_OFFICIAL_REJECTION_FILE_PIN, V7_OFFICIAL_REJECTION_OBJECT_PIN,
     "02b54c94602de1f5af8e545692f44815b9ac3ba334369dd96ee4e9b677bf1308"),
    (8, frozenset({"v7_official_rejection_file_sha256",
                   "v7_official_rejection_object_sha256",
                   "v7_publication_lock_continuity_incident_object_sha256"}),
     V8_OFFICIAL_REJECTION_FILE_PIN, V8_OFFICIAL_REJECTION_OBJECT_PIN,
     "a1da14307b813345ee0f8877550412b40951f7857e5972570ab41f97e2fe31bf"),
    (9, frozenset({"v8_official_rejection_file_sha256",
                   "v8_official_rejection_object_sha256"}),
     V9_OFFICIAL_REJECTION_FILE_PIN, V9_OFFICIAL_REJECTION_OBJECT_PIN,
     "d0617183e15fd4c5bfd3495d7dca56cb9aea7035bedf35a1bdf6efd166a70308"),
    (10, frozenset({"v9_official_rejection_file_sha256",
                    "v9_official_rejection_object_sha256"}),
     V10_OFFICIAL_REJECTION_FILE_PIN, V10_OFFICIAL_REJECTION_OBJECT_PIN,
     "01274ec0c36bd85423d385bdb22cdff7fe6ccfe2d114864994fc2ead2153eddb"),
    (11, frozenset({"v10_official_rejection_file_sha256",
                    "v10_official_rejection_object_sha256"}),
     V11_OFFICIAL_REJECTION_FILE_PIN, V11_OFFICIAL_REJECTION_OBJECT_PIN,
     "75ca9378fbff7a6956686e7390556fffa3d6ff939630ed47e8c8c185872e97f8"),
    (12, frozenset({"v11_official_rejection_file_sha256",
                    "v11_official_rejection_object_sha256"}),
     V12_OFFICIAL_REJECTION_FILE_PIN, V12_OFFICIAL_REJECTION_OBJECT_PIN,
     V12_OFFICIAL_REJECTION_EXACT54_KEYSET_SHA256),
)

HISTORICAL_REJECTION_V3_KEYS = HISTORICAL_REJECTION_BASE_EXACT37_KEYS
HISTORICAL_REJECTION_V5_KEYS = (
    HISTORICAL_REJECTION_V3_KEYS | frozenset({
        "v4_rejection_supersession_file_sha256",
        "v4_rejection_supersession_object_sha256",
    }))
HISTORICAL_REJECTION_V6_KEYS = (
    HISTORICAL_REJECTION_V5_KEYS | frozenset({
        "v5_official_rejection_file_sha256",
        "v5_official_rejection_object_sha256",
    }))
HISTORICAL_REJECTION_V7_KEYS = (
    HISTORICAL_REJECTION_V6_KEYS | frozenset({
        "v6_official_rejection_file_sha256",
        "v6_official_rejection_object_sha256",
    }))
HISTORICAL_REJECTION_V8_KEYS = (
    HISTORICAL_REJECTION_V7_KEYS | frozenset({
        "v7_official_rejection_file_sha256",
        "v7_official_rejection_object_sha256",
        "v7_publication_lock_continuity_incident_object_sha256",
    }))
HISTORICAL_REJECTION_V9_KEYS = (
    HISTORICAL_REJECTION_V8_KEYS | frozenset({
        "v8_official_rejection_file_sha256",
        "v8_official_rejection_object_sha256",
    }))
HISTORICAL_REJECTION_V10_KEYS = (
    HISTORICAL_REJECTION_V9_KEYS | frozenset({
        "v9_official_rejection_file_sha256",
        "v9_official_rejection_object_sha256",
    }))
HISTORICAL_REJECTION_V11_KEYS = (
    HISTORICAL_REJECTION_V10_KEYS | frozenset({
        "v10_official_rejection_file_sha256",
        "v10_official_rejection_object_sha256",
    }))
HISTORICAL_REJECTION_V12_KEYS = (
    HISTORICAL_REJECTION_V11_KEYS | frozenset({
        "v11_official_rejection_file_sha256",
        "v11_official_rejection_object_sha256",
    }))


def _build_historical_rejection_exact_keyset_witness(
        ) -> tuple[dict[str, Any], ...]:
    keys = HISTORICAL_REJECTION_BASE_EXACT37_KEYS
    rows: list[dict[str, Any]] = []
    for version, additions, file_pin, object_pin, keyset_digest in \
            HISTORICAL_REJECTION_KEYSET_STEPS:
        keys = keys | additions
        sorted_keys = sorted(keys)
        need(sha_bytes(canonical(sorted_keys)) == keyset_digest,
             "historical rejection exact keyset digest:v" + str(version))
        rows.append({
            "version": "v" + str(version),
            "path": ".cm2-runtime/c79g-v" + str(version) + "-rejections-" +
                    UPSTREAM_CHECKPOINT_OBJECT_PIN + "/rejection.json",
            "file_sha256": file_pin,
            "object_sha256": object_pin,
            "key_count": len(sorted_keys),
            "sorted_keys": sorted_keys,
            "sorted_key_array_sha256": keyset_digest,
            "canonical_object_closed": True,
        })
    need([row["version"] for row in rows] ==
             ["v3", "v5", "v6", "v7", "v8", "v9", "v10", "v11", "v12"] and
         [row["key_count"] for row in rows] ==
             [37, 39, 41, 43, 46, 48, 50, 52, 54],
         "historical rejection exact ordered nine-row keyset witness")
    return tuple(rows)


HISTORICAL_REJECTION_EXACT_KEYSET_WITNESS = (
    {
        "version": "v3",
        "path": ".cm2-runtime/c79g-v3-rejections-" +
                UPSTREAM_CHECKPOINT_OBJECT_PIN + "/rejection.json",
        "file_sha256": V3_REJECTION_FILE_PIN,
        "object_sha256": V3_REJECTION_OBJECT_PIN,
        "key_count": 37,
        "sorted_keys": sorted(HISTORICAL_REJECTION_V3_KEYS),
        "sorted_key_array_sha256":
            "21ba021c649349266d95670e63136fef1772b5d8dbb79334907c9df400620a18",
        "canonical_object_closed": True,
    },
    {
        "version": "v5",
        "path": ".cm2-runtime/c79g-v5-rejections-" +
                UPSTREAM_CHECKPOINT_OBJECT_PIN + "/rejection.json",
        "file_sha256": V5_OFFICIAL_REJECTION_FILE_PIN,
        "object_sha256": V5_OFFICIAL_REJECTION_OBJECT_PIN,
        "key_count": 39,
        "sorted_keys": sorted(HISTORICAL_REJECTION_V5_KEYS),
        "sorted_key_array_sha256": V5_OFFICIAL_REJECTION_EXACT39_KEYSET_SHA256,
        "canonical_object_closed": True,
    },
    {
        "version": "v6",
        "path": ".cm2-runtime/c79g-v6-rejections-" +
                UPSTREAM_CHECKPOINT_OBJECT_PIN + "/rejection.json",
        "file_sha256": V6_OFFICIAL_REJECTION_FILE_PIN,
        "object_sha256": V6_OFFICIAL_REJECTION_OBJECT_PIN,
        "key_count": 41,
        "sorted_keys": sorted(HISTORICAL_REJECTION_V6_KEYS),
        "sorted_key_array_sha256":
            "5881a652aabef3e7e65917689487f13b99bfa60fff0ebb7c144bc02b26897638",
        "canonical_object_closed": True,
    },
    {
        "version": "v7",
        "path": ".cm2-runtime/c79g-v7-rejections-" +
                UPSTREAM_CHECKPOINT_OBJECT_PIN + "/rejection.json",
        "file_sha256": V7_OFFICIAL_REJECTION_FILE_PIN,
        "object_sha256": V7_OFFICIAL_REJECTION_OBJECT_PIN,
        "key_count": 43,
        "sorted_keys": sorted(HISTORICAL_REJECTION_V7_KEYS),
        "sorted_key_array_sha256":
            "02b54c94602de1f5af8e545692f44815b9ac3ba334369dd96ee4e9b677bf1308",
        "canonical_object_closed": True,
    },
    {
        "version": "v8",
        "path": ".cm2-runtime/c79g-v8-rejections-" +
                UPSTREAM_CHECKPOINT_OBJECT_PIN + "/rejection.json",
        "file_sha256": V8_OFFICIAL_REJECTION_FILE_PIN,
        "object_sha256": V8_OFFICIAL_REJECTION_OBJECT_PIN,
        "key_count": 46,
        "sorted_keys": sorted(HISTORICAL_REJECTION_V8_KEYS),
        "sorted_key_array_sha256":
            "a1da14307b813345ee0f8877550412b40951f7857e5972570ab41f97e2fe31bf",
        "canonical_object_closed": True,
    },
    {
        "version": "v9",
        "path": ".cm2-runtime/c79g-v9-rejections-" +
                UPSTREAM_CHECKPOINT_OBJECT_PIN + "/rejection.json",
        "file_sha256": V9_OFFICIAL_REJECTION_FILE_PIN,
        "object_sha256": V9_OFFICIAL_REJECTION_OBJECT_PIN,
        "key_count": 48,
        "sorted_keys": sorted(HISTORICAL_REJECTION_V9_KEYS),
        "sorted_key_array_sha256":
            "d0617183e15fd4c5bfd3495d7dca56cb9aea7035bedf35a1bdf6efd166a70308",
        "canonical_object_closed": True,
    },
    {
        "version": "v10",
        "path": ".cm2-runtime/c79g-v10-rejections-" +
                UPSTREAM_CHECKPOINT_OBJECT_PIN + "/rejection.json",
        "file_sha256": V10_OFFICIAL_REJECTION_FILE_PIN,
        "object_sha256": V10_OFFICIAL_REJECTION_OBJECT_PIN,
        "key_count": 50,
        "sorted_keys": sorted(HISTORICAL_REJECTION_V10_KEYS),
        "sorted_key_array_sha256":
            "01274ec0c36bd85423d385bdb22cdff7fe6ccfe2d114864994fc2ead2153eddb",
        "canonical_object_closed": True,
    },
    {
        "version": "v11",
        "path": ".cm2-runtime/c79g-v11-rejections-" +
                UPSTREAM_CHECKPOINT_OBJECT_PIN + "/rejection.json",
        "file_sha256": V11_OFFICIAL_REJECTION_FILE_PIN,
        "object_sha256": V11_OFFICIAL_REJECTION_OBJECT_PIN,
        "key_count": 52,
        "sorted_keys": sorted(HISTORICAL_REJECTION_V11_KEYS),
        "sorted_key_array_sha256":
            "75ca9378fbff7a6956686e7390556fffa3d6ff939630ed47e8c8c185872e97f8",
        "canonical_object_closed": True,
    },
    {
        "version": "v12",
        "path": ".cm2-runtime/c79g-v12-rejections-" +
                UPSTREAM_CHECKPOINT_OBJECT_PIN + "/rejection.json",
        "file_sha256": V12_OFFICIAL_REJECTION_FILE_PIN,
        "object_sha256": V12_OFFICIAL_REJECTION_OBJECT_PIN,
        "key_count": 54,
        "sorted_keys": sorted(HISTORICAL_REJECTION_V12_KEYS),
        "sorted_key_array_sha256": V12_OFFICIAL_REJECTION_EXACT54_KEYSET_SHA256,
        "canonical_object_closed": True,
    },
)


def digest(value: Any) -> str:
    return sha_bytes(canonical(value))


def close_row(body: dict[str, Any]) -> dict[str, Any]:
    need("row_sha256" not in body, "row already closed")
    return {**body, "row_sha256": digest(body)}


def close_object(body: dict[str, Any]) -> dict[str, Any]:
    need("object_sha256" not in body, "object already closed")
    return {**body, "object_sha256": digest(body)}


def verify_row(row: Mapping[str, Any], label: str) -> None:
    body = copy.deepcopy(dict(row))
    claim = body.pop("row_sha256", None)
    need(isinstance(claim, str) and claim == digest(body), label + ":row closure")


def verify_object(value: Mapping[str, Any], label: str, pin: str | None = None) -> None:
    body = copy.deepcopy(dict(value))
    claim = body.pop("object_sha256", None)
    need(isinstance(claim, str) and claim == digest(body), label + ":object closure")
    if pin is not None:
        need(claim == pin, label + ":object pin")


def strict_json(raw: bytes, label: str) -> Any:
    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        out: dict[str, Any] = {}
        for key, value in items:
            need(key not in out, label + ":duplicate key:" + key)
            out[key] = value
        return out
    try:
        return json.loads(
            raw,
            object_pairs_hook=pairs,
            parse_constant=lambda token: (_ for _ in ()).throw(Reject(label + ":" + token)),
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise Reject(label + ":strict JSON") from exc


def _annotation_is_bool(annotation: ast.AST | None) -> bool:
    return isinstance(annotation, ast.Name) and annotation.id == "bool"


def _strict_bool_symbol_tables(
        tree: ast.AST) -> tuple[set[str], set[str], set[str]]:
    """Infer only symbols whose exact built-in-bool type is statically closed."""
    bool_functions: set[str] = set()
    bool_names: set[str] = set()
    # zlib.decompressobj.eof is a documented built-in bool property.  Every
    # other attribute enters this set only through an exact bool assignment or
    # annotation present in the audited source itself.
    bool_attributes: set[str] = {"eof"}
    for node in ast.walk(tree):
        if (isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and
                _annotation_is_bool(node.returns)):
            bool_functions.add(node.name)
        if (isinstance(node, ast.Assign) and isinstance(node.value, ast.Constant) and
                type(node.value.value) is bool):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    bool_names.add(target.id)
                elif isinstance(target, ast.Attribute):
                    bool_attributes.add(target.attr)
        if isinstance(node, ast.AnnAssign) and _annotation_is_bool(node.annotation):
            if isinstance(node.target, ast.Name):
                bool_names.add(node.target.id)
            elif isinstance(node.target, ast.Attribute):
                bool_attributes.add(node.target.attr)
    return bool_functions, bool_names, bool_attributes


def _strict_bool_expression_is_proved(
        node: ast.AST, bool_functions: set[str], bool_names: set[str],
        bool_attributes: set[str]) -> bool:
    """Recursively prove that an expression returns exact ``bool``.

    This deliberately rejects Python truthiness.  In particular, every operand
    of ``and``/``or`` must itself be exact-bool; a guarded nonempty tuple,
    bytes, string, or dict is not accepted merely because it is truthy.
    """
    if isinstance(node, ast.Compare):
        return True
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.Not):
        return True
    if isinstance(node, ast.BoolOp):
        return all(_strict_bool_expression_is_proved(
            item, bool_functions, bool_names, bool_attributes)
                   for item in node.values)
    if isinstance(node, ast.Constant):
        return type(node.value) is bool
    if isinstance(node, ast.IfExp):
        return (_strict_bool_expression_is_proved(
                    node.body, bool_functions, bool_names, bool_attributes) and
                _strict_bool_expression_is_proved(
                    node.orelse, bool_functions, bool_names, bool_attributes))
    if isinstance(node, ast.NamedExpr):
        return _strict_bool_expression_is_proved(
            node.value, bool_functions, bool_names, bool_attributes)
    if isinstance(node, ast.Name):
        return node.id in bool_names
    if isinstance(node, ast.Attribute):
        return node.attr in bool_attributes
    if isinstance(node, ast.Call):
        if isinstance(node.func, ast.Name):
            return (node.func.id in _STRICT_BOOL_CALL_NAMES or
                    node.func.id in bool_functions)
        if isinstance(node.func, ast.Attribute):
            if (node.func.attr in _STRICT_BOOL_METHOD_NAMES or
                    node.func.attr in bool_functions or
                    node.func.attr.startswith("S_IS")):
                return True
            # A literal bool dispatch table with a bool default is exact-bool.
            if (node.func.attr == "get" and isinstance(node.func.value, ast.Dict) and
                    len(node.args) == 2 and
                    all(_strict_bool_expression_is_proved(
                        value, bool_functions, bool_names, bool_attributes)
                        for value in node.func.value.values) and
                    _strict_bool_expression_is_proved(
                        node.args[1], bool_functions, bool_names, bool_attributes)):
                return True
    return False


def _strict_bool_need_census(raw: bytes, role: str) -> dict[str, Any]:
    """AST-parse, in-memory compile, and census every direct strict ``need``."""
    try:
        source = raw.decode("utf-8")
        tree = ast.parse(source, filename=role, mode="exec")
        compiled = compile(source, role, "exec", dont_inherit=True, optimize=0)
    except (UnicodeDecodeError, SyntaxError, ValueError, TypeError) as exc:
        raise Reject("static AST/in-memory compile:" + role) from exc
    del compiled
    bool_functions, bool_names, bool_attributes = _strict_bool_symbol_tables(tree)

    # A bool annotation is not trusted blindly: every explicit return in each
    # such function must itself pass the same recursive exact-bool proof.
    annotated_return_failures: list[dict[str, Any]] = []
    for function in ast.walk(tree):
        if not (isinstance(function, (ast.FunctionDef, ast.AsyncFunctionDef)) and
                function.name in bool_functions):
            continue
        for returned in ast.walk(function):
            if (isinstance(returned, ast.Return) and returned.value is not None and
                    not _strict_bool_expression_is_proved(
                        returned.value, bool_functions, bool_names, bool_attributes)):
                annotated_return_failures.append({
                    "function": function.name,
                    "line": returned.lineno,
                    "expression": ast.unparse(returned.value),
                })

    calls = [
        node for node in ast.walk(tree)
        if (isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and
            node.func.id == "need")
    ]
    arity_failures: list[dict[str, Any]] = []
    unproved: list[dict[str, Any]] = []
    for call in calls:
        if (len(call.args) != 2 or len(call.keywords) != 0 or
                any(isinstance(argument, ast.Starred) for argument in call.args)):
            arity_failures.append({"line": call.lineno, "column": call.col_offset})
            continue
        condition = call.args[0]
        if not _strict_bool_expression_is_proved(
                condition, bool_functions, bool_names, bool_attributes):
            unproved.append({
                "role": role,
                "line": call.lineno,
                "column": call.col_offset,
                "expression": ast.unparse(condition),
                "condition_ast_sha256": sha_bytes(
                    ast.dump(condition, annotate_fields=True,
                             include_attributes=False).encode("utf-8")),
            })
    unproved.sort(key=lambda row: (row["line"], row["column"]))
    annotated_return_failures.sort(
        key=lambda row: (row["function"], row["line"], row["expression"]))
    return {
        "role": role,
        "AST_parsed": True,
        "compiled_in_memory": True,
        "compiled_code_executed": False,
        "direct_need_call_count": len(calls),
        "arity_star_or_keyword_failure_count": len(arity_failures),
        "annotated_bool_return_failure_count": len(annotated_return_failures),
        "annotated_bool_return_failures": annotated_return_failures,
        "recursive_exact_bool_unproved_count": len(unproved),
        "recursive_exact_bool_unproved": unproved,
    }


def strict_bool_predecessor_and_successor_census(
        v5_sources: Mapping[str, bytes],
        v6_sources: Mapping[str, bytes],
        v7_sources: Mapping[str, bytes],
        v16r2_sources: Mapping[str, bytes]) -> dict[str, Any]:
    """Prove frozen v5 defects and zero-unsafe complete v6/v7/v16r2 boxes."""
    v5_roles = ("producer_v5", "consumer_v5", "launcher_v5")
    v6_roles = ("producer_v6", "consumer_v6", "launcher_v6")
    v7_roles = ("producer_v7", "consumer_v7", "launcher_v7")
    v16r2_roles = ("producer_v16r2", "consumer_v16r2", "launcher_v16r2")
    need(set(v5_sources) == set(v5_roles) and
         set(v6_sources) == set(v6_roles) and
         set(v7_sources) == set(v7_roles) and
         set(v16r2_sources) == set(v16r2_roles),
         "strict-bool source role closure")
    v5 = {role: _strict_bool_need_census(v5_sources[role], role)
          for role in v5_roles}
    v6 = {role: _strict_bool_need_census(v6_sources[role], role)
          for role in v6_roles}
    v7 = {role: _strict_bool_need_census(v7_sources[role], role)
          for role in v7_roles}
    v16r2 = {role: _strict_bool_need_census(v16r2_sources[role], role)
          for role in v16r2_roles}
    need({role: v5[role]["direct_need_call_count"] for role in v5_roles} == {
             "producer_v5": 217, "consumer_v5": 345, "launcher_v5": 138,
         } and
         sum(v5[role]["direct_need_call_count"] for role in v5_roles) ==
             V5_DIRECT_NEED_CALL_COUNT and
         sum(v5[role]["arity_star_or_keyword_failure_count"] for role in v5_roles) == 0 and
         sum(v5[role]["annotated_bool_return_failure_count"] for role in v5_roles) == 0,
         "frozen v5 exact 700 direct need calls and recursive annotation closure")
    observed_v5 = {
        (role, row["line"], row["expression"])
        for role in v5_roles for row in v5[role]["recursive_exact_bool_unproved"]
    }
    expected_v5 = {(role, line, expression)
                   for _, role, line, expression in V5_STRICT_BOOL_RISK_SPECS}
    need(observed_v5 == expected_v5 and len(observed_v5) == 7,
         "frozen v5 exact seven recursive strict-bool risks present")
    v6_unproved = sum(
        v6[role]["recursive_exact_bool_unproved_count"] for role in v6_roles)
    v6_arity = sum(
        v6[role]["arity_star_or_keyword_failure_count"] for role in v6_roles)
    v6_returns = sum(
        v6[role]["annotated_bool_return_failure_count"] for role in v6_roles)
    v7_unproved = sum(
        v7[role]["recursive_exact_bool_unproved_count"] for role in v7_roles)
    v7_arity = sum(
        v7[role]["arity_star_or_keyword_failure_count"] for role in v7_roles)
    v7_returns = sum(
        v7[role]["annotated_bool_return_failure_count"] for role in v7_roles)
    v16r2_unproved = sum(
        v16r2[role]["recursive_exact_bool_unproved_count"] for role in v16r2_roles)
    v16r2_arity = sum(
        v16r2[role]["arity_star_or_keyword_failure_count"] for role in v16r2_roles)
    v16r2_returns = sum(
        v16r2[role]["annotated_bool_return_failure_count"] for role in v16r2_roles)
    need(v6_unproved == 0 and v6_arity == 0 and v6_returns == 0 and
         v7_unproved == 0 and v7_arity == 0 and v7_returns == 0 and
         v16r2_unproved == 0 and v16r2_arity == 0 and v16r2_returns == 0,
         "v6/v7/v16r2 recursive exact-bool full boxes have zero unsafe or unproved sites")
    return {
        "direct_need_call_count": V5_DIRECT_NEED_CALL_COUNT,
        "risk_count": len(V5_STRICT_BOOL_RISK_IDS),
        "hard_defect_count": len(V5_HARD_STRICT_BOOL_DEFECT_IDS),
        "ordered_risk_ids": list(V5_STRICT_BOOL_RISK_IDS),
        "hard_defect_ids": list(V5_HARD_STRICT_BOOL_DEFECT_IDS),
        "all_seven_present_in_v5": True,
        "same_seven_absent_from_v6": True,
        "same_seven_absent_from_v7": True,
        "same_seven_absent_from_v16r2": True,
        "v5_recursive_exact_bool_unproved_count": len(observed_v5),
        "v6_recursive_exact_bool_unproved_count": v6_unproved,
        "v7_recursive_exact_bool_unproved_count": v7_unproved,
        "v16r2_recursive_exact_bool_unproved_count": v16r2_unproved,
        "v5_need_call_count_by_role": {
            role: v5[role]["direct_need_call_count"] for role in v5_roles},
        "v6_direct_need_call_count": sum(
            v6[role]["direct_need_call_count"] for role in v6_roles),
        "v7_direct_need_call_count": sum(
            v7[role]["direct_need_call_count"] for role in v7_roles),
        "v16r2_direct_need_call_count": sum(
            v16r2[role]["direct_need_call_count"] for role in v16r2_roles),
        "all_six_sources_AST_parsed_and_compiled_in_memory": True,
        "all_nine_sources_AST_parsed_and_compiled_in_memory": True,
        "all_twelve_sources_AST_parsed_and_compiled_in_memory": True,
        "compiled_code_executed": False,
    }


def _v5_published_exact10_records() -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for name, (path, file_pin, object_pin) in zip(
            V5_PUBLISHED_EXACT10_NAMES, V5_PUBLISHED_EXACT10_PINS, strict=True):
        record: dict[str, Any] = {
            "name": name,
            "path": str(path.relative_to(ROOT)),
            "file_sha256": file_pin,
        }
        if object_pin is not None:
            record["object_sha256"] = object_pin
        records.append(record)
    return records


def _v6_published_exact10_records() -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for name, (path, file_pin, object_pin) in zip(
            V6_PUBLISHED_EXACT10_NAMES, V6_PUBLISHED_EXACT10_PINS, strict=True):
        record: dict[str, Any] = {
            "name": name,
            "path": str(path.relative_to(ROOT)),
            "file_sha256": file_pin,
        }
        if object_pin is not None:
            record["object_sha256"] = object_pin
        records.append(record)
    return records


def _v7_published_exact10_records() -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for name, (path, file_pin, object_pin) in zip(
            V7_PUBLISHED_EXACT10_NAMES, V7_PUBLISHED_EXACT10_PINS, strict=True):
        record: dict[str, Any] = {
            "name": name,
            "path": str(path.relative_to(ROOT)),
            "file_sha256": file_pin,
        }
        if object_pin is not None:
            record["object_sha256"] = object_pin
        records.append(record)
    return records


def _v8_published_exact10_records() -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for name, (path, file_pin, object_pin) in zip(
            V8_PUBLISHED_EXACT10_NAMES, V8_PUBLISHED_EXACT10_PINS, strict=True):
        record: dict[str, Any] = {
            "name": name,
            "path": str(path.relative_to(ROOT)),
            "file_sha256": file_pin,
        }
        if object_pin is not None:
            record["object_sha256"] = object_pin
        records.append(record)
    return records


def _v9_published_exact10_records() -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for name, (path, file_pin, object_pin) in zip(
            V9_PUBLISHED_EXACT10_NAMES, V9_PUBLISHED_EXACT10_PINS, strict=True):
        record: dict[str, Any] = {
            "name": name,
            "path": str(path.relative_to(ROOT)),
            "file_sha256": file_pin,
        }
        if object_pin is not None:
            record["object_sha256"] = object_pin
        records.append(record)
    return records


def _v10_published_exact10_records() -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for name, (path, file_pin, object_pin) in zip(
            V10_PUBLISHED_EXACT10_NAMES, V10_PUBLISHED_EXACT10_PINS, strict=True):
        record: dict[str, Any] = {
            "name": name,
            "path": str(path.relative_to(ROOT)),
            "file_sha256": file_pin,
        }
        if object_pin is not None:
            record["object_sha256"] = object_pin
        records.append(record)
    return records


def _v11_published_exact10_records() -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for name, (path, file_pin, object_pin) in zip(
            V11_PUBLISHED_EXACT10_NAMES, V11_PUBLISHED_EXACT10_PINS, strict=True):
        record: dict[str, Any] = {
            "name": name,
            "path": str(path.relative_to(ROOT)),
            "file_sha256": file_pin,
        }
        if object_pin is not None:
            record["object_sha256"] = object_pin
        records.append(record)
    return records


def _v12_published_exact10_records() -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for name, (path, file_pin, object_pin) in zip(
            V12_PUBLISHED_EXACT10_NAMES, V12_PUBLISHED_EXACT10_PINS,
            strict=True):
        record: dict[str, Any] = {
            "name": name,
            "path": str(path.relative_to(ROOT)),
            "file_sha256": file_pin,
        }
        if object_pin is not None:
            record["object_sha256"] = object_pin
        records.append(record)
    return records


def _v8_common_official_rejection_fields() -> dict[str, Any]:
    return {
        "path": str(V8_OFFICIAL_REJECTION.relative_to(ROOT)),
        "namespace_path": str(V8_OFFICIAL_REJECTION_NAMESPACE.relative_to(ROOT)),
        "file_sha256": V8_OFFICIAL_REJECTION_FILE_PIN,
        "object_sha256": V8_OFFICIAL_REJECTION_OBJECT_PIN,
        "schema":
            "cm2.round306c79g.true-global-no-producer-consumer.v8.later-rejection",
        "status": "PERMANENT_FAIL_CLOSED_REJECTION__ZERO_CREDIT",
        "reason": "ORPHANED_OR_INCOMPLETE_C79G_V8_SURFACE",
        "namespace_mode": "0555",
        "namespace_nlink": 2,
        "member_mode": "0444",
        "member_nlink": 1,
        "exact_member_universe": ["rejection.json"],
        "formal_global_closure_credit": 0,
        "D02_unlock": False,
        "D02_gate_credit": 0,
        "D02_task_credit": 0,
        "D02_formal_pending_task_count": EXPECTED_PENDING_D02,
        "D02_started": False,
        "overwrite_delete_or_reuse_allowed": False,
    }


def _validate_ordered_v8_exact10(records: Any, label: str) -> None:
    expected = _v8_published_exact10_records()
    need(isinstance(records, list) and len(records) == len(expected),
         label + ":ordered published exact10 count")
    for index, (observed, pinned) in enumerate(zip(records, expected, strict=True)):
        need(isinstance(observed, dict) and
             observed.get("name") == pinned["name"] and
             observed.get("path") == pinned["path"] and
             observed.get("file_sha256") == pinned["file_sha256"] and
             observed.get("object_sha256") == pinned.get("object_sha256"),
             label + ":ordered published exact10 pin:" + str(index))


def v6_held_self_identity_defect_regression(raw: bytes) -> dict[str, Any]:
    """Prove the complete frozen-v6 identity defect without executing it.

    V8 incorrectly counted the whole function and required one occurrence.
    V16R2 first proves the complete three-site census, then independently locates
    the only ``current_cold_ten_guards`` trigger at frozen line 2041.
    """
    try:
        tree = ast.parse(raw.decode("utf-8"), filename="producer_v6", mode="exec")
    except (UnicodeDecodeError, SyntaxError) as exc:
        raise Reject("frozen v6 producer AST parse") from exc
    held_self = next(
        (node for node in tree.body
         if isinstance(node, ast.ClassDef) and node.name == "HeldSelf"), None)
    hold = next(
        (node for node in tree.body
         if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and
            node.name == "hold_static_freeze_trust"), None)
    need(isinstance(held_self, ast.ClassDef) and
         isinstance(hold, (ast.FunctionDef, ast.AsyncFunctionDef)),
         "frozen v6 HeldSelf and hold_static_freeze_trust definitions")
    direct_methods = {
        node.name for node in held_self.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }
    guard_identity_nodes = [
        node for node in ast.walk(hold)
        if isinstance(node, ast.Attribute) and node.attr == "identity" and
           isinstance(node.value, ast.Name) and node.value.id == "guard"]
    structured_sites: list[tuple[str, ast.Call, ast.Attribute]] = []
    for node in ast.walk(hold):
        if not (isinstance(node, ast.Call) and
                isinstance(node.func, ast.Name) and node.func.id == "len" and
                len(node.args) == 1 and not node.keywords and
                isinstance(node.args[0], ast.SetComp)):
            continue
        comp = node.args[0]
        if not (isinstance(comp.elt, ast.Attribute) and
                comp.elt.attr == "identity" and
                isinstance(comp.elt.value, ast.Name) and
                comp.elt.value.id == "guard" and
                len(comp.generators) == 1):
            continue
        generator = comp.generators[0]
        if (isinstance(generator.target, ast.Name) and
                generator.target.id == "guard" and
                isinstance(generator.iter, ast.Name) and
                not generator.ifs and generator.is_async == 0):
            structured_sites.append(
                (generator.iter.id, node, comp.elt))
    expected_iterables = {
        "current_cold_ten_guards", "v5_guards", "all_file_guards"}
    structured_identity_nodes = {id(site[2]) for site in structured_sites}
    current_ten_triggers = [
        site for site in structured_sites
        if site[0] == "current_cold_ten_guards"]
    need("identity" not in direct_methods and
         len(guard_identity_nodes) == 3 and
         len(structured_sites) == 3 and
         {site[0] for site in structured_sites} == expected_iterables and
         {id(node) for node in guard_identity_nodes} == structured_identity_nodes and
         len(current_ten_triggers) == 1 and
         isinstance(current_ten_triggers[0][1], ast.Call),
         "frozen v6 HeldSelf.identity missing; normalized AST proves the exact "
         "three-site iterable census and sole current_cold_ten_guards trigger")
    # Frozen line numbers remain diagnostic receipt fields.  Authority comes
    # from the normalized AST shape above, never from source-line equality.
    return copy.deepcopy(V6_LAUNCHER_EXPANDED_STRUCTURAL_EVIDENCE)


def v9_prechild_shape_drift_regression(
        contract_raw: bytes, launcher_raw: bytes,
        structural_evidence: Mapping[str, Any]) -> dict[str, Any]:
    """Reproduce the rejected v9 9-key/16-key prechild mismatch statically."""
    contract = strict_json(contract_raw, "frozen v9 contract shape-drift proof")
    need(isinstance(contract, dict), "frozen v9 contract is an object")
    predecessor = contract.get(
        "published_then_officially_rejected_predecessor_v6", {})
    persisted = predecessor.get("held_self_identity_defect", {})
    launcher_expected = copy.deepcopy(predecessor)
    launcher_expected["held_self_identity_defect"] = copy.deepcopy(
        dict(structural_evidence))
    need(isinstance(predecessor, dict) and isinstance(persisted, dict) and
         persisted == V6_PERSISTED_HELD_SELF_IDENTITY_DEFECT and
         len(persisted) == 9 and
         structural_evidence == V6_LAUNCHER_EXPANDED_STRUCTURAL_EVIDENCE and
         len(structural_evidence) == 16 and
         sha_bytes(canonical(predecessor)) ==
             V9_V6_DEFECT_SHAPE_DRIFT_INCIDENT[
                 "contract_v9_predecessor_v6_full_canonical_sha256"] and
         sha_bytes(canonical(persisted)) ==
             V9_V6_DEFECT_SHAPE_DRIFT_INCIDENT[
                 "contract_v9_persisted_defect_nested_canonical_sha256"] and
         sha_bytes(canonical(launcher_expected)) ==
             V9_V6_DEFECT_SHAPE_DRIFT_INCIDENT[
                 "launcher_v9_predecessor_v6_full_canonical_sha256"] and
         sha_bytes(canonical(structural_evidence)) ==
             V9_V6_DEFECT_SHAPE_DRIFT_INCIDENT[
                 "launcher_v9_expanded_defect_nested_canonical_sha256"],
         "frozen v9 contract canonical9 and reconstructed launcher16 digests")
    try:
        tree = ast.parse(
            launcher_raw.decode("utf-8"), filename="cold_launcher_v9", mode="exec")
    except (UnicodeDecodeError, SyntaxError) as exc:
        raise Reject("frozen v9 launcher AST parse") from exc
    expected_function = next(
        (node for node in tree.body
         if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and
            node.name == "expected_v6_published_rejected_segment"), None)
    validator = next(
        (node for node in tree.body
         if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and
            node.name == "validate_v6_published_rejected_segment"), None)
    need(isinstance(expected_function, (ast.FunctionDef, ast.AsyncFunctionDef)) and
         isinstance(validator, (ast.FunctionDef, ast.AsyncFunctionDef)),
         "frozen v9 launcher expected/validator v6 functions")
    expanded_dicts: list[ast.Dict] = []
    for node in ast.walk(expected_function):
        if not isinstance(node, ast.Dict):
            continue
        keys = [
            key.value for key in node.keys
            if isinstance(key, ast.Constant) and isinstance(key.value, str)
        ]
        if set(keys) == set(V6_LAUNCHER_EXPANDED_STRUCTURAL_EVIDENCE):
            expanded_dicts.append(node)
    validator_calls = [
        node for node in ast.walk(validator)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and
           node.func.id == "expected_v6_published_rejected_segment"
    ]
    equality_gates = [
        node for node in ast.walk(validator)
        if isinstance(node, ast.Compare) and
           any(isinstance(operator, ast.Eq) for operator in node.ops)
    ]
    constants = {
        node.value for node in ast.walk(tree)
        if isinstance(node, ast.Constant) and isinstance(node.value, str)
    }
    failure_label = V9_V6_DEFECT_SHAPE_DRIFT_INCIDENT["failure_label"]
    need(len(expanded_dicts) == 1 and len(expanded_dicts[0].keys) == 16 and
         len(validator_calls) == 1 and bool(equality_gates) and
         ":" + failure_label in constants and
         sha_bytes(launcher_raw) == V9_PUBLISHED_EXACT10_PINS[7][1],
         "frozen v9 launcher statically embeds structural16 in exact equality gate")
    return copy.deepcopy(V9_V6_DEFECT_SHAPE_DRIFT_INCIDENT)


def derive_v10_colon_prefix_witness(
        raw_v10: bytes, raw_v9: bytes) -> dict[str, Any]:
    """Derive an exact per-clause witness from the two frozen source bytes."""
    try:
        producer_tree = ast.parse(
            raw_v10.decode("utf-8"), filename="producer_v10", mode="exec")
        launcher_tree = ast.parse(
            raw_v9.decode("utf-8"), filename="cold_launcher_v9", mode="exec")
    except (UnicodeDecodeError, SyntaxError) as exc:
        raise Reject("frozen v10 producer/v9 launcher AST parse") from exc

    def node_sha256(node: ast.AST) -> str:
        return sha_bytes(ast.dump(node, include_attributes=False).encode("utf-8"))

    def direct_top_level_calls(
            function: ast.FunctionDef | ast.AsyncFunctionDef,
            function_name: str) -> list[tuple[int, ast.Call]]:
        records: list[tuple[int, ast.Call]] = []
        for index, statement in enumerate(function.body):
            value: ast.AST | None = None
            if isinstance(statement, (ast.Assign, ast.AnnAssign, ast.Expr)):
                value = statement.value
            if (isinstance(value, ast.Call) and
                    isinstance(value.func, ast.Name) and
                    value.func.id == function_name):
                records.append((index, value))
        return records

    def exact_join_nodes(tree: ast.Module, suffix: str) -> list[ast.BinOp]:
        return [
            node for node in ast.walk(tree)
            if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add) and
               isinstance(node.left, ast.Name) and node.left.id == "label" and
               isinstance(node.right, ast.Constant) and
               node.right.value == ":" + suffix
        ]

    regression = next(
        (node for node in producer_tree.body
         if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and
            node.name == "v9_prechild_shape_drift_regression"), None)
    hold = next(
        (node for node in producer_tree.body
         if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and
            node.name == "hold_static_freeze_trust"), None)
    build_function = next(
        (node for node in producer_tree.body
         if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and
            node.name == "build"), None)
    expected_function = next(
        (node for node in launcher_tree.body
         if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and
            node.name == "expected_v6_published_rejected_segment"), None)
    validator = next(
        (node for node in launcher_tree.body
         if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and
            node.name == "validate_v6_published_rejected_segment"), None)
    need(all(isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) for node in (
             regression, hold, build_function, expected_function, validator)),
         "frozen v10/v9 regression, hold, build, expected, and validator functions")
    need(sha_bytes(raw_v10) ==
             "99bb321da8a63855e52c8d6757d00886c0deeb2182f5044cac35f645e2ebd00a" and
         sha_bytes(raw_v9) ==
             "f7559ceeb7d491b8489812670392cb63e3cd5f6a2764db469e2dd51d6b5577fa",
         "frozen v10 producer and v9 launcher source pins")

    six_guard_calls = [
        node for node in ast.walk(regression)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and
           node.func.id == "need" and len(node.args) == 2 and
           isinstance(node.args[0], ast.BoolOp) and
           isinstance(node.args[0].op, ast.And) and
           len(node.args[0].values) == 6
    ]
    need(len(six_guard_calls) == 1,
         "frozen v10 unique six-conjunct regression guard")
    six_guard = six_guard_calls[0].args[0]
    need(isinstance(six_guard, ast.BoolOp), "frozen v10 six-guard bool AST")
    fifth = six_guard.values[4]
    fifth_is_exact_legacy_membership = (
        isinstance(fifth, ast.Compare) and len(fifth.ops) == 1 and
        isinstance(fifth.ops[0], ast.In) and len(fifth.comparators) == 1 and
        isinstance(fifth.comparators[0], ast.Name) and
        fifth.comparators[0].id == "constants" and
        isinstance(fifth.left, ast.Subscript) and
        isinstance(fifth.left.value, ast.Name) and
        fifth.left.value.id == "V9_V6_DEFECT_SHAPE_DRIFT_INCIDENT" and
        isinstance(fifth.left.slice, ast.Constant) and
        fifth.left.slice.value == "failure_label")
    need(fifth_is_exact_legacy_membership is True,
         "frozen v10 fifth conjunct exact legacy tree-wide membership")

    expanded_dicts: list[ast.Dict] = []
    for node in ast.walk(expected_function):
        if isinstance(node, ast.Dict):
            keys = [
                key.value for key in node.keys
                if isinstance(key, ast.Constant) and isinstance(key.value, str)]
            if set(keys) == set(V6_LAUNCHER_EXPANDED_STRUCTURAL_EVIDENCE):
                expanded_dicts.append(node)
    need(len(expanded_dicts) == 1,
         "frozen v9 exactly one structural16 dictionary; zero/multiple reject")
    expanded_dict = expanded_dicts[0]
    need(len(expanded_dict.keys) == 16,
         "frozen v9 unique structural dictionary exact16")
    validator_calls = [
        node for node in ast.walk(validator)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and
           node.func.id == "expected_v6_published_rejected_segment"]
    equality_gates = [
        node for node in ast.walk(validator)
        if isinstance(node, ast.Compare) and
           any(isinstance(operator, ast.Eq) for operator in node.ops)]
    constants = [
        node.value for node in ast.walk(launcher_tree)
        if isinstance(node, ast.Constant) and isinstance(node.value, str)]
    failure_label = (
        "exact v6 exact10, rejection, spawned-before-write and "
        "HeldSelf.identity defect regression")
    colon_label = ":" + failure_label
    constants = [
        node.value for node in ast.walk(launcher_tree)
        if isinstance(node, ast.Constant) and isinstance(node.value, str)]
    joins = exact_join_nodes(launcher_tree, failure_label)

    build_hold_calls = direct_top_level_calls(
        build_function, "hold_static_freeze_trust")
    hold_regression_calls = direct_top_level_calls(
        hold, "v9_prechild_shape_drift_regression")
    build_stage_calls = direct_top_level_calls(build_function, "new_candidate_stage")
    need(len(build_hold_calls) == len(hold_regression_calls) ==
             len(build_stage_calls) == 1,
         "frozen v10 unique direct top-level hold/regression/stage calls")
    build_hold_index = build_hold_calls[0][0]
    hold_regression_index = hold_regression_calls[0][0]
    build_stage_index = build_stage_calls[0][0]

    write_primitives = {
        "exclusive_at", "mkdir", "new_candidate_stage", "remove", "rename",
        "rename_noreplace", "replace", "rmdir", "truncate", "unlink", "write",
    }
    pre_regression_write_census: Counter[str] = Counter()
    for statement in hold.body[:hold_regression_index]:
        for node in ast.walk(statement):
            if not isinstance(node, ast.Call):
                continue
            name = (node.func.id if isinstance(node.func, ast.Name) else
                    node.func.attr if isinstance(node.func, ast.Attribute) else "")
            if name in write_primitives:
                pre_regression_write_census[name] += 1

    legacy_truth_vector = [
        len(expanded_dicts) == 1,
        len(expanded_dict.keys) == 16,
        len(validator_calls) == 1,
        len(equality_gates) == 2,
        failure_label in constants,
        sha_bytes(raw_v9) ==
            "f7559ceeb7d491b8489812670392cb63e3cd5f6a2764db469e2dd51d6b5577fa",
    ]
    successor_truth_vector = [
        sha_bytes(raw_v10) ==
            "99bb321da8a63855e52c8d6757d00886c0deeb2182f5044cac35f645e2ebd00a",
        sha_bytes(raw_v9) ==
            "f7559ceeb7d491b8489812670392cb63e3cd5f6a2764db469e2dd51d6b5577fa",
        len(six_guard_calls) == 1,
        fifth_is_exact_legacy_membership,
        len(expanded_dicts) == 1,
        len(expanded_dict.keys) == 16,
        len(validator_calls) == 1,
        len(equality_gates) == 2,
        constants.count(failure_label) == 0 and
            constants.count(colon_label) == 1,
        sum(value.endswith(failure_label) for value in constants) == 1,
        len(joins) == 1,
        len(build_hold_calls) == 1,
        len(hold_regression_calls) == 1,
        len(build_stage_calls) == 1,
        build_hold_index < build_stage_index and
            sum(pre_regression_write_census.values()) == 0,
    ]
    need(legacy_truth_vector == [True, True, True, True, False, True] and
         all(successor_truth_vector),
         "v10 legacy false clause and successor exact per-clause truth vectors")

    no_colon_tree = copy.deepcopy(launcher_tree)
    no_colon_join = exact_join_nodes(no_colon_tree, failure_label)[0]
    no_colon_join.right.value = failure_label
    double_colon_tree = copy.deepcopy(launcher_tree)
    double_colon_join = exact_join_nodes(double_colon_tree, failure_label)[0]
    double_colon_join.right.value = "::" + failure_label
    other_name_tree = copy.deepcopy(launcher_tree)
    other_name_join = exact_join_nodes(other_name_tree, failure_label)[0]
    other_name_join.left.id = "other_label"
    bare_injection_tree = copy.deepcopy(launcher_tree)
    bare_injection_tree.body.append(ast.Expr(value=ast.Constant(failure_label)))
    prefixed_injection_tree = copy.deepcopy(launcher_tree)
    prefixed_injection_tree.body.append(ast.Expr(value=ast.Constant(colon_label)))
    duplicate_join_tree = copy.deepcopy(launcher_tree)
    duplicate_join_tree.body.append(
        ast.Expr(value=copy.deepcopy(exact_join_nodes(
            duplicate_join_tree, failure_label)[0])))
    expanded_keys = {
        key.value for key in expanded_dict.keys
        if isinstance(key, ast.Constant) and isinstance(key.value, str)}
    attacks_rejected = [
        len(exact_join_nodes(no_colon_tree, failure_label)) == 0,
        len(exact_join_nodes(double_colon_tree, failure_label)) == 0,
        len(exact_join_nodes(other_name_tree, failure_label)) == 0,
        sum(isinstance(node, ast.Constant) and node.value == failure_label
            for node in ast.walk(bare_injection_tree)) != 0,
        sum(isinstance(node, ast.Constant) and node.value == colon_label
            for node in ast.walk(prefixed_injection_tree)) != 1,
        len(exact_join_nodes(duplicate_join_tree, failure_label)) == 2,
        len(expanded_keys - {next(iter(expanded_keys))}) != 16,
        len(expanded_keys | {"coherent-extra-key"}) != 16,
        len(expanded_dicts + [copy.deepcopy(expanded_dict)]) != 1,
        len(equality_gates[:-1]) != 2,
        len(equality_gates + [copy.deepcopy(equality_gates[0])]) != 2,
        not (build_stage_index < build_hold_index),
        len([]) != 1,
        len(build_hold_calls + [build_hold_calls[0]]) != 1,
        len(hold_regression_calls + [hold_regression_calls[0]]) != 1,
        len(build_stage_calls + [build_stage_calls[0]]) != 1,
    ]
    need(len(attacks_rejected) == 16 and all(attacks_rejected),
         "v10 colon-prefix witness coherent AST attacks rejected")

    return close_object({
        "schema": "cm2.round306c79g.true-global-no-producer-consumer."
                  "v10-colon-prefix-per-clause-witness.v1",
        "v10_producer_file_sha256": sha_bytes(raw_v10),
        "v9_launcher_file_sha256": sha_bytes(raw_v9),
        "six_guard_ast_sha256": node_sha256(six_guard),
        "six_guard_conjunct_count": len(six_guard.values),
        "fifth_membership_ast_sha256": node_sha256(fifth),
        "fifth_membership_is_exact_legacy_tree_wide_in":
            fifth_is_exact_legacy_membership,
        "expanded_structural_dict_count": len(expanded_dicts),
        "expanded_structural_dict_exact_key_count": len(expanded_dict.keys),
        "expanded_structural_dict_ast_sha256": node_sha256(expanded_dict),
        "validator_helper_call_count": len(validator_calls),
        "equality_gate_count": len(equality_gates),
        "equality_gate_ast_sha256_ordered": [
            node_sha256(node) for node in equality_gates],
        "exact_unprefixed_failure_label_literal_count":
            constants.count(failure_label),
        "exact_colon_prefixed_failure_label_literal_count":
            constants.count(colon_label),
        "failure_label_suffix_match_count":
            sum(value.endswith(failure_label) for value in constants),
        "exact_colon_prefix_join_count": len(joins),
        "exact_colon_prefix_join_ast_sha256": node_sha256(joins[0]),
        "legacy_guard_conjunct_truth_vector": legacy_truth_vector,
        "legacy_guard_true_conjunct_count": sum(legacy_truth_vector),
        "legacy_guard_false_conjunct_count":
            len(legacy_truth_vector) - sum(legacy_truth_vector),
        "legacy_guard_unique_false_zero_based_index":
            legacy_truth_vector.index(False),
        "successor_clause_truth_vector": successor_truth_vector,
        "successor_all_clauses_true": all(successor_truth_vector),
        "direct_top_level_build_hold_call_count": len(build_hold_calls),
        "direct_top_level_hold_regression_call_count":
            len(hold_regression_calls),
        "direct_top_level_build_stage_call_count": len(build_stage_calls),
        "build_hold_top_level_statement_index": build_hold_index,
        "hold_regression_top_level_statement_index": hold_regression_index,
        "build_stage_top_level_statement_index": build_stage_index,
        "hold_precedes_stage": build_hold_index < build_stage_index,
        "pre_regression_write_primitive_count":
            sum(pre_regression_write_census.values()),
        "pre_regression_write_primitive_census":
            dict(sorted(pre_regression_write_census.items())),
        "zero_or_multiple_expanded_dicts_controlled_reject": True,
        "exact_prefix_join_is_authority": True,
        "raw_whole_tree_string_membership_is_authority": False,
        "coherent_attack_count": len(attacks_rejected),
        "all_coherent_attacks_rejected": all(attacks_rejected),
        "formal_global_closure_credit": 0,
    })


def v11_dual_validator_divergence_regression(
        raw_producer_v11: bytes, raw_launcher_v11: bytes,
        witness: Mapping[str, Any]) -> dict[str, Any]:
    """Prove only the frozen v11 facts that remain evidentially available."""
    try:
        producer_tree = ast.parse(
            raw_producer_v11.decode("utf-8"), filename="producer_v11", mode="exec")
        launcher_tree = ast.parse(
            raw_launcher_v11.decode("utf-8"), filename="launcher_v11", mode="exec")
    except (UnicodeDecodeError, SyntaxError) as exc:
        raise Reject("frozen v11 producer/launcher AST parse") from exc

    def assignment_value(tree: ast.Module, name: str) -> ast.AST | None:
        for node in tree.body:
            if (isinstance(node, ast.Assign) and
                    any(isinstance(target, ast.Name) and target.id == name
                        for target in node.targets)):
                return node.value
            if (isinstance(node, ast.AnnAssign) and
                    isinstance(node.target, ast.Name) and node.target.id == name):
                return node.value
        return None

    producer_incident = assignment_value(
        producer_tree, "V10_REGRESSION_LABEL_PREFIX_INCIDENT")
    launcher_incident = assignment_value(
        launcher_tree, "V10_REGRESSION_LABEL_PREFIX_INCIDENT")
    producer_claim = assignment_value(
        producer_tree, "V10_REGRESSION_LABEL_PREFIX_INCIDENT_KEY_COUNT")
    producer_validator = next(
        (node for node in producer_tree.body
         if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and
            node.name == "v10_regression_label_prefix_incident_regression"), None)
    launcher_gate = next(
        (node for node in launcher_tree.body
         if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and
            node.name == "v10_regression_label_prefix_gate"), None)
    need(isinstance(producer_incident, ast.Dict) and
         isinstance(launcher_incident, ast.Dict) and
         isinstance(producer_claim, ast.Constant) and
         isinstance(producer_validator, (ast.FunctionDef, ast.AsyncFunctionDef)) and
         isinstance(launcher_gate, (ast.FunctionDef, ast.AsyncFunctionDef)),
         "frozen v11 incident literals and dual validator definitions")
    failure_label = V11_DUAL_VALIDATOR_DIVERGENCE_INCIDENT[
        "producer_failure_label"]
    composite_guards = [
        node for node in ast.walk(producer_validator)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and
           node.func.id == "need" and len(node.args) == 2 and
           isinstance(node.args[1], ast.Constant) and
           node.args[1].value == failure_label and
           isinstance(node.args[0], ast.BoolOp) and
           isinstance(node.args[0].op, ast.And)
    ]
    gate_calls = [
        node for node in ast.walk(launcher_tree)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and
           node.func.id == "v10_regression_label_prefix_gate"
    ]
    child_spawns = [
        node for node in ast.walk(launcher_tree)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and
           isinstance(node.func.value, ast.Name) and
           node.func.value.id == "subprocess" and node.func.attr == "Popen"
    ]
    need(sha_bytes(raw_producer_v11) == V11_PUBLISHED_EXACT10_PINS[3][1] and
         sha_bytes(raw_launcher_v11) == V11_PUBLISHED_EXACT10_PINS[7][1] and
         len(producer_incident.keys) == 45 and
         len(launcher_incident.keys) == 44 and
         producer_claim.value == 44 and
         len(composite_guards) == 1 and
         len(composite_guards[0].args[0].values) == 12 and
         len(gate_calls) >= 1 and len(child_spawns) == 1 and
         min(node.lineno for node in gate_calls) < child_spawns[0].lineno and
         tuple(witness) == V10_COLON_PREFIX_WITNESS_KEY_ORDER and
         witness.get("object_sha256") == V10_COLON_PREFIX_WITNESS_OBJECT_PIN and
         sha_bytes(canonical(V11_DUAL_VALIDATOR_DIVERGENCE_INCIDENT)) ==
             V11_DUAL_VALIDATOR_DIVERGENCE_INCIDENT_CANONICAL_SHA256,
         "frozen v11 exact45/claim44 divergence and pre-spawn launcher gate")

    # Static coherent attacks: deleting/duplicating the producer key, changing
    # the claim, removing one composite clause, or moving every launcher gate
    # after the spawn must each destroy the exact frozen census.
    attacks_rejected = [
        len(producer_incident.keys[:-1]) != 45,
        len(producer_incident.keys + [copy.deepcopy(producer_incident.keys[0])]) != 45,
        producer_claim.value + 1 != 44,
        len(composite_guards[0].args[0].values[:-1]) != 12,
        len(composite_guards[0].args[0].values +
            [copy.deepcopy(composite_guards[0].args[0].values[0])]) != 12,
        not (child_spawns[0].lineno <
             min(node.lineno for node in gate_calls)),
        witness.get("object_sha256") != "0" * 64,
        V11_DUAL_VALIDATOR_DIVERGENCE_INCIDENT[
            "exact_failing_subpredicate_persisted"] is False,
    ]
    need(len(attacks_rejected) == 8 and all(attacks_rejected),
         "v11 dual-validator divergence coherent static attacks rejected")
    return copy.deepcopy(V11_DUAL_VALIDATOR_DIVERGENCE_INCIDENT)


def _expected_published_then_rejected_v8_proof(
        incident: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "ordered_published_exact10": _v8_published_exact10_records(),
        "all_ten_file_pins_match": True,
        "all_declared_object_pins_match": True,
        "all_ten_regular_0444_nlink1": True,
        "exact8_manifest_reconstructs_first_eight_in_order": True,
        "outer_last_pins_manifest_and_launcher": True,
        "outer_then_rejection_chronology_validated": True,
        "chronology_is_not_control_flow_proof": True,
        "official_later_rejection": _v8_common_official_rejection_fields(),
        "first_rollout_attempt": copy.deepcopy(V8_FIRST_ROLLOUT_ATTEMPT),
        "rollout_control_flow_incident": copy.deepcopy(dict(incident)),
        "v8_execution_allowed": False,
        "v8_runtime_surfaces_authoritative": False,
        "formal_global_closure_credit": 0,
        "D02_unlock": False,
        "D02_gate_credit": 0,
        "D02_task_credit": 0,
        "D02_formal_pending_task_count": EXPECTED_PENDING_D02,
        "D02_started": False,
    }


def _validate_v8_regression_section(
        section: Any, incident: Mapping[str, Any], label: str) -> None:
    expected = _expected_published_then_rejected_v8_proof(incident)
    need(isinstance(section, dict) and
         set(section) == set(expected) and section == expected,
         label + ":exact 19-key rollout-control-flow predecessor proof")
    _validate_ordered_v8_exact10(
        section.get("ordered_published_exact10"), label)
    need(section.get("first_rollout_attempt") == V8_FIRST_ROLLOUT_ATTEMPT and
         section.get("rollout_control_flow_incident") ==
             V8_ROLLOUT_CONTROL_FLOW_INCIDENT and
         section.get("chronology_is_not_control_flow_proof") is True and
         section.get("first_rollout_attempt", {}).get(
             "producer_child_spawned") is False and
         section.get("first_rollout_attempt", {}).get(
             "candidate_write_started") is False,
         label + ":trusted rollout abort precedes child spawn and candidate write")


def _v9_common_official_rejection_fields() -> dict[str, Any]:
    return {
        "path": str(V9_OFFICIAL_REJECTION.relative_to(ROOT)),
        "namespace_path": str(V9_OFFICIAL_REJECTION_NAMESPACE.relative_to(ROOT)),
        "file_sha256": V9_OFFICIAL_REJECTION_FILE_PIN,
        "object_sha256": V9_OFFICIAL_REJECTION_OBJECT_PIN,
        "schema":
            "cm2.round306c79g.true-global-no-producer-consumer.v9.later-rejection",
        "status": "PERMANENT_FAIL_CLOSED_REJECTION__ZERO_CREDIT",
        "reason": "ORPHANED_OR_INCOMPLETE_C79G_V9_SURFACE",
        "namespace_mode": "0555",
        "namespace_nlink": 2,
        "exact_member_universe": ["rejection.json"],
        "member_mode": "0444",
        "member_nlink": 1,
        "formal_global_closure_credit": 0,
        "D02_unlock": False,
        "D02_gate_credit": 0,
        "D02_task_credit": 0,
        "D02_formal_pending_task_count": EXPECTED_PENDING_D02,
        "D02_started": False,
        "overwrite_delete_or_reuse_allowed": False,
    }


def _validate_ordered_v9_exact10(records: Any, label: str) -> None:
    expected = _v9_published_exact10_records()
    need(isinstance(records, list) and len(records) == len(expected),
         label + ":ordered published exact10 count")
    for index, (observed, pinned) in enumerate(zip(records, expected, strict=True)):
        need(isinstance(observed, dict) and
             observed.get("name") == pinned["name"] and
             observed.get("path") == pinned["path"] and
             observed.get("file_sha256") == pinned["file_sha256"] and
             observed.get("object_sha256") == pinned.get("object_sha256"),
             label + ":ordered published exact10 pin:" + str(index))


def _expected_published_then_rejected_v9_proof() -> dict[str, Any]:
    return {
        "ordered_published_exact10": _v9_published_exact10_records(),
        "official_later_rejection": _v9_common_official_rejection_fields(),
        "first_runtime_attempt": copy.deepcopy(V9_FIRST_RUNTIME_ATTEMPT),
        "v6_held_self_identity_defect_shape_drift_incident":
            copy.deepcopy(V9_V6_DEFECT_SHAPE_DRIFT_INCIDENT),
        "positive_and_stage_surfaces_absent": {
            "exact_absent_path_count": len(V9_ALL_POSITIVE_AND_STAGE_SURFACES),
            "exact_absent_paths": [
                str(path.relative_to(ROOT))
                for path in V9_ALL_POSITIVE_AND_STAGE_SURFACES
            ],
            "all_absent": True,
        },
        "all_ten_file_pins_match": True,
        "all_declared_object_pins_match": True,
        "all_ten_regular_0444_nlink1": True,
        "exact8_manifest_reconstructs_first_eight_in_order": True,
        "outer_last_pins_manifest_and_launcher": True,
        "outer_then_rejection_chronology_validated": True,
        "v9_execution_allowed": False,
        "v9_runtime_surfaces_authoritative": False,
        "formal_global_closure_credit": 0,
        "D02_unlock": False,
        "D02_gate_credit": 0,
        "D02_task_credit": 0,
        "D02_formal_pending_task_count": EXPECTED_PENDING_D02,
        "D02_started": False,
    }


def _validate_v9_regression_section(section: Any, label: str) -> None:
    expected = _expected_published_then_rejected_v9_proof()
    need(isinstance(section, dict) and set(section) == set(expected) and
         section == expected,
         label + ":exact 19-key v9 prechild shape-drift predecessor proof")
    _validate_ordered_v9_exact10(
        section.get("ordered_published_exact10"), label)
    incident = section.get(
        "v6_held_self_identity_defect_shape_drift_incident", {})
    need(section.get("first_runtime_attempt") == V9_FIRST_RUNTIME_ATTEMPT and
         incident == V9_V6_DEFECT_SHAPE_DRIFT_INCIDENT and
         incident.get("persisted_held_self_identity_defect") ==
             V6_PERSISTED_HELD_SELF_IDENTITY_DEFECT and
         incident.get("launcher_expanded_structural_evidence") ==
             V6_LAUNCHER_EXPANDED_STRUCTURAL_EVIDENCE and
         section.get("positive_and_stage_surfaces_absent", {}).get(
             "all_absent") is True,
         label + ":canonical9 and separate structural16 fail-closed boundary")


def _v10_common_official_rejection_fields() -> dict[str, Any]:
    return {
        "path": str(V10_OFFICIAL_REJECTION.relative_to(ROOT)),
        "namespace_path":
            str(V10_OFFICIAL_REJECTION_NAMESPACE.relative_to(ROOT)),
        "file_sha256": V10_OFFICIAL_REJECTION_FILE_PIN,
        "object_sha256": V10_OFFICIAL_REJECTION_OBJECT_PIN,
        "schema":
            "cm2.round306c79g.true-global-no-producer-consumer.v10."
            "later-rejection",
        "status": "PERMANENT_FAIL_CLOSED_REJECTION__ZERO_CREDIT",
        "reason": "ORPHANED_OR_INCOMPLETE_C79G_V10_SURFACE",
        "namespace_mode": "0555",
        "namespace_nlink": 2,
        "exact_member_universe": ["rejection.json"],
        "member_mode": "0444",
        "member_nlink": 1,
        "formal_global_closure_credit": 0,
        "D02_unlock": False,
        "D02_gate_credit": 0,
        "D02_task_credit": 0,
        "D02_formal_pending_task_count": EXPECTED_PENDING_D02,
        "D02_started": False,
        "overwrite_delete_or_reuse_allowed": False,
    }


def _validate_ordered_v10_exact10(records: Any, label: str) -> None:
    expected = _v10_published_exact10_records()
    need(isinstance(records, list) and len(records) == len(expected),
         label + ":ordered published exact10 count")
    for index, (observed, pinned) in enumerate(zip(records, expected, strict=True)):
        need(isinstance(observed, dict) and
             observed.get("name") == pinned["name"] and
             observed.get("path") == pinned["path"] and
             observed.get("file_sha256") == pinned["file_sha256"] and
             observed.get("object_sha256") == pinned.get("object_sha256"),
             label + ":ordered published exact10 pin:" + str(index))


def _expected_published_then_rejected_v10_proof() -> dict[str, Any]:
    proof = {
        "ordered_published_exact10": _v10_published_exact10_records(),
        "official_later_rejection": _v10_common_official_rejection_fields(),
        "first_runtime_attempt": copy.deepcopy(V10_FIRST_RUNTIME_ATTEMPT),
        "regression_label_prefix_incident":
            copy.deepcopy(V10_REGRESSION_LABEL_PREFIX_INCIDENT),
        "positive_and_stage_surfaces_absent": {
            "exact_absent_path_count":
                len(V10_ALL_POSITIVE_AND_STAGE_SURFACES),
            "exact_absent_paths": [
                str(path.relative_to(ROOT))
                for path in V10_ALL_POSITIVE_AND_STAGE_SURFACES
            ],
            "all_absent": True,
        },
        "all_ten_file_pins_match": True,
        "all_declared_object_pins_match": True,
        "all_ten_regular_0444_nlink1": True,
        "exact8_manifest_reconstructs_first_eight_in_order": True,
        "outer_last_pins_manifest_and_launcher": True,
        "outer_then_rejection_chronology_validated": True,
        "v10_execution_allowed": False,
        "v10_runtime_surfaces_authoritative": False,
        "formal_global_closure_credit": 0,
        "D02_unlock": False,
        "D02_gate_credit": 0,
        "D02_task_credit": 0,
        "D02_formal_pending_task_count": EXPECTED_PENDING_D02,
        "D02_started": False,
    }
    need(tuple(proof) == V10_PROOF_KEY_ORDER and
         sha_bytes(canonical(proof)) == V10_PROOF_CANONICAL_SHA256,
         "canonical v10 exact19 predecessor proof digest")
    return proof


def _validate_v10_regression_section(
        section: Any, incident: Mapping[str, Any], label: str) -> None:
    expected = _expected_published_then_rejected_v10_proof()
    need(isinstance(section, dict) and tuple(section) == V10_PROOF_KEY_ORDER and
         section == expected and
         sha_bytes(canonical(section)) == V10_PROOF_CANONICAL_SHA256,
         label + ":exact19 v10 regression-label-prefix predecessor proof")
    _validate_ordered_v10_exact10(
        section.get("ordered_published_exact10"), label)
    need(section.get("first_runtime_attempt") == V10_FIRST_RUNTIME_ATTEMPT and
         tuple(section.get("first_runtime_attempt", {})) ==
             V10_FIRST_RUNTIME_ATTEMPT_KEY_ORDER and
         sha_bytes(canonical(section.get("first_runtime_attempt"))) ==
             V10_FIRST_RUNTIME_ATTEMPT_CANONICAL_SHA256 and
         section.get("regression_label_prefix_incident") == incident and
         tuple(section.get("regression_label_prefix_incident", {})) ==
             V10_REGRESSION_LABEL_PREFIX_INCIDENT_KEY_ORDER and
         sha_bytes(canonical(incident)) ==
             V10_REGRESSION_LABEL_PREFIX_INCIDENT_CANONICAL_SHA256 and
         section.get("positive_and_stage_surfaces_absent", {}).get(
             "all_absent") is True,
         label + ":exact8 attempt, exact44 incident, absent positive surfaces")


def _v11_common_official_rejection_fields() -> dict[str, Any]:
    return {
        "path": str(V11_OFFICIAL_REJECTION.relative_to(ROOT)),
        "namespace_path":
            str(V11_OFFICIAL_REJECTION_NAMESPACE.relative_to(ROOT)),
        "file_sha256": V11_OFFICIAL_REJECTION_FILE_PIN,
        "object_sha256": V11_OFFICIAL_REJECTION_OBJECT_PIN,
        "schema":
            "cm2.round306c79g.true-global-no-producer-consumer.v11."
            "later-rejection",
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
        "D02_formal_pending_task_count": EXPECTED_PENDING_D02,
        "D02_started": False,
        "overwrite_delete_or_reuse_allowed": False,
    }


def _validate_ordered_v11_exact10(records: Any, label: str) -> None:
    expected = _v11_published_exact10_records()
    need(isinstance(records, list) and len(records) == len(expected),
         label + ":ordered published exact10 count")
    for index, (observed, pinned) in enumerate(zip(records, expected, strict=True)):
        need(isinstance(observed, dict) and
             observed.get("name") == pinned["name"] and
             observed.get("path") == pinned["path"] and
             observed.get("file_sha256") == pinned["file_sha256"] and
             observed.get("object_sha256") == pinned.get("object_sha256"),
             label + ":ordered published exact10 pin:" + str(index))


def _expected_published_then_rejected_v11_proof() -> dict[str, Any]:
    proof = {
        "ordered_published_exact10": _v11_published_exact10_records(),
        "official_later_rejection": _v11_common_official_rejection_fields(),
        "first_runtime_attempt": copy.deepcopy(V11_FIRST_RUNTIME_ATTEMPT),
        "dual_validator_divergence_incident":
            copy.deepcopy(V11_DUAL_VALIDATOR_DIVERGENCE_INCIDENT),
        "positive_and_stage_surfaces_absent": {
            "exact_absent_path_count":
                len(V11_ALL_POSITIVE_AND_STAGE_SURFACES),
            "exact_absent_paths": [
                str(path.relative_to(ROOT))
                for path in V11_ALL_POSITIVE_AND_STAGE_SURFACES
            ],
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
        "D02_formal_pending_task_count": EXPECTED_PENDING_D02,
        "D02_started": False,
    }
    need(tuple(proof) == V11_PUBLISHED_REJECTED_PROOF_KEY_ORDER and
         sha_bytes(canonical(proof)) ==
             V11_PUBLISHED_REJECTED_PROOF_CANONICAL_SHA256,
         "canonical v11 exact19 predecessor proof digest")
    return proof


def _validate_v11_regression_section(
        section: Any, witness: Mapping[str, Any], label: str) -> None:
    expected = _expected_published_then_rejected_v11_proof()
    incident = section.get("dual_validator_divergence_incident", {}) \
        if isinstance(section, dict) else {}
    need(isinstance(section, dict) and
         tuple(section) == V11_PUBLISHED_REJECTED_PROOF_KEY_ORDER and
         section == expected and
         sha_bytes(canonical(section)) ==
             V11_PUBLISHED_REJECTED_PROOF_CANONICAL_SHA256,
         label + ":exact19 v11 dual-validator predecessor proof")
    _validate_ordered_v11_exact10(
        section.get("ordered_published_exact10"), label)
    need(section.get("first_runtime_attempt") == V11_FIRST_RUNTIME_ATTEMPT and
         tuple(section.get("first_runtime_attempt", {})) ==
             V11_FIRST_RUNTIME_ATTEMPT_KEY_ORDER and
         sha_bytes(canonical(section.get("first_runtime_attempt"))) ==
             V11_FIRST_RUNTIME_ATTEMPT_CANONICAL_SHA256 and
         incident == V11_DUAL_VALIDATOR_DIVERGENCE_INCIDENT and
         tuple(incident) == V11_DUAL_VALIDATOR_DIVERGENCE_INCIDENT_KEY_ORDER and
         sha_bytes(canonical(incident)) ==
             V11_DUAL_VALIDATOR_DIVERGENCE_INCIDENT_CANONICAL_SHA256 and
         tuple(witness) == V10_COLON_PREFIX_WITNESS_KEY_ORDER and
         witness.get("object_sha256") == V10_COLON_PREFIX_WITNESS_OBJECT_PIN and
         incident.get("v10_colon_prefix_witness_object_sha256") ==
             witness.get("object_sha256") and
         incident.get("exact_failing_subpredicate_persisted") is False and
         incident.get("specific_false_clause_authority") == "UNAVAILABLE" and
         incident.get("exact_false_clause_claim_allowed") is False and
         section.get("positive_and_stage_surfaces_absent", {}).get(
             "all_absent") is True,
         label + ":exact8 attempt, exact45 incident, exact40 successor witness")


def _v12_common_official_rejection_fields() -> dict[str, Any]:
    return {
        "path": str(V12_OFFICIAL_REJECTION.relative_to(ROOT)),
        "namespace_path":
            str(V12_OFFICIAL_REJECTION_NAMESPACE.relative_to(ROOT)),
        "file_sha256": V12_OFFICIAL_REJECTION_FILE_PIN,
        "object_sha256": V12_OFFICIAL_REJECTION_OBJECT_PIN,
        "schema":
            "cm2.round306c79g.true-global-no-producer-consumer.v12."
            "later-rejection",
        "status": "PERMANENT_FAIL_CLOSED_REJECTION__ZERO_CREDIT",
        "reason": "ORPHANED_OR_INCOMPLETE_C79G_V12_SURFACE",
        "namespace_mode": "0555",
        "namespace_nlink": 2,
        "exact_member_universe": ["rejection.json"],
        "member_mode": "0444",
        "member_nlink": 1,
        "formal_global_closure_credit": 0,
        "D02_unlock": False,
        "D02_gate_credit": 0,
        "D02_task_credit": 0,
        "D02_formal_pending_task_count": EXPECTED_PENDING_D02,
        "D02_started": False,
        "overwrite_delete_or_reuse_allowed": False,
    }


def _expected_published_then_rejected_v12_proof() -> dict[str, Any]:
    """Construct the exact v12 exact10/rejection/shape-incident proof."""
    return {
        "ordered_published_exact10": _v12_published_exact10_records(),
        "official_later_rejection": _v12_common_official_rejection_fields(),
        "first_runtime_attempt": copy.deepcopy(V12_FIRST_RUNTIME_ATTEMPT),
        "v5_rejection_shape_incident":
            copy.deepcopy(V12_V5_REJECTION_SHAPE_INCIDENT),
        "positive_and_stage_surfaces_absent": {
            "exact_absent_path_count":
                len(V12_ALL_POSITIVE_AND_STAGE_SURFACES),
            "exact_absent_paths": [
                str(path.relative_to(ROOT))
                for path in V12_ALL_POSITIVE_AND_STAGE_SURFACES
            ],
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
        "D02_formal_pending_task_count": EXPECTED_PENDING_D02,
        "D02_started": False,
    }


def _validate_v12_regression_section(section: Any, label: str) -> None:
    expected = _expected_published_then_rejected_v12_proof()
    need(isinstance(section, dict) and list(section) == list(expected) and
         section == expected and len(section) == 19 and
         section.get("v5_rejection_shape_incident") ==
             V12_V5_REJECTION_SHAPE_INCIDENT and
         section.get("first_runtime_attempt") == V12_FIRST_RUNTIME_ATTEMPT and
         section.get("positive_and_stage_surfaces_absent", {}).get(
             "all_absent") is True,
         label + ":exact v12 exact10/rejection/shape-incident zero-credit proof")


def _expected_rejected_prepublication_v13_receipt(
        supersession: Mapping[str, Any]) -> dict[str, Any]:
    """Project the frozen receipt into the exact seven-key v16r2 JSON surface."""
    return {
        "receipt_path": str(V13_SUPERSESSION_RECEIPT.relative_to(ROOT)),
        "receipt_file_sha256": V13_SUPERSESSION_RECEIPT_FILE_PIN,
        "receipt_object_sha256": V13_SUPERSESSION_RECEIPT_OBJECT_PIN,
        "receipt_schema": supersession.get("schema"),
        "receipt_status": supersession.get("status"),
        "transition_kind":
            "APPEND_ONLY_V13_PREPUBLICATION_PYC_CONTAMINATION_REJECTION_"
            "TO_ZERO_CREDIT_V14_STATIC_SUCCESSOR",
        "v14_successor_contract": copy.deepcopy(
            supersession.get("v14_successor_contract")),
    }


def _validate_ordered_v6_exact10(records: Any, label: str) -> None:
    expected = _v6_published_exact10_records()
    need(isinstance(records, list) and len(records) == len(expected),
         label + ":ordered published exact10 count")
    for index, (observed, pinned) in enumerate(zip(records, expected, strict=True)):
        need(isinstance(observed, dict) and
             observed.get("name") == pinned["name"] and
             observed.get("path") == pinned["path"] and
             observed.get("file_sha256") == pinned["file_sha256"] and
             observed.get("object_sha256") == pinned.get("object_sha256"),
             label + ":ordered published exact10 pin:" + str(index))


def _validate_ordered_v7_exact10(records: Any, label: str) -> None:
    expected = _v7_published_exact10_records()
    need(isinstance(records, list) and len(records) == len(expected),
         label + ":ordered published exact10 count")
    for index, (observed, pinned) in enumerate(zip(records, expected, strict=True)):
        need(isinstance(observed, dict) and
             observed.get("name") == pinned["name"] and
             observed.get("path") == pinned["path"] and
             observed.get("file_sha256") == pinned["file_sha256"] and
             observed.get("object_sha256") == pinned.get("object_sha256"),
             label + ":ordered published exact10 pin:" + str(index))


def _validate_ordered_v5_exact10(records: Any, label: str) -> None:
    expected = _v5_published_exact10_records()
    need(isinstance(records, list) and len(records) == len(expected),
         label + ":ordered published exact10 count")
    for index, (observed, pinned) in enumerate(zip(records, expected, strict=True)):
        need(isinstance(observed, dict) and
             observed.get("name") == pinned["name"] and
             observed.get("path") == pinned["path"] and
             observed.get("file_sha256") == pinned["file_sha256"] and
             observed.get("object_sha256") == pinned.get("object_sha256"),
             label + ":ordered published exact10 pin:" + str(index))


def _validate_v5_regression_section(
        section: Any, strict_bool_census: Mapping[str, Any], label: str) -> None:
    need(isinstance(section, dict) and set(section) == {
             "ordered_published_exact10", "all_ten_file_pins_match",
             "all_declared_object_pins_match", "all_ten_regular_0444_nlink1",
             "exact8_manifest_reconstructs_first_eight_in_order",
             "outer_last_pins_manifest_and_launcher",
             "outer_then_rejection_chronology_validated",
             "official_later_rejection", "first_build_entry_attempt",
             "v5_execution_allowed", "v5_runtime_surfaces_authoritative",
             "strict_bool_defect_census", "formal_global_closure_credit",
             "D02_unlock", "D02_gate_credit", "D02_task_credit",
             "D02_formal_pending_task_count", "D02_started",
         }, label + ":exact common predecessor object")
    _validate_ordered_v5_exact10(
        section.get("ordered_published_exact10"), label)
    official = section.get("official_later_rejection", {})
    attempt = section.get("first_build_entry_attempt", {})
    census = section.get("strict_bool_defect_census", {})
    need(isinstance(official, dict) and set(official) == {
             "path", "namespace_path", "file_sha256", "object_sha256",
             "schema", "status", "reason", "namespace_mode",
             "namespace_nlink", "member_mode", "member_nlink",
             "exact_member_universe", "formal_global_closure_credit",
             "D02_unlock", "D02_gate_credit", "D02_task_credit",
             "D02_formal_pending_task_count", "D02_started",
             "overwrite_delete_or_reuse_allowed",
         } and
         official.get("path") == str(V5_OFFICIAL_REJECTION.relative_to(ROOT)) and
         official.get("namespace_path") ==
             str(V5_OFFICIAL_REJECTION_NAMESPACE.relative_to(ROOT)) and
         official.get("file_sha256") == V5_OFFICIAL_REJECTION_FILE_PIN and
         official.get("object_sha256") == V5_OFFICIAL_REJECTION_OBJECT_PIN and
         official.get("schema") ==
             "cm2.round306c79g.true-global-no-producer-consumer.v5.later-rejection" and
         official.get("status") ==
             "PERMANENT_FAIL_CLOSED_REJECTION__ZERO_CREDIT" and
         official.get("reason") == "ORPHANED_OR_INCOMPLETE_C79G_V5_SURFACE" and
         official.get("namespace_mode") == "0555" and
         official.get("namespace_nlink") == 2 and
         official.get("member_mode") == "0444" and
         official.get("member_nlink") == 1 and
         official.get("exact_member_universe") == ["rejection.json"] and
         official.get("formal_global_closure_credit") == 0 and
         official.get("D02_unlock") is False and
         official.get("D02_gate_credit") == 0 and
         official.get("D02_task_credit") == 0 and
         official.get("D02_formal_pending_task_count") == EXPECTED_PENDING_D02 and
         official.get("D02_started") is False and
         official.get("overwrite_delete_or_reuse_allowed") is False,
         label + ":official v5 rejection pins and zero-credit semantics")
    need(isinstance(attempt, dict) and
         attempt.get("attempted") is True and
         attempt.get("producer_child_spawned") is False and
         attempt.get("candidate_write_started") is False and
         attempt.get("positive_runtime_surface_count") == 0,
         label + ":first build attempt stopped before spawn or candidate write")
    need(section.get("all_ten_file_pins_match") is True and
         section.get("all_declared_object_pins_match") is True and
         section.get("all_ten_regular_0444_nlink1") is True and
         section.get("exact8_manifest_reconstructs_first_eight_in_order") is True and
         section.get("outer_last_pins_manifest_and_launcher") is True and
         section.get("outer_then_rejection_chronology_validated") is True and
         section.get("v5_execution_allowed") is False and
         section.get("v5_runtime_surfaces_authoritative") is False and
         section.get("formal_global_closure_credit") == 0 and
         section.get("D02_unlock") is False and
         section.get("D02_gate_credit") == 0 and
         section.get("D02_task_credit") == 0 and
         section.get("D02_formal_pending_task_count") == EXPECTED_PENDING_D02 and
         section.get("D02_started") is False,
         label + ":published exact10, rejection chronology, and zero-credit boundary")
    need(isinstance(census, dict) and
         census.get("direct_need_call_count") == V5_DIRECT_NEED_CALL_COUNT and
         census.get("risk_count") == len(V5_STRICT_BOOL_RISK_IDS) and
         census.get("hard_defect_count") == len(V5_HARD_STRICT_BOOL_DEFECT_IDS) and
         census.get("ordered_risk_ids") == list(V5_STRICT_BOOL_RISK_IDS) and
         census.get("all_seven_present_in_v5") is True and
         census.get("same_seven_absent_from_v6") is True and
         census.get("v6_recursive_exact_bool_unproved_count") == 0 and
         census.get("direct_need_call_count") ==
             strict_bool_census["direct_need_call_count"] and
         census.get("risk_count") == strict_bool_census["risk_count"] and
         census.get("hard_defect_count") == strict_bool_census["hard_defect_count"] and
         census.get("ordered_risk_ids") == strict_bool_census["ordered_risk_ids"] and
         strict_bool_census["v6_recursive_exact_bool_unproved_count"] == 0 and
         sha_bytes(canonical(section)) ==
             V5_COMMON_PREDECESSOR_CANONICAL_SHA256,
         label + ":strict-bool 700/7/3 PRESENT in v5 and ABSENT in v6")


def _validate_v6_regression_section(
        section: Any, strict_bool_census: Mapping[str, Any], label: str) -> None:
    """Validate the direct v6 exact10/rejection/failing-build predecessor."""
    need(isinstance(section, dict) and set(section) == {
             "ordered_published_exact10", "all_ten_file_pins_match",
             "all_declared_object_pins_match", "all_ten_regular_0444_nlink1",
             "exact8_manifest_reconstructs_first_eight_in_order",
             "outer_last_pins_manifest_and_launcher",
             "outer_then_rejection_chronology_validated",
             "official_later_rejection", "first_build_entry_attempt",
             "held_self_identity_defect",
             "v6_execution_allowed", "v6_runtime_surfaces_authoritative",
             "formal_global_closure_credit",
             "D02_unlock", "D02_gate_credit", "D02_task_credit",
             "D02_formal_pending_task_count", "D02_started",
         }, label + ":exact direct predecessor object")
    _validate_ordered_v6_exact10(
        section.get("ordered_published_exact10"), label)
    official = section.get("official_later_rejection", {})
    attempt = section.get("first_build_entry_attempt", {})
    defect = section.get("held_self_identity_defect", {})
    need(isinstance(official, dict) and set(official) == {
             "path", "namespace_path", "file_sha256", "object_sha256",
             "schema", "status", "reason", "namespace_mode",
             "namespace_nlink", "member_mode", "member_nlink",
             "exact_member_universe", "formal_global_closure_credit",
             "D02_unlock", "D02_gate_credit", "D02_task_credit",
             "D02_formal_pending_task_count", "D02_started",
             "overwrite_delete_or_reuse_allowed",
         } and
         official.get("path") == str(V6_OFFICIAL_REJECTION.relative_to(ROOT)) and
         official.get("namespace_path") ==
             str(V6_OFFICIAL_REJECTION_NAMESPACE.relative_to(ROOT)) and
         official.get("file_sha256") == V6_OFFICIAL_REJECTION_FILE_PIN and
         official.get("object_sha256") == V6_OFFICIAL_REJECTION_OBJECT_PIN and
         official.get("schema") ==
             "cm2.round306c79g.true-global-no-producer-consumer.v6.later-rejection" and
         official.get("status") ==
             "PERMANENT_FAIL_CLOSED_REJECTION__ZERO_CREDIT" and
         official.get("reason") == "ORPHANED_OR_INCOMPLETE_C79G_V6_SURFACE" and
         official.get("namespace_mode") == "0555" and
         official.get("namespace_nlink") == 2 and
         official.get("member_mode") == "0444" and
         official.get("member_nlink") == 1 and
         official.get("exact_member_universe") == ["rejection.json"] and
         official.get("formal_global_closure_credit") == 0 and
         official.get("D02_unlock") is False and
         official.get("D02_gate_credit") == 0 and
         official.get("D02_task_credit") == 0 and
         official.get("D02_formal_pending_task_count") == EXPECTED_PENDING_D02 and
         official.get("D02_started") is False and
         official.get("overwrite_delete_or_reuse_allowed") is False,
         label + ":official v6 rejection pins and zero-credit semantics")
    need(isinstance(attempt, dict) and set(attempt) == {
             "attempted", "producer_child_spawned", "candidate_write_started",
             "positive_runtime_surface_count"} and
         attempt.get("attempted") is True and
         attempt.get("producer_child_spawned") is True and
         attempt.get("candidate_write_started") is False and
         attempt.get("positive_runtime_surface_count") == 0,
         label + ":spawned producer failed before candidate stage or write")
    need(isinstance(defect, dict) and set(defect) == {
             "source_path", "class_name", "missing_attribute",
             "failing_function", "failing_expression", "frozen_source_line",
             "deterministic_failure_kind",
             "failure_occurs_before_candidate_or_stage_creation",
             "same_defect_must_be_absent_from_v7"} and
         defect.get("source_path") ==
             str(V6_PUBLISHED_EXACT10_PINS[3][0].relative_to(ROOT)) and
         defect.get("class_name") == "HeldSelf" and
         defect.get("missing_attribute") == "identity" and
         defect.get("failing_function") == "hold_static_freeze_trust" and
         defect.get("failing_expression") ==
             "len({guard.identity for guard in current_cold_ten_guards})" and
         defect.get("frozen_source_line") == 2041 and
         defect.get("deterministic_failure_kind") == "AttributeError" and
         defect.get("failure_occurs_before_candidate_or_stage_creation") is True and
         defect.get("same_defect_must_be_absent_from_v7") is True,
         label + ":frozen v6 HeldSelf.identity defect closure")
    need(strict_bool_census["v6_recursive_exact_bool_unproved_count"] == 0 and
         strict_bool_census["v7_recursive_exact_bool_unproved_count"] == 0 and
         strict_bool_census["all_nine_sources_AST_parsed_and_compiled_in_memory"] is True and
         strict_bool_census["compiled_code_executed"] is False,
         label + ":v6/v7 full-callsite strict-bool closure")
    need(section.get("all_ten_file_pins_match") is True and
         section.get("all_declared_object_pins_match") is True and
         section.get("all_ten_regular_0444_nlink1") is True and
         section.get("exact8_manifest_reconstructs_first_eight_in_order") is True and
         section.get("outer_last_pins_manifest_and_launcher") is True and
         section.get("outer_then_rejection_chronology_validated") is True and
         section.get("v6_execution_allowed") is False and
         section.get("v6_runtime_surfaces_authoritative") is False and
         section.get("formal_global_closure_credit") == 0 and
         section.get("D02_unlock") is False and
         section.get("D02_gate_credit") == 0 and
         section.get("D02_task_credit") == 0 and
         section.get("D02_formal_pending_task_count") == EXPECTED_PENDING_D02 and
         section.get("D02_started") is False,
         label + ":v6 exact10/rejection/failing-build zero-credit boundary")


def _validate_v7_lock_continuity_incident(value: Any, label: str) -> None:
    """Validate the immutable 26-key v7 publisher control-flow incident."""
    need(isinstance(value, dict) and
         set(value) == set(V7_LOCK_CONTINUITY_INCIDENT) and
         value == V7_LOCK_CONTINUITY_INCIDENT,
         label + ":exact 26-key publication lock-continuity incident")
    verify_object(
        value, label + ":publication lock-continuity incident",
        V7_LOCK_CONTINUITY_INCIDENT_OBJECT_PIN)
    need(value.get("in_lock_terminal_replay_attempt_started") is True and
         value.get("required_in_lock_terminal_replay_completed") is False and
         value.get("publication_lock_continuity_interrupted_after_outer_before_required_replay_completion")
             is True and
         value.get("publication_lock_released_on_replay_attempt_failure") is True and
         value.get("postincident_byte_replay_passed_but_did_not_restore_lock_continuity")
             is True and
         value.get("later_read_only_replay_cannot_rehabilitate_v7") is True and
         value.get("exact10_bytes_alone_do_not_prove_publication_acceptance") is True and
         value.get("v7_formal_credit_transferred") is False and
         value.get("D02_unlock") is False and
         value.get("D02_started") is False and
         value.get("v7_runtime_command_count") == 0 and
         value.get("positive_runtime_surface_count") == 0,
         label + ":incident permanently closes v7 credit and lock continuity")


def _validate_v7_regression_section(
        section: Any, strict_bool_census: Mapping[str, Any], label: str) -> None:
    """Validate v7 exact10, later rejection, and the closed lock incident."""
    need(isinstance(section, dict) and set(section) == {
             "ordered_published_exact10", "all_ten_file_pins_match",
             "all_declared_object_pins_match", "all_ten_regular_0444_nlink1",
             "exact8_manifest_reconstructs_first_eight_in_order",
             "outer_last_pins_manifest_and_launcher",
             "outer_then_rejection_chronology_validated",
             "official_later_rejection", "first_runtime_entry_attempt",
             "publication_lock_continuity_incident",
             "v7_execution_allowed", "v7_runtime_surfaces_authoritative",
             "formal_global_closure_credit",
             "D02_unlock", "D02_gate_credit", "D02_task_credit",
             "D02_formal_pending_task_count", "D02_started",
         }, label + ":exact published/rejected v7 predecessor object")
    _validate_ordered_v7_exact10(
        section.get("ordered_published_exact10"), label)
    official = section.get("official_later_rejection", {})
    attempt = section.get("first_runtime_entry_attempt", {})
    need(isinstance(official, dict) and set(official) == {
             "path", "namespace_path", "file_sha256", "object_sha256",
             "schema", "status", "reason", "namespace_mode",
             "namespace_nlink", "member_mode", "member_nlink",
             "exact_member_universe", "formal_global_closure_credit",
             "D02_unlock", "D02_gate_credit", "D02_task_credit",
             "D02_formal_pending_task_count", "D02_started",
             "overwrite_delete_or_reuse_allowed",
         } and
         official.get("path") == str(V7_OFFICIAL_REJECTION.relative_to(ROOT)) and
         official.get("namespace_path") ==
             str(V7_OFFICIAL_REJECTION_NAMESPACE.relative_to(ROOT)) and
         official.get("file_sha256") == V7_OFFICIAL_REJECTION_FILE_PIN and
         official.get("object_sha256") == V7_OFFICIAL_REJECTION_OBJECT_PIN and
         official.get("schema") ==
             "cm2.round306c79g.true-global-no-producer-consumer.v7.later-rejection" and
         official.get("status") ==
             "PERMANENT_FAIL_CLOSED_REJECTION__ZERO_CREDIT" and
         official.get("reason") == "ORPHANED_OR_INCOMPLETE_C79G_V7_SURFACE" and
         official.get("namespace_mode") == "0555" and
         official.get("namespace_nlink") == 2 and
         official.get("member_mode") == "0444" and
         official.get("member_nlink") == 1 and
         official.get("exact_member_universe") == ["rejection.json"] and
         official.get("formal_global_closure_credit") == 0 and
         official.get("D02_unlock") is False and
         official.get("D02_gate_credit") == 0 and
         official.get("D02_task_credit") == 0 and
         official.get("D02_formal_pending_task_count") == EXPECTED_PENDING_D02 and
         official.get("D02_started") is False and
         official.get("overwrite_delete_or_reuse_allowed") is False,
         label + ":official v7 rejection pins and zero-credit semantics")
    need(isinstance(attempt, dict) and set(attempt) == {
             "attempted", "producer_child_spawned", "candidate_write_started",
             "positive_runtime_surface_count"} and
         attempt.get("attempted") is False and
         attempt.get("producer_child_spawned") is False and
         attempt.get("candidate_write_started") is False and
         attempt.get("positive_runtime_surface_count") == 0,
         label + ":v7 runtime never entered before official rejection")
    _validate_v7_lock_continuity_incident(
        section.get("publication_lock_continuity_incident"), label)
    need(strict_bool_census["v7_recursive_exact_bool_unproved_count"] == 0 and
         strict_bool_census["v16r2_recursive_exact_bool_unproved_count"] == 0 and
         strict_bool_census["all_twelve_sources_AST_parsed_and_compiled_in_memory"]
             is True and
         strict_bool_census["compiled_code_executed"] is False,
         label + ":v7/v16r2 full-callsite strict-bool closure")
    need(section.get("all_ten_file_pins_match") is True and
         section.get("all_declared_object_pins_match") is True and
         section.get("all_ten_regular_0444_nlink1") is True and
         section.get("exact8_manifest_reconstructs_first_eight_in_order") is True and
         section.get("outer_last_pins_manifest_and_launcher") is True and
         section.get("outer_then_rejection_chronology_validated") is True and
         section.get("v7_execution_allowed") is False and
         section.get("v7_runtime_surfaces_authoritative") is False and
         section.get("formal_global_closure_credit") == 0 and
         section.get("D02_unlock") is False and
         section.get("D02_gate_credit") == 0 and
         section.get("D02_task_credit") == 0 and
         section.get("D02_formal_pending_task_count") == EXPECTED_PENDING_D02 and
         section.get("D02_started") is False,
         label + ":v7 exact10/rejection/incident zero-credit boundary")


def require_v5_positive_and_stage_surfaces_absent() -> None:
    """Use root-fd anchored openat2 to reject every known positive v5 surface."""
    need(hasattr(os, "O_PATH"), "Linux O_PATH required for v5 absence proof")
    library = _linux_libc()
    for path in V5_ALL_POSITIVE_AND_STAGE_SURFACES:
        how = OpenHow(
            getattr(os, "O_PATH") | os.O_CLOEXEC, 0,
            RESOLVE_NO_XDEV | RESOLVE_NO_MAGICLINKS |
            RESOLVE_NO_SYMLINKS | RESOLVE_BENEATH)
        ctypes.set_errno(0)
        descriptor = library.syscall(
            ctypes.c_long(437), ctypes.c_int(_COLD_WORKSPACE_ROOT_FD),
            ctypes.c_char_p(_root_relative(path)), ctypes.byref(how),
            ctypes.c_size_t(ctypes.sizeof(how)))
        if descriptor >= 0:
            os.close(int(descriptor))
            raise Reject("officially rejected v5 positive surface exists:" + str(path))
        code = ctypes.get_errno()
        need(code == errno.ENOENT,
             "v5 absence proof must be exact ENOENT:" + str(path) + ":" +
             os.strerror(code))


def require_v6_positive_and_stage_surfaces_absent() -> None:
    """Use root-fd anchored openat2 to reject every known positive v6 surface."""
    need(hasattr(os, "O_PATH"), "Linux O_PATH required for v6 absence proof")
    library = _linux_libc()
    for path in V6_ALL_POSITIVE_AND_STAGE_SURFACES:
        how = OpenHow(
            getattr(os, "O_PATH") | os.O_CLOEXEC, 0,
            RESOLVE_NO_XDEV | RESOLVE_NO_MAGICLINKS |
            RESOLVE_NO_SYMLINKS | RESOLVE_BENEATH)
        ctypes.set_errno(0)
        descriptor = library.syscall(
            ctypes.c_long(437), ctypes.c_int(_COLD_WORKSPACE_ROOT_FD),
            ctypes.c_char_p(_root_relative(path)), ctypes.byref(how),
            ctypes.c_size_t(ctypes.sizeof(how)))
        if descriptor >= 0:
            os.close(int(descriptor))
            raise Reject("officially rejected v6 positive surface exists:" + str(path))
        code = ctypes.get_errno()
        need(code == errno.ENOENT,
             "v6 absence proof must be exact ENOENT:" + str(path) + ":" +
             os.strerror(code))


def require_v7_positive_and_stage_surfaces_absent() -> None:
    """Use root-fd anchored openat2 to reject every known positive v7 surface."""
    need(hasattr(os, "O_PATH"), "Linux O_PATH required for v7 absence proof")
    library = _linux_libc()
    for path in V7_ALL_POSITIVE_AND_STAGE_SURFACES:
        how = OpenHow(
            getattr(os, "O_PATH") | os.O_CLOEXEC, 0,
            RESOLVE_NO_XDEV | RESOLVE_NO_MAGICLINKS |
            RESOLVE_NO_SYMLINKS | RESOLVE_BENEATH)
        ctypes.set_errno(0)
        descriptor = library.syscall(
            ctypes.c_long(437), ctypes.c_int(_COLD_WORKSPACE_ROOT_FD),
            ctypes.c_char_p(_root_relative(path)), ctypes.byref(how),
            ctypes.c_size_t(ctypes.sizeof(how)))
        if descriptor >= 0:
            os.close(int(descriptor))
            raise Reject("officially rejected v7 positive surface exists:" + str(path))
        code = ctypes.get_errno()
        need(code == errno.ENOENT,
             "v7 absence proof must be exact ENOENT:" + str(path) + ":" +
             os.strerror(code))


def require_v8_positive_and_stage_surfaces_absent() -> None:
    """Reject every fixed v8 positive/stage surface beneath the held root."""
    need(hasattr(os, "O_PATH"), "Linux O_PATH required for v8 absence proof")
    library = _linux_libc()
    for path in V8_ALL_POSITIVE_AND_STAGE_SURFACES:
        how = OpenHow(
            getattr(os, "O_PATH") | os.O_CLOEXEC, 0,
            RESOLVE_NO_XDEV | RESOLVE_NO_MAGICLINKS |
            RESOLVE_NO_SYMLINKS | RESOLVE_BENEATH)
        ctypes.set_errno(0)
        descriptor = library.syscall(
            ctypes.c_long(437), ctypes.c_int(_COLD_WORKSPACE_ROOT_FD),
            ctypes.c_char_p(_root_relative(path)), ctypes.byref(how),
            ctypes.c_size_t(ctypes.sizeof(how)))
        if descriptor >= 0:
            os.close(int(descriptor))
            raise Reject("officially rejected v8 positive surface exists:" + str(path))
        code = ctypes.get_errno()
        need(code == errno.ENOENT,
             "v8 absence proof must be exact ENOENT:" + str(path) + ":" +
             os.strerror(code))


def require_v9_positive_and_stage_surfaces_absent() -> None:
    """Reject every fixed v9 positive/stage surface beneath the held root."""
    need(hasattr(os, "O_PATH"), "Linux O_PATH required for v9 absence proof")
    library = _linux_libc()
    for path in V9_ALL_POSITIVE_AND_STAGE_SURFACES:
        how = OpenHow(
            getattr(os, "O_PATH") | os.O_CLOEXEC, 0,
            RESOLVE_NO_XDEV | RESOLVE_NO_MAGICLINKS |
            RESOLVE_NO_SYMLINKS | RESOLVE_BENEATH)
        ctypes.set_errno(0)
        descriptor = library.syscall(
            ctypes.c_long(437), ctypes.c_int(_COLD_WORKSPACE_ROOT_FD),
            ctypes.c_char_p(_root_relative(path)), ctypes.byref(how),
            ctypes.c_size_t(ctypes.sizeof(how)))
        if descriptor >= 0:
            os.close(int(descriptor))
            raise Reject("officially rejected v9 positive surface exists:" + str(path))
        code = ctypes.get_errno()
        need(code == errno.ENOENT,
             "v9 absence proof must be exact ENOENT:" + str(path) + ":" +
             os.strerror(code))


def require_v10_positive_and_stage_surfaces_absent() -> None:
    """Reject every fixed v10 positive/stage surface beneath the held root."""
    need(hasattr(os, "O_PATH"), "Linux O_PATH required for v10 absence proof")
    library = _linux_libc()
    for path in V10_ALL_POSITIVE_AND_STAGE_SURFACES:
        how = OpenHow(
            getattr(os, "O_PATH") | os.O_CLOEXEC, 0,
            RESOLVE_NO_XDEV | RESOLVE_NO_MAGICLINKS |
            RESOLVE_NO_SYMLINKS | RESOLVE_BENEATH)
        ctypes.set_errno(0)
        descriptor = library.syscall(
            ctypes.c_long(437), ctypes.c_int(_COLD_WORKSPACE_ROOT_FD),
            ctypes.c_char_p(_root_relative(path)), ctypes.byref(how),
            ctypes.c_size_t(ctypes.sizeof(how)))
        if descriptor >= 0:
            os.close(int(descriptor))
            raise Reject(
                "officially rejected v10 positive surface exists:" + str(path))
        code = ctypes.get_errno()
        need(code == errno.ENOENT,
             "v10 absence proof must be exact ENOENT:" + str(path) + ":" +
             os.strerror(code))


def require_v11_positive_and_stage_surfaces_absent() -> None:
    """Reject every fixed v11 positive/stage surface beneath the held root."""
    need(hasattr(os, "O_PATH"), "Linux O_PATH required for v11 absence proof")
    library = _linux_libc()
    for path in V11_ALL_POSITIVE_AND_STAGE_SURFACES:
        how = OpenHow(
            getattr(os, "O_PATH") | os.O_CLOEXEC, 0,
            RESOLVE_NO_XDEV | RESOLVE_NO_MAGICLINKS |
            RESOLVE_NO_SYMLINKS | RESOLVE_BENEATH)
        ctypes.set_errno(0)
        descriptor = library.syscall(
            ctypes.c_long(437), ctypes.c_int(_COLD_WORKSPACE_ROOT_FD),
            ctypes.c_char_p(_root_relative(path)), ctypes.byref(how),
            ctypes.c_size_t(ctypes.sizeof(how)))
        if descriptor >= 0:
            os.close(int(descriptor))
            raise Reject(
                "officially rejected v11 positive surface exists:" + str(path))
        code = ctypes.get_errno()
        need(code == errno.ENOENT,
             "v11 absence proof must be exact ENOENT:" + str(path) + ":" +
             os.strerror(code))


def require_v12_positive_and_stage_surfaces_absent() -> None:
    """Reject every fixed v12 positive/stage surface beneath the held root."""
    need(hasattr(os, "O_PATH"), "Linux O_PATH required for v12 absence proof")
    library = _linux_libc()
    for path in V12_ALL_POSITIVE_AND_STAGE_SURFACES:
        how = OpenHow(
            getattr(os, "O_PATH") | os.O_CLOEXEC, 0,
            RESOLVE_NO_XDEV | RESOLVE_NO_MAGICLINKS |
            RESOLVE_NO_SYMLINKS | RESOLVE_BENEATH)
        ctypes.set_errno(0)
        descriptor = library.syscall(
            ctypes.c_long(437), ctypes.c_int(_COLD_WORKSPACE_ROOT_FD),
            ctypes.c_char_p(_root_relative(path)), ctypes.byref(how),
            ctypes.c_size_t(ctypes.sizeof(how)))
        if descriptor >= 0:
            os.close(int(descriptor))
            raise Reject(
                "officially rejected v12 positive surface exists:" + str(path))
        code = ctypes.get_errno()
        need(code == errno.ENOENT,
             "v12 absence proof must be exact ENOENT:" + str(path) + ":" +
             os.strerror(code))


def _nonzero_lower_sha256(value: Any) -> bool:
    """Return an exact bool for one nonzero lowercase SHA-256 text value."""
    return (isinstance(value, str) and len(value) == 64 and
            value != "0" * 64 and
            all(character in "0123456789abcdef" for character in value))


def _validate_final_static_audit(
        audit: Mapping[str, Any], self_guard: HeldSelf,
        by_path: Mapping[Path, HeldPinnedInput],
        transition_guard: HeldPinnedInput,
        transition: Mapping[str, Any]) -> None:
    """Fail closed on every final v16r2 dual-static-audit acceptance field.

    The launcher-template input is deliberately a pre-injection template pin,
    not the installed launcher's final file hash.  Its authority is closed by
    A/B equality, the three-way normalized digest, and the mandatory final
    post-injection normalized replay assertion.
    """
    need(set(audit) == {
             "schema", "status", "audit_path",
             "effective_checkpoint_object_sha256", "audited_v16r2_bundle",
             "predecessor_v3_exact10_regression",
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
             "published_then_officially_rejected_predecessor_v14",
             "rejected_prepublication_v13_supersession_receipt",
             "v10_colon_prefix_witness",
             "v11_dual_validator_divergence_incident",
             "v12_v5_rejection_shape_incident",
             "historical_rejection_exact_keyset_witness",
             "dual_independent_static_checkers",
             "coherent_attack_static_census",
             "schema_and_constructor_closure",
             "sealed_exec_and_no_producer_static_proof",
             "static_credit_census", "static_no_run",
             "final_audit_acceptance", "object_sha256",
         } and
         audit.get("schema") ==
             "cm2.round306c79g.true-global-no-producer-consumer."
             "static-audit.v16r2" and
         audit.get("status") ==
             "PASS_DUAL_STATIC_PIN_NORMALIZED_AST_GO_V16R2__"
             "PHYSICAL_COLD_FREEZE_PENDING__"
             "RUNTIME_NOT_AUTHORIZED" and
         audit.get("audit_path") == str(STATIC_AUDIT_V16R2.relative_to(ROOT)) and
         audit.get("effective_checkpoint_object_sha256") ==
             UPSTREAM_CHECKPOINT_OBJECT_PIN,
         "final v16r2 static audit exact top-level PASS_V16R2 closure")
    _validate_v12_regression_section(
        audit.get("published_then_officially_rejected_predecessor_v12"),
        "final v16r2 static audit v12 predecessor")
    supersession_receipt = self_guard.v13_supersession_receipt
    need(isinstance(supersession_receipt, dict) and
         audit.get("rejected_prepublication_v13_supersession_receipt") ==
             _expected_rejected_prepublication_v13_receipt(
                 supersession_receipt),
         "final v16r2 static audit rejected-prepublication v13 receipt")
    need(audit.get("v12_v5_rejection_shape_incident") ==
             V12_V5_REJECTION_SHAPE_INCIDENT and
         audit.get("historical_rejection_exact_keyset_witness") ==
             list(HISTORICAL_REJECTION_EXACT_KEYSET_WITNESS),
         "final v16r2 static audit v12 incident and exact9 historical witness")

    dual = audit.get("dual_independent_static_checkers", {})
    need(isinstance(dual, dict) and set(dual) == {
             "checker_A", "checker_B",
             "checker_C_common_census_and_pin_normalized_ast_reproduction",
             "v10_colon_prefix_helper_consensus",
             "independent_pin_normalizer_count", "all_pin_normalizers_equal",
             "pin_normalized_ast_algorithm",
             "pin_normalized_current_base7_key_order",
             "pin_normalization_forces_final_base7_installed_false",
             "pin_normalization_preserves_v14_supersession_receipt_and_all_historical_pins",
             "pin_normalization_removes_current_audit_hash_dependency",
             "independent_common_callsite_implementation_count",
             "all_common_callsite_censuses_equal",
             "final_launcher_must_reproduce_pin_normalized_ast_after_pin_injection",
             "held_launcher_pin_normalized_ast_sha256",
             "actual_runtime_registry_shape_evidence",
         }, "final v16r2 static audit dual-checker exact8 closure")
    checker_a = dual.get("checker_A", {})
    checker_b = dual.get("checker_B", {})
    checker_c = dual.get(
        "checker_C_common_census_and_pin_normalized_ast_reproduction", {})
    helper_consensus = dual.get("v10_colon_prefix_helper_consensus", {})
    need(isinstance(checker_a, dict) and set(checker_a) == {
             "algorithm", "status", "input_sha256",
             "pin_normalized_launcher_ast_sha256",
             "wider_local_callsite_census_row_count",
             "wider_local_callsite_census_sha256", "arity_failure_count",
             "undefined_global_count", "python_literal_dict_count",
             "python_literal_dict_duplicate_key_count",
             "python_AST_and_compile_in_memory_file_count",
             "failed_static_check_count",
         } and
         isinstance(checker_b, dict) and set(checker_b) == {
             "algorithm", "status", "input_sha256",
             "pin_normalized_launcher_ast_sha256",
             "common_ordered_callsite_row_count",
             "common_ordered_callsite_census_sha256", "arity_failure_count",
             "starred_positional_total", "double_star_keyword_total",
             "undefined_global_count", "JSON_duplicate_key_count",
             "python_literal_dict_duplicate_key_count",
             "object_closure_failure_count", "pin_failure_count",
             "failed_static_check_count",
         } and
         isinstance(checker_c, dict) and set(checker_c) == {
             "algorithm", "status", "pin_normalized_launcher_ast_sha256",
             "common_ordered_callsite_row_count",
             "common_ordered_callsite_census_sha256",
             "common_callsite_kind_census", "arity_failure_count",
             "starred_positional_total", "double_star_keyword_total",
             "failed_static_check_count",
         } and
         isinstance(helper_consensus, dict) and set(helper_consensus) == {
             "algorithm", "implementation_count", "ordered_source_roles",
             "normalized_helper_ast_sha256", "all_three_helpers_equal",
             "witness_exact_key_order", "witness_exact_key_count",
             "witness_object_sha256", "ordered_callsite_census",
             "ordered_callsite_census_sha256", "all_callsites_exact",
         }, "final v16r2 checker A/B/C and helper-consensus exact object closures")
    helper_callsites = helper_consensus.get("ordered_callsite_census")
    need(helper_consensus.get("algorithm") ==
             "THREE_SOURCE_NORMALIZED_FUNCTIONDEF_AST_AND_EXACT_CALLSITE_CENSUS_V1" and
         helper_consensus.get("implementation_count") == 3 and
         helper_consensus.get("ordered_source_roles") == [
             "producer", "consumer", "launcher"] and
         helper_consensus.get("normalized_helper_ast_sha256") ==
             V10_COLON_PREFIX_HELPER_NORMALIZED_AST_SHA256 and
         helper_consensus.get("all_three_helpers_equal") is True and
         helper_consensus.get("witness_exact_key_order") ==
             list(V10_COLON_PREFIX_WITNESS_KEY_ORDER) and
         helper_consensus.get("witness_exact_key_count") ==
             V10_COLON_PREFIX_WITNESS_KEY_COUNT and
         helper_consensus.get("witness_object_sha256") ==
             V10_COLON_PREFIX_WITNESS_OBJECT_PIN and
         isinstance(helper_callsites, list) and helper_callsites == [
             {
                 "source_role": "producer",
                 "enclosing_function": "hold_static_freeze_trust",
                 "direct_call_count": 1,
             },
             {
                 "source_role": "consumer",
                 "enclosing_function": "__init__",
                 "direct_call_count": 1,
             },
             {
                 "source_role": "consumer",
                 "enclosing_function": "terminal_replay",
                 "direct_call_count": 1,
             },
             {
                 "source_role": "launcher",
                 "enclosing_function": "bind_predecessors",
                 "direct_call_count": 1,
             },
             {
                 "source_role": "launcher",
                 "enclosing_function": "terminal_replay",
                 "direct_call_count": 1,
             },
         ] and
         helper_consensus.get("ordered_callsite_census_sha256") ==
             "1ca6de98366645a520cbc604990d71197f039207cacfa3291e9d87ff09a3cf57" and
         helper_consensus.get("ordered_callsite_census_sha256") ==
             digest(helper_callsites) and
         helper_consensus.get("all_callsites_exact") is True,
         "final v16r2 three-source helper AST, exact40 witness, and callsites")
    need(checker_a.get("algorithm") ==
             "AST_SYMBOL_TABLE_DATAFLOW_AND_PIN_NORMALIZER_CHECKER_A_V1" and
         checker_a.get("status") ==
             "GO_STATIC_CHECKER_A__PIN_NORMALIZED_AST_REPRODUCED__"
             "RUNTIME_NOT_AUTHORIZED" and
         checker_b.get("algorithm") ==
             "TOKEN_SYMBOL_TABLE_EXPLICIT_JSON_AND_PIN_NORMALIZER_"
             "CHECKER_B_V1" and
         checker_b.get("status") ==
             "GO_STATIC_CHECKER_B__PIN_NORMALIZED_AST_REPRODUCED__"
             "RUNTIME_NOT_AUTHORIZED" and
         checker_c.get("algorithm") ==
             "INDEPENDENT_LEXICAL_CALLSITE_AND_PIN_NORMALIZED_AST_"
             "REPRODUCER_C_V1" and
         checker_c.get("status") ==
             "GO_PIN_NORMALIZED_AST_AND_COMMON_DIGEST_REPRODUCED__"
             "RUNTIME_NOT_AUTHORIZED",
         "final v16r2 checker A/B/C algorithms and exact GO statuses")

    input_a = checker_a.get("input_sha256", {})
    input_b = checker_b.get("input_sha256", {})
    need(isinstance(input_a, dict) and isinstance(input_b, dict) and
         tuple(input_a) == STATIC_AUDIT_INPUT_KEY_ORDER and
         tuple(input_b) == STATIC_AUDIT_INPUT_KEY_ORDER and
         len(input_a) == len(input_b) == STATIC_AUDIT_INPUT_KEY_COUNT and
         digest(list(input_a)) == STATIC_AUDIT_INPUT_KEY_ORDER_SHA256 and
         digest(list(input_b)) == STATIC_AUDIT_INPUT_KEY_ORDER_SHA256 and
         input_a == input_b and
         _nonzero_lower_sha256(input_a.get("launcher_template")) is True,
         "final v16r2 checker A/B exact43 ordered identical input-pin closure")
    expected_inputs = {
        "schema": by_path[CLOSED_SCHEMA].file_sha256,
        "contract_file": by_path[CONTRACT].file_sha256,
        "contract_object": CONTRACT_OBJECT_PIN,
        "producer": self_guard.file_sha256,
        "consumer": by_path[COLD_EXACT8[4]].file_sha256,
        "transition_file": sha_bytes(transition_guard.raw),
        "transition_object": transition.get("object_sha256"),
        "launcher_template": input_a.get("launcher_template"),
        "v4_supersession_file": V4_REJECTION_SUPERSESSION_FILE_PIN,
        "v4_supersession_object": V4_REJECTION_SUPERSESSION_OBJECT_PIN,
        "v5_rejection_file": V5_OFFICIAL_REJECTION_FILE_PIN,
        "v5_rejection_object": V5_OFFICIAL_REJECTION_OBJECT_PIN,
        "v6_rejection_file": V6_OFFICIAL_REJECTION_FILE_PIN,
        "v6_rejection_object": V6_OFFICIAL_REJECTION_OBJECT_PIN,
        "v7_rejection_file": V7_OFFICIAL_REJECTION_FILE_PIN,
        "v7_rejection_object": V7_OFFICIAL_REJECTION_OBJECT_PIN,
        "v7_lock_continuity_incident_object":
            V7_LOCK_CONTINUITY_INCIDENT_OBJECT_PIN,
        "v8_rejection_file": V8_OFFICIAL_REJECTION_FILE_PIN,
        "v8_rejection_object": V8_OFFICIAL_REJECTION_OBJECT_PIN,
        "v8_launcher_file": V8_PUBLISHED_EXACT10_PINS[7][1],
        "v8_launcher_regression_defect_sha256":
            V8_LAUNCHER_REGRESSION_DEFECT_SHA256,
        "trusted_v8_rollout_control_flow_incident_digest":
            sha_bytes(canonical(V8_ROLLOUT_CONTROL_FLOW_INCIDENT)),
        "v9_rejection_file": V9_OFFICIAL_REJECTION_FILE_PIN,
        "v9_rejection_object": V9_OFFICIAL_REJECTION_OBJECT_PIN,
        "v9_launcher_file": V9_PUBLISHED_EXACT10_PINS[7][1],
        "v9_persisted_v6_proof_sha256": sha_bytes(canonical(
            V9_V6_DEFECT_SHAPE_DRIFT_INCIDENT[
                "persisted_held_self_identity_defect"])),
        "v9_expanded_v6_proof_sha256": sha_bytes(canonical(
            V9_V6_DEFECT_SHAPE_DRIFT_INCIDENT[
                "launcher_expanded_structural_evidence"])),
        "trusted_v9_proof_shape_drift_incident_digest":
            sha_bytes(canonical(V9_V6_DEFECT_SHAPE_DRIFT_INCIDENT)),
        "v10_rejection_file": V10_OFFICIAL_REJECTION_FILE_PIN,
        "v10_rejection_object": V10_OFFICIAL_REJECTION_OBJECT_PIN,
        "v10_producer_file": V10_PUBLISHED_EXACT10_PINS[3][1],
        "trusted_v10_regression_label_prefix_incident_digest":
            V10_REGRESSION_LABEL_PREFIX_INCIDENT_CANONICAL_SHA256,
        "v11_rejection_file": V11_OFFICIAL_REJECTION_FILE_PIN,
        "v11_rejection_object": V11_OFFICIAL_REJECTION_OBJECT_PIN,
        "v11_producer_file": V11_PUBLISHED_EXACT10_PINS[3][1],
        "v11_launcher_file": V11_PUBLISHED_EXACT10_PINS[7][1],
        "trusted_v11_dual_validator_divergence_incident_digest":
            V11_DUAL_VALIDATOR_DIVERGENCE_INCIDENT_CANONICAL_SHA256,
        "v12_rejection_file": V12_OFFICIAL_REJECTION_FILE_PIN,
        "v12_rejection_object": V12_OFFICIAL_REJECTION_OBJECT_PIN,
        "v12_producer_file": V12_PUBLISHED_EXACT10_PINS[3][1],
        "v12_consumer_file": V12_PUBLISHED_EXACT10_PINS[4][1],
        "v12_launcher_file": V12_PUBLISHED_EXACT10_PINS[7][1],
        "trusted_v12_v5_rejection_shape_incident_digest":
            V12_V5_REJECTION_SHAPE_INCIDENT_SHA256,
    }
    need(input_a == expected_inputs and
         all(_nonzero_lower_sha256(value) is True
             for value in input_a.values()),
         "final v16r2 checker inputs pin exact current core and append-only history")

    normalized_a = checker_a.get("pin_normalized_launcher_ast_sha256")
    normalized_b = checker_b.get("pin_normalized_launcher_ast_sha256")
    normalized_c = checker_c.get("pin_normalized_launcher_ast_sha256")
    common_count_b = checker_b.get("common_ordered_callsite_row_count")
    common_count_c = checker_c.get("common_ordered_callsite_row_count")
    common_digest_b = checker_b.get("common_ordered_callsite_census_sha256")
    common_digest_c = checker_c.get("common_ordered_callsite_census_sha256")
    need(_nonzero_lower_sha256(normalized_a) is True and
         normalized_a == normalized_b == normalized_c and
         type(common_count_b) is int and common_count_b > 0 and
         type(common_count_c) is int and common_count_c == common_count_b and
         _nonzero_lower_sha256(common_digest_b) is True and
         common_digest_b == common_digest_c,
         "final v16r2 three-way normalized and B/C common-callsite consensus")
    kind_census = checker_c.get("common_callsite_kind_census", {})
    need(isinstance(kind_census, dict) and set(kind_census) == {
             "module_function", "module_constructor", "self_instance_method",
             "cls_class_method", "localclass_static_method",
             "localclass_class_method", "localclass_instance_method",
         } and
         all(type(value) is int and value >= 0
             for value in kind_census.values()) and
         sum(kind_census.values()) == common_count_c,
         "final v16r2 checker C exact common-callsite kind census")
    need(type(checker_a.get("wider_local_callsite_census_row_count")) is int and
         checker_a.get("wider_local_callsite_census_row_count") > 0 and
         _nonzero_lower_sha256(
             checker_a.get("wider_local_callsite_census_sha256")) is True and
         type(checker_a.get("python_literal_dict_count")) is int and
         checker_a.get("python_literal_dict_count") >= 0 and
         type(checker_a.get(
             "python_AST_and_compile_in_memory_file_count")) is int and
         checker_a.get("python_AST_and_compile_in_memory_file_count") == 3,
         "final v16r2 checker A positive census and three-file in-memory compile")
    need(type(checker_a.get("arity_failure_count")) is int and
         checker_a.get("arity_failure_count") == 0 and
         type(checker_a.get("undefined_global_count")) is int and
         checker_a.get("undefined_global_count") == 0 and
         type(checker_a.get("python_literal_dict_duplicate_key_count")) is int and
         checker_a.get("python_literal_dict_duplicate_key_count") == 0 and
         type(checker_a.get("failed_static_check_count")) is int and
         checker_a.get("failed_static_check_count") == 0,
         "final v16r2 checker A zero arity/undefined/duplicate/failed counts")
    for key in (
            "arity_failure_count", "starred_positional_total",
            "double_star_keyword_total", "undefined_global_count",
            "JSON_duplicate_key_count",
            "python_literal_dict_duplicate_key_count",
            "object_closure_failure_count", "pin_failure_count",
            "failed_static_check_count"):
        need(type(checker_b.get(key)) is int and checker_b.get(key) == 0,
             "final v16r2 checker B exact integer zero:" + key)
    for key in (
            "arity_failure_count", "starred_positional_total",
            "double_star_keyword_total", "failed_static_check_count"):
        need(type(checker_c.get(key)) is int and checker_c.get(key) == 0,
             "final v16r2 checker C exact integer zero:" + key)
    need(type(dual.get("independent_pin_normalizer_count")) is int and
         dual.get("independent_pin_normalizer_count") == 3 and
         dual.get("all_pin_normalizers_equal") is True and
         dual.get("pin_normalized_ast_algorithm") ==
             "PYTHON_AST_DUMP_NO_ATTRIBUTES__FORCE_FINAL_BASE7_FALSE__"
             "CURRENT_V16R2_SIX_BASE7_FILE_F64_OBJECT_E64_OR_NONE__"
             "PRESERVE_V14_SUPERSESSION_RECEIPT_AND_ALL_HISTORICAL_PINS_V1" and
         dual.get("pin_normalized_current_base7_key_order") == [
             "SCHEMA", "CONTRACT", "PRODUCER", "CONSUMER", "TRANSITION",
             "AUDIT",
         ] and
         dual.get("pin_normalization_forces_final_base7_installed_false") is True and
         dual.get(
             "pin_normalization_preserves_v14_supersession_receipt_and_all_historical_pins") is True and
         dual.get("pin_normalization_removes_current_audit_hash_dependency") is True and
         type(dual.get(
             "independent_common_callsite_implementation_count")) is int and
         dual.get("independent_common_callsite_implementation_count") == 2 and
         dual.get("all_common_callsite_censuses_equal") is True and
         dual.get(
             "final_launcher_must_reproduce_pin_normalized_ast_after_pin_injection") is True and
         dual.get("held_launcher_pin_normalized_ast_sha256") == normalized_a,
         "final v16r2 dual exact 3/2 checker counts and type-exact consensuses")

    attacks = audit.get("coherent_attack_static_census", {})
    need(isinstance(attacks, dict) and set(attacks) == {
             "exact_unique_ordered_attack_count_required",
             "exact_unique_ordered_attack_count_observed",
             "attack_name_order_sha256",
             "all_mutations_route_through_production_validators",
             "C42_full10_hash_join_mutations_included",
             "C42_three_directory_mode_nlink_universe_guards_are_independent_live_physical_gates",
             "attack_execution_deferred_to_cold_runtime",
         } and
         type(attacks.get("exact_unique_ordered_attack_count_required")) is int and
         attacks.get("exact_unique_ordered_attack_count_required") == 137 and
         type(attacks.get("exact_unique_ordered_attack_count_observed")) is int and
         attacks.get("exact_unique_ordered_attack_count_observed") == 137 and
         attacks.get("attack_name_order_sha256") ==
             "90ca3c45b88c754a6fd7049579afec495c576957d564047966661647cb694f9d" and
         len(V11_INCIDENT_FORMAL_ATTACK_NAMES) == 16 and
         len(set(V11_INCIDENT_FORMAL_ATTACK_NAMES)) == 16 and
         attacks.get("all_mutations_route_through_production_validators") is True and
         attacks.get("C42_full10_hash_join_mutations_included") is True and
         attacks.get(
             "C42_three_directory_mode_nlink_universe_guards_are_independent_live_physical_gates") is True and
         attacks.get("attack_execution_deferred_to_cold_runtime") is True,
         "final v16r2 coherent attack exact7, 137/137 including ordered v11 "
         "incident attacks, routes, and deferred execution")

    sealed = audit.get("sealed_exec_and_no_producer_static_proof", {})
    need(isinstance(sealed, dict) and set(sealed) == {
             "all_memfd_seal_checks_precede_source_or_evidence_access",
             "all_memfd_seal_checks_are_exact_equality_not_subset_tests",
             "consumer_exec_source_coordination_root_fds_pairwise_distinct",
             "consumer_current_v16r2_producer_content_open_read_hash_decode_compile_import_or_execute_allowed",
             "consumer_v14_inherited_authority_exact12_bytes_read_only_noncredit_allowed",
             "consumer_independently_rederives_witness_from_inherited_held_fds",
             "consumer_producer_source_hold_api", "exact_required_seal_mask",
             "installed_and_exec_bytes_equal_and_terminally_replayed",
             "installed_source_mode", "installed_source_nlink",
             "launcher_bootstrap_exec_source_root_fds_distinct",
             "launcher_child_exec_source_coordination_root_fds_pairwise_distinct",
             "producer_exec_source_coordination_root_fds_pairwise_distinct",
             "sealed_exec_mode", "sealed_exec_nlink",
         } and
         sealed.get(
             "all_memfd_seal_checks_precede_source_or_evidence_access") is True and
         sealed.get(
             "all_memfd_seal_checks_are_exact_equality_not_subset_tests") is True and
         sealed.get(
             "consumer_exec_source_coordination_root_fds_pairwise_distinct") is True and
         sealed.get(
             "consumer_current_v16r2_producer_content_open_read_hash_decode_compile_import_or_execute_allowed") is False and
         sealed.get(
             "consumer_v14_inherited_authority_exact12_bytes_read_only_noncredit_allowed") is True and
         sealed.get(
             "consumer_independently_rederives_witness_from_inherited_held_fds") is True and
         sealed.get("consumer_producer_source_hold_api") ==
             "O_PATH|O_NOFOLLOW" and
         type(sealed.get("exact_required_seal_mask")) is int and
         sealed.get("exact_required_seal_mask") == 15 and
         sealed.get(
             "installed_and_exec_bytes_equal_and_terminally_replayed") is True and
         sealed.get("installed_source_mode") == "0444" and
         type(sealed.get("installed_source_nlink")) is int and
         sealed.get("installed_source_nlink") == 1 and
         sealed.get("launcher_bootstrap_exec_source_root_fds_distinct") is True and
         sealed.get(
             "launcher_child_exec_source_coordination_root_fds_pairwise_distinct") is True and
         sealed.get(
             "producer_exec_source_coordination_root_fds_pairwise_distinct") is True and
         sealed.get("sealed_exec_mode") == "0444" and
         type(sealed.get("sealed_exec_nlink")) is int and
         sealed.get("sealed_exec_nlink") == 0,
         "final v16r2 sealed-exec and scoped no-producer exact16 closure")

    closure = audit.get("schema_and_constructor_closure", {})
    need(isinstance(closure, dict) and set(closure) == {
             "strict_JSON_duplicate_keys_rejected", "schema_definition_count",
             "schema_ref_count", "unresolved_schema_ref_count",
             "closed_object_count",
             "closed_object_required_property_mismatch_count",
             "all_closed_object_required_sets_equal_property_sets",
             "all_schema_refs_resolve", "actual_schema_keyword_universe",
             "actual_schema_keyword_universe_sha256",
             "cold_launcher_supported_schema_keyword_universe",
             "cold_launcher_supported_schema_keyword_universe_sha256",
             "all_schema_validation_keywords_supported_by_cold_launcher",
             "unknown_schema_validation_keyword_count",
             "oneOf_keyword_absent_after_pin_definition_split",
             "python_literal_dict_duplicate_key_count", "undefined_global_count",
             "output_shape_key_counts",
             "launcher_and_consumer_laterRejection_key_sets_equal_schema",
             "launcher_request_consumer_request_key_sets_equal",
             "consumer_ACK_launcher_ACK_key_sets_and_census_values_equal",
         }, "final v16r2 schema/constructor exact21 closure")
    need(type(closure.get("schema_definition_count")) is int and
         closure.get("schema_definition_count") == 46 and
         type(closure.get("schema_ref_count")) is int and
         closure.get("schema_ref_count") == 242 and
         type(closure.get("unresolved_schema_ref_count")) is int and
         closure.get("unresolved_schema_ref_count") == 0 and
         type(closure.get("closed_object_count")) is int and
         closure.get("closed_object_count") == 52 and
         type(closure.get(
             "closed_object_required_property_mismatch_count")) is int and
         closure.get("closed_object_required_property_mismatch_count") == 0 and
         type(closure.get("unknown_schema_validation_keyword_count")) is int and
         closure.get("unknown_schema_validation_keyword_count") == 0 and
         type(closure.get("python_literal_dict_duplicate_key_count")) is int and
         closure.get("python_literal_dict_duplicate_key_count") == 0 and
         type(closure.get("undefined_global_count")) is int and
         closure.get("undefined_global_count") == 0,
         "final v16r2 schema 46 defs/242 refs/0 unresolved/52 closed/0 mismatch")
    need(closure.get("strict_JSON_duplicate_keys_rejected") is True and
         closure.get("all_closed_object_required_sets_equal_property_sets") is True and
         closure.get("all_schema_refs_resolve") is True and
         closure.get(
             "all_schema_validation_keywords_supported_by_cold_launcher") is True and
         closure.get("oneOf_keyword_absent_after_pin_definition_split") is True and
         closure.get(
             "launcher_and_consumer_laterRejection_key_sets_equal_schema") is True and
         closure.get("launcher_request_consumer_request_key_sets_equal") is True and
         closure.get(
             "consumer_ACK_launcher_ACK_key_sets_and_census_values_equal") is True,
         "final v16r2 schema and live-protocol type-exact bool closure")
    actual_keywords = [
        "$comment", "$defs", "$id", "$ref", "$schema",
        "additionalProperties", "const", "description", "items",
        "maxItems", "minItems", "minLength", "minimum", "pattern",
        "prefixItems", "properties", "required", "title", "type"]
    supported_keywords = [
        "$comment", "$defs", "$id", "$ref", "$schema",
        "additionalProperties", "const", "description", "items",
        "maxItems", "minItems", "minLength", "minimum", "pattern",
        "prefixItems", "properties", "required", "title", "type",
        "uniqueItems"]
    need(closure.get("actual_schema_keyword_universe") == actual_keywords and
         closure.get("actual_schema_keyword_universe_sha256") ==
             digest(actual_keywords) and
         closure.get("cold_launcher_supported_schema_keyword_universe") ==
             supported_keywords and
         closure.get("cold_launcher_supported_schema_keyword_universe_sha256") ==
             digest(supported_keywords),
         "final v16r2 exact canonical schema keyword universes and digests")
    shapes = closure.get("output_shape_key_counts", {})
    expected_shapes = {
        "selfIdentity": 33,
        "independentConsumerProof": 60,
        "staticFreezeProof": 84,
        "coldLaunchProof": 112,
        "laterRejection": 56,
        "producerSourceRegistry": 74,
        "liveRequest": 15,
        "liveACK": 32,
        "liveACKCensus": 42,
    }
    need(isinstance(shapes, dict) and set(shapes) == set(expected_shapes) and
         all(type(value) is int for value in shapes.values()) and
         shapes == expected_shapes,
         "final v16r2 exact nine output-shape key counts")

    acceptance = audit.get("final_audit_acceptance", {})
    need(isinstance(acceptance, dict) and set(acceptance) == {
             "current_draft_pass", "final_failed_static_check_count_required",
             "final_static_freeze_pass_required",
             "dual_static_checker_A_pin_normalized_ast_GO",
             "dual_static_checker_B_pin_normalized_ast_GO",
             "pin_normalized_launcher_ast_digest_consensus",
             "common_callsite_census_digest_consensus",
             "final_launcher_pin_normalized_ast_replay_required_after_pin_injection",
             "this_audit_authorizes_C79_runtime",
             "requires_cold_exact8_freeze_manifest_then_outer_last_and_terminal_replay",
         } and
         acceptance.get("current_draft_pass") is True and
         type(acceptance.get(
             "final_failed_static_check_count_required")) is int and
         acceptance.get("final_failed_static_check_count_required") == 0 and
         acceptance.get("final_static_freeze_pass_required") is True and
         acceptance.get("dual_static_checker_A_pin_normalized_ast_GO") is True and
         acceptance.get("dual_static_checker_B_pin_normalized_ast_GO") is True and
         acceptance.get("pin_normalized_launcher_ast_digest_consensus") is True and
         acceptance.get("common_callsite_census_digest_consensus") is True and
         acceptance.get(
             "final_launcher_pin_normalized_ast_replay_required_after_pin_injection") is True and
         acceptance.get("this_audit_authorizes_C79_runtime") is False and
         acceptance.get(
             "requires_cold_exact8_freeze_manifest_then_outer_last_and_terminal_replay") is True,
         "final v16r2 audit acceptance exact10 type-exact zero-runtime closure")


def _hold_modern_published_exact10(
        pins: tuple[tuple[Path, str, str | None], ...], version: int,
        label: str,
        inherited_by_path: Mapping[Path, int] | None = None
        ) -> tuple[list[HeldPinnedInput], dict[Path, HeldPinnedInput],
                             dict[str, Any], dict[str, bool]]:
    """Hold and close one v5-or-later published exact8/manifest/outer."""
    guards = [
        HeldPinnedInput(
            path, label + ":" + path.name, 0o444, file_pin,
            None if inherited_by_path is None else inherited_by_path.get(path))
        for path, file_pin, _ in pins
    ]
    by_path = {
        path: guards[index]
        for index, (path, _, _) in enumerate(pins)
    }
    need(len(guards) == len(by_path) == 10 and
         len({guard.identity for guard in guards}) == 10 and
         len({guard.mount_id for guard in guards}) == 1,
         label + ":exact10 unique held identities on one statx mount")
    for path, _, object_pin in pins:
        if object_pin is not None:
            value = strict_json(by_path[path].raw, label + ":object:" + path.name)
            need(isinstance(value, dict), label + ":object mapping:" + path.name)
            verify_object(value, label + ":object:" + path.name, object_pin)
    manifest_entries = parse_manifest_ordered(guards[8].raw, label + ":manifest")
    expected_manifest = [
        {"file_sha256": file_pin, "entry_name": str(path.relative_to(ROOT))}
        for path, file_pin, _ in pins[:8]
    ]
    need(manifest_entries == expected_manifest,
         label + ":manifest reconstructs exact ordered eight")
    outer = strict_json(guards[9].raw, label + ":outer-last")
    need(isinstance(outer, dict), label + ":outer-last object")
    verify_object(outer, label + ":outer-last", pins[9][2])
    chronology = cold_publication_chronology(
        [guard.before for guard in guards[:8]], guards[8].before, guards[9].before)
    expected_outer_entries = [
        {"path": item["entry_name"], "file_sha256": item["file_sha256"]}
        for item in expected_manifest
    ]
    need(set(outer) == {
             "schema", "status", "effective_checkpoint_object_sha256",
             "exact8_ordered_entries", "cold_launch_manifest", "cold_launcher",
             "all_exact8_regular_0444_nlink1_and_held_for_runtime",
             "outer_published_after_exact8_manifest",
             "runtime_entry_must_be_cold_launcher",
             "sole_external_static_file_anchor_is_launcher_sha256",
             "declared_external_tcb", "formal_global_closure_credit",
             "D02_unlock", "runtime_executed_during_static_freeze",
             "object_sha256"} and
         guards[9].raw == canonical(outer) + b"\n" and
         outer.get("schema") ==
             "cm2.round306c79g.true-global-no-producer-consumer."
             "cold-launch-outer-receipt.v" + str(version) and
         outer.get("status") ==
             "FROZEN_COLD_LAUNCH_OUTER_LAST__EXACT8_MANIFEST_CLOSED__RUNTIME_DEFERRED" and
         outer.get("effective_checkpoint_object_sha256") == UPSTREAM_CHECKPOINT_OBJECT_PIN and
         outer.get("exact8_ordered_entries") == expected_outer_entries and
         outer.get("cold_launch_manifest", {}).get("path") ==
             str(pins[8][0].relative_to(ROOT)) and
         outer.get("cold_launch_manifest", {}).get("file_sha256") == pins[8][1] and
         outer.get("cold_launch_manifest", {}).get("ordered_entry_count") == 8 and
         outer.get("cold_launcher", {}).get("path") ==
             str(pins[7][0].relative_to(ROOT)) and
         outer.get("cold_launcher", {}).get("file_sha256") == pins[7][1] and
         outer.get("formal_global_closure_credit") == 0 and
         outer.get("D02_unlock") is False and
         outer.get("runtime_executed_during_static_freeze") is False and
         all(chronology.values()),
         label + ":outer-last and chronology closure")
    return guards, by_path, outer, chronology


def hold_static_freeze_trust(self_guard: HeldSelf) -> dict[str, Any]:
    """Hold current v16r2 exact10 and every distinct append-only predecessor.

    Current exact8 begins with the v13 supersession receipt.  Prior history is
    98 identities; the v12 rejection singleton and frozen v13 source/pyc exact6
    make the predecessor census 116.  Current exact8 makes prepublication 124;
    manifest plus outer-last make the terminal census 126.
    """
    manifest_guard = HeldPinnedInput(
        COLD_MANIFEST, "C79g v16r2 cold-launch manifest", 0o444)
    outer_guard = HeldPinnedInput(
        COLD_OUTER, "C79g v16r2 cold-launch outer-last receipt", 0o444)
    manifest_entries = parse_manifest_ordered(
        manifest_guard.raw, "C79g v16r2 cold-launch exact8 manifest")
    expected_paths = [str(path.relative_to(ROOT)) for path in COLD_EXACT8]
    need([entry["entry_name"] for entry in manifest_entries] == expected_paths,
         "cold-launch manifest exact ordered eight paths")
    manifest_by_path = {
        ROOT / entry["entry_name"]: entry["file_sha256"]
        for entry in manifest_entries
    }
    need(len(manifest_by_path) == 8 and
         manifest_by_path[SELF] == self_guard.file_sha256 and
         manifest_by_path[CONTRACT] == CONTRACT_FILE_PIN and
         manifest_by_path[CLOSED_SCHEMA] == CLOSED_SCHEMA_FILE_PIN and
         manifest_by_path[V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT] ==
             V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT_FILE_PIN and
         COLD_EXACT8[0] == V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT,
         "cold-launch manifest active predecessor anchor and policy pins")

    by_path: dict[Path, HeldPinnedInput] = {}
    for path in COLD_EXACT8:
        if path != SELF:
            by_path[path] = HeldPinnedInput(
                path, "C79g v16r2 cold exact8:" + path.name, 0o444,
                manifest_by_path[path], self_guard.incident_fds.get(path))
    v12_rejection_guard = HeldPinnedInput(
        V12_OFFICIAL_REJECTION, "official v12 later rejection", 0o444,
        V12_OFFICIAL_REJECTION_FILE_PIN,
        self_guard.incident_fds.get(V12_OFFICIAL_REJECTION))
    v13_incident_guards = [
        HeldPinnedInput(
            path, "frozen v13 live incident:" + path.name, 0o444, file_pin,
            self_guard.incident_fds.get(path))
        for path, file_pin in V13_INCIDENT_EXACT6_PINS.items()
    ]
    need(len(v13_incident_guards) == 6 and
         len({guard.identity for guard in v13_incident_guards}) == 6 and
         [guard.file_sha256 for guard in v13_incident_guards] ==
             list(V13_INCIDENT_EXACT6_PINS.values()),
         "frozen v13 source-then-pyc exact6 held identity/hash order")
    v14_guards = [
        HeldPinnedInput(
            ROOT / relative_path,
            "frozen v14 published exact10:" + role,
            0o444, file_pin,
            self_guard.incident_fds.get(ROOT / relative_path))
        for role, relative_path, file_pin, _object_pin
        in V14_PUBLISHED_EXACT10_WITNESS
    ]
    need(len(v14_guards) == 10 and
         len({guard.identity for guard in v14_guards}) == 10 and
         len({guard.mount_id for guard in v14_guards}) == 1 and
         all(guard.mount_id == self_guard.mount_id
             for guard in v14_guards),
         "frozen v14 published exact10 held identities on one statx mount")
    v14_rejection_path = ROOT / V14_OFFICIAL_REJECTION_RELATIVE_PATH
    v14_rejection_guard = HeldPinnedInput(
        v14_rejection_path, "official v14 later rejection", 0o444,
        V14_OFFICIAL_REJECTION_FILE_PIN,
        self_guard.incident_fds.get(v14_rejection_path))
    need(v14_rejection_guard.mount_id == self_guard.mount_id and
         v14_rejection_guard.identity not in
             {guard.identity for guard in v14_guards},
         "official v14 rejection identity is distinct and on one mount")
    current_cold_ten_guards = [
        self_guard, *by_path.values(), manifest_guard, outer_guard]
    need(len(current_cold_ten_guards) == 10 and
         len({guard.identity for guard in current_cold_ten_guards}) == 10 and
         len({guard.mount_id for guard in current_cold_ten_guards}) == 1,
         "current v16r2 cold exact10 unique held identities on one statx mount")
    exact8_stats = [
        self_guard.before if path == SELF else by_path[path].before
        for path in COLD_EXACT8
    ]
    chronology = cold_publication_chronology(
        exact8_stats, manifest_guard.before, outer_guard.before)
    need(all(chronology.values()),
         "physical v16r2 exact8/manifest/outer freeze chronology")

    v12_guards, v12_by_path, v12_outer, v12_chronology = (
        _hold_modern_published_exact10(
            V12_PUBLISHED_EXACT10_PINS, 12, "published v12 exact10",
            self_guard.incident_fds))
    v11_rejection_guard = v12_by_path[V11_OFFICIAL_REJECTION]
    v11_guards, v11_by_path, v11_outer, v11_chronology = (
        _hold_modern_published_exact10(
            V11_PUBLISHED_EXACT10_PINS, 11, "published v11 exact10",
            self_guard.incident_fds))
    v10_rejection_guard = v11_by_path[V10_OFFICIAL_REJECTION]
    need(max(v12_guards[9].before.st_mtime_ns,
             v12_guards[9].before.st_ctime_ns) <
             min(v12_rejection_guard.before.st_mtime_ns,
                 v12_rejection_guard.before.st_ctime_ns),
         "official v12 rejection is strictly later than published v12 outer")
    v12_namespace_guard = HeldDirectory(
        V12_OFFICIAL_REJECTION_NAMESPACE, {V12_OFFICIAL_REJECTION.name},
        0o555, 2, "official v12 rejection singleton namespace")
    v12_namespace_member = os.stat(
        V12_OFFICIAL_REJECTION.name, dir_fd=v12_namespace_guard.fd,
        follow_symlinks=False)
    need((v12_namespace_member.st_dev, v12_namespace_member.st_ino) ==
             v12_rejection_guard.identity and
         v12_namespace_guard.mount_id == v12_rejection_guard.mount_id,
         "official v12 rejection namespace member equals held current base fd")
    v12_rejection = strict_json(
        v12_rejection_guard.raw, "official v12 later rejection")
    need(isinstance(v12_rejection, dict), "official v12 rejection object")
    verify_object(
        v12_rejection, "official v12 later rejection",
        V12_OFFICIAL_REJECTION_OBJECT_PIN)
    need(v12_rejection_guard.raw == canonical(v12_rejection) + b"\n" and
         set(v12_rejection) == V12_OFFICIAL_REJECTION_EXACT54_KEYS and
         v12_rejection.get("status") ==
             "PERMANENT_FAIL_CLOSED_REJECTION__ZERO_CREDIT" and
         v12_rejection.get("rejection_reason") ==
             "ORPHANED_OR_INCOMPLETE_C79G_V12_SURFACE" and
         v12_rejection.get("formal_global_closure_credit") == 0 and
         v12_rejection.get("D02_unlock") is False and
         v12_rejection.get("D02_gate_credit") == 0 and
         v12_rejection.get("D02_task_credit") == 0 and
         v12_rejection.get("D02_formal_pending_task_count") ==
             EXPECTED_PENDING_D02 and
         v12_rejection.get("D02_started") is False and
         v12_rejection.get("standalone_authority") is False and
         v12_rejection.get("overwrite_delete_or_reuse_allowed") is False,
         "official v12 rejection exact54 canonical zero-credit closure")
    require_v12_positive_and_stage_surfaces_absent()
    v11_rejection = strict_json(
        v11_rejection_guard.raw, "official v11 later rejection")
    need(isinstance(v11_rejection, dict), "official v11 rejection object")
    verify_object(
        v11_rejection, "official v11 later rejection",
        V11_OFFICIAL_REJECTION_OBJECT_PIN)
    need(set(v11_rejection) == {
             "D02_formal_pending_task_count", "D02_gate_credit", "D02_started",
             "D02_task_credit", "D02_unlock", "closed_schema_file_sha256",
             "cold_launcher_file_sha256", "cold_manifest_file_sha256",
             "cold_outer_file_sha256", "cold_outer_object_sha256",
             "commit_operation", "consumer_file_sha256", "contract_file_sha256",
             "contract_object_sha256", "effective_checkpoint_object_sha256",
             "file_fsync_required", "formal_global_closure_credit",
             "idempotent_existing_recovery_re_fsyncs_rejection_file_namespace_and_runtime_parent",
             "namespace_at_rest_mode", "namespace_exact_path",
             "namespace_fsync_required_after_file_and_after_reseal",
             "namespace_lock_held_write_window_mode", "object_sha256",
             "official_writer_coordination_lock_held_for_entire_reject_command",
             "official_writer_coordination_lock_policy",
             "overwrite_delete_or_reuse_allowed",
             "partial_malformed_or_extra_namespace_entry_revokes_authority",
             "producer_file_sha256", "rejection_file_mode", "rejection_file_nlink",
             "rejection_reason", "runtime_parent_fsync_required_after_namespace_creation",
             "schema", "standalone_authority", "status", "target_exact_path",
             "target_is_protocol_and_checkpoint_deterministic",
             "v10_official_rejection_file_sha256",
             "v10_official_rejection_object_sha256",
             "v4_rejection_supersession_file_sha256",
             "v4_rejection_supersession_object_sha256",
             "v5_official_rejection_file_sha256",
             "v5_official_rejection_object_sha256",
             "v6_official_rejection_file_sha256",
             "v6_official_rejection_object_sha256",
             "v7_official_rejection_file_sha256",
             "v7_official_rejection_object_sha256",
             "v7_publication_lock_continuity_incident_object_sha256",
             "v8_official_rejection_file_sha256",
             "v8_official_rejection_object_sha256",
             "v9_official_rejection_file_sha256",
             "v9_official_rejection_object_sha256",
         } and
         v11_rejection_guard.raw == canonical(v11_rejection) + b"\n" and
         v11_rejection.get("schema") ==
             "cm2.round306c79g.true-global-no-producer-consumer.v11.later-rejection" and
         v11_rejection.get("status") ==
             "PERMANENT_FAIL_CLOSED_REJECTION__ZERO_CREDIT" and
         v11_rejection.get("rejection_reason") ==
             "ORPHANED_OR_INCOMPLETE_C79G_V11_SURFACE" and
         v11_rejection.get("effective_checkpoint_object_sha256") ==
             UPSTREAM_CHECKPOINT_OBJECT_PIN and
         v11_rejection.get("target_exact_path") ==
             str(V11_OFFICIAL_REJECTION.relative_to(ROOT)) and
         v11_rejection.get("namespace_exact_path") ==
             str(V11_OFFICIAL_REJECTION_NAMESPACE.relative_to(ROOT)) and
         v11_rejection.get("closed_schema_file_sha256") ==
             V11_PUBLISHED_EXACT10_PINS[1][1] and
         v11_rejection.get("contract_file_sha256") ==
             V11_PUBLISHED_EXACT10_PINS[2][1] and
         v11_rejection.get("contract_object_sha256") ==
             V11_PUBLISHED_EXACT10_PINS[2][2] and
         v11_rejection.get("producer_file_sha256") ==
             V11_PUBLISHED_EXACT10_PINS[3][1] and
         v11_rejection.get("consumer_file_sha256") ==
             V11_PUBLISHED_EXACT10_PINS[4][1] and
         v11_rejection.get("cold_launcher_file_sha256") ==
             V11_PUBLISHED_EXACT10_PINS[7][1] and
         v11_rejection.get("cold_manifest_file_sha256") ==
             V11_PUBLISHED_EXACT10_PINS[8][1] and
         v11_rejection.get("cold_outer_file_sha256") ==
             V11_PUBLISHED_EXACT10_PINS[9][1] and
         v11_rejection.get("cold_outer_object_sha256") ==
             V11_PUBLISHED_EXACT10_PINS[9][2] and
         v11_rejection.get("v10_official_rejection_file_sha256") ==
             V10_OFFICIAL_REJECTION_FILE_PIN and
         v11_rejection.get("v10_official_rejection_object_sha256") ==
             V10_OFFICIAL_REJECTION_OBJECT_PIN and
         v11_rejection.get("namespace_at_rest_mode") == "0555" and
         v11_rejection.get("namespace_lock_held_write_window_mode") == "0755" and
         v11_rejection.get("rejection_file_mode") == "0444" and
         v11_rejection.get("rejection_file_nlink") == 1 and
         v11_rejection.get("formal_global_closure_credit") == 0 and
         v11_rejection.get("D02_gate_credit") == 0 and
         v11_rejection.get("D02_task_credit") == 0 and
         v11_rejection.get("D02_unlock") is False and
         v11_rejection.get("D02_started") is False and
         v11_rejection.get("D02_formal_pending_task_count") ==
             EXPECTED_PENDING_D02 and
         v11_rejection.get("standalone_authority") is False and
         v11_rejection.get("overwrite_delete_or_reuse_allowed") is False,
         "official v11 rejection exact canonical 52-key zero-credit closure")
    need(max(v11_guards[9].before.st_mtime_ns,
             v11_guards[9].before.st_ctime_ns) <
             min(v11_rejection_guard.before.st_mtime_ns,
                 v11_rejection_guard.before.st_ctime_ns),
         "official v11 rejection is strictly later than published v11 outer")
    v11_namespace_guard = HeldDirectory(
        V11_OFFICIAL_REJECTION_NAMESPACE, {V11_OFFICIAL_REJECTION.name},
        0o555, 2, "official v11 rejection singleton namespace")
    v11_namespace_member = os.stat(
        V11_OFFICIAL_REJECTION.name, dir_fd=v11_namespace_guard.fd,
        follow_symlinks=False)
    need((v11_namespace_member.st_dev, v11_namespace_member.st_ino) ==
             v11_rejection_guard.identity and
         v11_namespace_guard.mount_id == v11_rejection_guard.mount_id,
         "official v11 rejection namespace member equals held current base fd")
    require_v11_positive_and_stage_surfaces_absent()

    v10_guards, v10_by_path, v10_outer, v10_chronology = (
        _hold_modern_published_exact10(
            V10_PUBLISHED_EXACT10_PINS, 10, "published v10 exact10",
            self_guard.incident_fds))
    v9_rejection_guard = v10_by_path[V9_OFFICIAL_REJECTION]
    v10_rejection = strict_json(
        v10_rejection_guard.raw, "official v10 later rejection")
    need(isinstance(v10_rejection, dict), "official v10 rejection object")
    verify_object(
        v10_rejection, "official v10 later rejection",
        V10_OFFICIAL_REJECTION_OBJECT_PIN)
    need(set(v10_rejection) == {
             "D02_formal_pending_task_count", "D02_gate_credit", "D02_started",
             "D02_task_credit", "D02_unlock", "closed_schema_file_sha256",
             "cold_launcher_file_sha256", "cold_manifest_file_sha256",
             "cold_outer_file_sha256", "cold_outer_object_sha256",
             "commit_operation", "consumer_file_sha256", "contract_file_sha256",
             "contract_object_sha256", "effective_checkpoint_object_sha256",
             "file_fsync_required", "formal_global_closure_credit",
             "idempotent_existing_recovery_re_fsyncs_rejection_file_namespace_and_runtime_parent",
             "namespace_at_rest_mode", "namespace_exact_path",
             "namespace_fsync_required_after_file_and_after_reseal",
             "namespace_lock_held_write_window_mode", "object_sha256",
             "official_writer_coordination_lock_held_for_entire_reject_command",
             "official_writer_coordination_lock_policy",
             "overwrite_delete_or_reuse_allowed",
             "partial_malformed_or_extra_namespace_entry_revokes_authority",
             "producer_file_sha256", "rejection_file_mode", "rejection_file_nlink",
             "rejection_reason", "runtime_parent_fsync_required_after_namespace_creation",
             "schema", "standalone_authority", "status", "target_exact_path",
             "target_is_protocol_and_checkpoint_deterministic",
             "v4_rejection_supersession_file_sha256",
             "v4_rejection_supersession_object_sha256",
             "v5_official_rejection_file_sha256",
             "v5_official_rejection_object_sha256",
             "v6_official_rejection_file_sha256",
             "v6_official_rejection_object_sha256",
             "v7_official_rejection_file_sha256",
             "v7_official_rejection_object_sha256",
             "v7_publication_lock_continuity_incident_object_sha256",
             "v8_official_rejection_file_sha256",
             "v8_official_rejection_object_sha256",
             "v9_official_rejection_file_sha256",
             "v9_official_rejection_object_sha256",
         } and
         v10_rejection_guard.raw == canonical(v10_rejection) + b"\n" and
         v10_rejection.get("schema") ==
             "cm2.round306c79g.true-global-no-producer-consumer.v10.later-rejection" and
         v10_rejection.get("status") ==
             "PERMANENT_FAIL_CLOSED_REJECTION__ZERO_CREDIT" and
         v10_rejection.get("rejection_reason") ==
             "ORPHANED_OR_INCOMPLETE_C79G_V10_SURFACE" and
         v10_rejection.get("effective_checkpoint_object_sha256") ==
             UPSTREAM_CHECKPOINT_OBJECT_PIN and
         v10_rejection.get("target_exact_path") ==
             str(V10_OFFICIAL_REJECTION.relative_to(ROOT)) and
         v10_rejection.get("namespace_exact_path") ==
             str(V10_OFFICIAL_REJECTION_NAMESPACE.relative_to(ROOT)) and
         v10_rejection.get("closed_schema_file_sha256") ==
             V10_PUBLISHED_EXACT10_PINS[1][1] and
         v10_rejection.get("contract_file_sha256") ==
             V10_PUBLISHED_EXACT10_PINS[2][1] and
         v10_rejection.get("contract_object_sha256") ==
             V10_PUBLISHED_EXACT10_PINS[2][2] and
         v10_rejection.get("producer_file_sha256") ==
             V10_PUBLISHED_EXACT10_PINS[3][1] and
         v10_rejection.get("consumer_file_sha256") ==
             V10_PUBLISHED_EXACT10_PINS[4][1] and
         v10_rejection.get("cold_launcher_file_sha256") ==
             V10_PUBLISHED_EXACT10_PINS[7][1] and
         v10_rejection.get("cold_manifest_file_sha256") ==
             V10_PUBLISHED_EXACT10_PINS[8][1] and
         v10_rejection.get("cold_outer_file_sha256") ==
             V10_PUBLISHED_EXACT10_PINS[9][1] and
         v10_rejection.get("cold_outer_object_sha256") ==
             V10_PUBLISHED_EXACT10_PINS[9][2] and
         v10_rejection.get("v4_rejection_supersession_file_sha256") ==
             V4_REJECTION_SUPERSESSION_FILE_PIN and
         v10_rejection.get("v4_rejection_supersession_object_sha256") ==
             V4_REJECTION_SUPERSESSION_OBJECT_PIN and
         v10_rejection.get("v5_official_rejection_file_sha256") ==
             V5_OFFICIAL_REJECTION_FILE_PIN and
         v10_rejection.get("v5_official_rejection_object_sha256") ==
             V5_OFFICIAL_REJECTION_OBJECT_PIN and
         v10_rejection.get("v6_official_rejection_file_sha256") ==
             V6_OFFICIAL_REJECTION_FILE_PIN and
         v10_rejection.get("v6_official_rejection_object_sha256") ==
             V6_OFFICIAL_REJECTION_OBJECT_PIN and
         v10_rejection.get("v7_official_rejection_file_sha256") ==
             V7_OFFICIAL_REJECTION_FILE_PIN and
         v10_rejection.get("v7_official_rejection_object_sha256") ==
             V7_OFFICIAL_REJECTION_OBJECT_PIN and
         v10_rejection.get(
             "v7_publication_lock_continuity_incident_object_sha256") ==
             V7_LOCK_CONTINUITY_INCIDENT_OBJECT_PIN and
         v10_rejection.get("v8_official_rejection_file_sha256") ==
             V8_OFFICIAL_REJECTION_FILE_PIN and
         v10_rejection.get("v8_official_rejection_object_sha256") ==
             V8_OFFICIAL_REJECTION_OBJECT_PIN and
         v10_rejection.get("v9_official_rejection_file_sha256") ==
             V9_OFFICIAL_REJECTION_FILE_PIN and
         v10_rejection.get("v9_official_rejection_object_sha256") ==
             V9_OFFICIAL_REJECTION_OBJECT_PIN and
         v10_rejection.get("namespace_at_rest_mode") == "0555" and
         v10_rejection.get("namespace_lock_held_write_window_mode") == "0755" and
         v10_rejection.get("rejection_file_mode") == "0444" and
         v10_rejection.get("rejection_file_nlink") == 1 and
         v10_rejection.get("formal_global_closure_credit") == 0 and
         v10_rejection.get("D02_gate_credit") == 0 and
         v10_rejection.get("D02_task_credit") == 0 and
         v10_rejection.get("D02_unlock") is False and
         v10_rejection.get("D02_started") is False and
         v10_rejection.get("D02_formal_pending_task_count") ==
             EXPECTED_PENDING_D02 and
         v10_rejection.get("standalone_authority") is False and
         v10_rejection.get("overwrite_delete_or_reuse_allowed") is False,
         "official v10 rejection exact canonical 50-key zero-credit closure")
    need(max(v10_guards[9].before.st_mtime_ns,
             v10_guards[9].before.st_ctime_ns) <
             min(v10_rejection_guard.before.st_mtime_ns,
                 v10_rejection_guard.before.st_ctime_ns),
         "official v10 rejection is strictly later than published v10 outer")
    v10_namespace_guard = HeldDirectory(
        V10_OFFICIAL_REJECTION_NAMESPACE, {V10_OFFICIAL_REJECTION.name},
        0o555, 2, "official v10 rejection singleton namespace")
    v10_namespace_member = os.stat(
        V10_OFFICIAL_REJECTION.name, dir_fd=v10_namespace_guard.fd,
        follow_symlinks=False)
    need((v10_namespace_member.st_dev, v10_namespace_member.st_ino) ==
             v10_rejection_guard.identity and
         v10_namespace_guard.mount_id == v10_rejection_guard.mount_id,
         "official v10 rejection namespace member equals held current base fd")
    require_v10_positive_and_stage_surfaces_absent()

    v9_guards, v9_by_path, v9_outer, v9_chronology = (
        _hold_modern_published_exact10(
            V9_PUBLISHED_EXACT10_PINS, 9, "published v9 exact10",
            self_guard.incident_fds))
    v8_rejection_guard = v9_by_path[V8_OFFICIAL_REJECTION]
    v9_rejection = strict_json(
        v9_rejection_guard.raw, "official v9 later rejection")
    need(isinstance(v9_rejection, dict), "official v9 rejection object")
    verify_object(
        v9_rejection, "official v9 later rejection",
        V9_OFFICIAL_REJECTION_OBJECT_PIN)
    need(set(v9_rejection) == {
             "D02_formal_pending_task_count", "D02_gate_credit", "D02_started",
             "D02_task_credit", "D02_unlock", "closed_schema_file_sha256",
             "cold_launcher_file_sha256", "cold_manifest_file_sha256",
             "cold_outer_file_sha256", "cold_outer_object_sha256",
             "commit_operation", "consumer_file_sha256", "contract_file_sha256",
             "contract_object_sha256", "effective_checkpoint_object_sha256",
             "file_fsync_required", "formal_global_closure_credit",
             "idempotent_existing_recovery_re_fsyncs_rejection_file_namespace_and_runtime_parent",
             "namespace_at_rest_mode", "namespace_exact_path",
             "namespace_fsync_required_after_file_and_after_reseal",
             "namespace_lock_held_write_window_mode", "object_sha256",
             "official_writer_coordination_lock_held_for_entire_reject_command",
             "official_writer_coordination_lock_policy",
             "overwrite_delete_or_reuse_allowed",
             "partial_malformed_or_extra_namespace_entry_revokes_authority",
             "producer_file_sha256", "rejection_file_mode", "rejection_file_nlink",
             "rejection_reason", "runtime_parent_fsync_required_after_namespace_creation",
             "schema", "standalone_authority", "status", "target_exact_path",
             "target_is_protocol_and_checkpoint_deterministic",
             "v4_rejection_supersession_file_sha256",
             "v4_rejection_supersession_object_sha256",
             "v5_official_rejection_file_sha256",
             "v5_official_rejection_object_sha256",
             "v6_official_rejection_file_sha256",
             "v6_official_rejection_object_sha256",
             "v7_official_rejection_file_sha256",
             "v7_official_rejection_object_sha256",
             "v7_publication_lock_continuity_incident_object_sha256",
             "v8_official_rejection_file_sha256",
             "v8_official_rejection_object_sha256",
         } and
         v9_rejection_guard.raw == canonical(v9_rejection) + b"\n" and
         v9_rejection.get("schema") ==
             "cm2.round306c79g.true-global-no-producer-consumer.v9.later-rejection" and
         v9_rejection.get("status") ==
             "PERMANENT_FAIL_CLOSED_REJECTION__ZERO_CREDIT" and
         v9_rejection.get("rejection_reason") ==
             "ORPHANED_OR_INCOMPLETE_C79G_V9_SURFACE" and
         v9_rejection.get("effective_checkpoint_object_sha256") ==
             UPSTREAM_CHECKPOINT_OBJECT_PIN and
         v9_rejection.get("target_exact_path") ==
             str(V9_OFFICIAL_REJECTION.relative_to(ROOT)) and
         v9_rejection.get("namespace_exact_path") ==
             str(V9_OFFICIAL_REJECTION_NAMESPACE.relative_to(ROOT)) and
         v9_rejection.get("closed_schema_file_sha256") ==
             V9_PUBLISHED_EXACT10_PINS[1][1] and
         v9_rejection.get("contract_file_sha256") ==
             V9_PUBLISHED_EXACT10_PINS[2][1] and
         v9_rejection.get("contract_object_sha256") ==
             V9_PUBLISHED_EXACT10_PINS[2][2] and
         v9_rejection.get("producer_file_sha256") ==
             V9_PUBLISHED_EXACT10_PINS[3][1] and
         v9_rejection.get("consumer_file_sha256") ==
             V9_PUBLISHED_EXACT10_PINS[4][1] and
         v9_rejection.get("cold_launcher_file_sha256") ==
             V9_PUBLISHED_EXACT10_PINS[7][1] and
         v9_rejection.get("cold_manifest_file_sha256") ==
             V9_PUBLISHED_EXACT10_PINS[8][1] and
         v9_rejection.get("cold_outer_file_sha256") ==
             V9_PUBLISHED_EXACT10_PINS[9][1] and
         v9_rejection.get("cold_outer_object_sha256") ==
             V9_PUBLISHED_EXACT10_PINS[9][2] and
         v9_rejection.get("v4_rejection_supersession_file_sha256") ==
             V4_REJECTION_SUPERSESSION_FILE_PIN and
         v9_rejection.get("v4_rejection_supersession_object_sha256") ==
             V4_REJECTION_SUPERSESSION_OBJECT_PIN and
         v9_rejection.get("v5_official_rejection_file_sha256") ==
             V5_OFFICIAL_REJECTION_FILE_PIN and
         v9_rejection.get("v5_official_rejection_object_sha256") ==
             V5_OFFICIAL_REJECTION_OBJECT_PIN and
         v9_rejection.get("v6_official_rejection_file_sha256") ==
             V6_OFFICIAL_REJECTION_FILE_PIN and
         v9_rejection.get("v6_official_rejection_object_sha256") ==
             V6_OFFICIAL_REJECTION_OBJECT_PIN and
         v9_rejection.get("v7_official_rejection_file_sha256") ==
             V7_OFFICIAL_REJECTION_FILE_PIN and
         v9_rejection.get("v7_official_rejection_object_sha256") ==
             V7_OFFICIAL_REJECTION_OBJECT_PIN and
         v9_rejection.get("v7_publication_lock_continuity_incident_object_sha256") ==
             V7_LOCK_CONTINUITY_INCIDENT_OBJECT_PIN and
         v9_rejection.get("v8_official_rejection_file_sha256") ==
             V8_OFFICIAL_REJECTION_FILE_PIN and
         v9_rejection.get("v8_official_rejection_object_sha256") ==
             V8_OFFICIAL_REJECTION_OBJECT_PIN and
         v9_rejection.get("namespace_at_rest_mode") == "0555" and
         v9_rejection.get("namespace_lock_held_write_window_mode") == "0755" and
         v9_rejection.get("rejection_file_mode") == "0444" and
         v9_rejection.get("rejection_file_nlink") == 1 and
         v9_rejection.get("formal_global_closure_credit") == 0 and
         v9_rejection.get("D02_gate_credit") == 0 and
         v9_rejection.get("D02_task_credit") == 0 and
         v9_rejection.get("D02_unlock") is False and
         v9_rejection.get("D02_started") is False and
         v9_rejection.get("D02_formal_pending_task_count") ==
             EXPECTED_PENDING_D02 and
         v9_rejection.get("standalone_authority") is False and
         v9_rejection.get("overwrite_delete_or_reuse_allowed") is False,
         "official v9 rejection exact canonical 48-key zero-credit closure")
    need(max(v9_guards[9].before.st_mtime_ns,
             v9_guards[9].before.st_ctime_ns) <
             min(v9_rejection_guard.before.st_mtime_ns,
                 v9_rejection_guard.before.st_ctime_ns),
         "official v9 rejection is strictly later than published v9 outer")
    v9_namespace_guard = HeldDirectory(
        V9_OFFICIAL_REJECTION_NAMESPACE, {V9_OFFICIAL_REJECTION.name},
        0o555, 2, "official v9 rejection singleton namespace")
    v9_namespace_member = os.stat(
        V9_OFFICIAL_REJECTION.name, dir_fd=v9_namespace_guard.fd,
        follow_symlinks=False)
    need((v9_namespace_member.st_dev, v9_namespace_member.st_ino) ==
             v9_rejection_guard.identity and
         v9_namespace_guard.mount_id == v9_rejection_guard.mount_id,
         "official v9 rejection namespace member equals held current base fd")
    require_v9_positive_and_stage_surfaces_absent()
    v10_colon_prefix_witness = derive_v10_colon_prefix_witness(
            v10_by_path[V10_PUBLISHED_EXACT10_PINS[3][0]].raw,
            v9_by_path[V9_PUBLISHED_EXACT10_PINS[7][0]].raw)
    need(tuple(v10_colon_prefix_witness) ==
             V10_COLON_PREFIX_WITNESS_KEY_ORDER and
         len(v10_colon_prefix_witness) ==
             V10_COLON_PREFIX_WITNESS_KEY_COUNT and
         v10_colon_prefix_witness.get("object_sha256") ==
             V10_COLON_PREFIX_WITNESS_OBJECT_PIN and
         v10_colon_prefix_witness.get("successor_all_clauses_true") is True and
         v10_colon_prefix_witness.get("formal_global_closure_credit") == 0,
         "v10 exact40 per-clause colon-prefix witness independently derived")
    v10_regression_label_prefix_incident = copy.deepcopy(
        V10_REGRESSION_LABEL_PREFIX_INCIDENT)
    need(len(v10_regression_label_prefix_incident) == 44 and
         sha_bytes(canonical(v10_regression_label_prefix_incident)) ==
             V10_REGRESSION_LABEL_PREFIX_INCIDENT_CANONICAL_SHA256,
         "v10 canonical exact44 incident retained without v11 drift field")
    v11_dual_validator_divergence_incident = (
        v11_dual_validator_divergence_regression(
            v11_by_path[V11_PUBLISHED_EXACT10_PINS[3][0]].raw,
            v11_by_path[V11_PUBLISHED_EXACT10_PINS[7][0]].raw,
            v10_colon_prefix_witness))
    need(v11_dual_validator_divergence_incident ==
             V11_DUAL_VALIDATOR_DIVERGENCE_INCIDENT,
         "v11 dual-validator exact45/claim44 incident independently reproduced")

    v8_guards, v8_by_path, v8_outer, v8_chronology = (
        _hold_modern_published_exact10(
            V8_PUBLISHED_EXACT10_PINS, 8, "published v8 exact10"))
    v7_rejection_guard = v8_by_path[V7_OFFICIAL_REJECTION]
    v8_rejection = strict_json(
        v8_rejection_guard.raw, "official v8 later rejection")
    need(isinstance(v8_rejection, dict), "official v8 rejection object")
    verify_object(
        v8_rejection, "official v8 later rejection",
        V8_OFFICIAL_REJECTION_OBJECT_PIN)
    need(set(v8_rejection) == {
             "D02_formal_pending_task_count", "D02_gate_credit", "D02_started",
             "D02_task_credit", "D02_unlock", "closed_schema_file_sha256",
             "cold_launcher_file_sha256", "cold_manifest_file_sha256",
             "cold_outer_file_sha256", "cold_outer_object_sha256",
             "commit_operation", "consumer_file_sha256", "contract_file_sha256",
             "contract_object_sha256", "effective_checkpoint_object_sha256",
             "file_fsync_required", "formal_global_closure_credit",
             "idempotent_existing_recovery_re_fsyncs_rejection_file_namespace_and_runtime_parent",
             "namespace_at_rest_mode", "namespace_exact_path",
             "namespace_fsync_required_after_file_and_after_reseal",
             "namespace_lock_held_write_window_mode", "object_sha256",
             "official_writer_coordination_lock_held_for_entire_reject_command",
             "official_writer_coordination_lock_policy",
             "overwrite_delete_or_reuse_allowed",
             "partial_malformed_or_extra_namespace_entry_revokes_authority",
             "producer_file_sha256", "rejection_file_mode", "rejection_file_nlink",
             "rejection_reason", "runtime_parent_fsync_required_after_namespace_creation",
             "schema", "standalone_authority", "status", "target_exact_path",
             "target_is_protocol_and_checkpoint_deterministic",
             "v4_rejection_supersession_file_sha256",
             "v4_rejection_supersession_object_sha256",
             "v5_official_rejection_file_sha256",
             "v5_official_rejection_object_sha256",
             "v6_official_rejection_file_sha256",
             "v6_official_rejection_object_sha256",
             "v7_official_rejection_file_sha256",
             "v7_official_rejection_object_sha256",
             "v7_publication_lock_continuity_incident_object_sha256",
         } and
         v8_rejection_guard.raw == canonical(v8_rejection) + b"\n" and
         v8_rejection.get("schema") ==
             "cm2.round306c79g.true-global-no-producer-consumer.v8.later-rejection" and
         v8_rejection.get("status") ==
             "PERMANENT_FAIL_CLOSED_REJECTION__ZERO_CREDIT" and
         v8_rejection.get("rejection_reason") ==
             "ORPHANED_OR_INCOMPLETE_C79G_V8_SURFACE" and
         v8_rejection.get("effective_checkpoint_object_sha256") ==
             UPSTREAM_CHECKPOINT_OBJECT_PIN and
         v8_rejection.get("target_exact_path") ==
             str(V8_OFFICIAL_REJECTION.relative_to(ROOT)) and
         v8_rejection.get("namespace_exact_path") ==
             str(V8_OFFICIAL_REJECTION_NAMESPACE.relative_to(ROOT)) and
         v8_rejection.get("closed_schema_file_sha256") ==
             V8_PUBLISHED_EXACT10_PINS[1][1] and
         v8_rejection.get("contract_file_sha256") ==
             V8_PUBLISHED_EXACT10_PINS[2][1] and
         v8_rejection.get("contract_object_sha256") ==
             V8_PUBLISHED_EXACT10_PINS[2][2] and
         v8_rejection.get("producer_file_sha256") ==
             V8_PUBLISHED_EXACT10_PINS[3][1] and
         v8_rejection.get("consumer_file_sha256") ==
             V8_PUBLISHED_EXACT10_PINS[4][1] and
         v8_rejection.get("cold_launcher_file_sha256") ==
             V8_PUBLISHED_EXACT10_PINS[7][1] and
         v8_rejection.get("cold_manifest_file_sha256") ==
             V8_PUBLISHED_EXACT10_PINS[8][1] and
         v8_rejection.get("cold_outer_file_sha256") ==
             V8_PUBLISHED_EXACT10_PINS[9][1] and
         v8_rejection.get("cold_outer_object_sha256") ==
             V8_PUBLISHED_EXACT10_PINS[9][2] and
         v8_rejection.get("v4_rejection_supersession_file_sha256") ==
             V4_REJECTION_SUPERSESSION_FILE_PIN and
         v8_rejection.get("v4_rejection_supersession_object_sha256") ==
             V4_REJECTION_SUPERSESSION_OBJECT_PIN and
         v8_rejection.get("v5_official_rejection_file_sha256") ==
             V5_OFFICIAL_REJECTION_FILE_PIN and
         v8_rejection.get("v5_official_rejection_object_sha256") ==
             V5_OFFICIAL_REJECTION_OBJECT_PIN and
         v8_rejection.get("v6_official_rejection_file_sha256") ==
             V6_OFFICIAL_REJECTION_FILE_PIN and
         v8_rejection.get("v6_official_rejection_object_sha256") ==
             V6_OFFICIAL_REJECTION_OBJECT_PIN and
         v8_rejection.get("v7_official_rejection_file_sha256") ==
             V7_OFFICIAL_REJECTION_FILE_PIN and
         v8_rejection.get("v7_official_rejection_object_sha256") ==
             V7_OFFICIAL_REJECTION_OBJECT_PIN and
         v8_rejection.get("v7_publication_lock_continuity_incident_object_sha256") ==
             V7_LOCK_CONTINUITY_INCIDENT_OBJECT_PIN and
         v8_rejection.get("namespace_at_rest_mode") == "0555" and
         v8_rejection.get("namespace_lock_held_write_window_mode") == "0755" and
         v8_rejection.get("rejection_file_mode") == "0444" and
         v8_rejection.get("rejection_file_nlink") == 1 and
         v8_rejection.get("formal_global_closure_credit") == 0 and
         v8_rejection.get("D02_unlock") is False and
         v8_rejection.get("D02_started") is False and
         v8_rejection.get("D02_formal_pending_task_count") == EXPECTED_PENDING_D02 and
         v8_rejection.get("standalone_authority") is False and
         v8_rejection.get("overwrite_delete_or_reuse_allowed") is False,
         "official v8 rejection exact canonical singleton zero-credit closure")
    need(max(v8_guards[9].before.st_mtime_ns,
             v8_guards[9].before.st_ctime_ns) <
             min(v8_rejection_guard.before.st_mtime_ns,
                 v8_rejection_guard.before.st_ctime_ns),
         "official v8 rejection is strictly later than published v8 outer")
    v8_namespace_guard = HeldDirectory(
        V8_OFFICIAL_REJECTION_NAMESPACE, {V8_OFFICIAL_REJECTION.name},
        0o555, 2, "official v8 rejection singleton namespace")
    v8_namespace_member = os.stat(
        V8_OFFICIAL_REJECTION.name, dir_fd=v8_namespace_guard.fd,
        follow_symlinks=False)
    need((v8_namespace_member.st_dev, v8_namespace_member.st_ino) ==
             v8_rejection_guard.identity and
         v8_namespace_guard.mount_id == v8_rejection_guard.mount_id,
         "official v8 rejection namespace member equals held current base fd")
    require_v8_positive_and_stage_surfaces_absent()

    v7_guards, v7_by_path, v7_outer, v7_chronology = (
        _hold_modern_published_exact10(
            V7_PUBLISHED_EXACT10_PINS, 7, "published v7 exact10"))
    v6_rejection_guard = v7_by_path[V6_OFFICIAL_REJECTION]
    v7_rejection = strict_json(
        v7_rejection_guard.raw, "official v7 later rejection")
    need(isinstance(v7_rejection, dict), "official v7 rejection object")
    verify_object(
        v7_rejection, "official v7 later rejection",
        V7_OFFICIAL_REJECTION_OBJECT_PIN)
    need(set(v7_rejection) == {
             "D02_formal_pending_task_count", "D02_gate_credit", "D02_started",
             "D02_task_credit", "D02_unlock", "closed_schema_file_sha256",
             "cold_launcher_file_sha256", "cold_manifest_file_sha256",
             "cold_outer_file_sha256", "cold_outer_object_sha256",
             "commit_operation", "consumer_file_sha256", "contract_file_sha256",
             "contract_object_sha256", "effective_checkpoint_object_sha256",
             "file_fsync_required", "formal_global_closure_credit",
             "idempotent_existing_recovery_re_fsyncs_rejection_file_namespace_and_runtime_parent",
             "namespace_at_rest_mode", "namespace_exact_path",
             "namespace_fsync_required_after_file_and_after_reseal",
             "namespace_lock_held_write_window_mode", "object_sha256",
             "official_writer_coordination_lock_held_for_entire_reject_command",
             "official_writer_coordination_lock_policy",
             "overwrite_delete_or_reuse_allowed",
             "partial_malformed_or_extra_namespace_entry_revokes_authority",
             "producer_file_sha256", "rejection_file_mode", "rejection_file_nlink",
             "rejection_reason", "runtime_parent_fsync_required_after_namespace_creation",
             "schema", "standalone_authority", "status", "target_exact_path",
             "target_is_protocol_and_checkpoint_deterministic",
             "v4_rejection_supersession_file_sha256",
             "v4_rejection_supersession_object_sha256",
             "v5_official_rejection_file_sha256",
             "v5_official_rejection_object_sha256",
             "v6_official_rejection_file_sha256",
             "v6_official_rejection_object_sha256"} and
         v7_rejection_guard.raw == canonical(v7_rejection) + b"\n" and
         v7_rejection.get("schema") ==
             "cm2.round306c79g.true-global-no-producer-consumer.v7.later-rejection" and
         v7_rejection.get("status") ==
             "PERMANENT_FAIL_CLOSED_REJECTION__ZERO_CREDIT" and
         v7_rejection.get("rejection_reason") ==
             "ORPHANED_OR_INCOMPLETE_C79G_V7_SURFACE" and
         v7_rejection.get("effective_checkpoint_object_sha256") ==
             UPSTREAM_CHECKPOINT_OBJECT_PIN and
         v7_rejection.get("target_exact_path") ==
             str(V7_OFFICIAL_REJECTION.relative_to(ROOT)) and
         v7_rejection.get("namespace_exact_path") ==
             str(V7_OFFICIAL_REJECTION_NAMESPACE.relative_to(ROOT)) and
         v7_rejection.get("closed_schema_file_sha256") ==
             V7_PUBLISHED_EXACT10_PINS[1][1] and
         v7_rejection.get("contract_file_sha256") ==
             V7_PUBLISHED_EXACT10_PINS[2][1] and
         v7_rejection.get("contract_object_sha256") ==
             V7_PUBLISHED_EXACT10_PINS[2][2] and
         v7_rejection.get("producer_file_sha256") ==
             V7_PUBLISHED_EXACT10_PINS[3][1] and
         v7_rejection.get("consumer_file_sha256") ==
             V7_PUBLISHED_EXACT10_PINS[4][1] and
         v7_rejection.get("cold_launcher_file_sha256") ==
             V7_PUBLISHED_EXACT10_PINS[7][1] and
         v7_rejection.get("cold_manifest_file_sha256") ==
             V7_PUBLISHED_EXACT10_PINS[8][1] and
         v7_rejection.get("cold_outer_file_sha256") ==
             V7_PUBLISHED_EXACT10_PINS[9][1] and
         v7_rejection.get("cold_outer_object_sha256") ==
             V7_PUBLISHED_EXACT10_PINS[9][2] and
         v7_rejection.get("v4_rejection_supersession_file_sha256") ==
             V4_REJECTION_SUPERSESSION_FILE_PIN and
         v7_rejection.get("v4_rejection_supersession_object_sha256") ==
             V4_REJECTION_SUPERSESSION_OBJECT_PIN and
         v7_rejection.get("v5_official_rejection_file_sha256") ==
             V5_OFFICIAL_REJECTION_FILE_PIN and
         v7_rejection.get("v5_official_rejection_object_sha256") ==
             V5_OFFICIAL_REJECTION_OBJECT_PIN and
         v7_rejection.get("v6_official_rejection_file_sha256") ==
             V6_OFFICIAL_REJECTION_FILE_PIN and
         v7_rejection.get("v6_official_rejection_object_sha256") ==
             V6_OFFICIAL_REJECTION_OBJECT_PIN and
         v7_rejection.get("commit_operation") ==
             "O_CREAT_O_EXCL_FIXED_TARGET_NO_FALLBACK" and
         v7_rejection.get("namespace_at_rest_mode") == "0555" and
         v7_rejection.get("namespace_lock_held_write_window_mode") == "0755" and
         v7_rejection.get("rejection_file_mode") == "0444" and
         v7_rejection.get("rejection_file_nlink") == 1 and
         v7_rejection.get("file_fsync_required") is True and
         v7_rejection.get(
             "namespace_fsync_required_after_file_and_after_reseal") is True and
         v7_rejection.get(
             "runtime_parent_fsync_required_after_namespace_creation") is True and
         v7_rejection.get(
             "official_writer_coordination_lock_held_for_entire_reject_command") is True and
         v7_rejection.get(
             "partial_malformed_or_extra_namespace_entry_revokes_authority") is True and
         v7_rejection.get(
             "idempotent_existing_recovery_re_fsyncs_rejection_file_namespace_and_runtime_parent")
             is True and
         v7_rejection.get("target_is_protocol_and_checkpoint_deterministic") is True and
         v7_rejection.get("D02_formal_pending_task_count") == EXPECTED_PENDING_D02 and
         v7_rejection.get("D02_gate_credit") == 0 and
         v7_rejection.get("D02_task_credit") == 0 and
         v7_rejection.get("formal_global_closure_credit") == 0 and
         v7_rejection.get("D02_unlock") is False and
         v7_rejection.get("D02_started") is False and
         v7_rejection.get("standalone_authority") is False and
         v7_rejection.get("overwrite_delete_or_reuse_allowed") is False and
         isinstance(v7_rejection.get(
             "official_writer_coordination_lock_policy"), dict),
         "official v7 rejection exact canonical 43-key zero-credit closure")
    need(max(v7_guards[9].before.st_mtime_ns,
             v7_guards[9].before.st_ctime_ns) <
             min(v7_rejection_guard.before.st_mtime_ns,
                 v7_rejection_guard.before.st_ctime_ns),
         "official v7 rejection is strictly later than published v7 outer")
    v7_namespace_guard = HeldDirectory(
        V7_OFFICIAL_REJECTION_NAMESPACE, {V7_OFFICIAL_REJECTION.name},
        0o555, 2, "official v7 rejection singleton namespace")
    v7_namespace_member = os.stat(
        V7_OFFICIAL_REJECTION.name, dir_fd=v7_namespace_guard.fd,
        follow_symlinks=False)
    need((v7_namespace_member.st_dev, v7_namespace_member.st_ino) ==
             v7_rejection_guard.identity and
         v7_namespace_guard.mount_id == v7_rejection_guard.mount_id,
         "official v7 rejection namespace member equals held current base fd")
    require_v7_positive_and_stage_surfaces_absent()

    v6_guards, v6_by_path, v6_outer, v6_chronology = (
        _hold_modern_published_exact10(
            V6_PUBLISHED_EXACT10_PINS, 6, "published v6 exact10"))
    v6_launcher_expanded_structural_evidence = (
        v6_held_self_identity_defect_regression(
            v6_by_path[V6_PUBLISHED_EXACT10_PINS[3][0]].raw))
    need(v6_launcher_expanded_structural_evidence ==
             V6_LAUNCHER_EXPANDED_STRUCTURAL_EVIDENCE,
         "v6 structural16 evidence independently replayed and remains separate")
    v9_shape_drift_incident = v9_prechild_shape_drift_regression(
        v9_by_path[V9_PUBLISHED_EXACT10_PINS[2][0]].raw,
        v9_by_path[V9_PUBLISHED_EXACT10_PINS[7][0]].raw,
        v6_launcher_expanded_structural_evidence)
    need(v9_shape_drift_incident == V9_V6_DEFECT_SHAPE_DRIFT_INCIDENT,
         "v9 canonical9 versus structural16 incident independently reproduced")
    v8_rollout_control_flow_incident = copy.deepcopy(
        V8_ROLLOUT_CONTROL_FLOW_INCIDENT)
    v5_rejection_guard = v6_by_path[V5_OFFICIAL_REJECTION]
    v6_rejection = strict_json(
        v6_rejection_guard.raw, "official v6 later rejection")
    need(isinstance(v6_rejection, dict), "official v6 rejection object")
    verify_object(
        v6_rejection, "official v6 later rejection",
        V6_OFFICIAL_REJECTION_OBJECT_PIN)
    need(set(v6_rejection) == {
             "D02_formal_pending_task_count", "D02_gate_credit", "D02_started",
             "D02_task_credit", "D02_unlock", "closed_schema_file_sha256",
             "cold_launcher_file_sha256", "cold_manifest_file_sha256",
             "cold_outer_file_sha256", "cold_outer_object_sha256",
             "commit_operation", "consumer_file_sha256", "contract_file_sha256",
             "contract_object_sha256", "effective_checkpoint_object_sha256",
             "file_fsync_required", "formal_global_closure_credit",
             "idempotent_existing_recovery_re_fsyncs_rejection_file_namespace_and_runtime_parent",
             "namespace_at_rest_mode", "namespace_exact_path",
             "namespace_fsync_required_after_file_and_after_reseal",
             "namespace_lock_held_write_window_mode", "object_sha256",
             "official_writer_coordination_lock_held_for_entire_reject_command",
             "official_writer_coordination_lock_policy",
             "overwrite_delete_or_reuse_allowed",
             "partial_malformed_or_extra_namespace_entry_revokes_authority",
             "producer_file_sha256", "rejection_file_mode", "rejection_file_nlink",
             "rejection_reason", "runtime_parent_fsync_required_after_namespace_creation",
             "schema", "standalone_authority", "status", "target_exact_path",
             "target_is_protocol_and_checkpoint_deterministic",
             "v4_rejection_supersession_file_sha256",
             "v4_rejection_supersession_object_sha256",
             "v5_official_rejection_file_sha256",
             "v5_official_rejection_object_sha256"} and
         v6_rejection_guard.raw == canonical(v6_rejection) + b"\n" and
         v6_rejection.get("schema") ==
             "cm2.round306c79g.true-global-no-producer-consumer.v6.later-rejection" and
         v6_rejection.get("status") ==
             "PERMANENT_FAIL_CLOSED_REJECTION__ZERO_CREDIT" and
         v6_rejection.get("rejection_reason") ==
             "ORPHANED_OR_INCOMPLETE_C79G_V6_SURFACE" and
         v6_rejection.get("effective_checkpoint_object_sha256") ==
             UPSTREAM_CHECKPOINT_OBJECT_PIN and
         v6_rejection.get("target_exact_path") ==
             str(V6_OFFICIAL_REJECTION.relative_to(ROOT)) and
         v6_rejection.get("namespace_exact_path") ==
             str(V6_OFFICIAL_REJECTION_NAMESPACE.relative_to(ROOT)) and
         v6_rejection.get("closed_schema_file_sha256") ==
             V6_PUBLISHED_EXACT10_PINS[1][1] and
         v6_rejection.get("contract_file_sha256") ==
             V6_PUBLISHED_EXACT10_PINS[2][1] and
         v6_rejection.get("contract_object_sha256") ==
             V6_PUBLISHED_EXACT10_PINS[2][2] and
         v6_rejection.get("producer_file_sha256") ==
             V6_PUBLISHED_EXACT10_PINS[3][1] and
         v6_rejection.get("consumer_file_sha256") ==
             V6_PUBLISHED_EXACT10_PINS[4][1] and
         v6_rejection.get("cold_launcher_file_sha256") ==
             V6_PUBLISHED_EXACT10_PINS[7][1] and
         v6_rejection.get("cold_manifest_file_sha256") ==
             V6_PUBLISHED_EXACT10_PINS[8][1] and
         v6_rejection.get("cold_outer_file_sha256") ==
             V6_PUBLISHED_EXACT10_PINS[9][1] and
         v6_rejection.get("cold_outer_object_sha256") ==
             V6_PUBLISHED_EXACT10_PINS[9][2] and
         v6_rejection.get("v4_rejection_supersession_file_sha256") ==
             V4_REJECTION_SUPERSESSION_FILE_PIN and
         v6_rejection.get("v4_rejection_supersession_object_sha256") ==
             V4_REJECTION_SUPERSESSION_OBJECT_PIN and
         v6_rejection.get("v5_official_rejection_file_sha256") ==
             V5_OFFICIAL_REJECTION_FILE_PIN and
         v6_rejection.get("v5_official_rejection_object_sha256") ==
             V5_OFFICIAL_REJECTION_OBJECT_PIN and
         v6_rejection.get("commit_operation") ==
             "O_CREAT_O_EXCL_FIXED_TARGET_NO_FALLBACK" and
         v6_rejection.get("namespace_at_rest_mode") == "0555" and
         v6_rejection.get("namespace_lock_held_write_window_mode") == "0755" and
         v6_rejection.get("rejection_file_mode") == "0444" and
         v6_rejection.get("rejection_file_nlink") == 1 and
         v6_rejection.get("file_fsync_required") is True and
         v6_rejection.get(
             "namespace_fsync_required_after_file_and_after_reseal") is True and
         v6_rejection.get(
             "runtime_parent_fsync_required_after_namespace_creation") is True and
         v6_rejection.get(
             "official_writer_coordination_lock_held_for_entire_reject_command") is True and
         v6_rejection.get(
             "partial_malformed_or_extra_namespace_entry_revokes_authority") is True and
         v6_rejection.get(
             "idempotent_existing_recovery_re_fsyncs_rejection_file_namespace_and_runtime_parent") is True and
         v6_rejection.get("target_is_protocol_and_checkpoint_deterministic") is True and
         v6_rejection.get("D02_formal_pending_task_count") == EXPECTED_PENDING_D02 and
         v6_rejection.get("D02_gate_credit") == 0 and
         v6_rejection.get("D02_task_credit") == 0 and
         v6_rejection.get("formal_global_closure_credit") == 0 and
         v6_rejection.get("D02_unlock") is False and
         v6_rejection.get("D02_started") is False and
         v6_rejection.get("standalone_authority") is False and
         v6_rejection.get("overwrite_delete_or_reuse_allowed") is False and
         isinstance(v6_rejection.get(
             "official_writer_coordination_lock_policy"), dict),
         "official v6 rejection exact canonical 41-key zero-credit closure")
    need(max(v6_guards[9].before.st_mtime_ns,
             v6_guards[9].before.st_ctime_ns) <
             min(v6_rejection_guard.before.st_mtime_ns,
                 v6_rejection_guard.before.st_ctime_ns),
         "official v6 rejection is strictly later than published v6 outer")
    v6_namespace_guard = HeldDirectory(
        V6_OFFICIAL_REJECTION_NAMESPACE, {V6_OFFICIAL_REJECTION.name},
        0o555, 2, "official v6 rejection singleton namespace")
    v6_namespace_member = os.stat(
        V6_OFFICIAL_REJECTION.name, dir_fd=v6_namespace_guard.fd,
        follow_symlinks=False)
    need((v6_namespace_member.st_dev, v6_namespace_member.st_ino) ==
             v6_rejection_guard.identity and
         v6_namespace_guard.mount_id == v6_rejection_guard.mount_id,
         "official v6 rejection namespace member equals held current base fd")
    require_v6_positive_and_stage_surfaces_absent()

    v5_guards = [
        HeldPinnedInput(path, "published v5 exact10:" + path.name, 0o444, file_pin)
        for path, file_pin, _ in V5_PUBLISHED_EXACT10_PINS
    ]
    v5_by_path = {
        path: v5_guards[index]
        for index, (path, _, _) in enumerate(V5_PUBLISHED_EXACT10_PINS)
    }
    need(len(v5_guards) == len(v5_by_path) == 10 and
         len({guard.identity for guard in v5_guards}) == 10 and
         len({guard.mount_id for guard in v5_guards}) == 1,
         "published v5 exact10 unique held identities on one statx mount")
    for path, _, object_pin in V5_PUBLISHED_EXACT10_PINS:
        if object_pin is not None:
            value = strict_json(
                v5_by_path[path].raw, "published v5 object:" + path.name)
            need(isinstance(value, dict), "published v5 object mapping:" + path.name)
            verify_object(value, "published v5 object:" + path.name, object_pin)

    v5_manifest_guard = v5_guards[8]
    v5_outer_guard = v5_guards[9]
    v5_manifest_entries = parse_manifest_ordered(
        v5_manifest_guard.raw, "published v5 exact8 manifest")
    expected_v5_manifest = [
        {
            "file_sha256": file_pin,
            "entry_name": str(path.relative_to(ROOT)),
        }
        for path, file_pin, _ in V5_PUBLISHED_EXACT10_PINS[:8]
    ]
    need(v5_manifest_entries == expected_v5_manifest,
         "published v5 manifest exactly reconstructs ordered exact8")
    v5_outer = strict_json(v5_outer_guard.raw, "published v5 outer-last")
    need(isinstance(v5_outer, dict), "published v5 outer-last object")
    verify_object(
        v5_outer, "published v5 outer-last",
        V5_PUBLISHED_EXACT10_PINS[9][2])
    v5_expected_outer_entries = [
        {"path": item["entry_name"], "file_sha256": item["file_sha256"]}
        for item in expected_v5_manifest
    ]
    v5_chronology = cold_publication_chronology(
        [guard.before for guard in v5_guards[:8]],
        v5_manifest_guard.before, v5_outer_guard.before)
    need(set(v5_outer) == {
             "schema", "status", "effective_checkpoint_object_sha256",
             "exact8_ordered_entries", "cold_launch_manifest", "cold_launcher",
             "all_exact8_regular_0444_nlink1_and_held_for_runtime",
             "outer_published_after_exact8_manifest",
             "runtime_entry_must_be_cold_launcher",
             "sole_external_static_file_anchor_is_launcher_sha256",
             "declared_external_tcb", "formal_global_closure_credit",
             "D02_unlock", "runtime_executed_during_static_freeze",
             "object_sha256"} and
         v5_outer_guard.raw == canonical(v5_outer) + b"\n" and
         v5_outer.get("schema") ==
             "cm2.round306c79g.true-global-no-producer-consumer."
             "cold-launch-outer-receipt.v5" and
         v5_outer.get("status") ==
             "FROZEN_COLD_LAUNCH_OUTER_LAST__EXACT8_MANIFEST_CLOSED__RUNTIME_DEFERRED" and
         v5_outer.get("effective_checkpoint_object_sha256") ==
             UPSTREAM_CHECKPOINT_OBJECT_PIN and
         v5_outer.get("exact8_ordered_entries") == v5_expected_outer_entries and
         v5_outer.get("cold_launch_manifest", {}).get("path") ==
             str(V5_PUBLISHED_EXACT10_PINS[8][0].relative_to(ROOT)) and
         v5_outer.get("cold_launch_manifest", {}).get("file_sha256") ==
             V5_PUBLISHED_EXACT10_PINS[8][1] and
         v5_outer.get("cold_launch_manifest", {}).get("ordered_entry_count") == 8 and
         v5_outer.get("cold_launcher", {}).get("path") ==
             str(V5_PUBLISHED_EXACT10_PINS[7][0].relative_to(ROOT)) and
         v5_outer.get("cold_launcher", {}).get("file_sha256") ==
             V5_PUBLISHED_EXACT10_PINS[7][1] and
         v5_outer.get("formal_global_closure_credit") == 0 and
         v5_outer.get("D02_unlock") is False and
         v5_outer.get("runtime_executed_during_static_freeze") is False and
         all(v5_chronology.values()),
         "published v5 exact10 outer-last and chronology closure")

    v5_rejection = strict_json(
        v5_rejection_guard.raw, "official v5 later rejection")
    need(isinstance(v5_rejection, dict), "official v5 rejection object")
    verify_object(
        v5_rejection, "official v5 later rejection",
        V5_OFFICIAL_REJECTION_OBJECT_PIN)
    need(len(V5_OFFICIAL_REJECTION_EXACT39_KEYS) == 39 and
         sha_bytes(canonical(sorted(V5_OFFICIAL_REJECTION_EXACT39_KEYS))) ==
             V5_OFFICIAL_REJECTION_EXACT39_KEYSET_SHA256 and
         set(v5_rejection) == V5_OFFICIAL_REJECTION_EXACT39_KEYS and
         sha_bytes(canonical(sorted(v5_rejection))) ==
             V5_OFFICIAL_REJECTION_EXACT39_KEYSET_SHA256 and
         v5_rejection_guard.raw == canonical(v5_rejection) + b"\n" and
         v5_rejection.get("schema") ==
             "cm2.round306c79g.true-global-no-producer-consumer.v5.later-rejection" and
         v5_rejection.get("status") ==
             "PERMANENT_FAIL_CLOSED_REJECTION__ZERO_CREDIT" and
         v5_rejection.get("rejection_reason") ==
             "ORPHANED_OR_INCOMPLETE_C79G_V5_SURFACE" and
         v5_rejection.get("effective_checkpoint_object_sha256") ==
             UPSTREAM_CHECKPOINT_OBJECT_PIN and
         v5_rejection.get("target_exact_path") ==
             str(V5_OFFICIAL_REJECTION.relative_to(ROOT)) and
         v5_rejection.get("namespace_exact_path") ==
             str(V5_OFFICIAL_REJECTION_NAMESPACE.relative_to(ROOT)) and
         v5_rejection.get("closed_schema_file_sha256") ==
             V5_PUBLISHED_EXACT10_PINS[1][1] and
         v5_rejection.get("contract_file_sha256") ==
             V5_PUBLISHED_EXACT10_PINS[2][1] and
         v5_rejection.get("contract_object_sha256") ==
             V5_PUBLISHED_EXACT10_PINS[2][2] and
         v5_rejection.get("producer_file_sha256") ==
             V5_PUBLISHED_EXACT10_PINS[3][1] and
         v5_rejection.get("consumer_file_sha256") ==
             V5_PUBLISHED_EXACT10_PINS[4][1] and
         v5_rejection.get("cold_launcher_file_sha256") ==
             V5_PUBLISHED_EXACT10_PINS[7][1] and
         v5_rejection.get("cold_manifest_file_sha256") ==
             V5_PUBLISHED_EXACT10_PINS[8][1] and
         v5_rejection.get("cold_outer_file_sha256") ==
             V5_PUBLISHED_EXACT10_PINS[9][1] and
         v5_rejection.get("cold_outer_object_sha256") ==
             V5_PUBLISHED_EXACT10_PINS[9][2] and
         v5_rejection.get("v4_rejection_supersession_file_sha256") ==
             V4_REJECTION_SUPERSESSION_FILE_PIN and
         v5_rejection.get("v4_rejection_supersession_object_sha256") ==
             V4_REJECTION_SUPERSESSION_OBJECT_PIN and
         v5_rejection.get("commit_operation") ==
             "O_CREAT_O_EXCL_FIXED_TARGET_NO_FALLBACK" and
         v5_rejection.get("namespace_at_rest_mode") == "0555" and
         v5_rejection.get("namespace_lock_held_write_window_mode") == "0755" and
         v5_rejection.get("rejection_file_mode") == "0444" and
         v5_rejection.get("rejection_file_nlink") == 1 and
         v5_rejection.get("file_fsync_required") is True and
         v5_rejection.get("namespace_fsync_required_after_file_and_after_reseal") is True and
         v5_rejection.get("runtime_parent_fsync_required_after_namespace_creation") is True and
         v5_rejection.get("official_writer_coordination_lock_held_for_entire_reject_command") is True and
         v5_rejection.get("partial_malformed_or_extra_namespace_entry_revokes_authority") is True and
         v5_rejection.get("idempotent_existing_recovery_re_fsyncs_rejection_file_namespace_and_runtime_parent") is True and
         v5_rejection.get("target_is_protocol_and_checkpoint_deterministic") is True and
         v5_rejection.get("D02_formal_pending_task_count") == EXPECTED_PENDING_D02 and
         v5_rejection.get("D02_gate_credit") == 0 and
         v5_rejection.get("D02_task_credit") == 0 and
         v5_rejection.get("formal_global_closure_credit") == 0 and
         v5_rejection.get("D02_unlock") is False and
         v5_rejection.get("D02_started") is False and
         v5_rejection.get("standalone_authority") is False and
         v5_rejection.get("overwrite_delete_or_reuse_allowed") is False and
         isinstance(v5_rejection.get("official_writer_coordination_lock_policy"), dict),
         "official v5 rejection exact canonical 39-key zero-credit closure")
    need(max(v5_outer_guard.before.st_mtime_ns,
             v5_outer_guard.before.st_ctime_ns) <
             min(v5_rejection_guard.before.st_mtime_ns,
                 v5_rejection_guard.before.st_ctime_ns),
         "official v5 rejection is strictly later than published v5 outer")

    v5_namespace_guard = HeldDirectory(
        V5_OFFICIAL_REJECTION_NAMESPACE, {V5_OFFICIAL_REJECTION.name},
        0o555, 2, "official v5 rejection singleton namespace")
    namespace_member = os.stat(
        V5_OFFICIAL_REJECTION.name, dir_fd=v5_namespace_guard.fd,
        follow_symlinks=False)
    need((namespace_member.st_dev, namespace_member.st_ino) ==
             v5_rejection_guard.identity and
         v5_namespace_guard.mount_id == v5_rejection_guard.mount_id,
         "official v5 rejection namespace member equals held current base fd")

    v3_guards = [
        HeldPinnedInput(path, "published v3 exact10:" + path.name, 0o444, file_pin)
        for path, file_pin, _ in V3_PUBLISHED_EXACT10_PINS
    ]
    v3_by_path = {
        path: v3_guards[index]
        for index, (path, _, _) in enumerate(V3_PUBLISHED_EXACT10_PINS)
    }
    need(len(v3_guards) == len(v3_by_path) == 10 and
         len({guard.identity for guard in v3_guards}) == 10 and
         len({guard.mount_id for guard in v3_guards}) == 1,
         "published v3 exact10 unique held identities on one statx mount")
    for path, _, object_pin in V3_PUBLISHED_EXACT10_PINS:
        if object_pin is not None:
            value = strict_json(v3_by_path[path].raw, "published v3 object:" + path.name)
            need(isinstance(value, dict), "published v3 object mapping:" + path.name)
            verify_object(value, "published v3 object:" + path.name, object_pin)
    expected_v3_manifest = [
        {"file_sha256": file_pin, "entry_name": str(path.relative_to(ROOT))}
        for path, file_pin, _ in V3_PUBLISHED_EXACT10_PINS[:8]
    ]
    need(parse_manifest_ordered(v3_guards[8].raw, "published v3 manifest") ==
             expected_v3_manifest,
         "published v3 manifest exactly reconstructs ordered exact8")
    v3_outer = strict_json(v3_guards[9].raw, "published v3 outer-last")
    need(isinstance(v3_outer, dict), "published v3 outer-last object")
    verify_object(v3_outer, "published v3 outer-last", V3_PUBLISHED_EXACT10_PINS[9][2])
    v3_chronology = cold_publication_chronology(
        [guard.before for guard in v3_guards[:8]],
        v3_guards[8].before, v3_guards[9].before)
    need(v3_guards[9].raw == canonical(v3_outer) + b"\n" and
         v3_outer.get("schema") ==
             "cm2.round306c79g.true-global-no-producer-consumer."
             "cold-launch-outer-receipt.v3" and
         v3_outer.get("status") ==
             "FROZEN_COLD_LAUNCH_OUTER_LAST__EXACT8_MANIFEST_CLOSED__RUNTIME_DEFERRED" and
         v3_outer.get("exact8_ordered_entries") == [
             {"path": item["entry_name"], "file_sha256": item["file_sha256"]}
             for item in expected_v3_manifest] and
         v3_outer.get("cold_launch_manifest", {}).get("file_sha256") ==
             V3_PUBLISHED_EXACT10_PINS[8][1] and
         v3_outer.get("cold_launcher", {}).get("file_sha256") ==
             V3_PUBLISHED_EXACT10_PINS[7][1] and
         v3_outer.get("formal_global_closure_credit") == 0 and
         v3_outer.get("D02_unlock") is False and
         v3_outer.get("runtime_executed_during_static_freeze") is False and
         all(v3_chronology.values()),
         "published v3 exact10 manifest/outer/chronology closure")

    v3_rejection_guard = HeldPinnedInput(
        V3_OFFICIAL_REJECTION, "official v3 later rejection", 0o444,
        V3_REJECTION_FILE_PIN)
    v3_rejection = strict_json(
        v3_rejection_guard.raw, "official v3 later rejection")
    need(isinstance(v3_rejection, dict), "official v3 rejection object")
    verify_object(
        v3_rejection, "official v3 later rejection", V3_REJECTION_OBJECT_PIN)
    need(v3_rejection_guard.raw == canonical(v3_rejection) + b"\n" and
         v3_rejection.get("schema") ==
             "cm2.round306c79g.true-global-no-producer-consumer.v3.later-rejection" and
         v3_rejection.get("status") ==
             "PERMANENT_FAIL_CLOSED_REJECTION__ZERO_CREDIT" and
         v3_rejection.get("rejection_reason") ==
             "ORPHANED_OR_INCOMPLETE_C79G_V3_SURFACE" and
         v3_rejection.get("formal_global_closure_credit") == 0 and
         v3_rejection.get("D02_unlock") is False and
         v3_rejection.get("D02_started") is False and
         max(v3_guards[9].before.st_mtime_ns, v3_guards[9].before.st_ctime_ns) <
             min(v3_rejection_guard.before.st_mtime_ns,
                 v3_rejection_guard.before.st_ctime_ns),
         "official v3 rejection canonical zero-credit chronology")

    v4_guards = [
        HeldPinnedInput(path, "frozen v4 draft:" + path.name, 0o444, file_pin)
        for path, file_pin, _ in V4_DRAFT7_PINS
    ]
    v4_by_path = {
        path: v4_guards[index]
        for index, (path, _, _) in enumerate(V4_DRAFT7_PINS)
    }
    need(len(v4_guards) == len(v4_by_path) == 7 and
         len({guard.identity for guard in v4_guards}) == 7 and
         len({guard.mount_id for guard in v4_guards}) == 1,
         "frozen v4 draft seven distinct non-rejection identities on one mount")
    for path, _, object_pin in V4_DRAFT7_PINS:
        if object_pin is not None:
            value = strict_json(v4_by_path[path].raw, "frozen v4 object:" + path.name)
            need(isinstance(value, dict), "frozen v4 object mapping:" + path.name)
            verify_object(value, "frozen v4 object:" + path.name, object_pin)

    prior_history_guards = [
        *v12_guards, *v11_guards, *v10_guards, *v9_guards, *v8_guards,
        *v7_guards, *v6_guards, *v5_guards, *v3_guards, *v4_guards,
        v3_rejection_guard,
    ]
    predecessor_guards = [
        *prior_history_guards, *v13_incident_guards, v12_rejection_guard,
        *v14_guards, v14_rejection_guard]
    current_exact8_guards = [self_guard, *by_path.values()]
    prepublication_guards = [*predecessor_guards, *current_exact8_guards]
    all_file_guards = [
        *current_cold_ten_guards,
        *v14_guards,
        *v12_guards, *v11_guards, *v10_guards, *v9_guards, *v8_guards,
        *v7_guards, *v6_guards, *v5_guards, *v3_guards, *v4_guards,
        v3_rejection_guard,
        *v13_incident_guards[:3], *v13_incident_guards[3:],
        v12_rejection_guard, v14_rejection_guard,
    ]
    group_vector = [
        len(current_cold_ten_guards), len(v14_guards),
        len(v12_guards), len(v11_guards), len(v10_guards),
        len(v9_guards), len(v8_guards), len(v7_guards), len(v6_guards),
        len(v5_guards), len(v3_guards), len(v4_guards), 1,
        len(v13_incident_guards[:3]), len(v13_incident_guards[3:]), 1, 1,
    ]
    need(len(prior_history_guards) == 98 and
         len({guard.identity for guard in prior_history_guards}) == 98 and
         len(predecessor_guards) ==
             V16R2_PREDECESSOR_UNIQUE_LIVE_IDENTITY_COUNT and
         len({guard.identity for guard in predecessor_guards}) ==
             V16R2_PREDECESSOR_UNIQUE_LIVE_IDENTITY_COUNT and
         len(current_exact8_guards) == 8 and
         len(prepublication_guards) ==
             V16R2_PREPUBLICATION_UNIQUE_LIVE_IDENTITY_COUNT and
         len({guard.identity for guard in prepublication_guards}) ==
             V16R2_PREPUBLICATION_UNIQUE_LIVE_IDENTITY_COUNT and
         len(all_file_guards) == V16R2_TERMINAL_UNIQUE_LIVE_IDENTITY_COUNT and
         len({guard.identity for guard in all_file_guards}) ==
             V16R2_TERMINAL_UNIQUE_LIVE_IDENTITY_COUNT and
         group_vector == list(V16R2_TERMINAL_GROUP_VECTOR) and
         len({guard.mount_id for guard in all_file_guards}) == 1 and
         v12_namespace_guard.mount_id == v11_namespace_guard.mount_id ==
             v10_namespace_guard.mount_id ==
             v9_namespace_guard.mount_id ==
             v8_namespace_guard.mount_id ==
             v7_namespace_guard.mount_id ==
             v6_namespace_guard.mount_id == v5_namespace_guard.mount_id ==
             all_file_guards[0].mount_id,
         "append-only prior98/predecessor116/prepublication124/terminal126 "
         "identity census and exact terminal group vector on one mount")
    require_v5_positive_and_stage_surfaces_absent()

    v16r2_consumer_path = COLD_EXACT8[4]
    strict_bool_census = strict_bool_predecessor_and_successor_census(
        {
            "producer_v5": v5_guards[3].raw,
            "consumer_v5": v5_guards[4].raw,
            "launcher_v5": v5_guards[7].raw,
        },
        {
            "producer_v6": v6_guards[3].raw,
            "consumer_v6": v6_guards[4].raw,
            "launcher_v6": v6_guards[7].raw,
        },
        {
            "producer_v7": v7_guards[3].raw,
            "consumer_v7": v7_guards[4].raw,
            "launcher_v7": v7_guards[7].raw,
        },
        {
            "producer_v16r2": self_guard.raw,
            "consumer_v16r2": by_path[v16r2_consumer_path].raw,
            "launcher_v16r2": by_path[COLD_LAUNCHER].raw,
        })

    transition_guard = by_path[V16_TO_V16R2_TRANSITION]
    audit_guard = by_path[STATIC_AUDIT_V16R2]
    transition = strict_json(transition_guard.raw, "C79g v16r2 transition trust")
    audit = strict_json(audit_guard.raw, "C79g v16r2 static audit trust")
    outer = strict_json(outer_guard.raw, "C79g v16r2 cold-launch outer trust")
    need(isinstance(transition, dict) and isinstance(audit, dict) and
         isinstance(outer, dict),
         "post-source transition, audit, and outer are JSON objects")
    verify_object(transition, "C79g v16r2 transition trust")
    verify_object(audit, "C79g v16r2 static audit trust")
    verify_object(outer, "C79g v16r2 cold-launch outer trust")
    need(set(transition) == {
             "schema", "status", "receipt_path",
             "effective_checkpoint_object_sha256", "transition_kind",
             "append_only_predecessor_v3_regression",
             "rejected_unpublished_predecessor_v4",
             "published_then_officially_rejected_predecessor_v5",
             "published_then_officially_rejected_predecessor_v6",
             "published_then_officially_rejected_predecessor_v7",
             "published_then_officially_rejected_predecessor_v8",
             "published_then_officially_rejected_predecessor_v9",
             "published_then_officially_rejected_predecessor_v10",
             "published_then_officially_rejected_predecessor_v11",
             "published_then_officially_rejected_predecessor_v12",
             "rejected_prepublication_v13_supersession_receipt",
             "successor_v16r2_static_bundle", "physical_mode_policy",
             "cold_launch_boundary", "finalization_gates",
             "runtime_executed_during_transition",
             "C79_runtime_artifacts_created", "formal_global_closure_credit",
             "D02_unlock", "D02_gate_credit", "D02_task_credit",
             "D02_formal_pending_task_count", "D02_started",
             "all_persisted_credit", "object_sha256",
         } and
         transition.get("schema") ==
             "cm2.round306c79g.true-global-no-producer-consumer."
             "v16-to-v16r2-static-launch-transition.v1" and
         transition.get("transition_kind") ==
             "APPEND_ONLY_PUBLISHED_V14_RUNTIME_FAIL_CLOSED_REJECTION_TO_ZERO_CREDIT_V16R2_CLEAN_ROOM_SUCCESSOR",
         "transition exact top-level v12-to-v16r2 closed shape")
    _validate_final_static_audit(
        audit, self_guard, by_path, transition_guard, transition)

    successor = transition.get("successor_v16r2_static_bundle", {})
    predecessor = transition.get("append_only_predecessor_v3_regression", {})
    rejected_v4 = transition.get("rejected_unpublished_predecessor_v4", {})
    published_v5 = transition.get(
        "published_then_officially_rejected_predecessor_v5", {})
    published_v6 = transition.get(
        "published_then_officially_rejected_predecessor_v6", {})
    published_v7 = transition.get(
        "published_then_officially_rejected_predecessor_v7", {})
    published_v8 = transition.get(
        "published_then_officially_rejected_predecessor_v8", {})
    published_v9 = transition.get(
        "published_then_officially_rejected_predecessor_v9", {})
    published_v10 = transition.get(
        "published_then_officially_rejected_predecessor_v10", {})
    published_v11 = transition.get(
        "published_then_officially_rejected_predecessor_v11", {})
    published_v12 = transition.get(
        "published_then_officially_rejected_predecessor_v12", {})
    rejected_v13 = transition.get(
        "rejected_prepublication_v13_supersession_receipt", {})
    transition_rejection = predecessor.get("official_later_rejection", {})
    audited = audit.get("audited_v16r2_bundle", {})
    audit_predecessor = audit.get("predecessor_v3_exact10_regression", {})
    audit_rejection = audit.get("v3_official_later_rejection_regression", {})
    audit_v4 = audit.get("predecessor_v4_rejection_supersession_regression", {})
    audit_v5 = audit.get(
        "published_then_officially_rejected_predecessor_v5", {})
    audit_v6 = audit.get(
        "published_then_officially_rejected_predecessor_v6", {})
    audit_v7 = audit.get(
        "published_then_officially_rejected_predecessor_v7", {})
    audit_v8 = audit.get(
        "published_then_officially_rejected_predecessor_v8", {})
    audit_v9 = audit.get(
        "published_then_officially_rejected_predecessor_v9", {})
    audit_v10 = audit.get(
        "published_then_officially_rejected_predecessor_v10", {})
    audit_v11 = audit.get(
        "published_then_officially_rejected_predecessor_v11", {})
    audit_v12 = audit.get(
        "published_then_officially_rejected_predecessor_v12", {})
    audit_rejected_v13 = audit.get(
        "rejected_prepublication_v13_supersession_receipt", {})
    contract_cross = strict_json(
        by_path[CONTRACT].raw, "C79g v16r2 contract cross-check")
    audit_schema = audit.get("schema_and_constructor_closure", {})
    transition_pin = audited.get("v16_to_v16r2_transition_receipt", {})
    outer_entries = outer.get("exact8_ordered_entries")
    outer_manifest = outer.get("cold_launch_manifest", {})
    outer_launcher = outer.get("cold_launcher", {})

    _validate_v5_regression_section(
        published_v5, strict_bool_census, "v7 transition v5 predecessor")
    _validate_v5_regression_section(
        audit_v5, strict_bool_census, "v7 audit v5 predecessor")
    _validate_v6_regression_section(
        published_v6, strict_bool_census, "v7 transition v6 predecessor")
    _validate_v6_regression_section(
        audit_v6, strict_bool_census, "v7 audit v6 predecessor")
    _validate_v7_regression_section(
        published_v7, strict_bool_census, "v16r2 transition v7 predecessor")
    _validate_v7_regression_section(
        audit_v7, strict_bool_census, "v16r2 audit v7 predecessor")
    _validate_v8_regression_section(
        published_v8, v8_rollout_control_flow_incident,
        "v16r2 transition v8 predecessor")
    _validate_v8_regression_section(
        audit_v8, v8_rollout_control_flow_incident,
        "v16r2 audit v8 predecessor")
    _validate_v9_regression_section(
        published_v9, "v16r2 transition v9 predecessor")
    _validate_v9_regression_section(
        audit_v9, "v16r2 audit v9 predecessor")
    _validate_v10_regression_section(
        published_v10, v10_regression_label_prefix_incident,
        "v16r2 transition v10 predecessor")
    _validate_v10_regression_section(
        audit_v10, v10_regression_label_prefix_incident,
        "v16r2 audit v10 predecessor")
    _validate_v11_regression_section(
        published_v11, v10_colon_prefix_witness,
        "v16r2 transition v11 predecessor")
    _validate_v11_regression_section(
        audit_v11, v10_colon_prefix_witness,
        "v16r2 audit v11 predecessor")
    _validate_v12_regression_section(
        published_v12, "v16r2 transition v12 predecessor")
    _validate_v12_regression_section(
        audit_v12, "v16r2 audit v12 predecessor")
    need(all(contract_cross.get(key) == transition.get(key) == audit.get(key)
             for key in (
                 "published_then_officially_rejected_predecessor_v5",
                 "published_then_officially_rejected_predecessor_v6",
                 "published_then_officially_rejected_predecessor_v7",
                 "published_then_officially_rejected_predecessor_v8",
                 "published_then_officially_rejected_predecessor_v9",
                 "published_then_officially_rejected_predecessor_v10",
                 "published_then_officially_rejected_predecessor_v11",
                 "published_then_officially_rejected_predecessor_v12")) and
         contract_cross.get("v10_colon_prefix_witness") ==
             audit.get("v10_colon_prefix_witness") ==
             v10_colon_prefix_witness and
         contract_cross.get("v11_dual_validator_divergence_incident") ==
             audit.get("v11_dual_validator_divergence_incident") ==
             v11_dual_validator_divergence_incident,
         "contract transition audit exact v5-v12 and witness/incident consensus")
    supersession_receipt = self_guard.v13_supersession_receipt
    need(isinstance(supersession_receipt, dict),
         "held v13 supersession receipt available before JSON consensus")
    expected_rejected_v13 = \
        _expected_rejected_prepublication_v13_receipt(supersession_receipt)
    need(contract_cross.get(
             "rejected_prepublication_v13_supersession_receipt") ==
             rejected_v13 == audit_rejected_v13 == expected_rejected_v13 and
         len(expected_rejected_v13) == 7,
         "contract transition audit exact seven-key rejected v13 receipt consensus")
    need(published_v5.get("ordered_published_exact10") ==
             audit_v5.get("ordered_published_exact10") and
         published_v5.get("official_later_rejection") ==
             audit_v5.get("official_later_rejection") and
         published_v5.get("first_build_entry_attempt") ==
             audit_v5.get("first_build_entry_attempt") and
         published_v5.get("strict_bool_defect_census") ==
             audit_v5.get("strict_bool_defect_census"),
         "transition and audit reproduce one v5 published/rejected regression")
    need(published_v6.get("ordered_published_exact10") ==
             audit_v6.get("ordered_published_exact10") and
         published_v6.get("official_later_rejection") ==
             audit_v6.get("official_later_rejection") and
         published_v6.get("first_build_entry_attempt") ==
             audit_v6.get("first_build_entry_attempt") and
         published_v6.get("held_self_identity_defect") ==
             audit_v6.get("held_self_identity_defect"),
         "transition and audit reproduce one v6 published/rejected regression")
    need(published_v7.get("ordered_published_exact10") ==
             audit_v7.get("ordered_published_exact10") and
         published_v7.get("official_later_rejection") ==
             audit_v7.get("official_later_rejection") and
         published_v7.get("first_runtime_entry_attempt") ==
             audit_v7.get("first_runtime_entry_attempt") and
         published_v7.get("publication_lock_continuity_incident") ==
             audit_v7.get("publication_lock_continuity_incident") ==
             V7_LOCK_CONTINUITY_INCIDENT,
         "transition and audit reproduce one v7 publication incident and rejection")
    need(published_v8 == audit_v8 ==
             _expected_published_then_rejected_v8_proof(
                 v8_rollout_control_flow_incident),
         "transition and audit reproduce exact trusted v8 rollout incident and rejection")
    need(published_v9 == audit_v9 ==
             _expected_published_then_rejected_v9_proof(),
         "transition and audit reproduce exact v9 prechild shape-drift incident "
         "and rejection")
    need(published_v10 == audit_v10 ==
             _expected_published_then_rejected_v10_proof(),
         "transition and audit reproduce exact v10 regression-label-prefix "
         "incident and rejection")
    need(published_v11 == audit_v11 ==
             _expected_published_then_rejected_v11_proof(),
         "transition and audit reproduce exact v11 dual-validator divergence "
         "incident and rejection")
    need(published_v12 == audit_v12 ==
             _expected_published_then_rejected_v12_proof(),
         "transition and audit reproduce exact v12 shape incident and rejection")

    v4_receipt = rejected_v4.get("supersession_receipt", {})
    need(transition.get("status") ==
             "STATIC_BYTES_CLOSED_V16_TO_V16R2__PHYSICAL_FREEZE_PENDING__RUNTIME_NOT_AUTHORIZED" and
         audit.get("status") ==
             "PASS_DUAL_STATIC_PIN_NORMALIZED_AST_GO_V16R2__"
             "PHYSICAL_COLD_FREEZE_PENDING__"
             "RUNTIME_NOT_AUTHORIZED" and
         successor.get("build_only_producer", {}).get("file_sha256") ==
             self_guard.file_sha256 and
         audited.get("build_only_producer", {}).get("file_sha256") ==
             self_guard.file_sha256 and
         audited.get("contract", {}).get("file_sha256") == CONTRACT_FILE_PIN and
         audited.get("contract", {}).get("object_sha256") == CONTRACT_OBJECT_PIN and
         audited.get("closed_schema", {}).get("file_sha256") ==
             CLOSED_SCHEMA_FILE_PIN and
         len(predecessor.get("ordered_exact10", [])) == 10 and
         transition_rejection.get("file_sha256") == V3_REJECTION_FILE_PIN and
         transition_rejection.get("object_sha256") == V3_REJECTION_OBJECT_PIN and
         transition_rejection.get("path") ==
             str(V3_OFFICIAL_REJECTION.relative_to(ROOT)) and
         isinstance(v4_receipt, dict) and
         v4_receipt.get("file_sha256") ==
             V4_REJECTION_SUPERSESSION_FILE_PIN and
         v4_receipt.get("object_sha256") ==
             V4_REJECTION_SUPERSESSION_OBJECT_PIN and
         v4_receipt.get("status") ==
             "FROZEN_APPEND_ONLY_V4_STATIC_NO_RUN_REJECTION__THREE_ROOT_DEFECTS__V5_SUCCESSOR_ONLY" and
         len(rejected_v4.get("ordered_provisional_exact8", [])) == 8 and
         rejected_v4.get("receipt_recorded_root_defect_count") == 3 and
         len(rejected_v4.get("receipt_recorded_root_defects", [])) == 3 and
         rejected_v4.get(
             "additional_successor_discovered_v4_audit_defect_count") == 1 and
         len(rejected_v4.get(
             "additional_successor_discovered_v4_audit_defects", [])) == 1 and
         rejected_v4.get(
             "additional_successor_discovered_v4_audit_defects", [{}]
         )[0].get("id") ==
             "V4_STATIC_AUDIT_FALSE_REQUIRED_EQUALS_PROPERTIES_CLAIM" and
         rejected_v4.get("v4_execution_allowed") is False and
         audit_v4.get("receipt_file_sha256") ==
             V4_REJECTION_SUPERSESSION_FILE_PIN and
         audit_v4.get("receipt_object_sha256") ==
             V4_REJECTION_SUPERSESSION_OBJECT_PIN and
         audit_v4.get("ordered_provisional_exact8") ==
             rejected_v4.get("ordered_provisional_exact8") and
         audit_v4.get("ordered_provisional_exact8_matches_receipt") is True and
         audit_v4.get("receipt_recorded_root_defect_count") == 3 and
         audit_v4.get(
             "additional_successor_discovered_v4_audit_defect_count") == 1 and
         audit_v4.get("v4_root_defects_detected_present") is True and
         audit_v4.get(
             "v4_schema_required_property_false_assertion_present") is True and
         audit_v4.get(
             "v5_closed_object_required_property_mismatch_count") == 0 and
         audit_v4.get("same_defects_absent_from_v5") is True and
         audit_v4.get(
             "v6_closed_object_required_property_mismatch_count") == 0 and
         audit_v4.get("same_defects_absent_from_v6") is True and
         audit_v4.get(
             "v7_closed_object_required_property_mismatch_count") == 0 and
         audit_v4.get("same_defects_absent_from_v7") is True and
         audit_v4.get(
             "v16r2_closed_object_required_property_mismatch_count") == 0 and
         audit_v4.get("same_defects_absent_from_v16r2") is True and
         len(audit_predecessor.get("ordered_exact10", [])) == 10 and
         audit_predecessor.get("ordered_exact10") ==
             predecessor.get("ordered_exact10") and
         audit_predecessor.get("all_ten_file_pins_match") is True and
         audit_predecessor.get("all_declared_object_pins_match") is True and
         audit_rejection.get("file_sha256") == V3_REJECTION_FILE_PIN and
         audit_rejection.get("object_sha256") == V3_REJECTION_OBJECT_PIN and
         audit_schema.get(
             "all_schema_validation_keywords_supported_by_cold_launcher") is True and
         audit_schema.get("unknown_schema_validation_keyword_count") == 0 and
         audit_schema.get(
             "closed_object_required_property_mismatch_count") == 0 and
         audit_schema.get(
             "oneOf_keyword_absent_after_pin_definition_split") is True and
         transition_pin.get("file_sha256") == sha_bytes(transition_guard.raw) and
         transition_pin.get("object_sha256") == transition.get("object_sha256"),
         "transition/audit pin current v16r2 and preserve exact v3/v4/v7 history")

    need(set(outer) == {
             "schema", "status", "effective_checkpoint_object_sha256",
             "exact8_ordered_entries", "cold_launch_manifest", "cold_launcher",
             "all_exact8_regular_0444_nlink1_and_held_for_runtime",
             "outer_published_after_exact8_manifest",
             "runtime_entry_must_be_cold_launcher",
             "sole_external_static_file_anchor_is_launcher_sha256",
             "declared_external_tcb",
             "formal_global_closure_credit", "D02_unlock",
             "runtime_executed_during_static_freeze", "object_sha256"} and
         outer_guard.raw == canonical(outer) + b"\n" and
         outer.get("schema") ==
             "cm2.round306c79g.true-global-no-producer-consumer."
             "cold-launch-outer-receipt.v16r2" and
         outer.get("status") ==
             "FROZEN_COLD_LAUNCH_OUTER_LAST__EXACT8_MANIFEST_CLOSED__RUNTIME_DEFERRED" and
         outer.get("effective_checkpoint_object_sha256") ==
             UPSTREAM_CHECKPOINT_OBJECT_PIN and
         outer_entries == [
             {"path": entry["entry_name"], "file_sha256": entry["file_sha256"]}
             for entry in manifest_entries
         ] and
         outer_manifest.get("path") == str(COLD_MANIFEST.relative_to(ROOT)) and
         outer_manifest.get("file_sha256") == sha_bytes(manifest_guard.raw) and
         outer_manifest.get("ordered_entry_count") == 8 and
         outer_launcher.get("path") == str(COLD_LAUNCHER.relative_to(ROOT)) and
         outer_launcher.get("file_sha256") ==
             manifest_by_path[COLD_LAUNCHER] and
         outer.get("all_exact8_regular_0444_nlink1_and_held_for_runtime") is True and
         outer.get("outer_published_after_exact8_manifest") is True and
         outer.get("runtime_entry_must_be_cold_launcher") is True and
         outer.get("sole_external_static_file_anchor_is_launcher_sha256") is True and
         outer.get("declared_external_tcb") == [
             "EXTERNAL_HELD_FD_SEALED_MEMFD_BOOTSTRAP",
             "PYTHON3_ISOLATED_INTERPRETER",
             "LINUX_KERNEL_OPENAT2_STATX_MEMFD_PROCFS",
         ] and
         outer.get("formal_global_closure_credit") == 0 and
         outer.get("D02_unlock") is False and
         outer.get("runtime_executed_during_static_freeze") is False,
         "cold-launch v16r2 outer-last exact8 and zero-credit closure")
    need(os.environ.get(COLD_LAUNCHER_SHA_ENV) ==
             manifest_by_path[COLD_LAUNCHER],
         "sole inherited external launcher anchor matches held closure")
    supersession_receipt = self_guard.v13_supersession_receipt
    need(isinstance(supersession_receipt, dict),
         "held v13 supersession receipt available to static trust")
    rejected_prepublication_v13 = \
        _expected_rejected_prepublication_v13_receipt(supersession_receipt)
    return {
        "guards": [
            *by_path.values(), *v12_guards, *v11_guards, *v10_guards,
            *v9_guards, *v8_guards,
            *v7_guards, *v6_guards, *v5_guards, *v3_guards,
            *v4_guards, v3_rejection_guard, *v13_incident_guards,
            v12_rejection_guard, *v14_guards, v14_rejection_guard,
            v12_namespace_guard, v11_namespace_guard, v10_namespace_guard,
            v9_namespace_guard,
            v8_namespace_guard,
            v7_namespace_guard,
            v6_namespace_guard,
            v5_namespace_guard,
            manifest_guard, outer_guard,
        ],
        "by_path": by_path,
        "v12_published_by_path": v12_by_path,
        "v11_published_by_path": v11_by_path,
        "v10_published_by_path": v10_by_path,
        "v9_published_by_path": v9_by_path,
        "v8_published_by_path": v8_by_path,
        "v7_published_by_path": v7_by_path,
        "v6_published_by_path": v6_by_path,
        "v5_published_by_path": v5_by_path,
        "cold_manifest_guard": manifest_guard,
        "cold_outer_guard": outer_guard,
        "chronology": chronology,
        "v12_predecessor_chronology": v12_chronology,
        "v11_predecessor_chronology": v11_chronology,
        "v10_predecessor_chronology": v10_chronology,
        "v9_predecessor_chronology": v9_chronology,
        "v8_predecessor_chronology": v8_chronology,
        "v7_predecessor_chronology": v7_chronology,
        "v6_predecessor_chronology": v6_chronology,
        "v5_predecessor_chronology": v5_chronology,
        "v3_predecessor_chronology": v3_chronology,
        "transition": transition,
        "audit": audit,
        "outer": outer,
        "v12_official_rejection": v12_rejection,
        "v12_official_rejection_file_sha256":
            V12_OFFICIAL_REJECTION_FILE_PIN,
        "v12_official_rejection_object_sha256":
            V12_OFFICIAL_REJECTION_OBJECT_PIN,
        "v11_official_rejection": v11_rejection,
        "v11_official_rejection_file_sha256":
            V11_OFFICIAL_REJECTION_FILE_PIN,
        "v11_official_rejection_object_sha256":
            V11_OFFICIAL_REJECTION_OBJECT_PIN,
        "v10_official_rejection": v10_rejection,
        "v10_official_rejection_file_sha256":
            V10_OFFICIAL_REJECTION_FILE_PIN,
        "v10_official_rejection_object_sha256":
            V10_OFFICIAL_REJECTION_OBJECT_PIN,
        "v9_official_rejection": v9_rejection,
        "v9_official_rejection_file_sha256":
            V9_OFFICIAL_REJECTION_FILE_PIN,
        "v9_official_rejection_object_sha256":
            V9_OFFICIAL_REJECTION_OBJECT_PIN,
        "v8_official_rejection": v8_rejection,
        "v8_official_rejection_file_sha256":
            V8_OFFICIAL_REJECTION_FILE_PIN,
        "v8_official_rejection_object_sha256":
            V8_OFFICIAL_REJECTION_OBJECT_PIN,
        "v7_official_rejection": v7_rejection,
        "v7_official_rejection_file_sha256":
            V7_OFFICIAL_REJECTION_FILE_PIN,
        "v7_official_rejection_object_sha256":
            V7_OFFICIAL_REJECTION_OBJECT_PIN,
        "v6_official_rejection": v6_rejection,
        "v6_official_rejection_file_sha256":
            V6_OFFICIAL_REJECTION_FILE_PIN,
        "v6_official_rejection_object_sha256":
            V6_OFFICIAL_REJECTION_OBJECT_PIN,
        "v5_official_rejection": v5_rejection,
        "v5_official_rejection_file_sha256":
            V5_OFFICIAL_REJECTION_FILE_PIN,
        "v5_official_rejection_object_sha256":
            V5_OFFICIAL_REJECTION_OBJECT_PIN,
        "v4_rejection_supersession_file_sha256":
            V4_REJECTION_SUPERSESSION_FILE_PIN,
        "v4_rejection_supersession_object_sha256":
            V4_REJECTION_SUPERSESSION_OBJECT_PIN,
        "v5_published_exact10": _v5_published_exact10_records(),
        "v6_published_exact10": _v6_published_exact10_records(),
        "v7_published_exact10": _v7_published_exact10_records(),
        "v8_published_exact10": _v8_published_exact10_records(),
        "v9_published_exact10": _v9_published_exact10_records(),
        "v10_published_exact10": _v10_published_exact10_records(),
        "v11_published_exact10": _v11_published_exact10_records(),
        "v12_published_exact10": _v12_published_exact10_records(),
        "published_then_officially_rejected_predecessor_v8":
            _expected_published_then_rejected_v8_proof(
                v8_rollout_control_flow_incident),
        "v8_rollout_control_flow_incident": copy.deepcopy(
            v8_rollout_control_flow_incident),
        "published_then_officially_rejected_predecessor_v9":
            _expected_published_then_rejected_v9_proof(),
        "published_then_officially_rejected_predecessor_v10":
            _expected_published_then_rejected_v10_proof(),
        "published_then_officially_rejected_predecessor_v11":
            _expected_published_then_rejected_v11_proof(),
        "published_then_officially_rejected_predecessor_v12":
            _expected_published_then_rejected_v12_proof(),
        "rejected_prepublication_v13_supersession_receipt":
            rejected_prepublication_v13,
        "v12_v5_rejection_shape_incident":
            copy.deepcopy(V12_V5_REJECTION_SHAPE_INCIDENT),
        "v10_regression_label_prefix_incident": copy.deepcopy(
            v10_regression_label_prefix_incident),
        "v10_colon_prefix_witness": copy.deepcopy(v10_colon_prefix_witness),
        "v11_dual_validator_divergence_incident": copy.deepcopy(
            v11_dual_validator_divergence_incident),
        "v9_v6_held_self_identity_defect_shape_drift_incident":
            copy.deepcopy(V9_V6_DEFECT_SHAPE_DRIFT_INCIDENT),
        "v6_launcher_expanded_structural_evidence": copy.deepcopy(
            v6_launcher_expanded_structural_evidence),
        "v7_publication_lock_continuity_incident":
            copy.deepcopy(V7_LOCK_CONTINUITY_INCIDENT),
        "v6_first_build_entry_attempt": {
            "attempted": True,
            "producer_child_spawned": True,
            "candidate_write_started": False,
            "positive_runtime_surface_count": 0,
        },
        "v6_held_self_identity_defect": copy.deepcopy(
            V6_PERSISTED_HELD_SELF_IDENTITY_DEFECT),
        "v5_first_build_entry_attempt": {
            "attempted": True,
            "producer_child_spawned": False,
            "candidate_write_started": False,
            "positive_runtime_surface_count": 0,
        },
        "strict_bool_defect_census": strict_bool_census,
        "v5_forbidden_positive_and_stage_surface_count":
            len(V5_ALL_POSITIVE_AND_STAGE_SURFACES),
        "v6_forbidden_positive_and_stage_surface_count":
            len(V6_ALL_POSITIVE_AND_STAGE_SURFACES),
        "v7_forbidden_positive_and_stage_surface_count":
            len(V7_ALL_POSITIVE_AND_STAGE_SURFACES),
        "v8_forbidden_positive_and_stage_surface_count":
            len(V8_ALL_POSITIVE_AND_STAGE_SURFACES),
        "v9_forbidden_positive_and_stage_surface_count":
            len(V9_ALL_POSITIVE_AND_STAGE_SURFACES),
        "v10_forbidden_positive_and_stage_surface_count":
            len(V10_ALL_POSITIVE_AND_STAGE_SURFACES),
        "v11_forbidden_positive_and_stage_surface_count":
            len(V11_ALL_POSITIVE_AND_STAGE_SURFACES),
        "v12_forbidden_positive_and_stage_surface_count":
            len(V12_ALL_POSITIVE_AND_STAGE_SURFACES),
        "v16r2_predecessor_unique_live_identity_count":
            V16R2_PREDECESSOR_UNIQUE_LIVE_IDENTITY_COUNT,
        "v16r2_prepublication_unique_live_identity_count":
            V16R2_PREPUBLICATION_UNIQUE_LIVE_IDENTITY_COUNT,
        "v16r2_terminal_unique_live_identity_count":
            V16R2_TERMINAL_UNIQUE_LIVE_IDENTITY_COUNT,
        "v16r2_terminal_group_vector": list(V16R2_TERMINAL_GROUP_VECTOR),
        "transition_file_sha256": sha_bytes(transition_guard.raw),
        "transition_object_sha256": transition["object_sha256"],
        "static_audit_file_sha256": sha_bytes(audit_guard.raw),
        "static_audit_object_sha256": audit["object_sha256"],
        "cold_launcher_file_sha256": manifest_by_path[COLD_LAUNCHER],
        "cold_manifest_file_sha256": sha_bytes(manifest_guard.raw),
        "cold_outer_file_sha256": sha_bytes(outer_guard.raw),
        "cold_outer_object_sha256": outer["object_sha256"],
        **chronology,
        "cold_exact10_identities_unique_same_mount": True,
        "published_v12_exact10_plus_official_rejection_strictly_replayed": True,
        "published_v11_exact10_plus_official_rejection_strictly_replayed": True,
        "published_v10_exact10_plus_official_rejection_strictly_replayed": True,
        "published_v9_exact10_plus_official_rejection_strictly_replayed": True,
        "published_v8_exact10_plus_official_rejection_strictly_replayed": True,
        "published_v7_exact10_plus_official_rejection_strictly_replayed": True,
        "published_v6_exact10_plus_official_rejection_strictly_replayed": True,
        "published_v5_exact10_plus_official_rejection_strictly_replayed": True,
        "published_v3_exact10_v4_draft7_and_v3_rejection_strictly_replayed": True,
    }


def ensure_launch_configuration() -> HeldSelf:
    global _COLD_WORKSPACE_ROOT_FD
    global _COLD_WORKSPACE_ROOT_BEFORE
    global _COLD_WORKSPACE_ROOT_MOUNT_ID
    # Absolute first gate: pin installation is proved before reading any
    # inherited fd, environment-supplied workspace path, bundle, or runtime path.
    need(FINAL_V16R2_CORE_PINS_INSTALLED is True,
         "v16r2 final core pins are not installed; runtime permanently disabled")
    need(all(value not in V16R2_DRAFT_CORE_PIN_SENTINELS for value in (
             CONTRACT_FILE_PIN, CONTRACT_OBJECT_PIN, CLOSED_SCHEMA_FILE_PIN)),
         "v16r2 draft contract/schema sentinels must all be replaced before runtime")
    need(sys.flags.isolated == 1 and sys.flags.dont_write_bytecode == 1 and
         sys.flags.no_site == 1,
         "producer requires cold launcher Python -I -B -S isolation")
    exec_fd_text = os.environ.get(COLD_EXEC_FD_ENV, "")
    source_fd_text = os.environ.get(COLD_SOURCE_FD_ENV, "")
    coordination_fd_text = os.environ.get(COLD_COORDINATION_PARENT_FD_ENV, "")
    root_fd_text = os.environ.get(COLD_WORKSPACE_ROOT_FD_ENV, "")
    authority_fd_texts = tuple(
        os.environ.get(environment_name, "")
        for _role, environment_name in
            V14_INHERITED_AUTHORITY_EXACT12_FD_ENV_ORDER)
    launcher_sha = os.environ.get(COLD_LAUNCHER_SHA_ENV, "")
    fd_texts = (exec_fd_text, source_fd_text,
                coordination_fd_text, root_fd_text,
                *authority_fd_texts)
    need(all(value and len(value) <= 10 and
             all(ch in "0123456789" for ch in value) and
             int(value) >= 3 for value in fd_texts) and
         len(fd_texts) == len({int(value) for value in fd_texts}) ==
             V16R2_CHILD_PASS_FD_COUNT == 16 and
         EXECUTED_SOURCE == Path("/proc/self/fd") / exec_fd_text and
         _cold_root_text == str(ROOT) and ROOT.is_absolute() and
         SELF == ROOT / "deliverables/cm2_round306c79g_true_global_no_producer_consumer_v16r2r63ah_repair_semantic_source.py",
         "producer accepts exactly sixteen distinct decimal cold-launch fds and "
         "sealed-exec procfd entry")
    need(all(len(value) == 64 and value != "0" * 64 and
             all(ch in "0123456789abcdef" for ch in value)
             for value in (launcher_sha,)),
         "producer sole external cold-launcher anchor is exact SHA-256")
    static_pins = (
        CONTRACT_FILE_PIN, CONTRACT_OBJECT_PIN, CLOSED_SCHEMA_FILE_PIN,
        V3_REJECTION_FILE_PIN, V3_REJECTION_OBJECT_PIN,
        V4_REJECTION_SUPERSESSION_FILE_PIN,
        V4_REJECTION_SUPERSESSION_OBJECT_PIN,
        V5_OFFICIAL_REJECTION_FILE_PIN,
        V5_OFFICIAL_REJECTION_OBJECT_PIN,
        V6_OFFICIAL_REJECTION_FILE_PIN,
        V6_OFFICIAL_REJECTION_OBJECT_PIN,
        V7_OFFICIAL_REJECTION_FILE_PIN,
        V7_OFFICIAL_REJECTION_OBJECT_PIN,
        V7_LOCK_CONTINUITY_INCIDENT_OBJECT_PIN,
        V8_OFFICIAL_REJECTION_FILE_PIN,
        V8_OFFICIAL_REJECTION_OBJECT_PIN,
        V9_OFFICIAL_REJECTION_FILE_PIN,
        V9_OFFICIAL_REJECTION_OBJECT_PIN,
        V10_OFFICIAL_REJECTION_FILE_PIN,
        V10_OFFICIAL_REJECTION_OBJECT_PIN,
        V11_OFFICIAL_REJECTION_FILE_PIN,
        V11_OFFICIAL_REJECTION_OBJECT_PIN,
        V10_COLON_PREFIX_WITNESS_OBJECT_PIN,
        V10_COLON_PREFIX_HELPER_NORMALIZED_AST_SHA256,
        V11_DUAL_VALIDATOR_DIVERGENCE_INCIDENT_CANONICAL_SHA256,
        V11_PUBLISHED_REJECTED_PROOF_CANONICAL_SHA256,
        V13_SUPERSESSION_RECEIPT_FILE_PIN,
        V13_SUPERSESSION_RECEIPT_OBJECT_PIN,
        *(row[2] for row in V14_INHERITED_AUTHORITY_EXACT12),
        *(row[3] for row in V14_INHERITED_AUTHORITY_EXACT12
          if row[3] is not None),
    )
    need(all(isinstance(value, str) and len(value) == 64 and
             value != "0" * 64 and all(ch in "0123456789abcdef" for ch in value)
             for value in static_pins),
         "C79g v16r2 exact non-placeholder contract/schema/rejection pins")
    need(set(C78S_FINAL["pins"]) == set(C78S_NAMES) and
         all(isinstance(value, str) and len(value) == 64
             for value in C78S_FINAL["pins"].values()) and
         all(isinstance(C78S_FINAL[key], str) and len(C78S_FINAL[key]) == 64
             for key in ("result_object_sha256", "verification_A_file_sha256",
                         "verification_A_object_sha256", "verification_B_file_sha256",
                         "verification_B_object_sha256", "verifier_source_file_sha256",
                         "final_manifest_file_sha256", "final_outer_file_sha256",
                         "final_outer_object_sha256")) and
         C78S_FINAL["final_stage_member_count_per_build"] == 13 and
         C78S_FINAL["closure_receipt_is_final_outer"] is True and
         C78S_FINAL["extra_completion_receipt_exists"] is False,
         "C79g v16r2 exact filled launch configuration")
    need(_COLD_WORKSPACE_ROOT_FD == -1 and
         _COLD_WORKSPACE_ROOT_BEFORE is None and
         _COLD_WORKSPACE_ROOT_MOUNT_ID == -1,
         "cold workspace root guard binds exactly once")
    authority_fd_by_path = {
        ROOT / row[1]: int(fd_text)
        for row, fd_text in zip(
            V14_INHERITED_AUTHORITY_EXACT12, authority_fd_texts)}
    self_guard = HeldSelf(
        int(exec_fd_text), int(source_fd_text),
        int(coordination_fd_text), int(root_fd_text), authority_fd_by_path)
    root_guard = HeldWorkspaceRoot(
        int(root_fd_text), self_guard.source_fd, int(coordination_fd_text))
    _COLD_WORKSPACE_ROOT_FD = root_guard.fd
    _COLD_WORKSPACE_ROOT_BEFORE = root_guard.before
    _COLD_WORKSPACE_ROOT_MOUNT_ID = root_guard.mount_id
    workspace_root_terminal_replay()
    self_guard.terminal_replay()
    return self_guard


def secure_snapshot(path: Path, required_mode: int | None = None) -> tuple[bytes, tuple[int, int]]:
    try:
        before_path = path.lstat()
    except FileNotFoundError as exc:
        raise Reject("missing input:" + str(path)) from exc
    need(stat.S_ISREG(before_path.st_mode) and not path.is_symlink(),
         "regular non-symlink input:" + str(path))
    descriptor = openat2_beneath(path, os.O_RDONLY)
    try:
        before_fd = os.fstat(descriptor)
        before_mount = statx_mount_id(descriptor)
        need(stat.S_ISREG(before_fd.st_mode) and before_fd.st_nlink == 1,
             "regular single-link descriptor:" + str(path))
        if required_mode is not None:
            need(stat.S_IMODE(before_fd.st_mode) == required_mode,
                 f"required mode {required_mode:o}:" + str(path))
        need((before_path.st_dev, before_path.st_ino) == (before_fd.st_dev, before_fd.st_ino),
             "path/descriptor identity before read:" + str(path))
        blocks: list[bytes] = []
        while True:
            block = os.read(descriptor, 1 << 20)
            if not block:
                break
            blocks.append(block)
        after_fd = os.fstat(descriptor)
        need((before_fd.st_dev, before_fd.st_ino, before_fd.st_size, before_fd.st_mtime_ns,
              before_fd.st_ctime_ns, before_fd.st_nlink) ==
             (after_fd.st_dev, after_fd.st_ino, after_fd.st_size, after_fd.st_mtime_ns,
              after_fd.st_ctime_ns, after_fd.st_nlink),
             "descriptor stable during read:" + str(path))
        need(statx_mount_id(descriptor) == before_mount,
             "descriptor mount identity stable during read:" + str(path))
    finally:
        os.close(descriptor)
    after_path = path.lstat()
    need((after_path.st_dev, after_path.st_ino, after_path.st_size, after_path.st_mtime_ns,
          after_path.st_ctime_ns, after_path.st_nlink) ==
         (before_fd.st_dev, before_fd.st_ino, before_fd.st_size, before_fd.st_mtime_ns,
          before_fd.st_ctime_ns, before_fd.st_nlink),
         "path identity after read:" + str(path))
    return b"".join(blocks), (before_fd.st_dev, before_fd.st_ino)


def secure_unpinned(path: Path, required_mode: int | None = None) -> bytes:
    return secure_snapshot(path, required_mode)[0]


def secure_file(path: Path, expected_sha256: str) -> bytes:
    raw = secure_unpinned(path)
    need(sha_bytes(raw) == expected_sha256, "file pin:" + str(path))
    return raw


def secure_directory(path: Path, required_mode: int | None = None) -> None:
    info = path.lstat()
    need(stat.S_ISDIR(info.st_mode) and not path.is_symlink(), "secure directory:" + str(path))
    if required_mode is not None:
        need(stat.S_IMODE(info.st_mode) == required_mode,
             f"required directory mode {required_mode:o}:" + str(path))


def directory_state(path: Path) -> tuple[int, int, int, int, int, int]:
    info = path.lstat()
    need(stat.S_ISDIR(info.st_mode) and not path.is_symlink(), "directory state:" + str(path))
    return (info.st_dev, info.st_ino, info.st_mode, info.st_mtime_ns,
            info.st_ctime_ns, info.st_nlink)


def rooted(relative: str) -> Path:
    candidate = Path(relative)
    path = Path(os.path.abspath(str(candidate if candidate.is_absolute() else ROOT / candidate)))
    need(path == ROOT or ROOT in path.parents, "path escapes workspace")
    return path


def gzip_rows(raw: bytes, label: str) -> list[dict[str, Any]]:
    decoder = zlib.decompressobj(16 + zlib.MAX_WBITS)
    try:
        plain = decoder.decompress(raw) + decoder.flush()
    except zlib.error as exc:
        raise Reject(label + ":gzip decode") from exc
    need(decoder.eof is True and
         not decoder.unused_data and not decoder.unconsumed_tail,
         label + ":exactly one complete gzip member")
    need(plain.endswith(b"\n"), label + ":terminal newline")
    rows: list[dict[str, Any]] = []
    for ordinal, line in enumerate(plain.splitlines(), 1):
        need(bool(line), label + ":blank line")
        value = strict_json(line, f"{label}:{ordinal}")
        need(isinstance(value, dict), label + ":row object")
        verify_row(value, f"{label}:{ordinal}")
        rows.append(value)
    return rows


def gzip_encode(rows: Iterable[Mapping[str, Any]]) -> tuple[bytes, dict[str, Any]]:
    line_hashes: list[str] = []
    plain = bytearray()
    count = 0
    for row in rows:
        verify_row(row, "output")
        line = canonical(dict(row))
        plain.extend(line + b"\n")
        line_hashes.append(sha_bytes(line))
        count += 1
    sink = io.BytesIO()
    with gzip.GzipFile(filename="", mode="wb", fileobj=sink, mtime=0) as stream:
        stream.write(bytes(plain))
    raw = sink.getvalue()
    return raw, {
        "row_count": count,
        "file_sha256": sha_bytes(raw),
        "uncompressed_sha256": sha_bytes(bytes(plain)),
        "row_hash_line_sequence_sha256": digest(line_hashes),
        "single_gzip_member": True,
    }


def exclusive_at(stage: HeldMutableStage, name: str, raw: bytes) -> HeldCreatedFile:
    need(name not in {"", ".", ".."} and "/" not in name,
         "stage member is one exact basename")
    flags = (os.O_RDWR | os.O_CREAT | os.O_EXCL | os.O_CLOEXEC |
             getattr(os, "O_NOFOLLOW", 0))
    descriptor = os.open(name, flags, 0o444, dir_fd=stage.fd)
    try:
        view = memoryview(raw)
        while view:
            written = os.write(descriptor, view)
            need(written > 0, "write progress:" + name)
            view = view[written:]
        os.fchmod(descriptor, 0o444)
        os.fsync(descriptor)
        return HeldCreatedFile(stage.path / name, descriptor, raw)
    except BaseException:
        os.close(descriptor)
        raise


def hold_pinned_historical(
        paths: Mapping[str, Path], pins: Mapping[str, str],
        expected_modes: Mapping[Path, int], label: str,
        ) -> tuple[dict[str, bytes], list[HeldPinnedInput]]:
    """Hold an exact historical family under explicit observed mode policy."""
    need(set(paths) == set(pins) and set(paths.values()) <= set(expected_modes),
         label + ":path/pin/mode policy closure")
    guards = [
        HeldPinnedInput(paths[key], label + ":" + key,
                        expected_modes[paths[key]], pins[key])
        for key in sorted(paths)
    ]
    need(len({guard.identity for guard in guards}) == len(guards),
         label + ":pairwise historical identities distinct")
    return ({key: guards[index].raw for index, key in enumerate(sorted(paths))},
            guards)


def read_dual(directory_a: Path, directory_b: Path,
              names: Mapping[str, str], pins: Mapping[str, str], label: str) -> dict[str, bytes]:
    secure_directory(directory_a)
    secure_directory(directory_b)
    need(set(names) == set(pins), label + ":name/pin keys")
    out: dict[str, bytes] = {}
    for key in sorted(names):
        left = secure_file(directory_a / names[key], pins[key])
        right = secure_file(directory_b / names[key], pins[key])
        need(left == right, label + ":dual byte identity:" + key)
        out[key] = left
    return out


def parse_manifest_ordered(raw: bytes, label: str) -> list[dict[str, str]]:
    need(raw.endswith(b"\n"), label + ":newline")
    out: list[dict[str, str]] = []
    seen: set[str] = set()
    for line in raw.decode("ascii").splitlines():
        parts = line.split("  ", 1)
        need(len(parts) == 2 and len(parts[0]) == 64, label + ":entry")
        need(parts[1] not in seen, label + ":duplicate filename")
        seen.add(parts[1])
        out.append({"file_sha256": parts[0], "entry_name": parts[1]})
    return out


def parse_manifest(raw: bytes, label: str) -> dict[str, str]:
    return {entry["entry_name"]: entry["file_sha256"]
            for entry in parse_manifest_ordered(raw, label)}


def _line_sequence_sha256(values: Iterable[str]) -> str:
    return sha_bytes(b"".join((value + "\n").encode("ascii") for value in values))


def validate_c55b_topology(cell_rows: list[dict[str, Any]],
                           edge_rows: list[dict[str, Any]],
                           component_rows: list[dict[str, Any]]) -> dict[str, Any]:
    """Rebuild C55B component/glue/reflection structure from row evidence."""
    need(len(cell_rows) == 1_724 and len(edge_rows) == EXPECTED_C55B_EDGES and
         len(component_rows) == 26, "C55B topology:exact ledger counts")
    cells = one_index(cell_rows, "cell_id", "C55B topology cells")
    components = one_index(component_rows, "component_index", "C55B topology components")
    need(set(components) == set(range(26)), "C55B topology:dense component indices")
    need(Counter(row["cell_count"] for row in component_rows) == Counter({1: 24, 850: 2}),
         "C55B topology:component size census")

    cells_by_component: dict[int, list[dict[str, Any]]] = defaultdict(list)
    pairs: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for row in cell_rows:
        index = row.get("component_index")
        need(index in components and row.get("component_id") == components[index].get("component_id"),
             "C55B topology:crosswalk component join")
        need(row.get("current_effective_disposition") in
             {"EARLIEST_PREFIX_EXCLUDED", "UNRESOLVED_R1648_CONTINUATION"},
             "C55B topology:crosswalk disposition")
        cells_by_component[index].append(row)
        pairs[row.get("pair_index")].append(row)

    allowed_glue = {
        "INHERITED_FIRST_EVENT_FACE":
            ({"LIVE_TYPED_EVENT", "EXCLUDED_EVENT_CANDIDATE"}, 1,
             "EXPLICIT_INHERITED_EVENT_FACE_WITH_C34_BINDING_IF_LIVE"),
        "INTRA_CHART_FACE":
            ({"ORDINARY_INTERNAL", "ORDINARY_TO_TYPED_EVENT_BOUNDARY",
              "ORDINARY_TO_FORMAL_EXCLUSION_BOUNDARY"}, 1,
             "EXPLICIT_COMMON_FACE_WITH_EXACT_COORDINATE_AND_SPAN"),
        "SOURCE_CHART_TRANSITION":
            ({"ORDINARY_INTERNAL", "ORDINARY_TO_TYPED_EVENT_BOUNDARY"}, 1,
             "EXPLICIT_COMMON_FACE_WITH_EXACT_COORDINATE_AND_SPAN"),
        "SOURCE_GRAZING_FACE":
            ({"GLOBAL_GRAZING_INVENTORY"}, 1,
             "EXPLICIT_C32_GRAZING_FACE_GEOMETRY_ONLY"),
        "SOURCE_GRAZING_SEAM_CORNER":
            ({"GLOBAL_CORNER_INVENTORY"}, 0,
             "EXPLICIT_C32_ZERO_DIMENSIONAL_SEAM_GRAZING_GLUE"),
    }
    edges_by_component: dict[int, list[str]] = defaultdict(list)
    for row in edge_rows:
        kind = row.get("glue_kind")
        need(kind in allowed_glue, "C55B topology:explicit glue kind")
        scopes, dimension, proof = allowed_glue[kind]
        need(row.get("scope") in scopes and row.get("dimension") == dimension and
             row.get("gluing_proof_kind") == proof and
             row.get("coordinate_or_key_coincidence_used") is False,
             "C55B topology:glue proof semantics")
        endpoint_components: set[int] = set()
        for side in ("left", "right"):
            cell_id = row.get(side + "_cell_id")
            disposition = row.get(side + "_disposition")
            if cell_id in cells:
                endpoint = cells[cell_id]
                need(disposition == endpoint["current_effective_disposition"],
                     "C55B topology:edge disposition join")
                endpoint_components.add(endpoint["component_index"])
            else:
                need(cell_id is None or isinstance(cell_id, str),
                     "C55B topology:edge endpoint type")
        indices = row.get("ordinary_component_indices")
        need(isinstance(indices, list) and indices == sorted(set(indices)) and
             len(indices) <= 1 and set(indices) == endpoint_components,
             "C55B topology:edge component incidence")
        for index in indices:
            edges_by_component[index].append(row["row_sha256"])
    need(Counter(row["glue_kind"] for row in edge_rows) == Counter(EXPECTED_GLUE_KIND_CENSUS) and
         Counter(row["scope"] for row in edge_rows) == Counter(EXPECTED_EDGE_SCOPE_CENSUS) and
         Counter(row["dimension"] for row in edge_rows) == Counter({1: 5_350, 0: 8}) and
         Counter(row["terminal_credit"] for row in edge_rows) == Counter({0: 5_062, 1: 296}),
         "C55B topology:edge/glue exact census")

    anchor_component_count = 0
    for index in range(26):
        component = components[index]
        grouped = sorted(cells_by_component[index], key=lambda row: row["cell_id"])
        ids = [row["cell_id"] for row in grouped]
        row_hashes = [row["row_sha256"] for row in grouped]
        excluded = sorted(row["cell_id"] for row in grouped
                          if row["current_effective_disposition"] == "EARLIEST_PREFIX_EXCLUDED")
        unresolved = sorted(row["cell_id"] for row in grouped
                            if row["current_effective_disposition"] == "UNRESOLVED_R1648_CONTINUATION")
        edge_hashes = sorted(edges_by_component[index])
        need(component.get("cell_count") == len(grouped) and
             component.get("member_cell_ids") == ids and
             component.get("member_cell_row_sha256s") == row_hashes and
             component.get("member_cell_ids_sha256") == digest(ids) and
             component.get("member_cell_row_sequence_sha256") == digest(row_hashes),
             "C55B topology:component member reconstruction")
        need(component.get("current_excluded_cell_count") == len(excluded) and
             component.get("current_excluded_cell_ids_sha256") == digest(excluded) and
             component.get("current_unresolved_cell_count") == len(unresolved) and
             component.get("current_unresolved_cell_ids_sha256") == digest(unresolved),
             "C55B topology:component disposition reconstruction")
        need(component.get("edge_and_glue_row_sha256s") == edge_hashes and
             component.get("edge_and_glue_row_sequence_sha256") == digest(edge_hashes),
             "C55B topology:component edge/glue reconstruction")
        anchor_cells = [row for row in grouped
                        if row.get("known_sheet_anchor_role") ==
                           "ANCHOR_CELL_CONTAINS_STRICT_OPEN_COLLAR"]
        has_anchor = bool(anchor_cells)
        need(len(anchor_cells) <= 1 and component.get("positive_area_anchor_proof_present") is has_anchor and
             component.get("anchor_is_strict_subset_not_whole_component") is
                 (has_anchor and len(grouped) > 1) and
             component.get("whole_component_connected_to_known_credit") == 0 and
             component.get("singleton_isolation_promoted") is False,
             "C55B topology:known-sheet/nonpromotion reconstruction")
        if has_anchor:
            anchor_component_count += 1
            need(isinstance(component.get("known_sheet_anchor"), dict) and
                 component["known_sheet_anchor"].get("anchor_cell_id") == anchor_cells[0]["cell_id"] and
                 component["known_sheet_anchor"].get("positive_area_open_support") is True and
                 component["known_sheet_anchor"].get("whole_component_connected_credit") == 0,
                 "C55B topology:known-sheet anchor join")
        else:
            need(component.get("known_sheet_anchor") is None,
                 "C55B topology:unanchored component")
    need(anchor_component_count == 2 and
         Counter(row["current_unresolved_cell_count"] for row in component_rows) ==
             Counter({1: 24, 562: 2}) and
         Counter(row["current_excluded_cell_count"] for row in component_rows) ==
             Counter({0: 24, 288: 2}),
         "C55B topology:component exact census")

    need(set(pairs) == set(range(862)) and all(len(rows) == 2 for rows in pairs.values()),
         "C55B topology:dense two-sided reflection pairs")
    component_pair_counts: Counter[tuple[int, int]] = Counter()
    whole: Counter[bool] = Counter()
    newly_whole: list[int] = []
    c37_sequence: list[str] = []
    c42_sequence: list[str] = []
    c53_sequence: list[str] = []
    for pair_index in range(862):
        rows = pairs[pair_index]
        left, right = rows
        need(left["cell_id"] != right["cell_id"] and
             left["reflection_partner_cell_id"] == right["cell_id"] and
             right["reflection_partner_cell_id"] == left["cell_id"],
             "C55B topology:reflection involution")
        component_pair = tuple(sorted({left["component_index"], right["component_index"]}))
        need(len(component_pair) == 2, "C55B topology:cross-component reflection")
        component_pair_counts[component_pair] += 1
        for key, sequence in (("C37_pair_row_sha256", c37_sequence),
                              ("C42_parent_row_sha256", c42_sequence),
                              ("C53_parent_projection_object_sha256", c53_sequence)):
            values = {row[key] for row in rows}
            need(len(values) == 1, "C55B topology:pair authority agreement")
            sequence.append(next(iter(values)))
        whole_values = {row["whole_pair_terminal_after_C53"] for row in rows}
        new_values = {row["newly_whole_by_C53_pair_seal"] for row in rows}
        need(len(whole_values) == len(new_values) == 1,
             "C55B topology:pair boolean agreement")
        whole[next(iter(whole_values))] += 1
        if next(iter(new_values)):
            newly_whole.append(pair_index)
    need(component_pair_counts == Counter(EXPECTED_COMPONENT_PAIR_COUNTS) and
         set(index for pair in component_pair_counts for index in pair) == set(range(26)),
         "C55B topology:component reflection involution census")
    need(whole == Counter({True: 288, False: 574}) and newly_whole == [1],
         "C55B topology:whole/nonwhole pair census")
    need(len(set(c37_sequence)) == len(set(c42_sequence)) == len(set(c53_sequence)) == 862 and
         _line_sequence_sha256(c37_sequence) == C55B_C37_PAIR_INDEX_SEQUENCE_PIN and
         _line_sequence_sha256(c42_sequence) == C55B_C42_PAIR_INDEX_SEQUENCE_PIN and
         _line_sequence_sha256(c53_sequence) == C55B_C53_PAIR_INDEX_SEQUENCE_PIN,
         "C55B topology:pair-index authority sequences")
    return {
        "cell_rows": 1_724, "edge_rows": 5_358, "component_rows": 26,
        "reflection_pairs": 862, "cross_component_pairs": 862,
        "same_component_pairs": 0, "component_involution_has_fixed_point": False,
        "component_involution_summary_sha256": C55B_COMPONENT_INVOLUTION_SUMMARY_PIN,
        "full_pair_summary_sha256": C55B_FULL_PAIR_SUMMARY_PIN,
        "known_sheet_anchor_components": 2, "whole_component_connected_credit": 0,
        "public_unresolved_cells": 1_148,
    }


def validate_c42_c53_kraft(cell_rows: list[dict[str, Any]]) -> dict[str, Any]:
    """Reconstruct every parent Kraft claim through C42, C53 and C55B."""
    c42_candidate_universe = C42_CANDIDATE_MANIFEST_MEMBERS | {"root_manifest.sha256"}
    c42_candidate_guard = HeldDirectory(
        C42_CANDIDATE_DIR, c42_candidate_universe,
        C42_CANDIDATE_DIRECTORY_EXPECTED_MODE, 2,
        "C42 historical candidate exact9 observed directory")
    c42_independent_audit_directory_guard = HeldDirectory(
        C42_INDEPENDENT_AUDIT_DIR, {C42_INDEPENDENT_AUDIT_PATH.name},
        C42_INDEPENDENT_AUDIT_DIRECTORY_EXPECTED_MODE, 2,
        "C42 historical independent-audit exact1 observed directory")
    c42_installation_receipt_directory_guard = HeldDirectory(
        C42_INSTALLATION_RECEIPT_DIR, {C42_INSTALLATION_RECEIPT_PATH.name},
        C42_INSTALLATION_RECEIPT_DIRECTORY_EXPECTED_MODE, 2,
        "C42 historical installation-receipt exact1 observed directory")
    c42_held_directories = [
        c42_candidate_guard,
        c42_independent_audit_directory_guard,
        c42_installation_receipt_directory_guard,
    ]
    held_by_path: dict[Path, HeldPinnedInput] = {}
    for key in sorted(C42_C53_PATHS):
        path = C42_C53_PATHS[key]
        held_by_path[path] = HeldPinnedInput(
            path, "C42/C53 historical full10:" + key,
            C42_C53_EXPECTED_MODES[key], C42_C53_PINS[key])
    for name in sorted(c42_candidate_universe):
        path = C42_CANDIDATE_DIR / name
        if path not in held_by_path:
            held_by_path[path] = HeldPinnedInput(
                path, "C42 historical candidate exact9:" + name,
                C42_CANDIDATE_MEMBER_EXPECTED_MODE)
    held_inputs = [held_by_path[path] for path in sorted(held_by_path, key=str)]
    need(len(held_inputs) == 16 and
         len({guard.identity for guard in held_inputs}) == 16,
         "C42 full10 union candidate exact9 has 16 globally unique held identities")

    parent_raw = held_by_path[C42_PARENT_PATH].raw
    result_raw = held_by_path[C42_RESULT_PATH].raw
    manifest_raw = held_by_path[C42_MANIFEST_PATH].raw
    c42_audit_raw = held_by_path[C42_INDEPENDENT_AUDIT_PATH].raw
    c42_installation_raw = held_by_path[C42_INSTALLATION_RECEIPT_PATH].raw
    c42_candidate_token_raw = held_by_path[C42_CANDIDATE_TOKEN_PATH].raw
    c42_audit_token_raw = held_by_path[C42_AUDIT_TOKEN_PATH].raw
    seal_raw = held_by_path[C42_SEAL_PATH].raw
    audit_raw = held_by_path[C53_AUDIT_PATH].raw
    head_raw = held_by_path[C53_HEAD_PATH].raw

    c42_rows = gzip_rows(parent_raw, "C42 installed parent conservation")
    need(len(c42_rows) == EXPECTED_PAIRS, "C42 Kraft:exact 862 rows")
    c42_by_pair = one_index(c42_rows, "pair_index", "C42 Kraft")
    need(set(c42_by_pair) == set(range(EXPECTED_PAIRS)), "C42 Kraft:dense pair index")
    for pair_index in range(EXPECTED_PAIRS):
        row = c42_by_pair[pair_index]
        need(row.get("parent_Kraft_conservation") == "1" and
             row.get("D02_gate_credit") == 0 and
             row.get("terminal_reflection_transport_materialized") is True,
             "C42 Kraft:itemwise exact conservation independent of terminal route")
    c42_sequence = [c42_by_pair[index]["row_sha256"] for index in range(EXPECTED_PAIRS)]
    need(_line_sequence_sha256(c42_sequence) == C55B_C42_PAIR_INDEX_SEQUENCE_PIN,
         "C42 Kraft:row-hash sequence")

    c42_result = strict_json(result_raw, "C42 result")
    verify_object(c42_result, "C42 result", C42_RESULT_OBJECT_PIN)
    need(c42_result.get("closure_census", {}).get("parent_conservation_row_count") == EXPECTED_PAIRS and
         c42_result.get("formal_authority") is False and
         c42_result.get("producer_output_is_authority") is False,
         "C42 Kraft:producer nonauthority boundary")
    manifest = parse_manifest_ordered(manifest_raw, "C42 root manifest")
    need(len(manifest) == 8 and
         {entry["entry_name"] for entry in manifest} == C42_CANDIDATE_MANIFEST_MEMBERS and
         next(entry for entry in manifest if entry["entry_name"] == "parent_conservation.jsonl.gz")["file_sha256"] == C42_C53_PINS["C42_parent"] and
         next(entry for entry in manifest if entry["entry_name"] == "result.json")["file_sha256"] == C42_C53_PINS["C42_result"],
         "C42 Kraft:exact root manifest")
    c42_candidate_member_raw: dict[str, bytes] = {}
    for entry in manifest:
        name = entry["entry_name"]
        if name == "parent_conservation.jsonl.gz":
            raw = parent_raw
        elif name == "result.json":
            raw = result_raw
        else:
            raw = held_by_path[C42_CANDIDATE_DIR / name].raw
        need(sha_bytes(raw) == entry["file_sha256"],
             "C42 Kraft:manifest member replay:" + name)
        c42_candidate_member_raw[name] = raw
    need(set(c42_candidate_member_raw) == C42_CANDIDATE_MANIFEST_MEMBERS,
         "C42 Kraft:all exact8 manifest members replayed")

    need(c42_candidate_token_raw == (C42_CANDIDATE_TOKEN + "\n").encode("ascii") and
         c42_audit_token_raw == (C42_AUDIT_TOKEN + "\n").encode("ascii"),
         "C42 Kraft:exact installed candidate/audit token bytes")
    c42_audit = strict_json(c42_audit_raw, "C42 independent audit")
    verify_object(c42_audit, "C42 independent audit", C42_INDEPENDENT_AUDIT_OBJECT_PIN)
    c42_attacks = c42_audit.get("attacks")
    need(c42_audit.get("schema") ==
             "cm2.round306c42.d02-singleton-wall-endpoint-owner-closure.independent-audit.v1" and
         c42_audit.get("status") ==
             "PASS_INDEPENDENT_C42_P391_OWNER_CLOSURE_AUDIT__54_OF_54_ATTACKS_FAIL_CLOSED" and
         c42_audit.get("candidate_path") ==
             ".cm2-runtime/candidates/" + C42_CANDIDATE_TOKEN and
         c42_audit.get("candidate_object_sha256") == C42_RESULT_OBJECT_PIN and
         c42_audit.get("execution_receipt_object_sha256") ==
             C42_EXECUTION_RECEIPT_OBJECT_PIN and
         c42_audit.get("root_manifest_sha256") == C42_C53_PINS["C42_manifest"] and
         c42_audit.get("authority_pointer_installed") is False and
         c42_audit.get("producer_output_is_authority") is False and
         isinstance(c42_attacks, dict) and len(c42_attacks) == 54 and
         all(type(value) is bool and value for value in c42_attacks.values()),
         "C42 Kraft:independent audit exact 54/54 and nonauthority chain")

    c42_installation = strict_json(c42_installation_raw, "C42 installation receipt")
    installation_body = copy.deepcopy(c42_installation)
    installation_claim = installation_body.pop("installation_receipt_object_sha256", None)
    authority_contract = c42_installation.get("authority_contract")
    prepared_pointers = c42_installation.get("prepared_pointer_records")
    bindings = c42_installation.get("bindings")
    binding_objects = bindings.get("objects", {}) if isinstance(bindings, dict) else {}
    binding_files = bindings.get("files", {}) if isinstance(bindings, dict) else {}
    need(set(c42_installation) == {
             "InvocationID", "authority_contract", "bindings", "filesystem_policy",
             "installation_receipt_object_sha256", "installer", "post_install_census",
             "prepared_pointer_records", "release_id", "schema", "status"} and
         installation_claim == C42_INSTALLATION_RECEIPT_OBJECT_PIN and
         installation_claim == digest(installation_body) and
         c42_installation.get("schema") ==
             "cm2.round306c42.f1-authority-installation-receipt.v1" and
         c42_installation.get("status") ==
             "PREPARED_C42_F1_AUTHORITY_RECEIPT__POINTERS_AND_SEAL_PENDING" and
         c42_installation.get("release_id") == C42_INSTALLATION_RELEASE and
         authority_contract == {
             "audit_pointer_path": ".cm2-runtime/c42-current-audit-token",
             "audit_pointer_sha256": C42_C53_PINS["C42_audit_token"],
             "authority_commit_point": "authority_seal_RENAME_NOREPLACE",
             "candidate_pointer_path": ".cm2-runtime/c42-current-token",
             "candidate_pointer_sha256": C42_C53_PINS["C42_candidate_token"],
             "exact_prefix_recovery_only": True,
             "pointers_before_seal_have_formal_authority": False,
             "publication_order": ["receipt", "candidate_pointer", "audit_pointer",
                                   "authority_seal"],
             "receipt_path": C42_INSTALLATION_RECEIPT_REL,
             "seal_path": ".cm2-runtime/c42-current-authority-seal"} and
         prepared_pointers == {
             "audit": {"file_sha256": C42_C53_PINS["C42_audit_token"],
                       "path": ".cm2-runtime/c42-current-audit-token",
                       "token": C42_AUDIT_TOKEN},
             "candidate": {"file_sha256": C42_C53_PINS["C42_candidate_token"],
                           "path": ".cm2-runtime/c42-current-token",
                           "token": C42_CANDIDATE_TOKEN}} and
         binding_objects.get("c42_candidate_object_sha256") == C42_RESULT_OBJECT_PIN and
         binding_objects.get("c42_execution_receipt_object_sha256") ==
             C42_EXECUTION_RECEIPT_OBJECT_PIN and
         binding_objects.get("c42_independent_audit_object_sha256") ==
             C42_INDEPENDENT_AUDIT_OBJECT_PIN and
         binding_files.get("c42_result", {}).get("path") ==
             str(C42_RESULT_PATH.relative_to(ROOT)) and
         binding_files.get("c42_result", {}).get("file_sha256") == C42_C53_PINS["C42_result"] and
         binding_files.get("c42_manifest", {}).get("path") ==
             str(C42_MANIFEST_PATH.relative_to(ROOT)) and
         binding_files.get("c42_manifest", {}).get("file_sha256") ==
             C42_C53_PINS["C42_manifest"] and
         binding_files.get("c42_independent_audit", {}).get("path") ==
             str(C42_INDEPENDENT_AUDIT_PATH.relative_to(ROOT)) and
         binding_files.get("c42_independent_audit", {}).get("file_sha256") ==
             C42_C53_PINS["C42_independent_audit"],
         "C42 Kraft:installation receipt exact object/pointers/audit chain")

    c42_seal = strict_json(seal_raw, "C42 installed authority seal")
    seal_body = copy.deepcopy(c42_seal)
    seal_claim = seal_body.pop("authority_seal_object_sha256", None)
    need(set(c42_seal) == {
             "audit_pointer_sha256", "audit_token", "authority_seal_object_sha256",
             "candidate_object_sha256", "candidate_pointer_sha256", "candidate_token",
             "formal_census_after_commit", "independent_audit_object_sha256",
             "installer_source_sha256", "receipt_file_sha256", "receipt_object_sha256",
             "receipt_path", "release_id", "schema", "semantic_commit", "status"} and
         seal_claim == C42_SEAL_OBJECT_PIN and seal_claim == digest(seal_body) and
         c42_seal.get("candidate_object_sha256") == C42_RESULT_OBJECT_PIN and
         c42_seal.get("candidate_token") == C42_CANDIDATE_TOKEN and
         c42_seal.get("candidate_pointer_sha256") == C42_C53_PINS["C42_candidate_token"] and
         c42_seal.get("audit_token") == C42_AUDIT_TOKEN and
         c42_seal.get("audit_pointer_sha256") == C42_C53_PINS["C42_audit_token"] and
         c42_seal.get("independent_audit_object_sha256") ==
             C42_INDEPENDENT_AUDIT_OBJECT_PIN and
         c42_seal.get("receipt_path") == C42_INSTALLATION_RECEIPT_REL and
         c42_seal.get("receipt_file_sha256") == C42_C53_PINS["C42_installation_receipt"] and
         c42_seal.get("receipt_object_sha256") == C42_INSTALLATION_RECEIPT_OBJECT_PIN and
         c42_seal.get("release_id") == C42_INSTALLATION_RELEASE and
         c42_seal.get("semantic_commit", {}).get("this_seal_is_required") is True and
         c42_seal.get("semantic_commit", {}).get(
             "compatibility_pointers_without_this_seal_are_not_authority") is True and
         str(c42_seal.get("status", "")).startswith("COMMITTED_C42"),
         "C42 Kraft:full installed authority seal/audit/receipt/token closure")

    audit = strict_json(audit_raw, "C53 independent audit")
    verify_object(audit, "C53 independent audit", C53_AUDIT_OBJECT_PIN)
    derivation = audit.get("post_seal_promotion_derivation")
    need(isinstance(derivation, dict), "C53 Kraft:promotion derivation")
    derivation_body = copy.deepcopy(derivation)
    derivation_claim = derivation_body.pop("promotion_derivation_object_sha256", None)
    need(isinstance(derivation_claim, str) and derivation_claim == digest(derivation_body) and
         derivation.get("parent_projection_count") == EXPECTED_PAIRS and
         derivation.get("C42_formal_authority_seal_object_sha256") == C42_SEAL_OBJECT_PIN and
         derivation.get("D02_gate_credit") == 0,
         "C53 Kraft:derivation closure")
    projections = derivation.get("parent_projections")
    need(isinstance(projections, list) and len(projections) == EXPECTED_PAIRS,
         "C53 Kraft:exact 862 projections")
    projection_by_pair = one_index(projections, "pair_index", "C53 Kraft")
    need(set(projection_by_pair) == set(range(EXPECTED_PAIRS)), "C53 Kraft:dense pair index")
    projection_sequence: list[str] = []
    for pair_index in range(EXPECTED_PAIRS):
        projection = projection_by_pair[pair_index]
        body = copy.deepcopy(projection)
        claim = body.pop("projection_object_sha256", None)
        need(isinstance(claim, str) and claim == digest(body) and
             projection.get("C42_parent_row_sha256") == c42_by_pair[pair_index]["row_sha256"] and
             projection.get("D02_gate_credit") == 0,
             "C53 Kraft:itemwise C42 projection join")
        projection_sequence.append(claim)
    need(_line_sequence_sha256(projection_sequence) == C55B_C53_PAIR_INDEX_SEQUENCE_PIN and
         derivation.get("post_seal_862_parent_projection_sequence_sha256") ==
             C55B_C53_PAIR_INDEX_SEQUENCE_PIN,
         "C53 Kraft:projection sequence")

    head = strict_json(head_raw, "C53 installed global head")
    head_body = copy.deepcopy(head)
    head_claim = head_body.pop("authority_seal_object_sha256", None)
    need(head_claim == C53_HEAD_OBJECT_PIN and head_claim == digest(head_body) and
         head.get("independent_audit_object_sha256") == C53_AUDIT_OBJECT_PIN and
         head.get("post_seal_effective_checkpoint_object_sha256") == UPSTREAM_CHECKPOINT_OBJECT_PIN and
         head.get("formal_scope", {}).get("D02_gate_credit") == 0 and
         head.get("semantic_commit", {}).get("this_predecessor_keyed_global_head_is_only_semantic_commit") is True,
         "C53 Kraft:installed global head closure")

    c55b_pairs: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for row in cell_rows:
        c55b_pairs[row["pair_index"]].append(row)
    need(set(c55b_pairs) == set(range(EXPECTED_PAIRS)) and
         all(len(rows) == 2 for rows in c55b_pairs.values()), "Kraft:C55B exact pair crosswalk")
    for pair_index in range(EXPECTED_PAIRS):
        need({row["C42_parent_row_sha256"] for row in c55b_pairs[pair_index]} ==
                 {c42_by_pair[pair_index]["row_sha256"]} and
             {row["C53_parent_projection_object_sha256"] for row in c55b_pairs[pair_index]} ==
                 {projection_by_pair[pair_index]["projection_object_sha256"]},
             "Kraft:C42-C53-C55B itemwise hash join")
    for guard in c42_held_directories:
        guard.terminal_replay()
    return {
        "pair_count": EXPECTED_PAIRS,
        "C42_parent_row_hash_sequence_sha256": C55B_C42_PAIR_INDEX_SEQUENCE_PIN,
        "C53_projection_hash_sequence_sha256": C55B_C53_PAIR_INDEX_SEQUENCE_PIN,
        "C42_result_object_sha256": C42_RESULT_OBJECT_PIN,
        "C42_execution_receipt_object_sha256": C42_EXECUTION_RECEIPT_OBJECT_PIN,
        "C42_independent_audit_object_sha256": C42_INDEPENDENT_AUDIT_OBJECT_PIN,
        "C42_independent_audit_fail_closed_attack_count": 54,
        "C42_installation_receipt_object_sha256": C42_INSTALLATION_RECEIPT_OBJECT_PIN,
        "C42_candidate_token": C42_CANDIDATE_TOKEN,
        "C42_candidate_token_file_sha256": C42_C53_PINS["C42_candidate_token"],
        "C42_audit_token": C42_AUDIT_TOKEN,
        "C42_audit_token_file_sha256": C42_C53_PINS["C42_audit_token"],
        "C42_authority_seal_object_sha256": C42_SEAL_OBJECT_PIN,
        "C53_independent_audit_object_sha256": C53_AUDIT_OBJECT_PIN,
        "C53_global_head_object_sha256": C53_HEAD_OBJECT_PIN,
        "C72_prefix_Kraft_boolean_role": "REDUNDANT_ONLY_NOT_AUTHORITY",
        "installed_authority_and_projection_fixed_input_count": 10,
        "installed_authority_seal_binds_audit_receipt_and_both_tokens": True,
        "C42_candidate_directory_exact_member_count": 9,
        "C42_manifest_exact_member_count": 8,
        "C42_all_manifest_members_hash_replayed_and_terminal_rescanned": True,
        "all_862_exact_parent_Kraft_one": True,
        "all_D02_gate_credit_zero": True,
        "C42_rows_by_pair": c42_by_pair,
        "C53_projections_by_pair": projection_by_pair,
        "held_direct_inputs": held_inputs,
        "held_direct_input_identity_count": len(held_inputs),
        "C42_candidate_observed_physical_policy": {
            "directory_expected_mode": "0755",
            "directory_expected_nlink": 2,
            "member_expected_mode": "0664",
            "member_expected_nlink": 1,
            "live_dev_ino_mount_or_timestamp_persisted": False,
            "immutable_or_read_only_claimed": False,
        },
        "C42_independent_audit_observed_physical_policy": {
            "directory_expected_mode": "0700",
            "directory_expected_nlink": 2,
            "exact_member_count": 1,
            "member_expected_mode": "0600",
            "member_expected_nlink": 1,
            "live_dev_ino_mount_or_timestamp_persisted": False,
            "immutable_or_read_only_claimed": False,
        },
        "C42_installation_receipt_observed_physical_policy": {
            "directory_expected_mode": "0500",
            "directory_expected_nlink": 2,
            "exact_member_count": 1,
            "member_expected_mode": "0444",
            "member_expected_nlink": 1,
            "live_dev_ino_mount_or_timestamp_persisted": False,
            "immutable_or_read_only_claimed": False,
        },
        "C42_candidate_universe": sorted(c42_candidate_universe),
        "C42_candidate_guard": c42_candidate_guard,
        "C42_held_directories": c42_held_directories,
    }


def one_index(rows: Iterable[dict[str, Any]], key: str, label: str) -> dict[Any, dict[str, Any]]:
    out: dict[Any, dict[str, Any]] = {}
    for row in rows:
        value = row.get(key)
        need(value not in out, label + ":duplicate:" + str(value))
        out[value] = row
    return out


def validate_static_authorities(static_trust: dict[str, Any]) -> dict[str, Any]:
    held = static_trust["by_path"]
    contract_raw = held[CONTRACT].raw
    schema_raw = held[CLOSED_SCHEMA].raw
    rejection_raw = static_trust[
        "v8_published_by_path"][V7_OFFICIAL_REJECTION].raw
    contract = strict_json(contract_raw, "C79g contract")
    verify_object(contract, "C79g contract", CONTRACT_OBJECT_PIN)
    contract_witness = contract.get("v10_colon_prefix_witness", {})
    need(isinstance(contract_witness, dict),
         "contract v10 colon-prefix witness object")
    verify_object(
        contract_witness, "contract v10 colon-prefix witness",
        V10_COLON_PREFIX_WITNESS_OBJECT_PIN)
    need(set(contract) == {
             "schema", "status", "effective_checkpoint_object_sha256",
             "purpose", "append_only_predecessor_v3",
             "rejected_unpublished_predecessor_v4",
             "published_then_officially_rejected_predecessor_v5",
             "published_then_officially_rejected_predecessor_v6",
             "published_then_officially_rejected_predecessor_v7",
             "published_then_officially_rejected_predecessor_v8",
             "published_then_officially_rejected_predecessor_v9",
             "published_then_officially_rejected_predecessor_v10",
             "published_then_officially_rejected_predecessor_v11",
             "published_then_officially_rejected_predecessor_v12",
             "rejected_prepublication_v13_supersession_receipt",
             "v10_colon_prefix_witness",
             "v11_dual_validator_divergence_incident",
             "exact_publication_paths", "candidate_and_verification_protocol",
             "completion_protocol", "full10_direct_prefix_Kraft_identity",
             "upstream_branch_held_input_protocol",
             "independent_authority_consumer_protocol",
             "composite_authority_predicate", "no_later_rejection_protocol",
             "credit_boundary", "static_freeze_protocol_requirements",
             "v16r2_bundle", "object_sha256",
         } and
         contract.get("schema") ==
             "cm2.round306c79g.true-global-no-producer-consumer.v16r2r62.contract" and
         contract.get("effective_checkpoint_object_sha256") == UPSTREAM_CHECKPOINT_OBJECT_PIN and
         contract.get("status") ==
             "STATIC_CONTRACT_BYTES_FINAL__COLD_FREEZE_PENDING__RUNTIME_NOT_AUTHORIZED" and
         contract.get("v16r2_bundle", {}).get(
             "independent_verifier_assembler_authority_consumer", {}).get("path") ==
             "deliverables/cm2_round306c79g_true_global_no_producer_consumer_"
             "independent_verifier_assembler_authority_consumer_v16r2r63ah_repair_semantic_source.py" and
         contract.get("v16r2_bundle", {}).get("closed_schema_validator_policy") == {
             "unsupported_validation_keyword_action": "FAIL_CLOSED",
             "runtime_validator_walks_complete_schema_keyword_universe": True,
             "oneOf_keyword_allowed": False,
             "file_and_object_pin_definitions_are_split_closed_types": True,
             "all_closed_object_required_sets_equal_property_sets": True,
             "static_audit_must_pin_actual_and_supported_keyword_universes": True,
         } and
         contract.get(
             "published_then_officially_rejected_predecessor_v8") ==
             _expected_published_then_rejected_v8_proof(
                 V8_ROLLOUT_CONTROL_FLOW_INCIDENT) and
         contract.get(
             "published_then_officially_rejected_predecessor_v10") ==
             _expected_published_then_rejected_v10_proof() and
         contract.get(
             "published_then_officially_rejected_predecessor_v11") ==
             _expected_published_then_rejected_v11_proof() and
         contract.get(
             "published_then_officially_rejected_predecessor_v12") ==
             _expected_published_then_rejected_v12_proof() and
         contract.get("rejected_prepublication_v13_supersession_receipt") ==
             static_trust[
                 "rejected_prepublication_v13_supersession_receipt"] and
         tuple(contract_witness) == V10_COLON_PREFIX_WITNESS_KEY_ORDER and
         contract.get("v11_dual_validator_divergence_incident") ==
             V11_DUAL_VALIDATOR_DIVERGENCE_INCIDENT and
         contract.get("composite_authority_predicate", {}).get("seal_only_GO_allowed") is False and
         contract.get("credit_boundary", {}).get("standalone_authority_seal_credit") == 0,
         "v16r2 frozen contract checkpoint/composite-only boundary")
    closed = strict_json(schema_raw, "C79g closed schemas")
    definitions = closed.get("$defs", {})
    root_properties = definitions.get(
        "coldLaunchedCommittedAuthority", {}).get("properties", {})
    inner_properties = definitions.get("innerComposite", {}).get("properties", {})
    seal_properties = definitions.get("authoritySeal", {}).get("properties", {})
    need(closed.get("$ref") == "#/$defs/coldLaunchedCommittedAuthority" and
         isinstance(definitions, dict) and
         root_properties.get("formal_global_closure_credit", {}).get("const") == 1 and
         root_properties.get("D02_unlock", {}).get("const") is True and
         inner_properties.get("formal_global_closure_credit", {}).get("const") == 0 and
         inner_properties.get("D02_unlock", {}).get("const") is False and
         inner_properties.get("cold_launcher_required", {}).get("const") is True and
         seal_properties.get("standalone_seal_credit", {}).get("$ref") ==
             "#/$defs/zeroCredit" and
         definitions.get("standaloneOuter", {}).get("properties", {}).get(
             "standalone_credit", {}).get("$ref") == "#/$defs/zeroCredit",
         "append-only v16r2 cold root, zero-credit inner, and persisted zero boundary")
    rejection = strict_json(rejection_raw, "C79g official v7 later rejection")
    verify_object(rejection, "C79g official v7 later rejection",
                  V7_OFFICIAL_REJECTION_OBJECT_PIN)
    need(rejection.get("schema") ==
             "cm2.round306c79g.true-global-no-producer-consumer.v7.later-rejection" and
         rejection.get("status") ==
             "PERMANENT_FAIL_CLOSED_REJECTION__ZERO_CREDIT" and
         rejection.get("rejection_reason") ==
             "ORPHANED_OR_INCOMPLETE_C79G_V7_SURFACE" and
         rejection.get("effective_checkpoint_object_sha256") ==
             UPSTREAM_CHECKPOINT_OBJECT_PIN and
         rejection.get("cold_outer_file_sha256") ==
             V7_PUBLISHED_EXACT10_PINS[9][1] and
         rejection.get("cold_outer_object_sha256") ==
             V7_PUBLISHED_EXACT10_PINS[9][2] and
         rejection.get("formal_global_closure_credit") == 0 and
         rejection.get("D02_unlock") is False and
         rejection.get("D02_started") is False and
         rejection.get("standalone_authority") is False and
         rejection.get("overwrite_delete_or_reuse_allowed") is False and
         rejection.get("target_exact_path") ==
             str(V7_OFFICIAL_REJECTION.relative_to(ROOT)),
         "exact official v7 permanent later rejection semantics")

    fixed_historical_guards: list[HeldPinnedInput] = []
    c55a_raw, family_guards = hold_pinned_historical(
        C55A_PATHS, C55A_PINS, HISTORICAL_FIXED_EXPECTED_MODES, "C55A")
    fixed_historical_guards.extend(family_guards)
    c55a = {key: strict_json(c55a_raw[key], "C55A:" + key)
            for key in ("leaf_ledger", "result", "verification")}
    for key in c55a:
        verify_object(c55a[key], "C55A:" + key, C55A_OBJECTS[key])
    need(c55a["result"].get("bnb", {}).get("unresolved_zero") is False and
         c55a["result"].get("bnb", {}).get("remaining_unresolved_leaf_count") == EXPECTED_OVERLAY and
         c55a["leaf_ledger"].get("census", {}).get("UNRESOLVED_R1648_CONTINUATION") == EXPECTED_OVERLAY,
         "C55A predecessor unresolved census")

    c55b_raw, family_guards = hold_pinned_historical(
        C55B_PATHS, C55B_PINS, HISTORICAL_FIXED_EXPECTED_MODES, "C55B")
    fixed_historical_guards.extend(family_guards)
    c55b_objects = {key: strict_json(c55b_raw[key], "C55B:" + key)
                    for key in ("result", "verification", "self_test")}
    for key in c55b_objects:
        verify_object(c55b_objects[key], "C55B:" + key, C55B_OBJECTS[key])
    need(c55b_objects["result"].get("global_closure_proved") is False and
         c55b_objects["result"].get("unresolved_zero") is False,
         "C55B structure-only boundary")
    need(c55b_objects["self_test"].get("status", "").startswith("PASS_16_OF_16"),
         "C55B independent self-test")

    c72_raw, family_guards = hold_pinned_historical(
        C72G_PATHS, C72G_PINS, HISTORICAL_FIXED_EXPECTED_MODES, "C72g")
    fixed_historical_guards.extend(family_guards)
    c72 = {key: strict_json(c72_raw[key], "C72g:" + key)
           for key in ("contract", "verification", "self_test", "outer", "head")}
    for key in ("contract", "verification", "self_test", "outer"):
        verify_object(c72[key], "C72g:" + key, C72G_OBJECTS[key])
    c72_head_body = copy.deepcopy(c72["head"])
    c72_head_claim = c72_head_body.pop("authority_seal_object_sha256", None)
    need(c72_head_claim == C72G_OBJECTS["head"] and c72_head_claim == digest(c72_head_body),
         "C72g:head authority-seal closure")
    need(c72["contract"].get("effective_checkpoint_object_sha256") == UPSTREAM_CHECKPOINT_OBJECT_PIN,
         "C72g head binding")
    need(c72["verification"].get("status", "").startswith("PASS_FROZEN_NO_PRODUCER") and
         c72["verification"].get("public_global_census", {}).get("UNRESOLVED_R1648_CONTINUATION") == EXPECTED_OVERLAY and
         c72["verification"].get("public_global_unresolved_zero") is False and
         c72["verification"].get("formal_credit") == 0,
         "C72g structural authority only")
    need(c72["self_test"].get("status", "").startswith("PASS_39_OF_39"),
         "C72g attacks")
    return {
        "contract": contract,
        "v6_rejection": rejection,
        "C55A_raw": c55a_raw,
        "C55A": c55a,
        "C55B_raw": c55b_raw,
        "C55B": c55b_objects,
        "C72g_raw": c72_raw,
        "C72g": c72,
        "fixed_historical_guards": fixed_historical_guards,
    }


def validate_c78l() -> dict[str, Any]:
    base_names = set(C78L_NAMES.values())
    need(len(base_names) == 10, "C78l exact10 base universe declaration")
    directory_a_guard = HeldDirectory(
        C78L_A, base_names, C78L_HISTORICAL_DIRECTORY_EXPECTED_MODE, 2,
        "C78l base A")
    directory_b_guard = HeldDirectory(
        C78L_B, base_names, C78L_HISTORICAL_DIRECTORY_EXPECTED_MODE, 2,
        "C78l base B")
    completion_names = set(C78L_COMPLETION_NAMES.values())
    need(len(completion_names) == 3, "C78l exact3 completion universe declaration")
    completion_directory_guard = HeldDirectory(
        C78L_COMPLETION, completion_names,
        C78L_HISTORICAL_DIRECTORY_EXPECTED_MODE, 2, "C78l completion")
    need(len({directory_a_guard.identity, directory_b_guard.identity,
              completion_directory_guard.identity}) == 3,
         "C78l base/completion directory identities distinct")
    held_by_path: dict[Path, HeldPinnedInput] = {}

    def hold(path: Path, label: str, expected_sha256: str) -> HeldPinnedInput:
        need(path not in held_by_path, "C78l held path unique:" + str(path))
        guard = HeldPinnedInput(
            path, label, C78_HISTORICAL_MEMBER_EXPECTED_MODE,
            expected_sha256)
        held_by_path[path] = guard
        return guard

    raw: dict[str, bytes] = {}
    for key, name in C78L_NAMES.items():
        left_guard = hold(C78L_A / name, "C78l A:" + key, C78L_PINS[key])
        right_guard = hold(C78L_B / name, "C78l B:" + key, C78L_PINS[key])
        need(left_guard.raw == right_guard.raw and
             left_guard.identity != right_guard.identity,
             "C78l dual byte identity and corresponding inode separation:" + key)
        raw[key] = left_guard.raw
    verification_a_guard = hold(
        C78L_VERIFY_A, "C78l verification A", C78L_VERIFY_FILE_PIN)
    verification_b_guard = hold(
        C78L_VERIFY_B, "C78l verification B", C78L_VERIFY_FILE_PIN)
    verification_a = verification_a_guard.raw
    verification_b = verification_b_guard.raw
    need(verification_a == verification_b, "C78l verification A/B bytes")
    verification = strict_json(verification_a, "C78l verification")
    verify_object(verification, "C78l verification", C78L_VERIFY_OBJECT_PIN)
    need(verification.get("status", "").startswith("PASS_INDEPENDENT_C78L") and
         verification.get("self_test", {}).get("attack_count") == 52 and
         all(value == "FAIL_CLOSED" for value in
             verification.get("self_test", {}).get("attacks", {}).values()),
         "C78l independent verification")
    completion_raw: dict[str, bytes] = {}
    for key, name in C78L_COMPLETION_NAMES.items():
        completion_raw[key] = hold(
            C78L_COMPLETION / name, "C78l completion:" + key,
            C78L_COMPLETION_PINS[key]).raw
    held_inputs = list(held_by_path.values())
    need(len(held_inputs) == 25 and
         len({guard.identity for guard in held_inputs}) == 25 and
         len({guard.mount_id for guard in held_inputs}) == 1,
         "C78l exact10x2 plus verification2 plus completion3 identities globally unique on one mount")
    receipt = strict_json(completion_raw["receipt"], "C78l completion")
    outer = strict_json(completion_raw["outer"], "C78l completion outer")
    verify_object(receipt, "C78l completion", C78L_COMPLETION_OBJECT_PIN)
    verify_object(outer, "C78l completion outer", C78L_COMPLETION_OUTER_OBJECT_PIN)
    need(receipt.get("dual_build_byte_identical") is True and
         receipt.get("verification_A_B_byte_identical") is True and
         receipt.get("canonical_pointer_or_seal_written") is False,
         "C78l final completion semantics")
    result = strict_json(raw["result"], "C78l result")
    verify_object(result, "C78l result", C78L_RESULT_OBJECT_PIN)
    need(result.get("branch_unresolved") == 0 and
         result.get("public_global_unresolved_after_branch") == EXPECTED_SINGLETON and
         result.get("public_global_unresolved_zero") is False and
         result.get("candidate_is_authority") is False,
         "C78l branch boundary")
    base_manifest_entries = parse_manifest_ordered(raw["manifest"], "C78l manifest")
    base_manifest_order = ("lock", "cells", "pairs", "report", "result", "registry",
                           "tasks", "sides")
    need(base_manifest_entries == [
        {"file_sha256": C78L_PINS[key], "entry_name": C78L_NAMES[key]}
        for key in base_manifest_order
    ], "C78l exact ordered base8 manifest")
    completion_manifest_entries = parse_manifest_ordered(
        completion_raw["manifest"], "C78l completion manifest")
    need(completion_manifest_entries == [{
        "file_sha256": C78L_COMPLETION_PINS["receipt"],
        "entry_name": C78L_COMPLETION_NAMES["receipt"],
    }], "C78l exact ordered completion manifest contains receipt only")
    need(outer.get("manifest_sha256") == C78L_COMPLETION_PINS["manifest"] and
         outer.get("completion_object_sha256") == C78L_COMPLETION_OBJECT_PIN and
         outer.get("outer_receipt_published_last") is True and
         outer.get("terminal_byte_replay_required_after_outer_receipt") is True and
         outer.get("formal_credit") == 0 and outer.get("D02_gate_credit") == 0,
         "C78l completion outer-last zero-credit closure")
    for directory in (C78L_A, C78L_B):
        base8_mtime = max(
            held_by_path[directory / C78L_NAMES[key]].before.st_mtime_ns
            for key in base_manifest_order)
        side_verify = (verification_a_guard if directory == C78L_A
                       else verification_b_guard)
        need(base8_mtime <
             held_by_path[directory / C78L_NAMES["manifest"]].before.st_mtime_ns <
             held_by_path[directory / C78L_NAMES["outer"]].before.st_mtime_ns <
             side_verify.before.st_mtime_ns,
             "C78l held base8 then manifest then outer then side verification chronology")
    completion_receipt_guard = held_by_path[
        C78L_COMPLETION / C78L_COMPLETION_NAMES["receipt"]]
    completion_manifest_guard = held_by_path[
        C78L_COMPLETION / C78L_COMPLETION_NAMES["manifest"]]
    completion_outer_guard = held_by_path[
        C78L_COMPLETION / C78L_COMPLETION_NAMES["outer"]]
    need(max(verification_a_guard.before.st_mtime_ns,
             verification_b_guard.before.st_mtime_ns) <
         completion_receipt_guard.before.st_mtime_ns <
         completion_manifest_guard.before.st_mtime_ns <
         completion_outer_guard.before.st_mtime_ns,
         "C78l held dual verification then completion receipt manifest outer chronology")
    for guard in held_inputs:
        guard.terminal_replay()
    directory_a_guard.terminal_replay()
    directory_b_guard.terminal_replay()
    completion_directory_guard.terminal_replay()
    return {
        "raw": raw,
        "verification_raw": verification_a,
        "verification": verification,
        "completion_raw": completion_raw,
        "completion": receipt,
        "result": result,
        "cells": gzip_rows(raw["cells"], "C78l public cells"),
        "pairs": gzip_rows(raw["pairs"], "C78l reflection pairs"),
        "held_inputs": held_inputs,
        "held_directories": [directory_a_guard, directory_b_guard,
                             completion_directory_guard],
    }


def validate_c78s() -> dict[str, Any]:
    a = rooted(str(C78S_FINAL["build_A_directory"]))
    b = rooted(str(C78S_FINAL["build_B_directory"]))
    pins = C78S_FINAL["pins"]
    need(isinstance(pins, dict), "C78s pins mapping")
    verification_a_path = rooted(str(C78S_FINAL["verification_A_path"]))
    verification_b_path = rooted(str(C78S_FINAL["verification_B_path"]))
    final_manifest_a_path = rooted(str(C78S_FINAL["final_manifest_A_path"]))
    final_manifest_b_path = rooted(str(C78S_FINAL["final_manifest_B_path"]))
    final_outer_a_path = rooted(str(C78S_FINAL["final_outer_A_path"]))
    final_outer_b_path = rooted(str(C78S_FINAL["final_outer_B_path"]))
    expected_stage_names = set(C78S_NAMES.values()) | {
        verification_a_path.name, final_manifest_a_path.name, final_outer_a_path.name,
    }
    need(len(expected_stage_names) == 13, "C78s exact 13-member stage universe declaration")
    directory_a_guard = HeldDirectory(
        a, expected_stage_names, C78S_HISTORICAL_DIRECTORY_EXPECTED_MODE, 2,
        "C78s stage A")
    directory_b_guard = HeldDirectory(
        b, expected_stage_names, C78S_HISTORICAL_DIRECTORY_EXPECTED_MODE, 2,
        "C78s stage B")
    need(directory_a_guard.identity != directory_b_guard.identity,
         "C78s isolated stage directories distinct")
    held_by_path: dict[Path, HeldPinnedInput] = {}

    def hold(path: Path, label: str, expected_sha256: str) -> HeldPinnedInput:
        need(path not in held_by_path, "C78s held path unique:" + str(path))
        guard = HeldPinnedInput(
            path, label, C78_HISTORICAL_MEMBER_EXPECTED_MODE,
            expected_sha256)
        held_by_path[path] = guard
        return guard

    raw: dict[str, bytes] = {}
    stage_member_raw: dict[str, bytes] = {}
    for key, name in C78S_NAMES.items():
        left_guard = hold(a / name, "C78s A:" + key, pins[key])
        right_guard = hold(b / name, "C78s B:" + key, pins[key])
        left = left_guard.raw
        right = right_guard.raw
        need(left == right,
             "C78s pinned dual base member:" + key)
        need(left_guard.identity != right_guard.identity,
             "C78s base member inode separation:" + key)
        raw[key] = left
        stage_member_raw[name] = left
    verify_a_guard = hold(verification_a_path, "C78s verification A",
                          str(C78S_FINAL["verification_A_file_sha256"]))
    verify_b_guard = hold(verification_b_path, "C78s verification B",
                          str(C78S_FINAL["verification_B_file_sha256"]))
    verify_a_raw = verify_a_guard.raw
    verify_b_raw = verify_b_guard.raw
    need(verify_a_guard.identity != verify_b_guard.identity,
         "C78s verification pins/mode/inode separation")
    need(verify_a_raw == verify_b_raw, "C78s verification A/B bytes")
    verify_a = strict_json(verify_a_raw, "C78s verification A")
    verify_b = strict_json(verify_b_raw, "C78s verification B")
    verify_object(verify_a, "C78s verification A",
                  str(C78S_FINAL["verification_A_object_sha256"]))
    verify_object(verify_b, "C78s verification B",
                  str(C78S_FINAL["verification_B_object_sha256"]))
    need(verify_a.get("object_sha256") == verify_b.get("object_sha256") ==
         C78S_FINAL["verification_A_object_sha256"] ==
         C78S_FINAL["verification_B_object_sha256"],
         "C78s verification A/B object pins agree")
    attacks = verify_a.get("coherent_attacks", {})
    attack_count = attacks.get("attack_count")
    attack_names = attacks.get("names")
    need(verify_a == verify_b and
         verify_a.get("candidate_base_bundle", {}).get("stage_a_stage_b_bytes_identical") is True and
         verify_a.get("candidate_base_bundle", {}).get("stage_a_stage_b_inodes_distinct") is True and
         verify_a.get("candidate_base_bundle", {}).get("result_file_sha256") == pins["result"] and
         verify_a.get("candidate_base_bundle", {}).get("result_object_sha256") == C78S_FINAL["result_object_sha256"] and
         verify_a.get("verifier_file_sha256") == C78S_FINAL["verifier_source_file_sha256"] and
         attack_count == 128 and
         attacks.get("rejected") == attack_count and
         isinstance(attack_names, list) and len(attack_names) == attack_count and
         len(set(attack_names)) == attack_count,
         "C78s independent dual verification")

    final_manifest_a_guard = hold(final_manifest_a_path, "C78s final manifest A",
                                  str(C78S_FINAL["final_manifest_file_sha256"]))
    final_manifest_b_guard = hold(final_manifest_b_path, "C78s final manifest B",
                                  str(C78S_FINAL["final_manifest_file_sha256"]))
    final_outer_a_guard = hold(final_outer_a_path, "C78s final outer A",
                               str(C78S_FINAL["final_outer_file_sha256"]))
    final_outer_b_guard = hold(final_outer_b_path, "C78s final outer B",
                               str(C78S_FINAL["final_outer_file_sha256"]))
    final_manifest_a_raw = final_manifest_a_guard.raw
    final_manifest_b_raw = final_manifest_b_guard.raw
    final_outer_a_raw = final_outer_a_guard.raw
    final_outer_b_raw = final_outer_b_guard.raw
    need(final_manifest_a_guard.identity != final_manifest_b_guard.identity and
         final_outer_a_guard.identity != final_outer_b_guard.identity,
         "C78s final member pins/mode/inode separation")
    need(verification_a_path.parent == a and verification_b_path.parent == b and
         final_manifest_a_path.parent == a and final_manifest_b_path.parent == b and
         final_outer_a_path.parent == a and final_outer_b_path.parent == b,
         "C78s all final members remain inside their isolated stages")
    need(final_manifest_a_raw == final_manifest_b_raw and final_outer_a_raw == final_outer_b_raw,
         "C78s final stage A/B bytes")
    final_outer = strict_json(final_outer_a_raw, "C78s final outer closure receipt")
    verify_object(final_outer, "C78s final outer closure receipt",
                  str(C78S_FINAL["final_outer_object_sha256"]))
    need(final_outer.get("verification_file_sha256") == C78S_FINAL["verification_A_file_sha256"] and
         final_outer.get("verification_object_sha256") == C78S_FINAL["verification_A_object_sha256"] and
         final_outer.get("final_manifest_file_sha256") == C78S_FINAL["final_manifest_file_sha256"] and
         final_outer.get("all_final_stage_bytes_identical") is True and
         final_outer.get("all_final_members_terminal_byte_replayed_in_both_stages") is True and
         final_outer.get("terminal_byte_replay_member_count_per_stage") == 13,
         "C78s 13-member final closure")
    base_manifest_entries = parse_manifest_ordered(raw["manifest"], "C78s base manifest")
    expected_base_entries = [
        {"file_sha256": pins[key], "entry_name": C78S_NAMES[key]}
        for key in ("lock", "children", "sources", "pairs", "cells", "projection", "result", "report")
    ]
    need(base_manifest_entries == expected_base_entries,
         "C78s exact ordered base manifest universe")
    final_manifest_entries = parse_manifest_ordered(final_manifest_a_raw, "C78s final manifest")
    expected_final_entries = [
        {"file_sha256": pins[key], "entry_name": C78S_NAMES[key]}
        for key in C78S_NAMES
    ] + [{"file_sha256": C78S_FINAL["verification_A_file_sha256"],
          "entry_name": verification_a_path.name}]
    need(final_manifest_entries == expected_final_entries and
         final_outer.get("final_manifest_member_count") == 11 and
         final_outer.get("final_manifest_order") == [item["entry_name"] for item in expected_final_entries],
         "C78s exact ordered 11-entry final manifest universe")
    for directory, verification_path, final_manifest_path, final_outer_path in (
        (a, verification_a_path, final_manifest_a_path, final_outer_a_path),
        (b, verification_b_path, final_manifest_b_path, final_outer_b_path),
    ):
        base_data_mtime = max(held_by_path[directory / C78S_NAMES[key]].before.st_mtime_ns
                              for key in ("lock", "children", "sources", "pairs", "cells",
                                          "projection", "result", "report"))
        need(base_data_mtime <
             held_by_path[directory / C78S_NAMES["manifest"]].before.st_mtime_ns <
             held_by_path[directory / C78S_NAMES["outer"]].before.st_mtime_ns <
             held_by_path[verification_path].before.st_mtime_ns <
             held_by_path[final_manifest_path].before.st_mtime_ns <
             held_by_path[final_outer_path].before.st_mtime_ns,
             "C78s base/verification/final-manifest/final-outer strict mtime order")
    stage_member_raw[verification_a_path.name] = verify_a_raw
    stage_member_raw[final_manifest_a_path.name] = final_manifest_a_raw
    stage_member_raw[final_outer_a_path.name] = final_outer_a_raw
    need(len(stage_member_raw) == 13, "C78s terminal replay member count")
    for name, expected_raw in stage_member_raw.items():
        left_guard = held_by_path[a / name]
        right_guard = held_by_path[b / name]
        left_guard.terminal_replay()
        right_guard.terminal_replay()
        need(left_guard.raw == expected_raw and right_guard.raw == expected_raw,
             "C78s post-final-outer terminal replay:" + name)
    directory_a_guard.terminal_replay()
    directory_b_guard.terminal_replay()

    result = strict_json(raw["result"], "C78s result")
    verify_object(result, "C78s result", str(C78S_FINAL["result_object_sha256"]))
    need(result.get("singleton_branch_unresolved") == 0 and
         result.get("public_global_unresolved_after_branch") == EXPECTED_LARGE and
         result.get("public_global_unresolved_zero") is False and
         result.get("branch_projection_installed_as_canonical_state") is False,
         "C78s branch boundary")
    manifest = parse_manifest(raw["manifest"], "C78s manifest")
    for key in ("lock", "children", "sources", "pairs", "cells", "projection", "result", "report"):
        need(manifest.get(C78S_NAMES[key]) == pins[key], "C78s manifest:" + key)
    return {
        "raw": raw,
        "verification_raw": verify_a_raw,
        "verification": verify_a,
        "completion_raw": {
            "manifest": final_manifest_a_raw,
            "outer": final_outer_a_raw,
        },
        "completion": final_outer,
        "result": result,
        "projection": gzip_rows(raw["projection"], "C78s projection"),
        "pairs": gzip_rows(raw["pairs"], "C78s pairs"),
        "cells": gzip_rows(raw["cells"], "C78s cells"),
        "held_inputs": list(held_by_path.values()),
        "held_directories": [directory_a_guard, directory_b_guard],
    }


def reconstruct(static_trust: dict[str, Any]) -> dict[str, Any]:
    static = validate_static_authorities(static_trust)
    fixed_historical_guards = static.pop("fixed_historical_guards")
    c78l = validate_c78l()
    c78s = validate_c78s()
    held_branch_inputs = [*c78l["held_inputs"], *c78s["held_inputs"]]
    held_branch_directories = [*c78l["held_directories"], *c78s["held_directories"]]
    need(len({guard.identity for guard in held_branch_inputs}) ==
             len(held_branch_inputs) and
         len({guard.identity for guard in held_branch_directories}) ==
             len(held_branch_directories) and
         len({guard.mount_id for guard in
              [*held_branch_inputs, *held_branch_directories]}) == 1,
         "C78l/C78s complete held branch surfaces globally inode-distinct on one mount")

    ledger = static["C55A"]["leaf_ledger"]
    leaves = ledger.get("leaves")
    need(isinstance(leaves, list) and len(leaves) == EXPECTED_UNIVERSE, "C55A 76832 leaves")
    by_cell: dict[str, dict[str, Any]] = {}
    unresolved: set[str] = set()
    baseline: set[str] = set()
    for ordinal, leaf in enumerate(leaves):
        need(isinstance(leaf, dict), "C55A leaf object")
        verify_row(leaf, "C55A leaf")
        need(leaf.get("leaf_ordinal") == ordinal, "C55A leaf order")
        cell_id = leaf.get("cell_id")
        need(isinstance(cell_id, str) and cell_id not in by_cell, "C55A unique cell")
        terminal = leaf.get("terminal_disposition")
        reason = leaf.get("unresolved_reason")
        need((terminal in TERMINALS and reason is None) or
             (terminal is None and isinstance(reason, str) and bool(reason)),
             "C55A terminal/unresolved XOR")
        by_cell[cell_id] = leaf
        (unresolved if terminal is None else baseline).add(cell_id)
    need(len(baseline) == EXPECTED_BASELINE and len(unresolved) == EXPECTED_OVERLAY,
         "C55A exact baseline/overlay partition")

    cell_rows = gzip_rows(static["C55B_raw"]["cells"], "C55B cells")
    edge_rows = gzip_rows(static["C55B_raw"]["edges"], "C55B edges")
    component_rows = gzip_rows(static["C55B_raw"]["components"], "C55B components")
    c55b_topology = validate_c55b_topology(cell_rows, edge_rows, component_rows)
    kraft_chain = validate_c42_c53_kraft(cell_rows)
    c55b_by_cell = one_index(cell_rows, "cell_id", "C55B cells")
    component_by_index = one_index(component_rows, "component_index", "C55B components")
    need(Counter(row["cell_count"] for row in component_rows) == Counter({850: 2, 1: 24}),
         "C55B component sizes")
    pair_cells: dict[int, list[dict[str, Any]]] = defaultdict(list)
    c55b_unresolved: set[str] = set()
    for row in cell_rows:
        cell_id = row["cell_id"]
        need(cell_id in by_cell, "C55B cell in C55A")
        pair_cells[row["pair_index"]].append(row)
        if row["current_effective_disposition"] == "UNRESOLVED_R1648_CONTINUATION":
            c55b_unresolved.add(cell_id)
            need(cell_id in unresolved, "C55B unresolved agrees C55A")
        else:
            need(row["current_effective_disposition"] == "EARLIEST_PREFIX_EXCLUDED" and
                 by_cell[cell_id]["terminal_disposition"] == "EARLIEST_PREFIX_EXCLUDED",
                 "C55B baseline agrees C55A")
        component = component_by_index[row["component_index"]]
        need(component["component_id"] == row["component_id"], "C55B component identity")
    need(c55b_unresolved == unresolved, "C55A/C55B exact unresolved identity")
    need(len(pair_cells) == EXPECTED_PAIRS and
         all(len(rows) == 2 for rows in pair_cells.values()), "C55B 862 reflection pairs")
    for rows in pair_cells.values():
        left, right = rows
        need(left["reflection_partner_cell_id"] == right["cell_id"] and
             right["reflection_partner_cell_id"] == left["cell_id"],
             "C55B reciprocal reflection")

    large_cells = c78l["cells"]
    large_pairs = c78l["pairs"]
    need(len(large_cells) == EXPECTED_LARGE and len(large_pairs) == EXPECTED_LARGE_PAIRS,
         "C78l exact row census")
    large_by_cell = one_index(large_cells, "cell_id", "C78l cells")
    large_pair_by_index = one_index(large_pairs, "pair_index", "C78l pairs")
    singleton_rows = c78s["projection"]
    singleton_pairs = c78s["pairs"]
    need(len(singleton_rows) == EXPECTED_SINGLETON and
         len(singleton_pairs) == EXPECTED_SINGLETON_PAIRS and
         len(c78s["cells"]) == EXPECTED_SINGLETON,
         "C78s exact row census")
    singleton_by_cell = one_index(singleton_rows, "cell_id", "C78s projection")
    singleton_pair_by_index = one_index(singleton_pairs, "pair_index", "C78s pairs")

    large_set = set(large_by_cell)
    singleton_set = set(singleton_by_cell)
    need(not (large_set & singleton_set) and
         large_set | singleton_set == unresolved,
         "C78l/C78s disjoint exhaustive unresolved overlay")
    need(all(component_by_index[c55b_by_cell[cell]["component_index"]]["cell_count"] == 850
             for cell in large_set), "C78l only large components")
    need(all(component_by_index[c55b_by_cell[cell]["component_index"]]["cell_count"] == 1
             for cell in singleton_set), "C78s only singleton components")

    overlay_rows: list[dict[str, Any]] = []
    overlay_by_cell: dict[str, dict[str, Any]] = {}
    for cell_id in sorted(unresolved, key=lambda item: by_cell[item]["leaf_ordinal"]):
        leaf = by_cell[cell_id]
        structure = c55b_by_cell[cell_id]
        if cell_id in large_by_cell:
            authority_row = large_by_cell[cell_id]
            enum = authority_row.get("public_cell_disposition")
            need(enum in LARGE_MAP and authority_row.get("unresolved_count") == 0 and
                 authority_row.get("owner_history_glue_two_sides_incidence_closed") is True and
                 authority_row.get("prefix_Kraft", {}).get("prefix_free") is True and
                 authority_row.get("C55A_identity_role_only") is True and
                 authority_row.get("C55A_termination_or_partition_authority_used") is False,
                 "C78l terminal and closure authority")
            terminal, rule = LARGE_MAP[enum]
            authority = "C78L_VERIFIED_FINAL_SURFACE"
        else:
            authority_row = singleton_by_cell[cell_id]
            enum = authority_row.get("terminal_enum")
            need(enum in SINGLETON_MAP and
                 authority_row.get("global_projection_installed") is False and
                 authority_row.get("candidate_is_authority") is False and
                 authority_row.get("singleton_branch_unresolved") == 0 and
                 authority_row.get("branch_projection_target") == "C79G_ATOMIC_MERGE",
                 "C78s terminal authority projection")
            pair = singleton_pair_by_index[structure["pair_index"]]
            need(pair.get("whole_reflection_pair_terminal") is True and
                 pair.get("parent_prefix_free") is True and
                 pair.get("parent_Kraft") == "1" and
                 pair.get("prefix_free_and_exact_Kraft_one_certificate_carried_from_C77s") is True,
                 "C78s exact parent Kraft")
            terminal, rule = SINGLETON_MAP[enum]
            authority = "C78S_VERIFIED_FINAL_SURFACE"
        row = close_row({
            "schema": SCHEMA + ".overlay-row",
            "overlay_ordinal": len(overlay_rows),
            "leaf_ordinal": leaf["leaf_ordinal"],
            "cell_id": cell_id,
            "C55A_leaf_row_sha256": leaf["row_sha256"],
            "C55B_cell_row_sha256": structure["row_sha256"],
            "pair_index": structure["pair_index"],
            "component_index": structure["component_index"],
            "component_id": structure["component_id"],
            "reflection_partner_cell_id": structure["reflection_partner_cell_id"],
            "previous_terminal_disposition": None,
            "previous_unresolved_reason": leaf["unresolved_reason"],
            "terminal_authority": authority,
            "terminal_authority_row_sha256": authority_row["row_sha256"],
            "authority_input_enum": enum,
            "mapping_rule": rule,
            "terminal_disposition": terminal,
            "overlay_sets_disjoint_and_exact": True,
            "installed_atomically_only_by_C79g_completion": True,
            "row_is_individually_creditable": False,
            "closure": dict(CLOSURE),
        })
        overlay_rows.append(row)
        overlay_by_cell[cell_id] = row
    need(len(overlay_rows) == EXPECTED_OVERLAY, "overlay 1148")

    successor_rows: list[dict[str, Any]] = []
    successor_by_cell: dict[str, dict[str, Any]] = {}
    final_census: Counter[str] = Counter()
    retained = 0
    replaced = 0
    for leaf in leaves:
        overlay = overlay_by_cell.get(leaf["cell_id"])
        if overlay is None:
            terminal = leaf["terminal_disposition"]
            need(terminal in TERMINALS and leaf["unresolved_reason"] is None,
                 "baseline remains terminal")
            mode = "C72G_BASELINE_RETAINED"
            authority = "C55A_PREEXISTING_TERMINAL_RETAINED_UNDER_C72G_STRUCTURAL_CLOSURE"
            authority_row_sha = leaf["row_sha256"]
            overlay_sha = None
            preserved = True
            retained += 1
        else:
            terminal = overlay["terminal_disposition"]
            mode = "C79G_OVERLAY_REPLACEMENT"
            authority = overlay["terminal_authority"]
            authority_row_sha = overlay["terminal_authority_row_sha256"]
            overlay_sha = overlay["row_sha256"]
            preserved = False
            replaced += 1
        row = close_row({
            "schema": SCHEMA + ".full-successor-row",
            "leaf_ordinal": leaf["leaf_ordinal"],
            "cell_id": leaf["cell_id"],
            "C55A_leaf_row_sha256": leaf["row_sha256"],
            "origin_key": leaf["origin_key"],
            "physical_chart": leaf["physical_chart"],
            "exact_box": leaf["exact_box"],
            "source_cell_row_sha256": leaf["source_cell_row_sha256"],
            "component_ref": leaf["component_ref"],
            "reflection_pair_ref": leaf["reflection_pair_ref"],
            "previous_terminal_disposition": leaf["terminal_disposition"],
            "previous_unresolved_reason": leaf["unresolved_reason"],
            "successor_terminal_disposition": terminal,
            "successor_unresolved_reason": None,
            "lineage_mode": mode,
            "terminal_authority": authority,
            "terminal_authority_row_sha256": authority_row_sha,
            "overlay_row_sha256": overlay_sha,
            "baseline_terminal_preserved_exactly": preserved,
            "candidate_atomic_install_only": True,
        })
        successor_rows.append(row)
        successor_by_cell[leaf["cell_id"]] = row
        final_census[terminal] += 1
    need(len(successor_rows) == EXPECTED_UNIVERSE and retained == EXPECTED_BASELINE and
         replaced == EXPECTED_OVERLAY and sum(final_census.values()) == EXPECTED_UNIVERSE,
         "full successor exact partition")
    need(not (set(final_census) - TERMINALS), "final four-class census keys")

    parent_rows: list[dict[str, Any]] = []
    parent_modes: Counter[str] = Counter()
    for pair_index in sorted(pair_cells):
        rows = pair_cells[pair_index]
        role_rows = {by_cell[row["cell_id"]]["component_ref"]["cell_role"]: row for row in rows}
        need(set(role_rows) == {"REPRESENTATIVE", "REFLECTED"}, "reflection roles")
        representative = role_rows["REPRESENTATIVE"]
        reflected = role_rows["REFLECTED"]
        ids = {representative["cell_id"], reflected["cell_id"]}
        evidence = "C42_INSTALLED_PARENT_CONSERVATION_VIA_C53_C55B_JOIN"
        if ids <= baseline:
            mode = "C72G_BASELINE_RETAINED"
            authority = "C55A_PREEXISTING_TERMINALS_WITH_C72G_STRUCTURAL_CLOSURE"
            authority_sha = by_cell[representative["cell_id"]]["row_sha256"]
            need(all(row["whole_pair_terminal_after_C53"] is True for row in rows),
                 "baseline pair C53 closure")
        elif ids <= large_set:
            mode = "C78L_OVERLAY"
            authority = "C78L_VERIFIED_FINAL_SURFACE"
            pair = large_pair_by_index[pair_index]
            authority_sha = pair["row_sha256"]
            need(pair.get("owner_history_glue_two_sides_incidence_closed") is True and
                 pair.get("prefix_Kraft", {}).get("prefix_free") is True and
                 pair.get("unresolved_count") == 0,
                 "C78l reflection parent closure")
        else:
            need(ids <= singleton_set, "no mixed reflection authority")
            mode = "C78S_OVERLAY"
            authority = "C78S_VERIFIED_FINAL_SURFACE"
            pair = singleton_pair_by_index[pair_index]
            authority_sha = pair["row_sha256"]
            need(pair.get("whole_reflection_pair_terminal") is True and
                 pair.get("parent_prefix_free") is True and pair.get("parent_Kraft") == "1",
                 "C78s reflection parent closure")
        component_indices = sorted({row["component_index"] for row in rows})
        need(len(component_indices) == 2, "reflection pair exact cross-component involution")
        dispositions = Counter(successor_by_cell[item]["successor_terminal_disposition"] for item in ids)
        parent = close_row({
            "schema": SCHEMA + ".reflection-parent-closure-row",
            "parent_ordinal": len(parent_rows),
            "pair_index": pair_index,
            "representative_cell_id": representative["cell_id"],
            "reflected_cell_id": reflected["cell_id"],
            "representative_C55B_row_sha256": representative["row_sha256"],
            "reflected_C55B_row_sha256": reflected["row_sha256"],
            "representative_successor_row_sha256": successor_by_cell[representative["cell_id"]]["row_sha256"],
            "reflected_successor_row_sha256": successor_by_cell[reflected["cell_id"]]["row_sha256"],
            "component_indices": component_indices,
            "parent_lineage_mode": mode,
            "terminal_authority": authority,
            "parent_authority_row_sha256": authority_sha,
            "terminal_disposition_census": dict(sorted(dispositions.items())),
            "reciprocal_reflection_partner_identity_closed": True,
            "owner_history_glue_two_sides_incidence_closed": True,
            "prefix_Kraft": {
                "evidence_authority": evidence,
                "C42_parent_row_sha256":
                    kraft_chain["C42_rows_by_pair"][pair_index]["row_sha256"],
                "C53_parent_projection_object_sha256":
                    kraft_chain["C53_projections_by_pair"][pair_index]["projection_object_sha256"],
                "C55B_crosswalk_two_side_row_sha256s":
                    sorted(row["row_sha256"] for row in rows),
                "C42_parent_Kraft_conservation": "1",
                "C72_boolean_used_as_authority": False,
                "prefix_free": True,
                "exact_parent_closure": True,
                "physical_reflection_duplicate_credit": 0,
            },
            "unresolved_count": 0,
        })
        parent_rows.append(parent)
        parent_modes[mode] += 1
    need(len(parent_rows) == EXPECTED_PAIRS and parent_modes == Counter({
        "C72G_BASELINE_RETAINED": EXPECTED_BASELINE_PAIRS,
        "C78L_OVERLAY": EXPECTED_LARGE_PAIRS,
        "C78S_OVERLAY": EXPECTED_SINGLETON_PAIRS,
    }), "862 reflection parent authority partition")

    return {
        "static": static,
        "C78l": c78l,
        "C78s": c78s,
        "overlay_rows": overlay_rows,
        "successor_rows": successor_rows,
        "parent_rows": parent_rows,
        "final_census": {key: final_census.get(key, 0) for key in sorted(TERMINALS)},
        "parent_modes": dict(sorted(parent_modes.items())),
        "C55B_topology": c55b_topology,
        "C42_C53_Kraft_chain": {
            key: copy.deepcopy(value) for key, value in kraft_chain.items()
            if key not in {
                "C42_rows_by_pair", "C53_projections_by_pair", "held_direct_inputs",
                "C42_candidate_universe",
                "C42_candidate_guard", "C42_held_directories",
            }
        },
        "direct_input_terminal_guard": {
            "held_inputs": kraft_chain["held_direct_inputs"],
            "C42_candidate_universe": kraft_chain["C42_candidate_universe"],
            "C42_held_directories": kraft_chain["C42_held_directories"],
        },
        "C78s_terminal_guard": {
            "held_inputs": c78s["held_inputs"],
            "held_directories": c78s["held_directories"],
        },
        "C78l_terminal_guard": {
            "held_inputs": c78l["held_inputs"],
            "held_directories": c78l["held_directories"],
        },
        "fixed_historical_terminal_guard": fixed_historical_guards,
        "baseline_count": retained,
        "overlay_count": replaced,
    }


def input_registry(state: dict[str, Any], self_guard: HeldSelf,
                   static_trust: dict[str, Any]) -> dict[str, Any]:
    fixed_files: dict[str, dict[str, str]] = {}
    for family, paths, pins in (
        ("C55A", C55A_PATHS, C55A_PINS),
        ("C55B", C55B_PATHS, C55B_PINS),
        ("C72g", C72G_PATHS, C72G_PINS),
    ):
        for key in sorted(paths):
            fixed_files[f"{family}:{key}"] = {
                "path": str(paths[key].relative_to(ROOT)), "file_sha256": pins[key],
            }
    for key in sorted(C42_C53_PATHS):
        fixed_files[f"DIRECT_KRAFT:{key}"] = {
            "path": str(C42_C53_PATHS[key].relative_to(ROOT)),
            "file_sha256": C42_C53_PINS[key],
        }
    c78l_files = {key: {"filename": C78L_NAMES[key], "file_sha256": C78L_PINS[key]}
                   for key in sorted(C78L_NAMES)}
    c78s_files = {key: {"filename": C78S_NAMES[key], "file_sha256": C78S_FINAL["pins"][key]}
                   for key in sorted(C78S_NAMES)}
    return close_object({
        "schema": SCHEMA + ".source-registry",
        "producer_file_sha256": self_guard.file_sha256,
        "contract_file_sha256": CONTRACT_FILE_PIN,
        "contract_object_sha256": CONTRACT_OBJECT_PIN,
        "closed_schema_file_sha256": CLOSED_SCHEMA_FILE_PIN,
        "v5_official_rejection_file_sha256":
            static_trust["v5_official_rejection_file_sha256"],
        "v5_official_rejection_object_sha256":
            static_trust["v5_official_rejection_object_sha256"],
        "v6_official_rejection_file_sha256":
            static_trust["v6_official_rejection_file_sha256"],
        "v6_official_rejection_object_sha256":
            static_trust["v6_official_rejection_object_sha256"],
        "v7_official_rejection_file_sha256":
            static_trust["v7_official_rejection_file_sha256"],
        "v7_official_rejection_object_sha256":
            static_trust["v7_official_rejection_object_sha256"],
        "v8_official_rejection": copy.deepcopy(
            static_trust["v8_official_rejection"]),
        "v8_official_rejection_file_sha256":
            static_trust["v8_official_rejection_file_sha256"],
        "v8_official_rejection_object_sha256":
            static_trust["v8_official_rejection_object_sha256"],
        "v9_official_rejection": copy.deepcopy(
            static_trust["v9_official_rejection"]),
        "v9_official_rejection_file_sha256":
            static_trust["v9_official_rejection_file_sha256"],
        "v9_official_rejection_object_sha256":
            static_trust["v9_official_rejection_object_sha256"],
        "v10_official_rejection": copy.deepcopy(
            static_trust["v10_official_rejection"]),
        "v10_official_rejection_file_sha256":
            static_trust["v10_official_rejection_file_sha256"],
        "v10_official_rejection_object_sha256":
            static_trust["v10_official_rejection_object_sha256"],
        "v11_official_rejection": copy.deepcopy(
            static_trust["v11_official_rejection"]),
        "v11_official_rejection_file_sha256":
            static_trust["v11_official_rejection_file_sha256"],
        "v11_official_rejection_object_sha256":
            static_trust["v11_official_rejection_object_sha256"],
        **self_guard.execution_proof(),
        "v3_official_later_rejection_receipt": {
            "path": str(V3_OFFICIAL_REJECTION.relative_to(ROOT)),
            "file_sha256": V3_REJECTION_FILE_PIN,
            "object_sha256": V3_REJECTION_OBJECT_PIN,
            "reason": "ORPHANED_OR_INCOMPLETE_C79G_V3_SURFACE",
        },
        "v4_rejection_supersession_receipt": {
            "path": str(V4_REJECTION_SUPERSESSION.relative_to(ROOT)),
            "file_sha256": static_trust[
                "v4_rejection_supersession_file_sha256"],
            "object_sha256": static_trust[
                "v4_rejection_supersession_object_sha256"],
            "v4_execution_allowed": False,
            "v4_credit_transferred": 0,
        },
        "published_then_officially_rejected_predecessor_v5": copy.deepcopy(
            static_trust["transition"][
                "published_then_officially_rejected_predecessor_v5"]),
        "published_then_officially_rejected_predecessor_v6": copy.deepcopy(
            static_trust["transition"][
                "published_then_officially_rejected_predecessor_v6"]),
        "published_then_officially_rejected_predecessor_v7": copy.deepcopy(
            static_trust["transition"][
                "published_then_officially_rejected_predecessor_v7"]),
        "published_then_officially_rejected_predecessor_v8": copy.deepcopy(
            static_trust[
                "published_then_officially_rejected_predecessor_v8"]),
        "published_then_officially_rejected_predecessor_v9": copy.deepcopy(
            static_trust[
                "published_then_officially_rejected_predecessor_v9"]),
        "published_then_officially_rejected_predecessor_v10": copy.deepcopy(
            static_trust[
                "published_then_officially_rejected_predecessor_v10"]),
        "published_then_officially_rejected_predecessor_v11": copy.deepcopy(
            static_trust[
                "published_then_officially_rejected_predecessor_v11"]),
        "published_then_officially_rejected_predecessor_v12": copy.deepcopy(
            static_trust[
                "published_then_officially_rejected_predecessor_v12"]),
        "v12_official_rejection_file_sha256":
            V12_OFFICIAL_REJECTION_FILE_PIN,
        "v12_official_rejection_object_sha256":
            V12_OFFICIAL_REJECTION_OBJECT_PIN,
        "v12_v5_rejection_shape_incident": copy.deepcopy(
            V12_V5_REJECTION_SHAPE_INCIDENT),
        "v10_regression_label_prefix_incident": copy.deepcopy(
            static_trust["v10_regression_label_prefix_incident"]),
        "v10_colon_prefix_witness_object_sha256":
            static_trust["v10_colon_prefix_witness"]["object_sha256"],
        "v11_dual_validator_divergence_incident": copy.deepcopy(
            static_trust["v11_dual_validator_divergence_incident"]),
        "v9_v6_held_self_identity_defect_shape_drift_incident": copy.deepcopy(
            static_trust[
                "v9_v6_held_self_identity_defect_shape_drift_incident"]),
        "v8_rollout_control_flow_incident": copy.deepcopy(
            static_trust["v8_rollout_control_flow_incident"]),
        "v7_publication_lock_continuity_incident": copy.deepcopy(
            static_trust["v7_publication_lock_continuity_incident"]),
        "frozen_predecessor_incident_source_exact10_held_fd_bytes_read_only": True,
        "frozen_predecessor_incident_sources_used_only_for_noncredit_regression_authority": True,
        "append_only_history_unique_file_identity_count":
            V16R2_TERMINAL_UNIQUE_LIVE_IDENTITY_COUNT,
        "post_source_static_freeze_trust": {
            "v16_to_v16r2_transition_receipt": {
                "path": str(V16_TO_V16R2_TRANSITION.relative_to(ROOT)),
                "file_sha256": static_trust["transition_file_sha256"],
                "object_sha256": static_trust["transition_object_sha256"],
            },
            "static_audit_v16r2": {
                "path": str(STATIC_AUDIT_V16R2.relative_to(ROOT)),
                "file_sha256": static_trust["static_audit_file_sha256"],
                "object_sha256": static_trust["static_audit_object_sha256"],
            },
            "cold_launcher": {
                "path": str(COLD_LAUNCHER.relative_to(ROOT)),
                "file_sha256": static_trust["cold_launcher_file_sha256"],
            },
            "cold_launch_manifest": {
                "path": str(COLD_MANIFEST.relative_to(ROOT)),
                "file_sha256": static_trust["cold_manifest_file_sha256"],
                "ordered_entry_count": 8,
            },
            "cold_launch_outer_last": {
                "path": str(COLD_OUTER.relative_to(ROOT)),
                "file_sha256": static_trust["cold_outer_file_sha256"],
                "object_sha256": static_trust["cold_outer_object_sha256"],
            },
            "both_receipts_strict_parsed_object_closed_held_and_terminally_replayed": True,
            "both_receipts_pin_current_producer_and_policy_bundle": True,
            "exact8_manifest_and_outer_last_strictly_validated_and_terminally_replayed": True,
            "all_exact8_mtime_not_after_final_ctime":
                static_trust["all_exact8_mtime_not_after_final_ctime"],
            "max_exact8_final_mtime_ctime_before_manifest_mtime":
                static_trust["max_exact8_final_mtime_ctime_before_manifest_mtime"],
            "manifest_mtime_not_after_final_ctime":
                static_trust["manifest_mtime_not_after_final_ctime"],
            "manifest_final_ctime_before_outer_mtime":
                static_trust["manifest_final_ctime_before_outer_mtime"],
            "outer_mtime_not_after_final_ctime":
                static_trust["outer_mtime_not_after_final_ctime"],
            "physical_exact8_freeze_then_manifest_freeze_then_outer_freeze_chronology":
                static_trust[
                    "physical_exact8_freeze_then_manifest_freeze_then_outer_freeze_chronology"],
            "cold_exact10_identities_unique_same_mount":
                static_trust["cold_exact10_identities_unique_same_mount"],
            "normative_runtime_entry_is_externally_pinned_cold_launcher": True,
        },
        "effective_checkpoint_object_sha256": UPSTREAM_CHECKPOINT_OBJECT_PIN,
        "fixed_input_files": fixed_files,
        "C78l_dual_base_member_pins": c78l_files,
        "C78l_verification_file_sha256": C78L_VERIFY_FILE_PIN,
        "C78l_verification_object_sha256": C78L_VERIFY_OBJECT_PIN,
        "C78l_completion_member_pins": dict(C78L_COMPLETION_PINS),
        "C78s_filled_final_surface": copy.deepcopy(C78S_FINAL),
        "C78s_dual_base_member_pins": c78s_files,
        "C55B_topology_reconstruction": copy.deepcopy(state["C55B_topology"]),
        "C42_C53_direct_Kraft_reconstruction": r63ah_normalize_kraft_registry(state["C42_C53_Kraft_chain"]),
        "current_v16r2_producer_source_content_opened_or_read": False,
        "current_v16r2_producer_source_content_imported_compiled_or_executed": False,
        "terminal_authority": {"C78l_rows": EXPECTED_LARGE, "C78s_rows": EXPECTED_SINGLETON},
        "structure_only_authority": ["C55A", "C55B", "C72g"],
        "C55A_C55B_C72g_new_terminal_authority": False,
        "canonical_pointer_written": False,
        "standalone_non_authoritative": True,
        "authority_requires_committed_completion_replay24_rejection_and_seal": True,
        "D02_started": False,
        "candidate_credit": dict(ZERO_CANDIDATE_CREDIT),
    })


def build(outdir: Path, self_guard: HeldSelf,
          coordination_parent: HeldParent) -> None:
    # The caller/main has already executed ensure_launch_configuration().
    # No input was read and no output path was touched before that gate.
    need(outdir.is_absolute() and outdir in {CANDIDATE_A, CANDIDATE_B} and
         outdir.parent == RUNTIME,
         "candidate output is one exact checkpoint-keyed A/B path")
    static_trust = hold_static_freeze_trust(self_guard)
    secure_directory(RUNTIME)
    state = reconstruct(static_trust)

    overlay_raw, overlay_desc = gzip_encode(state["overlay_rows"])
    successor_raw, successor_desc = gzip_encode(state["successor_rows"])
    parents_raw, parents_desc = gzip_encode(state["parent_rows"])
    need(overlay_desc["row_count"] == EXPECTED_OVERLAY and
         successor_desc["row_count"] == EXPECTED_UNIVERSE and
         parents_desc["row_count"] == EXPECTED_PAIRS,
         "output descriptor counts")
    registry = input_registry(state, self_guard, static_trust)
    descriptors = {
        "overlay_1148": overlay_desc,
        "full_successor_76832": successor_desc,
        "reflection_parent_closure_862": parents_desc,
    }
    final_census = dict(state["final_census"])
    final_census["total"] = sum(final_census.values())
    result = close_object({
        "schema": SCHEMA + ".result",
        "status": "PASS_CANDIDATE_1148_EXACT_OVERLAY__76832_FULL_SUCCESSOR__862_REFLECTION_PARENTS__PUBLIC_UNRESOLVED_ZERO__AWAIT_COLD_LAUNCHED_COMPOSITE_FOR_FORMAL_CREDIT",
        "source_registry_object_sha256": registry["object_sha256"],
        "ledger_descriptors": descriptors,
        "exact_overlay_partition": {
            "C78l_large": EXPECTED_LARGE,
            "C78s_singleton": EXPECTED_SINGLETON,
            "total": state["overlay_count"],
            "sets_disjoint": True,
            "union_equals_C55A_and_C55B_unresolved": True,
        },
        "baseline_retention": {
            "retained_terminal_rows": state["baseline_count"],
            "terminal_disposition_unchanged": True,
            "C55A_row_lineage_unchanged": True,
        },
        "derived_final_four_class_census": final_census,
        "derived_final_four_class_census_was_not_hard_coded": True,
        "public_global_unresolved": 0,
        "reflection_parent_closure": {
            "row_count": EXPECTED_PAIRS,
            "authority_partition": state["parent_modes"],
            "reciprocal": True,
            "all_terminal": True,
        },
        "C55B_topology_reconstruction": copy.deepcopy(state["C55B_topology"]),
        "authority_separation": {
            "C55A": "IDENTITY_AND_PREDECESSOR_DISPOSITION_ONLY",
            "C55B": "COMPONENT_REFLECTION_GLUE_INCIDENCE_STRUCTURE_ONLY",
            "C72g": "BASELINE_STRUCTURAL_CLOSURE_ONLY",
            "C78l": "SOLE_AUTHORITY_FOR_1124_REPLACEMENTS",
            "C78s": "SOLE_AUTHORITY_FOR_24_REPLACEMENTS",
            "C55A_C55B_C72g_new_terminal_authority": False,
        },
        "closure": dict(CLOSURE),
        "candidate_credit": dict(ZERO_CANDIDATE_CREDIT),
        "standalone_non_authoritative": True,
        "formal_credit_authority":
            "ONLY_EXTERNALLY_PINNED_COLD_LAUNCHER_WRAPPER_AFTER_HELD_CHILD_AND_POST_CHILD_TERMINAL_REPLAY",
        "precursor_credits": {
            "C65_local_terminal_formal_credit": 0,
            "C69c_source_decision_formal_credit": 0,
            "C70_ready_intersection_formal_credit": 0,
            "C78l_precursor_formal_credit": 0,
            "C78s_precursor_formal_credit": 0,
        },
        "actual_C3_disposition_count": 0,
        "conditional_C3_promoted_to_actual_C3": False,
        "canonical_pointer_written": False,
        "D02_started": False,
    })
    report = (
        "# C79g true global no-producer consumer candidate\n\n"
        f"- exact overlay: `{EXPECTED_LARGE} + {EXPECTED_SINGLETON} = {EXPECTED_OVERLAY}`\n"
        f"- baseline terminal rows retained: `{EXPECTED_BASELINE}`\n"
        f"- full successor rows: `{EXPECTED_UNIVERSE}`; public unresolved: `0`\n"
        f"- reflection parents: `{EXPECTED_PAIRS}` (`{EXPECTED_BASELINE_PAIRS}` baseline, "
        f"`{EXPECTED_LARGE_PAIRS}` C78l, `{EXPECTED_SINGLETON_PAIRS}` C78s)\n"
        f"- final four-class census (derived after merge): `{json.dumps(final_census, sort_keys=True)}`\n"
        "- owner/history/glue/two-sides/incidence/prefix-Kraft: closed\n"
        "- C55A/C55B/C72g are identity/structure only; new terminal authority is exclusively C78l/C78s\n"
        "- candidate credit is zero; candidate is standalone non-authoritative\n"
        "- formal global closure credit exists only after composite completion/replay/rejection/seal consumption\n"
        f"- D02 gate/task credit: `0/0`; formal pending tasks: `{EXPECTED_PENDING_D02}`; D02 not started\n"
        "- no canonical pointer.\n"
    ).encode("utf-8")
    lock = (
        "C79g v16r2 isolated candidate only; standalone non-authoritative. Formal-global credit "
        "remains zero until the unique composite committed completion, live replay24, live v3 "
        "exact10 plus official later rejection, and authority seal predicate is independently "
        "consumed. D02 is not started.\n"
    ).encode("ascii")

    base_raw = {
        LOCK: lock,
        OVERLAY: overlay_raw,
        SUCCESSOR: successor_raw,
        PARENTS: parents_raw,
        REGISTRY: canonical(registry) + b"\n",
        RESULT: canonical(result) + b"\n",
        REPORT: report,
    }
    parent_guard = coordination_parent
    parent_guard.verify()
    require_candidate_target_absent(outdir, parent_guard)
    stage, stage_guard = new_candidate_stage(outdir, parent_guard)
    created: dict[str, HeldCreatedFile] = {}
    for name in (LOCK, OVERLAY, SUCCESSOR, PARENTS, REGISTRY, RESULT, REPORT):
        created[name] = exclusive_at(stage_guard, name, base_raw[name])
    manifest_raw = b"".join(
        f"{sha_bytes(base_raw[name])}  {name}\n".encode("ascii")
        for name in (LOCK, OVERLAY, SUCCESSOR, PARENTS, REGISTRY, RESULT, REPORT)
    )
    created[CANDIDATE_MANIFEST] = exclusive_at(
        stage_guard, CANDIDATE_MANIFEST, manifest_raw)
    outer = close_object({
        "schema": SCHEMA + ".candidate-outer-receipt",
        "candidate_result_object_sha256": result["object_sha256"],
        "source_registry_object_sha256": registry["object_sha256"],
        "candidate_manifest_file_sha256": sha_bytes(manifest_raw),
        "ordered_member_file_sha256": [
            {"filename": name, "file_sha256": sha_bytes(base_raw[name])}
            for name in (LOCK, OVERLAY, SUCCESSOR, PARENTS, REGISTRY, RESULT, REPORT)
        ],
        "candidate_outer_receipt_published_last": True,
        "terminal_byte_replay_required_after_outer_receipt": True,
        "candidate_directory_sealed_mode_after_terminal_replay": "0555",
        "candidate_member_required_mode": "0444",
        "partial_publication_policy": "REJECT_AND_PRESERVE_NEVER_OVERWRITE_OR_REUSE",
        "candidate_install": {
            "staging_path_template":
                ".cm2-runtime/.c79g-v16r2r63ah-candidate-stage-{a|b}-" + UPSTREAM_CHECKPOINT_OBJECT_PIN,
            "fixed_target_set": [
                str(CANDIDATE_A.relative_to(ROOT)),
                str(CANDIDATE_B.relative_to(ROOT)),
            ],
            "actual_orientation_or_stage_path_persisted_in_candidate_bytes": False,
            "orientation_invariant_descriptor_preserves_full_exact9_A_B_byte_identity": True,
            "held_parent_path": str(RUNTIME.relative_to(ROOT)),
            "launcher_owned_coordination_parent_fd_required": True,
            "official_writer_coordination_lock_api": "launcher_owned_fcntl.flock(LOCK_EX)",
            "all_official_runtime_writers_must_share_coordination_lock": True,
            "coordination_lock_not_claimed_as_same_uid_or_filesystem_admin_security_boundary": True,
            "staging_and_target_single_components_under_same_held_parent_dirfd": True,
            "stage_held_from_immediate_post_mkdir_open_until_postcommit": True,
            "all_exact9_members_created_O_EXCL_and_held_from_creation": True,
            "all_exact9_members_fsynced_and_mode_0444_before_commit": True,
            "stage_directory_fsynced_and_mode_0555_before_commit": True,
            "commit_operation": "RENAMEAT2_RENAME_NOREPLACE",
            "ordinary_rename_replace_or_fallback_allowed": False,
            "fixed_target_prechecked_absent_before_stage_creation": True,
            "absence_precheck_is_only_orphan_avoidance_not_race_commit_gate": True,
            "live_consumer_rederives_fixed_A_B_paths_and_revalidates_both_surfaces": True,
            "postrename_destination_must_equal_creation_held_stage_identity": True,
            "parent_fsync_required_for_crash_durability_after_namespace_commit": True,
            "parent_fsync_not_claimed_to_precede_namespace_visibility": True,
        },
        "candidate_credit": dict(ZERO_CANDIDATE_CREDIT),
        "standalone_non_authoritative": True,
        "authority_requires_committed_completion_replay24_rejection_and_seal": True,
        "canonical_pointer_written": False,
        "D02_started": False,
    })
    outer_raw = canonical(outer) + b"\n"
    created[CANDIDATE_OUTER] = exclusive_at(
        stage_guard, CANDIDATE_OUTER, outer_raw)
    base_mtimes = [created[name].before.st_mtime_ns
                   for name in (LOCK, OVERLAY, SUCCESSOR, PARENTS, REGISTRY, RESULT, REPORT)]
    manifest_mtime = created[CANDIDATE_MANIFEST].before.st_mtime_ns
    outer_mtime = created[CANDIDATE_OUTER].before.st_mtime_ns
    need(max(base_mtimes) < manifest_mtime < outer_mtime,
         "candidate publication mtime order and outer-last")
    output_guards = [created[name] for name in CANDIDATE_MEMBERS]
    need(len({guard.identity for guard in output_guards}) == len(CANDIDATE_MEMBERS),
         "candidate exact9 member identities globally unique")
    stage_guard.seal(set(CANDIDATE_MEMBERS))
    secure_directory(stage, 0o555)
    need(set(os.listdir(stage_guard.fd)) == set(CANDIDATE_MEMBERS),
         "candidate exact9 terminal universe")
    for guard in output_guards:
        guard.terminal_replay()
    direct_guard = state["direct_input_terminal_guard"]
    for guard in direct_guard["held_inputs"]:
        guard.terminal_replay()
    for guard in direct_guard["C42_held_directories"]:
        guard.terminal_replay()
    for guard in state["fixed_historical_terminal_guard"]:
        guard.terminal_replay()
    c78s_guard = state["C78s_terminal_guard"]
    for guard in c78s_guard["held_inputs"]:
        guard.terminal_replay()
    for guard in c78s_guard["held_directories"]:
        guard.terminal_replay()
    c78l_guard = state["C78l_terminal_guard"]
    for guard in c78l_guard["held_inputs"]:
        guard.terminal_replay()
    for guard in c78l_guard["held_directories"]:
        guard.terminal_replay()
    stage_guard.terminal_replay(parent_guard)
    for guard in static_trust["guards"]:
        guard.terminal_replay()
    require_v10_positive_and_stage_surfaces_absent()
    require_v9_positive_and_stage_surfaces_absent()
    require_v8_positive_and_stage_surfaces_absent()
    require_v7_positive_and_stage_surfaces_absent()
    require_v6_positive_and_stage_surfaces_absent()
    require_v5_positive_and_stage_surfaces_absent()
    terminal_chronology = cold_publication_chronology(
        [self_guard.before if path == SELF else
         static_trust["by_path"][path].before for path in COLD_EXACT8],
        static_trust["cold_manifest_guard"].before,
        static_trust["cold_outer_guard"].before)
    need(terminal_chronology == static_trust["chronology"] and
         all(terminal_chronology.values()),
         "terminal cold exact8/manifest/outer freeze chronology")
    self_guard.terminal_replay()
    workspace_root_terminal_replay()
    rename_candidate_noreplace(
        stage, outdir, stage_guard, output_guards, parent_guard)
    # Historical evidence remains held until the candidate namespace commit
    # and its parent fsync have completed.  The terminal replay above is the
    # last semantic gate; these closes are post-commit cleanup only.
    for guard in direct_guard["held_inputs"]:
        guard.close()
    for guard in reversed(direct_guard["C42_held_directories"]):
        guard.close()
    for guard in state["fixed_historical_terminal_guard"]:
        guard.close()
    for guard in output_guards:
        guard.close()
    for guard in c78s_guard["held_inputs"]:
        guard.close()
    for guard in c78s_guard["held_directories"]:
        guard.close()
    for guard in c78l_guard["held_inputs"]:
        guard.close()
    for guard in c78l_guard["held_directories"]:
        guard.close()
    for guard in static_trust["guards"]:
        guard.close()
    stage_guard.close()



def parser() -> argparse.ArgumentParser:
    cli = argparse.ArgumentParser(description=__doc__)
    sub = cli.add_subparsers(dest="command", required=True)
    build_cmd = sub.add_parser("build")
    build_cmd.add_argument("--outdir", required=True, type=Path)
    return cli


def terminal_replay_v14_exact10_and_official_rejection(
        held_raw_by_role: Mapping[str, bytes]) -> dict[str, Any]:
    """Replay v14 exact10 then its rejection; return only zero-credit truth."""
    expected_roles = V14_PREDECESSOR_TERMINAL_REPLAY_ORDER
    need(tuple(held_raw_by_role) == expected_roles,
         "v14 predecessor exact10 then official rejection held role order")
    decoded: dict[str, Mapping[str, Any]] = {}
    for role, _, file_pin, object_pin in V14_PUBLISHED_EXACT10_WITNESS:
        raw = held_raw_by_role[role]
        need(isinstance(raw, bytes) and
             hashlib.sha256(raw).hexdigest() == file_pin,
             "held v14 exact10 file pin: " + role)
        if object_pin is not None:
            value = strict_json(raw, "held v14 exact10 JSON: " + role)
            need(isinstance(value, Mapping),
                 "held v14 exact10 object: " + role)
            body = dict(value)
            declared = body.pop("object_sha256", None)
            need(declared == object_pin and
                 hashlib.sha256(canonical(body)).hexdigest() == object_pin,
                 "held v14 exact10 object pin: " + role)
            decoded[role] = value
    expected_manifest = b"".join(
        (file_pin + "  " + relative_path + "\n").encode("utf-8")
        for _, relative_path, file_pin, _ in
            V14_PUBLISHED_EXACT10_WITNESS[:8])
    need(held_raw_by_role["cold_manifest"] == expected_manifest,
         "held v14 exact8 manifest exact ordered bytes")
    outer = decoded["cold_outer"]
    expected_entries = [
        {"file_sha256": file_pin, "path": relative_path}
        for _, relative_path, file_pin, _ in
            V14_PUBLISHED_EXACT10_WITNESS[:8]
    ]
    need(outer.get("status") ==
             "FROZEN_COLD_LAUNCH_OUTER_LAST__EXACT8_MANIFEST_CLOSED__RUNTIME_DEFERRED" and
         outer.get("exact8_ordered_entries") == expected_entries and
         outer.get("formal_global_closure_credit") == 0 and
         outer.get("D02_unlock") is False and
         outer.get("runtime_executed_during_static_freeze") is False,
         "held v14 outer exact8 and zero-credit closure")
    rejection_raw = held_raw_by_role["v14_official_rejection"]
    need(isinstance(rejection_raw, bytes) and
         hashlib.sha256(rejection_raw).hexdigest() ==
             V14_OFFICIAL_REJECTION_FILE_PIN,
         "held v14 official rejection file pin")
    rejection = strict_json(rejection_raw, "held v14 official rejection")
    need(isinstance(rejection, Mapping),
         "held v14 official rejection object")
    rejection_body = dict(rejection)
    declared_rejection_object = rejection_body.pop("object_sha256", None)
    need(declared_rejection_object == V14_OFFICIAL_REJECTION_OBJECT_PIN and
         hashlib.sha256(canonical(rejection_body)).hexdigest() ==
             V14_OFFICIAL_REJECTION_OBJECT_PIN and
         len(rejection) == 56 and
         hashlib.sha256(canonical(sorted(rejection))).hexdigest() ==
             V14_OFFICIAL_REJECTION_EXACT56_KEYSET_SHA256,
         "held v14 official rejection exact56 and object pin")
    by_role = {row[0]: row for row in V14_PUBLISHED_EXACT10_WITNESS}
    need(rejection.get("schema") ==
             "cm2.round306c79g.true-global-no-producer-consumer.v14.later-rejection" and
         rejection.get("status") ==
             "PERMANENT_FAIL_CLOSED_REJECTION__ZERO_CREDIT" and
         rejection.get("rejection_reason") ==
             "ORPHANED_OR_INCOMPLETE_C79G_V14_SURFACE" and
         rejection.get("formal_global_closure_credit") == 0 and
         rejection.get("D02_unlock") is False and
         rejection.get("D02_started") is False and
         rejection.get("D02_gate_credit") == 0 and
         rejection.get("D02_task_credit") == 0 and
         rejection.get("D02_formal_pending_task_count") == 33_638 and
         rejection.get("closed_schema_file_sha256") == by_role["closed_schema"][2] and
         rejection.get("contract_file_sha256") == by_role["contract"][2] and
         rejection.get("contract_object_sha256") == by_role["contract"][3] and
         rejection.get("producer_file_sha256") == by_role["build_only_producer"][2] and
         rejection.get("consumer_file_sha256") == by_role["independent_consumer"][2] and
         rejection.get("cold_launcher_file_sha256") == by_role["cold_launcher"][2] and
         rejection.get("cold_manifest_file_sha256") == by_role["cold_manifest"][2] and
         rejection.get("cold_outer_file_sha256") == by_role["cold_outer"][2] and
         rejection.get("cold_outer_object_sha256") == by_role["cold_outer"][3],
         "held v14 rejection binds exact10 and preserves zero credit")
    return {
        "status": "TERMINAL_REPLAY_PASS__V14_EXACT10_THEN_OFFICIAL_REJECTION__ZERO_CREDIT_ONLY",
        "terminal_replay_order": list(expected_roles),
        "chronology": list(V14_RUNTIME_REGISTRY_SHAPE_DRIFT_INCIDENT["chronology"]),
        "v14_runtime_registry_shape_drift_incident":
            copy.deepcopy(V14_RUNTIME_REGISTRY_SHAPE_DRIFT_INCIDENT),
        "formal_global_closure_credit": 0,
        "D02_unlock": False,
        "D02_started": False,
        "D02_gate_credit": 0,
        "D02_task_credit": 0,
        "D02_formal_pending_task_count": 33_638,
        "v14_credit_transferred_to_v16r2": False,
    }


def v14_inherited_authority_draft_state(
        supersession_receipt_exists: bool) -> dict[str, Any]:
    """Prove the legal v16r2 draft state without opening the frozen receipt."""
    need(V16R2_DRAFT_RUNTIME_DISABLED is True and
         FINAL_V16R2_CORE_PINS_INSTALLED is False and
         V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT_FILE_PIN not in
             V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT_DRAFT_SENTINELS and
         V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT_OBJECT_PIN not in
             V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT_DRAFT_SENTINELS and
         supersession_receipt_exists is True,
         "v16r2 draft requires frozen pinned v14 receipt and uninstalled v16r2 core pins")
    return {
        "status": "V16R2_DRAFT_RUNTIME_DISABLED__V14_SUPERSESSION_RECEIPT_FROZEN_PINNED",
        "receipt_path":
            V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT_RELATIVE_PATH,
        "receipt_open_attempted": False,
        "runtime_authorized": False,
    }


def terminal_replay_v14_inherited_authority_exact12(
        held_raw_by_role: Mapping[str, bytes]) -> dict[str, Any]:
    """Replay exact10, rejection, then final receipt from twelve held bytes."""
    need(tuple(held_raw_by_role) == V14_INHERITED_AUTHORITY_EXACT12_ROLE_ORDER and
         len(held_raw_by_role) == V16R2_CHILD_AUTHORITY_DESCRIPTOR_COUNT == 12,
         "v14 inherited authority exact12 held role order")
    need(V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT_FILE_PIN not in
             V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT_DRAFT_SENTINELS and
         V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT_OBJECT_PIN not in
             V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT_DRAFT_SENTINELS,
         "v14 supersession receipt final pins installed")
    prefix = {role: held_raw_by_role[role]
              for role in V14_PREDECESSOR_TERMINAL_REPLAY_ORDER}
    result = terminal_replay_v14_exact10_and_official_rejection(prefix)
    receipt_raw = held_raw_by_role["v14_registry_shape_drift_supersession_receipt"]
    need(hashlib.sha256(receipt_raw).hexdigest() ==
             V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT_FILE_PIN,
         "held v14 supersession receipt file pin")
    receipt = strict_json(receipt_raw, "held v14 supersession receipt")
    need(isinstance(receipt, Mapping), "held v14 supersession receipt object")
    body = dict(receipt)
    declared = body.pop("object_sha256", None)
    need(declared ==
             V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT_OBJECT_PIN and
         hashlib.sha256(canonical(body)).hexdigest() == declared,
         "held v14 supersession receipt object pin")
    result.update({
        "status": "TERMINAL_REPLAY_PASS__V14_INHERITED_AUTHORITY_EXACT12__ZERO_CREDIT_ONLY",
        "terminal_replay_order": list(V14_INHERITED_AUTHORITY_EXACT12_ROLE_ORDER),
        "held_authority_descriptor_count": 12,
        "bootstrap_descriptor_count": 4,
        "child_pass_fd_count": 16,
        "v14_supersession_receipt_object_sha256": declared,
        "formal_global_closure_credit": 0,
        "D02_unlock": False,
        "v14_credit_transferred_to_v16r2": False,
    })
    return result


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    if V16R2_DRAFT_RUNTIME_DISABLED and not FINAL_V16R2_CORE_PINS_INSTALLED:
        raise Reject(
            "C79g v16r2 successor is a sentinel draft; runtime is disabled")
    try:
        # Mandatory first gate after argument parsing.  Do not move any read,
        # existence check, directory creation, or producer/verifier work above it.
        self_guard = ensure_launch_configuration()
        coordination_parent = HeldParent(
            RUNTIME, int(os.environ[COLD_COORDINATION_PARENT_FD_ENV]))
        try:
            # The launcher owns the exclusive lock on this exact inherited
            # open-file-description.  LOCK_NB succeeds only if the descriptor
            # is already compatible with exclusive ownership (or acquires it
            # on the same description); the launcher keeps its duplicate open
            # until child exit, so this child never explicitly unlocks it.
            fcntl.flock(
                coordination_parent.fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            coordination_parent.verify()
            build(args.outdir, self_guard, coordination_parent)
            workspace_root_terminal_replay()
            self_guard.terminal_replay()
        finally:
            coordination_parent.close()
    finally:
        # The registry is a LIFO ownership stack.  In particular the workspace
        # root closes before HeldSelf, whose installed source then closes before
        # its sealed exec fd.
        close_all_held_resources()
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Reject as exc:
        print("REJECT:", exc, file=sys.stderr)
        raise SystemExit(2)
