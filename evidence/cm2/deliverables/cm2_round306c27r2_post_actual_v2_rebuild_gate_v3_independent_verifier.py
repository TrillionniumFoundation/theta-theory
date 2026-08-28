#!/usr/bin/env python3
"""No-import verifier for the post-actual-v2 C27R2 rebuild launch gate v3."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import stat
import subprocess
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
SERVICE_UNIT = "cm2-c27-source-g-actual-v2-p1-finalizer-v2-20260808T1544.service"
FINALIZER_RUN = ROOT / ".cm2-runtime/audit/c27-primitive-twenty-family-gate-v5-actual-v2-dual-seed-finalizer-p1v2-20260808T1544-run"
BASE_SEAL = ROOT / ".cm2-runtime/audit/c27-primitive-twenty-family-gate-v5-actual-v2-dual-seed-zero-credit-seal-v2-20260808T1544"
TERMINAL = ROOT / ".cm2-runtime/audit/c27-primitive-twenty-family-gate-v5-actual-v2-dual-seed-zero-credit-seal-v2-20260808T1544-terminal-replay"

EXPECTED_HASHES = {
    BASE_SEAL / "receipt.json": "cf5e381c29e31a2b3b9107fc8e53109b15cee86d498bd11deed0558c4d85f614",
    BASE_SEAL / "payload_manifest.sha256": "99165cc3e0e7be219c8187158b68d822802a1c9f5451c210a5e76a5ecacb4020",
    BASE_SEAL / "root_manifest.sha256": "51472919ec2b51fb53ec5c078ac4e1b1e4c57526c7a79ce135511cf21016449b",
    TERMINAL / "terminal_receipt.json": "8fc365cc487d8f74695a858afd5ee26efc514547631960a9e0bc6dc8cf597cb1",
    TERMINAL / "terminal_replay.json": "aa0bcf639c416c5b2deaccd58070c561ab6f6607b33c94143f9358f4585f13b8",
    TERMINAL / "payload_manifest.sha256": "9cf2a36f207152a34b58e95500d84cf145d1950970c55e30ec52d509f578f79a",
    TERMINAL / "root_manifest.sha256": "c46609c00ede1308d160aa724c3ee7c9387d0329c82be7d01d09d12a3ddaadae",
    FINALIZER_RUN / "final_result.json": "8fc365cc487d8f74695a858afd5ee26efc514547631960a9e0bc6dc8cf597cb1",
}

SOURCE_HASHES = {
    ROOT / "deliverables/cm2_c27_primitive_twenty_family_gate_v5_actual_v2_runner.py": "c0f2c29d03aad122762ba0b3dad5885418c17872dab3da665eb764dad9cab245",
    ROOT / "deliverables/cm2_c27_primitive_twenty_family_gate_v5_actual_v2.py": "038c6a661438f9253fb00a29b9f41941bea33a3a8769a258d8dfa5763880b561",
    ROOT / "deliverables/cm2_c27_primitive_twenty_family_gate_v5_actual_v2_seed2_gated_handoff.py": "3e5f874230c9faf809975808a2bd7284acf32c6e2b771e36a86d532a1a22c386",
    ROOT / "deliverables/cm2_c27_primitive_twenty_family_gate_v5_actual_v2_dual_seed_independent_verifier_v2.py": "fa85d391ec62a4e0026bd6895f2adb76df052c10426b0317466e0238ccc31268",
    ROOT / "deliverables/cm2_c27_primitive_twenty_family_gate_v5_actual_v2_dual_seed_coherent_attack_harness_v2.py": "883992243b9aabbcb948ca76484e2f77994a874d9a9034190084ebe987af34ae",
    ROOT / "deliverables/cm2_c27_primitive_twenty_family_gate_v5_actual_v2_dual_seed_terminal_replay_v1.py": "bce8f616c139823300f14fe7c16eeec60d4a4455216926fc1cff09d47d87bcab",
    ROOT / "deliverables/cm2_c27_primitive_twenty_family_gate_v5_actual_v2_dual_seed_finalizer_watcher_v2.py": "b34b41bb070d83312ff3687439d0f0afa88633ec50b5321a061e5b6a8ee5e4e0",
    ROOT / "deliverables/cm2_round306c15_source_g_502204_member_fresh_dsu_freeze_member_component_ledger.jsonl.gz": "e70c667fd8f14cb3c3d6444bb752dfc86244e61be292a9f884889d53951ff25a",
    Path("/usr/bin/python3.12"): "1643dacd9feaedc58f3cc581e4d22577dfe25c09b10282936186ccf0f2e61118",
}
TERMINAL_SCHEMA = "cm2.c27-independent.primitive-twenty-family-gate-v5-actual-v2-dual-seed-terminal-receipt.v1"
TERMINAL_STATUS = "PASS_ACTUAL_V2_TWO_REAL_SEEDS_INDEPENDENT_REPLAY_24_ATTACKS_COLD_REPLAY_TERMINAL_SEAL__ZERO_CREDIT"
REPLAY_SCHEMA = "cm2.c27-independent.primitive-twenty-family-gate-v5-actual-v2-dual-seed-terminal-replay.v1"
REPLAY_STATUS = "PASS_COLD_ROOT_PAYLOAD_CURRENT_SHA_STAT_NATIVE_DUAL_SEED_INDEPENDENT_REPLAY_AND_24_ATTACKS__ZERO_CREDIT"
POSITIVE_STATUS = "PASS_EXACT_ACTUAL_V2_DUAL_SEED_TERMINAL_SERVICE_RECEIPT_ROOT_PAYLOAD_AND_PASS_LOCK__FRESH_C27R2_REBUILD_MAY_BEGIN__ZERO_CREDIT"
NEGATIVE_STATUS = "REJECT_STATIC_SELF_TEST_ACTUAL_V2_TERMINAL_RECEIPT_MISSING__ZERO_CREDIT"
ALLOWED_IMPORTS = {
    "__future__", "argparse", "hashlib", "json", "os", "pathlib",
    "stat", "subprocess", "typing",
}


class Reject(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Reject(label)


def wire(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def object_sha(value: Any) -> str:
    return hashlib.sha256(wire(value)).hexdigest()


def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    output: dict[str, Any] = {}
    for key, value in pairs:
        need(key not in output, "duplicate-key:" + key)
        output[key] = value
    return output


def parse_json(raw: bytes, label: str, closure: str | None = None) -> Any:
    value = json.loads(
        raw, object_pairs_hook=unique,
        parse_constant=lambda item: (_ for _ in ()).throw(
            Reject(label + ":nonfinite:" + item)))
    need(raw == wire(value) + b"\n", label + ":canonical")
    if closure is not None:
        need(type(value) is dict, label + ":object")
        body = dict(value)
        claim = body.pop(closure, None)
        need(type(claim) is str and claim == object_sha(body), label + ":closure")
    return value


def file_sha(path: Path) -> str:
    descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
                         | getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(descriptor)
        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1,
             "regular-single-link:" + str(path))
        identity = (before.st_dev, before.st_ino, before.st_mode, before.st_nlink,
                    before.st_size, before.st_mtime_ns, before.st_ctime_ns,
                    before.st_uid, before.st_gid)
        state = hashlib.sha256()
        while block := os.read(descriptor, 4 << 20):
            state.update(block)
        after = os.fstat(descriptor)
        need(identity == (after.st_dev, after.st_ino, after.st_mode, after.st_nlink,
                          after.st_size, after.st_mtime_ns, after.st_ctime_ns,
                          after.st_uid, after.st_gid),
             "stable-fstat:" + str(path))
        return state.hexdigest()
    finally:
        os.close(descriptor)


def strict_file(path: Path, expected: str) -> bytes:
    need(not path.is_symlink() and file_sha(path) == expected,
         "pinned-file:" + str(path))
    raw = path.read_bytes()
    need(hashlib.sha256(raw).hexdigest() == expected,
         "stable-second-read:" + str(path))
    return raw


def manifest(raw: bytes, count: int, label: str) -> list[tuple[str, str]]:
    need(raw.endswith(b"\n"), label + ":newline")
    lines = raw.decode("ascii", "strict").splitlines()
    need(len(lines) == count, label + ":count")
    output = []
    seen = set()
    for ordinal, line in enumerate(lines):
        pieces = line.split("  ", 1)
        need(len(pieces) == 2 and len(pieces[0]) == 64
             and all(char in "0123456789abcdef" for char in pieces[0])
             and pieces[1] not in seen, f"{label}:line:{ordinal}")
        seen.add(pieces[1])
        output.append((pieces[1], pieces[0]))
    return output


def payload_path(relative: str) -> Path:
    pure = PurePosixPath(relative)
    need(not pure.is_absolute() and ".." not in pure.parts
         and "." not in pure.parts and str(pure) == relative,
         "payload-path:" + relative)
    path = (ROOT / relative).resolve()
    need(path == ROOT or ROOT in path.parents, "payload-workspace:" + relative)
    return path


def source_audit(path: Path, expected: str) -> dict[str, Any]:
    raw = strict_file(path, expected)
    tree = ast.parse(raw, filename=str(path))
    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.extend(alias.name.split(".", 1)[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            imports.append((node.module or "").split(".", 1)[0])
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            need(node.func.id not in {"eval", "exec", "__import__"},
                 "producer-dynamic-execution")
    need(set(imports) <= ALLOWED_IMPORTS, "producer-import-surface")
    text = raw.decode("utf-8")
    for forbidden in (
        "cm2_round306c27_source_g_corrected_transition_frontier",
        "cm2_round306c28_source_g_125616475670",
        "cm2_round306c29_source_g_maximal_component",
    ):
        need(forbidden not in text, "producer-forbidden-old-authority:" + forbidden)
    return {"sha256": expected, "stdlib_only": True,
            "producer_module_imported": False,
            "import_roots": sorted(set(imports))}


def verify_payloads() -> dict[str, Any]:
    for path, expected in EXPECTED_HASHES.items():
        strict_file(path, expected)
    for path, expected in SOURCE_HASHES.items():
        strict_file(path, expected)
    base_receipt_raw = strict_file(BASE_SEAL / "receipt.json",
                                   EXPECTED_HASHES[BASE_SEAL / "receipt.json"])
    terminal_receipt_raw = strict_file(
        TERMINAL / "terminal_receipt.json",
        EXPECTED_HASHES[TERMINAL / "terminal_receipt.json"])
    replay_raw = strict_file(TERMINAL / "terminal_replay.json",
                             EXPECTED_HASHES[TERMINAL / "terminal_replay.json"])
    base = parse_json(base_receipt_raw, "base-receipt", "receipt_sha256")
    terminal = parse_json(terminal_receipt_raw, "terminal-receipt",
                          "terminal_receipt_sha256")
    replay = parse_json(replay_raw, "terminal-replay", "result_sha256")
    need(terminal["schema"] == TERMINAL_SCHEMA
         and terminal["status"] == TERMINAL_STATUS
         and terminal["actual_v2_terminal_seal_passed"] is True
         and terminal["formal_credit"] == 0
         and terminal["manifest_authorized"] is False
         and terminal["C27R2_C28_C29"]
             == "AUTHORIZED_TO_BEGIN_FRESH_REBUILD_ONLY__NOT_REBUILT_NOT_CREDITED"
         and terminal["CM2"] == "NO-GO_FOR_CLAIM",
         "terminal-state")
    need(replay["schema"] == REPLAY_SCHEMA and replay["status"] == REPLAY_STATUS
         and replay["actual_v2_terminal_gate"]
             == "PASS_COLD_REPLAY_READY_FOR_TERMINAL_RECEIPT"
         and replay["formal_credit"] == 0
         and replay["manifest_authorized"] is False
         and replay["C27R2_C28_C29"] == "UNAUTHORIZED_PENDING_TERMINAL_RECEIPT",
         "replay-state")
    need(base["formal_credit"] == 0 and base["manifest_authorized"] is False
         and base["C27R2_C28_C29"]
             == "UNAUTHORIZED_PENDING_ACTUAL_V2_COLD_REPLAY",
         "base-state")
    need((FINALIZER_RUN / "PASS.lock").read_bytes()
         == b"PASS_ACTUAL_V2_DUAL_SEED_FINALIZER_TERMINAL_ZERO_CREDIT\n"
         and (TERMINAL / "PASS.lock").read_bytes()
         == b"PASS_ACTUAL_V2_DUAL_SEED_TERMINAL_ZERO_CREDIT_SEAL\n"
         and not (FINALIZER_RUN / "FAILED.lock").exists()
         and not (TERMINAL / "FAILED.lock").exists(), "exclusive-pass-locks")
    need(strict_file(FINALIZER_RUN / "final_result.json",
                     EXPECTED_HASHES[FINALIZER_RUN / "final_result.json"])
         == terminal_receipt_raw, "final-result-byte-identity")
    base_payload_sha = EXPECTED_HASHES[BASE_SEAL / "payload_manifest.sha256"]
    base_receipt_sha = EXPECTED_HASHES[BASE_SEAL / "receipt.json"]
    need(strict_file(BASE_SEAL / "root_manifest.sha256",
                     EXPECTED_HASHES[BASE_SEAL / "root_manifest.sha256"])
         == (f"{base_payload_sha}  payload_manifest.sha256\n"
             f"{base_receipt_sha}  receipt.json\n").encode("ascii"),
         "base-root")
    terminal_payload_sha = EXPECTED_HASHES[TERMINAL / "payload_manifest.sha256"]
    terminal_receipt_sha = EXPECTED_HASHES[TERMINAL / "terminal_receipt.json"]
    need(strict_file(TERMINAL / "root_manifest.sha256",
                     EXPECTED_HASHES[TERMINAL / "root_manifest.sha256"])
         == (f"{terminal_payload_sha}  payload_manifest.sha256\n"
             f"{terminal_receipt_sha}  terminal_receipt.json\n").encode("ascii"),
         "terminal-root")
    for label, path, count in (
        ("base", BASE_SEAL / "payload_manifest.sha256", 56),
        ("terminal", TERMINAL / "payload_manifest.sha256", 12),
    ):
        raw = strict_file(path, EXPECTED_HASHES[path])
        for relative, expected in manifest(raw, count, label + "-payload"):
            need(file_sha(payload_path(relative)) == expected,
                 label + "-payload-hash:" + relative)
    for stage in ("independent_verifier", "coherent_attacks", "terminal_replay"):
        need((FINALIZER_RUN / (stage + ".exit_code.txt")).read_bytes() == b"0\n"
             and (FINALIZER_RUN / (stage + ".stderr.log")).read_bytes() == b"",
             "stage-exit0-empty-stderr:" + stage)
    return {
        "terminal_receipt_file_sha256": terminal_receipt_sha,
        "terminal_receipt_object_sha256": terminal["terminal_receipt_sha256"],
        "terminal_replay_file_sha256":
            EXPECTED_HASHES[TERMINAL / "terminal_replay.json"],
        "terminal_replay_object_sha256": replay["result_sha256"],
        "base_payload_entries": 56, "terminal_payload_entries": 12,
        "payload_hashes_verified": 68,
    }


def verify_service(receipt: dict[str, Any]) -> dict[str, Any]:
    expected = receipt["actual_v2_terminal_evidence"]["service"]
    show = subprocess.run([
        "/usr/bin/systemctl", "--user", "show", SERVICE_UNIT,
        "--property=Id", "--property=LoadState", "--property=ActiveState",
        "--property=SubState", "--property=Result", "--property=ExecMainCode",
        "--property=ExecMainStatus", "--no-pager",
    ], cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    need(show.returncode == 0 and show.stderr == b"", "service-show")
    values = dict(line.split("=", 1) for line in
                  show.stdout.decode("ascii").splitlines() if "=" in line)
    need(values.get("Id") == SERVICE_UNIT
         and values.get("ActiveState") == "inactive"
         and values.get("SubState") == "dead"
         and values.get("ExecMainStatus") == "0", "service-terminal")
    if values.get("LoadState") == "loaded":
        need(expected["mode"] == "LOADED_INACTIVE_DEAD_SUCCESS_EXIT0"
             and values.get("Result") == "success"
             and values.get("ExecMainCode") in {"1", "exited"},
             "loaded-service-evidence")
    else:
        need(values.get("LoadState") == "not-found"
             and expected["mode"]
                 == "TRANSIENT_UNIT_COLLECTED_AFTER_DURABLE_TERMINAL_SUCCESS",
             "collected-service-mode")
        journal = subprocess.run([
            "/usr/bin/journalctl", "--user", "-u", SERVICE_UNIT,
            "--no-pager", "-o", "cat",
        ], cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        need(journal.returncode == 0 and journal.stderr == b""
             and hashlib.sha256(journal.stdout).hexdigest()
                 == expected["journal_sha256"], "collected-service-journal")
    return {"mode": expected["mode"], "unit": SERVICE_UNIT}


def verify_receipt(receipt_path: Path, producer: Path,
                   producer_sha256: str) -> dict[str, Any]:
    source = source_audit(producer, producer_sha256)
    raw = receipt_path.read_bytes()
    receipt = parse_json(raw, "gate-receipt", "gate_receipt_sha256")
    need(receipt["schema"] == "cm2.round306c27r2.post-actual-v2-rebuild-gate.v3"
         and receipt["formal_credit"] == 0
         and receipt["manifest_authorized"] is False
         and receipt["C28"] == receipt["C29"] == "UNAUTHORIZED"
         and receipt["CM2"] == "NO-GO_FOR_CLAIM", "gate-governance")
    if receipt["decision"] == "REJECT":
        need(receipt["status"] == NEGATIVE_STATUS
             and receipt["intended_process_exit_code"] == 2
             and receipt["self_test_mode"] == "NEGATIVE_MISSING_TERMINAL_ONLY"
             and receipt["actual_v2_terminal_gate_validated"] is False
             and receipt["fresh_C27R2_rebuild_may_start"] is False
             and receipt["C27R2"] == "UNAUTHORIZED"
             and type(receipt["missing_required_paths"]) is list
             and len(receipt["missing_required_paths"]) == 1,
             "truthful-negative-self-test")
        missing = Path(receipt["missing_required_paths"][0])
        need(missing.is_absolute() and not missing.exists()
             and not (missing == ROOT or ROOT in missing.parents),
             "independent-missing-path")
        details = {"negative_missing_path_verified": str(missing)}
    else:
        need(receipt["decision"] == "PASS" and receipt["status"] == POSITIVE_STATUS
             and receipt["intended_process_exit_code"] == 0
             and receipt["self_test_mode"] is None
             and receipt["actual_v2_terminal_gate_validated"] is True
             and receipt["fresh_C27R2_rebuild_may_start"] is True
             and receipt["C27R2"]
                 == "PREFLIGHT_GATE_PASS_ONLY__NOT_REBUILT_NOT_CREDITED",
             "positive-gate-state")
        need(receipt["derived_post_rebuild_contract"] == {
            "initial_frozen_C15_components": 57_876,
            "proof_derived_component_edges": 14_860,
            "successful_DSU_merges": 14_192,
            "cycle_edges": 668,
            "post_C27R2_components": 43_684,
            "member_denominator": 502_204,
            "total_unordered_member_pairs": 126_104_177_706,
            "post_C27R2_within_component_pairs": 542_179_508,
            "post_C27R2_cross_component_pair_denominator": 125_561_998_198,
            "counts_are_launch_contract_not_formal_C27R2_authority": True,
        }, "derived-contract")
        payloads = verify_payloads()
        service = verify_service(receipt)
        evidence = receipt["actual_v2_terminal_evidence"]
        need(evidence["terminal_receipt_object_sha256"]
             == payloads["terminal_receipt_object_sha256"]
             and evidence["terminal_replay_object_sha256"]
                 == payloads["terminal_replay_object_sha256"]
             and evidence["base_payload_entries_verified"] == 56
             and evidence["terminal_payload_entries_verified"] == 12
             and evidence["all_payload_hashes_and_pre_post_stats_verified"] is True,
             "gate-evidence-binding")
        details = {"payloads": payloads, "service": service}
    return {"receipt": receipt, "source": source, "details": details}


def write_new(path: Path, value: dict[str, Any]) -> None:
    need(path.parent.is_dir(), "output-parent")
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL
                         | getattr(os, "O_NOFOLLOW", 0), 0o600)
    try:
        os.write(descriptor, wire(value) + b"\n")
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--receipt", required=True)
    parser.add_argument("--producer-source", required=True)
    parser.add_argument("--expect-producer-sha256", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    try:
        result = verify_receipt(Path(args.receipt).resolve(),
                                Path(args.producer_source).resolve(),
                                args.expect_producer_sha256)
        body = {
            "schema": "cm2.round306c27r2.post-actual-v2-rebuild-gate-independent-verification.v3",
            "status": "PASS_NO_IMPORT_INDEPENDENT_GATE_RECEIPT_SERVICE_ROOT_PAYLOAD_AND_GOVERNANCE_VERIFICATION__ZERO_CREDIT",
            "gate_receipt_file_sha256": file_sha(Path(args.receipt).resolve()),
            "gate_receipt_object_sha256": result["receipt"]["gate_receipt_sha256"],
            "gate_decision": result["receipt"]["decision"],
            "fresh_C27R2_rebuild_may_start":
                result["receipt"]["fresh_C27R2_rebuild_may_start"],
            "source_audit": result["source"], "details": result["details"],
            "producer_module_imported": False,
            "formal_credit": 0, "manifest_authorized": False,
            "C27R2": "NOT_REBUILT_NOT_CREDITED",
            "C28": "UNAUTHORIZED", "C29": "UNAUTHORIZED",
            "CM2": "NO-GO_FOR_CLAIM",
        }
        body["verification_sha256"] = object_sha(body)
        write_new(Path(args.output).resolve(), body)
        print(wire({"status": body["status"],
                    "verification_sha256": body["verification_sha256"],
                    "gate_decision": body["gate_decision"]}).decode("ascii"))
        return 0
    except (Reject, KeyError, TypeError, ValueError, OSError,
            json.JSONDecodeError, SyntaxError) as error:
        print("REJECT:" + str(error))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
