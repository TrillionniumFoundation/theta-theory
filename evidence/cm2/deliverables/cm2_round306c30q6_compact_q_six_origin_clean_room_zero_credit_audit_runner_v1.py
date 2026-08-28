#!/usr/bin/env python3
"""Append-only audit runner for the C30q6 zero-credit research census."""

from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
import tempfile
import time
from typing import Any


sys.dont_write_bytecode = True
HERE = Path(__file__).absolute().parent
ROOT = HERE.parent
PYTHON = Path(sys.executable).resolve(strict=True)
PRODUCER = HERE / "cm2_round306c30q6_compact_q_six_origin_clean_room_zero_credit_gate_v1.py"
VERIFIER = HERE / "cm2_round306c30q6_compact_q_six_origin_clean_room_zero_credit_independent_verifier_v1.py"
ATTACK = HERE / "cm2_round306c30q6_compact_q_six_origin_clean_room_zero_credit_coherent_attack_harness_v1.py"
SOURCE_PINS = {
    PRODUCER: "3f9eeaf6043d7247d7f493a58aef7e384388b9936988fd32b58934e0407f9890",
    VERIFIER: "6ee4adb36cd071ba5015281508416c45e7ab70788f8165535c6339e6f4515351",
    ATTACK: "44cc2d9ce21b4216f083ac34b5e9d2454ccc05e28ad6e6a32f453fcb8274de93",
}
SEEDS = (30660061, 30660947)
COLD_SEED = 30669991
MANIFESTS = {
    ROOT / "deliverables/cm2_round306c30b_source_w_outgoing_h_whole_origin_disposition_manifest.sha256": ROOT / "deliverables",
    ROOT / ".cm2-runtime/audit/c30q3-south-theorem-zero-credit-v1-20260808T064505Z/manifest.sha256": ROOT / ".cm2-runtime/audit/c30q3-south-theorem-zero-credit-v1-20260808T064505Z",
    ROOT / ".cm2-runtime/audit/c30q4-11010111-universal-containment-zero-credit-v1-20260808T070947Z/manifest.sha256": ROOT / ".cm2-runtime/audit/c30q4-11010111-universal-containment-zero-credit-v1-20260808T070947Z",
    ROOT / ".cm2-runtime/audit/c30q5-11010101-clipped-graph-zero-credit-v1-20260808T075621Z/manifest.sha256": ROOT / ".cm2-runtime/audit/c30q5-11010101-clipped-graph-zero-credit-v1-20260808T075621Z",
}


class Reject(RuntimeError):
    pass


def need(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise Reject(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False, allow_nan=False).encode("utf-8")


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def identity(path: Path) -> tuple[int, ...]:
    info = os.lstat(path)
    return (info.st_dev, info.st_ino, info.st_mode, info.st_nlink, info.st_size,
            info.st_mtime_ns, info.st_ctime_ns, info.st_uid, info.st_gid)


def safe_file(path: Path) -> None:
    absolute = path.absolute()
    need(absolute.resolve(strict=True) == absolute, "canonical input:" + str(path))
    info = os.lstat(absolute)
    need(stat.S_ISREG(info.st_mode) and info.st_nlink == 1,
         "regular single-link input:" + str(path))
    need(absolute.is_relative_to(ROOT), "workspace scope:" + str(path))


def manifest_members(manifest: Path, base: Path) -> set[Path]:
    safe_file(manifest)
    result = {manifest}
    seen: set[str] = set()
    for row in manifest.read_text("ascii").splitlines():
        need(len(row) >= 67 and row[64:66] == "  ", "manifest row")
        relative = row[66:]
        part = Path(relative)
        need(not part.is_absolute() and ".." not in part.parts and relative not in seen,
             "manifest path")
        seen.add(relative)
        workspace = ROOT / part
        result.add(workspace if workspace.exists() else base / part)
    return result


def tracked_inputs() -> list[Path]:
    paths: set[Path] = {HERE / Path(__file__).name, PRODUCER, VERIFIER, ATTACK}
    for manifest, base in MANIFESTS.items():
        paths.update(manifest_members(manifest, base))
    paths.update({
        ROOT / ".cm2-runtime/audit/c30q0-representative-analytic-v2-20260807T1021/stdout.json",
        ROOT / ".cm2-runtime/audit/c30q0-independent-v1-20260807T105735/verifier_stdout.json",
        ROOT / ".cm2-runtime/audit/c30q0-independent-v1-20260807T105735/harness_stdout.json",
        ROOT / ".cm2-runtime/audit/c30q1-cohort-counterexample-v3-20260807T1205/seed30630071_stdout.json",
        ROOT / ".cm2-runtime/audit/c30q1-cohort-counterexample-v3-20260807T1205/seed30630929_stdout.json",
        ROOT / ".cm2-runtime/audit/c30q2-seven-cohort-routing-v3-20260807T1325/seed30630071_stdout.json",
        ROOT / ".cm2-runtime/audit/c30q2-seven-cohort-routing-v3-20260807T1325/seed30630929_stdout.json",
    })
    for name in ("c30q0-independent-v1-20260807T105735",
                 "c30q1-cohort-counterexample-v3-20260807T1205",
                 "c30q2-seven-cohort-routing-v3-20260807T1325"):
        directory = ROOT / ".cm2-runtime/audit" / name
        for pattern in ("pre.sha256", "post.sha256", "pre.stat", "post.stat",
                        "*_exit_code.txt", "*_stderr.log"):
            paths.update(directory.glob(pattern))
    output = sorted(path.absolute() for path in paths)
    for path in output:
        safe_file(path)
    return output


def snapshot(paths: list[Path]) -> tuple[bytes, bytes]:
    hash_rows: list[str] = []
    stat_rows: list[dict[str, Any]] = []
    for path in paths:
        before = identity(path)
        raw = path.read_bytes()
        after = identity(path)
        need(before == after, "stable snapshot:" + str(path))
        relative = str(path.relative_to(ROOT))
        hash_rows.append(sha(raw) + "  " + relative)
        stat_rows.append({"path": relative, "identity": list(before)})
    return (("\n".join(hash_rows) + "\n").encode("utf-8"),
            canonical(stat_rows) + b"\n")


def write(path: Path, raw: bytes) -> None:
    need(not path.exists() and not path.is_symlink(), "append-only output:" + path.name)
    path.write_bytes(raw)


def run_stage(output: Path, name: str, command: list[str], seed: int,
              cold: bool = False) -> dict[str, Any]:
    environment = {
        "PATH": "/usr/bin:/bin", "LANG": "C", "LC_ALL": "C",
        "PYTHONDONTWRITEBYTECODE": "1", "PYTHONHASHSEED": str(seed),
    }
    start = time.monotonic()
    if cold:
        with tempfile.TemporaryDirectory(prefix="cm2-c30q6-cold-") as directory:
            process = subprocess.run(command, stdin=subprocess.DEVNULL,
                                     stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                     cwd=directory, env=environment, timeout=180, check=False)
    else:
        process = subprocess.run(command, stdin=subprocess.DEVNULL,
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                 cwd=ROOT, env=environment, timeout=180, check=False)
    elapsed = time.monotonic() - start
    write(output / f"{name}_stdout.json", process.stdout)
    write(output / f"{name}_stderr.log", process.stderr)
    write(output / f"{name}_exit_code.txt", f"{process.returncode}\n".encode("ascii"))
    write(output / f"{name}_time.json", canonical({
        "elapsed_seconds": format(elapsed, ".6f"), "numeric_exit_code": process.returncode,
    }) + b"\n")
    return {"exit_code": process.returncode, "stdout": process.stdout,
            "stderr": process.stderr, "elapsed_seconds": format(elapsed, ".6f")}


def artifact_map(output: Path) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for path in sorted(output.iterdir()):
        if path.name in {"manifest.sha256", "receipt.json"}:
            continue
        safe_file(path)
        raw = path.read_bytes()
        result[path.name] = {"bytes": len(raw), "sha256": sha(raw)}
    return result


def main(argv: list[str]) -> int:
    output: Path | None = None
    try:
        need(len(argv) == 2, "usage: runner OUTPUT_DIR")
        output = Path(argv[1]).absolute()
        audit_root = (ROOT / ".cm2-runtime/audit").absolute()
        need(output.parent == audit_root and not output.exists() and not output.is_symlink(),
             "fresh direct audit child")
        output.mkdir(mode=0o700)
        for source, expected in SOURCE_PINS.items():
            need(sha(source.read_bytes()) == expected, "source pin:" + source.name)
        paths = tracked_inputs()
        pre_hash, pre_stat = snapshot(paths)
        write(output / "start_utc.txt",
              (datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ") + "\n").encode("ascii"))
        write(output / "pre.sha256", pre_hash)
        write(output / "pre.stat", pre_stat)
        provenance = {
            "schema": "cm2.round306c30q6.clean-room-audit-provenance.v1",
            "python": str(PYTHON), "python_sha256": sha(PYTHON.read_bytes()),
            "real_hash_seeds": list(SEEDS), "cold_hash_seed": COLD_SEED,
            "source_sha256": {str(path.relative_to(ROOT)): value
                              for path, value in SOURCE_PINS.items()},
            "runner_sha256": sha((HERE / Path(__file__).name).read_bytes()),
            "tracked_input_count": len(paths),
        }
        write(output / "provenance.json", canonical(provenance) + b"\n")

        producers = []
        for seed in SEEDS:
            producers.append(run_stage(
                output, f"producer_seed{seed}",
                [str(PYTHON), "-B", "-s", str(PRODUCER)], seed))
        need(all(stage["exit_code"] == 0 and stage["stderr"] == b"" for stage in producers),
             "producer execution")
        need(producers[0]["stdout"] == producers[1]["stdout"], "dual producer bytes")

        verifiers = []
        for seed in SEEDS:
            candidate = output / f"producer_seed{seed}_stdout.json"
            verifiers.append(run_stage(
                output, f"verifier_seed{seed}",
                [str(PYTHON), "-B", "-s", str(VERIFIER), str(candidate)], seed))
        need(all(stage["exit_code"] == 0 and stage["stderr"] == b"" for stage in verifiers),
             "verifier execution")
        need(verifiers[0]["stdout"] == verifiers[1]["stdout"], "dual verifier bytes")

        attack = run_stage(
            output, "attacks",
            [str(PYTHON), "-B", "-s", str(ATTACK),
             str(output / f"producer_seed{SEEDS[0]}_stdout.json")], SEEDS[0])
        need(attack["exit_code"] == 0 and attack["stderr"] == b"", "attacks execution")

        cold = run_stage(
            output, "cold_replay",
            [str(PYTHON), "-B", "-s", str(VERIFIER),
             str(output / f"producer_seed{SEEDS[1]}_stdout.json")], COLD_SEED, True)
        need(cold["exit_code"] == 0 and cold["stderr"] == b"", "cold replay execution")
        need(cold["stdout"] == verifiers[0]["stdout"], "cold replay bytes")

        post_hash, post_stat = snapshot(paths)
        write(output / "post.sha256", post_hash)
        write(output / "post.stat", post_stat)
        need(pre_hash == post_hash and pre_stat == post_stat, "pre/post input identity")
        write(output / "end_utc.txt",
              (datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ") + "\n").encode("ascii"))
        write(output / "PASS_ZERO_CREDIT.lock",
              b"PASS_C30Q6_RESEARCH_CLOSURE_FAIL_CLOSED_ZERO_CREDIT\n")

        candidate = json.loads(producers[0]["stdout"])
        verification = json.loads(verifiers[0]["stdout"])
        attacks = json.loads(attack["stdout"])
        write(output / "runner_status.json", canonical({
            "schema": "cm2.round306c30q6.clean-room-runner-status.v1",
            "status": "PASS_ALL_STAGES_ZERO_CREDIT",
            "numeric_exit_zero": True, "stderr_all_empty": True,
            "dual_seed_byte_identical": True, "cold_replay_byte_identical": True,
            "pre_post_sha_stat_identical": True,
        }) + b"\n")
        artifacts = artifact_map(output)
        receipt_payload = {
            "schema": "cm2.round306c30q6.compact-q-six-origin-clean-room-zero-credit-receipt.v1",
            "status": "PASS_C30Q6_CLEAN_ROOM_DUAL_SEED_COLD_REPLAY_AND_ATTACKS__FAIL_CLOSED_ZERO_CREDIT",
            "candidate_result_sha256": candidate["result_sha256"],
            "producer": {"dual_real_seed_stdout_identical": True,
                         "both_numeric_exit_zero": True, "both_stderr_empty": True,
                         "stdout_sha256": sha(producers[0]["stdout"])},
            "independent_verifier": {"dual_real_seed_stdout_identical": True,
                                     "both_numeric_exit_zero": True,
                                     "both_stderr_empty": True,
                                     "stdout_sha256": sha(verifiers[0]["stdout"]),
                                     "producer_imported_or_executed": False},
            "coherent_attacks": {"numeric_exit_zero": True, "stderr_empty": True,
                                 "total": attacks["attack_count"],
                                 "rejected": attacks["rejected"]},
            "cold_replay": {"isolated_working_directory": True,
                            "minimal_environment": True, "numeric_exit_zero": True,
                            "stderr_empty": True,
                            "byte_identical_to_dual_verifier": True},
            "input_stability": {"tracked_input_count": len(paths),
                                "pre_post_sha256_identical": True,
                                "pre_post_stat_identical": True,
                                "pre_sha256_file_sha256": sha(pre_hash),
                                "pre_stat_file_sha256": sha(pre_stat)},
            "authority_audit": {
                "six_research_origins_closed": True,
                "uniform_formal_predecessor_authority": False,
                "formal_54_to_48_authorized": False,
                "blocker_count": len(candidate["result"]["authority_fail_closed"]["blocking_reasons"]),
            },
            "strict_nonpromotion": candidate["result"]["strict_nonpromotion"],
            "source_sha256": provenance["source_sha256"],
            "runner_sha256": provenance["runner_sha256"],
            "artifacts": artifacts,
            "verification_status": verification["status"],
        }
        receipt = dict(receipt_payload)
        receipt["receipt_payload_sha256"] = sha(canonical(receipt_payload))
        write(output / "receipt.json", canonical(receipt) + b"\n")
        manifest_rows = []
        for path in sorted(output.iterdir()):
            if path.name == "manifest.sha256":
                continue
            safe_file(path)
            manifest_rows.append(sha(path.read_bytes()) + "  " + path.name)
        write(output / "manifest.sha256", ("\n".join(manifest_rows) + "\n").encode("ascii"))
        sys.stdout.buffer.write(canonical({
            "status": receipt["status"], "output": str(output),
            "receipt_sha256": sha((output / "receipt.json").read_bytes()),
            "manifest_sha256": sha((output / "manifest.sha256").read_bytes()),
            "formal_credit": 0, "source_W_formal_remaining": 80,
            "compact_q_formal_remaining": 54,
        }) + b"\n")
        return 0
    except (OSError, KeyError, TypeError, ValueError, Reject,
            subprocess.SubprocessError) as error:
        if output is not None and output.exists():
            failure = {"schema": "cm2.round306c30q6.clean-room-failure.v1",
                       "status": "FAILED_CLOSED", "reason": str(error),
                       "formal_credit": 0, "source_W_formal_remaining": 80,
                       "compact_q_formal_remaining": 54}
            if not (output / "failure.json").exists():
                (output / "failure.json").write_bytes(canonical(failure) + b"\n")
            if not (output / "FAILED.lock").exists():
                (output / "FAILED.lock").write_bytes(b"FAILED_CLOSED_C30Q6\n")
        sys.stderr.write("REJECT:" + str(error) + "\n")
        return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
