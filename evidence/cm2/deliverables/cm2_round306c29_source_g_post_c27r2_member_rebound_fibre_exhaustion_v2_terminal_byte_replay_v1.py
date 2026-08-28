#!/usr/bin/env python3
"""Sole independent byte-replay source permitted to mint C29-v2 authority.

Development of this source does not itself authorize C29.  Authority exists
only if a future fresh invocation produces the exact six-file terminal graph
after every conditional predecessor has passed.
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
AUDIT = ROOT / ".cm2-runtime/audit"
PREFIX = "cm2_round306c29_source_g_post_c27r2_member_rebound_fibre_exhaustion_v2"
BASE = "cm2.round306c29.source-g-post-c27r2-member-rebound-fibre-exhaustion.v2."
SEAL_SCHEMA = BASE + "release-terminal-seal-candidate.v1"
SEAL_STATUS = "PASS_CONDITIONAL_C29_V2_TERMINAL_SEAL_CANDIDATE__ZERO_CREDIT_PENDING_INDEPENDENT_BYTE_REPLAY"
OUTER_SCHEMA = BASE + "release-outer-verification.v1"
OUTER_STATUS = "PASS_INDEPENDENT_C29_V2_FULL_LEDGER_DUAL_PREDECESSOR_MANIFEST_COLD_AND_40_RELEASE_ATTACK_CHECK__CONDITIONAL_ZERO_CREDIT"
MANIFEST_SCHEMA = BASE + "release-manifest-receipt.v1"
TERMINAL_STATUS = "PASS_C29_V2_TERMINAL_BYTE_REPLAY__FORMAL_SOURCE_G_FIBRE_AUTHORITY_MINTED"
PASS_BYTES = b"PASS_C29_V2_SOURCE_G_FIBRE_AUTHORITY_TERMINAL_BYTE_REPLAY__SOURCE_W_UNCHANGED_CM2_NO_GO\n"
EXPECTED_MATH = {
    "members": 502_204, "representations": 549_616,
    "post_C27R2_components": 43_684, "official_keys": 124,
    "component_key_incidences": 60_296,
    "component_key_multiplicity_census": {
        "1": 27_108, "2": 16_556, "3": 8, "4": 8, "5": 4},
    "family_member_census": {"G2A": 5_264, "G2B": 10_128,
        "NON_GRAPH": 55_604, "PRESERVED": 126_468,
        "R2": 295_336, "R292": 9_404},
    "total_unordered_member_pairs": 126_104_177_706,
    "within_post_component_member_pairs": 542_179_508,
    "cross_post_component_member_pairs": 125_561_998_198,
}
CANDIDATE_FILES = sorted([
    PREFIX + "_global_member_disposition_ledger.jsonl.gz",
    PREFIX + "_official_key_fibre_exhaustion_ledger.jsonl.gz",
    PREFIX + "_post_component_official_key_assignment_ledger.jsonl.gz",
    PREFIX + "_result.json",
])


class Blocked(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Blocked(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def valid_sha(value: Any) -> bool:
    return type(value) is str and len(value) == 64 and all(
        char in "0123456789abcdef" for char in value)


def strict(payload: bytes) -> Any:
    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in items:
            need(type(key) is str and key not in result, "unique JSON key")
            result[key] = value
        return result
    return json.loads(payload, object_pairs_hook=pairs,
                      parse_constant=lambda token: (_ for _ in ()).throw(
                          ValueError(token)))


def fingerprint(value: os.stat_result) -> tuple[int, ...]:
    return (value.st_dev, value.st_ino, value.st_mode, value.st_nlink,
            value.st_size, value.st_mtime_ns, value.st_ctime_ns,
            value.st_uid, value.st_gid)


def file_sha(path: Path) -> str:
    path = path.absolute()
    need(path.resolve(strict=True) == path, "canonical path:" + str(path))
    descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
                         | getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(descriptor)
        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1,
             "regular singleton:" + str(path))
        state = hashlib.sha256()
        while block := os.read(descriptor, 4 << 20):
            state.update(block)
        need(fingerprint(os.fstat(descriptor)) == fingerprint(before),
             "stable SHA/stat:" + str(path))
        return state.hexdigest()
    finally:
        os.close(descriptor)


def document(path: Path, closure: str) -> dict[str, Any]:
    payload = path.read_bytes()
    need(payload.endswith(b"\n") and not payload.endswith(b"\n\n"),
         "JSON newline")
    value = strict(payload[:-1])
    need(type(value) is dict and canonical(value) == payload[:-1],
         "canonical JSON")
    body = dict(value)
    claim = body.pop(closure, None)
    need(valid_sha(claim) and claim == digest(body), "object closure")
    return value


def parse_manifest(path: Path) -> dict[str, str]:
    payload = path.read_bytes()
    need(payload.endswith(b"\n"), "manifest newline")
    result: dict[str, str] = {}
    for line in payload.decode("ascii").splitlines():
        fields = line.split("  ", 1)
        need(len(fields) == 2 and valid_sha(fields[0])
             and fields[1] not in result, "manifest row")
        relative = Path(fields[1])
        need(not relative.is_absolute() and str(relative) == fields[1]
             and all(part not in {"", ".", ".."} for part in relative.parts),
             "canonical manifest path")
        result[fields[1]] = fields[0]
    need(list(result) == sorted(result)
         and all(file_sha(ROOT / path) == sha for path, sha in result.items()),
         "manifest sorted/current")
    return result


def manifest(paths: set[Path]) -> bytes:
    rows = sorted((str(path.absolute().relative_to(ROOT)), file_sha(path))
                  for path in paths)
    need(len(rows) == len({path for path, _ in rows}), "manifest unique")
    return ("\n".join(f"{sha}  {path}" for path, sha in rows) + "\n").encode("ascii")


def write_once(path: Path, payload: bytes) -> None:
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL
                         | getattr(os, "O_NOFOLLOW", 0), 0o400)
    try:
        offset = 0
        while offset < len(payload):
            offset += os.write(descriptor, payload[offset:])
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def terminal_body(seal: dict[str, Any], outer: dict[str, Any],
                  payload_sha: str, root_sha: str) -> dict[str, Any]:
    return {"schema": BASE + "terminal-receipt.v1", "status": TERMINAL_STATUS,
        "seal_candidate_object_sha256": seal["seal_candidate_sha256"],
        "manifest_receipt_object_sha256": seal["manifest_receipt_object_sha256"],
        "payload_manifest_sha256": seal["payload_manifest_sha256"],
        "root_manifest_sha256": seal["root_manifest_sha256"],
        "outer_verification_object_sha256": outer["outer_verification_sha256"],
        "terminal_payload_manifest_sha256": payload_sha,
        "terminal_root_manifest_sha256": root_sha,
        "dual_predecessor_terminal_pins": outer["dual_predecessor_terminal_pins"],
        "exact_census": EXPECTED_MATH,
        "C25_fresh_component_id_historical_only": True,
        "legacy_C28_or_C29_authority_consumed": False,
        "terminal_replay_completed": True,
        "terminal_receipt_byte_replay_identical": True,
        "authority_minted": True, "formal_credit": 0,
        "manifest_authorized": True,
        "C29": "AUTHORIZED_TERMINAL_SOURCE_G_POST_C27R2_FIBRE_AUTHORITY",
        "Source_G": "REPAIRED_C29_V2_TERMINAL_AUTHORITY",
        "Source_W": "UNCHANGED_BY_SOURCE_G_C29_V2_TERMINAL",
        "D02": "BLOCKED_COMPOSITE", "D03": "UNAUTHORIZED",
        "D04": "NOT_MINTED", "Gate5": "10/18",
        "CM2": "NO-GO_FOR_CLAIM"}


def execute(args: argparse.Namespace) -> dict[str, Any]:
    pins = (args.expect_replay_sha256, args.expect_seal_candidate_file_sha256,
            args.expect_seal_candidate_object_sha256,
            args.expect_seal_payload_manifest_sha256,
            args.expect_seal_root_manifest_sha256,
            args.expect_outer_file_sha256, args.expect_outer_object_sha256,
            args.expect_manifest_receipt_file_sha256,
            args.expect_manifest_receipt_object_sha256)
    need(all(valid_sha(value) for value in pins)
         and file_sha(SELF) == args.expect_replay_sha256, "all replay/dynamic pins")
    control = Path(args.core_control_dir).absolute()
    cold_control = Path(args.cold_control_dir).absolute()
    evidence_dir = Path(args.evidence_dir).absolute()
    attacks_path = Path(args.release_attacks_file).absolute()
    manifest_dir = Path(args.manifest_dir).absolute()
    outer_path = Path(args.outer_file).absolute()
    seal_dir = Path(args.seal_dir).absolute()
    output = Path(args.output_dir).absolute()
    need(output.parent == AUDIT and not output.exists(), "fresh terminal output")
    need({entry.name for entry in manifest_dir.iterdir()} == {
             "manifest_receipt.json", "payload_manifest.sha256",
             "root_manifest.sha256"}
         and {entry.name for entry in seal_dir.iterdir()} == {
             "seal_candidate.json", "seal_payload_manifest.sha256",
             "seal_root_manifest.sha256"}, "manifest/seal exact inventory")
    receipt_path = manifest_dir / "manifest_receipt.json"
    payload_path = manifest_dir / "payload_manifest.sha256"
    root_path = manifest_dir / "root_manifest.sha256"
    seal_path = seal_dir / "seal_candidate.json"
    seal_payload = seal_dir / "seal_payload_manifest.sha256"
    seal_root = seal_dir / "seal_root_manifest.sha256"
    manifest_receipt = document(receipt_path, "manifest_receipt_sha256")
    outer = document(outer_path, "outer_verification_sha256")
    seal = document(seal_path, "seal_candidate_sha256")
    need(file_sha(receipt_path) == args.expect_manifest_receipt_file_sha256
         and manifest_receipt["manifest_receipt_sha256"]
             == args.expect_manifest_receipt_object_sha256
         and manifest_receipt.get("schema") == MANIFEST_SCHEMA
         and file_sha(outer_path) == args.expect_outer_file_sha256
         and outer["outer_verification_sha256"] == args.expect_outer_object_sha256
         and outer.get("schema") == OUTER_SCHEMA and outer.get("status") == OUTER_STATUS
         and file_sha(seal_path) == args.expect_seal_candidate_file_sha256
         and seal["seal_candidate_sha256"] == args.expect_seal_candidate_object_sha256
         and file_sha(seal_payload) == args.expect_seal_payload_manifest_sha256
         and file_sha(seal_root) == args.expect_seal_root_manifest_sha256
         and seal.get("schema") == SEAL_SCHEMA and seal.get("status") == SEAL_STATUS
         and seal.get("expected_terminal_status") == TERMINAL_STATUS
         and seal.get("exact_census") == EXPECTED_MATH
         and seal.get("terminal_replay_completed") is False
         and seal.get("authority_minted") is False
         and seal.get("manifest_authorized") is False
         and outer.get("exact_census") == EXPECTED_MATH
         and outer.get("formal_credit") == 0
         and outer.get("manifest_authorized") is False,
         "conditional seal/outer/manifests")
    for path in (payload_path, root_path, seal_payload, seal_root):
        parse_manifest(path)
    pinset = document(control / "pinset.json", "pinset_sha256")
    targets = {name: ROOT / raw for name, raw in pinset["targets"].items()}
    candidate = targets["candidate"]
    core_path = control / "core_receipt.json"
    cold_path = cold_control / "cold_replay_receipt.json"
    evidence_path = evidence_dir / "evidence_bundle.json"
    c27 = Path(pinset["C27R2_terminal"]["dir"]).absolute()
    c28 = Path(pinset["C28_terminal"]["dir"]).absolute()
    need(outer["dual_predecessor_terminal_pins"] == {
             "C27R2": manifest_receipt["C27R2_terminal_pins"],
             "C28": manifest_receipt["C28_terminal_pins"]},
         "dual predecessor pin identity")
    if args.preflight_only:
        return {"status": "PASS_C29_V2_SEAL_OUTER_MANIFEST_AND_FRESH_TERMINAL_PREFLIGHT__NO_OUTPUT_ZERO_CREDIT"}
    terminal_payload_members = {seal_path, seal_payload, seal_root, receipt_path,
        payload_path, root_path, outer_path, core_path, control / "PASS.lock",
        cold_path, cold_control / "PASS.lock", evidence_path, attacks_path, SELF}
    terminal_payload_members.update(candidate / name for name in CANDIDATE_FILES)
    for terminal in (c27, c28):
        terminal_payload_members.update({terminal / "root_manifest.sha256",
            terminal / "terminal_receipt.json", terminal / "terminal_replay.json",
            terminal / "PASS.lock"})
    output.mkdir(mode=0o700)
    terminal_payload_raw = manifest(terminal_payload_members)
    terminal_payload_path = output / "payload_manifest.sha256"
    write_once(terminal_payload_path, terminal_payload_raw)
    terminal_root_members = {terminal_payload_path, seal_root, root_path,
        core_path, control / "PASS.lock", cold_path, cold_control / "PASS.lock", SELF}
    for terminal in (c27, c28):
        terminal_root_members.update({terminal / "root_manifest.sha256",
            terminal / "terminal_receipt.json", terminal / "terminal_replay.json",
            terminal / "PASS.lock"})
    terminal_root_raw = manifest(terminal_root_members)
    terminal_root_path = output / "root_manifest.sha256"
    write_once(terminal_root_path, terminal_root_raw)
    first = terminal_body(seal, outer, file_sha(terminal_payload_path),
                          file_sha(terminal_root_path))
    second = terminal_body(dict(seal), dict(outer),
                           hashlib.sha256(terminal_payload_raw).hexdigest(),
                           hashlib.sha256(terminal_root_raw).hexdigest())
    need(first == second and canonical(first) == canonical(second),
         "independent terminal body byte replay")
    receipt = dict(first)
    receipt["terminal_receipt_sha256"] = digest(receipt)
    receipt_raw = canonical(receipt) + b"\n"
    terminal_receipt_path = output / "terminal_receipt.json"
    write_once(terminal_receipt_path, receipt_raw)
    need(terminal_receipt_path.read_bytes() == receipt_raw,
         "terminal receipt byte identity")
    replay_body = {"schema": BASE + "terminal-byte-replay.v1",
        "status": TERMINAL_STATUS,
        "terminal_receipt_file_sha256": file_sha(terminal_receipt_path),
        "terminal_receipt_object_sha256": receipt["terminal_receipt_sha256"],
        "terminal_payload_manifest_sha256": file_sha(terminal_payload_path),
        "terminal_root_manifest_sha256": file_sha(terminal_root_path),
        "terminal_receipt_byte_replay_identical": True,
        "dual_predecessor_terminal_pins": outer["dual_predecessor_terminal_pins"],
        "authority_minted": True, "formal_credit": 0,
        "manifest_authorized": True,
        "C29": "AUTHORIZED_TERMINAL_SOURCE_G_POST_C27R2_FIBRE_AUTHORITY",
        "Source_W": "UNCHANGED", "CM2": "NO-GO_FOR_CLAIM"}
    replay = dict(replay_body)
    replay["terminal_replay_sha256"] = digest(replay)
    replay_path = output / "terminal_replay.json"
    write_once(replay_path, canonical(replay) + b"\n")
    chain_body = {"schema": BASE + "release-chain-status.v1",
        "status": TERMINAL_STATUS,
        "terminal_receipt_file_sha256": file_sha(terminal_receipt_path),
        "terminal_receipt_object_sha256": receipt["terminal_receipt_sha256"],
        "terminal_replay_file_sha256": file_sha(replay_path),
        "terminal_replay_object_sha256": replay["terminal_replay_sha256"],
        "authority_minted": True, "formal_credit": 0,
        "manifest_authorized": True,
        "C29": "AUTHORIZED_TERMINAL_SOURCE_G_POST_C27R2_FIBRE_AUTHORITY",
        "Source_W": "UNCHANGED", "CM2": "NO-GO_FOR_CLAIM"}
    chain = dict(chain_body)
    chain["chain_status_sha256"] = digest(chain)
    write_once(output / "chain_status.json", canonical(chain) + b"\n")
    write_once(output / "PASS.lock", PASS_BYTES)
    need({entry.name for entry in output.iterdir()} == {"PASS.lock",
        "chain_status.json", "payload_manifest.sha256", "root_manifest.sha256",
        "terminal_receipt.json", "terminal_replay.json"}, "terminal inventory")
    return replay


def self_test() -> dict[str, Any]:
    seal = {"seal_candidate_sha256": "0" * 64,
            "manifest_receipt_object_sha256": "1" * 64,
            "payload_manifest_sha256": "2" * 64,
            "root_manifest_sha256": "3" * 64}
    outer = {"outer_verification_sha256": "4" * 64,
             "dual_predecessor_terminal_pins": {"C27R2": {}, "C28": {}}}
    first = terminal_body(seal, outer, "5" * 64, "6" * 64)
    second = terminal_body(dict(seal), dict(outer), "5" * 64, "6" * 64)
    need(canonical(first) == canonical(second), "terminal body fixture")
    return {"status": "PASS_C29_V2_TERMINAL_BYTE_REPLAY_SELF_TEST",
            "formal_credit": 0, "C29": "UNAUTHORIZED_NO_TERMINAL_RUN",
            "CM2": "NO-GO_FOR_CLAIM"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--preflight-only", action="store_true")
    for name in ("core-control-dir", "cold-control-dir", "evidence-dir",
                 "release-attacks-file", "manifest-dir", "outer-file",
                 "seal-dir", "output-dir", "expect-replay-sha256",
                 "expect-seal-candidate-file-sha256",
                 "expect-seal-candidate-object-sha256",
                 "expect-seal-payload-manifest-sha256",
                 "expect-seal-root-manifest-sha256",
                 "expect-outer-file-sha256", "expect-outer-object-sha256",
                 "expect-manifest-receipt-file-sha256",
                 "expect-manifest-receipt-object-sha256"):
        parser.add_argument("--" + name)
    args = parser.parse_args()
    fields = tuple(name.replace("-", "_") for name in (
        "core-control-dir", "cold-control-dir", "evidence-dir",
        "release-attacks-file", "manifest-dir", "outer-file", "seal-dir",
        "output-dir", "expect-replay-sha256",
        "expect-seal-candidate-file-sha256",
        "expect-seal-candidate-object-sha256",
        "expect-seal-payload-manifest-sha256",
        "expect-seal-root-manifest-sha256", "expect-outer-file-sha256",
        "expect-outer-object-sha256", "expect-manifest-receipt-file-sha256",
        "expect-manifest-receipt-object-sha256"))
    try:
        if args.self_test:
            need(not args.preflight_only
                 and all(getattr(args, field) is None for field in fields),
                 "self-test arguments")
            result = self_test()
        else:
            need(all(getattr(args, field) is not None for field in fields),
                 "run arguments")
            result = execute(args)
        sys.stdout.buffer.write(canonical({"CM2": "NO-GO_FOR_CLAIM",
            "formal_credit": 0, "status": result["status"]}) + b"\n")
        return 0
    except (Blocked, OSError, ValueError, KeyError, TypeError) as error:
        sys.stderr.write("REJECT:" + str(error) + "\n")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
