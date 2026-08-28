#!/usr/bin/env python3
"""Independent outer mathematical checker for the C30c v3 publication.

The checker validates the manifest-first byte graph, the deterministic raw
bundle, the exact Round306C30b predecessor, the v3 receipt replay, both bridge
checker receipts, the cold replay, all candidate ledgers, and one fresh
independent verifier execution.  Its output is conditional and zero credit;
only the separate terminal replay may authorize 80 -> 78.
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import os
import stat
import subprocess
import tarfile
from pathlib import Path
from typing import Any

WORKSPACE = Path("/home/qian-qi/.openclaw/workspaces/telegram-bot-8449317572")
DELIVERABLES = WORKSPACE / "deliverables"
AUDIT = WORKSPACE / ".cm2-runtime/audit"
RUN_NAME = "c30c-v5-toctou-robustness-rerun-20260808T0635Z-receipt-v3"
BRIDGE_NAME = "c30c-postreceipt-v3-p1-bridge-v1-20260808T0655Z"
RUN = AUDIT / RUN_NAME
RECEIPT = WORKSPACE / ".cm2-runtime/receipts" / RUN_NAME
BRIDGE = AUDIT / BRIDGE_NAME
PREFIX = "cm2_round306c30c_source_w_full_delta_whole_origin_disposition"
VALIDATOR = DELIVERABLES / "cm2_round306c30c_62_attack_run_receipt_validator_v3.py"
VERIFIER = DELIVERABLES / (PREFIX + "_independent_verifier.py")
PYTHON = WORKSPACE / ".cm2-runtime/python-flint-0.9.0/bin/python"
C30B_MANIFEST_REL = (
    "deliverables/cm2_round306c30b_source_w_outgoing_h_whole_origin_"
    "disposition_manifest.sha256"
)
C30B_MANIFEST_SHA256 = "6af636a4239f390712d057030f03e09fbbca332c6170f183d3d0095f19f0f248"
C30B_VERIFICATION_SHA256 = "e9e72536be9ba707fe2fdf6034b47978be4d09235e5133414ec7b0a31acf4e71"
VALIDATOR_SHA256 = "c68633b3cc996c344c737f1e6c71da382a81c8f6bf6c4318b233b6d9db34c97a"
VERIFIER_SHA256 = "0fd82ce16053b69cbb04eddc423cb3f4b8cf8d11923219b50e6ff659f97b7377"
RESULT_OBJECT_SHA256 = "df4531942e743389f5e8f85b2d013132f0808f562c21f430e7904577d67087d4"
VERIFIER_STATUS = (
    "PASS_INDEPENDENT_CANDIDATE_C30C__80_DELTA_H_CELLS__"
    "2_RESOLVED_MIXED__ZERO_FORMAL_CREDIT"
)
SCRIPT_NAMES = (
    PREFIX + "_audit_evidence_bundle_builder_v3.py",
    PREFIX + "_publication_manifest_builder_v3.py",
    PREFIX + "_formal_handoff_outer_verifier_v3.py",
    PREFIX + "_terminal_seal_replay_v3.py",
    "cm2_round306c30c_publication_static_consistency_gate_v3.py",
    "cm2_round306c30c_postreceipt_v3_publication_chain_watch_v1.py",
)
CANDIDATE_HASHES = {
    "cm2_round306c30b_python_flint_runtime_attestation.json":
        "6b48cd0ca3fd53f9fdd457cc3c1106055e12db4d4ad999fcfd1fc89ad36b95df",
    PREFIX + "_combined_boundary_atomic_owner_join_ledger.jsonl.gz":
        "63f004bdb065d8674ecfde9eb957f3477ee6c3f806064ef8f151850cd391d251",
    PREFIX + "_delta_h_cell_ledger.jsonl.gz":
        "acbd71e9155d81d17ae4b42eecd31f0fc9d4bb91ac36aa93a7ab7df08e3dee50",
    PREFIX + "_inherited_h_cell_ledger.jsonl.gz":
        "d4142d7748e0546184542bea7b3b337c9f33e7312efa2e7c5271d2a9dba30abd",
    PREFIX + "_result.json":
        "96c1e9f627bd6113fc56f7b6d35856581b57b4afde049e997b10eef3f8c706f1",
    PREFIX + "_whole_origin_ledger.jsonl.gz":
        "48a3e612de84004ba746d93d492e8f3e9f587ebf6b3574615fa946dddf21a573",
}
LEDGER_ROWS = {
    PREFIX + "_combined_boundary_atomic_owner_join_ledger.jsonl.gz": 2080,
    PREFIX + "_delta_h_cell_ledger.jsonl.gz": 80,
    PREFIX + "_inherited_h_cell_ledger.jsonl.gz": 88,
    PREFIX + "_whole_origin_ledger.jsonl.gz": 2,
}


class Blocked(RuntimeError):
    pass


def need(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise Blocked(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=True, allow_nan=False, sort_keys=True,
                      separators=(",", ":")).encode("ascii")


def identity(value: os.stat_result) -> tuple[int, ...]:
    return (value.st_dev, value.st_ino, value.st_mode, value.st_nlink,
            value.st_size, value.st_mtime_ns, value.st_ctime_ns)


def capture(path: Path, maximum: int = 64 << 30) -> bytes:
    absolute = Path(os.path.abspath(os.fspath(path)))
    need(absolute.resolve(strict=True) == absolute, "canonical path:" + os.fspath(path))
    descriptor = os.open(absolute, os.O_RDONLY | os.O_CLOEXEC |
                         getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(descriptor)
        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1 and
             0 <= before.st_size <= maximum, "bounded singleton:" + os.fspath(path))
        chunks: list[bytes] = []
        remaining = before.st_size
        while remaining:
            block = os.read(descriptor, min(4 << 20, remaining))
            need(bool(block), "complete read:" + os.fspath(path))
            chunks.append(block)
            remaining -= len(block)
        need(os.read(descriptor, 1) == b"", "stable EOF:" + os.fspath(path))
        after = os.fstat(descriptor)
    finally:
        os.close(descriptor)
    need(identity(before) == identity(after), "stable capture:" + os.fspath(path))
    return b"".join(chunks)


def hash_size(path: Path) -> tuple[str, int]:
    state = hashlib.sha256()
    descriptor = os.open(path, os.O_RDONLY | os.O_CLOEXEC |
                         getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(descriptor)
        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1,
             "hash singleton:" + os.fspath(path))
        total = 0
        while block := os.read(descriptor, 4 << 20):
            state.update(block)
            total += len(block)
        after = os.fstat(descriptor)
    finally:
        os.close(descriptor)
    need(identity(before) == identity(after) and total == before.st_size,
         "stable hash:" + os.fspath(path))
    return state.hexdigest(), total


def sha(path: Path) -> str:
    return hash_size(path)[0]


def strict_object_raw(raw: bytes, label: str) -> dict[str, Any]:
    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        output: dict[str, Any] = {}
        for key, value in pairs:
            need(type(key) is str and key not in output, "unique key:" + label)
            output[key] = value
        return output
    try:
        value = json.loads(raw.decode("ascii"), object_pairs_hook=unique,
                           parse_constant=lambda token: (_ for _ in ()).throw(ValueError(token)))
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as error:
        raise Blocked("strict JSON:" + label) from error
    need(type(value) is dict and raw in {canonical(value), canonical(value) + b"\n"},
         "canonical JSON:" + label)
    return value


def strict_object(path: Path, label: str) -> dict[str, Any]:
    return strict_object_raw(capture(path, 64 << 20), label)


def parse_manifest(path: Path) -> tuple[bytes, dict[str, str]]:
    raw = capture(path, 8 << 20)
    rows: dict[str, str] = {}
    try:
        lines = raw.decode("ascii").splitlines()
    except UnicodeDecodeError as error:
        raise Blocked("ASCII manifest:" + path.name) from error
    for line in lines:
        pieces = line.split("  ", 1)
        need(len(pieces) == 2 and len(pieces[0]) == 64 and
             all(c in "0123456789abcdef" for c in pieces[0]) and pieces[1] and
             not Path(pieces[1]).is_absolute() and ".." not in Path(pieces[1]).parts and
             pieces[1] not in rows, "manifest syntax:" + path.name)
        rows[pieces[1]] = pieces[0]
    need(raw == b"".join((rows[name] + "  " + name + "\n").encode("ascii")
                         for name in sorted(rows)), "canonical sorted manifest:" + path.name)
    return raw, rows


def c30b_member_names() -> set[str]:
    manifest = WORKSPACE / C30B_MANIFEST_REL
    need(sha(manifest) == C30B_MANIFEST_SHA256, "exact C30b manifest hash")
    _, rows = parse_manifest(manifest)
    need(len(rows) == 14, "C30b 14 members")
    for name, expected in rows.items():
        need(sha(DELIVERABLES / name) == expected, "C30b member:" + name)
    verification = strict_object(
        DELIVERABLES /
        "cm2_round306c30b_source_w_outgoing_h_whole_origin_disposition_verification.json",
        "C30b verification",
    )
    need(sha(DELIVERABLES /
             "cm2_round306c30b_source_w_outgoing_h_whole_origin_disposition_verification.json")
         == C30B_VERIFICATION_SHA256, "C30b verification hash")
    transition = verification.get("source_W_ledger_transition", {})
    need(verification.get("status") ==
         "PASS_FORMAL_C30B__688_H_CELLS__2_WHOLE_ORIGIN_EXCLUSIONS__"
         "10_RESOLVED_MIXED__SOURCE_W_92_TO_80__D02_STILL_BLOCKED"
         and transition.get("before", {}).get("remaining") == 92
         and transition.get("after", {}).get("remaining") == 80
         and transition.get("credits") == {"resolved_nonexcluded": 10,
                                            "resolved_origin_dispositions": 12,
                                            "whole_origin_exclusions": 2},
         "exact C30b formal authority")
    return {"deliverables/" + name for name in rows}


def expected_payload_names(chain_dir: Path) -> set[str]:
    names = c30b_member_names() | {C30B_MANIFEST_REL}
    names.update("deliverables/" + name for name in SCRIPT_NAMES)
    names.update("deliverables/" + name for name in (
        "cm2_round306c30c_62_attack_run_receipt_validator_v3.py",
        "cm2_round306c30c_postreceipt_v3_p1_bridge_watch_v1.py",
        PREFIX + "_independent_verifier.py", PREFIX + "_attack_harness.py",
        PREFIX + "_cold_trace_analyzer.py",
        "cm2_round306c30c_cold_trace_unfinished_pairing_attack_gate.py",
    ))
    for seed in ("30630071", "30630929"):
        names.update(".cm2-runtime/candidates/c30c-v4-seed-" + seed + "/" + name
                     for name in CANDIDATE_HASHES)
    names.update({
        ".cm2-runtime/receipts/" + RUN_NAME + "/receipt.json",
        ".cm2-runtime/audit/" + BRIDGE_NAME + "/terminal_status.json",
        ".cm2-runtime/audit/" + BRIDGE_NAME + "/receipt_gate.json",
        ".cm2-runtime/audit/" + BRIDGE_NAME + "/dual_checker_receipt.json",
        ".cm2-runtime/audit/" + BRIDGE_NAME + "/cold_replay_receipt.json",
        ".cm2-runtime/control/" + BRIDGE_NAME + "/pins.sha256",
        ".cm2-runtime/control/" + RUN_NAME + "/pins.sha256",
    })
    chain_rel = chain_dir.relative_to(WORKSPACE).as_posix()
    names.update({chain_rel + "/c30c_v3_audit_evidence.tar.gz",
                  chain_rel + "/evidence_bundle_receipt.json"})
    return names


def verify_manifests(chain_dir: Path) -> dict[str, str]:
    payload_raw, payload = parse_manifest(chain_dir / "payload_manifest.sha256")
    need(set(payload) == expected_payload_names(chain_dir), "exact payload member contract")
    for relative, expected in payload.items():
        path = WORKSPACE / relative
        need(path.resolve(strict=True).is_relative_to(WORKSPACE.resolve(strict=True)),
             "payload containment:" + relative)
        need(sha(path) == expected, "payload member hash:" + relative)
    root_raw, root = parse_manifest(chain_dir / "root_manifest.sha256")
    chain_rel = chain_dir.relative_to(WORKSPACE).as_posix()
    need(root == {chain_rel + "/payload_manifest.sha256":
                  hashlib.sha256(payload_raw).hexdigest(),
                  C30B_MANIFEST_REL: C30B_MANIFEST_SHA256}, "exact two-member root")
    receipt = strict_object(chain_dir / "manifest_receipt.json", "manifest receipt")
    need(receipt.get("status") == "PASS_PAYLOAD_AND_ROOT_MANIFESTS__ZERO_FORMAL_CREDIT"
         and receipt.get("payload_manifest_sha256") == hashlib.sha256(payload_raw).hexdigest()
         and receipt.get("payload_member_count") == len(payload)
         and receipt.get("root_manifest_sha256") == hashlib.sha256(root_raw).hexdigest()
         and receipt.get("round306c30b_manifest_sha256") == C30B_MANIFEST_SHA256
         and receipt.get("formal_credit") == 0
         and receipt.get("source_W_transition_authorized") is False,
         "manifest receipt conclusion")
    return {"payload": hashlib.sha256(payload_raw).hexdigest(),
            "root": hashlib.sha256(root_raw).hexdigest()}


def bundle_source(name: str) -> Path:
    if name.startswith("transaction/run/"):
        return RUN / name.removeprefix("transaction/run/")
    if name.startswith("transaction/receipt/"):
        return RECEIPT / name.removeprefix("transaction/receipt/")
    if name.startswith("bridge/"):
        return BRIDGE / name.removeprefix("bridge/")
    raise Blocked("unknown bundle source:" + name)


def verify_bundle(chain_dir: Path) -> dict[str, Any]:
    receipt = strict_object(chain_dir / "evidence_bundle_receipt.json", "bundle receipt")
    entries = receipt.get("entries")
    need(type(entries) is dict and receipt.get("status") ==
         "PASS_EXACT_V3_TRANSACTION_AND_BRIDGE_EVIDENCE_BUNDLED__ZERO_FORMAL_CREDIT"
         and receipt.get("formal_credit") == 0
         and receipt.get("source_W_transition_authorized") is False,
         "bundle receipt boundary")
    bundle = chain_dir / "c30c_v3_audit_evidence.tar.gz"
    need(receipt.get("bundle_sha256") == sha(bundle), "bundle outer hash")
    expected_manifest = b"".join(
        (entries[name]["sha256"] + "  " + name + "\n").encode("ascii")
        for name in sorted(entries)
    )
    observed: set[str] = set()
    with tarfile.open(bundle, mode="r:gz") as archive:
        members = archive.getmembers()
        need({item.name for item in members} == {"MANIFEST.sha256", *entries},
             "bundle exact member names")
        need(len(members) == len(entries) + 1, "bundle unique member count")
        for member in members:
            need(member.isfile() and member.uid == 0 and member.gid == 0 and
                 member.mtime == 0 and member.mode == 0o400 and
                 member.name not in observed, "deterministic safe tar member:" + member.name)
            observed.add(member.name)
            stream = archive.extractfile(member)
            need(stream is not None, "tar member stream:" + member.name)
            state = hashlib.sha256()
            total = 0
            chunks: list[bytes] = [] if member.name == "MANIFEST.sha256" else []
            while block := stream.read(4 << 20):
                state.update(block)
                total += len(block)
                if member.name == "MANIFEST.sha256":
                    chunks.append(block)
            if member.name == "MANIFEST.sha256":
                need(b"".join(chunks) == expected_manifest, "bundle internal manifest")
            else:
                meta = entries.get(member.name)
                need(type(meta) is dict and meta.get("sha256") == state.hexdigest()
                     and meta.get("size") == total == member.size,
                     "bundle entry receipt:" + member.name)
                source_hash, source_size = hash_size(bundle_source(member.name))
                need(source_hash == state.hexdigest() and source_size == total,
                     "bundle source byte identity:" + member.name)
    return {"bundle_sha256": sha(bundle), "bundle_entry_count": len(entries)}


def validate_transaction_and_bridge() -> dict[str, Any]:
    need(sha(VALIDATOR) == VALIDATOR_SHA256, "pinned v3 validator")
    receipt_raw = capture(RECEIPT / "receipt.json", 4 << 20)
    receipt = strict_object_raw(receipt_raw, "v3 transaction receipt")
    need(receipt.get("schema") == "cm2.round306c30c.attack-run-receipt-validation.v3"
         and receipt.get("status") ==
         "PASS_COMPLETE_C30C_62_ATTACK_RUN_RECEIPT_V3__ZERO_FORMAL_CREDIT"
         and receipt.get("validator_sha256") == VALIDATOR_SHA256
         and receipt.get("attack_count") == 62
         and receipt.get("numeric_exit_code") == 0 and receipt.get("signal") is None
         and receipt.get("formal_credit") == 0
         and receipt.get("source_W_formal_remainder") == 80
         and receipt.get("source_W_transition_authorized") is False,
         "v3 transaction receipt conclusion")
    replay = subprocess.run(["/usr/bin/python3", "-I", "-B", os.fspath(VALIDATOR),
                             os.fspath(RUN)], cwd=WORKSPACE,
                            env={"HOME": "/nonexistent", "LC_ALL": "C.UTF-8", "TZ": "UTC"},
                            stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, check=False)
    need(replay.returncode == 0 and replay.stderr == b"" and replay.stdout == receipt_raw,
         "byte-identical v3 validator replay")
    terminal = strict_object(BRIDGE / "terminal_status.json", "bridge terminal")
    need(terminal.get("status") ==
         "PASS_ZERO_CREDIT_THROUGH_DUAL_AND_COLD__BLOCKED_BEFORE_PUBLICATION"
         and terminal.get("terminal_replay_completed") is False
         and terminal.get("formal_credit") == 0
         and terminal.get("source_W_formal_remainder") == 80
         and terminal.get("source_W_transition_authorized") is False,
         "bridge exact terminal boundary")
    bindings = {"receipt_gate_sha256": "receipt_gate.json",
                "dual_checker_receipt_sha256": "dual_checker_receipt.json",
                "cold_replay_receipt_sha256": "cold_replay_receipt.json",
                "downstream_inventory_sha256": "downstream_inventory.json"}
    for key, name in bindings.items():
        need(terminal.get(key) == sha(BRIDGE / name), "bridge receipt binding:" + name)
    dual = strict_object(BRIDGE / "dual_checker_receipt.json", "dual receipt")
    cold = strict_object(BRIDGE / "cold_replay_receipt.json", "cold receipt")
    need(dual.get("status") == "PASS_FRESH_DUAL_CONTROLLED_SEED_CHECKER__ZERO_FORMAL_CREDIT"
         and dual.get("seeds") == ["30630071", "30630929"]
         and dual.get("candidate_result_sha256") == RESULT_OBJECT_SHA256
         and dual.get("formal_credit") == 0
         and dual.get("source_W_transition_authorized") is False,
         "dual receipt exact conclusion")
    need(cold.get("status") == "PASS_FRESH_FULL_TRACE_COLD_REPLAY__ZERO_FORMAL_CREDIT"
         and cold.get("formal_credit") == 0
         and cold.get("source_W_transition_authorized") is False,
         "cold receipt exact conclusion")
    for seed in ("30630071", "30630929"):
        stdout = BRIDGE / ("dual-seed-" + seed) / "stdout.json"
        need(dual.get("stdout_sha256", {}).get(seed) == sha(stdout),
             "dual stdout receipt:" + seed)
    need(cold.get("trace_sha256") == sha(BRIDGE / "cold-seed-30630071/trace.raw")
         and cold.get("checker_stdout_sha256") ==
         sha(BRIDGE / "cold-seed-30630071/stdout.json")
         and cold.get("trace_audit_sha256") ==
         sha(BRIDGE / "cold-seed-30630071/trace_audit.json")
         and cold.get("pairing_gate_sha256") ==
         sha(BRIDGE / "cold-seed-30630071/pairing_gate.json"),
         "cold receipt byte bindings")
    return {"transaction_receipt_sha256": hashlib.sha256(receipt_raw).hexdigest(),
            "bridge_terminal_sha256": sha(BRIDGE / "terminal_status.json")}


def validate_ledger(path: Path, expected_rows: int) -> None:
    count = 0
    row_hashes: set[str] = set()
    try:
        with gzip.open(path, "rb") as stream:
            for raw in stream:
                value = strict_object_raw(raw, "ledger row:" + path.name)
                canonical_row = canonical(value) + b"\n"
                need(raw == canonical_row, "canonical ledger row:" + path.name)
                row_hash = hashlib.sha256(canonical_row).hexdigest()
                need(row_hash not in row_hashes, "unique ledger rows:" + path.name)
                row_hashes.add(row_hash)
                count += 1
    except (gzip.BadGzipFile, EOFError) as error:
        raise Blocked("complete gzip:" + path.name) from error
    need(count == expected_rows, "ledger row count:" + path.name)


def validate_candidates() -> dict[str, Any]:
    bases = [WORKSPACE / ".cm2-runtime/candidates" / ("c30c-v4-seed-" + seed)
             for seed in ("30630071", "30630929")]
    for name, expected in CANDIDATE_HASHES.items():
        first = capture(bases[0] / name)
        second = capture(bases[1] / name)
        need(first == second and hashlib.sha256(first).hexdigest() == expected,
             "dual candidate byte identity:" + name)
    for name, rows in LEDGER_ROWS.items():
        validate_ledger(bases[0] / name, rows)
    result_raw = capture(bases[0] / (PREFIX + "_result.json"), 16 << 20)
    result = strict_object_raw(result_raw, "candidate result")
    body = dict(result)
    closure = body.pop("result_sha256", None)
    need(closure == RESULT_OBJECT_SHA256 == hashlib.sha256(canonical(body)).hexdigest(),
         "candidate result object closure")
    transition = result.get("proposed_source_W_ledger_transition_if_independently_verified", {})
    credit = result.get("candidate_credit_if_independently_verified", {})
    theorem = result.get("candidate_theorem", {})
    need(result.get("formal_credit") == {"combined_Delta_H_cell_dispositions": 0,
                                         "resolved_nonexcluded": 0,
                                         "resolved_source_W_origin_dispositions": 0,
                                         "whole_source_W_origin_exclusions": 0}
         and transition.get("before", {}).get("remaining") == 80
         and transition.get("after", {}).get("remaining") == 78
         and transition.get("candidate_credits") == {"resolved_nonexcluded": 2,
                                                      "resolved_origin_disposition": 2,
                                                      "whole_origin_exclusion": 0}
         and transition.get("official_ledger_mutated") is False
         and credit.get("resolved_source_W_origin_dispositions") == 2
         and credit.get("whole_source_W_origin_exclusions") == 0
         and theorem.get("both_whole_origins_are_resolved_mixed") is True
         and theorem.get("child_count_or_volume_used_as_whole_origin_credit") is False,
         "exact C30c mathematical result")
    return {"candidate_result_file_sha256": hashlib.sha256(result_raw).hexdigest(),
            "candidate_result_object_sha256": RESULT_OBJECT_SHA256,
            "ledger_row_counts": LEDGER_ROWS}


def fresh_verifier() -> dict[str, Any]:
    need(sha(VERIFIER) == VERIFIER_SHA256, "pinned independent verifier")
    expected_raw = capture(BRIDGE / "dual-seed-30630071/stdout.json", 64 << 20)
    need(expected_raw == capture(BRIDGE / "dual-seed-30630929/stdout.json", 64 << 20),
         "dual verifier byte identity")
    expected = strict_object_raw(expected_raw, "bridge verifier output")
    need(expected.get("status") == VERIFIER_STATUS
         and expected.get("candidate_result_sha256") == RESULT_OBJECT_SHA256
         and expected.get("proposed_source_W_remaining_transition") == "80->78"
         and expected.get("formal_credit") == 0
         and expected.get("manifest_authorized") is False,
         "bridge verifier mathematical conclusion")
    completed = subprocess.run(
        [os.fspath(PYTHON), "-I", "-B", os.fspath(VERIFIER),
         os.fspath(WORKSPACE / ".cm2-runtime/candidates/c30c-v4-seed-30630071")],
        cwd=WORKSPACE,
        env={"HOME": "/nonexistent", "LC_ALL": "C.UTF-8", "TZ": "UTC",
             "PATH": "/usr/bin:/bin", "PYTHONDONTWRITEBYTECODE": "1"},
        stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        check=False,
    )
    need(completed.returncode == 0 and completed.stderr == b"",
         "fresh outer verifier execution")
    fresh = strict_object_raw(completed.stdout, "fresh outer verifier")
    need(canonical(fresh) == canonical(expected), "fresh outer verifier result identity")
    return {"fresh_verifier_stdout_sha256": hashlib.sha256(completed.stdout).hexdigest(),
            "independent_verifier_sha256": VERIFIER_SHA256}


def run(chain_dir: Path) -> dict[str, Any]:
    first = verify_manifests(chain_dir)
    bundle = verify_bundle(chain_dir)
    bridge = validate_transaction_and_bridge()
    candidates = validate_candidates()
    replay = fresh_verifier()
    second = verify_manifests(chain_dir)
    need(first == second, "manifest graph stable across independent replay")
    return {
        "schema": "cm2.round306c30c.v3-formal-handoff-outer-verification.v1",
        "status": "PASS_INDEPENDENT_OUTER_MATHEMATICAL_CHECK__CONDITIONAL_80_TO_78",
        "round306c30b_authority": {
            "manifest_sha256": C30B_MANIFEST_SHA256,
            "verification_sha256": C30B_VERIFICATION_SHA256,
            "formal_source_W_remaining": 80,
        },
        "manifests": {"payload_manifest_sha256": first["payload"],
                      "root_manifest_sha256": first["root"]},
        "evidence": {**bundle, **bridge},
        "mathematics": {**candidates, **replay,
                        "whole_origin_dispositions": {"RESOLVED_MIXED": 2,
                                                       "EXCLUDED": 0}},
        "formal_handoff": {"before": {"remaining": 80},
                           "conditional_after": {"remaining": 78},
                           "resolved_nonexcluded_credit": 2,
                           "whole_origin_exclusion_credit": 0},
        "terminal_replay_required": True,
        "formal_credit": 0,
        "source_W_formal_remainder": 80,
        "source_W_transition_authorized": False,
        "D02": "BLOCKED_COMPOSITE",
        "D03": "UNAUTHORIZED",
        "D04": "NOT_MINTED",
        "CM2": "NO-GO_FOR_CLAIM",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--chain-dir", required=True, type=Path)
    arguments = parser.parse_args()
    try:
        output = run(arguments.chain_dir.resolve(strict=True))
    except (Blocked, OSError, ValueError, TypeError, KeyError,
            subprocess.SubprocessError, tarfile.TarError) as error:
        print(canonical({"schema": "cm2.round306c30c.v3-formal-handoff-outer-verification.v1",
                         "status": "BLOCKED_FAIL_CLOSED", "error": str(error),
                         "formal_credit": 0, "source_W_formal_remainder": 80,
                         "source_W_transition_authorized": False,
                         "CM2": "NO-GO_FOR_CLAIM"}).decode("ascii"))
        return 1
    print(canonical(output).decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
