#!/usr/bin/env python3
"""Read-only, fail-closed static review for the C79g v14 successor.

The protocol sources are read as inert bytes and are never imported or
executed.  Python validation is limited to AST parsing, symtable analysis and
in-memory ``compile``.  JSON surfaces are decoded with duplicate-key tracking.

This reviewer deliberately distinguishes a safe draft state from a final
static bundle.  A draft may pass the absence/disabled checks, but the overall
result remains FAIL_CLOSED until all four v14 JSON surfaces exist, close, and
all three final pin flags are true.  Publication and runtime are never
authorized by this program.
"""

from __future__ import annotations

import ast
import builtins
import copy
import hashlib
import json
import os
import re
import stat
import symtable
from pathlib import Path
from typing import Any, Iterable, Mapping


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "deliverables"
RUNTIME = ROOT / ".cm2-runtime"
BASE = "cm2_round306c79g_true_global_no_producer_consumer"
CHECKPOINT = (
    "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab")

V14_PYTHON = {
    "producer": OUT / f"{BASE}_v14.py",
    "consumer": OUT / (
        f"{BASE}_independent_verifier_assembler_authority_consumer_v14.py"),
    "launcher": OUT / f"{BASE}_cold_launch_v14.py",
}
V14_PYC_DIRECTORY = OUT / "__pycache__"
V14_JSON = {
    "schema": OUT / f"{BASE}_schema_v14.json",
    "contract": OUT / f"{BASE}_contract_v14.json",
    "transition": OUT / f"{BASE}_v13_to_v14_static_launch_transition_receipt_v1.json",
    "audit": OUT / f"{BASE}_static_audit_v14.json",
}
V14_MANIFEST = OUT / f"{BASE}_cold_launch_manifest_v14.sha256"
V14_OUTER = OUT / f"{BASE}_cold_launch_outer_receipt_v14.json"
V14_JSON_BUILDER = ROOT / "scripts" / "c79g_v14_json_draft_builder.py"
V5_REJECTION = RUNTIME / f"c79g-v5-rejections-{CHECKPOINT}" / "rejection.json"
V12_REJECTION = RUNTIME / f"c79g-v12-rejections-{CHECKPOINT}" / "rejection.json"
V13_SUPERSESSION_RECEIPT = OUT / (
    f"{BASE}_v13_prepublication_pyc_contamination_rejection_"
    "supersession_receipt_v1.json")

EXPECTED_V12_REJECTION_FILE_SHA256 = (
    "b6b087a3e31b25f0bbe0ffe6caa40f3c181b2f77c5c8b6169ce3af27439762b5")
EXPECTED_V12_REJECTION_OBJECT_SHA256 = (
    "18951895ea97f455bc3294e8ef9cdaa937f3b16e9831275b047e88142e9b91f6")
EXPECTED_V13_SUPERSESSION_RECEIPT_FILE_SHA256 = (
    "098296d9807a89f58250f4fd404bdd45b1cf343e3e2e1c7a51a24d67225d016f")
EXPECTED_V13_SUPERSESSION_RECEIPT_OBJECT_SHA256 = (
    "3c9c44500465c6b416cc0ee6689ea82cdd9096a79687b94f94c409ca5a78c677")
EXPECTED_V13_EXACT16_CANONICAL_SHA256 = (
    "bf70829a4632cd322ef45e9313d4150138a57f98966fcd93d2c7a718fb44f64e")
EXPECTED_V13_NORMALIZED_EXACT10_CANONICAL_SHA256 = (
    "600768327003f17f0f367e64b03d0fd9ada23f2933db64845a37cfee140c61b5")
EXPECTED_V5_REJECTION_FILE_SHA256 = (
    "c49218967b2d5023d07e5c65fa53df12f0383d6644bf4bd7d35a8e50abeb85b5")
EXPECTED_V5_REJECTION_OBJECT_SHA256 = (
    "9a94bf8b580f6145c4977dd335d9a63c69057d18d62678ab47c7916c764f8e4c")
EXPECTED_EXACT39_KEYSET_SHA256 = (
    "3b74017677a537d23cacbfbf95f1cc78e3b33fc4839be24e02e848bdd7410460")
EXPECTED_EXACT56_KEYSET_SHA256 = (
    "9c272f16d92497a7c5ced499e9e42c514b81cbfddcdb3f79c4f33837836e057e")
EXPECTED_V12_INCIDENT_HELPER_AST_SHA256 = (
    "fa4cf4f0bdb9e9f1b2a3bdeed7d7271830833395a2f58d32457f363e596fb5e9")

HISTORICAL_REJECTION_PINS = {
    "v3": (
        "57ce7a4361555c4ff403f725f17ef9cef50446a2e76d7086635c30a0f17bc62f",
        "c946e0d8170a75e32aa7031b42cf0dd5b7b585ba463b7b1ce0010cb65bb3b421",
        37, "21ba021c649349266d95670e63136fef1772b5d8dbb79334907c9df400620a18"),
    "v5": (
        "c49218967b2d5023d07e5c65fa53df12f0383d6644bf4bd7d35a8e50abeb85b5",
        "9a94bf8b580f6145c4977dd335d9a63c69057d18d62678ab47c7916c764f8e4c",
        39, "3b74017677a537d23cacbfbf95f1cc78e3b33fc4839be24e02e848bdd7410460"),
    "v6": (
        "3559dcfd9e6d0ebb0e093226d6d3ae8d09d67eaeb186d4ec956241af87fcbd06",
        "87c0cd17ae6ca3885a01da82b47b66e96419eb778594b51423eb04cf3c68f48c",
        41, "5881a652aabef3e7e65917689487f13b99bfa60fff0ebb7c144bc02b26897638"),
    "v7": (
        "63d4bbc4f50ef674b6b90f6fde625ac4705d5272f500fd495111d445274ebf6b",
        "29c43ad51082bd56c2291dea88b619731c2853969b79ea008abea1cca3c83ecd",
        43, "02b54c94602de1f5af8e545692f44815b9ac3ba334369dd96ee4e9b677bf1308"),
    "v8": (
        "3b00a60c6c30cc10171d82e8262f880d67aa975e9f040888a29d7bdb4014ef95",
        "9fbc65609f33a62751b9fc60aa4def316a499dae9e3f64e1d4ae8a3be58894d5",
        46, "a1da14307b813345ee0f8877550412b40951f7857e5972570ab41f97e2fe31bf"),
    "v9": (
        "bca8f1042a1f3ee5b82d85a2e10c6ed2bf35d486116870bf50387f9ee9dcd302",
        "682ead5d02c386b992c15e1e845e5e35a3147e0c1387d440c604f431c7a8b1b4",
        48, "d0617183e15fd4c5bfd3495d7dca56cb9aea7035bedf35a1bdf6efd166a70308"),
    "v10": (
        "1b5bbd9ec04f07e7d7d433685aa693b73bf2315a91e4813960bd5a81e8112828",
        "efdb614e870e70c20202834d3c6ec1a7513a3e98ba5cb4e1b32f87976a529d76",
        50, "01274ec0c36bd85423d385bdb22cdff7fe6ccfe2d114864994fc2ead2153eddb"),
    "v11": (
        "f6cc10d8b7e72553ef0b7a32bbfb99255f36cce16b735002f17be58ae51d3bc8",
        "7ae86e38c5910bc9ceaa0a4e5cb1f8fbbf1e73de9c0314fedabbd8cb2db3bb7a",
        52, "75ca9378fbff7a6956686e7390556fffa3d6ff939630ed47e8c8c185872e97f8"),
    "v12": (
        EXPECTED_V12_REJECTION_FILE_SHA256,
        EXPECTED_V12_REJECTION_OBJECT_SHA256,
        54, "271055dec2aa42fb77c14bbd9b5c19e6bd4281428a71dc5db55c7d0db168b985"),
}
HISTORICAL_REJECTION_VERSION_ORDER = tuple(HISTORICAL_REJECTION_PINS)

INCIDENT_FD_ENV_NAMES = (
    "V10_PRODUCER_FD_ENV", "V9_LAUNCHER_FD_ENV",
    "V11_PRODUCER_FD_ENV", "V11_LAUNCHER_FD_ENV",
    "V11_REJECTION_FD_ENV", "V12_PRODUCER_FD_ENV",
    "V12_CONSUMER_FD_ENV", "V12_LAUNCHER_FD_ENV",
    "V5_REJECTION_FD_ENV", "V12_REJECTION_FD_ENV",
    "V13_PRODUCER_FD_ENV", "V13_CONSUMER_FD_ENV",
    "V13_LAUNCHER_FD_ENV", "V13_PRODUCER_PYC_FD_ENV",
    "V13_CONSUMER_PYC_FD_ENV", "V13_LAUNCHER_PYC_FD_ENV",
    "V13_SUPERSESSION_RECEIPT_FD_ENV",
)
EXPECTED_INCIDENT_HELPER_CALLSITES = {
    "producer": [
        ("HeldSelf", "__init__", 5),
        ("HeldSelf", "terminal_replay", 5),
    ],
    "consumer": [
        ("HeldInheritedIncidentAuthorityExact17", "__init__", 5),
        ("HeldInheritedIncidentAuthorityExact17", "terminal_replay", 5),
    ],
    "launcher": [
        ("HeldV12PredecessorExact10", "bind_history", 5),
        ("HeldV12PredecessorExact10", "terminal_replay", 5),
    ],
}

# The v12 published exact10 is immutable predecessor evidence.  The v12
# official rejection is intentionally separate and strictly later.
V12_EXACT10 = (
    (f".cm2-runtime/c79g-v11-rejections-{CHECKPOINT}/rejection.json",
     "f6cc10d8b7e72553ef0b7a32bbfb99255f36cce16b735002f17be58ae51d3bc8",
     "7ae86e38c5910bc9ceaa0a4e5cb1f8fbbf1e73de9c0314fedabbd8cb2db3bb7a"),
    (f"deliverables/{BASE}_schema_v12.json",
     "5ed911a55e8f90e750fdcaf6ab4fb6c9683bebaf66a4d6250329dff98acb2e28", None),
    (f"deliverables/{BASE}_contract_v12.json",
     "72246725b15891f92cbc6e3fa1c07ab4a76cdaa19f1b366a736f47f51989b343",
     "f5c1710817dc8e3aa7fe2bbf4b88e6e39baaa1b17bbeb0f8bf37c8c4575ae5d7"),
    (f"deliverables/{BASE}_v12.py",
     "4cafc594f8a60063b7e7caaa82ddcc2b7983d0fbf0929034cd3cb5f360f3ed1d", None),
    (f"deliverables/{BASE}_independent_verifier_assembler_authority_consumer_v12.py",
     "b74dee738257d485e9ca3357d7d138b5175b95e58f1c8ea87d1eca7bfc96b2ed", None),
    (f"deliverables/{BASE}_v11_to_v12_static_launch_transition_receipt_v1.json",
     "45dabc1ef60eb2f8ba34aa7daa69f9d2b3bedccd4168d9c472bd4bbb696b5400",
     "0673ecafaa9991cd78e905e144e7c8c1b91717a3d753befa13e82552d44a4072"),
    (f"deliverables/{BASE}_static_audit_v12.json",
     "ac29b1e31e0d1b51e8610b7699d1aaf55c80fa6f13f00b20b209c2889e121d37",
     "c1473ae0f5a08d8772227f61a55bd32c479a7b5c7d40da17b37e796abf4d9783"),
    (f"deliverables/{BASE}_cold_launch_v12.py",
     "b7aaff67be866f8fd7a01f71e97ea1491574f69e62b7760b6ced9183997444ba", None),
    (f"deliverables/{BASE}_cold_launch_manifest_v12.sha256",
     "297e9f58dc7657c6fa959dd45081efffe4e7e8dadcd16ab89457863e2661ece6", None),
    (f"deliverables/{BASE}_cold_launch_outer_receipt_v12.json",
     "27129990a9d5b6697fd13ee8e2086100cbf158f12e5b767166d771e63088b6d0",
     "bc6d06141865954590bd11bfc96ad59dbbffa003f568355ecb47155a8a3a809d"),
)

# Receipt-defined inherited exact16.  The first ten are the normalized
# historical incident authority, followed by the frozen v13 source/pyc exact6.
EXPECTED_V13_EXACT16 = (
    ("v10_producer", f"deliverables/{BASE}_v10.py",
     "99bb321da8a63855e52c8d6757d00886c0deeb2182f5044cac35f645e2ebd00a"),
    ("v9_launcher", f"deliverables/{BASE}_cold_launch_v9.py",
     "f7559ceeb7d491b8489812670392cb63e3cd5f6a2764db469e2dd51d6b5577fa"),
    ("v11_producer", f"deliverables/{BASE}_v11.py",
     "f3b364afc0f5b2f729a3d7786eb8e9c25a9303959d6d2464a40395968090a30b"),
    ("v11_launcher", f"deliverables/{BASE}_cold_launch_v11.py",
     "9f6971d2ca3e2c8f448a6aeed70bc16f38154c626f7744a4e20ba723e3082cc2"),
    ("v11_rejection", f".cm2-runtime/c79g-v11-rejections-{CHECKPOINT}/rejection.json",
     "f6cc10d8b7e72553ef0b7a32bbfb99255f36cce16b735002f17be58ae51d3bc8"),
    ("v12_producer", f"deliverables/{BASE}_v12.py",
     "4cafc594f8a60063b7e7caaa82ddcc2b7983d0fbf0929034cd3cb5f360f3ed1d"),
    ("v12_consumer",
     f"deliverables/{BASE}_independent_verifier_assembler_authority_consumer_v12.py",
     "b74dee738257d485e9ca3357d7d138b5175b95e58f1c8ea87d1eca7bfc96b2ed"),
    ("v12_launcher", f"deliverables/{BASE}_cold_launch_v12.py",
     "b7aaff67be866f8fd7a01f71e97ea1491574f69e62b7760b6ced9183997444ba"),
    ("v5_rejection", f".cm2-runtime/c79g-v5-rejections-{CHECKPOINT}/rejection.json",
     "c49218967b2d5023d07e5c65fa53df12f0383d6644bf4bd7d35a8e50abeb85b5"),
    ("v12_rejection", f".cm2-runtime/c79g-v12-rejections-{CHECKPOINT}/rejection.json",
     EXPECTED_V12_REJECTION_FILE_SHA256),
    ("v13_build_only_producer_source", f"deliverables/{BASE}_v13.py",
     "ec4982babaec3bfb6693e29a220ca827087fb591c77f6c715889e934f124310e"),
    ("v13_independent_consumer_source",
     f"deliverables/{BASE}_independent_verifier_assembler_authority_consumer_v13.py",
     "a8b32b7e0073e70a95e6f5f17ad08b63b701ca64a1299f0f614215c5aa9f970a"),
    ("v13_cold_launcher_source", f"deliverables/{BASE}_cold_launch_v13.py",
     "aa1306ed3e764c69679db531c3dcd30d609ed1cbd699feda5ed17cc1e24da88b"),
    ("v13_build_only_producer_pyc",
     f"deliverables/__pycache__/{BASE}_v13.cpython-312.pyc",
     "0383cab58260ff076b18482f2077ed100456b21bcc2587afd5e457c8a19d7d36"),
    ("v13_independent_consumer_pyc",
     f"deliverables/__pycache__/{BASE}_independent_verifier_assembler_authority_consumer_v13.cpython-312.pyc",
     "f13c8f7f40139bcbe6d5f20014fb14d8659539814baf985f73f99fbb13ffccaa"),
    ("v13_cold_launcher_pyc",
     f"deliverables/__pycache__/{BASE}_cold_launch_v13.cpython-312.pyc",
     "50a210fe6c414d140f7e0ac9a969500192f68fafae2de9d104526d73479365e0"),
)

EXACT39_KEYS = frozenset({
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

V12_REJECTION_KEYS = frozenset(
    set(EXACT39_KEYS) |
    {f"v{version}_official_rejection_{kind}_sha256"
     for version in range(5, 12) for kind in ("file", "object")} |
    {"v7_publication_lock_continuity_incident_object_sha256"})
EXACT56_KEYS = frozenset(
    set(V12_REJECTION_KEYS) |
    {"v12_official_rejection_file_sha256",
     "v12_official_rejection_object_sha256"})

EXPECTED_PREDECESSOR_IDENTITY_COUNT = 105
EXPECTED_PREPUBLICATION_IDENTITY_COUNT = 113
EXPECTED_TERMINAL_IDENTITY_COUNT = 115
EXPECTED_RUNTIME_GROUP_VECTOR = [10] * 10 + [7, 1, 3, 3, 1]
HEX64 = re.compile(r"^[0-9a-f]{64}$")
MISSING = object()


def canonical(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True,
        separators=(",", ":")).encode("utf-8")


def sha_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def identity(value: os.stat_result) -> tuple[int, ...]:
    return (
        value.st_dev, value.st_ino, value.st_mode, value.st_nlink,
        value.st_size, value.st_mtime_ns, value.st_ctime_ns,
    )


def read_stable(path: Path) -> tuple[bytes, tuple[int, ...]]:
    flags = os.O_RDONLY | os.O_CLOEXEC | getattr(os, "O_NOFOLLOW", 0)
    descriptor = os.open(path, flags)
    try:
        before = os.fstat(descriptor)
        if not stat.S_ISREG(before.st_mode):
            raise ValueError(f"not a regular file: {path}")
        chunks: list[bytes] = []
        while True:
            chunk = os.read(descriptor, 1 << 20)
            if not chunk:
                break
            chunks.append(chunk)
        after = os.fstat(descriptor)
        raw = b"".join(chunks)
        if identity(before) != identity(after) or len(raw) != before.st_size:
            raise ValueError(f"identity changed during held read: {path}")
        return raw, identity(before)
    finally:
        os.close(descriptor)


def decode_json(raw: bytes, label: str) -> tuple[Any, list[str]]:
    duplicates: list[str] = []

    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in items:
            if key in result:
                duplicates.append(key)
            result[key] = value
        return result

    value = json.loads(raw.decode("utf-8"), object_pairs_hook=pairs)
    return value, duplicates


def object_closure(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict) or not isinstance(value.get("object_sha256"), str):
        return {"declared": None, "computed": None, "matches": False}
    work = copy.deepcopy(value)
    declared = work.pop("object_sha256")
    computed = sha_bytes(canonical(work))
    return {"declared": declared, "computed": computed,
            "matches": declared == computed}


def v13_supersession_receipt_review(
        raw: bytes, value: Any, duplicates: list[str]) -> dict[str, Any]:
    closure = object_closure(value)
    expected_records = [
        {"ordinal": ordinal, "role": role, "path": path,
         "file_sha256": file_pin}
        for ordinal, (role, path, file_pin) in enumerate(
            EXPECTED_V13_EXACT16, start=1)]
    successor = value.get("v14_successor_contract", {}) \
        if isinstance(value, dict) else {}
    inherited = successor.get("inherited_incident_authority_exact16", {}) \
        if isinstance(successor, dict) else {}
    normalized = value.get(
        "frozen_v13_inherited_incident_authority_exact10_source_contract", {}) \
        if isinstance(value, dict) else {}
    records_raw = canonical(expected_records)
    matches = (
        isinstance(value, dict) and not duplicates and
        sha_bytes(raw) == EXPECTED_V13_SUPERSESSION_RECEIPT_FILE_SHA256 and
        raw == canonical(value) + b"\n" and closure["matches"] and
        closure["declared"] == EXPECTED_V13_SUPERSESSION_RECEIPT_OBJECT_SHA256 and
        value.get("schema") ==
            "cm2.round306c79g.true-global-no-producer-consumer."
            "v13-prepublication-pyc-contamination-rejection-supersession-"
            "receipt.v1" and
        value.get("status") ==
            "FROZEN_APPEND_ONLY_V13_PREPUBLICATION_PYC_CONTAMINATION_"
            "REJECTION__V14_SUCCESSOR_ONLY" and
        value.get("receipt_path") ==
            str(V13_SUPERSESSION_RECEIPT.relative_to(ROOT)) and
        value.get("effective_checkpoint_object_sha256") == CHECKPOINT and
        inherited.get("ordered_members") == expected_records and
        inherited.get("ordered_member_count") == 16 and
        inherited.get("ordered_member_exact_keys") ==
            ["ordinal", "role", "path", "file_sha256"] and
        len(records_raw) == 3646 and
        sha_bytes(records_raw) ==
            inherited.get("ordered_exact16_canonical_sha256") ==
            EXPECTED_V13_EXACT16_CANONICAL_SHA256 and
        normalized.get("normalized_ordered_member_count") == 10 and
        normalized.get("normalized_exact10_canonical_byte_length") == 2657 and
        normalized.get("normalized_exact10_canonical_sha256") ==
            EXPECTED_V13_NORMALIZED_EXACT10_CANONICAL_SHA256 and
        successor.get("v14_current_exact8_first_member_must_be_this_receipt")
            is True and
        successor.get("v14_must_preserve_v12_exact10_and_official_rejection")
            is True and
        successor.get("v14_predecessor_unique_live_identity_count") == 105 and
        successor.get("v14_prepublication_unique_live_identity_count") == 113 and
        successor.get("v14_terminal_unique_live_identity_count") == 115 and
        successor.get("v14_terminal_group_vector") ==
            EXPECTED_RUNTIME_GROUP_VECTOR and
        inherited.get(
            "v14_must_live_hold_and_terminally_replay_exact16_plus_this_receipt")
            is True)
    return {
        "file_sha256": sha_bytes(raw),
        "object_closure": closure,
        "duplicate_keys": duplicates,
        "expected_exact16": expected_records,
        "ordered_exact16_canonical_sha256": sha_bytes(records_raw),
        "matches": matches,
    }


class Report:
    def __init__(self) -> None:
        self.checks: list[dict[str, Any]] = []

    def add(self, name: str, passed: bool, **details: Any) -> None:
        row: dict[str, Any] = {"name": name, "passed": bool(passed)}
        if details:
            row["details"] = details
        self.checks.append(row)

    def finish(self, sections: Mapping[str, Any]) -> dict[str, Any]:
        failures = [row["name"] for row in self.checks if not row["passed"]]
        return {
            "schema": "cm2.c79g.v14.independent-read-only-static-review.v1",
            "status": (
                "PASS_STATIC_BYTES__RUNTIME_NOT_AUTHORIZED"
                if not failures else
                "FAIL_CLOSED_STATIC_REVIEW__RUNTIME_NOT_AUTHORIZED"),
            "read_only": True,
            "protocol_python_imported_or_executed": False,
            "protocol_or_runtime_files_written": False,
            "root": str(ROOT),
            "check_count": len(self.checks),
            "failed_check_count": len(failures),
            "failed_checks": failures,
            "checks": self.checks,
            "sections": dict(sections),
        }


def module_assignments(tree: ast.Module) -> dict[str, list[ast.AST]]:
    result: dict[str, list[ast.AST]] = {}
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    result.setdefault(target.id, []).append(node.value)
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            result.setdefault(node.target.id, []).append(node.value)
    return result


def safe_literal(node: ast.AST | None, env: Mapping[str, Any]) -> Any:
    if node is None:
        return MISSING
    try:
        return ast.literal_eval(node)
    except (ValueError, TypeError, SyntaxError, MemoryError, RecursionError):
        pass
    if isinstance(node, ast.Name):
        return env.get(node.id, MISSING)
    if isinstance(node, ast.BinOp) and isinstance(
            node.op, (ast.Add, ast.Mult, ast.BitOr, ast.Sub)):
        left, right = safe_literal(node.left, env), safe_literal(node.right, env)
        if left is MISSING or right is MISSING:
            return MISSING
        try:
            if isinstance(node.op, ast.Add):
                return left + right
            if isinstance(node.op, ast.Mult):
                return left * right
            if isinstance(node.op, ast.Sub):
                return left - right
            return left | right
        except (TypeError, ValueError, OverflowError):
            return MISSING
    if isinstance(node, (ast.Tuple, ast.List, ast.Set)):
        values = [safe_literal(item, env) for item in node.elts]
        if any(value is MISSING for value in values):
            return MISSING
        if isinstance(node, ast.Tuple):
            return tuple(values)
        if isinstance(node, ast.List):
            return values
        try:
            return set(values)
        except TypeError:
            return MISSING
    if isinstance(node, ast.Dict):
        result: dict[Any, Any] = {}
        for key_node, value_node in zip(node.keys, node.values):
            if key_node is None:
                return MISSING
            key, value = safe_literal(key_node, env), safe_literal(value_node, env)
            if key is MISSING or value is MISSING:
                return MISSING
            try:
                result[key] = value
            except TypeError:
                return MISSING
        return result
    if (isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and
            node.func.id in {"tuple", "list", "set", "frozenset"} and
            len(node.args) in {0, 1} and not node.keywords):
        value = safe_literal(node.args[0], env) if node.args else ()
        if value is MISSING:
            return MISSING
        try:
            return {"tuple": tuple, "list": list, "set": set,
                    "frozenset": frozenset}[node.func.id](value)
        except (TypeError, ValueError):
            return MISSING
    if (isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and
            node.func.id == "sorted" and len(node.args) == 1 and
            not node.keywords):
        value = safe_literal(node.args[0], env)
        if value is MISSING:
            return MISSING
        try:
            return sorted(value)
        except (TypeError, ValueError):
            return MISSING
    return MISSING


def literal_environment(tree: ast.Module) -> dict[str, Any]:
    assignments = module_assignments(tree)
    env: dict[str, Any] = {}
    for _ in range(max(2, len(assignments))):
        changed = False
        for name, nodes in assignments.items():
            if len(nodes) != 1 or name in env:
                continue
            value = safe_literal(nodes[0], env)
            if value is not MISSING:
                env[name] = value
                changed = True
        if not changed:
            break
    return env


def dict_literal_stats(tree: ast.Module, label: str) -> dict[str, Any]:
    duplicate_rows: list[dict[str, Any]] = []
    count = 0
    for node in ast.walk(tree):
        if not isinstance(node, ast.Dict):
            continue
        count += 1
        seen: dict[Any, int] = {}
        for index, key_node in enumerate(node.keys):
            if key_node is None:
                continue
            try:
                key = ast.literal_eval(key_node)
                if key in seen:
                    duplicate_rows.append({
                        "source": label, "line": node.lineno,
                        "key": repr(key), "first_index": seen[key],
                        "second_index": index,
                    })
                else:
                    seen[key] = index
            except (ValueError, TypeError, SyntaxError, MemoryError, RecursionError):
                continue
    return {"dict_literal_count": count,
            "duplicate_count": len(duplicate_rows),
            "duplicates": duplicate_rows}


def undefined_globals(source: str, label: str) -> list[str]:
    table = symtable.symtable(source, label, "exec")
    definitions = {
        symbol.get_name() for symbol in table.get_symbols()
        if (symbol.is_assigned() or symbol.is_imported() or
            symbol.is_namespace() or symbol.is_parameter())
    }
    allowed = set(dir(builtins)) | {
        "__file__", "__name__", "__package__", "__spec__", "__loader__",
        "__builtins__", "__annotations__", "__cached__",
    }
    bad: set[str] = set()

    def walk(scope: symtable.SymbolTable) -> None:
        for symbol in scope.get_symbols():
            if (symbol.is_referenced() and symbol.is_global() and
                    symbol.get_name() not in definitions | allowed):
                bad.add(symbol.get_name())
        for child in scope.get_children():
            walk(child)

    walk(table)
    return sorted(bad)


def literal_strings(tree: ast.Module) -> set[str]:
    return {
        node.value for node in ast.walk(tree)
        if isinstance(node, ast.Constant) and isinstance(node.value, str)}


def comparison_has_name_and_set_gate(node: ast.Compare, name: str) -> bool:
    parts = [node.left, *node.comparators]
    has_name = any(
        isinstance(item, ast.Name) and item.id == name
        for part in parts for item in ast.walk(part))
    has_set = any(
        isinstance(item, ast.Call) and isinstance(item.func, ast.Name) and
        item.func.id == "set" and len(item.args) == 1
        for part in parts for item in ast.walk(part))
    return has_name and has_set


def is_len_equals(node: ast.Compare, expected: int) -> ast.AST | None:
    parts = [node.left, *node.comparators]
    for left, right in zip(parts, parts[1:]):
        pairs = ((left, right), (right, left))
        for call, constant in pairs:
            if (isinstance(call, ast.Call) and isinstance(call.func, ast.Name) and
                    call.func.id == "len" and len(call.args) == 1 and
                    not call.keywords and isinstance(constant, ast.Constant) and
                    type(constant.value) is int and constant.value == expected):
                return call.args[0]
    return None


def parent_map(tree: ast.Module) -> dict[ast.AST, ast.AST]:
    result: dict[ast.AST, ast.AST] = {}
    for node in ast.walk(tree):
        for child in ast.iter_child_nodes(node):
            result[child] = node
    return result


def owner_chain(node: ast.AST, parents: Mapping[ast.AST, ast.AST]) -> list[str]:
    names: list[str] = []
    current = node
    while current in parents:
        current = parents[current]
        if isinstance(current, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            names.append(current.name)
    return names


def stale_v5_len52_rows(tree: ast.Module, role: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    parents = parent_map(tree)
    all_rows: list[dict[str, Any]] = []
    stale: list[dict[str, Any]] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Compare):
            continue
        argument = is_len_equals(node, 52)
        if argument is None:
            continue
        owners = owner_chain(node, parents)
        expression = ast.unparse(argument)
        row = {"role": role, "line": node.lineno,
               "len_argument": expression, "owner_chain": owners}
        all_rows.append(row)
        haystack = " ".join([expression, *owners]).lower()
        if "v5" in haystack:
            stale.append(row)
    return all_rows, stale


def exact39_gate_counts(tree: ast.Module) -> dict[str, int]:
    set_gates = sum(
        comparison_has_name_and_set_gate(node, "V5_OFFICIAL_REJECTION_EXACT39_KEYS")
        for node in ast.walk(tree) if isinstance(node, ast.Compare))
    len39 = sum(
        is_len_equals(node, 39) is not None and
        any(isinstance(item, ast.Name) and
            item.id == "V5_OFFICIAL_REJECTION_EXACT39_KEYS"
            for item in ast.walk(node))
        for node in ast.walk(tree) if isinstance(node, ast.Compare))
    return {"set_equality_gate_count": set_gates,
            "derived_len39_gate_count": len39}


def frozen_literal_exact39_gate_count(tree: ast.Module) -> int:
    """Count historical set(value)==literal/local exact39-keyset gates."""
    parents = parent_map(tree)

    def enclosing_function(node: ast.AST) -> ast.AST | None:
        cursor = node
        while cursor in parents:
            cursor = parents[cursor]
            if isinstance(cursor, (ast.FunctionDef, ast.AsyncFunctionDef)):
                return cursor
        return None

    def resolve_keyset(node: ast.AST, owner: ast.AST | None) -> Any:
        value = safe_literal(node, {})
        if value is not MISSING:
            return value
        if isinstance(node, ast.Name) and isinstance(
                owner, (ast.FunctionDef, ast.AsyncFunctionDef)):
            assignments = [
                item.value for item in owner.body
                if isinstance(item, ast.Assign) and
                any(isinstance(target, ast.Name) and target.id == node.id
                    for target in item.targets)]
            if len(assignments) == 1:
                return safe_literal(assignments[0], {})
        return MISSING

    count = 0
    for compare in ast.walk(tree):
        if not isinstance(compare, ast.Compare):
            continue
        expressions = [compare.left, *compare.comparators]
        owner = enclosing_function(compare)
        for index, operation in enumerate(compare.ops):
            if not isinstance(operation, ast.Eq):
                continue
            left, right = expressions[index], expressions[index + 1]
            for set_call, keyset_node in ((left, right), (right, left)):
                if not (isinstance(set_call, ast.Call) and
                        isinstance(set_call.func, ast.Name) and
                        set_call.func.id == "set" and len(set_call.args) == 1 and
                        not set_call.keywords):
                    continue
                if resolve_keyset(keyset_node, owner) == EXACT39_KEYS:
                    count += 1
                    break
    return count


def largest_string_key_dict(function: ast.FunctionDef) -> set[str]:
    candidates: list[set[str]] = []
    for node in ast.walk(function):
        if not isinstance(node, ast.Dict) or any(key is None for key in node.keys):
            continue
        keys: set[str] = set()
        valid = True
        for key in node.keys:
            if not (isinstance(key, ast.Constant) and isinstance(key.value, str)):
                valid = False
                break
            keys.add(key.value)
        if valid:
            candidates.append(keys)
    return max(candidates, key=len, default=set())


def output_shape_values(tree: ast.Module, env: Mapping[str, Any]) -> list[dict[str, int]]:
    expected_names = {
        "selfIdentity", "independentConsumerProof", "staticFreezeProof",
        "coldLaunchProof", "laterRejection", "producerSourceRegistry",
        "liveRequest", "liveACK", "liveACKCensus",
    }
    rows: list[dict[str, int]] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Dict):
            continue
        value = safe_literal(node, env)
        if (isinstance(value, dict) and set(value) == expected_names and
                all(type(item) is int for item in value.values())):
            normalized = dict(value)
            if normalized not in rows:
                rows.append(normalized)
    return rows


def history_census_values(tree: ast.Module) -> dict[str, Any]:
    dictionary_values: list[int] = []
    comparisons: list[dict[str, Any]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Dict):
            for key, value in zip(node.keys, node.values):
                if (isinstance(key, ast.Constant) and
                        key.value == "append_only_history_unique_file_identity_count" and
                        isinstance(value, ast.Constant) and type(value.value) is int):
                    dictionary_values.append(value.value)
        elif isinstance(node, ast.Compare):
            for number in (105, 113, 115):
                argument = is_len_equals(node, number)
                if argument is not None and "history" in ast.unparse(argument).lower():
                    comparisons.append({"line": node.lineno,
                                        "expression": ast.unparse(argument),
                                        "expected": number})
    return {"dictionary_values": dictionary_values,
            "history_len_comparisons": comparisons}


def launcher_exact10_pins(tree: ast.Module, env: Mapping[str, Any]) -> list[tuple[str, str | None]]:
    candidates: list[ast.Tuple] = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.Assign, ast.AnnAssign)):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            if (any(isinstance(target, ast.Name) and target.id == "V12_EXACT10_PINS"
                    for target in targets) and isinstance(node.value, ast.Tuple) and
                    len(node.value.elts) == 10):
                candidates.append(node.value)
    if len(candidates) != 1:
        return []
    rows: list[tuple[str, str | None]] = []
    for row in candidates[0].elts:
        if not isinstance(row, ast.Tuple) or len(row.elts) != 3:
            return []
        file_pin = safe_literal(row.elts[1], env)
        object_pin = safe_literal(row.elts[2], env)
        if not (isinstance(file_pin, str) and HEX64.fullmatch(file_pin)):
            return []
        if object_pin is not None and not (
                isinstance(object_pin, str) and HEX64.fullmatch(object_pin)):
            return []
        rows.append((file_pin, object_pin))
    return rows


def producer_exact10_pins(tree: ast.Module) -> list[tuple[str, str | None]]:
    nodes = module_assignments(tree).get("V12_PUBLISHED_EXACT10_WITNESS", [])
    if len(nodes) != 1 or not isinstance(nodes[0], ast.Tuple) or len(nodes[0].elts) != 10:
        return []
    rows: list[tuple[str, str | None]] = []
    for row in nodes[0].elts:
        if not isinstance(row, ast.Tuple):
            return []
        hashes = [
            item.value for item in ast.walk(row)
            if isinstance(item, ast.Constant) and isinstance(item.value, str) and
            HEX64.fullmatch(item.value)]
        if not hashes:
            return []
        rows.append((hashes[0], hashes[1] if len(hashes) > 1 else None))
    return rows


def consumer_exact10_files(tree: ast.Module, env: Mapping[str, Any]) -> list[str]:
    value = env.get("V12_PUBLISHED_EXACT10_FILE_SHA256_ORDER")
    if not (isinstance(value, tuple) and len(value) == 10 and
            all(isinstance(item, str) and HEX64.fullmatch(item) for item in value)):
        return []
    return list(value)


def path_exists(path: Path) -> bool:
    try:
        os.lstat(path)
    except FileNotFoundError:
        return False
    return True


def target_v14_pyc_paths() -> list[Path]:
    """Return only cache files whose source stem is one of the three targets."""
    if not V14_PYC_DIRECTORY.is_dir():
        return []
    stems = {path.stem for path in V14_PYTHON.values()}
    result: list[Path] = []
    for path in V14_PYC_DIRECTORY.iterdir():
        if not path.name.endswith(".pyc"):
            continue
        if any(path.name == stem + ".pyc" or
               path.name.startswith(stem + ".") for stem in stems):
            result.append(path)
    return sorted(result, key=lambda path: path.name)


def target_v14_pyc_role(path: Path) -> str | None:
    for role, source in V14_PYTHON.items():
        if (path.name == source.stem + ".pyc" or
                path.name.startswith(source.stem + ".")):
            return role
    return None


def decode_pyc_header(raw: bytes) -> dict[str, Any]:
    """Decode the fixed PEP 552 header without loading the code object."""
    if len(raw) < 16:
        return {
            "header_size_required": 16, "observed_file_size": len(raw),
            "header_complete": False,
        }
    flags = int.from_bytes(raw[4:8], "little", signed=False)
    hash_based = bool(flags & 0x01)
    result: dict[str, Any] = {
        "header_size_required": 16,
        "header_complete": True,
        "magic_number_hex": raw[:4].hex(),
        "flags_uint32_le": flags,
        "hash_based": hash_based,
        "checked_hash": bool(flags & 0x02) if hash_based else None,
        "payload_bytes_8_15_hex": raw[8:16].hex(),
    }
    if hash_based:
        result["source_hash_8_hex"] = raw[8:16].hex()
        result["source_timestamp_uint32_le"] = None
        result["source_size_uint32_le"] = None
    else:
        result["source_hash_8_hex"] = None
        result["source_timestamp_uint32_le"] = int.from_bytes(
            raw[8:12], "little", signed=False)
        result["source_size_uint32_le"] = int.from_bytes(
            raw[12:16], "little", signed=False)
    return result


def v14_runtime_surfaces() -> list[Path]:
    explicit_names = [
        f"c79g-v14-candidate-a-{CHECKPOINT}",
        f"c79g-v14-candidate-b-{CHECKPOINT}",
        f"c79g-v14-verification-a-{CHECKPOINT}",
        f"c79g-v14-verification-b-{CHECKPOINT}",
        f"c79g-v14-committed-completion-{CHECKPOINT}",
        f"c79g-v14-rejections-{CHECKPOINT}",
        f".c79g-v14-candidate-stage-a-{CHECKPOINT}",
        f".c79g-v14-candidate-stage-b-{CHECKPOINT}",
        f".c79g-v14-verification-stage-a-{CHECKPOINT}",
        f".c79g-v14-verification-stage-b-{CHECKPOINT}",
        f".c79g-v14-completion-stage-{CHECKPOINT}",
    ]
    result = [RUNTIME / name for name in explicit_names]
    heads = RUNTIME / "cm2-global-authority-heads"
    result.extend([
        heads / f"c79g-v14-{CHECKPOINT}.seal",
        heads / f".c79g-v14-authority-stage-{CHECKPOINT}.seal",
    ])
    if RUNTIME.is_dir():
        result.extend(path for path in RUNTIME.iterdir()
                      if "c79g-v14" in path.name.lower())
    if heads.is_dir():
        result.extend(path for path in heads.iterdir()
                      if "c79g-v14" in path.name.lower())
    return sorted(set(result), key=str)


def incident_helper_review(tree: ast.Module, role: str) -> dict[str, Any]:
    helper_name = "derive_v12_v5_rejection_shape_incident"
    definitions = [
        node for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and
        node.name == helper_name]
    if len(definitions) != 1:
        return {
            "definition_count": len(definitions), "normalized_ast_sha256": None,
            "direct_callsites": [], "non_direct_loads": ["definition_missing"],
            "matches_expected_callsites": False,
        }
    normalized = ast.dump(
        definitions[0], annotate_fields=True,
        include_attributes=False).encode("utf-8")
    parents = parent_map(tree)
    rows: list[tuple[str | None, str | None, int]] = []
    non_direct: list[dict[str, Any]] = []
    for node in ast.walk(tree):
        if not (isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load) and
                node.id == helper_name):
            continue
        parent = parents.get(node)
        if not (isinstance(parent, ast.Call) and parent.func is node and
                len(parent.args) == 5 and not parent.keywords):
            non_direct.append({"line": node.lineno,
                               "parent": type(parent).__name__ if parent else None})
            continue
        chain = owner_chain(parent, parents)
        function = next((name for name in chain if name not in {
            "HeldSelf", "HeldInheritedIncidentAuthorityExact17",
            "HeldV12PredecessorExact10"}), None)
        class_name = next((name for name in chain if name in {
            "HeldSelf", "HeldInheritedIncidentAuthorityExact17",
            "HeldV12PredecessorExact10"}), None)
        rows.append((class_name, function, len(parent.args)))
    expected = EXPECTED_INCIDENT_HELPER_CALLSITES[role]
    return {
        "definition_count": 1,
        "normalized_ast_sha256": sha_bytes(normalized),
        "normalized_ast_size": len(normalized),
        "direct_callsites": [list(row) for row in rows],
        "expected_callsites": [list(row) for row in expected],
        "non_direct_loads": non_direct,
        "matches_expected_callsites": rows == expected and not non_direct,
    }


def v10_helper_callsite_contract_review(
        source_trees: Mapping[str, ast.Module],
        builder_tree: ast.Module | None,
) -> dict[str, Any]:
    """Close the builder/runtime exact-five helper-census contract."""
    expected = [
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
    expected_digest = sha_bytes(canonical(expected))
    stale_exact4 = [expected[index] for index in (0, 1, 3, 4)]
    stale_exact4_digest = sha_bytes(canonical(stale_exact4))

    actual: list[dict[str, Any]] = []
    source_rows: dict[str, Any] = {}
    for role in ("producer", "consumer", "launcher"):
        tree = source_trees.get(role)
        direct_calls: list[tuple[int, str]] = []
        non_direct: list[dict[str, Any]] = []
        if isinstance(tree, ast.Module):
            parents = parent_map(tree)
            for node in ast.walk(tree):
                if not (isinstance(node, ast.Name) and
                        isinstance(node.ctx, ast.Load) and
                        node.id == "derive_v10_colon_prefix_witness"):
                    continue
                call = parents.get(node)
                if not (isinstance(call, ast.Call) and call.func is node and
                        len(call.args) == 2 and not call.keywords):
                    non_direct.append({
                        "line": node.lineno,
                        "parent": type(call).__name__ if call else None})
                    continue
                cursor: ast.AST = call
                owner: str | None = None
                while cursor in parents:
                    cursor = parents[cursor]
                    if isinstance(cursor, ast.Lambda):
                        non_direct.append({
                            "line": node.lineno, "parent": "Lambda"})
                        owner = None
                        break
                    if isinstance(cursor, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        owner = cursor.name
                        break
                if owner is None:
                    non_direct.append({
                        "line": node.lineno, "parent": "NO_FUNCTION_OWNER"})
                    continue
                direct_calls.append((call.lineno, owner))
        ordered_owners: list[str] = []
        for _, owner in sorted(direct_calls):
            if owner not in ordered_owners:
                ordered_owners.append(owner)
        role_rows = [
            {"source_role": role, "enclosing_function": owner,
             "direct_call_count": sum(
                 call_owner == owner for _, call_owner in direct_calls)}
            for owner in ordered_owners]
        actual.extend(role_rows)
        source_rows[role] = {
            "direct_call_count": len(direct_calls),
            "grouped_rows": role_rows,
            "non_direct_loads": non_direct,
            "matches": not non_direct,
        }

    exact_row_keys = {
        "source_role", "enclosing_function", "direct_call_count"}
    validator_owners = {
        "builder": "build_static_audit",
        "producer": "_validate_final_static_audit",
        "consumer": "_validate_final_static_audit",
        "launcher": "validate_final_static_audit",
    }
    validation_trees: dict[str, ast.Module | None] = {
        "builder": builder_tree,
        **{role: source_trees.get(role)
           for role in ("producer", "consumer", "launcher")},
    }
    validator_rows: dict[str, Any] = {}
    for role, tree in validation_trees.items():
        candidates: list[dict[str, Any]] = []
        strings = literal_strings(tree) if isinstance(tree, ast.Module) else set()
        if isinstance(tree, ast.Module):
            parents = parent_map(tree)
            for node in ast.walk(tree):
                if not isinstance(node, ast.List):
                    continue
                try:
                    value = ast.literal_eval(node)
                except (ValueError, TypeError, SyntaxError, MemoryError,
                        RecursionError):
                    continue
                if not (isinstance(value, list) and value and all(
                        isinstance(row, dict) and set(row) == exact_row_keys
                        for row in value)):
                    continue
                cursor: ast.AST = node
                owner: str | None = None
                while cursor in parents:
                    cursor = parents[cursor]
                    if isinstance(cursor, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        owner = cursor.name
                        break
                candidates.append({
                    "line": node.lineno, "owner": owner, "value": value})
        expected_candidates = [
            row for row in candidates
            if row["owner"] == validator_owners[role]]
        validator_rows[role] = {
            "required_owner": validator_owners[role],
            "candidate_count": len(candidates),
            "required_owner_candidate_count": len(expected_candidates),
            "required_owner_candidates": expected_candidates,
            "expected_digest_literal_present": expected_digest in strings,
            "stale_exact4_digest_literal_present": stale_exact4_digest in strings,
            "matches": (
                len(expected_candidates) == 1 and
                expected_candidates[0]["value"] == expected and
                stale_exact4_digest not in strings),
        }

    matches = (
        set(source_rows) == {"producer", "consumer", "launcher"} and
        all(row["matches"] for row in source_rows.values()) and
        actual == expected and expected_digest ==
            "1ca6de98366645a520cbc604990d71197f039207cacfa3291e9d87ff09a3cf57" and
        stale_exact4_digest ==
            "69979c91172f95d179e5af986d4f8d2d5406ffcfdc14abaef1f1578766c1963d" and
        set(validator_rows) == set(validator_owners) and
        all(row["matches"] for row in validator_rows.values()))
    return {
        "expected_exact5": expected,
        "actual_exact5": actual,
        "expected_exact5_sha256": expected_digest,
        "stale_exact4_sha256": stale_exact4_digest,
        "source_census": source_rows,
        "builder_and_runtime_validator_literals": validator_rows,
        "matches": matches,
    }


def incident_fd_environment_review(
        tree: ast.Module, env: Mapping[str, Any], role: str,
) -> dict[str, Any]:
    coordination_name = (
        "COLD_COORDINATION_PARENT_FD_ENV" if role == "producer"
        else "COORDINATION_PARENT_FD_ENV")
    control_names = (
        "COLD_EXEC_FD_ENV", "COLD_SOURCE_FD_ENV",
        "COLD_WORKSPACE_ROOT_FD_ENV", coordination_name,
    )
    expected_names = set(control_names) | set(INCIDENT_FD_ENV_NAMES)
    expected_values = {
        name: "CM2_C79G_V14_" + name.removesuffix("_ENV")
        for name in expected_names}
    expected_values[coordination_name] = "CM2_C79G_V14_COORDINATION_PARENT_FD"
    assignments = {
        name: value for name, value in env.items()
        if name.endswith("_FD_ENV") and isinstance(value, str) and
        value.startswith("CM2_C79G_V14_")}
    load_counts = {
        name: sum(
            isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load) and
            node.id == name for node in ast.walk(tree))
        for name in INCIDENT_FD_ENV_NAMES}
    return {
        "expected_total_fd_env_count": 21,
        "observed_total_fd_env_count": len(assignments),
        "expected_incident_fd_env_count": 17,
        "observed_incident_fd_env_count": sum(
            name in assignments for name in INCIDENT_FD_ENV_NAMES),
        "missing_names": sorted(expected_names - set(assignments)),
        "extra_names": sorted(set(assignments) - expected_names),
        "value_mismatches": {
            name: {"observed": assignments.get(name), "expected": expected}
            for name, expected in expected_values.items()
            if assignments.get(name) != expected},
        "unique_observed_value_count": len(set(assignments.values())),
        "incident_role_load_counts": load_counts,
        "matches": (
            set(assignments) == expected_names and
            assignments == expected_values and len(set(assignments.values())) == 21 and
            all(count >= 1 for count in load_counts.values())),
    }


def draft_final_main_gate_review(
        tree: ast.Module, final_flag_name: str) -> dict[str, Any]:
    mains = [
        node for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and
        node.name == "main"]
    rows: list[dict[str, Any]] = []
    expected_prefix_sources = {
        "FINAL_V14_CORE_PINS_INSTALLED": (
            "args = parser().parse_args(argv)",
        ),
        "FINAL_CURRENT_V14_PINS_INSTALLED": (
            "cli = argparse.ArgumentParser(description=__doc__)",
            "sub = cli.add_subparsers(dest='command', required=True)",
            "verify_cli = sub.add_parser('verify')",
            "verify_cli.add_argument('--orientation', required=True, "
            "choices=('a', 'b'))",
            "sub.add_parser('assemble')",
            "sub.add_parser('authorize')",
            "sub.add_parser('reject', help='non-normative fallback; cold "
            "launcher owns normative reject')",
            "args = cli.parse_args(argv)",
        ),
        "FINAL_BASE7_PINS_INSTALLED": (
            "args = parser().parse_args(argv)",
        ),
    }
    expected_prefix = expected_prefix_sources.get(final_flag_name, ())
    expected_prefix_dumps = [
        ast.dump(ast.parse(source, mode="exec").body[0],
                 annotate_fields=True, include_attributes=False)
        for source in expected_prefix]

    def exact_draft_branch(node: ast.If) -> dict[str, Any]:
        statement = node.body[0] if len(node.body) == 1 else None
        exception = statement.exc if isinstance(statement, ast.Raise) else None
        exact_reject_call = (
            isinstance(exception, ast.Call) and
            isinstance(exception.func, ast.Name) and
            exception.func.id == "Reject" and len(exception.args) == 1 and
            isinstance(exception.args[0], ast.Constant) and
            exception.args[0].value ==
                "C79g v14 successor is a sentinel draft; runtime is disabled" and
            not exception.keywords)
        matches = (
            len(node.body) == 1 and isinstance(statement, ast.Raise) and
            statement.cause is None and exact_reject_call and not node.orelse)
        return {
            "statement_count": len(node.body),
            "orelse_statement_count": len(node.orelse),
            "body": [ast.unparse(item) for item in node.body],
            "exact_single_Reject_raise": exact_reject_call,
            "matches": matches,
        }

    if len(mains) == 1:
        main = mains[0]
        for statement_index, node in enumerate(main.body):
            if not (isinstance(node, ast.If) and any(
                    isinstance(item, ast.Name) and
                    item.id == "V14_DRAFT_RUNTIME_DISABLED"
                    for item in ast.walk(node.test))):
                continue
            exact_and = (
                isinstance(node.test, ast.BoolOp) and
                isinstance(node.test.op, ast.And) and
                len(node.test.values) == 2 and
                isinstance(node.test.values[0], ast.Name) and
                node.test.values[0].id == "V14_DRAFT_RUNTIME_DISABLED" and
                isinstance(node.test.values[1], ast.UnaryOp) and
                isinstance(node.test.values[1].op, ast.Not) and
                isinstance(node.test.values[1].operand, ast.Name) and
                node.test.values[1].operand.id == final_flag_name)
            observed_prefix = main.body[:statement_index]
            observed_prefix_dumps = [
                ast.dump(statement, annotate_fields=True,
                         include_attributes=False)
                for statement in observed_prefix]
            prefix_exact = observed_prefix_dumps == expected_prefix_dumps
            branch = exact_draft_branch(node)
            rows.append({
                "line": node.lineno,
                "direct_main_statement_index": statement_index,
                "test": ast.unparse(node.test),
                "exact_draft_and_not_final_gate": exact_and,
                "expected_pre_gate_statements": list(expected_prefix),
                "observed_pre_gate_statements": [
                    ast.unparse(statement) for statement in observed_prefix],
                "pre_gate_CLI_setup_and_argv_parse_AST_exact": prefix_exact,
                "draft_branch_exact_body": branch,
                "gate_precedes_first_protocol_input_read_or_side_effect":
                    prefix_exact,
            })
    return {
        "main_definition_count": len(mains),
        "draft_gate_rows": rows,
        "matches": len(mains) == 1 and len(rows) == 1 and
                   rows[0]["exact_draft_and_not_final_gate"] and
                   rows[0]["pre_gate_CLI_setup_and_argv_parse_AST_exact"] and
                   rows[0]["draft_branch_exact_body"]["matches"] and
                   rows[0][
                       "gate_precedes_first_protocol_input_read_or_side_effect"],
    }


def launcher_receipt_first_review(
        tree: ast.Module, env: Mapping[str, Any],
) -> dict[str, Any]:
    configure = [
        node for node in tree.body
        if isinstance(node, ast.FunctionDef) and
        node.name == "configure_workspace_paths"]
    base7_order: list[str | None] = []
    exact8_order: list[str | None] = []
    if len(configure) == 1:
        for node in configure[0].body:
            if (isinstance(node, ast.Assign) and len(node.targets) == 1 and
                    isinstance(node.targets[0], ast.Name)):
                if node.targets[0].id == "BASE7_PINS" and isinstance(node.value, ast.Dict):
                    base7_order = [
                        key.id if isinstance(key, ast.Name) else None
                        for key in node.value.keys]
                if node.targets[0].id == "EXACT8" and isinstance(node.value, ast.Tuple):
                    exact8_order = [
                        item.id if isinstance(item, ast.Name) else None
                        for item in node.value.elts]

    normalizers = [
        node for node in tree.body
        if isinstance(node, ast.FunctionDef) and
        node.name == "pin_normalized_launcher_ast_sha256"]
    normalizer_receipt_names = normalizer_v12_names = -1
    normalizer_receipt_strings: list[str] = []
    if len(normalizers) == 1:
        normalizer_receipt_names = sum(
            isinstance(node, ast.Name) and node.id == "V13_SUPERSESSION_RECEIPT"
            for node in ast.walk(normalizers[0]))
        normalizer_v12_names = sum(
            isinstance(node, ast.Name) and node.id == "V12_OFFICIAL_REJECTION"
            for node in ast.walk(normalizers[0]))
        normalizer_receipt_strings = [
            node.value for node in ast.walk(normalizers[0])
            if isinstance(node, ast.Constant) and isinstance(node.value, str) and
            "supersession" in node.value.lower()]

    base_object_orders: list[list[str | None]] = []
    classes = [
        node for node in tree.body
        if isinstance(node, ast.ClassDef) and node.name == "HeldBundle"]
    if len(classes) == 1:
        initializers = [
            node for node in classes[0].body
            if isinstance(node, ast.FunctionDef) and node.name == "_initialize"]
        if len(initializers) == 1:
            for node in ast.walk(initializers[0]):
                if (isinstance(node, ast.For) and isinstance(node.target, ast.Name) and
                        node.target.id == "path" and isinstance(node.iter, ast.Tuple)):
                    names = [
                        item.id if isinstance(item, ast.Name) else None
                        for item in node.iter.elts]
                    if {"CONTRACT", "TRANSITION", "AUDIT"}.issubset(set(names)):
                        base_object_orders.append(names)

    expected_base7 = [
        "V13_SUPERSESSION_RECEIPT", "SCHEMA", "CONTRACT", "PRODUCER",
        "CONSUMER", "TRANSITION", "AUDIT"]
    expected_exact8 = [*expected_base7, "SELF"]
    expected_base_objects = [
        "V13_SUPERSESSION_RECEIPT", "CONTRACT", "TRANSITION", "AUDIT"]
    algorithm = env.get("PIN_NORMALIZED_AST_ALGORITHM")
    matches = (
        base7_order == expected_base7 and exact8_order == expected_exact8 and
        len(normalizers) == 1 and
        "V13_SUPERSESSION_RECEIPT" in normalizer_receipt_strings and
        normalizer_v12_names == 0 and normalizer_receipt_strings and
        isinstance(algorithm, str) and
        "PRESERVE_V13_SUPERSESSION_RECEIPT" in algorithm and
        base_object_orders == [expected_base_objects])
    return {
        "configured_base7_key_order": base7_order,
        "configured_exact8_order": exact8_order,
        "pin_normalizer_definition_count": len(normalizers),
        "pin_normalizer_v12_symbol_count": normalizer_v12_names,
        "pin_normalizer_receipt_symbol_count": normalizer_receipt_names,
        "pin_normalizer_receipt_strings": normalizer_receipt_strings,
        "pin_normalized_ast_algorithm": algorithm,
        "base_objects_loop_orders": base_object_orders,
        "expected_base_objects_loop_order": expected_base_objects,
        "matches": matches,
    }


def independent_pin_normalized_launcher_ast_review(raw: bytes) -> dict[str, Any]:
    """Reproduce the launcher's cycle-breaking AST digest without execution."""
    current_keys = ("SCHEMA", "CONTRACT", "PRODUCER", "CONSUMER",
                    "TRANSITION", "AUDIT")
    object_keys = {"CONTRACT", "TRANSITION", "AUDIT"}
    try:
        tree = ast.parse(raw.decode("utf-8"), filename="v14_launcher_pin_graph",
                         mode="exec")
        compile(tree, "v14_launcher_pin_graph", "exec", dont_inherit=True)
        assignments: list[ast.Assign | ast.AnnAssign] = []
        for node in tree.body:
            if (isinstance(node, ast.Assign) and len(node.targets) == 1 and
                    isinstance(node.targets[0], ast.Name) and
                    node.targets[0].id == "FINAL_BASE7_PINS_INSTALLED"):
                assignments.append(node)
            elif (isinstance(node, ast.AnnAssign) and
                  isinstance(node.target, ast.Name) and
                  node.target.id == "FINAL_BASE7_PINS_INSTALLED"):
                assignments.append(node)
        if len(assignments) != 1:
            raise ValueError("not exactly one final launcher pin assignment")
        assignments[0].value = ast.Constant(value=False)

        configure = [
            node for node in tree.body
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and
            node.name == "configure_workspace_paths"]
        if len(configure) != 1:
            raise ValueError("not exactly one configure_workspace_paths")
        base7_assignments = [
            node for node in configure[0].body
            if isinstance(node, ast.Assign) and len(node.targets) == 1 and
            isinstance(node.targets[0], ast.Name) and
            node.targets[0].id == "BASE7_PINS"]
        if (len(base7_assignments) != 1 or
                not isinstance(base7_assignments[0].value, ast.Dict)):
            raise ValueError("not exactly one direct BASE7_PINS dictionary")
        base7 = base7_assignments[0].value
        key_order = [
            key.id if isinstance(key, ast.Name) else None for key in base7.keys]
        expected_order = ["V13_SUPERSESSION_RECEIPT", *current_keys]
        if key_order != expected_order or len(base7.values) != 7:
            raise ValueError("BASE7 key order is not receipt plus current exact6")
        receipt_before = ast.dump(
            base7.values[0], annotate_fields=True, include_attributes=False)
        for index, key in enumerate(key_order[1:], start=1):
            base7.values[index] = ast.Tuple(
                elts=[
                    ast.Constant(value="f" * 64),
                    ast.Constant(value="e" * 64 if key in object_keys else None),
                ],
                ctx=ast.Load())
        receipt_after = ast.dump(
            base7.values[0], annotate_fields=True, include_attributes=False)
        if receipt_before != receipt_after:
            raise ValueError("receipt pin changed during normalization")
        digest = sha_bytes(ast.dump(
            tree, annotate_fields=True,
            include_attributes=False).encode("utf-8"))
        return {
            "algorithm": (
                "PYTHON_AST_DUMP_NO_ATTRIBUTES__FORCE_FINAL_BASE7_FALSE__"
                "CURRENT_V14_SIX_BASE7_FILE_F64_OBJECT_E64_OR_NONE__"
                "PRESERVE_V13_SUPERSESSION_RECEIPT_AND_ALL_HISTORICAL_PINS_V1"),
            "configured_key_order": key_order,
            "receipt_value_preserved": True,
            "sha256": digest,
            "matches": bool(HEX64.fullmatch(digest)),
        }
    except Exception as exc:
        return {
            "matches": False,
            "error": f"{type(exc).__name__}: {exc}",
        }


def launcher_active_base7_review(
        tree: ast.Module, env: Mapping[str, Any],
) -> dict[str, Any]:
    configure = [
        node for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and
        node.name == "configure_workspace_paths"]
    key_order: list[str | None] = []
    values: dict[str, Any] = {}
    exact8_order: list[str | None] = []
    if len(configure) == 1:
        for node in configure[0].body:
            if not (isinstance(node, ast.Assign) and len(node.targets) == 1 and
                    isinstance(node.targets[0], ast.Name)):
                continue
            if (node.targets[0].id == "BASE7_PINS" and
                    isinstance(node.value, ast.Dict)):
                key_order = [
                    key.id if isinstance(key, ast.Name) else None
                    for key in node.value.keys]
                for key, value_node in zip(key_order, node.value.values):
                    if key is None:
                        continue
                    value = safe_literal(value_node, env)
                    values[key] = (
                        value if value is not MISSING else "UNRESOLVED_STATIC_VALUE")
            elif (node.targets[0].id == "EXACT8" and
                  isinstance(node.value, ast.Tuple)):
                exact8_order = [
                    item.id if isinstance(item, ast.Name) else None
                    for item in node.value.elts]
    return {
        "configure_workspace_paths_definition_count": len(configure),
        "base7_key_order": key_order,
        "base7_pin_values": values,
        "exact8_order": exact8_order,
    }


def launcher_configured_path_graph_review(tree: ast.Module) -> dict[str, Any]:
    """Close the exact root-relative current-v14 path construction AST."""
    expected_expressions = {
        "ROOT": "root",
        "OUT": "ROOT / 'deliverables'",
        "SELF": "ROOT / LAUNCHER_RELATIVE",
        "SCHEMA": "OUT / (BASE + '_schema_v14.json')",
        "CONTRACT": "OUT / (BASE + '_contract_v14.json')",
        "PRODUCER": "OUT / (BASE + '_v14.py')",
        "CONSUMER": (
            "OUT / (BASE + "
            "'_independent_verifier_assembler_authority_consumer_v14.py')"),
        "TRANSITION": (
            "OUT / (BASE + "
            "'_v13_to_v14_static_launch_transition_receipt_v1.json')"),
        "AUDIT": "OUT / (BASE + '_static_audit_v14.json')",
        "MANIFEST": "OUT / (BASE + '_cold_launch_manifest_v14.sha256')",
        "OUTER": "OUT / (BASE + '_cold_launch_outer_receipt_v14.json')",
    }

    def expression_dump(source: str) -> str:
        expression = ast.parse(source, mode="eval").body
        return ast.dump(expression, annotate_fields=True,
                        include_attributes=False)

    expected_dumps = {
        name: expression_dump(expression)
        for name, expression in expected_expressions.items()}
    configure = [
        node for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and
        node.name == "configure_workspace_paths"]
    assignments: dict[str, list[ast.AST]] = {
        name: [] for name in expected_expressions}
    observed_assignment_order: list[str] = []
    declared_globals: set[str] = set()
    if len(configure) == 1:
        for node in configure[0].body:
            if isinstance(node, ast.Global):
                declared_globals.update(node.names)
            if (isinstance(node, ast.Assign) and len(node.targets) == 1 and
                    isinstance(node.targets[0], ast.Name) and
                    node.targets[0].id in assignments):
                assignments[node.targets[0].id].append(node.value)
                observed_assignment_order.append(node.targets[0].id)
    rows = {
        name: {
            "expected_expression": expected_expressions[name],
            "observed_expressions": [ast.unparse(node) for node in nodes],
            "assignment_count": len(nodes),
            "declared_global": name in declared_globals,
            "matches": (
                len(nodes) == 1 and
                ast.dump(nodes[0], annotate_fields=True,
                         include_attributes=False) == expected_dumps[name] and
                name in declared_globals),
        }
        for name, nodes in assignments.items()}
    return {
        "configure_workspace_paths_definition_count": len(configure),
        "required_path_assignment_order": list(expected_expressions),
        "observed_path_assignment_order": observed_assignment_order,
        "paths": rows,
        "matches": (
            len(configure) == 1 and
            observed_assignment_order == list(expected_expressions) and
            all(row["matches"] for row in rows.values())),
    }


def sentinel_declaration_review(
        source_envs: Mapping[str, Mapping[str, Any]],
        source_trees: Mapping[str, ast.Module] | None = None,
) -> dict[str, Any]:
    expected = {
        "producer": {
            "declaration_name": "V14_DRAFT_CORE_PIN_SENTINELS",
            "values": ("d0" * 32, "e0" * 32, "f0" * 32),
            "active_names": (
                "CONTRACT_FILE_PIN", "CONTRACT_OBJECT_PIN",
                "CLOSED_SCHEMA_FILE_PIN"),
        },
        "consumer": {
            "declaration_name": "V14_DRAFT_CURRENT_CORE_PINS",
            "values": (
                "d9" * 32, "e9" * 32, "f9" * 32, "a9" * 32),
            "active_names": (
                "CONTRACT_FILE_PIN", "CONTRACT_OBJECT_PIN",
                "CLOSED_SCHEMA_FILE_PIN", "PRODUCER_SOURCE_PIN"),
        },
    }
    rows: dict[str, Any] = {}
    for role, specification in expected.items():
        env = source_envs.get(role, {})
        declaration = env.get(specification["declaration_name"])
        active = tuple(env.get(name) for name in specification["active_names"])
        tree = source_trees.get(role) if source_trees is not None else None
        assignments = module_assignments(tree).get(
            specification["declaration_name"], []) \
            if isinstance(tree, ast.Module) else []
        assignment_values = [safe_literal(node, env) for node in assignments]
        assignment_matches = (
            len(assignments) == 1 and
            assignment_values == [specification["values"]]) \
            if source_trees is not None else True
        rows[role] = {
            "declaration_name": specification["declaration_name"],
            "declared_type": type(declaration).__name__,
            "declared_count": len(declaration)
                if isinstance(declaration, tuple) else None,
            "declared_values": declaration,
            "expected_values": specification["values"],
            "active_pin_names": specification["active_names"],
            "active_pin_values": active,
            "module_assignment_count": len(assignments)
                if source_trees is not None else None,
            "module_assignment_values": assignment_values
                if source_trees is not None else None,
            "module_assignment_matches": assignment_matches,
            "declaration_matches": (
                type(declaration) is tuple and
                declaration == specification["values"]),
            "active_matches_declared": active == specification["values"],
        }
        rows[role]["matches"] = (
            rows[role]["declaration_matches"] and assignment_matches)
    launcher = source_envs.get("launcher", {})
    launcher_values = (
        launcher.get("_DRAFT_FILE_PIN"), launcher.get("_DRAFT_OBJECT_PIN"))
    launcher_tree = source_trees.get("launcher") \
        if source_trees is not None else None
    launcher_assignments = module_assignments(launcher_tree) \
        if isinstance(launcher_tree, ast.Module) else {}
    launcher_assignment_values = {
        name: [safe_literal(node, launcher) for node in launcher_assignments.get(name, [])]
        for name in ("_DRAFT_FILE_PIN", "_DRAFT_OBJECT_PIN")}
    launcher_assignment_matches = (
        launcher_assignment_values == {
            "_DRAFT_FILE_PIN": ["f" * 64],
            "_DRAFT_OBJECT_PIN": ["e" * 64],
        }) if source_trees is not None else True
    rows["launcher"] = {
        "declaration_names": ("_DRAFT_FILE_PIN", "_DRAFT_OBJECT_PIN"),
        "declared_type_names": tuple(type(value).__name__
                                     for value in launcher_values),
        "declared_count": len(launcher_values),
        "declared_values": launcher_values,
        "expected_values": ("f" * 64, "e" * 64),
        "module_assignment_values": launcher_assignment_values
            if source_trees is not None else None,
        "module_assignment_matches": launcher_assignment_matches,
        "matches": (
            all(type(value) is str for value in launcher_values) and
            launcher_values == ("f" * 64, "e" * 64) and
            launcher_assignment_matches),
    }
    return {
        "roles": rows,
        "matches": set(rows) == {"producer", "consumer", "launcher"} and
                   all(row["matches"] for row in rows.values()),
    }


def draft_active_pin_graph_review(
        source_trees: Mapping[str, ast.Module],
        source_envs: Mapping[str, Mapping[str, Any]],
        receipt_review: Mapping[str, Any],
) -> dict[str, Any]:
    """Close the active (not merely declared) safe-draft current pin graph."""
    expected_source_pins = {
        "producer": {
            "CONTRACT_FILE_PIN": "d0" * 32,
            "CONTRACT_OBJECT_PIN": "e0" * 32,
            "CLOSED_SCHEMA_FILE_PIN": "f0" * 32,
        },
        "consumer": {
            "CONTRACT_FILE_PIN": "d9" * 32,
            "CONTRACT_OBJECT_PIN": "e9" * 32,
            "CLOSED_SCHEMA_FILE_PIN": "f9" * 32,
            "PRODUCER_SOURCE_PIN": "a9" * 32,
        },
    }
    source_rows: dict[str, Any] = {}
    for role, expected in expected_source_pins.items():
        env = source_envs.get(role, {})
        observed = {name: env.get(name) for name in expected}
        source_rows[role] = {
            "expected": expected,
            "observed": observed,
            "matches": observed == expected and
                       all(type(value) is str for value in observed.values()),
        }

    launcher_tree = source_trees.get("launcher")
    launcher_env = source_envs.get("launcher", {})
    launcher_active = (
        launcher_active_base7_review(launcher_tree, launcher_env)
        if isinstance(launcher_tree, ast.Module) else {
            "base7_key_order": [], "base7_pin_values": {},
            "exact8_order": []})
    receipt_closure = receipt_review.get("object_closure", {})
    receipt_object = (
        receipt_closure.get("declared")
        if isinstance(receipt_closure, Mapping) else None)
    draft_file = launcher_env.get("_DRAFT_FILE_PIN")
    draft_object = launcher_env.get("_DRAFT_OBJECT_PIN")
    expected_launcher = {
        "V13_SUPERSESSION_RECEIPT": (
            receipt_review.get("file_sha256"), receipt_object),
        "SCHEMA": (draft_file, None),
        "CONTRACT": (draft_file, draft_object),
        "PRODUCER": (draft_file, None),
        "CONSUMER": (draft_file, None),
        "TRANSITION": (draft_file, draft_object),
        "AUDIT": (draft_file, draft_object),
    }
    launcher_matches = (
        receipt_review.get("matches") is True and
        draft_file == "f" * 64 and draft_object == "e" * 64 and
        launcher_active.get("base7_key_order") == list(expected_launcher) and
        launcher_active.get("base7_pin_values") == expected_launcher and
        launcher_active.get("exact8_order") == [*expected_launcher, "SELF"])
    return {
        "producer_consumer_active_pins": source_rows,
        "launcher_active_base7": launcher_active,
        "launcher_expected_draft_base7": expected_launcher,
        "launcher_matches": launcher_matches,
        "matches": (
            set(source_rows) == set(expected_source_pins) and
            all(row["matches"] for row in source_rows.values()) and
            launcher_matches),
    }


def external_frozen_audit_input_evidence_review(
        frozen_exact10: Mapping[str, tuple[bytes, tuple[int, ...]]],
        v5_raw: bytes, v5_value: Any, v5_duplicates: Sequence[str],
        v5_closure: Mapping[str, Any],
        v12_rejection_raw: bytes, v12_rejection: Any,
        v12_rejection_duplicates: Sequence[str],
        v12_rejection_closure: Mapping[str, Any],
        incident_value: Any, incident_digest: Any,
) -> dict[str, Any]:
    """Derive inherited exact43 values from immutable predecessor evidence."""
    exact10_indexes = {
        "producer": 3, "consumer": 4, "audit": 6, "launcher": 7}
    frozen_rows: dict[str, Any] = {}
    frozen_ok = set(frozen_exact10) == set(exact10_indexes)
    for role, index in exact10_indexes.items():
        raw_and_identity = frozen_exact10.get(role)
        if raw_and_identity is None:
            frozen_rows[role] = {"matches": False, "error": "missing"}
            frozen_ok = False
            continue
        raw, identity = raw_and_identity
        expected_file = V12_EXACT10[index][1]
        metadata_ok = (
            len(identity) >= 4 and stat.S_IMODE(identity[2]) == 0o444 and
            identity[3] == 1)
        row_ok = sha_bytes(raw) == expected_file and metadata_ok
        frozen_rows[role] = {
            "observed_file_sha256": sha_bytes(raw),
            "expected_file_sha256": expected_file,
            "mode": oct(stat.S_IMODE(identity[2])) if len(identity) >= 3 else None,
            "nlink": identity[3] if len(identity) >= 4 else None,
            "matches": row_ok,
        }
        frozen_ok &= row_ok

    frozen_audit_value: Any = None
    frozen_audit_duplicates: list[str] = []
    frozen_audit_closure: dict[str, Any] = {"matches": False}
    frozen_checker_inputs: dict[str, Any] = {}
    try:
        frozen_audit_raw = frozen_exact10["audit"][0]
        frozen_audit_value, frozen_audit_duplicates = decode_json(
            frozen_audit_raw, "frozen_v12_static_audit")
        frozen_audit_closure = object_closure(frozen_audit_value)
        dual = frozen_audit_value.get("dual_independent_static_checkers", {})
        if isinstance(dual, dict):
            for name in ("checker_A", "checker_B"):
                checker = dual.get(name, {})
                if isinstance(checker, dict) and isinstance(
                        checker.get("input_sha256"), dict):
                    frozen_checker_inputs[name] = checker["input_sha256"]
    except Exception as exc:
        frozen_audit_closure = {
            "matches": False, "error": f"{type(exc).__name__}: {exc}"}

    inherited_order = EXPECTED_STATIC_AUDIT_V14_INPUT_ORDER[:37]
    checker_a_inputs = frozen_checker_inputs.get("checker_A")
    checker_b_inputs = frozen_checker_inputs.get("checker_B")
    inherited_inputs_match = (
        frozen_ok and isinstance(frozen_audit_value, dict) and
        not frozen_audit_duplicates and
        frozen_audit_closure.get("matches") is True and
        frozen_audit_closure.get("declared") == V12_EXACT10[6][2] and
        isinstance(checker_a_inputs, dict) and
        isinstance(checker_b_inputs, dict) and
        tuple(checker_a_inputs) == inherited_order and
        tuple(checker_b_inputs) == inherited_order and
        checker_a_inputs == checker_b_inputs and
        all(type(value) is str and HEX64.fullmatch(value) and value != "0" * 64
            for value in checker_a_inputs.values()))

    historical_tail = {
        key: checker_a_inputs.get(key) if isinstance(checker_a_inputs, dict)
        else None
        for key in EXPECTED_STATIC_AUDIT_V14_INPUT_ORDER[8:37]}

    v5_external_matches = (
        isinstance(v5_value, dict) and not v5_duplicates and
        sha_bytes(v5_raw) == EXPECTED_V5_REJECTION_FILE_SHA256 and
        v5_closure.get("matches") is True and
        v5_closure.get("declared") == EXPECTED_V5_REJECTION_OBJECT_SHA256 and
        set(v5_value) == EXACT39_KEYS)
    rejection_external_matches = (
        isinstance(v12_rejection, dict) and not v12_rejection_duplicates and
        sha_bytes(v12_rejection_raw) == EXPECTED_V12_REJECTION_FILE_SHA256 and
        v12_rejection_closure.get("matches") is True and
        v12_rejection_closure.get("declared") ==
            EXPECTED_V12_REJECTION_OBJECT_SHA256 and
        set(v12_rejection) == V12_REJECTION_KEYS)

    frozen_ast_rows: dict[str, Any] = {}
    frozen_ast_ok = True
    frozen_trees: dict[str, ast.Module] = {}
    for role in ("producer", "consumer", "launcher"):
        try:
            raw = frozen_exact10[role][0]
            tree = ast.parse(raw.decode("utf-8"),
                             filename=f"frozen_v12_{role}", mode="exec")
            compile(tree, f"frozen_v12_{role}", "exec", dont_inherit=True)
            frozen_trees[role] = tree
            frozen_ast_rows[role] = {"AST_and_compile_in_memory": True}
        except Exception as exc:
            frozen_ast_ok = False
            frozen_ast_rows[role] = {
                "AST_and_compile_in_memory": False,
                "error": f"{type(exc).__name__}: {exc}"}
    producer_exact39_gate_count = frozen_literal_exact39_gate_count(
        frozen_trees["producer"]) if "producer" in frozen_trees else 0
    consumer_exact39_gate_count = frozen_literal_exact39_gate_count(
        frozen_trees["consumer"]) if "consumer" in frozen_trees else 0
    launcher_len52_rows = stale_v5_len52_rows(
        frozen_trees["launcher"], "launcher")[1] \
        if "launcher" in frozen_trees else []
    frozen_failure_shape_matches = (
        frozen_ast_ok and
        producer_exact39_gate_count >= 1 and
        consumer_exact39_gate_count >= 1 and
        bool(launcher_len52_rows))
    incident_matches = (
        isinstance(incident_value, dict) and
        v12_incident_semantics(incident_value) and
        type(incident_digest) is str and HEX64.fullmatch(incident_digest) and
        sha_bytes(canonical(incident_value)) == incident_digest and
        frozen_failure_shape_matches and v5_external_matches and
        rejection_external_matches)

    suffix = {
        "v12_rejection_file": sha_bytes(v12_rejection_raw),
        "v12_rejection_object": v12_rejection_closure.get("declared"),
        "v12_producer_file": sha_bytes(frozen_exact10["producer"][0])
            if "producer" in frozen_exact10 else None,
        "v12_consumer_file": sha_bytes(frozen_exact10["consumer"][0])
            if "consumer" in frozen_exact10 else None,
        "v12_launcher_file": sha_bytes(frozen_exact10["launcher"][0])
            if "launcher" in frozen_exact10 else None,
        "trusted_v12_v5_rejection_shape_incident_digest": incident_digest,
    }
    expected_tail = {**historical_tail, **suffix}
    expected_tail_order = EXPECTED_STATIC_AUDIT_V14_INPUT_ORDER[8:]
    expected_tail_values_valid = (
        tuple(expected_tail) == expected_tail_order and
        all(type(value) is str and HEX64.fullmatch(value) and value != "0" * 64
            for value in expected_tail.values()))
    matches = (
        inherited_inputs_match and incident_matches and
        tuple(suffix) == STATIC_AUDIT_V12_INPUT_SUFFIX and
        expected_tail_values_valid)
    return {
        "frozen_exact10_files": frozen_rows,
        "frozen_v12_audit": {
            "file_sha256": sha_bytes(frozen_exact10["audit"][0])
                if "audit" in frozen_exact10 else None,
            "duplicate_keys": frozen_audit_duplicates,
            "object_closure": frozen_audit_closure,
            "checker_A_B_exact37_equal": inherited_inputs_match,
            "input_order": list(inherited_order),
        },
        "v5_external_matches": v5_external_matches,
        "v12_rejection_external_matches": rejection_external_matches,
        "frozen_v12_failure_shape": {
            "AST_rows": frozen_ast_rows,
            "producer_literal_exact39_gate_count":
                producer_exact39_gate_count,
            "consumer_literal_exact39_gate_count":
                consumer_exact39_gate_count,
            "launcher_v5_len52_rows": launcher_len52_rows,
            "matches": frozen_failure_shape_matches,
        },
        "incident_digest": incident_digest,
        "incident_matches_frozen_failure_evidence": incident_matches,
        "expected_tail_order": list(expected_tail_order),
        "expected_tail": expected_tail,
        "expected_tail_values_are_nonzero_hex64": expected_tail_values_valid,
        "matches": matches,
    }


def exact43_audit_input_review(
        dual: Mapping[str, Any], expected_inputs: Mapping[str, Any],
) -> dict[str, Any]:
    checker_names = ("checker_A", "checker_B")
    rows: dict[str, Any] = {}
    expected_order = EXPECTED_STATIC_AUDIT_V14_INPUT_ORDER
    expected_digest = sha_bytes(canonical(list(expected_order)))
    expected_mapping = dict(expected_inputs)
    expected_values_are_nonzero_hex64 = (
        tuple(expected_mapping) == expected_order and
        all(type(value) is str and HEX64.fullmatch(value) and value != "0" * 64
            for value in expected_mapping.values()))
    for name in checker_names:
        checker = dual.get(name)
        checker = checker if isinstance(checker, dict) else {}
        inputs = checker.get("input_sha256")
        observed_order = tuple(inputs) if isinstance(inputs, dict) else None
        rows[name] = {
            "observed_count": len(inputs) if isinstance(inputs, dict) else None,
            "observed_order": list(observed_order)
                if observed_order is not None else None,
            "observed_order_sha256": sha_bytes(canonical(list(observed_order)))
                if observed_order is not None else None,
            "missing_keys": sorted(set(expected_mapping) - set(inputs))
                if isinstance(inputs, dict) else sorted(expected_mapping),
            "extra_keys": sorted(set(inputs) - set(expected_mapping))
                if isinstance(inputs, dict) else [],
            "value_mismatch_keys": [
                key for key in expected_order
                if not isinstance(inputs, dict) or
                inputs.get(key) != expected_mapping.get(key)],
            "matches": (
                isinstance(inputs, dict) and
                observed_order == expected_order and
                inputs == expected_mapping and
                expected_digest ==
                    "7e11baf937aa7e9695f30718fcb14793ed2fdacbdf0f33bda659086d399e4574"),
        }
    return {
        "expected_count": len(expected_order),
        "expected_order": list(expected_order),
        "expected_order_sha256": expected_digest,
        "expected_values": expected_mapping,
        "expected_values_are_nonzero_hex64": expected_values_are_nonzero_hex64,
        "checkers": rows,
        "matches": (
            tuple(expected_mapping) == expected_order and
            expected_values_are_nonzero_hex64 and
            len(rows) == 2 and all(row["matches"] for row in rows.values())),
    }


def static_audit_validator_exact43_review(
        source_trees: Mapping[str, ast.Module],
        source_envs: Mapping[str, Mapping[str, Any]],
) -> dict[str, Any]:
    """Prove each runtime validator enforces the full ordered A/B exact43."""
    specifications = {
        "producer": (
            "_validate_final_static_audit", "STATIC_AUDIT_INPUT_KEY_ORDER",
            "STATIC_AUDIT_INPUT_KEY_ORDER_SHA256"),
        "consumer": (
            "_validate_final_static_audit", "STATIC_AUDIT_INPUT_EXACT43",
            "STATIC_AUDIT_INPUT_EXACT43_ORDER_SHA256"),
        "launcher": (
            "validate_final_static_audit",
            "FINAL_STATIC_AUDIT_INPUT_KEY_ORDER",
            "FINAL_STATIC_AUDIT_INPUT_KEY_ORDER_SHA256"),
    }
    expected_digest = sha_bytes(canonical(
        list(EXPECTED_STATIC_AUDIT_V14_INPUT_ORDER)))

    def expression_dump(source: str) -> str:
        return ast.dump(ast.parse(source, mode="eval").body,
                        annotate_fields=True, include_attributes=False)

    def need_conditions(function: ast.AST) -> list[ast.AST]:
        return [
            call.args[0] for call in ast.walk(function)
            if isinstance(call, ast.Call) and call.args and
            isinstance(call.func, ast.Name) and call.func.id == "need"]

    def equal_pair_present(
            conditions: Sequence[ast.AST], left: str, right: str) -> bool:
        left_dump = expression_dump(left)
        right_dump = expression_dump(right)
        for condition in conditions:
            for compare in ast.walk(condition):
                if not isinstance(compare, ast.Compare):
                    continue
                expressions = [compare.left, *compare.comparators]
                for index, operation in enumerate(compare.ops):
                    if not isinstance(operation, ast.Eq):
                        continue
                    pair = {
                        ast.dump(expressions[index], annotate_fields=True,
                                 include_attributes=False),
                        ast.dump(expressions[index + 1], annotate_fields=True,
                                 include_attributes=False),
                    }
                    if pair == {left_dump, right_dump}:
                        return True
        return False

    rows: dict[str, Any] = {}
    for role, (function_name, order_name, digest_name) in specifications.items():
        tree = source_trees.get(role)
        env = source_envs.get(role, {})
        functions = [
            node for node in tree.body
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and
            node.name == function_name] if isinstance(tree, ast.Module) else []
        function = functions[0] if len(functions) == 1 else None
        conditions = need_conditions(function) if function is not None else []
        expected_assignments = [
            node.value for node in function.body
            if isinstance(node, ast.Assign) and len(node.targets) == 1 and
            isinstance(node.targets[0], ast.Name) and
            node.targets[0].id == "expected_inputs" and
            isinstance(node.value, ast.Dict)] if function is not None else []
        expected_input_keys: list[Any] = []
        if len(expected_assignments) == 1:
            expected_input_keys = [
                safe_literal(key, env) for key in expected_assignments[0].keys]
        order_value = env.get(order_name)
        digest_value = env.get(digest_name)
        count_guard = False
        digest_guard = False
        for condition in conditions:
            for compare in ast.walk(condition):
                if not isinstance(compare, ast.Compare):
                    continue
                expressions = [compare.left, *compare.comparators]
                has_exact43 = any(safe_literal(item, env) == 43
                                  for item in expressions)
                has_relevant_len = any(
                    isinstance(item, ast.Call) and
                    isinstance(item.func, ast.Name) and
                    item.func.id == "len" and len(item.args) == 1 and
                    isinstance(item.args[0], ast.Name) and
                    item.args[0].id in {
                        "input_a", "input_b", "input_keys", "expected_inputs"}
                    for item in expressions)
                count_guard |= has_exact43 and has_relevant_len
                digest_guard |= (
                    any(isinstance(item, ast.Name) and item.id == digest_name
                        for item in ast.walk(compare)) and
                    any(isinstance(item, ast.Call) and
                        ((isinstance(item.func, ast.Name) and
                          item.func.id in {"digest", "sha", "sha_bytes"}) or
                         (isinstance(item.func, ast.Name) and
                          item.func.id == "canonical"))
                        for item in ast.walk(compare)))
        tuple_a_guard = equal_pair_present(
            conditions, "tuple(input_a)", order_name)
        tuple_b_guard = equal_pair_present(
            conditions, "tuple(input_b)", order_name)
        a_b_equal_guard = equal_pair_present(conditions, "input_a", "input_b")
        live_expected_guard = equal_pair_present(
            conditions, "input_a", "expected_inputs")
        exact_expected_keys = (
            tuple(expected_input_keys) == EXPECTED_STATIC_AUDIT_V14_INPUT_ORDER)
        matches = (
            len(functions) == 1 and type(order_value) is tuple and
            order_value == EXPECTED_STATIC_AUDIT_V14_INPUT_ORDER and
            digest_value == expected_digest and expected_digest ==
                "7e11baf937aa7e9695f30718fcb14793ed2fdacbdf0f33bda659086d399e4574" and
            len(expected_assignments) == 1 and exact_expected_keys and
            tuple(expected_input_keys[-6:]) == STATIC_AUDIT_V12_INPUT_SUFFIX and
            tuple_a_guard and tuple_b_guard and a_b_equal_guard and
            live_expected_guard and count_guard and digest_guard)
        rows[role] = {
            "validator_function": function_name,
            "definition_count": len(functions),
            "order_constant": order_name,
            "observed_order_count": len(order_value)
                if isinstance(order_value, tuple) else None,
            "observed_order_digest": digest_value,
            "expected_inputs_assignment_count": len(expected_assignments),
            "expected_inputs_key_count": len(expected_input_keys),
            "expected_inputs_suffix": expected_input_keys[-6:],
            "tuple_input_A_order_guard": tuple_a_guard,
            "tuple_input_B_order_guard": tuple_b_guard,
            "input_A_equals_input_B_guard": a_b_equal_guard,
            "input_A_equals_live_expected_inputs_guard": live_expected_guard,
            "explicit_exact43_count_guard": count_guard,
            "order_digest_guard": digest_guard,
            "matches": matches,
        }
    return {
        "expected_count": 43,
        "expected_order": list(EXPECTED_STATIC_AUDIT_V14_INPUT_ORDER),
        "expected_v12_suffix": list(STATIC_AUDIT_V12_INPUT_SUFFIX),
        "expected_order_sha256": expected_digest,
        "roles": rows,
        "matches": set(rows) == set(specifications) and
                   all(row["matches"] for row in rows.values()),
    }


def transition_audit_non_authority_review(
        transition: Mapping[str, Any], audit: Mapping[str, Any],
) -> dict[str, Any]:
    def exact_typed_mapping(
            observed: Mapping[str, Any], expected: Mapping[str, Any],
    ) -> bool:
        return (
            set(observed) == set(expected) and
            all(type(observed[key]) is type(value) and observed[key] == value
                for key, value in expected.items()))

    expected_transition_kind = (
        "APPEND_ONLY_V13_PREPUBLICATION_PYC_CONTAMINATION_REJECTION_TO_"
        "ZERO_CREDIT_V14_STATIC_SUCCESSOR")
    transition_expected = {
        "effective_checkpoint_object_sha256": CHECKPOINT,
        "transition_kind": expected_transition_kind,
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
    transition_observed = {
        key: transition.get(key) for key in transition_expected}
    cold_boundary = transition.get("cold_launch_boundary")
    cold_boundary = cold_boundary if isinstance(cold_boundary, dict) else {}
    transition_matches = (
        all(type(transition_observed[key]) is type(value) and
            transition_observed[key] == value
            for key, value in transition_expected.items()) and
        cold_boundary.get("runtime_entry_authorized_by_this_transition") is False and
        cold_boundary.get("manifest_or_outer_exists_at_transition_time") is False and
        cold_boundary.get("manifest_or_outer_created_by_this_transition") is False)

    credit_expected = {
        "all_persisted_v14_objects_D02_started": False,
        "all_persisted_v14_objects_D02_unlock": False,
        "all_persisted_v14_objects_formal_global_closure_credit": 0,
        "cold_live_inner_formal_global_closure_credit": 0,
        "launcher_virtual_positive_root_exact_credit_literal_count": 2,
        "only_cold_launcher_fresh_virtual_wrapper_may_derive_credit_one": True,
    }
    no_run_expected = {
        "C79_entrypoint_executed": False,
        "C79_v14_runtime_artifact_count": 0,
        "C79_v14_process_count": 0,
        "pyc_or___pycache___created": False,
        "cold_manifest_or_outer_created_before_dual_GO": False,
    }
    credit = audit.get("static_credit_census")
    no_run = audit.get("static_no_run")
    acceptance = audit.get("final_audit_acceptance")
    credit = credit if isinstance(credit, dict) else {}
    no_run = no_run if isinstance(no_run, dict) else {}
    acceptance = acceptance if isinstance(acceptance, dict) else {}
    audit_matches = (
        audit.get("effective_checkpoint_object_sha256") == CHECKPOINT and
        exact_typed_mapping(credit, credit_expected) and
        exact_typed_mapping(no_run, no_run_expected) and
        acceptance.get("this_audit_authorizes_C79_runtime") is False and
        acceptance.get(
            "requires_cold_exact8_freeze_manifest_then_outer_last_and_terminal_replay")
            is True)
    return {
        "transition_expected": transition_expected,
        "transition_observed": transition_observed,
        "cold_launch_boundary": cold_boundary,
        "transition_matches": transition_matches,
        "audit_static_credit_expected": credit_expected,
        "audit_static_credit_observed": credit,
        "audit_static_no_run_expected": no_run_expected,
        "audit_static_no_run_observed": no_run,
        "audit_acceptance": acceptance,
        "audit_matches": audit_matches,
        "matches": transition_matches and audit_matches,
    }


def final_pin_graph_in_memory_negative_tests(
        source_trees: Mapping[str, ast.Module],
        source_envs: Mapping[str, Mapping[str, Any]],
        receipt_review: Mapping[str, Any],
) -> dict[str, Any]:
    """Exercise the six lifecycle predicates against in-memory tampering."""
    rows: dict[str, Any] = {}

    synthetic_envs = copy.deepcopy(dict(source_envs))
    for role in ("producer", "consumer", "launcher"):
        synthetic_envs.setdefault(role, {})
    synthetic_envs["producer"].update({
        "V14_DRAFT_CORE_PIN_SENTINELS":
            ("d0" * 32, "e0" * 32, "f0" * 32),
        "CONTRACT_FILE_PIN": "d0" * 32,
        "CONTRACT_OBJECT_PIN": "e0" * 32,
        "CLOSED_SCHEMA_FILE_PIN": "f0" * 32,
    })
    synthetic_envs["consumer"].update({
        "V14_DRAFT_CURRENT_CORE_PINS":
            ("d9" * 32, "e9" * 32, "f9" * 32, "a9" * 32),
        "CONTRACT_FILE_PIN": "d9" * 32,
        "CONTRACT_OBJECT_PIN": "e9" * 32,
        "CLOSED_SCHEMA_FILE_PIN": "f9" * 32,
        "PRODUCER_SOURCE_PIN": "a9" * 32,
    })
    synthetic_envs["launcher"].update({
        "_DRAFT_FILE_PIN": "f" * 64,
        "_DRAFT_OBJECT_PIN": "e" * 64,
    })
    synthetic_trees = copy.deepcopy(dict(source_trees))

    def force_launcher_draft_base7(tree: ast.Module) -> bool:
        configure = [
            node for node in tree.body
            if isinstance(node, ast.FunctionDef) and
            node.name == "configure_workspace_paths"]
        if len(configure) != 1:
            return False
        assignments = [
            node for node in configure[0].body
            if isinstance(node, ast.Assign) and len(node.targets) == 1 and
            isinstance(node.targets[0], ast.Name) and
            node.targets[0].id == "BASE7_PINS" and
            isinstance(node.value, ast.Dict)]
        if len(assignments) != 1:
            return False
        base7 = assignments[0].value
        key_order = [
            key.id if isinstance(key, ast.Name) else None for key in base7.keys]
        expected_order = [
            "V13_SUPERSESSION_RECEIPT", "SCHEMA", "CONTRACT", "PRODUCER",
            "CONSUMER", "TRANSITION", "AUDIT"]
        if key_order != expected_order or len(base7.values) != 7:
            return False
        object_names = {"CONTRACT", "TRANSITION", "AUDIT"}
        for index, key in enumerate(key_order[1:], start=1):
            base7.values[index] = ast.Tuple(
                elts=[
                    ast.Name(id="_DRAFT_FILE_PIN", ctx=ast.Load()),
                    ast.Name(id="_DRAFT_OBJECT_PIN", ctx=ast.Load())
                    if key in object_names else ast.Constant(value=None),
                ], ctx=ast.Load())
        ast.fix_missing_locations(tree)
        return True

    launcher_tree = synthetic_trees.get("launcher")
    synthetic_launcher_ready = (
        isinstance(launcher_tree, ast.Module) and
        force_launcher_draft_base7(launcher_tree))
    active_baseline = draft_active_pin_graph_review(
        synthetic_trees, synthetic_envs, receipt_review)
    active_env_tamper = copy.deepcopy(synthetic_envs)
    active_env_tamper["producer"]["CONTRACT_FILE_PIN"] = "0" * 64
    active_source_rejected = not draft_active_pin_graph_review(
        synthetic_trees, active_env_tamper, receipt_review)["matches"]
    active_tree_tamper = copy.deepcopy(synthetic_trees)
    active_launcher_tamper_ready = False
    tamper_launcher = active_tree_tamper.get("launcher")
    if isinstance(tamper_launcher, ast.Module):
        configure = [
            node for node in tamper_launcher.body
            if isinstance(node, ast.FunctionDef) and
            node.name == "configure_workspace_paths"]
        if len(configure) == 1:
            dictionaries = [
                node.value for node in configure[0].body
                if isinstance(node, ast.Assign) and len(node.targets) == 1 and
                isinstance(node.targets[0], ast.Name) and
                node.targets[0].id == "BASE7_PINS" and
                isinstance(node.value, ast.Dict)]
            if len(dictionaries) == 1 and len(dictionaries[0].values) == 7:
                dictionaries[0].values[1] = ast.Tuple(
                    elts=[ast.Constant(value="0" * 64), ast.Constant(value=None)],
                    ctx=ast.Load())
                ast.fix_missing_locations(tamper_launcher)
                active_launcher_tamper_ready = True
    active_launcher_rejected = (
        active_launcher_tamper_ready and
        not draft_active_pin_graph_review(
            active_tree_tamper, synthetic_envs, receipt_review)["matches"])
    rows["draft_active_P_C_and_launcher_BASE7"] = {
        "synthetic_launcher_ready": synthetic_launcher_ready,
        "baseline_passed": active_baseline["matches"],
        "producer_active_pin_tamper_rejected": active_source_rejected,
        "launcher_BASE7_tamper_rejected": active_launcher_rejected,
        "matches": (
            synthetic_launcher_ready and active_baseline["matches"] and
            active_source_rejected and active_launcher_rejected),
    }

    synthetic_inputs = {
        key: sha_bytes(("negative-test:" + key).encode("utf-8"))
        for key in EXPECTED_STATIC_AUDIT_V14_INPUT_ORDER}
    checker_names = ("checker_A", "checker_B")
    synthetic_dual = {
        name: {"input_sha256": dict(synthetic_inputs)}
        for name in checker_names}
    exact43_baseline = exact43_audit_input_review(
        synthetic_dual, synthetic_inputs)
    exact43_cases: dict[str, bool] = {}
    missing = copy.deepcopy(synthetic_dual)
    missing["checker_A"]["input_sha256"].pop(
        EXPECTED_STATIC_AUDIT_V14_INPUT_ORDER[-1])
    exact43_cases["missing_key"] = not exact43_audit_input_review(
        missing, synthetic_inputs)["matches"]
    reordered = copy.deepcopy(synthetic_dual)
    reordered_a = reordered["checker_A"]["input_sha256"]
    first, second, *rest = EXPECTED_STATIC_AUDIT_V14_INPUT_ORDER
    reordered["checker_A"]["input_sha256"] = {
        second: reordered_a[second], first: reordered_a[first],
        **{key: reordered_a[key] for key in rest}}
    exact43_cases["wrong_order"] = not exact43_audit_input_review(
        reordered, synthetic_inputs)["matches"]
    wrong_value = copy.deepcopy(synthetic_dual)
    wrong_value["checker_B"]["input_sha256"][first] = "0" * 64
    exact43_cases["wrong_value"] = not exact43_audit_input_review(
        wrong_value, synthetic_inputs)["matches"]
    validator_baseline = static_audit_validator_exact43_review(
        source_trees, source_envs)
    validator_tamper_trees = copy.deepcopy(dict(source_trees))
    launcher_validator_tamper = validator_tamper_trees.get("launcher")
    validator_tamper_ready = False
    if isinstance(launcher_validator_tamper, ast.Module):
        validators = [
            node for node in launcher_validator_tamper.body
            if isinstance(node, ast.FunctionDef) and
            node.name == "validate_final_static_audit"]
        if len(validators) == 1:
            input_dicts = [
                node.value for node in validators[0].body
                if isinstance(node, ast.Assign) and len(node.targets) == 1 and
                isinstance(node.targets[0], ast.Name) and
                node.targets[0].id == "expected_inputs" and
                isinstance(node.value, ast.Dict)]
            if len(input_dicts) == 1 and input_dicts[0].keys:
                input_dicts[0].keys.pop()
                input_dicts[0].values.pop()
                ast.fix_missing_locations(launcher_validator_tamper)
                validator_tamper_ready = True
    validator_suffix_tamper_rejected = (
        validator_tamper_ready and
        not static_audit_validator_exact43_review(
            validator_tamper_trees, source_envs)["matches"])
    rows["audit_A_B_exact43_key_order_value"] = {
        "baseline_passed": exact43_baseline["matches"],
        "tamper_rejected": exact43_cases,
        "source_validator_baseline_passed": validator_baseline["matches"],
        "source_validator_v12_suffix_tamper_ready": validator_tamper_ready,
        "source_validator_v12_suffix_tamper_rejected":
            validator_suffix_tamper_rejected,
        "matches": (
            exact43_baseline["matches"] and all(exact43_cases.values()) and
            validator_baseline["matches"] and
            validator_suffix_tamper_rejected),
    }

    sentinel_baseline = sentinel_declaration_review(
        synthetic_envs, synthetic_trees)
    sentinel_cases: dict[str, bool] = {}
    sentinel_type = copy.deepcopy(synthetic_envs)
    sentinel_type["producer"]["V14_DRAFT_CORE_PIN_SENTINELS"] = list(
        sentinel_type["producer"]["V14_DRAFT_CORE_PIN_SENTINELS"])
    sentinel_cases["wrong_type"] = not sentinel_declaration_review(
        sentinel_type, synthetic_trees)["matches"]
    sentinel_count = copy.deepcopy(synthetic_envs)
    sentinel_count["consumer"]["V14_DRAFT_CURRENT_CORE_PINS"] = (
        sentinel_count["consumer"]["V14_DRAFT_CURRENT_CORE_PINS"][:-1])
    sentinel_cases["wrong_count"] = not sentinel_declaration_review(
        sentinel_count, synthetic_trees)["matches"]
    sentinel_value = copy.deepcopy(synthetic_envs)
    declared = sentinel_value["producer"]["V14_DRAFT_CORE_PIN_SENTINELS"]
    sentinel_value["producer"]["V14_DRAFT_CORE_PIN_SENTINELS"] = (
        "0" * 64, *declared[1:])
    sentinel_cases["wrong_value"] = not sentinel_declaration_review(
        sentinel_value, synthetic_trees)["matches"]
    duplicate_tree_set = copy.deepcopy(synthetic_trees)
    duplicate_producer = duplicate_tree_set.get("producer")
    duplicate_ready = False
    if isinstance(duplicate_producer, ast.Module):
        declaration_nodes = module_assignments(duplicate_producer).get(
            "V14_DRAFT_CORE_PIN_SENTINELS", [])
        if len(declaration_nodes) == 1:
            duplicate_producer.body.append(ast.Assign(
                targets=[ast.Name(
                    id="V14_DRAFT_CORE_PIN_SENTINELS", ctx=ast.Store())],
                value=copy.deepcopy(declaration_nodes[0])))
            ast.fix_missing_locations(duplicate_producer)
            duplicate_ready = True
    sentinel_cases["duplicate_module_declaration"] = (
        duplicate_ready and
        not sentinel_declaration_review(
            synthetic_envs, duplicate_tree_set)["matches"])
    rows["sentinel_declaration_type_count_value"] = {
        "baseline_passed": sentinel_baseline["matches"],
        "tamper_rejected": sentinel_cases,
        "matches": sentinel_baseline["matches"] and all(sentinel_cases.values()),
    }

    path_baseline = (
        launcher_configured_path_graph_review(source_trees["launcher"])
        if "launcher" in source_trees else {"matches": False})
    path_tree = copy.deepcopy(source_trees.get("launcher"))
    path_tamper_ready = False
    if isinstance(path_tree, ast.Module):
        configure = [
            node for node in path_tree.body
            if isinstance(node, ast.FunctionDef) and
            node.name == "configure_workspace_paths"]
        if len(configure) == 1:
            assignments = [
                node for node in configure[0].body
                if isinstance(node, ast.Assign) and len(node.targets) == 1 and
                isinstance(node.targets[0], ast.Name) and
                node.targets[0].id == "SCHEMA"]
            if len(assignments) == 1:
                assignments[0].value = ast.copy_location(
                    ast.Constant(value="tampered-schema-path"),
                    assignments[0].value)
                ast.fix_missing_locations(path_tree)
                path_tamper_ready = True
    path_rejected = (
        path_tamper_ready and isinstance(path_tree, ast.Module) and
        not launcher_configured_path_graph_review(path_tree)["matches"])
    rows["launcher_configured_path_graph"] = {
        "baseline_passed": path_baseline["matches"],
        "tamper_ready": path_tamper_ready,
        "tamper_rejected": path_rejected,
        "matches": path_baseline["matches"] and path_rejected,
    }

    empty_non_authority = transition_audit_non_authority_review({}, {})
    transition_template = {
        **empty_non_authority["transition_expected"],
        "cold_launch_boundary": {
            "runtime_entry_authorized_by_this_transition": False,
            "manifest_or_outer_exists_at_transition_time": False,
            "manifest_or_outer_created_by_this_transition": False,
        },
    }
    audit_template = {
        "effective_checkpoint_object_sha256": CHECKPOINT,
        "static_credit_census":
            empty_non_authority["audit_static_credit_expected"],
        "static_no_run": empty_non_authority["audit_static_no_run_expected"],
        "final_audit_acceptance": {
            "this_audit_authorizes_C79_runtime": False,
            "requires_cold_exact8_freeze_manifest_then_outer_last_and_terminal_replay":
                True,
        },
    }
    non_authority_baseline = transition_audit_non_authority_review(
        transition_template, audit_template)
    non_authority_cases: dict[str, bool] = {}
    bad_checkpoint = copy.deepcopy(transition_template)
    bad_checkpoint["effective_checkpoint_object_sha256"] = "0" * 64
    non_authority_cases["transition_checkpoint"] = not \
        transition_audit_non_authority_review(
        bad_checkpoint, audit_template)["matches"]
    bad_audit_checkpoint = copy.deepcopy(audit_template)
    bad_audit_checkpoint["effective_checkpoint_object_sha256"] = "0" * 64
    non_authority_cases["audit_checkpoint"] = not \
        transition_audit_non_authority_review(
            transition_template, bad_audit_checkpoint)["matches"]
    bad_kind = copy.deepcopy(transition_template)
    bad_kind["transition_kind"] = "TAMPERED"
    non_authority_cases["transition_kind"] = not \
        transition_audit_non_authority_review(bad_kind, audit_template)["matches"]
    bad_credit = copy.deepcopy(transition_template)
    bad_credit["D02_unlock"] = True
    non_authority_cases["zero_credit_D02_flags"] = not \
        transition_audit_non_authority_review(bad_credit, audit_template)["matches"]
    bad_persisted_credit = copy.deepcopy(transition_template)
    bad_persisted_credit["all_persisted_credit"] = 1
    non_authority_cases["all_persisted_credit"] = not \
        transition_audit_non_authority_review(
            bad_persisted_credit, audit_template)["matches"]
    bad_transition_runtime = copy.deepcopy(transition_template)
    bad_transition_runtime["runtime_executed_during_transition"] = True
    non_authority_cases["transition_runtime_executed"] = not \
        transition_audit_non_authority_review(
            bad_transition_runtime, audit_template)["matches"]
    bad_boundary = copy.deepcopy(transition_template)
    bad_boundary["cold_launch_boundary"][
        "runtime_entry_authorized_by_this_transition"] = True
    non_authority_cases["transition_runtime_authorized"] = not \
        transition_audit_non_authority_review(
            bad_boundary, audit_template)["matches"]
    bad_no_run = copy.deepcopy(audit_template)
    bad_no_run["static_no_run"]["C79_entrypoint_executed"] = True
    non_authority_cases["static_no_run"] = not \
        transition_audit_non_authority_review(
            transition_template, bad_no_run)["matches"]
    bad_authorization = copy.deepcopy(audit_template)
    bad_authorization["final_audit_acceptance"][
        "this_audit_authorizes_C79_runtime"] = True
    non_authority_cases["this_audit_authorizes"] = not \
        transition_audit_non_authority_review(
            transition_template, bad_authorization)["matches"]
    rows["transition_audit_non_authority"] = {
        "baseline_passed": non_authority_baseline["matches"],
        "tamper_rejected": non_authority_cases,
        "matches": (
            non_authority_baseline["matches"] and
            all(non_authority_cases.values())),
    }

    final_names = {
        "producer": "FINAL_V14_CORE_PINS_INSTALLED",
        "consumer": "FINAL_CURRENT_V14_PINS_INSTALLED",
        "launcher": "FINAL_BASE7_PINS_INSTALLED",
    }
    main_baselines = {
        role: draft_final_main_gate_review(source_trees[role], flag)
        for role, flag in final_names.items() if role in source_trees}
    main_baseline_passed = (
        set(main_baselines) == set(final_names) and
        all(row["matches"] for row in main_baselines.values()))
    main_cases: dict[str, bool] = {}
    unsafe_tree = copy.deepcopy(source_trees.get("producer"))
    unsafe_ready = False
    if isinstance(unsafe_tree, ast.Module):
        mains = [
            node for node in unsafe_tree.body
            if isinstance(node, ast.FunctionDef) and node.name == "main"]
        if len(mains) == 1:
            gates = [
                (index, node) for index, node in enumerate(mains[0].body)
                if isinstance(node, ast.If) and any(
                    isinstance(item, ast.Name) and
                    item.id == "V14_DRAFT_RUNTIME_DISABLED"
                    for item in ast.walk(node.test))]
            if len(gates) == 1:
                index, gate = gates[0]
                unsafe_call = ast.Expr(value=ast.Call(
                    func=ast.Name(id="open", ctx=ast.Load()),
                    args=[ast.Constant(value="tampered")], keywords=[]))
                mains[0].body.insert(index, ast.copy_location(unsafe_call, gate))
                ast.fix_missing_locations(unsafe_tree)
                unsafe_ready = True
    main_cases["pre_gate_side_effect_or_input_read"] = (
        unsafe_ready and isinstance(unsafe_tree, ast.Module) and
        not draft_final_main_gate_review(
            unsafe_tree, final_names["producer"])["matches"])
    no_terminator_tree = copy.deepcopy(source_trees.get("producer"))
    no_terminator_ready = False
    if isinstance(no_terminator_tree, ast.Module):
        mains = [
            node for node in no_terminator_tree.body
            if isinstance(node, ast.FunctionDef) and node.name == "main"]
        if len(mains) == 1:
            gates = [
                node for node in mains[0].body
                if isinstance(node, ast.If) and any(
                    isinstance(item, ast.Name) and
                    item.id == "V14_DRAFT_RUNTIME_DISABLED"
                    for item in ast.walk(node.test))]
            if len(gates) == 1:
                gates[0].body = [ast.copy_location(ast.Pass(), gates[0])]
                ast.fix_missing_locations(no_terminator_tree)
                no_terminator_ready = True
    main_cases["non_terminating_gate"] = (
        no_terminator_ready and isinstance(no_terminator_tree, ast.Module) and
        not draft_final_main_gate_review(
            no_terminator_tree, final_names["producer"])["matches"])
    unsafe_body_tree = copy.deepcopy(source_trees.get("producer"))
    unsafe_body_ready = False
    if isinstance(unsafe_body_tree, ast.Module):
        mains = [
            node for node in unsafe_body_tree.body
            if isinstance(node, ast.FunctionDef) and node.name == "main"]
        if len(mains) == 1:
            gates = [
                node for node in mains[0].body
                if isinstance(node, ast.If) and any(
                    isinstance(item, ast.Name) and
                    item.id == "V14_DRAFT_RUNTIME_DISABLED"
                    for item in ast.walk(node.test))]
            if len(gates) == 1:
                unsafe_call = ast.Expr(value=ast.Call(
                    func=ast.Name(id="open", ctx=ast.Load()),
                    args=[ast.Constant(value="tampered")], keywords=[]))
                gates[0].body.insert(
                    0, ast.copy_location(unsafe_call, gates[0].body[0]))
                ast.fix_missing_locations(unsafe_body_tree)
                unsafe_body_ready = True
    main_cases["draft_gate_body_side_effect_before_raise"] = (
        unsafe_body_ready and isinstance(unsafe_body_tree, ast.Module) and
        not draft_final_main_gate_review(
            unsafe_body_tree, final_names["producer"])["matches"])
    wrong_predicate_tree = copy.deepcopy(source_trees.get("producer"))
    wrong_predicate_ready = False
    if isinstance(wrong_predicate_tree, ast.Module):
        mains = [
            node for node in wrong_predicate_tree.body
            if isinstance(node, ast.FunctionDef) and node.name == "main"]
        if len(mains) == 1:
            gates = [
                node for node in mains[0].body
                if isinstance(node, ast.If) and any(
                    isinstance(item, ast.Name) and
                    item.id == "V14_DRAFT_RUNTIME_DISABLED"
                    for item in ast.walk(node.test))]
            if len(gates) == 1 and isinstance(gates[0].test, ast.BoolOp):
                gates[0].test.values.reverse()
                ast.fix_missing_locations(wrong_predicate_tree)
                wrong_predicate_ready = True
    main_cases["wrong_boolean_gate_AST"] = (
        wrong_predicate_ready and
        isinstance(wrong_predicate_tree, ast.Module) and
        not draft_final_main_gate_review(
            wrong_predicate_tree, final_names["producer"])["matches"])
    rows["main_pre_effect_terminating_draft_gate"] = {
        "baseline_passed": main_baseline_passed,
        "tamper_rejected": main_cases,
        "matches": main_baseline_passed and all(main_cases.values()),
    }

    return {
        "test_class_count": len(rows),
        "expected_test_class_count": 6,
        "classes": rows,
        "matches": len(rows) == 6 and all(row["matches"] for row in rows.values()),
    }


def mutually_exclusive_json_lifecycle_review(
        final_flags: Mapping[str, Any],
        json_presence: Mapping[str, Any],
        final_bundle_matches: bool,
) -> dict[str, Any]:
    """Accept exactly the absent draft or the complete final lifecycle."""
    expected_flag_roles = {"producer", "consumer", "launcher"}
    expected_json_names = {"schema", "contract", "transition", "audit"}
    flags_shape_matches = (
        set(final_flags) == expected_flag_roles and
        all(type(value) is bool for value in final_flags.values()))
    presence_shape_matches = (
        set(json_presence) == expected_json_names and
        all(type(value) is bool for value in json_presence.values()))
    all_flags_false = (
        flags_shape_matches and all(value is False for value in final_flags.values()))
    all_flags_true = (
        flags_shape_matches and all(value is True for value in final_flags.values()))
    all_json_absent = (
        presence_shape_matches and
        all(value is False for value in json_presence.values()))
    all_json_present = (
        presence_shape_matches and
        all(value is True for value in json_presence.values()))
    draft_matches = all_flags_false and all_json_absent
    final_matches = (
        all_flags_true and all_json_present and final_bundle_matches is True)
    matches = (draft_matches is True) != (final_matches is True)
    return {
        "flags_shape_matches": flags_shape_matches,
        "presence_shape_matches": presence_shape_matches,
        "all_flags_false": all_flags_false,
        "all_flags_true": all_flags_true,
        "all_json_absent": all_json_absent,
        "all_json_present": all_json_present,
        "final_bundle_matches": final_bundle_matches,
        "draft_matches": draft_matches,
        "final_matches": final_matches,
        "state": (
            "safe_prebuilder_draft" if draft_matches else
            "complete_final" if final_matches else "mixed_or_partial_invalid"),
        "matches": matches,
    }


def mutually_exclusive_json_lifecycle_in_memory_tests() -> dict[str, Any]:
    false_flags = {role: False for role in ("producer", "consumer", "launcher")}
    true_flags = {role: True for role in ("producer", "consumer", "launcher")}
    absent = {
        name: False for name in ("schema", "contract", "transition", "audit")}
    present = {name: True for name in absent}

    draft = mutually_exclusive_json_lifecycle_review(
        false_flags, absent, False)
    final = mutually_exclusive_json_lifecycle_review(
        true_flags, present, True)
    mixed_flags = dict(false_flags)
    mixed_flags["launcher"] = True
    mixed = mutually_exclusive_json_lifecycle_review(
        mixed_flags, absent, False)
    partial_draft_presence = dict(absent)
    partial_draft_presence["schema"] = True
    partial_draft = mutually_exclusive_json_lifecycle_review(
        false_flags, partial_draft_presence, False)
    partial_final_presence = dict(present)
    partial_final_presence["audit"] = False
    partial_final = mutually_exclusive_json_lifecycle_review(
        true_flags, partial_final_presence, True)
    incomplete_final_bundle = mutually_exclusive_json_lifecycle_review(
        true_flags, present, False)
    cases = {
        "safe_prebuilder_draft_positive": {
            "observed": draft,
            "matches": draft["matches"] is True and
                       draft["state"] == "safe_prebuilder_draft"},
        "complete_final_positive": {
            "observed": final,
            "matches": final["matches"] is True and
                       final["state"] == "complete_final"},
        "mixed_flags_negative": {
            "observed": mixed,
            "matches": mixed["matches"] is False and
                       mixed["state"] == "mixed_or_partial_invalid"},
        "partial_JSON_in_draft_negative": {
            "observed": partial_draft,
            "matches": partial_draft["matches"] is False},
        "partial_JSON_in_final_negative": {
            "observed": partial_final,
            "matches": partial_final["matches"] is False},
        "complete_presence_but_incomplete_final_bundle_negative": {
            "observed": incomplete_final_bundle,
            "matches": incomplete_final_bundle["matches"] is False},
    }
    return {
        "case_count": len(cases),
        "cases": cases,
        "matches": len(cases) == 6 and
                   all(row["matches"] for row in cases.values()),
    }


def final_pin_graph_review(
        source_raw: Mapping[str, bytes],
        source_trees: Mapping[str, ast.Module],
        source_envs: Mapping[str, Mapping[str, Any]],
        json_presence: Mapping[str, bool],
        json_raw: Mapping[str, bytes],
        json_values: Mapping[str, Any],
        json_duplicates: Mapping[str, Sequence[str]],
        json_closures: Mapping[str, Mapping[str, Any] | None],
        receipt_review: Mapping[str, Any],
        external_audit_input_evidence: Mapping[str, Any],
) -> dict[str, Any]:
    """Close the final S/C/P/C/T/A/L pin graph from inert held bytes.

    Absence of all four JSON surfaces with all three final flags false is the
    one safe draft state.  Every other state must be the complete final graph;
    partial pin installation is never accepted as a lifecycle state.
    """
    final_names = {
        "producer": "FINAL_V14_CORE_PINS_INSTALLED",
        "consumer": "FINAL_CURRENT_V14_PINS_INSTALLED",
        "launcher": "FINAL_BASE7_PINS_INSTALLED",
    }
    final_flags = {
        role: source_envs.get(role, {}).get(name)
        for role, name in final_names.items()}
    all_absent = not any(json_presence.values())
    all_present = all(json_presence.values())
    draft_flags_and_absence_match = (
        all_absent and set(final_flags) == set(final_names) and
        all(value is False for value in final_flags.values()))
    sentinel_declarations = sentinel_declaration_review(
        source_envs, source_trees)
    launcher_tree_for_lifecycle = source_trees.get("launcher")
    draft_active_pins = draft_active_pin_graph_review(
        source_trees, source_envs, receipt_review)
    launcher_paths = (
        launcher_configured_path_graph_review(launcher_tree_for_lifecycle)
        if isinstance(launcher_tree_for_lifecycle, ast.Module) else {
            "matches": False, "error": "launcher AST unavailable"})
    main_control_flow = {
        role: draft_final_main_gate_review(source_trees[role], final_names[role])
        for role in final_names if role in source_trees}
    main_control_flow_matches = (
        set(main_control_flow) == set(final_names) and
        all(row["matches"] for row in main_control_flow.values()))
    in_memory_negative_tests = final_pin_graph_in_memory_negative_tests(
        source_trees, source_envs, receipt_review)
    draft_matches = (
        draft_flags_and_absence_match and sentinel_declarations["matches"] and
        draft_active_pins["matches"] and
        launcher_paths.get("matches") is True and main_control_flow_matches and
        in_memory_negative_tests.get("matches") is True and
        external_audit_input_evidence.get("matches") is True)

    source_hashes = {
        role: sha_bytes(raw) for role, raw in source_raw.items()}
    file_hashes = {
        name: sha_bytes(raw) for name, raw in json_raw.items()}
    object_hashes = {
        name: closure.get("declared")
        for name, closure in json_closures.items()
        if isinstance(closure, Mapping) and closure.get("matches") is True}
    expected_json_names = {"schema", "contract", "transition", "audit"}
    strict_json_rows: dict[str, Any] = {}
    for name in expected_json_names:
        value = json_values.get(name)
        duplicates = list(json_duplicates.get(name, []))
        closure = json_closures.get(name)
        closure_required = name != "schema"
        matches = (
            json_presence.get(name) is True and isinstance(value, dict) and
            not duplicates and
            (not closure_required or
             (isinstance(closure, Mapping) and closure.get("matches") is True)))
        strict_json_rows[name] = {
            "present": json_presence.get(name) is True,
            "root_is_object": isinstance(value, dict),
            "duplicate_keys": duplicates,
            "object_closure_required": closure_required,
            "object_closure": closure,
            "matches": matches,
        }
    strict_json_matches = (
        set(strict_json_rows) == expected_json_names and
        all(row["matches"] for row in strict_json_rows.values()))

    schema_path = str(V14_JSON["schema"].relative_to(ROOT))
    contract_path = str(V14_JSON["contract"].relative_to(ROOT))
    transition_path = str(V14_JSON["transition"].relative_to(ROOT))
    audit_path = str(V14_JSON["audit"].relative_to(ROOT))
    producer_path = str(V14_PYTHON["producer"].relative_to(ROOT))
    consumer_path = str(V14_PYTHON["consumer"].relative_to(ROOT))
    launcher_path = str(V14_PYTHON["launcher"].relative_to(ROOT))
    receipt_path = str(V13_SUPERSESSION_RECEIPT.relative_to(ROOT))
    manifest_path = str(V14_MANIFEST.relative_to(ROOT))
    outer_path = str(V14_OUTER.relative_to(ROOT))
    expected_base7_paths = [
        receipt_path, schema_path, contract_path, producer_path, consumer_path,
        transition_path, audit_path]
    expected_exact8_paths = [*expected_base7_paths, launcher_path]

    schema = json_values.get("schema")
    contract = json_values.get("contract")
    transition = json_values.get("transition")
    audit = json_values.get("audit")
    schema_map = schema if isinstance(schema, dict) else {}
    contract_map = contract if isinstance(contract, dict) else {}
    transition_map = transition if isinstance(transition, dict) else {}
    audit_map = audit if isinstance(audit, dict) else {}

    contract_bundle = contract_map.get("v14_bundle", {})
    contract_bundle = contract_bundle if isinstance(contract_bundle, dict) else {}
    closed_schema = contract_bundle.get("closed_schema", {})
    closed_schema = closed_schema if isinstance(closed_schema, dict) else {}
    contract_self = contract_bundle.get("contract", {})
    contract_self = contract_self if isinstance(contract_self, dict) else {}
    producer_contract = contract_bundle.get("build_only_producer", {})
    producer_contract = producer_contract if isinstance(producer_contract, dict) else {}
    consumer_contract = contract_bundle.get(
        "independent_verifier_assembler_authority_consumer", {})
    consumer_contract = consumer_contract if isinstance(consumer_contract, dict) else {}
    trust_receipts = contract_bundle.get("post_source_static_trust_receipts", {})
    trust_receipts = trust_receipts if isinstance(trust_receipts, dict) else {}
    publication_paths = contract_map.get("exact_publication_paths", {})
    publication_paths = publication_paths if isinstance(publication_paths, dict) else {}
    static_requirements = contract_map.get("static_freeze_protocol_requirements", {})
    static_requirements = static_requirements if isinstance(
        static_requirements, dict) else {}
    expected_contract_status = (
        "STATIC_CONTRACT_BYTES_FINAL__COLD_FREEZE_PENDING__"
        "RUNTIME_NOT_AUTHORIZED")
    expected_schema_id = (
        "cm2.round306c79g.true-global-no-producer-consumer."
        "v14.composite-authority-schema")
    contract_paths_match = (
        contract_bundle.get("base7_ordered_paths") == expected_base7_paths and
        contract_bundle.get("exact8_ordered_paths") == expected_exact8_paths and
        closed_schema.get("path") == schema_path and
        closed_schema.get("file_sha256") == file_hashes.get("schema") and
        contract_self.get("path") == contract_path and
        producer_contract.get("path") == producer_path and
        consumer_contract.get("path") == consumer_path and
        trust_receipts.get("static_audit_path") == audit_path and
        trust_receipts.get("v13_to_v14_transition_path") == transition_path and
        publication_paths.get("cold_launcher") == launcher_path and
        publication_paths.get("cold_launch_exact8_manifest") == manifest_path and
        publication_paths.get("cold_launch_outer_last") == outer_path and
        publication_paths.get("v14_rejection_namespace") == str(
            Path(".cm2-runtime") / f"c79g-v14-rejections-{CHECKPOINT}") and
        publication_paths.get("v14_later_rejection") == str(
            Path(".cm2-runtime") / f"c79g-v14-rejections-{CHECKPOINT}" /
            "rejection.json"))
    contract_review = {
        "schema_id": schema_map.get("$id"),
        "contract_schema": contract_map.get("schema"),
        "contract_status": contract_map.get("status"),
        "closed_schema_pin": closed_schema,
        "configured_base7_paths": contract_bundle.get("base7_ordered_paths"),
        "configured_exact8_paths": contract_bundle.get("exact8_ordered_paths"),
        "v14_publication_paths": publication_paths,
        "paths_match": contract_paths_match,
        "matches": (
            schema_map.get("$id") == expected_schema_id and
            contract_map.get("schema") ==
                "cm2.round306c79g.true-global-no-producer-consumer.v14.contract" and
            contract_map.get("status") == expected_contract_status and
            contract_paths_match and
            static_requirements.get("zero_or_nonhex_placeholders_remaining")
                is False),
    }

    producer_env = source_envs.get("producer", {})
    consumer_env = source_envs.get("consumer", {})
    producer_expected = {
        "CLOSED_SCHEMA_FILE_PIN": file_hashes.get("schema"),
        "CONTRACT_FILE_PIN": file_hashes.get("contract"),
        "CONTRACT_OBJECT_PIN": object_hashes.get("contract"),
    }
    producer_observed = {
        key: producer_env.get(key) for key in producer_expected}
    producer_pin_review = {
        "final_flag": final_flags.get("producer"),
        "expected": producer_expected,
        "observed": producer_observed,
        "matches": (
            final_flags.get("producer") is True and
            producer_observed == producer_expected and
            all(isinstance(value, str) and HEX64.fullmatch(value)
                for value in producer_expected.values())),
    }
    consumer_expected = {
        **producer_expected,
        "PRODUCER_SOURCE_PIN": source_hashes.get("producer"),
    }
    consumer_observed = {
        key: consumer_env.get(key) for key in consumer_expected}
    consumer_pin_review = {
        "final_flag": final_flags.get("consumer"),
        "expected": consumer_expected,
        "observed": consumer_observed,
        "matches": (
            final_flags.get("consumer") is True and
            consumer_observed == consumer_expected and
            all(isinstance(value, str) and HEX64.fullmatch(value)
                for value in consumer_expected.values())),
    }

    transition_bundle = transition_map.get("successor_v14_static_bundle", {})
    transition_bundle = transition_bundle if isinstance(
        transition_bundle, dict) else {}

    def pinned_member(
            container: Mapping[str, Any], name: str, path: str,
            file_hash: Any, object_hash: Any = MISSING) -> bool:
        member = container.get(name)
        if not isinstance(member, dict):
            return False
        matches = member.get("path") == path and member.get(
            "file_sha256") == file_hash
        if object_hash is not MISSING:
            matches &= member.get("object_sha256") == object_hash
        return bool(matches)

    transition_members_match = (
        pinned_member(transition_bundle, "closed_schema", schema_path,
                      file_hashes.get("schema")) and
        pinned_member(transition_bundle, "contract", contract_path,
                      file_hashes.get("contract"),
                      object_hashes.get("contract")) and
        pinned_member(transition_bundle, "build_only_producer", producer_path,
                      source_hashes.get("producer")) and
        pinned_member(
            transition_bundle,
            "independent_verifier_assembler_authority_consumer",
            consumer_path, source_hashes.get("consumer")))
    non_authority_review = transition_audit_non_authority_review(
        transition_map, audit_map)
    transition_review = {
        "schema": transition_map.get("schema"),
        "status": transition_map.get("status"),
        "receipt_path": transition_map.get("receipt_path"),
        "successor_v14_static_bundle": transition_bundle,
        "members_match": transition_members_match,
        "non_authority": non_authority_review,
        "matches": (
            transition_map.get("schema") ==
                "cm2.round306c79g.true-global-no-producer-consumer."
                "v13-to-v14-static-launch-transition.v1" and
            transition_map.get("status") ==
                "STATIC_BYTES_CLOSED_V13_TO_V14__PHYSICAL_FREEZE_PENDING__"
                "RUNTIME_NOT_AUTHORIZED" and
            transition_map.get("receipt_path") == transition_path and
            transition_members_match and
            transition_bundle.get("draft_pin_sentinels_remain_present") is False and
            transition_bundle.get("final_consumer_pin_installed") is True and
            transition_bundle.get("all_four_core_file_pins_final") is True and
            transition_bundle.get("static_audit_v14_path") == audit_path and
            transition_bundle.get("cold_launcher_v14_path") == launcher_path and
            non_authority_review.get("transition_matches") is True),
    }

    pin_normalized = independent_pin_normalized_launcher_ast_review(
        source_raw.get("launcher", b""))
    normalized_digest = pin_normalized.get("sha256")
    audit_bundle = audit_map.get("audited_v14_bundle", {})
    audit_bundle = audit_bundle if isinstance(audit_bundle, dict) else {}
    audit_members_match = (
        pinned_member(audit_bundle, "closed_schema", schema_path,
                      file_hashes.get("schema")) and
        pinned_member(audit_bundle, "contract", contract_path,
                      file_hashes.get("contract"),
                      object_hashes.get("contract")) and
        pinned_member(audit_bundle, "build_only_producer", producer_path,
                      source_hashes.get("producer")) and
        pinned_member(
            audit_bundle, "independent_verifier_assembler_authority_consumer",
            consumer_path, source_hashes.get("consumer")) and
        pinned_member(audit_bundle, "v13_to_v14_transition_receipt",
                      transition_path, file_hashes.get("transition"),
                      object_hashes.get("transition")))
    current_audit_inputs = {
        "schema": file_hashes.get("schema"),
        "contract_file": file_hashes.get("contract"),
        "contract_object": object_hashes.get("contract"),
        "producer": source_hashes.get("producer"),
        "consumer": source_hashes.get("consumer"),
        "transition_file": file_hashes.get("transition"),
        "transition_object": object_hashes.get("transition"),
        "launcher_template": normalized_digest,
    }
    external_tail = external_audit_input_evidence.get("expected_tail")
    external_tail = external_tail if isinstance(external_tail, Mapping) else {}
    expected_audit_inputs = {**current_audit_inputs, **external_tail}
    dual = audit_map.get("dual_independent_static_checkers", {})
    dual = dual if isinstance(dual, dict) else {}
    checker_a = dual.get("checker_A", {})
    checker_b = dual.get("checker_B", {})
    checker_c = dual.get(
        "checker_C_common_census_and_pin_normalized_ast_reproduction", {})
    checker_a = checker_a if isinstance(checker_a, dict) else {}
    checker_b = checker_b if isinstance(checker_b, dict) else {}
    checker_c = checker_c if isinstance(checker_c, dict) else {}
    exact43_inputs = exact43_audit_input_review(dual, expected_audit_inputs)

    def checker_inputs_match(checker: Mapping[str, Any]) -> bool:
        inputs = checker.get("input_sha256")
        return (
            isinstance(inputs, dict) and
            tuple(inputs) == EXPECTED_STATIC_AUDIT_V14_INPUT_ORDER and
            inputs == expected_audit_inputs and
            checker.get("pin_normalized_launcher_ast_sha256") ==
                normalized_digest)

    normalized_claims = {
        "checker_A": checker_a.get("pin_normalized_launcher_ast_sha256"),
        "checker_B": checker_b.get("pin_normalized_launcher_ast_sha256"),
        "checker_C": checker_c.get("pin_normalized_launcher_ast_sha256"),
        "dual_held": dual.get("held_launcher_pin_normalized_ast_sha256"),
    }
    checker_statuses_match = (
        checker_a.get("status") ==
            "GO_STATIC_CHECKER_A__PIN_NORMALIZED_AST_REPRODUCED__"
            "RUNTIME_NOT_AUTHORIZED" and
        checker_b.get("status") ==
            "GO_STATIC_CHECKER_B__PIN_NORMALIZED_AST_REPRODUCED__"
            "RUNTIME_NOT_AUTHORIZED" and
        checker_c.get("status") ==
            "GO_PIN_NORMALIZED_AST_AND_COMMON_DIGEST_REPRODUCED__"
            "RUNTIME_NOT_AUTHORIZED")
    audit_acceptance = audit_map.get("final_audit_acceptance", {})
    audit_acceptance = audit_acceptance if isinstance(
        audit_acceptance, dict) else {}
    audit_review = {
        "schema": audit_map.get("schema"),
        "status": audit_map.get("status"),
        "audit_path": audit_map.get("audit_path"),
        "audited_v14_bundle": audit_bundle,
        "members_match": audit_members_match,
        "expected_current_input_pins": expected_audit_inputs,
        "exact43_A_B_input_review": exact43_inputs,
        "pin_normalized_launcher_reproduction": pin_normalized,
        "declared_pin_normalized_launcher_digests": normalized_claims,
        "checker_A_inputs_match": checker_inputs_match(checker_a),
        "checker_B_inputs_match": checker_inputs_match(checker_b),
        "checker_statuses_match": checker_statuses_match,
        "matches": (
            audit_map.get("schema") ==
                "cm2.round306c79g.true-global-no-producer-consumer."
                "static-audit.v14" and
            audit_map.get("status") ==
                "PASS_DUAL_STATIC_PIN_NORMALIZED_AST_GO_V14__"
                "PHYSICAL_COLD_FREEZE_PENDING__RUNTIME_NOT_AUTHORIZED" and
            audit_map.get("audit_path") == audit_path and
            audit_members_match and pin_normalized.get("matches") is True and
            exact43_inputs.get("matches") is True and
            checker_inputs_match(checker_a) and checker_inputs_match(checker_b) and
            checker_statuses_match and normalized_digest is not None and
            all(value == normalized_digest for value in normalized_claims.values()) and
            dual.get("independent_pin_normalizer_count") == 3 and
            dual.get("all_pin_normalizers_equal") is True and
            dual.get("pin_normalization_forces_final_base7_installed_false")
                is True and
            dual.get("final_launcher_must_reproduce_pin_normalized_ast_after_pin_injection")
                is True and
            audit_acceptance.get("current_draft_pass") is True and
            audit_acceptance.get("final_static_freeze_pass_required") is True and
            audit_acceptance.get("pin_normalized_launcher_ast_digest_consensus")
                is True),
    }

    launcher_tree = source_trees.get("launcher")
    launcher_env = source_envs.get("launcher", {})
    launcher_active = (
        launcher_active_base7_review(launcher_tree, launcher_env)
        if isinstance(launcher_tree, ast.Module) else {
            "base7_key_order": [], "base7_pin_values": {}, "exact8_order": []})
    receipt_closure = receipt_review.get("object_closure", {})
    receipt_object = (
        receipt_closure.get("declared")
        if isinstance(receipt_closure, Mapping) else None)
    expected_launcher_pins = {
        "V13_SUPERSESSION_RECEIPT": (
            receipt_review.get("file_sha256"), receipt_object),
        "SCHEMA": (file_hashes.get("schema"), None),
        "CONTRACT": (
            file_hashes.get("contract"), object_hashes.get("contract")),
        "PRODUCER": (source_hashes.get("producer"), None),
        "CONSUMER": (source_hashes.get("consumer"), None),
        "TRANSITION": (
            file_hashes.get("transition"), object_hashes.get("transition")),
        "AUDIT": (file_hashes.get("audit"), object_hashes.get("audit")),
    }
    expected_launcher_key_order = list(expected_launcher_pins)
    expected_launcher_exact8 = [*expected_launcher_key_order, "SELF"]
    launcher_pin_review = {
        **launcher_active,
        "final_flag": final_flags.get("launcher"),
        "expected_base7_pin_values": expected_launcher_pins,
        "expected_exact8_order": expected_launcher_exact8,
        "matches": (
            final_flags.get("launcher") is True and
            receipt_review.get("matches") is True and
            launcher_active.get("base7_key_order") ==
                expected_launcher_key_order and
            launcher_active.get("base7_pin_values") == expected_launcher_pins and
            launcher_active.get("exact8_order") == expected_launcher_exact8),
    }

    sentinel_values: set[str] = set()
    for role, name in (
            ("producer", "V14_DRAFT_CORE_PIN_SENTINELS"),
            ("consumer", "V14_DRAFT_CURRENT_CORE_PINS")):
        value = source_envs.get(role, {}).get(name)
        if isinstance(value, tuple):
            sentinel_values.update(item for item in value if isinstance(item, str))
    sentinel_values.update(
        item for item in (
            launcher_env.get("_DRAFT_FILE_PIN"),
            launcher_env.get("_DRAFT_OBJECT_PIN")) if isinstance(item, str))
    active_pin_values: list[str] = []
    active_pin_values.extend(
        value for value in producer_observed.values() if isinstance(value, str))
    active_pin_values.extend(
        value for value in consumer_observed.values() if isinstance(value, str))
    for value in launcher_active.get("base7_pin_values", {}).values():
        if isinstance(value, (tuple, list)):
            active_pin_values.extend(item for item in value if isinstance(item, str))
    sentinel_hits = sorted(set(active_pin_values) & sentinel_values)
    active_hashes_valid = all(
        HEX64.fullmatch(value) and value != "0" * 64
        for value in active_pin_values)
    sentinel_review = {
        "declared_sentinel_count": len(sentinel_values),
        "active_pin_value_count": len(active_pin_values),
        "active_sentinel_hits": sentinel_hits,
        "all_active_pin_hashes_nonzero_hex64": active_hashes_valid,
        "matches": not sentinel_hits and active_hashes_valid,
    }

    finals_true = (
        set(final_flags) == set(final_names) and
        all(value is True for value in final_flags.values()))
    final_matches = (
        all_present and strict_json_matches and finals_true and
        contract_review["matches"] and producer_pin_review["matches"] and
        consumer_pin_review["matches"] and transition_review["matches"] and
        audit_review["matches"] and launcher_pin_review["matches"] and
        sentinel_review["matches"])
    lifecycle_matches = draft_matches or final_matches
    state = "draft" if draft_matches else "final" if final_matches else "partial_or_invalid"
    return {
        "state": state,
        "json_presence": dict(json_presence),
        "final_flags": final_flags,
        "strict_json": strict_json_rows,
        "draft_flags_and_absence_match": draft_flags_and_absence_match,
        "sentinel_declarations": sentinel_declarations,
        "draft_active_pin_graph": draft_active_pins,
        "launcher_configured_path_graph": launcher_paths,
        "main_control_flow": main_control_flow,
        "in_memory_negative_tests": in_memory_negative_tests,
        "external_audit_input_evidence": external_audit_input_evidence,
        "contract_schema_paths_and_status": contract_review,
        "producer_current_pin_graph": producer_pin_review,
        "consumer_current_pin_graph": consumer_pin_review,
        "transition_current_pin_graph": transition_review,
        "audit_current_pin_graph": audit_review,
        "launcher_base7_and_exact8_pin_graph": launcher_pin_review,
        "active_sentinel_exclusion": sentinel_review,
        "draft_matches": draft_matches,
        "final_matches": final_matches,
        "lifecycle_matches": lifecycle_matches,
    }


def normalized_historical_witness(value: Any) -> list[dict[str, Any]] | None:
    if not isinstance(value, (tuple, list)):
        return None
    exact_keys = {
        "version", "path", "file_sha256", "object_sha256", "key_count",
        "sorted_keys", "sorted_key_array_sha256", "canonical_object_closed",
    }
    rows: list[dict[str, Any]] = []
    for value_row in value:
        if not isinstance(value_row, dict) or set(value_row) != exact_keys:
            return None
        row = dict(value_row)
        if isinstance(row["sorted_keys"], tuple):
            row["sorted_keys"] = list(row["sorted_keys"])
        rows.append(row)
    return rows


def _module_assignment_node(tree: ast.Module, name: str) -> ast.AST | None:
    nodes = module_assignments(tree).get(name, [])
    return nodes[0] if len(nodes) == 1 else None


def historical_witness_builder_review(
        tree: ast.Module, env: Mapping[str, Any], role: str,
        expected_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    """Rebuild the nine historical rows without invoking source code.

    The source-level witness is deliberately initialized with a function call,
    so it cannot be accepted from ``literal_environment``.  Authority here is
    the literal BASE/STEP graph plus the AST shape of the sole builder.
    """
    base = env.get("HISTORICAL_REJECTION_BASE_EXACT37_KEYS")
    steps = env.get("HISTORICAL_REJECTION_KEYSET_STEPS")
    rows: list[dict[str, Any]] = []
    errors: list[str] = []
    expected_versions = [3, 5, 6, 7, 8, 9, 10, 11, 12]
    expected_counts = [37, 39, 41, 43, 46, 48, 50, 52, 54]
    if not isinstance(base, (set, frozenset)):
        errors.append("BASE_NOT_STATIC_SET")
        keys: set[str] = set()
    else:
        keys = set(base)
        if len(keys) != 37 or not all(isinstance(item, str) for item in keys):
            errors.append("BASE_NOT_EXACT37_STRING_KEYS")
    if not isinstance(steps, tuple) or len(steps) != 9:
        errors.append("STEPS_NOT_EXACT9_STATIC_TUPLE")
        step_values: tuple[Any, ...] = ()
    else:
        step_values = steps
    for index, step in enumerate(step_values):
        if not isinstance(step, tuple) or len(step) != 5:
            errors.append(f"STEP_{index}_NOT_EXACT5")
            continue
        version, additions, file_pin, object_pin, keyset_digest = step
        if version != expected_versions[index]:
            errors.append(f"STEP_{index}_VERSION")
        if not isinstance(additions, (set, frozenset)) or not all(
                isinstance(item, str) for item in additions):
            errors.append(f"STEP_{index}_ADDITIONS")
            additions = frozenset()
        if not (isinstance(file_pin, str) and HEX64.fullmatch(file_pin)):
            errors.append(f"STEP_{index}_FILE_PIN")
        if not (isinstance(object_pin, str) and HEX64.fullmatch(object_pin)):
            errors.append(f"STEP_{index}_OBJECT_PIN")
        if not (isinstance(keyset_digest, str) and HEX64.fullmatch(keyset_digest)):
            errors.append(f"STEP_{index}_KEYSET_DIGEST")
        keys |= set(additions)
        sorted_keys = sorted(keys)
        computed_digest = sha_bytes(canonical(sorted_keys))
        if len(sorted_keys) != expected_counts[index]:
            errors.append(f"STEP_{index}_COUNT")
        if computed_digest != keyset_digest:
            errors.append(f"STEP_{index}_DIGEST")
        version_label = f"v{version}"
        rows.append({
            "version": version_label,
            "path": (
                f".cm2-runtime/c79g-{version_label}-rejections-{CHECKPOINT}/"
                "rejection.json"),
            "file_sha256": file_pin,
            "object_sha256": object_pin,
            "key_count": len(sorted_keys),
            "sorted_keys": sorted_keys,
            "sorted_key_array_sha256": keyset_digest,
            "canonical_object_closed": True,
        })

    definitions = [
        node for node in tree.body
        if isinstance(node, ast.FunctionDef) and
        node.name == "_build_historical_rejection_exact_keyset_witness"]
    structure: dict[str, Any] = {"definition_count": len(definitions)}
    structure_ok = len(definitions) == 1
    if len(definitions) == 1:
        function = definitions[0]
        normalized = ast.dump(
            function, annotate_fields=True,
            include_attributes=False).encode("utf-8")
        for_nodes = [node for node in ast.walk(function) if isinstance(node, ast.For)]
        exact_for = [
            node for node in for_nodes
            if isinstance(node.target, ast.Tuple) and
            [item.id if isinstance(item, ast.Name) else None
             for item in node.target.elts] == [
                 "version", "additions", "file_pin", "object_pin",
                 "keyset_digest"] and
            isinstance(node.iter, ast.Name) and
            node.iter.id == "HISTORICAL_REJECTION_KEYSET_STEPS"]
        union_updates = [
            node for node in ast.walk(function)
            if isinstance(node, ast.Assign) and len(node.targets) == 1 and
            isinstance(node.targets[0], ast.Name) and
            node.targets[0].id == "keys" and
            isinstance(node.value, ast.BinOp) and
            isinstance(node.value.op, ast.BitOr) and
            isinstance(node.value.left, ast.Name) and node.value.left.id == "keys" and
            isinstance(node.value.right, ast.Name) and
            node.value.right.id == "additions"]
        sorted_updates = [
            node for node in ast.walk(function)
            if isinstance(node, ast.Assign) and len(node.targets) == 1 and
            isinstance(node.targets[0], ast.Name) and
            node.targets[0].id == "sorted_keys" and
            isinstance(node.value, ast.Call) and
            isinstance(node.value.func, ast.Name) and
            node.value.func.id == "sorted" and len(node.value.args) == 1 and
            isinstance(node.value.args[0], ast.Name) and
            node.value.args[0].id == "keys"]
        append_dicts = [
            node.args[0] for node in ast.walk(function)
            if isinstance(node, ast.Call) and
            isinstance(node.func, ast.Attribute) and
            isinstance(node.func.value, ast.Name) and
            node.func.value.id == "rows" and node.func.attr == "append" and
            len(node.args) == 1 and isinstance(node.args[0], ast.Dict)]
        expected_row_keys = {
            "version", "path", "file_sha256", "object_sha256", "key_count",
            "sorted_keys", "sorted_key_array_sha256",
            "canonical_object_closed"}
        append_keysets = [
            {key.value for key in node.keys
             if isinstance(key, ast.Constant) and isinstance(key.value, str)}
            for node in append_dicts]
        returns = [node for node in ast.walk(function) if isinstance(node, ast.Return)]
        return_tuple_rows = (
            len(returns) == 1 and isinstance(returns[0].value, ast.Call) and
            isinstance(returns[0].value.func, ast.Name) and
            returns[0].value.func.id == "tuple" and
            len(returns[0].value.args) == 1 and
            isinstance(returns[0].value.args[0], ast.Name) and
            returns[0].value.args[0].id == "rows")
        structure.update({
            "normalized_ast_sha256": sha_bytes(normalized),
            "for_step_loop_count": len(exact_for),
            "key_union_update_count": len(union_updates),
            "sorted_key_update_count": len(sorted_updates),
            "row_append_keysets": [sorted(value) for value in append_keysets],
            "returns_tuple_rows": return_tuple_rows,
        })
        structure_ok &= (
            len(exact_for) == 1 and len(union_updates) == 1 and
            len(sorted_updates) == 1 and append_keysets == [expected_row_keys] and
            return_tuple_rows)
    witness_assignment = _module_assignment_node(
        tree, "HISTORICAL_REJECTION_EXACT_KEYSET_WITNESS")
    assignment_is_builder_call = (
        isinstance(witness_assignment, ast.Call) and
        isinstance(witness_assignment.func, ast.Name) and
        witness_assignment.func.id ==
            "_build_historical_rejection_exact_keyset_witness" and
        not witness_assignment.args and not witness_assignment.keywords)
    materialized_assignment = normalized_historical_witness(
        safe_literal(witness_assignment, env))
    assignment_is_exact_materialization = materialized_assignment == rows
    structure["module_assignment_is_exact_zero_argument_builder_call"] = \
        assignment_is_builder_call
    structure["module_assignment_is_exact_static_materialization"] = \
        assignment_is_exact_materialization
    structure["module_assignment_mode"] = (
        "BUILDER_CALL" if assignment_is_builder_call else
        "STATIC_MATERIALIZATION" if assignment_is_exact_materialization else
        "INVALID")
    structure_ok &= assignment_is_builder_call or assignment_is_exact_materialization
    return {
        "role": role,
        "base_key_count": len(base) if isinstance(base, (set, frozenset)) else None,
        "step_count": len(steps) if isinstance(steps, tuple) else None,
        "reconstructed_rows": rows,
        "errors": errors,
        "builder_structure": structure,
        "matches_external_expected_rows": rows == expected_rows,
        "matches": not errors and structure_ok and rows == expected_rows,
    }


def _statement_successors(tree: ast.Module) -> dict[ast.stmt, ast.stmt]:
    successors: dict[ast.stmt, ast.stmt] = {}
    for owner in ast.walk(tree):
        for _, value in ast.iter_fields(owner):
            if not isinstance(value, list):
                continue
            statements = [item for item in value if isinstance(item, ast.stmt)]
            for left, right in zip(statements, statements[1:]):
                successors[left] = right
    return successors


def _containing_statement(
        node: ast.AST, parents: Mapping[ast.AST, ast.AST],
) -> ast.stmt | None:
    current = node
    while current in parents:
        current = parents[current]
        if isinstance(current, ast.stmt):
            return current
    return None


def published_v11_v12_adjacency_review(
        tree: ast.Module, role: str,
) -> dict[str, Any]:
    """Require every exact v11 proof surface to be immediately extended by v12."""
    v11 = "published_then_officially_rejected_predecessor_v11"
    v12 = "published_then_officially_rejected_predecessor_v12"
    parents = parent_map(tree)
    successors = _statement_successors(tree)
    occurrences = [
        node for node in ast.walk(tree)
        if isinstance(node, ast.Constant) and node.value == v11]
    v12_occurrences = [
        node for node in ast.walk(tree)
        if isinstance(node, ast.Constant) and node.value == v12]
    rows: list[dict[str, Any]] = []
    for occurrence in sorted(occurrences, key=lambda item: (item.lineno, item.col_offset)):
        direct_dict: ast.Dict | None = None
        parent = parents.get(occurrence)
        if isinstance(parent, ast.Dict) and occurrence in parent.keys:
            direct_dict = parent
        passed = False
        context = "statement"
        next_value: str | None = None
        if direct_dict is not None:
            context = "dict-key"
            index = direct_dict.keys.index(occurrence)
            if index + 1 < len(direct_dict.keys):
                next_key = direct_dict.keys[index + 1]
                if isinstance(next_key, ast.Constant) and isinstance(next_key.value, str):
                    next_value = next_key.value
            passed = next_value == v12
        else:
            statement = _containing_statement(occurrence, parents)
            relevant: list[ast.Constant] = []
            if statement is not None:
                relevant = sorted([
                    item for item in ast.walk(statement)
                    if isinstance(item, ast.Constant) and item.value in {v11, v12}
                ], key=lambda item: (item.lineno, item.col_offset))
            try:
                index = relevant.index(occurrence)
            except ValueError:
                index = -1
            if index >= 0 and index + 1 < len(relevant):
                next_value = relevant[index + 1].value
            elif statement is not None and statement in successors:
                following = sorted([
                    item for item in ast.walk(successors[statement])
                    if isinstance(item, ast.Constant) and item.value in {v11, v12}
                ], key=lambda item: (item.lineno, item.col_offset))
                if following:
                    next_value = following[0].value
                    context = "next-statement"
            passed = next_value == v12
        rows.append({
            "role": role, "line": occurrence.lineno, "context": context,
            "next_published_predecessor_key": next_value, "passes": passed,
        })
    return {
        "v11_occurrence_count": len(occurrences),
        "v12_occurrence_count": len(v12_occurrences),
        "occurrence_rows": rows,
        "failed_rows": [row for row in rows if not row["passes"]],
        "matches": bool(occurrences) and bool(v12_occurrences) and
            all(row["passes"] for row in rows),
    }


def _functions_named(tree: ast.Module, name: str) -> list[ast.FunctionDef]:
    return [
        node for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef) and node.name == name]


def _literal_string_keyset(node: ast.AST) -> set[str] | None:
    if not isinstance(node, (ast.Set, ast.Tuple, ast.List)):
        return None
    values: set[str] = set()
    for item in node.elts:
        if not (isinstance(item, ast.Constant) and isinstance(item.value, str)):
            return None
        values.add(item.value)
    return values


def consumer_static_freeze_v12_review(tree: ast.Module) -> dict[str, Any]:
    functions = _functions_named(tree, "static_freeze_proof")
    if len(functions) != 1:
        return {"definition_count": len(functions), "matches": False}
    function = functions[0]
    required_transition_key = \
        "published_then_officially_rejected_predecessor_v12"
    required_v13_key = "rejected_prepublication_v13_supersession_receipt"
    transition_keysets: list[dict[str, Any]] = []
    for node in ast.walk(function):
        keyset = _literal_string_keyset(node)
        if keyset is None or "transition_kind" not in keyset or \
                "successor_v14_static_bundle" not in keyset:
            continue
        transition_keysets.append({
            "line": node.lineno, "key_count": len(keyset),
            "has_v11": "published_then_officially_rejected_predecessor_v11" in keyset,
            "has_v12": required_transition_key in keyset,
            "has_rejected_v13": required_v13_key in keyset,
        })
    desired_kind = (
        "APPEND_ONLY_V13_PREPUBLICATION_PYC_CONTAMINATION_REJECTION_TO_"
        "ZERO_CREDIT_V14_STATIC_SUCCESSOR")
    stale_kind = (
        "APPEND_ONLY_PUBLISHED_THEN_OFFICIALLY_REJECTED_V12_TO_"
        "ZERO_CREDIT_V14_STATIC_SUCCESSOR")
    function_strings = literal_strings(function)  # type: ignore[arg-type]
    exact8_first_expressions: list[str] = []
    for node in ast.walk(function):
        if not isinstance(node, ast.Assign) or not any(
                isinstance(target, ast.Name) and target.id == "exact8_stats"
                for target in node.targets):
            continue
        if isinstance(node.value, (ast.List, ast.Tuple)) and node.value.elts:
            exact8_first_expressions.append(ast.unparse(node.value.elts[0]))
    policy_functions = _functions_named(tree, "_static_policy_guards")
    policy_rows: list[dict[str, Any]] = []
    for policy in policy_functions:
        names = {
            node.id for node in ast.walk(policy) if isinstance(node, ast.Name)}
        policy_rows.append({
            "line": policy.lineno,
            "has_v12_official_rejection": "V12_OFFICIAL_REJECTION" in names,
            "has_v13_supersession_receipt":
                "V13_SUPERSESSION_RECEIPT" in names,
            "has_v13_to_v14_transition": "V13_TO_V14_TRANSITION" in names,
        })
    transition_shape_ok = (
        len(transition_keysets) == 1 and transition_keysets[0]["has_v11"] and
        transition_keysets[0]["has_v12"] and
        transition_keysets[0]["has_rejected_v13"])
    exact8_first_ok = (
        exact8_first_expressions and
        all("V13_SUPERSESSION_RECEIPT" in value and
            "V12_OFFICIAL_REJECTION" not in value
            for value in exact8_first_expressions))
    policy_ok = (
        len(policy_rows) == 1 and
        policy_rows[0]["has_v13_supersession_receipt"] and
        policy_rows[0]["has_v13_to_v14_transition"])
    return {
        "definition_count": 1,
        "transition_top_level_keysets": transition_keysets,
        "desired_transition_kind_present": desired_kind in function_strings,
        "stale_v11_transition_kind_present": stale_kind in function_strings,
        "exact8_first_expressions": exact8_first_expressions,
        "static_policy_guard_rows": policy_rows,
        "matches": (
            transition_shape_ok and desired_kind in function_strings and
            stale_kind not in function_strings and exact8_first_ok and policy_ok),
    }


def _terminal_call_version(node: ast.Call, role: str) -> int | None:
    if role == "consumer" and isinstance(node.func, ast.Name):
        if node.func.id == "terminal_replay_v11_published_exact10":
            return 11
        if node.func.id == "terminal_replay_v12_published_exact10":
            return 12
    if role == "launcher" and isinstance(node.func, ast.Attribute) and \
            node.func.attr == "terminal_replay":
        value = node.func.value
        if (isinstance(value, ast.Attribute) and isinstance(value.value, ast.Name) and
                value.value.id == "self"):
            if value.attr == "predecessor_v11":
                return 11
            if value.attr == "predecessor_v12":
                return 12
    return None


def terminal_replay_v11_then_v12_review(
        trees: Mapping[str, ast.Module],
) -> dict[str, Any]:
    role_rows: dict[str, Any] = {}
    all_pairs_ok = True
    for role in ("consumer", "launcher"):
        tree = trees.get(role)
        if tree is None:
            role_rows[role] = {"source_missing": True, "matches": False}
            all_pairs_ok = False
            continue
        parents = parent_map(tree)
        calls_by_function: dict[ast.FunctionDef, list[tuple[int, ast.Call]]] = {}
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            version = _terminal_call_version(node, role)
            if version is None:
                continue
            current: ast.AST = node
            owner: ast.FunctionDef | None = None
            while current in parents:
                current = parents[current]
                if isinstance(current, ast.FunctionDef):
                    owner = current
                    break
            if owner is not None:
                calls_by_function.setdefault(owner, []).append((version, node))
        pairs: list[dict[str, Any]] = []
        for function, calls in calls_by_function.items():
            ordered = sorted(calls, key=lambda row: (row[1].lineno, row[1].col_offset))
            for index, (version, call) in enumerate(ordered):
                if version != 11:
                    continue
                next_version = ordered[index + 1][0] if index + 1 < len(ordered) else None
                next_line = ordered[index + 1][1].lineno if index + 1 < len(ordered) else None
                row = {
                    "function": function.name, "v11_line": call.lineno,
                    "next_historical_replay_version": next_version,
                    "next_historical_replay_line": next_line,
                    "passes": next_version == 12,
                }
                pairs.append(row)
        v11_count = sum(len([1 for version, _ in calls if version == 11])
                        for calls in calls_by_function.values())
        v12_count = sum(len([1 for version, _ in calls if version == 12])
                        for calls in calls_by_function.values())
        definition_ok = True
        if role == "consumer":
            definition_ok = (
                len(_functions_named(tree, "terminal_replay_v11_published_exact10")) == 1 and
                len(_functions_named(tree, "terminal_replay_v12_published_exact10")) == 1)
        role_ok = bool(pairs) and definition_ok and all(row["passes"] for row in pairs)
        role_rows[role] = {
            "v11_call_count": v11_count, "v12_call_count": v12_count,
            "consumer_both_replay_definitions_exist": definition_ok,
            "pair_rows": pairs, "matches": role_ok,
        }
        all_pairs_ok &= role_ok

    authorize_rows: list[dict[str, Any]] = []
    launcher = trees.get("launcher")
    if launcher is not None:
        launcher_parents = parent_map(launcher)
        for function in _functions_named(launcher, "run_authorize_child"):
            replay_lines: list[int] = []
            for node in ast.walk(function):
                if not (isinstance(node, ast.Call) and
                        isinstance(node.func, ast.Attribute) and
                        isinstance(node.func.value, ast.Name) and
                        node.func.value.id == "bundle" and
                        node.func.attr == "terminal_replay"):
                    continue
                current: ast.AST = node
                nearest: ast.FunctionDef | None = None
                while current in launcher_parents:
                    current = launcher_parents[current]
                    if isinstance(current, ast.FunctionDef):
                        nearest = current
                        break
                if nearest is function:
                    replay_lines.append(node.lineno)
            request_lines = [
                node.lineno for node in ast.walk(function)
                if isinstance(node, ast.Assign) and any(
                    isinstance(target, ast.Name) and target.id == "request"
                    for target in node.targets)]
            authorize_rows.append({
                "function": function.name, "bundle_terminal_replay_lines": replay_lines,
                "live_request_assignment_lines": request_lines,
                "passes": bool(replay_lines) and len(request_lines) == 1 and
                    max(replay_lines) < request_lines[0],
            })
    authorize_ok = len(authorize_rows) == 1 and authorize_rows[0]["passes"]
    return {
        "roles": role_rows,
        "authorize_request_order": authorize_rows,
        "matches": all_pairs_ok and authorize_ok,
    }


def _expression_keyset(
        node: ast.AST, known: Mapping[str, set[str]],
        attribute_known: Mapping[str, set[str]] | None = None,
) -> tuple[set[str], list[str]]:
    attribute_known = attribute_known or {}
    rendered = ast.unparse(node)
    if rendered in attribute_known:
        return set(attribute_known[rendered]), []
    if isinstance(node, ast.Dict):
        keys: set[str] = set()
        unresolved: list[str] = []
        for key, value in zip(node.keys, node.values):
            if key is None:
                unpacked, missing = _expression_keyset(value, known, attribute_known)
                keys |= unpacked
                unresolved.extend(missing)
            elif isinstance(key, ast.Constant) and isinstance(key.value, str):
                keys.add(key.value)
            else:
                unresolved.append("DYNAMIC_KEY:" + ast.unparse(key))
        return keys, unresolved
    if isinstance(node, ast.Name):
        if node.id in known:
            return set(known[node.id]), []
        return set(), ["UNKNOWN_NAME:" + node.id]
    if isinstance(node, ast.Attribute):
        name = ast.unparse(node)
        if name in attribute_known:
            return set(attribute_known[name]), []
        return set(), ["UNKNOWN_ATTRIBUTE:" + name]
    if (isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and
            node.func.id == "dict" and len(node.args) == 1 and not node.keywords):
        return _expression_keyset(node.args[0], known, attribute_known)
    return set(), ["UNSUPPORTED_UNPACK:" + ast.unparse(node)]


def _unwrap_close_object(node: ast.AST) -> tuple[ast.AST, bool]:
    if (isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and
            node.func.id == "close_object" and len(node.args) == 1 and
            not node.keywords):
        return node.args[0], True
    return node, False


def _function_keyset(
        tree: ast.Module, function_name: str, *, target_name: str | None = None,
        attribute_known: Mapping[str, set[str]] | None = None,
) -> dict[str, Any]:
    functions = _functions_named(tree, function_name)
    if len(functions) != 1:
        return {"definition_count": len(functions), "keys": [],
                "unresolved": ["FUNCTION_COUNT"], "closed": False}
    function = functions[0]
    known: dict[str, set[str]] = {}
    assignments: list[tuple[str, ast.AST]] = []
    for node in ast.walk(function):
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and \
                isinstance(node.targets[0], ast.Name):
            assignments.append((node.targets[0].id, node.value))
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            assignments.append((node.target.id, node.value))
    for _ in range(max(2, len(assignments))):
        changed = False
        for name, value in assignments:
            if name in known:
                continue
            rendered = ast.unparse(value)
            if attribute_known and rendered in attribute_known:
                known[name] = set(attribute_known[rendered])
                changed = True
                continue
            if (attribute_known and isinstance(value, ast.Call) and
                    isinstance(value.func, ast.Name) and
                    "CALL:" + value.func.id in attribute_known):
                known[name] = set(attribute_known["CALL:" + value.func.id])
                changed = True
                continue
            body, closed = _unwrap_close_object(value)
            if not isinstance(body, ast.Dict):
                continue
            keys, unresolved = _expression_keyset(body, known, attribute_known)
            if unresolved:
                continue
            if closed:
                keys.add("object_sha256")
            known[name] = keys
            changed = True
        if not changed:
            break

    candidates: list[tuple[int, ast.AST]] = []
    if target_name is not None:
        for node in ast.walk(function):
            if isinstance(node, (ast.Assign, ast.AnnAssign)):
                targets = node.targets if isinstance(node, ast.Assign) else [node.target]
                if any(isinstance(target, ast.Name) and target.id == target_name
                       for target in targets):
                    candidates.append((node.lineno, node.value))
    else:
        candidates = [
            (node.lineno, node.value) for node in ast.walk(function)
            if isinstance(node, ast.Return) and node.value is not None]
    rows: list[dict[str, Any]] = []
    for line, value in candidates:
        body, closed = _unwrap_close_object(value)
        keys, unresolved = _expression_keyset(body, known, attribute_known)
        if closed:
            keys.add("object_sha256")
        rows.append({
            "line": line, "key_count": len(keys), "keys": sorted(keys),
            "unresolved": unresolved, "closed_by_close_object": closed,
        })
    usable = [row for row in rows if not row["unresolved"]]
    selected = max(usable, key=lambda row: row["key_count"], default=None)
    return {
        "definition_count": 1, "candidate_rows": rows,
        "line": selected["line"] if selected else None,
        "key_count": selected["key_count"] if selected else None,
        "keys": selected["keys"] if selected else [],
        "unresolved": selected["unresolved"] if selected else ["NO_USABLE_CANDIDATE"],
        "closed": selected["closed_by_close_object"] if selected else False,
    }


def registry_v12_authority_review(
        trees: Mapping[str, ast.Module],
) -> dict[str, Any]:
    required_registry = {
        "published_then_officially_rejected_predecessor_v12",
        "v12_official_rejection_file_sha256",
        "v12_official_rejection_object_sha256",
        "v12_v5_rejection_shape_incident",
    }
    rows: dict[str, Any] = {}
    producer = trees.get("producer")
    if producer is not None:
        execution_keys = set(_function_keyset(
            producer, "execution_proof").get("keys", []))
        row = _function_keyset(
            producer, "input_registry",
            attribute_known={"self_guard.execution_proof()": execution_keys})
        keys = set(row.get("keys", []))
        row["required_v12_authority_keys"] = sorted(required_registry)
        row["missing_v12_authority_keys"] = sorted(required_registry - keys)
        row["matches"] = not row["missing_v12_authority_keys"]
        rows["producer_input_registry"] = row
    consumer = trees.get("consumer")
    if consumer is not None:
        candidates: list[dict[str, Any]] = []
        for node in ast.walk(consumer):
            keyset = _literal_string_keyset(node)
            if keyset is None or "producer_file_sha256" not in keyset or \
                    "published_then_officially_rejected_predecessor_v11" not in keyset:
                continue
            candidates.append({"line": node.lineno, "keys": sorted(keyset),
                               "key_count": len(keyset)})
        candidate = max(candidates, key=lambda row: row["key_count"], default=None)
        keys = set(candidate["keys"]) if candidate else set()
        rows["consumer_registry_exact_set_gate"] = {
            "candidate_count": len(candidates), "selected": candidate,
            "required_v12_authority_keys": sorted(required_registry),
            "missing_v12_authority_keys": sorted(required_registry - keys),
            "matches": candidate is not None and not (required_registry - keys),
        }
    launcher = trees.get("launcher")
    if launcher is not None:
        chronology = _function_keyset(
            launcher, "cold_publication_chronology").get("keys", [])
        proof = _function_keyset(
            launcher, "cold_root", target_name="proof",
            attribute_known={"bundle.chronology": set(chronology)})
        proof_keys = set(proof.get("keys", []))
        proof["required_v12_authority_keys"] = sorted(required_registry)
        proof["missing_v12_authority_keys"] = sorted(required_registry - proof_keys)
        proof["matches"] = not proof["unresolved"] and not \
            proof["missing_v12_authority_keys"]
        rows["launcher_cold_launch_proof"] = proof
        authority_required = {
            "v12_official_rejection_file_sha256",
            "v12_official_rejection_object_sha256",
            "trusted_v12_v5_rejection_shape_incident_digest",
        }
        authority_candidates: list[dict[str, Any]] = []
        for node in ast.walk(next(iter(_functions_named(launcher, "cold_root")), launcher)):
            if not isinstance(node, ast.Dict):
                continue
            keys, unresolved = _expression_keyset(node, {}, {})
            if "authority_root_sha256" in ast.unparse(
                    parent_map(launcher).get(node, node)) or \
                    "trusted_v11_dual_validator_divergence_incident_digest" in keys:
                authority_candidates.append({
                    "line": node.lineno, "keys": sorted(keys),
                    "unresolved": unresolved, "key_count": len(keys)})
        authority = max(
            authority_candidates, key=lambda row: row["key_count"], default=None)
        authority_keys = set(authority["keys"]) if authority else set()
        rows["launcher_authority_root_domain"] = {
            "candidate_count": len(authority_candidates), "selected": authority,
            "required_v12_authority_keys": sorted(authority_required),
            "missing_v12_authority_keys": sorted(authority_required - authority_keys),
            "matches": authority is not None and not (authority_required - authority_keys),
        }
    return {"roles": rows,
            "matches": len(rows) == 4 and all(row.get("matches") for row in rows.values())}


STATIC_AUDIT_V11_BASE_INPUT_ORDER = (
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
STATIC_AUDIT_V12_INPUT_SUFFIX = (
    "v12_rejection_file", "v12_rejection_object", "v12_producer_file",
    "v12_consumer_file", "v12_launcher_file",
    "trusted_v12_v5_rejection_shape_incident_digest",
)
EXPECTED_STATIC_AUDIT_V14_INPUT_ORDER = (
    *STATIC_AUDIT_V11_BASE_INPUT_ORDER, *STATIC_AUDIT_V12_INPUT_SUFFIX)


def static_audit_input_v12_extension_review(
        source_envs: Mapping[str, Mapping[str, Any]],
        builder_env: Mapping[str, Any],
) -> dict[str, Any]:
    names = {
        "producer": "STATIC_AUDIT_INPUT_KEY_ORDER",
        "consumer": "STATIC_AUDIT_INPUT_EXACT43",
        "launcher": "FINAL_STATIC_AUDIT_INPUT_KEY_ORDER",
        "builder": "STATIC_AUDIT_INPUT_KEY_ORDER",
    }
    environments: dict[str, Mapping[str, Any]] = dict(source_envs)
    environments["builder"] = builder_env
    expected_digest = sha_bytes(canonical(list(EXPECTED_STATIC_AUDIT_V14_INPUT_ORDER)))
    rows: dict[str, Any] = {}
    for role, name in names.items():
        value = environments.get(role, {}).get(name)
        observed = list(value) if isinstance(value, tuple) else None
        digest_names = [
            key for key in environments.get(role, {})
            if "STATIC_AUDIT_INPUT" in key and "SHA256" in key]
        declared_digests = {
            key: environments[role].get(key) for key in digest_names}
        rows[role] = {
            "assignment_name": name,
            "observed_count": len(value) if isinstance(value, tuple) else None,
            "observed_order": observed,
            "observed_suffix": observed[-len(STATIC_AUDIT_V12_INPUT_SUFFIX):]
                if observed is not None and len(observed) >= len(STATIC_AUDIT_V12_INPUT_SUFFIX)
                else None,
            "declared_digest_values": declared_digests,
            "computed_order_sha256": sha_bytes(canonical(observed))
                if observed is not None else None,
            "matches": (
                value == EXPECTED_STATIC_AUDIT_V14_INPUT_ORDER and
                (not declared_digests or
                 set(declared_digests.values()) == {expected_digest})),
        }
    return {
        "expected_count": len(EXPECTED_STATIC_AUDIT_V14_INPUT_ORDER),
        "expected_v12_suffix": list(STATIC_AUDIT_V12_INPUT_SUFFIX),
        "expected_order_sha256": expected_digest,
        "roles": rows,
        "matches": len(rows) == 4 and all(row["matches"] for row in rows.values()),
    }


def history_identity_semantics_review(
        trees: Mapping[str, ast.Module],
        envs: Mapping[str, Mapping[str, Any]],
) -> dict[str, Any]:
    constant_expectations: dict[str, Any] = {
        "V14_PREDECESSOR_UNIQUE_LIVE_IDENTITY_COUNT":
            EXPECTED_PREDECESSOR_IDENTITY_COUNT,
        "V14_PREPUBLICATION_UNIQUE_LIVE_IDENTITY_COUNT":
            EXPECTED_PREPUBLICATION_IDENTITY_COUNT,
        "V14_TERMINAL_UNIQUE_LIVE_IDENTITY_COUNT":
            EXPECTED_TERMINAL_IDENTITY_COUNT,
        "V14_TERMINAL_GROUP_VECTOR": tuple(EXPECTED_RUNTIME_GROUP_VECTOR),
    }
    use_requirements = {
        "producer": (
            ("_validate_v13_supersession_receipt",),
            ("hold_static_freeze_trust",),
        ),
        "consumer": (
            ("__init__", "HeldInheritedIncidentAuthorityExact17"),
            ("read_evidence",),
        ),
    }
    constant_rows: dict[str, Any] = {}
    for role in ("producer", "consumer"):
        tree = trees.get(role)
        env = envs.get(role, {})
        assignments = module_assignments(tree) if tree is not None else {}
        parents = parent_map(tree) if tree is not None else {}
        role_rows: dict[str, Any] = {}
        for name, expected in constant_expectations.items():
            loads = [] if tree is None else [
                node for node in ast.walk(tree)
                if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load) and
                node.id == name]
            load_rows = [
                {"line": node.lineno, "owner_chain": owner_chain(node, parents)}
                for node in loads]
            required_owner_chains = use_requirements[role]
            owner_chain_matches = [
                any(all(owner in row["owner_chain"] for owner in requirement)
                    for row in load_rows)
                for requirement in required_owner_chains]
            role_rows[name] = {
                "assignment_count": len(assignments.get(name, [])),
                "declared_value": env.get(name),
                "expected_value": expected,
                "load_rows": load_rows,
                "required_owner_chains": [list(row)
                                          for row in required_owner_chains],
                "required_owner_chains_present": owner_chain_matches,
                "matches": (
                    len(assignments.get(name, [])) == 1 and
                    env.get(name) == expected and
                    all(owner_chain_matches)),
            }
        constant_rows[role] = {
            "constants": role_rows,
            "matches": all(row["matches"] for row in role_rows.values()),
        }

    def get_key(expression: ast.AST) -> str | None:
        if not (isinstance(expression, ast.Call) and
                isinstance(expression.func, ast.Attribute) and
                expression.func.attr == "get" and expression.args and
                isinstance(expression.args[0], ast.Constant) and
                isinstance(expression.args[0].value, str)):
            return None
        return expression.args[0].value

    receipt_expectations: dict[str, Any] = {
        "v14_predecessor_unique_live_identity_count":
            EXPECTED_PREDECESSOR_IDENTITY_COUNT,
        "v14_prepublication_unique_live_identity_count":
            EXPECTED_PREPUBLICATION_IDENTITY_COUNT,
        "v14_terminal_unique_live_identity_count":
            EXPECTED_TERMINAL_IDENTITY_COUNT,
        "v14_terminal_group_vector": EXPECTED_RUNTIME_GROUP_VECTOR,
    }

    def receipt_comparisons(node: ast.AST) -> dict[str, list[dict[str, Any]]]:
        result: dict[str, list[dict[str, Any]]] = {
            key: [] for key in receipt_expectations}
        for comparison in ast.walk(node):
            if not isinstance(comparison, ast.Compare):
                continue
            parts = [comparison.left, *comparison.comparators]
            for left, right in zip(parts, parts[1:]):
                for keyed, value_expression in ((left, right), (right, left)):
                    key = get_key(keyed)
                    if key not in receipt_expectations:
                        continue
                    value = safe_literal(value_expression, {})
                    if value == receipt_expectations[key]:
                        result[key].append({
                            "line": comparison.lineno,
                            "value_expression": ast.unparse(value_expression),
                        })
        return result

    launcher = trees.get("launcher")
    launcher_row: dict[str, Any] = {"matches": False}
    vector: list[int] = []
    if launcher is not None:
        validator_functions = _functions_named(
            launcher, "validate_v13_supersession_receipt")
        validator_receipt_rows = (
            receipt_comparisons(validator_functions[0])
            if len(validator_functions) == 1 else {})
        validator_receipt_closed = (
            set(validator_receipt_rows) == set(receipt_expectations) and
            all(len(validator_receipt_rows[key]) == 1
                for key in receipt_expectations))

        held_bundle_classes = [
            node for node in ast.walk(launcher)
            if isinstance(node, ast.ClassDef) and node.name == "HeldBundle"]
        initialize_methods = [] if len(held_bundle_classes) != 1 else [
            node for node in held_bundle_classes[0].body
            if isinstance(node, ast.FunctionDef) and node.name == "_initialize"]
        initialize = initialize_methods[0] if len(initialize_methods) == 1 else None
        validator_calls = [] if initialize is None else [
            {"line": node.lineno, "argument_count": len(node.args)}
            for node in ast.walk(initialize)
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and
            node.func.id == "validate_v13_supersession_receipt"]
        initialize_receipt_rows = (
            receipt_comparisons(initialize) if initialize is not None else {})
        initialize_receipt_closed = (
            set(initialize_receipt_rows) == set(receipt_expectations) and
            all(initialize_receipt_rows[key] for key in receipt_expectations))

        terminal115_rows: list[dict[str, Any]] = []
        runtime_vector_rows: list[dict[str, Any]] = []
        if initialize is not None:
            for node in ast.walk(initialize):
                if not isinstance(node, ast.Compare):
                    continue
                argument = is_len_equals(node, EXPECTED_TERMINAL_IDENTITY_COUNT)
                if argument is not None and ast.unparse(argument) == \
                        "all_history_identities":
                    terminal115_rows.append({
                        "line": node.lineno, "expression": ast.unparse(argument)})
                for expression in [node.left, *node.comparators]:
                    value = safe_literal(expression, {})
                    if value == EXPECTED_RUNTIME_GROUP_VECTOR:
                        runtime_vector_rows.append({
                            "line": node.lineno,
                            "expression": ast.unparse(expression),
                            "vector": value,
                        })
        vector = (runtime_vector_rows[0]["vector"]
                  if runtime_vector_rows and
                  all(row["vector"] == EXPECTED_RUNTIME_GROUP_VECTOR
                      for row in runtime_vector_rows) else [])

        cold_root_functions = _functions_named(launcher, "cold_root")
        prepublication113_rows: list[dict[str, Any]] = []
        prepublication_truth_rows: list[dict[str, Any]] = []
        if len(cold_root_functions) == 1:
            for node in ast.walk(cold_root_functions[0]):
                if not isinstance(node, ast.Dict):
                    continue
                for key_node, value_node in zip(node.keys, node.values):
                    key = safe_literal(key_node, {})
                    value = safe_literal(value_node, {})
                    if (key ==
                            "current_v14_and_all_predecessor_unique_file_identity_count" and
                            value == EXPECTED_PREPUBLICATION_IDENTITY_COUNT):
                        prepublication113_rows.append({
                            "line": node.lineno, "value": value})
                    if (key ==
                            "all_current_and_historical_113_identities_globally_unique_on_one_statx_mount" and
                            value is True):
                        prepublication_truth_rows.append({
                            "line": node.lineno, "value": value})

        launcher_row = {
            "receipt_validator_definition_count": len(validator_functions),
            "receipt_validator_exact_constant_rows": validator_receipt_rows,
            "receipt_validator_exact_constants_closed": validator_receipt_closed,
            "held_bundle_definition_count": len(held_bundle_classes),
            "held_bundle_initialize_definition_count": len(initialize_methods),
            "held_bundle_receipt_validator_calls": validator_calls,
            "held_bundle_inline_receipt_constant_rows": initialize_receipt_rows,
            "held_bundle_inline_receipt_constants_closed":
                initialize_receipt_closed,
            "held_bundle_terminal115_rows": terminal115_rows,
            "held_bundle_runtime_group_vector_rows": runtime_vector_rows,
            "cold_root_prepublication113_rows": prepublication113_rows,
            "cold_root_prepublication113_truth_rows": prepublication_truth_rows,
            "matches": (
                validator_receipt_closed and len(validator_calls) == 1 and
                validator_calls[0]["argument_count"] == 2 and
                initialize_receipt_closed and bool(terminal115_rows) and
                bool(runtime_vector_rows) and bool(prepublication113_rows) and
                bool(prepublication_truth_rows)),
        }

    derived = {
        "predecessor_identity_count": sum(vector[1:]) if vector else None,
        "prepublication_identity_count": sum(vector) - 2 if vector else None,
        "terminal_identity_count": sum(vector) if vector else None,
    }
    matches = (
        all(row["matches"] for row in constant_rows.values()) and
        launcher_row["matches"] and vector == EXPECTED_RUNTIME_GROUP_VECTOR and
        derived == {
            "predecessor_identity_count": EXPECTED_PREDECESSOR_IDENTITY_COUNT,
            "prepublication_identity_count": EXPECTED_PREPUBLICATION_IDENTITY_COUNT,
            "terminal_identity_count": EXPECTED_TERMINAL_IDENTITY_COUNT,
        })
    return {
        "producer_consumer_module_constants_and_use_chains": constant_rows,
        "launcher_receipt_validation_and_runtime_census": launcher_row,
        "mechanically_derived_from_runtime_group_vector": derived,
        "matches": matches,
    }


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


def output_shape_constructor_review(
        trees: Mapping[str, ast.Module],
        envs: Mapping[str, Mapping[str, Any]],
) -> dict[str, Any]:
    consumer = trees.get("consumer")
    producer = trees.get("producer")
    launcher = trees.get("launcher")
    constructor_rows: dict[str, Any] = {}
    if consumer is not None:
        consumer_chronology_keys = set(_function_keyset(
            consumer, "cold_publication_chronology").get("keys", []))
        constructor_rows["selfIdentity"] = _function_keyset(
            consumer, "_self_identity")
        constructor_rows["independentConsumerProof"] = _function_keyset(
            consumer, "independent_consumer_proof")
        constructor_rows["staticFreezeProof"] = _function_keyset(
            consumer, "static_freeze_proof",
            attribute_known={
                "CALL:cold_publication_chronology": consumer_chronology_keys})
        constructor_rows["liveACK"] = _function_keyset(
            consumer, "cold_authorize_live_protocol", target_name="ack")
        census_candidates: list[dict[str, Any]] = []
        protocol_functions = _functions_named(consumer, "cold_authorize_live_protocol")
        if len(protocol_functions) == 1:
            for node in ast.walk(protocol_functions[0]):
                if not isinstance(node, ast.Dict):
                    continue
                for key, value in zip(node.keys, node.values):
                    if (isinstance(key, ast.Constant) and
                            key.value == "final_dynamic_replay_census" and
                            isinstance(value, ast.Dict)):
                        keys, unresolved = _expression_keyset(value, {}, {})
                        census_candidates.append({
                            "line": value.lineno, "key_count": len(keys),
                            "keys": sorted(keys), "unresolved": unresolved,
                            "closed_by_close_object": False,
                        })
        census_selected = max(
            [row for row in census_candidates if not row["unresolved"]],
            key=lambda row: row["key_count"], default=None)
        constructor_rows["liveACKCensus"] = {
            "definition_count": len(protocol_functions),
            "candidate_rows": census_candidates,
            "line": census_selected["line"] if census_selected else None,
            "key_count": census_selected["key_count"] if census_selected else None,
            "keys": census_selected["keys"] if census_selected else [],
            "unresolved": census_selected["unresolved"] if census_selected
                else ["NO_USABLE_CANDIDATE"],
            "closed": False,
        }
    if producer is not None:
        execution_keys = set(_function_keyset(
            producer, "execution_proof").get("keys", []))
        constructor_rows["producerSourceRegistry"] = _function_keyset(
            producer, "input_registry",
            attribute_known={"self_guard.execution_proof()": execution_keys})
    if launcher is not None:
        chronology_keys = set(_function_keyset(
            launcher, "cold_publication_chronology").get("keys", []))
        constructor_rows["coldLaunchProof"] = _function_keyset(
            launcher, "cold_root", target_name="proof",
            attribute_known={"bundle.chronology": chronology_keys})
        constructor_rows["laterRejection"] = _function_keyset(
            launcher, "construct_launcher_native_rejection")
        constructor_rows["liveRequest"] = _function_keyset(
            launcher, "run_authorize_child", target_name="request")
    for name, row in constructor_rows.items():
        row["expected_key_count"] = EXPECTED_OUTPUT_SHAPES[name]
        row["matches_expected_key_count"] = (
            not row.get("unresolved") and
            row.get("key_count") == EXPECTED_OUTPUT_SHAPES[name])

    declaration_rows = {
        role: output_shape_values(tree, envs[role])
        for role, tree in trees.items()}
    declarations_ok = (
        len(declaration_rows) == 3 and
        all(rows == [EXPECTED_OUTPUT_SHAPES] for rows in declaration_rows.values()))
    constructors_ok = (
        set(constructor_rows) == set(EXPECTED_OUTPUT_SHAPES) and
        all(row["matches_expected_key_count"] for row in constructor_rows.values()))
    return {
        "expected_shapes": EXPECTED_OUTPUT_SHAPES,
        "constructor_keyset_reconstruction": constructor_rows,
        "three_source_declared_shapes": declaration_rows,
        "declarations_match": declarations_ok,
        "constructors_match": constructors_ok,
        "matches": declarations_ok and constructors_ok,
    }


def v12_incident_semantics(value: Any) -> bool:
    if not isinstance(value, dict):
        return False
    expected_source_files = {
        "v12_producer_source_file_sha256": V12_EXACT10[3][1],
        "v12_consumer_source_file_sha256": V12_EXACT10[4][1],
        "v12_launcher_source_file_sha256": V12_EXACT10[7][1],
        "v12_manifest_file_sha256": V12_EXACT10[8][1],
        "v12_outer_file_sha256": V12_EXACT10[9][1],
        "v12_outer_object_sha256": V12_EXACT10[9][2],
        "v12_official_rejection_file_sha256":
            EXPECTED_V12_REJECTION_FILE_SHA256,
        "v12_official_rejection_object_sha256":
            EXPECTED_V12_REJECTION_OBJECT_SHA256,
        "v5_rejection_exact39_keyset_sha256": EXPECTED_EXACT39_KEYSET_SHA256,
    }
    return (
        all(value.get(key) == expected for key, expected in expected_source_files.items()) and
        value.get("schema") == (
            "cm2.round306c79g.true-global-no-producer-consumer."
            "v12-v5-rejection-shape-incident.v1") and
        value.get("incident_id") == (
            "V12_LAUNCHER_V5_REJECTION_WRONG_EXPECTED_KEY_COUNT_52_FOR_"
            "CANONICAL_EXACT39") and
        value.get("failed_phase") ==
            "LAUNCHER_PRECHILD_HELD_HISTORY_CONSTRUCTOR" and
        value.get("actual_v5_rejection_key_count") == 39 and
        value.get("wrong_v12_launcher_expected_key_count") == 52 and
        value.get("v5_rejection_exact39_sorted_keys") == sorted(EXACT39_KEYS) and
        value.get("producer_v12_validator_uses_exact39_keyset") is True and
        value.get("consumer_v12_validator_uses_exact39_keyset") is True and
        value.get("launcher_v12_validator_used_bare_wrong_length_52") is True and
        value.get("bare_length_only_is_authority") is False and
        value.get("producer_child_spawned") is False and
        value.get("consumer_child_spawned") is False and
        value.get("candidate_write_started") is False and
        value.get("stage_write_started") is False and
        value.get("positive_runtime_surface_count") == 0 and
        value.get("formal_global_closure_credit") == 0 and
        value.get("D02_unlock") is False and
        value.get("D02_gate_credit") == 0 and
        value.get("D02_task_credit") == 0 and
        value.get("D02_formal_pending_task_count") == 33_638 and
        value.get("D02_started") is False)


def review() -> dict[str, Any]:
    report = Report()
    sections: dict[str, Any] = {}
    held: dict[Path, tuple[bytes, tuple[int, ...]]] = {}

    def snapshot(path: Path) -> bytes:
        if path not in held:
            held[path] = read_stable(path)
        return held[path][0]

    source_raw: dict[str, bytes] = {}
    source_trees: dict[str, ast.Module] = {}
    source_envs: dict[str, dict[str, Any]] = {}
    python_section: dict[str, Any] = {}
    total_duplicates = 0
    all_undefined: dict[str, list[str]] = {}
    for role, path in V14_PYTHON.items():
        raw = snapshot(path)
        source_raw[role] = raw
        label = path.name
        try:
            source = raw.decode("utf-8")
            tree = ast.parse(source, filename=label, mode="exec")
            compile(tree, label, "exec", dont_inherit=True)
            stats = dict_literal_stats(tree, label)
            undefined = undefined_globals(source, label)
            source_trees[role] = tree
            source_envs[role] = literal_environment(tree)
            total_duplicates += stats["duplicate_count"]
            all_undefined[role] = undefined
            python_section[role] = {
                "path": str(path.relative_to(ROOT)),
                "file_sha256": sha_bytes(raw),
                "size": len(raw),
                "ast_parse_and_in_memory_compile": True,
                "dict_literals": stats,
                "undefined_globals": undefined,
            }
        except Exception as exc:  # fail closed but retain the other source reports
            all_undefined[role] = [f"STATIC_PARSE_ERROR:{type(exc).__name__}"]
            python_section[role] = {
                "path": str(path.relative_to(ROOT)),
                "file_sha256": sha_bytes(raw),
                "size": len(raw),
                "ast_parse_and_in_memory_compile": False,
                "error": f"{type(exc).__name__}: {exc}",
            }
    sections["python_static"] = python_section
    report.add("three_python_ast_parse_and_in_memory_compile", len(source_trees) == 3)
    report.add("python_literal_dict_duplicate_key_count_zero",
               len(source_trees) == 3 and total_duplicates == 0,
               duplicate_count=total_duplicates)
    report.add("python_undefined_global_count_zero",
               len(source_trees) == 3 and not any(all_undefined.values()),
               undefined_globals=all_undefined)

    target_pyc_initial = target_v14_pyc_paths()
    pyc_directory_row: dict[str, Any]
    try:
        pyc_directory_stat = os.lstat(V14_PYC_DIRECTORY)
        pyc_directory_row = {
            "path": str(V14_PYC_DIRECTORY.relative_to(ROOT)),
            "present": True,
            "is_directory": stat.S_ISDIR(pyc_directory_stat.st_mode),
            "is_symlink": stat.S_ISLNK(pyc_directory_stat.st_mode),
            "mode": oct(stat.S_IMODE(pyc_directory_stat.st_mode)),
            "st_dev": pyc_directory_stat.st_dev,
            "st_ino": pyc_directory_stat.st_ino,
            "st_nlink": pyc_directory_stat.st_nlink,
            "st_mtime_ns": pyc_directory_stat.st_mtime_ns,
            "st_ctime_ns": pyc_directory_stat.st_ctime_ns,
        }
    except FileNotFoundError:
        pyc_directory_row = {
            "path": str(V14_PYC_DIRECTORY.relative_to(ROOT)),
            "present": False,
        }
    target_pyc_rows: list[dict[str, Any]] = []
    for path in target_pyc_initial:
        role = target_v14_pyc_role(path)
        raw = snapshot(path)
        pyc_identity = held[path][1]
        source_path = V14_PYTHON[role] if role is not None else None
        source_identity = held[source_path][1] if source_path in held else None
        header = decode_pyc_header(raw)
        header_timestamp = header.get("source_timestamp_uint32_le")
        header_size = header.get("source_size_uint32_le")
        source_mtime_seconds = (
            source_identity[5] // 1_000_000_000
            if source_identity is not None else None)
        source_size = source_identity[4] if source_identity is not None else None
        target_pyc_rows.append({
            "role": role,
            "path": str(path.relative_to(ROOT)),
            "file_sha256": sha_bytes(raw),
            "stat": {
                "st_dev": pyc_identity[0], "st_ino": pyc_identity[1],
                "mode": oct(stat.S_IMODE(pyc_identity[2])),
                "st_nlink": pyc_identity[3], "st_size": pyc_identity[4],
                "st_mtime_ns": pyc_identity[5], "st_ctime_ns": pyc_identity[6],
            },
            "header": header,
            "source": {
                "path": str(source_path.relative_to(ROOT))
                    if source_path is not None else None,
                "current_file_sha256": sha_bytes(source_raw[role])
                    if role in source_raw else None,
                "current_st_size": source_size,
                "current_st_mtime_ns": source_identity[5]
                    if source_identity is not None else None,
                "current_st_mtime_epoch_seconds": source_mtime_seconds,
                "current_st_ctime_ns": source_identity[6]
                    if source_identity is not None else None,
            },
            "timestamp_header_matches_current_source_mtime_seconds": (
                header_timestamp == source_mtime_seconds
                if header_timestamp is not None and source_mtime_seconds is not None
                else None),
            "timestamp_header_size_matches_current_source_size": (
                header_size == source_size
                if header_size is not None and source_size is not None else None),
        })
    target_pyc_present = bool(target_pyc_rows)
    role_counts = {
        role: sum(row["role"] == role for row in target_pyc_rows)
        for role in V14_PYTHON}
    sections["target_v14_pyc_incident"] = {
        "pyc_or___pycache___created": target_pyc_present,
        "target_pyc_created_or_present": target_pyc_present,
        "target___pycache___directory": pyc_directory_row,
        "target_pyc_count": len(target_pyc_rows),
        "target_pyc_role_counts": role_counts,
        "target_pyc_files": target_pyc_rows,
        "pyc_code_objects_unmarshalled_or_executed": False,
        "files_deleted_moved_or_modified_by_reviewer": False,
    }
    report.add(
        "target_v14_pyc_or___pycache___created_or_present_false",
        not target_pyc_present,
        target_pyc_created_or_present=target_pyc_present,
        target_pyc_count=len(target_pyc_rows),
        target_pyc_paths=[row["path"] for row in target_pyc_rows])

    builder_tree: ast.Module | None = None
    builder_env: dict[str, Any] = {}
    builder_section: dict[str, Any]
    try:
        builder_raw = snapshot(V14_JSON_BUILDER)
        builder_source = builder_raw.decode("utf-8")
        builder_tree = ast.parse(
            builder_source, filename=V14_JSON_BUILDER.name, mode="exec")
        compile(builder_tree, V14_JSON_BUILDER.name, "exec", dont_inherit=True)
        builder_env = literal_environment(builder_tree)
        builder_duplicates = dict_literal_stats(
            builder_tree, V14_JSON_BUILDER.name)
        builder_undefined = undefined_globals(
            builder_source, V14_JSON_BUILDER.name)
        builder_section = {
            "path": str(V14_JSON_BUILDER.relative_to(ROOT)),
            "file_sha256": sha_bytes(builder_raw),
            "ast_parse_and_in_memory_compile": True,
            "dict_literals": builder_duplicates,
            "undefined_globals": builder_undefined,
        }
        builder_static_ok = (
            builder_duplicates["duplicate_count"] == 0 and not builder_undefined)
    except Exception as exc:
        builder_static_ok = False
        builder_section = {"path": str(V14_JSON_BUILDER.relative_to(ROOT)),
                           "error": f"{type(exc).__name__}: {exc}"}
    helper_callsite_contract = v10_helper_callsite_contract_review(
        source_trees, builder_tree)
    builder_static_ok = (
        builder_static_ok and helper_callsite_contract.get("matches") is True)
    sections["json_builder_static"] = builder_section
    sections["v10_helper_exact5_builder_runtime_validator_contract"] = \
        helper_callsite_contract
    report.add("v14_json_builder_ast_compile_duplicates_and_undefined_close",
               builder_static_ok, details=builder_section,
               helper_callsite_exact5_contract=helper_callsite_contract)

    helper_rows = {
        role: incident_helper_review(tree, role)
        for role, tree in source_trees.items()}
    helper_ast_digests = {
        row["normalized_ast_sha256"] for row in helper_rows.values()
        if row["normalized_ast_sha256"] is not None}
    incident_helper_ok = (
        len(helper_rows) == 3 and
        helper_ast_digests == {EXPECTED_V12_INCIDENT_HELPER_AST_SHA256} and
        all(row["matches_expected_callsites"] for row in helper_rows.values()))
    sections["v12_incident_helper_and_callsites"] = {
        "expected_normalized_ast_sha256":
            EXPECTED_V12_INCIDENT_HELPER_AST_SHA256,
        "roles": helper_rows,
    }
    report.add("v12_incident_helper_normalized_ast_and_exact_callsites_close_P_C_L",
               incident_helper_ok)

    incident_values = {
        role: env.get("V12_V5_REJECTION_SHAPE_INCIDENT")
        for role, env in source_envs.items()}
    incident_declared_digests = {
        role: env.get("V12_V5_REJECTION_SHAPE_INCIDENT_SHA256")
        for role, env in source_envs.items()}
    incident_computed_digests = {
        role: sha_bytes(canonical(value)) if isinstance(value, dict) else None
        for role, value in incident_values.items()}
    distinct_incident_objects = {
        canonical(value) for value in incident_values.values()
        if isinstance(value, dict)}
    common_incident_digest = next(iter(incident_computed_digests.values()), None)
    builder_incident_value = builder_env.get("V12_V5_REJECTION_SHAPE_INCIDENT")
    builder_declared_incident_digest = builder_env.get(
        "V12_V5_REJECTION_SHAPE_INCIDENT_SHA256")
    incident_object_ok = (
        len(incident_values) == 3 and len(distinct_incident_objects) == 1 and
        all(v12_incident_semantics(value) for value in incident_values.values()) and
        common_incident_digest is not None and
        set(incident_computed_digests.values()) == {common_incident_digest} and
        set(incident_declared_digests.values()) == {common_incident_digest} and
        builder_declared_incident_digest == common_incident_digest and
        (builder_incident_value is None or
         (isinstance(builder_incident_value, dict) and
          canonical(builder_incident_value) in distinct_incident_objects)))
    sections["v12_incident_object_digest_consensus"] = {
        "source_declared_digests": incident_declared_digests,
        "source_computed_digests": incident_computed_digests,
        "source_object_byte_identity_count": len(distinct_incident_objects),
        "source_semantics_match": {
            role: v12_incident_semantics(value)
            for role, value in incident_values.items()},
        "builder_declared_digest": builder_declared_incident_digest,
        "builder_embeds_incident_object": isinstance(builder_incident_value, dict),
        "builder_object_matches_sources": (
            isinstance(builder_incident_value, dict) and
            canonical(builder_incident_value) in distinct_incident_objects),
    }
    report.add("v12_incident_object_canonical_digest_consensus_P_C_L_builder",
               incident_object_ok)

    try:
        receipt_raw = snapshot(V13_SUPERSESSION_RECEIPT)
        receipt_value, receipt_duplicates = decode_json(
            receipt_raw, str(V13_SUPERSESSION_RECEIPT))
        receipt_review = v13_supersession_receipt_review(
            receipt_raw, receipt_value, receipt_duplicates)
    except Exception as exc:
        receipt_review = {
            "matches": False, "error": f"{type(exc).__name__}: {exc}"}
    exact16_live_rows: list[dict[str, Any]] = []
    exact16_live_ok = True
    for role_name, relative, file_pin in EXPECTED_V13_EXACT16:
        path = ROOT / relative
        try:
            raw = snapshot(path)
            metadata = held[path][1]
            matches = (
                sha_bytes(raw) == file_pin and
                stat.S_IMODE(metadata[2]) == 0o444 and metadata[3] == 1)
            exact16_live_rows.append({
                "role": role_name, "path": relative,
                "file_sha256": sha_bytes(raw), "expected_file_sha256": file_pin,
                "mode": oct(stat.S_IMODE(metadata[2])),
                "nlink": metadata[3], "matches": matches})
            exact16_live_ok &= matches
        except Exception as exc:
            exact16_live_ok = False
            exact16_live_rows.append({
                "role": role_name, "path": relative,
                "matches": False, "error": f"{type(exc).__name__}: {exc}"})
    v13_source_pin_presence: dict[str, Any] = {}
    expected_v13_pins = {
        file_pin for _, _, file_pin in EXPECTED_V13_EXACT16[10:]}
    expected_v13_pins.update({
        EXPECTED_V13_SUPERSESSION_RECEIPT_FILE_SHA256,
        EXPECTED_V13_SUPERSESSION_RECEIPT_OBJECT_SHA256,
        EXPECTED_V13_EXACT16_CANONICAL_SHA256,
        EXPECTED_V13_NORMALIZED_EXACT10_CANONICAL_SHA256,
    })
    for role, tree in source_trees.items():
        available = literal_strings(tree) | {
            value for value in source_envs[role].values()
            if isinstance(value, str)}
        missing = sorted(expected_v13_pins - available)
        v13_source_pin_presence[role] = {
            "missing_pins": missing, "matches": not missing}

    fd_environment_rows = {
        role: incident_fd_environment_review(
            source_trees[role], source_envs[role], role)
        for role in ("producer", "consumer") if role in source_trees}
    incident_fd_environment_ok = (
        set(fd_environment_rows) == {"producer", "consumer"} and
        all(row["matches"] for row in fd_environment_rows.values()) and
        receipt_review.get("matches") is True and exact16_live_ok and
        set(v13_source_pin_presence) == set(V14_PYTHON) and
        all(row["matches"] for row in v13_source_pin_presence.values()))
    sections["v13_receipt_exact17_and_P_C_fd_environment"] = {
        "receipt": receipt_review,
        "exact16_live_files": exact16_live_rows,
        "source_pin_presence": v13_source_pin_presence,
        "producer_consumer_fd_environment": fd_environment_rows,
    }
    report.add("v13_receipt_exact16_and_producer_consumer_exact17_total_fd21_close",
               incident_fd_environment_ok)

    launcher_v12_first = (
        launcher_receipt_first_review(
            source_trees["launcher"], source_envs["launcher"])
        if "launcher" in source_trees else {"matches": False})
    launcher_v12_first_ok = bool(launcher_v12_first.get("matches"))
    sections["launcher_receipt_first_pin_graph"] = launcher_v12_first
    report.add("launcher_pin_normalizer_and_base_objects_are_v13_receipt_first",
               launcher_v12_first_ok)

    flags: dict[str, Any] = {}
    final_names = {
        "producer": "FINAL_V14_CORE_PINS_INSTALLED",
        "consumer": "FINAL_CURRENT_V14_PINS_INSTALLED",
        "launcher": "FINAL_BASE7_PINS_INSTALLED",
    }
    for role in V14_PYTHON:
        env = source_envs.get(role, {})
        flags[role] = {
            "V14_DRAFT_RUNTIME_DISABLED": env.get("V14_DRAFT_RUNTIME_DISABLED"),
            "final_flag_name": final_names[role],
            "final_flag_value": env.get(final_names[role]),
        }
    main_gate_rows = {
        role: draft_final_main_gate_review(source_trees[role], final_names[role])
        for role in source_trees}
    sections["draft_and_final_flags"] = {
        "flags": flags, "main_gate_AST": main_gate_rows}
    report.add("draft_execution_disabled_in_all_three_sources",
               all(row["V14_DRAFT_RUNTIME_DISABLED"] is True
                   for row in flags.values()) and
               set(main_gate_rows) == set(V14_PYTHON) and
               all(row["matches"] for row in main_gate_rows.values()),
               flags=flags, main_gate_AST=main_gate_rows)

    json_initial_presence = {name: path_exists(path) for name, path in V14_JSON.items()}

    expected_pin_rows = [(file_pin, object_pin) for _, file_pin, object_pin in V12_EXACT10]
    exact10_filesystem: list[dict[str, Any]] = []
    exact10_fs_ok = True
    for relative, file_pin, object_pin in V12_EXACT10:
        path = ROOT / relative
        raw = snapshot(path)
        closure: dict[str, Any] | None = None
        if object_pin is not None:
            try:
                value, duplicates = decode_json(raw, str(path))
                closure = object_closure(value)
                closure["duplicate_keys"] = duplicates
                object_ok = (not duplicates and closure["matches"] and
                             closure["declared"] == object_pin)
            except Exception as exc:
                closure = {"matches": False, "error": f"{type(exc).__name__}: {exc}"}
                object_ok = False
        else:
            object_ok = True
        row_ok = sha_bytes(raw) == file_pin and object_ok
        exact10_fs_ok &= row_ok
        exact10_filesystem.append({
            "path": relative, "observed_file_sha256": sha_bytes(raw),
            "expected_file_sha256": file_pin,
            "expected_object_sha256": object_pin,
            "object_closure": closure, "matches": row_ok,
        })
    sections["v12_published_exact10_filesystem"] = exact10_filesystem
    report.add("v12_published_exact10_files_and_objects_match", exact10_fs_ok,
               exact10_count=len(exact10_filesystem))

    v12_rejection_raw = snapshot(V12_REJECTION)
    v12_rejection, v12_duplicates = decode_json(v12_rejection_raw, str(V12_REJECTION))
    v12_closure = object_closure(v12_rejection)
    v12_rejection_ok = (
        isinstance(v12_rejection, dict) and not v12_duplicates and
        sha_bytes(v12_rejection_raw) == EXPECTED_V12_REJECTION_FILE_SHA256 and
        v12_closure["matches"] and
        v12_closure["declared"] == EXPECTED_V12_REJECTION_OBJECT_SHA256 and
        set(v12_rejection) == V12_REJECTION_KEYS)
    sections["v12_official_rejection"] = {
        "path": str(V12_REJECTION.relative_to(ROOT)),
        "file_sha256": sha_bytes(v12_rejection_raw),
        "object_closure": v12_closure,
        "key_count": len(v12_rejection) if isinstance(v12_rejection, dict) else None,
        "keyset_sha256": sha_bytes(canonical(sorted(v12_rejection)))
            if isinstance(v12_rejection, dict) else None,
        "duplicate_keys": v12_duplicates,
    }
    report.add("v12_official_rejection_exact54_file_object_and_keyset_match",
               v12_rejection_ok)

    source_pin_rows: dict[str, Any] = {}
    if len(source_trees) == 3:
        producer_rows = producer_exact10_pins(source_trees["producer"])
        consumer_files = consumer_exact10_files(
            source_trees["consumer"], source_envs["consumer"])
        launcher_rows = launcher_exact10_pins(
            source_trees["launcher"], source_envs["launcher"])
        source_pin_rows = {
            "producer": producer_rows,
            "consumer_file_order": consumer_files,
            "launcher": launcher_rows,
        }
        exact10_source_ok = (
            producer_rows == expected_pin_rows and
            consumer_files == [row[0] for row in expected_pin_rows] and
            launcher_rows == expected_pin_rows)
    else:
        exact10_source_ok = False
    sections["v12_exact10_source_pins"] = source_pin_rows
    report.add("v12_exact10_pins_close_across_producer_consumer_launcher",
               exact10_source_ok)

    rejection_pin_state: dict[str, Any] = {}
    for role, env in source_envs.items():
        file_name = (
            "V12_REJECTION_FILE_PIN" if role == "launcher"
            else "V12_OFFICIAL_REJECTION_FILE_PIN")
        object_name = (
            "V12_REJECTION_OBJECT_PIN" if role == "launcher"
            else "V12_OFFICIAL_REJECTION_OBJECT_PIN")
        strings = literal_strings(source_trees[role])
        rejection_pin_state[role] = {
            "file_pin": env.get(file_name), "object_pin": env.get(object_name),
            "all_exact10_file_pins_present_somewhere": all(
                pin in strings or pin in env.values()
                for _, pin, _ in V12_EXACT10),
            "all_exact10_object_pins_present_somewhere": all(
                object_pin is None or object_pin in strings or object_pin in env.values()
                for _, _, object_pin in V12_EXACT10),
            # The no-producer consumer intentionally carries the ordered ten
            # file pins; producer and launcher carry the canonical object
            # pins used for historical object closure.
            "exact10_object_pin_presence_required_for_role":
                role in {"producer", "launcher"},
        }
    rejection_pin_sources_ok = all(
        row["file_pin"] == EXPECTED_V12_REJECTION_FILE_SHA256 and
        row["object_pin"] == EXPECTED_V12_REJECTION_OBJECT_SHA256 and
        row["all_exact10_file_pins_present_somewhere"] and
        (not row["exact10_object_pin_presence_required_for_role"] or
         row["all_exact10_object_pins_present_somewhere"])
        for row in rejection_pin_state.values())
    sections["v12_rejection_and_exact10_pin_presence"] = rejection_pin_state
    report.add("v12_exact10_plus_official_rejection_pins_present_in_all_three_sources",
               len(rejection_pin_state) == 3 and rejection_pin_sources_ok)

    v5_raw = snapshot(V5_REJECTION)
    v5_value, v5_duplicates = decode_json(v5_raw, str(V5_REJECTION))
    v5_closure = object_closure(v5_value)
    exact39_authority_ok = (
        isinstance(v5_value, dict) and not v5_duplicates and
        sha_bytes(v5_raw) == EXPECTED_V5_REJECTION_FILE_SHA256 and
        v5_closure["matches"] and
        v5_closure["declared"] == EXPECTED_V5_REJECTION_OBJECT_SHA256 and
        set(v5_value) == EXACT39_KEYS and len(EXACT39_KEYS) == 39 and
        sha_bytes(canonical(sorted(EXACT39_KEYS))) == EXPECTED_EXACT39_KEYSET_SHA256)
    exact39_sources: dict[str, Any] = {}
    exact39_source_ok = len(source_trees) == 3
    all_len52: list[dict[str, Any]] = []
    stale_len52: list[dict[str, Any]] = []
    for role, tree in source_trees.items():
        env = source_envs[role]
        gates = exact39_gate_counts(tree)
        all_rows, stale_rows = stale_v5_len52_rows(tree, role)
        all_len52.extend(all_rows)
        stale_len52.extend(stale_rows)
        row = {
            "declared_key_count": len(env.get("V5_OFFICIAL_REJECTION_EXACT39_KEYS", ()))
                if isinstance(env.get("V5_OFFICIAL_REJECTION_EXACT39_KEYS"),
                              (set, frozenset, tuple, list)) else None,
            "declared_keys_match": env.get("V5_OFFICIAL_REJECTION_EXACT39_KEYS") == EXACT39_KEYS,
            "declared_keyset_sha256": env.get(
                "V5_OFFICIAL_REJECTION_EXACT39_KEYSET_SHA256"),
            **gates,
        }
        exact39_sources[role] = row
        exact39_source_ok &= (
            row["declared_keys_match"] and
            row["declared_keyset_sha256"] == EXPECTED_EXACT39_KEYSET_SHA256 and
            row["set_equality_gate_count"] >= 1 and
            row["derived_len39_gate_count"] >= 1)
    sections["v5_exact39_authority"] = {
        "file_sha256": sha_bytes(v5_raw), "object_closure": v5_closure,
        "key_count": len(v5_value) if isinstance(v5_value, dict) else None,
        "keyset_sha256": sha_bytes(canonical(sorted(v5_value)))
            if isinstance(v5_value, dict) else None,
        "source_gates": exact39_sources,
        "all_len52_rows": all_len52,
        "stale_v5_len52_rows": stale_len52,
    }
    report.add("v5_rejection_exact39_external_authority_matches", exact39_authority_ok)
    report.add("v5_exact39_keyset_and_set_equality_gate_close_in_all_three_sources",
               exact39_source_ok)
    report.add("old_v5_len52_magic_number_gate_absent", not stale_len52,
               stale_rows=stale_len52, allowed_non_v5_len52_rows=all_len52)

    historical_actual: dict[str, Any] = {}
    expected_historical_witness: list[dict[str, Any]] = []
    historical_external_ok = True
    for version in HISTORICAL_REJECTION_VERSION_ORDER:
        file_pin, object_pin, key_count, keyset_digest = (
            HISTORICAL_REJECTION_PINS[version])
        path = (RUNTIME / f"c79g-{version}-rejections-{CHECKPOINT}" /
                "rejection.json")
        raw = snapshot(path)
        value, duplicates = decode_json(raw, str(path))
        closure = object_closure(value)
        observed_keys = sorted(value) if isinstance(value, dict) else []
        observed_keyset_digest = sha_bytes(canonical(observed_keys))
        held_identity = held[path][1]
        matches = (
            isinstance(value, dict) and not duplicates and
            sha_bytes(raw) == file_pin and closure["matches"] and
            closure["declared"] == object_pin and len(value) == key_count and
            observed_keyset_digest == keyset_digest and
            raw == canonical(value) + b"\n" and
            stat.S_IMODE(held_identity[2]) == 0o444 and held_identity[3] == 1)
        historical_external_ok &= matches
        relative = str(path.relative_to(ROOT))
        historical_actual[version] = {
            "path": relative, "file_sha256": sha_bytes(raw),
            "object_closure": closure, "key_count": len(observed_keys),
            "sorted_key_array_sha256": observed_keyset_digest,
            "mode": oct(stat.S_IMODE(held_identity[2])),
            "nlink": held_identity[3], "duplicate_keys": duplicates,
            "matches": matches,
        }
        expected_historical_witness.append({
            "version": version, "path": relative,
            "file_sha256": file_pin, "object_sha256": object_pin,
            "key_count": key_count, "sorted_keys": observed_keys,
            "sorted_key_array_sha256": keyset_digest,
            "canonical_object_closed": True,
        })
    historical_witness_reviews = {
        role: historical_witness_builder_review(
            source_trees[role], source_envs[role], role,
            expected_historical_witness)
        for role in source_trees}
    historical_witness_rows = {
        role: row["reconstructed_rows"]
        for role, row in historical_witness_reviews.items()}
    historical_witness_ok = (
        historical_external_ok and len(historical_witness_reviews) == 3 and
        all(row["matches"] for row in historical_witness_reviews.values()))
    sections["historical_rejection_exact_keyset_witness"] = {
        "required_version_order": list(HISTORICAL_REJECTION_VERSION_ORDER),
        "external_rejections": historical_actual,
        "source_witness_rows": historical_witness_rows,
        "source_AST_builder_reviews": historical_witness_reviews,
        "expected_witness_rows": expected_historical_witness,
    }
    report.add("historical_rejection_v3_v5_through_v12_external_keysets_close",
               historical_external_ok)
    report.add("historical_rejection_exact_keyset_witness_closes_in_P_C_L",
               historical_witness_ok)

    published_adjacency = {
        role: published_v11_v12_adjacency_review(tree, role)
        for role, tree in source_trees.items()}
    published_adjacency_ok = (
        len(published_adjacency) == 3 and
        all(row["matches"] for row in published_adjacency.values()))
    sections["published_v11_then_v12_all_surface_adjacency"] = published_adjacency
    report.add(
        "published_then_officially_rejected_predecessor_v12_adjacent_after_every_v11_surface_P_C_L",
        published_adjacency_ok,
        failed_row_count=sum(
            len(row["failed_rows"]) for row in published_adjacency.values()))

    consumer_static_v12 = (
        consumer_static_freeze_v12_review(source_trees["consumer"])
        if "consumer" in source_trees else {"matches": False})
    consumer_static_v12_ok = bool(consumer_static_v12.get("matches"))
    sections["consumer_static_freeze_current_v12_transition"] = consumer_static_v12
    report.add(
        "consumer_static_freeze_preserves_v12_rejection_and_uses_v13_receipt_first",
        consumer_static_v12_ok)

    replay_v12 = terminal_replay_v11_then_v12_review(source_trees)
    replay_v12_ok = bool(replay_v12.get("matches"))
    sections["v11_then_v12_terminal_replay_before_authorize_request"] = replay_v12
    report.add(
        "every_existing_v11_exact10_terminal_replay_is_followed_by_v12_before_authorize_request",
        replay_v12_ok)

    registry_v12 = registry_v12_authority_review(source_trees)
    registry_v12_ok = bool(registry_v12.get("matches"))
    sections["registry_and_cold_authority_v12"] = registry_v12
    report.add(
        "producer_registry_consumer_registry_and_launcher_cold_authority_include_v12_authority",
        registry_v12_ok)

    static_audit_inputs = static_audit_input_v12_extension_review(
        source_envs, builder_env)
    static_audit_validator_exact43 = static_audit_validator_exact43_review(
        source_trees, source_envs)
    static_audit_inputs_ok = (
        static_audit_inputs.get("matches") is True and
        static_audit_validator_exact43.get("matches") is True)
    sections["static_audit_input_v12_extension"] = static_audit_inputs
    sections["static_audit_runtime_validator_exact43"] = \
        static_audit_validator_exact43
    report.add(
        "static_audit_input_order_extends_v11_exact37_with_exact_v12_authority_suffix_P_C_L_builder",
        static_audit_inputs_ok,
        runtime_validator_exact43=static_audit_validator_exact43)

    exact56_digest_ok = (
        len(EXACT56_KEYS) == 56 and
        sha_bytes(canonical(sorted(EXACT56_KEYS))) == EXPECTED_EXACT56_KEYSET_SHA256)
    launcher_constructed_keys: set[str] = set()
    launcher_digest = None
    if "launcher" in source_trees:
        functions = [
            node for node in source_trees["launcher"].body
            if isinstance(node, ast.FunctionDef) and
            node.name == "construct_launcher_native_rejection"]
        if len(functions) == 1:
            launcher_constructed_keys = largest_string_key_dict(functions[0])
        launcher_digest = source_envs["launcher"].get(
            "V14_LATER_REJECTION_EXACT56_KEYSET_SHA256")
    output_shape_review = output_shape_constructor_review(
        source_trees, source_envs)
    output_shapes_ok = bool(output_shape_review.get("matches"))
    shape_rows = output_shape_review["three_source_declared_shapes"]
    shapes_ok = (
        output_shape_review.get("declarations_match") is True and
        output_shape_review.get("constructor_keyset_reconstruction", {}).get(
            "laterRejection", {}).get("matches_expected_key_count") is True)
    # ``construct_launcher_native_rejection`` passes a 55-key body to
    # close_object(); object_sha256 is deterministically appended there.
    launcher_closed_keys = launcher_constructed_keys | {"object_sha256"}
    exact56_source_ok = (
        exact56_digest_ok and launcher_closed_keys == EXACT56_KEYS and
        launcher_digest == EXPECTED_EXACT56_KEYSET_SHA256 and shapes_ok)
    sections["v14_exact56_keyset"] = {
        "expected_key_count": len(EXACT56_KEYS),
        "expected_sorted_key_array_sha256": sha_bytes(canonical(sorted(EXACT56_KEYS))),
        "launcher_declared_digest": launcher_digest,
        "launcher_body_key_count_before_close_object": len(launcher_constructed_keys),
        "launcher_closed_key_count": len(launcher_closed_keys),
        "launcher_closed_keyset_sha256": sha_bytes(
            canonical(sorted(launcher_closed_keys))),
        "missing_launcher_closed_keys": sorted(EXACT56_KEYS - launcher_closed_keys),
        "extra_launcher_closed_keys": sorted(launcher_closed_keys - EXACT56_KEYS),
        "output_shape_rows": shape_rows,
    }
    report.add("v14_launcher_exact56_and_three_source_shape_declarations_match",
               exact56_source_ok)
    sections["output_shape_constructor_reconstruction"] = output_shape_review
    report.add(
        "all_nine_output_shapes_mechanically_recompute_from_AST_constructors",
        output_shapes_ok)

    json_section: dict[str, Any] = {}
    current_json_raw: dict[str, bytes] = {}
    current_json_values: dict[str, Any] = {}
    current_json_duplicates: dict[str, list[str]] = {}
    current_json_closures: dict[str, dict[str, Any] | None] = {}
    json_all_present = all(json_initial_presence.values())
    json_all_close = json_all_present
    schema_exact56 = False
    for name, path in V14_JSON.items():
        if not json_initial_presence[name]:
            json_section[name] = {"present": False}
            continue
        try:
            raw = snapshot(path)
            value, duplicates = decode_json(raw, str(path))
            closure = object_closure(value) if name != "schema" else None
            current_json_raw[name] = raw
            current_json_values[name] = value
            current_json_duplicates[name] = duplicates
            current_json_closures[name] = closure
            row_ok = not duplicates and isinstance(value, dict)
            if name != "schema":
                row_ok &= bool(closure and closure["matches"])
            if name == "schema" and isinstance(value, dict):
                definition = value.get("$defs", {}).get("laterRejection", {})
                schema_keys = set(definition.get("properties", {}))
                required = set(definition.get("required", []))
                schema_exact56 = (
                    definition.get("type") == "object" and
                    definition.get("additionalProperties") is False and
                    schema_keys == required == EXACT56_KEYS)
                row_ok &= schema_exact56
            json_all_close &= row_ok
            json_section[name] = {
                "present": True, "file_sha256": sha_bytes(raw),
                "duplicate_keys": duplicates, "object_closure": closure,
                "matches_current_static_requirements": row_ok,
            }
        except Exception as exc:
            json_all_close = False
            json_section[name] = {"present": True,
                                  "error": f"{type(exc).__name__}: {exc}"}
    frozen_exact10 = {
        role: held[ROOT / V12_EXACT10[index][0]]
        for role, index in {
            "producer": 3, "consumer": 4, "audit": 6, "launcher": 7,
        }.items()
    }
    external_audit_input_evidence = external_frozen_audit_input_evidence_review(
        frozen_exact10,
        v5_raw, v5_value, v5_duplicates, v5_closure,
        v12_rejection_raw, v12_rejection, v12_duplicates, v12_closure,
        incident_values.get("producer"), common_incident_digest)
    sections["external_frozen_exact43_audit_input_evidence"] = \
        external_audit_input_evidence
    sections["v14_json_surfaces"] = json_section
    final_pin_graph = final_pin_graph_review(
        source_raw, source_trees, source_envs, json_initial_presence,
        current_json_raw, current_json_values, current_json_duplicates,
        current_json_closures, receipt_review, external_audit_input_evidence)
    sections["final_pin_graph_review"] = final_pin_graph
    report.add("v14_draft_absent_false_or_final_present_true_lifecycle_flags",
               final_pin_graph["lifecycle_matches"],
               state=final_pin_graph["state"],
               draft_matches=final_pin_graph["draft_matches"],
               final_matches=final_pin_graph["final_matches"])
    json_lifecycle = mutually_exclusive_json_lifecycle_review(
        final_pin_graph["final_flags"], json_initial_presence,
        final_pin_graph["final_matches"])
    json_lifecycle_tests = \
        mutually_exclusive_json_lifecycle_in_memory_tests()
    sections["mutually_exclusive_JSON_lifecycle"] = {
        "current": json_lifecycle,
        "in_memory_tests": json_lifecycle_tests,
    }
    report.add(
        "v14_json_surfaces_match_mutually_exclusive_absent_draft_or_complete_final_lifecycle",
        json_lifecycle["matches"] and json_lifecycle_tests["matches"],
        current=json_lifecycle, in_memory_tests=json_lifecycle_tests)
    report.add("v14_json_surfaces_present_closed_and_schema_laterRejection_exact56",
               json_all_present and json_all_close and schema_exact56,
               presence=json_initial_presence, schema_exact56=schema_exact56)

    history_semantics = history_identity_semantics_review(
        source_trees, source_envs)
    history_semantics_ok = bool(history_semantics.get("matches"))
    sections["history_identity_census"] = {
        "expected_predecessor_unique_identity_count":
            EXPECTED_PREDECESSOR_IDENTITY_COUNT,
        "expected_prepublication_unique_identity_count":
            EXPECTED_PREPUBLICATION_IDENTITY_COUNT,
        "expected_terminal_unique_identity_count": EXPECTED_TERMINAL_IDENTITY_COUNT,
        "expected_runtime_group_vector": EXPECTED_RUNTIME_GROUP_VECTOR,
        **history_semantics,
    }
    report.add(
        "v14_history_identity_semantics_predecessor105_prepublication113_terminal115_vector_close",
        history_semantics_ok)

    runtime_initial = [path for path in v14_runtime_surfaces() if path_exists(path)]
    manifest_outer_initial = {
        "manifest": path_exists(V14_MANIFEST), "outer": path_exists(V14_OUTER)}
    sections["publication_and_runtime_absence"] = {
        "manifest_outer_presence": manifest_outer_initial,
        "runtime_surface_count": len(runtime_initial),
        "runtime_surfaces": [str(path.relative_to(ROOT)) for path in runtime_initial],
    }
    report.add("v14_manifest_and_outer_absent_before_publication",
               not any(manifest_outer_initial.values()),
               presence=manifest_outer_initial)
    report.add("v14_runtime_candidate_verification_completion_authority_rejection_and_stages_absent",
               not runtime_initial,
               present=[str(path.relative_to(ROOT)) for path in runtime_initial])

    finals_true = all(row["final_flag_value"] is True for row in flags.values())
    report.add("v14_final_static_bundle_gate",
               builder_static_ok and incident_helper_ok and incident_object_ok and
               incident_fd_environment_ok and launcher_v12_first_ok and
               historical_external_ok and historical_witness_ok and
               finals_true and json_all_present and json_all_close and
               schema_exact56 and exact10_fs_ok and v12_rejection_ok and
               exact10_source_ok and rejection_pin_sources_ok and
               exact39_authority_ok and exact39_source_ok and not stale_len52 and
               exact56_source_ok and output_shapes_ok and
               published_adjacency_ok and consumer_static_v12_ok and
               replay_v12_ok and registry_v12_ok and static_audit_inputs_ok and
               history_semantics_ok and final_pin_graph["final_matches"] and
               not target_pyc_present and
               not any(manifest_outer_initial.values()) and not runtime_initial,
               final_flags_true=finals_true,
               incident_helper_ok=incident_helper_ok,
               incident_object_ok=incident_object_ok,
               incident_fd_environment_ok=incident_fd_environment_ok,
               launcher_v12_first_ok=launcher_v12_first_ok,
               historical_witness_ok=historical_witness_ok,
               published_adjacency_ok=published_adjacency_ok,
               consumer_static_v12_ok=consumer_static_v12_ok,
               replay_v12_ok=replay_v12_ok,
               registry_v12_ok=registry_v12_ok,
               static_audit_inputs_ok=static_audit_inputs_ok,
               output_shapes_ok=output_shapes_ok,
               history_semantics_ok=history_semantics_ok,
               final_pin_graph_matches=final_pin_graph["final_matches"],
               target_pyc_created_or_present=target_pyc_present,
               json_all_present=json_all_present,
               json_all_close=json_all_close,
               publication_and_runtime_absent=(
                   not any(manifest_outer_initial.values()) and not runtime_initial))

    # Terminal snapshot: reopening is read-only and detects both metadata and
    # byte drift.  No intermediate hash can yield GO if any held source moved.
    changed: list[dict[str, Any]] = []
    for path, (before_raw, before_identity) in sorted(held.items(), key=lambda item: str(item[0])):
        try:
            after_raw, after_identity = read_stable(path)
            if before_identity != after_identity or before_raw != after_raw:
                changed.append({
                    "path": str(path.relative_to(ROOT)),
                    "before_identity": before_identity,
                    "after_identity": after_identity,
                    "before_sha256": sha_bytes(before_raw),
                    "after_sha256": sha_bytes(after_raw),
                })
        except Exception as exc:
            changed.append({"path": str(path.relative_to(ROOT)),
                            "terminal_error": f"{type(exc).__name__}: {exc}"})
    json_terminal_presence = {name: path_exists(path) for name, path in V14_JSON.items()}
    runtime_terminal = [path for path in v14_runtime_surfaces() if path_exists(path)]
    target_pyc_terminal = target_v14_pyc_paths()
    manifest_outer_terminal = {
        "manifest": path_exists(V14_MANIFEST), "outer": path_exists(V14_OUTER)}
    initial_target_pyc_names = {str(path) for path in target_pyc_initial}
    terminal_target_pyc_names = {str(path) for path in target_pyc_terminal}
    target_pyc_set_changed = initial_target_pyc_names != terminal_target_pyc_names
    sections["target_v14_pyc_incident"].update({
        "terminal_target_pyc_count": len(target_pyc_terminal),
        "terminal_target_pyc_paths": [
            str(path.relative_to(ROOT)) for path in target_pyc_terminal],
        "target_pyc_set_changed_during_review": target_pyc_set_changed,
    })
    if target_pyc_set_changed:
        changed.append({
            "surface": "target_v14_pyc_presence",
            "before": sorted(initial_target_pyc_names),
            "after": sorted(terminal_target_pyc_names),
        })
    if json_initial_presence != json_terminal_presence:
        changed.append({"surface": "v14_json_presence",
                        "before": json_initial_presence,
                        "after": json_terminal_presence})
    if manifest_outer_initial != manifest_outer_terminal:
        changed.append({"surface": "v14_manifest_outer_presence",
                        "before": manifest_outer_initial,
                        "after": manifest_outer_terminal})
    if {str(path) for path in runtime_initial} != {str(path) for path in runtime_terminal}:
        changed.append({"surface": "v14_runtime_presence",
                        "before": [str(path) for path in runtime_initial],
                        "after": [str(path) for path in runtime_terminal]})
    sections["terminal_snapshot"] = {
        "held_file_count": len(held), "changed_file_count": len(changed),
        "changed_files_or_surfaces": changed,
    }
    report.add("terminal_snapshot_changed_file_count_zero", not changed,
               changed_file_count=len(changed), changes=changed)
    return report.finish(sections)


def main() -> int:
    try:
        result = review()
    except Exception as exc:
        result = {
            "schema": "cm2.c79g.v14.independent-read-only-static-review.v1",
            "status": "FAIL_CLOSED_STATIC_REVIEW__RUNTIME_NOT_AUTHORIZED",
            "read_only": True,
            "protocol_python_imported_or_executed": False,
            "protocol_or_runtime_files_written": False,
            "fatal_error": f"{type(exc).__name__}: {exc}",
            "failed_check_count": 1,
            "failed_checks": ["review_completed_without_fatal_error"],
        }
    print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2))
    # Keep the JSON report as the source of detail, but make the process
    # status fail closed as well.  Previously a static FAIL report was printed
    # and the interpreter still exited zero, allowing a shell/CI caller to
    # mistake a rejected review for a successful gate.  The separate CI
    # wrapper additionally validates the report with jq -e; this return code
    # preserves the same invariant for direct callers.
    return 0 if result.get("status") == (
        "PASS_STATIC_BYTES__RUNTIME_NOT_AUTHORIZED") else 1


if __name__ == "__main__":
    raise SystemExit(main())
