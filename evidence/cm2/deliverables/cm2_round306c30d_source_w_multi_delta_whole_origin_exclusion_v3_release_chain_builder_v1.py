#!/usr/bin/env python3
"""Build the C30d-v3 terminal graph and install its formal Source-W transition.

The builder accepts only byte-identical dual-seed candidates plus persisted
independent-verifier and coherent-attack receipts.  It writes an acyclic
terminal graph first, then a separate consolidated Source-W ledger whose
second transition is bound to that terminal replay.  Every output is fresh,
canonical, closed, and fail-closed under the transition invariants below.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import stat
import sys
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
SELF = Path(__file__).resolve()
PREFIX = "cm2_round306c30d_source_w_multi_delta_whole_origin_exclusion_v3"
RESULT = PREFIX + "_result.json"
CANDIDATE_FILES = frozenset({
    "cm2_round306c30b_python_flint_runtime_attestation.json",
    PREFIX + "_atomic_half_open_owner_ledger.jsonl.gz",
    PREFIX + "_multi_delta_cell_ledger.jsonl.gz",
    PREFIX + "_whole_origin_ledger.jsonl.gz",
    RESULT,
})
PROVENANCE = (
    "deliverables/cm2_round306c30d_c30c_v3_predecessor_authority_adapter_v1.py",
    "deliverables/cm2_round306c30d_c30c_v3_predecessor_authority_independent_verifier_v1.py",
    "deliverables/cm2_round306c30d_source_w_multi_delta_whole_origin_exclusion_v3_producer.py",
    "deliverables/cm2_round306c30d_source_w_multi_delta_whole_origin_exclusion_v3_independent_verifier.py",
    "deliverables/cm2_round306c30d_source_w_multi_delta_whole_origin_exclusion_v3_coherent_attack_harness.py",
)
PROVENANCE_SHA256 = {
    PROVENANCE[0]: "f10613b8698997c99d3cece4f301cc89ea9f532f2d23c9d08325ef150b578503",
    PROVENANCE[1]: "2502080768137561722df2ef5662a560e3a49c943606920690b99e6ea695caae",
    PROVENANCE[2]: "946955775cfe1ddc2acba538f6723b64c57b8080ce12bd34e4959c2c46e1f11c",
    PROVENANCE[3]: "a7d88985d591ea981eb78ff56fa407c48ba7e90e88860a72f7b87a3b88949a1c",
    PROVENANCE[4]: "3fb93a3468b1bb49e4dbbd385d83365ac86f7bfed977eb086c52b7beca8c29c7",
}

RESULT_SCHEMA = "cm2.round306c30d.source-w-multi-delta-whole-origin-exclusion.candidate.v3"
RESULT_STATUS = (
    "PASS_CANDIDATE_C30D_V3__1176_MULTI_DELTA_CELLS__20_WHOLE_ORIGINS_"
    "EXCLUDED__ZERO_FORMAL_CREDIT__UNAUTHORIZED"
)
VERIFICATION_SCHEMA = (
    "cm2.round306c30d.source-w-multi-delta-whole-origin-exclusion."
    "independent-verification.v3"
)
VERIFICATION_STATUS = (
    "PASS_NO_IMPORT_INDEPENDENT_C30D_V3__1176_CELLS__20_EXCLUDED_ORIGINS__"
    "ZERO_FORMAL_CREDIT__MANIFEST_UNAUTHORIZED"
)
ATTACK_SCHEMA = "cm2.round306c30d.v3-coherent-attack-harness.v1"
ATTACK_STATUS = (
    "PASS_ALL_C30D_V3_COHERENT_CANDIDATE_ATTACKS_REJECTED__ZERO_FORMAL_CREDIT"
)
TERMINAL_STATUS = "PASS_FORMAL_C30D_TERMINAL__78_TO_58_AUTHORIZED"
CHAIN_STATUS = "PASS_C30D_V3_TERMINAL_BYTE_REPLAY__FORMAL_SOURCE_W_78_TO_58"

BEFORE = {
    "excluded": 74_746,
    "conservative_live": 2_086,
    "resolved_nonexcluded": 2_008,
    "remaining": 78,
    "total": 76_832,
    "remaining_partition": {
        "multi_Delta": 20,
        "reduced_live": 2,
        "retained_source_seams": 2,
        "compact_q": 54,
    },
}
AFTER = {
    "excluded": 74_766,
    "conservative_live": 2_066,
    "resolved_nonexcluded": 2_008,
    "remaining": 58,
    "total": 76_832,
    "remaining_partition": {
        "reduced_live": 2,
        "retained_source_seams": 2,
        "compact_q": 54,
    },
}
CREDIT = {
    "resolved_source_W_origin_dispositions": 20,
    "whole_source_W_origin_exclusions": 20,
    "resolved_nonexcluded": 0,
}
ZERO_FORMAL = {
    "multi_Delta_cell_dispositions": 0,
    "multi_Delta_whole_cell_exclusions": 0,
    "resolved_source_W_origin_dispositions": 0,
    "whole_source_W_origin_exclusions": 0,
}
STRICT = {
    "D02": "BLOCKED_COMPOSITE",
    "D03": "UNAUTHORIZED",
    "D04": "NOT_MINTED",
    "Gate5": "10/18",
    "complete_global_18_field_blocks": 0,
    "CM2": "NO-GO_FOR_CLAIM",
}
ORIGIN_KEYS_SHA256 = "4b9d22a6c363960f67d4da851f5a77e487ee240f427bc9bd9016ced24c1b88e4"


class Reject(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Reject(label)


def canonical(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=True,
        allow_nan=False,
    ).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def valid_sha(value: Any) -> bool:
    return (
        type(value) is str and len(value) == 64
        and all(character in "0123456789abcdef" for character in value)
    )


def close(value: dict[str, Any], field: str) -> dict[str, Any]:
    need(field not in value, "closure field absent:" + field)
    return {**value, field: digest(value)}


def strict_pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in items:
        need(key not in result, "duplicate JSON key:" + key)
        result[key] = value
    return result


def strict_bytes(raw: bytes, label: str) -> dict[str, Any]:
    need(not raw.endswith(b"\n\n"), label + ":newline")
    payload = raw[:-1] if raw.endswith(b"\n") else raw
    value = json.loads(
        payload, object_pairs_hook=strict_pairs,
        parse_constant=lambda token: (_ for _ in ()).throw(Reject(token)),
    )
    need(type(value) is dict and canonical(value) == payload, label + ":canonical")
    return value


def workspace(raw: Path, *, absent: bool = False) -> Path:
    supplied = raw if raw.is_absolute() else ROOT / raw
    path = Path(os.path.abspath(os.fspath(supplied)))
    try:
        relative = path.relative_to(ROOT)
    except ValueError as error:
        raise Reject("path outside workspace:" + os.fspath(raw)) from error
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
    need(
        stat.S_ISREG(before.st_mode) and before.st_nlink == 1
        and 0 < before.st_size <= maximum,
        label + ":regular-single-link-size",
    )
    raw = absolute.read_bytes()
    after = absolute.lstat()
    need(
        (before.st_dev, before.st_ino, before.st_mode, before.st_nlink,
         before.st_size, before.st_mtime_ns, before.st_ctime_ns)
        == (after.st_dev, after.st_ino, after.st_mode, after.st_nlink,
            after.st_size, after.st_mtime_ns, after.st_ctime_ns),
        label + ":TOCTOU",
    )
    return raw


def file_sha(path: Path, label: str, maximum: int = 128 << 20) -> str:
    return hashlib.sha256(regular(path, label, maximum)).hexdigest()


def document(path: Path, label: str, closure: str | None = None) -> dict[str, Any]:
    value = strict_bytes(regular(path, label), label)
    if closure is not None:
        body = dict(value)
        claimed = body.pop(closure, None)
        need(valid_sha(claimed) and claimed == digest(body), label + ":closure")
    return value


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    path.write_bytes(canonical(value) + b"\n")
    os.chmod(path, 0o600)


def copy_regular(source: Path, target: Path, label: str) -> str:
    raw = regular(source, label)
    target.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    target.write_bytes(raw)
    os.chmod(target, 0o600)
    need(target.read_bytes() == raw, label + ":copy equality")
    return hashlib.sha256(raw).hexdigest()


def manifest(root: Path, members: list[str]) -> bytes:
    need(len(members) == len(set(members)) and members == sorted(members), "manifest ordered unique")
    rows: list[str] = []
    for member in members:
        need(not member.startswith("/") and ".." not in Path(member).parts, "manifest member path")
        rows.append(file_sha(root / member, "manifest:" + member) + "  " + member)
    return ("\n".join(rows) + "\n").encode("ascii")


def validate_state(state: Any, expected: dict[str, Any], label: str) -> None:
    need(state == expected, label + ":exact state")
    need(
        state["excluded"] + state["conservative_live"] == state["total"]
        and state["resolved_nonexcluded"] + state["remaining"] == state["conservative_live"]
        and sum(state["remaining_partition"].values()) == state["remaining"],
        label + ":conservation",
    )


def validate_candidate(candidate: Path) -> tuple[dict[str, Any], dict[str, str]]:
    directory = workspace(candidate)
    state = directory.lstat()
    need(stat.S_ISDIR(state.st_mode) and not directory.is_symlink(), "candidate directory")
    names = {entry.name for entry in os.scandir(directory)}
    need(names == CANDIDATE_FILES, "candidate exact file set")
    hashes = {name: file_sha(directory / name, "candidate:" + name) for name in sorted(names)}
    result = document(directory / RESULT, "candidate result")
    body = dict(result)
    claimed = body.pop("result_sha256", None)
    transition = result.get("proposed_source_W_transition_if_C30d_is_terminally_sealed")
    scope = result.get("scope")
    need(
        valid_sha(claimed) and claimed == digest(body)
        and result.get("schema") == RESULT_SCHEMA
        and result.get("status") == RESULT_STATUS
        and result.get("formal_credit") == ZERO_FORMAL
        and type(scope) is dict
        and scope.get("origin_count") == 20
        and scope.get("origin_keys_sha256") == ORIGIN_KEYS_SHA256
        and scope.get("new_multi_Delta_cell_count") == 1_176
        and type(transition) is dict
        and transition.get("before") == BEFORE
        and transition.get("after") == AFTER
        and transition.get("C30d_transition_authorized") is False,
        "candidate exact theorem and zero-credit boundary",
    )
    return result, hashes


def validate_receipts(
    verification_path: Path, attack_path: Path, result: dict[str, Any],
    candidate_hashes: dict[str, str],
) -> tuple[dict[str, Any], dict[str, Any]]:
    verification = document(verification_path, "verification receipt")
    attacks = document(attack_path, "attack receipt")
    need(
        verification.get("schema") == VERIFICATION_SCHEMA
        and verification.get("status") == VERIFICATION_STATUS
        and verification.get("candidate_result_sha256") == result["result_sha256"]
        and verification.get("candidate_files") == candidate_hashes
        and verification.get("whole_origin_disposition_census") == {"EXCLUDED": 20}
        and verification.get("formal_credit") == ZERO_FORMAL
        and verification.get("manifest_authorized") is False
        and verification.get("C30d_transition_authorized") is False
        and verification.get("source_W_formal_remainder") == 78,
        "independent verification exact pass",
    )
    need(
        attacks.get("schema") == ATTACK_SCHEMA
        and attacks.get("status") == ATTACK_STATUS
        and attacks.get("candidate_result_sha256") == result["result_sha256"]
        and attacks.get("attack_count") == 26
        and type(attacks.get("rejected_attacks")) is list
        and len(attacks["rejected_attacks"]) == 26
        and len(set(attacks["rejected_attacks"])) == 26
        and attacks.get("formal_credit") == ZERO_FORMAL
        and attacks.get("C30d_transition_authorized") is False,
        "coherent attacks exact pass",
    )
    return verification, attacks


def validate_predecessor(directory: Path) -> tuple[dict[str, Any], dict[str, str]]:
    root = workspace(directory)
    names = {entry.name for entry in os.scandir(root)}
    need(
        {"source_w_formal_ledger.json", "application_receipt.json", "hostile_audit.json", "root_manifest.sha256", "PASS.lock"}.issubset(names),
        "predecessor ledger member set",
    )
    ledger = document(root / "source_w_formal_ledger.json", "predecessor ledger", "object_sha256")
    application = document(root / "application_receipt.json", "predecessor application", "object_sha256")
    audit = document(root / "hostile_audit.json", "predecessor hostile audit", "object_sha256")
    validate_state(ledger.get("current_state"), BEFORE, "predecessor")
    need(
        ledger.get("schema") == "cm2.source-w.consolidated-formal-ledger.v1"
        and ledger.get("status") == "PASS_CONSOLIDATED_SOURCE_W_FORMAL_LEDGER__REMAINDER_78"
        and ledger.get("formal_coverage_numerator") == 76_754
        and ledger.get("formal_coverage_denominator") == 76_832
        and ledger.get("applied_transition_ids")
        == ["daddf0b33682a7a75c82f562d6f385ef4944f65bcc4b4d59856bd18e4a8dc620"]
        and application.get("source_W_formal_remainder") == 78
        and application.get("source_W_transition_authorized") is True
        and audit.get("negative_test_count") == 9,
        "predecessor ledger exact authority",
    )
    hashes = {
        name: file_sha(root / name, "predecessor:" + name)
        for name in sorted(names) if (root / name).is_file()
    }
    return ledger, hashes


def process_attestation() -> dict[str, Any]:
    token = os.environ.get("CM2_PUBLICATION_TOKEN", "")
    unit = os.environ.get("CM2_PUBLICATION_UNIT", "")
    invocation = os.environ.get("INVOCATION_ID", "")
    need(re.fullmatch(r"c30d-v3-publication-[a-z0-9-]{16,160}", token) is not None, "fresh publication token shape")
    need(re.fullmatch(r"cm2-c30d-v3-publication-[a-z0-9-]{16,160}\.service", unit) is not None, "publication unit shape")
    need(re.fullmatch(r"[0-9a-f]{32}", invocation) is not None, "systemd InvocationID")
    need(
        os.environ.get("HOME") == "/nonexistent"
        and os.environ.get("LC_ALL") == "C.UTF-8"
        and os.environ.get("TZ") == "UTC"
        and os.environ.get("PYTHONHASHSEED") == "0",
        "controlled publication environment",
    )
    return {
        "publication_token": token,
        "unit": unit,
        "InvocationID": invocation,
        "ExecMainPID": os.getpid(),
        "uid": os.getuid(),
        "controlled_environment": {
            name: os.environ[name]
            for name in ("HOME", "LC_ALL", "TZ", "PYTHONHASHSEED")
        },
    }


def transition_body(
    predecessor: dict[str, Any], result: dict[str, Any],
    verification_sha: str, attack_sha: str, replay: dict[str, Any],
    chain_status: dict[str, Any],
) -> dict[str, Any]:
    return {
        "sequence": 2,
        "round": "C30d",
        "before": BEFORE,
        "after": AFTER,
        "credits": CREDIT,
        "disposition": "EXCLUDED",
        "origin_keys": result["scope"]["origin_keys"],
        "origin_keys_sha256": ORIGIN_KEYS_SHA256,
        "candidate_result_object_sha256": result["result_sha256"],
        "independent_verification_file_sha256": verification_sha,
        "coherent_attack_receipt_file_sha256": attack_sha,
        "predecessor_ledger_object_sha256": predecessor["object_sha256"],
        "terminal_replay_object_sha256": replay["terminal_replay_sha256"],
        "chain_status_object_sha256": chain_status["chain_status_sha256"],
    }


def validate_transition(
    value: dict[str, Any], predecessor: dict[str, Any],
    authority: dict[str, Any] | None = None,
) -> None:
    expected_keys = {
        "sequence", "round", "before", "after", "credits", "disposition",
        "origin_keys", "origin_keys_sha256", "candidate_result_object_sha256",
        "independent_verification_file_sha256", "coherent_attack_receipt_file_sha256",
        "predecessor_ledger_object_sha256", "terminal_replay_object_sha256",
        "chain_status_object_sha256", "transition_id",
    }
    body = dict(value)
    claimed = body.pop("transition_id", None)
    need(set(value) == expected_keys and claimed == digest(body), "transition schema/object")
    validate_state(value["before"], BEFORE, "transition before")
    validate_state(value["after"], AFTER, "transition after")
    need(
        predecessor["current_state"] == value["before"]
        and value["sequence"] == len(predecessor["transitions"]) + 1
        and value["round"] == "C30d"
        and value["credits"] == CREDIT
        and value["disposition"] == "EXCLUDED"
        and len(value["origin_keys"]) == 20
        and len(set(value["origin_keys"])) == 20
        and value["origin_keys"] == sorted(value["origin_keys"])
        and value["origin_keys_sha256"] == ORIGIN_KEYS_SHA256
        and value["predecessor_ledger_object_sha256"] == predecessor["object_sha256"]
        and all(valid_sha(value[field]) for field in (
            "candidate_result_object_sha256", "independent_verification_file_sha256",
            "coherent_attack_receipt_file_sha256", "terminal_replay_object_sha256",
            "chain_status_object_sha256",
        )),
        "transition continuity and authority pins",
    )
    if authority is not None:
        for field in (
            "origin_keys", "origin_keys_sha256", "candidate_result_object_sha256",
            "independent_verification_file_sha256", "coherent_attack_receipt_file_sha256",
            "predecessor_ledger_object_sha256", "terminal_replay_object_sha256",
            "chain_status_object_sha256",
        ):
            need(value[field] == authority[field], "transition exact authority:" + field)


def hostile_audit(transition: dict[str, Any], predecessor: dict[str, Any]) -> dict[str, Any]:
    attacks: list[tuple[str, Any]] = []
    attacks.append(("conservation", lambda item: item["after"].__setitem__("remaining", 59)))
    attacks.append(("duplicate_application", lambda item: item.__setitem__("sequence", 1)))
    attacks.append(("out_of_order", lambda item: item.__setitem__("before", copy.deepcopy(AFTER))))
    attacks.append(("schema", lambda item: item.__setitem__("round", "C30x")))
    attacks.append(("stale_predecessor", lambda item: item.__setitem__("predecessor_ledger_object_sha256", "0" * 64)))
    attacks.append(("manifest", lambda item: item.__setitem__("independent_verification_file_sha256", "1" * 64)))
    attacks.append(("terminal_object", lambda item: item.__setitem__("terminal_replay_object_sha256", "2" * 64)))
    attacks.append(("candidate_object", lambda item: item.__setitem__("candidate_result_object_sha256", "3" * 64)))
    attacks.append(("partition", lambda item: item["after"]["remaining_partition"].__setitem__("compact_q", 53)))
    rejected: list[str] = []
    for name, mutate in attacks:
        target = copy.deepcopy(transition)
        mutate(target)
        body = dict(target)
        body.pop("transition_id", None)
        target["transition_id"] = digest(body)
        try:
            validate_transition(target, predecessor, transition)
        except Reject:
            rejected.append(name)
    need(rejected == [name for name, _ in attacks], "all hostile transition attacks rejected")
    return close({
        "schema": "cm2.round306c30d.formal-source-w-ledger-hostile-audit.v1",
        "status": "PASS_C30D_FORMAL_LEDGER_ALL_9_HOSTILE_ATTACKS_REJECTED",
        "negative_test_count": len(rejected),
        "rejected_attacks": rejected,
        "formal_transition_authorized_by_audit": False,
        **STRICT,
    }, "object_sha256")


def build(args: argparse.Namespace) -> dict[str, Any]:
    candidate_a = workspace(args.candidate_a)
    candidate_b = workspace(args.candidate_b)
    verification_path = workspace(args.verification_receipt)
    attack_path = workspace(args.attack_receipt)
    chain = workspace(args.chain_dir, absent=True)
    ledger_dir = workspace(args.ledger_dir, absent=True)
    need(not chain.exists() and not ledger_dir.exists(), "fresh chain and ledger outputs")
    need(chain.parent.exists() and ledger_dir.parent.exists(), "output parents exist")

    result_a, hashes_a = validate_candidate(candidate_a)
    result_b, hashes_b = validate_candidate(candidate_b)
    need(hashes_a == hashes_b and canonical(result_a) == canonical(result_b), "dual-seed byte identity")
    for name in CANDIDATE_FILES:
        need(regular(candidate_a / name, "seed-a:" + name) == regular(candidate_b / name, "seed-b:" + name), "dual-seed member equality:" + name)
    verification, attacks = validate_receipts(verification_path, attack_path, result_a, hashes_a)
    predecessor, predecessor_hashes = validate_predecessor(args.predecessor_ledger_dir)
    process = process_attestation()
    for relative, expected in PROVENANCE_SHA256.items():
        need(file_sha(ROOT / relative, "provenance:" + relative, 8 << 20) == expected, "provenance pin:" + relative)

    chain_tmp = chain.with_name(chain.name + ".tmp-" + str(os.getpid()))
    ledger_tmp = ledger_dir.with_name(ledger_dir.name + ".tmp-" + str(os.getpid()))
    need(not chain_tmp.exists() and not ledger_tmp.exists(), "fresh temporary outputs")
    chain_tmp.mkdir(mode=0o700)
    payload = chain_tmp / "payload"
    (payload / "candidate").mkdir(mode=0o700, parents=True)
    (payload / "predecessor").mkdir(mode=0o700)
    (payload / "provenance").mkdir(mode=0o700)
    try:
        for name in sorted(CANDIDATE_FILES):
            copy_regular(candidate_a / name, payload / "candidate" / name, "candidate publication:" + name)
        copy_regular(verification_path, payload / "independent_verification.json", "verification publication")
        copy_regular(attack_path, payload / "coherent_attack_receipt.json", "attack publication")
        for name in sorted(predecessor_hashes):
            copy_regular(workspace(args.predecessor_ledger_dir) / name, payload / "predecessor" / name, "predecessor publication:" + name)
        for relative in PROVENANCE:
            copy_regular(ROOT / relative, payload / "provenance" / Path(relative).name, "provenance publication:" + relative)

        evidence = close({
            "schema": "cm2.round306c30d.v3-evidence-bundle-receipt.v1",
            "status": "PASS_C30D_V3_DUAL_SEED_VERIFICATION_AND_26_ATTACK_EVIDENCE",
            "process_attestation": process,
            "candidate_result_object_sha256": result_a["result_sha256"],
            "candidate_member_sha256": hashes_a,
            "dual_seed_byte_identical": True,
            "seed_count": 2,
            "independent_verification_file_sha256": file_sha(verification_path, "verification input"),
            "independent_verification_status": verification["status"],
            "coherent_attack_receipt_file_sha256": file_sha(attack_path, "attack input"),
            "coherent_attack_status": attacks["status"],
            "coherent_attack_count": 26,
            "predecessor_ledger_object_sha256": predecessor["object_sha256"],
            "predecessor_member_sha256": predecessor_hashes,
            "provenance_source_sha256": PROVENANCE_SHA256,
            "formal_credit": ZERO_FORMAL,
            **STRICT,
        }, "evidence_bundle_sha256")
        write_json(chain_tmp / "evidence_bundle_receipt.json", evidence)

        payload_members = sorted(
            path.relative_to(chain_tmp).as_posix()
            for path in chain_tmp.rglob("*")
            if path.is_file()
        )
        payload_manifest = manifest(chain_tmp, payload_members)
        (chain_tmp / "payload_manifest.sha256").write_bytes(payload_manifest)
        os.chmod(chain_tmp / "payload_manifest.sha256", 0o600)
        payload_hash = hashlib.sha256(payload_manifest).hexdigest()
        manifest_receipt = close({
            "schema": "cm2.round306c30d.v3-manifest-receipt.v1",
            "status": "PASS_C30D_V3_PAYLOAD_MANIFEST_ALL_MEMBERS_VERIFIED",
            "payload_manifest_sha256": payload_hash,
            "payload_manifest_member_count": len(payload_members),
            "payload_members": payload_members,
            "all_members_verified": True,
            "evidence_bundle_sha256": evidence["evidence_bundle_sha256"],
            "formal_credit": ZERO_FORMAL,
            **STRICT,
        }, "manifest_receipt_sha256")
        write_json(chain_tmp / "manifest_receipt.json", manifest_receipt)

        outer = close({
            "schema": "cm2.round306c30d.v3-outer-verification.v1",
            "status": "PASS_C30D_V3_OUTER_VERIFICATION__78_TO_58_READY_FOR_TERMINAL",
            "candidate_result_object_sha256": result_a["result_sha256"],
            "independent_verification_file_sha256": file_sha(verification_path, "verification outer"),
            "coherent_attack_receipt_file_sha256": file_sha(attack_path, "attack outer"),
            "payload_manifest_sha256": payload_hash,
            "manifest_receipt_sha256": manifest_receipt["manifest_receipt_sha256"],
            "predecessor_ledger_object_sha256": predecessor["object_sha256"],
            "before": BEFORE,
            "credit": CREDIT,
            "after": AFTER,
            "conservation_verified": True,
            "origin_count": 20,
            "origin_keys_sha256": ORIGIN_KEYS_SHA256,
            "candidate_files_byte_replayed": True,
            "dual_seed_byte_replayed": True,
            "formal_credit_before_terminal": ZERO_FORMAL,
            **STRICT,
        }, "outer_verification_sha256")
        write_json(chain_tmp / "outer_verification.json", outer)
        root_manifest = manifest(chain_tmp, ["outer_verification.json", "payload_manifest.sha256"])
        (chain_tmp / "root_manifest.sha256").write_bytes(root_manifest)
        os.chmod(chain_tmp / "root_manifest.sha256", 0o600)
        root_hash = hashlib.sha256(root_manifest).hexdigest()

        seal = close({
            "schema": "cm2.round306c30d.v3-terminal-seal-receipt.v1",
            "status": "PASS_C30D_V3_EXACT_TERMINAL_SEAL__78_TO_58",
            "evidence_bundle_sha256": evidence["evidence_bundle_sha256"],
            "manifest_receipt_sha256": manifest_receipt["manifest_receipt_sha256"],
            "payload_manifest_sha256": payload_hash,
            "root_manifest_sha256": root_hash,
            "outer_verification_sha256": outer["outer_verification_sha256"],
            "before": BEFORE,
            "credit": CREDIT,
            "after": AFTER,
            "terminal_status": TERMINAL_STATUS,
            "all_receipt_object_hashes_closed": True,
            "all_payload_members_verified": True,
            "formal_transition_authorized_by_seal_alone": False,
            **STRICT,
        }, "terminal_seal_receipt_sha256")
        write_json(chain_tmp / "terminal_seal_receipt.json", seal)

        replay_member_names = [
            "evidence_bundle_receipt.json", "manifest_receipt.json",
            "outer_verification.json", "payload_manifest.sha256",
            "root_manifest.sha256", "terminal_seal_receipt.json",
        ]
        replay_members = {
            name: file_sha(chain_tmp / name, "terminal replay:" + name)
            for name in replay_member_names
        }
        replay = close({
            "schema": "cm2.round306c30d.v3-terminal-byte-replay.v1",
            "status": TERMINAL_STATUS,
            "required_member_sha256": replay_members,
            "terminal_seal_receipt_sha256": seal["terminal_seal_receipt_sha256"],
            "candidate_result_object_sha256": result_a["result_sha256"],
            "before": BEFORE,
            "credit": CREDIT,
            "after": AFTER,
            "all_bytes_replayed": True,
            "root_binds_payload_manifest": True,
            "root_binds_outer_verification": True,
            "C30d_transition_authorized": True,
            "source_W_formal_remainder": 58,
            **STRICT,
        }, "terminal_replay_sha256")
        write_json(chain_tmp / "terminal_replay.json", replay)
        chain_status = close({
            "schema": "cm2.round306c30d.v3-release-chain-status.v1",
            "status": CHAIN_STATUS,
            "terminal_status": TERMINAL_STATUS,
            "terminal_replay_file_sha256": file_sha(chain_tmp / "terminal_replay.json", "chain status replay"),
            "terminal_replay_object_sha256": replay["terminal_replay_sha256"],
            "terminal_seal_file_sha256": file_sha(chain_tmp / "terminal_seal_receipt.json", "chain status seal"),
            "terminal_seal_object_sha256": seal["terminal_seal_receipt_sha256"],
            "source_W_transition": {"before": 78, "after": 58},
            "source_W_transition_authorized": True,
            "source_W_formal_remainder": 58,
            "publication_token": process["publication_token"],
            "unit": process["unit"],
            "InvocationID": process["InvocationID"],
            "ExecMainPID": process["ExecMainPID"],
            **STRICT,
        }, "chain_status_sha256")
        write_json(chain_tmp / "chain_status.json", chain_status)
        (chain_tmp / "PASS.lock").write_bytes((CHAIN_STATUS + "\n").encode("ascii"))
        os.chmod(chain_tmp / "PASS.lock", 0o600)

        transition = transition_body(
            predecessor, result_a, file_sha(verification_path, "verification ledger"),
            file_sha(attack_path, "attack ledger"), replay, chain_status,
        )
        transition = {**transition, "transition_id": digest(transition)}
        validate_transition(transition, predecessor, transition)
        audit = hostile_audit(transition, predecessor)
        ledger_body = {
            "schema": "cm2.source-w.consolidated-formal-ledger.v1",
            "status": "PASS_CONSOLIDATED_SOURCE_W_FORMAL_LEDGER__REMAINDER_58",
            "total_source_W_origins": 76_832,
            "formally_addressed_source_W_origins": 76_774,
            "formal_coverage_numerator": 76_774,
            "formal_coverage_denominator": 76_832,
            "remaining_origin_partition": AFTER["remaining_partition"],
            "current_state": AFTER,
            "applied_transition_ids": predecessor["applied_transition_ids"] + [transition["transition_id"]],
            "transitions": predecessor["transitions"] + [transition],
            "authority_pins": {
                **predecessor["authority_pins"],
                "c30d_candidate_result_object_sha256": result_a["result_sha256"],
                "c30d_independent_verification_file_sha256": file_sha(verification_path, "verification authority"),
                "c30d_coherent_attack_receipt_file_sha256": file_sha(attack_path, "attack authority"),
                "c30d_terminal_replay_object_sha256": replay["terminal_replay_sha256"],
                "c30d_chain_status_object_sha256": chain_status["chain_status_sha256"],
                "c30d_hostile_audit_object_sha256": audit["object_sha256"],
            },
            "strict_nonpromotion": STRICT,
        }
        ledger = close(ledger_body, "object_sha256")
        application = close({
            "schema": "cm2.round306c30d.formal-source-w-ledger-application-receipt.v1",
            "status": "PASS_C30D_FORMAL_LEDGER_SINGLE_APPLICATION__SOURCE_W_78_TO_58",
            "source_W_transition": {"before": 78, "after": 58},
            "source_W_transition_authorized": True,
            "source_W_formal_remainder": 58,
            "transition_id": transition["transition_id"],
            "ledger_object_sha256": ledger["object_sha256"],
            "terminal_replay_object_sha256": replay["terminal_replay_sha256"],
            "chain_status_object_sha256": chain_status["chain_status_sha256"],
            "hostile_audit_object_sha256": audit["object_sha256"],
            "application_count": 1,
            "negative_test_count": 9,
            "publication_token": process["publication_token"],
            "unit": process["unit"],
            "InvocationID": process["InvocationID"],
            "ExecMainPID": process["ExecMainPID"],
            **STRICT,
        }, "object_sha256")
        ledger_tmp.mkdir(mode=0o700)
        write_json(ledger_tmp / "source_w_formal_ledger.json", ledger)
        write_json(ledger_tmp / "application_receipt.json", application)
        write_json(ledger_tmp / "hostile_audit.json", audit)
        ledger_root = manifest(ledger_tmp, [
            "application_receipt.json", "hostile_audit.json", "source_w_formal_ledger.json",
        ])
        (ledger_tmp / "root_manifest.sha256").write_bytes(ledger_root)
        os.chmod(ledger_tmp / "root_manifest.sha256", 0o600)
        (ledger_tmp / "PASS.lock").write_bytes(b"PASS_C30D_FORMAL_SOURCE_W_LEDGER__REMAINDER_58\n")
        os.chmod(ledger_tmp / "PASS.lock", 0o600)

        os.rename(chain_tmp, chain)
        os.rename(ledger_tmp, ledger_dir)
    except BaseException:
        shutil.rmtree(chain_tmp, ignore_errors=True)
        shutil.rmtree(ledger_tmp, ignore_errors=True)
        raise

    output = close({
        "schema": "cm2.round306c30d.v3-release-chain-builder-receipt.v1",
        "status": CHAIN_STATUS,
        "chain_dir": chain.relative_to(ROOT).as_posix(),
        "ledger_dir": ledger_dir.relative_to(ROOT).as_posix(),
        "chain_status_object_sha256": chain_status["chain_status_sha256"],
        "terminal_replay_object_sha256": replay["terminal_replay_sha256"],
        "ledger_object_sha256": ledger["object_sha256"],
        "application_object_sha256": application["object_sha256"],
        "transition_id": transition["transition_id"],
        "hostile_negative_test_count": 9,
        "source_W_formal_remainder": 58,
        **STRICT,
    }, "release_receipt_sha256")
    return output


def self_test() -> dict[str, Any]:
    validate_state(BEFORE, BEFORE, "fixture before")
    validate_state(AFTER, AFTER, "fixture after")
    need(BEFORE["remaining"] - AFTER["remaining"] == CREDIT["resolved_source_W_origin_dispositions"], "fixture delta")
    need(sum(AFTER["remaining_partition"].values()) == 58, "fixture partition")
    return close({
        "schema": "cm2.round306c30d.v3-release-chain-builder-self-test.v1",
        "status": "PASS_C30D_V3_RELEASE_BUILDER_STATIC_CONSERVATION_FIXTURES",
        "before": BEFORE,
        "credit": CREDIT,
        "after": AFTER,
        "expected_hostile_negative_test_count": 9,
        "formal_credit": ZERO_FORMAL,
        **STRICT,
    }, "self_test_sha256")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate-a", type=Path)
    parser.add_argument("--candidate-b", type=Path)
    parser.add_argument("--verification-receipt", type=Path)
    parser.add_argument("--attack-receipt", type=Path)
    parser.add_argument("--predecessor-ledger-dir", type=Path)
    parser.add_argument("--chain-dir", type=Path)
    parser.add_argument("--ledger-dir", type=Path)
    parser.add_argument("--self-test", action="store_true")
    arguments = parser.parse_args()
    try:
        if arguments.self_test:
            need(all(getattr(arguments, name) is None for name in (
                "candidate_a", "candidate_b", "verification_receipt", "attack_receipt",
                "predecessor_ledger_dir", "chain_dir", "ledger_dir",
            )), "self-test argument isolation")
            output = self_test()
        else:
            need(all(getattr(arguments, name) is not None for name in (
                "candidate_a", "candidate_b", "verification_receipt", "attack_receipt",
                "predecessor_ledger_dir", "chain_dir", "ledger_dir",
            )), "complete release arguments")
            output = build(arguments)
    except (Reject, OSError, ValueError, TypeError, KeyError, AssertionError, json.JSONDecodeError) as error:
        print("REJECT:" + type(error).__name__ + ":" + str(error), file=sys.stderr)
        return 2
    print(canonical(output).decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
