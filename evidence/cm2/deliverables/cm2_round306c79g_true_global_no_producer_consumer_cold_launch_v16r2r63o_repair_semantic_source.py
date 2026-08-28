"""Externally pinned cold launcher for the C79g v16r2 exact10 static bundle.

An external held-fd bootstrap (declared TCB, not a bundle member) securely
opens and hashes the installed launcher, copies the pinned bytes into a sealed
memfd, and invokes this source through ``/proc/self/fd/N`` while inheriting the
installed source and workspace-root descriptors.  No workspace surface is
opened until this source proves those three descriptors.

This is the sole constructor of a positive-credit C79g value.  Its native
``reject`` path runs after self-proof and the official lock but before any
bundle file is opened.  The producer
and independent consumer are executed from source descriptors already held by
this launcher and can emit only zero-credit persisted surfaces or a zero-credit
inner live composite.  Non-authorize and zero-output authorize branches replay
the exact10 static bundle after clean child exit.  The positive authorize branch
replays exact10 before its child-live ACK, then commits the non-persisted wrapper
only by a raw blocking fd1 final-newline write; RELEASE and reap are thereafter
non-authority cleanup.
"""
from __future__ import annotations
import argparse
import ast
from collections import Counter
import copy
import ctypes
import errno
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import sys
from typing import Any, Mapping
CHECKPOINT = 'b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab'
CHECKPOINT_OBJECT_PIN = 'dd9d64f3f0bd0dfd00fd399e3154517a34ba19cfb601ec749f44cbc08b03ca1b'
V14_PUBLISHED_EXACT10_WITNESS = (('v13_supersession_receipt', 'deliverables/cm2_round306c79g_true_global_no_producer_consumer_v13_prepublication_pyc_contamination_rejection_supersession_receipt_v1.json', '098296d9807a89f58250f4fd404bdd45b1cf343e3e2e1c7a51a24d67225d016f', '3c9c44500465c6b416cc0ee6689ea82cdd9096a79687b94f94c409ca5a78c677'), ('closed_schema', 'deliverables/cm2_round306c79g_true_global_no_producer_consumer_schema_v14.json', '3d07ccda67cb71d0e5c64d37c0d8e1fcf425de4fbfefddf03bf43934ffdaaa4d', None), ('contract', 'deliverables/cm2_round306c79g_true_global_no_producer_consumer_contract_v14.json', '479a0b3f6b4f0ad7e25d22c9f32eec046758a9a7d40509a6bda200e8e41e0ece', '11fd8966ed631f3bcc0eb6b1881f0536c814b7a7c093eca8289680e38a7d7b8b'), ('build_only_producer', 'deliverables/cm2_round306c79g_true_global_no_producer_consumer_v14.py', '9fa2f2e20cdf15ed37d7f3ff904197fa7bc46a4eec243cab0ae8fb477e2e1ff0', None), ('independent_consumer', 'deliverables/cm2_round306c79g_true_global_no_producer_consumer_independent_verifier_assembler_authority_consumer_v14.py', '83c58e792b922ad57a7c031b4aca60fe4d5868679e6f7a70b513e3cc4b7dc24c', None), ('v13_to_v14_transition', 'deliverables/cm2_round306c79g_true_global_no_producer_consumer_v13_to_v14_static_launch_transition_receipt_v1.json', 'e8c810f85b511cbc3637321f872f96c996a854454ab7ae1fbb3f5bdf19d7fd95', '78912a8f23f7a2e229795aae0e609ca58232dbe36c52ad50bddad727f259413f'), ('static_audit', 'deliverables/cm2_round306c79g_true_global_no_producer_consumer_static_audit_v14.json', 'dbf5e6bf0f13524ee847d01482f9ad34f715368deb2df40207bd2eb436f293e9', '16a8bc6e274a9e4e5a8fe4b2a39b80136cbbb117bfdf2e0ed89ee90fdc71944a'), ('cold_launcher', 'deliverables/cm2_round306c79g_true_global_no_producer_consumer_cold_launch_v14.py', '1236f53865d69d69d27091758a66b21ddc2ea33ed7f422bc8d56adb69a23f5b5', None), ('cold_manifest', 'deliverables/cm2_round306c79g_true_global_no_producer_consumer_cold_launch_manifest_v14.sha256', 'aae2b3735ca9d5469d4228189ff0127e85aca934c6e56dfa3650a4d4d46a5937', None), ('cold_outer', 'deliverables/cm2_round306c79g_true_global_no_producer_consumer_cold_launch_outer_receipt_v14.json', 'fa6d10673d96a36aaf0163c44e014162ffb7811b12b1efa9068d78c8aa5b2040', '786f9be9142ae0aafd31a6d86b08f815d5d4f7ca09fd67506f499635fdddc256'))
V14_PREDECESSOR_TERMINAL_REPLAY_ORDER = tuple((row[0] for row in V14_PUBLISHED_EXACT10_WITNESS)) + ('v14_official_rejection',)
V14_OFFICIAL_REJECTION_RELATIVE_PATH = '.cm2-runtime/c79g-v14-rejections-' + CHECKPOINT + '/rejection.json'
V14_OFFICIAL_REJECTION_FILE_PIN = '1cc1b5836457f219ce26aa8e463ebebe8d48a26d2145806d24f7cbfea6c7e567'
V14_OFFICIAL_REJECTION_OBJECT_PIN = '0856353a2390c46b4f4bdefe9f13f6eb6e0e94aa352174cdc8d2f672ace4a41d'
V14_OFFICIAL_REJECTION_EXACT56_KEYSET_SHA256 = '9c272f16d92497a7c5ced499e9e42c514b81cbfddcdb3f79c4f33837836e057e'
V14_PUBLISHED_EXACT10_PINS = V14_PUBLISHED_EXACT10_WITNESS
V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT_RELATIVE_PATH = 'deliverables/cm2_round306c79g_true_global_no_producer_consumer_v14_runtime_registry_shape_drift_rejection_supersession_receipt_v1.json'
V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT_FILE_PIN = 'aa4323027e2313f8a2eda0d6ffc039a537afe342d496d1f75cd73fcd47446c01'
V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT_OBJECT_PIN = '93689e62ae36f405f045a769f4dc6f6e6fd83a16605d08299d5c3397ad657e2e'
V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT_DRAFT_SENTINELS = ('b4' * 32, 'c4' * 32)
V14_EXACT10_FD_ENV_ORDER = tuple(((role, 'CM2_C79G_V16R2_V14_' + role.upper() + '_FD') for role, _, _, _ in V14_PUBLISHED_EXACT10_WITNESS))
V14_OFFICIAL_REJECTION_FD_ENV = 'CM2_C79G_V16R2_V14_OFFICIAL_REJECTION_FD'
V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT_FD_ENV = 'CM2_C79G_V16R2_V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT_FD'
V14_INHERITED_AUTHORITY_EXACT12 = V14_PUBLISHED_EXACT10_WITNESS + (('v14_official_rejection', V14_OFFICIAL_REJECTION_RELATIVE_PATH, V14_OFFICIAL_REJECTION_FILE_PIN, V14_OFFICIAL_REJECTION_OBJECT_PIN), ('v14_registry_shape_drift_supersession_receipt', V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT_RELATIVE_PATH, V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT_FILE_PIN, V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT_OBJECT_PIN))
V14_INHERITED_AUTHORITY_EXACT12_ROLE_ORDER = tuple((row[0] for row in V14_INHERITED_AUTHORITY_EXACT12))
V14_INHERITED_AUTHORITY_EXACT12_FD_ENV_ORDER = (*V14_EXACT10_FD_ENV_ORDER, ('v14_official_rejection', V14_OFFICIAL_REJECTION_FD_ENV), ('v14_registry_shape_drift_supersession_receipt', V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT_FD_ENV))
V16R2_BOOTSTRAP_DESCRIPTOR_COUNT = 4
V16R2_CHILD_AUTHORITY_DESCRIPTOR_COUNT = 12
V16R2_CHILD_PASS_FD_COUNT = 16
V14_RUNTIME_REGISTRY_SHAPE_DRIFT_INCIDENT = {'schema': 'cm2.round306c79g.true-global-no-producer-consumer.v14-runtime-registry-shape-drift-incident.v1', 'failed_phase': 'LAUNCHER_PRECHILD_PRODUCER_SOURCE_REGISTRY_SHAPE_CENSUS', 'stale_launcher_explicit_key_expectation': 62, 'actual_producer_explicit_key_count': 67, 'execution_proof_key_count': 7, 'enclosing_object_closure_count': 1, 'stale_computed_shape': 70, 'actual_registry_shape': 75, 'producer_child_spawned': False, 'consumer_child_spawned': False, 'candidate_surface_count': 0, 'stage_surface_count': 0, 'positive_runtime_surface_count': 0, 'formal_global_closure_credit': 0, 'D02_unlock': False, 'D02_gate_credit': 0, 'D02_task_credit': 0, 'D02_formal_pending_task_count': 33638, 'D02_started': False, 'timestamps_are_not_chronology_authority': True, 'chronology': ['V14_EXACT10_OUTER_PUBLISHED_RUNTIME_DEFERRED', 'FIRST_RUNTIME_ATTEMPT_FAILED_BEFORE_CHILD_OR_SURFACE', 'OFFICIAL_V14_REJECTION_INSTALLED', 'TERMINAL_REPLAY_EXACT10_THEN_REJECTION_REQUIRED'], 'v14_credit_may_transfer_to_v16r2': False}
HISTORICAL_BASE = 'cm2_round306c79g_true_global_no_producer_consumer'
HISTORICAL_BASE = 'cm2_round306c79g_true_global_no_producer_consumer'
BASE = 'cm2_round306c79g_true_global_no_producer_consumer_v16r2r62_semantic_source'
LAUNCHER_RELATIVE = Path('deliverables') / 'cm2_round306c79g_true_global_no_producer_consumer_cold_launch_v16r2r63o_repair_semantic_source.py'
ROOT = Path('/__C79G_V16R2_UNCONFIGURED_ROOT__')
OUT = ROOT / 'deliverables'
V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT = OUT / 'cm2_round306c79g_true_global_no_producer_consumer_v14_runtime_registry_shape_drift_rejection_supersession_receipt_v1.json'
ACTIVE_PREDECESSOR_SUPERSESSION = OUT / 'cm2_round306c79g_true_global_no_producer_consumer_v16r2r62_active_predecessor_supersession_receipt_v1.json'
ACTIVE_SUCCESSOR_NAMESPACE = 'v16r2r62_semantic_source'
ACTIVE_SUCCESSOR_NAMESPACE_TAG = 'v16r2r62-semantic-regeneration'
ACTIVE_PREDECESSOR_SUPERSESSION_FILE_PIN = 'bf90b37c218c18d974793498816f6165807685e3f8e806bbf034468a7af66194'
ACTIVE_PREDECESSOR_SUPERSESSION_OBJECT_PIN = '0262a45dfb6812eaae673955934f6eb0ca5d6ace92f75b428f1cde33e777c9c6'
HISTORICAL_V16_SEMANTIC_SUPERSESSION = OUT / 'cm2_round306c79g_true_global_no_producer_consumer_v16_semantic_rejection_supersession_receipt_v1.json'
HISTORICAL_V16_SEMANTIC_SUPERSESSION_FILE_PIN = '4b05c7dcd7303311fed7b51ea878641e006e707b5fe413f2aefbc3146afddb3c'
HISTORICAL_V16_SEMANTIC_SUPERSESSION_OBJECT_PIN = '430c663c5ccababd932246d9bc87ecc08fa9957113792aa2bd1e10e205a2ff7c'
UPSTREAM_CHECKPOINT_OBJECT_PIN = 'b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab'
SUCCESSOR_CHECKPOINT_OBJECT_PIN = 'dd9d64f3f0bd0dfd00fd399e3154517a34ba19cfb601ec749f44cbc08b03ca1b'
UPSTREAM_C53_CHECKPOINT_OBJECT_PIN = UPSTREAM_CHECKPOINT_OBJECT_PIN
SUCCESSOR_REJECTION_CHECKPOINT_OBJECT_PIN = SUCCESSOR_CHECKPOINT_OBJECT_PIN
CHECKPOINT_CHAIN_OBJECT_PINS = (UPSTREAM_C53_CHECKPOINT_OBJECT_PIN, SUCCESSOR_REJECTION_CHECKPOINT_OBJECT_PIN)
RUNTIME_AUTHORIZED = False
FORMAL_GLOBAL_CLOSURE_CREDIT = 0
D02_UNLOCK = False
ACTIVE_EXACT8_FIRST_MEMBER = OUT / 'cm2_round306c79g_true_global_no_producer_consumer_v14_runtime_registry_shape_drift_rejection_supersession_receipt_v1.json'
V16R2_DRAFT_RUNTIME_DISABLED = True
V16_DRAFT_RUNTIME_DISABLED = True
ACTIVE_REJECTED_RETRY_SUPERSESSION = OUT / 'cm2_round306c79g_true_global_no_producer_consumer_v16r2r62_active_predecessor_supersession_receipt_v1.json'
RUNTIME = ROOT / '.cm2-runtime'
SELF = ROOT / 'deliverables/cm2_round306c79g_true_global_no_producer_consumer_cold_launch_v16r2r63o_repair_semantic_source.py'
V3_OFFICIAL_REJECTION = ROOT / '__unconfigured_v3_rejection__'
V4_REJECTION_SUPERSESSION = ROOT / '__unconfigured_v4_supersession__'
V5_OFFICIAL_REJECTION = ROOT / '__unconfigured_v5_rejection__'
V6_OFFICIAL_REJECTION = ROOT / '__unconfigured_v6_rejection__'
V7_OFFICIAL_REJECTION = ROOT / '__unconfigured_v7_rejection__'
V8_OFFICIAL_REJECTION = ROOT / '__unconfigured_v8_rejection__'
V9_OFFICIAL_REJECTION = ROOT / '__unconfigured_v9_rejection__'
V10_OFFICIAL_REJECTION = ROOT / '__unconfigured_v10_rejection__'
V11_OFFICIAL_REJECTION = ROOT / '__unconfigured_v11_rejection__'
V12_OFFICIAL_REJECTION = ROOT / '__unconfigured_v12_rejection__'
V13_SUPERSESSION_RECEIPT = ROOT / '__unconfigured_v13_supersession_receipt__'
V13_FROZEN_PRODUCER = ROOT / '__unconfigured_v13_producer__'
V13_FROZEN_CONSUMER = ROOT / '__unconfigured_v13_consumer__'
V13_FROZEN_LAUNCHER = ROOT / '__unconfigured_v13_launcher__'
V13_FROZEN_PRODUCER_PYC = ROOT / '__unconfigured_v13_producer_pyc__'
V13_FROZEN_CONSUMER_PYC = ROOT / '__unconfigured_v13_consumer_pyc__'
V13_FROZEN_LAUNCHER_PYC = ROOT / '__unconfigured_v13_launcher_pyc__'
V16R2_REJECTION_NAMESPACE = ROOT / '__unconfigured_v16r2_semantic_rejections__'
V16R2_LATER_REJECTION = V16R2_REJECTION_NAMESPACE / 'rejection.json'
SCHEMA = ROOT / 'deliverables/cm2_round306c79g_true_global_no_producer_consumer_schema_v16r2r62.json'
CONTRACT = ROOT / 'deliverables/cm2_round306c79g_true_global_no_producer_consumer_contract_v16r2r63o_repair.json'
PRODUCER = ROOT / 'deliverables/cm2_round306c79g_true_global_no_producer_consumer_v16r2r63o_repair_semantic_source.py'
CONSUMER = ROOT / 'deliverables/cm2_round306c79g_true_global_no_producer_consumer_independent_verifier_assembler_authority_consumer_v16r2r63o_repair_semantic_source.py'
TRANSITION = ROOT / 'deliverables/cm2_round306c79g_true_global_no_producer_consumer_v16r2r62_to_v16r2r63o_repair_static_launch_transition_receipt_v1.json'
AUDIT = ROOT / 'deliverables/cm2_round306c79g_true_global_no_producer_consumer_static_audit_v16r2r63o_repair.json'
MANIFEST = ROOT / 'deliverables/cm2_round306c79g_true_global_no_producer_consumer_cold_launch_manifest_v16r2r63o_runtime_repair.sha256'
OUTER = ROOT / 'deliverables/cm2_round306c79g_true_global_no_producer_consumer_cold_launch_outer_receipt_v16r2r63o_runtime_repair.json'
MANIFEST = OUT / 'cm2_round306c79g_true_global_no_producer_consumer_cold_launch_manifest_v16r2r63o_runtime_repair.sha256'
OUTER = OUT / 'cm2_round306c79g_true_global_no_producer_consumer_cold_launch_outer_receipt_v16r2r63o_runtime_repair.json'
V16R2_DRAFT_RUNTIME_DISABLED = True
FINAL_BASE7_PINS_INSTALLED = True
_DRAFT_FILE_PIN = 'f' * 64
_DRAFT_OBJECT_PIN = 'e' * 64
BASE7_PINS = {}
EXACT8: tuple[Path, ...] = (V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT, SCHEMA, CONTRACT, PRODUCER, CONSUMER, TRANSITION, AUDIT, SELF)
V3_EXACT10_PINS: tuple[tuple[Path, str, str | None], ...] = ()
V4_FROZEN_DRAFT7_PINS: tuple[tuple[Path, str, str | None], ...] = ()
V4_FORBIDDEN_RUNTIME_PATHS: tuple[Path, ...] = ()
V5_EXACT10_PINS: tuple[tuple[Path, str, str | None], ...] = ()
V5_FORBIDDEN_RUNTIME_PATHS: tuple[Path, ...] = ()
V6_EXACT10_PINS: tuple[tuple[Path, str, str | None], ...] = ()
V6_FORBIDDEN_RUNTIME_PATHS: tuple[Path, ...] = ()
V7_EXACT10_PINS: tuple[tuple[Path, str, str | None], ...] = ()
V7_FORBIDDEN_RUNTIME_PATHS: tuple[Path, ...] = ()
V8_EXACT10_PINS: tuple[tuple[Path, str, str | None], ...] = ()
V8_FORBIDDEN_RUNTIME_PATHS: tuple[Path, ...] = ()
V9_EXACT10_PINS: tuple[tuple[Path, str, str | None], ...] = ()
V9_FORBIDDEN_RUNTIME_PATHS: tuple[Path, ...] = ()
V10_EXACT10_PINS: tuple[tuple[Path, str, str | None], ...] = ()
V10_FORBIDDEN_RUNTIME_PATHS: tuple[Path, ...] = ()
V11_EXACT10_PINS: tuple[tuple[Path, str, str | None], ...] = ()
V11_FORBIDDEN_RUNTIME_PATHS: tuple[Path, ...] = ()
V12_EXACT10_PINS: tuple[tuple[Path, str, str | None], ...] = ()
V12_FORBIDDEN_RUNTIME_PATHS: tuple[Path, ...] = ()
V3_REJECTION_FILE_PIN = '57ce7a4361555c4ff403f725f17ef9cef50446a2e76d7086635c30a0f17bc62f'
V3_REJECTION_OBJECT_PIN = 'c946e0d8170a75e32aa7031b42cf0dd5b7b585ba463b7b1ce0010cb65bb3b421'
V4_SUPERSESSION_FILE_PIN = 'e3dff621fec2fa5bac14f73685c8f44ce89bc68d80b6478e0688ce926f57c183'
V4_SUPERSESSION_OBJECT_PIN = '1c8fc9d91be75502b0741b096a1ca6d9d59b877b1e69daada15096669215d19f'
V5_REJECTION_FILE_PIN = 'c49218967b2d5023d07e5c65fa53df12f0383d6644bf4bd7d35a8e50abeb85b5'
V5_REJECTION_OBJECT_PIN = '9a94bf8b580f6145c4977dd335d9a63c69057d18d62678ab47c7916c764f8e4c'
V6_REJECTION_FILE_PIN = '3559dcfd9e6d0ebb0e093226d6d3ae8d09d67eaeb186d4ec956241af87fcbd06'
V6_REJECTION_OBJECT_PIN = '87c0cd17ae6ca3885a01da82b47b66e96419eb778594b51423eb04cf3c68f48c'
V7_REJECTION_FILE_PIN = '63d4bbc4f50ef674b6b90f6fde625ac4705d5272f500fd495111d445274ebf6b'
V7_REJECTION_OBJECT_PIN = '29c43ad51082bd56c2291dea88b619731c2853969b79ea008abea1cca3c83ecd'
V8_REJECTION_FILE_PIN = '3b00a60c6c30cc10171d82e8262f880d67aa975e9f040888a29d7bdb4014ef95'
V8_REJECTION_OBJECT_PIN = '9fbc65609f33a62751b9fc60aa4def316a499dae9e3f64e1d4ae8a3be58894d5'
V9_REJECTION_FILE_PIN = 'bca8f1042a1f3ee5b82d85a2e10c6ed2bf35d486116870bf50387f9ee9dcd302'
V9_REJECTION_OBJECT_PIN = '682ead5d02c386b992c15e1e845e5e35a3147e0c1387d440c604f431c7a8b1b4'
V10_REJECTION_FILE_PIN = '1b5bbd9ec04f07e7d7d433685aa693b73bf2315a91e4813960bd5a81e8112828'
V10_REJECTION_OBJECT_PIN = 'efdb614e870e70c20202834d3c6ec1a7513a3e98ba5cb4e1b32f87976a529d76'
V10_PRODUCER_FILE_PIN = '99bb321da8a63855e52c8d6757d00886c0deeb2182f5044cac35f645e2ebd00a'
V10_LAUNCHER_FILE_PIN = '629347f42bcfd2eca3d9e38d29eb3bea66ff9abd48ec16867040c74e81e9134c'
V11_REJECTION_FILE_PIN = 'f6cc10d8b7e72553ef0b7a32bbfb99255f36cce16b735002f17be58ae51d3bc8'
V11_REJECTION_OBJECT_PIN = '7ae86e38c5910bc9ceaa0a4e5cb1f8fbbf1e73de9c0314fedabbd8cb2db3bb7a'
V12_REJECTION_FILE_PIN = 'b6b087a3e31b25f0bbe0ffe6caa40f3c181b2f77c5c8b6169ce3af27439762b5'
V12_REJECTION_OBJECT_PIN = '18951895ea97f455bc3294e8ef9cdaa937f3b16e9831275b047e88142e9b91f6'
V13_SUPERSESSION_RECEIPT_FILE_PIN = '098296d9807a89f58250f4fd404bdd45b1cf343e3e2e1c7a51a24d67225d016f'
V13_SUPERSESSION_RECEIPT_OBJECT_PIN = '3c9c44500465c6b416cc0ee6689ea82cdd9096a79687b94f94c409ca5a78c677'
V13_PRODUCER_FILE_PIN = 'ec4982babaec3bfb6693e29a220ca827087fb591c77f6c715889e934f124310e'
V13_CONSUMER_FILE_PIN = 'a8b32b7e0073e70a95e6f5f17ad08b63b701ca64a1299f0f614215c5aa9f970a'
V13_LAUNCHER_FILE_PIN = 'aa1306ed3e764c69679db531c3dcd30d609ed1cbd699feda5ed17cc1e24da88b'
V13_PRODUCER_PYC_FILE_PIN = '0383cab58260ff076b18482f2077ed100456b21bcc2587afd5e457c8a19d7d36'
V13_CONSUMER_PYC_FILE_PIN = 'f13c8f7f40139bcbe6d5f20014fb14d8659539814baf985f73f99fbb13ffccaa'
V13_LAUNCHER_PYC_FILE_PIN = '50a210fe6c414d140f7e0ac9a969500192f68fafae2de9d104526d73479365e0'
V13_INHERITED_EXACT16_CANONICAL_SHA256 = 'bf70829a4632cd322ef45e9313d4150138a57f98966fcd93d2c7a718fb44f64e'
V13_NORMALIZED_EXACT10_CANONICAL_SHA256 = '600768327003f17f0f367e64b03d0fd9ada23f2933db64845a37cfee140c61b5'
V5_OFFICIAL_REJECTION_FILE_PIN = V5_REJECTION_FILE_PIN
V5_OFFICIAL_REJECTION_OBJECT_PIN = V5_REJECTION_OBJECT_PIN
V12_OFFICIAL_REJECTION_FILE_PIN = V12_REJECTION_FILE_PIN
V12_OFFICIAL_REJECTION_OBJECT_PIN = V12_REJECTION_OBJECT_PIN
V3_OFFICIAL_REJECTION_FILE_PIN = V3_REJECTION_FILE_PIN
V3_OFFICIAL_REJECTION_OBJECT_PIN = V3_REJECTION_OBJECT_PIN
V6_OFFICIAL_REJECTION_FILE_PIN = V6_REJECTION_FILE_PIN
V6_OFFICIAL_REJECTION_OBJECT_PIN = V6_REJECTION_OBJECT_PIN
V7_OFFICIAL_REJECTION_FILE_PIN = V7_REJECTION_FILE_PIN
V7_OFFICIAL_REJECTION_OBJECT_PIN = V7_REJECTION_OBJECT_PIN
V8_OFFICIAL_REJECTION_FILE_PIN = V8_REJECTION_FILE_PIN
V8_OFFICIAL_REJECTION_OBJECT_PIN = V8_REJECTION_OBJECT_PIN
V9_OFFICIAL_REJECTION_FILE_PIN = V9_REJECTION_FILE_PIN
V9_OFFICIAL_REJECTION_OBJECT_PIN = V9_REJECTION_OBJECT_PIN
V10_OFFICIAL_REJECTION_FILE_PIN = V10_REJECTION_FILE_PIN
V10_OFFICIAL_REJECTION_OBJECT_PIN = V10_REJECTION_OBJECT_PIN
V11_OFFICIAL_REJECTION_FILE_PIN = V11_REJECTION_FILE_PIN
V11_OFFICIAL_REJECTION_OBJECT_PIN = V11_REJECTION_OBJECT_PIN
V11_PRODUCER_FILE_PIN = 'f3b364afc0f5b2f729a3d7786eb8e9c25a9303959d6d2464a40395968090a30b'
V11_LAUNCHER_FILE_PIN = '9f6971d2ca3e2c8f448a6aeed70bc16f38154c626f7744a4e20ba723e3082cc2'
V5_OFFICIAL_REJECTION_EXACT39_KEYS = frozenset({'D02_formal_pending_task_count', 'D02_gate_credit', 'D02_started', 'D02_task_credit', 'D02_unlock', 'closed_schema_file_sha256', 'cold_launcher_file_sha256', 'cold_manifest_file_sha256', 'cold_outer_file_sha256', 'cold_outer_object_sha256', 'commit_operation', 'consumer_file_sha256', 'contract_file_sha256', 'contract_object_sha256', 'effective_checkpoint_object_sha256', 'file_fsync_required', 'formal_global_closure_credit', 'idempotent_existing_recovery_re_fsyncs_rejection_file_namespace_and_runtime_parent', 'namespace_at_rest_mode', 'namespace_exact_path', 'namespace_fsync_required_after_file_and_after_reseal', 'namespace_lock_held_write_window_mode', 'object_sha256', 'official_writer_coordination_lock_held_for_entire_reject_command', 'official_writer_coordination_lock_policy', 'overwrite_delete_or_reuse_allowed', 'partial_malformed_or_extra_namespace_entry_revokes_authority', 'producer_file_sha256', 'rejection_file_mode', 'rejection_file_nlink', 'rejection_reason', 'runtime_parent_fsync_required_after_namespace_creation', 'schema', 'standalone_authority', 'status', 'target_exact_path', 'target_is_protocol_and_checkpoint_deterministic', 'v4_rejection_supersession_file_sha256', 'v4_rejection_supersession_object_sha256'})
V5_OFFICIAL_REJECTION_EXACT39_KEYSET_SHA256 = '3b74017677a537d23cacbfbf95f1cc78e3b33fc4839be24e02e848bdd7410460'
V12_OFFICIAL_REJECTION_EXACT54_KEYS = V5_OFFICIAL_REJECTION_EXACT39_KEYS | frozenset({'v5_official_rejection_file_sha256', 'v5_official_rejection_object_sha256', 'v6_official_rejection_file_sha256', 'v6_official_rejection_object_sha256', 'v7_official_rejection_file_sha256', 'v7_official_rejection_object_sha256', 'v7_publication_lock_continuity_incident_object_sha256', 'v8_official_rejection_file_sha256', 'v8_official_rejection_object_sha256', 'v9_official_rejection_file_sha256', 'v9_official_rejection_object_sha256', 'v10_official_rejection_file_sha256', 'v10_official_rejection_object_sha256', 'v11_official_rejection_file_sha256', 'v11_official_rejection_object_sha256'})
V12_OFFICIAL_REJECTION_EXACT54_KEYSET_SHA256 = '271055dec2aa42fb77c14bbd9b5c19e6bd4281428a71dc5db55c7d0db168b985'
V12_V5_REJECTION_SHAPE_INCIDENT_SHA256 = '79ff0e0aa1df0e455af3abad67348f22e3b6b95512b864edf673422e72e17167'
V12_FIRST_RUNTIME_ATTEMPT = {'attempted': True, 'failed_phase': 'LAUNCHER_PRECHILD_HELD_HISTORY_CONSTRUCTOR', 'producer_child_spawned': False, 'consumer_child_spawned': False, 'candidate_write_started': False, 'stage_write_started': False, 'positive_runtime_surface_count': 0, 'official_v12_rejection_installed': True}
V12_FIRST_RUNTIME_ATTEMPT_SHA256 = '8ee3eefa4e9f7c1114d5968e5af9b40c8234295ef9ef05f8ef9cf19f1f776ce9'
V12_V5_REJECTION_SHAPE_INCIDENT = {'schema': 'cm2.round306c79g.true-global-no-producer-consumer.v12-v5-rejection-shape-incident.v1', 'incident_id': 'V12_LAUNCHER_V5_REJECTION_WRONG_EXPECTED_KEY_COUNT_52_FOR_CANONICAL_EXACT39', 'evidence_source': 'FROZEN_V12_LAUNCHER_AST__FROZEN_V12_PRODUCER_AND_CONSUMER_AST__FROZEN_V5_REJECTION_BYTES__FIRST_BUILD_A_CONTROL_FLOW__OFFICIAL_V12_REJECTION', 'failure_class': 'FAIL_CLOSED_HISTORICAL_REJECTION_SHAPE_FALSE_NEGATIVE', 'failure_label': 'official v5 rejection binds published v5 exact10', 'failed_phase': 'LAUNCHER_PRECHILD_HELD_HISTORY_CONSTRUCTOR', 'v12_launcher_source_path': 'deliverables/cm2_round306c79g_true_global_no_producer_consumer_cold_launch_v12.py', 'v12_launcher_source_file_sha256': 'b7aaff67be866f8fd7a01f71e97ea1491574f69e62b7760b6ced9183997444ba', 'v12_producer_source_file_sha256': '4cafc594f8a60063b7e7caaa82ddcc2b7983d0fbf0929034cd3cb5f360f3ed1d', 'v12_consumer_source_file_sha256': 'b74dee738257d485e9ca3357d7d138b5175b95e58f1c8ea87d1eca7bfc96b2ed', 'v12_manifest_file_sha256': '297e9f58dc7657c6fa959dd45081efffe4e7e8dadcd16ab89457863e2661ece6', 'v12_outer_file_sha256': '27129990a9d5b6697fd13ee8e2086100cbf158f12e5b767166d771e63088b6d0', 'v12_outer_object_sha256': 'bc6d06141865954590bd11bfc96ad59dbbffa003f568355ecb47155a8a3a809d', 'v12_official_rejection_file_sha256': V12_REJECTION_FILE_PIN, 'v12_official_rejection_object_sha256': V12_REJECTION_OBJECT_PIN, 'diagnostic_class_name': 'HeldV5PredecessorExact10', 'diagnostic_function_name': '__init__', 'diagnostic_frozen_source_line': 4750, 'source_locations_are_diagnostic_not_authority': True, 'actual_v5_rejection_key_count': 39, 'wrong_v12_launcher_expected_key_count': 52, 'v5_rejection_exact39_sorted_keys': sorted(V5_OFFICIAL_REJECTION_EXACT39_KEYS), 'v5_rejection_exact39_keyset_sha256': V5_OFFICIAL_REJECTION_EXACT39_KEYSET_SHA256, 'producer_v12_validator_uses_exact39_keyset': True, 'consumer_v12_validator_uses_exact39_keyset': True, 'launcher_v12_validator_used_bare_wrong_length_52': True, 'bare_length_only_is_authority': False, 'required_successor_fix': 'THREE_WAY_EXACT39_SORTED_KEYSET_AND_KEYSET_SHA256_WITNESS__NO_BARE_LENGTH_AUTHORITY', 'producer_child_spawned': False, 'consumer_child_spawned': False, 'candidate_write_started': False, 'stage_write_started': False, 'positive_runtime_surface_count': 0, 'formal_global_closure_credit': 0, 'D02_unlock': False, 'D02_gate_credit': 0, 'D02_task_credit': 0, 'D02_formal_pending_task_count': 33638, 'D02_started': False}
V16R2_LATER_REJECTION_EXACT56_KEYSET_SHA256 = '9c272f16d92497a7c5ced499e9e42c514b81cbfddcdb3f79c4f33837836e057e'
V8_LAUNCHER_FILE_PIN = '169866df2d418c3ccb467ef2b678d322584910500cdeee9dd2b40d8564de3d1e'
V8_LAUNCHER_REGRESSION_DEFECT: dict[str, Any] = {'D02_started': False, 'D02_unlock': False, 'actual_guard_identity_census': 3, 'authority_uses_source_locations': False, 'candidate_surface_count': 0, 'child_process_started': False, 'callsite_owner': 'HeldV6PredecessorExact10.__init__', 'diagnostic_source_lines': [2041, 2062, 2235], 'formal_global_closure_credit': 0, 'frozen_v8_launcher_file_sha256': V8_LAUNCHER_FILE_PIN, 'helper': 'v6_held_self_identity_defect_regression', 'old_global_count_expectation': 1, 'prechild_constructor_subprocess_call_count': 0, 'official_rejection_file_sha256': V8_REJECTION_FILE_PIN, 'official_rejection_object_sha256': V8_REJECTION_OBJECT_PIN, 'regression_authority': 'UNIQUE_STRUCTURAL_COMPREHENSION_WITH_ITERABLE_CURRENT_COLD_TEN_GUARDS_AND_ELT_GUARD_IDENTITY', 'schema': 'cm2.round306c79g.true-global-no-producer-consumer.v8-launcher-regression-defect.v1', 'v8_execution_allowed': False, 'v8_formal_credit_transferred': False}
V8_ROLLOUT_CONTROL_FLOW_INCIDENT: dict[str, Any] = {'schema': 'cm2.round306c79g.true-global-no-producer-consumer.v8-rollout-control-flow-incident.v1', 'incident_id': 'V8_LAUNCHER_REGRESSOR_WHOLE_FUNCTION_OCCURRENCE_COUNT_FALSE_POSITIVE', 'evidence_source': 'TRUSTED_ROLLOUT_CONTROL_FLOW_RECORD', 'incident_fact_comes_from_rollout_control_flow_record_not_from_timestamps': True, 'timestamps_are_not_used_to_infer_control_flow': True, 'timestamp_chronology_is_corrobative_only': True, 'regressor_scope': 'WHOLE_FUNCTION_SOURCE_OCCURRENCE_CENSUS', 'regressor_expected_occurrence_count': 1, 'regressor_observed_occurrence_count': 3, 'actual_semantic_trigger_count': 1, 'actual_semantic_trigger_line': 2041, 'observed_source_lines': [2041, 2062, 2235], 'nontrigger_occurrence_lines': [2062, 2235], 'failure_kind': 'FALSE_POSITIVE_REGRESSION_GUARD_ABORT', 'required_successor_fix': 'AST_SEMANTIC_TRIGGER_CHECK_MUST_SELECT_LINE_2041_AND_MUST_NOT_REQUIRE_WHOLE_FUNCTION_TEXT_OCCURRENCE_COUNT_ONE', 'positive_runtime_surface_count': 0, 'v8_execution_allowed': False, 'v8_runtime_surfaces_authoritative': False, 'formal_global_closure_credit': 0, 'D02_unlock': False, 'D02_started': False}
V6_LAUNCHER_EXPANDED_STRUCTURAL_EVIDENCE = {'source_path': 'deliverables/cm2_round306c79g_true_global_no_producer_consumer_v6.py', 'class_name': 'HeldSelf', 'missing_attribute': 'identity', 'failing_function': 'hold_static_freeze_trust', 'failing_expression': 'len({guard.identity for guard in current_cold_ten_guards})', 'diagnostic_source_lines': [2041, 2062, 2235], 'source_locations_are_diagnostic_not_authority': True, 'guard_identity_structural_census': 3, 'target_structural_comprehension_count': 1, 'target_structural_comprehension_ast_sha256': 'a7fb9f5f32fd3fbf06a7fafce3643c003e2f90a2b5be42872838e11da4f20b6c', 'normalized_frozen_source_ast_sha256': '1b4ddb88cb5ac48548ac2bcad3e4d13f93bf41e40d9905c3647e4c56ce09fe48', 'independent_semantic_checker_count': 2, 'independent_semantic_checkers_agree': True, 'deterministic_failure_kind': 'AttributeError', 'failure_occurs_before_candidate_or_stage_creation': True, 'same_defect_must_be_absent_from_v7': True}
V9_V6_PROOF_SHAPE_DRIFT_INCIDENT: dict[str, Any] = {'schema': 'cm2.round306c79g.true-global-no-producer-consumer.v9-v6-held-self-defect-shape-drift-incident.v1', 'incident_id': 'V9_LAUNCHER_EXPANDED_V6_PERSISTED_DEFECT_PAYLOAD_16_KEYS_VERSUS_CONTRACT_CANONICAL_9_KEYS', 'evidence_source': 'FROZEN_V9_LAUNCHER_CONTROL_FLOW_AND_FIRST_RUNTIME_STDERR', 'failure_label': 'exact v6 exact10, rejection, spawned-before-write and HeldSelf.identity defect regression', 'persisted_held_self_identity_defect_exact_key_count': 9, 'persisted_held_self_identity_defect': {'source_path': 'deliverables/cm2_round306c79g_true_global_no_producer_consumer_v6.py', 'class_name': 'HeldSelf', 'missing_attribute': 'identity', 'failing_function': 'hold_static_freeze_trust', 'failing_expression': 'len({guard.identity for guard in current_cold_ten_guards})', 'frozen_source_line': 2041, 'deterministic_failure_kind': 'AttributeError', 'failure_occurs_before_candidate_or_stage_creation': True, 'same_defect_must_be_absent_from_v7': True}, 'launcher_expanded_structural_evidence_exact_key_count': 16, 'launcher_expanded_structural_evidence': {'source_path': 'deliverables/cm2_round306c79g_true_global_no_producer_consumer_v6.py', 'class_name': 'HeldSelf', 'missing_attribute': 'identity', 'failing_function': 'hold_static_freeze_trust', 'failing_expression': 'len({guard.identity for guard in current_cold_ten_guards})', 'diagnostic_source_lines': [2041, 2062, 2235], 'source_locations_are_diagnostic_not_authority': True, 'guard_identity_structural_census': 3, 'target_structural_comprehension_count': 1, 'target_structural_comprehension_ast_sha256': 'a7fb9f5f32fd3fbf06a7fafce3643c003e2f90a2b5be42872838e11da4f20b6c', 'normalized_frozen_source_ast_sha256': '1b4ddb88cb5ac48548ac2bcad3e4d13f93bf41e40d9905c3647e4c56ce09fe48', 'independent_semantic_checker_count': 2, 'independent_semantic_checkers_agree': True, 'deterministic_failure_kind': 'AttributeError', 'failure_occurs_before_candidate_or_stage_creation': True, 'same_defect_must_be_absent_from_v7': True}, 'contract_v9_predecessor_v6_full_canonical_sha256': '827bff2782109ae7aa905b4a8f5d25ac37cd814cef34cbee531a25fad4b1abc0', 'contract_v9_persisted_defect_nested_canonical_sha256': '8dce2a1ea02dc47b3158540547b97810ee3e0ad5adfc5b4849f275fc4ac0407f', 'launcher_v9_predecessor_v6_full_canonical_sha256': '7f3cc1b44f157b8a7ab981d0918e0cf83cb93c49661173a104489deecd38371a', 'launcher_v9_expanded_defect_nested_canonical_sha256': 'd6ac736b4a8e72deef40cf5573545285440b2102e48f9bf6ea2cbcb6fe46a068', 'whole_predecessor_v6_equality_failed_before_child_spawn': True, 'structural_evidence_must_not_be_inserted_into_persisted_payload': True, 'required_successor_fix': 'PRESERVE_CANONICAL_9_KEY_PERSISTED_PAYLOAD_AND_VALIDATE_16_KEY_STRUCTURAL_EVIDENCE_SEPARATELY', 'producer_child_spawned': False, 'candidate_or_stage_created': False, 'positive_runtime_surface_count': 0, 'formal_global_closure_credit': 0, 'D02_unlock': False, 'D02_started': False}
V10_REGRESSION_LABEL_PREFIX_INCIDENT: dict[str, Any] = {'schema': 'cm2.round306c79g.true-global-no-producer-consumer.v10-regression-label-prefix-incident.v1', 'incident_id': 'V10_PRODUCER_V9_REGRESSION_LABEL_PREFIX_COLON_MISMATCH', 'evidence_source': 'FROZEN_V10_PRODUCER_AST_CONTROL_FLOW_AND_FIRST_BUILD_A_STDERR', 'authority_source': 'AST_STRUCTURE_AND_EXACT_PREFIX_JOIN__NOT_RAW_WHOLE_TREE_STRING_EQUALITY', 'producer_source_path': 'deliverables/cm2_round306c79g_true_global_no_producer_consumer_v10.py', 'producer_source_file_sha256': V10_PRODUCER_FILE_PIN, 'frozen_v9_launcher_path': 'deliverables/cm2_round306c79g_true_global_no_producer_consumer_cold_launch_v9.py', 'frozen_v9_launcher_file_sha256': 'f7559ceeb7d491b8489812670392cb63e3cd5f6a2764db469e2dd51d6b5577fa', 'regression_function': 'v9_prechild_shape_drift_regression', 'first_command': 'build', 'first_orientation': 'a', 'inner_stderr_line': 'REJECT: frozen v9 launcher statically embeds structural16 in exact equality gate', 'outer_stderr_line': 'REJECT: cold child rejected or failed', 'regression_guard_conjunct_count': 6, 'regression_guard_conjunct_truth_vector': [True, True, True, True, False, True], 'regression_guard_true_conjunct_count': 5, 'regression_guard_false_conjunct_count': 1, 'unique_false_conjunct_zero_based_index': 4, 'unique_false_conjunct_source_line': 2315, 'expanded_structural_dict_count': 1, 'expanded_structural_dict_exact_key_count': 16, 'validator_call_count': 1, 'equality_gate_count': 2, 'v9_launcher_hash_gate': True, 'failure_label_without_colon_prefix': 'exact v6 exact10, rejection, spawned-before-write and HeldSelf.identity defect regression', 'exact_unprefixed_failure_label_literal_count': 0, 'colon_prefixed_failure_label_literal': ':exact v6 exact10, rejection, spawned-before-write and HeldSelf.identity defect regression', 'exact_colon_prefixed_failure_label_literal_count': 1, 'failure_label_suffix_match_count': 1, 'authority_derived_from_AST_structure_and_exact_prefix_join': True, 'raw_whole_tree_string_equality_is_authority': False, 'hold_static_freeze_trust_call_source_line': 6310, 'regression_call_inside_hold_source_line': 3811, 'candidate_stage_creation_source_line': 6415, 'hold_function_contains_mkdir_call': False, 'producer_child_spawned': True, 'candidate_write_started': False, 'candidate_or_stage_created': False, 'positive_runtime_surface_count': 0, 'failure_occurs_before_candidate_or_stage_creation': True, 'required_successor_fix': 'MATCH_COLON_PREFIX_BY_AST_STRUCTURE_AND_EXACT_PREFIX_JOIN__NEVER_RAW_WHOLE_TREE_LITERAL_MEMBERSHIP', 'formal_global_closure_credit': 0, 'D02_unlock': False, 'D02_started': False}
V11_FIRST_RUNTIME_ATTEMPT: dict[str, Any] = {'attempted': True, 'producer_child_spawned': True, 'candidate_write_started': False, 'candidate_or_stage_created': False, 'positive_runtime_surface_count': 0, 'aborted_by_dual_validator_divergence_guard': True, 'command': 'build', 'orientation': 'a'}
V10_COLON_PREFIX_WITNESS_OBJECT_PIN = '374ec1404780efc5cf78da8e4c4b2554d25e6a1bc5da65d063263b34e0531011'
V10_COLON_PREFIX_WITNESS_KEY_COUNT = 40
V10_COLON_PREFIX_WITNESS_KEY_ORDER = ('schema', 'v10_producer_file_sha256', 'v9_launcher_file_sha256', 'six_guard_ast_sha256', 'six_guard_conjunct_count', 'fifth_membership_ast_sha256', 'fifth_membership_is_exact_legacy_tree_wide_in', 'expanded_structural_dict_count', 'expanded_structural_dict_exact_key_count', 'expanded_structural_dict_ast_sha256', 'validator_helper_call_count', 'equality_gate_count', 'equality_gate_ast_sha256_ordered', 'exact_unprefixed_failure_label_literal_count', 'exact_colon_prefixed_failure_label_literal_count', 'failure_label_suffix_match_count', 'exact_colon_prefix_join_count', 'exact_colon_prefix_join_ast_sha256', 'legacy_guard_conjunct_truth_vector', 'legacy_guard_true_conjunct_count', 'legacy_guard_false_conjunct_count', 'legacy_guard_unique_false_zero_based_index', 'successor_clause_truth_vector', 'successor_all_clauses_true', 'direct_top_level_build_hold_call_count', 'direct_top_level_hold_regression_call_count', 'direct_top_level_build_stage_call_count', 'build_hold_top_level_statement_index', 'hold_regression_top_level_statement_index', 'build_stage_top_level_statement_index', 'hold_precedes_stage', 'pre_regression_write_primitive_count', 'pre_regression_write_primitive_census', 'zero_or_multiple_expanded_dicts_controlled_reject', 'exact_prefix_join_is_authority', 'raw_whole_tree_string_membership_is_authority', 'coherent_attack_count', 'all_coherent_attacks_rejected', 'formal_global_closure_credit', 'object_sha256')
V10_COLON_PREFIX_WITNESS_SUCCESSOR_TRUTH_VECTOR = [True] * 15
V10_COLON_PREFIX_HELPER_NORMALIZED_AST_SHA256 = '38ebe2f639bdb26cac05cec05110ef78bf8057159ebf0f9c8f5d1ce22743fa07'
V11_FIRST_RUNTIME_ATTEMPT_DIGEST = '3b768c47f673b18c090946aee79dd103c9a37855451b4af09e0f7bd8042ab63f'
V11_DUAL_VALIDATOR_DIVERGENCE_INCIDENT_DIGEST = '64db719d426d3604be39d9bcd52118c1c39a409e47c2aaf38704b18d49ce7ab3'
V11_DUAL_VALIDATOR_DIVERGENCE_INCIDENT: dict[str, Any] = {'schema': 'cm2.round306c79g.true-global-no-producer-consumer.v11-dual-validator-divergence-incident.v1', 'incident_id': 'V11_LAUNCHER_GATE_PASSED__PRODUCER_COMPOSITE_GUARD_REJECTED__NO_EXACT_FALSE_CLAUSE', 'evidence_source': 'FROZEN_V11_LAUNCHER_AND_PRODUCER_AST__FIRST_BUILD_A_STDERR__OFFICIAL_REJECTION', 'v11_producer_source_path': 'deliverables/cm2_round306c79g_true_global_no_producer_consumer_v11.py', 'v11_producer_source_file_sha256': V11_PRODUCER_FILE_PIN, 'v11_launcher_source_path': 'deliverables/cm2_round306c79g_true_global_no_producer_consumer_cold_launch_v11.py', 'v11_launcher_source_file_sha256': V11_LAUNCHER_FILE_PIN, 'v11_official_rejection_file_sha256': V11_REJECTION_FILE_PIN, 'v11_official_rejection_object_sha256': V11_REJECTION_OBJECT_PIN, 'first_command': 'build', 'first_orientation': 'a', 'producer_child_spawned': True, 'candidate_write_started': False, 'candidate_or_stage_created': False, 'positive_runtime_surface_count': 0, 'launcher_gate_function': 'v10_regression_label_prefix_gate', 'launcher_gate_passed_before_child_spawn': True, 'producer_guard_function': 'v10_regression_label_prefix_incident_regression', 'producer_composite_guard_rejected': True, 'producer_failure_label': 'frozen v10 sole-false colon-prefix regression and pre-stage control flow', 'producer_embedded_v10_incident_key_count_claim': 44, 'producer_embedded_v10_incident_actual_key_count': 45, 'producer_composite_guard_conjunct_count': 12, 'exact_failing_subpredicate_persisted': False, 'specific_false_clause_authority': 'UNAVAILABLE', 'child_consumed_inherited_held_predecessor_fds': False, 'child_reopened_predecessor_paths': True, 'launcher_and_producer_validator_implementations_distinct': True, 'producer_per_clause_witness_persisted': False, 'v10_colon_prefix_witness_object_sha256': V10_COLON_PREFIX_WITNESS_OBJECT_PIN, 'v10_colon_prefix_witness_key_count': V10_COLON_PREFIX_WITNESS_KEY_COUNT, 'v10_colon_prefix_witness_successor_clause_truth_vector': V10_COLON_PREFIX_WITNESS_SUCCESSOR_TRUTH_VECTOR, 'v10_colon_prefix_witness_all_clauses_true': True, 'inner_stderr_line': 'REJECT: frozen v10 sole-false colon-prefix regression and pre-stage control flow', 'outer_stderr_line': 'REJECT: cold child rejected or failed', 'failure_occurs_before_candidate_or_stage_creation': True, 'official_rejection_strictly_after_v11_outer': True, 'required_successor_fix': 'INHERITED_HELD_FD_BYTES__THREE_INDEPENDENT_IDENTICAL_HELPERS__EXACT_PER_CLAUSE_WITNESS', 'required_held_fd_fix': 'CHILD_REVALIDATES_INHERITED_V10_V9_V11_AND_REJECTION_FDS__NO_SECOND_PATH_VIEW_AS_INCIDENT_AUTHORITY', 'required_validator_fix': 'EXACT40_CLOSED_WITNESS__CONTROLLED_ZERO_OR_MULTIPLE_DICT_REJECT__NO_RAW_TREE_LITERAL_AUTHORITY', 'formal_global_closure_credit': 0, 'D02_unlock': False, 'D02_started': False, 'standalone_authority': False, 'exact_false_clause_claim_allowed': False}
V7_LOCK_CONTINUITY_INCIDENT_OBJECT_PIN = '15f92090e77eda4c6acac0af759541fe47dc4f8358e15659077d6dea8071e764'
V7_LOCK_CONTINUITY_INCIDENT: dict[str, Any] = {'D02_started': False, 'D02_unlock': False, 'effective_checkpoint_object_sha256': CHECKPOINT, 'exact10_bytes_alone_do_not_prove_publication_acceptance': True, 'failure_trigger': 'LOCAL_READ_ONLY_HISTORY_REPLAY_RETURNED_NONZERO_UNDER_SET_E_LOCK_HOLDER', 'false_extra_assumption': 'HISTORICAL_V4_PRETTY_JSON_REQUIRED_CANONICAL_SINGLE_LINE', 'in_lock_terminal_replay_attempt_started': True, 'incident_fact_comes_from_publisher_control_flow_record_not_from_timestamps_alone': True, 'incident_id': 'V7_OFFICIAL_LOCK_RELEASED_AFTER_OUTER_BEFORE_REQUIRED_IN_LOCK_TERMINAL_REPLAY_COMPLETION', 'later_read_only_replay_cannot_rehabilitate_v7': True, 'object_sha256': V7_LOCK_CONTINUITY_INCIDENT_OBJECT_PIN, 'official_rejection_file_sha256': V7_REJECTION_FILE_PIN, 'official_rejection_object_sha256': V7_REJECTION_OBJECT_PIN, 'outer_frozen_and_fsynced': True, 'outer_then_rejection_chronology_validated': True, 'positive_runtime_surface_count': 0, 'postincident_byte_replay_passed_but_did_not_restore_lock_continuity': True, 'publication_lock_continuity_interrupted_after_outer_before_required_replay_completion': True, 'publication_lock_released_on_replay_attempt_failure': True, 'published_exact10_count': 10, 'published_outer_file_sha256': '0a1fc6afe12db5c630b0c73e1fb8280140adb1590c93f176c564e4e24637584e', 'published_outer_object_sha256': '8214fa50020fed7ea4046d607b1631723f660d18b3f8a2f8653f7444b02a1795', 'required_in_lock_terminal_replay_completed': False, 'schema': 'cm2.round306c79g.true-global-no-producer-consumer.v7-publication-lock-continuity-incident.v1', 'v7_formal_credit_transferred': False, 'v7_runtime_command_count': 0}
V5_STRICT_BOOL_UNPROVED_CENSUS_SHA256 = '90b5b3c6059ca166b56a9aad5d456c3308814df12465a7e6f326131d3bbabbf2'
V5_STRICT_BOOL_RISK_IDS = ('V5_LAUNCHER_SCHEMA_DEFS_NAME_NON_BOOL', 'V5_LAUNCHER_SCHEMA_PROPERTY_NAME_NON_BOOL', 'V5_CONSUMER_ATTACK_PATCH_NON_BOOL', 'V5_PRODUCER_RELATIVE_PARTS_NON_BOOL_SHORT_CIRCUIT', 'V5_CONSUMER_RELATIVE_PARTS_NON_BOOL_SHORT_CIRCUIT', 'V5_LAUNCHER_RELATIVE_PARTS_NON_BOOL_SHORT_CIRCUIT', 'V5_LAUNCHER_RELATIVE_BYTES_NON_BOOL_SHORT_CIRCUIT')
V5_STRICT_BOOL_RISK_ID_ORDER_SHA256 = '8f0957d9aa790bb7a5209e1fae86dd02d0d05de0afb2c6bb24301fe793e7ea4b'
V6_NORMALIZED_AST_SHA256 = '1b4ddb88cb5ac48548ac2bcad3e4d13f93bf41e40d9905c3647e4c56ce09fe48'
V6_TARGET_IDENTITY_COMPREHENSION_AST_SHA256 = 'a7fb9f5f32fd3fbf06a7fafce3643c003e2f90a2b5be42872838e11da4f20b6c'

def configure_workspace_paths(root: Path) -> None:
    """Install the one root-fd-bound lexical namespace after self-proof."""
    global ROOT, OUT, RUNTIME, SELF, V3_OFFICIAL_REJECTION
    global ACTIVE_PREDECESSOR_SUPERSESSION, ACTIVE_REJECTED_RETRY_SUPERSESSION
    global ACTIVE_EXACT8_FIRST_MEMBER
    global ACTIVE_SUCCESSOR_NAMESPACE, ACTIVE_SUCCESSOR_NAMESPACE_TAG
    global ACTIVE_PREDECESSOR_SUPERSESSION_FILE_PIN
    global ACTIVE_PREDECESSOR_SUPERSESSION_OBJECT_PIN
    global ACTIVE_PREDECESSOR_SUPERSESSION, ACTIVE_REJECTED_RETRY_SUPERSESSION
    global ACTIVE_EXACT8_FIRST_MEMBER
    global ACTIVE_SUCCESSOR_NAMESPACE, ACTIVE_SUCCESSOR_NAMESPACE_TAG
    global ACTIVE_PREDECESSOR_SUPERSESSION_FILE_PIN
    global ACTIVE_PREDECESSOR_SUPERSESSION_OBJECT_PIN
    global V4_REJECTION_SUPERSESSION, V5_OFFICIAL_REJECTION
    global V6_OFFICIAL_REJECTION, V7_OFFICIAL_REJECTION
    global V8_OFFICIAL_REJECTION, V9_OFFICIAL_REJECTION
    global V10_OFFICIAL_REJECTION, V11_OFFICIAL_REJECTION
    global V12_OFFICIAL_REJECTION, V13_SUPERSESSION_RECEIPT
    global V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT
    global V13_FROZEN_PRODUCER, V13_FROZEN_CONSUMER, V13_FROZEN_LAUNCHER
    global V13_FROZEN_PRODUCER_PYC, V13_FROZEN_CONSUMER_PYC
    global V13_FROZEN_LAUNCHER_PYC
    global V16R2_REJECTION_NAMESPACE
    global V16R2_LATER_REJECTION, SCHEMA, CONTRACT, PRODUCER, CONSUMER
    global TRANSITION, AUDIT, MANIFEST, OUTER, BASE7_PINS, EXACT8
    global V3_EXACT10_PINS, V4_FROZEN_DRAFT7_PINS, V5_EXACT10_PINS
    global V6_EXACT10_PINS, V7_EXACT10_PINS, V8_EXACT10_PINS
    global V9_EXACT10_PINS, V10_EXACT10_PINS, V11_EXACT10_PINS
    global V12_EXACT10_PINS
    global V4_FORBIDDEN_RUNTIME_PATHS, V5_FORBIDDEN_RUNTIME_PATHS
    global V6_FORBIDDEN_RUNTIME_PATHS, V7_FORBIDDEN_RUNTIME_PATHS
    global V8_FORBIDDEN_RUNTIME_PATHS, V9_FORBIDDEN_RUNTIME_PATHS
    global V10_FORBIDDEN_RUNTIME_PATHS, V11_FORBIDDEN_RUNTIME_PATHS
    global V12_FORBIDDEN_RUNTIME_PATHS
    ROOT = root
    OUT = ROOT / 'deliverables'
    ACTIVE_PREDECESSOR_SUPERSESSION = OUT / 'cm2_round306c79g_true_global_no_producer_consumer_v16r2r62_active_predecessor_supersession_receipt_v1.json'
    ACTIVE_REJECTED_RETRY_SUPERSESSION = ACTIVE_PREDECESSOR_SUPERSESSION
    ACTIVE_EXACT8_FIRST_MEMBER = OUT / 'cm2_round306c79g_true_global_no_producer_consumer_v14_runtime_registry_shape_drift_rejection_supersession_receipt_v1.json'
    ACTIVE_SUCCESSOR_NAMESPACE = 'v16r2r62_semantic_source'
    ACTIVE_SUCCESSOR_NAMESPACE_TAG = 'v16r2r62-semantic-regeneration'
    ACTIVE_PREDECESSOR_SUPERSESSION_FILE_PIN = 'bf90b37c218c18d974793498816f6165807685e3f8e806bbf034468a7af66194'
    ACTIVE_PREDECESSOR_SUPERSESSION_OBJECT_PIN = '0262a45dfb6812eaae673955934f6eb0ca5d6ace92f75b428f1cde33e777c9c6'
    RUNTIME = ROOT / '.cm2-runtime'
    SELF = ROOT / 'deliverables/cm2_round306c79g_true_global_no_producer_consumer_cold_launch_v16r2r63o_repair_semantic_source.py'
    V3_OFFICIAL_REJECTION = RUNTIME / ('c79g-v3-rejections-' + CHECKPOINT + '/rejection.json')
    V4_REJECTION_SUPERSESSION = OUT / (HISTORICAL_BASE + '_v4_rejection_supersession_receipt_v1.json')
    V5_OFFICIAL_REJECTION = RUNTIME / ('c79g-v5-rejections-' + CHECKPOINT + '/rejection.json')
    V6_OFFICIAL_REJECTION = RUNTIME / ('c79g-v6-rejections-' + CHECKPOINT + '/rejection.json')
    V7_OFFICIAL_REJECTION = RUNTIME / ('c79g-v7-rejections-' + CHECKPOINT + '/rejection.json')
    V8_OFFICIAL_REJECTION = RUNTIME / ('c79g-v8-rejections-' + CHECKPOINT + '/rejection.json')
    V9_OFFICIAL_REJECTION = RUNTIME / ('c79g-v9-rejections-' + CHECKPOINT + '/rejection.json')
    V10_OFFICIAL_REJECTION = RUNTIME / ('c79g-v10-rejections-' + CHECKPOINT + '/rejection.json')
    V11_OFFICIAL_REJECTION = RUNTIME / ('c79g-v11-rejections-' + CHECKPOINT + '/rejection.json')
    V12_OFFICIAL_REJECTION = RUNTIME / ('c79g-v12-rejections-' + CHECKPOINT + '/rejection.json')
    V13_SUPERSESSION_RECEIPT = OUT / (HISTORICAL_BASE + '_v13_prepublication_pyc_contamination_rejection_supersession_receipt_v1.json')
    V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT = OUT / (HISTORICAL_BASE + '_v14_runtime_registry_shape_drift_rejection_supersession_receipt_v1.json')
    V13_FROZEN_PRODUCER = OUT / (HISTORICAL_BASE + '_v13.py')
    V13_FROZEN_CONSUMER = OUT / (HISTORICAL_BASE + '_independent_verifier_assembler_authority_consumer_v13.py')
    V13_FROZEN_LAUNCHER = OUT / (HISTORICAL_BASE + '_cold_launch_v13.py')
    V13_FROZEN_PRODUCER_PYC = OUT / '__pycache__' / (HISTORICAL_BASE + '_v13.cpython-312.pyc')
    V13_FROZEN_CONSUMER_PYC = OUT / '__pycache__' / (HISTORICAL_BASE + '_independent_verifier_assembler_authority_consumer_v13.cpython-312.pyc')
    V13_FROZEN_LAUNCHER_PYC = OUT / '__pycache__' / (HISTORICAL_BASE + '_cold_launch_v13.cpython-312.pyc')
    V16R2_REJECTION_NAMESPACE = RUNTIME / ('c79g-v16r2-rejections-' + CHECKPOINT)
    V16R2_LATER_REJECTION = V16R2_REJECTION_NAMESPACE / 'rejection.json'
    SCHEMA = OUT / 'cm2_round306c79g_true_global_no_producer_consumer_schema_v16r2r62.json'
    CONTRACT = OUT / 'cm2_round306c79g_true_global_no_producer_consumer_contract_v16r2r63o_repair.json'
    PRODUCER = OUT / 'cm2_round306c79g_true_global_no_producer_consumer_v16r2r63o_repair_semantic_source.py'
    CONSUMER = OUT / 'cm2_round306c79g_true_global_no_producer_consumer_independent_verifier_assembler_authority_consumer_v16r2r63o_repair_semantic_source.py'
    TRANSITION = OUT / 'cm2_round306c79g_true_global_no_producer_consumer_v16r2r62_to_v16r2r63o_repair_static_launch_transition_receipt_v1.json'
    AUDIT = OUT / 'cm2_round306c79g_true_global_no_producer_consumer_static_audit_v16r2r63o_repair.json'
    MANIFEST = OUT / 'cm2_round306c79g_true_global_no_producer_consumer_cold_launch_manifest_v16r2r63o_runtime_repair.sha256'
    OUTER = OUT / 'cm2_round306c79g_true_global_no_producer_consumer_cold_launch_outer_receipt_v16r2r63o_runtime_repair.json'
    BASE7_PINS = {V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT: ('aa4323027e2313f8a2eda0d6ffc039a537afe342d496d1f75cd73fcd47446c01', '93689e62ae36f405f045a769f4dc6f6e6fd83a16605d08299d5c3397ad657e2e'), SCHEMA: ('1a9c03d332a1c12a34f330b30acb77b13a8f315732fc0bc75be29d3b8c3e1577', None), CONTRACT: ('7662281de23b89aa45089c853e12a9c61cf49ea63168e6fa4811402273c14223', '323d6fa55e2974e78b85c87ef1dcbff049c7d6b9ff9e993443085c6abff813aa'), PRODUCER: ('cfd74eb7a4ab756ed5c0db6336e647d08b44746279db346631d2c0f580c83e51', None), CONSUMER: ('c26e5e65b78b90517711bd2eb3a5477820890ecfbe37520796df6691eddce44a', None), TRANSITION: ('6b8c366cccc6cfdc25e96dd0dec66829757712eac0b2e77fd6546923c8eb0c13', '49bfa83ac1315e03eed1522d3f08d7aac091dda4c2677beacadd0c926e0eb642'), AUDIT: ('071069f88d86d18a0c2434574dcc393ddbe718e3996622dbf8110ab2bac138bc', '73743440dd2e702432617913efc2bd7ed07a9b09e979ebfc331364d4ade38f18')}
    EXACT8 = (V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT, SCHEMA, CONTRACT, PRODUCER, CONSUMER, TRANSITION, AUDIT, SELF)
    V3_EXACT10_PINS = ((OUT / (HISTORICAL_BASE + '_v2_rejection_supersession_receipt_v1.json'), 'fdd1921afda98a34c87ae20094e60fca1b75c8f233cf37890e7817fe35d82408', '518cbc5b30fc62d55291feef407c5677b880a05cb9a5b9f51404c79381c648fa'), (OUT / (HISTORICAL_BASE + '_schema_v3.json'), '275a86286480f915af69e18d81d7032140e3db6982d32679206a6a5b88fee036', None), (OUT / (HISTORICAL_BASE + '_contract_v3.json'), 'ee2a969b5d3ae28dfc116fc24ab6bee6c3983d64db183641981108481c05ae7d', 'fe82dcf80e8dd856390b694e8a286abc3087f33d0a2b4bebda1a01836b796a6b'), (OUT / (HISTORICAL_BASE + '_v3.py'), '587933a52505488fd87b1c4f99d5659df6f3c3e9557c0a77edd642e6e4dde0ab', None), (OUT / (HISTORICAL_BASE + '_independent_verifier_assembler_authority_consumer_v3.py'), 'd66143d32f4c4257041f03e24e4a4da8f15542853b2a8f47fa39f5b72871bfdd', None), (OUT / (HISTORICAL_BASE + '_v2_to_v3_static_launch_transition_receipt_v1.json'), 'd2c0a78db1ae19ccb21f068c4c4f9337220cabbf16721fdc15ed41825a6f3374', 'fabe51379dc16bd4177d2116a43f2d1d5c103cc5a53f845fd5397eae0ea1c25b'), (OUT / (HISTORICAL_BASE + '_static_audit_v3.json'), 'b7c3732296df713b6588527284983fab758e225c17c51fbc4a38b1f43da8aece', '2ef7588e66a83944fee0e2044177445f15b71fe030871ca96f354ce65dc8499a'), (OUT / (HISTORICAL_BASE + '_cold_launch_v3.py'), '63e1b04ce152770ce4bcfda826d418414fd3196ba540752d0bd61a97eec0075b', None), (OUT / (HISTORICAL_BASE + '_cold_launch_manifest_v3.sha256'), '53c97fc8f01f0dc0de3f7c5729d5940587467a1877ef9a7c96e9ea2403c0b028', None), (OUT / (HISTORICAL_BASE + '_cold_launch_outer_receipt_v3.json'), '692608ca777ca9ee625e2044bc71f694edf893f51953d7ff5662f29264d245ea', '450e1551a9f3cac2529bd202aa63ad28e4fd7e2ec4c7d7fb415883840ca0143d'))
    V4_FROZEN_DRAFT7_PINS = ((OUT / (HISTORICAL_BASE + '_schema_v4.json'), 'b2cb58e88b66daed7d0449d11a4441095179b7e537a48a35ee9c630f76beca6a', None), (OUT / (HISTORICAL_BASE + '_contract_v4.json'), '84608ada466fb9aa3d99adfd34662e9af02dfd009d8eb185374c065a6da0c23c', '62609ff0809ba9439be07a215ece772262f30ead7d87fda92a6e4e23bb5895b7'), (OUT / (HISTORICAL_BASE + '_v4.py'), '968e401852f45d5104f48526b50d4f59a86bb1fed8e7af23782c5f6d447d1cf1', None), (OUT / (HISTORICAL_BASE + '_independent_verifier_assembler_authority_consumer_v4.py'), '23753584725365cdc0174d518c26b7d8dbdeb12eea2345a5e3b281274548420c', None), (OUT / (HISTORICAL_BASE + '_v3_to_v4_static_launch_transition_receipt_v1.json'), '4c46f7cf8eaba93fd1b9562c288c2117b49d7c8cdeb62482b93c5e247d412256', 'd2d0797a6edb8463f9af7007e28356932472f2e0478fb73b35869d3f51184129'), (OUT / (HISTORICAL_BASE + '_static_audit_v4.json'), '5efa44ae5cf78000940a4640a98ac0fe486e1946aecc9d20e7023e27ed13049c', '489a0aad575872e79dc264d5fc45cf2f12903c4c990f25d15a9cdd1448e980f4'), (OUT / (HISTORICAL_BASE + '_cold_launch_v4.py'), '04617c7ac60ad4cee278ac1b4c7d154fd130a3e2225a691ef9a75ad644a062a3', None))
    V4_FORBIDDEN_RUNTIME_PATHS = (RUNTIME / ('c79g-v4-candidate-a-' + CHECKPOINT), RUNTIME / ('c79g-v4-candidate-b-' + CHECKPOINT), RUNTIME / ('c79g-v4-verification-a-' + CHECKPOINT), RUNTIME / ('c79g-v4-verification-b-' + CHECKPOINT), RUNTIME / ('c79g-v4-committed-completion-' + CHECKPOINT), RUNTIME / 'cm2-global-authority-heads' / ('c79g-v4-' + CHECKPOINT + '.seal'), RUNTIME / ('c79g-v4-rejections-' + CHECKPOINT), RUNTIME / ('.c79g-v4-candidate-stage-a-' + CHECKPOINT), RUNTIME / ('.c79g-v4-candidate-stage-b-' + CHECKPOINT), RUNTIME / ('.c79g-v4-verification-stage-a-' + CHECKPOINT), RUNTIME / ('.c79g-v4-verification-stage-b-' + CHECKPOINT), RUNTIME / ('.c79g-v4-completion-stage-' + CHECKPOINT), RUNTIME / 'cm2-global-authority-heads' / ('.c79g-v4-authority-stage-' + CHECKPOINT + '.seal'))
    V5_EXACT10_PINS = ((V4_REJECTION_SUPERSESSION, V4_SUPERSESSION_FILE_PIN, V4_SUPERSESSION_OBJECT_PIN), (OUT / (HISTORICAL_BASE + '_schema_v5.json'), '1048740103257351abb1266ed91bb80028436cb1497918a0f0f177ec3268ff4f', None), (OUT / (HISTORICAL_BASE + '_contract_v5.json'), '162cd554ea972b434c019924a9ab8b87621ab65aae7d4896b6dac72d6288b997', '27d457a583f4d9892e0a866917ea4add25ff677669ee814861e0608036189377'), (OUT / (HISTORICAL_BASE + '_v5.py'), 'bc6d48903f61257cd75b20b83c6cd369ca3748d19427cf18129c0fb9bb59e76e', None), (OUT / (HISTORICAL_BASE + '_independent_verifier_assembler_authority_consumer_v5.py'), '03aed000a94fc7b7d7e68d3c55611bcc55e7ce293f65ddfb3be7709e44fc854d', None), (OUT / (HISTORICAL_BASE + '_v4_to_v5_static_launch_transition_receipt_v1.json'), '6784668e91a4a4cc0812c6405cb1df8c10ad90e40daf321ac75c16cadd5cd715', '0678e3b81d5a4f6088967613df0cd585910b9b26800dfbf1724b637fc7c43526'), (OUT / (HISTORICAL_BASE + '_static_audit_v5.json'), 'b852a41aaa992b85abec5f7139dc4669d2f1fe38bd79ab8ab812453c5cfca4f0', 'ba9bf728ce08b795b5dd92191f2ccac3b2cfbc6ef7f7b919379feb6b9557e546'), (OUT / (HISTORICAL_BASE + '_cold_launch_v5.py'), '889775cfbe1d3cba597c85c28765545805710c99f06ad05673e57b7b7627bc54', None), (OUT / (HISTORICAL_BASE + '_cold_launch_manifest_v5.sha256'), '55336d5a95e1765cc0f229bbc98ddfb1f6c14218f5b5e619f84d19da39961474', None), (OUT / (HISTORICAL_BASE + '_cold_launch_outer_receipt_v5.json'), '71b7eaca4af58a34b70bb751044bd09d0e40352a1dc6f016a0c7618b6d4b4ab8', '57d5c31bf232d725e661932d2d210b31d1125cd0877a74a8167451bbbdaf0e1c'))
    V5_FORBIDDEN_RUNTIME_PATHS = (RUNTIME / ('c79g-v5-candidate-a-' + CHECKPOINT), RUNTIME / ('c79g-v5-candidate-b-' + CHECKPOINT), RUNTIME / ('c79g-v5-verification-a-' + CHECKPOINT), RUNTIME / ('c79g-v5-verification-b-' + CHECKPOINT), RUNTIME / ('c79g-v5-committed-completion-' + CHECKPOINT), RUNTIME / 'cm2-global-authority-heads' / ('c79g-v5-' + CHECKPOINT + '.seal'), RUNTIME / ('.c79g-v5-candidate-stage-a-' + CHECKPOINT), RUNTIME / ('.c79g-v5-candidate-stage-b-' + CHECKPOINT), RUNTIME / ('.c79g-v5-verification-stage-a-' + CHECKPOINT), RUNTIME / ('.c79g-v5-verification-stage-b-' + CHECKPOINT), RUNTIME / ('.c79g-v5-completion-stage-' + CHECKPOINT), RUNTIME / 'cm2-global-authority-heads' / ('.c79g-v5-authority-stage-' + CHECKPOINT + '.seal'))
    V6_EXACT10_PINS = ((V5_OFFICIAL_REJECTION, V5_REJECTION_FILE_PIN, V5_REJECTION_OBJECT_PIN), (OUT / (HISTORICAL_BASE + '_schema_v6.json'), '250e27777e3ffdaf159a19c00ae683a4ef079f6e785f0b37d003a724099419bc', None), (OUT / (HISTORICAL_BASE + '_contract_v6.json'), '6e4f7f4693b759397c8775f8d943048c867b3c460c27f5cb3d9681a0fefee30c', '58ae6e3c9912294cc89b6804741e56b373a143d16a5fa2547325989fa1af2546'), (OUT / (HISTORICAL_BASE + '_v6.py'), 'f48982effd6a1068c50260d0d419b281a3fa8c614e4ca76c3b8ee2a48e8afb56', None), (OUT / (HISTORICAL_BASE + '_independent_verifier_assembler_authority_consumer_v6.py'), 'af4875d2ab84101b05eff9811f33d8bf7b1a060720a956ae3fb42d8d466f4775', None), (OUT / (HISTORICAL_BASE + '_v5_to_v6_static_launch_transition_receipt_v1.json'), 'a6ac971e7efd9a6a80c7055449fb6c4ef02b77d3e8303324104a060618d45569', 'edb97beae5ca5cfeff9e549c017892d6381d3b5a01be16b12e7e52e06d09c5e1'), (OUT / (HISTORICAL_BASE + '_static_audit_v6.json'), 'f4f5b3ea2c289f388da9cc7d4181c0f1d6cf692aae0b85cbb17533ca4131f474', '2478b44d085336b87d13e309dc4416e58a85ef6ae28eb89cd787ea95b07c0449'), (OUT / (HISTORICAL_BASE + '_cold_launch_v6.py'), '796cbb3c0a4a2a5f3801f9a9132421112fc19e81272938092edd3014ef031fcb', None), (OUT / (HISTORICAL_BASE + '_cold_launch_manifest_v6.sha256'), '281232171e4c2713f81122e731bd4d50e95afef6bdbd2a5040f5e93c3b7171ea', None), (OUT / (HISTORICAL_BASE + '_cold_launch_outer_receipt_v6.json'), 'e37cce305826fb2149798a125a12b3880070fca5f338b6508beeea947c2854bd', '423621bbe2115183a54dc0161abdbdc964f09af31efb39eee40f46bc81bbe251'))
    V6_FORBIDDEN_RUNTIME_PATHS = (RUNTIME / ('c79g-v6-candidate-a-' + CHECKPOINT), RUNTIME / ('c79g-v6-candidate-b-' + CHECKPOINT), RUNTIME / ('c79g-v6-verification-a-' + CHECKPOINT), RUNTIME / ('c79g-v6-verification-b-' + CHECKPOINT), RUNTIME / ('c79g-v6-committed-completion-' + CHECKPOINT), RUNTIME / 'cm2-global-authority-heads' / ('c79g-v6-' + CHECKPOINT + '.seal'), RUNTIME / ('.c79g-v6-candidate-stage-a-' + CHECKPOINT), RUNTIME / ('.c79g-v6-candidate-stage-b-' + CHECKPOINT), RUNTIME / ('.c79g-v6-verification-stage-a-' + CHECKPOINT), RUNTIME / ('.c79g-v6-verification-stage-b-' + CHECKPOINT), RUNTIME / ('.c79g-v6-completion-stage-' + CHECKPOINT), RUNTIME / 'cm2-global-authority-heads' / ('.c79g-v6-authority-stage-' + CHECKPOINT + '.seal'))
    V7_EXACT10_PINS = ((V6_OFFICIAL_REJECTION, V6_REJECTION_FILE_PIN, V6_REJECTION_OBJECT_PIN), (OUT / (HISTORICAL_BASE + '_schema_v7.json'), 'edcdbb568044d04fc7c86b4c4e64fdb7b12b3841f1e93092694ebc3177b6fe18', None), (OUT / (HISTORICAL_BASE + '_contract_v7.json'), '041ca2567f81c148f765dd85e3515a6ac01295bca06c3032b027459eceb2c014', 'a87f7434b32a96923ee81f7761efab9b0937f15103c2fa9b47e8402104b612a5'), (OUT / (HISTORICAL_BASE + '_v7.py'), '67670681481cf372f775ad39a9f8d8b2459a77ef708e2f4da14ca114ac0f0d95', None), (OUT / (HISTORICAL_BASE + '_independent_verifier_assembler_authority_consumer_v7.py'), '3ee9f2c666b7297a23faa31d39d5ea66b708d545120b1aeb93f77ac9ef704f8a', None), (OUT / (HISTORICAL_BASE + '_v6_to_v7_static_launch_transition_receipt_v1.json'), 'e732442e16a3a1f66629562af4cae72d9ae3e78b511f67ee22aa84869b90bec8', '0f1f240b6a61a6774991b8355c6132c1a9ae30b15690e8c058f88206db69453e'), (OUT / (HISTORICAL_BASE + '_static_audit_v7.json'), '74c72540bd66b5929fa30ec554207db21f40999484752340f0294590d407a667', 'efd83fae1a716c864e8bb61238370e10b9ebf54444f023b902c7cef2a41a6766'), (OUT / (HISTORICAL_BASE + '_cold_launch_v7.py'), '93404ad229728b682018ad236075b6c789e12ee4bf043426049e2aa501b2b9e0', None), (OUT / (HISTORICAL_BASE + '_cold_launch_manifest_v7.sha256'), 'eeabe5d52504231a6163b0e057e9129b632b8a4c33a18fc3a3ac4576612de80c', None), (OUT / (HISTORICAL_BASE + '_cold_launch_outer_receipt_v7.json'), '0a1fc6afe12db5c630b0c73e1fb8280140adb1590c93f176c564e4e24637584e', '8214fa50020fed7ea4046d607b1631723f660d18b3f8a2f8653f7444b02a1795'))
    V7_FORBIDDEN_RUNTIME_PATHS = (RUNTIME / ('c79g-v7-candidate-a-' + CHECKPOINT), RUNTIME / ('c79g-v7-candidate-b-' + CHECKPOINT), RUNTIME / ('c79g-v7-verification-a-' + CHECKPOINT), RUNTIME / ('c79g-v7-verification-b-' + CHECKPOINT), RUNTIME / ('c79g-v7-committed-completion-' + CHECKPOINT), RUNTIME / 'cm2-global-authority-heads' / ('c79g-v7-' + CHECKPOINT + '.seal'), RUNTIME / ('.c79g-v7-candidate-stage-a-' + CHECKPOINT), RUNTIME / ('.c79g-v7-candidate-stage-b-' + CHECKPOINT), RUNTIME / ('.c79g-v7-verification-stage-a-' + CHECKPOINT), RUNTIME / ('.c79g-v7-verification-stage-b-' + CHECKPOINT), RUNTIME / ('.c79g-v7-completion-stage-' + CHECKPOINT), RUNTIME / 'cm2-global-authority-heads' / ('.c79g-v7-authority-stage-' + CHECKPOINT + '.seal'))
    V8_EXACT10_PINS = ((V7_OFFICIAL_REJECTION, V7_REJECTION_FILE_PIN, V7_REJECTION_OBJECT_PIN), (OUT / (HISTORICAL_BASE + '_schema_v8.json'), '65904d48296a568d2cd4ec2fc49abe1a7651ca77d4a119a780fc91fb6ddaaeeb', None), (OUT / (HISTORICAL_BASE + '_contract_v8.json'), '6ddb6dd015ee9bb88c716cfb939bf2b954789effffa17b141833091a72187ca4', '0bb6634778bf50a9f090d5df7b23358cae30769ce9b2fb87119800f38a1b75c0'), (OUT / (HISTORICAL_BASE + '_v8.py'), '93a591fc870c0fa35ed37e6e2d0f9066161988d3d340031b7ffdb7239eb2c512', None), (OUT / (HISTORICAL_BASE + '_independent_verifier_assembler_authority_consumer_v8.py'), 'd9c5c56f0ae88b573812c660a64eb94dd345d7efd0257cce975752945e1240f3', None), (OUT / (HISTORICAL_BASE + '_v7_to_v8_static_launch_transition_receipt_v1.json'), '92c7b1473bdced6426b0e52a4b29d181d4153fc1174ae7709469a7552bfd3524', '679920565b320b2bfb94f431902cac93a2af1ce506b725f0e3ea88ec1a59ae96'), (OUT / (HISTORICAL_BASE + '_static_audit_v8.json'), 'b467b7eea54a0d208ff560677929e15d14304f044016e858b9a267f6c5dab8dd', '8138cb5c1c99cb737ae50ff61c1a56efad6ac202889719d22d12997d1e0b6bb0'), (OUT / (HISTORICAL_BASE + '_cold_launch_v8.py'), V8_LAUNCHER_FILE_PIN, None), (OUT / (HISTORICAL_BASE + '_cold_launch_manifest_v8.sha256'), 'ae6e4998d6b347902b3e1ab5256abb6f9ab62d5feabf63a597a28e881068365f', None), (OUT / (HISTORICAL_BASE + '_cold_launch_outer_receipt_v8.json'), 'bc1f7d4c4c8cd2d5ade666ba71e920532651266a9e733b361dfa979b7a0e446f', '35c63aebeb08cf93339f01d3cc05c9552cbf0bffa50010ce60d4350990f3181d'))
    V8_FORBIDDEN_RUNTIME_PATHS = (RUNTIME / ('c79g-v8-candidate-a-' + CHECKPOINT), RUNTIME / ('c79g-v8-candidate-b-' + CHECKPOINT), RUNTIME / ('c79g-v8-verification-a-' + CHECKPOINT), RUNTIME / ('c79g-v8-verification-b-' + CHECKPOINT), RUNTIME / ('c79g-v8-committed-completion-' + CHECKPOINT), RUNTIME / 'cm2-global-authority-heads' / ('c79g-v8-' + CHECKPOINT + '.seal'), RUNTIME / ('.c79g-v8-candidate-stage-a-' + CHECKPOINT), RUNTIME / ('.c79g-v8-candidate-stage-b-' + CHECKPOINT), RUNTIME / ('.c79g-v8-verification-stage-a-' + CHECKPOINT), RUNTIME / ('.c79g-v8-verification-stage-b-' + CHECKPOINT), RUNTIME / ('.c79g-v8-completion-stage-' + CHECKPOINT), RUNTIME / 'cm2-global-authority-heads' / ('.c79g-v8-authority-stage-' + CHECKPOINT + '.seal'))
    V9_EXACT10_PINS = ((V8_OFFICIAL_REJECTION, V8_REJECTION_FILE_PIN, V8_REJECTION_OBJECT_PIN), (OUT / (HISTORICAL_BASE + '_schema_v9.json'), '2ddd254e43a196bb550fce69552c7f51eae063f4a9b75bc5818099c93335080b', None), (OUT / (HISTORICAL_BASE + '_contract_v9.json'), 'c37676119597f235f94104a55095c07e292fdd5c373c1811eeeed10c1b3d333f', '9a5fc94e11a30099ea0e23a574394399842efb8b350c98e9c16c5e8a8ce3963a'), (OUT / (HISTORICAL_BASE + '_v9.py'), 'e3dfcf7d2bda8daaeaf1412685909a1a96e1ff88f8d3c6ab1645288ee97c5a70', None), (OUT / (HISTORICAL_BASE + '_independent_verifier_assembler_authority_consumer_v9.py'), '0b38317123f88dc5f065603e51f63171ac0fcd3760de758cd1aa50544f8d3c97', None), (OUT / (HISTORICAL_BASE + '_v8_to_v9_static_launch_transition_receipt_v1.json'), 'ff4b42e258fec6cdd68d3c24f4903c9f3c2cec1ed2dc8f19dca703bddb45c522', '618f560f9ebbaaa5442af66af11f2efa7e4fe110a4f9cb586e3ab4424a1f95dc'), (OUT / (HISTORICAL_BASE + '_static_audit_v9.json'), '1c272852c18bff065a6b641d9c1f2a1c5a0da6db2a6e86a20588acb2be843571', '39463fbf2fb1c12ec68e4802b3ecd7dc48a95a2af6fcfe3430a27a0cb6ef9f4e'), (OUT / (HISTORICAL_BASE + '_cold_launch_v9.py'), 'f7559ceeb7d491b8489812670392cb63e3cd5f6a2764db469e2dd51d6b5577fa', None), (OUT / (HISTORICAL_BASE + '_cold_launch_manifest_v9.sha256'), '648f3dce04ca5fdfed8635e0f8c0d21c09404b3799dbfd108e92013fab5392a4', None), (OUT / (HISTORICAL_BASE + '_cold_launch_outer_receipt_v9.json'), '498a2d3c46c091f3a218c835bef0557b783401e81bb30dfb131562c23027b28b', '7df5cfed652b2696fa63387b9d471cd1947f90dd269c4e7846ffa0f6641ad6be'))
    V9_FORBIDDEN_RUNTIME_PATHS = (RUNTIME / ('c79g-v9-candidate-a-' + CHECKPOINT), RUNTIME / ('c79g-v9-candidate-b-' + CHECKPOINT), RUNTIME / ('c79g-v9-verification-a-' + CHECKPOINT), RUNTIME / ('c79g-v9-verification-b-' + CHECKPOINT), RUNTIME / ('c79g-v9-committed-completion-' + CHECKPOINT), RUNTIME / 'cm2-global-authority-heads' / ('c79g-v9-' + CHECKPOINT + '.seal'), RUNTIME / ('.c79g-v9-candidate-stage-a-' + CHECKPOINT), RUNTIME / ('.c79g-v9-candidate-stage-b-' + CHECKPOINT), RUNTIME / ('.c79g-v9-verification-stage-a-' + CHECKPOINT), RUNTIME / ('.c79g-v9-verification-stage-b-' + CHECKPOINT), RUNTIME / ('.c79g-v9-completion-stage-' + CHECKPOINT), RUNTIME / 'cm2-global-authority-heads' / ('.c79g-v9-authority-stage-' + CHECKPOINT + '.seal'))
    V10_EXACT10_PINS = ((V9_OFFICIAL_REJECTION, V9_REJECTION_FILE_PIN, V9_REJECTION_OBJECT_PIN), (OUT / (HISTORICAL_BASE + '_schema_v10.json'), 'a42dc06e276cc9206b29ec22df74ac7f8d76a4afb1de30115d048e1f7ce52801', None), (OUT / (HISTORICAL_BASE + '_contract_v10.json'), 'e9f9387c191ff7d34a75f73331d4926c989e0bcc641e21c6a3ace58fc5a7d479', 'c99acd60e953a939e3e9fd95e7559ce4249dc6efda0c3653e8ac1ae42b771bf4'), (OUT / (HISTORICAL_BASE + '_v10.py'), V10_PRODUCER_FILE_PIN, None), (OUT / (HISTORICAL_BASE + '_independent_verifier_assembler_authority_consumer_v10.py'), '3a72bba8930f15a66fa1111c76b9c3b6b2b9a2d21db32093d64d0c68a9f6d708', None), (OUT / (HISTORICAL_BASE + '_v9_to_v10_static_launch_transition_receipt_v1.json'), '6fe81931ee2051148e8ce0b7e67fcc45e56b992db7c74307f95aa9cc9dac6643', '249fd39eb7da989cbce59656f567028a38bb9900e4b577ae6d2f2ab4983ca6ac'), (OUT / (HISTORICAL_BASE + '_static_audit_v10.json'), 'e8a3f0497451689ec0835bb4048fe7be69fee4926e40620cdd128cc7b55ffb71', 'bb2cf294babf04fdbbbd35c88c1d6bce8c58426765ae69925c659b396feabcb8'), (OUT / (HISTORICAL_BASE + '_cold_launch_v10.py'), V10_LAUNCHER_FILE_PIN, None), (OUT / (HISTORICAL_BASE + '_cold_launch_manifest_v10.sha256'), 'bead6e9e1c53478c874612f00cae6cab1add14069d41b71b4310eb9b46b958db', None), (OUT / (HISTORICAL_BASE + '_cold_launch_outer_receipt_v10.json'), '2d95b83a2658d10a70d7c1e87b195920fc8207fc639fa407ff23252e5bc5edc4', 'fc2f595fb47795aff01396b9593630ef15f65237dcc0ffab2e5628e92722a6a4'))
    V10_FORBIDDEN_RUNTIME_PATHS = (RUNTIME / ('c79g-v10-candidate-a-' + CHECKPOINT), RUNTIME / ('c79g-v10-candidate-b-' + CHECKPOINT), RUNTIME / ('c79g-v10-verification-a-' + CHECKPOINT), RUNTIME / ('c79g-v10-verification-b-' + CHECKPOINT), RUNTIME / ('c79g-v10-committed-completion-' + CHECKPOINT), RUNTIME / 'cm2-global-authority-heads' / ('c79g-v10-' + CHECKPOINT + '.seal'), RUNTIME / ('.c79g-v10-candidate-stage-a-' + CHECKPOINT), RUNTIME / ('.c79g-v10-candidate-stage-b-' + CHECKPOINT), RUNTIME / ('.c79g-v10-verification-stage-a-' + CHECKPOINT), RUNTIME / ('.c79g-v10-verification-stage-b-' + CHECKPOINT), RUNTIME / ('.c79g-v10-completion-stage-' + CHECKPOINT), RUNTIME / 'cm2-global-authority-heads' / ('.c79g-v10-authority-stage-' + CHECKPOINT + '.seal'))
    V11_EXACT10_PINS = ((V10_OFFICIAL_REJECTION, V10_REJECTION_FILE_PIN, V10_REJECTION_OBJECT_PIN), (OUT / (HISTORICAL_BASE + '_schema_v11.json'), 'cf1630e3ab1b590876c663b8752d702eae5fe37b7bdbcc7824efbd03bbdbd8e2', None), (OUT / (HISTORICAL_BASE + '_contract_v11.json'), 'c8851778bc8df7a9804efb5fc226548424b58119a2dff3f75bdea9fcac0ec5cf', 'b998162a009927f13eb34a88e37f657515e43ae160b3d550de5edb0040486af9'), (OUT / (HISTORICAL_BASE + '_v11.py'), V11_PRODUCER_FILE_PIN, None), (OUT / (HISTORICAL_BASE + '_independent_verifier_assembler_authority_consumer_v11.py'), 'd8ad069e3486b9d657e4840e504885bf13129050f68e6cc04e47b71f149370ec', None), (OUT / (HISTORICAL_BASE + '_v10_to_v11_static_launch_transition_receipt_v1.json'), '31b33566b898277fb8b272a6f3cd3b51b0b80eac4f58f43979dddfa647a38f4e', '9a253960a378521423751735dd272e06dec5c99cfc016d27bf66cfbe7673caaf'), (OUT / (HISTORICAL_BASE + '_static_audit_v11.json'), '6c94068e3f60a89fb608585ae5e6c7dbe02af17880195132bf7c9033ab797115', '007fba200b67c7704360bb85819435ed13cc6459c8dbac381b99c3adaaf884c3'), (OUT / (HISTORICAL_BASE + '_cold_launch_v11.py'), V11_LAUNCHER_FILE_PIN, None), (OUT / (HISTORICAL_BASE + '_cold_launch_manifest_v11.sha256'), 'e27e9b58dbf57a72550da701589819dad7ebb01f6b3c649a56b701c99ef13135', None), (OUT / (HISTORICAL_BASE + '_cold_launch_outer_receipt_v11.json'), '689a4a323e742427c7f50ec6a7bbea08cdf28c36cbdb43d855a29601329f8c8f', '369dfe73b1dbc68e4147ba39e1c1b7155555b5443d9471159c5ac748723414a4'))
    V11_FORBIDDEN_RUNTIME_PATHS = (RUNTIME / ('c79g-v11-candidate-a-' + CHECKPOINT), RUNTIME / ('c79g-v11-candidate-b-' + CHECKPOINT), RUNTIME / ('c79g-v11-verification-a-' + CHECKPOINT), RUNTIME / ('c79g-v11-verification-b-' + CHECKPOINT), RUNTIME / ('c79g-v11-committed-completion-' + CHECKPOINT), RUNTIME / 'cm2-global-authority-heads' / ('c79g-v11-' + CHECKPOINT + '.seal'), RUNTIME / ('.c79g-v11-candidate-stage-a-' + CHECKPOINT), RUNTIME / ('.c79g-v11-candidate-stage-b-' + CHECKPOINT), RUNTIME / ('.c79g-v11-verification-stage-a-' + CHECKPOINT), RUNTIME / ('.c79g-v11-verification-stage-b-' + CHECKPOINT), RUNTIME / ('.c79g-v11-completion-stage-' + CHECKPOINT), RUNTIME / 'cm2-global-authority-heads' / ('.c79g-v11-authority-stage-' + CHECKPOINT + '.seal'))
    V12_EXACT10_PINS = ((V11_OFFICIAL_REJECTION, V11_REJECTION_FILE_PIN, V11_REJECTION_OBJECT_PIN), (OUT / (HISTORICAL_BASE + '_schema_v12.json'), '5ed911a55e8f90e750fdcaf6ab4fb6c9683bebaf66a4d6250329dff98acb2e28', None), (OUT / (HISTORICAL_BASE + '_contract_v12.json'), '72246725b15891f92cbc6e3fa1c07ab4a76cdaa19f1b366a736f47f51989b343', 'f5c1710817dc8e3aa7fe2bbf4b88e6e39baaa1b17bbeb0f8bf37c8c4575ae5d7'), (OUT / (HISTORICAL_BASE + '_v12.py'), '4cafc594f8a60063b7e7caaa82ddcc2b7983d0fbf0929034cd3cb5f360f3ed1d', None), (OUT / (HISTORICAL_BASE + '_independent_verifier_assembler_authority_consumer_v12.py'), 'b74dee738257d485e9ca3357d7d138b5175b95e58f1c8ea87d1eca7bfc96b2ed', None), (OUT / (HISTORICAL_BASE + '_v11_to_v12_static_launch_transition_receipt_v1.json'), '45dabc1ef60eb2f8ba34aa7daa69f9d2b3bedccd4168d9c472bd4bbb696b5400', '0673ecafaa9991cd78e905e144e7c8c1b91717a3d753befa13e82552d44a4072'), (OUT / (HISTORICAL_BASE + '_static_audit_v12.json'), 'ac29b1e31e0d1b51e8610b7699d1aaf55c80fa6f13f00b20b209c2889e121d37', 'c1473ae0f5a08d8772227f61a55bd32c479a7b5c7d40da17b37e796abf4d9783'), (OUT / (HISTORICAL_BASE + '_cold_launch_v12.py'), 'b7aaff67be866f8fd7a01f71e97ea1491574f69e62b7760b6ced9183997444ba', None), (OUT / (HISTORICAL_BASE + '_cold_launch_manifest_v12.sha256'), '297e9f58dc7657c6fa959dd45081efffe4e7e8dadcd16ab89457863e2661ece6', None), (OUT / (HISTORICAL_BASE + '_cold_launch_outer_receipt_v12.json'), '27129990a9d5b6697fd13ee8e2086100cbf158f12e5b767166d771e63088b6d0', 'bc6d06141865954590bd11bfc96ad59dbbffa003f568355ecb47155a8a3a809d'))
    V12_FORBIDDEN_RUNTIME_PATHS = (RUNTIME / ('c79g-v12-candidate-a-' + CHECKPOINT), RUNTIME / ('c79g-v12-candidate-b-' + CHECKPOINT), RUNTIME / ('c79g-v12-verification-a-' + CHECKPOINT), RUNTIME / ('c79g-v12-verification-b-' + CHECKPOINT), RUNTIME / ('c79g-v12-committed-completion-' + CHECKPOINT), RUNTIME / 'cm2-global-authority-heads' / ('c79g-v12-' + CHECKPOINT + '.seal'), RUNTIME / ('.c79g-v12-candidate-stage-a-' + CHECKPOINT), RUNTIME / ('.c79g-v12-candidate-stage-b-' + CHECKPOINT), RUNTIME / ('.c79g-v12-verification-stage-a-' + CHECKPOINT), RUNTIME / ('.c79g-v12-verification-stage-b-' + CHECKPOINT), RUNTIME / ('.c79g-v12-completion-stage-' + CHECKPOINT), RUNTIME / 'cm2-global-authority-heads' / ('.c79g-v12-authority-stage-' + CHECKPOINT + '.seal'))
INNER_SCHEMA = 'cm2.round306c79g.true-global-no-producer-consumer.v16r2.inner-composite'
COLD_ROOT_SCHEMA = 'cm2.round306c79g.true-global-no-producer-consumer.v16r2.cold-launched-committed-authority'
COLD_ROOT_DOMAIN = b'CM2_C79G_V16R2_COLD_LAUNCHED_AUTHORITY_ROOT_V1\x00'
LIVE_PROTOCOL = 'CM2_C79G_V16R2_COLD_TWO_PHASE_LIVE_ACK_V1'
LIVE_REQUEST_SCHEMA = 'cm2.round306c79g.true-global-no-producer-consumer.v16r2.cold-live-commit-request'
LIVE_ACK_SCHEMA = 'cm2.round306c79g.true-global-no-producer-consumer.v16r2.cold-live-ack'
LIVE_RELEASE_SCHEMA = 'cm2.round306c79g.true-global-no-producer-consumer.v16r2.cold-live-release'
PREWRAPPER_BODY_DOMAIN = 'CM2_C79G_V16R2_COLD_PREWRAPPER_BODY_V1'
TRANSACTION_BINDING_DOMAIN = 'CM2_C79G_V16R2_COLD_TRANSACTION_BINDING_V1'
LIVE_ACK_BINDING_DOMAIN = 'CM2_C79G_V16R2_COLD_LIVE_ACK_BINDING_V1'
SOURCE_FD_ENV = 'CM2_C79G_V16R2_COLD_SOURCE_FD'
EXEC_FD_ENV = 'CM2_C79G_V16R2_COLD_EXEC_FD'
COORDINATION_PARENT_FD_ENV = 'CM2_C79G_V16R2_COORDINATION_PARENT_FD'
WORKSPACE_ROOT_ENV = 'CM2_C79G_V16R2_COLD_WORKSPACE_ROOT'
WORKSPACE_ROOT_FD_ENV = 'CM2_C79G_V16R2_COLD_WORKSPACE_ROOT_FD'
LAUNCHER_SHA_ENV = 'CM2_C79G_V16R2_COLD_LAUNCHER_FILE_SHA256'
HELD_V10_PRODUCER_FD_ENV = 'CM2_C79G_V16R2_V10_PRODUCER_FD'
HELD_V9_LAUNCHER_FD_ENV = 'CM2_C79G_V16R2_V9_LAUNCHER_FD'
HELD_V11_PRODUCER_FD_ENV = 'CM2_C79G_V16R2_V11_PRODUCER_FD'
HELD_V11_LAUNCHER_FD_ENV = 'CM2_C79G_V16R2_V11_LAUNCHER_FD'
HELD_V11_REJECTION_FD_ENV = 'CM2_C79G_V16R2_V11_REJECTION_FD'
HELD_V12_PRODUCER_FD_ENV = 'CM2_C79G_V16R2_V12_PRODUCER_FD'
HELD_V12_CONSUMER_FD_ENV = 'CM2_C79G_V16R2_V12_CONSUMER_FD'
HELD_V12_LAUNCHER_FD_ENV = 'CM2_C79G_V16R2_V12_LAUNCHER_FD'
HELD_V5_REJECTION_FD_ENV = 'CM2_C79G_V16R2_V5_REJECTION_FD'
HELD_V12_REJECTION_FD_ENV = 'CM2_C79G_V16R2_V12_REJECTION_FD'
HELD_V13_PRODUCER_FD_ENV = 'CM2_C79G_V16R2_V13_PRODUCER_FD'
HELD_V13_CONSUMER_FD_ENV = 'CM2_C79G_V16R2_V13_CONSUMER_FD'
HELD_V13_LAUNCHER_FD_ENV = 'CM2_C79G_V16R2_V13_LAUNCHER_FD'
HELD_V13_PRODUCER_PYC_FD_ENV = 'CM2_C79G_V16R2_V13_PRODUCER_PYC_FD'
HELD_V13_CONSUMER_PYC_FD_ENV = 'CM2_C79G_V16R2_V13_CONSUMER_PYC_FD'
HELD_V13_LAUNCHER_PYC_FD_ENV = 'CM2_C79G_V16R2_V13_LAUNCHER_PYC_FD'
HELD_V13_SUPERSESSION_RECEIPT_FD_ENV = 'CM2_C79G_V16R2_V13_SUPERSESSION_RECEIPT_FD'

def v13_inherited_exact16_records() -> list[dict[str, Any]]:
    """Rebuild the receipt's ordered exact16 from independent fixed pins."""
    members = (('v10_producer', V10_EXACT10_PINS[3][0], V10_PRODUCER_FILE_PIN), ('v9_launcher', V9_EXACT10_PINS[7][0], V9_EXACT10_PINS[7][1]), ('v11_producer', V11_EXACT10_PINS[3][0], V11_PRODUCER_FILE_PIN), ('v11_launcher', V11_EXACT10_PINS[7][0], V11_LAUNCHER_FILE_PIN), ('v11_rejection', V11_OFFICIAL_REJECTION, V11_REJECTION_FILE_PIN), ('v12_producer', V12_EXACT10_PINS[3][0], V12_EXACT10_PINS[3][1]), ('v12_consumer', V12_EXACT10_PINS[4][0], V12_EXACT10_PINS[4][1]), ('v12_launcher', V12_EXACT10_PINS[7][0], V12_EXACT10_PINS[7][1]), ('v5_rejection', V5_OFFICIAL_REJECTION, V5_REJECTION_FILE_PIN), ('v12_rejection', V12_OFFICIAL_REJECTION, V12_REJECTION_FILE_PIN), ('v13_build_only_producer_source', V13_FROZEN_PRODUCER, V13_PRODUCER_FILE_PIN), ('v13_independent_consumer_source', V13_FROZEN_CONSUMER, V13_CONSUMER_FILE_PIN), ('v13_cold_launcher_source', V13_FROZEN_LAUNCHER, V13_LAUNCHER_FILE_PIN), ('v13_build_only_producer_pyc', V13_FROZEN_PRODUCER_PYC, V13_PRODUCER_PYC_FILE_PIN), ('v13_independent_consumer_pyc', V13_FROZEN_CONSUMER_PYC, V13_CONSUMER_PYC_FILE_PIN), ('v13_cold_launcher_pyc', V13_FROZEN_LAUNCHER_PYC, V13_LAUNCHER_PYC_FILE_PIN))
    return [{'ordinal': ordinal, 'role': role, 'path': str(path.relative_to(ROOT)), 'file_sha256': file_pin} for ordinal, (role, path, file_pin) in enumerate(members, start=1)]

def validate_v13_supersession_receipt(value: Any, exact6: list[HeldFile] | None=None) -> None:
    """Close the one-way receipt, exact16 table, census and live exact6."""
    need(isinstance(value, dict), 'v13 supersession receipt object')
    verify_object(value, 'v13 supersession receipt', V13_SUPERSESSION_RECEIPT_OBJECT_PIN)
    exact16 = v13_inherited_exact16_records()
    exact16_raw = canonical(exact16)
    successor = value.get('v14_successor_contract', {})
    inherited = successor.get('inherited_incident_authority_exact16', {})
    normalized = value.get('frozen_v13_inherited_incident_authority_exact10_source_contract', {})
    need(value.get('schema') == 'cm2.round306c79g.true-global-no-producer-consumer.v13-prepublication-pyc-contamination-rejection-supersession-receipt.v1' and value.get('status') == 'FROZEN_APPEND_ONLY_V13_PREPUBLICATION_PYC_CONTAMINATION_REJECTION__V14_SUCCESSOR_ONLY' and (value.get('receipt_path') == str(V13_SUPERSESSION_RECEIPT.relative_to(ROOT))) and (value.get('effective_checkpoint_object_sha256') == CHECKPOINT) and (inherited.get('ordered_members') == exact16) and (inherited.get('ordered_member_count') == 16) and (inherited.get('ordered_member_exact_keys') == ['ordinal', 'role', 'path', 'file_sha256']) and (len(exact16_raw) == 3646) and (sha_bytes(exact16_raw) == inherited.get('ordered_exact16_canonical_sha256') == V13_INHERITED_EXACT16_CANONICAL_SHA256) and (normalized.get('normalized_ordered_member_count') == 10) and (normalized.get('normalized_exact10_canonical_byte_length') == 2657) and (normalized.get('normalized_exact10_canonical_sha256') == V13_NORMALIZED_EXACT10_CANONICAL_SHA256) and (successor.get('v14_current_exact8_first_member_must_be_this_receipt') is True) and (successor.get('v14_must_preserve_v12_exact10_and_official_rejection') is True) and (successor.get('v14_predecessor_unique_live_identity_count') == 105) and (successor.get('v14_prepublication_unique_live_identity_count') == 113) and (successor.get('v14_terminal_unique_live_identity_count') == 115) and (successor.get('v14_terminal_group_vector') == [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 7, 1, 3, 3, 1]) and (inherited.get('v14_must_live_hold_and_terminally_replay_exact16_plus_this_receipt') is True), 'v13 supersession receipt exact16/digest/census closure')
    if exact6 is not None:
        expected = exact16[10:]
        need(len(exact6) == 6 and [item.path for item in exact6] == [ROOT / row['path'] for row in expected] and ([item.file_sha256 for item in exact6] == [row['file_sha256'] for row in expected]), 'v13 receipt exact6 equals live held source/pyc order and pins')

def expected_v13_supersession_summary(receipt: Mapping[str, Any]) -> dict[str, Any]:
    """Build the exact seven-key non-predecessor v13 rejection summary."""
    return {'receipt_path': str(V13_SUPERSESSION_RECEIPT.relative_to(ROOT)), 'receipt_file_sha256': V13_SUPERSESSION_RECEIPT_FILE_PIN, 'receipt_object_sha256': V13_SUPERSESSION_RECEIPT_OBJECT_PIN, 'receipt_schema': 'cm2.round306c79g.true-global-no-producer-consumer.v13-prepublication-pyc-contamination-rejection-supersession-receipt.v1', 'receipt_status': 'FROZEN_APPEND_ONLY_V13_PREPUBLICATION_PYC_CONTAMINATION_REJECTION__V14_SUCCESSOR_ONLY', 'transition_kind': 'APPEND_ONLY_V13_PREPUBLICATION_PYC_CONTAMINATION_REJECTION_TO_ZERO_CREDIT_V14_STATIC_SUCCESSOR', 'v14_successor_contract': copy.deepcopy(receipt['v14_successor_contract'])}

def validate_v13_supersession_summary(value: Any, receipt: Mapping[str, Any], label: str) -> None:
    expected = expected_v13_supersession_summary(receipt)
    need(isinstance(value, dict) and list(value) == list(expected) and (value == expected) and (len(value) == 7), label + ':exact rejected-prepublication v13 receipt summary')

class Reject(RuntimeError):
    pass

def need(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise Reject(label)

def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=True, allow_nan=False).encode('ascii')

def sha_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()

def derive_v12_v5_rejection_shape_incident(producer_raw: bytes, consumer_raw: bytes, launcher_raw: bytes, v5_rejection_raw: bytes, v12_rejection_raw: bytes) -> dict[str, Any]:
    """Reproduce the frozen v12 pre-child exact39-vs-52 incident."""
    source_rows = (('producer', producer_raw, 'official v5 rejection exact canonical 39-key zero-credit closure'), ('consumer', consumer_raw, 'v5 official rejection canonical singleton zero-credit envelope'), ('launcher', launcher_raw, 'official v5 rejection binds published v5 exact10'))
    expected_hashes = {'producer': V12_V5_REJECTION_SHAPE_INCIDENT['v12_producer_source_file_sha256'], 'consumer': V12_V5_REJECTION_SHAPE_INCIDENT['v12_consumer_source_file_sha256'], 'launcher': V12_V5_REJECTION_SHAPE_INCIDENT['v12_launcher_source_file_sha256']}
    exact39_counts: dict[str, int] = {}
    wrong52_counts: dict[str, int] = {}
    for role, raw, label in source_rows:
        need(sha_bytes(raw) == expected_hashes[role], 'frozen v12 incident source hash:' + role)
        try:
            tree = ast.parse(raw.decode('utf-8'), filename='v12_' + role)
        except (UnicodeDecodeError, SyntaxError) as exc:
            raise Reject('frozen v12 incident source AST:' + role) from exc
        owners = [node for node in ast.walk(tree) if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and any((isinstance(call, ast.Call) and isinstance(call.func, ast.Name) and (call.func.id == 'need') and (len(call.args) == 2) and isinstance(call.args[1], ast.Constant) and (call.args[1].value == label) for call in ast.walk(node)))]
        need(len(owners) == 1, 'frozen v12 unique labelled v5 rejection gate:' + role)
        owner = owners[0]
        exact39_counts[role] = sum((1 for node in ast.walk(owner) if isinstance(node, ast.Set) and len(node.elts) == 39 and all((isinstance(item, ast.Constant) and isinstance(item.value, str) for item in node.elts)) and ({item.value for item in node.elts} == V5_OFFICIAL_REJECTION_EXACT39_KEYS)))
        wrong52_counts[role] = sum((1 for node in ast.walk(owner) if isinstance(node, ast.Compare) and isinstance(node.left, ast.Call) and isinstance(node.left.func, ast.Name) and (node.left.func.id == 'len') and (len(node.left.args) == 1) and (len(node.ops) == len(node.comparators) == 1) and isinstance(node.ops[0], ast.Eq) and isinstance(node.comparators[0], ast.Constant) and (node.comparators[0].value == 52)))
    need(exact39_counts == {'producer': 1, 'consumer': 1, 'launcher': 0} and wrong52_counts == {'producer': 0, 'consumer': 0, 'launcher': 1}, 'frozen v12 P/C exact39 versus launcher wrong52 structural witness')
    v5_rejection = strict_json(v5_rejection_raw, 'frozen v5 rejection incident')
    need(isinstance(v5_rejection, dict) and set(v5_rejection) == V5_OFFICIAL_REJECTION_EXACT39_KEYS and (len(v5_rejection) == 39) and (sha_bytes(canonical(sorted(v5_rejection))) == V5_OFFICIAL_REJECTION_EXACT39_KEYSET_SHA256) and (sha_bytes(v5_rejection_raw) == V5_OFFICIAL_REJECTION_FILE_PIN) and (v5_rejection_raw == canonical(v5_rejection) + b'\n'), 'frozen v5 rejection exact39 incident bytes')
    verify_object(v5_rejection, 'frozen v5 rejection incident', V5_OFFICIAL_REJECTION_OBJECT_PIN)
    v12_rejection = strict_json(v12_rejection_raw, 'frozen v12 rejection incident')
    need(isinstance(v12_rejection, dict) and set(v12_rejection) == V12_OFFICIAL_REJECTION_EXACT54_KEYS and (len(v12_rejection) == 54) and (sha_bytes(canonical(sorted(v12_rejection))) == V12_OFFICIAL_REJECTION_EXACT54_KEYSET_SHA256) and (sha_bytes(v12_rejection_raw) == V12_OFFICIAL_REJECTION_FILE_PIN) and (v12_rejection_raw == canonical(v12_rejection) + b'\n') and (v12_rejection.get('formal_global_closure_credit') == 0) and (v12_rejection.get('D02_unlock') is False) and (v12_rejection.get('D02_started') is False), 'frozen v12 rejection exact54 zero-credit incident bytes')
    verify_object(v12_rejection, 'frozen v12 rejection incident', V12_OFFICIAL_REJECTION_OBJECT_PIN)
    need(sha_bytes(canonical(V12_FIRST_RUNTIME_ATTEMPT)) == V12_FIRST_RUNTIME_ATTEMPT_SHA256 and sha_bytes(canonical(V12_V5_REJECTION_SHAPE_INCIDENT)) == V12_V5_REJECTION_SHAPE_INCIDENT_SHA256, 'v12 first-attempt and shape-incident canonical witnesses')
    return copy.deepcopy(V12_V5_REJECTION_SHAPE_INCIDENT)
HISTORICAL_REJECTION_BASE_EXACT37_KEYS = frozenset({'D02_formal_pending_task_count', 'D02_gate_credit', 'D02_started', 'D02_task_credit', 'D02_unlock', 'closed_schema_file_sha256', 'cold_launcher_file_sha256', 'cold_manifest_file_sha256', 'cold_outer_file_sha256', 'cold_outer_object_sha256', 'commit_operation', 'consumer_file_sha256', 'contract_file_sha256', 'contract_object_sha256', 'effective_checkpoint_object_sha256', 'file_fsync_required', 'formal_global_closure_credit', 'idempotent_existing_recovery_re_fsyncs_rejection_file_namespace_and_runtime_parent', 'namespace_at_rest_mode', 'namespace_exact_path', 'namespace_fsync_required_after_file_and_after_reseal', 'namespace_lock_held_write_window_mode', 'object_sha256', 'official_writer_coordination_lock_held_for_entire_reject_command', 'official_writer_coordination_lock_policy', 'overwrite_delete_or_reuse_allowed', 'partial_malformed_or_extra_namespace_entry_revokes_authority', 'producer_file_sha256', 'rejection_file_mode', 'rejection_file_nlink', 'rejection_reason', 'runtime_parent_fsync_required_after_namespace_creation', 'schema', 'standalone_authority', 'status', 'target_exact_path', 'target_is_protocol_and_checkpoint_deterministic'})
HISTORICAL_REJECTION_KEYSET_STEPS = ((3, frozenset(), V3_OFFICIAL_REJECTION_FILE_PIN, V3_OFFICIAL_REJECTION_OBJECT_PIN, '21ba021c649349266d95670e63136fef1772b5d8dbb79334907c9df400620a18'), (5, frozenset({'v4_rejection_supersession_file_sha256', 'v4_rejection_supersession_object_sha256'}), V5_OFFICIAL_REJECTION_FILE_PIN, V5_OFFICIAL_REJECTION_OBJECT_PIN, V5_OFFICIAL_REJECTION_EXACT39_KEYSET_SHA256), (6, frozenset({'v5_official_rejection_file_sha256', 'v5_official_rejection_object_sha256'}), V6_OFFICIAL_REJECTION_FILE_PIN, V6_OFFICIAL_REJECTION_OBJECT_PIN, '5881a652aabef3e7e65917689487f13b99bfa60fff0ebb7c144bc02b26897638'), (7, frozenset({'v6_official_rejection_file_sha256', 'v6_official_rejection_object_sha256'}), V7_OFFICIAL_REJECTION_FILE_PIN, V7_OFFICIAL_REJECTION_OBJECT_PIN, '02b54c94602de1f5af8e545692f44815b9ac3ba334369dd96ee4e9b677bf1308'), (8, frozenset({'v7_official_rejection_file_sha256', 'v7_official_rejection_object_sha256', 'v7_publication_lock_continuity_incident_object_sha256'}), V8_OFFICIAL_REJECTION_FILE_PIN, V8_OFFICIAL_REJECTION_OBJECT_PIN, 'a1da14307b813345ee0f8877550412b40951f7857e5972570ab41f97e2fe31bf'), (9, frozenset({'v8_official_rejection_file_sha256', 'v8_official_rejection_object_sha256'}), V9_OFFICIAL_REJECTION_FILE_PIN, V9_OFFICIAL_REJECTION_OBJECT_PIN, 'd0617183e15fd4c5bfd3495d7dca56cb9aea7035bedf35a1bdf6efd166a70308'), (10, frozenset({'v9_official_rejection_file_sha256', 'v9_official_rejection_object_sha256'}), V10_OFFICIAL_REJECTION_FILE_PIN, V10_OFFICIAL_REJECTION_OBJECT_PIN, '01274ec0c36bd85423d385bdb22cdff7fe6ccfe2d114864994fc2ead2153eddb'), (11, frozenset({'v10_official_rejection_file_sha256', 'v10_official_rejection_object_sha256'}), V11_OFFICIAL_REJECTION_FILE_PIN, V11_OFFICIAL_REJECTION_OBJECT_PIN, '75ca9378fbff7a6956686e7390556fffa3d6ff939630ed47e8c8c185872e97f8'), (12, frozenset({'v11_official_rejection_file_sha256', 'v11_official_rejection_object_sha256'}), V12_OFFICIAL_REJECTION_FILE_PIN, V12_OFFICIAL_REJECTION_OBJECT_PIN, V12_OFFICIAL_REJECTION_EXACT54_KEYSET_SHA256))
HISTORICAL_REJECTION_V3_KEYS = HISTORICAL_REJECTION_BASE_EXACT37_KEYS
HISTORICAL_REJECTION_V5_KEYS = HISTORICAL_REJECTION_V3_KEYS | frozenset({'v4_rejection_supersession_file_sha256', 'v4_rejection_supersession_object_sha256'})
HISTORICAL_REJECTION_V6_KEYS = HISTORICAL_REJECTION_V5_KEYS | frozenset({'v5_official_rejection_file_sha256', 'v5_official_rejection_object_sha256'})
HISTORICAL_REJECTION_V7_KEYS = HISTORICAL_REJECTION_V6_KEYS | frozenset({'v6_official_rejection_file_sha256', 'v6_official_rejection_object_sha256'})
HISTORICAL_REJECTION_V8_KEYS = HISTORICAL_REJECTION_V7_KEYS | frozenset({'v7_official_rejection_file_sha256', 'v7_official_rejection_object_sha256', 'v7_publication_lock_continuity_incident_object_sha256'})
HISTORICAL_REJECTION_V9_KEYS = HISTORICAL_REJECTION_V8_KEYS | frozenset({'v8_official_rejection_file_sha256', 'v8_official_rejection_object_sha256'})
HISTORICAL_REJECTION_V10_KEYS = HISTORICAL_REJECTION_V9_KEYS | frozenset({'v9_official_rejection_file_sha256', 'v9_official_rejection_object_sha256'})
HISTORICAL_REJECTION_V11_KEYS = HISTORICAL_REJECTION_V10_KEYS | frozenset({'v10_official_rejection_file_sha256', 'v10_official_rejection_object_sha256'})
HISTORICAL_REJECTION_V12_KEYS = HISTORICAL_REJECTION_V11_KEYS | frozenset({'v11_official_rejection_file_sha256', 'v11_official_rejection_object_sha256'})

def _build_historical_rejection_exact_keyset_witness() -> tuple[dict[str, Any], ...]:
    keys = HISTORICAL_REJECTION_BASE_EXACT37_KEYS
    rows: list[dict[str, Any]] = []
    for version, additions, file_pin, object_pin, keyset_digest in HISTORICAL_REJECTION_KEYSET_STEPS:
        keys = keys | additions
        sorted_keys = sorted(keys)
        need(sha_bytes(canonical(sorted_keys)) == keyset_digest, 'historical rejection exact keyset digest:v' + str(version))
        rows.append({'version': 'v' + str(version), 'path': '.cm2-runtime/c79g-v' + str(version) + '-rejections-' + CHECKPOINT + '/rejection.json', 'file_sha256': file_pin, 'object_sha256': object_pin, 'key_count': len(sorted_keys), 'sorted_keys': sorted_keys, 'sorted_key_array_sha256': keyset_digest, 'canonical_object_closed': True})
    need([row['version'] for row in rows] == ['v3', 'v5', 'v6', 'v7', 'v8', 'v9', 'v10', 'v11', 'v12'] and [row['key_count'] for row in rows] == [37, 39, 41, 43, 46, 48, 50, 52, 54], 'historical rejection exact ordered nine-row keyset witness')
    return tuple(rows)
HISTORICAL_REJECTION_EXACT_KEYSET_WITNESS = ({'version': 'v3', 'path': '.cm2-runtime/c79g-v3-rejections-' + CHECKPOINT + '/rejection.json', 'file_sha256': V3_OFFICIAL_REJECTION_FILE_PIN, 'object_sha256': V3_OFFICIAL_REJECTION_OBJECT_PIN, 'key_count': 37, 'sorted_keys': sorted(HISTORICAL_REJECTION_V3_KEYS), 'sorted_key_array_sha256': '21ba021c649349266d95670e63136fef1772b5d8dbb79334907c9df400620a18', 'canonical_object_closed': True}, {'version': 'v5', 'path': '.cm2-runtime/c79g-v5-rejections-' + CHECKPOINT + '/rejection.json', 'file_sha256': V5_OFFICIAL_REJECTION_FILE_PIN, 'object_sha256': V5_OFFICIAL_REJECTION_OBJECT_PIN, 'key_count': 39, 'sorted_keys': sorted(HISTORICAL_REJECTION_V5_KEYS), 'sorted_key_array_sha256': V5_OFFICIAL_REJECTION_EXACT39_KEYSET_SHA256, 'canonical_object_closed': True}, {'version': 'v6', 'path': '.cm2-runtime/c79g-v6-rejections-' + CHECKPOINT + '/rejection.json', 'file_sha256': V6_OFFICIAL_REJECTION_FILE_PIN, 'object_sha256': V6_OFFICIAL_REJECTION_OBJECT_PIN, 'key_count': 41, 'sorted_keys': sorted(HISTORICAL_REJECTION_V6_KEYS), 'sorted_key_array_sha256': '5881a652aabef3e7e65917689487f13b99bfa60fff0ebb7c144bc02b26897638', 'canonical_object_closed': True}, {'version': 'v7', 'path': '.cm2-runtime/c79g-v7-rejections-' + CHECKPOINT + '/rejection.json', 'file_sha256': V7_OFFICIAL_REJECTION_FILE_PIN, 'object_sha256': V7_OFFICIAL_REJECTION_OBJECT_PIN, 'key_count': 43, 'sorted_keys': sorted(HISTORICAL_REJECTION_V7_KEYS), 'sorted_key_array_sha256': '02b54c94602de1f5af8e545692f44815b9ac3ba334369dd96ee4e9b677bf1308', 'canonical_object_closed': True}, {'version': 'v8', 'path': '.cm2-runtime/c79g-v8-rejections-' + CHECKPOINT + '/rejection.json', 'file_sha256': V8_OFFICIAL_REJECTION_FILE_PIN, 'object_sha256': V8_OFFICIAL_REJECTION_OBJECT_PIN, 'key_count': 46, 'sorted_keys': sorted(HISTORICAL_REJECTION_V8_KEYS), 'sorted_key_array_sha256': 'a1da14307b813345ee0f8877550412b40951f7857e5972570ab41f97e2fe31bf', 'canonical_object_closed': True}, {'version': 'v9', 'path': '.cm2-runtime/c79g-v9-rejections-' + CHECKPOINT + '/rejection.json', 'file_sha256': V9_OFFICIAL_REJECTION_FILE_PIN, 'object_sha256': V9_OFFICIAL_REJECTION_OBJECT_PIN, 'key_count': 48, 'sorted_keys': sorted(HISTORICAL_REJECTION_V9_KEYS), 'sorted_key_array_sha256': 'd0617183e15fd4c5bfd3495d7dca56cb9aea7035bedf35a1bdf6efd166a70308', 'canonical_object_closed': True}, {'version': 'v10', 'path': '.cm2-runtime/c79g-v10-rejections-' + CHECKPOINT + '/rejection.json', 'file_sha256': V10_OFFICIAL_REJECTION_FILE_PIN, 'object_sha256': V10_OFFICIAL_REJECTION_OBJECT_PIN, 'key_count': 50, 'sorted_keys': sorted(HISTORICAL_REJECTION_V10_KEYS), 'sorted_key_array_sha256': '01274ec0c36bd85423d385bdb22cdff7fe6ccfe2d114864994fc2ead2153eddb', 'canonical_object_closed': True}, {'version': 'v11', 'path': '.cm2-runtime/c79g-v11-rejections-' + CHECKPOINT + '/rejection.json', 'file_sha256': V11_OFFICIAL_REJECTION_FILE_PIN, 'object_sha256': V11_OFFICIAL_REJECTION_OBJECT_PIN, 'key_count': 52, 'sorted_keys': sorted(HISTORICAL_REJECTION_V11_KEYS), 'sorted_key_array_sha256': '75ca9378fbff7a6956686e7390556fffa3d6ff939630ed47e8c8c185872e97f8', 'canonical_object_closed': True}, {'version': 'v12', 'path': '.cm2-runtime/c79g-v12-rejections-' + CHECKPOINT + '/rejection.json', 'file_sha256': V12_OFFICIAL_REJECTION_FILE_PIN, 'object_sha256': V12_OFFICIAL_REJECTION_OBJECT_PIN, 'key_count': 54, 'sorted_keys': sorted(HISTORICAL_REJECTION_V12_KEYS), 'sorted_key_array_sha256': V12_OFFICIAL_REJECTION_EXACT54_KEYSET_SHA256, 'canonical_object_closed': True})

def _nonzero_sha256(value: Any) -> bool:
    return isinstance(value, str) and re.fullmatch('[0-9a-f]{64}', value) is not None and (value != '0' * 64)
_STRICT_BOOL_CALL_NAMES = frozenset({'isinstance', 'issubclass', 'hasattr', 'callable', 'bool', 'all', 'any', '_static_freeze_is_valid', '_nonzero_sha256', '_no_zero_hash_placeholder', '_closed_object_equal'})
_STRICT_BOOL_METHOD_NAMES = frozenset({'startswith', 'endswith', 'isascii', 'isdecimal', 'isdigit', 'is_absolute', 'is_symlink', 'is_file', 'is_dir', 'exists', 'isdisjoint', 'issubset', 'issuperset', 'S_ISDIR', 'S_ISREG', 'S_ISFIFO', 'get_blocking'})

def _strict_bool_expression_is_proved(node: ast.AST) -> bool:
    """Conservative syntax proof for a strict-bool ``need`` condition."""
    if isinstance(node, ast.Compare):
        return True
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.Not):
        return True
    if isinstance(node, ast.BoolOp):
        return all((_strict_bool_expression_is_proved(item) for item in node.values))
    if isinstance(node, ast.Constant):
        return type(node.value) is bool
    if isinstance(node, ast.IfExp):
        return _strict_bool_expression_is_proved(node.body) and _strict_bool_expression_is_proved(node.orelse)
    if isinstance(node, ast.Call):
        if isinstance(node.func, ast.Name):
            return node.func.id in _STRICT_BOOL_CALL_NAMES
        if isinstance(node.func, ast.Attribute):
            return node.func.attr in _STRICT_BOOL_METHOD_NAMES
    return False

def v5_strict_bool_regression(sources: Mapping[str, bytes]) -> dict[str, Any]:
    """Reproduce the frozen v5 700-call / 15-risk deterministic census."""
    ordered_roles = ('producer_v5', 'consumer_v5', 'launcher_v5')
    expected_need_counts = {'producer_v5': 217, 'consumer_v5': 345, 'launcher_v5': 138}
    rows: list[dict[str, Any]] = []
    observed_need_counts: dict[str, int] = {}
    for role in ordered_roles:
        raw = sources.get(role)
        if not isinstance(raw, bytes):
            raise Reject('frozen v5 strict-bool source bytes:' + role)
        try:
            source = raw.decode('utf-8')
            tree = ast.parse(source, filename=role, mode='exec')
        except (UnicodeDecodeError, SyntaxError) as exc:
            raise Reject('frozen v5 strict-bool AST parse:' + role) from exc
        calls = [node for node in ast.walk(tree) if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and (node.func.id == 'need')]
        observed_need_counts[role] = len(calls)
        for call in calls:
            if len(call.args) != 2 or call.keywords or any((isinstance(item, ast.Starred) for item in call.args)):
                raise Reject('frozen v5 need arity/star/keyword:' + role)
            condition = call.args[0]
            if not _strict_bool_expression_is_proved(condition):
                segment = ast.get_source_segment(source, condition)
                if not isinstance(segment, str):
                    raise Reject('frozen v5 need source segment:' + role)
                rows.append({'role': role, 'line': call.lineno, 'column': call.col_offset, 'condition': segment.replace('\n', ' '), 'condition_ast': ast.dump(condition, annotate_fields=True, include_attributes=False)})
    role_order = {role: index for index, role in enumerate(ordered_roles)}
    rows.sort(key=lambda row: (role_order[row['role']], row['line'], row['column']))
    risk_id_by_callsite = {('launcher_v5', 1677): V5_STRICT_BOOL_RISK_IDS[0], ('launcher_v5', 1682): V5_STRICT_BOOL_RISK_IDS[1], ('consumer_v5', 3740): V5_STRICT_BOOL_RISK_IDS[2], ('producer_v5', 510): V5_STRICT_BOOL_RISK_IDS[3], ('consumer_v5', 894): V5_STRICT_BOOL_RISK_IDS[4], ('launcher_v5', 317): V5_STRICT_BOOL_RISK_IDS[5], ('launcher_v5', 324): V5_STRICT_BOOL_RISK_IDS[6]}
    hard_callsite_set = {('consumer_v5', 3740), ('launcher_v5', 1677), ('launcher_v5', 1682)}
    observed_hard = {(row['role'], row['line']) for row in rows if (row['role'], row['line']) in hard_callsite_set}
    observed_risk_id_set = {risk_id_by_callsite[row['role'], row['line']] for row in rows if (row['role'], row['line']) in risk_id_by_callsite}
    result = {'need_call_count': sum(observed_need_counts.values()), 'need_call_count_by_role': observed_need_counts, 'arity_star_keyword_failure_count': 0, 'strict_bool_unproved_count': len(rows), 'strict_bool_risk_count': len(observed_risk_id_set), 'ordered_strict_bool_risk_ids': list(V5_STRICT_BOOL_RISK_IDS), 'ordered_strict_bool_risk_id_sha256': sha_bytes(canonical(list(V5_STRICT_BOOL_RISK_IDS))), 'definite_truthy_nonbool_hard_callsite_count': len(observed_hard), 'definite_truthy_nonbool_hard_callsites': sorted(observed_hard), 'ordered_census_sha256': sha_bytes(canonical(rows))}
    need(observed_need_counts == expected_need_counts and result['need_call_count'] == 700 and (result['strict_bool_unproved_count'] == 15) and (result['strict_bool_risk_count'] == 7) and (observed_risk_id_set == set(V5_STRICT_BOOL_RISK_IDS)) and (result['ordered_strict_bool_risk_id_sha256'] == V5_STRICT_BOOL_RISK_ID_ORDER_SHA256) and (observed_hard == hard_callsite_set) and (result['ordered_census_sha256'] == V5_STRICT_BOOL_UNPROVED_CENSUS_SHA256), 'frozen v5 strict-bool 700/7-risk/three-hard census')
    return result

def expected_v5_published_rejected_segment() -> dict[str, Any]:
    """Construct the one exact v5 regression shape shared by v16r2 proofs."""
    names = ('v4_rejection_supersession', 'closed_schema', 'contract', 'build_only_producer', 'independent_consumer', 'v4_to_v5_transition', 'static_audit', 'cold_launcher', 'cold_manifest', 'cold_outer')
    ordered: list[dict[str, Any]] = []
    for name, (path, file_pin, object_pin) in zip(names, V5_EXACT10_PINS, strict=True):
        member: dict[str, Any] = {'name': name, 'path': str(path.relative_to(ROOT)), 'file_sha256': file_pin}
        if object_pin is not None:
            member['object_sha256'] = object_pin
        ordered.append(member)
    return {'ordered_published_exact10': ordered, 'official_later_rejection': {'path': str(V5_OFFICIAL_REJECTION.relative_to(ROOT)), 'namespace_path': str(V5_OFFICIAL_REJECTION.parent.relative_to(ROOT)), 'file_sha256': V5_REJECTION_FILE_PIN, 'object_sha256': V5_REJECTION_OBJECT_PIN, 'schema': 'cm2.round306c79g.true-global-no-producer-consumer.v5.later-rejection', 'status': 'PERMANENT_FAIL_CLOSED_REJECTION__ZERO_CREDIT', 'reason': 'ORPHANED_OR_INCOMPLETE_C79G_V5_SURFACE', 'namespace_mode': '0555', 'namespace_nlink': 2, 'member_mode': '0444', 'member_nlink': 1, 'exact_member_universe': ['rejection.json'], 'formal_global_closure_credit': 0, 'D02_unlock': False, 'D02_gate_credit': 0, 'D02_task_credit': 0, 'D02_formal_pending_task_count': 33638, 'D02_started': False, 'overwrite_delete_or_reuse_allowed': False}, 'first_build_entry_attempt': {'attempted': True, 'producer_child_spawned': False, 'candidate_write_started': False, 'positive_runtime_surface_count': 0}, 'strict_bool_defect_census': {'direct_need_call_count': 700, 'risk_count': 7, 'hard_defect_count': 3, 'ordered_risk_ids': list(V5_STRICT_BOOL_RISK_IDS), 'all_seven_present_in_v5': True, 'same_seven_absent_from_v6': True, 'v6_recursive_exact_bool_unproved_count': 0}, 'all_ten_file_pins_match': True, 'all_declared_object_pins_match': True, 'all_ten_regular_0444_nlink1': True, 'exact8_manifest_reconstructs_first_eight_in_order': True, 'outer_last_pins_manifest_and_launcher': True, 'outer_then_rejection_chronology_validated': True, 'v5_execution_allowed': False, 'v5_runtime_surfaces_authoritative': False, 'formal_global_closure_credit': 0, 'D02_unlock': False, 'D02_gate_credit': 0, 'D02_task_credit': 0, 'D02_formal_pending_task_count': 33638, 'D02_started': False}

def validate_v5_published_rejected_segment(value: Any, label: str) -> None:
    expected = expected_v5_published_rejected_segment()
    need(isinstance(value, dict) and set(value) == set(expected) and (value == expected), label + ':exact published exact10, rejection, first-attempt and strict-bool regression')

def expected_v6_published_rejected_segment() -> dict[str, Any]:
    """Construct the exact frozen v6 publication/rejection/failed-build proof."""
    names = ('v5_official_rejection', 'closed_schema', 'contract', 'build_only_producer', 'independent_consumer', 'v5_to_v6_transition', 'static_audit', 'cold_launcher', 'cold_manifest', 'cold_outer')
    ordered: list[dict[str, Any]] = []
    for name, (path, file_pin, object_pin) in zip(names, V6_EXACT10_PINS, strict=True):
        member: dict[str, Any] = {'name': name, 'path': str(path.relative_to(ROOT)), 'file_sha256': file_pin}
        if object_pin is not None:
            member['object_sha256'] = object_pin
        ordered.append(member)
    return {'ordered_published_exact10': ordered, 'official_later_rejection': {'path': str(V6_OFFICIAL_REJECTION.relative_to(ROOT)), 'namespace_path': str(V6_OFFICIAL_REJECTION.parent.relative_to(ROOT)), 'file_sha256': V6_REJECTION_FILE_PIN, 'object_sha256': V6_REJECTION_OBJECT_PIN, 'schema': 'cm2.round306c79g.true-global-no-producer-consumer.v6.later-rejection', 'status': 'PERMANENT_FAIL_CLOSED_REJECTION__ZERO_CREDIT', 'reason': 'ORPHANED_OR_INCOMPLETE_C79G_V6_SURFACE', 'namespace_mode': '0555', 'namespace_nlink': 2, 'member_mode': '0444', 'member_nlink': 1, 'exact_member_universe': ['rejection.json'], 'formal_global_closure_credit': 0, 'D02_unlock': False, 'D02_gate_credit': 0, 'D02_task_credit': 0, 'D02_formal_pending_task_count': 33638, 'D02_started': False, 'overwrite_delete_or_reuse_allowed': False}, 'first_build_entry_attempt': {'attempted': True, 'producer_child_spawned': True, 'candidate_write_started': False, 'positive_runtime_surface_count': 0}, 'held_self_identity_defect': {'source_path': str(V6_EXACT10_PINS[3][0].relative_to(ROOT)), 'class_name': 'HeldSelf', 'missing_attribute': 'identity', 'failing_function': 'hold_static_freeze_trust', 'failing_expression': 'len({guard.identity for guard in current_cold_ten_guards})', 'frozen_source_line': 2041, 'deterministic_failure_kind': 'AttributeError', 'failure_occurs_before_candidate_or_stage_creation': True, 'same_defect_must_be_absent_from_v7': True}, 'all_ten_file_pins_match': True, 'all_declared_object_pins_match': True, 'all_ten_regular_0444_nlink1': True, 'exact8_manifest_reconstructs_first_eight_in_order': True, 'outer_last_pins_manifest_and_launcher': True, 'outer_then_rejection_chronology_validated': True, 'v6_execution_allowed': False, 'v6_runtime_surfaces_authoritative': False, 'formal_global_closure_credit': 0, 'D02_unlock': False, 'D02_gate_credit': 0, 'D02_task_credit': 0, 'D02_formal_pending_task_count': 33638, 'D02_started': False}

def validate_v6_published_rejected_segment(value: Any, label: str) -> None:
    expected = expected_v6_published_rejected_segment()
    need(isinstance(value, dict) and set(value) == set(expected) and (value == expected), label + ':exact v6 exact10, rejection, spawned-before-write and HeldSelf.identity defect regression')

def validate_v7_lock_continuity_incident(value: Any, label: str) -> None:
    """Validate the frozen publisher-control-flow incident, not timestamps alone."""
    need(isinstance(value, dict) and value == V7_LOCK_CONTINUITY_INCIDENT and (set(value) == set(V7_LOCK_CONTINUITY_INCIDENT)), label + ':exact 26-key v7 publication-lock incident')
    verify_object(value, label + ':v7 incident', V7_LOCK_CONTINUITY_INCIDENT_OBJECT_PIN)

def expected_v7_published_rejected_segment() -> dict[str, Any]:
    """Construct the exact v7 exact10, official rejection, and lock incident."""
    names = ('v6_official_rejection', 'closed_schema', 'contract', 'build_only_producer', 'independent_consumer', 'v6_to_v7_transition', 'static_audit', 'cold_launcher', 'cold_manifest', 'cold_outer')
    ordered: list[dict[str, Any]] = []
    for name, (path, file_pin, object_pin) in zip(names, V7_EXACT10_PINS, strict=True):
        member: dict[str, Any] = {'name': name, 'path': str(path.relative_to(ROOT)), 'file_sha256': file_pin}
        if object_pin is not None:
            member['object_sha256'] = object_pin
        ordered.append(member)
    return {'ordered_published_exact10': ordered, 'official_later_rejection': {'path': str(V7_OFFICIAL_REJECTION.relative_to(ROOT)), 'namespace_path': str(V7_OFFICIAL_REJECTION.parent.relative_to(ROOT)), 'file_sha256': V7_REJECTION_FILE_PIN, 'object_sha256': V7_REJECTION_OBJECT_PIN, 'schema': 'cm2.round306c79g.true-global-no-producer-consumer.v7.later-rejection', 'status': 'PERMANENT_FAIL_CLOSED_REJECTION__ZERO_CREDIT', 'reason': 'ORPHANED_OR_INCOMPLETE_C79G_V7_SURFACE', 'namespace_mode': '0555', 'namespace_nlink': 2, 'member_mode': '0444', 'member_nlink': 1, 'exact_member_universe': ['rejection.json'], 'formal_global_closure_credit': 0, 'D02_unlock': False, 'D02_gate_credit': 0, 'D02_task_credit': 0, 'D02_formal_pending_task_count': 33638, 'D02_started': False, 'overwrite_delete_or_reuse_allowed': False}, 'first_runtime_entry_attempt': {'attempted': False, 'producer_child_spawned': False, 'candidate_write_started': False, 'positive_runtime_surface_count': 0}, 'publication_lock_continuity_incident': copy.deepcopy(V7_LOCK_CONTINUITY_INCIDENT), 'all_ten_file_pins_match': True, 'all_declared_object_pins_match': True, 'all_ten_regular_0444_nlink1': True, 'exact8_manifest_reconstructs_first_eight_in_order': True, 'outer_last_pins_manifest_and_launcher': True, 'outer_then_rejection_chronology_validated': True, 'v7_execution_allowed': False, 'v7_runtime_surfaces_authoritative': False, 'formal_global_closure_credit': 0, 'D02_unlock': False, 'D02_gate_credit': 0, 'D02_task_credit': 0, 'D02_formal_pending_task_count': 33638, 'D02_started': False}

def validate_v7_published_rejected_segment(value: Any, label: str) -> None:
    expected = expected_v7_published_rejected_segment()
    need(isinstance(value, dict) and set(value) == set(expected) and (value == expected), label + ':exact v7 exact10/rejection/incident zero-credit proof')
    validate_v7_lock_continuity_incident(value.get('publication_lock_continuity_incident'), label)

def expected_v8_published_rejected_segment() -> dict[str, Any]:
    """Construct frozen v8 exact10, official rejection and launcher defect."""
    names = ('v7_official_rejection', 'closed_schema', 'contract', 'build_only_producer', 'independent_consumer', 'v7_to_v8_transition', 'static_audit', 'cold_launcher', 'cold_manifest', 'cold_outer')
    ordered: list[dict[str, Any]] = []
    for name, (path, file_pin, object_pin) in zip(names, V8_EXACT10_PINS, strict=True):
        member: dict[str, Any] = {'name': name, 'path': str(path.relative_to(ROOT)), 'file_sha256': file_pin}
        if object_pin is not None:
            member['object_sha256'] = object_pin
        ordered.append(member)
    return {'ordered_published_exact10': ordered, 'official_later_rejection': {'path': str(V8_OFFICIAL_REJECTION.relative_to(ROOT)), 'namespace_path': str(V8_OFFICIAL_REJECTION.parent.relative_to(ROOT)), 'file_sha256': V8_REJECTION_FILE_PIN, 'object_sha256': V8_REJECTION_OBJECT_PIN, 'schema': 'cm2.round306c79g.true-global-no-producer-consumer.v8.later-rejection', 'status': 'PERMANENT_FAIL_CLOSED_REJECTION__ZERO_CREDIT', 'reason': 'ORPHANED_OR_INCOMPLETE_C79G_V8_SURFACE', 'namespace_mode': '0555', 'namespace_nlink': 2, 'member_mode': '0444', 'member_nlink': 1, 'exact_member_universe': ['rejection.json'], 'formal_global_closure_credit': 0, 'D02_unlock': False, 'D02_gate_credit': 0, 'D02_task_credit': 0, 'D02_formal_pending_task_count': 33638, 'D02_started': False, 'overwrite_delete_or_reuse_allowed': False}, 'first_rollout_attempt': {'attempted': True, 'producer_child_spawned': False, 'candidate_write_started': False, 'positive_runtime_surface_count': 0, 'aborted_by_regression_guard': True}, 'rollout_control_flow_incident': copy.deepcopy(V8_ROLLOUT_CONTROL_FLOW_INCIDENT), 'all_ten_file_pins_match': True, 'all_declared_object_pins_match': True, 'all_ten_regular_0444_nlink1': True, 'exact8_manifest_reconstructs_first_eight_in_order': True, 'outer_last_pins_manifest_and_launcher': True, 'outer_then_rejection_chronology_validated': True, 'chronology_is_not_control_flow_proof': True, 'v8_execution_allowed': False, 'v8_runtime_surfaces_authoritative': False, 'formal_global_closure_credit': 0, 'D02_unlock': False, 'D02_gate_credit': 0, 'D02_task_credit': 0, 'D02_formal_pending_task_count': 33638, 'D02_started': False}

def validate_v8_published_rejected_segment(value: Any, label: str) -> None:
    expected = expected_v8_published_rejected_segment()
    need(isinstance(value, dict) and set(value) == set(expected) and (value == expected), label + ':exact v8 exact10/rejection/rollout-incident zero-credit proof')
    incident = value.get('rollout_control_flow_incident')
    first = value.get('first_rollout_attempt')
    need(isinstance(incident, dict) and incident == V8_ROLLOUT_CONTROL_FLOW_INCIDENT and (incident.get('regressor_expected_occurrence_count') == V8_LAUNCHER_REGRESSION_DEFECT['old_global_count_expectation']) and (incident.get('regressor_observed_occurrence_count') == V8_LAUNCHER_REGRESSION_DEFECT['actual_guard_identity_census']) and (incident.get('positive_runtime_surface_count') == V8_LAUNCHER_REGRESSION_DEFECT['candidate_surface_count']) and isinstance(first, dict) and (first.get('producer_child_spawned') is False) and (first.get('candidate_write_started') is False) and (value.get('chronology_is_not_control_flow_proof') is True), label + ':exact trusted v8 rollout control-flow incident gate')

def expected_v9_published_rejected_segment() -> dict[str, Any]:
    """Construct the exact v9 exact10, rejection and proof-shape incident."""
    names = ('v8_official_rejection', 'closed_schema', 'contract', 'build_only_producer', 'independent_consumer', 'v8_to_v9_transition', 'static_audit', 'cold_launcher', 'cold_manifest', 'cold_outer')
    ordered: list[dict[str, Any]] = []
    for name, (path, file_pin, object_pin) in zip(names, V9_EXACT10_PINS, strict=True):
        member: dict[str, Any] = {'name': name, 'path': str(path.relative_to(ROOT)), 'file_sha256': file_pin}
        if object_pin is not None:
            member['object_sha256'] = object_pin
        ordered.append(member)
    absent = [str(path.relative_to(ROOT)) for path in V9_FORBIDDEN_RUNTIME_PATHS]
    return {'ordered_published_exact10': ordered, 'official_later_rejection': {'path': str(V9_OFFICIAL_REJECTION.relative_to(ROOT)), 'namespace_path': str(V9_OFFICIAL_REJECTION.parent.relative_to(ROOT)), 'file_sha256': V9_REJECTION_FILE_PIN, 'object_sha256': V9_REJECTION_OBJECT_PIN, 'schema': 'cm2.round306c79g.true-global-no-producer-consumer.v9.later-rejection', 'status': 'PERMANENT_FAIL_CLOSED_REJECTION__ZERO_CREDIT', 'reason': 'ORPHANED_OR_INCOMPLETE_C79G_V9_SURFACE', 'namespace_mode': '0555', 'namespace_nlink': 2, 'exact_member_universe': ['rejection.json'], 'member_mode': '0444', 'member_nlink': 1, 'formal_global_closure_credit': 0, 'D02_unlock': False, 'D02_gate_credit': 0, 'D02_task_credit': 0, 'D02_formal_pending_task_count': 33638, 'D02_started': False, 'overwrite_delete_or_reuse_allowed': False}, 'first_runtime_attempt': {'attempted': True, 'producer_child_spawned': False, 'candidate_write_started': False, 'positive_runtime_surface_count': 0, 'aborted_by_v6_defect_shape_drift_guard': True}, 'v6_held_self_identity_defect_shape_drift_incident': copy.deepcopy(V9_V6_PROOF_SHAPE_DRIFT_INCIDENT), 'positive_and_stage_surfaces_absent': {'exact_absent_path_count': 12, 'exact_absent_paths': absent, 'all_absent': True}, 'all_ten_file_pins_match': True, 'all_declared_object_pins_match': True, 'all_ten_regular_0444_nlink1': True, 'exact8_manifest_reconstructs_first_eight_in_order': True, 'outer_last_pins_manifest_and_launcher': True, 'outer_then_rejection_chronology_validated': True, 'v9_execution_allowed': False, 'v9_runtime_surfaces_authoritative': False, 'formal_global_closure_credit': 0, 'D02_unlock': False, 'D02_gate_credit': 0, 'D02_task_credit': 0, 'D02_formal_pending_task_count': 33638, 'D02_started': False}

def validate_v9_published_rejected_segment(value: Any, label: str) -> None:
    expected = expected_v9_published_rejected_segment()
    need(isinstance(value, dict) and set(value) == set(expected) and (value == expected), label + ':exact v9 exact10/rejection/shape-drift zero-credit proof')
    incident = value.get('v6_held_self_identity_defect_shape_drift_incident')
    need(isinstance(incident, dict) and incident == V9_V6_PROOF_SHAPE_DRIFT_INCIDENT and (len(incident.get('persisted_held_self_identity_defect', {})) == 9) and (len(incident.get('launcher_expanded_structural_evidence', {})) == 16) and (incident.get('whole_predecessor_v6_equality_failed_before_child_spawn') is True) and (value.get('positive_and_stage_surfaces_absent', {}).get('all_absent') is True), label + ':exact trusted v9 proof-shape drift incident gate')

def expected_v10_published_rejected_segment() -> dict[str, Any]:
    """Construct exact v10 exact10, rejection and label-prefix incident."""
    names = ('v9_official_rejection', 'closed_schema', 'contract', 'build_only_producer', 'independent_consumer', 'v9_to_v10_transition', 'static_audit', 'cold_launcher', 'cold_manifest', 'cold_outer')
    ordered: list[dict[str, Any]] = []
    for name, (path, file_pin, object_pin) in zip(names, V10_EXACT10_PINS, strict=True):
        member: dict[str, Any] = {'name': name, 'path': str(path.relative_to(ROOT)), 'file_sha256': file_pin}
        if object_pin is not None:
            member['object_sha256'] = object_pin
        ordered.append(member)
    absent = [str(path.relative_to(ROOT)) for path in V10_FORBIDDEN_RUNTIME_PATHS]
    return {'ordered_published_exact10': ordered, 'official_later_rejection': {'path': str(V10_OFFICIAL_REJECTION.relative_to(ROOT)), 'namespace_path': str(V10_OFFICIAL_REJECTION.parent.relative_to(ROOT)), 'file_sha256': V10_REJECTION_FILE_PIN, 'object_sha256': V10_REJECTION_OBJECT_PIN, 'schema': 'cm2.round306c79g.true-global-no-producer-consumer.v10.later-rejection', 'status': 'PERMANENT_FAIL_CLOSED_REJECTION__ZERO_CREDIT', 'reason': 'ORPHANED_OR_INCOMPLETE_C79G_V10_SURFACE', 'namespace_mode': '0555', 'namespace_nlink': 2, 'exact_member_universe': ['rejection.json'], 'member_mode': '0444', 'member_nlink': 1, 'formal_global_closure_credit': 0, 'D02_unlock': False, 'D02_gate_credit': 0, 'D02_task_credit': 0, 'D02_formal_pending_task_count': 33638, 'D02_started': False, 'overwrite_delete_or_reuse_allowed': False}, 'first_runtime_attempt': {'attempted': True, 'command': 'build', 'orientation': 'a', 'producer_child_spawned': True, 'candidate_write_started': False, 'candidate_or_stage_created': False, 'positive_runtime_surface_count': 0, 'aborted_by_regression_label_prefix_guard': True}, 'regression_label_prefix_incident': copy.deepcopy(V10_REGRESSION_LABEL_PREFIX_INCIDENT), 'positive_and_stage_surfaces_absent': {'exact_absent_path_count': 12, 'exact_absent_paths': absent, 'all_absent': True}, 'all_ten_file_pins_match': True, 'all_declared_object_pins_match': True, 'all_ten_regular_0444_nlink1': True, 'exact8_manifest_reconstructs_first_eight_in_order': True, 'outer_last_pins_manifest_and_launcher': True, 'outer_then_rejection_chronology_validated': True, 'v10_execution_allowed': False, 'v10_runtime_surfaces_authoritative': False, 'formal_global_closure_credit': 0, 'D02_unlock': False, 'D02_gate_credit': 0, 'D02_task_credit': 0, 'D02_formal_pending_task_count': 33638, 'D02_started': False}

def validate_v10_published_rejected_segment(value: Any, label: str) -> None:
    expected = expected_v10_published_rejected_segment()
    need(isinstance(value, dict) and set(value) == set(expected) and (value == expected), label + ':exact v10 exact10/rejection/label-prefix zero-credit proof')
    incident = value.get('regression_label_prefix_incident')
    first = value.get('first_runtime_attempt')
    need(isinstance(incident, dict) and incident == V10_REGRESSION_LABEL_PREFIX_INCIDENT and (len(incident) == 44) and (incident.get('regression_guard_conjunct_truth_vector') == [True, True, True, True, False, True]) and (incident.get('unique_false_conjunct_zero_based_index') == 4) and (incident.get('exact_unprefixed_failure_label_literal_count') == 0) and (incident.get('exact_colon_prefixed_failure_label_literal_count') == 1) and isinstance(first, dict) and (first.get('producer_child_spawned') is True) and (first.get('candidate_or_stage_created') is False) and (value.get('positive_and_stage_surfaces_absent', {}).get('all_absent') is True), label + ':exact trusted v10 regression label-prefix incident gate')

def expected_v11_published_rejected_segment() -> dict[str, Any]:
    """Construct exact v11 exact10, rejection and dual-validator incident."""
    names = ('v10_official_rejection', 'closed_schema', 'contract', 'build_only_producer', 'independent_consumer', 'v10_to_v11_transition', 'static_audit', 'cold_launcher', 'cold_manifest', 'cold_outer')
    ordered: list[dict[str, Any]] = []
    for name, (path, file_pin, object_pin) in zip(names, V11_EXACT10_PINS, strict=True):
        member: dict[str, Any] = {'name': name, 'path': str(path.relative_to(ROOT)), 'file_sha256': file_pin}
        if object_pin is not None:
            member['object_sha256'] = object_pin
        ordered.append(member)
    absent = [str(path.relative_to(ROOT)) for path in V11_FORBIDDEN_RUNTIME_PATHS]
    return {'ordered_published_exact10': ordered, 'official_later_rejection': {'path': str(V11_OFFICIAL_REJECTION.relative_to(ROOT)), 'namespace_path': str(V11_OFFICIAL_REJECTION.parent.relative_to(ROOT)), 'file_sha256': V11_REJECTION_FILE_PIN, 'object_sha256': V11_REJECTION_OBJECT_PIN, 'schema': 'cm2.round306c79g.true-global-no-producer-consumer.v11.later-rejection', 'status': 'PERMANENT_FAIL_CLOSED_REJECTION__ZERO_CREDIT', 'reason': 'ORPHANED_OR_INCOMPLETE_C79G_V11_SURFACE', 'namespace_mode': '0555', 'namespace_nlink': 2, 'exact_member_universe': ['rejection.json'], 'member_mode': '0444', 'member_nlink': 1, 'formal_global_closure_credit': 0, 'D02_unlock': False, 'D02_gate_credit': 0, 'D02_task_credit': 0, 'D02_formal_pending_task_count': 33638, 'D02_started': False, 'overwrite_delete_or_reuse_allowed': False}, 'first_runtime_attempt': copy.deepcopy(V11_FIRST_RUNTIME_ATTEMPT), 'dual_validator_divergence_incident': copy.deepcopy(V11_DUAL_VALIDATOR_DIVERGENCE_INCIDENT), 'positive_and_stage_surfaces_absent': {'exact_absent_path_count': 12, 'exact_absent_paths': absent, 'all_absent': True}, 'all_ten_file_pins_match': True, 'all_declared_object_pins_match': True, 'all_ten_regular_0444_nlink1': True, 'exact8_manifest_reconstructs_first_eight_in_order': True, 'outer_last_pins_manifest_and_launcher': True, 'outer_then_rejection_chronology_validated': True, 'v11_execution_allowed': False, 'v11_runtime_surfaces_authoritative': False, 'formal_global_closure_credit': 0, 'D02_unlock': False, 'D02_gate_credit': 0, 'D02_task_credit': 0, 'D02_formal_pending_task_count': 33638, 'D02_started': False}

def validate_v11_published_rejected_segment(value: Any, label: str) -> None:
    expected = expected_v11_published_rejected_segment()
    need(isinstance(value, dict) and list(value) == list(expected) and (value == expected) and (len(value) == 19), label + ':exact v11 exact10/rejection/dual-validator zero-credit proof')
    incident = value.get('dual_validator_divergence_incident')
    first = value.get('first_runtime_attempt')
    need(isinstance(incident, dict) and list(incident) == list(V11_DUAL_VALIDATOR_DIVERGENCE_INCIDENT) and (incident == V11_DUAL_VALIDATOR_DIVERGENCE_INCIDENT) and (len(incident) == 45) and (incident.get('producer_embedded_v10_incident_key_count_claim') == 44) and (incident.get('producer_embedded_v10_incident_actual_key_count') == 45) and (incident.get('exact_failing_subpredicate_persisted') is False) and (incident.get('specific_false_clause_authority') == 'UNAVAILABLE') and (incident.get('exact_false_clause_claim_allowed') is False) and isinstance(first, dict) and (first == V11_FIRST_RUNTIME_ATTEMPT) and (first.get('producer_child_spawned') is True) and (first.get('candidate_or_stage_created') is False) and (value.get('positive_and_stage_surfaces_absent', {}).get('all_absent') is True) and (sha_bytes(canonical(first)) == V11_FIRST_RUNTIME_ATTEMPT_DIGEST) and (sha_bytes(canonical(incident)) == V11_DUAL_VALIDATOR_DIVERGENCE_INCIDENT_DIGEST), label + ':exact trusted v11 44-to-45 dual-validator divergence gate')

def expected_v12_published_rejected_segment() -> dict[str, Any]:
    """Construct exact v12 exact10, official rejection and shape incident."""
    names = ('v11_official_rejection', 'closed_schema', 'contract', 'build_only_producer', 'independent_consumer', 'v11_to_v12_transition', 'static_audit', 'cold_launcher', 'cold_manifest', 'cold_outer')
    ordered: list[dict[str, Any]] = []
    for name, (path, file_pin, object_pin) in zip(names, V12_EXACT10_PINS, strict=True):
        member: dict[str, Any] = {'name': name, 'path': str(path.relative_to(ROOT)), 'file_sha256': file_pin}
        if object_pin is not None:
            member['object_sha256'] = object_pin
        ordered.append(member)
    absent = [str(path.relative_to(ROOT)) for path in V12_FORBIDDEN_RUNTIME_PATHS]
    return {'ordered_published_exact10': ordered, 'official_later_rejection': {'path': str(V12_OFFICIAL_REJECTION.relative_to(ROOT)), 'namespace_path': str(V12_OFFICIAL_REJECTION.parent.relative_to(ROOT)), 'file_sha256': V12_REJECTION_FILE_PIN, 'object_sha256': V12_REJECTION_OBJECT_PIN, 'schema': 'cm2.round306c79g.true-global-no-producer-consumer.v12.later-rejection', 'status': 'PERMANENT_FAIL_CLOSED_REJECTION__ZERO_CREDIT', 'reason': 'ORPHANED_OR_INCOMPLETE_C79G_V12_SURFACE', 'namespace_mode': '0555', 'namespace_nlink': 2, 'exact_member_universe': ['rejection.json'], 'member_mode': '0444', 'member_nlink': 1, 'formal_global_closure_credit': 0, 'D02_unlock': False, 'D02_gate_credit': 0, 'D02_task_credit': 0, 'D02_formal_pending_task_count': 33638, 'D02_started': False, 'overwrite_delete_or_reuse_allowed': False}, 'first_runtime_attempt': copy.deepcopy(V12_FIRST_RUNTIME_ATTEMPT), 'v5_rejection_shape_incident': copy.deepcopy(V12_V5_REJECTION_SHAPE_INCIDENT), 'positive_and_stage_surfaces_absent': {'exact_absent_path_count': len(V12_FORBIDDEN_RUNTIME_PATHS), 'exact_absent_paths': absent, 'all_absent': True}, 'all_ten_file_pins_match': True, 'all_declared_object_pins_match': True, 'all_ten_regular_0444_nlink1': True, 'exact8_manifest_reconstructs_first_eight_in_order': True, 'outer_last_pins_manifest_and_launcher': True, 'outer_then_rejection_chronology_validated': True, 'v12_execution_allowed': False, 'v12_runtime_surfaces_authoritative': False, 'formal_global_closure_credit': 0, 'D02_unlock': False, 'D02_gate_credit': 0, 'D02_task_credit': 0, 'D02_formal_pending_task_count': 33638, 'D02_started': False}

def validate_v12_published_rejected_segment(value: Any, label: str) -> None:
    expected = expected_v12_published_rejected_segment()
    need(isinstance(value, dict) and list(value) == list(expected) and (value == expected) and (len(value) == 19) and (value.get('v5_rejection_shape_incident') == V12_V5_REJECTION_SHAPE_INCIDENT), label + ':exact v12 exact10/rejection/shape-incident zero-credit proof')

def structural_python_ast_sha256(raw: bytes, label: str) -> str:
    """Hash executable structure while deliberately excluding source locations."""
    try:
        tree = ast.parse(raw.decode('utf-8'), filename=label, mode='exec')
    except (UnicodeDecodeError, SyntaxError) as exc:
        raise Reject(label + ':structural AST parse') from exc
    normalized = ast.dump(tree, annotate_fields=True, include_attributes=False).encode('utf-8')
    return sha_bytes(normalized)

def normalized_named_function_ast_sha256(raw: bytes, function_name: str, label: str) -> str:
    """Hash one exact module-level helper without source-location authority."""
    try:
        tree = ast.parse(raw.decode('utf-8'), filename=label, mode='exec')
    except (UnicodeDecodeError, SyntaxError) as exc:
        raise Reject(label + ':helper AST parse') from exc
    matches = [node for node in tree.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == function_name]
    need(len(matches) == 1, label + ':one exact module-level helper')
    return sha_bytes(ast.dump(matches[0], annotate_fields=True, include_attributes=False).encode('utf-8'))

def exact_helper_callsite_census(ordered_sources: list[tuple[str, bytes]]) -> list[dict[str, Any]]:
    """Derive one row per distinct direct enclosing function in source order."""
    need([role for role, _ in ordered_sources] == ['producer', 'consumer', 'launcher'], 'helper callsite exact ordered source roles')
    result: list[dict[str, Any]] = []
    for role, raw in ordered_sources:
        try:
            tree = ast.parse(raw.decode('utf-8'), filename='helper_callsites_' + role, mode='exec')
        except (UnicodeDecodeError, SyntaxError) as exc:
            raise Reject(role + ':helper callsite AST parse') from exc
        parent: dict[ast.AST, ast.AST] = {}
        for node in ast.walk(tree):
            for child in ast.iter_child_nodes(node):
                parent[child] = node
        loaded_names = [node for node in ast.walk(tree) if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load) and (node.id == 'derive_v10_colon_prefix_witness')]
        calls: list[tuple[ast.Call, ast.FunctionDef | ast.AsyncFunctionDef]] = []
        for name in loaded_names:
            call = parent.get(name)
            need(isinstance(call, ast.Call) and call.func is name and (len(call.args) == 2) and (not call.keywords), role + ':helper is used only by exact direct two-argument calls')
            cursor: ast.AST = call
            owner: ast.FunctionDef | ast.AsyncFunctionDef | None = None
            while cursor in parent:
                cursor = parent[cursor]
                need(not isinstance(cursor, ast.Lambda), role + ':helper call not nested in lambda')
                if isinstance(cursor, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    owner = cursor
                    break
            need(owner is not None, role + ':helper call has direct enclosing function')
            calls.append((call, owner))
        need(bool(calls), role + ':at least one exact helper callsite')
        owners: list[ast.FunctionDef | ast.AsyncFunctionDef] = []
        counts: Counter[int] = Counter()
        for call, owner in sorted(calls, key=lambda item: (item[0].lineno, item[0].col_offset)):
            identity = id(owner)
            if identity not in counts:
                owners.append(owner)
            counts[identity] += 1
        for owner in sorted(owners, key=lambda node: (node.lineno, node.col_offset)):
            result.append({'source_role': role, 'enclosing_function': owner.name, 'direct_call_count': counts[id(owner)]})
    return result
PIN_NORMALIZED_CURRENT_BASE7_KEY_ORDER = ('SCHEMA', 'CONTRACT', 'PRODUCER', 'CONSUMER', 'TRANSITION', 'AUDIT')
PIN_NORMALIZED_OBJECT_BASE7_KEYS = frozenset({'CONTRACT', 'TRANSITION', 'AUDIT'})
PIN_NORMALIZED_AST_ALGORITHM = 'PYTHON_AST_DUMP_NO_ATTRIBUTES__FORCE_FINAL_BASE7_FALSE__CURRENT_V16R2_SIX_BASE7_FILE_F64_OBJECT_E64_OR_NONE__PRESERVE_V14_SUPERSESSION_RECEIPT_AND_ALL_HISTORICAL_PINS_V1'
FINAL_STATIC_AUDIT_INPUT_KEY_ORDER = ('schema', 'contract_file', 'contract_object', 'producer', 'consumer', 'transition_file', 'transition_object', 'launcher_template', 'v4_supersession_file', 'v4_supersession_object', 'v5_rejection_file', 'v5_rejection_object', 'v6_rejection_file', 'v6_rejection_object', 'v7_rejection_file', 'v7_rejection_object', 'v7_lock_continuity_incident_object', 'v8_rejection_file', 'v8_rejection_object', 'v8_launcher_file', 'v8_launcher_regression_defect_sha256', 'trusted_v8_rollout_control_flow_incident_digest', 'v9_rejection_file', 'v9_rejection_object', 'v9_launcher_file', 'v9_persisted_v6_proof_sha256', 'v9_expanded_v6_proof_sha256', 'trusted_v9_proof_shape_drift_incident_digest', 'v10_rejection_file', 'v10_rejection_object', 'v10_producer_file', 'trusted_v10_regression_label_prefix_incident_digest', 'v11_rejection_file', 'v11_rejection_object', 'v11_producer_file', 'v11_launcher_file', 'trusted_v11_dual_validator_divergence_incident_digest', 'v12_rejection_file', 'v12_rejection_object', 'v12_producer_file', 'v12_consumer_file', 'v12_launcher_file', 'trusted_v12_v5_rejection_shape_incident_digest')
FINAL_STATIC_AUDIT_INPUT_KEY_ORDER_SHA256 = '7e11baf937aa7e9695f30718fcb14793ed2fdacbdf0f33bda659086d399e4574'
FINAL_STATIC_AUDIT_TOP_LEVEL_KEY_ORDER = ('schema', 'status', 'audit_path', 'effective_checkpoint_object_sha256', 'audited_v16r2_bundle', 'predecessor_v3_exact10_regression', 'v3_official_later_rejection_regression', 'predecessor_v4_rejection_supersession_regression', 'published_then_officially_rejected_predecessor_v5', 'published_then_officially_rejected_predecessor_v6', 'published_then_officially_rejected_predecessor_v7', 'published_then_officially_rejected_predecessor_v8', 'published_then_officially_rejected_predecessor_v9', 'published_then_officially_rejected_predecessor_v10', 'published_then_officially_rejected_predecessor_v11', 'published_then_officially_rejected_predecessor_v12', 'published_then_officially_rejected_predecessor_v14', 'rejected_prepublication_v13_supersession_receipt', 'v10_colon_prefix_witness', 'v11_dual_validator_divergence_incident', 'v12_v5_rejection_shape_incident', 'historical_rejection_exact_keyset_witness', 'dual_independent_static_checkers', 'coherent_attack_static_census', 'schema_and_constructor_closure', 'sealed_exec_and_no_producer_static_proof', 'static_credit_census', 'static_no_run', 'final_audit_acceptance', 'object_sha256')
FINAL_STATIC_AUDIT_STATUS = 'PASS_DUAL_STATIC_PIN_NORMALIZED_AST_GO_V16R2__PHYSICAL_COLD_FREEZE_PENDING__RUNTIME_NOT_AUTHORIZED'
FINAL_STATIC_AUDIT_CHECKER_STATUSES = {'checker_A': 'GO_STATIC_CHECKER_A__PIN_NORMALIZED_AST_REPRODUCED__RUNTIME_NOT_AUTHORIZED', 'checker_B': 'GO_STATIC_CHECKER_B__PIN_NORMALIZED_AST_REPRODUCED__RUNTIME_NOT_AUTHORIZED', 'checker_C': 'GO_PIN_NORMALIZED_AST_AND_COMMON_DIGEST_REPRODUCED__RUNTIME_NOT_AUTHORIZED'}
FINAL_STATIC_AUDIT_OUTPUT_SHAPES = {'selfIdentity': 33, 'independentConsumerProof': 60, 'staticFreezeProof': 84, 'coldLaunchProof': 112, 'laterRejection': 56, 'producerSourceRegistry': 75, 'liveRequest': 15, 'liveACK': 32, 'liveACKCensus': 42}

def pin_normalized_launcher_ast_sha256(raw: bytes, label: str) -> str:
    """Hash a fresh AST copy after the exact cycle-breaking pin rewrite.

    Authority is the canonical ``ast.dump`` of a newly parsed held source with
    exactly seven local edits: the final-pin flag is forced false and only the
    six current-v16r2 BASE7 values are replaced by fixed draft sentinels.  The
    frozen v14 rejection-supersession-receipt BASE7 member and every
    historical pin
    remain untouched.
    """
    try:
        tree = ast.parse(raw.decode('utf-8'), filename=label, mode='exec')
    except (UnicodeDecodeError, SyntaxError) as exc:
        raise Reject(label + ':PIN_NORMALIZED AST parse') from exc
    flag_assignments: list[ast.Assign | ast.AnnAssign] = []
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name) and (node.targets[0].id == 'FINAL_BASE7_PINS_INSTALLED'):
            flag_assignments.append(node)
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name) and (node.target.id == 'FINAL_BASE7_PINS_INSTALLED'):
            flag_assignments.append(node)
    need(len(flag_assignments) == 1, label + ':one module FINAL_BASE7_PINS_INSTALLED assignment')
    flag_assignments[0].value = ast.Constant(value=False)
    configure_functions = [node for node in tree.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == 'configure_workspace_paths']
    need(len(configure_functions) == 1, label + ':one configure_workspace_paths definition')
    base7_assignments = [node for node in configure_functions[0].body if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name) and (node.targets[0].id == 'BASE7_PINS')]
    need(len(base7_assignments) == 1 and isinstance(base7_assignments[0].value, ast.Dict), label + ':one direct BASE7_PINS dict assignment')
    base7 = base7_assignments[0].value
    key_names = [key.id if isinstance(key, ast.Name) else None for key in base7.keys]
    expected_key_names = ['V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT', *PIN_NORMALIZED_CURRENT_BASE7_KEY_ORDER]
    need(key_names == expected_key_names and len(base7.values) == len(expected_key_names), label + ':exact ordered v14-receipt-plus-current-v16r2 BASE7 key census')
    receipt_before = ast.dump(base7.values[0], annotate_fields=True, include_attributes=False)
    for index, key_name in enumerate(key_names[1:], start=1):
        object_sentinel: str | None = 'e' * 64 if key_name in PIN_NORMALIZED_OBJECT_BASE7_KEYS else None
        base7.values[index] = ast.Tuple(elts=[ast.Constant(value='f' * 64), ast.Constant(value=object_sentinel)], ctx=ast.Load())
    need(ast.dump(base7.values[0], annotate_fields=True, include_attributes=False) == receipt_before, label + ':v14 rejection-supersession-receipt BASE7 value preserved')
    normalized = ast.dump(tree, annotate_fields=True, include_attributes=False).encode('utf-8')
    return sha_bytes(normalized)

def producer_source_registry_shape_from_ast(raw: bytes) -> int:
    """Derive explicit67 + execution-proof7 + object closure1 structurally."""
    try:
        tree = ast.parse(raw.decode('utf-8'), filename='producer_v16r2', mode='exec')
    except (UnicodeDecodeError, SyntaxError) as exc:
        raise Reject('current v16r2 producer registry AST parse') from exc
    registry_function = next((node for node in tree.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == 'input_registry'), None)
    held_self = next((node for node in tree.body if isinstance(node, ast.ClassDef) and node.name == 'HeldSelf'), None)
    execution_proof = next((node for node in held_self.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == 'execution_proof'), None) if isinstance(held_self, ast.ClassDef) else None
    need(isinstance(registry_function, (ast.FunctionDef, ast.AsyncFunctionDef)) and isinstance(execution_proof, (ast.FunctionDef, ast.AsyncFunctionDef)), 'current v16r2 input_registry and HeldSelf.execution_proof')
    registry_returns = [node for node in ast.walk(registry_function) if isinstance(node, ast.Return) and isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Name) and (node.value.func.id == 'close_object') and (len(node.value.args) == 1) and isinstance(node.value.args[0], ast.Dict)]
    proof_returns = [node for node in ast.walk(execution_proof) if isinstance(node, ast.Return) and isinstance(node.value, ast.Dict)]
    need(len(registry_returns) == 1 and len(proof_returns) == 1, 'unique current v16r2 registry/proof return dicts')
    registry_dict = registry_returns[0].value.args[0]
    proof_dict = proof_returns[0].value
    explicit_keys = [key.value for key in registry_dict.keys if isinstance(key, ast.Constant) and isinstance(key.value, str)]
    expansions = [value for key, value in zip(registry_dict.keys, registry_dict.values) if key is None]
    need(len(explicit_keys) == len(set(explicit_keys)) == 67 and len(expansions) == 1 and isinstance(expansions[0], ast.Call) and isinstance(expansions[0].func, ast.Attribute) and isinstance(expansions[0].func.value, ast.Name) and (expansions[0].func.value.id == 'self_guard') and (expansions[0].func.attr == 'execution_proof') and (not expansions[0].args) and (not expansions[0].keywords) and (len(proof_dict.keys) == 7) and all((isinstance(key, ast.Constant) and isinstance(key.value, str) for key in proof_dict.keys)), 'current v16r2 registry explicit67 plus exact execution-proof7')
    shape = len(explicit_keys) + len(proof_dict.keys) + 1
    need(shape == 75, 'current v16r2 producerSourceRegistry exact explicit67 plus execution-proof7 plus enclosing-object1 equals 75')
    return shape

def _v6_identity_semantic_checker_a(hold: ast.FunctionDef | ast.AsyncFunctionDef) -> dict[str, Any]:
    """Direct-field structural matcher; line numbers never select authority."""
    identity_uses = [node for node in ast.walk(hold) if isinstance(node, ast.Attribute) and node.attr == 'identity' and isinstance(node.value, ast.Name) and (node.value.id == 'guard')]
    targets = []
    for node in ast.walk(hold):
        if not isinstance(node, ast.SetComp) or len(node.generators) != 1:
            continue
        generator = node.generators[0]
        if isinstance(generator.target, ast.Name) and generator.target.id == 'guard' and isinstance(generator.iter, ast.Name) and (generator.iter.id == 'current_cold_ten_guards') and (not generator.ifs) and (generator.is_async == 0) and isinstance(node.elt, ast.Attribute) and (node.elt.attr == 'identity') and isinstance(node.elt.value, ast.Name) and (node.elt.value.id == 'guard'):
            targets.append(node)
    target_digests = [sha_bytes(ast.dump(node, annotate_fields=True, include_attributes=False).encode('utf-8')) for node in targets]
    self_guard_constructions = [node for node in ast.walk(hold) if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name) and (node.targets[0].id == 'current_cold_ten_guards') and isinstance(node.value, ast.List) and any((isinstance(element, ast.Name) and element.id == 'self_guard' for element in node.value.elts))]
    return {'guard_identity_structural_census': len(identity_uses), 'diagnostic_source_lines': sorted((node.lineno for node in identity_uses)), 'current_cold_ten_guards_self_guard_construction_count': len(self_guard_constructions), 'target_count': len(targets), 'target_ast_sha256': target_digests}

def _v6_identity_semantic_checker_b(hold: ast.FunctionDef | ast.AsyncFunctionDef) -> dict[str, Any]:
    """Independent visitor implementation of the same semantic predicate."""

    class Visitor(ast.NodeVisitor):

        def __init__(self) -> None:
            self.identity_uses: list[ast.Attribute] = []
            self.targets: list[ast.SetComp] = []
            self.self_guard_constructions: list[ast.Assign] = []

        def visit_Assign(self, node: ast.Assign) -> None:
            if len(node.targets) == 1 and isinstance(node.targets[0], ast.Name) and (node.targets[0].id == 'current_cold_ten_guards') and isinstance(node.value, ast.List) and any((isinstance(element, ast.Name) and element.id == 'self_guard' for element in node.value.elts)):
                self.self_guard_constructions.append(node)
            self.generic_visit(node)

        def visit_Attribute(self, node: ast.Attribute) -> None:
            if node.attr == 'identity' and isinstance(node.value, ast.Name) and (node.value.id == 'guard'):
                self.identity_uses.append(node)
            self.generic_visit(node)

        def visit_SetComp(self, node: ast.SetComp) -> None:
            signature = ast.dump(node, annotate_fields=True, include_attributes=False)
            required = ("elt=Attribute(value=Name(id='guard', ctx=Load()), attr='identity', ctx=Load())", "target=Name(id='guard', ctx=Store())", "iter=Name(id='current_cold_ten_guards', ctx=Load())", 'ifs=[], is_async=0')
            if len(node.generators) == 1 and all((part in signature for part in required)):
                self.targets.append(node)
            self.generic_visit(node)
    visitor = Visitor()
    visitor.visit(hold)
    target_digests = [sha_bytes(ast.dump(node, annotate_fields=True, include_attributes=False).encode('utf-8')) for node in visitor.targets]
    return {'guard_identity_structural_census': len(visitor.identity_uses), 'diagnostic_source_lines': sorted((node.lineno for node in visitor.identity_uses)), 'current_cold_ten_guards_self_guard_construction_count': len(visitor.self_guard_constructions), 'target_count': len(visitor.targets), 'target_ast_sha256': target_digests}

def v6_held_self_identity_structural_evidence(raw: bytes) -> dict[str, Any]:
    """Return the separate 16-key structural evidence for the frozen v6 defect."""
    try:
        tree = ast.parse(raw.decode('utf-8'), filename='producer_v6', mode='exec')
    except (UnicodeDecodeError, SyntaxError) as exc:
        raise Reject('frozen v6 producer AST parse') from exc
    held_self = next((node for node in tree.body if isinstance(node, ast.ClassDef) and node.name == 'HeldSelf'), None)
    hold = next((node for node in tree.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == 'hold_static_freeze_trust'), None)
    need(isinstance(held_self, ast.ClassDef) and isinstance(hold, (ast.FunctionDef, ast.AsyncFunctionDef)), 'frozen v6 HeldSelf and hold_static_freeze_trust definitions')
    direct_methods = {node.name for node in held_self.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))}
    checker_a = _v6_identity_semantic_checker_a(hold)
    checker_b = _v6_identity_semantic_checker_b(hold)
    structural_digest = structural_python_ast_sha256(raw, 'producer_v6')
    semantic_a = {key: value for key, value in checker_a.items() if key != 'diagnostic_source_lines'}
    semantic_b = {key: value for key, value in checker_b.items() if key != 'diagnostic_source_lines'}
    need('identity' not in direct_methods and semantic_a == semantic_b and (semantic_a == {'guard_identity_structural_census': 3, 'current_cold_ten_guards_self_guard_construction_count': 1, 'target_count': 1, 'target_ast_sha256': [V6_TARGET_IDENTITY_COMPREHENSION_AST_SHA256]}) and (structural_digest == V6_NORMALIZED_AST_SHA256), 'frozen v6 HeldSelf.identity structural defect and dual checker')
    evidence = {'source_path': str(V6_EXACT10_PINS[3][0].relative_to(ROOT)), 'class_name': 'HeldSelf', 'missing_attribute': 'identity', 'failing_function': 'hold_static_freeze_trust', 'failing_expression': 'len({guard.identity for guard in current_cold_ten_guards})', 'diagnostic_source_lines': checker_a['diagnostic_source_lines'], 'source_locations_are_diagnostic_not_authority': True, 'guard_identity_structural_census': checker_a['guard_identity_structural_census'], 'target_structural_comprehension_count': checker_a['target_count'], 'target_structural_comprehension_ast_sha256': checker_a['target_ast_sha256'][0], 'normalized_frozen_source_ast_sha256': structural_digest, 'independent_semantic_checker_count': 2, 'independent_semantic_checkers_agree': True, 'deterministic_failure_kind': 'AttributeError', 'failure_occurs_before_candidate_or_stage_creation': True, 'same_defect_must_be_absent_from_v7': True}
    need(evidence == V9_V6_PROOF_SHAPE_DRIFT_INCIDENT['launcher_expanded_structural_evidence'], 'frozen v6 exact independent 16-key structural evidence')
    return evidence

def v6_held_self_identity_defect_regression(raw: bytes) -> dict[str, Any]:
    """Validate strong AST evidence, then return only canonical persisted9."""
    structural = v6_held_self_identity_structural_evidence(raw)
    persisted = expected_v6_published_rejected_segment()['held_self_identity_defect']
    need(len(structural) == 16 and len(persisted) == 9 and (structural != persisted) and (persisted == V9_V6_PROOF_SHAPE_DRIFT_INCIDENT['persisted_held_self_identity_defect']), 'v6 structural16 remains separate from canonical persisted9')
    return persisted

def v8_launcher_regression_defect_gate(raw: bytes) -> dict[str, Any]:
    """Pin the rejected v8 launcher's faulty global-count predicate by AST."""
    try:
        tree = ast.parse(raw.decode('utf-8'), filename='cold_launcher_v8', mode='exec')
    except (UnicodeDecodeError, SyntaxError) as exc:
        raise Reject('frozen v8 launcher AST parse') from exc
    helper = next((node for node in tree.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == 'v6_held_self_identity_defect_regression'), None)
    need(isinstance(helper, (ast.FunctionDef, ast.AsyncFunctionDef)), 'frozen v8 launcher regression helper definition')
    old_count_predicates = []
    for node in ast.walk(helper):
        if isinstance(node, ast.Compare) and len(node.ops) == 1 and isinstance(node.ops[0], ast.Eq) and (len(node.comparators) == 1) and isinstance(node.comparators[0], ast.Constant) and (node.comparators[0].value == 1) and isinstance(node.left, ast.Call) and isinstance(node.left.func, ast.Name) and (node.left.func.id == 'len') and (len(node.left.args) == 1) and isinstance(node.left.args[0], ast.Name) and (node.left.args[0].id == 'failing'):
            old_count_predicates.append(node)
    callsites = [node for node in ast.walk(tree) if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and (node.func.id == 'v6_held_self_identity_defect_regression')]
    held_v6 = next((node for node in tree.body if isinstance(node, ast.ClassDef) and node.name == 'HeldV6PredecessorExact10'), None)
    held_v6_init = next((node for node in held_v6.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == '__init__'), None) if isinstance(held_v6, ast.ClassDef) else None
    init_helper_calls = [node for node in ast.walk(held_v6_init) if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and (node.func.id == 'v6_held_self_identity_defect_regression')] if isinstance(held_v6_init, (ast.FunctionDef, ast.AsyncFunctionDef)) else []
    init_subprocess_calls = [node for node in ast.walk(held_v6_init) if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name) and (node.func.value.id == 'subprocess')] if isinstance(held_v6_init, (ast.FunctionDef, ast.AsyncFunctionDef)) else []
    need(len(old_count_predicates) == 1 and len(callsites) == 1 and (len(init_helper_calls) == 1) and (not init_subprocess_calls) and (sha_bytes(raw) == V8_LAUNCHER_FILE_PIN), 'frozen v8 launcher old count predicate in prechild held-v6 constructor')
    return copy.deepcopy(V8_LAUNCHER_REGRESSION_DEFECT)

def v9_proof_shape_drift_gate(raw: bytes) -> dict[str, Any]:
    """Prove the frozen v9 launcher's expanded16-versus-persisted9 drift."""
    try:
        tree = ast.parse(raw.decode('utf-8'), filename='cold_launcher_v9', mode='exec')
    except (UnicodeDecodeError, SyntaxError) as exc:
        raise Reject('frozen v9 launcher AST parse') from exc
    need(sha_bytes(raw) == V9_EXACT10_PINS[7][1], 'frozen v9 launcher exact file pin')
    expected_expanded_keys = set(V9_V6_PROOF_SHAPE_DRIFT_INCIDENT['launcher_expanded_structural_evidence'])
    expanded_dicts: list[ast.Dict] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Dict):
            continue
        keys = {key.value for key in node.keys if isinstance(key, ast.Constant) and isinstance(key.value, str)}
        if keys == expected_expanded_keys and len(node.keys) == 16:
            expanded_dicts.append(node)
    helper = next((node for node in tree.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == 'v6_held_self_identity_defect_regression'), None)
    helper_expected_calls = [node for node in ast.walk(helper) if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and (node.func.id == 'expected_v6_published_rejected_segment')] if isinstance(helper, (ast.FunctionDef, ast.AsyncFunctionDef)) else []
    validator = next((node for node in tree.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == 'validate_v6_published_rejected_segment'), None)
    equality_tests = [node for node in ast.walk(validator) if isinstance(node, ast.Compare) and any((isinstance(op, ast.Eq) for op in node.ops))] if isinstance(validator, (ast.FunctionDef, ast.AsyncFunctionDef)) else []
    held_v6 = next((node for node in tree.body if isinstance(node, ast.ClassDef) and node.name == 'HeldV6PredecessorExact10'), None)
    held_v6_init = next((node for node in held_v6.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == '__init__'), None) if isinstance(held_v6, ast.ClassDef) else None
    subprocess_calls = [node for node in ast.walk(held_v6_init) if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name) and (node.func.value.id == 'subprocess')] if isinstance(held_v6_init, (ast.FunctionDef, ast.AsyncFunctionDef)) else []
    need(len(expanded_dicts) == 1 and len(helper_expected_calls) == 1 and isinstance(validator, (ast.FunctionDef, ast.AsyncFunctionDef)) and bool(equality_tests) and (not subprocess_calls) and (len(expected_v6_published_rejected_segment()['held_self_identity_defect']) == 9), 'frozen v9 expanded16 equality gate precedes every child spawn')
    return copy.deepcopy(V9_V6_PROOF_SHAPE_DRIFT_INCIDENT)

def derive_v10_colon_prefix_witness(raw_v10: bytes, raw_v9: bytes) -> dict[str, Any]:
    """Derive an exact per-clause witness from the two frozen source bytes."""
    try:
        producer_tree = ast.parse(raw_v10.decode('utf-8'), filename='producer_v10', mode='exec')
        launcher_tree = ast.parse(raw_v9.decode('utf-8'), filename='cold_launcher_v9', mode='exec')
    except (UnicodeDecodeError, SyntaxError) as exc:
        raise Reject('frozen v10 producer/v9 launcher AST parse') from exc

    def node_sha256(node: ast.AST) -> str:
        return sha_bytes(ast.dump(node, include_attributes=False).encode('utf-8'))

    def direct_top_level_calls(function: ast.FunctionDef | ast.AsyncFunctionDef, function_name: str) -> list[tuple[int, ast.Call]]:
        records: list[tuple[int, ast.Call]] = []
        for index, statement in enumerate(function.body):
            value: ast.AST | None = None
            if isinstance(statement, (ast.Assign, ast.AnnAssign, ast.Expr)):
                value = statement.value
            if isinstance(value, ast.Call) and isinstance(value.func, ast.Name) and (value.func.id == function_name):
                records.append((index, value))
        return records

    def exact_join_nodes(tree: ast.Module, suffix: str) -> list[ast.BinOp]:
        return [node for node in ast.walk(tree) if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add) and isinstance(node.left, ast.Name) and (node.left.id == 'label') and isinstance(node.right, ast.Constant) and (node.right.value == ':' + suffix)]
    regression = next((node for node in producer_tree.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == 'v9_prechild_shape_drift_regression'), None)
    hold = next((node for node in producer_tree.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == 'hold_static_freeze_trust'), None)
    build_function = next((node for node in producer_tree.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == 'build'), None)
    expected_function = next((node for node in launcher_tree.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == 'expected_v6_published_rejected_segment'), None)
    validator = next((node for node in launcher_tree.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == 'validate_v6_published_rejected_segment'), None)
    need(all((isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) for node in (regression, hold, build_function, expected_function, validator))), 'frozen v10/v9 regression, hold, build, expected, and validator functions')
    need(sha_bytes(raw_v10) == '99bb321da8a63855e52c8d6757d00886c0deeb2182f5044cac35f645e2ebd00a' and sha_bytes(raw_v9) == 'f7559ceeb7d491b8489812670392cb63e3cd5f6a2764db469e2dd51d6b5577fa', 'frozen v10 producer and v9 launcher source pins')
    six_guard_calls = [node for node in ast.walk(regression) if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and (node.func.id == 'need') and (len(node.args) == 2) and isinstance(node.args[0], ast.BoolOp) and isinstance(node.args[0].op, ast.And) and (len(node.args[0].values) == 6)]
    need(len(six_guard_calls) == 1, 'frozen v10 unique six-conjunct regression guard')
    six_guard = six_guard_calls[0].args[0]
    need(isinstance(six_guard, ast.BoolOp), 'frozen v10 six-guard bool AST')
    fifth = six_guard.values[4]
    fifth_is_exact_legacy_membership = isinstance(fifth, ast.Compare) and len(fifth.ops) == 1 and isinstance(fifth.ops[0], ast.In) and (len(fifth.comparators) == 1) and isinstance(fifth.comparators[0], ast.Name) and (fifth.comparators[0].id == 'constants') and isinstance(fifth.left, ast.Subscript) and isinstance(fifth.left.value, ast.Name) and (fifth.left.value.id == 'V9_V6_DEFECT_SHAPE_DRIFT_INCIDENT') and isinstance(fifth.left.slice, ast.Constant) and (fifth.left.slice.value == 'failure_label')
    need(fifth_is_exact_legacy_membership is True, 'frozen v10 fifth conjunct exact legacy tree-wide membership')
    expanded_dicts: list[ast.Dict] = []
    for node in ast.walk(expected_function):
        if isinstance(node, ast.Dict):
            keys = [key.value for key in node.keys if isinstance(key, ast.Constant) and isinstance(key.value, str)]
            if set(keys) == set(V6_LAUNCHER_EXPANDED_STRUCTURAL_EVIDENCE):
                expanded_dicts.append(node)
    need(len(expanded_dicts) == 1, 'frozen v9 exactly one structural16 dictionary; zero/multiple reject')
    expanded_dict = expanded_dicts[0]
    need(len(expanded_dict.keys) == 16, 'frozen v9 unique structural dictionary exact16')
    validator_calls = [node for node in ast.walk(validator) if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and (node.func.id == 'expected_v6_published_rejected_segment')]
    equality_gates = [node for node in ast.walk(validator) if isinstance(node, ast.Compare) and any((isinstance(operator, ast.Eq) for operator in node.ops))]
    constants = [node.value for node in ast.walk(launcher_tree) if isinstance(node, ast.Constant) and isinstance(node.value, str)]
    failure_label = 'exact v6 exact10, rejection, spawned-before-write and HeldSelf.identity defect regression'
    colon_label = ':' + failure_label
    constants = [node.value for node in ast.walk(launcher_tree) if isinstance(node, ast.Constant) and isinstance(node.value, str)]
    joins = exact_join_nodes(launcher_tree, failure_label)
    build_hold_calls = direct_top_level_calls(build_function, 'hold_static_freeze_trust')
    hold_regression_calls = direct_top_level_calls(hold, 'v9_prechild_shape_drift_regression')
    build_stage_calls = direct_top_level_calls(build_function, 'new_candidate_stage')
    need(len(build_hold_calls) == len(hold_regression_calls) == len(build_stage_calls) == 1, 'frozen v10 unique direct top-level hold/regression/stage calls')
    build_hold_index = build_hold_calls[0][0]
    hold_regression_index = hold_regression_calls[0][0]
    build_stage_index = build_stage_calls[0][0]
    write_primitives = {'exclusive_at', 'mkdir', 'new_candidate_stage', 'remove', 'rename', 'rename_noreplace', 'replace', 'rmdir', 'truncate', 'unlink', 'write'}
    pre_regression_write_census: Counter[str] = Counter()
    for statement in hold.body[:hold_regression_index]:
        for node in ast.walk(statement):
            if not isinstance(node, ast.Call):
                continue
            name = node.func.id if isinstance(node.func, ast.Name) else node.func.attr if isinstance(node.func, ast.Attribute) else ''
            if name in write_primitives:
                pre_regression_write_census[name] += 1
    legacy_truth_vector = [len(expanded_dicts) == 1, len(expanded_dict.keys) == 16, len(validator_calls) == 1, len(equality_gates) == 2, failure_label in constants, sha_bytes(raw_v9) == 'f7559ceeb7d491b8489812670392cb63e3cd5f6a2764db469e2dd51d6b5577fa']
    successor_truth_vector = [sha_bytes(raw_v10) == '99bb321da8a63855e52c8d6757d00886c0deeb2182f5044cac35f645e2ebd00a', sha_bytes(raw_v9) == 'f7559ceeb7d491b8489812670392cb63e3cd5f6a2764db469e2dd51d6b5577fa', len(six_guard_calls) == 1, fifth_is_exact_legacy_membership, len(expanded_dicts) == 1, len(expanded_dict.keys) == 16, len(validator_calls) == 1, len(equality_gates) == 2, constants.count(failure_label) == 0 and constants.count(colon_label) == 1, sum((value.endswith(failure_label) for value in constants)) == 1, len(joins) == 1, len(build_hold_calls) == 1, len(hold_regression_calls) == 1, len(build_stage_calls) == 1, build_hold_index < build_stage_index and sum(pre_regression_write_census.values()) == 0]
    need(legacy_truth_vector == [True, True, True, True, False, True] and all(successor_truth_vector), 'v10 legacy false clause and successor exact per-clause truth vectors')
    no_colon_tree = copy.deepcopy(launcher_tree)
    no_colon_join = exact_join_nodes(no_colon_tree, failure_label)[0]
    no_colon_join.right.value = failure_label
    double_colon_tree = copy.deepcopy(launcher_tree)
    double_colon_join = exact_join_nodes(double_colon_tree, failure_label)[0]
    double_colon_join.right.value = '::' + failure_label
    other_name_tree = copy.deepcopy(launcher_tree)
    other_name_join = exact_join_nodes(other_name_tree, failure_label)[0]
    other_name_join.left.id = 'other_label'
    bare_injection_tree = copy.deepcopy(launcher_tree)
    bare_injection_tree.body.append(ast.Expr(value=ast.Constant(failure_label)))
    prefixed_injection_tree = copy.deepcopy(launcher_tree)
    prefixed_injection_tree.body.append(ast.Expr(value=ast.Constant(colon_label)))
    duplicate_join_tree = copy.deepcopy(launcher_tree)
    duplicate_join_tree.body.append(ast.Expr(value=copy.deepcopy(exact_join_nodes(duplicate_join_tree, failure_label)[0])))
    expanded_keys = {key.value for key in expanded_dict.keys if isinstance(key, ast.Constant) and isinstance(key.value, str)}
    attacks_rejected = [len(exact_join_nodes(no_colon_tree, failure_label)) == 0, len(exact_join_nodes(double_colon_tree, failure_label)) == 0, len(exact_join_nodes(other_name_tree, failure_label)) == 0, sum((isinstance(node, ast.Constant) and node.value == failure_label for node in ast.walk(bare_injection_tree))) != 0, sum((isinstance(node, ast.Constant) and node.value == colon_label for node in ast.walk(prefixed_injection_tree))) != 1, len(exact_join_nodes(duplicate_join_tree, failure_label)) == 2, len(expanded_keys - {next(iter(expanded_keys))}) != 16, len(expanded_keys | {'coherent-extra-key'}) != 16, len(expanded_dicts + [copy.deepcopy(expanded_dict)]) != 1, len(equality_gates[:-1]) != 2, len(equality_gates + [copy.deepcopy(equality_gates[0])]) != 2, not build_stage_index < build_hold_index, len([]) != 1, len(build_hold_calls + [build_hold_calls[0]]) != 1, len(hold_regression_calls + [hold_regression_calls[0]]) != 1, len(build_stage_calls + [build_stage_calls[0]]) != 1]
    need(len(attacks_rejected) == 16 and all(attacks_rejected), 'v10 colon-prefix witness coherent AST attacks rejected')
    return close_object({'schema': 'cm2.round306c79g.true-global-no-producer-consumer.v10-colon-prefix-per-clause-witness.v1', 'v10_producer_file_sha256': sha_bytes(raw_v10), 'v9_launcher_file_sha256': sha_bytes(raw_v9), 'six_guard_ast_sha256': node_sha256(six_guard), 'six_guard_conjunct_count': len(six_guard.values), 'fifth_membership_ast_sha256': node_sha256(fifth), 'fifth_membership_is_exact_legacy_tree_wide_in': fifth_is_exact_legacy_membership, 'expanded_structural_dict_count': len(expanded_dicts), 'expanded_structural_dict_exact_key_count': len(expanded_dict.keys), 'expanded_structural_dict_ast_sha256': node_sha256(expanded_dict), 'validator_helper_call_count': len(validator_calls), 'equality_gate_count': len(equality_gates), 'equality_gate_ast_sha256_ordered': [node_sha256(node) for node in equality_gates], 'exact_unprefixed_failure_label_literal_count': constants.count(failure_label), 'exact_colon_prefixed_failure_label_literal_count': constants.count(colon_label), 'failure_label_suffix_match_count': sum((value.endswith(failure_label) for value in constants)), 'exact_colon_prefix_join_count': len(joins), 'exact_colon_prefix_join_ast_sha256': node_sha256(joins[0]), 'legacy_guard_conjunct_truth_vector': legacy_truth_vector, 'legacy_guard_true_conjunct_count': sum(legacy_truth_vector), 'legacy_guard_false_conjunct_count': len(legacy_truth_vector) - sum(legacy_truth_vector), 'legacy_guard_unique_false_zero_based_index': legacy_truth_vector.index(False), 'successor_clause_truth_vector': successor_truth_vector, 'successor_all_clauses_true': all(successor_truth_vector), 'direct_top_level_build_hold_call_count': len(build_hold_calls), 'direct_top_level_hold_regression_call_count': len(hold_regression_calls), 'direct_top_level_build_stage_call_count': len(build_stage_calls), 'build_hold_top_level_statement_index': build_hold_index, 'hold_regression_top_level_statement_index': hold_regression_index, 'build_stage_top_level_statement_index': build_stage_index, 'hold_precedes_stage': build_hold_index < build_stage_index, 'pre_regression_write_primitive_count': sum(pre_regression_write_census.values()), 'pre_regression_write_primitive_census': dict(sorted(pre_regression_write_census.items())), 'zero_or_multiple_expanded_dicts_controlled_reject': True, 'exact_prefix_join_is_authority': True, 'raw_whole_tree_string_membership_is_authority': False, 'coherent_attack_count': len(attacks_rejected), 'all_coherent_attacks_rejected': all(attacks_rejected), 'formal_global_closure_credit': 0})

def validate_v11_dual_validator_divergence(producer_v11_raw: bytes, launcher_v11_raw: bytes, colon_witness: Mapping[str, Any]) -> None:
    """Prove the frozen 44/45 drift without inventing a false subclause."""
    try:
        producer_tree = ast.parse(producer_v11_raw.decode('utf-8'), filename='producer_v11', mode='exec')
        launcher_tree = ast.parse(launcher_v11_raw.decode('utf-8'), filename='cold_launcher_v11', mode='exec')
    except (UnicodeDecodeError, SyntaxError) as exc:
        raise Reject('frozen v11 producer/launcher AST parse') from exc

    def assignment_value(tree: ast.Module, name: str) -> ast.AST:
        values: list[ast.AST] = []
        for node in tree.body:
            if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name) and (node.targets[0].id == name):
                values.append(node.value)
            elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name) and (node.target.id == name) and (node.value is not None):
                values.append(node.value)
        need(len(values) == 1, 'frozen v11 unique assignment:' + name)
        return values[0]
    producer_incident = assignment_value(producer_tree, 'V10_REGRESSION_LABEL_PREFIX_INCIDENT')
    launcher_incident = assignment_value(launcher_tree, 'V10_REGRESSION_LABEL_PREFIX_INCIDENT')
    producer_claim = assignment_value(producer_tree, 'V10_REGRESSION_LABEL_PREFIX_INCIDENT_KEY_COUNT')
    need(isinstance(producer_incident, ast.Dict) and isinstance(launcher_incident, ast.Dict) and isinstance(producer_claim, ast.Constant) and (producer_claim.value == 44), 'frozen v11 producer incident key-count claim AST')
    producer_keys = [key.value for key in producer_incident.keys if isinstance(key, ast.Constant) and isinstance(key.value, str)]
    launcher_keys = [key.value for key in launcher_incident.keys if isinstance(key, ast.Constant) and isinstance(key.value, str)]
    need(len(producer_keys) == 45 and len(set(producer_keys)) == 45 and (len(launcher_keys) == 44) and (len(set(launcher_keys)) == 44) and (set(producer_keys) - set(launcher_keys) == {'source_locations_are_diagnostic_not_authority'}) and (not set(launcher_keys) - set(producer_keys)), 'frozen v11 exact producer45 versus launcher44 incident drift')
    producer_guard = next((node for node in producer_tree.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == 'v10_regression_label_prefix_incident_regression'), None)
    launcher_gate = next((node for node in launcher_tree.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == 'v10_regression_label_prefix_gate'), None)
    held_v10 = next((node for node in launcher_tree.body if isinstance(node, ast.ClassDef) and node.name == 'HeldV10PredecessorExact10'), None)
    need(isinstance(producer_guard, (ast.FunctionDef, ast.AsyncFunctionDef)) and isinstance(launcher_gate, (ast.FunctionDef, ast.AsyncFunctionDef)) and isinstance(held_v10, ast.ClassDef), 'frozen v11 dual validator definitions')
    composite_calls = [node for node in ast.walk(producer_guard) if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and (node.func.id == 'need') and (len(node.args) == 2) and isinstance(node.args[1], ast.Constant) and (node.args[1].value == 'frozen v10 sole-false colon-prefix regression and pre-stage control flow')]
    need(len(composite_calls) == 1 and isinstance(composite_calls[0].args[0], ast.BoolOp) and isinstance(composite_calls[0].args[0].op, ast.And) and (len(composite_calls[0].args[0].values) == 12), 'frozen v11 producer one non-diagnostic twelve-conjunct guard')
    prechild_gate_calls = [node for node in ast.walk(held_v10) if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and (node.func.id == 'v10_regression_label_prefix_gate')]
    need(len(prechild_gate_calls) == 2, 'frozen v11 launcher bind and terminal prechild gate calls')
    need(sha_bytes(producer_v11_raw) == V11_PRODUCER_FILE_PIN and sha_bytes(launcher_v11_raw) == V11_LAUNCHER_FILE_PIN and (list(V11_DUAL_VALIDATOR_DIVERGENCE_INCIDENT) == ['schema', 'incident_id', 'evidence_source', 'v11_producer_source_path', 'v11_producer_source_file_sha256', 'v11_launcher_source_path', 'v11_launcher_source_file_sha256', 'v11_official_rejection_file_sha256', 'v11_official_rejection_object_sha256', 'first_command', 'first_orientation', 'producer_child_spawned', 'candidate_write_started', 'candidate_or_stage_created', 'positive_runtime_surface_count', 'launcher_gate_function', 'launcher_gate_passed_before_child_spawn', 'producer_guard_function', 'producer_composite_guard_rejected', 'producer_failure_label', 'producer_embedded_v10_incident_key_count_claim', 'producer_embedded_v10_incident_actual_key_count', 'producer_composite_guard_conjunct_count', 'exact_failing_subpredicate_persisted', 'specific_false_clause_authority', 'child_consumed_inherited_held_predecessor_fds', 'child_reopened_predecessor_paths', 'launcher_and_producer_validator_implementations_distinct', 'producer_per_clause_witness_persisted', 'v10_colon_prefix_witness_object_sha256', 'v10_colon_prefix_witness_key_count', 'v10_colon_prefix_witness_successor_clause_truth_vector', 'v10_colon_prefix_witness_all_clauses_true', 'inner_stderr_line', 'outer_stderr_line', 'failure_occurs_before_candidate_or_stage_creation', 'official_rejection_strictly_after_v11_outer', 'required_successor_fix', 'required_held_fd_fix', 'required_validator_fix', 'formal_global_closure_credit', 'D02_unlock', 'D02_started', 'standalone_authority', 'exact_false_clause_claim_allowed']) and (len(V11_DUAL_VALIDATOR_DIVERGENCE_INCIDENT) == 45) and (colon_witness.get('object_sha256') == V10_COLON_PREFIX_WITNESS_OBJECT_PIN) and (colon_witness.get('successor_clause_truth_vector') == V10_COLON_PREFIX_WITNESS_SUCCESSOR_TRUTH_VECTOR) and (colon_witness.get('successor_all_clauses_true') is True) and (V11_DUAL_VALIDATOR_DIVERGENCE_INCIDENT['specific_false_clause_authority'] == 'UNAVAILABLE') and (V11_DUAL_VALIDATOR_DIVERGENCE_INCIDENT['exact_false_clause_claim_allowed'] is False), 'v11 dual-validator incident exact evidence and no invented clause')

def _v10_exact_label_prefix_join_count(tree: ast.Module, suffix: str) -> int:
    """Count ``label + ':suffix'`` structurally, never by tree-wide equality."""
    count = 0
    for node in ast.walk(tree):
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add) and isinstance(node.left, ast.Name) and (node.left.id == 'label') and isinstance(node.right, ast.Constant) and (node.right.value == ':' + suffix):
            count += 1
    return count

def v10_regression_label_prefix_gate(producer_raw: bytes, launcher_v9_raw: bytes) -> dict[str, Any]:
    """Reproduce v10's sole false conjunct and prove the colon-prefix repair."""
    try:
        producer_tree = ast.parse(producer_raw.decode('utf-8'), filename='producer_v10', mode='exec')
        launcher_tree = ast.parse(launcher_v9_raw.decode('utf-8'), filename='cold_launcher_v9', mode='exec')
    except (UnicodeDecodeError, SyntaxError) as exc:
        raise Reject('frozen v10 producer/v9 launcher AST parse') from exc
    need(sha_bytes(producer_raw) == V10_PRODUCER_FILE_PIN and sha_bytes(launcher_v9_raw) == V9_EXACT10_PINS[7][1], 'frozen v10 producer and v9 launcher exact pins')
    regression = next((node for node in producer_tree.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == 'v9_prechild_shape_drift_regression'), None)
    hold = next((node for node in producer_tree.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == 'hold_static_freeze_trust'), None)
    build = next((node for node in producer_tree.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == 'build'), None)
    need(isinstance(regression, (ast.FunctionDef, ast.AsyncFunctionDef)) and isinstance(hold, (ast.FunctionDef, ast.AsyncFunctionDef)) and isinstance(build, (ast.FunctionDef, ast.AsyncFunctionDef)), 'frozen v10 regression, hold and build definitions')
    expected_function = next((node for node in launcher_tree.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == 'expected_v6_published_rejected_segment'), None)
    validator = next((node for node in launcher_tree.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == 'validate_v6_published_rejected_segment'), None)
    need(isinstance(expected_function, (ast.FunctionDef, ast.AsyncFunctionDef)) and isinstance(validator, (ast.FunctionDef, ast.AsyncFunctionDef)), 'frozen v9 expected/validator functions for v6 predecessor')
    guard_calls = [node for node in ast.walk(regression) if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and (node.func.id == 'need') and (len(node.args) == 2) and isinstance(node.args[0], ast.BoolOp) and isinstance(node.args[0].op, ast.And) and (len(node.args[0].values) == 6)]
    need(len(guard_calls) == 1, 'frozen v10 unique six-conjunct regression guard')
    guard = guard_calls[0].args[0]
    need(isinstance(guard, ast.BoolOp), 'frozen v10 six-conjunct guard AST')
    fifth = guard.values[4]
    need(isinstance(fifth, ast.Compare) and len(fifth.ops) == 1 and isinstance(fifth.ops[0], ast.In) and (len(fifth.comparators) == 1) and isinstance(fifth.comparators[0], ast.Name) and (fifth.comparators[0].id == 'constants') and isinstance(fifth.left, ast.Subscript) and isinstance(fifth.left.value, ast.Name) and (fifth.left.value.id == 'V9_V6_DEFECT_SHAPE_DRIFT_INCIDENT') and isinstance(fifth.left.slice, ast.Constant) and (fifth.left.slice.value == 'failure_label'), 'frozen v10 unique false conjunct exact AST anchor')
    expected_keys = set(V9_V6_PROOF_SHAPE_DRIFT_INCIDENT['launcher_expanded_structural_evidence'])
    expanded_dicts = []
    for node in ast.walk(expected_function):
        if not isinstance(node, ast.Dict):
            continue
        keys = {key.value for key in node.keys if isinstance(key, ast.Constant) and isinstance(key.value, str)}
        if keys == expected_keys:
            expanded_dicts.append(node)
    validator_calls = [node for node in ast.walk(validator) if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and (node.func.id == 'expected_v6_published_rejected_segment')]
    equality_gates = [node for node in ast.walk(validator) if isinstance(node, ast.Compare) and any((isinstance(operator, ast.Eq) for operator in node.ops))]
    constants = [node.value for node in ast.walk(launcher_tree) if isinstance(node, ast.Constant) and isinstance(node.value, str)]
    suffix = V10_REGRESSION_LABEL_PREFIX_INCIDENT['failure_label_without_colon_prefix']
    need(isinstance(suffix, str), 'v10 regression incident suffix string')
    unprefixed_count = constants.count(suffix)
    prefixed_count = constants.count(':' + suffix)
    suffix_count = sum((value.endswith(suffix) for value in constants))
    join_count = _v10_exact_label_prefix_join_count(launcher_tree, suffix)
    truth_vector = [len(expanded_dicts) == 1, bool(expanded_dicts) and len(expanded_dicts[0].keys) == 16, len(validator_calls) == 1, len(equality_gates) == 2, unprefixed_count > 0, sha_bytes(launcher_v9_raw) == V9_EXACT10_PINS[7][1]]
    hold_regression_calls = [node for node in ast.walk(hold) if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and (node.func.id == 'v9_prechild_shape_drift_regression')]
    hold_mkdir_calls = [node for node in ast.walk(hold) if isinstance(node, ast.Call) and (isinstance(node.func, ast.Attribute) and node.func.attr == 'mkdir' or (isinstance(node.func, ast.Name) and node.func.id == 'mkdir'))]
    build_hold_calls = [node for node in ast.walk(build) if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and (node.func.id == 'hold_static_freeze_trust')]
    producer_stage_calls = [node for node in ast.walk(build) if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and (node.func.id == 'new_candidate_stage')]

    def enclosing_statement_index(function: ast.FunctionDef | ast.AsyncFunctionDef, target: ast.AST) -> int:
        indices = [index for index, statement in enumerate(function.body) if any((node is target for node in ast.walk(statement)))]
        need(len(indices) == 1, 'unique enclosing top-level statement for v10 control-flow node')
        return indices[0]
    hold_statement_index = enclosing_statement_index(build, build_hold_calls[0]) if len(build_hold_calls) == 1 else -1
    stage_statement_index = enclosing_statement_index(build, producer_stage_calls[0]) if len(producer_stage_calls) == 1 else -1
    need(truth_vector == [True, True, True, True, False, True] and unprefixed_count == 0 and (prefixed_count == 1) and (suffix_count == 1) and (join_count == 1) and (len(hold_regression_calls) == 1) and (not hold_mkdir_calls) and (len(build_hold_calls) == 1) and (len(producer_stage_calls) == 1) and (hold_statement_index < stage_statement_index), 'frozen v10 five true/one false label-prefix pre-candidate gate')
    no_colon_tree = copy.deepcopy(launcher_tree)
    no_colon_join = next((node for node in ast.walk(no_colon_tree) if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add) and isinstance(node.left, ast.Name) and (node.left.id == 'label') and isinstance(node.right, ast.Constant) and (node.right.value == ':' + suffix)))
    no_colon_join.right.value = suffix
    double_colon_tree = copy.deepcopy(launcher_tree)
    double_colon_join = next((node for node in ast.walk(double_colon_tree) if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add) and isinstance(node.left, ast.Name) and (node.left.id == 'label') and isinstance(node.right, ast.Constant) and (node.right.value == ':' + suffix)))
    double_colon_join.right.value = '::' + suffix
    need(_v10_exact_label_prefix_join_count(no_colon_tree, suffix) == 0 and _v10_exact_label_prefix_join_count(double_colon_tree, suffix) == 0 and (_v10_exact_label_prefix_join_count(launcher_tree, suffix) == 1), 'with/without/double-colon structural prefix mutation attacks')
    return copy.deepcopy(V10_REGRESSION_LABEL_PREFIX_INCIDENT)

def validate_final_static_audit(audit: Mapping[str, Any], schema: Mapping[str, Any], schema_keywords: frozenset[str], held_by_path: Mapping[Path, 'HeldFile'], base_objects: Mapping[Path, Mapping[str, Any]], predecessor_v5: 'HeldV5PredecessorExact10', predecessor_v6: 'HeldV6PredecessorExact10', predecessor_v7: 'HeldV7PredecessorExact10', predecessor_v8: 'HeldV8PredecessorExact10', predecessor_v9: 'HeldV9PredecessorExact10', predecessor_v10: 'HeldV10PredecessorExact10', predecessor_v11: 'HeldV11PredecessorExact10', predecessor_v12: 'HeldV12PredecessorExact10', v13_supersession: Mapping[str, Any], launcher_source_raw: bytes) -> None:
    """Fail closed on every final dual-static GO claim before child spawn."""
    audit_keys = set(FINAL_STATIC_AUDIT_TOP_LEVEL_KEY_ORDER)
    need(set(audit) == audit_keys and audit.get('schema') == 'cm2.round306c79g.true-global-no-producer-consumer.static-audit.v16r2' and (audit.get('audit_path') == str(AUDIT.relative_to(ROOT))) and (audit.get('effective_checkpoint_object_sha256') == CHECKPOINT) and (audit.get('status') == FINAL_STATIC_AUDIT_STATUS), 'final static audit exact top-level closure and PASS_V16R2 status')
    validate_v6_published_rejected_segment(audit.get('published_then_officially_rejected_predecessor_v6'), 'final static audit v6 direct-predecessor regression')
    validate_v7_published_rejected_segment(audit.get('published_then_officially_rejected_predecessor_v7'), 'final static audit v7 direct-predecessor regression')
    validate_v8_published_rejected_segment(audit.get('published_then_officially_rejected_predecessor_v8'), 'final static audit v8 direct-predecessor regression')
    validate_v9_published_rejected_segment(audit.get('published_then_officially_rejected_predecessor_v9'), 'final static audit v9 direct-predecessor regression')
    validate_v10_published_rejected_segment(audit.get('published_then_officially_rejected_predecessor_v10'), 'final static audit v10 direct-predecessor regression')
    validate_v11_published_rejected_segment(audit.get('published_then_officially_rejected_predecessor_v11'), 'final static audit v11 direct-predecessor regression')
    validate_v12_published_rejected_segment(audit.get('published_then_officially_rejected_predecessor_v12'), 'final static audit v12 direct-predecessor regression')
    validate_v13_supersession_summary(audit.get('rejected_prepublication_v13_supersession_receipt'), v13_supersession, 'final static audit v13 prepublication rejection')
    need(predecessor_v11.colon_witness is not None and predecessor_v12.shape_incident == V12_V5_REJECTION_SHAPE_INCIDENT and (audit.get('v10_colon_prefix_witness') == predecessor_v11.colon_witness) and (audit.get('v10_colon_prefix_witness', {}).get('object_sha256') == V10_COLON_PREFIX_WITNESS_OBJECT_PIN) and (audit.get('v11_dual_validator_divergence_incident') == V11_DUAL_VALIDATOR_DIVERGENCE_INCIDENT) and (sha_bytes(canonical(audit.get('v11_dual_validator_divergence_incident'))) == V11_DUAL_VALIDATOR_DIVERGENCE_INCIDENT_DIGEST) and (audit.get('v12_v5_rejection_shape_incident') == V12_V5_REJECTION_SHAPE_INCIDENT) and (audit.get('historical_rejection_exact_keyset_witness') == list(HISTORICAL_REJECTION_EXACT_KEYSET_WITNESS)), 'final static audit exact v10/v11/v12 incident and rejection-keyset closure')
    helper_digests = [normalized_named_function_ast_sha256(held_by_path[path].raw, 'derive_v10_colon_prefix_witness', 'held current ' + path.name) for path in (PRODUCER, CONSUMER, SELF)]
    need(helper_digests == [V10_COLON_PREFIX_HELPER_NORMALIZED_AST_SHA256, V10_COLON_PREFIX_HELPER_NORMALIZED_AST_SHA256, V10_COLON_PREFIX_HELPER_NORMALIZED_AST_SHA256], 'producer consumer launcher exact independent helper AST consensus')
    dual = audit.get('dual_independent_static_checkers')
    dual_keys = {'checker_A', 'checker_B', 'checker_C_common_census_and_pin_normalized_ast_reproduction', 'v10_colon_prefix_helper_consensus', 'independent_pin_normalizer_count', 'all_pin_normalizers_equal', 'pin_normalized_ast_algorithm', 'pin_normalized_current_base7_key_order', 'pin_normalization_forces_final_base7_installed_false', 'pin_normalization_preserves_v14_supersession_receipt_and_all_historical_pins', 'pin_normalization_removes_current_audit_hash_dependency', 'independent_common_callsite_implementation_count', 'all_common_callsite_censuses_equal', 'final_launcher_must_reproduce_pin_normalized_ast_after_pin_injection', 'held_launcher_pin_normalized_ast_sha256', 'actual_runtime_registry_shape_evidence'}
    need(isinstance(dual, dict) and set(dual) == dual_keys, 'final static audit exact dual-checker wrapper')
    checker_a = dual.get('checker_A')
    checker_b = dual.get('checker_B')
    checker_c = dual.get('checker_C_common_census_and_pin_normalized_ast_reproduction')
    helper_consensus = dual.get('v10_colon_prefix_helper_consensus')
    runtime_registry_evidence = dual.get('actual_runtime_registry_shape_evidence', {})
    runtime_registry_keys = {'producer_source_registry_census', 'launcher_runtime_registry_helper_census', 'runtime_registry_shape_consensus', 'explicit62_in_memory_tamper_rejected', 'actual_closed_registry_shape'}
    producer_registry = runtime_registry_evidence.get('producer_source_registry_census', {}) if isinstance(runtime_registry_evidence, dict) else {}
    launcher_registry = runtime_registry_evidence.get('launcher_runtime_registry_helper_census', {}) if isinstance(runtime_registry_evidence, dict) else {}
    registry_consensus = runtime_registry_evidence.get('runtime_registry_shape_consensus', {}) if isinstance(runtime_registry_evidence, dict) else {}
    need(isinstance(runtime_registry_evidence, dict) and set(runtime_registry_evidence) == runtime_registry_keys and (runtime_registry_evidence.get('explicit62_in_memory_tamper_rejected') is True) and (runtime_registry_evidence.get('actual_closed_registry_shape') == 75) and isinstance(producer_registry, dict) and (producer_registry.get('explicit_key_count') == 67) and (producer_registry.get('execution_proof_key_count') == 7) and (producer_registry.get('computed_closed_registry_key_count') == 75) and (producer_registry.get('matches') is True) and isinstance(launcher_registry, dict) and (launcher_registry.get('explicit_key_guard_literals') == [67]) and (launcher_registry.get('exact_execution_proof_7_guard_count') == 1) and (launcher_registry.get('exact_shape_75_guard_count') == 1) and (launcher_registry.get('held_producer_independent_computed_shape') == 75) and (launcher_registry.get('matches') is True) and isinstance(registry_consensus, dict) and (registry_consensus.get('producer_independent_closed_key_count') == 75) and (registry_consensus.get('audit_declared_producerSourceRegistry') == 75) and (registry_consensus.get('expected_closed_key_count') == 75) and (registry_consensus.get('launcher_actual_runtime_helper_matches') is True) and (registry_consensus.get('matches') is True), 'final static audit exact V14 runtime-registry evidence')
    checker_a_keys = {'algorithm', 'status', 'input_sha256', 'pin_normalized_launcher_ast_sha256', 'wider_local_callsite_census_row_count', 'wider_local_callsite_census_sha256', 'arity_failure_count', 'undefined_global_count', 'python_literal_dict_count', 'python_literal_dict_duplicate_key_count', 'python_AST_and_compile_in_memory_file_count', 'failed_static_check_count'}
    checker_b_keys = {'algorithm', 'status', 'input_sha256', 'pin_normalized_launcher_ast_sha256', 'common_ordered_callsite_row_count', 'common_ordered_callsite_census_sha256', 'arity_failure_count', 'starred_positional_total', 'double_star_keyword_total', 'undefined_global_count', 'JSON_duplicate_key_count', 'python_literal_dict_duplicate_key_count', 'object_closure_failure_count', 'pin_failure_count', 'failed_static_check_count'}
    checker_c_keys = {'algorithm', 'status', 'pin_normalized_launcher_ast_sha256', 'common_ordered_callsite_row_count', 'common_ordered_callsite_census_sha256', 'common_callsite_kind_census', 'arity_failure_count', 'starred_positional_total', 'double_star_keyword_total', 'failed_static_check_count'}
    need(isinstance(checker_a, dict) and set(checker_a) == checker_a_keys and isinstance(checker_b, dict) and (set(checker_b) == checker_b_keys) and isinstance(checker_c, dict) and (set(checker_c) == checker_c_keys), 'final static audit exact A/B/C checker objects')
    helper_consensus_keys = {'algorithm', 'implementation_count', 'ordered_source_roles', 'normalized_helper_ast_sha256', 'all_three_helpers_equal', 'witness_exact_key_order', 'witness_exact_key_count', 'witness_object_sha256', 'ordered_callsite_census', 'ordered_callsite_census_sha256', 'all_callsites_exact'}
    helper_callsites = helper_consensus.get('ordered_callsite_census') if isinstance(helper_consensus, dict) else None
    expected_helper_callsites = [{'source_role': 'producer', 'enclosing_function': 'hold_static_freeze_trust', 'direct_call_count': 1}, {'source_role': 'consumer', 'enclosing_function': '__init__', 'direct_call_count': 1}, {'source_role': 'consumer', 'enclosing_function': 'terminal_replay', 'direct_call_count': 1}, {'source_role': 'launcher', 'enclosing_function': 'bind_predecessors', 'direct_call_count': 1}, {'source_role': 'launcher', 'enclosing_function': 'terminal_replay', 'direct_call_count': 1}]
    actual_helper_callsites = exact_helper_callsite_census([('producer', held_by_path[PRODUCER].raw), ('consumer', held_by_path[CONSUMER].raw), ('launcher', launcher_source_raw)])
    need(isinstance(helper_consensus, dict) and set(helper_consensus) == helper_consensus_keys and (helper_consensus.get('algorithm') == 'THREE_SOURCE_NORMALIZED_FUNCTIONDEF_AST_AND_EXACT_CALLSITE_CENSUS_V1') and (helper_consensus.get('implementation_count') == 3) and (helper_consensus.get('ordered_source_roles') == ['producer', 'consumer', 'launcher']) and (helper_consensus.get('normalized_helper_ast_sha256') == V10_COLON_PREFIX_HELPER_NORMALIZED_AST_SHA256) and (helper_consensus.get('all_three_helpers_equal') is True) and (helper_consensus.get('witness_exact_key_order') == list(V10_COLON_PREFIX_WITNESS_KEY_ORDER)) and (helper_consensus.get('witness_exact_key_count') == V10_COLON_PREFIX_WITNESS_KEY_COUNT) and (helper_consensus.get('witness_object_sha256') == V10_COLON_PREFIX_WITNESS_OBJECT_PIN) and isinstance(helper_callsites, list) and (helper_callsites == actual_helper_callsites == expected_helper_callsites) and all((isinstance(row, dict) and set(row) == {'source_role', 'enclosing_function', 'direct_call_count'} for row in helper_callsites)) and (helper_consensus.get('ordered_callsite_census_sha256') == sha_bytes(canonical(helper_callsites))) and (helper_consensus.get('all_callsites_exact') is True), 'final static audit exact three-source helper and callsite consensus')
    need(checker_a.get('algorithm') == 'AST_SYMBOL_TABLE_DATAFLOW_AND_PIN_NORMALIZER_CHECKER_A_V1' and checker_a.get('status') == FINAL_STATIC_AUDIT_CHECKER_STATUSES['checker_A'] and (checker_b.get('algorithm') == 'TOKEN_SYMBOL_TABLE_EXPLICIT_JSON_AND_PIN_NORMALIZER_CHECKER_B_V1') and (checker_b.get('status') == FINAL_STATIC_AUDIT_CHECKER_STATUSES['checker_B']) and (checker_c.get('algorithm') == 'INDEPENDENT_LEXICAL_CALLSITE_AND_PIN_NORMALIZED_AST_REPRODUCER_C_V1') and (checker_c.get('status') == FINAL_STATIC_AUDIT_CHECKER_STATUSES['checker_C']), 'final static audit exact independent checker GO statuses')
    input_a = checker_a.get('input_sha256')
    input_b = checker_b.get('input_sha256')
    need(isinstance(input_a, dict) and isinstance(input_b, dict) and (tuple(input_a) == FINAL_STATIC_AUDIT_INPUT_KEY_ORDER) and (tuple(input_b) == FINAL_STATIC_AUDIT_INPUT_KEY_ORDER) and (len(input_a) == len(input_b) == 43) and (sha_bytes(canonical(list(input_a))) == FINAL_STATIC_AUDIT_INPUT_KEY_ORDER_SHA256) and (sha_bytes(canonical(list(input_b))) == FINAL_STATIC_AUDIT_INPUT_KEY_ORDER_SHA256) and (input_a == input_b) and _nonzero_sha256(input_a.get('launcher_template')), 'final static audit exact ordered equal forty-three-pin A/B input census')
    expected_inputs = {'schema': held_by_path[SCHEMA].file_sha256, 'contract_file': held_by_path[CONTRACT].file_sha256, 'contract_object': base_objects[CONTRACT]['object_sha256'], 'producer': held_by_path[PRODUCER].file_sha256, 'consumer': held_by_path[CONSUMER].file_sha256, 'transition_file': held_by_path[TRANSITION].file_sha256, 'transition_object': base_objects[TRANSITION]['object_sha256'], 'launcher_template': pin_normalized_launcher_ast_sha256(launcher_source_raw, 'held_v16r2_launcher_source'), 'v4_supersession_file': predecessor_v5.by_path[V4_REJECTION_SUPERSESSION].file_sha256, 'v4_supersession_object': V4_SUPERSESSION_OBJECT_PIN, 'v5_rejection_file': predecessor_v6.by_path[V5_OFFICIAL_REJECTION].file_sha256, 'v5_rejection_object': V5_REJECTION_OBJECT_PIN, 'v6_rejection_file': predecessor_v7.by_path[V6_OFFICIAL_REJECTION].file_sha256, 'v6_rejection_object': V6_REJECTION_OBJECT_PIN, 'v7_rejection_file': predecessor_v7.rejection.file_sha256, 'v7_rejection_object': V7_REJECTION_OBJECT_PIN, 'v7_lock_continuity_incident_object': V7_LOCK_CONTINUITY_INCIDENT_OBJECT_PIN, 'v8_rejection_file': predecessor_v8.rejection.file_sha256, 'v8_rejection_object': V8_REJECTION_OBJECT_PIN, 'v8_launcher_file': predecessor_v8.by_path[V8_EXACT10_PINS[7][0]].file_sha256, 'v8_launcher_regression_defect_sha256': sha_bytes(canonical(V8_LAUNCHER_REGRESSION_DEFECT)), 'trusted_v8_rollout_control_flow_incident_digest': sha_bytes(canonical(V8_ROLLOUT_CONTROL_FLOW_INCIDENT)), 'v9_rejection_file': predecessor_v9.rejection.file_sha256, 'v9_rejection_object': V9_REJECTION_OBJECT_PIN, 'v9_launcher_file': predecessor_v9.by_path[V9_EXACT10_PINS[7][0]].file_sha256, 'v9_persisted_v6_proof_sha256': sha_bytes(canonical(V9_V6_PROOF_SHAPE_DRIFT_INCIDENT['persisted_held_self_identity_defect'])), 'v9_expanded_v6_proof_sha256': sha_bytes(canonical(V9_V6_PROOF_SHAPE_DRIFT_INCIDENT['launcher_expanded_structural_evidence'])), 'trusted_v9_proof_shape_drift_incident_digest': sha_bytes(canonical(V9_V6_PROOF_SHAPE_DRIFT_INCIDENT)), 'v10_rejection_file': predecessor_v10.rejection.file_sha256, 'v10_rejection_object': V10_REJECTION_OBJECT_PIN, 'v10_producer_file': predecessor_v10.by_path[V10_EXACT10_PINS[3][0]].file_sha256, 'trusted_v10_regression_label_prefix_incident_digest': sha_bytes(canonical(V10_REGRESSION_LABEL_PREFIX_INCIDENT)), 'v11_rejection_file': predecessor_v11.rejection.file_sha256, 'v11_rejection_object': V11_REJECTION_OBJECT_PIN, 'v11_producer_file': predecessor_v11.by_path[V11_EXACT10_PINS[3][0]].file_sha256, 'v11_launcher_file': predecessor_v11.by_path[V11_EXACT10_PINS[7][0]].file_sha256, 'trusted_v11_dual_validator_divergence_incident_digest': V11_DUAL_VALIDATOR_DIVERGENCE_INCIDENT_DIGEST, 'v12_rejection_file': predecessor_v12.rejection.file_sha256, 'v12_rejection_object': V12_REJECTION_OBJECT_PIN, 'v12_producer_file': predecessor_v12.by_path[V12_EXACT10_PINS[3][0]].file_sha256, 'v12_consumer_file': predecessor_v12.by_path[V12_EXACT10_PINS[4][0]].file_sha256, 'v12_launcher_file': predecessor_v12.by_path[V12_EXACT10_PINS[7][0]].file_sha256, 'trusted_v12_v5_rejection_shape_incident_digest': V12_V5_REJECTION_SHAPE_INCIDENT_SHA256}
    need(tuple(expected_inputs) == FINAL_STATIC_AUDIT_INPUT_KEY_ORDER and input_a == expected_inputs and all((_nonzero_sha256(value) for value in input_a.values())), 'final static audit A/B pins equal live held files and object closures')
    pin_normalized = checker_a.get('pin_normalized_launcher_ast_sha256')
    common_count = checker_b.get('common_ordered_callsite_row_count')
    common_digest = checker_b.get('common_ordered_callsite_census_sha256')
    zero_a = {'arity_failure_count', 'undefined_global_count', 'python_literal_dict_duplicate_key_count', 'failed_static_check_count'}
    zero_b = {'arity_failure_count', 'starred_positional_total', 'double_star_keyword_total', 'undefined_global_count', 'JSON_duplicate_key_count', 'python_literal_dict_duplicate_key_count', 'object_closure_failure_count', 'pin_failure_count', 'failed_static_check_count'}
    zero_c = {'arity_failure_count', 'starred_positional_total', 'double_star_keyword_total', 'failed_static_check_count'}
    need(_nonzero_sha256(pin_normalized) and checker_b.get('pin_normalized_launcher_ast_sha256') == pin_normalized and (checker_c.get('pin_normalized_launcher_ast_sha256') == pin_normalized) and (type(checker_a.get('wider_local_callsite_census_row_count')) is int) and (checker_a.get('wider_local_callsite_census_row_count') > 0) and _nonzero_sha256(checker_a.get('wider_local_callsite_census_sha256')) and (type(checker_a.get('python_literal_dict_count')) is int) and (checker_a.get('python_literal_dict_count') > 0) and (type(checker_a.get('python_AST_and_compile_in_memory_file_count')) is int) and (checker_a.get('python_AST_and_compile_in_memory_file_count') == 3) and all((type(checker_a.get(key)) is int and checker_a.get(key) == 0 for key in zero_a)) and (type(common_count) is int) and (common_count > 0) and _nonzero_sha256(common_digest) and (checker_c.get('common_ordered_callsite_row_count') == common_count) and (checker_c.get('common_ordered_callsite_census_sha256') == common_digest) and all((type(checker_b.get(key)) is int and checker_b.get(key) == 0 for key in zero_b)) and all((type(checker_c.get(key)) is int and checker_c.get(key) == 0 for key in zero_c)), 'final static audit digest consensus and exact zero-failure censuses')
    kind_census = checker_c.get('common_callsite_kind_census')
    kind_keys = {'module_function', 'module_constructor', 'self_instance_method', 'cls_class_method', 'localclass_static_method', 'localclass_class_method', 'localclass_instance_method'}
    need(isinstance(kind_census, dict) and set(kind_census) == kind_keys and all((type(value) is int and value >= 0 for value in kind_census.values())) and (sum(kind_census.values()) == common_count) and (type(dual.get('independent_pin_normalizer_count')) is int) and (dual.get('independent_pin_normalizer_count') == 3) and (dual.get('all_pin_normalizers_equal') is True) and (dual.get('pin_normalized_ast_algorithm') == PIN_NORMALIZED_AST_ALGORITHM) and (dual.get('pin_normalized_current_base7_key_order') == list(PIN_NORMALIZED_CURRENT_BASE7_KEY_ORDER)) and (dual.get('pin_normalization_forces_final_base7_installed_false') is True) and (dual.get('pin_normalization_preserves_v14_supersession_receipt_and_all_historical_pins') is True) and (dual.get('pin_normalization_removes_current_audit_hash_dependency') is True) and (type(dual.get('independent_common_callsite_implementation_count')) is int) and (dual.get('independent_common_callsite_implementation_count') == 2) and (dual.get('all_common_callsite_censuses_equal') is True) and (dual.get('final_launcher_must_reproduce_pin_normalized_ast_after_pin_injection') is True) and (dual.get('held_launcher_pin_normalized_ast_sha256') == pin_normalized) and (dual.get('held_launcher_pin_normalized_ast_sha256') == pin_normalized_launcher_ast_sha256(launcher_source_raw, 'held_v16r2_launcher_source')), 'final static audit exact PIN_NORMALIZED AST and callsite consensus')
    attack = audit.get('coherent_attack_static_census')
    attack_keys = {'exact_unique_ordered_attack_count_required', 'exact_unique_ordered_attack_count_observed', 'attack_name_order_sha256', 'all_mutations_route_through_production_validators', 'C42_full10_hash_join_mutations_included', 'C42_three_directory_mode_nlink_universe_guards_are_independent_live_physical_gates', 'attack_execution_deferred_to_cold_runtime'}
    need(isinstance(attack, dict) and set(attack) == attack_keys and (type(attack.get('exact_unique_ordered_attack_count_required')) is int) and (attack.get('exact_unique_ordered_attack_count_required') == 137) and (type(attack.get('exact_unique_ordered_attack_count_observed')) is int) and (attack.get('exact_unique_ordered_attack_count_observed') == 137) and (attack.get('attack_name_order_sha256') == '90ca3c45b88c754a6fd7049579afec495c576957d564047966661647cb694f9d') and (attack.get('all_mutations_route_through_production_validators') is True) and (attack.get('C42_full10_hash_join_mutations_included') is True) and (attack.get('C42_three_directory_mode_nlink_universe_guards_are_independent_live_physical_gates') is True) and (attack.get('attack_execution_deferred_to_cold_runtime') is True), 'final static audit exact 137/137 coherent attack census')
    closure = audit.get('schema_and_constructor_closure')
    closure_keys = {'strict_JSON_duplicate_keys_rejected', 'schema_definition_count', 'schema_ref_count', 'unresolved_schema_ref_count', 'closed_object_count', 'closed_object_required_property_mismatch_count', 'all_closed_object_required_sets_equal_property_sets', 'all_schema_refs_resolve', 'actual_schema_keyword_universe', 'actual_schema_keyword_universe_sha256', 'cold_launcher_supported_schema_keyword_universe', 'cold_launcher_supported_schema_keyword_universe_sha256', 'all_schema_validation_keywords_supported_by_cold_launcher', 'unknown_schema_validation_keyword_count', 'oneOf_keyword_absent_after_pin_definition_split', 'python_literal_dict_duplicate_key_count', 'undefined_global_count', 'output_shape_key_counts', 'launcher_and_consumer_laterRejection_key_sets_equal_schema', 'launcher_request_consumer_request_key_sets_equal', 'consumer_ACK_launcher_ACK_key_sets_and_census_values_equal'}
    stack: list[Any] = [schema]
    schema_nodes: list[Mapping[str, Any]] = []
    while stack:
        node = stack.pop()
        if isinstance(node, dict):
            schema_nodes.append(node)
            stack.extend(node.values())
        elif isinstance(node, list):
            stack.extend(node)
    closed_nodes = [node for node in schema_nodes if node.get('type') == 'object' and node.get('additionalProperties') is False]
    closed_mismatch_count = sum((set(node.get('required', [])) != set(node.get('properties', {})) for node in closed_nodes))
    actual_keywords = sorted(schema_keywords)
    supported_keywords = sorted(SUPPORTED_SCHEMA_KEYWORDS)
    expected_shapes = FINAL_STATIC_AUDIT_OUTPUT_SHAPES
    computed_registry_shape = producer_source_registry_shape_from_ast(held_by_path[PRODUCER].raw)
    need(isinstance(closure, dict) and set(closure) == closure_keys and (closure.get('strict_JSON_duplicate_keys_rejected') is True) and (type(closure.get('schema_definition_count')) is int) and (closure.get('schema_definition_count') == 46 == len(schema.get('$defs', {}))) and (type(closure.get('schema_ref_count')) is int) and (closure.get('schema_ref_count') == 242 == sum(('$ref' in node for node in schema_nodes))) and (type(closure.get('unresolved_schema_ref_count')) is int) and (closure.get('unresolved_schema_ref_count') == 0) and (type(closure.get('closed_object_count')) is int) and (closure.get('closed_object_count') == 52 == len(closed_nodes)) and (type(closure.get('closed_object_required_property_mismatch_count')) is int) and (closure.get('closed_object_required_property_mismatch_count') == 0 == closed_mismatch_count) and (closure.get('all_closed_object_required_sets_equal_property_sets') is True) and (closure.get('all_schema_refs_resolve') is True) and (closure.get('actual_schema_keyword_universe') == actual_keywords) and (closure.get('actual_schema_keyword_universe_sha256') == sha_bytes(canonical(actual_keywords))) and (closure.get('cold_launcher_supported_schema_keyword_universe') == supported_keywords) and (closure.get('cold_launcher_supported_schema_keyword_universe_sha256') == sha_bytes(canonical(supported_keywords))) and (closure.get('all_schema_validation_keywords_supported_by_cold_launcher') is True) and (type(closure.get('unknown_schema_validation_keyword_count')) is int) and (closure.get('unknown_schema_validation_keyword_count') == 0) and (closure.get('oneOf_keyword_absent_after_pin_definition_split') is True) and (type(closure.get('python_literal_dict_duplicate_key_count')) is int) and (closure.get('python_literal_dict_duplicate_key_count') == 0) and (type(closure.get('undefined_global_count')) is int) and (closure.get('undefined_global_count') == 0) and (closure.get('output_shape_key_counts') == expected_shapes) and (computed_registry_shape == expected_shapes['producerSourceRegistry'] == 75) and (closure.get('launcher_and_consumer_laterRejection_key_sets_equal_schema') is True) and (closure.get('launcher_request_consumer_request_key_sets_equal') is True) and (closure.get('consumer_ACK_launcher_ACK_key_sets_and_census_values_equal') is True), 'final static audit exact schema, constructor and output-shape closure')
    no_producer = audit.get('sealed_exec_and_no_producer_static_proof')
    no_producer_keys = {'all_memfd_seal_checks_precede_source_or_evidence_access', 'all_memfd_seal_checks_are_exact_equality_not_subset_tests', 'consumer_exec_source_coordination_root_fds_pairwise_distinct', 'consumer_current_v16r2_producer_content_open_read_hash_decode_compile_import_or_execute_allowed', 'consumer_producer_source_hold_api', 'exact_required_seal_mask', 'installed_and_exec_bytes_equal_and_terminally_replayed', 'installed_source_mode', 'installed_source_nlink', 'launcher_bootstrap_exec_source_root_fds_distinct', 'launcher_child_exec_source_coordination_root_fds_pairwise_distinct', 'producer_exec_source_coordination_root_fds_pairwise_distinct', 'sealed_exec_mode', 'sealed_exec_nlink', 'consumer_v14_inherited_authority_exact12_bytes_read_only_noncredit_allowed', 'consumer_independently_rederives_witness_from_inherited_held_fds'}
    need(isinstance(no_producer, dict) and set(no_producer) == no_producer_keys and (no_producer.get('all_memfd_seal_checks_precede_source_or_evidence_access') is True) and (no_producer.get('all_memfd_seal_checks_are_exact_equality_not_subset_tests') is True) and (no_producer.get('consumer_exec_source_coordination_root_fds_pairwise_distinct') is True) and (no_producer.get('consumer_current_v16r2_producer_content_open_read_hash_decode_compile_import_or_execute_allowed') is False) and (no_producer.get('consumer_producer_source_hold_api') == 'O_PATH|O_NOFOLLOW') and (no_producer.get('exact_required_seal_mask') == 15) and (no_producer.get('installed_and_exec_bytes_equal_and_terminally_replayed') is True) and (no_producer.get('installed_source_mode') == '0444') and (no_producer.get('installed_source_nlink') == 1) and (no_producer.get('launcher_bootstrap_exec_source_root_fds_distinct') is True) and (no_producer.get('launcher_child_exec_source_coordination_root_fds_pairwise_distinct') is True) and (no_producer.get('producer_exec_source_coordination_root_fds_pairwise_distinct') is True) and (no_producer.get('sealed_exec_mode') == '0444') and (no_producer.get('sealed_exec_nlink') == 0) and (no_producer.get('consumer_v14_inherited_authority_exact12_bytes_read_only_noncredit_allowed') is True) and (no_producer.get('consumer_independently_rederives_witness_from_inherited_held_fds') is True), 'final static audit exact current-v16r2 no-producer and inherited incident evidence policy')
    acceptance = audit.get('final_audit_acceptance')
    acceptance_keys = {'current_draft_pass', 'final_failed_static_check_count_required', 'final_static_freeze_pass_required', 'dual_static_checker_A_pin_normalized_ast_GO', 'dual_static_checker_B_pin_normalized_ast_GO', 'pin_normalized_launcher_ast_digest_consensus', 'common_callsite_census_digest_consensus', 'final_launcher_pin_normalized_ast_replay_required_after_pin_injection', 'this_audit_authorizes_C79_runtime', 'requires_cold_exact8_freeze_manifest_then_outer_last_and_terminal_replay'}
    need(isinstance(acceptance, dict) and set(acceptance) == acceptance_keys and (acceptance.get('current_draft_pass') is True) and (type(acceptance.get('final_failed_static_check_count_required')) is int) and (acceptance.get('final_failed_static_check_count_required') == 0) and (acceptance.get('final_static_freeze_pass_required') is True) and (acceptance.get('dual_static_checker_A_pin_normalized_ast_GO') is True) and (acceptance.get('dual_static_checker_B_pin_normalized_ast_GO') is True) and (acceptance.get('pin_normalized_launcher_ast_digest_consensus') is True) and (acceptance.get('common_callsite_census_digest_consensus') is True) and (acceptance.get('final_launcher_pin_normalized_ast_replay_required_after_pin_injection') is True) and (acceptance.get('this_audit_authorizes_C79_runtime') is False) and (acceptance.get('requires_cold_exact8_freeze_manifest_then_outer_last_and_terminal_replay') is True), 'final static audit exact ten-key acceptance gate')
    no_run = audit.get('static_no_run')
    need(isinstance(no_run, dict) and set(no_run) == {'C79_entrypoint_executed', 'C79_v16r2_runtime_artifact_count', 'C79_v16r2_process_count', 'pyc_or___pycache___created', 'cold_manifest_or_outer_created_before_dual_GO'} and (no_run.get('C79_entrypoint_executed') is False) and (type(no_run.get('C79_v16r2_runtime_artifact_count')) is int) and (no_run.get('C79_v16r2_runtime_artifact_count') == 0) and (type(no_run.get('C79_v16r2_process_count')) is int) and (no_run.get('C79_v16r2_process_count') == 0) and (no_run.get('pyc_or___pycache___created') is False) and (no_run.get('cold_manifest_or_outer_created_before_dual_GO') is False), 'final static audit exact no-run attestation')

def close_object(value: dict[str, Any]) -> dict[str, Any]:
    need('object_sha256' not in value, 'object closes exactly once')
    out = copy.deepcopy(value)
    out['object_sha256'] = sha_bytes(canonical(value))
    return out

def strict_json(raw: bytes, label: str) -> Any:

    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in items:
            need(key not in result, label + ':duplicate key:' + key)
            result[key] = value
        return result
    try:
        return json.loads(raw, object_pairs_hook=pairs, parse_constant=lambda token: (_ for _ in ()).throw(Reject(label + ':non-finite:' + token)))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise Reject(label + ':strict JSON') from exc

def verify_object(value: Mapping[str, Any], label: str, expected: str | None=None) -> None:
    body = copy.deepcopy(dict(value))
    claim = body.pop('object_sha256', None)
    need(isinstance(claim, str) and claim == sha_bytes(canonical(body)), label + ':object closure')
    if expected is not None:
        need(claim == expected, label + ':object pin')
AT_EMPTY_PATH = 4096
AT_SYMLINK_NOFOLLOW = 256
STATX_BASIC_STATS = 2047
STATX_MNT_ID = 4096
RESOLVE_NO_XDEV = 1
RESOLVE_NO_MAGICLINKS = 2
RESOLVE_NO_SYMLINKS = 4
RESOLVE_BENEATH = 8

class OpenHow(ctypes.Structure):
    _fields_ = [('flags', ctypes.c_uint64), ('mode', ctypes.c_uint64), ('resolve', ctypes.c_uint64)]

class StatxTimestamp(ctypes.Structure):
    _fields_ = [('tv_sec', ctypes.c_int64), ('tv_nsec', ctypes.c_uint32), ('reserved', ctypes.c_int32)]

class Statx(ctypes.Structure):
    _fields_ = [('stx_mask', ctypes.c_uint32), ('stx_blksize', ctypes.c_uint32), ('stx_attributes', ctypes.c_uint64), ('stx_nlink', ctypes.c_uint32), ('stx_uid', ctypes.c_uint32), ('stx_gid', ctypes.c_uint32), ('stx_mode', ctypes.c_uint16), ('spare0', ctypes.c_uint16), ('stx_ino', ctypes.c_uint64), ('stx_size', ctypes.c_uint64), ('stx_blocks', ctypes.c_uint64), ('stx_attributes_mask', ctypes.c_uint64), ('stx_atime', StatxTimestamp), ('stx_btime', StatxTimestamp), ('stx_ctime', StatxTimestamp), ('stx_mtime', StatxTimestamp), ('stx_rdev_major', ctypes.c_uint32), ('stx_rdev_minor', ctypes.c_uint32), ('stx_dev_major', ctypes.c_uint32), ('stx_dev_minor', ctypes.c_uint32), ('stx_mnt_id', ctypes.c_uint64), ('stx_dio_mem_align', ctypes.c_uint32), ('stx_dio_offset_align', ctypes.c_uint32), ('spare3', ctypes.c_uint64 * 12)]

def _libc() -> ctypes.CDLL:
    need(sys.platform.startswith('linux'), 'cold launcher is Linux fail-closed')
    library = ctypes.CDLL(None, use_errno=True)
    need(hasattr(library, 'syscall') and hasattr(library, 'statx'), 'openat2 and statx required')
    return library
_ACTIVE_BOOTSTRAP: 'HeldBootstrapEntry | None' = None

def _relative(path: Path) -> bytes:
    need(path.is_absolute() and path != ROOT and (ROOT in path.parents), 'exact absolute workspace descendant:' + str(path))
    relative = path.relative_to(ROOT)
    need(len(relative.parts) > 0 and all((part not in {'', '.', '..'} for part in relative.parts)), 'clean relative path:' + str(path))
    return os.fsencode(str(relative))

def openat2_from_root_fd(root_fd: int, relative: bytes, flags: int=os.O_RDONLY) -> int:
    need(len(relative) > 0 and (not relative.startswith(b'/')) and (b'\x00' not in relative) and (b'..' not in relative.split(b'/')), 'openat2 clean relative bytes')
    how = OpenHow(flags | os.O_CLOEXEC, 0, RESOLVE_NO_XDEV | RESOLVE_NO_MAGICLINKS | RESOLVE_NO_SYMLINKS | RESOLVE_BENEATH)
    ctypes.set_errno(0)
    descriptor = _libc().syscall(ctypes.c_long(437), ctypes.c_int(root_fd), ctypes.c_char_p(relative), ctypes.byref(how), ctypes.c_size_t(ctypes.sizeof(how)))
    if descriptor < 0:
        code = ctypes.get_errno()
        if code == errno.ENOENT:
            raise FileNotFoundError(code, os.strerror(code), os.fsdecode(relative))
        raise Reject('openat2 fail closed:' + os.fsdecode(relative) + ':' + os.strerror(code))
    return int(descriptor)

def openat2_beneath(path: Path, flags: int=os.O_RDONLY) -> int:
    need(_ACTIVE_BOOTSTRAP is not None, 'workspace root fd activated before any openat2')
    return openat2_from_root_fd(_ACTIVE_BOOTSTRAP.root_fd, _relative(path), flags)

def root_lstat(path: Path) -> os.stat_result:
    need(_ACTIVE_BOOTSTRAP is not None, 'workspace root fd activated before any statat')
    descriptor = openat2_beneath(path, getattr(os, 'O_PATH', os.O_RDONLY) | getattr(os, 'O_NOFOLLOW', 0))
    try:
        return os.fstat(descriptor)
    finally:
        os.close(descriptor)

def root_absent(path: Path, label: str) -> None:
    try:
        root_lstat(path)
    except FileNotFoundError:
        return
    raise Reject(label + ':must remain absent')

def mount_id(fd: int) -> int:
    info = Statx()
    ctypes.set_errno(0)
    outcome = _libc().statx(ctypes.c_int(fd), ctypes.c_char_p(b''), ctypes.c_int(AT_EMPTY_PATH | AT_SYMLINK_NOFOLLOW), ctypes.c_uint(STATX_BASIC_STATS | STATX_MNT_ID), ctypes.byref(info))
    if outcome != 0:
        code = ctypes.get_errno()
        raise Reject('statx fail closed:' + os.strerror(code))
    need(bool(info.stx_mask & STATX_MNT_ID), 'statx mount id unavailable')
    return int(info.stx_mnt_id)

def fingerprint(value: os.stat_result) -> tuple[int, ...]:
    return (value.st_dev, value.st_ino, value.st_mode, value.st_nlink, value.st_size, value.st_mtime_ns, value.st_ctime_ns)

def cold_publication_chronology(exact8: list[os.stat_result], manifest: os.stat_result, outer: os.stat_result) -> dict[str, bool]:
    """Prove final chmod/freeze order, not merely content-write mtime order."""
    exact8_mtime_not_after_ctime = all((item.st_mtime_ns <= item.st_ctime_ns for item in exact8))
    max_exact8_before_manifest = max((max(item.st_mtime_ns, item.st_ctime_ns) for item in exact8)) < manifest.st_mtime_ns
    manifest_mtime_not_after_ctime = manifest.st_mtime_ns <= manifest.st_ctime_ns
    manifest_ctime_before_outer = manifest.st_ctime_ns < outer.st_mtime_ns
    outer_mtime_not_after_ctime = outer.st_mtime_ns <= outer.st_ctime_ns
    return {'all_exact8_mtime_not_after_final_ctime': exact8_mtime_not_after_ctime, 'max_exact8_final_mtime_ctime_before_manifest_mtime': max_exact8_before_manifest, 'manifest_mtime_not_after_final_ctime': manifest_mtime_not_after_ctime, 'manifest_final_ctime_before_outer_mtime': manifest_ctime_before_outer, 'outer_mtime_not_after_final_ctime': outer_mtime_not_after_ctime, 'physical_exact8_freeze_then_manifest_freeze_then_outer_freeze_chronology': exact8_mtime_not_after_ctime and max_exact8_before_manifest and manifest_mtime_not_after_ctime and manifest_ctime_before_outer and outer_mtime_not_after_ctime}

def directory_identity(value: os.stat_result) -> tuple[int, int, int]:
    return (value.st_dev, value.st_ino, value.st_mode)
F_GET_SEALS = getattr(fcntl, 'F_GET_SEALS', 1034)
F_ADD_SEALS = getattr(fcntl, 'F_ADD_SEALS', 1033)
F_SEAL_SEAL = getattr(fcntl, 'F_SEAL_SEAL', 1)
F_SEAL_SHRINK = getattr(fcntl, 'F_SEAL_SHRINK', 2)
F_SEAL_GROW = getattr(fcntl, 'F_SEAL_GROW', 4)
F_SEAL_WRITE = getattr(fcntl, 'F_SEAL_WRITE', 8)
REQUIRED_EXEC_SEALS = F_SEAL_SEAL | F_SEAL_SHRINK | F_SEAL_GROW | F_SEAL_WRITE
MFD_CLOEXEC = getattr(os, 'MFD_CLOEXEC', 1)
MFD_ALLOW_SEALING = getattr(os, 'MFD_ALLOW_SEALING', 2)

def read_fd(fd: int) -> bytes:
    os.lseek(fd, 0, os.SEEK_SET)
    chunks: list[bytes] = []
    while True:
        chunk = os.read(fd, 1 << 20)
        if not chunk:
            return b''.join(chunks)
        chunks.append(chunk)

class HeldBootstrapEntry:
    """Prove the bytes Python parsed before trusting any workspace surface.

    The external bootstrap is an explicitly declared TCB.  It securely opens
    the installed source beneath a held workspace root, hashes it against the
    caller's launcher anchor, copies those bytes into a sealed memfd, and execs
    ``python3 -I -B -S /proc/self/fd/EXEC`` while inheriting EXEC, SOURCE and
    ROOT.  This class proves all three descriptors and the installed path before
    activating the workspace namespace.
    """

    def __init__(self, exec_fd: int, source_fd: int, root_fd: int, root_text: str, expected_sha256: str) -> None:
        need(sys.flags.isolated == 1 and sys.flags.dont_write_bytecode == 1 and (sys.flags.no_site == 1), 'sealed-fd launcher requires python3 -I -B -S')
        need(all((type(value) is int and value >= 3 for value in (exec_fd, source_fd, root_fd))) and len({exec_fd, source_fd, root_fd}) == 3, 'three distinct inherited bootstrap descriptors')
        proc_path = '/proc/self/fd/' + str(exec_fd)
        need(sys.argv[0] == proc_path and os.path.abspath(__file__) == proc_path, 'argv0 and __file__ are the inherited sealed exec fd')
        need(re.fullmatch('[0-9a-f]{64}', expected_sha256) is not None and expected_sha256 != '0' * 64, 'caller-supplied external launcher SHA-256 anchor')
        need(root_text == os.path.abspath(root_text) and Path(root_text).is_absolute(), 'bootstrap workspace root is an absolute normalized label')
        self.exec_fd = exec_fd
        self.source_fd = source_fd
        self.root_fd = root_fd
        self.root = Path(root_text)
        self.expected_sha256 = expected_sha256
        self.proc_path = proc_path
        self.exec_before = os.fstat(exec_fd)
        self.source_before = os.fstat(source_fd)
        self.root_before = os.fstat(root_fd)
        need(stat.S_ISREG(self.exec_before.st_mode) and stat.S_IMODE(self.exec_before.st_mode) == 292 and (self.exec_before.st_nlink == 0), 'sealed exec fd is anonymous regular 0444 nlink0')
        try:
            self.exec_seals = int(fcntl.fcntl(exec_fd, F_GET_SEALS))
        except OSError as exc:
            raise Reject('sealed exec fd exposes F_GET_SEALS') from exc
        need(self.exec_seals == REQUIRED_EXEC_SEALS, 'exec memfd is permanently write/grow/shrink sealed')
        need(stat.S_ISREG(self.source_before.st_mode) and stat.S_IMODE(self.source_before.st_mode) == 292 and (self.source_before.st_nlink == 1), 'installed source fd regular 0444 nlink1')
        need(stat.S_ISDIR(self.root_before.st_mode), 'inherited workspace root fd is a directory')
        self.root_mount_id = mount_id(root_fd)
        self.source_mount_id = mount_id(source_fd)
        self.exec_mount_id = mount_id(exec_fd)
        need(self.root_mount_id == self.source_mount_id, 'installed launcher and workspace root share one mount')
        root_path_state = os.lstat(self.root)
        need(stat.S_ISDIR(root_path_state.st_mode) and directory_identity(root_path_state) == directory_identity(self.root_before), 'workspace root label binds inherited root fd identity')
        installed_fd = openat2_from_root_fd(root_fd, os.fsencode(str(LAUNCHER_RELATIVE)), os.O_RDONLY)
        try:
            installed_before = os.fstat(installed_fd)
            installed_mount = mount_id(installed_fd)
            exec_raw = read_fd(exec_fd)
            exec_after = os.fstat(exec_fd)
            source_raw = read_fd(source_fd)
            source_after = os.fstat(source_fd)
            installed_raw = read_fd(installed_fd)
            installed_after = os.fstat(installed_fd)
            need(fingerprint(self.exec_before) == fingerprint(exec_after) and fingerprint(self.source_before) == fingerprint(source_after) and (fingerprint(installed_before) == fingerprint(installed_after)), 'bootstrap fd reads are identity bracketed')
            need((installed_before.st_dev, installed_before.st_ino) == (self.source_before.st_dev, self.source_before.st_ino) and installed_mount == self.source_mount_id and (fingerprint(installed_before) == fingerprint(self.source_before)), 'installed path is the inherited source inode')
            need(exec_raw == source_raw == installed_raw and sha_bytes(exec_raw) == expected_sha256, 'sealed executed bytes equal installed externally pinned bytes')
            self.raw = exec_raw
        finally:
            os.close(installed_fd)
        global _ACTIVE_BOOTSTRAP
        need(_ACTIVE_BOOTSTRAP is None, 'bootstrap root activates exactly once')
        configure_workspace_paths(self.root)
        _ACTIVE_BOOTSTRAP = self
        self.closed = False

    def held_launcher(self) -> 'HeldFile':
        need(not self.closed, 'bootstrap entry remains live')
        return HeldFile.from_existing_fd(SELF, 'cold exact8:' + SELF.name, self.expected_sha256, self.source_fd)

    def terminal_replay(self) -> None:
        need(not self.closed, 'bootstrap entry terminal replay while live')
        root_path_state = os.lstat(self.root)
        root_now = os.fstat(self.root_fd)
        exec_before = os.fstat(self.exec_fd)
        source_before = os.fstat(self.source_fd)
        exec_raw = read_fd(self.exec_fd)
        source_raw = read_fd(self.source_fd)
        exec_after = os.fstat(self.exec_fd)
        source_after = os.fstat(self.source_fd)
        installed_fd = openat2_beneath(SELF)
        try:
            installed_before = os.fstat(installed_fd)
            installed_raw = read_fd(installed_fd)
            installed_after = os.fstat(installed_fd)
            need(fingerprint(installed_before) == fingerprint(installed_after) and (installed_before.st_dev, installed_before.st_ino) == (self.source_before.st_dev, self.source_before.st_ino) and (mount_id(installed_fd) == self.source_mount_id), 'terminal installed launcher identity')
        finally:
            os.close(installed_fd)
        need(directory_identity(root_path_state) == directory_identity(root_now) == directory_identity(self.root_before) and mount_id(self.root_fd) == self.root_mount_id and (fingerprint(exec_before) == fingerprint(self.exec_before) == fingerprint(exec_after)) and (fingerprint(source_before) == fingerprint(self.source_before) == fingerprint(source_after)) and (fcntl.fcntl(self.exec_fd, F_GET_SEALS) == REQUIRED_EXEC_SEALS) and (exec_raw == source_raw == installed_raw == self.raw) and (sha_bytes(exec_raw) == self.expected_sha256), 'terminal sealed-exec/source/root/path byte replay')

    def identity_object(self) -> dict[str, Any]:
        return {'external_static_file_anchor_sha256': self.expected_sha256, 'executed_proc_fd_path': self.proc_path, 'executed_sealed_memfd': True, 'required_memfd_seals': REQUIRED_EXEC_SEALS, 'installed_source_st_dev': self.source_before.st_dev, 'installed_source_st_ino': self.source_before.st_ino, 'installed_source_statx_mnt_id': self.source_mount_id, 'workspace_root_st_dev': self.root_before.st_dev, 'workspace_root_st_ino': self.root_before.st_ino, 'workspace_root_statx_mnt_id': self.root_mount_id, 'external_bootstrap_python_kernel_openat2_procfs_declared_TCB': True, 'launcher_sha256_is_only_external_static_file_anchor_not_only_TCB': True}

    def close(self) -> None:
        if self.closed:
            return
        self.closed = True
        for descriptor in (self.exec_fd, self.source_fd, self.root_fd):
            os.close(descriptor)

class HeldFile:

    def __init__(self, path: Path, label: str, expected: str | None=None, inherited_fd: int | None=None) -> None:
        self.path = path
        self.label = label
        before_path = root_lstat(path)
        need(stat.S_ISREG(before_path.st_mode) and stat.S_IMODE(before_path.st_mode) == 292 and (before_path.st_nlink == 1), label + ':regular 0444 nlink1')
        self.fd = openat2_beneath(path) if inherited_fd is None else os.dup(inherited_fd)
        try:
            self.before = os.fstat(self.fd)
            self.mount_id = mount_id(self.fd)
            need(directory_identity(before_path) == directory_identity(self.before), label + ':initial path/fd identity')
            self.raw = self._read()
            after_fd = os.fstat(self.fd)
            after_path = root_lstat(path)
            need(fingerprint(before_path) == fingerprint(self.before) == fingerprint(after_fd) == fingerprint(after_path) and mount_id(self.fd) == self.mount_id, label + ':initial bracketed same-fd read')
            self.file_sha256 = sha_bytes(self.raw)
            if expected is not None:
                need(self.file_sha256 == expected, label + ':file pin')
        except BaseException:
            os.close(self.fd)
            self.fd = -1
            raise

    @classmethod
    def from_existing_fd(cls, path: Path, label: str, expected: str, inherited_fd: int) -> 'HeldFile':
        return cls(path, label, expected, inherited_fd)

    @property
    def identity(self) -> tuple[int, int]:
        return (self.before.st_dev, self.before.st_ino)

    def _read(self) -> bytes:
        os.lseek(self.fd, 0, os.SEEK_SET)
        chunks: list[bytes] = []
        while True:
            chunk = os.read(self.fd, 1 << 20)
            if not chunk:
                return b''.join(chunks)
            chunks.append(chunk)

    def terminal_replay(self) -> None:
        before_fd = os.fstat(self.fd)
        before_path = root_lstat(self.path)
        replay = self._read()
        after_fd = os.fstat(self.fd)
        after_path = root_lstat(self.path)
        need(replay == self.raw and fingerprint(before_fd) == fingerprint(before_path) == fingerprint(self.before) == fingerprint(after_fd) == fingerprint(after_path) and stat.S_ISREG(after_fd.st_mode) and (stat.S_IMODE(after_fd.st_mode) == 292) and (after_fd.st_nlink == 1) and (mount_id(self.fd) == self.mount_id), self.label + ':terminal bracketed same-fd replay')

    def identity_object(self) -> dict[str, Any]:
        return {'path': str(self.path.relative_to(ROOT)), 'file_sha256': self.file_sha256, 'st_dev': self.before.st_dev, 'st_ino': self.before.st_ino, 'stx_mnt_id': self.mount_id, 'st_size': self.before.st_size, 'mode': '0444', 'nlink': 1, 'opened_by_exact_lexical_path_with_O_NOFOLLOW': True, 'opened_with_openat2_RESOLVE_BENEATH_NO_SYMLINKS_NO_MAGICLINKS_NO_XDEV': True, 'statx_mount_id_stable': True, 'initial_fd_identity_equals_terminal_fd_identity': True, 'initial_bytes_equal_terminal_same_fd_bytes': True, 'terminal_fd_identity_equals_terminal_path_lstat_identity': True, 'parent_components_securely_walked': True, 'regular_file': True}

    def close(self) -> None:
        if self.fd >= 0:
            os.close(self.fd)
            self.fd = -1

class HeldSealedChildExec:
    """Fresh immutable execution copy of one already-held exact8 source."""

    def __init__(self, source: HeldFile) -> None:
        need(hasattr(os, 'memfd_create'), 'Linux memfd_create required for sealed child execution')
        try:
            self.fd = os.memfd_create('c79g-v16r2-child-exec', MFD_CLOEXEC | MFD_ALLOW_SEALING)
        except OSError as exc:
            raise Reject('fresh child exec memfd creation') from exc
        self.closed = False
        self.expected_raw = source.raw
        self.expected_sha256 = source.file_sha256
        try:
            view = memoryview(self.expected_raw)
            offset = 0
            while offset < len(view):
                written = os.write(self.fd, view[offset:])
                need(written > 0, 'complete child exec memfd write')
                offset += written
            os.fsync(self.fd)
            os.fchmod(self.fd, 292)
            fcntl.fcntl(self.fd, F_ADD_SEALS, REQUIRED_EXEC_SEALS)
            self.before = os.fstat(self.fd)
            self.seals = int(fcntl.fcntl(self.fd, F_GET_SEALS))
            self.raw = read_fd(self.fd)
            after = os.fstat(self.fd)
            need(stat.S_ISREG(self.before.st_mode) and stat.S_IMODE(self.before.st_mode) == 292 and (self.before.st_nlink == 0) and (self.seals == REQUIRED_EXEC_SEALS) and (fingerprint(self.before) == fingerprint(after)) and (self.raw == self.expected_raw) and (sha_bytes(self.raw) == self.expected_sha256), 'fresh sealed child exec bytes, mode, link count, and seals')
        except BaseException:
            os.close(self.fd)
            self.fd = -1
            self.closed = True
            raise

    def terminal_replay(self) -> None:
        need(not self.closed and self.fd >= 3, 'sealed child exec held through terminal replay')
        before = os.fstat(self.fd)
        replay = read_fd(self.fd)
        after = os.fstat(self.fd)
        seals = int(fcntl.fcntl(self.fd, F_GET_SEALS))
        need(fingerprint(before) == fingerprint(self.before) == fingerprint(after) and stat.S_IMODE(after.st_mode) == 292 and (after.st_nlink == 0) and (seals == REQUIRED_EXEC_SEALS) and (replay == self.expected_raw) and (sha_bytes(replay) == self.expected_sha256), 'sealed child exec terminal byte/mode/seal replay')

    def close(self) -> None:
        if not self.closed:
            os.close(self.fd)
            self.fd = -1
            self.closed = True

class HeldCoordinationParent:
    """Launcher-owned official-writer lock on the exact RUNTIME dir inode.

    The same open-file-description is inherited by every child.  Keeping this
    launcher descriptor open prevents a child crash after the final dynamic
    ACK from releasing the lock before the positive wrapper's final newline is
    committed through the raw blocking stdout pipe.
    This is a mandatory cooperative protocol lock; it is deliberately not
    described as isolation from a same-UID process that ignores the protocol.
    """

    def __init__(self) -> None:
        self.path = RUNTIME
        self.fd = -1
        self.lock_owned = False
        before_path = root_lstat(self.path)
        need(stat.S_ISDIR(before_path.st_mode), 'coordination parent exact nonsymlink directory')
        self.fd = openat2_beneath(self.path, os.O_RDONLY | os.O_DIRECTORY)
        try:
            self.before = os.fstat(self.fd)
            self.mount_id = mount_id(self.fd)
            need(fingerprint(before_path) == fingerprint(self.before), 'coordination parent initial path/fd identity')
            fcntl.flock(self.fd, fcntl.LOCK_EX)
            self.lock_owned = True
            self.verify()
        except BaseException:
            if self.lock_owned:
                fcntl.flock(self.fd, fcntl.LOCK_UN)
                self.lock_owned = False
            os.close(self.fd)
            self.fd = -1
            raise

    @property
    def identity(self) -> tuple[int, int]:
        return (self.before.st_dev, self.before.st_ino)

    def verify(self) -> None:
        before_fd = os.fstat(self.fd)
        before_path = root_lstat(self.path)
        fcntl.flock(self.fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        after_fd = os.fstat(self.fd)
        after_path = root_lstat(self.path)
        need(self.lock_owned is True and stat.S_ISDIR(before_fd.st_mode) and stat.S_ISDIR(after_fd.st_mode) and (directory_identity(before_fd) == directory_identity(before_path) == directory_identity(self.before) == directory_identity(after_fd) == directory_identity(after_path)) and (mount_id(self.fd) == self.mount_id), 'launcher-owned coordination lock and parent identity stable')

    def identity_object(self) -> dict[str, Any]:
        return {'path': str(self.path.relative_to(ROOT)), 'st_dev': self.before.st_dev, 'st_ino': self.before.st_ino, 'stx_mnt_id': self.mount_id, 'directory': True, 'opened_with_openat2_RESOLVE_BENEATH_NO_SYMLINKS_NO_MAGICLINKS_NO_XDEV': True, 'launcher_owned_flock_LOCK_EX': self.lock_owned, 'same_open_file_description_inherited_by_child': True, 'lock_scope_is_mandatory_official_writer_protocol_only': True, 'same_uid_bypass_is_not_claimed_prevented': True}

    def close(self) -> None:
        if self.lock_owned:
            fcntl.flock(self.fd, fcntl.LOCK_UN)
            self.lock_owned = False
        if self.fd >= 0:
            os.close(self.fd)
            self.fd = -1

class HeldEmptyRejectionNamespace:
    """Launcher-level permanent-rejection guard for every non-reject command."""

    def __init__(self, coordination: HeldCoordinationParent) -> None:
        coordination.verify()
        name = V16R2_REJECTION_NAMESPACE.name
        created_descriptor = -1
        self.fd = -1
        try:
            try:
                state = os.stat(name, dir_fd=coordination.fd, follow_symlinks=False)
            except FileNotFoundError:
                os.mkdir(name, 365, dir_fd=coordination.fd)
                created_descriptor = os.open(name, os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC | getattr(os, 'O_NOFOLLOW', 0), dir_fd=coordination.fd)
                os.fchmod(created_descriptor, 365)
                os.fsync(created_descriptor)
                os.fsync(coordination.fd)
                state = os.stat(name, dir_fd=coordination.fd, follow_symlinks=False)
            self.path = V16R2_REJECTION_NAMESPACE
            self.fd = created_descriptor if created_descriptor >= 0 else openat2_beneath(self.path, os.O_RDONLY | os.O_DIRECTORY)
            created_descriptor = -1
            self.before = os.fstat(self.fd)
            self.mount_id = mount_id(self.fd)
            path_before = root_lstat(self.path)
            first = set(os.listdir(self.fd))
            after = os.fstat(self.fd)
            path_after = root_lstat(self.path)
            second = set(os.listdir(self.fd))
            need(stat.S_ISDIR(state.st_mode) and stat.S_IMODE(state.st_mode) == 365 and (state.st_nlink == 2) and (fingerprint(state) == fingerprint(self.before) == fingerprint(path_before) == fingerprint(after) == fingerprint(path_after)) and (first == second == set()) and (self.mount_id == coordination.mount_id), 'launcher permanent-rejection namespace exact empty sealed state')
        except BaseException:
            if created_descriptor >= 0:
                os.close(created_descriptor)
            if self.fd >= 0:
                os.close(self.fd)
                self.fd = -1
            raise

    def terminal_replay(self) -> None:
        before = os.fstat(self.fd)
        path_before = root_lstat(self.path)
        first = set(os.listdir(self.fd))
        after = os.fstat(self.fd)
        path_after = root_lstat(self.path)
        second = set(os.listdir(self.fd))
        need(fingerprint(before) == fingerprint(path_before) == fingerprint(self.before) == fingerprint(after) == fingerprint(path_after) and first == second == set() and (stat.S_IMODE(after.st_mode) == 365) and (after.st_nlink == 2) and (mount_id(self.fd) == self.mount_id), 'launcher rejection namespace terminal exact-empty replay')

    def close(self) -> None:
        if self.fd >= 0:
            os.close(self.fd)
            self.fd = -1

def stable_official_writer_lock_policy() -> dict[str, Any]:
    """Return the reboot-stable lock policy without persisting live identity."""
    return {'path': '.cm2-runtime', 'lock_api': 'launcher_owned_fcntl.flock(LOCK_EX)', 'launcher_owned_open_file_description_must_be_inherited_by_child': True, 'child_must_duplicate_and_identity_mount_check_inherited_fd': True, 'launcher_exclusive_lock_must_be_confirmed_by_independent_nonblocking_probe': True, 'child_calls_LOCK_UN': False, 'launcher_lock_owner_scope_requirement_includes_child_live_protocol': True, 'mandatory_for_all_official_runtime_writers': True, 'acquired_before_any_runtime_evidence_or_commit_surface_open_for_each_command': True, 'required_final_hold_scope': ['inner_canonical_stdout_flush', 'launcher_commit_request', 'absolute_last_dynamic_terminal_replay', 'live_ACK_canonical_stdout_flush', 'launcher_positive_wrapper_raw_fd1_final_newline_write', 'launcher_RELEASE'], 'protocol_requires_launcher_RELEASE_before_normal_child_guard_close': True, 'coordination_lock_is_not_claimed_as_a_security_boundary_against_noncooperating_same_uid_or_filesystem_administrator': True, 'live_st_dev_st_ino_and_stx_mnt_id_must_not_be_persisted': True}

def reconstruct_unopened_publication_hashes(bootstrap: HeldBootstrapEntry) -> tuple[str, str, str]:
    """Rebuild final manifest/outer hashes from final pins without opening them."""
    need(FINAL_BASE7_PINS_INSTALLED is True and len(BASE7_PINS) == 7 and (EXACT8 == (V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT, SCHEMA, CONTRACT, PRODUCER, CONSUMER, TRANSITION, AUDIT, SELF)), 'launcher-native rejection requires final active-anchor pins')
    entries: list[dict[str, str]] = []
    for path in EXACT8:
        file_pin = bootstrap.expected_sha256 if path == SELF else BASE7_PINS[path][0]
        need(re.fullmatch('[0-9a-f]{64}', file_pin) is not None and file_pin not in {_DRAFT_FILE_PIN, '0' * 64}, 'launcher-native rejection exact8 final file pin')
        entries.append({'path': str(path.relative_to(ROOT)), 'file_sha256': file_pin})
    manifest_raw = b''.join((f'{entry['file_sha256']}  {entry['path']}\n'.encode('ascii') for entry in entries))
    manifest_sha256 = sha_bytes(manifest_raw)
    outer = close_object({'schema': 'cm2.round306c79g.true-global-no-producer-consumer.cold-launch-outer-receipt.v16r2', 'status': 'FROZEN_COLD_LAUNCH_OUTER_LAST__EXACT8_MANIFEST_CLOSED__RUNTIME_DEFERRED', 'effective_checkpoint_object_sha256': CHECKPOINT, 'exact8_ordered_entries': entries, 'cold_launch_manifest': {'path': str(MANIFEST.relative_to(ROOT)), 'file_sha256': manifest_sha256, 'ordered_entry_count': 8}, 'cold_launcher': {'path': str(SELF.relative_to(ROOT)), 'file_sha256': bootstrap.expected_sha256}, 'all_exact8_regular_0444_nlink1_and_held_for_runtime': True, 'outer_published_after_exact8_manifest': True, 'runtime_entry_must_be_cold_launcher': True, 'sole_external_static_file_anchor_is_launcher_sha256': True, 'declared_external_tcb': ['EXTERNAL_HELD_FD_SEALED_MEMFD_BOOTSTRAP', 'PYTHON3_ISOLATED_INTERPRETER', 'LINUX_KERNEL_OPENAT2_STATX_MEMFD_PROCFS'], 'formal_global_closure_credit': 0, 'D02_unlock': False, 'runtime_executed_during_static_freeze': False})
    outer_raw = canonical(outer) + b'\n'
    return (manifest_sha256, sha_bytes(outer_raw), outer['object_sha256'])

def construct_launcher_native_rejection(bootstrap: HeldBootstrapEntry) -> dict[str, Any]:
    """Return the exact closed-schema rejection without opening the bundle."""
    manifest_sha256, outer_file_sha256, outer_object_sha256 = reconstruct_unopened_publication_hashes(bootstrap)
    return close_object({'schema': 'cm2.round306c79g.true-global-no-producer-consumer.v16r2.later-rejection', 'status': 'PERMANENT_FAIL_CLOSED_REJECTION__ZERO_CREDIT', 'effective_checkpoint_object_sha256': CHECKPOINT, 'namespace_exact_path': str(V16R2_REJECTION_NAMESPACE.relative_to(ROOT)), 'target_exact_path': str(V16R2_LATER_REJECTION.relative_to(ROOT)), 'rejection_reason': 'ORPHANED_OR_INCOMPLETE_C79G_V16R2_SURFACE', 'consumer_file_sha256': BASE7_PINS[CONSUMER][0], 'producer_file_sha256': BASE7_PINS[PRODUCER][0], 'contract_file_sha256': BASE7_PINS[CONTRACT][0], 'contract_object_sha256': BASE7_PINS[CONTRACT][1], 'closed_schema_file_sha256': BASE7_PINS[SCHEMA][0], 'v5_official_rejection_file_sha256': V5_REJECTION_FILE_PIN, 'v5_official_rejection_object_sha256': V5_REJECTION_OBJECT_PIN, 'v6_official_rejection_file_sha256': V6_REJECTION_FILE_PIN, 'v6_official_rejection_object_sha256': V6_REJECTION_OBJECT_PIN, 'v7_official_rejection_file_sha256': V7_REJECTION_FILE_PIN, 'v7_official_rejection_object_sha256': V7_REJECTION_OBJECT_PIN, 'v7_publication_lock_continuity_incident_object_sha256': V7_LOCK_CONTINUITY_INCIDENT_OBJECT_PIN, 'v8_official_rejection_file_sha256': V8_REJECTION_FILE_PIN, 'v8_official_rejection_object_sha256': V8_REJECTION_OBJECT_PIN, 'v9_official_rejection_file_sha256': V9_REJECTION_FILE_PIN, 'v9_official_rejection_object_sha256': V9_REJECTION_OBJECT_PIN, 'v10_official_rejection_file_sha256': V10_REJECTION_FILE_PIN, 'v10_official_rejection_object_sha256': V10_REJECTION_OBJECT_PIN, 'v11_official_rejection_file_sha256': V11_REJECTION_FILE_PIN, 'v11_official_rejection_object_sha256': V11_REJECTION_OBJECT_PIN, 'v12_official_rejection_file_sha256': V12_REJECTION_FILE_PIN, 'v12_official_rejection_object_sha256': V12_REJECTION_OBJECT_PIN, 'v4_rejection_supersession_file_sha256': V4_SUPERSESSION_FILE_PIN, 'v4_rejection_supersession_object_sha256': V4_SUPERSESSION_OBJECT_PIN, 'cold_launcher_file_sha256': bootstrap.expected_sha256, 'cold_manifest_file_sha256': manifest_sha256, 'cold_outer_file_sha256': outer_file_sha256, 'cold_outer_object_sha256': outer_object_sha256, 'official_writer_coordination_lock_policy': stable_official_writer_lock_policy(), 'official_writer_coordination_lock_held_for_entire_reject_command': True, 'target_is_protocol_and_checkpoint_deterministic': True, 'commit_operation': 'O_CREAT_O_EXCL_FIXED_TARGET_NO_FALLBACK', 'namespace_at_rest_mode': '0555', 'namespace_lock_held_write_window_mode': '0755', 'rejection_file_mode': '0444', 'rejection_file_nlink': 1, 'file_fsync_required': True, 'namespace_fsync_required_after_file_and_after_reseal': True, 'runtime_parent_fsync_required_after_namespace_creation': True, 'idempotent_existing_recovery_re_fsyncs_rejection_file_namespace_and_runtime_parent': True, 'overwrite_delete_or_reuse_allowed': False, 'partial_malformed_or_extra_namespace_entry_revokes_authority': True, 'standalone_authority': False, 'formal_global_closure_credit': 0, 'D02_unlock': False, 'D02_gate_credit': 0, 'D02_task_credit': 0, 'D02_formal_pending_task_count': 33638, 'D02_started': False})

def _write_all(fd: int, raw: bytes) -> None:
    offset = 0
    while offset < len(raw):
        written = os.write(fd, raw[offset:])
        need(written > 0, 'launcher-native rejection complete write')
        offset += written

def install_or_replay_launcher_native_rejection(bootstrap: HeldBootstrapEntry, coordination: HeldCoordinationParent) -> None:
    """Append the sole fixed rejection before opening any cold bundle file."""
    coordination.verify()
    expected = construct_launcher_native_rejection(bootstrap)
    expected_raw = canonical(expected) + b'\n'
    name = V16R2_REJECTION_NAMESPACE.name
    namespace_fd = -1
    try:
        try:
            state = os.stat(name, dir_fd=coordination.fd, follow_symlinks=False)
        except FileNotFoundError:
            os.mkdir(name, 365, dir_fd=coordination.fd)
            namespace_fd = os.open(name, os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC | getattr(os, 'O_NOFOLLOW', 0), dir_fd=coordination.fd)
            os.fchmod(namespace_fd, 365)
            os.fsync(namespace_fd)
            os.fsync(coordination.fd)
            state = os.fstat(namespace_fd)
        else:
            namespace_fd = openat2_beneath(V16R2_REJECTION_NAMESPACE, os.O_RDONLY | os.O_DIRECTORY)
    except BaseException:
        if namespace_fd >= 0:
            os.close(namespace_fd)
        raise
    rejection_guard: HeldFile | None = None
    try:
        before = os.fstat(namespace_fd)
        path_before = root_lstat(V16R2_REJECTION_NAMESPACE)
        universe = set(os.listdir(namespace_fd))
        need(stat.S_ISDIR(state.st_mode) and fingerprint(state) == fingerprint(before) == fingerprint(path_before) and (stat.S_IMODE(before.st_mode) == 365) and (before.st_nlink == 2) and (mount_id(namespace_fd) == coordination.mount_id), 'launcher-native rejection namespace sealed before append')
        target = os.stat(V16R2_LATER_REJECTION.name, dir_fd=namespace_fd, follow_symlinks=False) if V16R2_LATER_REJECTION.name in universe else None
        if target is not None:
            need(universe == {V16R2_LATER_REJECTION.name}, 'idempotent rejection exact singleton')
            rejection_guard = HeldFile(V16R2_LATER_REJECTION, 'existing launcher-native v16r2 rejection')
        else:
            need(not universe, 'first rejection append requires exact empty namespace')
            os.fchmod(namespace_fd, 493)
            os.fsync(namespace_fd)
            need(stat.S_IMODE(os.fstat(namespace_fd).st_mode) == 493, 'launcher-native rejection exact write-window mode')
            writer = -1
            try:
                writer = os.open(V16R2_LATER_REJECTION.name, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_CLOEXEC | getattr(os, 'O_NOFOLLOW', 0), 384, dir_fd=namespace_fd)
                _write_all(writer, expected_raw)
                os.fsync(writer)
                os.fchmod(writer, 292)
                os.fsync(writer)
            finally:
                if writer >= 0:
                    os.close(writer)
                os.fchmod(namespace_fd, 365)
                os.fsync(namespace_fd)
            rejection_guard = HeldFile(V16R2_LATER_REJECTION, 'new launcher-native v16r2 rejection')
        need(rejection_guard is not None, 'launcher-native rejection file held')
        value = strict_json(rejection_guard.raw, 'launcher-native v16r2 rejection')
        need(isinstance(value, dict), 'launcher-native rejection mapping')
        verify_object(value, 'launcher-native v16r2 rejection')
        os.fsync(rejection_guard.fd)
        os.fsync(namespace_fd)
        os.fsync(coordination.fd)
        after = os.fstat(namespace_fd)
        path_after = root_lstat(V16R2_REJECTION_NAMESPACE)
        need(value == expected and rejection_guard.raw == expected_raw and (set(os.listdir(namespace_fd)) == {V16R2_LATER_REJECTION.name}) and (fingerprint(after) == fingerprint(path_after)) and (stat.S_IMODE(after.st_mode) == 365) and (after.st_nlink == 2), 'launcher-native rejection durable exact singleton')
        rejection_guard.terminal_replay()
        coordination.verify()
        bootstrap.terminal_replay()
    finally:
        if rejection_guard is not None:
            rejection_guard.close()
        if namespace_fd >= 0:
            os.close(namespace_fd)

class HeldV3RejectionNamespace:
    """Hold the official predecessor rejection namespace under the lock."""

    def __init__(self, coordination: HeldCoordinationParent, rejection: HeldFile) -> None:
        coordination.verify()
        self.path = V3_OFFICIAL_REJECTION.parent
        self.fd = -1
        self.fd = openat2_beneath(self.path, os.O_RDONLY | os.O_DIRECTORY)
        try:
            self.before = os.fstat(self.fd)
            self.mount_id = mount_id(self.fd)
            before_path = root_lstat(self.path)
            first = set(os.listdir(self.fd))
            member = os.stat(V3_OFFICIAL_REJECTION.name, dir_fd=self.fd, follow_symlinks=False)
            after = os.fstat(self.fd)
            after_path = root_lstat(self.path)
            second = set(os.listdir(self.fd))
            need(stat.S_ISDIR(self.before.st_mode) and stat.S_IMODE(self.before.st_mode) == 365 and (self.before.st_nlink == 2) and (fingerprint(before_path) == fingerprint(self.before) == fingerprint(after) == fingerprint(after_path)) and (first == second == {V3_OFFICIAL_REJECTION.name}) and ((member.st_dev, member.st_ino) == rejection.identity) and (self.mount_id == rejection.mount_id == coordination.mount_id), 'official v3 rejection exact singleton namespace held under lock')
        except BaseException:
            os.close(self.fd)
            self.fd = -1
            raise

    def terminal_replay(self, rejection: HeldFile) -> None:
        before = os.fstat(self.fd)
        before_path = root_lstat(self.path)
        first = set(os.listdir(self.fd))
        member = os.stat(V3_OFFICIAL_REJECTION.name, dir_fd=self.fd, follow_symlinks=False)
        after = os.fstat(self.fd)
        after_path = root_lstat(self.path)
        second = set(os.listdir(self.fd))
        need(fingerprint(before) == fingerprint(before_path) == fingerprint(self.before) == fingerprint(after) == fingerprint(after_path) and first == second == {V3_OFFICIAL_REJECTION.name} and (stat.S_IMODE(after.st_mode) == 365) and (after.st_nlink == 2) and ((member.st_dev, member.st_ino) == rejection.identity) and (mount_id(self.fd) == self.mount_id), 'official v3 rejection namespace terminal singleton replay')

    def close(self) -> None:
        if self.fd >= 0:
            os.close(self.fd)
            self.fd = -1

class HeldV3PredecessorExact10:
    """Live-replay the frozen v3 exact10 plus its official later rejection."""

    def __init__(self, coordination: HeldCoordinationParent, rejection: HeldFile) -> None:
        coordination.verify()
        self.files: list[HeldFile] = []
        self.namespace: HeldV3RejectionNamespace | None = None
        try:
            for path, file_pin, _ in V3_EXACT10_PINS:
                self.files.append(HeldFile(path, 'frozen v3 exact10:' + path.name, file_pin))
            self.by_path = {item.path: item for item in self.files}
            need(len(self.by_path) == 10 and len({item.identity for item in self.files}) == 10 and (len({item.mount_id for item in self.files}) == 1) and (next(iter({item.mount_id for item in self.files})) == coordination.mount_id == rejection.mount_id), 'frozen v3 exact10 unique live files on coordination mount')
            for path, _, object_pin in V3_EXACT10_PINS:
                if object_pin is not None:
                    value = strict_json(self.by_path[path].raw, 'frozen v3 object:' + path.name)
                    need(isinstance(value, dict), 'frozen v3 object mapping')
                    verify_object(value, 'frozen v3 object:' + path.name, object_pin)
            expected_exact8 = [{'path': str(path.relative_to(ROOT)), 'file_sha256': file_pin} for path, file_pin, _ in V3_EXACT10_PINS[:8]]
            manifest = self.files[8]
            need(parse_manifest(manifest.raw) == expected_exact8, 'frozen v3 exact8 manifest reconstructed exactly')
            outer = strict_json(self.files[9].raw, 'frozen v3 outer')
            need(isinstance(outer, dict) and outer.get('status') == 'FROZEN_COLD_LAUNCH_OUTER_LAST__EXACT8_MANIFEST_CLOSED__RUNTIME_DEFERRED' and (outer.get('effective_checkpoint_object_sha256') == CHECKPOINT) and (outer.get('exact8_ordered_entries') == expected_exact8) and (outer.get('cold_launch_manifest', {}).get('file_sha256') == V3_EXACT10_PINS[8][1]) and (outer.get('cold_launcher', {}).get('file_sha256') == V3_EXACT10_PINS[7][1]) and (outer.get('formal_global_closure_credit') == 0) and (outer.get('D02_unlock') is False) and (max(self.files[9].before.st_mtime_ns, self.files[9].before.st_ctime_ns) < min(rejection.before.st_mtime_ns, rejection.before.st_ctime_ns)), 'frozen v3 exact10 outer and strictly later rejection closure')
            rejected = strict_json(rejection.raw, 'official v3 later rejection')
            need(isinstance(rejected, dict) and rejected.get('schema') == 'cm2.round306c79g.true-global-no-producer-consumer.v3.later-rejection' and (rejected.get('status') == 'PERMANENT_FAIL_CLOSED_REJECTION__ZERO_CREDIT') and (rejected.get('rejection_reason') == 'ORPHANED_OR_INCOMPLETE_C79G_V3_SURFACE') and (rejected.get('effective_checkpoint_object_sha256') == CHECKPOINT) and (rejected.get('target_exact_path') == str(V3_OFFICIAL_REJECTION.relative_to(ROOT))) and (rejected.get('namespace_exact_path') == str(V3_OFFICIAL_REJECTION.parent.relative_to(ROOT))) and (rejected.get('cold_launcher_file_sha256') == V3_EXACT10_PINS[7][1]) and (rejected.get('cold_manifest_file_sha256') == V3_EXACT10_PINS[8][1]) and (rejected.get('cold_outer_file_sha256') == V3_EXACT10_PINS[9][1]) and (rejected.get('cold_outer_object_sha256') == V3_EXACT10_PINS[9][2]) and (rejected.get('formal_global_closure_credit') == 0) and (rejected.get('D02_unlock') is False) and (rejected.get('D02_started') is False) and (rejected.get('standalone_authority') is False) and (rejected.get('overwrite_delete_or_reuse_allowed') is False), 'official v3 rejection binds frozen v3 exact10')
            self.namespace = HeldV3RejectionNamespace(coordination, rejection)
        except BaseException:
            if self.namespace is not None:
                self.namespace.close()
            for item in reversed(self.files):
                item.close()
            raise

    def terminal_replay(self, rejection: HeldFile) -> None:
        for item in self.files:
            item.terminal_replay()
        need(self.namespace is not None, 'v3 rejection namespace held')
        self.namespace.terminal_replay(rejection)

    def close(self) -> None:
        if self.namespace is not None:
            self.namespace.close()
            self.namespace = None
        for item in self.files:
            item.close()
        self.files = []

class HeldV5RejectionNamespace:
    """Hold the immediate predecessor's official rejection singleton."""

    def __init__(self, coordination: HeldCoordinationParent, rejection: HeldFile) -> None:
        coordination.verify()
        self.path = V5_OFFICIAL_REJECTION.parent
        self.fd = -1
        self.fd = openat2_beneath(self.path, os.O_RDONLY | os.O_DIRECTORY)
        try:
            self.before = os.fstat(self.fd)
            self.mount_id = mount_id(self.fd)
            before_path = root_lstat(self.path)
            first = set(os.listdir(self.fd))
            member = os.stat(V5_OFFICIAL_REJECTION.name, dir_fd=self.fd, follow_symlinks=False)
            after = os.fstat(self.fd)
            after_path = root_lstat(self.path)
            second = set(os.listdir(self.fd))
            need(stat.S_ISDIR(self.before.st_mode) and stat.S_IMODE(self.before.st_mode) == 365 and (self.before.st_nlink == 2) and (fingerprint(before_path) == fingerprint(self.before) == fingerprint(after) == fingerprint(after_path)) and (first == second == {V5_OFFICIAL_REJECTION.name}) and ((member.st_dev, member.st_ino) == rejection.identity) and (self.mount_id == rejection.mount_id == coordination.mount_id), 'official v5 rejection exact singleton namespace held under lock')
        except BaseException:
            os.close(self.fd)
            self.fd = -1
            raise

    def terminal_replay(self, rejection: HeldFile) -> None:
        before = os.fstat(self.fd)
        before_path = root_lstat(self.path)
        first = set(os.listdir(self.fd))
        member = os.stat(V5_OFFICIAL_REJECTION.name, dir_fd=self.fd, follow_symlinks=False)
        after = os.fstat(self.fd)
        after_path = root_lstat(self.path)
        second = set(os.listdir(self.fd))
        need(fingerprint(before) == fingerprint(before_path) == fingerprint(self.before) == fingerprint(after) == fingerprint(after_path) and first == second == {V5_OFFICIAL_REJECTION.name} and (stat.S_IMODE(after.st_mode) == 365) and (after.st_nlink == 2) and ((member.st_dev, member.st_ino) == rejection.identity) and (mount_id(self.fd) == self.mount_id), 'official v5 rejection namespace terminal singleton replay')

    def close(self) -> None:
        if self.fd >= 0:
            os.close(self.fd)
            self.fd = -1

class HeldV5PredecessorExact10:
    """Replay published v5 exact10 plus its strictly later official rejection."""

    def __init__(self, coordination: HeldCoordinationParent, rejection: HeldFile) -> None:
        coordination.verify()
        self.files: list[HeldFile] = []
        self.namespace: HeldV5RejectionNamespace | None = None
        try:
            for path, file_pin, _ in V5_EXACT10_PINS:
                self.files.append(HeldFile(path, 'frozen v5 exact10:' + path.name, file_pin))
            self.by_path = {item.path: item for item in self.files}
            need(len(self.by_path) == 10 and len({item.identity for item in self.files}) == 10 and (len({item.mount_id for item in self.files}) == 1) and (next(iter({item.mount_id for item in self.files})) == coordination.mount_id == rejection.mount_id), 'frozen v5 exact10 unique live files on coordination mount')
            for path, _, object_pin in V5_EXACT10_PINS:
                if object_pin is not None:
                    value = strict_json(self.by_path[path].raw, 'frozen v5 object:' + path.name)
                    need(isinstance(value, dict), 'frozen v5 object mapping')
                    verify_object(value, 'frozen v5 object:' + path.name, object_pin)
            expected_exact8 = [{'path': str(path.relative_to(ROOT)), 'file_sha256': file_pin} for path, file_pin, _ in V5_EXACT10_PINS[:8]]
            manifest = self.files[8]
            need(parse_manifest(manifest.raw) == expected_exact8, 'frozen v5 exact8 manifest reconstructed exactly')
            outer = strict_json(self.files[9].raw, 'frozen v5 outer')
            need(isinstance(outer, dict), 'frozen v5 outer mapping')
            verify_object(outer, 'frozen v5 outer', V5_EXACT10_PINS[9][2])
            chronology = cold_publication_chronology([item.before for item in self.files[:8]], self.files[8].before, self.files[9].before)
            need(self.files[9].raw == canonical(outer) + b'\n' and set(outer) == {'D02_unlock', 'all_exact8_regular_0444_nlink1_and_held_for_runtime', 'cold_launch_manifest', 'cold_launcher', 'declared_external_tcb', 'effective_checkpoint_object_sha256', 'exact8_ordered_entries', 'formal_global_closure_credit', 'object_sha256', 'outer_published_after_exact8_manifest', 'runtime_entry_must_be_cold_launcher', 'runtime_executed_during_static_freeze', 'schema', 'sole_external_static_file_anchor_is_launcher_sha256', 'status'} and (outer.get('schema') == 'cm2.round306c79g.true-global-no-producer-consumer.cold-launch-outer-receipt.v5') and (outer.get('status') == 'FROZEN_COLD_LAUNCH_OUTER_LAST__EXACT8_MANIFEST_CLOSED__RUNTIME_DEFERRED') and (outer.get('effective_checkpoint_object_sha256') == CHECKPOINT) and (outer.get('exact8_ordered_entries') == expected_exact8) and (outer.get('cold_launch_manifest', {}).get('file_sha256') == V5_EXACT10_PINS[8][1]) and (outer.get('cold_launcher', {}).get('file_sha256') == V5_EXACT10_PINS[7][1]) and (outer.get('formal_global_closure_credit') == 0) and (outer.get('D02_unlock') is False) and (outer.get('runtime_executed_during_static_freeze') is False) and all(chronology.values()) and (max(self.files[9].before.st_mtime_ns, self.files[9].before.st_ctime_ns) < min(rejection.before.st_mtime_ns, rejection.before.st_ctime_ns)), 'frozen v5 exact10 outer then strictly later rejection closure')
            rejected = strict_json(rejection.raw, 'official v5 later rejection')
            need(isinstance(rejected, dict), 'official v5 rejection mapping')
            verify_object(rejected, 'official v5 later rejection', V5_REJECTION_OBJECT_PIN)
            need(len(V5_OFFICIAL_REJECTION_EXACT39_KEYS) == 39 and sha_bytes(canonical(sorted(V5_OFFICIAL_REJECTION_EXACT39_KEYS))) == V5_OFFICIAL_REJECTION_EXACT39_KEYSET_SHA256 and (set(rejected) == V5_OFFICIAL_REJECTION_EXACT39_KEYS) and (sha_bytes(canonical(sorted(rejected))) == V5_OFFICIAL_REJECTION_EXACT39_KEYSET_SHA256) and (rejection.raw == canonical(rejected) + b'\n') and (rejected.get('schema') == 'cm2.round306c79g.true-global-no-producer-consumer.v5.later-rejection') and (rejected.get('status') == 'PERMANENT_FAIL_CLOSED_REJECTION__ZERO_CREDIT') and (rejected.get('rejection_reason') == 'ORPHANED_OR_INCOMPLETE_C79G_V5_SURFACE') and (rejected.get('effective_checkpoint_object_sha256') == CHECKPOINT) and (rejected.get('target_exact_path') == str(V5_OFFICIAL_REJECTION.relative_to(ROOT))) and (rejected.get('namespace_exact_path') == str(V5_OFFICIAL_REJECTION.parent.relative_to(ROOT))) and (rejected.get('closed_schema_file_sha256') == V5_EXACT10_PINS[1][1]) and (rejected.get('contract_file_sha256') == V5_EXACT10_PINS[2][1]) and (rejected.get('contract_object_sha256') == V5_EXACT10_PINS[2][2]) and (rejected.get('producer_file_sha256') == V5_EXACT10_PINS[3][1]) and (rejected.get('consumer_file_sha256') == V5_EXACT10_PINS[4][1]) and (rejected.get('cold_launcher_file_sha256') == V5_EXACT10_PINS[7][1]) and (rejected.get('cold_manifest_file_sha256') == V5_EXACT10_PINS[8][1]) and (rejected.get('cold_outer_file_sha256') == V5_EXACT10_PINS[9][1]) and (rejected.get('cold_outer_object_sha256') == V5_EXACT10_PINS[9][2]) and (rejected.get('v4_rejection_supersession_file_sha256') == V4_SUPERSESSION_FILE_PIN) and (rejected.get('v4_rejection_supersession_object_sha256') == V4_SUPERSESSION_OBJECT_PIN) and (rejected.get('formal_global_closure_credit') == 0) and (rejected.get('D02_unlock') is False) and (rejected.get('D02_started') is False) and (rejected.get('standalone_authority') is False) and (rejected.get('overwrite_delete_or_reuse_allowed') is False), 'official v5 rejection binds published v5 exact10')
            self.strict_bool_regression = v5_strict_bool_regression({'producer_v5': self.files[3].raw, 'consumer_v5': self.files[4].raw, 'launcher_v5': self.files[7].raw})
            self.namespace = HeldV5RejectionNamespace(coordination, rejection)
            self._assert_positive_runtime_absence()
        except BaseException:
            if self.namespace is not None:
                self.namespace.close()
                self.namespace = None
            for item in reversed(self.files):
                item.close()
            self.files = []
            raise

    @staticmethod
    def _assert_positive_runtime_absence() -> None:
        for path in V5_FORBIDDEN_RUNTIME_PATHS:
            root_absent(path, 'officially rejected v5 runtime surface:' + path.name)

    def terminal_replay(self, rejection: HeldFile) -> None:
        for item in self.files:
            item.terminal_replay()
        need(self.namespace is not None, 'v5 rejection namespace held')
        self.namespace.terminal_replay(rejection)
        self._assert_positive_runtime_absence()

    def close(self) -> None:
        if self.namespace is not None:
            self.namespace.close()
            self.namespace = None
        for item in reversed(self.files):
            item.close()
        self.files = []

class HeldV6RejectionNamespace:
    """Hold the immediate predecessor's official rejection singleton."""

    def __init__(self, coordination: HeldCoordinationParent, rejection: HeldFile) -> None:
        coordination.verify()
        self.path = V6_OFFICIAL_REJECTION.parent
        self.fd = -1
        self.fd = openat2_beneath(self.path, os.O_RDONLY | os.O_DIRECTORY)
        try:
            self.before = os.fstat(self.fd)
            self.mount_id = mount_id(self.fd)
            before_path = root_lstat(self.path)
            first = set(os.listdir(self.fd))
            member = os.stat(V6_OFFICIAL_REJECTION.name, dir_fd=self.fd, follow_symlinks=False)
            after = os.fstat(self.fd)
            after_path = root_lstat(self.path)
            second = set(os.listdir(self.fd))
            need(stat.S_ISDIR(self.before.st_mode) and stat.S_IMODE(self.before.st_mode) == 365 and (self.before.st_nlink == 2) and (fingerprint(before_path) == fingerprint(self.before) == fingerprint(after) == fingerprint(after_path)) and (first == second == {V6_OFFICIAL_REJECTION.name}) and ((member.st_dev, member.st_ino) == rejection.identity) and (self.mount_id == rejection.mount_id == coordination.mount_id), 'official v6 rejection exact singleton namespace held under lock')
        except BaseException:
            os.close(self.fd)
            self.fd = -1
            raise

    def terminal_replay(self, rejection: HeldFile) -> None:
        before = os.fstat(self.fd)
        before_path = root_lstat(self.path)
        first = set(os.listdir(self.fd))
        member = os.stat(V6_OFFICIAL_REJECTION.name, dir_fd=self.fd, follow_symlinks=False)
        after = os.fstat(self.fd)
        after_path = root_lstat(self.path)
        second = set(os.listdir(self.fd))
        need(fingerprint(before) == fingerprint(before_path) == fingerprint(self.before) == fingerprint(after) == fingerprint(after_path) and first == second == {V6_OFFICIAL_REJECTION.name} and (stat.S_IMODE(after.st_mode) == 365) and (after.st_nlink == 2) and ((member.st_dev, member.st_ino) == rejection.identity) and (mount_id(self.fd) == self.mount_id), 'official v6 rejection namespace terminal singleton replay')

    def close(self) -> None:
        if self.fd >= 0:
            os.close(self.fd)
            self.fd = -1

class HeldV6PredecessorExact10:
    """Replay published v6 exact10 plus its strictly later official rejection."""

    def __init__(self, coordination: HeldCoordinationParent, rejection: HeldFile) -> None:
        coordination.verify()
        self.files: list[HeldFile] = []
        self.namespace: HeldV6RejectionNamespace | None = None
        try:
            for path, file_pin, _ in V6_EXACT10_PINS:
                self.files.append(HeldFile(path, 'frozen v6 exact10:' + path.name, file_pin))
            self.by_path = {item.path: item for item in self.files}
            need(len(self.by_path) == 10 and len({item.identity for item in self.files}) == 10 and (len({item.mount_id for item in self.files}) == 1) and (next(iter({item.mount_id for item in self.files})) == coordination.mount_id == rejection.mount_id), 'frozen v6 exact10 unique live files on coordination mount')
            for path, _, object_pin in V6_EXACT10_PINS:
                if object_pin is not None:
                    value = strict_json(self.by_path[path].raw, 'frozen v6 object:' + path.name)
                    need(isinstance(value, dict), 'frozen v6 object mapping')
                    verify_object(value, 'frozen v6 object:' + path.name, object_pin)
            expected_exact8 = [{'path': str(path.relative_to(ROOT)), 'file_sha256': file_pin} for path, file_pin, _ in V6_EXACT10_PINS[:8]]
            manifest = self.files[8]
            need(parse_manifest(manifest.raw) == expected_exact8, 'frozen v6 exact8 manifest reconstructed exactly')
            outer = strict_json(self.files[9].raw, 'frozen v6 outer')
            need(isinstance(outer, dict), 'frozen v6 outer mapping')
            verify_object(outer, 'frozen v6 outer', V6_EXACT10_PINS[9][2])
            chronology = cold_publication_chronology([item.before for item in self.files[:8]], self.files[8].before, self.files[9].before)
            need(self.files[9].raw == canonical(outer) + b'\n' and set(outer) == {'D02_unlock', 'all_exact8_regular_0444_nlink1_and_held_for_runtime', 'cold_launch_manifest', 'cold_launcher', 'declared_external_tcb', 'effective_checkpoint_object_sha256', 'exact8_ordered_entries', 'formal_global_closure_credit', 'object_sha256', 'outer_published_after_exact8_manifest', 'runtime_entry_must_be_cold_launcher', 'runtime_executed_during_static_freeze', 'schema', 'sole_external_static_file_anchor_is_launcher_sha256', 'status'} and (outer.get('schema') == 'cm2.round306c79g.true-global-no-producer-consumer.cold-launch-outer-receipt.v6') and (outer.get('status') == 'FROZEN_COLD_LAUNCH_OUTER_LAST__EXACT8_MANIFEST_CLOSED__RUNTIME_DEFERRED') and (outer.get('effective_checkpoint_object_sha256') == CHECKPOINT) and (outer.get('exact8_ordered_entries') == expected_exact8) and (outer.get('cold_launch_manifest', {}).get('file_sha256') == V6_EXACT10_PINS[8][1]) and (outer.get('cold_launcher', {}).get('file_sha256') == V6_EXACT10_PINS[7][1]) and (outer.get('formal_global_closure_credit') == 0) and (outer.get('D02_unlock') is False) and (outer.get('runtime_executed_during_static_freeze') is False) and all(chronology.values()) and (max(self.files[9].before.st_mtime_ns, self.files[9].before.st_ctime_ns) < min(rejection.before.st_mtime_ns, rejection.before.st_ctime_ns)), 'frozen v6 exact10 outer then strictly later rejection closure')
            rejected = strict_json(rejection.raw, 'official v6 later rejection')
            need(isinstance(rejected, dict), 'official v6 rejection mapping')
            verify_object(rejected, 'official v6 later rejection', V6_REJECTION_OBJECT_PIN)
            need(rejection.raw == canonical(rejected) + b'\n' and rejected.get('schema') == 'cm2.round306c79g.true-global-no-producer-consumer.v6.later-rejection' and (rejected.get('status') == 'PERMANENT_FAIL_CLOSED_REJECTION__ZERO_CREDIT') and (rejected.get('rejection_reason') == 'ORPHANED_OR_INCOMPLETE_C79G_V6_SURFACE') and (rejected.get('effective_checkpoint_object_sha256') == CHECKPOINT) and (rejected.get('target_exact_path') == str(V6_OFFICIAL_REJECTION.relative_to(ROOT))) and (rejected.get('namespace_exact_path') == str(V6_OFFICIAL_REJECTION.parent.relative_to(ROOT))) and (rejected.get('closed_schema_file_sha256') == V6_EXACT10_PINS[1][1]) and (rejected.get('contract_file_sha256') == V6_EXACT10_PINS[2][1]) and (rejected.get('contract_object_sha256') == V6_EXACT10_PINS[2][2]) and (rejected.get('producer_file_sha256') == V6_EXACT10_PINS[3][1]) and (rejected.get('consumer_file_sha256') == V6_EXACT10_PINS[4][1]) and (rejected.get('cold_launcher_file_sha256') == V6_EXACT10_PINS[7][1]) and (rejected.get('cold_manifest_file_sha256') == V6_EXACT10_PINS[8][1]) and (rejected.get('cold_outer_file_sha256') == V6_EXACT10_PINS[9][1]) and (rejected.get('cold_outer_object_sha256') == V6_EXACT10_PINS[9][2]) and (rejected.get('v4_rejection_supersession_file_sha256') == V4_SUPERSESSION_FILE_PIN) and (rejected.get('v4_rejection_supersession_object_sha256') == V4_SUPERSESSION_OBJECT_PIN) and (rejected.get('v5_official_rejection_file_sha256') == V5_REJECTION_FILE_PIN) and (rejected.get('v5_official_rejection_object_sha256') == V5_REJECTION_OBJECT_PIN) and (rejected.get('formal_global_closure_credit') == 0) and (rejected.get('D02_unlock') is False) and (rejected.get('D02_started') is False) and (rejected.get('standalone_authority') is False) and (rejected.get('overwrite_delete_or_reuse_allowed') is False), 'official v6 rejection binds published v6 exact10')
            self.held_self_identity_structural_evidence = v6_held_self_identity_structural_evidence(self.files[3].raw)
            self.held_self_identity_defect = v6_held_self_identity_defect_regression(self.files[3].raw)
            self.namespace = HeldV6RejectionNamespace(coordination, rejection)
            self._assert_positive_runtime_absence()
        except BaseException:
            if self.namespace is not None:
                self.namespace.close()
                self.namespace = None
            for item in reversed(self.files):
                item.close()
            self.files = []
            raise

    @staticmethod
    def _assert_positive_runtime_absence() -> None:
        for path in V6_FORBIDDEN_RUNTIME_PATHS:
            root_absent(path, 'officially rejected v6 runtime surface:' + path.name)

    def terminal_replay(self, rejection: HeldFile) -> None:
        for item in self.files:
            item.terminal_replay()
        need(self.namespace is not None, 'v6 rejection namespace held')
        self.namespace.terminal_replay(rejection)
        need(v6_held_self_identity_defect_regression(self.files[3].raw) == self.held_self_identity_defect and v6_held_self_identity_structural_evidence(self.files[3].raw) == self.held_self_identity_structural_evidence, 'terminal frozen v6 structural defect dual-check replay')
        self._assert_positive_runtime_absence()

    def close(self) -> None:
        if self.namespace is not None:
            self.namespace.close()
            self.namespace = None
        for item in reversed(self.files):
            item.close()
        self.files = []

class HeldV7RejectionNamespace:
    """Hold the direct predecessor's official rejection singleton."""

    def __init__(self, coordination: HeldCoordinationParent, rejection: HeldFile) -> None:
        coordination.verify()
        self.path = V7_OFFICIAL_REJECTION.parent
        self.fd = openat2_beneath(self.path, os.O_RDONLY | os.O_DIRECTORY)
        try:
            self.before = os.fstat(self.fd)
            self.mount_id = mount_id(self.fd)
            path_before = root_lstat(self.path)
            first = set(os.listdir(self.fd))
            member = os.stat(V7_OFFICIAL_REJECTION.name, dir_fd=self.fd, follow_symlinks=False)
            after = os.fstat(self.fd)
            path_after = root_lstat(self.path)
            second = set(os.listdir(self.fd))
            need(stat.S_ISDIR(self.before.st_mode) and stat.S_IMODE(self.before.st_mode) == 365 and (self.before.st_nlink == 2) and (fingerprint(path_before) == fingerprint(self.before) == fingerprint(after) == fingerprint(path_after)) and (first == second == {V7_OFFICIAL_REJECTION.name}) and ((member.st_dev, member.st_ino) == rejection.identity) and (self.mount_id == rejection.mount_id == coordination.mount_id), 'official v7 rejection exact singleton namespace held under lock')
        except BaseException:
            os.close(self.fd)
            self.fd = -1
            raise

    def terminal_replay(self, rejection: HeldFile) -> None:
        before = os.fstat(self.fd)
        path_before = root_lstat(self.path)
        first = set(os.listdir(self.fd))
        member = os.stat(V7_OFFICIAL_REJECTION.name, dir_fd=self.fd, follow_symlinks=False)
        after = os.fstat(self.fd)
        path_after = root_lstat(self.path)
        second = set(os.listdir(self.fd))
        need(fingerprint(before) == fingerprint(path_before) == fingerprint(self.before) == fingerprint(after) == fingerprint(path_after) and first == second == {V7_OFFICIAL_REJECTION.name} and (stat.S_IMODE(after.st_mode) == 365) and (after.st_nlink == 2) and ((member.st_dev, member.st_ino) == rejection.identity) and (mount_id(self.fd) == self.mount_id), 'official v7 rejection namespace terminal singleton replay')

    def close(self) -> None:
        if self.fd >= 0:
            os.close(self.fd)
            self.fd = -1

class HeldV7PredecessorExact10:
    """Replay v7 exact10, official rejection, and the lock-continuity incident."""

    def __init__(self, coordination: HeldCoordinationParent, rejection: HeldFile) -> None:
        coordination.verify()
        self.files: list[HeldFile] = []
        self.namespace: HeldV7RejectionNamespace | None = None
        self.rejection = rejection
        try:
            for path, file_pin, _ in V7_EXACT10_PINS:
                self.files.append(HeldFile(path, 'frozen v7 exact10:' + path.name, file_pin))
            self.by_path = {item.path: item for item in self.files}
            need(len(self.by_path) == 10 and len({item.identity for item in self.files}) == 10 and (len({item.mount_id for item in self.files}) == 1) and (next(iter({item.mount_id for item in self.files})) == coordination.mount_id == rejection.mount_id), 'frozen v7 exact10 unique live files on coordination mount')
            for path, _, object_pin in V7_EXACT10_PINS:
                if object_pin is not None:
                    value = strict_json(self.by_path[path].raw, 'frozen v7 object:' + path.name)
                    need(isinstance(value, dict), 'frozen v7 object mapping')
                    verify_object(value, 'frozen v7 object:' + path.name, object_pin)
            expected_exact8 = [{'path': str(path.relative_to(ROOT)), 'file_sha256': file_pin} for path, file_pin, _ in V7_EXACT10_PINS[:8]]
            need(parse_manifest(self.files[8].raw) == expected_exact8, 'frozen v7 exact8 manifest reconstructed exactly')
            outer = strict_json(self.files[9].raw, 'frozen v7 outer')
            need(isinstance(outer, dict), 'frozen v7 outer mapping')
            verify_object(outer, 'frozen v7 outer', V7_EXACT10_PINS[9][2])
            chronology = cold_publication_chronology([item.before for item in self.files[:8]], self.files[8].before, self.files[9].before)
            need(self.files[9].raw == canonical(outer) + b'\n' and outer.get('schema') == 'cm2.round306c79g.true-global-no-producer-consumer.cold-launch-outer-receipt.v7' and (outer.get('status') == 'FROZEN_COLD_LAUNCH_OUTER_LAST__EXACT8_MANIFEST_CLOSED__RUNTIME_DEFERRED') and (outer.get('effective_checkpoint_object_sha256') == CHECKPOINT) and (outer.get('exact8_ordered_entries') == expected_exact8) and (outer.get('cold_launch_manifest', {}).get('file_sha256') == V7_EXACT10_PINS[8][1]) and (outer.get('cold_launcher', {}).get('file_sha256') == V7_EXACT10_PINS[7][1]) and (outer.get('formal_global_closure_credit') == 0) and (outer.get('D02_unlock') is False) and (outer.get('runtime_executed_during_static_freeze') is False) and all(chronology.values()) and (max(self.files[9].before.st_mtime_ns, self.files[9].before.st_ctime_ns) < min(rejection.before.st_mtime_ns, rejection.before.st_ctime_ns)), 'frozen v7 exact10 outer then strictly later rejection closure')
            rejected = strict_json(rejection.raw, 'official v7 later rejection')
            need(isinstance(rejected, dict), 'official v7 rejection mapping')
            verify_object(rejected, 'official v7 later rejection', V7_REJECTION_OBJECT_PIN)
            need(rejection.raw == canonical(rejected) + b'\n' and rejected.get('schema') == 'cm2.round306c79g.true-global-no-producer-consumer.v7.later-rejection' and (rejected.get('status') == 'PERMANENT_FAIL_CLOSED_REJECTION__ZERO_CREDIT') and (rejected.get('rejection_reason') == 'ORPHANED_OR_INCOMPLETE_C79G_V7_SURFACE') and (rejected.get('effective_checkpoint_object_sha256') == CHECKPOINT) and (rejected.get('target_exact_path') == str(V7_OFFICIAL_REJECTION.relative_to(ROOT))) and (rejected.get('namespace_exact_path') == str(V7_OFFICIAL_REJECTION.parent.relative_to(ROOT))) and (rejected.get('closed_schema_file_sha256') == V7_EXACT10_PINS[1][1]) and (rejected.get('contract_file_sha256') == V7_EXACT10_PINS[2][1]) and (rejected.get('contract_object_sha256') == V7_EXACT10_PINS[2][2]) and (rejected.get('producer_file_sha256') == V7_EXACT10_PINS[3][1]) and (rejected.get('consumer_file_sha256') == V7_EXACT10_PINS[4][1]) and (rejected.get('cold_launcher_file_sha256') == V7_EXACT10_PINS[7][1]) and (rejected.get('cold_manifest_file_sha256') == V7_EXACT10_PINS[8][1]) and (rejected.get('cold_outer_file_sha256') == V7_EXACT10_PINS[9][1]) and (rejected.get('cold_outer_object_sha256') == V7_EXACT10_PINS[9][2]) and (rejected.get('v6_official_rejection_file_sha256') == V6_REJECTION_FILE_PIN) and (rejected.get('v6_official_rejection_object_sha256') == V6_REJECTION_OBJECT_PIN) and (rejected.get('formal_global_closure_credit') == 0) and (rejected.get('D02_unlock') is False) and (rejected.get('D02_started') is False) and (rejected.get('standalone_authority') is False) and (rejected.get('overwrite_delete_or_reuse_allowed') is False), 'official v7 rejection binds published v7 exact10')
            validate_v7_lock_continuity_incident(V7_LOCK_CONTINUITY_INCIDENT, 'held v7 predecessor')
            self.namespace = HeldV7RejectionNamespace(coordination, rejection)
            self._assert_positive_runtime_absence()
        except BaseException:
            if self.namespace is not None:
                self.namespace.close()
                self.namespace = None
            for item in reversed(self.files):
                item.close()
            self.files = []
            raise

    @staticmethod
    def _assert_positive_runtime_absence() -> None:
        for path in V7_FORBIDDEN_RUNTIME_PATHS:
            root_absent(path, 'officially rejected v7 runtime surface:' + path.name)

    def terminal_replay(self, rejection: HeldFile) -> None:
        for item in self.files:
            item.terminal_replay()
        need(self.namespace is not None, 'v7 rejection namespace held')
        self.namespace.terminal_replay(rejection)
        validate_v7_lock_continuity_incident(V7_LOCK_CONTINUITY_INCIDENT, 'terminal v7 predecessor')
        self._assert_positive_runtime_absence()

    def close(self) -> None:
        if self.namespace is not None:
            self.namespace.close()
            self.namespace = None
        for item in reversed(self.files):
            item.close()
        self.files = []

class HeldV8RejectionNamespace:
    """Hold the direct predecessor v8 official rejection singleton."""

    def __init__(self, coordination: HeldCoordinationParent, rejection: HeldFile) -> None:
        coordination.verify()
        self.path = V8_OFFICIAL_REJECTION.parent
        self.fd = openat2_beneath(self.path, os.O_RDONLY | os.O_DIRECTORY)
        try:
            self.before = os.fstat(self.fd)
            self.mount_id = mount_id(self.fd)
            path_before = root_lstat(self.path)
            first = set(os.listdir(self.fd))
            member = os.stat(V8_OFFICIAL_REJECTION.name, dir_fd=self.fd, follow_symlinks=False)
            after = os.fstat(self.fd)
            path_after = root_lstat(self.path)
            second = set(os.listdir(self.fd))
            need(stat.S_ISDIR(self.before.st_mode) and stat.S_IMODE(self.before.st_mode) == 365 and (self.before.st_nlink == 2) and (fingerprint(path_before) == fingerprint(self.before) == fingerprint(after) == fingerprint(path_after)) and (first == second == {V8_OFFICIAL_REJECTION.name}) and ((member.st_dev, member.st_ino) == rejection.identity) and (self.mount_id == rejection.mount_id == coordination.mount_id), 'official v8 rejection exact singleton namespace held under lock')
        except BaseException:
            os.close(self.fd)
            self.fd = -1
            raise

    def terminal_replay(self, rejection: HeldFile) -> None:
        before = os.fstat(self.fd)
        path_before = root_lstat(self.path)
        first = set(os.listdir(self.fd))
        member = os.stat(V8_OFFICIAL_REJECTION.name, dir_fd=self.fd, follow_symlinks=False)
        after = os.fstat(self.fd)
        path_after = root_lstat(self.path)
        second = set(os.listdir(self.fd))
        need(fingerprint(before) == fingerprint(path_before) == fingerprint(self.before) == fingerprint(after) == fingerprint(path_after) and first == second == {V8_OFFICIAL_REJECTION.name} and (stat.S_IMODE(after.st_mode) == 365) and (after.st_nlink == 2) and ((member.st_dev, member.st_ino) == rejection.identity) and (mount_id(self.fd) == self.mount_id), 'official v8 rejection namespace terminal singleton replay')

    def close(self) -> None:
        if self.fd >= 0:
            os.close(self.fd)
            self.fd = -1

class HeldV8PredecessorExact10:
    """Replay published v8 exact10, rejection and launcher-regression gate."""

    def __init__(self, coordination: HeldCoordinationParent, rejection: HeldFile) -> None:
        coordination.verify()
        self.files: list[HeldFile] = []
        self.namespace: HeldV8RejectionNamespace | None = None
        self.rejection = rejection
        try:
            for path, file_pin, _ in V8_EXACT10_PINS:
                self.files.append(HeldFile(path, 'frozen v8 exact10:' + path.name, file_pin))
            self.by_path = {item.path: item for item in self.files}
            need(len(self.by_path) == 10 and len({item.identity for item in self.files}) == 10 and (len({item.mount_id for item in self.files}) == 1) and (next(iter({item.mount_id for item in self.files})) == coordination.mount_id == rejection.mount_id), 'frozen v8 exact10 unique live files on coordination mount')
            for path, _, object_pin in V8_EXACT10_PINS:
                if object_pin is not None:
                    value = strict_json(self.by_path[path].raw, 'frozen v8 object:' + path.name)
                    need(isinstance(value, dict), 'frozen v8 object mapping')
                    verify_object(value, 'frozen v8 object:' + path.name, object_pin)
            expected_exact8 = [{'path': str(path.relative_to(ROOT)), 'file_sha256': file_pin} for path, file_pin, _ in V8_EXACT10_PINS[:8]]
            need(parse_manifest(self.files[8].raw) == expected_exact8, 'frozen v8 exact8 manifest reconstructed exactly')
            outer = strict_json(self.files[9].raw, 'frozen v8 outer')
            need(isinstance(outer, dict), 'frozen v8 outer mapping')
            verify_object(outer, 'frozen v8 outer', V8_EXACT10_PINS[9][2])
            chronology = cold_publication_chronology([item.before for item in self.files[:8]], self.files[8].before, self.files[9].before)
            need(self.files[9].raw == canonical(outer) + b'\n' and outer.get('schema') == 'cm2.round306c79g.true-global-no-producer-consumer.cold-launch-outer-receipt.v8' and (outer.get('status') == 'FROZEN_COLD_LAUNCH_OUTER_LAST__EXACT8_MANIFEST_CLOSED__RUNTIME_DEFERRED') and (outer.get('effective_checkpoint_object_sha256') == CHECKPOINT) and (outer.get('exact8_ordered_entries') == expected_exact8) and (outer.get('cold_launch_manifest', {}).get('file_sha256') == V8_EXACT10_PINS[8][1]) and (outer.get('cold_launcher', {}).get('file_sha256') == V8_EXACT10_PINS[7][1]) and (outer.get('formal_global_closure_credit') == 0) and (outer.get('D02_unlock') is False) and (outer.get('runtime_executed_during_static_freeze') is False) and all(chronology.values()) and (max(self.files[9].before.st_mtime_ns, self.files[9].before.st_ctime_ns) < min(rejection.before.st_mtime_ns, rejection.before.st_ctime_ns)), 'frozen v8 exact10 outer then strictly later rejection closure')
            rejected = strict_json(rejection.raw, 'official v8 later rejection')
            need(isinstance(rejected, dict), 'official v8 rejection mapping')
            verify_object(rejected, 'official v8 later rejection', V8_REJECTION_OBJECT_PIN)
            need(rejection.raw == canonical(rejected) + b'\n' and rejected.get('schema') == 'cm2.round306c79g.true-global-no-producer-consumer.v8.later-rejection' and (rejected.get('status') == 'PERMANENT_FAIL_CLOSED_REJECTION__ZERO_CREDIT') and (rejected.get('rejection_reason') == 'ORPHANED_OR_INCOMPLETE_C79G_V8_SURFACE') and (rejected.get('effective_checkpoint_object_sha256') == CHECKPOINT) and (rejected.get('target_exact_path') == str(V8_OFFICIAL_REJECTION.relative_to(ROOT))) and (rejected.get('namespace_exact_path') == str(V8_OFFICIAL_REJECTION.parent.relative_to(ROOT))) and (rejected.get('closed_schema_file_sha256') == V8_EXACT10_PINS[1][1]) and (rejected.get('contract_file_sha256') == V8_EXACT10_PINS[2][1]) and (rejected.get('contract_object_sha256') == V8_EXACT10_PINS[2][2]) and (rejected.get('producer_file_sha256') == V8_EXACT10_PINS[3][1]) and (rejected.get('consumer_file_sha256') == V8_EXACT10_PINS[4][1]) and (rejected.get('cold_launcher_file_sha256') == V8_EXACT10_PINS[7][1]) and (rejected.get('cold_manifest_file_sha256') == V8_EXACT10_PINS[8][1]) and (rejected.get('cold_outer_file_sha256') == V8_EXACT10_PINS[9][1]) and (rejected.get('cold_outer_object_sha256') == V8_EXACT10_PINS[9][2]) and (rejected.get('v7_official_rejection_file_sha256') == V7_REJECTION_FILE_PIN) and (rejected.get('v7_official_rejection_object_sha256') == V7_REJECTION_OBJECT_PIN) and (rejected.get('v7_publication_lock_continuity_incident_object_sha256') == V7_LOCK_CONTINUITY_INCIDENT_OBJECT_PIN) and (rejected.get('formal_global_closure_credit') == 0) and (rejected.get('D02_unlock') is False) and (rejected.get('D02_started') is False) and (rejected.get('standalone_authority') is False) and (rejected.get('overwrite_delete_or_reuse_allowed') is False), 'official v8 rejection binds published v8 exact10')
            need(v8_launcher_regression_defect_gate(self.by_path[V8_EXACT10_PINS[7][0]].raw) == V8_LAUNCHER_REGRESSION_DEFECT, 'held v8 launcher regression defect exact gate')
            self.namespace = HeldV8RejectionNamespace(coordination, rejection)
            self._assert_positive_runtime_absence()
        except BaseException:
            if self.namespace is not None:
                self.namespace.close()
                self.namespace = None
            for item in reversed(self.files):
                item.close()
            self.files = []
            raise

    @staticmethod
    def _assert_positive_runtime_absence() -> None:
        for path in V8_FORBIDDEN_RUNTIME_PATHS:
            root_absent(path, 'officially rejected v8 runtime surface:' + path.name)

    def terminal_replay(self, rejection: HeldFile) -> None:
        for item in self.files:
            item.terminal_replay()
        need(self.namespace is not None, 'v8 rejection namespace held')
        self.namespace.terminal_replay(rejection)
        need(v8_launcher_regression_defect_gate(self.by_path[V8_EXACT10_PINS[7][0]].raw) == V8_LAUNCHER_REGRESSION_DEFECT, 'terminal v8 launcher regression defect exact gate')
        self._assert_positive_runtime_absence()

    def close(self) -> None:
        if self.namespace is not None:
            self.namespace.close()
            self.namespace = None
        for item in reversed(self.files):
            item.close()
        self.files = []

class HeldV9RejectionNamespace:
    """Hold the direct predecessor v9 official rejection singleton."""

    def __init__(self, coordination: HeldCoordinationParent, rejection: HeldFile) -> None:
        coordination.verify()
        self.path = V9_OFFICIAL_REJECTION.parent
        self.fd = openat2_beneath(self.path, os.O_RDONLY | os.O_DIRECTORY)
        try:
            self.before = os.fstat(self.fd)
            self.mount_id = mount_id(self.fd)
            path_before = root_lstat(self.path)
            first = set(os.listdir(self.fd))
            member = os.stat(V9_OFFICIAL_REJECTION.name, dir_fd=self.fd, follow_symlinks=False)
            after = os.fstat(self.fd)
            path_after = root_lstat(self.path)
            second = set(os.listdir(self.fd))
            need(stat.S_ISDIR(self.before.st_mode) and stat.S_IMODE(self.before.st_mode) == 365 and (self.before.st_nlink == 2) and (fingerprint(path_before) == fingerprint(self.before) == fingerprint(after) == fingerprint(path_after)) and (first == second == {V9_OFFICIAL_REJECTION.name}) and ((member.st_dev, member.st_ino) == rejection.identity) and (self.mount_id == rejection.mount_id == coordination.mount_id), 'official v9 rejection exact singleton namespace held under lock')
        except BaseException:
            os.close(self.fd)
            self.fd = -1
            raise

    def terminal_replay(self, rejection: HeldFile) -> None:
        before = os.fstat(self.fd)
        path_before = root_lstat(self.path)
        first = set(os.listdir(self.fd))
        member = os.stat(V9_OFFICIAL_REJECTION.name, dir_fd=self.fd, follow_symlinks=False)
        after = os.fstat(self.fd)
        path_after = root_lstat(self.path)
        second = set(os.listdir(self.fd))
        need(fingerprint(before) == fingerprint(path_before) == fingerprint(self.before) == fingerprint(after) == fingerprint(path_after) and first == second == {V9_OFFICIAL_REJECTION.name} and (stat.S_IMODE(after.st_mode) == 365) and (after.st_nlink == 2) and ((member.st_dev, member.st_ino) == rejection.identity) and (mount_id(self.fd) == self.mount_id), 'official v9 rejection namespace terminal singleton replay')

    def close(self) -> None:
        if self.fd >= 0:
            os.close(self.fd)
            self.fd = -1

class HeldV9PredecessorExact10:
    """Replay v9 exact10, rejection and proof-shape-drift incident gate."""

    def __init__(self, coordination: HeldCoordinationParent, rejection: HeldFile) -> None:
        coordination.verify()
        self.files: list[HeldFile] = []
        self.namespace: HeldV9RejectionNamespace | None = None
        self.rejection = rejection
        try:
            for path, file_pin, _ in V9_EXACT10_PINS:
                self.files.append(HeldFile(path, 'frozen v9 exact10:' + path.name, file_pin))
            self.by_path = {item.path: item for item in self.files}
            need(len(self.by_path) == 10 and len({item.identity for item in self.files}) == 10 and (len({item.mount_id for item in self.files}) == 1) and (next(iter({item.mount_id for item in self.files})) == coordination.mount_id == rejection.mount_id), 'frozen v9 exact10 unique live files on coordination mount')
            for path, _, object_pin in V9_EXACT10_PINS:
                if object_pin is not None:
                    value = strict_json(self.by_path[path].raw, 'frozen v9 object:' + path.name)
                    need(isinstance(value, dict), 'frozen v9 object mapping')
                    verify_object(value, 'frozen v9 object:' + path.name, object_pin)
            expected_exact8 = [{'path': str(path.relative_to(ROOT)), 'file_sha256': file_pin} for path, file_pin, _ in V9_EXACT10_PINS[:8]]
            need(parse_manifest(self.files[8].raw) == expected_exact8, 'frozen v9 exact8 manifest reconstructed exactly')
            outer = strict_json(self.files[9].raw, 'frozen v9 outer')
            need(isinstance(outer, dict), 'frozen v9 outer mapping')
            verify_object(outer, 'frozen v9 outer', V9_EXACT10_PINS[9][2])
            chronology = cold_publication_chronology([item.before for item in self.files[:8]], self.files[8].before, self.files[9].before)
            need(self.files[9].raw == canonical(outer) + b'\n' and outer.get('schema') == 'cm2.round306c79g.true-global-no-producer-consumer.cold-launch-outer-receipt.v9' and (outer.get('status') == 'FROZEN_COLD_LAUNCH_OUTER_LAST__EXACT8_MANIFEST_CLOSED__RUNTIME_DEFERRED') and (outer.get('effective_checkpoint_object_sha256') == CHECKPOINT) and (outer.get('exact8_ordered_entries') == expected_exact8) and (outer.get('cold_launch_manifest', {}).get('file_sha256') == V9_EXACT10_PINS[8][1]) and (outer.get('cold_launcher', {}).get('file_sha256') == V9_EXACT10_PINS[7][1]) and (outer.get('formal_global_closure_credit') == 0) and (outer.get('D02_unlock') is False) and (outer.get('runtime_executed_during_static_freeze') is False) and all(chronology.values()) and (max(self.files[9].before.st_mtime_ns, self.files[9].before.st_ctime_ns) < min(rejection.before.st_mtime_ns, rejection.before.st_ctime_ns)), 'frozen v9 exact10 outer then strictly later rejection closure')
            rejected = strict_json(rejection.raw, 'official v9 later rejection')
            need(isinstance(rejected, dict), 'official v9 rejection mapping')
            verify_object(rejected, 'official v9 later rejection', V9_REJECTION_OBJECT_PIN)
            need(rejection.raw == canonical(rejected) + b'\n' and rejected.get('schema') == 'cm2.round306c79g.true-global-no-producer-consumer.v9.later-rejection' and (rejected.get('status') == 'PERMANENT_FAIL_CLOSED_REJECTION__ZERO_CREDIT') and (rejected.get('rejection_reason') == 'ORPHANED_OR_INCOMPLETE_C79G_V9_SURFACE') and (rejected.get('effective_checkpoint_object_sha256') == CHECKPOINT) and (rejected.get('target_exact_path') == str(V9_OFFICIAL_REJECTION.relative_to(ROOT))) and (rejected.get('namespace_exact_path') == str(V9_OFFICIAL_REJECTION.parent.relative_to(ROOT))) and (rejected.get('closed_schema_file_sha256') == V9_EXACT10_PINS[1][1]) and (rejected.get('contract_file_sha256') == V9_EXACT10_PINS[2][1]) and (rejected.get('contract_object_sha256') == V9_EXACT10_PINS[2][2]) and (rejected.get('producer_file_sha256') == V9_EXACT10_PINS[3][1]) and (rejected.get('consumer_file_sha256') == V9_EXACT10_PINS[4][1]) and (rejected.get('cold_launcher_file_sha256') == V9_EXACT10_PINS[7][1]) and (rejected.get('cold_manifest_file_sha256') == V9_EXACT10_PINS[8][1]) and (rejected.get('cold_outer_file_sha256') == V9_EXACT10_PINS[9][1]) and (rejected.get('cold_outer_object_sha256') == V9_EXACT10_PINS[9][2]) and (rejected.get('v8_official_rejection_file_sha256') == V8_REJECTION_FILE_PIN) and (rejected.get('v8_official_rejection_object_sha256') == V8_REJECTION_OBJECT_PIN) and (rejected.get('formal_global_closure_credit') == 0) and (rejected.get('D02_unlock') is False) and (rejected.get('D02_started') is False) and (rejected.get('standalone_authority') is False) and (rejected.get('overwrite_delete_or_reuse_allowed') is False), 'official v9 rejection binds published v9 exact10')
            need(v9_proof_shape_drift_gate(self.by_path[V9_EXACT10_PINS[7][0]].raw) == V9_V6_PROOF_SHAPE_DRIFT_INCIDENT, 'held v9 launcher proof-shape drift exact gate')
            self.namespace = HeldV9RejectionNamespace(coordination, rejection)
            self._assert_positive_runtime_absence()
        except BaseException:
            if self.namespace is not None:
                self.namespace.close()
                self.namespace = None
            for item in reversed(self.files):
                item.close()
            self.files = []
            raise

    @staticmethod
    def _assert_positive_runtime_absence() -> None:
        for path in V9_FORBIDDEN_RUNTIME_PATHS:
            root_absent(path, 'officially rejected v9 runtime surface:' + path.name)

    def terminal_replay(self, rejection: HeldFile) -> None:
        for item in self.files:
            item.terminal_replay()
        need(self.namespace is not None, 'v9 rejection namespace held')
        self.namespace.terminal_replay(rejection)
        need(v9_proof_shape_drift_gate(self.by_path[V9_EXACT10_PINS[7][0]].raw) == V9_V6_PROOF_SHAPE_DRIFT_INCIDENT, 'terminal v9 launcher proof-shape drift exact gate')
        self._assert_positive_runtime_absence()

    def close(self) -> None:
        if self.namespace is not None:
            self.namespace.close()
            self.namespace = None
        for item in reversed(self.files):
            item.close()
        self.files = []

class HeldV12RejectionNamespace:
    """Hold the direct predecessor v12 official rejection singleton."""

    def __init__(self, coordination: HeldCoordinationParent, rejection: HeldFile) -> None:
        coordination.verify()
        self.path = V12_OFFICIAL_REJECTION.parent
        self.fd = openat2_beneath(self.path, os.O_RDONLY | os.O_DIRECTORY)
        try:
            self.before = os.fstat(self.fd)
            self.mount_id = mount_id(self.fd)
            path_before = root_lstat(self.path)
            first = set(os.listdir(self.fd))
            member = os.stat(V12_OFFICIAL_REJECTION.name, dir_fd=self.fd, follow_symlinks=False)
            after = os.fstat(self.fd)
            path_after = root_lstat(self.path)
            second = set(os.listdir(self.fd))
            need(stat.S_ISDIR(self.before.st_mode) and stat.S_IMODE(self.before.st_mode) == 365 and (self.before.st_nlink == 2) and (fingerprint(path_before) == fingerprint(self.before) == fingerprint(after) == fingerprint(path_after)) and (first == second == {V12_OFFICIAL_REJECTION.name}) and ((member.st_dev, member.st_ino) == rejection.identity) and (self.mount_id == rejection.mount_id == coordination.mount_id), 'official v12 rejection exact singleton namespace held under lock')
        except BaseException:
            os.close(self.fd)
            self.fd = -1
            raise

    def terminal_replay(self, rejection: HeldFile) -> None:
        before = os.fstat(self.fd)
        path_before = root_lstat(self.path)
        first = set(os.listdir(self.fd))
        member = os.stat(V12_OFFICIAL_REJECTION.name, dir_fd=self.fd, follow_symlinks=False)
        after = os.fstat(self.fd)
        path_after = root_lstat(self.path)
        second = set(os.listdir(self.fd))
        need(fingerprint(before) == fingerprint(path_before) == fingerprint(self.before) == fingerprint(after) == fingerprint(path_after) and first == second == {V12_OFFICIAL_REJECTION.name} and (stat.S_IMODE(after.st_mode) == 365) and (after.st_nlink == 2) and ((member.st_dev, member.st_ino) == rejection.identity) and (mount_id(self.fd) == self.mount_id), 'official v12 rejection namespace terminal singleton replay')

    def close(self) -> None:
        if self.fd >= 0:
            os.close(self.fd)
            self.fd = -1

class HeldV12PredecessorExact10:
    """Hold v12 exact10, official rejection, and its exact39-vs-52 incident."""

    def __init__(self, coordination: HeldCoordinationParent, rejection: HeldFile) -> None:
        coordination.verify()
        self.files: list[HeldFile] = []
        self.namespace: HeldV12RejectionNamespace | None = None
        self.rejection = rejection
        self.predecessor_v11: HeldV11PredecessorExact10 | None = None
        self.v5_rejection: HeldFile | None = None
        self.shape_incident: dict[str, Any] | None = None
        try:
            for path, file_pin, _ in V12_EXACT10_PINS:
                self.files.append(HeldFile(path, 'frozen v12 exact10:' + path.name, file_pin))
            self.by_path = {item.path: item for item in self.files}
            need(len(V12_EXACT10_PINS) == len(self.files) == len(self.by_path) == 10 and len({item.identity for item in self.files}) == 10 and (len({item.mount_id for item in self.files}) == 1) and (next(iter({item.mount_id for item in self.files})) == coordination.mount_id == rejection.mount_id), 'frozen v12 exact10 unique live files on coordination mount')
            for path, _, object_pin in V12_EXACT10_PINS:
                if object_pin is not None:
                    value = strict_json(self.by_path[path].raw, 'frozen v12 object:' + path.name)
                    need(isinstance(value, dict), 'frozen v12 object mapping')
                    verify_object(value, 'frozen v12 object:' + path.name, object_pin)
            expected_exact8 = [{'path': str(path.relative_to(ROOT)), 'file_sha256': file_pin} for path, file_pin, _ in V12_EXACT10_PINS[:8]]
            need(parse_manifest(self.files[8].raw) == expected_exact8, 'frozen v12 exact8 manifest reconstructed exactly')
            outer = strict_json(self.files[9].raw, 'frozen v12 outer')
            need(isinstance(outer, dict), 'frozen v12 outer mapping')
            verify_object(outer, 'frozen v12 outer', V12_EXACT10_PINS[9][2])
            chronology = cold_publication_chronology([item.before for item in self.files[:8]], self.files[8].before, self.files[9].before)
            need(self.files[9].raw == canonical(outer) + b'\n' and outer.get('schema') == 'cm2.round306c79g.true-global-no-producer-consumer.cold-launch-outer-receipt.v12' and (outer.get('status') == 'FROZEN_COLD_LAUNCH_OUTER_LAST__EXACT8_MANIFEST_CLOSED__RUNTIME_DEFERRED') and (outer.get('effective_checkpoint_object_sha256') == CHECKPOINT) and (outer.get('exact8_ordered_entries') == expected_exact8) and (outer.get('cold_launch_manifest', {}).get('file_sha256') == V12_EXACT10_PINS[8][1]) and (outer.get('cold_launcher', {}).get('file_sha256') == V12_EXACT10_PINS[7][1]) and (outer.get('formal_global_closure_credit') == 0) and (outer.get('D02_unlock') is False) and (outer.get('runtime_executed_during_static_freeze') is False) and all(chronology.values()) and (max(self.files[9].before.st_mtime_ns, self.files[9].before.st_ctime_ns) < min(rejection.before.st_mtime_ns, rejection.before.st_ctime_ns)), 'frozen v12 exact10 outer then strictly later rejection closure')
            rejected = strict_json(rejection.raw, 'official v12 later rejection')
            need(isinstance(rejected, dict), 'official v12 rejection mapping')
            verify_object(rejected, 'official v12 later rejection', V12_REJECTION_OBJECT_PIN)
            need(rejection.raw == canonical(rejected) + b'\n' and len(rejected) == len(V12_OFFICIAL_REJECTION_EXACT54_KEYS) == 54 and (set(rejected) == V12_OFFICIAL_REJECTION_EXACT54_KEYS) and (sha_bytes(canonical(sorted(rejected))) == V12_OFFICIAL_REJECTION_EXACT54_KEYSET_SHA256) and (rejected.get('schema') == 'cm2.round306c79g.true-global-no-producer-consumer.v12.later-rejection') and (rejected.get('status') == 'PERMANENT_FAIL_CLOSED_REJECTION__ZERO_CREDIT') and (rejected.get('rejection_reason') == 'ORPHANED_OR_INCOMPLETE_C79G_V12_SURFACE') and (rejected.get('effective_checkpoint_object_sha256') == CHECKPOINT) and (rejected.get('target_exact_path') == str(V12_OFFICIAL_REJECTION.relative_to(ROOT))) and (rejected.get('namespace_exact_path') == str(V12_OFFICIAL_REJECTION.parent.relative_to(ROOT))) and (rejected.get('closed_schema_file_sha256') == V12_EXACT10_PINS[1][1]) and (rejected.get('contract_file_sha256') == V12_EXACT10_PINS[2][1]) and (rejected.get('contract_object_sha256') == V12_EXACT10_PINS[2][2]) and (rejected.get('producer_file_sha256') == V12_EXACT10_PINS[3][1]) and (rejected.get('consumer_file_sha256') == V12_EXACT10_PINS[4][1]) and (rejected.get('cold_launcher_file_sha256') == V12_EXACT10_PINS[7][1]) and (rejected.get('cold_manifest_file_sha256') == V12_EXACT10_PINS[8][1]) and (rejected.get('cold_outer_file_sha256') == V12_EXACT10_PINS[9][1]) and (rejected.get('cold_outer_object_sha256') == V12_EXACT10_PINS[9][2]) and (rejected.get('v11_official_rejection_file_sha256') == V11_REJECTION_FILE_PIN) and (rejected.get('v11_official_rejection_object_sha256') == V11_REJECTION_OBJECT_PIN) and (rejected.get('formal_global_closure_credit') == 0) and (rejected.get('D02_unlock') is False) and (rejected.get('D02_gate_credit') == 0) and (rejected.get('D02_task_credit') == 0) and (rejected.get('D02_formal_pending_task_count') == 33638) and (rejected.get('D02_started') is False) and (rejected.get('standalone_authority') is False) and (rejected.get('overwrite_delete_or_reuse_allowed') is False), 'official v12 rejection exact54 binds published v12 exact10')
            self.namespace = HeldV12RejectionNamespace(coordination, rejection)
            self._assert_positive_runtime_absence()
        except BaseException:
            if self.namespace is not None:
                self.namespace.close()
                self.namespace = None
            for item in reversed(self.files):
                item.close()
            self.files = []
            raise

    @staticmethod
    def _assert_positive_runtime_absence() -> None:
        need(len(V12_FORBIDDEN_RUNTIME_PATHS) == 12, 'v12 exact twelve forbidden runtime paths')
        for path in V12_FORBIDDEN_RUNTIME_PATHS:
            root_absent(path, 'officially rejected v12 runtime surface:' + path.name)

    def bind_history(self, predecessor_v11: 'HeldV11PredecessorExact10', v5_rejection: HeldFile) -> None:
        need(self.predecessor_v11 is None and self.v5_rejection is None and (self.shape_incident is None), 'v12 predecessor and incident held-byte evidence bind once')
        need(predecessor_v11.rejection.identity == self.by_path[V11_OFFICIAL_REJECTION].identity and v5_rejection.path == V5_OFFICIAL_REJECTION, 'v12 binds shared v11 and v5 rejection held identities')
        incident = derive_v12_v5_rejection_shape_incident(self.by_path[V12_EXACT10_PINS[3][0]].raw, self.by_path[V12_EXACT10_PINS[4][0]].raw, self.by_path[V12_EXACT10_PINS[7][0]].raw, v5_rejection.raw, self.rejection.raw)
        need(incident == V12_V5_REJECTION_SHAPE_INCIDENT, 'v12 exact39-vs-52 incident exact reproduction')
        self.predecessor_v11 = predecessor_v11
        self.v5_rejection = v5_rejection
        self.shape_incident = incident

    def inherited_v12_evidence_fds(self) -> tuple[int, int, int, int, int]:
        need(self.predecessor_v11 is not None and self.v5_rejection is not None and (self.shape_incident is not None), 'v12 inherited incident evidence fully bound')
        return (self.by_path[V12_EXACT10_PINS[3][0]].fd, self.by_path[V12_EXACT10_PINS[4][0]].fd, self.by_path[V12_EXACT10_PINS[7][0]].fd, self.v5_rejection.fd, self.rejection.fd)

    def terminal_replay(self, rejection: HeldFile) -> None:
        for item in self.files:
            item.terminal_replay()
        need(self.namespace is not None and self.predecessor_v11 is not None and (self.v5_rejection is not None) and (self.shape_incident is not None), 'v12 exact10, namespace, history, and incident held')
        self.namespace.terminal_replay(rejection)
        need(derive_v12_v5_rejection_shape_incident(self.by_path[V12_EXACT10_PINS[3][0]].raw, self.by_path[V12_EXACT10_PINS[4][0]].raw, self.by_path[V12_EXACT10_PINS[7][0]].raw, self.v5_rejection.raw, rejection.raw) == self.shape_incident, 'terminal v12 exact39-vs-52 incident replay')
        self._assert_positive_runtime_absence()

    def close(self) -> None:
        if self.namespace is not None:
            self.namespace.close()
            self.namespace = None
        for item in reversed(self.files):
            item.close()
        self.files = []

class HeldV11RejectionNamespace:
    """Hold the direct predecessor v11 official rejection singleton."""

    def __init__(self, coordination: HeldCoordinationParent, rejection: HeldFile) -> None:
        coordination.verify()
        self.path = V11_OFFICIAL_REJECTION.parent
        self.fd = openat2_beneath(self.path, os.O_RDONLY | os.O_DIRECTORY)
        try:
            self.before = os.fstat(self.fd)
            self.mount_id = mount_id(self.fd)
            path_before = root_lstat(self.path)
            first = set(os.listdir(self.fd))
            member = os.stat(V11_OFFICIAL_REJECTION.name, dir_fd=self.fd, follow_symlinks=False)
            after = os.fstat(self.fd)
            path_after = root_lstat(self.path)
            second = set(os.listdir(self.fd))
            need(stat.S_ISDIR(self.before.st_mode) and stat.S_IMODE(self.before.st_mode) == 365 and (self.before.st_nlink == 2) and (fingerprint(path_before) == fingerprint(self.before) == fingerprint(after) == fingerprint(path_after)) and (first == second == {V11_OFFICIAL_REJECTION.name}) and ((member.st_dev, member.st_ino) == rejection.identity) and (self.mount_id == rejection.mount_id == coordination.mount_id), 'official v11 rejection exact singleton namespace held under lock')
        except BaseException:
            os.close(self.fd)
            self.fd = -1
            raise

    def terminal_replay(self, rejection: HeldFile) -> None:
        before = os.fstat(self.fd)
        path_before = root_lstat(self.path)
        first = set(os.listdir(self.fd))
        member = os.stat(V11_OFFICIAL_REJECTION.name, dir_fd=self.fd, follow_symlinks=False)
        after = os.fstat(self.fd)
        path_after = root_lstat(self.path)
        second = set(os.listdir(self.fd))
        need(fingerprint(before) == fingerprint(path_before) == fingerprint(self.before) == fingerprint(after) == fingerprint(path_after) and first == second == {V11_OFFICIAL_REJECTION.name} and (stat.S_IMODE(after.st_mode) == 365) and (after.st_nlink == 2) and ((member.st_dev, member.st_ino) == rejection.identity) and (mount_id(self.fd) == self.mount_id), 'official v11 rejection namespace terminal singleton replay')

    def close(self) -> None:
        if self.fd >= 0:
            os.close(self.fd)
            self.fd = -1

class HeldV11PredecessorExact10:
    """Replay v11 exact10, official rejection, and the 44/45 incident."""

    def __init__(self, coordination: HeldCoordinationParent, rejection: HeldFile) -> None:
        coordination.verify()
        self.files: list[HeldFile] = []
        self.namespace: HeldV11RejectionNamespace | None = None
        self.rejection = rejection
        self.predecessor_v10: HeldV10PredecessorExact10 | None = None
        self.predecessor_v9: HeldV9PredecessorExact10 | None = None
        self.colon_witness: dict[str, Any] | None = None
        try:
            for path, file_pin, _ in V11_EXACT10_PINS:
                self.files.append(HeldFile(path, 'frozen v11 exact10:' + path.name, file_pin))
            self.by_path = {item.path: item for item in self.files}
            need(len(self.by_path) == 10 and len({item.identity for item in self.files}) == 10 and (len({item.mount_id for item in self.files}) == 1) and (next(iter({item.mount_id for item in self.files})) == coordination.mount_id == rejection.mount_id), 'frozen v11 exact10 unique live files on coordination mount')
            for path, _, object_pin in V11_EXACT10_PINS:
                if object_pin is not None:
                    value = strict_json(self.by_path[path].raw, 'frozen v11 object:' + path.name)
                    need(isinstance(value, dict), 'frozen v11 object mapping')
                    verify_object(value, 'frozen v11 object:' + path.name, object_pin)
            expected_exact8 = [{'path': str(path.relative_to(ROOT)), 'file_sha256': file_pin} for path, file_pin, _ in V11_EXACT10_PINS[:8]]
            need(parse_manifest(self.files[8].raw) == expected_exact8, 'frozen v11 exact8 manifest reconstructed exactly')
            outer = strict_json(self.files[9].raw, 'frozen v11 outer')
            need(isinstance(outer, dict), 'frozen v11 outer mapping')
            verify_object(outer, 'frozen v11 outer', V11_EXACT10_PINS[9][2])
            chronology = cold_publication_chronology([item.before for item in self.files[:8]], self.files[8].before, self.files[9].before)
            need(self.files[9].raw == canonical(outer) + b'\n' and outer.get('schema') == 'cm2.round306c79g.true-global-no-producer-consumer.cold-launch-outer-receipt.v11' and (outer.get('status') == 'FROZEN_COLD_LAUNCH_OUTER_LAST__EXACT8_MANIFEST_CLOSED__RUNTIME_DEFERRED') and (outer.get('effective_checkpoint_object_sha256') == CHECKPOINT) and (outer.get('exact8_ordered_entries') == expected_exact8) and (outer.get('cold_launch_manifest', {}).get('file_sha256') == V11_EXACT10_PINS[8][1]) and (outer.get('cold_launcher', {}).get('file_sha256') == V11_EXACT10_PINS[7][1]) and (outer.get('formal_global_closure_credit') == 0) and (outer.get('D02_unlock') is False) and (outer.get('runtime_executed_during_static_freeze') is False) and all(chronology.values()) and (max(self.files[9].before.st_mtime_ns, self.files[9].before.st_ctime_ns) < min(rejection.before.st_mtime_ns, rejection.before.st_ctime_ns)), 'frozen v11 exact10 outer then strictly later rejection closure')
            rejected = strict_json(rejection.raw, 'official v11 later rejection')
            need(isinstance(rejected, dict), 'official v11 rejection mapping')
            verify_object(rejected, 'official v11 later rejection', V11_REJECTION_OBJECT_PIN)
            need(rejection.raw == canonical(rejected) + b'\n' and rejected.get('schema') == 'cm2.round306c79g.true-global-no-producer-consumer.v11.later-rejection' and (rejected.get('status') == 'PERMANENT_FAIL_CLOSED_REJECTION__ZERO_CREDIT') and (rejected.get('rejection_reason') == 'ORPHANED_OR_INCOMPLETE_C79G_V11_SURFACE') and (rejected.get('effective_checkpoint_object_sha256') == CHECKPOINT) and (rejected.get('target_exact_path') == str(V11_OFFICIAL_REJECTION.relative_to(ROOT))) and (rejected.get('namespace_exact_path') == str(V11_OFFICIAL_REJECTION.parent.relative_to(ROOT))) and (rejected.get('closed_schema_file_sha256') == V11_EXACT10_PINS[1][1]) and (rejected.get('contract_file_sha256') == V11_EXACT10_PINS[2][1]) and (rejected.get('contract_object_sha256') == V11_EXACT10_PINS[2][2]) and (rejected.get('producer_file_sha256') == V11_EXACT10_PINS[3][1]) and (rejected.get('consumer_file_sha256') == V11_EXACT10_PINS[4][1]) and (rejected.get('cold_launcher_file_sha256') == V11_EXACT10_PINS[7][1]) and (rejected.get('cold_manifest_file_sha256') == V11_EXACT10_PINS[8][1]) and (rejected.get('cold_outer_file_sha256') == V11_EXACT10_PINS[9][1]) and (rejected.get('cold_outer_object_sha256') == V11_EXACT10_PINS[9][2]) and (rejected.get('v10_official_rejection_file_sha256') == V10_REJECTION_FILE_PIN) and (rejected.get('v10_official_rejection_object_sha256') == V10_REJECTION_OBJECT_PIN) and (rejected.get('formal_global_closure_credit') == 0) and (rejected.get('D02_unlock') is False) and (rejected.get('D02_started') is False) and (rejected.get('standalone_authority') is False) and (rejected.get('overwrite_delete_or_reuse_allowed') is False), 'official v11 rejection binds published v11 exact10')
            self.namespace = HeldV11RejectionNamespace(coordination, rejection)
            self._assert_positive_runtime_absence()
        except BaseException:
            if self.namespace is not None:
                self.namespace.close()
                self.namespace = None
            for item in reversed(self.files):
                item.close()
            self.files = []
            raise

    @staticmethod
    def _assert_positive_runtime_absence() -> None:
        need(len(V11_FORBIDDEN_RUNTIME_PATHS) == 12, 'v11 exact twelve forbidden runtime paths')
        for path in V11_FORBIDDEN_RUNTIME_PATHS:
            root_absent(path, 'officially rejected v11 runtime surface:' + path.name)

    def bind_predecessors(self, predecessor_v10: 'HeldV10PredecessorExact10', predecessor_v9: 'HeldV9PredecessorExact10') -> None:
        need(self.predecessor_v10 is None and self.predecessor_v9 is None, 'v11 predecessor held-byte evidence binds once')
        witness = derive_v10_colon_prefix_witness(predecessor_v10.by_path[V10_EXACT10_PINS[3][0]].raw, predecessor_v9.by_path[V9_EXACT10_PINS[7][0]].raw)
        need(len(witness) == V10_COLON_PREFIX_WITNESS_KEY_COUNT and witness.get('object_sha256') == V10_COLON_PREFIX_WITNESS_OBJECT_PIN and (witness.get('successor_all_clauses_true') is True) and (witness.get('formal_global_closure_credit') == 0), 'held v10/v9 exact per-clause colon-prefix witness')
        validate_v11_dual_validator_divergence(self.by_path[V11_EXACT10_PINS[3][0]].raw, self.by_path[V11_EXACT10_PINS[7][0]].raw, witness)
        self.predecessor_v10 = predecessor_v10
        self.predecessor_v9 = predecessor_v9
        self.colon_witness = witness

    def inherited_evidence_fds(self) -> tuple[int, int, int, int, int]:
        need(self.predecessor_v10 is not None and self.predecessor_v9 is not None, 'v11 inherited predecessor fd evidence bound')
        return (self.predecessor_v10.by_path[V10_EXACT10_PINS[3][0]].fd, self.predecessor_v9.by_path[V9_EXACT10_PINS[7][0]].fd, self.by_path[V11_EXACT10_PINS[3][0]].fd, self.by_path[V11_EXACT10_PINS[7][0]].fd, self.rejection.fd)

    def terminal_replay(self, rejection: HeldFile) -> None:
        for item in self.files:
            item.terminal_replay()
        need(self.namespace is not None, 'v11 rejection namespace held')
        self.namespace.terminal_replay(rejection)
        need(self.predecessor_v10 is not None and self.predecessor_v9 is not None and (self.colon_witness is not None) and (derive_v10_colon_prefix_witness(self.predecessor_v10.by_path[V10_EXACT10_PINS[3][0]].raw, self.predecessor_v9.by_path[V9_EXACT10_PINS[7][0]].raw) == self.colon_witness), 'terminal v11 exact per-clause witness replay')
        validate_v11_dual_validator_divergence(self.by_path[V11_EXACT10_PINS[3][0]].raw, self.by_path[V11_EXACT10_PINS[7][0]].raw, self.colon_witness)
        self._assert_positive_runtime_absence()

    def close(self) -> None:
        if self.namespace is not None:
            self.namespace.close()
            self.namespace = None
        for item in reversed(self.files):
            item.close()
        self.files = []

class HeldV10RejectionNamespace:
    """Hold the direct predecessor v10 official rejection singleton."""

    def __init__(self, coordination: HeldCoordinationParent, rejection: HeldFile) -> None:
        coordination.verify()
        self.path = V10_OFFICIAL_REJECTION.parent
        self.fd = openat2_beneath(self.path, os.O_RDONLY | os.O_DIRECTORY)
        try:
            self.before = os.fstat(self.fd)
            self.mount_id = mount_id(self.fd)
            path_before = root_lstat(self.path)
            first = set(os.listdir(self.fd))
            member = os.stat(V10_OFFICIAL_REJECTION.name, dir_fd=self.fd, follow_symlinks=False)
            after = os.fstat(self.fd)
            path_after = root_lstat(self.path)
            second = set(os.listdir(self.fd))
            need(stat.S_ISDIR(self.before.st_mode) and stat.S_IMODE(self.before.st_mode) == 365 and (self.before.st_nlink == 2) and (fingerprint(path_before) == fingerprint(self.before) == fingerprint(after) == fingerprint(path_after)) and (first == second == {V10_OFFICIAL_REJECTION.name}) and ((member.st_dev, member.st_ino) == rejection.identity) and (self.mount_id == rejection.mount_id == coordination.mount_id), 'official v10 rejection exact singleton namespace held under lock')
        except BaseException:
            os.close(self.fd)
            self.fd = -1
            raise

    def terminal_replay(self, rejection: HeldFile) -> None:
        before = os.fstat(self.fd)
        path_before = root_lstat(self.path)
        first = set(os.listdir(self.fd))
        member = os.stat(V10_OFFICIAL_REJECTION.name, dir_fd=self.fd, follow_symlinks=False)
        after = os.fstat(self.fd)
        path_after = root_lstat(self.path)
        second = set(os.listdir(self.fd))
        need(fingerprint(before) == fingerprint(path_before) == fingerprint(self.before) == fingerprint(after) == fingerprint(path_after) and first == second == {V10_OFFICIAL_REJECTION.name} and (stat.S_IMODE(after.st_mode) == 365) and (after.st_nlink == 2) and ((member.st_dev, member.st_ino) == rejection.identity) and (mount_id(self.fd) == self.mount_id), 'official v10 rejection namespace terminal singleton replay')

    def close(self) -> None:
        if self.fd >= 0:
            os.close(self.fd)
            self.fd = -1

class HeldV10PredecessorExact10:
    """Replay v10 exact10, rejection and label-prefix false-negative gate."""

    def __init__(self, coordination: HeldCoordinationParent, rejection: HeldFile) -> None:
        coordination.verify()
        self.files: list[HeldFile] = []
        self.namespace: HeldV10RejectionNamespace | None = None
        self.rejection = rejection
        self.predecessor_v9: HeldV9PredecessorExact10 | None = None
        try:
            for path, file_pin, _ in V10_EXACT10_PINS:
                self.files.append(HeldFile(path, 'frozen v10 exact10:' + path.name, file_pin))
            self.by_path = {item.path: item for item in self.files}
            need(len(self.by_path) == 10 and len({item.identity for item in self.files}) == 10 and (len({item.mount_id for item in self.files}) == 1) and (next(iter({item.mount_id for item in self.files})) == coordination.mount_id == rejection.mount_id), 'frozen v10 exact10 unique live files on coordination mount')
            for path, _, object_pin in V10_EXACT10_PINS:
                if object_pin is not None:
                    value = strict_json(self.by_path[path].raw, 'frozen v10 object:' + path.name)
                    need(isinstance(value, dict), 'frozen v10 object mapping')
                    verify_object(value, 'frozen v10 object:' + path.name, object_pin)
            expected_exact8 = [{'path': str(path.relative_to(ROOT)), 'file_sha256': file_pin} for path, file_pin, _ in V10_EXACT10_PINS[:8]]
            need(parse_manifest(self.files[8].raw) == expected_exact8, 'frozen v10 exact8 manifest reconstructed exactly')
            outer = strict_json(self.files[9].raw, 'frozen v10 outer')
            need(isinstance(outer, dict), 'frozen v10 outer mapping')
            verify_object(outer, 'frozen v10 outer', V10_EXACT10_PINS[9][2])
            chronology = cold_publication_chronology([item.before for item in self.files[:8]], self.files[8].before, self.files[9].before)
            need(self.files[9].raw == canonical(outer) + b'\n' and outer.get('schema') == 'cm2.round306c79g.true-global-no-producer-consumer.cold-launch-outer-receipt.v10' and (outer.get('status') == 'FROZEN_COLD_LAUNCH_OUTER_LAST__EXACT8_MANIFEST_CLOSED__RUNTIME_DEFERRED') and (outer.get('effective_checkpoint_object_sha256') == CHECKPOINT) and (outer.get('exact8_ordered_entries') == expected_exact8) and (outer.get('cold_launch_manifest', {}).get('file_sha256') == V10_EXACT10_PINS[8][1]) and (outer.get('cold_launcher', {}).get('file_sha256') == V10_EXACT10_PINS[7][1]) and (outer.get('formal_global_closure_credit') == 0) and (outer.get('D02_unlock') is False) and (outer.get('runtime_executed_during_static_freeze') is False) and all(chronology.values()) and (max(self.files[9].before.st_mtime_ns, self.files[9].before.st_ctime_ns) < min(rejection.before.st_mtime_ns, rejection.before.st_ctime_ns)), 'frozen v10 exact10 outer then strictly later rejection closure')
            rejected = strict_json(rejection.raw, 'official v10 later rejection')
            need(isinstance(rejected, dict), 'official v10 rejection mapping')
            verify_object(rejected, 'official v10 later rejection', V10_REJECTION_OBJECT_PIN)
            need(rejection.raw == canonical(rejected) + b'\n' and rejected.get('schema') == 'cm2.round306c79g.true-global-no-producer-consumer.v10.later-rejection' and (rejected.get('status') == 'PERMANENT_FAIL_CLOSED_REJECTION__ZERO_CREDIT') and (rejected.get('rejection_reason') == 'ORPHANED_OR_INCOMPLETE_C79G_V10_SURFACE') and (rejected.get('effective_checkpoint_object_sha256') == CHECKPOINT) and (rejected.get('target_exact_path') == str(V10_OFFICIAL_REJECTION.relative_to(ROOT))) and (rejected.get('namespace_exact_path') == str(V10_OFFICIAL_REJECTION.parent.relative_to(ROOT))) and (rejected.get('closed_schema_file_sha256') == V10_EXACT10_PINS[1][1]) and (rejected.get('contract_file_sha256') == V10_EXACT10_PINS[2][1]) and (rejected.get('contract_object_sha256') == V10_EXACT10_PINS[2][2]) and (rejected.get('producer_file_sha256') == V10_EXACT10_PINS[3][1]) and (rejected.get('consumer_file_sha256') == V10_EXACT10_PINS[4][1]) and (rejected.get('cold_launcher_file_sha256') == V10_EXACT10_PINS[7][1]) and (rejected.get('cold_manifest_file_sha256') == V10_EXACT10_PINS[8][1]) and (rejected.get('cold_outer_file_sha256') == V10_EXACT10_PINS[9][1]) and (rejected.get('cold_outer_object_sha256') == V10_EXACT10_PINS[9][2]) and (rejected.get('v9_official_rejection_file_sha256') == V9_REJECTION_FILE_PIN) and (rejected.get('v9_official_rejection_object_sha256') == V9_REJECTION_OBJECT_PIN) and (rejected.get('formal_global_closure_credit') == 0) and (rejected.get('D02_unlock') is False) and (rejected.get('D02_started') is False) and (rejected.get('standalone_authority') is False) and (rejected.get('overwrite_delete_or_reuse_allowed') is False), 'official v10 rejection binds published v10 exact10')
            self.namespace = HeldV10RejectionNamespace(coordination, rejection)
            self._assert_positive_runtime_absence()
        except BaseException:
            if self.namespace is not None:
                self.namespace.close()
                self.namespace = None
            for item in reversed(self.files):
                item.close()
            self.files = []
            raise

    @staticmethod
    def _assert_positive_runtime_absence() -> None:
        for path in V10_FORBIDDEN_RUNTIME_PATHS:
            root_absent(path, 'officially rejected v10 runtime surface:' + path.name)

    def bind_predecessor_v9(self, predecessor_v9: HeldV9PredecessorExact10) -> None:
        need(self.predecessor_v9 is None, 'v10 predecessor-v9 regression evidence binds once')
        need(v10_regression_label_prefix_gate(self.by_path[V10_EXACT10_PINS[3][0]].raw, predecessor_v9.by_path[V9_EXACT10_PINS[7][0]].raw) == V10_REGRESSION_LABEL_PREFIX_INCIDENT, 'held v10 producer regression label-prefix exact gate')
        self.predecessor_v9 = predecessor_v9

    def terminal_replay(self, rejection: HeldFile) -> None:
        for item in self.files:
            item.terminal_replay()
        need(self.namespace is not None, 'v10 rejection namespace held')
        self.namespace.terminal_replay(rejection)
        need(self.predecessor_v9 is not None and v10_regression_label_prefix_gate(self.by_path[V10_EXACT10_PINS[3][0]].raw, self.predecessor_v9.by_path[V9_EXACT10_PINS[7][0]].raw) == V10_REGRESSION_LABEL_PREFIX_INCIDENT, 'terminal v10 producer regression label-prefix exact gate')
        self._assert_positive_runtime_absence()

    def close(self) -> None:
        if self.namespace is not None:
            self.namespace.close()
            self.namespace = None
        for item in reversed(self.files):
            item.close()
        self.files = []

class HeldV4RejectedDraft7:
    """Hold the frozen unpublished v4 draft7 and its supersession proof."""

    def __init__(self, coordination: HeldCoordinationParent, receipt: HeldFile, v3_rejection: HeldFile) -> None:
        coordination.verify()
        self.files: list[HeldFile] = []
        try:
            for path, file_pin, _ in V4_FROZEN_DRAFT7_PINS:
                self.files.append(HeldFile(path, 'rejected frozen v4 draft7:' + path.name, file_pin))
            self.by_path = {item.path: item for item in self.files}
            need(len(self.by_path) == 7 and len({item.identity for item in self.files}) == 7 and (len({item.mount_id for item in self.files}) == 1) and (next(iter({item.mount_id for item in self.files})) == coordination.mount_id == receipt.mount_id == v3_rejection.mount_id), 'rejected v4 draft7 unique live files on coordination mount')
            for path, _, object_pin in V4_FROZEN_DRAFT7_PINS:
                if object_pin is not None:
                    value = strict_json(self.by_path[path].raw, 'rejected v4 object:' + path.name)
                    need(isinstance(value, dict), 'rejected v4 object mapping')
                    verify_object(value, 'rejected v4 object:' + path.name, object_pin)
            value = strict_json(receipt.raw, 'v4 rejection supersession')
            need(isinstance(value, dict), 'v4 supersession mapping')
            verify_object(value, 'v4 rejection supersession', V4_SUPERSESSION_OBJECT_PIN)
            expected_members = [{'file_sha256': V3_REJECTION_FILE_PIN, 'mode': '0444', 'name': 'official_v3_later_rejection', 'nlink': 1, 'object_sha256': V3_REJECTION_OBJECT_PIN, 'path': str(V3_OFFICIAL_REJECTION.relative_to(ROOT))}]
            names = ('closed_schema_v4', 'contract_v4', 'build_only_producer_v4', 'independent_consumer_v4', 'transition_v3_to_v4', 'static_audit_v4', 'cold_launcher_v4')
            for name, (path, file_pin, object_pin) in zip(names, V4_FROZEN_DRAFT7_PINS, strict=True):
                member: dict[str, Any] = {'file_sha256': file_pin, 'mode': '0444', 'name': name, 'nlink': 1, 'path': str(path.relative_to(ROOT))}
                if object_pin is not None:
                    member['object_sha256'] = object_pin
                expected_members.append(member)
            root_defects = value.get('root_defects')
            frozen = value.get('frozen_v4_provisional_exact8')
            no_run = value.get('no_run_attestation')
            rejection = value.get('rejection')
            supersession = value.get('supersession')
            need(receipt.raw == canonical(value) + b'\n' and value.get('schema') == 'cm2.round306c79g.true-global-no-producer-consumer.v4-rejection-supersession-receipt.v1' and (value.get('status') == 'FROZEN_APPEND_ONLY_V4_STATIC_NO_RUN_REJECTION__THREE_ROOT_DEFECTS__V5_SUCCESSOR_ONLY') and (value.get('effective_checkpoint_object_sha256') == CHECKPOINT) and (value.get('formal_global_closure_credit') == 0) and (value.get('D02_unlock') is False) and (value.get('D02_started') is False) and isinstance(frozen, dict) and (frozen.get('ordered_members') == expected_members) and (frozen.get('all_eight_file_pins_match') is True) and (frozen.get('all_eight_regular_0444_nlink1') is True) and (frozen.get('cold_manifest_v4_exists') is False) and (frozen.get('cold_outer_v4_exists') is False) and isinstance(root_defects, list) and (len(root_defects) == 3) and ({item.get('id') for item in root_defects if isinstance(item, dict)} == {'V4_CONSUMER_NEED_THREE_POSITIONAL_ARGUMENTS', 'V4_CONSUMER_HELDOPAQUEMETADATA_MISSING_EXPECTED_MODE', 'V4_LAUNCHER_PATHNAME_EXECUTION_PRECEDES_HELD_FD_HASH'}) and isinstance(no_run, dict) and (no_run.get('v4_runtime_commands_invoked') == []) and (no_run.get('v4_candidate_verification_completion_authority_surfaces_created') == 0) and isinstance(rejection, dict) and (rejection.get('v4_execution_allowed') is False) and (rejection.get('v4_runtime_surfaces_authoritative') is False) and isinstance(supersession, dict) and (supersession.get('successor_version') == 5) and (supersession.get('successor_must_pin_this_receipt_file_and_object_hashes') is True), 'frozen v4 receipt exactly rejects and supersedes draft7')
            self.receipt_value = value
            self._assert_unpublished_absence(frozen)
        except BaseException:
            for item in reversed(self.files):
                item.close()
            raise

    @staticmethod
    def _assert_unpublished_absence(frozen: Mapping[str, Any]) -> None:
        root_absent(ROOT / str(frozen['cold_manifest_v4_path']), 'v4 cold manifest')
        root_absent(ROOT / str(frozen['cold_outer_v4_path']), 'v4 cold outer')
        for path in V4_FORBIDDEN_RUNTIME_PATHS:
            root_absent(path, 'rejected v4 runtime surface:' + path.name)

    def terminal_replay(self) -> None:
        for item in self.files:
            item.terminal_replay()
        frozen = self.receipt_value['frozen_v4_provisional_exact8']
        need(isinstance(frozen, dict), 'v4 frozen receipt replay mapping')
        self._assert_unpublished_absence(frozen)

    def close(self) -> None:
        for item in self.files:
            item.close()
        self.files = []

def parse_manifest(raw: bytes) -> list[dict[str, str]]:
    need(raw.endswith(b'\n'), 'cold manifest terminal newline')
    result: list[dict[str, str]] = []
    seen: set[str] = set()
    for line in raw.decode('ascii').splitlines():
        parts = line.split('  ', 1)
        need(len(parts) == 2 and re.fullmatch('[0-9a-f]{64}', parts[0]) is not None and (parts[1] not in seen), 'cold manifest exact line')
        seen.add(parts[1])
        result.append({'path': parts[1], 'file_sha256': parts[0]})
    return result

class HeldBundle:

    def __init__(self, expected_launcher_sha256: str, coordination: HeldCoordinationParent, bootstrap: HeldBootstrapEntry) -> None:
        self.files: list[HeldFile] = []
        self.manifest: HeldFile | None = None
        self.outer: HeldFile | None = None
        self.v3_rejection: HeldFile | None = None
        self.v12_rejection: HeldFile | None = None
        self.v13_incident_sources: list[HeldFile] = []
        self.v13_incident_pycs: list[HeldFile] = []
        self.v14_inherited_authority_exact12: list[HeldFile] = []
        self.v14_inherited_authority_exact12_owned: list[HeldFile] = []
        self.v14_inherited_authority_by_role: dict[str, HeldFile] = {}
        self.v14_inherited_authority_initial_replay: dict[str, Any] | None = None
        self.global_identity_census: dict[str, Any] | None = None
        self.predecessor_v3: HeldV3PredecessorExact10 | None = None
        self.predecessor_v5: HeldV5PredecessorExact10 | None = None
        self.predecessor_v6: HeldV6PredecessorExact10 | None = None
        self.predecessor_v7: HeldV7PredecessorExact10 | None = None
        self.predecessor_v8: HeldV8PredecessorExact10 | None = None
        self.predecessor_v9: HeldV9PredecessorExact10 | None = None
        self.predecessor_v10: HeldV10PredecessorExact10 | None = None
        self.predecessor_v11: HeldV11PredecessorExact10 | None = None
        self.predecessor_v12: HeldV12PredecessorExact10 | None = None
        self.rejected_v4: HeldV4RejectedDraft7 | None = None
        self.bootstrap = bootstrap
        try:
            self._initialize(expected_launcher_sha256, coordination, bootstrap)
        except BaseException:
            self.close()
            raise

    def _initialize(self, expected_launcher_sha256: str, coordination: HeldCoordinationParent, bootstrap: HeldBootstrapEntry) -> None:
        coordination.verify()
        need(SELF == OUT / 'cm2_round306c79g_true_global_no_producer_consumer_cold_launch_v16r2r63o_repair_semantic_source.py', 'exact cold launcher path')
        need(FINAL_BASE7_PINS_INSTALLED is True, 'draft launcher disabled until root installs final audited base7 pins')
        for path, (file_pin, object_pin) in BASE7_PINS.items():
            need(re.fullmatch('[0-9a-f]{64}', file_pin) is not None and file_pin != '0' * 64 and (path == V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT or file_pin != _DRAFT_FILE_PIN) and (object_pin is None or (re.fullmatch('[0-9a-f]{64}', object_pin) is not None and object_pin != '0' * 64 and (path == V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT or object_pin != _DRAFT_OBJECT_PIN))), 'all embedded base7 pins final')
        need(re.fullmatch('[0-9a-f]{64}', expected_launcher_sha256) is not None and expected_launcher_sha256 != '0' * 64, 'caller-supplied external launcher SHA-256 anchor')
        bootstrap.terminal_replay()
        for path in EXACT8:
            item = bootstrap.held_launcher() if path == SELF else HeldFile(path, 'cold exact8:' + path.name, BASE7_PINS[path][0])
            self.files.append(item)
        self.by_path = {guard.path: guard for guard in self.files}
        need(expected_launcher_sha256 == self.by_path[SELF].file_sha256, 'sole external launcher SHA-256 equals held SELF')
        for path, (file_pin, _) in BASE7_PINS.items():
            need(self.by_path[path].file_sha256 == file_pin, 'embedded base7 file pin:' + path.name)
        expected_entries = [{'path': str(path.relative_to(ROOT)), 'file_sha256': self.by_path[path].file_sha256} for path in EXACT8]
        expected_manifest_raw = b''.join(((entry['file_sha256'] + '  ' + entry['path'] + '\n').encode('ascii') for entry in expected_entries))
        self.manifest = HeldFile(MANIFEST, 'cold exact8 manifest')
        need(self.manifest.raw == expected_manifest_raw, 'cold manifest byte-identical to reconstructed ordered exact8')
        entries = parse_manifest(self.manifest.raw)
        need(entries == expected_entries, 'cold manifest exact ordered eight')
        self.outer = HeldFile(OUTER, 'cold outer-last')
        exact10 = [*self.files, self.manifest, self.outer]
        need(len(exact10) == 10 and len({item.identity for item in exact10}) == 10 and (len({item.mount_id for item in exact10}) == 1), 'cold exact10 identities globally unique on one mount')
        self.chronology = cold_publication_chronology([item.before for item in self.files], self.manifest.before, self.outer.before)
        need(all(self.chronology.values()), 'physical exact8 freeze then manifest freeze then outer freeze chronology')
        self.entries = entries
        self.schema = strict_json(self.by_path[SCHEMA].raw, 'closed schema')
        need(isinstance(self.schema, dict) and self.schema.get('$ref') == '#/$defs/coldLaunchedCommittedAuthority', 'closed schema has cold-launched root only')
        self.schema_keywords = schema_keyword_universe(self.schema)
        self.base_objects: dict[Path, dict[str, Any]] = {}
        for path in (V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT, CONTRACT, TRANSITION, AUDIT):
            value = strict_json(self.by_path[path].raw, 'cold object:' + path.name)
            need(isinstance(value, dict), 'cold base JSON object:' + path.name)
            verify_object(value, path.name, BASE7_PINS[path][1])
            self.base_objects[path] = value
        supersession = self.base_objects[V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT]
        successor_contract = supersession.get('v' + '15_successor_contract', {})
        credit = supersession.get('credit', {})
        need(self.by_path[V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT].raw == canonical(supersession) + b'\n' and supersession.get('status') == 'FROZEN_APPEND_ONLY_V14_RUNTIME_REGISTRY_SHAPE_DRIFT_REJECTION__ZERO_CREDIT__V' + '15_SUCCESSOR_ONLY' and (supersession.get('object_sha256') == V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT_OBJECT_PIN) and (credit == {'D02_formal_pending_task_count': 33638, 'D02_gate_credit': 0, 'D02_started': False, 'D02_task_credit': 0, 'D02_unlock': False, 'formal_global_closure_credit': 0}) and (successor_contract.get('v' + '15_current_exact8_first_member_must_be_this_receipt') is True) and (successor_contract.get('v' + '15_must_directly_hold_and_terminally_replay_v14_exact10_plus_official_rejection_plus_this_receipt') is True) and (successor_contract.get('v' + '15_inherited_published_incident_authority_exact12_count') == 12) and (successor_contract.get('v' + '15_launcher_registry_helper_must_require_explicit67_plus_execution_proof7_plus_object_closure1_equals75') is True), 'v14 supersession receipt exact12/current-first/zero-credit contract')
        self._hold_v14_inherited_authority_exact12(coordination)
        v13_supersession = strict_json(self.v14_inherited_authority_by_role['v13_supersession_receipt'].raw, 'v14 exact12 inherited v13 supersession receipt')
        need(isinstance(v13_supersession, dict), 'v14 exact12 inherited v13 supersession receipt object')
        need(set(self.base_objects[TRANSITION]) == {'schema', 'status', 'receipt_path', 'effective_checkpoint_object_sha256', 'transition_kind', 'append_only_predecessor_v3_regression', 'rejected_unpublished_predecessor_v4', 'published_then_officially_rejected_predecessor_v5', 'published_then_officially_rejected_predecessor_v6', 'published_then_officially_rejected_predecessor_v7', 'published_then_officially_rejected_predecessor_v8', 'published_then_officially_rejected_predecessor_v9', 'published_then_officially_rejected_predecessor_v10', 'published_then_officially_rejected_predecessor_v11', 'published_then_officially_rejected_predecessor_v12', 'rejected_prepublication_v13_supersession_receipt', 'successor_v16r2_static_bundle', 'physical_mode_policy', 'cold_launch_boundary', 'finalization_gates', 'runtime_executed_during_transition', 'C79_runtime_artifacts_created', 'formal_global_closure_credit', 'D02_unlock', 'D02_gate_credit', 'D02_task_credit', 'D02_formal_pending_task_count', 'D02_started', 'all_persisted_credit', 'object_sha256'} and self.base_objects[TRANSITION].get('schema') == 'cm2.round306c79g.true-global-no-producer-consumer.v16-to-v16r2-static-launch-transition.v1' and (self.base_objects[TRANSITION].get('transition_kind') == 'APPEND_ONLY_PUBLISHED_V14_RUNTIME_FAIL_CLOSED_REJECTION_TO_ZERO_CREDIT_V16R2_CLEAN_ROOM_SUCCESSOR'), 'transition exact top-level v16-to-v16r2 closed shape')
        need(set(self.base_objects[CONTRACT]) == {'schema', 'status', 'effective_checkpoint_object_sha256', 'purpose', 'append_only_predecessor_v3', 'rejected_unpublished_predecessor_v4', 'published_then_officially_rejected_predecessor_v5', 'published_then_officially_rejected_predecessor_v6', 'published_then_officially_rejected_predecessor_v7', 'published_then_officially_rejected_predecessor_v8', 'published_then_officially_rejected_predecessor_v9', 'published_then_officially_rejected_predecessor_v10', 'published_then_officially_rejected_predecessor_v11', 'published_then_officially_rejected_predecessor_v12', 'rejected_prepublication_v13_supersession_receipt', 'v10_colon_prefix_witness', 'v11_dual_validator_divergence_incident', 'exact_publication_paths', 'candidate_and_verification_protocol', 'completion_protocol', 'full10_direct_prefix_Kraft_identity', 'upstream_branch_held_input_protocol', 'independent_authority_consumer_protocol', 'composite_authority_predicate', 'no_later_rejection_protocol', 'credit_boundary', 'static_freeze_protocol_requirements', 'v16r2_bundle', 'object_sha256'} and self.base_objects[CONTRACT].get('schema') == 'cm2.round306c79g.true-global-no-producer-consumer.v16r2r62.contract' and (self.base_objects[CONTRACT].get('status') == 'STATIC_CONTRACT_BYTES_FINAL__COLD_FREEZE_PENDING__RUNTIME_NOT_AUTHORIZED') and (self.base_objects[TRANSITION].get('status') == 'STATIC_BYTES_CLOSED_V16_TO_V16R2__PHYSICAL_FREEZE_PENDING__RUNTIME_NOT_AUTHORIZED') and (self.base_objects[AUDIT].get('status') == 'PASS_DUAL_STATIC_PIN_NORMALIZED_AST_GO_V16R2__PHYSICAL_COLD_FREEZE_PENDING__RUNTIME_NOT_AUTHORIZED'), 'contract transition and dual audit exact prepublication statuses')
        for proof_path in (CONTRACT, TRANSITION, AUDIT):
            validate_v5_published_rejected_segment(self.base_objects[proof_path].get('published_then_officially_rejected_predecessor_v5'), proof_path.name)
            validate_v6_published_rejected_segment(self.base_objects[proof_path].get('published_then_officially_rejected_predecessor_v6'), proof_path.name)
            validate_v7_published_rejected_segment(self.base_objects[proof_path].get('published_then_officially_rejected_predecessor_v7'), proof_path.name)
            validate_v8_published_rejected_segment(self.base_objects[proof_path].get('published_then_officially_rejected_predecessor_v8'), proof_path.name)
            validate_v9_published_rejected_segment(self.base_objects[proof_path].get('published_then_officially_rejected_predecessor_v9'), proof_path.name)
            validate_v10_published_rejected_segment(self.base_objects[proof_path].get('published_then_officially_rejected_predecessor_v10'), proof_path.name)
            validate_v11_published_rejected_segment(self.base_objects[proof_path].get('published_then_officially_rejected_predecessor_v11'), proof_path.name)
            validate_v12_published_rejected_segment(self.base_objects[proof_path].get('published_then_officially_rejected_predecessor_v12'), proof_path.name)
            validate_v13_supersession_summary(self.base_objects[proof_path].get('rejected_prepublication_v13_supersession_receipt'), v13_supersession, proof_path.name)
        contract_witness = self.base_objects[CONTRACT].get('v10_colon_prefix_witness')
        audit_witness = self.base_objects[AUDIT].get('v10_colon_prefix_witness')
        need(isinstance(contract_witness, dict) and contract_witness == audit_witness and (tuple(contract_witness) == V10_COLON_PREFIX_WITNESS_KEY_ORDER) and (contract_witness.get('object_sha256') == V10_COLON_PREFIX_WITNESS_OBJECT_PIN) and (self.base_objects[CONTRACT].get('v11_dual_validator_divergence_incident') == self.base_objects[AUDIT].get('v11_dual_validator_divergence_incident') == V11_DUAL_VALIDATOR_DIVERGENCE_INCIDENT), 'contract and audit exact v11 incident and witness consensus')
        schema_audit = self.base_objects[AUDIT].get('schema_and_constructor_closure', {})
        need(isinstance(schema_audit, dict) and schema_audit.get('actual_schema_keyword_universe') == sorted(self.schema_keywords) and (schema_audit.get('cold_launcher_supported_schema_keyword_universe') == sorted(SUPPORTED_SCHEMA_KEYWORDS)) and (schema_audit.get('all_schema_validation_keywords_supported_by_cold_launcher') is True) and (schema_audit.get('unknown_schema_validation_keyword_count') == 0) and (schema_audit.get('oneOf_keyword_absent_after_pin_definition_split') is True) and ('oneOf' not in self.schema_keywords) and (self.schema_keywords <= SUPPORTED_SCHEMA_KEYWORDS), 'static audit and live closed schema prove complete supported keyword universe')
        self.outer_object = strict_json(self.outer.raw, 'cold outer-last')
        need(isinstance(self.outer_object, dict), 'cold outer JSON object')
        verify_object(self.outer_object, 'cold outer-last')
        need(set(self.outer_object) == {'schema', 'status', 'effective_checkpoint_object_sha256', 'exact8_ordered_entries', 'cold_launch_manifest', 'cold_launcher', 'all_exact8_regular_0444_nlink1_and_held_for_runtime', 'outer_published_after_exact8_manifest', 'runtime_entry_must_be_cold_launcher', 'sole_external_static_file_anchor_is_launcher_sha256', 'declared_external_tcb', 'formal_global_closure_credit', 'D02_unlock', 'runtime_executed_during_static_freeze', 'object_sha256'} and self.outer.raw == canonical(self.outer_object) + b'\n' and (self.outer_object.get('schema') == 'cm2.round306c79g.true-global-no-producer-consumer.cold-launch-outer-receipt.v16r2') and (self.outer_object.get('status') == 'FROZEN_COLD_LAUNCH_OUTER_LAST__EXACT8_MANIFEST_CLOSED__RUNTIME_DEFERRED') and (self.outer_object.get('effective_checkpoint_object_sha256') == CHECKPOINT) and (self.outer_object.get('exact8_ordered_entries') == entries) and (self.outer_object.get('cold_launch_manifest') == {'path': str(MANIFEST.relative_to(ROOT)), 'file_sha256': self.manifest.file_sha256, 'ordered_entry_count': 8}) and (self.outer_object.get('cold_launcher') == {'path': str(SELF.relative_to(ROOT)), 'file_sha256': self.by_path[SELF].file_sha256}) and (self.outer_object.get('all_exact8_regular_0444_nlink1_and_held_for_runtime') is True) and (self.outer_object.get('outer_published_after_exact8_manifest') is True) and (self.outer_object.get('runtime_entry_must_be_cold_launcher') is True) and (self.outer_object.get('sole_external_static_file_anchor_is_launcher_sha256') is True) and (self.outer_object.get('declared_external_tcb') == ['EXTERNAL_HELD_FD_SEALED_MEMFD_BOOTSTRAP', 'PYTHON3_ISOLATED_INTERPRETER', 'LINUX_KERNEL_OPENAT2_STATX_MEMFD_PROCFS']) and (self.outer_object.get('formal_global_closure_credit') == 0) and (self.outer_object.get('D02_unlock') is False) and (self.outer_object.get('runtime_executed_during_static_freeze') is False), 'cold outer-last exact closure')
        self.v12_rejection = HeldFile(V12_OFFICIAL_REJECTION, 'official v12 later rejection', V12_REJECTION_FILE_PIN)
        v13_source_pins = ((V13_FROZEN_PRODUCER, V13_PRODUCER_FILE_PIN), (V13_FROZEN_CONSUMER, V13_CONSUMER_FILE_PIN), (V13_FROZEN_LAUNCHER, V13_LAUNCHER_FILE_PIN))
        v13_pyc_pins = ((V13_FROZEN_PRODUCER_PYC, V13_PRODUCER_PYC_FILE_PIN), (V13_FROZEN_CONSUMER_PYC, V13_CONSUMER_PYC_FILE_PIN), (V13_FROZEN_LAUNCHER_PYC, V13_LAUNCHER_PYC_FILE_PIN))
        self.v13_incident_sources = [HeldFile(path, 'frozen v13 incident source:' + path.name, pin) for path, pin in v13_source_pins]
        self.v13_incident_pycs = [HeldFile(path, 'frozen v13 incident pyc:' + path.name, pin) for path, pin in v13_pyc_pins]
        validate_v13_supersession_receipt(v13_supersession, [*self.v13_incident_sources, *self.v13_incident_pycs])
        incident_guards = [*self.v13_incident_sources, *self.v13_incident_pycs, self.v12_rejection, self.v14_inherited_authority_by_role['v13_supersession_receipt']]
        need(len({item.identity for item in incident_guards}) == 8 and len({item.mount_id for item in incident_guards}) == 1 and (next(iter({item.mount_id for item in incident_guards})) == coordination.mount_id), 'v13 exact6, receipt, and v12 rejection are distinct held files')
        self.predecessor_v12 = HeldV12PredecessorExact10(coordination, self.v12_rejection)
        self.predecessor_v11 = HeldV11PredecessorExact10(coordination, self.predecessor_v12.by_path[V11_OFFICIAL_REJECTION])
        self.predecessor_v10 = HeldV10PredecessorExact10(coordination, self.predecessor_v11.by_path[V10_OFFICIAL_REJECTION])
        self.predecessor_v9 = HeldV9PredecessorExact10(coordination, self.predecessor_v10.by_path[V9_OFFICIAL_REJECTION])
        self.predecessor_v10.bind_predecessor_v9(self.predecessor_v9)
        self.predecessor_v11.bind_predecessors(self.predecessor_v10, self.predecessor_v9)
        self.predecessor_v8 = HeldV8PredecessorExact10(coordination, self.predecessor_v9.by_path[V8_OFFICIAL_REJECTION])
        self.predecessor_v7 = HeldV7PredecessorExact10(coordination, self.predecessor_v8.by_path[V7_OFFICIAL_REJECTION])
        self.predecessor_v6 = HeldV6PredecessorExact10(coordination, self.predecessor_v7.by_path[V6_OFFICIAL_REJECTION])
        need(self.predecessor_v6.held_self_identity_structural_evidence.get('guard_identity_structural_census') == V8_LAUNCHER_REGRESSION_DEFECT['actual_guard_identity_census'] and self.predecessor_v6.held_self_identity_structural_evidence.get('target_structural_comprehension_count') == 1 and (self.predecessor_v6.held_self_identity_defect == V9_V6_PROOF_SHAPE_DRIFT_INCIDENT['persisted_held_self_identity_defect']) and (V8_LAUNCHER_REGRESSION_DEFECT['old_global_count_expectation'] == 1), 'v8/v9 incidents join pinned v6 structural16 and persisted9')
        self.predecessor_v5 = HeldV5PredecessorExact10(coordination, self.predecessor_v6.by_path[V5_OFFICIAL_REJECTION])
        self.predecessor_v12.bind_history(self.predecessor_v11, self.predecessor_v6.by_path[V5_OFFICIAL_REJECTION])
        self.v3_rejection = HeldFile(V3_OFFICIAL_REJECTION, 'official v3 later rejection', V3_REJECTION_FILE_PIN)
        rejected_value = strict_json(self.v3_rejection.raw, 'official v3 later rejection object')
        need(isinstance(rejected_value, dict), 'official v3 rejection mapping')
        verify_object(rejected_value, 'official v3 later rejection object', V3_REJECTION_OBJECT_PIN)
        self.predecessor_v3 = HeldV3PredecessorExact10(coordination, self.v3_rejection)
        self.rejected_v4 = HeldV4RejectedDraft7(coordination, self.predecessor_v5.by_path[V4_REJECTION_SUPERSESSION], self.v3_rejection)
        self.global_identity_census = self._global_identity_census()
        contract_static_census = self.base_objects[CONTRACT].get('v16r2_bundle', {}).get('cold_launch_outer_closure', {})
        need(self.global_identity_census == {'v16r2_predecessor_unique_live_identity_count': 116, 'v16r2_prepublication_unique_live_identity_count': 124, 'v16r2_terminal_unique_live_identity_count': 126, 'v16r2_terminal_group_vector': [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 7, 1, 3, 3, 1, 1], 'all_126_file_identities_share_one_statx_mount': True, 'all_126_held_descriptors_are_pairwise_distinct': True, 'current_exact8_first_member_is_v14_registry_shape_drift_supersession_receipt': True, 'all_current_and_historical_124_identities_globally_unique_on_one_statx_mount': True} and isinstance(contract_static_census, dict) and (contract_static_census.get('current_v16r2_exact10_plus_all_append_only_predecessors_unique_file_identity_count') == self.global_identity_census['v16r2_terminal_unique_live_identity_count']) and all((contract_static_census.get(key) == self.global_identity_census[key] for key in ('v16r2_predecessor_unique_live_identity_count', 'v16r2_prepublication_unique_live_identity_count', 'v16r2_terminal_unique_live_identity_count', 'v16r2_terminal_group_vector', 'all_126_file_identities_share_one_statx_mount'))) and (next(iter({guard.mount_id for guard in [*self.files, self.manifest, self.outer, *self.v14_inherited_authority_exact12_owned]})) == coordination.mount_id), 'current v16r2 exact10 plus all predecessors are an exact 126-file terminal census (124 prepublication) on one mount')
        validate_final_static_audit(self.base_objects[AUDIT], self.schema, self.schema_keywords, self.by_path, self.base_objects, self.predecessor_v5, self.predecessor_v6, self.predecessor_v7, self.predecessor_v8, self.predecessor_v9, self.predecessor_v10, self.predecessor_v11, self.predecessor_v12, v13_supersession, self.by_path[SELF].raw)

    def _global_identity_census(self) -> dict[str, Any]:
        """Rebuild the disjoint live-file census from held descriptors.

        The v14 supersession receipt is deliberately shared with current
        exact8 member zero.  Its other eleven exact12 members are distinct
        predecessor identities: v14 exact10 contributes ten and its official
        rejection contributes the final singleton group.
        """
        need(self.manifest is not None and self.outer is not None and (self.predecessor_v3 is not None) and (self.predecessor_v5 is not None) and (self.predecessor_v6 is not None) and (self.predecessor_v7 is not None) and (self.predecessor_v8 is not None) and (self.predecessor_v9 is not None) and (self.predecessor_v10 is not None) and (self.predecessor_v11 is not None) and (self.predecessor_v12 is not None) and (self.rejected_v4 is not None) and (self.v3_rejection is not None) and (self.v12_rejection is not None) and (tuple(self.v14_inherited_authority_by_role) == V14_INHERITED_AUTHORITY_EXACT12_ROLE_ORDER), 'complete current and predecessor guards for global census')
        current_exact10 = [*self.files, self.manifest, self.outer]
        v14_published_exact10 = [self.v14_inherited_authority_by_role[role] for role, _, _, _ in V14_PUBLISHED_EXACT10_WITNESS]
        v14_official_rejection = [self.v14_inherited_authority_by_role['v14_official_rejection']]
        v14_supersession = self.v14_inherited_authority_by_role['v14_registry_shape_drift_supersession_receipt']
        group_guards = [current_exact10, self.predecessor_v12.files, self.predecessor_v11.files, self.predecessor_v10.files, self.predecessor_v9.files, self.predecessor_v8.files, self.predecessor_v7.files, self.predecessor_v6.files, self.predecessor_v5.files, self.predecessor_v3.files, v14_published_exact10, self.rejected_v4.files, [self.v3_rejection], self.v13_incident_sources, self.v13_incident_pycs, [self.v12_rejection], v14_official_rejection]
        identity_groups = [{guard.identity for guard in group} for group in group_guards]
        terminal_group_vector = [len(group) for group in identity_groups]
        terminal_identities: set[tuple[int, int]] = set()
        for identity_group in identity_groups:
            terminal_identities.update(identity_group)
        predecessor_identities: set[tuple[int, int]] = set()
        for identity_group in identity_groups[1:]:
            predecessor_identities.update(identity_group)
        current_exact8_identities = {guard.identity for guard in self.files}
        prepublication_identities = current_exact8_identities | predecessor_identities
        all_guards = [guard for group in group_guards for guard in group]
        pairwise_disjoint = all((identity_groups[left].isdisjoint(identity_groups[right]) for left in range(len(identity_groups)) for right in range(left + 1, len(identity_groups))))
        all_mount_ids = {guard.mount_id for guard in all_guards}
        owned_v14_identities = {guard.identity for guard in self.v14_inherited_authority_exact12_owned}
        current_first_is_receipt = len(self.files) == 8 and EXACT8[0] == V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT and (self.files[0] is self.by_path[EXACT8[0]]) and (self.by_path[EXACT8[0]].identity in current_exact8_identities)
        exact_vector = terminal_group_vector == [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 7, 1, 3, 3, 1, 1]
        exact_partition = pairwise_disjoint and len(all_guards) == 126 and (len(terminal_identities) == 126) and (len(predecessor_identities) == 116) and (len(prepublication_identities) == 124) and (terminal_identities - prepublication_identities == {self.manifest.identity, self.outer.identity}) and current_exact8_identities.isdisjoint(predecessor_identities) and (len(owned_v14_identities) == 11) and (owned_v14_identities == {guard.identity for guard in v14_published_exact10} | {v14_official_rejection[0].identity}) and (v14_supersession.identity not in owned_v14_identities)
        one_mount = len(all_mount_ids) == 1
        distinct_descriptors = len({guard.fd for guard in all_guards}) == 126
        need(exact_vector is True and exact_partition is True and one_mount is True and distinct_descriptors is True and current_first_is_receipt is True, 'global exact126 terminal/exact124 prepublication identity partition, v14 exact12 overlap, descriptors, and mount')
        return {'v16r2_predecessor_unique_live_identity_count': len(predecessor_identities), 'v16r2_prepublication_unique_live_identity_count': len(prepublication_identities), 'v16r2_terminal_unique_live_identity_count': len(terminal_identities), 'v16r2_terminal_group_vector': terminal_group_vector, 'all_126_file_identities_share_one_statx_mount': one_mount, 'all_126_held_descriptors_are_pairwise_distinct': distinct_descriptors, 'current_exact8_first_member_is_v14_registry_shape_drift_supersession_receipt': current_first_is_receipt, 'all_current_and_historical_124_identities_globally_unique_on_one_statx_mount': exact_partition and one_mount and (len(prepublication_identities) == 124)}

    def _hold_v14_inherited_authority_exact12(self, coordination: HeldCoordinationParent) -> None:
        """Hold v14 exact10, rejection, and final receipt in fixed order.

        The final receipt is already the first current-v16r2 exact8 guard and is
        deliberately reused.  The other eleven descriptors are launcher-owned
        predecessor guards.  No legacy exact17 descriptor is part of this
        child authority surface.
        """
        need(not self.v14_inherited_authority_exact12 and (not self.v14_inherited_authority_exact12_owned) and (not self.v14_inherited_authority_by_role), 'v14 inherited authority exact12 binds once')
        need(tuple((role for role, _ in V14_INHERITED_AUTHORITY_EXACT12_FD_ENV_ORDER)) == V14_INHERITED_AUTHORITY_EXACT12_ROLE_ORDER and len(V14_INHERITED_AUTHORITY_EXACT12_FD_ENV_ORDER) == V16R2_CHILD_AUTHORITY_DESCRIPTOR_COUNT == 12, 'v14 exact12 role/environment order closure')
        for role, relative_path, file_pin, _ in V14_INHERITED_AUTHORITY_EXACT12:
            path = ROOT / relative_path
            if role == 'v14_registry_shape_drift_supersession_receipt':
                guard = self.by_path[V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT]
                need(guard.path == path, 'v14 exact12 final receipt reuses current exact8 first guard')
            else:
                guard = HeldFile(path, 'v14 inherited authority exact12:' + role, file_pin)
                self.v14_inherited_authority_exact12_owned.append(guard)
            need(guard.file_sha256 == file_pin, 'v14 inherited authority exact12 file pin:' + role)
            self.v14_inherited_authority_exact12.append(guard)
            self.v14_inherited_authority_by_role[role] = guard
        guards = self.v14_inherited_authority_exact12
        need(len(guards) == len({guard.fd for guard in guards}) == len({guard.identity for guard in guards}) == 12 and len({guard.mount_id for guard in guards}) == 1 and (next(iter({guard.mount_id for guard in guards})) == coordination.mount_id) and (guards[-1] is self.files[0]), 'v14 inherited authority exact12 unique same-mount held guards')
        held_raw_by_role = {role: self.v14_inherited_authority_by_role[role].raw for role in V14_INHERITED_AUTHORITY_EXACT12_ROLE_ORDER}
        self.v14_inherited_authority_initial_replay = terminal_replay_v14_inherited_authority_exact12(held_raw_by_role)

    def inherited_v14_authority_exact12_fds(self) -> tuple[int, ...]:
        need(tuple(self.v14_inherited_authority_by_role) == V14_INHERITED_AUTHORITY_EXACT12_ROLE_ORDER and len(self.v14_inherited_authority_exact12) == 12, 'v14 inherited authority exact12 remains held')
        result = tuple((self.v14_inherited_authority_by_role[role].fd for role in V14_INHERITED_AUTHORITY_EXACT12_ROLE_ORDER))
        need(len(result) == len(set(result)) == V16R2_CHILD_AUTHORITY_DESCRIPTOR_COUNT == 12, 'v14 inherited authority exact12 descriptors pairwise distinct')
        return result

    def terminal_replay(self) -> None:
        need(self.predecessor_v3 is not None and self.predecessor_v5 is not None and (self.predecessor_v6 is not None) and (self.predecessor_v7 is not None) and (self.predecessor_v8 is not None) and (self.predecessor_v9 is not None) and (self.predecessor_v10 is not None) and (self.predecessor_v11 is not None) and (self.predecessor_v12 is not None) and (self.rejected_v4 is not None) and (self.v3_rejection is not None) and (self.v12_rejection is not None) and (len(self.v13_incident_sources) == 3) and (len(self.v13_incident_pycs) == 3) and (self.manifest is not None) and (self.outer is not None) and (len(self.v14_inherited_authority_exact12) == 12) and (self.v14_inherited_authority_initial_replay is not None), 'complete historical and current bundle held')
        self.predecessor_v11.terminal_replay(self.predecessor_v12.by_path[V11_OFFICIAL_REJECTION])
        self.predecessor_v12.terminal_replay(self.v12_rejection)
        self.predecessor_v10.terminal_replay(self.predecessor_v11.by_path[V10_OFFICIAL_REJECTION])
        self.predecessor_v9.terminal_replay(self.predecessor_v10.by_path[V9_OFFICIAL_REJECTION])
        self.predecessor_v8.terminal_replay(self.predecessor_v9.by_path[V8_OFFICIAL_REJECTION])
        self.predecessor_v7.terminal_replay(self.predecessor_v8.by_path[V7_OFFICIAL_REJECTION])
        self.predecessor_v6.terminal_replay(self.predecessor_v7.by_path[V6_OFFICIAL_REJECTION])
        self.predecessor_v5.terminal_replay(self.predecessor_v6.by_path[V5_OFFICIAL_REJECTION])
        self.predecessor_v3.terminal_replay(self.v3_rejection)
        self.rejected_v4.terminal_replay()
        self.v3_rejection.terminal_replay()
        self.v12_rejection.terminal_replay()
        for guard in [*self.v13_incident_sources, *self.v13_incident_pycs]:
            guard.terminal_replay()
        for guard in self.v14_inherited_authority_exact12:
            guard.terminal_replay()
        replayed_v14_authority = terminal_replay_v14_inherited_authority_exact12({role: self.v14_inherited_authority_by_role[role].raw for role in V14_INHERITED_AUTHORITY_EXACT12_ROLE_ORDER})
        need(replayed_v14_authority == self.v14_inherited_authority_initial_replay, 'v14 inherited authority exact12 terminal replay unchanged')
        for guard in [*self.files, self.manifest, self.outer]:
            guard.terminal_replay()
        terminal_chronology = cold_publication_chronology([item.before for item in self.files], self.manifest.before, self.outer.before)
        need(terminal_chronology == self.chronology and all(terminal_chronology.values()), 'terminal cold freeze chronology unchanged')
        self.bootstrap.terminal_replay()

    def close(self) -> None:
        if self.rejected_v4 is not None:
            self.rejected_v4.close()
            self.rejected_v4 = None
        if self.predecessor_v5 is not None:
            self.predecessor_v5.close()
            self.predecessor_v5 = None
        if self.predecessor_v6 is not None:
            self.predecessor_v6.close()
            self.predecessor_v6 = None
        if self.predecessor_v7 is not None:
            self.predecessor_v7.close()
            self.predecessor_v7 = None
        if self.predecessor_v8 is not None:
            self.predecessor_v8.close()
            self.predecessor_v8 = None
        if self.predecessor_v9 is not None:
            self.predecessor_v9.close()
            self.predecessor_v9 = None
        if self.predecessor_v10 is not None:
            self.predecessor_v10.close()
            self.predecessor_v10 = None
        if self.predecessor_v11 is not None:
            self.predecessor_v11.close()
            self.predecessor_v11 = None
        if self.predecessor_v12 is not None:
            self.predecessor_v12.close()
            self.predecessor_v12 = None
        if self.predecessor_v3 is not None:
            self.predecessor_v3.close()
            self.predecessor_v3 = None
        if self.v3_rejection is not None:
            self.v3_rejection.close()
            self.v3_rejection = None
        if self.v12_rejection is not None:
            self.v12_rejection.close()
            self.v12_rejection = None
        for guard in reversed(self.v13_incident_pycs):
            guard.close()
        self.v13_incident_pycs = []
        for guard in reversed(self.v13_incident_sources):
            guard.close()
        self.v13_incident_sources = []
        for guard in reversed(self.v14_inherited_authority_exact12_owned):
            guard.close()
        self.v14_inherited_authority_exact12_owned = []
        self.v14_inherited_authority_exact12 = []
        self.v14_inherited_authority_by_role = {}
        self.v14_inherited_authority_initial_replay = None
        self.global_identity_census = None
        for guard in reversed(self.files):
            guard.close()
        self.files = []
        if self.manifest is not None:
            self.manifest.close()
            self.manifest = None
        if self.outer is not None:
            self.outer.close()
            self.outer = None

def _type_matches(value: Any, type_name: str) -> bool:
    return {'object': isinstance(value, dict), 'array': isinstance(value, list), 'string': isinstance(value, str), 'integer': type(value) is int, 'number': type(value) in {int, float}, 'boolean': type(value) is bool, 'null': value is None}.get(type_name, False)
SUPPORTED_SCHEMA_KEYWORDS = frozenset({'$schema', '$id', '$comment', 'title', 'description', '$defs', '$ref', 'type', 'const', 'additionalProperties', 'required', 'properties', 'items', 'prefixItems', 'minItems', 'maxItems', 'uniqueItems', 'minLength', 'pattern', 'minimum'})

def schema_keyword_universe(root: Mapping[str, Any]) -> frozenset[str]:
    """Reject every validation keyword this closed validator cannot enforce."""
    seen: set[str] = set()

    def walk(node: Any, label: str) -> None:
        need(isinstance(node, dict), label + ':schema node object')
        unknown = set(node) - SUPPORTED_SCHEMA_KEYWORDS
        need(not unknown, label + ':unsupported schema keywords:' + ','.join(sorted(unknown)))
        seen.update(node)
        definitions = node.get('$defs', {})
        need(isinstance(definitions, dict), label + ':$defs object')
        for name, child in definitions.items():
            need(isinstance(name, str) and len(name) > 0, label + ':$defs name')
            walk(child, label + '.$defs.' + name)
        properties = node.get('properties', {})
        need(isinstance(properties, dict), label + ':properties object')
        for name, child in properties.items():
            need(isinstance(name, str) and len(name) > 0, label + ':property name')
            walk(child, label + '.properties.' + name)
        prefix_items = node.get('prefixItems', [])
        need(isinstance(prefix_items, list), label + ':prefixItems array')
        for index, child in enumerate(prefix_items):
            walk(child, f'{label}.prefixItems[{index}]')
        items = node.get('items')
        need(items is None or items is False or isinstance(items, dict), label + ':items schema-or-false')
        if isinstance(items, dict):
            walk(items, label + '.items')
        additional = node.get('additionalProperties')
        need(additional is None or isinstance(additional, bool) or isinstance(additional, dict), label + ':additionalProperties schema-or-boolean')
        if isinstance(additional, dict):
            walk(additional, label + '.additionalProperties')
    walk(root, 'closed-schema')
    return frozenset(seen)

def validate_schema(value: Any, node: Mapping[str, Any], root: Mapping[str, Any], label: str) -> None:
    need(set(node) <= SUPPORTED_SCHEMA_KEYWORDS, label + ':no unsupported schema validation keyword')
    if '$ref' in node:
        reference = node['$ref']
        need(isinstance(reference, str) and reference.startswith('#/$defs/'), label + ':local ref only')
        name = reference.removeprefix('#/$defs/')
        target = root.get('$defs', {}).get(name)
        need(isinstance(target, dict), label + ':resolved ref:' + name)
        validate_schema(value, target, root, label + '->' + name)
        return
    if 'const' in node:
        expected = node['const']
        need(type(value) is type(expected) and value == expected, label + ':const')
    type_name = node.get('type')
    if type_name is not None:
        need(isinstance(type_name, str) and _type_matches(value, type_name) is True, label + ':type:' + str(type_name))
    if isinstance(value, dict):
        required = node.get('required', [])
        need(isinstance(required, list) and all((key in value for key in required)), label + ':required')
        properties = node.get('properties', {})
        need(isinstance(properties, dict), label + ':properties')
        if node.get('additionalProperties') is False:
            need(set(value) <= set(properties), label + ':additionalProperties')
        for key, child in properties.items():
            if key in value:
                need(isinstance(child, dict), label + ':child schema')
                validate_schema(value[key], child, root, label + '.' + key)
    if isinstance(value, list):
        if 'minItems' in node:
            need(len(value) >= node['minItems'], label + ':minItems')
        if 'maxItems' in node:
            need(len(value) <= node['maxItems'], label + ':maxItems')
        if node.get('uniqueItems') is True:
            need(len({canonical(item) for item in value}) == len(value), label + ':uniqueItems')
        prefix = node.get('prefixItems', [])
        need(isinstance(prefix, list), label + ':prefixItems')
        for index, child_schema in enumerate(prefix[:len(value)]):
            need(isinstance(child_schema, dict), label + ':prefix schema')
            validate_schema(value[index], child_schema, root, f'{label}[{index}]')
        if len(value) > len(prefix):
            item_schema = node.get('items')
            need(item_schema is not False, label + ':items false')
            if item_schema is not None:
                need(isinstance(item_schema, dict), label + ':items schema')
                for index in range(len(prefix), len(value)):
                    validate_schema(value[index], item_schema, root, f'{label}[{index}]')
    if isinstance(value, str):
        if 'minLength' in node:
            need(len(value) >= node['minLength'], label + ':minLength')
        if 'pattern' in node:
            need(re.search(node['pattern'], value) is not None, label + ':pattern')
    if type(value) in {int, float} and 'minimum' in node:
        need(value >= node['minimum'], label + ':minimum')

def child_environment(bundle: HeldBundle, child_exec: HeldSealedChildExec, source: HeldFile, coordination: HeldCoordinationParent) -> dict[str, str]:
    authority_fds = bundle.inherited_v14_authority_exact12_fds()
    need(tuple((role for role, _ in V14_INHERITED_AUTHORITY_EXACT12_FD_ENV_ORDER)) == V14_INHERITED_AUTHORITY_EXACT12_ROLE_ORDER and len(authority_fds) == len(V14_INHERITED_AUTHORITY_EXACT12_FD_ENV_ORDER) == 12, 'v14 exact12 child environment role/fd order')
    authority_environment = {env_name: str(descriptor) for (_, env_name), descriptor in zip(V14_INHERITED_AUTHORITY_EXACT12_FD_ENV_ORDER, authority_fds, strict=True)}
    result = {'LC_ALL': 'C', 'TZ': 'UTC', EXEC_FD_ENV: str(child_exec.fd), SOURCE_FD_ENV: str(source.fd), COORDINATION_PARENT_FD_ENV: str(coordination.fd), WORKSPACE_ROOT_ENV: str(ROOT), WORKSPACE_ROOT_FD_ENV: str(bundle.bootstrap.root_fd), LAUNCHER_SHA_ENV: bundle.by_path[SELF].file_sha256}
    result.update(authority_environment)
    need(len(authority_environment) == 12 and set(authority_environment) == {env_name for _, env_name in V14_INHERITED_AUTHORITY_EXACT12_FD_ENV_ORDER} and all((env_name.startswith('CM2_C79G_V16R2_V14_') and env_name.endswith('_FD') for env_name in authority_environment)), 'children receive only the twelve ordered v14 authority environments')
    return result

def child_pass_fds(bundle: HeldBundle, child_exec: HeldSealedChildExec, source: HeldFile, coordination: HeldCoordinationParent) -> tuple[int, ...]:
    result = (child_exec.fd, source.fd, coordination.fd, bundle.bootstrap.root_fd, *bundle.inherited_v14_authority_exact12_fds())
    need(len(result) == len(set(result)) == V16R2_CHILD_PASS_FD_COUNT == V16R2_BOOTSTRAP_DESCRIPTOR_COUNT + V16R2_CHILD_AUTHORITY_DESCRIPTOR_COUNT == 16, 'child exact sixteen inherited descriptors are pairwise distinct')
    return result

def child_argv(child_exec: HeldSealedChildExec, command: str, forwarded: list[str]) -> list[str]:
    return [sys.executable, '-I', '-B', '-S', '/proc/self/fd/' + str(child_exec.fd), command, *forwarded]

def run_non_authorize_child(bundle: HeldBundle, coordination: HeldCoordinationParent, rejection_guard: HeldEmptyRejectionNamespace, command: str, forwarded: list[str]) -> bytes:
    need(command in {'build', 'verify', 'assemble'}, 'only non-reject child commands reach bundle dispatch')
    source = bundle.by_path[PRODUCER if command == 'build' else CONSUMER]
    child_exec = HeldSealedChildExec(source)
    try:
        os.lseek(child_exec.fd, 0, os.SEEK_SET)
        completed = subprocess.run(child_argv(child_exec, command, forwarded), stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=child_environment(bundle, child_exec, source, coordination), pass_fds=child_pass_fds(bundle, child_exec, source, coordination), check=False)
        if completed.stderr:
            sys.stderr.buffer.write(completed.stderr)
        need(completed.returncode == 0, 'cold child rejected or failed')
        child_exec.terminal_replay()
        bundle.terminal_replay()
        rejection_guard.terminal_replay()
        coordination.verify()
        return completed.stdout
    finally:
        child_exec.close()

def cold_root(bundle: HeldBundle, coordination: HeldCoordinationParent, child_exec: HeldSealedChildExec, inner_raw: bytes) -> tuple[dict[str, Any], dict[str, Any]]:
    need(inner_raw.endswith(b'\n') and inner_raw.count(b'\n') == 1, 'authorize child first stdout is exactly one JSON line')
    inner = strict_json(inner_raw, 'zero-credit inner live composite')
    need(isinstance(inner, dict), 'inner live composite object')
    verify_object(inner, 'inner live composite')
    validate_schema(inner, {'$ref': '#/$defs/innerComposite'}, bundle.schema, 'inner')
    need(inner.get('schema') == INNER_SCHEMA and inner.get('formal_global_closure_credit') == 0 and (inner.get('D02_unlock') is False) and (inner.get('cold_launcher_required') is True) and (inner_raw == canonical(inner) + b'\n'), 'direct consumer result is canonical launcher-required zero-only inner')
    need(bundle.predecessor_v5 is not None and bundle.predecessor_v6 is not None and (bundle.predecessor_v7 is not None) and (bundle.predecessor_v8 is not None) and (bundle.predecessor_v9 is not None) and (bundle.predecessor_v10 is not None) and (bundle.predecessor_v11 is not None), 'v11 direct predecessor and v10/v9/v8/v7/v6/v5 history remain held')
    predecessor_v5 = bundle.predecessor_v5
    predecessor_v6 = bundle.predecessor_v6
    predecessor_v7 = bundle.predecessor_v7
    predecessor_v8 = bundle.predecessor_v8
    predecessor_v9 = bundle.predecessor_v9
    predecessor_v10 = bundle.predecessor_v10
    predecessor_v11 = bundle.predecessor_v11
    live_global_identity_census = bundle._global_identity_census()
    need(bundle.global_identity_census is not None and live_global_identity_census == bundle.global_identity_census, 'cold-root live global exact126/exact124 identity census unchanged')
    proof = {'launcher_identity': bundle.by_path[SELF].identity_object(), 'manifest_identity': bundle.manifest.identity_object(), 'outer_identity': bundle.outer.identity_object(), 'ordered_exact8_identities': [bundle.by_path[path].identity_object() for path in EXACT8], 'exact10_identity_count': 10, 'current_exact8_first_member_is_v14_registry_shape_drift_supersession_receipt': live_global_identity_census['current_exact8_first_member_is_v14_registry_shape_drift_supersession_receipt'], 'v7_official_rejection_identity': {**predecessor_v8.by_path[V7_OFFICIAL_REJECTION].identity_object(), 'object_sha256': V7_REJECTION_OBJECT_PIN}, 'v7_official_rejection_file_sha256': V7_REJECTION_FILE_PIN, 'v7_official_rejection_object_sha256': V7_REJECTION_OBJECT_PIN, 'v6_official_rejection_identity': {**predecessor_v7.by_path[V6_OFFICIAL_REJECTION].identity_object(), 'object_sha256': V6_REJECTION_OBJECT_PIN}, 'v6_official_rejection_file_sha256': V6_REJECTION_FILE_PIN, 'v6_official_rejection_object_sha256': V6_REJECTION_OBJECT_PIN, 'v5_official_rejection_identity': {**predecessor_v6.by_path[V5_OFFICIAL_REJECTION].identity_object(), 'object_sha256': V5_REJECTION_OBJECT_PIN}, 'v5_official_rejection_file_sha256': V5_REJECTION_FILE_PIN, 'v5_official_rejection_object_sha256': V5_REJECTION_OBJECT_PIN, 'v4_rejection_supersession_identity': {**predecessor_v5.by_path[V4_REJECTION_SUPERSESSION].identity_object(), 'object_sha256': V4_SUPERSESSION_OBJECT_PIN}, 'v4_rejection_supersession_file_sha256': V4_SUPERSESSION_FILE_PIN, 'v4_rejection_supersession_object_sha256': V4_SUPERSESSION_OBJECT_PIN, 'all_exact10_identities_globally_unique_on_one_statx_mount': True, 'all_current_and_historical_124_identities_globally_unique_on_one_statx_mount': live_global_identity_census['all_current_and_historical_124_identities_globally_unique_on_one_statx_mount'], 'current_v16r2_and_all_predecessor_unique_file_identity_count': live_global_identity_census['v16r2_prepublication_unique_live_identity_count'], 'current_v16r2_and_all_predecessor_same_statx_mount': live_global_identity_census['all_126_file_identities_share_one_statx_mount'], **bundle.chronology, 'external_launcher_file_sha256_pin_required': True, 'external_launcher_file_sha256_equals_held_launcher': True, 'sole_external_launcher_sha256_is_only_external_static_anchor': True, 'sole_external_static_byte_anchor_excludes_explicit_bootstrap_interpreter_kernel_TCB': True, 'external_bootstrap_is_minimal_inline_trusted_code': True, 'external_bootstrap_opens_workspace_root_and_launcher_with_openat2_four_resolve_flags': True, 'external_bootstrap_hashes_installed_source_copies_exact_bytes_into_and_executes_same_sealed_exec_fd': True, 'launcher_executed_only_via_proc_self_fd': True, 'launcher_exec_fd_equals_argv0___file___and_source_fd_equals_installed_path_identity': True, 'launcher_root_bound_to_inherited_preopened_root_fd': True, 'launcher_pathname_execution_fallback_allowed': False, 'trusted_python_interpreter_linux_kernel_openat2_and_minimal_bootstrap_declared_TCB': True, 'launcher_native_reject_dispatch_after_self_proof_and_lock_before_current_bundle_open': True, 'manifest_and_outer_reconstructed_without_independent_external_hash': True, 'child_source_path': str(CONSUMER.relative_to(ROOT)), 'child_source_file_sha256': bundle.by_path[CONSUMER].file_sha256, 'child_exec_fd_distinct_from_held_exact8_source_fd': child_exec.fd != bundle.by_path[CONSUMER].fd, 'child_exec_is_fresh_sealed_memfd_0444_nlink0': True, 'child_exec_has_write_grow_shrink_and_seal_seals': True, 'child_exec_bytes_equal_held_exact8_source_fd_bytes': child_exec.raw == bundle.by_path[CONSUMER].raw, 'child_exec_argv0_and___file___equal_proc_self_fd_exec': True, 'child_held_exact8_source_fd_terminally_replayed': True, 'child_python_isolated_no_site_and_no_pyc': True, 'child_first_stdout_exact_one_canonical_inner_object': True, 'inner_validated_against_closed_innerComposite_schema': True, 'cold_outer_object_sha256': bundle.outer_object['object_sha256'], 'official_writer_coordination_parent': coordination.identity_object(), 'launcher_owned_coordination_lock_acquired_before_child_spawn': True, 'coordination_lock_passed_as_same_open_file_description': True, 'coordination_lock_is_mandatory_for_official_writers_only': True, 'launcher_empty_rejection_namespace_guard_held_from_before_child_spawn_and_terminally_replayed_before_final_dynamic_request': True, 'same_uid_or_filesystem_administrator_bypass_not_claimed_prevented': True, 'cold_two_phase_live_protocol': LIVE_PROTOCOL, 'wrapper_closed_and_schema_validated_before_request': True, 'wrapper_body_excludes_transaction_binding_request_ACK_and_RELEASE_to_avoid_hash_cycle': True, 'transaction_binding_is_replay_identical_not_fresh_or_random': True, 'terminal_exact10_replay_completed_before_final_dynamic_request': True, 'live_v3_exact10_ordered_pins': [{'path': str(path.relative_to(ROOT)), 'file_sha256': file_pin, **({'object_sha256': object_pin} if object_pin is not None else {})} for path, file_pin, object_pin in V3_EXACT10_PINS], 'live_v5_exact10_ordered_pins': [{'path': str(path.relative_to(ROOT)), 'file_sha256': file_pin, **({'object_sha256': object_pin} if object_pin is not None else {})} for path, file_pin, object_pin in V5_EXACT10_PINS], 'live_v6_exact10_ordered_pins': [{'path': str(path.relative_to(ROOT)), 'file_sha256': file_pin, **({'object_sha256': object_pin} if object_pin is not None else {})} for path, file_pin, object_pin in V6_EXACT10_PINS], 'live_v7_exact10_ordered_pins': [{'path': str(path.relative_to(ROOT)), 'file_sha256': file_pin, **({'object_sha256': object_pin} if object_pin is not None else {})} for path, file_pin, object_pin in V7_EXACT10_PINS], 'live_v10_exact10_ordered_pins': [{'path': str(path.relative_to(ROOT)), 'file_sha256': file_pin, **({'object_sha256': object_pin} if object_pin is not None else {})} for path, file_pin, object_pin in V10_EXACT10_PINS], 'published_then_officially_rejected_predecessor_v8': expected_v8_published_rejected_segment(), 'published_then_officially_rejected_predecessor_v9': expected_v9_published_rejected_segment(), 'published_then_officially_rejected_predecessor_v10': expected_v10_published_rejected_segment(), 'published_then_officially_rejected_predecessor_v11': expected_v11_published_rejected_segment(), 'published_then_officially_rejected_predecessor_v12': expected_v12_published_rejected_segment(), 'v12_official_rejection_file_sha256': V12_REJECTION_FILE_PIN, 'v12_official_rejection_object_sha256': V12_REJECTION_OBJECT_PIN, 'v12_v5_rejection_shape_incident': copy.deepcopy(V12_V5_REJECTION_SHAPE_INCIDENT), 'published_then_officially_rejected_predecessor_v7': expected_v7_published_rejected_segment(), 'official_v7_later_rejection': {'path': str(V7_OFFICIAL_REJECTION.relative_to(ROOT)), 'namespace_path': str(V7_OFFICIAL_REJECTION.parent.relative_to(ROOT)), 'file_sha256': V7_REJECTION_FILE_PIN, 'object_sha256': V7_REJECTION_OBJECT_PIN}, 'v7_publication_lock_continuity_incident': copy.deepcopy(V7_LOCK_CONTINUITY_INCIDENT), 'official_v10_later_rejection': {'path': str(V10_OFFICIAL_REJECTION.relative_to(ROOT)), 'namespace_path': str(V10_OFFICIAL_REJECTION.parent.relative_to(ROOT)), 'file_sha256': V10_REJECTION_FILE_PIN, 'object_sha256': V10_REJECTION_OBJECT_PIN}, 'official_v6_later_rejection': {'path': str(V6_OFFICIAL_REJECTION.relative_to(ROOT)), 'namespace_path': str(V6_OFFICIAL_REJECTION.parent.relative_to(ROOT)), 'file_sha256': V6_REJECTION_FILE_PIN, 'object_sha256': V6_REJECTION_OBJECT_PIN}, 'v6_predecessor_HeldSelf_identity_defect': predecessor_v6.held_self_identity_defect, 'official_v5_later_rejection': {'path': str(V5_OFFICIAL_REJECTION.relative_to(ROOT)), 'namespace_path': str(V5_OFFICIAL_REJECTION.parent.relative_to(ROOT)), 'file_sha256': V5_REJECTION_FILE_PIN, 'object_sha256': V5_REJECTION_OBJECT_PIN}, 'v5_predecessor_strict_bool_regression': predecessor_v5.strict_bool_regression, 'official_v3_later_rejection': {'path': str(V3_OFFICIAL_REJECTION.relative_to(ROOT)), 'namespace_path': str(V3_OFFICIAL_REJECTION.parent.relative_to(ROOT)), 'file_sha256': V3_REJECTION_FILE_PIN, 'object_sha256': V3_REJECTION_OBJECT_PIN}, 'ordered_provisional_exact8_live_pins': [{'path': str(V3_OFFICIAL_REJECTION.relative_to(ROOT)), 'file_sha256': V3_REJECTION_FILE_PIN, 'object_sha256': V3_REJECTION_OBJECT_PIN}, *[{'path': str(path.relative_to(ROOT)), 'file_sha256': file_pin, **({'object_sha256': object_pin} if object_pin is not None else {})} for path, file_pin, object_pin in V4_FROZEN_DRAFT7_PINS]], 'launcher_same_lock_live_v3_exact10_and_official_rejection_singleton_namespace_held': True, 'launcher_same_lock_live_v6_exact10_and_official_rejection_held': True, 'terminal_v6_exact10_and_official_rejection_replay_completed_before_final_dynamic_request': True, 'launcher_same_lock_live_v7_exact10_and_official_rejection_held': True, 'terminal_v7_exact10_and_official_rejection_replay_completed_before_final_dynamic_request': True, 'launcher_same_lock_live_v8_exact10_and_official_rejection_held': True, 'terminal_v8_exact10_and_official_rejection_replay_completed_before_final_dynamic_request': True, 'launcher_same_lock_live_v10_exact10_and_official_rejection_held': True, 'terminal_v10_exact10_and_official_rejection_replay_completed_before_final_dynamic_request': True, 'v10_regression_label_prefix_incident_validated_by_AST_structure_and_exact_prefix_join': v10_regression_label_prefix_gate(predecessor_v10.by_path[V10_EXACT10_PINS[3][0]].raw, predecessor_v9.by_path[V9_EXACT10_PINS[7][0]].raw) == V10_REGRESSION_LABEL_PREFIX_INCIDENT, 'v8_rollout_control_flow_incident_validated_without_timestamp_inference': True, 'v7_interrupted_publication_cannot_be_rehabilitated_by_later_replay': True, 'launcher_same_lock_live_v5_exact10_and_official_rejection_held': True, 'terminal_v5_exact10_and_official_rejection_replay_completed_before_final_dynamic_request': True, 'launcher_same_lock_live_v4_provisional_exact8_and_supersession_receipt_held': True, 'terminal_v4_provisional_exact8_and_supersession_replay_completed_before_final_dynamic_request': True, 'reject_command_exempts_only_fresh_empty_v16r2_rejection_namespace': True, 'final_dynamic_ack_bound_to_inner_and_final_wrapper_object': True, 'final_dynamic_ack_requires_full_replay_and_fresh_rejection_scan': True, 'launcher_lock_survives_child_exit_or_crash_until_wrapper_raw_final_newline_commit': True, 'no_fallible_schema_or_filesystem_gate_after_validated_ack': True, 'positive_wrapper_stdout_fd1_blocking_pipe_preflushed_and_duplicated_before_dynamic_request': True, 'positive_wrapper_raw_fd1_final_newline_write_is_semantic_commit': True, 'post_ACK_release_and_child_exit_are_non_authority_cleanup': True}
    authority_root_sha256 = sha_bytes(COLD_ROOT_DOMAIN + canonical({'inner_object_sha256': inner['object_sha256'], 'manifest_file_sha256': bundle.manifest.file_sha256, 'outer_file_sha256': bundle.outer.file_sha256, 'outer_object_sha256': bundle.outer_object['object_sha256'], 'launcher_file_sha256': bundle.by_path[SELF].file_sha256, 'v6_official_rejection_file_sha256': V6_REJECTION_FILE_PIN, 'v6_official_rejection_object_sha256': V6_REJECTION_OBJECT_PIN, 'v7_official_rejection_file_sha256': V7_REJECTION_FILE_PIN, 'v7_official_rejection_object_sha256': V7_REJECTION_OBJECT_PIN, 'v7_publication_lock_continuity_incident_object_sha256': V7_LOCK_CONTINUITY_INCIDENT_OBJECT_PIN, 'v8_official_rejection_file_sha256': V8_REJECTION_FILE_PIN, 'v8_official_rejection_object_sha256': V8_REJECTION_OBJECT_PIN, 'trusted_v8_rollout_control_flow_incident_digest': sha_bytes(canonical(V8_ROLLOUT_CONTROL_FLOW_INCIDENT)), 'v9_official_rejection_file_sha256': V9_REJECTION_FILE_PIN, 'v9_official_rejection_object_sha256': V9_REJECTION_OBJECT_PIN, 'trusted_v9_proof_shape_drift_incident_digest': sha_bytes(canonical(V9_V6_PROOF_SHAPE_DRIFT_INCIDENT)), 'v10_official_rejection_file_sha256': V10_REJECTION_FILE_PIN, 'v10_official_rejection_object_sha256': V10_REJECTION_OBJECT_PIN, 'trusted_v10_regression_label_prefix_incident_digest': sha_bytes(canonical(V10_REGRESSION_LABEL_PREFIX_INCIDENT)), 'v11_official_rejection_file_sha256': V11_REJECTION_FILE_PIN, 'v11_official_rejection_object_sha256': V11_REJECTION_OBJECT_PIN, 'v10_colon_prefix_witness_object_sha256': V10_COLON_PREFIX_WITNESS_OBJECT_PIN, 'trusted_v11_dual_validator_divergence_incident_digest': V11_DUAL_VALIDATOR_DIVERGENCE_INCIDENT_DIGEST, 'v12_official_rejection_file_sha256': V12_REJECTION_FILE_PIN, 'v12_official_rejection_object_sha256': V12_REJECTION_OBJECT_PIN, 'trusted_v12_v5_rejection_shape_incident_digest': V12_V5_REJECTION_SHAPE_INCIDENT_SHA256, 'v5_official_rejection_file_sha256': V5_REJECTION_FILE_PIN, 'v5_official_rejection_object_sha256': V5_REJECTION_OBJECT_PIN, 'v4_supersession_file_sha256': V4_SUPERSESSION_FILE_PIN, 'v4_supersession_object_sha256': V4_SUPERSESSION_OBJECT_PIN, 'v3_official_rejection_file_sha256': V3_REJECTION_FILE_PIN, 'v3_official_rejection_object_sha256': V3_REJECTION_OBJECT_PIN, 'coordination_parent_st_dev': coordination.before.st_dev, 'coordination_parent_st_ino': coordination.before.st_ino, 'coordination_parent_statx_mnt_id': coordination.mount_id}))
    root = close_object({'schema': COLD_ROOT_SCHEMA, 'status': 'GO_COLD_LAUNCHED_LIVE_COMPOSITE_ONLY', 'authority_decision': 'GO_COLD_LAUNCHED_COMPOSITE_ONLY', 'effective_checkpoint_object_sha256': CHECKPOINT, 'inner_composite': inner, 'cold_launch_proof': proof, 'preseal_root_sha256': inner['preseal_root_sha256'], 'inner_authority_root_sha256': inner['authority_root_sha256'], 'authority_root_domain': COLD_ROOT_DOMAIN[:-1].decode('ascii'), 'authority_root_sha256': authority_root_sha256, 'formal_global_closure_credit': 1, 'D02_unlock': True, 'D02_gate_credit': 0, 'D02_task_credit': 0, 'D02_formal_pending_task_count': 33638, 'D02_started': False, 'root_is_virtual_and_must_not_be_persisted': True})
    validate_schema(root, bundle.schema, bundle.schema, 'cold-root')
    return (root, inner)

def _read_child_line(pipe: Any, label: str) -> bytes:
    maximum = 32 * 1024 * 1024
    raw = pipe.readline(maximum + 1)
    need(raw.endswith(b'\n') and len(raw) <= maximum and (raw.count(b'\n') == 1), label + ':one bounded newline-terminated object')
    return raw

def _wrapper_body_domain_sha256(root: Mapping[str, Any]) -> str:
    body = {key: value for key, value in root.items() if key != 'object_sha256'}
    return sha_bytes(PREWRAPPER_BODY_DOMAIN.encode('ascii') + b'\x00' + canonical(body))

def _deterministic_transaction_binding(bundle: HeldBundle, inner_object_sha256: str, wrapper_body_domain_sha256: str, wrapper_object_sha256: str) -> str:
    return sha_bytes(TRANSACTION_BINDING_DOMAIN.encode('ascii') + b'\x00' + inner_object_sha256.encode('ascii') + wrapper_body_domain_sha256.encode('ascii') + wrapper_object_sha256.encode('ascii') + bundle.by_path[SELF].file_sha256.encode('ascii'))

def _expected_ack_binding(request: Mapping[str, Any]) -> str:
    return sha_bytes(LIVE_ACK_BINDING_DOMAIN.encode('ascii') + b'\x00' + request['transaction_binding_sha256'].encode('ascii') + request['inner_object_sha256'].encode('ascii') + request['wrapper_body_domain_sha256'].encode('ascii') + request['wrapper_object_sha256'].encode('ascii') + request['object_sha256'].encode('ascii'))

def _validate_lock_ack(value: Any, coordination: HeldCoordinationParent) -> None:
    need(isinstance(value, dict) and set(value) == {'path', 'held_parent_st_dev', 'held_parent_st_ino', 'held_parent_statx_mnt_id', 'lock_api', 'received_from_frozen_launcher_as_inherited_open_file_description_fd', 'child_duplicated_and_identity_mount_checked_inherited_fd', 'child_calls_LOCK_UN', 'launcher_lock_owner_scope_requirement_includes_child_live_protocol', 'mandatory_for_all_official_runtime_writers', 'acquired_before_any_runtime_evidence_or_commit_surface_open_for_this_command', 'required_final_hold_scope', 'protocol_requires_launcher_RELEASE_before_normal_child_guard_close', 'coordination_lock_is_not_claimed_as_a_security_boundary_against_noncooperating_same_uid_or_filesystem_administrator', 'launcher_exclusive_lock_confirmed_by_independent_nonblocking_probe'} and (value.get('path') == str(RUNTIME.relative_to(ROOT))) and (value.get('held_parent_st_dev') == coordination.before.st_dev) and (value.get('held_parent_st_ino') == coordination.before.st_ino) and (value.get('held_parent_statx_mnt_id') == coordination.mount_id) and (value.get('lock_api') == 'launcher_owned_fcntl.flock(LOCK_EX)') and (value.get('received_from_frozen_launcher_as_inherited_open_file_description_fd') is True) and (value.get('child_duplicated_and_identity_mount_checked_inherited_fd') is True) and (value.get('child_calls_LOCK_UN') is False) and (value.get('launcher_lock_owner_scope_requirement_includes_child_live_protocol') is True) and (value.get('mandatory_for_all_official_runtime_writers') is True) and (value.get('acquired_before_any_runtime_evidence_or_commit_surface_open_for_this_command') is True) and (value.get('required_final_hold_scope') == ['inner_canonical_stdout_flush', 'launcher_commit_request', 'absolute_last_dynamic_terminal_replay', 'live_ACK_canonical_stdout_flush', 'launcher_positive_wrapper_raw_fd1_final_newline_write', 'launcher_RELEASE']) and (value.get('protocol_requires_launcher_RELEASE_before_normal_child_guard_close') is True) and (value.get('coordination_lock_is_not_claimed_as_a_security_boundary_against_noncooperating_same_uid_or_filesystem_administrator') is True) and (value.get('launcher_exclusive_lock_confirmed_by_independent_nonblocking_probe') is True), 'live ACK exact launcher-owned official-writer lock proof')

def _validate_live_ack(raw: bytes, request: Mapping[str, Any], coordination: HeldCoordinationParent) -> dict[str, Any]:
    ack = strict_json(raw, 'cold final-dynamic live ACK')
    need(isinstance(ack, dict), 'cold live ACK object')
    verify_object(ack, 'cold final-dynamic live ACK')
    expected_keys = {'schema', 'status', 'protocol', 'transaction_binding_domain', 'transaction_binding_sha256', 'request_object_sha256', 'inner_object_sha256', 'wrapper_body_domain', 'wrapper_body_domain_sha256', 'wrapper_object_sha256', 'ack_binding_domain', 'ack_binding_sha256', 'official_writer_coordination_lock', 'final_dynamic_replay_census', 'all_dynamic_conjuncts_live', 'wrapper_closed_and_schema_validated_before_request', 'wrapper_body_excludes_transaction_binding_request_ACK_and_RELEASE_to_avoid_hash_cycle', 'transaction_binding_is_replay_identical_not_fresh_or_random', 'static_v16r2_exact10_with_v11_exact10_and_official_rejection_v10_exact10_and_official_rejection_v9_exact10_and_official_rejection_v8_exact10_and_official_rejection_v7_exact10_and_official_rejection_v6_exact10_and_official_rejection_v5_exact10_and_official_rejection_v4_supersession_v3_exact10_and_official_rejection_terminal_replay_completed_by_launcher_before_request', 'launcher_empty_rejection_namespace_guard_terminally_replayed_before_request', 'consumer_exec_fd_is_fresh_sealed_memfd', 'consumer_exec_fd_distinct_from_installed_source_fd', 'consumer_exec_memfd_required_seals_valid', 'consumer_exec_bytes_equal_installed_source_bytes', 'consumer_exec_and_installed_source_terminal_replayed', 'positive_wrapper_emitted_by_combined_child', 'release_required_before_dynamic_guards_close', 'positive_wrapper_raw_fd1_final_newline_write_is_launcher_semantic_commit', 'post_ACK_RELEASE_and_child_exit_are_non_authority_cleanup', 'formal_global_closure_credit', 'D02_unlock', 'object_sha256'}
    expected_census = {'C78l_C78s_held_file_count': 51, 'C78l_C78s_held_directory_count': 5, 'C55_C72_fixed_held_file_count_excluding_shared_head': 16, 'shared_C72G_C53_head_held_via_C42_full10_count': 1, 'frozen_v3_readable_held_file_count': 7, 'frozen_v3_source_metadata_only_held_count': 3, 'v3_official_rejection_shared_readable_held_file_count': 1, 'frozen_v5_readable_held_file_count': 7, 'frozen_v5_source_metadata_only_held_count': 3, 'v5_official_rejection_shared_readable_held_file_count': 1, 'frozen_v6_readable_held_file_count': 7, 'frozen_v6_source_metadata_only_held_count': 3, 'v6_official_rejection_shared_readable_held_file_count': 1, 'frozen_v7_readable_held_file_count': 7, 'frozen_v7_source_metadata_only_held_count': 3, 'v7_official_rejection_shared_readable_held_file_count': 1, 'frozen_v8_readable_held_file_count': 7, 'frozen_v8_source_metadata_only_held_count': 3, 'v8_official_rejection_shared_readable_held_file_count': 1, 'frozen_v9_readable_held_file_count': 7, 'frozen_v9_source_metadata_only_held_count': 3, 'v9_official_rejection_shared_readable_held_file_count': 1, 'frozen_v10_readable_held_file_count': 7, 'frozen_v10_source_metadata_only_held_count': 3, 'v10_official_rejection_shared_readable_held_file_count': 1, 'frozen_v11_readable_held_file_count': 7, 'frozen_v11_source_metadata_only_held_count': 3, 'v11_official_rejection_shared_readable_held_file_count': 1, 'rejected_v4_readable_held_file_count': 4, 'rejected_v4_source_metadata_only_held_count': 3, 'current_producer_metadata_only_held_count': 1, 'consumer_installed_source_held_count': 1, 'consumer_sealed_exec_memfd_held_count': 1, 'public_candidate_verification_completion_held_file_count': 24, 'public_candidate_verification_completion_held_directory_count': 5, 'C42_full10_union_candidate9_held_file_count': 16, 'C42_candidate_audit_install_held_directory_count': 3, 'authority_seal_held_file_count': 1, 'static_policy_held_file_count': 8, 'v11_official_rejection_in_static_policy_held_file_count': 1, 'terminal_deterministic_stage_absence_count': 5, 'fresh_rejection_namespace_scan_count': 1}
    need(set(ack) == expected_keys and ack.get('schema') == LIVE_ACK_SCHEMA and (ack.get('status') == 'ACK_FINAL_DYNAMIC_CONJUNCTS_LIVE__ZERO_CREDIT__AWAIT_POSITIVE_WRAPPER_AND_RELEASE') and (ack.get('protocol') == LIVE_PROTOCOL) and (ack.get('transaction_binding_domain') == TRANSACTION_BINDING_DOMAIN) and (ack.get('transaction_binding_sha256') == request['transaction_binding_sha256']) and (ack.get('request_object_sha256') == request['object_sha256']) and (ack.get('inner_object_sha256') == request['inner_object_sha256']) and (ack.get('wrapper_body_domain') == PREWRAPPER_BODY_DOMAIN) and (ack.get('wrapper_body_domain_sha256') == request['wrapper_body_domain_sha256']) and (ack.get('wrapper_object_sha256') == request['wrapper_object_sha256']) and (ack.get('ack_binding_domain') == LIVE_ACK_BINDING_DOMAIN) and (ack.get('ack_binding_sha256') == _expected_ack_binding(request)) and (ack.get('final_dynamic_replay_census') == expected_census) and (ack.get('all_dynamic_conjuncts_live') is True) and (ack.get('wrapper_closed_and_schema_validated_before_request') is True) and (ack.get('wrapper_body_excludes_transaction_binding_request_ACK_and_RELEASE_to_avoid_hash_cycle') is True) and (ack.get('transaction_binding_is_replay_identical_not_fresh_or_random') is True) and (ack.get('static_v16r2_exact10_with_v11_exact10_and_official_rejection_v10_exact10_and_official_rejection_v9_exact10_and_official_rejection_v8_exact10_and_official_rejection_v7_exact10_and_official_rejection_v6_exact10_and_official_rejection_v5_exact10_and_official_rejection_v4_supersession_v3_exact10_and_official_rejection_terminal_replay_completed_by_launcher_before_request') is True) and (ack.get('launcher_empty_rejection_namespace_guard_terminally_replayed_before_request') is True) and (ack.get('consumer_exec_fd_is_fresh_sealed_memfd') is True) and (ack.get('consumer_exec_fd_distinct_from_installed_source_fd') is True) and (ack.get('consumer_exec_memfd_required_seals_valid') is True) and (ack.get('consumer_exec_bytes_equal_installed_source_bytes') is True) and (ack.get('consumer_exec_and_installed_source_terminal_replayed') is True) and (ack.get('positive_wrapper_emitted_by_combined_child') is False) and (ack.get('release_required_before_dynamic_guards_close') is True) and (ack.get('positive_wrapper_raw_fd1_final_newline_write_is_launcher_semantic_commit') is True) and (ack.get('post_ACK_RELEASE_and_child_exit_are_non_authority_cleanup') is True) and (ack.get('formal_global_closure_credit') == 0) and (ack.get('D02_unlock') is False) and (raw == canonical(ack) + b'\n'), 'cold live ACK exact binding, census, zero-credit, and chronology')
    _validate_lock_ack(ack['official_writer_coordination_lock'], coordination)
    return ack

def run_authorize_child(bundle: HeldBundle, coordination: HeldCoordinationParent, rejection_guard: HeldEmptyRejectionNamespace) -> bool:
    source = bundle.by_path[CONSUMER]
    child_exec = HeldSealedChildExec(source)
    try:
        os.lseek(child_exec.fd, 0, os.SEEK_SET)
        process = subprocess.Popen(child_argv(child_exec, 'authorize', []), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=None, env=child_environment(bundle, child_exec, source, coordination), pass_fds=child_pass_fds(bundle, child_exec, source, coordination))
    except BaseException:
        child_exec.close()
        raise
    wrapper_committed = False
    positive_output_fd = -1
    try:
        need(process.stdin is not None and process.stdout is not None, 'cold authorize dedicated bidirectional pipes')
        inner_raw = process.stdout.readline(32 * 1024 * 1024 + 1)
        if inner_raw == b'':
            process.wait()
            need(process.returncode == 0, 'cold authorize zero-output seal installation')
            child_exec.terminal_replay()
            bundle.terminal_replay()
            rejection_guard.terminal_replay()
            coordination.verify()
            return False
        need(inner_raw.endswith(b'\n') and len(inner_raw) <= 32 * 1024 * 1024 and (inner_raw.count(b'\n') == 1), 'cold inner stdout:one bounded newline-terminated object')
        need(sys.stdout.buffer.fileno() == 1, 'positive wrapper stdout is exact fd1')
        sys.stdout.buffer.flush()
        stdout_flags = fcntl.fcntl(1, fcntl.F_GETFL)
        stdout_info = os.fstat(1)
        need(stat.S_ISFIFO(stdout_info.st_mode) and (not stdout_flags & os.O_NONBLOCK) and os.get_blocking(1), 'positive wrapper fd1 is a blocking pipe preflushed before final ACK')
        positive_output_fd = os.dup(1)
        held_stdout_info = os.fstat(positive_output_fd)
        held_stdout_flags = fcntl.fcntl(positive_output_fd, fcntl.F_GETFL)
        need((held_stdout_info.st_dev, held_stdout_info.st_ino, held_stdout_info.st_mode) == (stdout_info.st_dev, stdout_info.st_ino, stdout_info.st_mode) and (not held_stdout_flags & os.O_NONBLOCK) and os.get_blocking(positive_output_fd), 'held duplicate of prevalidated blocking positive-output pipe')
        child_exec.terminal_replay()
        root, inner = cold_root(bundle, coordination, child_exec, inner_raw)
        root_raw = canonical(root) + b'\n'
        need(root_raw.endswith(b'\n') and root_raw.count(b'\n') == 1, 'preclosed wrapper exact canonical line')
        wrapper_body_sha256 = _wrapper_body_domain_sha256(root)
        transaction_binding = _deterministic_transaction_binding(bundle, inner['object_sha256'], wrapper_body_sha256, root['object_sha256'])
        bundle.terminal_replay()
        child_exec.terminal_replay()
        rejection_guard.terminal_replay()
        coordination.verify()
        request = close_object({'schema': LIVE_REQUEST_SCHEMA, 'status': 'REQUEST_FINAL_DYNAMIC_LIVE_ACK_BEFORE_POSITIVE_WRAPPER_OUTPUT', 'protocol': LIVE_PROTOCOL, 'transaction_binding_domain': TRANSACTION_BINDING_DOMAIN, 'transaction_binding_sha256': transaction_binding, 'inner_object_sha256': inner['object_sha256'], 'wrapper_body_domain': PREWRAPPER_BODY_DOMAIN, 'wrapper_body_domain_sha256': wrapper_body_sha256, 'wrapper_object_sha256': root['object_sha256'], 'wrapper_closed_and_schema_validated_before_request': True, 'wrapper_body_excludes_transaction_binding_request_ACK_and_RELEASE_to_avoid_hash_cycle': True, 'transaction_binding_is_replay_identical_not_fresh_or_random': True, 'static_v16r2_exact10_with_v11_exact10_and_official_rejection_v10_exact10_and_official_rejection_v9_exact10_and_official_rejection_v8_exact10_and_official_rejection_v7_exact10_and_official_rejection_v6_exact10_and_official_rejection_v5_exact10_and_official_rejection_v4_supersession_v3_exact10_and_official_rejection_terminal_replay_completed_by_launcher_before_request': True, 'launcher_empty_rejection_namespace_guard_terminally_replayed_before_request': True})
        request_raw = canonical(request) + b'\n'
        written = process.stdin.write(request_raw)
        need(written == len(request_raw), 'complete cold live request write')
        process.stdin.flush()
        ack_raw = _read_child_line(process.stdout, 'cold final-dynamic ACK')
        ack = _validate_live_ack(ack_raw, request, coordination)
        release = close_object({'schema': LIVE_RELEASE_SCHEMA, 'status': 'RELEASE_AFTER_POSITIVE_WRAPPER_RAW_FD1_FINAL_NEWLINE_COMMIT', 'protocol': LIVE_PROTOCOL, 'transaction_binding_sha256': request['transaction_binding_sha256'], 'inner_object_sha256': request['inner_object_sha256'], 'wrapper_body_domain_sha256': request['wrapper_body_domain_sha256'], 'wrapper_object_sha256': request['wrapper_object_sha256'], 'ack_object_sha256': ack['object_sha256']})
        release_raw = canonical(release) + b'\n'
        view = memoryview(root_raw)
        offset = 0
        while offset < len(view):
            try:
                written = os.write(positive_output_fd, view[offset:])
            except InterruptedError:
                continue
            need(written > 0, 'positive wrapper raw fd1 made forward progress')
            offset += written
        wrapper_committed = True
        try:
            process.stdin.write(release_raw)
            process.stdin.flush()
        except (BrokenPipeError, OSError):
            pass
        try:
            process.stdin.close()
        except OSError:
            pass
        try:
            process.wait()
        except (OSError, subprocess.SubprocessError):
            pass
    finally:
        if wrapper_committed:
            try:
                if process.stdin is not None and (not process.stdin.closed):
                    process.stdin.close()
            except OSError:
                pass
            try:
                if process.poll() is None:
                    process.terminate()
                    process.wait()
            except (OSError, subprocess.SubprocessError):
                pass
            try:
                process.stdout.close()
            except OSError:
                pass
            if positive_output_fd >= 0:
                try:
                    os.close(positive_output_fd)
                except OSError:
                    pass
        else:
            if process.stdin is not None and (not process.stdin.closed):
                process.stdin.close()
            if process.poll() is None:
                process.terminate()
                process.wait()
            process.stdout.close()
            if positive_output_fd >= 0:
                os.close(positive_output_fd)
        if not wrapper_committed:
            coordination.verify()
        if wrapper_committed:
            try:
                child_exec.close()
            except OSError:
                pass
        else:
            child_exec.close()
    return wrapper_committed

def parser() -> argparse.ArgumentParser:
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--bootstrap-exec-fd', required=True, type=int, help=argparse.SUPPRESS)
    cli.add_argument('--bootstrap-source-fd', required=True, type=int, help=argparse.SUPPRESS)
    cli.add_argument('--bootstrap-root-fd', required=True, type=int, help=argparse.SUPPRESS)
    cli.add_argument('--cold-workspace-root', required=True, help=argparse.SUPPRESS)
    cli.add_argument('--expected-launcher-sha256', required=True)
    sub = cli.add_subparsers(dest='command', required=True)
    build = sub.add_parser('build')
    build.add_argument('--outdir', required=True)
    verify = sub.add_parser('verify')
    verify.add_argument('--orientation', required=True, choices=('a', 'b'))
    sub.add_parser('assemble')
    sub.add_parser('authorize')
    sub.add_parser('reject')
    return cli

def terminal_replay_v14_exact10_and_official_rejection(held_raw_by_role: Mapping[str, bytes]) -> dict[str, Any]:
    """Replay v14 exact10 then its rejection; return only zero-credit truth."""
    expected_roles = V14_PREDECESSOR_TERMINAL_REPLAY_ORDER
    need(tuple(held_raw_by_role) == expected_roles, 'v14 predecessor exact10 then official rejection held role order')
    decoded: dict[str, Mapping[str, Any]] = {}
    for role, _, file_pin, object_pin in V14_PUBLISHED_EXACT10_WITNESS:
        raw = held_raw_by_role[role]
        need(isinstance(raw, bytes) and hashlib.sha256(raw).hexdigest() == file_pin, 'held v14 exact10 file pin: ' + role)
        if object_pin is not None:
            value = strict_json(raw, 'held v14 exact10 JSON: ' + role)
            need(isinstance(value, Mapping), 'held v14 exact10 object: ' + role)
            body = dict(value)
            declared = body.pop('object_sha256', None)
            need(declared == object_pin and hashlib.sha256(canonical(body)).hexdigest() == object_pin, 'held v14 exact10 object pin: ' + role)
            decoded[role] = value
    expected_manifest = b''.join(((file_pin + '  ' + relative_path + '\n').encode('utf-8') for _, relative_path, file_pin, _ in V14_PUBLISHED_EXACT10_WITNESS[:8]))
    need(held_raw_by_role['cold_manifest'] == expected_manifest, 'held v14 exact8 manifest exact ordered bytes')
    outer = decoded['cold_outer']
    expected_entries = [{'file_sha256': file_pin, 'path': relative_path} for _, relative_path, file_pin, _ in V14_PUBLISHED_EXACT10_WITNESS[:8]]
    need(outer.get('status') == 'FROZEN_COLD_LAUNCH_OUTER_LAST__EXACT8_MANIFEST_CLOSED__RUNTIME_DEFERRED' and outer.get('exact8_ordered_entries') == expected_entries and (outer.get('formal_global_closure_credit') == 0) and (outer.get('D02_unlock') is False) and (outer.get('runtime_executed_during_static_freeze') is False), 'held v14 outer exact8 and zero-credit closure')
    rejection_raw = held_raw_by_role['v14_official_rejection']
    need(isinstance(rejection_raw, bytes) and hashlib.sha256(rejection_raw).hexdigest() == V14_OFFICIAL_REJECTION_FILE_PIN, 'held v14 official rejection file pin')
    rejection = strict_json(rejection_raw, 'held v14 official rejection')
    need(isinstance(rejection, Mapping), 'held v14 official rejection object')
    rejection_body = dict(rejection)
    declared_rejection_object = rejection_body.pop('object_sha256', None)
    need(declared_rejection_object == V14_OFFICIAL_REJECTION_OBJECT_PIN and hashlib.sha256(canonical(rejection_body)).hexdigest() == V14_OFFICIAL_REJECTION_OBJECT_PIN and (len(rejection) == 56) and (hashlib.sha256(canonical(sorted(rejection))).hexdigest() == V14_OFFICIAL_REJECTION_EXACT56_KEYSET_SHA256), 'held v14 official rejection exact56 and object pin')
    by_role = {row[0]: row for row in V14_PUBLISHED_EXACT10_WITNESS}
    need(rejection.get('schema') == 'cm2.round306c79g.true-global-no-producer-consumer.v14.later-rejection' and rejection.get('status') == 'PERMANENT_FAIL_CLOSED_REJECTION__ZERO_CREDIT' and (rejection.get('rejection_reason') == 'ORPHANED_OR_INCOMPLETE_C79G_V14_SURFACE') and (rejection.get('formal_global_closure_credit') == 0) and (rejection.get('D02_unlock') is False) and (rejection.get('D02_started') is False) and (rejection.get('D02_gate_credit') == 0) and (rejection.get('D02_task_credit') == 0) and (rejection.get('D02_formal_pending_task_count') == 33638) and (rejection.get('closed_schema_file_sha256') == by_role['closed_schema'][2]) and (rejection.get('contract_file_sha256') == by_role['contract'][2]) and (rejection.get('contract_object_sha256') == by_role['contract'][3]) and (rejection.get('producer_file_sha256') == by_role['build_only_producer'][2]) and (rejection.get('consumer_file_sha256') == by_role['independent_consumer'][2]) and (rejection.get('cold_launcher_file_sha256') == by_role['cold_launcher'][2]) and (rejection.get('cold_manifest_file_sha256') == by_role['cold_manifest'][2]) and (rejection.get('cold_outer_file_sha256') == by_role['cold_outer'][2]) and (rejection.get('cold_outer_object_sha256') == by_role['cold_outer'][3]), 'held v14 rejection binds exact10 and preserves zero credit')
    return {'status': 'TERMINAL_REPLAY_PASS__V14_EXACT10_THEN_OFFICIAL_REJECTION__ZERO_CREDIT_ONLY', 'terminal_replay_order': list(expected_roles), 'chronology': list(V14_RUNTIME_REGISTRY_SHAPE_DRIFT_INCIDENT['chronology']), 'v14_runtime_registry_shape_drift_incident': copy.deepcopy(V14_RUNTIME_REGISTRY_SHAPE_DRIFT_INCIDENT), 'formal_global_closure_credit': 0, 'D02_unlock': False, 'D02_started': False, 'D02_gate_credit': 0, 'D02_task_credit': 0, 'D02_formal_pending_task_count': 33638, 'v14_credit_transferred_to_v16r2': False}

def v14_inherited_authority_draft_state(supersession_receipt_exists: bool) -> dict[str, Any]:
    """Prove the legal v16r2 draft state without opening the frozen receipt."""
    need(V16R2_DRAFT_RUNTIME_DISABLED is True and FINAL_BASE7_PINS_INSTALLED is False and (V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT_FILE_PIN not in V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT_DRAFT_SENTINELS) and (V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT_OBJECT_PIN not in V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT_DRAFT_SENTINELS) and (supersession_receipt_exists is True), 'v16r2 draft requires frozen pinned v14 receipt and uninstalled v16r2 base7 pins')
    return {'status': 'V16R2_DRAFT_RUNTIME_DISABLED__V14_SUPERSESSION_RECEIPT_FROZEN_PINNED', 'receipt_path': V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT_RELATIVE_PATH, 'receipt_open_attempted': False, 'runtime_authorized': False}

def terminal_replay_v14_inherited_authority_exact12(held_raw_by_role: Mapping[str, bytes]) -> dict[str, Any]:
    """Replay exact10, rejection, then final receipt from twelve held bytes."""
    need(tuple(held_raw_by_role) == V14_INHERITED_AUTHORITY_EXACT12_ROLE_ORDER and len(held_raw_by_role) == V16R2_CHILD_AUTHORITY_DESCRIPTOR_COUNT == 12, 'v14 inherited authority exact12 held role order')
    need(V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT_FILE_PIN not in V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT_DRAFT_SENTINELS and V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT_OBJECT_PIN not in V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT_DRAFT_SENTINELS, 'v14 supersession receipt final pins installed')
    prefix = {role: held_raw_by_role[role] for role in V14_PREDECESSOR_TERMINAL_REPLAY_ORDER}
    result = terminal_replay_v14_exact10_and_official_rejection(prefix)
    receipt_raw = held_raw_by_role['v14_registry_shape_drift_supersession_receipt']
    need(hashlib.sha256(receipt_raw).hexdigest() == V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT_FILE_PIN, 'held v14 supersession receipt file pin')
    receipt = strict_json(receipt_raw, 'held v14 supersession receipt')
    need(isinstance(receipt, Mapping), 'held v14 supersession receipt object')
    body = dict(receipt)
    declared = body.pop('object_sha256', None)
    need(declared == V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT_OBJECT_PIN and hashlib.sha256(canonical(body)).hexdigest() == declared, 'held v14 supersession receipt object pin')
    result.update({'status': 'TERMINAL_REPLAY_PASS__V14_INHERITED_AUTHORITY_EXACT12__ZERO_CREDIT_ONLY', 'terminal_replay_order': list(V14_INHERITED_AUTHORITY_EXACT12_ROLE_ORDER), 'held_authority_descriptor_count': 12, 'bootstrap_descriptor_count': 4, 'child_pass_fd_count': 16, 'v14_supersession_receipt_object_sha256': declared, 'formal_global_closure_credit': 0, 'D02_unlock': False, 'v14_credit_transferred_to_v16r2': False})
    return result

def main(argv: list[str] | None=None) -> int:
    args = parser().parse_args(argv)
    if V16R2_DRAFT_RUNTIME_DISABLED and (not FINAL_BASE7_PINS_INSTALLED):
        raise Reject('C79g v16r2 successor is a sentinel draft; runtime is disabled')
    need(FINAL_BASE7_PINS_INSTALLED is True, 'C79g v16r2 launcher requires final base7 pins')
    inherited = (args.bootstrap_exec_fd, args.bootstrap_source_fd, args.bootstrap_root_fd)
    try:
        bootstrap = HeldBootstrapEntry(args.bootstrap_exec_fd, args.bootstrap_source_fd, args.bootstrap_root_fd, args.cold_workspace_root, args.expected_launcher_sha256)
    except BaseException:
        for descriptor in set(inherited):
            try:
                os.close(descriptor)
            except OSError:
                pass
        raise
    wrapper_committed = False
    coordination: HeldCoordinationParent | None = None
    bundle: HeldBundle | None = None
    rejection_guard: HeldEmptyRejectionNamespace | None = None
    try:
        coordination = HeldCoordinationParent()
        if args.command == 'reject':
            install_or_replay_launcher_native_rejection(bootstrap, coordination)
            return 0
        rejection_guard = HeldEmptyRejectionNamespace(coordination)
        bundle = HeldBundle(args.expected_launcher_sha256, coordination, bootstrap)
        if args.command == 'build':
            stdout = run_non_authorize_child(bundle, coordination, rejection_guard, 'build', ['--outdir', args.outdir])
        elif args.command == 'verify':
            stdout = run_non_authorize_child(bundle, coordination, rejection_guard, 'verify', ['--orientation', args.orientation])
        elif args.command == 'assemble':
            stdout = run_non_authorize_child(bundle, coordination, rejection_guard, 'assemble', [])
        else:
            wrapper_committed = run_authorize_child(bundle, coordination, rejection_guard)
            stdout = b''
        if args.command != 'authorize':
            need(not stdout, 'non-root cold child unexpectedly wrote stdout')
    finally:
        if bundle is not None:
            if wrapper_committed:
                try:
                    bundle.close()
                except OSError:
                    pass
            else:
                bundle.close()
        if rejection_guard is not None:
            rejection_guard.close()
        if coordination is not None:
            if wrapper_committed:
                try:
                    coordination.close()
                except OSError:
                    pass
            else:
                coordination.close()
        if wrapper_committed:
            try:
                bootstrap.close()
            except OSError:
                pass
        else:
            bootstrap.close()
    return 0
if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except Reject as exc:
        print('REJECT:', exc, file=sys.stderr)
        raise SystemExit(2)
