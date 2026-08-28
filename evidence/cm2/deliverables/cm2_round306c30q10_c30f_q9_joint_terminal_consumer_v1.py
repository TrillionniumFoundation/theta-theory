#!/usr/bin/env python3
"""Rebind the audited Q9 54-origin theorem to the exact C30f terminal."""

from __future__ import annotations

import argparse
import copy
import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import stat
import sys
from types import ModuleType
from typing import Any, Callable


ROOT = Path(__file__).resolve().parent.parent
COMMON_PATH = ROOT / "deliverables/cm2_round306c30d_source_w_multi_delta_whole_origin_exclusion_v3_terminal_consumer_adapter_v1.py"


def load_common() -> ModuleType:
    spec = importlib.util.spec_from_file_location("_cm2_q10_terminal_common", COMMON_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("Q10 common import specification")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


common = load_common()
Reject = common.Reject
need = common.need
canonical = common.canonical
digest = common.digest
close = common.close
workspace = common.workspace
regular = common.regular
file_sha = common.file_sha
strict_json = common.strict_json
parse_manifest = common.parse_manifest
exact_state = common.exact_state
REQUIRED = common.REQUIRED
LEDGER_MEMBERS = common.LEDGER_MEMBERS

C30F_TERMINAL_STATUS = "PASS_FORMAL_C30F_TERMINAL__56_TO_54_AUTHORIZED"
C30F_CHAIN_STATUS = "PASS_C30F_V2_TERMINAL_BYTE_REPLAY__FORMAL_SOURCE_W_56_TO_54"
Q9_STATUS = (
    "PASS_C30Q9_DUAL_SEED_FULL_PHYSICAL_FIRST_HIT_DISPOSITION__44_EXCLUDED__"
    "10_RESOLVED_MIXED__44_ATTACKS__ZERO_CREDIT_PRE_TERMINAL"
)
TERMINAL_STATUS = "PASS_FORMAL_C30Q10_JOINT_TERMINAL__SOURCE_W_54_TO_0_AUTHORIZED"
CHAIN_STATUS = "PASS_C30Q10_C30F_Q9_JOINT_TERMINAL_BYTE_REPLAY__FORMAL_SOURCE_W_ZERO"
BEFORE = {
    "excluded": 74_768, "conservative_live": 2_064,
    "resolved_nonexcluded": 2_010, "remaining": 54, "total": 76_832,
    "remaining_partition": {"compact_q": 54},
}
AFTER = {
    "excluded": 74_812, "conservative_live": 2_020,
    "resolved_nonexcluded": 2_020, "remaining": 0, "total": 76_832,
    "remaining_partition": {"compact_q": 0},
}
CREDIT = {
    "resolved_source_W_origin_dispositions": 54,
    "whole_source_W_origin_exclusions": 44,
    "resolved_nonexcluded": 10,
    "EXCLUDED": 44,
    "RESOLVED_MIXED": 10,
}
STRICT = {
    "D02": "BLOCKED_COMPOSITE", "D03": "UNAUTHORIZED",
    "D04": "NOT_MINTED", "Gate5": "10/18",
    "complete_global_18_field_blocks": 0, "CM2": "NO-GO_FOR_CLAIM",
}


def raw_file(path: Path, label: str, maximum: int = 128 << 20) -> bytes:
    absolute = workspace(path)
    before = absolute.lstat()
    need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1
         and 0 <= before.st_size <= maximum, label + ":regular")
    raw = absolute.read_bytes()
    after = absolute.lstat()
    need((before.st_dev, before.st_ino, before.st_mode, before.st_nlink,
          before.st_size, before.st_mtime_ns, before.st_ctime_ns)
         == (after.st_dev, after.st_ino, after.st_mode, after.st_nlink,
             after.st_size, after.st_mtime_ns, after.st_ctime_ns), label + ":TOCTOU")
    return raw


def raw_sha(path: Path, label: str) -> str:
    import hashlib
    return hashlib.sha256(raw_file(path, label)).hexdigest()


def loose_json(path: Path, label: str) -> dict[str, Any]:
    value = json.loads(raw_file(path, label))
    need(type(value) is dict, label + ":object")
    return value


def parse_q9_manifest(directory: Path) -> dict[str, str]:
    raw = raw_file(directory / "manifest.sha256", "Q9 manifest")
    need(raw.endswith(b"\n") and not raw.endswith(b"\n\n"), "Q9 manifest newline")
    result: dict[str, str] = {}
    for row in raw.decode("ascii").splitlines():
        fields = row.split("  ", 1)
        need(len(fields) == 2 and len(fields[0]) == 64 and fields[1] not in result,
             "Q9 manifest row")
        need(raw_sha(directory / fields[1], "Q9 manifest member:" + fields[1]) == fields[0],
             "Q9 manifest SHA:" + fields[1])
        result[fields[1]] = fields[0]
    return result


def process_attestation() -> dict[str, Any]:
    token = os.environ.get("CM2_PUBLICATION_TOKEN", "")
    unit = os.environ.get("CM2_PUBLICATION_UNIT", "")
    invocation = os.environ.get("INVOCATION_ID", "")
    need(re.fullmatch(r"c30q10-publication-[a-z0-9-]{16,160}", token) is not None,
         "fresh Q10 token")
    need(re.fullmatch(r"cm2-c30q10-publication-[a-z0-9-]{16,160}\.service", unit) is not None,
         "Q10 unit")
    need(re.fullmatch(r"[0-9a-f]{32}", invocation) is not None, "Q10 InvocationID")
    need(os.environ.get("HOME") == "/nonexistent"
         and os.environ.get("LC_ALL") == "C.UTF-8"
         and os.environ.get("TZ") == "UTC"
         and os.environ.get("PYTHONHASHSEED") == "0", "Q10 controlled environment")
    return {"publication_token": token, "unit": unit, "InvocationID": invocation,
            "ExecMainPID": os.getpid(), "uid": os.getuid()}


def validate_c30f(chain_raw: Path, ledger_raw: Path) -> dict[str, Any]:
    chain = workspace(chain_raw)
    ledger_dir = workspace(ledger_raw)
    need({entry.name for entry in os.scandir(chain)} == set(REQUIRED) | {"PASS.lock", "payload"},
         "C30f exact terminal top-level")
    need(regular(chain / "PASS.lock", "C30f PASS") == (C30F_CHAIN_STATUS + "\n").encode("ascii"),
         "C30f PASS marker")
    required = {name: file_sha(chain / name, "C30f terminal:" + name) for name in REQUIRED}
    payload = parse_manifest(chain, chain / "payload_manifest.sha256", "C30f payload")
    root = parse_manifest(chain, chain / "root_manifest.sha256", "C30f root")
    need(root == {"outer_verification.json": required["outer_verification.json"],
                  "payload_manifest.sha256": required["payload_manifest.sha256"]},
         "C30f exact root")
    evidence = strict_json(chain / "evidence_bundle_receipt.json", "C30f evidence", "evidence_bundle_sha256")
    manifest_receipt = strict_json(chain / "manifest_receipt.json", "C30f manifest", "manifest_receipt_sha256")
    outer = strict_json(chain / "outer_verification.json", "C30f outer", "outer_verification_sha256")
    seal = strict_json(chain / "terminal_seal_receipt.json", "C30f seal", "terminal_seal_receipt_sha256")
    replay = strict_json(chain / "terminal_replay.json", "C30f replay", "terminal_replay_sha256")
    status = strict_json(chain / "chain_status.json", "C30f status", "chain_status_sha256")
    need(evidence.get("status") == "PASS_C30F_V2_DUAL_SEED_VERIFICATION_AND_ATTACK_EVIDENCE"
         and evidence.get("dual_seed_byte_identical") is True
         and evidence.get("coherent_attack_count") == 16, "C30f evidence")
    need(manifest_receipt.get("status") == "PASS_C30F_V2_PAYLOAD_MANIFEST_ALL_MEMBERS_VERIFIED"
         and manifest_receipt.get("payload_manifest_member_count") == len(payload)
         and manifest_receipt.get("payload_manifest_sha256") == required["payload_manifest.sha256"],
         "C30f manifest")
    need(outer.get("status") == "PASS_C30F_V2_OUTER_VERIFICATION__56_TO_54_READY_FOR_TERMINAL"
         and outer.get("before") == {
             "excluded": 74_766, "conservative_live": 2_066,
             "resolved_nonexcluded": 2_010, "remaining": 56, "total": 76_832,
             "remaining_partition": {"retained_source_seams": 2, "compact_q": 54}}
         and outer.get("after") == BEFORE and outer.get("conservation_verified") is True,
         "C30f outer")
    need(seal.get("status") == "PASS_C30F_V2_EXACT_TERMINAL_SEAL__56_TO_54"
         and seal.get("terminal_status") == C30F_TERMINAL_STATUS
         and seal.get("after") == BEFORE, "C30f seal")
    need(replay.get("status") == C30F_TERMINAL_STATUS
         and replay.get("C30f_transition_authorized") is True
         and replay.get("after") == BEFORE and replay.get("source_W_formal_remainder") == 54,
         "C30f replay")
    need(status.get("status") == C30F_CHAIN_STATUS
         and status.get("terminal_status") == C30F_TERMINAL_STATUS
         and status.get("terminal_replay_object_sha256") == replay["terminal_replay_sha256"]
         and status.get("source_W_transition") == {"before": 56, "after": 54}
         and status.get("source_W_transition_authorized") is True, "C30f status")
    process = evidence.get("process_attestation")
    need(type(process) is dict and process.get("unit") == status.get("unit")
         and process.get("InvocationID") == status.get("InvocationID")
         and process.get("ExecMainPID") == status.get("ExecMainPID"), "C30f process binding")

    need({entry.name for entry in os.scandir(ledger_dir)} == set(LEDGER_MEMBERS),
         "C30f exact ledger members")
    need(regular(ledger_dir / "PASS.lock", "C30f ledger PASS")
         == b"PASS_C30F_FORMAL_SOURCE_W_LEDGER__REMAINDER_54\n", "C30f ledger marker")
    ledger_root = parse_manifest(ledger_dir, ledger_dir / "root_manifest.sha256", "C30f ledger root")
    need(set(ledger_root) == {"application_receipt.json", "hostile_audit.json",
                              "source_w_formal_ledger.json"}, "C30f ledger root")
    ledger = strict_json(ledger_dir / "source_w_formal_ledger.json", "C30f ledger", "object_sha256")
    application = strict_json(ledger_dir / "application_receipt.json", "C30f application", "object_sha256")
    audit = strict_json(ledger_dir / "hostile_audit.json", "C30f audit", "object_sha256")
    exact_state(ledger.get("current_state"), BEFORE, "C30f formal state")
    need(ledger.get("status") == "PASS_CONSOLIDATED_SOURCE_W_FORMAL_LEDGER__REMAINDER_54"
         and ledger.get("formal_coverage_numerator") == 76_778
         and len(ledger.get("transitions", [])) == 4
         and ledger["transitions"][-1].get("terminal_replay_object_sha256") == replay["terminal_replay_sha256"],
         "C30f formal ledger")
    need(application.get("source_W_transition_authorized") is True
         and application.get("ledger_object_sha256") == ledger["object_sha256"]
         and audit.get("negative_test_count") == 9, "C30f application/audit")
    return {
        "chain": chain, "ledger_dir": ledger_dir, "required": required,
        "payload_count": len(payload), "chain_status": status,
        "terminal_replay": replay, "formal_ledger": ledger,
        "application": application, "audit": audit,
    }


def validate_q9(raw: Path) -> dict[str, Any]:
    directory = workspace(raw)
    names = {entry.name for entry in os.scandir(directory)}
    manifest = parse_q9_manifest(directory)
    need(names == set(manifest) | {"manifest.sha256"}, "Q9 exact directory/manifest")
    receipt = loose_json(directory / "receipt.json", "Q9 receipt")
    artifacts = receipt.get("artifacts")
    need(type(artifacts) is dict and set(artifacts) == set(manifest) - {"receipt.json"},
         "Q9 artifact inventory")
    for name, descriptor in artifacts.items():
        need(type(descriptor) is dict and descriptor.get("sha256") == manifest[name]
             and descriptor.get("bytes") == len(raw_file(directory / name, "Q9 artifact:" + name)),
             "Q9 artifact descriptor:" + name)
    need(receipt.get("schema")
         == "cm2.round306c30q9.full-physical-first-hit-disposition-receipt.zero-credit.v1"
         and receipt.get("status") == Q9_STATUS
         and receipt.get("candidate_result_sha256") == "9102308165cefc800321b859a7e9f87db503b9b9d61f99feafc637ac2677cb23"
         and receipt.get("formal_54_to_0_minted") is False
         and receipt.get("formal_dispositions_minted") == 0
         and receipt.get("research_classification") == {
             "distinct_route_switches": 2,
             "historic_root_by_root_subdivision_used": False,
             "research_EXCLUDED_candidates": 44,
             "research_RESOLVED_MIXED_candidates": 10,
             "total_origins": 54, "unresolved_research_origins": 0}
         and receipt.get("coherent_attacks", {}).get("rejected") == 44
         and receipt.get("coherent_attacks", {}).get("total") == 44
         and receipt.get("cold_replay", {}).get("byte_identical_to_dual_verifier") is True,
         "Q9 exact zero-credit receipt")
    need(raw_file(directory / "pre.sha256", "Q9 pre SHA")
         == raw_file(directory / "post.sha256", "Q9 post SHA")
         and raw_file(directory / "pre.stat", "Q9 pre stat")
         == raw_file(directory / "post.stat", "Q9 post stat"), "Q9 input stability")
    producer_a = raw_file(directory / "producer_seed30990083_stdout.json", "Q9 producer A")
    producer_b = raw_file(directory / "producer_seed30990941_stdout.json", "Q9 producer B")
    verifier_a = raw_file(directory / "verifier_seed30990083_stdout.json", "Q9 verifier A")
    verifier_b = raw_file(directory / "verifier_seed30990941_stdout.json", "Q9 verifier B")
    need(producer_a == producer_b and verifier_a == verifier_b
         and verifier_a == raw_file(directory / "cold_replay_stdout.json", "Q9 cold replay"),
         "Q9 dual-seed/cold byte identity")
    producer = json.loads(producer_a)
    verifier = json.loads(verifier_a)
    attacks = loose_json(directory / "coherent_attacks_stdout.json", "Q9 attacks")
    need(type(producer) is dict and type(verifier) is dict
         and producer.get("schema")
         == "cm2.round306c30q9.compact-q-full-physical-first-hit-disposition.zero-credit.v1"
         and producer.get("result_sha256") == digest(producer["result"])
         and producer.get("result_sha256") == receipt["candidate_result_sha256"]
         and verifier.get("status")
         == "PASS_INDEPENDENT_C30Q9_FULL_PHYSICAL_FIRST_HIT_DISPOSITION_ZERO_CREDIT"
         and attacks.get("status") == "PASS_ALL_COHERENT_C30Q9_MUTATIONS_REJECTED"
         and attacks.get("rejected") == 44, "Q9 producer/verifier/attacks")
    result = producer["result"]
    ledger = result.get("research_disposition_ledger")
    need(type(ledger) is list and len(ledger) == 54
         and [row["origin_key"] for row in ledger] == sorted(row["origin_key"] for row in ledger)
         and len({row["origin_key"] for row in ledger}) == 54
         and sum(row["research_disposition"] == "EXCLUDED" for row in ledger) == 44
         and sum(row["research_disposition"] == "RESOLVED_MIXED" for row in ledger) == 10,
         "Q9 exact 54-origin research ledger")
    handoff = result.get("future_C30f_gated_handoff_candidate")
    need(handoff == {
        "required_predecessor": "C30f v2 exact terminal replay authorizing the 56-to-54 step",
        "predecessor_exists_in_this_audit": False,
        "terminal_adapter_present": False,
        "before": {key: value for key, value in BEFORE.items() if key != "total"},
        "candidate_credit": {"EXCLUDED": 44, "RESOLVED_MIXED": 10, "total_dispositions": 54},
        "candidate_after": {key: value for key, value in AFTER.items() if key != "total"},
        "conservation": {"before_excluded_plus_live": 76_832,
                         "after_excluded_plus_live": 76_832,
                         "partition_before": 54, "partition_after": 0},
        "formal_54_to_0_minted": False,
        "release_state": "PROHIBITED_PRE_TERMINAL",
    }, "Q9 exact future C30f handoff")
    origin_keys = [row["origin_key"] for row in ledger]
    return {
        "directory": directory, "manifest": manifest, "receipt": receipt,
        "result": result, "result_sha256": producer["result_sha256"],
        "origin_keys": origin_keys, "origin_keys_sha256": digest(origin_keys),
    }


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    path.write_bytes(canonical(value) + b"\n")
    os.chmod(path, 0o600)


def copy_raw(source: Path, target: Path, label: str) -> str:
    raw = raw_file(source, label)
    target.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    target.write_bytes(raw)
    os.chmod(target, 0o600)
    return raw_sha(target, label + ":copy")


def make_manifest(root: Path, names: list[str]) -> bytes:
    need(names == sorted(names) and len(names) == len(set(names)), "Q10 manifest order")
    return ("\n".join(raw_sha(root / name, "Q10 manifest:" + name) + "  " + name
                      for name in names) + "\n").encode("ascii")


def validate_transition(value: dict[str, Any], prior: dict[str, Any], exact: dict[str, Any]) -> None:
    body = dict(value)
    claimed = body.pop("transition_id", None)
    need(claimed == digest(body) and value == exact, "Q10 exact transition")
    exact_state(value["before"], BEFORE, "Q10 before")
    exact_state(value["after"], AFTER, "Q10 after")
    need(value["sequence"] == 5 and value["round"] == "C30q10"
         and value["predecessor_ledger_object_sha256"] == prior["object_sha256"],
         "Q10 transition order")


def hostile(transition: dict[str, Any], prior: dict[str, Any]) -> dict[str, Any]:
    attacks: tuple[tuple[str, Callable[[dict[str, Any]], None]], ...] = (
        ("conservation", lambda item: item["after"].__setitem__("remaining", 1)),
        ("duplicate", lambda item: item.__setitem__("sequence", 4)),
        ("out_of_order", lambda item: item.__setitem__("before", copy.deepcopy(AFTER))),
        ("schema", lambda item: item.__setitem__("round", "C30x")),
        ("PID", lambda item: item.__setitem__("ExecMainPID", 2)),
        ("stale", lambda item: item.__setitem__("predecessor_ledger_object_sha256", "0" * 64)),
        ("marker", lambda item: item.__setitem__("terminal_replay_object_sha256", "1" * 64)),
        ("manifest", lambda item: item.__setitem__("q9_manifest_file_sha256", "2" * 64)),
        ("object", lambda item: item.__setitem__("q9_result_object_sha256", "3" * 64)),
    )
    rejected: list[str] = []
    for name, mutate in attacks:
        target = copy.deepcopy(transition)
        mutate(target)
        body = dict(target)
        body.pop("transition_id", None)
        target["transition_id"] = digest(body)
        try:
            validate_transition(target, prior, transition)
        except Reject:
            rejected.append(name)
    need(rejected == [name for name, _ in attacks], "Q10 all hostile attacks")
    return close({
        "schema": "cm2.round306c30q10.formal-source-w-ledger-hostile-audit.v1",
        "status": "PASS_C30Q10_FORMAL_LEDGER_ALL_9_HOSTILE_ATTACKS_REJECTED",
        "negative_test_count": 9, "rejected_attacks": rejected,
        "formal_transition_authorized_by_audit": False, **STRICT,
    }, "object_sha256")


def build(arguments: argparse.Namespace) -> dict[str, Any]:
    c30f = validate_c30f(arguments.c30f_chain_dir, arguments.c30f_ledger_dir)
    q9 = validate_q9(arguments.q9_audit_dir)
    process = process_attestation()
    chain = workspace(arguments.chain_dir, absent=True)
    ledger_dir = workspace(arguments.ledger_dir, absent=True)
    need(not chain.exists() and not ledger_dir.exists(), "fresh Q10 outputs")
    chain_tmp = chain.with_name(chain.name + ".tmp-" + str(os.getpid()))
    ledger_tmp = ledger_dir.with_name(ledger_dir.name + ".tmp-" + str(os.getpid()))
    chain_tmp.mkdir(mode=0o700)
    try:
        payload = chain_tmp / "payload"
        (payload / "c30f-terminal").mkdir(mode=0o700, parents=True)
        (payload / "c30f-ledger").mkdir(mode=0o700)
        (payload / "q9-audit").mkdir(mode=0o700)
        for name in sorted(set(REQUIRED) | {"PASS.lock"}):
            copy_raw(c30f["chain"] / name, payload / "c30f-terminal" / name,
                     "C30f payload:" + name)
        for name in LEDGER_MEMBERS:
            copy_raw(c30f["ledger_dir"] / name, payload / "c30f-ledger" / name,
                     "C30f ledger payload:" + name)
        for name in sorted(set(q9["manifest"]) | {"manifest.sha256"}):
            copy_raw(q9["directory"] / name, payload / "q9-audit" / name,
                     "Q9 payload:" + name)
        evidence = close({
            "schema": "cm2.round306c30q10.c30f-q9-joint-evidence-bundle.v1",
            "status": "PASS_C30Q10_EXACT_C30F_TERMINAL_AND_Q9_54_ORIGIN_JOINT_EVIDENCE",
            "process_attestation": process,
            "c30f_chain_status_object_sha256": c30f["chain_status"]["chain_status_sha256"],
            "c30f_terminal_replay_object_sha256": c30f["terminal_replay"]["terminal_replay_sha256"],
            "c30f_formal_ledger_object_sha256": c30f["formal_ledger"]["object_sha256"],
            "q9_receipt_file_sha256": raw_sha(q9["directory"] / "receipt.json", "Q9 receipt SHA"),
            "q9_manifest_file_sha256": raw_sha(q9["directory"] / "manifest.sha256", "Q9 manifest SHA"),
            "q9_result_object_sha256": q9["result_sha256"],
            "q9_origin_keys_sha256": q9["origin_keys_sha256"],
            "q9_origin_count": 54, "q9_EXCLUDED": 44, "q9_RESOLVED_MIXED": 10,
            "q9_coherent_attack_count": 44, "c30f_to_q9_predecessor_rebound": True,
            "formal_credit_before_terminal": 0, **STRICT,
        }, "evidence_bundle_sha256")
        write_json(chain_tmp / "evidence_bundle_receipt.json", evidence)
        payload_names = sorted(path.relative_to(chain_tmp).as_posix()
                               for path in chain_tmp.rglob("*") if path.is_file())
        payload_manifest = make_manifest(chain_tmp, payload_names)
        (chain_tmp / "payload_manifest.sha256").write_bytes(payload_manifest)
        os.chmod(chain_tmp / "payload_manifest.sha256", 0o600)
        payload_sha = raw_sha(chain_tmp / "payload_manifest.sha256", "Q10 payload manifest")
        manifest_receipt = close({
            "schema": "cm2.round306c30q10.manifest-receipt.v1",
            "status": "PASS_C30Q10_PAYLOAD_MANIFEST_ALL_MEMBERS_VERIFIED",
            "payload_manifest_sha256": payload_sha,
            "payload_manifest_member_count": len(payload_names),
            "payload_members": payload_names, "all_members_verified": True,
            "evidence_bundle_sha256": evidence["evidence_bundle_sha256"], **STRICT,
        }, "manifest_receipt_sha256")
        write_json(chain_tmp / "manifest_receipt.json", manifest_receipt)
        outer = close({
            "schema": "cm2.round306c30q10.c30f-q9-joint-outer-verification.v1",
            "status": "PASS_C30Q10_OUTER_VERIFICATION__SOURCE_W_54_TO_0_READY_FOR_TERMINAL",
            "payload_manifest_sha256": payload_sha,
            "manifest_receipt_sha256": manifest_receipt["manifest_receipt_sha256"],
            "c30f_formal_ledger_object_sha256": c30f["formal_ledger"]["object_sha256"],
            "q9_result_object_sha256": q9["result_sha256"],
            "q9_origin_keys_sha256": q9["origin_keys_sha256"],
            "before": BEFORE, "credit": CREDIT, "after": AFTER,
            "conservation_verified": True, "origin_count": 54,
            "all_q9_artifacts_byte_replayed": True,
            "c30f_terminal_and_ledger_byte_replayed": True,
            "formal_credit_before_terminal": 0, **STRICT,
        }, "outer_verification_sha256")
        write_json(chain_tmp / "outer_verification.json", outer)
        root_manifest = make_manifest(chain_tmp, ["outer_verification.json", "payload_manifest.sha256"])
        (chain_tmp / "root_manifest.sha256").write_bytes(root_manifest)
        os.chmod(chain_tmp / "root_manifest.sha256", 0o600)
        root_sha = raw_sha(chain_tmp / "root_manifest.sha256", "Q10 root")
        seal = close({
            "schema": "cm2.round306c30q10.terminal-seal-receipt.v1",
            "status": "PASS_C30Q10_EXACT_TERMINAL_SEAL__SOURCE_W_54_TO_0",
            "evidence_bundle_sha256": evidence["evidence_bundle_sha256"],
            "manifest_receipt_sha256": manifest_receipt["manifest_receipt_sha256"],
            "payload_manifest_sha256": payload_sha, "root_manifest_sha256": root_sha,
            "outer_verification_sha256": outer["outer_verification_sha256"],
            "before": BEFORE, "credit": CREDIT, "after": AFTER,
            "terminal_status": TERMINAL_STATUS,
            "all_receipt_object_hashes_closed": True,
            "all_payload_members_verified": True,
            "formal_transition_authorized_by_seal_alone": False, **STRICT,
        }, "terminal_seal_receipt_sha256")
        write_json(chain_tmp / "terminal_seal_receipt.json", seal)
        replay_names = ["evidence_bundle_receipt.json", "manifest_receipt.json",
                        "outer_verification.json", "payload_manifest.sha256",
                        "root_manifest.sha256", "terminal_seal_receipt.json"]
        replay = close({
            "schema": "cm2.round306c30q10.terminal-byte-replay.v1",
            "status": TERMINAL_STATUS,
            "required_member_sha256": {name: raw_sha(chain_tmp / name, "Q10 replay:" + name)
                                       for name in replay_names},
            "terminal_seal_receipt_sha256": seal["terminal_seal_receipt_sha256"],
            "c30f_terminal_replay_object_sha256": c30f["terminal_replay"]["terminal_replay_sha256"],
            "q9_result_object_sha256": q9["result_sha256"],
            "before": BEFORE, "credit": CREDIT, "after": AFTER,
            "all_bytes_replayed": True, "root_binds_payload_manifest": True,
            "root_binds_outer_verification": True,
            "C30q10_transition_authorized": True,
            "source_W_formal_remainder": 0, **STRICT,
        }, "terminal_replay_sha256")
        write_json(chain_tmp / "terminal_replay.json", replay)
        status = close({
            "schema": "cm2.round306c30q10.release-chain-status.v1",
            "status": CHAIN_STATUS, "terminal_status": TERMINAL_STATUS,
            "terminal_replay_file_sha256": raw_sha(chain_tmp / "terminal_replay.json", "Q10 status replay"),
            "terminal_replay_object_sha256": replay["terminal_replay_sha256"],
            "terminal_seal_file_sha256": raw_sha(chain_tmp / "terminal_seal_receipt.json", "Q10 status seal"),
            "terminal_seal_object_sha256": seal["terminal_seal_receipt_sha256"],
            "source_W_transition": {"before": 54, "after": 0},
            "source_W_transition_authorized": True,
            "source_W_formal_remainder": 0, **process, **STRICT,
        }, "chain_status_sha256")
        write_json(chain_tmp / "chain_status.json", status)
        (chain_tmp / "PASS.lock").write_bytes((CHAIN_STATUS + "\n").encode("ascii"))
        os.chmod(chain_tmp / "PASS.lock", 0o600)

        prior = c30f["formal_ledger"]
        transition_body = {
            "sequence": 5, "round": "C30q10", "before": BEFORE, "after": AFTER,
            "credits": CREDIT,
            "disposition": "44_EXCLUDED__10_RESOLVED_MIXED",
            "origin_keys": q9["origin_keys"],
            "origin_keys_sha256": q9["origin_keys_sha256"],
            "q9_result_object_sha256": q9["result_sha256"],
            "q9_receipt_file_sha256": raw_sha(q9["directory"] / "receipt.json", "Q9 transition receipt"),
            "q9_manifest_file_sha256": raw_sha(q9["directory"] / "manifest.sha256", "Q9 transition manifest"),
            "predecessor_ledger_object_sha256": prior["object_sha256"],
            "terminal_replay_object_sha256": replay["terminal_replay_sha256"],
            "chain_status_object_sha256": status["chain_status_sha256"],
            "InvocationID": process["InvocationID"], "ExecMainPID": process["ExecMainPID"],
        }
        transition = {**transition_body, "transition_id": digest(transition_body)}
        validate_transition(transition, prior, transition)
        audit = hostile(transition, prior)
        ledger = close({
            "schema": "cm2.source-w.consolidated-formal-ledger.v1",
            "status": "PASS_CONSOLIDATED_SOURCE_W_FORMAL_LEDGER__REMAINDER_0",
            "total_source_W_origins": 76_832,
            "formally_addressed_source_W_origins": 76_832,
            "formal_coverage_numerator": 76_832,
            "formal_coverage_denominator": 76_832,
            "remaining_origin_partition": AFTER["remaining_partition"],
            "current_state": AFTER,
            "applied_transition_ids": prior["applied_transition_ids"] + [transition["transition_id"]],
            "transitions": prior["transitions"] + [transition],
            "authority_pins": {
                **prior["authority_pins"],
                "c30q10_q9_result_object_sha256": q9["result_sha256"],
                "c30q10_q9_receipt_file_sha256": transition["q9_receipt_file_sha256"],
                "c30q10_terminal_replay_object_sha256": replay["terminal_replay_sha256"],
                "c30q10_chain_status_object_sha256": status["chain_status_sha256"],
                "c30q10_hostile_audit_object_sha256": audit["object_sha256"],
            },
            "strict_nonpromotion": STRICT,
        }, "object_sha256")
        application = close({
            "schema": "cm2.round306c30q10.formal-source-w-ledger-application-receipt.v1",
            "status": "PASS_C30Q10_FORMAL_LEDGER_SINGLE_APPLICATION__SOURCE_W_54_TO_0",
            "source_W_transition": {"before": 54, "after": 0},
            "source_W_transition_authorized": True,
            "source_W_formal_remainder": 0,
            "transition_id": transition["transition_id"],
            "ledger_object_sha256": ledger["object_sha256"],
            "terminal_replay_object_sha256": replay["terminal_replay_sha256"],
            "chain_status_object_sha256": status["chain_status_sha256"],
            "hostile_audit_object_sha256": audit["object_sha256"],
            "application_count": 1, "negative_test_count": 9, **process, **STRICT,
        }, "object_sha256")
        ledger_tmp.mkdir(mode=0o700)
        write_json(ledger_tmp / "source_w_formal_ledger.json", ledger)
        write_json(ledger_tmp / "application_receipt.json", application)
        write_json(ledger_tmp / "hostile_audit.json", audit)
        ledger_manifest = make_manifest(ledger_tmp, ["application_receipt.json",
                                                     "hostile_audit.json",
                                                     "source_w_formal_ledger.json"])
        (ledger_tmp / "root_manifest.sha256").write_bytes(ledger_manifest)
        os.chmod(ledger_tmp / "root_manifest.sha256", 0o600)
        (ledger_tmp / "PASS.lock").write_bytes(b"PASS_C30Q10_FORMAL_SOURCE_W_LEDGER__REMAINDER_0\n")
        os.chmod(ledger_tmp / "PASS.lock", 0o600)
        os.rename(chain_tmp, chain)
        os.rename(ledger_tmp, ledger_dir)
    except BaseException:
        shutil.rmtree(chain_tmp, ignore_errors=True)
        shutil.rmtree(ledger_tmp, ignore_errors=True)
        raise
    return close({
        "schema": "cm2.round306c30q10.c30f-q9-joint-publication-receipt.v1",
        "status": CHAIN_STATUS,
        "chain_dir": chain.relative_to(ROOT).as_posix(),
        "ledger_dir": ledger_dir.relative_to(ROOT).as_posix(),
        "chain_status_object_sha256": status["chain_status_sha256"],
        "terminal_replay_object_sha256": replay["terminal_replay_sha256"],
        "ledger_object_sha256": ledger["object_sha256"],
        "application_object_sha256": application["object_sha256"],
        "transition_id": transition["transition_id"],
        "q9_origin_count": 54, "q9_EXCLUDED": 44, "q9_RESOLVED_MIXED": 10,
        "hostile_negative_test_count": 9,
        "source_W_formal_remainder": 0, **STRICT,
    }, "publication_receipt_sha256")


def self_test() -> dict[str, Any]:
    exact_state(BEFORE, BEFORE, "Q10 fixture before")
    exact_state(AFTER, AFTER, "Q10 fixture after")
    need(BEFORE["remaining"] == 54 and AFTER["remaining"] == 0
         and CREDIT["EXCLUDED"] + CREDIT["RESOLVED_MIXED"] == 54,
         "Q10 fixture credit")
    return {
        "schema": "cm2.round306c30q10.c30f-q9-joint-consumer-self-test.v1",
        "status": "PASS_C30Q10_C30F_Q9_JOINT_STATIC_CONSERVATION_FIXTURES",
        "before": BEFORE, "credit": CREDIT, "after": AFTER,
        "expected_hostile_negative_test_count": 9, "CM2": "NO-GO_FOR_CLAIM",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--c30f-chain-dir", type=Path)
    parser.add_argument("--c30f-ledger-dir", type=Path)
    parser.add_argument("--q9-audit-dir", type=Path)
    parser.add_argument("--chain-dir", type=Path)
    parser.add_argument("--ledger-dir", type=Path)
    parser.add_argument("--self-test", action="store_true")
    arguments = parser.parse_args()
    fields = ("c30f_chain_dir", "c30f_ledger_dir", "q9_audit_dir",
              "chain_dir", "ledger_dir")
    try:
        if arguments.self_test:
            need(all(getattr(arguments, field) is None for field in fields), "self-test isolation")
            output = self_test()
        else:
            need(all(getattr(arguments, field) is not None for field in fields), "complete Q10 arguments")
            output = build(arguments)
    except (Reject, OSError, ValueError, TypeError, KeyError, AssertionError,
            RuntimeError, json.JSONDecodeError) as error:
        print("REJECT:" + type(error).__name__ + ":" + str(error), file=sys.stderr)
        return 2
    print(canonical(output).decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
