#!/usr/bin/env python3
"""r45 append-only clean-room builder.

The r44 static bytes are a rejected predecessor.  This builder never reads
them as candidate inputs: it retags the pinned r39 partial bytes in memory and
uses r44 only as an immutable chain witness.  Before installation it
recomputes the r42 ``-I -B`` guard report twice and seals the complete report
and its exact missing-side-evidence vector as a fresh r45 witness.
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
os.environ.update({"PYTHONDONTWRITEBYTECODE": "1", "PYTHONNOUSERSITE": "1"})

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "deliverables"
BASE = "cm2_round306c79g_true_global_no_producer_consumer"
TEMPLATE = "v16r2r39"
TEMPLATE_PREV = "v16r2r38"
PREV = "v16r2r44"
TAG = "v16r2r45"
UPSTREAM = "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab"
SUCCESSOR_PIN = "dd9d64f3f0bd0dfd00fd399e3154517a34ba19cfb601ec749f44cbc08b03ca1b"

R44_ANCHOR = OUT / f"{BASE}_v16r2r44_active_predecessor_supersession_receipt_v1.json"
# r44 itself has no rejection receipt yet: this r45 install seals that
# predecessor rejection exactly once, before creating the r44->r45 edge.
R44_SUP = OUT / f"{BASE}_v16r2r43_to_v16r2r44_static_bundle_rejection_supersession_receipt_v1.json"
R44_TRANSITION = OUT / f"{BASE}_v16r2r43_to_v16r2r44_static_launch_transition_receipt_v1.json"
R44_SCHEMA = OUT / f"{BASE}_schema_v16r2r44.json"
R44_TOOLING = ROOT / "scripts/c79g_v16r2r44_candidate_builder.py"

R44_ANCHOR_SHA = "19514a07b5cc65167e7805b73779bd0726ddc6ec023f7456fec120ca3427f316"
R44_ANCHOR_OBJECT = "5a16d62b835f118d309767dd10cdb2f8faa6f9631897edac451b1348d822178d"
R44_SUP_SHA = "339cb3404f376118418df99cf88617785fbc3da3b9757cbe5c0a352113f10a63"
R44_SUP_OBJECT = "956584c99940d7280736bef01ba79f3877f54840fabb01ae5772fd83f781b649"
R44_TRANSITION_SHA = "659d6d28718af8f5d6c04d68dd1d786da82a381b1aa382697e90d77ef0eef5ed"
R44_TRANSITION_OBJECT = "ea3c6a15f89b6d38da1cb21ae266396c6f4d4a82172bc1178dccaf778ec569f9"
R44_SCHEMA_SHA = "74939d8ac33545a775bdd4bdb537628fdc7ebf4b393d5e611b5c07d3eec17084"

R42_GUARD = ROOT / "scripts/c79g_v16r2r42_cold_freeze_guard.py"
R42_CONFIG = ROOT / "scripts/config/c79g_v16r2r42_cold_freeze_config.json"
R42_REPORT_OBJECT = "1d0ab79ad8edbd549f020baafa8671f6d4cca573ff2b944736a84b7a8937bd50"
R42_REPORT_RAW = "538269b4f5d8700304e33292a9578b1d14f77cfdfd3e6726300e79da4fe92097"
R42_REPORT_BYTES = 9873
LEGACY_R42_OBJECT = "19ed0012556cd3db6f04183ebdd0bd542aef1fe62d6a4ab13cda0dc909e38452"


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
            part = os.read(fd, 1 << 20)
            if not part: break
            chunks.append(part)
        after = os.fstat(fd); named_after = os.lstat(path)
        if ((before.st_dev, before.st_ino, before.st_size) !=
                (after.st_dev, after.st_ino, after.st_size) or
                (before.st_dev, before.st_ino) !=
                (named_after.st_dev, named_after.st_ino)):
            raise RuntimeError(f"drift:{path}")
        raw = b"".join(chunks)
        if len(raw) != before.st_size: raise RuntimeError(f"short:{path}")
        return raw
    finally:
        os.close(fd)


def pyc_inventory() -> dict[str, str]:
    result = {}
    for p in ROOT.rglob("*.pyc"):
        try: result[str(p.relative_to(ROOT))] = sha(stable(p))
        except OSError: result[str(p.relative_to(ROOT))] = "UNREADABLE"
    return result


def load_r44_tooling() -> dict[str, Any]:
    raw = stable(R44_TOOLING).decode("utf-8")
    tree = ast.parse(raw, filename=str(R44_TOOLING)); compile(tree, str(R44_TOOLING), "exec")
    ns: dict[str, Any] = {"__name__": "_r45_r44_tooling", "__file__": str(R44_TOOLING), "__package__": None}
    exec(compile(tree, str(R44_TOOLING), "exec"), ns, ns)
    # Rebind only tooling globals.  Candidate inputs remain the immutable r39
    # files configured by the reviewed r40 constructor.
    ns.update({
        "PREV": PREV, "TAG": TAG,
        "R43_ANCHOR": R44_ANCHOR, "R43_SUP": R44_SUP,
        "R43_TRANSITION": R44_TRANSITION, "R43_SCHEMA": R44_SCHEMA,
        "R43_ANCHOR_SHA256": R44_ANCHOR_SHA,
        "R43_ANCHOR_OBJECT_SHA256": R44_ANCHOR_OBJECT,
        "R43_SUP_SHA256": R44_SUP_SHA, "R43_SUP_OBJECT_SHA256": R44_SUP_OBJECT,
        "R43_TRANSITION_SHA256": R44_TRANSITION_SHA,
        "R43_SCHEMA_SHA256": R44_SCHEMA_SHA,
        "R43_SCHEMA_OBJECT_SHA256": "__schema_object_not_required__",
        "SCHEMA_DESCRIPTION": f"Append-only {TAG} schema.  Active predecessor chain and C53 root remain pinned; runtime authority is disabled.",
    })
    return ns


def check_r44_chain() -> None:
    expected = [(R44_ANCHOR, R44_ANCHOR_SHA, R44_ANCHOR_OBJECT),
                (R44_SUP, R44_SUP_SHA, R44_SUP_OBJECT),
                (R44_TRANSITION, R44_TRANSITION_SHA, R44_TRANSITION_OBJECT),
                (R44_SCHEMA, R44_SCHEMA_SHA, None)]
    for path, fh, oh in expected:
        raw = stable(path)
        if sha(raw) != fh or stat.S_IMODE(path.stat().st_mode) != 0o444 or path.stat().st_nlink != 1:
            raise RuntimeError(f"r44 predecessor drift:{path}")
        if path.suffix == ".json":
            value = json.loads(raw.decode())
            if oh is not None and value.get("object_sha256") != oh: raise RuntimeError(f"r44 object drift:{path}")
            if path != R44_SCHEMA and (value.get("formal_global_closure_credit") not in (0, False, None) or value.get("D02_unlock") is True or value.get("runtime_authorized") is True):
                raise RuntimeError(f"r44 nonzero predecessor:{path}")
    a = json.loads(stable(R44_ANCHOR).decode()); s = json.loads(stable(R44_SUP).decode())
    if a.get("predecessor_namespace") != "v16r2r43" or a.get("successor_namespace") != "v16r2r44_semantic_source": raise RuntimeError("r44 anchor direction")
    if s.get("predecessor_namespace") != "v16r2r43" or s.get("successor_namespace") != "v16r2r44": raise RuntimeError("r44 supersession direction")


def recompute_guard_witness() -> dict[str, Any]:
    before = pyc_inventory(); reports = []
    command = ["/usr/bin/python3", "-I", "-B", str(R42_GUARD), "--config", str(R42_CONFIG), "--preflight"]
    for seed in (1, 99991):
        env = dict(os.environ); env.update({"PYTHONHASHSEED": str(seed), "PYTHONDONTWRITEBYTECODE": "1", "PYTHONNOUSERSITE": "1"})
        proc = subprocess.run(command, cwd=str(ROOT), env=env, capture_output=True, check=False)
        if proc.returncode != 1: raise RuntimeError(f"r42 guard rc:{proc.returncode}")
        lines = [x for x in proc.stdout.decode().splitlines() if x.strip()]
        if len(lines) != 1: raise RuntimeError("r42 guard output cardinality")
        reports.append((proc.stdout, json.loads(lines[0])))
    after = pyc_inventory()
    if before != after: raise RuntimeError("r42 guard changed pyc inventory")
    report = reports[0][1]
    for _, other in reports[1:]:
        if canon(other) != canon(report): raise RuntimeError("r42 seed report drift")
    body = dict(report); claim = body.pop("object_sha256", None)
    if claim != R42_REPORT_OBJECT or sha(canon(body)) != R42_REPORT_OBJECT: raise RuntimeError("r42 report object witness")
    if report.get("status") != "PREFLIGHT_FAIL_CLOSED_V16R2R42_COLD_FREEZE_GUARD" or report.get("check_count") != 7 or report.get("failed_check_count") != 1: raise RuntimeError("r42 report status")
    failed = [x for x in report.get("checks", []) if x.get("passed") is False]
    if len(failed) != 1 or failed[0].get("name") != "side_evidence_closed_zero_credit": raise RuntimeError("r42 failed vector")
    detail = failed[0].get("detail", {})
    for key in ("no_producer", "mutation_attacks", "terminal_replay"):
        if detail.get(key) != {"passed": False, "present_closed": False, "status": None}: raise RuntimeError("r42 side vector")
    cfg = json.loads(stable(R42_CONFIG).decode()); paths = []
    for key in ("no_producer", "mutation_attacks", "terminal_replay"):
        rel = cfg["evidence_receipts"][key]; p = ROOT / rel
        if p.exists(): raise RuntimeError(f"historical evidence unexpectedly exists:{p}")
        paths.append({"key": key, "path": rel, "exists": False})
    raw0 = reports[0][0]
    if len(raw0) != R42_REPORT_BYTES or sha(raw0) != R42_REPORT_RAW: raise RuntimeError("r42 raw witness")
    return {"schema": f"cm2.c79g.{TAG}.r42-guard-witness.v1", "status": "RECOMPUTED_R42_PREFLIGHT_FAIL_CLOSED__ZERO_CREDIT", "guard_report": report, "guard_report_object_sha256": R42_REPORT_OBJECT, "guard_report_raw_sha256": R42_REPORT_RAW, "guard_report_raw_bytes": R42_REPORT_BYTES, "guard_exit_code": 1, "replay_seeds": [1, 99991], "raw_sha256_equal": True, "failed_check_count": 1, "failed_checks": ["side_evidence_closed_zero_credit"], "side_evidence": paths, "recomputed_witness": True, "recomputed_under_I_B": True, "legacy_historical_failure": {"reason": "R42_COLD_FREEZE_GUARD_PYC_FAIL_CLOSED", "legacy_object_sha256": LEGACY_R42_OBJECT, "legacy_full_body_available": False}, "formal_global_closure_credit": 0, "D02_unlock": False, "runtime_authorized": False, "manifest_created": False, "outer_created": False}


def static_self_check() -> dict[str, Any]:
    check_r44_chain()
    tool = load_r44_tooling()
    witness = recompute_guard_witness()
    ns = tool["load_r40_constructor"](); ns["PREV"] = PREV; ns["TAG"] = TAG
    schema = json.loads(stable(OUT / f"{BASE}_schema_{TEMPLATE}.json").decode())
    fixed = tool["_schema_residue_fix"](schema, ns)
    if fixed.get("$id") != f"cm2.round306c79g.true-global-no-producer-consumer.{TAG}.schema": raise RuntimeError("r45 schema retag")
    for role, rel in (("producer", f"{BASE}_{TEMPLATE}_semantic_source.py"), ("consumer", f"{BASE}_independent_verifier_assembler_authority_consumer_{TEMPLATE}_semantic_source.py"), ("launcher", f"{BASE}_cold_launch_{TEMPLATE}_semantic_source.py")):
        text = ns["retag_source"](stable(OUT / rel).decode())
        if f"{BASE}_{PREV}_to_{TAG}_static_launch_transition_receipt_v1.json" not in text or f"{BASE}_{TAG}_active_predecessor_supersession_receipt_v1.json" not in text: raise RuntimeError(f"{role} r45 active edge")
    targets = [OUT / f"{BASE}_{TAG}_semantic_source.py", OUT / f"{BASE}_independent_verifier_assembler_authority_consumer_{TAG}_semantic_source.py", OUT / f"{BASE}_cold_launch_{TAG}_semantic_source.py", OUT / f"{BASE}_schema_{TAG}.json", OUT / f"{BASE}_contract_{TAG}.json", OUT / f"{BASE}_{PREV}_to_{TAG}_static_launch_transition_receipt_v1.json", OUT / f"{BASE}_static_audit_{TAG}.json", OUT / f"{BASE}_{TAG}_r42_guard_witness_receipt_v1.json"]
    if any(p.exists() for p in targets): raise RuntimeError("r45 target already exists")
    if any(TAG in p for p in pyc_inventory()): raise RuntimeError("r45 pyc preexists")
    return {"status": "PASS_R45_CLEAN_ROOM_RECOMPUTED_GUARD_WITNESS_STATIC_ONLY", "target_namespace": TAG, "predecessor_namespace": PREV, "witness": witness, "formal_global_closure_credit": 0, "D02_unlock": False, "runtime_authorized": False, "installation_performed": False}


def _install() -> int:
    tool = load_r44_tooling(); ns = tool["load_r40_constructor"](); original = ns["configure"]
    def configure(module: Any, b: Any) -> None:
        original(module, b); tool["_configure_r44"](ns, b)
    ns["configure"] = configure
    def seal(b: Any) -> dict[str, str]:
        witness = recompute_guard_witness(); wp = OUT / f"{BASE}_{TAG}_r42_guard_witness_receipt_v1.json"; wr = canon(witness) + b"\n"; b.install(wp, wr)
        path = OUT / f"{BASE}_{PREV}_static_bundle_rejection_receipt_v1.json"; ar = stable(R44_ANCHOR); av = json.loads(ar.decode())
        value = b.close({"schema": f"cm2.c79g.{PREV}.publication-witness-rejection.v1", "status": f"PERMANENT_FAIL_CLOSED_{PREV.upper()}_WITNESS_REMEDIATION__ZERO_CREDIT", "failed_namespace": PREV, "rejection_reason": "R44_R42_GUARD_WITNESS_NOT_INDEPENDENTLY_GROUNDED_FAIL_CLOSED", "detail": {"anchor_path": str(R44_ANCHOR.relative_to(ROOT)), "anchor_file_sha256": sha(ar), "anchor_object_sha256": av.get("object_sha256"), "witness_path": str(wp.relative_to(ROOT)), "witness_file_sha256": sha(wr), "witness_object_sha256": witness.get("object_sha256"), "recomputed_report_object_sha256": R42_REPORT_OBJECT, "legacy_unverified_object_sha256": LEGACY_R42_OBJECT, "runtime_protocol_executed": False}, "append_only": True, "overwrite_delete_or_reuse_allowed": False, "runtime_authorized": False, "formal_global_closure_credit": 0, "D02_unlock": False, "manifest_created": False, "outer_created": False, "runtime_surface_created": False})
        raw = b.canon(value) + b"\n"; action = b.install(path, raw); installed, iraw = b.load(path); return {"action": action, "file_sha256": b.sha(iraw), "object_sha256": installed["object_sha256"]}
    ns["seal_r39_rejection"] = seal
    return int(ns["main"]())


def main() -> int:
    try:
        result = static_self_check()
        if "--install" in sys.argv[1:]: return _install()
        print(json.dumps(result, ensure_ascii=False, sort_keys=True)); return 0
    except Exception as exc:
        print(json.dumps({"status": "FAIL_CLOSED_R45_CLEAN_ROOM_STATIC_ONLY", "error": {"type": type(exc).__name__, "message": str(exc)}, "installation_performed": False, "formal_global_closure_credit": 0, "D02_unlock": False}, ensure_ascii=False, sort_keys=True)); return 1


if __name__ == "__main__": raise SystemExit(main())
