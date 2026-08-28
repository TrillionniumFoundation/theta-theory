#!/usr/bin/env python3
"""Release C30e or C30f candidates into an acyclic terminal and formal ledger."""

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
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
BASE_PATH = ROOT / "deliverables/cm2_round306c30d_source_w_multi_delta_whole_origin_exclusion_v3_release_chain_builder_v1.py"


def load_base() -> ModuleType:
    specification = importlib.util.spec_from_file_location("_cm2_source_w_release_base", BASE_PATH)
    if specification is None or specification.loader is None:
        raise RuntimeError("release base import specification")
    module = importlib.util.module_from_spec(specification)
    sys.modules[specification.name] = module
    specification.loader.exec_module(module)
    return module


base = load_base()
Reject = base.Reject
need = base.need
canonical = base.canonical
digest = base.digest
close = base.close
workspace = base.workspace
regular = base.regular
file_sha = base.file_sha
document = base.document
write_json = base.write_json
copy_regular = base.copy_regular
manifest = base.manifest
validate_state = base.validate_state
STRICT = base.STRICT


C30E_BEFORE = {
    "excluded": 74_766, "conservative_live": 2_066,
    "resolved_nonexcluded": 2_008, "remaining": 58, "total": 76_832,
    "remaining_partition": {
        "reduced_live": 2, "retained_source_seams": 2, "compact_q": 54,
    },
}
C30E_AFTER = {
    "excluded": 74_766, "conservative_live": 2_066,
    "resolved_nonexcluded": 2_010, "remaining": 56, "total": 76_832,
    "remaining_partition": {"retained_source_seams": 2, "compact_q": 54},
}
C30F_AFTER = {
    "excluded": 74_768, "conservative_live": 2_064,
    "resolved_nonexcluded": 2_010, "remaining": 54, "total": 76_832,
    "remaining_partition": {"compact_q": 54},
}
C30E_ZERO = {
    "outgoing_H_cell_dispositions": 0, "strict_LIVE_cell_dispositions": 0,
    "resolved_source_W_origin_dispositions": 0, "resolved_nonexcluded": 0,
    "whole_source_W_origin_exclusions": 0,
    "D02": 0, "D03": 0, "D04": 0, "Gate5": 0, "CM2": 0,
}
C30F_ZERO = {
    "target_cell_dispositions": 0, "target_whole_cell_exclusions": 0,
    "source_half_open_stratum_dispositions": 0,
    "resolved_source_W_origin_dispositions": 0,
    "whole_source_W_origin_exclusions": 0, "resolved_nonexcluded": 0,
    "D02": 0, "D03": 0, "D04": 0, "Gate5": 0, "CM2": 0,
}


CONFIGS: dict[str, dict[str, Any]] = {
    "c30e": {
        "round": "C30e", "version": "v2", "sequence": 3,
        "prefix": "cm2_round306c30e_source_w_reduced_live_whole_origin_disposition_v2",
        "files": (
            "cm2_round306c30b_python_flint_runtime_attestation.json",
            "cm2_round306c30e_source_w_reduced_live_whole_origin_disposition_v2_atomic_half_open_owner_ledger.jsonl.gz",
            "cm2_round306c30e_source_w_reduced_live_whole_origin_disposition_v2_h_cell_ledger.jsonl.gz",
            "cm2_round306c30e_source_w_reduced_live_whole_origin_disposition_v2_strict_live_cell_ledger.jsonl.gz",
            "cm2_round306c30e_source_w_reduced_live_whole_origin_disposition_v2_whole_origin_ledger.jsonl.gz",
            "cm2_round306c30e_source_w_reduced_live_whole_origin_disposition_v2_result.json",
        ),
        "result": "cm2_round306c30e_source_w_reduced_live_whole_origin_disposition_v2_result.json",
        "result_schema": "cm2.round306c30e.source-w-reduced-live-whole-origin-disposition.candidate.v2",
        "result_status": "PASS_CANDIDATE_ROUND306C30E_V2_REDUCED_LIVE_DISPOSITION__C30D_TERMINAL_BOUND__ZERO_CREDIT__UNAUTHORIZED_PENDING_RELEASE",
        "transition_key": "proposed_source_W_transition_if_C30e_terminal_replay_passes",
        "transition_after_key": "after",
        "scope_key": "dynamic_scope",
        "before": C30E_BEFORE, "after": C30E_AFTER,
        "credit": {"resolved_source_W_origin_dispositions": 2,
                   "whole_source_W_origin_exclusions": 0,
                   "resolved_nonexcluded": 2},
        "disposition": "RESOLVED_MIXED", "origin_count": 2,
        "zero": C30E_ZERO,
        "verification_schema": "cm2.round306c30e.source-w-reduced-live.independent-verification.candidate.v2",
        "verification_status": "PASS_INDEPENDENT_C30E_V2_CANDIDATE__2_DYNAMIC_ORIGINS__24_REDUCED_LIVE_PLUS_128_H_PER_ORIGIN__BOTH_RESOLVED_MIXED__FORMAL_CREDIT_ZERO",
        "verification_credit": 0,
        "attack_schema": "cm2.round306c30e.source-w-reduced-live.coherent-attack-harness.candidate.v3",
        "attack_status": "PASS_ALL_C30E_V2_COHERENT_ATTACKS_REJECTED",
        "attack_count": 15, "attack_credit": 0,
        "terminal_status": "PASS_FORMAL_C30E_TERMINAL__58_TO_56_AUTHORIZED",
        "chain_status": "PASS_C30E_V2_TERMINAL_BYTE_REPLAY__FORMAL_SOURCE_W_58_TO_56",
        "ledger_status": "PASS_CONSOLIDATED_SOURCE_W_FORMAL_LEDGER__REMAINDER_56",
        "application_status": "PASS_C30E_FORMAL_LEDGER_SINGLE_APPLICATION__SOURCE_W_58_TO_56",
        "provenance": (
            "deliverables/cm2_round306c30e_source_w_reduced_live_whole_origin_disposition_v2_producer.py",
            "deliverables/cm2_round306c30e_source_w_reduced_live_whole_origin_disposition_v2_independent_verifier.py",
            "deliverables/cm2_round306c30e_source_w_reduced_live_whole_origin_disposition_v2_coherent_attack_harness.py",
        ),
    },
    "c30f": {
        "round": "C30f", "version": "v2", "sequence": 4,
        "prefix": "cm2_round306c30f_source_w_retained_physical_seam_whole_origin_exclusion_v2",
        "files": (
            "cm2_round306c30f_source_w_retained_physical_seam_whole_origin_exclusion_v2_result.json",
            "cm2_round306c30f_source_w_retained_physical_seam_whole_origin_exclusion_v2_source_half_open_strata_ledger.jsonl.gz",
            "cm2_round306c30f_source_w_retained_physical_seam_whole_origin_exclusion_v2_target_cell_ledger.jsonl.gz",
            "cm2_round306c30f_source_w_retained_physical_seam_whole_origin_exclusion_v2_whole_origin_ledger.jsonl.gz",
        ),
        "result": "cm2_round306c30f_source_w_retained_physical_seam_whole_origin_exclusion_v2_result.json",
        "result_schema": "cm2.round306c30f.source-w-retained-physical-seam-whole-origin-exclusion.candidate.v2",
        "result_status": "PASS_CANDIDATE_C30F_V2__C30E_TERMINAL_BOUND__2_WHOLE_ORIGINS_EXCLUDED__ZERO_FORMAL_CREDIT",
        "transition_key": "source_W_handoff_candidate",
        "transition_after_key": "after_if_later_terminal_release_passes",
        "scope_key": "dynamic_scope",
        "before": C30E_AFTER, "after": C30F_AFTER,
        "credit": {"resolved_source_W_origin_dispositions": 2,
                   "whole_source_W_origin_exclusions": 2,
                   "resolved_nonexcluded": 0},
        "disposition": "EXCLUDED", "origin_count": 2,
        "zero": C30F_ZERO,
        "verification_schema": "cm2.round306c30f.retained-physical-seam.independent-verification.report.v2",
        "verification_status": "PASS_INDEPENDENT_C30F_V2__C30E_TERMINAL_BOUND__288_TARGETS__994_SOURCE_STRATA__2_EXCLUDED_CANDIDATES__ZERO_FORMAL_CREDIT",
        "verification_credit": {
            "verified_target_cells": 0, "verified_source_atomic_strata": 0,
            "verified_whole_origin_exclusions": 0,
            "D02": 0, "D03": 0, "D04": 0, "Gate5": 0, "CM2": 0,
        },
        "attack_schema": "cm2.round306c30f.retained-physical-seam.coherent-attack-harness.report.v2",
        "attack_status": "PASS_ALL_C30F_V2_COHERENT_CANDIDATE_ATTACKS_REJECTED__ZERO_FORMAL_CREDIT",
        "attack_count": 16,
        "attack_credit": {
            "attack_successes": 0, "target_cell_dispositions": 0,
            "source_strata_dispositions": 0, "whole_origin_exclusions": 0,
            "D02": 0, "D03": 0, "D04": 0, "Gate5": 0, "CM2": 0,
        },
        "terminal_status": "PASS_FORMAL_C30F_TERMINAL__56_TO_54_AUTHORIZED",
        "chain_status": "PASS_C30F_V2_TERMINAL_BYTE_REPLAY__FORMAL_SOURCE_W_56_TO_54",
        "ledger_status": "PASS_CONSOLIDATED_SOURCE_W_FORMAL_LEDGER__REMAINDER_54",
        "application_status": "PASS_C30F_FORMAL_LEDGER_SINGLE_APPLICATION__SOURCE_W_56_TO_54",
        "provenance": (
            "deliverables/cm2_round306c30f_source_w_retained_physical_seam_whole_origin_exclusion_v2_producer.py",
            "deliverables/cm2_round306c30f_source_w_retained_physical_seam_whole_origin_exclusion_v2_independent_verifier.py",
            "deliverables/cm2_round306c30f_source_w_retained_physical_seam_whole_origin_exclusion_v2_coherent_attack_harness.py",
        ),
    },
}


def process_attestation(config: dict[str, Any]) -> dict[str, Any]:
    token = os.environ.get("CM2_PUBLICATION_TOKEN", "")
    unit = os.environ.get("CM2_PUBLICATION_UNIT", "")
    prefix = config["round"].lower() + "-v2-publication-"
    need(re.fullmatch(re.escape(prefix) + r"[a-z0-9-]{16,160}", token) is not None,
         "fresh downstream publication token")
    need(re.fullmatch("cm2-" + re.escape(prefix) + r"[a-z0-9-]{16,160}\.service", unit) is not None,
         "downstream publication unit")
    invocation = os.environ.get("INVOCATION_ID", "")
    need(re.fullmatch(r"[0-9a-f]{32}", invocation) is not None, "downstream InvocationID")
    need(os.environ.get("HOME") == "/nonexistent"
         and os.environ.get("LC_ALL") == "C.UTF-8"
         and os.environ.get("TZ") == "UTC"
         and os.environ.get("PYTHONHASHSEED") == "0", "controlled downstream environment")
    return {
        "publication_token": token, "unit": unit, "InvocationID": invocation,
        "ExecMainPID": os.getpid(), "uid": os.getuid(),
    }


def candidate(config: dict[str, Any], raw: Path) -> tuple[dict[str, Any], dict[str, str]]:
    directory = workspace(raw)
    need(stat.S_ISDIR(directory.lstat().st_mode) and not directory.is_symlink(), "candidate directory")
    names = {entry.name for entry in os.scandir(directory)}
    need(names == set(config["files"]), "candidate exact files")
    hashes = {name: file_sha(directory / name, "candidate:" + name) for name in sorted(names)}
    result = document(directory / config["result"], "candidate result")
    body = dict(result)
    claimed = body.pop("result_sha256", None)
    transition = result.get(config["transition_key"])
    scope = result.get(config["scope_key"])
    need(claimed == digest(body) and result.get("schema") == config["result_schema"]
         and result.get("status") == config["result_status"]
         and result.get("formal_credit") == config["zero"]
         and type(transition) is dict and transition.get("before") == config["before"]
         and transition.get(config["transition_after_key"]) == config["after"]
         and type(scope) is dict and scope.get("origin_count") == config["origin_count"]
         and len(scope.get("origin_keys", [])) == config["origin_count"]
         and scope.get("origin_keys_sha256") == digest(scope["origin_keys"]),
         "candidate exact result and handoff")
    return result, hashes


def receipts(
    config: dict[str, Any], verification_path: Path, attack_path: Path,
    result: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    verification = document(verification_path, "verification")
    attacks = document(attack_path, "attacks")
    need(verification.get("schema") == config["verification_schema"]
         and verification.get("status") == config["verification_status"]
         and verification.get("candidate_result_sha256") == result["result_sha256"]
         and verification.get("formal_credit") == config["verification_credit"],
         "downstream independent verification")
    result_key = "baseline_candidate_result_sha256" if config["round"] == "C30e" else "baseline_result_sha256"
    need(attacks.get("schema") == config["attack_schema"]
         and attacks.get("status") == config["attack_status"]
         and attacks.get(result_key) == result["result_sha256"]
         and attacks.get("attack_count") == config["attack_count"]
         and attacks.get("formal_credit") == config["attack_credit"],
         "downstream coherent attacks")
    return verification, attacks


def predecessor(config: dict[str, Any], raw: Path) -> tuple[dict[str, Any], dict[str, str]]:
    directory = workspace(raw)
    expected = {"PASS.lock", "application_receipt.json", "hostile_audit.json",
                "root_manifest.sha256", "source_w_formal_ledger.json"}
    need({entry.name for entry in os.scandir(directory)} == expected, "predecessor exact ledger files")
    ledger = document(directory / "source_w_formal_ledger.json", "predecessor ledger", "object_sha256")
    validate_state(ledger.get("current_state"), config["before"], "predecessor state")
    need(ledger.get("status") == "PASS_CONSOLIDATED_SOURCE_W_FORMAL_LEDGER__REMAINDER_" + str(config["before"]["remaining"])
         and len(ledger.get("transitions", [])) == config["sequence"] - 1
         and len(ledger.get("applied_transition_ids", [])) == config["sequence"] - 1,
         "predecessor ledger sequence")
    return ledger, {name: file_sha(directory / name, "predecessor:" + name) for name in sorted(expected)}


def validate_transition(value: dict[str, Any], config: dict[str, Any], prior: dict[str, Any], exact: dict[str, Any]) -> None:
    body = dict(value)
    claimed = body.pop("transition_id", None)
    need(claimed == digest(body) and value == exact, "exact transition object")
    validate_state(value["before"], config["before"], "transition before")
    validate_state(value["after"], config["after"], "transition after")
    need(value["sequence"] == config["sequence"] and value["round"] == config["round"]
         and value["credits"] == config["credit"]
         and value["predecessor_ledger_object_sha256"] == prior["object_sha256"],
         "transition order and authority")


def hostile(config: dict[str, Any], transition: dict[str, Any], prior: dict[str, Any]) -> dict[str, Any]:
    attacks = (
        ("conservation", lambda item: item["after"].__setitem__("remaining", item["after"]["remaining"] + 1)),
        ("duplicate", lambda item: item.__setitem__("sequence", item["sequence"] - 1)),
        ("out_of_order", lambda item: item.__setitem__("before", copy.deepcopy(config["after"]))),
        ("schema", lambda item: item.__setitem__("round", "C30x")),
        ("PID", lambda item: item.__setitem__("ExecMainPID", 2)),
        ("stale", lambda item: item.__setitem__("predecessor_ledger_object_sha256", "0" * 64)),
        ("marker", lambda item: item.__setitem__("terminal_replay_object_sha256", "1" * 64)),
        ("manifest", lambda item: item.__setitem__("independent_verification_file_sha256", "2" * 64)),
        ("object", lambda item: item.__setitem__("candidate_result_object_sha256", "3" * 64)),
    )
    rejected: list[str] = []
    for name, mutate in attacks:
        target = copy.deepcopy(transition)
        mutate(target)
        body = dict(target)
        body.pop("transition_id", None)
        target["transition_id"] = digest(body)
        try:
            validate_transition(target, config, prior, transition)
        except Reject:
            rejected.append(name)
    need(rejected == [name for name, _ in attacks], "all downstream hostile attacks")
    return close({
        "schema": "cm2." + config["round"].lower() + ".formal-source-w-ledger-hostile-audit.v1",
        "status": "PASS_" + config["round"].upper() + "_FORMAL_LEDGER_ALL_9_HOSTILE_ATTACKS_REJECTED",
        "negative_test_count": 9, "rejected_attacks": rejected,
        "formal_transition_authorized_by_audit": False, **STRICT,
    }, "object_sha256")


def build(arguments: argparse.Namespace) -> dict[str, Any]:
    config = CONFIGS[arguments.round]
    candidate_a = workspace(arguments.candidate_a)
    candidate_b = workspace(arguments.candidate_b)
    verification_path = workspace(arguments.verification_receipt)
    attack_path = workspace(arguments.attack_receipt)
    adapter_path = workspace(arguments.predecessor_adapter)
    pins_path = workspace(arguments.predecessor_dynamic_pins)
    chain = workspace(arguments.chain_dir, absent=True)
    ledger_dir = workspace(arguments.ledger_dir, absent=True)
    need(not chain.exists() and not ledger_dir.exists(), "fresh downstream outputs")
    result_a, hashes_a = candidate(config, candidate_a)
    result_b, hashes_b = candidate(config, candidate_b)
    need(hashes_a == hashes_b and all(
        regular(candidate_a / name, "seed-a:" + name)
        == regular(candidate_b / name, "seed-b:" + name)
        for name in config["files"]
    ), "downstream dual-seed byte identity")
    verification, attacks = receipts(config, verification_path, attack_path, result_a)
    prior, prior_hashes = predecessor(config, arguments.predecessor_ledger_dir)
    process = process_attestation(config)
    provenance = {
        relative: file_sha(ROOT / relative, "provenance:" + relative, 8 << 20)
        for relative in config["provenance"]
    }
    provenance[adapter_path.relative_to(ROOT).as_posix()] = file_sha(adapter_path, "predecessor adapter", 8 << 20)
    provenance[pins_path.relative_to(ROOT).as_posix()] = file_sha(pins_path, "predecessor pins", 8 << 20)
    provenance[BASE_PATH.relative_to(ROOT).as_posix()] = file_sha(BASE_PATH, "release base", 8 << 20)

    chain_tmp = chain.with_name(chain.name + ".tmp-" + str(os.getpid()))
    ledger_tmp = ledger_dir.with_name(ledger_dir.name + ".tmp-" + str(os.getpid()))
    chain_tmp.mkdir(mode=0o700)
    payload = chain_tmp / "payload"
    (payload / "candidate").mkdir(mode=0o700, parents=True)
    (payload / "predecessor").mkdir(mode=0o700)
    (payload / "provenance").mkdir(mode=0o700)
    try:
        for name in sorted(config["files"]):
            copy_regular(candidate_a / name, payload / "candidate" / name, "candidate publication:" + name)
        copy_regular(verification_path, payload / "independent_verification.json", "verification publication")
        copy_regular(attack_path, payload / "coherent_attack_receipt.json", "attack publication")
        prior_dir = workspace(arguments.predecessor_ledger_dir)
        for name in sorted(prior_hashes):
            copy_regular(prior_dir / name, payload / "predecessor" / name, "prior publication:" + name)
        for ordinal, (relative, sha) in enumerate(sorted(provenance.items())):
            source = ROOT / relative
            target = payload / "provenance" / f"{ordinal:02d}-{Path(relative).name}"
            need(copy_regular(source, target, "provenance publication:" + relative) == sha,
                 "provenance copy pin")
        evidence = close({
            "schema": "cm2." + arguments.round + ".v2-evidence-bundle-receipt.v1",
            "status": "PASS_" + arguments.round.upper() + "_V2_DUAL_SEED_VERIFICATION_AND_ATTACK_EVIDENCE",
            "process_attestation": process,
            "candidate_result_object_sha256": result_a["result_sha256"],
            "candidate_member_sha256": hashes_a,
            "dual_seed_byte_identical": True, "seed_count": 2,
            "independent_verification_file_sha256": file_sha(verification_path, "verification evidence"),
            "independent_verification_status": verification["status"],
            "coherent_attack_receipt_file_sha256": file_sha(attack_path, "attack evidence"),
            "coherent_attack_status": attacks["status"],
            "coherent_attack_count": config["attack_count"],
            "predecessor_ledger_object_sha256": prior["object_sha256"],
            "predecessor_member_sha256": prior_hashes,
            "provenance_source_sha256": provenance,
            "formal_credit": config["zero"], **STRICT,
        }, "evidence_bundle_sha256")
        write_json(chain_tmp / "evidence_bundle_receipt.json", evidence)
        payload_members = sorted(path.relative_to(chain_tmp).as_posix()
                                 for path in chain_tmp.rglob("*") if path.is_file())
        payload_bytes = manifest(chain_tmp, payload_members)
        (chain_tmp / "payload_manifest.sha256").write_bytes(payload_bytes)
        os.chmod(chain_tmp / "payload_manifest.sha256", 0o600)
        payload_sha = file_sha(chain_tmp / "payload_manifest.sha256", "payload manifest")
        manifest_receipt = close({
            "schema": "cm2." + arguments.round + ".v2-manifest-receipt.v1",
            "status": "PASS_" + arguments.round.upper() + "_V2_PAYLOAD_MANIFEST_ALL_MEMBERS_VERIFIED",
            "payload_manifest_sha256": payload_sha,
            "payload_manifest_member_count": len(payload_members),
            "payload_members": payload_members, "all_members_verified": True,
            "evidence_bundle_sha256": evidence["evidence_bundle_sha256"],
            "formal_credit": config["zero"], **STRICT,
        }, "manifest_receipt_sha256")
        write_json(chain_tmp / "manifest_receipt.json", manifest_receipt)
        scope = result_a[config["scope_key"]]
        outer = close({
            "schema": "cm2." + arguments.round + ".v2-outer-verification.v1",
            "status": "PASS_" + arguments.round.upper() + "_V2_OUTER_VERIFICATION__"
                      + str(config["before"]["remaining"]) + "_TO_" + str(config["after"]["remaining"])
                      + "_READY_FOR_TERMINAL",
            "candidate_result_object_sha256": result_a["result_sha256"],
            "independent_verification_file_sha256": file_sha(verification_path, "verification outer"),
            "coherent_attack_receipt_file_sha256": file_sha(attack_path, "attack outer"),
            "payload_manifest_sha256": payload_sha,
            "manifest_receipt_sha256": manifest_receipt["manifest_receipt_sha256"],
            "predecessor_ledger_object_sha256": prior["object_sha256"],
            "before": config["before"], "credit": config["credit"], "after": config["after"],
            "conservation_verified": True, "origin_count": config["origin_count"],
            "origin_keys_sha256": scope["origin_keys_sha256"],
            "candidate_files_byte_replayed": True, "dual_seed_byte_replayed": True,
            "formal_credit_before_terminal": config["zero"], **STRICT,
        }, "outer_verification_sha256")
        write_json(chain_tmp / "outer_verification.json", outer)
        root_bytes = manifest(chain_tmp, ["outer_verification.json", "payload_manifest.sha256"])
        (chain_tmp / "root_manifest.sha256").write_bytes(root_bytes)
        os.chmod(chain_tmp / "root_manifest.sha256", 0o600)
        root_sha = file_sha(chain_tmp / "root_manifest.sha256", "root manifest")
        seal = close({
            "schema": "cm2." + arguments.round + ".v2-terminal-seal-receipt.v1",
            "status": "PASS_" + arguments.round.upper() + "_V2_EXACT_TERMINAL_SEAL__"
                      + str(config["before"]["remaining"]) + "_TO_" + str(config["after"]["remaining"]),
            "evidence_bundle_sha256": evidence["evidence_bundle_sha256"],
            "manifest_receipt_sha256": manifest_receipt["manifest_receipt_sha256"],
            "payload_manifest_sha256": payload_sha, "root_manifest_sha256": root_sha,
            "outer_verification_sha256": outer["outer_verification_sha256"],
            "before": config["before"], "credit": config["credit"], "after": config["after"],
            "terminal_status": config["terminal_status"],
            "all_receipt_object_hashes_closed": True, "all_payload_members_verified": True,
            "formal_transition_authorized_by_seal_alone": False, **STRICT,
        }, "terminal_seal_receipt_sha256")
        write_json(chain_tmp / "terminal_seal_receipt.json", seal)
        replay_names = ["evidence_bundle_receipt.json", "manifest_receipt.json",
                        "outer_verification.json", "payload_manifest.sha256",
                        "root_manifest.sha256", "terminal_seal_receipt.json"]
        replay = close({
            "schema": "cm2." + arguments.round + ".v2-terminal-byte-replay.v1",
            "status": config["terminal_status"],
            "required_member_sha256": {name: file_sha(chain_tmp / name, "replay:" + name)
                                       for name in replay_names},
            "terminal_seal_receipt_sha256": seal["terminal_seal_receipt_sha256"],
            "candidate_result_object_sha256": result_a["result_sha256"],
            "before": config["before"], "credit": config["credit"], "after": config["after"],
            "all_bytes_replayed": True, "root_binds_payload_manifest": True,
            "root_binds_outer_verification": True,
            config["round"] + "_transition_authorized": True,
            "source_W_formal_remainder": config["after"]["remaining"], **STRICT,
        }, "terminal_replay_sha256")
        write_json(chain_tmp / "terminal_replay.json", replay)
        status = close({
            "schema": "cm2." + arguments.round + ".v2-release-chain-status.v1",
            "status": config["chain_status"], "terminal_status": config["terminal_status"],
            "terminal_replay_file_sha256": file_sha(chain_tmp / "terminal_replay.json", "status replay"),
            "terminal_replay_object_sha256": replay["terminal_replay_sha256"],
            "terminal_seal_file_sha256": file_sha(chain_tmp / "terminal_seal_receipt.json", "status seal"),
            "terminal_seal_object_sha256": seal["terminal_seal_receipt_sha256"],
            "source_W_transition": {"before": config["before"]["remaining"],
                                    "after": config["after"]["remaining"]},
            "source_W_transition_authorized": True,
            "source_W_formal_remainder": config["after"]["remaining"], **process, **STRICT,
        }, "chain_status_sha256")
        write_json(chain_tmp / "chain_status.json", status)
        (chain_tmp / "PASS.lock").write_bytes((config["chain_status"] + "\n").encode("ascii"))
        os.chmod(chain_tmp / "PASS.lock", 0o600)

        transition_body = {
            "sequence": config["sequence"], "round": config["round"],
            "before": config["before"], "after": config["after"],
            "credits": config["credit"], "disposition": config["disposition"],
            "origin_keys": scope["origin_keys"], "origin_keys_sha256": scope["origin_keys_sha256"],
            "candidate_result_object_sha256": result_a["result_sha256"],
            "independent_verification_file_sha256": file_sha(verification_path, "ledger verification"),
            "coherent_attack_receipt_file_sha256": file_sha(attack_path, "ledger attacks"),
            "predecessor_ledger_object_sha256": prior["object_sha256"],
            "terminal_replay_object_sha256": replay["terminal_replay_sha256"],
            "chain_status_object_sha256": status["chain_status_sha256"],
            "InvocationID": process["InvocationID"], "ExecMainPID": process["ExecMainPID"],
        }
        transition = {**transition_body, "transition_id": digest(transition_body)}
        validate_transition(transition, config, prior, transition)
        audit = hostile(config, transition, prior)
        ledger = close({
            "schema": "cm2.source-w.consolidated-formal-ledger.v1",
            "status": config["ledger_status"], "total_source_W_origins": 76_832,
            "formally_addressed_source_W_origins": 76_832 - config["after"]["remaining"],
            "formal_coverage_numerator": 76_832 - config["after"]["remaining"],
            "formal_coverage_denominator": 76_832,
            "remaining_origin_partition": config["after"]["remaining_partition"],
            "current_state": config["after"],
            "applied_transition_ids": prior["applied_transition_ids"] + [transition["transition_id"]],
            "transitions": prior["transitions"] + [transition],
            "authority_pins": {
                **prior["authority_pins"],
                arguments.round + "_candidate_result_object_sha256": result_a["result_sha256"],
                arguments.round + "_independent_verification_file_sha256": file_sha(verification_path, "authority verification"),
                arguments.round + "_coherent_attack_receipt_file_sha256": file_sha(attack_path, "authority attacks"),
                arguments.round + "_terminal_replay_object_sha256": replay["terminal_replay_sha256"],
                arguments.round + "_chain_status_object_sha256": status["chain_status_sha256"],
                arguments.round + "_hostile_audit_object_sha256": audit["object_sha256"],
            },
            "strict_nonpromotion": STRICT,
        }, "object_sha256")
        application = close({
            "schema": "cm2." + arguments.round + ".formal-source-w-ledger-application-receipt.v1",
            "status": config["application_status"],
            "source_W_transition": {"before": config["before"]["remaining"],
                                    "after": config["after"]["remaining"]},
            "source_W_transition_authorized": True,
            "source_W_formal_remainder": config["after"]["remaining"],
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
        ledger_root = manifest(ledger_tmp, ["application_receipt.json", "hostile_audit.json",
                                            "source_w_formal_ledger.json"])
        (ledger_tmp / "root_manifest.sha256").write_bytes(ledger_root)
        os.chmod(ledger_tmp / "root_manifest.sha256", 0o600)
        (ledger_tmp / "PASS.lock").write_bytes(("PASS_" + config["round"].upper()
                                                + "_FORMAL_SOURCE_W_LEDGER__REMAINDER_"
                                                + str(config["after"]["remaining"]) + "\n").encode("ascii"))
        os.chmod(ledger_tmp / "PASS.lock", 0o600)
        os.rename(chain_tmp, chain)
        os.rename(ledger_tmp, ledger_dir)
    except BaseException:
        shutil.rmtree(chain_tmp, ignore_errors=True)
        shutil.rmtree(ledger_tmp, ignore_errors=True)
        raise
    return close({
        "schema": "cm2." + arguments.round + ".v2-release-chain-builder-receipt.v1",
        "status": config["chain_status"],
        "chain_dir": chain.relative_to(ROOT).as_posix(),
        "ledger_dir": ledger_dir.relative_to(ROOT).as_posix(),
        "chain_status_object_sha256": status["chain_status_sha256"],
        "terminal_replay_object_sha256": replay["terminal_replay_sha256"],
        "ledger_object_sha256": ledger["object_sha256"],
        "application_object_sha256": application["object_sha256"],
        "transition_id": transition["transition_id"], "hostile_negative_test_count": 9,
        "source_W_formal_remainder": config["after"]["remaining"], **STRICT,
    }, "release_receipt_sha256")


def self_test() -> dict[str, Any]:
    for name, config in CONFIGS.items():
        validate_state(config["before"], config["before"], name + " before")
        validate_state(config["after"], config["after"], name + " after")
        need(config["before"]["remaining"] - config["after"]["remaining"]
             == config["origin_count"], name + " remainder delta")
    return {
        "schema": "cm2.round306.source-w-downstream-release-builder-self-test.v1",
        "status": "PASS_C30E_C30F_RELEASE_BUILDER_STATIC_FIXTURES",
        "rounds": {name: {"before": config["before"]["remaining"],
                           "after": config["after"]["remaining"],
                           "attacks": config["attack_count"]}
                   for name, config in CONFIGS.items()},
        "CM2": "NO-GO_FOR_CLAIM",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--round", choices=sorted(CONFIGS))
    parser.add_argument("--candidate-a", type=Path)
    parser.add_argument("--candidate-b", type=Path)
    parser.add_argument("--verification-receipt", type=Path)
    parser.add_argument("--attack-receipt", type=Path)
    parser.add_argument("--predecessor-ledger-dir", type=Path)
    parser.add_argument("--predecessor-adapter", type=Path)
    parser.add_argument("--predecessor-dynamic-pins", type=Path)
    parser.add_argument("--chain-dir", type=Path)
    parser.add_argument("--ledger-dir", type=Path)
    parser.add_argument("--self-test", action="store_true")
    arguments = parser.parse_args()
    fields = ("round", "candidate_a", "candidate_b", "verification_receipt",
              "attack_receipt", "predecessor_ledger_dir", "predecessor_adapter",
              "predecessor_dynamic_pins", "chain_dir", "ledger_dir")
    try:
        if arguments.self_test:
            need(all(getattr(arguments, field) is None for field in fields), "self-test isolation")
            output = self_test()
        else:
            need(all(getattr(arguments, field) is not None for field in fields), "complete arguments")
            output = build(arguments)
    except (Reject, OSError, ValueError, TypeError, KeyError, AssertionError,
            RuntimeError, json.JSONDecodeError) as error:
        print("REJECT:" + type(error).__name__ + ":" + str(error), file=sys.stderr)
        return 2
    print(canonical(output).decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
