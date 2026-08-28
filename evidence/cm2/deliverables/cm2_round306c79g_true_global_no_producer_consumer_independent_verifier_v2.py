#!/usr/bin/env python3
"""Independent C79g v2 no-producer verifier and finalizer.

The verifier never opens, reads, imports, compiles, decodes, or executes the
C79g producer or any upstream producer source.  It reconstructs the complete
pinned evidence chain, exact ledgers, direct C42/C53 Kraft joins, and exact 121
production-validator attacks.  Two swapped-orientation runs create isolated,
byte-identical verification surfaces.  The independent finalizer alone may
publish the exact4 completion surface and its unique final outer credit.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import copy
import hashlib
import json
import os
from pathlib import Path
import stat
import sys
from typing import Any, Iterable, Mapping
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
ATTACK_NAME_ORDER_PIN = "6ba54c7d1847d960cbbd43d0863779e3fb2a2adf7663100936f185a6ce21d01a"
PRODUCER_SOURCE_PIN = "771fbaf2e0d52a0bf47c7d7093be42a8fb9da0a86ca0bad9c844fb35625a23ae"
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
VERIFICATION_FILE = BASE + "_independent_verification_v2.json"
COMPLETION_VERIFICATION = BASE + "_completion_verification_copy_v2.json"
COMPLETION_RECEIPT = BASE + "_pre_outer_completion_receipt_v2.json"
GLOBAL_MANIFEST = BASE + "_one_global_manifest_v2.sha256"
FINAL_OUTER = BASE + "_final_outer_receipt_v2.json"
COMPLETION_MEMBERS = (COMPLETION_VERIFICATION, COMPLETION_RECEIPT, GLOBAL_MANIFEST, FINAL_OUTER)


class Reject(RuntimeError):
    pass


class HeldSelf:
    """Hold one O_NOFOLLOW SELF fd across the entire verifier/finalizer run."""
    def __init__(self) -> None:
        need(SELF == OUT /
             "cm2_round306c79g_true_global_no_producer_consumer_independent_verifier_v2.py",
             "SELF exact frozen verifier/finalizer path")
        before_path = SELF.lstat()
        need(stat.S_ISREG(before_path.st_mode) and not SELF.is_symlink(), "SELF regular path")
        self.fd = os.open(SELF, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
        self.before = os.fstat(self.fd)
        need(stat.S_ISREG(self.before.st_mode) and self.before.st_nlink == 1 and
             (self.before.st_dev, self.before.st_ino) == (before_path.st_dev, before_path.st_ino),
             "SELF held-fd initial identity")
        self.raw = self._read_same_fd()
        self.file_sha256 = sha(self.raw)

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


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Reject(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def digest(value: Any) -> str:
    return sha(canonical(value))


def close_row(body: dict[str, Any]) -> dict[str, Any]:
    need("row_sha256" not in body, "close row")
    return {**body, "row_sha256": digest(body)}


def close_object(body: dict[str, Any]) -> dict[str, Any]:
    need("object_sha256" not in body, "close object")
    return {**body, "object_sha256": digest(body)}


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


def ensure_c78s_filled() -> None:
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


def secure_snapshot(path: Path, required_mode: int | None = None) -> tuple[bytes, tuple[int, int]]:
    try:
        before_path = path.lstat()
    except FileNotFoundError as exc:
        raise Reject("missing input:" + str(path)) from exc
    need(stat.S_ISREG(before_path.st_mode) and not path.is_symlink(), "regular input:" + str(path))
    descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(descriptor)
        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1 and
             (before.st_dev, before.st_ino) == (before_path.st_dev, before_path.st_ino),
             "descriptor identity:" + str(path))
        if required_mode is not None:
            need(stat.S_IMODE(before.st_mode) == required_mode,
                 f"required mode {required_mode:o}:" + str(path))
        blocks: list[bytes] = []
        while True:
            block = os.read(descriptor, 1 << 20)
            if not block:
                break
            blocks.append(block)
        after = os.fstat(descriptor)
        need((before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns,
              before.st_ctime_ns, before.st_nlink) ==
             (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns,
              after.st_ctime_ns, after.st_nlink), "stable descriptor:" + str(path))
    finally:
        os.close(descriptor)
    path_after = path.lstat()
    need((path_after.st_dev, path_after.st_ino, path_after.st_size, path_after.st_mtime_ns,
          path_after.st_ctime_ns, path_after.st_nlink) ==
         (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns,
          after.st_ctime_ns, after.st_nlink), "stable path:" + str(path))
    return b"".join(blocks), (before.st_dev, before.st_ino)


def secure_unpinned(path: Path, required_mode: int | None = None) -> bytes:
    return secure_snapshot(path, required_mode)[0]


def secure(path: Path, pin: str) -> bytes:
    raw = secure_unpinned(path)
    need(sha(raw) == pin, "file pin:" + str(path))
    return raw


def secure_dir(path: Path, required_mode: int | None = None) -> None:
    info = path.lstat()
    need(stat.S_ISDIR(info.st_mode) and not path.is_symlink(), "secure directory:" + str(path))
    if required_mode is not None:
        need(stat.S_IMODE(info.st_mode) == required_mode,
             f"required directory mode {required_mode:o}:" + str(path))


def directory_state(path: Path) -> tuple[int, int, int, int, int, int]:
    info = path.lstat()
    need(stat.S_ISDIR(info.st_mode) and not path.is_symlink(), "directory state:" + str(path))
    return (info.st_dev, info.st_ino, info.st_mode, info.st_mtime_ns, info.st_ctime_ns, info.st_nlink)


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
    need(decoder.eof and not decoder.unused_data and not decoder.unconsumed_tail,
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


def validate_c42_c53_kraft(cell_rows: list[dict[str, Any]]) -> dict[str, Any]:
    """Direct itemwise C42 authority -> C53 audit -> C55B crosswalk join."""
    secure_dir(C42_CANDIDATE_DIR)
    c42_candidate_directory_state = directory_state(C42_CANDIDATE_DIR)
    c42_candidate_universe = C42_CANDIDATE_MANIFEST_MEMBERS | {"root_manifest.sha256"}
    need({path.name for path in C42_CANDIDATE_DIR.iterdir()} == c42_candidate_universe,
         "C42 Kraft:candidate directory exact9 universe")
    c42_rows = gzip_rows(secure(C42_PARENT_PATH, C42_C53_PINS["C42_parent"]),
                         "C42 installed parent conservation")
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

    result = strict_json(secure(C42_RESULT_PATH, C42_C53_PINS["C42_result"]), "C42 result")
    verify_object(result, "C42 result", C42_RESULT_OBJECT_PIN)
    need(result.get("closure_census", {}).get("parent_conservation_row_count") == PAIR_COUNT and
         result.get("formal_authority") is False and
         result.get("producer_output_is_authority") is False,
         "C42 Kraft:producer nonauthority boundary")
    c42_manifest_raw = secure(C42_MANIFEST_PATH, C42_C53_PINS["C42_manifest"])
    manifest = parse_manifest(c42_manifest_raw, "C42 root manifest")
    need(len(manifest) == 8 and set(manifest) == C42_CANDIDATE_MANIFEST_MEMBERS and
         manifest["parent_conservation.jsonl.gz"] == C42_C53_PINS["C42_parent"] and
         manifest["result.json"] == C42_C53_PINS["C42_result"],
         "C42 Kraft:exact root manifest")
    c42_candidate_member_raw: dict[str, bytes] = {}
    for name in manifest:
        if name == "parent_conservation.jsonl.gz":
            raw = secure(C42_PARENT_PATH, C42_C53_PINS["C42_parent"])
        elif name == "result.json":
            raw = secure(C42_RESULT_PATH, C42_C53_PINS["C42_result"])
        else:
            raw = secure_unpinned(C42_CANDIDATE_DIR / name)
        need(sha(raw) == manifest[name], "C42 Kraft:manifest member replay:" + name)
        c42_candidate_member_raw[name] = raw
    need(set(c42_candidate_member_raw) == C42_CANDIDATE_MANIFEST_MEMBERS,
         "C42 Kraft:all exact8 manifest members replayed")

    c42_candidate_token_raw = secure(
        C42_CANDIDATE_TOKEN_PATH, C42_C53_PINS["C42_candidate_token"])
    c42_audit_token_raw = secure(C42_AUDIT_TOKEN_PATH, C42_C53_PINS["C42_audit_token"])
    need(c42_candidate_token_raw == (C42_CANDIDATE_TOKEN + "\n").encode("ascii") and
         c42_audit_token_raw == (C42_AUDIT_TOKEN + "\n").encode("ascii"),
         "C42 Kraft:exact installed candidate/audit token bytes")
    c42_audit = strict_json(
        secure(C42_INDEPENDENT_AUDIT_PATH, C42_C53_PINS["C42_independent_audit"]),
        "C42 independent audit")
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

    c42_installation = strict_json(
        secure(C42_INSTALLATION_RECEIPT_PATH, C42_C53_PINS["C42_installation_receipt"]),
        "C42 installation receipt")
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
    seal = strict_json(secure(C42_SEAL_PATH, C42_C53_PINS["C42_seal"]), "C42 seal")
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

    audit = strict_json(secure(C53_AUDIT_PATH, C42_C53_PINS["C53_audit"]), "C53 audit")
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
    head = strict_json(secure(C53_HEAD_PATH, C42_C53_PINS["C53_head"]), "C53 head")
    head_body = copy.deepcopy(head)
    head_claim = head_body.pop("authority_seal_object_sha256", None)
    need(head_claim == C53_HEAD_OBJECT_PIN and head_claim == digest(head_body) and
         head.get("independent_audit_object_sha256") == C53_AUDIT_OBJECT_PIN and
         head.get("post_seal_effective_checkpoint_object_sha256") == CHECKPOINT_OBJECT_PIN and
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
    need(directory_state(C42_CANDIDATE_DIR) == c42_candidate_directory_state and
         {path.name for path in C42_CANDIDATE_DIR.iterdir()} == c42_candidate_universe,
         "C42 Kraft:candidate exact9 terminal directory rescan")
    need(secure_unpinned(C42_MANIFEST_PATH) == c42_manifest_raw,
         "C42 Kraft:root manifest terminal replay")
    for name in sorted(C42_CANDIDATE_MANIFEST_MEMBERS):
        need(secure_unpinned(C42_CANDIDATE_DIR / name) == c42_candidate_member_raw[name],
             "C42 Kraft:manifest member terminal replay:" + name)
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


def dual(a: Path, b: Path, names: Mapping[str, str], pins: Mapping[str, str], label: str) -> dict[str, bytes]:
    secure_dir(a); secure_dir(b)
    need(set(names) == set(pins), label + ":keys")
    out: dict[str, bytes] = {}
    for key in sorted(names):
        left = secure(a / names[key], pins[key]); right = secure(b / names[key], pins[key])
        need(left == right, label + ":dual bytes:" + key)
        out[key] = left
    return out


def read_evidence() -> dict[str, Any]:
    contract = strict_json(secure(CONTRACT, CONTRACT_FILE_PIN), "contract")
    verify_object(contract, "contract", CONTRACT_OBJECT_PIN)
    need(contract["effective_checkpoint_object_sha256"] == CHECKPOINT_OBJECT_PIN, "checkpoint")
    closed = strict_json(secure(CLOSED_SCHEMA, CLOSED_SCHEMA_FILE_PIN), "closed schema")
    need(closed.get("execution_enabled") is True and
         closed.get("verifier_execution_role") == "DUAL_SWAPPED_ORIENTATION_NO_PRODUCER" and
         closed.get("finalizer_execution_role") ==
             "INDEPENDENT_NO_PRODUCER_FINAL_OUTER_ONLY_CREDIT" and
         closed.get("C42_C53_Kraft_pin_state") == "FILLED_DIRECT_EXACT_862_ITEMWISE_JOIN",
         "append-only v2 verifier/finalizer schema declaration")

    fixed = {key: secure(FIXED_PATHS[key], FIXED_PINS[key]) for key in sorted(FIXED_PATHS)}
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
    kraft_chain = validate_c42_c53_kraft(c55b_cells)

    secure_dir(C78L_A, 0o755); secure_dir(C78L_B, 0o755)
    c78l_directory_states = {path: directory_state(path) for path in (C78L_A, C78L_B)}
    need((C78L_A.lstat().st_dev, C78L_A.lstat().st_ino) !=
         (C78L_B.lstat().st_dev, C78L_B.lstat().st_ino) and
         {path.name for path in C78L_A.iterdir()} == set(C78L_NAMES.values()) and
         {path.name for path in C78L_B.iterdir()} == set(C78L_NAMES.values()),
         "C78l exact dual historical 0755/10-member surfaces")
    c78l = dual(C78L_A, C78L_B, C78L_NAMES, C78L_PINS, "C78l")
    for key, name in C78L_NAMES.items():
        left, left_identity = secure_snapshot(C78L_A / name, 0o444)
        right, right_identity = secure_snapshot(C78L_B / name, 0o444)
        need(left == right == c78l[key] and left_identity != right_identity,
             "C78l member mode/link/inode separation:" + key)
    lva, lva_identity = secure_snapshot(C78L_VERIFY_A, 0o444)
    lvb, lvb_identity = secure_snapshot(C78L_VERIFY_B, 0o444)
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
    secure_dir(C78L_COMPLETION, 0o755)
    c78l_directory_states[C78L_COMPLETION] = directory_state(C78L_COMPLETION)
    need({path.name for path in C78L_COMPLETION.iterdir()} == set(C78L_COMPLETION_NAMES.values()),
         "C78l completion exact3 historical surface")
    completion_raw: dict[str, bytes] = {}
    for key, name in C78L_COMPLETION_NAMES.items():
        raw, _ = secure_snapshot(C78L_COMPLETION / name, 0o444)
        need(sha(raw) == C78L_COMPLETION_PINS[key], "C78l completion pin:" + key)
        completion_raw[key] = raw
        if key == "receipt":
            value = strict_json(raw, "C78l completion"); verify_object(value, "C78l completion", C78L_COMPLETION_OBJECT)
        elif key == "outer":
            value = strict_json(raw, "C78l completion outer"); verify_object(value, "C78l completion outer", C78L_COMPLETION_OUTER_OBJECT)
    need(parse_manifest_ordered(completion_raw["manifest"], "C78l completion manifest") ==
         [{"file_sha256": C78L_COMPLETION_PINS["receipt"],
           "entry_name": C78L_COMPLETION_NAMES["receipt"]}] and
         (C78L_COMPLETION / C78L_COMPLETION_NAMES["receipt"]).stat().st_mtime_ns <
         (C78L_COMPLETION / C78L_COMPLETION_NAMES["manifest"]).stat().st_mtime_ns <
         (C78L_COMPLETION / C78L_COMPLETION_NAMES["outer"]).stat().st_mtime_ns,
         "C78l completion manifest/order/outer-last")
    need(max(C78L_VERIFY_A.stat().st_mtime_ns, C78L_VERIFY_B.stat().st_mtime_ns) <
         (C78L_COMPLETION / C78L_COMPLETION_NAMES["receipt"]).stat().st_mtime_ns,
         "C78l both verifications before completion")
    base_order = ["lock", "cells", "pairs", "report", "result", "registry", "tasks", "sides"]
    need(parse_manifest_ordered(c78l["manifest"], "C78l base manifest") ==
         [{"file_sha256": C78L_PINS[key], "entry_name": C78L_NAMES[key]} for key in base_order],
         "C78l exact ordered base8 manifest")
    for directory in (C78L_A, C78L_B):
        base_max = max((directory / C78L_NAMES[key]).stat().st_mtime_ns for key in base_order)
        need(base_max < (directory / C78L_NAMES["manifest"]).stat().st_mtime_ns <
             (directory / C78L_NAMES["outer"]).stat().st_mtime_ns,
             "C78l build manifest/outer mtime order")
        for key, name in C78L_NAMES.items():
            replay, _ = secure_snapshot(directory / name, 0o444)
            need(replay == c78l[key], "C78l terminal replay:" + key)
    need((C78L_A / C78L_NAMES["outer"]).stat().st_mtime_ns < C78L_VERIFY_A.stat().st_mtime_ns and
         (C78L_B / C78L_NAMES["outer"]).stat().st_mtime_ns < C78L_VERIFY_B.stat().st_mtime_ns,
         "C78l corresponding outer before independent verification")
    for key, name in C78L_COMPLETION_NAMES.items():
        replay, _ = secure_snapshot(C78L_COMPLETION / name, 0o444)
        need(replay == completion_raw[key], "C78l completion replay:" + key)
    lresult = strict_json(c78l["result"], "C78l result"); verify_object(lresult, "C78l result", C78L_RESULT_OBJECT)

    c78s_a = rooted(str(C78S_FINAL["build_A_directory"]))
    c78s_b = rooted(str(C78S_FINAL["build_B_directory"]))
    secure_dir(c78s_a, 0o555); secure_dir(c78s_b, 0o555)
    c78s_directory_states = {path: directory_state(path) for path in (c78s_a, c78s_b)}
    need((c78s_a.lstat().st_dev, c78s_a.lstat().st_ino) !=
         (c78s_b.lstat().st_dev, c78s_b.lstat().st_ino),
         "C78s isolated directory identities")
    sva_path = rooted(str(C78S_FINAL["verification_A_path"]))
    svb_path = rooted(str(C78S_FINAL["verification_B_path"]))
    fma_path = rooted(str(C78S_FINAL["final_manifest_A_path"]))
    fmb_path = rooted(str(C78S_FINAL["final_manifest_B_path"]))
    foa_path = rooted(str(C78S_FINAL["final_outer_A_path"]))
    fob_path = rooted(str(C78S_FINAL["final_outer_B_path"]))
    exact13 = set(C78S_NAMES.values()) | {sva_path.name, fma_path.name, foa_path.name}
    need(len(exact13) == 13 and {path.name for path in c78s_a.iterdir()} == exact13 and
         {path.name for path in c78s_b.iterdir()} == exact13,
         "C78s exact13 stage universes")
    c78s = dual(c78s_a, c78s_b, C78S_NAMES, C78S_FINAL["pins"], "C78s")
    stage_raw: dict[str, bytes] = {}
    for key, name in C78S_NAMES.items():
        left, left_identity = secure_snapshot(c78s_a / name, 0o444)
        right, right_identity = secure_snapshot(c78s_b / name, 0o444)
        need(left == right == c78s[key] and left_identity != right_identity,
             "C78s base member mode/link/inode separation:" + key)
        stage_raw[name] = left
    sva, sva_identity = secure_snapshot(sva_path, 0o444)
    svb, svb_identity = secure_snapshot(svb_path, 0o444)
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
    final_manifest_a, fma_identity = secure_snapshot(fma_path, 0o444)
    final_manifest_b, fmb_identity = secure_snapshot(fmb_path, 0o444)
    final_outer_a, foa_identity = secure_snapshot(foa_path, 0o444)
    final_outer_b, fob_identity = secure_snapshot(fob_path, 0o444)
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
        base_max = max((directory / C78S_NAMES[key]).stat().st_mtime_ns for key in base_order)
        need(base_max < (directory / C78S_NAMES["manifest"]).stat().st_mtime_ns <
             (directory / C78S_NAMES["outer"]).stat().st_mtime_ns <
             verification_path.stat().st_mtime_ns < manifest_path.stat().st_mtime_ns <
             outer_path.stat().st_mtime_ns, "C78s strict publication mtime order")
    stage_raw[sva_path.name] = sva
    stage_raw[fma_path.name] = final_manifest_a
    stage_raw[foa_path.name] = final_outer_a
    need(len(stage_raw) == 13, "C78s replay exact13")
    for name, expected_raw in stage_raw.items():
        replay_a, _ = secure_snapshot(c78s_a / name, 0o444)
        replay_b, _ = secure_snapshot(c78s_b / name, 0o444)
        need(replay_a == replay_b == expected_raw, "C78s terminal replay:" + name)
    sresult = strict_json(c78s["result"], "C78s result")
    verify_object(sresult, "C78s result", str(C78S_FINAL["result_object_sha256"]))
    # Owner-writable historical C78l directories and all sealed C78s stages
    # receive a final universe/state rescan after every other evidence read.
    for directory in (C78L_A, C78L_B):
        need(directory_state(directory) == c78l_directory_states[directory] and
             {path.name for path in directory.iterdir()} == set(C78L_NAMES.values()),
             "C78l terminal directory state/universe rescan")
        for key, name in C78L_NAMES.items():
            replay, _ = secure_snapshot(directory / name, 0o444)
            need(replay == c78l[key], "C78l final post-evidence replay:" + key)
    need(directory_state(C78L_COMPLETION) == c78l_directory_states[C78L_COMPLETION] and
         {path.name for path in C78L_COMPLETION.iterdir()} == set(C78L_COMPLETION_NAMES.values()),
         "C78l completion terminal state/universe rescan")
    for key, name in C78L_COMPLETION_NAMES.items():
        replay, _ = secure_snapshot(C78L_COMPLETION / name, 0o444)
        need(replay == completion_raw[key], "C78l final completion replay:" + key)
    replay_lva, replay_lva_identity = secure_snapshot(C78L_VERIFY_A, 0o444)
    replay_lvb, replay_lvb_identity = secure_snapshot(C78L_VERIFY_B, 0o444)
    need(replay_lva == lva and replay_lvb == lvb and
         replay_lva_identity == lva_identity and replay_lvb_identity == lvb_identity,
         "C78l final dual verification replay")
    for directory in (c78s_a, c78s_b):
        need(directory_state(directory) == c78s_directory_states[directory] and
             {path.name for path in directory.iterdir()} == exact13,
             "C78s terminal directory state/universe rescan")
        for name, expected_raw in stage_raw.items():
            replay, _ = secure_snapshot(directory / name, 0o444)
            need(replay == expected_raw, "C78s final post-evidence replay:" + name)
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
    return {"overlay": overlay_rows, "successor": successor_rows, "parents": parent_rows,
            "census": {key: census.get(key, 0) for key in sorted(TERMINALS)},
            "modes": dict(sorted(modes.items())),
            "C55B_topology": copy.deepcopy(evidence["c55b_topology"]),
            "Kraft_chain_summary": {
                key: copy.deepcopy(value) for key, value in evidence["kraft_chain"].items()
                if key not in {"C42_rows_by_pair", "C53_projections_by_pair"}
            }}


def candidate(candidate_dir: Path, peer_candidate_dir: Path) -> dict[str, Any]:
    secure_dir(candidate_dir, 0o555)
    secure_dir(peer_candidate_dir, 0o555)
    left_dir = candidate_dir.lstat(); right_dir = peer_candidate_dir.lstat()
    need((left_dir.st_dev, left_dir.st_ino) != (right_dir.st_dev, right_dir.st_ino),
         "dual candidate directory identity separation")
    directory_states = {candidate_dir: directory_state(candidate_dir),
                        peer_candidate_dir: directory_state(peer_candidate_dir)}
    need({path.name for path in candidate_dir.iterdir()} == set(MEMBERS),
         "candidate A exact member universe")
    need({path.name for path in peer_candidate_dir.iterdir()} == set(MEMBERS),
         "candidate B exact member universe")
    raw: dict[str, bytes] = {}
    peer_raw: dict[str, bytes] = {}
    for name in MEMBERS:
        left, left_identity = secure_snapshot(candidate_dir / name, 0o444)
        right, right_identity = secure_snapshot(peer_candidate_dir / name, 0o444)
        need(left == right, "dual candidate byte identity:" + name)
        need(left_identity != right_identity, "dual candidate inode separation:" + name)
        raw[name] = left
        peer_raw[name] = right
    manifest = parse_manifest(raw[MANIFEST], "candidate manifest")
    need(set(manifest) == {LOCK, OVERLAY, SUCCESSOR, PARENTS, REGISTRY, RESULT, REPORT},
         "candidate manifest exact universe")
    for name in (LOCK, OVERLAY, SUCCESSOR, PARENTS, REGISTRY, RESULT, REPORT):
        need(manifest.get(name) == sha(raw[name]), "candidate manifest:" + name)
    outer = strict_json(raw[OUTER_RECEIPT], "candidate outer"); verify_object(outer, "candidate outer")
    need(outer["candidate_manifest_file_sha256"] == sha(raw[MANIFEST]) and
         outer["candidate_outer_receipt_published_last"] is True and
         outer["candidate_credit"] == ZERO and outer["canonical_pointer_written"] is False,
         "candidate outer semantics")
    registry = strict_json(raw[REGISTRY], "candidate registry"); verify_object(registry, "candidate registry")
    result = strict_json(raw[RESULT], "candidate result"); verify_object(result, "candidate result")
    need(result["source_registry_object_sha256"] == registry["object_sha256"] and
         outer["candidate_result_object_sha256"] == result["object_sha256"], "object chain")
    for directory in (candidate_dir, peer_candidate_dir):
        base_mtimes = [(directory / name).stat().st_mtime_ns
                       for name in (LOCK, OVERLAY, SUCCESSOR, PARENTS, REGISTRY, RESULT, REPORT)]
        manifest_mtime = (directory / MANIFEST).stat().st_mtime_ns
        outer_mtime = (directory / OUTER_RECEIPT).stat().st_mtime_ns
        need(max(base_mtimes) < manifest_mtime < outer_mtime,
             "candidate publication mtime order and outer-last:" + str(directory))
    # A second secure itemwise read is the verifier's terminal replay of both
    # already-sealed candidate surfaces.
    for name in MEMBERS:
        replay_a, _ = secure_snapshot(candidate_dir / name, 0o444)
        replay_b, _ = secure_snapshot(peer_candidate_dir / name, 0o444)
        need(replay_a == raw[name] and replay_b == peer_raw[name],
             "dual candidate terminal replay:" + name)
    for directory in (candidate_dir, peer_candidate_dir):
        need(directory_state(directory) == directory_states[directory] and
             {path.name for path in directory.iterdir()} == set(MEMBERS),
             "candidate terminal directory state/exact9 rescan")
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
    need(decoder.eof and not decoder.unused_data and not decoder.unconsumed_tail and
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
             "closure", "candidate_credit", "formal_credit_authority", "precursor_credits",
             "actual_C3_disposition_count", "conditional_C3_promoted_to_actual_C3",
             "canonical_pointer_written", "D02_started", "object_sha256"} and
         result["schema"] == SCHEMA + ".result" and
         result["status"] ==
             "PASS_CANDIDATE_1148_EXACT_OVERLAY__76832_FULL_SUCCESSOR__862_REFLECTION_PARENTS__PUBLIC_UNRESOLVED_ZERO__AWAIT_DUAL_COMPLETION_FOR_FORMAL_CREDIT" and
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
         result["formal_credit_authority"] ==
             "INDEPENDENT_NO_PRODUCER_FINALIZER_GLOBAL_OUTER_ONLY" and
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
             "schema", "consumer_file_sha256", "contract_file_sha256", "contract_object_sha256",
             "closed_schema_file_sha256", "effective_checkpoint_object_sha256", "fixed_input_files",
             "C78l_dual_base_member_pins", "C78l_verification_file_sha256",
             "C78l_verification_object_sha256", "C78l_completion_member_pins",
             "C78s_filled_final_surface", "C78s_dual_base_member_pins",
             "C55B_topology_reconstruction", "C42_C53_direct_Kraft_reconstruction",
             "all_upstream_producer_sources_opened_or_read",
             "all_upstream_producer_sources_imported_compiled_or_executed",
             "terminal_authority", "structure_only_authority",
             "C55A_C55B_C72g_new_terminal_authority", "canonical_pointer_written",
             "D02_started", "candidate_credit", "object_sha256"} and
         registry["schema"] == SCHEMA + ".source-registry" and
         registry["contract_file_sha256"] == CONTRACT_FILE_PIN and
         registry["contract_object_sha256"] == CONTRACT_OBJECT_PIN and
         registry["closed_schema_file_sha256"] == CLOSED_SCHEMA_FILE_PIN and
         registry["effective_checkpoint_object_sha256"] == CHECKPOINT_OBJECT_PIN and
         isinstance(registry["consumer_file_sha256"], str) and
         registry["consumer_file_sha256"] == PRODUCER_SOURCE_PIN and
         registry["fixed_input_files"] == expected_fixed_registry and
         registry["C78l_dual_base_member_pins"] == expected_c78l_registry and
         registry["C78l_verification_file_sha256"] == C78L_VERIFY_FILE and
         registry["C78l_verification_object_sha256"] == C78L_VERIFY_OBJECT and
         registry["C78l_completion_member_pins"] == C78L_COMPLETION_PINS and
         registry["C78s_filled_final_surface"] == C78S_FINAL and
         registry["C78s_dual_base_member_pins"] == expected_c78s_registry and
         registry["C55B_topology_reconstruction"] == expected["C55B_topology"] and
         registry["C42_C53_direct_Kraft_reconstruction"] == expected["Kraft_chain_summary"] and
         registry["all_upstream_producer_sources_opened_or_read"] is False and
         registry["all_upstream_producer_sources_imported_compiled_or_executed"] is False and
         registry["C55A_C55B_C72g_new_terminal_authority"] is False and
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
             "partial_publication_policy", "candidate_credit", "canonical_pointer_written",
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
         outer.get("candidate_credit") == ZERO and
         outer.get("canonical_pointer_written") is False and outer.get("D02_started") is False,
         "metadata validator:outer/result/registry chain")


def validate_attack_patch(patch: dict[str, Any], pristine: dict[str, Any],
                          expected: dict[str, Any]) -> None:
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
        ("registry:producer_opened", "registry", ("all_upstream_producer_sources_opened_or_read",)),
        ("registry:producer_executed", "registry", ("all_upstream_producer_sources_imported_compiled_or_executed",)),
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
    raise Reject("unknown attack family:" + family)


def run_attacks(pristine: dict[str, Any], expected: dict[str, Any]) -> dict[str, dict[str, str]]:
    cases = make_attack_cases(pristine)
    names = [name for name, _ in cases]
    need(len(cases) == 121 and len(set(names)) == 121 and
         _line_sequence_sha256(names) == ATTACK_NAME_ORDER_PIN,
         "exact 121 unique ordered actual attacks")
    results: dict[str, dict[str, str]] = {}
    for name, create_patch in cases:
        patch = create_patch()
        need(isinstance(patch, dict) and patch, "nonempty actual attack patch:" + name)
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


def exclusive(path: Path, raw: bytes) -> None:
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL |
                         getattr(os, "O_NOFOLLOW", 0), 0o444)
    try:
        view = memoryview(raw)
        while view:
            count = os.write(descriptor, view)
            need(count > 0, "verification write")
            view = view[count:]
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def construct_expected_verification(
        actual: dict[str, Any], expected: dict[str, Any],
        attacks: dict[str, dict[str, str]], self_file_sha256: str,
        producer_file_sha256: str,
        member_hashes: Mapping[str, str]) -> dict[str, Any]:
    """Pure constructor shared by verifier publication and finalizer replay."""
    census = dict(expected["census"]); census["total"] = sum(census.values())
    attack_names = list(attacks)
    return close_object({
        "schema": SCHEMA + ".independent-verification",
        "status": "PASS_INDEPENDENT_C79G_V2__EXACT_121_ATTACKS__CANDIDATE_ZERO_CREDIT",
        "verifier_file_sha256": self_file_sha256,
        "declared_producer_file_sha256": producer_file_sha256,
        "producer_hash_is_declarative_binding_only": True,
        "producer_was_not_opened_read_decoded_parsed_compiled_imported_or_executed": True,
        "verification_orientation_is_order_invariant": True,
        "candidate_member_file_sha256": dict(member_hashes),
        "dual_candidate_build_directories_mode": actual["dual_candidate_build_directories_mode"],
        "dual_candidate_members_mode": actual["dual_candidate_members_mode"],
        "dual_candidate_members_single_link": actual["dual_candidate_members_single_link"],
        "dual_candidate_members_byte_identical": actual["dual_candidate_members_byte_identical"],
        "dual_candidate_corresponding_inodes_distinct":
            actual["dual_candidate_corresponding_inodes_distinct"],
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
            "rejected": sum(record["status"] == "FAIL_CLOSED" for record in attacks.values()),
            "names": attack_names,
            "name_order_sha256": _line_sequence_sha256(attack_names),
            "records": attacks,
        },
        "all_attacks_fail_closed":
            all(record.get("status") == "FAIL_CLOSED" for record in attacks.values()),
        "candidate_credit": dict(ZERO),
        "formal_credit_authority": "INDEPENDENT_NO_PRODUCER_FINALIZER_GLOBAL_OUTER_ONLY",
        "precursor_credits_zero": True,
        "canonical_pointer_written": False,
        "D02_started": False,
    })


def build_verification(candidate_dir: Path, peer_candidate_dir: Path,
                       verification_dir: Path, self_guard: HeldSelf) -> None:
    evidence = read_evidence()
    expected = reconstruct_expected(evidence)
    actual = candidate(candidate_dir, peer_candidate_dir)
    compare(actual, expected)
    validate_candidate_metadata(actual["result"], actual["registry"], actual["outer"],
                                actual["manifest"], actual["raw"], expected)
    attacks = run_attacks(attack_model(actual, evidence), expected)
    member_hashes = {name: sha(actual["raw"][name]) for name in sorted(MEMBERS)}
    verification = construct_expected_verification(
        actual, expected, attacks, self_guard.file_sha256,
        PRODUCER_SOURCE_PIN, member_hashes)
    need(not verification_dir.exists() and verification_dir.parent.is_dir(),
         "fresh verification directory")
    os.mkdir(verification_dir, 0o755)
    verification_path = verification_dir / VERIFICATION_FILE
    verification_raw = canonical(verification) + b"\n"
    exclusive(verification_path, verification_raw)
    replay, _ = secure_snapshot(verification_path, 0o444)
    need(replay == verification_raw, "verification terminal replay")
    os.chmod(verification_dir, 0o555)
    secure_dir(verification_dir, 0o555)
    self_guard.terminal_replay()


def read_verification_surface(
        directory: Path, expected_verification: Mapping[str, Any]
        ) -> tuple[bytes, dict[str, Any], tuple[int, int]]:
    secure_dir(directory, 0o555)
    initial_directory_state = directory_state(directory)
    need({path.name for path in directory.iterdir()} == {VERIFICATION_FILE},
         "verification exact one-member surface")
    raw, identity = secure_snapshot(directory / VERIFICATION_FILE, 0o444)
    value = strict_json(raw, "C79g verification surface")
    verify_object(value, "C79g verification surface")
    attacks = value.get("coherent_attacks", {})
    names = attacks.get("names")
    records = attacks.get("records")
    need(set(value) == {
             "schema", "status", "verifier_file_sha256", "declared_producer_file_sha256",
             "producer_hash_is_declarative_binding_only",
             "producer_was_not_opened_read_decoded_parsed_compiled_imported_or_executed",
             "verification_orientation_is_order_invariant", "candidate_member_file_sha256",
             "dual_candidate_build_directories_mode", "dual_candidate_members_mode",
             "dual_candidate_members_single_link", "dual_candidate_members_byte_identical",
             "dual_candidate_corresponding_inodes_distinct", "reconstruction",
             "coherent_attacks", "all_attacks_fail_closed", "candidate_credit",
             "formal_credit_authority", "precursor_credits_zero", "canonical_pointer_written",
             "D02_started", "object_sha256"} and
         value == dict(expected_verification) and
         raw == canonical(dict(expected_verification)) + b"\n" and
         value.get("status") ==
             "PASS_INDEPENDENT_C79G_V2__EXACT_121_ATTACKS__CANDIDATE_ZERO_CREDIT" and
         value.get("verifier_file_sha256") == expected_verification["verifier_file_sha256"] and
         value.get("declared_producer_file_sha256") == PRODUCER_SOURCE_PIN and
         value.get("producer_hash_is_declarative_binding_only") is True and
         value.get("producer_was_not_opened_read_decoded_parsed_compiled_imported_or_executed") is True and
         value.get("verification_orientation_is_order_invariant") is True and
         value.get("candidate_member_file_sha256") ==
             expected_verification["candidate_member_file_sha256"] and
         value.get("dual_candidate_build_directories_mode") == "0555" and
         value.get("dual_candidate_members_mode") == "0444" and
         value.get("dual_candidate_members_single_link") is True and
         value.get("dual_candidate_members_byte_identical") is True and
         value.get("dual_candidate_corresponding_inodes_distinct") is True and
         value.get("candidate_credit") == ZERO and
         value.get("formal_credit_authority") ==
             "INDEPENDENT_NO_PRODUCER_FINALIZER_GLOBAL_OUTER_ONLY" and
         value.get("canonical_pointer_written") is False and value.get("D02_started") is False and
         value.get("precursor_credits_zero") is True and
         isinstance(value.get("reconstruction"), dict) and
         set(value["reconstruction"]) == {
             "overlay_rows", "successor_rows", "reflection_parent_rows",
             "derived_final_four_class_census", "authority_partition",
             "public_global_unresolved", "closure", "C42_C53_C55B_direct_Kraft_pair_count"} and
         value["reconstruction"] == expected_verification["reconstruction"] and
         set(attacks) == {"attack_count", "rejected", "names", "name_order_sha256", "records"} and
         attacks.get("attack_count") == 121 and attacks.get("rejected") == 121 and
         isinstance(names, list) and len(names) == 121 and len(set(names)) == 121 and
         attacks.get("name_order_sha256") == ATTACK_NAME_ORDER_PIN and
         _line_sequence_sha256(names) == ATTACK_NAME_ORDER_PIN and
         isinstance(records, dict) and set(records) == set(names) and
         all(set(record) == {"status", "validator_route", "actual_rejection_stage"} and
             record.get("status") == "FAIL_CLOSED" and
             record.get("validator_route") == attack_validator_route(name) and
             isinstance(record.get("actual_rejection_stage"), str) and record["actual_rejection_stage"]
             for name, record in records.items()) and
         value.get("all_attacks_fail_closed") is True,
         "verification exact independently reconstructed production semantics")
    replay, replay_identity = secure_snapshot(directory / VERIFICATION_FILE, 0o444)
    need(replay == raw and replay_identity == identity and
         directory_state(directory) == initial_directory_state and
         {path.name for path in directory.iterdir()} == {VERIFICATION_FILE},
         "verification terminal directory/member replay")
    return raw, value, identity


def finalize(candidate_a: Path, candidate_b: Path, verification_a: Path,
             verification_b: Path, completion_dir: Path, self_guard: HeldSelf) -> None:
    # The finalizer replays the full no-producer reconstruction itself; it does
    # not accept either verifier's conclusion as a substitute for evidence.
    evidence = read_evidence()
    expected = reconstruct_expected(evidence)
    actual = candidate(candidate_a, candidate_b)
    compare(actual, expected)
    validate_candidate_metadata(actual["result"], actual["registry"], actual["outer"],
                                actual["manifest"], actual["raw"], expected)
    self_file_sha256 = self_guard.file_sha256
    member_hashes = {name: sha(actual["raw"][name]) for name in sorted(MEMBERS)}
    # The finalizer does not authenticate the verification files by their
    # self-hashes.  It independently re-executes the exact production attack
    # suite and constructs the sole acceptable verification object.
    finalizer_attacks = run_attacks(attack_model(actual, evidence), expected)
    expected_verification = construct_expected_verification(
        actual, expected, finalizer_attacks, self_file_sha256,
        PRODUCER_SOURCE_PIN, member_hashes)
    va_raw, va, va_identity = read_verification_surface(
        verification_a, expected_verification)
    vb_raw, vb, vb_identity = read_verification_surface(
        verification_b, expected_verification)
    expected_verification_raw = canonical(expected_verification) + b"\n"
    need(va_raw == vb_raw == expected_verification_raw and
         va == vb == expected_verification and va_identity != vb_identity,
         "dual verification exact reconstructed bytes/object and inode separation")
    all_dirs = [candidate_a, candidate_b, verification_a, verification_b]
    identities = {(path.lstat().st_dev, path.lstat().st_ino) for path in all_dirs}
    need(len(identities) == 4, "candidate and verification directory isolation")
    need(not completion_dir.exists() and completion_dir.parent.is_dir(),
         "fresh completion directory")
    os.mkdir(completion_dir, 0o755)

    completion_verification_raw = va_raw
    exclusive(completion_dir / COMPLETION_VERIFICATION, completion_verification_raw)
    completion_receipt = close_object({
        "schema": SCHEMA + ".pre-outer-completion-receipt",
        "status": "PASS_DUAL_ISOLATED_CANDIDATES_AND_DUAL_INDEPENDENT_VERIFICATIONS__AWAIT_FINAL_OUTER",
        "candidate_A_result_object_sha256": actual["result"]["object_sha256"],
        "candidate_B_result_object_sha256": actual["result"]["object_sha256"],
        "candidate_A_outer_object_sha256": actual["outer"]["object_sha256"],
        "candidate_B_outer_object_sha256": actual["outer"]["object_sha256"],
        "verification_A_object_sha256": va["object_sha256"],
        "verification_B_object_sha256": vb["object_sha256"],
        "dual_candidate_bytes_identical_inodes_distinct": True,
        "dual_verification_bytes_identical_inodes_distinct": True,
        "independent_no_producer_reconstruction_replayed": True,
        "candidate_credit": dict(ZERO),
        "canonical_pointer_written": False,
        "D02_started": False,
        "partial_publication_policy": "REJECT_AND_PRESERVE_NEVER_OVERWRITE_OR_REUSE",
    })
    completion_receipt_raw = canonical(completion_receipt) + b"\n"
    exclusive(completion_dir / COMPLETION_RECEIPT, completion_receipt_raw)

    ordered22: list[tuple[str, str]] = []
    for prefix in ("build-A", "build-B"):
        ordered22.extend((sha(actual["raw"][name]), prefix + "/" + name) for name in MEMBERS)
    ordered22.extend([
        (sha(va_raw), "verification-A/" + VERIFICATION_FILE),
        (sha(vb_raw), "verification-B/" + VERIFICATION_FILE),
        (sha(completion_verification_raw), "completion/" + COMPLETION_VERIFICATION),
        (sha(completion_receipt_raw), "completion/" + COMPLETION_RECEIPT),
    ])
    need(len(ordered22) == 22 and len({name for _, name in ordered22}) == 22,
         "one-global manifest exact ordered22")
    global_manifest_raw = b"".join(
        f"{file_sha256}  {entry_name}\n".encode("ascii")
        for file_sha256, entry_name in ordered22
    )
    exclusive(completion_dir / GLOBAL_MANIFEST, global_manifest_raw)
    final_outer = close_object({
        "schema": SCHEMA + ".final-outer-receipt",
        "status": "PASS_FINAL_C79G_TRUE_GLOBAL_CLOSURE__PUBLIC_UNRESOLVED_ZERO__D02_UNLOCKED_NOT_STARTED",
        "completion_receipt_object_sha256": completion_receipt["object_sha256"],
        "completion_verification_file_sha256": sha(completion_verification_raw),
        "dual_verification_object_sha256": va["object_sha256"],
        "effective_checkpoint_object_sha256": CHECKPOINT_OBJECT_PIN,
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
        "formal_global_closure_credit": 1,
        "D02_unlock": True,
        "D02_gate_credit": 0,
        "D02_task_credit": 0,
        "D02_formal_pending_task_count": PENDING_D02,
        "D02_started": False,
        "precursor_formal_credits_zero": True,
        "canonical_pointer_written": False,
        "only_this_final_outer_may_carry_formal_global_closure_credit": True,
    })
    final_outer_raw = canonical(final_outer) + b"\n"
    exclusive(completion_dir / FINAL_OUTER, final_outer_raw)
    need({path.name for path in completion_dir.iterdir()} == set(COMPLETION_MEMBERS),
         "completion exact4 member universe")
    need((completion_dir / COMPLETION_VERIFICATION).stat().st_mtime_ns <
         (completion_dir / COMPLETION_RECEIPT).stat().st_mtime_ns <
         (completion_dir / GLOBAL_MANIFEST).stat().st_mtime_ns <
         (completion_dir / FINAL_OUTER).stat().st_mtime_ns,
         "completion publication order outer-last")
    candidate_outer_latest = max((candidate_a / OUTER_RECEIPT).stat().st_mtime_ns,
                                 (candidate_b / OUTER_RECEIPT).stat().st_mtime_ns)
    verification_mtimes = [
        (verification_a / VERIFICATION_FILE).stat().st_mtime_ns,
        (verification_b / VERIFICATION_FILE).stat().st_mtime_ns,
    ]
    verification_earliest = min(verification_mtimes)
    verification_latest = max(verification_mtimes)
    completion_verification_mtime = (
        completion_dir / COMPLETION_VERIFICATION).stat().st_mtime_ns
    need(candidate_outer_latest < verification_earliest and
         verification_latest < completion_verification_mtime <
             (completion_dir / COMPLETION_RECEIPT).stat().st_mtime_ns <
             (completion_dir / GLOBAL_MANIFEST).stat().st_mtime_ns <
             (completion_dir / FINAL_OUTER).stat().st_mtime_ns,
         "strict global candidate-before-both-verifications-before-completion chronology")

    replay_targets: list[tuple[Path, bytes]] = []
    replay_targets.extend((candidate_a / name, actual["raw"][name]) for name in MEMBERS)
    replay_targets.extend((candidate_b / name, actual["raw"][name]) for name in MEMBERS)
    replay_targets.extend([
        (verification_a / VERIFICATION_FILE, va_raw),
        (verification_b / VERIFICATION_FILE, vb_raw),
        (completion_dir / COMPLETION_VERIFICATION, completion_verification_raw),
        (completion_dir / COMPLETION_RECEIPT, completion_receipt_raw),
        (completion_dir / GLOBAL_MANIFEST, global_manifest_raw),
        (completion_dir / FINAL_OUTER, final_outer_raw),
    ])
    need(len(replay_targets) == 24, "post-outer terminal replay exact24")
    final_outer_mtime = (completion_dir / FINAL_OUTER).stat().st_mtime_ns
    need(all(path == completion_dir / FINAL_OUTER or path.stat().st_mtime_ns < final_outer_mtime
             for path, _ in replay_targets), "final outer unique latest across exact24")
    for path, expected_raw in replay_targets:
        replay, _ = secure_snapshot(path, 0o444)
        need(replay == expected_raw, "post-outer terminal byte replay:" + str(path))
    os.chmod(completion_dir, 0o555)
    secure_dir(completion_dir, 0o555)
    self_guard.terminal_replay()


def main(argv: list[str] | None = None) -> int:
    cli = argparse.ArgumentParser(description=__doc__)
    sub = cli.add_subparsers(dest="command", required=True)
    verify_cli = sub.add_parser("verify")
    verify_cli.add_argument("--candidate-dir", required=True, type=Path)
    verify_cli.add_argument("--peer-candidate-dir", required=True, type=Path)
    verify_cli.add_argument("--verification-dir", required=True, type=Path)
    final_cli = sub.add_parser("finalize")
    final_cli.add_argument("--candidate-a", required=True, type=Path)
    final_cli.add_argument("--candidate-b", required=True, type=Path)
    final_cli.add_argument("--verification-a", required=True, type=Path)
    final_cli.add_argument("--verification-b", required=True, type=Path)
    final_cli.add_argument("--completion-dir", required=True, type=Path)
    args = cli.parse_args(argv)
    # Mandatory first operation after argument parsing.  The static verifier
    # must not inspect either candidate directory/output or any immutable input
    # before it.
    ensure_c78s_filled()
    self_guard = HeldSelf()
    try:
        if args.command == "verify":
            build_verification(args.candidate_dir, args.peer_candidate_dir,
                               args.verification_dir, self_guard)
        else:
            finalize(args.candidate_a, args.candidate_b, args.verification_a,
                     args.verification_b, args.completion_dir, self_guard)
    finally:
        self_guard.close()
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Reject as exc:
        print("REJECT:", exc, file=sys.stderr)
        raise SystemExit(2)
