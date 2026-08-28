#!/usr/bin/env python3
"""Append-only zero-credit seal for the corrected T00 actual-v5 adapter."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
PYTHON = Path("/usr/bin/python3.12")
PYTHON_SHA = "1643dacd9feaedc58f3cc581e4d22577dfe25c09b10282936186ccf0f2e61118"
PINS = {
    "seed1_receipt": (
        ".cm2-runtime/audit/c27-primitive-v5-actual-t00-same-chart-exact-contact-adapter-v2-seed30647101-attempt2/adapter_receipt.json",
        "3f75140f8bf754f8ca503f8ea39062a4070e5e3303fb42c335071e7b149d542c",
        "63ccd4cf0679ad1bdd87d7f3a06e10c64c61d15158841716516147d46d9a0bf7",
        "receipt_sha256"),
    "seed2_receipt": (
        ".cm2-runtime/audit/c27-primitive-v5-actual-t00-same-chart-exact-contact-adapter-v2-seed30647991-attempt1/adapter_receipt.json",
        "ec6fc6e09355df236ca0af2d1812cde625e7d96c58444e5e0b0421d3068ac7ad",
        "a3f428e67b9fe323723fb14f950610997bffe3bd7d8117a0b1f0d33c6acba917",
        "receipt_sha256"),
    "seed1_run": (
        ".cm2-runtime/audit/c27-primitive-v5-actual-t00-same-chart-exact-contact-adapter-v2-seed30647101-attempt2-run/run_attestation.json",
        "b0c11e7fadf0ebc35f6cbc0787adb2d4b8e1d0f06b4eacc58276fc048d8169fe",
        "16421962c0facb3678dd9a797edd554ce50cf512ec18e497f048923f7cbc0c98",
        "run_attestation_sha256"),
    "seed2_run": (
        ".cm2-runtime/audit/c27-primitive-v5-actual-t00-same-chart-exact-contact-adapter-v2-seed30647991-attempt1-run/run_attestation.json",
        "ff6d5e69c49531379eef0bc8723329077d3294c041a02c5dcf62de8ca99761be",
        "03d7a35a234fed09114da666e0f71aa4a9fd0ad4b010cc7050f1e92b89cd0fdf",
        "run_attestation_sha256"),
    "verification": (
        ".cm2-runtime/audit/c27-primitive-v5-actual-t00-same-chart-exact-contact-adapter-v2-independent-verifier/verification.json",
        "a681ec83b06581cb9257739c10b99bc6a1ad0ad15c4d6c6d2f7ad04d6456bc39",
        "b4dfe7e085a3046370a16088ecd36e1bbb8379cb3b431b04e0a57ee7349125a4",
        "verification_sha256"),
    "verifier_run": (
        ".cm2-runtime/audit/c27-primitive-v5-actual-t00-same-chart-exact-contact-adapter-v2-independent-verifier-run/run_attestation.json",
        "8352e89842f50a401c42798a67d526603657cc397898a063d20dbe2ed71fadf5",
        "ceec8c3667a9d682c4813bce1df358b83e4fc5cfe2102587adcdfe750d98b01e",
        "run_attestation_sha256"),
    "attacks": (
        ".cm2-runtime/audit/c27-primitive-v5-actual-t00-same-chart-exact-contact-adapter-v2-coherent-attacks/attack_result.json",
        "774fb983cb553b7bf61adcbf28e3ccd5b4b2451185fdb6fec7339274e82f61ef",
        "33c4ea5aff0899cd7cc24942a8d2cf41d487ccc54ae1a5b8d6c91333a536e1b1",
        "attack_result_sha256"),
    "interface": (
        ".cm2-runtime/audit/c27r2-fresh-actual-v5-rebuild-interface-correction-v2/preflight.json",
        "6873b33d7b131a4bde0c4dbcf99873e6826cf2190fde6dfdf6640ee47d53c9d6",
        "3ece982b83b968e7cc23c4d43f2602fb5f8490484af5ed2f214515be4f0eb37e",
        "preflight_sha256"),
}
SOURCES = {
    "producer": (
        "deliverables/cm2_c27_primitive_v5_actual_t00_same_chart_exact_contact_adapter_v2.py",
        "27b1a0e0eef9d71070a5925a40b3a2d4e33608437545fde2e4ec2ad9013f4e66"),
    "producer_runner": (
        "deliverables/cm2_c27_primitive_v5_actual_t00_same_chart_exact_contact_adapter_v2_runner.py",
        "38af3747bed3f8800972847c104328b7aa870c1c63bfb8232282ec533fe041fd"),
    "verifier": (
        "deliverables/cm2_c27_primitive_v5_actual_t00_same_chart_exact_contact_adapter_v2_independent_verifier.py",
        "775ddcebebc8758d2fe70a28e0c34c02767d65f4f01235898396eeca92a2731b"),
    "verifier_runner": (
        "deliverables/cm2_c27_primitive_v5_actual_t00_same_chart_exact_contact_adapter_v2_verifier_runner.py",
        "21ebffcd4205c7b49c0cb3c567f753eb6ed9584c17b19f77b4cb13ac87406f16"),
    "attack_harness": (
        "deliverables/cm2_c27_primitive_v5_actual_t00_same_chart_exact_contact_adapter_v2_attack_harness.py",
        "72c0ef82b567a5e6f17f1f9ae711497834be35e36c21d816dbd81b14e3d4231a"),
}
RUN_DIRS = {
    "seed1": ".cm2-runtime/audit/c27-primitive-v5-actual-t00-same-chart-exact-contact-adapter-v2-seed30647101-attempt2-run",
    "seed2": ".cm2-runtime/audit/c27-primitive-v5-actual-t00-same-chart-exact-contact-adapter-v2-seed30647991-attempt1-run",
    "verifier": ".cm2-runtime/audit/c27-primitive-v5-actual-t00-same-chart-exact-contact-adapter-v2-independent-verifier-run",
}


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


def byte_identical(left: Path, right: Path) -> bool:
    if left.stat().st_size != right.stat().st_size:
        return False
    with left.open("rb") as a, right.open("rb") as b:
        while True:
            x, y = a.read(4 << 20), b.read(4 << 20)
            if x != y:
                return False
            if not x:
                return True


def document(path: Path, closure: str) -> dict[str, Any]:
    value = json.loads(path.read_bytes())
    body = dict(value)
    claim = body.pop(closure, None)
    need(type(claim) is str and claim == digest(body),
         "document closure:" + path.name)
    return value


def workspace_path(relative: str) -> Path:
    path = (ROOT / relative).resolve()
    need(ROOT in path.parents, "path inside workspace")
    return path


def manifest_entry(path: Path) -> str:
    need(ROOT in path.resolve().parents, "manifest member inside workspace")
    return f"{fsha(path)}  {path.resolve().relative_to(ROOT)}\n"


def write_exclusive(path: Path, payload: bytes) -> None:
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL
                 | getattr(os, "O_NOFOLLOW", 0), 0o600)
    try:
        os.write(fd, payload)
        os.fsync(fd)
    finally:
        os.close(fd)


def run_evidence(label: str) -> dict[str, Any]:
    directory = workspace_path(RUN_DIRS[label])
    command_path = directory / "command.json"
    stdout_path = directory / "stdout.log"
    stderr_path = directory / "stderr.log"
    exit_path = directory / "exit_code.txt"
    need(all(path.is_file() for path in
             (command_path, stdout_path, stderr_path, exit_path)),
         "complete run evidence:" + label)
    command = json.loads(command_path.read_bytes())
    need(type(command) is list and all(type(item) is str for item in command),
         "argv vector:" + label)
    need(stderr_path.read_bytes() == b"" and exit_path.read_bytes() == b"0\n"
         and len(stdout_path.read_bytes().splitlines()) == 1,
         "exit/stderr/stdout:" + label)
    return {"argv": command,
            "command_file_sha256": fsha(command_path),
            "stdout_file_sha256": fsha(stdout_path),
            "stderr_file_sha256": fsha(stderr_path),
            "exit_code_file_sha256": fsha(exit_path)}


def build(output: Path) -> dict[str, Any]:
    need(not output.exists(), "fresh output")
    need(all(file_pin != "PENDING" and object_pin != "PENDING"
             for _, file_pin, object_pin, _ in PINS.values()),
         "all evidence pins finalized")
    documents = {}
    for label, (relative, file_pin, object_pin, closure) in PINS.items():
        path = workspace_path(relative)
        need(path.is_file() and fsha(path) == file_pin, "file pin:" + label)
        row = document(path, closure)
        need(row[closure] == object_pin, "object pin:" + label)
        documents[label] = row
    for label, (relative, pin) in SOURCES.items():
        need(fsha(workspace_path(relative)) == pin, "source pin:" + label)
    need(PYTHON.is_file() and fsha(PYTHON) == PYTHON_SHA
         and Path(shutil.which("python") or "").resolve() == PYTHON,
         "python runtime alias and hash")

    seed1, seed2 = documents["seed1_receipt"], documents["seed2_receipt"]
    run1, run2 = documents["seed1_run"], documents["seed2_run"]
    verification = documents["verification"]
    verifier_run = documents["verifier_run"]
    attacks = documents["attacks"]
    need(seed1["execution_seed"] == 30_647_101
         and seed2["execution_seed"] == 30_647_991
         and seed1["execution_seed"] != seed2["execution_seed"]
         and seed1["exact_census"] == seed2["exact_census"]
         and seed1["formal_credit"] == seed2["formal_credit"] == 0,
         "dual seed receipts")
    expected = {"candidate_count": 5_970_840,
                "lower_cross_component_candidate_count": 2_598_666,
                "lower_same_component_candidate_count": 3_185_042,
                "strict_cross_component_physical_proof_count": 32_240,
                "unique_component_edge_count": 14_772}
    need(all(seed1["exact_census"][key] == value
             for key, value in expected.items()), "exact census")
    ledgers = []
    for key in ("primitive_authority_ledger", "candidate_ownership_ledger",
                "materialized_physical_proof_fragment_ledger"):
        left = seed1["terminal_adapter"][key]
        right = seed2["terminal_adapter"][key]
        a, b = workspace_path(left["path"]), workspace_path(right["path"])
        need({k: left[k] for k in left if k != "path"}
             == {k: right[k] for k in right if k != "path"}
             and byte_identical(a, b), "dual ledger:" + key)
        ledgers.append((left, right))
    for run, receipt, pin_label in ((run1, seed1, "seed1_receipt"),
                                    (run2, seed2, "seed2_receipt")):
        need(run["run"]["numeric_exit_code"] == 0
             and run["run"]["signal"] is None
             and run["run"]["stderr_empty"] is True
             and run["run"]["pre_post_sha256_identical"] is True
             and run["run"]["pre_post_stat_identical"] is True
             and run["input_pre"] == run["input_post"]
             and run["run"]["receipt_file_sha256"] == PINS[pin_label][1]
             and run["run"]["receipt_object_sha256"] == receipt["receipt_sha256"],
             "producer run attestation")
    need(verification["status"].startswith("PASS_NO_PRODUCER_IMPORT")
         and verification["producer_imported"] is False
         and verification["exact_census"]["candidate_count"] == 5_970_840
         and verification["exact_census"]["physical_proof_count"] == 32_240
         and verification["exact_census"]["unique_component_edge_count"] == 14_772
         and verification["exact_census"]["observed_unmatched_candidate_count"] == 0
         and verification["formal_credit"] == 0,
         "independent verification")
    need(verifier_run["run"]["numeric_exit_code"] == 0
         and verifier_run["run"]["signal"] is None
         and verifier_run["run"]["stderr_empty"] is True
         and verifier_run["run"]["runtime_path"] == str(PYTHON)
         and verifier_run["run"]["runtime_sha256"] == PYTHON_SHA
         and verifier_run["run"]["verification_file_sha256"] == PINS["verification"][1]
         and verifier_run["run"]["verification_object_sha256"]
             == verification["verification_sha256"]
         and verifier_run["input_pre"] == verifier_run["input_post"],
         "verifier run attestation")
    need(attacks["census"] == {
            "attack_count": 22, "coherently_resigned_attack_count": 22,
            "row_reclosed_attack_count": 2, "rejected_count": 22}
         and attacks["formal_credit"] == 0,
         "coherent attacks")

    evidence = {label: run_evidence(label) for label in RUN_DIRS}
    producer = str(workspace_path(SOURCES["producer"][0]))
    for label, seed, receipt_path in (
            ("seed1", 30_647_101, workspace_path(PINS["seed1_receipt"][0])),
            ("seed2", 30_647_991, workspace_path(PINS["seed2_receipt"][0]))):
        expected_argv = ["python", "-B", producer, "--out-dir",
                         str(receipt_path.parent), "--seed", str(seed)]
        need(evidence[label]["argv"] == expected_argv,
             "exact producer argv:" + label)
    verifier_argv = [str(PYTHON), "-B",
        str(workspace_path(SOURCES["verifier"][0])),
        "--receipt", str(workspace_path(PINS["seed1_receipt"][0])),
        "--second-receipt", str(workspace_path(PINS["seed2_receipt"][0])),
        "--run-attestation", str(workspace_path(PINS["seed1_run"][0])),
        "--second-run-attestation", str(workspace_path(PINS["seed2_run"][0])),
        "--temporary-db", str(workspace_path(
            ".cm2-runtime/audit/c27-primitive-v5-actual-t00-same-chart-exact-contact-adapter-v2-independent-verifier/temporary.sqlite")),
        "--output", str(workspace_path(PINS["verification"][0]))]
    need(evidence["verifier"]["argv"] == verifier_argv,
         "exact verifier argv")

    output.mkdir(parents=True)
    payload_paths: set[Path] = set()
    for relative, _, _, _ in PINS.values():
        payload_paths.add(workspace_path(relative))
    for relative, _ in SOURCES.values():
        payload_paths.add(workspace_path(relative))
    payload_paths.add(Path(__file__).resolve())
    for receipt in (seed1, seed2):
        payload_paths.add(workspace_path(receipt["terminal_adapter"]
                                        ["primitive_authority_ledger"]["path"]))
        payload_paths.add(workspace_path(receipt["terminal_adapter"]
                                        ["candidate_ownership_ledger"]["path"]))
        payload_paths.add(workspace_path(receipt["terminal_adapter"]
                                        ["materialized_physical_proof_fragment_ledger"]["path"]))
        payload_paths.add(workspace_path(
            str(Path(PINS["seed1_receipt" if receipt is seed1 else
                          "seed2_receipt"][0]).parent / "manifest.sha256")))
        for item in receipt["root_input_capture"]["attestations"].values():
            payload_paths.add(workspace_path(item["path"]))
    for relative in RUN_DIRS.values():
        directory = workspace_path(relative)
        payload_paths.update(directory / name for name in
                             ("command.json", "stdout.log", "stderr.log",
                              "exit_code.txt", "run_attestation.json"))
    payload_lines = sorted(manifest_entry(path) for path in payload_paths)
    payload_path = output / "payload_manifest.sha256"
    write_exclusive(payload_path, "".join(payload_lines).encode("ascii"))

    body = {
        "schema": "cm2.c27-independent.primitive-v5-actual-t00-same-chart-exact-contact-adapter-v2-zero-credit-receipt.v1",
        "status": "PASS_T00_5970840_EXACT_CONTACT_CANDIDATES__DUAL_SEED_ROW_INVERSE_COMPLETE_ENUMERATION_22_ATTACKS__ZERO_CREDIT",
        "interface_v2_object_sha256": documents["interface"]["preflight_sha256"],
        "terminal_adapter": seed1["terminal_adapter"],
        "exact_census": seed1["exact_census"],
        "dual_seed": {
            "seed1_receipt_file_sha256": PINS["seed1_receipt"][1],
            "seed1_receipt_object_sha256": seed1["receipt_sha256"],
            "seed2_receipt_file_sha256": PINS["seed2_receipt"][1],
            "seed2_receipt_object_sha256": seed2["receipt_sha256"],
            "ledger_pair_count": 3, "all_ledgers_byte_identical": True,
            "producer_run_attestation_objects": [
                run1["run_attestation_sha256"], run2["run_attestation_sha256"]]},
        "independent_verifier": {
            "source_sha256": SOURCES["verifier"][1],
            "runner_source_sha256": SOURCES["verifier_runner"][1],
            "result_file_sha256": PINS["verification"][1],
            "result_object_sha256": verification["verification_sha256"],
            "run_attestation_file_sha256": PINS["verifier_run"][1],
            "run_attestation_object_sha256": verifier_run["run_attestation_sha256"],
            "producer_imported": False},
        "coherent_attacks": {
            "source_sha256": SOURCES["attack_harness"][1],
            "result_file_sha256": PINS["attacks"][1],
            "result_object_sha256": attacks["attack_result_sha256"],
            "attacks": 22, "rejected": 22, "row_reclosed": 2},
        "runtime_and_argv_closure": {
            "python_alias": "/usr/bin/python", "resolved_runtime": str(PYTHON),
            "runtime_sha256": PYTHON_SHA, "run_evidence": evidence},
        "payload_manifest": {"filename": payload_path.name,
                             "entry_count": len(payload_lines),
                             "file_sha256": fsha(payload_path)},
        "formal_credit": 0, "manifest_authorized": False,
        "Source_W_transition_authorized": False,
        "strict_nonpromotion": {"C27_transition_totality": 0,
                                "C28_pair_routing": 0,
                                "C29_physical_maximality": 0,
                                "CM2": "NO-GO_FOR_CLAIM"},
        "receipt_builder_source_sha256": fsha(Path(__file__).resolve()),
    }
    receipt = dict(body)
    receipt["receipt_sha256"] = digest(receipt)
    receipt_path = output / "receipt.json"
    write_exclusive(receipt_path, canonical(receipt) + b"\n")
    root_lines = sorted((manifest_entry(payload_path),
                         manifest_entry(receipt_path)))
    write_exclusive(output / "root_manifest.sha256",
                    "".join(root_lines).encode("ascii"))
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    try:
        receipt = build(Path(args.output_dir).resolve())
    except (Failure, KeyError, TypeError, ValueError, OSError,
            json.JSONDecodeError) as error:
        print("FAIL:" + str(error))
        return 2
    print(canonical({"status": receipt["status"],
                     "exact_census": receipt["exact_census"],
                     "receipt_sha256": receipt["receipt_sha256"]}).decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
