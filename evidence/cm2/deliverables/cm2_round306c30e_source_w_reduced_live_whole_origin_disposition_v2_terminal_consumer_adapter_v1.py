#!/usr/bin/env python3
"""Normalize the exact C30e terminal and formal ledger for C30f-v2."""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
from pathlib import Path
import stat
import sys
from types import ModuleType
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
SELF = Path(__file__).resolve()
COMMON_PATH = ROOT / "deliverables/cm2_round306c30d_source_w_multi_delta_whole_origin_exclusion_v3_terminal_consumer_adapter_v1.py"
RELEASE_PATH = ROOT / "deliverables/cm2_round306_source_w_downstream_release_chain_builder_v1.py"


def load_common() -> ModuleType:
    spec = importlib.util.spec_from_file_location("_cm2_c30e_terminal_common", COMMON_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("terminal common import specification")
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

PIN_SCHEMA = "cm2.round306c30e.v2-terminal-consumer-dynamic-pins.v1"
PIN_STATUS = "PASS_C30E_V2_TERMINAL_AND_FORMAL_LEDGER_DYNAMIC_PINS"
PROJECTION_SCHEMA = "cm2.round306c30f.c30e-terminal-predecessor-projection.v1"
PROJECTION_STATUS = (
    "PASS_EXACT_VERSIONED_C30E_TERMINAL_GRAPH_AS_C30F_PREDECESSOR__"
    "ZERO_C30F_FORMAL_CREDIT"
)
TERMINAL_STATUS = "PASS_FORMAL_C30E_TERMINAL__58_TO_56_AUTHORIZED"
CHAIN_STATUS = "PASS_C30E_V2_TERMINAL_BYTE_REPLAY__FORMAL_SOURCE_W_58_TO_56"
REQUIRED = common.REQUIRED
LEDGER_MEMBERS = common.LEDGER_MEMBERS
BEFORE = {
    "excluded": 74_766, "conservative_live": 2_066,
    "resolved_nonexcluded": 2_008, "remaining": 58, "total": 76_832,
    "remaining_partition": {
        "reduced_live": 2, "retained_source_seams": 2, "compact_q": 54,
    },
}
AFTER = {
    "excluded": 74_766, "conservative_live": 2_066,
    "resolved_nonexcluded": 2_010, "remaining": 56, "total": 76_832,
    "remaining_partition": {"retained_source_seams": 2, "compact_q": 54},
}
CREDIT = {
    "resolved_source_W_origin_dispositions": 2,
    "whole_source_W_origin_exclusions": 0,
    "resolved_nonexcluded": 2,
}
ZERO = {
    "target_cell_dispositions": 0, "target_whole_cell_exclusions": 0,
    "source_half_open_stratum_dispositions": 0,
    "resolved_source_W_origin_dispositions": 0,
    "whole_source_W_origin_exclusions": 0, "resolved_nonexcluded": 0,
    "D02": 0, "D03": 0, "D04": 0, "Gate5": 0, "CM2": 0,
}


def make_pins(chain_raw: Path, ledger_raw: Path, output_raw: Path) -> dict[str, Any]:
    chain = workspace(chain_raw)
    ledger = workspace(ledger_raw)
    output = workspace(output_raw, absent=True)
    need(not output.exists() and output.parent.exists(), "fresh C30e pins")
    need({entry.name for entry in os.scandir(chain)} == set(REQUIRED) | {"PASS.lock", "payload"},
         "C30e chain exact top-level")
    need({entry.name for entry in os.scandir(ledger)} == set(LEDGER_MEMBERS),
         "C30e ledger exact members")
    required = {name: file_sha(chain / name, "C30e pin:" + name) for name in REQUIRED}
    ledger_members = {name: file_sha(ledger / name, "C30e ledger pin:" + name)
                      for name in LEDGER_MEMBERS}
    replay = strict_json(chain / "terminal_replay.json", "C30e replay pin", "terminal_replay_sha256")
    status = strict_json(chain / "chain_status.json", "C30e status pin", "chain_status_sha256")
    formal = strict_json(ledger / "source_w_formal_ledger.json", "C30e ledger pin", "object_sha256")
    pins = close({
        "schema": PIN_SCHEMA, "status": PIN_STATUS,
        "chain_dir": chain.relative_to(ROOT).as_posix(),
        "chain_dir_basename": chain.name,
        "ledger_dir": ledger.relative_to(ROOT).as_posix(),
        "adapter_sha256": file_sha(SELF, "C30e adapter source", 8 << 20),
        "common_adapter_sha256": file_sha(COMMON_PATH, "terminal common source", 8 << 20),
        "release_builder_sha256": file_sha(RELEASE_PATH, "downstream release source", 8 << 20),
        "required_members_sha256": required,
        "ledger_members_sha256": ledger_members,
        "terminal_replay_object_sha256": replay["terminal_replay_sha256"],
        "chain_status_object_sha256": status["chain_status_sha256"],
        "formal_ledger_object_sha256": formal["object_sha256"],
        "source_W_formal_remainder": 56,
    }, "pins_sha256")
    output.write_bytes(canonical(pins) + b"\n")
    os.chmod(output, 0o600)
    return {
        "schema": "cm2.round306c30e.v2-terminal-consumer-pin-builder-receipt.v1",
        "status": PIN_STATUS,
        "dynamic_pins": output.relative_to(ROOT).as_posix(),
        "dynamic_pins_file_sha256": file_sha(output, "C30e written pins"),
        "dynamic_pins_object_sha256": pins["pins_sha256"],
    }


def consume(chain_raw: Path, pins_raw: Path) -> dict[str, Any]:
    chain = workspace(chain_raw)
    pins_path = workspace(pins_raw)
    pins_file_sha = file_sha(pins_path, "C30e dynamic pins")
    pins = strict_json(pins_path, "C30e dynamic pins", "pins_sha256")
    need(set(pins) == {
        "schema", "status", "chain_dir", "chain_dir_basename", "ledger_dir",
        "adapter_sha256", "common_adapter_sha256", "release_builder_sha256",
        "required_members_sha256", "ledger_members_sha256",
        "terminal_replay_object_sha256", "chain_status_object_sha256",
        "formal_ledger_object_sha256", "source_W_formal_remainder", "pins_sha256",
    }, "C30e pins exact schema")
    need(pins["schema"] == PIN_SCHEMA and pins["status"] == PIN_STATUS
         and pins["chain_dir"] == chain.relative_to(ROOT).as_posix()
         and pins["chain_dir_basename"] == chain.name
         and pins["adapter_sha256"] == file_sha(SELF, "C30e adapter self", 8 << 20)
         and pins["common_adapter_sha256"] == file_sha(COMMON_PATH, "terminal common", 8 << 20)
         and pins["release_builder_sha256"] == file_sha(RELEASE_PATH, "downstream release", 8 << 20)
         and pins["source_W_formal_remainder"] == 56, "C30e pin identities")
    required = pins["required_members_sha256"]
    need(type(required) is dict and set(required) == set(REQUIRED), "C30e required pins")
    need({entry.name for entry in os.scandir(chain)} == set(REQUIRED) | {"PASS.lock", "payload"},
         "C30e chain exact top-level")
    need(regular(chain / "PASS.lock", "C30e PASS marker")
         == (CHAIN_STATUS + "\n").encode("ascii"), "C30e exact PASS marker")
    for name in REQUIRED:
        need(file_sha(chain / name, "C30e member:" + name) == required[name],
             "C30e member pin:" + name)
    payload = parse_manifest(chain, chain / "payload_manifest.sha256", "C30e payload")
    root = parse_manifest(chain, chain / "root_manifest.sha256", "C30e root")
    need(root == {"outer_verification.json": required["outer_verification.json"],
                  "payload_manifest.sha256": required["payload_manifest.sha256"]},
         "C30e exact root")
    evidence = strict_json(chain / "evidence_bundle_receipt.json", "C30e evidence", "evidence_bundle_sha256")
    manifest_receipt = strict_json(chain / "manifest_receipt.json", "C30e manifest receipt", "manifest_receipt_sha256")
    outer = strict_json(chain / "outer_verification.json", "C30e outer", "outer_verification_sha256")
    seal = strict_json(chain / "terminal_seal_receipt.json", "C30e seal", "terminal_seal_receipt_sha256")
    replay = strict_json(chain / "terminal_replay.json", "C30e replay", "terminal_replay_sha256")
    status = strict_json(chain / "chain_status.json", "C30e status", "chain_status_sha256")
    need(evidence.get("status") == "PASS_C30E_V2_DUAL_SEED_VERIFICATION_AND_ATTACK_EVIDENCE"
         and evidence.get("dual_seed_byte_identical") is True
         and evidence.get("seed_count") == 2 and evidence.get("coherent_attack_count") == 15,
         "C30e evidence pass")
    need(manifest_receipt.get("status") == "PASS_C30E_V2_PAYLOAD_MANIFEST_ALL_MEMBERS_VERIFIED"
         and manifest_receipt.get("payload_manifest_sha256") == required["payload_manifest.sha256"]
         and manifest_receipt.get("payload_manifest_member_count") == len(payload)
         and manifest_receipt.get("payload_members") == sorted(payload)
         and manifest_receipt.get("all_members_verified") is True, "C30e manifest pass")
    need(outer.get("status") == "PASS_C30E_V2_OUTER_VERIFICATION__58_TO_56_READY_FOR_TERMINAL"
         and outer.get("before") == BEFORE and outer.get("credit") == CREDIT
         and outer.get("after") == AFTER and outer.get("conservation_verified") is True
         and outer.get("payload_manifest_sha256") == required["payload_manifest.sha256"],
         "C30e outer pass")
    need(seal.get("status") == "PASS_C30E_V2_EXACT_TERMINAL_SEAL__58_TO_56"
         and seal.get("terminal_status") == TERMINAL_STATUS
         and seal.get("before") == BEFORE and seal.get("credit") == CREDIT
         and seal.get("after") == AFTER
         and seal.get("outer_verification_sha256") == outer["outer_verification_sha256"]
         and seal.get("all_receipt_object_hashes_closed") is True, "C30e seal pass")
    replay_members = replay.get("required_member_sha256")
    replay_names = ("evidence_bundle_receipt.json", "manifest_receipt.json",
                    "outer_verification.json", "payload_manifest.sha256",
                    "root_manifest.sha256", "terminal_seal_receipt.json")
    need(replay.get("status") == TERMINAL_STATUS and type(replay_members) is dict
         and replay_members == {name: required[name] for name in replay_names}
         and replay.get("before") == BEFORE and replay.get("credit") == CREDIT
         and replay.get("after") == AFTER
         and replay.get("C30e_transition_authorized") is True
         and replay.get("source_W_formal_remainder") == 56, "C30e replay pass")
    need(status.get("status") == CHAIN_STATUS and status.get("terminal_status") == TERMINAL_STATUS
         and status.get("terminal_replay_file_sha256") == required["terminal_replay.json"]
         and status.get("terminal_replay_object_sha256") == replay["terminal_replay_sha256"]
         and status.get("source_W_transition") == {"before": 58, "after": 56}
         and status.get("source_W_transition_authorized") is True
         and pins["terminal_replay_object_sha256"] == replay["terminal_replay_sha256"]
         and pins["chain_status_object_sha256"] == status["chain_status_sha256"],
         "C30e status pass")
    process = evidence.get("process_attestation")
    need(type(process) is dict and process.get("unit") == status.get("unit")
         and process.get("InvocationID") == status.get("InvocationID")
         and process.get("ExecMainPID") == status.get("ExecMainPID"),
         "C30e process identity closure")

    ledger = workspace(Path(pins["ledger_dir"]))
    ledger_pins = pins["ledger_members_sha256"]
    need(type(ledger_pins) is dict and set(ledger_pins) == set(LEDGER_MEMBERS)
         and {entry.name for entry in os.scandir(ledger)} == set(LEDGER_MEMBERS),
         "C30e ledger exact members")
    for name in LEDGER_MEMBERS:
        need(file_sha(ledger / name, "C30e formal member:" + name) == ledger_pins[name],
             "C30e formal member pin:" + name)
    need(regular(ledger / "PASS.lock", "C30e ledger marker")
         == b"PASS_C30E_FORMAL_SOURCE_W_LEDGER__REMAINDER_56\n",
         "C30e formal marker")
    ledger_root = parse_manifest(ledger, ledger / "root_manifest.sha256", "C30e ledger root")
    need(set(ledger_root) == {"application_receipt.json", "hostile_audit.json",
                              "source_w_formal_ledger.json"}, "C30e ledger root exact")
    formal = strict_json(ledger / "source_w_formal_ledger.json", "C30e formal ledger", "object_sha256")
    application = strict_json(ledger / "application_receipt.json", "C30e application", "object_sha256")
    audit = strict_json(ledger / "hostile_audit.json", "C30e hostile", "object_sha256")
    exact_state(formal.get("current_state"), AFTER, "C30e formal state")
    need(formal.get("status") == "PASS_CONSOLIDATED_SOURCE_W_FORMAL_LEDGER__REMAINDER_56"
         and formal.get("formal_coverage_numerator") == 76_776
         and len(formal.get("transitions", [])) == 3
         and formal["transitions"][-1].get("before") == BEFORE
         and formal["transitions"][-1].get("after") == AFTER
         and formal["transitions"][-1].get("terminal_replay_object_sha256") == replay["terminal_replay_sha256"]
         and formal["transitions"][-1].get("chain_status_object_sha256") == status["chain_status_sha256"]
         and pins["formal_ledger_object_sha256"] == formal["object_sha256"],
         "C30e formal ledger pass")
    need(application.get("status") == "PASS_C30E_FORMAL_LEDGER_SINGLE_APPLICATION__SOURCE_W_58_TO_56"
         and application.get("source_W_transition_authorized") is True
         and application.get("ledger_object_sha256") == formal["object_sha256"]
         and application.get("terminal_replay_object_sha256") == replay["terminal_replay_sha256"]
         and audit.get("negative_test_count") == 9, "C30e application and hostile pass")
    projection = {
        "schema": PROJECTION_SCHEMA, "status": PROJECTION_STATUS,
        "authority": {
            "adapter_contract": "DIRECT_VERSIONED_C30E_TERMINAL_GRAPH__NO_LEGACY_ALIAS",
            "chain_dir_basename": chain.name, "dynamic_pins_sha256": pins_file_sha,
            "required_members_sha256": {name: required[name] for name in REQUIRED},
            "payload_manifest_member_count": len(payload),
            "root_manifest_member_count": len(root),
            "root_binds_payload_manifest": True, "root_binds_outer_verification": True,
            "payload_all_members_verified": True, "all_receipt_object_hashes_closed": True,
            "terminal_seal_exact_pass": True, "terminal_replay_exact_pass": True,
            "chain_status_exact_pass": True,
        },
        "formal_handoff": {
            "before": BEFORE, "credit": CREDIT, "after": AFTER,
            "transition_status": TERMINAL_STATUS,
            "terminal_replay_authorizes_transition": True,
        },
        "release_boundary": {
            "C30e_formal_terminal_pass": True, "C30f_candidate_created": False,
            "C30f_manifest_created": False, "C30f_terminal_created": False,
            "source_W_formal_remainder": 56,
            "source_W_transition_authorized_by_this_projection": False,
            "formal_credit": ZERO,
            "D02": "BLOCKED_COMPOSITE", "D03": "UNAUTHORIZED",
            "D04": "NOT_MINTED", "Gate5": "10/18", "CM2": "NO-GO_FOR_CLAIM",
        },
    }
    return close(projection, "projection_sha256")


def self_test() -> dict[str, Any]:
    exact_state(BEFORE, BEFORE, "C30e fixture before")
    exact_state(AFTER, AFTER, "C30e fixture after")
    return {
        "schema": "cm2.round306c30e.v2-terminal-consumer-adapter-self-test.v1",
        "status": "PASS_C30E_V2_TERMINAL_ADAPTER_STATIC_FIXTURES",
        "source_W_handoff": {"before": 58, "after": 56},
        "required_terminal_member_count": 8, "CM2": "NO-GO_FOR_CLAIM",
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
                arguments.dynamic_pins_output)), "self-test isolation")
            output = self_test()
            print(canonical(output).decode("ascii"))
        elif arguments.make_pins:
            need(arguments.chain_dir is not None and arguments.ledger_dir is not None
                 and arguments.dynamic_pins_output is not None and arguments.dynamic_pins is None,
                 "make-pins arguments")
            output = make_pins(arguments.chain_dir, arguments.ledger_dir,
                               arguments.dynamic_pins_output)
            print(canonical(output).decode("ascii"))
        else:
            need(arguments.chain_dir is not None and arguments.dynamic_pins is not None
                 and arguments.ledger_dir is None and arguments.dynamic_pins_output is None,
                 "consume arguments")
            output = consume(arguments.chain_dir, arguments.dynamic_pins)
            os.write(1, canonical(output))
    except (Reject, OSError, ValueError, TypeError, KeyError, AssertionError,
            RuntimeError, json.JSONDecodeError) as error:
        print("REJECT:" + type(error).__name__ + ":" + str(error), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
