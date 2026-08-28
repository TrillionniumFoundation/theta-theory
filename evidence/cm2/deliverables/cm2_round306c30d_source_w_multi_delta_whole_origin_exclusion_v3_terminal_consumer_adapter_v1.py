#!/usr/bin/env python3
"""Consume the exact C30d-v3 terminal graph as the C30e predecessor.

The adapter accepts a fresh dynamic pin document, replays every terminal and
formal-ledger byte, verifies both manifests and every object closure, and emits
only the six-key projection required by the C30e-v2 producer.  It grants no
C30e credit.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import stat
import sys
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
SELF = Path(__file__).resolve()
BUILDER = ROOT / "deliverables/cm2_round306c30d_source_w_multi_delta_whole_origin_exclusion_v3_release_chain_builder_v1.py"
PIN_SCHEMA = "cm2.round306c30d.v3-terminal-consumer-dynamic-pins.v1"
PIN_STATUS = "PASS_C30D_V3_TERMINAL_AND_FORMAL_LEDGER_DYNAMIC_PINS"
PROJECTION_SCHEMA = "cm2.round306c30e.c30d-terminal-predecessor-projection.v1"
PROJECTION_STATUS = (
    "PASS_EXACT_VERSIONED_C30D_TERMINAL_GRAPH_AS_C30E_PREDECESSOR__"
    "ZERO_C30E_FORMAL_CREDIT"
)
TERMINAL_STATUS = "PASS_FORMAL_C30D_TERMINAL__78_TO_58_AUTHORIZED"
CHAIN_STATUS = "PASS_C30D_V3_TERMINAL_BYTE_REPLAY__FORMAL_SOURCE_W_78_TO_58"
REQUIRED = tuple(sorted((
    "chain_status.json",
    "evidence_bundle_receipt.json",
    "manifest_receipt.json",
    "outer_verification.json",
    "payload_manifest.sha256",
    "root_manifest.sha256",
    "terminal_replay.json",
    "terminal_seal_receipt.json",
)))
LEDGER_MEMBERS = tuple(sorted((
    "PASS.lock", "application_receipt.json", "hostile_audit.json",
    "root_manifest.sha256", "source_w_formal_ledger.json",
)))
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
    "outgoing_H_cell_dispositions": 0,
    "strict_LIVE_cell_dispositions": 0,
    "resolved_source_W_origin_dispositions": 0,
    "resolved_nonexcluded": 0,
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
    need(field not in value, "closure field absent")
    return {**value, field: digest(value)}


def strict_pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in items:
        need(key not in result, "duplicate JSON key:" + key)
        result[key] = value
    return result


def workspace(raw: Path, *, absent: bool = False) -> Path:
    supplied = raw if raw.is_absolute() else ROOT / raw
    path = Path(os.path.abspath(os.fspath(supplied)))
    try:
        relative = path.relative_to(ROOT)
    except ValueError as error:
        raise Reject("outside workspace:" + os.fspath(raw)) from error
    need(relative.parts and all(part not in {"", ".", ".."} for part in relative.parts), "canonical path")
    cursor = ROOT
    for part in relative.parts:
        cursor /= part
        if not cursor.exists():
            need(absent, "missing path:" + os.fspath(cursor))
            break
        need(not cursor.is_symlink(), "symlink path:" + os.fspath(cursor))
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


def file_sha(path: Path, label: str, maximum: int = 128 << 20) -> str:
    return hashlib.sha256(regular(path, label, maximum)).hexdigest()


def strict_json(path: Path, label: str, closure: str | None = None) -> dict[str, Any]:
    raw = regular(path, label)
    need(raw.endswith(b"\n") and not raw.endswith(b"\n\n"), label + ":newline")
    value = json.loads(raw[:-1], object_pairs_hook=strict_pairs,
                       parse_constant=lambda token: (_ for _ in ()).throw(Reject(token)))
    need(type(value) is dict and canonical(value) == raw[:-1], label + ":canonical")
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
        need(len(fields) == 2 and valid_sha(fields[0]), label + ":row")
        name = fields[1]
        need(name not in result and not name.startswith("/")
             and ".." not in Path(name).parts, label + ":path")
        member = root / name
        need(file_sha(member, label + ":" + name) == fields[0], label + ":member SHA")
        result[name] = fields[0]
    need(bool(result), label + ":nonempty")
    return result


def exact_state(value: Any, expected: dict[str, Any], label: str) -> None:
    need(value == expected, label + ":exact")
    need(value["excluded"] + value["conservative_live"] == value["total"]
         and value["resolved_nonexcluded"] + value["remaining"] == value["conservative_live"]
         and sum(value["remaining_partition"].values()) == value["remaining"],
         label + ":conservation")


def make_pins(chain_raw: Path, ledger_raw: Path, output_raw: Path) -> dict[str, Any]:
    chain = workspace(chain_raw)
    ledger = workspace(ledger_raw)
    output = workspace(output_raw, absent=True)
    need(not output.exists() and output.parent.exists(), "fresh pins output")
    need({entry.name for entry in os.scandir(chain)} == set(REQUIRED) | {"PASS.lock", "payload"}, "chain exact top-level")
    need(regular(chain / "PASS.lock", "chain PASS marker") == (CHAIN_STATUS + "\n").encode("ascii"), "chain exact PASS marker")
    need({entry.name for entry in os.scandir(ledger)} == set(LEDGER_MEMBERS), "ledger exact members")
    required = {name: file_sha(chain / name, "pin chain:" + name) for name in REQUIRED}
    ledger_members = {name: file_sha(ledger / name, "pin ledger:" + name) for name in LEDGER_MEMBERS}
    replay = strict_json(chain / "terminal_replay.json", "pin replay", "terminal_replay_sha256")
    status = strict_json(chain / "chain_status.json", "pin status", "chain_status_sha256")
    formal = strict_json(ledger / "source_w_formal_ledger.json", "pin formal ledger", "object_sha256")
    pins = close({
        "schema": PIN_SCHEMA,
        "status": PIN_STATUS,
        "chain_dir": chain.relative_to(ROOT).as_posix(),
        "chain_dir_basename": chain.name,
        "ledger_dir": ledger.relative_to(ROOT).as_posix(),
        "adapter_sha256": file_sha(SELF, "adapter source", 8 << 20),
        "release_builder_sha256": file_sha(BUILDER, "release builder source", 8 << 20),
        "required_members_sha256": required,
        "ledger_members_sha256": ledger_members,
        "terminal_replay_object_sha256": replay["terminal_replay_sha256"],
        "chain_status_object_sha256": status["chain_status_sha256"],
        "formal_ledger_object_sha256": formal["object_sha256"],
        "source_W_formal_remainder": 58,
    }, "pins_sha256")
    output.write_bytes(canonical(pins) + b"\n")
    os.chmod(output, 0o600)
    return {
        "schema": "cm2.round306c30d.v3-terminal-consumer-pin-builder-receipt.v1",
        "status": PIN_STATUS,
        "dynamic_pins": output.relative_to(ROOT).as_posix(),
        "dynamic_pins_file_sha256": file_sha(output, "written pins"),
        "dynamic_pins_object_sha256": pins["pins_sha256"],
    }


def consume(chain_raw: Path, pins_raw: Path) -> dict[str, Any]:
    chain = workspace(chain_raw)
    pins_path = workspace(pins_raw)
    pins_file_sha = file_sha(pins_path, "dynamic pins")
    pins = strict_json(pins_path, "dynamic pins", "pins_sha256")
    need(set(pins) == {
        "schema", "status", "chain_dir", "chain_dir_basename", "ledger_dir",
        "adapter_sha256", "release_builder_sha256", "required_members_sha256",
        "ledger_members_sha256", "terminal_replay_object_sha256",
        "chain_status_object_sha256", "formal_ledger_object_sha256",
        "source_W_formal_remainder", "pins_sha256",
    }, "pins exact schema")
    need(pins["schema"] == PIN_SCHEMA and pins["status"] == PIN_STATUS
         and pins["chain_dir"] == chain.relative_to(ROOT).as_posix()
         and pins["chain_dir_basename"] == chain.name
         and pins["adapter_sha256"] == file_sha(SELF, "adapter self", 8 << 20)
         and pins["release_builder_sha256"] == file_sha(BUILDER, "builder source", 8 << 20)
         and pins["source_W_formal_remainder"] == 58, "pins exact identities")
    required = pins["required_members_sha256"]
    need(type(required) is dict and set(required) == set(REQUIRED)
         and all(valid_sha(value) for value in required.values()), "required member pins")
    need({entry.name for entry in os.scandir(chain)} == set(REQUIRED) | {"PASS.lock", "payload"}, "chain exact top-level")
    need(regular(chain / "PASS.lock", "chain PASS marker")
         == (CHAIN_STATUS + "\n").encode("ascii"),
         "chain exact PASS marker")
    for name in REQUIRED:
        need(file_sha(chain / name, "terminal member:" + name) == required[name], "terminal member pin:" + name)

    payload = parse_manifest(chain, chain / "payload_manifest.sha256", "payload manifest")
    root = parse_manifest(chain, chain / "root_manifest.sha256", "root manifest")
    need(root == {
        "outer_verification.json": required["outer_verification.json"],
        "payload_manifest.sha256": required["payload_manifest.sha256"],
    }, "root exact two-member binding")
    evidence = strict_json(chain / "evidence_bundle_receipt.json", "evidence", "evidence_bundle_sha256")
    manifest_receipt = strict_json(chain / "manifest_receipt.json", "manifest receipt", "manifest_receipt_sha256")
    outer = strict_json(chain / "outer_verification.json", "outer", "outer_verification_sha256")
    seal = strict_json(chain / "terminal_seal_receipt.json", "seal", "terminal_seal_receipt_sha256")
    replay = strict_json(chain / "terminal_replay.json", "replay", "terminal_replay_sha256")
    status = strict_json(chain / "chain_status.json", "chain status", "chain_status_sha256")
    need(evidence.get("status") == "PASS_C30D_V3_DUAL_SEED_VERIFICATION_AND_26_ATTACK_EVIDENCE"
         and evidence.get("dual_seed_byte_identical") is True
         and evidence.get("seed_count") == 2
         and evidence.get("coherent_attack_count") == 26, "evidence exact pass")
    need(manifest_receipt.get("status") == "PASS_C30D_V3_PAYLOAD_MANIFEST_ALL_MEMBERS_VERIFIED"
         and manifest_receipt.get("payload_manifest_sha256") == required["payload_manifest.sha256"]
         and manifest_receipt.get("payload_manifest_member_count") == len(payload)
         and manifest_receipt.get("payload_members") == sorted(payload)
         and manifest_receipt.get("all_members_verified") is True, "manifest receipt exact pass")
    need(outer.get("status") == "PASS_C30D_V3_OUTER_VERIFICATION__78_TO_58_READY_FOR_TERMINAL"
         and outer.get("payload_manifest_sha256") == required["payload_manifest.sha256"]
         and outer.get("manifest_receipt_sha256") == manifest_receipt["manifest_receipt_sha256"]
         and outer.get("before") == BEFORE and outer.get("credit") == CREDIT
         and outer.get("after") == AFTER and outer.get("conservation_verified") is True
         and outer.get("dual_seed_byte_replayed") is True, "outer exact pass")
    need(seal.get("status") == "PASS_C30D_V3_EXACT_TERMINAL_SEAL__78_TO_58"
         and seal.get("terminal_status") == TERMINAL_STATUS
         and seal.get("outer_verification_sha256") == outer["outer_verification_sha256"]
         and seal.get("manifest_receipt_sha256") == manifest_receipt["manifest_receipt_sha256"]
         and seal.get("payload_manifest_sha256") == required["payload_manifest.sha256"]
         and seal.get("root_manifest_sha256") == required["root_manifest.sha256"]
         and seal.get("before") == BEFORE and seal.get("credit") == CREDIT
         and seal.get("after") == AFTER and seal.get("all_receipt_object_hashes_closed") is True
         and seal.get("all_payload_members_verified") is True, "terminal seal exact pass")
    replay_members = replay.get("required_member_sha256")
    need(replay.get("status") == TERMINAL_STATUS
         and type(replay_members) is dict
         and replay_members == {name: required[name] for name in (
             "evidence_bundle_receipt.json", "manifest_receipt.json",
             "outer_verification.json", "payload_manifest.sha256",
             "root_manifest.sha256", "terminal_seal_receipt.json",
         )}
         and replay.get("terminal_seal_receipt_sha256") == seal["terminal_seal_receipt_sha256"]
         and replay.get("before") == BEFORE and replay.get("credit") == CREDIT
         and replay.get("after") == AFTER and replay.get("all_bytes_replayed") is True
         and replay.get("C30d_transition_authorized") is True
         and replay.get("source_W_formal_remainder") == 58, "terminal replay exact pass")
    need(status.get("status") == CHAIN_STATUS and status.get("terminal_status") == TERMINAL_STATUS
         and status.get("terminal_replay_file_sha256") == required["terminal_replay.json"]
         and status.get("terminal_replay_object_sha256") == replay["terminal_replay_sha256"]
         and status.get("terminal_seal_file_sha256") == required["terminal_seal_receipt.json"]
         and status.get("terminal_seal_object_sha256") == seal["terminal_seal_receipt_sha256"]
         and status.get("source_W_transition") == {"before": 78, "after": 58}
         and status.get("source_W_transition_authorized") is True
         and status.get("source_W_formal_remainder") == 58
         and pins["terminal_replay_object_sha256"] == replay["terminal_replay_sha256"]
         and pins["chain_status_object_sha256"] == status["chain_status_sha256"], "chain status exact pass")
    process = evidence.get("process_attestation")
    need(type(process) is dict
         and process.get("publication_token") == status.get("publication_token")
         and process.get("unit") == status.get("unit")
         and process.get("InvocationID") == status.get("InvocationID")
         and process.get("ExecMainPID") == status.get("ExecMainPID")
         and type(process.get("ExecMainPID")) is int and process["ExecMainPID"] > 1,
         "publication process identity closure")

    ledger = workspace(Path(pins["ledger_dir"]))
    ledger_pins = pins["ledger_members_sha256"]
    need(type(ledger_pins) is dict and set(ledger_pins) == set(LEDGER_MEMBERS)
         and {entry.name for entry in os.scandir(ledger)} == set(LEDGER_MEMBERS), "ledger exact member set")
    for name in LEDGER_MEMBERS:
        need(file_sha(ledger / name, "formal ledger member:" + name) == ledger_pins[name], "formal ledger member pin:" + name)
    need(regular(ledger / "PASS.lock", "formal ledger PASS marker")
         == b"PASS_C30D_FORMAL_SOURCE_W_LEDGER__REMAINDER_58\n",
         "formal ledger exact PASS marker")
    ledger_root = parse_manifest(ledger, ledger / "root_manifest.sha256", "formal ledger root")
    need(set(ledger_root) == {"application_receipt.json", "hostile_audit.json", "source_w_formal_ledger.json"}, "formal ledger root exact")
    formal = strict_json(ledger / "source_w_formal_ledger.json", "formal ledger", "object_sha256")
    application = strict_json(ledger / "application_receipt.json", "formal application", "object_sha256")
    audit = strict_json(ledger / "hostile_audit.json", "formal hostile audit", "object_sha256")
    exact_state(formal.get("current_state"), AFTER, "formal current state")
    need(formal.get("schema") == "cm2.source-w.consolidated-formal-ledger.v1"
         and formal.get("status") == "PASS_CONSOLIDATED_SOURCE_W_FORMAL_LEDGER__REMAINDER_58"
         and formal.get("formal_coverage_numerator") == 76_774
         and formal.get("formal_coverage_denominator") == 76_832
         and len(formal.get("transitions", [])) == 2
         and len(formal.get("applied_transition_ids", [])) == 2
         and formal["transitions"][-1].get("before") == BEFORE
         and formal["transitions"][-1].get("after") == AFTER
         and formal["transitions"][-1].get("candidate_result_object_sha256")
         == evidence.get("candidate_result_object_sha256")
         and formal["transitions"][-1].get("terminal_replay_object_sha256") == replay["terminal_replay_sha256"]
         and formal["transitions"][-1].get("chain_status_object_sha256") == status["chain_status_sha256"]
         and pins["formal_ledger_object_sha256"] == formal["object_sha256"], "formal ledger exact transition")
    need(application.get("status") == "PASS_C30D_FORMAL_LEDGER_SINGLE_APPLICATION__SOURCE_W_78_TO_58"
         and application.get("source_W_transition_authorized") is True
         and application.get("source_W_formal_remainder") == 58
         and application.get("ledger_object_sha256") == formal["object_sha256"]
         and application.get("terminal_replay_object_sha256") == replay["terminal_replay_sha256"]
         and application.get("chain_status_object_sha256") == status["chain_status_sha256"]
         and application.get("InvocationID") == status.get("InvocationID")
         and application.get("ExecMainPID") == status.get("ExecMainPID")
         and audit.get("status") == "PASS_C30D_FORMAL_LEDGER_ALL_9_HOSTILE_ATTACKS_REJECTED"
         and audit.get("negative_test_count") == 9, "formal application and hostile audit")
    exact_state(BEFORE, BEFORE, "handoff before")
    exact_state(AFTER, AFTER, "handoff after")

    projection_body = {
        "schema": PROJECTION_SCHEMA,
        "status": PROJECTION_STATUS,
        "authority": {
            "adapter_contract": "DIRECT_VERSIONED_C30D_TERMINAL_GRAPH__NO_LEGACY_SEALED_ALIAS",
            "chain_dir_basename": chain.name,
            "dynamic_pins_sha256": pins_file_sha,
            "required_members_sha256": {name: required[name] for name in REQUIRED},
            "payload_manifest_member_count": len(payload),
            "root_manifest_member_count": len(root),
            "root_binds_payload_manifest": True,
            "root_binds_outer_verification": True,
            "payload_all_members_verified": True,
            "all_receipt_object_hashes_closed": True,
            "terminal_seal_exact_pass": True,
            "terminal_replay_exact_pass": True,
            "chain_status_exact_pass": True,
        },
        "formal_handoff": {
            "before": PROJECTION_BEFORE,
            "credit": CREDIT,
            "after": AFTER,
            "transition_status": TERMINAL_STATUS,
            "terminal_replay_authorizes_transition": True,
        },
        "release_boundary": {
            "C30d_formal_terminal_pass": True,
            "C30e_candidate_created": False,
            "C30e_manifest_created": False,
            "C30e_terminal_created": False,
            "source_W_formal_remainder": 58,
            "source_W_transition_authorized_by_this_projection": False,
            "formal_credit": ZERO_C30E,
            "D02": "BLOCKED_COMPOSITE", "D03": "UNAUTHORIZED",
            "D04": "NOT_MINTED", "Gate5": "10/18", "CM2": "NO-GO_FOR_CLAIM",
        },
    }
    return close(projection_body, "projection_sha256")


def self_test() -> dict[str, Any]:
    exact_state(BEFORE, BEFORE, "fixture before")
    exact_state(AFTER, AFTER, "fixture after")
    need(set(REQUIRED) == set(REQUIRED) and len(REQUIRED) == 8, "required member fixture")
    return {
        "schema": "cm2.round306c30d.v3-terminal-consumer-adapter-self-test.v1",
        "status": "PASS_C30D_V3_TERMINAL_ADAPTER_STATIC_FIXTURES",
        "required_terminal_member_count": 8,
        "source_W_handoff": {"before": 78, "after": 58},
        "C30e_formal_credit": ZERO_C30E,
        "CM2": "NO-GO_FOR_CLAIM",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--chain-dir", type=Path)
    parser.add_argument("--dynamic-pins", type=Path)
    parser.add_argument("--ledger-dir", type=Path)
    parser.add_argument("--dynamic-pins-output", type=Path)
    parser.add_argument("--make-pins", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    arguments = parser.parse_args()
    try:
        if arguments.self_test:
            need(not arguments.make_pins and all(value is None for value in (
                arguments.chain_dir, arguments.dynamic_pins, arguments.ledger_dir,
                arguments.dynamic_pins_output,
            )), "self-test isolation")
            output = self_test()
        elif arguments.make_pins:
            need(arguments.chain_dir is not None and arguments.ledger_dir is not None
                 and arguments.dynamic_pins_output is not None
                 and arguments.dynamic_pins is None, "make-pins arguments")
            output = make_pins(arguments.chain_dir, arguments.ledger_dir, arguments.dynamic_pins_output)
        else:
            need(arguments.chain_dir is not None and arguments.dynamic_pins is not None
                 and arguments.ledger_dir is None and arguments.dynamic_pins_output is None,
                 "consume arguments")
            output = consume(arguments.chain_dir, arguments.dynamic_pins)
    except (Reject, OSError, ValueError, TypeError, KeyError, AssertionError, json.JSONDecodeError) as error:
        print("REJECT:" + type(error).__name__ + ":" + str(error), file=sys.stderr)
        return 2
    print(canonical(output).decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
