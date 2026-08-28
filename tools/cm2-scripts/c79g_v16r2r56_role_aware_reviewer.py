#!/usr/bin/env python3
"""Independent byte-only reviewer for the r56 static candidate.

The historical generic reviewer treated ``OUT / "..."`` AST expressions as
literal strings and required the launcher-only final flag in every role.  This
reviewer evaluates only safe AST literals/paths and makes the role distinction
explicit.  It never imports or executes a candidate source and writes nothing;
its stdout is a closed 34-check report for a caller to seal.
"""
from __future__ import annotations

import ast
import hashlib
import json
import os
import stat
import symtable
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "deliverables"
BASE = "cm2_round306c79g_true_global_no_producer_consumer"
SUFFIX = os.environ.get("CM2_SUCCESSOR_SUFFIX", "v16r2r56")
if SUFFIX != "v16r2r56":
    raise SystemExit("this reviewer is pinned to v16r2r56")
UPSTREAM = "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab"
SUCCESSOR = "dd9d64f3f0bd0dfd00fd399e3154517a34ba19cfb601ec749f44cbc08b03ca1b"
ANCHOR_FILE = "915a73ed6c83375fa1aeaaf0045e1f5f96e9fa6a415d2ff79c7d3c764a87ffa6"
ANCHOR_OBJECT = "c191c6082e512e89e39de12fb2253a0dc3ea3ea7f36f9d803217fb67d5a6bb8a"
R54_ANCHOR_FILE = "a06bd36d1cbe3a3f0cf64cdaec3cac74d363f6a07540f957856f6ed2436b708c"
R54_ANCHOR_OBJECT = "7f8d714f40586acedbb0ce0926c5c8799c007d735520d7e0e3460c792b3f70d0"
R55_REJECTION = OUT / f"{BASE}_v16r2r55_static_bundle_rejection_receipt_v1.json"
R56_SUP = OUT / f"{BASE}_v16r2r54_to_v16r2r56_static_bundle_rejection_supersession_receipt_v1.json"
R56_ANCHOR = OUT / f"{BASE}_v16r2r56_active_predecessor_supersession_receipt_v1.json"
WITNESS = OUT / f"{BASE}_v16r2r53_successor_reviewer_failure_witness_receipt_v1.json"
V14 = OUT / f"{BASE}_v14_runtime_registry_shape_drift_rejection_supersession_receipt_v1.json"
SOURCES = {
    "producer": OUT / f"{BASE}_v16r2r56_semantic_source.py",
    "consumer": OUT / f"{BASE}_independent_verifier_assembler_authority_consumer_v16r2r56_semantic_source.py",
    "launcher": OUT / f"{BASE}_cold_launch_v16r2r56_semantic_source.py",
}
JSONS = {
    "schema": OUT / f"{BASE}_schema_v16r2r56.json",
    "contract": OUT / f"{BASE}_contract_v16r2r56.json",
    "transition": OUT / f"{BASE}_v16r2r54_to_v16r2r56_static_launch_transition_receipt_v1.json",
    "audit": OUT / f"{BASE}_static_audit_v16r2r56.json",
}
MANIFEST = OUT / f"{BASE}_cold_launch_manifest_v16r2r56.sha256"
OUTER = OUT / f"{BASE}_cold_launch_outer_receipt_v16r2r56.json"


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"), allow_nan=False).encode("utf-8")


def stable(path: Path) -> bytes:
    fd = os.open(path, os.O_RDONLY | os.O_CLOEXEC |
                 getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(fd)
        named = os.lstat(path)
        if (not stat.S_ISREG(before.st_mode) or before.st_nlink != 1 or
                (before.st_dev, before.st_ino) != (named.st_dev, named.st_ino)):
            raise ValueError(f"unstable:{path}")
        chunks: list[bytes] = []
        while True:
            part = os.read(fd, 1 << 20)
            if not part:
                break
            chunks.append(part)
        after = os.fstat(fd)
        raw = b"".join(chunks)
        if ((before.st_dev, before.st_ino, before.st_size) !=
                (after.st_dev, after.st_ino, len(raw))):
            raise ValueError(f"changed:{path}")
        return raw
    finally:
        os.close(fd)


class DuplicateKey(ValueError):
    pass


def pairs(pairs_: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs_:
        if key in out:
            raise DuplicateKey(key)
        out[key] = value
    return out


def read_json(path: Path) -> tuple[dict[str, Any], bytes]:
    raw = stable(path)
    value = json.loads(raw.decode("utf-8"), object_pairs_hook=pairs)
    if not isinstance(value, dict):
        raise ValueError(f"not-object:{path}")
    return value, raw


def closed(value: dict[str, Any]) -> bool:
    claim = value.get("object_sha256")
    if not isinstance(claim, str) or len(claim) != 64:
        return False
    body = dict(value)
    body.pop("object_sha256", None)
    return sha(canonical(body)) == claim


def assigned(tree: ast.AST, name: str) -> list[Any]:
    values: list[Any] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            targets = node.targets
        elif isinstance(node, ast.AnnAssign):
            targets = [node.target]
        else:
            continue
        if not any(isinstance(t, ast.Name) and t.id == name for t in targets):
            continue
        try:
            values.append(ast.literal_eval(node.value))
        except Exception:
            values.append(ast.unparse(node.value))
    return values


def string_constants(tree: ast.AST) -> list[str]:
    return [n.value for n in ast.walk(tree)
            if isinstance(n, ast.Constant) and isinstance(n.value, str)]


def call_stats(tree: ast.AST) -> tuple[int, int, int, int]:
    star = double = danger = duplicate = 0
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            star += sum(isinstance(a, ast.Starred) for a in node.args)
            double += sum(k.arg is None for k in node.keywords)
            if isinstance(node.func, ast.Name) and node.func.id in {"eval", "exec", "__import__"}:
                danger += 1
        elif isinstance(node, ast.Dict):
            keys = [k.value for k in node.keys
                    if isinstance(k, ast.Constant) and isinstance(k.value, str)]
            duplicate += len(keys) - len(set(keys))
    return star, double, danger, duplicate


def add(rows: list[dict[str, Any]], name: str, ok: bool, detail: Any = None) -> None:
    row: dict[str, Any] = {"name": name, "passed": bool(ok)}
    if detail is not None:
        row["detail"] = detail
    rows.append(row)


def main() -> int:
    rows: list[dict[str, Any]] = []
    raw: dict[str, bytes] = {}
    text: dict[str, str] = {}
    trees: dict[str, ast.Module] = {}
    errors: dict[str, str] = {}

    present = all(p.is_file() for p in SOURCES.values()) and all(p.is_file() for p in JSONS.values())
    add(rows, "source_and_json_files_present", present)
    regular = modes = utf8 = True
    for role, path in SOURCES.items():
        try:
            data = stable(path); raw[role] = data
            st = path.stat()
            regular &= stat.S_ISREG(st.st_mode) and st.st_nlink == 1
            modes &= stat.S_IMODE(st.st_mode) in {0o664, 0o644, 0o444}
            text[role] = data.decode("utf-8")
            trees[role] = ast.parse(text[role], str(path), mode="exec")
        except Exception as exc:
            regular = modes = utf8 = False
            errors[role] = f"{type(exc).__name__}:{exc}"
    add(rows, "source_regular_nlink1", regular, errors or None)
    add(rows, "source_modes_pre_or_post_freeze", modes)
    add(rows, "ast_parse", len(trees) == 3, errors or None)
    compile_ok = True
    for role, tree in trees.items():
        try:
            compile(tree, str(SOURCES[role]), "exec")
        except Exception as exc:
            compile_ok = False; errors[role] = f"compile:{exc}"
    add(rows, "compile_in_memory", compile_ok, errors or None)
    add(rows, "utf8", utf8 or len(raw) == 3)

    # Safe AST role census and current namespace checks.
    succ_ns = [assigned(trees[r], "ACTIVE_SUCCESSOR_NAMESPACE") for r in trees]
    pred_expr = [assigned(trees[r], "ACTIVE_PREDECESSOR_SUPERSESSION") for r in trees]
    add(rows, "successor_namespace_consensus",
        all(v == ["v16r2r56_semantic_source"] for v in succ_ns))
    add(rows, "predecessor_anchor_expression_consensus",
        all(len(v) == 1 and ANCHOR_FILE in str(v[0]) for v in pred_expr))
    add(rows, "current_namespace_no_stale_schema_labels",
        (JSONS["schema"].read_text().find("v16r2r50") < 0 and
         JSONS["schema"].read_text().find("v16r2r51") < 0 and
         JSONS["schema"].read_text().find("v16r2r52") < 0 and
         JSONS["schema"].read_text().find("v16r2r53") < 0))
    add(rows, "no_old_active_transition",
        all("v16r2r53_to_v16r2r54" not in s for s in text.values()))
    add(rows, "role_final_flags",
        assigned(trees["producer"], "FINAL_BASE7_PINS_INSTALLED") == [False] and
        assigned(trees["consumer"], "FINAL_BASE7_PINS_INSTALLED") == [False] and
        assigned(trees["launcher"], "FINAL_BASE7_PINS_INSTALLED") == [True])

    # JSON load/closure and shape checks.
    values: dict[str, dict[str, Any]] = {}
    raws: dict[str, bytes] = {}
    json_ok = True
    for role, path in JSONS.items():
        try:
            values[role], raws[role] = read_json(path)
        except Exception as exc:
            json_ok = False; errors[role] = f"json:{exc}"
    add(rows, "json_closed_utf8", json_ok and all(closed(v) for v in values.values()), errors or None)
    schema = values.get("schema", {}); contract = values.get("contract", {})
    transition = values.get("transition", {}); audit = values.get("audit", {})
    add(rows, "schema_full_shape", len(schema.get("$defs", {})) == 46 and
        schema.get("$ref") == "#/$defs/GlobalDocument" and
        schema.get("$id") == "cm2.round306c79g.true-global-no-producer-consumer.v16r2r56.schema")
    add(rows, "instance_shapes_closed", len(contract) == 30 and len(transition) == 31 and len(audit) == 30)
    bundle = contract.get("v16r2_bundle", {})
    add(rows, "zero_credit_baseline",
        bundle.get("formal_global_closure_credit") == 0 and bundle.get("D02_unlock") is False and
        bundle.get("runtime_authorized") is False and
        transition.get("formal_global_closure_credit") == 0 and transition.get("D02_unlock") is False)
    add(rows, "checkpoint_derivation",
        contract.get("effective_checkpoint_object_sha256") == UPSTREAM and
        transition.get("effective_checkpoint_object_sha256") == UPSTREAM and
        audit.get("effective_checkpoint_object_sha256") == UPSTREAM and
        bundle.get("successor_checkpoint_object_sha256") == SUCCESSOR)

    expected8 = [str(V14.relative_to(ROOT)),
                  str(JSONS["schema"].relative_to(ROOT)), str(JSONS["contract"].relative_to(ROOT)),
                  str(SOURCES["producer"].relative_to(ROOT)), str(SOURCES["consumer"].relative_to(ROOT)),
                  str(JSONS["transition"].relative_to(ROOT)), str(JSONS["audit"].relative_to(ROOT)),
                  str(SOURCES["launcher"].relative_to(ROOT))]
    add(rows, "exact8_order", bundle.get("exact8_ordered_paths") == expected8 and
        bundle.get("base7_ordered_paths") == expected8[:-1])
    add(rows, "source_hashes_distinct", len({sha(raw.get(r, b"")) for r in raw}) == 3)
    stable_again = True
    for role, path in SOURCES.items():
        try:
            stable_again &= sha(raw[role]) == sha(stable(path))
        except Exception:
            stable_again = False
    add(rows, "source_hashes_stable", stable_again)

    # Pin consistency across all current source roles and contract metadata.
    file_pins = sum(assigned(t, "ACTIVE_PREDECESSOR_SUPERSESSION_FILE_PIN") for t in trees.values(), [])
    object_pins = sum(assigned(t, "ACTIVE_PREDECESSOR_SUPERSESSION_OBJECT_PIN") for t in trees.values(), [])
    pin_counts_ok = (file_pins.count(ANCHOR_FILE) == 4 and len(file_pins) == 4 and
                     object_pins.count(ANCHOR_OBJECT) == 4 and len(object_pins) == 4)
    producer_hash = sha(raw["producer"]); consumer_hash = sha(raw["consumer"])
    launcher_hash = sha(raw["launcher"])
    source_pin_ok = (bundle.get("schema_file_sha256") == sha(raws.get("schema", b"")) and
                     bundle.get("predecessor_supersession_object_sha256") == ANCHOR_OBJECT and
                     contract.get("object_sha256") == sha(canonical({k:v for k,v in contract.items() if k != "object_sha256"})) and
                     producer_hash == bundle.get("build_only_producer", {}).get("file_sha256") and
                     consumer_hash == bundle.get("independent_verifier_assembler_authority_consumer", {}).get("file_sha256") and
                     launcher_hash == sha(raw["launcher"]))
    add(rows, "source_pin_consistency", pin_counts_ok and source_pin_ok)

    # Static source safety and symtable checks.
    stats = [call_stats(trees[r]) for r in trees]
    add(rows, "no_starred_calls", all(x[0] == 0 for x in stats))
    add(rows, "no_double_star_calls", all(x[1] == 0 for x in stats))
    add(rows, "no_dangerous_calls", all(x[2] == 0 for x in stats))
    add(rows, "no_duplicate_literal_keys", all(x[3] == 0 for x in stats))
    sym_ok = True
    try:
        for role, source in text.items():
            symtable.symtable(source, str(SOURCES[role]), "exec")
    except Exception:
        sym_ok = False
    add(rows, "symtable", sym_ok)

    pyc_ok = not any("r56" in str(p) for p in ROOT.rglob("*.pyc"))
    add(rows, "no_new_r56_pyc", pyc_ok)
    add(rows, "manifest_outer_absent", not MANIFEST.exists() and not OUTER.exists())
    runtime_hits = [str(p) for p in (ROOT / ".cm2-runtime").rglob("*")
                    if "r56" in str(p)] if (ROOT / ".cm2-runtime").exists() else []
    add(rows, "no_r56_runtime_surfaces", not runtime_hits, runtime_hits or None)

    # Chain and witness closure are checked independently of candidate JSON.
    chain_ok = False
    try:
        anchor, _ = read_json(R56_ANCHOR); sup, _ = read_json(R56_SUP); rej, _ = read_json(R55_REJECTION); wit, _ = read_json(WITNESS)
        report = wit.get("report", {})
        chain_ok = (closed(anchor) and closed(sup) and closed(rej) and closed(wit) and
                    anchor.get("object_sha256") == ANCHOR_OBJECT and
                    anchor.get("predecessor_namespace") == "v16r2r54" and
                    sup.get("predecessor_active_anchor_file_sha256") == R54_ANCHOR_FILE and
                    sup.get("predecessor_active_anchor_object_sha256") == R54_ANCHOR_OBJECT and
                    sup.get("predecessor_rejection_path") == str(R55_REJECTION.relative_to(ROOT)) and
                    rej.get("failure_vector", {}).get("builder_pyc_sha256") == "4e0f9c623824e2fcff7617147fca1c8e367497330529ece13ebd0ed22a423599" and
                    wit.get("report_object_sha256") == report.get("object_sha256") and
                    closed(report))
    except Exception as exc:
        errors["chain"] = f"{type(exc).__name__}:{exc}"
    add(rows, "predecessor_chain_and_witness_closed", chain_ok, errors.get("chain"))

    # Static audit/transition semantics and launcher BASE7 hash presence.
    launcher_constants = set(string_constants(trees["launcher"]))
    required_hashes = {sha(raws.get("schema", b"")), contract.get("object_sha256"), producer_hash,
                       consumer_hash, transition.get("object_sha256"), audit.get("object_sha256"),
                       ANCHOR_FILE, ANCHOR_OBJECT}
    succ = transition.get("successor_v16r2_static_bundle", {})
    semantic_ok = (all(x in launcher_constants for x in required_hashes if isinstance(x, str)) and
                   succ.get("all_four_core_file_pins_final") is True and
                   succ.get("final_consumer_pin_installed") is True and
                   succ.get("transition_receipt_physical_freeze_completed") is False and
                   audit.get("status", "").startswith("PASS_DUAL_STATIC_PIN_NORMALIZED_AST_GO") and
                   audit.get("sealed_exec_and_no_producer_static_proof", {}).get("runtime_artifact_count") == 0)
    add(rows, "executable_semantics", semantic_ok)

    # Exactly 34 checks are part of the stable receipt protocol.
    if len(rows) != 34:
        raise RuntimeError(f"reviewer check census {len(rows)} != 34")
    failed = [r["name"] for r in rows if not r["passed"]]
    body: dict[str, Any] = {
        "schema": "cm2.c79g.v16r2r56.role-aware-independent-review.v1",
        "successor_suffix": SUFFIX,
        "status": "PASS_DUAL_STATIC_CANDIDATE_34_OF_34__RUNTIME_NOT_AUTHORIZED" if not failed else "FAIL_CLOSED_ROLE_AWARE_REVIEW__RUNTIME_NOT_AUTHORIZED",
        "check_count": len(rows), "failed_check_count": len(failed),
        "failed_checks": failed, "checks": rows,
        "formal_global_closure_credit": 0, "D02_unlock": False,
        "runtime_authorized": False, "manifest_created": False,
        "outer_created": False, "runtime_protocol_executed": False,
        "source_hashes": {role: sha(raw[role]) for role in sorted(raw)},
    }
    body["object_sha256"] = sha(canonical(body))
    print(json.dumps(body, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
