#!/usr/bin/env python3
"""Terminal runner for the independent T00 v2 verifier."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
PYTHON = Path("/usr/bin/python3.12")
PYTHON_SHA = "1643dacd9feaedc58f3cc581e4d22577dfe25c09b10282936186ccf0f2e61118"
VERIFIER = ROOT / "deliverables/cm2_c27_primitive_v5_actual_t00_same_chart_exact_contact_adapter_v2_independent_verifier.py"
VERIFIER_SHA = "775ddcebebc8758d2fe70a28e0c34c02767d65f4f01235898396eeca92a2731b"


class Failure(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Failure(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def fsha(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(4 << 20):
            state.update(block)
    return state.hexdigest()


def stat_wire(path: Path) -> list[int]:
    info = path.stat()
    return [info.st_dev, info.st_ino, info.st_size, info.st_mtime_ns,
            info.st_ctime_ns, info.st_mode, info.st_uid, info.st_gid]


def receipt_paths(path: Path) -> set[Path]:
    receipt = json.loads(path.read_bytes())
    result = {path, path.parent / "manifest.sha256"}
    for key in ("primitive_authority_ledger", "candidate_ownership_ledger",
                "materialized_physical_proof_fragment_ledger"):
        result.add((ROOT / receipt["terminal_adapter"][key]["path"]).resolve())
    for item in receipt["root_input_capture"]["attestations"].values():
        result.add((ROOT / item["path"]).resolve())
    return result


def snapshot(paths: set[Path]) -> dict[str, Any]:
    result = {}
    for path in sorted(paths):
        need(path.is_file(), "snapshot file")
        if ROOT in path.parents:
            label = str(path.relative_to(ROOT))
        else:
            need(path == PYTHON, "external snapshot path is pinned runtime")
            label = str(path)
        result[label] = {
            "sha256": fsha(path), "stat": stat_wire(path)}
    return result


def run(args: argparse.Namespace) -> dict[str, Any]:
    receipt = Path(args.receipt).resolve()
    second = Path(args.second_receipt).resolve()
    run1 = Path(args.run_attestation).resolve()
    run2 = Path(args.second_run_attestation).resolve()
    temporary = Path(args.temporary_db).resolve()
    output = Path(args.output).resolve()
    run_dir = Path(args.run_dir).resolve()
    need(not output.exists() and not temporary.exists() and not run_dir.exists(),
         "fresh verifier run paths")
    need(fsha(PYTHON) == PYTHON_SHA and fsha(VERIFIER) == VERIFIER_SHA,
         "runtime/verifier pins")
    paths = receipt_paths(receipt) | receipt_paths(second)
    paths.update((run1, run2, VERIFIER, PYTHON))
    pre = snapshot(paths)
    run_dir.mkdir(parents=True)
    command = [str(PYTHON), "-B", str(VERIFIER),
               "--receipt", str(receipt),
               "--second-receipt", str(second),
               "--run-attestation", str(run1),
               "--second-run-attestation", str(run2),
               "--temporary-db", str(temporary), "--output", str(output)]
    (run_dir / "command.json").write_bytes(canonical(command) + b"\n")
    completed = subprocess.run(command, cwd=ROOT, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, check=False)
    (run_dir / "stdout.log").write_bytes(completed.stdout)
    (run_dir / "stderr.log").write_bytes(completed.stderr)
    (run_dir / "exit_code.txt").write_text(str(completed.returncode) + "\n",
                                            encoding="ascii")
    need(completed.returncode == 0 and completed.stderr == b"",
         "verifier exit0/stderr empty")
    need(len(completed.stdout.splitlines()) == 1,
         "verifier single stdout result")
    verification = json.loads(output.read_bytes())
    body = dict(verification)
    claim = body.pop("verification_sha256", None)
    need(claim == digest(body)
         and verification["status"].startswith("PASS_NO_PRODUCER_IMPORT")
         and verification["formal_credit"] == 0,
         "verification closure/status")
    post = snapshot(paths)
    need(pre == post, "verifier pre/post input identity")
    stable = {"numeric_exit_code": 0, "signal": None,
              "stderr_empty": True, "stdout_line_count": 1,
              "runtime_path": str(PYTHON), "runtime_sha256": PYTHON_SHA,
              "pre_post_sha256_identical": True,
              "pre_post_stat_identical": True,
              "verification_file_sha256": fsha(output),
              "verification_object_sha256": verification["verification_sha256"]}
    body = {
        "schema": "cm2.c27-independent.primitive-v5-actual-t00-same-chart-exact-contact-adapter-v2-verifier-run-attestation.v1",
        "status": "PASS_VERIFIER_EXIT0_SIGNAL_NULL_STDERR_EMPTY_PRE_POST_IDENTITY__ZERO_CREDIT",
        "run": stable, "input_pre": pre, "input_post": post,
        "formal_credit": 0, "manifest_authorized": False,
        "C27_C28_C29": "UNAUTHORIZED", "CM2": "NO-GO_FOR_CLAIM",
        "runner_source_sha256": fsha(Path(__file__).resolve())}
    result = dict(body)
    result["run_attestation_sha256"] = digest(result)
    (run_dir / "run_attestation.json").write_bytes(canonical(result) + b"\n")
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--receipt", required=True)
    parser.add_argument("--second-receipt", required=True)
    parser.add_argument("--run-attestation", required=True)
    parser.add_argument("--second-run-attestation", required=True)
    parser.add_argument("--temporary-db", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--run-dir", required=True)
    args = parser.parse_args()
    try:
        result = run(args)
    except (Failure, KeyError, TypeError, ValueError, OSError,
            json.JSONDecodeError) as error:
        print("FAIL:" + str(error))
        return 2
    print(canonical({"status": result["status"], "run": result["run"],
                     "run_attestation_sha256":
                         result["run_attestation_sha256"]}).decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
