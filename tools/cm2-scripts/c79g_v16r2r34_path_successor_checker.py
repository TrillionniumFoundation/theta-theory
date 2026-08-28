#!/usr/bin/env python3
"""Read-only r34 patch-spec checker for the r33 append-only candidate.

The checker intentionally does not mutate r33 bytes.  It reports the exact
path/successor defects that an r34 builder must repair before deriving new
source pins: canonical current runtime paths, cold-launch aliases and exact8 /
exact10 order must agree, while effective checkpoint fields stay b58 and an
explicit successor field carries dd9.  ``TAG`` and ``PREV`` are environment
parameters, so the same checker can audit a later append-only hop.
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


class DuplicateKey(ValueError):
    pass


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
    fd = os.open(path, os.O_RDONLY | os.O_CLOEXEC |
                 getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(fd)
        named = os.lstat(path)
        if (not stat.S_ISREG(before.st_mode) or before.st_nlink != 1 or
                (before.st_dev, before.st_ino, before.st_size) !=
                (named.st_dev, named.st_ino, named.st_size)):
            raise RuntimeError(f"unstable:{path}")
        data = bytearray()
        while True:
            block = os.read(fd, 1 << 20)
            if not block:
                break
            data.extend(block)
        after = os.fstat(fd)
        named_after = os.lstat(path)
        if ((before.st_dev, before.st_ino, before.st_size) !=
                (after.st_dev, after.st_ino, after.st_size) or
                (before.st_dev, before.st_ino) !=
                (named_after.st_dev, named_after.st_ino) or
                len(data) != before.st_size):
            raise RuntimeError(f"drift:{path}")
        return bytes(data)
    finally:
        os.close(fd)


def load(path: Path) -> tuple[dict[str, Any], bytes]:
    raw = stable(path)
    value = json.loads(raw.decode("utf-8"), object_pairs_hook=pairs)
    if not isinstance(value, dict):
        raise RuntimeError(f"object-required:{path}")
    claim = value.get("object_sha256")
    body = dict(value)
    body.pop("object_sha256", None)
    if not isinstance(claim, str) or not HEX.fullmatch(claim) or sha(canon(body)) != claim:
        raise RuntimeError(f"object-closure:{path}")
    return value, raw


def walk(value: Any, key_name: str | None = None) -> list[Any]:
    found: list[Any] = []
    if isinstance(value, dict):
        for key, child in value.items():
            if key_name is None or key == key_name:
                if key_name is not None:
                    found.append(child)
            found.extend(walk(child, key_name))
    elif isinstance(value, list):
        for child in value:
            found.extend(walk(child, key_name))
    return found


def effective(value: Any) -> list[Any]:
    found: list[Any] = []
    if isinstance(value, dict):
        for key, child in value.items():
            if (isinstance(key, str) and
                    ("effective_checkpoint" in key or
                     "post_seal_effective" in key)):
                found.append(child)
            found.extend(effective(child))
    elif isinstance(value, list):
        for child in value:
            found.extend(effective(child))
    return found


def source_file(role: str) -> Path:
    if role == "producer":
        return OUT / f"{BASE}_{TAG}_semantic_source.py"
    if role == "consumer":
        return OUT / (f"{BASE}_independent_verifier_assembler_authority_consumer_"
                      f"{TAG}_semantic_source.py")
    return OUT / f"{BASE}_cold_launch_{TAG}_semantic_source.py"


def execute(path: Path, role: str) -> dict[str, Any]:
    text = stable(path).decode("utf-8")
    tree = ast.parse(text, filename=str(path), mode="exec")
    compile(tree, str(path), "exec")
    ns: dict[str, Any] = {"__name__": f"_r34_path_{role}",
                          "__file__": str(path), "__package__": None}
    env = "CM2_C79G_V16R2_COLD_WORKSPACE_ROOT"
    old = os.environ.get(env)
    os.environ[env] = str(ROOT)
    try:
        exec(compile(tree, str(path), "exec"), ns, ns)
    finally:
        if old is None:
            os.environ.pop(env, None)
        else:
            os.environ[env] = old
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
        jpaths = {
            "contract": OUT / f"{BASE}_contract_{TAG}.json",
            "transition": OUT / (
                f"{BASE}_{PREV}_to_{TAG}_static_launch_transition_receipt_v1.json"),
            "audit": OUT / f"{BASE}_static_audit_{TAG}.json",
        }
        anchor_path = OUT / f"{BASE}_{TAG}_active_predecessor_supersession_receipt_v1.json"
        members = [source_file(role) for role in ("producer", "consumer", "launcher")]
        members += [*jpaths.values(), anchor_path]
        present = {str(path.relative_to(ROOT)): path.is_file() for path in members}
        check("members_present", all(present.values()), present)
        if not all(present.values()):
            raise RuntimeError("r34-check-input-missing")

        values = {name: load(path)[0] for name, path in jpaths.items()}
        anchor, anchor_raw = load(anchor_path)
        check("anchor_roles", anchor.get("upstream_checkpoint_object_sha256") == B58 and
              anchor.get("successor_checkpoint_object_sha256") == DD9 and
              anchor.get("successor_namespace") == f"{TAG}_semantic_source")

        # Full active exact-publication map, including the three cold aliases
        # that older builders accidentally left at unsuffixed v16r2 names.
        launcher_rel = f"deliverables/{source_file('launcher').name}"
        manifest_rel = f"deliverables/{BASE}_cold_launch_manifest_{TAG}.sha256"
        outer_rel = f"deliverables/{BASE}_cold_launch_outer_receipt_{TAG}.json"
        canonical = {
            "candidate_A": f".cm2-runtime/c79g-v16r2-candidate-a-{B58}",
            "candidate_B": f".cm2-runtime/c79g-v16r2-candidate-b-{B58}",
            "verification_A": f".cm2-runtime/c79g-v16r2-verification-a-{B58}",
            "verification_B": f".cm2-runtime/c79g-v16r2-verification-b-{B58}",
            "committed_completion": f".cm2-runtime/c79g-v16r2-committed-completion-{B58}",
            "authority_seal": f".cm2-runtime/cm2-global-authority-heads/c79g-v16r2-{B58}.seal",
            "v16r2_rejection_namespace": f".cm2-runtime/c79g-v16r2-rejections-{B58}",
            "v16r2_later_rejection": f".cm2-runtime/c79g-v16r2-rejections-{B58}/rejection.json",
            "candidate_staging_path_template": f".cm2-runtime/.c79g-v16r2-candidate-stage-{{a|b}}-{B58}",
            "verification_staging_path_template": f".cm2-runtime/.c79g-v16r2-verification-stage-{{a|b}}-{B58}",
            "completion_staging_path": f".cm2-runtime/.c79g-v16r2-completion-stage-{B58}",
            "authority_staging_path": f".cm2-runtime/cm2-global-authority-heads/.c79g-v16r2-authority-stage-{B58}.seal",
            "cold_launcher": launcher_rel,
            "cold_launch_exact8_manifest": manifest_rel,
            "cold_launch_outer_last": outer_rel,
        }
        paths = values["contract"].get("exact_publication_paths", {})
        path_result = {key: paths.get(key) == value
                       for key, value in canonical.items()}
        check("exact_publication_paths_full_canonical", all(path_result.values()),
              {key: {"actual": paths.get(key), "expected": value}
               for key, value in canonical.items() if not path_result[key]})
        # Legacy aliases are allowed only when they resolve to the same b58
        # current rejection object; no alias may point at a successor path.
        alias_result = {}
        for old, new in (("v15_later_rejection", "v16r2_later_rejection"),
                         ("v15_rejection_namespace", "v16r2_rejection_namespace")):
            if old in paths:
                alias_result[old] = paths[old] == paths.get(new)
        check("legacy_aliases_same_current_path", all(alias_result.values()), alias_result)

        bundle = values["contract"].get("v16r2_bundle", {})
        expected8 = [
            f"deliverables/{BASE}_{TAG}_active_predecessor_supersession_receipt_v1.json",
            f"deliverables/{BASE}_schema_{TAG}.json",
            f"deliverables/{BASE}_contract_{TAG}.json",
            f"deliverables/{BASE}_{TAG}_semantic_source.py",
            f"deliverables/{BASE}_independent_verifier_assembler_authority_consumer_{TAG}_semantic_source.py",
            f"deliverables/{BASE}_{PREV}_to_{TAG}_static_launch_transition_receipt_v1.json",
            f"deliverables/{BASE}_static_audit_{TAG}.json", launcher_rel,
        ]
        expected10 = expected8 + [manifest_rel, outer_rel]
        order_result = {
            "exact8": bundle.get("exact8_ordered_paths") == expected8,
            "base7": bundle.get("base7_ordered_paths") == expected8[:-1],
            "exact10": bundle.get("exact10_ordered_paths") == expected10,
        }
        check("contract_exact8_manifest_outer_order", all(order_result.values()),
              order_result)

        modules = {role: execute(source_file(role), role)
                   for role in ("producer", "consumer", "launcher")}
        producer_result = {
            "candidate_A": modules["producer"].get("CANDIDATE_A") == ROOT / canonical["candidate_A"],
            "candidate_B": modules["producer"].get("CANDIDATE_B") == ROOT / canonical["candidate_B"],
        }
        check("producer_paths", all(producer_result.values()), producer_result)
        consumer_names = {
            "candidate_A": "CANDIDATE_A", "candidate_B": "CANDIDATE_B",
            "verification_A": "VERIFICATION_A", "verification_B": "VERIFICATION_B",
            "committed_completion": "COMMITTED_COMPLETION", "authority_seal": "AUTHORITY_SEAL",
            "v16r2_rejection_namespace": "REJECTION_NAMESPACE", "v16r2_later_rejection": "LATER_REJECTION",
            "candidate_staging_path_template": "CANDIDATE_STAGE_A",
            "verification_staging_path_template": "VERIFICATION_STAGE_A",
            "completion_staging_path": "COMPLETION_STAGE", "authority_staging_path": "AUTHORITY_STAGE",
        }
        consumer_result = {}
        for key, name in consumer_names.items():
            actual = modules["consumer"].get(name)
            target = ROOT / canonical[key]
            if key.endswith("_template"):
                consumer_result[key] = str(actual).replace("-a-", "-{a|b}-") == str(target)
            else:
                consumer_result[key] = actual == target
        check("consumer_paths", all(consumer_result.values()), consumer_result)
        launcher_result = {
            "self": modules["launcher"].get("SELF") == ROOT / launcher_rel,
            "manifest": modules["launcher"].get("MANIFEST") == ROOT / manifest_rel,
            "outer": modules["launcher"].get("OUTER") == ROOT / outer_rel,
            "rejection": modules["launcher"].get("V16R2_LATER_REJECTION") == ROOT / canonical["v16r2_later_rejection"],
        }
        check("launcher_paths", all(launcher_result.values()), launcher_result)

        effective_result = {}
        successor_result = {}
        for name, value in values.items():
            eff = effective(value)
            succ = walk(value, "successor_checkpoint_object_sha256")
            effective_result[name] = bool(eff) and all(item == B58 for item in eff)
            successor_result[name] = bool(succ) and all(item == DD9 for item in succ)
        check("effective_fields_b58", all(effective_result.values()), effective_result)
        check("explicit_successor_fields_dd9", all(successor_result.values()), successor_result)

        v14 = f".cm2-runtime/c79g-v14-rejections-{B58}/rejection.json"
        v14_sources = {role: modules[role].get("V14_OFFICIAL_REJECTION_RELATIVE_PATH") == v14
                       for role in modules}
        v14_json = {name: bool(walk(value, "v14_official_rejection_path")) and
                    all(item == v14 for item in walk(value, "v14_official_rejection_path"))
                    for name, value in values.items() if name in ("contract", "audit")}
        check("v14_trust_b58", all(v14_sources.values()) and all(v14_json.values()),
              {"sources": v14_sources, "json": v14_json})

        pyc = [str(path.relative_to(ROOT)) for path in ROOT.rglob("*.pyc") if TAG in str(path)]
        check("no_tag_pyc", not pyc, pyc)
        check("manifest_outer_not_published", not (OUT / f"{BASE}_cold_launch_manifest_{TAG}.sha256").exists() and
              not (OUT / f"{BASE}_cold_launch_outer_receipt_{TAG}.json").exists())

        passed = all(row["passed"] for row in checks)
        report: dict[str, Any] = {
            "schema": f"cm2.c79g.{TAG}.r34-path-successor-checker.v1",
            "status": "PASS_R34_PATCH_SPEC_CHECK__ZERO_CREDIT" if passed else
            "FAIL_CLOSED_R34_PATCH_SPEC_CHECK",
            "successor_suffix": TAG, "predecessor_suffix": PREV,
            "checks": checks, "failed_check_count": sum(not row["passed"] for row in checks),
            "patch_spec": {
                "rewrite_exact_publication_paths": [key for key, ok in path_result.items() if not ok],
                "reclose_contract_transition_audit_after_successor_field_injection": [
                    name for name, ok in successor_result.items() if not ok],
                "preserve_historical_v16_dd9_rejection_path": True,
                "publication_allowed": False,
            },
            "formal_global_closure_credit": 0, "D02_unlock": False,
            "runtime_authorized": False, "read_only": True,
        }
        report["object_sha256"] = sha(canon(report))
        print(json.dumps(report, ensure_ascii=False, sort_keys=True))
        return 0 if passed else 1
    except Exception as exc:
        report = {
            "schema": f"cm2.c79g.{TAG}.r34-path-successor-checker.v1",
            "status": "FAIL_CLOSED_R34_PATCH_SPEC_CHECK_EXCEPTION",
            "error": f"{type(exc).__name__}: {exc}",
            "formal_global_closure_credit": 0, "D02_unlock": False,
            "runtime_authorized": False, "read_only": True,
        }
        report["object_sha256"] = sha(canon(report))
        print(json.dumps(report, ensure_ascii=False, sort_keys=True))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
