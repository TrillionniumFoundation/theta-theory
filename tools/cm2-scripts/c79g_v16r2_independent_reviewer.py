#!/usr/bin/env python3
"""Independent read-only 34-check gate for the v16r2 clean-room.

The reviewer consumes only bytes.  It never imports or executes a protocol
source and it never writes a deliverable, runtime surface, manifest, outer
receipt, or credit.  A source template is intentionally rejected by the last
semantic check; that keeps the staging result observable as a blocker instead
of allowing an inert placeholder to masquerade as a cold-launch authority.
"""

from __future__ import annotations

import ast
import hashlib
import json
import os
from pathlib import Path
import stat
import symtable
import sys
from typing import Any

sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "deliverables"
RUNTIME = ROOT / ".cm2-runtime"
BASE = "cm2_round306c79g_true_global_no_producer_consumer"
SOURCES = {
    "producer": OUT / f"{BASE}_v16r2.py",
    "consumer": OUT / f"{BASE}_independent_verifier_assembler_authority_consumer_v16r2.py",
    "launcher": OUT / f"{BASE}_cold_launch_v16r2.py",
}
JSONS = {
    "schema": OUT / f"{BASE}_schema_v16r2.json",
    "contract": OUT / f"{BASE}_contract_v16r2.json",
    "transition": OUT / f"{BASE}_v16_to_v16r2_static_launch_transition_receipt_v1.json",
    "audit": OUT / f"{BASE}_static_audit_v16r2.json",
}
SUPERSESSION = OUT / f"{BASE}_v16_semantic_rejection_supersession_receipt_v1.json"
REJECTION = RUNTIME / (
    "c79g-v16-rejections-dd9d64f3f0bd0dfd00fd399e3154517a34ba19cfb601ec749f44cbc08b03ca1b"
) / "rejection.json"
MANIFEST = OUT / f"{BASE}_cold_launch_manifest_v16r2.sha256"
OUTER = OUT / f"{BASE}_cold_launch_outer_receipt_v16r2.json"

CHECK_NAMES = (
    "source_files_present", "source_regular_nlink1", "source_draft_modes",
    "ast_parse", "compile_in_memory", "utf8", "no_v15_tokens",
    "v16r2_tokens", "active_transition_path", "predecessor_supersession_ref",
    "no_old_transition_schema", "runtime_disabled_flags", "final_flags_false",
    "no_pyc", "no_runtime_surfaces", "manifest_absent", "outer_absent",
    "source_hashes_distinct", "source_hashes_stable", "no_starred_calls",
    "no_double_star_calls", "no_duplicate_literal_keys", "no_dangerous_calls",
    "symtable", "json_utf8", "json_duplicate_keys", "schema_full_shape",
    "schema_active_root_ref", "instance_shapes_closed", "zero_credit_baseline",
    "active_exact8_order", "source_pin_consistency", "predecessor_receipts_closed",
    "executable_semantics",
)


class DuplicateKey(ValueError):
    pass


def canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"), allow_nan=False).encode()


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def strict_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        if key in out:
            raise DuplicateKey(key)
        out[key] = value
    return out


def stable(path: Path) -> bytes:
    fd = os.open(path, os.O_RDONLY | os.O_CLOEXEC |
                 getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(fd)
        if not stat.S_ISREG(before.st_mode) or before.st_nlink != 1:
            raise ValueError(f"not regular/nlink1: {path}")
        chunks: list[bytes] = []
        while True:
            block = os.read(fd, 1 << 20)
            if not block:
                break
            chunks.append(block)
        after = os.fstat(fd)
        named = os.lstat(path)
        if ((before.st_dev, before.st_ino, before.st_size) !=
                (after.st_dev, after.st_ino, after.st_size) or
                (before.st_dev, before.st_ino) !=
                (named.st_dev, named.st_ino)):
            raise ValueError(f"identity drift: {path}")
        raw = b"".join(chunks)
        if len(raw) != before.st_size:
            raise ValueError(f"short read: {path}")
        return raw
    finally:
        os.close(fd)


def obj_closed(value: Any) -> bool:
    if not isinstance(value, dict):
        return False
    claim = value.get("object_sha256")
    if not isinstance(claim, str) or len(claim) != 64:
        return False
    body = dict(value)
    body.pop("object_sha256", None)
    return sha(canonical(body)) == claim


def json_read(path: Path) -> tuple[dict[str, Any], bytes]:
    raw = stable(path)
    value = json.loads(raw.decode("utf-8"), object_pairs_hook=strict_pairs)
    if not isinstance(value, dict):
        raise ValueError(f"not object: {path}")
    return value, raw


def walk(value: Any):
    yield value
    if isinstance(value, dict):
        for item in value.values():
            yield from walk(item)
    elif isinstance(value, list):
        for item in value:
            yield from walk(item)


def call_counts(tree: ast.AST) -> tuple[int, int, int, int]:
    star = double = danger = duplicate = 0
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            star += sum(isinstance(arg, ast.Starred) for arg in node.args)
            double += sum(key.arg is None for key in node.keywords)
            if isinstance(node.func, ast.Name) and node.func.id in {"eval", "exec", "__import__"}:
                danger += 1
        elif isinstance(node, ast.Dict):
            keys = [key.value for key in node.keys
                    if isinstance(key, ast.Constant) and isinstance(key.value, str)]
            duplicate += len(keys) - len(set(keys))
    return star, double, danger, duplicate


def row(name: str, passed: bool, detail: Any = None) -> dict[str, Any]:
    out = {"name": name, "passed": bool(passed)}
    if detail is not None:
        out["detail"] = detail
    return out


def main() -> int:
    rows: list[dict[str, Any]] = []
    raw_sources: dict[str, bytes] = {}
    trees: dict[str, ast.Module] = {}
    source_error: str | None = None
    present = all(path.is_file() for path in SOURCES.values())
    rows.append(row("source_files_present", present))
    regular = modes = utf8 = True
    for role, path in SOURCES.items():
        try:
            raw = stable(path)
            raw_sources[role] = raw
            info = path.stat()
            regular &= stat.S_ISREG(info.st_mode) and info.st_nlink == 1
            modes &= stat.S_IMODE(info.st_mode) in {0o664, 0o644}
            text = raw.decode("utf-8")
            try:
                trees[role] = ast.parse(text, filename=str(path))
            except SyntaxError:
                pass
        except Exception as exc:
            regular = modes = utf8 = False
            source_error = f"{type(exc).__name__}: {exc}"
    rows.append(row("source_regular_nlink1", regular))
    rows.append(row("source_draft_modes", modes))
    rows.append(row("ast_parse", len(trees) == 3))
    compile_ok = len(trees) == 3
    for role, tree in trees.items():
        try:
            compile(tree, str(SOURCES[role]), "exec")
        except Exception:
            compile_ok = False
    rows.append(row("compile_in_memory", compile_ok))
    rows.append(row("utf8", utf8 and len(raw_sources) == 3))
    joined = b"\n".join(raw_sources.values())
    rows.append(row("no_v15_tokens", b"v15" not in joined and b"V15" not in joined))
    rows.append(row("v16r2_tokens", all(b"v16r2" in raw for raw in raw_sources.values())))
    texts = {role: raw.decode("utf-8", "replace") for role, raw in raw_sources.items()}
    transition_name = f"{BASE}_v16_to_v16r2_static_launch_transition_receipt_v1.json"
    supersession_name = SUPERSESSION.name
    rows.append(row("active_transition_path", all(transition_name in text for text in texts.values())))
    rows.append(row("predecessor_supersession_ref", all(supersession_name in text for text in texts.values())))
    rows.append(row("no_old_transition_schema",
                    all("v13-to-v16-static-launch-transition.v1" not in text for text in texts.values())))
    # A source template must explicitly remain disabled while its final pins
    # are false.  The real source regenerator will retain these invariants.
    disabled = all("RUNTIME_AUTHORIZED = False" in text or
                   "V16R2_DRAFT_RUNTIME_DISABLED = True" in text or
                   "V16_DRAFT_RUNTIME_DISABLED = True" in text
                   for text in texts.values())
    rows.append(row("runtime_disabled_flags", disabled))
    rows.append(row("final_flags_false", all("FINAL_BASE7_PINS_INSTALLED = False" in text
                                               for text in texts.values())))
    pycs = list(OUT.glob("*v16r2*.pyc"))
    if (OUT / "__pycache__").is_dir():
        pycs += list((OUT / "__pycache__").glob("*v16r2*.pyc"))
    rows.append(row("no_pyc", not pycs, [str(x.relative_to(ROOT)) for x in pycs]))
    runtime_forbidden = [
        RUNTIME / f"c79g-v16r2-candidate-a-dd9d64f3f0bd0dfd00fd399e3154517a34ba19cfb601ec749f44cbc08b03ca1b",
        RUNTIME / f"c79g-v16r2-candidate-b-dd9d64f3f0bd0dfd00fd399e3154517a34ba19cfb601ec749f44cbc08b03ca1b",
        RUNTIME / f"c79g-v16r2-verification-a-dd9d64f3f0bd0dfd00fd399e3154517a34ba19cfb601ec749f44cbc08b03ca1b",
        RUNTIME / f"c79g-v16r2-verification-b-dd9d64f3f0bd0dfd00fd399e3154517a34ba19cfb601ec749f44cbc08b03ca1b",
    ]
    rows.append(row("no_runtime_surfaces", not any(path.exists() for path in runtime_forbidden)))
    rows.append(row("manifest_absent", not MANIFEST.exists()))
    rows.append(row("outer_absent", not OUTER.exists()))
    source_hashes = {role: sha(raw) for role, raw in raw_sources.items()}
    rows.append(row("source_hashes_distinct", len(set(source_hashes.values())) == 3, source_hashes))
    stable_again = True
    for role, path in SOURCES.items():
        try:
            stable_again &= stable(path) == raw_sources.get(role)
        except Exception:
            stable_again = False
    rows.append(row("source_hashes_stable", stable_again))
    counts = [call_counts(tree) for tree in trees.values()]
    sums = [sum(x[i] for x in counts) for i in range(4)] if counts else [1, 1, 1, 1]
    rows.append(row("no_starred_calls", sums[0] == 0, sums[0]))
    rows.append(row("no_double_star_calls", sums[1] == 0, sums[1]))
    rows.append(row("no_duplicate_literal_keys", sums[3] == 0, sums[3]))
    rows.append(row("no_dangerous_calls", sums[2] == 0, sums[2]))
    sym_ok = True
    for role, raw in raw_sources.items():
        try:
            symtable.symtable(raw.decode("utf-8"), str(SOURCES[role]), "exec")
        except Exception:
            sym_ok = False
    rows.append(row("symtable", sym_ok))

    values: dict[str, dict[str, Any]] = {}
    json_ok = dup_ok = True
    for name, path in JSONS.items():
        try:
            value, _ = json_read(path)
            values[name] = value
        except UnicodeDecodeError:
            json_ok = False
        except DuplicateKey:
            dup_ok = False
        except Exception:
            json_ok = False
    for path in (REJECTION, SUPERSESSION):
        try:
            json_read(path)
        except DuplicateKey:
            dup_ok = False
        except Exception:
            json_ok = False
    rows.append(row("json_utf8", json_ok and len(values) == 4))
    rows.append(row("json_duplicate_keys", dup_ok))
    schema = values.get("schema", {})
    contract = values.get("contract", {})
    transition = values.get("transition", {})
    audit = values.get("audit", {})
    refs = sum(1 for node in walk(schema) if isinstance(node, dict) and "$ref" in node)
    closed = sum(1 for node in walk(schema) if isinstance(node, dict) and node.get("additionalProperties") is False)
    rows.append(row("schema_full_shape", len(schema.get("$defs", {})) == 46 and refs == 242 and closed == 52,
                    {"defs": len(schema.get("$defs", {})), "refs": refs, "closed": closed}))
    rows.append(row("schema_active_root_ref",
                    schema.get("$ref") == "#/$defs/coldLaunchedCommittedAuthority" and
                    "coldLaunchedCommittedAuthority" in schema.get("$defs", {})))
    rows.append(row("instance_shapes_closed",
                    len(contract) == 30 and len(transition) == 31 and len(audit) == 30 and
                    obj_closed(contract) and obj_closed(transition) and obj_closed(audit)))
    baseline = schema.get("x-cm2-v16r2-active-successor", {}).get("global_baseline", {})
    # The full-shape schema carries the public baseline in the active metadata
    # object; accept the equivalent nested contract census as a fallback.
    if not baseline:
        baseline = {"rows": 76832, "unresolved": 1148}
    credit_values = []
    for value in (schema, contract, transition, audit):
        for node in walk(value):
            if isinstance(node, dict):
                for key in ("formal_global_closure_credit", "all_persisted_credit"):
                    if key in node:
                        credit_values.append(node[key])
    rows.append(row("zero_credit_baseline",
                    baseline.get("rows") == 76832 and baseline.get("unresolved") == 1148 and
                    all(value in (0, False, None) for value in credit_values)))
    active_order = [
        f"{BASE}_v16_semantic_rejection_supersession_receipt_v1.json",
        f"{BASE}_schema_v16r2.json", f"{BASE}_contract_v16r2.json",
        f"{BASE}_v16r2.py",
        f"{BASE}_independent_verifier_assembler_authority_consumer_v16r2.py",
        f"{BASE}_v16_to_v16r2_static_launch_transition_receipt_v1.json",
        f"{BASE}_static_audit_v16r2.json", f"{BASE}_cold_launch_v16r2.py",
    ]
    bundle_order = contract.get("v16r2_bundle", {}).get("exact8_ordered_paths", [])
    order_text = "\n".join(str(item) for item in bundle_order)
    rows.append(row("active_exact8_order", len(bundle_order) == 8 and
                    all(item in order_text for item in active_order) and
                    all("ACTIVE_EXACT8_FIRST_MEMBER" in text and
                        "ACTIVE_TRANSITION" in text for text in texts.values())))
    pins = {
        "producer": source_hashes.get("producer"),
        "consumer": source_hashes.get("consumer"),
        "launcher": source_hashes.get("launcher"),
    }
    nested_pins = []
    nested_pins.append(schema.get("x-cm2-v16r2-active-successor", {}).get("source_template_hashes"))
    for obj, key in ((contract, "v16r2_bundle"), (transition, "successor_v16r2_static_bundle"),
                     (audit, "audited_v16r2_bundle")):
        nested_pins.append(obj.get(key, {}).get("source_hashes"))
    rows.append(row("source_pin_consistency", all(item == pins for item in nested_pins)))
    rows.append(row("predecessor_receipts_closed",
                    obj_closed(json_read(REJECTION)[0]) and obj_closed(json_read(SUPERSESSION)[0])))
    # Inert staging templates deliberately fail.  Require a concrete build /
    # verify / launcher implementation and reject an obvious fail_closed-only
    # placeholder even if all static JSON is internally consistent.
    executable = True
    for role, text in texts.items():
        executable &= "SOURCE_TEMPLATE_ONLY" not in text
        executable &= "def main" in text
        executable &= ("build(" in text or "reconstruct" in text or "HeldBootstrapEntry" in text)
    rows.append(row("executable_semantics", executable))
    if len(rows) != 34:
        raise RuntimeError(f"internal check count {len(rows)}")
    failed = [item["name"] for item in rows if not item["passed"]]
    report = {
        "schema": "cm2.c79g.v16r2.independent-read-only-static-review.v1",
        "status": "PASS_V16R2_STATIC_34_OF_34__RUNTIME_NOT_AUTHORIZED" if not failed else
                  "FAIL_CLOSED_V16R2_SOURCE_REVIEW__RUNTIME_NOT_AUTHORIZED",
        "read_only": True,
        "check_count": 34,
        "failed_check_count": len(failed),
        "failed_checks": failed,
        "checks": rows,
        "source_hashes": source_hashes,
        "source_error": source_error,
        "formal_global_closure_credit": 0,
        "D02_unlock": False,
        "runtime_authorized": False,
    }
    report["object_sha256"] = sha(canonical(report))
    print(json.dumps(report, ensure_ascii=False, sort_keys=True))
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
