#!/usr/bin/env python3
"""Append-only dual-seed/cold-replay runner for the zero-credit Q7 theorem."""

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
PYTHON = (ROOT / ".cm2-runtime/python-flint-0.9.0/bin/python3").absolute()
PYTHON_RESOLVED = Path("/usr/bin/python3.12")
PRODUCER = (
    HERE
    / "cm2_round306c30q7_compact_q_11011101_two_witness_whole_pair_"
      "zero_credit_gate_v1.py"
)
VERIFIER = (
    HERE
    / "cm2_round306c30q7_compact_q_11011101_two_witness_whole_pair_"
      "zero_credit_independent_verifier_v1.py"
)
ATTACK = (
    HERE
    / "cm2_round306c30q7_compact_q_11011101_two_witness_whole_pair_"
      "zero_credit_coherent_attack_harness_v1.py"
)
SOURCE_PINS = {
    PRODUCER: "f1e7d8e983d6783f8acc5d72a4790c6aecae7726c7a20c8d959b638a5ef6d8d9",
    VERIFIER: "80b4ad775aa931451d4f7096d91ba84633c346193544fbc3acc95007407420a9",
    ATTACK: "d244978d2b7cc6b60e66ad782bfc58822440ebe3a4985240f06f7f0c276af3fd",
}
RUNTIME_PINS = {
    PYTHON_RESOLVED: "1643dacd9feaedc58f3cc581e4d22577dfe25c09b10282936186ccf0f2e61118",
    ROOT / ".cm2-runtime/python-flint-0.9.0/pyvenv.cfg":
        "7a941243ffcb93edeea4c49bc4543a1ff8150b3300f846cda2f13717b6469550",
    ROOT / ".cm2-runtime/python-flint-0.9.0/lib/python3.12/site-packages/flint/__init__.py":
        "2e5f8f1768d14eccd7961353c635195bd557f297edff8b8de09e2d211f03ec2d",
    ROOT / ".cm2-runtime/python-flint-0.9.0/lib/python3.12/site-packages/flint/pyflint.abi3.so":
        "1f7ef1f52024937f542772ff9190e2f74449228cd69a6746b6608fbbd449d138",
    ROOT / ".cm2-runtime/python-flint-0.9.0/lib/python3.12/site-packages/python_flint.libs/libflint-6839011d.so.24.0.0":
        "871a4132fd1e9f3638391b2208e07088f8e3e72a10e41d45f58b150a60c2a1a9",
    ROOT / ".cm2-runtime/python-flint-0.9.0/lib/python3.12/site-packages/python_flint.libs/libgmp-e0c82b6b.so.10.5.0":
        "33d24e675b10f8b1ab93a8ad3fa2ed5012e1b0d89dcdb97273877c6c6b9450d8",
    ROOT / ".cm2-runtime/python-flint-0.9.0/lib/python3.12/site-packages/python_flint.libs/libmpfr-be332c05.so.6.2.2":
        "c4dfcfc7c5c7ab71d427e15f2f9fae4ace88592a81d4596a918dcc02eadfc6e3",
}
SEEDS = (30770073, 30770931)
COLD_SEED = 30779997
MANIFESTS = {
    ROOT / "deliverables/cm2_round306c30b_source_w_outgoing_h_whole_origin_disposition_manifest.sha256":
        ROOT / "deliverables",
    ROOT / ".cm2-runtime/audit/c30q6-six-origin-clean-room-zero-credit-v1-20260808T085007Z/manifest.sha256":
        ROOT / ".cm2-runtime/audit/c30q6-six-origin-clean-room-zero-credit-v1-20260808T085007Z",
}
DIRECT_INPUTS = {
    ROOT / "deliverables/cm2_round306c30b_sealed/cm2_round306c30b_source_w_outgoing_h_whole_origin_disposition_result.json",
    ROOT / "deliverables/cm2_round306c30b_source_w_outgoing_h_whole_origin_disposition_verification.json",
    ROOT / ".cm2-runtime/audit/c30q1-cohort-counterexample-v3-20260807T1205/seed30630071_stdout.json",
    ROOT / ".cm2-runtime/audit/c30q1-cohort-counterexample-v3-20260807T1205/seed30630929_stdout.json",
    ROOT / ".cm2-runtime/audit/c30q2-seven-cohort-routing-v3-20260807T1325/seed30630071_stdout.json",
    ROOT / ".cm2-runtime/audit/c30q2-seven-cohort-routing-v3-20260807T1325/seed30630929_stdout.json",
    ROOT / ".cm2-runtime/audit/c30q6-six-origin-clean-room-zero-credit-v1-20260808T085007Z/receipt.json",
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


FIELDS = ("st_dev", "st_ino", "st_mode", "st_nlink", "st_size",
          "st_mtime_ns", "st_ctime_ns", "st_uid", "st_gid")


def identity(path: Path) -> tuple[int, ...]:
    info = os.lstat(path)
    return tuple(getattr(info, field) for field in FIELDS)


def safe_file(path: Path) -> None:
    absolute = path.absolute()
    need(absolute.resolve(strict=True) == absolute, "canonical file:" + str(path))
    info = os.lstat(absolute)
    need(stat.S_ISREG(info.st_mode) and info.st_nlink == 1,
         "regular single-link file:" + str(path))
    if absolute != PYTHON_RESOLVED:
        need(absolute.is_relative_to(ROOT), "workspace scope:" + str(path))


def manifest_members(manifest: Path, base: Path) -> set[Path]:
    safe_file(manifest)
    result = {manifest}
    seen: set[str] = set()
    for row in manifest.read_text("ascii").splitlines():
        need(len(row) >= 67 and row[64:66] == "  ", "manifest syntax")
        expected, relative = row[:64], row[66:]
        part = Path(relative)
        need(all(char in "0123456789abcdef" for char in expected)
             and not part.is_absolute() and ".." not in part.parts
             and relative not in seen, "manifest row")
        seen.add(relative)
        workspace = ROOT / part
        target = workspace if workspace.exists() else base / part
        safe_file(target)
        need(sha(target.read_bytes()) == expected, "manifest member:" + relative)
        result.add(target.absolute())
    need(len(result) > 1, "nonempty manifest")
    return result


def tracked_inputs() -> list[Path]:
    paths: set[Path] = {
        (HERE / Path(__file__).name).absolute(), PRODUCER, VERIFIER, ATTACK,
        *DIRECT_INPUTS, *RUNTIME_PINS,
    }
    for manifest, base in MANIFESTS.items():
        paths.update(manifest_members(manifest, base))
    flint_dir = (
        ROOT
        / ".cm2-runtime/python-flint-0.9.0/lib/python3.12/site-packages/flint"
    )
    paths.update(path.absolute() for path in flint_dir.iterdir() if path.is_file())
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
        relative = str(path) if path == PYTHON_RESOLVED else str(path.relative_to(ROOT))
        hash_rows.append(sha(raw) + "  " + relative)
        stat_rows.append({
            "path": relative,
            "fields": list(FIELDS),
            "identity": list(before),
        })
    return (("\n".join(hash_rows) + "\n").encode("utf-8"),
            canonical(stat_rows) + b"\n")


def write(path: Path, raw: bytes) -> None:
    need(not path.exists() and not path.is_symlink(), "append-only output:" + path.name)
    path.write_bytes(raw)


def strict_canonical_json(raw: bytes, label: str) -> dict[str, Any]:
    value = json.loads(raw.decode("utf-8", "strict"))
    need(type(value) is dict and raw == canonical(value) + b"\n",
         "canonical JSON stage:" + label)
    return value


def run_stage(output: Path, name: str, command: list[str], seed: int,
              cold: bool = False, timeout: int = 180) -> dict[str, Any]:
    environment = {
        "PATH": "/usr/bin:/bin", "LANG": "C", "LC_ALL": "C",
        "PYTHONDONTWRITEBYTECODE": "1", "PYTHONHASHSEED": str(seed),
    }
    start = time.monotonic()
    if cold:
        with tempfile.TemporaryDirectory(prefix="cm2-c30q7-cold-") as directory:
            process = subprocess.run(
                command, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                stderr=subprocess.PIPE, cwd=directory, env=environment,
                timeout=timeout, check=False,
            )
    else:
        process = subprocess.run(
            command, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, cwd=ROOT, env=environment,
            timeout=timeout, check=False,
        )
    elapsed = time.monotonic() - start
    signal = -process.returncode if process.returncode < 0 else None
    numeric_exit = process.returncode if process.returncode >= 0 else None
    write(output / f"{name}_stdout.json", process.stdout)
    write(output / f"{name}_stderr.log", process.stderr)
    write(output / f"{name}_process.json", canonical({
        "PYTHONHASHSEED": seed,
        "elapsed_seconds": format(elapsed, ".6f"),
        "numeric_exit_code": numeric_exit,
        "signal": signal,
        "stderr_bytes": len(process.stderr),
        "stdout_bytes": len(process.stdout),
    }) + b"\n")
    return {
        "returncode": process.returncode, "numeric_exit_code": numeric_exit,
        "signal": signal, "stdout": process.stdout, "stderr": process.stderr,
    }


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
        need(PYTHON.resolve(strict=True) == PYTHON_RESOLVED, "Python runtime resolution")
        for path, expected in {**SOURCE_PINS, **RUNTIME_PINS}.items():
            safe_file(path)
            need(sha(path.read_bytes()) == expected, "frozen pin:" + path.name)

        paths = tracked_inputs()
        pre_hash, pre_stat = snapshot(paths)
        write(output / "start_utc.txt",
              (datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ") + "\n").encode("ascii"))
        write(output / "pre.sha256", pre_hash)
        write(output / "pre.stat", pre_stat)
        runner = HERE / Path(__file__).name
        provenance = {
            "schema": "cm2.round306c30q7.two-witness-audit-provenance.v1",
            "python_invocation": str(PYTHON),
            "python_resolved": str(PYTHON_RESOLVED),
            "python_sha256": RUNTIME_PINS[PYTHON_RESOLVED],
            "python_flint_version": "0.9.0",
            "real_hash_seeds": list(SEEDS), "cold_hash_seed": COLD_SEED,
            "source_sha256": {str(path.relative_to(ROOT)): expected
                              for path, expected in SOURCE_PINS.items()},
            "runtime_sha256": {str(path): expected
                               for path, expected in RUNTIME_PINS.items()},
            "runner_sha256": sha(runner.read_bytes()),
            "tracked_input_count": len(paths),
            "stat_field_count": len(FIELDS),
            "stat_fields": list(FIELDS),
        }
        write(output / "provenance.json", canonical(provenance) + b"\n")

        producers = [
            run_stage(output, f"producer_seed{seed}",
                      [str(PYTHON), "-B", "-s", str(PRODUCER)], seed)
            for seed in SEEDS
        ]
        need(all(row["numeric_exit_code"] == 0 and row["signal"] is None
                 and row["stderr"] == b"" for row in producers),
             "dual producer process controls")
        need(producers[0]["stdout"] == producers[1]["stdout"],
             "dual producer byte identity")
        candidate = strict_canonical_json(producers[0]["stdout"], "producer")

        verifiers = [
            run_stage(
                output, f"verifier_seed{seed}",
                [str(PYTHON), "-B", "-s", str(VERIFIER),
                 str(output / f"producer_seed{seed}_stdout.json")], seed,
            ) for seed in SEEDS
        ]
        need(all(row["numeric_exit_code"] == 0 and row["signal"] is None
                 and row["stderr"] == b"" for row in verifiers),
             "dual verifier process controls")
        need(verifiers[0]["stdout"] == verifiers[1]["stdout"],
             "dual verifier byte identity")
        verification = strict_canonical_json(verifiers[0]["stdout"], "verifier")

        attacks = run_stage(
            output, "coherent_attacks",
            [str(PYTHON), "-B", "-s", str(ATTACK),
             str(output / f"producer_seed{SEEDS[0]}_stdout.json")], SEEDS[0],
        )
        need(attacks["numeric_exit_code"] == 0 and attacks["signal"] is None
             and attacks["stderr"] == b"", "attack process controls")
        attack_result = strict_canonical_json(attacks["stdout"], "attacks")

        cold = run_stage(
            output, "cold_replay",
            [str(PYTHON), "-B", "-s", str(VERIFIER),
             str(output / f"producer_seed{SEEDS[1]}_stdout.json")],
            COLD_SEED, cold=True,
        )
        need(cold["numeric_exit_code"] == 0 and cold["signal"] is None
             and cold["stderr"] == b"", "cold process controls")
        need(cold["stdout"] == verifiers[0]["stdout"], "cold verifier byte identity")
        strict_canonical_json(cold["stdout"], "cold verifier")

        post_hash, post_stat = snapshot(paths)
        write(output / "post.sha256", post_hash)
        write(output / "post.stat", post_stat)
        need(pre_hash == post_hash and pre_stat == post_stat,
             "input pre/post SHA and nine-field stat")
        write(output / "end_utc.txt",
              (datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ") + "\n").encode("ascii"))
        write(output / "PASS_ZERO_CREDIT.lock",
              b"PASS_C30Q7_TWO_WITNESS_WHOLE_PAIR_RESEARCH_ZERO_CREDIT\n")
        write(output / "runner_status.json", canonical({
            "schema": "cm2.round306c30q7.two-witness-runner-status.v1",
            "status": "PASS_ALL_STAGES_ZERO_CREDIT",
            "dual_real_seed_producer_byte_identical": True,
            "dual_real_seed_verifier_byte_identical": True,
            "all_numeric_exit_zero": True, "all_signals_null": True,
            "all_stderr_empty": True, "cold_replay_byte_identical": True,
            "input_pre_post_sha_identical": True,
            "input_pre_post_nine_field_stat_identical": True,
            "formal_credit": 0,
            "compact_q_formal_remaining": 54,
        }) + b"\n")

        artifacts = artifact_map(output)
        payload = {
            "schema": "cm2.round306c30q7.two-witness-whole-pair-zero-credit-receipt.v1",
            "status": "PASS_C30Q7_DUAL_SEED_GLOBAL_TWO_WITNESS_ATTACKS_AND_COLD_REPLAY__ZERO_FORMAL_CREDIT",
            "candidate_result_sha256": candidate["result_sha256"],
            "producer": {
                "real_hash_seeds": list(SEEDS),
                "dual_seed_stdout_byte_identical": True,
                "both_numeric_exit_zero": True, "both_signals_null": True,
                "both_stderr_empty": True,
                "stdout_sha256": sha(producers[0]["stdout"]),
            },
            "independent_verifier": {
                "real_hash_seeds": list(SEEDS),
                "dual_seed_stdout_byte_identical": True,
                "both_numeric_exit_zero": True, "both_signals_null": True,
                "both_stderr_empty": True,
                "stdout_sha256": sha(verifiers[0]["stdout"]),
                "producer_imported_or_executed": False,
                "status": verification["status"],
            },
            "coherent_attacks": {
                "numeric_exit_zero": True, "signal_null": True,
                "stderr_empty": True, "total": attack_result["attack_count"],
                "rejected": attack_result["rejected"],
                "mandatory_coverage": attack_result["mandatory_coverage"],
            },
            "cold_replay": {
                "isolated_working_directory": True,
                "minimal_environment": True, "hash_seed": COLD_SEED,
                "numeric_exit_zero": True, "signal_null": True,
                "stderr_empty": True,
                "byte_identical_to_dual_verifier": True,
            },
            "input_stability": {
                "tracked_input_count": len(paths),
                "stat_field_count": 9, "stat_fields": list(FIELDS),
                "pre_post_sha256_identical": True,
                "pre_post_stat_identical": True,
                "pre_sha256_file_sha256": sha(pre_hash),
                "pre_stat_file_sha256": sha(pre_stat),
            },
            "theorem": {
                "origin_keys": candidate["result"]["whole_pair_research_conclusion"]["origin_keys"],
                "roots_per_origin": 16, "old_gap_roots_per_origin": 12,
                "global_interval_box_count": 2, "switch": "13/16",
                "right_witness_is_two_crossing_chord_with_f_at_1_positive": True,
                "finite_old_gap_root_subdivision_count": 0,
            },
            "formal_boundary": candidate["result"]["formal_boundary"],
            "can_serve_as_compact_q_cohort_formal_predecessor": False,
            "formal_54_to_52_authorized": False,
            "source_sha256": provenance["source_sha256"],
            "runtime_sha256": provenance["runtime_sha256"],
            "runner_sha256": provenance["runner_sha256"],
            "artifacts": artifacts,
        }
        receipt = dict(payload)
        receipt["receipt_payload_sha256"] = sha(canonical(payload))
        write(output / "receipt.json", canonical(receipt) + b"\n")
        manifest_rows: list[str] = []
        for path in sorted(output.iterdir()):
            if path.name == "manifest.sha256":
                continue
            safe_file(path)
            manifest_rows.append(sha(path.read_bytes()) + "  " + path.name)
        write(output / "manifest.sha256", ("\n".join(manifest_rows) + "\n").encode("ascii"))
        summary = {
            "status": receipt["status"], "output": str(output),
            "receipt_sha256": sha((output / "receipt.json").read_bytes()),
            "manifest_sha256": sha((output / "manifest.sha256").read_bytes()),
            "formal_credit": 0, "source_W_formal_remaining": 80,
            "compact_q_formal_remaining": 54,
            "can_serve_as_formal_predecessor": False,
        }
        sys.stdout.buffer.write(canonical(summary) + b"\n")
        return 0
    except (OSError, KeyError, TypeError, ValueError, Reject,
            subprocess.SubprocessError, subprocess.TimeoutExpired) as error:
        if output is not None and output.exists():
            failure = {
                "schema": "cm2.round306c30q7.two-witness-failure.v1",
                "status": "FAILED_CLOSED", "reason": str(error),
                "formal_credit": 0, "source_W_formal_remaining": 80,
                "compact_q_formal_remaining": 54,
                "formal_54_to_52_authorized": False,
            }
            if not (output / "failure.json").exists():
                (output / "failure.json").write_bytes(canonical(failure) + b"\n")
            if not (output / "FAILED.lock").exists():
                (output / "FAILED.lock").write_bytes(b"FAILED_CLOSED_C30Q7\n")
        sys.stderr.write("REJECT_C30Q7_RUNNER:" + str(error) + "\n")
        return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
