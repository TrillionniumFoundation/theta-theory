#!/usr/bin/env python3
"""Independently verify the C30c v5/v6 formal predecessor projection."""
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
ADAPTER = DELIVERABLES / "cm2_round306c30d_c30c_v3_predecessor_authority_adapter_v1.py"
ADAPTER_SHA256 = "f10613b8698997c99d3cece4f301cc89ea9f532f2d23c9d08325ef150b578503"
CONSUMER = DELIVERABLES / "cm2_round306c30c_formal_source_w_ledger_consumer_v1.py"
CONSUMER_SHA256 = "448c5f6bbd252e837bb8457dd3eaddbfca76c9755ddbafc07f91325d4bd29ba9"
PIN_SCHEMA = "cm2.round306c30d.c30c-v5-v6-formal-predecessor-dynamic-pins.v1"
PROJECTION_SCHEMA = "cm2.round306c30d.c30c-v5-v6-formal-predecessor-projection.v1"
PROJECTION_STATUS = (
    "PASS_EXACT_C30C_V5_V6_TERMINAL_AND_FORMAL_LEDGER_AS_C30D_PREDECESSOR__"
    "ZERO_C30D_FORMAL_CREDIT"
)
AUTHORITY_KIND = "C30C_V5_V6_PUBLICATION_TERMINAL_PLUS_CONSOLIDATED_FORMAL_LEDGER"
CANDIDATE_OBJECT = "df4531942e743389f5e8f85b2d013132f0808f562c21f430e7904577d67087d4"
ORIGIN_KEYS_OBJECT = "a928d0328e94ca98f04a0ee5d5d45ee0b75ee9ca2292afffe5c117880f0d5f93"
CHAIN_FILES = frozenset({
    "PUBLICATION_PASS.lock", "adapter_verification.json",
    "c30c_v5_v6_joint_publication_evidence.tar.gz", "chain_status.json",
    "evidence_index.json", "outer_verification.json", "payload_manifest.sha256",
    "root_manifest.sha256", "terminal_replay.json",
})
LEDGER_FILES = frozenset({
    "PASS.lock", "application_receipt.json", "hostile_audit.json",
    "root_manifest.sha256", "source_w_formal_ledger.json",
})
HEX64 = re.compile(r"[0-9a-f]{64}\Z")
PUBLICATION_MARKER = b"PASS_C30C_V5_V6_JOINT_PUBLICATION__SOURCE_W_80_TO_78__CM2_NO_GO\n"
LEDGER_MARKER = b"PASS_C30C_FORMAL_SOURCE_W_LEDGER_SINGLE_APPLICATION__80_TO_78__CM2_NO_GO\n"
ZERO = {
    "multi_Delta_cell_dispositions": 0,
    "multi_Delta_whole_cell_exclusions": 0,
    "resolved_source_W_origin_dispositions": 0,
    "whole_source_W_origin_exclusions": 0,
}
BEFORE = {
    "conservative_live": 2086,
    "excluded": 74746,
    "remaining": 80,
    "remaining_partition": {
        "compact_q": 54, "full_Delta": 2, "multi_Delta": 20,
        "reduced_live": 2, "retained_source_seams": 2,
    },
    "resolved_nonexcluded": 2006,
    "total": 76832,
}
AFTER = {
    "conservative_live": 2086,
    "excluded": 74746,
    "remaining": 78,
    "remaining_partition": {
        "compact_q": 54, "multi_Delta": 20, "reduced_live": 2,
        "retained_source_seams": 2,
    },
    "resolved_nonexcluded": 2008,
    "total": 76832,
}


class Reject(RuntimeError):
    pass


def require(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise Reject(label)


def wire(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=True, allow_nan=False, sort_keys=True,
                      separators=(",", ":")).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(wire(value)).hexdigest()


def checked(path: Path, label: str) -> Path:
    absolute = Path(os.path.abspath(os.fspath(path)))
    require(absolute.resolve(strict=True) == absolute, "path identity:" + label)
    return absolute


def bytes_once(path: Path, limit: int, label: str) -> bytes:
    absolute = checked(path, label)
    descriptor = os.open(absolute, os.O_RDONLY | os.O_CLOEXEC | getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(descriptor)
        require(stat.S_ISREG(before.st_mode) and before.st_nlink == 1
                and 0 <= before.st_size <= limit, "singleton:" + label)
        output = bytearray()
        while len(output) <= before.st_size:
            block = os.read(descriptor, min(2 << 20, before.st_size + 1 - len(output)))
            if not block:
                break
            output.extend(block)
        after = os.fstat(descriptor)
    finally:
        os.close(descriptor)
    identity = lambda item: (item.st_dev, item.st_ino, item.st_mode, item.st_nlink,
                             item.st_uid, item.st_gid, item.st_size, item.st_mtime_ns,
                             item.st_ctime_ns)
    require(len(output) == before.st_size and identity(before) == identity(after),
            "stable bytes:" + label)
    return bytes(output)


def sha(path: Path) -> str:
    state = hashlib.sha256()
    with checked(path, "hash").open("rb") as stream:
        while block := stream.read(2 << 20):
            state.update(block)
    return state.hexdigest()


def strict(raw: bytes, label: str) -> dict[str, Any]:
    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        output: dict[str, Any] = {}
        for key, value in pairs:
            require(type(key) is str and key not in output, "duplicate JSON:" + label)
            output[key] = value
        return output

    try:
        value = json.loads(raw.decode("ascii"), object_pairs_hook=unique,
                           parse_constant=lambda token: (_ for _ in ()).throw(ValueError(token)))
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as error:
        raise Reject("JSON syntax:" + label) from error
    require(type(value) is dict and raw in {wire(value), wire(value) + b"\n"},
            "canonical JSON:" + label)
    return value


def closed(path: Path, field: str, label: str) -> dict[str, Any]:
    value = strict(bytes_once(path, 64 << 20, label), label)
    body = dict(value)
    observed = body.pop(field, None)
    require(type(observed) is str and HEX64.fullmatch(observed) is not None
            and digest(body) == observed, "closure:" + label)
    return value


def manifest(path: Path, label: str) -> dict[str, str]:
    raw = bytes_once(path, 16 << 20, label)
    output: dict[str, str] = {}
    for row in raw.decode("ascii").splitlines():
        match = re.fullmatch(r"([0-9a-f]{64})  ([A-Za-z0-9_.-]+)", row)
        require(match is not None and match.group(2) not in output, "manifest:" + label)
        output[match.group(2)] = match.group(1)
    require(bool(output) and raw.endswith(b"\n"), "manifest suffix:" + label)
    return output


def parse_pins(path: Path) -> tuple[dict[str, Any], str, str]:
    raw = bytes_once(path, 8 << 20, "pins")
    value = strict(raw, "pins")
    body = dict(value)
    object_sha = body.pop("pinset_object_sha256", None)
    require(set(body) == {
        "schema", "chain_relative_path", "chain_members",
        "publication_audit_relative_path", "publication_audit",
        "ledger_relative_path", "ledger_members",
        "ledger_verification_relative_path", "ledger_verification",
    } and body.get("schema") == PIN_SCHEMA and object_sha == digest(body),
            "pin object")
    require(type(body["chain_members"]) is dict and set(body["chain_members"]) == CHAIN_FILES
            and type(body["ledger_members"]) is dict
            and set(body["ledger_members"]) == LEDGER_FILES, "pin inventories")
    for descriptor in [*body["chain_members"].values(), *body["ledger_members"].values(),
                       body["publication_audit"], body["ledger_verification"]]:
        require(type(descriptor) is dict and set(descriptor) == {"sha256", "size"}
                and type(descriptor["sha256"]) is str
                and HEX64.fullmatch(descriptor["sha256"]) is not None
                and type(descriptor["size"]) is int and descriptor["size"] >= 0,
                "pin descriptor")
    return body, object_sha, hashlib.sha256(raw).hexdigest()


def relative_path(value: Any, label: str) -> Path:
    require(type(value) is str and value != "", "relative path:" + label)
    path = checked(WORKSPACE / value, label)
    require(path.is_relative_to(WORKSPACE), "path confinement:" + label)
    return path


def descriptor(path: Path, expected: Mapping[str, Any], label: str) -> None:
    info = path.lstat()
    require(stat.S_ISREG(info.st_mode) and info.st_nlink == 1 and not path.is_symlink()
            and info.st_size == expected.get("size") and sha(path) == expected.get("sha256"),
            "pin replay:" + label)


def bus_environment() -> dict[str, str]:
    runtime = Path(f"/run/user/{os.getuid()}")
    bus = runtime / "bus"
    require(runtime.is_dir() and not runtime.is_symlink()
            and stat.S_ISSOCK(bus.lstat().st_mode) and not bus.is_symlink(), "user bus")
    return {
        "PATH": "/usr/bin:/bin", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8",
        "TZ": "UTC", "PYTHONDONTWRITEBYTECODE": "1",
        "XDG_RUNTIME_DIR": os.fspath(runtime),
        "DBUS_SESSION_BUS_ADDRESS": "unix:path=" + os.fspath(bus),
    }


def run_json(program: Path, arguments: list[str], expected_sha: str,
             label: str) -> dict[str, Any]:
    require(sha(program) == expected_sha, "source pin:" + label)
    completed = subprocess.run(["/usr/bin/python3", "-I", "-B", os.fspath(program),
                                *arguments], cwd=WORKSPACE, env=bus_environment(),
                               stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, check=False)
    require(completed.returncode == 0 and completed.stderr == b"", "process:" + label)
    return strict(completed.stdout, "stdout:" + label)


def expected_projection(facts: Mapping[str, Any], pin_file: str,
                        pin_object: str) -> dict[str, Any]:
    terminal = facts["terminal"]
    status = facts["status"]
    publication = facts["publication"]
    ledger = facts["ledger"]
    application = facts["application"]
    verification = facts["verification"]
    return {
        "schema": PROJECTION_SCHEMA,
        "status": PROJECTION_STATUS,
        "authority": {
            "kind": AUTHORITY_KIND,
            "chain_relative_path": facts["chain_relative"],
            "formal_ledger_relative_path": facts["ledger_relative"],
            "dynamic_pinset_file_sha256": pin_file,
            "dynamic_pinset_object_sha256": pin_object,
            "payload_manifest_sha256": facts["payload_sha"],
            "root_manifest_sha256": facts["root_sha"],
            "outer_verification_sha256": facts["outer_sha"],
            "terminal_replay_sha256": facts["terminal_sha"],
            "terminal_replay_object_sha256": terminal["object_sha256"],
            "chain_status_sha256": facts["status_sha"],
            "chain_status_object_sha256": status["object_sha256"],
            "publication_independent_audit_object_sha256": publication["object_sha256"],
            "formal_ledger_object_sha256": ledger["object_sha256"],
            "formal_ledger_application_object_sha256": application["object_sha256"],
            "formal_ledger_independent_verification_object_sha256": verification["object_sha256"],
            "formal_ledger_transition_id": application["transition_id"],
            "candidate_result_object_sha256": CANDIDATE_OBJECT,
            "candidate_origin_keys_sha256": ORIGIN_KEYS_OBJECT,
        },
        "predecessor_formal_handoff": {
            "transition": {"before": 80, "after": 78},
            "before": BEFORE,
            "after": AFTER,
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
        "formal_credit": ZERO,
        "source_W_formal_remainder": 78,
        "source_W_transition_authorized_by_this_projection": False,
        "D02": "BLOCKED_COMPOSITE",
        "D03": "UNAUTHORIZED",
        "D04": "NOT_MINTED",
        "Gate5": "10/18",
        "CM2": "NO-GO_FOR_CLAIM",
    }


def verify(chain_dir: Path, pins_path: Path) -> dict[str, Any]:
    pins, pin_object, pin_file = parse_pins(pins_path)
    chain = checked(chain_dir, "chain")
    ledger = relative_path(pins["ledger_relative_path"], "ledger")
    publication_path = relative_path(pins["publication_audit_relative_path"], "publication")
    verification_path = relative_path(pins["ledger_verification_relative_path"], "verification")
    require(chain == relative_path(pins["chain_relative_path"], "pinned chain")
            and not chain.is_symlink() and not ledger.is_symlink()
            and {entry.name for entry in chain.iterdir()} == CHAIN_FILES
            and {entry.name for entry in ledger.iterdir()} == LEDGER_FILES,
            "directory topology")
    for name, value in pins["chain_members"].items():
        descriptor(chain / name, value, "chain:" + name)
    for name, value in pins["ledger_members"].items():
        descriptor(ledger / name, value, "ledger:" + name)
    descriptor(publication_path, pins["publication_audit"], "publication")
    descriptor(verification_path, pins["ledger_verification"], "verification")
    terminal = closed(chain / "terminal_replay.json", "object_sha256", "terminal")
    status = closed(chain / "chain_status.json", "object_sha256", "status")
    publication = closed(publication_path, "object_sha256", "publication")
    ledger_object = closed(ledger / "source_w_formal_ledger.json", "object_sha256", "ledger")
    application = closed(ledger / "application_receipt.json", "object_sha256", "application")
    hostile = closed(ledger / "hostile_audit.json", "object_sha256", "hostile")
    verification = closed(verification_path, "object_sha256", "verification")
    payload_sha = sha(chain / "payload_manifest.sha256")
    root_sha = sha(chain / "root_manifest.sha256")
    terminal_sha = sha(chain / "terminal_replay.json")
    status_sha = sha(chain / "chain_status.json")
    outer_sha = sha(chain / "outer_verification.json")
    require(terminal.get("schema") ==
            "cm2.round306c30c.v5-v6-joint-publication-terminal-replay.v1"
            and terminal.get("status") == "PASS_TERMINAL_REPLAY__FORMAL_SOURCE_W_80_TO_78"
            and terminal.get("candidate_result_object_sha256") == CANDIDATE_OBJECT
            and terminal.get("source_W_transition") == {"before": 80, "after": 78}
            and terminal.get("source_W_formal_remainder") == 78
            and terminal.get("source_W_transition_authorized") is True
            and terminal.get("payload_manifest_sha256") == payload_sha
            and terminal.get("root_manifest_sha256") == root_sha, "terminal authority")
    require(status.get("terminal_replay_object_sha256") == terminal["object_sha256"]
            and publication.get("terminal_replay_object_sha256") == terminal["object_sha256"]
            and publication.get("chain_status_object_sha256") == status["object_sha256"],
            "publication closure")
    require(ledger_object.get("status") ==
            "PASS_CONSOLIDATED_SOURCE_W_FORMAL_LEDGER__REMAINDER_78"
            and ledger_object.get("current_state") == AFTER
            and ledger_object.get("applied_transition_ids") == [application.get("transition_id")]
            and application.get("ledger_object_sha256") == ledger_object["object_sha256"]
            and application.get("hostile_audit_object_sha256") == hostile["object_sha256"]
            and application.get("negative_test_count") == 9
            and verification.get("ledger_object_sha256") == ledger_object["object_sha256"]
            and verification.get("application_receipt_object_sha256") == application["object_sha256"]
            and verification.get("hostile_audit_object_sha256") == hostile["object_sha256"],
            "ledger closure")
    require(manifest(chain / "root_manifest.sha256", "chain root") == {
                "payload_manifest.sha256": payload_sha}
            and manifest(ledger / "root_manifest.sha256", "ledger root") == {
                "source_w_formal_ledger.json": sha(ledger / "source_w_formal_ledger.json"),
                "hostile_audit.json": sha(ledger / "hostile_audit.json"),
                "application_receipt.json": sha(ledger / "application_receipt.json"),
            }
            and bytes_once(chain / "PUBLICATION_PASS.lock", 256, "publication marker")
                == PUBLICATION_MARKER
            and bytes_once(ledger / "PASS.lock", 256, "ledger marker") == LEDGER_MARKER,
            "manifest/marker closure")
    replay = run_json(CONSUMER, ["--verify", "--output-dir", os.fspath(ledger)],
                      CONSUMER_SHA256, "consumer")
    require(replay == verification, "consumer replay identity")
    facts = {
        "chain_relative": pins["chain_relative_path"],
        "ledger_relative": pins["ledger_relative_path"],
        "payload_sha": payload_sha,
        "root_sha": root_sha,
        "outer_sha": outer_sha,
        "terminal_sha": terminal_sha,
        "status_sha": status_sha,
        "terminal": terminal,
        "status": status,
        "publication": publication,
        "ledger": ledger_object,
        "application": application,
        "verification": verification,
    }
    expected = expected_projection(facts, pin_file, pin_object)
    adapter_output = run_json(ADAPTER, ["--chain-dir", os.fspath(chain),
                                       "--dynamic-pins", os.fspath(pins_path)],
                              ADAPTER_SHA256, "adapter")
    require(adapter_output == expected, "independent/adapter projection identity")
    return expected


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--chain-dir", required=True, type=Path)
    parser.add_argument("--dynamic-pins", type=Path)
    parser.add_argument("--negative-missing-terminal-test", action="store_true")
    args = parser.parse_args()
    try:
        if args.negative_missing_terminal_test:
            require(not (args.chain_dir / "terminal_replay.json").is_file(),
                    "negative fixture unexpectedly has terminal")
            raise Reject("C30C_V5_V6_TERMINAL_INCOMPLETE:terminal_replay.json")
        require(args.dynamic_pins is not None, "dynamic pins required")
        output = verify(args.chain_dir, args.dynamic_pins)
    except (Reject, OSError, ValueError, TypeError, KeyError,
            subprocess.SubprocessError) as error:
        output = {
            "schema": PROJECTION_SCHEMA,
            "status": "BLOCKED_FAIL_CLOSED",
            "error": str(error),
            "formal_credit": ZERO,
            "source_W_formal_remainder": 78,
            "source_W_transition_authorized_by_this_projection": False,
            "CM2": "NO-GO_FOR_CLAIM",
        }
        sys.stdout.buffer.write(wire(output) + b"\n")
        return 1
    sys.stdout.buffer.write(wire(output) + b"\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
