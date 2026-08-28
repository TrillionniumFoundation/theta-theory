#!/usr/bin/env python3
"""Build a conditional C27R2 repair seal and anticipated terminal bytes.

No authority or PASS is produced.  The anticipated terminal receipt is exact
canonical future bytes, but only the separate no-import terminal replay may
reconstruct those bytes independently and mint repaired C27R2 authority.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import sys
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
SELF = Path(__file__).resolve()
BASE = "cm2.round306c27r2.source-g-authority-v2.release-repair."
MANIFEST_SCHEMA = BASE + "manifest-receipt.v3"
OUTER_SCHEMA = BASE + "outer-verification.v3"
SEAL_SCHEMA = BASE + "conditional-terminal-seal.v3"
SEAL_STATUS = ("PASS_CONDITIONAL_C27R2_RELEASE_REPAIR_SEAL_AND_ANTICIPATED_"
               "TERMINAL_BYTES__ZERO_CREDIT_PENDING_INDEPENDENT_REPLAY")
TERMINAL_SCHEMA = BASE + "terminal-receipt.v3"
TERMINAL_STATUS = ("PASS_C27R2_RELEASE_REPAIR_INDEPENDENT_TERMINAL_BYTE_"
                   "REPLAY__FORMAL_C27R2_AUTHORITY_REPAIRED")
EXPECTED = {"frozen_C15_components": 57_876,
            "post_C27R2_components": 43_684,
            "proof_derived_component_edges": 14_860,
            "successful_DSU_merges": 14_192, "cycle_edges": 668,
            "frozen_C15_members": 502_204,
            "total_unordered_member_pairs": 126_104_177_706,
            "within_post_component_member_pairs": 542_179_508,
            "cross_post_component_member_pairs": 125_561_998_198}
CANDIDATE = {"member_to_post_component.jsonl.gz",
             "old_c15_component_to_post_component.jsonl.gz",
             "post_component_census.jsonl.gz", "result.json"}


class Blocked(RuntimeError): pass


def need(v: bool, label: str) -> None:
    if type(v) is not bool or not v: raise Blocked(label)


def canonical(v: Any) -> bytes:
    return json.dumps(v, sort_keys=True, separators=(",", ":"),
        ensure_ascii=True, allow_nan=False).encode("ascii")


def digest(v: Any) -> str: return hashlib.sha256(canonical(v)).hexdigest()


def sha(v: Any) -> bool:
    return type(v) is str and re.fullmatch(r"[0-9a-f]{64}", v) is not None


def strict(raw: bytes) -> Any:
    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        out: dict[str, Any] = {}
        for k, v in items: need(k not in out, "duplicate key"); out[k] = v
        return out
    return json.loads(raw, object_pairs_hook=pairs,
        parse_constant=lambda x: (_ for _ in ()).throw(Blocked(x)))


def inside(raw: str | Path, absent: bool = False) -> Path:
    supplied = Path(raw); path = (supplied if supplied.is_absolute()
        else ROOT / supplied).absolute()
    try: rel = path.relative_to(ROOT)
    except ValueError as error: raise Blocked("outside workspace") from error
    need(rel.parts and all(x not in {"", ".", ".."} for x in rel.parts),
         "canonical path")
    cursor = ROOT
    for part in rel.parts:
        cursor /= part
        if not cursor.exists(): need(absent, "missing path"); break
        need(not cursor.is_symlink(), "symlink path")
    return path


def fp(s: os.stat_result) -> list[int]:
    return [s.st_dev, s.st_ino, s.st_mode, s.st_nlink, s.st_size,
            s.st_mtime_ns, s.st_ctime_ns, s.st_uid, s.st_gid]


def rec(path: Path) -> dict[str, Any]:
    need(path.is_file() and not path.is_symlink(), "regular file")
    fd = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(fd); need(stat.S_ISREG(before.st_mode)
            and before.st_nlink == 1, "single-link")
        h = hashlib.sha256()
        while block := os.read(fd, 4 << 20): h.update(block)
        need(fp(os.stat(path, follow_symlinks=False)) == fp(before), "stable file")
        return {"path": str(path.relative_to(ROOT)), "sha256": h.hexdigest(),
                "size": before.st_size, "stat_fingerprint": fp(before)}
    finally: os.close(fd)


def doc(path: Path, closure: str) -> tuple[dict[str, Any], dict[str, Any]]:
    r = rec(path); raw = path.read_bytes(); need(raw.endswith(b"\n"), "newline")
    v = strict(raw[:-1]); need(type(v) is dict and canonical(v) == raw[:-1],
        "canonical JSON")
    body = dict(v); claim = body.pop(closure, None)
    need(sha(claim) and claim == digest(body), "object closure")
    return v, r


def manifest(path: Path) -> dict[str, dict[str, Any]]:
    raw = path.read_bytes(); need(raw.endswith(b"\n"), "manifest newline")
    out: dict[str, dict[str, Any]] = {}
    for line in raw.decode("ascii").splitlines():
        m = re.fullmatch(r"([0-9a-f]{64})  ([^\x00\r\n]+)", line)
        need(m is not None, "manifest row"); claim, shown = m.groups()
        need(shown not in out, "duplicate path")
        item = rec(inside(shown)); need(item["sha256"] == claim, "manifest SHA")
        out[shown] = item
    need(out and list(out) == sorted(out), "sorted manifest"); return out


def manifest_bytes(paths: set[Path], virtual: dict[Path, str] | None = None) -> bytes:
    virtual = virtual or {}; rows = []
    for path in sorted(paths | set(virtual)):
        value = virtual.get(path, rec(path)["sha256"] if path not in virtual else "")
        need(sha(value), "manifest virtual/current SHA")
        rows.append(f"{value}  {path.relative_to(ROOT)}\n")
    need(rows, "nonempty manifest"); return "".join(rows).encode("ascii")


def write(path: Path, raw: bytes) -> None:
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL
                 | getattr(os, "O_NOFOLLOW", 0), 0o400)
    try: os.write(fd, raw); os.fsync(fd)
    finally: os.close(fd)


def terminal_body(manifest_receipt: dict[str, Any], outer: dict[str, Any],
                  seal_file: str, seal_object: str, seal_payload: str,
                  seal_root: str, terminal_payload: str, terminal_root: str,
                  terminal_replay_source_sha: str) -> dict[str, Any]:
    return {"schema": TERMINAL_SCHEMA, "status": TERMINAL_STATUS,
        "manifest_receipt_file_sha256": outer["manifest_receipt_file_sha256"],
        "manifest_receipt_object_sha256":
            outer["manifest_receipt_object_sha256"],
        "outer_verification_file_sha256": outer["outer_verification_file_sha256"],
        "outer_verification_object_sha256": outer["outer_verification_sha256"],
        "seal_candidate_file_sha256": seal_file,
        "seal_candidate_object_sha256": seal_object,
        "seal_payload_manifest_file_sha256": seal_payload,
        "seal_root_manifest_file_sha256": seal_root,
        "terminal_payload_manifest_file_sha256": terminal_payload,
        "terminal_root_manifest_file_sha256": terminal_root,
        "terminal_replay_source_sha256": terminal_replay_source_sha,
        "core_receipt_file_sha256": manifest_receipt["core_receipt_file_sha256"],
        "core_receipt_object_sha256": manifest_receipt["core_receipt_object_sha256"],
        "candidate_result_file_sha256":
            manifest_receipt["candidate_result_file_sha256"],
        "candidate_result_object_sha256":
            manifest_receipt["candidate_result_object_sha256"],
        "candidate_file_sha256": manifest_receipt["candidate_file_sha256"],
        "actual_v2_terminal_role": "PREDECESSOR_EVIDENCE_ONLY",
        "actual_v2_terminal_authority_eligible": False,
        "historical_C27R2_terminal": manifest_receipt["historical_C27R2_terminal"],
        "same_core_and_candidate_as_historical_terminal": True,
        "exact_math": EXPECTED, "terminal_replay_completed": True,
        "terminal_receipt_byte_replay_identical": True,
        "authority_minted": True, "formal_credit": 0,
        "manifest_authorized": True, "C27R2": "FORMAL_AUTHORITY_REPAIRED",
        "C28": "UNAUTHORIZED_PENDING_REPAIR_COMPATIBILITY_REBIND",
        "C29": "UNAUTHORIZED_PENDING_REPAIR_COMPATIBILITY_REBIND",
        "CM2": "NO-GO_FOR_CLAIM"}


def execute(a: argparse.Namespace) -> dict[str, Any]:
    pins = (a.expect_self_sha256, a.expect_manifest_receipt_file_sha256,
        a.expect_manifest_receipt_object_sha256,
        a.expect_payload_manifest_sha256, a.expect_root_manifest_sha256,
        a.expect_outer_file_sha256, a.expect_outer_object_sha256,
        a.expect_terminal_replay_source_sha256)
    need(all(sha(x) for x in pins) and rec(SELF)["sha256"]
         == a.expect_self_sha256, "dynamic SHA/self pins")
    manifest_dir = inside(a.manifest_dir)
    mr, mrr = doc(manifest_dir / "manifest_receipt.json",
                  "manifest_receipt_sha256")
    payload_path = manifest_dir / "payload_manifest.sha256"
    root_path = manifest_dir / "root_manifest.sha256"
    payload = manifest(payload_path); root = manifest(root_path)
    need(mrr["sha256"] == a.expect_manifest_receipt_file_sha256
         and mr["manifest_receipt_sha256"]
             == a.expect_manifest_receipt_object_sha256
         and mr.get("schema") == MANIFEST_SCHEMA and mr.get("exact_math") == EXPECTED
         and rec(payload_path)["sha256"] == a.expect_payload_manifest_sha256
         and rec(root_path)["sha256"] == a.expect_root_manifest_sha256
         and mr.get("payload_member_count") == len(payload)
         and mr.get("root_member_count") == len(root)
         and mr.get("historical_C27R2_terminal", {}).get("authority_eligible") is False
         and mr.get("formal_credit") == 0, "manifest boundary")
    outer_path = inside(a.outer_file)
    outer, outer_record = doc(outer_path, "outer_verification_sha256")
    need(outer_record["sha256"] == a.expect_outer_file_sha256
         and outer["outer_verification_sha256"] == a.expect_outer_object_sha256
         and outer.get("schema") == OUTER_SCHEMA and outer.get("exact_math") == EXPECTED
         and outer.get("no_core_or_builder_import_or_execution") is True
         and outer.get("streamed_three_candidate_ledgers_and_actual_v2_edge_ledger") is True
         and outer.get("outer_is_conditional_until_independent_terminal_byte_replay") is True
         and outer.get("formal_credit") == 0 and outer.get("authority_minted") is False,
         "outer conditional boundary")
    # Inject current outer file SHA for the terminal body without altering outer.
    outer = {**outer, "outer_verification_file_sha256": outer_record["sha256"]}
    candidate = inside(a.candidate_dir); need(candidate.is_dir()
        and {x.name for x in candidate.iterdir()} == CANDIDATE, "candidate inventory")
    terminal_source = inside(a.terminal_replay_source)
    need(rec(terminal_source)["sha256"] == a.expect_terminal_replay_source_sha256
         and rec(terminal_source)["path"] in payload, "terminal replay source pin")
    output = inside(a.output_dir, True); anticipated = inside(
        a.anticipated_terminal_dir, True)
    need(not output.exists() and not anticipated.exists()
         and output.parent == anticipated.parent and output != anticipated,
         "fresh seal/anticipated terminal paths")
    if a.preflight_only:
        return {"status": "PASS_C27R2_REPAIR_SEAL_V3_PREFLIGHT_NO_OUTPUT"}
    output.mkdir(parents=True, mode=0o700)
    seal_payload_path = output / "seal_payload_manifest.sha256"
    seal_payload_raw = manifest_bytes({manifest_dir / "manifest_receipt.json",
        payload_path, root_path, outer_path, SELF, terminal_source})
    write(seal_payload_path, seal_payload_raw)
    seal_root_path = output / "seal_root_manifest.sha256"
    seal_root_raw = manifest_bytes({seal_payload_path, root_path, outer_path,
                                    terminal_source})
    write(seal_root_path, seal_root_raw)
    seal_body = {"schema": SEAL_SCHEMA, "status": SEAL_STATUS,
        "manifest_receipt_file_sha256": mrr["sha256"],
        "manifest_receipt_object_sha256": mr["manifest_receipt_sha256"],
        "outer_verification_file_sha256": outer_record["sha256"],
        "outer_verification_object_sha256": outer["outer_verification_sha256"],
        "seal_payload_manifest_file_sha256": rec(seal_payload_path)["sha256"],
        "seal_root_manifest_file_sha256": rec(seal_root_path)["sha256"],
        "anticipated_terminal_dir": str(anticipated.relative_to(ROOT)),
        "terminal_replay_source_sha256": a.expect_terminal_replay_source_sha256,
        "core_receipt_file_sha256": mr["core_receipt_file_sha256"],
        "core_receipt_object_sha256": mr["core_receipt_object_sha256"],
        "candidate_file_sha256": mr["candidate_file_sha256"],
        "historical_C27R2_terminal": mr["historical_C27R2_terminal"],
        "exact_math": EXPECTED, "terminal_replay_completed": False,
        "authority_minted": False, "formal_credit": 0,
        "manifest_authorized": False, "C27R2": "AUDIT_HOLD_UNAUTHORIZED",
        "C28_C29": "UNAUTHORIZED", "CM2": "NO-GO_FOR_CLAIM"}
    seal = {**seal_body, "seal_candidate_sha256": digest(seal_body)}
    seal_path = output / "seal_candidate.json"
    write(seal_path, canonical(seal) + b"\n")

    post_dir = inside(a.post_evidence_dir)
    terminal_payload_paths = {seal_path, seal_payload_path, seal_root_path,
        manifest_dir / "manifest_receipt.json", payload_path, root_path,
        outer_path, post_dir / "post_attack_evidence.json",
        post_dir / "authority_inventory.sha256", terminal_source}
    terminal_payload_paths |= {candidate / name for name in CANDIDATE}
    terminal_payload_raw = manifest_bytes(terminal_payload_paths)
    terminal_payload_sha = hashlib.sha256(terminal_payload_raw).hexdigest()
    future_payload_path = anticipated / "payload_manifest.sha256"
    terminal_root_raw = manifest_bytes({seal_root_path, root_path, outer_path},
        {future_payload_path: terminal_payload_sha})
    terminal_root_sha = hashlib.sha256(terminal_root_raw).hexdigest()
    body = terminal_body(mr, outer, rec(seal_path)["sha256"],
        seal["seal_candidate_sha256"], rec(seal_payload_path)["sha256"],
        rec(seal_root_path)["sha256"], terminal_payload_sha, terminal_root_sha,
        a.expect_terminal_replay_source_sha256)
    anticipated_receipt = {**body, "terminal_receipt_sha256": digest(body)}
    anticipated_path = output / "anticipated_terminal_receipt.json"
    write(anticipated_path, canonical(anticipated_receipt) + b"\n")
    need({x.name for x in output.iterdir()} == {"seal_candidate.json",
        "seal_payload_manifest.sha256", "seal_root_manifest.sha256",
        "anticipated_terminal_receipt.json"}, "seal output inventory")
    return seal


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=__doc__); p.add_argument("--self-test", action="store_true")
    p.add_argument("--preflight-only", action="store_true")
    names = ("manifest-dir", "outer-file", "candidate-dir", "post-evidence-dir",
        "terminal-replay-source", "output-dir", "anticipated-terminal-dir",
        "expect-self-sha256", "expect-manifest-receipt-file-sha256",
        "expect-manifest-receipt-object-sha256", "expect-payload-manifest-sha256",
        "expect-root-manifest-sha256", "expect-outer-file-sha256",
        "expect-outer-object-sha256", "expect-terminal-replay-source-sha256")
    for name in names: p.add_argument("--" + name)
    return p


def main() -> int:
    p = parser(); a = p.parse_args(); names = [x.dest for x in p._actions
        if x.dest not in {"help", "self_test", "preflight_only"}]
    try:
        if a.self_test:
            need(not a.preflight_only and all(getattr(a, x) is None for x in names),
                 "self-test no args")
            fake_manifest = {"core_receipt_file_sha256": "1" * 64,
                "core_receipt_object_sha256": "2" * 64,
                "candidate_result_file_sha256": "3" * 64,
                "candidate_result_object_sha256": "4" * 64,
                "candidate_file_sha256": {}, "historical_C27R2_terminal": {}}
            fake_outer = {"manifest_receipt_file_sha256": "5" * 64,
                "manifest_receipt_object_sha256": "6" * 64,
                "outer_verification_file_sha256": "7" * 64,
                "outer_verification_sha256": "8" * 64}
            one = terminal_body(fake_manifest, fake_outer, "9" * 64,
                "a" * 64, "b" * 64, "c" * 64, "d" * 64, "e" * 64,
                "f" * 64)
            need(one["authority_minted"] is True
                 and one["historical_C27R2_terminal"] == {}, "template fixture")
            out = {"status": "PASS_C27R2_RELEASE_REPAIR_SEAL_V3_SELF_TEST"}
        else:
            need(all(getattr(a, x) is not None for x in names), "all pins required")
            out = execute(a)
        sys.stdout.buffer.write(canonical({"CM2": "NO-GO_FOR_CLAIM",
            "formal_credit": 0, "status": out["status"]}) + b"\n"); return 0
    except (Blocked, OSError, ValueError, KeyError, TypeError) as e:
        sys.stderr.write("REJECT:" + str(e) + "\n"); return 2


if __name__ == "__main__": raise SystemExit(main())
