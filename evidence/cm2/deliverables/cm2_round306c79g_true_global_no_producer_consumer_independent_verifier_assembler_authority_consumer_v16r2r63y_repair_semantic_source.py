#!/usr/bin/env python3
"""Independent C79g v16r2 verifier, assembler, and authority consumer.

The verifier never content-opens, reads, hashes, imports, compiles, decodes,
or executes the current C79g v16r2 producer source.  Frozen predecessor source
bytes are readable only after the launcher's inherited v14 exact12 held-fd
gate; older history is then opened and retained by pathname solely to rederive
noncredit incident authority.  It reconstructs the complete
pinned evidence chain, exact ledgers, direct C42/C53 Kraft joins, and exact 137
production-validator attacks.  Two swapped-orientation runs create isolated,
byte-identical zero-credit verification surfaces.  The assembler installs an
exact4 zero-credit completion surface with Linux RENAME_NOREPLACE.  The
independent authority consumer installs only a zero-credit seal, then on a
later fresh live replay constructs a zero-credit inner composite
result.  A dedicated cold-launched reject command can permanently revoke the
checkpoint without depending on C78/C42/public evidence.  Only the separately
frozen cold launcher may wrap a non-rejected inner result
into the one-credit root after its own post-child terminal replay.  Neither an
outer, a seal, nor this directly invoked source is authoritative.
"""

from __future__ import annotations

import argparse
import ast
from collections import Counter, defaultdict
import copy
import ctypes
import errno
import fcntl
import hashlib
import json
import os
from pathlib import Path
import select
import stat
import sys
from typing import Any, Iterable, Mapping
import zlib


SOURCE_BASENAME = "cm2_round306c79g_true_global_no_producer_consumer_independent_verifier_assembler_authority_consumer_v16r2r63y_repair_semantic_source.py"
COLD_EXEC_FD_ENV = "CM2_C79G_V16R2_COLD_EXEC_FD"
COLD_SOURCE_FD_ENV = "CM2_C79G_V16R2_COLD_SOURCE_FD"
COLD_WORKSPACE_ROOT_ENV = "CM2_C79G_V16R2_COLD_WORKSPACE_ROOT"
COLD_WORKSPACE_ROOT_FD_ENV = "CM2_C79G_V16R2_COLD_WORKSPACE_ROOT_FD"
COLD_LAUNCHER_SHA_ENV = "CM2_C79G_V16R2_COLD_LAUNCHER_FILE_SHA256"
COORDINATION_PARENT_FD_ENV = "CM2_C79G_V16R2_COORDINATION_PARENT_FD"
V10_PRODUCER_FD_ENV = "CM2_C79G_V16R2_V10_PRODUCER_FD"
V9_LAUNCHER_FD_ENV = "CM2_C79G_V16R2_V9_LAUNCHER_FD"
V11_PRODUCER_FD_ENV = "CM2_C79G_V16R2_V11_PRODUCER_FD"
V11_LAUNCHER_FD_ENV = "CM2_C79G_V16R2_V11_LAUNCHER_FD"
V11_REJECTION_FD_ENV = "CM2_C79G_V16R2_V11_REJECTION_FD"
V12_PRODUCER_FD_ENV = "CM2_C79G_V16R2_V12_PRODUCER_FD"
V12_CONSUMER_FD_ENV = "CM2_C79G_V16R2_V12_CONSUMER_FD"
V12_LAUNCHER_FD_ENV = "CM2_C79G_V16R2_V12_LAUNCHER_FD"
V5_REJECTION_FD_ENV = "CM2_C79G_V16R2_V5_REJECTION_FD"
V12_REJECTION_FD_ENV = "CM2_C79G_V16R2_V12_REJECTION_FD"
V13_PRODUCER_FD_ENV = "CM2_C79G_V16R2_V13_PRODUCER_FD"
V13_CONSUMER_FD_ENV = "CM2_C79G_V16R2_V13_CONSUMER_FD"
V13_LAUNCHER_FD_ENV = "CM2_C79G_V16R2_V13_LAUNCHER_FD"
V13_PRODUCER_PYC_FD_ENV = "CM2_C79G_V16R2_V13_PRODUCER_PYC_FD"
V13_CONSUMER_PYC_FD_ENV = "CM2_C79G_V16R2_V13_CONSUMER_PYC_FD"
V13_LAUNCHER_PYC_FD_ENV = "CM2_C79G_V16R2_V13_LAUNCHER_PYC_FD"
V13_SUPERSESSION_RECEIPT_FD_ENV = (
    "CM2_C79G_V16R2_V13_SUPERSESSION_RECEIPT_FD")
EXECUTED_SOURCE_PATH = Path(os.path.abspath(__file__))
_COLD_ROOT_TEXT = os.environ.get(COLD_WORKSPACE_ROOT_ENV)
ROOT = Path(os.path.abspath(_COLD_ROOT_TEXT)) if _COLD_ROOT_TEXT else \
    EXECUTED_SOURCE_PATH.parents[1]
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
FORMAL_GLOBAL_CLOSURE_CREDIT = 0
D02_UNLOCK = False
ACTIVE_EXACT8_FIRST_MEMBER = V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT
V16R2_DRAFT_RUNTIME_DISABLED = True
V16_DRAFT_RUNTIME_DISABLED = True
FINAL_BASE7_PINS_INSTALLED = False
FINAL_CURRENT_V16R2_PINS_INSTALLED = True
FINAL_CURRENT_V16_PINS_INSTALLED = False
ACTIVE_REJECTED_RETRY_SUPERSESSION = OUT / "cm2_round306c79g_true_global_no_producer_consumer_v16r2r62_active_predecessor_supersession_receipt_v1.json"
SELF = OUT / SOURCE_BASENAME
# Bound exactly once from the launcher-inherited workspace-root descriptor.
# Every later openat2 is anchored to this long-held dirfd; this consumer never
# reopens ROOT by pathname.
_COLD_WORKSPACE_ROOT_FD = -1
_COLD_WORKSPACE_ROOT_BEFORE: os.stat_result | None = None
_COLD_WORKSPACE_ROOT_MOUNT_ID = -1
SCHEMA = "cm2.round306c79g.true-global-no-producer-consumer.v16r2r62"
BASE = "cm2_round306c79g_true_global_no_producer_consumer_v16r2r62_semantic_source"
CONTRACT = OUT / "cm2_round306c79g_true_global_no_producer_consumer_contract_v16r2r63y_repair.json"
CLOSED_SCHEMA = OUT / "cm2_round306c79g_true_global_no_producer_consumer_schema_v16r2r62.json"
V3_OFFICIAL_REJECTION = ROOT / (
    ".cm2-runtime/c79g-v3-rejections-"
    "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab/"
    "rejection.json")
V4_REJECTION_SUPERSESSION = OUT / (
    "cm2_round306c79g_true_global_no_producer_consumer_"
    "v4_rejection_supersession_receipt_v1.json")
V5_OFFICIAL_REJECTION = ROOT / (
    ".cm2-runtime/c79g-v5-rejections-"
    "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab/"
    "rejection.json")
V6_OFFICIAL_REJECTION = ROOT / (
    ".cm2-runtime/c79g-v6-rejections-"
    "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab/"
    "rejection.json")
V7_OFFICIAL_REJECTION = ROOT / (
    ".cm2-runtime/c79g-v7-rejections-"
    "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab/"
    "rejection.json")
V8_OFFICIAL_REJECTION = ROOT / (
    ".cm2-runtime/c79g-v8-rejections-"
    "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab/"
    "rejection.json")
V9_OFFICIAL_REJECTION = ROOT / (
    ".cm2-runtime/c79g-v9-rejections-"
    "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab/"
    "rejection.json")
V10_OFFICIAL_REJECTION = ROOT / (
    ".cm2-runtime/c79g-v10-rejections-"
    "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab/"
    "rejection.json")
V11_OFFICIAL_REJECTION = ROOT / (
    ".cm2-runtime/c79g-v11-rejections-"
    "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab/"
    "rejection.json")
V12_OFFICIAL_REJECTION = ROOT / (
    ".cm2-runtime/c79g-v12-rejections-"
    "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab/"
    "rejection.json")
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
V12_FROZEN_PRODUCER = OUT / "cm2_round306c79g_true_global_no_producer_consumer_v12.py"
V12_FROZEN_CONSUMER = OUT / (
    "cm2_round306c79g_true_global_no_producer_consumer_"
    "independent_verifier_assembler_authority_consumer_v12.py")
V12_FROZEN_LAUNCHER = OUT / (
    "cm2_round306c79g_true_global_no_producer_consumer_cold_launch_v12.py")
V5_TO_V6_TRANSITION = OUT / (
    "cm2_round306c79g_true_global_no_producer_consumer_"
    "v5_to_v6_static_launch_transition_receipt_v1.json")
STATIC_AUDIT_V6 = OUT / (
    "cm2_round306c79g_true_global_no_producer_consumer_static_audit_v6.json")
V6_TO_V7_TRANSITION = OUT / (
    "cm2_round306c79g_true_global_no_producer_consumer_"
    "v6_to_v7_static_launch_transition_receipt_v1.json")
STATIC_AUDIT_V7 = OUT / (
    "cm2_round306c79g_true_global_no_producer_consumer_static_audit_v7.json")
V16_TO_V16R2_TRANSITION = OUT / "cm2_round306c79g_true_global_no_producer_consumer_v16r2r62_to_v16r2r63y_repair_static_launch_transition_receipt_v1.json"
STATIC_AUDIT_V16R2 = OUT / "cm2_round306c79g_true_global_no_producer_consumer_static_audit_v16r2r63y_repair.json"
PRODUCER_SOURCE = OUT / "cm2_round306c79g_true_global_no_producer_consumer_v16r2r63y_repair_semantic_source.py"
COLD_LAUNCHER = OUT / "cm2_round306c79g_true_global_no_producer_consumer_cold_launch_v16r2r63y_repair_semantic_source.py"
COLD_LAUNCH_MANIFEST = OUT / "cm2_round306c79g_true_global_no_producer_consumer_cold_launch_manifest_v16r2r63y_runtime_repair.sha256"
COLD_LAUNCH_OUTER = OUT / "cm2_round306c79g_true_global_no_producer_consumer_cold_launch_outer_receipt_v16r2r63y_runtime_repair.json"
# Final current-v16r2 static-freeze pins.  The historical draft sentinels remain
# explicit below so the absolute command gate proves none survived injection.
V16R2_DRAFT_RUNTIME_DISABLED = True
FINAL_CURRENT_V16R2_PINS_INSTALLED = True
CONTRACT_FILE_PIN = "1bc8e76efa96d92e7823fc93db8cd33eea5dbc693600508bfadc35cf5b61e8ac"
CONTRACT_OBJECT_PIN = "2b0d9ab2ef9e72f8bf14c20d478e80459c8b5d0fdcc7edb1e8ac95169a2d72f3"
CLOSED_SCHEMA_FILE_PIN = "1a9c03d332a1c12a34f330b30acb77b13a8f315732fc0bc75be29d3b8c3e1577"
V3_OFFICIAL_REJECTION_FILE_PIN = "57ce7a4361555c4ff403f725f17ef9cef50446a2e76d7086635c30a0f17bc62f"
V3_OFFICIAL_REJECTION_OBJECT_PIN = "c946e0d8170a75e32aa7031b42cf0dd5b7b585ba463b7b1ce0010cb65bb3b421"
V4_REJECTION_SUPERSESSION_FILE_PIN = "e3dff621fec2fa5bac14f73685c8f44ce89bc68d80b6478e0688ce926f57c183"
V4_REJECTION_SUPERSESSION_OBJECT_PIN = "1c8fc9d91be75502b0741b096a1ca6d9d59b877b1e69daada15096669215d19f"
V5_OFFICIAL_REJECTION_FILE_PIN = "c49218967b2d5023d07e5c65fa53df12f0383d6644bf4bd7d35a8e50abeb85b5"
V5_OFFICIAL_REJECTION_OBJECT_PIN = "9a94bf8b580f6145c4977dd335d9a63c69057d18d62678ab47c7916c764f8e4c"
V6_OFFICIAL_REJECTION_FILE_PIN = "3559dcfd9e6d0ebb0e093226d6d3ae8d09d67eaeb186d4ec956241af87fcbd06"
V6_OFFICIAL_REJECTION_OBJECT_PIN = "87c0cd17ae6ca3885a01da82b47b66e96419eb778594b51423eb04cf3c68f48c"
V7_OFFICIAL_REJECTION_FILE_PIN = "63d4bbc4f50ef674b6b90f6fde625ac4705d5272f500fd495111d445274ebf6b"
V7_OFFICIAL_REJECTION_OBJECT_PIN = "29c43ad51082bd56c2291dea88b619731c2853969b79ea008abea1cca3c83ecd"
V8_OFFICIAL_REJECTION_FILE_PIN = "3b00a60c6c30cc10171d82e8262f880d67aa975e9f040888a29d7bdb4014ef95"
V8_OFFICIAL_REJECTION_OBJECT_PIN = "9fbc65609f33a62751b9fc60aa4def316a499dae9e3f64e1d4ae8a3be58894d5"
V9_OFFICIAL_REJECTION_FILE_PIN = "bca8f1042a1f3ee5b82d85a2e10c6ed2bf35d486116870bf50387f9ee9dcd302"
V9_OFFICIAL_REJECTION_OBJECT_PIN = "682ead5d02c386b992c15e1e845e5e35a3147e0c1387d440c604f431c7a8b1b4"
V10_OFFICIAL_REJECTION_FILE_PIN = "1b5bbd9ec04f07e7d7d433685aa693b73bf2315a91e4813960bd5a81e8112828"
V10_OFFICIAL_REJECTION_OBJECT_PIN = "efdb614e870e70c20202834d3c6ec1a7513a3e98ba5cb4e1b32f87976a529d76"
V11_OFFICIAL_REJECTION_FILE_PIN = "f6cc10d8b7e72553ef0b7a32bbfb99255f36cce16b735002f17be58ae51d3bc8"
V11_OFFICIAL_REJECTION_OBJECT_PIN = "7ae86e38c5910bc9ceaa0a4e5cb1f8fbbf1e73de9c0314fedabbd8cb2db3bb7a"
V12_OFFICIAL_REJECTION_FILE_PIN = "b6b087a3e31b25f0bbe0ffe6caa40f3c181b2f77c5c8b6169ce3af27439762b5"
V12_OFFICIAL_REJECTION_OBJECT_PIN = "18951895ea97f455bc3294e8ef9cdaa937f3b16e9831275b047e88142e9b91f6"
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
V13_INHERITED_EXACT16_CANONICAL_SHA256 = (
    "bf70829a4632cd322ef45e9313d4150138a57f98966fcd93d2c7a718fb44f64e")
V13_INHERITED_EXACT16_CANONICAL_BYTE_LENGTH = 3_646
V13_NORMALIZED_EXACT10_CANONICAL_SHA256 = (
    "600768327003f17f0f367e64b03d0fd9ada23f2933db64845a37cfee140c61b5")
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
V14_HISTORICAL_PREDECESSOR_UNIQUE_LIVE_IDENTITY_COUNT = 105
V14_HISTORICAL_PREPUBLICATION_UNIQUE_LIVE_IDENTITY_COUNT = 113
V14_HISTORICAL_TERMINAL_UNIQUE_LIVE_IDENTITY_COUNT = 115
V14_HISTORICAL_TERMINAL_GROUP_VECTOR = (
    10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 7, 1, 3, 3, 1)
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
V14_INHERITED_AUTHORITY_EXACT12_CANONICAL_SHA256 = (
    "24e5e65f8690ad507f7590fe74b9b29702e978e0a8fb2837977e21e5b48df5cd")
V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_SCHEMA = (
    "cm2.round306c79g.true-global-no-producer-consumer."
    "v14-runtime-registry-shape-drift-rejection-supersession-receipt.v1")
V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_STATUS = (
    "FROZEN_APPEND_ONLY_V14_RUNTIME_REGISTRY_SHAPE_DRIFT_REJECTION__"
    "ZERO_CREDIT__V16R2_SUCCESSOR_ONLY")
V16_TO_V16R2_TRANSITION_KIND = (
    "APPEND_ONLY_PUBLISHED_V14_RUNTIME_FAIL_CLOSED_REJECTION_TO_"
    "ZERO_CREDIT_V16R2_CLEAN_ROOM_SUCCESSOR")
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
V16R2_CURRENT_EXACT8 = (    V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT,
    CLOSED_SCHEMA,
    CONTRACT,
    PRODUCER_SOURCE,
    SELF,
    V16_TO_V16R2_TRANSITION,
    STATIC_AUDIT_V16R2,
    COLD_LAUNCHER,
)
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

V7_PUBLICATION_LOCK_CONTINUITY_INCIDENT = {
    "D02_started": False,
    "D02_unlock": False,
    "effective_checkpoint_object_sha256": UPSTREAM_CHECKPOINT_OBJECT_PIN,
    "exact10_bytes_alone_do_not_prove_publication_acceptance": True,
    "failure_trigger":
        "LOCAL_READ_ONLY_HISTORY_REPLAY_RETURNED_NONZERO_UNDER_SET_E_LOCK_HOLDER",
    "false_extra_assumption":
        "HISTORICAL_V4_PRETTY_JSON_REQUIRED_CANONICAL_SINGLE_LINE",
    "in_lock_terminal_replay_attempt_started": True,
    "incident_fact_comes_from_publisher_control_flow_record_not_from_timestamps_alone": True,
    "incident_id":
        "V7_OFFICIAL_LOCK_RELEASED_AFTER_OUTER_BEFORE_REQUIRED_IN_LOCK_TERMINAL_REPLAY_COMPLETION",
    "later_read_only_replay_cannot_rehabilitate_v7": True,
    "object_sha256":
        "15f92090e77eda4c6acac0af759541fe47dc4f8358e15659077d6dea8071e764",
    "official_rejection_file_sha256": V7_OFFICIAL_REJECTION_FILE_PIN,
    "official_rejection_object_sha256": V7_OFFICIAL_REJECTION_OBJECT_PIN,
    "outer_frozen_and_fsynced": True,
    "outer_then_rejection_chronology_validated": True,
    "positive_runtime_surface_count": 0,
    "postincident_byte_replay_passed_but_did_not_restore_lock_continuity": True,
    "publication_lock_continuity_interrupted_after_outer_before_required_replay_completion": True,
    "publication_lock_released_on_replay_attempt_failure": True,
    "published_exact10_count": 10,
    "published_outer_file_sha256":
        "0a1fc6afe12db5c630b0c73e1fb8280140adb1590c93f176c564e4e24637584e",
    "published_outer_object_sha256":
        "8214fa50020fed7ea4046d607b1631723f660d18b3f8a2f8653f7444b02a1795",
    "required_in_lock_terminal_replay_completed": False,
    "schema":
        "cm2.round306c79g.true-global-no-producer-consumer."
        "v7-publication-lock-continuity-incident.v1",
    "v7_formal_credit_transferred": False,
    "v7_runtime_command_count": 0,
}

UNIVERSE = 76_832
BASELINE = 75_684
OVERLAY_COUNT = 1_148
LARGE_COUNT = 1_124
SINGLETON_COUNT = 24
PAIR_COUNT = 862
BASELINE_PAIRS = 288
LARGE_PAIRS = 562
SINGLETON_PAIRS = 12
PENDING_D02 = 33_638
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
    "C42_parent": 0o664, "C42_result": 0o664,
    "C42_manifest": 0o664, "C42_independent_audit": 0o600,
    "C42_installation_receipt": 0o444,
    "C42_candidate_token": 0o444, "C42_audit_token": 0o444,
    "C42_seal": 0o444, "C53_audit": 0o664, "C53_head": 0o444,
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
ATTACK_NAME_ORDER_PIN = "90ca3c45b88c754a6fd7049579afec495c576957d564047966661647cb694f9d"
V11_INCIDENT_ATTACK_NAMES = (
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
PRODUCER_SOURCE_PIN = "875d038915820c5fb8b716334b3bb592fa82c9c17d0dbd4184a9103c3f4ea0ca"
V16R2_DRAFT_CURRENT_CORE_PINS = ("dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd", "eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee", "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff", "cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc")

V12_PUBLISHED_EXACT10_FILE_SHA256_ORDER = (
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
TERMINALS = {
    "CONNECTED_TO_KNOWN", "EARLIEST_PREFIX_EXCLUDED",
    "SOURCE_GRAZING_OR_CEMETERY", "TYPED_EVENT_GRAPH",
}
LARGE_MAP = {
    "WHOLE_PUBLIC_CELL_STRICT_EXCLUSION": (
        "EARLIEST_PREFIX_EXCLUDED", "C78L_WHOLE_STRICT_TO_EARLIEST_PREFIX_EXCLUDED"),
    "EXHAUSTIVE_PUBLIC_CELL_TYPED_EVENT_C3_PARTITION": (
        "TYPED_EVENT_GRAPH", "C78L_TYPED_PARTITION_TO_TYPED_EVENT_GRAPH"),
}
SINGLETON_MAP = {
    "STRICT_EXCLUSION_ONLY": (
        "EARLIEST_PREFIX_EXCLUDED", "C78S_STRICT_ONLY_TO_EARLIEST_PREFIX_EXCLUDED"),
    "STRICT_EXCLUSION_PLUS_CEMETERY_TANGENCY": (
        "SOURCE_GRAZING_OR_CEMETERY",
        "C78S_STRICT_PLUS_CEMETERY_TO_SOURCE_GRAZING_OR_CEMETERY"),
}
CLOSURE = {"owner": True, "history": True, "glue": True,
           "two_sides": True, "incidence": True, "prefix_Kraft": True}
ZERO = {"formal_global_closure_credit": 0, "D02_unlock": False,
        "D02_gate_credit": 0, "D02_task_credit": 0,
        "D02_formal_pending_task_count": PENDING_D02, "D02_started": False}

FIXED_PATHS = {
    "C55A_LEAF": OUT / "cm2_round306c55a_four_chart_fundamental_domain_bnb_leaf_ledger_v1.json",
    "C55A_RESULT": OUT / "cm2_round306c55a_four_chart_fundamental_domain_bnb_result_v1.json",
    "C55A_VERIFY": OUT / "cm2_round306c55a_four_chart_fundamental_domain_bnb_independent_verification_v1.json",
    "C55A_MANIFEST": OUT / "cm2_round306c55a_four_chart_fundamental_domain_bnb_manifest_v1.sha256",
    "C55B_CELLS": OUT / "cm2_round306c55b_global_component_adjacency_known_sheet_cell_component_crosswalk_v1.jsonl.gz",
    "C55B_EDGES": OUT / "cm2_round306c55b_global_component_adjacency_known_sheet_component_edges_and_glue_v1.jsonl.gz",
    "C55B_COMPONENTS": OUT / "cm2_round306c55b_global_component_adjacency_known_sheet_ordinary_components_v1.jsonl.gz",
    "C55B_RESULT": OUT / "cm2_round306c55b_global_component_adjacency_known_sheet_result_v1.json",
    "C55B_VERIFY": OUT / "cm2_round306c55b_global_component_adjacency_known_sheet_independent_verification_v1.json",
    "C55B_SELFTEST": OUT / "cm2_round306c55b_global_component_adjacency_known_sheet_independent_self_test_v1.json",
    "C55B_MANIFEST": OUT / "cm2_round306c55b_global_component_adjacency_known_sheet_manifest_v1.sha256",
    "C72G_CONTRACT": OUT / "cm2_round306c72g_no_producer_global_consumer_successor_contract_v1.json",
    "C72G_VERIFY": OUT / "cm2_round306c72g_no_producer_global_consumer_successor_verification_v1.json",
    "C72G_SELFTEST": OUT / "cm2_round306c72g_no_producer_global_consumer_successor_self_test_v1.json",
    "C72G_MANIFEST": OUT / "cm2_round306c72g_no_producer_global_consumer_successor_manifest_v1.sha256",
    "C72G_OUTER": OUT / "cm2_round306c72g_no_producer_global_consumer_successor_outer_receipt_v1.json",
    "C72G_HEAD": ROOT / ".cm2-runtime/cm2-global-authority-heads/predecessor-10fb050d30c92b0f2bdcf85a30d28ff670d8efc0b48104b7f04a63c391967b41.seal",
}
FIXED_PINS = {
    "C55A_LEAF": "e80c012e3260e8f9e68d5858ba5d9dafd94611e2a1c1200d787a20e3842d8db6",
    "C55A_RESULT": "d38f39792fc944b72e70100f9f96f312b5e30e034d5104ce5f848d24378ae5af",
    "C55A_VERIFY": "6e9dfe5c50cfb104cbb8014873f69f79761b22848f50a51033fced651a121772",
    "C55A_MANIFEST": "848c56c5d328cbdf291715d1eaab2611d3af95fb8bf2875beaadcbb9ffca6e0d",
    "C55B_CELLS": "123a742ed553d89fd1026cf65c64879d9a92916492b5b583888c3312551ca2ce",
    "C55B_EDGES": "23ea0b4419f155f62d32b6b73c5a16c6f402884d333c222ff803899a58da29a0",
    "C55B_COMPONENTS": "bebc49f66efb01c0b980ec10258a60d7aead9d4d2006d28bdd169c9a9ae38a04",
    "C55B_RESULT": "6bf9cae7b4b422c5c2121f95828e1508700fe1a5d1b1128598c8617f65032a93",
    "C55B_VERIFY": "42f31f0c158b08651bec97d83d6980f0372353e71cb4f59959f186a329601bae",
    "C55B_SELFTEST": "e2e45f1a26ae73dd5e0aca08d8fa05b5b3f87fc985cf0a55b977c136948c7a15",
    "C55B_MANIFEST": "c5bd6973bd4836c3d72ae6c32961266ea12a281e4821306fbcc69be86acc45be",
    "C72G_CONTRACT": "6de59a039600f75d0b0d5722f9735fb2456f3b25b8a777df3fffef1f27e1749a",
    "C72G_VERIFY": "7e21fcca280d1f860559d9a1a4afdd2f592b717c5844fc4178fabb2e1d8b684f",
    "C72G_SELFTEST": "79935bb45848ff83db595a4b173bd2df12925be09fa4c3be66dabcdd5453b058",
    "C72G_MANIFEST": "fa77aff4fee070710fb9daf3d229182fb9f14f6b3e7a2534bb728ea91f5a51a7",
    "C72G_OUTER": "de70ab6c7c621e768662055f96a552d5cb4aaae123d4dd82b56ceed926fa68ee",
    "C72G_HEAD": "f62483c87df4b6f4a8a2ad8dcf56febbfce9977200ce94a0ad6ce38e736aeeb3",
}
FIXED_OBJECTS = {
    "C55A_LEAF": "7dd4c19cfb2b9f8cd30a4a9a23e30f11734e856cc6cc5a04e9a169c051059d90",
    "C55A_RESULT": "93b732cd65be4453e7b29379d7f70d8c849057d5bcba5489e1f6c4dd705972e3",
    "C55A_VERIFY": "cd6e3915f1dd89d8eef0766b4a806bc8a22244f348162af72fd009b98368d623",
    "C55B_RESULT": "1ce396e9746d3c0364325e8308e94c9dcd4a3bfbba8c17a9c9961915e807cc56",
    "C55B_VERIFY": "350f076a3dcfaa4424bfb27f2730e876d0f6159baa033c7aafbfaded8c870a68",
    "C55B_SELFTEST": "665cb4eea435b367e8c261788c0c6fe30620b2f0f66f6cd618976500ada1ef01",
    "C72G_CONTRACT": "5b2784b7f033ba4dde0a3d7f30af05ba4a71fb64bd6bf9fe34b64c48cc976b51",
    "C72G_VERIFY": "cd259985de0d2c43d5ad030843fc8116204c6f1cbcce1e18eea44137fe62c62d",
    "C72G_SELFTEST": "0ac9d83cc5e08dae3d0aabeddc2bf0fa665af0bc31c382ff20543c31ec64e0c1",
    "C72G_OUTER": "6380e5bf80dc2063bce5632fa73389dd07f4fe175c6c4b54a2661516d712fa92",
    "C72G_HEAD": "cb90ab914c3b6518384669f42d05df33c21a717596190131c6a0f5683934cbfb",
}

HISTORICAL_FIXED_EXPECTED_MODES = {
    FIXED_PATHS["C55A_LEAF"]: 0o444,
    FIXED_PATHS["C55A_RESULT"]: 0o444,
    FIXED_PATHS["C55A_VERIFY"]: 0o444,
    FIXED_PATHS["C55A_MANIFEST"]: 0o664,
    **{FIXED_PATHS[key]: 0o664 for key in (
        "C55B_CELLS", "C55B_EDGES", "C55B_COMPONENTS", "C55B_RESULT",
        "C55B_VERIFY", "C55B_SELFTEST", "C55B_MANIFEST")},
    FIXED_PATHS["C72G_CONTRACT"]: 0o664,
    FIXED_PATHS["C72G_VERIFY"]: 0o644,
    FIXED_PATHS["C72G_SELFTEST"]: 0o644,
    FIXED_PATHS["C72G_MANIFEST"]: 0o644,
    FIXED_PATHS["C72G_OUTER"]: 0o644,
    FIXED_PATHS["C72G_HEAD"]: 0o444,
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
C78L_VERIFY_FILE = "22223e2aca6eaa069cfda7ab95da5f31b6adb36773544f9f2034bd01c6d1f0c1"
C78L_VERIFY_OBJECT = "850eba67fb2d343e8b607394469c8d2febf47229b26d86c6894249fd060c1419"
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
C78L_RESULT_OBJECT = "bfee46ce15d46718326881fce97cbca7ff10df459732a789b314928ca7c62204"
C78L_COMPLETION_OBJECT = "4b627b9e05d4552ce1a5c55c31a2e9dc11e3e5067657691e0b3fdfdf53562cfe"
C78L_COMPLETION_OUTER_OBJECT = "d67abd63ffabefddcb7829cb781dc038a00498686726e54d806db10f3c2fc4a9"

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
MANIFEST = BASE + "_candidate_manifest.sha256"
OUTER_RECEIPT = BASE + "_candidate_outer_receipt.json"
MEMBERS = (LOCK, OVERLAY, SUCCESSOR, PARENTS, REGISTRY, RESULT, REPORT, MANIFEST, OUTER_RECEIPT)
VERIFICATION_FILE = BASE + "_independent_verification_v16r2.json"
COMPLETION_VERIFICATION = "cm2_round306c79g_true_global_no_producer_consumer_completion_verification_copy_v16r2.json"
COMPLETION_RECEIPT = "cm2_round306c79g_true_global_no_producer_consumer_pre_outer_completion_receipt_v16r2.json"
GLOBAL_MANIFEST = "cm2_round306c79g_true_global_no_producer_consumer_one_global_manifest_v16r2.sha256"
FINAL_OUTER = "cm2_round306c79g_true_global_no_producer_consumer_cold_launch_outer_receipt_v16r2r63y_runtime_repair.json"
COMPLETION_MEMBERS = (COMPLETION_VERIFICATION, COMPLETION_RECEIPT, GLOBAL_MANIFEST, FINAL_OUTER)

RUNTIME = ROOT / ".cm2-runtime"
CANDIDATE_A = RUNTIME / ("c79g-v16r2r63y-candidate-a-" + UPSTREAM_CHECKPOINT_OBJECT_PIN)
CANDIDATE_B = RUNTIME / ("c79g-v16r2r63y-candidate-b-" + UPSTREAM_CHECKPOINT_OBJECT_PIN)
VERIFICATION_A = RUNTIME / ("c79g-v16r2r63y-verification-a-" + UPSTREAM_CHECKPOINT_OBJECT_PIN)
VERIFICATION_B = RUNTIME / ("c79g-v16r2r63y-verification-b-" + UPSTREAM_CHECKPOINT_OBJECT_PIN)
COMMITTED_COMPLETION = RUNTIME / ("c79g-v16r2r63y-committed-completion-" + UPSTREAM_CHECKPOINT_OBJECT_PIN)
AUTHORITY_HEADS = RUNTIME / "cm2-global-authority-heads"
AUTHORITY_SEAL = AUTHORITY_HEADS / ("c79g-v16r2r63y-" + UPSTREAM_CHECKPOINT_OBJECT_PIN + ".seal")
REJECTION_NAMESPACE = RUNTIME / ("c79g-v16r2r63y-rejections-" + UPSTREAM_CHECKPOINT_OBJECT_PIN)
LATER_REJECTION = REJECTION_NAMESPACE / "rejection.json"
COMPLETION_STAGE_PREFIX = ".c79g-v16r2r63y-completion-stage-"
AUTHORITY_STAGE_PREFIX = ".c79g-v16r2r63y-authority-stage-"
VERIFICATION_STAGE_A = RUNTIME / (
    ".c79g-v16r2r63y-verification-stage-a-" + UPSTREAM_CHECKPOINT_OBJECT_PIN)
VERIFICATION_STAGE_B = RUNTIME / (
    ".c79g-v16r2r63y-verification-stage-b-" + UPSTREAM_CHECKPOINT_OBJECT_PIN)
CANDIDATE_STAGE_A = RUNTIME / (
    ".c79g-v16r2r63y-candidate-stage-a-" + UPSTREAM_CHECKPOINT_OBJECT_PIN)
CANDIDATE_STAGE_B = RUNTIME / (
    ".c79g-v16r2r63y-candidate-stage-b-" + UPSTREAM_CHECKPOINT_OBJECT_PIN)
COMPLETION_STAGE = RUNTIME / (COMPLETION_STAGE_PREFIX + UPSTREAM_CHECKPOINT_OBJECT_PIN)
AUTHORITY_STAGE = AUTHORITY_HEADS / (
    AUTHORITY_STAGE_PREFIX + UPSTREAM_CHECKPOINT_OBJECT_PIN + ".seal")

AUTHORITY_SEAL_SCHEMA = "cm2.round306c79g.true-global-no-producer-consumer.v16r2.authority-seal"
PRESEAL_SCHEMA = "cm2.round306c79g.true-global-no-producer-consumer.v16r2.preseal-committed-surface"
INNER_ROOT_SCHEMA = "cm2.round306c79g.true-global-no-producer-consumer.v16r2.inner-composite"
LATER_REJECTION_SCHEMA = "cm2.round306c79g.true-global-no-producer-consumer.v16r2.later-rejection"
LATER_REJECTION_REASON = "ORPHANED_OR_INCOMPLETE_C79G_V16R2_SURFACE"
COLD_ROOT_SCHEMA = "cm2.round306c79g.true-global-no-producer-consumer.v16r2.cold-launched-committed-authority"
LIVE_PROTOCOL = "CM2_C79G_V16R2_COLD_TWO_PHASE_LIVE_ACK_V1"
LIVE_REQUEST_SCHEMA = "cm2.round306c79g.true-global-no-producer-consumer.v16r2.cold-live-commit-request"
LIVE_ACK_SCHEMA = "cm2.round306c79g.true-global-no-producer-consumer.v16r2.cold-live-ack"
LIVE_RELEASE_SCHEMA = "cm2.round306c79g.true-global-no-producer-consumer.v16r2.cold-live-release"
PREWRAPPER_BODY_DOMAIN = "CM2_C79G_V16R2_COLD_PREWRAPPER_BODY_V1"
TRANSACTION_BINDING_DOMAIN = "CM2_C79G_V16R2_COLD_TRANSACTION_BINDING_V1"
LIVE_ACK_BINDING_DOMAIN = "CM2_C79G_V16R2_COLD_LIVE_ACK_BINDING_V1"
V3_FROZEN_FILES = {
    "v2_rejection_supersession":
        (OUT / "cm2_round306c79g_true_global_no_producer_consumer_v2_rejection_supersession_receipt_v1.json",
         "fdd1921afda98a34c87ae20094e60fca1b75c8f233cf37890e7817fe35d82408"),
    "closed_schema":
        (OUT / "cm2_round306c79g_true_global_no_producer_consumer_schema_v3.json",
         "275a86286480f915af69e18d81d7032140e3db6982d32679206a6a5b88fee036"),
    "contract":
        (OUT / "cm2_round306c79g_true_global_no_producer_consumer_contract_v3.json",
         "ee2a969b5d3ae28dfc116fc24ab6bee6c3983d64db183641981108481c05ae7d"),
    "build_only_producer":
        (OUT / "cm2_round306c79g_true_global_no_producer_consumer_v3.py",
         "587933a52505488fd87b1c4f99d5659df6f3c3e9557c0a77edd642e6e4dde0ab"),
    "independent_consumer":
        (OUT / "cm2_round306c79g_true_global_no_producer_consumer_independent_verifier_assembler_authority_consumer_v3.py",
         "d66143d32f4c4257041f03e24e4a4da8f15542853b2a8f47fa39f5b72871bfdd"),
    "transition":
        (OUT / "cm2_round306c79g_true_global_no_producer_consumer_v2_to_v3_static_launch_transition_receipt_v1.json",
         "d2c0a78db1ae19ccb21f068c4c4f9337220cabbf16721fdc15ed41825a6f3374"),
    "static_audit":
        (OUT / "cm2_round306c79g_true_global_no_producer_consumer_static_audit_v3.json",
         "b7c3732296df713b6588527284983fab758e225c17c51fbc4a38b1f43da8aece"),
    "cold_launcher":
        (OUT / "cm2_round306c79g_true_global_no_producer_consumer_cold_launch_v3.py",
         "63e1b04ce152770ce4bcfda826d418414fd3196ba540752d0bd61a97eec0075b"),
    "cold_manifest":
        (OUT / "cm2_round306c79g_true_global_no_producer_consumer_cold_launch_manifest_v3.sha256",
         "53c97fc8f01f0dc0de3f7c5729d5940587467a1877ef9a7c96e9ea2403c0b028"),
    "cold_outer":
        (OUT / "cm2_round306c79g_true_global_no_producer_consumer_cold_launch_outer_receipt_v3.json",
         "692608ca777ca9ee625e2044bc71f694edf893f51953d7ff5662f29264d245ea"),
}
V3_EXACT10_ORDER = (
    "v2_rejection_supersession", "closed_schema", "contract",
    "build_only_producer", "independent_consumer", "transition",
    "static_audit", "cold_launcher", "cold_manifest", "cold_outer",
)
V3_FROZEN_OBJECTS = {
    "v2_rejection_supersession":
        "518cbc5b30fc62d55291feef407c5677b880a05cb9a5b9f51404c79381c648fa",
    "contract": "fe82dcf80e8dd856390b694e8a286abc3087f33d0a2b4bebda1a01836b796a6b",
    "transition": "fabe51379dc16bd4177d2116a43f2d1d5c103cc5a53f845fd5397eae0ea1c25b",
    "static_audit": "2ef7588e66a83944fee0e2044177445f15b71fe030871ca96f354ce65dc8499a",
    "cold_outer": "450e1551a9f3cac2529bd202aa63ad28e4fd7e2ec4c7d7fb415883840ca0143d",
}
V4_REJECTED_FILES = {
    "closed_schema_v4":
        (OUT / "cm2_round306c79g_true_global_no_producer_consumer_schema_v4.json",
         "b2cb58e88b66daed7d0449d11a4441095179b7e537a48a35ee9c630f76beca6a"),
    "contract_v4":
        (OUT / "cm2_round306c79g_true_global_no_producer_consumer_contract_v4.json",
         "84608ada466fb9aa3d99adfd34662e9af02dfd009d8eb185374c065a6da0c23c"),
    "build_only_producer_v4":
        (OUT / "cm2_round306c79g_true_global_no_producer_consumer_v4.py",
         "968e401852f45d5104f48526b50d4f59a86bb1fed8e7af23782c5f6d447d1cf1"),
    "independent_consumer_v4":
        (OUT / "cm2_round306c79g_true_global_no_producer_consumer_"
               "independent_verifier_assembler_authority_consumer_v4.py",
         "23753584725365cdc0174d518c26b7d8dbdeb12eea2345a5e3b281274548420c"),
    "transition_v3_to_v4":
        (OUT / "cm2_round306c79g_true_global_no_producer_consumer_"
               "v3_to_v4_static_launch_transition_receipt_v1.json",
         "4c46f7cf8eaba93fd1b9562c288c2117b49d7c8cdeb62482b93c5e247d412256"),
    "static_audit_v4":
        (OUT / "cm2_round306c79g_true_global_no_producer_consumer_static_audit_v4.json",
         "5efa44ae5cf78000940a4640a98ac0fe486e1946aecc9d20e7023e27ed13049c"),
    "cold_launcher_v4":
        (OUT / "cm2_round306c79g_true_global_no_producer_consumer_cold_launch_v4.py",
         "04617c7ac60ad4cee278ac1b4c7d154fd130a3e2225a691ef9a75ad644a062a3"),
}
V4_REJECTED_OBJECTS = {
    "contract_v4": "62609ff0809ba9439be07a215ece772262f30ead7d87fda92a6e4e23bb5895b7",
    "transition_v3_to_v4":
        "d2d0797a6edb8463f9af7007e28356932472f2e0478fb73b35869d3f51184129",
    "static_audit_v4":
        "489a0aad575872e79dc264d5fc45cf2f12903c4c990f25d15a9cdd1448e980f4",
}
V5_FROZEN_FILES = {
    "v4_rejection_supersession":
        (V4_REJECTION_SUPERSESSION,
         V4_REJECTION_SUPERSESSION_FILE_PIN),
    "closed_schema_v5":
        (OUT / "cm2_round306c79g_true_global_no_producer_consumer_schema_v5.json",
         "1048740103257351abb1266ed91bb80028436cb1497918a0f0f177ec3268ff4f"),
    "contract_v5":
        (OUT / "cm2_round306c79g_true_global_no_producer_consumer_contract_v5.json",
         "162cd554ea972b434c019924a9ab8b87621ab65aae7d4896b6dac72d6288b997"),
    "build_only_producer_v5":
        (OUT / "cm2_round306c79g_true_global_no_producer_consumer_v5.py",
         "bc6d48903f61257cd75b20b83c6cd369ca3748d19427cf18129c0fb9bb59e76e"),
    "independent_consumer_v5":
        (OUT / "cm2_round306c79g_true_global_no_producer_consumer_"
               "independent_verifier_assembler_authority_consumer_v5.py",
         "03aed000a94fc7b7d7e68d3c55611bcc55e7ce293f65ddfb3be7709e44fc854d"),
    "transition_v4_to_v5":
        (OUT / "cm2_round306c79g_true_global_no_producer_consumer_"
               "v4_to_v5_static_launch_transition_receipt_v1.json",
         "6784668e91a4a4cc0812c6405cb1df8c10ad90e40daf321ac75c16cadd5cd715"),
    "static_audit_v5":
        (OUT / "cm2_round306c79g_true_global_no_producer_consumer_static_audit_v5.json",
         "b852a41aaa992b85abec5f7139dc4669d2f1fe38bd79ab8ab812453c5cfca4f0"),
    "cold_launcher_v5":
        (OUT / "cm2_round306c79g_true_global_no_producer_consumer_cold_launch_v5.py",
         "889775cfbe1d3cba597c85c28765545805710c99f06ad05673e57b7b7627bc54"),
    "cold_manifest_v5":
        (OUT / "cm2_round306c79g_true_global_no_producer_consumer_"
               "cold_launch_manifest_v5.sha256",
         "55336d5a95e1765cc0f229bbc98ddfb1f6c14218f5b5e619f84d19da39961474"),
    "cold_outer_v5":
        (OUT / "cm2_round306c79g_true_global_no_producer_consumer_"
               "cold_launch_outer_receipt_v5.json",
         "71b7eaca4af58a34b70bb751044bd09d0e40352a1dc6f016a0c7618b6d4b4ab8"),
}
V5_EXACT10_ORDER = (
    "v4_rejection_supersession", "closed_schema_v5", "contract_v5",
    "build_only_producer_v5", "independent_consumer_v5",
    "transition_v4_to_v5", "static_audit_v5", "cold_launcher_v5",
    "cold_manifest_v5", "cold_outer_v5",
)
V5_FROZEN_OBJECTS = {
    "v4_rejection_supersession": V4_REJECTION_SUPERSESSION_OBJECT_PIN,
    "contract_v5":
        "27d457a583f4d9892e0a866917ea4add25ff677669ee814861e0608036189377",
    "transition_v4_to_v5":
        "0678e3b81d5a4f6088967613df0cd585910b9b26800dfbf1724b637fc7c43526",
    "static_audit_v5":
        "ba9bf728ce08b795b5dd92191f2ccac3b2cfbc6ef7f7b919379feb6b9557e546",
    "cold_outer_v5":
        "57d5c31bf232d725e661932d2d210b31d1125cd0877a74a8167451bbbdaf0e1c",
}
V5_STRICT_BOOL_RISK_IDS = [
    "V5_LAUNCHER_SCHEMA_DEFS_NAME_NON_BOOL",
    "V5_LAUNCHER_SCHEMA_PROPERTY_NAME_NON_BOOL",
    "V5_CONSUMER_ATTACK_PATCH_NON_BOOL",
    "V5_PRODUCER_RELATIVE_PARTS_NON_BOOL_SHORT_CIRCUIT",
    "V5_CONSUMER_RELATIVE_PARTS_NON_BOOL_SHORT_CIRCUIT",
    "V5_LAUNCHER_RELATIVE_PARTS_NON_BOOL_SHORT_CIRCUIT",
    "V5_LAUNCHER_RELATIVE_BYTES_NON_BOOL_SHORT_CIRCUIT",
]

# The complete published v6 cold root is the direct append-only predecessor.
# Its producer, consumer, and launcher are executable source files and are held
# strictly with O_PATH metadata descriptors; their file pins are cross-bound by
# the readable transition/audit/manifest/outer evidence.  In particular, no
# predecessor producer byte is content-opened by this consumer.
V6_FROZEN_FILES = {
    "v5_official_rejection":
        (V5_OFFICIAL_REJECTION, V5_OFFICIAL_REJECTION_FILE_PIN),
    "closed_schema_v6":
        (OUT / "cm2_round306c79g_true_global_no_producer_consumer_schema_v6.json",
         "250e27777e3ffdaf159a19c00ae683a4ef079f6e785f0b37d003a724099419bc"),
    "contract_v6":
        (OUT / "cm2_round306c79g_true_global_no_producer_consumer_contract_v6.json",
         "6e4f7f4693b759397c8775f8d943048c867b3c460c27f5cb3d9681a0fefee30c"),
    "build_only_producer_v6":
        (OUT / "cm2_round306c79g_true_global_no_producer_consumer_v6.py",
         "f48982effd6a1068c50260d0d419b281a3fa8c614e4ca76c3b8ee2a48e8afb56"),
    "independent_consumer_v6":
        (OUT / "cm2_round306c79g_true_global_no_producer_consumer_"
               "independent_verifier_assembler_authority_consumer_v6.py",
         "af4875d2ab84101b05eff9811f33d8bf7b1a060720a956ae3fb42d8d466f4775"),
    "transition_v5_to_v6":
        (V5_TO_V6_TRANSITION,
         "a6ac971e7efd9a6a80c7055449fb6c4ef02b77d3e8303324104a060618d45569"),
    "static_audit_v6":
        (STATIC_AUDIT_V6,
         "f4f5b3ea2c289f388da9cc7d4181c0f1d6cf692aae0b85cbb17533ca4131f474"),
    "cold_launcher_v6":
        (OUT / "cm2_round306c79g_true_global_no_producer_consumer_cold_launch_v6.py",
         "796cbb3c0a4a2a5f3801f9a9132421112fc19e81272938092edd3014ef031fcb"),
    "cold_manifest_v6":
        (OUT / "cm2_round306c79g_true_global_no_producer_consumer_"
               "cold_launch_manifest_v6.sha256",
         "281232171e4c2713f81122e731bd4d50e95afef6bdbd2a5040f5e93c3b7171ea"),
    "cold_outer_v6":
        (OUT / "cm2_round306c79g_true_global_no_producer_consumer_"
               "cold_launch_outer_receipt_v6.json",
         "e37cce305826fb2149798a125a12b3880070fca5f338b6508beeea947c2854bd"),
}
V6_EXACT10_ORDER = (
    "v5_official_rejection", "closed_schema_v6", "contract_v6",
    "build_only_producer_v6", "independent_consumer_v6",
    "transition_v5_to_v6", "static_audit_v6", "cold_launcher_v6",
    "cold_manifest_v6", "cold_outer_v6",
)
V6_FROZEN_OBJECTS = {
    "v5_official_rejection": V5_OFFICIAL_REJECTION_OBJECT_PIN,
    "contract_v6":
        "58ae6e3c9912294cc89b6804741e56b373a143d16a5fa2547325989fa1af2546",
    "transition_v5_to_v6":
        "edb97beae5ca5cfeff9e549c017892d6381d3b5a01be16b12e7e52e06d09c5e1",
    "static_audit_v6":
        "2478b44d085336b87d13e309dc4416e58a85ef6ae28eb89cd787ea95b07c0449",
    "cold_outer_v6":
        "423621bbe2115183a54dc0161abdbdc964f09af31efb39eee40f46bc81bbe251",
}

# The complete published v7 cold root is retained as immutable rejected
# history.  Its official later rejection is the first member of the current
# v16r2 base7 and is therefore shared with the current static-policy holder.  The
# three executable predecessor sources are metadata-only O_PATH holds here.
V7_FROZEN_FILES = {
    "v6_official_rejection":
        (V6_OFFICIAL_REJECTION, V6_OFFICIAL_REJECTION_FILE_PIN),
    "closed_schema_v7":
        (OUT / "cm2_round306c79g_true_global_no_producer_consumer_schema_v7.json",
         "edcdbb568044d04fc7c86b4c4e64fdb7b12b3841f1e93092694ebc3177b6fe18"),
    "contract_v7":
        (OUT / "cm2_round306c79g_true_global_no_producer_consumer_contract_v7.json",
         "041ca2567f81c148f765dd85e3515a6ac01295bca06c3032b027459eceb2c014"),
    "build_only_producer_v7":
        (OUT / "cm2_round306c79g_true_global_no_producer_consumer_v7.py",
         "67670681481cf372f775ad39a9f8d8b2459a77ef708e2f4da14ca114ac0f0d95"),
    "independent_consumer_v7":
        (OUT / "cm2_round306c79g_true_global_no_producer_consumer_"
               "independent_verifier_assembler_authority_consumer_v7.py",
         "3ee9f2c666b7297a23faa31d39d5ea66b708d545120b1aeb93f77ac9ef704f8a"),
    "transition_v6_to_v7":
        (V6_TO_V7_TRANSITION,
         "e732442e16a3a1f66629562af4cae72d9ae3e78b511f67ee22aa84869b90bec8"),
    "static_audit_v7":
        (STATIC_AUDIT_V7,
         "74c72540bd66b5929fa30ec554207db21f40999484752340f0294590d407a667"),
    "cold_launcher_v7":
        (OUT / "cm2_round306c79g_true_global_no_producer_consumer_cold_launch_v7.py",
         "93404ad229728b682018ad236075b6c789e12ee4bf043426049e2aa501b2b9e0"),
    "cold_manifest_v7":
        (OUT / "cm2_round306c79g_true_global_no_producer_consumer_"
               "cold_launch_manifest_v7.sha256",
         "eeabe5d52504231a6163b0e057e9129b632b8a4c33a18fc3a3ac4576612de80c"),
    "cold_outer_v7":
        (OUT / "cm2_round306c79g_true_global_no_producer_consumer_"
               "cold_launch_outer_receipt_v7.json",
         "0a1fc6afe12db5c630b0c73e1fb8280140adb1590c93f176c564e4e24637584e"),
}
V7_EXACT10_ORDER = (
    "v6_official_rejection", "closed_schema_v7", "contract_v7",
    "build_only_producer_v7", "independent_consumer_v7",
    "transition_v6_to_v7", "static_audit_v7", "cold_launcher_v7",
    "cold_manifest_v7", "cold_outer_v7",
)
V7_FROZEN_OBJECTS = {
    "v6_official_rejection": V6_OFFICIAL_REJECTION_OBJECT_PIN,
    "contract_v7":
        "a87f7434b32a96923ee81f7761efab9b0937f15103c2fa9b47e8402104b612a5",
    "transition_v6_to_v7":
        "0f1f240b6a61a6774991b8355c6132c1a9ae30b15690e8c058f88206db69453e",
    "static_audit_v7":
        "efd83fae1a716c864e8bb61238370e10b9ebf54444f023b902c7cef2a41a6766",
    "cold_outer_v7":
        "8214fa50020fed7ea4046d607b1631723f660d18b3f8a2f8653f7444b02a1795",
}

# Frozen v8 is the immediate append-only predecessor.  The three executable
# sources are metadata-only O_PATH holds; no verifier path may content-open,
# import, compile, or execute them.
V8_FROZEN_FILES = {
    "v7_official_rejection":
        (V7_OFFICIAL_REJECTION, V7_OFFICIAL_REJECTION_FILE_PIN),
    "closed_schema_v8":
        (OUT / "cm2_round306c79g_true_global_no_producer_consumer_schema_v8.json",
         "65904d48296a568d2cd4ec2fc49abe1a7651ca77d4a119a780fc91fb6ddaaeeb"),
    "contract_v8":
        (OUT / "cm2_round306c79g_true_global_no_producer_consumer_contract_v8.json",
         "6ddb6dd015ee9bb88c716cfb939bf2b954789effffa17b141833091a72187ca4"),
    "build_only_producer_v8":
        (OUT / "cm2_round306c79g_true_global_no_producer_consumer_v8.py",
         "93a591fc870c0fa35ed37e6e2d0f9066161988d3d340031b7ffdb7239eb2c512"),
    "independent_consumer_v8":
        (OUT / "cm2_round306c79g_true_global_no_producer_consumer_"
               "independent_verifier_assembler_authority_consumer_v8.py",
         "d9c5c56f0ae88b573812c660a64eb94dd345d7efd0257cce975752945e1240f3"),
    "transition_v7_to_v8":
        (OUT / "cm2_round306c79g_true_global_no_producer_consumer_"
               "v7_to_v8_static_launch_transition_receipt_v1.json",
         "92c7b1473bdced6426b0e52a4b29d181d4153fc1174ae7709469a7552bfd3524"),
    "static_audit_v8":
        (OUT / "cm2_round306c79g_true_global_no_producer_consumer_static_audit_v8.json",
         "b467b7eea54a0d208ff560677929e15d14304f044016e858b9a267f6c5dab8dd"),
    "cold_launcher_v8":
        (OUT / "cm2_round306c79g_true_global_no_producer_consumer_cold_launch_v8.py",
         "169866df2d418c3ccb467ef2b678d322584910500cdeee9dd2b40d8564de3d1e"),
    "cold_manifest_v8":
        (OUT / "cm2_round306c79g_true_global_no_producer_consumer_"
               "cold_launch_manifest_v8.sha256",
         "ae6e4998d6b347902b3e1ab5256abb6f9ab62d5feabf63a597a28e881068365f"),
    "cold_outer_v8":
        (OUT / "cm2_round306c79g_true_global_no_producer_consumer_"
               "cold_launch_outer_receipt_v8.json",
         "bc1f7d4c4c8cd2d5ade666ba71e920532651266a9e733b361dfa979b7a0e446f"),
}
V8_EXACT10_ORDER = (
    "v7_official_rejection", "closed_schema_v8", "contract_v8",
    "build_only_producer_v8", "independent_consumer_v8",
    "transition_v7_to_v8", "static_audit_v8", "cold_launcher_v8",
    "cold_manifest_v8", "cold_outer_v8",
)
V8_FROZEN_OBJECTS = {
    "v7_official_rejection": V7_OFFICIAL_REJECTION_OBJECT_PIN,
    "contract_v8":
        "0bb6634778bf50a9f090d5df7b23358cae30769ce9b2fb87119800f38a1b75c0",
    "transition_v7_to_v8":
        "679920565b320b2bfb94f431902cac93a2af1ce506b725f0e3ea88ec1a59ae96",
    "static_audit_v8":
        "8138cb5c1c99cb737ae50ff61c1a56efad6ac202889719d22d12997d1e0b6bb0",
    "cold_outer_v8":
        "35c63aebeb08cf93339f01d3cc05c9552cbf0bffa50010ce60d4350990f3181d",
}
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

# Frozen v9 publication identities use O_PATH metadata holds.  Its launcher
# bytes have the sole explicit read-only exception through the inherited
# incident-authority fd used by the exact40 helper.
V9_FROZEN_FILES = {
    "v8_official_rejection":
        (V8_OFFICIAL_REJECTION, V8_OFFICIAL_REJECTION_FILE_PIN),
    "closed_schema_v9":
        (OUT / "cm2_round306c79g_true_global_no_producer_consumer_schema_v9.json",
         "2ddd254e43a196bb550fce69552c7f51eae063f4a9b75bc5818099c93335080b"),
    "contract_v9":
        (OUT / "cm2_round306c79g_true_global_no_producer_consumer_contract_v9.json",
         "c37676119597f235f94104a55095c07e292fdd5c373c1811eeeed10c1b3d333f"),
    "build_only_producer_v9":
        (OUT / "cm2_round306c79g_true_global_no_producer_consumer_v9.py",
         "e3dfcf7d2bda8daaeaf1412685909a1a96e1ff88f8d3c6ab1645288ee97c5a70"),
    "independent_consumer_v9":
        (OUT / "cm2_round306c79g_true_global_no_producer_consumer_"
               "independent_verifier_assembler_authority_consumer_v9.py",
         "0b38317123f88dc5f065603e51f63171ac0fcd3760de758cd1aa50544f8d3c97"),
    "transition_v8_to_v9":
        (OUT / "cm2_round306c79g_true_global_no_producer_consumer_"
               "v8_to_v9_static_launch_transition_receipt_v1.json",
         "ff4b42e258fec6cdd68d3c24f4903c9f3c2cec1ed2dc8f19dca703bddb45c522"),
    "static_audit_v9":
        (OUT / "cm2_round306c79g_true_global_no_producer_consumer_static_audit_v9.json",
         "1c272852c18bff065a6b641d9c1f2a1c5a0da6db2a6e86a20588acb2be843571"),
    "cold_launcher_v9":
        (OUT / "cm2_round306c79g_true_global_no_producer_consumer_cold_launch_v9.py",
         "f7559ceeb7d491b8489812670392cb63e3cd5f6a2764db469e2dd51d6b5577fa"),
    "cold_manifest_v9":
        (OUT / "cm2_round306c79g_true_global_no_producer_consumer_"
               "cold_launch_manifest_v9.sha256",
         "648f3dce04ca5fdfed8635e0f8c0d21c09404b3799dbfd108e92013fab5392a4"),
    "cold_outer_v9":
        (OUT / "cm2_round306c79g_true_global_no_producer_consumer_"
               "cold_launch_outer_receipt_v9.json",
         "498a2d3c46c091f3a218c835bef0557b783401e81bb30dfb131562c23027b28b"),
}
V9_EXACT10_ORDER = (
    "v8_official_rejection", "closed_schema_v9", "contract_v9",
    "build_only_producer_v9", "independent_consumer_v9",
    "transition_v8_to_v9", "static_audit_v9", "cold_launcher_v9",
    "cold_manifest_v9", "cold_outer_v9",
)
V9_FROZEN_OBJECTS = {
    "v8_official_rejection": V8_OFFICIAL_REJECTION_OBJECT_PIN,
    "contract_v9":
        "9a5fc94e11a30099ea0e23a574394399842efb8b350c98e9c16c5e8a8ce3963a",
    "transition_v8_to_v9":
        "618f560f9ebbaaa5442af66af11f2efa7e4fe110a4f9cb586e3ab4424a1f95dc",
    "static_audit_v9":
        "39463fbf2fb1c12ec68e4802b3ecd7dc48a95a2af6fcfe3430a27a0cb6ef9f4e",
    "cold_outer_v9":
        "7df5cfed652b2696fa63387b9d471cd1947f90dd269c4e7846ffa0f6641ad6be",
}
V9_FIRST_RUNTIME_ATTEMPT = {
    "attempted": True,
    "producer_child_spawned": False,
    "candidate_write_started": False,
    "positive_runtime_surface_count": 0,
    "aborted_by_v6_defect_shape_drift_guard": True,
}
V9_V6_PERSISTED_PROOF_SHA256 = (
    "827bff2782109ae7aa905b4a8f5d25ac37cd814cef34cbee531a25fad4b1abc0")
V9_V6_PERSISTED_DEFECT_SHA256 = (
    "8dce2a1ea02dc47b3158540547b97810ee3e0ad5adfc5b4849f275fc4ac0407f")
V9_V6_LAUNCHER_EXPANDED_PROOF_SHA256 = (
    "7f3cc1b44f157b8a7ab981d0918e0cf83cb93c49661173a104489deecd38371a")
V9_V6_LAUNCHER_EXPANDED_DEFECT_SHA256 = (
    "d6ac736b4a8e72deef40cf5573545285440b2102e48f9bf6ea2cbcb6fe46a068")
V9_V6_HELD_SELF_IDENTITY_DEFECT_SHAPE_DRIFT_INCIDENT = {
    "schema":
        "cm2.round306c79g.true-global-no-producer-consumer."
        "v9-v6-held-self-defect-shape-drift-incident.v1",
    "incident_id":
        "V9_LAUNCHER_EXPANDED_V6_PERSISTED_DEFECT_PAYLOAD_16_KEYS_VERSUS_"
        "CONTRACT_CANONICAL_9_KEYS",
    "evidence_source":
        "FROZEN_V9_LAUNCHER_CONTROL_FLOW_AND_FIRST_RUNTIME_STDERR",
    "failure_label":
        "exact v6 exact10, rejection, spawned-before-write and "
        "HeldSelf.identity defect regression",
    "persisted_held_self_identity_defect_exact_key_count": 9,
    "persisted_held_self_identity_defect": {
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
        },
    "launcher_expanded_structural_evidence_exact_key_count": 16,
    "launcher_expanded_structural_evidence": {
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
    },
    "contract_v9_predecessor_v6_full_canonical_sha256":
        V9_V6_PERSISTED_PROOF_SHA256,
    "contract_v9_persisted_defect_nested_canonical_sha256":
        V9_V6_PERSISTED_DEFECT_SHA256,
    "launcher_v9_predecessor_v6_full_canonical_sha256":
        V9_V6_LAUNCHER_EXPANDED_PROOF_SHA256,
    "launcher_v9_expanded_defect_nested_canonical_sha256":
        V9_V6_LAUNCHER_EXPANDED_DEFECT_SHA256,
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


# Frozen v10 is an append-only predecessor.  Its ordinary publication identity
# remains an O_PATH metadata hold; its producer bytes are additionally consumed
# only from the launcher-inherited incident-authority fd for exact40 rederivation.
V10_FROZEN_FILES = {
    "v9_official_rejection":
        (V9_OFFICIAL_REJECTION, V9_OFFICIAL_REJECTION_FILE_PIN),
    "closed_schema_v10":
        (OUT / "cm2_round306c79g_true_global_no_producer_consumer_schema_v10.json",
         "a42dc06e276cc9206b29ec22df74ac7f8d76a4afb1de30115d048e1f7ce52801"),
    "contract_v10":
        (OUT / "cm2_round306c79g_true_global_no_producer_consumer_contract_v10.json",
         "e9f9387c191ff7d34a75f73331d4926c989e0bcc641e21c6a3ace58fc5a7d479"),
    "build_only_producer_v10":
        (OUT / "cm2_round306c79g_true_global_no_producer_consumer_v10.py",
         "99bb321da8a63855e52c8d6757d00886c0deeb2182f5044cac35f645e2ebd00a"),
    "independent_consumer_v10":
        (OUT / "cm2_round306c79g_true_global_no_producer_consumer_"
               "independent_verifier_assembler_authority_consumer_v10.py",
         "3a72bba8930f15a66fa1111c76b9c3b6b2b9a2d21db32093d64d0c68a9f6d708"),
    "transition_v9_to_v10":
        (OUT / "cm2_round306c79g_true_global_no_producer_consumer_"
               "v9_to_v10_static_launch_transition_receipt_v1.json",
         "6fe81931ee2051148e8ce0b7e67fcc45e56b992db7c74307f95aa9cc9dac6643"),
    "static_audit_v10":
        (OUT / "cm2_round306c79g_true_global_no_producer_consumer_static_audit_v10.json",
         "e8a3f0497451689ec0835bb4048fe7be69fee4926e40620cdd128cc7b55ffb71"),
    "cold_launcher_v10":
        (OUT / "cm2_round306c79g_true_global_no_producer_consumer_cold_launch_v10.py",
         "629347f42bcfd2eca3d9e38d29eb3bea66ff9abd48ec16867040c74e81e9134c"),
    "cold_manifest_v10":
        (OUT / "cm2_round306c79g_true_global_no_producer_consumer_"
               "cold_launch_manifest_v10.sha256",
         "bead6e9e1c53478c874612f00cae6cab1add14069d41b71b4310eb9b46b958db"),
    "cold_outer_v10":
        (OUT / "cm2_round306c79g_true_global_no_producer_consumer_"
               "cold_launch_outer_receipt_v10.json",
         "2d95b83a2658d10a70d7c1e87b195920fc8207fc639fa407ff23252e5bc5edc4"),
}
V10_EXACT10_ORDER = (
    "v9_official_rejection", "closed_schema_v10", "contract_v10",
    "build_only_producer_v10", "independent_consumer_v10",
    "transition_v9_to_v10", "static_audit_v10", "cold_launcher_v10",
    "cold_manifest_v10", "cold_outer_v10",
)
V10_FROZEN_OBJECTS = {
    "v9_official_rejection": V9_OFFICIAL_REJECTION_OBJECT_PIN,
    "contract_v10":
        "c99acd60e953a939e3e9fd95e7559ce4249dc6efda0c3653e8ac1ae42b771bf4",
    "transition_v9_to_v10":
        "249fd39eb7da989cbce59656f567028a38bb9900e4b577ae6d2f2ab4983ca6ac",
    "static_audit_v10":
        "bb2cf294babf04fdbbbd35c88c1d6bce8c58426765ae69925c659b396feabcb8",
    "cold_outer_v10":
        "fc2f595fb47795aff01396b9593630ef15f65237dcc0ffab2e5628e92722a6a4",
}
V10_FIRST_RUNTIME_ATTEMPT = {'attempted': True,
 'command': 'build',
 'orientation': 'a',
 'producer_child_spawned': True,
 'candidate_write_started': False,
 'candidate_or_stage_created': False,
 'positive_runtime_surface_count': 0,
 'aborted_by_regression_label_prefix_guard': True}
V10_REGRESSION_LABEL_PREFIX_INCIDENT = {'schema': 'cm2.round306c79g.true-global-no-producer-consumer.v10-regression-label-prefix-incident.v1',
 'incident_id': 'V10_PRODUCER_V9_REGRESSION_LABEL_PREFIX_COLON_MISMATCH',
 'evidence_source': 'FROZEN_V10_PRODUCER_AST_CONTROL_FLOW_AND_FIRST_BUILD_A_STDERR',
 'authority_source': 'AST_STRUCTURE_AND_EXACT_PREFIX_JOIN__NOT_RAW_WHOLE_TREE_STRING_EQUALITY',
 'producer_source_path': 'deliverables/cm2_round306c79g_true_global_no_producer_consumer_v10.py',
 'producer_source_file_sha256': '99bb321da8a63855e52c8d6757d00886c0deeb2182f5044cac35f645e2ebd00a',
 'frozen_v9_launcher_path': 'deliverables/cm2_round306c79g_true_global_no_producer_consumer_cold_launch_v9.py',
 'frozen_v9_launcher_file_sha256': 'f7559ceeb7d491b8489812670392cb63e3cd5f6a2764db469e2dd51d6b5577fa',
 'regression_function': 'v9_prechild_shape_drift_regression',
 'first_command': 'build',
 'first_orientation': 'a',
 'inner_stderr_line': 'REJECT: frozen v9 launcher statically embeds structural16 in '
                      'exact equality gate',
 'outer_stderr_line': 'REJECT: cold child rejected or failed',
 'regression_guard_conjunct_count': 6,
 'regression_guard_conjunct_truth_vector': [True, True, True, True, False, True],
 'regression_guard_true_conjunct_count': 5,
 'regression_guard_false_conjunct_count': 1,
 'unique_false_conjunct_zero_based_index': 4,
 'unique_false_conjunct_source_line': 2315,
 'expanded_structural_dict_count': 1,
 'expanded_structural_dict_exact_key_count': 16,
 'validator_call_count': 1,
 'equality_gate_count': 2,
 'v9_launcher_hash_gate': True,
 'failure_label_without_colon_prefix': 'exact v6 exact10, rejection, '
                                       'spawned-before-write and HeldSelf.identity '
                                       'defect regression',
 'exact_unprefixed_failure_label_literal_count': 0,
 'colon_prefixed_failure_label_literal': ':exact v6 exact10, rejection, '
                                         'spawned-before-write and HeldSelf.identity '
                                         'defect regression',
 'exact_colon_prefixed_failure_label_literal_count': 1,
 'failure_label_suffix_match_count': 1,
 'authority_derived_from_AST_structure_and_exact_prefix_join': True,
 'raw_whole_tree_string_equality_is_authority': False,
 'hold_static_freeze_trust_call_source_line': 6310,
 'regression_call_inside_hold_source_line': 3811,
 'candidate_stage_creation_source_line': 6415,
 'hold_function_contains_mkdir_call': False,
 'producer_child_spawned': True,
 'candidate_write_started': False,
 'candidate_or_stage_created': False,
 'positive_runtime_surface_count': 0,
 'failure_occurs_before_candidate_or_stage_creation': True,
 'required_successor_fix': 'MATCH_COLON_PREFIX_BY_AST_STRUCTURE_AND_EXACT_PREFIX_JOIN__NEVER_RAW_WHOLE_TREE_LITERAL_MEMBERSHIP',
 'formal_global_closure_credit': 0,
 'D02_unlock': False,
 'D02_started': False}
V10_REGRESSION_LABEL_PREFIX_INCIDENT_SHA256 = (
    "882d5646ea49b31ccdb9db4f5b8f5d6dd860d2ed8eb9b44c9d10f9c5eacfa33b")
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

# Frozen v11 is the immediate append-only predecessor.  Ordinary publication
# identities remain O_PATH metadata holds.  The producer/launcher bytes and
# official rejection bytes are opened only after the inherited v14 exact12
# gate, then retained for pinned noncredit incident authority.
V11_FROZEN_FILES = {
    "v10_official_rejection":
        (V10_OFFICIAL_REJECTION, V10_OFFICIAL_REJECTION_FILE_PIN),
    "closed_schema_v11":
        (OUT / "cm2_round306c79g_true_global_no_producer_consumer_schema_v11.json",
         "cf1630e3ab1b590876c663b8752d702eae5fe37b7bdbcc7824efbd03bbdbd8e2"),
    "contract_v11":
        (OUT / "cm2_round306c79g_true_global_no_producer_consumer_contract_v11.json",
         "c8851778bc8df7a9804efb5fc226548424b58119a2dff3f75bdea9fcac0ec5cf"),
    "build_only_producer_v11":
        (OUT / "cm2_round306c79g_true_global_no_producer_consumer_v11.py",
         "f3b364afc0f5b2f729a3d7786eb8e9c25a9303959d6d2464a40395968090a30b"),
    "independent_consumer_v11":
        (OUT / "cm2_round306c79g_true_global_no_producer_consumer_"
               "independent_verifier_assembler_authority_consumer_v11.py",
         "d8ad069e3486b9d657e4840e504885bf13129050f68e6cc04e47b71f149370ec"),
    "transition_v10_to_v11":
        (OUT / "cm2_round306c79g_true_global_no_producer_consumer_"
               "v10_to_v11_static_launch_transition_receipt_v1.json",
         "31b33566b898277fb8b272a6f3cd3b51b0b80eac4f58f43979dddfa647a38f4e"),
    "static_audit_v11":
        (OUT / "cm2_round306c79g_true_global_no_producer_consumer_static_audit_v11.json",
         "6c94068e3f60a89fb608585ae5e6c7dbe02af17880195132bf7c9033ab797115"),
    "cold_launcher_v11":
        (OUT / "cm2_round306c79g_true_global_no_producer_consumer_cold_launch_v11.py",
         "9f6971d2ca3e2c8f448a6aeed70bc16f38154c626f7744a4e20ba723e3082cc2"),
    "cold_manifest_v11":
        (OUT / "cm2_round306c79g_true_global_no_producer_consumer_"
               "cold_launch_manifest_v11.sha256",
         "e27e9b58dbf57a72550da701589819dad7ebb01f6b3c649a56b701c99ef13135"),
    "cold_outer_v11":
        (OUT / "cm2_round306c79g_true_global_no_producer_consumer_"
               "cold_launch_outer_receipt_v11.json",
         "689a4a323e742427c7f50ec6a7bbea08cdf28c36cbdb43d855a29601329f8c8f"),
}
V11_EXACT10_ORDER = (
    "v10_official_rejection", "closed_schema_v11", "contract_v11",
    "build_only_producer_v11", "independent_consumer_v11",
    "transition_v10_to_v11", "static_audit_v11", "cold_launcher_v11",
    "cold_manifest_v11", "cold_outer_v11",
)
V11_FROZEN_OBJECTS = {
    "v10_official_rejection": V10_OFFICIAL_REJECTION_OBJECT_PIN,
    "contract_v11":
        "b998162a009927f13eb34a88e37f657515e43ae160b3d550de5edb0040486af9",
    "transition_v10_to_v11":
        "9a253960a378521423751735dd272e06dec5c99cfc016d27bf66cfbe7673caaf",
    "static_audit_v11":
        "007fba200b67c7704360bb85819435ed13cc6459c8dbac381b99c3adaaf884c3",
    "cold_outer_v11":
        "369dfe73b1dbc68e4147ba39e1c1b7155555b5443d9471159c5ac748723414a4",
}
V12_FROZEN_FILES = {
    "v11_official_rejection":
        (V11_OFFICIAL_REJECTION, V11_OFFICIAL_REJECTION_FILE_PIN),
    "closed_schema_v12":
        (OUT / "cm2_round306c79g_true_global_no_producer_consumer_schema_v12.json",
         "5ed911a55e8f90e750fdcaf6ab4fb6c9683bebaf66a4d6250329dff98acb2e28"),
    "contract_v12":
        (OUT / "cm2_round306c79g_true_global_no_producer_consumer_contract_v12.json",
         "72246725b15891f92cbc6e3fa1c07ab4a76cdaa19f1b366a736f47f51989b343"),
    "build_only_producer_v12":
        (V12_FROZEN_PRODUCER,
         "4cafc594f8a60063b7e7caaa82ddcc2b7983d0fbf0929034cd3cb5f360f3ed1d"),
    "independent_consumer_v12":
        (V12_FROZEN_CONSUMER,
         "b74dee738257d485e9ca3357d7d138b5175b95e58f1c8ea87d1eca7bfc96b2ed"),
    "transition_v11_to_v12":
        (OUT / "cm2_round306c79g_true_global_no_producer_consumer_"
               "v11_to_v12_static_launch_transition_receipt_v1.json",
         "45dabc1ef60eb2f8ba34aa7daa69f9d2b3bedccd4168d9c472bd4bbb696b5400"),
    "static_audit_v12":
        (OUT / "cm2_round306c79g_true_global_no_producer_consumer_static_audit_v12.json",
         "ac29b1e31e0d1b51e8610b7699d1aaf55c80fa6f13f00b20b209c2889e121d37"),
    "cold_launcher_v12":
        (V12_FROZEN_LAUNCHER,
         "b7aaff67be866f8fd7a01f71e97ea1491574f69e62b7760b6ced9183997444ba"),
    "cold_manifest_v12":
        (OUT / "cm2_round306c79g_true_global_no_producer_consumer_"
               "cold_launch_manifest_v12.sha256",
         "297e9f58dc7657c6fa959dd45081efffe4e7e8dadcd16ab89457863e2661ece6"),
    "cold_outer_v12":
        (OUT / "cm2_round306c79g_true_global_no_producer_consumer_"
               "cold_launch_outer_receipt_v12.json",
         "27129990a9d5b6697fd13ee8e2086100cbf158f12e5b767166d771e63088b6d0"),
}
V12_EXACT10_ORDER = (
    "v11_official_rejection", "closed_schema_v12", "contract_v12",
    "build_only_producer_v12", "independent_consumer_v12",
    "transition_v11_to_v12", "static_audit_v12", "cold_launcher_v12",
    "cold_manifest_v12", "cold_outer_v12",
)
V12_FROZEN_OBJECTS = {
    "v11_official_rejection": V11_OFFICIAL_REJECTION_OBJECT_PIN,
    "contract_v12":
        "f5c1710817dc8e3aa7fe2bbf4b88e6e39baaa1b17bbeb0f8bf37c8c4575ae5d7",
    "transition_v11_to_v12":
        "0673ecafaa9991cd78e905e144e7c8c1b91717a3d753befa13e82552d44a4072",
    "static_audit_v12":
        "c1473ae0f5a08d8772227f61a55bd32c479a7b5c7d40da17b37e796abf4d9783",
    "cold_outer_v12":
        "bc6d06141865954590bd11bfc96ad59dbbffa003f568355ecb47155a8a3a809d",
}
V11_FIRST_RUNTIME_ATTEMPT = {
    "attempted": True,
    "command": "build",
    "orientation": "a",
    "producer_child_spawned": True,
    "candidate_write_started": False,
    "candidate_or_stage_created": False,
    "positive_runtime_surface_count": 0,
    "aborted_by_dual_validator_divergence_guard": True,
}
V10_COLON_PREFIX_WITNESS_HELPER_AST_SHA256 = (
    "38ebe2f639bdb26cac05cec05110ef78bf8057159ebf0f9c8f5d1ce22743fa07")
V10_COLON_PREFIX_WITNESS = {
    "schema":
        "cm2.round306c79g.true-global-no-producer-consumer."
        "v10-colon-prefix-per-clause-witness.v1",
    "v10_producer_file_sha256":
        "99bb321da8a63855e52c8d6757d00886c0deeb2182f5044cac35f645e2ebd00a",
    "v9_launcher_file_sha256":
        "f7559ceeb7d491b8489812670392cb63e3cd5f6a2764db469e2dd51d6b5577fa",
    "six_guard_ast_sha256":
        "aad296d59f0c196d5f1a733db80251fe7d01b8f658db00e3815392228cd1b94a",
    "six_guard_conjunct_count": 6,
    "fifth_membership_ast_sha256":
        "e1212df00bbe1d30edd9ddd5f0cdd4c5c489533ada4e9b3dee8a63fd1e64b3a5",
    "fifth_membership_is_exact_legacy_tree_wide_in": True,
    "expanded_structural_dict_count": 1,
    "expanded_structural_dict_exact_key_count": 16,
    "expanded_structural_dict_ast_sha256":
        "5e7482a66f4f5e7daaae15817b0ed4ca227642c259f159cab2ee9aa913b15c6d",
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
    "exact_colon_prefix_join_ast_sha256":
        "32166f78c1a380ba16122e37f91de30255bf99399e605b97a9c7e97d5a60d138",
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
    "object_sha256":
        "374ec1404780efc5cf78da8e4c4b2554d25e6a1bc5da65d063263b34e0531011",
}
V10_COLON_PREFIX_WITNESS_KEY_ORDER = tuple(V10_COLON_PREFIX_WITNESS)
V11_DUAL_VALIDATOR_DIVERGENCE_INCIDENT = {
    "schema":
        "cm2.round306c79g.true-global-no-producer-consumer."
        "v11-dual-validator-divergence-incident.v1",
    "incident_id":
        "V11_LAUNCHER_GATE_PASSED__PRODUCER_COMPOSITE_GUARD_REJECTED__NO_EXACT_FALSE_CLAUSE",
    "evidence_source":
        "FROZEN_V11_LAUNCHER_AND_PRODUCER_AST__FIRST_BUILD_A_STDERR__OFFICIAL_REJECTION",
    "v11_producer_source_path":
        "deliverables/cm2_round306c79g_true_global_no_producer_consumer_v11.py",
    "v11_producer_source_file_sha256":
        "f3b364afc0f5b2f729a3d7786eb8e9c25a9303959d6d2464a40395968090a30b",
    "v11_launcher_source_path":
        "deliverables/cm2_round306c79g_true_global_no_producer_consumer_cold_launch_v11.py",
    "v11_launcher_source_file_sha256":
        "9f6971d2ca3e2c8f448a6aeed70bc16f38154c626f7744a4e20ba723e3082cc2",
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
    "producer_guard_function": "v10_regression_label_prefix_incident_regression",
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
        "374ec1404780efc5cf78da8e4c4b2554d25e6a1bc5da65d063263b34e0531011",
    "v10_colon_prefix_witness_key_count": 40,
    "v10_colon_prefix_witness_successor_clause_truth_vector": [True] * 15,
    "v10_colon_prefix_witness_all_clauses_true": True,
    "inner_stderr_line":
        "REJECT: frozen v10 sole-false colon-prefix regression and pre-stage control flow",
    "outer_stderr_line": "REJECT: cold child rejected or failed",
    "failure_occurs_before_candidate_or_stage_creation": True,
    "official_rejection_strictly_after_v11_outer": True,
    "required_successor_fix":
        "INHERITED_HELD_FD_BYTES__THREE_INDEPENDENT_IDENTICAL_HELPERS__EXACT_PER_CLAUSE_WITNESS",
    "required_held_fd_fix":
        "CHILD_REVALIDATES_INHERITED_V10_V9_V11_AND_REJECTION_FDS__NO_SECOND_PATH_VIEW_AS_INCIDENT_AUTHORITY",
    "required_validator_fix":
        "EXACT40_CLOSED_WITNESS__CONTROLLED_ZERO_OR_MULTIPLE_DICT_REJECT__NO_RAW_TREE_LITERAL_AUTHORITY",
    "formal_global_closure_credit": 0,
    "D02_unlock": False,
    "D02_started": False,
    "standalone_authority": False,
    "exact_false_clause_claim_allowed": False,
}
V11_DUAL_VALIDATOR_DIVERGENCE_INCIDENT_SHA256 = (
    "64db719d426d3604be39d9bcd52118c1c39a409e47c2aaf38704b18d49ce7ab3")
V11_PUBLISHED_THEN_REJECTED_PROOF_SHA256 = (
    "8ee05054f12eddddb000f354a3dd1354532a91e37ef1b6d53a250257d9fe8990")
HISTORICAL_TRANSITIVE_PATHSET_EXACT17 = (
    (V10_PRODUCER_FD_ENV, V10_FROZEN_FILES["build_only_producer_v10"][0],
     V10_FROZEN_FILES["build_only_producer_v10"][1]),
    (V9_LAUNCHER_FD_ENV, V9_FROZEN_FILES["cold_launcher_v9"][0],
     V9_FROZEN_FILES["cold_launcher_v9"][1]),
    (V11_PRODUCER_FD_ENV, V11_FROZEN_FILES["build_only_producer_v11"][0],
     V11_FROZEN_FILES["build_only_producer_v11"][1]),
    (V11_LAUNCHER_FD_ENV, V11_FROZEN_FILES["cold_launcher_v11"][0],
     V11_FROZEN_FILES["cold_launcher_v11"][1]),
    (V11_REJECTION_FD_ENV, V11_OFFICIAL_REJECTION,
     V11_OFFICIAL_REJECTION_FILE_PIN),
    (V12_PRODUCER_FD_ENV, V12_FROZEN_PRODUCER,
     V12_FROZEN_FILES["build_only_producer_v12"][1]),
    (V12_CONSUMER_FD_ENV, V12_FROZEN_CONSUMER,
     V12_FROZEN_FILES["independent_consumer_v12"][1]),
    (V12_LAUNCHER_FD_ENV, V12_FROZEN_LAUNCHER,
     V12_FROZEN_FILES["cold_launcher_v12"][1]),
    (V5_REJECTION_FD_ENV, V5_OFFICIAL_REJECTION,
     V5_OFFICIAL_REJECTION_FILE_PIN),
    (V12_REJECTION_FD_ENV, V12_OFFICIAL_REJECTION,
     V12_OFFICIAL_REJECTION_FILE_PIN),
    (V13_PRODUCER_FD_ENV, V13_FROZEN_PRODUCER,
     V13_INCIDENT_EXACT6_PINS[V13_FROZEN_PRODUCER]),
    (V13_CONSUMER_FD_ENV, V13_FROZEN_CONSUMER,
     V13_INCIDENT_EXACT6_PINS[V13_FROZEN_CONSUMER]),
    (V13_LAUNCHER_FD_ENV, V13_FROZEN_LAUNCHER,
     V13_INCIDENT_EXACT6_PINS[V13_FROZEN_LAUNCHER]),
    (V13_PRODUCER_PYC_FD_ENV, V13_FROZEN_PRODUCER_PYC,
     V13_INCIDENT_EXACT6_PINS[V13_FROZEN_PRODUCER_PYC]),
    (V13_CONSUMER_PYC_FD_ENV, V13_FROZEN_CONSUMER_PYC,
     V13_INCIDENT_EXACT6_PINS[V13_FROZEN_CONSUMER_PYC]),
    (V13_LAUNCHER_PYC_FD_ENV, V13_FROZEN_LAUNCHER_PYC,
     V13_INCIDENT_EXACT6_PINS[V13_FROZEN_LAUNCHER_PYC]),
    (V13_SUPERSESSION_RECEIPT_FD_ENV, V13_SUPERSESSION_RECEIPT,
     V13_SUPERSESSION_RECEIPT_FILE_PIN),
)
HISTORICAL_TRANSITIVE_EXACT16_ROLES = (
    "v10_producer", "v9_launcher", "v11_producer", "v11_launcher",
    "v11_rejection", "v12_producer", "v12_consumer", "v12_launcher",
    "v5_rejection", "v12_rejection",
    "v13_build_only_producer_source", "v13_independent_consumer_source",
    "v13_cold_launcher_source", "v13_build_only_producer_pyc",
    "v13_independent_consumer_pyc", "v13_cold_launcher_pyc",
)
_INCIDENT_AUTHORITY_WITNESS: dict[str, Any] | None = None
_INCIDENT_AUTHORITY_V12_SHAPE: dict[str, Any] | None = None
_INCIDENT_AUTHORITY_HOLD: Any | None = None

STATIC_AUDIT_INPUT_EXACT43 = (
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
STATIC_AUDIT_INPUT_EXACT43_ORDER_SHA256 = (
    "7e11baf937aa7e9695f30718fcb14793ed2fdacbdf0f33bda659086d399e4574")
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


class Reject(RuntimeError):
    pass


F_GET_SEALS = getattr(fcntl, "F_GET_SEALS", 1034)
F_SEAL_SEAL = getattr(fcntl, "F_SEAL_SEAL", 0x0001)
F_SEAL_SHRINK = getattr(fcntl, "F_SEAL_SHRINK", 0x0002)
F_SEAL_GROW = getattr(fcntl, "F_SEAL_GROW", 0x0004)
F_SEAL_WRITE = getattr(fcntl, "F_SEAL_WRITE", 0x0008)
REQUIRED_EXEC_SEALS = (
    F_SEAL_SEAL | F_SEAL_SHRINK | F_SEAL_GROW | F_SEAL_WRITE)


def _fd_fingerprint(value: os.stat_result) -> tuple[int, ...]:
    return (
        value.st_dev, value.st_ino, value.st_mode, value.st_size,
        value.st_mtime_ns, value.st_ctime_ns, value.st_nlink)


def _pread_all(descriptor: int) -> bytes:
    """Read one regular fd without changing its shared open-file offset."""
    blocks: list[bytes] = []
    offset = 0
    while True:
        block = os.pread(descriptor, 1 << 20, offset)
        if not block:
            return b"".join(blocks)
        blocks.append(block)
        offset += len(block)


def _initial_sealed_exec_source_gate(
        exec_fd: int, source_fd: int) -> tuple[bytes, bytes]:
    """Prove execution and installed-source bytes before any workspace access."""
    exec_before = os.fstat(exec_fd)
    source_before = os.fstat(source_fd)
    try:
        exec_seals = int(fcntl.fcntl(exec_fd, F_GET_SEALS))
    except OSError as exc:
        raise Reject("cold exec fd exposes exact memfd seals") from exc
    exec_raw = _pread_all(exec_fd)
    source_raw = _pread_all(source_fd)
    exec_after = os.fstat(exec_fd)
    source_after = os.fstat(source_fd)
    need(stat.S_ISREG(exec_before.st_mode) and
         stat.S_IMODE(exec_before.st_mode) == 0o444 and
         exec_before.st_nlink == 0 and
         exec_seals == REQUIRED_EXEC_SEALS and
         _fd_fingerprint(exec_before) == _fd_fingerprint(exec_after),
         "sealed exec memfd exact regular 0444 nlink0 four-seal identity")
    need(stat.S_ISREG(source_before.st_mode) and
         stat.S_IMODE(source_before.st_mode) == 0o444 and
         source_before.st_nlink == 1 and
         _fd_fingerprint(source_before) == _fd_fingerprint(source_after),
         "installed source fd exact regular 0444 nlink1 identity")
    need((exec_before.st_dev, exec_before.st_ino) !=
             (source_before.st_dev, source_before.st_ino) and
         exec_raw == source_raw,
         "distinct sealed exec and installed source fds have byte-identical content")
    return exec_raw, source_raw


class HeldSelf:
    """Hold distinct sealed-exec and installed-source fds for the command."""
    def __init__(self) -> None:
        need(SELF == OUT /
             "cm2_round306c79g_true_global_no_producer_consumer_independent_verifier_assembler_authority_consumer_v16r2r63y_repair_semantic_source.py",
             "SELF exact frozen v16r2 verifier/assembler/authority-consumer path")
        exec_text = os.environ.get(COLD_EXEC_FD_ENV, "")
        source_text = os.environ.get(COLD_SOURCE_FD_ENV, "")
        need(exec_text.isascii() and exec_text.isdecimal() and
             source_text.isascii() and source_text.isdecimal(),
             "cold launcher inherited exec/source-fd environment")
        inherited_exec_fd = int(exec_text)
        inherited_source_fd = int(source_text)
        need(str(EXECUTED_SOURCE_PATH) ==
                 "/proc/self/fd/" + str(inherited_exec_fd),
             "consumer executed only through exact inherited sealed exec memfd")
        self.exec_fd = -1
        self.source_fd = -1
        self.fd = -1
        path_fd = -1
        try:
            self.exec_fd = os.dup(inherited_exec_fd)
            self.source_fd = os.dup(inherited_source_fd)
            # ``fd`` remains the installed source alias used by the existing
            # exact10/static identity code.  The anonymous exec copy is never
            # misrepresented as a frozen package member.
            self.fd = self.source_fd
            self.exec_before = os.fstat(self.exec_fd)
            self.before = os.fstat(self.source_fd)
            self.exec_seals = int(fcntl.fcntl(self.exec_fd, F_GET_SEALS))
            self.exec_raw = _pread_all(self.exec_fd)
            self.raw = _pread_all(self.source_fd)
            path_fd = openat2_beneath(SELF, os.O_RDONLY | os.O_NOFOLLOW)
            path_before = os.fstat(path_fd)
            path_raw = _pread_all(path_fd)
            need(stat.S_ISREG(self.exec_before.st_mode) and
                 stat.S_IMODE(self.exec_before.st_mode) == 0o444 and
                 self.exec_before.st_nlink == 0 and
                 self.exec_seals == REQUIRED_EXEC_SEALS,
                 "held executed memfd exact regular 0444 nlink0 four seals")
            need(stat.S_ISREG(self.before.st_mode) and
                 stat.S_IMODE(self.before.st_mode) == 0o444 and
                 self.before.st_nlink == 1 and
                 _fd_fingerprint(self.before) == _fd_fingerprint(path_before),
                 "held installed source fd equals securely opened SELF path")
            need((self.exec_before.st_dev, self.exec_before.st_ino) !=
                     (self.before.st_dev, self.before.st_ino) and
                 self.exec_raw == self.raw == path_raw,
                 "sealed executed bytes equal distinct installed source/path bytes")
            self.exec_mount_id = statx_mount_id(self.exec_fd)
            self.mount_id = statx_mount_id(self.source_fd)
            need(statx_mount_id(path_fd) == self.mount_id,
                 "installed source fd/path statx mount identity")
            self.file_sha256 = sha(self.raw)
            self.exec_file_sha256 = sha(self.exec_raw)
            need(self.exec_file_sha256 == self.file_sha256,
                 "sealed exec and installed source SHA-256 equality")
            workspace_root_terminal_replay()
        except BaseException:
            if path_fd >= 0:
                os.close(path_fd)
                path_fd = -1
            if self.source_fd >= 0:
                os.close(self.source_fd)
                self.source_fd = -1
                self.fd = -1
            if self.exec_fd >= 0:
                os.close(self.exec_fd)
                self.exec_fd = -1
            raise
        finally:
            if path_fd >= 0:
                os.close(path_fd)

    @property
    def identity(self) -> tuple[int, int]:
        """Installed SELF identity; the anonymous exec inode is never published."""
        return (self.before.st_dev, self.before.st_ino)

    def terminal_replay(self) -> None:
        workspace_root_terminal_replay()
        path_fd = openat2_beneath(SELF, os.O_RDONLY | os.O_NOFOLLOW)
        try:
            exec_pre = os.fstat(self.exec_fd)
            source_pre = os.fstat(self.source_fd)
            path_pre = os.fstat(path_fd)
            exec_replay = _pread_all(self.exec_fd)
            source_replay = _pread_all(self.source_fd)
            path_replay = _pread_all(path_fd)
            exec_post = os.fstat(self.exec_fd)
            source_post = os.fstat(self.source_fd)
            path_post = os.fstat(path_fd)
            exec_seals = int(fcntl.fcntl(self.exec_fd, F_GET_SEALS))
            need(_fd_fingerprint(exec_pre) ==
                     _fd_fingerprint(self.exec_before) ==
                     _fd_fingerprint(exec_post) and
                 stat.S_IMODE(exec_post.st_mode) == 0o444 and
                 exec_post.st_nlink == 0 and
                 exec_seals == self.exec_seals == REQUIRED_EXEC_SEALS and
                 exec_replay == self.exec_raw,
                 "sealed exec memfd terminal identity/bytes/four-seal replay")
            need(_fd_fingerprint(source_pre) ==
                     _fd_fingerprint(self.before) ==
                     _fd_fingerprint(source_post) ==
                     _fd_fingerprint(path_pre) ==
                     _fd_fingerprint(path_post) and
                 source_replay == self.raw == path_replay and
                 exec_replay == source_replay,
                 "installed source same-fd/path and sealed-exec terminal byte replay")
            need(statx_mount_id(self.exec_fd) == self.exec_mount_id and
                 statx_mount_id(self.source_fd) == self.mount_id ==
                     statx_mount_id(path_fd),
                 "sealed exec and installed source/path terminal mount identities")
        finally:
            os.close(path_fd)
        workspace_root_terminal_replay()

    def close(self) -> None:
        if self.source_fd >= 0:
            os.close(self.source_fd)
            self.source_fd = -1
            self.fd = -1
        if self.exec_fd >= 0:
            os.close(self.exec_fd)
            self.exec_fd = -1


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Reject(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


sha_bytes = sha


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
})
HISTORICAL_REJECTION_KEYSET_STEPS = (
    (3, frozenset(), V3_OFFICIAL_REJECTION_FILE_PIN,
     V3_OFFICIAL_REJECTION_OBJECT_PIN,
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
HISTORICAL_REJECTION_V5_KEYS = HISTORICAL_REJECTION_V3_KEYS | frozenset({
    "v4_rejection_supersession_file_sha256",
    "v4_rejection_supersession_object_sha256",
})
HISTORICAL_REJECTION_V6_KEYS = HISTORICAL_REJECTION_V5_KEYS | frozenset({
    "v5_official_rejection_file_sha256",
    "v5_official_rejection_object_sha256",
})
HISTORICAL_REJECTION_V7_KEYS = HISTORICAL_REJECTION_V6_KEYS | frozenset({
    "v6_official_rejection_file_sha256",
    "v6_official_rejection_object_sha256",
})
HISTORICAL_REJECTION_V8_KEYS = HISTORICAL_REJECTION_V7_KEYS | frozenset({
    "v7_official_rejection_file_sha256",
    "v7_official_rejection_object_sha256",
    "v7_publication_lock_continuity_incident_object_sha256",
})
HISTORICAL_REJECTION_V9_KEYS = HISTORICAL_REJECTION_V8_KEYS | frozenset({
    "v8_official_rejection_file_sha256",
    "v8_official_rejection_object_sha256",
})
HISTORICAL_REJECTION_V10_KEYS = HISTORICAL_REJECTION_V9_KEYS | frozenset({
    "v9_official_rejection_file_sha256",
    "v9_official_rejection_object_sha256",
})
HISTORICAL_REJECTION_V11_KEYS = HISTORICAL_REJECTION_V10_KEYS | frozenset({
    "v10_official_rejection_file_sha256",
    "v10_official_rejection_object_sha256",
})
HISTORICAL_REJECTION_V12_KEYS = HISTORICAL_REJECTION_V11_KEYS | frozenset({
    "v11_official_rejection_file_sha256",
    "v11_official_rejection_object_sha256",
})


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
    {"version": "v3", "path": ".cm2-runtime/c79g-v3-rejections-" +
     UPSTREAM_CHECKPOINT_OBJECT_PIN + "/rejection.json",
     "file_sha256": V3_OFFICIAL_REJECTION_FILE_PIN,
     "object_sha256": V3_OFFICIAL_REJECTION_OBJECT_PIN, "key_count": 37,
     "sorted_keys": sorted(HISTORICAL_REJECTION_V3_KEYS),
     "sorted_key_array_sha256":
     "21ba021c649349266d95670e63136fef1772b5d8dbb79334907c9df400620a18",
     "canonical_object_closed": True},
    {"version": "v5", "path": ".cm2-runtime/c79g-v5-rejections-" +
     UPSTREAM_CHECKPOINT_OBJECT_PIN + "/rejection.json",
     "file_sha256": V5_OFFICIAL_REJECTION_FILE_PIN,
     "object_sha256": V5_OFFICIAL_REJECTION_OBJECT_PIN, "key_count": 39,
     "sorted_keys": sorted(HISTORICAL_REJECTION_V5_KEYS),
     "sorted_key_array_sha256": V5_OFFICIAL_REJECTION_EXACT39_KEYSET_SHA256,
     "canonical_object_closed": True},
    {"version": "v6", "path": ".cm2-runtime/c79g-v6-rejections-" +
     UPSTREAM_CHECKPOINT_OBJECT_PIN + "/rejection.json",
     "file_sha256": V6_OFFICIAL_REJECTION_FILE_PIN,
     "object_sha256": V6_OFFICIAL_REJECTION_OBJECT_PIN, "key_count": 41,
     "sorted_keys": sorted(HISTORICAL_REJECTION_V6_KEYS),
     "sorted_key_array_sha256":
     "5881a652aabef3e7e65917689487f13b99bfa60fff0ebb7c144bc02b26897638",
     "canonical_object_closed": True},
    {"version": "v7", "path": ".cm2-runtime/c79g-v7-rejections-" +
     UPSTREAM_CHECKPOINT_OBJECT_PIN + "/rejection.json",
     "file_sha256": V7_OFFICIAL_REJECTION_FILE_PIN,
     "object_sha256": V7_OFFICIAL_REJECTION_OBJECT_PIN, "key_count": 43,
     "sorted_keys": sorted(HISTORICAL_REJECTION_V7_KEYS),
     "sorted_key_array_sha256":
     "02b54c94602de1f5af8e545692f44815b9ac3ba334369dd96ee4e9b677bf1308",
     "canonical_object_closed": True},
    {"version": "v8", "path": ".cm2-runtime/c79g-v8-rejections-" +
     UPSTREAM_CHECKPOINT_OBJECT_PIN + "/rejection.json",
     "file_sha256": V8_OFFICIAL_REJECTION_FILE_PIN,
     "object_sha256": V8_OFFICIAL_REJECTION_OBJECT_PIN, "key_count": 46,
     "sorted_keys": sorted(HISTORICAL_REJECTION_V8_KEYS),
     "sorted_key_array_sha256":
     "a1da14307b813345ee0f8877550412b40951f7857e5972570ab41f97e2fe31bf",
     "canonical_object_closed": True},
    {"version": "v9", "path": ".cm2-runtime/c79g-v9-rejections-" +
     UPSTREAM_CHECKPOINT_OBJECT_PIN + "/rejection.json",
     "file_sha256": V9_OFFICIAL_REJECTION_FILE_PIN,
     "object_sha256": V9_OFFICIAL_REJECTION_OBJECT_PIN, "key_count": 48,
     "sorted_keys": sorted(HISTORICAL_REJECTION_V9_KEYS),
     "sorted_key_array_sha256":
     "d0617183e15fd4c5bfd3495d7dca56cb9aea7035bedf35a1bdf6efd166a70308",
     "canonical_object_closed": True},
    {"version": "v10", "path": ".cm2-runtime/c79g-v10-rejections-" +
     UPSTREAM_CHECKPOINT_OBJECT_PIN + "/rejection.json",
     "file_sha256": V10_OFFICIAL_REJECTION_FILE_PIN,
     "object_sha256": V10_OFFICIAL_REJECTION_OBJECT_PIN, "key_count": 50,
     "sorted_keys": sorted(HISTORICAL_REJECTION_V10_KEYS),
     "sorted_key_array_sha256":
     "01274ec0c36bd85423d385bdb22cdff7fe6ccfe2d114864994fc2ead2153eddb",
     "canonical_object_closed": True},
    {"version": "v11", "path": ".cm2-runtime/c79g-v11-rejections-" +
     UPSTREAM_CHECKPOINT_OBJECT_PIN + "/rejection.json",
     "file_sha256": V11_OFFICIAL_REJECTION_FILE_PIN,
     "object_sha256": V11_OFFICIAL_REJECTION_OBJECT_PIN, "key_count": 52,
     "sorted_keys": sorted(HISTORICAL_REJECTION_V11_KEYS),
     "sorted_key_array_sha256":
     "75ca9378fbff7a6956686e7390556fffa3d6ff939630ed47e8c8c185872e97f8",
     "canonical_object_closed": True},
    {"version": "v12", "path": ".cm2-runtime/c79g-v12-rejections-" +
     UPSTREAM_CHECKPOINT_OBJECT_PIN + "/rejection.json",
     "file_sha256": V12_OFFICIAL_REJECTION_FILE_PIN,
     "object_sha256": V12_OFFICIAL_REJECTION_OBJECT_PIN, "key_count": 54,
     "sorted_keys": sorted(HISTORICAL_REJECTION_V12_KEYS),
     "sorted_key_array_sha256": V12_OFFICIAL_REJECTION_EXACT54_KEYSET_SHA256,
     "canonical_object_closed": True},
)


def digest(value: Any) -> str:
    return sha(canonical(value))


def close_row(body: dict[str, Any]) -> dict[str, Any]:
    need("row_sha256" not in body, "close row")
    return {**body, "row_sha256": digest(body)}


def close_object(body: dict[str, Any]) -> dict[str, Any]:
    need("object_sha256" not in body, "close object")
    return {**body, "object_sha256": digest(body)}


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


def verify_row(row: Mapping[str, Any], label: str) -> None:
    body = copy.deepcopy(dict(row)); claim = body.pop("row_sha256", None)
    need(isinstance(claim, str) and claim == digest(body), label + ":row closure")


def verify_object(value: Mapping[str, Any], label: str, pin: str | None = None) -> None:
    body = copy.deepcopy(dict(value)); claim = body.pop("object_sha256", None)
    need(isinstance(claim, str) and claim == digest(body), label + ":object closure")
    if pin is not None:
        need(claim == pin, label + ":object pin")


def strict_json(raw: bytes, label: str) -> Any:
    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        out: dict[str, Any] = {}
        for key, value in items:
            need(key not in out, label + ":duplicate:" + key)
            out[key] = value
        return out
    try:
        return json.loads(raw, object_pairs_hook=pairs,
                          parse_constant=lambda x: (_ for _ in ()).throw(Reject(label + ":" + x)))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise Reject(label + ":strict JSON") from exc


def _nonzero_sha256(value: Any) -> bool:
    return (isinstance(value, str) and len(value) == 64 and
            value != "0" * 64 and all(character in "0123456789abcdef" for character in value))


def ensure_configuration() -> HeldWorkspaceRoot:
    global _COLD_WORKSPACE_ROOT_FD
    global _COLD_WORKSPACE_ROOT_BEFORE
    global _COLD_WORKSPACE_ROOT_MOUNT_ID
    # Absolute command gate: prove final pins before consulting inherited
    # descriptors or opening any current or historical surface.
    need(type(FINAL_CURRENT_V16R2_PINS_INSTALLED) is bool and
         FINAL_CURRENT_V16R2_PINS_INSTALLED is True,
         "v16r2 final current pins are not installed; every command is disabled")
    need(all(value not in V16R2_DRAFT_CURRENT_CORE_PINS for value in (
             CONTRACT_FILE_PIN, CONTRACT_OBJECT_PIN, CLOSED_SCHEMA_FILE_PIN,
             PRODUCER_SOURCE_PIN)),
         "v16r2 draft current-core sentinels must be replaced before execution")
    need(sys.flags.isolated == 1 and
         sys.flags.dont_write_bytecode == 1 and
         sys.flags.no_site == 1,
         "combined child requires Python -I -B -S cold execution")
    exec_fd_text = os.environ.get(COLD_EXEC_FD_ENV, "")
    source_fd_text = os.environ.get(COLD_SOURCE_FD_ENV, "")
    coordination_fd_text = os.environ.get(COORDINATION_PARENT_FD_ENV, "")
    root_fd_text = os.environ.get(COLD_WORKSPACE_ROOT_FD_ENV, "")
    authority_fd_texts = tuple(
        os.environ.get(env_name, "")
        for _, env_name in V14_INHERITED_AUTHORITY_EXACT12_FD_ENV_ORDER)
    all_fd_texts = (
        exec_fd_text, source_fd_text, coordination_fd_text, root_fd_text,
        *authority_fd_texts)
    need(all(value.isascii() and value.isdecimal() and len(value) <= 10 and
             int(value) >= 3 for value in all_fd_texts) and
         len(all_fd_texts) == len({int(value) for value in all_fd_texts}) ==
             V16R2_CHILD_PASS_FD_COUNT == 16 and
         EXECUTED_SOURCE_PATH == Path("/proc/self/fd") / exec_fd_text and
         Path(os.path.abspath(sys.argv[0])) == EXECUTED_SOURCE_PATH and
         os.environ.get(COLD_WORKSPACE_ROOT_ENV) == str(ROOT) and
         ROOT.is_absolute() and
         _nonzero_sha256(os.environ.get(COLD_LAUNCHER_SHA_ENV)),
         "four bootstrap plus v14 exact12 pairwise-distinct fds and mandatory "
         "frozen cold-launch bindings")
    # This gate is intentionally before every ROOT/OUT/SELF lstat, openat2, or
    # evidence access.  The interpreter must already be reading an immutable
    # anonymous copy whose bytes equal the separately held installed source.
    _initial_sealed_exec_source_gate(
        int(exec_fd_text), int(source_fd_text))
    need(all(_nonzero_sha256(value) for value in
             (CONTRACT_FILE_PIN, CONTRACT_OBJECT_PIN, CLOSED_SCHEMA_FILE_PIN,
              V3_OFFICIAL_REJECTION_FILE_PIN, V3_OFFICIAL_REJECTION_OBJECT_PIN,
              V4_REJECTION_SUPERSESSION_FILE_PIN,
              V4_REJECTION_SUPERSESSION_OBJECT_PIN,
              V5_OFFICIAL_REJECTION_FILE_PIN,
              V5_OFFICIAL_REJECTION_OBJECT_PIN,
              V6_OFFICIAL_REJECTION_FILE_PIN,
              V6_OFFICIAL_REJECTION_OBJECT_PIN,
              V7_OFFICIAL_REJECTION_FILE_PIN,
              V7_OFFICIAL_REJECTION_OBJECT_PIN,
              V8_OFFICIAL_REJECTION_FILE_PIN,
              V8_OFFICIAL_REJECTION_OBJECT_PIN,
              V9_OFFICIAL_REJECTION_FILE_PIN,
              V9_OFFICIAL_REJECTION_OBJECT_PIN,
              V10_OFFICIAL_REJECTION_FILE_PIN,
              V10_OFFICIAL_REJECTION_OBJECT_PIN,
              V11_OFFICIAL_REJECTION_FILE_PIN,
              V11_OFFICIAL_REJECTION_OBJECT_PIN,
              V12_OFFICIAL_REJECTION_FILE_PIN,
              V12_OFFICIAL_REJECTION_OBJECT_PIN,
              V13_SUPERSESSION_RECEIPT_FILE_PIN,
              V13_SUPERSESSION_RECEIPT_OBJECT_PIN,
              *V13_INCIDENT_EXACT6_PINS.values(),
              PRODUCER_SOURCE_PIN)),
         "all v16r2 static-freeze placeholders must be filled nonzero lowercase 64hex")
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
         "C79g verifier exact filled C78s configuration")
    need(CANDIDATE_A == ROOT / (".cm2-runtime/c79g-v16r2r63y-candidate-a-" + UPSTREAM_CHECKPOINT_OBJECT_PIN) and
         CANDIDATE_B == ROOT / (".cm2-runtime/c79g-v16r2r63y-candidate-b-" + UPSTREAM_CHECKPOINT_OBJECT_PIN) and
         VERIFICATION_A == ROOT / (".cm2-runtime/c79g-v16r2r63y-verification-a-" + UPSTREAM_CHECKPOINT_OBJECT_PIN) and
         VERIFICATION_B == ROOT / (".cm2-runtime/c79g-v16r2r63y-verification-b-" + UPSTREAM_CHECKPOINT_OBJECT_PIN) and
         COMMITTED_COMPLETION == ROOT /
             (".cm2-runtime/c79g-v16r2r63y-committed-completion-" + UPSTREAM_CHECKPOINT_OBJECT_PIN) and
         AUTHORITY_SEAL == ROOT / (".cm2-runtime/cm2-global-authority-heads/c79g-v16r2r63y-" +
                                   UPSTREAM_CHECKPOINT_OBJECT_PIN + ".seal") and
         len(MEMBERS) == 9 and len(COMPLETION_MEMBERS) == 4,
         "fixed full-checkpoint paths and exact surface cardinalities")
    need(_COLD_WORKSPACE_ROOT_FD == -1 and
         _COLD_WORKSPACE_ROOT_BEFORE is None and
         _COLD_WORKSPACE_ROOT_MOUNT_ID == -1,
         "cold workspace root guard binds exactly once")
    root_guard = HeldWorkspaceRoot(
        int(root_fd_text), int(source_fd_text), int(coordination_fd_text))
    _COLD_WORKSPACE_ROOT_FD = root_guard.fd
    _COLD_WORKSPACE_ROOT_BEFORE = root_guard.before
    _COLD_WORKSPACE_ROOT_MOUNT_ID = root_guard.mount_id
    try:
        workspace_root_terminal_replay()
    except BaseException:
        root_guard.close()
        raise
    return root_guard


# Linux-only path/commit primitives.  There is deliberately no compatibility
# fallback: inability to obtain openat2, statx mount identity, or renameat2
# RENAME_NOREPLACE is a hard rejection.
AT_FDCWD = -100
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
    _fields_ = [("flags", ctypes.c_uint64),
                ("mode", ctypes.c_uint64),
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
    need(sys.platform.startswith("linux"), "Linux-only publication protocol")
    library = ctypes.CDLL(None, use_errno=True)
    need(hasattr(library, "syscall") and hasattr(library, "statx") and
         hasattr(library, "renameat2"),
         "kernel/libc openat2+statx+renameat2 required; no fallback")
    return library


def _root_relative(path: Path) -> bytes:
    absolute = Path(os.path.abspath(path))
    need(absolute != ROOT and ROOT in absolute.parents and not path.is_symlink(),
         "exact workspace-root-contained nonsymlink path:" + str(path))
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


def require_v8_positive_and_stage_surfaces_absent() -> None:
    """Prove every fixed v8 positive/stage target is exactly absent."""
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
            raise Reject("officially rejected v8 positive surface exists:" +
                         str(path))
        code = ctypes.get_errno()
        need(code == errno.ENOENT,
             "v8 forbidden-surface proof requires exact ENOENT:" +
             str(path) + ":" + os.strerror(code))


def require_v9_positive_and_stage_surfaces_absent() -> None:
    """Prove every fixed v9 positive/stage target is exactly absent."""
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
            raise Reject("officially rejected v9 positive surface exists:" +
                         str(path))
        code = ctypes.get_errno()
        need(code == errno.ENOENT,
             "v9 forbidden-surface proof requires exact ENOENT:" +
             str(path) + ":" + os.strerror(code))


def require_v10_positive_and_stage_surfaces_absent() -> None:
    """Prove every fixed v10 positive/stage target is exactly absent."""
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
            raise Reject("officially rejected v10 positive surface exists:" +
                         str(path))
        code = ctypes.get_errno()
        need(code == errno.ENOENT,
             "v10 forbidden-surface proof requires exact ENOENT:" +
             str(path) + ":" + os.strerror(code))


def require_v11_positive_and_stage_surfaces_absent() -> None:
    """Prove every fixed v11 positive/stage target is exactly absent."""
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
            raise Reject("officially rejected v11 positive surface exists:" +
                         str(path))
        code = ctypes.get_errno()
        need(code == errno.ENOENT,
             "v11 forbidden-surface proof requires exact ENOENT:" +
             str(path) + ":" + os.strerror(code))


def require_v12_positive_and_stage_surfaces_absent() -> None:
    """Prove every fixed v12 positive/stage target is exactly absent."""
    need(len(V12_ALL_POSITIVE_AND_STAGE_SURFACES) == 12 and
         len(set(V12_ALL_POSITIVE_AND_STAGE_SURFACES)) == 12,
         "v12 exact positive/stage absence path census")
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
            raise Reject("officially rejected v12 positive surface exists:" +
                         str(path))
        code = ctypes.get_errno()
        need(code == errno.ENOENT,
             "v12 forbidden-surface proof requires exact ENOENT:" +
             str(path) + ":" + os.strerror(code))


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


class HeldWorkspaceRoot:
    """Own the launcher-inherited workspace-root dirfd for one invocation."""

    def __init__(self, inherited_fd: int, source_fd: int,
                 coordination_fd: int) -> None:
        self.fd = -1
        try:
            self.fd = os.dup(inherited_fd)
            self.before = os.fstat(self.fd)
            self.mount_id = statx_mount_id(self.fd)
            source_before = os.fstat(source_fd)
            coordination_before = os.fstat(coordination_fd)
            path_before = ROOT.lstat()
            need(stat.S_ISDIR(self.before.st_mode) and
                 stat.S_ISREG(source_before.st_mode) and
                 stat.S_ISDIR(coordination_before.st_mode) and
                 stat.S_ISDIR(path_before.st_mode) and
                 not ROOT.is_symlink() and
                 (self.before.st_dev, self.before.st_ino,
                  self.before.st_mode, self.before.st_nlink) ==
                 (path_before.st_dev, path_before.st_ino,
                  path_before.st_mode, path_before.st_nlink) and
                 statx_mount_id(source_fd) == self.mount_id and
                 statx_mount_id(coordination_fd) == self.mount_id,
                 "inherited root/source/coordination fd types, path identity, and mount")
        except BaseException:
            if self.fd >= 0:
                os.close(self.fd)
                self.fd = -1
            raise

    def terminal_replay(self) -> None:
        workspace_root_terminal_replay()

    def close(self) -> None:
        global _COLD_WORKSPACE_ROOT_FD
        global _COLD_WORKSPACE_ROOT_BEFORE
        global _COLD_WORKSPACE_ROOT_MOUNT_ID
        if self.fd >= 0:
            descriptor = self.fd
            os.close(descriptor)
            self.fd = -1
            if _COLD_WORKSPACE_ROOT_FD == descriptor:
                _COLD_WORKSPACE_ROOT_FD = -1
                _COLD_WORKSPACE_ROOT_BEFORE = None
                _COLD_WORKSPACE_ROOT_MOUNT_ID = -1


def workspace_root_terminal_replay() -> None:
    """Reprove the inherited root fd and its path label without reopening it."""
    need(_COLD_WORKSPACE_ROOT_FD >= 3 and
         _COLD_WORKSPACE_ROOT_BEFORE is not None and
         _COLD_WORKSPACE_ROOT_MOUNT_ID >= 0,
         "cold workspace root guard configured")
    before = _COLD_WORKSPACE_ROOT_BEFORE
    current = os.fstat(_COLD_WORKSPACE_ROOT_FD)
    path_current = ROOT.lstat()
    need(stat.S_ISDIR(current.st_mode) and
         stat.S_ISDIR(path_current.st_mode) and not ROOT.is_symlink() and
         (current.st_dev, current.st_ino, current.st_mode, current.st_nlink) ==
             (before.st_dev, before.st_ino, before.st_mode, before.st_nlink) ==
             (path_current.st_dev, path_current.st_ino,
              path_current.st_mode, path_current.st_nlink) and
         statx_mount_id(_COLD_WORKSPACE_ROOT_FD) ==
             _COLD_WORKSPACE_ROOT_MOUNT_ID,
         "inherited workspace root fd/path identity and mount terminal replay")


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


class HeldPinnedInput:
    """Retain one exact observed file snapshot and terminally replay it.

    The explicit mode is a historical path fact, never an immutability or
    read-only claim.  Same-fd bytes and full identity/mode/link/mount brackets
    detect any live drift during this invocation.
    """
    def __init__(self, path: Path, label: str, expected_mode: int,
                 expected_sha256: str | None = None) -> None:
        self.path = path
        self.label = label
        self.expected_mode = expected_mode
        self.fd = openat2_beneath(path, os.O_RDONLY)
        before_path = path.lstat()
        self.before = os.fstat(self.fd)
        self.mount_id = statx_mount_id(self.fd)
        need(stat.S_ISREG(self.before.st_mode) and
             stat.S_IMODE(self.before.st_mode) == expected_mode and
             self.before.st_nlink == 1 and
             not path.is_symlink() and
             (before_path.st_dev, before_path.st_ino) ==
                 (self.before.st_dev, self.before.st_ino),
             label + ":initial exact observed regular/nlink1 identity and mode")
        self.raw = self._read()
        initial_post = os.fstat(self.fd)
        initial_path_post = path.lstat()
        fingerprint = lambda value: (
            value.st_dev, value.st_ino, value.st_mode, value.st_nlink,
            value.st_size, value.st_mtime_ns, value.st_ctime_ns)
        need(fingerprint(initial_post) == fingerprint(initial_path_post) ==
             fingerprint(self.before), label + ":initial read-bracket stability")
        if expected_sha256 is not None:
            need(sha(self.raw) == expected_sha256, label + ":file pin")

    @classmethod
    def from_creation_fd(
            cls, path: Path, label: str, descriptor: int,
            expected_raw: bytes) -> "HeldPinnedInput":
        """Adopt the O_EXCL creation fd; never reopen before first hold."""
        held = cls.__new__(cls)
        held.path = path
        held.label = label
        held.expected_mode = 0o444
        held.fd = descriptor
        before_path = path.lstat()
        held.before = os.fstat(descriptor)
        held.mount_id = statx_mount_id(descriptor)
        need(stat.S_ISREG(held.before.st_mode) and
             stat.S_IMODE(held.before.st_mode) == 0o444 and
             held.before.st_nlink == 1 and not path.is_symlink() and
             (before_path.st_dev, before_path.st_ino) ==
                 (held.before.st_dev, held.before.st_ino),
             label + ":creation-fd exact regular 0444/nlink1 identity")
        held.raw = held._read()
        initial_post = os.fstat(descriptor)
        initial_path_post = path.lstat()
        fingerprint = lambda value: (
            value.st_dev, value.st_ino, value.st_mode, value.st_nlink,
            value.st_size, value.st_mtime_ns, value.st_ctime_ns)
        need(held.raw == expected_raw,
             label + ":creation-fd initial same-fd byte replay")
        need(fingerprint(initial_post) == fingerprint(initial_path_post) ==
             fingerprint(held.before),
             label + ":creation-fd initial read-bracket stability")
        return held

    @property
    def identity(self) -> tuple[int, int]:
        return (self.before.st_dev, self.before.st_ino)

    def _read(self) -> bytes:
        os.lseek(self.fd, 0, os.SEEK_SET)
        chunks: list[bytes] = []
        while True:
            chunk = os.read(self.fd, 1 << 20)
            if not chunk:
                return b"".join(chunks)
            chunks.append(chunk)

    def terminal_replay(self) -> None:
        pre = os.fstat(self.fd)
        pre_path = self.path.lstat()
        fingerprint = lambda value: (
            value.st_dev, value.st_ino, value.st_mode, value.st_nlink,
            value.st_size, value.st_mtime_ns, value.st_ctime_ns)
        replay = self._read()
        post = os.fstat(self.fd)
        post_path = self.path.lstat()
        need(replay == self.raw and
             fingerprint(pre) == fingerprint(pre_path) ==
             fingerprint(post) == fingerprint(post_path) ==
             fingerprint(self.before) and
             stat.S_IMODE(post.st_mode) == self.expected_mode and
             statx_mount_id(self.fd) == self.mount_id,
             self.label + ":held-fd terminal bytes/path/identity/mount replay")

    def close(self) -> None:
        os.close(self.fd)


class HeldOpaqueMetadata:
    """Hold producer identity with O_PATH; never content-open, read, or hash it."""
    def __init__(self, path: Path, label: str, expected_mode: int) -> None:
        self.path = path
        self.label = label
        self.expected_mode = expected_mode
        need(hasattr(os, "O_PATH") and hasattr(os, "O_NOFOLLOW"),
             label + ":Linux O_PATH|O_NOFOLLOW metadata-only hold required")
        self.fd = openat2_beneath(
            path, os.O_PATH | os.O_NOFOLLOW)
        self.before = os.fstat(self.fd)
        self.mount_id = statx_mount_id(self.fd)
        self.inherited_launcher_coordination_fd = False
        self.launcher_exclusive_lock_confirmed_by_independent_probe = False
        path_before = path.lstat()
        need(stat.S_ISREG(self.before.st_mode) and
             stat.S_IMODE(self.before.st_mode) == expected_mode and
             self.before.st_nlink == 1 and not path.is_symlink() and
             (path_before.st_dev, path_before.st_ino) ==
                 (self.before.st_dev, self.before.st_ino),
             label + ":O_PATH metadata-only exact identity")

    @property
    def identity(self) -> tuple[int, int]:
        return (self.before.st_dev, self.before.st_ino)

    def terminal_replay(self) -> None:
        pre = os.fstat(self.fd)
        pre_path = self.path.lstat()
        post = os.fstat(self.fd)
        post_path = self.path.lstat()
        fingerprint = lambda value: (
            value.st_dev, value.st_ino, value.st_mode, value.st_nlink,
            value.st_size, value.st_mtime_ns, value.st_ctime_ns)
        need(fingerprint(pre) == fingerprint(pre_path) ==
             fingerprint(post) == fingerprint(post_path) ==
             fingerprint(self.before) and
             stat.S_IMODE(post.st_mode) == self.expected_mode and
             statx_mount_id(self.fd) == self.mount_id,
             self.label + ":terminal metadata-only identity/mount replay")

    def close(self) -> None:
        os.close(self.fd)


class HeldInheritedFileView:
    """Attribute view of one continuously held inherited pinned descriptor."""

    def __init__(self, env_name: str, path: Path, file_sha256: str, fd: int,
                 before: os.stat_result, mount_id: int, raw: bytes) -> None:
        self.env_name = env_name
        self.path = path
        self.file_sha256 = file_sha256
        self.fd = fd
        self.before = before
        self.mount_id = mount_id
        self.raw = raw

    @property
    def identity(self) -> tuple[int, int]:
        return (self.before.st_dev, self.before.st_ino)


class HeldInheritedV14AuthorityExact12:
    """Hold the launcher's v14 terminal exact12 before historical traversal.

    Only these twelve descriptors are inherited from the launcher.  Older
    v10--v13 bytes are transitive history and may be opened by pathname only
    after the exact12 same-view gate has passed.  They are retained solely for
    compatibility with the independent historical incident derivations.
    """
    def __init__(self) -> None:
        global _INCIDENT_AUTHORITY_WITNESS
        global _INCIDENT_AUTHORITY_V12_SHAPE
        global _INCIDENT_AUTHORITY_HOLD
        need(_INCIDENT_AUTHORITY_WITNESS is None,
             "single inherited v14 exact12 authority hold per process")
        need(_INCIDENT_AUTHORITY_V12_SHAPE is None and
             _INCIDENT_AUTHORITY_HOLD is None,
             "single inherited v12 incident/predecessor hold per process")
        self.authority_exact12: list[HeldInheritedFileView] = []
        self.files: list[HeldPinnedInput] = []
        self.v12_members: list[HeldPinnedInput] = []
        self.v12_raw_by_path: dict[Path, bytes] = {}
        self.v12_stat_by_path: dict[Path, os.stat_result] = {}
        self.v12_identity_by_path: dict[Path, tuple[int, int]] = {}
        self.v12_mount_by_path: dict[Path, int] = {}
        self.v11_rejection_namespace: HeldDirectory | None = None
        self.v12_rejection_namespace: HeldDirectory | None = None
        self.v13_supersession_receipt: dict[str, Any] | None = None
        exact12_identities: set[tuple[int, int]] = set()
        exact12_mount_ids: set[int] = set()
        try:
            for (role, env_name), witness in zip(
                    V14_INHERITED_AUTHORITY_EXACT12_FD_ENV_ORDER,
                    V14_INHERITED_AUTHORITY_EXACT12, strict=True):
                expected_role, relative_path, file_pin, _ = witness
                need(role == expected_role,
                     "v14 inherited exact12 role/fd-order agreement:" + role)
                path = ROOT / relative_path
                text = os.environ.get(env_name)
                need(isinstance(text, str) and text.isdecimal(),
                     "v14 inherited exact12 fd environment:" + env_name)
                inherited_fd = int(text)
                need(inherited_fd >= 3,
                     "v14 inherited exact12 nonnegative fd:" + env_name)
                descriptor = os.dup(inherited_fd)
                try:
                    inherited_before = os.fstat(inherited_fd)
                    before = os.fstat(descriptor)
                    path_before = path.lstat()
                    mount_id = statx_mount_id(descriptor)
                    inherited_mount_id = statx_mount_id(inherited_fd)
                    access_mode = (
                        fcntl.fcntl(descriptor, fcntl.F_GETFL) & os.O_ACCMODE)
                    need(stat.S_ISREG(before.st_mode) and
                         stat.S_IMODE(before.st_mode) == 0o444 and
                         before.st_nlink == 1 and access_mode == os.O_RDONLY and
                         not path.is_symlink() and
                         (inherited_before.st_dev, inherited_before.st_ino) ==
                             (before.st_dev, before.st_ino) ==
                             (path_before.st_dev, path_before.st_ino) and
                         inherited_mount_id == mount_id,
                         "v14 inherited exact12 identity/mount/mode:" + role)
                    raw = self._pread_all(descriptor, before.st_size)
                    after = os.fstat(descriptor)
                    path_after = path.lstat()
                    fingerprint = lambda value: (
                        value.st_dev, value.st_ino, value.st_mode,
                        value.st_nlink, value.st_size, value.st_mtime_ns,
                        value.st_ctime_ns)
                    need(sha(raw) == file_pin and
                         fingerprint(inherited_before) == fingerprint(before) ==
                         fingerprint(path_before) == fingerprint(after) ==
                         fingerprint(path_after) and
                         statx_mount_id(descriptor) == mount_id,
                         "v14 inherited exact12 same-view pinned read:" + role)
                except BaseException:
                    os.close(descriptor)
                    raise
                exact12_identities.add((before.st_dev, before.st_ino))
                exact12_mount_ids.add(mount_id)
                self.authority_exact12.append(HeldInheritedFileView(
                    env_name, path, file_pin, descriptor, before, mount_id, raw))
            need(len(self.authority_exact12) == len(exact12_identities) ==
                     V16R2_CHILD_AUTHORITY_DESCRIPTOR_COUNT == 12 and
                 len(exact12_mount_ids) == 1,
                 "v14 inherited exact12 unique identities on one mount")
            self.authority_exact12_by_role = {
                role: item for (role, _), item in zip(
                    V14_INHERITED_AUTHORITY_EXACT12_FD_ENV_ORDER,
                    self.authority_exact12, strict=True)}
            exact12_raw_by_role = {
                role: self.authority_exact12_by_role[role].raw
                for role in V14_INHERITED_AUTHORITY_EXACT12_ROLE_ORDER}
            exact12_replay = terminal_replay_v14_inherited_authority_exact12(
                exact12_raw_by_role)
            need(exact12_replay.get("held_authority_descriptor_count") == 12 and
                 exact12_replay.get("child_pass_fd_count") == 16 and
                 exact12_replay.get("formal_global_closure_credit") == 0 and
                 exact12_replay.get("D02_unlock") is False,
                 "v14 inherited exact12 first replay zero-credit boundary")

            # Transitive historical bytes are opened only after the exact12
            # gate.  They never enter the child environment or pass_fds set.
            for env_name, path, file_pin in HISTORICAL_TRANSITIVE_PATHSET_EXACT17:
                held = HeldPinnedInput(
                    path, "transitive historical authority:" + env_name,
                    0o444, file_pin)
                held.env_name = env_name
                held.file_sha256 = file_pin
                self.files.append(held)
        except BaseException:
            for item in reversed(self.files):
                item.close()
            for item in reversed(self.authority_exact12):
                os.close(item.fd)
            raise
        historical_identities = {item.identity for item in self.files}
        historical_mount_ids = {item.mount_id for item in self.files}
        need(len(self.files) == len(historical_identities) == 17 and
             len(historical_mount_ids) == 1,
             "transitive historical exact17 unique same-mount path holds")
        self.by_env = {item.env_name: item for item in self.files}
        need(set(self.by_env) == {
                 env_name for env_name, _, _ in
                 HISTORICAL_TRANSITIVE_PATHSET_EXACT17},
             "transitive historical exact17 compatibility role closure")
        by_env = self.by_env
        rejection = strict_json(
            by_env[V11_REJECTION_FD_ENV].raw,
            "inherited v11 official rejection")
        verify_object(rejection, "inherited v11 official rejection",
                      V11_OFFICIAL_REJECTION_OBJECT_PIN)
        need(len(rejection) > 0 and len(rejection) == 52 and
             rejection.get("status") ==
                 "PERMANENT_FAIL_CLOSED_REJECTION__ZERO_CREDIT" and
             rejection.get("formal_global_closure_credit") == 0 and
             rejection.get("D02_unlock") is False and
             rejection.get("D02_started") is False,
             "inherited v11 rejection exact52 zero-credit authority")
        witness = derive_v10_colon_prefix_witness(
            by_env[V10_PRODUCER_FD_ENV].raw,
            by_env[V9_LAUNCHER_FD_ENV].raw)
        need(witness == V10_COLON_PREFIX_WITNESS and
             len(witness) == 40 and _closed_object_equal(witness) and
             witness.get("successor_clause_truth_vector") == [True] * 15 and
             witness.get("successor_all_clauses_true") is True,
             "inherited incident exact40 independently rederived witness")
        self.v12_shape_incident = derive_v12_v5_rejection_shape_incident(
            by_env[V12_PRODUCER_FD_ENV].raw,
            by_env[V12_CONSUMER_FD_ENV].raw,
            by_env[V12_LAUNCHER_FD_ENV].raw,
            by_env[V5_REJECTION_FD_ENV].raw,
            by_env[V12_REJECTION_FD_ENV].raw)
        need(self.v12_shape_incident == V12_V5_REJECTION_SHAPE_INCIDENT,
             "consumer inherited exact17 reproduces v12 shape incident")
        exact16 = [
            {
                "ordinal": ordinal,
                "role": HISTORICAL_TRANSITIVE_EXACT16_ROLES[
                    ordinal - 1],
                "path": str(path.relative_to(ROOT)),
                "file_sha256": file_pin,
            }
            for ordinal, (_, path, file_pin) in enumerate(
                HISTORICAL_TRANSITIVE_PATHSET_EXACT17[:16], 1)
        ]
        exact16_raw = canonical(exact16)
        need(len(exact16_raw) ==
                 V13_INHERITED_EXACT16_CANONICAL_BYTE_LENGTH and
             sha(exact16_raw) == V13_INHERITED_EXACT16_CANONICAL_SHA256,
             "inherited incident exact16 canonical length and digest")
        supersession = strict_json(
            by_env[V13_SUPERSESSION_RECEIPT_FD_ENV].raw,
            "inherited v13 supersession receipt")
        need(isinstance(supersession, dict),
             "inherited v13 supersession receipt mapping")
        verify_object(
            supersession, "inherited v13 supersession receipt",
            V13_SUPERSESSION_RECEIPT_OBJECT_PIN)
        successor_contract = supersession.get("v14_successor_contract")
        inherited_exact16 = (successor_contract.get(
            "inherited_incident_authority_exact16")
            if isinstance(successor_contract, dict) else None)
        normalized_exact10 = supersession.get(
            "frozen_v13_inherited_incident_authority_exact10_source_contract")
        normalized_rows = (normalized_exact10.get("normalized_ordered_members")
                           if isinstance(normalized_exact10, dict) else None)
        expected_normalized_rows = [
            {
                "ordinal": ordinal,
                "role": HISTORICAL_TRANSITIVE_EXACT16_ROLES[
                    ordinal - 1],
                "fd_environment": env_name.replace("_V16R2_", "_V13_", 1),
                "path": str(path.relative_to(ROOT)),
                "file_sha256": file_pin,
            }
            for ordinal, (env_name, path, file_pin) in enumerate(
                HISTORICAL_TRANSITIVE_PATHSET_EXACT17[:10], 1)
        ]
        normalized_exact10_raw = canonical(expected_normalized_rows)
        live_exact6 = supersession.get(
            "live_successor_required_incident_exact6")
        credit = supersession.get("credit")
        expected_live_exact6 = HISTORICAL_TRANSITIVE_PATHSET_EXACT17[10:16]
        live_rows = (live_exact6.get("ordered_members")
                     if isinstance(live_exact6, dict) else None)
        need(by_env[V13_SUPERSESSION_RECEIPT_FD_ENV].raw ==
                 canonical(supersession) + b"\n" and
             set(supersession) == {
                 "schema", "status", "transition_kind", "receipt_path",
                 "effective_checkpoint_object_sha256", "credit",
                 "v13_no_run_no_publication_attestation",
                 "pyc_contamination_incident", "permanent_rejection_policy",
                 "frozen_v12_authority_anchor",
                 "frozen_v13_prepublication_evidence_exact8",
                 "supplemental_tooling_exact2",
                 "live_successor_required_incident_exact6",
                 "frozen_v13_inherited_incident_authority_exact10_source_contract",
                 "publication_mechanics", "v14_successor_contract",
                 "object_sha256"} and
             supersession.get("schema") ==
                 "cm2.round306c79g.true-global-no-producer-consumer."
                 "v13-prepublication-pyc-contamination-rejection-"
                 "supersession-receipt.v1" and
             supersession.get("status") ==
                 "FROZEN_APPEND_ONLY_V13_PREPUBLICATION_PYC_CONTAMINATION_"
                 "REJECTION__V14_SUCCESSOR_ONLY" and
             supersession.get("transition_kind") ==
                 "PREPUBLICATION_PYC_CONTAMINATION_REJECTION_AND_"
                 "SUPERSESSION_WITHOUT_IMPORT_EXECUTION_RUNTIME_OR_"
                 "POSITIVE_PUBLICATION" and
             supersession.get("receipt_path") ==
                 str(V13_SUPERSESSION_RECEIPT.relative_to(ROOT)) and
             supersession.get("effective_checkpoint_object_sha256") ==
                 UPSTREAM_CHECKPOINT_OBJECT_PIN and
             supersession.get("object_sha256") ==
                 V13_SUPERSESSION_RECEIPT_OBJECT_PIN and
             isinstance(credit, dict) and set(credit) == {
                 "formal_global_closure_credit", "D02_unlock",
                 "D02_gate_credit", "D02_task_credit",
                 "D02_formal_pending_task_count", "D02_started"} and
             credit == {
                 "formal_global_closure_credit": 0, "D02_unlock": False,
                 "D02_gate_credit": 0, "D02_task_credit": 0,
                 "D02_formal_pending_task_count": PENDING_D02,
                 "D02_started": False} and
             isinstance(inherited_exact16, dict) and
             inherited_exact16.get("ordered_member_count") == 16 and
             inherited_exact16.get("inherited_normalized_exact10_count") == 10 and
             inherited_exact16.get("ordered_member_exact_keys") ==
                 ["ordinal", "role", "path", "file_sha256"] and
             inherited_exact16.get("ordered_members") == exact16 and
             inherited_exact16.get("ordered_exact16_canonical_byte_length") ==
                 V13_INHERITED_EXACT16_CANONICAL_BYTE_LENGTH and
             inherited_exact16.get("ordered_exact16_canonical_sha256") ==
                 V13_INHERITED_EXACT16_CANONICAL_SHA256 and
             inherited_exact16.get(
                 "v14_must_live_hold_and_terminally_replay_exact16_plus_this_receipt")
                 is True and
             isinstance(normalized_exact10, dict) and
             normalized_exact10.get("normalized_ordered_member_count") == 10 and
             normalized_exact10.get("normalized_record_exact_keys") ==
                 ["ordinal", "role", "fd_environment", "path", "file_sha256"] and
             normalized_rows == expected_normalized_rows and
             len(normalized_exact10_raw) == 2_657 and
             normalized_exact10.get(
                 "normalized_exact10_canonical_byte_length") == 2_657 and
             sha(normalized_exact10_raw) ==
                 V13_NORMALIZED_EXACT10_CANONICAL_SHA256 and
             normalized_exact10.get("normalized_exact10_canonical_sha256") ==
                 V13_NORMALIZED_EXACT10_CANONICAL_SHA256 and
             isinstance(live_exact6, dict) and
             live_exact6.get("ordered_member_count") == 6 and
             isinstance(live_rows, list) and len(live_rows) == 6 and
             all(isinstance(row, dict) and
                 row.get("path") == str(path.relative_to(ROOT)) and
                 row.get("file_sha256") == file_pin and
                 row.get("frozen_mode") == "0444" and
                 row.get("nlink") == 1
                 for row, (_, path, file_pin) in zip(
                     live_rows, expected_live_exact6, strict=True)) and
             live_exact6.get(
                 "v14_must_live_hold_and_terminally_replay_all_six_plus_this_receipt")
                 is True and
             isinstance(successor_contract, dict) and
             successor_contract.get("successor_version") == 14 and
             successor_contract.get(
                 "v14_current_exact8_first_member_must_be_this_receipt") is True and
             successor_contract.get(
                 "v14_must_preserve_v12_exact10_and_official_rejection") is True and
             successor_contract.get(
                 "v14_predecessor_unique_live_identity_count") ==
                 V14_HISTORICAL_PREDECESSOR_UNIQUE_LIVE_IDENTITY_COUNT and
             successor_contract.get(
                 "v14_prepublication_unique_live_identity_count") ==
                 V14_HISTORICAL_PREPUBLICATION_UNIQUE_LIVE_IDENTITY_COUNT and
             successor_contract.get(
                 "v14_terminal_unique_live_identity_count") ==
                 V14_HISTORICAL_TERMINAL_UNIQUE_LIVE_IDENTITY_COUNT and
             successor_contract.get("v14_terminal_group_vector") ==
                 list(V14_HISTORICAL_TERMINAL_GROUP_VECTOR) and
             successor_contract.get(
                 "v14_must_pin_this_receipt_file_and_object_sha256") is True and
             successor_contract.get(
                 "this_receipt_does_not_pin_any_v14_successor_byte") is True,
             "inherited v13 supersession exact17 receipt contract")
        self.v13_supersession_receipt = copy.deepcopy(supersession)
        self._hold_and_validate_v12_predecessor()
        _INCIDENT_AUTHORITY_WITNESS = copy.deepcopy(witness)
        _INCIDENT_AUTHORITY_V12_SHAPE = copy.deepcopy(self.v12_shape_incident)
        _INCIDENT_AUTHORITY_HOLD = self

    def _hold_and_validate_v12_predecessor(self) -> None:
        incident_env_by_path = {
            V11_OFFICIAL_REJECTION: V11_REJECTION_FD_ENV,
            V12_FROZEN_PRODUCER: V12_PRODUCER_FD_ENV,
            V12_FROZEN_CONSUMER: V12_CONSUMER_FD_ENV,
            V12_FROZEN_LAUNCHER: V12_LAUNCHER_FD_ENV,
        }
        self.v12_members = [
            HeldPinnedInput(path, "published v12 readable held:" + name,
                            0o444, file_sha256)
            for name, (path, file_sha256) in V12_FROZEN_FILES.items()
            if path not in incident_env_by_path
        ]
        member_by_path = {item.path: item for item in self.v12_members}
        need(len(member_by_path) == len(self.v12_members) == 6,
             "published v12 exact10 has exact6 ordinary held members")
        raw_by_path = {
            path: self.by_env[env_name].raw
            for path, env_name in incident_env_by_path.items()
        }
        raw_by_path.update({item.path: item.raw for item in self.v12_members})
        stat_by_path = {
            path: self.by_env[env_name].before
            for path, env_name in incident_env_by_path.items()
        }
        stat_by_path.update({item.path: item.before for item in self.v12_members})
        identity_by_path = {
            path: self.by_env[env_name].identity
            for path, env_name in incident_env_by_path.items()
        }
        identity_by_path.update({item.path: item.identity for item in self.v12_members})
        mount_by_path = {
            path: self.by_env[env_name].mount_id
            for path, env_name in incident_env_by_path.items()
        }
        mount_by_path.update({item.path: item.mount_id for item in self.v12_members})
        need(set(raw_by_path) == {path for path, _ in V12_FROZEN_FILES.values()} and
             len(raw_by_path) == len(set(identity_by_path.values())) == 10 and
             len(set(mount_by_path.values())) == 1 and
             tuple(V12_FROZEN_FILES[name][1] for name in V12_EXACT10_ORDER) ==
                 V12_PUBLISHED_EXACT10_FILE_SHA256_ORDER,
             "published v12 exact10 complete unique same-mount pinned identity")
        self.v12_raw_by_path = raw_by_path
        self.v12_stat_by_path = stat_by_path
        self.v12_identity_by_path = identity_by_path
        self.v12_mount_by_path = mount_by_path
        for name in V12_EXACT10_ORDER:
            path, file_pin = V12_FROZEN_FILES[name]
            raw = raw_by_path[path]
            need(sha_bytes(raw) == file_pin,
                 "published v12 exact10 file pin:" + name)
            if name in V12_FROZEN_OBJECTS:
                value = strict_json(raw, "published v12 object:" + name)
                need(isinstance(value, dict), "published v12 object mapping:" + name)
                verify_object(value, "published v12 object:" + name,
                              V12_FROZEN_OBJECTS[name])
        exact8_expected = [
            {"file_sha256": V12_FROZEN_FILES[name][1],
             "entry_name": str(V12_FROZEN_FILES[name][0].relative_to(ROOT))}
            for name in V12_EXACT10_ORDER[:8]
        ]
        manifest_path = V12_FROZEN_FILES["cold_manifest_v12"][0]
        outer_path = V12_FROZEN_FILES["cold_outer_v12"][0]
        manifest = parse_manifest_ordered(
            raw_by_path[manifest_path], "published v12 exact8 manifest")
        outer = strict_json(raw_by_path[outer_path], "published v12 outer-last")
        need(isinstance(outer, dict), "published v12 outer-last mapping")
        verify_object(outer, "published v12 outer-last",
                      V12_FROZEN_OBJECTS["cold_outer_v12"])
        chronology = cold_publication_chronology(
            [stat_by_path[V12_FROZEN_FILES[name][0]]
             for name in V12_EXACT10_ORDER[:8]],
            stat_by_path[manifest_path], stat_by_path[outer_path])
        rejection_before = self.by_env[V12_REJECTION_FD_ENV].before
        need(manifest == exact8_expected and
             outer.get("exact8_ordered_entries") == [
                 {"path": item["entry_name"], "file_sha256": item["file_sha256"]}
                 for item in exact8_expected] and
             outer.get("status") ==
                 "FROZEN_COLD_LAUNCH_OUTER_LAST__EXACT8_MANIFEST_CLOSED__RUNTIME_DEFERRED" and
             outer.get("formal_global_closure_credit") == 0 and
             outer.get("D02_unlock") is False and
             outer.get("runtime_executed_during_static_freeze") is False and
             all(chronology.values()) and
             max(stat_by_path[outer_path].st_mtime_ns,
                 stat_by_path[outer_path].st_ctime_ns) <
                 min(rejection_before.st_mtime_ns, rejection_before.st_ctime_ns),
             "published v12 exact10 manifest/outer/rejection chronology")
        self.v11_rejection_namespace = HeldDirectory(
            V11_OFFICIAL_REJECTION.parent, {V11_OFFICIAL_REJECTION.name},
            0o555, 2, "published v12 shared v11 rejection singleton namespace")
        self.v12_rejection_namespace = HeldDirectory(
            V12_OFFICIAL_REJECTION.parent, {V12_OFFICIAL_REJECTION.name},
            0o555, 2, "official v12 rejection singleton namespace")
        need({self.v11_rejection_namespace.mount_id,
              self.v12_rejection_namespace.mount_id} <=
                 set(mount_by_path.values()) |
                 {self.by_env[V12_REJECTION_FD_ENV].mount_id},
             "published v12 exact10/v11 and v12 rejection singletons same mount")
        self._require_v12_positive_and_stage_absence()

    @staticmethod
    def _require_v12_positive_and_stage_absence() -> None:
        require_v12_positive_and_stage_surfaces_absent()

    def v12_exact10_identities(self) -> set[tuple[int, int]]:
        incident_members = (
            self.by_env[V11_REJECTION_FD_ENV],
            self.by_env[V12_PRODUCER_FD_ENV],
            self.by_env[V12_CONSUMER_FD_ENV],
            self.by_env[V12_LAUNCHER_FD_ENV],
        )
        return ({item.identity for item in incident_members} |
                {item.identity for item in self.v12_members})

    def v12_exact10_mount_ids(self) -> set[int]:
        incident_members = (
            self.by_env[V11_REJECTION_FD_ENV],
            self.by_env[V12_PRODUCER_FD_ENV],
            self.by_env[V12_CONSUMER_FD_ENV],
            self.by_env[V12_LAUNCHER_FD_ENV],
        )
        return ({item.mount_id for item in incident_members} |
                {item.mount_id for item in self.v12_members})

    def v13_incident_source_identities(self) -> set[tuple[int, int]]:
        return {
            self.by_env[env_name].identity for env_name in (
                V13_PRODUCER_FD_ENV, V13_CONSUMER_FD_ENV,
                V13_LAUNCHER_FD_ENV)}

    def v13_incident_pyc_identities(self) -> set[tuple[int, int]]:
        return {
            self.by_env[env_name].identity for env_name in (
                V13_PRODUCER_PYC_FD_ENV, V13_CONSUMER_PYC_FD_ENV,
                V13_LAUNCHER_PYC_FD_ENV)}

    def v13_incident_mount_ids(self) -> set[int]:
        return {
            self.by_env[env_name].mount_id for env_name in (
                V13_PRODUCER_FD_ENV, V13_CONSUMER_FD_ENV,
                V13_LAUNCHER_FD_ENV, V13_PRODUCER_PYC_FD_ENV,
                V13_CONSUMER_PYC_FD_ENV, V13_LAUNCHER_PYC_FD_ENV)}

    def v12_rejection_identity(self) -> tuple[int, int]:
        return self.by_env[V12_REJECTION_FD_ENV].identity

    def v13_supersession_identity(self) -> tuple[int, int]:
        return self.by_env[V13_SUPERSESSION_RECEIPT_FD_ENV].identity

    def v14_exact10_identities(self) -> set[tuple[int, int]]:
        return {
            self.authority_exact12_by_role[role].identity
            for role in V14_INHERITED_AUTHORITY_EXACT12_ROLE_ORDER[:10]}

    def v14_exact10_mount_ids(self) -> set[int]:
        return {
            self.authority_exact12_by_role[role].mount_id
            for role in V14_INHERITED_AUTHORITY_EXACT12_ROLE_ORDER[:10]}

    def v14_rejection_identity(self) -> tuple[int, int]:
        return self.authority_exact12_by_role[
            "v14_official_rejection"].identity

    def v14_supersession_identity(self) -> tuple[int, int]:
        return self.authority_exact12_by_role[
            "v14_registry_shape_drift_supersession_receipt"].identity

    @staticmethod
    def _pread_all(descriptor: int, size: int) -> bytes:
        chunks: list[bytes] = []
        offset = 0
        while offset < size:
            chunk = os.pread(descriptor, min(1 << 20, size - offset), offset)
            need(bool(chunk), "inherited incident fd premature EOF")
            chunks.append(chunk)
            offset += len(chunk)
        need(os.pread(descriptor, 1, size) == b"",
             "inherited incident fd exact EOF")
        return b"".join(chunks)

    def terminal_replay(self) -> None:
        exact12_raw_by_role: dict[str, bytes] = {}
        for (role, _), item in zip(
                V14_INHERITED_AUTHORITY_EXACT12_FD_ENV_ORDER,
                self.authority_exact12, strict=True):
            descriptor = item.fd
            before = os.fstat(descriptor)
            path_before = item.path.lstat()
            raw = self._pread_all(descriptor, item.before.st_size)
            after = os.fstat(descriptor)
            path_after = item.path.lstat()
            fingerprint = lambda value: (
                value.st_dev, value.st_ino, value.st_mode, value.st_nlink,
                value.st_size, value.st_mtime_ns, value.st_ctime_ns)
            need(raw == item.raw and sha(raw) == item.file_sha256 and
                 fingerprint(before) == fingerprint(path_before) ==
                 fingerprint(after) == fingerprint(path_after) ==
                 fingerprint(item.before) and
                 statx_mount_id(descriptor) == item.mount_id,
                 "v14 inherited exact12 terminal same-view replay:" + role)
            exact12_raw_by_role[role] = raw
        exact12_replay = terminal_replay_v14_inherited_authority_exact12(
            exact12_raw_by_role)
        need(exact12_replay.get("held_authority_descriptor_count") == 12 and
             exact12_replay.get("child_pass_fd_count") == 16 and
             exact12_replay.get("formal_global_closure_credit") == 0 and
             exact12_replay.get("D02_unlock") is False,
             "v14 inherited exact12 terminal replay zero-credit boundary")
        for item in self.files:
            descriptor = item.fd
            before = os.fstat(descriptor)
            path_before = item.path.lstat()
            raw = self._pread_all(descriptor, item.before.st_size)
            after = os.fstat(descriptor)
            path_after = item.path.lstat()
            fingerprint = lambda value: (
                value.st_dev, value.st_ino, value.st_mode, value.st_nlink,
                value.st_size, value.st_mtime_ns, value.st_ctime_ns)
            need(raw == item.raw and sha(raw) == item.file_sha256 and
                 fingerprint(before) == fingerprint(path_before) ==
                 fingerprint(after) == fingerprint(path_after) ==
                 fingerprint(item.before) and
                 statx_mount_id(descriptor) == item.mount_id,
                 "transitive historical terminal same-view replay:" +
                 item.env_name)
        for item in self.v12_members:
            item.terminal_replay()
        need(self.v11_rejection_namespace is not None,
             "held v11 rejection singleton namespace remains owned")
        self.v11_rejection_namespace.terminal_replay()
        need(self.v12_rejection_namespace is not None,
             "held v12 rejection singleton namespace remains owned")
        self.v12_rejection_namespace.terminal_replay()
        self._require_v12_positive_and_stage_absence()
        replayed = derive_v12_v5_rejection_shape_incident(
            self.by_env[V12_PRODUCER_FD_ENV].raw,
            self.by_env[V12_CONSUMER_FD_ENV].raw,
            self.by_env[V12_LAUNCHER_FD_ENV].raw,
            self.by_env[V5_REJECTION_FD_ENV].raw,
            self.by_env[V12_REJECTION_FD_ENV].raw)
        need(replayed == self.v12_shape_incident ==
                 V12_V5_REJECTION_SHAPE_INCIDENT,
             "consumer v12 exact10 incident terminal replay")
        v10_replayed = derive_v10_colon_prefix_witness(
            self.by_env[V10_PRODUCER_FD_ENV].raw,
            self.by_env[V9_LAUNCHER_FD_ENV].raw)
        need(v10_replayed == _INCIDENT_AUTHORITY_WITNESS ==
                 V10_COLON_PREFIX_WITNESS,
             "consumer v10 inherited exact10 witness terminal replay")
        supersession_replayed = strict_json(
            self.by_env[V13_SUPERSESSION_RECEIPT_FD_ENV].raw,
            "terminal inherited v13 supersession receipt")
        need(isinstance(supersession_replayed, dict) and
             supersession_replayed == self.v13_supersession_receipt and
             self.by_env[V13_SUPERSESSION_RECEIPT_FD_ENV].raw ==
                 canonical(supersession_replayed) + b"\n",
             "consumer transitive historical supersession terminal replay")
        verify_object(
            supersession_replayed,
            "terminal inherited v13 supersession receipt",
            V13_SUPERSESSION_RECEIPT_OBJECT_PIN)

    def close(self) -> None:
        global _INCIDENT_AUTHORITY_WITNESS
        global _INCIDENT_AUTHORITY_V12_SHAPE
        global _INCIDENT_AUTHORITY_HOLD
        failures: list[str] = []
        if self.v12_rejection_namespace is not None:
            try:
                self.v12_rejection_namespace.close()
            except OSError as exc:
                failures.append("v12_rejection_namespace:" + str(exc))
            self.v12_rejection_namespace = None
        if self.v11_rejection_namespace is not None:
            try:
                self.v11_rejection_namespace.close()
            except OSError as exc:
                failures.append("v11_rejection_namespace:" + str(exc))
            self.v11_rejection_namespace = None
        for item in reversed(self.v12_members):
            try:
                item.close()
            except OSError as exc:
                failures.append("v12_member:" + str(exc))
        self.v12_members.clear()
        self.v12_raw_by_path.clear()
        self.v12_stat_by_path.clear()
        self.v12_identity_by_path.clear()
        self.v12_mount_by_path.clear()
        self.v13_supersession_receipt = None
        for item in reversed(self.files):
            try:
                os.close(item.fd)
            except OSError as exc:
                failures.append(item.env_name + ":" + str(exc))
        self.files.clear()
        for item in reversed(self.authority_exact12):
            try:
                os.close(item.fd)
            except OSError as exc:
                failures.append("v14_exact12:" + item.env_name + ":" + str(exc))
        self.authority_exact12.clear()
        self.authority_exact12_by_role.clear()
        _INCIDENT_AUTHORITY_WITNESS = None
        _INCIDENT_AUTHORITY_V12_SHAPE = None
        _INCIDENT_AUTHORITY_HOLD = None
        if failures:
            raise Reject("inherited v14 exact12 close:" + "|".join(failures))


class HeldDirectory:
    def __init__(self, path: Path, names: set[str], required_mode: int,
                 required_nlink: int, label: str) -> None:
        self.path = path
        self.names = set(names)
        self.label = label
        self.required_mode = required_mode
        self.required_nlink = required_nlink
        self.fd = openat2_beneath(path, os.O_RDONLY | os.O_DIRECTORY)
        before_path = path.lstat()
        self.before = os.fstat(self.fd)
        self.mount_id = statx_mount_id(self.fd)
        initial_universe = set(os.listdir(self.fd))
        initial_post = os.fstat(self.fd)
        initial_path_post = path.lstat()
        fingerprint = lambda value: (
            value.st_dev, value.st_ino, value.st_mode, value.st_nlink,
            value.st_mtime_ns, value.st_ctime_ns)
        need(stat.S_ISDIR(self.before.st_mode) and
             stat.S_IMODE(self.before.st_mode) == required_mode and
             self.before.st_nlink == required_nlink and
             not path.is_symlink() and
             (before_path.st_dev, before_path.st_ino) ==
                 (self.before.st_dev, self.before.st_ino) and
             initial_universe == self.names and
             fingerprint(initial_post) == fingerprint(initial_path_post) ==
                 fingerprint(self.before),
             label + ":initial exact directory surface")

    @classmethod
    def from_existing_fd(
            cls, path: Path, names: set[str], required_mode: int,
            required_nlink: int,
            label: str, descriptor: int) -> "HeldDirectory":
        """Adopt a dup of an already-held directory fd without path reopen."""
        held = cls.__new__(cls)
        held.path = path
        held.names = set(names)
        held.label = label
        held.required_mode = required_mode
        held.required_nlink = required_nlink
        held.fd = descriptor
        before_path = path.lstat()
        held.before = os.fstat(descriptor)
        held.mount_id = statx_mount_id(descriptor)
        initial_universe = set(os.listdir(descriptor))
        initial_post = os.fstat(descriptor)
        initial_path_post = path.lstat()
        fingerprint = lambda value: (
            value.st_dev, value.st_ino, value.st_mode, value.st_nlink,
            value.st_mtime_ns, value.st_ctime_ns)
        need(stat.S_ISDIR(held.before.st_mode) and
             stat.S_IMODE(held.before.st_mode) == required_mode and
             held.before.st_nlink == required_nlink and
             not path.is_symlink() and
             (before_path.st_dev, before_path.st_ino) ==
                 (held.before.st_dev, held.before.st_ino) and
             initial_universe == held.names and
             fingerprint(initial_post) == fingerprint(initial_path_post) ==
                 fingerprint(held.before),
             label + ":adopted-fd exact directory surface")
        return held

    @property
    def identity(self) -> tuple[int, int]:
        return (self.before.st_dev, self.before.st_ino)

    def terminal_replay(self) -> None:
        pre = os.fstat(self.fd)
        pre_path = self.path.lstat()
        fingerprint = lambda value: (
            value.st_dev, value.st_ino, value.st_mode, value.st_nlink,
            value.st_mtime_ns, value.st_ctime_ns)
        universe_pre = set(os.listdir(self.fd))
        middle = os.fstat(self.fd)
        middle_path = self.path.lstat()
        universe_post = set(os.listdir(self.fd))
        post = os.fstat(self.fd)
        post_path = self.path.lstat()
        need(fingerprint(pre) == fingerprint(pre_path) ==
             fingerprint(middle) == fingerprint(middle_path) ==
             fingerprint(post) == fingerprint(post_path) ==
             fingerprint(self.before) and
             stat.S_IMODE(post.st_mode) == self.required_mode and
             post.st_nlink == self.required_nlink and
             statx_mount_id(self.fd) == self.mount_id and
             universe_pre == universe_post == self.names,
             self.label + ":terminal exact directory identity/mount/universe replay")

    def close(self) -> None:
        os.close(self.fd)


class HeldCommitParent:
    """One parent dirfd held from staging creation through NOCLOBBER commit."""
    def __init__(self, path: Path, label: str) -> None:
        self.path = path
        self.label = label
        self.fd = openat2_beneath(path, os.O_RDONLY | os.O_DIRECTORY)
        self.before = os.fstat(self.fd)
        self.mount_id = statx_mount_id(self.fd)
        path_before = path.lstat()
        need(stat.S_ISDIR(self.before.st_mode) and not path.is_symlink() and
             (path_before.st_dev, path_before.st_ino) ==
                 (self.before.st_dev, self.before.st_ino),
             label + ":held parent initial identity")

    @classmethod
    def from_creation_fd(
            cls, path: Path, label: str, descriptor: int,
            required_mode: int) -> "HeldCommitParent":
        """Adopt the directory fd opened immediately after mkdirat."""
        held = cls.__new__(cls)
        held.path = path
        held.label = label
        held.fd = descriptor
        os.fchmod(descriptor, required_mode)
        os.fsync(descriptor)
        held.before = os.fstat(descriptor)
        held.mount_id = statx_mount_id(descriptor)
        held.inherited_launcher_coordination_fd = False
        held.launcher_exclusive_lock_confirmed_by_independent_probe = False
        path_before = path.lstat()
        need(stat.S_ISDIR(held.before.st_mode) and
             stat.S_IMODE(held.before.st_mode) == required_mode and
             not path.is_symlink() and
             (path_before.st_dev, path_before.st_ino) ==
                 (held.before.st_dev, held.before.st_ino),
             label + ":mkdirat-to-held-fd exact directory identity")
        return held

    @classmethod
    def from_inherited_launcher_coordination_fd(
            cls, path: Path, label: str, inherited_descriptor: int
            ) -> "HeldCommitParent":
        """Duplicate the launcher-owned locked runtime parent open description."""
        need(path == RUNTIME and inherited_descriptor >= 0,
             label + ":exact inherited runtime coordination fd")
        inherited_before = os.fstat(inherited_descriptor)
        descriptor = os.dup(inherited_descriptor)
        held = cls.__new__(cls)
        held.path = path
        held.label = label
        held.fd = descriptor
        held.before = os.fstat(descriptor)
        held.mount_id = statx_mount_id(descriptor)
        held.inherited_launcher_coordination_fd = True
        path_before = path.lstat()
        need(stat.S_ISDIR(inherited_before.st_mode) and
             stat.S_ISDIR(held.before.st_mode) and not path.is_symlink() and
             (inherited_before.st_dev, inherited_before.st_ino) ==
                 (held.before.st_dev, held.before.st_ino) ==
                 (path_before.st_dev, path_before.st_ino),
             label + ":launcher fd/dup/fixed runtime path exact identity")
        need(statx_mount_id(inherited_descriptor) == held.mount_id,
             label + ":launcher fd/dup statx mount identity")
        probe = openat2_beneath(path, os.O_RDONLY | os.O_DIRECTORY)
        launcher_lock_confirmed = False
        try:
            probe_info = os.fstat(probe)
            need((probe_info.st_dev, probe_info.st_ino) ==
                 (held.before.st_dev, held.before.st_ino) and
                 statx_mount_id(probe) == held.mount_id,
                 label + ":independent lock-probe identity/mount")
            try:
                fcntl.flock(probe, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except OSError as exc:
                need(exc.errno in {errno.EACCES, errno.EAGAIN},
                     label + ":unexpected launcher-lock probe failure")
                launcher_lock_confirmed = True
        finally:
            os.close(probe)
        need(launcher_lock_confirmed is True,
             label + ":launcher must already own exclusive flock on inherited OFD")
        held.launcher_exclusive_lock_confirmed_by_independent_probe = True
        return held

    def terminal_identity(self) -> None:
        current = os.fstat(self.fd)
        path_current = self.path.lstat()
        need((current.st_dev, current.st_ino) ==
             (self.before.st_dev, self.before.st_ino) and
             (path_current.st_dev, path_current.st_ino) ==
             (self.before.st_dev, self.before.st_ino) and
             statx_mount_id(self.fd) == self.mount_id,
             self.label + ":held parent terminal identity/mount")

    def mkdir_exclusive(self, name: str, mode: int) -> "HeldCommitParent":
        need("/" not in name and name not in {"", ".", ".."},
             self.label + ":mkdir single component")
        os.mkdir(name, mode, dir_fd=self.fd)
        descriptor = -1
        transferred = False
        try:
            # This open is deliberately the first operation after mkdirat.
            descriptor = os.open(
                name, os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC |
                getattr(os, "O_NOFOLLOW", 0), dir_fd=self.fd)
            held = HeldCommitParent.from_creation_fd(
                self.path / name, self.label + ":new held child", descriptor, mode)
            os.fsync(self.fd)
            transferred = True
            return held
        finally:
            if descriptor >= 0 and not transferred:
                os.close(descriptor)

    def exclusive_file(
            self, name: str, raw: bytes, mode: int = 0o444) -> HeldPinnedInput:
        need("/" not in name and name not in {"", ".", ".."},
             self.label + ":file single component")
        descriptor = os.open(name, os.O_RDWR | os.O_CREAT | os.O_EXCL |
                             os.O_CLOEXEC | getattr(os, "O_NOFOLLOW", 0),
                             mode, dir_fd=self.fd)
        transferred = False
        try:
            view = memoryview(raw)
            while view:
                count = os.write(descriptor, view)
                need(count > 0, self.label + ":stage write")
                view = view[count:]
            os.fchmod(descriptor, mode)
            os.fsync(descriptor)
            held = HeldPinnedInput.from_creation_fd(
                self.path / name, self.label + ":new held file", descriptor, raw)
            os.fsync(self.fd)
            transferred = True
            return held
        finally:
            if not transferred:
                os.close(descriptor)

    def close(self) -> None:
        os.close(self.fd)


def held_child_lstat_or_absent(
        parent: HeldCommitParent, name: str, label: str) -> os.stat_result | None:
    need("/" not in name and name not in {"", ".", ".."},
         label + ":single held-parent component")
    try:
        info = os.stat(name, dir_fd=parent.fd, follow_symlinks=False)
    except FileNotFoundError:
        return None
    path_info = (parent.path / name).lstat()
    need((info.st_dev, info.st_ino, info.st_mode) ==
         (path_info.st_dev, path_info.st_ino, path_info.st_mode),
         label + ":held-parent child equals exact lexical path")
    return info


class HeldInputSet:
    def __init__(self, files: list[HeldPinnedInput], directories: list[HeldDirectory]) -> None:
        self.files = files
        self.directories = directories
        identities = [item.identity for item in files] + [item.identity for item in directories]
        need(len(identities) == len(set(identities)),
             "global file/directory identity uniqueness; reject hardlink/dev+ino/mount aliases")

    def terminal_replay(self) -> None:
        for item in self.files:
            item.terminal_replay()
        for item in self.directories:
            item.terminal_replay()

    def close(self) -> None:
        for item in reversed(self.files):
            item.close()
        for item in reversed(self.directories):
            item.close()


def rename_noreplace(
        parent: HeldCommitParent, source_name: str, destination_name: str,
        expected_identity: tuple[int, int], expected_mount_id: int) -> None:
    """Atomic commit through one parent dirfd held since stage creation."""
    need("/" not in source_name and "/" not in destination_name and
         source_name not in {"", ".", ".."} and
         destination_name not in {"", ".", ".."},
         "NOCLOBBER source/destination are single held-parent basenames")
    parent.terminal_identity()
    workspace_root_terminal_replay()
    source_fd = os.open(
        source_name, getattr(os, "O_PATH", os.O_RDONLY) | os.O_CLOEXEC |
        getattr(os, "O_NOFOLLOW", 0), dir_fd=parent.fd)
    try:
        source_before = os.fstat(source_fd)
        need((source_before.st_dev, source_before.st_ino) == expected_identity and
             statx_mount_id(source_fd) == expected_mount_id == parent.mount_id,
             "NOCLOBBER reopened source equals long-held stage identity/mount")
        library = _linux_libc()
        ctypes.set_errno(0)
        outcome = library.renameat2(
            ctypes.c_int(parent.fd), ctypes.c_char_p(os.fsencode(source_name)),
            ctypes.c_int(parent.fd), ctypes.c_char_p(os.fsencode(destination_name)),
            ctypes.c_uint(RENAME_NOREPLACE))
        if outcome != 0:
            code = ctypes.get_errno()
            raise Reject("renameat2 RENAME_NOREPLACE fail closed:" + os.strerror(code))
        destination_after = os.stat(
            destination_name, dir_fd=parent.fd, follow_symlinks=False)
        need((destination_after.st_dev, destination_after.st_ino) ==
             expected_identity,
             "postcommit destination is exact long-held staging inode")
        try:
            os.stat(source_name, dir_fd=parent.fd, follow_symlinks=False)
        except FileNotFoundError:
            pass
        else:
            raise Reject("postcommit source did not disappear")
        os.fsync(parent.fd)
        parent.terminal_identity()
        workspace_root_terminal_replay()
        return
    finally:
        os.close(source_fd)


def rooted(text: str) -> Path:
    candidate = Path(text)
    path = Path(os.path.abspath(str(candidate if candidate.is_absolute() else ROOT / candidate)))
    need(path == ROOT or ROOT in path.parents, "workspace path")
    return path


def gzip_rows(raw: bytes, label: str) -> list[dict[str, Any]]:
    decoder = zlib.decompressobj(16 + zlib.MAX_WBITS)
    try:
        plain = decoder.decompress(raw) + decoder.flush()
    except zlib.error as exc:
        raise Reject(label + ":gzip") from exc
    need(decoder.eof is True and
         not decoder.unused_data and not decoder.unconsumed_tail,
         label + ":one complete gzip member")
    need(plain.endswith(b"\n"), label + ":newline")
    rows: list[dict[str, Any]] = []
    for index, line in enumerate(plain.splitlines(), 1):
        need(bool(line), label + ":blank line")
        row = strict_json(line, f"{label}:{index}")
        need(isinstance(row, dict), label + ":object row")
        verify_row(row, f"{label}:{index}")
        rows.append(row)
    return rows


def parse_manifest_ordered(raw: bytes, label: str) -> list[dict[str, str]]:
    need(raw.endswith(b"\n"), label + ":newline")
    out: list[dict[str, str]] = []
    seen: set[str] = set()
    for line in raw.decode("ascii").splitlines():
        parts = line.split("  ", 1)
        need(len(parts) == 2 and len(parts[0]) == 64 and parts[1] not in seen, label + ":entry")
        seen.add(parts[1])
        out.append({"file_sha256": parts[0], "entry_name": parts[1]})
    return out


def parse_manifest(raw: bytes, label: str) -> dict[str, str]:
    return {entry["entry_name"]: entry["file_sha256"]
            for entry in parse_manifest_ordered(raw, label)}


def candidate_install_protocol() -> dict[str, Any]:
    return {
        "staging_path_template":
            ".cm2-runtime/.c79g-v16r2r63y-candidate-stage-{a|b}-" + UPSTREAM_CHECKPOINT_OBJECT_PIN,
        "fixed_target_set": [str(CANDIDATE_A.relative_to(ROOT)),
                             str(CANDIDATE_B.relative_to(ROOT))],
        "actual_orientation_or_stage_path_persisted_in_candidate_bytes": False,
        "orientation_invariant_descriptor_preserves_full_exact9_A_B_byte_identity": True,
        "held_parent_path": str(RUNTIME.relative_to(ROOT)),
        "launcher_owned_coordination_parent_fd_required": True,
        "official_writer_coordination_lock_api":
            "launcher_owned_fcntl.flock(LOCK_EX)",
        "all_official_runtime_writers_must_share_coordination_lock": True,
        "coordination_lock_not_claimed_as_same_uid_or_filesystem_admin_security_boundary": True,
        "staging_and_target_single_components_under_same_held_parent_dirfd": True,
        "stage_held_from_immediate_post_mkdir_open_until_postcommit": True,
        "all_exact9_members_created_O_EXCL_and_held_from_creation": True,
        "all_exact9_members_fsynced_and_mode_0444_before_commit": True,
        "stage_directory_fsynced_and_mode_0555_before_commit": True,
        "commit_operation": "RENAMEAT2_RENAME_NOREPLACE",
        "ordinary_rename_replace_or_fallback_allowed": False,
        "live_consumer_rederives_fixed_A_B_paths_and_revalidates_both_surfaces": True,
        "postrename_destination_must_equal_creation_held_stage_identity": True,
        "parent_fsync_required_for_crash_durability_after_namespace_commit": True,
        "parent_fsync_not_claimed_to_precede_namespace_visibility": True,
    }


def hold_c42_full10_union_candidate9() -> HeldInputSet:
    """Hold exact C42/C53 semantics under observed historical mode policy."""
    directories = [
        HeldDirectory(C42_CANDIDATE_DIR,
                      C42_CANDIDATE_MANIFEST_MEMBERS | {"root_manifest.sha256"},
                      C42_CANDIDATE_DIRECTORY_EXPECTED_MODE, 2,
                      "C42 historical candidate exact9"),
        HeldDirectory(C42_INDEPENDENT_AUDIT_DIR,
                      {C42_INDEPENDENT_AUDIT_PATH.name},
                      C42_INDEPENDENT_AUDIT_DIRECTORY_EXPECTED_MODE, 2,
                      "C42 historical independent-audit exact1"),
        HeldDirectory(C42_INSTALLATION_RECEIPT_DIR,
                      {C42_INSTALLATION_RECEIPT_PATH.name},
                      C42_INSTALLATION_RECEIPT_DIRECTORY_EXPECTED_MODE, 2,
                      "C42 historical installation-receipt exact1"),
    ]
    files: list[HeldPinnedInput] = []
    by_path: dict[Path, HeldPinnedInput] = {}
    for name in C42_C53_PATHS:
        path = C42_C53_PATHS[name]
        held = HeldPinnedInput(
            path, "C42/C53 historical full10:" + name,
            C42_C53_EXPECTED_MODES[name], C42_C53_PINS[name])
        files.append(held)
        by_path[path] = held
    need(len(files) == 10 and len({item.identity for item in files}) == 10,
         "C42 full10 identities pairwise distinct")
    manifest_guard = by_path[C42_MANIFEST_PATH]
    ordered = parse_manifest_ordered(manifest_guard.raw, "C42 held manifest")
    manifest = {entry["entry_name"]: entry["file_sha256"] for entry in ordered}
    need(len(ordered) == 8 and len(manifest) == 8 and
         set(manifest) == C42_CANDIDATE_MANIFEST_MEMBERS,
         "C42 exact ordered8 manifest")
    for name in C42_CANDIDATE_MANIFEST_MEMBERS:
        path = C42_CANDIDATE_DIR / name
        if path in by_path:
            need(sha(by_path[path].raw) == manifest[name],
                 "C42 overlapping full10/candidate9 pin:" + name)
            continue
        held = HeldPinnedInput(
            path, "C42 historical candidate9:" + name,
            C42_CANDIDATE_MEMBER_EXPECTED_MODE, manifest[name])
        files.append(held)
        by_path[path] = held
    need(len(files) == 16 and len(by_path) == 16,
         "C42 full10 union candidate9 exact16 unique paths")
    return HeldInputSet(files, directories)


def hold_surfaces(specifications: list[tuple[Path, tuple[str, ...], str]]) -> HeldInputSet:
    files: list[HeldPinnedInput] = []
    directories: list[HeldDirectory] = []
    for directory_path, names, label in specifications:
        directories.append(HeldDirectory(
            directory_path, set(names), 0o555, 2, label))
        for name in names:
            files.append(HeldPinnedInput(
                directory_path / name, label + ":" + name, 0o444))
    return HeldInputSet(files, directories)


def hold_v3_predecessor_exact10(
        ) -> tuple[HeldInputSet, list[HeldOpaqueMetadata]]:
    source_names = {"build_only_producer", "independent_consumer", "cold_launcher"}
    files = [
        HeldPinnedInput(path, "frozen v3 held:" + name, 0o444, file_sha256)
        for name, (path, file_sha256) in V3_FROZEN_FILES.items()
        if name not in source_names
    ]
    files.append(HeldPinnedInput(
        V3_OFFICIAL_REJECTION, "official v3 later rejection held with predecessor",
        0o444, V3_OFFICIAL_REJECTION_FILE_PIN))
    source_metadata = [
        HeldOpaqueMetadata(V3_FROZEN_FILES[name][0],
                           "frozen v3 source metadata-only held:" + name,
                           0o444)
        for name in sorted(source_names)
    ]
    need(len(files) == 8 and len(source_metadata) == 3 and
         len({item.path for item in files}) == 8 and
         len({item.path for item in source_metadata}) == 3,
         "frozen v3 exact10: exact7 readable plus exact3 metadata-only source "
         "members, with one additional official-rejection readable fd")
    return HeldInputSet(files, []), source_metadata


def terminal_replay_v3_predecessor_exact10(
        guard: HeldInputSet,
        source_metadata: list[HeldOpaqueMetadata]) -> None:
    guard.terminal_replay()
    for item in source_metadata:
        item.terminal_replay()


def hold_v4_rejected_static_draft7(
        ) -> tuple[HeldInputSet, list[HeldOpaqueMetadata]]:
    source_names = {
        "build_only_producer_v4", "independent_consumer_v4", "cold_launcher_v4"}
    files = [
        HeldPinnedInput(path, "rejected v4 readable held:" + name, 0o444,
                        file_sha256)
        for name, (path, file_sha256) in V4_REJECTED_FILES.items()
        if name not in source_names
    ]
    source_metadata = [
        HeldOpaqueMetadata(V4_REJECTED_FILES[name][0],
                           "rejected v4 source metadata-only held:" + name,
                           0o444)
        for name in sorted(source_names)
    ]
    need(len(files) == 4 and len(source_metadata) == 3 and
         len({item.path for item in files}) == 4 and
         len({item.path for item in source_metadata}) == 3,
         "rejected v4 exact4 readable plus exact3 source metadata-only members")
    return HeldInputSet(files, []), source_metadata


def terminal_replay_v4_rejected_static_draft7(
        guard: HeldInputSet,
        source_metadata: list[HeldOpaqueMetadata]) -> None:
    guard.terminal_replay()
    for item in source_metadata:
        item.terminal_replay()


def hold_v5_published_exact10(
        ) -> tuple[HeldInputSet, list[HeldOpaqueMetadata]]:
    """Hold frozen v5 without making any predecessor source content readable."""
    source_names = {
        "build_only_producer_v5", "independent_consumer_v5",
        "cold_launcher_v5"}
    files = [
        HeldPinnedInput(path, "published v5 readable held:" + name, 0o444,
                        file_sha256)
        for name, (path, file_sha256) in V5_FROZEN_FILES.items()
        if name not in source_names
    ]
    source_metadata = [
        HeldOpaqueMetadata(V5_FROZEN_FILES[name][0],
                           "published v5 source metadata-only held:" + name,
                           0o444)
        for name in sorted(source_names)
    ]
    need(len(files) == 7 and len(source_metadata) == 3 and
         len({item.path for item in files}) == 7 and
         len({item.path for item in source_metadata}) == 3 and
         {item.path for item in files}.isdisjoint(
             {item.path for item in source_metadata}),
         "published v5 exact10 partitions into exact7 readable and exact3 "
         "strict O_PATH metadata-only source members")
    return HeldInputSet(files, []), source_metadata


def terminal_replay_v5_published_exact10(
        guard: HeldInputSet,
        source_metadata: list[HeldOpaqueMetadata]) -> None:
    guard.terminal_replay()
    for item in source_metadata:
        item.terminal_replay()


def hold_v6_published_exact10(
        ) -> tuple[HeldInputSet, list[HeldOpaqueMetadata]]:
    """Hold published v6 while keeping every predecessor source metadata-only."""
    source_names = {
        "build_only_producer_v6", "independent_consumer_v6",
        "cold_launcher_v6"}
    files = [
        HeldPinnedInput(path, "published v6 readable held:" + name, 0o444,
                        file_sha256)
        for name, (path, file_sha256) in V6_FROZEN_FILES.items()
        if name not in source_names
    ]
    source_metadata = [
        HeldOpaqueMetadata(V6_FROZEN_FILES[name][0],
                           "published v6 source metadata-only held:" + name,
                           0o444)
        for name in sorted(source_names)
    ]
    readable_paths = {item.path for item in files}
    metadata_paths = {item.path for item in source_metadata}
    need(len(files) == 7 and len(source_metadata) == 3 and
         len(readable_paths) == 7 and len(metadata_paths) == 3 and
         readable_paths.isdisjoint(metadata_paths),
         "published v6 exact10 partitions into exact7 readable and exact3 "
         "strict O_PATH metadata-only source members")
    directories = [HeldDirectory(
        V5_OFFICIAL_REJECTION.parent, {V5_OFFICIAL_REJECTION.name},
        0o555, 2, "published v6 shared v5 rejection singleton namespace")]
    return HeldInputSet(files, directories), source_metadata


def terminal_replay_v6_published_exact10(
        guard: HeldInputSet,
        source_metadata: list[HeldOpaqueMetadata]) -> None:
    guard.terminal_replay()
    for item in source_metadata:
        item.terminal_replay()


def hold_v7_published_exact10(
        ) -> tuple[HeldInputSet, list[HeldOpaqueMetadata]]:
    """Hold frozen v7 exact10; never content-open any v7 executable source."""
    source_names = {
        "build_only_producer_v7", "independent_consumer_v7",
        "cold_launcher_v7"}
    files = [
        HeldPinnedInput(path, "published v7 readable held:" + name, 0o444,
                        file_sha256)
        for name, (path, file_sha256) in V7_FROZEN_FILES.items()
        if name not in source_names
    ]
    source_metadata = [
        HeldOpaqueMetadata(V7_FROZEN_FILES[name][0],
                           "published v7 source metadata-only held:" + name,
                           0o444)
        for name in sorted(source_names)
    ]
    readable_paths = {item.path for item in files}
    metadata_paths = {item.path for item in source_metadata}
    need(len(files) == 7 and len(source_metadata) == 3 and
         len(readable_paths) == 7 and len(metadata_paths) == 3 and
         readable_paths.isdisjoint(metadata_paths),
         "published v7 exact10 partitions into exact7 readable and exact3 "
         "strict O_PATH metadata-only source members")
    directories = [HeldDirectory(
        V6_OFFICIAL_REJECTION.parent, {V6_OFFICIAL_REJECTION.name},
        0o555, 2, "published v7 shared v6 rejection singleton namespace")]
    return HeldInputSet(files, directories), source_metadata


def terminal_replay_v7_published_exact10(
        guard: HeldInputSet,
        source_metadata: list[HeldOpaqueMetadata]) -> None:
    guard.terminal_replay()
    for item in source_metadata:
        item.terminal_replay()


def hold_v8_published_exact10(
        ) -> tuple[HeldInputSet, list[HeldOpaqueMetadata]]:
    """Hold frozen v8 exact10 without content-opening executable sources."""
    source_names = {
        "build_only_producer_v8", "independent_consumer_v8",
        "cold_launcher_v8"}
    files = [
        HeldPinnedInput(path, "published v8 readable held:" + name, 0o444,
                        file_sha256)
        for name, (path, file_sha256) in V8_FROZEN_FILES.items()
        if name not in source_names
    ]
    source_metadata = [
        HeldOpaqueMetadata(V8_FROZEN_FILES[name][0],
                           "published v8 source metadata-only held:" + name,
                           0o444)
        for name in sorted(source_names)
    ]
    readable_paths = {item.path for item in files}
    metadata_paths = {item.path for item in source_metadata}
    need(len(files) == 7 and len(source_metadata) == 3 and
         len(readable_paths) == 7 and len(metadata_paths) == 3 and
         readable_paths.isdisjoint(metadata_paths),
         "published v8 exact10 partitions into exact7 readable and exact3 "
         "strict O_PATH metadata-only source members")
    directories = [HeldDirectory(
        V7_OFFICIAL_REJECTION.parent, {V7_OFFICIAL_REJECTION.name},
        0o555, 2, "published v8 shared v7 rejection singleton namespace")]
    return HeldInputSet(files, directories), source_metadata


def terminal_replay_v8_published_exact10(
        guard: HeldInputSet,
        source_metadata: list[HeldOpaqueMetadata]) -> None:
    guard.terminal_replay()
    for item in source_metadata:
        item.terminal_replay()


def hold_v9_published_exact10(
        ) -> tuple[HeldInputSet, list[HeldOpaqueMetadata]]:
    """Hold frozen v9 exact10 without content-opening executable sources."""
    source_names = {
        "build_only_producer_v9", "independent_consumer_v9",
        "cold_launcher_v9"}
    files = [
        HeldPinnedInput(path, "published v9 readable held:" + name, 0o444,
                        file_sha256)
        for name, (path, file_sha256) in V9_FROZEN_FILES.items()
        if name not in source_names
    ]
    source_metadata = [
        HeldOpaqueMetadata(V9_FROZEN_FILES[name][0],
                           "published v9 source metadata-only held:" + name,
                           0o444)
        for name in sorted(source_names)
    ]
    readable_paths = {item.path for item in files}
    metadata_paths = {item.path for item in source_metadata}
    need(len(files) == 7 and len(source_metadata) == 3 and
         len(readable_paths) == 7 and len(metadata_paths) == 3 and
         readable_paths.isdisjoint(metadata_paths),
         "published v9 exact10 partitions into exact7 readable and exact3 "
         "strict O_PATH metadata-only source members")
    directories = [HeldDirectory(
        V8_OFFICIAL_REJECTION.parent, {V8_OFFICIAL_REJECTION.name},
        0o555, 2, "published v9 shared v8 rejection singleton namespace")]
    return HeldInputSet(files, directories), source_metadata


def terminal_replay_v9_published_exact10(
        guard: HeldInputSet,
        source_metadata: list[HeldOpaqueMetadata]) -> None:
    guard.terminal_replay()
    for item in source_metadata:
        item.terminal_replay()


def hold_v10_published_exact10(
        ) -> tuple[HeldInputSet, list[HeldOpaqueMetadata]]:
    """Hold frozen v10 exact10 without content-opening executable sources."""
    source_names = {
        "build_only_producer_v10", "independent_consumer_v10",
        "cold_launcher_v10"}
    files = [
        HeldPinnedInput(path, "published v10 readable held:" + name, 0o444,
                        file_sha256)
        for name, (path, file_sha256) in V10_FROZEN_FILES.items()
        if name not in source_names
    ]
    source_metadata = [
        HeldOpaqueMetadata(V10_FROZEN_FILES[name][0],
                           "published v10 source metadata-only held:" + name,
                           0o444)
        for name in sorted(source_names)
    ]
    readable_paths = {item.path for item in files}
    metadata_paths = {item.path for item in source_metadata}
    need(len(files) == 7 and len(source_metadata) == 3 and
         len(readable_paths) == 7 and len(metadata_paths) == 3 and
         readable_paths.isdisjoint(metadata_paths),
         "published v10 exact10 partitions into exact7 readable and exact3 "
         "strict O_PATH metadata-only source members")
    directories = [HeldDirectory(
        V9_OFFICIAL_REJECTION.parent, {V9_OFFICIAL_REJECTION.name},
        0o555, 2, "published v10 shared v9 rejection singleton namespace")]
    return HeldInputSet(files, directories), source_metadata


def terminal_replay_v10_published_exact10(
        guard: HeldInputSet,
        source_metadata: list[HeldOpaqueMetadata]) -> None:
    guard.terminal_replay()
    for item in source_metadata:
        item.terminal_replay()


def hold_v11_published_exact10(
        ) -> tuple[HeldInputSet, list[HeldOpaqueMetadata]]:
    """Hold frozen v11 exact10 without content-opening executable sources."""
    source_names = {
        "build_only_producer_v11", "independent_consumer_v11",
        "cold_launcher_v11"}
    files = [
        HeldPinnedInput(path, "published v11 readable held:" + name, 0o444,
                        file_sha256)
        for name, (path, file_sha256) in V11_FROZEN_FILES.items()
        if name not in source_names
    ]
    source_metadata = [
        HeldOpaqueMetadata(V11_FROZEN_FILES[name][0],
                           "published v11 source metadata-only held:" + name,
                           0o444)
        for name in sorted(source_names)
    ]
    readable_paths = {item.path for item in files}
    metadata_paths = {item.path for item in source_metadata}
    need(len(files) == 7 and len(source_metadata) == 3 and
         len(readable_paths) == 7 and len(metadata_paths) == 3 and
         readable_paths.isdisjoint(metadata_paths),
         "published v11 exact10 partitions into exact7 readable and exact3 "
         "strict O_PATH metadata-only source members")
    directories = [HeldDirectory(
        V10_OFFICIAL_REJECTION.parent, {V10_OFFICIAL_REJECTION.name},
        0o555, 2, "published v11 shared v10 rejection singleton namespace")]
    return HeldInputSet(files, directories), source_metadata


def terminal_replay_v11_published_exact10(
        guard: HeldInputSet,
        source_metadata: list[HeldOpaqueMetadata]) -> None:
    guard.terminal_replay()
    for item in source_metadata:
        item.terminal_replay()


def terminal_replay_v12_published_exact10() -> None:
    need(isinstance(_INCIDENT_AUTHORITY_HOLD,
                    HeldInheritedV14AuthorityExact12),
         "published v12 exact10 remains continuously inherited and held")
    _INCIDENT_AUTHORITY_HOLD.terminal_replay()


def held_v12_official_rejection() -> HeldPinnedInput:
    need(isinstance(_INCIDENT_AUTHORITY_HOLD,
                    HeldInheritedV14AuthorityExact12),
         "official v12 rejection comes from inherited exact17 authority")
    receipt_guard = _INCIDENT_AUTHORITY_HOLD.by_env[V12_REJECTION_FD_ENV]
    namespace_guard = _INCIDENT_AUTHORITY_HOLD.v12_rejection_namespace
    need(receipt_guard.path == V12_OFFICIAL_REJECTION and
         namespace_guard is not None and
         namespace_guard.path == V12_OFFICIAL_REJECTION.parent and
         namespace_guard.names == {V12_OFFICIAL_REJECTION.name},
         "official v12 rejection and singleton namespace held by exact17 authority")
    return receipt_guard


def held_v13_supersession_receipt() -> HeldPinnedInput:
    need(isinstance(_INCIDENT_AUTHORITY_HOLD,
                    HeldInheritedV14AuthorityExact12),
         "v13 supersession receipt comes from inherited exact17 authority")
    receipt_guard = _INCIDENT_AUTHORITY_HOLD.by_env[
        V13_SUPERSESSION_RECEIPT_FD_ENV]
    need(receipt_guard.path == V13_SUPERSESSION_RECEIPT and
         isinstance(_INCIDENT_AUTHORITY_HOLD.v13_supersession_receipt, dict),
         "v13 supersession receipt held with parsed exact17 contract")
    return receipt_guard


def expected_rejected_prepublication_v13_supersession_receipt(
        ) -> dict[str, Any]:
    guard = held_v13_supersession_receipt()
    receipt = strict_json(guard.raw, "v13 supersession receipt binding")
    need(isinstance(receipt, dict) and
         receipt == _INCIDENT_AUTHORITY_HOLD.v13_supersession_receipt,
         "v13 supersession binding reuses inherited exact17 parsed object")
    return {
        "receipt_path": str(V13_SUPERSESSION_RECEIPT.relative_to(ROOT)),
        "receipt_file_sha256": V13_SUPERSESSION_RECEIPT_FILE_PIN,
        "receipt_object_sha256": V13_SUPERSESSION_RECEIPT_OBJECT_PIN,
        "receipt_schema": receipt["schema"],
        "receipt_status": receipt["status"],
        "transition_kind":
            "APPEND_ONLY_V13_PREPUBLICATION_PYC_CONTAMINATION_REJECTION_"
            "TO_ZERO_CREDIT_V14_STATIC_SUCCESSOR",
        "v14_successor_contract": copy.deepcopy(
            receipt["v14_successor_contract"]),
    }


def expected_published_then_rejected_v14_summary() -> dict[str, Any]:
    need(isinstance(_INCIDENT_AUTHORITY_HOLD,
                    HeldInheritedV14AuthorityExact12),
         "v14 exact12 authority remains held for transition summary")
    guard = _INCIDENT_AUTHORITY_HOLD.authority_exact12_by_role[
        "v14_registry_shape_drift_supersession_receipt"]
    receipt = strict_json(guard.raw, "v14 supersession receipt binding")
    need(isinstance(receipt, dict) and
         guard.path == V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT and
         sha(guard.raw) ==
             V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT_FILE_PIN and
         receipt.get("object_sha256") ==
             V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT_OBJECT_PIN and
         receipt.get("schema") ==
             V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_SCHEMA and
         receipt.get("status") ==
             "FROZEN_APPEND_ONLY_V14_RUNTIME_REGISTRY_SHAPE_DRIFT_REJECTION__ZERO_CREDIT__V" + "15_SUCCESSOR_ONLY" and
         receipt.get("transition_kind") == "APPEND_ONLY_PUBLISHED_V14_RUNTIME_FAIL_CLOSED_REJECTION_TO_ZERO_CREDIT_V" + "15_CLEAN_ROOM_SUCCESSOR" and
         isinstance(receipt.get("v" + "15_successor_contract"), dict),
         "v14 supersession receipt exact summary inputs")
    return {
        "receipt_path": str(
            V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT.relative_to(
                ROOT)),
        "receipt_file_sha256":
            V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT_FILE_PIN,
        "receipt_object_sha256":
            V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT_OBJECT_PIN,
        "receipt_schema":
            V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_SCHEMA,
        "receipt_status":
            "FROZEN_APPEND_ONLY_V14_RUNTIME_REGISTRY_SHAPE_DRIFT_REJECTION__ZERO_CREDIT__V" + "15_SUCCESSOR_ONLY",
        "transition_kind": "APPEND_ONLY_PUBLISHED_V14_RUNTIME_FAIL_CLOSED_REJECTION_TO_ZERO_CREDIT_V" + "15_CLEAN_ROOM_SUCCESSOR",
        "inherited_authority_exact12_member_count": 12,
        "inherited_authority_exact12_canonical_sha256":
            V14_INHERITED_AUTHORITY_EXACT12_CANONICAL_SHA256,
        "v" + "15_successor_contract": copy.deepcopy(
            receipt["v" + "15_successor_contract"]),
    }


def held_v3_official_rejection(guard: HeldInputSet) -> HeldPinnedInput:
    matches = [item for item in guard.files
               if item.path == V3_OFFICIAL_REJECTION]
    need(len(matches) == 1,
         "official v3 rejection is one independently held predecessor file")
    return matches[0]


def held_v4_supersession_from_v5(guard: HeldInputSet) -> HeldPinnedInput:
    matches = [item for item in guard.files
               if item.path == V4_REJECTION_SUPERSESSION]
    need(len(matches) == 1,
         "v4 supersession is one shared readable member of published v5 exact10")
    return matches[0]


def held_v5_official_rejection(policy_guard: HeldInputSet) -> HeldPinnedInput:
    matches = [item for item in policy_guard.files
               if item.path == V5_OFFICIAL_REJECTION]
    need(len(matches) == 1,
         "official v5 rejection is one shared current-policy held file")
    namespace_matches = [item for item in policy_guard.directories
                         if item.path == V5_OFFICIAL_REJECTION.parent]
    need(len(namespace_matches) == 1 and
         namespace_matches[0].names == {V5_OFFICIAL_REJECTION.name},
         "official v5 rejection namespace is one exact singleton held dirfd")
    return matches[0]


def held_v6_official_rejection(policy_guard: HeldInputSet) -> HeldPinnedInput:
    matches = [item for item in policy_guard.files
               if item.path == V6_OFFICIAL_REJECTION]
    need(len(matches) == 1,
         "official v6 rejection is one shared current-policy held file")
    namespace_matches = [item for item in policy_guard.directories
                         if item.path == V6_OFFICIAL_REJECTION.parent]
    need(len(namespace_matches) == 1 and
         namespace_matches[0].names == {V6_OFFICIAL_REJECTION.name},
         "official v6 rejection namespace is one exact singleton held dirfd")
    return matches[0]


def held_v7_official_rejection(policy_guard: HeldInputSet) -> HeldPinnedInput:
    matches = [item for item in policy_guard.files
               if item.path == V7_OFFICIAL_REJECTION]
    need(len(matches) == 1,
         "official v7 rejection is one shared current-policy held file")
    namespace_matches = [item for item in policy_guard.directories
                         if item.path == V7_OFFICIAL_REJECTION.parent]
    need(len(namespace_matches) == 1 and
         namespace_matches[0].names == {V7_OFFICIAL_REJECTION.name},
         "official v7 rejection namespace is one exact singleton held dirfd")
    return matches[0]


def held_v8_official_rejection(policy_guard: HeldInputSet) -> HeldPinnedInput:
    matches = [item for item in policy_guard.files
               if item.path == V8_OFFICIAL_REJECTION]
    need(len(matches) == 1,
         "official v8 rejection is one shared current-policy held file")
    namespace_matches = [item for item in policy_guard.directories
                         if item.path == V8_OFFICIAL_REJECTION.parent]
    need(len(namespace_matches) == 1 and
         namespace_matches[0].names == {V8_OFFICIAL_REJECTION.name},
         "official v8 rejection namespace is one exact singleton held dirfd")
    return matches[0]


def held_v9_official_rejection(policy_guard: HeldInputSet) -> HeldPinnedInput:
    matches = [item for item in policy_guard.files
               if item.path == V9_OFFICIAL_REJECTION]
    need(len(matches) == 1,
         "official v9 rejection is one shared current-policy held file")
    namespace_matches = [item for item in policy_guard.directories
                         if item.path == V9_OFFICIAL_REJECTION.parent]
    need(len(namespace_matches) == 1 and
         namespace_matches[0].names == {V9_OFFICIAL_REJECTION.name},
         "official v9 rejection namespace is one exact singleton held dirfd")
    return matches[0]


def held_v10_official_rejection(policy_guard: HeldInputSet) -> HeldPinnedInput:
    matches = [item for item in policy_guard.files
               if item.path == V10_OFFICIAL_REJECTION]
    need(len(matches) == 1,
         "official v10 rejection is one shared current-policy held file")
    namespace_matches = [item for item in policy_guard.directories
                         if item.path == V10_OFFICIAL_REJECTION.parent]
    need(len(namespace_matches) == 1 and
         namespace_matches[0].names == {V10_OFFICIAL_REJECTION.name},
         "official v10 rejection namespace is one exact singleton held dirfd")
    return matches[0]


def held_v11_official_rejection() -> HeldInheritedFileView:
    need(isinstance(_INCIDENT_AUTHORITY_HOLD,
                    HeldInheritedV14AuthorityExact12),
         "official v11 rejection comes from held v12 predecessor")
    receipt_guard = _INCIDENT_AUTHORITY_HOLD.by_env[V11_REJECTION_FD_ENV]
    namespace_guard = _INCIDENT_AUTHORITY_HOLD.v11_rejection_namespace
    need(receipt_guard.path == V11_OFFICIAL_REJECTION and
         namespace_guard is not None and
         namespace_guard.path == V11_OFFICIAL_REJECTION.parent and
         namespace_guard.names == {V11_OFFICIAL_REJECTION.name},
         "official v11 rejection and singleton namespace held by v12 history")
    return receipt_guard


def _expected_v4_provisional_exact8() -> list[dict[str, Any]]:
    ordered: list[dict[str, Any]] = [{
        "name": "official_v3_later_rejection",
        "path": str(V3_OFFICIAL_REJECTION.relative_to(ROOT)),
        "file_sha256": V3_OFFICIAL_REJECTION_FILE_PIN,
        "object_sha256": V3_OFFICIAL_REJECTION_OBJECT_PIN,
        "mode": "0444", "nlink": 1,
    }]
    for name, (path, file_pin) in V4_REJECTED_FILES.items():
        member: dict[str, Any] = {
            "name": name, "path": str(path.relative_to(ROOT)),
            "file_sha256": file_pin, "mode": "0444", "nlink": 1,
        }
        if name in V4_REJECTED_OBJECTS:
            member["object_sha256"] = V4_REJECTED_OBJECTS[name]
        ordered.append(member)
    return ordered


def validate_v4_rejected_static_draft7(
        receipt: Mapping[str, Any], guard: HeldInputSet,
        source_metadata: list[HeldOpaqueMetadata],
        shared_v3_rejection_guard: HeldPinnedInput) -> None:
    source_names = {
        "build_only_producer_v4", "independent_consumer_v4", "cold_launcher_v4"}
    readable_by_path = {item.path: item for item in guard.files}
    source_by_path = {item.path: item for item in source_metadata}
    need(set(readable_by_path) == {
             path for name, (path, _) in V4_REJECTED_FILES.items()
             if name not in source_names} and
         set(source_by_path) == {
             path for name, (path, _) in V4_REJECTED_FILES.items()
             if name in source_names} and
         shared_v3_rejection_guard.path == V3_OFFICIAL_REJECTION and
         sha(shared_v3_rejection_guard.raw) == V3_OFFICIAL_REJECTION_FILE_PIN,
         "rejected v4 exact7 partition reuses independently held v3 rejection fd")
    for name, (path, file_pin) in V4_REJECTED_FILES.items():
        if name in source_names:
            metadata = source_by_path[path]
            need(stat.S_ISREG(metadata.before.st_mode) and
                 stat.S_IMODE(metadata.before.st_mode) == 0o444 and
                 metadata.before.st_nlink == 1,
                 "rejected v4 metadata-only source mode/nlink:" + name)
            continue
        raw = readable_by_path[path].raw
        need(sha(raw) == file_pin, "rejected v4 readable file pin:" + name)
        if name in V4_REJECTED_OBJECTS:
            value = strict_json(raw, "rejected v4 object:" + name)
            verify_object(value, "rejected v4 object:" + name,
                          V4_REJECTED_OBJECTS[name])
    ordered_expected = _expected_v4_provisional_exact8()
    frozen = receipt.get("frozen_v4_provisional_exact8")
    need(isinstance(frozen, dict) and
         frozen.get("ordered_members") == ordered_expected,
         "rejected v4 exact8 receipt order equals shared v3 rejection plus held draft7")
    identities = (
        {item.identity for item in guard.files} |
        {item.identity for item in source_metadata} |
        {shared_v3_rejection_guard.identity})
    mount_ids = (
        {item.mount_id for item in guard.files} |
        {item.mount_id for item in source_metadata} |
        {shared_v3_rejection_guard.mount_id})
    need(len(identities) == 8 and len(mount_ids) == 1,
         "rejected v4 exact8 held identities unique on one statx mount")


def exact_v4_rejection_supersession(
        receipt_guard: HeldPinnedInput) -> dict[str, Any]:
    need(receipt_guard.path == V4_REJECTION_SUPERSESSION and
         sha(receipt_guard.raw) == V4_REJECTION_SUPERSESSION_FILE_PIN,
         "exact held v4 rejection/supersession receipt file pin")
    value = strict_json(
        receipt_guard.raw, "v4 rejection/supersession receipt")
    verify_object(value, "v4 rejection/supersession receipt",
                  V4_REJECTION_SUPERSESSION_OBJECT_PIN)
    need(receipt_guard.raw == canonical(value) + b"\n" and set(value) == {
             "schema", "status", "transition_kind", "receipt_path",
             "effective_checkpoint_object_sha256",
             "frozen_v4_provisional_exact8", "root_defects",
             "no_run_attestation", "rejection", "supersession",
             "formal_global_closure_credit", "D02_unlock", "D02_gate_credit",
             "D02_task_credit", "D02_formal_pending_task_count", "D02_started",
             "object_sha256"} and
         value.get("schema") ==
             "cm2.round306c79g.true-global-no-producer-consumer."
             "v4-rejection-supersession-receipt.v1" and
         value.get("status") ==
             "FROZEN_APPEND_ONLY_V4_STATIC_NO_RUN_REJECTION__THREE_ROOT_DEFECTS__V5_SUCCESSOR_ONLY" and
         value.get("transition_kind") ==
             "REJECTION_AND_SUPERSESSION_WITHOUT_MUTATING_FROZEN_V4_BYTES" and
         value.get("receipt_path") ==
             str(V4_REJECTION_SUPERSESSION.relative_to(ROOT)) and
         value.get("effective_checkpoint_object_sha256") == UPSTREAM_CHECKPOINT_OBJECT_PIN and
         value.get("formal_global_closure_credit") == 0 and
         value.get("D02_unlock") is False and
         value.get("D02_gate_credit") == 0 and
         value.get("D02_task_credit") == 0 and
         value.get("D02_formal_pending_task_count") == PENDING_D02 and
         value.get("D02_started") is False,
         "v4 rejection/supersession exact canonical zero-credit envelope")
    frozen = value.get("frozen_v4_provisional_exact8")
    no_run = value.get("no_run_attestation")
    rejection = value.get("rejection")
    supersession = value.get("supersession")
    defects = value.get("root_defects")
    ordered = frozen.get("ordered_members") if isinstance(frozen, dict) else None
    need(isinstance(frozen, dict) and isinstance(no_run, dict) and
         isinstance(rejection, dict) and isinstance(supersession, dict) and
         isinstance(defects, list) and isinstance(ordered, list) and
         len(ordered) == 8 and
         [member.get("name") for member in ordered] == [
             "official_v3_later_rejection", "closed_schema_v4", "contract_v4",
             "build_only_producer_v4", "independent_consumer_v4",
             "transition_v3_to_v4", "static_audit_v4", "cold_launcher_v4"] and
         all(member.get("mode") == "0444" and member.get("nlink") == 1 and
             _nonzero_sha256(member.get("file_sha256"))
             for member in ordered) and
         ordered[0].get("path") ==
             str(V3_OFFICIAL_REJECTION.relative_to(ROOT)) and
         ordered[0].get("file_sha256") == V3_OFFICIAL_REJECTION_FILE_PIN and
         ordered[0].get("object_sha256") == V3_OFFICIAL_REJECTION_OBJECT_PIN and
         frozen.get("all_eight_file_pins_match") is True and
         frozen.get("all_declared_object_pins_match") is True and
         frozen.get("all_eight_regular_0444_nlink1") is True and
         frozen.get("v4_working_modes_frozen_to_0444_before_receipt") is True and
         frozen.get("v4_bytes_modified_by_this_receipt") is False and
         frozen.get("cold_manifest_v4_exists") is False and
         frozen.get("cold_outer_v4_exists") is False and
         no_run.get("v4_runtime_commands_invoked") == [] and
         no_run.get("v4_candidate_verification_completion_authority_surfaces_created") == 0 and
         no_run.get("v4_cold_manifest_created") is False and
         no_run.get("v4_cold_outer_created") is False and
         no_run.get("v4_positive_wrapper_emitted") is False and
         no_run.get("D02_started") is False and
         rejection.get("v4_execution_allowed") is False and
         rejection.get("v4_build_allowed") is False and
         rejection.get("v4_verify_allowed") is False and
         rejection.get("v4_assemble_allowed") is False and
         rejection.get("v4_authorize_allowed") is False and
         rejection.get("v4_reject_command_allowed") is False and
         rejection.get("v4_runtime_surfaces_authoritative") is False and
         {defect.get("id") for defect in defects if isinstance(defect, dict)} == {
             "V4_CONSUMER_NEED_THREE_POSITIONAL_ARGUMENTS",
             "V4_CONSUMER_HELDOPAQUEMETADATA_MISSING_EXPECTED_MODE",
             "V4_LAUNCHER_PATHNAME_EXECUTION_PRECEDES_HELD_FD_HASH"} and
         supersession.get("successor_version") == 5 and
         supersession.get("successor_must_pin_this_receipt_file_and_object_hashes") is True and
         supersession.get("this_receipt_does_not_pin_successor_bytes") is True and
         supersession.get("reason_for_one_way_binding") == "AVOID_HASH_CYCLE",
         "v4 exact rejected draft/no-run/defect/successor semantics")
    return value


def _expected_published_v5_exact10() -> list[dict[str, Any]]:
    expected: list[dict[str, Any]] = []
    public_names = {
        "v4_rejection_supersession": "v4_rejection_supersession",
        "closed_schema_v5": "closed_schema",
        "contract_v5": "contract",
        "build_only_producer_v5": "build_only_producer",
        "independent_consumer_v5": "independent_consumer",
        "transition_v4_to_v5": "v4_to_v5_transition",
        "static_audit_v5": "static_audit",
        "cold_launcher_v5": "cold_launcher",
        "cold_manifest_v5": "cold_manifest",
        "cold_outer_v5": "cold_outer",
    }
    for name in V5_EXACT10_ORDER:
        path, file_sha256 = V5_FROZEN_FILES[name]
        entry: dict[str, Any] = {
            "name": public_names[name],
            "path": str(path.relative_to(ROOT)),
            "file_sha256": file_sha256,
        }
        if name in V5_FROZEN_OBJECTS:
            entry["object_sha256"] = V5_FROZEN_OBJECTS[name]
        expected.append(entry)
    return expected


def _v5_strict_bool_defect_census() -> dict[str, Any]:
    return {
        "direct_need_call_count": 700,
        "risk_count": 7,
        "hard_defect_count": 3,
        "ordered_risk_ids": list(V5_STRICT_BOOL_RISK_IDS),
        "all_seven_present_in_v5": True,
        "same_seven_absent_from_v6": True,
        "v6_recursive_exact_bool_unproved_count": 0,
    }


def _v5_first_build_entry_attempt() -> dict[str, Any]:
    return {
        "attempted": True,
        "producer_child_spawned": False,
        "candidate_write_started": False,
        "positive_runtime_surface_count": 0,
    }


def validate_v5_common_official_rejection_fields() -> dict[str, Any]:
    return {
        "path": str(V5_OFFICIAL_REJECTION.relative_to(ROOT)),
        "namespace_path": str(V5_OFFICIAL_REJECTION.parent.relative_to(ROOT)),
        "file_sha256": V5_OFFICIAL_REJECTION_FILE_PIN,
        "object_sha256": V5_OFFICIAL_REJECTION_OBJECT_PIN,
        "schema":
            "cm2.round306c79g.true-global-no-producer-consumer.v5.later-rejection",
        "status": "PERMANENT_FAIL_CLOSED_REJECTION__ZERO_CREDIT",
        "reason": "ORPHANED_OR_INCOMPLETE_C79G_V5_SURFACE",
        "namespace_mode": "0555",
        "namespace_nlink": 2,
        "member_mode": "0444",
        "member_nlink": 1,
        "exact_member_universe": ["rejection.json"],
        "formal_global_closure_credit": 0,
        "D02_unlock": False,
        "D02_gate_credit": 0,
        "D02_task_credit": 0,
        "D02_formal_pending_task_count": PENDING_D02,
        "D02_started": False,
        "overwrite_delete_or_reuse_allowed": False,
    }


def _expected_published_then_rejected_v5_proof() -> dict[str, Any]:
    return {
        "ordered_published_exact10": _expected_published_v5_exact10(),
        "all_ten_file_pins_match": True,
        "all_declared_object_pins_match": True,
        "all_ten_regular_0444_nlink1": True,
        "exact8_manifest_reconstructs_first_eight_in_order": True,
        "outer_last_pins_manifest_and_launcher": True,
        "outer_then_rejection_chronology_validated": True,
        "official_later_rejection":
            validate_v5_common_official_rejection_fields(),
        "first_build_entry_attempt": _v5_first_build_entry_attempt(),
        "v5_execution_allowed": False,
        "v5_runtime_surfaces_authoritative": False,
        "strict_bool_defect_census": _v5_strict_bool_defect_census(),
        "formal_global_closure_credit": 0,
        "D02_unlock": False,
        "D02_gate_credit": 0,
        "D02_task_credit": 0,
        "D02_formal_pending_task_count": PENDING_D02,
        "D02_started": False,
    }


def exact_v5_official_rejection(
        policy_guard: HeldInputSet) -> tuple[dict[str, Any], HeldPinnedInput]:
    receipt_guard = held_v5_official_rejection(policy_guard)
    need(receipt_guard.path == V5_OFFICIAL_REJECTION and
         sha(receipt_guard.raw) == V5_OFFICIAL_REJECTION_FILE_PIN,
         "exact held v5 official rejection file pin")
    value = strict_json(receipt_guard.raw, "official v5 rejection")
    verify_object(value, "official v5 rejection",
                  V5_OFFICIAL_REJECTION_OBJECT_PIN)
    need(len(V5_OFFICIAL_REJECTION_EXACT39_KEYS) == 39 and
         sha(canonical(sorted(V5_OFFICIAL_REJECTION_EXACT39_KEYS))) ==
             V5_OFFICIAL_REJECTION_EXACT39_KEYSET_SHA256 and
         set(value) == V5_OFFICIAL_REJECTION_EXACT39_KEYS and
         sha(canonical(sorted(value))) ==
             V5_OFFICIAL_REJECTION_EXACT39_KEYSET_SHA256 and
         receipt_guard.raw == canonical(value) + b"\n" and
         value.get("schema") ==
             "cm2.round306c79g.true-global-no-producer-consumer.v5.later-rejection" and
         value.get("status") ==
             "PERMANENT_FAIL_CLOSED_REJECTION__ZERO_CREDIT" and
         value.get("rejection_reason") ==
             "ORPHANED_OR_INCOMPLETE_C79G_V5_SURFACE" and
         value.get("effective_checkpoint_object_sha256") == UPSTREAM_CHECKPOINT_OBJECT_PIN and
         value.get("namespace_exact_path") ==
             str(V5_OFFICIAL_REJECTION.parent.relative_to(ROOT)) and
         value.get("target_exact_path") ==
             str(V5_OFFICIAL_REJECTION.relative_to(ROOT)) and
         value.get("namespace_at_rest_mode") == "0555" and
         value.get("rejection_file_mode") == "0444" and
         value.get("rejection_file_nlink") == 1 and
         value.get("v4_rejection_supersession_file_sha256") ==
             V4_REJECTION_SUPERSESSION_FILE_PIN and
         value.get("v4_rejection_supersession_object_sha256") ==
             V4_REJECTION_SUPERSESSION_OBJECT_PIN and
         value.get("formal_global_closure_credit") == 0 and
         value.get("D02_unlock") is False and
         value.get("D02_gate_credit") == 0 and
         value.get("D02_task_credit") == 0 and
         value.get("D02_formal_pending_task_count") == PENDING_D02 and
         value.get("D02_started") is False and
         value.get("standalone_authority") is False and
         value.get("overwrite_delete_or_reuse_allowed") is False,
         "v5 official rejection canonical singleton zero-credit envelope")
    return value, receipt_guard


def validate_v5_published_then_rejected_predecessor(
        policy_guard: HeldInputSet, v5_guard: HeldInputSet,
        v5_source_metadata: list[HeldOpaqueMetadata]) -> dict[str, Any]:
    rejection, rejection_guard = exact_v5_official_rejection(policy_guard)
    source_names = {
        "build_only_producer_v5", "independent_consumer_v5",
        "cold_launcher_v5"}
    readable_by_path = {item.path: item for item in v5_guard.files}
    source_by_path = {item.path: item for item in v5_source_metadata}
    need(set(readable_by_path) == {
             path for name, (path, _) in V5_FROZEN_FILES.items()
             if name not in source_names} and
         set(source_by_path) == {
             path for name, (path, _) in V5_FROZEN_FILES.items()
             if name in source_names},
         "published v5 exact10 exact7-readable/exact3-metadata partition")
    for name, (path, file_pin) in V5_FROZEN_FILES.items():
        if name in source_names:
            metadata = source_by_path[path]
            need(stat.S_ISREG(metadata.before.st_mode) and
                 stat.S_IMODE(metadata.before.st_mode) == 0o444 and
                 metadata.before.st_nlink == 1,
                 "published v5 strict O_PATH metadata source:" + name)
            continue
        held = readable_by_path[path]
        need(sha(held.raw) == file_pin,
             "published v5 readable member pin:" + name)
        if name in V5_FROZEN_OBJECTS:
            parsed = strict_json(held.raw, "published v5 object:" + name)
            verify_object(parsed, "published v5 object:" + name,
                          V5_FROZEN_OBJECTS[name])
    exact8_expected = [
        {"file_sha256": V5_FROZEN_FILES[name][1],
         "entry_name": str(V5_FROZEN_FILES[name][0].relative_to(ROOT))}
        for name in V5_EXACT10_ORDER[:8]
    ]
    manifest_guard = readable_by_path[V5_FROZEN_FILES["cold_manifest_v5"][0]]
    outer_guard = readable_by_path[V5_FROZEN_FILES["cold_outer_v5"][0]]
    manifest = parse_manifest_ordered(manifest_guard.raw,
                                      "published v5 exact8 manifest")
    outer = strict_json(outer_guard.raw, "published v5 outer-last")
    verify_object(outer, "published v5 outer-last",
                  V5_FROZEN_OBJECTS["cold_outer_v5"])
    exact8_stats = []
    for name in V5_EXACT10_ORDER[:8]:
        path = V5_FROZEN_FILES[name][0]
        held_member = (source_by_path[path] if name in source_names
                       else readable_by_path[path])
        exact8_stats.append(held_member.before)
    chronology = cold_publication_chronology(
        exact8_stats, manifest_guard.before, outer_guard.before)
    need(manifest == exact8_expected and
         outer.get("exact8_ordered_entries") == [
             {"path": item["entry_name"],
              "file_sha256": item["file_sha256"]}
             for item in exact8_expected] and
         outer.get("status") ==
             "FROZEN_COLD_LAUNCH_OUTER_LAST__EXACT8_MANIFEST_CLOSED__RUNTIME_DEFERRED" and
         outer.get("formal_global_closure_credit") == 0 and
         outer.get("D02_unlock") is False and
         outer.get("runtime_executed_during_static_freeze") is False and
         all(chronology.values()) and
         max(outer_guard.before.st_mtime_ns, outer_guard.before.st_ctime_ns) <
             min(rejection_guard.before.st_mtime_ns,
                 rejection_guard.before.st_ctime_ns),
         "published v5 exact10 manifest/outer/official-rejection chronology")
    identities = ({item.identity for item in v5_guard.files} |
                  {item.identity for item in v5_source_metadata} |
                  {rejection_guard.identity})
    mount_ids = ({item.mount_id for item in v5_guard.files} |
                 {item.mount_id for item in v5_source_metadata} |
                 {rejection_guard.mount_id})
    need(len(identities) == 11 and len(mount_ids) == 1,
         "published v5 exact10 plus official rejection unique on one statx mount")
    return _expected_published_then_rejected_v5_proof()


def _expected_published_v6_exact10() -> list[dict[str, Any]]:
    expected: list[dict[str, Any]] = []
    public_names = {
        "v5_official_rejection": "v5_official_rejection",
        "closed_schema_v6": "closed_schema",
        "contract_v6": "contract",
        "build_only_producer_v6": "build_only_producer",
        "independent_consumer_v6": "independent_consumer",
        "transition_v5_to_v6": "v5_to_v6_transition",
        "static_audit_v6": "static_audit",
        "cold_launcher_v6": "cold_launcher",
        "cold_manifest_v6": "cold_manifest",
        "cold_outer_v6": "cold_outer",
    }
    for name in V6_EXACT10_ORDER:
        path, file_sha256 = V6_FROZEN_FILES[name]
        entry: dict[str, Any] = {
            "name": public_names[name],
            "path": str(path.relative_to(ROOT)),
            "file_sha256": file_sha256,
        }
        if name in V6_FROZEN_OBJECTS:
            entry["object_sha256"] = V6_FROZEN_OBJECTS[name]
        expected.append(entry)
    return expected


def _v6_first_build_entry_attempt() -> dict[str, Any]:
    return {
        "attempted": True,
        "producer_child_spawned": True,
        "candidate_write_started": False,
        "positive_runtime_surface_count": 0,
    }


def _v6_held_self_identity_defect() -> dict[str, Any]:
    return {
        "source_path": str(
            V6_FROZEN_FILES["build_only_producer_v6"][0].relative_to(ROOT)),
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


def validate_v6_common_official_rejection_fields() -> dict[str, Any]:
    return {
        "path": str(V6_OFFICIAL_REJECTION.relative_to(ROOT)),
        "namespace_path": str(V6_OFFICIAL_REJECTION.parent.relative_to(ROOT)),
        "file_sha256": V6_OFFICIAL_REJECTION_FILE_PIN,
        "object_sha256": V6_OFFICIAL_REJECTION_OBJECT_PIN,
        "schema":
            "cm2.round306c79g.true-global-no-producer-consumer.v6.later-rejection",
        "status": "PERMANENT_FAIL_CLOSED_REJECTION__ZERO_CREDIT",
        "reason": "ORPHANED_OR_INCOMPLETE_C79G_V6_SURFACE",
        "namespace_mode": "0555",
        "namespace_nlink": 2,
        "member_mode": "0444",
        "member_nlink": 1,
        "exact_member_universe": ["rejection.json"],
        "formal_global_closure_credit": 0,
        "D02_unlock": False,
        "D02_gate_credit": 0,
        "D02_task_credit": 0,
        "D02_formal_pending_task_count": PENDING_D02,
        "D02_started": False,
        "overwrite_delete_or_reuse_allowed": False,
    }


def _expected_published_then_rejected_v6_proof() -> dict[str, Any]:
    return {
        "ordered_published_exact10": _expected_published_v6_exact10(),
        "all_ten_file_pins_match": True,
        "all_declared_object_pins_match": True,
        "all_ten_regular_0444_nlink1": True,
        "exact8_manifest_reconstructs_first_eight_in_order": True,
        "outer_last_pins_manifest_and_launcher": True,
        "outer_then_rejection_chronology_validated": True,
        "official_later_rejection":
            validate_v6_common_official_rejection_fields(),
        "first_build_entry_attempt": _v6_first_build_entry_attempt(),
        "held_self_identity_defect": _v6_held_self_identity_defect(),
        "v6_execution_allowed": False,
        "v6_runtime_surfaces_authoritative": False,
        "formal_global_closure_credit": 0,
        "D02_unlock": False,
        "D02_gate_credit": 0,
        "D02_task_credit": 0,
        "D02_formal_pending_task_count": PENDING_D02,
        "D02_started": False,
    }


def exact_v6_official_rejection(
        policy_guard: HeldInputSet) -> tuple[dict[str, Any], HeldPinnedInput]:
    receipt_guard = held_v6_official_rejection(policy_guard)
    need(receipt_guard.path == V6_OFFICIAL_REJECTION and
         sha(receipt_guard.raw) == V6_OFFICIAL_REJECTION_FILE_PIN,
         "exact held v6 official rejection file pin")
    value = strict_json(receipt_guard.raw, "official v6 rejection")
    verify_object(value, "official v6 rejection",
                  V6_OFFICIAL_REJECTION_OBJECT_PIN)
    exact_keys = {
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
    }
    need(set(value) == exact_keys and
         receipt_guard.raw == canonical(value) + b"\n" and
         value.get("schema") ==
             "cm2.round306c79g.true-global-no-producer-consumer.v6.later-rejection" and
         value.get("status") ==
             "PERMANENT_FAIL_CLOSED_REJECTION__ZERO_CREDIT" and
         value.get("rejection_reason") ==
             "ORPHANED_OR_INCOMPLETE_C79G_V6_SURFACE" and
         value.get("effective_checkpoint_object_sha256") == UPSTREAM_CHECKPOINT_OBJECT_PIN and
         value.get("namespace_exact_path") ==
             str(V6_OFFICIAL_REJECTION.parent.relative_to(ROOT)) and
         value.get("target_exact_path") ==
             str(V6_OFFICIAL_REJECTION.relative_to(ROOT)) and
         value.get("namespace_at_rest_mode") == "0555" and
         value.get("rejection_file_mode") == "0444" and
         value.get("rejection_file_nlink") == 1 and
         value.get("closed_schema_file_sha256") ==
             V6_FROZEN_FILES["closed_schema_v6"][1] and
         value.get("contract_file_sha256") ==
             V6_FROZEN_FILES["contract_v6"][1] and
         value.get("contract_object_sha256") ==
             V6_FROZEN_OBJECTS["contract_v6"] and
         value.get("producer_file_sha256") ==
             V6_FROZEN_FILES["build_only_producer_v6"][1] and
         value.get("consumer_file_sha256") ==
             V6_FROZEN_FILES["independent_consumer_v6"][1] and
         value.get("cold_launcher_file_sha256") ==
             V6_FROZEN_FILES["cold_launcher_v6"][1] and
         value.get("cold_manifest_file_sha256") ==
             V6_FROZEN_FILES["cold_manifest_v6"][1] and
         value.get("cold_outer_file_sha256") ==
             V6_FROZEN_FILES["cold_outer_v6"][1] and
         value.get("cold_outer_object_sha256") ==
             V6_FROZEN_OBJECTS["cold_outer_v6"] and
         value.get("v4_rejection_supersession_file_sha256") ==
             V4_REJECTION_SUPERSESSION_FILE_PIN and
         value.get("v4_rejection_supersession_object_sha256") ==
             V4_REJECTION_SUPERSESSION_OBJECT_PIN and
         value.get("v5_official_rejection_file_sha256") ==
             V5_OFFICIAL_REJECTION_FILE_PIN and
         value.get("v5_official_rejection_object_sha256") ==
             V5_OFFICIAL_REJECTION_OBJECT_PIN and
         value.get("formal_global_closure_credit") == 0 and
         value.get("D02_unlock") is False and
         value.get("D02_gate_credit") == 0 and
         value.get("D02_task_credit") == 0 and
         value.get("D02_formal_pending_task_count") == PENDING_D02 and
         value.get("D02_started") is False and
         value.get("standalone_authority") is False and
         value.get("overwrite_delete_or_reuse_allowed") is False,
         "v6 official rejection canonical singleton zero-credit envelope")
    return value, receipt_guard


def validate_v6_published_then_rejected_predecessor(
        policy_guard: HeldInputSet, v6_guard: HeldInputSet,
        v6_source_metadata: list[HeldOpaqueMetadata]) -> dict[str, Any]:
    _, rejection_guard = exact_v6_official_rejection(policy_guard)
    source_names = {
        "build_only_producer_v6", "independent_consumer_v6",
        "cold_launcher_v6"}
    readable_by_path = {item.path: item for item in v6_guard.files}
    source_by_path = {item.path: item for item in v6_source_metadata}
    need(set(readable_by_path) == {
             path for name, (path, _) in V6_FROZEN_FILES.items()
             if name not in source_names} and
         set(source_by_path) == {
             path for name, (path, _) in V6_FROZEN_FILES.items()
             if name in source_names},
         "published v6 exact10 exact7-readable/exact3-metadata partition")
    for name, (path, file_pin) in V6_FROZEN_FILES.items():
        if name in source_names:
            metadata = source_by_path[path]
            need(stat.S_ISREG(metadata.before.st_mode) and
                 stat.S_IMODE(metadata.before.st_mode) == 0o444 and
                 metadata.before.st_nlink == 1,
                 "published v6 strict O_PATH metadata source:" + name)
            continue
        held = readable_by_path[path]
        need(sha(held.raw) == file_pin,
             "published v6 readable member pin:" + name)
        if name in V6_FROZEN_OBJECTS:
            parsed = strict_json(held.raw, "published v6 object:" + name)
            verify_object(parsed, "published v6 object:" + name,
                          V6_FROZEN_OBJECTS[name])
    exact8_expected = [
        {"file_sha256": V6_FROZEN_FILES[name][1],
         "entry_name": str(V6_FROZEN_FILES[name][0].relative_to(ROOT))}
        for name in V6_EXACT10_ORDER[:8]
    ]
    manifest_guard = readable_by_path[V6_FROZEN_FILES["cold_manifest_v6"][0]]
    outer_guard = readable_by_path[V6_FROZEN_FILES["cold_outer_v6"][0]]
    manifest = parse_manifest_ordered(manifest_guard.raw,
                                      "published v6 exact8 manifest")
    outer = strict_json(outer_guard.raw, "published v6 outer-last")
    verify_object(outer, "published v6 outer-last",
                  V6_FROZEN_OBJECTS["cold_outer_v6"])
    exact8_stats = []
    for name in V6_EXACT10_ORDER[:8]:
        path = V6_FROZEN_FILES[name][0]
        held_member = (source_by_path[path] if name in source_names
                       else readable_by_path[path])
        exact8_stats.append(held_member.before)
    chronology = cold_publication_chronology(
        exact8_stats, manifest_guard.before, outer_guard.before)
    need(manifest == exact8_expected and
         outer.get("exact8_ordered_entries") == [
             {"path": item["entry_name"],
              "file_sha256": item["file_sha256"]}
             for item in exact8_expected] and
         outer.get("status") ==
             "FROZEN_COLD_LAUNCH_OUTER_LAST__EXACT8_MANIFEST_CLOSED__RUNTIME_DEFERRED" and
         outer.get("formal_global_closure_credit") == 0 and
         outer.get("D02_unlock") is False and
         outer.get("runtime_executed_during_static_freeze") is False and
         all(chronology.values()) and
         max(outer_guard.before.st_mtime_ns, outer_guard.before.st_ctime_ns) <
             min(rejection_guard.before.st_mtime_ns,
                 rejection_guard.before.st_ctime_ns),
         "published v6 exact10 manifest/outer/official-rejection chronology")
    identities = ({item.identity for item in v6_guard.files} |
                  {item.identity for item in v6_source_metadata} |
                  {rejection_guard.identity})
    mount_ids = ({item.mount_id for item in v6_guard.files} |
                 {item.mount_id for item in v6_source_metadata} |
                 {rejection_guard.mount_id})
    need(len(identities) == 11 and len(mount_ids) == 1,
         "published v6 exact10 plus official rejection unique on one statx mount")
    return _expected_published_then_rejected_v6_proof()


def _expected_published_v7_exact10() -> list[dict[str, Any]]:
    public_names = {
        "v6_official_rejection": "v6_official_rejection",
        "closed_schema_v7": "closed_schema",
        "contract_v7": "contract",
        "build_only_producer_v7": "build_only_producer",
        "independent_consumer_v7": "independent_consumer",
        "transition_v6_to_v7": "v6_to_v7_transition",
        "static_audit_v7": "static_audit",
        "cold_launcher_v7": "cold_launcher",
        "cold_manifest_v7": "cold_manifest",
        "cold_outer_v7": "cold_outer",
    }
    expected: list[dict[str, Any]] = []
    for name in V7_EXACT10_ORDER:
        path, file_sha256 = V7_FROZEN_FILES[name]
        entry: dict[str, Any] = {
            "name": public_names[name],
            "path": str(path.relative_to(ROOT)),
            "file_sha256": file_sha256,
        }
        if name in V7_FROZEN_OBJECTS:
            entry["object_sha256"] = V7_FROZEN_OBJECTS[name]
        expected.append(entry)
    return expected


def validate_v7_common_official_rejection_fields() -> dict[str, Any]:
    return {
        "path": str(V7_OFFICIAL_REJECTION.relative_to(ROOT)),
        "namespace_path": str(V7_OFFICIAL_REJECTION.parent.relative_to(ROOT)),
        "file_sha256": V7_OFFICIAL_REJECTION_FILE_PIN,
        "object_sha256": V7_OFFICIAL_REJECTION_OBJECT_PIN,
        "schema":
            "cm2.round306c79g.true-global-no-producer-consumer.v7.later-rejection",
        "status": "PERMANENT_FAIL_CLOSED_REJECTION__ZERO_CREDIT",
        "reason": "ORPHANED_OR_INCOMPLETE_C79G_V7_SURFACE",
        "namespace_mode": "0555",
        "namespace_nlink": 2,
        "member_mode": "0444",
        "member_nlink": 1,
        "exact_member_universe": ["rejection.json"],
        "formal_global_closure_credit": 0,
        "D02_unlock": False,
        "D02_gate_credit": 0,
        "D02_task_credit": 0,
        "D02_formal_pending_task_count": PENDING_D02,
        "D02_started": False,
        "overwrite_delete_or_reuse_allowed": False,
    }


def _validated_v7_publication_lock_continuity_incident() -> dict[str, Any]:
    incident = copy.deepcopy(V7_PUBLICATION_LOCK_CONTINUITY_INCIDENT)
    need(len(incident) == 26 and
         set(incident) == {
             "D02_started", "D02_unlock",
             "effective_checkpoint_object_sha256",
             "exact10_bytes_alone_do_not_prove_publication_acceptance",
             "failure_trigger", "false_extra_assumption",
             "in_lock_terminal_replay_attempt_started",
             "incident_fact_comes_from_publisher_control_flow_record_not_from_timestamps_alone",
             "incident_id", "later_read_only_replay_cannot_rehabilitate_v7",
             "object_sha256", "official_rejection_file_sha256",
             "official_rejection_object_sha256", "outer_frozen_and_fsynced",
             "outer_then_rejection_chronology_validated",
             "positive_runtime_surface_count",
             "postincident_byte_replay_passed_but_did_not_restore_lock_continuity",
             "publication_lock_continuity_interrupted_after_outer_before_required_replay_completion",
             "publication_lock_released_on_replay_attempt_failure",
             "published_exact10_count", "published_outer_file_sha256",
             "published_outer_object_sha256",
             "required_in_lock_terminal_replay_completed", "schema",
             "v7_formal_credit_transferred", "v7_runtime_command_count",
         }, "v7 publication-lock incident exact26 key closure")
    verify_object(
        incident, "v7 publication-lock continuity incident",
        "15f92090e77eda4c6acac0af759541fe47dc4f8358e15659077d6dea8071e764")
    return incident


def _expected_published_then_rejected_v7_proof() -> dict[str, Any]:
    return {
        "ordered_published_exact10": _expected_published_v7_exact10(),
        "all_ten_file_pins_match": True,
        "all_declared_object_pins_match": True,
        "all_ten_regular_0444_nlink1": True,
        "exact8_manifest_reconstructs_first_eight_in_order": True,
        "outer_last_pins_manifest_and_launcher": True,
        "outer_then_rejection_chronology_validated": True,
        "official_later_rejection":
            validate_v7_common_official_rejection_fields(),
        "publication_lock_continuity_incident":
            _validated_v7_publication_lock_continuity_incident(),
        "first_runtime_entry_attempt": {
            "attempted": False,
            "producer_child_spawned": False,
            "candidate_write_started": False,
            "positive_runtime_surface_count": 0,
        },
        "v7_execution_allowed": False,
        "v7_runtime_surfaces_authoritative": False,
        "formal_global_closure_credit": 0,
        "D02_unlock": False,
        "D02_gate_credit": 0,
        "D02_task_credit": 0,
        "D02_formal_pending_task_count": PENDING_D02,
        "D02_started": False,
    }


def exact_v7_official_rejection(
        policy_guard: HeldInputSet) -> tuple[dict[str, Any], HeldPinnedInput]:
    receipt_guard = held_v7_official_rejection(policy_guard)
    need(receipt_guard.path == V7_OFFICIAL_REJECTION and
         sha(receipt_guard.raw) == V7_OFFICIAL_REJECTION_FILE_PIN,
         "exact held v7 official rejection file pin")
    value = strict_json(receipt_guard.raw, "official v7 rejection")
    verify_object(value, "official v7 rejection", V7_OFFICIAL_REJECTION_OBJECT_PIN)
    need(receipt_guard.raw == canonical(value) + b"\n" and len(value) == 43 and
         value.get("schema") ==
             "cm2.round306c79g.true-global-no-producer-consumer.v7.later-rejection" and
         value.get("status") ==
             "PERMANENT_FAIL_CLOSED_REJECTION__ZERO_CREDIT" and
         value.get("rejection_reason") ==
             "ORPHANED_OR_INCOMPLETE_C79G_V7_SURFACE" and
         value.get("effective_checkpoint_object_sha256") == UPSTREAM_CHECKPOINT_OBJECT_PIN and
         value.get("namespace_exact_path") ==
             str(V7_OFFICIAL_REJECTION.parent.relative_to(ROOT)) and
         value.get("target_exact_path") ==
             str(V7_OFFICIAL_REJECTION.relative_to(ROOT)) and
         value.get("namespace_at_rest_mode") == "0555" and
         value.get("rejection_file_mode") == "0444" and
         value.get("rejection_file_nlink") == 1 and
         value.get("closed_schema_file_sha256") ==
             V7_FROZEN_FILES["closed_schema_v7"][1] and
         value.get("contract_file_sha256") ==
             V7_FROZEN_FILES["contract_v7"][1] and
         value.get("contract_object_sha256") ==
             V7_FROZEN_OBJECTS["contract_v7"] and
         value.get("producer_file_sha256") ==
             V7_FROZEN_FILES["build_only_producer_v7"][1] and
         value.get("consumer_file_sha256") ==
             V7_FROZEN_FILES["independent_consumer_v7"][1] and
         value.get("cold_launcher_file_sha256") ==
             V7_FROZEN_FILES["cold_launcher_v7"][1] and
         value.get("cold_manifest_file_sha256") ==
             V7_FROZEN_FILES["cold_manifest_v7"][1] and
         value.get("cold_outer_file_sha256") ==
             V7_FROZEN_FILES["cold_outer_v7"][1] and
         value.get("cold_outer_object_sha256") ==
             V7_FROZEN_OBJECTS["cold_outer_v7"] and
         value.get("v4_rejection_supersession_file_sha256") ==
             V4_REJECTION_SUPERSESSION_FILE_PIN and
         value.get("v4_rejection_supersession_object_sha256") ==
             V4_REJECTION_SUPERSESSION_OBJECT_PIN and
         value.get("v5_official_rejection_file_sha256") ==
             V5_OFFICIAL_REJECTION_FILE_PIN and
         value.get("v5_official_rejection_object_sha256") ==
             V5_OFFICIAL_REJECTION_OBJECT_PIN and
         value.get("v6_official_rejection_file_sha256") ==
             V6_OFFICIAL_REJECTION_FILE_PIN and
         value.get("v6_official_rejection_object_sha256") ==
             V6_OFFICIAL_REJECTION_OBJECT_PIN and
         value.get("formal_global_closure_credit") == 0 and
         value.get("D02_unlock") is False and
         value.get("D02_gate_credit") == 0 and
         value.get("D02_task_credit") == 0 and
         value.get("D02_formal_pending_task_count") == PENDING_D02 and
         value.get("D02_started") is False and
         value.get("standalone_authority") is False and
         value.get("overwrite_delete_or_reuse_allowed") is False,
         "v7 official rejection canonical singleton zero-credit envelope")
    return value, receipt_guard


def validate_v7_published_then_rejected_predecessor(
        policy_guard: HeldInputSet, v7_guard: HeldInputSet,
        v7_source_metadata: list[HeldOpaqueMetadata]) -> dict[str, Any]:
    _, rejection_guard = exact_v7_official_rejection(policy_guard)
    source_names = {
        "build_only_producer_v7", "independent_consumer_v7",
        "cold_launcher_v7"}
    readable_by_path = {item.path: item for item in v7_guard.files}
    source_by_path = {item.path: item for item in v7_source_metadata}
    need(set(readable_by_path) == {
             path for name, (path, _) in V7_FROZEN_FILES.items()
             if name not in source_names} and
         set(source_by_path) == {
             path for name, (path, _) in V7_FROZEN_FILES.items()
             if name in source_names},
         "published v7 exact10 exact7-readable/exact3-metadata partition")
    for name, (path, file_pin) in V7_FROZEN_FILES.items():
        if name in source_names:
            metadata = source_by_path[path]
            need(stat.S_ISREG(metadata.before.st_mode) and
                 stat.S_IMODE(metadata.before.st_mode) == 0o444 and
                 metadata.before.st_nlink == 1,
                 "published v7 strict O_PATH metadata source:" + name)
            continue
        held = readable_by_path[path]
        need(sha(held.raw) == file_pin,
             "published v7 readable member pin:" + name)
        if name in V7_FROZEN_OBJECTS:
            parsed = strict_json(held.raw, "published v7 object:" + name)
            verify_object(parsed, "published v7 object:" + name,
                          V7_FROZEN_OBJECTS[name])
    exact8_expected = [
        {"file_sha256": V7_FROZEN_FILES[name][1],
         "entry_name": str(V7_FROZEN_FILES[name][0].relative_to(ROOT))}
        for name in V7_EXACT10_ORDER[:8]
    ]
    manifest_guard = readable_by_path[V7_FROZEN_FILES["cold_manifest_v7"][0]]
    outer_guard = readable_by_path[V7_FROZEN_FILES["cold_outer_v7"][0]]
    manifest = parse_manifest_ordered(manifest_guard.raw,
                                      "published v7 exact8 manifest")
    outer = strict_json(outer_guard.raw, "published v7 outer-last")
    verify_object(outer, "published v7 outer-last",
                  V7_FROZEN_OBJECTS["cold_outer_v7"])
    exact8_stats = []
    for name in V7_EXACT10_ORDER[:8]:
        path = V7_FROZEN_FILES[name][0]
        exact8_stats.append((source_by_path[path] if name in source_names
                             else readable_by_path[path]).before)
    chronology = cold_publication_chronology(
        exact8_stats, manifest_guard.before, outer_guard.before)
    need(manifest == exact8_expected and
         outer.get("exact8_ordered_entries") == [
             {"path": item["entry_name"], "file_sha256": item["file_sha256"]}
             for item in exact8_expected] and
         outer.get("status") ==
             "FROZEN_COLD_LAUNCH_OUTER_LAST__EXACT8_MANIFEST_CLOSED__RUNTIME_DEFERRED" and
         outer.get("formal_global_closure_credit") == 0 and
         outer.get("D02_unlock") is False and
         outer.get("runtime_executed_during_static_freeze") is False and
         all(chronology.values()) and
         max(outer_guard.before.st_mtime_ns, outer_guard.before.st_ctime_ns) <
             min(rejection_guard.before.st_mtime_ns,
                 rejection_guard.before.st_ctime_ns),
         "published v7 exact10 manifest/outer/official-rejection chronology")
    identities = ({item.identity for item in v7_guard.files} |
                  {item.identity for item in v7_source_metadata} |
                  {rejection_guard.identity})
    mount_ids = ({item.mount_id for item in v7_guard.files} |
                 {item.mount_id for item in v7_source_metadata} |
                 {rejection_guard.mount_id})
    need(len(identities) == 11 and len(mount_ids) == 1,
         "published v7 exact10 plus official rejection unique on one statx mount")
    return _expected_published_then_rejected_v7_proof()


def _expected_published_v8_exact10() -> list[dict[str, Any]]:
    public_names = {
        "v7_official_rejection": "v7_official_rejection",
        "closed_schema_v8": "closed_schema",
        "contract_v8": "contract",
        "build_only_producer_v8": "build_only_producer",
        "independent_consumer_v8": "independent_consumer",
        "transition_v7_to_v8": "v7_to_v8_transition",
        "static_audit_v8": "static_audit",
        "cold_launcher_v8": "cold_launcher",
        "cold_manifest_v8": "cold_manifest",
        "cold_outer_v8": "cold_outer",
    }
    expected: list[dict[str, Any]] = []
    for name in V8_EXACT10_ORDER:
        path, file_sha256 = V8_FROZEN_FILES[name]
        entry: dict[str, Any] = {
            "name": public_names[name],
            "path": str(path.relative_to(ROOT)),
            "file_sha256": file_sha256,
        }
        if name in V8_FROZEN_OBJECTS:
            entry["object_sha256"] = V8_FROZEN_OBJECTS[name]
        expected.append(entry)
    return expected


def validate_v8_common_official_rejection_fields() -> dict[str, Any]:
    return {
        "path": str(V8_OFFICIAL_REJECTION.relative_to(ROOT)),
        "namespace_path": str(V8_OFFICIAL_REJECTION.parent.relative_to(ROOT)),
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
        "D02_formal_pending_task_count": PENDING_D02,
        "D02_started": False,
        "overwrite_delete_or_reuse_allowed": False,
    }


def _expected_published_then_rejected_v8_proof() -> dict[str, Any]:
    return {
        "ordered_published_exact10": _expected_published_v8_exact10(),
        "all_ten_file_pins_match": True,
        "all_declared_object_pins_match": True,
        "all_ten_regular_0444_nlink1": True,
        "exact8_manifest_reconstructs_first_eight_in_order": True,
        "outer_last_pins_manifest_and_launcher": True,
        "outer_then_rejection_chronology_validated": True,
        "chronology_is_not_control_flow_proof": True,
        "official_later_rejection":
            validate_v8_common_official_rejection_fields(),
        "first_rollout_attempt": copy.deepcopy(V8_FIRST_ROLLOUT_ATTEMPT),
        "rollout_control_flow_incident": copy.deepcopy(
            V8_ROLLOUT_CONTROL_FLOW_INCIDENT),
        "v8_execution_allowed": False,
        "v8_runtime_surfaces_authoritative": False,
        "formal_global_closure_credit": 0,
        "D02_unlock": False,
        "D02_gate_credit": 0,
        "D02_task_credit": 0,
        "D02_formal_pending_task_count": PENDING_D02,
        "D02_started": False,
    }


def exact_v8_official_rejection(
        policy_guard: HeldInputSet) -> tuple[dict[str, Any], HeldPinnedInput]:
    receipt_guard = held_v8_official_rejection(policy_guard)
    need(receipt_guard.path == V8_OFFICIAL_REJECTION and
         sha(receipt_guard.raw) == V8_OFFICIAL_REJECTION_FILE_PIN,
         "exact held v8 official rejection file pin")
    value = strict_json(receipt_guard.raw, "official v8 rejection")
    verify_object(value, "official v8 rejection", V8_OFFICIAL_REJECTION_OBJECT_PIN)
    exact_keys = {
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
    }
    need(set(value) == exact_keys and
         receipt_guard.raw == canonical(value) + b"\n" and
         value.get("schema") ==
             "cm2.round306c79g.true-global-no-producer-consumer.v8.later-rejection" and
         value.get("status") ==
             "PERMANENT_FAIL_CLOSED_REJECTION__ZERO_CREDIT" and
         value.get("rejection_reason") ==
             "ORPHANED_OR_INCOMPLETE_C79G_V8_SURFACE" and
         value.get("effective_checkpoint_object_sha256") == UPSTREAM_CHECKPOINT_OBJECT_PIN and
         value.get("namespace_exact_path") ==
             str(V8_OFFICIAL_REJECTION.parent.relative_to(ROOT)) and
         value.get("target_exact_path") ==
             str(V8_OFFICIAL_REJECTION.relative_to(ROOT)) and
         value.get("namespace_at_rest_mode") == "0555" and
         value.get("namespace_lock_held_write_window_mode") == "0755" and
         value.get("rejection_file_mode") == "0444" and
         value.get("rejection_file_nlink") == 1 and
         value.get("closed_schema_file_sha256") ==
             V8_FROZEN_FILES["closed_schema_v8"][1] and
         value.get("contract_file_sha256") ==
             V8_FROZEN_FILES["contract_v8"][1] and
         value.get("contract_object_sha256") ==
             V8_FROZEN_OBJECTS["contract_v8"] and
         value.get("producer_file_sha256") ==
             V8_FROZEN_FILES["build_only_producer_v8"][1] and
         value.get("consumer_file_sha256") ==
             V8_FROZEN_FILES["independent_consumer_v8"][1] and
         value.get("cold_launcher_file_sha256") ==
             V8_FROZEN_FILES["cold_launcher_v8"][1] and
         value.get("cold_manifest_file_sha256") ==
             V8_FROZEN_FILES["cold_manifest_v8"][1] and
         value.get("cold_outer_file_sha256") ==
             V8_FROZEN_FILES["cold_outer_v8"][1] and
         value.get("cold_outer_object_sha256") ==
             V8_FROZEN_OBJECTS["cold_outer_v8"] and
         value.get("v4_rejection_supersession_file_sha256") ==
             V4_REJECTION_SUPERSESSION_FILE_PIN and
         value.get("v4_rejection_supersession_object_sha256") ==
             V4_REJECTION_SUPERSESSION_OBJECT_PIN and
         value.get("v5_official_rejection_file_sha256") ==
             V5_OFFICIAL_REJECTION_FILE_PIN and
         value.get("v5_official_rejection_object_sha256") ==
             V5_OFFICIAL_REJECTION_OBJECT_PIN and
         value.get("v6_official_rejection_file_sha256") ==
             V6_OFFICIAL_REJECTION_FILE_PIN and
         value.get("v6_official_rejection_object_sha256") ==
             V6_OFFICIAL_REJECTION_OBJECT_PIN and
         value.get("v7_official_rejection_file_sha256") ==
             V7_OFFICIAL_REJECTION_FILE_PIN and
         value.get("v7_official_rejection_object_sha256") ==
             V7_OFFICIAL_REJECTION_OBJECT_PIN and
         value.get("v7_publication_lock_continuity_incident_object_sha256") ==
             V7_PUBLICATION_LOCK_CONTINUITY_INCIDENT["object_sha256"] and
         value.get("formal_global_closure_credit") == 0 and
         value.get("D02_unlock") is False and
         value.get("D02_gate_credit") == 0 and
         value.get("D02_task_credit") == 0 and
         value.get("D02_formal_pending_task_count") == PENDING_D02 and
         value.get("D02_started") is False and
         value.get("standalone_authority") is False and
         value.get("overwrite_delete_or_reuse_allowed") is False,
         "v8 official rejection canonical singleton zero-credit envelope")
    return value, receipt_guard


def validate_v8_published_then_rejected_predecessor(
        policy_guard: HeldInputSet, v8_guard: HeldInputSet,
        v8_source_metadata: list[HeldOpaqueMetadata]) -> dict[str, Any]:
    _, rejection_guard = exact_v8_official_rejection(policy_guard)
    source_names = {
        "build_only_producer_v8", "independent_consumer_v8",
        "cold_launcher_v8"}
    readable_by_path = {item.path: item for item in v8_guard.files}
    source_by_path = {item.path: item for item in v8_source_metadata}
    need(set(readable_by_path) == {
             path for name, (path, _) in V8_FROZEN_FILES.items()
             if name not in source_names} and
         set(source_by_path) == {
             path for name, (path, _) in V8_FROZEN_FILES.items()
             if name in source_names},
         "published v8 exact10 exact7-readable/exact3-metadata partition")
    for name, (path, file_pin) in V8_FROZEN_FILES.items():
        if name in source_names:
            metadata = source_by_path[path]
            need(stat.S_ISREG(metadata.before.st_mode) and
                 stat.S_IMODE(metadata.before.st_mode) == 0o444 and
                 metadata.before.st_nlink == 1,
                 "published v8 strict O_PATH metadata source:" + name)
            continue
        held = readable_by_path[path]
        need(sha(held.raw) == file_pin,
             "published v8 readable member pin:" + name)
        if name in V8_FROZEN_OBJECTS:
            parsed = strict_json(held.raw, "published v8 object:" + name)
            verify_object(parsed, "published v8 object:" + name,
                          V8_FROZEN_OBJECTS[name])
    exact8_expected = [
        {"file_sha256": V8_FROZEN_FILES[name][1],
         "entry_name": str(V8_FROZEN_FILES[name][0].relative_to(ROOT))}
        for name in V8_EXACT10_ORDER[:8]
    ]
    manifest_guard = readable_by_path[V8_FROZEN_FILES["cold_manifest_v8"][0]]
    outer_guard = readable_by_path[V8_FROZEN_FILES["cold_outer_v8"][0]]
    manifest = parse_manifest_ordered(
        manifest_guard.raw, "published v8 exact8 manifest")
    outer = strict_json(outer_guard.raw, "published v8 outer-last")
    verify_object(outer, "published v8 outer-last",
                  V8_FROZEN_OBJECTS["cold_outer_v8"])
    exact8_stats = []
    for name in V8_EXACT10_ORDER[:8]:
        path = V8_FROZEN_FILES[name][0]
        exact8_stats.append((source_by_path[path] if name in source_names
                             else readable_by_path[path]).before)
    chronology = cold_publication_chronology(
        exact8_stats, manifest_guard.before, outer_guard.before)
    need(manifest == exact8_expected and
         outer.get("exact8_ordered_entries") == [
             {"path": item["entry_name"], "file_sha256": item["file_sha256"]}
             for item in exact8_expected] and
         outer.get("status") ==
             "FROZEN_COLD_LAUNCH_OUTER_LAST__EXACT8_MANIFEST_CLOSED__RUNTIME_DEFERRED" and
         outer.get("formal_global_closure_credit") == 0 and
         outer.get("D02_unlock") is False and
         outer.get("runtime_executed_during_static_freeze") is False and
         all(chronology.values()) and
         max(outer_guard.before.st_mtime_ns, outer_guard.before.st_ctime_ns) <
             min(rejection_guard.before.st_mtime_ns,
                 rejection_guard.before.st_ctime_ns),
         "published v8 exact10 manifest/outer/official-rejection chronology")
    identities = ({item.identity for item in v8_guard.files} |
                  {item.identity for item in v8_source_metadata} |
                  {rejection_guard.identity})
    mount_ids = ({item.mount_id for item in v8_guard.files} |
                 {item.mount_id for item in v8_source_metadata} |
                 {rejection_guard.mount_id})
    need(len(identities) == 11 and len(mount_ids) == 1,
         "published v8 exact10 plus official rejection unique on one statx mount")
    require_v8_positive_and_stage_surfaces_absent()
    return _expected_published_then_rejected_v8_proof()


def _expected_published_v9_exact10() -> list[dict[str, Any]]:
    public_names = {
        "v8_official_rejection": "v8_official_rejection",
        "closed_schema_v9": "closed_schema",
        "contract_v9": "contract",
        "build_only_producer_v9": "build_only_producer",
        "independent_consumer_v9": "independent_consumer",
        "transition_v8_to_v9": "v8_to_v9_transition",
        "static_audit_v9": "static_audit",
        "cold_launcher_v9": "cold_launcher",
        "cold_manifest_v9": "cold_manifest",
        "cold_outer_v9": "cold_outer",
    }
    expected: list[dict[str, Any]] = []
    for name in V9_EXACT10_ORDER:
        path, file_sha256 = V9_FROZEN_FILES[name]
        entry: dict[str, Any] = {
            "name": public_names[name],
            "path": str(path.relative_to(ROOT)),
            "file_sha256": file_sha256,
        }
        if name in V9_FROZEN_OBJECTS:
            entry["object_sha256"] = V9_FROZEN_OBJECTS[name]
        expected.append(entry)
    return expected


def validate_v9_common_official_rejection_fields() -> dict[str, Any]:
    return {
        "path": str(V9_OFFICIAL_REJECTION.relative_to(ROOT)),
        "namespace_path": str(V9_OFFICIAL_REJECTION.parent.relative_to(ROOT)),
        "file_sha256": V9_OFFICIAL_REJECTION_FILE_PIN,
        "object_sha256": V9_OFFICIAL_REJECTION_OBJECT_PIN,
        "schema":
            "cm2.round306c79g.true-global-no-producer-consumer.v9.later-rejection",
        "status": "PERMANENT_FAIL_CLOSED_REJECTION__ZERO_CREDIT",
        "reason": "ORPHANED_OR_INCOMPLETE_C79G_V9_SURFACE",
        "namespace_mode": "0555",
        "namespace_nlink": 2,
        "member_mode": "0444",
        "member_nlink": 1,
        "exact_member_universe": ["rejection.json"],
        "formal_global_closure_credit": 0,
        "D02_unlock": False,
        "D02_gate_credit": 0,
        "D02_task_credit": 0,
        "D02_formal_pending_task_count": PENDING_D02,
        "D02_started": False,
        "overwrite_delete_or_reuse_allowed": False,
    }


def _expected_published_then_rejected_v9_proof() -> dict[str, Any]:
    return {
        "ordered_published_exact10": _expected_published_v9_exact10(),
        "all_ten_file_pins_match": True,
        "all_declared_object_pins_match": True,
        "all_ten_regular_0444_nlink1": True,
        "exact8_manifest_reconstructs_first_eight_in_order": True,
        "outer_last_pins_manifest_and_launcher": True,
        "outer_then_rejection_chronology_validated": True,
        "official_later_rejection":
            validate_v9_common_official_rejection_fields(),
        "first_runtime_attempt": copy.deepcopy(V9_FIRST_RUNTIME_ATTEMPT),
        "v6_held_self_identity_defect_shape_drift_incident": copy.deepcopy(
            V9_V6_HELD_SELF_IDENTITY_DEFECT_SHAPE_DRIFT_INCIDENT),
        "positive_and_stage_surfaces_absent": {
            "exact_absent_path_count":
                len(V9_ALL_POSITIVE_AND_STAGE_SURFACES),
            "exact_absent_paths": [
                str(path.relative_to(ROOT))
                for path in V9_ALL_POSITIVE_AND_STAGE_SURFACES
            ],
            "all_absent": True,
        },
        "v9_execution_allowed": False,
        "v9_runtime_surfaces_authoritative": False,
        "formal_global_closure_credit": 0,
        "D02_unlock": False,
        "D02_gate_credit": 0,
        "D02_task_credit": 0,
        "D02_formal_pending_task_count": PENDING_D02,
        "D02_started": False,
    }


def exact_v9_official_rejection(
        policy_guard: HeldInputSet) -> tuple[dict[str, Any], HeldPinnedInput]:
    receipt_guard = held_v9_official_rejection(policy_guard)
    need(receipt_guard.path == V9_OFFICIAL_REJECTION and
         sha(receipt_guard.raw) == V9_OFFICIAL_REJECTION_FILE_PIN,
         "exact held v9 official rejection file pin")
    value = strict_json(receipt_guard.raw, "official v9 rejection")
    verify_object(value, "official v9 rejection", V9_OFFICIAL_REJECTION_OBJECT_PIN)
    exact_keys = {
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
    }
    expected_pins = {
        "closed_schema_file_sha256": V9_FROZEN_FILES["closed_schema_v9"][1],
        "contract_file_sha256": V9_FROZEN_FILES["contract_v9"][1],
        "contract_object_sha256": V9_FROZEN_OBJECTS["contract_v9"],
        "producer_file_sha256": V9_FROZEN_FILES["build_only_producer_v9"][1],
        "consumer_file_sha256": V9_FROZEN_FILES["independent_consumer_v9"][1],
        "cold_launcher_file_sha256": V9_FROZEN_FILES["cold_launcher_v9"][1],
        "cold_manifest_file_sha256": V9_FROZEN_FILES["cold_manifest_v9"][1],
        "cold_outer_file_sha256": V9_FROZEN_FILES["cold_outer_v9"][1],
        "cold_outer_object_sha256": V9_FROZEN_OBJECTS["cold_outer_v9"],
        "v4_rejection_supersession_file_sha256":
            V4_REJECTION_SUPERSESSION_FILE_PIN,
        "v4_rejection_supersession_object_sha256":
            V4_REJECTION_SUPERSESSION_OBJECT_PIN,
        "v5_official_rejection_file_sha256": V5_OFFICIAL_REJECTION_FILE_PIN,
        "v5_official_rejection_object_sha256": V5_OFFICIAL_REJECTION_OBJECT_PIN,
        "v6_official_rejection_file_sha256": V6_OFFICIAL_REJECTION_FILE_PIN,
        "v6_official_rejection_object_sha256": V6_OFFICIAL_REJECTION_OBJECT_PIN,
        "v7_official_rejection_file_sha256": V7_OFFICIAL_REJECTION_FILE_PIN,
        "v7_official_rejection_object_sha256": V7_OFFICIAL_REJECTION_OBJECT_PIN,
        "v7_publication_lock_continuity_incident_object_sha256":
            V7_PUBLICATION_LOCK_CONTINUITY_INCIDENT["object_sha256"],
        "v8_official_rejection_file_sha256":
            V8_OFFICIAL_REJECTION_FILE_PIN,
        "v8_official_rejection_object_sha256":
            V8_OFFICIAL_REJECTION_OBJECT_PIN,
    }
    need(set(value) == exact_keys and
         receipt_guard.raw == canonical(value) + b"\n" and
         value.get("schema") ==
             "cm2.round306c79g.true-global-no-producer-consumer.v9.later-rejection" and
         value.get("status") ==
             "PERMANENT_FAIL_CLOSED_REJECTION__ZERO_CREDIT" and
         value.get("rejection_reason") ==
             "ORPHANED_OR_INCOMPLETE_C79G_V9_SURFACE" and
         value.get("effective_checkpoint_object_sha256") == UPSTREAM_CHECKPOINT_OBJECT_PIN and
         value.get("namespace_exact_path") ==
             str(V9_OFFICIAL_REJECTION.parent.relative_to(ROOT)) and
         value.get("target_exact_path") ==
             str(V9_OFFICIAL_REJECTION.relative_to(ROOT)) and
         value.get("namespace_at_rest_mode") == "0555" and
         value.get("namespace_lock_held_write_window_mode") == "0755" and
         value.get("rejection_file_mode") == "0444" and
         value.get("rejection_file_nlink") == 1 and
         all(value.get(key) == expected for key, expected in expected_pins.items()) and
         value.get("formal_global_closure_credit") == 0 and
         value.get("D02_unlock") is False and
         value.get("D02_gate_credit") == 0 and
         value.get("D02_task_credit") == 0 and
         value.get("D02_formal_pending_task_count") == PENDING_D02 and
         value.get("D02_started") is False and
         value.get("standalone_authority") is False and
         value.get("overwrite_delete_or_reuse_allowed") is False,
         "v9 official rejection canonical singleton zero-credit envelope")
    return value, receipt_guard


def validate_v9_published_then_rejected_predecessor(
        policy_guard: HeldInputSet, v9_guard: HeldInputSet,
        v9_source_metadata: list[HeldOpaqueMetadata]) -> dict[str, Any]:
    _, rejection_guard = exact_v9_official_rejection(policy_guard)
    source_names = {
        "build_only_producer_v9", "independent_consumer_v9",
        "cold_launcher_v9"}
    readable_by_path = {item.path: item for item in v9_guard.files}
    source_by_path = {item.path: item for item in v9_source_metadata}
    need(set(readable_by_path) == {
             path for name, (path, _) in V9_FROZEN_FILES.items()
             if name not in source_names} and
         set(source_by_path) == {
             path for name, (path, _) in V9_FROZEN_FILES.items()
             if name in source_names},
         "published v9 exact10 exact7-readable/exact3-metadata partition")
    for name, (path, file_pin) in V9_FROZEN_FILES.items():
        if name in source_names:
            metadata = source_by_path[path]
            need(stat.S_ISREG(metadata.before.st_mode) and
                 stat.S_IMODE(metadata.before.st_mode) == 0o444 and
                 metadata.before.st_nlink == 1,
                 "published v9 strict O_PATH metadata source:" + name)
            continue
        held = readable_by_path[path]
        need(sha(held.raw) == file_pin,
             "published v9 readable member pin:" + name)
        if name in V9_FROZEN_OBJECTS:
            parsed = strict_json(held.raw, "published v9 object:" + name)
            verify_object(parsed, "published v9 object:" + name,
                          V9_FROZEN_OBJECTS[name])
    exact8_expected = [
        {"file_sha256": V9_FROZEN_FILES[name][1],
         "entry_name": str(V9_FROZEN_FILES[name][0].relative_to(ROOT))}
        for name in V9_EXACT10_ORDER[:8]
    ]
    manifest_guard = readable_by_path[V9_FROZEN_FILES["cold_manifest_v9"][0]]
    outer_guard = readable_by_path[V9_FROZEN_FILES["cold_outer_v9"][0]]
    manifest = parse_manifest_ordered(
        manifest_guard.raw, "published v9 exact8 manifest")
    outer = strict_json(outer_guard.raw, "published v9 outer-last")
    verify_object(outer, "published v9 outer-last",
                  V9_FROZEN_OBJECTS["cold_outer_v9"])
    exact8_stats = []
    for name in V9_EXACT10_ORDER[:8]:
        path = V9_FROZEN_FILES[name][0]
        exact8_stats.append((source_by_path[path] if name in source_names
                             else readable_by_path[path]).before)
    chronology = cold_publication_chronology(
        exact8_stats, manifest_guard.before, outer_guard.before)
    need(manifest == exact8_expected and
         outer.get("exact8_ordered_entries") == [
             {"path": item["entry_name"], "file_sha256": item["file_sha256"]}
             for item in exact8_expected] and
         outer.get("status") ==
             "FROZEN_COLD_LAUNCH_OUTER_LAST__EXACT8_MANIFEST_CLOSED__RUNTIME_DEFERRED" and
         outer.get("formal_global_closure_credit") == 0 and
         outer.get("D02_unlock") is False and
         outer.get("runtime_executed_during_static_freeze") is False and
         all(chronology.values()) and
         max(outer_guard.before.st_mtime_ns, outer_guard.before.st_ctime_ns) <
             min(rejection_guard.before.st_mtime_ns,
                 rejection_guard.before.st_ctime_ns),
         "published v9 exact10 manifest/outer/official-rejection chronology")
    identities = ({item.identity for item in v9_guard.files} |
                  {item.identity for item in v9_source_metadata} |
                  {rejection_guard.identity})
    mount_ids = ({item.mount_id for item in v9_guard.files} |
                 {item.mount_id for item in v9_source_metadata} |
                 {rejection_guard.mount_id})
    need(len(identities) == 11 and len(mount_ids) == 1,
         "published v9 exact10 plus official rejection unique on one statx mount")
    require_v9_positive_and_stage_surfaces_absent()
    return _expected_published_then_rejected_v9_proof()


def _expected_published_v10_exact10() -> list[dict[str, Any]]:
    public_names = {
        "v9_official_rejection": "v9_official_rejection",
        "closed_schema_v10": "closed_schema",
        "contract_v10": "contract",
        "build_only_producer_v10": "build_only_producer",
        "independent_consumer_v10": "independent_consumer",
        "transition_v9_to_v10": "v9_to_v10_transition",
        "static_audit_v10": "static_audit",
        "cold_launcher_v10": "cold_launcher",
        "cold_manifest_v10": "cold_manifest",
        "cold_outer_v10": "cold_outer",
    }
    expected: list[dict[str, Any]] = []
    for name in V10_EXACT10_ORDER:
        path, file_sha256 = V10_FROZEN_FILES[name]
        entry: dict[str, Any] = {
            "name": public_names[name],
            "path": str(path.relative_to(ROOT)),
            "file_sha256": file_sha256,
        }
        if name in V10_FROZEN_OBJECTS:
            entry["object_sha256"] = V10_FROZEN_OBJECTS[name]
        expected.append(entry)
    return expected


def validate_v10_common_official_rejection_fields() -> dict[str, Any]:
    return {
        "path": str(V10_OFFICIAL_REJECTION.relative_to(ROOT)),
        "namespace_path": str(V10_OFFICIAL_REJECTION.parent.relative_to(ROOT)),
        "file_sha256": V10_OFFICIAL_REJECTION_FILE_PIN,
        "object_sha256": V10_OFFICIAL_REJECTION_OBJECT_PIN,
        "schema":
            "cm2.round306c79g.true-global-no-producer-consumer.v10.later-rejection",
        "status": "PERMANENT_FAIL_CLOSED_REJECTION__ZERO_CREDIT",
        "reason": "ORPHANED_OR_INCOMPLETE_C79G_V10_SURFACE",
        "namespace_mode": "0555",
        "namespace_nlink": 2,
        "member_mode": "0444",
        "member_nlink": 1,
        "exact_member_universe": ["rejection.json"],
        "formal_global_closure_credit": 0,
        "D02_unlock": False,
        "D02_gate_credit": 0,
        "D02_task_credit": 0,
        "D02_formal_pending_task_count": PENDING_D02,
        "D02_started": False,
        "overwrite_delete_or_reuse_allowed": False,
    }


def _expected_published_then_rejected_v10_proof() -> dict[str, Any]:
    return {
        "ordered_published_exact10": _expected_published_v10_exact10(),
        "official_later_rejection":
            validate_v10_common_official_rejection_fields(),
        "first_runtime_attempt": copy.deepcopy(V10_FIRST_RUNTIME_ATTEMPT),
        "regression_label_prefix_incident": copy.deepcopy(
            V10_REGRESSION_LABEL_PREFIX_INCIDENT),
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
        "D02_formal_pending_task_count": PENDING_D02,
        "D02_started": False,
    }


def exact_v10_official_rejection(
        policy_guard: HeldInputSet) -> tuple[dict[str, Any], HeldPinnedInput]:
    receipt_guard = held_v10_official_rejection(policy_guard)
    need(receipt_guard.path == V10_OFFICIAL_REJECTION and
         sha(receipt_guard.raw) == V10_OFFICIAL_REJECTION_FILE_PIN,
         "exact held v10 official rejection file pin")
    value = strict_json(receipt_guard.raw, "official v10 rejection")
    verify_object(
        value, "official v10 rejection", V10_OFFICIAL_REJECTION_OBJECT_PIN)
    exact_keys = {'D02_formal_pending_task_count',
 'D02_gate_credit',
 'D02_started',
 'D02_task_credit',
 'D02_unlock',
 'closed_schema_file_sha256',
 'cold_launcher_file_sha256',
 'cold_manifest_file_sha256',
 'cold_outer_file_sha256',
 'cold_outer_object_sha256',
 'commit_operation',
 'consumer_file_sha256',
 'contract_file_sha256',
 'contract_object_sha256',
 'effective_checkpoint_object_sha256',
 'file_fsync_required',
 'formal_global_closure_credit',
 'idempotent_existing_recovery_re_fsyncs_rejection_file_namespace_and_runtime_parent',
 'namespace_at_rest_mode',
 'namespace_exact_path',
 'namespace_fsync_required_after_file_and_after_reseal',
 'namespace_lock_held_write_window_mode',
 'object_sha256',
 'official_writer_coordination_lock_held_for_entire_reject_command',
 'official_writer_coordination_lock_policy',
 'overwrite_delete_or_reuse_allowed',
 'partial_malformed_or_extra_namespace_entry_revokes_authority',
 'producer_file_sha256',
 'rejection_file_mode',
 'rejection_file_nlink',
 'rejection_reason',
 'runtime_parent_fsync_required_after_namespace_creation',
 'schema',
 'standalone_authority',
 'status',
 'target_exact_path',
 'target_is_protocol_and_checkpoint_deterministic',
 'v4_rejection_supersession_file_sha256',
 'v4_rejection_supersession_object_sha256',
 'v5_official_rejection_file_sha256',
 'v5_official_rejection_object_sha256',
 'v6_official_rejection_file_sha256',
 'v6_official_rejection_object_sha256',
 'v7_official_rejection_file_sha256',
 'v7_official_rejection_object_sha256',
 'v7_publication_lock_continuity_incident_object_sha256',
 'v8_official_rejection_file_sha256',
 'v8_official_rejection_object_sha256',
 'v9_official_rejection_file_sha256',
 'v9_official_rejection_object_sha256'}
    expected_pins = {
        "closed_schema_file_sha256": V10_FROZEN_FILES["closed_schema_v10"][1],
        "contract_file_sha256": V10_FROZEN_FILES["contract_v10"][1],
        "contract_object_sha256": V10_FROZEN_OBJECTS["contract_v10"],
        "producer_file_sha256": V10_FROZEN_FILES["build_only_producer_v10"][1],
        "consumer_file_sha256":
            V10_FROZEN_FILES["independent_consumer_v10"][1],
        "cold_launcher_file_sha256":
            V10_FROZEN_FILES["cold_launcher_v10"][1],
        "cold_manifest_file_sha256":
            V10_FROZEN_FILES["cold_manifest_v10"][1],
        "cold_outer_file_sha256": V10_FROZEN_FILES["cold_outer_v10"][1],
        "cold_outer_object_sha256": V10_FROZEN_OBJECTS["cold_outer_v10"],
        "v4_rejection_supersession_file_sha256":
            V4_REJECTION_SUPERSESSION_FILE_PIN,
        "v4_rejection_supersession_object_sha256":
            V4_REJECTION_SUPERSESSION_OBJECT_PIN,
        "v5_official_rejection_file_sha256": V5_OFFICIAL_REJECTION_FILE_PIN,
        "v5_official_rejection_object_sha256": V5_OFFICIAL_REJECTION_OBJECT_PIN,
        "v6_official_rejection_file_sha256": V6_OFFICIAL_REJECTION_FILE_PIN,
        "v6_official_rejection_object_sha256": V6_OFFICIAL_REJECTION_OBJECT_PIN,
        "v7_official_rejection_file_sha256": V7_OFFICIAL_REJECTION_FILE_PIN,
        "v7_official_rejection_object_sha256": V7_OFFICIAL_REJECTION_OBJECT_PIN,
        "v7_publication_lock_continuity_incident_object_sha256":
            V7_PUBLICATION_LOCK_CONTINUITY_INCIDENT["object_sha256"],
        "v8_official_rejection_file_sha256": V8_OFFICIAL_REJECTION_FILE_PIN,
        "v8_official_rejection_object_sha256": V8_OFFICIAL_REJECTION_OBJECT_PIN,
        "v9_official_rejection_file_sha256": V9_OFFICIAL_REJECTION_FILE_PIN,
        "v9_official_rejection_object_sha256": V9_OFFICIAL_REJECTION_OBJECT_PIN,
    }
    need(set(value) == exact_keys and len(exact_keys) == 50 and
         receipt_guard.raw == canonical(value) + b"\n" and
         value.get("schema") ==
             "cm2.round306c79g.true-global-no-producer-consumer.v10.later-rejection" and
         value.get("status") ==
             "PERMANENT_FAIL_CLOSED_REJECTION__ZERO_CREDIT" and
         value.get("rejection_reason") ==
             "ORPHANED_OR_INCOMPLETE_C79G_V10_SURFACE" and
         value.get("effective_checkpoint_object_sha256") ==
             UPSTREAM_CHECKPOINT_OBJECT_PIN and
         value.get("namespace_exact_path") ==
             str(V10_OFFICIAL_REJECTION.parent.relative_to(ROOT)) and
         value.get("target_exact_path") ==
             str(V10_OFFICIAL_REJECTION.relative_to(ROOT)) and
         value.get("namespace_at_rest_mode") == "0555" and
         value.get("namespace_lock_held_write_window_mode") == "0755" and
         value.get("rejection_file_mode") == "0444" and
         value.get("rejection_file_nlink") == 1 and
         all(value.get(key) == expected
             for key, expected in expected_pins.items()) and
         value.get("formal_global_closure_credit") == 0 and
         value.get("D02_unlock") is False and
         value.get("D02_gate_credit") == 0 and
         value.get("D02_task_credit") == 0 and
         value.get("D02_formal_pending_task_count") == PENDING_D02 and
         value.get("D02_started") is False and
         value.get("standalone_authority") is False and
         value.get("overwrite_delete_or_reuse_allowed") is False,
         "v10 official rejection canonical singleton zero-credit envelope")
    return value, receipt_guard


def validate_v10_published_then_rejected_predecessor(
        policy_guard: HeldInputSet, v10_guard: HeldInputSet,
        v10_source_metadata: list[HeldOpaqueMetadata]) -> dict[str, Any]:
    _, rejection_guard = exact_v10_official_rejection(policy_guard)
    source_names = {
        "build_only_producer_v10", "independent_consumer_v10",
        "cold_launcher_v10"}
    readable_by_path = {item.path: item for item in v10_guard.files}
    source_by_path = {item.path: item for item in v10_source_metadata}
    need(set(readable_by_path) == {
             path for name, (path, _) in V10_FROZEN_FILES.items()
             if name not in source_names} and
         set(source_by_path) == {
             path for name, (path, _) in V10_FROZEN_FILES.items()
             if name in source_names},
         "published v10 exact10 exact7-readable/exact3-metadata partition")
    for name, (path, file_pin) in V10_FROZEN_FILES.items():
        if name in source_names:
            metadata = source_by_path[path]
            need(stat.S_ISREG(metadata.before.st_mode) and
                 stat.S_IMODE(metadata.before.st_mode) == 0o444 and
                 metadata.before.st_nlink == 1,
                 "published v10 strict O_PATH metadata source:" + name)
            continue
        held = readable_by_path[path]
        need(sha(held.raw) == file_pin,
             "published v10 readable member pin:" + name)
        if name in V10_FROZEN_OBJECTS:
            parsed = strict_json(held.raw, "published v10 object:" + name)
            verify_object(parsed, "published v10 object:" + name,
                          V10_FROZEN_OBJECTS[name])
    exact8_expected = [
        {"file_sha256": V10_FROZEN_FILES[name][1],
         "entry_name": str(V10_FROZEN_FILES[name][0].relative_to(ROOT))}
        for name in V10_EXACT10_ORDER[:8]
    ]
    manifest_guard = readable_by_path[V10_FROZEN_FILES["cold_manifest_v10"][0]]
    outer_guard = readable_by_path[V10_FROZEN_FILES["cold_outer_v10"][0]]
    manifest = parse_manifest_ordered(
        manifest_guard.raw, "published v10 exact8 manifest")
    outer = strict_json(outer_guard.raw, "published v10 outer-last")
    verify_object(outer, "published v10 outer-last",
                  V10_FROZEN_OBJECTS["cold_outer_v10"])
    exact8_stats = []
    for name in V10_EXACT10_ORDER[:8]:
        path = V10_FROZEN_FILES[name][0]
        exact8_stats.append((source_by_path[path] if name in source_names
                             else readable_by_path[path]).before)
    chronology = cold_publication_chronology(
        exact8_stats, manifest_guard.before, outer_guard.before)
    need(manifest == exact8_expected and
         outer.get("exact8_ordered_entries") == [
             {"path": item["entry_name"], "file_sha256": item["file_sha256"]}
             for item in exact8_expected] and
         outer.get("status") ==
             "FROZEN_COLD_LAUNCH_OUTER_LAST__EXACT8_MANIFEST_CLOSED__RUNTIME_DEFERRED" and
         outer.get("formal_global_closure_credit") == 0 and
         outer.get("D02_unlock") is False and
         outer.get("runtime_executed_during_static_freeze") is False and
         all(chronology.values()) and
         max(outer_guard.before.st_mtime_ns, outer_guard.before.st_ctime_ns) <
             min(rejection_guard.before.st_mtime_ns,
                 rejection_guard.before.st_ctime_ns),
         "published v10 exact10 manifest/outer/official-rejection chronology")
    identities = ({item.identity for item in v10_guard.files} |
                  {item.identity for item in v10_source_metadata} |
                  {rejection_guard.identity})
    mount_ids = ({item.mount_id for item in v10_guard.files} |
                 {item.mount_id for item in v10_source_metadata} |
                 {rejection_guard.mount_id})
    need(len(identities) == 11 and len(mount_ids) == 1,
         "published v10 exact10 plus official rejection unique on one statx mount")
    require_v10_positive_and_stage_surfaces_absent()
    return _expected_published_then_rejected_v10_proof()


def _expected_published_v11_exact10() -> list[dict[str, Any]]:
    public_names = {
        "v10_official_rejection": "v10_official_rejection",
        "closed_schema_v11": "closed_schema",
        "contract_v11": "contract",
        "build_only_producer_v11": "build_only_producer",
        "independent_consumer_v11": "independent_consumer",
        "transition_v10_to_v11": "v10_to_v11_transition",
        "static_audit_v11": "static_audit",
        "cold_launcher_v11": "cold_launcher",
        "cold_manifest_v11": "cold_manifest",
        "cold_outer_v11": "cold_outer",
    }
    expected: list[dict[str, Any]] = []
    for name in V11_EXACT10_ORDER:
        path, file_sha256 = V11_FROZEN_FILES[name]
        entry: dict[str, Any] = {
            "name": public_names[name],
            "path": str(path.relative_to(ROOT)),
            "file_sha256": file_sha256,
        }
        if name in V11_FROZEN_OBJECTS:
            entry["object_sha256"] = V11_FROZEN_OBJECTS[name]
        expected.append(entry)
    return expected


def validate_v11_common_official_rejection_fields() -> dict[str, Any]:
    return {
        "path": str(V11_OFFICIAL_REJECTION.relative_to(ROOT)),
        "namespace_path": str(V11_OFFICIAL_REJECTION.parent.relative_to(ROOT)),
        "file_sha256": V11_OFFICIAL_REJECTION_FILE_PIN,
        "object_sha256": V11_OFFICIAL_REJECTION_OBJECT_PIN,
        "schema":
            "cm2.round306c79g.true-global-no-producer-consumer.v11.later-rejection",
        "status": "PERMANENT_FAIL_CLOSED_REJECTION__ZERO_CREDIT",
        "reason": "ORPHANED_OR_INCOMPLETE_C79G_V11_SURFACE",
        "namespace_mode": "0555",
        "namespace_nlink": 2,
        "member_mode": "0444",
        "member_nlink": 1,
        "exact_member_universe": ["rejection.json"],
        "formal_global_closure_credit": 0,
        "D02_unlock": False,
        "D02_gate_credit": 0,
        "D02_task_credit": 0,
        "D02_formal_pending_task_count": PENDING_D02,
        "D02_started": False,
        "overwrite_delete_or_reuse_allowed": False,
    }


def _expected_published_then_rejected_v11_proof() -> dict[str, Any]:
    return {
        "ordered_published_exact10": _expected_published_v11_exact10(),
        "official_later_rejection":
            validate_v11_common_official_rejection_fields(),
        "first_runtime_attempt": copy.deepcopy(V11_FIRST_RUNTIME_ATTEMPT),
        "dual_validator_divergence_incident": copy.deepcopy(
            V11_DUAL_VALIDATOR_DIVERGENCE_INCIDENT),
        "positive_and_stage_surfaces_absent": {
            "exact_absent_path_count": len(V11_ALL_POSITIVE_AND_STAGE_SURFACES),
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
        "D02_formal_pending_task_count": PENDING_D02,
        "D02_started": False,
    }


def exact_v11_official_rejection(
        ) -> tuple[dict[str, Any], HeldInheritedFileView]:
    receipt_guard = held_v11_official_rejection()
    need(receipt_guard.path == V11_OFFICIAL_REJECTION and
         sha(receipt_guard.raw) == V11_OFFICIAL_REJECTION_FILE_PIN,
         "exact held v11 official rejection file pin")
    value = strict_json(receipt_guard.raw, "official v11 rejection")
    verify_object(
        value, "official v11 rejection", V11_OFFICIAL_REJECTION_OBJECT_PIN)
    exact_keys = {
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
    }
    expected_pins = {
        "closed_schema_file_sha256": V11_FROZEN_FILES["closed_schema_v11"][1],
        "contract_file_sha256": V11_FROZEN_FILES["contract_v11"][1],
        "contract_object_sha256": V11_FROZEN_OBJECTS["contract_v11"],
        "producer_file_sha256": V11_FROZEN_FILES["build_only_producer_v11"][1],
        "consumer_file_sha256": V11_FROZEN_FILES["independent_consumer_v11"][1],
        "cold_launcher_file_sha256": V11_FROZEN_FILES["cold_launcher_v11"][1],
        "cold_manifest_file_sha256": V11_FROZEN_FILES["cold_manifest_v11"][1],
        "cold_outer_file_sha256": V11_FROZEN_FILES["cold_outer_v11"][1],
        "cold_outer_object_sha256": V11_FROZEN_OBJECTS["cold_outer_v11"],
        "v4_rejection_supersession_file_sha256":
            V4_REJECTION_SUPERSESSION_FILE_PIN,
        "v4_rejection_supersession_object_sha256":
            V4_REJECTION_SUPERSESSION_OBJECT_PIN,
        "v5_official_rejection_file_sha256": V5_OFFICIAL_REJECTION_FILE_PIN,
        "v5_official_rejection_object_sha256": V5_OFFICIAL_REJECTION_OBJECT_PIN,
        "v6_official_rejection_file_sha256": V6_OFFICIAL_REJECTION_FILE_PIN,
        "v6_official_rejection_object_sha256": V6_OFFICIAL_REJECTION_OBJECT_PIN,
        "v7_official_rejection_file_sha256": V7_OFFICIAL_REJECTION_FILE_PIN,
        "v7_official_rejection_object_sha256": V7_OFFICIAL_REJECTION_OBJECT_PIN,
        "v7_publication_lock_continuity_incident_object_sha256":
            V7_PUBLICATION_LOCK_CONTINUITY_INCIDENT["object_sha256"],
        "v8_official_rejection_file_sha256": V8_OFFICIAL_REJECTION_FILE_PIN,
        "v8_official_rejection_object_sha256": V8_OFFICIAL_REJECTION_OBJECT_PIN,
        "v9_official_rejection_file_sha256": V9_OFFICIAL_REJECTION_FILE_PIN,
        "v9_official_rejection_object_sha256": V9_OFFICIAL_REJECTION_OBJECT_PIN,
        "v10_official_rejection_file_sha256": V10_OFFICIAL_REJECTION_FILE_PIN,
        "v10_official_rejection_object_sha256": V10_OFFICIAL_REJECTION_OBJECT_PIN,
    }
    need(set(value) == exact_keys and len(exact_keys) == 52 and
         receipt_guard.raw == canonical(value) + b"\n" and
         value.get("schema") ==
             "cm2.round306c79g.true-global-no-producer-consumer.v11.later-rejection" and
         value.get("status") ==
             "PERMANENT_FAIL_CLOSED_REJECTION__ZERO_CREDIT" and
         value.get("rejection_reason") ==
             "ORPHANED_OR_INCOMPLETE_C79G_V11_SURFACE" and
         value.get("effective_checkpoint_object_sha256") == UPSTREAM_CHECKPOINT_OBJECT_PIN and
         value.get("namespace_exact_path") ==
             str(V11_OFFICIAL_REJECTION.parent.relative_to(ROOT)) and
         value.get("target_exact_path") ==
             str(V11_OFFICIAL_REJECTION.relative_to(ROOT)) and
         value.get("namespace_at_rest_mode") == "0555" and
         value.get("namespace_lock_held_write_window_mode") == "0755" and
         value.get("rejection_file_mode") == "0444" and
         value.get("rejection_file_nlink") == 1 and
         all(value.get(key) == expected
             for key, expected in expected_pins.items()) and
         value.get("formal_global_closure_credit") == 0 and
         value.get("D02_unlock") is False and
         value.get("D02_gate_credit") == 0 and
         value.get("D02_task_credit") == 0 and
         value.get("D02_formal_pending_task_count") == PENDING_D02 and
         value.get("D02_started") is False and
         value.get("standalone_authority") is False and
         value.get("overwrite_delete_or_reuse_allowed") is False,
         "v11 official rejection canonical singleton zero-credit envelope")
    return value, receipt_guard


def validate_v11_published_then_rejected_predecessor(
        v11_guard: HeldInputSet,
        v11_source_metadata: list[HeldOpaqueMetadata]) -> dict[str, Any]:
    _, rejection_guard = exact_v11_official_rejection()
    source_names = {
        "build_only_producer_v11", "independent_consumer_v11",
        "cold_launcher_v11"}
    readable_by_path = {item.path: item for item in v11_guard.files}
    source_by_path = {item.path: item for item in v11_source_metadata}
    need(set(readable_by_path) == {
             path for name, (path, _) in V11_FROZEN_FILES.items()
             if name not in source_names} and
         set(source_by_path) == {
             path for name, (path, _) in V11_FROZEN_FILES.items()
             if name in source_names},
         "published v11 exact10 exact7-readable/exact3-metadata partition")
    for name, (path, file_pin) in V11_FROZEN_FILES.items():
        if name in source_names:
            metadata = source_by_path[path]
            need(stat.S_ISREG(metadata.before.st_mode) and
                 stat.S_IMODE(metadata.before.st_mode) == 0o444 and
                 metadata.before.st_nlink == 1,
                 "published v11 strict O_PATH metadata source:" + name)
            continue
        held = readable_by_path[path]
        need(sha(held.raw) == file_pin,
             "published v11 readable member pin:" + name)
        if name in V11_FROZEN_OBJECTS:
            parsed = strict_json(held.raw, "published v11 object:" + name)
            verify_object(parsed, "published v11 object:" + name,
                          V11_FROZEN_OBJECTS[name])
    exact8_expected = [
        {"file_sha256": V11_FROZEN_FILES[name][1],
         "entry_name": str(V11_FROZEN_FILES[name][0].relative_to(ROOT))}
        for name in V11_EXACT10_ORDER[:8]
    ]
    manifest_guard = readable_by_path[V11_FROZEN_FILES["cold_manifest_v11"][0]]
    outer_guard = readable_by_path[V11_FROZEN_FILES["cold_outer_v11"][0]]
    manifest = parse_manifest_ordered(
        manifest_guard.raw, "published v11 exact8 manifest")
    outer = strict_json(outer_guard.raw, "published v11 outer-last")
    verify_object(outer, "published v11 outer-last",
                  V11_FROZEN_OBJECTS["cold_outer_v11"])
    exact8_stats = []
    for name in V11_EXACT10_ORDER[:8]:
        path = V11_FROZEN_FILES[name][0]
        exact8_stats.append((source_by_path[path] if name in source_names
                             else readable_by_path[path]).before)
    chronology = cold_publication_chronology(
        exact8_stats, manifest_guard.before, outer_guard.before)
    need(manifest == exact8_expected and
         outer.get("exact8_ordered_entries") == [
             {"path": item["entry_name"], "file_sha256": item["file_sha256"]}
             for item in exact8_expected] and
         outer.get("status") ==
             "FROZEN_COLD_LAUNCH_OUTER_LAST__EXACT8_MANIFEST_CLOSED__RUNTIME_DEFERRED" and
         outer.get("formal_global_closure_credit") == 0 and
         outer.get("D02_unlock") is False and
         outer.get("runtime_executed_during_static_freeze") is False and
         all(chronology.values()) and
         max(outer_guard.before.st_mtime_ns, outer_guard.before.st_ctime_ns) <
             min(rejection_guard.before.st_mtime_ns,
                 rejection_guard.before.st_ctime_ns),
         "published v11 exact10 manifest/outer/official-rejection chronology")
    identities = ({item.identity for item in v11_guard.files} |
                  {item.identity for item in v11_source_metadata} |
                  {rejection_guard.identity})
    mount_ids = ({item.mount_id for item in v11_guard.files} |
                 {item.mount_id for item in v11_source_metadata} |
                 {rejection_guard.mount_id})
    need(len(identities) == 11 and len(mount_ids) == 1,
         "published v11 exact10 plus official rejection unique on one statx mount")
    require_v11_positive_and_stage_surfaces_absent()
    proof = _expected_published_then_rejected_v11_proof()
    need(len(proof) == 19 and digest(proof) ==
             V11_PUBLISHED_THEN_REJECTED_PROOF_SHA256,
         "published v11 exact19 canonical proof digest")
    return proof


def _expected_published_v12_exact10() -> list[dict[str, Any]]:
    public_names = {
        "v11_official_rejection": "v11_official_rejection",
        "closed_schema_v12": "closed_schema",
        "contract_v12": "contract",
        "build_only_producer_v12": "build_only_producer",
        "independent_consumer_v12": "independent_consumer",
        "transition_v11_to_v12": "v11_to_v12_transition",
        "static_audit_v12": "static_audit",
        "cold_launcher_v12": "cold_launcher",
        "cold_manifest_v12": "cold_manifest",
        "cold_outer_v12": "cold_outer",
    }
    expected: list[dict[str, Any]] = []
    for name in V12_EXACT10_ORDER:
        path, file_sha256 = V12_FROZEN_FILES[name]
        entry: dict[str, Any] = {
            "name": public_names[name],
            "path": str(path.relative_to(ROOT)),
            "file_sha256": file_sha256,
        }
        if name in V12_FROZEN_OBJECTS:
            entry["object_sha256"] = V12_FROZEN_OBJECTS[name]
        expected.append(entry)
    return expected


def validate_v12_common_official_rejection_fields() -> dict[str, Any]:
    return {
        "path": str(V12_OFFICIAL_REJECTION.relative_to(ROOT)),
        "namespace_path": str(V12_OFFICIAL_REJECTION.parent.relative_to(ROOT)),
        "file_sha256": V12_OFFICIAL_REJECTION_FILE_PIN,
        "object_sha256": V12_OFFICIAL_REJECTION_OBJECT_PIN,
        "schema":
            "cm2.round306c79g.true-global-no-producer-consumer.v12.later-rejection",
        "status": "PERMANENT_FAIL_CLOSED_REJECTION__ZERO_CREDIT",
        "reason": "ORPHANED_OR_INCOMPLETE_C79G_V12_SURFACE",
        "namespace_mode": "0555",
        "namespace_nlink": 2,
        "member_mode": "0444",
        "member_nlink": 1,
        "exact_member_universe": ["rejection.json"],
        "formal_global_closure_credit": 0,
        "D02_unlock": False,
        "D02_gate_credit": 0,
        "D02_task_credit": 0,
        "D02_formal_pending_task_count": PENDING_D02,
        "D02_started": False,
        "overwrite_delete_or_reuse_allowed": False,
    }


def _expected_published_then_rejected_v12_proof() -> dict[str, Any]:
    return {
        "ordered_published_exact10": _expected_published_v12_exact10(),
        "official_later_rejection":
            validate_v12_common_official_rejection_fields(),
        "first_runtime_attempt": copy.deepcopy(V12_FIRST_RUNTIME_ATTEMPT),
        "v5_rejection_shape_incident": copy.deepcopy(
            V12_V5_REJECTION_SHAPE_INCIDENT),
        "positive_and_stage_surfaces_absent": {
            "exact_absent_path_count": len(V12_ALL_POSITIVE_AND_STAGE_SURFACES),
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
        "D02_formal_pending_task_count": PENDING_D02,
        "D02_started": False,
    }


def exact_v12_official_rejection(
        ) -> tuple[dict[str, Any], HeldInheritedFileView]:
    receipt_guard = held_v12_official_rejection()
    need(receipt_guard.path == V12_OFFICIAL_REJECTION and
         sha(receipt_guard.raw) == V12_OFFICIAL_REJECTION_FILE_PIN,
         "exact current-policy held v12 official rejection file pin")
    value = strict_json(receipt_guard.raw, "official v12 rejection")
    verify_object(
        value, "official v12 rejection", V12_OFFICIAL_REJECTION_OBJECT_PIN)
    expected_pins = {
        "closed_schema_file_sha256": V12_FROZEN_FILES["closed_schema_v12"][1],
        "contract_file_sha256": V12_FROZEN_FILES["contract_v12"][1],
        "contract_object_sha256": V12_FROZEN_OBJECTS["contract_v12"],
        "producer_file_sha256": V12_FROZEN_FILES["build_only_producer_v12"][1],
        "consumer_file_sha256": V12_FROZEN_FILES["independent_consumer_v12"][1],
        "cold_launcher_file_sha256": V12_FROZEN_FILES["cold_launcher_v12"][1],
        "cold_manifest_file_sha256": V12_FROZEN_FILES["cold_manifest_v12"][1],
        "cold_outer_file_sha256": V12_FROZEN_FILES["cold_outer_v12"][1],
        "cold_outer_object_sha256": V12_FROZEN_OBJECTS["cold_outer_v12"],
        "v4_rejection_supersession_file_sha256":
            V4_REJECTION_SUPERSESSION_FILE_PIN,
        "v4_rejection_supersession_object_sha256":
            V4_REJECTION_SUPERSESSION_OBJECT_PIN,
        "v5_official_rejection_file_sha256": V5_OFFICIAL_REJECTION_FILE_PIN,
        "v5_official_rejection_object_sha256": V5_OFFICIAL_REJECTION_OBJECT_PIN,
        "v6_official_rejection_file_sha256": V6_OFFICIAL_REJECTION_FILE_PIN,
        "v6_official_rejection_object_sha256": V6_OFFICIAL_REJECTION_OBJECT_PIN,
        "v7_official_rejection_file_sha256": V7_OFFICIAL_REJECTION_FILE_PIN,
        "v7_official_rejection_object_sha256": V7_OFFICIAL_REJECTION_OBJECT_PIN,
        "v7_publication_lock_continuity_incident_object_sha256":
            V7_PUBLICATION_LOCK_CONTINUITY_INCIDENT["object_sha256"],
        "v8_official_rejection_file_sha256": V8_OFFICIAL_REJECTION_FILE_PIN,
        "v8_official_rejection_object_sha256": V8_OFFICIAL_REJECTION_OBJECT_PIN,
        "v9_official_rejection_file_sha256": V9_OFFICIAL_REJECTION_FILE_PIN,
        "v9_official_rejection_object_sha256": V9_OFFICIAL_REJECTION_OBJECT_PIN,
        "v10_official_rejection_file_sha256": V10_OFFICIAL_REJECTION_FILE_PIN,
        "v10_official_rejection_object_sha256": V10_OFFICIAL_REJECTION_OBJECT_PIN,
        "v11_official_rejection_file_sha256": V11_OFFICIAL_REJECTION_FILE_PIN,
        "v11_official_rejection_object_sha256": V11_OFFICIAL_REJECTION_OBJECT_PIN,
    }
    need(set(value) == V12_OFFICIAL_REJECTION_EXACT54_KEYS and
         len(value) == len(V12_OFFICIAL_REJECTION_EXACT54_KEYS) == 54 and
         sha_bytes(canonical(sorted(value))) ==
             V12_OFFICIAL_REJECTION_EXACT54_KEYSET_SHA256 and
         receipt_guard.raw == canonical(value) + b"\n" and
         value.get("schema") ==
             "cm2.round306c79g.true-global-no-producer-consumer.v12.later-rejection" and
         value.get("status") ==
             "PERMANENT_FAIL_CLOSED_REJECTION__ZERO_CREDIT" and
         value.get("rejection_reason") ==
             "ORPHANED_OR_INCOMPLETE_C79G_V12_SURFACE" and
         value.get("effective_checkpoint_object_sha256") ==
             UPSTREAM_CHECKPOINT_OBJECT_PIN and
         value.get("namespace_exact_path") ==
             str(V12_OFFICIAL_REJECTION.parent.relative_to(ROOT)) and
         value.get("target_exact_path") ==
             str(V12_OFFICIAL_REJECTION.relative_to(ROOT)) and
         value.get("namespace_at_rest_mode") == "0555" and
         value.get("namespace_lock_held_write_window_mode") == "0755" and
         value.get("rejection_file_mode") == "0444" and
         value.get("rejection_file_nlink") == 1 and
         all(value.get(key) == expected
             for key, expected in expected_pins.items()) and
         value.get("formal_global_closure_credit") == 0 and
         value.get("D02_unlock") is False and
         value.get("D02_gate_credit") == 0 and
         value.get("D02_task_credit") == 0 and
         value.get("D02_formal_pending_task_count") == PENDING_D02 and
         value.get("D02_started") is False and
         value.get("standalone_authority") is False and
         value.get("overwrite_delete_or_reuse_allowed") is False,
         "v12 official rejection canonical exact54 singleton zero-credit envelope")
    return value, receipt_guard


def validate_v12_published_then_rejected_predecessor() -> dict[str, Any]:
    need(isinstance(_INCIDENT_AUTHORITY_HOLD,
                    HeldInheritedV14AuthorityExact12),
         "v12 predecessor exact10 remains held from inherited launch authority")
    hold = _INCIDENT_AUTHORITY_HOLD
    _, rejection_guard = exact_v12_official_rejection()
    need(set(hold.v12_raw_by_path) == {
             path for path, _ in V12_FROZEN_FILES.values()} and
         set(hold.v12_stat_by_path) == set(hold.v12_raw_by_path) and
         set(hold.v12_identity_by_path) == set(hold.v12_raw_by_path) and
         set(hold.v12_mount_by_path) == set(hold.v12_raw_by_path),
         "published v12 exact10 held raw/stat/identity/mount views close")
    for name, (path, file_pin) in V12_FROZEN_FILES.items():
        raw = hold.v12_raw_by_path[path]
        before = hold.v12_stat_by_path[path]
        need(sha(raw) == file_pin and stat.S_ISREG(before.st_mode) and
             stat.S_IMODE(before.st_mode) == 0o444 and before.st_nlink == 1,
             "published v12 exact10 held member pin/mode/nlink:" + name)
        if name in V12_FROZEN_OBJECTS:
            parsed = strict_json(raw, "published v12 object:" + name)
            verify_object(parsed, "published v12 object:" + name,
                          V12_FROZEN_OBJECTS[name])
    exact8_expected = [
        {"file_sha256": V12_FROZEN_FILES[name][1],
         "entry_name": str(V12_FROZEN_FILES[name][0].relative_to(ROOT))}
        for name in V12_EXACT10_ORDER[:8]
    ]
    manifest_path = V12_FROZEN_FILES["cold_manifest_v12"][0]
    outer_path = V12_FROZEN_FILES["cold_outer_v12"][0]
    manifest = parse_manifest_ordered(
        hold.v12_raw_by_path[manifest_path], "published v12 exact8 manifest")
    outer = strict_json(
        hold.v12_raw_by_path[outer_path], "published v12 outer-last")
    verify_object(outer, "published v12 outer-last",
                  V12_FROZEN_OBJECTS["cold_outer_v12"])
    chronology = cold_publication_chronology(
        [hold.v12_stat_by_path[V12_FROZEN_FILES[name][0]]
         for name in V12_EXACT10_ORDER[:8]],
        hold.v12_stat_by_path[manifest_path], hold.v12_stat_by_path[outer_path])
    need(manifest == exact8_expected and
         outer.get("exact8_ordered_entries") == [
             {"path": item["entry_name"], "file_sha256": item["file_sha256"]}
             for item in exact8_expected] and
         outer.get("status") ==
             "FROZEN_COLD_LAUNCH_OUTER_LAST__EXACT8_MANIFEST_CLOSED__RUNTIME_DEFERRED" and
         outer.get("formal_global_closure_credit") == 0 and
         outer.get("D02_unlock") is False and
         outer.get("runtime_executed_during_static_freeze") is False and
         all(chronology.values()) and
         max(hold.v12_stat_by_path[outer_path].st_mtime_ns,
             hold.v12_stat_by_path[outer_path].st_ctime_ns) <
             min(rejection_guard.before.st_mtime_ns,
                 rejection_guard.before.st_ctime_ns),
         "published v12 exact10 manifest/outer/official-rejection chronology")
    identities = hold.v12_exact10_identities() | {rejection_guard.identity}
    mount_ids = hold.v12_exact10_mount_ids() | {rejection_guard.mount_id}
    need(len(identities) == 11 and len(mount_ids) == 1,
         "published v12 exact10 plus current-policy rejection unique on one mount")
    require_v12_positive_and_stage_surfaces_absent()
    proof = _expected_published_then_rejected_v12_proof()
    need(len(proof) == 19 and
         proof["v5_rejection_shape_incident"] ==
             V12_V5_REJECTION_SHAPE_INCIDENT and
         sha_bytes(canonical(proof["v5_rejection_shape_incident"])) ==
             V12_V5_REJECTION_SHAPE_INCIDENT_SHA256,
         "published v12 exact19 proof and incident canonical closure")
    return proof


def exact_v3_rejection(
        receipt_guard: HeldPinnedInput,
        v3_guard: HeldInputSet,
        v3_source_metadata: list[HeldOpaqueMetadata]) -> dict[str, Any]:
    need(receipt_guard.path == V3_OFFICIAL_REJECTION and
         sha(receipt_guard.raw) == V3_OFFICIAL_REJECTION_FILE_PIN,
         "exact full-run held official v3 later rejection")
    value = strict_json(receipt_guard.raw, "official v3 later rejection")
    verify_object(value, "official v3 later rejection", V3_OFFICIAL_REJECTION_OBJECT_PIN)
    need(value.get("schema") ==
             "cm2.round306c79g.true-global-no-producer-consumer.v3.later-rejection" and
         value.get("status") == "PERMANENT_FAIL_CLOSED_REJECTION__ZERO_CREDIT" and
         value.get("rejection_reason") ==
             "ORPHANED_OR_INCOMPLETE_C79G_V3_SURFACE" and
         value.get("effective_checkpoint_object_sha256") == UPSTREAM_CHECKPOINT_OBJECT_PIN and
         value.get("target_exact_path") == str(V3_OFFICIAL_REJECTION.relative_to(ROOT)) and
         value.get("namespace_exact_path") ==
             str(V3_OFFICIAL_REJECTION.parent.relative_to(ROOT)) and
         value.get("formal_global_closure_credit") == 0 and
         value.get("D02_unlock") is False and value.get("D02_started") is False and
         value.get("standalone_authority") is False and
         value.get("overwrite_delete_or_reuse_allowed") is False and
         value.get("cold_launcher_file_sha256") ==
             V3_FROZEN_FILES["cold_launcher"][1] and
         value.get("cold_manifest_file_sha256") ==
             V3_FROZEN_FILES["cold_manifest"][1] and
         value.get("cold_outer_file_sha256") ==
             V3_FROZEN_FILES["cold_outer"][1] and
         value.get("cold_outer_object_sha256") ==
             V3_FROZEN_OBJECTS["cold_outer"],
         "official v3 permanent rejection and exact frozen-cold binding")
    by_path = {item.path: item for item in v3_guard.files}
    source_by_path = {item.path: item for item in v3_source_metadata}
    source_names = {"build_only_producer", "independent_consumer", "cold_launcher"}
    need(set(by_path) == {
             path for name, (path, _) in V3_FROZEN_FILES.items()
             if name not in source_names} | {V3_OFFICIAL_REJECTION} and
         set(source_by_path) == {
             path for name, (path, _) in V3_FROZEN_FILES.items()
             if name in source_names},
         "frozen v3 exact10 partition plus separate official-rejection readable fd")
    for name, (path, file_pin) in V3_FROZEN_FILES.items():
        if name in source_names:
            source_info = source_by_path[path].before
            need(stat.S_ISREG(source_info.st_mode) and
                 stat.S_IMODE(source_info.st_mode) == 0o444 and
                 source_info.st_nlink == 1,
                 "frozen v3 O_PATH source metadata exact mode/nlink:" + name)
            continue
        raw_member = by_path[path].raw
        need(sha(raw_member) == file_pin, "frozen v3 exact member pin:" + name)
        if name in V3_FROZEN_OBJECTS:
            member_value = strict_json(raw_member, "frozen v3 object:" + name)
            verify_object(member_value, "frozen v3 object:" + name,
                          V3_FROZEN_OBJECTS[name])
    manifest_guard = by_path[V3_FROZEN_FILES["cold_manifest"][0]]
    manifest_entries = parse_manifest_ordered(
        manifest_guard.raw, "frozen v3 exact8 ordered manifest")
    expected_exact8 = [
        {"file_sha256": V3_FROZEN_FILES[name][1],
         "entry_name": str(V3_FROZEN_FILES[name][0].relative_to(ROOT))}
        for name in V3_EXACT10_ORDER[:8]
    ]
    need(manifest_entries == expected_exact8,
         "frozen v3 exact8 manifest order and pins")
    outer_guard = by_path[V3_FROZEN_FILES["cold_outer"][0]]
    outer = strict_json(outer_guard.raw, "frozen v3 cold outer")
    verify_object(outer, "frozen v3 cold outer", V3_FROZEN_OBJECTS["cold_outer"])
    need(outer.get("status") ==
             "FROZEN_COLD_LAUNCH_OUTER_LAST__EXACT8_MANIFEST_CLOSED__RUNTIME_DEFERRED" and
         outer.get("effective_checkpoint_object_sha256") == UPSTREAM_CHECKPOINT_OBJECT_PIN and
         outer.get("formal_global_closure_credit") == 0 and
         outer.get("D02_unlock") is False and
         outer.get("cold_launch_manifest", {}).get("file_sha256") ==
             V3_FROZEN_FILES["cold_manifest"][1] and
         outer.get("cold_launcher", {}).get("file_sha256") ==
             V3_FROZEN_FILES["cold_launcher"][1] and
         outer.get("exact8_ordered_entries") == [
             {"file_sha256": entry["file_sha256"], "path": entry["entry_name"]}
             for entry in expected_exact8] and
         max(outer_guard.before.st_mtime_ns, outer_guard.before.st_ctime_ns) <
             min(receipt_guard.before.st_mtime_ns,
                 receipt_guard.before.st_ctime_ns),
         "frozen v3 outer closure and strictly later official rejection")
    return {
        "official_v3_rejection": value,
        "predecessor_exact10_ordered": [
            {"path": str(V3_FROZEN_FILES[name][0].relative_to(ROOT)),
             "file_sha256": V3_FROZEN_FILES[name][1]}
            for name in V3_EXACT10_ORDER],
        "producer_source_content_opened_by_independent_consumer": False,
        "live_identity_values_persisted": False,
    }


def _line_sequence_sha256(values: Iterable[str]) -> str:
    return sha(b"".join((value + "\n").encode("ascii") for value in values))


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
        anchor_cells = [row for row in grouped if row.get("known_sheet_anchor_role") ==
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


def validate_c42_c53_kraft(
        cell_rows: list[dict[str, Any]],
        c42_guard: HeldInputSet) -> dict[str, Any]:
    """Direct itemwise C42 authority -> C53 audit -> C55B crosswalk join."""
    by_path = {item.path: item for item in c42_guard.files}
    by_directory = {item.path: item for item in c42_guard.directories}
    c42_candidate_universe = C42_CANDIDATE_MANIFEST_MEMBERS | {"root_manifest.sha256"}
    full10_paths = set(C42_C53_PATHS.values())
    candidate9_paths = {
        C42_CANDIDATE_DIR / name for name in c42_candidate_universe}
    need(len(full10_paths) == 10 and len(candidate9_paths) == 9 and
         len(full10_paths | candidate9_paths) == 16 and
         set(by_path) == full10_paths | candidate9_paths and
         set(by_directory) == {
             C42_CANDIDATE_DIR,
             C42_INDEPENDENT_AUDIT_DIR,
             C42_INSTALLATION_RECEIPT_DIR,
         } and
         by_directory[C42_CANDIDATE_DIR].names == c42_candidate_universe and
         by_directory[C42_INDEPENDENT_AUDIT_DIR].names ==
             {C42_INDEPENDENT_AUDIT_PATH.name} and
         by_directory[C42_INSTALLATION_RECEIPT_DIR].names ==
             {C42_INSTALLATION_RECEIPT_PATH.name},
         "C42 Kraft:full10 union candidate9 exact held-fd universe")
    c42_parent_raw = by_path[C42_PARENT_PATH].raw
    need(sha(c42_parent_raw) == C42_C53_PINS["C42_parent"],
         "C42 Kraft:held parent-conservation file pin")
    c42_rows = gzip_rows(c42_parent_raw, "C42 installed parent conservation")
    need(len(c42_rows) == PAIR_COUNT, "C42 Kraft:exact 862 rows")
    c42 = one_index(c42_rows, "pair_index", "C42 Kraft")
    need(set(c42) == set(range(PAIR_COUNT)), "C42 Kraft:dense pair index")
    for pair_index in range(PAIR_COUNT):
        row = c42[pair_index]
        need(row.get("parent_Kraft_conservation") == "1" and
             row.get("D02_gate_credit") == 0 and
             row.get("terminal_reflection_transport_materialized") is True,
             "C42 Kraft:itemwise exact conservation independent of terminal route")
    c42_sequence = [c42[index]["row_sha256"] for index in range(PAIR_COUNT)]
    need(_line_sequence_sha256(c42_sequence) == C55B_C42_PAIR_INDEX_SEQUENCE_PIN,
         "C42 Kraft:row-hash sequence")

    result_raw = by_path[C42_RESULT_PATH].raw
    need(sha(result_raw) == C42_C53_PINS["C42_result"],
         "C42 Kraft:held result file pin")
    result = strict_json(result_raw, "C42 result")
    verify_object(result, "C42 result", C42_RESULT_OBJECT_PIN)
    need(result.get("closure_census", {}).get("parent_conservation_row_count") == PAIR_COUNT and
         result.get("formal_authority") is False and
         result.get("producer_output_is_authority") is False,
         "C42 Kraft:producer nonauthority boundary")
    c42_manifest_raw = by_path[C42_MANIFEST_PATH].raw
    need(sha(c42_manifest_raw) == C42_C53_PINS["C42_manifest"],
         "C42 Kraft:held root-manifest file pin")
    manifest = parse_manifest(c42_manifest_raw, "C42 root manifest")
    need(len(manifest) == 8 and set(manifest) == C42_CANDIDATE_MANIFEST_MEMBERS and
         manifest["parent_conservation.jsonl.gz"] == C42_C53_PINS["C42_parent"] and
         manifest["result.json"] == C42_C53_PINS["C42_result"],
         "C42 Kraft:exact root manifest")
    c42_candidate_member_raw: dict[str, bytes] = {}
    for name in manifest:
        raw = by_path[C42_CANDIDATE_DIR / name].raw
        need(sha(raw) == manifest[name], "C42 Kraft:manifest member replay:" + name)
        c42_candidate_member_raw[name] = raw
    need(set(c42_candidate_member_raw) == C42_CANDIDATE_MANIFEST_MEMBERS,
         "C42 Kraft:all exact8 manifest members replayed")

    c42_candidate_token_raw = by_path[C42_CANDIDATE_TOKEN_PATH].raw
    c42_audit_token_raw = by_path[C42_AUDIT_TOKEN_PATH].raw
    need(sha(c42_candidate_token_raw) == C42_C53_PINS["C42_candidate_token"] and
         sha(c42_audit_token_raw) == C42_C53_PINS["C42_audit_token"],
         "C42 Kraft:held candidate/audit token pins")
    need(c42_candidate_token_raw == (C42_CANDIDATE_TOKEN + "\n").encode("ascii") and
         c42_audit_token_raw == (C42_AUDIT_TOKEN + "\n").encode("ascii"),
         "C42 Kraft:exact installed candidate/audit token bytes")
    c42_audit_raw = by_path[C42_INDEPENDENT_AUDIT_PATH].raw
    need(sha(c42_audit_raw) == C42_C53_PINS["C42_independent_audit"],
         "C42 Kraft:held independent-audit file pin")
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

    c42_installation_raw = by_path[C42_INSTALLATION_RECEIPT_PATH].raw
    need(sha(c42_installation_raw) == C42_C53_PINS["C42_installation_receipt"],
         "C42 Kraft:held installation-receipt file pin")
    c42_installation = strict_json(
        c42_installation_raw, "C42 installation receipt")
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
    c42_seal_raw = by_path[C42_SEAL_PATH].raw
    need(sha(c42_seal_raw) == C42_C53_PINS["C42_seal"],
         "C42 Kraft:held authority-seal file pin")
    seal = strict_json(c42_seal_raw, "C42 seal")
    seal_body = copy.deepcopy(seal)
    seal_claim = seal_body.pop("authority_seal_object_sha256", None)
    need(set(seal) == {
             "audit_pointer_sha256", "audit_token", "authority_seal_object_sha256",
             "candidate_object_sha256", "candidate_pointer_sha256", "candidate_token",
             "formal_census_after_commit", "independent_audit_object_sha256",
             "installer_source_sha256", "receipt_file_sha256", "receipt_object_sha256",
             "receipt_path", "release_id", "schema", "semantic_commit", "status"} and
         seal_claim == C42_SEAL_OBJECT_PIN and seal_claim == digest(seal_body) and
         seal.get("candidate_object_sha256") == C42_RESULT_OBJECT_PIN and
         seal.get("candidate_token") == C42_CANDIDATE_TOKEN and
         seal.get("candidate_pointer_sha256") == C42_C53_PINS["C42_candidate_token"] and
         seal.get("audit_token") == C42_AUDIT_TOKEN and
         seal.get("audit_pointer_sha256") == C42_C53_PINS["C42_audit_token"] and
         seal.get("independent_audit_object_sha256") == C42_INDEPENDENT_AUDIT_OBJECT_PIN and
         seal.get("receipt_path") == C42_INSTALLATION_RECEIPT_REL and
         seal.get("receipt_file_sha256") == C42_C53_PINS["C42_installation_receipt"] and
         seal.get("receipt_object_sha256") == C42_INSTALLATION_RECEIPT_OBJECT_PIN and
         seal.get("release_id") == C42_INSTALLATION_RELEASE and
         seal.get("semantic_commit", {}).get("this_seal_is_required") is True and
         seal.get("semantic_commit", {}).get(
             "compatibility_pointers_without_this_seal_are_not_authority") is True and
         str(seal.get("status", "")).startswith("COMMITTED_C42"),
         "C42 Kraft:full installed authority seal/audit/receipt/token closure")

    c53_audit_raw = by_path[C53_AUDIT_PATH].raw
    need(sha(c53_audit_raw) == C42_C53_PINS["C53_audit"],
         "C53 Kraft:held audit file pin")
    audit = strict_json(c53_audit_raw, "C53 audit")
    verify_object(audit, "C53 audit", C53_AUDIT_OBJECT_PIN)
    derivation = audit.get("post_seal_promotion_derivation")
    need(isinstance(derivation, dict), "C53 Kraft:derivation")
    derivation_body = copy.deepcopy(derivation)
    derivation_claim = derivation_body.pop("promotion_derivation_object_sha256", None)
    need(isinstance(derivation_claim, str) and derivation_claim == digest(derivation_body) and
         derivation.get("parent_projection_count") == PAIR_COUNT and
         derivation.get("C42_formal_authority_seal_object_sha256") == C42_SEAL_OBJECT_PIN and
         derivation.get("D02_gate_credit") == 0,
         "C53 Kraft:derivation closure")
    projections = derivation.get("parent_projections")
    need(isinstance(projections, list) and len(projections) == PAIR_COUNT,
         "C53 Kraft:exact 862 projections")
    c53 = one_index(projections, "pair_index", "C53 Kraft")
    need(set(c53) == set(range(PAIR_COUNT)), "C53 Kraft:dense pair index")
    c53_sequence: list[str] = []
    for pair_index in range(PAIR_COUNT):
        projection = c53[pair_index]
        body = copy.deepcopy(projection)
        claim = body.pop("projection_object_sha256", None)
        need(isinstance(claim, str) and claim == digest(body) and
             projection.get("C42_parent_row_sha256") == c42[pair_index]["row_sha256"] and
             projection.get("D02_gate_credit") == 0,
             "C53 Kraft:itemwise projection")
        c53_sequence.append(claim)
    need(_line_sequence_sha256(c53_sequence) == C55B_C53_PAIR_INDEX_SEQUENCE_PIN and
         derivation.get("post_seal_862_parent_projection_sequence_sha256") ==
             C55B_C53_PAIR_INDEX_SEQUENCE_PIN,
         "C53 Kraft:projection sequence")
    c53_head_raw = by_path[C53_HEAD_PATH].raw
    need(sha(c53_head_raw) == C42_C53_PINS["C53_head"],
         "C53 Kraft:held head file pin")
    head = strict_json(c53_head_raw, "C53 head")
    head_body = copy.deepcopy(head)
    head_claim = head_body.pop("authority_seal_object_sha256", None)
    need(head_claim == C53_HEAD_OBJECT_PIN and head_claim == digest(head_body) and
         head.get("independent_audit_object_sha256") == C53_AUDIT_OBJECT_PIN and
         head.get("post_seal_effective_checkpoint_object_sha256") == UPSTREAM_CHECKPOINT_OBJECT_PIN and
         head.get("formal_scope", {}).get("D02_gate_credit") == 0 and
         head.get("semantic_commit", {}).get("this_predecessor_keyed_global_head_is_only_semantic_commit") is True,
         "C53 Kraft:installed global head closure")

    crosswalk: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for row in cell_rows:
        crosswalk[row["pair_index"]].append(row)
    need(set(crosswalk) == set(range(PAIR_COUNT)) and
         all(len(rows) == 2 for rows in crosswalk.values()), "Kraft:C55B exact crosswalk")
    for pair_index in range(PAIR_COUNT):
        need({row["C42_parent_row_sha256"] for row in crosswalk[pair_index]} ==
                 {c42[pair_index]["row_sha256"]} and
             {row["C53_parent_projection_object_sha256"] for row in crosswalk[pair_index]} ==
                 {c53[pair_index]["projection_object_sha256"]},
             "Kraft:C42-C53-C55B itemwise hash join")
    need(by_directory[C42_CANDIDATE_DIR].names == c42_candidate_universe and
         by_path[C42_MANIFEST_PATH].raw == c42_manifest_raw and
         all(by_path[C42_CANDIDATE_DIR / name].raw ==
             c42_candidate_member_raw[name]
             for name in C42_CANDIDATE_MANIFEST_MEMBERS),
         "C42 Kraft:all semantics derived from the full-run held fd set")
    return {
        "pair_count": PAIR_COUNT,
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
        "C42_held_directory_count": 3,
        "C42_candidate_directory_expected_mode": "0755",
        "C42_candidate_directory_expected_nlink": 2,
        "C42_independent_audit_directory_expected_mode": "0700",
        "C42_independent_audit_directory_expected_nlink": 2,
        "C42_installation_receipt_directory_expected_mode": "0500",
        "C42_installation_receipt_directory_expected_nlink": 2,
        "C42_auxiliary_directory_exact_member_count_each": 1,
        "historical_directory_modes_are_exact_observed_snapshot_guards_not_immutability_claims": True,
        "all_862_exact_parent_Kraft_one": True,
        "all_D02_gate_credit_zero": True,
        "C42_rows_by_pair": c42,
        "C53_projections_by_pair": c53,
    }


def one_index(rows: Iterable[dict[str, Any]], key: str, label: str) -> dict[Any, dict[str, Any]]:
    out: dict[Any, dict[str, Any]] = {}
    for row in rows:
        value = row.get(key)
        need(value not in out, label + ":duplicate")
        out[value] = row
    return out


def hold_c78_upstream_surfaces() -> HeldInputSet:
    files: list[HeldPinnedInput] = []
    directories: list[HeldDirectory] = []
    for directory in (C78L_A, C78L_B):
        directories.append(HeldDirectory(
            directory, set(C78L_NAMES.values()),
            C78L_HISTORICAL_DIRECTORY_EXPECTED_MODE, 2,
            "C78l historical exact10 held surface"))
        for key, name in C78L_NAMES.items():
            files.append(HeldPinnedInput(
                directory / name, "C78l held:" + key,
                C78_HISTORICAL_MEMBER_EXPECTED_MODE, C78L_PINS[key]))
    files.extend([
        HeldPinnedInput(C78L_VERIFY_A, "C78l held verification A",
                        C78_HISTORICAL_MEMBER_EXPECTED_MODE, C78L_VERIFY_FILE),
        HeldPinnedInput(C78L_VERIFY_B, "C78l held verification B",
                        C78_HISTORICAL_MEMBER_EXPECTED_MODE, C78L_VERIFY_FILE),
    ])
    directories.append(HeldDirectory(
        C78L_COMPLETION, set(C78L_COMPLETION_NAMES.values()),
        C78L_HISTORICAL_DIRECTORY_EXPECTED_MODE, 2,
        "C78l historical exact3 completion held surface"))
    for key, name in C78L_COMPLETION_NAMES.items():
        files.append(HeldPinnedInput(
            C78L_COMPLETION / name, "C78l held completion:" + key,
            C78_HISTORICAL_MEMBER_EXPECTED_MODE,
            C78L_COMPLETION_PINS[key]))

    c78s_a = rooted(str(C78S_FINAL["build_A_directory"]))
    c78s_b = rooted(str(C78S_FINAL["build_B_directory"]))
    sva_path = rooted(str(C78S_FINAL["verification_A_path"]))
    svb_path = rooted(str(C78S_FINAL["verification_B_path"]))
    fma_path = rooted(str(C78S_FINAL["final_manifest_A_path"]))
    fmb_path = rooted(str(C78S_FINAL["final_manifest_B_path"]))
    foa_path = rooted(str(C78S_FINAL["final_outer_A_path"]))
    fob_path = rooted(str(C78S_FINAL["final_outer_B_path"]))
    exact13 = set(C78S_NAMES.values()) | {sva_path.name, fma_path.name, foa_path.name}
    for directory in (c78s_a, c78s_b):
        directories.append(HeldDirectory(
            directory, exact13, C78S_HISTORICAL_DIRECTORY_EXPECTED_MODE, 2,
            "C78s exact13 held surface"))
        for key, name in C78S_NAMES.items():
            files.append(HeldPinnedInput(
                directory / name, "C78s held:" + key,
                C78_HISTORICAL_MEMBER_EXPECTED_MODE,
                str(C78S_FINAL["pins"][key])))
    for path, label, pin in (
        (sva_path, "C78s held verification A", C78S_FINAL["verification_A_file_sha256"]),
        (svb_path, "C78s held verification B", C78S_FINAL["verification_B_file_sha256"]),
        (fma_path, "C78s held final manifest A", C78S_FINAL["final_manifest_file_sha256"]),
        (fmb_path, "C78s held final manifest B", C78S_FINAL["final_manifest_file_sha256"]),
        (foa_path, "C78s held final outer A", C78S_FINAL["final_outer_file_sha256"]),
        (fob_path, "C78s held final outer B", C78S_FINAL["final_outer_file_sha256"]),
    ):
        files.append(HeldPinnedInput(
            path, label, C78_HISTORICAL_MEMBER_EXPECTED_MODE, str(pin)))
    need(len(files) == 51 and len(directories) == 5 and
         len({item.mount_id for item in [*files, *directories]}) == 1,
         "C78l exact25 plus C78s exact26 held files and exact5 directories on one statx mount")
    return HeldInputSet(files, directories)


def hold_fixed_evidence_surfaces() -> HeldInputSet:
    """Hold every fixed C55/C72 input not already held by the C42 full10."""
    c42_paths = set(C42_C53_PATHS.values())
    files = [
        HeldPinnedInput(path, "fixed historical evidence held:" + key,
                        HISTORICAL_FIXED_EXPECTED_MODES[path], FIXED_PINS[key])
        for key, path in FIXED_PATHS.items() if path not in c42_paths
    ]
    need(len(files) == 16 and len({item.path for item in files}) == 16 and
         FIXED_PATHS["C72G_HEAD"] == C53_HEAD_PATH,
         "fixed evidence exact16 plus shared C72G/C53 held head")
    return HeldInputSet(files, [])


def read_evidence(
        self_guard: HeldSelf,
        producer_guard: HeldOpaqueMetadata,
        c78_guard: HeldInputSet,
        c42_guard: HeldInputSet,
        fixed_guard: HeldInputSet,
        policy_guard: HeldInputSet,
        v3_guard: HeldInputSet,
        v3_source_metadata: list[HeldOpaqueMetadata],
        v4_guard: HeldInputSet,
        v4_source_metadata: list[HeldOpaqueMetadata],
        v5_guard: HeldInputSet,
        v5_source_metadata: list[HeldOpaqueMetadata],
        v6_guard: HeldInputSet,
        v6_source_metadata: list[HeldOpaqueMetadata],
        v7_guard: HeldInputSet,
        v7_source_metadata: list[HeldOpaqueMetadata],
        v8_guard: HeldInputSet,
        v8_source_metadata: list[HeldOpaqueMetadata],
        v9_guard: HeldInputSet,
        v9_source_metadata: list[HeldOpaqueMetadata],
        v10_guard: HeldInputSet,
        v10_source_metadata: list[HeldOpaqueMetadata],
        v11_guard: HeldInputSet,
        v11_source_metadata: list[HeldOpaqueMetadata]) -> dict[str, Any]:
    c78_by_path = {item.path: item for item in c78_guard.files}
    c78_directories = {item.path: item for item in c78_guard.directories}
    need(len(c78_by_path) == 51 and len(c78_directories) == 5,
         "read evidence consumes full-run held C78l/C78s surfaces")
    policy_by_path = {item.path: item for item in policy_guard.files}
    need(set(policy_by_path) == {
                 V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT, CONTRACT, CLOSED_SCHEMA,
                 V16_TO_V16R2_TRANSITION, STATIC_AUDIT_V16R2,
                 COLD_LAUNCHER, COLD_LAUNCH_MANIFEST, COLD_LAUNCH_OUTER},
             "read evidence active static/cold policy set")
    contract = strict_json(policy_by_path[CONTRACT].raw, "contract")
    verify_object(contract, "contract", CONTRACT_OBJECT_PIN)
    need(contract["effective_checkpoint_object_sha256"] == UPSTREAM_CHECKPOINT_OBJECT_PIN and
         contract.get("append_only_predecessor_v3", {}).get("execution_allowed") is False and
         contract.get("append_only_predecessor_v3", {}).get("runtime_surfaces_authoritative") is False and
         contract.get("completion_protocol", {}).get("standalone_final_outer_is_authoritative") is False and
         contract.get("completion_protocol", {}).get("committed_completion_itself_grants_credit") == 0 and
         contract.get("composite_authority_predicate", {}).get(
             "schema_root") == COLD_ROOT_SCHEMA,
         "v16r2 contract checkpoint/rejection/zero-outer/composite-root boundary")
    closed = strict_json(policy_by_path[CLOSED_SCHEMA].raw, "closed schema")
    allowed_root_keys = {"$schema", "$id", "$comment", "title", "description",
                         "$defs", "$ref"}
    need(isinstance(closed, dict) and set(closed) <= allowed_root_keys and
         isinstance(closed.get("$defs"), dict) and
         isinstance(closed.get("$ref"), str) and
         closed["$ref"] == "#/$defs/coldLaunchedCommittedAuthority" and
         "standaloneOuter" in closed["$defs"] and
         "authoritySeal" in closed["$defs"] and
         "innerComposite" in closed["$defs"] and
         "coldLaunchedCommittedAuthority" in closed["$defs"],
         "v16r2 schema root is cold-launched wrapper over zero-credit inner composite")
    v5_predecessor = validate_v5_published_then_rejected_predecessor(
        v6_guard, v5_guard, v5_source_metadata)
    v6_predecessor = validate_v6_published_then_rejected_predecessor(
        v7_guard, v6_guard, v6_source_metadata)
    v7_predecessor = validate_v7_published_then_rejected_predecessor(
        v8_guard, v7_guard, v7_source_metadata)
    v8_predecessor = validate_v8_published_then_rejected_predecessor(
        v9_guard, v8_guard, v8_source_metadata)
    v9_predecessor = validate_v9_published_then_rejected_predecessor(
        v10_guard, v9_guard, v9_source_metadata)
    v10_predecessor = validate_v10_published_then_rejected_predecessor(
        v11_guard, v10_guard, v10_source_metadata)
    v11_predecessor = validate_v11_published_then_rejected_predecessor(
        v11_guard, v11_source_metadata)
    v12_predecessor = validate_v12_published_then_rejected_predecessor()
    v4_supersession = exact_v4_rejection_supersession(
        held_v4_supersession_from_v5(v5_guard))
    v3_receipt_guard = held_v3_official_rejection(v3_guard)
    exact_v3_rejection(v3_receipt_guard, v3_guard, v3_source_metadata)
    validate_v4_rejected_static_draft7(
        v4_supersession, v4_guard, v4_source_metadata, v3_receipt_guard)
    current_terminal_identities = (
        {item.identity for item in policy_guard.files} |
        {self_guard.identity, producer_guard.identity})
    need(isinstance(_INCIDENT_AUTHORITY_HOLD,
                    HeldInheritedV14AuthorityExact12),
         "v12/v13 predecessor authority remains held during history closure")
    incident_hold = _INCIDENT_AUTHORITY_HOLD
    v12_predecessor_identities = \
        incident_hold.v12_exact10_identities()
    v12_predecessor_mount_ids = \
        incident_hold.v12_exact10_mount_ids()
    v14_predecessor_identities = incident_hold.v14_exact10_identities()
    v14_predecessor_mount_ids = incident_hold.v14_exact10_mount_ids()
    v14_rejection_identities = {incident_hold.v14_rejection_identity()}
    published_v11_identities = (
        {item.identity for item in v11_guard.files} |
        {item.identity for item in v11_source_metadata})
    published_v10_identities = (
        {item.identity for item in v10_guard.files} |
        {item.identity for item in v10_source_metadata})
    published_v9_identities = (
        {item.identity for item in v9_guard.files} |
        {item.identity for item in v9_source_metadata})
    published_v8_identities = (
        {item.identity for item in v8_guard.files} |
        {item.identity for item in v8_source_metadata})
    published_v7_identities = (
        {item.identity for item in v7_guard.files} |
        {item.identity for item in v7_source_metadata})
    published_v6_identities = (
        {item.identity for item in v6_guard.files} |
        {item.identity for item in v6_source_metadata})
    published_v5_identities = (
        {item.identity for item in v5_guard.files} |
        {item.identity for item in v5_source_metadata})
    published_v3_identities = (
        {item.identity for item in v3_guard.files
         if item.path != V3_OFFICIAL_REJECTION} |
        {item.identity for item in v3_source_metadata})
    rejected_v4_identities = (
        {item.identity for item in v4_guard.files} |
        {item.identity for item in v4_source_metadata})
    v3_rejection_identities = {v3_receipt_guard.identity}
    v13_source_identities = incident_hold.v13_incident_source_identities()
    v13_pyc_identities = incident_hold.v13_incident_pyc_identities()
    v12_rejection_identities = {incident_hold.v12_rejection_identity()}
    identity_groups = [
        current_terminal_identities, v14_predecessor_identities,
        v12_predecessor_identities,
        published_v11_identities, published_v10_identities,
        published_v9_identities, published_v8_identities,
        published_v7_identities, published_v6_identities,
        published_v5_identities, published_v3_identities,
        rejected_v4_identities, v3_rejection_identities,
        v13_source_identities, v13_pyc_identities,
        v12_rejection_identities, v14_rejection_identities,
    ]
    predecessor_identities = set()
    for identity_group in identity_groups[1:]:
        predecessor_identities.update(identity_group)
    current_exact8_identities = current_terminal_identities - {
        policy_by_path[COLD_LAUNCH_MANIFEST].identity,
        policy_by_path[COLD_LAUNCH_OUTER].identity,
    }
    prepublication_identities = predecessor_identities | current_exact8_identities
    terminal_identities = predecessor_identities | current_terminal_identities
    need(len(current_terminal_identities) == 10 and
         len(v12_predecessor_identities) == 10 and
         [len(group) for group in identity_groups] ==
             list(V16R2_TERMINAL_GROUP_VECTOR) and
         all(identity_groups[left].isdisjoint(identity_groups[right])
             for left in range(len(identity_groups))
             for right in range(left + 1, len(identity_groups))) and
         len(predecessor_identities) ==
             V16R2_PREDECESSOR_UNIQUE_LIVE_IDENTITY_COUNT and
         len(prepublication_identities) ==
             V16R2_PREPUBLICATION_UNIQUE_LIVE_IDENTITY_COUNT and
         len(terminal_identities) ==
             V16R2_TERMINAL_UNIQUE_LIVE_IDENTITY_COUNT and
         incident_hold.v13_supersession_identity() ==
             incident_hold.authority_exact12_by_role[
                 "v13_supersession_receipt"].identity and
         incident_hold.v14_supersession_identity() ==
             policy_by_path[
                 V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT].identity and
         len({item.mount_id for item in policy_guard.files} |
             {self_guard.mount_id, producer_guard.mount_id} |
             {item.mount_id for item in v3_guard.files} |
             {item.mount_id for item in v3_source_metadata} |
             {item.mount_id for item in v4_guard.files} |
             {item.mount_id for item in v4_source_metadata} |
             {item.mount_id for item in v5_guard.files} |
             {item.mount_id for item in v5_source_metadata} |
             {item.mount_id for item in v6_guard.files} |
             {item.mount_id for item in v6_source_metadata} |
             {item.mount_id for item in v7_guard.files} |
             {item.mount_id for item in v7_source_metadata} |
             {item.mount_id for item in v8_guard.files} |
             {item.mount_id for item in v8_source_metadata} |
             {item.mount_id for item in v9_guard.files} |
             {item.mount_id for item in v9_source_metadata} |
             {item.mount_id for item in v10_guard.files} |
             {item.mount_id for item in v10_source_metadata} |
             {item.mount_id for item in v11_guard.files} |
             {item.mount_id for item in v11_source_metadata} |
             v14_predecessor_mount_ids |
             v12_predecessor_mount_ids |
             incident_hold.v13_incident_mount_ids() |
             {incident_hold.by_env[V12_REJECTION_FD_ENV].mount_id,
              incident_hold.by_env[V13_SUPERSESSION_RECEIPT_FD_ENV].mount_id,
              incident_hold.authority_exact12_by_role[
                  "v14_official_rejection"].mount_id,
              incident_hold.authority_exact12_by_role[
                  "v14_registry_shape_drift_supersession_receipt"].mount_id}) == 1,
         "current v16r2 exact10 plus predecessor exact116 close as exact126 "
         "unique identities on one mount")

    fixed_by_path = {item.path: item for item in fixed_guard.files}
    c42_by_path = {item.path: item for item in c42_guard.files}
    expected_fixed16 = set(FIXED_PATHS.values()) - {C53_HEAD_PATH}
    need(len(expected_fixed16) == 16 and set(fixed_by_path) == expected_fixed16 and
         C53_HEAD_PATH in c42_by_path,
         "read evidence exact held fixed16 plus shared held C72G/C53 head")
    fixed: dict[str, bytes] = {}
    for key in sorted(FIXED_PATHS):
        path = FIXED_PATHS[key]
        item = c42_by_path[path] if path == C53_HEAD_PATH else fixed_by_path[path]
        need(sha(item.raw) == FIXED_PINS[key], "held fixed evidence pin:" + key)
        fixed[key] = item.raw
    objects: dict[str, Any] = {}
    for key, pin in FIXED_OBJECTS.items():
        value = strict_json(fixed[key], key)
        if key == "C72G_HEAD":
            body = copy.deepcopy(value)
            claim = body.pop("authority_seal_object_sha256", None)
            need(claim == pin and claim == digest(body), key + ":authority-seal closure")
        else:
            verify_object(value, key, pin)
        objects[key] = value
    need(objects["C55A_RESULT"]["bnb"]["remaining_unresolved_leaf_count"] == OVERLAY_COUNT and
         objects["C55B_RESULT"]["exact_unresolved_partition"]["total_current_unresolved_cell_count"] == OVERLAY_COUNT and
         objects["C72G_VERIFY"]["public_global_census"]["UNRESOLVED_R1648_CONTINUATION"] == OVERLAY_COUNT and
         objects["C72G_VERIFY"]["structural_closure"] == CLOSURE,
         "fixed predecessor semantics")
    # Fully decode and row-close the structure ledgers, not merely their pins.
    c55b_cells = gzip_rows(fixed["C55B_CELLS"], "C55B cells")
    c55b_edges = gzip_rows(fixed["C55B_EDGES"], "C55B edges")
    c55b_components = gzip_rows(fixed["C55B_COMPONENTS"], "C55B components")
    c55b_topology = validate_c55b_topology(c55b_cells, c55b_edges, c55b_components)
    kraft_chain = validate_c42_c53_kraft(c55b_cells, c42_guard)

    need(c78_directories[C78L_A].identity != c78_directories[C78L_B].identity and
         c78_directories[C78L_A].names == set(C78L_NAMES.values()) and
         c78_directories[C78L_B].names == set(C78L_NAMES.values()),
         "C78l exact dual historical 0755/10-member surfaces")
    c78l: dict[str, bytes] = {}
    for key, name in C78L_NAMES.items():
        left_item = c78_by_path[C78L_A / name]
        right_item = c78_by_path[C78L_B / name]
        left, left_identity = left_item.raw, left_item.identity
        right, right_identity = right_item.raw, right_item.identity
        need(left == right and left_identity != right_identity and
             sha(left) == C78L_PINS[key],
             "C78l held pin/bytes/inode separation:" + key)
        c78l[key] = left
    lva_item = c78_by_path[C78L_VERIFY_A]
    lvb_item = c78_by_path[C78L_VERIFY_B]
    lva, lva_identity = lva_item.raw, lva_item.identity
    lvb, lvb_identity = lvb_item.raw, lvb_item.identity
    need(sha(lva) == C78L_VERIFY_FILE and sha(lvb) == C78L_VERIFY_FILE and
         lva_identity != lvb_identity, "C78l verification pin/inode separation")
    need(lva == lvb, "C78l verification dual bytes")
    lv = strict_json(lva, "C78l verification"); verify_object(lv, "C78l verification", C78L_VERIFY_OBJECT)
    l_attacks = lv.get("self_test", {})
    need(lv.get("status") ==
             "PASS_INDEPENDENT_C78L__DUAL_BYTES__33319_TASKS__1124_C55A_OVERLAY__562_PAIRS__BRANCH_UNRESOLVED_ZERO__GLOBAL_REMAINDER_24__ZERO_CREDIT" and
         lv.get("verifier_file_sha256") ==
             "a384bba4c957046db26324d3794a346793b5467995de1798556c1fd4fe94ad6d" and
         lv.get("declared_producer_file_sha256") ==
             "9cdedea3c48e8f7b2db0ddeda56e2ce45037caaf1545f810c2033afae79db911" and
         lv.get("producer_was_not_opened_read_parsed_imported_executed_or_decoded") is True and
         lv.get("task_count") == 33_319 and lv.get("task_side_occurrence_count") == 66_638 and
         lv.get("public_cell_count") == 1_124 and lv.get("reflection_pair_count") == 562 and
         lv.get("branch_unresolved") == 0 and lv.get("public_global_unresolved_after_branch") == 24 and
         lv.get("public_global_unresolved_zero") is False and
         all(lv.get(key) == 0 for key in ("CM2_credit", "formal_credit", "global_credit",
                                          "whole_component_credit", "D02_gate_credit")) and
         l_attacks.get("attack_count") == 52 and
         len(l_attacks.get("attacks", {})) == 52 and
         all(value == "FAIL_CLOSED" for value in l_attacks["attacks"].values()) and
         str(l_attacks.get("status", "")).startswith("PASS_52_OF_52"),
         "C78l exact52 fail-closed attacks")
    need(c78_directories[C78L_COMPLETION].names == set(C78L_COMPLETION_NAMES.values()),
         "C78l completion exact3 historical surface")
    completion_raw: dict[str, bytes] = {}
    for key, name in C78L_COMPLETION_NAMES.items():
        raw = c78_by_path[C78L_COMPLETION / name].raw
        need(sha(raw) == C78L_COMPLETION_PINS[key], "C78l completion pin:" + key)
        completion_raw[key] = raw
        if key == "receipt":
            value = strict_json(raw, "C78l completion"); verify_object(value, "C78l completion", C78L_COMPLETION_OBJECT)
        elif key == "outer":
            value = strict_json(raw, "C78l completion outer"); verify_object(value, "C78l completion outer", C78L_COMPLETION_OUTER_OBJECT)
    need(parse_manifest_ordered(completion_raw["manifest"], "C78l completion manifest") ==
         [{"file_sha256": C78L_COMPLETION_PINS["receipt"],
           "entry_name": C78L_COMPLETION_NAMES["receipt"]}] and
         c78_by_path[C78L_COMPLETION /
                      C78L_COMPLETION_NAMES["receipt"]].before.st_mtime_ns <
         c78_by_path[C78L_COMPLETION /
                      C78L_COMPLETION_NAMES["manifest"]].before.st_mtime_ns <
         c78_by_path[C78L_COMPLETION /
                      C78L_COMPLETION_NAMES["outer"]].before.st_mtime_ns,
         "C78l completion manifest/order/outer-last")
    need(max(lva_item.before.st_mtime_ns, lvb_item.before.st_mtime_ns) <
         c78_by_path[C78L_COMPLETION /
                      C78L_COMPLETION_NAMES["receipt"]].before.st_mtime_ns,
         "C78l both verifications before completion")
    base_order = ["lock", "cells", "pairs", "report", "result", "registry", "tasks", "sides"]
    need(parse_manifest_ordered(c78l["manifest"], "C78l base manifest") ==
         [{"file_sha256": C78L_PINS[key], "entry_name": C78L_NAMES[key]} for key in base_order],
         "C78l exact ordered base8 manifest")
    for directory in (C78L_A, C78L_B):
        base_max = max(c78_by_path[directory /
                                   C78L_NAMES[key]].before.st_mtime_ns
                       for key in base_order)
        need(base_max < c78_by_path[directory /
                                    C78L_NAMES["manifest"]].before.st_mtime_ns <
             c78_by_path[directory /
                          C78L_NAMES["outer"]].before.st_mtime_ns,
             "C78l build manifest/outer mtime order")
    need(c78_by_path[C78L_A / C78L_NAMES["outer"]].before.st_mtime_ns <
             lva_item.before.st_mtime_ns and
         c78_by_path[C78L_B / C78L_NAMES["outer"]].before.st_mtime_ns <
             lvb_item.before.st_mtime_ns,
         "C78l corresponding outer before independent verification")
    lresult = strict_json(c78l["result"], "C78l result"); verify_object(lresult, "C78l result", C78L_RESULT_OBJECT)

    c78s_a = rooted(str(C78S_FINAL["build_A_directory"]))
    c78s_b = rooted(str(C78S_FINAL["build_B_directory"]))
    sva_path = rooted(str(C78S_FINAL["verification_A_path"]))
    svb_path = rooted(str(C78S_FINAL["verification_B_path"]))
    fma_path = rooted(str(C78S_FINAL["final_manifest_A_path"]))
    fmb_path = rooted(str(C78S_FINAL["final_manifest_B_path"]))
    foa_path = rooted(str(C78S_FINAL["final_outer_A_path"]))
    fob_path = rooted(str(C78S_FINAL["final_outer_B_path"]))
    exact13 = set(C78S_NAMES.values()) | {sva_path.name, fma_path.name, foa_path.name}
    need(len(exact13) == 13 and
         c78_directories[c78s_a].names == exact13 and
         c78_directories[c78s_b].names == exact13 and
         c78_directories[c78s_a].identity != c78_directories[c78s_b].identity,
         "C78s exact13 stage universes")
    c78s: dict[str, bytes] = {}
    stage_raw: dict[str, bytes] = {}
    for key, name in C78S_NAMES.items():
        left_item = c78_by_path[c78s_a / name]
        right_item = c78_by_path[c78s_b / name]
        left, left_identity = left_item.raw, left_item.identity
        right, right_identity = right_item.raw, right_item.identity
        need(left == right and left_identity != right_identity and
             sha(left) == C78S_FINAL["pins"][key],
             "C78s held pin/bytes/inode separation:" + key)
        c78s[key] = left
        stage_raw[name] = left
    sva_item = c78_by_path[sva_path]
    svb_item = c78_by_path[svb_path]
    sva, sva_identity = sva_item.raw, sva_item.identity
    svb, svb_identity = svb_item.raw, svb_item.identity
    need(sha(sva) == C78S_FINAL["verification_A_file_sha256"] and
         sha(svb) == C78S_FINAL["verification_B_file_sha256"] and
         sva_identity != svb_identity, "C78s verification pin/inode separation")
    need(sva == svb, "C78s verification bytes")
    sv = strict_json(sva, "C78s verification")
    verify_object(sv, "C78s verification", str(C78S_FINAL["verification_A_object_sha256"]))
    need(C78S_FINAL["verification_A_object_sha256"] ==
         C78S_FINAL["verification_B_object_sha256"], "C78s verification object pins agree")
    attacks = sv.get("coherent_attacks", {})
    producer_policy = sv.get("producer_source_policy", {})
    upstream_policy = sv.get("upstream_producer_source_policy", {})
    sealed_authority = sv.get("sealed_terminal_authority", {})
    branch_boundary = sv.get("branch_boundary", {})
    need(sv.get("status") ==
             "PASS_INDEPENDENT_NO_PRODUCER_EXACT_RECONSTRUCTION__SEALED_C77S_C77D_TERMINAL_AUTHORITY_ONLY__C55A_IDENTITY_ONLY__ZERO_INSTALLED_CREDIT" and
         sv.get("verifier_file_sha256") == C78S_FINAL["verifier_source_file_sha256"] and
         set(producer_policy) == {"compiled", "decoded", "executed", "imported", "opened", "parsed", "read"} and
         all(value is False for value in producer_policy.values()) and
         set(upstream_policy) == {"C77s", "C77d"} and
         all(set(policy) == set(producer_policy) and all(value is False for value in policy.values())
             for policy in upstream_policy.values()) and
         sealed_authority.get("C55A_role") == "OVERLAY_IDENTITY_ONLY_NEVER_TERMINAL_AUTHORITY" and
         sealed_authority.get("C55A_may_supply_or_modify_terminal_disposition") is False and
         sealed_authority.get("exclusive_sources") == [
             "INDEPENDENTLY_VERIFIED_SEALED_C77S_DUAL_BUNDLE",
             "INDEPENDENTLY_VERIFIED_SEALED_C77D_DUAL_BUNDLE"] and
         all(sv.get(key) == 0 for key in ("CM2_credit", "D02_gate_credit", "formal_credit",
                                          "global_installed_credit", "whole_parent_credit")) and
         sv.get("candidate_is_authority") is False and
         sv.get("canonical_pointer_or_seal_written") is False and
         sv.get("runtime_canonical_pointer_or_seal_writes") is False and
         branch_boundary.get("current_public_global_unresolved") == 1_148 and
         branch_boundary.get("candidate_public_unresolved_decrement") == 0 and
         branch_boundary.get("public_global_unresolved_after_branch") == 1_124 and
         branch_boundary.get("public_global_unresolved_zero") is False and
         attacks.get("attack_count") == attacks.get("rejected") and
         attacks.get("attack_count") == 128 and attacks.get("rejected") == 128 and
         len(attacks.get("names", [])) == attacks["attack_count"] and
         len(set(attacks["names"])) == attacks["attack_count"], "C78s coherent attacks")
    fma_item = c78_by_path[fma_path]
    fmb_item = c78_by_path[fmb_path]
    foa_item = c78_by_path[foa_path]
    fob_item = c78_by_path[fob_path]
    final_manifest_a, fma_identity = fma_item.raw, fma_item.identity
    final_manifest_b, fmb_identity = fmb_item.raw, fmb_item.identity
    final_outer_a, foa_identity = foa_item.raw, foa_item.identity
    final_outer_b, fob_identity = fob_item.raw, fob_item.identity
    need(sha(final_manifest_a) == C78S_FINAL["final_manifest_file_sha256"] and
         sha(final_manifest_b) == C78S_FINAL["final_manifest_file_sha256"] and
         sha(final_outer_a) == C78S_FINAL["final_outer_file_sha256"] and
         sha(final_outer_b) == C78S_FINAL["final_outer_file_sha256"] and
         fma_identity != fmb_identity and foa_identity != fob_identity,
         "C78s final pins/inode separation")
    need(sva_path.parent == c78s_a and svb_path.parent == c78s_b and
         fma_path.parent == c78s_a and fmb_path.parent == c78s_b and
         foa_path.parent == c78s_a and fob_path.parent == c78s_b,
         "C78s final members inside isolated stages")
    need(final_manifest_a == final_manifest_b and final_outer_a == final_outer_b,
         "C78s final dual bytes")
    sfinal = strict_json(final_outer_a, "C78s final outer")
    verify_object(sfinal, "C78s final outer", str(C78S_FINAL["final_outer_object_sha256"]))
    need(sfinal.get("all_final_stage_bytes_identical") is True and
         sfinal.get("all_final_members_terminal_byte_replayed_in_both_stages") is True and
         sfinal.get("terminal_byte_replay_member_count_per_stage") == 13,
         "C78s final closure")
    base_order = ["lock", "children", "sources", "pairs", "cells", "projection", "result", "report"]
    need(parse_manifest_ordered(c78s["manifest"], "C78s base manifest") ==
         [{"file_sha256": C78S_FINAL["pins"][key], "entry_name": C78S_NAMES[key]}
          for key in base_order], "C78s exact ordered base8 manifest")
    expected_final = [
        {"file_sha256": C78S_FINAL["pins"][key], "entry_name": C78S_NAMES[key]}
        for key in C78S_NAMES
    ] + [{"file_sha256": C78S_FINAL["verification_A_file_sha256"],
          "entry_name": sva_path.name}]
    need(parse_manifest_ordered(final_manifest_a, "C78s final manifest") == expected_final and
         sfinal.get("final_manifest_member_count") == 11 and
         sfinal.get("final_manifest_order") == [entry["entry_name"] for entry in expected_final],
         "C78s exact ordered final11 manifest")
    for directory, verification_path, manifest_path, outer_path in (
        (c78s_a, sva_path, fma_path, foa_path), (c78s_b, svb_path, fmb_path, fob_path)):
        base_max = max(c78_by_path[directory /
                                   C78S_NAMES[key]].before.st_mtime_ns
                       for key in base_order)
        need(base_max < c78_by_path[directory /
                                    C78S_NAMES["manifest"]].before.st_mtime_ns <
             c78_by_path[directory /
                          C78S_NAMES["outer"]].before.st_mtime_ns <
             c78_by_path[verification_path].before.st_mtime_ns <
             c78_by_path[manifest_path].before.st_mtime_ns <
             c78_by_path[outer_path].before.st_mtime_ns,
             "C78s strict held-fd publication mtime order")
    stage_raw[sva_path.name] = sva
    stage_raw[fma_path.name] = final_manifest_a
    stage_raw[foa_path.name] = final_outer_a
    need(len(stage_raw) == 13, "C78s replay exact13")
    sresult = strict_json(c78s["result"], "C78s result")
    verify_object(sresult, "C78s result", str(C78S_FINAL["result_object_sha256"]))
    # The full-run c78_guard remains open; callers execute its bracketed
    # same-fd/file-path and readable-dirfd universe replay immediately before
    # their semantic commit or inner-root return.
    return {
        "fixed": fixed,
        "objects": objects,
        "c78l": c78l,
        "c78l_cells": gzip_rows(c78l["cells"], "C78l cells"),
        "c78l_pairs": gzip_rows(c78l["pairs"], "C78l pairs"),
        "c78s": c78s,
        "c78s_projection": gzip_rows(c78s["projection"], "C78s projection"),
        "c78s_pairs": gzip_rows(c78s["pairs"], "C78s pairs"),
        "c55b_cells": c55b_cells,
        "c55b_edges": c55b_edges,
        "c55b_components": c55b_components,
        "c55b_topology": c55b_topology,
        "kraft_chain": kraft_chain,
        "authority_objects": {
            "C78l_verification": lv,
            "C78s_verification": sv,
            "C78s_final_outer": sfinal,
        },
        "published_then_officially_rejected_predecessor_v5": v5_predecessor,
        "published_then_officially_rejected_predecessor_v6": v6_predecessor,
        "published_then_officially_rejected_predecessor_v7": v7_predecessor,
        "published_then_officially_rejected_predecessor_v8": v8_predecessor,
        "v8_official_rejection": exact_v8_official_rejection(v9_guard)[0],
        "published_then_officially_rejected_predecessor_v9": v9_predecessor,
        "v9_official_rejection": exact_v9_official_rejection(v10_guard)[0],
        "published_then_officially_rejected_predecessor_v10": v10_predecessor,
        "v10_official_rejection": exact_v10_official_rejection(v11_guard)[0],
        "published_then_officially_rejected_predecessor_v11": v11_predecessor,
        "published_then_officially_rejected_predecessor_v12": v12_predecessor,
        "v11_official_rejection": exact_v11_official_rejection()[0],
        "v12_official_rejection": exact_v12_official_rejection()[0],
        "v16r2_predecessor_unique_live_identity_count":
            len(predecessor_identities),
        "v16r2_prepublication_unique_live_identity_count":
            len(prepublication_identities),
        "v16r2_terminal_unique_live_identity_count": len(terminal_identities),
        "v16r2_terminal_group_vector": [len(group) for group in identity_groups],
    }


def reconstruct_expected(evidence: dict[str, Any]) -> dict[str, Any]:
    leaf_object = strict_json(evidence["fixed"]["C55A_LEAF"], "C55A leaf ledger")
    verify_object(leaf_object, "C55A leaf ledger", FIXED_OBJECTS["C55A_LEAF"])
    leaves = leaf_object["leaves"]
    need(len(leaves) == UNIVERSE, "leaf count")
    leaf_by_cell: dict[str, dict[str, Any]] = {}
    unresolved: set[str] = set(); baseline: set[str] = set()
    for ordinal, leaf in enumerate(leaves):
        verify_row(leaf, "C55A leaf")
        need(leaf["leaf_ordinal"] == ordinal and leaf["cell_id"] not in leaf_by_cell, "leaf order/identity")
        terminal = leaf["terminal_disposition"]; reason = leaf["unresolved_reason"]
        need((terminal in TERMINALS and reason is None) or
             (terminal is None and isinstance(reason, str) and bool(reason)), "leaf XOR")
        leaf_by_cell[leaf["cell_id"]] = leaf
        (unresolved if terminal is None else baseline).add(leaf["cell_id"])
    need(len(baseline) == BASELINE and len(unresolved) == OVERLAY_COUNT, "baseline/overlay")

    cells = evidence["c55b_cells"]
    need(len(cells) == 1_724, "C55B cell count")
    c55b = one_index(cells, "cell_id", "C55B cells")
    pairs: dict[int, list[dict[str, Any]]] = defaultdict(list)
    c55b_unresolved: set[str] = set()
    for row in cells:
        need(row["cell_id"] in leaf_by_cell, "C55B identity")
        pairs[row["pair_index"]].append(row)
        if row["current_effective_disposition"] == "UNRESOLVED_R1648_CONTINUATION":
            c55b_unresolved.add(row["cell_id"])
    need(c55b_unresolved == unresolved and len(pairs) == PAIR_COUNT and
         all(len(rows) == 2 for rows in pairs.values()), "C55B unresolved/pairs")
    for rows in pairs.values():
        need(rows[0]["reflection_partner_cell_id"] == rows[1]["cell_id"] and
             rows[1]["reflection_partner_cell_id"] == rows[0]["cell_id"], "reciprocity")

    large = one_index(evidence["c78l_cells"], "cell_id", "large")
    singleton = one_index(evidence["c78s_projection"], "cell_id", "singleton")
    large_pair = one_index(evidence["c78l_pairs"], "pair_index", "large pairs")
    singleton_pair = one_index(evidence["c78s_pairs"], "pair_index", "singleton pairs")
    large_set = set(large); singleton_set = set(singleton)
    need(len(large_set) == LARGE_COUNT and len(singleton_set) == SINGLETON_COUNT and
         not large_set & singleton_set and large_set | singleton_set == unresolved and
         len(large_pair) == LARGE_PAIRS and len(singleton_pair) == SINGLETON_PAIRS,
         "authority overlay partition")

    overlay_rows: list[dict[str, Any]] = []; overlay_by_cell: dict[str, dict[str, Any]] = {}
    for cell_id in sorted(unresolved, key=lambda item: leaf_by_cell[item]["leaf_ordinal"]):
        leaf = leaf_by_cell[cell_id]; structure = c55b[cell_id]
        if cell_id in large:
            authority_row = large[cell_id]; enum = authority_row["public_cell_disposition"]
            need(enum in LARGE_MAP and authority_row["unresolved_count"] == 0 and
                 authority_row["owner_history_glue_two_sides_incidence_closed"] is True and
                 authority_row["prefix_Kraft"]["prefix_free"] is True, "large semantics")
            terminal, rule = LARGE_MAP[enum]; authority = "C78L_VERIFIED_FINAL_SURFACE"
        else:
            authority_row = singleton[cell_id]; enum = authority_row["terminal_enum"]
            need(enum in SINGLETON_MAP and authority_row["global_projection_installed"] is False and
                 authority_row["candidate_is_authority"] is False, "singleton semantics")
            pair = singleton_pair[structure["pair_index"]]
            need(pair["parent_prefix_free"] is True and pair["parent_Kraft"] == "1", "singleton Kraft")
            terminal, rule = SINGLETON_MAP[enum]; authority = "C78S_VERIFIED_FINAL_SURFACE"
        row = close_row({
            "schema": SCHEMA + ".overlay-row", "overlay_ordinal": len(overlay_rows),
            "leaf_ordinal": leaf["leaf_ordinal"], "cell_id": cell_id,
            "C55A_leaf_row_sha256": leaf["row_sha256"],
            "C55B_cell_row_sha256": structure["row_sha256"],
            "pair_index": structure["pair_index"], "component_index": structure["component_index"],
            "component_id": structure["component_id"],
            "reflection_partner_cell_id": structure["reflection_partner_cell_id"],
            "previous_terminal_disposition": None,
            "previous_unresolved_reason": leaf["unresolved_reason"],
            "terminal_authority": authority,
            "terminal_authority_row_sha256": authority_row["row_sha256"],
            "authority_input_enum": enum, "mapping_rule": rule,
            "terminal_disposition": terminal,
            "overlay_sets_disjoint_and_exact": True,
            "installed_atomically_only_by_C79g_completion": True,
            "row_is_individually_creditable": False, "closure": dict(CLOSURE),
        })
        overlay_rows.append(row); overlay_by_cell[cell_id] = row

    successor_rows: list[dict[str, Any]] = []; successor_by_cell: dict[str, dict[str, Any]] = {}
    census: Counter[str] = Counter(); retained = 0
    for leaf in leaves:
        overlay = overlay_by_cell.get(leaf["cell_id"])
        if overlay is None:
            terminal = leaf["terminal_disposition"]
            mode = "C72G_BASELINE_RETAINED"
            authority = "C55A_PREEXISTING_TERMINAL_RETAINED_UNDER_C72G_STRUCTURAL_CLOSURE"
            authority_row_sha = leaf["row_sha256"]
            overlay_sha = None; preserved = True; retained += 1
        else:
            terminal = overlay["terminal_disposition"]
            mode = "C79G_OVERLAY_REPLACEMENT"; authority = overlay["terminal_authority"]
            authority_row_sha = overlay["terminal_authority_row_sha256"]
            overlay_sha = overlay["row_sha256"]; preserved = False
        need(terminal in TERMINALS, "successor terminal")
        row = close_row({
            "schema": SCHEMA + ".full-successor-row", "leaf_ordinal": leaf["leaf_ordinal"],
            "cell_id": leaf["cell_id"], "C55A_leaf_row_sha256": leaf["row_sha256"],
            "origin_key": leaf["origin_key"], "physical_chart": leaf["physical_chart"],
            "exact_box": leaf["exact_box"], "source_cell_row_sha256": leaf["source_cell_row_sha256"],
            "component_ref": leaf["component_ref"], "reflection_pair_ref": leaf["reflection_pair_ref"],
            "previous_terminal_disposition": leaf["terminal_disposition"],
            "previous_unresolved_reason": leaf["unresolved_reason"],
            "successor_terminal_disposition": terminal, "successor_unresolved_reason": None,
            "lineage_mode": mode, "terminal_authority": authority,
            "terminal_authority_row_sha256": authority_row_sha,
            "overlay_row_sha256": overlay_sha,
            "baseline_terminal_preserved_exactly": preserved,
            "candidate_atomic_install_only": True,
        })
        successor_rows.append(row); successor_by_cell[leaf["cell_id"]] = row; census[terminal] += 1
    need(retained == BASELINE and len(successor_rows) == UNIVERSE, "successor counts")

    parent_rows: list[dict[str, Any]] = []; modes: Counter[str] = Counter()
    kraft = evidence["kraft_chain"]
    for pair_index in sorted(pairs):
        structural = pairs[pair_index]
        roles = {leaf_by_cell[row["cell_id"]]["component_ref"]["cell_role"]: row for row in structural}
        need(set(roles) == {"REPRESENTATIVE", "REFLECTED"}, "roles")
        representative = roles["REPRESENTATIVE"]; reflected = roles["REFLECTED"]
        ids = {representative["cell_id"], reflected["cell_id"]}
        evidence_authority = "C42_INSTALLED_PARENT_CONSERVATION_VIA_C53_C55B_JOIN"
        if ids <= baseline:
            mode = "C72G_BASELINE_RETAINED"
            authority = "C55A_PREEXISTING_TERMINALS_WITH_C72G_STRUCTURAL_CLOSURE"
            authority_sha = leaf_by_cell[representative["cell_id"]]["row_sha256"]
            need(all(row["whole_pair_terminal_after_C53"] is True for row in structural), "baseline pair")
        elif ids <= large_set:
            mode = "C78L_OVERLAY"; authority = "C78L_VERIFIED_FINAL_SURFACE"
            pair = large_pair[pair_index]; authority_sha = pair["row_sha256"]
            need(pair["prefix_Kraft"]["prefix_free"] is True and pair["unresolved_count"] == 0, "large pair")
        else:
            need(ids <= singleton_set, "no mixed pair")
            mode = "C78S_OVERLAY"; authority = "C78S_VERIFIED_FINAL_SURFACE"
            pair = singleton_pair[pair_index]; authority_sha = pair["row_sha256"]
            need(pair["parent_prefix_free"] is True and pair["parent_Kraft"] == "1", "singleton pair")
        components = sorted({row["component_index"] for row in structural})
        need(len(components) == 2, "cross-component reflection involution")
        dispositions = Counter(successor_by_cell[cell]["successor_terminal_disposition"] for cell in ids)
        parent_rows.append(close_row({
            "schema": SCHEMA + ".reflection-parent-closure-row",
            "parent_ordinal": len(parent_rows), "pair_index": pair_index,
            "representative_cell_id": representative["cell_id"],
            "reflected_cell_id": reflected["cell_id"],
            "representative_C55B_row_sha256": representative["row_sha256"],
            "reflected_C55B_row_sha256": reflected["row_sha256"],
            "representative_successor_row_sha256": successor_by_cell[representative["cell_id"]]["row_sha256"],
            "reflected_successor_row_sha256": successor_by_cell[reflected["cell_id"]]["row_sha256"],
            "component_indices": components, "parent_lineage_mode": mode,
            "terminal_authority": authority, "parent_authority_row_sha256": authority_sha,
            "terminal_disposition_census": dict(sorted(dispositions.items())),
            "reciprocal_reflection_partner_identity_closed": True,
            "owner_history_glue_two_sides_incidence_closed": True,
            "prefix_Kraft": {
                "evidence_authority": evidence_authority,
                "C42_parent_row_sha256": kraft["C42_rows_by_pair"][pair_index]["row_sha256"],
                "C53_parent_projection_object_sha256":
                    kraft["C53_projections_by_pair"][pair_index]["projection_object_sha256"],
                "C55B_crosswalk_two_side_row_sha256s":
                    sorted(row["row_sha256"] for row in structural),
                "C42_parent_Kraft_conservation": "1",
                "C72_boolean_used_as_authority": False,
                "prefix_free": True, "exact_parent_closure": True,
                "physical_reflection_duplicate_credit": 0},
            "unresolved_count": 0,
        })); modes[mode] += 1
    need(modes == Counter({"C72G_BASELINE_RETAINED": BASELINE_PAIRS,
                           "C78L_OVERLAY": LARGE_PAIRS, "C78S_OVERLAY": SINGLETON_PAIRS}),
         "parent modes")
    need(_INCIDENT_AUTHORITY_WITNESS == V10_COLON_PREFIX_WITNESS,
         "consumer inherited exact10 witness remains independently derived")
    return {"overlay": overlay_rows, "successor": successor_rows, "parents": parent_rows,
            "census": {key: census.get(key, 0) for key in sorted(TERMINALS)},
            "modes": dict(sorted(modes.items())),
            "published_then_officially_rejected_predecessor_v5":
                copy.deepcopy(
                    evidence["published_then_officially_rejected_predecessor_v5"]),
            "published_then_officially_rejected_predecessor_v6":
                copy.deepcopy(
                    evidence["published_then_officially_rejected_predecessor_v6"]),
            "published_then_officially_rejected_predecessor_v7":
                copy.deepcopy(
                    evidence["published_then_officially_rejected_predecessor_v7"]),
            "published_then_officially_rejected_predecessor_v8":
                copy.deepcopy(
                    evidence["published_then_officially_rejected_predecessor_v8"]),
            "v8_official_rejection": copy.deepcopy(
                evidence["v8_official_rejection"]),
            "published_then_officially_rejected_predecessor_v9":
                copy.deepcopy(
                    evidence["published_then_officially_rejected_predecessor_v9"]),
            "v9_official_rejection": copy.deepcopy(
                evidence["v9_official_rejection"]),
            "published_then_officially_rejected_predecessor_v10":
                copy.deepcopy(
                    evidence["published_then_officially_rejected_predecessor_v10"]),
            "v10_official_rejection": copy.deepcopy(
                evidence["v10_official_rejection"]),
            "published_then_officially_rejected_predecessor_v11":
                copy.deepcopy(
                    evidence["published_then_officially_rejected_predecessor_v11"]),
            "published_then_officially_rejected_predecessor_v12":
                copy.deepcopy(
                    evidence["published_then_officially_rejected_predecessor_v12"]),
            "v11_official_rejection": copy.deepcopy(
                evidence["v11_official_rejection"]),
            "v12_official_rejection": copy.deepcopy(
                evidence["v12_official_rejection"]),
            "v10_colon_prefix_witness_object_sha256":
                V10_COLON_PREFIX_WITNESS["object_sha256"],
            "v11_dual_validator_divergence_incident": copy.deepcopy(
                V11_DUAL_VALIDATOR_DIVERGENCE_INCIDENT),
            "C55B_topology": copy.deepcopy(evidence["c55b_topology"]),
            "Kraft_chain_summary": {
                key: copy.deepcopy(value) for key, value in evidence["kraft_chain"].items()
                if key not in {"C42_rows_by_pair", "C53_projections_by_pair"}
            }}


def candidate(
        candidate_dir: Path, peer_candidate_dir: Path,
        candidate_guard: HeldInputSet) -> dict[str, Any]:
    need(candidate_dir != peer_candidate_dir and
         {candidate_dir, peer_candidate_dir} == {CANDIDATE_A, CANDIDATE_B},
         "candidate paths are exact checkpoint-keyed A/B pair")
    by_path = {item.path: item for item in candidate_guard.files}
    by_directory = {item.path: item for item in candidate_guard.directories}
    expected_paths = ({candidate_dir / name for name in MEMBERS} |
                      {peer_candidate_dir / name for name in MEMBERS})
    need(set(by_path) == expected_paths and
         set(by_directory) == {candidate_dir, peer_candidate_dir} and
         by_directory[candidate_dir].identity != by_directory[peer_candidate_dir].identity and
         by_directory[candidate_dir].names == set(MEMBERS) and
         by_directory[peer_candidate_dir].names == set(MEMBERS),
         "dual candidate exact held directory/file surfaces")
    raw: dict[str, bytes] = {}
    peer_raw: dict[str, bytes] = {}
    member_identities: list[tuple[int, int]] = []
    for name in MEMBERS:
        left_item = by_path[candidate_dir / name]
        right_item = by_path[peer_candidate_dir / name]
        left, left_identity = left_item.raw, left_item.identity
        right, right_identity = right_item.raw, right_item.identity
        need(left == right, "dual candidate byte identity:" + name)
        need(left_identity != right_identity, "dual candidate inode separation:" + name)
        member_identities.extend((left_identity, right_identity))
        raw[name] = left
        peer_raw[name] = right
    need(len(member_identities) == 18 and len(set(member_identities)) == 18,
         "all 18 candidate member identities globally unique")
    manifest = parse_manifest(raw[MANIFEST], "candidate manifest")
    need(set(manifest) == {LOCK, OVERLAY, SUCCESSOR, PARENTS, REGISTRY, RESULT, REPORT},
         "candidate manifest exact universe")
    for name in (LOCK, OVERLAY, SUCCESSOR, PARENTS, REGISTRY, RESULT, REPORT):
        need(manifest.get(name) == sha(raw[name]), "candidate manifest:" + name)
    outer = strict_json(raw[OUTER_RECEIPT], "candidate outer"); verify_object(outer, "candidate outer")
    need(outer["candidate_manifest_file_sha256"] == sha(raw[MANIFEST]) and
         outer["candidate_outer_receipt_published_last"] is True and
         outer.get("candidate_install") == candidate_install_protocol() and
         outer["candidate_credit"] == ZERO and
         outer.get("standalone_non_authoritative") is True and
         outer.get("authority_requires_committed_completion_replay24_rejection_and_seal") is True and
         outer["canonical_pointer_written"] is False,
         "candidate outer semantics")
    registry = strict_json(raw[REGISTRY], "candidate registry"); verify_object(registry, "candidate registry")
    result = strict_json(raw[RESULT], "candidate result"); verify_object(result, "candidate result")
    need(result["source_registry_object_sha256"] == registry["object_sha256"] and
         outer["candidate_result_object_sha256"] == result["object_sha256"], "object chain")
    for directory in (candidate_dir, peer_candidate_dir):
        base_mtimes = [by_path[directory / name].before.st_mtime_ns
                       for name in (LOCK, OVERLAY, SUCCESSOR, PARENTS, REGISTRY, RESULT, REPORT)]
        manifest_mtime = by_path[directory / MANIFEST].before.st_mtime_ns
        outer_mtime = by_path[directory / OUTER_RECEIPT].before.st_mtime_ns
        need(max(base_mtimes) < manifest_mtime < outer_mtime,
             "candidate publication mtime order and outer-last:" + str(directory))
    return {"raw": raw, "overlay": gzip_rows(raw[OVERLAY], "candidate overlay"),
            "successor": gzip_rows(raw[SUCCESSOR], "candidate successor"),
            "parents": gzip_rows(raw[PARENTS], "candidate parents"),
            "registry": registry, "result": result, "outer": outer, "manifest": manifest,
            "dual_candidate_build_directories_mode": "0555",
            "dual_candidate_members_mode": "0444",
            "dual_candidate_members_single_link": True,
            "dual_candidate_members_byte_identical": True,
            "dual_candidate_corresponding_inodes_distinct": True}


def derive_ledger_descriptor(raw: bytes, rows: list[dict[str, Any]], label: str) -> dict[str, Any]:
    decoder = zlib.decompressobj(16 + zlib.MAX_WBITS)
    try:
        plain = decoder.decompress(raw) + decoder.flush()
    except zlib.error as exc:
        raise Reject(label + ":descriptor gzip") from exc
    need(decoder.eof is True and
         not decoder.unused_data and not decoder.unconsumed_tail and
         plain.endswith(b"\n") and len(plain.splitlines()) == len(rows),
         label + ":descriptor exact member")
    return {
        "row_count": len(rows),
        "file_sha256": sha(raw),
        "uncompressed_sha256": sha(plain),
        "row_hash_line_sequence_sha256": digest([sha(line) for line in plain.splitlines()]),
        "single_gzip_member": True,
    }


def compare(candidate_state: dict[str, Any], expected: dict[str, Any]) -> None:
    for key in ("overlay", "successor", "parents"):
        need(candidate_state[key] == expected[key], "independent exact reconstruction:" + key)
    result = candidate_state["result"]
    census = dict(expected["census"]); census["total"] = sum(census.values())
    need(set(result) == {
             "schema", "status", "source_registry_object_sha256", "ledger_descriptors",
             "exact_overlay_partition", "baseline_retention", "derived_final_four_class_census",
             "derived_final_four_class_census_was_not_hard_coded", "public_global_unresolved",
             "reflection_parent_closure", "C55B_topology_reconstruction", "authority_separation",
             "closure", "candidate_credit", "standalone_non_authoritative",
             "formal_credit_authority", "precursor_credits",
             "actual_C3_disposition_count", "conditional_C3_promoted_to_actual_C3",
             "canonical_pointer_written", "D02_started", "object_sha256"} and
         result["schema"] == SCHEMA + ".result" and
         result["status"] ==
             "PASS_CANDIDATE_1148_EXACT_OVERLAY__76832_FULL_SUCCESSOR__862_REFLECTION_PARENTS__PUBLIC_UNRESOLVED_ZERO__AWAIT_COLD_LAUNCHED_COMPOSITE_FOR_FORMAL_CREDIT" and
         result["exact_overlay_partition"] == {"C78l_large": LARGE_COUNT,
         "C78s_singleton": SINGLETON_COUNT, "total": OVERLAY_COUNT,
         "sets_disjoint": True, "union_equals_C55A_and_C55B_unresolved": True},
         "result overlay")
    need(result["baseline_retention"] == {
             "retained_terminal_rows": BASELINE, "terminal_disposition_unchanged": True,
             "C55A_row_lineage_unchanged": True} and
         result["derived_final_four_class_census"] == census and
         result["derived_final_four_class_census_was_not_hard_coded"] is True and
         result["public_global_unresolved"] == 0 and
         result["reflection_parent_closure"] == {
             "row_count": PAIR_COUNT, "authority_partition": expected["modes"],
             "reciprocal": True, "all_terminal": True} and
         result["C55B_topology_reconstruction"] == expected["C55B_topology"] and
         result["authority_separation"] == {
             "C55A": "IDENTITY_AND_PREDECESSOR_DISPOSITION_ONLY",
             "C55B": "COMPONENT_REFLECTION_GLUE_INCIDENCE_STRUCTURE_ONLY",
             "C72g": "BASELINE_STRUCTURAL_CLOSURE_ONLY",
             "C78l": "SOLE_AUTHORITY_FOR_1124_REPLACEMENTS",
             "C78s": "SOLE_AUTHORITY_FOR_24_REPLACEMENTS",
             "C55A_C55B_C72g_new_terminal_authority": False} and
         result["closure"] == CLOSURE and result["candidate_credit"] == ZERO and
         result["standalone_non_authoritative"] is True and
         result["formal_credit_authority"] ==
             "ONLY_EXTERNALLY_PINNED_COLD_LAUNCHER_WRAPPER_AFTER_HELD_CHILD_AND_POST_CHILD_TERMINAL_REPLAY" and
         result["canonical_pointer_written"] is False and result["D02_started"] is False and
         result["actual_C3_disposition_count"] == 0 and
         result["conditional_C3_promoted_to_actual_C3"] is False and
         result["precursor_credits"] == {
             "C65_local_terminal_formal_credit": 0,
             "C69c_source_decision_formal_credit": 0,
             "C70_ready_intersection_formal_credit": 0,
             "C78l_precursor_formal_credit": 0,
             "C78s_precursor_formal_credit": 0},
         "result semantics")
    registry = candidate_state["registry"]
    fixed_registry_keys = {
        "C55A:leaf_ledger": "C55A_LEAF", "C55A:result": "C55A_RESULT",
        "C55A:verification": "C55A_VERIFY", "C55A:manifest": "C55A_MANIFEST",
        "C55B:cells": "C55B_CELLS", "C55B:edges": "C55B_EDGES",
        "C55B:components": "C55B_COMPONENTS", "C55B:result": "C55B_RESULT",
        "C55B:verification": "C55B_VERIFY", "C55B:self_test": "C55B_SELFTEST",
        "C55B:manifest": "C55B_MANIFEST", "C72g:contract": "C72G_CONTRACT",
        "C72g:verification": "C72G_VERIFY", "C72g:self_test": "C72G_SELFTEST",
        "C72g:manifest": "C72G_MANIFEST", "C72g:outer": "C72G_OUTER",
        "C72g:head": "C72G_HEAD",
    }
    expected_fixed_registry = {
        label: {"path": str(FIXED_PATHS[key].relative_to(ROOT)),
                "file_sha256": FIXED_PINS[key]}
        for label, key in fixed_registry_keys.items()
    }
    expected_fixed_registry.update({
        f"DIRECT_KRAFT:{key}": {
            "path": str(C42_C53_PATHS[key].relative_to(ROOT)),
            "file_sha256": C42_C53_PINS[key],
        }
        for key in sorted(C42_C53_PATHS)
    })
    expected_c78l_registry = {
        key: {"filename": C78L_NAMES[key], "file_sha256": C78L_PINS[key]}
        for key in sorted(C78L_NAMES)
    }
    expected_c78s_registry = {
        key: {"filename": C78S_NAMES[key], "file_sha256": C78S_FINAL["pins"][key]}
        for key in sorted(C78S_NAMES)
    }
    need(set(registry) == {
             "schema", "producer_file_sha256", "contract_file_sha256", "contract_object_sha256",
             "closed_schema_file_sha256", "effective_checkpoint_object_sha256", "fixed_input_files",
             "C78l_dual_base_member_pins", "C78l_verification_file_sha256",
             "C78l_verification_object_sha256", "C78l_completion_member_pins",
             "C78s_filled_final_surface", "C78s_dual_base_member_pins",
             "C55B_topology_reconstruction", "C42_C53_direct_Kraft_reconstruction",
             "v3_official_later_rejection_receipt",
             "v4_rejection_supersession_receipt", "post_source_static_freeze_trust",
             "published_then_officially_rejected_predecessor_v5",
             "v5_official_rejection_file_sha256",
             "v5_official_rejection_object_sha256",
             "published_then_officially_rejected_predecessor_v6",
             "v6_official_rejection_file_sha256",
             "v6_official_rejection_object_sha256",
             "published_then_officially_rejected_predecessor_v7",
             "v7_official_rejection_file_sha256",
             "v7_official_rejection_object_sha256",
             "v7_publication_lock_continuity_incident",
             "published_then_officially_rejected_predecessor_v8",
             "v8_official_rejection", "v8_official_rejection_file_sha256",
             "v8_official_rejection_object_sha256",
             "v8_rollout_control_flow_incident",
             "published_then_officially_rejected_predecessor_v9",
             "v9_official_rejection", "v9_official_rejection_file_sha256",
             "v9_official_rejection_object_sha256",
             "v9_v6_held_self_identity_defect_shape_drift_incident",
             "published_then_officially_rejected_predecessor_v10",
             "v10_official_rejection", "v10_official_rejection_file_sha256",
             "v10_official_rejection_object_sha256",
             "v10_regression_label_prefix_incident",
             "published_then_officially_rejected_predecessor_v11",
             "published_then_officially_rejected_predecessor_v12",
             "v11_official_rejection", "v11_official_rejection_file_sha256",
             "v11_official_rejection_object_sha256",
             "v12_official_rejection_file_sha256",
             "v12_official_rejection_object_sha256",
             "v12_v5_rejection_shape_incident",
             "v10_colon_prefix_witness_object_sha256",
             "v11_dual_validator_divergence_incident",
             "append_only_history_unique_file_identity_count",
             "producer_exec_fd_is_fresh_sealed_memfd",
             "producer_exec_fd_distinct_from_installed_source_fd",
             "producer_exec_memfd_required_seals_valid",
             "producer_exec_bytes_equal_installed_source_bytes",
             "producer_exec_and_installed_source_terminal_replayed",
             "ten_incident_authority_inputs_inherited_as_held_fds",
             "ten_incident_held_fds_path_identity_mount_and_hash_revalidated",
             "current_v16r2_producer_source_content_opened_or_read",
             "current_v16r2_producer_source_content_imported_compiled_or_executed",
             "frozen_predecessor_incident_source_exact10_held_fd_bytes_read_only",
             "frozen_predecessor_incident_sources_used_only_for_noncredit_regression_authority",
             "terminal_authority", "structure_only_authority",
             "C55A_C55B_C72g_new_terminal_authority", "canonical_pointer_written",
             "standalone_non_authoritative",
             "authority_requires_committed_completion_replay24_rejection_and_seal",
             "D02_started", "candidate_credit", "object_sha256"} and
         registry["schema"] == SCHEMA + ".source-registry" and
         registry["contract_file_sha256"] == CONTRACT_FILE_PIN and
         registry["contract_object_sha256"] == CONTRACT_OBJECT_PIN and
         registry["closed_schema_file_sha256"] == CLOSED_SCHEMA_FILE_PIN and
         registry["v3_official_later_rejection_receipt"] == {
             "path": str(V3_OFFICIAL_REJECTION.relative_to(ROOT)),
             "file_sha256": V3_OFFICIAL_REJECTION_FILE_PIN,
             "object_sha256": V3_OFFICIAL_REJECTION_OBJECT_PIN,
             "reason": "ORPHANED_OR_INCOMPLETE_C79G_V3_SURFACE"} and
         registry["v4_rejection_supersession_receipt"] == {
             "path": str(V4_REJECTION_SUPERSESSION.relative_to(ROOT)),
             "file_sha256": V4_REJECTION_SUPERSESSION_FILE_PIN,
             "object_sha256": V4_REJECTION_SUPERSESSION_OBJECT_PIN,
             "v4_execution_allowed": False,
             "v4_credit_transferred": 0} and
         registry["published_then_officially_rejected_predecessor_v5"] ==
             expected["published_then_officially_rejected_predecessor_v5"] and
         registry["v5_official_rejection_file_sha256"] ==
             V5_OFFICIAL_REJECTION_FILE_PIN and
         registry["v5_official_rejection_object_sha256"] ==
             V5_OFFICIAL_REJECTION_OBJECT_PIN and
         registry["published_then_officially_rejected_predecessor_v6"] ==
             expected["published_then_officially_rejected_predecessor_v6"] and
         registry["v6_official_rejection_file_sha256"] ==
             V6_OFFICIAL_REJECTION_FILE_PIN and
         registry["v6_official_rejection_object_sha256"] ==
             V6_OFFICIAL_REJECTION_OBJECT_PIN and
         registry["published_then_officially_rejected_predecessor_v7"] ==
             expected["published_then_officially_rejected_predecessor_v7"] and
         registry["v7_official_rejection_file_sha256"] ==
             V7_OFFICIAL_REJECTION_FILE_PIN and
         registry["v7_official_rejection_object_sha256"] ==
             V7_OFFICIAL_REJECTION_OBJECT_PIN and
         registry["v7_publication_lock_continuity_incident"] ==
             _validated_v7_publication_lock_continuity_incident() and
         registry["published_then_officially_rejected_predecessor_v8"] ==
             expected["published_then_officially_rejected_predecessor_v8"] and
         registry["v8_official_rejection_file_sha256"] ==
             V8_OFFICIAL_REJECTION_FILE_PIN and
         registry["v8_official_rejection_object_sha256"] ==
             V8_OFFICIAL_REJECTION_OBJECT_PIN and
         registry["v8_official_rejection"].get("object_sha256") ==
             V8_OFFICIAL_REJECTION_OBJECT_PIN and
         registry["v8_rollout_control_flow_incident"] ==
             V8_ROLLOUT_CONTROL_FLOW_INCIDENT and
         registry["published_then_officially_rejected_predecessor_v9"] ==
             expected["published_then_officially_rejected_predecessor_v9"] and
         registry["v9_official_rejection_file_sha256"] ==
             V9_OFFICIAL_REJECTION_FILE_PIN and
         registry["v9_official_rejection_object_sha256"] ==
             V9_OFFICIAL_REJECTION_OBJECT_PIN and
         registry["v9_official_rejection"].get("object_sha256") ==
             V9_OFFICIAL_REJECTION_OBJECT_PIN and
         registry["v9_v6_held_self_identity_defect_shape_drift_incident"] ==
             V9_V6_HELD_SELF_IDENTITY_DEFECT_SHAPE_DRIFT_INCIDENT and
         registry["published_then_officially_rejected_predecessor_v10"] ==
             expected["published_then_officially_rejected_predecessor_v10"] and
         registry["v10_official_rejection_file_sha256"] ==
             V10_OFFICIAL_REJECTION_FILE_PIN and
         registry["v10_official_rejection_object_sha256"] ==
             V10_OFFICIAL_REJECTION_OBJECT_PIN and
         registry["v10_official_rejection"].get("object_sha256") ==
             V10_OFFICIAL_REJECTION_OBJECT_PIN and
         registry["v10_regression_label_prefix_incident"] ==
             V10_REGRESSION_LABEL_PREFIX_INCIDENT and
         registry["published_then_officially_rejected_predecessor_v11"] ==
             _expected_published_then_rejected_v11_proof() and
         registry["published_then_officially_rejected_predecessor_v12"] ==
             _expected_published_then_rejected_v12_proof() and
         registry["v11_official_rejection_file_sha256"] ==
             V11_OFFICIAL_REJECTION_FILE_PIN and
         registry["v11_official_rejection_object_sha256"] ==
             V11_OFFICIAL_REJECTION_OBJECT_PIN and
         registry["v11_official_rejection"].get("object_sha256") ==
             V11_OFFICIAL_REJECTION_OBJECT_PIN and
         registry["v12_official_rejection_file_sha256"] ==
             V12_OFFICIAL_REJECTION_FILE_PIN and
         registry["v12_official_rejection_object_sha256"] ==
             V12_OFFICIAL_REJECTION_OBJECT_PIN and
         registry["v12_v5_rejection_shape_incident"] ==
             V12_V5_REJECTION_SHAPE_INCIDENT and
         registry["v10_colon_prefix_witness_object_sha256"] ==
             V10_COLON_PREFIX_WITNESS["object_sha256"] and
         registry["v11_dual_validator_divergence_incident"] ==
             V11_DUAL_VALIDATOR_DIVERGENCE_INCIDENT and
         registry["append_only_history_unique_file_identity_count"] ==
             V16R2_TERMINAL_UNIQUE_LIVE_IDENTITY_COUNT and
         registry["producer_exec_fd_is_fresh_sealed_memfd"] is True and
         registry["producer_exec_fd_distinct_from_installed_source_fd"] is True and
         registry["producer_exec_memfd_required_seals_valid"] is True and
         registry["producer_exec_bytes_equal_installed_source_bytes"] is True and
         registry["producer_exec_and_installed_source_terminal_replayed"] is True and
         registry["effective_checkpoint_object_sha256"] == UPSTREAM_CHECKPOINT_OBJECT_PIN and
         isinstance(registry["producer_file_sha256"], str) and
         registry["producer_file_sha256"] == PRODUCER_SOURCE_PIN and
         registry["fixed_input_files"] == expected_fixed_registry and
         registry["C78l_dual_base_member_pins"] == expected_c78l_registry and
         registry["C78l_verification_file_sha256"] == C78L_VERIFY_FILE and
         registry["C78l_verification_object_sha256"] == C78L_VERIFY_OBJECT and
         registry["C78l_completion_member_pins"] == C78L_COMPLETION_PINS and
         registry["C78s_filled_final_surface"] == C78S_FINAL and
         registry["C78s_dual_base_member_pins"] == expected_c78s_registry and
         registry["C55B_topology_reconstruction"] == expected["C55B_topology"] and
         registry["C42_C53_direct_Kraft_reconstruction"] == expected["Kraft_chain_summary"] and
         isinstance(registry["post_source_static_freeze_trust"], dict) and
         set(registry["post_source_static_freeze_trust"]) == {
             "v16_to_v16r2_transition_receipt", "static_audit_v16r2", "cold_launcher",
             "cold_launch_manifest", "cold_launch_outer_last",
             "both_receipts_strict_parsed_object_closed_held_and_terminally_replayed",
             "both_receipts_pin_current_producer_and_policy_bundle",
             "exact8_manifest_and_outer_last_strictly_validated_and_terminally_replayed",
             "all_exact8_mtime_not_after_final_ctime",
             "max_exact8_final_mtime_ctime_before_manifest_mtime",
             "manifest_mtime_not_after_final_ctime",
             "manifest_final_ctime_before_outer_mtime",
             "outer_mtime_not_after_final_ctime",
             "physical_exact8_freeze_then_manifest_freeze_then_outer_freeze_chronology",
             "cold_exact10_identities_unique_same_mount",
             "normative_runtime_entry_is_externally_pinned_cold_launcher"} and
         registry["post_source_static_freeze_trust"].get(
             "v16_to_v16r2_transition_receipt", {}).get("path") ==
             str(V16_TO_V16R2_TRANSITION.relative_to(ROOT)) and
         _nonzero_sha256(registry["post_source_static_freeze_trust"].get(
             "v16_to_v16r2_transition_receipt", {}).get("file_sha256")) and
         _nonzero_sha256(registry["post_source_static_freeze_trust"].get(
             "v16_to_v16r2_transition_receipt", {}).get("object_sha256")) and
         registry["post_source_static_freeze_trust"].get(
             "static_audit_v16r2", {}).get("path") ==
             str(STATIC_AUDIT_V16R2.relative_to(ROOT)) and
         _nonzero_sha256(registry["post_source_static_freeze_trust"].get(
             "static_audit_v16r2", {}).get("file_sha256")) and
         _nonzero_sha256(registry["post_source_static_freeze_trust"].get(
             "static_audit_v16r2", {}).get("object_sha256")) and
         registry["post_source_static_freeze_trust"].get(
             "cold_launcher", {}).get("path") == str(COLD_LAUNCHER.relative_to(ROOT)) and
         _nonzero_sha256(registry["post_source_static_freeze_trust"].get(
             "cold_launcher", {}).get("file_sha256")) and
         registry["post_source_static_freeze_trust"].get(
             "cold_launch_manifest", {}).get("path") ==
             str(COLD_LAUNCH_MANIFEST.relative_to(ROOT)) and
         registry["post_source_static_freeze_trust"].get(
             "cold_launch_manifest", {}).get("ordered_entry_count") == 8 and
         _nonzero_sha256(registry["post_source_static_freeze_trust"].get(
             "cold_launch_manifest", {}).get("file_sha256")) and
         registry["post_source_static_freeze_trust"].get(
             "cold_launch_outer_last", {}).get("path") ==
             str(COLD_LAUNCH_OUTER.relative_to(ROOT)) and
         _nonzero_sha256(registry["post_source_static_freeze_trust"].get(
             "cold_launch_outer_last", {}).get("file_sha256")) and
         _nonzero_sha256(registry["post_source_static_freeze_trust"].get(
             "cold_launch_outer_last", {}).get("object_sha256")) and
         all(registry["post_source_static_freeze_trust"].get(name) is True for name in (
             "both_receipts_strict_parsed_object_closed_held_and_terminally_replayed",
             "both_receipts_pin_current_producer_and_policy_bundle",
             "exact8_manifest_and_outer_last_strictly_validated_and_terminally_replayed",
             "all_exact8_mtime_not_after_final_ctime",
             "max_exact8_final_mtime_ctime_before_manifest_mtime",
             "manifest_mtime_not_after_final_ctime",
             "manifest_final_ctime_before_outer_mtime",
             "outer_mtime_not_after_final_ctime",
             "physical_exact8_freeze_then_manifest_freeze_then_outer_freeze_chronology",
             "cold_exact10_identities_unique_same_mount",
             "normative_runtime_entry_is_externally_pinned_cold_launcher")) and
         registry["ten_incident_authority_inputs_inherited_as_held_fds"] is True and
         registry["ten_incident_held_fds_path_identity_mount_and_hash_revalidated"] is True and
         registry["current_v16r2_producer_source_content_opened_or_read"] is False and
         registry["current_v16r2_producer_source_content_imported_compiled_or_executed"] is False and
         registry["frozen_predecessor_incident_source_exact10_held_fd_bytes_read_only"] is True and
         registry["frozen_predecessor_incident_sources_used_only_for_noncredit_regression_authority"] is True and
         registry["C55A_C55B_C72g_new_terminal_authority"] is False and
         registry["standalone_non_authoritative"] is True and
         registry["authority_requires_committed_completion_replay24_rejection_and_seal"] is True and
         registry["candidate_credit"] == ZERO and registry["D02_started"] is False and
         registry["canonical_pointer_written"] is False and
         registry["terminal_authority"] == {"C78l_rows": LARGE_COUNT, "C78s_rows": SINGLETON_COUNT} and
         registry["structure_only_authority"] == ["C55A", "C55B", "C72g"],
         "registry independence/credit")


def set_path(value: dict[str, Any], path: tuple[str, ...], replacement: Any) -> None:
    target: Any = value
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = replacement


def altered(value: Any) -> Any:
    if type(value) is bool:
        return not value
    if isinstance(value, int):
        return value + 1
    if value is None:
        return "ATTACK"
    if isinstance(value, str):
        replacement = "0" * 64 if len(value) == 64 else value + "__ATTACK"
        return ("1" * 64) if replacement == value else replacement
    if isinstance(value, list):
        return list(reversed(value)) if len(value) > 1 else [*value, "ATTACK"]
    raise Reject("unsupported structural mutation")


def reclose_row(row: dict[str, Any]) -> dict[str, Any]:
    body = copy.deepcopy(row); body.pop("row_sha256", None)
    return close_row(body)


def reclose_object(value: dict[str, Any]) -> dict[str, Any]:
    body = copy.deepcopy(value); body.pop("object_sha256", None)
    return close_object(body)


def attack_model(actual: dict[str, Any], evidence: dict[str, Any]) -> dict[str, Any]:
    return {
        "overlay": actual["overlay"], "successor": actual["successor"],
        "parents": actual["parents"], "result": actual["result"],
        "registry": actual["registry"], "outer": actual["outer"],
        "manifest": parse_manifest(actual["raw"][MANIFEST], "attack manifest"),
        "authority_objects": evidence["authority_objects"],
        "raw_overlay": actual["raw"][OVERLAY],
        "raw_successor": actual["raw"][SUCCESSOR],
        "raw_parents": actual["raw"][PARENTS],
        "raw_members": actual["raw"],
    }


def validate_authority_objects(values: Mapping[str, Any]) -> None:
    need(set(values) == {"C78l_verification", "C78s_verification", "C78s_final_outer"},
         "authority validator:exact object universe")
    large = values["C78l_verification"]
    single = values["C78s_verification"]
    outer = values["C78s_final_outer"]
    verify_object(large, "authority validator:C78l", C78L_VERIFY_OBJECT)
    verify_object(single, "authority validator:C78s", str(C78S_FINAL["verification_A_object_sha256"]))
    verify_object(outer, "authority validator:C78s outer",
                  str(C78S_FINAL["final_outer_object_sha256"]))
    need(str(large.get("status", "")).startswith("PASS_INDEPENDENT_C78L") and
         large.get("producer_was_not_opened_read_parsed_imported_executed_or_decoded") is True and
         large.get("self_test", {}).get("attack_count") == 52 and
         large.get("public_global_unresolved_zero") is False,
         "authority validator:C78l semantics")
    attacks = single.get("coherent_attacks", {})
    names = attacks.get("names")
    need(single.get("verifier_file_sha256") == C78S_FINAL["verifier_source_file_sha256"] and
         single.get("candidate_base_bundle", {}).get("stage_a_stage_b_bytes_identical") is True and
         single.get("candidate_base_bundle", {}).get("stage_a_stage_b_inodes_distinct") is True and
         single.get("candidate_base_bundle", {}).get("result_file_sha256") == C78S_FINAL["pins"]["result"] and
         single.get("candidate_base_bundle", {}).get("result_object_sha256") == C78S_FINAL["result_object_sha256"] and
         attacks.get("attack_count") == 128 and attacks.get("rejected") == 128 and
         isinstance(names, list) and len(names) == 128 and len(set(names)) == 128,
         "authority validator:C78s verification semantics")
    need(outer.get("verification_file_sha256") == C78S_FINAL["verification_A_file_sha256"] and
         outer.get("verification_object_sha256") == C78S_FINAL["verification_A_object_sha256"] and
         outer.get("final_manifest_file_sha256") == C78S_FINAL["final_manifest_file_sha256"] and
         outer.get("all_final_stage_bytes_identical") is True and
         outer.get("all_final_members_terminal_byte_replayed_in_both_stages") is True and
         outer.get("terminal_byte_replay_member_count_per_stage") == 13,
         "authority validator:C78s outer semantics")


def validate_candidate_metadata(result: dict[str, Any], registry: dict[str, Any],
                                outer: dict[str, Any], manifest: Mapping[str, str],
                                raw_members: Mapping[str, bytes], expected: dict[str, Any]) -> None:
    compare({"overlay": expected["overlay"], "successor": expected["successor"],
             "parents": expected["parents"], "result": result, "registry": registry}, expected)
    expected_descriptors = {
        "overlay_1148": derive_ledger_descriptor(
            raw_members[OVERLAY], expected["overlay"], "metadata overlay"),
        "full_successor_76832": derive_ledger_descriptor(
            raw_members[SUCCESSOR], expected["successor"], "metadata successor"),
        "reflection_parent_closure_862": derive_ledger_descriptor(
            raw_members[PARENTS], expected["parents"], "metadata parents"),
    }
    need(result.get("ledger_descriptors") == expected_descriptors,
         "metadata validator:derived ledger descriptors")
    need(set(manifest) == {LOCK, OVERLAY, SUCCESSOR, PARENTS, REGISTRY, RESULT, REPORT},
         "metadata validator:manifest exact universe")
    for name in (LOCK, OVERLAY, SUCCESSOR, PARENTS, REGISTRY, RESULT, REPORT):
        need(manifest.get(name) == sha(raw_members[name]),
             "metadata validator:manifest member:" + name)
    manifest_raw = b"".join(
        f"{manifest[name]}  {name}\n".encode("ascii")
        for name in (LOCK, OVERLAY, SUCCESSOR, PARENTS, REGISTRY, RESULT, REPORT)
    )
    ordered_member_hashes = [
        {"filename": name, "file_sha256": sha(raw_members[name])}
        for name in (LOCK, OVERLAY, SUCCESSOR, PARENTS, REGISTRY, RESULT, REPORT)
    ]
    need(set(outer) == {
             "schema", "candidate_result_object_sha256", "source_registry_object_sha256",
             "candidate_manifest_file_sha256", "ordered_member_file_sha256",
             "candidate_outer_receipt_published_last", "terminal_byte_replay_required_after_outer_receipt",
             "candidate_directory_sealed_mode_after_terminal_replay", "candidate_member_required_mode",
             "partial_publication_policy", "candidate_install", "candidate_credit",
             "canonical_pointer_written",
             "standalone_non_authoritative",
             "authority_requires_committed_completion_replay24_rejection_and_seal",
             "D02_started", "object_sha256"} and
         outer.get("schema") == SCHEMA + ".candidate-outer-receipt" and
         result.get("source_registry_object_sha256") == registry.get("object_sha256") and
         outer.get("candidate_result_object_sha256") == result.get("object_sha256") and
         outer.get("source_registry_object_sha256") == registry.get("object_sha256") and
         outer.get("candidate_manifest_file_sha256") == sha(manifest_raw) and
         outer.get("ordered_member_file_sha256") == ordered_member_hashes and
         outer.get("candidate_outer_receipt_published_last") is True and
         outer.get("terminal_byte_replay_required_after_outer_receipt") is True and
         outer.get("candidate_directory_sealed_mode_after_terminal_replay") == "0555" and
         outer.get("candidate_member_required_mode") == "0444" and
         outer.get("partial_publication_policy") == "REJECT_AND_PRESERVE_NEVER_OVERWRITE_OR_REUSE" and
         outer.get("candidate_install") == candidate_install_protocol() and
         outer.get("candidate_credit") == ZERO and
         outer.get("standalone_non_authoritative") is True and
         outer.get("authority_requires_committed_completion_replay24_rejection_and_seal") is True and
         outer.get("canonical_pointer_written") is False and outer.get("D02_started") is False,
         "metadata validator:outer/result/registry chain")


def v11_incident_attack_bundle() -> dict[str, Any]:
    return {
        "v10_colon_prefix_witness": copy.deepcopy(V10_COLON_PREFIX_WITNESS),
        "v11_dual_validator_divergence_incident": copy.deepcopy(
            V11_DUAL_VALIDATOR_DIVERGENCE_INCIDENT),
        "v11_dual_validator_divergence_incident_sha256":
            V11_DUAL_VALIDATOR_DIVERGENCE_INCIDENT_SHA256,
        "three_independent_helper_normalized_ast_sha256":
            V10_COLON_PREFIX_WITNESS_HELPER_AST_SHA256,
        "inherited_held_fd_revalidation": {
            "v10_producer_same_path_inode_mount_and_sha256": True,
            "v9_launcher_same_path_inode_mount_and_sha256": True,
            "v11_producer_same_path_inode_mount_and_sha256": True,
            "v11_launcher_same_path_inode_mount_and_sha256": True,
            "v11_rejection_same_path_inode_mount_and_sha256": True,
            "all_five_inherited_descriptors_revalidated_before_incident_authority": True,
        },
        "v11_official_rejection_closure": {
            "file_sha256": V11_OFFICIAL_REJECTION_FILE_PIN,
            "object_sha256": V11_OFFICIAL_REJECTION_OBJECT_PIN,
            "exact_key_count": 52,
            "file_mode": "0444",
            "file_nlink": 1,
            "singleton_namespace_mode": "0555",
            "singleton_namespace_nlink": 2,
            "positive_or_stage_surface_count": 0,
            "outer_strictly_precedes_rejection": True,
        },
    }


def v11_incident_attack_mutation(
        path: tuple[str, ...], replacement: Any) -> dict[str, Any]:
    bundle = v11_incident_attack_bundle()
    target: Any = bundle
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = replacement
    if path[0] == "v10_colon_prefix_witness":
        witness = dict(bundle["v10_colon_prefix_witness"])
        witness.pop("object_sha256", None)
        bundle["v10_colon_prefix_witness"] = close_object(witness)
    elif path[0] == "v11_dual_validator_divergence_incident":
        bundle["v11_dual_validator_divergence_incident_sha256"] = digest(
            bundle["v11_dual_validator_divergence_incident"])
    return {"v11_incident_attack": bundle}


def validate_v11_incident_attack_patch(bundle: Mapping[str, Any]) -> None:
    need(set(bundle) == {
             "v10_colon_prefix_witness",
             "v11_dual_validator_divergence_incident",
             "v11_dual_validator_divergence_incident_sha256",
             "three_independent_helper_normalized_ast_sha256",
             "inherited_held_fd_revalidation",
             "v11_official_rejection_closure"},
         "v11 incident attack exact bundle")
    witness = bundle.get("v10_colon_prefix_witness")
    incident = bundle.get("v11_dual_validator_divergence_incident")
    held = bundle.get("inherited_held_fd_revalidation")
    rejection = bundle.get("v11_official_rejection_closure")
    need(isinstance(witness, dict) and _closed_object_equal(witness) and
         set(witness) == set(V10_COLON_PREFIX_WITNESS) and
         witness == V10_COLON_PREFIX_WITNESS and
         witness.get("successor_clause_truth_vector") == [True] * 15 and
         witness.get("successor_all_clauses_true") is True and
         witness.get("zero_or_multiple_expanded_dicts_controlled_reject") is True,
         "v11 incident attack exact40 witness")
    need(isinstance(incident, dict) and
         set(incident) == set(V11_DUAL_VALIDATOR_DIVERGENCE_INCIDENT) and
         incident == V11_DUAL_VALIDATOR_DIVERGENCE_INCIDENT and
         bundle.get("v11_dual_validator_divergence_incident_sha256") ==
             V11_DUAL_VALIDATOR_DIVERGENCE_INCIDENT_SHA256 == digest(incident),
         "v11 incident attack exact45 incident")
    need(bundle.get("three_independent_helper_normalized_ast_sha256") ==
             V10_COLON_PREFIX_WITNESS_HELPER_AST_SHA256,
         "v11 incident attack three-helper normalized AST agreement")
    need(held == {
             "v10_producer_same_path_inode_mount_and_sha256": True,
             "v9_launcher_same_path_inode_mount_and_sha256": True,
             "v11_producer_same_path_inode_mount_and_sha256": True,
             "v11_launcher_same_path_inode_mount_and_sha256": True,
             "v11_rejection_same_path_inode_mount_and_sha256": True,
             "all_five_inherited_descriptors_revalidated_before_incident_authority": True,
         }, "v11 incident attack inherited held-fd bindings")
    need(rejection == {
             "file_sha256": V11_OFFICIAL_REJECTION_FILE_PIN,
             "object_sha256": V11_OFFICIAL_REJECTION_OBJECT_PIN,
             "exact_key_count": 52,
             "file_mode": "0444",
             "file_nlink": 1,
             "singleton_namespace_mode": "0555",
             "singleton_namespace_nlink": 2,
             "positive_or_stage_surface_count": 0,
             "outer_strictly_precedes_rejection": True,
         }, "v11 incident attack official rejection and surface closure")


def validate_attack_patch(patch: dict[str, Any], pristine: dict[str, Any],
                          expected: dict[str, Any]) -> None:
    if "v11_incident_attack" in patch:
        need(set(patch) == {"v11_incident_attack"},
             "v11 incident attack patch exact singleton")
        value = patch["v11_incident_attack"]
        need(isinstance(value, dict), "v11 incident attack patch object")
        validate_v11_incident_attack_patch(value)
    overlay = patch.get("overlay", pristine["overlay"])
    successor = patch.get("successor", pristine["successor"])
    parents = patch.get("parents", pristine["parents"])
    result = patch.get("result", pristine["result"])
    registry = patch.get("registry", pristine["registry"])
    outer = patch.get("outer", pristine["outer"])
    manifest = patch.get("manifest", pristine["manifest"])
    authority_objects = patch.get("authority_objects", pristine["authority_objects"])

    for label, rows in (("overlay", overlay), ("successor", successor), ("parents", parents)):
        for row in rows:
            verify_row(row, "attack:" + label)
    verify_object(result, "attack result")
    verify_object(registry, "attack registry")
    verify_object(outer, "attack outer")
    validate_authority_objects(authority_objects)

    # Every mutated structure is fed back through the same independent exact
    # reconstruction and semantic validator used for the real candidate.
    need(overlay == expected["overlay"], "attack overlay reconstruction")
    need(successor == expected["successor"], "attack successor reconstruction")
    need(parents == expected["parents"], "attack parent reconstruction")
    state = {"overlay": overlay, "successor": successor, "parents": parents,
             "result": result, "registry": registry}
    compare(state, expected)
    validate_candidate_metadata(result, registry, outer, manifest,
                                pristine["raw_members"], expected)

    if "raw_overlay" in patch:
        need(gzip_rows(patch["raw_overlay"], "attacked overlay gzip") == overlay,
             "attacked overlay gzip rows")
    if "raw_successor" in patch:
        need(gzip_rows(patch["raw_successor"], "attacked successor gzip") == successor,
             "attacked successor gzip rows")
    if "raw_parents" in patch:
        need(gzip_rows(patch["raw_parents"], "attacked parent gzip") == parents,
             "attacked parent gzip rows")


def row_mutation(pristine: dict[str, Any], ledger: str, index: int,
                 path: tuple[str, ...], replacement: Any | None = None) -> dict[str, Any]:
    rows = list(pristine[ledger])
    row = copy.deepcopy(rows[index])
    target: Any = row
    for key in path:
        target = target[key]
    set_path(row, path, altered(target) if replacement is None else replacement)
    rows[index] = reclose_row(row)
    return {ledger: rows}


def object_mutation(pristine: dict[str, Any], key: str, path: tuple[str, ...],
                    replacement: Any | None = None) -> dict[str, Any]:
    value = copy.deepcopy(pristine[key])
    target: Any = value
    for item in path:
        target = target[item]
    set_path(value, path, altered(target) if replacement is None else replacement)
    return {key: reclose_object(value)}


def authority_mutation(pristine: dict[str, Any], authority: str,
                       path: tuple[str, ...], replacement: Any | None = None) -> dict[str, Any]:
    values = copy.deepcopy(pristine["authority_objects"])
    value = values[authority]
    target: Any = value
    for item in path:
        target = target[item]
    set_path(value, path, altered(target) if replacement is None else replacement)
    values[authority] = reclose_object(value)
    return {"authority_objects": values}


def make_attack_cases(pristine: dict[str, Any]) -> list[tuple[str, Any]]:
    overlay = pristine["overlay"]; successor = pristine["successor"]; parents = pristine["parents"]
    large_i = next(i for i, row in enumerate(overlay)
                   if row["terminal_authority"] == "C78L_VERIFIED_FINAL_SURFACE")
    singleton_i = next(i for i, row in enumerate(overlay)
                       if row["terminal_authority"] == "C78S_VERIFIED_FINAL_SURFACE")
    baseline_i = next(i for i, row in enumerate(successor)
                      if row["lineage_mode"] == "C72G_BASELINE_RETAINED")
    replacement_i = next(i for i, row in enumerate(successor)
                         if row["lineage_mode"] == "C79G_OVERLAY_REPLACEMENT")
    base_pair_i = next(i for i, row in enumerate(parents)
                       if row["parent_lineage_mode"] == "C72G_BASELINE_RETAINED")
    large_pair_i = next(i for i, row in enumerate(parents)
                        if row["parent_lineage_mode"] == "C78L_OVERLAY")
    singleton_pair_i = next(i for i, row in enumerate(parents)
                            if row["parent_lineage_mode"] == "C78S_OVERLAY")
    cases: list[tuple[str, Any]] = []

    def row_case(name: str, ledger: str, index: int, path: tuple[str, ...],
                 replacement: Any | None = None) -> None:
        cases.append((name, lambda ledger=ledger, index=index, path=path, replacement=replacement:
                      row_mutation(pristine, ledger, index, path, replacement)))

    for name, path in (
        ("overlay:leaf_ordinal_drift", ("leaf_ordinal",)),
        ("overlay:cell_id_drift", ("cell_id",)),
        ("overlay:C55A_row_drift", ("C55A_leaf_row_sha256",)),
        ("overlay:C55B_row_drift", ("C55B_cell_row_sha256",)),
        ("overlay:pair_index_drift", ("pair_index",)),
        ("overlay:component_index_drift", ("component_index",)),
        ("overlay:component_id_drift", ("component_id",)),
        ("overlay:partner_drift", ("reflection_partner_cell_id",)),
        ("overlay:authority_row_drift", ("terminal_authority_row_sha256",)),
        ("overlay:input_enum_drift", ("authority_input_enum",)),
        ("overlay:mapping_rule_drift", ("mapping_rule",)),
        ("overlay:terminal_drift", ("terminal_disposition",)),
        ("overlay:previous_reason_drift", ("previous_unresolved_reason",)),
        ("overlay:individual_credit_inflation", ("row_is_individually_creditable",)),
        ("overlay:installation_erasure", ("installed_atomically_only_by_C79g_completion",)),
        ("overlay:owner_closure_false", ("closure", "owner")),
        ("overlay:history_closure_false", ("closure", "history")),
        ("overlay:prefix_Kraft_false", ("closure", "prefix_Kraft")),
    ):
        row_case(name, "overlay", large_i, path)
    row_case("overlay:large_authority_swapped_to_singleton", "overlay", large_i,
             ("terminal_authority",), "C78S_VERIFIED_FINAL_SURFACE")
    row_case("overlay:singleton_authority_swapped_to_large", "overlay", singleton_i,
             ("terminal_authority",), "C78L_VERIFIED_FINAL_SURFACE")
    row_case("overlay:singleton_strict_plus_cemetery_mapped_typed", "overlay", singleton_i,
             ("terminal_disposition",), "TYPED_EVENT_GRAPH")

    for name, index, path in (
        ("successor:baseline_cell_id_join_erasure", baseline_i, ("cell_id",)),
        ("successor:baseline_C55A_lineage_drift", baseline_i, ("C55A_leaf_row_sha256",)),
        ("successor:baseline_disposition_mutation", baseline_i, ("successor_terminal_disposition",)),
        ("successor:baseline_authority_inflation", baseline_i, ("terminal_authority",)),
        ("successor:baseline_authority_row_drift", baseline_i, ("terminal_authority_row_sha256",)),
        ("successor:baseline_preservation_false", baseline_i, ("baseline_terminal_preserved_exactly",)),
        ("successor:baseline_mode_swap", baseline_i, ("lineage_mode",)),
        ("successor:overlay_cell_id_join_erasure", replacement_i, ("cell_id",)),
        ("successor:overlay_reference_erasure", replacement_i, ("overlay_row_sha256",)),
        ("successor:overlay_authority_row_erasure", replacement_i, ("terminal_authority_row_sha256",)),
        ("successor:overlay_authority_swap", replacement_i, ("terminal_authority",)),
        ("successor:overlay_disposition_mutation", replacement_i, ("successor_terminal_disposition",)),
        ("successor:unresolved_reintroduced", replacement_i, ("successor_unresolved_reason",)),
        ("successor:origin_key_drift", replacement_i, ("origin_key",)),
        ("successor:source_cell_lineage_drift", replacement_i, ("source_cell_row_sha256",)),
        ("successor:atomic_install_erasure", replacement_i, ("candidate_atomic_install_only",)),
    ):
        row_case(name, "successor", index, path)

    for name, index, path in (
        ("parent:pair_index_drift", base_pair_i, ("pair_index",)),
        ("parent:representative_drift", base_pair_i, ("representative_cell_id",)),
        ("parent:reflected_drift", base_pair_i, ("reflected_cell_id",)),
        ("parent:representative_C55B_drift", base_pair_i, ("representative_C55B_row_sha256",)),
        ("parent:reflected_C55B_drift", base_pair_i, ("reflected_C55B_row_sha256",)),
        ("parent:representative_successor_drift", base_pair_i, ("representative_successor_row_sha256",)),
        ("parent:reflected_successor_drift", base_pair_i, ("reflected_successor_row_sha256",)),
        ("parent:component_mixing", base_pair_i, ("component_indices",)),
        ("parent:authority_row_drift", large_pair_i, ("parent_authority_row_sha256",)),
        ("parent:large_authority_swap", large_pair_i, ("terminal_authority",)),
        ("parent:singleton_authority_swap", singleton_pair_i, ("terminal_authority",)),
        ("parent:reciprocity_break", large_pair_i, ("reciprocal_reflection_partner_identity_closed",)),
        ("parent:closure_false", large_pair_i, ("owner_history_glue_two_sides_incidence_closed",)),
        ("parent:prefix_free_false", large_pair_i, ("prefix_Kraft", "prefix_free")),
        ("parent:C42_parent_row_hash_drift", large_pair_i,
         ("prefix_Kraft", "C42_parent_row_sha256")),
        ("parent:C53_projection_hash_drift", large_pair_i,
         ("prefix_Kraft", "C53_parent_projection_object_sha256")),
        ("parent:C55B_crosswalk_hash_drift", singleton_pair_i,
         ("prefix_Kraft", "C55B_crosswalk_two_side_row_sha256s")),
        ("parent:unresolved_reintroduced", singleton_pair_i, ("unresolved_count",)),
    ):
        row_case(name, "parents", index, path)

    # Whole-ledger mutations exercise missing/duplicate/order guards after all
    # surviving rows retain valid individual row hashes.
    cases.extend([
        ("overlay:row_missing", lambda: {"overlay": overlay[:-1]}),
        ("overlay:row_duplicate", lambda: {"overlay": [*overlay, overlay[-1]]}),
        ("overlay:row_order_swap", lambda: {"overlay": [overlay[1], overlay[0], *overlay[2:]]}),
        ("successor:row_missing", lambda: {"successor": successor[:-1]}),
        ("successor:row_duplicate", lambda: {"successor": [*successor, successor[-1]]}),
        ("successor:row_order_swap", lambda: {"successor": [successor[1], successor[0], *successor[2:]]}),
        ("parent:row_missing", lambda: {"parents": parents[:-1]}),
        ("parent:row_duplicate", lambda: {"parents": [*parents, parents[-1]]}),
        ("parent:row_order_swap", lambda: {"parents": [parents[1], parents[0], *parents[2:]]}),
    ])

    def object_case(name: str, key: str, path: tuple[str, ...],
                    replacement: Any | None = None) -> None:
        cases.append((name, lambda key=key, path=path, replacement=replacement:
                      object_mutation(pristine, key, path, replacement)))

    for name, key, path in (
        ("result:public_global_unresolved_nonzero", "result", ("public_global_unresolved",)),
        ("result:derived_census_forgery", "result", ("derived_final_four_class_census", "EARLIEST_PREFIX_EXCLUDED")),
        ("result:hardcode_flag_forgery", "result", ("derived_final_four_class_census_was_not_hard_coded",)),
        ("result:baseline_count_drift", "result", ("baseline_retention", "retained_terminal_rows")),
        ("result:overlay_count_drift", "result", ("exact_overlay_partition", "total")),
        ("result:overlay_disjoint_false", "result", ("exact_overlay_partition", "sets_disjoint")),
        ("result:owner_false", "result", ("closure", "owner")),
        ("result:history_false", "result", ("closure", "history")),
        ("result:glue_false", "result", ("closure", "glue")),
        ("result:two_sides_false", "result", ("closure", "two_sides")),
        ("result:incidence_false", "result", ("closure", "incidence")),
        ("result:prefix_Kraft_false", "result", ("closure", "prefix_Kraft")),
        ("credit:candidate_formal_forgery", "result", ("candidate_credit", "formal_global_closure_credit")),
        ("credit:candidate_D02_unlock_forgery", "result", ("candidate_credit", "D02_unlock")),
        ("credit:D02_gate_forgery", "result", ("candidate_credit", "D02_gate_credit")),
        ("credit:D02_task_forgery", "result", ("candidate_credit", "D02_task_credit")),
        ("credit:D02_pending_reduction", "result", ("candidate_credit", "D02_formal_pending_task_count")),
        ("credit:D02_started_forgery", "result", ("D02_started",)),
        ("credit:precursor_C65_forgery", "result", ("precursor_credits", "C65_local_terminal_formal_credit")),
        ("authority:C55A_terminal_inflation", "result", ("authority_separation", "C55A")),
        ("authority:C55B_terminal_inflation", "result", ("authority_separation", "C55B")),
        ("authority:C72g_overlay_inflation", "result", ("authority_separation", "C72g")),
        ("authority:conditional_C3_promoted", "result", ("conditional_C3_promoted_to_actual_C3",)),
        ("authority:actual_C3_inflation", "result", ("actual_C3_disposition_count",)),
        ("publication:canonical_pointer_forgery", "result", ("canonical_pointer_written",)),
        ("registry:producer_opened", "registry",
         ("current_v16r2_producer_source_content_opened_or_read",)),
        ("registry:producer_executed", "registry",
         ("current_v16r2_producer_source_content_imported_compiled_or_executed",)),
        ("registry:C42_installed_authority_input_pin_drift", "registry",
         ("fixed_input_files", "DIRECT_KRAFT:C42_independent_audit", "file_sha256")),
        ("registry:D02_started", "registry", ("D02_started",)),
        ("publication:outer_not_last", "outer", ("candidate_outer_receipt_published_last",)),
        ("publication:terminal_replay_omission", "outer", ("terminal_byte_replay_required_after_outer_receipt",)),
        ("publication:outer_credit_forgery", "outer", ("candidate_credit", "formal_global_closure_credit")),
        ("publication:outer_manifest_drift", "outer", ("candidate_manifest_file_sha256",)),
    ):
        object_case(name, key, path)

    cases.extend([
        ("publication:manifest_overlay_hash_bitflip", lambda: {
            "manifest": {**pristine["manifest"], OVERLAY: "0" * 64}}),
        ("publication:manifest_successor_missing", lambda: {
            "manifest": {k: v for k, v in pristine["manifest"].items() if k != SUCCESSOR}}),
        ("publication:manifest_parent_hash_bitflip", lambda: {
            "manifest": {**pristine["manifest"], PARENTS: "0" * 64}}),
    ])

    def authority_case(name: str, authority: str, path: tuple[str, ...],
                       replacement: Any | None = None) -> None:
        cases.append((name, lambda authority=authority, path=path, replacement=replacement:
                      authority_mutation(pristine, authority, path, replacement)))

    for name, authority, path in (
        ("C78l:verification_status_forgery", "C78l_verification", ("status",)),
        ("C78l:producer_read_inflation", "C78l_verification",
         ("producer_was_not_opened_read_parsed_imported_executed_or_decoded",)),
        ("C78l:attack_count_reduction", "C78l_verification", ("self_test", "attack_count")),
        ("C78l:global_zero_inflation", "C78l_verification", ("public_global_unresolved_zero",)),
        ("C78s:verifier_source_pin_drift", "C78s_verification", ("verifier_file_sha256",)),
        ("C78s:build_byte_identity_false", "C78s_verification",
         ("candidate_base_bundle", "stage_a_stage_b_bytes_identical")),
        ("C78s:inode_distinctness_false", "C78s_verification",
         ("candidate_base_bundle", "stage_a_stage_b_inodes_distinct")),
        ("C78s:result_file_pin_drift", "C78s_verification",
         ("candidate_base_bundle", "result_file_sha256")),
        ("C78s:result_object_pin_drift", "C78s_verification",
         ("candidate_base_bundle", "result_object_sha256")),
        ("C78s:coherent_attack_count_reduction", "C78s_verification",
         ("coherent_attacks", "attack_count")),
        ("C78s:coherent_attack_rejected_mismatch", "C78s_verification",
         ("coherent_attacks", "rejected")),
        ("C78s:coherent_attack_name_reorder", "C78s_verification",
         ("coherent_attacks", "names")),
        ("C78s:final_verification_pin_drift", "C78s_final_outer", ("verification_file_sha256",)),
        ("C78s:final_verification_object_drift", "C78s_final_outer", ("verification_object_sha256",)),
        ("C78s:final_manifest_pin_drift", "C78s_final_outer", ("final_manifest_file_sha256",)),
        ("C78s:final_bytes_identity_false", "C78s_final_outer", ("all_final_stage_bytes_identical",)),
        ("C78s:final_terminal_replay_false", "C78s_final_outer",
         ("all_final_members_terminal_byte_replayed_in_both_stages",)),
        ("C78s:final_member_count_drift", "C78s_final_outer",
         ("terminal_byte_replay_member_count_per_stage",)),
    ):
        authority_case(name, authority, path)

    # Raw-byte attacks are decoded again by the strict one-member gzip parser.
    cases.extend([
        ("gzip:overlay_concatenated_member", lambda: {
            "raw_overlay": pristine["raw_overlay"] + pristine["raw_overlay"]}),
        ("gzip:successor_truncation", lambda: {
            "raw_successor": pristine["raw_successor"][:-1]}),
        ("gzip:parent_corruption", lambda: {
            "raw_parents": pristine["raw_parents"][:-8] + b"ATTACK!!"}),
    ])
    cases.extend([
        (V11_INCIDENT_ATTACK_NAMES[0], lambda: v11_incident_attack_mutation(
            ("v10_colon_prefix_witness", "exact_colon_prefix_join_count"), 0)),
        (V11_INCIDENT_ATTACK_NAMES[1], lambda: v11_incident_attack_mutation(
            ("v10_colon_prefix_witness",
             "exact_colon_prefixed_failure_label_literal_count"), 0)),
        (V11_INCIDENT_ATTACK_NAMES[2], lambda: v11_incident_attack_mutation(
            ("v10_colon_prefix_witness",
             "exact_unprefixed_failure_label_literal_count"), 1)),
        (V11_INCIDENT_ATTACK_NAMES[3], lambda: v11_incident_attack_mutation(
            ("v10_colon_prefix_witness",
             "exact_colon_prefixed_failure_label_literal_count"), 2)),
        (V11_INCIDENT_ATTACK_NAMES[4], lambda: v11_incident_attack_mutation(
            ("v10_colon_prefix_witness", "exact_colon_prefix_join_count"), 2)),
        (V11_INCIDENT_ATTACK_NAMES[5], lambda: v11_incident_attack_mutation(
            ("v10_colon_prefix_witness", "exact_colon_prefix_join_ast_sha256"),
            "0" * 64)),
        (V11_INCIDENT_ATTACK_NAMES[6], lambda: v11_incident_attack_mutation(
            ("v10_colon_prefix_witness", "equality_gate_count"), 1)),
        (V11_INCIDENT_ATTACK_NAMES[7], lambda: v11_incident_attack_mutation(
            ("v10_colon_prefix_witness", "expanded_structural_dict_count"), 2)),
        (V11_INCIDENT_ATTACK_NAMES[8], lambda: v11_incident_attack_mutation(
            ("v10_colon_prefix_witness",
             "direct_top_level_hold_regression_call_count"), 0)),
        (V11_INCIDENT_ATTACK_NAMES[9], lambda: v11_incident_attack_mutation(
            ("v10_colon_prefix_witness", "hold_precedes_stage"), False)),
        (V11_INCIDENT_ATTACK_NAMES[10], lambda: v11_incident_attack_mutation(
            ("v10_colon_prefix_witness", "direct_top_level_build_stage_call_count"),
            2)),
        (V11_INCIDENT_ATTACK_NAMES[11], lambda: v11_incident_attack_mutation(
            ("inherited_held_fd_revalidation",
             "all_five_inherited_descriptors_revalidated_before_incident_authority"),
            False)),
        (V11_INCIDENT_ATTACK_NAMES[12], lambda: v11_incident_attack_mutation(
            ("three_independent_helper_normalized_ast_sha256",), "0" * 64)),
        (V11_INCIDENT_ATTACK_NAMES[13], lambda: v11_incident_attack_mutation(
            ("v10_colon_prefix_witness", "successor_clause_truth_vector"),
            [True] * 14 + [False])),
        (V11_INCIDENT_ATTACK_NAMES[14], lambda: v11_incident_attack_mutation(
            ("v11_official_rejection_closure", "positive_or_stage_surface_count"),
            1)),
        (V11_INCIDENT_ATTACK_NAMES[15], lambda: v11_incident_attack_mutation(
            ("v10_colon_prefix_witness",
             "zero_or_multiple_expanded_dicts_controlled_reject"), False)),
    ])
    return cases


def attack_validator_route(name: str) -> str:
    family = name.split(":", 1)[0]
    if family in {"overlay", "successor", "parent"}:
        return "ROW_CLOSURE_THEN_INDEPENDENT_EXACT_RECONSTRUCTION"
    if family in {"result", "credit", "registry"}:
        return "CANDIDATE_METADATA_PRODUCTION_VALIDATOR"
    if family in {"authority", "C78l", "C78s"}:
        return "PINNED_AUTHORITY_PRODUCTION_SEMANTIC_VALIDATOR"
    if family == "publication":
        return "MANIFEST_OUTER_OBJECT_CHAIN_PRODUCTION_VALIDATOR"
    if family == "gzip":
        return "STRICT_SINGLE_MEMBER_GZIP_PRODUCTION_VALIDATOR"
    if family == "v11incident":
        return "INHERITED_HELD_FD_AND_EXACT_PER_CLAUSE_WITNESS_PRODUCTION_VALIDATOR"
    raise Reject("unknown attack family:" + family)


def run_attacks(pristine: dict[str, Any], expected: dict[str, Any]) -> dict[str, dict[str, str]]:
    cases = make_attack_cases(pristine)
    names = [name for name, _ in cases]
    need(len(cases) == 137 and len(set(names)) == 137 and
         _line_sequence_sha256(names) == ATTACK_NAME_ORDER_PIN,
         "exact 137 unique ordered actual attacks")
    results: dict[str, dict[str, str]] = {}
    for name, create_patch in cases:
        patch = create_patch()
        need(isinstance(patch, dict) and len(patch) > 0,
             "nonempty actual attack patch:" + name)
        try:
            validate_attack_patch(patch, pristine, expected)
        except Reject as exc:
            results[name] = {
                "status": "FAIL_CLOSED",
                "validator_route": attack_validator_route(name),
                "actual_rejection_stage": str(exc),
            }
        else:
            raise Reject("actual structural attack accepted:" + name)
    return results


def construct_expected_verification(
        actual: dict[str, Any], expected: dict[str, Any],
        attacks: dict[str, dict[str, str]], self_file_sha256: str,
        producer_file_sha256: str,
        member_hashes: Mapping[str, str]) -> dict[str, Any]:
    """Canonical zero-credit object shared by verify, assemble, and authorize."""
    census = dict(expected["census"])
    census["total"] = sum(census.values())
    attack_names = list(attacks)
    return close_object({
        "schema": SCHEMA + ".independent-verification",
        "status": "PASS_INDEPENDENT_C79G_V16R2__EXACT_137_ATTACKS__STANDALONE_ZERO_CREDIT",
        "verifier_file_sha256": self_file_sha256,
        "declared_producer_file_sha256": producer_file_sha256,
        "producer_hash_is_declarative_binding_only": True,
        "producer_source_content_opened_read_decoded_parsed_compiled_imported_or_executed": False,
        "verification_orientation_is_order_invariant": True,
        "candidate_member_file_sha256": dict(member_hashes),
        "dual_candidate_build_directories_mode": actual["dual_candidate_build_directories_mode"],
        "dual_candidate_members_mode": actual["dual_candidate_members_mode"],
        "dual_candidate_members_single_link": actual["dual_candidate_members_single_link"],
        "dual_candidate_members_byte_identical": actual["dual_candidate_members_byte_identical"],
        "dual_candidate_corresponding_inodes_distinct":
            actual["dual_candidate_corresponding_inodes_distinct"],
        "all_18_candidate_member_identities_globally_unique": True,
        "reconstruction": {
            "overlay_rows": len(expected["overlay"]),
            "successor_rows": len(expected["successor"]),
            "reflection_parent_rows": len(expected["parents"]),
            "derived_final_four_class_census": census,
            "authority_partition": expected["modes"],
            "public_global_unresolved": 0,
            "closure": dict(CLOSURE),
            "C42_C53_C55B_direct_Kraft_pair_count": PAIR_COUNT,
        },
        "coherent_attacks": {
            "attack_count": len(attacks),
            "rejected": sum(record["status"] == "FAIL_CLOSED"
                            for record in attacks.values()),
            "names": attack_names,
            "name_order_sha256": _line_sequence_sha256(attack_names),
            "records": attacks,
        },
        "all_attacks_fail_closed":
            all(record.get("status") == "FAIL_CLOSED" for record in attacks.values()),
        "v3_official_later_rejection_object_sha256": V3_OFFICIAL_REJECTION_OBJECT_PIN,
        "verification_credit": dict(ZERO),
        "standalone_non_authoritative": True,
        "formal_credit_authority":
            "ONLY_EXTERNALLY_PINNED_COLD_LAUNCHER_WRAPPER_AFTER_HELD_CHILD_AND_POST_CHILD_TERMINAL_REPLAY",
        "precursor_credits_zero": True,
        "canonical_pointer_written": False,
        "D02_started": False,
    })


def reconstruct_publication_context(
        primary: Path, peer: Path, self_guard: HeldSelf,
        producer_guard: HeldOpaqueMetadata,
        candidate_guard: HeldInputSet,
        c78_guard: HeldInputSet,
        c42_guard: HeldInputSet,
        fixed_guard: HeldInputSet,
        policy_guard: HeldInputSet,
        v3_guard: HeldInputSet,
        v3_source_metadata: list[HeldOpaqueMetadata],
        v4_guard: HeldInputSet,
        v4_source_metadata: list[HeldOpaqueMetadata],
        v5_guard: HeldInputSet,
        v5_source_metadata: list[HeldOpaqueMetadata],
        v6_guard: HeldInputSet,
        v6_source_metadata: list[HeldOpaqueMetadata],
        v7_guard: HeldInputSet,
        v7_source_metadata: list[HeldOpaqueMetadata],
        v8_guard: HeldInputSet,
        v8_source_metadata: list[HeldOpaqueMetadata],
        v9_guard: HeldInputSet,
        v9_source_metadata: list[HeldOpaqueMetadata],
        v10_guard: HeldInputSet,
        v10_source_metadata: list[HeldOpaqueMetadata],
        v11_guard: HeldInputSet,
        v11_source_metadata: list[HeldOpaqueMetadata]) -> dict[str, Any]:
    evidence = read_evidence(
        self_guard, producer_guard,
        c78_guard, c42_guard, fixed_guard, policy_guard,
        v3_guard, v3_source_metadata, v4_guard, v4_source_metadata,
        v5_guard, v5_source_metadata, v6_guard, v6_source_metadata,
        v7_guard, v7_source_metadata, v8_guard, v8_source_metadata,
        v9_guard, v9_source_metadata, v10_guard, v10_source_metadata,
        v11_guard, v11_source_metadata)
    expected = reconstruct_expected(evidence)
    actual = candidate(primary, peer, candidate_guard)
    compare(actual, expected)
    validate_candidate_metadata(actual["result"], actual["registry"], actual["outer"],
                                actual["manifest"], actual["raw"], expected)
    attacks = run_attacks(attack_model(actual, evidence), expected)
    member_hashes = {name: sha(actual["raw"][name]) for name in sorted(MEMBERS)}
    verification = construct_expected_verification(
        actual, expected, attacks, self_guard.file_sha256,
        PRODUCER_SOURCE_PIN, member_hashes)
    return {
        "evidence": evidence,
        "expected": expected,
        "actual": actual,
        "attacks": attacks,
        "verification": verification,
        "verification_raw": canonical(verification) + b"\n",
    }


def _static_policy_guards() -> HeldInputSet:
    return HeldInputSet([
        HeldPinnedInput(
            V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT,
            "v14 supersession receipt current exact8 first member", 0o444,
            V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT_FILE_PIN),
        HeldPinnedInput(CLOSED_SCHEMA, "v16r2 closed schema", 0o444,
                        CLOSED_SCHEMA_FILE_PIN),
        HeldPinnedInput(CONTRACT, "v16r2 contract", 0o444, CONTRACT_FILE_PIN),
        HeldPinnedInput(
            V16_TO_V16R2_TRANSITION,
            "post-source v16-to-v16r2 transition receipt", 0o444),
        HeldPinnedInput(STATIC_AUDIT_V16R2, "post-source v16r2 static audit", 0o444),
        HeldPinnedInput(COLD_LAUNCHER, "frozen cold launcher", 0o444),
        HeldPinnedInput(COLD_LAUNCH_MANIFEST,
                        "frozen cold-launch exact8 manifest", 0o444),
        HeldPinnedInput(COLD_LAUNCH_OUTER,
                        "frozen cold-launch outer-last receipt", 0o444),
    ], [])


def _expected_frozen_v3_exact10() -> list[dict[str, Any]]:
    expected: list[dict[str, Any]] = []
    for name in V3_EXACT10_ORDER:
        path, file_sha256 = V3_FROZEN_FILES[name]
        entry: dict[str, Any] = {
            "name": name,
            "path": str(path.relative_to(ROOT)),
            "file_sha256": file_sha256,
        }
        if name in V3_FROZEN_OBJECTS:
            entry["object_sha256"] = V3_FROZEN_OBJECTS[name]
        expected.append(entry)
    return expected


def _expected_historical_mode_contract() -> dict[str, str]:
    return {
        "C55A_leaf_ledger": "0444", "C55A_result": "0444",
        "C55A_verification": "0444", "C55A_manifest": "0664",
        "C55B_cells": "0664", "C55B_edges": "0664",
        "C55B_components": "0664", "C55B_result": "0664",
        "C55B_verification": "0664", "C55B_self_test": "0664",
        "C55B_manifest": "0664", "C72_contract": "0664",
        "C72_verification": "0644", "C72_self_test": "0644",
        "C72_manifest": "0644", "C72_outer": "0644",
        "C72_head": "0444",
    }


def _validate_contract_bindings(contract: Mapping[str, Any]) -> None:
    verify_object(contract, "live v16r2 contract", CONTRACT_OBJECT_PIN)
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
             "STATIC_CONTRACT_BYTES_FINAL__COLD_FREEZE_PENDING__RUNTIME_NOT_AUTHORIZED",
         "contract exact effective checkpoint and honest pre-freeze status")
    paths = contract.get("exact_publication_paths")
    need(isinstance(paths, dict), "contract exact publication paths object")
    expected_paths = {
        "candidate_A": str(CANDIDATE_A.relative_to(ROOT)),
        "candidate_B": str(CANDIDATE_B.relative_to(ROOT)),
        "verification_A": str(VERIFICATION_A.relative_to(ROOT)),
        "verification_B": str(VERIFICATION_B.relative_to(ROOT)),
        "committed_completion": str(COMMITTED_COMPLETION.relative_to(ROOT)),
        "authority_seal": str(AUTHORITY_SEAL.relative_to(ROOT)),
        "v16r2_rejection_namespace": str(REJECTION_NAMESPACE.relative_to(ROOT)),
        "v16r2_later_rejection": str(LATER_REJECTION.relative_to(ROOT)),
        "candidate_staging_path_template":
            ".cm2-runtime/.c79g-v16r2r63y-candidate-stage-{a|b}-" +
            UPSTREAM_CHECKPOINT_OBJECT_PIN,
        "verification_staging_path_template":
            ".cm2-runtime/.c79g-v16r2r63y-verification-stage-{a|b}-" +
            UPSTREAM_CHECKPOINT_OBJECT_PIN,
        "completion_staging_path": str(COMPLETION_STAGE.relative_to(ROOT)),
        "authority_staging_path": str(AUTHORITY_STAGE.relative_to(ROOT)),
    }
    need(all(paths.get(name) == value for name, value in expected_paths.items()),
         "contract equals every fixed target and deterministic source-stage path")
    predecessor = contract.get("append_only_predecessor_v3")
    need(isinstance(predecessor, dict) and
         predecessor.get("ordered_exact10") == _expected_frozen_v3_exact10(),
         "contract exact ordered predecessor-v3 exact10")
    rejection = predecessor.get("official_later_rejection")
    need(isinstance(rejection, dict) and
         rejection.get("path") == str(V3_OFFICIAL_REJECTION.relative_to(ROOT)) and
         rejection.get("namespace_path") ==
             str(V3_OFFICIAL_REJECTION.parent.relative_to(ROOT)) and
         rejection.get("file_sha256") == V3_OFFICIAL_REJECTION_FILE_PIN and
         rejection.get("object_sha256") == V3_OFFICIAL_REJECTION_OBJECT_PIN and
         rejection.get("schema") ==
             "cm2.round306c79g.true-global-no-producer-consumer.v3.later-rejection" and
         rejection.get("status") ==
             "PERMANENT_FAIL_CLOSED_REJECTION__ZERO_CREDIT" and
         rejection.get("reason") ==
             "ORPHANED_OR_INCOMPLETE_C79G_V3_SURFACE" and
         rejection.get("namespace_mode") == "0555" and
         rejection.get("namespace_nlink") == 2 and
         rejection.get("exact_member_universe") == ["rejection.json"] and
         rejection.get("member_mode") == "0444" and
         rejection.get("member_nlink") == 1 and
         rejection.get("formal_global_closure_credit") == 0 and
         rejection.get("D02_unlock") is False and
         rejection.get("D02_started") is False and
         rejection.get("overwrite_delete_or_reuse_allowed") is False and
         predecessor.get("execution_allowed") is False and
         predecessor.get("runtime_surfaces_authoritative") is False and
         predecessor.get(
             "launcher_must_hold_exact10_plus_official_rejection_namespace_under_one_lock") is True and
         predecessor.get("official_rejection_is_strictly_later_than_v3_cold_outer") is True and
         predecessor.get("official_rejection_chronology_required") ==
             "MAX_V3_OUTER_MTIME_CTIME_LT_MIN_REJECTION_MTIME_CTIME",
         "contract exact v3 exact10 and official later-rejection binding")
    rejected_v4 = contract.get("rejected_unpublished_predecessor_v4")
    v4_supersession = (rejected_v4.get("supersession_receipt")
                       if isinstance(rejected_v4, dict) else None)
    need(isinstance(rejected_v4, dict) and isinstance(v4_supersession, dict) and
         v4_supersession.get("path") ==
             str(V4_REJECTION_SUPERSESSION.relative_to(ROOT)) and
         v4_supersession.get("file_sha256") ==
             V4_REJECTION_SUPERSESSION_FILE_PIN and
         v4_supersession.get("object_sha256") ==
             V4_REJECTION_SUPERSESSION_OBJECT_PIN and
         rejected_v4.get("frozen_member_count_including_shared_v3_official_rejection") == 8 and
         rejected_v4.get("all_eight_regular_0444_nlink1") is True and
         rejected_v4.get("v4_files_modified_by_v6") is False and
         rejected_v4.get("v4_execution_allowed") is False and
         rejected_v4.get("v4_runtime_surfaces_authoritative") is False and
         rejected_v4.get("v4_manifest_must_remain_absent") is True and
         rejected_v4.get("v4_outer_must_remain_absent") is True and
         rejected_v4.get("v4_runtime_artifact_count") == 0 and
         rejected_v4.get("v4_credit_transferred") == 0 and
         rejected_v4.get("consumer_may_read_v4_producer_consumer_or_launcher_source_content") is False and
         rejected_v4.get("overwrite_delete_reuse_complete_or_promote_v4_allowed") is False,
         "contract exact rejected-unpublished v4 supersession binding")
    published_v5 = contract.get(
        "published_then_officially_rejected_predecessor_v5")
    need(published_v5 == _expected_published_then_rejected_v5_proof(),
         "contract exact published-then-officially-rejected v5 binding")
    published_v6 = contract.get(
        "published_then_officially_rejected_predecessor_v6")
    need(published_v6 == _expected_published_then_rejected_v6_proof(),
         "contract exact published-then-officially-rejected v6 binding")
    published_v7 = contract.get(
        "published_then_officially_rejected_predecessor_v7")
    need(published_v7 == _expected_published_then_rejected_v7_proof() and
         published_v7.get("publication_lock_continuity_incident") ==
             _validated_v7_publication_lock_continuity_incident(),
         "contract exact interrupted-and-officially-rejected v7 binding")
    published_v8 = contract.get(
        "published_then_officially_rejected_predecessor_v8")
    need(published_v8 == _expected_published_then_rejected_v8_proof(),
         "contract exact pre-stage-failed-and-officially-rejected v8 binding")
    published_v9 = contract.get(
        "published_then_officially_rejected_predecessor_v9")
    need(published_v9 == _expected_published_then_rejected_v9_proof(),
         "contract exact pre-child-shape-drift-and-officially-rejected v9 binding")
    published_v10 = contract.get(
        "published_then_officially_rejected_predecessor_v10")
    need(published_v10 == _expected_published_then_rejected_v10_proof(),
         "contract exact label-prefix-regression-and-officially-rejected v10 binding")
    published_v11 = contract.get(
        "published_then_officially_rejected_predecessor_v11")
    published_v12 = contract.get(
        "published_then_officially_rejected_predecessor_v12")
    rejected_v13 = contract.get(
        "rejected_prepublication_v13_supersession_receipt")
    need(published_v11 == _expected_published_then_rejected_v11_proof() and
         published_v12 == _expected_published_then_rejected_v12_proof() and
         rejected_v13 ==
             expected_rejected_prepublication_v13_supersession_receipt() and
         contract.get("v10_colon_prefix_witness") == V10_COLON_PREFIX_WITNESS and
         contract.get("v11_dual_validator_divergence_incident") ==
             V11_DUAL_VALIDATOR_DIVERGENCE_INCIDENT,
         "contract exact v11/v12/v13/v14 rejection/supersession binding")
    bundle = contract.get("v16r2_bundle")
    expected_base7_paths = [
            str(V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT.relative_to(ROOT)),
            str(CLOSED_SCHEMA.relative_to(ROOT)), str(CONTRACT.relative_to(ROOT)),
            str(PRODUCER_SOURCE.relative_to(ROOT)), str(SELF.relative_to(ROOT)),
            str(V16_TO_V16R2_TRANSITION.relative_to(ROOT)),
            str(STATIC_AUDIT_V16R2.relative_to(ROOT)),
        ]
    expected_exact8_paths = [
        *expected_base7_paths, str(COLD_LAUNCHER.relative_to(ROOT))]
    expected_exact10_paths = [
        *expected_exact8_paths,
        str(COLD_LAUNCH_MANIFEST.relative_to(ROOT)),
        str(COLD_LAUNCH_OUTER.relative_to(ROOT)),
    ]
    receipts = (bundle.get("post_source_static_trust_receipts", {})
                if isinstance(bundle, dict) else {})
    need(isinstance(bundle, dict) and
         bundle.get("base7_ordered_paths") == expected_base7_paths and
         bundle.get("exact8_ordered_paths") == expected_exact8_paths and
         bundle.get("exact10_ordered_paths") == expected_exact10_paths and
         bundle.get("closed_schema", {}).get("path") ==
             str(CLOSED_SCHEMA.relative_to(ROOT)) and
         bundle.get("closed_schema", {}).get("file_sha256") ==
             CLOSED_SCHEMA_FILE_PIN and
         bundle.get("closed_schema_validator_policy") == {
             "unsupported_validation_keyword_action": "FAIL_CLOSED",
             "runtime_validator_walks_complete_schema_keyword_universe": True,
             "oneOf_keyword_allowed": False,
             "file_and_object_pin_definitions_are_split_closed_types": True,
             "all_closed_object_required_sets_equal_property_sets": True,
             "static_audit_must_pin_actual_and_supported_keyword_universes": True,
         } and
         bundle.get("contract", {}).get("path") ==
             str(CONTRACT.relative_to(ROOT)) and
         bundle.get("build_only_producer", {}).get("path") ==
             str(PRODUCER_SOURCE.relative_to(ROOT)) and
         bundle.get("independent_verifier_assembler_authority_consumer", {}).get("path") ==
             str(SELF.relative_to(ROOT)) and
         receipts.get(
             "v16_to_v16r2_transition_path") ==
             str(V16_TO_V16R2_TRANSITION.relative_to(ROOT)) and
         receipts.get("static_audit_path") ==
             str(STATIC_AUDIT_V16R2.relative_to(ROOT)) and
         receipts.get("v14_official_rejection_path") ==
             V14_OFFICIAL_REJECTION_RELATIVE_PATH and
         receipts.get(
             "v14_registry_shape_drift_supersession_receipt_path") ==
             str(V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT.
                 relative_to(ROOT)) and
         receipts.get(
             "runtime_consumer_must_hold_strict_parse_object_close_and_"
             "terminally_replay_inherited_v14_exact12") is True,
         "contract exact acyclic v16r2 bundle and post-source trust-anchor paths")
    full10 = contract.get("full10_direct_prefix_Kraft_identity")
    upstream = contract.get("upstream_branch_held_input_protocol")
    need(isinstance(full10, dict) and isinstance(upstream, dict) and
         full10.get("ordered_expected_modes") == [
             "0664", "0664", "0664", "0600", "0444",
             "0444", "0444", "0444", "0664", "0444"] and
         full10.get("C42_candidate_directory_expected_mode") == "0755" and
         full10.get("C42_candidate_directory_expected_nlink") == 2 and
         full10.get("C42_candidate_exact9_member_expected_mode") == "0664" and
         full10.get("C42_candidate_exact9_member_expected_nlink") == 1 and
         full10.get("C42_held_directory_count") == 3 and
         full10.get("C42_independent_audit_parent_directory_expected_mode") == "0700" and
         full10.get("C42_independent_audit_parent_directory_expected_nlink") == 2 and
         full10.get("C42_independent_audit_parent_directory_exact_member_count") == 1 and
         full10.get("C42_independent_audit_file_expected_mode") == "0600" and
         full10.get("C42_installation_parent_directory_expected_mode") == "0500" and
         full10.get("C42_installation_parent_directory_expected_nlink") == 2 and
         full10.get("C42_installation_parent_directory_exact_member_count") == 1 and
         full10.get("C42_installation_receipt_expected_mode") == "0444" and
         full10.get(
             "all_three_C42_directories_held_from_initial_validation_through_terminal_replay") is True and
         upstream.get("historical_fixed_file_expected_modes") ==
             _expected_historical_mode_contract() and
         upstream.get("C55B_manifest_chronology_claim") ==
             "NO_POST_VERIFICATION_OR_OUTER_LAST_CLAIM; MANIFEST_MTIME_PRECEDES_VERIFICATION_AND_SELF_TEST" and
         upstream.get("C72_observed_chronology") ==
             "CONTRACT_LT_VERIFICATION_LT_SELF_TEST_LT_MANIFEST_LT_OUTER" and
         upstream.get(
             "modes_are_exact_observed_snapshot_guards_not_immutability_or_read_only_claims") is True,
         "contract exact historical per-path mode and chronology policy")


def _need_exact_audit_bool(
        value: Mapping[str, Any], key: str, expected: bool,
        label: str) -> None:
    observed = value.get(key)
    need(type(observed) is bool and observed is expected,
         label + ":exact bool:" + key)


def _schema_static_counts(value: Mapping[str, Any]) -> tuple[int, int, int, int]:
    definitions = value.get("$defs")
    need(isinstance(definitions, dict), "final schema audit:$defs object")
    reference_count = 0
    closed_object_count = 0
    mismatch_count = 0
    stack: list[Any] = [value]
    while stack:
        current = stack.pop()
        if isinstance(current, dict):
            if "$ref" in current:
                reference_count += 1
            if (current.get("type") == "object" and
                    current.get("additionalProperties") is False):
                closed_object_count += 1
                if set(current.get("required", [])) != set(
                        current.get("properties", {})):
                    mismatch_count += 1
            stack.extend(current.values())
        elif isinstance(current, list):
            stack.extend(current)
    return len(definitions), reference_count, closed_object_count, mismatch_count


def _validate_final_static_audit(
        audit: Mapping[str, Any], closed_schema: Mapping[str, Any],
        self_guard: HeldSelf, transition_file_sha256: str,
        transition_object_sha256: str) -> None:
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
             "rejected_prepublication_v13_supersession_receipt",
             "published_then_officially_rejected_predecessor_v14",
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
             UPSTREAM_CHECKPOINT_OBJECT_PIN and
         audit.get("published_then_officially_rejected_predecessor_v12") ==
             _expected_published_then_rejected_v12_proof() and
         audit.get("rejected_prepublication_v13_supersession_receipt") ==
             expected_rejected_prepublication_v13_supersession_receipt() and
         audit.get("published_then_officially_rejected_predecessor_v14") ==
             expected_published_then_rejected_v14_summary(),
         "final v16r2 static audit exact top-level PASS_V16R2 closure")
    dual = audit.get("dual_independent_static_checkers", {})
    acceptance = audit.get("final_audit_acceptance")
    attacks = audit.get("coherent_attack_static_census")
    closure = audit.get("schema_and_constructor_closure")
    sealed = audit.get("sealed_exec_and_no_producer_static_proof")
    need(isinstance(dual, dict) and isinstance(acceptance, dict) and
         isinstance(attacks, dict) and isinstance(closure, dict) and
         isinstance(sealed, dict),
         "final static audit exact dual/acceptance/attack/schema objects")
    need(set(dual) == {
             "checker_A", "checker_B",
             "checker_C_common_census_and_pin_normalized_ast_reproduction",
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
             "v10_colon_prefix_helper_consensus",
             "actual_runtime_registry_shape_evidence",
         }, "final v16r2 static audit dual-checker exact16 closure")
    checker_a = dual.get("checker_A", {})
    checker_b = dual.get("checker_B", {})
    checker_c = dual.get(
        "checker_C_common_census_and_pin_normalized_ast_reproduction", {})
    helper_consensus = dual.get("v10_colon_prefix_helper_consensus", {})
    runtime_registry_evidence = dual.get(
        "actual_runtime_registry_shape_evidence", {})
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
         } and
         isinstance(runtime_registry_evidence, dict) and
         set(runtime_registry_evidence) == {
             "producer_source_registry_census",
             "launcher_runtime_registry_helper_census",
             "runtime_registry_shape_consensus",
             "explicit62_in_memory_tamper_rejected",
             "actual_closed_registry_shape",
         }, "final v16r2 checker A/B/C and helper-consensus exact object closures")
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
    need(helper_consensus == {
             "algorithm":
                 "THREE_SOURCE_NORMALIZED_FUNCTIONDEF_AST_AND_EXACT_CALLSITE_CENSUS_V1",
             "implementation_count": 3,
             "ordered_source_roles": ["producer", "consumer", "launcher"],
             "normalized_helper_ast_sha256":
                 V10_COLON_PREFIX_WITNESS_HELPER_AST_SHA256,
             "all_three_helpers_equal": True,
             "witness_exact_key_order":
                 list(V10_COLON_PREFIX_WITNESS_KEY_ORDER),
             "witness_exact_key_count": 40,
             "witness_object_sha256":
                 V10_COLON_PREFIX_WITNESS["object_sha256"],
             "ordered_callsite_census": expected_helper_callsites,
             "ordered_callsite_census_sha256":
                 "1ca6de98366645a520cbc604990d71197f039207cacfa3291e9d87ff09a3cf57",
             "all_callsites_exact": True,
         } and
         digest(expected_helper_callsites) ==
             "1ca6de98366645a520cbc604990d71197f039207cacfa3291e9d87ff09a3cf57",
         "final v16r2 exact three-helper AST/key-order/callsite consensus")
    producer_registry_census = runtime_registry_evidence.get(
        "producer_source_registry_census", {})
    launcher_registry_census = runtime_registry_evidence.get(
        "launcher_runtime_registry_helper_census", {})
    registry_consensus = runtime_registry_evidence.get(
        "runtime_registry_shape_consensus", {})
    execution_proof_exact7 = [
        "producer_exec_fd_is_fresh_sealed_memfd",
        "producer_exec_fd_distinct_from_installed_source_fd",
        "producer_exec_memfd_required_seals_valid",
        "producer_exec_bytes_equal_installed_source_bytes",
        "producer_exec_and_installed_source_terminal_replayed",
        "twelve_v14_inherited_authority_inputs_inherited_as_held_fds",
        "twelve_v14_inherited_authority_held_fds_path_identity_mount_and_hash_revalidated",
    ]
    need(set(producer_registry_census) == {
             "close_object_semantics",
             "explicit_key_count", "explicit_unique_key_count",
             "explicit_sorted_key_array_sha256",
             "unsupported_explicit_key_count",
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
             "object_closure_field_count",
             "object_sha256_absent_before_closure",
             "registry_return_is_direct_terminal",
             "computed_closed_registry_key_count", "matches"} and
         producer_registry_census.get("explicit_key_count") == 67 and
         producer_registry_census.get("explicit_unique_key_count") == 67 and
         _nonzero_sha256(producer_registry_census.get(
             "explicit_sorted_key_array_sha256")) and
         producer_registry_census.get("unsupported_explicit_key_count") == 0 and
         _nonzero_sha256(producer_registry_census.get(
             "explicit_ordered_key_array_sha256")) and
         producer_registry_census.get("execution_proof_key_count") == 7 and
         producer_registry_census.get("execution_proof_unique_key_count") == 7 and
         producer_registry_census.get("execution_proof_unsupported_key_count") == 0 and
         producer_registry_census.get("execution_proof_keys") ==
             execution_proof_exact7 and
         producer_registry_census.get(
             "execution_proof_return_is_direct_terminal") is True and
         producer_registry_census.get(
             "execution_proof_values_all_literal_true") is True and
         producer_registry_census.get(
             "execution_proof_expansion_exact_once") is True and
         producer_registry_census.get(
             "explicit_and_execution_proof_keysets_disjoint") is True and
         producer_registry_census.get(
             "in_memory_close_object_field_tamper_rejected") is True and
         producer_registry_census.get(
             "in_memory_explicit_proof_overlap_rejected") is True and
         producer_registry_census.get(
             "in_memory_nonstring_proof_key_rejected") is True and
         producer_registry_census.get(
             "in_memory_preclosure_object_sha256_rejected") is True and
         producer_registry_census.get("object_closure_field_count") == 1 and
         producer_registry_census.get(
             "object_sha256_absent_before_closure") is True and
         producer_registry_census.get(
             "registry_return_is_direct_terminal") is True and
         producer_registry_census.get("computed_closed_registry_key_count") == 75 and
         producer_registry_census.get("matches") is True,
         "final v16r2 producer actual source-registry exact75 census")
    close_semantics = producer_registry_census.get("close_object_semantics", {})
    need(set(close_semantics) == {
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
         _nonzero_sha256(close_semantics.get(
             "normalized_close_object_ast_sha256")) and
         close_semantics.get(
             "object_sha256_is_digest_of_unclosed_input") is True and
         close_semantics.get(
             "object_sha256_literal_field_exact_once") is True and
         close_semantics.get("single_positional_parameter") is True and
         close_semantics.get("matches") is True,
         "final v16r2 producer close_object exact semantics")
    need(set(launcher_registry_census) == {
             "normalized_helper_ast_sha256", "explicit_key_guard_literals",
             "expected_normalized_helper_ast_sha256",
             "exact_single_raw_parameter",
             "stale_literal_62_count", "exact_execution_proof_7_guard_count",
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
             "in_memory_stale_62_rejected", "matches"} and
         _nonzero_sha256(launcher_registry_census.get(
             "normalized_helper_ast_sha256")) and
         launcher_registry_census.get("expected_normalized_helper_ast_sha256") ==
             launcher_registry_census.get("normalized_helper_ast_sha256") and
         launcher_registry_census.get("exact_single_raw_parameter") is True and
         launcher_registry_census.get("explicit_key_guard_literals") == [67] and
         launcher_registry_census.get("stale_literal_62_count") == 0 and
         launcher_registry_census.get(
             "exact_execution_proof_7_guard_count") == 1 and
         launcher_registry_census.get(
             "exact_execution_proof_expansion_guard_count") == 1 and
         launcher_registry_census.get(
             "shape_formula_is_len_explicit_plus_len_proof_plus_one") is True and
         launcher_registry_census.get("return_is_computed_shape") is True and
         launcher_registry_census.get("exact_shape_75_guard_count") == 1 and
         launcher_registry_census.get("nested_helper_scope_count") == 0 and
         launcher_registry_census.get(
             "normalized_helper_semantics_match_reviewed_template") is True and
         launcher_registry_census.get("live_callsite_count") == 1 and
         launcher_registry_census.get("live_callsite_owner") ==
             "validate_final_static_audit" and
         launcher_registry_census.get(
             "live_callsite_is_direct_assignment") is True and
         launcher_registry_census.get(
             "live_callsite_uses_held_producer_raw") is True and
         launcher_registry_census.get(
             "live_computed_shape_consumed_by_expected_shapes_then_75_gate")
             is True and
         launcher_registry_census.get(
             "live_consumption_is_direct_need_gate") is True and
         launcher_registry_census.get(
             "held_producer_independent_computed_shape") == 75 and
         launcher_registry_census.get(
             "in_memory_dead_callsite_mutation_count") == 1 and
         launcher_registry_census.get(
             "in_memory_dead_callsite_rejected") is True and
         launcher_registry_census.get(
             "in_memory_stale_62_mutation_count") == 1 and
         launcher_registry_census.get("in_memory_stale_62_rejected") is True and
         launcher_registry_census.get("matches") is True,
         "final v16r2 launcher actual runtime-registry helper census")
    need(set(registry_consensus) == {
             "producer_independent_closed_key_count",
             "launcher_actual_runtime_helper_matches",
             "source_declared_producerSourceRegistry_values",
             "audit_declared_producerSourceRegistry",
             "expected_closed_key_count",
             "v14_inherited_authority_runtime_wiring_matches", "matches"} and
         registry_consensus.get("producer_independent_closed_key_count") == 75 and
         registry_consensus.get("launcher_actual_runtime_helper_matches") is True and
         isinstance(registry_consensus.get(
             "source_declared_producerSourceRegistry_values"), dict) and
         set(registry_consensus[
             "source_declared_producerSourceRegistry_values"]) ==
             {"producer", "consumer", "launcher"} and
         all(isinstance(values, list) and values and set(values) == {75}
             for values in registry_consensus[
                 "source_declared_producerSourceRegistry_values"].values()) and
         registry_consensus.get("audit_declared_producerSourceRegistry") == 75 and
         registry_consensus.get("expected_closed_key_count") == 75 and
         registry_consensus.get(
             "v14_inherited_authority_runtime_wiring_matches") is True and
         registry_consensus.get("matches") is True and
         runtime_registry_evidence.get(
             "explicit62_in_memory_tamper_rejected") is True and
         runtime_registry_evidence.get("actual_closed_registry_shape") == 75,
         "final v16r2 independent actual runtime-registry exact75 evidence")
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
    input_keys = {
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
    }
    need(isinstance(input_a, dict) and isinstance(input_b, dict) and
         set(input_a) == input_keys and set(input_b) == input_keys and
         len(input_keys) == 43 and input_a == input_b and
         tuple(input_a) == STATIC_AUDIT_INPUT_EXACT43 and
         tuple(input_b) == STATIC_AUDIT_INPUT_EXACT43 and
         sha(canonical(list(STATIC_AUDIT_INPUT_EXACT43))) ==
             STATIC_AUDIT_INPUT_EXACT43_ORDER_SHA256 and
         _nonzero_sha256(input_a.get("launcher_template")),
         "final v16r2 checker A/B exact43 ordered identical input-pin closure")
    expected_inputs = {
        "schema": CLOSED_SCHEMA_FILE_PIN,
        "contract_file": CONTRACT_FILE_PIN,
        "contract_object": CONTRACT_OBJECT_PIN,
        "producer": PRODUCER_SOURCE_PIN,
        "consumer": self_guard.file_sha256,
        "transition_file": transition_file_sha256,
        "transition_object": transition_object_sha256,
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
            V7_PUBLICATION_LOCK_CONTINUITY_INCIDENT["object_sha256"],
        "v8_rejection_file": V8_OFFICIAL_REJECTION_FILE_PIN,
        "v8_rejection_object": V8_OFFICIAL_REJECTION_OBJECT_PIN,
        "v8_launcher_file": V8_FROZEN_FILES["cold_launcher_v8"][1],
        "v8_launcher_regression_defect_sha256":
            V8_LAUNCHER_REGRESSION_DEFECT_SHA256,
        "trusted_v8_rollout_control_flow_incident_digest":
            sha(canonical(V8_ROLLOUT_CONTROL_FLOW_INCIDENT)),
        "v9_rejection_file": V9_OFFICIAL_REJECTION_FILE_PIN,
        "v9_rejection_object": V9_OFFICIAL_REJECTION_OBJECT_PIN,
        "v9_launcher_file": V9_FROZEN_FILES["cold_launcher_v9"][1],
        "v9_persisted_v6_proof_sha256": sha(canonical(
            V9_V6_HELD_SELF_IDENTITY_DEFECT_SHAPE_DRIFT_INCIDENT[
                "persisted_held_self_identity_defect"])),
        "v9_expanded_v6_proof_sha256": sha(canonical(
            V9_V6_HELD_SELF_IDENTITY_DEFECT_SHAPE_DRIFT_INCIDENT[
                "launcher_expanded_structural_evidence"])),
        "trusted_v9_proof_shape_drift_incident_digest": sha(canonical(
            V9_V6_HELD_SELF_IDENTITY_DEFECT_SHAPE_DRIFT_INCIDENT)),
        "v10_rejection_file": V10_OFFICIAL_REJECTION_FILE_PIN,
        "v10_rejection_object": V10_OFFICIAL_REJECTION_OBJECT_PIN,
        "v10_producer_file":
            V10_FROZEN_FILES["build_only_producer_v10"][1],
        "trusted_v10_regression_label_prefix_incident_digest":
            V10_REGRESSION_LABEL_PREFIX_INCIDENT_SHA256,
        "v11_rejection_file": V11_OFFICIAL_REJECTION_FILE_PIN,
        "v11_rejection_object": V11_OFFICIAL_REJECTION_OBJECT_PIN,
        "v11_producer_file": V11_FROZEN_FILES["build_only_producer_v11"][1],
        "v11_launcher_file": V11_FROZEN_FILES["cold_launcher_v11"][1],
        "trusted_v11_dual_validator_divergence_incident_digest":
            V11_DUAL_VALIDATOR_DIVERGENCE_INCIDENT_SHA256,
        "v12_rejection_file": V12_OFFICIAL_REJECTION_FILE_PIN,
        "v12_rejection_object": V12_OFFICIAL_REJECTION_OBJECT_PIN,
        "v12_producer_file": V12_FROZEN_FILES["build_only_producer_v12"][1],
        "v12_consumer_file": V12_FROZEN_FILES["independent_consumer_v12"][1],
        "v12_launcher_file": V12_FROZEN_FILES["cold_launcher_v12"][1],
        "trusted_v12_v5_rejection_shape_incident_digest":
            V12_V5_REJECTION_SHAPE_INCIDENT_SHA256,
    }
    need(tuple(expected_inputs) == STATIC_AUDIT_INPUT_EXACT43 and
         input_a == expected_inputs and
         all(_nonzero_sha256(value) for value in input_a.values()),
         "final v16r2 checker inputs pin exact current core and append-only history")
    normalized_a = checker_a.get("pin_normalized_launcher_ast_sha256")
    normalized_b = checker_b.get("pin_normalized_launcher_ast_sha256")
    normalized_c = checker_c.get("pin_normalized_launcher_ast_sha256")
    common_count_b = checker_b.get("common_ordered_callsite_row_count")
    common_count_c = checker_c.get("common_ordered_callsite_row_count")
    common_digest_b = checker_b.get("common_ordered_callsite_census_sha256")
    common_digest_c = checker_c.get("common_ordered_callsite_census_sha256")
    need(_nonzero_sha256(normalized_a) and
         normalized_a == normalized_b == normalized_c and
         type(common_count_b) is int and common_count_b > 0 and
         type(common_count_c) is int and common_count_c == common_count_b and
         _nonzero_sha256(common_digest_b) and
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
         _nonzero_sha256(
             checker_a.get("wider_local_callsite_census_sha256")) and
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

    need(set(sealed) == {
             "all_memfd_seal_checks_precede_source_or_evidence_access",
             "all_memfd_seal_checks_are_exact_equality_not_subset_tests",
             "consumer_current_v16r2_producer_content_open_read_hash_decode_compile_import_or_execute_allowed",
             "consumer_exec_source_coordination_root_fds_pairwise_distinct",
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
             "consumer_current_v16r2_producer_content_open_read_hash_decode_compile_import_or_execute_allowed") is False and
         sealed.get(
             "consumer_exec_source_coordination_root_fds_pairwise_distinct") is True and
         sealed.get(
             "consumer_v14_inherited_authority_exact12_bytes_read_only_noncredit_allowed") is True and
         sealed.get(
             "consumer_independently_rederives_witness_from_inherited_held_fds") is True and
         sealed.get("consumer_producer_source_hold_api") == "O_PATH|O_NOFOLLOW" and
         type(sealed.get("exact_required_seal_mask")) is int and
         sealed.get("exact_required_seal_mask") == 15 and
         sealed.get(
             "installed_and_exec_bytes_equal_and_terminally_replayed") is True and
         sealed.get("installed_source_mode") == "0444" and
         sealed.get("installed_source_nlink") == 1 and
         sealed.get("launcher_bootstrap_exec_source_root_fds_distinct") is True and
         sealed.get(
             "launcher_child_exec_source_coordination_root_fds_pairwise_distinct") is True and
         sealed.get(
             "producer_exec_source_coordination_root_fds_pairwise_distinct") is True and
         sealed.get("sealed_exec_mode") == "0444" and
         sealed.get("sealed_exec_nlink") == 0,
         "final v16r2 exact16 sealed-exec/current-producer/inherited-incident policy")

    need(set(acceptance) == {
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
         type(acceptance.get("final_failed_static_check_count_required")) is int and
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

    need(set(attacks) == {
             "exact_unique_ordered_attack_count_required",
             "exact_unique_ordered_attack_count_observed",
             "attack_name_order_sha256",
             "all_mutations_route_through_production_validators",
             "C42_full10_hash_join_mutations_included",
             "C42_three_directory_mode_nlink_universe_guards_are_independent_live_physical_gates",
             "attack_execution_deferred_to_cold_runtime"} and
         type(attacks.get("exact_unique_ordered_attack_count_required")) is int and
         type(attacks.get("exact_unique_ordered_attack_count_observed")) is int and
         attacks.get("exact_unique_ordered_attack_count_required") == 137 and
         attacks.get("exact_unique_ordered_attack_count_observed") == 137 and
         attacks.get("attack_name_order_sha256") == ATTACK_NAME_ORDER_PIN,
         "final audit exact seven-key 137/137 coherent attack census")
    for key in ("all_mutations_route_through_production_validators",
                "C42_full10_hash_join_mutations_included",
                "C42_three_directory_mode_nlink_universe_guards_are_independent_live_physical_gates",
                "attack_execution_deferred_to_cold_runtime"):
        _need_exact_audit_bool(attacks, key, True,
                               "final coherent attack census")

    need(set(closure) == {
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
             "consumer_ACK_launcher_ACK_key_sets_and_census_values_equal"},
         "final schema closure exact key universe")
    definition_count, reference_count, closed_count, mismatch_count = \
        _schema_static_counts(closed_schema)
    need(type(closure.get("schema_definition_count")) is int and
         closure.get("schema_definition_count") == definition_count == 46 and
         type(closure.get("schema_ref_count")) is int and
         closure.get("schema_ref_count") == reference_count == 242 and
         type(closure.get("unresolved_schema_ref_count")) is int and
         closure.get("unresolved_schema_ref_count") == 0 and
         type(closure.get("closed_object_count")) is int and
         closure.get("closed_object_count") == closed_count == 52 and
         type(closure.get("closed_object_required_property_mismatch_count")) is int and
         closure.get("closed_object_required_property_mismatch_count") ==
             mismatch_count == 0 and
         type(closure.get("unknown_schema_validation_keyword_count")) is int and
         closure.get("unknown_schema_validation_keyword_count") == 0 and
         type(closure.get("python_literal_dict_duplicate_key_count")) is int and
         closure.get("python_literal_dict_duplicate_key_count") == 0 and
         type(closure.get("undefined_global_count")) is int and
         closure.get("undefined_global_count") == 0,
         "final schema closure actual 46/242/52/0 counts")
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
         "final schema exact actual/supported keyword universe digests")
    for key in ("strict_JSON_duplicate_keys_rejected",
                "all_closed_object_required_sets_equal_property_sets",
                "all_schema_refs_resolve",
                "all_schema_validation_keywords_supported_by_cold_launcher",
                "oneOf_keyword_absent_after_pin_definition_split",
                "launcher_and_consumer_laterRejection_key_sets_equal_schema",
                "launcher_request_consumer_request_key_sets_equal",
                "consumer_ACK_launcher_ACK_key_sets_and_census_values_equal"):
        _need_exact_audit_bool(closure, key, True, "final schema closure")
    expected_shapes = {
        "selfIdentity": 33, "independentConsumerProof": 60,
        "staticFreezeProof": 84, "coldLaunchProof": 112,
        "laterRejection": 56, "producerSourceRegistry": 75,
        "liveRequest": 15, "liveACK": 32, "liveACKCensus": 42}
    shapes = closure.get("output_shape_key_counts")
    need(isinstance(shapes, dict) and set(shapes) == set(expected_shapes) and
         all(type(value) is int for value in shapes.values()) and
         shapes == expected_shapes,
         "final schema exact output-shape key counts")


def _no_zero_hash_placeholder(value: Any) -> bool:
    if isinstance(value, dict):
        return all(_no_zero_hash_placeholder(item) for item in value.values())
    if isinstance(value, list):
        return all(_no_zero_hash_placeholder(item) for item in value)
    return value != "0" * 64


def static_freeze_proof(
        policy_guard: HeldInputSet, self_guard: HeldSelf,
        producer_guard: HeldOpaqueMetadata,
        v5_guard: HeldInputSet,
        v5_source_metadata: list[HeldOpaqueMetadata],
        v6_guard: HeldInputSet,
        v6_source_metadata: list[HeldOpaqueMetadata],
        v7_guard: HeldInputSet,
        v7_source_metadata: list[HeldOpaqueMetadata],
        v8_guard: HeldInputSet,
        v8_source_metadata: list[HeldOpaqueMetadata],
        v9_guard: HeldInputSet,
        v9_source_metadata: list[HeldOpaqueMetadata],
        v10_guard: HeldInputSet,
        v10_source_metadata: list[HeldOpaqueMetadata],
        v11_guard: HeldInputSet,
        v11_source_metadata: list[HeldOpaqueMetadata]) -> dict[str, Any]:
    """Validate the acyclic post-source receipts without opening producer source."""
    by_path = {item.path: item for item in policy_guard.files}
    need(set(by_path) == {
            V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT, CONTRACT, CLOSED_SCHEMA,
            V16_TO_V16R2_TRANSITION, STATIC_AUDIT_V16R2,
            COLD_LAUNCHER, COLD_LAUNCH_MANIFEST, COLD_LAUNCH_OUTER,
        }, "exact active static/cold policy guard")
    need(producer_guard.path == PRODUCER_SOURCE,
         "exact producer path held metadata-only")
    contract = strict_json(by_path[CONTRACT].raw, "live v16r2 contract")
    v14_supersession = strict_json(
            by_path[V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT].raw,
            "live active predecessor supersession anchor")
    closed_schema = strict_json(
        by_path[CLOSED_SCHEMA].raw, "live v16r2 closed schema")
    transition = strict_json(
        by_path[V16_TO_V16R2_TRANSITION].raw, "post-source transition receipt")
    audit = strict_json(by_path[STATIC_AUDIT_V16R2].raw, "post-source static audit")
    v5_predecessor = validate_v5_published_then_rejected_predecessor(
        v6_guard, v5_guard, v5_source_metadata)
    v6_predecessor = validate_v6_published_then_rejected_predecessor(
        v7_guard, v6_guard, v6_source_metadata)
    v7_predecessor = validate_v7_published_then_rejected_predecessor(
        v8_guard, v7_guard, v7_source_metadata)
    v8_predecessor = validate_v8_published_then_rejected_predecessor(
        v9_guard, v8_guard, v8_source_metadata)
    v9_predecessor = validate_v9_published_then_rejected_predecessor(
        v10_guard, v9_guard, v9_source_metadata)
    v10_predecessor = validate_v10_published_then_rejected_predecessor(
        v11_guard, v10_guard, v10_source_metadata)
    v11_predecessor = validate_v11_published_then_rejected_predecessor(
        v11_guard, v11_source_metadata)
    v12_predecessor = validate_v12_published_then_rejected_predecessor()
    v4_receipt_guard = held_v4_supersession_from_v5(v5_guard)
    v4_supersession = exact_v4_rejection_supersession(v4_receipt_guard)
    cold_outer = strict_json(
        by_path[COLD_LAUNCH_OUTER].raw, "cold-launch outer-last receipt")
    need(isinstance(contract, dict) and isinstance(v14_supersession, dict) and
         isinstance(closed_schema, dict) and
         isinstance(transition, dict) and
         isinstance(audit, dict) and isinstance(cold_outer, dict),
         "static/cold policy objects")
    _validate_contract_bindings(contract)
    verify_object(
            v14_supersession, "live active predecessor supersession anchor",
            V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT_OBJECT_PIN)
    verify_object(transition, "post-source transition receipt")
    verify_object(audit, "post-source static audit")
    verify_object(cold_outer, "cold-launch outer-last receipt")
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
             V16_TO_V16R2_TRANSITION_KIND,
         "transition exact top-level v16-to-v16r2 closed shape")
    transition_file_sha256 = sha(by_path[V16_TO_V16R2_TRANSITION].raw)
    audit_file_sha256 = sha(by_path[STATIC_AUDIT_V16R2].raw)
    transition_object_sha256 = transition["object_sha256"]
    audit_object_sha256 = audit["object_sha256"]
    launcher_file_sha256 = sha(by_path[COLD_LAUNCHER].raw)
    cold_manifest_file_sha256 = sha(by_path[COLD_LAUNCH_MANIFEST].raw)
    cold_outer_file_sha256 = sha(by_path[COLD_LAUNCH_OUTER].raw)
    cold_outer_object_sha256 = cold_outer["object_sha256"]
    _validate_final_static_audit(
        audit, closed_schema, self_guard, transition_file_sha256,
        transition_object_sha256)
    exact8_stats = [
            by_path[V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT].before,
            by_path[CLOSED_SCHEMA].before, by_path[CONTRACT].before,
            producer_guard.before, self_guard.before,
            by_path[V16_TO_V16R2_TRANSITION].before,
            by_path[STATIC_AUDIT_V16R2].before,
            by_path[COLD_LAUNCHER].before,
        ]
    chronology = cold_publication_chronology(
        exact8_stats, by_path[COLD_LAUNCH_MANIFEST].before,
        by_path[COLD_LAUNCH_OUTER].before)
    successor = transition.get("successor_v16r2_static_bundle")
    successor_consumer = (successor.get(
        "independent_verifier_assembler_authority_consumer")
        if isinstance(successor, dict) else None)
    finalization_gates = transition.get("finalization_gates")
    cold_launch_boundary = transition.get("cold_launch_boundary")
    transition_predecessor = transition.get("append_only_predecessor_v3_regression")
    transition_v4 = transition.get("rejected_unpublished_predecessor_v4")
    transition_v5 = transition.get(
        "published_then_officially_rejected_predecessor_v5")
    transition_v6 = transition.get(
        "published_then_officially_rejected_predecessor_v6")
    transition_v7 = transition.get(
        "published_then_officially_rejected_predecessor_v7")
    transition_v8 = transition.get(
        "published_then_officially_rejected_predecessor_v8")
    transition_v9 = transition.get(
        "published_then_officially_rejected_predecessor_v9")
    transition_v10 = transition.get(
        "published_then_officially_rejected_predecessor_v10")
    transition_v11 = transition.get(
        "published_then_officially_rejected_predecessor_v11")
    transition_v12 = transition.get(
        "published_then_officially_rejected_predecessor_v12")
    transition_v13 = transition.get(
        "rejected_prepublication_v13_supersession_receipt")
    transition_v14 = transition.get(
        "published_then_officially_rejected_predecessor_v14")
    transition_v4_receipt = (transition_v4.get("supersession_receipt")
                             if isinstance(transition_v4, dict) else None)
    transition_rejection = (transition_predecessor.get("official_later_rejection")
                            if isinstance(transition_predecessor, dict) else None)
    need(isinstance(successor, dict) and isinstance(successor_consumer, dict) and
         isinstance(finalization_gates, dict) and
         isinstance(cold_launch_boundary, dict) and
         isinstance(transition_predecessor, dict) and
         isinstance(transition_rejection, dict) and isinstance(transition_v4, dict) and
         isinstance(transition_v5, dict) and
         isinstance(transition_v6, dict) and
         isinstance(transition_v7, dict) and
         isinstance(transition_v8, dict) and
         isinstance(transition_v9, dict) and
         isinstance(transition_v10, dict) and
         isinstance(transition_v11, dict) and
         isinstance(transition_v12, dict) and
         isinstance(transition_v13, dict) and
         isinstance(transition_v4_receipt, dict),
         "transition exact bundle/v3-v14 history objects")
    need(transition.get("status") ==
             "STATIC_BYTES_CLOSED_V16_TO_V16R2__PHYSICAL_FREEZE_PENDING__RUNTIME_NOT_AUTHORIZED" and
         transition.get("effective_checkpoint_object_sha256") == UPSTREAM_CHECKPOINT_OBJECT_PIN and
         transition.get("receipt_path") == str(V16_TO_V16R2_TRANSITION.relative_to(ROOT)) and
         set(successor) == {
             "all_four_core_file_pins_final", "build_only_producer",
             "closed_schema", "cold_launcher_v16r2_path", "contract",
             "draft_pin_sentinels_remain_present",
             "final_consumer_pin_installed",
             "independent_verifier_assembler_authority_consumer",
             "static_audit_v16r2_path",
             "transition_receipt_bytes_are_closed_around_final_core_pins",
             "transition_receipt_physical_freeze_completed"} and
         successor.get("all_four_core_file_pins_final") is True and
         successor.get("draft_pin_sentinels_remain_present") is False and
         successor.get("final_consumer_pin_installed") is True and
         successor.get(
             "transition_receipt_bytes_are_closed_around_final_core_pins") is True and
         successor.get("transition_receipt_physical_freeze_completed") is False and
         set(successor_consumer) == {"path", "file_sha256"} and
         successor_consumer.get("path") == str(SELF.relative_to(ROOT)) and
         successor_consumer.get("file_sha256") == self_guard.file_sha256 and
         successor.get("build_only_producer", {}).get("path") ==
             str(PRODUCER_SOURCE.relative_to(ROOT)) and
         successor.get("build_only_producer", {}).get("file_sha256") ==
             PRODUCER_SOURCE_PIN and
         successor.get("closed_schema", {}).get("path") ==
             str(CLOSED_SCHEMA.relative_to(ROOT)) and
         successor.get("closed_schema", {}).get("file_sha256") ==
             CLOSED_SCHEMA_FILE_PIN and
         successor.get("contract", {}).get("path") ==
             str(CONTRACT.relative_to(ROOT)) and
         successor.get("contract", {}).get("file_sha256") == CONTRACT_FILE_PIN and
         successor.get("contract", {}).get("object_sha256") == CONTRACT_OBJECT_PIN and
         set(cold_launch_boundary) == {
             "base7_order",
             "base7_first_member_is_v14_registry_shape_drift_supersession_receipt",
             "launcher_is_eighth", "manifest_is_ninth",
             "outer_is_tenth_and_last",
             "expected_predecessor_unique_file_identity_count",
             "expected_prepublication_unique_file_identity_count",
             "expected_terminal_unique_file_identity_count",
             "terminal_group_vector",
             "all_126_file_identities_must_share_one_statx_mount",
             "manifest_or_outer_exists_at_transition_time",
             "manifest_or_outer_created_by_this_transition",
             "runtime_entry_authorized_by_this_transition"} and
         cold_launch_boundary.get("base7_order") == [
             "v14_registry_shape_drift_supersession_receipt",
             "closed_schema_v16r2", "contract_v16r2", "producer_v16r2",
             "consumer_v16r2", "transition_v16_to_v16r2",
             "static_audit_v16r2"] and
         cold_launch_boundary.get(
             "base7_first_member_is_v14_registry_shape_drift_supersession_receipt")
             is True and
         cold_launch_boundary.get("launcher_is_eighth") is True and
         cold_launch_boundary.get("manifest_is_ninth") is True and
         cold_launch_boundary.get("outer_is_tenth_and_last") is True and
         cold_launch_boundary.get(
             "expected_predecessor_unique_file_identity_count") ==
             V16R2_PREDECESSOR_UNIQUE_LIVE_IDENTITY_COUNT and
         cold_launch_boundary.get(
             "expected_prepublication_unique_file_identity_count") ==
             V16R2_PREPUBLICATION_UNIQUE_LIVE_IDENTITY_COUNT and
         cold_launch_boundary.get(
             "expected_terminal_unique_file_identity_count") ==
             V16R2_TERMINAL_UNIQUE_LIVE_IDENTITY_COUNT and
         cold_launch_boundary.get("terminal_group_vector") ==
             list(V16R2_TERMINAL_GROUP_VECTOR) and
         cold_launch_boundary.get(
             "all_126_file_identities_must_share_one_statx_mount") is True and
         cold_launch_boundary.get(
             "manifest_or_outer_exists_at_transition_time") is False and
         cold_launch_boundary.get(
             "manifest_or_outer_created_by_this_transition") is False and
         cold_launch_boundary.get(
             "runtime_entry_authorized_by_this_transition") is False and
         set(finalization_gates) == {
             "cold_launcher_final_pin_instance_generated",
             "final_core_pins_installed_before_object_closure",
             "final_independent_static_audit_A_GO",
             "final_independent_static_audit_B_GO",
             "ordered_exact8_manifest_created", "outer_receipt_created_last",
             "terminal_byte_replay_completed"} and
         finalization_gates.get(
             "final_core_pins_installed_before_object_closure") is True and
         all(finalization_gates.get(name) is False for name in (
             "cold_launcher_final_pin_instance_generated",
             "final_independent_static_audit_A_GO",
             "final_independent_static_audit_B_GO",
             "ordered_exact8_manifest_created", "outer_receipt_created_last",
             "terminal_byte_replay_completed")) and
         transition_predecessor.get("ordered_exact10") == _expected_frozen_v3_exact10() and
         transition_rejection.get("path") == str(V3_OFFICIAL_REJECTION.relative_to(ROOT)) and
         transition_rejection.get("file_sha256") == V3_OFFICIAL_REJECTION_FILE_PIN and
         transition_rejection.get("object_sha256") == V3_OFFICIAL_REJECTION_OBJECT_PIN and
         transition_rejection.get("chronology_required") ==
             "MAX_V3_OUTER_MTIME_CTIME_LT_MIN_REJECTION_MTIME_CTIME" and
         transition_rejection.get("chronology_validated") is True and
         transition_v4_receipt.get("path") ==
             str(V4_REJECTION_SUPERSESSION.relative_to(ROOT)) and
         transition_v4_receipt.get("file_sha256") ==
             V4_REJECTION_SUPERSESSION_FILE_PIN and
         transition_v4_receipt.get("object_sha256") ==
             V4_REJECTION_SUPERSESSION_OBJECT_PIN and
         transition_v4.get("ordered_provisional_exact8") ==
             v4_supersession["frozen_v4_provisional_exact8"]["ordered_members"] and
         transition_v4.get("v4_execution_allowed") is False and
         transition_v5.get("ordered_published_exact10") ==
             _expected_published_v5_exact10() and
         transition_v5.get("first_build_entry_attempt") ==
             _v5_first_build_entry_attempt() and
         transition_v5.get("strict_bool_defect_census") ==
             _v5_strict_bool_defect_census() and
         transition_v5.get("official_later_rejection", {}).get("file_sha256") ==
             V5_OFFICIAL_REJECTION_FILE_PIN and
         transition_v5.get("official_later_rejection", {}).get("object_sha256") ==
             V5_OFFICIAL_REJECTION_OBJECT_PIN and
         transition_v6 == _expected_published_then_rejected_v6_proof() and
         transition_v7 == _expected_published_then_rejected_v7_proof() and
         transition_v8 == _expected_published_then_rejected_v8_proof() and
         transition_v9 == _expected_published_then_rejected_v9_proof() and
         transition_v10 == _expected_published_then_rejected_v10_proof() and
         transition_v11 == _expected_published_then_rejected_v11_proof() and
         transition_v12 == _expected_published_then_rejected_v12_proof() and
         transition_v13 ==
             expected_rejected_prepublication_v13_supersession_receipt(),
         "transition pins current bundle and append-only "
         "v3/v4/v5/v6/v7/v8/v9/v10/v11/v12/v13/v14 predecessors")
    audited = audit.get("audited_v16r2_bundle")
    audit_predecessor = audit.get("predecessor_v3_exact10_regression")
    audit_rejection = audit.get("v3_official_later_rejection_regression")
    audit_v4 = audit.get("predecessor_v4_rejection_supersession_regression")
    audit_v5 = audit.get(
        "published_then_officially_rejected_predecessor_v5")
    audit_v6 = audit.get(
        "published_then_officially_rejected_predecessor_v6")
    audit_v7 = audit.get(
        "published_then_officially_rejected_predecessor_v7")
    audit_v8 = audit.get(
        "published_then_officially_rejected_predecessor_v8")
    audit_v9 = audit.get(
        "published_then_officially_rejected_predecessor_v9")
    audit_v10 = audit.get(
        "published_then_officially_rejected_predecessor_v10")
    audit_v11 = audit.get(
        "published_then_officially_rejected_predecessor_v11")
    audit_v12 = audit.get(
        "published_then_officially_rejected_predecessor_v12")
    audit_v13 = audit.get(
        "rejected_prepublication_v13_supersession_receipt")
    audit_v14 = audit.get(
        "published_then_officially_rejected_predecessor_v14")
    attack_census = audit.get("coherent_attack_static_census")
    schema_closure = audit.get("schema_and_constructor_closure")
    acceptance = audit.get("final_audit_acceptance")
    need(isinstance(audited, dict) and isinstance(audit_predecessor, dict) and
         isinstance(audit_rejection, dict) and isinstance(audit_v4, dict) and
         isinstance(audit_v5, dict) and
         isinstance(audit_v6, dict) and
         isinstance(audit_v7, dict) and
         isinstance(audit_v8, dict) and
         isinstance(audit_v9, dict) and
         isinstance(audit_v10, dict) and
         isinstance(audit_v11, dict) and
         isinstance(audit_v12, dict) and
         isinstance(audit_v13, dict) and
         isinstance(audit_v14, dict) and
         isinstance(attack_census, dict) and isinstance(schema_closure, dict) and
         isinstance(acceptance, dict),
         "static audit exact bundle/rejection/attack/acceptance objects")
    need(audit.get("effective_checkpoint_object_sha256") == UPSTREAM_CHECKPOINT_OBJECT_PIN and
         audit.get("audit_path") == str(STATIC_AUDIT_V16R2.relative_to(ROOT)) and
         audited.get("independent_verifier_assembler_authority_consumer", {}).get(
             "path") == str(SELF.relative_to(ROOT)) and
         audited.get("independent_verifier_assembler_authority_consumer", {}).get(
             "file_sha256") == self_guard.file_sha256 and
         audited.get("build_only_producer", {}).get("path") ==
             str(PRODUCER_SOURCE.relative_to(ROOT)) and
         audited.get("build_only_producer", {}).get("file_sha256") ==
             PRODUCER_SOURCE_PIN and
         audited.get("closed_schema", {}).get("path") ==
             str(CLOSED_SCHEMA.relative_to(ROOT)) and
         audited.get("closed_schema", {}).get("file_sha256") ==
             CLOSED_SCHEMA_FILE_PIN and
         audited.get("contract", {}).get("path") ==
             str(CONTRACT.relative_to(ROOT)) and
         audited.get("contract", {}).get("file_sha256") == CONTRACT_FILE_PIN and
         audited.get("contract", {}).get("object_sha256") == CONTRACT_OBJECT_PIN and
         audited.get("v16_to_v16r2_transition_receipt", {}).get("path") ==
             str(V16_TO_V16R2_TRANSITION.relative_to(ROOT)) and
         audited.get("v16_to_v16r2_transition_receipt", {}).get("file_sha256") ==
             transition_file_sha256 and
         audited.get("v16_to_v16r2_transition_receipt", {}).get("object_sha256") ==
             transition_object_sha256 and
         audit_predecessor.get("ordered_exact10") == _expected_frozen_v3_exact10() and
         audit_predecessor.get("all_ten_file_pins_match") is True and
         audit_predecessor.get("all_declared_object_pins_match") is True and
         audit_rejection.get("path") == str(V3_OFFICIAL_REJECTION.relative_to(ROOT)) and
         audit_rejection.get("file_sha256") == V3_OFFICIAL_REJECTION_FILE_PIN and
         audit_rejection.get("object_sha256") == V3_OFFICIAL_REJECTION_OBJECT_PIN and
         audit_rejection.get("chronology_required") ==
             "MAX_V3_OUTER_MTIME_CTIME_LT_MIN_REJECTION_MTIME_CTIME" and
         audit_rejection.get("chronology_validated") is True and
         audit_v4.get("receipt_file_sha256") ==
             V4_REJECTION_SUPERSESSION_FILE_PIN and
         audit_v4.get("receipt_object_sha256") ==
             V4_REJECTION_SUPERSESSION_OBJECT_PIN and
         audit_v4.get("ordered_provisional_exact8_matches_receipt") is True and
         audit_v4.get("v4_root_defects_detected_present") is True and
         audit_v4.get("receipt_recorded_root_defect_count") == 3 and
         audit_v4.get(
             "additional_successor_discovered_v4_audit_defect_count") == 1 and
         audit_v4.get(
             "v4_schema_required_property_false_assertion_present") is True and
         audit_v4.get(
             "v5_closed_object_required_property_mismatch_count") == 0 and
         audit_v4.get("same_defects_absent_from_v5") is True and
         audit_v4.get(
             "v6_closed_object_required_property_mismatch_count") == 0 and
         audit_v4.get("same_defects_absent_from_v6") is True and
         audit_v5.get("ordered_published_exact10") ==
             _expected_published_v5_exact10() and
         audit_v5.get("official_later_rejection", {}).get("file_sha256") ==
             V5_OFFICIAL_REJECTION_FILE_PIN and
         audit_v5.get("official_later_rejection", {}).get("object_sha256") ==
             V5_OFFICIAL_REJECTION_OBJECT_PIN and
         audit_v5.get("first_build_entry_attempt") ==
             _v5_first_build_entry_attempt() and
         audit_v5.get("strict_bool_defect_census") ==
             _v5_strict_bool_defect_census() and
         audit_v6 == _expected_published_then_rejected_v6_proof() and
         audit_v7 == _expected_published_then_rejected_v7_proof() and
         audit_v8 == _expected_published_then_rejected_v8_proof() and
         audit_v9 == _expected_published_then_rejected_v9_proof() and
         audit_v10 == _expected_published_then_rejected_v10_proof() and
         audit_v11 == _expected_published_then_rejected_v11_proof() and
         len(audit_v11) == 19 and
         digest(audit_v11) == V11_PUBLISHED_THEN_REJECTED_PROOF_SHA256 and
         audit_v12 == _expected_published_then_rejected_v12_proof() and
         len(audit_v12) == 19 and
         audit_v13 ==
             expected_rejected_prepublication_v13_supersession_receipt() and
         audit_v14 == expected_published_then_rejected_v14_summary() and
         audit.get("v10_colon_prefix_witness") == V10_COLON_PREFIX_WITNESS and
         audit.get("v11_dual_validator_divergence_incident") ==
             V11_DUAL_VALIDATOR_DIVERGENCE_INCIDENT and
         audit.get("v12_v5_rejection_shape_incident") ==
             V12_V5_REJECTION_SHAPE_INCIDENT and
         audit.get("historical_rejection_exact_keyset_witness") ==
             list(HISTORICAL_REJECTION_EXACT_KEYSET_WITNESS) and
         attack_census.get("attack_name_order_sha256") == ATTACK_NAME_ORDER_PIN and
         attack_census.get("exact_unique_ordered_attack_count_required") == 137 and
         schema_closure.get(
             "all_schema_validation_keywords_supported_by_cold_launcher") is True and
         schema_closure.get("unknown_schema_validation_keyword_count") == 0 and
         schema_closure.get(
             "closed_object_required_property_mismatch_count") == 0 and
         schema_closure.get(
             "oneOf_keyword_absent_after_pin_definition_split") is True and
         acceptance.get("current_draft_pass") is True and
         acceptance.get("final_failed_static_check_count_required") == 0 and
         acceptance.get("final_static_freeze_pass_required") is True and
         audit.get("status") ==
             "PASS_DUAL_STATIC_PIN_NORMALIZED_AST_GO_V16R2__"
             "PHYSICAL_COLD_FREEZE_PENDING__"
             "RUNTIME_NOT_AUTHORIZED" and
         "DRAFT" not in str(transition.get("status")) and
         _no_zero_hash_placeholder(transition) and
         _no_zero_hash_placeholder(audit),
         "static audit pins current bundle plus rejected-v4 and v3 regressions and is final")
    exact8_expected = [
            {"file_sha256": V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT_FILE_PIN,
             "entry_name": str(V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT.relative_to(ROOT))},
            {"file_sha256": CLOSED_SCHEMA_FILE_PIN, "entry_name": str(CLOSED_SCHEMA.relative_to(ROOT))},
            {"file_sha256": CONTRACT_FILE_PIN, "entry_name": str(CONTRACT.relative_to(ROOT))},
            {"file_sha256": PRODUCER_SOURCE_PIN, "entry_name": str(PRODUCER_SOURCE.relative_to(ROOT))},
            {"file_sha256": self_guard.file_sha256, "entry_name": str(SELF.relative_to(ROOT))},
            {"file_sha256": transition_file_sha256, "entry_name": str(V16_TO_V16R2_TRANSITION.relative_to(ROOT))},
            {"file_sha256": audit_file_sha256, "entry_name": str(STATIC_AUDIT_V16R2.relative_to(ROOT))},
            {"file_sha256": launcher_file_sha256, "entry_name": str(COLD_LAUNCHER.relative_to(ROOT))},
        ]
    cold_manifest = parse_manifest_ordered(
        by_path[COLD_LAUNCH_MANIFEST].raw, "cold-launch exact8 manifest")
    need(cold_manifest == exact8_expected and
         all(_nonzero_sha256(entry["file_sha256"]) for entry in cold_manifest),
         "cold-launch manifest exact8 actual ordered hashes")
    outer_expected_entries = [
        {"path": entry["entry_name"], "file_sha256": entry["file_sha256"]}
        for entry in exact8_expected]
    need(set(cold_outer) == {
             "schema", "status", "effective_checkpoint_object_sha256",
             "exact8_ordered_entries", "cold_launch_manifest", "cold_launcher",
             "all_exact8_regular_0444_nlink1_and_held_for_runtime",
             "outer_published_after_exact8_manifest",
             "runtime_entry_must_be_cold_launcher",
             "sole_external_static_file_anchor_is_launcher_sha256",
             "declared_external_tcb",
             "formal_global_closure_credit", "D02_unlock",
             "runtime_executed_during_static_freeze", "object_sha256"} and
         by_path[COLD_LAUNCH_OUTER].raw == canonical(cold_outer) + b"\n" and
         cold_outer.get("schema") ==
             "cm2.round306c79g.true-global-no-producer-consumer."
             "cold-launch-outer-receipt.v16r2" and
         cold_outer.get("status") ==
             "FROZEN_COLD_LAUNCH_OUTER_LAST__EXACT8_MANIFEST_CLOSED__RUNTIME_DEFERRED" and
         cold_outer.get("effective_checkpoint_object_sha256") == UPSTREAM_CHECKPOINT_OBJECT_PIN and
         cold_outer.get("exact8_ordered_entries") == outer_expected_entries and
         cold_outer.get("cold_launch_manifest") == {
             "path": str(COLD_LAUNCH_MANIFEST.relative_to(ROOT)),
             "file_sha256": cold_manifest_file_sha256,
             "ordered_entry_count": 8} and
         cold_outer.get("cold_launcher") == {
             "path": str(COLD_LAUNCHER.relative_to(ROOT)),
             "file_sha256": launcher_file_sha256} and
         cold_outer.get("all_exact8_regular_0444_nlink1_and_held_for_runtime") is True and
         cold_outer.get("outer_published_after_exact8_manifest") is True and
         cold_outer.get("runtime_entry_must_be_cold_launcher") is True and
         cold_outer.get("sole_external_static_file_anchor_is_launcher_sha256") is True and
         cold_outer.get("declared_external_tcb") == [
             "EXTERNAL_HELD_FD_SEALED_MEMFD_BOOTSTRAP",
             "PYTHON3_ISOLATED_INTERPRETER",
             "LINUX_KERNEL_OPENAT2_STATX_MEMFD_PROCFS"] and
         cold_outer.get("formal_global_closure_credit") == 0 and
         cold_outer.get("D02_unlock") is False and
         cold_outer.get("runtime_executed_during_static_freeze") is False and
         os.environ.get(COLD_LAUNCHER_SHA_ENV) == launcher_file_sha256 and
         all(chronology.values()),
         "cold-launch outer exact object closure/order/zero-credit/outer-last")
    transition_identity = _one_identity(by_path[V16_TO_V16R2_TRANSITION])
    transition_identity["object_sha256"] = transition_object_sha256
    audit_identity = _one_identity(by_path[STATIC_AUDIT_V16R2])
    audit_identity["object_sha256"] = audit_object_sha256
    v4_supersession_identity = _one_identity(v4_receipt_guard)
    v4_supersession_identity["object_sha256"] = \
        V4_REJECTION_SUPERSESSION_OBJECT_PIN
    launcher_identity = _one_identity(by_path[COLD_LAUNCHER])
    manifest_identity = _one_identity(by_path[COLD_LAUNCH_MANIFEST])
    cold_outer_identity = _one_identity(by_path[COLD_LAUNCH_OUTER])
    cold_outer_identity["object_sha256"] = cold_outer_object_sha256
    exact10_identities = (
        [item.identity for item in policy_guard.files] +
        [(self_guard.before.st_dev, self_guard.before.st_ino),
         producer_guard.identity])
    exact10_mount_ids = (
        [item.mount_id for item in policy_guard.files] +
        [self_guard.mount_id, producer_guard.mount_id])
    need(len(exact10_identities) == 10 and
         len(set(exact10_identities)) == 10 and
         len(set(exact10_mount_ids)) == 1,
         "cold exact10 identities globally unique on one statx mount")
    producer_identity_metadata = {
        "path": str(PRODUCER_SOURCE.relative_to(ROOT)),
        "st_dev": producer_guard.before.st_dev,
        "st_ino": producer_guard.before.st_ino,
        "stx_mnt_id": producer_guard.mount_id,
        "st_size": producer_guard.before.st_size,
        "mode": f"{stat.S_IMODE(producer_guard.before.st_mode):04o}",
        "nlink": producer_guard.before.st_nlink,
        "held_with_openat2_O_PATH_NOFOLLOW_and_four_resolve_flags": True,
        "producer_content_opened_read_or_hashed": False,
        "producer_identity_metadata_held": True,
    }
    # Bind the cold-exec claim to an executed terminal replay before the proof
    # object can report it.  Later command-specific terminal replays remain
    # mandatory and independently fail closed.
    self_guard.terminal_replay()
    v5_rejection_identity = _one_identity(
        held_v5_official_rejection(v6_guard))
    v5_rejection_identity["object_sha256"] = \
        V5_OFFICIAL_REJECTION_OBJECT_PIN
    v6_rejection_identity = _one_identity(
        held_v6_official_rejection(v7_guard))
    v6_rejection_identity["object_sha256"] = \
        V6_OFFICIAL_REJECTION_OBJECT_PIN
    v7_rejection_identity = _one_identity(
        held_v7_official_rejection(v8_guard))
    v7_rejection_identity["object_sha256"] = \
        V7_OFFICIAL_REJECTION_OBJECT_PIN
    v8_rejection_identity = _one_identity(
        held_v8_official_rejection(v9_guard))
    v8_rejection_identity["object_sha256"] = \
        V8_OFFICIAL_REJECTION_OBJECT_PIN
    v12_rejection_identity = _one_identity(held_v12_official_rejection())
    v12_rejection_identity["object_sha256"] = \
        V12_OFFICIAL_REJECTION_OBJECT_PIN
    return {
        "published_then_officially_rejected_predecessor_v5":
            copy.deepcopy(v5_predecessor),
        "v5_official_rejection_identity": v5_rejection_identity,
        "v5_official_rejection_file_sha256": V5_OFFICIAL_REJECTION_FILE_PIN,
        "v5_official_rejection_object_sha256":
            V5_OFFICIAL_REJECTION_OBJECT_PIN,
        "v4_rejection_supersession_identity": v4_supersession_identity,
        "v4_rejection_supersession_file_sha256":
            V4_REJECTION_SUPERSESSION_FILE_PIN,
        "v4_rejection_supersession_object_sha256":
            V4_REJECTION_SUPERSESSION_OBJECT_PIN,
        "v16_to_v16r2_transition_identity": transition_identity,
        "static_audit_identity": audit_identity,
        "transition_object_sha256": transition_object_sha256,
        "static_audit_object_sha256": audit_object_sha256,
        "transition_pins_current_consumer_SELF":
            successor["independent_verifier_assembler_authority_consumer"]
                ["file_sha256"] == self_guard.file_sha256 and
            transition_v13 ==
                expected_rejected_prepublication_v13_supersession_receipt(),
        "static_audit_pins_current_consumer_SELF_transition_contract_schema_rejection_and_producer":
            audited["independent_verifier_assembler_authority_consumer"]
                ["file_sha256"] == self_guard.file_sha256 and
            audited["v16_to_v16r2_transition_receipt"]["file_sha256"] ==
                transition_file_sha256 and
            audited["v16_to_v16r2_transition_receipt"]["object_sha256"] ==
                transition_object_sha256 and
            audited["contract"]["file_sha256"] == CONTRACT_FILE_PIN and
            audited["contract"]["object_sha256"] == CONTRACT_OBJECT_PIN and
            audited["closed_schema"]["file_sha256"] == CLOSED_SCHEMA_FILE_PIN and
            audit_rejection["file_sha256"] == V3_OFFICIAL_REJECTION_FILE_PIN and
            audit_rejection["object_sha256"] == V3_OFFICIAL_REJECTION_OBJECT_PIN and
            audit_v4["receipt_file_sha256"] ==
                V4_REJECTION_SUPERSESSION_FILE_PIN and
            audit_v4["receipt_object_sha256"] ==
                V4_REJECTION_SUPERSESSION_OBJECT_PIN and
            audit_v13 ==
                expected_rejected_prepublication_v13_supersession_receipt() and
            audit_v14 == expected_published_then_rejected_v14_summary() and
            audited["build_only_producer"]["file_sha256"] == PRODUCER_SOURCE_PIN,
        "rejected_unpublished_predecessor_v4_validated":
            v4_receipt_guard.raw ==
                canonical(v4_supersession) + b"\n" and
            v4_supersession["object_sha256"] ==
                V4_REJECTION_SUPERSESSION_OBJECT_PIN and
            transition_v4.get("v4_execution_allowed") is False,
        "ordered_provisional_exact8_validated":
            transition_v4.get("ordered_provisional_exact8") ==
                v4_supersession["frozen_v4_provisional_exact8"]["ordered_members"],
        "current_exact8_first_member_is_v14_registry_shape_drift_supersession_receipt":
            cold_manifest[0] == {
                "file_sha256":
                    V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT_FILE_PIN,
                "entry_name": str(
                    V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT.
                    relative_to(ROOT))} and
            by_path[
                V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT].identity ==
                _INCIDENT_AUTHORITY_HOLD.v14_supersession_identity() and
            v14_supersession == strict_json(
                _INCIDENT_AUTHORITY_HOLD.authority_exact12_by_role[
                    "v14_registry_shape_drift_supersession_receipt"].raw,
                "held v14 supersession current exact8 anchor") and
            audit_v14 == expected_published_then_rejected_v14_summary(),
        "rejected_prepublication_v13_supersession_receipt_validated":
            sha(_INCIDENT_AUTHORITY_HOLD.by_env[
                V13_SUPERSESSION_RECEIPT_FD_ENV].raw) ==
                V13_SUPERSESSION_RECEIPT_FILE_PIN and
            strict_json(
                _INCIDENT_AUTHORITY_HOLD.by_env[
                    V13_SUPERSESSION_RECEIPT_FD_ENV].raw,
                "held historical v13 supersession") ==
                _INCIDENT_AUTHORITY_HOLD.v13_supersession_receipt and
            contract.get(
                "rejected_prepublication_v13_supersession_receipt") ==
            transition_v13 == audit_v13 ==
                expected_rejected_prepublication_v13_supersession_receipt(),
        "published_then_officially_rejected_predecessor_v5_validated":
            transition_v5 == audit_v5 and
            transition_v5.get("ordered_published_exact10") ==
                v5_predecessor["ordered_published_exact10"] and
            transition_v5.get("first_build_entry_attempt") ==
                v5_predecessor["first_build_entry_attempt"] and
            transition_v5.get("strict_bool_defect_census") ==
                v5_predecessor["strict_bool_defect_census"] and
            transition_v5.get("official_later_rejection", {}).get(
                "file_sha256") == V5_OFFICIAL_REJECTION_FILE_PIN and
            transition_v5.get("official_later_rejection", {}).get(
                "object_sha256") == V5_OFFICIAL_REJECTION_OBJECT_PIN,
        "published_then_officially_rejected_predecessor_v6":
            copy.deepcopy(v6_predecessor),
        "v6_official_rejection_identity": v6_rejection_identity,
        "v6_official_rejection_file_sha256": V6_OFFICIAL_REJECTION_FILE_PIN,
        "v6_official_rejection_object_sha256":
            V6_OFFICIAL_REJECTION_OBJECT_PIN,
        "published_then_officially_rejected_predecessor_v6_validated":
            transition_v6 == audit_v6 == v6_predecessor and
            transition_v6.get("ordered_published_exact10") ==
                _expected_published_v6_exact10() and
            transition_v6.get("first_build_entry_attempt") ==
                _v6_first_build_entry_attempt() and
            transition_v6.get("held_self_identity_defect") ==
                _v6_held_self_identity_defect() and
            transition_v6.get("official_later_rejection", {}).get(
                "file_sha256") == V6_OFFICIAL_REJECTION_FILE_PIN and
            transition_v6.get("official_later_rejection", {}).get(
                "object_sha256") == V6_OFFICIAL_REJECTION_OBJECT_PIN,
        "published_then_officially_rejected_predecessor_v7":
            copy.deepcopy(v7_predecessor),
        "v7_publication_lock_continuity_incident": copy.deepcopy(
            v7_predecessor["publication_lock_continuity_incident"]),
        "v7_official_rejection_identity": v7_rejection_identity,
        "v7_official_rejection_file_sha256": V7_OFFICIAL_REJECTION_FILE_PIN,
        "v7_official_rejection_object_sha256":
            V7_OFFICIAL_REJECTION_OBJECT_PIN,
        "v7_official_rejection_shared_v8_predecessor_held_fd":
            held_v7_official_rejection(v8_guard).fd ==
                {item.path: item for item in v8_guard.files}[
                    V7_OFFICIAL_REJECTION].fd,
        "published_then_officially_rejected_predecessor_v7_validated":
            transition_v7 == audit_v7 == v7_predecessor and
            transition_v7.get("ordered_published_exact10") ==
                _expected_published_v7_exact10() and
            transition_v7.get("publication_lock_continuity_incident") ==
                _validated_v7_publication_lock_continuity_incident() and
            transition_v7.get("official_later_rejection", {}).get(
                "file_sha256") == V7_OFFICIAL_REJECTION_FILE_PIN and
            transition_v7.get("official_later_rejection", {}).get(
                "object_sha256") == V7_OFFICIAL_REJECTION_OBJECT_PIN,
        "v7_publication_lock_continuity_incident_validated":
            v7_predecessor["publication_lock_continuity_incident"] ==
                _validated_v7_publication_lock_continuity_incident(),
        "published_then_officially_rejected_predecessor_v8":
            copy.deepcopy(v8_predecessor),
        "v8_official_rejection": exact_v8_official_rejection(v9_guard)[0],
        "v8_official_rejection_identity": v8_rejection_identity,
        "v8_official_rejection_file_sha256": V8_OFFICIAL_REJECTION_FILE_PIN,
        "v8_official_rejection_object_sha256":
            V8_OFFICIAL_REJECTION_OBJECT_PIN,
        "v8_official_rejection_shared_v9_predecessor_held_fd":
            held_v8_official_rejection(v9_guard).fd ==
                {item.path: item for item in v9_guard.files}[
                    V8_OFFICIAL_REJECTION].fd,
        "published_then_officially_rejected_predecessor_v8_validated":
            transition_v8 == audit_v8 == v8_predecessor and
            transition_v8.get("ordered_published_exact10") ==
                _expected_published_v8_exact10() and
            transition_v8.get("first_rollout_attempt") ==
                V8_FIRST_ROLLOUT_ATTEMPT and
            transition_v8.get("rollout_control_flow_incident") ==
                V8_ROLLOUT_CONTROL_FLOW_INCIDENT and
            transition_v8.get("chronology_is_not_control_flow_proof") is True and
            transition_v8.get("official_later_rejection", {}).get(
                "file_sha256") == V8_OFFICIAL_REJECTION_FILE_PIN and
            transition_v8.get("official_later_rejection", {}).get(
                "object_sha256") == V8_OFFICIAL_REJECTION_OBJECT_PIN,
        "v8_forbidden_positive_and_stage_surface_count":
            len(V8_ALL_POSITIVE_AND_STAGE_SURFACES),
        "published_then_officially_rejected_predecessor_v9":
            copy.deepcopy(v9_predecessor),
        "published_then_officially_rejected_predecessor_v9_validated":
            transition_v9 == audit_v9 == v9_predecessor and
            transition_v9.get("ordered_published_exact10") ==
                _expected_published_v9_exact10() and
            transition_v9.get("first_runtime_attempt") ==
                V9_FIRST_RUNTIME_ATTEMPT and
            transition_v9.get(
                "v6_held_self_identity_defect_shape_drift_incident") ==
                V9_V6_HELD_SELF_IDENTITY_DEFECT_SHAPE_DRIFT_INCIDENT and
            transition_v9.get("positive_and_stage_surfaces_absent") ==
                _expected_published_then_rejected_v9_proof()[
                    "positive_and_stage_surfaces_absent"] and
            transition_v9.get("official_later_rejection", {}).get(
                "file_sha256") == V9_OFFICIAL_REJECTION_FILE_PIN and
            transition_v9.get("official_later_rejection", {}).get(
                "object_sha256") == V9_OFFICIAL_REJECTION_OBJECT_PIN,
        "published_then_officially_rejected_predecessor_v10":
            copy.deepcopy(v10_predecessor),
        "published_then_officially_rejected_predecessor_v10_validated":
            transition_v10 == audit_v10 == v10_predecessor and
            transition_v10.get("ordered_published_exact10") ==
                _expected_published_v10_exact10() and
            transition_v10.get("first_runtime_attempt") ==
                V10_FIRST_RUNTIME_ATTEMPT and
            transition_v10.get("regression_label_prefix_incident") ==
                V10_REGRESSION_LABEL_PREFIX_INCIDENT and
            sha(canonical(transition_v10[
                "regression_label_prefix_incident"])) ==
                V10_REGRESSION_LABEL_PREFIX_INCIDENT_SHA256 and
            V10_REGRESSION_LABEL_PREFIX_INCIDENT[
                "colon_prefixed_failure_label_literal"] ==
                ":" + V10_REGRESSION_LABEL_PREFIX_INCIDENT[
                    "failure_label_without_colon_prefix"] and
            V10_REGRESSION_LABEL_PREFIX_INCIDENT[
                "exact_unprefixed_failure_label_literal_count"] == 0 and
            V10_REGRESSION_LABEL_PREFIX_INCIDENT[
                "exact_colon_prefixed_failure_label_literal_count"] == 1 and
            V10_REGRESSION_LABEL_PREFIX_INCIDENT[
                "failure_label_suffix_match_count"] == 1 and
            V10_REGRESSION_LABEL_PREFIX_INCIDENT[
                "authority_derived_from_AST_structure_and_exact_prefix_join"] is True and
            V10_REGRESSION_LABEL_PREFIX_INCIDENT[
                "raw_whole_tree_string_equality_is_authority"] is False and
            V10_REGRESSION_LABEL_PREFIX_INCIDENT[
                "hold_function_contains_mkdir_call"] is False and
            transition_v10.get("positive_and_stage_surfaces_absent") ==
                _expected_published_then_rejected_v10_proof()[
                    "positive_and_stage_surfaces_absent"] and
            transition_v10.get("official_later_rejection", {}).get(
                "file_sha256") == V10_OFFICIAL_REJECTION_FILE_PIN and
            transition_v10.get("official_later_rejection", {}).get(
                "object_sha256") == V10_OFFICIAL_REJECTION_OBJECT_PIN,
        "published_then_officially_rejected_predecessor_v11":
            copy.deepcopy(v11_predecessor),
        "published_then_officially_rejected_predecessor_v12":
            copy.deepcopy(v12_predecessor),
        "published_then_officially_rejected_predecessor_v11_validated":
            transition_v11 == audit_v11 == v11_predecessor and
            transition_v11.get("ordered_published_exact10") ==
                _expected_published_v11_exact10() and
            transition_v11.get("first_runtime_attempt") ==
                V11_FIRST_RUNTIME_ATTEMPT and
            transition_v11.get("dual_validator_divergence_incident") ==
                V11_DUAL_VALIDATOR_DIVERGENCE_INCIDENT and
            transition_v11.get("positive_and_stage_surfaces_absent") ==
                _expected_published_then_rejected_v11_proof()[
                    "positive_and_stage_surfaces_absent"] and
            transition_v11.get("official_later_rejection", {}).get(
                "file_sha256") == V11_OFFICIAL_REJECTION_FILE_PIN and
            transition_v11.get("official_later_rejection", {}).get(
                "object_sha256") == V11_OFFICIAL_REJECTION_OBJECT_PIN,
        "v12_v5_rejection_shape_incident": copy.deepcopy(
            V12_V5_REJECTION_SHAPE_INCIDENT),
        "v12_official_rejection_identity": v12_rejection_identity,
        "v12_official_rejection_file_sha256": V12_OFFICIAL_REJECTION_FILE_PIN,
        "v12_official_rejection_object_sha256":
            V12_OFFICIAL_REJECTION_OBJECT_PIN,
        "published_then_officially_rejected_predecessor_v12_validated":
            transition_v12 == audit_v12 == v12_predecessor and
            transition_v12.get("ordered_published_exact10") ==
                _expected_published_v12_exact10() and
            transition_v12.get("first_runtime_attempt") ==
                V12_FIRST_RUNTIME_ATTEMPT and
            transition_v12.get("v5_rejection_shape_incident") ==
                V12_V5_REJECTION_SHAPE_INCIDENT and
            transition_v12.get("positive_and_stage_surfaces_absent") ==
                _expected_published_then_rejected_v12_proof()[
                    "positive_and_stage_surfaces_absent"] and
            transition_v12.get("official_later_rejection", {}).get(
                "file_sha256") == V12_OFFICIAL_REJECTION_FILE_PIN and
            transition_v12.get("official_later_rejection", {}).get(
                "object_sha256") == V12_OFFICIAL_REJECTION_OBJECT_PIN,
        "historical_rejection_exact_keyset_witness": copy.deepcopy(
            list(HISTORICAL_REJECTION_EXACT_KEYSET_WITNESS)),
        "historical_rejection_exact_keyset_witness_validated":
            audit.get("historical_rejection_exact_keyset_witness") ==
                list(HISTORICAL_REJECTION_EXACT_KEYSET_WITNESS) and
            digest(audit.get(
                "historical_rejection_exact_keyset_witness")) ==
                digest(list(HISTORICAL_REJECTION_EXACT_KEYSET_WITNESS)),
        "append_only_history_unique_file_identity_count":
            V16R2_TERMINAL_UNIQUE_LIVE_IDENTITY_COUNT,
        "v5_strict_bool_three_hard_seven_risk_present_and_v6_absent":
            v5_predecessor["strict_bool_defect_census"] ==
                _v5_strict_bool_defect_census(),
        "predecessor_v4_rejection_supersession_regression_validated":
            transition_v4_receipt.get("file_sha256") ==
                V4_REJECTION_SUPERSESSION_FILE_PIN and
            transition_v4_receipt.get("object_sha256") ==
                V4_REJECTION_SUPERSESSION_OBJECT_PIN and
            transition_v4.get("ordered_provisional_exact8") ==
                v4_supersession["frozen_v4_provisional_exact8"]["ordered_members"] and
            audit_v4.get("receipt_file_sha256") ==
                V4_REJECTION_SUPERSESSION_FILE_PIN and
            audit_v4.get("receipt_object_sha256") ==
                V4_REJECTION_SUPERSESSION_OBJECT_PIN and
            audit_v4.get("ordered_provisional_exact8_matches_receipt") is True and
            audit_v4.get("v4_root_defects_detected_present") is True and
            audit_v4.get("receipt_recorded_root_defect_count") == 3 and
            audit_v4.get(
                "additional_successor_discovered_v4_audit_defect_count") == 1 and
            audit_v4.get(
                "v4_schema_required_property_false_assertion_present") is True and
            audit_v4.get(
                "v5_closed_object_required_property_mismatch_count") == 0 and
            audit_v4.get("same_defects_absent_from_v5") is True and
            audit_v4.get(
                "v6_closed_object_required_property_mismatch_count") == 0 and
            audit_v4.get("same_defects_absent_from_v6") is True,
        "receipt_recorded_three_root_defects_and_additional_fourth_audit_defect_validated":
            len(v4_supersession.get("root_defects", [])) == 3 and
            contract.get("rejected_unpublished_predecessor_v4", {}).get(
                "additional_false_static_audit_claim") ==
                "V4_AUDIT_ASSERTED_ALL_CLOSED_OBJECT_REQUIRED_SETS_EQUAL_PROPERTY_SETS_WHILE_FROZEN_PREDECESSOR_PIN_AND_LIVE_PREDECESSOR_PIN_LEFT_OBJECT_SHA256_OPTIONAL" and
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
            audit_v4.get("same_defects_absent_from_v6") is True,
        "v4_rejection_supersession_receipt_held_and_terminally_replayed":
            v4_receipt_guard.fd >= 0,
        "both_receipts_strict_JSON_object_closed":
            transition_object_sha256 == digest({
                key: value for key, value in transition.items()
                if key != "object_sha256"}) and
            audit_object_sha256 == digest({
                key: value for key, value in audit.items()
                if key != "object_sha256"}),
        "both_receipts_held_and_terminally_replayed_across_full_consumer_run":
            by_path[V16_TO_V16R2_TRANSITION].fd >= 0 and
            by_path[STATIC_AUDIT_V16R2].fd >= 0,
        "post_source_receipts_are_runtime_trust_anchor_without_source_hash_cycle":
            successor["independent_verifier_assembler_authority_consumer"]
                ["file_sha256"] == self_guard.file_sha256 and
            audited["independent_verifier_assembler_authority_consumer"]
                ["file_sha256"] == self_guard.file_sha256,
        "cold_launcher_identity": launcher_identity,
        "cold_launch_manifest_identity": manifest_identity,
        "cold_launch_outer_identity": cold_outer_identity,
        "cold_launch_outer_object_sha256": cold_outer_object_sha256,
        "cold_launch_nonproducer_exact7_actual_hashes_equal_and_producer_hash_crossdeclared_by_transition_audit_manifest_outer":
            cold_manifest == exact8_expected and
            cold_outer.get("exact8_ordered_entries") == outer_expected_entries and
            successor["build_only_producer"]["file_sha256"] == PRODUCER_SOURCE_PIN and
            audited["build_only_producer"]["file_sha256"] == PRODUCER_SOURCE_PIN and
            cold_manifest[3]["file_sha256"] == PRODUCER_SOURCE_PIN and
            cold_outer["exact8_ordered_entries"][3]["file_sha256"] ==
                PRODUCER_SOURCE_PIN,
        "cold_launch_manifest_and_outer_held_and_terminally_replayed":
            by_path[COLD_LAUNCH_MANIFEST].fd >= 0 and
            by_path[COLD_LAUNCH_OUTER].fd >= 0,
        **chronology,
        "sole_external_static_file_anchor_equals_actual_held_launcher_and_outer_reconstructed":
            os.environ.get(COLD_LAUNCHER_SHA_ENV) == launcher_file_sha256 and
            cold_outer.get("cold_launcher", {}).get("file_sha256") ==
                launcher_file_sha256 and
            cold_outer.get("cold_launch_manifest", {}).get("file_sha256") ==
                cold_manifest_file_sha256 and
            cold_outer.get("sole_external_static_file_anchor_is_launcher_sha256") is True,
        "declared_external_tcb_matches_cold_launch_proof":
            cold_outer.get("declared_external_tcb") == [
                "EXTERNAL_HELD_FD_SEALED_MEMFD_BOOTSTRAP",
                "PYTHON3_ISOLATED_INTERPRETER",
                "LINUX_KERNEL_OPENAT2_STATX_MEMFD_PROCFS"],
        "consumer_exec_fd_is_fresh_sealed_memfd":
            stat.S_ISREG(self_guard.exec_before.st_mode) and
            stat.S_IMODE(self_guard.exec_before.st_mode) == 0o444 and
            self_guard.exec_before.st_nlink == 0 and
            self_guard.exec_seals == REQUIRED_EXEC_SEALS,
        "consumer_exec_fd_distinct_from_installed_source_fd":
            (self_guard.exec_before.st_dev, self_guard.exec_before.st_ino) !=
                (self_guard.before.st_dev, self_guard.before.st_ino),
        "consumer_exec_memfd_required_seals_valid":
            self_guard.exec_seals == REQUIRED_EXEC_SEALS,
        "consumer_exec_bytes_equal_installed_source_bytes":
            self_guard.exec_raw == self_guard.raw and
            self_guard.exec_file_sha256 == self_guard.file_sha256,
        "consumer_exec_and_installed_source_terminal_replayed": True,
        "producer_identity_metadata": producer_identity_metadata,
        "producer_content_opened_read_or_hashed": False,
        "producer_identity_metadata_held": True,
        "cold_exact10_identities_pairwise_unique_and_same_statx_mount":
            len(set(exact10_identities)) == 10 and len(set(exact10_mount_ids)) == 1,
    }


def _static_freeze_is_valid(proof: Mapping[str, Any]) -> bool:
    boolean_names = (
        "transition_pins_current_consumer_SELF",
        "static_audit_pins_current_consumer_SELF_transition_contract_schema_rejection_and_producer",
        "rejected_unpublished_predecessor_v4_validated",
        "ordered_provisional_exact8_validated",
        "current_exact8_first_member_is_v14_registry_shape_drift_supersession_receipt",
        "rejected_prepublication_v13_supersession_receipt_validated",
        "published_then_officially_rejected_predecessor_v5_validated",
        "published_then_officially_rejected_predecessor_v6_validated",
        "v7_official_rejection_shared_v8_predecessor_held_fd",
        "published_then_officially_rejected_predecessor_v7_validated",
        "v7_publication_lock_continuity_incident_validated",
        "v8_official_rejection_shared_v9_predecessor_held_fd",
        "published_then_officially_rejected_predecessor_v8_validated",
        "published_then_officially_rejected_predecessor_v9_validated",
        "published_then_officially_rejected_predecessor_v10_validated",
        "published_then_officially_rejected_predecessor_v11_validated",
        "published_then_officially_rejected_predecessor_v12_validated",
        "historical_rejection_exact_keyset_witness_validated",
        "v5_strict_bool_three_hard_seven_risk_present_and_v6_absent",
        "predecessor_v4_rejection_supersession_regression_validated",
        "receipt_recorded_three_root_defects_and_additional_fourth_audit_defect_validated",
        "v4_rejection_supersession_receipt_held_and_terminally_replayed",
        "both_receipts_strict_JSON_object_closed",
        "both_receipts_held_and_terminally_replayed_across_full_consumer_run",
        "post_source_receipts_are_runtime_trust_anchor_without_source_hash_cycle",
        "cold_launch_nonproducer_exact7_actual_hashes_equal_and_producer_hash_crossdeclared_by_transition_audit_manifest_outer",
        "cold_launch_manifest_and_outer_held_and_terminally_replayed",
        "all_exact8_mtime_not_after_final_ctime",
        "max_exact8_final_mtime_ctime_before_manifest_mtime",
        "manifest_mtime_not_after_final_ctime",
        "manifest_final_ctime_before_outer_mtime",
        "outer_mtime_not_after_final_ctime",
        "physical_exact8_freeze_then_manifest_freeze_then_outer_freeze_chronology",
        "sole_external_static_file_anchor_equals_actual_held_launcher_and_outer_reconstructed",
        "declared_external_tcb_matches_cold_launch_proof",
        "consumer_exec_fd_is_fresh_sealed_memfd",
        "consumer_exec_fd_distinct_from_installed_source_fd",
        "consumer_exec_memfd_required_seals_valid",
        "consumer_exec_bytes_equal_installed_source_bytes",
        "consumer_exec_and_installed_source_terminal_replayed",
        "producer_identity_metadata_held",
        "cold_exact10_identities_pairwise_unique_and_same_statx_mount",
    )
    return (set(proof) == {
        "published_then_officially_rejected_predecessor_v5",
        "v5_official_rejection_identity",
        "v5_official_rejection_file_sha256",
        "v5_official_rejection_object_sha256",
        "v4_rejection_supersession_identity",
        "v4_rejection_supersession_file_sha256",
        "v4_rejection_supersession_object_sha256",
        "published_then_officially_rejected_predecessor_v6",
        "v6_official_rejection_identity",
        "v6_official_rejection_file_sha256",
        "v6_official_rejection_object_sha256",
        "published_then_officially_rejected_predecessor_v7",
        "v7_publication_lock_continuity_incident",
        "v7_official_rejection_identity",
        "v7_official_rejection_file_sha256",
        "v7_official_rejection_object_sha256",
        "published_then_officially_rejected_predecessor_v8",
        "v8_official_rejection", "v8_official_rejection_identity",
        "v8_official_rejection_file_sha256",
        "v8_official_rejection_object_sha256",
        "v8_forbidden_positive_and_stage_surface_count",
        "published_then_officially_rejected_predecessor_v9",
        "published_then_officially_rejected_predecessor_v10",
        "published_then_officially_rejected_predecessor_v11",
        "published_then_officially_rejected_predecessor_v12",
        "v12_v5_rejection_shape_incident",
        "v12_official_rejection_identity",
        "v12_official_rejection_file_sha256",
        "v12_official_rejection_object_sha256",
        "historical_rejection_exact_keyset_witness",
        "append_only_history_unique_file_identity_count",
        "v16_to_v16r2_transition_identity", "static_audit_identity",
        "transition_object_sha256", "static_audit_object_sha256", *boolean_names,
        "cold_launcher_identity", "cold_launch_manifest_identity",
        "cold_launch_outer_identity", "cold_launch_outer_object_sha256",
        "producer_identity_metadata", "producer_content_opened_read_or_hashed",
    } and all(proof.get(name) is True for name in boolean_names) and
        proof.get("producer_content_opened_read_or_hashed") is False and
        proof.get("v4_rejection_supersession_identity", {}).get(
            "file_sha256") == V4_REJECTION_SUPERSESSION_FILE_PIN and
        proof.get("v4_rejection_supersession_file_sha256") ==
            V4_REJECTION_SUPERSESSION_FILE_PIN and
        proof.get("v4_rejection_supersession_object_sha256") ==
            V4_REJECTION_SUPERSESSION_OBJECT_PIN and
        proof.get("v5_official_rejection_identity", {}).get(
            "file_sha256") == V5_OFFICIAL_REJECTION_FILE_PIN and
        proof.get("v5_official_rejection_file_sha256") ==
            V5_OFFICIAL_REJECTION_FILE_PIN and
        proof.get("v5_official_rejection_object_sha256") ==
            V5_OFFICIAL_REJECTION_OBJECT_PIN and
        proof.get("v6_official_rejection_identity", {}).get(
            "file_sha256") == V6_OFFICIAL_REJECTION_FILE_PIN and
        proof.get("v6_official_rejection_file_sha256") ==
            V6_OFFICIAL_REJECTION_FILE_PIN and
        proof.get("v6_official_rejection_object_sha256") ==
            V6_OFFICIAL_REJECTION_OBJECT_PIN and
        proof.get("v7_official_rejection_identity", {}).get(
            "file_sha256") == V7_OFFICIAL_REJECTION_FILE_PIN and
        proof.get("v7_official_rejection_file_sha256") ==
            V7_OFFICIAL_REJECTION_FILE_PIN and
        proof.get("v7_official_rejection_object_sha256") ==
            V7_OFFICIAL_REJECTION_OBJECT_PIN and
        proof.get("v8_official_rejection_identity", {}).get(
            "file_sha256") == V8_OFFICIAL_REJECTION_FILE_PIN and
        proof.get("v8_official_rejection_file_sha256") ==
            V8_OFFICIAL_REJECTION_FILE_PIN and
        proof.get("v8_official_rejection_object_sha256") ==
            V8_OFFICIAL_REJECTION_OBJECT_PIN and
        proof.get("published_then_officially_rejected_predecessor_v5", {}).get(
            "strict_bool_defect_census") == _v5_strict_bool_defect_census() and
        proof.get("published_then_officially_rejected_predecessor_v6") ==
            _expected_published_then_rejected_v6_proof() and
        proof.get("published_then_officially_rejected_predecessor_v7") ==
            _expected_published_then_rejected_v7_proof() and
        proof.get("published_then_officially_rejected_predecessor_v8") ==
            _expected_published_then_rejected_v8_proof() and
        proof.get("published_then_officially_rejected_predecessor_v9") ==
            _expected_published_then_rejected_v9_proof() and
        proof.get("published_then_officially_rejected_predecessor_v10") ==
            _expected_published_then_rejected_v10_proof() and
        proof.get("published_then_officially_rejected_predecessor_v11") ==
            _expected_published_then_rejected_v11_proof() and
        proof.get("published_then_officially_rejected_predecessor_v12") ==
            _expected_published_then_rejected_v12_proof() and
        proof.get("v12_v5_rejection_shape_incident") ==
            V12_V5_REJECTION_SHAPE_INCIDENT and
        proof.get("v12_official_rejection_identity", {}).get(
            "file_sha256") == V12_OFFICIAL_REJECTION_FILE_PIN and
        proof.get("v12_official_rejection_file_sha256") ==
            V12_OFFICIAL_REJECTION_FILE_PIN and
        proof.get("v12_official_rejection_object_sha256") ==
            V12_OFFICIAL_REJECTION_OBJECT_PIN and
        proof.get("historical_rejection_exact_keyset_witness") ==
            list(HISTORICAL_REJECTION_EXACT_KEYSET_WITNESS) and
        proof.get("append_only_history_unique_file_identity_count") ==
            V16R2_TERMINAL_UNIQUE_LIVE_IDENTITY_COUNT and
        proof.get("v7_publication_lock_continuity_incident") ==
            _validated_v7_publication_lock_continuity_incident() and
        proof.get("v16_to_v16r2_transition_identity", {}).get("file_sha256") is not None and
        proof.get("static_audit_identity", {}).get("file_sha256") is not None)


def _candidate_verification_guards(include_completion: bool = False) -> HeldInputSet:
    specifications = [
        (CANDIDATE_A, MEMBERS, "candidate-A exact9"),
        (CANDIDATE_B, MEMBERS, "candidate-B exact9"),
        (VERIFICATION_A, (VERIFICATION_FILE,), "verification-A exact1"),
        (VERIFICATION_B, (VERIFICATION_FILE,), "verification-B exact1"),
    ]
    if include_completion:
        specifications.append(
            (COMMITTED_COMPLETION, COMPLETION_MEMBERS, "committed completion exact4"))
    return hold_surfaces(specifications)


def _all_mounts_one(guard: HeldInputSet, label: str) -> None:
    mount_ids = {item.mount_id for item in guard.files}
    mount_ids.update(item.mount_id for item in guard.directories)
    need(len(mount_ids) == 1, label + ":single statx mount; reject mount aliases")


def _new_hidden_stage(
        parent: HeldCommitParent, name: str,
        directory: bool) -> tuple[Path, HeldCommitParent | None]:
    need("/" not in name and name not in {"", ".", ".."},
         "deterministic hidden stage is one exact held-parent component")
    stage = parent.path / name
    if directory:
        writer = parent.mkdir_exclusive(name, 0o700)
        need(writer.path == stage,
             "mkdirat immediately-held deterministic stage path")
        return stage, writer
    return stage, None


def build_verification(
        orientation: str, self_guard: HeldSelf,
        c78_guard: HeldInputSet,
        fixed_guard: HeldInputSet,
        runtime_parent: HeldCommitParent,
        producer_guard: HeldOpaqueMetadata) -> None:
    need(orientation in {"a", "b"}, "verification orientation")
    primary = CANDIDATE_A if orientation == "a" else CANDIDATE_B
    peer = CANDIDATE_B if orientation == "a" else CANDIDATE_A
    destination = VERIFICATION_A if orientation == "a" else VERIFICATION_B
    need(destination.parent == RUNTIME,
         "fixed checkpoint-keyed verification destination; collision decided only by NOCLOBBER")
    c42_guard = hold_c42_full10_union_candidate9()
    policy_guard = _static_policy_guards()
    v3_guard, v3_source_metadata = hold_v3_predecessor_exact10()
    v4_guard, v4_source_metadata = hold_v4_rejected_static_draft7()
    v5_guard, v5_source_metadata = hold_v5_published_exact10()
    v6_guard, v6_source_metadata = hold_v6_published_exact10()
    v7_guard, v7_source_metadata = hold_v7_published_exact10()
    v8_guard, v8_source_metadata = hold_v8_published_exact10()
    v9_guard, v9_source_metadata = hold_v9_published_exact10()
    v10_guard, v10_source_metadata = hold_v10_published_exact10()
    v11_guard, v11_source_metadata = hold_v11_published_exact10()
    commit_parent = runtime_parent
    need(commit_parent.path == RUNTIME and
         commit_parent.inherited_launcher_coordination_fd is True,
         "verification uses launcher-owned coordination parent fd")
    candidate_guard = hold_surfaces([
        (CANDIDATE_A, MEMBERS, "candidate-A exact9"),
        (CANDIDATE_B, MEMBERS, "candidate-B exact9"),
    ])
    stage_guard: HeldInputSet | None = None
    created_files: list[HeldPinnedInput] = []
    stage_writer: HeldCommitParent | None = None
    try:
        freeze_proof = static_freeze_proof(
            policy_guard, self_guard, producer_guard,
            v5_guard, v5_source_metadata, v6_guard, v6_source_metadata,
            v7_guard, v7_source_metadata, v8_guard, v8_source_metadata,
            v9_guard, v9_source_metadata, v10_guard, v10_source_metadata,
            v11_guard, v11_source_metadata)
        need(_static_freeze_is_valid(freeze_proof),
             "verification requires final post-source static freeze")
        context = reconstruct_publication_context(
            primary, peer, self_guard, producer_guard, candidate_guard,
            c78_guard, c42_guard, fixed_guard, policy_guard,
            v3_guard, v3_source_metadata, v4_guard, v4_source_metadata,
            v5_guard, v5_source_metadata, v6_guard, v6_source_metadata,
            v7_guard, v7_source_metadata, v8_guard, v8_source_metadata,
            v9_guard, v9_source_metadata, v10_guard, v10_source_metadata,
            v11_guard, v11_source_metadata)
        verification_raw = context["verification_raw"]
        need(held_child_lstat_or_absent(
                 commit_parent, destination.name,
                 "verification fixed destination pre-stage probe") is None,
             "verification target already exists; reject without creating stage")
        expected_stage = (VERIFICATION_STAGE_A if orientation == "a"
                          else VERIFICATION_STAGE_B)
        stage, stage_writer = _new_hidden_stage(
            commit_parent, expected_stage.name, True)
        need(stage_writer is not None and stage == expected_stage,
             "fixed checkpoint-keyed verification stage")
        created_files.append(
            stage_writer.exclusive_file(VERIFICATION_FILE, verification_raw))
        candidate_by_path = {item.path: item for item in candidate_guard.files}
        need(max(candidate_by_path[CANDIDATE_A / OUTER_RECEIPT].before.st_mtime_ns,
                 candidate_by_path[CANDIDATE_B / OUTER_RECEIPT].before.st_mtime_ns) <
             created_files[0].before.st_mtime_ns,
             "both candidate outers precede verification")
        os.fchmod(stage_writer.fd, 0o555)
        os.fsync(stage_writer.fd)
        stage_writer.terminal_identity()
        stage_directory_guard = HeldDirectory(
            stage, {VERIFICATION_FILE}, 0o555, 2,
            "verification hidden stage exact1")
        need(stage_directory_guard.identity ==
             (stage_writer.before.st_dev, stage_writer.before.st_ino) and
             stage_directory_guard.mount_id == stage_writer.mount_id,
             "verification directory has been continuously held since mkdirat")
        stage_guard = HeldInputSet(created_files, [stage_directory_guard])
        created_files = []
        need(stage_guard.files[0].raw == verification_raw,
             "verification hidden stage canonical expected bytes")
        identities = [item.identity for item in candidate_guard.files + stage_guard.files]
        need(len(identities) == 19 and len(set(identities)) == 19,
             "candidate18 plus verification identity globally unique")
        c42_guard.terminal_replay()
        c78_guard.terminal_replay()
        fixed_guard.terminal_replay()
        terminal_replay_v3_predecessor_exact10(
            v3_guard, v3_source_metadata)
        terminal_replay_v4_rejected_static_draft7(
            v4_guard, v4_source_metadata)
        terminal_replay_v5_published_exact10(
            v5_guard, v5_source_metadata)
        terminal_replay_v6_published_exact10(
            v6_guard, v6_source_metadata)
        terminal_replay_v7_published_exact10(
            v7_guard, v7_source_metadata)
        terminal_replay_v8_published_exact10(
            v8_guard, v8_source_metadata)
        terminal_replay_v9_published_exact10(
            v9_guard, v9_source_metadata)
        terminal_replay_v10_published_exact10(
            v10_guard, v10_source_metadata)
        terminal_replay_v11_published_exact10(
            v11_guard, v11_source_metadata)
        terminal_replay_v12_published_exact10()
        producer_guard.terminal_replay()
        policy_guard.terminal_replay()
        candidate_guard.terminal_replay()
        stage_guard.terminal_replay()
        self_guard.terminal_replay()
        stage_directory = stage_guard.directories[0]
        rename_noreplace(
            commit_parent, stage.name, destination.name,
            stage_directory.identity, stage_directory.mount_id)
    finally:
        if stage_guard is not None:
            stage_guard.close()
        else:
            for item in reversed(created_files):
                item.close()
        if stage_writer is not None:
            stage_writer.close()
        candidate_guard.close()
        policy_guard.close()
        v3_guard.close()
        for item in reversed(v3_source_metadata):
            item.close()
        v4_guard.close()
        for item in reversed(v4_source_metadata):
            item.close()
        v6_guard.close()
        for item in reversed(v6_source_metadata):
            item.close()
        v7_guard.close()
        for item in reversed(v7_source_metadata):
            item.close()
        v8_guard.close()
        for item in reversed(v8_source_metadata):
            item.close()
        v9_guard.close()
        for item in reversed(v9_source_metadata):
            item.close()
        v10_guard.close()
        for item in reversed(v10_source_metadata):
            item.close()
        v11_guard.close()
        for item in reversed(v11_source_metadata):
            item.close()
        v5_guard.close()
        for item in reversed(v5_source_metadata):
            item.close()
        c42_guard.close()


def read_verification_surface(
        directory: Path, expected_verification: Mapping[str, Any],
        surface_guard: HeldInputSet
        ) -> tuple[bytes, dict[str, Any], tuple[int, int]]:
    need(directory in {VERIFICATION_A, VERIFICATION_B},
         "fixed checkpoint-keyed verification directory")
    by_path = {item.path: item for item in surface_guard.files}
    by_directory = {item.path: item for item in surface_guard.directories}
    item = by_path.get(directory / VERIFICATION_FILE)
    directory_guard = by_directory.get(directory)
    need(isinstance(item, HeldPinnedInput) and
         isinstance(directory_guard, HeldDirectory) and
         directory_guard.names == {VERIFICATION_FILE},
         "verification exact held one-member surface")
    raw, identity = item.raw, item.identity
    value = strict_json(raw, "C79g verification surface")
    verify_object(value, "C79g verification surface")
    attacks = value.get("coherent_attacks", {})
    names = attacks.get("names")
    records = attacks.get("records")
    need(set(value) == {
             "schema", "status", "verifier_file_sha256", "declared_producer_file_sha256",
             "producer_hash_is_declarative_binding_only",
             "producer_source_content_opened_read_decoded_parsed_compiled_imported_or_executed",
             "verification_orientation_is_order_invariant", "candidate_member_file_sha256",
             "dual_candidate_build_directories_mode", "dual_candidate_members_mode",
             "dual_candidate_members_single_link", "dual_candidate_members_byte_identical",
             "dual_candidate_corresponding_inodes_distinct",
             "all_18_candidate_member_identities_globally_unique", "reconstruction",
             "coherent_attacks", "all_attacks_fail_closed",
             "v3_official_later_rejection_object_sha256", "verification_credit",
             "standalone_non_authoritative", "formal_credit_authority",
             "precursor_credits_zero", "canonical_pointer_written", "D02_started",
             "object_sha256"} and
         value == dict(expected_verification) and
         raw == canonical(dict(expected_verification)) + b"\n" and
         value.get("status") ==
             "PASS_INDEPENDENT_C79G_V16R2__EXACT_137_ATTACKS__STANDALONE_ZERO_CREDIT" and
         value.get("verifier_file_sha256") == expected_verification["verifier_file_sha256"] and
         value.get("declared_producer_file_sha256") == PRODUCER_SOURCE_PIN and
         value.get("producer_hash_is_declarative_binding_only") is True and
         value.get("producer_source_content_opened_read_decoded_parsed_compiled_imported_or_executed") is False and
         value.get("verification_orientation_is_order_invariant") is True and
         value.get("candidate_member_file_sha256") ==
             expected_verification["candidate_member_file_sha256"] and
         value.get("dual_candidate_build_directories_mode") == "0555" and
         value.get("dual_candidate_members_mode") == "0444" and
         value.get("dual_candidate_members_single_link") is True and
         value.get("dual_candidate_members_byte_identical") is True and
         value.get("dual_candidate_corresponding_inodes_distinct") is True and
         value.get("all_18_candidate_member_identities_globally_unique") is True and
         value.get("verification_credit") == ZERO and
         value.get("standalone_non_authoritative") is True and
         value.get("formal_credit_authority") ==
             "ONLY_EXTERNALLY_PINNED_COLD_LAUNCHER_WRAPPER_AFTER_HELD_CHILD_AND_POST_CHILD_TERMINAL_REPLAY" and
         value.get("v3_official_later_rejection_object_sha256") == V3_OFFICIAL_REJECTION_OBJECT_PIN and
         value.get("canonical_pointer_written") is False and
         value.get("D02_started") is False and value.get("precursor_credits_zero") is True and
         isinstance(value.get("reconstruction"), dict) and
         set(value["reconstruction"]) == {
             "overlay_rows", "successor_rows", "reflection_parent_rows",
             "derived_final_four_class_census", "authority_partition",
             "public_global_unresolved", "closure",
             "C42_C53_C55B_direct_Kraft_pair_count"} and
         value["reconstruction"] == expected_verification["reconstruction"] and
         set(attacks) == {"attack_count", "rejected", "names",
                          "name_order_sha256", "records"} and
         attacks.get("attack_count") == 137 and attacks.get("rejected") == 137 and
         isinstance(names, list) and len(names) == 137 and len(set(names)) == 137 and
         attacks.get("name_order_sha256") == ATTACK_NAME_ORDER_PIN and
         _line_sequence_sha256(names) == ATTACK_NAME_ORDER_PIN and
         isinstance(records, dict) and set(records) == set(names) and
         all(set(record) == {"status", "validator_route", "actual_rejection_stage"} and
             record.get("status") == "FAIL_CLOSED" and
             record.get("validator_route") == attack_validator_route(name) and
             isinstance(record.get("actual_rejection_stage"), str) and
             bool(record["actual_rejection_stage"])
             for name, record in records.items()) and
         value.get("all_attacks_fail_closed") is True,
         "verification exact independently reconstructed production semantics")
    return raw, value, identity


def completion_install_proof(stage: Path) -> dict[str, Any]:
    return {
        "staging_path": str(stage.relative_to(ROOT)),
        "staging_created_exclusively": True,
        "staging_initial_mode": "0700",
        "committed_path": str(COMMITTED_COMPLETION.relative_to(ROOT)),
        "linux_openat2_statx_renameat2_available_or_fail_closed": True,
        "held_parent_dirfd_identity_and_mount_stable": True,
        "launcher_owned_coordination_parent_fd_required": True,
        "official_writer_coordination_lock_api":
            "launcher_owned_fcntl.flock(LOCK_EX)",
        "all_official_runtime_writers_must_share_coordination_lock": True,
        "coordination_lock_not_claimed_as_same_uid_or_filesystem_admin_security_boundary": True,
        "staging_and_target_are_single_components_under_same_held_parent_dirfd": True,
        "same_filesystem": True,
        "exact_member_count": 4,
        "exact_member_order": list(COMPLETION_MEMBERS),
        "all_members_mode": "0444",
        "all_members_nlink": 1,
        "all_members_fsynced": True,
        "sealed_directory_mode": "0555",
        "sealed_directory_fsynced": True,
        "same_fd_terminal_reread_before_commit": True,
        "terminal_path_identity_rescan_before_commit": True,
        "commit_operation": "RENAMEAT2_RENAME_NOREPLACE",
        "renameat2_fallback_allowed": False,
        "target_did_not_preexist": True,
        "postrename_destination_is_prechecked_staging_inode": True,
        "postrename_source_component_absent": True,
        "parent_directory_fsync_required_for_crash_durability_after_namespace_commit": True,
        "parent_fsync_not_claimed_to_precede_namespace_visibility": True,
        "postrename_semantic_gate_or_publication_performed": False,
        "overwrite_reuse_or_cross_device_copy_used": False,
    }


def construct_completion_surface(
        context: Mapping[str, Any], verification_a_raw: bytes,
        verification_a: Mapping[str, Any], verification_b_raw: bytes,
        verification_b: Mapping[str, Any], install_proof: Mapping[str, Any]
        ) -> tuple[dict[str, bytes], dict[str, Any]]:
    actual = context["actual"]
    completion_verification_raw = verification_a_raw
    completion_receipt = close_object({
        "schema": SCHEMA + ".pre-outer-completion-receipt",
        "status": "PASS_DUAL_ISOLATED_CANDIDATES_AND_VERIFICATIONS__ZERO_CREDIT_AWAIT_COMPOSITE_AUTHORITY",
        "candidate_A_result_object_sha256": actual["result"]["object_sha256"],
        "candidate_B_result_object_sha256": actual["result"]["object_sha256"],
        "candidate_A_outer_object_sha256": actual["outer"]["object_sha256"],
        "candidate_B_outer_object_sha256": actual["outer"]["object_sha256"],
        "verification_A_object_sha256": verification_a["object_sha256"],
        "verification_B_object_sha256": verification_b["object_sha256"],
        "dual_candidate_bytes_identical_inodes_distinct": True,
        "all_18_candidate_member_identities_globally_unique": True,
        "dual_verification_bytes_identical_inodes_distinct": True,
        "independent_no_producer_reconstruction_replayed": True,
        "v3_official_later_rejection_object_sha256": V3_OFFICIAL_REJECTION_OBJECT_PIN,
        "completion_credit": dict(ZERO),
        "standalone_non_authoritative": True,
        "canonical_pointer_written": False,
        "D02_started": False,
        "partial_publication_policy": "REJECT_AND_PRESERVE_NEVER_OVERWRITE_OR_REUSE",
        "atomic_commit_required": "LINUX_RENAMEAT2_RENAME_NOREPLACE_NO_FALLBACK",
        "completion_install": dict(install_proof),
        "candidate_install": copy.deepcopy(actual["outer"]["candidate_install"]),
    })
    completion_receipt_raw = canonical(completion_receipt) + b"\n"
    ordered22: list[tuple[str, str]] = []
    for prefix in ("candidate-A", "candidate-B"):
        ordered22.extend((sha(actual["raw"][name]), prefix + "/" + name)
                         for name in MEMBERS)
    ordered22.extend([
        (sha(verification_a_raw), "verification-A/" + VERIFICATION_FILE),
        (sha(verification_b_raw), "verification-B/" + VERIFICATION_FILE),
        (sha(completion_verification_raw), "completion/" + COMPLETION_VERIFICATION),
        (sha(completion_receipt_raw), "completion/" + COMPLETION_RECEIPT),
    ])
    need(len(ordered22) == 22 and len({name for _, name in ordered22}) == 22,
         "one-global manifest exact ordered22")
    global_manifest_raw = b"".join(
        f"{file_sha256}  {entry_name}\n".encode("ascii")
        for file_sha256, entry_name in ordered22)
    final_outer = close_object({
        "schema": SCHEMA + ".final-outer-receipt",
        "status": "PASS_COMMITTED_COMPLETION_SURFACE__STANDALONE_ZERO_CREDIT__AWAIT_COMPOSITE_AUTHORITY",
        "completion_receipt_object_sha256": completion_receipt["object_sha256"],
        "completion_verification_file_sha256": sha(completion_verification_raw),
        "dual_verification_object_sha256": verification_a["object_sha256"],
        "effective_checkpoint_object_sha256": UPSTREAM_CHECKPOINT_OBJECT_PIN,
        "public_global_unresolved": 0,
        "closure": dict(CLOSURE),
        "full_successor_row_count": UNIVERSE,
        "reflection_parent_row_count": PAIR_COUNT,
        "one_global_manifest_file_sha256": sha(global_manifest_raw),
        "one_global_manifest_entry_count": 22,
        "one_global_manifest_order": [entry_name for _, entry_name in ordered22],
        "completion_exact_member_count": 4,
        "post_outer_terminal_replay_target_count": 24,
        "final_outer_published_last": True,
        "formal_global_closure_credit": 0,
        "D02_unlock": False,
        "D02_gate_credit": 0,
        "D02_task_credit": 0,
        "D02_formal_pending_task_count": PENDING_D02,
        "D02_started": False,
        "precursor_formal_credits_zero": True,
        "canonical_pointer_written": False,
        "standalone_non_authoritative": True,
        "authority_requires_seal_surface_live_replay_and_no_later_rejection": True,
    })
    final_outer_raw = canonical(final_outer) + b"\n"
    raw = {
        COMPLETION_VERIFICATION: completion_verification_raw,
        COMPLETION_RECEIPT: completion_receipt_raw,
        GLOBAL_MANIFEST: global_manifest_raw,
        FINAL_OUTER: final_outer_raw,
    }
    return raw, {
        "verification": context["verification"],
        "completion_receipt": completion_receipt,
        "final_outer": final_outer,
        "ordered22": ordered22,
        "candidate_install": copy.deepcopy(actual["outer"]["candidate_install"]),
        "completion_install": dict(install_proof),
        "completion_member_file_sha256": {
            name: sha(raw[name]) for name in COMPLETION_MEMBERS},
    }


def validate_global_chronology(
        guard: HeldInputSet, completion_dir: Path) -> None:
    by_path = {item.path: item for item in guard.files}
    exact24_paths = (
        [CANDIDATE_A / name for name in MEMBERS] +
        [CANDIDATE_B / name for name in MEMBERS] +
        [VERIFICATION_A / VERIFICATION_FILE, VERIFICATION_B / VERIFICATION_FILE] +
        [completion_dir / name for name in COMPLETION_MEMBERS])
    need(len(exact24_paths) == 24 and set(by_path) == set(exact24_paths),
         "chronology consumes the exact held24 fd set")
    candidate_latest = max(
        by_path[CANDIDATE_A / OUTER_RECEIPT].before.st_mtime_ns,
        by_path[CANDIDATE_B / OUTER_RECEIPT].before.st_mtime_ns)
    verification_times = [
        by_path[VERIFICATION_A / VERIFICATION_FILE].before.st_mtime_ns,
        by_path[VERIFICATION_B / VERIFICATION_FILE].before.st_mtime_ns,
    ]
    completion_times = [
        by_path[completion_dir / COMPLETION_VERIFICATION].before.st_mtime_ns,
        by_path[completion_dir / COMPLETION_RECEIPT].before.st_mtime_ns,
        by_path[completion_dir / GLOBAL_MANIFEST].before.st_mtime_ns,
        by_path[completion_dir / FINAL_OUTER].before.st_mtime_ns,
    ]
    need(candidate_latest < min(verification_times) and
         max(verification_times) < completion_times[0] <
             completion_times[1] < completion_times[2] < completion_times[3],
         "candidate_latest < verification_earliest and verification_latest < "
         "completion_verification < preouter < manifest < outer")
    need(len(exact24_paths) == 24 and
         all(path == completion_dir / FINAL_OUTER or
             by_path[path].before.st_mtime_ns < completion_times[3]
             for path in exact24_paths),
         "final outer unique latest across exact24")


def _surface_descriptor(guard: HeldInputSet) -> list[dict[str, Any]]:
    return [{
        "path": str(item.path.relative_to(ROOT)),
        "file_sha256": sha(item.raw),
        "st_dev": item.before.st_dev,
        "st_ino": item.before.st_ino,
        "stx_mnt_id": item.mount_id,
        "st_size": item.before.st_size,
        "mode": f"{stat.S_IMODE(item.before.st_mode):04o}",
        "nlink": item.before.st_nlink,
        "opened_by_exact_lexical_path_with_O_NOFOLLOW": True,
        "opened_with_openat2_RESOLVE_BENEATH_NO_SYMLINKS_NO_MAGICLINKS_NO_XDEV": True,
        "statx_mount_id_stable": True,
        "initial_fd_identity_equals_terminal_fd_identity": True,
        "initial_bytes_equal_terminal_same_fd_bytes": True,
        "terminal_fd_identity_equals_terminal_path_lstat_identity": True,
        "parent_components_securely_walked": True,
        "regular_file": True,
    } for item in guard.files]


def _one_identity(item: HeldPinnedInput) -> dict[str, Any]:
    holder = HeldInputSet([item], [])
    return _surface_descriptor(holder)[0]


def exact_paths_object() -> dict[str, str]:
    return {
        "candidate_A": str(CANDIDATE_A.relative_to(ROOT)),
        "candidate_B": str(CANDIDATE_B.relative_to(ROOT)),
        "verification_A": str(VERIFICATION_A.relative_to(ROOT)),
        "verification_B": str(VERIFICATION_B.relative_to(ROOT)),
        "committed_completion": str(COMMITTED_COMPLETION.relative_to(ROOT)),
        "authority_seal": str(AUTHORITY_SEAL.relative_to(ROOT)),
        "v16r2_rejection_namespace": str(REJECTION_NAMESPACE.relative_to(ROOT)),
        "v16r2_later_rejection": str(LATER_REJECTION.relative_to(ROOT)),
    }


def official_writer_coordination_lock_object(
        runtime_parent: HeldCommitParent) -> dict[str, Any]:
    need(runtime_parent.path == RUNTIME and
         runtime_parent.inherited_launcher_coordination_fd is True and
         runtime_parent.launcher_exclusive_lock_confirmed_by_independent_probe is True,
         "official-writer coordination lock exact inherited runtime parent")
    runtime_parent.terminal_identity()
    return {
        "path": str(RUNTIME.relative_to(ROOT)),
        "held_parent_st_dev": runtime_parent.before.st_dev,
        "held_parent_st_ino": runtime_parent.before.st_ino,
        "held_parent_statx_mnt_id": runtime_parent.mount_id,
        "lock_api": "launcher_owned_fcntl.flock(LOCK_EX)",
        "received_from_frozen_launcher_as_inherited_open_file_description_fd": True,
        "child_duplicated_and_identity_mount_checked_inherited_fd": True,
        "launcher_exclusive_lock_confirmed_by_independent_nonblocking_probe": True,
        "child_calls_LOCK_UN": False,
        "launcher_lock_owner_scope_requirement_includes_child_live_protocol": True,
        "mandatory_for_all_official_runtime_writers": True,
        "acquired_before_any_runtime_evidence_or_commit_surface_open_for_this_command": True,
        "required_final_hold_scope": [
            "inner_canonical_stdout_flush",
            "launcher_commit_request",
            "absolute_last_dynamic_terminal_replay",
            "live_ACK_canonical_stdout_flush",
            "launcher_positive_wrapper_raw_fd1_final_newline_write",
            "launcher_RELEASE",
        ],
        "protocol_requires_launcher_RELEASE_before_normal_child_guard_close": True,
        "coordination_lock_is_not_claimed_as_a_security_boundary_against_noncooperating_same_uid_or_filesystem_administrator": True,
    }


def official_writer_coordination_lock_policy_object(
        live_lock: Mapping[str, Any]) -> dict[str, Any]:
    """Project a live lock proof onto a reboot-stable persisted policy.

    The authority seal must never persist st_dev/st_ino/stx_mnt_id.  Those
    values remain mandatory in the fresh preseal/consumer/ACK proofs and are
    compared only within one live invocation.
    """
    need(
        live_lock.get("path") == str(RUNTIME.relative_to(ROOT)) and
        live_lock.get("lock_api") == "launcher_owned_fcntl.flock(LOCK_EX)" and
        live_lock.get(
            "received_from_frozen_launcher_as_inherited_open_file_description_fd") is True and
        live_lock.get(
            "child_duplicated_and_identity_mount_checked_inherited_fd") is True and
        live_lock.get(
            "launcher_exclusive_lock_confirmed_by_independent_nonblocking_probe") is True and
        live_lock.get("child_calls_LOCK_UN") is False and
        live_lock.get(
            "launcher_lock_owner_scope_requirement_includes_child_live_protocol") is True and
        live_lock.get("mandatory_for_all_official_runtime_writers") is True and
        live_lock.get(
            "acquired_before_any_runtime_evidence_or_commit_surface_open_for_this_command") is True and
        live_lock.get("required_final_hold_scope") == [
            "inner_canonical_stdout_flush",
            "launcher_commit_request",
            "absolute_last_dynamic_terminal_replay",
            "live_ACK_canonical_stdout_flush",
            "launcher_positive_wrapper_raw_fd1_final_newline_write",
            "launcher_RELEASE",
        ] and
        live_lock.get(
            "protocol_requires_launcher_RELEASE_before_normal_child_guard_close") is True and
        live_lock.get(
            "coordination_lock_is_not_claimed_as_a_security_boundary_against_noncooperating_same_uid_or_filesystem_administrator") is True,
        "live official-writer lock satisfies stable persisted policy")
    return {
        "path": str(RUNTIME.relative_to(ROOT)),
        "lock_api": "launcher_owned_fcntl.flock(LOCK_EX)",
        "launcher_owned_open_file_description_must_be_inherited_by_child": True,
        "child_must_duplicate_and_identity_mount_check_inherited_fd": True,
        "launcher_exclusive_lock_must_be_confirmed_by_independent_nonblocking_probe": True,
        "child_calls_LOCK_UN": False,
        "launcher_lock_owner_scope_requirement_includes_child_live_protocol": True,
        "mandatory_for_all_official_runtime_writers": True,
        "acquired_before_any_runtime_evidence_or_commit_surface_open_for_each_command": True,
        "required_final_hold_scope": [
            "inner_canonical_stdout_flush",
            "launcher_commit_request",
            "absolute_last_dynamic_terminal_replay",
            "live_ACK_canonical_stdout_flush",
            "launcher_positive_wrapper_raw_fd1_final_newline_write",
            "launcher_RELEASE",
        ],
        "protocol_requires_launcher_RELEASE_before_normal_child_guard_close": True,
        "coordination_lock_is_not_claimed_as_a_security_boundary_against_noncooperating_same_uid_or_filesystem_administrator": True,
        "live_st_dev_st_ino_and_stx_mnt_id_must_not_be_persisted": True,
    }


def terminal_replay24_object(surface_guard: HeldInputSet) -> dict[str, Any]:
    identities = _surface_descriptor(surface_guard)
    need(len(identities) == 24, "terminalReplay24 exact ordered identities")
    return {
        "target_count": 24,
        "ordered_identities": identities,
        "candidate_A_count": 9,
        "candidate_B_count": 9,
        "verification_A_count": 1,
        "verification_B_count": 1,
        "completion_count": 4,
        "all_path_identities_exact": True,
        "all_same_fd_initial_and_terminal_bytes_equal": True,
        "all_member_inodes_pairwise_distinct": True,
        "candidate_A_B_complete_inode_sets_disjoint": True,
        "final_outer_unique_latest": True,
        "directory_universes_terminally_rescanned": True,
    }


def full10_identity_object(c42_guard: HeldInputSet) -> dict[str, Any]:
    ordered_names = list(C42_C53_PATHS)
    need(len(ordered_names) == 10 and len(c42_guard.files) == 16,
         "full10 plus C42 candidate9 union exact16")
    by_path = {item.path: item for item in c42_guard.files}
    ordered_items = [by_path[C42_C53_PATHS[name]] for name in ordered_names]
    identities = _surface_descriptor(HeldInputSet(ordered_items, []))
    expected_modes = [f"{C42_C53_EXPECTED_MODES[name]:04o}" for name in ordered_names]
    need([identity["mode"] for identity in identities] == expected_modes and
         len(c42_guard.directories) == 3,
         "full10 exact heterogeneous file modes and three held directories")
    return {
        "authority": "C42_INSTALLED_PARENT_CONSERVATION_VIA_C53_C55B_JOIN",
        "fixed_input_count": 10,
        "ordered_names": ordered_names,
        "ordered_paths": [str(C42_C53_PATHS[name].relative_to(ROOT))
                          for name in ordered_names],
        "ordered_file_sha256": [C42_C53_PINS[name] for name in ordered_names],
        "ordered_expected_modes": expected_modes,
        "ordered_identities": identities,
        "all_identity_modes_equal_ordered_expected_modes": True,
        "members_join_contract_name_path_hash_by_index": True,
        "all_held_open_across_full_consumer_run": True,
        "all_same_fd_bytes_terminally_replayed": True,
        "all_terminal_path_identities_equal_held_fd_identities": True,
        "all_pairwise_inode_distinct": True,
        "C42_candidate_exact_member_count": 9,
        "C42_held_directory_count": 3,
        "C42_candidate_directory_expected_mode": "0755",
        "C42_candidate_directory_expected_nlink": 2,
        "C42_independent_audit_directory_expected_mode": "0700",
        "C42_independent_audit_directory_expected_nlink": 2,
        "C42_independent_audit_directory_exact_member_count": 1,
        "C42_installation_receipt_directory_expected_mode": "0500",
        "C42_installation_receipt_directory_expected_nlink": 2,
        "C42_installation_receipt_directory_exact_member_count": 1,
        "all_three_directories_held_and_terminally_replayed": True,
        "historical_modes_are_exact_observed_snapshot_guards_not_immutability_claims": True,
        "C42_manifest_exact_ordered_entry_count": 8,
        "C42_all_manifest_members_terminally_replayed": True,
        "parent_count": PAIR_COUNT,
        "all_parent_Kraft_conservation": "1",
        "C72_boolean_used_as_authority": False,
    }


def _domain_root(domain: str, value: Mapping[str, Any]) -> str:
    return sha(domain.encode("ascii") + b"\x00" + canonical(dict(value)))


def _candidate_surface_proof(
        install_protocol: Mapping[str, Any],
        deterministic_sources_absent: bool,
        static_freeze_valid: bool) -> dict[str, Any]:
    need(dict(install_protocol) == candidate_install_protocol(),
         "candidate proof derives from exact frozen orientation-invariant install protocol")
    return {
        "candidate_A_path": str(CANDIDATE_A.relative_to(ROOT)),
        "candidate_B_path": str(CANDIDATE_B.relative_to(ROOT)),
        "exact_member_count_each": 9,
        "directory_mode_each": "0555",
        "member_mode_each": "0444",
        "member_nlink_each": 1,
        "bytes_identical_by_corresponding_name": True,
        "corresponding_inodes_distinct": True,
        "complete_nine_member_inode_sets_disjoint": True,
        "candidate_outer_credit_zero": True,
        "both_paths_installed_with_RENAME_NOREPLACE":
            install_protocol["commit_operation"] == "RENAMEAT2_RENAME_NOREPLACE" and
            install_protocol["ordinary_rename_replace_or_fallback_allowed"] is False and
            deterministic_sources_absent is True,
        "orientation_invariant_install_descriptor_exact":
            dict(install_protocol) == candidate_install_protocol(),
        "staging_path_template": install_protocol["staging_path_template"],
        "actual_orientation_or_stage_path_persisted_in_candidate_bytes":
            install_protocol[
                "actual_orientation_or_stage_path_persisted_in_candidate_bytes"],
        "static_freeze_implementation_binding_valid": static_freeze_valid is True,
        "live_consumer_rederives_and_validates_fixed_A_B_paths":
            install_protocol[
                "live_consumer_rederives_fixed_A_B_paths_and_revalidates_both_surfaces"] is True and
            deterministic_sources_absent is True,
    }


def _verification_surface_proof(
        deterministic_sources_absent: bool) -> dict[str, Any]:
    return {
        "verification_A_path": str(VERIFICATION_A.relative_to(ROOT)),
        "verification_B_path": str(VERIFICATION_B.relative_to(ROOT)),
        "exact_member_count_each": 1,
        "directory_mode_each": "0555",
        "member_mode_each": "0444",
        "member_nlink_each": 1,
        "bytes_identical": True,
        "inodes_distinct": True,
        "both_equal_independently_constructed_expected_bytes": True,
        "exact_attack_count_each": 137,
        "all_attacks_fail_closed": True,
        "verification_credit_zero": True,
        "both_paths_installed_with_RENAME_NOREPLACE":
            deterministic_sources_absent is True,
    }


def _standalone_outer_proof(completion_objects: Mapping[str, Any]) -> dict[str, Any]:
    final_outer = completion_objects["final_outer"]
    return close_object({
        "schema": SCHEMA + ".standalone-final-outer",
        "status": "PASS_PRESEAL_OUTER__ZERO_CREDIT__NON_AUTHORITATIVE",
        "effective_checkpoint_object_sha256": UPSTREAM_CHECKPOINT_OBJECT_PIN,
        "pre_outer_completion_receipt_object_sha256":
            completion_objects["completion_receipt"]["object_sha256"],
        "one_global_manifest_file_sha256":
            final_outer["one_global_manifest_file_sha256"],
        "one_global_manifest_exact_ordered_entries": 22,
        "final_outer_published_last_within_preseal_surface": True,
        "post_outer_terminal_replay_required": True,
        "non_authoritative_reason": "STANDALONE_PRESEAL_OUTER_ZERO_CREDIT",
        "authority_decision": "NO_GO_PRESEAL",
        "standalone_credit": dict(ZERO),
    })


def preseal_root(surface_guard: HeldInputSet, c42_guard: HeldInputSet,
                 completion_objects: Mapping[str, Any],
                 rejection: Mapping[str, Any],
                 committed_stage_absence: Mapping[str, bool],
                 freeze_proof: Mapping[str, Any],
                 runtime_parent: HeldCommitParent) -> dict[str, Any]:
    descriptor = _surface_descriptor(surface_guard)
    need(len(descriptor) == 24 and
         len({(item["st_dev"], item["st_ino"]) for item in descriptor}) == 24,
         "preseal exact24 global identity uniqueness")
    body: dict[str, Any] = {
        "schema": PRESEAL_SCHEMA,
        "status": "PASS_COMMITTED_COMPLETION__PRESEAL_ZERO_CREDIT",
        "effective_checkpoint_object_sha256": UPSTREAM_CHECKPOINT_OBJECT_PIN,
        "contract_file_sha256": CONTRACT_FILE_PIN,
        "contract_object_sha256": CONTRACT_OBJECT_PIN,
        "closed_schema_file_sha256": CLOSED_SCHEMA_FILE_PIN,
        "published_then_officially_rejected_predecessor_v5": copy.deepcopy(
            freeze_proof[
                "published_then_officially_rejected_predecessor_v5"]),
        "v5_official_rejection_identity": copy.deepcopy(
            freeze_proof["v5_official_rejection_identity"]),
        "v5_official_rejection_file_sha256":
            V5_OFFICIAL_REJECTION_FILE_PIN,
        "v5_official_rejection_object_sha256":
            V5_OFFICIAL_REJECTION_OBJECT_PIN,
        "published_then_officially_rejected_predecessor_v6": copy.deepcopy(
            freeze_proof[
                "published_then_officially_rejected_predecessor_v6"]),
        "v6_official_rejection_identity": copy.deepcopy(
            freeze_proof["v6_official_rejection_identity"]),
        "v6_official_rejection_file_sha256":
            V6_OFFICIAL_REJECTION_FILE_PIN,
        "v6_official_rejection_object_sha256":
            V6_OFFICIAL_REJECTION_OBJECT_PIN,
        "published_then_officially_rejected_predecessor_v7": copy.deepcopy(
            freeze_proof[
                "published_then_officially_rejected_predecessor_v7"]),
        "v7_publication_lock_continuity_incident": copy.deepcopy(
            freeze_proof["v7_publication_lock_continuity_incident"]),
        "v7_official_rejection_identity": copy.deepcopy(
            freeze_proof["v7_official_rejection_identity"]),
        "v7_official_rejection_file_sha256":
            V7_OFFICIAL_REJECTION_FILE_PIN,
        "v7_official_rejection_object_sha256":
            V7_OFFICIAL_REJECTION_OBJECT_PIN,
        "published_then_officially_rejected_predecessor_v8": copy.deepcopy(
            freeze_proof[
                "published_then_officially_rejected_predecessor_v8"]),
        "published_then_officially_rejected_predecessor_v9": copy.deepcopy(
            freeze_proof[
                "published_then_officially_rejected_predecessor_v9"]),
        "published_then_officially_rejected_predecessor_v10": copy.deepcopy(
            freeze_proof[
                "published_then_officially_rejected_predecessor_v10"]),
        "published_then_officially_rejected_predecessor_v11": copy.deepcopy(
            _expected_published_then_rejected_v11_proof()),
        "published_then_officially_rejected_predecessor_v12": copy.deepcopy(
            _expected_published_then_rejected_v12_proof()),
        "v4_rejection_supersession_identity": copy.deepcopy(
            freeze_proof["v4_rejection_supersession_identity"]),
        "v4_rejection_supersession_file_sha256":
            freeze_proof["v4_rejection_supersession_identity"]["file_sha256"],
        "v4_rejection_supersession_object_sha256":
            freeze_proof["v4_rejection_supersession_object_sha256"],
        "v4_rejection_supersession_held_and_replayed_before_preseal_root": True,
        "cold_launcher_file_sha256":
            freeze_proof["cold_launcher_identity"]["file_sha256"],
        "cold_manifest_file_sha256":
            freeze_proof["cold_launch_manifest_identity"]["file_sha256"],
        "cold_outer_file_sha256":
            freeze_proof["cold_launch_outer_identity"]["file_sha256"],
        "cold_outer_object_sha256":
            freeze_proof["cold_launch_outer_object_sha256"],
        "exact_paths": exact_paths_object(),
        "official_writer_coordination_lock":
            official_writer_coordination_lock_object(runtime_parent),
        "candidate_surface": _candidate_surface_proof(
            completion_objects["candidate_install"],
            committed_stage_absence.get("candidate_A") is True and
            committed_stage_absence.get("candidate_B") is True,
            _static_freeze_is_valid(freeze_proof)),
        "verification_surface": _verification_surface_proof(
            committed_stage_absence.get("verification_A") is True and
            committed_stage_absence.get("verification_B") is True),
        "completion_install": dict(completion_objects["completion_install"]),
        "one_global_manifest_file_sha256":
            completion_objects["final_outer"]["one_global_manifest_file_sha256"],
        "one_global_manifest_exact_ordered_entries": 22,
        "standalone_outer": _standalone_outer_proof(completion_objects),
        "terminal_replay_24": terminal_replay24_object(surface_guard),
        "full10_identity": full10_identity_object(c42_guard),
        "full_successor_row_count": UNIVERSE,
        "reflection_parent_row_count": PAIR_COUNT,
        "public_global_unresolved": 0,
        "closure": dict(CLOSURE),
        "authority_seal_present_in_preseal_object": False,
        "authority_decision": "NO_GO_PRESEAL",
        "preseal_credit": dict(ZERO),
        "preseal_root_domain": "CM2_C79G_V16R2_PRESEAL_ROOT_V2",
    }
    rejection_object = rejection.get("object_sha256")
    need(rejection_object == V3_OFFICIAL_REJECTION_OBJECT_PIN,
         "preseal binds exact official v3 later-rejection object")
    need(freeze_proof["v4_rejection_supersession_identity"]["file_sha256"] ==
             V4_REJECTION_SUPERSESSION_FILE_PIN and
         freeze_proof["v4_rejection_supersession_object_sha256"] ==
             V4_REJECTION_SUPERSESSION_OBJECT_PIN,
         "preseal binds exact v4 rejection/supersession receipt")
    need(freeze_proof[
             "published_then_officially_rejected_predecessor_v5"] ==
             _expected_published_then_rejected_v5_proof() and
         freeze_proof["v5_official_rejection_file_sha256"] ==
             V5_OFFICIAL_REJECTION_FILE_PIN and
         freeze_proof["v5_official_rejection_object_sha256"] ==
             V5_OFFICIAL_REJECTION_OBJECT_PIN,
         "preseal binds exact published-then-rejected v5 predecessor")
    need(freeze_proof[
             "published_then_officially_rejected_predecessor_v6"] ==
             _expected_published_then_rejected_v6_proof() and
         freeze_proof["v6_official_rejection_file_sha256"] ==
             V6_OFFICIAL_REJECTION_FILE_PIN and
         freeze_proof["v6_official_rejection_object_sha256"] ==
             V6_OFFICIAL_REJECTION_OBJECT_PIN,
         "preseal binds exact published-then-rejected v6 predecessor")
    need(freeze_proof[
             "published_then_officially_rejected_predecessor_v7"] ==
             _expected_published_then_rejected_v7_proof() and
         freeze_proof["v7_publication_lock_continuity_incident"] ==
             _validated_v7_publication_lock_continuity_incident() and
         freeze_proof["v7_official_rejection_file_sha256"] ==
             V7_OFFICIAL_REJECTION_FILE_PIN and
         freeze_proof["v7_official_rejection_object_sha256"] ==
             V7_OFFICIAL_REJECTION_OBJECT_PIN,
         "preseal binds exact interrupted-and-rejected v7 predecessor")
    need(freeze_proof[
             "published_then_officially_rejected_predecessor_v8"] ==
             _expected_published_then_rejected_v8_proof() and
         freeze_proof["v8_official_rejection_file_sha256"] ==
             V8_OFFICIAL_REJECTION_FILE_PIN and
         freeze_proof["v8_official_rejection_object_sha256"] ==
             V8_OFFICIAL_REJECTION_OBJECT_PIN,
         "preseal binds exact rollout-aborted-and-rejected v8 predecessor")
    need(freeze_proof[
             "published_then_officially_rejected_predecessor_v9"] ==
             _expected_published_then_rejected_v9_proof(),
         "preseal binds exact proof-shape-drift-and-rejected v9 predecessor")
    need(freeze_proof[
             "published_then_officially_rejected_predecessor_v10"] ==
             _expected_published_then_rejected_v10_proof(),
         "preseal binds exact label-prefix-regression-and-rejected v10 predecessor")
    need(freeze_proof[
             "published_then_officially_rejected_predecessor_v11"] ==
             _expected_published_then_rejected_v11_proof() and
         freeze_proof[
             "published_then_officially_rejected_predecessor_v12"] ==
             _expected_published_then_rejected_v12_proof(),
         "preseal binds exact rejected v11 then v12 predecessors")
    completion_root = digest([
        {"filename": name,
         "file_sha256": completion_objects["completion_member_file_sha256"][name]}
        for name in COMPLETION_MEMBERS])
    ordered22_digest = digest([
        {"file_sha256": file_sha256, "entry_name": entry_name}
        for file_sha256, entry_name in completion_objects["ordered22"]])
    replay24_expected_order_digest = _line_sequence_sha256(
        item["path"] for item in descriptor)
    body["preseal_root_sha256"] = sha(
        b"CM2_C79G_V16R2_PRESEAL_ROOT_V2" +
        UPSTREAM_CHECKPOINT_OBJECT_PIN.encode("ascii") +
        completion_root.encode("ascii") +
        ordered22_digest.encode("ascii") +
        replay24_expected_order_digest.encode("ascii") +
        rejection_object.encode("ascii") +
        V4_REJECTION_SUPERSESSION_FILE_PIN.encode("ascii") +
        V4_REJECTION_SUPERSESSION_OBJECT_PIN.encode("ascii") +
        V5_OFFICIAL_REJECTION_FILE_PIN.encode("ascii") +
        V5_OFFICIAL_REJECTION_OBJECT_PIN.encode("ascii") +
        V6_OFFICIAL_REJECTION_FILE_PIN.encode("ascii") +
        V6_OFFICIAL_REJECTION_OBJECT_PIN.encode("ascii") +
        V7_OFFICIAL_REJECTION_FILE_PIN.encode("ascii") +
        V7_OFFICIAL_REJECTION_OBJECT_PIN.encode("ascii") +
        V7_PUBLICATION_LOCK_CONTINUITY_INCIDENT[
            "object_sha256"].encode("ascii") +
        V8_OFFICIAL_REJECTION_FILE_PIN.encode("ascii") +
        V8_OFFICIAL_REJECTION_OBJECT_PIN.encode("ascii") +
        sha(canonical(V8_ROLLOUT_CONTROL_FLOW_INCIDENT)).encode("ascii") +
        V9_OFFICIAL_REJECTION_FILE_PIN.encode("ascii") +
        V9_OFFICIAL_REJECTION_OBJECT_PIN.encode("ascii") +
        sha(canonical(
            V9_V6_HELD_SELF_IDENTITY_DEFECT_SHAPE_DRIFT_INCIDENT)).encode(
                "ascii") +
        V10_OFFICIAL_REJECTION_FILE_PIN.encode("ascii") +
        V10_OFFICIAL_REJECTION_OBJECT_PIN.encode("ascii") +
        V10_REGRESSION_LABEL_PREFIX_INCIDENT_SHA256.encode("ascii") +
        V11_OFFICIAL_REJECTION_FILE_PIN.encode("ascii") +
        V11_OFFICIAL_REJECTION_OBJECT_PIN.encode("ascii") +
        V11_DUAL_VALIDATOR_DIVERGENCE_INCIDENT_SHA256.encode("ascii") +
        freeze_proof["cold_launcher_identity"]["file_sha256"].encode("ascii") +
        freeze_proof["cold_launch_manifest_identity"]["file_sha256"].encode("ascii") +
        freeze_proof["cold_launch_outer_identity"]["file_sha256"].encode("ascii") +
        freeze_proof["cold_launch_outer_object_sha256"].encode("ascii"))
    return close_object(body)
def _self_identity(self_guard: HeldSelf) -> dict[str, Any]:
    before = self_guard.before
    exec_before = self_guard.exec_before
    return {
        "path": str(SELF.relative_to(ROOT)),
        "file_sha256": self_guard.file_sha256,
        "st_dev": before.st_dev,
        "st_ino": before.st_ino,
        "stx_mnt_id": self_guard.mount_id,
        "st_size": before.st_size,
        "mode": "0444",
        "nlink": 1,
        "received_from_cold_launcher_as_distinct_inherited_exec_and_installed_source_fds":
            self_guard.exec_fd != self_guard.source_fd,
        "inherited_exec_fd_duplicated_before_any_evidence_or_output_access": True,
        "inherited_installed_source_fd_duplicated_before_any_evidence_or_output_access":
            True,
        "executed_via_exact_sealed_memfd_proc_self_fd_path":
            str(EXECUTED_SOURCE_PATH) ==
                "/proc/self/fd/" + os.environ[COLD_EXEC_FD_ENV],
        "executed_memfd_file_sha256": self_guard.exec_file_sha256,
        "executed_memfd_st_dev": exec_before.st_dev,
        "executed_memfd_st_ino": exec_before.st_ino,
        "executed_memfd_stx_mnt_id": self_guard.exec_mount_id,
        "executed_memfd_st_size": exec_before.st_size,
        "executed_memfd_mode": "0444",
        "executed_memfd_nlink": 0,
        "executed_memfd_required_seal_mask": REQUIRED_EXEC_SEALS,
        "executed_memfd_exact_write_grow_shrink_and_seal_seals":
            self_guard.exec_seals == REQUIRED_EXEC_SEALS,
        "executed_memfd_inode_distinct_from_installed_source_inode":
            (exec_before.st_dev, exec_before.st_ino) !=
                (before.st_dev, before.st_ino),
        "executed_memfd_bytes_equal_installed_source_bytes":
            self_guard.exec_raw == self_guard.raw and
            self_guard.exec_file_sha256 == self_guard.file_sha256,
        "installed_SELF_path_identity_equals_inherited_source_fd_identity": True,
        "installed_source_statx_mount_id_stable": True,
        "executed_memfd_statx_mount_id_stable": True,
        "installed_source_initial_fd_identity_equals_terminal_fd_identity": True,
        "sealed_exec_initial_fd_identity_equals_terminal_fd_identity": True,
        "sealed_exec_and_installed_source_initial_bytes_equal_terminal_bytes": True,
        "installed_source_terminal_fd_identity_equals_terminal_secure_path_identity":
            True,
        "parent_components_securely_walked": True,
        "installed_source_regular_file": True,
        "executed_memfd_regular_file": True,
    }


def independent_consumer_proof(
        preseal: Mapping[str, Any], self_guard: HeldSelf,
        freeze_proof: Mapping[str, Any]) -> dict[str, Any]:
    self_guard.terminal_replay()
    need(isinstance(_INCIDENT_AUTHORITY_HOLD,
                    HeldInheritedV14AuthorityExact12),
         "independent consumer retains inherited v14 exact12 authority")
    _INCIDENT_AUTHORITY_HOLD.terminal_replay()
    need(_INCIDENT_AUTHORITY_WITNESS == V10_COLON_PREFIX_WITNESS and
         _INCIDENT_AUTHORITY_V12_SHAPE == V12_V5_REJECTION_SHAPE_INCIDENT,
         "independent consumer retains both exact inherited-fd witnesses")
    return close_object({
        "schema": SCHEMA + ".independent-consumer-proof",
        "status": "PASS_INDEPENDENT_PRESEAL_CONSUMER__SEAL_ELIGIBLE__ZERO_CREDIT",
        "consumer_file_sha256": self_guard.file_sha256,
        "consumer_SELF_identity": _self_identity(self_guard),
        "consumer_exec_fd_is_fresh_sealed_memfd":
            stat.S_ISREG(self_guard.exec_before.st_mode) and
            stat.S_IMODE(self_guard.exec_before.st_mode) == 0o444 and
            self_guard.exec_before.st_nlink == 0 and
            self_guard.exec_seals == REQUIRED_EXEC_SEALS,
        "consumer_exec_fd_distinct_from_installed_source_fd":
            (self_guard.exec_before.st_dev, self_guard.exec_before.st_ino) !=
                (self_guard.before.st_dev, self_guard.before.st_ino),
        "consumer_exec_memfd_required_seals_valid":
            self_guard.exec_seals == REQUIRED_EXEC_SEALS,
        "consumer_exec_bytes_equal_installed_source_bytes":
            self_guard.exec_raw == self_guard.raw and
            self_guard.exec_file_sha256 == self_guard.file_sha256,
        "consumer_exec_and_installed_source_terminal_replayed": True,
        "current_v16r2_producer_source_content_opened_read_decoded_parsed_compiled_imported_or_executed": False,
        "v14_inherited_authority_exact12_held_and_terminally_replayed": True,
        "v10_colon_prefix_witness_independently_rederived_from_inherited_exact10_held_fds": True,
        "preseal_object_sha256": preseal["object_sha256"],
        "preseal_bytes_reconstructed_independently": True,
        "full_evidence_reconstructed_independently": True,
        "exact_attack_count_reexecuted": 137,
        "all_attacks_fail_closed": True,
        "both_verifications_equal_independently_constructed_expected_bytes": True,
        "exact_24_full_identity_validated": True,
        "full10_identity_validated": True,
        "C42_full10_union_candidate9_semantics_derived_only_from_full_run_held_fds": True,
        "C42_full10_union_candidate9_three_directories_held_across_full_command": True,
        "C55_C72_exact16_files_plus_shared_C53_head_held_across_full_command": True,
        "frozen_v3_exact7_readable_and_exact3_source_metadata_only_held_across_full_command": True,
        "published_v5_exact7_readable_exact3_source_metadata_only_plus_shared_official_rejection_held_across_full_command": True,
        "published_then_officially_rejected_predecessor_v5": copy.deepcopy(
            freeze_proof[
                "published_then_officially_rejected_predecessor_v5"]),
        "v5_official_rejection_identity": copy.deepcopy(
            freeze_proof["v5_official_rejection_identity"]),
        "v5_official_rejection_file_sha256":
            V5_OFFICIAL_REJECTION_FILE_PIN,
        "v5_official_rejection_object_sha256":
            V5_OFFICIAL_REJECTION_OBJECT_PIN,
        "published_then_officially_rejected_predecessor_v6": copy.deepcopy(
            freeze_proof[
                "published_then_officially_rejected_predecessor_v6"]),
        "v6_official_rejection_identity": copy.deepcopy(
            freeze_proof["v6_official_rejection_identity"]),
        "v6_official_rejection_file_sha256":
            V6_OFFICIAL_REJECTION_FILE_PIN,
        "v6_official_rejection_object_sha256":
            V6_OFFICIAL_REJECTION_OBJECT_PIN,
        "published_then_officially_rejected_predecessor_v7": copy.deepcopy(
            freeze_proof[
                "published_then_officially_rejected_predecessor_v7"]),
        "v7_publication_lock_continuity_incident": copy.deepcopy(
            freeze_proof["v7_publication_lock_continuity_incident"]),
        "v7_official_rejection_identity": copy.deepcopy(
            freeze_proof["v7_official_rejection_identity"]),
        "v7_official_rejection_file_sha256":
            V7_OFFICIAL_REJECTION_FILE_PIN,
        "v7_official_rejection_object_sha256":
            V7_OFFICIAL_REJECTION_OBJECT_PIN,
        "published_then_officially_rejected_predecessor_v8": copy.deepcopy(
            freeze_proof[
                "published_then_officially_rejected_predecessor_v8"]),
        "published_then_officially_rejected_predecessor_v9": copy.deepcopy(
            freeze_proof[
                "published_then_officially_rejected_predecessor_v9"]),
        "published_then_officially_rejected_predecessor_v10": copy.deepcopy(
            freeze_proof[
                "published_then_officially_rejected_predecessor_v10"]),
        "published_then_officially_rejected_predecessor_v11": copy.deepcopy(
            _expected_published_then_rejected_v11_proof()),
        "published_then_officially_rejected_predecessor_v12": copy.deepcopy(
            _expected_published_then_rejected_v12_proof()),
        "v4_rejection_supersession_identity": copy.deepcopy(
            freeze_proof["v4_rejection_supersession_identity"]),
        "v4_rejection_supersession_file_sha256":
            V4_REJECTION_SUPERSESSION_FILE_PIN,
        "v4_rejection_supersession_object_sha256":
            V4_REJECTION_SUPERSESSION_OBJECT_PIN,
        "v4_rejection_supersession_receipt_held_and_terminally_replayed_across_full_command": True,
        "rejected_v4_exact4_readable_and_exact3_source_metadata_only_held_across_full_command": True,
        "v3_official_rejection_shared_held_fd_reused_for_v3_and_v4_predecessor_proofs": True,
        "C78l_exact25_files_and_three_directories_held_across_full_command": True,
        "C78s_exact26_files_and_two_directories_held_across_full_command": True,
        "C78l_C78s_chronology_derived_only_from_held_fd_before_mtime": True,
        "C78l_C78s_terminal_same_fd_read_brackets_and_dirfd_universe_replay_required": True,
        "closure_validated": True,
        "public_global_unresolved": 0,
        "official_writer_coordination_lock_required":
            copy.deepcopy(preseal["official_writer_coordination_lock"]),
        "authority_seal_target_path": str(AUTHORITY_SEAL.relative_to(ROOT)),
        "authority_decision": "NO_GO_PRESEAL",
        "consumer_credit": dict(ZERO),
    })


def construct_authority_seal(
        preseal: Mapping[str, Any], consumer_proof: Mapping[str, Any],
        freeze_proof: Mapping[str, Any],
        stage_path: Path) -> dict[str, Any]:
    need(stage_path == AUTHORITY_STAGE,
         "authority stage exact deterministic checkpoint-keyed component")
    need(_static_freeze_is_valid(freeze_proof),
         "seal requires live post-source static freeze proof")
    return close_object({
        "schema": AUTHORITY_SEAL_SCHEMA,
        "status": "SEALED_COMPOSITE_INPUT__STANDALONE_ZERO_CREDIT",
        "effective_checkpoint_object_sha256": UPSTREAM_CHECKPOINT_OBJECT_PIN,
        "staging_path": str(stage_path.relative_to(ROOT)),
        "target_path": str(AUTHORITY_SEAL.relative_to(ROOT)),
        "consumer_file_sha256": consumer_proof["consumer_file_sha256"],
        "preseal_root_sha256": preseal["preseal_root_sha256"],
        "contract_file_sha256": CONTRACT_FILE_PIN,
        "contract_object_sha256": CONTRACT_OBJECT_PIN,
        "closed_schema_file_sha256": CLOSED_SCHEMA_FILE_PIN,
        "published_then_officially_rejected_predecessor_v5": copy.deepcopy(
            freeze_proof[
                "published_then_officially_rejected_predecessor_v5"]),
        "v5_official_rejection_identity": copy.deepcopy(
            freeze_proof["v5_official_rejection_identity"]),
        "v5_official_rejection_file_sha256":
            V5_OFFICIAL_REJECTION_FILE_PIN,
        "v5_official_rejection_object_sha256":
            V5_OFFICIAL_REJECTION_OBJECT_PIN,
        "published_then_officially_rejected_predecessor_v6": copy.deepcopy(
            freeze_proof[
                "published_then_officially_rejected_predecessor_v6"]),
        "v6_official_rejection_identity": copy.deepcopy(
            freeze_proof["v6_official_rejection_identity"]),
        "v6_official_rejection_file_sha256":
            V6_OFFICIAL_REJECTION_FILE_PIN,
        "v6_official_rejection_object_sha256":
            V6_OFFICIAL_REJECTION_OBJECT_PIN,
        "v4_rejection_supersession_identity": copy.deepcopy(
            freeze_proof["v4_rejection_supersession_identity"]),
        "v4_rejection_supersession_file_sha256":
            freeze_proof["v4_rejection_supersession_identity"]["file_sha256"],
        "v4_rejection_supersession_object_sha256":
            freeze_proof["v4_rejection_supersession_object_sha256"],
        "v4_rejection_supersession_identity_recomputed_from_held_fd": True,
        "published_then_officially_rejected_predecessor_v7": copy.deepcopy(
            freeze_proof[
                "published_then_officially_rejected_predecessor_v7"]),
        "v7_publication_lock_continuity_incident": copy.deepcopy(
            freeze_proof["v7_publication_lock_continuity_incident"]),
        "v7_official_rejection_identity": copy.deepcopy(
            freeze_proof["v7_official_rejection_identity"]),
        "v7_official_rejection_file_sha256":
            V7_OFFICIAL_REJECTION_FILE_PIN,
        "v7_official_rejection_object_sha256":
            V7_OFFICIAL_REJECTION_OBJECT_PIN,
        "published_then_officially_rejected_predecessor_v8": copy.deepcopy(
            freeze_proof[
                "published_then_officially_rejected_predecessor_v8"]),
        "published_then_officially_rejected_predecessor_v9": copy.deepcopy(
            freeze_proof[
                "published_then_officially_rejected_predecessor_v9"]),
        "published_then_officially_rejected_predecessor_v10": copy.deepcopy(
            freeze_proof[
                "published_then_officially_rejected_predecessor_v10"]),
        "published_then_officially_rejected_predecessor_v11": copy.deepcopy(
            _expected_published_then_rejected_v11_proof()),
        "published_then_officially_rejected_predecessor_v12": copy.deepcopy(
            _expected_published_then_rejected_v12_proof()),
        "v16_to_v16r2_transition_file_sha256":
            freeze_proof["v16_to_v16r2_transition_identity"]["file_sha256"],
        "v16_to_v16r2_transition_object_sha256":
            freeze_proof["transition_object_sha256"],
        "static_audit_file_sha256":
            freeze_proof["static_audit_identity"]["file_sha256"],
        "static_audit_object_sha256":
            freeze_proof["static_audit_object_sha256"],
        "cold_launcher_file_sha256":
            freeze_proof["cold_launcher_identity"]["file_sha256"],
        "cold_manifest_file_sha256":
            freeze_proof["cold_launch_manifest_identity"]["file_sha256"],
        "cold_outer_file_sha256":
            freeze_proof["cold_launch_outer_identity"]["file_sha256"],
        "cold_outer_object_sha256":
            freeze_proof["cold_launch_outer_object_sha256"],
        "official_writer_coordination_lock_policy":
            official_writer_coordination_lock_policy_object(
                preseal["official_writer_coordination_lock"]),
        "all_binding_hashes_recomputed_from_held_fds": True,
        "stage_file_mode": "0444",
        "stage_file_nlink": 1,
        "stage_file_and_directory_fsynced": True,
        "stage_same_fd_terminal_bytes_and_path_identity_replayed": True,
        "linux_openat2_statx_renameat2_available_or_fail_closed": True,
        "held_parent_dirfd_identity_and_mount_stable": True,
        "commit_operation": "RENAMEAT2_RENAME_NOREPLACE",
        "renameat2_fallback_allowed": False,
        "target_did_not_preexist": True,
        "postrename_destination_is_prechecked_stage_inode": True,
        "postrename_source_component_absent": True,
        "parent_directory_fsync_required_for_crash_durability_after_namespace_commit": True,
        "parent_fsync_not_claimed_to_precede_namespace_visibility": True,
        "postrename_semantic_gate_or_publication_performed": False,
        "seal_is_last_positive_path_non_revocation_persisted_semantic_commit": True,
        "only_permitted_later_persisted_semantic_action":
            "OFFICIAL_PERMANENT_REJECTION__ZERO_CREDIT__REVOCATION_ONLY",
        "authority_decision": "NO_GO_STANDALONE",
        "standalone_seal_credit": dict(ZERO),
    })


def v3_official_later_rejection_proof(
        rejection: Mapping[str, Any],
        receipt_guard: HeldPinnedInput) -> dict[str, Any]:
    identity = _one_identity(receipt_guard)
    identity["object_sha256"] = rejection["object_sha256"]
    return {
        "receipt_identity": identity,
        "receipt_path": str(V3_OFFICIAL_REJECTION.relative_to(ROOT)),
        "namespace_path": str(V3_OFFICIAL_REJECTION.parent.relative_to(ROOT)),
        "effective_checkpoint_object_sha256": UPSTREAM_CHECKPOINT_OBJECT_PIN,
        "ordered_predecessor_exact10": _expected_frozen_v3_exact10(),
        "all_ten_frozen_v3_pins_match_contract": True,
        "v3_execution_allowed": False,
        "v3_runtime_surfaces_authoritative": False,
        "v3_official_later_rejection_reason":
            "ORPHANED_OR_INCOMPLETE_C79G_V3_SURFACE",
        "v3_official_later_rejection_status":
            "PERMANENT_FAIL_CLOSED_REJECTION__ZERO_CREDIT",
        "v3_credit": dict(ZERO),
        "launcher_same_lock_live_predecessor_and_singleton_namespace_replay_required": True,
        "live_identity_or_timestamp_values_persisted": False,
        "successor_root_schema": COLD_ROOT_SCHEMA,
        "successor_exact_paths_match": True,
        "binding_direction_is_acyclic": True,
    }


def v4_rejection_supersession_proof(
        freeze_proof: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "receipt_identity": copy.deepcopy(
            freeze_proof["v4_rejection_supersession_identity"]),
        "receipt_path": str(V4_REJECTION_SUPERSESSION.relative_to(ROOT)),
        "receipt_file_sha256": V4_REJECTION_SUPERSESSION_FILE_PIN,
        "receipt_object_sha256": V4_REJECTION_SUPERSESSION_OBJECT_PIN,
        "effective_checkpoint_object_sha256": UPSTREAM_CHECKPOINT_OBJECT_PIN,
        "rejected_unpublished_predecessor_v4": True,
        "predecessor_v4_rejection_supersession_regression": True,
        "ordered_provisional_exact8": _expected_v4_provisional_exact8(),
        "all_eight_frozen_v4_pins_match_receipt": True,
        "all_eight_regular_0444_nlink1": True,
        "v4_manifest_absent": True,
        "v4_outer_absent": True,
        "v4_runtime_surface_count": 0,
        "receipt_recorded_root_defect_count": 3,
        "successor_discovered_additional_v4_audit_defect_count": 1,
        "v4_consumer_need_three_positional_arguments_defect_present": True,
        "v4_consumer_HeldOpaqueMetadata_missing_expected_mode_defect_present": True,
        "v4_launcher_pathname_preexec_TOCTOU_defect_present": True,
        "v4_static_audit_required_properties_false_claim_present": True,
        "successor_requires_all_four_v4_defects_absent": True,
        "v4_execution_allowed": False,
        "v4_runtime_surfaces_authoritative": False,
        "v4_credit": dict(ZERO),
        "launcher_same_lock_live_v4_provisional_exact8_and_receipt_replay_required": True,
        "receipt_identity_terminally_replayed": True,
        "binding_direction_is_acyclic": True,
    }


def postseal_live_replay_object(
        surface_guard: HeldInputSet, c42_guard: HeldInputSet,
        seal_guard: HeldPinnedInput, freeze_proof: Mapping[str, Any],
        durability_recovery_completed: bool) -> dict[str, Any]:
    need(durability_recovery_completed is True,
         "postseal proof requires fresh-invocation durability recovery")
    seal_identity = _one_identity(seal_guard)
    seal_identity["object_sha256"] = strict_json(
        seal_guard.raw, "postseal identity seal")["object_sha256"]
    return {
        "authority_seal_identity": seal_identity,
        "authority_seal_exact_path": str(AUTHORITY_SEAL.relative_to(ROOT)),
        "recorded_authority_staging_path_is_exact_single_component": True,
        "recorded_authority_staging_source_component_absent": True,
        "authority_seal_identity_path_and_hash_match_parsed_seal": True,
        "seal_opened_before_live_replay": True,
        "terminal_replay_24": terminal_replay24_object(surface_guard),
        "full10_identity": full10_identity_object(c42_guard),
        "v4_rejection_supersession_identity": copy.deepcopy(
            freeze_proof["v4_rejection_supersession_identity"]),
        "v4_rejection_supersession_identity_path_and_hash_match_static_freeze": True,
        "v4_rejection_supersession_terminal_same_fd_replay_completed": True,
        "published_then_officially_rejected_predecessor_v5": copy.deepcopy(
            freeze_proof[
                "published_then_officially_rejected_predecessor_v5"]),
        "v5_official_rejection_identity": copy.deepcopy(
            freeze_proof["v5_official_rejection_identity"]),
        "v5_official_rejection_identity_path_and_hash_match_static_freeze": True,
        "v5_official_rejection_terminal_same_fd_and_singleton_namespace_replay_completed": True,
        "published_then_officially_rejected_predecessor_v6": copy.deepcopy(
            freeze_proof[
                "published_then_officially_rejected_predecessor_v6"]),
        "v6_official_rejection_identity": copy.deepcopy(
            freeze_proof["v6_official_rejection_identity"]),
        "v6_official_rejection_identity_path_and_hash_match_static_freeze": True,
        "v6_official_rejection_terminal_same_fd_and_singleton_namespace_replay_completed": True,
        "published_then_officially_rejected_predecessor_v7": copy.deepcopy(
            freeze_proof[
                "published_then_officially_rejected_predecessor_v7"]),
        "v7_publication_lock_continuity_incident": copy.deepcopy(
            freeze_proof["v7_publication_lock_continuity_incident"]),
        "v7_official_rejection_identity": copy.deepcopy(
            freeze_proof["v7_official_rejection_identity"]),
        "v7_official_rejection_file_sha256":
            V7_OFFICIAL_REJECTION_FILE_PIN,
        "v7_official_rejection_object_sha256":
            V7_OFFICIAL_REJECTION_OBJECT_PIN,
        "v7_official_rejection_identity_path_and_hash_match_static_freeze": True,
        "v7_official_rejection_terminal_same_fd_and_singleton_namespace_replay_completed": True,
        "v7_publication_lock_continuity_incident_equal_static_freeze": True,
        "published_then_officially_rejected_predecessor_v8": copy.deepcopy(
            freeze_proof[
                "published_then_officially_rejected_predecessor_v8"]),
        "published_then_officially_rejected_predecessor_v9": copy.deepcopy(
            freeze_proof[
                "published_then_officially_rejected_predecessor_v9"]),
        "published_then_officially_rejected_predecessor_v10": copy.deepcopy(
            freeze_proof[
                "published_then_officially_rejected_predecessor_v10"]),
        "published_then_officially_rejected_predecessor_v11": copy.deepcopy(
            _expected_published_then_rejected_v11_proof()),
        "published_then_officially_rejected_predecessor_v12": copy.deepcopy(
            _expected_published_then_rejected_v12_proof()),
        "preseal_object_hash_recomputed_from_committed_bytes": True,
        "seal_binding_recomputed": True,
        "fresh_authorize_idempotent_durability_recovery_fsynced_all_exact24_member_fds_and_committed_directory_fds": True,
        "fresh_authorize_idempotent_durability_recovery_fsynced_rejection_namespace_runtime_parent_seal_and_authority_heads_parent": True,
        "fresh_authorize_idempotent_durability_recovery_terminal_replay_completed_before_inner_and_ACK": True,
        "all_replays_completed_before_terminal_rejection_scan": True,
    }


def recover_existing_authority_surface_durability(
        surface_guard: HeldInputSet, seal_guard: HeldPinnedInput,
        rejection_guard: HeldDirectory, runtime_parent: HeldCommitParent,
        authority_heads_parent: HeldCommitParent) -> bool:
    """Re-establish crash durability for a fully validated existing surface.

    Namespace visibility does not prove that the prior invocation reached its
    parent fsync.  A fresh positive authorize therefore re-fsyncs every held
    committed member, every committed directory, both namespace parents, and
    the seal before it may construct an inner object or participate in ACK.
    """
    need(len(surface_guard.files) == 24 and
         len(surface_guard.directories) == 5 and
         runtime_parent.path == RUNTIME and
         authority_heads_parent.path == AUTHORITY_HEADS,
         "fresh authorize durability recovery exact committed surface")
    for item in surface_guard.files:
        os.fsync(item.fd)
    for directory in surface_guard.directories:
        os.fsync(directory.fd)
    os.fsync(rejection_guard.fd)
    os.fsync(seal_guard.fd)
    os.fsync(runtime_parent.fd)
    os.fsync(authority_heads_parent.fd)
    surface_guard.terminal_replay()
    rejection_guard.terminal_replay()
    seal_guard.terminal_replay()
    runtime_parent.terminal_identity()
    authority_heads_parent.terminal_identity()
    return True


def no_later_rejection_object() -> dict[str, Any]:
    return {
        "namespace_exact_path": str(REJECTION_NAMESPACE.relative_to(ROOT)),
        "deterministic_target_exact_path": str(LATER_REJECTION.relative_to(ROOT)),
        "deterministic_target_absent": True,
        "namespace_at_rest_mode_0555": True,
        "official_reject_lock_held_0555_to_0755_to_0555_protocol": True,
        "partial_malformed_or_extra_entry_revokes_authority": True,
        "namespace_parent_securely_walked": True,
        "terminal_acceptance_scan_started_after_authority_seal_open": True,
        "terminal_scan_started_after_all_postseal_replays": True,
        "namespace_absence_or_directory_identity_checked_not_assumed": True,
        "accepted_well_formed_rejection_count": 0,
        "later_rejection_found": False,
        "namespace_state_or_identity_drift_found": False,
        "ambiguous_unreadable_or_symlink_state_found": False,
        "scan_fail_closed": True,
        "later_rejection_revokes_authority_immediately": True,
        "cached_scan_reuse_allowed": False,
    }


def _closed_object_equal(value: Mapping[str, Any]) -> bool:
    body = dict(value)
    claim = body.pop("object_sha256", None)
    return isinstance(claim, str) and claim == digest(body)


def binding_equalities_object(
        preseal: Mapping[str, Any], consumer_proof: Mapping[str, Any],
        seal: Mapping[str, Any], rejection: Mapping[str, Any],
        receipt_guard: HeldPinnedInput, freeze_proof: Mapping[str, Any],
        postseal: Mapping[str, Any], no_later: Mapping[str, Any],
        terminal_stage_absence: Mapping[str, bool],
        authority_root_sha256: str) -> dict[str, bool]:
    transition_identity = freeze_proof.get("v16_to_v16r2_transition_identity", {})
    audit_identity = freeze_proof.get("static_audit_identity", {})
    values: dict[str, bool] = {
        "checkpoint_equal_across_all_objects":
            preseal.get("effective_checkpoint_object_sha256") ==
                seal.get("effective_checkpoint_object_sha256") ==
                rejection.get("effective_checkpoint_object_sha256") ==
                UPSTREAM_CHECKPOINT_OBJECT_PIN,
        "exact_paths_equal_contract":
            _static_freeze_is_valid(freeze_proof) and
            preseal.get("exact_paths") == exact_paths_object() and
            set(terminal_stage_absence) == {
                "candidate_A", "candidate_B", "verification_A",
                "verification_B", "completion"} and
            all(terminal_stage_absence.values()),
        "v3_official_later_rejection_hashes_equal_contract":
            sha(receipt_guard.raw) == V3_OFFICIAL_REJECTION_FILE_PIN and
            rejection.get("object_sha256") == V3_OFFICIAL_REJECTION_OBJECT_PIN,
        "v4_rejection_supersession_file_and_object_hashes_equal_contract":
            freeze_proof.get("v4_rejection_supersession_identity", {}).get(
                "file_sha256") == V4_REJECTION_SUPERSESSION_FILE_PIN and
            freeze_proof.get("v4_rejection_supersession_object_sha256") ==
                V4_REJECTION_SUPERSESSION_OBJECT_PIN and
            preseal.get("v4_rejection_supersession_file_sha256") ==
                V4_REJECTION_SUPERSESSION_FILE_PIN and
            preseal.get("v4_rejection_supersession_object_sha256") ==
                V4_REJECTION_SUPERSESSION_OBJECT_PIN and
            seal.get("v4_rejection_supersession_file_sha256") ==
                V4_REJECTION_SUPERSESSION_FILE_PIN and
            seal.get("v4_rejection_supersession_object_sha256") ==
                V4_REJECTION_SUPERSESSION_OBJECT_PIN,
        "v4_rejection_supersession_identity_equal_static_freeze_and_postseal_replay":
            preseal.get("v4_rejection_supersession_identity") ==
                seal.get("v4_rejection_supersession_identity") ==
                postseal.get("v4_rejection_supersession_identity") ==
                freeze_proof.get("v4_rejection_supersession_identity") and
            postseal.get(
                "v4_rejection_supersession_identity_path_and_hash_match_static_freeze") is True and
            postseal.get(
                "v4_rejection_supersession_terminal_same_fd_replay_completed") is True,
        "rejected_unpublished_predecessor_v4_and_audit_regression_equal_transition_and_receipt":
            freeze_proof.get("rejected_unpublished_predecessor_v4_validated") is True and
            freeze_proof.get("ordered_provisional_exact8_validated") is True and
            freeze_proof.get(
                "predecessor_v4_rejection_supersession_regression_validated") is True and
            freeze_proof.get(
                "receipt_recorded_three_root_defects_and_additional_fourth_audit_defect_validated") is True,
        "published_then_officially_rejected_predecessor_v5_equal_across_static_preseal_consumer_seal_and_postseal":
            freeze_proof.get(
                "published_then_officially_rejected_predecessor_v5") ==
            preseal.get(
                "published_then_officially_rejected_predecessor_v5") ==
            consumer_proof.get(
                "published_then_officially_rejected_predecessor_v5") ==
            seal.get(
                "published_then_officially_rejected_predecessor_v5") ==
            postseal.get(
                "published_then_officially_rejected_predecessor_v5") and
            preseal.get("v5_official_rejection_file_sha256") ==
                seal.get("v5_official_rejection_file_sha256") ==
                V5_OFFICIAL_REJECTION_FILE_PIN and
            preseal.get("v5_official_rejection_object_sha256") ==
                seal.get("v5_official_rejection_object_sha256") ==
                V5_OFFICIAL_REJECTION_OBJECT_PIN and
            preseal.get("v5_official_rejection_identity") ==
                consumer_proof.get("v5_official_rejection_identity") ==
                seal.get("v5_official_rejection_identity") ==
                postseal.get("v5_official_rejection_identity") ==
                freeze_proof.get("v5_official_rejection_identity") and
            postseal.get(
                "v5_official_rejection_terminal_same_fd_and_singleton_namespace_replay_completed") is True,
        "published_then_officially_rejected_predecessor_v6_equal_across_static_preseal_consumer_seal_and_postseal":
            freeze_proof.get(
                "published_then_officially_rejected_predecessor_v6") ==
            preseal.get(
                "published_then_officially_rejected_predecessor_v6") ==
            consumer_proof.get(
                "published_then_officially_rejected_predecessor_v6") ==
            seal.get(
                "published_then_officially_rejected_predecessor_v6") ==
            postseal.get(
                "published_then_officially_rejected_predecessor_v6") and
            preseal.get("v6_official_rejection_file_sha256") ==
                seal.get("v6_official_rejection_file_sha256") ==
                V6_OFFICIAL_REJECTION_FILE_PIN and
            preseal.get("v6_official_rejection_object_sha256") ==
                seal.get("v6_official_rejection_object_sha256") ==
                V6_OFFICIAL_REJECTION_OBJECT_PIN and
            preseal.get("v6_official_rejection_identity") ==
                consumer_proof.get("v6_official_rejection_identity") ==
                seal.get("v6_official_rejection_identity") ==
                postseal.get("v6_official_rejection_identity") ==
                freeze_proof.get("v6_official_rejection_identity") and
            postseal.get(
                "v6_official_rejection_terminal_same_fd_and_singleton_namespace_replay_completed") is True,
        "published_then_officially_rejected_predecessor_v7_equal_across_static_preseal_consumer_seal_and_postseal":
            freeze_proof.get(
                "published_then_officially_rejected_predecessor_v7") ==
            preseal.get(
                "published_then_officially_rejected_predecessor_v7") ==
            consumer_proof.get(
                "published_then_officially_rejected_predecessor_v7") ==
            seal.get(
                "published_then_officially_rejected_predecessor_v7") ==
            postseal.get(
                "published_then_officially_rejected_predecessor_v7") and
            preseal.get("v7_official_rejection_file_sha256") ==
                seal.get("v7_official_rejection_file_sha256") ==
                V7_OFFICIAL_REJECTION_FILE_PIN and
            preseal.get("v7_official_rejection_object_sha256") ==
                seal.get("v7_official_rejection_object_sha256") ==
                V7_OFFICIAL_REJECTION_OBJECT_PIN and
            preseal.get("v7_official_rejection_identity") ==
                consumer_proof.get("v7_official_rejection_identity") ==
                seal.get("v7_official_rejection_identity") ==
                postseal.get("v7_official_rejection_identity") ==
                freeze_proof.get("v7_official_rejection_identity") and
            postseal.get(
                "v7_official_rejection_terminal_same_fd_and_singleton_namespace_replay_completed") is True,
        "v7_publication_lock_continuity_incident_equal_across_static_preseal_consumer_seal_and_postseal":
            freeze_proof.get("v7_publication_lock_continuity_incident") ==
                preseal.get("v7_publication_lock_continuity_incident") ==
                consumer_proof.get("v7_publication_lock_continuity_incident") ==
                seal.get("v7_publication_lock_continuity_incident") ==
                postseal.get("v7_publication_lock_continuity_incident") ==
                _validated_v7_publication_lock_continuity_incident() and
            postseal.get(
                "v7_publication_lock_continuity_incident_equal_static_freeze") is True,
        "published_then_officially_rejected_predecessor_v8_equal_across_static_preseal_consumer_seal_and_postseal":
            freeze_proof.get(
                "published_then_officially_rejected_predecessor_v8") ==
            preseal.get(
                "published_then_officially_rejected_predecessor_v8") ==
            consumer_proof.get(
                "published_then_officially_rejected_predecessor_v8") ==
            seal.get(
                "published_then_officially_rejected_predecessor_v8") ==
            postseal.get(
                "published_then_officially_rejected_predecessor_v8") ==
                _expected_published_then_rejected_v8_proof(),
        "published_then_officially_rejected_predecessor_v9_equal_across_static_preseal_consumer_seal_and_postseal":
            freeze_proof.get(
                "published_then_officially_rejected_predecessor_v9") ==
            preseal.get(
                "published_then_officially_rejected_predecessor_v9") ==
            consumer_proof.get(
                "published_then_officially_rejected_predecessor_v9") ==
            seal.get(
                "published_then_officially_rejected_predecessor_v9") ==
            postseal.get(
                "published_then_officially_rejected_predecessor_v9") ==
                _expected_published_then_rejected_v9_proof(),
        "published_then_officially_rejected_predecessor_v10_equal_across_static_preseal_consumer_seal_and_postseal":
            freeze_proof.get(
                "published_then_officially_rejected_predecessor_v10") ==
            preseal.get(
                "published_then_officially_rejected_predecessor_v10") ==
            consumer_proof.get(
                "published_then_officially_rejected_predecessor_v10") ==
            seal.get(
                "published_then_officially_rejected_predecessor_v10") ==
            postseal.get(
                "published_then_officially_rejected_predecessor_v10") ==
                _expected_published_then_rejected_v10_proof(),
        "published_then_officially_rejected_predecessor_v11_equal_across_static_preseal_consumer_seal_and_postseal":
            freeze_proof.get(
                "published_then_officially_rejected_predecessor_v11") ==
                _expected_published_then_rejected_v11_proof() and
            freeze_proof.get(
                "published_then_officially_rejected_predecessor_v12") ==
                _expected_published_then_rejected_v12_proof() and
            preseal.get(
                "published_then_officially_rejected_predecessor_v11") ==
                _expected_published_then_rejected_v11_proof() and
            preseal.get(
                "published_then_officially_rejected_predecessor_v12") ==
                _expected_published_then_rejected_v12_proof() and
            consumer_proof.get(
                "published_then_officially_rejected_predecessor_v11") ==
                _expected_published_then_rejected_v11_proof() and
            consumer_proof.get(
                "published_then_officially_rejected_predecessor_v12") ==
                _expected_published_then_rejected_v12_proof() and
            seal.get(
                "published_then_officially_rejected_predecessor_v11") ==
                _expected_published_then_rejected_v11_proof() and
            seal.get(
                "published_then_officially_rejected_predecessor_v12") ==
                _expected_published_then_rejected_v12_proof() and
            postseal.get(
                "published_then_officially_rejected_predecessor_v11") ==
                _expected_published_then_rejected_v11_proof() and
            postseal.get(
                "published_then_officially_rejected_predecessor_v12") ==
                _expected_published_then_rejected_v12_proof(),
        "preseal_contract_and_schema_hashes_equal_contract":
            preseal.get("contract_file_sha256") == CONTRACT_FILE_PIN and
            preseal.get("contract_object_sha256") == CONTRACT_OBJECT_PIN and
            preseal.get("closed_schema_file_sha256") == CLOSED_SCHEMA_FILE_PIN and
            preseal.get("cold_launcher_file_sha256") ==
                freeze_proof.get("cold_launcher_identity", {}).get("file_sha256") and
            preseal.get("cold_manifest_file_sha256") ==
                freeze_proof.get("cold_launch_manifest_identity", {}).get("file_sha256") and
            preseal.get("cold_outer_file_sha256") ==
                freeze_proof.get("cold_launch_outer_identity", {}).get("file_sha256") and
            preseal.get("cold_outer_object_sha256") ==
                freeze_proof.get("cold_launch_outer_object_sha256"),
        "consumer_source_hash_equals_contract":
            freeze_proof.get("transition_pins_current_consumer_SELF") is True and
            freeze_proof.get(
                "static_audit_pins_current_consumer_SELF_transition_contract_schema_rejection_and_producer") is True and
            consumer_proof.get("consumer_file_sha256") ==
                consumer_proof.get("consumer_SELF_identity", {}).get("file_sha256") ==
                seal.get("consumer_file_sha256"),
        "live_official_writer_coordination_lock_equal_preseal_and_consumer":
            preseal.get("official_writer_coordination_lock") ==
                consumer_proof.get("official_writer_coordination_lock_required"),
        "persisted_seal_coordination_lock_policy_equals_live_policy_projection":
            seal.get("official_writer_coordination_lock_policy") ==
                official_writer_coordination_lock_policy_object(
                    preseal.get("official_writer_coordination_lock", {})),
        "seal_stable_preseal_root_equals_freshly_recomputed_stable_preseal_root":
            seal.get("preseal_root_sha256") == preseal.get("preseal_root_sha256"),
        "independent_consumer_proof_is_fresh_virtual_and_not_persistently_pinned":
            _closed_object_equal(consumer_proof) and
            consumer_proof.get("preseal_object_sha256") == preseal.get("object_sha256"),
        "seal_contract_and_schema_hashes_equal_live_hashes":
            seal.get("contract_file_sha256") == CONTRACT_FILE_PIN and
            seal.get("contract_object_sha256") == CONTRACT_OBJECT_PIN and
            seal.get("closed_schema_file_sha256") == CLOSED_SCHEMA_FILE_PIN and
            seal.get("v4_rejection_supersession_file_sha256") ==
                V4_REJECTION_SUPERSESSION_FILE_PIN and
            seal.get("v4_rejection_supersession_object_sha256") ==
                V4_REJECTION_SUPERSESSION_OBJECT_PIN and
            seal.get("v16_to_v16r2_transition_file_sha256") ==
                transition_identity.get("file_sha256") and
            seal.get("v16_to_v16r2_transition_object_sha256") ==
                freeze_proof.get("transition_object_sha256") and
            seal.get("static_audit_file_sha256") == audit_identity.get("file_sha256") and
            seal.get("static_audit_object_sha256") ==
                freeze_proof.get("static_audit_object_sha256") and
            seal.get("cold_launcher_file_sha256") ==
                freeze_proof.get("cold_launcher_identity", {}).get("file_sha256") and
            seal.get("cold_manifest_file_sha256") ==
                freeze_proof.get("cold_launch_manifest_identity", {}).get("file_sha256") and
            seal.get("cold_outer_file_sha256") ==
                freeze_proof.get("cold_launch_outer_identity", {}).get("file_sha256") and
            seal.get("cold_outer_object_sha256") ==
                freeze_proof.get("cold_launch_outer_object_sha256"),
        "preseal_root_recomputed_from_checkpoint_completion_order_replay_and_rejection":
            _closed_object_equal(preseal) and
            _nonzero_sha256(preseal.get("preseal_root_sha256")) and
            preseal.get("preseal_root_domain") == "CM2_C79G_V16R2_PRESEAL_ROOT_V2",
        "authority_root_recomputed_from_preseal_root_and_seal_object":
            authority_root_sha256 == sha(
                b"CM2_C79G_V16R2_AUTHORITY_ROOT_V1" +
                str(preseal.get("preseal_root_sha256")).encode("ascii") +
                str(seal.get("object_sha256")).encode("ascii")),
        "postseal_replay_identities_equal_preseal_identity_set":
            postseal.get("terminal_replay_24") == preseal.get("terminal_replay_24") and
            postseal.get("full10_identity") == preseal.get("full10_identity"),
        "no_later_rejection_scan_is_fresh_for_this_root_instance":
            no_later.get(
                "terminal_acceptance_scan_started_after_authority_seal_open") is True and
            no_later.get("terminal_scan_started_after_all_postseal_replays") is True and
            no_later.get("later_rejection_found") is False and
            no_later.get("cached_scan_reuse_allowed") is False,
        "standalone_outer_credit_is_zero":
            preseal.get("standalone_outer", {}).get("standalone_credit") == ZERO and
            preseal.get("preseal_credit") == ZERO,
        "standalone_seal_credit_is_zero":
            seal.get("standalone_seal_credit") == ZERO and
            seal.get("authority_decision") == "NO_GO_STANDALONE",
    }
    values["all_root_conjuncts_true"] = all(values.values())
    return values


def authority_root(
        preseal: Mapping[str, Any], consumer_proof: Mapping[str, Any],
        seal: Mapping[str, Any], surface_guard: HeldInputSet,
        c42_guard: HeldInputSet, seal_guard: HeldPinnedInput,
        rejection: Mapping[str, Any], receipt_guard: HeldPinnedInput,
        freeze_proof: Mapping[str, Any],
        terminal_stage_absence: Mapping[str, bool],
        postseal_live_replay: bool, no_later_rejection: bool,
        durability_recovery_completed: bool) -> dict[str, Any]:
    """Virtual root result.  It is never persisted as a pointer or outer."""
    need(postseal_live_replay is True and no_later_rejection is True and
         durability_recovery_completed is True and
         seal.get("authority_decision") == "NO_GO_STANDALONE" and
         seal.get("standalone_seal_credit") == ZERO and
         seal.get("preseal_root_sha256") == preseal.get("preseal_root_sha256") and
         seal.get("consumer_file_sha256") == consumer_proof.get("consumer_file_sha256") and
         seal.get("contract_file_sha256") == CONTRACT_FILE_PIN and
         seal.get("contract_object_sha256") == CONTRACT_OBJECT_PIN and
         seal.get("closed_schema_file_sha256") == CLOSED_SCHEMA_FILE_PIN and
         seal.get("v4_rejection_supersession_file_sha256") ==
             V4_REJECTION_SUPERSESSION_FILE_PIN and
         seal.get("v4_rejection_supersession_object_sha256") ==
             V4_REJECTION_SUPERSESSION_OBJECT_PIN and
         preseal.get("v4_rejection_supersession_file_sha256") ==
             V4_REJECTION_SUPERSESSION_FILE_PIN and
         preseal.get("v4_rejection_supersession_object_sha256") ==
             V4_REJECTION_SUPERSESSION_OBJECT_PIN and
         seal.get("v16_to_v16r2_transition_file_sha256") ==
             freeze_proof.get("v16_to_v16r2_transition_identity", {}).get("file_sha256") and
         seal.get("v16_to_v16r2_transition_object_sha256") ==
             freeze_proof.get("transition_object_sha256") and
         seal.get("static_audit_file_sha256") ==
             freeze_proof.get("static_audit_identity", {}).get("file_sha256") and
         seal.get("static_audit_object_sha256") ==
             freeze_proof.get("static_audit_object_sha256") and
         seal.get("cold_launcher_file_sha256") ==
             freeze_proof.get("cold_launcher_identity", {}).get("file_sha256") and
         seal.get("cold_manifest_file_sha256") ==
             freeze_proof.get("cold_launch_manifest_identity", {}).get("file_sha256") and
         seal.get("cold_outer_file_sha256") ==
             freeze_proof.get("cold_launch_outer_identity", {}).get("file_sha256") and
         seal.get("cold_outer_object_sha256") ==
             freeze_proof.get("cold_launch_outer_object_sha256") and
         preseal.get("official_writer_coordination_lock") ==
             consumer_proof.get("official_writer_coordination_lock_required") and
         seal.get("official_writer_coordination_lock_policy") ==
             official_writer_coordination_lock_policy_object(
                 preseal.get("official_writer_coordination_lock", {})) and
         _static_freeze_is_valid(freeze_proof) and
         set(terminal_stage_absence) == {
             "candidate_A", "candidate_B", "verification_A",
             "verification_B", "completion"} and
         all(terminal_stage_absence.values()) and
         preseal.get("contract_file_sha256") == CONTRACT_FILE_PIN and
         preseal.get("contract_object_sha256") == CONTRACT_OBJECT_PIN and
         preseal.get("closed_schema_file_sha256") == CLOSED_SCHEMA_FILE_PIN and
         preseal.get("v4_rejection_supersession_file_sha256") ==
             V4_REJECTION_SUPERSESSION_FILE_PIN and
         preseal.get("v4_rejection_supersession_object_sha256") ==
             V4_REJECTION_SUPERSESSION_OBJECT_PIN and
         preseal.get("exact_paths") == exact_paths_object() and
         preseal.get("preseal_credit") == ZERO and
         preseal.get("standalone_outer", {}).get("standalone_credit") == ZERO and
         consumer_proof.get("preseal_object_sha256") == preseal.get("object_sha256") and
         consumer_proof.get("consumer_file_sha256") ==
             consumer_proof.get("consumer_SELF_identity", {}).get("file_sha256") and
         consumer_proof.get("consumer_SELF_identity", {}).get("path") ==
             str(SELF.relative_to(ROOT)) and
         consumer_proof.get(
             "current_v16r2_producer_source_content_opened_read_decoded_parsed_compiled_imported_or_executed") is False and
         consumer_proof.get(
             "v14_inherited_authority_exact12_held_and_terminally_replayed") is True and
         consumer_proof.get(
             "v10_colon_prefix_witness_independently_rederived_from_inherited_exact10_held_fds") is True and
         _INCIDENT_AUTHORITY_WITNESS == V10_COLON_PREFIX_WITNESS and
         _INCIDENT_AUTHORITY_V12_SHAPE == V12_V5_REJECTION_SHAPE_INCIDENT and
         sha(receipt_guard.raw) == V3_OFFICIAL_REJECTION_FILE_PIN and
         rejection.get("object_sha256") == V3_OFFICIAL_REJECTION_OBJECT_PIN and
         receipt_guard.path == V3_OFFICIAL_REJECTION,
         "all zero-credit inner composite conjuncts")
    postseal = postseal_live_replay_object(
        surface_guard, c42_guard, seal_guard, freeze_proof,
        durability_recovery_completed)
    no_later = no_later_rejection_object()
    computed_authority_root = sha(
        b"CM2_C79G_V16R2_AUTHORITY_ROOT_V1" +
        preseal["preseal_root_sha256"].encode("ascii") +
        seal["object_sha256"].encode("ascii"))
    bindings = binding_equalities_object(
        preseal, consumer_proof, seal, rejection, receipt_guard,
        freeze_proof, postseal, no_later, terminal_stage_absence,
        computed_authority_root)
    need(all(type(value) is bool and value for value in bindings.values()),
         "every reported composite binding equality has an executed validator")
    body: dict[str, Any] = {
        "schema": INNER_ROOT_SCHEMA,
        "status": "PASS_LIVE_INNER_COMPOSITE__ZERO_CREDIT__COLD_LAUNCHER_REQUIRED",
        "authority_decision": "NO_GO_INNER_REQUIRES_COLD_LAUNCHER",
        "effective_checkpoint_object_sha256": UPSTREAM_CHECKPOINT_OBJECT_PIN,
        "exact_paths": exact_paths_object(),
        "v3_official_later_rejection":
            v3_official_later_rejection_proof(rejection, receipt_guard),
        "v4_rejection_supersession":
            v4_rejection_supersession_proof(freeze_proof),
        "published_then_officially_rejected_predecessor_v5": copy.deepcopy(
            freeze_proof[
                "published_then_officially_rejected_predecessor_v5"]),
        "published_then_officially_rejected_predecessor_v6": copy.deepcopy(
            freeze_proof[
                "published_then_officially_rejected_predecessor_v6"]),
        "published_then_officially_rejected_predecessor_v7": copy.deepcopy(
            freeze_proof[
                "published_then_officially_rejected_predecessor_v7"]),
        "published_then_officially_rejected_predecessor_v8": copy.deepcopy(
            freeze_proof[
                "published_then_officially_rejected_predecessor_v8"]),
        "published_then_officially_rejected_predecessor_v9": copy.deepcopy(
            freeze_proof[
                "published_then_officially_rejected_predecessor_v9"]),
        "published_then_officially_rejected_predecessor_v10": copy.deepcopy(
            freeze_proof[
                "published_then_officially_rejected_predecessor_v10"]),
        "published_then_officially_rejected_predecessor_v11": copy.deepcopy(
            _expected_published_then_rejected_v11_proof()),
        "published_then_officially_rejected_predecessor_v12": copy.deepcopy(
            _expected_published_then_rejected_v12_proof()),
        "v7_publication_lock_continuity_incident": copy.deepcopy(
            freeze_proof["v7_publication_lock_continuity_incident"]),
        "preseal_committed_surface": dict(preseal),
        "independent_consumer_proof": dict(consumer_proof),
        "authority_seal": dict(seal),
        "postseal_live_replay": postseal,
        "no_later_rejection": no_later,
        "binding_equalities": bindings,
        "static_freeze_proof": dict(freeze_proof),
        "root_constructed_from_fresh_live_open_fds": True,
        "root_is_not_a_persisted_outer_or_seal": True,
        "positive_root_credit_literal_absent_from_all_persisted_and_inner_surfaces": True,
        "cold_launcher_required": True,
        "cold_live_protocol": {
            "protocol": LIVE_PROTOCOL,
            "request_schema": LIVE_REQUEST_SCHEMA,
            "ack_schema": LIVE_ACK_SCHEMA,
            "release_schema": LIVE_RELEASE_SCHEMA,
            "deterministic_transaction_binding_domain":
                TRANSACTION_BINDING_DOMAIN,
            "transaction_binding_is_replay_identical_not_fresh_or_random": True,
            "prewrapper_body_domain": PREWRAPPER_BODY_DOMAIN,
            "ack_binding_domain": LIVE_ACK_BINDING_DOMAIN,
            "launcher_owned_inherited_coordination_lock_required": True,
            "dynamic_guard_normal_close_requires_exact_bound_RELEASE": True,
        },
        "direct_combined_source_invocation_authoritative": False,
        "preseal_root_sha256": preseal["preseal_root_sha256"],
        "authority_root_domain": "CM2_C79G_V16R2_AUTHORITY_ROOT_V1",
    }
    body["authority_root_sha256"] = computed_authority_root
    body.update({
        "formal_global_closure_credit": 0,
        "D02_unlock": False,
        "D02_gate_credit": 0,
        "D02_task_credit": 0,
        "D02_formal_pending_task_count": PENDING_D02,
        "D02_started": False,
    })
    return close_object(body)
def _verify_completion_raw(
        guard: HeldInputSet, expected_raw: Mapping[str, bytes],
        completion_path: Path) -> None:
    by_path = {item.path: item for item in guard.files}
    for name in MEMBERS:
        need(by_path[CANDIDATE_A / name].raw == by_path[CANDIDATE_B / name].raw,
             "committed surface dual candidate bytes:" + name)
    need(by_path[VERIFICATION_A / VERIFICATION_FILE].raw ==
         by_path[VERIFICATION_B / VERIFICATION_FILE].raw ==
         expected_raw[COMPLETION_VERIFICATION],
         "committed surface dual canonical verification bytes")
    for name in COMPLETION_MEMBERS:
        need(by_path[completion_path / name].raw == expected_raw[name],
             "committed exact4 canonical member:" + name)
    identities = [item.identity for item in guard.files]
    need(len(identities) == 24 and len(set(identities)) == 24,
         "candidate18 + verification2 + completion4 exact24 identities globally unique")
    _all_mounts_one(guard, "exact24 surface")


def assemble(
        self_guard: HeldSelf, c78_guard: HeldInputSet,
        fixed_guard: HeldInputSet,
        runtime_parent: HeldCommitParent,
        producer_guard: HeldOpaqueMetadata) -> None:
    need(COMMITTED_COMPLETION.parent == RUNTIME and
         runtime_parent.path == RUNTIME and
         runtime_parent.inherited_launcher_coordination_fd is True,
         "fixed committed-completion target under inherited locked runtime parent")
    c42_guard = hold_c42_full10_union_candidate9()
    policy_guard = _static_policy_guards()
    v3_guard, v3_source_metadata = hold_v3_predecessor_exact10()
    v4_guard, v4_source_metadata = hold_v4_rejected_static_draft7()
    v5_guard, v5_source_metadata = hold_v5_published_exact10()
    v6_guard, v6_source_metadata = hold_v6_published_exact10()
    v7_guard, v7_source_metadata = hold_v7_published_exact10()
    v8_guard, v8_source_metadata = hold_v8_published_exact10()
    v9_guard, v9_source_metadata = hold_v9_published_exact10()
    v10_guard, v10_source_metadata = hold_v10_published_exact10()
    v11_guard, v11_source_metadata = hold_v11_published_exact10()
    commit_parent = runtime_parent
    need(commit_parent.path == RUNTIME and
         commit_parent.inherited_launcher_coordination_fd is True,
         "assembly uses launcher-owned coordination parent fd")
    public_guard = _candidate_verification_guards(False)
    stage_guard: HeldInputSet | None = None
    created_files: list[HeldPinnedInput] = []
    stage_writer: HeldCommitParent | None = None
    try:
        freeze_proof = static_freeze_proof(
            policy_guard, self_guard, producer_guard,
            v5_guard, v5_source_metadata, v6_guard, v6_source_metadata,
            v7_guard, v7_source_metadata, v8_guard, v8_source_metadata,
            v9_guard, v9_source_metadata, v10_guard, v10_source_metadata,
            v11_guard, v11_source_metadata)
        need(_static_freeze_is_valid(freeze_proof),
             "assembly requires final post-source static freeze")
        context = reconstruct_publication_context(
            CANDIDATE_A, CANDIDATE_B, self_guard, producer_guard, public_guard,
            c78_guard, c42_guard, fixed_guard, policy_guard,
            v3_guard, v3_source_metadata, v4_guard, v4_source_metadata,
            v5_guard, v5_source_metadata, v6_guard, v6_source_metadata,
            v7_guard, v7_source_metadata, v8_guard, v8_source_metadata,
            v9_guard, v9_source_metadata, v10_guard, v10_source_metadata,
            v11_guard, v11_source_metadata)
        va_raw, va, va_identity = read_verification_surface(
            VERIFICATION_A, context["verification"], public_guard)
        vb_raw, vb, vb_identity = read_verification_surface(
            VERIFICATION_B, context["verification"], public_guard)
        need(va_raw == vb_raw == context["verification_raw"] and
             va == vb == context["verification"] and va_identity != vb_identity,
             "dual verification exact canonical bytes/object/inode separation")
        need(held_child_lstat_or_absent(
                 commit_parent, COMMITTED_COMPLETION.name,
                 "completion fixed destination pre-stage probe") is None,
             "completion target already exists; reject without creating stage")
        stage, stage_writer = _new_hidden_stage(
            commit_parent, COMPLETION_STAGE.name, True)
        need(stage_writer is not None and stage == COMPLETION_STAGE,
             "fixed checkpoint-keyed completion stage")
        install_proof = completion_install_proof(stage)
        raw, completion_objects = construct_completion_surface(
            context, va_raw, va, vb_raw, vb, install_proof)
        for name in COMPLETION_MEMBERS:
            created_files.append(stage_writer.exclusive_file(name, raw[name]))
        need(set(os.listdir(stage_writer.fd)) == set(COMPLETION_MEMBERS),
             "completion hidden stage exact4 through continuously held dirfd")
        os.fchmod(stage_writer.fd, 0o555)
        os.fsync(stage_writer.fd)
        stage_writer.terminal_identity()
        stage_directory_guard = HeldDirectory(
            stage, set(COMPLETION_MEMBERS), 0o555, 2,
            "completion hidden stage exact4")
        need(stage_directory_guard.identity ==
             (stage_writer.before.st_dev, stage_writer.before.st_ino) and
             stage_directory_guard.mount_id == stage_writer.mount_id,
             "completion directory has been continuously held since mkdirat")
        stage_guard = HeldInputSet(created_files, [stage_directory_guard])
        created_files = []
        combined_files = public_guard.files + stage_guard.files
        combined_dirs = public_guard.directories + stage_guard.directories
        exact24_guard = HeldInputSet(combined_files, combined_dirs)
        _verify_completion_raw(exact24_guard, raw, stage)
        validate_global_chronology(exact24_guard, stage)
        need(completion_objects["final_outer"].get("formal_global_closure_credit") == 0 and
             completion_objects["final_outer"].get("D02_unlock") is False,
             "assembled completion remains zero-credit nonauthority")
        c42_guard.terminal_replay()
        c78_guard.terminal_replay()
        fixed_guard.terminal_replay()
        terminal_replay_v3_predecessor_exact10(
            v3_guard, v3_source_metadata)
        terminal_replay_v4_rejected_static_draft7(
            v4_guard, v4_source_metadata)
        terminal_replay_v5_published_exact10(
            v5_guard, v5_source_metadata)
        terminal_replay_v6_published_exact10(
            v6_guard, v6_source_metadata)
        terminal_replay_v7_published_exact10(
            v7_guard, v7_source_metadata)
        terminal_replay_v8_published_exact10(
            v8_guard, v8_source_metadata)
        terminal_replay_v9_published_exact10(
            v9_guard, v9_source_metadata)
        terminal_replay_v10_published_exact10(
            v10_guard, v10_source_metadata)
        terminal_replay_v11_published_exact10(
            v11_guard, v11_source_metadata)
        terminal_replay_v12_published_exact10()
        producer_guard.terminal_replay()
        policy_guard.terminal_replay()
        exact24_guard.terminal_replay()
        self_guard.terminal_replay()
        stage_directory = stage_guard.directories[0]
        rename_noreplace(
            commit_parent, stage.name, COMMITTED_COMPLETION.name,
            stage_directory.identity, stage_directory.mount_id)
    finally:
        if stage_guard is not None:
            stage_guard.close()
        else:
            for item in reversed(created_files):
                item.close()
        if stage_writer is not None:
            stage_writer.close()
        public_guard.close()
        policy_guard.close()
        v3_guard.close()
        for item in reversed(v3_source_metadata):
            item.close()
        v4_guard.close()
        for item in reversed(v4_source_metadata):
            item.close()
        v6_guard.close()
        for item in reversed(v6_source_metadata):
            item.close()
        v7_guard.close()
        for item in reversed(v7_source_metadata):
            item.close()
        v8_guard.close()
        for item in reversed(v8_source_metadata):
            item.close()
        v9_guard.close()
        for item in reversed(v9_source_metadata):
            item.close()
        v10_guard.close()
        for item in reversed(v10_source_metadata):
            item.close()
        v11_guard.close()
        for item in reversed(v11_source_metadata):
            item.close()
        v5_guard.close()
        for item in reversed(v5_source_metadata):
            item.close()
        c42_guard.close()


def construct_later_rejection(
        self_guard: HeldSelf, freeze_proof: Mapping[str, Any],
        runtime_parent: HeldCommitParent) -> dict[str, Any]:
    """Build the one permanent, zero-credit checkpoint rejection receipt."""
    live_lock = official_writer_coordination_lock_object(runtime_parent)
    return close_object({
        "schema": LATER_REJECTION_SCHEMA,
        "status": "PERMANENT_FAIL_CLOSED_REJECTION__ZERO_CREDIT",
        "effective_checkpoint_object_sha256": UPSTREAM_CHECKPOINT_OBJECT_PIN,
        "namespace_exact_path": str(REJECTION_NAMESPACE.relative_to(ROOT)),
        "target_exact_path": str(LATER_REJECTION.relative_to(ROOT)),
        "rejection_reason": LATER_REJECTION_REASON,
        "consumer_file_sha256": self_guard.file_sha256,
        "producer_file_sha256": PRODUCER_SOURCE_PIN,
        "contract_file_sha256": CONTRACT_FILE_PIN,
        "contract_object_sha256": CONTRACT_OBJECT_PIN,
        "closed_schema_file_sha256": CLOSED_SCHEMA_FILE_PIN,
        "v4_rejection_supersession_file_sha256":
            V4_REJECTION_SUPERSESSION_FILE_PIN,
        "v4_rejection_supersession_object_sha256":
            V4_REJECTION_SUPERSESSION_OBJECT_PIN,
        "v5_official_rejection_file_sha256":
            V5_OFFICIAL_REJECTION_FILE_PIN,
        "v5_official_rejection_object_sha256":
            V5_OFFICIAL_REJECTION_OBJECT_PIN,
        "v6_official_rejection_file_sha256":
            V6_OFFICIAL_REJECTION_FILE_PIN,
        "v6_official_rejection_object_sha256":
            V6_OFFICIAL_REJECTION_OBJECT_PIN,
        "v7_official_rejection_file_sha256":
            V7_OFFICIAL_REJECTION_FILE_PIN,
        "v7_official_rejection_object_sha256":
            V7_OFFICIAL_REJECTION_OBJECT_PIN,
        "v8_official_rejection_file_sha256":
            V8_OFFICIAL_REJECTION_FILE_PIN,
        "v8_official_rejection_object_sha256":
            V8_OFFICIAL_REJECTION_OBJECT_PIN,
        "v9_official_rejection_file_sha256":
            V9_OFFICIAL_REJECTION_FILE_PIN,
        "v9_official_rejection_object_sha256":
            V9_OFFICIAL_REJECTION_OBJECT_PIN,
        "v10_official_rejection_file_sha256":
            V10_OFFICIAL_REJECTION_FILE_PIN,
        "v10_official_rejection_object_sha256":
            V10_OFFICIAL_REJECTION_OBJECT_PIN,
        "v11_official_rejection_file_sha256":
            V11_OFFICIAL_REJECTION_FILE_PIN,
        "v11_official_rejection_object_sha256":
            V11_OFFICIAL_REJECTION_OBJECT_PIN,
        "v12_official_rejection_file_sha256":
            V12_OFFICIAL_REJECTION_FILE_PIN,
        "v12_official_rejection_object_sha256":
            V12_OFFICIAL_REJECTION_OBJECT_PIN,
        "v7_publication_lock_continuity_incident_object_sha256":
            V7_PUBLICATION_LOCK_CONTINUITY_INCIDENT["object_sha256"],
        "cold_launcher_file_sha256":
            freeze_proof["cold_launcher_identity"]["file_sha256"],
        "cold_manifest_file_sha256":
            freeze_proof["cold_launch_manifest_identity"]["file_sha256"],
        "cold_outer_file_sha256":
            freeze_proof["cold_launch_outer_identity"]["file_sha256"],
        "cold_outer_object_sha256":
            freeze_proof["cold_launch_outer_object_sha256"],
        "official_writer_coordination_lock_policy":
            official_writer_coordination_lock_policy_object(live_lock),
        "official_writer_coordination_lock_held_for_entire_reject_command": True,
        "target_is_protocol_and_checkpoint_deterministic": True,
        "commit_operation": "O_CREAT_O_EXCL_FIXED_TARGET_NO_FALLBACK",
        "namespace_at_rest_mode": "0555",
        "namespace_lock_held_write_window_mode": "0755",
        "rejection_file_mode": "0444",
        "rejection_file_nlink": 1,
        "file_fsync_required": True,
        "namespace_fsync_required_after_file_and_after_reseal": True,
        "runtime_parent_fsync_required_after_namespace_creation": True,
        "idempotent_existing_recovery_re_fsyncs_rejection_file_namespace_and_runtime_parent": True,
        "overwrite_delete_or_reuse_allowed": False,
        "partial_malformed_or_extra_namespace_entry_revokes_authority": True,
        "standalone_authority": False,
        "formal_global_closure_credit": 0,
        "D02_unlock": False,
        "D02_gate_credit": 0,
        "D02_task_credit": 0,
        "D02_formal_pending_task_count": PENDING_D02,
        "D02_started": False,
    })


def _rejection_namespace_parent(
        allow_create: bool,
        runtime_parent: HeldCommitParent) -> HeldCommitParent:
    need(runtime_parent.path == RUNTIME and
         runtime_parent.inherited_launcher_coordination_fd is True,
         "rejection namespace uses launcher-owned coordination parent fd")
    state = held_child_lstat_or_absent(
        runtime_parent, REJECTION_NAMESPACE.name, "rejection namespace")
    expected_identity: tuple[int, int] | None = (
        None if state is None else (state.st_dev, state.st_ino))
    namespace_parent: HeldCommitParent
    if state is None:
        need(allow_create is True,
             "committed seal requires preexisting rejection namespace; never recreate")
        namespace_parent = runtime_parent.mkdir_exclusive(
            REJECTION_NAMESPACE.name, 0o555)
        namespace_parent.terminal_identity()
        expected_identity = (
            namespace_parent.before.st_dev, namespace_parent.before.st_ino)
        runtime_parent.terminal_identity()
    else:
        namespace_parent = HeldCommitParent(
            REJECTION_NAMESPACE, "checkpoint-keyed rejection namespace parent")
    current = os.fstat(namespace_parent.fd)
    current_path = REJECTION_NAMESPACE.lstat()
    need(expected_identity is not None and
         (current.st_dev, current.st_ino) == expected_identity ==
             (current_path.st_dev, current_path.st_ino) and
         stat.S_ISDIR(current.st_mode) and
         stat.S_IMODE(current.st_mode) == 0o555 and current.st_nlink == 2 and
         namespace_parent.mount_id == runtime_parent.mount_id,
         "rejection namespace exact sealed-at-rest 0555 identity/mount")
    return namespace_parent


def _ensure_rejection_namespace(
        allow_create: bool,
        runtime_parent: HeldCommitParent) -> HeldDirectory:
    namespace_parent = _rejection_namespace_parent(allow_create, runtime_parent)
    expected_identity = (
        namespace_parent.before.st_dev, namespace_parent.before.st_ino)
    adopted_descriptor = os.dup(namespace_parent.fd)
    try:
        final_guard = HeldDirectory.from_existing_fd(
            REJECTION_NAMESPACE, set(), 0o555, 2,
            "checkpoint-keyed no-later-rejection namespace",
            adopted_descriptor)
    except BaseException:
        os.close(adopted_descriptor)
        raise
    finally:
        namespace_parent.close()
    need(final_guard.identity == expected_identity,
         "rejection namespace final guard equals held-parent observed identity")
    return final_guard


def reject_checkpoint(
        self_guard: HeldSelf, runtime_parent: HeldCommitParent,
        producer_guard: HeldOpaqueMetadata) -> None:
    """Non-normative fail-closed fallback for permanent checkpoint revocation.

    The normative reject route is launcher-native after launcher held-fd
    self-proof and the official lock, before this consumer or its bundle is
    loaded.  This compatibility fallback never authorizes runtime and must not
    be used as evidence that the launcher-native route exists or succeeded.
    """
    policy_guard = _static_policy_guards()
    v5_guard, v5_source_metadata = hold_v5_published_exact10()
    v6_guard, v6_source_metadata = hold_v6_published_exact10()
    v7_guard, v7_source_metadata = hold_v7_published_exact10()
    v8_guard, v8_source_metadata = hold_v8_published_exact10()
    v9_guard, v9_source_metadata = hold_v9_published_exact10()
    v10_guard, v10_source_metadata = hold_v10_published_exact10()
    v11_guard, v11_source_metadata = hold_v11_published_exact10()
    namespace_parent: HeldCommitParent | None = None
    rejection_guard: HeldPinnedInput | None = None
    final_directory: HeldDirectory | None = None
    try:
        freeze_proof = static_freeze_proof(
            policy_guard, self_guard, producer_guard,
            v5_guard, v5_source_metadata, v6_guard, v6_source_metadata,
            v7_guard, v7_source_metadata, v8_guard, v8_source_metadata,
            v9_guard, v9_source_metadata, v10_guard, v10_source_metadata,
            v11_guard, v11_source_metadata)
        need(_static_freeze_is_valid(freeze_proof),
             "reject requires the frozen cold bundle and current SELF")
        expected = construct_later_rejection(
            self_guard, freeze_proof, runtime_parent)
        expected_raw = canonical(expected) + b"\n"
        workspace_root_terminal_replay()
        namespace_parent = _rejection_namespace_parent(True, runtime_parent)
        universe = set(os.listdir(namespace_parent.fd))
        target_state = held_child_lstat_or_absent(
            namespace_parent, LATER_REJECTION.name,
            "deterministic permanent rejection target")
        if target_state is not None:
            need(universe == {LATER_REJECTION.name},
                 "idempotent rejection requires exact singleton namespace")
            rejection_guard = HeldPinnedInput(
                LATER_REJECTION, "existing permanent C79g v16r2 rejection", 0o444)
            value = strict_json(rejection_guard.raw, "permanent C79g v16r2 rejection")
            verify_object(value, "permanent C79g v16r2 rejection")
            need(value == expected and rejection_guard.raw == expected_raw,
                 "existing deterministic rejection is byte-identical")
        else:
            need(not universe, "rejection namespace must be exact empty before first append")
            os.fchmod(namespace_parent.fd, 0o755)
            os.fsync(namespace_parent.fd)
            writable = os.fstat(namespace_parent.fd)
            need(stat.S_IMODE(writable.st_mode) == 0o755 and
                 writable.st_nlink == 2,
                 "lock-held rejection namespace write window is exact 0755")
            try:
                rejection_guard = namespace_parent.exclusive_file(
                    LATER_REJECTION.name, expected_raw, 0o444)
                rejection_guard.terminal_replay()
            finally:
                os.fchmod(namespace_parent.fd, 0o555)
                os.fsync(namespace_parent.fd)
        need(rejection_guard is not None,
             "permanent rejection file is held before durability recovery")
        # Exact bytes are not enough for an idempotent EEXIST recovery: the
        # preceding invocation may have crashed after visibility but before a
        # parent fsync.  Re-fsync every durability layer on both branches.
        os.fsync(rejection_guard.fd)
        os.fsync(namespace_parent.fd)
        os.fsync(runtime_parent.fd)
        rejection_guard.terminal_replay()
        namespace_parent.terminal_identity()
        runtime_parent.terminal_identity()
        final_directory = HeldDirectory(
            REJECTION_NAMESPACE, {LATER_REJECTION.name}, 0o555, 2,
            "sealed permanent-rejection namespace")
        need(rejection_guard.identity not in {final_directory.identity} and
             rejection_guard.mount_id == final_directory.mount_id ==
                 runtime_parent.mount_id,
             "permanent rejection file/directory exact isolated identity/mount")
        policy_guard.terminal_replay()
        terminal_replay_v5_published_exact10(
            v5_guard, v5_source_metadata)
        terminal_replay_v6_published_exact10(
            v6_guard, v6_source_metadata)
        terminal_replay_v7_published_exact10(
            v7_guard, v7_source_metadata)
        terminal_replay_v8_published_exact10(
            v8_guard, v8_source_metadata)
        terminal_replay_v9_published_exact10(
            v9_guard, v9_source_metadata)
        terminal_replay_v10_published_exact10(
            v10_guard, v10_source_metadata)
        terminal_replay_v11_published_exact10(
            v11_guard, v11_source_metadata)
        terminal_replay_v12_published_exact10()
        producer_guard.terminal_replay()
        self_guard.terminal_replay()
        rejection_guard.terminal_replay()
        final_directory.terminal_replay()
        namespace_parent.terminal_identity()
        runtime_parent.terminal_identity()
        workspace_root_terminal_replay()
    finally:
        if final_directory is not None:
            final_directory.close()
        if rejection_guard is not None:
            rejection_guard.close()
        if namespace_parent is not None:
            namespace_parent.close()
        v6_guard.close()
        for item in reversed(v6_source_metadata):
            item.close()
        v7_guard.close()
        for item in reversed(v7_source_metadata):
            item.close()
        v8_guard.close()
        for item in reversed(v8_source_metadata):
            item.close()
        v9_guard.close()
        for item in reversed(v9_source_metadata):
            item.close()
        v10_guard.close()
        for item in reversed(v10_source_metadata):
            item.close()
        v11_guard.close()
        for item in reversed(v11_source_metadata):
            item.close()
        v5_guard.close()
        for item in reversed(v5_source_metadata):
            item.close()
        policy_guard.close()


def _committed_context(
        self_guard: HeldSelf, public_guard: HeldInputSet,
        runtime_parent: HeldCommitParent, c78_guard: HeldInputSet,
        c42_guard: HeldInputSet, fixed_guard: HeldInputSet,
        policy_guard: HeldInputSet, v3_guard: HeldInputSet,
        v3_source_metadata: list[HeldOpaqueMetadata],
        v4_guard: HeldInputSet,
        v4_source_metadata: list[HeldOpaqueMetadata],
        v5_guard: HeldInputSet,
        v5_source_metadata: list[HeldOpaqueMetadata],
        v6_guard: HeldInputSet,
        v6_source_metadata: list[HeldOpaqueMetadata],
        v7_guard: HeldInputSet,
        v7_source_metadata: list[HeldOpaqueMetadata],
        v8_guard: HeldInputSet,
        v8_source_metadata: list[HeldOpaqueMetadata],
        v9_guard: HeldInputSet,
        v9_source_metadata: list[HeldOpaqueMetadata],
        v10_guard: HeldInputSet,
        v10_source_metadata: list[HeldOpaqueMetadata],
        v11_guard: HeldInputSet,
        v11_source_metadata: list[HeldOpaqueMetadata],
        producer_guard: HeldOpaqueMetadata,
        ) -> tuple[dict[str, Any], dict[str, bytes], dict[str, Any],
                   dict[str, Any], dict[str, bool]]:
    context = reconstruct_publication_context(
        CANDIDATE_A, CANDIDATE_B, self_guard, producer_guard, public_guard,
        c78_guard, c42_guard, fixed_guard, policy_guard,
        v3_guard, v3_source_metadata, v4_guard, v4_source_metadata,
        v5_guard, v5_source_metadata, v6_guard, v6_source_metadata,
        v7_guard, v7_source_metadata, v8_guard, v8_source_metadata,
        v9_guard, v9_source_metadata, v10_guard, v10_source_metadata,
        v11_guard, v11_source_metadata)
    va_raw, va, va_identity = read_verification_surface(
        VERIFICATION_A, context["verification"], public_guard)
    vb_raw, vb, vb_identity = read_verification_surface(
        VERIFICATION_B, context["verification"], public_guard)
    need(va_raw == vb_raw == context["verification_raw"] and va == vb and
         va_identity != vb_identity,
         "authority dual canonical verification reconstruction")
    receipt_item = next(item for item in public_guard.files
                        if item.path == COMMITTED_COMPLETION / COMPLETION_RECEIPT)
    committed_receipt = strict_json(receipt_item.raw, "committed completion receipt")
    verify_object(committed_receipt, "committed completion receipt")
    install_proof = committed_receipt.get("completion_install")
    need(isinstance(install_proof, dict) and
         isinstance(install_proof.get("staging_path"), str),
         "committed completion recorded install proof")
    recorded_stage = rooted(install_proof["staging_path"])
    stage_paths = {
        "candidate_A": CANDIDATE_STAGE_A,
        "candidate_B": CANDIDATE_STAGE_B,
        "verification_A": VERIFICATION_STAGE_A,
        "verification_B": VERIFICATION_STAGE_B,
        "completion": COMPLETION_STAGE,
    }
    need(recorded_stage == COMPLETION_STAGE,
         "committed completion records exact deterministic source stage")
    runtime_parent.terminal_identity()
    committed_stage_absence = {
        name: held_child_lstat_or_absent(
            runtime_parent, path.name, "committed source stage:" + name) is None
        for name, path in stage_paths.items()
    }
    need(all(committed_stage_absence.values()),
         "all candidate/verification/completion deterministic sources absent")
    expected_raw, completion_objects = construct_completion_surface(
        context, va_raw, va, vb_raw, vb, install_proof)
    _verify_completion_raw(public_guard, expected_raw, COMMITTED_COMPLETION)
    validate_global_chronology(public_guard, COMMITTED_COMPLETION)
    receipt_guard = held_v3_official_rejection(v3_guard)
    rejection = exact_v3_rejection(
        receipt_guard, v3_guard, v3_source_metadata)
    return context, expected_raw, completion_objects, rejection, committed_stage_absence


def terminal_committed_stage_absence(
        runtime_parent: HeldCommitParent) -> dict[str, bool]:
    runtime_parent.terminal_identity()
    paths = {
        "candidate_A": CANDIDATE_STAGE_A,
        "candidate_B": CANDIDATE_STAGE_B,
        "verification_A": VERIFICATION_STAGE_A,
        "verification_B": VERIFICATION_STAGE_B,
        "completion": COMPLETION_STAGE,
    }
    result = {
        name: held_child_lstat_or_absent(
            runtime_parent, path.name, "terminal committed source stage:" + name) is None
        for name, path in paths.items()
    }
    need(all(result.values()),
         "terminal held-RUNTIME-parent exact5 deterministic source absence")
    return result


def _read_canonical_protocol_object(
        label: str, expected_schema: str, expected_status: str,
        exact_keys: set[str]) -> dict[str, Any]:
    descriptor = sys.stdin.fileno()
    raw = bytearray()
    while True:
        need(len(raw) < 16_384, label + ":line exceeds fixed bound")
        octet = os.read(descriptor, 1)
        need(octet != b"", label + ":unexpected EOF")
        raw.extend(octet)
        if octet == b"\n":
            break
    encoded = bytes(raw)
    value = strict_json(encoded, label)
    need(isinstance(value, dict) and set(value) == exact_keys and
         value.get("schema") == expected_schema and
         value.get("status") == expected_status and
         value.get("protocol") == LIVE_PROTOCOL and
         encoded == canonical(value) + b"\n",
         label + ":exact canonical protocol object")
    verify_object(value, label)
    return value


def _protocol_input_must_not_be_ready(label: str) -> None:
    ready, _, _ = select.select([sys.stdin.fileno()], [], [], 0)
    need(not ready, label + ":premature, pipelined, or EOF input")


def _live_ack_binding_sha256(request: Mapping[str, Any]) -> str:
    return sha(
        LIVE_ACK_BINDING_DOMAIN.encode("ascii") + b"\x00" +
        request["transaction_binding_sha256"].encode("ascii") +
        request["inner_object_sha256"].encode("ascii") +
        request["wrapper_body_domain_sha256"].encode("ascii") +
        request["wrapper_object_sha256"].encode("ascii") +
        request["object_sha256"].encode("ascii"))


def _expected_transaction_binding_sha256(request: Mapping[str, Any]) -> str:
    return sha(
        TRANSACTION_BINDING_DOMAIN.encode("ascii") + b"\x00" +
        request["inner_object_sha256"].encode("ascii") +
        request["wrapper_body_domain_sha256"].encode("ascii") +
        request["wrapper_object_sha256"].encode("ascii") +
        os.environ[COLD_LAUNCHER_SHA_ENV].encode("ascii"))


def cold_authorize_live_protocol(
        inner: Mapping[str, Any], runtime_parent: HeldCommitParent,
        authority_heads_parent: HeldCommitParent,
        public_guard: HeldInputSet, c42_guard: HeldInputSet,
        seal_guard: HeldPinnedInput, policy_guard: HeldInputSet,
        v3_guard: HeldInputSet,
        v3_source_metadata: list[HeldOpaqueMetadata],
        v4_guard: HeldInputSet,
        v4_source_metadata: list[HeldOpaqueMetadata],
        v5_guard: HeldInputSet,
        v5_source_metadata: list[HeldOpaqueMetadata],
        v6_guard: HeldInputSet,
        v6_source_metadata: list[HeldOpaqueMetadata],
        v7_guard: HeldInputSet,
        v7_source_metadata: list[HeldOpaqueMetadata],
        v8_guard: HeldInputSet,
        v8_source_metadata: list[HeldOpaqueMetadata],
        v9_guard: HeldInputSet,
        v9_source_metadata: list[HeldOpaqueMetadata],
        v10_guard: HeldInputSet,
        v10_source_metadata: list[HeldOpaqueMetadata],
        v11_guard: HeldInputSet,
        v11_source_metadata: list[HeldOpaqueMetadata],
        c78_guard: HeldInputSet, fixed_guard: HeldInputSet,
        producer_guard: HeldOpaqueMetadata, self_guard: HeldSelf,
        rejection_guard: HeldDirectory) -> None:
    """Two-phase cold IPC while every dynamic fd and the launcher lock stay live."""
    need(runtime_parent.inherited_launcher_coordination_fd is True and
         runtime_parent.path == RUNTIME and
         inner.get("schema") == INNER_ROOT_SCHEMA and
         inner.get("formal_global_closure_credit") == 0 and
         inner.get("D02_unlock") is False and
         inner.get("cold_launcher_required") is True and
         _closed_object_equal(inner),
         "cold live protocol exact zero-credit inner and inherited lock")
    stdin_info = os.fstat(sys.stdin.fileno())
    stdout_info = os.fstat(sys.stdout.fileno())
    need(stat.S_ISFIFO(stdin_info.st_mode) and stat.S_ISFIFO(stdout_info.st_mode),
         "cold live protocol requires dedicated launcher stdin/stdout pipes")
    _protocol_input_must_not_be_ready("request must follow inner stdout")
    inner_raw = canonical(dict(inner)) + b"\n"
    written = sys.stdout.buffer.write(inner_raw)
    need(written == len(inner_raw), "complete canonical inner stdout write")
    sys.stdout.buffer.flush()

    request_keys = {
        "schema", "status", "protocol", "transaction_binding_domain",
        "transaction_binding_sha256",
        "inner_object_sha256", "wrapper_body_domain",
        "wrapper_body_domain_sha256", "wrapper_object_sha256",
        "wrapper_closed_and_schema_validated_before_request",
        "wrapper_body_excludes_transaction_binding_request_ACK_and_RELEASE_to_avoid_hash_cycle",
        "transaction_binding_is_replay_identical_not_fresh_or_random",
        "static_v16r2_exact10_with_v11_exact10_and_official_rejection_v10_exact10_and_official_rejection_v9_exact10_and_official_rejection_v8_exact10_and_official_rejection_v7_exact10_and_official_rejection_v6_exact10_and_official_rejection_v5_exact10_and_official_rejection_v4_supersession_v3_exact10_and_official_rejection_terminal_replay_completed_by_launcher_before_request",
        "launcher_empty_rejection_namespace_guard_terminally_replayed_before_request",
        "object_sha256",
    }
    request = _read_canonical_protocol_object(
        "cold live commit request", LIVE_REQUEST_SCHEMA,
        "REQUEST_FINAL_DYNAMIC_LIVE_ACK_BEFORE_POSITIVE_WRAPPER_OUTPUT",
        request_keys)
    need(request.get("transaction_binding_domain") ==
             TRANSACTION_BINDING_DOMAIN and
         _nonzero_sha256(request.get("transaction_binding_sha256")) and
         request.get("transaction_binding_sha256") ==
             _expected_transaction_binding_sha256(request) and
         request.get("inner_object_sha256") == inner["object_sha256"] and
         request.get("wrapper_body_domain") == PREWRAPPER_BODY_DOMAIN and
         _nonzero_sha256(request.get("wrapper_body_domain_sha256")) and
         _nonzero_sha256(request.get("wrapper_object_sha256")) and
         request.get("wrapper_closed_and_schema_validated_before_request") is True and
         request.get(
             "wrapper_body_excludes_transaction_binding_request_ACK_and_RELEASE_to_avoid_hash_cycle") is True and
         request.get(
             "transaction_binding_is_replay_identical_not_fresh_or_random") is True and
         request.get(
             "static_v16r2_exact10_with_v11_exact10_and_official_rejection_v10_exact10_and_official_rejection_v9_exact10_and_official_rejection_v8_exact10_and_official_rejection_v7_exact10_and_official_rejection_v6_exact10_and_official_rejection_v5_exact10_and_official_rejection_v4_supersession_v3_exact10_and_official_rejection_terminal_replay_completed_by_launcher_before_request") is True and
         request.get(
             "launcher_empty_rejection_namespace_guard_terminally_replayed_before_request") is True,
         "cold live request deterministic transaction/inner/prewrapper/wrapper/static bindings")
    _protocol_input_must_not_be_ready("RELEASE must wait for live ACK")

    lock_proof = official_writer_coordination_lock_object(runtime_parent)
    ack_binding_sha256 = _live_ack_binding_sha256(request)
    ack = close_object({
        "schema": LIVE_ACK_SCHEMA,
        "status":
            "ACK_FINAL_DYNAMIC_CONJUNCTS_LIVE__ZERO_CREDIT__AWAIT_POSITIVE_WRAPPER_AND_RELEASE",
        "protocol": LIVE_PROTOCOL,
        "transaction_binding_domain": TRANSACTION_BINDING_DOMAIN,
        "transaction_binding_sha256": request["transaction_binding_sha256"],
        "request_object_sha256": request["object_sha256"],
        "inner_object_sha256": request["inner_object_sha256"],
        "wrapper_body_domain": PREWRAPPER_BODY_DOMAIN,
        "wrapper_body_domain_sha256": request["wrapper_body_domain_sha256"],
        "wrapper_object_sha256": request["wrapper_object_sha256"],
        "ack_binding_domain": LIVE_ACK_BINDING_DOMAIN,
        "ack_binding_sha256": ack_binding_sha256,
        "official_writer_coordination_lock": lock_proof,
        "final_dynamic_replay_census": {
            "C78l_C78s_held_file_count": 51,
            "C78l_C78s_held_directory_count": 5,
            "C55_C72_fixed_held_file_count_excluding_shared_head": 16,
            "shared_C72G_C53_head_held_via_C42_full10_count": 1,
            "frozen_v3_readable_held_file_count": 7,
            "frozen_v3_source_metadata_only_held_count": 3,
            "v3_official_rejection_shared_readable_held_file_count": 1,
            "rejected_v4_readable_held_file_count": 4,
            "rejected_v4_source_metadata_only_held_count": 3,
            "frozen_v5_readable_held_file_count": 7,
            "frozen_v5_source_metadata_only_held_count": 3,
            "v5_official_rejection_shared_readable_held_file_count": 1,
            "frozen_v6_readable_held_file_count": 7,
            "frozen_v6_source_metadata_only_held_count": 3,
            "v6_official_rejection_shared_readable_held_file_count": 1,
            "frozen_v7_readable_held_file_count": 7,
            "frozen_v7_source_metadata_only_held_count": 3,
            "v7_official_rejection_shared_readable_held_file_count": 1,
            "frozen_v8_readable_held_file_count": 7,
            "frozen_v8_source_metadata_only_held_count": 3,
            "v8_official_rejection_shared_readable_held_file_count": 1,
            "frozen_v9_readable_held_file_count": 7,
            "frozen_v9_source_metadata_only_held_count": 3,
            "v9_official_rejection_shared_readable_held_file_count": 1,
            "frozen_v10_readable_held_file_count": 7,
            "frozen_v10_source_metadata_only_held_count": 3,
            "v10_official_rejection_shared_readable_held_file_count": 1,
            "frozen_v11_readable_held_file_count": 7,
            "frozen_v11_source_metadata_only_held_count": 3,
            "v11_official_rejection_shared_readable_held_file_count": 1,
            "current_producer_metadata_only_held_count": 1,
            "consumer_installed_source_held_count": 1,
            "consumer_sealed_exec_memfd_held_count": 1,
            "public_candidate_verification_completion_held_file_count": 24,
            "public_candidate_verification_completion_held_directory_count": 5,
            "C42_full10_union_candidate9_held_file_count": 16,
            "C42_candidate_audit_install_held_directory_count": 3,
            "authority_seal_held_file_count": 1,
            "static_policy_held_file_count": 8,
            "v11_official_rejection_in_static_policy_held_file_count": 1,
            "terminal_deterministic_stage_absence_count": 5,
            "fresh_rejection_namespace_scan_count": 1,
        },
        "all_dynamic_conjuncts_live": True,
        "wrapper_closed_and_schema_validated_before_request": True,
        "wrapper_body_excludes_transaction_binding_request_ACK_and_RELEASE_to_avoid_hash_cycle": True,
        "transaction_binding_is_replay_identical_not_fresh_or_random": True,
        "static_v16r2_exact10_with_v11_exact10_and_official_rejection_v10_exact10_and_official_rejection_v9_exact10_and_official_rejection_v8_exact10_and_official_rejection_v7_exact10_and_official_rejection_v6_exact10_and_official_rejection_v5_exact10_and_official_rejection_v4_supersession_v3_exact10_and_official_rejection_terminal_replay_completed_by_launcher_before_request": True,
        "launcher_empty_rejection_namespace_guard_terminally_replayed_before_request": True,
        "consumer_exec_fd_is_fresh_sealed_memfd":
            stat.S_ISREG(self_guard.exec_before.st_mode) and
            stat.S_IMODE(self_guard.exec_before.st_mode) == 0o444 and
            self_guard.exec_before.st_nlink == 0 and
            self_guard.exec_seals == REQUIRED_EXEC_SEALS,
        "consumer_exec_fd_distinct_from_installed_source_fd":
            (self_guard.exec_before.st_dev, self_guard.exec_before.st_ino) !=
                (self_guard.before.st_dev, self_guard.before.st_ino),
        "consumer_exec_memfd_required_seals_valid":
            self_guard.exec_seals == REQUIRED_EXEC_SEALS,
        "consumer_exec_bytes_equal_installed_source_bytes":
            self_guard.exec_raw == self_guard.raw and
            self_guard.exec_file_sha256 == self_guard.file_sha256,
        "consumer_exec_and_installed_source_terminal_replayed": True,
        "positive_wrapper_emitted_by_combined_child": False,
        "release_required_before_dynamic_guards_close": True,
        "positive_wrapper_raw_fd1_final_newline_write_is_launcher_semantic_commit": True,
        "post_ACK_RELEASE_and_child_exit_are_non_authority_cleanup": True,
        "formal_global_closure_credit": 0,
        "D02_unlock": False,
    })
    ack_raw = canonical(ack) + b"\n"

    # Absolute-last dynamic gate.  All formatting and hashing needed for the
    # ACK is complete before this sequence.  The rejection scan is last.
    c78_guard.terminal_replay()
    fixed_guard.terminal_replay()
    terminal_replay_v3_predecessor_exact10(v3_guard, v3_source_metadata)
    terminal_replay_v4_rejected_static_draft7(
        v4_guard, v4_source_metadata)
    terminal_replay_v5_published_exact10(v5_guard, v5_source_metadata)
    terminal_replay_v6_published_exact10(v6_guard, v6_source_metadata)
    terminal_replay_v7_published_exact10(v7_guard, v7_source_metadata)
    terminal_replay_v8_published_exact10(v8_guard, v8_source_metadata)
    terminal_replay_v9_published_exact10(v9_guard, v9_source_metadata)
    terminal_replay_v10_published_exact10(v10_guard, v10_source_metadata)
    terminal_replay_v11_published_exact10(v11_guard, v11_source_metadata)
    terminal_replay_v12_published_exact10()
    producer_guard.terminal_replay()
    self_guard.terminal_replay()
    policy_guard.terminal_replay()
    public_guard.terminal_replay()
    c42_guard.terminal_replay()
    seal_guard.terminal_replay()
    terminal_committed_stage_absence(runtime_parent)
    need(held_child_lstat_or_absent(
             authority_heads_parent, AUTHORITY_STAGE.name,
             "terminal authority deterministic source stage") is None,
         "terminal authority deterministic source stage absent")
    rejection_guard.terminal_replay()

    written = sys.stdout.buffer.write(ack_raw)
    need(written == len(ack_raw), "complete canonical live ACK stdout write")
    sys.stdout.buffer.flush()

    release_keys = {
        "schema", "status", "protocol", "transaction_binding_sha256",
        "inner_object_sha256", "wrapper_body_domain_sha256",
        "wrapper_object_sha256", "ack_object_sha256", "object_sha256",
    }
    release = _read_canonical_protocol_object(
        "cold live release", LIVE_RELEASE_SCHEMA,
        "RELEASE_AFTER_POSITIVE_WRAPPER_RAW_FD1_FINAL_NEWLINE_COMMIT",
        release_keys)
    need(release.get("transaction_binding_sha256") ==
             request["transaction_binding_sha256"] and
         release.get("inner_object_sha256") == request["inner_object_sha256"] and
         release.get("wrapper_body_domain_sha256") ==
             request["wrapper_body_domain_sha256"] and
         release.get("wrapper_object_sha256") == request["wrapper_object_sha256"] and
         release.get("ack_object_sha256") == ack["object_sha256"],
         "cold live RELEASE exact transaction/inner/prewrapper/wrapper/ACK binding")
    need(os.read(sys.stdin.fileno(), 1) == b"",
         "cold live RELEASE must be followed by immediate EOF and no extra line")


def authorize(
        self_guard: HeldSelf, c78_guard: HeldInputSet,
        fixed_guard: HeldInputSet,
        runtime_parent: HeldCommitParent,
        producer_guard: HeldOpaqueMetadata) -> None:
    """Install a zero seal, or consume it later into a virtual live root."""
    c42_guard = hold_c42_full10_union_candidate9()
    policy_guard = _static_policy_guards()
    v3_guard, v3_source_metadata = hold_v3_predecessor_exact10()
    v4_guard, v4_source_metadata = hold_v4_rejected_static_draft7()
    v5_guard, v5_source_metadata = hold_v5_published_exact10()
    v6_guard, v6_source_metadata = hold_v6_published_exact10()
    v7_guard, v7_source_metadata = hold_v7_published_exact10()
    v8_guard, v8_source_metadata = hold_v8_published_exact10()
    v9_guard, v9_source_metadata = hold_v9_published_exact10()
    v10_guard, v10_source_metadata = hold_v10_published_exact10()
    v11_guard, v11_source_metadata = hold_v11_published_exact10()
    public_guard = _candidate_verification_guards(True)
    commit_parent = HeldCommitParent(AUTHORITY_HEADS, "authority-seal commit parent")
    need(runtime_parent.path == RUNTIME and
         runtime_parent.inherited_launcher_coordination_fd is True,
         "authority uses launcher-owned coordination parent fd")
    seal_state = held_child_lstat_or_absent(
        commit_parent, AUTHORITY_SEAL.name, "authority seal target")
    rejection_guard = _ensure_rejection_namespace(
        seal_state is None, runtime_parent)
    seal_guard: HeldPinnedInput | None = None
    stage_guard: HeldPinnedInput | None = None
    try:
        freeze_proof = static_freeze_proof(
            policy_guard, self_guard, producer_guard,
            v5_guard, v5_source_metadata, v6_guard, v6_source_metadata,
            v7_guard, v7_source_metadata, v8_guard, v8_source_metadata,
            v9_guard, v9_source_metadata, v10_guard, v10_source_metadata,
            v11_guard, v11_source_metadata)
        need(_static_freeze_is_valid(freeze_proof),
             "authority requires final post-source static freeze")
        _, _, completion_objects, rejection, committed_stage_absence = _committed_context(
            self_guard, public_guard, runtime_parent,
            c78_guard, c42_guard, fixed_guard, policy_guard,
            v3_guard, v3_source_metadata, v4_guard, v4_source_metadata,
            v5_guard, v5_source_metadata, v6_guard, v6_source_metadata,
            v7_guard, v7_source_metadata, v8_guard, v8_source_metadata,
            v9_guard, v9_source_metadata,
            v10_guard, v10_source_metadata,
            v11_guard, v11_source_metadata,
            producer_guard)
        preseal = preseal_root(
            public_guard, c42_guard, completion_objects, rejection,
            committed_stage_absence, freeze_proof, runtime_parent)
        consumer_proof = independent_consumer_proof(
            preseal, self_guard, freeze_proof)
        receipt_guard = held_v3_official_rejection(v3_guard)
        if seal_state is not None:
            seal_guard = HeldPinnedInput(
                AUTHORITY_SEAL, "committed C79g v16r2 zero-credit authority seal",
                0o444)
            seal = strict_json(seal_guard.raw, "C79g v16r2 authority seal")
            verify_object(seal, "C79g v16r2 authority seal")
            need(seal.get("schema") == AUTHORITY_SEAL_SCHEMA and
                 seal.get("status") ==
                     "SEALED_COMPOSITE_INPUT__STANDALONE_ZERO_CREDIT" and
                 seal.get("effective_checkpoint_object_sha256") ==
                     UPSTREAM_CHECKPOINT_OBJECT_PIN and
                 seal.get("target_path") == str(AUTHORITY_SEAL.relative_to(ROOT)) and
                 seal.get("consumer_file_sha256") == self_guard.file_sha256 and
                 seal.get("preseal_root_sha256") ==
                     preseal["preseal_root_sha256"] and
                 seal.get("contract_file_sha256") == CONTRACT_FILE_PIN and
                 seal.get("contract_object_sha256") == CONTRACT_OBJECT_PIN and
                 seal.get("closed_schema_file_sha256") == CLOSED_SCHEMA_FILE_PIN and
                 seal.get("v4_rejection_supersession_file_sha256") ==
                     V4_REJECTION_SUPERSESSION_FILE_PIN and
                 seal.get("v4_rejection_supersession_object_sha256") ==
                     V4_REJECTION_SUPERSESSION_OBJECT_PIN and
                 seal.get("v5_official_rejection_file_sha256") ==
                     V5_OFFICIAL_REJECTION_FILE_PIN and
                 seal.get("v5_official_rejection_object_sha256") ==
                     V5_OFFICIAL_REJECTION_OBJECT_PIN and
                 seal.get("v6_official_rejection_file_sha256") ==
                     V6_OFFICIAL_REJECTION_FILE_PIN and
                 seal.get("v6_official_rejection_object_sha256") ==
                     V6_OFFICIAL_REJECTION_OBJECT_PIN and
                 seal.get("v7_official_rejection_file_sha256") ==
                     V7_OFFICIAL_REJECTION_FILE_PIN and
                 seal.get("v7_official_rejection_object_sha256") ==
                     V7_OFFICIAL_REJECTION_OBJECT_PIN and
                 seal.get("v7_publication_lock_continuity_incident") ==
                     _validated_v7_publication_lock_continuity_incident() and
                 seal.get("v16_to_v16r2_transition_file_sha256") ==
                     freeze_proof["v16_to_v16r2_transition_identity"]["file_sha256"] and
                 seal.get("v16_to_v16r2_transition_object_sha256") ==
                     freeze_proof["transition_object_sha256"] and
                 seal.get("static_audit_file_sha256") ==
                     freeze_proof["static_audit_identity"]["file_sha256"] and
                 seal.get("static_audit_object_sha256") ==
                     freeze_proof["static_audit_object_sha256"] and
                 seal.get("cold_launcher_file_sha256") ==
                     freeze_proof["cold_launcher_identity"]["file_sha256"] and
                 seal.get("cold_manifest_file_sha256") ==
                     freeze_proof["cold_launch_manifest_identity"]["file_sha256"] and
                 seal.get("cold_outer_file_sha256") ==
                     freeze_proof["cold_launch_outer_identity"]["file_sha256"] and
                 seal.get("cold_outer_object_sha256") ==
                     freeze_proof["cold_launch_outer_object_sha256"] and
                 seal.get("authority_decision") == "NO_GO_STANDALONE" and
                 seal.get("standalone_seal_credit") == ZERO and
                 seal.get("commit_operation") ==
                     "RENAMEAT2_RENAME_NOREPLACE" and
                 seal.get("renameat2_fallback_allowed") is False,
                 "committed seal binds stable preseal root and remains standalone-zero")
            seal_stage = rooted(str(seal.get("staging_path")))
            need(seal_stage == AUTHORITY_STAGE and
                 held_child_lstat_or_absent(
                     commit_parent, AUTHORITY_STAGE.name,
                     "recorded authority source stage") is None,
                 "committed authority source stage disappeared after NOCLOBBER")
            expected_seal = construct_authority_seal(
                preseal, consumer_proof, freeze_proof, seal_stage)
            need(seal == expected_seal and
                 seal_guard.raw == canonical(expected_seal) + b"\n",
                 "committed seal exact stable canonical reconstruction")
            need(seal_guard.identity not in {item.identity for item in public_guard.files} and
                 seal_guard.mount_id in {item.mount_id for item in public_guard.files},
                 "seal identity isolated from exact24 on the same statx mount")
            durability_recovery_completed = \
                recover_existing_authority_surface_durability(
                    public_guard, seal_guard, rejection_guard,
                    runtime_parent, commit_parent)
            c42_guard.terminal_replay()
            c78_guard.terminal_replay()
            fixed_guard.terminal_replay()
            terminal_replay_v3_predecessor_exact10(
                v3_guard, v3_source_metadata)
            terminal_replay_v4_rejected_static_draft7(
                v4_guard, v4_source_metadata)
            terminal_replay_v5_published_exact10(
                v5_guard, v5_source_metadata)
            terminal_replay_v6_published_exact10(
                v6_guard, v6_source_metadata)
            terminal_replay_v7_published_exact10(
                v7_guard, v7_source_metadata)
            terminal_replay_v8_published_exact10(
                v8_guard, v8_source_metadata)
            terminal_replay_v9_published_exact10(
                v9_guard, v9_source_metadata)
            terminal_replay_v10_published_exact10(
                v10_guard, v10_source_metadata)
            terminal_replay_v11_published_exact10(
                v11_guard, v11_source_metadata)
            terminal_replay_v12_published_exact10()
            producer_guard.terminal_replay()
            policy_guard.terminal_replay()
            public_guard.terminal_replay()
            seal_guard.terminal_replay()
            self_guard.terminal_replay()
            terminal_stage_absence = terminal_committed_stage_absence(runtime_parent)
            # This is deliberately the terminal fresh namespace scan, after
            # every post-seal exact24/full10/SELF/seal replay.
            rejection_guard.terminal_replay()
            inner = authority_root(
                preseal, consumer_proof, seal, public_guard, c42_guard,
                seal_guard, rejection, receipt_guard, freeze_proof,
                terminal_stage_absence, True, True,
                durability_recovery_completed)
            cold_authorize_live_protocol(
                inner, runtime_parent, commit_parent,
                public_guard, c42_guard, seal_guard, policy_guard,
                v3_guard, v3_source_metadata, v4_guard, v4_source_metadata,
                v5_guard, v5_source_metadata, v6_guard, v6_source_metadata,
                v7_guard, v7_source_metadata, v8_guard, v8_source_metadata,
                v9_guard, v9_source_metadata,
                v10_guard, v10_source_metadata,
                v11_guard, v11_source_metadata,
                c78_guard, fixed_guard,
                producer_guard, self_guard, rejection_guard)
            return None

        stage, unused_stage_writer = _new_hidden_stage(
            commit_parent, AUTHORITY_STAGE.name, False)
        need(unused_stage_writer is None and stage == AUTHORITY_STAGE,
             "fixed checkpoint-keyed authority seal stage")
        expected_seal = construct_authority_seal(
            preseal, consumer_proof, freeze_proof, stage)
        expected_seal_raw = canonical(expected_seal) + b"\n"
        stage_guard = commit_parent.exclusive_file(
            stage.name, expected_seal_raw)
        need(stage_guard.raw == expected_seal_raw,
             "authority seal stage exact canonical bytes")
        c42_guard.terminal_replay()
        c78_guard.terminal_replay()
        fixed_guard.terminal_replay()
        terminal_replay_v3_predecessor_exact10(
            v3_guard, v3_source_metadata)
        terminal_replay_v4_rejected_static_draft7(
            v4_guard, v4_source_metadata)
        terminal_replay_v5_published_exact10(
            v5_guard, v5_source_metadata)
        terminal_replay_v6_published_exact10(
            v6_guard, v6_source_metadata)
        terminal_replay_v7_published_exact10(
            v7_guard, v7_source_metadata)
        terminal_replay_v8_published_exact10(
            v8_guard, v8_source_metadata)
        terminal_replay_v9_published_exact10(
            v9_guard, v9_source_metadata)
        terminal_replay_v10_published_exact10(
            v10_guard, v10_source_metadata)
        terminal_replay_v11_published_exact10(
            v11_guard, v11_source_metadata)
        terminal_replay_v12_published_exact10()
        producer_guard.terminal_replay()
        policy_guard.terminal_replay()
        public_guard.terminal_replay()
        stage_guard.terminal_replay()
        self_guard.terminal_replay()
        terminal_committed_stage_absence(runtime_parent)
        rejection_guard.terminal_replay()
        rename_noreplace(
            commit_parent, stage.name, AUTHORITY_SEAL.name,
            stage_guard.identity, stage_guard.mount_id)
        return None
    finally:
        if stage_guard is not None:
            stage_guard.close()
        if seal_guard is not None:
            seal_guard.close()
        commit_parent.close()
        rejection_guard.close()
        public_guard.close()
        policy_guard.close()
        v3_guard.close()
        for item in reversed(v3_source_metadata):
            item.close()
        v4_guard.close()
        for item in reversed(v4_source_metadata):
            item.close()
        v6_guard.close()
        for item in reversed(v6_source_metadata):
            item.close()
        v7_guard.close()
        for item in reversed(v7_source_metadata):
            item.close()
        v8_guard.close()
        for item in reversed(v8_source_metadata):
            item.close()
        v9_guard.close()
        for item in reversed(v9_source_metadata):
            item.close()
        v10_guard.close()
        for item in reversed(v10_source_metadata):
            item.close()
        v11_guard.close()
        for item in reversed(v11_source_metadata):
            item.close()
        v5_guard.close()
        for item in reversed(v5_source_metadata):
            item.close()
        c42_guard.close()
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
         FINAL_CURRENT_V16R2_PINS_INSTALLED is False and
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
    cli = argparse.ArgumentParser(description=__doc__)
    sub = cli.add_subparsers(dest="command", required=True)
    verify_cli = sub.add_parser("verify")
    verify_cli.add_argument("--orientation", required=True, choices=("a", "b"))
    sub.add_parser("assemble")
    sub.add_parser("authorize")
    sub.add_parser(
        "reject", help="non-normative fallback; cold launcher owns normative reject")
    args = cli.parse_args(argv)
    if V16R2_DRAFT_RUNTIME_DISABLED and not FINAL_CURRENT_V16R2_PINS_INSTALLED:
        raise Reject(
            "C79g v16r2 successor is a sentinel draft; runtime is disabled")
    # Constant-only gates bind the inherited root first.  Every later resource
    # is closed in strict reverse construction order on success or failure.
    workspace_root_guard = ensure_configuration()
    self_guard: HeldSelf | None = None
    incident_guard: HeldInheritedV14AuthorityExact12 | None = None
    producer_guard: HeldOpaqueMetadata | None = None
    runtime_parent: HeldCommitParent | None = None
    c78_guard: HeldInputSet | None = None
    fixed_guard: HeldInputSet | None = None
    try:
        self_guard = HeldSelf()
        incident_guard = HeldInheritedV14AuthorityExact12()
        producer_guard = HeldOpaqueMetadata(
            PRODUCER_SOURCE, "C79g producer metadata-only full-run hold", 0o444)
        runtime_parent = HeldCommitParent.from_inherited_launcher_coordination_fd(
            RUNTIME, "launcher-owned runtime coordination parent",
            int(os.environ[COORDINATION_PARENT_FD_ENV]))
        if args.command == "reject":
            reject_checkpoint(self_guard, runtime_parent, producer_guard)
        else:
            # Dynamic/upstream evidence is intentionally opened only after the
            # reject branch.  Drift cannot block the normative launcher reject.
            c78_guard = hold_c78_upstream_surfaces()
            fixed_guard = hold_fixed_evidence_surfaces()
            if args.command == "verify":
                build_verification(
                    args.orientation, self_guard, c78_guard,
                    fixed_guard, runtime_parent, producer_guard)
            elif args.command == "assemble":
                assemble(
                    self_guard, c78_guard, fixed_guard,
                    runtime_parent, producer_guard)
            else:
                authorize(
                    self_guard, c78_guard, fixed_guard,
                    runtime_parent, producer_guard)
        incident_guard.terminal_replay()
        workspace_root_terminal_replay()
        return 0
    finally:
        close_failures: list[str] = []
        for guard in (fixed_guard, c78_guard, runtime_parent,
                      producer_guard, incident_guard, self_guard,
                      workspace_root_guard):
            if guard is None:
                continue
            try:
                guard.close()
            except OSError as exc:
                close_failures.append(type(guard).__name__ + ":" + str(exc))
        if close_failures and sys.exc_info()[0] is None:
            raise Reject("held-resource reverse close failure:" +
                         "|".join(close_failures))


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Reject as exc:
        print("REJECT:", exc, file=sys.stderr)
        raise SystemExit(2)
