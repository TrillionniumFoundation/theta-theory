#!/usr/bin/env python3
"""Fail-closed, source-only final-pin installer for the C79g v15 DAG.

This program never imports or executes a v15 protocol source.  Every command
holds the official ``.cm2-runtime`` directory flock through terminal replay and
unlock.  PREFLIGHT modes are read-only.  INSTALL modes are disabled by default
and require either the corresponding one-shot source flag below or a complete
CLI prehash contract.

The non-crash CORE transaction is deliberately ordered producer then consumer.
It is not crash-atomic across the two inodes.  A process-local failure before
the durable commit point restores both held inodes and fsyncs them; a host
crash between the two writes leaves a fail-closed producer-final/consumer-draft
state which a later exact-prehash run may finish.  After both final bytes and
parent directories have been fsynced and terminally replayed, a later stdout or
unlock failure leaves a complete recoverable FINAL core, never a partial one.
No persisted receipt is written: the only receipt is stdout JSON.
"""

from __future__ import annotations

import argparse
import ast
import builtins
import copy
import fcntl
import hashlib
import json
import os
import stat
import symtable
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping


ONE_SHOT_CORE_WRITE_ENABLED = False
ONE_SHOT_LAUNCHER_WRITE_ENABLED = False

# These immutable byte pins make this installer specific to the reviewed v15
# clean-room source generation.  A later source generation needs a new
# installer namespace; it must not silently widen this one.
SCHEMA_FILE_SHA256 = (
    "ab120abd2d77667388c94e5af00637f843e7af1b48adba95306e1a7ea79e73bd")
CONTRACT_FILE_SHA256 = (
    "292ad598033ff2f89c1d6c502e4e6077df9559688a5885088ad107fa45a7dabf")
CONTRACT_OBJECT_SHA256 = (
    "9a2ba48cbcb200ff95bf1ca593cd8030ba6bac2b1b8fdc84301d3eb72605bd0e")
CURRENT_PRODUCER_DRAFT_SHA256 = (
    "52578a35f21675989834d3458afbcfa5ad2e5df289ec52dec48090fd430161ff")
CURRENT_CONSUMER_DRAFT_SHA256 = (
    "132afe73beb5abbbd022321ee3b7bb06ed5a762d2991a404c9d2c26357be0cdc")
CURRENT_LAUNCHER_DRAFT_SHA256 = (
    "e0828da2bea7cc4dce73818c954dc2c93d2c7ed5bf18000b588c5d47e60f5043")
CURRENT_PRODUCER_FINAL_SHA256 = (
    "7b3621bf6579cd9cc9289ed2bda353cbe5f2e32b108ec718bf80a4fd19af125b")
CURRENT_CONSUMER_FINAL_SHA256 = (
    "5f988490d014a1427a773b7c5fda03318ec67ad9716a4a75b4008b007e944541")

V14_INHERITED_AUTHORITY_EXACT12_CANONICAL_SHA256 = (
    "24e5e65f8690ad507f7590fe74b9b29702e978e0a8fb2837977e21e5b48df5cd")
V15_EXPECTED_EXACT12_TERMINAL_REPLAY_AST_SHA256 = (
    "7f5ea7ac3f3f4fa81e49947fd718220b0660b5a02b1269f4c9a0d0a12482af69")
V15_EXPECTED_NEED_AST_SHA256 = {
    "producer": "99e6a9e40c339be77ac5270f4ec7471e1cecf9144a83600106bdd01a50f7b99e",
    "consumer": "01d9df10bef3fcbb124dd2e265e685173ab38efedee7a0a8a7fba37930c831d1",
    "launcher": "99e6a9e40c339be77ac5270f4ec7471e1cecf9144a83600106bdd01a50f7b99e",
}
V15_EXPECTED_RUNTIME_OWNER_AST_SHA256 = {
    "producer": {
        "module.canonical":
            "84624bc091a80868ff92af73f4a5c79f0ec48db530007a2f6455c625818a975e",
        "module.strict_json":
            "cd18a308d38da9644fe5ea25fa81fca5e86395f70c07c474dc91fb68e75046f0",
        "module.terminal_replay_v14_exact10_and_official_rejection":
            "dbc5419a5afec206f495e374aa1f735ff5d81a4225b10e0cc400b4a444c3f6df",
        "module.ensure_launch_configuration":
            "7dd5704be115a6e39e376c141f35c4b1d4194b03b03ce7bf11348e14be38f97b",
        "HeldSelf.__init__":
            "05b8b426ba611112a333b5be890138e4dd9b7cb44a1a1b35c9780a3ca5cd2683",
        "HeldSelf.terminal_replay":
            "4419a2aedb75672a993f5cb43155d357237e33ace8a8e509a46645419f9d1782",
    },
    "consumer": {
        "module.canonical":
            "84624bc091a80868ff92af73f4a5c79f0ec48db530007a2f6455c625818a975e",
        "module.strict_json":
            "82403d3bb73d516043d6b21d95da0fbad59ff580229585fe39b24022edc1bae6",
        "module.terminal_replay_v14_exact10_and_official_rejection":
            "dbc5419a5afec206f495e374aa1f735ff5d81a4225b10e0cc400b4a444c3f6df",
        "module.main":
            "098ad9319c7cefd50d0a985e3974d1bd90cbc51cd38f4e34190c56c499ca2284",
        "HeldInheritedV14AuthorityExact12.__init__":
            "a3ab1415e01a49985fe2094dbadfecb3bfe031fa324f570e6554a36794c42762",
        "HeldInheritedV14AuthorityExact12.terminal_replay":
            "f621ac8001abf146077158488fc1b591d7079db1b9797a879f2b2b3256fa7b2b",
    },
    "launcher": {
        "module.canonical":
            "84624bc091a80868ff92af73f4a5c79f0ec48db530007a2f6455c625818a975e",
        "module.strict_json":
            "4ac3d06e0a2f4f2c7b46a41cae69e8cff017130719c1d9ce5e0bbda2e17b2657",
        "module.terminal_replay_v14_exact10_and_official_rejection":
            "dbc5419a5afec206f495e374aa1f735ff5d81a4225b10e0cc400b4a444c3f6df",
        "module.main":
            "d9a040e4fe431bc9b05542f9a6163db91e5b47b52feeef8bc6f44e4e3ca6c4f5",
        "HeldBundle._hold_v14_inherited_authority_exact12":
            "c433d3f7c8f964f56171dd035a27093af2d8a175fcc2d97bdccc7bea9e77f1d3",
        "HeldBundle.terminal_replay":
            "7ca1602756dc317897dd9abb04fad298424f0557f7c08a91f0ed2485352d45ae",
        "module.child_environment":
            "898f1cc9e566a6a4447653e693bf6c5a060ec78a43a1e5b80ca7d992bf641bbe",
        "module.child_pass_fds":
            "33d705bbbc8255dd4f4faf3d0767258cc723e60882aab56e7620f6238fa139e8",
    },
}

BASE = "cm2_round306c79g_true_global_no_producer_consumer"
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "deliverables"
RUNTIME = ROOT / ".cm2-runtime"

SCHEMA = OUT / f"{BASE}_schema_v15.json"
CONTRACT = OUT / f"{BASE}_contract_v15.json"
PRODUCER = OUT / f"{BASE}_v15.py"
CONSUMER = OUT / (
    f"{BASE}_independent_verifier_assembler_authority_consumer_v15.py")
TRANSITION = OUT / f"{BASE}_v14_to_v15_static_launch_transition_receipt_v1.json"
AUDIT = OUT / f"{BASE}_static_audit_v15.json"
LAUNCHER = OUT / f"{BASE}_cold_launch_v15.py"
MANIFEST = OUT / f"{BASE}_cold_launch_manifest_v15.sha256"
OUTER = OUT / f"{BASE}_cold_launch_outer_receipt_v15.json"
V14_SUPERSESSION_RECEIPT = OUT / (
    f"{BASE}_v14_runtime_registry_shape_drift_rejection_"
    "supersession_receipt_v1.json")

V14_SUPERSESSION_RECEIPT_FILE_SHA256 = (
    "aa4323027e2313f8a2eda0d6ffc039a537afe342d496d1f75cd73fcd47446c01")
V14_SUPERSESSION_RECEIPT_OBJECT_SHA256 = (
    "93689e62ae36f405f045a769f4dc6f6e6fd83a16605d08299d5c3397ad657e2e")

CHECKPOINT = (
    "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab")
V14_REJECTION = (
    RUNTIME / f"c79g-v14-rejections-{CHECKPOINT}" / "rejection.json")
V14_EXACT12_ROWS = (
    ("v13_supersession_receipt",
     f"deliverables/{BASE}_v13_prepublication_pyc_contamination_rejection_"
     "supersession_receipt_v1.json",
     "098296d9807a89f58250f4fd404bdd45b1cf343e3e2e1c7a51a24d67225d016f",
     "3c9c44500465c6b416cc0ee6689ea82cdd9096a79687b94f94c409ca5a78c677"),
    ("closed_schema", f"deliverables/{BASE}_schema_v14.json",
     "3d07ccda67cb71d0e5c64d37c0d8e1fcf425de4fbfefddf03bf43934ffdaaa4d", None),
    ("contract", f"deliverables/{BASE}_contract_v14.json",
     "479a0b3f6b4f0ad7e25d22c9f32eec046758a9a7d40509a6bda200e8e41e0ece",
     "11fd8966ed631f3bcc0eb6b1881f0536c814b7a7c093eca8289680e38a7d7b8b"),
    ("build_only_producer", f"deliverables/{BASE}_v14.py",
     "9fa2f2e20cdf15ed37d7f3ff904197fa7bc46a4eec243cab0ae8fb477e2e1ff0", None),
    ("independent_consumer",
     f"deliverables/{BASE}_independent_verifier_assembler_authority_consumer_v14.py",
     "83c58e792b922ad57a7c031b4aca60fe4d5868679e6f7a70b513e3cc4b7dc24c", None),
    ("v13_to_v14_transition",
     f"deliverables/{BASE}_v13_to_v14_static_launch_transition_receipt_v1.json",
     "e8c810f85b511cbc3637321f872f96c996a854454ab7ae1fbb3f5bdf19d7fd95",
     "78912a8f23f7a2e229795aae0e609ca58232dbe36c52ad50bddad727f259413f"),
    ("static_audit", f"deliverables/{BASE}_static_audit_v14.json",
     "dbf5e6bf0f13524ee847d01482f9ad34f715368deb2df40207bd2eb436f293e9",
     "16a8bc6e274a9e4e5a8fe4b2a39b80136cbbb117bfdf2e0ed89ee90fdc71944a"),
    ("cold_launcher", f"deliverables/{BASE}_cold_launch_v14.py",
     "1236f53865d69d69d27091758a66b21ddc2ea33ed7f422bc8d56adb69a23f5b5", None),
    ("cold_manifest", f"deliverables/{BASE}_cold_launch_manifest_v14.sha256",
     "aae2b3735ca9d5469d4228189ff0127e85aca934c6e56dfa3650a4d4d46a5937", None),
    ("cold_outer", f"deliverables/{BASE}_cold_launch_outer_receipt_v14.json",
     "fa6d10673d96a36aaf0163c44e014162ffb7811b12b1efa9068d78c8aa5b2040",
     "786f9be9142ae0aafd31a6d86b08f815d5d4f7ca09fd67506f499635fdddc256"),
    ("v14_official_rejection", str(V14_REJECTION.relative_to(ROOT)),
     "1cc1b5836457f219ce26aa8e463ebebe8d48a26d2145806d24f7cbfea6c7e567",
     "0856353a2390c46b4f4bdefe9f13f6eb6e0e94aa352174cdc8d2f672ace4a41d"),
    ("v14_registry_shape_drift_supersession_receipt",
     str(V14_SUPERSESSION_RECEIPT.relative_to(ROOT)),
     V14_SUPERSESSION_RECEIPT_FILE_SHA256,
     V14_SUPERSESSION_RECEIPT_OBJECT_SHA256),
)
V14_EXACT12_ROLE_ORDER = tuple(row[0] for row in V14_EXACT12_ROWS)
V14_EXACT12_FD_ENV_ORDER = tuple(
    (role, "CM2_C79G_V15_V14_" + role.upper() + "_FD")
    for role in V14_EXACT12_ROLE_ORDER[:10]) + (
        ("v14_official_rejection",
         "CM2_C79G_V15_V14_OFFICIAL_REJECTION_FD"),
        ("v14_registry_shape_drift_supersession_receipt",
         "CM2_C79G_V15_V14_RUNTIME_REGISTRY_SHAPE_DRIFT_"
         "SUPERSESSION_RECEIPT_FD"),
    )

TRANSACTION_CLAIM_NAME = ".c79g-v15-final-pin-installer.transaction-claim-v1"
TRANSACTION_CLAIM_BYTES = b"C79G_V15_FINAL_PIN_INSTALLER_TRANSACTION_CLAIM_V1\n"

CURRENT_BASE7_KEYS = (
    "SCHEMA", "CONTRACT", "PRODUCER", "CONSUMER", "TRANSITION", "AUDIT")
OBJECT_BASE7_KEYS = frozenset({"CONTRACT", "TRANSITION", "AUDIT"})

CORE_CRASH_BOUNDARY = (
    "NOT_CRASH_ATOMIC_ACROSS_PRODUCER_AND_CONSUMER__PRODUCER_WRITES_FIRST__"
    "A_CRASH_MAY_LEAVE_FINAL_PRODUCER_AND_DRAFT_CONSUMER__THIS_STATE_IS_"
    "FAIL_CLOSED_AND_EXACT_PREHASH_RECOVERABLE")
CORE_COMMIT_POINT = (
    "AFTER_BOTH_SOURCE_FDS_AND_PARENT_DIRECTORIES_ARE_FSYNCED__"
    "BOTH_FINAL_BYTES_TERMINALLY_REPLAYED__STATIC_ABSENCE_REVALIDATED__"
    "A_LATER_STDOUT_OR_UNLOCK_FAILURE_CANNOT_CREATE_A_PARTIAL_CORE_STATE")


class Refuse(RuntimeError):
    pass


def canonical(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"),
        ensure_ascii=False).encode("utf-8")


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def is_sha256(value: Any) -> bool:
    return (isinstance(value, str) and len(value) == 64 and
            all(ch in "0123456789abcdef" for ch in value))


def strict_json(
        raw: bytes, label: str, *, canonical_bytes: bool = False,
) -> dict[str, Any]:
    duplicates: list[str] = []

    def hook(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                duplicates.append(key)
            result[key] = value
        return result

    try:
        value = json.loads(raw, object_pairs_hook=hook)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise Refuse(label + ": strict JSON parse failed") from exc
    if duplicates:
        raise Refuse(label + ": duplicate JSON keys: " + repr(duplicates))
    if not isinstance(value, dict):
        raise Refuse(label + ": top level is not an object")
    if canonical_bytes and raw != canonical(value) + b"\n":
        raise Refuse(label + ": bytes are not canonical object plus newline")
    if not raw.endswith(b"\n"):
        raise Refuse(label + ": JSON bytes lack terminal newline")
    return value


def object_sha256(value: dict[str, Any], label: str) -> str:
    declared = value.get("object_sha256")
    if not is_sha256(declared):
        raise Refuse(label + ": missing/noncanonical object_sha256")
    body = copy.deepcopy(value)
    del body["object_sha256"]
    actual = sha256(canonical(body))
    if actual != declared:
        raise Refuse(label + ": object_sha256 closure mismatch")
    return actual


def fd_mount_id(fd: int) -> int:
    try:
        text = Path(f"/proc/self/fdinfo/{fd}").read_text()
    except OSError as exc:
        raise Refuse("cannot read held-fd mount identity") from exc
    for line in text.splitlines():
        if line.startswith("mnt_id:"):
            try:
                return int(line.split(":", 1)[1].strip())
            except ValueError as exc:
                raise Refuse("invalid held-fd mount identity") from exc
    raise Refuse("held-fd mount identity absent")


def pread_all(fd: int) -> bytes:
    blocks: list[bytes] = []
    offset = 0
    while True:
        block = os.pread(fd, 1 << 20, offset)
        if not block:
            return b"".join(blocks)
        blocks.append(block)
        offset += len(block)


@dataclass
class Held:
    path: Path
    fd: int
    parent_fd: int
    before: os.stat_result
    parent_before: os.stat_result
    mount_id: int
    parent_mount_id: int
    raw: bytes
    writable: bool
    expected_mode: int

    @classmethod
    def open(cls, path: Path, *, writable: bool, expected_mode: int) -> "Held":
        parent_fd = -1
        fd = -1
        try:
            parent_fd = os.open(
                path.parent,
                os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC | os.O_NOFOLLOW)
            flags = os.O_CLOEXEC | os.O_NOFOLLOW | (
                os.O_RDWR if writable else os.O_RDONLY)
            fd = os.open(path.name, flags, dir_fd=parent_fd)
            before = os.fstat(fd)
            parent_before = os.fstat(parent_fd)
            if (not stat.S_ISREG(before.st_mode) or
                    stat.S_IMODE(before.st_mode) != expected_mode or
                    before.st_nlink != 1):
                raise Refuse(
                    f"{path.relative_to(ROOT)}: expected regular "
                    f"{expected_mode:04o}/nlink1")
            if not stat.S_ISDIR(parent_before.st_mode):
                raise Refuse(str(path.parent) + ": held parent is not directory")
            mount_id = fd_mount_id(fd)
            parent_mount_id = fd_mount_id(parent_fd)
            if mount_id != parent_mount_id:
                raise Refuse(str(path) + ": file and parent mount differ")
            raw = pread_all(fd)
            result = cls(
                path, fd, parent_fd, before, parent_before, mount_id,
                parent_mount_id, raw, writable, expected_mode)
            result.revalidate_path_identity()
            return result
        except BaseException:
            if fd >= 0:
                os.close(fd)
            if parent_fd >= 0:
                os.close(parent_fd)
            raise

    def revalidate_path_identity(self) -> None:
        try:
            named_parent = os.stat(self.path.parent, follow_symlinks=False)
            current = os.stat(
                self.path.name, dir_fd=self.parent_fd, follow_symlinks=False)
            held = os.fstat(self.fd)
            parent = os.fstat(self.parent_fd)
        except OSError as exc:
            raise Refuse(str(self.path) + ": held/path identity unavailable") from exc
        if ((current.st_dev, current.st_ino) !=
                (held.st_dev, held.st_ino) or
                (named_parent.st_dev, named_parent.st_ino) !=
                (parent.st_dev, parent.st_ino) or
                (parent.st_dev, parent.st_ino) !=
                (self.parent_before.st_dev, self.parent_before.st_ino) or
                not stat.S_ISDIR(named_parent.st_mode) or
                not stat.S_ISDIR(parent.st_mode) or
                not stat.S_ISREG(current.st_mode) or
                not stat.S_ISREG(held.st_mode) or
                stat.S_IMODE(current.st_mode) != self.expected_mode or
                stat.S_IMODE(held.st_mode) != self.expected_mode or
                current.st_nlink != 1 or held.st_nlink != 1 or
                fd_mount_id(self.fd) != self.mount_id or
                fd_mount_id(self.parent_fd) != self.parent_mount_id):
            raise Refuse(str(self.path) + ": held/path identity drift")

    def terminal_replay(self, expected: bytes | None = None) -> bytes:
        self.revalidate_path_identity()
        raw = pread_all(self.fd)
        if expected is not None and raw != expected:
            raise Refuse(str(self.path) + ": held bytes drift")
        return raw

    def close(self) -> None:
        if self.fd >= 0:
            os.close(self.fd)
            self.fd = -1
        if self.parent_fd >= 0:
            os.close(self.parent_fd)
            self.parent_fd = -1


def close_all(held: Iterable[Held]) -> None:
    for item in reversed(list(held)):
        item.close()


def same_mount(held: Iterable[Held]) -> None:
    values = list(held)
    if not values or len({item.mount_id for item in values}) != 1:
        raise Refuse("all held DAG inputs must share one mount")


def open_v14_exact12() -> tuple[list[Held], dict[str, bytes]]:
    """Hold, pin, object-close, and role-order the frozen v14 exact12."""
    held: list[Held] = []
    raw_by_role: dict[str, bytes] = {}
    try:
        records = []
        identities: set[tuple[int, int]] = set()
        for role, relative, file_pin, object_pin in V14_EXACT12_ROWS:
            item = Held.open(
                ROOT / relative, writable=False, expected_mode=0o444)
            held.append(item)
            identities.add((item.before.st_dev, item.before.st_ino))
            if sha256(item.raw) != file_pin:
                raise Refuse("v14 exact12 file pin mismatch: " + role)
            if object_pin is not None:
                value = strict_json(
                    item.raw, "v14 exact12:" + role,
                    canonical_bytes=False)
                if object_sha256(value, "v14 exact12:" + role) != object_pin:
                    raise Refuse("v14 exact12 object pin mismatch: " + role)
            raw_by_role[role] = item.raw
            records.append({
                "path": relative,
                "file_sha256": file_pin,
                "object_sha256": object_pin,
            })
        if (tuple(raw_by_role) != V14_EXACT12_ROLE_ORDER or
                len(held) != 12 or len(identities) != 12):
            raise Refuse("v14 exact12 role/identity closure mismatch")
        if sha256(canonical(records)) != \
                V14_INHERITED_AUTHORITY_EXACT12_CANONICAL_SHA256:
            raise Refuse("v14 exact12 canonical role/path/pin digest mismatch")
        same_mount(held)
        replay_snapshot(held)
        return held, raw_by_role
    except BaseException:
        close_all(held)
        raise


def owned_function(tree: ast.Module, owner: str) -> ast.AST:
    owner_name, function_name = owner.split(".", 1)
    body: list[ast.stmt] = tree.body
    if owner_name != "module":
        classes = [node for node in tree.body
                   if isinstance(node, ast.ClassDef) and
                   node.name == owner_name]
        if len(classes) != 1:
            raise Refuse(owner + ": unique class owner absent")
        body = classes[0].body
    rows = [node for node in body
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and
            node.name == function_name]
    if len(rows) != 1:
        raise Refuse(owner + ": unique function owner absent")
    return rows[0]


def owned_function_sha256(tree: ast.Module, owner: str) -> str:
    return sha256(ast.dump(
        owned_function(tree, owner), annotate_fields=True,
        include_attributes=False).encode("utf-8"))


def exact_literal(tree: ast.Module, name: str) -> Any:
    node = assignment_value(module_assignment(tree, name))
    try:
        return ast.literal_eval(node)
    except Exception as exc:
        raise Refuse(name + ": exact literal required") from exc


def validate_exact12_16_source_wiring(
        raw_by_role: Mapping[str, bytes]) -> dict[str, Any]:
    """Pin the live exact12 authority consumers and launcher exact16 path.

    Whole-source pre/final hashes already exclude decoy edits.  These owner
    hashes additionally make the descriptor dataflow an explicit installer
    gate and a stable audit surface.
    """
    if tuple(raw_by_role) != ("producer", "consumer", "launcher"):
        raise Refuse("source wiring role order mismatch")
    trees = {
        role: source_tree(raw, "v15 wiring:" + role)
        for role, raw in raw_by_role.items()
    }
    observed: dict[str, dict[str, str]] = {}
    for role, expected in V15_EXPECTED_RUNTIME_OWNER_AST_SHA256.items():
        observed[role] = {
            owner: owned_function_sha256(trees[role], owner)
            for owner in expected}
        if observed[role] != expected:
            raise Refuse(role + ": exact12/16 runtime owner AST pin mismatch")
        if owned_function_sha256(trees[role], "module.need") != \
                V15_EXPECTED_NEED_AST_SHA256[role]:
            raise Refuse(role + ": need AST pin mismatch")
        if owned_function_sha256(
                trees[role],
                "module.terminal_replay_v14_inherited_authority_exact12") != \
                V15_EXPECTED_EXACT12_TERMINAL_REPLAY_AST_SHA256:
            raise Refuse(role + ": exact12 terminal replay AST pin mismatch")
        if exact_literal(
                trees[role], "V15_CHILD_AUTHORITY_DESCRIPTOR_COUNT") != 12:
            raise Refuse(role + ": exact12 authority count mismatch")
        for name, expected_pin in (
                ("V14_RUNTIME_REGISTRY_SHAPE_DRIFT_"
                 "SUPERSESSION_RECEIPT_FILE_PIN",
                 V14_SUPERSESSION_RECEIPT_FILE_SHA256),
                ("V14_RUNTIME_REGISTRY_SHAPE_DRIFT_"
                 "SUPERSESSION_RECEIPT_OBJECT_PIN",
                 V14_SUPERSESSION_RECEIPT_OBJECT_SHA256)):
            if exact_literal(trees[role], name) != expected_pin:
                raise Refuse(role + ": v14 receipt literal pin mismatch")

    launcher = trees["launcher"]
    if (exact_literal(launcher, "V15_BOOTSTRAP_DESCRIPTOR_COUNT") != 4 or
            exact_literal(launcher, "V15_CHILD_PASS_FD_COUNT") != 16):
        raise Refuse("launcher exact4+exact12=exact16 constants mismatch")
    launcher_strings = {
        node.value for node in ast.walk(launcher)
        if isinstance(node, ast.Constant) and isinstance(node.value, str)}
    # The first ten names are intentionally generated from the reviewed role
    # order inside the pinned owner AST.  The two appended names are literals.
    missing_env = sorted(
        env for _, env in V14_EXACT12_FD_ENV_ORDER[10:]
        if env not in launcher_strings)
    if missing_env:
        raise Refuse("launcher exact12 FD environments missing: " + repr(missing_env))
    return {
        "v14_exact12_authority_count": 12,
        "launcher_bootstrap_descriptor_count": 4,
        "launcher_child_pass_fd_count": 16,
        "runtime_owner_ast_sha256": observed,
        "terminal_exact12_ast_sha256":
            V15_EXPECTED_EXACT12_TERMINAL_REPLAY_AST_SHA256,
        "matches": True,
    }


def path_lexists(path: Path) -> bool:
    try:
        os.lstat(path)
        return True
    except FileNotFoundError:
        return False
    except OSError as exc:
        raise Refuse(str(path) + ": cannot establish path absence") from exc


def require_absent(path: Path, label: str) -> None:
    if path_lexists(path):
        raise Refuse(label + " already present (including symlink)")


@dataclass
class OfficialWriterLock:
    fd: int
    before: os.stat_result
    mount_id: int
    owned: bool = False
    claim_fd: int = -1
    claim_before: os.stat_result | None = None
    claim_owned: bool = False

    @classmethod
    def acquire(
            cls, *, transaction_claim: bool,
    ) -> "OfficialWriterLock":
        try:
            named = os.lstat(RUNTIME)
        except OSError as exc:
            raise Refuse("official runtime directory unavailable") from exc
        if not stat.S_ISDIR(named.st_mode) or stat.S_ISLNK(named.st_mode):
            raise Refuse("official runtime path is not a no-follow directory")
        fd = -1
        try:
            fd = os.open(
                RUNTIME,
                os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC | os.O_NOFOLLOW)
            before = os.fstat(fd)
            if ((named.st_dev, named.st_ino) != (before.st_dev, before.st_ino) or
                    not stat.S_ISDIR(before.st_mode)):
                raise Refuse("official runtime held/path identity mismatch")
            result = cls(fd=fd, before=before, mount_id=fd_mount_id(fd))
            fcntl.flock(fd, fcntl.LOCK_EX)
            result.owned = True
            result.revalidate_runtime()
            if transaction_claim:
                result.acquire_claim()
            result.revalidate()
            return result
        except BaseException:
            if "result" in locals():
                try:
                    result.remove_owned_claim(refuse_on_drift=False)
                except BaseException:
                    pass
                if result.claim_fd >= 0:
                    os.close(result.claim_fd)
                    result.claim_fd = -1
                if result.owned and fd >= 0:
                    try:
                        fcntl.flock(fd, fcntl.LOCK_UN)
                    except OSError:
                        pass
            if fd >= 0:
                os.close(fd)
            raise

    def revalidate_runtime(self) -> None:
        if not self.owned or self.fd < 0:
            raise Refuse("official writer lock is not owned")
        try:
            named = os.lstat(RUNTIME)
            held = os.fstat(self.fd)
        except OSError as exc:
            raise Refuse("official runtime lock identity unavailable") from exc
        if ((named.st_dev, named.st_ino) != (held.st_dev, held.st_ino) or
                (held.st_dev, held.st_ino) !=
                (self.before.st_dev, self.before.st_ino) or
                not stat.S_ISDIR(named.st_mode) or
                not stat.S_ISDIR(held.st_mode) or
                fd_mount_id(self.fd) != self.mount_id):
            raise Refuse("official runtime lock held/path identity drift")

    def acquire_claim(self) -> None:
        if self.claim_fd >= 0 or self.claim_owned:
            raise Refuse("transaction claim already acquired")
        flags = (os.O_RDWR | os.O_CREAT | os.O_EXCL | os.O_CLOEXEC |
                 os.O_NOFOLLOW)
        try:
            self.claim_fd = os.open(
                TRANSACTION_CLAIM_NAME, flags, 0o600, dir_fd=self.fd)
            self.claim_owned = True
            # O_EXCL ownership begins at open success, before any fstat or
            # content initialization which may itself be interrupted.
            self.claim_before = os.fstat(self.claim_fd)
            if (not stat.S_ISREG(self.claim_before.st_mode) or
                    stat.S_IMODE(self.claim_before.st_mode) != 0o600 or
                    self.claim_before.st_nlink != 1 or
                    fd_mount_id(self.claim_fd) != self.mount_id):
                raise Refuse("O_EXCL transaction claim inode invalid")
            offset = 0
            while offset < len(TRANSACTION_CLAIM_BYTES):
                written = os.pwrite(
                    self.claim_fd, TRANSACTION_CLAIM_BYTES[offset:], offset)
                if written <= 0:
                    raise OSError("transaction claim short/zero pwrite")
                offset += written
            os.ftruncate(self.claim_fd, len(TRANSACTION_CLAIM_BYTES))
            os.fsync(self.claim_fd)
            os.fsync(self.fd)
        except BaseException:
            self.remove_owned_claim(refuse_on_drift=False)
            if self.claim_fd >= 0:
                os.close(self.claim_fd)
                self.claim_fd = -1
            raise

    def revalidate_claim(self) -> None:
        if (not self.claim_owned or self.claim_fd < 0 or
                self.claim_before is None):
            raise Refuse("O_EXCL transaction claim is not owned")
        try:
            named = os.stat(
                TRANSACTION_CLAIM_NAME, dir_fd=self.fd,
                follow_symlinks=False)
            held = os.fstat(self.claim_fd)
        except OSError as exc:
            raise Refuse("transaction claim identity unavailable") from exc
        if ((named.st_dev, named.st_ino) != (held.st_dev, held.st_ino) or
                (held.st_dev, held.st_ino) !=
                (self.claim_before.st_dev, self.claim_before.st_ino) or
                not stat.S_ISREG(named.st_mode) or
                not stat.S_ISREG(held.st_mode) or
                stat.S_IMODE(named.st_mode) != 0o600 or
                stat.S_IMODE(held.st_mode) != 0o600 or
                named.st_nlink != 1 or held.st_nlink != 1 or
                pread_all(self.claim_fd) != TRANSACTION_CLAIM_BYTES or
                fd_mount_id(self.claim_fd) != self.mount_id):
            raise Refuse("O_EXCL transaction claim held/path/byte drift")

    def revalidate(self) -> None:
        self.revalidate_runtime()
        if self.claim_owned:
            self.revalidate_claim()

    def remove_owned_claim(self, *, refuse_on_drift: bool) -> None:
        # A BaseException may arrive after O_EXCL returned and claim_fd was
        # stored but before claim_owned was set.  A held descriptor is enough
        # to perform the same fresh held/named inode-identity cleanup.
        if not self.claim_owned and self.claim_fd < 0:
            return
        removable = False
        unlinked = False
        try:
            if self.claim_fd < 0:
                raise Refuse("owned transaction claim descriptor absent")
            named = os.stat(
                TRANSACTION_CLAIM_NAME, dir_fd=self.fd,
                follow_symlinks=False)
            held = os.fstat(self.claim_fd)
            removable = (named.st_dev, named.st_ino) == (
                held.st_dev, held.st_ino)
            if self.claim_before is not None:
                removable = removable and (
                    (held.st_dev, held.st_ino) ==
                    (self.claim_before.st_dev, self.claim_before.st_ino))
            if not removable:
                raise Refuse(
                    "transaction claim path no longer names owned inode")
            os.unlink(TRANSACTION_CLAIM_NAME, dir_fd=self.fd)
            unlinked = True
            self.claim_owned = False
            os.fsync(self.fd)
        except FileNotFoundError as exc:
            if refuse_on_drift:
                raise Refuse("owned transaction claim path disappeared") from exc
        except BaseException:
            if refuse_on_drift:
                raise
        finally:
            # Never unlink an unrecognized inode.  Closing our descriptor is
            # always safe; a foreign replacement remains fail-closed in place.
            if not self.claim_owned and self.claim_fd >= 0:
                os.close(self.claim_fd)
                self.claim_fd = -1
            if unlinked:
                self.claim_owned = False

    def release(self) -> None:
        if self.fd < 0:
            return
        primary_error: BaseException | None = None
        cleanup_error: BaseException | None = None
        try:
            if self.owned:
                try:
                    self.revalidate()
                except BaseException as exc:
                    primary_error = exc
                if self.claim_owned:
                    try:
                        # Removal is identity-only: byte/mode drift in our
                        # still-named inode must not strand the O_EXCL claim.
                        self.remove_owned_claim(refuse_on_drift=True)
                    except BaseException as exc:
                        cleanup_error = exc
                try:
                    self.revalidate_runtime()
                except BaseException as exc:
                    if primary_error is None:
                        primary_error = exc
                try:
                    fcntl.flock(self.fd, fcntl.LOCK_UN)
                except BaseException as exc:
                    if primary_error is None:
                        primary_error = exc
                else:
                    self.owned = False
        finally:
            if self.claim_fd >= 0:
                os.close(self.claim_fd)
                self.claim_fd = -1
            os.close(self.fd)
            self.fd = -1
        if cleanup_error is not None:
            raise cleanup_error
        if primary_error is not None:
            raise primary_error


def find_v15_pyc() -> list[str]:
    rows: list[str] = []
    for base in (OUT, ROOT / "scripts"):
        if base.is_dir():
            rows.extend(str(path.relative_to(ROOT)) for path in base.rglob("*.pyc")
                        if "v15" in path.name)
    return sorted(rows)


def runtime_surfaces(
        *, allowed_claim: OfficialWriterLock | None = None,
) -> list[str]:
    if not RUNTIME.is_dir():
        return []
    allowed: Path | None = None
    if allowed_claim is not None:
        allowed_claim.revalidate_claim()
        allowed = RUNTIME / TRANSACTION_CLAIM_NAME
    return sorted(
        str(path.relative_to(ROOT)) for path in RUNTIME.rglob("*")
        if "c79g-v15" in path.name.lower() and path != allowed)


def require_static_absence(
        *, allowed_claim: OfficialWriterLock | None = None,
) -> None:
    pycs = find_v15_pyc()
    if pycs:
        raise Refuse("v15 pyc present: " + repr(pycs))
    surfaces = runtime_surfaces(allowed_claim=allowed_claim)
    if surfaces:
        raise Refuse("v15 runtime surface present: " + repr(surfaces))
    require_absent(MANIFEST, "v15 manifest")
    require_absent(OUTER, "v15 outer receipt")


def require_core_phase_absence() -> None:
    require_absent(TRANSITION, "v15 transition")
    require_absent(AUDIT, "v15 audit")


def replay_snapshot(
        held: Iterable[Held],
        replacements: dict[Path, bytes] | None = None,
) -> None:
    replacements = replacements or {}
    for item in held:
        item.terminal_replay(replacements.get(item.path, item.raw))


def iter_symbol_tables(table: symtable.SymbolTable) -> Iterable[symtable.SymbolTable]:
    yield table
    for child in table.get_children():
        yield from iter_symbol_tables(child)


def python_static(raw: bytes, label: str) -> dict[str, Any]:
    try:
        source = raw.decode("utf-8")
        tree = ast.parse(source, filename=label)
        compile(tree, label, "exec")
    except (UnicodeDecodeError, SyntaxError) as exc:
        raise Refuse(label + ": AST parse/in-memory compile failed") from exc

    duplicates: list[dict[str, Any]] = []
    dict_count = 0
    for node in ast.walk(tree):
        if not isinstance(node, ast.Dict):
            continue
        dict_count += 1
        seen: dict[tuple[str, str], int] = {}
        for key in node.keys:
            if key is None:
                continue
            try:
                value = ast.literal_eval(key)
            except Exception:
                continue
            token = (type(value).__name__, repr(value))
            if token in seen:
                duplicates.append({
                    "dict_line": node.lineno, "key": repr(value),
                    "first_line": seen[token], "duplicate_line": key.lineno})
            else:
                seen[token] = key.lineno
    if duplicates:
        raise Refuse(label + ": duplicate Python literal dict keys")

    table = symtable.symtable(source, label, "exec")
    module_defined = {
        symbol.get_name() for symbol in table.get_symbols()
        if (symbol.is_assigned() or symbol.is_imported() or
            symbol.is_namespace() or symbol.is_parameter())}
    allowed = module_defined | set(dir(builtins)) | {
        "__file__", "__name__", "__package__", "__spec__", "__loader__",
        "__cached__", "__builtins__", "__doc__", "__annotations__"}
    undefined = sorted({
        symbol.get_name()
        for child in iter_symbol_tables(table)
        for symbol in child.get_symbols()
        if (symbol.is_referenced() and symbol.is_global() and
            symbol.get_name() not in allowed)})
    if undefined:
        raise Refuse(label + ": undefined globals: " + repr(undefined))
    return {"dict_literal_count": dict_count, "duplicate_key_count": 0,
            "undefined_global_count": 0}


def module_assignment(tree: ast.Module, name: str) -> ast.Assign | ast.AnnAssign:
    rows: list[ast.Assign | ast.AnnAssign] = []
    for node in tree.body:
        if (isinstance(node, ast.Assign) and len(node.targets) == 1 and
                isinstance(node.targets[0], ast.Name) and
                node.targets[0].id == name):
            rows.append(node)
        elif (isinstance(node, ast.AnnAssign) and
              isinstance(node.target, ast.Name) and node.target.id == name):
            rows.append(node)
    if len(rows) != 1:
        raise Refuse(f"expected one module assignment for {name}")
    return rows[0]


def assignment_value(node: ast.Assign | ast.AnnAssign) -> ast.expr:
    if node.value is None:
        raise Refuse("assignment has no value")
    return node.value


def small_eval(node: ast.AST, names: dict[str, Any] | None = None) -> Any:
    names = names or {}
    if isinstance(node, ast.Constant):
        return node.value
    if isinstance(node, ast.Name) and node.id in names:
        return names[node.id]
    if isinstance(node, ast.Tuple):
        return tuple(small_eval(item, names) for item in node.elts)
    if isinstance(node, ast.List):
        return [small_eval(item, names) for item in node.elts]
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Mult):
        return small_eval(node.left, names) * small_eval(node.right, names)
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
        return small_eval(node.left, names) + small_eval(node.right, names)
    raise Refuse("unsupported static expression: " + ast.dump(node))


def is_exact_repeat(node: ast.AST, unit: str, count: int) -> bool:
    return (isinstance(node, ast.BinOp) and isinstance(node.op, ast.Mult) and
            isinstance(node.left, ast.Constant) and node.left.value == unit and
            isinstance(node.right, ast.Constant) and node.right.value == count)


def require_exact_constant_tuple(
        node: ast.AST, expected: tuple[str, ...], label: str,
) -> None:
    if (not isinstance(node, ast.Tuple) or len(node.elts) != len(expected) or
            any(not isinstance(item, ast.Constant) or item.value != value
                for item, value in zip(node.elts, expected))):
        raise Refuse(label + ": forbidden sentinel literal tuple changed")


def source_tree(raw: bytes, label: str) -> ast.Module:
    python_static(raw, label)
    return ast.parse(raw.decode("utf-8"), filename=label)


def span(raw: bytes, node: ast.AST) -> tuple[int, int]:
    if not all(hasattr(node, attr) for attr in
               ("lineno", "col_offset", "end_lineno", "end_col_offset")):
        raise Refuse("AST node lacks exact source span")
    lines = raw.splitlines(keepends=True)
    start = sum(len(line) for line in lines[:node.lineno - 1]) + node.col_offset
    end = (sum(len(line) for line in lines[:node.end_lineno - 1]) +
           node.end_col_offset)
    return start, end


def apply_replacements(
        raw: bytes, replacements: list[tuple[ast.AST, bytes]]) -> bytes:
    edits = [(span(raw, node)[0], span(raw, node)[1], value)
             for node, value in replacements]
    edits.sort(reverse=True)
    result = raw
    last_start = len(raw) + 1
    for start, end, value in edits:
        if end > last_start or not (0 <= start < end <= len(raw)):
            raise Refuse("overlapping or invalid AST byte replacement")
        result = result[:start] + value + result[end:]
        last_start = start
    return result


def core_source_state(
        raw: bytes, role: str, pins: dict[str, str]) -> tuple[str, bytes, str]:
    tree = source_tree(raw, role)
    if role == "producer":
        flag_name = "FINAL_V15_CORE_PINS_INSTALLED"
        pin_names = (
            "CONTRACT_FILE_PIN", "CONTRACT_OBJECT_PIN", "CLOSED_SCHEMA_FILE_PIN")
        expected = (
            pins["contract_file"], pins["contract_object"], pins["schema_file"])
        draft = ("d0" * 32, "e0" * 32, "f0" * 32)
        sentinel_name = "V15_DRAFT_CORE_PIN_SENTINELS"
    elif role == "consumer":
        flag_name = "FINAL_CURRENT_V15_PINS_INSTALLED"
        pin_names = (
            "CONTRACT_FILE_PIN", "CONTRACT_OBJECT_PIN", "CLOSED_SCHEMA_FILE_PIN",
            "PRODUCER_SOURCE_PIN")
        expected = (
            pins["contract_file"], pins["contract_object"], pins["schema_file"],
            pins["producer_file"])
        draft = ("d9" * 32, "e9" * 32, "f9" * 32, "a9" * 32)
        sentinel_name = "V15_DRAFT_CURRENT_CORE_PINS"
    else:
        raise Refuse("unknown core role")

    flag_node = module_assignment(tree, flag_name)
    flag_value_node = assignment_value(flag_node)
    flag = small_eval(flag_value_node)
    if (not isinstance(flag_value_node, ast.Constant) or
            type(flag_value_node.value) is not bool):
        raise Refuse(role + ": final flag is not an exact bool literal")
    pin_value_nodes = tuple(
        assignment_value(module_assignment(tree, name)) for name in pin_names)
    values = tuple(small_eval(node) for node in pin_value_nodes)
    sentinel_value_node = assignment_value(
        module_assignment(tree, sentinel_name))
    require_exact_constant_tuple(
        sentinel_value_node, draft, role + " sentinel declaration")
    if any(value in draft for value in expected):
        raise Refuse(role + ": final DAG pin collides with a draft sentinel")
    if flag is False and values == draft:
        if any(not isinstance(node, ast.Constant) or node.value != value
               for node, value in zip(pin_value_nodes, draft)):
            raise Refuse(role + ": draft pin is not the exact sentinel literal")
        state = "DRAFT"
    elif flag is True and values == expected:
        if any(not isinstance(node, ast.Constant) or node.value != value
               for node, value in zip(pin_value_nodes, expected)):
            raise Refuse(role + ": final pin is not an exact string literal")
        state = "FINAL"
    else:
        raise Refuse(role + ": mixed, stale, or unrecognized pin state")
    if state == "FINAL":
        proposed = raw
    else:
        replacements: list[tuple[ast.AST, bytes]] = [
            (assignment_value(flag_node), b"True")]
        replacements.extend(
            (assignment_value(module_assignment(tree, name)),
             json.dumps(value).encode("ascii"))
            for name, value in zip(pin_names, expected))
        proposed = apply_replacements(raw, replacements)
    post_tree = source_tree(proposed, role + " proposed")
    post_flag = assignment_value(module_assignment(post_tree, flag_name))
    if (not isinstance(post_flag, ast.Constant) or post_flag.value is not True):
        raise Refuse(role + ": proposed final flag did not close")
    post_nodes = tuple(assignment_value(module_assignment(post_tree, name))
                       for name in pin_names)
    post_values = tuple(small_eval(node) for node in post_nodes)
    if post_values != expected:
        raise Refuse(role + ": proposed pins do not equal DAG inputs")
    if any(not isinstance(node, ast.Constant) or node.value != value
           for node, value in zip(post_nodes, expected)):
        raise Refuse(role + ": proposed pins are not exact string literals")
    require_exact_constant_tuple(
        assignment_value(module_assignment(post_tree, sentinel_name)),
        draft, role + " proposed sentinel declaration")
    return state, proposed, sha256(proposed)


def validate_launcher_receipt_first_pin(
        tree: ast.Module, mapping: ast.Dict, label: str,
) -> None:
    file_node = assignment_value(module_assignment(
        tree, "V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT_FILE_PIN"))
    object_node = assignment_value(module_assignment(
        tree, "V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT_OBJECT_PIN"))
    if (not isinstance(file_node, ast.Constant) or
            not isinstance(object_node, ast.Constant) or
            file_node.value != V14_SUPERSESSION_RECEIPT_FILE_SHA256 or
            object_node.value != V14_SUPERSESSION_RECEIPT_OBJECT_SHA256):
        raise Refuse(label + ": v14 supersession receipt constant literal pins mismatch")
    first = mapping.values[0]
    if (not isinstance(first, ast.Tuple) or len(first.elts) != 2 or
            not isinstance(first.elts[0], ast.Name) or
            first.elts[0].id != "V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT_FILE_PIN" or
            not isinstance(first.elts[1], ast.Name) or
            first.elts[1].id != "V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT_OBJECT_PIN"):
        raise Refuse(label + ": receipt-first tuple is not the exact fixed pin pair")


def require_launcher_current_pin_ast(
        mapping: ast.Dict, names: list[str | None],
        base7: dict[str, tuple[str, str | None]], state: str, label: str,
) -> None:
    for index, name in enumerate(names[1:], start=1):
        if name is None:
            raise Refuse(label + ": non-name BASE7 key")
        node = mapping.values[index]
        if not isinstance(node, ast.Tuple) or len(node.elts) != 2:
            raise Refuse(label + ": BASE7 pin row is not an exact pair")
        if state == "DRAFT":
            expected_object_name = (
                "_DRAFT_OBJECT_PIN" if name in OBJECT_BASE7_KEYS else None)
            if (not isinstance(node.elts[0], ast.Name) or
                    node.elts[0].id != "_DRAFT_FILE_PIN" or
                    (expected_object_name is None and not (
                        isinstance(node.elts[1], ast.Constant) and
                        node.elts[1].value is None)) or
                    (expected_object_name is not None and not (
                        isinstance(node.elts[1], ast.Name) and
                        node.elts[1].id == expected_object_name))):
                raise Refuse(label + ": draft BASE7 pin expression changed")
        else:
            expected = base7[name]
            if any(not isinstance(item, ast.Constant) or item.value != value
                   for item, value in zip(node.elts, expected)):
                raise Refuse(label + ": final BASE7 pin literals mismatch")


def pin_normalized_launcher_ast(raw: bytes, label: str) -> str:
    tree = source_tree(raw, label)
    flag = module_assignment(tree, "FINAL_BASE7_PINS_INSTALLED")
    flag.value = ast.Constant(value=False)
    funcs = [node for node in tree.body
             if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and
             node.name == "configure_workspace_paths"]
    if len(funcs) != 1:
        raise Refuse(label + ": configure_workspace_paths not unique")
    rows = [node for node in funcs[0].body
            if isinstance(node, ast.Assign) and len(node.targets) == 1 and
            isinstance(node.targets[0], ast.Name) and
            node.targets[0].id == "BASE7_PINS"]
    if len(rows) != 1 or not isinstance(rows[0].value, ast.Dict):
        raise Refuse(label + ": BASE7_PINS direct dict not unique")
    value = rows[0].value
    key_names = [key.id if isinstance(key, ast.Name) else None
                 for key in value.keys]
    expected_keys = ["V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT", *CURRENT_BASE7_KEYS]
    if key_names != expected_keys or len(value.values) != 7:
        raise Refuse(label + ": receipt-first BASE7 order mismatch")
    validate_launcher_receipt_first_pin(tree, value, label)
    receipt_before = ast.dump(value.values[0], include_attributes=False)
    for index, key in enumerate(key_names[1:], start=1):
        value.values[index] = ast.Tuple(elts=[
            ast.Constant(value="f" * 64),
            ast.Constant(value="e" * 64 if key in OBJECT_BASE7_KEYS else None),
        ], ctx=ast.Load())
    if ast.dump(value.values[0], include_attributes=False) != receipt_before:
        raise Refuse(label + ": normalizer changed v14 supersession receipt pin")
    return sha256(ast.dump(
        tree, annotate_fields=True, include_attributes=False).encode("utf-8"))


def launcher_state(
        raw: bytes,
        base7: dict[str, tuple[str, str | None]],
) -> tuple[str, bytes, str, str]:
    tree = source_tree(raw, "launcher")
    draft_file_node = assignment_value(
        module_assignment(tree, "_DRAFT_FILE_PIN"))
    draft_object_node = assignment_value(
        module_assignment(tree, "_DRAFT_OBJECT_PIN"))
    draft_file = small_eval(draft_file_node)
    draft_object = small_eval(draft_object_node)
    if draft_file != "f" * 64 or draft_object != "e" * 64:
        raise Refuse("launcher forbidden draft sentinel values changed")
    if (not is_exact_repeat(draft_file_node, "f", 64) or
            not is_exact_repeat(draft_object_node, "e", 64)):
        raise Refuse("launcher forbidden draft sentinel expressions changed")
    flag_node = module_assignment(tree, "FINAL_BASE7_PINS_INSTALLED")
    flag_value_node = assignment_value(flag_node)
    flag = small_eval(flag_value_node)
    if (not isinstance(flag_value_node, ast.Constant) or
            type(flag_value_node.value) is not bool):
        raise Refuse("launcher final flag is not an exact bool literal")
    funcs = [node for node in tree.body
             if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and
             node.name == "configure_workspace_paths"]
    if len(funcs) != 1:
        raise Refuse("launcher configure_workspace_paths not unique")
    assignments = [node for node in funcs[0].body
                   if isinstance(node, ast.Assign) and len(node.targets) == 1 and
                   isinstance(node.targets[0], ast.Name) and
                   node.targets[0].id == "BASE7_PINS"]
    if len(assignments) != 1 or not isinstance(assignments[0].value, ast.Dict):
        raise Refuse("launcher BASE7_PINS direct dict not unique")
    mapping = assignments[0].value
    names = [key.id if isinstance(key, ast.Name) else None for key in mapping.keys]
    if names != ["V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT", *CURRENT_BASE7_KEYS]:
        raise Refuse("launcher BASE7 is not receipt-first exact7")
    validate_launcher_receipt_first_pin(tree, mapping, "launcher")
    constants = {"_DRAFT_FILE_PIN": draft_file, "_DRAFT_OBJECT_PIN": draft_object}
    current = {
        name: small_eval(mapping.values[index], constants)
        for index, name in enumerate(names[1:], start=1)}
    expected_draft = {
        name: (draft_file, draft_object if name in OBJECT_BASE7_KEYS else None)
        for name in CURRENT_BASE7_KEYS}
    if flag is False and current == expected_draft:
        state = "DRAFT"
    elif flag is True and current == base7:
        state = "FINAL"
    else:
        raise Refuse("launcher mixed, stale, or unrecognized BASE7 state")
    require_launcher_current_pin_ast(
        mapping, names, base7, state, "launcher " + state.lower())
    normalized_before = pin_normalized_launcher_ast(raw, "launcher pre")
    if state == "FINAL":
        proposed = raw
    else:
        replacements: list[tuple[ast.AST, bytes]] = [
            (assignment_value(flag_node), b"True")]
        for index, name in enumerate(names[1:], start=1):
            replacements.append((
                mapping.values[index],
                repr(base7[name]).encode("ascii")))
        proposed = apply_replacements(raw, replacements)
    post_tree = source_tree(proposed, "launcher proposed")
    post_draft_file = assignment_value(
        module_assignment(post_tree, "_DRAFT_FILE_PIN"))
    post_draft_object = assignment_value(
        module_assignment(post_tree, "_DRAFT_OBJECT_PIN"))
    if (not is_exact_repeat(post_draft_file, "f", 64) or
            not is_exact_repeat(post_draft_object, "e", 64)):
        raise Refuse("launcher proposal modified forbidden sentinels")
    post_flag = assignment_value(module_assignment(
        post_tree, "FINAL_BASE7_PINS_INSTALLED"))
    if not isinstance(post_flag, ast.Constant) or post_flag.value is not True:
        raise Refuse("launcher proposed final flag is not exact True literal")
    post_funcs = [node for node in post_tree.body
                  if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and
                  node.name == "configure_workspace_paths"]
    post_assignments = [node for node in post_funcs[0].body
                        if isinstance(node, ast.Assign) and
                        len(node.targets) == 1 and
                        isinstance(node.targets[0], ast.Name) and
                        node.targets[0].id == "BASE7_PINS"]
    if len(post_assignments) != 1 or not isinstance(
            post_assignments[0].value, ast.Dict):
        raise Refuse("launcher proposed BASE7 direct dict not unique")
    post_mapping = post_assignments[0].value
    validate_launcher_receipt_first_pin(
        post_tree, post_mapping, "launcher proposed")
    require_launcher_current_pin_ast(
        post_mapping, names, base7, "FINAL", "launcher proposed")
    normalized_after = pin_normalized_launcher_ast(proposed, "launcher proposed")
    if normalized_before != normalized_after:
        raise Refuse("PIN_NORMALIZED launcher AST changed across injection")
    return state, proposed, sha256(proposed), normalized_before


def read_json_held(path: Path, label: str) -> tuple[Held, dict[str, Any], str, str | None]:
    held = Held.open(path, writable=False, expected_mode=0o664)
    try:
        value = strict_json(held.raw, label, canonical_bytes=False)
        obj = object_sha256(value, label) if "object_sha256" in value else None
        return held, value, sha256(held.raw), obj
    except BaseException:
        held.close()
        raise


def validate_schema_contract(
        schema: dict[str, Any], schema_hash: str,
        contract: dict[str, Any], contract_hash: str,
        contract_object: str) -> None:
    if not isinstance(schema.get("$defs"), dict):
        raise Refuse("schema: closed $defs mapping absent")
    bundle = contract.get("v15_bundle")
    if not isinstance(bundle, dict):
        raise Refuse("contract: v15_bundle absent")
    closed = bundle.get("closed_schema")
    if not isinstance(closed, dict) or closed.get("file_sha256") != schema_hash:
        raise Refuse("contract does not bind current schema bytes")
    if (schema_hash != SCHEMA_FILE_SHA256 or
            contract_hash != CONTRACT_FILE_SHA256 or
            contract_object != CONTRACT_OBJECT_SHA256):
        raise Refuse("schema/contract bytes differ from installer pins")


def open_core(*, writable: bool) -> tuple[list[Held], dict[str, Any]]:
    held: list[Held] = []
    try:
        exact12, _ = open_v14_exact12()
        held.extend(exact12)
        schema_h, schema, schema_file, _ = read_json_held(SCHEMA, "v15 schema")
        held.append(schema_h)
        contract_h, contract, contract_file, contract_object = read_json_held(
            CONTRACT, "v15 contract")
        held.append(contract_h)
        if contract_object is None:
            raise Refuse("v15 contract lacks object closure")
        validate_schema_contract(
            schema, schema_file, contract, contract_file, contract_object)
        require_core_phase_absence()
        launcher = Held.open(
            LAUNCHER, writable=False, expected_mode=0o664)
        held.append(launcher)
        launcher_tree = source_tree(launcher.raw, "launcher core-stage held")
        if (sha256(launcher.raw) != CURRENT_LAUNCHER_DRAFT_SHA256 or
                exact_literal(
                    launcher_tree, "FINAL_BASE7_PINS_INSTALLED") is not False):
            raise Refuse("core stage requires exact reviewed draft launcher")
        producer = Held.open(PRODUCER, writable=writable, expected_mode=0o664)
        consumer = Held.open(CONSUMER, writable=writable, expected_mode=0o664)
        held.extend((producer, consumer))
        same_mount(held)
        pins = {"schema_file": schema_file, "contract_file": contract_file,
                "contract_object": contract_object}
        p_state, p_new, p_new_hash = core_source_state(
            producer.raw, "producer", pins)
        producer_pre = sha256(producer.raw)
        expected_producer_pre = (
            CURRENT_PRODUCER_DRAFT_SHA256 if p_state == "DRAFT" else
            CURRENT_PRODUCER_FINAL_SHA256)
        if (producer_pre != expected_producer_pre or
                p_new_hash != CURRENT_PRODUCER_FINAL_SHA256):
            raise Refuse("producer current/proposed generation pin mismatch")
        pins["producer_file"] = p_new_hash
        c_state, c_new, c_new_hash = core_source_state(
            consumer.raw, "consumer", pins)
        if c_state == "FINAL" and p_state != "FINAL":
            raise Refuse(
                "invalid reverse partial state: consumer final before producer")
        consumer_pre = sha256(consumer.raw)
        expected_consumer_pre = (
            CURRENT_CONSUMER_DRAFT_SHA256 if c_state == "DRAFT" else
            CURRENT_CONSUMER_FINAL_SHA256)
        if (consumer_pre != expected_consumer_pre or
                c_new_hash != CURRENT_CONSUMER_FINAL_SHA256):
            raise Refuse("consumer current/proposed generation pin mismatch")
        wiring = validate_exact12_16_source_wiring({
            "producer": producer.raw,
            "consumer": consumer.raw,
            "launcher": launcher.raw,
        })
        return held, {
            "pins": pins,
            "producer_state": p_state,
            "consumer_state": c_state,
            "producer_pre_sha256": producer_pre,
            "consumer_pre_sha256": consumer_pre,
            "launcher_pre_sha256": sha256(launcher.raw),
            "producer_post_sha256": p_new_hash,
            "consumer_post_sha256": c_new_hash,
            "producer_new": p_new,
            "consumer_new": c_new,
            "exact12_16_wiring": wiring,
        }
    except BaseException:
        close_all(held)
        raise


def validate_transition_audit_bindings(
        transition: dict[str, Any], audit: dict[str, Any],
        hashes: dict[str, str]) -> None:
    successor = transition.get("successor_v15_static_bundle")
    audited = audit.get("audited_v15_bundle")
    if not isinstance(successor, dict) or not isinstance(audited, dict):
        raise Refuse("transition/audit current bundle binding absent")

    expected = {
        "closed_schema": (SCHEMA, hashes["SCHEMA"], None),
        "contract": (CONTRACT, hashes["CONTRACT"], hashes["CONTRACT_OBJECT"]),
        "build_only_producer": (PRODUCER, hashes["PRODUCER"], None),
        "independent_verifier_assembler_authority_consumer": (
            CONSUMER, hashes["CONSUMER"], None),
    }
    for key, (path, file_pin, object_pin) in expected.items():
        row = successor.get(key)
        if not isinstance(row, dict) or row.get("path") != str(path.relative_to(ROOT)) \
                or row.get("file_sha256") != file_pin:
            raise Refuse("transition stale binding: " + key)
        if object_pin is not None and row.get("object_sha256") != object_pin:
            raise Refuse("transition stale object binding: " + key)
        audit_row = audited.get(key)
        if not isinstance(audit_row, dict) or audit_row.get("path") != \
                str(path.relative_to(ROOT)) or audit_row.get("file_sha256") != file_pin:
            raise Refuse("audit stale binding: " + key)
        if object_pin is not None and audit_row.get("object_sha256") != object_pin:
            raise Refuse("audit stale object binding: " + key)

    transition_row = audited.get("v14_to_v15_transition_receipt")
    if (not isinstance(transition_row, dict) or
            transition_row.get("path") != str(TRANSITION.relative_to(ROOT)) or
            transition_row.get("file_sha256") != hashes["TRANSITION"] or
            transition_row.get("object_sha256") != hashes["TRANSITION_OBJECT"]):
        raise Refuse("audit does not bind current transition")

    dual = audit.get("dual_independent_static_checkers")
    if not isinstance(dual, dict):
        raise Refuse("audit dual checker proof absent")
    expected_normalized = hashes["LAUNCHER_PIN_NORMALIZED"]
    found = []
    for value in dual.values():
        if isinstance(value, dict) and "pin_normalized_launcher_ast_sha256" in value:
            found.append(value["pin_normalized_launcher_ast_sha256"])
    if not found or any(value != expected_normalized for value in found):
        raise Refuse("audit launcher PIN_NORMALIZED binding mismatch")


def open_launcher(*, writable: bool) -> tuple[list[Held], dict[str, Any]]:
    held: list[Held] = []
    try:
        for path, label in ((SCHEMA, "v15 schema"), (CONTRACT, "v15 contract"),
                            (TRANSITION, "v15 transition"), (AUDIT, "v15 audit")):
            item, value, file_hash, obj_hash = read_json_held(path, label)
            held.append(item)
            if path in (CONTRACT, TRANSITION, AUDIT) and obj_hash is None:
                raise Refuse(label + ": object closure absent")
            if path == SCHEMA:
                schema, schema_file = value, file_hash
            elif path == CONTRACT:
                contract, contract_file, contract_object = value, file_hash, obj_hash
            elif path == TRANSITION:
                transition, transition_file, transition_object = value, file_hash, obj_hash
            else:
                audit, audit_file, audit_object = value, file_hash, obj_hash
        validate_schema_contract(
            schema, schema_file, contract, contract_file, str(contract_object))

        producer = Held.open(PRODUCER, writable=False, expected_mode=0o664)
        consumer = Held.open(CONSUMER, writable=False, expected_mode=0o664)
        launcher = Held.open(LAUNCHER, writable=writable, expected_mode=0o664)
        receipt = Held.open(V14_SUPERSESSION_RECEIPT, writable=False, expected_mode=0o444)
        held.extend((producer, consumer, launcher, receipt))
        same_mount(held)
        receipt_value = strict_json(
            receipt.raw, "v14 runtime-registry supersession receipt", canonical_bytes=True)
        if (sha256(receipt.raw) != V14_SUPERSESSION_RECEIPT_FILE_SHA256 or
                object_sha256(receipt_value, "v14 runtime-registry supersession receipt") !=
                V14_SUPERSESSION_RECEIPT_OBJECT_SHA256):
            raise Refuse("v14 runtime-registry supersession receipt pin mismatch")

        core_pins = {"schema_file": schema_file, "contract_file": contract_file,
                     "contract_object": str(contract_object)}
        p_state, p_same, p_hash = core_source_state(
            producer.raw, "producer", core_pins)
        if p_state != "FINAL" or p_same != producer.raw:
            raise Refuse("launcher stage requires final producer")
        core_pins["producer_file"] = p_hash
        c_state, c_same, c_hash = core_source_state(
            consumer.raw, "consumer", core_pins)
        if c_state != "FINAL" or c_same != consumer.raw:
            raise Refuse("launcher stage requires final consumer")

        hashes = {
            "SCHEMA": schema_file,
            "CONTRACT": contract_file,
            "CONTRACT_OBJECT": str(contract_object),
            "PRODUCER": p_hash,
            "CONSUMER": c_hash,
            "TRANSITION": transition_file,
            "TRANSITION_OBJECT": str(transition_object),
            "AUDIT": audit_file,
            "AUDIT_OBJECT": str(audit_object),
            "LAUNCHER_PIN_NORMALIZED": pin_normalized_launcher_ast(
                launcher.raw, "launcher held"),
        }
        validate_transition_audit_bindings(transition, audit, hashes)
        base7 = {
            "SCHEMA": (schema_file, None),
            "CONTRACT": (contract_file, str(contract_object)),
            "PRODUCER": (p_hash, None),
            "CONSUMER": (c_hash, None),
            "TRANSITION": (transition_file, str(transition_object)),
            "AUDIT": (audit_file, str(audit_object)),
        }
        state, proposed, post_hash, normalized = launcher_state(launcher.raw, base7)
        if normalized != hashes["LAUNCHER_PIN_NORMALIZED"]:
            raise Refuse("launcher normalized hash drift during proposal")
        return held, {
            "hashes": hashes,
            "base7": base7,
            "launcher_state": state,
            "launcher_pre_sha256": sha256(launcher.raw),
            "launcher_post_sha256": post_hash,
            "launcher_pin_normalized_ast_sha256": normalized,
            "launcher_new": proposed,
        }
    except BaseException:
        close_all(held)
        raise


def write_held(
        item: Held, raw: bytes, *, expected_before: bytes | None = None,
) -> None:
    if not item.writable:
        raise Refuse(str(item.path) + ": held fd is read-only")
    if expected_before is None:
        item.revalidate_path_identity()
    else:
        item.terminal_replay(expected_before)
    offset = 0
    while offset < len(raw):
        written = os.pwrite(item.fd, raw[offset:offset + (1 << 20)], offset)
        if written <= 0:
            raise OSError("short/zero pwrite")
        offset += written
    os.ftruncate(item.fd, len(raw))
    os.fsync(item.fd)
    item.revalidate_path_identity()
    if pread_all(item.fd) != raw:
        raise Refuse(str(item.path) + ": post-write replay mismatch")


def fsync_parents(items: Iterable[Held]) -> None:
    seen: set[tuple[int, int]] = set()
    for item in items:
        info = os.fstat(item.parent_fd)
        identity = (info.st_dev, info.st_ino)
        if identity not in seen:
            os.fsync(item.parent_fd)
            seen.add(identity)


def contract_value(args: argparse.Namespace, name: str) -> str | None:
    return getattr(args, name, None)


def require_exact_contract(
        args: argparse.Namespace, expected: dict[str, str], enabled: bool) -> str:
    supplied = {name: contract_value(args, name) for name in expected}
    present = [value is not None for value in supplied.values()]
    if enabled and not any(present):
        return "SOURCE_ONE_SHOT_ENABLE_FLAG"
    if not all(present):
        raise Refuse(
            "write disabled: provide the complete exact expected-prehash contract")
    mismatches = {
        name: {"expected": expected[name], "supplied": supplied[name]}
        for name in expected if supplied[name] != expected[name]}
    if mismatches:
        raise Refuse("exact expected-prehash contract mismatch: " +
                     canonical(mismatches).decode("utf-8"))
    return "EXPLICIT_EXACT_EXPECTED_PREHASH_CONTRACT"


def core_result(info: dict[str, Any], status: str) -> dict[str, Any]:
    return {
        "schema": "cm2.c79g.v15.final-pin-installer.core-result.v1",
        "status": status,
        "stage": "CORE__S_TO_C_TO_P_TO_CONSUMER",
        "write_performed": False,
        "producer_state": info["producer_state"],
        "consumer_state": info["consumer_state"],
        "pre_sha256": {
            "schema": info["pins"]["schema_file"],
            "contract_file": info["pins"]["contract_file"],
            "contract_object": info["pins"]["contract_object"],
            "producer": info["producer_pre_sha256"],
            "consumer": info["consumer_pre_sha256"],
        },
        "proposed_post_sha256": {
            "producer": info["producer_post_sha256"],
            "consumer": info["consumer_post_sha256"],
        },
        "transition_and_audit_absent": True,
        "v15_pyc_count": 0,
        "runtime_surface_count": 0,
        "core_noncrash_atomicity_boundary": CORE_CRASH_BOUNDARY,
        "durable_core_commit_point": CORE_COMMIT_POINT,
    }


def launcher_result(info: dict[str, Any], status: str) -> dict[str, Any]:
    return {
        "schema": "cm2.c79g.v15.final-pin-installer.launcher-result.v1",
        "status": status,
        "stage": "LAUNCHER__T_TO_A_TO_L",
        "write_performed": False,
        "launcher_state": info["launcher_state"],
        "base7": {
            key: {"file_sha256": value[0], "object_sha256": value[1]}
            for key, value in info["base7"].items()},
        "launcher_pre_sha256": info["launcher_pre_sha256"],
        "launcher_proposed_post_sha256": info["launcher_post_sha256"],
        "pin_normalized_launcher_ast_sha256":
            info["launcher_pin_normalized_ast_sha256"],
        "pin_normalized_pre_post_identical": True,
        "v14_supersession_receipt_is_immutable_first_base7_member": True,
        "v15_pyc_count": 0,
        "runtime_surface_count": 0,
    }


def preflight_core() -> dict[str, Any]:
    require_static_absence()
    require_core_phase_absence()
    held, info = open_core(writable=False)
    try:
        replay_snapshot(held)
        require_core_phase_absence()
        require_static_absence()
        status = ("PREFLIGHT_CORE_ALREADY_INSTALLED" if
                  info["producer_state"] == info["consumer_state"] == "FINAL"
                  else "PREFLIGHT_CORE_PASS__INSTALL_NOT_EXECUTED")
        return core_result(info, status)
    finally:
        close_all(held)


def replay_core() -> dict[str, Any]:
    require_static_absence()
    require_core_phase_absence()
    held, info = open_core(writable=False)
    try:
        replay_snapshot(held)
        require_core_phase_absence()
        require_static_absence()
        if not (info["producer_state"] == info["consumer_state"] == "FINAL"):
            raise Refuse("REPLAY_CORE requires both core sources FINAL")
        result = core_result(info, "REPLAY_CORE_PASS__NO_WRITE")
        result["terminal_replay_completed"] = True
        return result
    finally:
        close_all(held)


def install_core(
        args: argparse.Namespace, official_lock: OfficialWriterLock,
) -> dict[str, Any]:
    official_lock.revalidate_claim()
    require_static_absence(allowed_claim=official_lock)
    require_core_phase_absence()
    held, info = open_core(writable=True)
    targets = held[-2:]
    originals = [item.raw for item in targets]
    commit_started = False
    try:
        expected_contract = {
            "expect_schema_file_sha256": info["pins"]["schema_file"],
            "expect_contract_file_sha256": info["pins"]["contract_file"],
            "expect_contract_object_sha256": info["pins"]["contract_object"],
            "expect_producer_pre_sha256": info["producer_pre_sha256"],
            "expect_consumer_pre_sha256": info["consumer_pre_sha256"],
        }
        authority = require_exact_contract(
            args, expected_contract, ONE_SHOT_CORE_WRITE_ENABLED)
        replay_snapshot(held)
        require_core_phase_absence()
        require_static_absence(allowed_claim=official_lock)
        if info["producer_state"] == info["consumer_state"] == "FINAL":
            result = core_result(info, "INSTALL_CORE_IDEMPOTENT_ALREADY_INSTALLED")
            result["authorization"] = authority
            return result
        if info["consumer_state"] == "FINAL" and info["producer_state"] != "FINAL":
            raise Refuse("invalid reverse partial state: consumer final before producer")
        commit_started = True
        write_held(
            targets[0], info["producer_new"], expected_before=targets[0].raw)
        replay_snapshot(held, {PRODUCER: info["producer_new"]})
        require_core_phase_absence()
        require_static_absence(allowed_claim=official_lock)
        write_held(
            targets[1], info["consumer_new"], expected_before=targets[1].raw)
        replay_snapshot(held, {
            PRODUCER: info["producer_new"],
            CONSUMER: info["consumer_new"],
        })
        require_core_phase_absence()
        require_static_absence(allowed_claim=official_lock)
        fsync_parents(targets)
        replay_snapshot(held, {
            PRODUCER: info["producer_new"],
            CONSUMER: info["consumer_new"],
        })
        require_core_phase_absence()
        require_static_absence(allowed_claim=official_lock)
        result = core_result(info, "INSTALL_CORE_PASS__STDOUT_RECEIPT_ONLY")
        result["write_performed"] = True
        result["authorization"] = authority
        result["post_sha256"] = {
            "producer": sha256(targets[0].terminal_replay(info["producer_new"])),
            "consumer": sha256(targets[1].terminal_replay(info["consumer_new"])),
        }
        result["rollback_required"] = False
        return result
    except BaseException as exc:
        rollback = {"attempted": commit_started, "restored": False,
                    "error": None}
        if commit_started:
            try:
                for item, original in zip(targets, originals):
                    write_held(item, original)
                fsync_parents(targets)
                replay_snapshot(held)
                require_core_phase_absence()
                require_static_absence(allowed_claim=official_lock)
                rollback["restored"] = True
            except BaseException as restore_exc:
                rollback["error"] = type(restore_exc).__name__ + ":" + str(restore_exc)
        raise Refuse(str(exc) + " | rollback=" +
                     canonical(rollback).decode("utf-8")) from exc
    finally:
        close_all(held)


def preflight_launcher() -> dict[str, Any]:
    require_static_absence()
    held, info = open_launcher(writable=False)
    try:
        replay_snapshot(held)
        require_static_absence()
        status = ("PREFLIGHT_LAUNCHER_ALREADY_INSTALLED" if
                  info["launcher_state"] == "FINAL" else
                  "PREFLIGHT_LAUNCHER_PASS__INSTALL_NOT_EXECUTED")
        return launcher_result(info, status)
    finally:
        close_all(held)


def replay_launcher() -> dict[str, Any]:
    require_static_absence()
    held, info = open_launcher(writable=False)
    try:
        replay_snapshot(held)
        require_static_absence()
        if info["launcher_state"] != "FINAL":
            raise Refuse("REPLAY_LAUNCHER requires final launcher pins")
        launcher = next(item for item in held if item.path == LAUNCHER)
        if pin_normalized_launcher_ast(
                launcher.terminal_replay(), "launcher terminal replay") != \
                info["launcher_pin_normalized_ast_sha256"]:
            raise Refuse("REPLAY_LAUNCHER PIN_NORMALIZED mismatch")
        result = launcher_result(
            info, "REPLAY_LAUNCHER_PASS__NO_WRITE")
        result["terminal_replay_completed"] = True
        return result
    finally:
        close_all(held)


def install_launcher(
        args: argparse.Namespace, official_lock: OfficialWriterLock,
) -> dict[str, Any]:
    official_lock.revalidate_claim()
    require_static_absence(allowed_claim=official_lock)
    held, info = open_launcher(writable=True)
    target = next(item for item in held if item.path == LAUNCHER)
    original = target.raw
    commit_started = False
    try:
        hashes = info["hashes"]
        expected_contract = {
            "expect_schema_file_sha256": hashes["SCHEMA"],
            "expect_contract_file_sha256": hashes["CONTRACT"],
            "expect_contract_object_sha256": hashes["CONTRACT_OBJECT"],
            "expect_producer_pre_sha256": hashes["PRODUCER"],
            "expect_consumer_pre_sha256": hashes["CONSUMER"],
            "expect_transition_file_sha256": hashes["TRANSITION"],
            "expect_transition_object_sha256": hashes["TRANSITION_OBJECT"],
            "expect_audit_file_sha256": hashes["AUDIT"],
            "expect_audit_object_sha256": hashes["AUDIT_OBJECT"],
            "expect_launcher_pre_sha256": info["launcher_pre_sha256"],
            "expect_launcher_pin_normalized_sha256":
                info["launcher_pin_normalized_ast_sha256"],
        }
        authority = require_exact_contract(
            args, expected_contract, ONE_SHOT_LAUNCHER_WRITE_ENABLED)
        replay_snapshot(held)
        require_static_absence(allowed_claim=official_lock)
        if info["launcher_state"] == "FINAL":
            result = launcher_result(
                info, "INSTALL_LAUNCHER_IDEMPOTENT_ALREADY_INSTALLED")
            result["authorization"] = authority
            return result
        commit_started = True
        write_held(
            target, info["launcher_new"], expected_before=target.raw)
        replay_snapshot(held, {LAUNCHER: info["launcher_new"]})
        require_static_absence(allowed_claim=official_lock)
        fsync_parents([target])
        replay_snapshot(held, {LAUNCHER: info["launcher_new"]})
        require_static_absence(allowed_claim=official_lock)
        if pin_normalized_launcher_ast(
                target.terminal_replay(), "launcher installed") != \
                info["launcher_pin_normalized_ast_sha256"]:
            raise Refuse("installed launcher PIN_NORMALIZED replay mismatch")
        require_static_absence(allowed_claim=official_lock)
        result = launcher_result(
            info, "INSTALL_LAUNCHER_PASS__STDOUT_RECEIPT_ONLY")
        result["write_performed"] = True
        result["authorization"] = authority
        result["launcher_post_sha256"] = sha256(
            target.terminal_replay(info["launcher_new"]))
        result["rollback_required"] = False
        return result
    except BaseException as exc:
        rollback = {"attempted": commit_started, "restored": False,
                    "error": None}
        if commit_started:
            try:
                write_held(target, original)
                fsync_parents([target])
                replay_snapshot(held)
                require_static_absence(allowed_claim=official_lock)
                rollback["restored"] = True
            except BaseException as restore_exc:
                rollback["error"] = type(restore_exc).__name__ + ":" + str(restore_exc)
        raise Refuse(str(exc) + " | rollback=" +
                     canonical(rollback).decode("utf-8")) from exc
    finally:
        close_all(held)


def add_contract_args(parser: argparse.ArgumentParser) -> None:
    for name in (
            "schema-file-sha256", "contract-file-sha256",
            "contract-object-sha256", "producer-pre-sha256",
            "consumer-pre-sha256", "transition-file-sha256",
            "transition-object-sha256", "audit-file-sha256",
            "audit-object-sha256", "launcher-pre-sha256",
            "launcher-pin-normalized-sha256"):
        parser.add_argument("--expect-" + name, default=None)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="C79g v15 fail-closed final-pin installer")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("PREFLIGHT_CORE")
    sub.add_parser("REPLAY_CORE")
    core = sub.add_parser("INSTALL_CORE")
    add_contract_args(core)
    sub.add_parser("PREFLIGHT_LAUNCHER")
    sub.add_parser("REPLAY_LAUNCHER")
    launcher = sub.add_parser("INSTALL_LAUNCHER")
    add_contract_args(launcher)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    official_lock: OfficialWriterLock | None = None
    try:
        write_command = args.command in {"INSTALL_CORE", "INSTALL_LAUNCHER"}
        official_lock = OfficialWriterLock.acquire(
            transaction_claim=write_command)
        if args.command == "PREFLIGHT_CORE":
            result = preflight_core()
        elif args.command == "REPLAY_CORE":
            result = replay_core()
        elif args.command == "INSTALL_CORE":
            result = install_core(args, official_lock)
        elif args.command == "PREFLIGHT_LAUNCHER":
            result = preflight_launcher()
        elif args.command == "REPLAY_LAUNCHER":
            result = replay_launcher()
        elif args.command == "INSTALL_LAUNCHER":
            result = install_launcher(args, official_lock)
        else:
            raise Refuse("unknown command")
        official_lock.revalidate()
        result["official_writer_coordination_lock"] = {
            "api": "fcntl.flock(LOCK_EX)",
            "held_for_entire_command": True,
            "runtime_directory_st_dev": official_lock.before.st_dev,
            "runtime_directory_st_ino": official_lock.before.st_ino,
            "runtime_directory_mount_id": official_lock.mount_id,
            "held_path_identity_terminally_revalidated_before_unlock": True,
            "transaction_claim_used": write_command,
        }
        official_lock.release()
        official_lock = None
        result["installer_file_sha256"] = sha256(Path(__file__).read_bytes())
        result["success"] = True
        sys.stdout.buffer.write(canonical(result) + b"\n")
        return 0
    except BaseException as exc:
        cleanup_error: str | None = None
        if official_lock is not None and official_lock.fd >= 0:
            try:
                official_lock.release()
            except BaseException as cleanup_exc:
                cleanup_error = type(cleanup_exc).__name__ + ":" + str(cleanup_exc)
        failure = {
            "schema": "cm2.c79g.v15.final-pin-installer.failure.v1",
            "status": "FAIL_CLOSED__NO_RUNTIME_AUTHORIZATION",
            "command": args.command,
            "success": False,
            "error_type": type(exc).__name__,
            "error": str(exc),
            "write_enable_flags": {
                "core": ONE_SHOT_CORE_WRITE_ENABLED,
                "launcher": ONE_SHOT_LAUNCHER_WRITE_ENABLED,
            },
            "core_noncrash_atomicity_boundary": CORE_CRASH_BOUNDARY,
            "durable_core_commit_point": CORE_COMMIT_POINT,
            "installer_file_sha256": sha256(Path(__file__).read_bytes()),
        }
        if cleanup_error is not None:
            failure["official_lock_cleanup_error"] = cleanup_error
        sys.stdout.buffer.write(canonical(failure) + b"\n")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
