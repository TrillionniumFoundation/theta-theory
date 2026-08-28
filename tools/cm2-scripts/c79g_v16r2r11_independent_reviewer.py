#!/usr/bin/env python3
"""Read-only 34-check reviewer for the v16r2r11 clean-room.

The reviewer consumes bytes only.  It never imports candidate protocol code,
never writes a receipt/manifest/runtime surface, and treats schema type
definitions separately from concrete zero-credit receipts.  In particular,
``$defs`` may describe the eventual positive authority state (a ``const: 1``
constraint); that is not persisted credit in this disabled staging bundle.
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
SUFFIX = os.environ.get("CM2_SUCCESSOR_SUFFIX", "v16r2r11")
PREDECESSOR_SUFFIX = os.environ.get("CM2_PREDECESSOR_SUFFIX", "v16r2r10")
CHECKPOINT = "dd9d64f3f0bd0dfd00fd399e3154517a34ba19cfb601ec749f44cbc08b03ca1b"
UPSTREAM = "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab"

SOURCES = {
    "producer": OUT / f"{BASE}_{SUFFIX}_semantic_source.py",
    "consumer": OUT / f"{BASE}_independent_verifier_assembler_authority_consumer_{SUFFIX}_semantic_source.py",
    "launcher": OUT / f"{BASE}_cold_launch_{SUFFIX}_semantic_source.py",
}
JSONS = {
    "schema": OUT / f"{BASE}_schema_{SUFFIX}.json",
    "contract": OUT / f"{BASE}_contract_{SUFFIX}.json",
    "transition": OUT / f"{BASE}_{PREDECESSOR_SUFFIX}_to_{SUFFIX}_static_launch_transition_receipt_v1.json",
    "audit": OUT / f"{BASE}_static_audit_{SUFFIX}.json",
}
MANIFEST = OUT / f"{BASE}_cold_launch_manifest_{SUFFIX}.sha256"
OUTER = OUT / f"{BASE}_cold_launch_outer_receipt_{SUFFIX}.json"

CHECK_NAMES = (
    "source_files_present", "source_regular_nlink1", "source_draft_modes",
    "ast_parse", "compile_in_memory", "utf8", "no_v15_tokens",
    "successor_tokens", "active_graph_consensus", "nearest_predecessor_closed",
    "checkpoint_derivation", "no_old_active_transition", "runtime_disabled",
    "final_flags_false", "no_pyc", "no_runtime_surfaces", "manifest_absent",
    "outer_absent", "source_hashes_distinct", "source_hashes_stable",
    "no_starred_calls", "no_double_star_calls", "no_duplicate_literal_keys",
    "no_dangerous_calls", "symtable", "json_closed_utf8", "schema_full_shape",
    "schema_root_ref", "instance_shapes_closed", "zero_credit_baseline",
    "exact8_order", "source_pin_consistency", "predecessor_chain_closed",
    "executable_semantics",
)


class DuplicateKey(ValueError):
    pass


def canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"), allow_nan=False).encode("utf-8")


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
                (before.st_dev, before.st_ino) != (named.st_dev, named.st_ino)):
            raise ValueError(f"identity drift: {path}")
        raw = b"".join(chunks)
        if len(raw) != before.st_size:
            raise ValueError(f"short read: {path}")
        return raw
    finally:
        os.close(fd)


def closed(value: Any) -> bool:
    if not isinstance(value, dict):
        return False
    claim = value.get("object_sha256")
    if not isinstance(claim, str) or len(claim) != 64:
        return False
    body = dict(value)
    body.pop("object_sha256", None)
    return sha(canonical(body)) == claim


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(stable(path).decode("utf-8"),
                       object_pairs_hook=strict_pairs)
    if not isinstance(value, dict):
        raise ValueError(f"not object: {path}")
    return value


def walk(value: Any):
    yield value
    if isinstance(value, dict):
        for child in value.values():
            yield from walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk(child)


def concrete_schema_walk(value: dict[str, Any]):
    """Walk schema metadata, excluding JSON-Schema type definitions."""
    for key, child in value.items():
        if key == "$defs":
            continue
        yield from walk(child)


def call_counts(tree: ast.AST) -> tuple[int, int, int, int]:
    star = double = danger = duplicate = 0
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            star += sum(isinstance(arg, ast.Starred) for arg in node.args)
            double += sum(item.arg is None for item in node.keywords)
            if isinstance(node.func, ast.Name) and node.func.id in {"eval", "exec", "__import__"}:
                danger += 1
        elif isinstance(node, ast.Dict):
            keys = [key.value for key in node.keys
                    if isinstance(key, ast.Constant) and isinstance(key.value, str)]
            duplicate += len(keys) - len(set(keys))
    return star, double, danger, duplicate


def add(rows: list[dict[str, Any]], name: str, passed: bool,
        detail: Any = None) -> None:
    item: dict[str, Any] = {"name": name, "passed": bool(passed)}
    if detail is not None:
        item["detail"] = detail
    rows.append(item)


def predecessor_path_from_sources(texts: dict[str, str]) -> str | None:
    values = []
    for text in texts.values():
        for line in text.splitlines():
            if line.startswith("ACTIVE_PREDECESSOR_SUPERSESSION =") and '"' in line:
                values.append(line.split('"', 2)[1])
    if not values or len(set(values)) != 1:
        return None
    return values[0]


def resolve_predecessor(name: str | None) -> Path | None:
    if not name:
        return None
    candidate = ROOT / name if "/" in name else OUT / name
    return candidate


def chain_closed(anchor: dict[str, Any], anchor_path: Path) -> bool:
    """Require the immediate r10→r11 and r9→r10 receipts, no skipped anchor."""
    try:
        immediate_path = resolve_predecessor(anchor.get("predecessor_supersession_path"))
        if immediate_path is None:
            return False
        immediate = read_json(immediate_path)
        if not closed(immediate) or immediate.get("predecessor_namespace") != PREDECESSOR_SUFFIX:
            return False
        if immediate.get("successor_namespace") != SUFFIX:
            return False
        if immediate.get("formal_global_closure_credit") != 0 or immediate.get("D02_unlock") is not False:
            return False
        predecessor_rej_path = resolve_predecessor(immediate.get("predecessor_rejection_path"))
        if predecessor_rej_path is None:
            return False
        predecessor_rej = read_json(predecessor_rej_path)
        if not closed(predecessor_rej) or predecessor_rej.get("failed_namespace") != PREDECESSOR_SUFFIX:
            return False
        prior = predecessor_rej.get("predecessor_chain_supersession")
        if not isinstance(prior, dict):
            return False
        prior_path = resolve_predecessor(prior.get("path"))
        if prior_path is None:
            return False
        prior_obj = read_json(prior_path)
        return (closed(prior_obj) and prior_obj.get("predecessor_namespace") == "v16r2r9"
                and prior_obj.get("successor_namespace") == PREDECESSOR_SUFFIX
                and prior_obj.get("formal_global_closure_credit") == 0
                and prior_obj.get("D02_unlock") is False)
    except Exception:
        return False


def main() -> int:
    rows: list[dict[str, Any]] = []
    raw: dict[str, bytes] = {}
    text: dict[str, str] = {}
    trees: dict[str, ast.Module] = {}
    errors: dict[str, str] = {}
    present = all(path.is_file() for path in SOURCES.values())
    add(rows, "source_files_present", present)
    regular = modes = utf8 = True
    for role, path in SOURCES.items():
        try:
            data = stable(path)
            raw[role] = data
            st = path.stat()
            regular &= stat.S_ISREG(st.st_mode) and st.st_nlink == 1
            modes &= stat.S_IMODE(st.st_mode) in {0o644, 0o664}
            text[role] = data.decode("utf-8")
            try:
                trees[role] = ast.parse(text[role], filename=str(path))
            except SyntaxError as exc:
                errors[role] = f"SyntaxError: {exc}"
        except UnicodeDecodeError as exc:
            utf8 = False
            errors[role] = f"UnicodeDecodeError: {exc}"
        except Exception as exc:
            regular = modes = utf8 = False
            errors[role] = f"{type(exc).__name__}: {exc}"
    add(rows, "source_regular_nlink1", regular)
    add(rows, "source_draft_modes", modes)
    add(rows, "ast_parse", len(trees) == 3, errors)
    compile_ok = len(trees) == 3
    for role, tree in trees.items():
        try:
            compile(tree, str(SOURCES[role]), "exec")
        except Exception as exc:
            compile_ok = False
            errors[role] = f"compile: {exc}"
    add(rows, "compile_in_memory", compile_ok)
    add(rows, "utf8", utf8 and len(raw) == 3)
    joined = b"\n".join(raw.values())
    add(rows, "no_v15_tokens", b"v15" not in joined and b"V15" not in joined)
    add(rows, "successor_tokens", all(SUFFIX.encode() in data for data in raw.values()))

    pred_name = predecessor_path_from_sources(text)
    namespaces = []
    for value in text.values():
        for line in value.splitlines():
            if line.startswith("ACTIVE_SUCCESSOR_NAMESPACE =") and '"' in line:
                namespaces.append(line.split('"', 2)[1])
    graph_ok = (pred_name is not None and len(set(namespaces)) == 1 and
                namespaces and namespaces[0].replace("-", "_").endswith(SUFFIX + "_semantic_source") and
                all(pred_name in value for value in text.values()) and
                "_v16_semantic_rejection_supersession_receipt_v1.json" not in pred_name)
    add(rows, "active_graph_consensus", graph_ok,
        {"predecessor": pred_name, "namespaces": namespaces})

    predecessor: dict[str, Any] | None = None
    predecessor_ok = False
    predecessor_path = resolve_predecessor(pred_name)
    try:
        if predecessor_path is None:
            raise ValueError("missing predecessor path")
        predecessor = read_json(predecessor_path)
        predecessor_ok = (closed(predecessor) and
                          predecessor.get("formal_global_closure_credit") == 0 and
                          predecessor.get("D02_unlock") is False)
    except Exception as exc:
        errors["predecessor"] = f"{type(exc).__name__}: {exc}"
    add(rows, "nearest_predecessor_closed", predecessor_ok, errors.get("predecessor"))

    checkpoint_ok = False
    for value in (predecessor or {},):
        if UPSTREAM in json.dumps(value, sort_keys=True) and CHECKPOINT in json.dumps(value, sort_keys=True):
            checkpoint_ok = True
    for path in JSONS.values():
        try:
            value = read_json(path)
            blob = json.dumps(value, sort_keys=True)
            checkpoint_ok |= UPSTREAM in blob and CHECKPOINT in blob
        except Exception:
            pass
    add(rows, "checkpoint_derivation", checkpoint_ok,
        {"upstream": UPSTREAM, "successor": CHECKPOINT})
    add(rows, "no_old_active_transition",
        all("V13_TO_V14" not in value and "v13_to_v14" not in value and
            "V14_TO_V15" not in value for value in text.values()))
    add(rows, "runtime_disabled",
        all("RUNTIME_AUTHORIZED = False" in value and
            "FORMAL_GLOBAL_CLOSURE_CREDIT = 0" in value and
            "D02_UNLOCK = False" in value for value in text.values()))
    add(rows, "final_flags_false",
        all("FINAL_BASE7_PINS_INSTALLED = False" in value for value in text.values()))
    pycs = [str(path.relative_to(ROOT)) for path in OUT.rglob("*.pyc") if SUFFIX in path.name]
    add(rows, "no_pyc", not pycs, pycs)
    forbidden = [RUNTIME / f"c79g-{SUFFIX}-candidate-a-{CHECKPOINT}",
                 RUNTIME / f"c79g-{SUFFIX}-candidate-b-{CHECKPOINT}",
                 RUNTIME / f"c79g-{SUFFIX}-verification-a-{CHECKPOINT}",
                 RUNTIME / f"c79g-{SUFFIX}-verification-b-{CHECKPOINT}"]
    add(rows, "no_runtime_surfaces", not any(path.exists() for path in forbidden))
    add(rows, "manifest_absent", not MANIFEST.exists())
    add(rows, "outer_absent", not OUTER.exists())
    hashes = {role: sha(data) for role, data in raw.items()}
    add(rows, "source_hashes_distinct", len(set(hashes.values())) == 3, hashes)
    stable_again = True
    for role, path in SOURCES.items():
        try:
            stable_again &= stable(path) == raw.get(role)
        except Exception:
            stable_again = False
    add(rows, "source_hashes_stable", stable_again)
    counts = [call_counts(tree) for tree in trees.values()]
    sums = [sum(item[i] for item in counts) for i in range(4)] if counts else [1, 1, 1, 1]
    add(rows, "no_starred_calls", sums[0] == 0, sums[0])
    add(rows, "no_double_star_calls", sums[1] == 0, sums[1])
    add(rows, "no_duplicate_literal_keys", sums[3] == 0, sums[3])
    add(rows, "no_dangerous_calls", sums[2] == 0, sums[2])
    sym_ok = True
    for role, data in raw.items():
        try:
            symtable.symtable(data.decode("utf-8"), str(SOURCES[role]), "exec")
        except Exception:
            sym_ok = False
    add(rows, "symtable", sym_ok)

    values: dict[str, dict[str, Any]] = {}
    json_ok = duplicate_ok = True
    for name, path in JSONS.items():
        try:
            values[name] = read_json(path)
        except DuplicateKey:
            duplicate_ok = False
        except Exception:
            json_ok = False
    add(rows, "json_closed_utf8", json_ok and len(values) == 4 and
        all(closed(value) for value in values.values()))
    schema = values.get("schema", {})
    contract = values.get("contract", {})
    transition = values.get("transition", {})
    audit = values.get("audit", {})
    refs = sum(1 for node in walk(schema) if isinstance(node, dict) and "$ref" in node)
    closed_count = sum(1 for node in walk(schema)
                       if isinstance(node, dict) and node.get("additionalProperties") is False)
    add(rows, "schema_full_shape", len(schema.get("$defs", {})) == 46 and
        refs == 242 and closed_count == 52,
        {"defs": len(schema.get("$defs", {})), "refs": refs, "closed": closed_count})
    add(rows, "schema_root_ref",
        schema.get("$ref") == "#/$defs/coldLaunchedCommittedAuthority" and
        "coldLaunchedCommittedAuthority" in schema.get("$defs", {}))
    add(rows, "instance_shapes_closed",
        len(contract) == 30 and len(transition) == 31 and len(audit) == 30 and
        all(closed(value) for value in (contract, transition, audit)))
    active = schema.get("x-cm2-successor-active", {})
    baseline = active.get("global_baseline", {}) if isinstance(active, dict) else {}
    credit_ok = True
    for name, value in values.items():
        nodes = concrete_schema_walk(value) if name == "schema" else walk(value)
        for node in nodes:
            if isinstance(node, dict):
                for key in ("formal_global_closure_credit", "all_persisted_credit"):
                    if key in node and node[key] not in (0, False, None):
                        credit_ok = False
    add(rows, "zero_credit_baseline",
        baseline.get("rows") == 76832 and baseline.get("unresolved") == 1148 and credit_ok)
    bundle = contract.get(f"{SUFFIX}_bundle", {})
    expected_names = [pred_name or "", JSONS["schema"].name,
                      JSONS["contract"].name, SOURCES["producer"].name,
                      SOURCES["consumer"].name, JSONS["transition"].name,
                      JSONS["audit"].name, SOURCES["launcher"].name]
    expected_paths = [[f"deliverables/{name}" for name in expected_names], expected_names]
    add(rows, "exact8_order", bundle.get("exact8_ordered_paths") in expected_paths,
        {"actual": bundle.get("exact8_ordered_paths"), "expected": expected_paths[0]})
    pins = hashes
    nested = [active.get("source_hashes") if isinstance(active, dict) else None,
              bundle.get("source_hashes"),
              transition.get(f"successor_{SUFFIX}_static_bundle", {}).get("source_hashes"),
              audit.get(f"audited_{SUFFIX}_bundle", {}).get("source_hashes")]
    add(rows, "source_pin_consistency", all(item == pins for item in nested), nested)
    add(rows, "predecessor_chain_closed", predecessor_ok and
        isinstance(predecessor, dict) and chain_closed(predecessor, predecessor_path or ROOT))
    executable = all("SOURCE_TEMPLATE_ONLY" not in value and "def main" in value and
                     ("HeldBootstrapEntry" in value or "reconstruct" in value or "global" in value)
                     for value in text.values())
    add(rows, "executable_semantics", executable)

    # ``duplicate_ok`` is folded into the UTF-8/closure gate without changing
    # the historical 34-check public shape.
    if not duplicate_ok:
        rows[-9]["passed"] = False  # json_closed_utf8 row
    if len(rows) != 34:
        raise RuntimeError(f"internal check count {len(rows)}")
    failed = [item["name"] for item in rows if not item["passed"]]
    report: dict[str, Any] = {
        "schema": "cm2.c79g.successor.v16r2r11-independent-read-only-review.v1",
        "successor_suffix": SUFFIX,
        "predecessor_suffix": PREDECESSOR_SUFFIX,
        "status": "PASS_DUAL_STATIC_CANDIDATE_34_OF_34__RUNTIME_NOT_AUTHORIZED" if not failed
                  else "FAIL_CLOSED_SUCCESSOR_REVIEW__RUNTIME_NOT_AUTHORIZED",
        "read_only": True, "check_count": 34,
        "failed_check_count": len(failed), "failed_checks": failed,
        "checks": rows, "source_hashes": hashes,
        "formal_global_closure_credit": 0, "D02_unlock": False,
        "runtime_authorized": False,
    }
    report["object_sha256"] = sha(canonical(report))
    print(json.dumps(report, ensure_ascii=False, sort_keys=True))
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
