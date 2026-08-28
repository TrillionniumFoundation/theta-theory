#!/usr/bin/env python3
"""C65s18 64-shard aggregate independent cold verifier, protocol v4.

This file supersedes the rejected development verifier without importing,
executing, or manifesting that source.  Its numerical kernel is the frozen
C41 independent auditor and its *complete* local ``cm2_*`` import closure,
loaded only from bytes captured in the same bounded snapshot as every live
authority and aggregate input.  No ``pyc`` or pre-existing local module is a
trust source.

The public workflow is deliberately multi-process and result-last:

Formal phases are accepted only when this file is the script opened and
executed through ``/proc/self/fd/N`` by the independently supplied, pinned
``FORMAL_ENTRY_BOOTSTRAP`` literal.  Direct path execution is rejected before
any formal read or write.  Direct ``--self-test`` remains a non-authoritative,
read-only synthetic check.

1. ``--launch-dual`` starts two fresh, held-script ``-S -P -s -B`` workers with
   hash seeds 1/2 under the sealed python-flint 0.9.0 runtime.
   The launcher, not a worker, captures process provenance and publishes each
   projection followed by its completion receipt.
2. ``--install`` fully validates both projections and receipts, then publishes
   verification followed by an installer completion receipt.
3. ``--publish-self-test`` publishes the hostile self-test and its completion
   receipt.
4. ``--release`` validates every prerequisite and frozen input, publishes a
   replay, one exact global manifest, and finally an outer completion receipt.

All artifacts are zero-credit and are installed with no-replace semantics.
Any orphaned partial target set requires an explicit later rejection and new
supersession version; this program never deletes, overwrites, or resumes one.
"""

from __future__ import annotations

import argparse
import ast
import builtins
from collections import Counter, defaultdict
import concurrent.futures
import contextlib
import copy
from dataclasses import dataclass
from fractions import Fraction
import hashlib
import importlib.abc
import importlib.util
import io
import json
import os
from pathlib import Path
from pathlib import PurePosixPath
import re
import selectors
import stat
import subprocess
import sys
import tempfile
import time
from types import ModuleType
from typing import Any, Callable, Iterable, Iterator, Mapping
import zlib


sys.dont_write_bytecode = True
EXECUTED_SELF = Path(__file__)
SELF = Path("/home/qian-qi/.openclaw/workspaces/telegram-bot-8449317572/deliverables/"
            "cm2_round306c65s18_64shard_aggregate_independent_cold_verifier_v4.py")
OUT = SELF.parent
ROOT = OUT.parent

SCHEMA = "cm2.round306c65s18.64shard-aggregate-independent-cold-verifier.v4"
SHARD_SCHEMA = "cm2.round306c65s18.depth18-64shard.v3"
AGG_SCHEMA = "cm2.round306c65s18.depth18-64shard.aggregate.v1"
AGG_STATUS = "PASS_COMPLETE_64_SHARD_DEPTH18_REPLACEMENT_AGGREGATE__ZERO_CREDIT"
ASSIGNMENT_DOMAIN = "cm2.round306c65s18.depth18-64shard.v2.assignment"
SHARDS = tuple(range(64))
PAIRS = (31, 188, 200, 270, 321, 410, 471, 474, 631, 711, 787, 853)
DISPOSITIONS = ("STRICT_TERMINAL", "COLLISION3_READY", "COLLISION2_HANDOFF")
ADDITIONAL_DEPTH = 6
HEX64 = re.compile(r"[0-9a-f]{64}\Z")

BASE = "cm2_round306c65s18_depth18_64shard"
RECEIPT_RE = re.compile(rf"{BASE}_shard_(\d{{2}})_receipt_v3\.json\Z")
LEDGER_RE = re.compile(rf"{BASE}_shard_(\d{{2}})_leaf_ledger_v3\.jsonl\.gz\Z")
SHARD_CANDIDATE_PREFIX = BASE + "_shard_"

EXECUTOR = OUT / "cm2_round306c65s18_depth18_64shard_executor_v3.py"
CONTROLLER = OUT / "cm2_round306c65s18_bulk_execution_controller_v1.py"
CHECKER = OUT / "cm2_round306c65s18_bulk_shard_readonly_checker_v1.py"
PRODUCER = OUT / "cm2_round306c65s18_64shard_zero_credit_aggregate_producer_v1.py"
CONTRACT = OUT / "cm2_round306c65s18_independent_contract_v2.json"
ASSIGNMENT = OUT / f"{BASE}_assignment_result_v2.json"
INVENTORY = OUT / f"{BASE}_assignment_inventory_v2.jsonl.gz"
AUTHORIZATION = OUT / "cm2_round306c65s18_assignment_authorization_seal_v2.json"
C61_RESULT = OUT / "cm2_round306c61s12_depth12_16shard_aggregate_result_v4.json"
C61_LEAVES = OUT / "cm2_round306c61s12_depth12_16shard_aggregate_leaf_ledger_v4.jsonl.gz"
C61_PARENTS = OUT / "cm2_round306c61s12_depth12_16shard_aggregate_parent_summary_v4.jsonl.gz"
C58_RESULT = OUT / "cm2_round306c58s2_singleton_collision2_handoff_depth6_refinement_result_v1.json"
C58_LEAVES = OUT / "cm2_round306c58s2_singleton_collision2_handoff_depth6_refinement_leaf_ledger_v1.jsonl.gz"
C40_DIR = ROOT / ".cm2-runtime/candidates/c40-h1-endpoint-c2-arrangement-20260810T234000Z-c2f144e29bc1172f"
C40_RESULT = C40_DIR / "result.json"
C40_ROUTED = C40_DIR / "routed_leaf_cells.jsonl.gz"
C41_ROOT_MODULE = "cm2_round306c41_d02_lower_strata_depth3_closure_independent_auditor_v1"
C41_SOURCE = OUT / (C41_ROOT_MODULE + ".py")

AGG_RESULT = OUT / f"{BASE}_aggregate_result_v1.json"
AGG_LEAVES = OUT / f"{BASE}_aggregate_leaf_ledger_v1.jsonl.gz"
AGG_SOURCES = OUT / f"{BASE}_aggregate_source_summary_v1.jsonl.gz"
AGG_PARENTS = OUT / f"{BASE}_aggregate_parent_summary_v1.jsonl.gz"

CANONICAL = OUT / "CM2_LATEST_STATUS.md"
CANONICAL_COMPANION = OUT / "CM2_LATEST_STATUS.sha256"
GLOBAL_HEAD = ROOT / ".cm2-runtime/cm2-global-authority-heads/predecessor-10fb050d30c92b0f2bdcf85a30d28ff670d8efc0b48104b7f04a63c391967b41.seal"
GLOBAL_CLAIM = ROOT / ".cm2-runtime/cm2-global-successor-claims/predecessor-10fb050d30c92b0f2bdcf85a30d28ff670d8efc0b48104b7f04a63c391967b41.claim"
C53_TOKEN = ROOT / ".cm2-runtime/c53-current-pair-successor-token"
C53_AUDIT_TOKEN = ROOT / ".cm2-runtime/c53-current-pair-successor-audit-token"

V1_REJECTION = OUT / "cm2_round306c65s18_64shard_aggregate_independent_cold_self_test_v1_REJECTED_PRE_CLOSE_SOURCE_DRIFT.md"
V2_REJECTION = OUT / "cm2_round306c65s18_64shard_aggregate_independent_cold_verifier_v2_REJECTED_PROTOCOL_AND_RUNTIME_CAPTURE_GAPS.md"
V3_REJECTION = OUT / "cm2_round306c65s18_64shard_aggregate_independent_cold_verifier_v3_REJECTED_GLOBAL_HEAD_CLOSURE_SCHEMA.md"
PRODUCER_CONTRACT_REJECTION = OUT / "cm2_round306c65s18_64shard_aggregate_producer_prepublication_contract_encoding_rejection_v1.md"
PRODUCER_PARENT_REJECTION = OUT / "cm2_round306c65s18_64shard_aggregate_producer_prepublication_parent_carry_rejection_v1.md"

SEED1_PROJECTION = OUT / "cm2_round306c65s18_64shard_aggregate_independent_cold_seed1_projection_v4.json"
SEED1_RECEIPT = OUT / "cm2_round306c65s18_64shard_aggregate_independent_cold_seed1_completion_receipt_v4.json"
SEED2_PROJECTION = OUT / "cm2_round306c65s18_64shard_aggregate_independent_cold_seed2_projection_v4.json"
SEED2_RECEIPT = OUT / "cm2_round306c65s18_64shard_aggregate_independent_cold_seed2_completion_receipt_v4.json"
VERIFY_OUT = OUT / "cm2_round306c65s18_64shard_aggregate_independent_cold_verification_v4.json"
VERIFY_RECEIPT = OUT / "cm2_round306c65s18_64shard_aggregate_independent_cold_verification_completion_receipt_v4.json"
SELFTEST_OUT = OUT / "cm2_round306c65s18_64shard_aggregate_independent_cold_self_test_v4.json"
SELFTEST_RECEIPT = OUT / "cm2_round306c65s18_64shard_aggregate_independent_cold_self_test_completion_receipt_v4.json"
REPLAY_OUT = OUT / "cm2_round306c65s18_64shard_aggregate_independent_cold_postpublication_replay_v4.json"
MANIFEST_OUT = OUT / "cm2_round306c65s18_64shard_aggregate_independent_cold_manifest_v4.sha256"
OUTER_RECEIPT = OUT / "cm2_round306c65s18_64shard_aggregate_independent_cold_outer_receipt_v4.json"

FORMAL_TARGETS = (SEED1_PROJECTION, SEED1_RECEIPT, SEED2_PROJECTION, SEED2_RECEIPT,
                  VERIFY_OUT, VERIFY_RECEIPT, SELFTEST_OUT, SELFTEST_RECEIPT,
                  REPLAY_OUT, MANIFEST_OUT, OUTER_RECEIPT)

SEALED_VENV = ROOT / ".cm2-runtime/python-flint-0.9.0"
SEALED_PYTHON_LINK = SEALED_VENV / "bin/python"
SEALED_PYTHON = Path("/usr/bin/python3.12")
PYVENV_CFG = SEALED_VENV / "pyvenv.cfg"
RUNTIME_REQUIREMENTS = OUT / "cm2_round306c30a_python_flint_requirements.lock"
RUNTIME_LOCK = OUT / "cm2_round306c30a_python_flint_runtime_lock.json"
RUNTIME_ATTESTATION = OUT / "cm2_round306c30b_sealed/cm2_round306c30b_python_flint_runtime_attestation.json"
FLINT_INIT = SEALED_VENV / "lib/python3.12/site-packages/flint/__init__.py"
FLINT_PYFLINT = SEALED_VENV / "lib/python3.12/site-packages/flint/pyflint.abi3.so"
FLINT_LIBS = (
    SEALED_VENV / "lib/python3.12/site-packages/python_flint.libs/libflint-6839011d.so.24.0.0",
    SEALED_VENV / "lib/python3.12/site-packages/python_flint.libs/libgmp-e0c82b6b.so.10.5.0",
    SEALED_VENV / "lib/python3.12/site-packages/python_flint.libs/libmpfr-be332c05.so.6.2.2",
)
HASH_SENTINEL = "CM2_C65_COLD_V4_HASH_SEED_SENTINEL"
HASH_FINGERPRINTS = {"1": -608947459856227912, "2": 3416907535422985676}
EXPECTED_SELFTEST_KEYS = frozenset({
    '63_candidate_rejected', 'AST_no_C65_program_import', 'BOM_rejected',
    'FIFO_rejected', 'Infinity_rejected', 'JSON_bool_int_type_sensitive',
    'NaN_rejected', 'TOCTOU_replacement_rejected', 'aggregate_capture_bound_rejected',
    'aggregate_pins_concrete', 'authority_cycle_rejected',
    'authority_diamond_revisit_allowed', 'authority_exact_closure_pin_concrete',
    'baseline_valid', 'bool_for_int_count_rejected', 'bool_for_int_credit_rejected',
    'bool_for_int_depth_rejected', 'bool_for_int_route_rejected',
    'candidate_exact64_accepts', 'captured_source_loader_valid_source',
    'coherent_C61_full_base_C2_rejected', 'coherent_C61_full_base_leaves_rejected',
    'coherent_C61_full_base_terminal_rejected', 'coherent_D02_gate_credit_rejected',
    'coherent_bounded_each_rejected', 'coherent_bounded_total_rejected',
    'coherent_complete_C2_rejected', 'coherent_complete_C3_rejected',
    'coherent_complete_leaves_rejected', 'coherent_complete_terminal_rejected',
    'coherent_controller_absent_rejected', 'coherent_distinct_worker_startticks_rejected',
    'coherent_executable_identity_stable_rejected', 'coherent_external_workers_rejected',
    'coherent_formal_credit_rejected', 'coherent_malformed_candidates_rejected_rejected',
    'coherent_no_pyc_or_preloaded_local_modules_rejected',
    'coherent_numeric_source_closure_count_rejected',
    'coherent_numeric_source_closure_object_rejected',
    'coherent_one_global_manifest_snapshot_rejected',
    'coherent_ordered_members_unique_rejected',
    'coherent_orphan_requires_supersession_rejected', 'coherent_outer_receipt_last_rejected',
    'coherent_per_shard_trie_routes_exact_rejected',
    'coherent_post_long_run_full_recapture_rejected',
    'coherent_post_manifest_full_recapture_rejected',
    'coherent_pretty_contract_exact_file_object_rejected',
    'coherent_projection_schema_exact_rejected', 'coherent_projection_types_exact_rejected',
    'coherent_receipt_full_fields_exact_rejected', 'coherent_receipt_ids_rejected',
    'coherent_release_full_validator_rejected', 'coherent_result_last_receipts_rejected',
    'coherent_runtime_write_rejected', 'coherent_single_frozen_snapshot_rejected',
    'coherent_v1_rejection_manifested_rejected', 'coherent_v1_source_not_manifested_rejected',
    'coherent_whole_parent_credit_rejected', 'complete_no_replace_rejected',
    'compute_has_no_direct_publication', 'dual_workers_parallel_GO_design',
    'duplicate_key_rejected', 'float_rejected', 'formal_eleven_target_phase_grammar_design',
    'formal_outputs_untouched_by_selftest', 'fresh_output_set_accepts',
    'gzip_concatenated_rejected', 'gzip_count_rejected', 'gzip_expand_bound_rejected',
    'gzip_sequence_rejected', 'gzip_trailing_junk_rejected', 'gzip_truncated_rejected',
    'hardlink_rejected', 'install_full_non_numeric_revalidation_design',
    'malformed_candidate_rejected', 'manifest_basename_alias_is_unique_design',
    'missing_newline_rejected', 'missing_rejected', 'orphan_output_set_rejected',
    'post_outer_joint_recapture_design', 'pretty_JSON_rejected_at_compact_boundary',
    'pretty_JSON_syntax_accepts_only_when_explicit',
    'pretty_when_compact_required_rejected', 'pyc_bytes_rejected',
    'release_manifest_single_snapshot_design', 'safe_runtime_exact_tree_pin_concrete',
    'selftest_no_clock_order_dependency', 'symlink_rejected', 'trailing_rejected',
    'generic_object_parser_rejects_global_head_schema',
    'global_head_schema_specific_closure_valid',
    'uncaptured_cm2_import_rejected', 'v1_rejection_pin_concrete',
    'v1_verifier_absent_from_release_members', 'v2_rejection_pin_concrete',
    'v3_rejection_pin_concrete', 'v3_verifier_absent_from_release_members',
    'valid_single_member_gzip',
})
FORMAL_ENTRY_BOOTSTRAP = r'''import fcntl,hashlib,os,re,stat,sys
SELF="/home/qian-qi/.openclaw/workspaces/telegram-bot-8449317572/deliverables/cm2_round306c65s18_64shard_aggregate_independent_cold_verifier_v4.py"
PYTHON="/usr/bin/python3.12"
VENV_PYTHON="/home/qian-qi/.openclaw/workspaces/telegram-bot-8449317572/.cm2-runtime/python-flint-0.9.0/bin/python"
PYTHON_SHA256="1643dacd9feaedc58f3cc581e4d22577dfe25c09b10282936186ccf0f2e61118"
PHASES={"--launch-dual","--install","--self-test","--preflight-smoke","--publish-self-test","--release"}
BASE_ENV={"HOME":"/nonexistent","LC_ALL":"C.UTF-8","TZ":"UTC","PYTHONHASHSEED":"1","PYTHONDONTWRITEBYTECODE":"1","PYTHONNOUSERSITE":"1"}
def need(ok,label):
 if not ok: raise SystemExit("C65 formal entry rejected:"+label)
def fp(s): return (s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns)
def open_abs(path):
 need(path.startswith("/") and "//" not in path and "/./" not in path and "/../" not in path,"absolute path")
 parts=path[1:].split("/"); need(parts and all(parts) and all(p not in {".",".."} for p in parts),"path parts")
 d=os.open("/",os.O_RDONLY|os.O_DIRECTORY|os.O_CLOEXEC)
 try:
  for part in parts[:-1]:
   n=os.open(part,os.O_RDONLY|os.O_DIRECTORY|os.O_CLOEXEC|os.O_NOFOLLOW,dir_fd=d); os.close(d); d=n
  return os.open(parts[-1],os.O_RDONLY|os.O_CLOEXEC|os.O_NOFOLLOW,dir_fd=d)
 finally:
  os.close(d)
def read_stable(fd,label):
 before=os.fstat(fd); need(stat.S_ISREG(before.st_mode) and before.st_nlink==1,label+" type/link")
 os.lseek(fd,0,os.SEEK_SET); blocks=[]
 while True:
  block=os.read(fd,1<<20)
  if not block: break
  blocks.append(block)
 raw=b"".join(blocks); need(len(raw)==before.st_size and fp(os.fstat(fd))==fp(before),label+" stable")
 return before,raw
need(os.environ==BASE_ENV,"initial env")
need(len(sys.argv)==3 and re.fullmatch(r"[0-9a-f]{64}",sys.argv[1]) is not None and sys.argv[2] in PHASES,"argv")
cmd=open("/proc/self/cmdline","rb",buffering=0).read().split(b"\0")[:-1]
need(len(cmd)==9 and cmd[:6]==[b"/usr/bin/python3.12",b"-S",b"-P",b"-s",b"-B",b"-c"] and cmd[7:]==[sys.argv[1].encode(),sys.argv[2].encode()],"exact command")
entry_sha=hashlib.sha256(cmd[6]).hexdigest()
self_fd=open_abs(SELF); self_state,self_raw=read_stable(self_fd,"SELF")
need(hashlib.sha256(self_raw).hexdigest()==sys.argv[1],"SELF expected hash")
self_fd2=open_abs(SELF)
try:
 self_state2,self_raw2=read_stable(self_fd2,"SELF reopen"); need(fp(self_state2)==fp(self_state) and self_raw2==self_raw,"SELF reopen equality")
finally: os.close(self_fd2)
python_fd=open_abs(PYTHON); python_state,python_raw=read_stable(python_fd,"python")
need(hashlib.sha256(python_raw).hexdigest()==PYTHON_SHA256 and fp(os.stat("/proc/self/exe"))==fp(python_state),"python hash/current exe")
python_fd2=open_abs(PYTHON)
try:
 python_state2,python_raw2=read_stable(python_fd2,"python reopen"); need(fp(python_state2)==fp(python_state) and python_raw2==python_raw,"python reopen equality")
finally: os.close(python_fd2)
need(stat.S_ISLNK(os.lstat(VENV_PYTHON).st_mode) and os.readlink(VENV_PYTHON)=="python3","venv link")
fcntl.fcntl(self_fd,fcntl.F_SETFD,fcntl.fcntl(self_fd,fcntl.F_GETFD)&~fcntl.FD_CLOEXEC)
fcntl.fcntl(python_fd,fcntl.F_SETFD,fcntl.fcntl(python_fd,fcntl.F_GETFD)&~fcntl.FD_CLOEXEC)
env=dict(BASE_ENV); env.update({"C65_COLD_BOOTSTRAPPED":"1","C65_COLD_ENTRY_SHA256":entry_sha,"C65_COLD_LAUNCHER_PID":str(os.getpid()),"C65_COLD_PYTHON_FD":str(python_fd),"C65_COLD_SELF_FD":str(self_fd),"C65_COLD_SELF_PATH":SELF,"C65_COLD_VERIFIER_SHA256":sys.argv[1]})
os.chdir("/")
os.execve(python_fd,[VENV_PYTHON,"-S","-P","-s","-B",f"/proc/self/fd/{self_fd}",sys.argv[2]],env)'''

PIN = {
    "formal_entry_bootstrap_sha256":
        "c2cd7e28358dbb094dacc414bd974f34e72f0ebcfa448d1c2aafad753169fc8d",
    "executor_file": "170df261ed9451fc3ecc1fca5e686c6f6d8eeb3d643126da09f30c634cda22ef",
    "controller_file": "1ee734f4bfca42ef17284e1de7225a5f5b0a88cff5167f0a9d33d7195caf0845",
    "checker_file": "f7e7db5590a52902e3e478b364a92c33e81508f90b52b4fe79f8a2b4cbce644d",
    "contract_file": "e320ac48b1cf3675a3c152d0cb9e6084ba750433722fef716e4a8ab534fab287",
    "contract_object": "5d8a39432c2b02e807c5624ea26f56a12b58f66601ab391b52fee89d0ca604a4",
    "assignment_file": "0306fd12de7d73988a45bac84acf70e4615e8e3aaef7c3c42a66fc39dbef4baa",
    "assignment_object": "c7671985713c8cfd8a496931f1b2686fa545448ce0a434c89e943b178000407f",
    "inventory_file": "e2c4714f1f1a8aa470a393d25ff03aaa3228f08979c30c90fd5f297469d6ad30",
    "authorization_file": "99788b913ee8b900c97e14b6b52d90b0ad83ef2c3fddda6d9f82ab0aacc39ca0",
    "authorization_object": "d1b508a54553b8944b50e926e895b35a589fe6aca3a03440e416571b339ca228",
    "C61_result_file": "06b4146185cb6ef0c8d908d523369008481f7df4e6a05ad5956c001267b07f5e",
    "C61_result_object": "05bcb4301ac74aefd6744db2e633c2479c423fab881b33609bf7234a5537e584",
    "C61_leaf_file": "2656bc4d1b99d37da3733338d85c8d6301621563a400d5db40380078c001b1c2",
    "C61_parent_file": "2206c817f49312c519a720e14bc2e152cde5362ed884cbe83d32349a7ff5bab2",
    "C58_result_file": "ed4eb1e5ea64c61e4b85a710c1429a2f0b489048320badd4d9a8214bc38c05bc",
    "C58_result_object": "038503bd21505dacde4ce6dc59a320fa70a97cc0dccce33be210c60bbd7d0a30",
    "C58_leaf_file": "15a5b1c5c15f8528591bd80be040317590dadec70b4476d01eb3763ae64965df",
    "C40_result_file": "f721b08a4addb7c0369b27ea3af8546c9fad293b1a7808d015bbf783b3aa22d6",
    "C40_object": "397eda962e4bd20429d7cab1ffc53d82cccfdf59bdce8cd03b271a8ded0536ba",
    "C40_routed_file": "175293702adf1b76600321c1db326a1a6744dbc8caea439ddaeff9779d1f9b5a",
    "producer_file": "4667ee6471c235980c4368c0999c3170af2d49dbc6eb0a3b0c682644beca87f7",
    "aggregate_result_file": "1ca46fb81cc104b727b31d3bb0adbb439ab8dae9123b8cbe05d3c60de0e75457",
    "aggregate_result_object": "79185dbca48f0d228977a006583eb545525cff2d9418160fb190c1f9c5b6c393",
    "aggregate_leaves_file": "4ff1c36a0a6331510da3afb988738f128a3cada04ddd297ac58584579115437d",
    "aggregate_sources_file": "de8fa908cbe46e379ff05564c5d8ed0ea97de2875eca05792ad3abf63287f432",
    "aggregate_parents_file": "91adb1e9e5e7e7dfdc1cbf674d5713d218851a4b5f15602ced2664972280bc4b",
    "C41_root_file": "537f3dea94c3743235df8984ba4922d37f82999ff3d8abbac59e5171ef38b74c",
    "numeric_source_closure_object": "5dff9981ce4bb473a49e18ec70068a55693b54f77a8f6af00e5f29ed169ee9da",
    "numeric_source_closure_count": 51,
    "canonical_file": "922fc5d01918b217556bc3f392c44efcc7c9c6345c881371e6cd34950eb99b57",
    "canonical_companion_file": "57d0c75a2dc774d312fc72a11c66e745cf9b7232531e469490bac492b0a91d6b",
    "global_head_file": "f62483c87df4b6f4a8a2ad8dcf56febbfce9977200ce94a0ad6ce38e736aeeb3",
    "global_head_object": "cb90ab914c3b6518384669f42d05df33c21a717596190131c6a0f5683934cbfb",
    "global_claim_file": "3801e452f218e330bc16faed5986146202a7d7026e46924bf7bc00167b05f77b",
    "C53_token_file": "dcad8792bb4bede7f97f9996d10b43497b6286704dbc8f1b8a4170a9e2416846",
    "C53_audit_token_file": "c3a9a3248b2ec3cb0887b62f4edade7664f73f1746593be1b69897404ae42eba",
    "authority_snapshot_object": "c9a8b97be4bed2008fa132f49e0d4ac0b384e973707ecdf48b27028b7d7e93cf",
    "effective_checkpoint_object": "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab",
    "v1_rejection_file": "b5773b5731128aa69d0371bae6d3c55027737b62359072163491007b7cd394de",
    "producer_contract_rejection_file":
        "a3e3246775e1622d46212df9679cd693790460c960d9358aa1f478a8b408b06f",
    "producer_parent_rejection_file":
        "3ca2a94a72370fd71111163554fbc1f98ead476373644ccec3a2b7cb1b724d21",
    "rejected_v1_selftest_file": "babd294faeaea9db0e5433527ad3a4688f3b22ae8ab053fbd0400feb10c3ce2b",
    "rejected_v1_selftest_object": "90f1b65d2b0361b3116919235d081430603cfff53e7aa63d646c7a8dc7422dca",
    "v2_rejection_file": "ba3ee3a56e908bcf5e42deeb60a2f155067bff7250a194098513b3b2551af97c",
    "rejected_v2_verifier_file": "497da169e255f1382965bc867cdf15525f1cfb60934c8ee746ccb2238b4a8f52",
    "v3_rejection_file": "901f78668b20d4c82a038b7be93bb044d831b5c8b97fcbaa41a5749d19405496",
    "rejected_v3_verifier_file": "f799b40c9d5c6a12df74b2b8c7c87d0b6911c9d7c289eaa3a538a81a76a60a22",
    "authority_directory_count": 9,
    "authority_file_count": 80,
    "authority_parsed_json_count": 28,
    "authority_edge_count": 37,
    "authority_total_bytes": 621_814_861,
    "authority_directory_object": "f78bfa504d6fc4ff25c6bfc6c5da83266abfee81beff4797169f6a00170240ec",
    "authority_file_object": "6966b271b14ce36ea517312ffed0e4eb2178e5b714aeb8e3ed6e48ef197ca66d",
    "authority_file_path_object": "b7577bb3d745511ff6e7dec84a2409f92f51da70c50259439e955c1c701c14a9",
    "authority_directory_members_object": "384e42d7f0ef0684b03d31df5497ce77a4e1309f4cb47a09d8d9070ba5758945",
    "authority_edge_object": "48b94f5f8a42685f985b3db824147631d6ec26853534de07b846c33cd4ce93a5",
    "authority_topology_object": "bd8de156f1929394a562fb32a07d01a26df63d475a9b1cd610a0e2c504acf102",
    "authority_closure_object": "cfed31f01b246d3c30fa97060047c5f510c3055aeff71e651560654abd065747",
    "runtime_requirements_file": "cd171f53dd8a187b2ef4bd7ad0cc2adbe2082395646c0c57407f4e3514c11f5c",
    "runtime_lock_file": "ffe714b67a0aa05d8094033a0d9cc8e10ccafa03157951adf3d64055c98cdc79",
    "runtime_attestation_file": "6b48cd0ca3fd53f9fdd457cc3c1106055e12db4d4ad999fcfd1fc89ad36b95df",
    "pyvenv_cfg_file": "7a941243ffcb93edeea4c49bc4543a1ff8150b3300f846cda2f13717b6469550",
    "python_file": "1643dacd9feaedc58f3cc581e4d22577dfe25c09b10282936186ccf0f2e61118",
    "flint_init_file": "2e5f8f1768d14eccd7961353c635195bd557f297edff8b8de09e2d211f03ec2d",
    "flint_pyflint_file": "1f7ef1f52024937f542772ff9190e2f74449228cd69a6746b6608fbbd449d138",
    "libflint_file": "871a4132fd1e9f3638391b2208e07088f8e3e72a10e41d45f58b150a60c2a1a9",
    "libgmp_file": "33d24e675b10f8b1ab93a8ad3fa2ed5012e1b0d89dcdb97273877c6c6b9450d8",
    "libmpfr_file": "c4dfcfc7c5c7ab71d427e15f2f9fae4ace88592a81d4596a918dcc02eadfc6e3",
    "safe_runtime_file_count": 98,
    "full_runtime_record_object": "862c9185021eccf86b89b24f0245c7db67f28c72be00a36a21d7e5745662f83a",
    "full_runtime_total_bytes": 26_758_280,
    "safe_runtime_total_bytes": 25_600_805,
    "safe_runtime_record_object": "a1443d028310c26178e41c1ae8d50d90ab16aafcc3fbee98d0936a66fc03161c",
    "safe_runtime_path_object": "ff9a098da76fbb5e80bc2dc006e6530f508450f8e153666ed880722cbace1626",
    "safe_runtime_directory_members_object": "f58e05046f863d6c7ec94dc4955c8aa670f35b9f77e52b621f682469c2d744f9",
    "selftest_key_object": "3527fcce70e855b2d74b6ec9acba3884ad490b9e6708edc87c118ae7e94c5bca",
}

EXPECTED_AUTHORITY = {
    "C50d_global_claim": PIN["global_claim_file"],
    "C50d_global_head": PIN["global_head_file"],
    "C53_audit_token": PIN["C53_audit_token_file"],
    "C53_successor_token": PIN["C53_token_file"],
    "CM2_LATEST_STATUS.md": PIN["canonical_file"],
    "CM2_LATEST_STATUS.sha256": PIN["canonical_companion_file"],
}

C61_LEDGER_TERMINAL = 23_997
C61_EARLIER_TERMINAL_CARRY = 3_411
C61_FULL_BASE_LEAVES = 48_287
C61_FULL_BASE_TERMINAL = 27_408
C61_FULL_BASE_C2 = 20_879
EXPECTED_REPLACEMENT_LEAVES = 358_919
EXPECTED_REPLACEMENT_TERMINAL = 191_664
EXPECTED_REPLACEMENT_C3 = 0
EXPECTED_REPLACEMENT_C2 = 167_255
EXPECTED_COMPLETE_LEAVES = 386_327
EXPECTED_COMPLETE_TERMINAL = 219_072

MAX_EACH = 1 << 30
MAX_TOTAL = 2 << 30
MAX_EXPANDED = 4 << 30


class Reject(RuntimeError):
    """Fail-closed protocol, filesystem, or mathematical rejection."""


class AwaitingInputs(Reject):
    pass


def need(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise Reject(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False,
                      allow_nan=False).encode("utf-8")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def close(value: dict[str, Any]) -> dict[str, Any]:
    need("object_sha256" not in value, "object already closed")
    result = copy.deepcopy(value)
    result["object_sha256"] = digest(result)
    return result


def exact_int(value: Any, expected: int, label: str) -> None:
    need(type(value) is int and value == expected, label + ": exact int")


def exact_nonnegative_int(value: Any, label: str) -> None:
    need(type(value) is int and value >= 0, label + ": nonnegative int")


def strict_keys(value: Any, keys: set[str], label: str) -> dict[str, Any]:
    need(type(value) is dict and set(value) == keys, label + ": exact keys")
    return value


def strict_json(raw: bytes, label: str, canonical_required: bool = True) -> Any:
    need(bool(raw) and not raw.startswith(b"\xef\xbb\xbf"), label + ": nonempty/no BOM")

    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in items:
            need(key not in result, label + ": duplicate key:" + key)
            result[key] = value
        return result

    try:
        value = json.loads(
            raw.decode("utf-8", "strict"), object_pairs_hook=pairs,
            parse_float=lambda token: (_ for _ in ()).throw(
                Reject(label + ": float forbidden:" + token)),
            parse_constant=lambda token: (_ for _ in ()).throw(
                Reject(label + ": nonfinite forbidden:" + token)),
        )
    except Reject:
        raise
    except Exception as error:
        raise Reject(label + ": JSON:" + str(error)) from error
    if canonical_required:
        need(raw == canonical(value) + b"\n", label + ": compact canonical/newline")
    return value


def closed_json_field(raw: bytes, label: str, claim_field: str,
                      file_pin: str | None = None,
                      object_pin: str | None = None,
                      canonical_required: bool = True) -> dict[str, Any]:
    if file_pin is not None:
        need(hashlib.sha256(raw).hexdigest() == file_pin, label + ": exact file pin")
    value = strict_json(raw, label, canonical_required)
    need(type(value) is dict and HEX64.fullmatch(str(value.get(claim_field))) is not None,
         label + ": closed object claim")
    body = copy.deepcopy(value)
    claim = body.pop(claim_field)
    need(digest(body) == claim and (object_pin is None or claim == object_pin),
         label + ": object closure/pin")
    return value


def closed_json(raw: bytes, label: str, file_pin: str | None = None,
                object_pin: str | None = None, canonical_required: bool = True) -> dict[str, Any]:
    return closed_json_field(raw, label, "object_sha256", file_pin, object_pin,
                             canonical_required)


def zero_credit(value: dict[str, Any], label: str) -> None:
    for key in ("formal_credit", "whole_parent_credit", "D02_gate_credit"):
        exact_int(value.get(key), 0, label + ":" + key)


def fingerprint(value: os.stat_result) -> tuple[int, ...]:
    return (value.st_dev, value.st_ino, value.st_mode, value.st_nlink, value.st_size,
            value.st_mtime_ns, value.st_ctime_ns)


@dataclass(frozen=True)
class Captured:
    logical_name: str
    path: Path
    raw: bytes
    identity: tuple[int, ...]
    parent_identity: tuple[int, ...]

    def record(self) -> dict[str, Any]:
        return {
            "logical_name": self.logical_name,
            "relative_path": logical_relative(self.path),
            "sha256": hashlib.sha256(self.raw).hexdigest(),
            "size": len(self.raw),
            "identity": list(self.identity),
            "parent_identity": list(self.parent_identity),
        }


def logical_alias(path: Path) -> str:
    relative = Path(logical_relative(path))
    alias = "__".join(relative.parts)
    need("/" not in alias and alias not in {"", ".", ".."}, "safe logical alias")
    return alias


def logical_relative(path: Path) -> str:
    path = path.absolute()
    if path.is_relative_to(ROOT):
        return str(path.relative_to(ROOT))
    need(path == SEALED_PYTHON, "only sealed machine interpreter may be external")
    return "machine-runtime/usr/bin/python3.12"


def anchored_dirfd(path: Path) -> int:
    """Open an absolute directory one component at a time, never following links."""
    path = path.absolute()
    need(path.is_absolute(), "anchored directory absolute")
    fd = os.open("/", os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC)
    try:
        for part in path.parts[1:]:
            next_fd = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC |
                              getattr(os, "O_NOFOLLOW", 0), dir_fd=fd)
            os.close(fd)
            fd = next_fd
        return fd
    except BaseException:
        os.close(fd)
        raise


def directory_identity(path: Path) -> tuple[int, ...]:
    fd = anchored_dirfd(path)
    try:
        state = os.fstat(fd)
        need(stat.S_ISDIR(state.st_mode), "directory identity is directory")
        return fingerprint(state)
    finally:
        os.close(fd)


def capture_bounded(paths: Iterable[Path], *, maximum_each: int = MAX_EACH,
                    maximum_total: int = MAX_TOTAL,
                    hook: Callable[[], None] | None = None) -> dict[Path, Captured]:
    ordered = tuple(Path(path).absolute() for path in paths)
    need(len(ordered) == len(set(ordered)), "capture duplicate path")
    need(all(path == path.resolve(strict=False) for path in ordered), "capture canonical paths")
    dirfds: dict[Path, int] = {}
    fds: dict[Path, int] = {}
    states: dict[Path, os.stat_result] = {}
    total = 0
    try:
        for path in ordered:
            parent = path.parent
            if parent not in dirfds:
                dirfds[parent] = anchored_dirfd(parent)
            fd = os.open(path.name, os.O_RDONLY | os.O_CLOEXEC |
                         getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_NONBLOCK", 0),
                         dir_fd=dirfds[parent])
            state = os.fstat(fd)
            current = os.stat(path.name, dir_fd=dirfds[parent], follow_symlinks=False)
            need(stat.S_ISREG(state.st_mode) and state.st_nlink == 1 and
                 0 <= state.st_size <= maximum_each and fingerprint(state) == fingerprint(current),
                 "capture regular single-link bounded identity:" + str(path))
            total += state.st_size
            need(total <= maximum_total, "capture aggregate byte bound")
            fds[path], states[path] = fd, state
        payloads: dict[Path, Captured] = {}
        read_total = 0
        for path in ordered:
            chunks: list[bytes] = []
            size = 0
            while True:
                block = os.read(fds[path], min(4 << 20, maximum_each - size + 1))
                if not block:
                    break
                size += len(block)
                read_total += len(block)
                need(size <= maximum_each and read_total <= maximum_total,
                     "capture streaming byte bound")
                chunks.append(block)
            raw = b"".join(chunks)
            need(len(raw) == states[path].st_size, "capture exact size:" + str(path))
            payloads[path] = Captured(logical_alias(path), path, raw, fingerprint(states[path]),
                                      fingerprint(os.fstat(dirfds[path.parent])))
        if hook is not None:
            hook()
        for path in ordered:
            current = os.stat(path.name, dir_fd=dirfds[path.parent], follow_symlinks=False)
            need(fingerprint(states[path]) == fingerprint(os.fstat(fds[path])) ==
                 fingerprint(current) and payloads[path].parent_identity ==
                 fingerprint(os.fstat(dirfds[path.parent])),
                 "capture TOCTOU file+parent:" + str(path))
        return payloads
    finally:
        for descriptor in fds.values():
            os.close(descriptor)
        for descriptor in dirfds.values():
            os.close(descriptor)


def compare_recapture(before: Mapping[Path, Captured], after: Mapping[Path, Captured],
                      label: str) -> None:
    need(tuple(before) == tuple(after), label + ": exact ordered path set")
    for path in before:
        need(before[path].identity == after[path].identity and
             before[path].parent_identity == after[path].parent_identity and
             before[path].raw == after[path].raw,
             label + ": bytes+file+parent identity:" + str(path))


def snapshot_vector(snapshot: Mapping[Path, Captured]) -> list[dict[str, Any]]:
    vector = [snapshot[path].record() for path in snapshot]
    aliases = [row["logical_name"] for row in vector]
    need(len(aliases) == len(set(aliases)), "snapshot logical basename uniqueness")
    return vector


def snapshot_object(snapshot: Mapping[Path, Captured]) -> str:
    return digest({"ordered_frozen_inputs": snapshot_vector(snapshot)})


def receipt_path(shard: int) -> Path:
    return OUT / f"{BASE}_shard_{shard:02d}_receipt_v3.json"


def shard_ledger_path(shard: int) -> Path:
    return OUT / f"{BASE}_shard_{shard:02d}_leaf_ledger_v3.jsonl.gz"


def candidate_name_gate(directory: Path, phase: str) -> tuple[str, ...]:
    """Reject malformed candidates, rather than filtering them out."""
    need(phase in {"receipt", "ledger"}, "candidate gate phase")
    directory_fd = anchored_dirfd(directory)
    try:
        names = tuple(sorted(os.listdir(directory_fd)))
    except OSError as error:
        raise Reject("candidate gate anchored listdir:" + str(error)) from error
    finally:
        os.close(directory_fd)
    regex = RECEIPT_RE if phase == "receipt" else LEDGER_RE
    shard_candidates = tuple(name for name in names if name.startswith(SHARD_CANDIDATE_PREFIX))
    malformed = tuple(name for name in shard_candidates
                      if RECEIPT_RE.fullmatch(name) is None and LEDGER_RE.fullmatch(name) is None)
    need(not malformed, phase + ": malformed candidate names:" + repr(malformed))
    matched = tuple(name for name in shard_candidates if regex.fullmatch(name) is not None)
    ids = tuple(int(regex.fullmatch(name).group(1)) for name in matched)  # type: ignore[union-attr]
    need(ids == SHARDS, phase + ": exact ids 00..63")
    expected = tuple((receipt_path(i) if phase == "receipt" else shard_ledger_path(i)).name
                     for i in SHARDS)
    need(matched == expected, phase + ": exact ordered canonical names")
    return matched


def shard_name_barrier() -> tuple[tuple[str, ...], tuple[str, ...]]:
    receipts = candidate_name_gate(OUT, "receipt")
    # Receipt barrier is intentionally complete before any ledger path is derived.
    ledgers = candidate_name_gate(OUT, "ledger")
    return receipts, ledgers


def proc_startticks(pid: int) -> int:
    raw = (Path("/proc") / str(pid) / "stat").read_text(encoding="ascii")
    close_paren = raw.rfind(")")
    need(close_paren > 0, "proc stat comm framing")
    fields = raw[close_paren + 2:].split()
    value = int(fields[19])
    need(value > 0, "proc positive startticks")
    return value


def executable_identity(pid: int) -> dict[str, Any]:
    proc = Path("/proc") / str(pid)
    target = Path(os.readlink(proc / "exe"))
    fd = os.open(proc / "exe", os.O_RDONLY | os.O_CLOEXEC)
    try:
        state = os.fstat(fd)
        chunks: list[bytes] = []
        while block := os.read(fd, 4 << 20):
            chunks.append(block)
        raw = b"".join(chunks)
        need(stat.S_ISREG(state.st_mode) and len(raw) == state.st_size and
             fingerprint(os.fstat(fd)) == fingerprint(state),
             "process executable held-fd regular/stable")
    finally:
        os.close(fd)
    current = capture_bounded((target,), maximum_each=32 << 20,
                              maximum_total=32 << 20)[target]
    need(current.identity == fingerprint(state) and current.raw == raw,
         "process executable proc-fd/path exact")
    return {
        "pid": pid, "startticks": proc_startticks(pid),
        "executable_path": str(target), "executable_dev": state.st_dev,
        "executable_inode": state.st_ino, "executable_size": state.st_size,
        "executable_mtime_ns": state.st_mtime_ns,
        "executable_sha256": hashlib.sha256(raw).hexdigest(),
    }


def controller_processes() -> tuple[dict[str, Any], ...]:
    needle = CONTROLLER.name.encode("utf-8")
    try:
        entries = tuple(Path("/proc").iterdir())
    except OSError as error:
        raise Reject("/proc controller enumeration unavailable:" + str(error)) from error
    hits: list[dict[str, Any]] = []
    for entry in entries:
        if not entry.name.isdigit():
            continue
        try:
            raw = (entry / "cmdline").read_bytes()
        except (FileNotFoundError, ProcessLookupError):
            continue
        except OSError as error:
            if error.errno in {2, 3}:
                continue
            raise Reject("/proc controller read failure:" + str(error)) from error
        if needle in raw:
            hits.append(executable_identity(int(entry.name)))
    return tuple(hits)


def runtime_barrier() -> dict[str, Any]:
    hits = controller_processes()
    need(not hits, "controller must be absent")
    return {
        "controller_processes": [],
        "controller_source_identity": list(fingerprint(CONTROLLER.stat())),
        "executor_source_identity": list(fingerprint(EXECUTOR.stat())),
        "checker_source_identity": list(fingerprint(CHECKER.stat())),
    }


def runtime_link_record() -> dict[str, Any]:
    parent = directory_identity(SEALED_PYTHON_LINK.parent)
    state = os.lstat(SEALED_PYTHON_LINK)
    need(stat.S_ISLNK(state.st_mode) and state.st_nlink == 1 and
         os.readlink(SEALED_PYTHON_LINK) == "python3" and
         SEALED_PYTHON_LINK.resolve(strict=True) == SEALED_PYTHON,
         "sealed python symlink chain exact")
    return {"path": str(SEALED_PYTHON_LINK.relative_to(ROOT)), "target": "python3",
            "identity": list(fingerprint(state)), "parent_identity": list(parent)}


def validate_formal_process_runtime() -> dict[str, Any]:
    need(os.environ.get("C65_COLD_BOOTSTRAPPED") == "1",
         "formal phase must execute through external held-script entry")
    validate_worker_runtime(os.environ["PYTHONHASHSEED"], formal=True)
    held_self_capture()
    held_python_capture()
    need(int(os.environ["C65_COLD_LAUNCHER_PID"]) == os.getpid(),
         "formal entry same-pid exec binding")
    process = executable_identity(os.getpid())
    need(sys.prefix == "/usr" and sys.base_prefix == "/usr" and
         Path(sys.executable).absolute() == SEALED_PYTHON_LINK and
         process["executable_path"] == str(SEALED_PYTHON) and
         process["executable_sha256"] == PIN["python_file"],
         "formal process exact sealed python-flint venv/runtime")
    return process


def stable_runtime(before: dict[str, Any], after: dict[str, Any], label: str) -> None:
    need(before == after, label + ": controller/executable/program identity stable")


def output_set_state(paths: Iterable[Path], label: str) -> None:
    ordered = tuple(paths)
    states = tuple(path.exists() or path.is_symlink() for path in ordered)
    if any(states):
        if not all(states):
            raise Reject(label + ": orphaned partial target set; terminal rejection and a new "
                         "supersession version are mandatory")
        raise Reject(label + ": completed targets already exist; no-replace")


def formal_phase_gate(phase: str) -> None:
    expected_prefix = {"launch": 0, "install": 4, "self-test": 6, "release": 8}
    need(phase in expected_prefix, "formal phase name")
    present: list[bool] = []
    parent_fd = anchored_dirfd(OUT)
    try:
        for path in FORMAL_TARGETS:
            try:
                state = os.stat(path.name, dir_fd=parent_fd, follow_symlinks=False)
            except FileNotFoundError:
                present.append(False)
                continue
            need(stat.S_ISREG(state.st_mode) and state.st_nlink == 1,
                 "formal target regular single-link:" + path.name)
            present.append(True)
    finally:
        os.close(parent_fd)
    prefix = expected_prefix[phase]
    expected = [ordinal < prefix for ordinal in range(len(FORMAL_TARGETS))]
    need(present == expected,
         phase + ": exact eleven-target phase grammar; mixed/future/orphan requires supersession")


def publish_bytes(path: Path, raw: bytes) -> None:
    parent = path.parent.absolute()
    directory = anchored_dirfd(parent)
    try:
        descriptor = os.open(path.name, os.O_RDWR | os.O_CREAT | os.O_EXCL | os.O_CLOEXEC |
                             getattr(os, "O_NOFOLLOW", 0), 0o644, dir_fd=directory)
        try:
            view = memoryview(raw)
            while view:
                written = os.write(descriptor, view)
                need(written > 0, "publication short write")
                view = view[written:]
            os.fsync(descriptor)
            before = os.fstat(descriptor)
            current = os.stat(path.name, dir_fd=directory, follow_symlinks=False)
            need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1 and
                 fingerprint(before) == fingerprint(current), "publication fd/path identity")
            os.lseek(descriptor, 0, os.SEEK_SET)
            chunks: list[bytes] = []
            while block := os.read(descriptor, 1 << 20):
                chunks.append(block)
            need(b"".join(chunks) == raw and fingerprint(os.fstat(descriptor)) ==
                 fingerprint(before), "publication terminal-byte replay")
            os.fsync(directory)
        finally:
            os.close(descriptor)
    finally:
        os.close(directory)


def publish_json(path: Path, value: dict[str, Any]) -> None:
    publish_bytes(path, canonical(value) + b"\n")


DESCRIPTOR_KEYS = {
    "filename", "order", "row_count", "row_hash_line_sequence_sha256", "sha256", "size",
}
RECEIPT_KEYS = {
    "schema", "status", "runner_file_sha256", "shard_id", "shard_count",
    "additional_binary_depth", "assignment_contract_file_sha256",
    "assignment_contract_object_sha256", "assignment_authorization_file_sha256",
    "assignment_authorization_object_sha256", "assignment_result_file_sha256",
    "assignment_result_object_sha256", "assignment_inventory_sha256",
    "assignment_preimage_schema", "assignment_formula", "assigned_input_count",
    "ordered_assignment_preimage_sha256_line_sequence_sha256", "input_assignment_rows",
    "route_evaluation_count", "output_disposition_census", "raw_classification_census",
    "output_ledger", "authority_snapshot_before", "authority_snapshot_after",
    "authority_snapshot_object_sha256", "shard_complete",
    "partial_statistics_are_formal_credit", "formal_credit", "whole_parent_credit",
    "D02_gate_credit", "runtime_canonical_pointer_or_seal_writes", "object_sha256",
}
RECEIPT_SOURCE_KEYS = {
    "assignment_preimage_sha256", "source_C61_aggregate_leaf_row_sha256",
    "source_output_row_count", "source_output_row_hash_line_sequence_sha256",
    "source_Kraft_conservation", "source_prefix_free",
}
SHARD_ROW_KEYS = {
    "schema", "shard_id", "assignment_preimage_sha256",
    "source_C61_aggregate_leaf_row_sha256", "source_C61_shard_row_sha256",
    "source_C58_leaf_row_sha256", "source_handoff_ordinal", "C58_source_path",
    "source_path", "path", "additional_depth_from_C61",
    "nominal_additional_depth_from_C58", "pair_index", "parent_volume_fraction",
    "exact_representative_box", "exact_reflected_box", "route_classification",
    "route_witness", "route_method", "disposition", "continuation",
    "local_terminal_credit", "formal_credit", "whole_parent_credit", "D02_gate_credit",
    "row_sha256",
}
CONTINUATION_KEYS = {
    "next_collision_index", "prior_C61_aggregate_leaf_row_sha256",
    "prior_C61_shard_row_sha256", "prior_C61_continuation_object_sha256",
    "prior_C58_leaf_row_sha256", "prior_C58_handoff_object_sha256",
    "collision1_history_row_sha256", "collision1_original_owner",
    "collision1_event_order", "exact_representative_box", "exact_reflected_box",
    "route_classification", "route_witness", "route_method", "continuation_credit",
    "continuation_object_sha256",
}
ASSIGNMENT_ROW_KEYS = {
    "schema", "shard_id", "assignment_preimage_sha256",
    "source_C61_aggregate_leaf_row_sha256", "source_C61_continuation_object_sha256",
    "source_C61_disposition", "source_C61_next_collision_index",
    "source_C61_source_shard_row_sha256", "source_C58_leaf_row_sha256",
    "source_handoff_ordinal", "source_path", "path", "pair_index",
    "parent_volume_fraction", "assignment_credit", "formal_credit",
    "whole_parent_credit", "D02_gate_credit", "row_sha256",
}
C61_ROW_KEYS = {
    "schema", "shard_id", "assignment_preimage_sha256", "source_shard_row_sha256",
    "source_C58_leaf_row_sha256", "source_handoff_ordinal", "source_path", "path",
    "additional_depth_from_C58", "pair_index", "parent_volume_fraction",
    "exact_representative_box", "exact_reflected_box", "route_classification",
    "route_witness", "route_method", "disposition", "continuation",
    "local_terminal_credit", "formal_credit", "whole_parent_credit", "D02_gate_credit",
    "row_sha256",
}
C61_PARENT_KEYS = {
    "schema", "pair_index", "combined_leaf_count", "strict_terminal_leaf_count",
    "collision3_ready_leaf_count", "collision2_handoff_leaf_count", "path_prefix_free",
    "parent_Kraft_conservation", "whole_pair_terminal", "whole_pair_credit",
    "D02_gate_credit", "row_sha256",
}
AGG_LEAF_KEYS = (SHARD_ROW_KEYS - {"schema", "shard_id", "row_sha256"}) | {
    "schema", "source_C65_shard_id", "source_C65_shard_row_sha256", "row_sha256",
}
AGG_SOURCE_KEYS = {
    "schema", "source_inventory_ordinal", "source_assignment_row_sha256",
    "assignment_preimage_sha256", "source_C61_aggregate_leaf_row_sha256",
    "source_C61_shard_row_sha256", "source_handoff_ordinal", "source_path", "pair_index",
    "source_C65_shard_id", "output_leaf_count", "strict_terminal_leaf_count",
    "collision3_ready_leaf_count", "collision2_handoff_leaf_count", "route_evaluation_count",
    "source_shard_output_row_hash_line_sequence_sha256",
    "aggregate_output_row_hash_line_sequence_sha256", "path_prefix_free",
    "source_Kraft_conservation", "whole_source_terminal",
    "whole_source_terminal_or_C3_ready", "formal_credit", "whole_parent_credit",
    "D02_gate_credit", "row_sha256",
}
AGG_PARENT_KEYS = {
    "schema", "pair_index", "C61_full_base_parent_row_sha256",
    "C61_full_base_combined_leaf_count", "C61_full_base_strict_terminal_leaf_count",
    "C61_full_base_collision3_ready_leaf_count", "C61_full_base_collision2_sources_replaced",
    "C61_aggregate_ledger_strict_terminal_leaf_count",
    "C57_C58_earlier_terminal_carry_leaf_count", "C65_replacement_leaf_count",
    "combined_leaf_count", "strict_terminal_leaf_count", "collision3_ready_leaf_count",
    "collision2_handoff_leaf_count", "path_prefix_free", "parent_Kraft_conservation",
    "parent_prefix_Kraft_preserved_by_base_certificate_and_exact_source_partitions",
    "whole_pair_terminal", "whole_pair_terminal_or_C3_ready", "formal_credit",
    "whole_parent_credit", "D02_gate_credit", "row_sha256",
}
AGG_RESULT_KEYS = {
    "schema", "status", "producer_file_sha256", "producer_independence", "frozen_inputs",
    "authority_snapshot", "shard_receipts", "coverage", "ledgers", "invariants",
    "candidate_is_authority", "formal_credit", "whole_parent_credit", "D02_gate_credit",
    "runtime_canonical_pointer_or_seal_writes", "object_sha256",
}

ASSIGNMENT_PREIMAGE_SCHEMA = {
    "BOM": False, "allow_nan": False, "encoding": "UTF-8", "ensure_ascii": False,
    "json_separators": [",", ":"], "keys_lexicographically_sorted": True,
    "schema": {
        "assignment_domain": "exact literal " + ASSIGNMENT_DOMAIN,
        "path": "exact 21-bit source path",
        "source_C61_aggregate_leaf_row_sha256": "64 lowercase hexadecimal characters",
    },
    "trailing_newline": False,
}


def descriptor(value: Any, filename: str, order: str, label: str) -> dict[str, Any]:
    strict_keys(value, DESCRIPTOR_KEYS, label)
    need(value["filename"] == filename and value["order"] == order and
         type(value["row_count"]) is int and value["row_count"] >= 0 and
         type(value["size"]) is int and value["size"] > 0 and
         HEX64.fullmatch(str(value["sha256"])) is not None and
         HEX64.fullmatch(str(value["row_hash_line_sequence_sha256"])) is not None,
         label + ": exact descriptor")
    return value


def iter_gzip(raw: bytes, desc: dict[str, Any], label: str,
              expanded_limit: int = MAX_EXPANDED) -> Iterator[dict[str, Any]]:
    need(len(raw) == desc["size"] and hashlib.sha256(raw).hexdigest() == desc["sha256"],
         label + ": descriptor bytes")
    need(len(raw) >= 18 and raw[:3] == b"\x1f\x8b\x08" and raw[3] == 0 and
         raw[4:8] == b"\0\0\0\0", label + ": deterministic gzip header")
    decoder = zlib.decompressobj(16 + zlib.MAX_WBITS)
    buffer = b""
    count = 0
    expanded = 0
    sequence = hashlib.sha256()
    for offset in range(0, len(raw), 1 << 20):
        try:
            block = decoder.decompress(raw[offset:offset + (1 << 20)])
        except zlib.error as error:
            raise Reject(label + ": gzip:" + str(error)) from error
        expanded += len(block)
        need(expanded <= expanded_limit, label + ": bounded inflate")
        buffer += block
        while b"\n" in buffer:
            line, buffer = buffer.split(b"\n", 1)
            row = strict_json(line + b"\n", label + ":row", True)
            need(type(row) is dict and HEX64.fullmatch(str(row.get("row_sha256"))) is not None,
                 label + ": row hash claim")
            body = copy.deepcopy(row)
            claim = body.pop("row_sha256")
            need(digest(body) == claim, label + ": row closure")
            sequence.update((claim + "\n").encode("ascii"))
            count += 1
            yield row
    try:
        buffer += decoder.flush()
    except zlib.error as error:
        raise Reject(label + ": gzip flush:" + str(error)) from error
    need(decoder.eof and not decoder.unused_data and not decoder.unconsumed_tail and
         buffer == b"", label + ": one member/no trailing/newline framing")
    need(count == desc["row_count"] and
         sequence.hexdigest() == desc["row_hash_line_sequence_sha256"],
         label + ": row count/sequence")


def fraction(value: Any) -> Fraction:
    need(type(value) is str and value and len(value) <= 128, "fraction textual bound")
    try:
        return Fraction(value)
    except (ValueError, ZeroDivisionError) as error:
        raise Reject("invalid fraction:" + value) from error


def prefix_free(paths: list[str]) -> bool:
    ordered = sorted(paths)
    return len(ordered) == len(set(ordered)) and all(
        not right.startswith(left) for left, right in zip(ordered, ordered[1:])
    )


def trie_route_count(source: str, leaves: list[str]) -> int:
    need(bool(leaves) and prefix_free(leaves), "trie nonempty prefix-free")
    nodes = {source}
    for leaf in leaves:
        need(leaf.startswith(source) and set(leaf) <= {"0", "1"}, "trie descendant path")
        nodes.update(leaf[:end] for end in range(len(source) + 1, len(leaf) + 1))
    return len(nodes)


def assignment_preimage(source_sha: str, path: str) -> bytes:
    need(HEX64.fullmatch(source_sha) is not None and type(path) is str and len(path) == 21 and
         set(path) <= {"0", "1"}, "assignment source/path")
    return canonical({"assignment_domain": ASSIGNMENT_DOMAIN, "path": path,
                      "source_C61_aggregate_leaf_row_sha256": source_sha})


def source_dependencies(source: bytes, filename: str) -> tuple[str, ...]:
    tree = ast.parse(source.decode("utf-8", "strict"), filename=filename)
    # Captured numerical modules must derive every workspace path from their
    # virtual __file__ or the frozen cwd; a literal live-workspace path would
    # reopen an unauthenticated trust root during the long replay.
    need(not any(isinstance(node, ast.Constant) and isinstance(node.value, str) and
                 str(ROOT) in node.value for node in ast.walk(tree)),
         "numeric source contains literal live workspace path:" + filename)
    dependencies: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            dependencies.update(alias.name for alias in node.names if alias.name.startswith("cm2_"))
        elif isinstance(node, ast.ImportFrom) and node.module and node.module.startswith("cm2_"):
            dependencies.add(node.module)
    return tuple(sorted(dependencies))


def discover_source_closure() -> tuple[dict[str, Path], dict[str, Captured]]:
    pending = [C41_ROOT_MODULE]
    paths: dict[str, Path] = {}
    captured: dict[str, Captured] = {}
    total = 0
    while pending:
        module = pending.pop()
        if module in paths:
            continue
        need(re.fullmatch(r"cm2_[A-Za-z0-9_]+", module) is not None,
             "numeric local module name")
        path = (OUT / (module + ".py")).absolute()
        one = capture_bounded((path,), maximum_each=16 << 20, maximum_total=16 << 20)[path]
        total += len(one.raw)
        need(total <= 256 << 20, "numeric source closure total bound")
        paths[module], captured[module] = path, one
        pending.extend(dep for dep in source_dependencies(one.raw, path.name) if dep not in paths)
    hashes = {module: hashlib.sha256(captured[module].raw).hexdigest()
              for module in sorted(captured)}
    need(len(hashes) == PIN["numeric_source_closure_count"] and
         digest(hashes) == PIN["numeric_source_closure_object"] and
         hashes.get(C41_ROOT_MODULE) == PIN["C41_root_file"],
         "complete authenticated numeric source closure")
    return paths, captured


def safe_workspace_path(text: str, label: str) -> Path:
    need(type(text) is str and text and "\0" not in text, label + ": path text")
    candidate = (ROOT / text).absolute()
    need(candidate == candidate.resolve(strict=False) and candidate.is_relative_to(ROOT),
         label + ": workspace-contained canonical path")
    return candidate


def authority_paths_from_result(value: Any) -> tuple[Path, ...]:
    result: set[Path] = set()

    def walk(node: Any, key: str = "") -> None:
        if type(node) is dict:
            for child_key, child in node.items():
                walk(child, child_key)
        elif type(node) is list:
            for child in node:
                walk(child, key)
        elif type(node) is str and (key == "path" or key.endswith("_path")):
            # Only explicit filesystem path fields are traversed.  Schema prose
            # such as "exact 21-bit source path" is never interpreted.
            if node.startswith((".cm2-runtime/", "deliverables/")):
                result.add(safe_workspace_path(node, "authority path"))

    walk(value)
    return tuple(sorted(result))


def authority_directory_inventory(directories: Iterable[Path]) -> dict[str, list[str]]:
    vector: dict[str, list[str]] = {}
    for path in sorted(Path(item).absolute() for item in directories):
        fd = anchored_dirfd(path)
        try:
            before = fingerprint(os.fstat(fd))
            names = sorted(os.listdir(fd))
            after = fingerprint(os.fstat(fd))
            need(before == after and names and all(type(name) is str for name in names),
                 "authority directory stable inventory:" + str(path))
            relative = str(path.relative_to(ROOT))
            vector[relative] = [str((path / name).relative_to(ROOT)) for name in names]
        finally:
            os.close(fd)
    return vector


def acyclic_edges(edges: Iterable[tuple[str, str]]) -> bool:
    graph: dict[str, set[str]] = defaultdict(set)
    for source, target in edges:
        graph[source].add(target)
    grey: set[str] = set()
    black: set[str] = set()
    def visit(node: str) -> bool:
        if node in black:
            return True
        if node in grey:
            return False
        grey.add(node)
        if not all(visit(child) for child in graph.get(node, ())):
            return False
        grey.remove(node)
        black.add(node)
        return True
    return all(visit(node) for node in tuple(graph))


def discover_numeric_authority() -> tuple[tuple[Path, ...], dict[str, Any]]:
    """Discover the complete C40->C39->... live authority closure fail-closed.

    Discovery captures each result before parsing and records whole candidate
    directories, audits, and explicitly referenced deliverable authorities.
    The discovery reads are not accepted as evidence; the returned set is then
    included in one full frozen snapshot and recaptured after the long replay.
    """
    pending: list[Path] = [C40_DIR]
    files: set[Path] = set()
    seen_dirs: set[Path] = set()
    parsed_json: set[Path] = set()
    edges: set[tuple[str, str]] = set()
    while pending:
        path = pending.pop()
        if path.is_dir():
            path = path.resolve(strict=True)
            need(path.is_relative_to(ROOT), "numeric authority directory contained")
            if path in seen_dirs:
                continue
            seen_dirs.add(path)
            fd = anchored_dirfd(path)
            try:
                names = tuple(sorted(os.listdir(fd)))
                entries = tuple(path / name for name in names)
                for entry in entries:
                    state = os.stat(entry.name, dir_fd=fd, follow_symlinks=False)
                    need(stat.S_ISREG(state.st_mode) and state.st_nlink == 1,
                         "numeric authority flat regular inventory:" + str(entry))
            finally:
                os.close(fd)
            files.update(entry.absolute() for entry in entries)
            result = path / "result.json"
            need(result in files, "numeric authority result present:" + str(path))
            pending.append(result)
            continue
        path = path.absolute()
        need(path.is_relative_to(ROOT), "numeric authority file contained")
        files.add(path)
        if path.suffix == ".json" and path not in parsed_json:
            parsed_json.add(path)
            cap = capture_bounded((path,), maximum_each=64 << 20,
                                  maximum_total=64 << 20)[path]
            try:
                value = strict_json(cap.raw, "authority discovery:" + str(path),
                                    canonical_required=False)
            except Reject:
                # Closed runtime result/audit objects must be strict JSON.  A
                # non-object referenced data certificate remains inert bytes.
                if path.name in {"result.json", "independent_audit.json"}:
                    raise
                continue
            if type(value) is dict:
                for target in authority_paths_from_result(value):
                    edges.add((str(path.relative_to(ROOT)), str(target.relative_to(ROOT))))
                    pending.append(target)
    directories = tuple(sorted(seen_dirs))
    ordered_files = tuple(sorted(files))
    ordered_edges = tuple(sorted(edges))
    file_vector = [{"path": str(path.relative_to(ROOT)),
                    "sha256": hashlib.sha256(capture_bounded(
                        (path,), maximum_each=MAX_EACH, maximum_total=MAX_EACH)[path].raw).hexdigest(),
                    "size": path.stat().st_size} for path in ordered_files]
    directory_vector = [str(path.relative_to(ROOT)) for path in directories]
    edge_vector = [list(edge) for edge in ordered_edges]
    directory_members = authority_directory_inventory(directories)
    file_paths = [row["path"] for row in file_vector]
    topology = {"root": str(C40_DIR.relative_to(ROOT)),
                "directory_members": directory_members,
                "reference_edges": edge_vector}
    closure = {"schema": "cm2.c65.numeric-authority-closure.pin.v1",
               "root": str(C40_DIR.relative_to(ROOT)),
               "directory_count": len(directories), "file_count": len(ordered_files),
               "reference_edge_count": len(ordered_edges),
               "total_bytes": sum(row["size"] for row in file_vector),
               "directory_members": directory_members, "reference_edges": edge_vector,
               "files": file_vector}
    need(C40_RESULT in files and C40_ROUTED in files and
         len(directories) == PIN["authority_directory_count"] and
         len(ordered_files) == PIN["authority_file_count"] and
         len(parsed_json) == PIN["authority_parsed_json_count"] and
         len(ordered_edges) == PIN["authority_edge_count"] and
         digest(directory_vector) == PIN["authority_directory_object"] and
         digest(file_vector) == PIN["authority_file_object"] and
         digest(file_paths) == PIN["authority_file_path_object"] and
         digest(directory_members) == PIN["authority_directory_members_object"] and
         digest(edge_vector) == PIN["authority_edge_object"] and
         digest(topology) == PIN["authority_topology_object"] and
         digest(closure) == PIN["authority_closure_object"] and
         closure["total_bytes"] == PIN["authority_total_bytes"] and
         acyclic_edges(ordered_edges),
         "numeric authority exact 9-dir/80-file/28-json/37-edge acyclic closure")
    return ordered_files, {"directories": directories, "edges": ordered_edges,
                           "directory_vector": directory_vector,
                           "file_vector": file_vector, "edge_vector": edge_vector,
                           "directory_inventory": directory_members,
                           "topology": topology, "closure": closure}


def runtime_paths_from_attestation() -> tuple[Path, ...]:
    raw = capture_bounded((RUNTIME_ATTESTATION,), maximum_each=4 << 20,
                          maximum_total=4 << 20)[RUNTIME_ATTESTATION].raw
    need(hashlib.sha256(raw).hexdigest() == PIN["runtime_attestation_file"],
         "sealed runtime attestation pin")
    value = strict_json(raw, "runtime attestation", canonical_required=False)
    need(type(value) is dict and value.get("verdict") == "PASS" and
         value.get("schema") == "cm2.round306c30b.python-flint-runtime-attestation.v1" and
         value.get("attestation_payload_sha256") ==
         "1d9aa48715a01bdd224582887fc95be175b8c2dbd47c35136a971874d16ad759",
         "sealed runtime attestation exact status/payload")
    installed = value["installed_distribution"]
    need(installed["distribution_name"] == "python-flint" and
         installed["distribution_version"] == "0.9.0" and
         installed["file_count"] == 139 and type(installed["file_table"]) is list and
         len(installed["file_table"]) == 139,
         "runtime attested distribution exact")
    site = SEALED_VENV / installed["site_packages_relpath"].split("site-packages/", 1)[-1]
    # site_packages_relpath itself already ends in site-packages; avoid accepting
    # an attestation-selected alternate root.
    site = SEALED_VENV / "lib/python3.12/site-packages"
    paths: list[Path] = [SEALED_PYTHON, PYVENV_CFG, RUNTIME_REQUIREMENTS, RUNTIME_LOCK,
                        RUNTIME_ATTESTATION]
    seen: set[str] = set()
    for row in installed["file_table"]:
        strict_keys(row, {"path", "sha256", "size"}, "runtime installed file row")
        relative = row["path"]
        need(type(relative) is str and relative not in seen and
             not relative.startswith(("/", "../")) and "/../" not in relative,
             "runtime installed path safe/unique")
        seen.add(relative)
        path = (site / relative).absolute()
        need(path.is_relative_to(SEALED_VENV), "runtime installed path contained")
        paths.append(path)
    native = value["native_runtime"]
    need(native["native_file_count"] == 42 and
         native["extension_module_count"] == 39 and
         native["bundled_library_count"] == 3,
         "runtime exact native closure counts")
    for row in (*native["extension_modules"], *native["bundled_libraries"]):
        path = (site / row["path"]).absolute()
        need(path in paths, "runtime native member included in attested distribution")
    return tuple(dict.fromkeys(paths))


def safe_runtime_tables(rows: list[dict[str, Any]]) -> tuple[
    list[dict[str, Any]], list[str], dict[str, list[str]],
]:
    safe = [copy.deepcopy(row) for row in rows
            if PurePosixPath(row["path"]).suffix != ".pyc" and
            PurePosixPath(row["path"]).parts[:2] != ("flint", "test")]
    safe.sort(key=lambda row: row["path"])
    paths = [row["path"] for row in safe]
    directories: set[PurePosixPath] = set()
    for text in paths:
        parent = PurePosixPath(text).parent
        while str(parent) != ".":
            directories.add(parent)
            parent = parent.parent
    members: dict[str, list[str]] = {}
    for directory in sorted(directories, key=str):
        values: set[str] = set()
        for text in paths:
            path = PurePosixPath(text)
            if path.parent == directory:
                values.add("f:" + path.name)
            elif directory in path.parents:
                values.add("d:" + path.parts[len(directory.parts)])
        members[str(directory)] = sorted(values)
    return safe, paths, members


def validate_runtime_snapshot(snapshot: Mapping[Path, Captured]) -> dict[str, Any]:
    pins = {
        RUNTIME_REQUIREMENTS: PIN["runtime_requirements_file"],
        RUNTIME_LOCK: PIN["runtime_lock_file"], RUNTIME_ATTESTATION: PIN["runtime_attestation_file"],
        PYVENV_CFG: PIN["pyvenv_cfg_file"], SEALED_PYTHON: PIN["python_file"],
        FLINT_INIT: PIN["flint_init_file"], FLINT_PYFLINT: PIN["flint_pyflint_file"],
        FLINT_LIBS[0]: PIN["libflint_file"], FLINT_LIBS[1]: PIN["libgmp_file"],
        FLINT_LIBS[2]: PIN["libmpfr_file"],
    }
    for path, expected in pins.items():
        need(path in snapshot and hashlib.sha256(snap_raw(snapshot, path)).hexdigest() == expected,
             "runtime exact pinned member:" + str(path))
    lock = strict_json(snap_raw(snapshot, RUNTIME_LOCK), "runtime lock",
                       canonical_required=False)
    need(lock == {
        "abi": "cp310-abi3", "architecture": "x86_64",
        "environment_relpath": ".cm2-runtime/python-flint-0.9.0",
        "flint_release": 30600, "flint_version": "3.6.0", "glibc": "2.39",
        "implementation": "cpython",
        "installer_command": ".cm2-runtime/python-flint-0.9.0/bin/python -m pip install --require-hashes -r deliverables/cm2_round306c30a_python_flint_requirements.lock",
        "machine_python_sha256": PIN["python_file"], "manylinux_floor": "manylinux_2_17_x86_64",
        "python_cache_tag": "cpython-312", "python_flint": "0.9.0",
        "python_version": "3.12.3", "schema": "cm2.round306c30a.python-flint-runtime-lock.v1",
        "wheel_filename": "python_flint-0.9.0-cp310-abi3-manylinux2014_x86_64.manylinux_2_17_x86_64.whl",
        "wheel_sha256": "376b88cacd30612479e839ffdba887599d3f9c8c0e214852bf80bb2b194e4d76",
    }, "runtime lock exact content")
    attestation = strict_json(snap_raw(snapshot, RUNTIME_ATTESTATION),
                              "runtime attestation", canonical_required=False)
    interpreter = attestation["interpreter"]
    need(interpreter["invoked_executable_relpath"] ==
         ".cm2-runtime/python-flint-0.9.0/bin/python" and
         interpreter["resolved_executable_path"] == str(SEALED_PYTHON) and
         interpreter["resolved_executable_sha256"] == PIN["python_file"] and
         interpreter["pyvenv_cfg_sha256"] == PIN["pyvenv_cfg_file"] and
         interpreter["python_version"] == "3.12.3" and
         attestation["imported_flint"]["python_flint_version"] == "0.9.0" and
         attestation["imported_flint"]["flint_version"] == "3.6.0",
         "runtime attestation interpreter/flint exact")
    installed_rows = attestation["installed_distribution"]["file_table"]
    site = SEALED_VENV / "lib/python3.12/site-packages"
    normalized_rows: list[dict[str, Any]] = []
    for row in installed_rows:
        normalized = strict_keys(row, {"path", "sha256", "size"},
                                 "attested runtime member")
        path = (site / normalized["path"]).absolute()
        need(path in snapshot and hashlib.sha256(snapshot[path].raw).hexdigest() ==
             normalized["sha256"] and len(snapshot[path].raw) == normalized["size"],
             "captured runtime row exact:" + normalized["path"])
        normalized_rows.append(copy.deepcopy(normalized))
    need(normalized_rows == sorted(normalized_rows, key=lambda row: row["path"]) and
         len(normalized_rows) == 139 and
         sum(row["size"] for row in normalized_rows) == PIN["full_runtime_total_bytes"] and
         digest(normalized_rows) == PIN["full_runtime_record_object"],
         "full runtime table exact order/count/hash/bytes")
    safe_rows, safe_paths, safe_members = safe_runtime_tables(normalized_rows)
    need(len(safe_rows) == PIN["safe_runtime_file_count"] and
         sum(row["size"] for row in safe_rows) == PIN["safe_runtime_total_bytes"] and
         digest(safe_rows) == PIN["safe_runtime_record_object"] and
         digest(safe_paths) == PIN["safe_runtime_path_object"] and
         digest(safe_members) == PIN["safe_runtime_directory_members_object"],
         "safe frozen runtime exact 98-row projected tree")
    # The venv entry point is a relative one-hop symlink.  Its link identity and
    # target are evidence even though only the resolved executable is read.
    link_state = os.lstat(SEALED_PYTHON_LINK)
    need(stat.S_ISLNK(link_state.st_mode) and os.readlink(SEALED_PYTHON_LINK) == "python3",
         "sealed venv python entry symlink exact")
    return {"python_sha256": PIN["python_file"], "sys_prefix": str(SEALED_VENV),
            "python_flint_version": "0.9.0", "flint_version": "3.6.0",
            "attestation_sha256": PIN["runtime_attestation_file"],
            "attested_distribution_member_count": 139,
            "safe_mirror_member_count": len(safe_rows),
            "safe_mirror_record_object_sha256": PIN["safe_runtime_record_object"],
            "safe_mirror_directory_members_object_sha256":
                PIN["safe_runtime_directory_members_object"],
            "runtime_snapshot_path_count": len(runtime_paths_from_attestation())}


def fixed_formal_paths(source_paths: Mapping[str, Path], numeric_paths: Iterable[Path],
                       runtime_paths: Iterable[Path]) -> tuple[Path, ...]:
    paths = (
        SELF, EXECUTOR, CONTROLLER, CHECKER, PRODUCER, CONTRACT, ASSIGNMENT, INVENTORY,
        AUTHORIZATION, C61_RESULT, C61_LEAVES, C61_PARENTS, C58_RESULT, C58_LEAVES,
        AGG_RESULT, AGG_LEAVES, AGG_SOURCES, AGG_PARENTS,
        CANONICAL, CANONICAL_COMPANION, GLOBAL_HEAD, GLOBAL_CLAIM, C53_TOKEN, C53_AUDIT_TOKEN,
        V1_REJECTION, V2_REJECTION, V3_REJECTION,
        PRODUCER_CONTRACT_REJECTION, PRODUCER_PARENT_REJECTION,
        *(receipt_path(shard) for shard in SHARDS),
        *(shard_ledger_path(shard) for shard in SHARDS),
        *(source_paths[module] for module in sorted(source_paths)),
        *numeric_paths,
        *runtime_paths,
    )
    unique = tuple(dict.fromkeys(path.absolute() for path in paths))
    need(len(unique) == len(set(unique)), "formal path set unique")
    return unique


def formal_snapshot() -> tuple[dict[Path, Captured], dict[str, Any]]:
    # Candidate-first receipt barrier and controller/executable identity precede
    # any ledger path derivation or ledger open.
    names_before = shard_name_barrier()
    runtime_before = runtime_barrier()
    runtime_link_before = runtime_link_record()
    source_paths, _discovery_sources = discover_source_closure()
    numeric_paths, numeric_metadata = discover_numeric_authority()
    runtime_paths = runtime_paths_from_attestation()
    paths = fixed_formal_paths(source_paths, numeric_paths, runtime_paths)
    snapshot = capture_bounded(paths)
    names_after = shard_name_barrier()
    runtime_after = runtime_barrier()
    need(names_before == names_after, "shard candidates stable across frozen capture")
    stable_runtime(runtime_before, runtime_after, "initial frozen capture")
    need(runtime_link_before == runtime_link_record(),
         "sealed runtime link stable across frozen capture")
    # Recompute closure exclusively from captured bytes.
    observed_sources = {
        module: hashlib.sha256(snapshot[path].raw).hexdigest()
        for module, path in sorted(source_paths.items())
    }
    need(digest(observed_sources) == PIN["numeric_source_closure_object"] and
         len(observed_sources) == PIN["numeric_source_closure_count"],
         "captured numeric source closure exact")
    observed_authority_files = [{"path": str(path.relative_to(ROOT)),
                                 "sha256": hashlib.sha256(snapshot[path].raw).hexdigest(),
                                 "size": len(snapshot[path].raw)} for path in numeric_paths]
    need(digest(observed_authority_files) == PIN["authority_file_object"] and
         authority_directory_inventory(numeric_metadata["directories"]) ==
         numeric_metadata["directory_inventory"],
         "captured exact numeric authority files/directories")
    runtime_descriptor = validate_runtime_snapshot(snapshot)
    return snapshot, {
        "shard_names": [list(names_before[0]), list(names_before[1])],
        "runtime": runtime_before,
        "source_modules": {module: str(path.relative_to(ROOT))
                           for module, path in sorted(source_paths.items())},
        "numeric_authority_file_count": len(tuple(numeric_paths)),
        "numeric_authority_directory_inventory": numeric_metadata["directory_inventory"],
        "numeric_authority_edges": [list(edge) for edge in numeric_metadata["edges"]],
        "runtime_descriptor": runtime_descriptor,
        "runtime_link": runtime_link_before,
        "frozen_input_count": len(snapshot),
        "frozen_input_object_sha256": snapshot_object(snapshot),
    }


class CapturedSourceLoader(importlib.abc.MetaPathFinder, importlib.abc.Loader):
    """Source-only loader for the authenticated local numerical closure."""

    def __init__(self, sources: Mapping[str, tuple[bytes, Path]]) -> None:
        self.sources = dict(sources)
        self.loaded: set[str] = set()

    def find_spec(self, fullname: str, path: Any = None,
                  target: ModuleType | None = None) -> Any:
        del path, target
        if fullname in self.sources:
            return importlib.util.spec_from_loader(fullname, self, origin=str(self.sources[fullname][1]))
        if fullname.startswith("cm2_"):
            raise ImportError("uncaptured local numeric module:" + fullname)
        return None

    def create_module(self, spec: Any) -> ModuleType | None:
        del spec
        return None

    def exec_module(self, module: ModuleType) -> None:
        name = module.__name__
        need(name in self.sources and name not in self.loaded,
             "captured source loader exact module/once:" + name)
        raw, virtual_path = self.sources[name]
        need(not raw.startswith(importlib.util.MAGIC_NUMBER) and b"\0" not in raw,
             "source bytes are not pyc:" + name)
        code = compile(raw, str(virtual_path), "exec", dont_inherit=True, optimize=0)
        module.__file__ = str(virtual_path)
        module.__cached__ = None
        self.loaded.add(name)
        exec(code, module.__dict__)


@contextlib.contextmanager
def authenticated_kernel(snapshot: Mapping[Path, Captured], metadata: dict[str, Any],
                         snapshot_root: Path) -> Iterator[Any]:
    module_paths = {module: ROOT / relative
                    for module, relative in metadata["source_modules"].items()}
    sources: dict[str, tuple[bytes, Path]] = {}
    for module, live_path in module_paths.items():
        need(live_path in snapshot, "source module in frozen snapshot:" + module)
        virtual = snapshot_root / live_path.relative_to(ROOT)
        sources[module] = (snapshot[live_path].raw, virtual)
    preloaded = sorted(name for name in sys.modules if name.startswith("cm2_"))
    need(not preloaded, "no pre-existing local numeric sys.modules:" + repr(preloaded))
    loader = CapturedSourceLoader(sources)
    sys.meta_path.insert(0, loader)
    old_bytecode = sys.dont_write_bytecode
    old_sys_path = list(sys.path)
    sys.dont_write_bytecode = True
    frozen_site = (snapshot_root / SEALED_VENV.relative_to(ROOT) /
                   Path("lib/python3.12/site-packages"))
    sys.path[:] = [str(frozen_site), "/usr/lib/python312.zip", "/usr/lib/python3.12",
                   "/usr/lib/python3.12/lib-dynload"]
    pre_flint_modules = {name for name in sys.modules if name == "flint" or name.startswith("flint.")}
    need(not pre_flint_modules, "no preloaded live flint modules")
    flint_module = importlib.import_module("flint")
    need(getattr(flint_module, "__version__", None) == "0.9.0" and
         Path(flint_module.__file__).absolute() ==
         frozen_site / "flint/__init__.py",
         "frozen-mirror python-flint 0.9.0 exact module")
    flint_ctx = flint_module.ctx
    old_context = {key: getattr(flint_ctx, key)
                   for key in ("prec", "dps", "cap", "threads", "pretty", "unicode")}
    flint_ctx.prec = 384
    flint_ctx.dps = 115
    flint_ctx.cap = 10
    flint_ctx.threads = 1
    flint_ctx.pretty = True
    flint_ctx.unicode = False
    try:
        spec = importlib.util.spec_from_loader(C41_ROOT_MODULE, loader,
                                               origin=str(sources[C41_ROOT_MODULE][1]))
        need(spec is not None, "C41 controlled loader spec")
        module = importlib.util.module_from_spec(spec)
        sys.modules[C41_ROOT_MODULE] = module
        loader.exec_module(module)
        need(loader.loaded == set(sources), "entire captured source closure loaded")
        need(all(getattr(sys.modules[name], "__cached__", None) is None for name in sources),
             "no pyc cache provenance")
        assert_flint_context(module)
        yield module
    finally:
        sys.meta_path.remove(loader)
        for name in sources:
            sys.modules.pop(name, None)
        for name in tuple(sys.modules):
            if name == "flint" or name.startswith("flint."):
                sys.modules.pop(name, None)
        sys.path[:] = old_sys_path
        sys.dont_write_bytecode = old_bytecode
        for key, value in old_context.items():
            setattr(flint_ctx, key, value)
        need(all(getattr(flint_ctx, key) == value for key, value in old_context.items()),
             "flint context restored in finally")
        need(not any(name in sys.modules for name in sources),
             "captured local modules removed after replay")


def flint_context_record(kernel: Any) -> dict[str, Any]:
    ctx = kernel.flint.ctx
    return {"python_flint_version": getattr(kernel.flint, "__version__", None),
            "flint_version": str(kernel.flint.__FLINT_VERSION__),
            "prec": ctx.prec, "dps": ctx.dps, "cap": ctx.cap,
            "threads": ctx.threads, "pretty": ctx.pretty, "unicode": ctx.unicode}


def assert_flint_context(kernel: Any) -> None:
    need(flint_context_record(kernel) == {
        "python_flint_version": "0.9.0", "flint_version": "3.6.0",
        "prec": 384, "dps": 115, "cap": 10, "threads": 1,
        "pretty": True, "unicode": False,
    }, "exact 384-bit flint context stable")


def materialize_snapshot(snapshot: Mapping[Path, Captured], destination: Path) -> None:
    """Create a private read-only mirror; numerical code sees no live input path."""
    for path, item in snapshot.items():
        if not mirror_member(path):
            continue
        relative = path.relative_to(ROOT)
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_CLOEXEC | getattr(os, "O_NOFOLLOW", 0)
        descriptor_fd = os.open(target, flags, 0o400)
        try:
            view = memoryview(item.raw)
            while view:
                written = os.write(descriptor_fd, view)
                need(written > 0, "snapshot materialization short write")
                view = view[written:]
            os.fsync(descriptor_fd)
        finally:
            os.close(descriptor_fd)
    # Freeze the complete mirror only after every file has closed and fsynced.
    directories = sorted((path for path in destination.rglob("*") if path.is_dir()),
                         key=lambda path: len(path.parts), reverse=True)
    for directory in directories:
        os.chmod(directory, 0o500)
    os.chmod(destination, 0o500)


def validate_mirror(snapshot: Mapping[Path, Captured], destination: Path) -> None:
    expected = {path.relative_to(ROOT): item.raw for path, item in snapshot.items()
                if mirror_member(path)}
    observed: set[Path] = set()
    for relative, raw in expected.items():
        target = destination / relative
        state = target.lstat()
        need(stat.S_ISREG(state.st_mode) and state.st_nlink == 1 and
             stat.S_IMODE(state.st_mode) == 0o400 and target.read_bytes() == raw,
             "private mirror exact read-only member:" + str(relative))
        observed.add(relative)
    actual = {path.relative_to(destination) for path in destination.rglob("*") if path.is_file()}
    need(actual == observed, "private mirror exact file member set")
    for directory in (destination, *(path for path in destination.rglob("*") if path.is_dir())):
        need(stat.S_IMODE(directory.stat().st_mode) == 0o500,
             "private mirror exact directory mode")


@contextlib.contextmanager
def live_root_open_guard() -> Iterator[None]:
    """Reject numerical Python attempts to reopen any live workspace path."""
    old_builtin_open, old_io_open, old_os_open = builtins.open, io.open, os.open
    root_text = str(ROOT)
    def reject_path(value: Any) -> None:
        if isinstance(value, (str, bytes, os.PathLike)):
            text = os.fsdecode(value)
            if os.path.isabs(text):
                normalized = os.path.abspath(text)
                need(not (normalized == root_text or normalized.startswith(root_text + os.sep)),
                     "numeric live-workspace open forbidden:" + normalized)
    def guarded_open(file: Any, *args: Any, **kwargs: Any) -> Any:
        reject_path(file)
        return old_builtin_open(file, *args, **kwargs)
    def guarded_io_open(file: Any, *args: Any, **kwargs: Any) -> Any:
        reject_path(file)
        return old_io_open(file, *args, **kwargs)
    def guarded_os_open(path: Any, flags: int, mode: int = 0o777, *, dir_fd: int | None = None) -> int:
        reject_path(path)
        return old_os_open(path, flags, mode, dir_fd=dir_fd)
    builtins.open, io.open, os.open = guarded_open, guarded_io_open, guarded_os_open
    try:
        yield
    finally:
        builtins.open, io.open, os.open = old_builtin_open, old_io_open, old_os_open


def thaw_mirror_for_cleanup(destination: Path) -> None:
    for directory in (destination, *(path for path in destination.rglob("*") if path.is_dir())):
        os.chmod(directory, 0o700)


def mirror_member(path: Path) -> bool:
    if not path.is_relative_to(ROOT):
        return False
    if path.is_relative_to(SEALED_VENV / "lib/python3.12/site-packages"):
        relative = path.relative_to(SEALED_VENV / "lib/python3.12/site-packages")
        text = relative.as_posix()
        if text.endswith(".pyc") or text.startswith("flint/test/"):
            return False
    return True


@contextlib.contextmanager
def frozen_working_directory(path: Path) -> Iterator[None]:
    """Make all relative lazy reads resolve only inside the private mirror."""
    saved = os.open(".", os.O_RDONLY | os.O_CLOEXEC)
    try:
        os.chdir(path)
        yield
    finally:
        os.fchdir(saved)
        os.close(saved)


def snap_raw(snapshot: Mapping[Path, Captured], path: Path) -> bytes:
    need(path.absolute() in snapshot, "path belongs to frozen snapshot:" + str(path))
    return snapshot[path.absolute()].raw


def authority_snapshot(snapshot: Mapping[Path, Captured]) -> dict[str, str]:
    observed = {
        "C50d_global_claim": hashlib.sha256(snap_raw(snapshot, GLOBAL_CLAIM)).hexdigest(),
        "C50d_global_head": hashlib.sha256(snap_raw(snapshot, GLOBAL_HEAD)).hexdigest(),
        "C53_audit_token": hashlib.sha256(snap_raw(snapshot, C53_AUDIT_TOKEN)).hexdigest(),
        "C53_successor_token": hashlib.sha256(snap_raw(snapshot, C53_TOKEN)).hexdigest(),
        "CM2_LATEST_STATUS.md": hashlib.sha256(snap_raw(snapshot, CANONICAL)).hexdigest(),
        "CM2_LATEST_STATUS.sha256": hashlib.sha256(
            snap_raw(snapshot, CANONICAL_COMPANION)).hexdigest(),
    }
    need(observed == EXPECTED_AUTHORITY and digest(observed) == PIN["authority_snapshot_object"],
         "live authority exact snapshot/object")
    need(snap_raw(snapshot, CANONICAL_COMPANION) ==
         (PIN["canonical_file"] + "  CM2_LATEST_STATUS.md\n").encode("ascii"),
         "canonical companion exact content")
    head = closed_json_field(
        snap_raw(snapshot, GLOBAL_HEAD), "global head", "authority_seal_object_sha256",
        PIN["global_head_file"], PIN["global_head_object"])
    need(head["post_seal_effective_checkpoint_object_sha256"] ==
         PIN["effective_checkpoint_object"] and
         head["successor_checkpoint_object_sha256"] == PIN["effective_checkpoint_object"],
         "global head effective checkpoint")
    return observed


def validate_rejections(snapshot: Mapping[Path, Captured]) -> dict[str, Any]:
    raw = snap_raw(snapshot, V1_REJECTION)
    text = raw.decode("utf-8", "strict")
    flat = " ".join(text.split())
    need(hashlib.sha256(raw).hexdigest() == PIN["v1_rejection_file"] and
         "REJECTED_PRE_CLOSE_VERIFIER_SOURCE_DRIFT__UNBOUND_SELF_TEST__ZERO_CREDIT" in text and
         PIN["rejected_v1_selftest_file"] in text and
         PIN["rejected_v1_selftest_object"] in text and
         "must never be used as a prerequisite" in flat,
         "v1 self-test terminal rejection exact semantics")
    v2_raw = snap_raw(snapshot, V2_REJECTION)
    v2_text = v2_raw.decode("utf-8", "strict")
    v2_flat = " ".join(v2_text.split())
    need(hashlib.sha256(v2_raw).hexdigest() == PIN["v2_rejection_file"] and
         PIN["rejected_v2_verifier_file"] in v2_text and
         "85/85" in v2_text and "eleven v2 formal targets were absent" in v2_flat and
         "All such credits remain exactly zero" in v2_flat and
         "must never be used as a" in v2_flat,
         "v2 verifier terminal rejection exact semantics")
    v3_raw = snap_raw(snapshot, V3_REJECTION)
    v3_text = v3_raw.decode("utf-8", "strict")
    v3_flat = " ".join(v3_text.split())
    need(hashlib.sha256(v3_raw).hexdigest() == PIN["v3_rejection_file"] and
         PIN["rejected_v3_verifier_file"] in v3_text and
         "REJECTED_V3_GLOBAL_HEAD_OBJECT_FIELD_MISMATCH_BEFORE_FORMAL_PUBLICATION__ZERO_CREDIT"
         in v3_text and "All eleven v3 formal targets were absent" in v3_flat and
         "authority_seal_object_sha256" in v3_text and
         PIN["global_head_object"] in v3_text and
         "must never be imported, executed as a prerequisite" in v3_flat,
         "v3 verifier terminal rejection exact semantics")
    contract_raw = snap_raw(snapshot, PRODUCER_CONTRACT_REJECTION)
    contract_text = contract_raw.decode("utf-8", "strict")
    contract_flat = " ".join(contract_text.split())
    need(hashlib.sha256(contract_raw).hexdigest() == PIN["producer_contract_rejection_file"] and
         "pre-publication rejection" in contract_text and PIN["contract_file"] in contract_text and
         "strict pretty-printed JSON" in contract_text and
         "208b305dc2bae74b2e7db61fe5ad5341b598afb8bba3f26cef85999a9c3b7a68" in contract_text and
         "No shard, authority, runtime, canonical file, or credit field was changed" in
         contract_flat and "must not be used as a producer, verifier input, manifest member" in
         contract_flat, "producer pretty-contract terminal rejection semantics")
    parent_raw = snap_raw(snapshot, PRODUCER_PARENT_REJECTION)
    parent_text = parent_raw.decode("utf-8", "strict")
    parent_flat = " ".join(parent_text.split())
    need(hashlib.sha256(parent_raw).hexdigest() == PIN["producer_parent_rejection_file"] and
         "parent-carry rejection" in parent_text and "23,997" in parent_text and
         "27,408" in parent_text and "48,287" in parent_text and "20,879" in parent_text and
         "386,327" in parent_text and "219,072" in parent_text and "167,255" in parent_text and
         "345eeb2465951c933893f2e372249e8bcc8d8c072784fa6c6eb2915d5c5a0dd8" in
         parent_text and PIN["producer_file"] in parent_text and
         "must not be used as a producer, verifier input, manifest member" in parent_flat,
         "producer parent-carry terminal rejection semantics")
    return {
        "v1_rejection_filename": V1_REJECTION.name,
        "v1_rejection_file_sha256": PIN["v1_rejection_file"],
        "rejected_v1_selftest_file_sha256": PIN["rejected_v1_selftest_file"],
        "rejected_v1_selftest_object_sha256": PIN["rejected_v1_selftest_object"],
        "v2_rejection_filename": V2_REJECTION.name,
        "v2_rejection_file_sha256": PIN["v2_rejection_file"],
        "rejected_v2_verifier_file_sha256": PIN["rejected_v2_verifier_file"],
        "v3_rejection_filename": V3_REJECTION.name,
        "v3_rejection_file_sha256": PIN["v3_rejection_file"],
        "rejected_v3_verifier_file_sha256": PIN["rejected_v3_verifier_file"],
        "producer_contract_rejection_file_sha256": PIN["producer_contract_rejection_file"],
        "producer_parent_rejection_file_sha256": PIN["producer_parent_rejection_file"],
        "rejected_producer_bytes_consumed": False,
        "rejected_v1_verifier_or_selftest_consumed": False,
        "rejected_v2_verifier_or_outputs_consumed": False,
        "rejected_v3_verifier_or_outputs_consumed": False,
    }


def program_independence(snapshot: Mapping[Path, Captured], aggregate: dict[str, Any]) -> dict[str, Any]:
    observed: dict[str, str] = {}
    for label, path, pin in (
        ("executor", EXECUTOR, PIN["executor_file"]),
        ("controller", CONTROLLER, PIN["controller_file"]),
        ("checker", CHECKER, PIN["checker_file"]),
    ):
        raw = snap_raw(snapshot, path)
        claim = hashlib.sha256(raw).hexdigest()
        need(claim == pin, label + ": source pin")
        ast.parse(raw.decode("utf-8", "strict"), filename=path.name)
        observed[label + "_file_sha256"] = claim
    producer_raw = snap_raw(snapshot, PRODUCER)
    producer_sha = hashlib.sha256(producer_raw).hexdigest()
    need(producer_sha == PIN["producer_file"] and
         aggregate["producer_file_sha256"] == producer_sha,
         "aggregate dynamically binds captured producer bytes")
    tree = ast.parse(producer_raw.decode("utf-8", "strict"), filename=PRODUCER.name)
    forbidden_modules = {EXECUTOR.stem, CONTROLLER.stem, CHECKER.stem}
    forbidden: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            forbidden.extend(alias.name for alias in node.names if alias.name in forbidden_modules)
        elif isinstance(node, ast.ImportFrom) and node.module in forbidden_modules:
            forbidden.append(str(node.module))
        elif isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name) and node.func.id in {
                "exec", "eval", "compile", "__import__",
            }:
                forbidden.append(node.func.id)
            elif isinstance(node.func, ast.Attribute) and node.func.attr in {
                "system", "popen", "run", "Popen", "call", "check_call", "check_output",
            }:
                forbidden.append(node.func.attr)
    source = producer_raw.decode("utf-8", "strict")
    need(not forbidden and "O_EXCL" in source and "O_NOFOLLOW" in source and "fsync" in source,
         "producer inert AST/no execution/no-replace")
    self_tree = ast.parse(snap_raw(snapshot, SELF).decode("utf-8", "strict"), filename=SELF.name)
    imports = set()
    for node in ast.walk(self_tree):
        if isinstance(node, ast.Import):
            imports.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.add(node.module)
    need(not (imports & (forbidden_modules | {PRODUCER.stem})),
         "v2 verifier never imports C65 programs")
    return {
        **observed,
        "aggregate_producer_file_sha256": producer_sha,
        "cold_verifier_file_sha256": hashlib.sha256(snap_raw(snapshot, SELF)).hexdigest(),
        "numeric_source_closure_object_sha256": PIN["numeric_source_closure_object"],
        "numeric_source_closure_count": PIN["numeric_source_closure_count"],
        "C65_programs_consumed_as_authenticated_inert_bytes_or_AST_only": True,
        "C65_programs_imported_or_executed": False,
        "numeric_kernel_loaded_only_from_captured_source_bytes": True,
        "pyc_or_preexisting_local_sys_modules_consumed": False,
    }


def validate_frozen_objects(snapshot: Mapping[Path, Captured]) -> tuple[
    dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any],
    dict[str, Any], list[dict[str, Any]],
]:
    # The historical contract is intentionally pretty-printed.  Exact pinned
    # bytes and object closure authenticate it; compact serialization is not a
    # requirement at this one boundary.
    contract = closed_json(snap_raw(snapshot, CONTRACT), "contract",
                           PIN["contract_file"], PIN["contract_object"], False)
    assignment = closed_json(snap_raw(snapshot, ASSIGNMENT), "assignment",
                             PIN["assignment_file"], PIN["assignment_object"])
    authorization = closed_json(snap_raw(snapshot, AUTHORIZATION), "authorization",
                                PIN["authorization_file"], PIN["authorization_object"])
    c61 = closed_json(snap_raw(snapshot, C61_RESULT), "C61 result",
                      PIN["C61_result_file"], PIN["C61_result_object"])
    c58 = closed_json(snap_raw(snapshot, C58_RESULT), "C58 result",
                      PIN["C58_result_file"], PIN["C58_result_object"])
    c40 = closed_json(snap_raw(snapshot, C40_RESULT), "C40 result",
                      PIN["C40_result_file"], PIN["C40_object"])
    need(contract["selection"]["exact_count"] == 20_879 and
         contract["selection"]["pair_indices_exactly"] == list(PAIRS) and
         contract["assignment"]["shard_ids_exactly"] == list(SHARDS) and
         contract["assignment"]["modulus"] == 64,
         "contract exact selection/shards")
    exact_int(contract["selection"]["exact_count"], 20_879, "contract count")
    exact_int(assignment["input_count"], 20_879, "assignment count")
    exact_int(assignment["shard_count"], 64, "assignment shard count")
    need(assignment["assignment_domain"] == ASSIGNMENT_DOMAIN and
         assignment["assignment_formula"] == "int(SHA256(preimage),16)%64" and
         assignment["assignment_preimage_schema"] == ASSIGNMENT_PREIMAGE_SCHEMA and
         assignment["assignment_complete"] is True and
         assignment["assignment_mutually_exclusive"] is True and
         assignment["candidate_is_authority"] is False and
         assignment["partial_statistics_are_formal_credit"] is False and
         assignment["runtime_canonical_pointer_or_seal_writes"] is False,
         "assignment exact protocol")
    zero_credit(assignment, "assignment")
    need(authorization["status"] ==
         "PASS_INDEPENDENT_FROZEN_ASSIGNMENT_BYTES_FOR_SHARD_EXECUTION__ZERO_CREDIT" and
         authorization["assignment"]["input_count"] == 20_879 and
         authorization["assignment"]["shard_count"] == 64 and
         authorization["assignment"]["complete"] is True and
         authorization["assignment"]["mutually_exclusive"] is True and
         authorization["assignment"]["source_identity_bijection"] is True and
         authorization["partial_shards_are_an_aggregate"] is False and
         authorization["candidate_is_authority"] is False and
         authorization["runtime_canonical_pointer_or_seal_writes"] is False,
         "authorization exact zero-credit protocol")
    zero_credit(authorization, "authorization")
    need(c61["schema"] == "cm2.round306c61s12.depth12-16shard.v1.aggregate-result.v4" and
         c61["coverage"]["disposition_census"] == {
             "STRICT_TERMINAL": C61_LEDGER_TERMINAL,
             "COLLISION3_READY": 0, "COLLISION2_HANDOFF": C61_FULL_BASE_C2,
         } and c61["coverage"]["output_leaf_count"] == 44_876 and
         c61["coverage"]["carried_C57_terminal_leaves"] == 462 and
         c61["coverage"]["carried_C58_terminal_leaves"] == 2_949 and
         c61["invariants"]["C57_C58_C61_parent_carry_complete"] is True and
         c61["invariants"]["all_12_combined_parents_prefix_free_and_Kraft_one"] is True,
         "C61 result full-base carry certificate")
    zero_credit(c61, "C61")
    parent_desc = descriptor(c61["ledgers"]["parent_summaries"], C61_PARENTS.name,
                             "PAIR_INDEX_ASCENDING", "C61 parent descriptor")
    need(parent_desc == {
        "filename": C61_PARENTS.name, "order": "PAIR_INDEX_ASCENDING", "row_count": 12,
        "row_hash_line_sequence_sha256":
            "48077d4a72d4688083e669994734ea3b3b1d800dd6259c207a8e3dcbf85cd8ba",
        "sha256": PIN["C61_parent_file"], "size": 947,
    }, "C61 frozen parent descriptor exact")
    parent_rows = list(iter_gzip(snap_raw(snapshot, C61_PARENTS), parent_desc,
                                 "C61 parent summaries", 4 << 20))
    totals: Counter[str] = Counter()
    for pair, row in zip(PAIRS, parent_rows, strict=True):
        strict_keys(row, C61_PARENT_KEYS, "C61 parent row")
        need(row["pair_index"] == pair and row["path_prefix_free"] is True and
             row["parent_Kraft_conservation"] == "1" and
             row["combined_leaf_count"] == row["strict_terminal_leaf_count"] +
             row["collision3_ready_leaf_count"] + row["collision2_handoff_leaf_count"] and
             row["whole_pair_terminal"] is
             (row["collision3_ready_leaf_count"] == row["collision2_handoff_leaf_count"] == 0) and
             row["whole_pair_credit"] == row["D02_gate_credit"] == 0,
             "C61 parent exact row semantics")
        for key in ("combined_leaf_count", "strict_terminal_leaf_count",
                    "collision3_ready_leaf_count", "collision2_handoff_leaf_count"):
            exact_nonnegative_int(row[key], "C61 parent:" + key)
        totals["combined"] += row["combined_leaf_count"]
        totals["terminal"] += row["strict_terminal_leaf_count"]
        totals["c3"] += row["collision3_ready_leaf_count"]
        totals["c2"] += row["collision2_handoff_leaf_count"]
    need(len(parent_rows) == 12 and totals == Counter({
        "combined": C61_FULL_BASE_LEAVES, "terminal": C61_FULL_BASE_TERMINAL,
        "c2": C61_FULL_BASE_C2,
    }), "C61 parent baseline exact 48287/27408/20879")
    routed_desc = descriptor(c40["ledgers"]["routed_leaf_cells"], C40_ROUTED.name,
                             "C39_ROW_ORDER_THEN_PATH", "C40 routed descriptor")
    need(routed_desc["sha256"] == PIN["C40_routed_file"], "C40 routed pin")
    return contract, assignment, authorization, c61, c58, c40, parent_rows


def expected_assignment_row(source: dict[str, Any], c58: dict[str, Any]) -> dict[str, Any]:
    claim = hashlib.sha256(assignment_preimage(source["row_sha256"], source["path"])).hexdigest()
    shard = int(claim, 16) % 64
    need(c58["row_sha256"] == source["source_C58_leaf_row_sha256"] and
         c58["disposition"] == "COLLISION2_HANDOFF" and
         c58["source_handoff_ordinal"] == source["source_handoff_ordinal"] and
         c58["path"] == source["source_path"] and source["path"].startswith(c58["path"]) and
         c58["pair_index"] == source["pair_index"] and
         source["continuation"]["prior_C58_leaf_row_sha256"] == c58["row_sha256"] and
         source["continuation"]["prior_C58_handoff_object_sha256"] ==
         c58["collision2_handoff"]["handoff_object_sha256"], "C61/C58 lineage")
    body = {
        "schema": "cm2.round306c65s18.depth18-64shard.v2.assignment-row",
        "assignment_preimage_sha256": claim, "shard_id": shard,
        "source_C61_aggregate_leaf_row_sha256": source["row_sha256"],
        "source_C61_continuation_object_sha256":
            source["continuation"]["continuation_object_sha256"],
        "source_C61_source_shard_row_sha256": source["source_shard_row_sha256"],
        "source_C58_leaf_row_sha256": source["source_C58_leaf_row_sha256"],
        "source_handoff_ordinal": source["source_handoff_ordinal"],
        "source_path": source["source_path"], "path": source["path"],
        "pair_index": source["pair_index"],
        "parent_volume_fraction": source["parent_volume_fraction"],
        "source_C61_disposition": source["disposition"],
        "source_C61_next_collision_index": source["continuation"]["next_collision_index"],
        "assignment_credit": 0, "formal_credit": 0,
        "whole_parent_credit": 0, "D02_gate_credit": 0,
    }
    return {**body, "row_sha256": digest(body)}


def load_source_universe(snapshot: Mapping[Path, Captured], assignment: dict[str, Any],
                         authorization: dict[str, Any], c61: dict[str, Any],
                         c58: dict[str, Any]) -> tuple[
    list[dict[str, Any]], list[dict[str, Any]], dict[str, dict[str, Any]],
    dict[int, list[dict[str, Any]]], dict[int, list[dict[str, Any]]],
]:
    c58_desc = descriptor(c58["ledgers"]["leaves"], C58_LEAVES.name,
                          "SOURCE_HANDOFF_ORDINAL_THEN_PATH", "C58 leaves")
    need(c58_desc["sha256"] == PIN["C58_leaf_file"], "C58 leaf pin")
    c58_rows = list(iter_gzip(snap_raw(snapshot, C58_LEAVES), c58_desc, "C58 leaves",
                              256 << 20))
    c58_by_hash = {row["row_sha256"]: row for row in c58_rows}
    need(len(c58_rows) == len(c58_by_hash) == 5_548, "C58 unique universe")
    c61_desc = descriptor(c61["ledgers"]["aggregate_leaves"], C61_LEAVES.name,
                          "SOURCE_HANDOFF_ORDINAL_THEN_PATH", "C61 leaves")
    need(c61_desc["sha256"] == PIN["C61_leaf_file"], "C61 leaf pin")
    selected: list[dict[str, Any]] = []
    carried: dict[int, list[dict[str, Any]]] = defaultdict(list)
    source_sequence = hashlib.sha256()
    continuation_sequence = hashlib.sha256()
    census: Counter[str] = Counter()
    for row in iter_gzip(snap_raw(snapshot, C61_LEAVES), c61_desc, "C61 leaves", 512 << 20):
        strict_keys(row, C61_ROW_KEYS, "C61 leaf row")
        need(row["pair_index"] in PAIRS, "C61 pair")
        zero_credit(row, "C61 leaf")
        census[row["disposition"]] += 1
        if row["disposition"] == "STRICT_TERMINAL":
            need(row["continuation"] is None, "C61 strict continuation")
            exact_int(row["local_terminal_credit"], 1, "C61 terminal local credit")
            carried[row["pair_index"]].append(row)
        elif row["disposition"] == "COLLISION2_HANDOFF":
            continuation = row["continuation"]
            need(type(continuation) is dict and len(row["path"]) == 21 and
                 row["parent_volume_fraction"] == "1/2097152", "C61 selected predicate")
            exact_int(continuation["next_collision_index"], 2, "C61 next collision")
            exact_int(row["additional_depth_from_C58"], 6, "C61 depth")
            exact_int(row["local_terminal_credit"], 0, "C61 nonterminal local")
            open_value = copy.deepcopy(continuation)
            claim = open_value.pop("continuation_object_sha256")
            need(digest(open_value) == claim, "C61 continuation closure")
            selected.append(row)
            source_sequence.update((row["row_sha256"] + "\n").encode("ascii"))
            continuation_sequence.update((claim + "\n").encode("ascii"))
        else:
            raise Reject("unexpected C61 disposition")
    need(census == Counter({"STRICT_TERMINAL": C61_LEDGER_TERMINAL,
                            "COLLISION2_HANDOFF": C61_FULL_BASE_C2}) and
         len(selected) == len({row["row_sha256"] for row in selected}) == 20_879 and
         set(carried) == set(PAIRS), "C61 exact selected/carried universe")
    need(source_sequence.hexdigest() ==
         assignment["filtered_source_row_sha256_line_sequence_sha256"] and
         continuation_sequence.hexdigest() ==
         assignment["filtered_continuation_object_sha256_line_sequence_sha256"],
         "C61 filtered sequences")
    inventory_desc = descriptor(assignment["inventory"], INVENTORY.name,
                                "C61_V4_AGGREGATE_LEDGER_ORDER_FILTERED_COLLISION2_HANDOFF",
                                "assignment inventory")
    need(inventory_desc["sha256"] == PIN["inventory_file"], "inventory pin")
    observed = iter_gzip(snap_raw(snapshot, INVENTORY), inventory_desc,
                         "assignment inventory", 256 << 20)
    rebuilt: list[dict[str, Any]] = []
    by_shard: dict[int, list[dict[str, Any]]] = {shard: [] for shard in SHARDS}
    counts: Counter[int] = Counter()
    preimages = hashlib.sha256()
    for source, row in zip(selected, observed, strict=True):
        c58_source = c58_by_hash.get(source["source_C58_leaf_row_sha256"])
        need(c58_source is not None, "C61 source in C58")
        expected = expected_assignment_row(source, c58_source)
        need(strict_keys(row, ASSIGNMENT_ROW_KEYS, "assignment row") == expected,
             "assignment exact independent rebuild")
        rebuilt.append(expected)
        by_shard[expected["shard_id"]].append(expected)
        counts[expected["shard_id"]] += 1
        preimages.update((expected["assignment_preimage_sha256"] + "\n").encode("ascii"))
    try:
        next(observed)
    except StopIteration:
        pass
    else:
        raise Reject("assignment inventory extra row")
    count_map = {str(shard): counts[shard] for shard in SHARDS}
    need(len(rebuilt) == 20_879 and count_map == assignment["per_shard_input_counts"] ==
         authorization["assignment"]["per_shard_input_counts"] and
         preimages.hexdigest() == assignment["ordered_preimage_sha256_line_sequence_sha256"] ==
         authorization["assignment"]["ordered_preimage_sha256_line_sequence_sha256"],
         "assignment global/per-shard closure")
    return selected, rebuilt, c58_by_hash, carried, by_shard


def validate_continuation(row: dict[str, Any]) -> None:
    disposition = row["disposition"]
    exact_int(row["local_terminal_credit"], 1 if disposition == "STRICT_TERMINAL" else 0,
              "row local terminal credit")
    if disposition == "STRICT_TERMINAL":
        need(row["continuation"] is None, "terminal continuation null")
        return
    continuation = strict_keys(row["continuation"], CONTINUATION_KEYS, "continuation")
    body = copy.deepcopy(continuation)
    claim = body.pop("continuation_object_sha256")
    expected_index = 3 if disposition == "COLLISION3_READY" else 2
    need(digest(body) == claim and continuation["next_collision_index"] == expected_index and
         continuation["exact_representative_box"] == row["exact_representative_box"] and
         continuation["exact_reflected_box"] == row["exact_reflected_box"] and
         continuation["route_classification"] == row["route_classification"] and
         continuation["route_witness"] == row["route_witness"] and
         continuation["route_method"] == row["route_method"],
         "continuation closure/index/route/box binding")
    exact_int(continuation["next_collision_index"], expected_index, "continuation index")
    exact_int(continuation["continuation_credit"], 0, "continuation credit")


def aggregate_leaf(row: dict[str, Any]) -> dict[str, Any]:
    body = {key: copy.deepcopy(value) for key, value in row.items()
            if key not in {"schema", "shard_id", "row_sha256"}}
    result = {
        "schema": AGG_SCHEMA + ".aggregate-leaf-row",
        "source_C65_shard_id": row["shard_id"],
        "source_C65_shard_row_sha256": row["row_sha256"], **body,
    }
    return {**result, "row_sha256": digest(result)}


def validate_receipts_and_ledgers(snapshot: Mapping[Path, Captured],
                                  by_shard: dict[int, list[dict[str, Any]]],
                                  authority: dict[str, str]) -> tuple[
    list[dict[str, Any]], dict[str, dict[str, Any]], dict[str, int], dict[str, int], int,
]:
    receipts: list[dict[str, Any]] = []
    source_groups: dict[str, dict[str, Any]] = {}
    global_disposition: Counter[str] = Counter()
    global_raw: Counter[str] = Counter()
    global_routes = 0
    receipt_files: set[str] = set()
    receipt_objects: set[str] = set()
    ledger_files: set[str] = set()
    for shard in SHARDS:
        raw = snap_raw(snapshot, receipt_path(shard))
        value = closed_json(raw, f"receipt {shard:02d}")
        strict_keys(value, RECEIPT_KEYS, f"receipt {shard:02d}")
        need(value["schema"] == SHARD_SCHEMA + ".shard-receipt" and
             value["status"] == "PASS_COMPLETE_NO_REPLACE_DEPTH18_SHARD__ZERO_CREDIT" and
             value["runner_file_sha256"] == PIN["executor_file"] and
             value["assignment_contract_file_sha256"] == PIN["contract_file"] and
             value["assignment_contract_object_sha256"] == PIN["contract_object"] and
             value["assignment_authorization_file_sha256"] == PIN["authorization_file"] and
             value["assignment_authorization_object_sha256"] == PIN["authorization_object"] and
             value["assignment_result_file_sha256"] == PIN["assignment_file"] and
             value["assignment_result_object_sha256"] == PIN["assignment_object"] and
             value["assignment_inventory_sha256"] == PIN["inventory_file"] and
             value["assignment_preimage_schema"] == ASSIGNMENT_PREIMAGE_SCHEMA and
             value["assignment_formula"] == "int(SHA256(preimage),16)%64" and
             value["authority_snapshot_before"] == value["authority_snapshot_after"] == authority and
             value["authority_snapshot_object_sha256"] == PIN["authority_snapshot_object"] and
             value["shard_complete"] is True and
             value["partial_statistics_are_formal_credit"] is False and
             value["runtime_canonical_pointer_or_seal_writes"] is False,
             f"receipt {shard:02d} full exact protocol")
        exact_int(value["shard_id"], shard, "receipt shard")
        exact_int(value["shard_count"], 64, "receipt shard count")
        exact_int(value["additional_binary_depth"], 6, "receipt depth")
        exact_int(value["assigned_input_count"], len(by_shard[shard]), "receipt assignment count")
        exact_nonnegative_int(value["route_evaluation_count"], "receipt route count")
        zero_credit(value, "receipt")
        desc = descriptor(value["output_ledger"], shard_ledger_path(shard).name,
                          "ASSIGNMENT_INVENTORY_ORDER_THEN_PATH", "shard ledger")
        receipt_file = hashlib.sha256(raw).hexdigest()
        need(receipt_file not in receipt_files and value["object_sha256"] not in receipt_objects and
             desc["sha256"] not in ledger_files, "unique receipt/object/ledger identities")
        receipt_files.add(receipt_file)
        receipt_objects.add(value["object_sha256"])
        ledger_files.add(desc["sha256"])
        assigned = by_shard[shard]
        index = {row["source_C61_aggregate_leaf_row_sha256"]: ordinal
                 for ordinal, row in enumerate(assigned)}
        need(len(index) == len(assigned), "per-shard assignment uniqueness")
        seq = hashlib.sha256()
        for row in assigned:
            seq.update((row["assignment_preimage_sha256"] + "\n").encode("ascii"))
        need(seq.hexdigest() == value["ordered_assignment_preimage_sha256_line_sequence_sha256"],
             "receipt assignment sequence")
        groups: dict[str, dict[str, Any]] = {}
        previous = (-1, "")
        shard_disposition: Counter[str] = Counter()
        shard_raw: Counter[str] = Counter()
        for row in iter_gzip(snap_raw(snapshot, shard_ledger_path(shard)), desc,
                             f"shard {shard:02d}", 512 << 20):
            strict_keys(row, SHARD_ROW_KEYS, "shard row")
            need(row["schema"] == SHARD_SCHEMA + ".shard-leaf-row" and
                 row["disposition"] in DISPOSITIONS, "shard row schema/disposition")
            exact_int(row["shard_id"], shard, "shard row id")
            need(type(row["additional_depth_from_C61"]) is int and
                 0 <= row["additional_depth_from_C61"] <= 6, "shard row depth")
            zero_credit(row, "shard row")
            validate_continuation(row)
            source_hash = row["source_C61_aggregate_leaf_row_sha256"]
            need(source_hash in index, "shard row assigned source")
            ordinal = index[source_hash]
            order = (ordinal, row["path"])
            need(order > previous, "shard assignment/path strict order")
            previous = order
            assignment_row = assigned[ordinal]
            need(row["assignment_preimage_sha256"] == assignment_row["assignment_preimage_sha256"] and
                 row["source_C61_shard_row_sha256"] ==
                 assignment_row["source_C61_source_shard_row_sha256"] and
                 row["source_C58_leaf_row_sha256"] == assignment_row["source_C58_leaf_row_sha256"] and
                 row["source_handoff_ordinal"] == assignment_row["source_handoff_ordinal"] and
                 row["pair_index"] == assignment_row["pair_index"] and
                 row["source_path"] == assignment_row["path"] and
                 row["C58_source_path"] == assignment_row["source_path"],
                 "shard row assignment lineage")
            group = groups.setdefault(source_hash, {
                "paths": [], "volumes": [], "rows": [], "aggregate_rows": [],
                "dispositions": Counter(), "raw": Counter(), "shard_id": shard,
            })
            group["paths"].append(row["path"])
            group["volumes"].append(fraction(row["parent_volume_fraction"]))
            group["rows"].append(row)
            group["aggregate_rows"].append(aggregate_leaf(row))
            group["dispositions"][row["disposition"]] += 1
            group["raw"][row["route_classification"]] += 1
            shard_disposition[row["disposition"]] += 1
            shard_raw[row["route_classification"]] += 1
        need(set(groups) == set(index), "shard exact source coverage")
        summaries: list[dict[str, Any]] = []
        shard_routes = 0
        for assignment_row in assigned:
            source_hash = assignment_row["source_C61_aggregate_leaf_row_sha256"]
            group = groups[source_hash]
            need(prefix_free(group["paths"]) and
                 sum(group["volumes"], Fraction(0)) ==
                 fraction(assignment_row["parent_volume_fraction"]), "source prefix/Kraft")
            routes = trie_route_count(assignment_row["path"], group["paths"])
            shard_routes += routes
            row_sequence = hashlib.sha256(
                "".join(row["row_sha256"] + "\n" for row in group["rows"]).encode("ascii")
            ).hexdigest()
            summary = {
                "assignment_preimage_sha256": assignment_row["assignment_preimage_sha256"],
                "source_C61_aggregate_leaf_row_sha256": source_hash,
                "source_output_row_count": len(group["rows"]),
                "source_output_row_hash_line_sequence_sha256": row_sequence,
                "source_Kraft_conservation": assignment_row["parent_volume_fraction"],
                "source_prefix_free": True,
            }
            summaries.append(summary)
            need(source_hash not in source_groups, "cross-shard source uniqueness")
            group["row_sequence"] = row_sequence
            group["aggregate_sequence"] = hashlib.sha256(
                "".join(row["row_sha256"] + "\n" for row in group["aggregate_rows"]).encode("ascii")
            ).hexdigest()
            group["trie_route_evaluations"] = routes
            source_groups[source_hash] = group
        need(value["input_assignment_rows"] == summaries and
             value["route_evaluation_count"] == shard_routes and
             value["output_disposition_census"] ==
             {key: shard_disposition[key] for key in DISPOSITIONS} and
             value["raw_classification_census"] == dict(sorted(shard_raw.items())),
             f"receipt {shard:02d} exact source summaries/trie routes/census")
        for summary in value["input_assignment_rows"]:
            strict_keys(summary, RECEIPT_SOURCE_KEYS, "receipt source summary")
            exact_nonnegative_int(summary["source_output_row_count"], "receipt source count")
            need(summary["source_prefix_free"] is True and
                 summary["source_Kraft_conservation"] == "1/2097152",
                 "receipt source summary exact types")
        for census in (value["output_disposition_census"], value["raw_classification_census"]):
            need(type(census) is dict and all(type(count) is int and count >= 0
                                              for count in census.values()),
                 "receipt census exact integer types")
        global_routes += shard_routes
        global_disposition.update(shard_disposition)
        global_raw.update(shard_raw)
        receipts.append(value)
    need(len(receipts) == 64 and len(source_groups) == 20_879 and
         len(receipt_files) == len(receipt_objects) == len(ledger_files) == 64,
         "64-shard receipt/source closure")
    return (receipts, source_groups,
            {key: global_disposition[key] for key in DISPOSITIONS},
            dict(sorted(global_raw.items())), global_routes)


def aggregate_descriptors(aggregate: dict[str, Any]) -> tuple[
    dict[str, Any], dict[str, Any], dict[str, Any],
]:
    need(type(aggregate["ledgers"]) is dict and
         set(aggregate["ledgers"]) == {"aggregate_leaves", "source_summaries", "parent_summaries"},
         "aggregate exact descriptor map")
    leaves = descriptor(aggregate["ledgers"]["aggregate_leaves"], AGG_LEAVES.name,
                        "C61_V4_FILTERED_C2_ORDER_THEN_CHILD_PATH", "aggregate leaves")
    sources = descriptor(aggregate["ledgers"]["source_summaries"], AGG_SOURCES.name,
                         "C61_V4_FILTERED_C2_ORDER", "aggregate sources")
    parents = descriptor(aggregate["ledgers"]["parent_summaries"], AGG_PARENTS.name,
                         "PAIR_INDEX_ASCENDING", "aggregate parents")
    exact_int(sources["row_count"], 20_879, "aggregate source count")
    exact_int(parents["row_count"], 12, "aggregate parent count")
    return leaves, sources, parents


def numeric_context(kernel: Any, frozen_root: Path) -> tuple[
    dict[str, tuple[int, dict[str, Any]]], dict[str, dict[str, Any]],
    dict[str, dict[str, Any]], dict[str, Any],
]:
    c40_directory = frozen_root / C40_DIR.relative_to(ROOT)
    c40_result = kernel.c40a.pinned_result(c40_directory, PIN["C40_object"], "C40 result")
    authority = c40_result["C39_authority"]
    c39_path = (frozen_root / authority["path"]).resolve()
    c39_audit = (frozen_root / authority["independent_audit_path"]).resolve()
    need(c39_path.is_relative_to(frozen_root) and c39_audit.is_relative_to(frozen_root),
         "frozen numeric authority paths contained")
    c39_result, _audit, _rows, _parents = kernel.c40a.load_c39_authority(c39_path, c39_audit)
    c38_index, cells, config = kernel.c40a.load_geometry_authority(c39_result)
    config["cores"] = tuple(kernel.round139.lower.core_cert.physical_cores())
    c40_rows = kernel.c40a.pinned_ledger(c40_directory, c40_result,
                                         "routed_leaf_cells", "C40 routed leaves")
    c40_index = {row["row_sha256"]: (ordinal, row)
                 for ordinal, row in enumerate(c40_rows)}
    need(len(c40_rows) == len(c40_index) == 35_009, "C40 routed row universe")
    kernel.install_complete_cache()
    return c40_index, c38_index, cells, config


def independent_expected_row(kernel: Any, assignment_row: dict[str, Any],
                             source: dict[str, Any], c58_source: dict[str, Any],
                             path: str, depth: int, volume: Fraction,
                             task: dict[str, Any], config: dict[str, Any],
                             route: dict[str, Any]) -> dict[str, Any]:
    family = kernel.disposition_family(route["classification"])
    if family == "TERMINAL_EXCLUDED":
        disposition, next_collision = "STRICT_TERMINAL", None
    elif family == "COLLISION3_READY":
        disposition, next_collision = "COLLISION3_READY", 3
    else:
        need(family == "RESIDUAL_OUTER" and depth == ADDITIONAL_DEPTH,
             "only depth6 residual is collision2 handoff")
        disposition, next_collision = "COLLISION2_HANDOFF", 2
    exact_box = kernel.box_payload(route["box"])
    reflected = kernel.reflected_box(task["c38_source"]["representative_origin_key"],
                                      route["box"])
    continuation: dict[str, Any] | None = None
    if next_collision is not None:
        continuation = {
            "next_collision_index": next_collision,
            "prior_C61_aggregate_leaf_row_sha256": source["row_sha256"],
            "prior_C61_shard_row_sha256": source["source_shard_row_sha256"],
            "prior_C61_continuation_object_sha256":
                source["continuation"]["continuation_object_sha256"],
            "prior_C58_leaf_row_sha256": c58_source["row_sha256"],
            "prior_C58_handoff_object_sha256":
                c58_source["collision2_handoff"]["handoff_object_sha256"],
            "collision1_history_row_sha256":
                source["continuation"]["collision1_history_row_sha256"],
            "collision1_original_owner": source["continuation"]["collision1_original_owner"],
            "collision1_event_order": source["continuation"]["collision1_event_order"],
            "exact_representative_box": exact_box, "exact_reflected_box": reflected,
            "route_classification": route["classification"],
            "route_witness": route["witness"], "route_method": route["route_method"],
            "continuation_credit": 0,
        }
        continuation["continuation_object_sha256"] = digest(continuation)
    body = {
        "schema": SHARD_SCHEMA + ".shard-leaf-row", "shard_id": assignment_row["shard_id"],
        "assignment_preimage_sha256": assignment_row["assignment_preimage_sha256"],
        "source_C61_aggregate_leaf_row_sha256": source["row_sha256"],
        "source_C61_shard_row_sha256": source["source_shard_row_sha256"],
        "source_C58_leaf_row_sha256": c58_source["row_sha256"],
        "source_handoff_ordinal": source["source_handoff_ordinal"],
        "C58_source_path": source["source_path"], "source_path": source["path"],
        "path": path, "additional_depth_from_C61": depth,
        "nominal_additional_depth_from_C58": source["additional_depth_from_C58"] + depth,
        "pair_index": source["pair_index"], "parent_volume_fraction": str(volume),
        "exact_representative_box": exact_box, "exact_reflected_box": reflected,
        "route_classification": route["classification"], "route_witness": route["witness"],
        "route_method": route["route_method"], "disposition": disposition,
        "continuation": continuation,
        "local_terminal_credit": int(disposition == "STRICT_TERMINAL"),
        "formal_credit": 0, "whole_parent_credit": 0, "D02_gate_credit": 0,
    }
    return {**body, "row_sha256": digest(body)}


def independent_numeric_replay(kernel: Any, frozen_root: Path,
                               selected: list[dict[str, Any]],
                               inventory: list[dict[str, Any]],
                               c58_by_hash: dict[str, dict[str, Any]],
                               structural: dict[str, dict[str, Any]],
                               aggregate_rows: Iterator[dict[str, Any]],
                               source_rows: Iterator[dict[str, Any]]) -> tuple[
    dict[int, list[dict[str, Any]]], dict[str, int], dict[str, int], int, int, int, int,
]:
    c40_index, c38_index, cells, config = numeric_context(kernel, frozen_root)
    replacements: dict[int, list[dict[str, Any]]] = defaultdict(list)
    disposition_total: Counter[str] = Counter()
    raw_total: Counter[str] = Counter()
    route_total = 0
    leaf_total = 0
    whole_terminal = 0
    whole_terminal_or_c3 = 0
    task_cache: dict[str, dict[str, Any]] = {}
    for ordinal, (source, assignment_row) in enumerate(zip(selected, inventory, strict=True)):
        c58_source = c58_by_hash[source["source_C58_leaf_row_sha256"]]
        c40_hash = c58_source["C40_source_row_sha256"]
        if c40_hash not in task_cache:
            need(c40_hash in c40_index, "C58 source belongs to frozen C40")
            c40_ordinal, c40_source = c40_index[c40_hash]
            task_cache[c40_hash] = kernel.task_for_source(
                c40_ordinal, c40_source, c38_index, cells, config["source_chart_seams"])
        task = task_cache[c40_hash]
        stack: list[tuple[str, int, Fraction]] = [
            (source["path"], 0, fraction(source["parent_volume_fraction"]))
        ]
        expected_rows: list[dict[str, Any]] = []
        source_routes = 0
        while stack:
            path, depth, volume = stack.pop()
            assert_flint_context(kernel)
            route = kernel.independent_route_at_path(task, path, config)
            assert_flint_context(kernel)
            source_routes += 1
            route_total += 1
            family = kernel.disposition_family(route["classification"])
            if family == "RESIDUAL_OUTER" and depth < ADDITIONAL_DEPTH:
                stack.append((path + "1", depth + 1, volume / 2))
                stack.append((path + "0", depth + 1, volume / 2))
                continue
            expected_rows.append(independent_expected_row(
                kernel, assignment_row, source, c58_source, path, depth, volume,
                task, config, route))
        paths = [row["path"] for row in expected_rows]
        need(paths == sorted(paths) and prefix_free(paths) and
             trie_route_count(source["path"], paths) == source_routes and
             sum((fraction(row["parent_volume_fraction"]) for row in expected_rows), Fraction(0)) ==
             fraction(source["parent_volume_fraction"]), "numeric DFS/trie/prefix/Kraft")
        expected_aggregate = [aggregate_leaf(row) for row in expected_rows]
        for expected in expected_aggregate:
            try:
                observed = next(aggregate_rows)
            except StopIteration as error:
                raise Reject("aggregate leaves ended early") from error
            need(strict_keys(observed, AGG_LEAF_KEYS, "aggregate leaf") == expected,
                 "aggregate leaf exact independent numeric replay")
            replacements[expected["pair_index"]].append(expected)
            disposition_total[expected["disposition"]] += 1
            raw_total[expected["route_classification"]] += 1
            leaf_total += 1
        counts = Counter(row["disposition"] for row in expected_rows)
        source_body = {
            "schema": AGG_SCHEMA + ".aggregate-source-row", "source_inventory_ordinal": ordinal,
            "source_assignment_row_sha256": assignment_row["row_sha256"],
            "assignment_preimage_sha256": assignment_row["assignment_preimage_sha256"],
            "source_C61_aggregate_leaf_row_sha256": source["row_sha256"],
            "source_C61_shard_row_sha256": source["source_shard_row_sha256"],
            "source_handoff_ordinal": source["source_handoff_ordinal"],
            "source_path": source["path"], "pair_index": source["pair_index"],
            "source_C65_shard_id": assignment_row["shard_id"],
            "output_leaf_count": len(expected_rows),
            "strict_terminal_leaf_count": counts["STRICT_TERMINAL"],
            "collision3_ready_leaf_count": counts["COLLISION3_READY"],
            "collision2_handoff_leaf_count": counts["COLLISION2_HANDOFF"],
            "route_evaluation_count": source_routes,
            "source_shard_output_row_hash_line_sequence_sha256": hashlib.sha256(
                "".join(row["row_sha256"] + "\n" for row in expected_rows).encode("ascii")
            ).hexdigest(),
            "aggregate_output_row_hash_line_sequence_sha256": hashlib.sha256(
                "".join(row["row_sha256"] + "\n" for row in expected_aggregate).encode("ascii")
            ).hexdigest(),
            "path_prefix_free": True, "source_Kraft_conservation": source["parent_volume_fraction"],
            "whole_source_terminal": counts["STRICT_TERMINAL"] == len(expected_rows),
            "whole_source_terminal_or_C3_ready": counts["COLLISION2_HANDOFF"] == 0,
            "formal_credit": 0, "whole_parent_credit": 0, "D02_gate_credit": 0,
        }
        expected_source = {**source_body, "row_sha256": digest(source_body)}
        try:
            observed_source = next(source_rows)
        except StopIteration as error:
            raise Reject("aggregate source rows ended early") from error
        need(strict_keys(observed_source, AGG_SOURCE_KEYS, "aggregate source") == expected_source,
             "aggregate source exact independent numeric replay")
        group = structural[source["row_sha256"]]
        need(group["rows"] == expected_rows and group["aggregate_rows"] == expected_aggregate and
             group["trie_route_evaluations"] == source_routes and
             group["row_sequence"] ==
             expected_source["source_shard_output_row_hash_line_sequence_sha256"] and
             group["aggregate_sequence"] ==
             expected_source["aggregate_output_row_hash_line_sequence_sha256"],
             "shard rows equal independent numeric replay")
        whole_terminal += int(expected_source["whole_source_terminal"])
        whole_terminal_or_c3 += int(expected_source["whole_source_terminal_or_C3_ready"])
    for iterator, label in ((aggregate_rows, "aggregate leaves"), (source_rows, "source summaries")):
        try:
            next(iterator)
        except StopIteration:
            pass
        else:
            raise Reject(label + ": trailing rows")
    return (replacements, {key: disposition_total[key] for key in DISPOSITIONS},
            dict(sorted(raw_total.items())), route_total, leaf_total,
            whole_terminal, whole_terminal_or_c3)


def expected_parent_rows(base_parents: list[dict[str, Any]],
                         carried: dict[int, list[dict[str, Any]]],
                         selected: list[dict[str, Any]],
                         replacements: dict[int, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    selected_count = Counter(row["pair_index"] for row in selected)
    result: list[dict[str, Any]] = []
    for pair, base in zip(PAIRS, base_parents, strict=True):
        ledger_carry = carried[pair]
        children = replacements[pair]
        child_census = Counter(row["disposition"] for row in children)
        earlier_carry = base["strict_terminal_leaf_count"] - len(ledger_carry)
        need(base["pair_index"] == pair and base["path_prefix_free"] is True and
             base["parent_Kraft_conservation"] == "1" and
             base["collision3_ready_leaf_count"] == 0 and
             base["collision2_handoff_leaf_count"] == selected_count[pair] and
             earlier_carry >= 0, "parent full-base replacement certificate")
        body = {
            "schema": AGG_SCHEMA + ".aggregate-parent-row", "pair_index": pair,
            "C61_full_base_parent_row_sha256": base["row_sha256"],
            "C61_full_base_combined_leaf_count": base["combined_leaf_count"],
            "C61_full_base_strict_terminal_leaf_count": base["strict_terminal_leaf_count"],
            "C61_full_base_collision3_ready_leaf_count": base["collision3_ready_leaf_count"],
            "C61_full_base_collision2_sources_replaced": base["collision2_handoff_leaf_count"],
            "C61_aggregate_ledger_strict_terminal_leaf_count": len(ledger_carry),
            "C57_C58_earlier_terminal_carry_leaf_count": earlier_carry,
            "C65_replacement_leaf_count": len(children),
            "combined_leaf_count": base["strict_terminal_leaf_count"] + len(children),
            "strict_terminal_leaf_count": base["strict_terminal_leaf_count"] +
                                          child_census["STRICT_TERMINAL"],
            "collision3_ready_leaf_count": child_census["COLLISION3_READY"],
            "collision2_handoff_leaf_count": child_census["COLLISION2_HANDOFF"],
            "path_prefix_free": True, "parent_Kraft_conservation": "1",
            "parent_prefix_Kraft_preserved_by_base_certificate_and_exact_source_partitions": True,
            "whole_pair_terminal": child_census["COLLISION3_READY"] ==
                                   child_census["COLLISION2_HANDOFF"] == 0,
            "whole_pair_terminal_or_C3_ready": child_census["COLLISION2_HANDOFF"] == 0,
            "formal_credit": 0, "whole_parent_credit": 0, "D02_gate_credit": 0,
        }
        result.append({**body, "row_sha256": digest(body)})
    need(len(result) == 12 and
         sum(row["C61_full_base_combined_leaf_count"] for row in result) == C61_FULL_BASE_LEAVES and
         sum(row["C61_full_base_strict_terminal_leaf_count"] for row in result) ==
         C61_FULL_BASE_TERMINAL and
         sum(row["C61_full_base_collision2_sources_replaced"] for row in result) == C61_FULL_BASE_C2 and
         sum(row["C61_aggregate_ledger_strict_terminal_leaf_count"] for row in result) ==
         C61_LEDGER_TERMINAL and
         sum(row["C57_C58_earlier_terminal_carry_leaf_count"] for row in result) ==
         C61_EARLIER_TERMINAL_CARRY and
         sum(row["C65_replacement_leaf_count"] for row in result) == EXPECTED_REPLACEMENT_LEAVES and
         sum(row["combined_leaf_count"] for row in result) == EXPECTED_COMPLETE_LEAVES and
         sum(row["strict_terminal_leaf_count"] for row in result) == EXPECTED_COMPLETE_TERMINAL and
         sum(row["collision3_ready_leaf_count"] for row in result) == EXPECTED_REPLACEMENT_C3 and
         sum(row["collision2_handoff_leaf_count"] for row in result) == EXPECTED_REPLACEMENT_C2,
         "12 parent full replacement exact census")
    return result


def receipt_vector(snapshot: Mapping[Path, Captured],
                   receipts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    vector: list[dict[str, Any]] = []
    for shard, value in zip(SHARDS, receipts, strict=True):
        vector.append({
            "shard_id": shard, "receipt_filename": receipt_path(shard).name,
            "receipt_file_sha256": hashlib.sha256(snap_raw(snapshot, receipt_path(shard))).hexdigest(),
            "receipt_object_sha256": value["object_sha256"],
            "assigned_input_count": value["assigned_input_count"],
            "route_evaluation_count": value["route_evaluation_count"],
            "output_ledger": copy.deepcopy(value["output_ledger"]),
        })
    return vector


def exact_aggregate_result(aggregate: dict[str, Any], snapshot: Mapping[Path, Captured],
                           program: dict[str, Any], authority: dict[str, str],
                           assignment: dict[str, Any], c61: dict[str, Any],
                           receipts: list[dict[str, Any]], descriptors: tuple[dict[str, Any], ...],
                           disposition: dict[str, int], raw_census: dict[str, int], routes: int,
                           leaves: int, whole_terminal: int,
                           whole_terminal_or_c3: int) -> None:
    leaf_desc, source_desc, parent_desc = descriptors
    expected_program = {
        "executor_file_sha256": PIN["executor_file"],
        "controller_file_sha256": PIN["controller_file"],
        "checker_file_sha256": PIN["checker_file"],
        "consumed_as_pinned_inert_bytes_and_AST_only": True,
        "imported": False, "executed": False,
    }
    expected_body = {
        "schema": AGG_SCHEMA + ".aggregate-result", "status": AGG_STATUS,
        "producer_file_sha256": program["aggregate_producer_file_sha256"],
        "producer_independence": expected_program,
        "frozen_inputs": {
            "contract_file_sha256": PIN["contract_file"],
            "contract_object_sha256": PIN["contract_object"],
            "assignment_result_file_sha256": PIN["assignment_file"],
            "assignment_result_object_sha256": PIN["assignment_object"],
            "assignment_inventory_file_sha256": PIN["inventory_file"],
            "authorization_file_sha256": PIN["authorization_file"],
            "authorization_object_sha256": PIN["authorization_object"],
            "C61_result_file_sha256": PIN["C61_result_file"],
            "C61_result_object_sha256": PIN["C61_result_object"],
            "C61_leaf_ledger_file_sha256": PIN["C61_leaf_file"],
            "C61_full_parent_summary_file_sha256": PIN["C61_parent_file"],
            "C61_full_parent_summary_descriptor": copy.deepcopy(
                c61["ledgers"]["parent_summaries"]),
            "assignment_ordered_preimage_sha256_line_sequence_sha256":
                assignment["ordered_preimage_sha256_line_sequence_sha256"],
            "post_seal_effective_checkpoint_object_sha256": PIN["effective_checkpoint_object"],
            "C69b_consumed": False, "C69c_consumed": False,
        },
        "authority_snapshot": {
            "files": authority, "object_sha256": PIN["authority_snapshot_object"],
            "post_seal_effective_checkpoint_object_sha256": PIN["effective_checkpoint_object"],
        },
        "shard_receipts": receipt_vector(snapshot, receipts),
        "coverage": {
            "input_C61_selected_collision2_sources": 20_879, "shard_receipt_count": 64,
            "assignment_complete": True, "assignment_mutually_exclusive": True,
            "route_evaluation_count": routes, "replacement_output_leaf_count": leaves,
            "replacement_disposition_census": disposition,
            "raw_classification_census": raw_census,
            "whole_sources_terminal": whole_terminal,
            "whole_sources_terminal_or_C3_ready": whole_terminal_or_c3,
            "C61_aggregate_leaf_ledger_strict_terminal_leaves": C61_LEDGER_TERMINAL,
            "C57_C58_earlier_terminal_carry_leaves": C61_EARLIER_TERMINAL_CARRY,
            "C61_full_base_strict_terminal_leaves": C61_FULL_BASE_TERMINAL,
            "C61_full_base_collision2_sources_replaced": C61_FULL_BASE_C2,
            "C61_full_base_leaf_count": C61_FULL_BASE_LEAVES,
            "complete_parent_leaf_count": EXPECTED_COMPLETE_LEAVES,
            "complete_parent_disposition_census": {
                "STRICT_TERMINAL": EXPECTED_COMPLETE_TERMINAL,
                "COLLISION3_READY": EXPECTED_REPLACEMENT_C3,
                "COLLISION2_HANDOFF": EXPECTED_REPLACEMENT_C2,
            },
            "parent_count": 12,
        },
        "ledgers": {"aggregate_leaves": leaf_desc, "source_summaries": source_desc,
                    "parent_summaries": parent_desc},
        "invariants": {
            "receipt_ids_exactly_00_through_63_before_any_ledger_open": True,
            "controller_exited_before_any_receipt_or_ledger_open": True,
            "all_frozen_inputs_single_snapshot_TOCTOU_checked": True,
            "all_64_receipt_and_ledger_descriptors_closed": True,
            "all_20879_assignment_sources_unique_and_exactly_once": True,
            "assignment_formula_and_global_per_shard_sequences_rebuilt": True,
            "all_shard_rows_and_continuation_objects_self_hash_closed": True,
            "all_20879_source_partitions_prefix_free_and_Kraft_conserved": True,
            "C61_full_parent_summary_descriptor_rows_and_object_closure_pinned": True,
            "C57_C58_earlier_terminal_carry_preserved": True,
            "C61_selected_collision2_parents_removed_before_children_inserted": True,
            "C61_parent_and_C65_children_not_double_counted": True,
            "all_12_replacement_parents_preserve_prefix_Kraft_via_C61_base_certificate_and_exact_source_partitions": True,
            "two_isolated_staging_builds_byte_identical": True,
            "gzip_descriptors_computed_after_close_and_reopen": True,
            "publication_no_replace_O_EXCL_O_NOFOLLOW_and_fsync": True,
            "C69b_or_C69c_capability_injected": False,
            "numeric_routes_independently_recomputed_by_this_aggregate_producer": False,
            "post_publication_no_producer_cold_numeric_replay_required": True,
            "partial_statistics_used_for_credit": False,
        },
        "candidate_is_authority": False, "formal_credit": 0, "whole_parent_credit": 0,
        "D02_gate_credit": 0, "runtime_canonical_pointer_or_seal_writes": False,
    }
    body = copy.deepcopy(aggregate)
    claim = body.pop("object_sha256")
    need(strict_keys(aggregate, AGG_RESULT_KEYS, "aggregate result") and
         body == expected_body and claim == digest(expected_body),
         "aggregate result exact complete C61-base projection")


PROJECTION_KEYS = {
    "schema", "status", "aggregate", "coverage", "frozen_snapshot", "independence",
    "rejections", "runtime_identity", "invariants", "candidate_is_authority",
    "formal_credit", "whole_parent_credit", "D02_gate_credit",
    "runtime_canonical_pointer_or_seal_writes", "object_sha256",
}
FROZEN_RECORD_KEYS = {
    "logical_name", "relative_path", "sha256", "size", "identity", "parent_identity",
}
SEED_RECEIPT_KEYS = {
    "schema", "status", "seed", "launcher", "worker", "challenge_sha256",
    "verifier_file_sha256", "frozen_input_object_sha256", "projection_filename",
    "projection_file_sha256", "projection_object_sha256", "projection_published_before_receipt",
    "candidate_is_authority", "formal_credit", "whole_parent_credit", "D02_gate_credit",
    "runtime_canonical_pointer_or_seal_writes", "object_sha256",
}
COMPLETION_RECEIPT_KEYS = {
    "schema", "status", "phase", "process", "verifier_file_sha256", "result_filename",
    "result_file_sha256", "result_object_sha256", "result_published_before_receipt",
    "frozen_input_object_sha256", "candidate_is_authority", "formal_credit",
    "whole_parent_credit", "D02_gate_credit", "runtime_canonical_pointer_or_seal_writes",
    "object_sha256",
}


def stable_runtime_projection(runtime: dict[str, Any], process: dict[str, Any],
                              metadata: dict[str, Any]) -> dict[str, Any]:
    return {
        "python_executable_path": process["executable_path"],
        "python_executable_dev": process["executable_dev"],
        "python_executable_inode": process["executable_inode"],
        "python_executable_size": process["executable_size"],
        "python_executable_mtime_ns": process["executable_mtime_ns"],
        "python_executable_sha256": process["executable_sha256"],
        "controller_source_identity": runtime["controller_source_identity"],
        "executor_source_identity": runtime["executor_source_identity"],
        "checker_source_identity": runtime["checker_source_identity"],
        "sealed_runtime": metadata["runtime_descriptor"],
        "sealed_python_link": metadata["runtime_link"],
        "flint_context": {
            "python_flint_version": "0.9.0", "flint_version": "3.6.0",
            "prec": 384, "dps": 115, "cap": 10, "threads": 1,
            "pretty": True, "unicode": False,
        },
    }


def verify_once() -> dict[str, Any]:
    snapshot, metadata = formal_snapshot()
    (_contract, assignment, authorization, c61, c58, _c40,
     base_parents) = validate_frozen_objects(snapshot)
    aggregate = closed_json(snap_raw(snapshot, AGG_RESULT), "aggregate result",
                            PIN["aggregate_result_file"], PIN["aggregate_result_object"])
    strict_keys(aggregate, AGG_RESULT_KEYS, "aggregate result")
    need(aggregate["schema"] == AGG_SCHEMA + ".aggregate-result" and
         aggregate["status"] == AGG_STATUS, "aggregate result schema/status")
    descriptors = aggregate_descriptors(aggregate)
    need(descriptors[0]["sha256"] == PIN["aggregate_leaves_file"] and
         descriptors[1]["sha256"] == PIN["aggregate_sources_file"] and
         descriptors[2]["sha256"] == PIN["aggregate_parents_file"],
         "aggregate exact published ledger pins")
    authority = authority_snapshot(snapshot)
    rejections = validate_rejections(snapshot)
    program = program_independence(snapshot, aggregate)
    selected, inventory, c58_by_hash, carried, by_shard = load_source_universe(
        snapshot, assignment, authorization, c61, c58)
    receipts, structural, receipt_disposition, receipt_raw, receipt_routes = (
        validate_receipts_and_ledgers(snapshot, by_shard, authority)
    )
    leaves_desc, sources_desc, parents_desc = descriptors
    aggregate_rows = iter_gzip(snap_raw(snapshot, AGG_LEAVES), leaves_desc,
                               "aggregate leaves", MAX_EXPANDED)
    source_rows = iter_gzip(snap_raw(snapshot, AGG_SOURCES), sources_desc,
                            "aggregate sources", 512 << 20)
    runtime_before = metadata["runtime"]
    with tempfile.TemporaryDirectory(prefix="cm2-c65-cold-v4-frozen-") as temporary:
        frozen_root = Path(temporary).resolve()
        materialize_snapshot(snapshot, frozen_root)
        validate_mirror(snapshot, frozen_root)
        try:
            with frozen_working_directory(frozen_root):
                with live_root_open_guard():
                    with authenticated_kernel(snapshot, metadata, frozen_root) as kernel:
                        (replacements, numeric_disposition, numeric_raw, numeric_routes, leaf_count,
                         whole_terminal, whole_terminal_or_c3) = independent_numeric_replay(
                            kernel, frozen_root, selected, inventory, c58_by_hash, structural,
                            aggregate_rows, source_rows)
            validate_mirror(snapshot, frozen_root)
        finally:
            thaw_mirror_for_cleanup(frozen_root)
    need(numeric_disposition == receipt_disposition and numeric_raw == receipt_raw and
         numeric_routes == receipt_routes and leaf_count == leaves_desc["row_count"] and
         numeric_disposition == {
             "STRICT_TERMINAL": EXPECTED_REPLACEMENT_TERMINAL,
             "COLLISION3_READY": EXPECTED_REPLACEMENT_C3,
             "COLLISION2_HANDOFF": EXPECTED_REPLACEMENT_C2,
         } and leaf_count == EXPECTED_REPLACEMENT_LEAVES,
         "independent numeric replay/receipt/frozen census equality")
    parents = expected_parent_rows(base_parents, carried, selected, replacements)
    observed_parents = iter_gzip(snap_raw(snapshot, AGG_PARENTS), parents_desc,
                                 "aggregate parents", 8 << 20)
    for expected in parents:
        try:
            observed = next(observed_parents)
        except StopIteration as error:
            raise Reject("aggregate parents ended early") from error
        need(strict_keys(observed, AGG_PARENT_KEYS, "aggregate parent") == expected,
             "aggregate parent exact full-base replacement")
    try:
        next(observed_parents)
    except StopIteration:
        pass
    else:
        raise Reject("aggregate parent trailing row")
    exact_aggregate_result(
        aggregate, snapshot, program, authority, assignment, c61, receipts, descriptors,
        numeric_disposition, numeric_raw, numeric_routes, leaf_count,
        whole_terminal, whole_terminal_or_c3)

    # Long-run recapture: all live authority, numerical source, aggregate,
    # receipt, and executable/program identities must still be exactly frozen.
    names_after = shard_name_barrier()
    need(names_after == tuple(tuple(values) for values in metadata["shard_names"]),
         "shard names stable after long replay")
    runtime_after = runtime_barrier()
    stable_runtime(runtime_before, runtime_after, "post-numeric replay")
    recaptured = capture_bounded(tuple(snapshot))
    compare_recapture(snapshot, recaptured, "post-numeric full frozen recapture")
    need(metadata["runtime_link"] == runtime_link_record(),
         "post-numeric sealed-python symlink identity stable")
    stable_runtime(runtime_after, runtime_barrier(), "post-recapture")

    parent_terminal = sum(int(row["whole_pair_terminal"]) for row in parents)
    frozen_vector = snapshot_vector(snapshot)
    return close({
        "schema": SCHEMA + ".cold-projection",
        "status": (
            "PASS_COMPLETE_C65_AGGREGATE_COLD_NUMERIC_REPLAY_V4__64_OF_64__"
            "20879_ASSIGNMENTS__C61_FULL_BASE_REPLACEMENT__ZERO_CREDIT"
        ),
        "aggregate": {
            "result_file_sha256": hashlib.sha256(snap_raw(snapshot, AGG_RESULT)).hexdigest(),
            "result_object_sha256": aggregate["object_sha256"],
            "leaf_ledger_sha256": leaves_desc["sha256"],
            "source_summary_sha256": sources_desc["sha256"],
            "parent_summary_sha256": parents_desc["sha256"],
            "producer_file_sha256": program["aggregate_producer_file_sha256"],
        },
        "coverage": {
            "shard_receipts": 64, "assigned_sources": 20_879,
            "numeric_route_evaluations": numeric_routes,
            "replacement_leaf_count": leaf_count,
            "replacement_disposition_census": numeric_disposition,
            "C61_full_base_leaf_count": C61_FULL_BASE_LEAVES,
            "C61_full_base_terminal_count": C61_FULL_BASE_TERMINAL,
            "C61_full_base_collision2_sources_replaced": C61_FULL_BASE_C2,
            "complete_parent_leaf_count": EXPECTED_COMPLETE_LEAVES,
            "complete_parent_disposition_census": {
                "STRICT_TERMINAL": EXPECTED_COMPLETE_TERMINAL,
                "COLLISION3_READY": EXPECTED_REPLACEMENT_C3,
                "COLLISION2_HANDOFF": EXPECTED_REPLACEMENT_C2,
            },
            "whole_sources_terminal": whole_terminal,
            "whole_sources_terminal_or_C3_ready": whole_terminal_or_c3,
            "whole_pairs_terminal": parent_terminal,
        },
        "frozen_snapshot": {
            "ordered_input_count": len(frozen_vector),
            "ordered_input_vector": frozen_vector,
            "object_sha256": metadata["frozen_input_object_sha256"],
            "numeric_source_closure_count": PIN["numeric_source_closure_count"],
            "numeric_source_closure_object_sha256": PIN["numeric_source_closure_object"],
            "numeric_authority_file_count": metadata["numeric_authority_file_count"],
            "numeric_authority_directory_count": PIN["authority_directory_count"],
            "numeric_authority_reference_edge_count": PIN["authority_edge_count"],
            "numeric_authority_closure_object_sha256": PIN["authority_closure_object"],
            "sealed_runtime_member_count":
                metadata["runtime_descriptor"]["attested_distribution_member_count"],
        },
        "independence": program, "rejections": rejections,
        "runtime_identity": stable_runtime_projection(
            runtime_before, executable_identity(os.getpid()), metadata),
        "invariants": {
            "malformed_candidate_names_rejected_before_ledger_derivation": True,
            "controller_and_executable_identity_stable_before_after_and_long_run": True,
            "all_live_authority_in_one_bounded_frozen_snapshot": True,
            "all_frozen_inputs_identity_and_bytes_recaptured_after_long_run": True,
            "pretty_contract_exact_file_and_object_accepted_without_compact_reencoding": True,
            "no_pyc_or_preexisting_local_sys_modules_consumed": True,
            "complete_transitive_numeric_source_closure_controlled_loader": True,
            "numeric_runtime_reads_private_frozen_mirror_not_live_authority": True,
            "all_receipt_fields_exact_and_all_shard_routes_rebuilt_from_tries": True,
            "all_20879_depth6_numeric_DFS_rows_recomputed": True,
            "C61_parent_summary_v4_full_baseline_48287_27408_20879": True,
            "complete_replacement_386327_219072_167255_0": True,
            "C69b_or_C69c_consumed": False,
            "authority_9dir_80file_37edge_closure_replayed": True,
            "sealed_python_flint_runtime_and_384bit_context_replayed": True,
            "held_self_fd_and_strict_worker_environment": True,
            "read_only_private_mirror_and_live_root_open_guard": True,
        },
        "candidate_is_authority": False, "formal_credit": 0,
        "whole_parent_credit": 0, "D02_gate_credit": 0,
        "runtime_canonical_pointer_or_seal_writes": False,
    })


def preflight_smoke() -> dict[str, Any]:
    """Exercise the frozen loader and exactly one source without formal output."""
    formal_phase_gate("launch")
    validate_formal_process_runtime()
    handshake = dual_held_script_handshake_smoke()
    snapshot, metadata = formal_snapshot()
    (_contract, assignment, authorization, c61, c58, _c40,
     _base_parents) = validate_frozen_objects(snapshot)
    aggregate = closed_json(snap_raw(snapshot, AGG_RESULT), "preflight aggregate",
                            PIN["aggregate_result_file"], PIN["aggregate_result_object"])
    authority_snapshot(snapshot)
    validate_rejections(snapshot)
    program_independence(snapshot, aggregate)
    selected, inventory, c58_by_hash, _carried, _by_shard = load_source_universe(
        snapshot, assignment, authorization, c61, c58)
    need(len(selected) == len(inventory) == 20_879, "preflight source universe")
    with tempfile.TemporaryDirectory(prefix="cm2-c65-cold-v4-smoke-") as temporary:
        frozen_root = Path(temporary).resolve()
        materialize_snapshot(snapshot, frozen_root)
        validate_mirror(snapshot, frozen_root)
        try:
            with frozen_working_directory(frozen_root):
                with live_root_open_guard():
                    with authenticated_kernel(snapshot, metadata, frozen_root) as kernel:
                        c40_index, c38_index, cells, config = numeric_context(kernel, frozen_root)
                        source, assignment_row = selected[0], inventory[0]
                        c58_source = c58_by_hash[source["source_C58_leaf_row_sha256"]]
                        c40_ordinal, c40_source = c40_index[c58_source["C40_source_row_sha256"]]
                        task = kernel.task_for_source(c40_ordinal, c40_source, c38_index, cells,
                                                      config["source_chart_seams"])
                        assert_flint_context(kernel)
                        route = kernel.independent_route_at_path(task, source["path"], config)
                        assert_flint_context(kernel)
                        need(type(route) is dict and type(route.get("classification")) is str and
                             kernel.disposition_family(route["classification"]) in {
                                 "TERMINAL_EXCLUDED", "COLLISION3_READY", "RESIDUAL_OUTER"},
                             "preflight one-source numeric route")
            validate_mirror(snapshot, frozen_root)
        finally:
            thaw_mirror_for_cleanup(frozen_root)
    recaptured = capture_bounded(tuple(snapshot))
    compare_recapture(snapshot, recaptured, "preflight full frozen recapture")
    return close({
        "schema": SCHEMA + ".preflight-smoke",
        "status": "PASS_FROZEN_SNAPSHOT_KERNEL_LOAD_AND_ONE_SOURCE_SMOKE__NO_FORMAL_OUTPUT",
        "frozen_input_count": len(snapshot),
        "frozen_input_object_sha256": metadata["frozen_input_object_sha256"],
        "authority_directory_count": 9, "authority_file_count": 80,
        "authority_reference_edge_count": 37, "numeric_source_closure_count": 51,
        "runtime_attested_member_count": 139, "runtime_safe_mirror_member_count": 98,
        "dual_held_script_handshake": handshake,
        "smoked_source_C61_aggregate_leaf_row_sha256": selected[0]["row_sha256"],
        "smoked_assignment_preimage_sha256": inventory[0]["assignment_preimage_sha256"],
        "formal_outputs_written": False, "candidate_is_authority": False,
        "formal_credit": 0, "whole_parent_credit": 0, "D02_gate_credit": 0,
        "runtime_canonical_pointer_or_seal_writes": False,
    })


def validate_frozen_vector(value: Any, label: str) -> list[dict[str, Any]]:
    need(type(value) is list and value, label + ": nonempty vector")
    aliases: list[str] = []
    relative_paths: list[str] = []
    for row in value:
        strict_keys(row, FROZEN_RECORD_KEYS, label + ":record")
        need(type(row["logical_name"]) is str and row["logical_name"] and
             type(row["relative_path"]) is str and row["relative_path"] and
             HEX64.fullmatch(str(row["sha256"])) is not None and
             type(row["size"]) is int and row["size"] >= 0 and
             type(row["identity"]) is list and len(row["identity"]) == 7 and
             type(row["parent_identity"]) is list and len(row["parent_identity"]) == 7 and
             all(type(item) is int for item in (*row["identity"], *row["parent_identity"])),
             label + ": record exact types")
        aliases.append(row["logical_name"])
        relative_paths.append(row["relative_path"])
    need(len(aliases) == len(set(aliases)) and
         len(relative_paths) == len(set(relative_paths)), label + ": vector uniqueness")
    return value


def validate_projection(value: dict[str, Any], raw: bytes | None = None,
                        expected_self_sha: str | None = None) -> dict[str, Any]:
    strict_keys(value, PROJECTION_KEYS, "projection")
    need(value["schema"] == SCHEMA + ".cold-projection" and
         value["status"] ==
         "PASS_COMPLETE_C65_AGGREGATE_COLD_NUMERIC_REPLAY_V4__64_OF_64__20879_ASSIGNMENTS__C61_FULL_BASE_REPLACEMENT__ZERO_CREDIT" and
         value["candidate_is_authority"] is False and
         value["runtime_canonical_pointer_or_seal_writes"] is False,
         "projection exact schema/status/boundary")
    zero_credit(value, "projection")
    aggregate = strict_keys(value["aggregate"], {
        "result_file_sha256", "result_object_sha256", "leaf_ledger_sha256",
        "source_summary_sha256", "parent_summary_sha256", "producer_file_sha256",
    }, "projection aggregate")
    need(aggregate == {
        "result_file_sha256": PIN["aggregate_result_file"],
        "result_object_sha256": PIN["aggregate_result_object"],
        "leaf_ledger_sha256": PIN["aggregate_leaves_file"],
        "source_summary_sha256": PIN["aggregate_sources_file"],
        "parent_summary_sha256": PIN["aggregate_parents_file"],
        "producer_file_sha256": PIN["producer_file"],
    }, "projection exact aggregate pins")
    coverage = strict_keys(value["coverage"], {
        "shard_receipts", "assigned_sources", "numeric_route_evaluations",
        "replacement_leaf_count", "replacement_disposition_census",
        "C61_full_base_leaf_count", "C61_full_base_terminal_count",
        "C61_full_base_collision2_sources_replaced", "complete_parent_leaf_count",
        "complete_parent_disposition_census", "whole_sources_terminal",
        "whole_sources_terminal_or_C3_ready", "whole_pairs_terminal",
    }, "projection coverage")
    exact_int(coverage["shard_receipts"], 64, "projection receipts")
    exact_int(coverage["assigned_sources"], 20_879, "projection sources")
    exact_int(coverage["replacement_leaf_count"], EXPECTED_REPLACEMENT_LEAVES,
              "projection replacement leaves")
    exact_int(coverage["C61_full_base_leaf_count"], C61_FULL_BASE_LEAVES,
              "projection C61 leaves")
    exact_int(coverage["C61_full_base_terminal_count"], C61_FULL_BASE_TERMINAL,
              "projection C61 terminal")
    exact_int(coverage["C61_full_base_collision2_sources_replaced"], C61_FULL_BASE_C2,
              "projection C61 c2")
    exact_int(coverage["complete_parent_leaf_count"], EXPECTED_COMPLETE_LEAVES,
              "projection complete leaves")
    need(coverage["replacement_disposition_census"] == {
        "STRICT_TERMINAL": EXPECTED_REPLACEMENT_TERMINAL,
        "COLLISION3_READY": EXPECTED_REPLACEMENT_C3,
        "COLLISION2_HANDOFF": EXPECTED_REPLACEMENT_C2,
    } and coverage["complete_parent_disposition_census"] == {
        "STRICT_TERMINAL": EXPECTED_COMPLETE_TERMINAL,
        "COLLISION3_READY": EXPECTED_REPLACEMENT_C3,
        "COLLISION2_HANDOFF": EXPECTED_REPLACEMENT_C2,
    }, "projection exact replacement/complete census")
    exact_int(coverage["numeric_route_evaluations"], 696_959, "projection routes")
    exact_int(coverage["whole_sources_terminal"], 2_943, "projection whole terminal sources")
    exact_int(coverage["whole_sources_terminal_or_C3_ready"], 2_943,
              "projection whole terminal-or-C3 sources")
    exact_int(coverage["whole_pairs_terminal"], 0, "projection whole terminal pairs")
    frozen = strict_keys(value["frozen_snapshot"], {
        "ordered_input_count", "ordered_input_vector", "object_sha256",
        "numeric_source_closure_count", "numeric_source_closure_object_sha256",
        "numeric_authority_file_count", "numeric_authority_directory_count",
        "numeric_authority_reference_edge_count", "numeric_authority_closure_object_sha256",
        "sealed_runtime_member_count",
    }, "projection frozen snapshot")
    vector = validate_frozen_vector(frozen["ordered_input_vector"], "projection frozen vector")
    exact_int(frozen["ordered_input_count"], len(vector), "projection input count")
    exact_int(frozen["numeric_source_closure_count"], PIN["numeric_source_closure_count"],
              "projection source closure count")
    exact_int(frozen["numeric_authority_file_count"], 80,
              "projection numeric authority count")
    exact_int(frozen["numeric_authority_directory_count"], 9,
              "projection numeric authority directory count")
    exact_int(frozen["numeric_authority_reference_edge_count"], 37,
              "projection numeric authority edge count")
    exact_int(frozen["sealed_runtime_member_count"], 139,
              "projection sealed runtime member count")
    need(frozen["numeric_authority_closure_object_sha256"] == PIN["authority_closure_object"] and
         frozen["numeric_source_closure_object_sha256"] ==
         PIN["numeric_source_closure_object"] and
         frozen["object_sha256"] == digest({"ordered_frozen_inputs": vector}),
         "projection frozen vector closure")
    self_rows = [row for row in vector if row["relative_path"] == str(SELF.relative_to(ROOT))]
    need(len(self_rows) == 1, "projection frozen verifier singleton")
    independence = strict_keys(value["independence"], {
        "executor_file_sha256", "controller_file_sha256", "checker_file_sha256",
        "aggregate_producer_file_sha256", "cold_verifier_file_sha256",
        "numeric_source_closure_object_sha256", "numeric_source_closure_count",
        "C65_programs_consumed_as_authenticated_inert_bytes_or_AST_only",
        "C65_programs_imported_or_executed",
        "numeric_kernel_loaded_only_from_captured_source_bytes",
        "pyc_or_preexisting_local_sys_modules_consumed",
    }, "projection independence")
    need(independence["executor_file_sha256"] == PIN["executor_file"] and
         independence["controller_file_sha256"] == PIN["controller_file"] and
         independence["checker_file_sha256"] == PIN["checker_file"] and
         independence["aggregate_producer_file_sha256"] == PIN["producer_file"] and
         independence["cold_verifier_file_sha256"] == self_rows[0]["sha256"] and
         (expected_self_sha is None or
          independence["cold_verifier_file_sha256"] == expected_self_sha) and
         independence["numeric_source_closure_object_sha256"] ==
         PIN["numeric_source_closure_object"] and
         independence["numeric_source_closure_count"] == PIN["numeric_source_closure_count"] and
         independence["C65_programs_consumed_as_authenticated_inert_bytes_or_AST_only"] is True and
         independence["C65_programs_imported_or_executed"] is False and
         independence["numeric_kernel_loaded_only_from_captured_source_bytes"] is True and
         independence["pyc_or_preexisting_local_sys_modules_consumed"] is False,
         "projection exact independence")
    rejections = strict_keys(value["rejections"], {
        "v1_rejection_filename", "v1_rejection_file_sha256",
        "rejected_v1_selftest_file_sha256", "rejected_v1_selftest_object_sha256",
        "v2_rejection_filename", "v2_rejection_file_sha256",
        "rejected_v2_verifier_file_sha256",
        "v3_rejection_filename", "v3_rejection_file_sha256",
        "rejected_v3_verifier_file_sha256",
        "producer_contract_rejection_file_sha256", "producer_parent_rejection_file_sha256",
        "rejected_producer_bytes_consumed", "rejected_v1_verifier_or_selftest_consumed",
        "rejected_v2_verifier_or_outputs_consumed", "rejected_v3_verifier_or_outputs_consumed",
    }, "projection rejections")
    need(rejections["v1_rejection_filename"] == V1_REJECTION.name and
         rejections["v1_rejection_file_sha256"] == PIN["v1_rejection_file"] and
         rejections["rejected_v1_selftest_file_sha256"] == PIN["rejected_v1_selftest_file"] and
         rejections["rejected_v1_selftest_object_sha256"] ==
         PIN["rejected_v1_selftest_object"] and
         rejections["v2_rejection_filename"] == V2_REJECTION.name and
         rejections["v2_rejection_file_sha256"] == PIN["v2_rejection_file"] and
         rejections["rejected_v2_verifier_file_sha256"] ==
         PIN["rejected_v2_verifier_file"] and
         rejections["v3_rejection_filename"] == V3_REJECTION.name and
         rejections["v3_rejection_file_sha256"] == PIN["v3_rejection_file"] and
         rejections["rejected_v3_verifier_file_sha256"] ==
         PIN["rejected_v3_verifier_file"] and
         rejections["producer_contract_rejection_file_sha256"] ==
         PIN["producer_contract_rejection_file"] and
         rejections["producer_parent_rejection_file_sha256"] ==
         PIN["producer_parent_rejection_file"] and
         rejections["rejected_producer_bytes_consumed"] is False and
         rejections["rejected_v1_verifier_or_selftest_consumed"] is False and
         rejections["rejected_v2_verifier_or_outputs_consumed"] is False and
         rejections["rejected_v3_verifier_or_outputs_consumed"] is False,
         "projection exact v1/v2/v3 rejection")
    runtime = strict_keys(value["runtime_identity"], {
        "python_executable_path", "python_executable_dev", "python_executable_inode",
        "python_executable_size", "python_executable_mtime_ns", "python_executable_sha256",
        "controller_source_identity", "executor_source_identity", "checker_source_identity",
        "sealed_runtime", "sealed_python_link", "flint_context",
    }, "projection runtime")
    need(runtime["python_executable_path"] == str(SEALED_PYTHON) and
         runtime["python_executable_sha256"] == PIN["python_file"] and
         all(type(runtime[key]) is int for key in (
             "python_executable_dev", "python_executable_inode", "python_executable_size",
             "python_executable_mtime_ns")) and
         all(type(runtime[key]) is list and len(runtime[key]) == 7 and
             all(type(item) is int for item in runtime[key]) for key in (
                 "controller_source_identity", "executor_source_identity", "checker_source_identity")),
         "projection runtime exact types")
    need(runtime["sealed_runtime"] == {
        "python_sha256": PIN["python_file"], "sys_prefix": str(SEALED_VENV),
        "python_flint_version": "0.9.0", "flint_version": "3.6.0",
        "attestation_sha256": PIN["runtime_attestation_file"],
        "attested_distribution_member_count": 139,
        "safe_mirror_member_count": 98,
        "safe_mirror_record_object_sha256": PIN["safe_runtime_record_object"],
        "safe_mirror_directory_members_object_sha256":
            PIN["safe_runtime_directory_members_object"],
        "runtime_snapshot_path_count": 144,
    } and runtime["flint_context"] == {
        "python_flint_version": "0.9.0", "flint_version": "3.6.0",
        "prec": 384, "dps": 115, "cap": 10, "threads": 1,
        "pretty": True, "unicode": False,
    }, "projection exact sealed runtime/flint context")
    link = strict_keys(runtime["sealed_python_link"], {
        "path", "target", "identity", "parent_identity",
    }, "projection sealed python link")
    need(link["path"] == str(SEALED_PYTHON_LINK.relative_to(ROOT)) and
         link["target"] == "python3" and
         all(type(link[key]) is list and len(link[key]) == 7 and
             all(type(item) is int for item in link[key])
             for key in ("identity", "parent_identity")),
         "projection exact sealed python link")
    invariants = value["invariants"]
    need(type(invariants) is dict and len(invariants) == 17 and
         set(invariants) == {
             "malformed_candidate_names_rejected_before_ledger_derivation",
             "controller_and_executable_identity_stable_before_after_and_long_run",
             "all_live_authority_in_one_bounded_frozen_snapshot",
             "all_frozen_inputs_identity_and_bytes_recaptured_after_long_run",
             "pretty_contract_exact_file_and_object_accepted_without_compact_reencoding",
             "no_pyc_or_preexisting_local_sys_modules_consumed",
             "complete_transitive_numeric_source_closure_controlled_loader",
             "numeric_runtime_reads_private_frozen_mirror_not_live_authority",
             "all_receipt_fields_exact_and_all_shard_routes_rebuilt_from_tries",
             "all_20879_depth6_numeric_DFS_rows_recomputed",
             "C61_parent_summary_v4_full_baseline_48287_27408_20879",
             "complete_replacement_386327_219072_167255_0",
             "C69b_or_C69c_consumed",
             "authority_9dir_80file_37edge_closure_replayed",
             "sealed_python_flint_runtime_and_384bit_context_replayed",
             "held_self_fd_and_strict_worker_environment",
             "read_only_private_mirror_and_live_root_open_guard",
         } and all(value is True for key, value in invariants.items()
                   if key != "C69b_or_C69c_consumed") and
         invariants["C69b_or_C69c_consumed"] is False,
         "projection exact invariant vector")
    body = copy.deepcopy(value)
    claim = body.pop("object_sha256")
    need(claim == digest(body), "projection object closure")
    if raw is not None:
        need(raw == canonical(value) + b"\n", "projection exact canonical bytes")
    return value


def projection_metadata_from_snapshot(snapshot: Mapping[Path, Captured]) -> dict[str, Any]:
    return {
        "runtime_link": runtime_link_record(),
        "runtime_descriptor": validate_runtime_snapshot(snapshot),
    }


def projection_matches_snapshot(projection: dict[str, Any],
                                snapshot: Mapping[Path, Captured],
                                metadata: Mapping[str, Any]) -> None:
    vector = snapshot_vector(snapshot)
    runtime = projection["runtime_identity"]
    python_row = snapshot[SEALED_PYTHON]
    process_expected = {
        "python_executable_dev": python_row.identity[0],
        "python_executable_inode": python_row.identity[1],
        "python_executable_size": python_row.identity[4],
        "python_executable_mtime_ns": python_row.identity[5],
        "python_executable_sha256": hashlib.sha256(python_row.raw).hexdigest(),
    }
    need(projection["frozen_snapshot"]["ordered_input_vector"] == vector and
         projection["frozen_snapshot"]["object_sha256"] == snapshot_object(snapshot) and
         projection["aggregate"]["result_file_sha256"] ==
         hashlib.sha256(snap_raw(snapshot, AGG_RESULT)).hexdigest() and
         projection["aggregate"]["leaf_ledger_sha256"] ==
         hashlib.sha256(snap_raw(snapshot, AGG_LEAVES)).hexdigest() and
         projection["aggregate"]["source_summary_sha256"] ==
         hashlib.sha256(snap_raw(snapshot, AGG_SOURCES)).hexdigest() and
         projection["aggregate"]["parent_summary_sha256"] ==
         hashlib.sha256(snap_raw(snapshot, AGG_PARENTS)).hexdigest() and
         projection["aggregate"]["producer_file_sha256"] ==
         hashlib.sha256(snap_raw(snapshot, PRODUCER)).hexdigest() and
         runtime["python_executable_path"] == str(SEALED_PYTHON) and
         all(runtime[key] == expected for key, expected in process_expected.items()) and
         runtime["controller_source_identity"] == list(snapshot[CONTROLLER].identity) and
         runtime["executor_source_identity"] == list(snapshot[EXECUTOR].identity) and
         runtime["checker_source_identity"] == list(snapshot[CHECKER].identity) and
         runtime["sealed_python_link"] == metadata["runtime_link"] and
         runtime["sealed_runtime"] == metadata["runtime_descriptor"],
         "projection exact current frozen snapshot/hash vector")


def worker_ready(seed: str, challenge: str, expected_self_sha: str,
                 self_capture: Captured) -> dict[str, Any]:
    need(seed in {"1", "2"} and re.fullmatch(r"[0-9a-f]{64}", challenge) is not None,
         "worker seed/challenge")
    parent = int(os.environ.get("C65_COLD_LAUNCHER_PID", "0"))
    need(parent == os.getppid() and parent > 1, "worker launcher parent binding")
    need(HEX64.fullmatch(expected_self_sha) is not None and
         hashlib.sha256(self_capture.raw).hexdigest() == expected_self_sha,
         "worker captured verifier exact launcher SHA")
    return close({
        "schema": SCHEMA + ".worker-ready", "seed": seed,
        "challenge_sha256": hashlib.sha256(bytes.fromhex(challenge)).hexdigest(),
        "process": executable_identity(os.getpid()), "launcher_pid": parent,
        "verifier_file_sha256": expected_self_sha,
    })


def held_self_capture() -> Captured:
    fd = int(os.environ.get("C65_COLD_SELF_FD", "-1"))
    need(fd >= 3 and str(EXECUTED_SELF) == f"/proc/self/fd/{fd}" and
         sys.argv[0] == f"/proc/self/fd/{fd}",
         "held verifier fd is the Python script entry")
    state = os.fstat(fd)
    need(stat.S_ISREG(state.st_mode) and state.st_nlink == 1 and
         fcntl_fd_cloexec(fd) is False, "held verifier fd exact inherited state")
    os.lseek(fd, 0, os.SEEK_SET)
    chunks: list[bytes] = []
    while block := os.read(fd, 1 << 20):
        chunks.append(block)
    raw = b"".join(chunks)
    need(len(raw) == state.st_size and fingerprint(os.fstat(fd)) == fingerprint(state),
         "held verifier exact bytes/identity")
    live = capture_bounded((SELF,), maximum_each=4 << 20, maximum_total=4 << 20)[SELF]
    executed_state = os.stat(EXECUTED_SELF, follow_symlinks=True)
    need(live.identity == fingerprint(state) == fingerprint(executed_state) and
         live.raw == raw and hashlib.sha256(raw).hexdigest() ==
         os.environ.get("C65_COLD_VERIFIER_SHA256"),
         "held/executed/logical verifier identity+bytes+expected SHA")
    return Captured(logical_alias(SELF), SELF, raw, fingerprint(state), live.parent_identity)


def fcntl_fd_cloexec(fd: int) -> bool:
    import fcntl
    return bool(fcntl.fcntl(fd, fcntl.F_GETFD) & fcntl.FD_CLOEXEC)


def held_python_capture() -> Captured:
    fd = int(os.environ.get("C65_COLD_PYTHON_FD", "-1"))
    need(fd >= 3 and fd != int(os.environ.get("C65_COLD_SELF_FD", "-1")),
         "held machine-python fd distinct")
    state = os.fstat(fd)
    need(stat.S_ISREG(state.st_mode) and state.st_nlink == 1 and
         fcntl_fd_cloexec(fd) is False, "held machine-python fd state")
    os.lseek(fd, 0, os.SEEK_SET)
    chunks: list[bytes] = []
    while block := os.read(fd, 1 << 20):
        chunks.append(block)
    raw = b"".join(chunks)
    live = capture_bounded((SEALED_PYTHON,), maximum_each=16 << 20,
                           maximum_total=16 << 20)[SEALED_PYTHON]
    process = executable_identity(os.getpid())
    need(len(raw) == state.st_size and fingerprint(os.fstat(fd)) == fingerprint(state) and
         live.identity == fingerprint(state) and live.raw == raw and
         hashlib.sha256(raw).hexdigest() == PIN["python_file"] and
         process["executable_dev"] == state.st_dev and
         process["executable_inode"] == state.st_ino and
         process["executable_size"] == state.st_size and
         process["executable_sha256"] == PIN["python_file"],
         "held/live/process machine-python exact identity+bytes")
    return Captured(logical_alias(SEALED_PYTHON), SEALED_PYTHON, raw,
                    fingerprint(state), live.parent_identity)


def validate_worker_runtime(seed: str, formal: bool = False) -> dict[str, Any]:
    expected_keys = {"HOME", "LC_ALL", "TZ", "PYTHONHASHSEED", "PYTHONDONTWRITEBYTECODE",
                     "PYTHONNOUSERSITE", "C65_COLD_LAUNCHER_PID",
                     "C65_COLD_ENTRY_SHA256", "C65_COLD_PYTHON_FD",
                     "C65_COLD_VERIFIER_SHA256", "C65_COLD_SELF_FD", "C65_COLD_SELF_PATH"}
    if formal:
        expected_keys.add("C65_COLD_BOOTSTRAPPED")
    need(set(os.environ) == expected_keys,
         "worker strict environment exact key whitelist")
    need(os.environ["HOME"] == "/nonexistent" and
         os.environ["LC_ALL"] == "C.UTF-8" and os.environ["TZ"] == "UTC" and
         os.environ["PYTHONDONTWRITEBYTECODE"] == "1" and
         os.environ["PYTHONNOUSERSITE"] == "1" and
         os.environ["C65_COLD_SELF_PATH"] == str(SELF),
         "worker strict environment exact values")
    need(os.environ["C65_COLD_ENTRY_SHA256"] == PIN["formal_entry_bootstrap_sha256"] and
         hashlib.sha256(FORMAL_ENTRY_BOOTSTRAP.encode("utf-8")).hexdigest() ==
         PIN["formal_entry_bootstrap_sha256"], "worker exact formal entry literal digest")
    need(str(EXECUTED_SELF) ==
         f"/proc/self/fd/{int(os.environ['C65_COLD_SELF_FD'])}",
         "worker executed-self held-script path")
    flags = sys.flags
    need(sys.prefix == "/usr" and sys.base_prefix == "/usr" and
         Path(sys.executable).absolute() == SEALED_PYTHON_LINK and
         flags.safe_path is True and flags.no_user_site == 1 and
         flags.no_site == 1 and flags.dont_write_bytecode == 1 and flags.hash_randomization == 1 and
         flags.isolated == 0 and flags.ignore_environment == 0 and
         hash(HASH_SENTINEL) == HASH_FINGERPRINTS[seed],
         "worker sealed runtime prefix/-P/-s/-B/hash sentinel")
    process = executable_identity(os.getpid())
    need(process["executable_path"] == str(SEALED_PYTHON) and
         process["executable_sha256"] == PIN["python_file"],
         "worker held-fd machine executable exact")
    return {"sys_prefix": sys.prefix, "sys_executable": sys.executable,
            "pythonhashseed": seed, "hash_sentinel": HASH_FINGERPRINTS[seed],
            "flags": {"safe_path": True, "no_user_site": 1,
                      "no_site": 1, "dont_write_bytecode": 1, "hash_randomization": 1,
                      "isolated": 0, "ignore_environment": 0}}


def worker_main(seed: str, challenge: str) -> int:
    need(os.environ.get("PYTHONHASHSEED") == seed, "worker exact PYTHONHASHSEED")
    validate_worker_runtime(seed)
    expected_self_sha = os.environ.get("C65_COLD_VERIFIER_SHA256", "")
    self_capture = held_self_capture()
    held_python_capture()
    ready = worker_ready(seed, challenge, expected_self_sha, self_capture)
    print(canonical(ready).decode("utf-8"), flush=True)
    need(sys.stdin.readline() == "GO\n", "worker launcher GO handshake")
    value = verify_once()
    validate_projection(value, expected_self_sha=expected_self_sha)
    after = held_self_capture()
    need(self_capture.identity == after.identity and self_capture.raw == after.raw,
         "worker verifier bytes+identity stable through long run")
    print(canonical(value).decode("utf-8"), flush=True)
    return 0


def handshake_worker(seed: str, challenge: str) -> int:
    need(os.environ.get("PYTHONHASHSEED") == seed, "handshake exact seed")
    validate_worker_runtime(seed)
    self_capture = held_self_capture()
    held_python_capture()
    ready = worker_ready(seed, challenge, os.environ["C65_COLD_VERIFIER_SHA256"], self_capture)
    ready.pop("object_sha256")
    ready["schema"] = SCHEMA + ".handshake-ready"
    ready = close(ready)
    print(canonical(ready).decode("utf-8"), flush=True)
    need(sys.stdin.readline() == "GO\n", "handshake GO")
    print(canonical(close({
        "schema": SCHEMA + ".handshake-complete", "seed": seed,
        "challenge_sha256": ready["challenge_sha256"],
        "verifier_file_sha256": ready["verifier_file_sha256"],
        "formal_credit": 0, "whole_parent_credit": 0, "D02_gate_credit": 0,
    })).decode("utf-8"), flush=True)
    return 0


def launch_worker(seed: str, self_sha: str, *, handshake: bool = False) -> tuple[
    subprocess.Popen[str], dict[str, Any], str,
]:
    challenge = os.urandom(32).hex()
    parent_fd = anchored_dirfd(SELF.parent)
    try:
        self_fd = os.open(SELF.name, os.O_RDONLY | os.O_CLOEXEC | getattr(os, "O_NOFOLLOW", 0),
                          dir_fd=parent_fd)
    finally:
        os.close(parent_fd)
    state = os.fstat(self_fd)
    os.lseek(self_fd, 0, os.SEEK_SET)
    raw = b""
    while block := os.read(self_fd, 1 << 20):
        raw += block
    need(stat.S_ISREG(state.st_mode) and state.st_nlink == 1 and
         hashlib.sha256(raw).hexdigest() == self_sha,
         "launcher held verifier bytes exact")
    python_parent_fd = anchored_dirfd(SEALED_PYTHON.parent)
    try:
        python_fd = os.open(SEALED_PYTHON.name, os.O_RDONLY | os.O_CLOEXEC |
                            getattr(os, "O_NOFOLLOW", 0), dir_fd=python_parent_fd)
    finally:
        os.close(python_parent_fd)
    python_state = os.fstat(python_fd)
    os.lseek(python_fd, 0, os.SEEK_SET)
    python_raw = b""
    while block := os.read(python_fd, 1 << 20):
        python_raw += block
    need(stat.S_ISREG(python_state.st_mode) and python_state.st_nlink == 1 and
         fingerprint(os.fstat(python_fd)) == fingerprint(python_state) and
         hashlib.sha256(python_raw).hexdigest() == PIN["python_file"],
         "launcher held machine-python bytes exact")
    os.set_inheritable(self_fd, True)
    os.set_inheritable(python_fd, True)
    environment = {
        "HOME": "/nonexistent", "LC_ALL": "C.UTF-8", "TZ": "UTC",
        "PYTHONHASHSEED": seed, "PYTHONDONTWRITEBYTECODE": "1", "PYTHONNOUSERSITE": "1",
        "C65_COLD_LAUNCHER_PID": str(os.getpid()),
        "C65_COLD_ENTRY_SHA256": os.environ["C65_COLD_ENTRY_SHA256"],
        "C65_COLD_PYTHON_FD": str(python_fd),
        "C65_COLD_VERIFIER_SHA256": self_sha, "C65_COLD_SELF_FD": str(self_fd),
        "C65_COLD_SELF_PATH": str(SELF),
    }
    process: subprocess.Popen[str] | None = None
    try:
        process = subprocess.Popen(
            [str(SEALED_PYTHON_LINK), "-S", "-P", "-s", "-B",
             f"/proc/self/fd/{self_fd}",
             "--handshake-worker" if handshake else "--worker", "--seed", seed,
             "--challenge", challenge], executable=f"/proc/self/fd/{python_fd}",
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            text=True, encoding="utf-8", cwd="/", env=environment, close_fds=True,
            pass_fds=(self_fd, python_fd),
        )
    finally:
        os.close(self_fd)
        os.close(python_fd)
    need(process is not None, "worker created")
    need(process.stdout is not None and process.stdin is not None and process.stderr is not None,
         "worker pipes")
    try:
        selector = selectors.DefaultSelector()
        try:
            selector.register(process.stdout, selectors.EVENT_READ)
            need(bool(selector.select(timeout=30.0)), "worker ready timeout")
        finally:
            selector.close()
        line = process.stdout.readline()
        ready = closed_json((line + ("" if line.endswith("\n") else "\n")).encode("utf-8"),
                            "worker ready")
        live = executable_identity(process.pid)
        expected_schema = SCHEMA + (".handshake-ready" if handshake else ".worker-ready")
        need(ready["schema"] == expected_schema and ready["seed"] == seed and
             ready["challenge_sha256"] == hashlib.sha256(bytes.fromhex(challenge)).hexdigest() and
             ready["process"] == live and ready["launcher_pid"] == os.getpid() and
             ready["verifier_file_sha256"] == self_sha,
             "worker ready independently observed process/source/challenge")
        return process, ready, challenge
    except BaseException:
        terminate_workers((process,))
        raise


def finish_worker(process: subprocess.Popen[str]) -> dict[str, Any]:
    need(process.stdout is not None and process.stderr is not None,
         "worker pipes finish")
    output, errors = process.communicate()
    returncode = process.returncode
    need(returncode == 0 and not errors and output.endswith("\n") and output.count("\n") == 1,
         "worker successful single projection line:" + errors[-2000:])
    value = closed_json(output.encode("utf-8"), "worker projection")
    return validate_projection(value, output.encode("utf-8"))


def finish_handshake_worker(process: subprocess.Popen[str], ready: dict[str, Any],
                            challenge: str) -> dict[str, Any]:
    need(process.stdout is not None and process.stderr is not None,
         "handshake pipes finish")
    output, errors = process.communicate()
    need(process.returncode == 0 and not errors and output.endswith("\n") and
         output.count("\n") == 1, "handshake successful one completion line")
    value = closed_json(output.encode("utf-8"), "handshake complete")
    strict_keys(value, {"schema", "seed", "challenge_sha256", "verifier_file_sha256",
                        "formal_credit", "whole_parent_credit", "D02_gate_credit",
                        "object_sha256"}, "handshake complete")
    need(value["schema"] == SCHEMA + ".handshake-complete" and
         value["seed"] == ready["seed"] and
         value["challenge_sha256"] == hashlib.sha256(bytes.fromhex(challenge)).hexdigest() and
         value["verifier_file_sha256"] == ready["verifier_file_sha256"],
         "handshake exact completion binding")
    zero_credit(value, "handshake")
    return value


def signal_worker(process: subprocess.Popen[str]) -> None:
    need(process.stdin is not None, "worker signal pipe")
    process.stdin.write("GO\n")
    process.stdin.flush()
    process.stdin.close()
    process.stdin = None


def terminate_workers(processes: Iterable[subprocess.Popen[str]]) -> None:
    for process in processes:
        if process.poll() is None:
            process.terminate()
    deadline = time.monotonic() + 5.0
    for process in processes:
        if process.poll() is None:
            try:
                process.wait(timeout=max(0.0, deadline - time.monotonic()))
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()


def parallel_worker_results(processes: list[subprocess.Popen[str]],
                            jobs: list[tuple[Callable[..., dict[str, Any]], tuple[Any, ...]]]
                            ) -> list[dict[str, Any]]:
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=len(jobs))
    futures = [executor.submit(function, *arguments) for function, arguments in jobs]
    try:
        done, pending = concurrent.futures.wait(
            futures, return_when=concurrent.futures.FIRST_EXCEPTION)
        failures = [future for future in done if future.exception() is not None]
        if failures:
            terminate_workers(processes)
            for future in pending:
                future.cancel()
            failure = failures[0].exception()
            need(failure is not None, "parallel worker exception present")
            raise failure
        need(not pending, "parallel workers all complete without exception")
        return [future.result() for future in futures]
    except BaseException:
        terminate_workers(processes)
        raise
    finally:
        executor.shutdown(wait=True, cancel_futures=True)


def dual_held_script_handshake_smoke() -> dict[str, Any]:
    self_sha = hashlib.sha256(held_self_capture().raw).hexdigest()
    processes: list[subprocess.Popen[str]] = []
    records: list[tuple[subprocess.Popen[str], dict[str, Any], str]] = []
    try:
        first = launch_worker("1", self_sha, handshake=True)
        processes.append(first[0])
        tick = 1.0 / int(os.sysconf("SC_CLK_TCK"))
        time.sleep(max(2 * tick, 0.02))
        second = launch_worker("2", self_sha, handshake=True)
        processes.append(second[0])
        records.extend((first, second))
        need(first[0].pid != second[0].pid and
             first[1]["process"]["startticks"] != second[1]["process"]["startticks"],
             "handshake distinct processes/startticks")
        for process, _ready, _challenge in records:
            signal_worker(process)
        completed = parallel_worker_results(
            processes, [(finish_handshake_worker, record) for record in records])
    except BaseException:
        terminate_workers(processes)
        raise
    return {
        "seeds": [item["seed"] for item in completed],
        "distinct_pid_and_startticks": True, "parallel_drain": True,
        "held_script_entry": True, "formal_credit": 0,
        "whole_parent_credit": 0, "D02_gate_credit": 0,
    }


def seed_receipt(seed: str, path: Path, projection: dict[str, Any],
                 projection_raw: bytes, launcher: dict[str, Any], worker: dict[str, Any],
                 challenge: str, self_sha: str) -> dict[str, Any]:
    return close({
        "schema": SCHEMA + ".seed-completion-receipt",
        "status": "PASS_EXTERNAL_LAUNCHER_FRESH_PROCESS_COMPLETION__ZERO_CREDIT",
        "seed": seed, "launcher": launcher, "worker": worker,
        "challenge_sha256": hashlib.sha256(bytes.fromhex(challenge)).hexdigest(),
        "verifier_file_sha256": self_sha,
        "frozen_input_object_sha256": projection["frozen_snapshot"]["object_sha256"],
        "projection_filename": path.name,
        "projection_file_sha256": hashlib.sha256(projection_raw).hexdigest(),
        "projection_object_sha256": projection["object_sha256"],
        "projection_published_before_receipt": True,
        "candidate_is_authority": False, "formal_credit": 0,
        "whole_parent_credit": 0, "D02_gate_credit": 0,
        "runtime_canonical_pointer_or_seal_writes": False,
    })


def launch_dual() -> dict[str, Any]:
    formal_phase_gate("launch")
    validate_formal_process_runtime()
    targets = (SEED1_PROJECTION, SEED1_RECEIPT, SEED2_PROJECTION, SEED2_RECEIPT)
    output_set_state(targets, "dual-seed publication")
    self_before = capture_bounded((SELF,), maximum_each=4 << 20, maximum_total=4 << 20)[SELF]
    self_sha = hashlib.sha256(self_before.raw).hexdigest()
    launcher = executable_identity(os.getpid())
    processes: list[subprocess.Popen[str]] = []
    try:
        first, first_ready, first_challenge = launch_worker("1", self_sha)
        processes.append(first)
        # Ensure different kernel start ticks while retaining parallel numerical work.
        tick = 1.0 / int(os.sysconf("SC_CLK_TCK"))
        time.sleep(max(2 * tick, 0.02))
        second, second_ready, second_challenge = launch_worker("2", self_sha)
        processes.append(second)
        need(first.pid != second.pid and
             first_ready["process"]["startticks"] != second_ready["process"]["startticks"],
             "dual workers distinct pid and startticks")
        signal_worker(first)
        signal_worker(second)
        first_value, second_value = parallel_worker_results(
            processes, [(finish_worker, (first,)), (finish_worker, (second,))])
    except BaseException:
        terminate_workers(processes)
        raise
    first_raw = canonical(first_value) + b"\n"
    second_raw = canonical(second_value) + b"\n"
    need(first_raw == second_raw and first_value == second_value,
         "dual fresh processes byte-identical projection")
    first_receipt = seed_receipt("1", SEED1_PROJECTION, first_value, first_raw,
                                 launcher, first_ready["process"], first_challenge, self_sha)
    second_receipt = seed_receipt("2", SEED2_PROJECTION, second_value, second_raw,
                                  launcher, second_ready["process"], second_challenge, self_sha)
    self_after = capture_bounded((SELF,), maximum_each=4 << 20, maximum_total=4 << 20)[SELF]
    need(self_before.identity == self_after.identity and self_before.raw == self_after.raw,
         "launcher verifier bytes+identity stable through both workers")
    # Each seed is result-last: projection followed by completion receipt.
    publish_bytes(SEED1_PROJECTION, first_raw)
    publish_json(SEED1_RECEIPT, first_receipt)
    publish_bytes(SEED2_PROJECTION, second_raw)
    publish_json(SEED2_RECEIPT, second_receipt)
    return close({
        "schema": SCHEMA + ".dual-launch-summary",
        "status": "PASS_TWO_EXTERNAL_FRESH_PROCESSES_DISTINCT_STARTTICKS_BYTE_IDENTICAL",
        "projection_file_sha256": hashlib.sha256(first_raw).hexdigest(),
        "projection_object_sha256": first_value["object_sha256"],
        "seed1_receipt_object_sha256": first_receipt["object_sha256"],
        "seed2_receipt_object_sha256": second_receipt["object_sha256"],
        "frozen_input_object_sha256": first_value["frozen_snapshot"]["object_sha256"],
        "formal_credit": 0, "whole_parent_credit": 0, "D02_gate_credit": 0,
    })


def validate_process_record(value: Any, label: str) -> dict[str, Any]:
    keys = {
        "pid", "startticks", "executable_path", "executable_dev", "executable_inode",
        "executable_size", "executable_mtime_ns", "executable_sha256",
    }
    strict_keys(value, keys, label)
    for key in ("pid", "startticks", "executable_dev", "executable_inode",
                "executable_size", "executable_mtime_ns"):
        need(type(value[key]) is int and value[key] > 0, label + ":" + key)
    need(type(value["executable_path"]) is str and value["executable_path"].startswith("/") and
         HEX64.fullmatch(str(value["executable_sha256"])) is not None,
         label + ": executable path/hash")
    return value


def validate_seed_receipt(value: dict[str, Any], seed: str, path: Path, raw: bytes,
                          projection: dict[str, Any], self_sha: str) -> dict[str, Any]:
    strict_keys(value, SEED_RECEIPT_KEYS, "seed receipt")
    need(value["schema"] == SCHEMA + ".seed-completion-receipt" and
         value["status"] == "PASS_EXTERNAL_LAUNCHER_FRESH_PROCESS_COMPLETION__ZERO_CREDIT" and
         value["seed"] == seed and
         value["verifier_file_sha256"] == self_sha and
         value["frozen_input_object_sha256"] == projection["frozen_snapshot"]["object_sha256"] and
         value["projection_filename"] == path.name and
         value["projection_file_sha256"] == hashlib.sha256(raw).hexdigest() and
         value["projection_object_sha256"] == projection["object_sha256"] and
         value["projection_published_before_receipt"] is True and
         value["candidate_is_authority"] is False and
         value["runtime_canonical_pointer_or_seal_writes"] is False and
         HEX64.fullmatch(str(value["challenge_sha256"])) is not None,
         "seed receipt exact bindings")
    zero_credit(value, "seed receipt")
    launcher = validate_process_record(value["launcher"], "seed launcher")
    worker = validate_process_record(value["worker"], "seed worker")
    runtime = projection["runtime_identity"]
    expected_process = {
        "executable_path": runtime["python_executable_path"],
        "executable_dev": runtime["python_executable_dev"],
        "executable_inode": runtime["python_executable_inode"],
        "executable_size": runtime["python_executable_size"],
        "executable_mtime_ns": runtime["python_executable_mtime_ns"],
        "executable_sha256": runtime["python_executable_sha256"],
    }
    need(all(worker[key] == expected for key, expected in expected_process.items()) and
         all(launcher[key] == expected for key, expected in expected_process.items()),
         "seed launcher/worker identities equal frozen projection machine runtime")
    return value


def read_dual_evidence(self_capture: Captured) -> tuple[
    dict[str, Any], dict[str, Any], dict[str, Any], bytes, bytes, bytes, bytes,
]:
    raw = capture_bounded((SEED1_PROJECTION, SEED1_RECEIPT,
                           SEED2_PROJECTION, SEED2_RECEIPT),
                          maximum_each=32 << 20, maximum_total=128 << 20)
    self_sha = hashlib.sha256(self_capture.raw).hexdigest()
    p1_raw, p2_raw = raw[SEED1_PROJECTION].raw, raw[SEED2_PROJECTION].raw
    p1 = validate_projection(closed_json(p1_raw, "seed1 projection"), p1_raw, self_sha)
    p2 = validate_projection(closed_json(p2_raw, "seed2 projection"), p2_raw, self_sha)
    need(p1_raw == p2_raw and p1 == p2, "installed dual projections byte-identical")
    r1_raw, r2_raw = raw[SEED1_RECEIPT].raw, raw[SEED2_RECEIPT].raw
    r1 = validate_seed_receipt(closed_json(r1_raw, "seed1 receipt"), "1",
                               SEED1_PROJECTION, p1_raw, p1, self_sha)
    r2 = validate_seed_receipt(closed_json(r2_raw, "seed2 receipt"), "2",
                               SEED2_PROJECTION, p2_raw, p2, self_sha)
    need(r1["worker"]["pid"] != r2["worker"]["pid"] and
         r1["worker"]["startticks"] != r2["worker"]["startticks"] and
         r1["launcher"] == r2["launcher"] and
         r1["challenge_sha256"] != r2["challenge_sha256"],
         "dual receipt independent processes/challenges/distinct startticks")
    return p1, r1, r2, p1_raw, r1_raw, p2_raw, r2_raw


def completion_receipt(phase: str, result_path: Path, result_raw: bytes,
                       result: dict[str, Any], frozen_object: str,
                       self_sha: str) -> dict[str, Any]:
    need(phase in {"install", "self-test"}, "completion phase")
    return close({
        "schema": SCHEMA + ".completion-receipt", "status": "PASS_RESULT_LAST_COMPLETION",
        "phase": phase, "process": executable_identity(os.getpid()),
        "verifier_file_sha256": self_sha,
        "result_filename": result_path.name,
        "result_file_sha256": hashlib.sha256(result_raw).hexdigest(),
        "result_object_sha256": result["object_sha256"],
        "result_published_before_receipt": True,
        "frozen_input_object_sha256": frozen_object,
        "candidate_is_authority": False, "formal_credit": 0,
        "whole_parent_credit": 0, "D02_gate_credit": 0,
        "runtime_canonical_pointer_or_seal_writes": False,
    })


def validate_completion_receipt(value: dict[str, Any], phase: str, result_path: Path,
                                result_raw: bytes, result: dict[str, Any],
                                frozen_object: str, self_sha: str,
                                expected_runtime: Mapping[str, Any]) -> dict[str, Any]:
    strict_keys(value, COMPLETION_RECEIPT_KEYS, phase + " completion receipt")
    need(value["schema"] == SCHEMA + ".completion-receipt" and
         value["status"] == "PASS_RESULT_LAST_COMPLETION" and value["phase"] == phase and
         value["verifier_file_sha256"] == self_sha and
         value["result_filename"] == result_path.name and
         value["result_file_sha256"] == hashlib.sha256(result_raw).hexdigest() and
         value["result_object_sha256"] == result["object_sha256"] and
         value["result_published_before_receipt"] is True and
         value["frozen_input_object_sha256"] == frozen_object and
         value["candidate_is_authority"] is False and
         value["runtime_canonical_pointer_or_seal_writes"] is False,
         phase + ": completion exact binding")
    process = validate_process_record(value["process"], phase + " process")
    need(process["executable_path"] == expected_runtime["python_executable_path"] and
         process["executable_dev"] == expected_runtime["python_executable_dev"] and
         process["executable_inode"] == expected_runtime["python_executable_inode"] and
         process["executable_size"] == expected_runtime["python_executable_size"] and
         process["executable_mtime_ns"] == expected_runtime["python_executable_mtime_ns"] and
         process["executable_sha256"] == expected_runtime["python_executable_sha256"],
         phase + ": completion process exact frozen machine runtime")
    zero_credit(value, phase + " completion")
    return value


def install_verification() -> dict[str, Any]:
    formal_phase_gate("install")
    validate_formal_process_runtime()
    output_set_state((VERIFY_OUT, VERIFY_RECEIPT), "verification installation")
    self_before = capture_bounded((SELF,), maximum_each=4 << 20, maximum_total=4 << 20)[SELF]
    self_sha = hashlib.sha256(self_before.raw).hexdigest()
    projection, first_receipt, second_receipt, projection_raw, *_rest = read_dual_evidence(
        self_before)
    snapshot, metadata = formal_snapshot()
    projection_matches_snapshot(projection, snapshot, metadata)
    authority_snapshot(snapshot)
    validate_rejections(snapshot)
    (_contract, assignment, authorization, c61, _c58, _c40,
     _base_parents) = validate_frozen_objects(snapshot)
    aggregate = closed_json(snap_raw(snapshot, AGG_RESULT), "install aggregate",
                            PIN["aggregate_result_file"], PIN["aggregate_result_object"])
    program_independence(snapshot, aggregate)
    need(assignment["object_sha256"] == PIN["assignment_object"] and
         authorization["object_sha256"] == PIN["authorization_object"] and
         c61["object_sha256"] == PIN["C61_result_object"],
         "install complete frozen object validation")
    body = copy.deepcopy(projection)
    body.pop("object_sha256")
    body["schema"] = SCHEMA + ".verification"
    body["status"] = (
        "PASS_DUAL_EXTERNAL_PROCESS_COLD_VERIFICATION_V4__DISTINCT_STARTTICKS__"
        "EXACT_FROZEN_VECTOR__ZERO_CREDIT"
    )
    body["dual_process_evidence"] = {
        "projection_file_sha256": hashlib.sha256(projection_raw).hexdigest(),
        "projection_object_sha256": projection["object_sha256"],
        "seed1_receipt_object_sha256": first_receipt["object_sha256"],
        "seed2_receipt_object_sha256": second_receipt["object_sha256"],
        "worker_pids": [first_receipt["worker"]["pid"], second_receipt["worker"]["pid"]],
        "worker_startticks": [first_receipt["worker"]["startticks"],
                              second_receipt["worker"]["startticks"]],
        "different_pid_and_startticks": True, "byte_identical": True,
    }
    verification = close(body)
    raw = canonical(verification) + b"\n"
    validate_verification(verification, raw, projection, first_receipt, second_receipt,
                          self_sha)
    receipt = completion_receipt("install", VERIFY_OUT, raw, verification,
                                 projection["frozen_snapshot"]["object_sha256"], self_sha)
    self_after = capture_bounded((SELF,), maximum_each=4 << 20, maximum_total=4 << 20)[SELF]
    need(self_before.identity == self_after.identity and self_before.raw == self_after.raw,
         "installer verifier bytes+identity stable")
    publish_bytes(VERIFY_OUT, raw)
    publish_json(VERIFY_RECEIPT, receipt)
    installed = capture_bounded((VERIFY_OUT, VERIFY_RECEIPT), maximum_each=32 << 20,
                                maximum_total=64 << 20)
    need(installed[VERIFY_OUT].raw == raw and
         validate_verification(closed_json(installed[VERIFY_OUT].raw,
                                           "installed verification"),
                               installed[VERIFY_OUT].raw, projection, first_receipt,
                               second_receipt, self_sha) == verification and
         validate_completion_receipt(
             closed_json(installed[VERIFY_RECEIPT].raw, "installed verification receipt"),
             "install", VERIFY_OUT, raw, verification,
             projection["frozen_snapshot"]["object_sha256"], self_sha,
             projection["runtime_identity"]) == receipt,
         "install result/receipt postpublication pair recapture")
    return verification


def synthetic_baseline() -> dict[str, Any]:
    return close({
        "schema": SCHEMA + ".synthetic-contract",
        "pretty_contract_exact_file_object": True,
        "numeric_source_closure_count": 51,
        "numeric_source_closure_object": PIN["numeric_source_closure_object"],
        "no_pyc_or_preloaded_local_modules": True,
        "single_frozen_snapshot": True, "post_long_run_full_recapture": True,
        "malformed_candidates_rejected": True, "controller_absent": True,
        "executable_identity_stable": True, "receipt_ids": list(SHARDS),
        "receipt_full_fields_exact": True, "per_shard_trie_routes_exact": True,
        "bounded_each": MAX_EACH, "bounded_total": MAX_TOTAL,
        "projection_schema_exact": True, "projection_types_exact": True,
        "external_workers": 2, "distinct_worker_startticks": True,
        "result_last_receipts": True, "orphan_requires_supersession": True,
        "v1_source_not_manifested": True, "v1_rejection_manifested": True,
        "release_full_validator": True, "one_global_manifest_snapshot": True,
        "post_manifest_full_recapture": True, "outer_receipt_last": True,
        "ordered_members_unique": True, "C61_full_base_leaves": C61_FULL_BASE_LEAVES,
        "C61_full_base_terminal": C61_FULL_BASE_TERMINAL,
        "C61_full_base_C2": C61_FULL_BASE_C2,
        "complete_leaves": EXPECTED_COMPLETE_LEAVES,
        "complete_terminal": EXPECTED_COMPLETE_TERMINAL,
        "complete_C2": EXPECTED_REPLACEMENT_C2, "complete_C3": EXPECTED_REPLACEMENT_C3,
        "formal_credit": 0, "whole_parent_credit": 0, "D02_gate_credit": 0,
        "runtime_write": False,
    })


def validate_synthetic(value: dict[str, Any], expected: dict[str, Any]) -> None:
    need(type(value) is dict and set(value) == set(expected), "synthetic exact keys")
    body = copy.deepcopy(value)
    claim = body.pop("object_sha256", None)
    need(claim == digest(body) and canonical(value) == canonical(expected),
         "synthetic exact closed baseline")


def expect_reject(tests: dict[str, bool], name: str, action: Callable[[], Any]) -> None:
    try:
        action()
    except (Reject, AwaitingInputs, OSError, ValueError, TypeError, zlib.error, ImportError):
        tests[name] = True
    else:
        tests[name] = False


def gzip_fixture(rows: list[dict[str, Any]]) -> tuple[bytes, dict[str, Any]]:
    import gzip
    payload = b"".join(canonical(row) + b"\n" for row in rows)
    compressed = gzip.compress(payload, compresslevel=6, mtime=0)
    return compressed, {
        "filename": "fixture.jsonl.gz", "order": "FIXTURE", "row_count": len(rows),
        "row_hash_line_sequence_sha256": hashlib.sha256(
            "".join(row["row_sha256"] + "\n" for row in rows).encode("ascii")
        ).hexdigest(), "sha256": hashlib.sha256(compressed).hexdigest(), "size": len(compressed),
    }


def self_test(self_raw: bytes | None = None) -> dict[str, Any]:
    def formal_target_state() -> tuple[tuple[str, tuple[int, ...] | None], ...]:
        state: list[tuple[str, tuple[int, ...] | None]] = []
        for path in FORMAL_TARGETS:
            try:
                observed = fingerprint(os.lstat(path))
            except FileNotFoundError:
                observed = None
            state.append((path.name, observed))
        return tuple(state)

    formal_before = formal_target_state()
    if self_raw is None:
        self_raw = capture_bounded((SELF,), maximum_each=4 << 20,
                                   maximum_total=4 << 20)[SELF].raw
    baseline = synthetic_baseline()
    validate_synthetic(baseline, baseline)
    tests: dict[str, bool] = {"baseline_valid": True}
    mutation_fields = [key for key in baseline if key not in {"schema", "object_sha256"}]
    for field in mutation_fields:
        attacked = copy.deepcopy(baseline)
        attacked.pop("object_sha256")
        value = attacked[field]
        if type(value) is bool:
            attacked[field] = not value
        elif type(value) is int:
            attacked[field] = value + 1
        elif type(value) is str:
            attacked[field] = "0" * 64 if HEX64.fullmatch(value) else value + "-mutated"
        elif type(value) is list:
            attacked[field] = value[:-1]
        else:
            raise Reject("unhandled synthetic mutation type")
        attacked = close(attacked)
        expect_reject(tests, "coherent_" + field + "_rejected",
                      lambda attacked=attacked: validate_synthetic(attacked, baseline))

    for label, expected in (("credit", 0), ("count", 64), ("depth", 6), ("route", 0)):
        expect_reject(tests, "bool_for_int_" + label + "_rejected",
                      lambda expected=expected: exact_int(True, expected, label))
    tests["JSON_bool_int_type_sensitive"] = canonical({"x": True}) != canonical({"x": 1})
    for name, payload in {
        "BOM": b"\xef\xbb\xbf{}\n", "duplicate_key": b'{"x":1,"x":2}\n',
        "NaN": b'{"x":NaN}\n', "Infinity": b'{"x":Infinity}\n',
        "float": b'{"x":1.25}\n', "trailing": b"{}\nX", "missing_newline": b"{}",
        "pretty_when_compact_required": b'{ "x" : 1 }\n',
    }.items():
        expect_reject(tests, name + "_rejected",
                      lambda payload=payload, name=name: strict_json(payload, name, True))
    pretty = snap = ("{\n  \"formal_credit\": 0,\n  \"object_sha256\": \"" + "0" * 64 +
                     "\"\n}\n").encode("ascii")
    tests["pretty_JSON_syntax_accepts_only_when_explicit"] = type(
        strict_json(pretty, "pretty fixture", False)) is dict
    expect_reject(tests, "pretty_JSON_rejected_at_compact_boundary",
                  lambda: strict_json(pretty, "pretty fixture", True))

    body = {"schema": "fixture.row", "value": 1}
    row = {**body, "row_sha256": digest(body)}
    compressed, desc = gzip_fixture([row])
    tests["valid_single_member_gzip"] = list(iter_gzip(compressed, desc, "valid fixture",
                                                       1 << 20)) == [row]

    def attacked_gzip(payload: bytes, changed: dict[str, Any] | None = None,
                      limit: int = 1 << 20) -> list[dict[str, Any]]:
        candidate = copy.deepcopy(desc if changed is None else changed)
        candidate["sha256"], candidate["size"] = hashlib.sha256(payload).hexdigest(), len(payload)
        return list(iter_gzip(payload, candidate, "attacked gzip", limit))

    for name, payload in {
        "truncated": compressed[:-3], "concatenated": compressed + compressed,
        "trailing_junk": compressed + b"junk",
    }.items():
        expect_reject(tests, "gzip_" + name + "_rejected",
                      lambda payload=payload: attacked_gzip(payload))
    bad_desc = copy.deepcopy(desc)
    bad_desc["row_count"] = 2
    expect_reject(tests, "gzip_count_rejected", lambda: attacked_gzip(compressed, bad_desc))
    bad_desc = copy.deepcopy(desc)
    bad_desc["row_hash_line_sequence_sha256"] = "0" * 64
    expect_reject(tests, "gzip_sequence_rejected", lambda: attacked_gzip(compressed, bad_desc))
    huge_body = {"schema": "fixture.row", "value": "x" * 4096}
    huge, huge_desc = gzip_fixture([{**huge_body, "row_sha256": digest(huge_body)}])
    expect_reject(tests, "gzip_expand_bound_rejected",
                  lambda: list(iter_gzip(huge, huge_desc, "huge", 64)))

    with tempfile.TemporaryDirectory(prefix="cm2-c65-cold-v2-selftest-") as temporary:
        root = Path(temporary)
        target = root / "target"
        target.write_bytes(canonical(baseline) + b"\n")
        link = root / "link"
        link.symlink_to(target.name)
        expect_reject(tests, "symlink_rejected", lambda: capture_bounded((link,)))
        hard = root / "hard"
        os.link(target, hard)
        expect_reject(tests, "hardlink_rejected", lambda: capture_bounded((target,)))
        hard.unlink()
        fifo = root / "fifo"
        os.mkfifo(fifo)
        expect_reject(tests, "FIFO_rejected", lambda: capture_bounded((fifo,)))
        replacement = root / "replacement"
        replacement.write_bytes(canonical(baseline) + b"\n")
        expect_reject(tests, "TOCTOU_replacement_rejected",
                      lambda: capture_bounded((target,), hook=lambda: os.replace(replacement, target)))
        expect_reject(tests, "missing_rejected", lambda: capture_bounded((root / "missing",)))
        first = root / "a"
        second = root / "b"
        first.write_bytes(b"a")
        second.write_bytes(b"b")
        expect_reject(tests, "aggregate_capture_bound_rejected",
                      lambda: capture_bounded((first, second), maximum_each=2, maximum_total=1))

        receipts = root / "receipts"
        receipts.mkdir()
        for shard in SHARDS:
            (receipts / f"{BASE}_shard_{shard:02d}_receipt_v3.json").write_bytes(b"{}\n")
        tests["candidate_exact64_accepts"] = len(candidate_name_gate(receipts, "receipt")) == 64
        malformed = receipts / f"{BASE}_shard_0_receipt_v3.json"
        malformed.write_bytes(b"{}\n")
        expect_reject(tests, "malformed_candidate_rejected",
                      lambda: candidate_name_gate(receipts, "receipt"))
        malformed.unlink()
        missing = receipts / f"{BASE}_shard_63_receipt_v3.json"
        missing.unlink()
        expect_reject(tests, "63_candidate_rejected",
                      lambda: candidate_name_gate(receipts, "receipt"))

        outputs = (root / "projection", root / "receipt")
        tests["fresh_output_set_accepts"] = output_set_state(outputs, "fixture") is None
        outputs[0].write_bytes(b"partial")
        expect_reject(tests, "orphan_output_set_rejected", lambda: output_set_state(outputs, "fixture"))
        outputs[1].write_bytes(b"complete")
        expect_reject(tests, "complete_no_replace_rejected",
                      lambda: output_set_state(outputs, "fixture"))

    # Controlled source loader attacks do not depend on timing or live files.
    fake_path = OUT / "cm2_fake_test.py"
    loader = CapturedSourceLoader({"cm2_fake_test": (b"VALUE = 7\n", fake_path)})
    fake_spec = importlib.util.spec_from_loader("cm2_fake_test", loader)
    need(fake_spec is not None, "fake loader spec")
    fake = importlib.util.module_from_spec(fake_spec)
    loader.exec_module(fake)
    tests["captured_source_loader_valid_source"] = fake.VALUE == 7 and fake.__cached__ is None
    pyc = importlib.util.MAGIC_NUMBER + b"x" * 32
    pyc_loader = CapturedSourceLoader({"cm2_fake_pyc": (pyc, fake_path)})
    pyc_spec = importlib.util.spec_from_loader("cm2_fake_pyc", pyc_loader)
    need(pyc_spec is not None, "pyc loader spec")
    pyc_module = importlib.util.module_from_spec(pyc_spec)
    expect_reject(tests, "pyc_bytes_rejected", lambda: pyc_loader.exec_module(pyc_module))
    expect_reject(tests, "uncaptured_cm2_import_rejected",
                  lambda: loader.find_spec("cm2_unlisted", None, None))

    # Projection exact-schema/type/vector attacks use a compact synthetic
    # projection with the same validator-relevant shape.  Rehashing cannot hide
    # a coherent mutation because validators derive exact constants and vectors.
    projection_source = self_raw.decode("utf-8", "strict")
    tree = ast.parse(projection_source, filename=SELF.name)
    imported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported.add(node.module)
    forbidden = {EXECUTOR.stem, CONTROLLER.stem, CHECKER.stem, PRODUCER.stem}
    tests["AST_no_C65_program_import"] = not (imported & forbidden)
    functions = {node.name: node for node in tree.body if isinstance(node, ast.FunctionDef)}
    segments = {name: ast.get_source_segment(projection_source, node) or ""
                for name, node in functions.items()}
    calls = {
        name: {node.func.id for node in ast.walk(functions[name])
               if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)}
        for name in functions
    }
    forbidden_release_names = {
        "cm2_round306c65s18_64shard_aggregate_independent_cold_verifier_v1.py",
        "cm2_round306c65s18_64shard_aggregate_independent_cold_self_test_v1.json",
        "cm2_round306c65s18_64shard_aggregate_independent_cold_verifier_v3.py",
    }
    release_fixture = release_dependency_paths((V1_REJECTION, V2_REJECTION, V3_REJECTION))
    tests["v1_verifier_absent_from_release_members"] = V1_REJECTION in release_fixture and all(
        path.name not in forbidden_release_names for path in release_fixture)
    tests["v3_verifier_absent_from_release_members"] = V3_REJECTION in release_fixture and all(
        path.name not in forbidden_release_names for path in release_fixture)
    tests["v1_rejection_pin_concrete"] = HEX64.fullmatch(PIN["v1_rejection_file"]) is not None
    tests["aggregate_pins_concrete"] = all(HEX64.fullmatch(PIN[key]) is not None for key in (
        "producer_file", "aggregate_result_file", "aggregate_result_object",
        "aggregate_leaves_file", "aggregate_sources_file", "aggregate_parents_file"))
    publish_calls = {"publish_bytes", "publish_json"}
    tests["formal_outputs_untouched_by_selftest"] = not (
        calls["self_test"] & publish_calls) and formal_target_state() == formal_before
    tests["compute_has_no_direct_publication"] = not (
        calls["verify_once"] & publish_calls)
    tests["selftest_no_clock_order_dependency"] = not (
        calls["self_test"] & {"time", "monotonic", "sleep"}) and \
        not any(isinstance(node, ast.Attribute) and node.attr in {"time", "monotonic", "sleep"}
                for node in ast.walk(functions["self_test"]))
    tests["release_manifest_single_snapshot_design"] = all(token in segments["release"] for token in (
        "manifest_snapshot = capture_bounded(member_paths)",
        "manifest_payload(manifest_snapshot)",
        "parse_manifest(manifest_raw, manifest_snapshot)",
    ))
    alias_fixture = {"alpha": "a", "beta": "b"}
    tests["manifest_basename_alias_is_unique_design"] = len(alias_fixture) == \
        len(set(alias_fixture)) and "alias not in aliases" in segments["manifest_payload"] and \
        "alias not in observed" in segments["parse_manifest"]
    tests["authority_diamond_revisit_allowed"] = acyclic_edges(
        (("a", "b"), ("a", "c"), ("b", "d"), ("c", "d")))
    tests["authority_cycle_rejected"] = not acyclic_edges((("a", "b"), ("b", "a")))
    tests["v2_rejection_pin_concrete"] = PIN["rejected_v2_verifier_file"] == \
        "497da169e255f1382965bc867cdf15525f1cfb60934c8ee746ccb2238b4a8f52"
    tests["v3_rejection_pin_concrete"] = PIN["rejected_v3_verifier_file"] == \
        "f799b40c9d5c6a12df74b2b8c7c87d0b6911c9d7c289eaa3a538a81a76a60a22"
    live_head = capture_bounded((GLOBAL_HEAD,), maximum_each=4 << 20,
                                maximum_total=4 << 20)[GLOBAL_HEAD].raw
    parsed_head = closed_json_field(live_head, "self-test global head",
                                    "authority_seal_object_sha256",
                                    PIN["global_head_file"], PIN["global_head_object"])
    tests["global_head_schema_specific_closure_valid"] = \
        parsed_head["authority_seal_object_sha256"] == PIN["global_head_object"]
    expect_reject(tests, "generic_object_parser_rejects_global_head_schema",
                  lambda: closed_json(live_head, "self-test generic global head"))
    tests["authority_exact_closure_pin_concrete"] = PIN["authority_closure_object"] == \
        "cfed31f01b246d3c30fa97060047c5f510c3055aeff71e651560654abd065747"
    tests["safe_runtime_exact_tree_pin_concrete"] = PIN["safe_runtime_record_object"] == \
        "a1443d028310c26178e41c1ae8d50d90ab16aafcc3fbee98d0936a66fc03161c"
    tests["dual_workers_parallel_GO_design"] = all(token in segments["launch_dual"] for token in (
        "signal_worker(first)", "signal_worker(second)",
        "parallel_worker_results(", "terminate_workers(processes)",
    )) and segments["launch_dual"].index("signal_worker(first)") < \
        segments["launch_dual"].index("parallel_worker_results(") and \
        "FIRST_EXCEPTION" in segments["parallel_worker_results"] and \
        "terminate_workers(processes)" in segments["parallel_worker_results"]
    phase_calls = [(name, ast.literal_eval(call.args[0]))
                   for name in ("launch_dual", "install_verification", "publish_selftest", "release")
                   for call in ast.walk(functions[name])
                   if isinstance(call, ast.Call) and isinstance(call.func, ast.Name) and
                   call.func.id == "formal_phase_gate" and len(call.args) == 1 and
                   isinstance(call.args[0], ast.Constant)]
    tests["formal_eleven_target_phase_grammar_design"] = \
        phase_calls == [("launch_dual", "launch"), ("install_verification", "install"),
                        ("publish_selftest", "self-test"), ("release", "release")] and \
        "len(FORMAL_TARGETS)" in projection_source and "exact eleven-target phase grammar" in \
        segments["formal_phase_gate"]
    tests["install_full_non_numeric_revalidation_design"] = all(
        call in calls["install_verification"] for call in (
            "formal_snapshot", "projection_matches_snapshot", "authority_snapshot",
            "validate_rejections", "validate_frozen_objects", "program_independence",
            "validate_verification", "validate_completion_receipt"))
    tests["post_outer_joint_recapture_design"] = all(token in segments["release"] for token in (
        "post_outer = capture_bounded((*member_paths, MANIFEST_OUT, OUTER_RECEIPT))",
        "post-manifest to post-outer manifest identity continuity",
        "post-outer joint members+manifest+outer terminal replay",
    ))

    exact_test_keys = sorted(tests)
    need(set(tests) == EXPECTED_SELFTEST_KEYS and len(EXPECTED_SELFTEST_KEYS) == 98 and
         digest(exact_test_keys) == PIN["selftest_key_object"] and
         all(type(value) is bool and value is True for value in tests.values()),
         f"self-test completeness:{sum(tests.values())}/{len(tests)}")
    return close({
        "schema": SCHEMA + ".self-test",
        "status": f"PASS_{len(tests)}_OF_{len(tests)}_PROTOCOL_FILESYSTEM_SCHEMA_LOADER_"
                  "PROVENANCE_MANIFEST_AND_C61_BASELINE_ATTACKS",
        "verifier_file_sha256": hashlib.sha256(self_raw).hexdigest(),
        "terminal_rejection": {
            "v1_marker_filename": V1_REJECTION.name,
            "v1_marker_file_sha256": PIN["v1_rejection_file"],
            "rejected_selftest_file_sha256": PIN["rejected_v1_selftest_file"],
            "rejected_selftest_object_sha256": PIN["rejected_v1_selftest_object"],
            "v2_marker_filename": V2_REJECTION.name,
            "v2_marker_file_sha256": PIN["v2_rejection_file"],
            "rejected_v2_verifier_file_sha256": PIN["rejected_v2_verifier_file"],
            "v3_marker_filename": V3_REJECTION.name,
            "v3_marker_file_sha256": PIN["v3_rejection_file"],
            "rejected_v3_verifier_file_sha256": PIN["rejected_v3_verifier_file"],
        },
        "tests": tests, "test_count": len(tests), "synthetic_is_authority": False,
        "candidate_is_authority": False, "formal_credit": 0,
        "whole_parent_credit": 0, "D02_gate_credit": 0,
        "runtime_canonical_pointer_or_seal_writes": False,
    })


def publish_selftest() -> dict[str, Any]:
    formal_phase_gate("self-test")
    validate_formal_process_runtime()
    output_set_state((SELFTEST_OUT, SELFTEST_RECEIPT), "self-test publication")
    self_before = capture_bounded((SELF,), maximum_each=4 << 20, maximum_total=4 << 20)[SELF]
    self_sha = hashlib.sha256(self_before.raw).hexdigest()
    projection, *_evidence = read_dual_evidence(self_before)
    value = self_test(self_before.raw)
    raw = canonical(value) + b"\n"
    # Self-test has no numeric input projection; bind the frozen synthetic
    # contract as its completion-domain object.
    frozen_object = synthetic_baseline()["object_sha256"]
    receipt = completion_receipt("self-test", SELFTEST_OUT, raw, value, frozen_object, self_sha)
    self_after = capture_bounded((SELF,), maximum_each=4 << 20, maximum_total=4 << 20)[SELF]
    need(self_before.identity == self_after.identity and self_before.raw == self_after.raw,
         "self-test publisher verifier bytes+identity stable")
    publish_bytes(SELFTEST_OUT, raw)
    publish_json(SELFTEST_RECEIPT, receipt)
    installed = capture_bounded((SELFTEST_OUT, SELFTEST_RECEIPT), maximum_each=16 << 20,
                                maximum_total=32 << 20)
    need(installed[SELFTEST_OUT].raw == raw and
         validate_selftest(closed_json(installed[SELFTEST_OUT].raw,
                                       "installed self-test"),
                           installed[SELFTEST_OUT].raw, self_sha) == value and
         validate_completion_receipt(
             closed_json(installed[SELFTEST_RECEIPT].raw, "installed self-test receipt"),
             "self-test", SELFTEST_OUT, raw, value, frozen_object, self_sha,
             projection["runtime_identity"]) == receipt,
         "self-test result/receipt postpublication pair recapture")
    return value


def validate_selftest(value: dict[str, Any], raw: bytes, self_sha: str) -> dict[str, Any]:
    strict_keys(value, {
        "schema", "status", "verifier_file_sha256", "terminal_rejection", "tests",
        "test_count", "synthetic_is_authority", "candidate_is_authority", "formal_credit",
        "whole_parent_credit", "D02_gate_credit", "runtime_canonical_pointer_or_seal_writes",
        "object_sha256",
    }, "self-test")
    need(value["schema"] == SCHEMA + ".self-test" and
         value["status"] ==
         "PASS_98_OF_98_PROTOCOL_FILESYSTEM_SCHEMA_LOADER_PROVENANCE_MANIFEST_AND_C61_BASELINE_ATTACKS" and
         value["verifier_file_sha256"] == self_sha and
         type(value["tests"]) is dict and type(value["test_count"]) is int and
         value["test_count"] == len(value["tests"]) == 98 and
         set(value["tests"]) == EXPECTED_SELFTEST_KEYS and
         digest(sorted(value["tests"])) == PIN["selftest_key_object"] and
         all(type(item) is bool and item is True for item in value["tests"].values()) and
         value["synthetic_is_authority"] is False and value["candidate_is_authority"] is False and
         value["runtime_canonical_pointer_or_seal_writes"] is False,
         "self-test exact schema/status/tests")
    need(value["terminal_rejection"] == {
        "v1_marker_filename": V1_REJECTION.name,
        "v1_marker_file_sha256": PIN["v1_rejection_file"],
        "rejected_selftest_file_sha256": PIN["rejected_v1_selftest_file"],
        "rejected_selftest_object_sha256": PIN["rejected_v1_selftest_object"],
        "v2_marker_filename": V2_REJECTION.name,
        "v2_marker_file_sha256": PIN["v2_rejection_file"],
        "rejected_v2_verifier_file_sha256": PIN["rejected_v2_verifier_file"],
        "v3_marker_filename": V3_REJECTION.name,
        "v3_marker_file_sha256": PIN["v3_rejection_file"],
        "rejected_v3_verifier_file_sha256": PIN["rejected_v3_verifier_file"],
    }, "self-test exact v1/v2/v3 rejection binding")
    zero_credit(value, "self-test")
    body = copy.deepcopy(value)
    claim = body.pop("object_sha256")
    need(claim == digest(body) and raw == canonical(value) + b"\n", "self-test closure/bytes")
    return value


def validate_verification_projection(value: dict[str, Any], self_sha: str) -> None:
    """Reuse the full projection validator on a verification's common fields."""
    candidate = {key: copy.deepcopy(value[key]) for key in PROJECTION_KEYS}
    candidate["schema"] = SCHEMA + ".cold-projection"
    candidate["status"] = (
        "PASS_COMPLETE_C65_AGGREGATE_COLD_NUMERIC_REPLAY_V4__64_OF_64__"
        "20879_ASSIGNMENTS__C61_FULL_BASE_REPLACEMENT__ZERO_CREDIT"
    )
    body = copy.deepcopy(candidate)
    body.pop("object_sha256")
    candidate["object_sha256"] = digest(body)
    validate_projection(candidate, expected_self_sha=self_sha)
    need(candidate["independence"]["cold_verifier_file_sha256"] == self_sha,
         "verification captured verifier SHA")


def validate_verification(value: dict[str, Any], raw: bytes,
                          projection: dict[str, Any], first_receipt: dict[str, Any],
                          second_receipt: dict[str, Any], self_sha: str) -> dict[str, Any]:
    expected_keys = (PROJECTION_KEYS - {"object_sha256"}) | {"dual_process_evidence",
                                                                 "object_sha256"}
    strict_keys(value, expected_keys, "verification")
    need(value["schema"] == SCHEMA + ".verification" and
         value["status"] ==
         "PASS_DUAL_EXTERNAL_PROCESS_COLD_VERIFICATION_V4__DISTINCT_STARTTICKS__EXACT_FROZEN_VECTOR__ZERO_CREDIT",
         "verification exact schema/status")
    validate_verification_projection(value, self_sha)
    evidence = strict_keys(value["dual_process_evidence"], {
        "projection_file_sha256", "projection_object_sha256",
        "seed1_receipt_object_sha256", "seed2_receipt_object_sha256",
        "worker_pids", "worker_startticks", "different_pid_and_startticks", "byte_identical",
    }, "dual process evidence")
    need(evidence == {
        "projection_file_sha256": hashlib.sha256(canonical(projection) + b"\n").hexdigest(),
        "projection_object_sha256": projection["object_sha256"],
        "seed1_receipt_object_sha256": first_receipt["object_sha256"],
        "seed2_receipt_object_sha256": second_receipt["object_sha256"],
        "worker_pids": [first_receipt["worker"]["pid"], second_receipt["worker"]["pid"]],
        "worker_startticks": [first_receipt["worker"]["startticks"],
                              second_receipt["worker"]["startticks"]],
        "different_pid_and_startticks": True, "byte_identical": True,
    }, "verification exact dual evidence projection")
    projection_body = copy.deepcopy(projection)
    projection_body.pop("object_sha256")
    observed_body = copy.deepcopy(value)
    claim = observed_body.pop("object_sha256")
    observed_body.pop("dual_process_evidence")
    projection_body["schema"] = SCHEMA + ".verification"
    projection_body["status"] = value["status"]
    need(observed_body == projection_body and claim == digest({**observed_body,
             "dual_process_evidence": evidence}) and raw == canonical(value) + b"\n",
         "verification exact projection schema/types/vector/closure")
    zero_credit(value, "verification")
    return value


def release_dependency_paths(formal_paths: Iterable[Path]) -> tuple[Path, ...]:
    # Rejected verifier/source bundles are deliberately absent.  Their
    # terminal rejection markers are included and semantically validated.
    additions = (
        SEED1_PROJECTION, SEED1_RECEIPT, SEED2_PROJECTION, SEED2_RECEIPT,
        VERIFY_OUT, VERIFY_RECEIPT, SELFTEST_OUT, SELFTEST_RECEIPT, REPLAY_OUT,
    )
    ordered = tuple(dict.fromkeys((*formal_paths, *additions)))
    need(len(ordered) == len(set(ordered)) and
         all(path in ordered for path in (V1_REJECTION, V2_REJECTION, V3_REJECTION)) and
         not any(path.name == "cm2_round306c65s18_64shard_aggregate_independent_cold_verifier_v1.py"
                 for path in ordered) and
         not any(path.name == "cm2_round306c65s18_64shard_aggregate_independent_cold_self_test_v1.json"
                 for path in ordered) and
         not any(path.name == "cm2_round306c65s18_64shard_aggregate_independent_cold_verifier_v3.py"
                 for path in ordered), "release exact v1/v2/v3 rejection-only dependency policy")
    return ordered


def validate_release_global_snapshot(global_snapshot: Mapping[Path, Captured],
                                     formal_paths: Iterable[Path], self_sha: str,
                                     expected_formal: Mapping[Path, Captured]) -> None:
    """Rebuild every release prerequisite from one global byte/identity capture."""
    formal = {path: global_snapshot[path] for path in formal_paths}
    compare_recapture(expected_formal, formal, "release global/formal")

    p1_raw = global_snapshot[SEED1_PROJECTION].raw
    p2_raw = global_snapshot[SEED2_PROJECTION].raw
    p1 = validate_projection(closed_json(p1_raw, "global seed1 projection"), p1_raw, self_sha)
    p2 = validate_projection(closed_json(p2_raw, "global seed2 projection"), p2_raw, self_sha)
    need(p1_raw == p2_raw and p1 == p2, "global dual projections byte-identical")
    r1 = validate_seed_receipt(
        closed_json(global_snapshot[SEED1_RECEIPT].raw, "global seed1 receipt"),
        "1", SEED1_PROJECTION, p1_raw, p1, self_sha)
    r2 = validate_seed_receipt(
        closed_json(global_snapshot[SEED2_RECEIPT].raw, "global seed2 receipt"),
        "2", SEED2_PROJECTION, p2_raw, p2, self_sha)
    need(r1["worker"]["pid"] != r2["worker"]["pid"] and
         r1["worker"]["startticks"] != r2["worker"]["startticks"] and
         r1["launcher"] == r2["launcher"] and
         r1["challenge_sha256"] != r2["challenge_sha256"],
         "global dual process provenance exact")

    verification_raw = global_snapshot[VERIFY_OUT].raw
    verification = validate_verification(
        closed_json(verification_raw, "global verification"), verification_raw,
        p1, r1, r2, self_sha)
    validate_completion_receipt(
        closed_json(global_snapshot[VERIFY_RECEIPT].raw, "global verification completion"),
        "install", VERIFY_OUT, verification_raw, verification,
        p1["frozen_snapshot"]["object_sha256"], self_sha, p1["runtime_identity"])
    selftest_raw = global_snapshot[SELFTEST_OUT].raw
    selftest = validate_selftest(
        closed_json(selftest_raw, "global self-test"), selftest_raw, self_sha)
    expected_selftest = self_test(global_snapshot[SELF].raw)
    need(selftest_raw == canonical(expected_selftest) + b"\n" and
         selftest == expected_selftest,
         "global self-test byte-exact recomputation from captured SELF bytes")
    validate_completion_receipt(
        closed_json(global_snapshot[SELFTEST_RECEIPT].raw, "global selftest completion"),
        "self-test", SELFTEST_OUT, selftest_raw, selftest,
        synthetic_baseline()["object_sha256"], self_sha, p1["runtime_identity"])

    projection_matches_snapshot(p1, formal, projection_metadata_from_snapshot(formal))
    validate_rejections(formal)
    authority_snapshot(formal)
    aggregate = closed_json(snap_raw(formal, AGG_RESULT), "global release aggregate",
                            PIN["aggregate_result_file"], PIN["aggregate_result_object"])
    program_independence(formal, aggregate)
    need([item["sha256"] for item in aggregate_descriptors(aggregate)] == [
        PIN["aggregate_leaves_file"], PIN["aggregate_sources_file"],
        PIN["aggregate_parents_file"],
    ], "global release exact aggregate descriptors")
    expected_replay = replay_value(
        verification, selftest, p1["frozen_snapshot"]["object_sha256"])
    need(global_snapshot[REPLAY_OUT].raw == canonical(expected_replay) + b"\n" and
         closed_json(global_snapshot[REPLAY_OUT].raw, "global replay") == expected_replay,
         "global replay exact closure")


def manifest_payload(snapshot: Mapping[Path, Captured]) -> bytes:
    lines: list[str] = []
    aliases: set[str] = set()
    for path, item in snapshot.items():
        alias = item.logical_name
        need(alias not in aliases, "manifest logical basename unique")
        aliases.add(alias)
        lines.append(hashlib.sha256(item.raw).hexdigest() + "  " + alias + "\n")
    return "".join(lines).encode("ascii")


def parse_manifest(raw: bytes, expected_snapshot: Mapping[Path, Captured]) -> dict[str, str]:
    need(raw.endswith(b"\n") and b"\r" not in raw and raw, "manifest framing")
    expected_aliases = [item.logical_name for item in expected_snapshot.values()]
    observed: dict[str, str] = {}
    for line in raw.decode("ascii", "strict").splitlines():
        need(re.fullmatch(r"[0-9a-f]{64}  [A-Za-z0-9_.-]+", line) is not None,
             "manifest line syntax")
        claim, alias = line.split("  ", 1)
        need(alias not in observed, "manifest alias uniqueness")
        observed[alias] = claim
    need(list(observed) == expected_aliases and len(observed) == len(expected_snapshot),
         "manifest exact ordered member set/count")
    for item in expected_snapshot.values():
        need(observed[item.logical_name] == hashlib.sha256(item.raw).hexdigest(),
             "manifest byte closure:" + item.logical_name)
    return observed


def replay_value(verification: dict[str, Any], selftest: dict[str, Any],
                 frozen_object: str) -> dict[str, Any]:
    return close({
        "schema": SCHEMA + ".postpublication-replay",
        "status": "PASS_FULL_RELEASE_VALIDATION_AND_POSTPUBLICATION_RECAPTURE__ZERO_CREDIT",
        "verification_file_sha256": hashlib.sha256(canonical(verification) + b"\n").hexdigest(),
        "verification_object_sha256": verification["object_sha256"],
        "self_test_file_sha256": hashlib.sha256(canonical(selftest) + b"\n").hexdigest(),
        "self_test_object_sha256": selftest["object_sha256"],
        "frozen_input_object_sha256": frozen_object,
        "full_validation_reused_at_release": True,
        "manifest_and_outer_receipt_published_after_this_result": True,
        "candidate_is_authority": False, "formal_credit": 0,
        "whole_parent_credit": 0, "D02_gate_credit": 0,
        "runtime_canonical_pointer_or_seal_writes": False,
    })


def outer_receipt_value(manifest_raw: bytes, manifest_snapshot: Mapping[Path, Captured],
                        closure: dict[str, str], frozen_object: str) -> dict[str, Any]:
    return close({
        "schema": SCHEMA + ".outer-receipt",
        "status": "PASS_ONE_GLOBAL_FROZEN_MANIFEST_AND_FULL_POSTPUBLICATION_RECAPTURE__ZERO_CREDIT",
        "manifest_filename": MANIFEST_OUT.name,
        "manifest_file_sha256": hashlib.sha256(manifest_raw).hexdigest(),
        "manifest_member_count": len(manifest_snapshot),
        "manifest_ordered_alias_sequence_sha256": hashlib.sha256(
            "".join(alias + "\n" for alias in closure).encode("ascii")).hexdigest(),
        "manifest_members_recaptured_after_publication": True,
        "manifest_member_bytes_and_identities_unchanged": True,
        "manifest_recaptured_and_parsed_after_publication": True,
        "frozen_input_object_sha256": frozen_object,
        "outer_receipt_published_last": True,
        "candidate_is_authority": False, "formal_credit": 0,
        "whole_parent_credit": 0, "D02_gate_credit": 0,
        "runtime_canonical_pointer_or_seal_writes": False,
    })


def release() -> dict[str, Any]:
    formal_phase_gate("release")
    validate_formal_process_runtime()
    # Result-last for release: replay, global manifest, then outer receipt.
    output_set_state((REPLAY_OUT, MANIFEST_OUT, OUTER_RECEIPT), "release publication")
    self_before = capture_bounded((SELF,), maximum_each=4 << 20, maximum_total=4 << 20)[SELF]
    self_sha = hashlib.sha256(self_before.raw).hexdigest()
    projection, first_receipt, second_receipt, *_dual_raw = read_dual_evidence(self_before)
    prerequisites = capture_bounded((VERIFY_OUT, VERIFY_RECEIPT, SELFTEST_OUT, SELFTEST_RECEIPT),
                                    maximum_each=64 << 20, maximum_total=256 << 20)
    verification_raw = prerequisites[VERIFY_OUT].raw
    verification = validate_verification(
        closed_json(verification_raw, "release verification"), verification_raw,
        projection, first_receipt, second_receipt, self_sha)
    verify_receipt_raw = prerequisites[VERIFY_RECEIPT].raw
    validate_completion_receipt(closed_json(verify_receipt_raw, "verification completion"),
                                "install", VERIFY_OUT, verification_raw, verification,
                                projection["frozen_snapshot"]["object_sha256"], self_sha,
                                projection["runtime_identity"])
    selftest_raw = prerequisites[SELFTEST_OUT].raw
    selftest = validate_selftest(closed_json(selftest_raw, "release self-test"), selftest_raw,
                                 self_sha)
    selftest_receipt_raw = prerequisites[SELFTEST_RECEIPT].raw
    validate_completion_receipt(closed_json(selftest_receipt_raw, "selftest completion"),
                                "self-test", SELFTEST_OUT, selftest_raw, selftest,
                                synthetic_baseline()["object_sha256"], self_sha,
                                projection["runtime_identity"])
    snapshot, metadata = formal_snapshot()
    projection_matches_snapshot(projection, snapshot, metadata)
    validate_rejections(snapshot)
    authority_snapshot(snapshot)
    # Re-validate exact aggregate pins, producer binding, result projection,
    # dual evidence, and all frozen inputs rather than trusting PASS labels.
    aggregate = closed_json(snap_raw(snapshot, AGG_RESULT), "release aggregate",
                            PIN["aggregate_result_file"], PIN["aggregate_result_object"])
    program_independence(snapshot, aggregate)
    descriptors = aggregate_descriptors(aggregate)
    need([item["sha256"] for item in descriptors] == [
        PIN["aggregate_leaves_file"], PIN["aggregate_sources_file"],
        PIN["aggregate_parents_file"],
    ], "release aggregate exact ledger pins")
    replay = replay_value(verification, selftest, metadata["frozen_input_object_sha256"])
    replay_raw = canonical(replay) + b"\n"
    publish_bytes(REPLAY_OUT, replay_raw)

    member_paths = release_dependency_paths(tuple(snapshot))
    manifest_snapshot = capture_bounded(member_paths)
    validate_release_global_snapshot(manifest_snapshot, tuple(snapshot), self_sha, snapshot)
    manifest_raw = manifest_payload(manifest_snapshot)
    closure = parse_manifest(manifest_raw, manifest_snapshot)
    publish_bytes(MANIFEST_OUT, manifest_raw)
    # Publication is not trusted until an independent fresh capture verifies
    # every member and the manifest itself, including identity continuity.
    post_manifest = capture_bounded((*member_paths, MANIFEST_OUT))
    recaptured_members = {path: post_manifest[path] for path in member_paths}
    compare_recapture(manifest_snapshot, recaptured_members,
                      "post-manifest joint all-member capture")
    need(post_manifest[MANIFEST_OUT].raw == manifest_raw and
         parse_manifest(post_manifest[MANIFEST_OUT].raw, recaptured_members) == closure,
         "postpublication joint manifest+member recapture/closure")
    need(shard_name_barrier() == tuple(tuple(values) for values in metadata["shard_names"]),
         "release shard names stable")
    stable_runtime(metadata["runtime"], runtime_barrier(), "release runtime stable")
    need(metadata["runtime_link"] == runtime_link_record(),
         "release pre-outer sealed-python symlink identity stable")
    final_formal = capture_bounded(tuple(snapshot))
    compare_recapture(snapshot, final_formal, "release all formal inputs stable")
    outer = outer_receipt_value(manifest_raw, manifest_snapshot, closure,
                                metadata["frozen_input_object_sha256"])
    publish_json(OUTER_RECEIPT, outer)
    post_outer = capture_bounded((*member_paths, MANIFEST_OUT, OUTER_RECEIPT))
    post_outer_members = {path: post_outer[path] for path in member_paths}
    compare_recapture(manifest_snapshot, post_outer_members,
                      "post-outer joint all-member capture")
    compare_recapture({MANIFEST_OUT: post_manifest[MANIFEST_OUT]},
                      {MANIFEST_OUT: post_outer[MANIFEST_OUT]},
                      "post-manifest to post-outer manifest identity continuity")
    need(post_outer[MANIFEST_OUT].raw == manifest_raw and
         parse_manifest(post_outer[MANIFEST_OUT].raw, post_outer_members) == closure and
         post_outer[OUTER_RECEIPT].raw == canonical(outer) + b"\n",
         "post-outer joint members+manifest+outer terminal replay")
    need(metadata["runtime_link"] == runtime_link_record(),
         "release post-outer sealed-python symlink identity stable")
    self_after = capture_bounded((SELF,), maximum_each=4 << 20, maximum_total=4 << 20)[SELF]
    need(self_before.identity == self_after.identity and self_before.raw == self_after.raw,
         "release verifier bytes+identity stable")
    return outer


def main() -> int:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--worker", action="store_true")
    group.add_argument("--handshake-worker", action="store_true")
    group.add_argument("--launch-dual", action="store_true")
    group.add_argument("--install", action="store_true")
    group.add_argument("--self-test", action="store_true")
    group.add_argument("--preflight-smoke", action="store_true")
    group.add_argument("--publish-self-test", action="store_true")
    group.add_argument("--release", action="store_true")
    parser.add_argument("--seed")
    parser.add_argument("--challenge")
    arguments = parser.parse_args()
    try:
        ordinary_selftest = arguments.self_test and \
            os.environ.get("C65_COLD_BOOTSTRAPPED") != "1"
        internal_worker = arguments.worker or arguments.handshake_worker
        if not internal_worker and not ordinary_selftest:
            need(os.environ.get("C65_COLD_BOOTSTRAPPED") == "1",
                 "formal CLI requires pinned external entry + held-script execve; "
                 "direct execution is non-authoritative and rejected before reads/writes")
        if internal_worker:
            need(arguments.seed is not None and arguments.challenge is not None,
                 "worker seed/challenge required")
            if arguments.handshake_worker:
                return handshake_worker(arguments.seed, arguments.challenge)
            return worker_main(arguments.seed, arguments.challenge)
        need(arguments.seed is None and arguments.challenge is None,
             "seed/challenge internal worker-only")
        if arguments.launch_dual:
            value = launch_dual()
        elif arguments.install:
            value = install_verification()
        elif arguments.self_test:
            if not ordinary_selftest:
                validate_formal_process_runtime()
            one = capture_bounded((SELF,), maximum_each=4 << 20, maximum_total=4 << 20)[SELF]
            value = self_test(one.raw)
            two = capture_bounded((SELF,), maximum_each=4 << 20, maximum_total=4 << 20)[SELF]
            need(one.identity == two.identity and one.raw == two.raw,
                 "self-test verifier bytes+identity stable")
        elif arguments.preflight_smoke:
            value = preflight_smoke()
        elif arguments.publish_self_test:
            value = publish_selftest()
        else:
            value = release()
        print(json.dumps({"status": value["status"], "object_sha256": value["object_sha256"]},
                         sort_keys=True, separators=(",", ":")))
        return 0
    except (AwaitingInputs, Reject, OSError, KeyError, TypeError, ValueError,
            SyntaxError, ImportError, zlib.error, subprocess.SubprocessError) as error:
        print(json.dumps({"status": "FAIL_CLOSED", "reason": str(error)},
                         sort_keys=True, separators=(",", ":")))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
