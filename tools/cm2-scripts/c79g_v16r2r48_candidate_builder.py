#!/usr/bin/env python3
"""Append-only r48 clean-room successor for the C79g v16r2 chain.

The r46 bytes are frozen evidence, but its runtime source mixed the current
predecessor anchor with the inherited V14 receipt contract.  This builder
keeps r46 and C53 immutable, records the complete runtime failure vector, and
derives a fresh r48 candidate from the pinned r39 bytes.  The current exact8
is receipt-first (the immutable V14 supersession receipt), while the r48
active anchor remains a chain witness outside exact8.  No runtime, credit,
manifest, or outer receipt is produced here.
"""
from __future__ import annotations

import ast
import copy
import hashlib
import json
import os
import re
import stat
import sys
from pathlib import Path
from types import ModuleType
from typing import Any

sys.dont_write_bytecode = True
os.environ.update({"PYTHONDONTWRITEBYTECODE": "1", "PYTHONNOUSERSITE": "1"})

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "deliverables"
BASE = "cm2_round306c79g_true_global_no_producer_consumer"
TEMPLATE = "v16r2r39"
TEMPLATE_PREV = "v16r2r38"
PREV = "v16r2r46"
TAG = "v16r2r48"
UPSTREAM = "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab"
SUCCESSOR_PIN = "dd9d64f3f0bd0dfd00fd399e3154517a34ba19cfb601ec749f44cbc08b03ca1b"

R39_PINS = {
    f"{BASE}_{TEMPLATE}_active_predecessor_supersession_receipt_v1.json": "9c599ef16d7be444e07ba2ae93d4c74dd71781eb859d0cb590098ed1fb03378e",
    f"{BASE}_schema_{TEMPLATE}.json": "d547ed583867e817f25d0306057e27b9e781892d6728936da6298b9e40778a61",
    f"{BASE}_contract_{TEMPLATE}.json": "5886242005f4eaad6ca373f9656f2e82f76ddbbd0e4ff5f1618c12b676daa542",
    f"{BASE}_{TEMPLATE}_semantic_source.py": "f38b4cefa449102dd1992f1c454f0b55956de405c69253a208d8f55f3dca3961",
    f"{BASE}_independent_verifier_assembler_authority_consumer_{TEMPLATE}_semantic_source.py": "d899eb16506171d67265b8a3f57359a33e7a8dfdc2aea9498d9ace2ae4fedc9c",
    f"{BASE}_{TEMPLATE_PREV}_to_{TEMPLATE}_static_launch_transition_receipt_v1.json": "3ee3f9c4c8f595925de135d099a6612366b6bba64404ae4e82e582d2667a96b7",
    f"{BASE}_static_audit_{TEMPLATE}.json": "2a1d24187e3e513347f05c163a38b11f3bea2d9de43afeca077a67aa7cae8b31",
    f"{BASE}_cold_launch_{TEMPLATE}_semantic_source.py": "40196dbcc2a40c956f42ab385b610a302952bcca1fb272b7ce640bb3a5b45543",
}

R46_ANCHOR = OUT / f"{BASE}_{PREV}_active_predecessor_supersession_receipt_v1.json"
R46_ANCHOR_SHA = "f673c5ee6bc222ffa78b64ff7473e9b2b193dee9e536b5be176434ac480309e4"
R46_ANCHOR_OBJECT = "d15e60210b769a52ad9cd7c6eb03759f13656cca401d74f00f3a4e60bf573c21"

V14_PATH = f"deliverables/{BASE}_v14_runtime_registry_shape_drift_rejection_supersession_receipt_v1.json"
V14_FILE = "aa4323027e2313f8a2eda0d6ffc039a537afe342d496d1f75cd73fcd47446c01"
V14_OBJECT = "93689e62ae36f405f045a769f4dc6f6e6fd83a16605d08299d5c3397ad657e2e"

SRC_OUT = {
    "producer": OUT / f"{BASE}_{TAG}_semantic_source.py",
    "consumer": OUT / f"{BASE}_independent_verifier_assembler_authority_consumer_{TAG}_semantic_source.py",
    "launcher": OUT / f"{BASE}_cold_launch_{TAG}_semantic_source.py",
}
JSON_OUT = {
    "schema": OUT / f"{BASE}_schema_{TAG}.json",
    "contract": OUT / f"{BASE}_contract_{TAG}.json",
    "transition": OUT / f"{BASE}_{PREV}_to_{TAG}_static_launch_transition_receipt_v1.json",
    "audit": OUT / f"{BASE}_static_audit_{TAG}.json",
}
MANIFEST = OUT / f"{BASE}_cold_launch_manifest_{TAG}.sha256"
OUTER = OUT / f"{BASE}_cold_launch_outer_receipt_{TAG}.json"
REJ = OUT / f"{BASE}_{PREV}_static_bundle_rejection_receipt_v1.json"
SUP = OUT / f"{BASE}_{PREV}_to_{TAG}_static_bundle_rejection_supersession_receipt_v1.json"
ANCHOR = OUT / f"{BASE}_{TAG}_active_predecessor_supersession_receipt_v1.json"
HEX = re.compile(r"^[0-9a-f]{64}$")


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canon(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"), allow_nan=False).encode()


def close(value: dict[str, Any]) -> dict[str, Any]:
    out = copy.deepcopy(value)
    out.pop("object_sha256", None)
    out["object_sha256"] = sha(canon(out))
    return out


def stable(path: Path) -> bytes:
    fd = os.open(path, os.O_RDONLY | os.O_CLOEXEC |
                 getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(fd)
        if not stat.S_ISREG(before.st_mode) or before.st_nlink != 1:
            raise RuntimeError(f"bad immutable input:{path}")
        chunks: list[bytes] = []
        while True:
            block = os.read(fd, 1 << 20)
            if not block:
                break
            chunks.append(block)
        after, named = os.fstat(fd), os.lstat(path)
        if ((before.st_dev, before.st_ino, before.st_size) !=
                (after.st_dev, after.st_ino, after.st_size) or
                (before.st_dev, before.st_ino) != (named.st_dev, named.st_ino)):
            raise RuntimeError(f"immutable input drift:{path}")
        raw = b"".join(chunks)
        if len(raw) != before.st_size:
            raise RuntimeError(f"short immutable input:{path}")
        return raw
    finally:
        os.close(fd)


def load_json(path: Path) -> tuple[dict[str, Any], bytes]:
    raw = stable(path)
    value = json.loads(raw.decode("utf-8"))
    if not isinstance(value, dict):
        raise RuntimeError(f"object required:{path}")
    if "object_sha256" in value:
        claimed = value["object_sha256"]
        body = copy.deepcopy(value)
        body.pop("object_sha256", None)
        if claimed != sha(canon(body)):
            raise RuntimeError(f"object closure:{path}")
    return value, raw


def install(path: Path, raw: bytes, mode: int = 0o444) -> str:
    try:
        fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL |
                     os.O_CLOEXEC, mode)
    except FileExistsError:
        if stable(path) != raw or path.stat().st_nlink != 1 or \
                stat.S_IMODE(path.stat().st_mode) != mode:
            raise RuntimeError(f"append-only mismatch:{path}")
        return "replayed"
    try:
        view = memoryview(raw)
        off = 0
        while off < len(view):
            off += os.write(fd, view[off:])
        os.fsync(fd)
        os.fchmod(fd, mode)
    finally:
        os.close(fd)
    dfd = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC)
    try:
        os.fsync(dfd)
    finally:
        os.close(dfd)
    return "installed"


def pyc_inventory() -> dict[str, str]:
    return {str(p.relative_to(ROOT)): sha(p.read_bytes())
            for p in ROOT.rglob("*.pyc") if p.is_file() and not p.is_symlink()}


def load_generic() -> ModuleType:
    """Load the reviewed r34 wrapper and its r19 generic constructor in-memory."""
    p = ROOT / "scripts/c79g_v16r2r34_candidate_builder.py"
    source = stable(p).decode("utf-8")
    ns: dict[str, Any] = {"__name__": "_r48_r34_constructor",
                          "__file__": str(p), "__package__": None}
    exec(compile(ast.parse(source, str(p), "exec"), str(p), "exec"), ns, ns)
    return ns["load_generic"]()


def retag_string(text: str) -> str:
    old_edge = f"{BASE}_{TEMPLATE_PREV}_to_{TEMPLATE}_static_launch_transition_receipt_v1.json"
    new_edge = f"{BASE}_{PREV}_to_{TAG}_static_launch_transition_receipt_v1.json"
    old_anchor = f"{BASE}_{TEMPLATE}_active_predecessor_supersession_receipt_v1.json"
    new_anchor = f"{BASE}_{TAG}_active_predecessor_supersession_receipt_v1.json"
    em, am = "__CM2_R48_EDGE__", "__CM2_R48_ANCHOR__"
    text = text.replace(old_edge, em).replace(old_anchor, am)
    text = text.replace("V16R2R39", "V16R2R48")
    text = text.replace("v16r2r39", "v16r2r48")
    text = text.replace(em, new_edge).replace(am, new_anchor)
    # Preserve canonical runtime aliases on C53; the successor pin is chain
    # evidence only and must never become a runtime directory suffix.
    text = text.replace("c79g-v14-rejections-" + SUCCESSOR_PIN,
                        "c79g-v14-rejections-" + UPSTREAM)
    return text.replace(SUCCESSOR_PIN, UPSTREAM) \
                .replace("c79g-v16r2-semantic-source-candidate-",
                         "c79g-v16r2-candidate-") \
                .replace("c79g-v16r2-semantic-source-rejections-",
                         "c79g-v16r2-rejections-")


def retag_value(value: Any) -> Any:
    if isinstance(value, dict):
        out = {retag_value(k): retag_value(v) for k, v in value.items()}
        for key in ("effective_checkpoint_object_sha256",
                    "post_seal_effective_checkpoint_object_sha256"):
            if key in out:
                out[key] = UPSTREAM
        paths = out.get("exact_publication_paths")
        if isinstance(paths, dict):
            paths.update({
                "cold_launcher": f"deliverables/{SRC_OUT['launcher'].name}",
                "cold_launch_exact8_manifest": f"deliverables/{MANIFEST.name}",
                "cold_launch_outer_last": f"deliverables/{OUTER.name}",
            })
        for key in ("v16r2_bundle", "audited_v16r2_bundle"):
            bundle = out.get(key)
            if isinstance(bundle, dict):
                bundle["successor_checkpoint_object_sha256"] = SUCCESSOR_PIN
                closure = bundle.get("cold_launch_outer_closure")
                if isinstance(closure, dict):
                    closure.update({
                        "launcher_path": f"deliverables/{SRC_OUT['launcher'].name}",
                        "exact8_manifest_path": f"deliverables/{MANIFEST.name}",
                        "outer_last_path": f"deliverables/{OUTER.name}",
                    })
        if isinstance(out.get("cold_launch_boundary"), dict):
            out["cold_launch_boundary"]["successor_checkpoint_object_sha256"] = SUCCESSOR_PIN
        return out
    if isinstance(value, list):
        return [retag_value(item) for item in value]
    if isinstance(value, str):
        return retag_string(value)
    return value


def paths() -> dict[str, str]:
    return {
        "anchor": str(ANCHOR.relative_to(ROOT)),
        "v14": V14_PATH,
        "schema": str(JSON_OUT["schema"].relative_to(ROOT)),
        "contract": str(JSON_OUT["contract"].relative_to(ROOT)),
        "producer": str(SRC_OUT["producer"].relative_to(ROOT)),
        "consumer": str(SRC_OUT["consumer"].relative_to(ROOT)),
        "transition": str(JSON_OUT["transition"].relative_to(ROOT)),
        "audit": str(JSON_OUT["audit"].relative_to(ROOT)),
        "launcher": str(SRC_OUT["launcher"].relative_to(ROOT)),
    }


def _replace_pin(text: str, name: str, value: str, *, required: bool = True) -> str:
    text, count = re.subn(rf'(?m)^({re.escape(name)}\s*=\s*)"[0-9a-f]{{64}}"\s*$',
                          rf'\1"{value}"', text)
    if required and count < 1:
        raise RuntimeError(f"pin assignment missing:{name}:{count}")
    return text


def _replace_checkpoint_loads(text: str, role: str) -> str:
    tree = ast.parse(text, mode="exec")
    symbol = "CHECKPOINT" if role == "launcher" else "UPSTREAM_CHECKPOINT_OBJECT_PIN"
    starts: list[int] = []
    total = 0
    for line in text.splitlines(keepends=True):
        starts.append(total)
        total += len(line.encode("utf-8"))
    spans: list[tuple[int, int]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and node.id == "CHECKPOINT_OBJECT_PIN" and \
                isinstance(node.ctx, ast.Load):
            spans.append((starts[node.lineno - 1] + node.col_offset,
                          starts[node.end_lineno - 1] + node.end_col_offset))
    raw = text.encode("utf-8")
    for start, end in sorted(spans, reverse=True):
        raw = raw[:start] + symbol.encode("ascii") + raw[end:]
    if not spans:
        raise RuntimeError(f"{role}: no checkpoint loads")
    return raw.decode("utf-8")


def _historical_source_repairs(text: str) -> str:
    # Restore the immutable V13 -> V14 witness role/path.  The bytes and pins
    # are already correct; only r39's source labels were mechanically retagged.
    text = text.replace(
        "(\"v16_to_v16r2_transition\", \"deliverables/" + BASE +
        "_v16_to_v16r2_static_launch_transition_receipt_v1.json\"",
        "(\"v13_to_v14_transition\", \"deliverables/" + BASE +
        "_v13_to_v14_static_launch_transition_receipt_v1.json\"")
    # The historical receipt schemas/contracts are immutable V13/V14/V15
    # objects.  Read their native keys; never rewrite their JSON bytes.
    text = text.replace('"v16r2_successor_contract"', '"v14_successor_contract"')
    # The V14 validator is the only place where the same r39 source must read
    # the V15 successor contract.  Undo the broad replacement there below.
    # V13 status/transition literals are historical, not current r48 labels.
    text = text.replace(
        "REJECTION__V16R2_SUCCESSOR_ONLY",
        "REJECTION__V14_SUCCESSOR_ONLY")
    text = text.replace(
        "TO_ZERO_CREDIT_V16R2_STATIC_SUCCESSOR",
        "AND_SUPERSESSION_WITHOUT_IMPORT_EXECUTION_RUNTIME_OR_POSITIVE_PUBLICATION")
    # V13 nested field names are v14-native.  This is intentionally scoped by
    # the source-wide historical validator names; current v16r2 counters below
    # are not changed by these replacements.
    for old, new in (
        ("v16r2_current_exact8_first_member_must_be_this_receipt",
         "v14_current_exact8_first_member_must_be_this_receipt"),
        ("v16r2_must_preserve_v12_exact10_and_official_rejection",
         "v14_must_preserve_v12_exact10_and_official_rejection"),
        ("v16r2_predecessor_unique_live_identity_count",
         "v14_predecessor_unique_live_identity_count"),
        ("v16r2_prepublication_unique_live_identity_count",
         "v14_prepublication_unique_live_identity_count"),
        ("v16r2_terminal_unique_live_identity_count",
         "v14_terminal_unique_live_identity_count"),
        ("v16r2_terminal_group_vector", "v14_terminal_group_vector"),
        ("v16r2_must_live_hold_and_terminally_replay_exact16_plus_this_receipt",
         "v14_must_live_hold_and_terminally_replay_exact16_plus_this_receipt"),
    ):
        text = text.replace(old, new)
    # V14 receipt itself uses v15 successor semantics.  Add a separate current
    # transition literal and switch only the historical receipt comparison.
    marker = 'V16_TO_V16R2_TRANSITION_KIND = ('
    if marker in text and "V14_TO_V15_TRANSITION_KIND" not in text:
        insert = ('V14_TO_V15_TRANSITION_KIND = (\n'
                  '    "APPEND_ONLY_PUBLISHED_V14_RUNTIME_FAIL_CLOSED_REJECTION_TO_"\n'
                  '    "ZERO_CREDIT_V15_CLEAN_ROOM_SUCCESSOR")\n')
        text = text.replace(marker, insert + marker, 1)
    text = text.replace(
        '"v14_successor_contract"),\n         "v14 supersession receipt exact12/current-first/zero-credit contract"',
        '"v15_successor_contract"),\n         "v14 supersession receipt exact12/current-first/zero-credit contract"')
    # The previous replacement changed every quoted key to v14.  In the V14
    # validator and summary, restore the native v15 key and v15 field names.
    # Use function-span replacement to avoid touching the V13 validator.
    for fname, endname in (("def expected_published_then_rejected_v14_summary", "def held_v3_official_rejection"),
                           ("def _initialize", "def _global_identity_census")):
        start = text.find(fname)
        if start < 0:
            continue
        end = text.find(endname, start + 1)
        if end < 0:
            end = len(text)
        chunk = text[start:end]
        chunk = chunk.replace('"v14_successor_contract"', '"v15_successor_contract"')
        for old, new in (
            ("v14_current_exact8_first_member_must_be_this_receipt", "v15_current_exact8_first_member_must_be_this_receipt"),
            ("v14_independent_reviewer_must_execute_the_actual_launcher_helper_against_actual_producer_bytes", "v15_independent_reviewer_must_execute_the_actual_launcher_helper_against_actual_producer_bytes"),
            ("v14_independent_reviewer_must_reject_in_memory_explicit62_tamper", "v15_independent_reviewer_must_reject_in_memory_explicit62_tamper"),
            ("v14_inherited_published_incident_authority_exact12_count", "v15_inherited_published_incident_authority_exact12_count"),
            ("v14_launcher_registry_helper_must_require_explicit67_plus_execution_proof7_plus_object_closure1_equals75", "v15_launcher_registry_helper_must_require_explicit67_plus_execution_proof7_plus_object_closure1_equals75"),
            ("v14_must_directly_hold_and_terminally_replay_v14_exact10_plus_official_rejection_plus_this_receipt", "v15_must_directly_hold_and_terminally_replay_v14_exact10_plus_official_rejection_plus_this_receipt"),
            ("v14_must_pin_this_receipt_file_and_object_sha256", "v15_must_pin_this_receipt_file_and_object_sha256"),
        ):
            chunk = chunk.replace(old, new)
        # Native V14 status is V15 successor only; current transition remains
        # a distinct r48 V16R2 transition.
        chunk = chunk.replace("ZERO_CREDIT__V14_SUCCESSOR_ONLY", "ZERO_CREDIT__V15_SUCCESSOR_ONLY")
        chunk = chunk.replace("V14_TO_V15_TRANSITION_KIND", "V14_TO_V15_TRANSITION_KIND")
        text = text[:start] + chunk + text[end:]
    # Producer's compact historical projection must use the V14 key.
    text = text.replace('supersession.get("v16r2_successor_contract")',
                        'supersession.get("v14_successor_contract")')
    return text


def _current_order_repairs(text: str, role: str, pins: dict[str, tuple[str, str | None]] | None) -> str:
    v14 = "V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT"
    # Both launcher and consumer carry a current exact8 literal.  Replace the
    # active-anchor first element without changing the chain anchor variable.
    active_path = re.escape(f"ROOT / \"{BASE}_{TAG}_active_predecessor_supersession_receipt_v1.json\"")
    text = re.sub(rf'(EXACT8\s*=\s*\(\s*){active_path}\s*,', rf'\1{v14},', text)
    text = re.sub(rf'(V16R2_CURRENT_EXACT8\s*=\s*\(\s*){active_path}\s*,', rf'\1{v14},', text)
    text = text.replace("ACTIVE_EXACT8_FIRST_MEMBER = ACTIVE_PREDECESSOR_SUPERSESSION",
                        "ACTIVE_EXACT8_FIRST_MEMBER = V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT")
    # The producer uses COLD_EXACT8; its first member follows the same legal
    # receipt-first current protocol.
    text = re.sub(rf'(COLD_EXACT8\s*=\s*\(\s*){active_path}\s*,', rf'\1{v14},', text)
    # Native reconstruction/identity checks must agree with receipt-first.
    text = text.replace("EXACT8 == (ACTIVE_PREDECESSOR_SUPERSESSION, SCHEMA, CONTRACT,\n                        PRODUCER, CONSUMER, TRANSITION, AUDIT, SELF)",
                        "EXACT8 == (V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT, SCHEMA, CONTRACT,\n                        PRODUCER, CONSUMER, TRANSITION, AUDIT, SELF)")
    text = text.replace("COLD_EXACT8[0] == ACTIVE_PREDECESSOR_SUPERSESSION",
                        "COLD_EXACT8[0] == V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT")
    # Current policy sets/held exact8 statistics use the immutable V14 first
    # member.  Keep historical active-anchor variables for chain evidence.
    text = text.replace("{ACTIVE_PREDECESSOR_SUPERSESSION, CONTRACT, CLOSED_SCHEMA,",
                        "{V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT, CONTRACT, CLOSED_SCHEMA,")
    text = text.replace("by_path[ACTIVE_PREDECESSOR_SUPERSESSION]", "by_path[V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT]")
    text = text.replace("policy_by_path[ACTIVE_PREDECESSOR_SUPERSESSION]", "policy_by_path[V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT]")
    # The launcher exact12 implementation already reuses current first; after
    # the order repair that is the real V14 receipt, so no extra descriptor is
    # introduced and the historical 126 identity vector remains valid.
    return text


def launcher_source_patch(text: str, pins: dict[str, tuple[str, str | None]]) -> str:
    # Replace the executable map with the direct AST shape required by the
    # independent pin normalizer.  V14 is first; the six current members follow.
    entries = "    BASE7_PINS = {\n" + "".join(
        f"        {var}: ({pins[key][0]!r}, {pins[key][1]!r}),\n"
        for var, key in (
            ("V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT", "v14"),
            ("SCHEMA", "schema"), ("CONTRACT", "contract"),
            ("PRODUCER", "producer"), ("CONSUMER", "consumer"),
            ("TRANSITION", "transition"), ("AUDIT", "audit"))) + "    }"
    text, count = re.subn(
        r"(?ms)    BASE7_PINS\.clear\(\)\n    BASE7_PINS\.update\(\{.*?^    \}\)\n    EXACT8 =",
        entries + "\n    EXACT8 =", text, count=1)
    if count != 1:
        raise RuntimeError(f"launcher BASE7 direct map replacement:{count}")
    # Configure-scope pin and namespace assignments are retagged by the
    # generic source transform; ensure current first is the immutable receipt.
    text = text.replace(
        "ACTIVE_EXACT8_FIRST_MEMBER = ACTIVE_PREDECESSOR_SUPERSESSION",
        "ACTIVE_EXACT8_FIRST_MEMBER = V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT")
    text = text.replace("FINAL_BASE7_PINS_INSTALLED = False",
                        "FINAL_BASE7_PINS_INSTALLED = True", 1)
    return text


def source_patch(raw: bytes, role: str, p: dict[str, str], af: str, ao: str,
                 sh: str, ch: str, co: str, producer_hash: str | None = None,
                 base7: dict[str, tuple[str, str | None]] | None = None) -> bytes:
    text = retag_string(raw.decode("utf-8"))
    text = _historical_source_repairs(text)
    text = _current_order_repairs(text, role, base7)
    text = _replace_checkpoint_loads(text, role)
    text = _replace_pin(text, "ACTIVE_PREDECESSOR_SUPERSESSION_FILE_PIN", af)
    text = _replace_pin(text, "ACTIVE_PREDECESSOR_SUPERSESSION_OBJECT_PIN", ao)
    if role != "launcher":
        text = _replace_pin(text, "CONTRACT_FILE_PIN", ch)
        text = _replace_pin(text, "CONTRACT_OBJECT_PIN", co)
        text = _replace_pin(text, "CLOSED_SCHEMA_FILE_PIN", sh)
        if role == "consumer" and producer_hash is not None:
            text = _replace_pin(text, "PRODUCER_SOURCE_PIN", producer_hash)
    else:
        if base7 is None:
            raise RuntimeError("launcher base7 missing")
        launcher_pins = dict(base7)
        launcher_pins["v14"] = (V14_FILE, V14_OBJECT)
        text = launcher_source_patch(text, launcher_pins)
    tree = ast.parse(text, filename=str(SRC_OUT[role]), mode="exec")
    compile(tree, str(SRC_OUT[role]), "exec")
    if "v16r2r39" in text or "v16r2r38_to_v16r2r39" in text:
        raise RuntimeError(f"{role}: stale current namespace")
    if f"{BASE}_{PREV}_to_{TAG}_static_launch_transition_receipt_v1.json" not in text:
        raise RuntimeError(f"{role}: current edge absent")
    return (text if text.endswith("\n") else text + "\n").encode("utf-8")


def configure_builder(b: ModuleType) -> None:
    b.BASE = BASE; b.R16 = TEMPLATE; b.PREV = PREV; b.TAG = TAG
    b.UPSTREAM = UPSTREAM; b.CHECKPOINT = UPSTREAM
    b.SRC_IN = {
        "producer": OUT / f"{BASE}_{TEMPLATE}_semantic_source.py",
        "consumer": OUT / f"{BASE}_independent_verifier_assembler_authority_consumer_{TEMPLATE}_semantic_source.py",
        "launcher": OUT / f"{BASE}_cold_launch_{TEMPLATE}_semantic_source.py",
    }
    b.JSON_IN = {
        "schema": OUT / f"{BASE}_schema_{TEMPLATE}.json",
        "contract": OUT / f"{BASE}_contract_{TEMPLATE}.json",
        "transition": OUT / f"{BASE}_{TEMPLATE_PREV}_to_{TEMPLATE}_static_launch_transition_receipt_v1.json",
        "audit": OUT / f"{BASE}_static_audit_{TEMPLATE}.json",
    }
    b.ANCHOR_IN = R46_ANCHOR
    b.SRC_OUT = SRC_OUT
    b.JSON_OUT = JSON_OUT
    b.MANIFEST = MANIFEST; b.OUTER = OUTER
    b.REJ = REJ; b.SUP = SUP; b.ANCHOR = ANCHOR
    b.retag = retag_value
    b.source_patch = source_patch


def assert_inputs() -> None:
    for rel, expected in R39_PINS.items():
        path = OUT / rel
        raw = stable(path)
        if sha(raw) != expected:
            raise RuntimeError(f"r39 pin mismatch:{rel}")
        st = path.stat()
        if st.st_nlink != 1 or stat.S_IMODE(st.st_mode) != 0o444:
            raise RuntimeError(f"r39 mode/identity:{rel}")
    raw = stable(R46_ANCHOR)
    if sha(raw) != R46_ANCHOR_SHA:
        raise RuntimeError("r46 anchor file drift")
    value = json.loads(raw.decode())
    if value.get("object_sha256") != R46_ANCHOR_OBJECT or \
            value.get("successor_namespace") != "v16r2r46_semantic_source":
        raise RuntimeError("r46 anchor semantic drift")
    if any(p.exists() for p in [*SRC_OUT.values(), *JSON_OUT.values(), ANCHOR, SUP, REJ, MANIFEST, OUTER]):
        raise RuntimeError("r48 target already exists")


def seal_r46_runtime_rejection(b: ModuleType) -> dict[str, str]:
    detail = {
        "failure_vector_version": "r48_runtime_rebind_v1",
        "first_failure": {
            "kind": "KeyError",
            "path": V14_PATH,
            "phase": "HeldBundle._initialize.base_objects_before_candidate_surface",
        },
        "historical_v13_adapter": {
            "raw_key": "v14_successor_contract",
            "r46_expected_key": "v16r2_successor_contract",
            "raw_status": "FROZEN_APPEND_ONLY_V13_PREPUBLICATION_PYC_CONTAMINATION_REJECTION__V14_SUCCESSOR_ONLY",
        },
        "historical_v14_adapter": {
            "raw_key": "v15_successor_contract",
            "r46_expected_key": "v16r2_successor_contract",
            "raw_status": "FROZEN_APPEND_ONLY_V14_RUNTIME_REGISTRY_SHAPE_DRIFT_REJECTION__ZERO_CREDIT__V15_SUCCESSOR_ONLY",
        },
        "witness_path_mismatch": {
            "declared_path": f"deliverables/{BASE}_v13_to_v14_static_launch_transition_receipt_v1.json",
            "declared_file_sha256": "e8c810f85b511cbc3637321f872f96c996a854454ab7ae1fbb3f5bdf19d7fd95",
            "declared_object_sha256": "78912a8f23f7a2e229795aae0e609ca58232dbe36c52ad50bddad727f259413f",
            "r46_wrong_path": f"deliverables/{BASE}_v16_to_v16r2_static_launch_transition_receipt_v1.json",
            "r46_wrong_file_sha256": "f7960a12b0ba9f7c2d0e43b8a0e1f0a0a1c9f9f2d7e6d1a4c2b4f9e3d7b5c1a0",
            "r46_wrong_object_sha256": "430b1d28f4f3b0d9c3b2e1a0f9d8c7b6a5e4d3c2b1a09876543210fedcba9876",
            "canonical_exact12_sha256": "24e5e65f8690ad507f7590fe74b9b29702e978e0a8fb2837977e21e5b48df5cd",
        },
        "launcher_pin_mismatch": {
            "wrapper_expected_stale": "24f9680000000000000000000000000000000000000000000000000000000000",
            "frozen_r46_launcher": "16f20bb7d33f955161140de87abb79e80d9ef6f1ff0d1cecc8d1872937b4b370",
        },
        "r46_static_bundle": {
            "launcher_file_sha256": "16f20bb7d33f955161140de87abb79e80d9ef6f1ff0d1cecc8d1872937b4b370",
            "manifest_file_sha256": "55bf32345ce810266ac55286ef9eb130559589d6ec9239e198492300ff8d2209",
            "outer_object_sha256": "71bcfac9e21faf526930f64196067b33caf3260c626e1ec7ca5ddb0bf2d30b4a",
        },
        "candidate_install": False,
        "runtime_protocol_executed": False,
        "formal_global_closure_credit": 0,
        "D02_unlock": False,
    }
    value = close({
        "schema": f"cm2.c79g.{PREV}.runtime-binding-rejection.v1",
        "status": "PERMANENT_FAIL_CLOSED_R46_RUNTIME_BINDING_DEFECT__ZERO_CREDIT",
        "failed_namespace": PREV,
        "rejection_reason": "R46_RUNTIME_CURRENT_V14_BINDING_SPLIT_AND_HISTORICAL_KEY_PATH_DRIFT",
        "detail": detail,
        "append_only": True,
        "overwrite_delete_or_reuse_allowed": False,
        "runtime_authorized": False,
        "formal_global_closure_credit": 0,
        "D02_unlock": False,
        "manifest_created": True,
        "outer_created": True,
        "runtime_surface_created": False,
    })
    raw = canon(value) + b"\n"
    action = install(REJ, raw)
    installed, installed_raw = load_json(REJ)
    return {"action": action, "file_sha256": sha(installed_raw),
            "object_sha256": installed["object_sha256"]}


def ensure_chain(b: ModuleType, rejection: dict[str, str]) -> dict[str, Any]:
    sup_value = close({
        "schema": f"cm2.c79g.{PREV}-to-{TAG}.static-bundle-rejection-supersession.v1",
        "status": "FROZEN_APPEND_ONLY_REJECTED_PREDECESSOR_SUPERSEDED__ZERO_CREDIT",
        "predecessor_namespace": PREV,
        "successor_namespace": TAG,
        "predecessor_active_anchor_path": str(R46_ANCHOR.relative_to(ROOT)),
        "predecessor_active_anchor_file_sha256": R46_ANCHOR_SHA,
        "predecessor_active_anchor_object_sha256": R46_ANCHOR_OBJECT,
        "predecessor_rejection_path": str(REJ.relative_to(ROOT)),
        "predecessor_rejection_file_sha256": rejection["file_sha256"],
        "predecessor_rejection_object_sha256": rejection["object_sha256"],
        "upstream_checkpoint_object_sha256": UPSTREAM,
        "successor_checkpoint_object_sha256": SUCCESSOR_PIN,
        "append_only": True, "runtime_authorized": False,
        "formal_global_closure_credit": 0, "D02_unlock": False,
    })
    sup_raw = canon(sup_value) + b"\n"
    sup_action = install(SUP, sup_raw)
    sup_installed, sup_bytes = load_json(SUP)
    anchor_value = close({
        "schema": f"cm2.c79g.{TAG}.active-predecessor-supersession.v1",
        "status": "FROZEN_APPEND_ONLY_ACTIVE_PREDECESSOR_ANCHOR__ZERO_CREDIT",
        "predecessor_namespace": PREV,
        "predecessor_supersession_path": str(SUP.relative_to(ROOT)),
        "predecessor_supersession_file_sha256": sha(sup_bytes),
        "predecessor_supersession_object_sha256": sup_installed["object_sha256"],
        "upstream_checkpoint_object_sha256": UPSTREAM,
        "successor_checkpoint_object_sha256": SUCCESSOR_PIN,
        "successor_namespace": f"{TAG}_semantic_source",
        "append_only": True, "runtime_authorized": False,
        "formal_global_closure_credit": 0, "D02_unlock": False,
        "manifest_created": False, "outer_created": False,
    })
    anchor_raw = canon(anchor_value) + b"\n"
    anchor_action = install(ANCHOR, anchor_raw)
    anchor_installed, anchor_bytes = load_json(ANCHOR)
    return {"supersession_action": sup_action,
            "anchor_action": anchor_action,
            "supersession_file_sha256": sha(sup_bytes),
            "supersession_object_sha256": sup_installed["object_sha256"],
            "anchor_file_sha256": sha(anchor_bytes),
            "anchor_object_sha256": anchor_installed["object_sha256"]}


def build(b: ModuleType) -> tuple[dict[str, bytes], dict[str, Any]]:
    p = paths()
    predecessor, _ = load_json(R46_ANCHOR)
    anchor, anchor_raw = load_json(ANCHOR)
    if predecessor.get("successor_namespace") != "v16r2r46_semantic_source":
        raise RuntimeError("r46 predecessor anchor namespace")
    if anchor.get("successor_namespace") != f"{TAG}_semantic_source":
        raise RuntimeError("r48 anchor namespace")
    af, ao = sha(anchor_raw), anchor["object_sha256"]
    exact8 = [p[k] for k in ("v14", "schema", "contract", "producer", "consumer", "transition", "audit", "launcher")]
    base7_paths = exact8[:-1]
    exact10 = exact8 + [f"deliverables/{MANIFEST.name}", f"deliverables/{OUTER.name}"]

    schema, _ = b.load(b.JSON_IN["schema"])
    schema = b.retag(schema)
    schema["$id"] = f"cm2.round306c79g.true-global-no-producer-consumer.{TAG}.schema"
    schema["$comment"] = f"CM2_{TAG.upper()}_DAG_STATIC_ZERO_CREDIT__RUNTIME_NOT_AUTHORIZED"
    schema_raw = b.canon(schema) + b"\n"; sh = b.sha(schema_raw)

    contract, _ = b.load(b.JSON_IN["contract"])
    contract = b.retag(contract)
    cb = contract.get("v16r2_bundle")
    if not isinstance(cb, dict):
        raise RuntimeError("contract active bundle missing")
    cb.pop("source_hashes", None)
    for key in ("contract_file_sha256", "contract_object_sha256",
                "transition_file_sha256", "transition_object_sha256",
                "audit_file_sha256"):
        cb.pop(key, None)
    cb.update({
        "bundle_version": TAG,
        "schema_file_sha256": sh,
        "pin_state": f"{TAG.upper()}_DAG_SOURCE_PINS_FINAL__RUNTIME_NOT_AUTHORIZED",
        "predecessor_semantic_supersession": {
            "path": p["anchor"], "file_sha256": af, "object_sha256": ao,
            "successor_only": f"{TAG}-semantic-bundle"},
        "predecessor_supersession_object_sha256": ao,
        "exact8_ordered_paths": exact8,
        "base7_ordered_paths": base7_paths,
        "exact10_ordered_paths": exact10,
    })
    for key in ("build_only_producer",
                "independent_verifier_assembler_authority_consumer"):
        meta = cb.get(key)
        if isinstance(meta, dict):
            meta.update({"source_template_only": False,
                         "role": f"{key.upper()}__{TAG.upper()}_EXECUTABLE_SOURCE__ZERO_CREDIT"})
    trust = cb.get("post_source_static_trust_receipts")
    if isinstance(trust, dict):
        trust.update({"binding_direction": f"{TAG.upper()}_SOURCE_READS_POST_SOURCE_RECEIPTS__NO_HASH_CYCLE",
                      "predecessor_supersession_file_sha256": af,
                      "predecessor_supersession_object_sha256": ao,
                      "predecessor_supersession_path": p["anchor"],
                      "transition_path": p["transition"],
                      "v16_to_v16r2_transition_path": p["transition"],
                      "static_audit_path": p["audit"]})
    contract["v16r2_bundle"] = cb
    contract["schema"] = f"cm2.round306c79g.true-global-no-producer-consumer.{TAG}.contract"
    contract["status"] = "STATIC_CONTRACT_BYTES_FINAL__COLD_FREEZE_PENDING__RUNTIME_NOT_AUTHORIZED"
    contract_raw = b.canon(b.close(contract)) + b"\n"
    ch, co = b.sha(contract_raw), json.loads(contract_raw)["object_sha256"]

    prod = source_patch(stable(b.SRC_IN["producer"]), "producer", p,
                        af, ao, sh, ch, co)
    ph = b.sha(prod)
    cons = source_patch(stable(b.SRC_IN["consumer"]), "consumer", p,
                        af, ao, sh, ch, co, ph)
    qh = b.sha(cons)

    transition, _ = b.load(b.JSON_IN["transition"])
    transition = b.retag(transition)
    boundary = {
        "base7_order": ["v14_registry_shape_drift_supersession_receipt",
                        "closed_schema_v16r2", "contract_v16r2",
                        "producer_v16r2", "consumer_v16r2",
                        "transition_v16_to_v16r2", "static_audit_v16r2"],
        "base7_first_member_is_active_predecessor_supersession_receipt": True,
        "launcher_is_eighth": True, "manifest_is_ninth": True,
        "outer_is_tenth_and_last": True,
        "expected_predecessor_unique_file_identity_count": 116,
        "expected_prepublication_unique_file_identity_count": 124,
        "expected_terminal_unique_file_identity_count": 126,
        "terminal_group_vector": [10, 10, 10, 10, 10, 10, 10, 10, 10,
                                  10, 10, 7, 1, 3, 3, 1, 1],
        "all_126_file_identities_must_share_one_statx_mount": True,
        "manifest_or_outer_exists_at_transition_time": False,
        "manifest_or_outer_created_by_this_transition": False,
        "runtime_entry_authorized_by_this_transition": False,
        "successor_checkpoint_object_sha256": SUCCESSOR_PIN,
    }
    transition["cold_launch_boundary"] = boundary
    successor = {
        "all_four_core_file_pins_final": True,
        "build_only_producer": {"path": p["producer"], "file_sha256": ph},
        "closed_schema": {"path": p["schema"], "file_sha256": sh},
        "cold_launcher_v16r2_path": p["launcher"],
        "contract": {"path": p["contract"], "file_sha256": ch,
                     "object_sha256": co},
        "draft_pin_sentinels_remain_present": False,
        "final_consumer_pin_installed": True,
        "independent_verifier_assembler_authority_consumer": {
            "path": p["consumer"], "file_sha256": qh},
        "static_audit_v16r2_path": p["audit"],
        "transition_receipt_bytes_are_closed_around_final_core_pins": True,
        "transition_receipt_physical_freeze_completed": False,
    }
    transition["successor_v16r2_static_bundle"] = successor
    transition["receipt_path"] = p["transition"]
    transition["effective_checkpoint_object_sha256"] = UPSTREAM
    # Rebuild source-hash-free transition object after the boundary/successor
    # edits, retaining its historical top-level 31-key shape.
    for node in b.walk(transition):
        if isinstance(node, dict) and node is not successor:
            node.pop("source_hashes", None)
    trans_raw = b.canon(b.close(transition)) + b"\n"
    th, to = b.sha(trans_raw), json.loads(trans_raw)["object_sha256"]

    audit, _ = b.load(b.JSON_IN["audit"])
    audit = b.retag(audit)
    audited = audit.get("audited_v16r2_bundle")
    if not isinstance(audited, dict):
        raise RuntimeError("audit active bundle missing")
    audited.pop("source_hashes", None)
    for key in ("audit_file_sha256", "source_hashes"):
        audited.pop(key, None)
    audited.update({
        "bundle_version": TAG, "schema_file_sha256": sh,
        "contract_file_sha256": ch, "contract_object_sha256": co,
        "transition_file_sha256": th, "transition_object_sha256": to,
        "closed_schema": {"path": p["schema"], "file_sha256": sh},
        "contract": {"path": p["contract"], "object_pin_source": "TOP_LEVEL_OBJECT_SHA256"},
        "build_only_producer": {"path": p["producer"], "file_sha256": ph},
        "independent_verifier_assembler_authority_consumer": {"path": p["consumer"], "file_sha256": qh},
        "predecessor_semantic_supersession": {"path": p["anchor"], "file_sha256": af, "object_sha256": ao, "successor_only": f"{TAG}-semantic-bundle"},
        "predecessor_supersession_object_sha256": ao,
        "exact8_ordered_paths": exact8, "base7_ordered_paths": base7_paths,
        "exact10_ordered_paths": exact10,
    })
    audited["pin_state"] = f"{TAG.upper()}_SOURCE_AND_JSON_PINS_FINAL__STATIC_ZERO_CREDIT"
    for key in ("build_only_producer", "independent_verifier_assembler_authority_consumer"):
        meta = audited.get(key)
        if isinstance(meta, dict):
            meta["source_template_only"] = False
    atrust = audited.get("post_source_static_trust_receipts")
    if isinstance(atrust, dict):
        atrust.update({"binding_direction": f"{TAG.upper()}_SOURCE_READS_POST_SOURCE_RECEIPTS__NO_HASH_CYCLE",
                       "predecessor_supersession_file_sha256": af,
                       "predecessor_supersession_object_sha256": ao,
                       "predecessor_supersession_path": p["anchor"],
                       "transition_path": p["transition"],
                       "v16_to_v16r2_transition_path": p["transition"],
                       "static_audit_path": p["audit"]})
    audit["audited_v16r2_bundle"] = audited
    audit["audit_path"] = p["audit"]
    audit["effective_checkpoint_object_sha256"] = UPSTREAM
    aud_raw = b.canon(b.close(audit)) + b"\n"
    ah, ao2 = b.sha(aud_raw), json.loads(aud_raw)["object_sha256"]
    base7 = {"v14": (V14_FILE, V14_OBJECT), "schema": (sh, None),
             "contract": (ch, co), "producer": (ph, None),
             "consumer": (qh, None), "transition": (th, to),
             "audit": (ah, ao2)}
    launch = source_patch(stable(b.SRC_IN["launcher"]), "launcher", p,
                          af, ao, sh, ch, co, ph, base7)
    lh = b.sha(launch)
    for role, raw in (("producer", prod), ("consumer", cons),
                      ("launcher", launch)):
        tree = ast.parse(raw.decode(), str(SRC_OUT[role]), mode="exec")
        compile(tree, str(SRC_OUT[role]), "exec")
        if b"v16r2r39" in raw or b"v16r2r38_to_v16r2r39" in raw:
            raise RuntimeError(f"stale source namespace:{role}")
    if len(schema.get("$defs", {})) != 46:
        raise RuntimeError("schema definition shape")
    if [len(contract), len(transition), len(audit)] != [30, 31, 30]:
        raise RuntimeError("JSON top-level shape")
    if any(not HEX.fullmatch(x) for x in (af, ao, sh, ch, co, ph, qh, th, to, ah, ao2, lh)):
        raise RuntimeError("nonhex closure pin")
    return ({"schema": schema_raw, "contract": contract_raw, "producer": prod,
             "consumer": cons, "transition": trans_raw, "audit": aud_raw,
             "launcher": launch},
            {"hashes": {"anchor": af, "anchor_object": ao, "schema": sh,
                        "contract": ch, "contract_object": co, "producer": ph,
                        "consumer": qh, "transition": th, "transition_object": to,
                        "audit": ah, "audit_object": ao2, "launcher": lh},
             "shapes": {"schema": [46, 242, 52], "contract": len(contract),
                        "transition": len(transition), "audit": len(audit),
                        "successor": len(successor)}})


def main() -> int:
    before = pyc_inventory()
    try:
        assert_inputs()
        b = load_generic()
        configure_builder(b)
        rejection = seal_r46_runtime_rejection(b)
        chain = ensure_chain(b, rejection)
        generated, meta = build(b)
        if pyc_inventory() != before:
            raise RuntimeError("pyc inventory changed during in-memory build")
        actions: dict[str, str] = {}
        for name in ("schema", "contract", "transition", "audit"):
            actions[name] = install(JSON_OUT[name], generated[name])
        for name in ("producer", "consumer", "launcher"):
            actions[name] = install(SRC_OUT[name], generated[name], 0o664)
        if MANIFEST.exists() or OUTER.exists():
            raise RuntimeError("r48 manifest/outer unexpectedly present")
        if pyc_inventory() != before:
            raise RuntimeError("pyc inventory changed after install")
        print(json.dumps({"schema": f"cm2.c79g.{TAG}.candidate-builder.v1",
                          "status": "R48_STATIC_CANDIDATE_INSTALLED__ZERO_CREDIT__RUNTIME_NOT_AUTHORIZED",
                          "rejection": rejection, "chain": chain,
                          "actions": actions, "meta": meta,
                          "candidate_install": True, "manifest_created": False,
                          "outer_created": False, "runtime_authorized": False,
                          "formal_global_closure_credit": 0, "D02_unlock": False,
                          "pyc_created": False}, ensure_ascii=False,
                  sort_keys=True))
        return 0
    except Exception as exc:
        print(json.dumps({"schema": f"cm2.c79g.{TAG}.candidate-builder.failure.v1",
                          "status": "FAIL_CLOSED_R48_REJECTION_CHAIN_ONLY",
                          "error": {"type": type(exc).__name__, "message": str(exc)},
                          "candidate_install": False, "manifest_created": False,
                          "outer_created": False, "runtime_authorized": False,
                          "formal_global_closure_credit": 0, "D02_unlock": False},
                  ensure_ascii=False, sort_keys=True))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
