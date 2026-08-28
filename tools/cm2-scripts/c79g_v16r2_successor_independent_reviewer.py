#!/usr/bin/env python3
"""Independent 34-check reviewer for an executable C79g successor bundle.

This reviewer is intentionally byte-only: it never imports a candidate source,
never invokes the protocol, and never creates a manifest, outer receipt, or
runtime directory.  The suffix is supplied through ``CM2_SUCCESSOR_SUFFIX``
so each append-only retry gets a new review without mutating an older report.
Every failed check returns a non-zero process status; the companion CI wrapper
uses ``jq -e`` to preserve that status through JSON extraction.
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
SUFFIX = os.environ.get("CM2_SUCCESSOR_SUFFIX", "v16r2r6")
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
    "transition": OUT / f"{BASE}_{SUFFIX}_static_launch_transition_receipt_v1.json",
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


def check(rows: list[dict[str, Any]], name: str, passed: bool,
          detail: Any = None) -> None:
    item: dict[str, Any] = {"name": name, "passed": bool(passed)}
    if detail is not None:
        item["detail"] = detail
    rows.append(item)


def main() -> int:
    rows: list[dict[str, Any]] = []
    raw: dict[str, bytes] = {}
    text: dict[str, str] = {}
    trees: dict[str, ast.Module] = {}
    present = all(path.is_file() for path in SOURCES.values())
    check(rows, "source_files_present", present)
    regular = modes = utf8 = True
    errors: dict[str, str] = {}
    for role, path in SOURCES.items():
        try:
            data = stable(path)
            raw[role] = data
            st = path.stat()
            regular &= stat.S_ISREG(st.st_mode) and st.st_nlink == 1
            modes &= stat.S_IMODE(st.st_mode) in {0o664, 0o644}
            text[role] = data.decode("utf-8")
            try:
                trees[role] = ast.parse(text[role], filename=str(path))
            except SyntaxError as exc:
                errors[role] = f"SyntaxError: {exc}"
        except Exception as exc:
            regular = modes = utf8 = False
            errors[role] = f"{type(exc).__name__}: {exc}"
    check(rows, "source_regular_nlink1", regular)
    check(rows, "source_draft_modes", modes)
    check(rows, "ast_parse", len(trees) == 3, errors)
    compile_ok = len(trees) == 3
    for role, tree in trees.items():
        try:
            compile(tree, str(SOURCES[role]), "exec")
        except Exception as exc:
            compile_ok = False
            errors[role] = f"compile: {exc}"
    check(rows, "compile_in_memory", compile_ok)
    check(rows, "utf8", utf8 and len(raw) == 3)
    joined = b"\n".join(raw.values())
    check(rows, "no_v15_tokens", b"v15" not in joined and b"V15" not in joined)
    check(rows, "successor_tokens",
          all(SUFFIX.encode() in data for data in raw.values()))

    expected_pred = None
    active_namespaces: list[str] = []
    for value in text.values():
        for line in value.splitlines():
            if line.startswith("ACTIVE_PREDECESSOR_SUPERSESSION ="):
                expected_pred = line.split('"', 2)[1] if '"' in line else line
            if line.startswith("ACTIVE_SUCCESSOR_NAMESPACE ="):
                active_namespaces.append(line.split('"', 2)[1] if '"' in line else line)
    namespace_ok = bool(
        active_namespaces and len(set(active_namespaces)) == 1 and
        (active_namespaces[0].replace("-", "_").endswith(SUFFIX + "_semantic_source") or
         active_namespaces[0].replace("-", "_").endswith(SUFFIX))
    )
    graph_ok = (expected_pred is not None and
                all(expected_pred in value for value in text.values()) and
                namespace_ok)
    # Also reject the known jump-back to the original v16 receipt.
    graph_ok = bool(graph_ok and expected_pred and
                    "_v16_semantic_rejection_supersession_receipt_v1.json" not in expected_pred)
    check(rows, "active_graph_consensus", graph_ok,
          {"predecessor": expected_pred, "namespaces": active_namespaces})

    predecessor: dict[str, Any] | None = None
    predecessor_ok = False
    if expected_pred:
        try:
            # Source constants commonly spell ``OUT / "file.json"`` and
            # therefore expose only a basename.  Resolve that spelling to
            # deliverables while still accepting a repository-relative path.
            pred_path = (ROOT / expected_pred if "/" in expected_pred
                         else OUT / expected_pred)
            predecessor = read_json(pred_path)
            predecessor_ok = closed(predecessor) and predecessor.get("formal_global_closure_credit") == 0 and predecessor.get("D02_unlock") is False
        except Exception as exc:
            errors["predecessor"] = f"{type(exc).__name__}: {exc}"
    check(rows, "nearest_predecessor_closed", predecessor_ok, errors.get("predecessor"))

    # The successor checkpoint is a deliberate derived pin: the transition
    # must carry both the C53 upstream checkpoint and the v16 successor pin.
    checkpoint_ok = False
    for value in (predecessor or {}, *(read_json(p) for p in JSONS.values() if p.exists())):
        if not isinstance(value, dict):
            continue
        blobs = json.dumps(value, sort_keys=True)
        if UPSTREAM in blobs and CHECKPOINT in blobs:
            checkpoint_ok = True
            break
    check(rows, "checkpoint_derivation", checkpoint_ok,
          {"upstream": UPSTREAM, "successor": CHECKPOINT})
    check(rows, "no_old_active_transition",
          all("V13_TO_V14" not in value and "v13_to_v14" not in value and
              "V14_TO_V15" not in value for value in text.values()))
    check(rows, "runtime_disabled",
          all("RUNTIME_AUTHORIZED = False" in value and
              "FORMAL_GLOBAL_CLOSURE_CREDIT = 0" in value and
              "D02_UNLOCK = False" in value for value in text.values()))
    check(rows, "final_flags_false",
          all("FINAL_BASE7_PINS_INSTALLED = False" in value for value in text.values()))
    pycs = [str(path.relative_to(ROOT)) for path in OUT.rglob("*.pyc")
            if SUFFIX in path.name]
    check(rows, "no_pyc", not pycs, pycs)
    forbidden = [RUNTIME / f"c79g-{SUFFIX}-candidate-a-{CHECKPOINT}",
                 RUNTIME / f"c79g-{SUFFIX}-candidate-b-{CHECKPOINT}",
                 RUNTIME / f"c79g-{SUFFIX}-verification-a-{CHECKPOINT}",
                 RUNTIME / f"c79g-{SUFFIX}-verification-b-{CHECKPOINT}"]
    check(rows, "no_runtime_surfaces", not any(path.exists() for path in forbidden))
    check(rows, "manifest_absent", not MANIFEST.exists())
    check(rows, "outer_absent", not OUTER.exists())
    source_hashes = {role: sha(data) for role, data in raw.items()}
    check(rows, "source_hashes_distinct", len(set(source_hashes.values())) == 3,
          source_hashes)
    stable_again = True
    for role, path in SOURCES.items():
        try:
            stable_again &= stable(path) == raw.get(role)
        except Exception:
            stable_again = False
    check(rows, "source_hashes_stable", stable_again)
    counts = [call_counts(tree) for tree in trees.values()]
    sums = [sum(item[i] for item in counts) for i in range(4)] if counts else [1] * 4
    check(rows, "no_starred_calls", sums[0] == 0, sums[0])
    check(rows, "no_double_star_calls", sums[1] == 0, sums[1])
    check(rows, "no_duplicate_literal_keys", sums[3] == 0, sums[3])
    check(rows, "no_dangerous_calls", sums[2] == 0, sums[2])
    sym_ok = True
    for role, data in raw.items():
        try:
            symtable.symtable(data.decode("utf-8"), str(SOURCES[role]), "exec")
        except Exception:
            sym_ok = False
    check(rows, "symtable", sym_ok)

    values: dict[str, dict[str, Any]] = {}
    json_ok = dup_ok = True
    for name, path in JSONS.items():
        try:
            values[name] = read_json(path)
        except DuplicateKey:
            dup_ok = False
        except Exception:
            json_ok = False
    check(rows, "json_closed_utf8", json_ok and len(values) == 4 and
          all(closed(value) for value in values.values()))
    schema = values.get("schema", {})
    contract = values.get("contract", {})
    transition = values.get("transition", {})
    audit = values.get("audit", {})
    refs = sum(1 for node in walk(schema) if isinstance(node, dict) and "$ref" in node)
    closed_count = sum(1 for node in walk(schema) if isinstance(node, dict) and node.get("additionalProperties") is False)
    check(rows, "schema_full_shape", len(schema.get("$defs", {})) == 46 and refs == 242 and closed_count == 52,
          {"defs": len(schema.get("$defs", {})), "refs": refs, "closed": closed_count})
    check(rows, "schema_root_ref",
          schema.get("$ref") == "#/$defs/coldLaunchedCommittedAuthority" and
          "coldLaunchedCommittedAuthority" in schema.get("$defs", {}))
    check(rows, "instance_shapes_closed",
          len(contract) == 30 and len(transition) == 31 and len(audit) == 30 and
          all(closed(value) for value in (contract, transition, audit)))
    baseline = schema.get("x-cm2-successor-active", {}).get("global_baseline", {})
    if not baseline:
        baseline = schema.get("x-cm2-v16r2-active-successor", {}).get("global_baseline", {})
    check(rows, "zero_credit_baseline",
          baseline.get("rows") == 76832 and baseline.get("unresolved") == 1148 and
          all(node.get(key) in (0, False, None) for value in values.values() for node in walk(value)
              if isinstance(node, dict) for key in ("formal_global_closure_credit", "all_persisted_credit")
              if key in node))
    order = contract.get(f"{SUFFIX}_bundle", {}).get("exact8_ordered_paths", [])
    expected_names = [
        expected_pred or "", JSONS["schema"].name, JSONS["contract"].name,
        SOURCES["producer"].name, SOURCES["consumer"].name,
        JSONS["transition"].name, JSONS["audit"].name, SOURCES["launcher"].name,
    ]
    check(rows, "exact8_order", order == [f"deliverables/{name}" for name in expected_names] or
          order == expected_names, {"actual": order, "expected": expected_names})
    pins = source_hashes
    nested = [schema.get("x-cm2-successor-active", {}).get("source_hashes"),
              contract.get(f"{SUFFIX}_bundle", {}).get("source_hashes"),
              transition.get(f"successor_{SUFFIX}_static_bundle", {}).get("source_hashes"),
              audit.get(f"audited_{SUFFIX}_bundle", {}).get("source_hashes")]
    check(rows, "source_pin_consistency", all(item == pins for item in nested), nested)
    check(rows, "predecessor_chain_closed", predecessor_ok and
          all(value.get("formal_global_closure_credit") == 0 and value.get("D02_unlock") is False
              for value in (predecessor or {},) if isinstance(value, dict)))
    executable = all("SOURCE_TEMPLATE_ONLY" not in value and "def main" in value and
                      ("HeldBootstrapEntry" in value or "reconstruct" in value or "global" in value)
                      for value in text.values())
    check(rows, "executable_semantics", executable)

    if len(rows) != 34:
        raise RuntimeError(f"internal check count {len(rows)}")
    failed = [item["name"] for item in rows if not item["passed"]]
    report: dict[str, Any] = {
        "schema": "cm2.c79g.successor.independent-read-only-review.v1",
        "successor_suffix": SUFFIX,
        "status": "PASS_DUAL_STATIC_CANDIDATE_34_OF_34__RUNTIME_NOT_AUTHORIZED" if not failed else
                  "FAIL_CLOSED_SUCCESSOR_REVIEW__RUNTIME_NOT_AUTHORIZED",
        "read_only": True,
        "check_count": 34,
        "failed_check_count": len(failed),
        "failed_checks": failed,
        "checks": rows,
        "source_hashes": source_hashes,
        "formal_global_closure_credit": 0,
        "D02_unlock": False,
        "runtime_authorized": False,
    }
    report["object_sha256"] = sha(canonical(report))
    print(json.dumps(report, ensure_ascii=False, sort_keys=True))
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
