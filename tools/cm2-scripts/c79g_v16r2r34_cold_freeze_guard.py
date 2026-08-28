#!/usr/bin/env python3
"""Read-only r34 cold-freeze preflight guard.

This is a fresh append-only guard for ``v16r2r34``.  It deliberately has no
publication implementation: ``PINS_PENDING`` and
``ONE_SHOT_FREEZE_PUBLISH_ENABLED`` remain true/false respectively, and every
preflight result requires the r34 manifest and outer-last receipt to be
absent.  The guard reads stable exact8 bytes, runs the independent A/B,
semantic, and canonical-path reports in ``-I -B`` subprocesses, validates the
zero-credit side evidence and unchanged C53 head, and emits only a report on
stdout.  It never imports or executes a candidate protocol and never writes a
workspace file.
"""
from __future__ import annotations

import ast
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
from typing import Any

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

BASE = "cm2_round306c79g_true_global_no_producer_consumer"
TAG = "v16r2r34"
PREV = "v16r2r33"
CHECKPOINT = "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab"
SUCCESSOR_CHECKPOINT = "dd9d64f3f0bd0dfd00fd399e3154517a34ba19cfb601ec749f44cbc08b03ca1b"
PINS_PENDING = True
ONE_SHOT_FREEZE_PUBLISH_ENABLED = False
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "deliverables"

# Exact8 file pins are intentionally literal, independently derived values.
# JSON object pins are required for the four closed receipts; source/schema
# members have no object_sha256 member and therefore retain None.
EXACT8: tuple[tuple[str, str, str | None, int], ...] = (
    (f"deliverables/{BASE}_{TAG}_active_predecessor_supersession_receipt_v1.json",
     "b0a47e3ea586aa9bca2fb647ace2086651c318b0676369e09b59d8b705ef7a89",
     "9047ba11c82743b18731818044755b7dedf591cf4bc1e3982921871521c78b0e", 0o444),
    (f"deliverables/{BASE}_schema_{TAG}.json",
     "faa68634c03eda0818f970c1963436bcc446a83695c5f20da36f6c632de9192d",
     None, 0o444),
    (f"deliverables/{BASE}_contract_{TAG}.json",
     "3c1e109fbb6a80b83e623131b549bf5007d8c9e3f3676087133714aa5f554b71",
     "98477ae1718cd6ad1a87cbe86a2099725e80bf1c2a4c16eed1d9271a2813f780", 0o444),
    (f"deliverables/{BASE}_{TAG}_semantic_source.py",
     "e83a718c0a480e4deaa44fc091b18d3438f87519efe7db27f4204cf99a3596ed",
     None, 0o664),
    (f"deliverables/{BASE}_independent_verifier_assembler_authority_consumer_{TAG}_semantic_source.py",
     "877f4a6ba6475ee27ffca8e030302d9af7c5309fcefb689b37be4049682a1e9b",
     None, 0o664),
    (f"deliverables/{BASE}_{PREV}_to_{TAG}_static_launch_transition_receipt_v1.json",
     "86ccf4e8543a095105958981804b1531a48b4da89f0dc9f1f363bf0c396c7933",
     "29d32e73855644d56d28d58345eeaf25ebc4ddc6a5c6a2ea2800f5a19faa13a3", 0o444),
    (f"deliverables/{BASE}_static_audit_{TAG}.json",
     "b924ecbc71ef8e280d1fa15bba22ba0af682711217713b2c7217b475c629e187",
     "c9c8ef2cbdfc0098e9c307ab360d5275bd4efe97f1038d24298b5684fbb5bf9a", 0o444),
    (f"deliverables/{BASE}_cold_launch_{TAG}_semantic_source.py",
     "24f9686462f47c009118887d1cdfd0f1b22791eeef335bcb64252d3ade931c0a",
     None, 0o664),
)

C53_PATH = ROOT / (
    ".cm2-runtime/cm2-global-authority-heads/"
    "predecessor-10fb050d30c92b0f2bdcf85a30d28ff670d8efc0b48104b7f04a63c391967b41.seal")
C53_FILE_SHA256 = "f62483c87df4b6f4a8a2ad8dcf56febbfce9977200ce94a0ad6ce38e736aeeb3"
C53_OBJECT_SHA256 = "cb90ab914c3b6518384669f42d05df33c21a717596190131c6a0f5683934cbfb"

RECEIPTS = {
    "no_producer": OUT / f"{BASE}_{TAG}_no_producer_dual_seed_evidence_receipt_v1.json",
    "mutation_attacks": OUT / f"{BASE}_{TAG}_mutation_attack_evidence_receipt_v1.json",
    "terminal_replay": OUT / f"{BASE}_{TAG}_dual_checker_terminal_replay_receipt_v1.json",
}


class DuplicateKey(ValueError):
    pass


def strict_pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in items:
        if key in result:
            raise DuplicateKey(key)
        result[key] = value
    return result


def canonical(value: Any) -> bytes:
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


def load_closed(path: Path) -> tuple[dict[str, Any], bytes] | None:
    if not path.is_file():
        return None
    raw = stable(path)
    value = json.loads(raw.decode("utf-8"), object_pairs_hook=strict_pairs)
    if not isinstance(value, dict):
        raise RuntimeError(f"object-required:{path}")
    claim = value.get("object_sha256")
    body = dict(value)
    body.pop("object_sha256", None)
    if not isinstance(claim, str) or len(claim) != 64 or sha(canonical(body)) != claim:
        raise RuntimeError(f"closure:{path}")
    return value, raw


def walk(value: Any, key: str | None = None) -> list[Any]:
    found: list[Any] = []
    if isinstance(value, dict):
        for name, child in value.items():
            if key is not None and name == key:
                found.append(child)
            found.extend(walk(child, key))
    elif isinstance(value, list):
        for child in value:
            found.extend(walk(child, key))
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


def run_json(script: Path, seed: str) -> tuple[int, dict[str, Any] | None, bytes, str]:
    env = dict(os.environ)
    env.update({"PYTHONDONTWRITEBYTECODE": "1", "PYTHONNOUSERSITE": "1",
                "PYTHONHASHSEED": seed, "CM2_SUCCESSOR_SUFFIX": TAG,
                "CM2_PREDECESSOR_SUFFIX": PREV})
    proc = subprocess.run(["/usr/bin/python3", "-I", "-B", str(script)],
                          cwd=str(ROOT), env=env, capture_output=True,
                          check=False)
    raw = proc.stdout
    try:
        value = json.loads(raw.decode("utf-8"))
    except Exception:
        value = None
    return proc.returncode, value if isinstance(value, dict) else None, raw, proc.stderr.decode("utf-8", "replace")


def jq_accept(value: dict[str, Any] | None, expression: str) -> bool:
    """Apply a jq -e predicate to an in-memory report without writing files."""
    if value is None:
        return False
    proc = subprocess.run(["jq", "-e", expression], input=canonical(value),
                          capture_output=True, check=False)
    return proc.returncode == 0


def main() -> int:
    checks: list[dict[str, Any]] = []

    def check(name: str, ok: bool, detail: Any = None) -> None:
        row: dict[str, Any] = {"name": name, "passed": bool(ok)}
        if detail is not None:
            row["detail"] = detail
        checks.append(row)

    try:
        # Exact8 stable identity, mode and hard pins.
        exact_details: dict[str, Any] = {}
        exact_raw: dict[str, bytes] = {}
        exact_ok = True
        for relative, file_pin, object_pin, mode in EXACT8:
            path = ROOT / relative
            try:
                first = stable(path)
                second = stable(path)
                raw = first
                value = (json.loads(raw.decode("utf-8"), object_pairs_hook=strict_pairs)
                         if path.suffix == ".json" else None)
                actual_object = value.get("object_sha256") if isinstance(value, dict) else None
                row = {
                    "file_sha256": sha(raw), "expected_file_sha256": file_pin,
                    "object_sha256": actual_object, "expected_object_sha256": object_pin,
                    "second_read_identical": first == second,
                    "mode": stat.S_IMODE(path.stat().st_mode), "expected_mode": mode,
                    "nlink": path.stat().st_nlink,
                }
                ok = (sha(raw) == file_pin and first == second and
                      stat.S_IMODE(path.stat().st_mode) == mode and
                      path.stat().st_nlink == 1 and
                      (object_pin is None or actual_object == object_pin))
                exact_ok &= ok
                exact_details[relative] = row
                exact_raw[relative] = raw
            except Exception as exc:
                exact_ok = False
                exact_details[relative] = {"error": f"{type(exc).__name__}: {exc}"}
        check("exact8_stable_pins_modes_nlink", exact_ok, exact_details)

        # C53 is read twice and compared byte-for-byte; its known file/object
        # pins remain upstream evidence and are never rewritten.
        try:
            c53a, c53b = stable(C53_PATH), stable(C53_PATH)
            c53value = json.loads(c53a.decode("utf-8"), object_pairs_hook=strict_pairs)
            c53_ok = (c53a == c53b and sha(c53a) == C53_FILE_SHA256 and
                      isinstance(c53value, dict) and
                      c53value.get("authority_seal_object_sha256") == C53_OBJECT_SHA256)
            c53_detail = {"file_sha256": sha(c53a), "object_sha256": c53value.get("authority_seal_object_sha256"),
                          "unchanged": c53a == c53b}
        except Exception as exc:
            c53_ok = False
            c53_detail = {"error": f"{type(exc).__name__}: {exc}"}
        check("c53_unchanged_and_pinned", c53_ok, c53_detail)

        # Independent subprocess reports, twice under distinct hash seeds.
        scripts = {
            "reviewer_A": ROOT / "scripts/c79g_v16r2r20_independent_reviewer.py",
            "checker_B": ROOT / "scripts/c79g_v16r2r23_structure_checker_b.py",
            "semantic_audit": ROOT / "scripts/c79g_v16r2r34_runtime_semantic_audit.py",
            "path_checker": ROOT / "scripts/c79g_v16r2r34_path_successor_checker.py",
        }
        report_results: dict[str, Any] = {}
        reports_ok = True
        for name, script in scripts.items():
            runs = []
            for seed in ("1", "99991"):
                rc, value, raw, stderr = run_json(script, seed)
                if name == "reviewer_A":
                    expr = ('.status == "PASS_DUAL_STATIC_CANDIDATE_34_OF_34__RUNTIME_NOT_AUTHORIZED"'
                            ' and .check_count == 34 and .failed_check_count == 0'
                            ' and .read_only == true and .formal_global_closure_credit == 0'
                            ' and .D02_unlock == false and .runtime_authorized == false')
                elif name == "checker_B":
                    expr = ('.status == "PASS_INDEPENDENT_CHECKER_B__ZERO_CREDIT"'
                            ' and .check_count == 16 and .failed_check_count == 0'
                            ' and .read_only == true and .formal_global_closure_credit == 0'
                            ' and .D02_unlock == false and .runtime_authorized == false')
                elif name == "semantic_audit":
                    expr = ('.status == "PASS_R34_CURRENT_PATH_CHECKPOINT_AND_TRUST_AUDIT__ZERO_CREDIT"'
                            ' and .failed_check_count == 0 and .read_only == true'
                            ' and .formal_global_closure_credit == 0 and .D02_unlock == false'
                            ' and .runtime_authorized == false')
                else:
                    expr = ('.status == "PASS_R34_PATCH_SPEC_CHECK__ZERO_CREDIT"'
                            ' and .failed_check_count == 0 and .read_only == true'
                            ' and .formal_global_closure_credit == 0 and .D02_unlock == false'
                            ' and .runtime_authorized == false')
                accepted = rc == 0 and jq_accept(value, expr)
                reports_ok &= accepted
                runs.append({"seed": int(seed), "return_code": rc,
                             "accepted": accepted,
                             "report_sha256": sha(raw),
                             "status": value.get("status") if value else None,
                             "stderr_tail": stderr[-240:] if stderr else ""})
            if runs[0]["report_sha256"] != runs[1]["report_sha256"]:
                reports_ok = False
            report_results[name] = runs
        check("independent_A_B_semantic_path_reports", reports_ok, report_results)

        # Closed active JSONs: canonical aliases, effective b58, successor dd9.
        json_checks: dict[str, Any] = {}
        for name, path in {
            "contract": OUT / f"{BASE}_contract_{TAG}.json",
            "transition": OUT / f"{BASE}_{PREV}_to_{TAG}_static_launch_transition_receipt_v1.json",
            "audit": OUT / f"{BASE}_static_audit_{TAG}.json",
        }.items():
            try:
                loaded = load_closed(path)
                value = loaded[0] if loaded else {}
                eff = effective(value)
                succ = walk(value, "successor_checkpoint_object_sha256")
                json_checks[name] = {
                    "effective_b58": bool(eff) and all(x == CHECKPOINT for x in eff),
                    "successor_dd9": bool(succ) and all(x == SUCCESSOR_CHECKPOINT for x in succ),
                    "object_closed": loaded is not None,
                }
            except Exception as exc:
                json_checks[name] = {"error": f"{type(exc).__name__}: {exc}"}
        check("active_json_effective_b58_successor_dd9_closure",
              all(all(v.values()) for v in json_checks.values()), json_checks)

        # Side evidence is append-only and must already be present/closed; the
        # guard never creates or repairs it.
        evidence_checks: dict[str, Any] = {}
        for name, path in RECEIPTS.items():
            try:
                loaded = load_closed(path)
                value = loaded[0] if loaded else {}
                writes = value.get("writes", {})
                if name == "no_producer":
                    ok = (value.get("status") ==
                          "PASS_READ_ONLY_NO_PRODUCER_DUAL_SEED_RECONSTRUCTION__ZERO_CREDIT" and
                          value.get("reconstruction", {}).get("overlay_rows") == 1148 and
                          value.get("reconstruction", {}).get("successor_rows") == 76832 and
                          value.get("reconstruction", {}).get("parent_rows") == 862 and
                          value.get("reconstruction", {}).get("public_unresolved_after_reconstruction") == 0)
                elif name == "mutation_attacks":
                    ok = (value.get("status") ==
                          "PASS_READ_ONLY_MUTATION_ATTACKS__13_OF_13_FAIL_CLOSED__ZERO_CREDIT" and
                          value.get("attack_count") == 13 and value.get("failed_closed_count") == 13)
                else:
                    ok = value.get("status") == "PASS_DUAL_INDEPENDENT_CHECKERS_AND_TERMINAL_BYTE_REPLAY__ZERO_CREDIT"
                ok = ok and loaded is not None and value.get("formal_global_closure_credit") == 0 and \
                     value.get("D02_unlock") is False and value.get("runtime_authorized") is False and \
                     all(item is False for item in writes.values()) if writes else ok
                evidence_checks[name] = {"present_closed": loaded is not None, "passed": bool(ok),
                                         "status": value.get("status")}
            except Exception as exc:
                evidence_checks[name] = {"passed": False, "error": f"{type(exc).__name__}: {exc}"}
        check("side_evidence_closed_zero_credit", all(v.get("passed") for v in evidence_checks.values()), evidence_checks)

        tag_pyc = [str(path.relative_to(ROOT)) for path in ROOT.rglob("*.pyc") if TAG in str(path)]
        check("no_r34_pyc", not tag_pyc, tag_pyc)
        manifest = OUT / f"{BASE}_cold_launch_manifest_{TAG}.sha256"
        outer = OUT / f"{BASE}_cold_launch_outer_receipt_{TAG}.json"
        check("manifest_outer_absent", not manifest.exists() and not outer.exists(),
              {"manifest": str(manifest), "outer": str(outer)})

        passed = all(row["passed"] for row in checks)
        report: dict[str, Any] = {
            "schema": f"cm2.c79g.{TAG}.cold-freeze-preflight.v1",
            "status": ("PREFLIGHT_PASS_R34_PINS_PENDING_MANIFEST_OUTER_ABSENT__ZERO_CREDIT"
                        if passed else
                        "PREFLIGHT_FAIL_CLOSED_R34_COLD_FREEZE_GUARD"),
            "successor_suffix": TAG, "predecessor_suffix": PREV,
            "PINS_PENDING": PINS_PENDING,
            "ONE_SHOT_FREEZE_PUBLISH_ENABLED": ONE_SHOT_FREEZE_PUBLISH_ENABLED,
            "exact8": [{"path": p, "file_sha256": f, "object_sha256": o,
                        "mode": mode} for p, f, o, mode in EXACT8],
            "checks": checks, "check_count": len(checks),
            "failed_check_count": sum(not row["passed"] for row in checks),
            "manifest_created": False, "outer_created": False,
            "runtime_authorized": False, "formal_global_closure_credit": 0,
            "D02_unlock": False, "read_only": True,
        }
        report["object_sha256"] = sha(canonical(report))
        print(json.dumps(report, ensure_ascii=False, sort_keys=True))
        return 0 if passed else 1
    except Exception as exc:
        report = {
            "schema": f"cm2.c79g.{TAG}.cold-freeze-preflight.v1",
            "status": "PREFLIGHT_FAIL_CLOSED_R34_COLD_FREEZE_GUARD_EXCEPTION",
            "error": f"{type(exc).__name__}: {exc}",
            "PINS_PENDING": PINS_PENDING,
            "ONE_SHOT_FREEZE_PUBLISH_ENABLED": ONE_SHOT_FREEZE_PUBLISH_ENABLED,
            "manifest_created": False, "outer_created": False,
            "runtime_authorized": False, "formal_global_closure_credit": 0,
            "D02_unlock": False, "read_only": True,
        }
        report["object_sha256"] = sha(canonical(report))
        print(json.dumps(report, ensure_ascii=False, sort_keys=True))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
