#!/usr/bin/env python3
"""Independently audit the C30d terminal consumer and its fail-closed surface."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
from pathlib import Path
import shutil
import stat
import subprocess
import sys
from typing import Any, Callable


ROOT = Path(__file__).resolve().parent.parent
REQUIRED = tuple(sorted((
    "chain_status.json", "evidence_bundle_receipt.json", "manifest_receipt.json",
    "outer_verification.json", "payload_manifest.sha256", "root_manifest.sha256",
    "terminal_replay.json", "terminal_seal_receipt.json",
)))
LEDGER_MEMBERS = tuple(sorted((
    "PASS.lock", "application_receipt.json", "hostile_audit.json",
    "root_manifest.sha256", "source_w_formal_ledger.json",
)))
PIN_SCHEMA = "cm2.round306c30d.v3-terminal-consumer-dynamic-pins.v1"
PROJECTION_SCHEMA = "cm2.round306c30e.c30d-terminal-predecessor-projection.v1"
PROJECTION_STATUS = (
    "PASS_EXACT_VERSIONED_C30D_TERMINAL_GRAPH_AS_C30E_PREDECESSOR__"
    "ZERO_C30E_FORMAL_CREDIT"
)
TERMINAL_STATUS = "PASS_FORMAL_C30D_TERMINAL__78_TO_58_AUTHORIZED"
CHAIN_STATUS = "PASS_C30D_V3_TERMINAL_BYTE_REPLAY__FORMAL_SOURCE_W_78_TO_58"
BEFORE = {
    "excluded": 74_746, "conservative_live": 2_086,
    "resolved_nonexcluded": 2_008, "remaining": 78, "total": 76_832,
    "remaining_partition": {
        "multi_Delta": 20, "reduced_live": 2,
        "retained_source_seams": 2, "compact_q": 54,
    },
}
PROJECTION_BEFORE = {
    **{key: value for key, value in BEFORE.items() if key != "remaining_partition"},
    "remaining_partition": {
        "multi_delta": 20, "reduced_live": 2,
        "retained_source_seams": 2, "compact_q": 54,
    },
}
AFTER = {
    "excluded": 74_766, "conservative_live": 2_066,
    "resolved_nonexcluded": 2_008, "remaining": 58, "total": 76_832,
    "remaining_partition": {
        "reduced_live": 2, "retained_source_seams": 2, "compact_q": 54,
    },
}
CREDIT = {
    "resolved_source_W_origin_dispositions": 20,
    "whole_source_W_origin_exclusions": 20,
    "resolved_nonexcluded": 0,
}
ZERO_C30E = {
    "outgoing_H_cell_dispositions": 0, "strict_LIVE_cell_dispositions": 0,
    "resolved_source_W_origin_dispositions": 0, "resolved_nonexcluded": 0,
    "whole_source_W_origin_exclusions": 0,
    "D02": 0, "D03": 0, "D04": 0, "Gate5": 0, "CM2": 0,
}


class Reject(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Reject(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def valid_sha(value: Any) -> bool:
    return type(value) is str and len(value) == 64 and all(
        character in "0123456789abcdef" for character in value
    )


def close(value: dict[str, Any], field: str) -> dict[str, Any]:
    body = dict(value)
    body.pop(field, None)
    return {**body, field: digest(body)}


def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
    output: dict[str, Any] = {}
    for key, value in items:
        need(key not in output, "duplicate key:" + key)
        output[key] = value
    return output


def workspace(raw: Path, *, absent: bool = False) -> Path:
    path = Path(os.path.abspath(os.fspath(raw if raw.is_absolute() else ROOT / raw)))
    try:
        relative = path.relative_to(ROOT)
    except ValueError as error:
        raise Reject("outside workspace") from error
    need(relative.parts and all(part not in {"", ".", ".."} for part in relative.parts), "canonical path")
    cursor = ROOT
    for part in relative.parts:
        cursor /= part
        if not cursor.exists():
            need(absent, "missing path")
            break
        need(not cursor.is_symlink(), "symlink path")
    return path


def regular(path: Path, label: str, maximum: int = 128 << 20) -> bytes:
    absolute = workspace(path)
    before = absolute.lstat()
    need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1
         and 0 < before.st_size <= maximum, label + ":regular")
    raw = absolute.read_bytes()
    after = absolute.lstat()
    need((before.st_dev, before.st_ino, before.st_mode, before.st_nlink,
          before.st_size, before.st_mtime_ns, before.st_ctime_ns)
         == (after.st_dev, after.st_ino, after.st_mode, after.st_nlink,
             after.st_size, after.st_mtime_ns, after.st_ctime_ns), label + ":TOCTOU")
    return raw


def file_sha(path: Path, label: str) -> str:
    return hashlib.sha256(regular(path, label)).hexdigest()


def strict_raw(raw: bytes, label: str) -> dict[str, Any]:
    need(raw.endswith(b"\n") and not raw.endswith(b"\n\n"), label + ":newline")
    value = json.loads(raw[:-1], object_pairs_hook=pairs,
                       parse_constant=lambda token: (_ for _ in ()).throw(Reject(token)))
    need(type(value) is dict and canonical(value) == raw[:-1], label + ":canonical")
    return value


def document(path: Path, label: str, closure: str | None = None) -> dict[str, Any]:
    value = strict_raw(regular(path, label), label)
    if closure is not None:
        body = dict(value)
        claimed = body.pop(closure, None)
        need(valid_sha(claimed) and claimed == digest(body), label + ":closure")
    return value


def parse_manifest(root: Path, path: Path, label: str) -> dict[str, str]:
    raw = regular(path, label)
    need(raw.endswith(b"\n") and not raw.endswith(b"\n\n"), label + ":newline")
    result: dict[str, str] = {}
    for row in raw.decode("ascii").splitlines():
        fields = row.split("  ", 1)
        need(len(fields) == 2 and valid_sha(fields[0]) and fields[1] not in result,
             label + ":row")
        need(file_sha(root / fields[1], label + ":" + fields[1]) == fields[0],
             label + ":member")
        result[fields[1]] = fields[0]
    return result


def run_adapter(adapter: Path, chain: Path, pins: Path) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        ["/usr/bin/python3", "-I", "-B", os.fspath(adapter),
         "--chain-dir", os.fspath(chain), "--dynamic-pins", os.fspath(pins)],
        stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        env={"HOME": "/nonexistent", "LC_ALL": "C.UTF-8", "TZ": "UTC", "PYTHONHASHSEED": "0"},
        timeout=600, check=False,
    )


def systemd_identity(status: dict[str, Any]) -> dict[str, Any]:
    completed = subprocess.run(
        ["/usr/bin/systemctl", "--user", "show", status["unit"],
         "--property=LoadState,ActiveState,SubState,Result,ExecMainStatus,ExecMainCode,ExecMainPID,InvocationID"],
        stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        timeout=30, check=False,
    )
    need(completed.returncode == 0 and completed.stderr == b"", "systemd unit query")
    facts = dict(line.split("=", 1) for line in completed.stdout.decode("ascii").splitlines() if "=" in line)
    need(facts.get("LoadState") == "loaded" and facts.get("ActiveState") == "active"
         and facts.get("SubState") == "exited" and facts.get("Result") == "success"
         and facts.get("ExecMainStatus") == "0" and facts.get("ExecMainCode") == "1"
         and facts.get("InvocationID") == status["InvocationID"]
         and facts.get("ExecMainPID") == str(status["ExecMainPID"]), "systemd exact identity")
    return facts


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.write_bytes(canonical(value) + b"\n")
    os.chmod(path, 0o600)


def mutate_json(path: Path, field: str, mutate: Callable[[dict[str, Any]], None]) -> None:
    value = document(path, "mutation input")
    mutate(value)
    write_json(path, close(value, field))


def negative_tests(
    adapter: Path, chain: Path, ledger: Path, pins: dict[str, Any], work_raw: Path,
) -> list[str]:
    work = workspace(work_raw, absent=True)
    need(not work.exists() and work.parent.exists(), "fresh negative work")
    work.mkdir(mode=0o700)
    rejected: list[str] = []

    def execute(name: str, pin_value: dict[str, Any], attack_chain: Path) -> None:
        pin_path = work / (name + ".json")
        write_json(pin_path, close(pin_value, "pins_sha256"))
        completed = run_adapter(adapter, attack_chain, pin_path)
        need(completed.returncode == 2 and completed.stdout == b""
             and completed.stderr.startswith(b"REJECT:"),
             "negative rejected:" + name)
        rejected.append(name)

    try:
        direct = (
            ("schema", lambda value: value.__setitem__("schema", "cm2.attack")),
            ("stale_adapter", lambda value: value.__setitem__("adapter_sha256", "0" * 64)),
            ("stale_builder", lambda value: value.__setitem__("release_builder_sha256", "1" * 64)),
        )
        for name, mutation in direct:
            value = copy.deepcopy(pins)
            mutation(value)
            execute(name, value, chain)

        graph_attacks = ("marker", "pid", "invocation", "manifest", "object", "ledger")
        for name in graph_attacks:
            attack_root = work / (name + "-graph")
            attack_chain = attack_root / "chain"
            attack_ledger = attack_root / "ledger"
            shutil.copytree(chain, attack_chain)
            shutil.copytree(ledger, attack_ledger)
            value = copy.deepcopy(pins)
            value["chain_dir"] = attack_chain.relative_to(ROOT).as_posix()
            value["chain_dir_basename"] = attack_chain.name
            value["ledger_dir"] = attack_ledger.relative_to(ROOT).as_posix()
            if name == "marker":
                (attack_chain / "PASS.lock").write_bytes(b"PASS_ATTACK\n")
            elif name in {"pid", "invocation"}:
                path = attack_chain / "chain_status.json"
                field = "ExecMainPID" if name == "pid" else "InvocationID"
                replacement: Any = 2 if name == "pid" else "0" * 32
                mutate_json(path, "chain_status_sha256", lambda item, f=field, r=replacement: item.__setitem__(f, r))
                value["required_members_sha256"]["chain_status.json"] = file_sha(path, name + " status")
                value["chain_status_object_sha256"] = document(path, name + " status object", "chain_status_sha256")["chain_status_sha256"]
            elif name == "manifest":
                path = attack_chain / "payload_manifest.sha256"
                path.write_bytes(regular(path, "manifest attack") + b"0" * 64 + b"  payload/attack\n")
                value["required_members_sha256"]["payload_manifest.sha256"] = file_sha(path, "attacked manifest")
            elif name == "object":
                path = attack_chain / "terminal_replay.json"
                mutate_json(path, "terminal_replay_sha256", lambda item: item.__setitem__("source_W_formal_remainder", 59))
                value["required_members_sha256"]["terminal_replay.json"] = file_sha(path, "attacked replay")
                value["terminal_replay_object_sha256"] = document(path, "attacked replay object", "terminal_replay_sha256")["terminal_replay_sha256"]
            elif name == "ledger":
                path = attack_ledger / "source_w_formal_ledger.json"
                mutate_json(path, "object_sha256", lambda item: item.__setitem__("formal_coverage_numerator", 76_775))
                value["ledger_members_sha256"]["source_w_formal_ledger.json"] = file_sha(path, "attacked ledger")
                value["formal_ledger_object_sha256"] = document(path, "attacked ledger object", "object_sha256")["object_sha256"]
            execute(name, value, attack_chain)
            shutil.rmtree(attack_root)
    finally:
        shutil.rmtree(work, ignore_errors=True)
    need(rejected == ["schema", "stale_adapter", "stale_builder", "marker", "pid", "invocation", "manifest", "object", "ledger"],
         "negative registry exact")
    return rejected


def verify(args: argparse.Namespace) -> dict[str, Any]:
    adapter = workspace(args.adapter)
    chain = workspace(args.chain_dir)
    pins_path = workspace(args.dynamic_pins)
    need(valid_sha(args.adapter_sha256) and file_sha(adapter, "adapter source") == args.adapter_sha256,
         "adapter SHA pin")
    need(valid_sha(args.dynamic_pins_sha256)
         and file_sha(pins_path, "dynamic pins") == args.dynamic_pins_sha256, "dynamic pins SHA pin")
    completed = run_adapter(adapter, chain, pins_path)
    need(completed.returncode == 0 and completed.stderr == b""
         and completed.stdout.count(b"\n") == 1, "adapter canonical execution")
    projection = strict_raw(completed.stdout, "adapter projection")
    projection_body = dict(projection)
    projection_sha = projection_body.pop("projection_sha256", None)
    need(projection_sha == digest(projection_body)
         and set(projection) == {"schema", "status", "authority", "formal_handoff", "release_boundary", "projection_sha256"}
         and projection["schema"] == PROJECTION_SCHEMA and projection["status"] == PROJECTION_STATUS,
         "projection exact schema/closure")
    authority = projection["authority"]
    need(set(authority) == {
        "adapter_contract", "chain_dir_basename", "dynamic_pins_sha256",
        "required_members_sha256", "payload_manifest_member_count",
        "root_manifest_member_count", "root_binds_payload_manifest",
        "root_binds_outer_verification", "payload_all_members_verified",
        "all_receipt_object_hashes_closed", "terminal_seal_exact_pass",
        "terminal_replay_exact_pass", "chain_status_exact_pass",
    } and authority["adapter_contract"] == "DIRECT_VERSIONED_C30D_TERMINAL_GRAPH__NO_LEGACY_SEALED_ALIAS"
       and authority["chain_dir_basename"] == chain.name
       and authority["dynamic_pins_sha256"] == args.dynamic_pins_sha256
       and authority["root_manifest_member_count"] == 2
       and all(authority[key] is True for key in (
           "root_binds_payload_manifest", "root_binds_outer_verification",
           "payload_all_members_verified", "all_receipt_object_hashes_closed",
           "terminal_seal_exact_pass", "terminal_replay_exact_pass", "chain_status_exact_pass",
       )), "projection authority exact")
    need(projection["formal_handoff"] == {
        "before": PROJECTION_BEFORE, "credit": CREDIT, "after": AFTER,
        "transition_status": TERMINAL_STATUS,
        "terminal_replay_authorizes_transition": True,
    }, "projection formal handoff")
    need(projection["release_boundary"] == {
        "C30d_formal_terminal_pass": True, "C30e_candidate_created": False,
        "C30e_manifest_created": False, "C30e_terminal_created": False,
        "source_W_formal_remainder": 58,
        "source_W_transition_authorized_by_this_projection": False,
        "formal_credit": ZERO_C30E,
        "D02": "BLOCKED_COMPOSITE", "D03": "UNAUTHORIZED",
        "D04": "NOT_MINTED", "Gate5": "10/18", "CM2": "NO-GO_FOR_CLAIM",
    }, "projection zero-credit release boundary")

    pins = document(pins_path, "pins independent", "pins_sha256")
    need(pins["schema"] == PIN_SCHEMA and pins["chain_dir"] == chain.relative_to(ROOT).as_posix()
         and pins["adapter_sha256"] == args.adapter_sha256, "independent pins identities")
    required = pins["required_members_sha256"]
    need(required == authority["required_members_sha256"] and set(required) == set(REQUIRED),
         "independent required member map")
    for name in REQUIRED:
        need(file_sha(chain / name, "independent terminal:" + name) == required[name],
             "independent terminal hash:" + name)
    payload = parse_manifest(chain, chain / "payload_manifest.sha256", "independent payload")
    root = parse_manifest(chain, chain / "root_manifest.sha256", "independent root")
    need(len(payload) == authority["payload_manifest_member_count"]
         and root == {"outer_verification.json": required["outer_verification.json"],
                      "payload_manifest.sha256": required["payload_manifest.sha256"]},
         "independent manifests")
    closure_specs = {
        "chain_status.json": "chain_status_sha256",
        "evidence_bundle_receipt.json": "evidence_bundle_sha256",
        "manifest_receipt.json": "manifest_receipt_sha256",
        "outer_verification.json": "outer_verification_sha256",
        "terminal_replay.json": "terminal_replay_sha256",
        "terminal_seal_receipt.json": "terminal_seal_receipt_sha256",
    }
    documents = {name: document(chain / name, "independent:" + name, field)
                 for name, field in closure_specs.items()}
    status = documents["chain_status.json"]
    replay = documents["terminal_replay.json"]
    need(status["status"] == CHAIN_STATUS and replay["status"] == TERMINAL_STATUS
         and status["terminal_replay_object_sha256"] == replay["terminal_replay_sha256"]
         and status["source_W_formal_remainder"] == 58, "independent terminal status")
    ledger = workspace(Path(pins["ledger_dir"]))
    ledger_pins = pins["ledger_members_sha256"]
    need(set(ledger_pins) == set(LEDGER_MEMBERS), "independent ledger member map")
    for name in LEDGER_MEMBERS:
        need(file_sha(ledger / name, "independent ledger:" + name) == ledger_pins[name],
             "independent ledger hash:" + name)
    formal = document(ledger / "source_w_formal_ledger.json", "independent formal", "object_sha256")
    application = document(ledger / "application_receipt.json", "independent application", "object_sha256")
    hostile = document(ledger / "hostile_audit.json", "independent hostile", "object_sha256")
    need(formal["status"] == "PASS_CONSOLIDATED_SOURCE_W_FORMAL_LEDGER__REMAINDER_58"
         and formal["current_state"] == AFTER and len(formal["transitions"]) == 2
         and formal["transitions"][-1]["terminal_replay_object_sha256"] == replay["terminal_replay_sha256"]
         and application["source_W_transition_authorized"] is True
         and application["ledger_object_sha256"] == formal["object_sha256"]
         and hostile["negative_test_count"] == 9, "independent formal ledger")
    unit = systemd_identity(status)
    rejected = negative_tests(adapter, chain, ledger, pins, args.work_dir)
    return close({
        "schema": "cm2.round306c30d.v3-terminal-consumer-independent-audit.v1",
        "status": "PASS_C30D_V3_TERMINAL_ADAPTER_AND_FORMAL_LEDGER_INDEPENDENT_AUDIT",
        "adapter_sha256": args.adapter_sha256,
        "dynamic_pins_sha256": args.dynamic_pins_sha256,
        "projection_sha256": projection_sha,
        "chain_status_object_sha256": status["chain_status_sha256"],
        "terminal_replay_object_sha256": replay["terminal_replay_sha256"],
        "formal_ledger_object_sha256": formal["object_sha256"],
        "payload_manifest_member_count": len(payload),
        "terminal_required_member_count": len(REQUIRED),
        "systemd_unit_identity": unit,
        "negative_test_count": len(rejected),
        "rejected_attacks": rejected,
        "source_W_transition": {"before": 78, "after": 58},
        "source_W_formal_remainder": 58,
        "D02": "BLOCKED_COMPOSITE", "D03": "UNAUTHORIZED",
        "D04": "NOT_MINTED", "Gate5": "10/18", "CM2": "NO-GO_FOR_CLAIM",
    }, "audit_sha256")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--adapter", type=Path, required=True)
    parser.add_argument("--adapter-sha256", required=True)
    parser.add_argument("--chain-dir", type=Path, required=True)
    parser.add_argument("--dynamic-pins", type=Path, required=True)
    parser.add_argument("--dynamic-pins-sha256", required=True)
    parser.add_argument("--work-dir", type=Path, required=True)
    arguments = parser.parse_args()
    try:
        output = verify(arguments)
    except (Reject, OSError, ValueError, TypeError, KeyError, AssertionError,
            json.JSONDecodeError, subprocess.SubprocessError) as error:
        print("REJECT:" + type(error).__name__ + ":" + str(error), file=sys.stderr)
        return 2
    print(canonical(output).decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
