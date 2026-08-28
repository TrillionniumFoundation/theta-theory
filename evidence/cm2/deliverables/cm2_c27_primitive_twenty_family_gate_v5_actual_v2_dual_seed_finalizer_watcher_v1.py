#!/usr/bin/env python3
"""Persistent fail-closed finalizer for the two real actual-v2 seed runs."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import signal
import stat
import subprocess
import sys
import time
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
SELF = Path(__file__).resolve()
PYTHON = Path("/usr/bin/python3.12")
RUNNER = ROOT / "deliverables/cm2_c27_primitive_twenty_family_gate_v5_actual_v2_runner.py"
ASSEMBLER = ROOT / "deliverables/cm2_c27_primitive_twenty_family_gate_v5_actual_v2.py"
SEED2_WATCHER = ROOT / "deliverables/cm2_c27_primitive_twenty_family_gate_v5_actual_v2_seed2_gated_handoff.py"
VERIFIER = ROOT / "deliverables/cm2_c27_primitive_twenty_family_gate_v5_actual_v2_dual_seed_independent_verifier_v1.py"
ATTACKS = ROOT / "deliverables/cm2_c27_primitive_twenty_family_gate_v5_actual_v2_dual_seed_coherent_attack_harness_v1.py"
REPLAY = ROOT / "deliverables/cm2_c27_primitive_twenty_family_gate_v5_actual_v2_dual_seed_terminal_replay_v1.py"
C15 = ROOT / "deliverables/cm2_round306c15_source_g_502204_member_fresh_dsu_freeze_member_component_ledger.jsonl.gz"
RUNNER_SHA256 = "c0f2c29d03aad122762ba0b3dad5885418c17872dab3da665eb764dad9cab245"
ASSEMBLER_SHA256 = "038c6a661438f9253fb00a29b9f41941bea33a3a8769a258d8dfa5763880b561"
SEED2_WATCHER_SHA256 = "3e5f874230c9faf809975808a2bd7284acf32c6e2b771e36a86d532a1a22c386"
C15_SHA256 = "e70c667fd8f14cb3c3d6444bb752dfc86244e61be292a9f884889d53951ff25a"
LEDGERS = (
    "candidate_ownership", "materialized_physical_proof_join",
    "atom_pair_incidence", "atom_incidence_disposition",
    "full_component_edge_union",
)


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


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="microseconds").replace(
        "+00:00", "Z")


def fingerprint(info: os.stat_result) -> tuple[int, ...]:
    return (info.st_dev, info.st_ino, info.st_size, info.st_mtime_ns,
            info.st_ctime_ns, info.st_mode, info.st_uid, info.st_gid)


def fsha(path: Path) -> str:
    descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
                         | getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(descriptor)
        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1,
             "regular single-link file:" + str(path))
        state = hashlib.sha256()
        while block := os.read(descriptor, 4 << 20):
            state.update(block)
        need(fingerprint(os.fstat(descriptor)) == fingerprint(before),
             "stable fstat:" + str(path))
        return state.hexdigest()
    finally:
        os.close(descriptor)


def inside(path: Path) -> Path:
    resolved = path.resolve()
    need(resolved == ROOT or ROOT in resolved.parents,
         "path inside workspace:" + str(path))
    need(not path.is_symlink(), "no symlink path:" + str(path))
    return resolved


def exclusive(path: Path, payload: bytes) -> None:
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL
                         | getattr(os, "O_NOFOLLOW", 0), 0o600)
    try:
        os.write(descriptor, payload)
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def write_json(path: Path, value: Any) -> None:
    exclusive(path, canonical(value) + b"\n")


def strict_json(path: Path, closure: str | None = None) -> Any:
    raw = path.read_bytes()
    value = json.loads(raw)
    need(raw == canonical(value) + b"\n", "canonical JSON:" + str(path))
    if closure is not None:
        need(type(value) is dict, "closed object:" + str(path))
        body = dict(value)
        claim = body.pop(closure, None)
        need(type(claim) is str and claim == digest(body),
             "object closure:" + str(path))
    return value


def source_pins(args: argparse.Namespace) -> dict[str, str]:
    observed = {
        "runner": fsha(RUNNER), "assembler": fsha(ASSEMBLER),
        "seed2_handoff_watcher": fsha(SEED2_WATCHER),
        "independent_verifier": fsha(VERIFIER),
        "coherent_attack_harness": fsha(ATTACKS),
        "terminal_replay": fsha(REPLAY),
        "finalizer_watcher": fsha(SELF), "frozen_C15": fsha(C15),
        "python": fsha(PYTHON),
    }
    expected = {
        "runner": RUNNER_SHA256, "assembler": ASSEMBLER_SHA256,
        "seed2_handoff_watcher": SEED2_WATCHER_SHA256,
        "independent_verifier": args.expect_verifier_sha256,
        "coherent_attack_harness": args.expect_attack_sha256,
        "terminal_replay": args.expect_replay_sha256,
        "finalizer_watcher": args.expect_finalizer_sha256,
        "frozen_C15": C15_SHA256, "python": args.expect_python_sha256,
    }
    need(observed == expected, "all source/executable SHA256 pins")
    return observed


def service_state(unit: str) -> tuple[str, str]:
    completed = subprocess.run(
        ["/usr/bin/systemctl", "--user", "show", unit,
         "--property=ActiveState", "--property=SubState"],
        cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
        check=False)
    values: dict[str, str] = {}
    for line in completed.stdout.decode("ascii", "strict").splitlines():
        if "=" in line:
            key, value = line.split("=", 1)
            values[key] = value
    return (values.get("ActiveState", "not-found"),
            values.get("SubState", "not-found"))


def wait_terminal(unit: str, run_dir: Path, timeout: int) -> tuple[str, str]:
    deadline = time.monotonic() + timeout
    while True:
        state = service_state(unit)
        if (run_dir / "FAILED.lock").exists():
            raise Failure("seed2 native FAILED.lock")
        active = state[0] in {"active", "activating", "deactivating"}
        if (run_dir / "PASS.lock").is_file() and not active:
            return state
        if not active and not (run_dir / "PASS.lock").is_file():
            raise Failure("seed2 service stopped without PASS:" + repr(state))
        if time.monotonic() >= deadline:
            raise Failure("seed2 finalizer wait timeout")
        time.sleep(20)


def quick_native(seed: int, out_dir: Path, run_dir: Path) -> dict[str, Any]:
    need((run_dir / "PASS.lock").read_bytes()
         == b"PASS_TRANSACTION_COMPLETE__ZERO_CREDIT\n"
         and not (run_dir / "FAILED.lock").exists(),
         "native PASS-only state")
    need((run_dir / "exit_code.txt").read_bytes() == b"0\n"
         and strict_json(run_dir / "signal.json") is None
         and (run_dir / "stderr.log").read_bytes() == b"",
         "native exit0/no-signal/empty-stderr")
    attestation = strict_json(run_dir / "run_attestation.json",
                              "run_attestation_sha256")
    validation = strict_json(run_dir / "output_validation.json")
    pre = strict_json(run_dir / "input_pre.json")
    post = strict_json(run_dir / "input_post.json")
    need(attestation["execution_seed"] == seed
         and attestation["numeric_exit_code"] == 0
         and attestation["signal"] is None
         and attestation["stderr_empty"] is True
         and attestation["pre_post_sha256_identical"] is True
         and attestation["pre_post_stat_identical"] is True
         and attestation["input_pre"] == pre == post
         and attestation["input_post"] == post
         and attestation["runner_source_sha256"] == RUNNER_SHA256
         and attestation["formal_credit"] == 0
         and attestation["manifest_authorized"] is False
         and attestation["CM2"] == "NO-GO_FOR_CLAIM"
         and digest(validation) == attestation["output_validation_sha256"]
         and validation["status"]
             == "PASS_7_OF_7_GZIP_CANONICAL_COUNT_CLOSURE"
         and validation["output_file_count"] == 7,
         "native attestation/validation")
    names = {item.name for item in out_dir.iterdir()}
    need(names == {*(name + ".jsonl.gz" for name in LEDGERS),
                   "assembler_receipt.json", "manifest.sha256"},
         "native current exact 7/7")
    return {
        "run_attestation_file_sha256": fsha(run_dir / "run_attestation.json"),
        "run_attestation_object_sha256": attestation["run_attestation_sha256"],
        "output_validation_file_sha256": fsha(run_dir / "output_validation.json"),
        "output_validation_object_sha256": digest(validation),
        "input_snapshot_sha256": digest(pre),
    }


def run_tool(label: str, command: list[str], run_dir: Path,
             pins_before: dict[str, str], args: argparse.Namespace) -> None:
    stdout = run_dir / (label + ".stdout.json")
    stderr = run_dir / (label + ".stderr.log")
    exit_path = run_dir / (label + ".exit_code.txt")
    start = time.monotonic_ns()
    with stdout.open("xb") as out, stderr.open("xb") as err:
        completed = subprocess.run(
            command, cwd=ROOT,
            env={"HOME": "/nonexistent", "LC_ALL": "C.UTF-8",
                 "TZ": "UTC", "PYTHONDONTWRITEBYTECODE": "1"},
            stdout=out, stderr=err, check=False)
        out.flush()
        err.flush()
        os.fsync(out.fileno())
        os.fsync(err.fileno())
    exclusive(exit_path, (str(completed.returncode) + "\n").encode("ascii"))
    write_json(run_dir / (label + ".time.json"), {
        "duration_ns": time.monotonic_ns() - start,
        "numeric_exit_code": completed.returncode
            if completed.returncode >= 0 else None,
        "signal": -completed.returncode if completed.returncode < 0 else None,
    })
    need(completed.returncode == 0
         and stderr.read_bytes() == b""
         and len(stdout.read_bytes().splitlines()) == 1,
         label + ":exit0/no-signal/empty-stderr/single-stdout")
    need(source_pins(args) == pins_before, label + ":source pins unchanged")


@dataclass
class Capture:
    label: str
    path: Path
    fd: int
    initial: tuple[int, ...]
    sha256: str

    @classmethod
    def open(cls, label: str, path: Path) -> "Capture":
        resolved = inside(path)
        descriptor = os.open(resolved, os.O_RDONLY
                             | getattr(os, "O_CLOEXEC", 0)
                             | getattr(os, "O_NOFOLLOW", 0))
        try:
            before = os.fstat(descriptor)
            need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1,
                 label + ":regular single-link")
            state = hashlib.sha256()
            while block := os.read(descriptor, 4 << 20):
                state.update(block)
            need(fingerprint(os.fstat(descriptor)) == fingerprint(before),
                 label + ":stable hash fstat")
            return cls(label, resolved, descriptor, fingerprint(before),
                       state.hexdigest())
        except BaseException:
            os.close(descriptor)
            raise

    def attestation(self) -> dict[str, Any]:
        need(fingerprint(os.fstat(self.fd)) == self.initial,
             self.label + ":terminal fstat")
        return {"path": str(self.path.relative_to(ROOT)),
                "sha256": self.sha256, "size": self.initial[2],
                "stat_fingerprint": list(self.initial),
                "O_NOFOLLOW": True,
                "single_open_file_description_hash_parse_fstat": True}

    def close(self) -> None:
        os.close(self.fd)


def add_seed_inputs(result: dict[str, Path], label: str,
                    out_dir: Path, run_dir: Path) -> None:
    for name in ("run_attestation", "output_validation", "input_pre",
                 "input_post", "pins", "transaction", "signal"):
        result[label + "_" + name] = run_dir / (name + ".json")
    result[label + "_exit"] = run_dir / "exit_code.txt"
    result[label + "_stderr"] = run_dir / "stderr.log"
    result[label + "_pass_lock"] = run_dir / "PASS.lock"
    result[label + "_assembler_receipt"] = out_dir / "assembler_receipt.json"
    result[label + "_manifest"] = out_dir / "manifest.sha256"
    for name in LEDGERS:
        result[label + "_" + name] = out_dir / (name + ".jsonl.gz")


def manifest_line(capture: Capture) -> str:
    return f"{capture.sha256}  {capture.path.relative_to(ROOT)}\n"


def build_base_seal(args: argparse.Namespace, pins: dict[str, str],
                    run_dir: Path, seal_dir: Path, seed1_out: Path,
                    seed1_run: Path, seed2_out: Path, seed2_run: Path,
                    handoff_dir: Path) -> tuple[dict[str, Any], str, str, str]:
    payload_dir = seal_dir / "payload"
    payload_dir.mkdir(parents=True, exist_ok=False)
    verification_path = payload_dir / "independent_verification.json"
    verifier_command = [
        str(PYTHON), "-I", "-B", str(VERIFIER),
        "--seed1", str(args.seed1), "--seed1-out", str(seed1_out),
        "--seed1-run", str(seed1_run), "--seed2", str(args.seed2),
        "--seed2-out", str(seed2_out), "--seed2-run", str(seed2_run),
        "--verification-seed", str(args.verification_seed),
        "--expect-verifier-sha256", args.expect_verifier_sha256,
        "--out-file", str(verification_path),
    ]
    run_tool("independent_verifier", verifier_command, run_dir, pins, args)
    verification = strict_json(verification_path, "verification_sha256")
    need(verification["status"]
         == "PASS_TWO_REAL_SEEDS_NATIVE_FULL_PASS_INDEPENDENT_GLOBAL_REPLAY_AND_EXACT_SEED_INVARIANCE__ZERO_CREDIT",
         "independent verifier terminal PASS")

    attacks_path = payload_dir / "coherent_attacks.json"
    attack_command = [
        str(PYTHON), "-I", "-B", str(ATTACKS),
        "--verification", str(verification_path.relative_to(ROOT)),
        "--verifier-source", str(VERIFIER.relative_to(ROOT)),
        "--expect-verifier-sha256", args.expect_verifier_sha256,
        "--expect-attack-harness-sha256", args.expect_attack_sha256,
        "--out-file", str(attacks_path.relative_to(ROOT)),
    ]
    run_tool("coherent_attacks", attack_command, run_dir, pins, args)
    attacks = strict_json(attacks_path, "attack_result_sha256")
    need(attacks["status"]
         == "PASS_CONTROL_AND_24_OF_24_COHERENT_RESIGNED_ATTACKS_REJECTED__ZERO_CREDIT"
         and attacks["attack_count"] == 24
         and attacks["rejected_attack_count"] == 24
         and attacks["accepted_attack_count"] == 0,
         "24/24 coherent attacks")

    inventory = {
        "schema": "cm2.c27-actual-v2-dual-seed-finalizer-input-inventory.v1",
        "status": "PASS_IMMUTABLE_INPUT_INVENTORY__ZERO_CREDIT",
        "execution_seeds": [args.seed1, args.seed2],
        "source_pins": pins,
        "seed1_out_dir": str(seed1_out.relative_to(ROOT)),
        "seed1_run_dir": str(seed1_run.relative_to(ROOT)),
        "seed2_out_dir": str(seed2_out.relative_to(ROOT)),
        "seed2_run_dir": str(seed2_run.relative_to(ROOT)),
        "seed2_handoff_dir": str(handoff_dir.relative_to(ROOT)),
        "authority_inventory": {
            "source_of_truth": str(ASSEMBLER.relative_to(ROOT)),
            "terminal_seal_groups": ["T00", "legacy", "T04", "T07_T09", "T11_T19"],
            "source_documents": ["legacy", "T04", "T11_T19"],
            "terminal_candidate_and_proof_ledger_slots": 20,
            "atom_ledgers": ["atom_pair_incidence", "atom_incidence_disposition"],
            "frozen_C15_sha256": C15_SHA256,
            "interface_v2_file_sha256": "6873b33d7b131a4bde0c4dbcf99873e6826cf2190fde6dfdf6640ee47d53c9d6",
            "interface_v2_object_sha256": "3ece982b83b968e7cc23c4d43f2602fb5f8490484af5ed2f214515be4f0eb37e",
        },
        "formal_credit": 0, "manifest_authorized": False,
        "C27R2_C28_C29": "UNAUTHORIZED_PENDING_ACTUAL_V2_TERMINAL_SEAL",
        "CM2": "NO-GO_FOR_CLAIM",
    }
    inventory["inventory_sha256"] = digest(inventory)
    inventory_path = payload_dir / "inventory.json"
    write_json(inventory_path, inventory)

    paths: dict[str, Path] = {
        "runner_source": RUNNER, "assembler_source": ASSEMBLER,
        "seed2_watcher_source": SEED2_WATCHER,
        "independent_verifier_source": VERIFIER,
        "attack_harness_source": ATTACKS,
        "terminal_replay_source": REPLAY, "finalizer_source": SELF,
        "frozen_C15": C15,
        "seed2_handoff_receipt": handoff_dir / "handoff_receipt.json",
        "seed2_handoff_gate_lock": handoff_dir / "HANDOFF_GATE_PASS.lock",
        "independent_verification": verification_path,
        "coherent_attacks": attacks_path, "inventory": inventory_path,
        "finalizer_watcher_start": run_dir / "watcher_start.json",
    }
    add_seed_inputs(paths, "seed1", seed1_out, seed1_run)
    add_seed_inputs(paths, "seed2", seed2_out, seed2_run)
    for label in ("independent_verifier", "coherent_attacks"):
        paths[label + "_stdout"] = run_dir / (label + ".stdout.json")
        paths[label + "_stderr"] = run_dir / (label + ".stderr.log")
        paths[label + "_exit"] = run_dir / (label + ".exit_code.txt")
        paths[label + "_time"] = run_dir / (label + ".time.json")
    need(len(paths) == len(set(paths))
         and len({path.resolve() for path in paths.values()}) == len(paths),
         "unique payload labels/paths")
    captures: dict[str, Capture] = {}
    try:
        for label, path in sorted(paths.items()):
            captures[label] = Capture.open(label, path)
        manifest_rows = "".join(sorted(manifest_line(item)
                                       for item in captures.values()))
        payload_manifest = seal_dir / "payload_manifest.sha256"
        exclusive(payload_manifest, manifest_rows.encode("ascii"))
        payload_manifest_sha = fsha(payload_manifest)
        handoff = strict_json(handoff_dir / "handoff_receipt.json",
                              "handoff_receipt_sha256")
        need(handoff["seed1"] == args.seed1 and handoff["seed2"] == args.seed2
             and handoff["runner_source_sha256"] == RUNNER_SHA256
             and handoff["watcher_source_sha256"] == SEED2_WATCHER_SHA256
             and handoff["formal_credit"] == 0
             and handoff["manifest_authorized"] is False,
             "seed2 handoff receipt")
        body = {
            "schema": "cm2.c27-independent.primitive-twenty-family-gate-v5-actual-v2-dual-seed-zero-credit-seal.v1",
            "status": "PASS_SEALED_TWO_REAL_SEEDS_NATIVE_AND_INDEPENDENT_REPLAY_PLUS_24_ATTACKS__PENDING_COLD_REPLAY__ZERO_CREDIT",
            "sealed_at_utc": utc_now(),
            "execution_seeds": [args.seed1, args.seed2],
            "source_pins": pins,
            "seed2_handoff": {
                "file_sha256": captures["seed2_handoff_receipt"].sha256,
                "object_sha256": handoff["handoff_receipt_sha256"],
            },
            "independent_verification": {
                "file_sha256": captures["independent_verification"].sha256,
                "object_sha256": verification["verification_sha256"],
                "semantic_projection_sha256":
                    verification["semantic_projection_sha256"],
            },
            "coherent_attacks": {
                "file_sha256": captures["coherent_attacks"].sha256,
                "object_sha256": attacks["attack_result_sha256"],
                "attack_count": 24, "rejected": 24, "accepted": 0,
            },
            "exact_census": verification["exact_census"],
            "seed_invariant_mathematical_projection_sha256":
                verification["seed_invariant_mathematical_projection_sha256"],
            "payload_manifest": {
                "filename": "payload_manifest.sha256",
                "entry_count": len(captures),
                "file_sha256": payload_manifest_sha,
            },
            "actual_v2_terminal_gate": "PENDING_COLD_REPLAY",
            "formal_credit": 0, "manifest_authorized": False,
            "C27R2_C28_C29": "UNAUTHORIZED_PENDING_ACTUAL_V2_COLD_REPLAY",
            "CM2": "NO-GO_FOR_CLAIM",
            "root_input_capture": {
                "all_inputs_single_stable_O_NOFOLLOW_FD_hash_parse_fstat": True,
                "attestations": {label: item.attestation()
                                 for label, item in sorted(captures.items())},
            },
        }
        receipt = dict(body)
        receipt["receipt_sha256"] = digest(receipt)
        receipt_path = seal_dir / "receipt.json"
        write_json(receipt_path, receipt)
        root_manifest = seal_dir / "root_manifest.sha256"
        exclusive(root_manifest, (
            f"{payload_manifest_sha}  payload_manifest.sha256\n"
            f"{fsha(receipt_path)}  receipt.json\n").encode("ascii"))
        for capture in captures.values():
            capture.attestation()
        return (receipt, fsha(receipt_path), payload_manifest_sha,
                fsha(root_manifest))
    finally:
        for capture in captures.values():
            capture.close()


def build_terminal(args: argparse.Namespace, pins: dict[str, str],
                   run_dir: Path, seal_dir: Path, terminal_dir: Path,
                   receipt: dict[str, Any], receipt_file_sha: str,
                   payload_sha: str, root_sha: str) -> dict[str, Any]:
    terminal_dir.mkdir(parents=True, exist_ok=False)
    replay_path = terminal_dir / "terminal_replay.json"
    command = [
        str(PYTHON), "-I", "-B", str(REPLAY),
        "--receipt", str(seal_dir / "receipt.json"),
        "--receipt-sha256", receipt_file_sha,
        "--payload-manifest", str(seal_dir / "payload_manifest.sha256"),
        "--payload-manifest-sha256", payload_sha,
        "--root-manifest", str(seal_dir / "root_manifest.sha256"),
        "--root-manifest-sha256", root_sha,
        "--expect-replay-sha256", args.expect_replay_sha256,
        "--replay-seed", str(args.replay_seed),
        "--out-file", str(replay_path),
    ]
    run_tool("terminal_replay", command, run_dir, pins, args)
    replay = strict_json(replay_path, "result_sha256")
    need(replay["status"]
         == "PASS_COLD_ROOT_PAYLOAD_CURRENT_SHA_STAT_NATIVE_DUAL_SEED_INDEPENDENT_REPLAY_AND_24_ATTACKS__ZERO_CREDIT"
         and replay["actual_v2_terminal_gate"]
             == "PASS_COLD_REPLAY_READY_FOR_TERMINAL_RECEIPT",
         "cold terminal replay PASS")
    terminal_payloads = [
        seal_dir / "receipt.json", seal_dir / "payload_manifest.sha256",
        seal_dir / "root_manifest.sha256", replay_path, REPLAY, SELF,
        seal_dir / "payload/independent_verification.json",
        seal_dir / "payload/coherent_attacks.json",
        run_dir / "terminal_replay.stdout.json",
        run_dir / "terminal_replay.stderr.log",
        run_dir / "terminal_replay.exit_code.txt",
        run_dir / "terminal_replay.time.json",
    ]
    rows = "".join(sorted(
        f"{fsha(path)}  {path.relative_to(ROOT)}\n"
        for path in terminal_payloads))
    terminal_payload_manifest = terminal_dir / "payload_manifest.sha256"
    exclusive(terminal_payload_manifest, rows.encode("ascii"))
    body = {
        "schema": "cm2.c27-independent.primitive-twenty-family-gate-v5-actual-v2-dual-seed-terminal-receipt.v1",
        "status": "PASS_ACTUAL_V2_TWO_REAL_SEEDS_INDEPENDENT_REPLAY_24_ATTACKS_COLD_REPLAY_TERMINAL_SEAL__ZERO_CREDIT",
        "sealed_at_utc": utc_now(),
        "execution_seeds": [args.seed1, args.seed2],
        "base_seal": {
            "receipt_file_sha256": receipt_file_sha,
            "receipt_object_sha256": receipt["receipt_sha256"],
            "payload_manifest_file_sha256": payload_sha,
            "root_manifest_file_sha256": root_sha,
        },
        "cold_replay": {
            "file_sha256": fsha(replay_path),
            "object_sha256": replay["result_sha256"],
            "semantic_projection_sha256": replay["semantic_projection_sha256"],
        },
        "terminal_payload_manifest": {
            "entry_count": len(terminal_payloads),
            "file_sha256": fsha(terminal_payload_manifest),
        },
        "source_pins": pins,
        "exact_census": receipt["exact_census"],
        "seed_invariant_mathematical_projection_sha256":
            receipt["seed_invariant_mathematical_projection_sha256"],
        "actual_v2_terminal_seal_passed": True,
        "formal_credit": 0, "manifest_authorized": False,
        "C27R2_C28_C29": "AUTHORIZED_TO_BEGIN_FRESH_REBUILD_ONLY__NOT_REBUILT_NOT_CREDITED",
        "Source_G": "ACTUAL_V2_TERMINAL_ZERO_CREDIT_AUTHORITY_RESTORED_FOR_FRESH_DOWNSTREAM_REBUILD",
        "CM2": "NO-GO_FOR_CLAIM",
    }
    result = dict(body)
    result["terminal_receipt_sha256"] = digest(result)
    terminal_receipt = terminal_dir / "terminal_receipt.json"
    write_json(terminal_receipt, result)
    root_manifest = terminal_dir / "root_manifest.sha256"
    exclusive(root_manifest, (
        f"{fsha(terminal_payload_manifest)}  payload_manifest.sha256\n"
        f"{fsha(terminal_receipt)}  terminal_receipt.json\n").encode("ascii"))
    exclusive(terminal_dir / "PASS.lock",
              b"PASS_ACTUAL_V2_DUAL_SEED_TERMINAL_ZERO_CREDIT_SEAL\n")
    return result


def preflight(args: argparse.Namespace) -> dict[str, Any]:
    seed1_out = inside(Path(args.seed1_out))
    seed1_run = inside(Path(args.seed1_run))
    seed2_out = inside(Path(args.seed2_out))
    seed2_run = inside(Path(args.seed2_run))
    handoff = inside(Path(args.handoff_dir))
    run_dir = inside(Path(args.finalizer_run_dir))
    seal_dir = inside(Path(args.seal_dir))
    terminal_dir = inside(Path(args.terminal_dir))
    need(args.seed1 > 0 and args.seed2 > 0 and args.seed1 != args.seed2,
         "two distinct positive real seeds")
    need(args.verification_seed > 0 and args.replay_seed > 0,
         "positive verifier/replay seeds")
    pins = source_pins(args)
    need(seed1_out.is_dir() and seed1_run.is_dir(), "seed1 paths exist")
    need(not (seed1_run / "FAILED.lock").exists(), "seed1 not failed")
    need(not (seed2_run / "FAILED.lock").exists(), "seed2 not failed")
    need(not run_dir.exists() and not seal_dir.exists()
         and not terminal_dir.exists(), "fresh finalizer/seal/terminal paths")
    need(len({seed1_out, seed1_run, seed2_out, seed2_run, handoff,
              run_dir, seal_dir, terminal_dir}) == 8,
         "all transaction paths distinct")
    seed1_state = service_state(args.seed1_service)
    seed2_state = service_state(args.seed2_service)
    need(seed1_state[0] in {"active", "activating", "deactivating", "inactive"}
         and seed2_state[0] in {"active", "activating", "deactivating", "inactive"},
         "known seed service states")
    return {
        "schema": "cm2.c27-actual-v2-dual-seed-finalizer-preflight.v1",
        "status": "PASS_FRESH_PATHS_PINS_AND_LIVE_OR_TERMINAL_SEED_SERVICES__ZERO_CREDIT",
        "source_pins": pins,
        "seed1_service_state": list(seed1_state),
        "seed2_service_state": list(seed2_state),
        "seed1": args.seed1, "seed2": args.seed2,
        "formal_credit": 0, "manifest_authorized": False,
        "C27R2_C28_C29": "UNAUTHORIZED_PENDING_ACTUAL_V2_TERMINAL_SEAL",
        "CM2": "NO-GO_FOR_CLAIM",
    }


def execute(args: argparse.Namespace) -> dict[str, Any]:
    check = preflight(args)
    run_dir = inside(Path(args.finalizer_run_dir))
    seal_dir = inside(Path(args.seal_dir))
    terminal_dir = inside(Path(args.terminal_dir))
    seed1_out = inside(Path(args.seed1_out))
    seed1_run = inside(Path(args.seed1_run))
    seed2_out = inside(Path(args.seed2_out))
    seed2_run = inside(Path(args.seed2_run))
    handoff = inside(Path(args.handoff_dir))
    run_dir.mkdir(parents=True, mode=0o700)
    stage = "watcher_initialization"
    try:
        write_json(run_dir / "watcher_start.json", {
            **check, "status": "WAITING_FOR_SEED2_TERMINAL_NATIVE_PASS__ZERO_CREDIT",
            "started_at_utc": utc_now(), "watcher_pid": os.getpid(),
            "seed1_service": args.seed1_service,
            "seed2_service": args.seed2_service,
        })

        def interrupted(signum: int, _frame: Any) -> None:
            raise Failure("finalizer interrupted by signal:" + str(signum))

        for item in (signal.SIGTERM, signal.SIGINT, signal.SIGHUP):
            signal.signal(item, interrupted)
        stage = "wait_seed2_native_terminal"
        terminal_state = wait_terminal(args.seed2_service, seed2_run,
                                       args.timeout_seconds)
        stage = "quick_native_dual_validation"
        seed1_evidence = quick_native(args.seed1, seed1_out, seed1_run)
        seed2_evidence = quick_native(args.seed2, seed2_out, seed2_run)
        need(seed1_evidence["input_snapshot_sha256"]
             == seed2_evidence["input_snapshot_sha256"],
             "dual native input snapshot identity")
        pins = source_pins(args)
        write_json(run_dir / "native_gate.json", {
            "schema": "cm2.c27-actual-v2-dual-seed-native-gate.v1",
            "status": "PASS_BOTH_NATIVE_TRANSACTIONS_7_OF_7_EXIT0_NO_SIGNAL_EMPTY_STDERR_PRE_POST_IDENTICAL__ZERO_CREDIT",
            "seed2_service_terminal_state": list(terminal_state),
            "seed1": seed1_evidence, "seed2": seed2_evidence,
            "formal_credit": 0, "manifest_authorized": False,
            "C27R2_C28_C29": "UNAUTHORIZED_PENDING_ACTUAL_V2_TERMINAL_SEAL",
            "CM2": "NO-GO_FOR_CLAIM",
        })
        stage = "independent_verification_attacks_and_base_seal"
        seal_dir.mkdir(parents=True, mode=0o700)
        receipt, receipt_file_sha, payload_sha, root_sha = build_base_seal(
            args, pins, run_dir, seal_dir, seed1_out, seed1_run,
            seed2_out, seed2_run, handoff)
        stage = "cold_replay_and_terminal_receipt"
        result = build_terminal(args, pins, run_dir, seal_dir, terminal_dir,
                                receipt, receipt_file_sha, payload_sha, root_sha)
        need(source_pins(args) == pins, "terminal source pins unchanged")
        write_json(run_dir / "final_result.json", result)
        exclusive(run_dir / "PASS.lock",
                  b"PASS_ACTUAL_V2_DUAL_SEED_FINALIZER_TERMINAL_ZERO_CREDIT\n")
        return result
    except BaseException as error:
        failure = {
            "schema": "cm2.c27-actual-v2-dual-seed-finalizer-failure.v1",
            "status": "FAIL_CLOSED_ZERO_CREDIT",
            "stage": stage, "error_type": type(error).__name__,
            "error": str(error), "recorded_at_utc": utc_now(),
            "formal_credit": 0, "manifest_authorized": False,
            "C27R2_C28_C29": "UNAUTHORIZED",
            "CM2": "NO-GO_FOR_CLAIM",
        }
        try:
            write_json(run_dir / "failure.json", failure)
            exclusive(run_dir / "FAILED.lock", b"FAIL_CLOSED_ZERO_CREDIT\n")
        except FileExistsError:
            pass
        raise


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed1", type=int, required=True)
    parser.add_argument("--seed1-service", required=True)
    parser.add_argument("--seed1-out", required=True)
    parser.add_argument("--seed1-run", required=True)
    parser.add_argument("--seed2", type=int, required=True)
    parser.add_argument("--seed2-service", required=True)
    parser.add_argument("--seed2-out", required=True)
    parser.add_argument("--seed2-run", required=True)
    parser.add_argument("--handoff-dir", required=True)
    parser.add_argument("--finalizer-run-dir", required=True)
    parser.add_argument("--seal-dir", required=True)
    parser.add_argument("--terminal-dir", required=True)
    parser.add_argument("--expect-verifier-sha256", required=True)
    parser.add_argument("--expect-attack-sha256", required=True)
    parser.add_argument("--expect-replay-sha256", required=True)
    parser.add_argument("--expect-finalizer-sha256", required=True)
    parser.add_argument("--expect-python-sha256", required=True)
    parser.add_argument("--verification-seed", type=int, default=30661701)
    parser.add_argument("--replay-seed", type=int, default=30662501)
    parser.add_argument("--timeout-seconds", type=int, default=259200)
    parser.add_argument("--preflight-only", action="store_true")
    args = parser.parse_args()
    try:
        result = preflight(args) if args.preflight_only else execute(args)
    except (Failure, KeyError, TypeError, ValueError, OSError,
            json.JSONDecodeError) as error:
        print("FAIL:" + str(error))
        return 2
    print(canonical(result if args.preflight_only else {
        "status": result["status"],
        "terminal_receipt_sha256": result["terminal_receipt_sha256"],
        "C27R2_C28_C29": result["C27R2_C28_C29"],
        "CM2": result["CM2"],
    }).decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
