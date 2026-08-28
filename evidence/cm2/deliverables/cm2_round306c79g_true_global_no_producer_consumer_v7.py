#!/usr/bin/env python3
"""C79g v7 append-only zero-credit candidate builder.

This append-only v7 binds the independently verified C78s 13-member final
surface.  It independently replays C55A/C55B/C72g, both
byte-identical C78l builds and their verification/completion surface, and the
corresponding C78s surface.  It derives (never guesses) an exact
1,148-row overlay, a compact 76,832-row successor ledger, and all 862
reflection-parent closure rows.  This producer exposes only ``build`` and can
never verifies, assembles, authorizes, or awards credit.  Its candidate outer
is permanently non-authoritative.  The separately committed v7 seal plus the
downstream consumer's secure replay may derive only a zero-credit inner
composite; only the held-fd-bootstrapped, externally SHA-256-pinned cold
launcher may wrap that inner value into the one virtual positive-credit root.
The inline bootstrap, declared Python interpreter, Linux kernel, openat2,
statx, procfs, and sealed memfd are an explicit cold-start TCB.
"""

from __future__ import annotations

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
COLD_EXEC_FD_ENV = "CM2_C79G_V7_COLD_EXEC_FD"
COLD_SOURCE_FD_ENV = "CM2_C79G_V7_COLD_SOURCE_FD"
COLD_COORDINATION_PARENT_FD_ENV = "CM2_C79G_V7_COORDINATION_PARENT_FD"
COLD_WORKSPACE_ROOT_ENV = "CM2_C79G_V7_COLD_WORKSPACE_ROOT"
COLD_WORKSPACE_ROOT_FD_ENV = "CM2_C79G_V7_COLD_WORKSPACE_ROOT_FD"
COLD_LAUNCHER_SHA_ENV = "CM2_C79G_V7_COLD_LAUNCHER_FILE_SHA256"
_cold_root_text = os.environ.get(COLD_WORKSPACE_ROOT_ENV)
ROOT = (Path(_cold_root_text) if _cold_root_text is not None
        else EXECUTED_SOURCE.parents[1])
OUT = ROOT / "deliverables"
SELF = OUT / "cm2_round306c79g_true_global_no_producer_consumer_v7.py"
SCHEMA = "cm2.round306c79g.true-global-no-producer-consumer.v7"
BASE = "cm2_round306c79g_true_global_no_producer_consumer_v7"

CONTRACT = OUT / "cm2_round306c79g_true_global_no_producer_consumer_contract_v7.json"
CLOSED_SCHEMA = OUT / "cm2_round306c79g_true_global_no_producer_consumer_schema_v7.json"
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
V6_TO_V7_TRANSITION = OUT / (
    "cm2_round306c79g_true_global_no_producer_consumer_"
    "v6_to_v7_static_launch_transition_receipt_v1.json")
STATIC_AUDIT_V7 = OUT / "cm2_round306c79g_true_global_no_producer_consumer_static_audit_v7.json"
COLD_LAUNCHER = OUT / "cm2_round306c79g_true_global_no_producer_consumer_cold_launch_v7.py"
COLD_MANIFEST = OUT / "cm2_round306c79g_true_global_no_producer_consumer_cold_launch_manifest_v7.sha256"
COLD_OUTER = OUT / "cm2_round306c79g_true_global_no_producer_consumer_cold_launch_outer_receipt_v7.json"
# These three explicit nonzero sentinels make this append-only source
# mechanically inspectable while making every runtime entry fail at the very
# first gate.  Finalization must replace all three and flip the flag in one
# newly audited source instance; a sentinel is never accepted as a live pin.
FINAL_V7_CORE_PINS_INSTALLED = True
CONTRACT_FILE_PIN = "041ca2567f81c148f765dd85e3515a6ac01295bca06c3032b027459eceb2c014"
CONTRACT_OBJECT_PIN = "a87f7434b32a96923ee81f7761efab9b0937f15103c2fa9b47e8402104b612a5"
CLOSED_SCHEMA_FILE_PIN = "edcdbb568044d04fc7c86b4c4e64fdb7b12b3841f1e93092694ebc3177b6fe18"
V7_DRAFT_CORE_PIN_SENTINELS = (
    "d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7",
    "e7e7e7e7e7e7e7e7e7e7e7e7e7e7e7e7e7e7e7e7e7e7e7e7e7e7e7e7e7e7e7e7",
    "f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7",
)
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
CHECKPOINT_OBJECT_PIN = "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab"
RUNTIME = ROOT / ".cm2-runtime"
CANDIDATE_A = RUNTIME / ("c79g-v7-candidate-a-" + CHECKPOINT_OBJECT_PIN)
CANDIDATE_B = RUNTIME / ("c79g-v7-candidate-b-" + CHECKPOINT_OBJECT_PIN)
COLD_EXACT8 = (
    V6_OFFICIAL_REJECTION,
    CLOSED_SCHEMA,
    CONTRACT,
    SELF,
    OUT / "cm2_round306c79g_true_global_no_producer_consumer_independent_verifier_assembler_authority_consumer_v7.py",
    V6_TO_V7_TRANSITION,
    STATIC_AUDIT_V7,
    COLD_LAUNCHER,
)

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
    ".cm2-runtime/c79g-v5-candidate-a-" + CHECKPOINT_OBJECT_PIN,
    ".cm2-runtime/c79g-v5-candidate-b-" + CHECKPOINT_OBJECT_PIN,
    ".cm2-runtime/c79g-v5-verification-a-" + CHECKPOINT_OBJECT_PIN,
    ".cm2-runtime/c79g-v5-verification-b-" + CHECKPOINT_OBJECT_PIN,
    ".cm2-runtime/c79g-v5-committed-completion-" + CHECKPOINT_OBJECT_PIN,
    ".cm2-runtime/cm2-global-authority-heads/c79g-v5-" +
        CHECKPOINT_OBJECT_PIN + ".seal",
))
V5_DETERMINISTIC_STAGE_SURFACES = tuple(ROOT / value for value in (
    ".cm2-runtime/.c79g-v5-candidate-stage-a-" + CHECKPOINT_OBJECT_PIN,
    ".cm2-runtime/.c79g-v5-candidate-stage-b-" + CHECKPOINT_OBJECT_PIN,
    ".cm2-runtime/.c79g-v5-verification-stage-a-" + CHECKPOINT_OBJECT_PIN,
    ".cm2-runtime/.c79g-v5-verification-stage-b-" + CHECKPOINT_OBJECT_PIN,
    ".cm2-runtime/.c79g-v5-completion-stage-" + CHECKPOINT_OBJECT_PIN,
    ".cm2-runtime/cm2-global-authority-heads/.c79g-v5-authority-stage-" +
        CHECKPOINT_OBJECT_PIN + ".seal",
))
V5_ALL_POSITIVE_AND_STAGE_SURFACES = (
    V5_POSITIVE_RUNTIME_SURFACES + V5_DETERMINISTIC_STAGE_SURFACES)

V6_POSITIVE_RUNTIME_SURFACES = tuple(ROOT / value for value in (
    ".cm2-runtime/c79g-v6-candidate-a-" + CHECKPOINT_OBJECT_PIN,
    ".cm2-runtime/c79g-v6-candidate-b-" + CHECKPOINT_OBJECT_PIN,
    ".cm2-runtime/c79g-v6-verification-a-" + CHECKPOINT_OBJECT_PIN,
    ".cm2-runtime/c79g-v6-verification-b-" + CHECKPOINT_OBJECT_PIN,
    ".cm2-runtime/c79g-v6-committed-completion-" + CHECKPOINT_OBJECT_PIN,
    ".cm2-runtime/cm2-global-authority-heads/c79g-v6-" +
        CHECKPOINT_OBJECT_PIN + ".seal",
))
V6_DETERMINISTIC_STAGE_SURFACES = tuple(ROOT / value for value in (
    ".cm2-runtime/.c79g-v6-candidate-stage-a-" + CHECKPOINT_OBJECT_PIN,
    ".cm2-runtime/.c79g-v6-candidate-stage-b-" + CHECKPOINT_OBJECT_PIN,
    ".cm2-runtime/.c79g-v6-verification-stage-a-" + CHECKPOINT_OBJECT_PIN,
    ".cm2-runtime/.c79g-v6-verification-stage-b-" + CHECKPOINT_OBJECT_PIN,
    ".cm2-runtime/.c79g-v6-completion-stage-" + CHECKPOINT_OBJECT_PIN,
    ".cm2-runtime/cm2-global-authority-heads/.c79g-v6-authority-stage-" +
        CHECKPOINT_OBJECT_PIN + ".seal",
))
V6_ALL_POSITIVE_AND_STAGE_SURFACES = (
    V6_POSITIVE_RUNTIME_SURFACES + V6_DETERMINISTIC_STAGE_SURFACES)

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
    need(sys.platform.startswith("linux"), "Linux-only v7 publication protocol")
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
    """Hold the sealed exec memfd and distinct installed producer source."""

    def __init__(self, exec_inherited: int, source_inherited: int,
                 coordination_inherited: int, root_inherited: int) -> None:
        self.exec_fd = -1
        self.source_fd = -1
        try:
            self.exec_fd = os.dup(exec_inherited)
        except OSError as exc:
            raise Reject("cold-launch inherited sealed producer exec fd unavailable") from exc
        register_held_resource(self)
        try:
            self.source_fd = os.dup(source_inherited)
        except OSError as exc:
            raise Reject("cold-launch inherited installed producer source fd unavailable") from exc

        # This is the first physical gate.  It intentionally touches only the
        # four inherited descriptors; no workspace pathname has been read yet.
        self.exec_before = os.fstat(self.exec_fd)
        self.source_before = os.fstat(self.source_fd)
        coordination_before = os.fstat(coordination_inherited)
        root_before = os.fstat(root_inherited)
        self.exec_mount_id = statx_mount_id(self.exec_fd)
        self.source_mount_id = statx_mount_id(self.source_fd)
        coordination_mount_id = statx_mount_id(coordination_inherited)
        root_mount_id = statx_mount_id(root_inherited)
        try:
            self.exec_seals = int(fcntl.fcntl(self.exec_fd, F_GET_SEALS))
        except OSError as exc:
            raise Reject("cold-launch exec fd is not a seal-capable memfd") from exc
        need(stat.S_ISREG(self.exec_before.st_mode) and
             stat.S_IMODE(self.exec_before.st_mode) == 0o444 and
             self.exec_before.st_nlink == 0 and
             self.exec_seals == REQUIRED_EXEC_SEALS and
             stat.S_ISREG(self.source_before.st_mode) and
             stat.S_IMODE(self.source_before.st_mode) == 0o444 and
             self.source_before.st_nlink == 1 and
             (self.exec_before.st_dev, self.exec_before.st_ino) !=
                 (self.source_before.st_dev, self.source_before.st_ino) and
             stat.S_ISDIR(coordination_before.st_mode) and
             stat.S_ISDIR(root_before.st_mode) and
             self.source_mount_id == coordination_mount_id == root_mount_id,
             "sealed exec/source/coordination/root fd first gate")
        self.exec_raw = self._read_fd(self.exec_fd)
        self.source_raw = self._read_fd(self.source_fd)
        exec_after_read = os.fstat(self.exec_fd)
        source_after_read = os.fstat(self.source_fd)
        need(self.exec_raw == self.source_raw and
             file_fingerprint(exec_after_read) ==
                 file_fingerprint(self.exec_before) and
             file_fingerprint(source_after_read) ==
                 file_fingerprint(self.source_before) and
             int(fcntl.fcntl(self.exec_fd, F_GET_SEALS)) == self.exec_seals and
             statx_mount_id(self.exec_fd) == self.exec_mount_id and
             statx_mount_id(self.source_fd) == self.source_mount_id,
             "sealed exec and installed source stable byte equality first gate")

        # Only after the fd-only first gate may the installed workspace path be
        # observed.  It must be the exact linked source already held above.
        need(SELF == OUT / "cm2_round306c79g_true_global_no_producer_consumer_v7.py",
             "SELF exact frozen producer path")
        before_path = SELF.lstat()
        need(stat.S_ISREG(before_path.st_mode) and
             stat.S_IMODE(before_path.st_mode) == 0o444 and
             before_path.st_nlink == 1 and
             file_fingerprint(before_path) ==
                 file_fingerprint(self.source_before),
             "installed SELF path equals held source fd identity and bytes")
        self.source_path_before = before_path

        # Compatibility aliases intentionally describe the installed source,
        # which is the exact8 member.  Execution itself came from exec_fd.
        self.fd = self.source_fd
        self.before = self.source_before
        self.mount_id = self.source_mount_id
        self.raw = self.source_raw
        self.file_sha256 = sha_bytes(self.source_raw)

    @property
    def identity(self) -> tuple[int, int]:
        """Identity of the installed exact8 source, never the anonymous exec."""
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
        }

    def terminal_replay(self) -> None:
        exec_before = os.fstat(self.exec_fd)
        source_before = os.fstat(self.source_fd)
        path_before = SELF.lstat()
        exec_replay = self._read_fd(self.exec_fd)
        source_replay = self._read_fd(self.source_fd)
        exec_after = os.fstat(self.exec_fd)
        source_after = os.fstat(self.source_fd)
        path_after = SELF.lstat()
        try:
            seals_after = int(fcntl.fcntl(self.exec_fd, F_GET_SEALS))
        except OSError as exc:
            raise Reject("sealed exec fd seal terminal replay unavailable") from exc
        need(exec_replay == source_replay == self.exec_raw == self.source_raw and
             file_fingerprint(exec_before) == file_fingerprint(self.exec_before) ==
                 file_fingerprint(exec_after) and
             file_fingerprint(source_before) ==
                 file_fingerprint(path_before) ==
                 file_fingerprint(self.source_before) ==
                 file_fingerprint(source_after) ==
                 file_fingerprint(path_after) and
             seals_after == self.exec_seals and
             seals_after == REQUIRED_EXEC_SEALS and
             statx_mount_id(self.exec_fd) == self.exec_mount_id and
             statx_mount_id(self.source_fd) == self.source_mount_id,
             "sealed exec plus installed source two-fd terminal byte/identity/seal replay")

    def close(self) -> None:
        # Reverse the acquisition order on every success/failure path.
        first_error: OSError | None = None
        if self.source_fd >= 0:
            descriptor = self.source_fd
            self.source_fd = -1
            self.fd = -1
            try:
                os.close(descriptor)
            except OSError as exc:
                first_error = exc
        if self.exec_fd >= 0:
            descriptor = self.exec_fd
            self.exec_fd = -1
            try:
                os.close(descriptor)
            except OSError as exc:
                if first_error is None:
                    first_error = exc
        if first_error is not None:
            raise first_error


class HeldPinnedInput:
    """Hold one exact observed input snapshot until terminal replay.

    ``expected_mode`` is a per-path historical fact, not an immutability or
    read-only claim.  The held fd and lexical path must retain the same bytes,
    identity, mode, link count, size, timestamps, and mount for this run.
    """

    def __init__(self, path: Path, label: str, expected_mode: int,
                 expected_sha256: str | None = None) -> None:
        self.path = path
        self.label = label
        self.expected_mode = expected_mode
        before_path = path.lstat()
        need(stat.S_ISREG(before_path.st_mode) and not path.is_symlink() and
             stat.S_IMODE(before_path.st_mode) == expected_mode and
             before_path.st_nlink == 1,
             label + ":initial exact observed regular single-link path mode")
        self.fd = openat2_beneath(path, os.O_RDONLY)
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
    name = ".c79g-v7-candidate-stage-" + orientation + "-" + CHECKPOINT_OBJECT_PIN
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
        v7_sources: Mapping[str, bytes]) -> dict[str, Any]:
    """Prove frozen v5 defects and zero-unsafe complete v6/v7 boxes."""
    v5_roles = ("producer_v5", "consumer_v5", "launcher_v5")
    v6_roles = ("producer_v6", "consumer_v6", "launcher_v6")
    v7_roles = ("producer_v7", "consumer_v7", "launcher_v7")
    need(set(v5_sources) == set(v5_roles) and
         set(v6_sources) == set(v6_roles) and
         set(v7_sources) == set(v7_roles),
         "strict-bool source role closure")
    v5 = {role: _strict_bool_need_census(v5_sources[role], role)
          for role in v5_roles}
    v6 = {role: _strict_bool_need_census(v6_sources[role], role)
          for role in v6_roles}
    v7 = {role: _strict_bool_need_census(v7_sources[role], role)
          for role in v7_roles}
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
    need(v6_unproved == 0 and v6_arity == 0 and v6_returns == 0 and
         v7_unproved == 0 and v7_arity == 0 and v7_returns == 0,
         "v6/v7 recursive exact-bool full boxes have zero unsafe or unproved sites")
    return {
        "direct_need_call_count": V5_DIRECT_NEED_CALL_COUNT,
        "risk_count": len(V5_STRICT_BOOL_RISK_IDS),
        "hard_defect_count": len(V5_HARD_STRICT_BOOL_DEFECT_IDS),
        "ordered_risk_ids": list(V5_STRICT_BOOL_RISK_IDS),
        "hard_defect_ids": list(V5_HARD_STRICT_BOOL_DEFECT_IDS),
        "all_seven_present_in_v5": True,
        "same_seven_absent_from_v6": True,
        "same_seven_absent_from_v7": True,
        "v5_recursive_exact_bool_unproved_count": len(observed_v5),
        "v6_recursive_exact_bool_unproved_count": v6_unproved,
        "v7_recursive_exact_bool_unproved_count": v7_unproved,
        "v5_need_call_count_by_role": {
            role: v5[role]["direct_need_call_count"] for role in v5_roles},
        "v6_direct_need_call_count": sum(
            v6[role]["direct_need_call_count"] for role in v6_roles),
        "v7_direct_need_call_count": sum(
            v7[role]["direct_need_call_count"] for role in v7_roles),
        "all_six_sources_AST_parsed_and_compiled_in_memory": True,
        "all_nine_sources_AST_parsed_and_compiled_in_memory": True,
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
    """Fail closed on every final v7 dual-static-audit acceptance field.

    The launcher-template input is deliberately a pre-injection template pin,
    not the installed launcher's final file hash.  Its authority is closed by
    A/B equality, the three-way normalized digest, and the mandatory final
    post-injection normalized replay assertion.
    """
    need(set(audit) == {
             "schema", "status", "audit_path",
             "effective_checkpoint_object_sha256", "audited_v7_bundle",
             "predecessor_v3_exact10_regression",
             "v3_official_later_rejection_regression",
             "predecessor_v4_rejection_supersession_regression",
             "published_then_officially_rejected_predecessor_v5",
             "published_then_officially_rejected_predecessor_v6",
             "dual_independent_static_checkers",
             "coherent_attack_static_census",
             "schema_and_constructor_closure",
             "sealed_exec_and_no_producer_static_proof",
             "static_credit_census", "static_no_run",
             "final_audit_acceptance", "object_sha256",
         } and
         audit.get("schema") ==
             "cm2.round306c79g.true-global-no-producer-consumer."
             "static-audit.v7" and
         audit.get("status") ==
             "PASS_DUAL_STATIC_BYTES_GO_V7__PHYSICAL_COLD_FREEZE_PENDING__"
             "RUNTIME_NOT_AUTHORIZED" and
         audit.get("audit_path") == str(STATIC_AUDIT_V7.relative_to(ROOT)) and
         audit.get("effective_checkpoint_object_sha256") ==
             CHECKPOINT_OBJECT_PIN,
         "final v7 static audit exact top-level PASS_V7 closure")

    dual = audit.get("dual_independent_static_checkers", {})
    need(isinstance(dual, dict) and set(dual) == {
             "checker_A", "checker_B",
             "checker_C_common_census_reproduction",
             "independent_normalizer_count", "all_normalizers_equal",
             "independent_common_callsite_implementation_count",
             "all_common_callsite_censuses_equal",
             "final_launcher_must_reproduce_normalized_digest_after_pin_injection",
         }, "final v7 static audit dual-checker exact8 closure")
    checker_a = dual.get("checker_A", {})
    checker_b = dual.get("checker_B", {})
    checker_c = dual.get("checker_C_common_census_reproduction", {})
    need(isinstance(checker_a, dict) and set(checker_a) == {
             "algorithm", "status", "input_sha256",
             "normalized_launcher_template_sha256",
             "wider_local_callsite_census_row_count",
             "wider_local_callsite_census_sha256", "arity_failure_count",
             "undefined_global_count", "python_literal_dict_count",
             "python_literal_dict_duplicate_key_count",
             "python_AST_and_compile_in_memory_file_count",
             "failed_static_check_count",
         } and
         isinstance(checker_b, dict) and set(checker_b) == {
             "algorithm", "status", "input_sha256",
             "normalized_launcher_template_sha256",
             "common_ordered_callsite_row_count",
             "common_ordered_callsite_census_sha256", "arity_failure_count",
             "starred_positional_total", "double_star_keyword_total",
             "undefined_global_count", "JSON_duplicate_key_count",
             "python_literal_dict_duplicate_key_count",
             "object_closure_failure_count", "pin_failure_count",
             "failed_static_check_count",
         } and
         isinstance(checker_c, dict) and set(checker_c) == {
             "algorithm", "status", "normalized_launcher_template_sha256",
             "common_ordered_callsite_row_count",
             "common_ordered_callsite_census_sha256",
             "common_callsite_kind_census", "arity_failure_count",
             "starred_positional_total", "double_star_keyword_total",
             "failed_static_check_count",
         }, "final v7 checker A/B/C exact object closures")
    need(checker_a.get("algorithm") ==
             "AST_SYMBOL_TABLE_DATAFLOW_CHECKER_A_V1" and
         checker_a.get("status") ==
             "GO_STATIC_CHECKER_A__FINAL_PIN_INJECTION_PENDING__RUNTIME_NOT_AUTHORIZED" and
         checker_b.get("algorithm") ==
             "TOKEN_SYMBOL_TABLE_EXPLICIT_JSON_WALKER_CHECKER_B_V1" and
         checker_b.get("status") ==
             "GO_STATIC_CHECKER_B__FINAL_PIN_INJECTION_PENDING__RUNTIME_NOT_AUTHORIZED" and
         checker_c.get("algorithm") ==
             "INDEPENDENT_LEXICAL_CALLSITE_AND_NORMALIZED_AST_REPRODUCER_C_V1" and
         checker_c.get("status") ==
             "GO_COMMON_DIGEST_REPRODUCED__RUNTIME_NOT_AUTHORIZED",
         "final v7 checker A/B/C algorithms and exact GO statuses")

    input_a = checker_a.get("input_sha256", {})
    input_b = checker_b.get("input_sha256", {})
    input_keys = {
        "schema", "contract_file", "contract_object", "producer", "consumer",
        "transition_file", "transition_object", "launcher_template",
        "v4_supersession_file", "v4_supersession_object",
        "v5_rejection_file", "v5_rejection_object",
        "v6_rejection_file", "v6_rejection_object",
    }
    need(isinstance(input_a, dict) and isinstance(input_b, dict) and
         set(input_a) == input_keys and set(input_b) == input_keys and
         input_a == input_b and
         _nonzero_lower_sha256(input_a.get("launcher_template")) is True,
         "final v7 checker A/B exact14 identical input-pin closure")
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
    }
    need(input_a == expected_inputs and
         all(_nonzero_lower_sha256(value) is True
             for value in input_a.values()),
         "final v7 checker inputs pin exact current core and append-only history")

    normalized_a = checker_a.get("normalized_launcher_template_sha256")
    normalized_b = checker_b.get("normalized_launcher_template_sha256")
    normalized_c = checker_c.get("normalized_launcher_template_sha256")
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
         "final v7 three-way normalized and B/C common-callsite consensus")
    kind_census = checker_c.get("common_callsite_kind_census", {})
    need(isinstance(kind_census, dict) and set(kind_census) == {
             "module_function", "module_constructor", "self_instance_method",
             "cls_class_method", "localclass_static_method",
             "localclass_class_method", "localclass_instance_method",
         } and
         all(type(value) is int and value >= 0
             for value in kind_census.values()) and
         sum(kind_census.values()) == common_count_c,
         "final v7 checker C exact common-callsite kind census")
    need(type(checker_a.get("wider_local_callsite_census_row_count")) is int and
         checker_a.get("wider_local_callsite_census_row_count") > 0 and
         _nonzero_lower_sha256(
             checker_a.get("wider_local_callsite_census_sha256")) is True and
         type(checker_a.get("python_literal_dict_count")) is int and
         checker_a.get("python_literal_dict_count") >= 0 and
         type(checker_a.get(
             "python_AST_and_compile_in_memory_file_count")) is int and
         checker_a.get("python_AST_and_compile_in_memory_file_count") == 3,
         "final v7 checker A positive census and three-file in-memory compile")
    need(type(checker_a.get("arity_failure_count")) is int and
         checker_a.get("arity_failure_count") == 0 and
         type(checker_a.get("undefined_global_count")) is int and
         checker_a.get("undefined_global_count") == 0 and
         type(checker_a.get("python_literal_dict_duplicate_key_count")) is int and
         checker_a.get("python_literal_dict_duplicate_key_count") == 0 and
         type(checker_a.get("failed_static_check_count")) is int and
         checker_a.get("failed_static_check_count") == 0,
         "final v7 checker A zero arity/undefined/duplicate/failed counts")
    for key in (
            "arity_failure_count", "starred_positional_total",
            "double_star_keyword_total", "undefined_global_count",
            "JSON_duplicate_key_count",
            "python_literal_dict_duplicate_key_count",
            "object_closure_failure_count", "pin_failure_count",
            "failed_static_check_count"):
        need(type(checker_b.get(key)) is int and checker_b.get(key) == 0,
             "final v7 checker B exact integer zero:" + key)
    for key in (
            "arity_failure_count", "starred_positional_total",
            "double_star_keyword_total", "failed_static_check_count"):
        need(type(checker_c.get(key)) is int and checker_c.get(key) == 0,
             "final v7 checker C exact integer zero:" + key)
    need(type(dual.get("independent_normalizer_count")) is int and
         dual.get("independent_normalizer_count") == 3 and
         dual.get("all_normalizers_equal") is True and
         type(dual.get(
             "independent_common_callsite_implementation_count")) is int and
         dual.get("independent_common_callsite_implementation_count") == 2 and
         dual.get("all_common_callsite_censuses_equal") is True and
         dual.get(
             "final_launcher_must_reproduce_normalized_digest_after_pin_injection") is True,
         "final v7 dual exact 3/2 checker counts and type-exact consensuses")

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
         attacks.get("exact_unique_ordered_attack_count_required") == 121 and
         type(attacks.get("exact_unique_ordered_attack_count_observed")) is int and
         attacks.get("exact_unique_ordered_attack_count_observed") == 121 and
         attacks.get("attack_name_order_sha256") ==
             "6ba54c7d1847d960cbbd43d0863779e3fb2a2adf7663100936f185a6ce21d01a" and
         attacks.get("all_mutations_route_through_production_validators") is True and
         attacks.get("C42_full10_hash_join_mutations_included") is True and
         attacks.get(
             "C42_three_directory_mode_nlink_universe_guards_are_independent_live_physical_gates") is True and
         attacks.get("attack_execution_deferred_to_cold_runtime") is True,
         "final v7 coherent attack exact7, 121/121, routes, and deferred execution")

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
         }, "final v7 schema/constructor exact21 closure")
    need(type(closure.get("schema_definition_count")) is int and
         closure.get("schema_definition_count") == 38 and
         type(closure.get("schema_ref_count")) is int and
         closure.get("schema_ref_count") == 191 and
         type(closure.get("unresolved_schema_ref_count")) is int and
         closure.get("unresolved_schema_ref_count") == 0 and
         type(closure.get("closed_object_count")) is int and
         closure.get("closed_object_count") == 44 and
         type(closure.get(
             "closed_object_required_property_mismatch_count")) is int and
         closure.get("closed_object_required_property_mismatch_count") == 0 and
         type(closure.get("unknown_schema_validation_keyword_count")) is int and
         closure.get("unknown_schema_validation_keyword_count") == 0 and
         type(closure.get("python_literal_dict_duplicate_key_count")) is int and
         closure.get("python_literal_dict_duplicate_key_count") == 0 and
         type(closure.get("undefined_global_count")) is int and
         closure.get("undefined_global_count") == 0,
         "final v7 schema 38 defs/191 refs/0 unresolved/44 closed/0 mismatch")
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
         "final v7 schema and live-protocol type-exact bool closure")
    actual_keywords = [
        "$defs", "$id", "$ref", "$schema", "additionalProperties",
        "const", "description", "items", "maxItems", "minItems",
        "minLength", "minimum", "pattern", "prefixItems", "properties",
        "required", "title", "type"]
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
         "final v7 exact canonical schema keyword universes and digests")
    shapes = closure.get("output_shape_key_counts", {})
    expected_shapes = {
        "selfIdentity": 33,
        "independentConsumerProof": 48,
        "staticFreezeProof": 53,
        "coldLaunchProof": 86,
        "laterRejection": 43,
        "producerSourceRegistry": 41,
        "liveRequest": 15,
        "liveACK": 32,
        "liveACKCensus": 27,
    }
    need(isinstance(shapes, dict) and set(shapes) == set(expected_shapes) and
         all(type(value) is int for value in shapes.values()) and
         shapes == expected_shapes,
         "final v7 exact nine output-shape key counts")

    acceptance = audit.get("final_audit_acceptance", {})
    need(isinstance(acceptance, dict) and set(acceptance) == {
             "current_draft_pass", "final_failed_static_check_count_required",
             "final_static_freeze_pass_required", "dual_static_checker_A_GO",
             "dual_static_checker_B_GO", "normalized_launcher_digest_consensus",
             "common_callsite_census_digest_consensus",
             "final_launcher_normalized_digest_replay_required_after_pin_injection",
             "this_audit_authorizes_C79_runtime",
             "requires_cold_exact8_freeze_manifest_then_outer_last_and_terminal_replay",
         } and
         acceptance.get("current_draft_pass") is True and
         type(acceptance.get(
             "final_failed_static_check_count_required")) is int and
         acceptance.get("final_failed_static_check_count_required") == 0 and
         acceptance.get("final_static_freeze_pass_required") is True and
         acceptance.get("dual_static_checker_A_GO") is True and
         acceptance.get("dual_static_checker_B_GO") is True and
         acceptance.get("normalized_launcher_digest_consensus") is True and
         acceptance.get("common_callsite_census_digest_consensus") is True and
         acceptance.get(
             "final_launcher_normalized_digest_replay_required_after_pin_injection") is True and
         acceptance.get("this_audit_authorizes_C79_runtime") is False and
         acceptance.get(
             "requires_cold_exact8_freeze_manifest_then_outer_last_and_terminal_replay") is True,
         "final v7 audit acceptance exact10 type-exact zero-runtime closure")


def _hold_modern_published_exact10(
        pins: tuple[tuple[Path, str, str | None], ...], version: int,
        label: str) -> tuple[list[HeldPinnedInput], dict[Path, HeldPinnedInput],
                             dict[str, Any], dict[str, bool]]:
    """Hold and close one v5-or-later published exact8/manifest/outer."""
    guards = [
        HeldPinnedInput(path, label + ":" + path.name, 0o444, file_pin)
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
         outer.get("effective_checkpoint_object_sha256") == CHECKPOINT_OBJECT_PIN and
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
    """Hold current v7 exact10 and every distinct append-only predecessor.

    Current BASE7 begins with the official v6 rejection itself.  The v6 and v5
    published exact10 surfaces remain distinct; v3 exact10, the separate v3
    rejection, and the seven other v4 draft files are also held.  The exact
    distinct-file identity census is therefore 10+10+10+10+7+1 = 48.
    """
    manifest_guard = HeldPinnedInput(
        COLD_MANIFEST, "C79g v7 cold-launch manifest", 0o444)
    outer_guard = HeldPinnedInput(
        COLD_OUTER, "C79g v7 cold-launch outer-last receipt", 0o444)
    manifest_entries = parse_manifest_ordered(
        manifest_guard.raw, "C79g v7 cold-launch exact8 manifest")
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
         manifest_by_path[V6_OFFICIAL_REJECTION] ==
             V6_OFFICIAL_REJECTION_FILE_PIN,
         "cold-launch manifest current SELF, v6 rejection, and policy pins")

    by_path: dict[Path, HeldPinnedInput] = {}
    for path in COLD_EXACT8:
        if path != SELF:
            by_path[path] = HeldPinnedInput(
                path, "C79g v7 cold exact8:" + path.name, 0o444,
                manifest_by_path[path])
    v6_rejection_guard = by_path[V6_OFFICIAL_REJECTION]
    current_cold_ten_guards = [
        self_guard, *by_path.values(), manifest_guard, outer_guard]
    need(len(current_cold_ten_guards) == 10 and
         len({guard.identity for guard in current_cold_ten_guards}) == 10 and
         len({guard.mount_id for guard in current_cold_ten_guards}) == 1,
         "current v7 cold exact10 unique held identities on one statx mount")
    exact8_stats = [
        self_guard.before if path == SELF else by_path[path].before
        for path in COLD_EXACT8
    ]
    chronology = cold_publication_chronology(
        exact8_stats, manifest_guard.before, outer_guard.before)
    need(all(chronology.values()),
         "physical v7 exact8/manifest/outer freeze chronology")

    v6_guards, v6_by_path, v6_outer, v6_chronology = (
        _hold_modern_published_exact10(
            V6_PUBLISHED_EXACT10_PINS, 6, "published v6 exact10"))
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
             CHECKPOINT_OBJECT_PIN and
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
             CHECKPOINT_OBJECT_PIN and
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
    need(set(v5_rejection) == {
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
             "v4_rejection_supersession_object_sha256"} and
         v5_rejection_guard.raw == canonical(v5_rejection) + b"\n" and
         v5_rejection.get("schema") ==
             "cm2.round306c79g.true-global-no-producer-consumer.v5.later-rejection" and
         v5_rejection.get("status") ==
             "PERMANENT_FAIL_CLOSED_REJECTION__ZERO_CREDIT" and
         v5_rejection.get("rejection_reason") ==
             "ORPHANED_OR_INCOMPLETE_C79G_V5_SURFACE" and
         v5_rejection.get("effective_checkpoint_object_sha256") ==
             CHECKPOINT_OBJECT_PIN and
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

    all_file_guards = [
        *current_cold_ten_guards, *v6_guards, *v5_guards, *v3_guards,
        *v4_guards, v3_rejection_guard,
    ]
    need(len(all_file_guards) == 48 and
         len({guard.identity for guard in all_file_guards}) == 48 and
         len({guard.mount_id for guard in all_file_guards}) == 1 and
         v6_namespace_guard.mount_id ==
             v5_namespace_guard.mount_id == all_file_guards[0].mount_id,
         "append-only v7/v6/v5/v3/v4/rejection history is 48 distinct files on one mount")
    require_v5_positive_and_stage_surfaces_absent()

    v7_consumer_path = COLD_EXACT8[4]
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
            "producer_v7": self_guard.raw,
            "consumer_v7": by_path[v7_consumer_path].raw,
            "launcher_v7": by_path[COLD_LAUNCHER].raw,
        })

    transition_guard = by_path[V6_TO_V7_TRANSITION]
    audit_guard = by_path[STATIC_AUDIT_V7]
    transition = strict_json(transition_guard.raw, "C79g v7 transition trust")
    audit = strict_json(audit_guard.raw, "C79g v7 static audit trust")
    outer = strict_json(outer_guard.raw, "C79g v7 cold-launch outer trust")
    need(isinstance(transition, dict) and isinstance(audit, dict) and
         isinstance(outer, dict),
         "post-source transition, audit, and outer are JSON objects")
    verify_object(transition, "C79g v7 transition trust")
    verify_object(audit, "C79g v7 static audit trust")
    verify_object(outer, "C79g v7 cold-launch outer trust")
    _validate_final_static_audit(
        audit, self_guard, by_path, transition_guard, transition)

    successor = transition.get("successor_v7_static_bundle", {})
    predecessor = transition.get("append_only_predecessor_v3_regression", {})
    rejected_v4 = transition.get("rejected_unpublished_predecessor_v4", {})
    published_v5 = transition.get(
        "published_then_officially_rejected_predecessor_v5", {})
    published_v6 = transition.get(
        "published_then_officially_rejected_predecessor_v6", {})
    transition_rejection = predecessor.get("official_later_rejection", {})
    audited = audit.get("audited_v7_bundle", {})
    audit_predecessor = audit.get("predecessor_v3_exact10_regression", {})
    audit_rejection = audit.get("v3_official_later_rejection_regression", {})
    audit_v4 = audit.get("predecessor_v4_rejection_supersession_regression", {})
    audit_v5 = audit.get(
        "published_then_officially_rejected_predecessor_v5", {})
    audit_v6 = audit.get(
        "published_then_officially_rejected_predecessor_v6", {})
    audit_schema = audit.get("schema_and_constructor_closure", {})
    transition_pin = audited.get("v6_to_v7_transition_receipt", {})
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

    v4_receipt = rejected_v4.get("supersession_receipt", {})
    need(transition.get("status") ==
             "STATIC_BYTES_CLOSED_V6_TO_V7__PHYSICAL_FREEZE_PENDING__RUNTIME_NOT_AUTHORIZED" and
         audit.get("status") ==
             "PASS_DUAL_STATIC_BYTES_GO_V7__PHYSICAL_COLD_FREEZE_PENDING__"
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
         "transition/audit pin current v7 and preserve exact v3/v4 history")

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
             "cold-launch-outer-receipt.v7" and
         outer.get("status") ==
             "FROZEN_COLD_LAUNCH_OUTER_LAST__EXACT8_MANIFEST_CLOSED__RUNTIME_DEFERRED" and
         outer.get("effective_checkpoint_object_sha256") ==
             CHECKPOINT_OBJECT_PIN and
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
         "cold-launch v7 outer-last exact8 and zero-credit closure")
    need(os.environ.get(COLD_LAUNCHER_SHA_ENV) ==
             manifest_by_path[COLD_LAUNCHER],
         "sole inherited external launcher anchor matches held closure")
    return {
        "guards": [
            *by_path.values(), *v6_guards, *v5_guards, *v3_guards,
            *v4_guards, v3_rejection_guard,
            v6_namespace_guard, v5_namespace_guard, manifest_guard, outer_guard,
        ],
        "by_path": by_path,
        "v6_published_by_path": v6_by_path,
        "v5_published_by_path": v5_by_path,
        "cold_manifest_guard": manifest_guard,
        "cold_outer_guard": outer_guard,
        "chronology": chronology,
        "v6_predecessor_chronology": v6_chronology,
        "v5_predecessor_chronology": v5_chronology,
        "v3_predecessor_chronology": v3_chronology,
        "transition": transition,
        "audit": audit,
        "outer": outer,
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
        "v6_first_build_entry_attempt": {
            "attempted": True,
            "producer_child_spawned": True,
            "candidate_write_started": False,
            "positive_runtime_surface_count": 0,
        },
        "v6_held_self_identity_defect": {
            "source_path": str(V6_PUBLISHED_EXACT10_PINS[3][0].relative_to(ROOT)),
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
        "append_only_history_unique_file_identity_count": 48,
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
        "published_v6_exact10_plus_official_rejection_strictly_replayed": True,
        "published_v5_exact10_plus_official_rejection_strictly_replayed": True,
        "published_v3_exact10_v4_draft7_and_v3_rejection_strictly_replayed": True,
    }


def ensure_launch_configuration() -> HeldSelf:
    global _COLD_WORKSPACE_ROOT_FD
    global _COLD_WORKSPACE_ROOT_BEFORE
    global _COLD_WORKSPACE_ROOT_MOUNT_ID
    # Absolute first gate: this draft must reject before reading any inherited
    # fd, environment-supplied workspace path, static bundle, or runtime path.
    need(FINAL_V7_CORE_PINS_INSTALLED is True,
         "v7 final core pins are not installed; runtime permanently disabled")
    need(all(value not in V7_DRAFT_CORE_PIN_SENTINELS for value in (
             CONTRACT_FILE_PIN, CONTRACT_OBJECT_PIN, CLOSED_SCHEMA_FILE_PIN)),
         "v7 draft contract/schema sentinels must all be replaced before runtime")
    need(sys.flags.isolated == 1 and sys.flags.dont_write_bytecode == 1 and
         sys.flags.no_site == 1,
         "producer requires cold launcher Python -I -B -S isolation")
    exec_fd_text = os.environ.get(COLD_EXEC_FD_ENV, "")
    source_fd_text = os.environ.get(COLD_SOURCE_FD_ENV, "")
    coordination_fd_text = os.environ.get(COLD_COORDINATION_PARENT_FD_ENV, "")
    root_fd_text = os.environ.get(COLD_WORKSPACE_ROOT_FD_ENV, "")
    launcher_sha = os.environ.get(COLD_LAUNCHER_SHA_ENV, "")
    fd_texts = (exec_fd_text, source_fd_text,
                coordination_fd_text, root_fd_text)
    need(all(value and len(value) <= 10 and
             all(ch in "0123456789" for ch in value) and
             int(value) >= 3 for value in fd_texts) and
         len({int(value) for value in fd_texts}) == 4 and
         EXECUTED_SOURCE == Path("/proc/self/fd") / exec_fd_text and
         _cold_root_text == str(ROOT) and ROOT.is_absolute() and
         SELF == ROOT / "deliverables/cm2_round306c79g_true_global_no_producer_consumer_v7.py",
         "producer accepts only four distinct decimal cold-launch fds and sealed-exec procfd entry")
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
    )
    need(all(isinstance(value, str) and len(value) == 64 and
             value != "0" * 64 and all(ch in "0123456789abcdef" for ch in value)
             for value in static_pins),
         "C79g v7 exact non-placeholder contract/schema/rejection pins")
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
         "C79g v7 exact filled launch configuration")
    need(_COLD_WORKSPACE_ROOT_FD == -1 and
         _COLD_WORKSPACE_ROOT_BEFORE is None and
         _COLD_WORKSPACE_ROOT_MOUNT_ID == -1,
         "cold workspace root guard binds exactly once")
    self_guard = HeldSelf(
        int(exec_fd_text), int(source_fd_text),
        int(coordination_fd_text), int(root_fd_text))
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
         head.get("post_seal_effective_checkpoint_object_sha256") == CHECKPOINT_OBJECT_PIN and
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
    rejection_raw = held[V6_OFFICIAL_REJECTION].raw
    contract = strict_json(contract_raw, "C79g contract")
    verify_object(contract, "C79g contract", CONTRACT_OBJECT_PIN)
    need(contract.get("effective_checkpoint_object_sha256") == CHECKPOINT_OBJECT_PIN and
         contract.get("status") ==
             "STATIC_CONTRACT_BYTES_FINAL__COLD_FREEZE_PENDING__RUNTIME_NOT_AUTHORIZED" and
         contract.get("v7_bundle", {}).get(
             "independent_verifier_assembler_authority_consumer", {}).get("path") ==
             "deliverables/cm2_round306c79g_true_global_no_producer_consumer_"
             "independent_verifier_assembler_authority_consumer_v7.py" and
         contract.get("v7_bundle", {}).get("closed_schema_validator_policy") == {
             "unsupported_validation_keyword_action": "FAIL_CLOSED",
             "runtime_validator_walks_complete_schema_keyword_universe": True,
             "oneOf_keyword_allowed": False,
             "file_and_object_pin_definitions_are_split_closed_types": True,
             "all_closed_object_required_sets_equal_property_sets": True,
             "static_audit_must_pin_actual_and_supported_keyword_universes": True,
         } and
         contract.get("composite_authority_predicate", {}).get("seal_only_GO_allowed") is False and
         contract.get("credit_boundary", {}).get("standalone_authority_seal_credit") == 0,
         "v7 frozen contract checkpoint/composite-only boundary")
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
         "append-only v7 cold root, zero-credit inner, and persisted zero boundary")
    rejection = strict_json(rejection_raw, "C79g official v6 later rejection")
    verify_object(rejection, "C79g official v6 later rejection",
                  V6_OFFICIAL_REJECTION_OBJECT_PIN)
    need(rejection.get("schema") ==
             "cm2.round306c79g.true-global-no-producer-consumer.v6.later-rejection" and
         rejection.get("status") ==
             "PERMANENT_FAIL_CLOSED_REJECTION__ZERO_CREDIT" and
         rejection.get("rejection_reason") ==
             "ORPHANED_OR_INCOMPLETE_C79G_V6_SURFACE" and
         rejection.get("effective_checkpoint_object_sha256") ==
             CHECKPOINT_OBJECT_PIN and
         rejection.get("cold_outer_file_sha256") ==
             V6_PUBLISHED_EXACT10_PINS[9][1] and
         rejection.get("cold_outer_object_sha256") ==
             V6_PUBLISHED_EXACT10_PINS[9][2] and
         rejection.get("formal_global_closure_credit") == 0 and
         rejection.get("D02_unlock") is False and
         rejection.get("D02_started") is False and
         rejection.get("standalone_authority") is False and
         rejection.get("overwrite_delete_or_reuse_allowed") is False and
         rejection.get("target_exact_path") ==
             str(V6_OFFICIAL_REJECTION.relative_to(ROOT)),
         "exact official v6 permanent later rejection semantics")

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
    need(c72["contract"].get("effective_checkpoint_object_sha256") == CHECKPOINT_OBJECT_PIN,
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
        "consumer_file_sha256": self_guard.file_sha256,
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
        "append_only_history_unique_file_identity_count":
            static_trust["append_only_history_unique_file_identity_count"],
        "post_source_static_freeze_trust": {
            "v6_to_v7_transition_receipt": {
                "path": str(V6_TO_V7_TRANSITION.relative_to(ROOT)),
                "file_sha256": static_trust["transition_file_sha256"],
                "object_sha256": static_trust["transition_object_sha256"],
            },
            "static_audit_v7": {
                "path": str(STATIC_AUDIT_V7.relative_to(ROOT)),
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
        "effective_checkpoint_object_sha256": CHECKPOINT_OBJECT_PIN,
        "fixed_input_files": fixed_files,
        "C78l_dual_base_member_pins": c78l_files,
        "C78l_verification_file_sha256": C78L_VERIFY_FILE_PIN,
        "C78l_verification_object_sha256": C78L_VERIFY_OBJECT_PIN,
        "C78l_completion_member_pins": dict(C78L_COMPLETION_PINS),
        "C78s_filled_final_surface": copy.deepcopy(C78S_FINAL),
        "C78s_dual_base_member_pins": c78s_files,
        "C55B_topology_reconstruction": copy.deepcopy(state["C55B_topology"]),
        "C42_C53_direct_Kraft_reconstruction": copy.deepcopy(state["C42_C53_Kraft_chain"]),
        "all_upstream_producer_source_content_opened_or_read": False,
        "all_upstream_producer_source_content_imported_compiled_or_executed": False,
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
        "C79g v7 isolated candidate only; standalone non-authoritative. Formal-global credit "
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
                ".cm2-runtime/.c79g-v7-candidate-stage-{a|b}-" + CHECKPOINT_OBJECT_PIN,
            "fixed_target_set": [
                str(CANDIDATE_A.relative_to(ROOT)),
                str(CANDIDATE_B.relative_to(ROOT)),
            ],
            "actual_orientation_or_stage_path_persisted_in_candidate_bytes": False,
            "orientation_invariant_descriptor_preserves_full_exact9_A_B_byte_identity": True,
            "held_parent_path": str(RUNTIME.relative_to(ROOT)),
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


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
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
