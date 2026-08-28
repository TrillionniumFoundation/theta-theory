#!/usr/bin/env python3
"""Adapt the C30c v5/v6 terminal plus formal ledger for C30d-v3."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import stat
import subprocess
import sys
from pathlib import Path
from typing import Any, Mapping

sys.dont_write_bytecode = True

DELIVERABLES = Path(__file__).resolve().parent
WORKSPACE = DELIVERABLES.parent
AUDIT_ROOT = WORKSPACE / ".cm2-runtime/audit"
CONSUMER = DELIVERABLES / "cm2_round306c30c_formal_source_w_ledger_consumer_v1.py"
CONSUMER_SHA256 = "448c5f6bbd252e837bb8457dd3eaddbfca76c9755ddbafc07f91325d4bd29ba9"
PIN_SCHEMA = "cm2.round306c30d.c30c-v5-v6-formal-predecessor-dynamic-pins.v1"
PROJECTION_SCHEMA = "cm2.round306c30d.c30c-v5-v6-formal-predecessor-projection.v1"
PROJECTION_STATUS = (
    "PASS_EXACT_C30C_V5_V6_TERMINAL_AND_FORMAL_LEDGER_AS_C30D_PREDECESSOR__"
    "ZERO_C30D_FORMAL_CREDIT"
)
AUTHORITY_KIND = "C30C_V5_V6_PUBLICATION_TERMINAL_PLUS_CONSOLIDATED_FORMAL_LEDGER"
C30C_RESULT_OBJECT_SHA256 = "df4531942e743389f5e8f85b2d013132f0808f562c21f430e7904577d67087d4"
C30C_ORIGIN_KEYS_SHA256 = "a928d0328e94ca98f04a0ee5d5d45ee0b75ee9ca2292afffe5c117880f0d5f93"
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
CHAIN_PATTERN = re.compile(
    r"\.cm2-runtime/audit/c30c-publication-v5-v6-chain-[0-9]{8}T[0-9]{6}Z-[0-9a-f]{16}\Z"
)
LEDGER_PATTERN = re.compile(
    r"\.cm2-runtime/audit/c30c-formal-source-w-ledger-[0-9]{8}T[0-9]{6}Z-[0-9a-f]{16}\Z"
)
HEX64 = re.compile(r"[0-9a-f]{64}\Z")
PASS_PUBLICATION = b"PASS_C30C_V5_V6_JOINT_PUBLICATION__SOURCE_W_80_TO_78__CM2_NO_GO\n"
PASS_LEDGER = b"PASS_C30C_FORMAL_SOURCE_W_LEDGER_SINGLE_APPLICATION__80_TO_78__CM2_NO_GO\n"
ZERO_C30D = {
    "multi_Delta_cell_dispositions": 0,
    "multi_Delta_whole_cell_exclusions": 0,
    "resolved_source_W_origin_dispositions": 0,
    "whole_source_W_origin_exclusions": 0,
}
BEFORE_80 = {
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
AFTER_78 = {
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


class Blocked(RuntimeError):
    pass


def need(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise Blocked(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=True, allow_nan=False, sort_keys=True,
                      separators=(",", ":")).encode("ascii")


def object_digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def fingerprint(value: os.stat_result) -> tuple[int, ...]:
    return (value.st_dev, value.st_ino, value.st_mode, value.st_nlink,
            value.st_uid, value.st_gid, value.st_size, value.st_mtime_ns,
            value.st_ctime_ns)


def canonical_path(path: Path, label: str) -> Path:
    absolute = Path(os.path.abspath(os.fspath(path)))
    need(absolute.resolve(strict=True) == absolute, "canonical path:" + label)
    return absolute


def capture(path: Path, maximum: int, label: str) -> bytes:
    absolute = canonical_path(path, label)
    descriptor = os.open(absolute, os.O_RDONLY | os.O_CLOEXEC | getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(descriptor)
        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1
             and 0 <= before.st_size <= maximum, "regular singleton:" + label)
        output = bytearray()
        while len(output) <= before.st_size:
            block = os.read(descriptor, min(4 << 20, before.st_size + 1 - len(output)))
            if not block:
                break
            output.extend(block)
        after = os.fstat(descriptor)
    finally:
        os.close(descriptor)
    need(len(output) == before.st_size and fingerprint(before) == fingerprint(after),
         "stable capture:" + label)
    return bytes(output)


def file_sha(path: Path) -> str:
    state = hashlib.sha256()
    with canonical_path(path, "hash").open("rb") as stream:
        while block := stream.read(4 << 20):
            state.update(block)
    return state.hexdigest()


def strict_object(raw: bytes, label: str) -> dict[str, Any]:
    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        output: dict[str, Any] = {}
        for key, value in pairs:
            need(type(key) is str and key not in output, "unique JSON key:" + label)
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


def closed_object(path: Path, field: str, label: str) -> dict[str, Any]:
    value = strict_object(capture(path, 64 << 20, label), label)
    body = dict(value)
    observed = body.pop(field, None)
    need(type(observed) is str and HEX64.fullmatch(observed) is not None
         and object_digest(body) == observed, "object closure:" + label)
    return value


def parse_manifest(path: Path, label: str) -> dict[str, str]:
    raw = capture(path, 16 << 20, label)
    output: dict[str, str] = {}
    for row in raw.decode("ascii").splitlines():
        match = re.fullmatch(r"([0-9a-f]{64})  ([A-Za-z0-9_.-]+)", row)
        need(match is not None and match.group(2) not in output, "manifest row:" + label)
        output[match.group(2)] = match.group(1)
    need(bool(output) and raw.endswith(b"\n"), "manifest termination:" + label)
    return output


def dynamic_pins(path: Path) -> tuple[dict[str, Any], str, str]:
    raw = capture(path, 8 << 20, "dynamic pins")
    value = strict_object(raw, "dynamic pins")
    body = dict(value)
    observed = body.pop("pinset_object_sha256", None)
    need(set(body) == {
        "schema", "chain_relative_path", "chain_members",
        "publication_audit_relative_path", "publication_audit",
        "ledger_relative_path", "ledger_members",
        "ledger_verification_relative_path", "ledger_verification",
    } and body.get("schema") == PIN_SCHEMA
         and type(observed) is str and observed == object_digest(body),
         "dynamic pinset closure")
    need(type(body["chain_relative_path"]) is str
         and CHAIN_PATTERN.fullmatch(body["chain_relative_path"]) is not None
         and type(body["ledger_relative_path"]) is str
         and LEDGER_PATTERN.fullmatch(body["ledger_relative_path"]) is not None,
         "dynamic authority paths")
    expected_publication = (
        ".cm2-runtime/receipts/" + Path(body["chain_relative_path"]).name
        + "/independent_audit.json"
    )
    expected_ledger_verification = (
        ".cm2-runtime/receipts/" + Path(body["ledger_relative_path"]).name
        + "/independent_verification.json"
    )
    need(body["publication_audit_relative_path"] == expected_publication
         and body["ledger_verification_relative_path"] == expected_ledger_verification,
         "receipt authority paths")
    need(type(body["chain_members"]) is dict
         and set(body["chain_members"]) == CHAIN_FILES
         and type(body["ledger_members"]) is dict
         and set(body["ledger_members"]) == LEDGER_FILES,
         "dynamic member inventories")
    for descriptor in [*body["chain_members"].values(), *body["ledger_members"].values(),
                       body["publication_audit"], body["ledger_verification"]]:
        need(type(descriptor) is dict and set(descriptor) == {"sha256", "size"}
             and type(descriptor["sha256"]) is str
             and HEX64.fullmatch(descriptor["sha256"]) is not None
             and type(descriptor["size"]) is int and descriptor["size"] >= 0,
             "dynamic member descriptor")
    return body, observed, hashlib.sha256(raw).hexdigest()


def resolve_relative(value: str, label: str) -> Path:
    path = canonical_path(WORKSPACE / value, label)
    need(path.is_relative_to(WORKSPACE), "confined path:" + label)
    return path


def validate_descriptor(path: Path, descriptor: Mapping[str, Any], label: str) -> None:
    info = path.lstat()
    need(stat.S_ISREG(info.st_mode) and info.st_nlink == 1 and not path.is_symlink()
         and info.st_size == descriptor.get("size")
         and file_sha(path) == descriptor.get("sha256"), "dynamic pin:" + label)


def consumer_replay(ledger: Path) -> dict[str, Any]:
    need(file_sha(CONSUMER) == CONSUMER_SHA256, "formal-ledger consumer source pin")
    runtime = Path(f"/run/user/{os.getuid()}")
    bus = runtime / "bus"
    need(runtime.is_dir() and not runtime.is_symlink()
         and stat.S_ISSOCK(bus.lstat().st_mode) and not bus.is_symlink(), "canonical user bus")
    environment = {
        "PATH": "/usr/bin:/bin",
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "TZ": "UTC",
        "PYTHONDONTWRITEBYTECODE": "1",
        "XDG_RUNTIME_DIR": os.fspath(runtime),
        "DBUS_SESSION_BUS_ADDRESS": "unix:path=" + os.fspath(bus),
    }
    completed = subprocess.run([
        "/usr/bin/python3", "-I", "-B", os.fspath(CONSUMER),
        "--verify", "--output-dir", os.fspath(ledger),
    ], cwd=WORKSPACE, env=environment, stdin=subprocess.DEVNULL,
       stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    need(completed.returncode == 0 and completed.stderr == b"", "formal-ledger live replay")
    value = strict_object(completed.stdout, "formal-ledger replay stdout")
    body = dict(value)
    observed = body.pop("object_sha256", None)
    need(type(observed) is str and object_digest(body) == observed
         and value.get("status") == "PASS_FULL_LEDGER_AUTHORITY_LIVE_UNIT_AND_9_NEGATIVE_REPLAY"
         and value.get("source_W_formal_remainder") == 78
         and value.get("source_W_transition_authorized") is True,
         "formal-ledger replay authority")
    return value


def projection(authority: Mapping[str, Any], pin_file_sha: str,
               pin_object_sha: str) -> dict[str, Any]:
    ledger = authority["ledger"]
    application = authority["application"]
    terminal = authority["terminal"]
    publication_audit = authority["publication_audit"]
    ledger_verification = authority["ledger_verification"]
    chain_status = authority["chain_status"]
    return {
        "schema": PROJECTION_SCHEMA,
        "status": PROJECTION_STATUS,
        "authority": {
            "kind": AUTHORITY_KIND,
            "chain_relative_path": authority["chain_relative"],
            "formal_ledger_relative_path": authority["ledger_relative"],
            "dynamic_pinset_file_sha256": pin_file_sha,
            "dynamic_pinset_object_sha256": pin_object_sha,
            "payload_manifest_sha256": authority["payload_sha256"],
            "root_manifest_sha256": authority["root_sha256"],
            "outer_verification_sha256": authority["outer_sha256"],
            "terminal_replay_sha256": authority["terminal_sha256"],
            "terminal_replay_object_sha256": terminal["object_sha256"],
            "chain_status_sha256": authority["chain_status_sha256"],
            "chain_status_object_sha256": chain_status["object_sha256"],
            "publication_independent_audit_object_sha256": publication_audit["object_sha256"],
            "formal_ledger_object_sha256": ledger["object_sha256"],
            "formal_ledger_application_object_sha256": application["object_sha256"],
            "formal_ledger_independent_verification_object_sha256":
                ledger_verification["object_sha256"],
            "formal_ledger_transition_id": application["transition_id"],
            "candidate_result_object_sha256": C30C_RESULT_OBJECT_SHA256,
            "candidate_origin_keys_sha256": C30C_ORIGIN_KEYS_SHA256,
        },
        "predecessor_formal_handoff": {
            "transition": {"before": 80, "after": 78},
            "before": BEFORE_80,
            "after": AFTER_78,
            "credit": {
                "resolved_source_W_origin_dispositions": 2,
                "resolved_nonexcluded": 2,
                "whole_source_W_origin_exclusions": 0,
            },
            "C30c_transition_authorized": True,
        },
        "C30d_boundary": {
            "formal_starting_remainder": 78,
            "proposed_after_remainder": 58,
            "mathematical_producer_executed": False,
            "candidate_created": False,
            "result_created": False,
            "manifest_created": False,
            "seal_created": False,
            "C30d_transition_authorized": False,
        },
        "formal_credit": ZERO_C30D,
        "source_W_formal_remainder": 78,
        "source_W_transition_authorized_by_this_projection": False,
        "D02": "BLOCKED_COMPOSITE",
        "D03": "UNAUTHORIZED",
        "D04": "NOT_MINTED",
        "Gate5": "10/18",
        "CM2": "NO-GO_FOR_CLAIM",
    }


def validate_projection(value: Mapping[str, Any]) -> None:
    authority = value.get("authority")
    handoff = value.get("predecessor_formal_handoff")
    boundary = value.get("C30d_boundary")
    need(value.get("schema") == PROJECTION_SCHEMA and value.get("status") == PROJECTION_STATUS
         and type(authority) is dict and authority.get("kind") == AUTHORITY_KIND
         and authority.get("candidate_result_object_sha256") == C30C_RESULT_OBJECT_SHA256
         and type(handoff) is dict and handoff.get("before") == BEFORE_80
         and handoff.get("after") == AFTER_78
         and handoff.get("transition") == {"before": 80, "after": 78}
         and handoff.get("C30c_transition_authorized") is True
         and type(boundary) is dict and boundary.get("formal_starting_remainder") == 78
         and boundary.get("proposed_after_remainder") == 58
         and boundary.get("C30d_transition_authorized") is False
         and value.get("formal_credit") == ZERO_C30D
         and value.get("source_W_formal_remainder") == 78
         and value.get("source_W_transition_authorized_by_this_projection") is False
         and value.get("D02") == "BLOCKED_COMPOSITE"
         and value.get("D03") == "UNAUTHORIZED"
         and value.get("D04") == "NOT_MINTED"
         and value.get("Gate5") == "10/18"
         and value.get("CM2") == "NO-GO_FOR_CLAIM", "projection boundary")


def validate(chain_dir: Path, pins_path: Path) -> dict[str, Any]:
    pins, pin_object_sha, pin_file_sha = dynamic_pins(pins_path)
    chain = canonical_path(chain_dir, "chain")
    ledger = resolve_relative(pins["ledger_relative_path"], "formal ledger")
    publication_audit_path = resolve_relative(pins["publication_audit_relative_path"],
                                              "publication audit")
    ledger_verification_path = resolve_relative(pins["ledger_verification_relative_path"],
                                                "ledger verification")
    need(chain == resolve_relative(pins["chain_relative_path"], "pinned chain")
         and chain.parent == AUDIT_ROOT and ledger.parent == AUDIT_ROOT
         and not chain.is_symlink() and not ledger.is_symlink()
         and {entry.name for entry in chain.iterdir()} == CHAIN_FILES
         and {entry.name for entry in ledger.iterdir()} == LEDGER_FILES,
         "exact authority directories")
    for name, descriptor in pins["chain_members"].items():
        validate_descriptor(chain / name, descriptor, "chain:" + name)
    for name, descriptor in pins["ledger_members"].items():
        validate_descriptor(ledger / name, descriptor, "ledger:" + name)
    validate_descriptor(publication_audit_path, pins["publication_audit"], "publication audit")
    validate_descriptor(ledger_verification_path, pins["ledger_verification"], "ledger verification")
    terminal = closed_object(chain / "terminal_replay.json", "object_sha256", "terminal")
    chain_status = closed_object(chain / "chain_status.json", "object_sha256", "chain status")
    publication_audit = closed_object(publication_audit_path, "object_sha256", "publication audit")
    formal_ledger = closed_object(ledger / "source_w_formal_ledger.json", "object_sha256",
                                  "formal ledger")
    application = closed_object(ledger / "application_receipt.json", "object_sha256", "application")
    hostile = closed_object(ledger / "hostile_audit.json", "object_sha256", "hostile audit")
    ledger_verification = closed_object(ledger_verification_path, "object_sha256",
                                        "ledger verification")
    payload_sha = file_sha(chain / "payload_manifest.sha256")
    root_sha = file_sha(chain / "root_manifest.sha256")
    outer_sha = file_sha(chain / "outer_verification.json")
    terminal_sha = file_sha(chain / "terminal_replay.json")
    chain_status_sha = file_sha(chain / "chain_status.json")
    need(terminal.get("schema") ==
         "cm2.round306c30c.v5-v6-joint-publication-terminal-replay.v1"
         and terminal.get("status") == "PASS_TERMINAL_REPLAY__FORMAL_SOURCE_W_80_TO_78"
         and terminal.get("candidate_result_object_sha256") == C30C_RESULT_OBJECT_SHA256
         and terminal.get("source_W_transition") == {"before": 80, "after": 78}
         and terminal.get("source_W_formal_remainder") == 78
         and terminal.get("source_W_transition_authorized") is True
         and terminal.get("payload_manifest_sha256") == payload_sha
         and terminal.get("root_manifest_sha256") == root_sha,
         "exact C30c terminal")
    need(chain_status.get("status") ==
         "PASS_C30C_V5_V6_JOINT_PUBLICATION__FORMAL_SOURCE_W_80_TO_78"
         and chain_status.get("terminal_replay_object_sha256") == terminal["object_sha256"]
         and publication_audit.get("status") ==
         "PASS_FULL_TAR_MANIFEST_OBJECT_UNIT_AND_LIVE_ADAPTER_REPLAY"
         and publication_audit.get("terminal_replay_object_sha256") == terminal["object_sha256"]
         and publication_audit.get("chain_status_object_sha256") == chain_status["object_sha256"],
         "publication audit binding")
    need(formal_ledger.get("status") ==
         "PASS_CONSOLIDATED_SOURCE_W_FORMAL_LEDGER__REMAINDER_78"
         and formal_ledger.get("current_state") == AFTER_78
         and formal_ledger.get("applied_transition_ids") == [application.get("transition_id")]
         and application.get("status") ==
         "PASS_C30C_FORMAL_LEDGER_SINGLE_APPLICATION__SOURCE_W_80_TO_78"
         and application.get("ledger_object_sha256") == formal_ledger["object_sha256"]
         and application.get("hostile_audit_object_sha256") == hostile["object_sha256"]
         and application.get("negative_test_count") == 9
         and ledger_verification.get("status") ==
         "PASS_FULL_LEDGER_AUTHORITY_LIVE_UNIT_AND_9_NEGATIVE_REPLAY"
         and ledger_verification.get("ledger_object_sha256") == formal_ledger["object_sha256"]
         and ledger_verification.get("application_receipt_object_sha256") == application["object_sha256"]
         and ledger_verification.get("hostile_audit_object_sha256") == hostile["object_sha256"],
         "formal ledger authority binding")
    need(parse_manifest(chain / "root_manifest.sha256", "chain root") == {
             "payload_manifest.sha256": payload_sha}
         and parse_manifest(ledger / "root_manifest.sha256", "ledger root") == {
             "source_w_formal_ledger.json": file_sha(ledger / "source_w_formal_ledger.json"),
             "hostile_audit.json": file_sha(ledger / "hostile_audit.json"),
             "application_receipt.json": file_sha(ledger / "application_receipt.json"),
         }
         and capture(chain / "PUBLICATION_PASS.lock", 256, "publication marker") == PASS_PUBLICATION
         and capture(ledger / "PASS.lock", 256, "ledger marker") == PASS_LEDGER,
         "manifest and marker closure")
    replay = consumer_replay(ledger)
    need(replay == ledger_verification, "persisted/live formal-ledger verification identity")
    authority = {
        "chain_relative": pins["chain_relative_path"],
        "ledger_relative": pins["ledger_relative_path"],
        "payload_sha256": payload_sha,
        "root_sha256": root_sha,
        "outer_sha256": outer_sha,
        "terminal_sha256": terminal_sha,
        "chain_status_sha256": chain_status_sha,
        "terminal": terminal,
        "chain_status": chain_status,
        "publication_audit": publication_audit,
        "ledger": formal_ledger,
        "application": application,
        "ledger_verification": ledger_verification,
    }
    output = projection(authority, pin_file_sha, pin_object_sha)
    validate_projection(output)
    return output


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--chain-dir", required=True, type=Path)
    parser.add_argument("--dynamic-pins", type=Path)
    parser.add_argument("--negative-missing-terminal-test", action="store_true")
    args = parser.parse_args()
    try:
        if args.negative_missing_terminal_test:
            need(not (args.chain_dir / "terminal_replay.json").is_file(),
                 "negative fixture unexpectedly has terminal")
            raise Blocked("C30C_V5_V6_TERMINAL_INCOMPLETE:terminal_replay.json")
        need(args.dynamic_pins is not None, "dynamic pins required")
        output = validate(args.chain_dir, args.dynamic_pins)
    except (Blocked, OSError, ValueError, TypeError, KeyError,
            subprocess.SubprocessError) as error:
        output = {
            "schema": PROJECTION_SCHEMA,
            "status": "BLOCKED_FAIL_CLOSED",
            "error": str(error),
            "formal_credit": ZERO_C30D,
            "source_W_formal_remainder": 78,
            "source_W_transition_authorized_by_this_projection": False,
            "CM2": "NO-GO_FOR_CLAIM",
        }
        sys.stdout.buffer.write(canonical(output) + b"\n")
        return 1
    sys.stdout.buffer.write(canonical(output) + b"\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
