#!/usr/bin/env python3
"""Independent B reviewer for the r60 launcher registry helper.

Unlike reviewer A, this implementation canonicalizes the extracted helper
lexically before reparsing it, then invokes only the frozen *checker
algorithms* in an inert namespace for the structural/mutation census.  It is
read-only and emits one deterministic closed report.
"""
from __future__ import annotations

import ast
import hashlib
import json
import os
import re
import stat
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "deliverables"
BASE = "cm2_round306c79g_true_global_no_producer_consumer"
TAG = "v16r2r60"
V15 = OUT / f"{BASE}_cold_launch_v15.py"
CURRENT = OUT / f"{BASE}_cold_launch_{TAG}_semantic_source.py"
PRODUCER = OUT / f"{BASE}_{TAG}_semantic_source.py"
CHECKER = ROOT / "scripts/c79g_v15_checker_census.py"
EXPECTED_CURRENT = "2acf6424fe5ca8c58bc19d28ff9fcf3b9326b7c62e59741adda17e5f8e84392d"
EXPECTED_OLD = "f27a5e8df3308e5b022519929e8f0f64257dcbc35b355fa1537b0169d5604a8c"
EXPECTED_NEUTRAL = "5f82214b873d270ea5d01ac43132c0bf1463b12c3289362a001a7c870952bada"
C53 = ROOT / ".cm2-runtime/cm2-global-authority-heads/predecessor-10fb050d30c92b0f2bdcf85a30d28ff670d8efc0b48104b7f04a63c391967b41.seal"
C53_SHA = "f62483c87df4b6f4a8a2ad8dcf56febbfce9977200ce94a0ad6ce38e736aeeb3"


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canon(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"), allow_nan=False).encode()


def stable(path: Path) -> bytes:
    fd = os.open(path, os.O_RDONLY | os.O_CLOEXEC |
                 getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(fd); named = os.lstat(path)
        if (not stat.S_ISREG(before.st_mode) or before.st_nlink != 1 or
                (before.st_dev, before.st_ino, before.st_size) !=
                (named.st_dev, named.st_ino, named.st_size)):
            raise RuntimeError(f"unstable:{path}")
        chunks = []
        while True:
            b = os.read(fd, 1 << 20)
            if not b: break
            chunks.append(b)
        raw = b"".join(chunks); after = os.fstat(fd); named_after = os.lstat(path)
        if ((before.st_dev, before.st_ino, before.st_size) !=
                (after.st_dev, after.st_ino, after.st_size) or
                (before.st_dev, before.st_ino) !=
                (named_after.st_dev, named_after.st_ino) or
                len(raw) != before.st_size):
            raise RuntimeError(f"identity drift:{path}")
        return raw
    finally:
        os.close(fd)


def helper(text: str) -> tuple[str, ast.FunctionDef]:
    tree = ast.parse(text, mode="exec")
    fn = next((n for n in tree.body if isinstance(n, ast.FunctionDef)
               and n.name == "producer_source_registry_shape_from_ast"), None)
    if fn is None:
        raise RuntimeError("helper missing")
    segment = ast.get_source_segment(text, fn)
    if not segment:
        raise RuntimeError("helper source segment missing")
    return segment, fn


def lexical_neutral(segment: str) -> tuple[str, ast.FunctionDef]:
    # This operates on source text, not AST Constant nodes (reviewer A's
    # algorithm).  The two substitutions are intentionally scope-limited to
    # the already extracted FunctionDef segment.
    out = re.sub(r"producer_(?:v15|v16r2)", "producer_CURRENT", segment)
    out = re.sub(r"current v(?:15|16r2)", "current CURRENT", out)
    tree = ast.parse(out, mode="exec")
    fn = tree.body[0]
    if not isinstance(fn, ast.FunctionDef):
        raise RuntimeError("normalized helper is not FunctionDef")
    return out, fn


def digest(fn: ast.FunctionDef) -> str:
    return sha(ast.dump(fn, annotate_fields=True,
                        include_attributes=False).encode())


def main() -> int:
    old_raw = stable(V15); cur_raw = stable(CURRENT); producer_raw = stable(PRODUCER)
    old_seg, old_fn = helper(old_raw.decode("utf-8"))
    cur_seg, cur_fn = helper(cur_raw.decode("utf-8"))
    old_norm_text, old_norm = lexical_neutral(old_seg)
    cur_norm_text, cur_norm = lexical_neutral(cur_seg)
    # Inertly load the historical checker implementation.  Candidate source
    # remains bytes parsed into AST only; no candidate module is imported.
    ns: dict[str, Any] = {"__name__": "_r59_checker_b", "__file__": str(CHECKER), "__package__": None}
    checker_tree = ast.parse(stable(CHECKER).decode("utf-8"), str(CHECKER), mode="exec")
    exec(compile(checker_tree, str(CHECKER), "exec"), ns, ns)
    current_tree = ast.parse(cur_raw.decode("utf-8"), str(CURRENT), mode="exec")
    producer_tree = ast.parse(producer_raw.decode("utf-8"), str(PRODUCER), mode="exec")
    ns["V15_EXPECTED_LAUNCHER_REGISTRY_HELPER_AST_SHA256"] = EXPECTED_CURRENT
    producer_report = ns["producer_source_registry_census"](producer_tree)
    helper_report = ns["launcher_runtime_registry_helper_census"](
        current_tree, producer_report["computed_closed_registry_key_count"])
    labels = {
        "producer_v16r2": cur_seg.count("producer_v16r2"),
        "current_v16r2": cur_seg.count("current v16r2"),
        "producer_v15": cur_seg.count("producer_v15"),
        "current_v15": cur_seg.count("current v15"),
    }
    mutation_ok = (helper_report.get("in_memory_stale_62_rejected") is True and
                   helper_report.get("in_memory_dead_callsite_rejected") is True)
    compile_ok = True
    try:
        for p in (CURRENT, PRODUCER):
            compile(ast.parse(stable(p).decode("utf-8"), str(p)), str(p), "exec")
    except Exception:
        compile_ok = False
    checks = {
        "old_raw_hash": digest(old_fn) == EXPECTED_OLD,
        "current_raw_hash": digest(cur_fn) == EXPECTED_CURRENT,
        "old_and_current_neutral_hash": digest(old_norm) == EXPECTED_NEUTRAL and digest(cur_norm) == EXPECTED_NEUTRAL,
        "current_labels": labels == {"producer_v16r2": 1, "current_v16r2": 5, "producer_v15": 0, "current_v15": 0},
        "producer_census_matches": producer_report.get("matches") is True and producer_report.get("computed_closed_registry_key_count") == 75,
        "helper_census_matches": helper_report.get("matches") is True,
        "mutation_fail_closed": mutation_ok,
        "candidate_ast_compile": compile_ok,
        "c53_unchanged": sha(stable(C53)) == C53_SHA,
    }
    failed = [k for k, ok in checks.items() if not ok]
    report: dict[str, Any] = {
        "schema": f"cm2.c79g.{TAG}.helper-version-neutral-reviewer-b.v1",
        "reviewer": "B",
        "candidate_namespace": TAG,
        "candidate_launcher_path": str(CURRENT.relative_to(ROOT)),
        "candidate_launcher_file_sha256": sha(cur_raw),
        "helper_function": "producer_source_registry_shape_from_ast",
        "helper_raw_ast_sha256": digest(cur_fn),
        "historical_template_raw_ast_sha256": digest(old_fn),
        "version_neutral_normalization_algorithm": "LEXICAL_FUNCTION_SEGMENT_REGEX_THEN_AST_DUMP_NO_ATTRIBUTES_V1",
        "version_neutral_normalized_helper_ast_sha256": digest(cur_norm),
        "labels": labels,
        "guard_vector": helper_report,
        "producer_census": producer_report,
        "checks": checks,
        "failed_checks": failed,
        "status": "PASS_VERSION_NEUTRAL_HELPER_REVIEW_B__ZERO_CREDIT" if not failed else "FAIL_CLOSED_VERSION_NEUTRAL_HELPER_REVIEW_B",
        "formal_global_closure_credit": 0, "D02_unlock": False,
        "runtime_authorized": False,
    }
    report["object_sha256"] = sha(canon(report))
    print(json.dumps(report, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
