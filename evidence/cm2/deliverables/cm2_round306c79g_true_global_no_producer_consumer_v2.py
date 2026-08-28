#!/usr/bin/env python3
"""C79g v2 zero-credit candidate builder.

This append-only v2 binds the independently verified C78s 13-member final
surface.  It independently replays C55A/C55B/C72g, both
byte-identical C78l builds and their verification/completion surface, and the
corresponding C78s surface.  It derives (never guesses) an exact
1,148-row overlay, a compact 76,832-row successor ledger, and all 862
reflection-parent closure rows.  This producer exposes only ``build`` and can
never finalize or award credit.  Formal global closure credit and the D02
unlock may appear only in the independent verifier/finalizer's last outer
receipt after dual isolated verification.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import copy
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


SELF = Path(os.path.abspath(__file__))
ROOT = SELF.parents[1]
OUT = ROOT / "deliverables"
SCHEMA = "cm2.round306c79g.true-global-no-producer-consumer.v2"
BASE = "cm2_round306c79g_true_global_no_producer_consumer_v2"

CONTRACT = OUT / "cm2_round306c79g_true_global_no_producer_consumer_contract_v2.json"
CLOSED_SCHEMA = OUT / "cm2_round306c79g_true_global_no_producer_consumer_schema_v2.json"
CONTRACT_FILE_PIN = "2430c5ef5ddbd375770258c0149d9c3b6eb87064f972ef35c576152e094e2497"
CONTRACT_OBJECT_PIN = "89704a2cb453311f0199ffff1e04764e9df63a8ea035f6e7e91019841bd2bae8"
CLOSED_SCHEMA_FILE_PIN = "0d3ad29b9080a4b613c9a668d2484760c98c93f95b4a4e91d96a75346909e14e"
CHECKPOINT_OBJECT_PIN = "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab"

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


class HeldSelf:
    """Hold one O_NOFOLLOW SELF fd throughout a complete producer build."""
    def __init__(self) -> None:
        need(SELF == OUT / "cm2_round306c79g_true_global_no_producer_consumer_v2.py",
             "SELF exact frozen producer path")
        before_path = SELF.lstat()
        need(stat.S_ISREG(before_path.st_mode) and not SELF.is_symlink(), "SELF regular path")
        self.fd = os.open(SELF, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
        self.before = os.fstat(self.fd)
        need(stat.S_ISREG(self.before.st_mode) and self.before.st_nlink == 1 and
             (self.before.st_dev, self.before.st_ino) == (before_path.st_dev, before_path.st_ino),
             "SELF held-fd initial identity")
        self.raw = self._read_same_fd()
        self.file_sha256 = sha_bytes(self.raw)

    def _read_same_fd(self) -> bytes:
        os.lseek(self.fd, 0, os.SEEK_SET)
        blocks: list[bytes] = []
        while True:
            block = os.read(self.fd, 1 << 20)
            if not block:
                return b"".join(blocks)
            blocks.append(block)

    def terminal_replay(self) -> None:
        replay = self._read_same_fd()
        after = os.fstat(self.fd)
        path_after = SELF.lstat()
        need(replay == self.raw and
             (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns,
              after.st_ctime_ns, after.st_nlink) ==
             (self.before.st_dev, self.before.st_ino, self.before.st_size,
              self.before.st_mtime_ns, self.before.st_ctime_ns, self.before.st_nlink) and
             (path_after.st_dev, path_after.st_ino, path_after.st_size,
              path_after.st_mtime_ns, path_after.st_ctime_ns, path_after.st_nlink) ==
             (self.before.st_dev, self.before.st_ino, self.before.st_size,
              self.before.st_mtime_ns, self.before.st_ctime_ns, self.before.st_nlink),
             "SELF same-fd terminal replay and path identity")

    def close(self) -> None:
        os.close(self.fd)


def need(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise Reject(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def sha_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def sha_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


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


def ensure_launch_configuration() -> None:
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
         "C79g v2 exact filled launch configuration")


def secure_snapshot(path: Path, required_mode: int | None = None) -> tuple[bytes, tuple[int, int]]:
    try:
        before_path = path.lstat()
    except FileNotFoundError as exc:
        raise Reject("missing input:" + str(path)) from exc
    need(stat.S_ISREG(before_path.st_mode) and not path.is_symlink(),
         "regular non-symlink input:" + str(path))
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
    descriptor = os.open(path, flags)
    try:
        before_fd = os.fstat(descriptor)
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
    need(decoder.eof and not decoder.unused_data and not decoder.unconsumed_tail,
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


def exclusive(path: Path, raw: bytes) -> None:
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0)
    descriptor = os.open(path, flags, 0o444)
    try:
        view = memoryview(raw)
        while view:
            written = os.write(descriptor, view)
            need(written > 0, "write progress:" + path.name)
            view = view[written:]
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def read_pinned(paths: Mapping[str, Path], pins: Mapping[str, str]) -> dict[str, bytes]:
    need(set(paths) == set(pins), "path/pin key equality")
    return {key: secure_file(paths[key], pins[key]) for key in sorted(paths)}


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
    secure_directory(C42_CANDIDATE_DIR)
    c42_candidate_directory_state = directory_state(C42_CANDIDATE_DIR)
    c42_candidate_universe = C42_CANDIDATE_MANIFEST_MEMBERS | {"root_manifest.sha256"}
    need({path.name for path in C42_CANDIDATE_DIR.iterdir()} == c42_candidate_universe,
         "C42 Kraft:candidate directory exact9 universe")
    parent_raw = secure_file(C42_PARENT_PATH, C42_C53_PINS["C42_parent"])
    result_raw = secure_file(C42_RESULT_PATH, C42_C53_PINS["C42_result"])
    manifest_raw = secure_file(C42_MANIFEST_PATH, C42_C53_PINS["C42_manifest"])
    c42_audit_raw = secure_file(
        C42_INDEPENDENT_AUDIT_PATH, C42_C53_PINS["C42_independent_audit"])
    c42_installation_raw = secure_file(
        C42_INSTALLATION_RECEIPT_PATH, C42_C53_PINS["C42_installation_receipt"])
    c42_candidate_token_raw = secure_file(
        C42_CANDIDATE_TOKEN_PATH, C42_C53_PINS["C42_candidate_token"])
    c42_audit_token_raw = secure_file(
        C42_AUDIT_TOKEN_PATH, C42_C53_PINS["C42_audit_token"])
    seal_raw = secure_file(C42_SEAL_PATH, C42_C53_PINS["C42_seal"])
    audit_raw = secure_file(C53_AUDIT_PATH, C42_C53_PINS["C53_audit"])
    head_raw = secure_file(C53_HEAD_PATH, C42_C53_PINS["C53_head"])

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
            raw = secure_unpinned(C42_CANDIDATE_DIR / name)
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
    need(directory_state(C42_CANDIDATE_DIR) == c42_candidate_directory_state and
         {path.name for path in C42_CANDIDATE_DIR.iterdir()} == c42_candidate_universe,
         "C42 Kraft:candidate exact9 terminal directory rescan")
    need(secure_unpinned(C42_MANIFEST_PATH) == manifest_raw,
         "C42 Kraft:root manifest terminal replay")
    for name in sorted(C42_CANDIDATE_MANIFEST_MEMBERS):
        need(secure_unpinned(C42_CANDIDATE_DIR / name) == c42_candidate_member_raw[name],
             "C42 Kraft:manifest member terminal replay:" + name)
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
    }


def one_index(rows: Iterable[dict[str, Any]], key: str, label: str) -> dict[Any, dict[str, Any]]:
    out: dict[Any, dict[str, Any]] = {}
    for row in rows:
        value = row.get(key)
        need(value not in out, label + ":duplicate:" + str(value))
        out[value] = row
    return out


def validate_static_authorities() -> dict[str, Any]:
    contract_raw = secure_file(CONTRACT, CONTRACT_FILE_PIN)
    schema_raw = secure_file(CLOSED_SCHEMA, CLOSED_SCHEMA_FILE_PIN)
    contract = strict_json(contract_raw, "C79g contract")
    verify_object(contract, "C79g contract", CONTRACT_OBJECT_PIN)
    need(contract["effective_checkpoint_object_sha256"] == CHECKPOINT_OBJECT_PIN,
         "contract checkpoint")
    closed = strict_json(schema_raw, "C79g closed schemas")
    need(closed.get("execution_enabled") is True and
         closed.get("producer_execution_role") == "BUILD_ONLY_ZERO_CREDIT" and
         closed.get("C78S_pin_state") == "FILLED_FROM_EXACT_FINAL_13_MEMBER_DUAL_SURFACE" and
         closed.get("C42_C53_Kraft_pin_state") == "FILLED_DIRECT_EXACT_862_ITEMWISE_JOIN",
         "append-only v2 closed schema launch declaration")

    c55a_raw = read_pinned(C55A_PATHS, C55A_PINS)
    c55a = {key: strict_json(c55a_raw[key], "C55A:" + key)
            for key in ("leaf_ledger", "result", "verification")}
    for key in c55a:
        verify_object(c55a[key], "C55A:" + key, C55A_OBJECTS[key])
    need(c55a["result"].get("bnb", {}).get("unresolved_zero") is False and
         c55a["result"].get("bnb", {}).get("remaining_unresolved_leaf_count") == EXPECTED_OVERLAY and
         c55a["leaf_ledger"].get("census", {}).get("UNRESOLVED_R1648_CONTINUATION") == EXPECTED_OVERLAY,
         "C55A predecessor unresolved census")

    c55b_raw = read_pinned(C55B_PATHS, C55B_PINS)
    c55b_objects = {key: strict_json(c55b_raw[key], "C55B:" + key)
                    for key in ("result", "verification", "self_test")}
    for key in c55b_objects:
        verify_object(c55b_objects[key], "C55B:" + key, C55B_OBJECTS[key])
    need(c55b_objects["result"].get("global_closure_proved") is False and
         c55b_objects["result"].get("unresolved_zero") is False,
         "C55B structure-only boundary")
    need(c55b_objects["self_test"].get("status", "").startswith("PASS_16_OF_16"),
         "C55B independent self-test")

    c72_raw = read_pinned(C72G_PATHS, C72G_PINS)
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
        "C55A_raw": c55a_raw,
        "C55A": c55a,
        "C55B_raw": c55b_raw,
        "C55B": c55b_objects,
        "C72g_raw": c72_raw,
        "C72g": c72,
    }


def validate_c78l() -> dict[str, Any]:
    raw = read_dual(C78L_A, C78L_B, C78L_NAMES, C78L_PINS, "C78l")
    verification_a = secure_file(C78L_VERIFY_A, C78L_VERIFY_FILE_PIN)
    verification_b = secure_file(C78L_VERIFY_B, C78L_VERIFY_FILE_PIN)
    need(verification_a == verification_b, "C78l verification A/B bytes")
    verification = strict_json(verification_a, "C78l verification")
    verify_object(verification, "C78l verification", C78L_VERIFY_OBJECT_PIN)
    need(verification.get("status", "").startswith("PASS_INDEPENDENT_C78L") and
         verification.get("self_test", {}).get("attack_count") == 52 and
         all(value == "FAIL_CLOSED" for value in
             verification.get("self_test", {}).get("attacks", {}).values()),
         "C78l independent verification")
    completion_raw = {
        key: secure_file(C78L_COMPLETION / name, C78L_COMPLETION_PINS[key])
        for key, name in C78L_COMPLETION_NAMES.items()
    }
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
    manifest = parse_manifest(raw["manifest"], "C78l manifest")
    for key in ("lock", "tasks", "sides", "cells", "pairs", "registry", "result", "report"):
        need(manifest.get(C78L_NAMES[key]) == C78L_PINS[key], "C78l manifest:" + key)
    return {
        "raw": raw,
        "verification_raw": verification_a,
        "verification": verification,
        "completion_raw": completion_raw,
        "completion": receipt,
        "result": result,
        "cells": gzip_rows(raw["cells"], "C78l public cells"),
        "pairs": gzip_rows(raw["pairs"], "C78l reflection pairs"),
    }


def validate_c78s() -> dict[str, Any]:
    a = rooted(str(C78S_FINAL["build_A_directory"]))
    b = rooted(str(C78S_FINAL["build_B_directory"]))
    pins = C78S_FINAL["pins"]
    need(isinstance(pins, dict), "C78s pins mapping")
    secure_directory(a, 0o555)
    secure_directory(b, 0o555)
    need((a.lstat().st_dev, a.lstat().st_ino) != (b.lstat().st_dev, b.lstat().st_ino),
         "C78s isolated stage directories distinct")
    verification_a_path = rooted(str(C78S_FINAL["verification_A_path"]))
    verification_b_path = rooted(str(C78S_FINAL["verification_B_path"]))
    final_manifest_a_path = rooted(str(C78S_FINAL["final_manifest_A_path"]))
    final_manifest_b_path = rooted(str(C78S_FINAL["final_manifest_B_path"]))
    final_outer_a_path = rooted(str(C78S_FINAL["final_outer_A_path"]))
    final_outer_b_path = rooted(str(C78S_FINAL["final_outer_B_path"]))
    expected_stage_names = set(C78S_NAMES.values()) | {
        verification_a_path.name, final_manifest_a_path.name, final_outer_a_path.name,
    }
    need(len(expected_stage_names) == 13 and
         {path.name for path in a.iterdir()} == expected_stage_names and
         {path.name for path in b.iterdir()} == expected_stage_names,
         "C78s exact 13-member stage universes")
    raw: dict[str, bytes] = {}
    stage_member_raw: dict[str, bytes] = {}
    for key, name in C78S_NAMES.items():
        left, left_identity = secure_snapshot(a / name, 0o444)
        right, right_identity = secure_snapshot(b / name, 0o444)
        need(sha_bytes(left) == pins[key] and sha_bytes(right) == pins[key] and left == right,
             "C78s pinned dual base member:" + key)
        need(left_identity != right_identity, "C78s base member inode separation:" + key)
        raw[key] = left
        stage_member_raw[name] = left
    verify_a_raw, verify_a_identity = secure_snapshot(verification_a_path, 0o444)
    verify_b_raw, verify_b_identity = secure_snapshot(verification_b_path, 0o444)
    need(sha_bytes(verify_a_raw) == C78S_FINAL["verification_A_file_sha256"] and
         sha_bytes(verify_b_raw) == C78S_FINAL["verification_B_file_sha256"] and
         verify_a_identity != verify_b_identity,
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

    final_manifest_a_raw, final_manifest_a_identity = secure_snapshot(final_manifest_a_path, 0o444)
    final_manifest_b_raw, final_manifest_b_identity = secure_snapshot(final_manifest_b_path, 0o444)
    final_outer_a_raw, final_outer_a_identity = secure_snapshot(final_outer_a_path, 0o444)
    final_outer_b_raw, final_outer_b_identity = secure_snapshot(final_outer_b_path, 0o444)
    need(sha_bytes(final_manifest_a_raw) == C78S_FINAL["final_manifest_file_sha256"] and
         sha_bytes(final_manifest_b_raw) == C78S_FINAL["final_manifest_file_sha256"] and
         sha_bytes(final_outer_a_raw) == C78S_FINAL["final_outer_file_sha256"] and
         sha_bytes(final_outer_b_raw) == C78S_FINAL["final_outer_file_sha256"] and
         final_manifest_a_identity != final_manifest_b_identity and
         final_outer_a_identity != final_outer_b_identity,
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
        base_data_mtime = max((directory / C78S_NAMES[key]).stat().st_mtime_ns
                              for key in ("lock", "children", "sources", "pairs", "cells",
                                          "projection", "result", "report"))
        need(base_data_mtime < (directory / C78S_NAMES["manifest"]).stat().st_mtime_ns <
             (directory / C78S_NAMES["outer"]).stat().st_mtime_ns <
             verification_path.stat().st_mtime_ns < final_manifest_path.stat().st_mtime_ns <
             final_outer_path.stat().st_mtime_ns,
             "C78s base/verification/final-manifest/final-outer strict mtime order")
    stage_member_raw[verification_a_path.name] = verify_a_raw
    stage_member_raw[final_manifest_a_path.name] = final_manifest_a_raw
    stage_member_raw[final_outer_a_path.name] = final_outer_a_raw
    need(len(stage_member_raw) == 13, "C78s terminal replay member count")
    for name, expected_raw in stage_member_raw.items():
        replay_a, _ = secure_snapshot(a / name, 0o444)
        replay_b, _ = secure_snapshot(b / name, 0o444)
        need(replay_a == expected_raw and replay_b == expected_raw,
             "C78s post-final-outer terminal replay:" + name)

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
    }


def reconstruct() -> dict[str, Any]:
    static = validate_static_authorities()
    c78l = validate_c78l()
    c78s = validate_c78s()

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
            if key not in {"C42_rows_by_pair", "C53_projections_by_pair"}
        },
        "baseline_count": retained,
        "overlay_count": replaced,
    }


def input_registry(state: dict[str, Any], self_file_sha256: str) -> dict[str, Any]:
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
        "consumer_file_sha256": self_file_sha256,
        "contract_file_sha256": CONTRACT_FILE_PIN,
        "contract_object_sha256": CONTRACT_OBJECT_PIN,
        "closed_schema_file_sha256": CLOSED_SCHEMA_FILE_PIN,
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
        "all_upstream_producer_sources_opened_or_read": False,
        "all_upstream_producer_sources_imported_compiled_or_executed": False,
        "terminal_authority": {"C78l_rows": EXPECTED_LARGE, "C78s_rows": EXPECTED_SINGLETON},
        "structure_only_authority": ["C55A", "C55B", "C72g"],
        "C55A_C55B_C72g_new_terminal_authority": False,
        "canonical_pointer_written": False,
        "D02_started": False,
        "candidate_credit": dict(ZERO_CANDIDATE_CREDIT),
    })


def build(outdir: Path, self_guard: HeldSelf) -> None:
    # The caller/main has already executed ensure_launch_configuration().
    # No input was read and no output path was touched before that gate.
    state = reconstruct()
    need(not outdir.exists() and outdir.parent.is_dir(), "fresh append-only candidate directory")

    overlay_raw, overlay_desc = gzip_encode(state["overlay_rows"])
    successor_raw, successor_desc = gzip_encode(state["successor_rows"])
    parents_raw, parents_desc = gzip_encode(state["parent_rows"])
    need(overlay_desc["row_count"] == EXPECTED_OVERLAY and
         successor_desc["row_count"] == EXPECTED_UNIVERSE and
         parents_desc["row_count"] == EXPECTED_PAIRS,
         "output descriptor counts")
    registry = input_registry(state, self_guard.file_sha256)
    descriptors = {
        "overlay_1148": overlay_desc,
        "full_successor_76832": successor_desc,
        "reflection_parent_closure_862": parents_desc,
    }
    final_census = dict(state["final_census"])
    final_census["total"] = sum(final_census.values())
    result = close_object({
        "schema": SCHEMA + ".result",
        "status": "PASS_CANDIDATE_1148_EXACT_OVERLAY__76832_FULL_SUCCESSOR__862_REFLECTION_PARENTS__PUBLIC_UNRESOLVED_ZERO__AWAIT_DUAL_COMPLETION_FOR_FORMAL_CREDIT",
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
        "formal_credit_authority": "INDEPENDENT_NO_PRODUCER_FINALIZER_GLOBAL_OUTER_ONLY",
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
        "- candidate credit is zero; formal global closure credit exists only after dual completion\n"
        f"- D02 gate/task credit: `0/0`; formal pending tasks: `{EXPECTED_PENDING_D02}`; D02 not started\n"
        "- no canonical pointer.\n"
    ).encode("utf-8")
    lock = (
        "C79g isolated candidate only. Formal-global credit remains zero until the unique "
        "dual-build, dual-verification completion surface is sealed. D02 is not started.\n"
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
    os.mkdir(outdir, 0o755)
    for name in (LOCK, OVERLAY, SUCCESSOR, PARENTS, REGISTRY, RESULT, REPORT):
        exclusive(outdir / name, base_raw[name])
    manifest_raw = b"".join(
        f"{sha_bytes(base_raw[name])}  {name}\n".encode("ascii")
        for name in (LOCK, OVERLAY, SUCCESSOR, PARENTS, REGISTRY, RESULT, REPORT)
    )
    exclusive(outdir / CANDIDATE_MANIFEST, manifest_raw)
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
        "candidate_credit": dict(ZERO_CANDIDATE_CREDIT),
        "canonical_pointer_written": False,
        "D02_started": False,
    })
    exclusive(outdir / CANDIDATE_OUTER, canonical(outer) + b"\n")
    base_mtimes = [(outdir / name).stat().st_mtime_ns
                   for name in (LOCK, OVERLAY, SUCCESSOR, PARENTS, REGISTRY, RESULT, REPORT)]
    manifest_mtime = (outdir / CANDIDATE_MANIFEST).stat().st_mtime_ns
    outer_mtime = (outdir / CANDIDATE_OUTER).stat().st_mtime_ns
    need(max(base_mtimes) < manifest_mtime < outer_mtime,
         "candidate publication mtime order and outer-last")
    for name in CANDIDATE_MEMBERS:
        secure_snapshot(outdir / name, 0o444)
    os.chmod(outdir, 0o555)
    secure_directory(outdir, 0o555)
    self_guard.terminal_replay()



def parser() -> argparse.ArgumentParser:
    cli = argparse.ArgumentParser(description=__doc__)
    sub = cli.add_subparsers(dest="command", required=True)
    build_cmd = sub.add_parser("build")
    build_cmd.add_argument("--outdir", required=True, type=Path)
    return cli


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    # Mandatory first gate after argument parsing.  Do not move any read,
    # existence check, directory creation, or producer/verifier work above it.
    ensure_launch_configuration()
    self_guard = HeldSelf()
    try:
        build(args.outdir, self_guard)
    finally:
        self_guard.close()
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Reject as exc:
        print("REJECT:", exc, file=sys.stderr)
        raise SystemExit(2)
