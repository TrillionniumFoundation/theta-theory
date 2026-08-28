#!/usr/bin/env python3
"""Externally pinned cold launcher for the C79g v6 exact10 static bundle.

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


CHECKPOINT = "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab"
BASE = "cm2_round306c79g_true_global_no_producer_consumer"
LAUNCHER_RELATIVE = Path("deliverables") / (BASE + "_cold_launch_v6.py")

# No workspace path is trusted at module-import time.  These values are
# configured exactly once by HeldBootstrapEntry after the sealed exec fd,
# installed source fd, and inherited workspace-root fd have been proved.
ROOT = Path("/__C79G_V6_UNCONFIGURED_ROOT__")
OUT = ROOT / "deliverables"
RUNTIME = ROOT / ".cm2-runtime"
SELF = ROOT / LAUNCHER_RELATIVE
V3_OFFICIAL_REJECTION = ROOT / "__unconfigured_v3_rejection__"
V4_REJECTION_SUPERSESSION = ROOT / "__unconfigured_v4_supersession__"
V5_OFFICIAL_REJECTION = ROOT / "__unconfigured_v5_rejection__"
V6_REJECTION_NAMESPACE = ROOT / "__unconfigured_v6_rejections__"
V6_LATER_REJECTION = V6_REJECTION_NAMESPACE / "rejection.json"
SCHEMA = CONTRACT = PRODUCER = CONSUMER = TRANSITION = AUDIT = SELF
MANIFEST = OUTER = SELF

# These deliberately nonzero values are draft sentinels, not publication
# pins.  The root integrator must mechanically replace every sentinel and set
# FINAL_BASE7_PINS_INSTALLED=True only after all seven bytes are final and the
# two independent static audits agree.  Runtime always rejects while false.
FINAL_BASE7_PINS_INSTALLED = True
_DRAFT_FILE_PIN = "f" * 64
_DRAFT_OBJECT_PIN = "e" * 64
BASE7_PINS: dict[Path, tuple[str, str | None]] = {}
EXACT8: tuple[Path, ...] = ()
V3_EXACT10_PINS: tuple[tuple[Path, str, str | None], ...] = ()
V4_FROZEN_DRAFT7_PINS: tuple[tuple[Path, str, str | None], ...] = ()
V4_FORBIDDEN_RUNTIME_PATHS: tuple[Path, ...] = ()
V5_EXACT10_PINS: tuple[tuple[Path, str, str | None], ...] = ()
V5_FORBIDDEN_RUNTIME_PATHS: tuple[Path, ...] = ()

V3_REJECTION_FILE_PIN = (
    "57ce7a4361555c4ff403f725f17ef9cef50446a2e76d7086635c30a0f17bc62f")
V3_REJECTION_OBJECT_PIN = (
    "c946e0d8170a75e32aa7031b42cf0dd5b7b585ba463b7b1ce0010cb65bb3b421")
V4_SUPERSESSION_FILE_PIN = (
    "e3dff621fec2fa5bac14f73685c8f44ce89bc68d80b6478e0688ce926f57c183")
V4_SUPERSESSION_OBJECT_PIN = (
    "1c8fc9d91be75502b0741b096a1ca6d9d59b877b1e69daada15096669215d19f")
V5_REJECTION_FILE_PIN = (
    "c49218967b2d5023d07e5c65fa53df12f0383d6644bf4bd7d35a8e50abeb85b5")
V5_REJECTION_OBJECT_PIN = (
    "9a94bf8b580f6145c4977dd335d9a63c69057d18d62678ab47c7916c764f8e4c")
V5_STRICT_BOOL_UNPROVED_CENSUS_SHA256 = (
    "90b5b3c6059ca166b56a9aad5d456c3308814df12465a7e6f326131d3bbabbf2")
V5_STRICT_BOOL_RISK_IDS = (
    "V5_LAUNCHER_SCHEMA_DEFS_NAME_NON_BOOL",
    "V5_LAUNCHER_SCHEMA_PROPERTY_NAME_NON_BOOL",
    "V5_CONSUMER_ATTACK_PATCH_NON_BOOL",
    "V5_PRODUCER_RELATIVE_PARTS_NON_BOOL_SHORT_CIRCUIT",
    "V5_CONSUMER_RELATIVE_PARTS_NON_BOOL_SHORT_CIRCUIT",
    "V5_LAUNCHER_RELATIVE_PARTS_NON_BOOL_SHORT_CIRCUIT",
    "V5_LAUNCHER_RELATIVE_BYTES_NON_BOOL_SHORT_CIRCUIT",
)
V5_STRICT_BOOL_RISK_ID_ORDER_SHA256 = (
    "8f0957d9aa790bb7a5209e1fae86dd02d0d05de0afb2c6bb24301fe793e7ea4b")


def configure_workspace_paths(root: Path) -> None:
    """Install the one root-fd-bound lexical namespace after self-proof."""
    global ROOT, OUT, RUNTIME, SELF, V3_OFFICIAL_REJECTION
    global V4_REJECTION_SUPERSESSION, V5_OFFICIAL_REJECTION
    global V6_REJECTION_NAMESPACE
    global V6_LATER_REJECTION, SCHEMA, CONTRACT, PRODUCER, CONSUMER
    global TRANSITION, AUDIT, MANIFEST, OUTER, BASE7_PINS, EXACT8
    global V3_EXACT10_PINS, V4_FROZEN_DRAFT7_PINS, V5_EXACT10_PINS
    global V4_FORBIDDEN_RUNTIME_PATHS, V5_FORBIDDEN_RUNTIME_PATHS
    ROOT = root
    OUT = ROOT / "deliverables"
    RUNTIME = ROOT / ".cm2-runtime"
    SELF = ROOT / LAUNCHER_RELATIVE
    V3_OFFICIAL_REJECTION = RUNTIME / (
        "c79g-v3-rejections-" + CHECKPOINT + "/rejection.json")
    V4_REJECTION_SUPERSESSION = OUT / (
        BASE + "_v4_rejection_supersession_receipt_v1.json")
    V5_OFFICIAL_REJECTION = RUNTIME / (
        "c79g-v5-rejections-" + CHECKPOINT + "/rejection.json")
    V6_REJECTION_NAMESPACE = RUNTIME / ("c79g-v6-rejections-" + CHECKPOINT)
    V6_LATER_REJECTION = V6_REJECTION_NAMESPACE / "rejection.json"
    SCHEMA = OUT / (BASE + "_schema_v6.json")
    CONTRACT = OUT / (BASE + "_contract_v6.json")
    PRODUCER = OUT / (BASE + "_v6.py")
    CONSUMER = OUT / (BASE + "_independent_verifier_assembler_authority_consumer_v6.py")
    TRANSITION = OUT / (BASE + "_v5_to_v6_static_launch_transition_receipt_v1.json")
    AUDIT = OUT / (BASE + "_static_audit_v6.json")
    MANIFEST = OUT / (BASE + "_cold_launch_manifest_v6.sha256")
    OUTER = OUT / (BASE + "_cold_launch_outer_receipt_v6.json")
    BASE7_PINS = {
        V5_OFFICIAL_REJECTION:
            (V5_REJECTION_FILE_PIN, V5_REJECTION_OBJECT_PIN),
        SCHEMA: ("250e27777e3ffdaf159a19c00ae683a4ef079f6e785f0b37d003a724099419bc", None),
        CONTRACT: ("6e4f7f4693b759397c8775f8d943048c867b3c460c27f5cb3d9681a0fefee30c", "58ae6e3c9912294cc89b6804741e56b373a143d16a5fa2547325989fa1af2546"),
        PRODUCER: ("f48982effd6a1068c50260d0d419b281a3fa8c614e4ca76c3b8ee2a48e8afb56", None),
        CONSUMER: ("af4875d2ab84101b05eff9811f33d8bf7b1a060720a956ae3fb42d8d466f4775", None),
        TRANSITION: ("a6ac971e7efd9a6a80c7055449fb6c4ef02b77d3e8303324104a060618d45569", "edb97beae5ca5cfeff9e549c017892d6381d3b5a01be16b12e7e52e06d09c5e1"),
        AUDIT: ("f4f5b3ea2c289f388da9cc7d4181c0f1d6cf692aae0b85cbb17533ca4131f474", "2478b44d085336b87d13e309dc4416e58a85ef6ae28eb89cd787ea95b07c0449"),
    }
    EXACT8 = (V5_OFFICIAL_REJECTION, SCHEMA, CONTRACT, PRODUCER,
              CONSUMER, TRANSITION, AUDIT, SELF)
    V3_EXACT10_PINS = (
        (OUT / (BASE + "_v2_rejection_supersession_receipt_v1.json"),
         "fdd1921afda98a34c87ae20094e60fca1b75c8f233cf37890e7817fe35d82408",
         "518cbc5b30fc62d55291feef407c5677b880a05cb9a5b9f51404c79381c648fa"),
        (OUT / (BASE + "_schema_v3.json"),
         "275a86286480f915af69e18d81d7032140e3db6982d32679206a6a5b88fee036", None),
        (OUT / (BASE + "_contract_v3.json"),
         "ee2a969b5d3ae28dfc116fc24ab6bee6c3983d64db183641981108481c05ae7d",
         "fe82dcf80e8dd856390b694e8a286abc3087f33d0a2b4bebda1a01836b796a6b"),
        (OUT / (BASE + "_v3.py"),
         "587933a52505488fd87b1c4f99d5659df6f3c3e9557c0a77edd642e6e4dde0ab", None),
        (OUT / (BASE + "_independent_verifier_assembler_authority_consumer_v3.py"),
         "d66143d32f4c4257041f03e24e4a4da8f15542853b2a8f47fa39f5b72871bfdd", None),
        (OUT / (BASE + "_v2_to_v3_static_launch_transition_receipt_v1.json"),
         "d2c0a78db1ae19ccb21f068c4c4f9337220cabbf16721fdc15ed41825a6f3374",
         "fabe51379dc16bd4177d2116a43f2d1d5c103cc5a53f845fd5397eae0ea1c25b"),
        (OUT / (BASE + "_static_audit_v3.json"),
         "b7c3732296df713b6588527284983fab758e225c17c51fbc4a38b1f43da8aece",
         "2ef7588e66a83944fee0e2044177445f15b71fe030871ca96f354ce65dc8499a"),
        (OUT / (BASE + "_cold_launch_v3.py"),
         "63e1b04ce152770ce4bcfda826d418414fd3196ba540752d0bd61a97eec0075b", None),
        (OUT / (BASE + "_cold_launch_manifest_v3.sha256"),
         "53c97fc8f01f0dc0de3f7c5729d5940587467a1877ef9a7c96e9ea2403c0b028", None),
        (OUT / (BASE + "_cold_launch_outer_receipt_v3.json"),
         "692608ca777ca9ee625e2044bc71f694edf893f51953d7ff5662f29264d245ea",
         "450e1551a9f3cac2529bd202aa63ad28e4fd7e2ec4c7d7fb415883840ca0143d"),
    )
    V4_FROZEN_DRAFT7_PINS = (
        (OUT / (BASE + "_schema_v4.json"),
         "b2cb58e88b66daed7d0449d11a4441095179b7e537a48a35ee9c630f76beca6a", None),
        (OUT / (BASE + "_contract_v4.json"),
         "84608ada466fb9aa3d99adfd34662e9af02dfd009d8eb185374c065a6da0c23c",
         "62609ff0809ba9439be07a215ece772262f30ead7d87fda92a6e4e23bb5895b7"),
        (OUT / (BASE + "_v4.py"),
         "968e401852f45d5104f48526b50d4f59a86bb1fed8e7af23782c5f6d447d1cf1", None),
        (OUT / (BASE + "_independent_verifier_assembler_authority_consumer_v4.py"),
         "23753584725365cdc0174d518c26b7d8dbdeb12eea2345a5e3b281274548420c", None),
        (OUT / (BASE + "_v3_to_v4_static_launch_transition_receipt_v1.json"),
         "4c46f7cf8eaba93fd1b9562c288c2117b49d7c8cdeb62482b93c5e247d412256",
         "d2d0797a6edb8463f9af7007e28356932472f2e0478fb73b35869d3f51184129"),
        (OUT / (BASE + "_static_audit_v4.json"),
         "5efa44ae5cf78000940a4640a98ac0fe486e1946aecc9d20e7023e27ed13049c",
         "489a0aad575872e79dc264d5fc45cf2f12903c4c990f25d15a9cdd1448e980f4"),
        (OUT / (BASE + "_cold_launch_v4.py"),
         "04617c7ac60ad4cee278ac1b4c7d154fd130a3e2225a691ef9a75ad644a062a3", None),
    )
    V4_FORBIDDEN_RUNTIME_PATHS = (
        RUNTIME / ("c79g-v4-candidate-a-" + CHECKPOINT),
        RUNTIME / ("c79g-v4-candidate-b-" + CHECKPOINT),
        RUNTIME / ("c79g-v4-verification-a-" + CHECKPOINT),
        RUNTIME / ("c79g-v4-verification-b-" + CHECKPOINT),
        RUNTIME / ("c79g-v4-committed-completion-" + CHECKPOINT),
        RUNTIME / "cm2-global-authority-heads" /
            ("c79g-v4-" + CHECKPOINT + ".seal"),
        RUNTIME / ("c79g-v4-rejections-" + CHECKPOINT),
        RUNTIME / (".c79g-v4-candidate-stage-a-" + CHECKPOINT),
        RUNTIME / (".c79g-v4-candidate-stage-b-" + CHECKPOINT),
        RUNTIME / (".c79g-v4-verification-stage-a-" + CHECKPOINT),
        RUNTIME / (".c79g-v4-verification-stage-b-" + CHECKPOINT),
        RUNTIME / (".c79g-v4-completion-stage-" + CHECKPOINT),
        RUNTIME / "cm2-global-authority-heads" /
            (".c79g-v4-authority-stage-" + CHECKPOINT + ".seal"),
    )
    V5_EXACT10_PINS = (
        (V4_REJECTION_SUPERSESSION,
         V4_SUPERSESSION_FILE_PIN, V4_SUPERSESSION_OBJECT_PIN),
        (OUT / (BASE + "_schema_v5.json"),
         "1048740103257351abb1266ed91bb80028436cb1497918a0f0f177ec3268ff4f", None),
        (OUT / (BASE + "_contract_v5.json"),
         "162cd554ea972b434c019924a9ab8b87621ab65aae7d4896b6dac72d6288b997",
         "27d457a583f4d9892e0a866917ea4add25ff677669ee814861e0608036189377"),
        (OUT / (BASE + "_v5.py"),
         "bc6d48903f61257cd75b20b83c6cd369ca3748d19427cf18129c0fb9bb59e76e", None),
        (OUT / (BASE + "_independent_verifier_assembler_authority_consumer_v5.py"),
         "03aed000a94fc7b7d7e68d3c55611bcc55e7ce293f65ddfb3be7709e44fc854d", None),
        (OUT / (BASE + "_v4_to_v5_static_launch_transition_receipt_v1.json"),
         "6784668e91a4a4cc0812c6405cb1df8c10ad90e40daf321ac75c16cadd5cd715",
         "0678e3b81d5a4f6088967613df0cd585910b9b26800dfbf1724b637fc7c43526"),
        (OUT / (BASE + "_static_audit_v5.json"),
         "b852a41aaa992b85abec5f7139dc4669d2f1fe38bd79ab8ab812453c5cfca4f0",
         "ba9bf728ce08b795b5dd92191f2ccac3b2cfbc6ef7f7b919379feb6b9557e546"),
        (OUT / (BASE + "_cold_launch_v5.py"),
         "889775cfbe1d3cba597c85c28765545805710c99f06ad05673e57b7b7627bc54", None),
        (OUT / (BASE + "_cold_launch_manifest_v5.sha256"),
         "55336d5a95e1765cc0f229bbc98ddfb1f6c14218f5b5e619f84d19da39961474", None),
        (OUT / (BASE + "_cold_launch_outer_receipt_v5.json"),
         "71b7eaca4af58a34b70bb751044bd09d0e40352a1dc6f016a0c7618b6d4b4ab8",
         "57d5c31bf232d725e661932d2d210b31d1125cd0877a74a8167451bbbdaf0e1c"),
    )
    V5_FORBIDDEN_RUNTIME_PATHS = (
        RUNTIME / ("c79g-v5-candidate-a-" + CHECKPOINT),
        RUNTIME / ("c79g-v5-candidate-b-" + CHECKPOINT),
        RUNTIME / ("c79g-v5-verification-a-" + CHECKPOINT),
        RUNTIME / ("c79g-v5-verification-b-" + CHECKPOINT),
        RUNTIME / ("c79g-v5-committed-completion-" + CHECKPOINT),
        RUNTIME / "cm2-global-authority-heads" /
            ("c79g-v5-" + CHECKPOINT + ".seal"),
        RUNTIME / (".c79g-v5-candidate-stage-a-" + CHECKPOINT),
        RUNTIME / (".c79g-v5-candidate-stage-b-" + CHECKPOINT),
        RUNTIME / (".c79g-v5-verification-stage-a-" + CHECKPOINT),
        RUNTIME / (".c79g-v5-verification-stage-b-" + CHECKPOINT),
        RUNTIME / (".c79g-v5-completion-stage-" + CHECKPOINT),
        RUNTIME / "cm2-global-authority-heads" /
            (".c79g-v5-authority-stage-" + CHECKPOINT + ".seal"),
    )
INNER_SCHEMA = "cm2.round306c79g.true-global-no-producer-consumer.v6.inner-composite"
COLD_ROOT_SCHEMA = (
    "cm2.round306c79g.true-global-no-producer-consumer.v6."
    "cold-launched-committed-authority"
)
COLD_ROOT_DOMAIN = b"CM2_C79G_V6_COLD_LAUNCHED_AUTHORITY_ROOT_V1\0"
LIVE_PROTOCOL = "CM2_C79G_V6_COLD_TWO_PHASE_LIVE_ACK_V1"
LIVE_REQUEST_SCHEMA = (
    "cm2.round306c79g.true-global-no-producer-consumer.v6."
    "cold-live-commit-request"
)
LIVE_ACK_SCHEMA = (
    "cm2.round306c79g.true-global-no-producer-consumer.v6.cold-live-ack"
)
LIVE_RELEASE_SCHEMA = (
    "cm2.round306c79g.true-global-no-producer-consumer.v6.cold-live-release"
)
PREWRAPPER_BODY_DOMAIN = "CM2_C79G_V6_COLD_PREWRAPPER_BODY_V1"
TRANSACTION_BINDING_DOMAIN = "CM2_C79G_V6_COLD_TRANSACTION_BINDING_V1"
LIVE_ACK_BINDING_DOMAIN = "CM2_C79G_V6_COLD_LIVE_ACK_BINDING_V1"
SOURCE_FD_ENV = "CM2_C79G_V6_COLD_SOURCE_FD"
EXEC_FD_ENV = "CM2_C79G_V6_COLD_EXEC_FD"
COORDINATION_PARENT_FD_ENV = "CM2_C79G_V6_COORDINATION_PARENT_FD"
WORKSPACE_ROOT_ENV = "CM2_C79G_V6_COLD_WORKSPACE_ROOT"
WORKSPACE_ROOT_FD_ENV = "CM2_C79G_V6_COLD_WORKSPACE_ROOT_FD"
LAUNCHER_SHA_ENV = "CM2_C79G_V6_COLD_LAUNCHER_FILE_SHA256"


class Reject(RuntimeError):
    pass


def need(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise Reject(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def sha_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _nonzero_sha256(value: Any) -> bool:
    return (isinstance(value, str) and
            re.fullmatch(r"[0-9a-f]{64}", value) is not None and
            value != "0" * 64)


_STRICT_BOOL_CALL_NAMES = frozenset({
    "isinstance", "issubclass", "hasattr", "callable", "bool", "all", "any",
    "_static_freeze_is_valid", "_nonzero_sha256",
    "_no_zero_hash_placeholder", "_closed_object_equal",
})
_STRICT_BOOL_METHOD_NAMES = frozenset({
    "startswith", "endswith", "isascii", "isdecimal", "isdigit",
    "is_absolute", "is_symlink", "is_file", "is_dir", "exists",
    "isdisjoint", "issubset", "issuperset", "S_ISDIR", "S_ISREG",
    "S_ISFIFO", "get_blocking",
})


def _strict_bool_expression_is_proved(node: ast.AST) -> bool:
    """Conservative syntax proof for a strict-bool ``need`` condition."""
    if isinstance(node, ast.Compare):
        return True
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.Not):
        return True
    if isinstance(node, ast.BoolOp):
        return all(_strict_bool_expression_is_proved(item) for item in node.values)
    if isinstance(node, ast.Constant):
        return type(node.value) is bool
    if isinstance(node, ast.IfExp):
        return (_strict_bool_expression_is_proved(node.body) and
                _strict_bool_expression_is_proved(node.orelse))
    if isinstance(node, ast.Call):
        if isinstance(node.func, ast.Name):
            return node.func.id in _STRICT_BOOL_CALL_NAMES
        if isinstance(node.func, ast.Attribute):
            return node.func.attr in _STRICT_BOOL_METHOD_NAMES
    return False


def v5_strict_bool_regression(
        sources: Mapping[str, bytes]) -> dict[str, Any]:
    """Reproduce the frozen v5 700-call / 15-risk deterministic census."""
    ordered_roles = ("producer_v5", "consumer_v5", "launcher_v5")
    expected_need_counts = {
        "producer_v5": 217, "consumer_v5": 345, "launcher_v5": 138,
    }
    rows: list[dict[str, Any]] = []
    observed_need_counts: dict[str, int] = {}
    for role in ordered_roles:
        raw = sources.get(role)
        if not isinstance(raw, bytes):
            raise Reject("frozen v5 strict-bool source bytes:" + role)
        try:
            source = raw.decode("utf-8")
            tree = ast.parse(source, filename=role, mode="exec")
        except (UnicodeDecodeError, SyntaxError) as exc:
            raise Reject("frozen v5 strict-bool AST parse:" + role) from exc
        calls = [
            node for node in ast.walk(tree)
            if isinstance(node, ast.Call) and
               isinstance(node.func, ast.Name) and node.func.id == "need"
        ]
        observed_need_counts[role] = len(calls)
        for call in calls:
            if (len(call.args) != 2 or call.keywords or
                    any(isinstance(item, ast.Starred) for item in call.args)):
                raise Reject("frozen v5 need arity/star/keyword:" + role)
            condition = call.args[0]
            if not _strict_bool_expression_is_proved(condition):
                segment = ast.get_source_segment(source, condition)
                if not isinstance(segment, str):
                    raise Reject("frozen v5 need source segment:" + role)
                rows.append({
                    "role": role,
                    "line": call.lineno,
                    "column": call.col_offset,
                    "condition": segment.replace("\n", " "),
                    "condition_ast": ast.dump(
                        condition, annotate_fields=True,
                        include_attributes=False),
                })
    role_order = {role: index for index, role in enumerate(ordered_roles)}
    rows.sort(key=lambda row: (
        role_order[row["role"]], row["line"], row["column"]))
    risk_id_by_callsite = {
        ("launcher_v5", 1677): V5_STRICT_BOOL_RISK_IDS[0],
        ("launcher_v5", 1682): V5_STRICT_BOOL_RISK_IDS[1],
        ("consumer_v5", 3740): V5_STRICT_BOOL_RISK_IDS[2],
        ("producer_v5", 510): V5_STRICT_BOOL_RISK_IDS[3],
        ("consumer_v5", 894): V5_STRICT_BOOL_RISK_IDS[4],
        ("launcher_v5", 317): V5_STRICT_BOOL_RISK_IDS[5],
        ("launcher_v5", 324): V5_STRICT_BOOL_RISK_IDS[6],
    }
    hard_callsite_set = {
        ("consumer_v5", 3740),
        ("launcher_v5", 1677),
        ("launcher_v5", 1682),
    }
    observed_hard = {
        (row["role"], row["line"]) for row in rows
        if (row["role"], row["line"]) in hard_callsite_set
    }
    observed_risk_id_set = {
        risk_id_by_callsite[(row["role"], row["line"])]
        for row in rows
        if (row["role"], row["line"]) in risk_id_by_callsite
    }
    result = {
        "need_call_count": sum(observed_need_counts.values()),
        "need_call_count_by_role": observed_need_counts,
        "arity_star_keyword_failure_count": 0,
        "strict_bool_unproved_count": len(rows),
        "strict_bool_risk_count": len(observed_risk_id_set),
        "ordered_strict_bool_risk_ids": list(V5_STRICT_BOOL_RISK_IDS),
        "ordered_strict_bool_risk_id_sha256": sha_bytes(
            canonical(list(V5_STRICT_BOOL_RISK_IDS))),
        "definite_truthy_nonbool_hard_callsite_count": len(observed_hard),
        "definite_truthy_nonbool_hard_callsites": sorted(observed_hard),
        "ordered_census_sha256": sha_bytes(canonical(rows)),
    }
    need(observed_need_counts == expected_need_counts and
         result["need_call_count"] == 700 and
         result["strict_bool_unproved_count"] == 15 and
         result["strict_bool_risk_count"] == 7 and
         observed_risk_id_set == set(V5_STRICT_BOOL_RISK_IDS) and
         result["ordered_strict_bool_risk_id_sha256"] ==
             V5_STRICT_BOOL_RISK_ID_ORDER_SHA256 and
         observed_hard == hard_callsite_set and
         result["ordered_census_sha256"] ==
             V5_STRICT_BOOL_UNPROVED_CENSUS_SHA256,
         "frozen v5 strict-bool 700/7-risk/three-hard census")
    return result


def expected_v5_published_rejected_segment() -> dict[str, Any]:
    """Construct the one exact v5 regression shape shared by v6 proofs."""
    names = (
        "v4_rejection_supersession", "closed_schema", "contract",
        "build_only_producer", "independent_consumer", "v4_to_v5_transition",
        "static_audit", "cold_launcher", "cold_manifest", "cold_outer",
    )
    ordered: list[dict[str, Any]] = []
    for name, (path, file_pin, object_pin) in zip(
            names, V5_EXACT10_PINS, strict=True):
        member: dict[str, Any] = {
            "name": name,
            "path": str(path.relative_to(ROOT)),
            "file_sha256": file_pin,
        }
        if object_pin is not None:
            member["object_sha256"] = object_pin
        ordered.append(member)
    return {
        "ordered_published_exact10": ordered,
        "official_later_rejection": {
            "path": str(V5_OFFICIAL_REJECTION.relative_to(ROOT)),
            "namespace_path": str(V5_OFFICIAL_REJECTION.parent.relative_to(ROOT)),
            "file_sha256": V5_REJECTION_FILE_PIN,
            "object_sha256": V5_REJECTION_OBJECT_PIN,
            "schema": (
                "cm2.round306c79g.true-global-no-producer-consumer.v5."
                "later-rejection"),
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
            "D02_formal_pending_task_count": 33_638,
            "D02_started": False,
            "overwrite_delete_or_reuse_allowed": False,
        },
        "first_build_entry_attempt": {
            "attempted": True,
            "producer_child_spawned": False,
            "candidate_write_started": False,
            "positive_runtime_surface_count": 0,
        },
        "strict_bool_defect_census": {
            "direct_need_call_count": 700,
            "risk_count": 7,
            "hard_defect_count": 3,
            "ordered_risk_ids": list(V5_STRICT_BOOL_RISK_IDS),
            "all_seven_present_in_v5": True,
            "same_seven_absent_from_v6": True,
            "v6_recursive_exact_bool_unproved_count": 0,
        },
        "all_ten_file_pins_match": True,
        "all_declared_object_pins_match": True,
        "all_ten_regular_0444_nlink1": True,
        "exact8_manifest_reconstructs_first_eight_in_order": True,
        "outer_last_pins_manifest_and_launcher": True,
        "outer_then_rejection_chronology_validated": True,
        "v5_execution_allowed": False,
        "v5_runtime_surfaces_authoritative": False,
        "formal_global_closure_credit": 0,
        "D02_unlock": False,
        "D02_gate_credit": 0,
        "D02_task_credit": 0,
        "D02_formal_pending_task_count": 33_638,
        "D02_started": False,
    }


def validate_v5_published_rejected_segment(value: Any, label: str) -> None:
    expected = expected_v5_published_rejected_segment()
    need(isinstance(value, dict) and set(value) == set(expected) and
         value == expected,
         label + ":exact published exact10, rejection, first-attempt and "
         "strict-bool regression")


def validate_final_static_audit(
        audit: Mapping[str, Any], schema: Mapping[str, Any],
        schema_keywords: frozenset[str], held_by_path: Mapping[Path, "HeldFile"],
        base_objects: Mapping[Path, Mapping[str, Any]],
        predecessor_v5: "HeldV5PredecessorExact10") -> None:
    """Fail closed on every final dual-static GO claim before child spawn."""
    audit_keys = {
        "schema", "status", "audit_path", "effective_checkpoint_object_sha256",
        "audited_v6_bundle", "predecessor_v3_exact10_regression",
        "v3_official_later_rejection_regression",
        "predecessor_v4_rejection_supersession_regression",
        "published_then_officially_rejected_predecessor_v5",
        "dual_independent_static_checkers", "coherent_attack_static_census",
        "schema_and_constructor_closure",
        "sealed_exec_and_no_producer_static_proof", "static_credit_census",
        "static_no_run", "final_audit_acceptance", "object_sha256",
    }
    need(set(audit) == audit_keys and
         audit.get("schema") ==
             "cm2.round306c79g.true-global-no-producer-consumer.static-audit.v6" and
         audit.get("audit_path") == str(AUDIT.relative_to(ROOT)) and
         audit.get("effective_checkpoint_object_sha256") == CHECKPOINT and
         audit.get("status") ==
         "PASS_DUAL_STATIC_BYTES_GO_V6__PHYSICAL_COLD_FREEZE_PENDING__"
         "RUNTIME_NOT_AUTHORIZED",
         "final static audit exact top-level closure and PASS_V6 status")

    dual = audit.get("dual_independent_static_checkers")
    dual_keys = {
        "checker_A", "checker_B", "checker_C_common_census_reproduction",
        "independent_normalizer_count", "all_normalizers_equal",
        "independent_common_callsite_implementation_count",
        "all_common_callsite_censuses_equal",
        "final_launcher_must_reproduce_normalized_digest_after_pin_injection",
    }
    need(isinstance(dual, dict) and set(dual) == dual_keys,
         "final static audit exact dual-checker wrapper")
    checker_a = dual.get("checker_A")
    checker_b = dual.get("checker_B")
    checker_c = dual.get("checker_C_common_census_reproduction")
    checker_a_keys = {
        "algorithm", "status", "input_sha256",
        "normalized_launcher_template_sha256",
        "wider_local_callsite_census_row_count",
        "wider_local_callsite_census_sha256", "arity_failure_count",
        "undefined_global_count", "python_literal_dict_count",
        "python_literal_dict_duplicate_key_count",
        "python_AST_and_compile_in_memory_file_count",
        "failed_static_check_count",
    }
    checker_b_keys = {
        "algorithm", "status", "input_sha256",
        "normalized_launcher_template_sha256",
        "common_ordered_callsite_row_count",
        "common_ordered_callsite_census_sha256", "arity_failure_count",
        "starred_positional_total", "double_star_keyword_total",
        "undefined_global_count", "JSON_duplicate_key_count",
        "python_literal_dict_duplicate_key_count",
        "object_closure_failure_count", "pin_failure_count",
        "failed_static_check_count",
    }
    checker_c_keys = {
        "algorithm", "status", "normalized_launcher_template_sha256",
        "common_ordered_callsite_row_count",
        "common_ordered_callsite_census_sha256",
        "common_callsite_kind_census", "arity_failure_count",
        "starred_positional_total", "double_star_keyword_total",
        "failed_static_check_count",
    }
    need(isinstance(checker_a, dict) and set(checker_a) == checker_a_keys and
         isinstance(checker_b, dict) and set(checker_b) == checker_b_keys and
         isinstance(checker_c, dict) and set(checker_c) == checker_c_keys,
         "final static audit exact A/B/C checker objects")
    need(checker_a.get("algorithm") ==
             "AST_SYMBOL_TABLE_DATAFLOW_CHECKER_A_V1" and
         checker_a.get("status") ==
             "GO_STATIC_CHECKER_A__FINAL_PIN_INJECTION_PENDING__"
             "RUNTIME_NOT_AUTHORIZED" and
         checker_b.get("algorithm") ==
             "TOKEN_SYMBOL_TABLE_EXPLICIT_JSON_WALKER_CHECKER_B_V1" and
         checker_b.get("status") ==
             "GO_STATIC_CHECKER_B__FINAL_PIN_INJECTION_PENDING__"
             "RUNTIME_NOT_AUTHORIZED" and
         checker_c.get("algorithm") ==
             "INDEPENDENT_LEXICAL_CALLSITE_AND_NORMALIZED_AST_REPRODUCER_C_V1" and
         checker_c.get("status") ==
             "GO_COMMON_DIGEST_REPRODUCED__RUNTIME_NOT_AUTHORIZED",
         "final static audit exact independent checker GO statuses")

    input_keys = {
        "schema", "contract_file", "contract_object", "producer", "consumer",
        "transition_file", "transition_object", "launcher_template",
        "v4_supersession_file", "v4_supersession_object",
        "v5_rejection_file", "v5_rejection_object",
    }
    input_a = checker_a.get("input_sha256")
    input_b = checker_b.get("input_sha256")
    need(isinstance(input_a, dict) and set(input_a) == input_keys and
         isinstance(input_b, dict) and set(input_b) == input_keys and
         input_a == input_b and _nonzero_sha256(input_a.get("launcher_template")),
         "final static audit exact equal twelve-pin A/B input census")
    expected_inputs = {
        "schema": held_by_path[SCHEMA].file_sha256,
        "contract_file": held_by_path[CONTRACT].file_sha256,
        "contract_object": base_objects[CONTRACT]["object_sha256"],
        "producer": held_by_path[PRODUCER].file_sha256,
        "consumer": held_by_path[CONSUMER].file_sha256,
        "transition_file": held_by_path[TRANSITION].file_sha256,
        "transition_object": base_objects[TRANSITION]["object_sha256"],
        "v4_supersession_file":
            predecessor_v5.by_path[V4_REJECTION_SUPERSESSION].file_sha256,
        "v4_supersession_object": V4_SUPERSESSION_OBJECT_PIN,
        "v5_rejection_file": held_by_path[V5_OFFICIAL_REJECTION].file_sha256,
        "v5_rejection_object": V5_REJECTION_OBJECT_PIN,
    }
    need(all(_nonzero_sha256(value) for value in input_a.values()) and
         all(input_a.get(key) == value for key, value in expected_inputs.items()),
         "final static audit A/B pins equal live held files and object closures")

    normalized = checker_a.get("normalized_launcher_template_sha256")
    common_count = checker_b.get("common_ordered_callsite_row_count")
    common_digest = checker_b.get("common_ordered_callsite_census_sha256")
    zero_a = {
        "arity_failure_count", "undefined_global_count",
        "python_literal_dict_duplicate_key_count", "failed_static_check_count",
    }
    zero_b = {
        "arity_failure_count", "starred_positional_total",
        "double_star_keyword_total", "undefined_global_count",
        "JSON_duplicate_key_count", "python_literal_dict_duplicate_key_count",
        "object_closure_failure_count", "pin_failure_count",
        "failed_static_check_count",
    }
    zero_c = {
        "arity_failure_count", "starred_positional_total",
        "double_star_keyword_total", "failed_static_check_count",
    }
    need(_nonzero_sha256(normalized) and
         checker_b.get("normalized_launcher_template_sha256") == normalized and
         checker_c.get("normalized_launcher_template_sha256") == normalized and
         type(checker_a.get("wider_local_callsite_census_row_count")) is int and
         checker_a.get("wider_local_callsite_census_row_count") > 0 and
         _nonzero_sha256(checker_a.get("wider_local_callsite_census_sha256")) and
         type(checker_a.get("python_literal_dict_count")) is int and
         checker_a.get("python_literal_dict_count") > 0 and
         type(checker_a.get("python_AST_and_compile_in_memory_file_count")) is int and
         checker_a.get("python_AST_and_compile_in_memory_file_count") == 3 and
         all(type(checker_a.get(key)) is int and checker_a.get(key) == 0
             for key in zero_a) and
         type(common_count) is int and common_count > 0 and
         _nonzero_sha256(common_digest) and
         checker_c.get("common_ordered_callsite_row_count") == common_count and
         checker_c.get("common_ordered_callsite_census_sha256") == common_digest and
         all(type(checker_b.get(key)) is int and checker_b.get(key) == 0
             for key in zero_b) and
         all(type(checker_c.get(key)) is int and checker_c.get(key) == 0
             for key in zero_c),
         "final static audit digest consensus and exact zero-failure censuses")
    kind_census = checker_c.get("common_callsite_kind_census")
    kind_keys = {
        "module_function", "module_constructor", "self_instance_method",
        "cls_class_method", "localclass_static_method",
        "localclass_class_method", "localclass_instance_method",
    }
    need(isinstance(kind_census, dict) and set(kind_census) == kind_keys and
         all(type(value) is int and value >= 0 for value in kind_census.values()) and
         sum(kind_census.values()) == common_count and
         type(dual.get("independent_normalizer_count")) is int and
         dual.get("independent_normalizer_count") == 3 and
         dual.get("all_normalizers_equal") is True and
         type(dual.get("independent_common_callsite_implementation_count")) is int and
         dual.get("independent_common_callsite_implementation_count") == 2 and
         dual.get("all_common_callsite_censuses_equal") is True and
         dual.get(
             "final_launcher_must_reproduce_normalized_digest_after_pin_injection") is True,
         "final static audit exact independent normalizer and callsite consensus")

    attack = audit.get("coherent_attack_static_census")
    attack_keys = {
        "exact_unique_ordered_attack_count_required",
        "exact_unique_ordered_attack_count_observed", "attack_name_order_sha256",
        "all_mutations_route_through_production_validators",
        "C42_full10_hash_join_mutations_included",
        "C42_three_directory_mode_nlink_universe_guards_are_independent_live_physical_gates",
        "attack_execution_deferred_to_cold_runtime",
    }
    need(isinstance(attack, dict) and set(attack) == attack_keys and
         type(attack.get("exact_unique_ordered_attack_count_required")) is int and
         attack.get("exact_unique_ordered_attack_count_required") == 121 and
         type(attack.get("exact_unique_ordered_attack_count_observed")) is int and
         attack.get("exact_unique_ordered_attack_count_observed") == 121 and
         attack.get("attack_name_order_sha256") ==
             "6ba54c7d1847d960cbbd43d0863779e3fb2a2adf7663100936f185a6ce21d01a" and
         attack.get("all_mutations_route_through_production_validators") is True and
         attack.get("C42_full10_hash_join_mutations_included") is True and
         attack.get(
             "C42_three_directory_mode_nlink_universe_guards_are_independent_live_physical_gates") is True and
         attack.get("attack_execution_deferred_to_cold_runtime") is True,
         "final static audit exact 121/121 coherent attack census")

    closure = audit.get("schema_and_constructor_closure")
    closure_keys = {
        "strict_JSON_duplicate_keys_rejected", "schema_definition_count",
        "schema_ref_count", "unresolved_schema_ref_count", "closed_object_count",
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
    }
    stack: list[Any] = [schema]
    schema_nodes: list[Mapping[str, Any]] = []
    while stack:
        node = stack.pop()
        if isinstance(node, dict):
            schema_nodes.append(node)
            stack.extend(node.values())
        elif isinstance(node, list):
            stack.extend(node)
    closed_nodes = [
        node for node in schema_nodes
        if node.get("type") == "object" and
           node.get("additionalProperties") is False
    ]
    closed_mismatch_count = sum(
        set(node.get("required", [])) != set(node.get("properties", {}))
        for node in closed_nodes)
    actual_keywords = sorted(schema_keywords)
    supported_keywords = sorted(SUPPORTED_SCHEMA_KEYWORDS)
    expected_shapes = {
        "selfIdentity": 33, "independentConsumerProof": 44,
        "staticFreezeProof": 48, "coldLaunchProof": 76,
        "laterRejection": 41, "producerSourceRegistry": 37,
        "liveRequest": 15, "liveACK": 32, "liveACKCensus": 24,
    }
    need(isinstance(closure, dict) and set(closure) == closure_keys and
         closure.get("strict_JSON_duplicate_keys_rejected") is True and
         type(closure.get("schema_definition_count")) is int and
         closure.get("schema_definition_count") == 37 ==
             len(schema.get("$defs", {})) and
         type(closure.get("schema_ref_count")) is int and
         closure.get("schema_ref_count") == 179 ==
             sum("$ref" in node for node in schema_nodes) and
         type(closure.get("unresolved_schema_ref_count")) is int and
         closure.get("unresolved_schema_ref_count") == 0 and
         type(closure.get("closed_object_count")) is int and
         closure.get("closed_object_count") == 43 == len(closed_nodes) and
         type(closure.get("closed_object_required_property_mismatch_count")) is int and
         closure.get("closed_object_required_property_mismatch_count") ==
             0 == closed_mismatch_count and
         closure.get("all_closed_object_required_sets_equal_property_sets") is True and
         closure.get("all_schema_refs_resolve") is True and
         closure.get("actual_schema_keyword_universe") == actual_keywords and
         closure.get("actual_schema_keyword_universe_sha256") ==
             sha_bytes(canonical(actual_keywords)) and
         closure.get("cold_launcher_supported_schema_keyword_universe") ==
             supported_keywords and
         closure.get("cold_launcher_supported_schema_keyword_universe_sha256") ==
             sha_bytes(canonical(supported_keywords)) and
         closure.get(
             "all_schema_validation_keywords_supported_by_cold_launcher") is True and
         type(closure.get("unknown_schema_validation_keyword_count")) is int and
         closure.get("unknown_schema_validation_keyword_count") == 0 and
         closure.get("oneOf_keyword_absent_after_pin_definition_split") is True and
         type(closure.get("python_literal_dict_duplicate_key_count")) is int and
         closure.get("python_literal_dict_duplicate_key_count") == 0 and
         type(closure.get("undefined_global_count")) is int and
         closure.get("undefined_global_count") == 0 and
         closure.get("output_shape_key_counts") == expected_shapes and
         closure.get(
             "launcher_and_consumer_laterRejection_key_sets_equal_schema") is True and
         closure.get("launcher_request_consumer_request_key_sets_equal") is True and
         closure.get(
             "consumer_ACK_launcher_ACK_key_sets_and_census_values_equal") is True,
         "final static audit exact schema, constructor and output-shape closure")

    acceptance = audit.get("final_audit_acceptance")
    acceptance_keys = {
        "current_draft_pass", "final_failed_static_check_count_required",
        "final_static_freeze_pass_required", "dual_static_checker_A_GO",
        "dual_static_checker_B_GO", "normalized_launcher_digest_consensus",
        "common_callsite_census_digest_consensus",
        "final_launcher_normalized_digest_replay_required_after_pin_injection",
        "this_audit_authorizes_C79_runtime",
        "requires_cold_exact8_freeze_manifest_then_outer_last_and_terminal_replay",
    }
    need(isinstance(acceptance, dict) and set(acceptance) == acceptance_keys and
         acceptance.get("current_draft_pass") is True and
         type(acceptance.get("final_failed_static_check_count_required")) is int and
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
         "final static audit exact ten-key acceptance gate")

    no_run = audit.get("static_no_run")
    need(isinstance(no_run, dict) and set(no_run) == {
             "C79_entrypoint_executed", "C79_v6_runtime_artifact_count",
             "C79_v6_process_count", "pyc_or___pycache___created",
             "cold_manifest_or_outer_created_before_dual_GO",
         } and no_run.get("C79_entrypoint_executed") is False and
         type(no_run.get("C79_v6_runtime_artifact_count")) is int and
         no_run.get("C79_v6_runtime_artifact_count") == 0 and
         type(no_run.get("C79_v6_process_count")) is int and
         no_run.get("C79_v6_process_count") == 0 and
         no_run.get("pyc_or___pycache___created") is False and
         no_run.get("cold_manifest_or_outer_created_before_dual_GO") is False,
         "final static audit exact no-run attestation")


def close_object(value: dict[str, Any]) -> dict[str, Any]:
    need("object_sha256" not in value, "object closes exactly once")
    out = copy.deepcopy(value)
    out["object_sha256"] = sha_bytes(canonical(value))
    return out


def strict_json(raw: bytes, label: str) -> Any:
    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in items:
            need(key not in result, label + ":duplicate key:" + key)
            result[key] = value
        return result
    try:
        return json.loads(
            raw, object_pairs_hook=pairs,
            parse_constant=lambda token: (_ for _ in ()).throw(
                Reject(label + ":non-finite:" + token)))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise Reject(label + ":strict JSON") from exc


def verify_object(value: Mapping[str, Any], label: str,
                  expected: str | None = None) -> None:
    body = copy.deepcopy(dict(value))
    claim = body.pop("object_sha256", None)
    need(isinstance(claim, str) and claim == sha_bytes(canonical(body)),
         label + ":object closure")
    if expected is not None:
        need(claim == expected, label + ":object pin")


AT_EMPTY_PATH = 0x1000
AT_SYMLINK_NOFOLLOW = 0x100
STATX_BASIC_STATS = 0x000007ff
STATX_MNT_ID = 0x00001000
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


def _libc() -> ctypes.CDLL:
    need(sys.platform.startswith("linux"), "cold launcher is Linux fail-closed")
    library = ctypes.CDLL(None, use_errno=True)
    need(hasattr(library, "syscall") and hasattr(library, "statx"),
         "openat2 and statx required")
    return library


_ACTIVE_BOOTSTRAP: "HeldBootstrapEntry | None" = None


def _relative(path: Path) -> bytes:
    need(path.is_absolute() and path != ROOT and ROOT in path.parents,
         "exact absolute workspace descendant:" + str(path))
    relative = path.relative_to(ROOT)
    need(len(relative.parts) > 0 and
         all(part not in {"", ".", ".."} for part in relative.parts),
         "clean relative path:" + str(path))
    return os.fsencode(str(relative))


def openat2_from_root_fd(root_fd: int, relative: bytes,
                         flags: int = os.O_RDONLY) -> int:
    need(len(relative) > 0 and not relative.startswith(b"/") and
         b"\x00" not in relative and b".." not in relative.split(b"/"),
         "openat2 clean relative bytes")
    how = OpenHow(flags | os.O_CLOEXEC, 0,
                  RESOLVE_NO_XDEV | RESOLVE_NO_MAGICLINKS |
                  RESOLVE_NO_SYMLINKS | RESOLVE_BENEATH)
    ctypes.set_errno(0)
    descriptor = _libc().syscall(
        ctypes.c_long(437), ctypes.c_int(root_fd),
        ctypes.c_char_p(relative), ctypes.byref(how),
        ctypes.c_size_t(ctypes.sizeof(how)))
    if descriptor < 0:
        code = ctypes.get_errno()
        if code == errno.ENOENT:
            raise FileNotFoundError(code, os.strerror(code),
                                    os.fsdecode(relative))
        raise Reject("openat2 fail closed:" + os.fsdecode(relative) + ":" +
                     os.strerror(code))
    return int(descriptor)


def openat2_beneath(path: Path, flags: int = os.O_RDONLY) -> int:
    need(_ACTIVE_BOOTSTRAP is not None,
         "workspace root fd activated before any openat2")
    return openat2_from_root_fd(_ACTIVE_BOOTSTRAP.root_fd, _relative(path), flags)


def root_lstat(path: Path) -> os.stat_result:
    need(_ACTIVE_BOOTSTRAP is not None,
         "workspace root fd activated before any statat")
    descriptor = openat2_beneath(
        path, getattr(os, "O_PATH", os.O_RDONLY) |
        getattr(os, "O_NOFOLLOW", 0))
    try:
        return os.fstat(descriptor)
    finally:
        os.close(descriptor)


def root_absent(path: Path, label: str) -> None:
    try:
        root_lstat(path)
    except FileNotFoundError:
        return
    raise Reject(label + ":must remain absent")


def mount_id(fd: int) -> int:
    info = Statx()
    ctypes.set_errno(0)
    outcome = _libc().statx(
        ctypes.c_int(fd), ctypes.c_char_p(b""),
        ctypes.c_int(AT_EMPTY_PATH | AT_SYMLINK_NOFOLLOW),
        ctypes.c_uint(STATX_BASIC_STATS | STATX_MNT_ID), ctypes.byref(info))
    if outcome != 0:
        code = ctypes.get_errno()
        raise Reject("statx fail closed:" + os.strerror(code))
    need(bool(info.stx_mask & STATX_MNT_ID), "statx mount id unavailable")
    return int(info.stx_mnt_id)


def fingerprint(value: os.stat_result) -> tuple[int, ...]:
    return (value.st_dev, value.st_ino, value.st_mode, value.st_nlink,
            value.st_size, value.st_mtime_ns, value.st_ctime_ns)


def cold_publication_chronology(
        exact8: list[os.stat_result], manifest: os.stat_result,
        outer: os.stat_result) -> dict[str, bool]:
    """Prove final chmod/freeze order, not merely content-write mtime order."""
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


def directory_identity(value: os.stat_result) -> tuple[int, int, int]:
    return (value.st_dev, value.st_ino, value.st_mode)


F_GET_SEALS = getattr(fcntl, "F_GET_SEALS", 1034)
F_ADD_SEALS = getattr(fcntl, "F_ADD_SEALS", 1033)
F_SEAL_SEAL = getattr(fcntl, "F_SEAL_SEAL", 0x0001)
F_SEAL_SHRINK = getattr(fcntl, "F_SEAL_SHRINK", 0x0002)
F_SEAL_GROW = getattr(fcntl, "F_SEAL_GROW", 0x0004)
F_SEAL_WRITE = getattr(fcntl, "F_SEAL_WRITE", 0x0008)
REQUIRED_EXEC_SEALS = F_SEAL_SEAL | F_SEAL_SHRINK | F_SEAL_GROW | F_SEAL_WRITE
MFD_CLOEXEC = getattr(os, "MFD_CLOEXEC", 0x0001)
MFD_ALLOW_SEALING = getattr(os, "MFD_ALLOW_SEALING", 0x0002)


def read_fd(fd: int) -> bytes:
    os.lseek(fd, 0, os.SEEK_SET)
    chunks: list[bytes] = []
    while True:
        chunk = os.read(fd, 1 << 20)
        if not chunk:
            return b"".join(chunks)
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

    def __init__(self, exec_fd: int, source_fd: int, root_fd: int,
                 root_text: str, expected_sha256: str) -> None:
        need(sys.flags.isolated == 1 and sys.flags.dont_write_bytecode == 1 and
             sys.flags.no_site == 1,
             "sealed-fd launcher requires python3 -I -B -S")
        need(all(type(value) is int and value >= 3
                 for value in (exec_fd, source_fd, root_fd)) and
             len({exec_fd, source_fd, root_fd}) == 3,
             "three distinct inherited bootstrap descriptors")
        proc_path = "/proc/self/fd/" + str(exec_fd)
        need(sys.argv[0] == proc_path and os.path.abspath(__file__) == proc_path,
             "argv0 and __file__ are the inherited sealed exec fd")
        need(re.fullmatch(r"[0-9a-f]{64}", expected_sha256) is not None and
             expected_sha256 != "0" * 64,
             "caller-supplied external launcher SHA-256 anchor")
        need(root_text == os.path.abspath(root_text) and
             Path(root_text).is_absolute(),
             "bootstrap workspace root is an absolute normalized label")

        self.exec_fd = exec_fd
        self.source_fd = source_fd
        self.root_fd = root_fd
        self.root = Path(root_text)
        self.expected_sha256 = expected_sha256
        self.proc_path = proc_path
        self.exec_before = os.fstat(exec_fd)
        self.source_before = os.fstat(source_fd)
        self.root_before = os.fstat(root_fd)
        need(stat.S_ISREG(self.exec_before.st_mode) and
             stat.S_IMODE(self.exec_before.st_mode) == 0o444 and
             self.exec_before.st_nlink == 0,
             "sealed exec fd is anonymous regular 0444 nlink0")
        try:
            self.exec_seals = int(fcntl.fcntl(exec_fd, F_GET_SEALS))
        except OSError as exc:
            raise Reject("sealed exec fd exposes F_GET_SEALS") from exc
        need(self.exec_seals == REQUIRED_EXEC_SEALS,
             "exec memfd is permanently write/grow/shrink sealed")
        need(stat.S_ISREG(self.source_before.st_mode) and
             stat.S_IMODE(self.source_before.st_mode) == 0o444 and
             self.source_before.st_nlink == 1,
             "installed source fd regular 0444 nlink1")
        need(stat.S_ISDIR(self.root_before.st_mode),
             "inherited workspace root fd is a directory")
        self.root_mount_id = mount_id(root_fd)
        self.source_mount_id = mount_id(source_fd)
        self.exec_mount_id = mount_id(exec_fd)
        need(self.root_mount_id == self.source_mount_id,
             "installed launcher and workspace root share one mount")

        root_path_state = os.lstat(self.root)
        need(stat.S_ISDIR(root_path_state.st_mode) and
             directory_identity(root_path_state) ==
                 directory_identity(self.root_before),
             "workspace root label binds inherited root fd identity")
        installed_fd = openat2_from_root_fd(
            root_fd, os.fsencode(str(LAUNCHER_RELATIVE)), os.O_RDONLY)
        try:
            installed_before = os.fstat(installed_fd)
            installed_mount = mount_id(installed_fd)
            exec_raw = read_fd(exec_fd)
            exec_after = os.fstat(exec_fd)
            source_raw = read_fd(source_fd)
            source_after = os.fstat(source_fd)
            installed_raw = read_fd(installed_fd)
            installed_after = os.fstat(installed_fd)
            need(fingerprint(self.exec_before) == fingerprint(exec_after) and
                 fingerprint(self.source_before) == fingerprint(source_after) and
                 fingerprint(installed_before) == fingerprint(installed_after),
                 "bootstrap fd reads are identity bracketed")
            need((installed_before.st_dev, installed_before.st_ino) ==
                     (self.source_before.st_dev, self.source_before.st_ino) and
                 installed_mount == self.source_mount_id and
                 fingerprint(installed_before) == fingerprint(self.source_before),
                 "installed path is the inherited source inode")
            need(exec_raw == source_raw == installed_raw and
                 sha_bytes(exec_raw) == expected_sha256,
                 "sealed executed bytes equal installed externally pinned bytes")
            self.raw = exec_raw
        finally:
            os.close(installed_fd)

        global _ACTIVE_BOOTSTRAP
        need(_ACTIVE_BOOTSTRAP is None, "bootstrap root activates exactly once")
        configure_workspace_paths(self.root)
        _ACTIVE_BOOTSTRAP = self
        self.closed = False

    def held_launcher(self) -> "HeldFile":
        need(not self.closed, "bootstrap entry remains live")
        return HeldFile.from_existing_fd(
            SELF, "cold exact8:" + SELF.name, self.expected_sha256,
            self.source_fd)

    def terminal_replay(self) -> None:
        need(not self.closed, "bootstrap entry terminal replay while live")
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
            need(fingerprint(installed_before) == fingerprint(installed_after) and
                 (installed_before.st_dev, installed_before.st_ino) ==
                     (self.source_before.st_dev, self.source_before.st_ino) and
                 mount_id(installed_fd) == self.source_mount_id,
                 "terminal installed launcher identity")
        finally:
            os.close(installed_fd)
        need(directory_identity(root_path_state) == directory_identity(root_now) ==
                 directory_identity(self.root_before) and
             mount_id(self.root_fd) == self.root_mount_id and
             fingerprint(exec_before) == fingerprint(self.exec_before) ==
                 fingerprint(exec_after) and
             fingerprint(source_before) == fingerprint(self.source_before) ==
                 fingerprint(source_after) and
             fcntl.fcntl(self.exec_fd, F_GET_SEALS) == REQUIRED_EXEC_SEALS and
             exec_raw == source_raw == installed_raw == self.raw and
             sha_bytes(exec_raw) == self.expected_sha256,
             "terminal sealed-exec/source/root/path byte replay")

    def identity_object(self) -> dict[str, Any]:
        return {
            "external_static_file_anchor_sha256": self.expected_sha256,
            "executed_proc_fd_path": self.proc_path,
            "executed_sealed_memfd": True,
            "required_memfd_seals": REQUIRED_EXEC_SEALS,
            "installed_source_st_dev": self.source_before.st_dev,
            "installed_source_st_ino": self.source_before.st_ino,
            "installed_source_statx_mnt_id": self.source_mount_id,
            "workspace_root_st_dev": self.root_before.st_dev,
            "workspace_root_st_ino": self.root_before.st_ino,
            "workspace_root_statx_mnt_id": self.root_mount_id,
            "external_bootstrap_python_kernel_openat2_procfs_declared_TCB": True,
            "launcher_sha256_is_only_external_static_file_anchor_not_only_TCB": True,
        }

    def close(self) -> None:
        if self.closed:
            return
        self.closed = True
        for descriptor in (self.exec_fd, self.source_fd, self.root_fd):
            os.close(descriptor)


class HeldFile:
    def __init__(self, path: Path, label: str, expected: str | None = None,
                 inherited_fd: int | None = None) -> None:
        self.path = path
        self.label = label
        before_path = root_lstat(path)
        need(stat.S_ISREG(before_path.st_mode) and
             stat.S_IMODE(before_path.st_mode) == 0o444 and before_path.st_nlink == 1,
             label + ":regular 0444 nlink1")
        self.fd = (openat2_beneath(path) if inherited_fd is None
                   else os.dup(inherited_fd))
        try:
            self.before = os.fstat(self.fd)
            self.mount_id = mount_id(self.fd)
            need(directory_identity(before_path) == directory_identity(self.before),
                 label + ":initial path/fd identity")
            self.raw = self._read()
            after_fd = os.fstat(self.fd)
            after_path = root_lstat(path)
            need(fingerprint(before_path) == fingerprint(self.before) ==
                 fingerprint(after_fd) == fingerprint(after_path) and
                 mount_id(self.fd) == self.mount_id,
                 label + ":initial bracketed same-fd read")
            self.file_sha256 = sha_bytes(self.raw)
            if expected is not None:
                need(self.file_sha256 == expected, label + ":file pin")
        except BaseException:
            os.close(self.fd)
            self.fd = -1
            raise

    @classmethod
    def from_existing_fd(cls, path: Path, label: str, expected: str,
                         inherited_fd: int) -> "HeldFile":
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
                return b"".join(chunks)
            chunks.append(chunk)

    def terminal_replay(self) -> None:
        before_fd = os.fstat(self.fd)
        before_path = root_lstat(self.path)
        replay = self._read()
        after_fd = os.fstat(self.fd)
        after_path = root_lstat(self.path)
        need(replay == self.raw and
             fingerprint(before_fd) == fingerprint(before_path) ==
             fingerprint(self.before) == fingerprint(after_fd) ==
             fingerprint(after_path) and
             stat.S_ISREG(after_fd.st_mode) and
             stat.S_IMODE(after_fd.st_mode) == 0o444 and after_fd.st_nlink == 1 and
             mount_id(self.fd) == self.mount_id,
             self.label + ":terminal bracketed same-fd replay")

    def identity_object(self) -> dict[str, Any]:
        return {
            "path": str(self.path.relative_to(ROOT)),
            "file_sha256": self.file_sha256,
            "st_dev": self.before.st_dev,
            "st_ino": self.before.st_ino,
            "stx_mnt_id": self.mount_id,
            "st_size": self.before.st_size,
            "mode": "0444",
            "nlink": 1,
            "opened_by_exact_lexical_path_with_O_NOFOLLOW": True,
            "opened_with_openat2_RESOLVE_BENEATH_NO_SYMLINKS_NO_MAGICLINKS_NO_XDEV": True,
            "statx_mount_id_stable": True,
            "initial_fd_identity_equals_terminal_fd_identity": True,
            "initial_bytes_equal_terminal_same_fd_bytes": True,
            "terminal_fd_identity_equals_terminal_path_lstat_identity": True,
            "parent_components_securely_walked": True,
            "regular_file": True,
        }

    def close(self) -> None:
        if self.fd >= 0:
            os.close(self.fd)
            self.fd = -1


class HeldSealedChildExec:
    """Fresh immutable execution copy of one already-held exact8 source."""

    def __init__(self, source: HeldFile) -> None:
        need(hasattr(os, "memfd_create"),
             "Linux memfd_create required for sealed child execution")
        try:
            self.fd = os.memfd_create(
                "c79g-v6-child-exec", MFD_CLOEXEC | MFD_ALLOW_SEALING)
        except OSError as exc:
            raise Reject("fresh child exec memfd creation") from exc
        self.closed = False
        self.expected_raw = source.raw
        self.expected_sha256 = source.file_sha256
        try:
            view = memoryview(self.expected_raw)
            offset = 0
            while offset < len(view):
                written = os.write(self.fd, view[offset:])
                need(written > 0, "complete child exec memfd write")
                offset += written
            os.fsync(self.fd)
            os.fchmod(self.fd, 0o444)
            fcntl.fcntl(self.fd, F_ADD_SEALS, REQUIRED_EXEC_SEALS)
            self.before = os.fstat(self.fd)
            self.seals = int(fcntl.fcntl(self.fd, F_GET_SEALS))
            self.raw = read_fd(self.fd)
            after = os.fstat(self.fd)
            need(stat.S_ISREG(self.before.st_mode) and
                 stat.S_IMODE(self.before.st_mode) == 0o444 and
                 self.before.st_nlink == 0 and
                 self.seals == REQUIRED_EXEC_SEALS and
                 fingerprint(self.before) == fingerprint(after) and
                 self.raw == self.expected_raw and
                 sha_bytes(self.raw) == self.expected_sha256,
                 "fresh sealed child exec bytes, mode, link count, and seals")
        except BaseException:
            os.close(self.fd)
            self.fd = -1
            self.closed = True
            raise

    def terminal_replay(self) -> None:
        need(not self.closed and self.fd >= 3,
             "sealed child exec held through terminal replay")
        before = os.fstat(self.fd)
        replay = read_fd(self.fd)
        after = os.fstat(self.fd)
        seals = int(fcntl.fcntl(self.fd, F_GET_SEALS))
        need(fingerprint(before) == fingerprint(self.before) == fingerprint(after) and
             stat.S_IMODE(after.st_mode) == 0o444 and after.st_nlink == 0 and
             seals == REQUIRED_EXEC_SEALS and
             replay == self.expected_raw and sha_bytes(replay) == self.expected_sha256,
             "sealed child exec terminal byte/mode/seal replay")

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
        need(stat.S_ISDIR(before_path.st_mode),
             "coordination parent exact nonsymlink directory")
        self.fd = openat2_beneath(
            self.path, os.O_RDONLY | os.O_DIRECTORY)
        try:
            self.before = os.fstat(self.fd)
            self.mount_id = mount_id(self.fd)
            need(fingerprint(before_path) == fingerprint(self.before),
                 "coordination parent initial path/fd identity")
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
        need(self.lock_owned is True and
             stat.S_ISDIR(before_fd.st_mode) and stat.S_ISDIR(after_fd.st_mode) and
             directory_identity(before_fd) == directory_identity(before_path) ==
             directory_identity(self.before) == directory_identity(after_fd) ==
             directory_identity(after_path) and mount_id(self.fd) == self.mount_id,
             "launcher-owned coordination lock and parent identity stable")

    def identity_object(self) -> dict[str, Any]:
        return {
            "path": str(self.path.relative_to(ROOT)),
            "st_dev": self.before.st_dev,
            "st_ino": self.before.st_ino,
            "stx_mnt_id": self.mount_id,
            "directory": True,
            "opened_with_openat2_RESOLVE_BENEATH_NO_SYMLINKS_NO_MAGICLINKS_NO_XDEV": True,
            "launcher_owned_flock_LOCK_EX": self.lock_owned,
            "same_open_file_description_inherited_by_child": True,
            "lock_scope_is_mandatory_official_writer_protocol_only": True,
            "same_uid_bypass_is_not_claimed_prevented": True,
        }

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
        name = V6_REJECTION_NAMESPACE.name
        created_descriptor = -1
        self.fd = -1
        try:
            try:
                state = os.stat(name, dir_fd=coordination.fd,
                                follow_symlinks=False)
            except FileNotFoundError:
                os.mkdir(name, 0o555, dir_fd=coordination.fd)
                created_descriptor = os.open(
                    name, os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC |
                    getattr(os, "O_NOFOLLOW", 0), dir_fd=coordination.fd)
                os.fchmod(created_descriptor, 0o555)
                os.fsync(created_descriptor)
                os.fsync(coordination.fd)
                state = os.stat(name, dir_fd=coordination.fd,
                                follow_symlinks=False)
            self.path = V6_REJECTION_NAMESPACE
            self.fd = (created_descriptor if created_descriptor >= 0 else
                       openat2_beneath(
                           self.path, os.O_RDONLY | os.O_DIRECTORY))
            created_descriptor = -1
            self.before = os.fstat(self.fd)
            self.mount_id = mount_id(self.fd)
            path_before = root_lstat(self.path)
            first = set(os.listdir(self.fd))
            after = os.fstat(self.fd)
            path_after = root_lstat(self.path)
            second = set(os.listdir(self.fd))
            need(stat.S_ISDIR(state.st_mode) and
                 stat.S_IMODE(state.st_mode) == 0o555 and state.st_nlink == 2 and
                 fingerprint(state) == fingerprint(self.before) ==
                     fingerprint(path_before) == fingerprint(after) ==
                     fingerprint(path_after) and
                 first == second == set() and
                 self.mount_id == coordination.mount_id,
                 "launcher permanent-rejection namespace exact empty sealed state")
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
        need(fingerprint(before) == fingerprint(path_before) ==
             fingerprint(self.before) == fingerprint(after) ==
             fingerprint(path_after) and first == second == set() and
             stat.S_IMODE(after.st_mode) == 0o555 and after.st_nlink == 2 and
             mount_id(self.fd) == self.mount_id,
             "launcher rejection namespace terminal exact-empty replay")

    def close(self) -> None:
        if self.fd >= 0:
            os.close(self.fd)
            self.fd = -1


def stable_official_writer_lock_policy() -> dict[str, Any]:
    """Return the reboot-stable lock policy without persisting live identity."""
    return {
        "path": ".cm2-runtime",
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


def reconstruct_unopened_publication_hashes(
        bootstrap: HeldBootstrapEntry) -> tuple[str, str, str]:
    """Rebuild final manifest/outer hashes from final pins without opening them."""
    need(FINAL_BASE7_PINS_INSTALLED is True and len(BASE7_PINS) == 7 and
         EXACT8 == (V5_OFFICIAL_REJECTION, SCHEMA, CONTRACT, PRODUCER,
                    CONSUMER, TRANSITION, AUDIT, SELF),
         "launcher-native rejection requires final acyclic base7 pins")
    entries: list[dict[str, str]] = []
    for path in EXACT8:
        file_pin = (bootstrap.expected_sha256 if path == SELF
                    else BASE7_PINS[path][0])
        need(re.fullmatch(r"[0-9a-f]{64}", file_pin) is not None and
             file_pin not in {_DRAFT_FILE_PIN, "0" * 64},
             "launcher-native rejection exact8 final file pin")
        entries.append({"path": str(path.relative_to(ROOT)),
                        "file_sha256": file_pin})
    manifest_raw = b"".join(
        f"{entry['file_sha256']}  {entry['path']}\n".encode("ascii")
        for entry in entries)
    manifest_sha256 = sha_bytes(manifest_raw)
    outer = close_object({
        "schema": (
            "cm2.round306c79g.true-global-no-producer-consumer."
            "cold-launch-outer-receipt.v6"),
        "status": (
            "FROZEN_COLD_LAUNCH_OUTER_LAST__EXACT8_MANIFEST_CLOSED__"
            "RUNTIME_DEFERRED"),
        "effective_checkpoint_object_sha256": CHECKPOINT,
        "exact8_ordered_entries": entries,
        "cold_launch_manifest": {
            "path": str(MANIFEST.relative_to(ROOT)),
            "file_sha256": manifest_sha256,
            "ordered_entry_count": 8,
        },
        "cold_launcher": {
            "path": str(SELF.relative_to(ROOT)),
            "file_sha256": bootstrap.expected_sha256,
        },
        "all_exact8_regular_0444_nlink1_and_held_for_runtime": True,
        "outer_published_after_exact8_manifest": True,
        "runtime_entry_must_be_cold_launcher": True,
        "sole_external_static_file_anchor_is_launcher_sha256": True,
        "declared_external_tcb": [
            "EXTERNAL_HELD_FD_SEALED_MEMFD_BOOTSTRAP",
            "PYTHON3_ISOLATED_INTERPRETER",
            "LINUX_KERNEL_OPENAT2_STATX_MEMFD_PROCFS",
        ],
        "formal_global_closure_credit": 0,
        "D02_unlock": False,
        "runtime_executed_during_static_freeze": False,
    })
    outer_raw = canonical(outer) + b"\n"
    return manifest_sha256, sha_bytes(outer_raw), outer["object_sha256"]


def construct_launcher_native_rejection(
        bootstrap: HeldBootstrapEntry) -> dict[str, Any]:
    """Return the exact closed-schema rejection without opening the bundle."""
    manifest_sha256, outer_file_sha256, outer_object_sha256 = (
        reconstruct_unopened_publication_hashes(bootstrap))
    return close_object({
        "schema": (
            "cm2.round306c79g.true-global-no-producer-consumer.v6."
            "later-rejection"),
        "status": "PERMANENT_FAIL_CLOSED_REJECTION__ZERO_CREDIT",
        "effective_checkpoint_object_sha256": CHECKPOINT,
        "namespace_exact_path": str(V6_REJECTION_NAMESPACE.relative_to(ROOT)),
        "target_exact_path": str(V6_LATER_REJECTION.relative_to(ROOT)),
        "rejection_reason": "ORPHANED_OR_INCOMPLETE_C79G_V6_SURFACE",
        "consumer_file_sha256": BASE7_PINS[CONSUMER][0],
        "producer_file_sha256": BASE7_PINS[PRODUCER][0],
        "contract_file_sha256": BASE7_PINS[CONTRACT][0],
        "contract_object_sha256": BASE7_PINS[CONTRACT][1],
        "closed_schema_file_sha256": BASE7_PINS[SCHEMA][0],
        "v5_official_rejection_file_sha256": V5_REJECTION_FILE_PIN,
        "v5_official_rejection_object_sha256": V5_REJECTION_OBJECT_PIN,
        "v4_rejection_supersession_file_sha256": V4_SUPERSESSION_FILE_PIN,
        "v4_rejection_supersession_object_sha256": V4_SUPERSESSION_OBJECT_PIN,
        "cold_launcher_file_sha256": bootstrap.expected_sha256,
        "cold_manifest_file_sha256": manifest_sha256,
        "cold_outer_file_sha256": outer_file_sha256,
        "cold_outer_object_sha256": outer_object_sha256,
        "official_writer_coordination_lock_policy":
            stable_official_writer_lock_policy(),
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
        "D02_formal_pending_task_count": 33_638,
        "D02_started": False,
    })


def _write_all(fd: int, raw: bytes) -> None:
    offset = 0
    while offset < len(raw):
        written = os.write(fd, raw[offset:])
        need(written > 0, "launcher-native rejection complete write")
        offset += written


def install_or_replay_launcher_native_rejection(
        bootstrap: HeldBootstrapEntry,
        coordination: HeldCoordinationParent) -> None:
    """Append the sole fixed rejection before opening any cold bundle file."""
    coordination.verify()
    expected = construct_launcher_native_rejection(bootstrap)
    expected_raw = canonical(expected) + b"\n"
    name = V6_REJECTION_NAMESPACE.name
    namespace_fd = -1
    try:
        try:
            state = os.stat(name, dir_fd=coordination.fd,
                            follow_symlinks=False)
        except FileNotFoundError:
            os.mkdir(name, 0o555, dir_fd=coordination.fd)
            namespace_fd = os.open(
                name, os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC |
                getattr(os, "O_NOFOLLOW", 0), dir_fd=coordination.fd)
            os.fchmod(namespace_fd, 0o555)
            os.fsync(namespace_fd)
            os.fsync(coordination.fd)
            state = os.fstat(namespace_fd)
        else:
            namespace_fd = openat2_beneath(
                V6_REJECTION_NAMESPACE, os.O_RDONLY | os.O_DIRECTORY)
    except BaseException:
        if namespace_fd >= 0:
            os.close(namespace_fd)
        raise
    rejection_guard: HeldFile | None = None
    try:
        before = os.fstat(namespace_fd)
        path_before = root_lstat(V6_REJECTION_NAMESPACE)
        universe = set(os.listdir(namespace_fd))
        need(stat.S_ISDIR(state.st_mode) and
             fingerprint(state) == fingerprint(before) == fingerprint(path_before) and
             stat.S_IMODE(before.st_mode) == 0o555 and before.st_nlink == 2 and
             mount_id(namespace_fd) == coordination.mount_id,
             "launcher-native rejection namespace sealed before append")
        target = os.stat(V6_LATER_REJECTION.name, dir_fd=namespace_fd,
                         follow_symlinks=False) if V6_LATER_REJECTION.name in universe else None
        if target is not None:
            need(universe == {V6_LATER_REJECTION.name},
                 "idempotent rejection exact singleton")
            rejection_guard = HeldFile(
                V6_LATER_REJECTION, "existing launcher-native v6 rejection")
        else:
            need(not universe, "first rejection append requires exact empty namespace")
            os.fchmod(namespace_fd, 0o755)
            os.fsync(namespace_fd)
            need(stat.S_IMODE(os.fstat(namespace_fd).st_mode) == 0o755,
                 "launcher-native rejection exact write-window mode")
            writer = -1
            try:
                writer = os.open(
                    V6_LATER_REJECTION.name,
                    os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_CLOEXEC |
                    getattr(os, "O_NOFOLLOW", 0), 0o600, dir_fd=namespace_fd)
                _write_all(writer, expected_raw)
                os.fsync(writer)
                os.fchmod(writer, 0o444)
                os.fsync(writer)
            finally:
                if writer >= 0:
                    os.close(writer)
                os.fchmod(namespace_fd, 0o555)
                os.fsync(namespace_fd)
            rejection_guard = HeldFile(
                V6_LATER_REJECTION, "new launcher-native v6 rejection")
        need(rejection_guard is not None,
             "launcher-native rejection file held")
        value = strict_json(rejection_guard.raw, "launcher-native v6 rejection")
        need(isinstance(value, dict), "launcher-native rejection mapping")
        verify_object(value, "launcher-native v6 rejection")
        os.fsync(rejection_guard.fd)
        os.fsync(namespace_fd)
        os.fsync(coordination.fd)
        after = os.fstat(namespace_fd)
        path_after = root_lstat(V6_REJECTION_NAMESPACE)
        need(value == expected and rejection_guard.raw == expected_raw and
             set(os.listdir(namespace_fd)) == {V6_LATER_REJECTION.name} and
             fingerprint(after) == fingerprint(path_after) and
             stat.S_IMODE(after.st_mode) == 0o555 and after.st_nlink == 2,
             "launcher-native rejection durable exact singleton")
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

    def __init__(self, coordination: HeldCoordinationParent,
                 rejection: HeldFile) -> None:
        coordination.verify()
        self.path = V3_OFFICIAL_REJECTION.parent
        self.fd = -1
        self.fd = openat2_beneath(self.path, os.O_RDONLY | os.O_DIRECTORY)
        try:
            self.before = os.fstat(self.fd)
            self.mount_id = mount_id(self.fd)
            before_path = root_lstat(self.path)
            first = set(os.listdir(self.fd))
            member = os.stat(V3_OFFICIAL_REJECTION.name, dir_fd=self.fd,
                             follow_symlinks=False)
            after = os.fstat(self.fd)
            after_path = root_lstat(self.path)
            second = set(os.listdir(self.fd))
            need(stat.S_ISDIR(self.before.st_mode) and
                 stat.S_IMODE(self.before.st_mode) == 0o555 and
                 self.before.st_nlink == 2 and
                 fingerprint(before_path) == fingerprint(self.before) ==
                     fingerprint(after) == fingerprint(after_path) and
                 first == second == {V3_OFFICIAL_REJECTION.name} and
                 (member.st_dev, member.st_ino) == rejection.identity and
                 self.mount_id == rejection.mount_id == coordination.mount_id,
                 "official v3 rejection exact singleton namespace held under lock")
        except BaseException:
            os.close(self.fd)
            self.fd = -1
            raise

    def terminal_replay(self, rejection: HeldFile) -> None:
        before = os.fstat(self.fd)
        before_path = root_lstat(self.path)
        first = set(os.listdir(self.fd))
        member = os.stat(V3_OFFICIAL_REJECTION.name, dir_fd=self.fd,
                         follow_symlinks=False)
        after = os.fstat(self.fd)
        after_path = root_lstat(self.path)
        second = set(os.listdir(self.fd))
        need(fingerprint(before) == fingerprint(before_path) ==
             fingerprint(self.before) == fingerprint(after) ==
             fingerprint(after_path) and
             first == second == {V3_OFFICIAL_REJECTION.name} and
             stat.S_IMODE(after.st_mode) == 0o555 and after.st_nlink == 2 and
             (member.st_dev, member.st_ino) == rejection.identity and
             mount_id(self.fd) == self.mount_id,
             "official v3 rejection namespace terminal singleton replay")

    def close(self) -> None:
        if self.fd >= 0:
            os.close(self.fd)
            self.fd = -1


class HeldV3PredecessorExact10:
    """Live-replay the frozen v3 exact10 plus its official later rejection."""

    def __init__(self, coordination: HeldCoordinationParent,
                 rejection: HeldFile) -> None:
        coordination.verify()
        self.files: list[HeldFile] = []
        self.namespace: HeldV3RejectionNamespace | None = None
        try:
            for path, file_pin, _ in V3_EXACT10_PINS:
                self.files.append(HeldFile(
                    path, "frozen v3 exact10:" + path.name, file_pin))
            self.by_path = {item.path: item for item in self.files}
            need(len(self.by_path) == 10 and
                 len({item.identity for item in self.files}) == 10 and
                 len({item.mount_id for item in self.files}) == 1 and
                 next(iter({item.mount_id for item in self.files})) ==
                     coordination.mount_id == rejection.mount_id,
                 "frozen v3 exact10 unique live files on coordination mount")
            for path, _, object_pin in V3_EXACT10_PINS:
                if object_pin is not None:
                    value = strict_json(self.by_path[path].raw,
                                        "frozen v3 object:" + path.name)
                    need(isinstance(value, dict), "frozen v3 object mapping")
                    verify_object(value, "frozen v3 object:" + path.name,
                                  object_pin)
            expected_exact8 = [
                {"path": str(path.relative_to(ROOT)), "file_sha256": file_pin}
                for path, file_pin, _ in V3_EXACT10_PINS[:8]
            ]
            manifest = self.files[8]
            need(parse_manifest(manifest.raw) == expected_exact8,
                 "frozen v3 exact8 manifest reconstructed exactly")
            outer = strict_json(self.files[9].raw, "frozen v3 outer")
            need(isinstance(outer, dict) and
             outer.get("status") ==
                 "FROZEN_COLD_LAUNCH_OUTER_LAST__EXACT8_MANIFEST_CLOSED__RUNTIME_DEFERRED" and
             outer.get("effective_checkpoint_object_sha256") == CHECKPOINT and
             outer.get("exact8_ordered_entries") == expected_exact8 and
             outer.get("cold_launch_manifest", {}).get("file_sha256") ==
                 V3_EXACT10_PINS[8][1] and
             outer.get("cold_launcher", {}).get("file_sha256") ==
                 V3_EXACT10_PINS[7][1] and
             outer.get("formal_global_closure_credit") == 0 and
             outer.get("D02_unlock") is False and
             max(self.files[9].before.st_mtime_ns,
                 self.files[9].before.st_ctime_ns) <
                 min(rejection.before.st_mtime_ns,
                     rejection.before.st_ctime_ns),
                 "frozen v3 exact10 outer and strictly later rejection closure")
            rejected = strict_json(rejection.raw, "official v3 later rejection")
            need(isinstance(rejected, dict) and
             rejected.get("schema") ==
                 "cm2.round306c79g.true-global-no-producer-consumer.v3.later-rejection" and
             rejected.get("status") ==
                 "PERMANENT_FAIL_CLOSED_REJECTION__ZERO_CREDIT" and
             rejected.get("rejection_reason") ==
                 "ORPHANED_OR_INCOMPLETE_C79G_V3_SURFACE" and
             rejected.get("effective_checkpoint_object_sha256") == CHECKPOINT and
             rejected.get("target_exact_path") ==
                 str(V3_OFFICIAL_REJECTION.relative_to(ROOT)) and
             rejected.get("namespace_exact_path") ==
                 str(V3_OFFICIAL_REJECTION.parent.relative_to(ROOT)) and
             rejected.get("cold_launcher_file_sha256") ==
                 V3_EXACT10_PINS[7][1] and
             rejected.get("cold_manifest_file_sha256") ==
                 V3_EXACT10_PINS[8][1] and
             rejected.get("cold_outer_file_sha256") == V3_EXACT10_PINS[9][1] and
             rejected.get("cold_outer_object_sha256") ==
                 V3_EXACT10_PINS[9][2] and
             rejected.get("formal_global_closure_credit") == 0 and
             rejected.get("D02_unlock") is False and
             rejected.get("D02_started") is False and
             rejected.get("standalone_authority") is False and
             rejected.get("overwrite_delete_or_reuse_allowed") is False,
                 "official v3 rejection binds frozen v3 exact10")
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
        need(self.namespace is not None, "v3 rejection namespace held")
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

    def __init__(self, coordination: HeldCoordinationParent,
                 rejection: HeldFile) -> None:
        coordination.verify()
        self.path = V5_OFFICIAL_REJECTION.parent
        self.fd = -1
        self.fd = openat2_beneath(self.path, os.O_RDONLY | os.O_DIRECTORY)
        try:
            self.before = os.fstat(self.fd)
            self.mount_id = mount_id(self.fd)
            before_path = root_lstat(self.path)
            first = set(os.listdir(self.fd))
            member = os.stat(V5_OFFICIAL_REJECTION.name, dir_fd=self.fd,
                             follow_symlinks=False)
            after = os.fstat(self.fd)
            after_path = root_lstat(self.path)
            second = set(os.listdir(self.fd))
            need(stat.S_ISDIR(self.before.st_mode) and
                 stat.S_IMODE(self.before.st_mode) == 0o555 and
                 self.before.st_nlink == 2 and
                 fingerprint(before_path) == fingerprint(self.before) ==
                     fingerprint(after) == fingerprint(after_path) and
                 first == second == {V5_OFFICIAL_REJECTION.name} and
                 (member.st_dev, member.st_ino) == rejection.identity and
                 self.mount_id == rejection.mount_id == coordination.mount_id,
                 "official v5 rejection exact singleton namespace held under lock")
        except BaseException:
            os.close(self.fd)
            self.fd = -1
            raise

    def terminal_replay(self, rejection: HeldFile) -> None:
        before = os.fstat(self.fd)
        before_path = root_lstat(self.path)
        first = set(os.listdir(self.fd))
        member = os.stat(V5_OFFICIAL_REJECTION.name, dir_fd=self.fd,
                         follow_symlinks=False)
        after = os.fstat(self.fd)
        after_path = root_lstat(self.path)
        second = set(os.listdir(self.fd))
        need(fingerprint(before) == fingerprint(before_path) ==
             fingerprint(self.before) == fingerprint(after) ==
             fingerprint(after_path) and
             first == second == {V5_OFFICIAL_REJECTION.name} and
             stat.S_IMODE(after.st_mode) == 0o555 and after.st_nlink == 2 and
             (member.st_dev, member.st_ino) == rejection.identity and
             mount_id(self.fd) == self.mount_id,
             "official v5 rejection namespace terminal singleton replay")

    def close(self) -> None:
        if self.fd >= 0:
            os.close(self.fd)
            self.fd = -1


class HeldV5PredecessorExact10:
    """Replay published v5 exact10 plus its strictly later official rejection."""

    def __init__(self, coordination: HeldCoordinationParent,
                 rejection: HeldFile) -> None:
        coordination.verify()
        self.files: list[HeldFile] = []
        self.namespace: HeldV5RejectionNamespace | None = None
        try:
            for path, file_pin, _ in V5_EXACT10_PINS:
                self.files.append(HeldFile(
                    path, "frozen v5 exact10:" + path.name, file_pin))
            self.by_path = {item.path: item for item in self.files}
            need(len(self.by_path) == 10 and
                 len({item.identity for item in self.files}) == 10 and
                 len({item.mount_id for item in self.files}) == 1 and
                 next(iter({item.mount_id for item in self.files})) ==
                     coordination.mount_id == rejection.mount_id,
                 "frozen v5 exact10 unique live files on coordination mount")
            for path, _, object_pin in V5_EXACT10_PINS:
                if object_pin is not None:
                    value = strict_json(self.by_path[path].raw,
                                        "frozen v5 object:" + path.name)
                    need(isinstance(value, dict), "frozen v5 object mapping")
                    verify_object(value, "frozen v5 object:" + path.name,
                                  object_pin)
            expected_exact8 = [
                {"path": str(path.relative_to(ROOT)), "file_sha256": file_pin}
                for path, file_pin, _ in V5_EXACT10_PINS[:8]
            ]
            manifest = self.files[8]
            need(parse_manifest(manifest.raw) == expected_exact8,
                 "frozen v5 exact8 manifest reconstructed exactly")
            outer = strict_json(self.files[9].raw, "frozen v5 outer")
            need(isinstance(outer, dict), "frozen v5 outer mapping")
            verify_object(outer, "frozen v5 outer", V5_EXACT10_PINS[9][2])
            chronology = cold_publication_chronology(
                [item.before for item in self.files[:8]],
                self.files[8].before, self.files[9].before)
            need(self.files[9].raw == canonical(outer) + b"\n" and
                 set(outer) == {
                     "D02_unlock",
                     "all_exact8_regular_0444_nlink1_and_held_for_runtime",
                     "cold_launch_manifest", "cold_launcher",
                     "declared_external_tcb",
                     "effective_checkpoint_object_sha256",
                     "exact8_ordered_entries", "formal_global_closure_credit",
                     "object_sha256", "outer_published_after_exact8_manifest",
                     "runtime_entry_must_be_cold_launcher",
                     "runtime_executed_during_static_freeze", "schema",
                     "sole_external_static_file_anchor_is_launcher_sha256",
                     "status",
                 } and
                 outer.get("schema") ==
                     "cm2.round306c79g.true-global-no-producer-consumer."
                     "cold-launch-outer-receipt.v5" and
                 outer.get("status") ==
                     "FROZEN_COLD_LAUNCH_OUTER_LAST__EXACT8_MANIFEST_CLOSED__RUNTIME_DEFERRED" and
                 outer.get("effective_checkpoint_object_sha256") == CHECKPOINT and
                 outer.get("exact8_ordered_entries") == expected_exact8 and
                 outer.get("cold_launch_manifest", {}).get("file_sha256") ==
                     V5_EXACT10_PINS[8][1] and
                 outer.get("cold_launcher", {}).get("file_sha256") ==
                     V5_EXACT10_PINS[7][1] and
                 outer.get("formal_global_closure_credit") == 0 and
                 outer.get("D02_unlock") is False and
                 outer.get("runtime_executed_during_static_freeze") is False and
                 all(chronology.values()) and
                 max(self.files[9].before.st_mtime_ns,
                     self.files[9].before.st_ctime_ns) <
                     min(rejection.before.st_mtime_ns,
                         rejection.before.st_ctime_ns),
                 "frozen v5 exact10 outer then strictly later rejection closure")
            rejected = strict_json(rejection.raw, "official v5 later rejection")
            need(isinstance(rejected, dict), "official v5 rejection mapping")
            verify_object(rejected, "official v5 later rejection",
                          V5_REJECTION_OBJECT_PIN)
            need(rejection.raw == canonical(rejected) + b"\n" and
                 rejected.get("schema") ==
                     "cm2.round306c79g.true-global-no-producer-consumer.v5."
                     "later-rejection" and
                 rejected.get("status") ==
                     "PERMANENT_FAIL_CLOSED_REJECTION__ZERO_CREDIT" and
                 rejected.get("rejection_reason") ==
                     "ORPHANED_OR_INCOMPLETE_C79G_V5_SURFACE" and
                 rejected.get("effective_checkpoint_object_sha256") == CHECKPOINT and
                 rejected.get("target_exact_path") ==
                     str(V5_OFFICIAL_REJECTION.relative_to(ROOT)) and
                 rejected.get("namespace_exact_path") ==
                     str(V5_OFFICIAL_REJECTION.parent.relative_to(ROOT)) and
                 rejected.get("closed_schema_file_sha256") ==
                     V5_EXACT10_PINS[1][1] and
                 rejected.get("contract_file_sha256") == V5_EXACT10_PINS[2][1] and
                 rejected.get("contract_object_sha256") == V5_EXACT10_PINS[2][2] and
                 rejected.get("producer_file_sha256") == V5_EXACT10_PINS[3][1] and
                 rejected.get("consumer_file_sha256") == V5_EXACT10_PINS[4][1] and
                 rejected.get("cold_launcher_file_sha256") == V5_EXACT10_PINS[7][1] and
                 rejected.get("cold_manifest_file_sha256") == V5_EXACT10_PINS[8][1] and
                 rejected.get("cold_outer_file_sha256") == V5_EXACT10_PINS[9][1] and
                 rejected.get("cold_outer_object_sha256") == V5_EXACT10_PINS[9][2] and
                 rejected.get("v4_rejection_supersession_file_sha256") ==
                     V4_SUPERSESSION_FILE_PIN and
                 rejected.get("v4_rejection_supersession_object_sha256") ==
                     V4_SUPERSESSION_OBJECT_PIN and
                 rejected.get("formal_global_closure_credit") == 0 and
                 rejected.get("D02_unlock") is False and
                 rejected.get("D02_started") is False and
                 rejected.get("standalone_authority") is False and
                 rejected.get("overwrite_delete_or_reuse_allowed") is False,
                 "official v5 rejection binds published v5 exact10")
            self.strict_bool_regression = v5_strict_bool_regression({
                "producer_v5": self.files[3].raw,
                "consumer_v5": self.files[4].raw,
                "launcher_v5": self.files[7].raw,
            })
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
            root_absent(path, "officially rejected v5 runtime surface:" + path.name)

    def terminal_replay(self, rejection: HeldFile) -> None:
        for item in self.files:
            item.terminal_replay()
        need(self.namespace is not None, "v5 rejection namespace held")
        self.namespace.terminal_replay(rejection)
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

    def __init__(self, coordination: HeldCoordinationParent,
                 receipt: HeldFile, v3_rejection: HeldFile) -> None:
        coordination.verify()
        self.files: list[HeldFile] = []
        try:
            for path, file_pin, _ in V4_FROZEN_DRAFT7_PINS:
                self.files.append(HeldFile(
                    path, "rejected frozen v4 draft7:" + path.name, file_pin))
            self.by_path = {item.path: item for item in self.files}
            need(len(self.by_path) == 7 and
                 len({item.identity for item in self.files}) == 7 and
                 len({item.mount_id for item in self.files}) == 1 and
                 next(iter({item.mount_id for item in self.files})) ==
                     coordination.mount_id == receipt.mount_id ==
                     v3_rejection.mount_id,
                 "rejected v4 draft7 unique live files on coordination mount")
            for path, _, object_pin in V4_FROZEN_DRAFT7_PINS:
                if object_pin is not None:
                    value = strict_json(self.by_path[path].raw,
                                        "rejected v4 object:" + path.name)
                    need(isinstance(value, dict), "rejected v4 object mapping")
                    verify_object(value, "rejected v4 object:" + path.name,
                                  object_pin)
            value = strict_json(receipt.raw, "v4 rejection supersession")
            need(isinstance(value, dict), "v4 supersession mapping")
            verify_object(value, "v4 rejection supersession",
                          V4_SUPERSESSION_OBJECT_PIN)
            expected_members = [{
                "file_sha256": V3_REJECTION_FILE_PIN,
                "mode": "0444",
                "name": "official_v3_later_rejection",
                "nlink": 1,
                "object_sha256": V3_REJECTION_OBJECT_PIN,
                "path": str(V3_OFFICIAL_REJECTION.relative_to(ROOT)),
            }]
            names = (
                "closed_schema_v4", "contract_v4", "build_only_producer_v4",
                "independent_consumer_v4", "transition_v3_to_v4",
                "static_audit_v4", "cold_launcher_v4")
            for name, (path, file_pin, object_pin) in zip(
                    names, V4_FROZEN_DRAFT7_PINS, strict=True):
                member: dict[str, Any] = {
                    "file_sha256": file_pin, "mode": "0444", "name": name,
                    "nlink": 1, "path": str(path.relative_to(ROOT)),
                }
                if object_pin is not None:
                    member["object_sha256"] = object_pin
                expected_members.append(member)
            root_defects = value.get("root_defects")
            frozen = value.get("frozen_v4_provisional_exact8")
            no_run = value.get("no_run_attestation")
            rejection = value.get("rejection")
            supersession = value.get("supersession")
            need(receipt.raw == canonical(value) + b"\n" and
                 value.get("schema") ==
                    "cm2.round306c79g.true-global-no-producer-consumer."
                    "v4-rejection-supersession-receipt.v1" and
                 value.get("status") ==
                    "FROZEN_APPEND_ONLY_V4_STATIC_NO_RUN_REJECTION__"
                    "THREE_ROOT_DEFECTS__V5_SUCCESSOR_ONLY" and
                 value.get("effective_checkpoint_object_sha256") == CHECKPOINT and
                 value.get("formal_global_closure_credit") == 0 and
                 value.get("D02_unlock") is False and
                 value.get("D02_started") is False and
                 isinstance(frozen, dict) and
                 frozen.get("ordered_members") == expected_members and
                 frozen.get("all_eight_file_pins_match") is True and
                 frozen.get("all_eight_regular_0444_nlink1") is True and
                 frozen.get("cold_manifest_v4_exists") is False and
                 frozen.get("cold_outer_v4_exists") is False and
                 isinstance(root_defects, list) and len(root_defects) == 3 and
                 {item.get("id") for item in root_defects
                  if isinstance(item, dict)} == {
                    "V4_CONSUMER_NEED_THREE_POSITIONAL_ARGUMENTS",
                    "V4_CONSUMER_HELDOPAQUEMETADATA_MISSING_EXPECTED_MODE",
                    "V4_LAUNCHER_PATHNAME_EXECUTION_PRECEDES_HELD_FD_HASH",
                 } and isinstance(no_run, dict) and
                 no_run.get("v4_runtime_commands_invoked") == [] and
                 no_run.get("v4_candidate_verification_completion_authority_surfaces_created") == 0 and
                 isinstance(rejection, dict) and
                 rejection.get("v4_execution_allowed") is False and
                 rejection.get("v4_runtime_surfaces_authoritative") is False and
                 isinstance(supersession, dict) and
                 supersession.get("successor_version") == 5 and
                 supersession.get("successor_must_pin_this_receipt_file_and_object_hashes") is True,
                 "frozen v4 receipt exactly rejects and supersedes draft7")
            self.receipt_value = value
            self._assert_unpublished_absence(frozen)
        except BaseException:
            for item in reversed(self.files):
                item.close()
            raise

    @staticmethod
    def _assert_unpublished_absence(frozen: Mapping[str, Any]) -> None:
        root_absent(ROOT / str(frozen["cold_manifest_v4_path"]),
                    "v4 cold manifest")
        root_absent(ROOT / str(frozen["cold_outer_v4_path"]),
                    "v4 cold outer")
        for path in V4_FORBIDDEN_RUNTIME_PATHS:
            root_absent(path, "rejected v4 runtime surface:" + path.name)

    def terminal_replay(self) -> None:
        for item in self.files:
            item.terminal_replay()
        frozen = self.receipt_value["frozen_v4_provisional_exact8"]
        need(isinstance(frozen, dict), "v4 frozen receipt replay mapping")
        self._assert_unpublished_absence(frozen)

    def close(self) -> None:
        for item in self.files:
            item.close()
        self.files = []


def parse_manifest(raw: bytes) -> list[dict[str, str]]:
    need(raw.endswith(b"\n"), "cold manifest terminal newline")
    result: list[dict[str, str]] = []
    seen: set[str] = set()
    for line in raw.decode("ascii").splitlines():
        parts = line.split("  ", 1)
        need(len(parts) == 2 and re.fullmatch(r"[0-9a-f]{64}", parts[0]) is not None and
             parts[1] not in seen, "cold manifest exact line")
        seen.add(parts[1])
        result.append({"path": parts[1], "file_sha256": parts[0]})
    return result


class HeldBundle:
    def __init__(self, expected_launcher_sha256: str,
                 coordination: HeldCoordinationParent,
                 bootstrap: HeldBootstrapEntry) -> None:
        self.files: list[HeldFile] = []
        self.manifest: HeldFile | None = None
        self.outer: HeldFile | None = None
        self.v3_rejection: HeldFile | None = None
        self.predecessor_v3: HeldV3PredecessorExact10 | None = None
        self.predecessor_v5: HeldV5PredecessorExact10 | None = None
        self.rejected_v4: HeldV4RejectedDraft7 | None = None
        self.bootstrap = bootstrap
        try:
            self._initialize(expected_launcher_sha256, coordination, bootstrap)
        except BaseException:
            self.close()
            raise

    def _initialize(self, expected_launcher_sha256: str,
                    coordination: HeldCoordinationParent,
                    bootstrap: HeldBootstrapEntry) -> None:
        coordination.verify()
        need(SELF == OUT / (BASE + "_cold_launch_v6.py"),
             "exact cold launcher path")
        need(FINAL_BASE7_PINS_INSTALLED is True,
             "draft launcher disabled until root installs final audited base7 pins")
        for path, (file_pin, object_pin) in BASE7_PINS.items():
            need(re.fullmatch(r"[0-9a-f]{64}", file_pin) is not None and
                 file_pin != "0" * 64 and
                 (path == V5_OFFICIAL_REJECTION or
                  file_pin != _DRAFT_FILE_PIN) and
                 (object_pin is None or
                  (re.fullmatch(r"[0-9a-f]{64}", object_pin) is not None and
                   object_pin != "0" * 64 and
                   (path == V5_OFFICIAL_REJECTION or
                    object_pin != _DRAFT_OBJECT_PIN))),
                 "all embedded base7 pins final")
        need(re.fullmatch(r"[0-9a-f]{64}", expected_launcher_sha256) is not None and
             expected_launcher_sha256 != "0" * 64,
             "caller-supplied external launcher SHA-256 anchor")
        bootstrap.terminal_replay()
        for path in EXACT8:
            item = (bootstrap.held_launcher() if path == SELF else HeldFile(
                path, "cold exact8:" + path.name, BASE7_PINS[path][0]))
            self.files.append(item)
        self.by_path = {guard.path: guard for guard in self.files}
        need(expected_launcher_sha256 == self.by_path[SELF].file_sha256,
             "sole external launcher SHA-256 equals held SELF")
        for path, (file_pin, _) in BASE7_PINS.items():
            need(self.by_path[path].file_sha256 == file_pin,
                 "embedded base7 file pin:" + path.name)
        expected_entries = [
            {"path": str(path.relative_to(ROOT)),
             "file_sha256": self.by_path[path].file_sha256}
            for path in EXACT8
        ]
        expected_manifest_raw = b"".join(
            (entry["file_sha256"] + "  " + entry["path"] + "\n").encode("ascii")
            for entry in expected_entries
        )
        self.manifest = HeldFile(MANIFEST, "cold exact8 manifest")
        need(self.manifest.raw == expected_manifest_raw,
             "cold manifest byte-identical to reconstructed ordered exact8")
        entries = parse_manifest(self.manifest.raw)
        need(entries == expected_entries, "cold manifest exact ordered eight")
        self.outer = HeldFile(OUTER, "cold outer-last")
        exact10 = [*self.files, self.manifest, self.outer]
        need(len(exact10) == 10 and len({item.identity for item in exact10}) == 10 and
             len({item.mount_id for item in exact10}) == 1,
             "cold exact10 identities globally unique on one mount")
        self.chronology = cold_publication_chronology(
            [item.before for item in self.files],
            self.manifest.before, self.outer.before)
        need(all(self.chronology.values()),
             "physical exact8 freeze then manifest freeze then outer freeze chronology")
        self.entries = entries
        self.schema = strict_json(self.by_path[SCHEMA].raw, "closed schema")
        need(isinstance(self.schema, dict) and
             self.schema.get("$ref") == "#/$defs/coldLaunchedCommittedAuthority",
             "closed schema has cold-launched root only")
        self.schema_keywords = schema_keyword_universe(self.schema)
        self.base_objects: dict[Path, dict[str, Any]] = {}
        for path in (V5_OFFICIAL_REJECTION, CONTRACT, TRANSITION, AUDIT):
            value = strict_json(self.by_path[path].raw, "cold object:" + path.name)
            need(isinstance(value, dict), "cold base JSON object:" + path.name)
            verify_object(value, path.name, BASE7_PINS[path][1])
            self.base_objects[path] = value
        need(self.base_objects[CONTRACT].get("status") ==
                 "STATIC_CONTRACT_BYTES_FINAL__COLD_FREEZE_PENDING__RUNTIME_NOT_AUTHORIZED" and
             self.base_objects[TRANSITION].get("status") ==
                 "STATIC_BYTES_CLOSED_V5_TO_V6__PHYSICAL_FREEZE_PENDING__RUNTIME_NOT_AUTHORIZED" and
             self.base_objects[AUDIT].get("status") ==
                 "PASS_DUAL_STATIC_BYTES_GO_V6__PHYSICAL_COLD_FREEZE_PENDING__RUNTIME_NOT_AUTHORIZED",
             "contract transition and dual audit exact prepublication statuses")
        for proof_path in (CONTRACT, TRANSITION, AUDIT):
            validate_v5_published_rejected_segment(
                self.base_objects[proof_path].get(
                    "published_then_officially_rejected_predecessor_v5"),
                proof_path.name)
        schema_audit = self.base_objects[AUDIT].get(
            "schema_and_constructor_closure", {})
        need(isinstance(schema_audit, dict) and
             schema_audit.get("actual_schema_keyword_universe") ==
                 sorted(self.schema_keywords) and
             schema_audit.get("cold_launcher_supported_schema_keyword_universe") ==
                 sorted(SUPPORTED_SCHEMA_KEYWORDS) and
             schema_audit.get(
                 "all_schema_validation_keywords_supported_by_cold_launcher") is True and
             schema_audit.get("unknown_schema_validation_keyword_count") == 0 and
             schema_audit.get(
                 "oneOf_keyword_absent_after_pin_definition_split") is True and
             "oneOf" not in self.schema_keywords and
             self.schema_keywords <= SUPPORTED_SCHEMA_KEYWORDS,
             "static audit and live closed schema prove complete supported keyword universe")
        self.outer_object = strict_json(self.outer.raw, "cold outer-last")
        need(isinstance(self.outer_object, dict), "cold outer JSON object")
        verify_object(self.outer_object, "cold outer-last")
        need(set(self.outer_object) == {
                 "schema", "status", "effective_checkpoint_object_sha256",
                 "exact8_ordered_entries", "cold_launch_manifest", "cold_launcher",
                 "all_exact8_regular_0444_nlink1_and_held_for_runtime",
                 "outer_published_after_exact8_manifest",
                 "runtime_entry_must_be_cold_launcher",
                 "sole_external_static_file_anchor_is_launcher_sha256",
                 "declared_external_tcb",
                 "formal_global_closure_credit", "D02_unlock",
                 "runtime_executed_during_static_freeze", "object_sha256"} and
             self.outer.raw == canonical(self.outer_object) + b"\n" and
             self.outer_object.get("schema") ==
                 "cm2.round306c79g.true-global-no-producer-consumer."
                 "cold-launch-outer-receipt.v6" and
             self.outer_object.get("status") ==
                 "FROZEN_COLD_LAUNCH_OUTER_LAST__EXACT8_MANIFEST_CLOSED__RUNTIME_DEFERRED" and
             self.outer_object.get("effective_checkpoint_object_sha256") == CHECKPOINT and
             self.outer_object.get("exact8_ordered_entries") == entries and
             self.outer_object.get("cold_launch_manifest") == {
                 "path": str(MANIFEST.relative_to(ROOT)),
                 "file_sha256": self.manifest.file_sha256,
                 "ordered_entry_count": 8,
             } and
             self.outer_object.get("cold_launcher") == {
                 "path": str(SELF.relative_to(ROOT)),
                 "file_sha256": self.by_path[SELF].file_sha256,
             } and
             self.outer_object.get("all_exact8_regular_0444_nlink1_and_held_for_runtime") is True and
             self.outer_object.get("outer_published_after_exact8_manifest") is True and
             self.outer_object.get("runtime_entry_must_be_cold_launcher") is True and
             self.outer_object.get("sole_external_static_file_anchor_is_launcher_sha256") is True and
             self.outer_object.get("declared_external_tcb") == [
                 "EXTERNAL_HELD_FD_SEALED_MEMFD_BOOTSTRAP",
                 "PYTHON3_ISOLATED_INTERPRETER",
                 "LINUX_KERNEL_OPENAT2_STATX_MEMFD_PROCFS",
             ] and
             self.outer_object.get("formal_global_closure_credit") == 0 and
             self.outer_object.get("D02_unlock") is False and
             self.outer_object.get("runtime_executed_during_static_freeze") is False,
             "cold outer-last exact closure")
        # Current exact8 owns the sole v5-rejection fd.  It is shared with the
        # immediate v5 exact10 proof.  The v5 exact10's v4 receipt fd is then
        # shared with the rejected-v4 proof; v3 keeps its separate singleton.
        self.predecessor_v5 = HeldV5PredecessorExact10(
            coordination, self.by_path[V5_OFFICIAL_REJECTION])
        self.v3_rejection = HeldFile(
            V3_OFFICIAL_REJECTION, "official v3 later rejection",
            V3_REJECTION_FILE_PIN)
        rejected_value = strict_json(
            self.v3_rejection.raw, "official v3 later rejection object")
        need(isinstance(rejected_value, dict), "official v3 rejection mapping")
        verify_object(rejected_value, "official v3 later rejection object",
                      V3_REJECTION_OBJECT_PIN)
        self.predecessor_v3 = HeldV3PredecessorExact10(
            coordination, self.v3_rejection)
        self.rejected_v4 = HeldV4RejectedDraft7(
            coordination,
            self.predecessor_v5.by_path[V4_REJECTION_SUPERSESSION],
            self.v3_rejection)
        predecessor_v3_identities = {
            item.identity for item in self.predecessor_v3.files
        }
        predecessor_v5_identities = {
            item.identity for item in self.predecessor_v5.files
        }
        rejected_v4_identities = {
            item.identity for item in self.rejected_v4.files
        }
        current_identities = {
            item.identity for item in [*self.files, self.manifest, self.outer]
        }
        need(len(predecessor_v3_identities) == 10 and
             len(predecessor_v5_identities) == 10 and
             len(rejected_v4_identities) == 7 and
             predecessor_v3_identities.isdisjoint(current_identities) and
             predecessor_v5_identities.isdisjoint(current_identities) and
             rejected_v4_identities.isdisjoint(current_identities) and
             predecessor_v3_identities.isdisjoint(predecessor_v5_identities) and
             predecessor_v3_identities.isdisjoint(rejected_v4_identities) and
             rejected_v4_identities.isdisjoint(predecessor_v5_identities) and
             self.v3_rejection.identity not in predecessor_v3_identities |
                 predecessor_v5_identities | rejected_v4_identities |
                 current_identities and
             self.by_path[V5_OFFICIAL_REJECTION].identity not in
                 predecessor_v5_identities | predecessor_v3_identities |
                 rejected_v4_identities and
             self.predecessor_v5.by_path[V4_REJECTION_SUPERSESSION].identity in
                 predecessor_v5_identities and
             len({item.mount_id for item in self.predecessor_v3.files} |
                 {item.mount_id for item in self.predecessor_v5.files} |
                 {item.mount_id for item in self.rejected_v4.files} |
                 {item.mount_id for item in [*self.files, self.manifest,
                                             self.outer, self.v3_rejection]}) == 1,
             "current exact10, v5 exact10, v3 exact10, v3 rejection and v4 draft7 are 38 unique live files on one mount")
        validate_final_static_audit(
            self.base_objects[AUDIT], self.schema, self.schema_keywords,
            self.by_path, self.base_objects, self.predecessor_v5)

    def terminal_replay(self) -> None:
        need(self.predecessor_v3 is not None and
             self.predecessor_v5 is not None and
             self.rejected_v4 is not None and
             self.v3_rejection is not None and self.manifest is not None and
             self.outer is not None,
             "complete historical and current bundle held")
        self.predecessor_v5.terminal_replay(
            self.by_path[V5_OFFICIAL_REJECTION])
        self.predecessor_v3.terminal_replay(self.v3_rejection)
        self.rejected_v4.terminal_replay()
        self.v3_rejection.terminal_replay()
        for guard in [*self.files, self.manifest, self.outer]:
            guard.terminal_replay()
        terminal_chronology = cold_publication_chronology(
            [item.before for item in self.files],
            self.manifest.before, self.outer.before)
        need(terminal_chronology == self.chronology and
             all(terminal_chronology.values()),
             "terminal cold freeze chronology unchanged")
        self.bootstrap.terminal_replay()

    def close(self) -> None:
        if self.rejected_v4 is not None:
            self.rejected_v4.close()
            self.rejected_v4 = None
        if self.predecessor_v5 is not None:
            self.predecessor_v5.close()
            self.predecessor_v5 = None
        if self.predecessor_v3 is not None:
            self.predecessor_v3.close()
            self.predecessor_v3 = None
        if self.v3_rejection is not None:
            self.v3_rejection.close()
            self.v3_rejection = None
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
    return {
        "object": isinstance(value, dict),
        "array": isinstance(value, list),
        "string": isinstance(value, str),
        "integer": type(value) is int,
        "number": type(value) in {int, float},
        "boolean": type(value) is bool,
        "null": value is None,
    }.get(type_name, False)


SUPPORTED_SCHEMA_KEYWORDS = frozenset({
    "$schema", "$id", "$comment", "title", "description", "$defs", "$ref",
    "type", "const", "additionalProperties", "required", "properties",
    "items", "prefixItems", "minItems", "maxItems", "uniqueItems",
    "minLength", "pattern", "minimum",
})


def schema_keyword_universe(root: Mapping[str, Any]) -> frozenset[str]:
    """Reject every validation keyword this closed validator cannot enforce."""
    seen: set[str] = set()

    def walk(node: Any, label: str) -> None:
        need(isinstance(node, dict), label + ":schema node object")
        unknown = set(node) - SUPPORTED_SCHEMA_KEYWORDS
        need(not unknown, label + ":unsupported schema keywords:" +
             ",".join(sorted(unknown)))
        seen.update(node)
        definitions = node.get("$defs", {})
        need(isinstance(definitions, dict), label + ":$defs object")
        for name, child in definitions.items():
            need(isinstance(name, str) and len(name) > 0,
                 label + ":$defs name")
            walk(child, label + ".$defs." + name)
        properties = node.get("properties", {})
        need(isinstance(properties, dict), label + ":properties object")
        for name, child in properties.items():
            need(isinstance(name, str) and len(name) > 0,
                 label + ":property name")
            walk(child, label + ".properties." + name)
        prefix_items = node.get("prefixItems", [])
        need(isinstance(prefix_items, list), label + ":prefixItems array")
        for index, child in enumerate(prefix_items):
            walk(child, f"{label}.prefixItems[{index}]")
        items = node.get("items")
        need(items is None or items is False or isinstance(items, dict),
             label + ":items schema-or-false")
        if isinstance(items, dict):
            walk(items, label + ".items")
        additional = node.get("additionalProperties")
        need(additional is None or isinstance(additional, bool) or
             isinstance(additional, dict),
             label + ":additionalProperties schema-or-boolean")
        if isinstance(additional, dict):
            walk(additional, label + ".additionalProperties")

    walk(root, "closed-schema")
    return frozenset(seen)


def validate_schema(value: Any, node: Mapping[str, Any], root: Mapping[str, Any],
                    label: str) -> None:
    need(set(node) <= SUPPORTED_SCHEMA_KEYWORDS,
         label + ":no unsupported schema validation keyword")
    if "$ref" in node:
        reference = node["$ref"]
        need(isinstance(reference, str) and reference.startswith("#/$defs/"),
             label + ":local ref only")
        name = reference.removeprefix("#/$defs/")
        target = root.get("$defs", {}).get(name)
        need(isinstance(target, dict), label + ":resolved ref:" + name)
        validate_schema(value, target, root, label + "->" + name)
        return
    if "const" in node:
        expected = node["const"]
        need(type(value) is type(expected) and value == expected, label + ":const")
    type_name = node.get("type")
    if type_name is not None:
        need(isinstance(type_name, str) and
             _type_matches(value, type_name) is True,
             label + ":type:" + str(type_name))
    if isinstance(value, dict):
        required = node.get("required", [])
        need(isinstance(required, list) and all(key in value for key in required),
             label + ":required")
        properties = node.get("properties", {})
        need(isinstance(properties, dict), label + ":properties")
        if node.get("additionalProperties") is False:
            need(set(value) <= set(properties), label + ":additionalProperties")
        for key, child in properties.items():
            if key in value:
                need(isinstance(child, dict), label + ":child schema")
                validate_schema(value[key], child, root, label + "." + key)
    if isinstance(value, list):
        if "minItems" in node:
            need(len(value) >= node["minItems"], label + ":minItems")
        if "maxItems" in node:
            need(len(value) <= node["maxItems"], label + ":maxItems")
        if node.get("uniqueItems") is True:
            need(len({canonical(item) for item in value}) == len(value),
                 label + ":uniqueItems")
        prefix = node.get("prefixItems", [])
        need(isinstance(prefix, list), label + ":prefixItems")
        for index, child_schema in enumerate(prefix[:len(value)]):
            need(isinstance(child_schema, dict), label + ":prefix schema")
            validate_schema(value[index], child_schema, root, f"{label}[{index}]")
        if len(value) > len(prefix):
            item_schema = node.get("items")
            need(item_schema is not False, label + ":items false")
            if item_schema is not None:
                need(isinstance(item_schema, dict), label + ":items schema")
                for index in range(len(prefix), len(value)):
                    validate_schema(value[index], item_schema, root,
                                    f"{label}[{index}]")
    if isinstance(value, str):
        if "minLength" in node:
            need(len(value) >= node["minLength"], label + ":minLength")
        if "pattern" in node:
            need(re.search(node["pattern"], value) is not None, label + ":pattern")
    if type(value) in {int, float} and "minimum" in node:
        need(value >= node["minimum"], label + ":minimum")


def child_environment(bundle: HeldBundle, child_exec: HeldSealedChildExec,
                      source: HeldFile,
                      coordination: HeldCoordinationParent) -> dict[str, str]:
    return {
        "LC_ALL": "C",
        "TZ": "UTC",
        EXEC_FD_ENV: str(child_exec.fd),
        SOURCE_FD_ENV: str(source.fd),
        COORDINATION_PARENT_FD_ENV: str(coordination.fd),
        WORKSPACE_ROOT_ENV: str(ROOT),
        WORKSPACE_ROOT_FD_ENV: str(bundle.bootstrap.root_fd),
        LAUNCHER_SHA_ENV: bundle.by_path[SELF].file_sha256,
    }


def child_argv(child_exec: HeldSealedChildExec, command: str,
               forwarded: list[str]) -> list[str]:
    return [sys.executable, "-I", "-B", "-S",
            "/proc/self/fd/" + str(child_exec.fd), command, *forwarded]


def run_non_authorize_child(
        bundle: HeldBundle, coordination: HeldCoordinationParent,
        rejection_guard: HeldEmptyRejectionNamespace,
        command: str, forwarded: list[str]) -> bytes:
    need(command in {"build", "verify", "assemble"},
         "only non-reject child commands reach bundle dispatch")
    source = bundle.by_path[PRODUCER if command == "build" else CONSUMER]
    child_exec = HeldSealedChildExec(source)
    try:
        os.lseek(child_exec.fd, 0, os.SEEK_SET)
        completed = subprocess.run(
            child_argv(child_exec, command, forwarded),
            stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=child_environment(bundle, child_exec, source, coordination),
            pass_fds=(child_exec.fd, source.fd, coordination.fd,
                      bundle.bootstrap.root_fd),
            check=False)
        if completed.stderr:
            sys.stderr.buffer.write(completed.stderr)
        need(completed.returncode == 0, "cold child rejected or failed")
        child_exec.terminal_replay()
        bundle.terminal_replay()
        rejection_guard.terminal_replay()
        coordination.verify()
        return completed.stdout
    finally:
        child_exec.close()


def cold_root(bundle: HeldBundle, coordination: HeldCoordinationParent,
              child_exec: HeldSealedChildExec,
              inner_raw: bytes) -> tuple[dict[str, Any], dict[str, Any]]:
    need(inner_raw.endswith(b"\n") and inner_raw.count(b"\n") == 1,
         "authorize child first stdout is exactly one JSON line")
    inner = strict_json(inner_raw, "zero-credit inner live composite")
    need(isinstance(inner, dict), "inner live composite object")
    verify_object(inner, "inner live composite")
    validate_schema(inner, {"$ref": "#/$defs/innerComposite"}, bundle.schema, "inner")
    need(inner.get("schema") == INNER_SCHEMA and
         inner.get("formal_global_closure_credit") == 0 and
         inner.get("D02_unlock") is False and
         inner.get("cold_launcher_required") is True and
         inner_raw == canonical(inner) + b"\n",
         "direct consumer result is canonical launcher-required zero-only inner")
    need(bundle.predecessor_v5 is not None,
         "immediate v5 predecessor remains held for cold root")
    predecessor_v5 = bundle.predecessor_v5
    proof = {
        "launcher_identity": bundle.by_path[SELF].identity_object(),
        "manifest_identity": bundle.manifest.identity_object(),
        "outer_identity": bundle.outer.identity_object(),
        "ordered_exact8_identities": [bundle.by_path[path].identity_object()
                                       for path in EXACT8],
        "exact10_identity_count": 10,
        "current_exact8_first_member_is_v5_official_rejection":
            EXACT8[0] == V5_OFFICIAL_REJECTION,
        "v5_official_rejection_identity": {
            **bundle.by_path[V5_OFFICIAL_REJECTION].identity_object(),
            "object_sha256": V5_REJECTION_OBJECT_PIN,
        },
        "v5_official_rejection_file_sha256": V5_REJECTION_FILE_PIN,
        "v5_official_rejection_object_sha256": V5_REJECTION_OBJECT_PIN,
        "v4_rejection_supersession_identity": {
            **predecessor_v5.by_path[
                V4_REJECTION_SUPERSESSION].identity_object(),
            "object_sha256": V4_SUPERSESSION_OBJECT_PIN,
        },
        "v4_rejection_supersession_file_sha256": V4_SUPERSESSION_FILE_PIN,
        "v4_rejection_supersession_object_sha256": V4_SUPERSESSION_OBJECT_PIN,
        "all_exact10_identities_globally_unique_on_one_statx_mount": True,
        "all_current_and_historical_38_identities_globally_unique_on_one_statx_mount": True,
        **bundle.chronology,
        "external_launcher_file_sha256_pin_required": True,
        "external_launcher_file_sha256_equals_held_launcher": True,
        "sole_external_launcher_sha256_is_only_external_static_anchor": True,
        "sole_external_static_byte_anchor_excludes_explicit_bootstrap_interpreter_kernel_TCB": True,
        "external_bootstrap_is_minimal_inline_trusted_code": True,
        "external_bootstrap_opens_workspace_root_and_launcher_with_openat2_four_resolve_flags": True,
        "external_bootstrap_hashes_installed_source_copies_exact_bytes_into_and_executes_same_sealed_exec_fd": True,
        "launcher_executed_only_via_proc_self_fd": True,
        "launcher_exec_fd_equals_argv0___file___and_source_fd_equals_installed_path_identity": True,
        "launcher_root_bound_to_inherited_preopened_root_fd": True,
        "launcher_pathname_execution_fallback_allowed": False,
        "trusted_python_interpreter_linux_kernel_openat2_and_minimal_bootstrap_declared_TCB": True,
        "launcher_native_reject_dispatch_after_self_proof_and_lock_before_current_bundle_open": True,
        "manifest_and_outer_reconstructed_without_independent_external_hash": True,
        "child_source_path": str(CONSUMER.relative_to(ROOT)),
        "child_source_file_sha256": bundle.by_path[CONSUMER].file_sha256,
        "child_exec_fd_distinct_from_held_exact8_source_fd":
            child_exec.fd != bundle.by_path[CONSUMER].fd,
        "child_exec_is_fresh_sealed_memfd_0444_nlink0": True,
        "child_exec_has_write_grow_shrink_and_seal_seals": True,
        "child_exec_bytes_equal_held_exact8_source_fd_bytes":
            child_exec.raw == bundle.by_path[CONSUMER].raw,
        "child_exec_argv0_and___file___equal_proc_self_fd_exec": True,
        "child_held_exact8_source_fd_terminally_replayed": True,
        "child_python_isolated_no_site_and_no_pyc": True,
        "child_first_stdout_exact_one_canonical_inner_object": True,
        "inner_validated_against_closed_innerComposite_schema": True,
        "cold_outer_object_sha256": bundle.outer_object["object_sha256"],
        "official_writer_coordination_parent": coordination.identity_object(),
        "launcher_owned_coordination_lock_acquired_before_child_spawn": True,
        "coordination_lock_passed_as_same_open_file_description": True,
        "coordination_lock_is_mandatory_for_official_writers_only": True,
        "launcher_empty_rejection_namespace_guard_held_from_before_child_spawn_and_terminally_replayed_before_final_dynamic_request": True,
        "same_uid_or_filesystem_administrator_bypass_not_claimed_prevented": True,
        "cold_two_phase_live_protocol": LIVE_PROTOCOL,
        "wrapper_closed_and_schema_validated_before_request": True,
        "wrapper_body_excludes_transaction_binding_request_ACK_and_RELEASE_to_avoid_hash_cycle": True,
        "transaction_binding_is_replay_identical_not_fresh_or_random": True,
        "terminal_exact10_replay_completed_before_final_dynamic_request": True,
        "live_v3_exact10_ordered_pins": [
            {"path": str(path.relative_to(ROOT)), "file_sha256": file_pin,
             **({"object_sha256": object_pin} if object_pin is not None else {})}
            for path, file_pin, object_pin in V3_EXACT10_PINS
        ],
        "live_v5_exact10_ordered_pins": [
            {"path": str(path.relative_to(ROOT)), "file_sha256": file_pin,
             **({"object_sha256": object_pin} if object_pin is not None else {})}
            for path, file_pin, object_pin in V5_EXACT10_PINS
        ],
        "official_v5_later_rejection": {
            "path": str(V5_OFFICIAL_REJECTION.relative_to(ROOT)),
            "namespace_path": str(V5_OFFICIAL_REJECTION.parent.relative_to(ROOT)),
            "file_sha256": V5_REJECTION_FILE_PIN,
            "object_sha256": V5_REJECTION_OBJECT_PIN,
        },
        "v5_predecessor_strict_bool_regression":
            predecessor_v5.strict_bool_regression,
        "official_v3_later_rejection": {
            "path": str(V3_OFFICIAL_REJECTION.relative_to(ROOT)),
            "namespace_path": str(V3_OFFICIAL_REJECTION.parent.relative_to(ROOT)),
            "file_sha256": V3_REJECTION_FILE_PIN,
            "object_sha256": V3_REJECTION_OBJECT_PIN,
        },
        "ordered_provisional_exact8_live_pins": [{
            "path": str(V3_OFFICIAL_REJECTION.relative_to(ROOT)),
            "file_sha256": V3_REJECTION_FILE_PIN,
            "object_sha256": V3_REJECTION_OBJECT_PIN,
        }, *[
            {"path": str(path.relative_to(ROOT)), "file_sha256": file_pin,
             **({"object_sha256": object_pin} if object_pin is not None else {})}
            for path, file_pin, object_pin in V4_FROZEN_DRAFT7_PINS
        ]],
        "launcher_same_lock_live_v3_exact10_and_official_rejection_singleton_namespace_held": True,
        "launcher_same_lock_live_v5_exact10_and_official_rejection_held": True,
        "terminal_v5_exact10_and_official_rejection_replay_completed_before_final_dynamic_request": True,
        "launcher_same_lock_live_v4_provisional_exact8_and_supersession_receipt_held": True,
        "terminal_v4_provisional_exact8_and_supersession_replay_completed_before_final_dynamic_request": True,
        "reject_command_exempts_only_fresh_empty_v6_rejection_namespace": True,
        "final_dynamic_ack_bound_to_inner_and_final_wrapper_object": True,
        "final_dynamic_ack_requires_full_replay_and_fresh_rejection_scan": True,
        "launcher_lock_survives_child_exit_or_crash_until_wrapper_raw_final_newline_commit": True,
        "no_fallible_schema_or_filesystem_gate_after_validated_ack": True,
        "positive_wrapper_stdout_fd1_blocking_pipe_preflushed_and_duplicated_before_dynamic_request": True,
        "positive_wrapper_raw_fd1_final_newline_write_is_semantic_commit": True,
        "post_ACK_release_and_child_exit_are_non_authority_cleanup": True,
    }
    authority_root_sha256 = sha_bytes(COLD_ROOT_DOMAIN + canonical({
        "inner_object_sha256": inner["object_sha256"],
        "manifest_file_sha256": bundle.manifest.file_sha256,
        "outer_file_sha256": bundle.outer.file_sha256,
        "outer_object_sha256": bundle.outer_object["object_sha256"],
        "launcher_file_sha256": bundle.by_path[SELF].file_sha256,
        "v5_official_rejection_file_sha256": V5_REJECTION_FILE_PIN,
        "v5_official_rejection_object_sha256": V5_REJECTION_OBJECT_PIN,
        "v4_supersession_file_sha256": V4_SUPERSESSION_FILE_PIN,
        "v4_supersession_object_sha256": V4_SUPERSESSION_OBJECT_PIN,
        "v3_official_rejection_file_sha256": V3_REJECTION_FILE_PIN,
        "v3_official_rejection_object_sha256": V3_REJECTION_OBJECT_PIN,
        "coordination_parent_st_dev": coordination.before.st_dev,
        "coordination_parent_st_ino": coordination.before.st_ino,
        "coordination_parent_statx_mnt_id": coordination.mount_id,
    }))
    root = close_object({
        "schema": COLD_ROOT_SCHEMA,
        "status": "GO_COLD_LAUNCHED_LIVE_COMPOSITE_ONLY",
        "authority_decision": "GO_COLD_LAUNCHED_COMPOSITE_ONLY",
        "effective_checkpoint_object_sha256": CHECKPOINT,
        "inner_composite": inner,
        "cold_launch_proof": proof,
        "preseal_root_sha256": inner["preseal_root_sha256"],
        "inner_authority_root_sha256": inner["authority_root_sha256"],
        "authority_root_domain": COLD_ROOT_DOMAIN[:-1].decode("ascii"),
        "authority_root_sha256": authority_root_sha256,
        "formal_global_closure_credit": 1,
        "D02_unlock": True,
        "D02_gate_credit": 0,
        "D02_task_credit": 0,
        "D02_formal_pending_task_count": 33_638,
        "D02_started": False,
        "root_is_virtual_and_must_not_be_persisted": True,
    })
    validate_schema(root, bundle.schema, bundle.schema, "cold-root")
    return root, inner


def _read_child_line(pipe: Any, label: str) -> bytes:
    maximum = 32 * 1024 * 1024
    raw = pipe.readline(maximum + 1)
    need(raw.endswith(b"\n") and len(raw) <= maximum and raw.count(b"\n") == 1,
         label + ":one bounded newline-terminated object")
    return raw


def _wrapper_body_domain_sha256(root: Mapping[str, Any]) -> str:
    body = {key: value for key, value in root.items() if key != "object_sha256"}
    return sha_bytes(PREWRAPPER_BODY_DOMAIN.encode("ascii") + b"\x00" +
                     canonical(body))


def _deterministic_transaction_binding(
        bundle: HeldBundle, inner_object_sha256: str,
        wrapper_body_domain_sha256: str,
        wrapper_object_sha256: str) -> str:
    # This value prevents private-pipe transaction mixups.  It is intentionally
    # deterministic and is not represented as a freshness or randomness claim.
    return sha_bytes(
        TRANSACTION_BINDING_DOMAIN.encode("ascii") + b"\x00" +
        inner_object_sha256.encode("ascii") +
        wrapper_body_domain_sha256.encode("ascii") +
        wrapper_object_sha256.encode("ascii") +
        bundle.by_path[SELF].file_sha256.encode("ascii"))


def _expected_ack_binding(request: Mapping[str, Any]) -> str:
    return sha_bytes(
        LIVE_ACK_BINDING_DOMAIN.encode("ascii") + b"\x00" +
        request["transaction_binding_sha256"].encode("ascii") +
        request["inner_object_sha256"].encode("ascii") +
        request["wrapper_body_domain_sha256"].encode("ascii") +
        request["wrapper_object_sha256"].encode("ascii") +
        request["object_sha256"].encode("ascii"))


def _validate_lock_ack(value: Any,
                       coordination: HeldCoordinationParent) -> None:
    need(isinstance(value, dict) and set(value) == {
             "path", "held_parent_st_dev", "held_parent_st_ino",
             "held_parent_statx_mnt_id", "lock_api",
             "received_from_frozen_launcher_as_inherited_open_file_description_fd",
             "child_duplicated_and_identity_mount_checked_inherited_fd",
             "child_calls_LOCK_UN",
             "launcher_lock_owner_scope_requirement_includes_child_live_protocol",
             "mandatory_for_all_official_runtime_writers",
             "acquired_before_any_runtime_evidence_or_commit_surface_open_for_this_command",
             "required_final_hold_scope",
             "protocol_requires_launcher_RELEASE_before_normal_child_guard_close",
             "coordination_lock_is_not_claimed_as_a_security_boundary_against_noncooperating_same_uid_or_filesystem_administrator",
             "launcher_exclusive_lock_confirmed_by_independent_nonblocking_probe",
         } and
         value.get("path") == str(RUNTIME.relative_to(ROOT)) and
         value.get("held_parent_st_dev") == coordination.before.st_dev and
         value.get("held_parent_st_ino") == coordination.before.st_ino and
         value.get("held_parent_statx_mnt_id") == coordination.mount_id and
         value.get("lock_api") == "launcher_owned_fcntl.flock(LOCK_EX)" and
         value.get("received_from_frozen_launcher_as_inherited_open_file_description_fd") is True and
         value.get("child_duplicated_and_identity_mount_checked_inherited_fd") is True and
         value.get("child_calls_LOCK_UN") is False and
         value.get("launcher_lock_owner_scope_requirement_includes_child_live_protocol") is True and
         value.get("mandatory_for_all_official_runtime_writers") is True and
         value.get("acquired_before_any_runtime_evidence_or_commit_surface_open_for_this_command") is True and
         value.get("required_final_hold_scope") == [
             "inner_canonical_stdout_flush", "launcher_commit_request",
             "absolute_last_dynamic_terminal_replay",
             "live_ACK_canonical_stdout_flush",
             "launcher_positive_wrapper_raw_fd1_final_newline_write", "launcher_RELEASE"] and
         value.get("protocol_requires_launcher_RELEASE_before_normal_child_guard_close") is True and
         value.get("coordination_lock_is_not_claimed_as_a_security_boundary_against_noncooperating_same_uid_or_filesystem_administrator") is True and
         value.get("launcher_exclusive_lock_confirmed_by_independent_nonblocking_probe") is True,
         "live ACK exact launcher-owned official-writer lock proof")


def _validate_live_ack(
        raw: bytes, request: Mapping[str, Any],
        coordination: HeldCoordinationParent) -> dict[str, Any]:
    ack = strict_json(raw, "cold final-dynamic live ACK")
    need(isinstance(ack, dict), "cold live ACK object")
    verify_object(ack, "cold final-dynamic live ACK")
    expected_keys = {
        "schema", "status", "protocol", "transaction_binding_domain",
        "transaction_binding_sha256",
        "request_object_sha256", "inner_object_sha256",
        "wrapper_body_domain", "wrapper_body_domain_sha256",
        "wrapper_object_sha256", "ack_binding_domain", "ack_binding_sha256",
        "official_writer_coordination_lock", "final_dynamic_replay_census",
        "all_dynamic_conjuncts_live",
        "wrapper_closed_and_schema_validated_before_request",
        "wrapper_body_excludes_transaction_binding_request_ACK_and_RELEASE_to_avoid_hash_cycle",
        "transaction_binding_is_replay_identical_not_fresh_or_random",
        "static_v6_exact10_with_v5_exact10_and_official_rejection_v4_supersession_v3_exact10_and_official_rejection_terminal_replay_completed_by_launcher_before_request",
        "launcher_empty_rejection_namespace_guard_terminally_replayed_before_request",
        "consumer_exec_fd_is_fresh_sealed_memfd",
        "consumer_exec_fd_distinct_from_installed_source_fd",
        "consumer_exec_memfd_required_seals_valid",
        "consumer_exec_bytes_equal_installed_source_bytes",
        "consumer_exec_and_installed_source_terminal_replayed",
        "positive_wrapper_emitted_by_combined_child",
        "release_required_before_dynamic_guards_close",
        "positive_wrapper_raw_fd1_final_newline_write_is_launcher_semantic_commit",
        "post_ACK_RELEASE_and_child_exit_are_non_authority_cleanup",
        "formal_global_closure_credit", "D02_unlock", "object_sha256",
    }
    expected_census = {
        "C78l_C78s_held_file_count": 51,
        "C78l_C78s_held_directory_count": 5,
        "C55_C72_fixed_held_file_count_excluding_shared_head": 16,
        "shared_C72G_C53_head_held_via_C42_full10_count": 1,
        "frozen_v3_readable_held_file_count": 7,
        "frozen_v3_source_metadata_only_held_count": 3,
        "v3_official_rejection_shared_readable_held_file_count": 1,
        "frozen_v5_readable_held_file_count": 7,
        "frozen_v5_source_metadata_only_held_count": 3,
        "v5_official_rejection_shared_readable_held_file_count": 1,
        "rejected_v4_readable_held_file_count": 4,
        "rejected_v4_source_metadata_only_held_count": 3,
        "current_producer_metadata_only_held_count": 1,
        "consumer_installed_source_held_count": 1,
        "consumer_sealed_exec_memfd_held_count": 1,
        "public_candidate_verification_completion_held_file_count": 24,
        "public_candidate_verification_completion_held_directory_count": 5,
        "C42_full10_union_candidate9_held_file_count": 16,
        "C42_candidate_audit_install_held_directory_count": 3,
        "authority_seal_held_file_count": 1,
        "static_policy_held_file_count": 8,
        "v5_official_rejection_in_static_policy_held_file_count": 1,
        "terminal_deterministic_stage_absence_count": 5,
        "fresh_rejection_namespace_scan_count": 1,
    }
    need(set(ack) == expected_keys and ack.get("schema") == LIVE_ACK_SCHEMA and
         ack.get("status") ==
             "ACK_FINAL_DYNAMIC_CONJUNCTS_LIVE__ZERO_CREDIT__AWAIT_POSITIVE_WRAPPER_AND_RELEASE" and
         ack.get("protocol") == LIVE_PROTOCOL and
         ack.get("transaction_binding_domain") == TRANSACTION_BINDING_DOMAIN and
         ack.get("transaction_binding_sha256") ==
             request["transaction_binding_sha256"] and
         ack.get("request_object_sha256") == request["object_sha256"] and
         ack.get("inner_object_sha256") == request["inner_object_sha256"] and
         ack.get("wrapper_body_domain") == PREWRAPPER_BODY_DOMAIN and
         ack.get("wrapper_body_domain_sha256") ==
             request["wrapper_body_domain_sha256"] and
         ack.get("wrapper_object_sha256") == request["wrapper_object_sha256"] and
         ack.get("ack_binding_domain") == LIVE_ACK_BINDING_DOMAIN and
         ack.get("ack_binding_sha256") == _expected_ack_binding(request) and
         ack.get("final_dynamic_replay_census") == expected_census and
         ack.get("all_dynamic_conjuncts_live") is True and
         ack.get("wrapper_closed_and_schema_validated_before_request") is True and
         ack.get("wrapper_body_excludes_transaction_binding_request_ACK_and_RELEASE_to_avoid_hash_cycle") is True and
         ack.get("transaction_binding_is_replay_identical_not_fresh_or_random") is True and
         ack.get("static_v6_exact10_with_v5_exact10_and_official_rejection_v4_supersession_v3_exact10_and_official_rejection_terminal_replay_completed_by_launcher_before_request") is True and
         ack.get("launcher_empty_rejection_namespace_guard_terminally_replayed_before_request") is True and
         ack.get("consumer_exec_fd_is_fresh_sealed_memfd") is True and
         ack.get("consumer_exec_fd_distinct_from_installed_source_fd") is True and
         ack.get("consumer_exec_memfd_required_seals_valid") is True and
         ack.get("consumer_exec_bytes_equal_installed_source_bytes") is True and
         ack.get("consumer_exec_and_installed_source_terminal_replayed") is True and
         ack.get("positive_wrapper_emitted_by_combined_child") is False and
         ack.get("release_required_before_dynamic_guards_close") is True and
         ack.get("positive_wrapper_raw_fd1_final_newline_write_is_launcher_semantic_commit") is True and
         ack.get("post_ACK_RELEASE_and_child_exit_are_non_authority_cleanup") is True and
         ack.get("formal_global_closure_credit") == 0 and
         ack.get("D02_unlock") is False and raw == canonical(ack) + b"\n",
         "cold live ACK exact binding, census, zero-credit, and chronology")
    _validate_lock_ack(ack["official_writer_coordination_lock"], coordination)
    return ack


def run_authorize_child(
        bundle: HeldBundle, coordination: HeldCoordinationParent,
        rejection_guard: HeldEmptyRejectionNamespace) -> bool:
    source = bundle.by_path[CONSUMER]
    child_exec = HeldSealedChildExec(source)
    try:
        os.lseek(child_exec.fd, 0, os.SEEK_SET)
        process = subprocess.Popen(
            child_argv(child_exec, "authorize", []),
            stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            # Inherit stderr so a verbose rejecting child cannot deadlock on a
            # bounded stderr pipe while the two-phase stdout protocol is active.
            stderr=None,
            env=child_environment(bundle, child_exec, source, coordination),
            pass_fds=(child_exec.fd, source.fd, coordination.fd,
                      bundle.bootstrap.root_fd))
    except BaseException:
        child_exec.close()
        raise
    wrapper_committed = False
    positive_output_fd = -1
    try:
        need(process.stdin is not None and process.stdout is not None,
             "cold authorize dedicated bidirectional pipes")
        inner_raw = process.stdout.readline(32 * 1024 * 1024 + 1)
        if inner_raw == b"":
            # The first authorize call may install the frozen zero-credit
            # authority seal and intentionally emit nothing.  A clean child
            # exit is a successful non-authoritative operation.
            process.wait()
            need(process.returncode == 0,
                 "cold authorize zero-output seal installation")
            child_exec.terminal_replay()
            bundle.terminal_replay()
            rejection_guard.terminal_replay()
            coordination.verify()
            return False
        need(inner_raw.endswith(b"\n") and
             len(inner_raw) <= 32 * 1024 * 1024 and
             inner_raw.count(b"\n") == 1,
             "cold inner stdout:one bounded newline-terminated object")
        need(sys.stdout.buffer.fileno() == 1,
             "positive wrapper stdout is exact fd1")
        sys.stdout.buffer.flush()
        stdout_flags = fcntl.fcntl(1, fcntl.F_GETFL)
        stdout_info = os.fstat(1)
        need(stat.S_ISFIFO(stdout_info.st_mode) and
             not (stdout_flags & os.O_NONBLOCK) and os.get_blocking(1),
             "positive wrapper fd1 is a blocking pipe preflushed before final ACK")
        positive_output_fd = os.dup(1)
        held_stdout_info = os.fstat(positive_output_fd)
        held_stdout_flags = fcntl.fcntl(positive_output_fd, fcntl.F_GETFL)
        need((held_stdout_info.st_dev, held_stdout_info.st_ino, held_stdout_info.st_mode) ==
             (stdout_info.st_dev, stdout_info.st_ino, stdout_info.st_mode) and
             not (held_stdout_flags & os.O_NONBLOCK) and
             os.get_blocking(positive_output_fd),
             "held duplicate of prevalidated blocking positive-output pipe")
        child_exec.terminal_replay()
        root, inner = cold_root(bundle, coordination, child_exec, inner_raw)
        root_raw = canonical(root) + b"\n"
        need(root_raw.endswith(b"\n") and root_raw.count(b"\n") == 1,
             "preclosed wrapper exact canonical line")
        wrapper_body_sha256 = _wrapper_body_domain_sha256(root)
        transaction_binding = _deterministic_transaction_binding(
            bundle, inner["object_sha256"], wrapper_body_sha256,
            root["object_sha256"])
        # Absolute last launcher-side static gate.  The child performs the
        # complete dynamic replay only after receiving the bound request.
        bundle.terminal_replay()
        child_exec.terminal_replay()
        rejection_guard.terminal_replay()
        coordination.verify()
        request = close_object({
            "schema": LIVE_REQUEST_SCHEMA,
            "status": "REQUEST_FINAL_DYNAMIC_LIVE_ACK_BEFORE_POSITIVE_WRAPPER_OUTPUT",
            "protocol": LIVE_PROTOCOL,
            "transaction_binding_domain": TRANSACTION_BINDING_DOMAIN,
            "transaction_binding_sha256": transaction_binding,
            "inner_object_sha256": inner["object_sha256"],
            "wrapper_body_domain": PREWRAPPER_BODY_DOMAIN,
            "wrapper_body_domain_sha256": wrapper_body_sha256,
            "wrapper_object_sha256": root["object_sha256"],
            "wrapper_closed_and_schema_validated_before_request": True,
            "wrapper_body_excludes_transaction_binding_request_ACK_and_RELEASE_to_avoid_hash_cycle": True,
            "transaction_binding_is_replay_identical_not_fresh_or_random": True,
            "static_v6_exact10_with_v5_exact10_and_official_rejection_v4_supersession_v3_exact10_and_official_rejection_terminal_replay_completed_by_launcher_before_request": True,
            "launcher_empty_rejection_namespace_guard_terminally_replayed_before_request": True,
        })
        request_raw = canonical(request) + b"\n"
        written = process.stdin.write(request_raw)
        need(written == len(request_raw), "complete cold live request write")
        process.stdin.flush()
        ack_raw = _read_child_line(process.stdout, "cold final-dynamic ACK")
        ack = _validate_live_ack(ack_raw, request, coordination)

        # Fully prepare the non-authoritative cleanup message before the
        # positive stdout commit.  Failure here still exposes no wrapper.
        release = close_object({
            "schema": LIVE_RELEASE_SCHEMA,
            "status": "RELEASE_AFTER_POSITIVE_WRAPPER_RAW_FD1_FINAL_NEWLINE_COMMIT",
            "protocol": LIVE_PROTOCOL,
            "transaction_binding_sha256":
                request["transaction_binding_sha256"],
            "inner_object_sha256": request["inner_object_sha256"],
            "wrapper_body_domain_sha256": request["wrapper_body_domain_sha256"],
            "wrapper_object_sha256": request["wrapper_object_sha256"],
            "ack_object_sha256": ack["object_sha256"],
        })
        release_raw = canonical(release) + b"\n"

        # No schema, filesystem, subprocess-status, or semantic gate follows
        # the validated ACK before exposure.  The launcher-owned lock remains
        # held even if the child crashes in this tiny output window.
        view = memoryview(root_raw)
        offset = 0
        while offset < len(view):
            try:
                written = os.write(positive_output_fd, view[offset:])
            except InterruptedError:
                continue
            need(written > 0, "positive wrapper raw fd1 made forward progress")
            offset += written
        # The semantic commit is the successful raw write of the final newline.
        # From this assignment onward there is no authority-determining gate.
        wrapper_committed = True

        # From the raw final-newline commit onward cleanup cannot revoke or downgrade the
        # already valid wrapper.  Keep the launcher lock while making a
        # best-effort bound RELEASE and reaping the child; do not apply another
        # authority gate after the semantic commit.
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
            # The wrapper's final raw newline is the semantic commit.  Every
            # operation below is strictly best-effort resource cleanup and
            # cannot turn that already exposed line back into a rejection.
            try:
                if process.stdin is not None and not process.stdin.closed:
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
            if process.stdin is not None and not process.stdin.closed:
                process.stdin.close()
            if process.poll() is None:
                process.terminate()
                process.wait()
            process.stdout.close()
            if positive_output_fd >= 0:
                os.close(positive_output_fd)
        # If wrapper exposure failed, the lock still remained held throughout
        # cleanup.  If it succeeded, RELEASE and child cleanup occurred before
        # the caller finally unlocks the coordination parent.
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
    cli.add_argument("--bootstrap-exec-fd", required=True, type=int,
                     help=argparse.SUPPRESS)
    cli.add_argument("--bootstrap-source-fd", required=True, type=int,
                     help=argparse.SUPPRESS)
    cli.add_argument("--bootstrap-root-fd", required=True, type=int,
                     help=argparse.SUPPRESS)
    cli.add_argument("--cold-workspace-root", required=True,
                     help=argparse.SUPPRESS)
    cli.add_argument("--expected-launcher-sha256", required=True)
    sub = cli.add_subparsers(dest="command", required=True)
    build = sub.add_parser("build")
    build.add_argument("--outdir", required=True)
    verify = sub.add_parser("verify")
    verify.add_argument("--orientation", required=True, choices=("a", "b"))
    sub.add_parser("assemble")
    sub.add_parser("authorize")
    sub.add_parser("reject")
    return cli


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    inherited = (args.bootstrap_exec_fd, args.bootstrap_source_fd,
                 args.bootstrap_root_fd)
    try:
        bootstrap = HeldBootstrapEntry(
            args.bootstrap_exec_fd, args.bootstrap_source_fd,
            args.bootstrap_root_fd, args.cold_workspace_root,
            args.expected_launcher_sha256)
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
        if args.command == "reject":
            install_or_replay_launcher_native_rejection(
                bootstrap, coordination)
            return 0
        # Every positive-capable command holds the exact-empty v6 rejection
        # namespace before any current or historical bundle file is opened.
        rejection_guard = HeldEmptyRejectionNamespace(coordination)
        bundle = HeldBundle(
            args.expected_launcher_sha256, coordination, bootstrap)
        if args.command == "build":
            stdout = run_non_authorize_child(
                bundle, coordination, rejection_guard,
                "build", ["--outdir", args.outdir])
        elif args.command == "verify":
            stdout = run_non_authorize_child(
                bundle, coordination, rejection_guard,
                "verify", ["--orientation", args.orientation])
        elif args.command == "assemble":
            stdout = run_non_authorize_child(
                bundle, coordination, rejection_guard, "assemble", [])
        else:
            wrapper_committed = run_authorize_child(
                bundle, coordination, rejection_guard)
            stdout = b""
        if args.command != "authorize":
            need(not stdout, "non-root cold child unexpectedly wrote stdout")
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


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Reject as exc:
        print("REJECT:", exc, file=sys.stderr)
        raise SystemExit(2)
