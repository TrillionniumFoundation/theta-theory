#!/usr/bin/env python3
"""Install the terminal-authorized C30c 80-to-78 transition exactly once."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import stat
import subprocess
import sys
import tarfile
from pathlib import Path
from typing import Any, Callable, Mapping

WORKSPACE = Path("/home/qian-qi/.openclaw/workspaces/telegram-bot-8449317572")
AUDIT = WORKSPACE / ".cm2-runtime/audit"
RECEIPTS = WORKSPACE / ".cm2-runtime/receipts"
WATCHER = WORKSPACE / "deliverables/cm2_round306c30c_postreceipt_v5_v6_publication_chain_watch_v2.py"
CHAIN_FILES = frozenset({
    "PUBLICATION_PASS.lock",
    "adapter_verification.json",
    "c30c_v5_v6_joint_publication_evidence.tar.gz",
    "chain_status.json",
    "evidence_index.json",
    "outer_verification.json",
    "payload_manifest.sha256",
    "root_manifest.sha256",
    "terminal_replay.json",
})
LEDGER_FILES = frozenset({
    "PASS.lock",
    "application_receipt.json",
    "hostile_audit.json",
    "root_manifest.sha256",
    "source_w_formal_ledger.json",
})
LEDGER_JSON_FILES = (
    "source_w_formal_ledger.json",
    "hostile_audit.json",
    "application_receipt.json",
)
PASS_BYTES = b"PASS_C30C_FORMAL_SOURCE_W_LEDGER_SINGLE_APPLICATION__80_TO_78__CM2_NO_GO\n"
PUBLICATION_BYTES = b"PASS_C30C_V5_V6_JOINT_PUBLICATION__SOURCE_W_80_TO_78__CM2_NO_GO\n"
HEX64 = re.compile(r"[0-9a-f]{64}\Z")
INVOCATION = re.compile(r"[0-9a-f]{32}\Z")
MANIFEST_ROW = re.compile(r"([0-9a-f]{64})  ([A-Za-z0-9_./-]+)\Z")
TERMINAL_SCHEMA = "cm2.round306c30c.v5-v6-joint-publication-terminal-replay.v1"
TERMINAL_STATUS = "PASS_TERMINAL_REPLAY__FORMAL_SOURCE_W_80_TO_78"
AUDIT_SCHEMA = "cm2.round306c30c.v5-v6-publication-independent-audit.v1"
AUDIT_STATUS = "PASS_FULL_TAR_MANIFEST_OBJECT_UNIT_AND_LIVE_ADAPTER_REPLAY"
CHAIN_SCHEMA = "cm2.round306c30c.v5-v6-publication-chain-watch.v2"
CHAIN_STATUS = "PASS_C30C_V5_V6_JOINT_PUBLICATION__FORMAL_SOURCE_W_80_TO_78"
C30B_SCHEMA = "cm2.round306c30b.source-w-outgoing-h-whole-origin-disposition.v1"
C30B_STATUS = "PASS_BOUNDED_ROUND306C30B_OUTGOING_H_DISPOSITION"
C30C_SCHEMA = "cm2.round306c30c.source-w-full-delta-whole-origin-disposition.candidate.v1"
C30C_STATUS = "PASS_CANDIDATE_ROUND306C30C_FULL_DELTA_DISPOSITION__AWAITING_INDEPENDENT_VERIFIER_AND_MANIFEST"
CANDIDATE_ENTRY = "candidate/cm2_round306c30c_source_w_full_delta_whole_origin_disposition_result.json"
PREDECESSOR_MANIFEST_ENTRY = "predecessor/manifest.sha256"


class Blocked(RuntimeError):
    pass


def need(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise Blocked(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=True, allow_nan=False, sort_keys=True,
                      separators=(",", ":")).encode("ascii")


def digest(value: Mapping[str, Any]) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def closed(value: Mapping[str, Any], field: str = "object_sha256") -> dict[str, Any]:
    output = dict(value)
    output[field] = digest(output)
    return output


def strict_json(raw: bytes, label: str) -> dict[str, Any]:
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


def validate_closure(value: Mapping[str, Any], field: str, label: str) -> None:
    body = dict(value)
    observed = body.pop(field, None)
    need(type(observed) is str and HEX64.fullmatch(observed) is not None
         and digest(body) == observed, "object closure:" + label)


def file_bytes(path: Path, maximum: int = 512 << 20) -> bytes:
    absolute = Path(os.path.abspath(os.fspath(path)))
    need(absolute.resolve(strict=True) == absolute, "canonical path:" + os.fspath(path))
    descriptor = os.open(absolute, os.O_RDONLY | os.O_CLOEXEC | getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(descriptor)
        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1
             and 0 <= before.st_size <= maximum, "bounded singleton:" + os.fspath(path))
        raw = bytearray()
        while len(raw) <= before.st_size:
            block = os.read(descriptor, min(4 << 20, before.st_size + 1 - len(raw)))
            if not block:
                break
            raw.extend(block)
        after = os.fstat(descriptor)
    finally:
        os.close(descriptor)
    identity = lambda value: (value.st_dev, value.st_ino, value.st_mode, value.st_nlink,
                              value.st_uid, value.st_gid, value.st_size,
                              value.st_mtime_ns, value.st_ctime_ns)
    need(len(raw) == before.st_size and identity(before) == identity(after),
         "stable capture:" + os.fspath(path))
    return bytes(raw)


def file_sha(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(4 << 20):
            state.update(block)
    return state.hexdigest()


def read_json(path: Path, closure_field: str, label: str) -> dict[str, Any]:
    value = strict_json(file_bytes(path, 64 << 20), label)
    validate_closure(value, closure_field, label)
    return value


def parse_manifest(raw: bytes, label: str) -> dict[str, str]:
    try:
        rows = raw.decode("ascii").splitlines()
    except UnicodeDecodeError as error:
        raise Blocked("ASCII manifest:" + label) from error
    output: dict[str, str] = {}
    for row in rows:
        match = MANIFEST_ROW.fullmatch(row)
        need(match is not None and match.group(2) not in output, "manifest row:" + label)
        output[match.group(2)] = match.group(1)
    need(bool(output) and raw.endswith(b"\n"), "nonempty terminated manifest:" + label)
    return output


def validate_manifest(observed: Mapping[str, str], expected: Mapping[str, str], label: str) -> None:
    need(dict(observed) == dict(expected), "manifest closure:" + label)


def exact_state() -> tuple[dict[str, Any], dict[str, Any]]:
    before = {
        "conservative_live": 2086,
        "excluded": 74746,
        "remaining": 80,
        "remaining_partition": {
            "compact_q": 54,
            "full_Delta": 2,
            "multi_Delta": 20,
            "reduced_live": 2,
            "retained_source_seams": 2,
        },
        "resolved_nonexcluded": 2006,
        "total": 76832,
    }
    after = {
        "conservative_live": 2086,
        "excluded": 74746,
        "remaining": 78,
        "remaining_partition": {
            "compact_q": 54,
            "multi_Delta": 20,
            "reduced_live": 2,
            "retained_source_seams": 2,
        },
        "resolved_nonexcluded": 2008,
        "total": 76832,
    }
    return before, after


def validate_state(value: Mapping[str, Any], label: str) -> None:
    keys = {"conservative_live", "excluded", "remaining", "remaining_partition",
            "resolved_nonexcluded", "total"}
    need(set(value) == keys, "state fields:" + label)
    integers = [value.get(name) for name in keys if name != "remaining_partition"]
    need(all(type(number) is int and number >= 0 for number in integers), "state integers:" + label)
    partition = value.get("remaining_partition")
    need(type(partition) is dict and bool(partition)
         and all(type(key) is str and type(number) is int and number >= 0
                 for key, number in partition.items()), "remaining partition:" + label)
    need(value["excluded"] + value["conservative_live"] == value["total"]
         and value["resolved_nonexcluded"] + value["remaining"] == value["conservative_live"]
         and sum(partition.values()) == value["remaining"], "conservation:" + label)


def transition_id(terminal: Mapping[str, Any], predecessor: Mapping[str, Any]) -> str:
    body = {
        "schema": "cm2.source-w.formal-transition-id.v1",
        "predecessor_result_object_sha256": predecessor["result_sha256"],
        "terminal_replay_object_sha256": terminal["object_sha256"],
        "before": 80,
        "after": 78,
    }
    return digest(body)


def apply_transition(current: Mapping[str, Any], proposal: Mapping[str, Any], identifier: str,
                     applied: list[str]) -> dict[str, Any]:
    need(type(identifier) is str and HEX64.fullmatch(identifier) is not None,
         "transition identifier")
    need(all(type(value) is str and HEX64.fullmatch(value) is not None for value in applied),
         "applied transition identifiers")
    need(identifier not in applied, "duplicate transition application")
    before = proposal.get("before")
    after = proposal.get("after")
    need(type(before) is dict and type(after) is dict, "typed transition states")
    validate_state(current, "current")
    validate_state(before, "proposal before")
    validate_state(after, "proposal after")
    need(dict(current) == before, "ordered predecessor state")
    need(after["total"] == before["total"]
         and after["excluded"] == before["excluded"]
         and after["conservative_live"] == before["conservative_live"]
         and after["resolved_nonexcluded"] - before["resolved_nonexcluded"] == 2
         and before["remaining"] - after["remaining"] == 2,
         "exact conserved 80-to-78 delta")
    return dict(after)


def validate_terminal(value: Mapping[str, Any]) -> None:
    validate_closure(value, "object_sha256", "terminal")
    need(value.get("schema") == TERMINAL_SCHEMA and value.get("status") == TERMINAL_STATUS
         and value.get("source_W_transition") == {"before": 80, "after": 78}
         and value.get("source_W_formal_remainder") == 78
         and value.get("source_W_transition_authorized") is True
         and value.get("formal_credit") == {
             "resolved_nonexcluded": 2,
             "resolved_source_W_origin_dispositions": 2,
             "whole_source_W_origin_exclusions": 0,
         }
         and value.get("D02") == "BLOCKED_COMPOSITE"
         and value.get("D03") == "UNAUTHORIZED"
         and value.get("D04") == "NOT_MINTED"
         and value.get("Gate5") == "10/18"
         and value.get("CM2") == "NO-GO_FOR_CLAIM", "exact terminal authority")


def validate_unit_binding(fields: Mapping[str, str], audit: Mapping[str, Any]) -> None:
    unit = audit.get("unit")
    invocation = audit.get("InvocationID")
    pid = audit.get("ExecMainPID")
    watcher_sha256 = audit.get("watcher_sha256")
    need(type(unit) is str and unit.startswith("cm2-c30c-publication-v5-v6-")
         and unit.endswith(".service") and type(invocation) is str
         and INVOCATION.fullmatch(invocation) is not None and type(pid) is int and pid > 1
         and type(watcher_sha256) is str and HEX64.fullmatch(watcher_sha256) is not None,
         "typed publication service authority")
    need(fields.get("Id") == unit and fields.get("InvocationID") == invocation
         and fields.get("MainPID") == "0" and fields.get("ExecMainPID") == str(pid)
         and fields.get("ActiveState") == "active" and fields.get("SubState") == "exited"
         and fields.get("Result") == "success" and fields.get("ExecMainCode") in {"1", "exited"}
         and fields.get("ExecMainStatus") == "0"
         and watcher_sha256 in fields.get("ExecStart", "")
         and os.fspath(WATCHER) in fields.get("ExecStart", ""), "live PID/Invocation/source binding")


def systemctl_fields(unit: str) -> dict[str, str]:
    names = ("Id", "InvocationID", "MainPID", "ExecMainPID", "ActiveState", "SubState",
             "Result", "ExecMainCode", "ExecMainStatus", "ExecStart")
    command = ["/usr/bin/systemctl", "--user", "show", unit]
    for name in names:
        command.extend(("-p", name))
    completed = subprocess.run(command, cwd=WORKSPACE, stdin=subprocess.DEVNULL,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    need(completed.returncode == 0 and completed.stderr == b"", "clean systemctl query")
    fields = dict(row.split("=", 1) for row in completed.stdout.decode("ascii").splitlines()
                  if "=" in row)
    need(set(fields) == set(names), "exact systemctl fields")
    return fields


def validate_publication_marker(raw: bytes) -> None:
    need(raw == PUBLICATION_BYTES, "exact publication marker")


def tar_replay(chain: Path, evidence: Mapping[str, Any]) -> dict[str, bytes]:
    entries = evidence.get("entries")
    need(type(entries) is list and evidence.get("entry_count") == len(entries), "evidence census")
    expected: dict[str, str] = {}
    for row in entries:
        need(type(row) is dict and set(row) >= {"name", "sha256"}
             and type(row.get("name")) is str and row["name"] not in expected
             and type(row.get("sha256")) is str and HEX64.fullmatch(row["sha256"]) is not None,
             "typed unique evidence row")
        expected[row["name"]] = row["sha256"]
    selected: dict[str, bytes] = {}
    observed: dict[str, str] = {}
    bundle = chain / "c30c_v5_v6_joint_publication_evidence.tar.gz"
    try:
        with tarfile.open(bundle, "r:gz") as archive:
            for member in archive:
                need(member.isfile() and member.name not in observed and member.name in expected,
                     "regular indexed tar entry")
                stream = archive.extractfile(member)
                need(stream is not None, "tar stream")
                raw = stream.read()
                observed[member.name] = hashlib.sha256(raw).hexdigest()
                if member.name in {CANDIDATE_ENTRY, PREDECESSOR_MANIFEST_ENTRY}:
                    selected[member.name] = raw
    except tarfile.TarError as error:
        raise Blocked("tar replay") from error
    need(observed == expected and set(selected) == {CANDIDATE_ENTRY, PREDECESSOR_MANIFEST_ENTRY},
         "full tar/index byte replay")
    return selected


def relative_workspace(path: Path) -> str:
    return os.fspath(path.relative_to(WORKSPACE))


def workspace_path(value: Any, label: str) -> Path:
    need(type(value) is str and value != "", "typed source path:" + label)
    path = (WORKSPACE / value).resolve(strict=True)
    need(path.is_relative_to(WORKSPACE), "confined source path:" + label)
    return path


def validate_authority(chain: Path, independent_path: Path, c30b_result_path: Path,
                       c30b_manifest_path: Path) -> dict[str, Any]:
    need(chain.parent == AUDIT and chain.name.startswith("c30c-publication-v5-v6-chain-")
         and {entry.name for entry in chain.iterdir()} == CHAIN_FILES, "exact chain inventory")
    need(independent_path.parent == RECEIPTS / chain.name
         and independent_path.name == "independent_audit.json", "exact independent receipt path")
    terminal = read_json(chain / "terminal_replay.json", "object_sha256", "terminal")
    validate_terminal(terminal)
    status = read_json(chain / "chain_status.json", "object_sha256", "chain status")
    evidence = read_json(chain / "evidence_index.json", "object_sha256", "evidence index")
    outer = read_json(chain / "outer_verification.json", "object_sha256", "outer verification")
    adapter = read_json(chain / "adapter_verification.json", "object_sha256", "adapter verification")
    independent = read_json(independent_path, "object_sha256", "independent audit")
    need(status.get("schema") == CHAIN_SCHEMA and status.get("status") == CHAIN_STATUS
         and status.get("chain_name") == chain.name
         and status.get("terminal_replay_object_sha256") == terminal["object_sha256"]
         and status.get("terminal_replay_file_sha256") == file_sha(chain / "terminal_replay.json")
         and status.get("source_W_formal_remainder") == 78
         and status.get("source_W_transition_authorized") is True
         and status.get("CM2") == "NO-GO_FOR_CLAIM", "exact chain status")
    need(independent.get("schema") == AUDIT_SCHEMA and independent.get("status") == AUDIT_STATUS
         and independent.get("chain_name") == chain.name
         and independent.get("chain_status_object_sha256") == status["object_sha256"]
         and independent.get("terminal_replay_object_sha256") == terminal["object_sha256"]
         and independent.get("source_W_formal_remainder") == 78
         and independent.get("source_W_transition_authorized") is True
         and independent.get("CM2") == "NO-GO_FOR_CLAIM", "exact independent audit")
    need(outer.get("status") ==
         "PASS_JOINT_ADAPTER_AND_AUDITED_DUAL_MATHEMATICS__CONDITIONAL_80_TO_78"
         and outer.get("source_W_transition_authorized") is False
         and adapter.get("status") == "PASS_ADAPTER_LIVE_REPLAY_AND_ALL_BINDINGS",
         "preterminal zero-credit boundaries")
    need(file_sha(WATCHER) == independent.get("watcher_sha256"), "watcher source pin")
    fields = systemctl_fields(independent["unit"])
    validate_unit_binding(fields, independent)
    payload = parse_manifest(file_bytes(chain / "payload_manifest.sha256"), "payload")
    validate_manifest(payload, {
        "adapter_verification.json": file_sha(chain / "adapter_verification.json"),
        "outer_verification.json": file_sha(chain / "outer_verification.json"),
        "c30c_v5_v6_joint_publication_evidence.tar.gz":
            file_sha(chain / "c30c_v5_v6_joint_publication_evidence.tar.gz"),
        "evidence_index.json": file_sha(chain / "evidence_index.json"),
    }, "payload")
    root = parse_manifest(file_bytes(chain / "root_manifest.sha256"), "root")
    validate_manifest(root, {"payload_manifest.sha256": file_sha(chain / "payload_manifest.sha256")},
                      "root")
    need(terminal.get("payload_manifest_sha256") == file_sha(chain / "payload_manifest.sha256")
         and terminal.get("root_manifest_sha256") == file_sha(chain / "root_manifest.sha256"),
         "terminal manifest binding")
    validate_publication_marker(file_bytes(chain / "PUBLICATION_PASS.lock", 256))
    bundle_sha256 = file_sha(chain / "c30c_v5_v6_joint_publication_evidence.tar.gz")
    need(evidence.get("bundle_sha256") == independent.get("bundle_sha256") == bundle_sha256,
         "bundle binding")
    selected = tar_replay(chain, evidence)
    candidate = strict_json(selected[CANDIDATE_ENTRY], "tar candidate")
    validate_closure(candidate, "result_sha256", "tar candidate")
    before, after = exact_state()
    proposal = candidate.get("proposed_source_W_ledger_transition_if_independently_verified")
    need(candidate.get("schema") == C30C_SCHEMA and candidate.get("status") == C30C_STATUS
         and candidate.get("result_sha256") == terminal.get("candidate_result_object_sha256")
         and type(proposal) is dict and proposal.get("before") == before
         and proposal.get("after") == after
         and proposal.get("candidate_credits") == {
             "resolved_nonexcluded": 2,
             "resolved_origin_disposition": 2,
             "whole_origin_exclusion": 0,
         }
         and proposal.get("official_ledger_mutated") is False
         and candidate.get("scope", {}).get("origin_keys") == [
             "W:N:04.00.10000010", "W:S:H.04.00.10000010"]
         and candidate.get("scope", {}).get("whole_origin_disposition_census") == {
             "RESOLVED_MIXED": 2}, "exact C30c candidate transition")
    c30b_result = read_json(c30b_result_path, "result_sha256", "C30b result")
    c30b_manifest_raw = file_bytes(c30b_manifest_path, 8 << 20)
    c30b_manifest = parse_manifest(c30b_manifest_raw, "C30b manifest")
    expected_result_name = relative_workspace(c30b_result_path).removeprefix("deliverables/")
    need(c30b_result.get("schema") == C30B_SCHEMA and c30b_result.get("status") == C30B_STATUS
         and c30b_result.get("source_W_ledger_transition", {}).get("after") == before
         and c30b_manifest.get(expected_result_name) == file_sha(c30b_result_path)
         and file_sha(c30b_manifest_path) == terminal.get("round306c30b_manifest_sha256")
         and c30b_manifest_raw == selected[PREDECESSOR_MANIFEST_ENTRY]
         and candidate.get("upstream_C30b_dependency", {}).get("sealed_authority", {}).get(
             "result_object_sha256") == c30b_result["result_sha256"], "exact C30b predecessor")
    identifier = transition_id(terminal, c30b_result)
    current = apply_transition(before, proposal, identifier, [])
    need(current == after, "installed state")
    return {
        "terminal": terminal,
        "status": status,
        "independent": independent,
        "candidate": candidate,
        "c30b_result": c30b_result,
        "proposal": proposal,
        "transition_id": identifier,
        "before": before,
        "after": after,
        "bundle_sha256": bundle_sha256,
        "evidence_entry_count": evidence["entry_count"],
        "live_fields": fields,
    }


def hostile_self_test() -> dict[str, Any]:
    before, after = exact_state()
    terminal = closed({
        "schema": TERMINAL_SCHEMA,
        "status": TERMINAL_STATUS,
        "source_W_transition": {"before": 80, "after": 78},
        "source_W_formal_remainder": 78,
        "source_W_transition_authorized": True,
        "formal_credit": {
            "resolved_nonexcluded": 2,
            "resolved_source_W_origin_dispositions": 2,
            "whole_source_W_origin_exclusions": 0,
        },
        "D02": "BLOCKED_COMPOSITE",
        "D03": "UNAUTHORIZED",
        "D04": "NOT_MINTED",
        "Gate5": "10/18",
        "CM2": "NO-GO_FOR_CLAIM",
    })
    validate_terminal(terminal)
    identifier = "a" * 64
    proposal = {"before": before, "after": after}
    audit = {
        "unit": "cm2-c30c-publication-v5-v6-fixture.service",
        "InvocationID": "b" * 32,
        "ExecMainPID": 4242,
        "watcher_sha256": "c" * 64,
    }
    fields = {
        "Id": audit["unit"],
        "InvocationID": audit["InvocationID"],
        "MainPID": "0",
        "ExecMainPID": "4242",
        "ActiveState": "active",
        "SubState": "exited",
        "Result": "success",
        "ExecMainCode": "1",
        "ExecMainStatus": "0",
        "ExecStart": os.fspath(WATCHER) + " " + audit["watcher_sha256"],
    }
    validate_unit_binding(fields, audit)
    attacks: list[tuple[str, Callable[[], Any]]] = []
    bad_after = dict(after)
    bad_after["remaining"] = 77
    attacks.append(("conservation", lambda: apply_transition(before, {
        "before": before, "after": bad_after}, identifier, [])))
    attacks.append(("duplicate", lambda: apply_transition(before, proposal, identifier, [identifier])))
    wrong_current = dict(before)
    wrong_current["remaining"] = 79
    wrong_current["resolved_nonexcluded"] = 2007
    attacks.append(("out_of_order", lambda: apply_transition(wrong_current, proposal, identifier, [])))
    bad_schema = closed({**{key: value for key, value in terminal.items()
                            if key != "object_sha256"}, "schema": "stale.schema.v0"})
    attacks.append(("schema", lambda: validate_terminal(bad_schema)))
    bad_pid = dict(fields)
    bad_pid["ExecMainPID"] = "4243"
    attacks.append(("PID", lambda: validate_unit_binding(bad_pid, audit)))
    bad_stale = dict(fields)
    bad_stale["InvocationID"] = "d" * 32
    attacks.append(("stale", lambda: validate_unit_binding(bad_stale, audit)))
    attacks.append(("marker", lambda: validate_publication_marker(PUBLICATION_BYTES + b"X")))
    attacks.append(("manifest", lambda: validate_manifest({"a": "0" * 64}, {"a": "1" * 64},
                                                           "hostile")))
    bad_object = dict(terminal)
    bad_object["source_W_formal_remainder"] = 77
    attacks.append(("object", lambda: validate_terminal(bad_object)))
    rejected: list[str] = []
    for name, attack in attacks:
        try:
            attack()
        except Blocked:
            rejected.append(name)
        else:
            raise Blocked("negative accepted:" + name)
    need(rejected == ["conservation", "duplicate", "out_of_order", "schema", "PID",
                      "stale", "marker", "manifest", "object"], "negative test order")
    return closed({
        "schema": "cm2.round306c30c.formal-source-w-ledger-consumer-hostile-audit.v1",
        "status": "PASS_9_OF_9_CONSERVATION_DUPLICATE_ORDER_SCHEMA_PID_STALE_MARKER_MANIFEST_OBJECT_REJECTED",
        "negative_tests": rejected,
        "negative_test_count": len(rejected),
        "formal_credit": 0,
        "source_W_transition_authorized": False,
        "CM2": "NO-GO_FOR_CLAIM",
    })


def exclusive(path: Path, raw: bytes) -> None:
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_CLOEXEC, 0o400)
    try:
        need(os.write(descriptor, raw) == len(raw), "complete write:" + path.name)
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def build_ledger(authority: Mapping[str, Any], paths: Mapping[str, Path],
                 hostile: Mapping[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    terminal = authority["terminal"]
    independent = authority["independent"]
    candidate = authority["candidate"]
    c30b_result = authority["c30b_result"]
    identifier = authority["transition_id"]
    ledger = closed({
        "schema": "cm2.source-w.consolidated-formal-ledger.v1",
        "status": "PASS_CONSOLIDATED_SOURCE_W_FORMAL_LEDGER__REMAINDER_78",
        "total_source_W_origins": 76832,
        "formally_addressed_source_W_origins": 76754,
        "formal_coverage_numerator": 76754,
        "formal_coverage_denominator": 76832,
        "current_state": authority["after"],
        "remaining_origin_partition": authority["after"]["remaining_partition"],
        "applied_transition_ids": [identifier],
        "transitions": [{
            "sequence": 1,
            "transition_id": identifier,
            "round": "C30c",
            "before": authority["before"],
            "after": authority["after"],
            "credits": {
                "resolved_nonexcluded": 2,
                "resolved_source_W_origin_dispositions": 2,
                "whole_source_W_origin_exclusions": 0,
            },
            "origin_keys": ["W:N:04.00.10000010", "W:S:H.04.00.10000010"],
            "disposition": "RESOLVED_MIXED",
            "predecessor_result_object_sha256": c30b_result["result_sha256"],
            "candidate_result_object_sha256": candidate["result_sha256"],
            "terminal_replay_object_sha256": terminal["object_sha256"],
            "independent_audit_object_sha256": independent["object_sha256"],
        }],
        "authority_pins": {
            "c30b_result_file_sha256": file_sha(paths["c30b_result"]),
            "c30b_result_object_sha256": c30b_result["result_sha256"],
            "c30b_manifest_file_sha256": file_sha(paths["c30b_manifest"]),
            "c30c_candidate_result_object_sha256": candidate["result_sha256"],
            "c30c_publication_terminal_file_sha256": file_sha(paths["chain"] / "terminal_replay.json"),
            "c30c_publication_terminal_object_sha256": terminal["object_sha256"],
            "c30c_independent_audit_file_sha256": file_sha(paths["independent"]),
            "c30c_independent_audit_object_sha256": independent["object_sha256"],
            "publication_bundle_sha256": authority["bundle_sha256"],
            "hostile_audit_object_sha256": hostile["object_sha256"],
        },
        "strict_nonpromotion": {
            "D02": "BLOCKED_COMPOSITE",
            "D03": "UNAUTHORIZED",
            "D04": "NOT_MINTED",
            "Gate5": "10/18",
            "complete_global_18_field_blocks": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        },
    })
    receipt = closed({
        "schema": "cm2.round306c30c.formal-source-w-ledger-application-receipt.v1",
        "status": "PASS_C30C_FORMAL_LEDGER_SINGLE_APPLICATION__SOURCE_W_80_TO_78",
        "ledger_object_sha256": ledger["object_sha256"],
        "transition_id": identifier,
        "application_count": 1,
        "hostile_audit_object_sha256": hostile["object_sha256"],
        "negative_test_count": hostile["negative_test_count"],
        "evidence_entry_count": authority["evidence_entry_count"],
        "source_paths": {key: relative_workspace(path) for key, path in paths.items()},
        "source_file_sha256": {
            "terminal_replay": file_sha(paths["chain"] / "terminal_replay.json"),
            "independent_audit": file_sha(paths["independent"]),
            "c30b_result": file_sha(paths["c30b_result"]),
            "c30b_manifest": file_sha(paths["c30b_manifest"]),
        },
        "publication_unit": independent["unit"],
        "publication_InvocationID": independent["InvocationID"],
        "publication_ExecMainPID": independent["ExecMainPID"],
        "source_W_transition": {"before": 80, "after": 78},
        "source_W_formal_remainder": 78,
        "source_W_transition_authorized": True,
        "D02": "BLOCKED_COMPOSITE",
        "D03": "UNAUTHORIZED",
        "D04": "NOT_MINTED",
        "Gate5": "10/18",
        "CM2": "NO-GO_FOR_CLAIM",
    })
    return ledger, receipt


def install(paths: Mapping[str, Path], output: Path) -> dict[str, Any]:
    need(output.parent == AUDIT and output.name.startswith("c30c-formal-source-w-ledger-")
         and not output.exists(), "fresh exact ledger output")
    hostile = hostile_self_test()
    authority = validate_authority(paths["chain"], paths["independent"],
                                   paths["c30b_result"], paths["c30b_manifest"])
    ledger, receipt = build_ledger(authority, paths, hostile)
    output.mkdir(mode=0o700)
    exclusive(output / "source_w_formal_ledger.json", canonical(ledger) + b"\n")
    exclusive(output / "hostile_audit.json", canonical(hostile) + b"\n")
    exclusive(output / "application_receipt.json", canonical(receipt) + b"\n")
    manifest = "".join(f"{file_sha(output / name)}  {name}\n" for name in LEDGER_JSON_FILES)
    exclusive(output / "root_manifest.sha256", manifest.encode("ascii"))
    exclusive(output / "PASS.lock", PASS_BYTES)
    return receipt


def verify(output: Path) -> dict[str, Any]:
    need(output.parent == AUDIT and output.name.startswith("c30c-formal-source-w-ledger-")
         and {entry.name for entry in output.iterdir()} == LEDGER_FILES, "exact ledger inventory")
    ledger = read_json(output / "source_w_formal_ledger.json", "object_sha256", "formal ledger")
    hostile = read_json(output / "hostile_audit.json", "object_sha256", "hostile audit")
    receipt = read_json(output / "application_receipt.json", "object_sha256", "application receipt")
    source_paths = receipt.get("source_paths")
    need(type(source_paths) is dict and set(source_paths) == {
        "chain", "independent", "c30b_result", "c30b_manifest"}, "receipt source paths")
    paths = {key: workspace_path(value, key) for key, value in source_paths.items()}
    authority = validate_authority(paths["chain"], paths["independent"],
                                   paths["c30b_result"], paths["c30b_manifest"])
    rebuilt_ledger, rebuilt_receipt = build_ledger(authority, paths, hostile)
    need(hostile == hostile_self_test() and ledger == rebuilt_ledger and receipt == rebuilt_receipt,
         "full deterministic ledger replay")
    root = parse_manifest(file_bytes(output / "root_manifest.sha256"), "ledger root")
    validate_manifest(root, {name: file_sha(output / name) for name in LEDGER_JSON_FILES},
                      "ledger root")
    need(file_bytes(output / "PASS.lock", 256) == PASS_BYTES, "exact ledger marker")
    return closed({
        "schema": "cm2.round306c30c.formal-source-w-ledger-independent-verification.v1",
        "status": "PASS_FULL_LEDGER_AUTHORITY_LIVE_UNIT_AND_9_NEGATIVE_REPLAY",
        "ledger_directory": output.name,
        "ledger_object_sha256": ledger["object_sha256"],
        "application_receipt_object_sha256": receipt["object_sha256"],
        "hostile_audit_object_sha256": hostile["object_sha256"],
        "transition_id": authority["transition_id"],
        "negative_test_count": hostile["negative_test_count"],
        "source_W_formal_remainder": 78,
        "source_W_transition_authorized": True,
        "CM2": "NO-GO_FOR_CLAIM",
    })


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--self-test", action="store_true")
    mode.add_argument("--install", action="store_true")
    mode.add_argument("--verify", action="store_true")
    parser.add_argument("--chain-dir", type=Path)
    parser.add_argument("--independent-audit", type=Path)
    parser.add_argument("--c30b-result", type=Path)
    parser.add_argument("--c30b-manifest", type=Path)
    parser.add_argument("--output-dir", type=Path)
    args = parser.parse_args()
    try:
        sources = (args.chain_dir, args.independent_audit, args.c30b_result, args.c30b_manifest)
        if args.self_test:
            need(all(value is None for value in sources) and args.output_dir is None,
                 "self-test isolation")
            result = hostile_self_test()
        elif args.install:
            need(all(value is not None for value in sources) and args.output_dir is not None,
                 "install paths")
            paths = {
                "chain": args.chain_dir.resolve(strict=True),
                "independent": args.independent_audit.resolve(strict=True),
                "c30b_result": args.c30b_result.resolve(strict=True),
                "c30b_manifest": args.c30b_manifest.resolve(strict=True),
            }
            result = install(paths, args.output_dir.absolute())
        else:
            need(all(value is None for value in sources) and args.output_dir is not None,
                 "verify paths")
            result = verify(args.output_dir.resolve(strict=True))
    except (Blocked, OSError, ValueError, TypeError, KeyError, json.JSONDecodeError,
            subprocess.SubprocessError, tarfile.TarError) as error:
        result = {
            "schema": "cm2.round306c30c.formal-source-w-ledger-consumer-failure.v1",
            "status": "BLOCKED_FAIL_CLOSED",
            "error": str(error),
            "source_W_transition_authorized": False,
            "formal_credit": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        }
        sys.stdout.buffer.write(canonical(result) + b"\n")
        return 2
    sys.stdout.buffer.write(canonical(result) + b"\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
