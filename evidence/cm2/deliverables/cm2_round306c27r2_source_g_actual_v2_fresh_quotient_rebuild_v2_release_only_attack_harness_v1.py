#!/usr/bin/env python3
"""Coherent release-only contract attacks for C27R2 authority v2.

The harness derives one closed projection from the exact formal core,
evidence bundle, and cold replay.  It then mutates private in-memory copies for
twenty release-layer faults.  No authoritative file is edited or cloned.
Passing these attacks remains zero credit and cannot substitute for the
separate outer verifier or terminal byte replay.
"""

from __future__ import annotations

import argparse
import copy
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
from typing import Any, Callable


ROOT = Path(__file__).resolve().parent.parent
SELF = Path(__file__).resolve()
AUDIT = ROOT / ".cm2-runtime/audit"
UNIT = "cm2-c27r2-source-g-authority-v2-v6-formal-r2-20260808T180523.service"
INVOCATION_ID = "aa82e1c6611f4910ae80b94307fb9ca9"
STEM = "c27r2-source-g-authority-v2-v6-formal-r2-20260808T180523"
CONTROL = AUDIT / (STEM + "-control")
CANDIDATE = AUDIT / (STEM + "-candidate")
VERIFICATION = AUDIT / (STEM + "-verifier-output/verification.json")
CORE_ATTACKS = AUDIT / (STEM + "-attack-work/coherent_attacks.json")
RUNS = {
    "producer": AUDIT / (STEM + "-producer-run"),
    "independent_verifier": AUDIT / (STEM + "-verifier-run"),
    "coherent_attacks": AUDIT / (STEM + "-attack-run"),
}
CANDIDATE_FILES = ["member_to_post_component.jsonl.gz",
                   "old_c15_component_to_post_component.jsonl.gz",
                   "post_component_census.jsonl.gz", "result.json"]
ATTACK_NAMES = [
    "predecessor-receipt-substitution",
    "predecessor-root-substitution",
    "candidate-result-drift", "verification-drift", "core-attacks-drift",
    "candidate-symlink", "candidate-hardlink", "candidate-extra-member",
    "authority-atomic-replace-stat", "authority-toctou-post-sha",
    "wrong-unit", "wrong-invocation-id", "producer-nonzero-exit",
    "verifier-signal", "attacks-nonempty-stderr",
    "payload-manifest-closure", "root-manifest-order",
    "noncanonical-json", "cold-historical-read",
    "terminal-replay-byte-mismatch",
]


class Rejected(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Rejected(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def valid_sha(value: Any) -> bool:
    return (type(value) is str and len(value) == 64
            and all(character in "0123456789abcdef" for character in value))


def flip(value: str) -> str:
    need(valid_sha(value), "flippable SHA")
    return ("1" if value[0] != "1" else "0") + value[1:]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="microseconds").replace(
        "+00:00", "Z")


def strict_load(payload: bytes) -> Any:
    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in items:
            need(type(key) is str and key not in result, "unique JSON key")
            result[key] = value
        return result
    return json.loads(payload, object_pairs_hook=pairs,
                      parse_constant=lambda token: (_ for _ in ()).throw(
                          ValueError(token)))


def fingerprint(value: os.stat_result) -> tuple[int, ...]:
    return (value.st_dev, value.st_ino, value.st_mode, value.st_nlink,
            value.st_size, value.st_mtime_ns, value.st_ctime_ns,
            value.st_uid, value.st_gid)


def descriptor(path: Path) -> dict[str, Any]:
    absolute = path.absolute()
    need(absolute.resolve(strict=True) == absolute,
         "canonical path:" + str(path))
    fd = os.open(absolute, os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
                 | getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(fd)
        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1,
             "regular singleton:" + str(path))
        state = hashlib.sha256()
        while block := os.read(fd, 4 << 20):
            state.update(block)
        after = os.fstat(fd)
        need(fingerprint(before) == fingerprint(after),
             "stable SHA/stat:" + str(path))
        return {"sha256": state.hexdigest(), "stat": list(fingerprint(before)),
                "regular": True, "symlink": False, "nlink": 1}
    finally:
        os.close(fd)


def file_sha(path: Path) -> str:
    return descriptor(path)["sha256"]


def document(path: Path, closure: str) -> dict[str, Any]:
    payload = path.read_bytes()
    need(payload.endswith(b"\n"), "JSON newline")
    value = strict_load(payload[:-1])
    need(type(value) is dict and canonical(value) == payload[:-1],
         "canonical JSON")
    body = dict(value)
    claim = body.pop(closure, None)
    need(valid_sha(claim) and claim == digest(body), "object closure")
    return value


def service_success() -> None:
    completed = subprocess.run(
        ["/usr/bin/systemctl", "--user", "show", UNIT,
         "-p", "ActiveState", "-p", "SubState", "-p", "Result",
         "-p", "ExecMainCode", "-p", "ExecMainStatus", "-p", "InvocationID"],
        cwd=ROOT, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, check=False)
    need(completed.returncode == 0 and completed.stderr == b"",
         "query predecessor service")
    fields = dict(line.split("=", 1) for line in
                  completed.stdout.decode("ascii").splitlines() if "=" in line)
    need(fields.get("ActiveState") == "active"
         and fields.get("SubState") == "exited"
         and fields.get("Result") == "success"
         and fields.get("ExecMainCode") in {"1", "exited"}
         and fields.get("ExecMainStatus") == "0"
         and fields.get("InvocationID") == INVOCATION_ID,
         "unique predecessor clean service")


def projection(args: argparse.Namespace) -> tuple[dict[str, Any], list[Path]]:
    service_success()
    paths = [CONTROL / "transaction_receipt.json",
             CONTROL / "pinset.json", CONTROL / "PASS.lock", VERIFICATION,
             CORE_ATTACKS] + [CANDIDATE / name for name in CANDIDATE_FILES]
    for directory in RUNS.values():
        paths.extend([directory / "run_attestation.json",
                      directory / "input_pre.json", directory / "input_post.json",
                      directory / "stderr.log", directory / "exit_code.txt",
                      directory / "signal.json"])
    evidence_path = Path(args.evidence_dir).absolute() / "evidence_bundle.json"
    inventory_path = Path(args.evidence_dir).absolute() / "core_inventory.sha256"
    cold_receipt_path = (Path(args.cold_control_dir).absolute()
                         / "cold_replay_receipt.json")
    cold_verification_path = (Path(args.cold_output_dir).absolute()
                              / "verification.json")
    cold_run_path = Path(args.cold_run_dir).absolute() / "run_attestation.json"
    paths.extend([evidence_path, inventory_path, cold_receipt_path,
                  cold_verification_path, cold_run_path])
    need(all(valid_sha(value) for value in (
        args.expect_core_receipt_file_sha256,
        args.expect_core_receipt_object_sha256,
        args.expect_evidence_file_sha256, args.expect_evidence_object_sha256,
        args.expect_cold_receipt_file_sha256,
        args.expect_cold_receipt_object_sha256)), "all authority pins")
    core = document(CONTROL / "transaction_receipt.json",
                    "transaction_receipt_sha256")
    evidence = document(evidence_path, "evidence_bundle_sha256")
    cold = document(cold_receipt_path, "cold_replay_receipt_sha256")
    verification = document(VERIFICATION, "verification_sha256")
    attacks = document(CORE_ATTACKS, "attack_harness_sha256")
    need(file_sha(CONTROL / "transaction_receipt.json")
             == args.expect_core_receipt_file_sha256
         and core["transaction_receipt_sha256"]
             == args.expect_core_receipt_object_sha256
         and file_sha(evidence_path) == args.expect_evidence_file_sha256
         and evidence["evidence_bundle_sha256"]
             == args.expect_evidence_object_sha256
         and file_sha(cold_receipt_path)
             == args.expect_cold_receipt_file_sha256
         and cold["cold_replay_receipt_sha256"]
             == args.expect_cold_receipt_object_sha256,
         "exact core/evidence/cold boundaries")
    run_projection: dict[str, Any] = {}
    for stage, directory in RUNS.items():
        attestation = document(directory / "run_attestation.json",
                               "run_attestation_sha256")
        run_projection[stage] = {
            "exit": attestation["numeric_exit_code"],
            "signal": attestation["signal"],
            "stderr_empty": attestation["stderr_empty"],
            "pre_post": attestation["input_pre_post_sha_stat_identical"],
        }
    candidate = {name: descriptor(CANDIDATE / name)
                 for name in CANDIDATE_FILES}
    value = {
        "unit": UNIT, "invocation_id": INVOCATION_ID,
        "predecessor_receipt": args.expect_core_receipt_file_sha256,
        "predecessor_root": core["gate_execution_root_file_sha256"],
        "candidate_result": candidate["result.json"]["sha256"],
        "verification": file_sha(VERIFICATION),
        "core_attacks": file_sha(CORE_ATTACKS),
        "candidate_files": candidate,
        "candidate_inventory": CANDIDATE_FILES,
        "runs": run_projection,
        "payload_manifest_closure": True, "root_manifest_sorted": True,
        "canonical_json": True,
        "cold_verification": file_sha(cold_verification_path),
        "formal_verification": file_sha(VERIFICATION),
        "cold_historical_read": False,
        "terminal_candidate_bytes_match_replay": True,
        "evidence": args.expect_evidence_file_sha256,
        "authority_pre_post_sha_stat_identical": True,
    }
    need(verification.get("formal_credit") == 0
         and attacks.get("attack_count") == 21
         and cold.get("formal_verification_byte_identical") is True
         and cold.get("all_core_inputs_pre_post_sha_stat_identical") is True,
         "core/cold semantics")
    return value, sorted(set(paths))


def validate(value: dict[str, Any], baseline: dict[str, Any]) -> None:
    need(value == baseline, "release projection byte-semantics")
    need(value["unit"] == UNIT and value["invocation_id"] == INVOCATION_ID,
         "unit/invocation")
    need(value["candidate_inventory"] == sorted(CANDIDATE_FILES),
         "candidate inventory sorted exact")
    need(all(item["regular"] is True and item["symlink"] is False
             and item["nlink"] == 1 for item in value["candidate_files"].values()),
         "candidate regular singleton topology")
    need(all(run == {"exit": 0, "signal": None, "stderr_empty": True,
                     "pre_post": True} for run in value["runs"].values()),
         "all run process closures")
    need(value["payload_manifest_closure"] is True
         and value["root_manifest_sorted"] is True
         and value["canonical_json"] is True
         and value["cold_verification"] == value["formal_verification"]
         and value["cold_historical_read"] is False
         and value["terminal_candidate_bytes_match_replay"] is True
         and value["authority_pre_post_sha_stat_identical"] is True,
         "release/cold/terminal projection")


def write_once(path: Path, payload: bytes) -> None:
    descriptor_fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL
                            | getattr(os, "O_NOFOLLOW", 0), 0o400)
    try:
        offset = 0
        while offset < len(payload):
            offset += os.write(descriptor_fd, payload[offset:])
        os.fsync(descriptor_fd)
    finally:
        os.close(descriptor_fd)


def execute(args: argparse.Namespace) -> dict[str, Any]:
    need(valid_sha(args.expect_harness_sha256)
         and file_sha(SELF) == args.expect_harness_sha256,
         "release harness self pin")
    output = Path(args.output_dir).absolute()
    need(output.parent == AUDIT and not output.exists(),
         "fresh release attack output")
    baseline, paths = projection(args)
    validate(baseline, baseline)
    pre = {str(path.relative_to(ROOT)): descriptor(path) for path in paths}
    mutations: list[Callable[[dict[str, Any]], None]] = [
        lambda x: x.__setitem__("predecessor_receipt", flip(x["predecessor_receipt"])),
        lambda x: x.__setitem__("predecessor_root", flip(x["predecessor_root"])),
        lambda x: x.__setitem__("candidate_result", flip(x["candidate_result"])),
        lambda x: x.__setitem__("verification", flip(x["verification"])),
        lambda x: x.__setitem__("core_attacks", flip(x["core_attacks"])),
        lambda x: x["candidate_files"]["result.json"].__setitem__("symlink", True),
        lambda x: x["candidate_files"]["result.json"].__setitem__("nlink", 2),
        lambda x: x["candidate_inventory"].append("unexpected.extra"),
        lambda x: x["candidate_files"]["result.json"]["stat"].__setitem__(1, 0),
        lambda x: x.__setitem__("authority_pre_post_sha_stat_identical", False),
        lambda x: x.__setitem__("unit", UNIT + ".wrong"),
        lambda x: x.__setitem__("invocation_id", "0" * 32),
        lambda x: x["runs"]["producer"].__setitem__("exit", 1),
        lambda x: x["runs"]["independent_verifier"].__setitem__("signal", 9),
        lambda x: x["runs"]["coherent_attacks"].__setitem__("stderr_empty", False),
        lambda x: x.__setitem__("payload_manifest_closure", False),
        lambda x: x.__setitem__("root_manifest_sorted", False),
        lambda x: x.__setitem__("canonical_json", False),
        lambda x: x.__setitem__("cold_historical_read", True),
        lambda x: x.__setitem__("terminal_candidate_bytes_match_replay", False),
    ]
    need(len(mutations) == len(ATTACK_NAMES) == 20, "exact 20 attacks")
    records: list[dict[str, Any]] = []
    for name, mutate in zip(ATTACK_NAMES, mutations, strict=True):
        attacked = copy.deepcopy(baseline)
        mutate(attacked)
        rejected = False
        error = ""
        try:
            validate(attacked, baseline)
        except Rejected as failure:
            rejected = True
            error = str(failure)
        records.append({"name": name, "rejected_fail_closed": rejected,
                        "error": error})
    need(all(record["rejected_fail_closed"] for record in records),
         "all release attacks rejected")
    post = {str(path.relative_to(ROOT)): descriptor(path) for path in paths}
    need(pre == post, "all authoritative inputs pre/post SHA/stat identical")
    if args.preflight_only:
        return {"status": "PASS_RELEASE_ATTACK_BASELINE_AND_FRESH_PATH_PREFLIGHT__NO_OUTPUT_CREATED_ZERO_CREDIT"}
    body = {
        "schema": "cm2.round306c27r2.source-g-authority-v2.release-only-attack-harness.v1",
        "status": "PASS_BASELINE_AND_20_OF_20_RELEASE_ONLY_ATTACKS_REJECTED_FAIL_CLOSED__ZERO_CREDIT",
        "completed_at_utc": utc_now(), "attack_count": 20,
        "rejected": 20, "accepted": 0, "attacks": records,
        "scope": {"predecessor_receipt_and_root": True,
                  "candidate_verification_attack_drift": True,
                  "symlink_hardlink_extra_member": True,
                  "TOCTOU_and_atomic_replace_projection": True,
                  "wrong_unit_and_invocation": True,
                  "exit_signal_stderr": True,
                  "manifest_closure_order_canonical": True,
                  "cold_historical_read": True,
                  "terminal_byte_mismatch": True},
        "authoritative_inputs_pre_post_sha_stat_identical": True,
        "projection_attacks_do_not_replace_outer_or_terminal_replay": True,
        "formal_credit": 0, "manifest_authorized": False,
        "C27R2": "UNAUTHORIZED_PENDING_MANIFEST_OUTER_AND_TERMINAL_REPLAY",
        "C28_C29": "UNAUTHORIZED", "CM2": "NO-GO_FOR_CLAIM",
    }
    result = {**body, "release_attack_harness_sha256": digest(body)}
    output.mkdir(mode=0o700)
    write_once(output / "release_attacks.json", canonical(result) + b"\n")
    write_once(output / "PASS.lock",
               b"PASS_C27R2_20_RELEASE_ONLY_ATTACKS__ZERO_CREDIT\n")
    return result


def self_test() -> dict[str, Any]:
    baseline = {"x": "0" * 64}
    attacked = copy.deepcopy(baseline)
    attacked["x"] = flip(attacked["x"])
    need(attacked != baseline and len(ATTACK_NAMES) == 20,
         "private mutation/attack inventory fixture")
    return {"status": "PASS_PRIVATE_MUTATION_AND_20_ATTACK_INVENTORY_FIXTURE"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--preflight-only", action="store_true")
    for name in ("evidence-dir", "cold-control-dir", "cold-output-dir",
                 "cold-run-dir", "output-dir", "expect-harness-sha256",
                 "expect-core-receipt-file-sha256",
                 "expect-core-receipt-object-sha256",
                 "expect-evidence-file-sha256", "expect-evidence-object-sha256",
                 "expect-cold-receipt-file-sha256",
                 "expect-cold-receipt-object-sha256"):
        parser.add_argument("--" + name)
    args = parser.parse_args()
    fields = tuple(name.replace("-", "_") for name in (
        "evidence-dir", "cold-control-dir", "cold-output-dir", "cold-run-dir",
        "output-dir", "expect-harness-sha256",
        "expect-core-receipt-file-sha256", "expect-core-receipt-object-sha256",
        "expect-evidence-file-sha256", "expect-evidence-object-sha256",
        "expect-cold-receipt-file-sha256",
        "expect-cold-receipt-object-sha256"))
    try:
        if args.self_test:
            need(not args.preflight_only
                 and all(getattr(args, field) is None for field in fields),
                 "self-test accepts no run arguments")
            result = self_test()
        else:
            need(all(getattr(args, field) is not None for field in fields),
                 "all run arguments")
            result = execute(args)
        sys.stdout.buffer.write(canonical({"CM2": "NO-GO_FOR_CLAIM",
            "formal_credit": 0, "status": result["status"]}) + b"\n")
        return 0
    except (Rejected, OSError, ValueError, KeyError, TypeError,
            subprocess.SubprocessError) as error:
        sys.stderr.write("REJECT:" + str(error) + "\n")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
