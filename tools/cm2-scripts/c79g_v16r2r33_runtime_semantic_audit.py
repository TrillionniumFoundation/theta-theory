#!/usr/bin/env python3
"""Read-only r33 current-path and checkpoint semantic audit.

This is an independent clean-room witness for a future r33 static candidate.
It executes only top-level definitions from the three candidate sources in an
isolated namespace and compares the resulting ``Path`` objects with the
contract's canonical ``exact_publication_paths`` map.  It does not import a
protocol, create a receipt, write a runtime surface, or award credit.

The successor/predecessor suffixes are environment parameters so this checker
can be reused for an append-only hop without editing an older audit.  The
effective C53 checkpoint must remain b58; dd9 is accepted only in explicit
successor-chain fields and the source successor constant.
"""
from __future__ import annotations

import ast
import hashlib
import json
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
TAG = os.environ.get("CM2_SUCCESSOR_SUFFIX", "v16r2r33")
PREV = os.environ.get("CM2_PREDECESSOR_SUFFIX", "v16r2r32")
B58 = "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab"
DD9 = "dd9d64f3f0bd0dfd00fd399e3154517a34ba19cfb601ec749f44cbc08b03ca1b"
HEX = re.compile(r"^[0-9a-f]{64}$")
SUFFIX = re.compile(r"^v16r2r[0-9]+$")


class DuplicateKey(ValueError):
    """Raised when a supposedly closed JSON object contains duplicate keys."""


def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in items:
        if key in out:
            raise DuplicateKey(key)
        out[key] = value
    return out


def canon(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"), allow_nan=False).encode("utf-8")


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def stable(path: Path) -> bytes:
    """Read one immutable regular file and bracket it with identity checks."""
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
        raw = b"".join(chunks)
        if len(raw) != before.st_size:
            raise RuntimeError(f"short-read:{path}")
        return raw
    finally:
        os.close(fd)


def load_json(path: Path) -> tuple[dict[str, Any], bytes]:
    raw = stable(path)
    value = json.loads(raw.decode("utf-8"), object_pairs_hook=pairs)
    if not isinstance(value, dict):
        raise RuntimeError(f"json-object-required:{path}")
    claim = value.get("object_sha256")
    if not isinstance(claim, str) or not HEX.fullmatch(claim):
        raise RuntimeError(f"object-pin-missing:{path}")
    body = dict(value)
    body.pop("object_sha256", None)
    if sha(canon(body)) != claim:
        raise RuntimeError(f"object-closure:{path}")
    return value, raw


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
    ns: dict[str, Any] = {
        "__name__": f"_r33_semantic_audit_{role}",
        "__file__": str(path),
        "__package__": None,
    }
    # Candidate producer/consumer sources bind ROOT from this variable at
    # import time.  Pin it for the smoke and restore any caller value.
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


def walk_key(value: Any, wanted: str) -> list[Any]:
    found: list[Any] = []
    if isinstance(value, dict):
        for key, child in value.items():
            if key == wanted:
                found.append(child)
            found.extend(walk_key(child, wanted))
    elif isinstance(value, list):
        for child in value:
            found.extend(walk_key(child, wanted))
    return found


def walk_effective(value: Any) -> list[Any]:
    found: list[Any] = []
    if isinstance(value, dict):
        for key, child in value.items():
            if (isinstance(key, str) and
                    ("effective_checkpoint" in key or
                     "post_seal_effective" in key)):
                found.append(child)
            found.extend(walk_effective(child))
    elif isinstance(value, list):
        for child in value:
            found.extend(walk_effective(child))
    return found


def path_string(value: Any) -> str:
    return str(value) if isinstance(value, (str, Path)) else ""


def launcher_rebind_census(path: Path, anchor_file: str,
                           anchor_object: str) -> dict[str, Any]:
    text = stable(path).decode("utf-8")
    tree = ast.parse(text, filename=str(path), mode="exec")
    funcs = [node for node in tree.body
             if isinstance(node, ast.FunctionDef) and
             node.name == "configure_workspace_paths"]
    required = {
        "ACTIVE_SUCCESSOR_NAMESPACE",
        "ACTIVE_SUCCESSOR_NAMESPACE_TAG",
        "ACTIVE_PREDECESSOR_SUPERSESSION_FILE_PIN",
        "ACTIVE_PREDECESSOR_SUPERSESSION_OBJECT_PIN",
    }
    if len(funcs) != 1:
        raise RuntimeError(f"launcher-configurator-count:{len(funcs)}")
    fn = funcs[0]
    globals_seen = {name for node in fn.body if isinstance(node, ast.Global)
                    for name in node.names}
    stores: dict[str, int] = {name: 0 for name in required}
    literal: dict[str, Any] = {}
    for node in ast.walk(fn):
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
            if node.id in stores:
                stores[node.id] += 1
        if (isinstance(node, ast.Assign) and len(node.targets) == 1 and
                isinstance(node.targets[0], ast.Name) and
                isinstance(node.value, ast.Constant)):
            literal[node.targets[0].id] = node.value.value
    if not required <= globals_seen:
        raise RuntimeError("launcher-configurator-globals")
    if any(stores[name] != 1 for name in required):
        raise RuntimeError(f"launcher-configurator-store-count:{stores}")
    expected = {
        "ACTIVE_SUCCESSOR_NAMESPACE": f"{TAG}_semantic_source",
        "ACTIVE_SUCCESSOR_NAMESPACE_TAG": f"{TAG}-semantic-regeneration",
        # The active source binds the *active anchor file* itself.  The
        # nested predecessor_supersession_* fields describe the prior edge
        # and are not the source's active-anchor pins.
        "ACTIVE_PREDECESSOR_SUPERSESSION_FILE_PIN": anchor_file,
        "ACTIVE_PREDECESSOR_SUPERSESSION_OBJECT_PIN": anchor_object,
    }
    if any(literal.get(key) != value for key, value in expected.items()):
        raise RuntimeError(f"launcher-configurator-literals:{literal}")
    return {"globals": sorted(globals_seen & required), "stores": stores,
            "expected": expected}


def main() -> int:
    checks: list[dict[str, Any]] = []

    def check(name: str, ok: bool, detail: Any = None) -> None:
        row: dict[str, Any] = {"name": name, "passed": bool(ok)}
        if detail is not None:
            row["detail"] = detail
        checks.append(row)

    try:
        check("suffix_parameters", bool(SUFFIX.fullmatch(TAG)) and
              bool(SUFFIX.fullmatch(PREV)), {"tag": TAG, "prev": PREV})
        if not SUFFIX.fullmatch(TAG) or not SUFFIX.fullmatch(PREV):
            raise RuntimeError("invalid-suffix")
        src = source_paths()
        jpaths = json_paths()
        ap = anchor_path()
        all_members = [*src.values(), *jpaths.values(), ap]
        present = {str(p.relative_to(ROOT)): p.is_file() for p in all_members}
        check("members_present", all(present.values()), present)
        if not all(present.values()):
            raise RuntimeError("r33-member-missing")

        values: dict[str, dict[str, Any]] = {}
        raws: dict[str, bytes] = {}
        for name, path in jpaths.items():
            values[name], raws[name] = load_json(path)
        anchor, anchor_raw = load_json(ap)
        check("json_object_closure", True)
        check("anchor_chain_roles", anchor.get("upstream_checkpoint_object_sha256") == B58 and
              anchor.get("successor_checkpoint_object_sha256") == DD9 and
              anchor.get("predecessor_namespace") == PREV and
              anchor.get("successor_namespace") == f"{TAG}_semantic_source",
              {key: anchor.get(key) for key in
               ("predecessor_namespace", "successor_namespace",
                "upstream_checkpoint_object_sha256",
                "successor_checkpoint_object_sha256")})

        contract = values["contract"]
        expected = contract.get("exact_publication_paths")
        if not isinstance(expected, dict):
            raise RuntimeError("contract-exact-publication-paths-missing")
        expected_abs = {key: ROOT / value for key, value in expected.items()
                        if isinstance(value, str) and value.startswith(".")}
        required = {
            "candidate_A", "candidate_B", "verification_A", "verification_B",
            "committed_completion", "authority_seal", "v16r2_rejection_namespace",
            "v16r2_later_rejection", "candidate_staging_path_template",
            "verification_staging_path_template", "completion_staging_path",
            "authority_staging_path",
        }
        check("contract_canonical_runtime_keyset", required <= set(expected_abs),
              {"missing": sorted(required - set(expected_abs))})
        if not required <= set(expected_abs):
            raise RuntimeError("contract-canonical-keyset")
        aliases: dict[str, bool] = {}
        for old, new in (("v15_later_rejection", "v16r2_later_rejection"),
                         ("v15_rejection_namespace", "v16r2_rejection_namespace")):
            if old in expected_abs:
                aliases[old] = expected_abs[old] == expected_abs[new]
        check("legacy_runtime_aliases_canonical", all(aliases.values()), aliases)
        bad_current = {
            key: str(expected[key]) for key in required
            if DD9 in str(expected[key]) or "semantic-source" in str(expected[key])
        }
        check("contract_current_paths_b58_and_nonsemantic", not bad_current,
              bad_current)

        modules = {role: execute_defs(path, role) for role, path in src.items()}
        check("ast_compile_and_definition_smoke", True)

        producer = modules["producer"]
        producer_result = {
            "candidate_A": producer.get("CANDIDATE_A") == expected_abs["candidate_A"],
            "candidate_B": producer.get("CANDIDATE_B") == expected_abs["candidate_B"],
        }
        check("producer_current_paths_match_contract",
              all(producer_result.values()), producer_result)

        consumer = modules["consumer"]
        consumer_map = {
            "candidate_A": "CANDIDATE_A", "candidate_B": "CANDIDATE_B",
            "verification_A": "VERIFICATION_A", "verification_B": "VERIFICATION_B",
            "committed_completion": "COMMITTED_COMPLETION",
            "authority_seal": "AUTHORITY_SEAL",
            "candidate_staging_path_template": "CANDIDATE_STAGE_A",
            "verification_staging_path_template": "VERIFICATION_STAGE_A",
            "completion_staging_path": "COMPLETION_STAGE",
            "authority_staging_path": "AUTHORITY_STAGE",
            "v16r2_rejection_namespace": "REJECTION_NAMESPACE",
            "v16r2_later_rejection": "LATER_REJECTION",
        }
        consumer_result: dict[str, bool] = {}
        for key, name in consumer_map.items():
            actual = consumer.get(name)
            target = expected_abs.get(key)
            if key.endswith("_template"):
                actual_s = path_string(actual).replace("-a-", "-{a|b}-")
                consumer_result[key] = actual_s == path_string(target)
            else:
                consumer_result[key] = actual == target
        check("consumer_current_paths_match_contract",
              all(consumer_result.values()), consumer_result)

        launcher = modules["launcher"]
        launcher_result = {
            "rejection_namespace": launcher.get("V16R2_REJECTION_NAMESPACE") ==
            expected_abs["v16r2_rejection_namespace"],
            "later_rejection": launcher.get("V16R2_LATER_REJECTION") ==
            expected_abs["v16r2_later_rejection"],
            "self": launcher.get("SELF") == src["launcher"],
            "exact8_len": len(launcher.get("EXACT8", ())) == 8,
            "base7_keys_exact8": tuple(launcher.get("BASE7_PINS", {})) ==
            tuple(launcher.get("EXACT8", ()))[:7],
        }
        check("launcher_current_paths_and_exact8",
              all(launcher_result.values()), launcher_result)
        census = launcher_rebind_census(src["launcher"], sha(anchor_raw),
                                        anchor["object_sha256"])
        check("launcher_function_namespace_tag_rebind", True, census)

        pin_results: dict[str, bool] = {}
        for role, ns in modules.items():
            pin_results[role] = (
                ns.get("UPSTREAM_CHECKPOINT_OBJECT_PIN") == B58 and
                ns.get("SUCCESSOR_CHECKPOINT_OBJECT_PIN") == DD9 and
                ns.get("CHECKPOINT_OBJECT_PIN") == DD9 and
                ns.get("CHECKPOINT", B58) == B58)
        check("source_checkpoint_roles", all(pin_results.values()), pin_results)

        effective_detail: dict[str, Any] = {}
        effective_ok: dict[str, bool] = {}
        for name, value in values.items():
            found = walk_effective(value)
            effective_detail[name] = {"count": len(found),
                                      "unique": sorted(set(map(str, found)))}
            effective_ok[name] = bool(found) and all(item == B58 for item in found)
        check("each_active_json_effective_b58", all(effective_ok.values()),
              effective_detail)

        successor_detail: dict[str, Any] = {}
        successor_ok: dict[str, bool] = {}
        for name, value in values.items():
            found = walk_key(value, "successor_checkpoint_object_sha256")
            successor_detail[name] = {"count": len(found),
                                      "unique": sorted(set(map(str, found)))}
            # The schema is a validator document, not a chain receipt.  The
            # three active JSON receipts must nevertheless carry dd9
            # explicitly so inherited r23 fields cannot masquerade as r33.
            successor_ok[name] = (name == "contract" and
                                  bool(found) and all(item == DD9 for item in found)) or \
                                 (name != "contract" and
                                  bool(found) and all(item == DD9 for item in found))
        check("each_active_json_successor_dd9", all(successor_ok.values()),
              successor_detail)

        v14_expected = f".cm2-runtime/c79g-v14-rejections-{B58}/rejection.json"
        v14_source = {
            role: ns.get("V14_OFFICIAL_REJECTION_RELATIVE_PATH") == v14_expected
            for role, ns in modules.items()
        }
        check("source_v14_trust_path_b58", all(v14_source.values()), v14_source)
        v14_json: dict[str, list[Any]] = {}
        for name in ("contract", "audit"):
            found = walk_key(values[name], "v14_official_rejection_path")
            v14_json[name] = found
        check("json_v14_trust_path_b58",
              all(v14_json[name] and all(item == v14_expected
                                         for item in v14_json[name])
                  for name in v14_json),
              v14_json)

        r33_pyc = [str(path.relative_to(ROOT)) for path in ROOT.rglob("*.pyc")
                   if TAG in str(path)]
        check("no_r33_pyc", not r33_pyc, r33_pyc)
        manifest = OUT / f"{BASE}_cold_launch_manifest_{TAG}.sha256"
        outer = OUT / f"{BASE}_cold_launch_outer_receipt_{TAG}.json"
        check("manifest_outer_absent", not manifest.exists() and not outer.exists(),
              {"manifest": str(manifest), "outer": str(outer)})

        passed = all(row["passed"] for row in checks)
        report: dict[str, Any] = {
            "schema": f"cm2.c79g.{TAG}.runtime-semantic-audit.v1",
            "status": ("PASS_R33_CURRENT_PATH_CHECKPOINT_AND_TRUST_AUDIT__ZERO_CREDIT"
                        if passed else
                        "FAIL_CLOSED_R33_CURRENT_PATH_CHECKPOINT_AND_TRUST_AUDIT"),
            "successor_suffix": TAG, "predecessor_suffix": PREV,
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
            "status": "FAIL_CLOSED_R33_CURRENT_PATH_CHECKPOINT_AND_TRUST_AUDIT_EXCEPTION",
            "error": f"{type(exc).__name__}: {exc}",
            "formal_global_closure_credit": 0, "D02_unlock": False,
            "runtime_authorized": False, "read_only": True,
        }
        report["object_sha256"] = sha(canon(report))
        print(json.dumps(report, ensure_ascii=False, sort_keys=True))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
