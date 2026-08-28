#!/usr/bin/env python3
"""Terminal seal and byte-for-byte cold replay for the C30c v3 handoff.

The terminal seal itself is zero credit.  Only after a fresh outer checker
execution is byte-identical and the complete payload/root graph is unchanged
does terminal_replay.json authorize the formal Source-W 80 -> 78 transition.
CM2, D02, D03, and D04 remain blocked.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import stat
import subprocess
from pathlib import Path
from typing import Any

WORKSPACE = Path("/home/qian-qi/.openclaw/workspaces/telegram-bot-8449317572")
DELIVERABLES = WORKSPACE / "deliverables"
PREFIX = "cm2_round306c30c_source_w_full_delta_whole_origin_disposition"
OUTER = DELIVERABLES / (PREFIX + "_formal_handoff_outer_verifier_v3.py")
C30B_MANIFEST_REL = (
    "deliverables/cm2_round306c30b_source_w_outgoing_h_whole_origin_"
    "disposition_manifest.sha256"
)
C30B_MANIFEST_SHA256 = "6af636a4239f390712d057030f03e09fbbca332c6170f183d3d0095f19f0f248"
C30B_VERIFICATION_SHA256 = "e9e72536be9ba707fe2fdf6034b47978be4d09235e5133414ec7b0a31acf4e71"
RESULT_OBJECT_SHA256 = "df4531942e743389f5e8f85b2d013132f0808f562c21f430e7904577d67087d4"
OUTER_SCHEMA = "cm2.round306c30c.v3-formal-handoff-outer-verification.v1"
OUTER_STATUS = "PASS_INDEPENDENT_OUTER_MATHEMATICAL_CHECK__CONDITIONAL_80_TO_78"


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


def capture(path: Path, maximum: int = 64 << 30) -> tuple[bytes, tuple[int, ...]]:
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
    return b"".join(chunks), identity(before)


def hash_identity(path: Path) -> tuple[str, tuple[int, ...]]:
    absolute = Path(os.path.abspath(os.fspath(path)))
    need(absolute.resolve(strict=True) == absolute, "canonical hash path:" + os.fspath(path))
    descriptor = os.open(absolute, os.O_RDONLY | os.O_CLOEXEC |
                         getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(descriptor)
        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1,
             "hash singleton:" + os.fspath(path))
        state = hashlib.sha256()
        total = 0
        while block := os.read(descriptor, 4 << 20):
            state.update(block)
            total += len(block)
        after = os.fstat(descriptor)
    finally:
        os.close(descriptor)
    need(identity(before) == identity(after) and total == before.st_size,
         "stable hash:" + os.fspath(path))
    return state.hexdigest(), identity(before)


def sha(path: Path) -> str:
    return hash_identity(path)[0]


def strict_object(raw: bytes, label: str) -> dict[str, Any]:
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


def parse_manifest(path: Path) -> tuple[bytes, dict[str, str]]:
    raw, _ = capture(path, 8 << 20)
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
                         for name in sorted(rows)), "sorted manifest:" + path.name)
    return raw, rows


def verify_graph(chain_dir: Path) -> tuple[dict[str, tuple[int, ...]], dict[str, str]]:
    payload_raw, payload = parse_manifest(chain_dir / "payload_manifest.sha256")
    identities: dict[str, tuple[int, ...]] = {}
    for relative, expected in payload.items():
        path = WORKSPACE / relative
        need(path.resolve(strict=True).is_relative_to(WORKSPACE.resolve(strict=True)),
             "payload containment:" + relative)
        item_hash, item_identity = hash_identity(path)
        need(item_hash == expected, "payload hash:" + relative)
        identities[relative] = item_identity
    root_raw, root = parse_manifest(chain_dir / "root_manifest.sha256")
    chain_rel = chain_dir.relative_to(WORKSPACE).as_posix()
    need(root == {chain_rel + "/payload_manifest.sha256":
                  hashlib.sha256(payload_raw).hexdigest(),
                  C30B_MANIFEST_REL: C30B_MANIFEST_SHA256}, "exact root authority")
    need(payload.get("deliverables/" + OUTER.name) == sha(OUTER),
         "outer checker pinned by payload")
    need(payload.get("deliverables/" + Path(__file__).name) == sha(Path(__file__)),
         "terminal checker pinned by payload")
    return identities, {"payload": hashlib.sha256(payload_raw).hexdigest(),
                        "root": hashlib.sha256(root_raw).hexdigest()}


def validate_outer(raw: bytes, manifests: dict[str, str]) -> dict[str, Any]:
    value = strict_object(raw, "outer verification")
    authority = value.get("round306c30b_authority", {})
    handoff = value.get("formal_handoff", {})
    mathematics = value.get("mathematics", {})
    need(value.get("schema") == OUTER_SCHEMA and value.get("status") == OUTER_STATUS
         and authority == {"manifest_sha256": C30B_MANIFEST_SHA256,
                           "verification_sha256": C30B_VERIFICATION_SHA256,
                           "formal_source_W_remaining": 80}
         and value.get("manifests") == {"payload_manifest_sha256": manifests["payload"],
                                        "root_manifest_sha256": manifests["root"]}
         and mathematics.get("candidate_result_object_sha256") == RESULT_OBJECT_SHA256
         and mathematics.get("whole_origin_dispositions") ==
             {"RESOLVED_MIXED": 2, "EXCLUDED": 0}
         and handoff == {"before": {"remaining": 80},
                         "conditional_after": {"remaining": 78},
                         "resolved_nonexcluded_credit": 2,
                         "whole_origin_exclusion_credit": 0}
         and value.get("terminal_replay_required") is True
         and value.get("formal_credit") == 0
         and value.get("source_W_formal_remainder") == 80
         and value.get("source_W_transition_authorized") is False
         and value.get("D02") == "BLOCKED_COMPOSITE"
         and value.get("D03") == "UNAUTHORIZED"
         and value.get("D04") == "NOT_MINTED"
         and value.get("CM2") == "NO-GO_FOR_CLAIM",
         "exact conditional outer conclusion")
    return value


def exclusive(path: Path, raw: bytes) -> None:
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_CLOEXEC, 0o400)
    try:
        view = memoryview(raw)
        while view:
            count = os.write(descriptor, view)
            need(count > 0, "complete write:" + path.name)
            view = view[count:]
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def run(chain_dir: Path) -> dict[str, Any]:
    before_identities, manifests = verify_graph(chain_dir)
    outer_path = chain_dir / "outer_verification.json"
    outer_raw, outer_identity = capture(outer_path, 64 << 20)
    validate_outer(outer_raw, manifests)
    seal = {
        "schema": "cm2.round306c30c.v3-terminal-seal.v1",
        "status": "PASS_CONDITIONAL_TERMINAL_SEAL__ZERO_FORMAL_CREDIT__REPLAY_REQUIRED",
        "payload_manifest_sha256": manifests["payload"],
        "root_manifest_sha256": manifests["root"],
        "outer_verification_sha256": hashlib.sha256(outer_raw).hexdigest(),
        "round306c30b_manifest_sha256": C30B_MANIFEST_SHA256,
        "candidate_result_object_sha256": RESULT_OBJECT_SHA256,
        "conditional_source_W_transition": "80->78",
        "formal_credit": 0,
        "source_W_formal_remainder": 80,
        "source_W_transition_authorized": False,
        "CM2": "NO-GO_FOR_CLAIM",
    }
    seal_raw = canonical(seal) + b"\n"
    seal_path = chain_dir / "terminal_seal_receipt.json"
    exclusive(seal_path, seal_raw)
    completed = subprocess.run(
        ["/usr/bin/python3", "-I", "-B", os.fspath(OUTER),
         "--chain-dir", os.fspath(chain_dir)], cwd=WORKSPACE,
        env={"HOME": "/nonexistent", "LC_ALL": "C.UTF-8", "TZ": "UTC",
             "PATH": "/usr/bin:/bin", "PYTHONDONTWRITEBYTECODE": "1"},
        stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        check=False,
    )
    need(completed.returncode == 0 and completed.stderr == b"",
         "terminal outer cold replay execution")
    need(completed.stdout == outer_raw, "terminal outer replay byte identity")
    after_identities, after_manifests = verify_graph(chain_dir)
    need(before_identities == after_identities and manifests == after_manifests,
         "payload graph TOCTOU identity")
    need(capture(outer_path, 64 << 20) == (outer_raw, outer_identity),
         "outer receipt TOCTOU identity")
    output = {
        "schema": "cm2.round306c30c.v3-terminal-replay.v1",
        "status": "PASS_TERMINAL_REPLAY__FORMAL_SOURCE_W_80_TO_78",
        "terminal_seal_sha256": hashlib.sha256(seal_raw).hexdigest(),
        "payload_manifest_sha256": manifests["payload"],
        "root_manifest_sha256": manifests["root"],
        "outer_verification_sha256": hashlib.sha256(outer_raw).hexdigest(),
        "outer_replay_stdout_sha256": hashlib.sha256(completed.stdout).hexdigest(),
        "round306c30b_manifest_sha256": C30B_MANIFEST_SHA256,
        "round306c30b_verification_sha256": C30B_VERIFICATION_SHA256,
        "candidate_result_object_sha256": RESULT_OBJECT_SHA256,
        "source_W_transition": {"before": 80, "after": 78},
        "formal_credit": {"resolved_source_W_origin_dispositions": 2,
                          "resolved_nonexcluded": 2,
                          "whole_source_W_origin_exclusions": 0},
        "source_W_formal_remainder": 78,
        "source_W_transition_authorized": True,
        "D02": "BLOCKED_COMPOSITE",
        "D03": "UNAUTHORIZED",
        "D04": "NOT_MINTED",
        "Gate5": "10/18",
        "CM2": "NO-GO_FOR_CLAIM",
    }
    exclusive(chain_dir / "terminal_replay.json", canonical(output) + b"\n")
    return output


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--chain-dir", required=True, type=Path)
    arguments = parser.parse_args()
    try:
        output = run(arguments.chain_dir.resolve(strict=True))
    except (Blocked, OSError, ValueError, TypeError, KeyError,
            subprocess.SubprocessError) as error:
        print(canonical({"schema": "cm2.round306c30c.v3-terminal-replay.v1",
                         "status": "BLOCKED_FAIL_CLOSED", "error": str(error),
                         "formal_credit": 0, "source_W_formal_remainder": 80,
                         "source_W_transition_authorized": False,
                         "CM2": "NO-GO_FOR_CLAIM"}).decode("ascii"))
        return 1
    print(canonical(output).decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
