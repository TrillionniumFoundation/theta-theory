#!/usr/bin/env python3
"""Independent, read-only r31 current-path/checkpoint semantic audit.

This checker deliberately does not import a protocol module and never writes a
receipt.  It executes only module-level definitions in an isolated namespace
(``__name__`` is not ``__main__``), then compares the resulting deterministic
Path objects with the contract's exact-publication map.  It exists to catch the
class of defect that a textual 34-check reviewer cannot see: a source using a
dd9/``semantic-source`` runtime path while the closed contract names the b58
protocol path.
"""
from __future__ import annotations

import ast
import hashlib
import json
import os
import stat
import sys
from pathlib import Path
from typing import Any

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "deliverables"
BASE = "cm2_round306c79g_true_global_no_producer_consumer"
TAG = os.environ.get("CM2_SUCCESSOR_SUFFIX", "v16r2r31")
PREV = os.environ.get("CM2_PREDECESSOR_SUFFIX", "v16r2r30")
B58 = "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab"
DD9 = "dd9d64f3f0bd0dfd00fd399e3154517a34ba19cfb601ec749f44cbc08b03ca1b"


def canon(v: Any) -> bytes:
    return json.dumps(v, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"), allow_nan=False).encode()


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


def closed(v: dict[str, Any]) -> bool:
    claim = v.get("object_sha256")
    if not isinstance(claim, str):
        return False
    body = dict(v)
    body.pop("object_sha256", None)
    return sha(canon(body)) == claim


def source_paths() -> dict[str, Path]:
    return {
        "producer": OUT / f"{BASE}_{TAG}_semantic_source.py",
        "consumer": OUT / (
            f"{BASE}_independent_verifier_assembler_authority_consumer_"
            f"{TAG}_semantic_source.py"),
        "launcher": OUT / f"{BASE}_cold_launch_{TAG}_semantic_source.py",
    }


def contract_path() -> Path:
    return OUT / f"{BASE}_contract_{TAG}.json"


def active_json_paths() -> dict[str, Path]:
    return {
        "contract": OUT / f"{BASE}_contract_{TAG}.json",
        "transition": OUT / (
            f"{BASE}_{PREV}_to_{TAG}_static_launch_transition_receipt_v1.json"),
        "audit": OUT / f"{BASE}_static_audit_{TAG}.json",
    }


def execute_defs(path: Path, role: str) -> dict[str, Any]:
    text = stable(path).decode("utf-8")
    tree = ast.parse(text, filename=str(path), mode="exec")
    compile(tree, str(path), "exec")
    ns: dict[str, Any] = {
        "__name__": f"_r31_semantic_audit_{role}",
        "__file__": str(path),
        "__package__": None,
    }
    # The producer/consumer bind ROOT from this environment variable during
    # definition execution.  Pin it to this audit's workspace for every role
    # (and restore the caller's value afterwards), so a stray inherited env
    # cannot make the Path-vs-contract comparison inspect another tree.
    old_root = os.environ.get("CM2_C79G_V16R2_COLD_WORKSPACE_ROOT")
    os.environ["CM2_C79G_V16R2_COLD_WORKSPACE_ROOT"] = str(ROOT)
    old_pycache = os.environ.get("PYTHONDONTWRITEBYTECODE")
    os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
    try:
        exec(compile(tree, str(path), "exec"), ns, ns)
    finally:
        if old_root is None:
            os.environ.pop("CM2_C79G_V16R2_COLD_WORKSPACE_ROOT", None)
        else:
            os.environ["CM2_C79G_V16R2_COLD_WORKSPACE_ROOT"] = old_root
        if old_pycache is None:
            os.environ.pop("PYTHONDONTWRITEBYTECODE", None)
        else:
            os.environ["PYTHONDONTWRITEBYTECODE"] = old_pycache
    if role == "launcher":
        ns["configure_workspace_paths"](ROOT)
    return ns


def main() -> int:
    checks: list[dict[str, Any]] = []

    def check(name: str, ok: bool, detail: Any = None) -> None:
        row: dict[str, Any] = {"name": name, "passed": bool(ok)}
        if detail is not None:
            row["detail"] = detail
        checks.append(row)

    try:
        src = source_paths()
        json_members = active_json_paths()
        cp = json_members["contract"]
        all_paths = [*src.values(), *json_members.values()]
        check("members_present", all(p.is_file() for p in all_paths))
        if not all(p.is_file() for p in all_paths):
            raise RuntimeError("missing r31 member")

        values = {name: json.loads(stable(path).decode("utf-8"))
                  for name, path in json_members.items()}
        contract = values["contract"]
        check("json_object_closure", all(isinstance(v, dict) and closed(v)
              for v in values.values()))
        expected = contract.get("exact_publication_paths", {})
        expected_abs = {k: ROOT / v for k, v in expected.items()
                        if isinstance(v, str) and v.startswith(".")}

        # r23 carried the historical ``v15_*`` labels.  A fresh r31 contract
        # must expose the canonical v16r2 labels as well; retain the legacy
        # labels only as a consistency witness, never as the active lookup.
        required_runtime_keys = {
            "candidate_A", "candidate_B", "verification_A", "verification_B",
            "committed_completion", "authority_seal", "v16r2_rejection_namespace",
            "v16r2_later_rejection", "candidate_staging_path_template",
            "verification_staging_path_template", "completion_staging_path",
            "authority_staging_path",
        }
        check("contract_canonical_runtime_keyset",
              required_runtime_keys <= set(expected_abs),
              {"missing": sorted(required_runtime_keys - set(expected_abs))})
        # If the historical aliases are present they must point to exactly the
        # same b58 objects; an alias pointing at dd9 is a path split.
        alias_results = {}
        for old, new in (("v15_later_rejection", "v16r2_later_rejection"),
                         ("v15_rejection_namespace", "v16r2_rejection_namespace")):
            if old in expected_abs:
                alias_results[old] = expected_abs[old] == expected_abs.get(new)
        check("legacy_runtime_aliases_canonical", all(alias_results.values()),
              alias_results)

        modules = {role: execute_defs(path, role) for role, path in src.items()}
        check("ast_compile_and_definition_smoke", True)

        # The current executable path family is canonical b58 and has no
        # semantic-source infix.  These are intentionally compared as Path
        # identities, not as substring claims.
        consumer = modules["consumer"]
        path_map = {
            "candidate_A": "CANDIDATE_A",
            "candidate_B": "CANDIDATE_B",
            "verification_A": "VERIFICATION_A",
            "verification_B": "VERIFICATION_B",
            "committed_completion": "COMMITTED_COMPLETION",
            "authority_seal": "AUTHORITY_SEAL",
            "candidate_staging_path_template": "CANDIDATE_STAGE_A",
            "verification_staging_path_template": "VERIFICATION_STAGE_A",
            "completion_staging_path": "COMPLETION_STAGE",
            "authority_staging_path": "AUTHORITY_STAGE",
            "v16r2_later_rejection": "LATER_REJECTION",
        }
        path_results: dict[str, bool] = {}
        for key, name in path_map.items():
            if key not in expected_abs or name not in consumer:
                path_results[key] = False
                continue
            actual = consumer[name]
            target = expected_abs[key]
            # Staging templates are represented by the ``a`` member in source;
            # compare the fixed prefix and b58 suffix after removing the side.
            if key.endswith("_template"):
                actual_s = str(actual).replace("-a-", "-{a|b}-")
                path_results[key] = actual_s == str(target)
            else:
                path_results[key] = actual == target
        check("consumer_current_paths_match_contract", all(path_results.values()),
              path_results)

        producer = modules["producer"]
        producer_results = {
            "candidate_A": producer.get("CANDIDATE_A") ==
            expected_abs.get("candidate_A"),
            "candidate_B": producer.get("CANDIDATE_B") ==
            expected_abs.get("candidate_B"),
        }
        check("producer_current_paths_match_contract",
              all(producer_results.values()), producer_results)

        launcher = modules["launcher"]
        launcher_results = {
            "v16r2_rejection_namespace": launcher.get("V16R2_REJECTION_NAMESPACE") ==
            expected_abs.get("v16r2_rejection_namespace"),
            "v16r2_later_rejection": launcher.get("V16R2_LATER_REJECTION") ==
            expected_abs.get("v16r2_later_rejection"),
            "active_self": launcher.get("SELF") ==
            src["launcher"],
            "exact8_len": len(launcher.get("EXACT8", ())) == 8,
            "base7_keys_exact8": tuple(launcher.get("BASE7_PINS", {})) ==
            tuple(launcher.get("EXACT8", ()))[:7],
        }
        check("launcher_current_paths_and_exact8", all(launcher_results.values()),
              launcher_results)

        # Checkpoint roles: b58 is effective/current; dd9 can only remain as
        # the explicitly named successor-chain pin.
        pin_results = {}
        for role, ns in modules.items():
            pin_results[role] = (
                ns.get("UPSTREAM_CHECKPOINT_OBJECT_PIN") == B58 and
                ns.get("SUCCESSOR_CHECKPOINT_OBJECT_PIN") == DD9 and
                ns.get("CHECKPOINT_OBJECT_PIN") == DD9 and
                ns.get("CHECKPOINT", B58) == B58)
        check("checkpoint_roles", all(pin_results.values()), pin_results)

        # Every effective field in contract/transition/audit must be b58; no
        # effective field may retain dd9.
        effective: list[str] = []

        def walk(v: Any) -> None:
            if isinstance(v, dict):
                for k, child in v.items():
                    if isinstance(k, str) and ("effective_checkpoint" in k or
                                                "post_seal_effective" in k):
                        effective.append(child)
                    walk(child)
            elif isinstance(v, list):
                for child in v:
                    walk(child)

        per_json_effective: dict[str, list[Any]] = {}
        for name, value in values.items():
            local: list[Any] = []

            def walk_local(v: Any) -> None:
                if isinstance(v, dict):
                    for k, child in v.items():
                        if (isinstance(k, str) and
                                ("effective_checkpoint" in k or
                                 "post_seal_effective" in k)):
                            local.append(child)
                        walk_local(child)
                elif isinstance(v, list):
                    for child in v:
                        walk_local(child)

            walk_local(value)
            per_json_effective[name] = local
            effective.extend(local)
        per_json_ok = {name: bool(items) and all(item == B58 for item in items)
                       for name, items in per_json_effective.items()}
        check("each_active_json_effective_b58", all(per_json_ok.values()),
              {name: {"count": len(per_json_effective[name]),
                      "unique": sorted(set(map(str, per_json_effective[name])))}
               for name in per_json_effective})
        check("contract_effective_b58", bool(effective) and
              all(v == B58 for v in effective),
              {"count": len(effective), "unique": sorted(set(effective))})

        # The successor pin is a chain witness, not an effective checkpoint.
        # r31 transition/audit/contract objects must carry it explicitly so a
        # future guard cannot mistake an inherited r23 receipt for this hop.
        successor_fields: dict[str, list[Any]] = {}

        def collect_successor(v: Any, out: list[Any]) -> None:
            if isinstance(v, dict):
                for k, child in v.items():
                    if k == "successor_checkpoint_object_sha256":
                        out.append(child)
                    collect_successor(child, out)
            elif isinstance(v, list):
                for child in v:
                    collect_successor(child, out)

        for name, value in values.items():
            found: list[Any] = []
            collect_successor(value, found)
            successor_fields[name] = found
        successor_ok = {
            name: bool(found) and all(item == DD9 for item in found)
            for name, found in successor_fields.items()
        }
        check("successor_pin_explicit_in_active_json", all(successor_ok.values()),
              {name: {"count": len(successor_fields[name]),
                      "unique": sorted(set(map(str, successor_fields[name])))}
               for name in successor_fields})

        # Candidate namespace / no-pyc publication surfaces must not exist at
        # this pre-freeze stage.  Historical r28/r30 pyc evidence is allowed;
        # only r31-named bytecode is a contamination of this namespace.
        r31_pyc = [str(p.relative_to(ROOT)) for p in ROOT.rglob("*.pyc")
                   if TAG in str(p)]
        check("no_r31_pyc", not r31_pyc, r31_pyc)
        check("manifest_outer_absent", not (OUT / f"{BASE}_cold_launch_manifest_{TAG}.sha256").exists() and
              not (OUT / f"{BASE}_cold_launch_outer_receipt_{TAG}.json").exists())

        passed = all(row["passed"] for row in checks)
        report = {
            "schema": f"cm2.c79g.{TAG}.runtime-semantic-audit.v1",
            "status": "PASS_R31_CURRENT_PATH_AND_CHECKPOINT_SEMANTIC_AUDIT__ZERO_CREDIT" if passed else
            "FAIL_CLOSED_R31_CURRENT_PATH_AND_CHECKPOINT_SEMANTIC_AUDIT",
            "successor_suffix": TAG, "predecessor_suffix": PREV,
            "checks": checks, "check_count": len(checks),
            "failed_check_count": sum(not x["passed"] for x in checks),
            "formal_global_closure_credit": 0, "D02_unlock": False,
            "runtime_authorized": False, "read_only": True,
        }
        report["object_sha256"] = sha(canon(report))
        print(json.dumps(report, ensure_ascii=False, sort_keys=True))
        return 0 if passed else 1
    except Exception as exc:
        print(json.dumps({
            "schema": f"cm2.c79g.{TAG}.runtime-semantic-audit.v1",
            "status": "FAIL_CLOSED_R31_CURRENT_PATH_AND_CHECKPOINT_SEMANTIC_AUDIT_EXCEPTION",
            "error": f"{type(exc).__name__}: {exc}",
            "formal_global_closure_credit": 0, "D02_unlock": False,
            "runtime_authorized": False, "read_only": True,
        }, ensure_ascii=False, sort_keys=True))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
