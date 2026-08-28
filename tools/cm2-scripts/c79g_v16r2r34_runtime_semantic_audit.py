#!/usr/bin/env python3
"""Independent read-only r34 runtime/path semantic audit.

This append-only audit composes the r34 full-path checker with the remaining
source-level gates from the preceding semantic audit.  It never imports a
candidate as a protocol and never writes a receipt, manifest, outer, runtime
surface, or credit.  ``CM2_SUCCESSOR_SUFFIX``/``CM2_PREDECESSOR_SUFFIX`` are
the only namespace selectors; defaults are ``v16r2r34``/``v16r2r33``.
"""
from __future__ import annotations

import ast
import contextlib
import importlib.util
import io
import json
import hashlib
import os
import re
import stat
import sys
from pathlib import Path
from typing import Any

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "deliverables"
BASE = "cm2_round306c79g_true_global_no_producer_consumer"
TAG = os.environ.get("CM2_SUCCESSOR_SUFFIX", "v16r2r34")
PREV = os.environ.get("CM2_PREDECESSOR_SUFFIX", "v16r2r33")
B58 = "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab"
DD9 = "dd9d64f3f0bd0dfd00fd399e3154517a34ba19cfb601ec749f44cbc08b03ca1b"
HEX = re.compile(r"^[0-9a-f]{64}$")


def canon(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"), allow_nan=False).encode("utf-8")


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def stable(path: Path) -> bytes:
    fd = os.open(path, os.O_RDONLY | os.O_CLOEXEC |
                 getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(fd)
        named = os.lstat(path)
        if (not stat.S_ISREG(before.st_mode) or before.st_nlink != 1 or
                (before.st_dev, before.st_ino, before.st_size) !=
                (named.st_dev, named.st_ino, named.st_size)):
            raise RuntimeError(f"unstable:{path}")
        chunks: list[bytes] = []
        while True:
            block = os.read(fd, 1 << 20)
            if not block:
                break
            chunks.append(block)
        after = os.fstat(fd)
        named_after = os.lstat(path)
        if ((before.st_dev, before.st_ino, before.st_size) !=
                (after.st_dev, after.st_ino, after.st_size) or
                (before.st_dev, before.st_ino) !=
                (named_after.st_dev, named_after.st_ino)):
            raise RuntimeError(f"drift:{path}")
        return b"".join(chunks)
    finally:
        os.close(fd)


def load_checker() -> Any:
    """Load the focused full-path checker without entering its CLI branch."""
    path = ROOT / "scripts/c79g_v16r2r34_path_successor_checker.py"
    spec = importlib.util.spec_from_file_location("_r34_path_checker", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("path-checker-loader")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def source_paths() -> dict[str, Path]:
    return {
        "producer": OUT / f"{BASE}_{TAG}_semantic_source.py",
        "consumer": OUT / (
            f"{BASE}_independent_verifier_assembler_authority_consumer_"
            f"{TAG}_semantic_source.py"),
        "launcher": OUT / f"{BASE}_cold_launch_{TAG}_semantic_source.py",
    }


def json_paths() -> dict[str, Path]:
    return {
        "contract": OUT / f"{BASE}_contract_{TAG}.json",
        "transition": OUT / (
            f"{BASE}_{PREV}_to_{TAG}_static_launch_transition_receipt_v1.json"),
        "audit": OUT / f"{BASE}_static_audit_{TAG}.json",
    }


def anchor_path() -> Path:
    return OUT / f"{BASE}_{TAG}_active_predecessor_supersession_receipt_v1.json"


def execute_defs(path: Path, role: str) -> dict[str, Any]:
    text = stable(path).decode("utf-8")
    tree = ast.parse(text, filename=str(path), mode="exec")
    compile(tree, str(path), "exec")
    ns: dict[str, Any] = {"__name__": f"_r34_semantic_{role}",
                          "__file__": str(path), "__package__": None}
    env_name = "CM2_C79G_V16R2_COLD_WORKSPACE_ROOT"
    old_root = os.environ.get(env_name)
    old_py = os.environ.get("PYTHONDONTWRITEBYTECODE")
    os.environ[env_name] = str(ROOT)
    os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
    try:
        exec(compile(tree, str(path), "exec"), ns, ns)
    finally:
        if old_root is None:
            os.environ.pop(env_name, None)
        else:
            os.environ[env_name] = old_root
        if old_py is None:
            os.environ.pop("PYTHONDONTWRITEBYTECODE", None)
        else:
            os.environ["PYTHONDONTWRITEBYTECODE"] = old_py
    if role == "launcher":
        configure = ns.get("configure_workspace_paths")
        if not callable(configure):
            raise RuntimeError("launcher-configurator-missing")
        configure(ROOT)
    return ns


def launcher_function_census(path: Path, anchor_file: str,
                             anchor_object: str) -> dict[str, Any]:
    tree = ast.parse(stable(path).decode("utf-8"), filename=str(path), mode="exec")
    funcs = [node for node in tree.body if isinstance(node, ast.FunctionDef)
             and node.name == "configure_workspace_paths"]
    if len(funcs) != 1:
        raise RuntimeError(f"launcher-configurator-count:{len(funcs)}")
    fn = funcs[0]
    required = {
        "ACTIVE_SUCCESSOR_NAMESPACE", "ACTIVE_SUCCESSOR_NAMESPACE_TAG",
        "ACTIVE_PREDECESSOR_SUPERSESSION_FILE_PIN",
        "ACTIVE_PREDECESSOR_SUPERSESSION_OBJECT_PIN",
    }
    globals_seen = {name for node in fn.body if isinstance(node, ast.Global)
                    for name in node.names}
    stores = {name: 0 for name in required}
    literals: dict[str, Any] = {}
    for node in ast.walk(fn):
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
            if node.id in stores:
                stores[node.id] += 1
        if (isinstance(node, ast.Assign) and len(node.targets) == 1 and
                isinstance(node.targets[0], ast.Name) and
                isinstance(node.value, ast.Constant)):
            literals[node.targets[0].id] = node.value.value
    if not required <= globals_seen or any(v != 1 for v in stores.values()):
        raise RuntimeError(f"launcher-rebind-shape:{globals_seen}:{stores}")
    expected = {
        "ACTIVE_SUCCESSOR_NAMESPACE": f"{TAG}_semantic_source",
        "ACTIVE_SUCCESSOR_NAMESPACE_TAG": f"{TAG}-semantic-regeneration",
        # These are the active anchor's own immutable file/object pins, not
        # the nested predecessor-supersession witness fields.
        "ACTIVE_PREDECESSOR_SUPERSESSION_FILE_PIN": anchor_file,
        "ACTIVE_PREDECESSOR_SUPERSESSION_OBJECT_PIN": anchor_object,
    }
    if any(literals.get(k) != v for k, v in expected.items()):
        raise RuntimeError(f"launcher-rebind-literals:{literals}")
    return {"globals": sorted(required), "stores": stores, "values": expected}


def main() -> int:
    checks: list[dict[str, Any]] = []

    def check(name: str, ok: bool, detail: Any = None) -> None:
        row: dict[str, Any] = {"name": name, "passed": bool(ok)}
        if detail is not None:
            row["detail"] = detail
        checks.append(row)

    try:
        # Run the full canonical path/successor checker in-process with the
        # requested dynamic suffixes.  It is read-only and returns a closed
        # JSON report on both PASS and FAIL.
        os.environ["CM2_SUCCESSOR_SUFFIX"] = TAG
        os.environ["CM2_PREDECESSOR_SUFFIX"] = PREV
        focused = load_checker()
        capture = io.StringIO()
        with contextlib.redirect_stdout(capture):
            focused_rc = focused.main()
        lines = [line for line in capture.getvalue().splitlines() if line.strip()]
        focused_report = json.loads(lines[-1]) if lines else {
            "status": "NO_FOCUSED_REPORT", "failed_check_count": 1}
        check("focused_full_path_successor_checker", focused_rc == 0 and
              focused_report.get("status", "").startswith("PASS_"),
              {"return_code": focused_rc,
               "status": focused_report.get("status"),
               "failed_check_count": focused_report.get("failed_check_count")})

        src = source_paths()
        jpaths = json_paths()
        ap = anchor_path()
        if any(not p.is_file() for p in [*src.values(), *jpaths.values(), ap]):
            raise RuntimeError("r34-audit-member-missing")
        anchor_raw = stable(ap)
        anchor = json.loads(anchor_raw.decode("utf-8"))
        anchor_file = sha(anchor_raw)
        anchor_object = anchor.get("object_sha256")
        if not isinstance(anchor_object, str):
            raise RuntimeError("r34-anchor-object-pin")

        modules = {role: execute_defs(path, role) for role, path in src.items()}
        check("source_ast_definition_smoke", True)
        pin_results = {
            role: ns.get("UPSTREAM_CHECKPOINT_OBJECT_PIN") == B58 and
            ns.get("SUCCESSOR_CHECKPOINT_OBJECT_PIN") == DD9 and
            ns.get("CHECKPOINT_OBJECT_PIN") == DD9 and
            ns.get("CHECKPOINT", B58) == B58
            for role, ns in modules.items()
        }
        check("source_effective_b58_successor_dd9_roles",
              all(pin_results.values()), pin_results)

        edge = f"{BASE}_{PREV}_to_{TAG}_static_launch_transition_receipt_v1.json"
        anchor_name = f"{BASE}_{TAG}_active_predecessor_supersession_receipt_v1.json"
        census: dict[str, dict[str, Any]] = {}
        for role, path in src.items():
            text = stable(path).decode("utf-8")
            edges = re.findall(rf"{re.escape(BASE)}_v16r2r\d+_to_v16r2r\d+_static_launch_transition_receipt_v1\.json", text)
            anchors = re.findall(rf"{re.escape(BASE)}_v16r2r\d+_active_predecessor_supersession_receipt_v1\.json", text)
            census[role] = {
                "edge_exact": bool(edges) and all(item == edge for item in edges),
                "anchor_exact": bool(anchors) and all(item == anchor_name for item in anchors),
                "successor_load_absent": not any(
                    isinstance(node, ast.Name) and node.id == "CHECKPOINT_OBJECT_PIN" and
                    isinstance(node.ctx, ast.Load)
                    for node in ast.walk(ast.parse(text))),
                "semantic_source_runtime_absent": (
                    "c79g-v16r2-semantic-source-candidate-" not in text and
                    "c79g-v16r2-semantic-source-rejections-" not in text),
            }
        check("source_active_edge_anchor_census", all(all(row.values())
              for row in census.values()), census)

        launcher_census = launcher_function_census(src["launcher"],
                                                   anchor_file, anchor_object)
        check("launcher_function_namespace_tag_and_anchor_rebind", True,
              launcher_census)

        # The checker above verifies exact_publication_paths, cold aliases,
        # exact8/exact10, effective fields and explicit dd9 recursively.  Keep
        # a compact duplicate witness in this report so a guard can consume a
        # single r34 object without trusting a textual status string.
        json_values: dict[str, Any] = {}
        for name, path in jpaths.items():
            raw = stable(path)
            value = json.loads(raw.decode("utf-8"))
            claim = value.get("object_sha256")
            body = dict(value)
            body.pop("object_sha256", None)
            json_values[name] = {
                "object_closed": isinstance(claim, str) and HEX.fullmatch(claim) is not None and
                sha(canon(body)) == claim,
                "effective_b58": all(item == B58 for item in _effective(value)),
                "successor_dd9": bool(_successor(value)) and
                all(item == DD9 for item in _successor(value)),
            }
        check("active_json_closure_effective_and_successor", all(
            all(row.values()) for row in json_values.values()), json_values)

        tag_pyc = [str(path.relative_to(ROOT)) for path in ROOT.rglob("*.pyc")
                   if TAG in str(path)]
        check("no_r34_pyc", not tag_pyc, tag_pyc)
        check("manifest_outer_absent", not (OUT / f"{BASE}_cold_launch_manifest_{TAG}.sha256").exists() and
              not (OUT / f"{BASE}_cold_launch_outer_receipt_{TAG}.json").exists())

        passed = all(row["passed"] for row in checks)
        report: dict[str, Any] = {
            "schema": f"cm2.c79g.{TAG}.runtime-semantic-audit.v1",
            "status": ("PASS_R34_CURRENT_PATH_CHECKPOINT_AND_TRUST_AUDIT__ZERO_CREDIT"
                        if passed else
                        "FAIL_CLOSED_R34_CURRENT_PATH_CHECKPOINT_AND_TRUST_AUDIT"),
            "successor_suffix": TAG, "predecessor_suffix": PREV,
            "focused_report": focused_report,
            "checks": checks, "check_count": len(checks),
            "failed_check_count": sum(not row["passed"] for row in checks),
            "formal_global_closure_credit": 0, "D02_unlock": False,
            "runtime_authorized": False, "read_only": True,
        }
        report["object_sha256"] = sha(canon(report))
        print(json.dumps(report, ensure_ascii=False, sort_keys=True))
        return 0 if passed else 1
    except Exception as exc:
        report = {
            "schema": f"cm2.c79g.{TAG}.runtime-semantic-audit.v1",
            "status": "FAIL_CLOSED_R34_CURRENT_PATH_CHECKPOINT_AND_TRUST_AUDIT_EXCEPTION",
            "error": f"{type(exc).__name__}: {exc}",
            "formal_global_closure_credit": 0, "D02_unlock": False,
            "runtime_authorized": False, "read_only": True,
        }
        report["object_sha256"] = sha(canon(report))
        print(json.dumps(report, ensure_ascii=False, sort_keys=True))
        return 1


def _effective(value: Any) -> list[Any]:
    found: list[Any] = []
    if isinstance(value, dict):
        for key, child in value.items():
            if (isinstance(key, str) and
                    ("effective_checkpoint" in key or
                     "post_seal_effective" in key)):
                found.append(child)
            found.extend(_effective(child))
    elif isinstance(value, list):
        for child in value:
            found.extend(_effective(child))
    return found


def _successor(value: Any) -> list[Any]:
    found: list[Any] = []
    if isinstance(value, dict):
        for key, child in value.items():
            if key == "successor_checkpoint_object_sha256":
                found.append(child)
            found.extend(_successor(child))
    elif isinstance(value, list):
        for child in value:
            found.extend(_successor(child))
    return found


if __name__ == "__main__":
    raise SystemExit(main())
