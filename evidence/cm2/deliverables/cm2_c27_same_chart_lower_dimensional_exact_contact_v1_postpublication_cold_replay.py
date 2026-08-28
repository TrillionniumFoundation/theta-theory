#!/usr/bin/env python3
"""Cold post-publication replay for the lower-contact zero-credit bundle."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time
from typing import Any


PREFIX = "cm2_c27_same_chart_lower_dimensional_exact_contact_v1"
BASE_MANIFEST = PREFIX + "_manifest.sha256"
BASE_RECEIPT = PREFIX + "_terminal_receipt.json"
VERIFIER = PREFIX + "_independent_verifier.py"
RESULT = PREFIX + "_result.json"
COLD_VERIFICATION = PREFIX + "_postpublication_cold_replay_verification.json"
COLD_RECEIPT = PREFIX + "_postpublication_cold_replay_receipt.json"
COLD_MANIFEST = PREFIX + "_postpublication_cold_replay_manifest.sha256"


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode("ascii")


def objsha(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def filesha(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(4 << 20), b""):
            state.update(block)
    return state.hexdigest()


def stat_record(path: Path) -> dict[str, Any]:
    value = path.stat()
    return {"device": value.st_dev, "inode": value.st_ino, "mode": value.st_mode, "uid": value.st_uid, "gid": value.st_gid, "size": value.st_size, "mtime_ns": value.st_mtime_ns, "ctime_ns": value.st_ctime_ns}


def closed_json(path: Path, key: str) -> dict[str, Any]:
    raw = path.read_bytes()
    value = json.loads(raw)
    if canonical(value) != raw:
        raise RuntimeError("canonical JSON:" + path.name)
    body = dict(value)
    claimed = body.pop(key, None)
    if claimed != objsha(body):
        raise RuntimeError("JSON closure:" + path.name)
    return value


def read_manifest(root: Path) -> dict[str, str]:
    lines = (root / BASE_MANIFEST).read_text("ascii").splitlines()
    result = {}
    for line in lines:
        if len(line) < 67 or line[64:66] != "  ":
            raise RuntimeError("manifest syntax")
        pin, name = line[:64], line[66:]
        if len(pin) != 64 or any(char not in "0123456789abcdef" for char in pin) or not name or "/" in name or name in result:
            raise RuntimeError("manifest member syntax")
        if filesha(root / name) != pin:
            raise RuntimeError("manifest member hash:" + name)
        result[name] = pin
    if BASE_RECEIPT not in result or VERIFIER not in result or RESULT not in result:
        raise RuntimeError("manifest required members")
    return result


def snapshot(paths: dict[str, Path]) -> dict[str, dict[str, Any]]:
    return {name: {"sha256": filesha(path), "stat": stat_record(path)} for name, path in sorted(paths.items())}


def publish(source: Path, destination: Path) -> None:
    if destination.exists():
        if filesha(source) != filesha(destination):
            raise RuntimeError("no-replace conflict:" + destination.name)
        return
    shutil.copy2(source, destination)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--published-dir", required=True)
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--seed", required=True, type=int)
    args = parser.parse_args()
    root = Path(args.published_dir).resolve()
    run = Path(args.run_dir).resolve()
    if run.exists():
        raise RuntimeError("new cold run directory required")
    run.mkdir(parents=True)
    members = read_manifest(root)
    base_receipt = closed_json(root / BASE_RECEIPT, "receipt_sha256")
    if base_receipt["formal_credit"] != 0 or base_receipt["C27_C28_C29"] != "REBUILD_REQUIRED_AND_NOT_AUTHORIZED" or base_receipt["source_W_transition_authorized"] is not False:
        raise RuntimeError("base receipt nonpromotion")
    python = Path(sys.executable).resolve()
    wrapper = Path(__file__).resolve()
    watched = {"base_manifest": root / BASE_MANIFEST, "python": python, "wrapper": wrapper}
    watched.update({"member:" + name: root / name for name in members})
    pre = snapshot(watched)
    output = run / "verification.json"
    command = [str(python), "-I", "-S", "-B", str(root / VERIFIER), "--candidate-dir", str(root), "--output", str(output), "--seed", str(args.seed)]
    env = {"PATH": "/usr/bin:/bin", "LANG": "C", "LC_ALL": "C", "TZ": "UTC", "PYTHONHASHSEED": "0"}
    start = time.monotonic_ns()
    process = subprocess.run(command, cwd=run, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    elapsed = time.monotonic_ns() - start
    (run / "stdout.log").write_bytes(process.stdout)
    (run / "stderr.log").write_bytes(process.stderr)
    (run / "command.json").write_bytes(canonical(command))
    (run / "exit.json").write_bytes(canonical({"numeric_exit": process.returncode, "signal": -process.returncode if process.returncode < 0 else None, "elapsed_monotonic_ns": elapsed}))
    if process.returncode != 0 or process.stderr != b"":
        raise RuntimeError("cold verifier process")
    verification = closed_json(output, "verification_sha256")
    if process.stdout != canonical(verification) + b"\n":
        raise RuntimeError("cold stdout/output equality")
    expected_status = "PASS_INDEPENDENT_NONSQLITE_EXACT_T_SWEEP_MATCHES_ALL_5783708_LOWER_CONTACTS_AND_76000_ENDPOINT_ROWS__ZERO_FORMAL_CREDIT"
    if verification["status"] != expected_status or verification["verification_seed"] != args.seed:
        raise RuntimeError("cold verification status/seed")
    if verification["formal_credit"] != 0 or verification["C27_C28_C29"] != "REBUILD_REQUIRED_AND_NOT_AUTHORIZED" or verification["CM2"] != "NO-GO_FOR_CLAIM" or verification["source_W_transition_authorized"] is not False:
        raise RuntimeError("cold verification nonpromotion")
    if verification["candidate_result_sha256"] != base_receipt["producer_runs"][0]["result_sha256"]:
        raise RuntimeError("cold candidate result exact binding")
    post = snapshot(watched)
    if pre != post:
        raise RuntimeError("TOCTOU pre/post SHA+stat mismatch")
    if read_manifest(root) != members:
        raise RuntimeError("post manifest replay")

    published_verification = root / COLD_VERIFICATION
    publish(output, published_verification)
    semantic = {
        "schema": "cm2.c27.same-chart-lower-dimensional-exact-contact.v1.postpublication-cold-replay-receipt.v1",
        "status": "PASS_COLD_POSTPUBLICATION_INDEPENDENT_SWEEP__PRE_POST_SHA_STAT_IDENTICAL__ZERO_FORMAL_CREDIT",
        "scope": "SAME_CHART_LOWER_DIMENSIONAL_EXACT_CONTACT_SUBGATE_ONLY",
        "full_20_family_totality_authorized": False,
        "other_primitive_terminals_still_required": True,
        "base_manifest_sha256": filesha(root / BASE_MANIFEST), "base_manifest_member_count": len(members),
        "base_terminal_receipt_sha256": base_receipt["receipt_sha256"],
        "verification_seed": args.seed, "verification_sha256": verification["verification_sha256"],
        "verification_file_sha256": filesha(published_verification),
        "normalized_command_argv": command, "numeric_exit": process.returncode, "signal": None,
        "stderr_empty": True, "stdout_equals_canonical_verification": True, "elapsed_monotonic_ns": elapsed,
        "pre_snapshot_sha256": objsha(pre), "post_snapshot_sha256": objsha(post),
        "pre_post_sha256_identical": True, "pre_post_stat_identical": True,
        "resolved_python_sha256": pre["python"]["sha256"], "wrapper_sha256": pre["wrapper"]["sha256"],
        "complete_lower_candidate_count": verification["lower_dimensional_candidate_pair_count"],
        "C19C_endpoint_dependent_contact_count": verification["C19C_endpoint_dependent_contact_count"],
        "legal_cross_component_lower_dimensional_witness_count": verification["legal_cross_component_lower_dimensional_witness_count"],
        "formal_credit": 0, "C27_C28_C29": "REBUILD_REQUIRED_AND_NOT_AUTHORIZED", "CM2": "NO-GO_FOR_CLAIM", "source_W_transition_authorized": False,
        "required_next": "COMBINE_WITH_REMAINING_PRIMITIVE_TERMINAL_SUBGATES_BEFORE_ANY_C27_REBUILD_AUTHORIZATION",
    }
    receipt = {**semantic, "receipt_sha256": objsha(semantic)}
    receipt_path = root / COLD_RECEIPT
    if receipt_path.exists() and receipt_path.read_bytes() != canonical(receipt):
        raise RuntimeError("no-replace cold receipt conflict")
    if not receipt_path.exists():
        with receipt_path.open("xb") as stream:
            stream.write(canonical(receipt))
    supplement = [BASE_MANIFEST, COLD_VERIFICATION, COLD_RECEIPT, wrapper.name]
    manifest_bytes = "".join(f"{filesha(root / name)}  {name}\n" for name in sorted(supplement)).encode("ascii")
    manifest_path = root / COLD_MANIFEST
    if manifest_path.exists() and manifest_path.read_bytes() != manifest_bytes:
        raise RuntimeError("no-replace cold manifest conflict")
    if not manifest_path.exists():
        with manifest_path.open("xb") as stream:
            stream.write(manifest_bytes)
    print(canonical({"status": receipt["status"], "receipt_sha256": receipt["receipt_sha256"], "manifest_sha256": filesha(manifest_path)}).decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
