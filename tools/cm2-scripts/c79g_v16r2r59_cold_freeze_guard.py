#!/usr/bin/env python3
"""Read-only r59 exact8 cold-freeze guard.

The guard is intentionally a separate, version-specific implementation.  It
only reads the pinned bytes, re-runs the two independent static reviewers, and
checks the already sealed side receipts.  It never imports candidate code,
changes permissions, creates a publication file, or touches authority/credit.
"""
from __future__ import annotations

import ast
from dataclasses import dataclass
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

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "deliverables"
BASE = "cm2_round306c79g_true_global_no_producer_consumer"
TAG = "v16r2r59"
PREV = "v16r2r58"
CHECKPOINT = "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab"
SUCCESSOR = "dd9d64f3f0bd0dfd00fd399e3154517a34ba19cfb601ec749f44cbc08b03ca1b"

MANIFEST = OUT / f"{BASE}_cold_launch_manifest_{TAG}.sha256"
OUTER = OUT / f"{BASE}_cold_launch_outer_receipt_{TAG}.json"
C53 = ROOT / ".cm2-runtime/cm2-global-authority-heads/predecessor-10fb050d30c92b0f2bdcf85a30d28ff670d8efc0b48104b7f04a63c391967b41.seal"
C53_FILE_SHA = "f62483c87df4b6f4a8a2ad8dcf56febbfce9977200ce94a0ad6ce38e736aeeb3"
C53_OBJECT_SHA = "cb90ab914c3b6518384669f42d05df33c21a717596190131c6a0f5683934cbfb"


@dataclass(frozen=True)
class Pin:
    relative: str
    file_sha: str
    object_sha: str | None
    mode: int


EXACT8: tuple[Pin, ...] = (
    Pin(f"deliverables/{BASE}_v14_runtime_registry_shape_drift_rejection_supersession_receipt_v1.json",
        "aa4323027e2313f8a2eda0d6ffc039a537afe342d496d1f75cd73fcd47446c01",
        "93689e62ae36f405f045a769f4dc6f6e6fd83a16605d08299d5c3397ad657e2e", 0o444),
    Pin(f"deliverables/{BASE}_schema_{TAG}.json",
        "f10bd33759b184c0695f9beb710914635fbda779bbc27037b6703dc0a808a676", None, 0o444),
    Pin(f"deliverables/{BASE}_contract_{TAG}.json",
        "e93ca9b5e2e64d48de6d77e698756ed4afee749501ffdf651aaee57b9ee50c7d",
        "a28dbb0dcf703f72e9a60d7295efea7c7b0acfdf11d676de664d6c67fc088c60", 0o444),
    Pin(f"deliverables/{BASE}_{TAG}_semantic_source.py",
        "1a8d3b17aab88351890992fe45a6b17c2194d8a5dc4f3ad25f8ecd894538dc32", None, 0o664),
    Pin(f"deliverables/{BASE}_independent_verifier_assembler_authority_consumer_{TAG}_semantic_source.py",
        "2f0452b1dd4cb24ed058285802f6bd6f3854798a79289832cbef03b1789473cd", None, 0o664),
    Pin(f"deliverables/{BASE}_{PREV}_to_{TAG}_static_launch_transition_receipt_v1.json",
        "2c8b9d20c4af440a58837b05404be5a0a8e3f665a1a06e6aa7260a1a2ee21d2f",
        "91c4f18aa4aed1e40d5f22c055515dc16d01d232cd9819418f64a021dcec8ca2", 0o444),
    Pin(f"deliverables/{BASE}_static_audit_{TAG}.json",
        "41b0c0f0a6b40df1f2688c56fcf5222e0cebe87e46157c93b45fe4b4bffe3093",
        "61d42e9291c8e10e186d8fc3c95583e7776744dc9c910ddc3318ae5827f1fd36", 0o444),
    Pin(f"deliverables/{BASE}_cold_launch_{TAG}_semantic_source.py",
        "323bced6d33ec437b8a175f82c557bcbd9ce1831411d698643b1dce1537ade80", None, 0o664),
)

RECEIPTS = {
    "helper": OUT / f"{BASE}_{TAG}_launcher_registry_helper_version_neutral_review_receipt_v1.json",
    "no_producer": OUT / f"{BASE}_{TAG}_no_producer_dual_seed_evidence_receipt_v1.json",
    "attacks": OUT / f"{BASE}_{TAG}_mutation_attack_evidence_receipt_v1.json",
    "terminal": OUT / f"{BASE}_{TAG}_dual_checker_terminal_replay_receipt_v1.json",
}


class DuplicateKey(ValueError):
    pass


def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in items:
        if key in out:
            raise DuplicateKey(key)
        out[key] = value
    return out


def canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"), allow_nan=False).encode("utf-8")


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def stable(path: Path) -> tuple[bytes, os.stat_result]:
    fd = os.open(path, os.O_RDONLY | os.O_CLOEXEC | getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(fd)
        named = os.lstat(path)
        ident = (before.st_dev, before.st_ino, before.st_size, before.st_nlink)
        if (not stat.S_ISREG(before.st_mode) or before.st_nlink != 1 or
                ident != (named.st_dev, named.st_ino, named.st_size, named.st_nlink)):
            raise RuntimeError(f"unstable:{path}")
        chunks: list[bytes] = []
        while True:
            block = os.read(fd, 1 << 20)
            if not block:
                break
            chunks.append(block)
        after = os.fstat(fd)
        named_after = os.lstat(path)
        if ((before.st_dev, before.st_ino, before.st_size, before.st_nlink) !=
                (after.st_dev, after.st_ino, after.st_size, after.st_nlink) or
                (after.st_dev, after.st_ino) != (named_after.st_dev, named_after.st_ino) or
                sum(map(len, chunks)) != before.st_size):
            raise RuntimeError(f"identity-drift:{path}")
        return b"".join(chunks), after
    finally:
        os.close(fd)


def closed_json(path: Path) -> tuple[dict[str, Any], bytes]:
    raw, _ = stable(path)
    value = json.loads(raw.decode("utf-8"), object_pairs_hook=pairs,
                       parse_constant=lambda x: (_ for _ in ()).throw(ValueError(x)))
    if not isinstance(value, dict):
        raise ValueError(f"object-required:{path}")
    claim = value.get("object_sha256")
    body = dict(value)
    body.pop("object_sha256", None)
    if not isinstance(claim, str) or len(claim) != 64 or sha(canonical(body)) != claim:
        raise ValueError(f"object-closure:{path}")
    return value, raw


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


def run_reviewer(script: Path, seed: str) -> tuple[int, dict[str, Any] | None, bytes, str]:
    env = dict(os.environ)
    env.update({"PYTHONDONTWRITEBYTECODE": "1", "PYTHONNOUSERSITE": "1",
                "PYTHONHASHSEED": seed})
    proc = subprocess.run(["/usr/bin/python3", "-I", "-B", "-S", str(script)],
                          cwd=str(ROOT), env=env, capture_output=True, check=False,
                          timeout=180)
    value: dict[str, Any] | None = None
    try:
        parsed = json.loads(proc.stdout.decode("utf-8"), object_pairs_hook=pairs)
        if isinstance(parsed, dict):
            value = parsed
    except Exception:
        pass
    return proc.returncode, value, proc.stdout, proc.stderr.decode("utf-8", "replace")


def main() -> int:
    rows: list[dict[str, Any]] = []

    def check(name: str, passed: bool, detail: Any = None) -> None:
        row: dict[str, Any] = {"name": name, "passed": bool(passed)}
        if detail is not None:
            row["detail"] = detail
        rows.append(row)

    try:
        exact_detail: list[dict[str, Any]] = []
        exact_ok = True
        raws: dict[str, bytes] = {}
        for pin in EXACT8:
            path = ROOT / pin.relative
            first, st = stable(path)
            second, st2 = stable(path)
            value: dict[str, Any] | None = None
            if path.suffix == ".json":
                value = json.loads(first.decode("utf-8"), object_pairs_hook=pairs)
            actual_object = value.get("object_sha256") if isinstance(value, dict) else None
            ok = (first == second and sha(first) == pin.file_sha and
                  stat.S_IMODE(st.st_mode) == pin.mode and st.st_nlink == 1 and
                  (pin.object_sha is None or actual_object == pin.object_sha))
            exact_ok &= ok
            raws[pin.relative] = first
            exact_detail.append({"path": pin.relative, "file_sha256": sha(first),
                                 "object_sha256": actual_object,
                                 "mode": stat.S_IMODE(st.st_mode), "nlink": st.st_nlink,
                                 "second_read_identical": first == second,
                                 "passed": ok})
        check("exact8_stable_pins_and_pre_freeze_modes", exact_ok, exact_detail)

        c53a, c53st = stable(C53)
        c53b, _ = stable(C53)
        c53val = json.loads(c53a.decode("utf-8"), object_pairs_hook=pairs)
        c53ok = (c53a == c53b and sha(c53a) == C53_FILE_SHA and
                 c53st.st_nlink == 1 and stat.S_IMODE(c53st.st_mode) == 0o444 and
                 isinstance(c53val, dict) and
                 c53val.get("authority_seal_object_sha256") == C53_OBJECT_SHA)
        check("c53_unchanged_and_pinned", c53ok,
              {"file_sha256": sha(c53a), "object_sha256": c53val.get("authority_seal_object_sha256"),
               "second_read_identical": c53a == c53b})

        # Parse/compile only in memory; candidate modules are never imported.
        compile_ok = True
        compile_detail: dict[str, Any] = {}
        for pin in EXACT8:
            if not pin.relative.endswith(".py"):
                continue
            try:
                ast.parse(raws[pin.relative].decode("utf-8"), filename=pin.relative)
                compile(ast.parse(raws[pin.relative].decode("utf-8"), filename=pin.relative),
                        pin.relative, "exec")
                compile_detail[pin.relative] = True
            except Exception as exc:
                compile_ok = False
                compile_detail[pin.relative] = f"{type(exc).__name__}: {exc}"
        check("exact8_source_ast_and_memory_compile", compile_ok, compile_detail)

        reviewer_a = ROOT / "scripts/c79g_v16r2r59_role_aware_reviewer.py"
        reviewer_b = ROOT / "scripts/c79g_v16r2r59_helper_reviewer_b.py"
        reviewer_detail: dict[str, Any] = {}
        reviewers_ok = True
        for label, script in (("A", reviewer_a), ("B", reviewer_b)):
            runs: list[dict[str, Any]] = []
            for seed in ("1", "99991"):
                rc, value, raw, stderr = run_reviewer(script, seed)
                if label == "A":
                    accepted = (rc == 0 and isinstance(value, dict) and
                                value.get("status") == "PASS_DUAL_STATIC_CANDIDATE_34_OF_34__VERSION_NEUTRAL_HELPER_GO__RUNTIME_NOT_AUTHORIZED" and
                                value.get("check_count") == 34 and value.get("failed_check_count") == 0 and
                                value.get("formal_global_closure_credit") == 0 and
                                value.get("D02_unlock") is False and value.get("runtime_authorized") is False)
                else:
                    accepted = (rc == 0 and isinstance(value, dict) and
                                value.get("status") == "PASS_VERSION_NEUTRAL_HELPER_REVIEW_B__ZERO_CREDIT" and
                                value.get("failed_checks") == [] and
                                value.get("formal_global_closure_credit") == 0 and
                                value.get("D02_unlock") is False and value.get("runtime_authorized") is False)
                reviewers_ok &= accepted
                runs.append({"seed": int(seed), "return_code": rc, "accepted": accepted,
                             "report_sha256": sha(raw), "status": value.get("status") if value else None,
                             "stderr_tail": stderr[-240:]})
            if len(runs) != 2 or runs[0]["report_sha256"] != runs[1]["report_sha256"]:
                reviewers_ok = False
            reviewer_detail[label] = runs
        check("independent_r59_A_B_dual_seed_static_review", reviewers_ok, reviewer_detail)

        # Closed active JSON semantics: every effective checkpoint is b58 and
        # every explicit successor checkpoint is dd9.
        semantic_detail: dict[str, Any] = {}
        semantic_ok = True
        for pin in EXACT8:
            if not pin.relative.endswith(".json"):
                continue
            if pin.object_sha is None:
                raw, _ = stable(ROOT / pin.relative)
                value = json.loads(raw.decode("utf-8"), object_pairs_hook=pairs)
                if not isinstance(value, dict):
                    raise ValueError(f"object-required:{pin.relative}")
            else:
                value, _ = closed_json(ROOT / pin.relative)
            effective_values = [x for x in walk_key(value, "effective_checkpoint_object_sha256")]
            successor_values = [x for x in walk_key(value, "successor_checkpoint_object_sha256")]
            # The historical v14 witness intentionally has null successor/effective
            # fields; only r59 active JSONs are subject to the current path gate.
            # The closed schema contains illustrative checkpoint-shaped
            # examples; it is not a live protocol path.  Current-path pins
            # apply to the contract/transition/audit receipts only.
            if TAG in pin.relative and not pin.relative.endswith(f"_schema_{TAG}.json"):
                good = (all(x == CHECKPOINT for x in effective_values) and
                        (not successor_values or all(x == SUCCESSOR for x in successor_values)))
                semantic_detail[pin.relative] = {"effective_count": len(effective_values),
                                                   "successor_count": len(successor_values),
                                                   "effective_b58": all(x == CHECKPOINT for x in effective_values),
                                                   "successor_dd9": all(x == SUCCESSOR for x in successor_values),
                                                   "passed": good}
                semantic_ok &= good
        check("r59_current_json_checkpoint_and_successor_closure", semantic_ok, semantic_detail)

        evidence_detail: dict[str, Any] = {}
        evidence_ok = True
        expected_status = {
            "helper": "PASS_R59_DUAL_INDEPENDENT_VERSION_NEUTRAL_HELPER_REVIEW__ZERO_CREDIT",
            "no_producer": "PASS_READ_ONLY_NO_PRODUCER_DUAL_SEED_RECONSTRUCTION__ZERO_CREDIT",
            "attacks": "PASS_R59_STATIC_ATTACK_ENUMERATION_137_OF_137__LEGACY_13_FAIL_CLOSED__RUNTIME_EXECUTION_DEFERRED__ZERO_CREDIT",
            "terminal": "PASS_R59_DUAL_INDEPENDENT_CHECKERS_AND_TERMINAL_BYTE_REPLAY__ZERO_CREDIT__COLD_FREEZE_PENDING",
        }
        expected_source_hashes = {p.relative: p.file_sha for p in EXACT8 if TAG in p.relative}
        for label, path in RECEIPTS.items():
            value, _ = closed_json(path)
            writes = value.get("writes", {})
            writes_ok = all(v is False for v in writes.values()) if writes else True
            hashes = value.get("source_hashes", {})
            hash_ok = all(hashes.get(k) == v for k, v in expected_source_hashes.items()) if hashes else True
            ok = (value.get("status") == expected_status[label] and
                  value.get("formal_global_closure_credit") == 0 and
                  value.get("D02_unlock") is False and value.get("runtime_authorized") is False and
                  writes_ok and hash_ok)
            if label == "no_producer":
                recon = value.get("reconstruction", {})
                ok &= (recon.get("overlay_rows") == 1148 and recon.get("successor_rows") == 76832 and
                       recon.get("parent_rows") == 862 and recon.get("public_unresolved_after_reconstruction") == 0 and
                       value.get("attack_execution_observed") is False)
            if label == "attacks":
                enum = value.get("enumeration", {})
                ok &= (enum.get("count") == 137 and enum.get("checker_A_count") == 137 and
                       enum.get("checker_B_count") == 137 and enum.get("execution_observed") is False and
                       value.get("execution_blocker", {}).get("kind") == "NORMATIVE_COLD_RUNTIME_137_MUTATION_EXECUTION_NOT_OBSERVED")
            evidence_ok &= bool(ok)
            evidence_detail[label] = {"path": str(path.relative_to(ROOT)), "passed": bool(ok),
                                      "status": value.get("status"), "object_sha256": value.get("object_sha256"),
                                      "writes": writes}
        check("sealed_side_receipts_closed_zero_credit", evidence_ok, evidence_detail)

        pyc = [str(p.relative_to(ROOT)) for p in ROOT.rglob("*.pyc") if TAG in str(p)]
        check("no_r59_pyc_or_tagged_runtime_residue", not pyc, pyc)
        runtime_residue = []
        runtime = ROOT / ".cm2-runtime"
        if runtime.exists():
            runtime_residue = [str(p.relative_to(ROOT)) for p in runtime.rglob("*") if TAG in str(p)]
        check("no_r59_runtime_surface", not runtime_residue, runtime_residue)
        check("manifest_and_outer_absent_before_freeze", not MANIFEST.exists() and not OUTER.exists(),
              {"manifest": str(MANIFEST.relative_to(ROOT)), "outer": str(OUTER.relative_to(ROOT))})

        passed = all(row["passed"] for row in rows)
        report: dict[str, Any] = {
            "schema": f"cm2.c79g.{TAG}.cold-freeze-preflight.v1",
            "status": ("PREFLIGHT_PASS_R59_PINS_PENDING_MANIFEST_OUTER_ABSENT__ZERO_CREDIT"
                        if passed else "PREFLIGHT_FAIL_CLOSED_R59_COLD_FREEZE_GUARD"),
            "successor_suffix": TAG, "predecessor_suffix": PREV,
            "exact8": [{"path": p.relative, "file_sha256": p.file_sha,
                        "object_sha256": p.object_sha, "mode": p.mode} for p in EXACT8],
            "checks": rows, "check_count": len(rows),
            "failed_check_count": sum(not r["passed"] for r in rows),
            "manifest_created": False, "outer_created": False,
            "runtime_authorized": False, "formal_global_closure_credit": 0,
            "D02_unlock": False, "read_only": True,
            "normative_137_runtime_execution_observed": False,
        }
        report["object_sha256"] = sha(canonical(report))
        print(json.dumps(report, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
        return 0 if passed else 1
    except Exception as exc:
        report = {
            "schema": f"cm2.c79g.{TAG}.cold-freeze-preflight.v1",
            "status": "PREFLIGHT_FAIL_CLOSED_R59_COLD_FREEZE_GUARD_EXCEPTION",
            "error": f"{type(exc).__name__}: {exc}",
            "check_count": len(rows), "failed_check_count": len(rows),
            "manifest_created": False, "outer_created": False,
            "runtime_authorized": False, "formal_global_closure_credit": 0,
            "D02_unlock": False, "read_only": True,
        }
        report["object_sha256"] = sha(canonical(report))
        print(json.dumps(report, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
